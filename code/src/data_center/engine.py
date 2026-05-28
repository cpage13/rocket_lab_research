"""The GPU-first valuation engine — YAML config in, typed v8 artifact out.

This module is the deterministic computation. Given a
:class:`data_center.config.ValuationConfig`, it picks a frontier generation
for each fiscal year, applies the GPU-first formulas to derive per-year
per-node economics, rolls the living fleet up by cohort, and returns a typed
v8 :class:`data_center.output.ValuationOutput`.

The GPU-first per-node formulas (the heart of the model):

    mass_per_pkg = kg/1000 + kW × (solar_t_per_kW + radiator_t_per_kW)
            N    = floor((mass_envelope − node_mass_fixed) / mass_per_pkg)
       node_kW   = N × kW/pkg
   compute_cost  = N × $/pkg
    node_total   = compute + bus + solar + radiator + launch_cost(cadence)
  cost_annual    = node_total / service_life
   revenue_R     = cost_annual × R(launch_year, band)

The radiator t/kW steps at the Tjmax-lift year (D11): the hot-loop coolant
arrives at year 5 and radiator-mass-per-kW drops (0.013 -> 0.012, cycle-2).
Launch cost is cadence-indexed (SOURCE_INDEX NTR-009): a log-linear curve over
the launches-per-year the logistic cadence ramp produces. Bus cost compounds
at `bus_growth_pre` through `bus_flatten_after_yr`, then holds flat (D12).

The fleet rollup vintages each calendar year's launches into a
:class:`data_center.fleet.Cohort` and sums the living set (5-year hard cliff,
D1). Revenue is an R band — low / central / high (D18) — so every
revenue / gross-profit / margin figure surfaces as a three-way split.

Cycle-2 v8 output: the artifact has five top-level keys
(``metadata`` / ``inputs`` / ``physical`` / ``business`` / ``meta``); every
leaf numeric is a :class:`data_center.provenance.ProvenanceCell`. The
v8 assembly (metadata + inputs + meta + the final ``ValuationOutput``) is
delegated to :func:`data_center.json_output.build_output`.

References:
    plan_05_20_cycle2.md § 5 — Phase 4A (v8 output + JSON emit).
    strategy_05_20_cycle2.md § 3 — the v8 schema.
    tests/test_parity.py — the frozen-trajectory parity test.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import UTC, datetime

from .cadence import compute_launch_cost_musd, compute_launches_per_year
from .config import GospelInputs, RBand, ValuationConfig
from .constants import KG_PER_T, USD_PER_MUSD
from .fleet import Cohort, FleetYear, compute_fleet_year, r_at_year
from .generations import (
    KNOWN_GENS,
    GenerationSpec,
    extend_generations,
    frontier_at,
)
from .output import BusinessYear, CostBreakdownBlock, PhysicalYear, ValuationOutput
from .provenance import FieldPath, ProvenanceCell, cell
from .volume import (
    VolumeBreakdown,
    compute_binding_constraint,
    compute_solar_area_per_pkg,
    compute_volume_per_node,
    compute_volume_per_pkg,
    compute_volume_utilization,
)

# ---------------------------------------------------------------------------
# Per-year helpers
# ---------------------------------------------------------------------------


def radiator_t_per_kw_for_year(year_idx: int, gospel: GospelInputs) -> float:
    """Return the radiator t/kW prevailing in a given model year (D11).

    Steps from `radiator_t_per_kw_pre` to `radiator_t_per_kw_post` at
    `tjmax_lift_year` — the hot-loop coolant arrives and radiator mass per
    kW drops.

    Args:
        year_idx: Zero-based model year index.
        gospel: The locked gospel anchors (provides the pre/post dials).

    Returns:
        The radiator t/kW in effect for the year.
    """
    if year_idx >= gospel.tjmax_lift_year:
        return gospel.radiator_t_per_kw_post
    return gospel.radiator_t_per_kw_pre


def bus_cost_for_year(year_idx: int, gospel: GospelInputs) -> float:
    """Bus cost in a given model year ($M).

    Compounds at `bus_growth_pre` (typically a gentle decline) through
    `bus_flatten_after_yr`, then holds flat at that level (D12).

    Args:
        year_idx: Zero-based model year index.
        gospel: The locked gospel anchors (provides the bus dials).

    Returns:
        The per-node bus cost for the year, $M.
    """
    pre_years = min(year_idx, gospel.bus_flatten_after_yr)
    return gospel.bus_base_musd * (1.0 + gospel.bus_growth_pre) ** pre_years


# ---------------------------------------------------------------------------
# Typed unwrap helpers
# ---------------------------------------------------------------------------


def _cell_float(c: ProvenanceCell) -> float:
    """Unwrap a numeric :class:`ProvenanceCell` to a plain ``float``.

    Args:
        c: A ProvenanceCell whose ``value`` is numeric.

    Returns:
        The cell's value as a ``float``.

    Raises:
        TypeError: If the cell's value is not a real number.
    """
    if isinstance(c.value, bool) or not isinstance(c.value, (int, float)):
        raise TypeError(f"ProvenanceCell {c.formula_name!r} is not numeric: {c.value!r}")
    return float(c.value)


def _cell_int(c: ProvenanceCell) -> int:
    """Unwrap an integer :class:`ProvenanceCell` to a plain ``int``.

    Args:
        c: A ProvenanceCell whose ``value`` is an integer.

    Returns:
        The cell's value as an ``int``.

    Raises:
        TypeError: If the cell's value is not an integer.
    """
    if isinstance(c.value, bool) or not isinstance(c.value, int):
        raise TypeError(f"ProvenanceCell {c.formula_name!r} is not an int: {c.value!r}")
    return c.value


# ---------------------------------------------------------------------------
# Per-year cell-producing functions (cycle-2 provenance — plan § 0.9)
# ---------------------------------------------------------------------------
#
# Each function below produces one leaf value of the per-node trajectory as
# a `ProvenanceCell`: value + unit + formula + uses + sources + description.


def compute_mass_per_pkg(
    gen_pkg_mass_t: float,
    kw_per_pkg: float,
    solar_t_per_kw: float,
    radiator_t_per_kw_active: float,
    *,
    gen_mass_path: FieldPath,
    kw_per_pkg_path: FieldPath,
    solar_dial_path: FieldPath,
    radiator_dial_path: FieldPath,
) -> ProvenanceCell:
    """Per-package effective mass including apportioned solar + radiator.

    Args:
        gen_pkg_mass_t: The generation's per-package mass, tonnes.
        kw_per_pkg: The generation's per-package electrical power, kW.
        solar_t_per_kw: Solar-array mass per kW, t/kW.
        radiator_t_per_kw_active: Radiator mass per kW prevailing this year
            (post-Tjmax-lift value from year 5 — D11), t/kW.
        gen_mass_path: JSON path of the upstream generation mass figure.
        kw_per_pkg_path: JSON path of the upstream per-package kW figure.
        solar_dial_path: JSON path of the solar-mass dial.
        radiator_dial_path: JSON path of the radiator-mass dial.

    Returns:
        A :class:`ProvenanceCell` carrying the per-package mass in tonnes.
    """
    value_t = gen_pkg_mass_t + kw_per_pkg * (solar_t_per_kw + radiator_t_per_kw_active)
    return cell(
        value=value_t,
        unit="t",
        formula_name="mass_per_pkg_from_gen_and_dials",
        uses=[gen_mass_path, kw_per_pkg_path, solar_dial_path, radiator_dial_path],
        sources=["cycle-1 engine formula"],
        description=(
            "Per-package effective mass (generation mass + apportioned solar + radiator), tonnes."
        ),
    )


def compute_n_packages(
    mass_budget_t: float,
    mass_per_pkg_t: float,
    *,
    mass_budget_path: FieldPath,
    mass_per_pkg_path: FieldPath,
) -> ProvenanceCell:
    """Packages per node — the mass-bound floor (D6).

    Args:
        mass_budget_t: Mass available for packages (envelope - fixed), tonnes.
        mass_per_pkg_t: Per-package effective mass, tonnes.
        mass_budget_path: JSON path of the upstream mass-budget cell.
        mass_per_pkg_path: JSON path of the upstream per-package-mass cell.

    Returns:
        A :class:`ProvenanceCell` carrying the integer package count.
    """
    value = math.floor(mass_budget_t / mass_per_pkg_t) if mass_per_pkg_t > 0 else 0
    return cell(
        value=value,
        unit="count",
        formula_name="n_packages_from_mass_envelope",
        uses=[mass_budget_path, mass_per_pkg_path],
        sources=["cycle-1 engine formula", "research/SOURCE_INDEX.md#NTR-007"],
        description="Packages per node, mass-bound floor of the mass budget.",
    )


def compute_kw_per_node(
    n_packages: int,
    kw_per_pkg: float,
    *,
    n_packages_path: FieldPath,
    kw_per_pkg_path: FieldPath,
) -> ProvenanceCell:
    """Total node electrical power — N x kW/pkg (derived, not capped — D3).

    Args:
        n_packages: Packages per node.
        kw_per_pkg: The generation's per-package electrical power, kW.
        n_packages_path: JSON path of the upstream package-count cell.
        kw_per_pkg_path: JSON path of the upstream per-package kW figure.

    Returns:
        A :class:`ProvenanceCell` carrying the node power in kW.
    """
    return cell(
        value=n_packages * kw_per_pkg,
        unit="kW",
        formula_name="kw_per_node_from_n_and_kw_per_pkg",
        uses=[n_packages_path, kw_per_pkg_path],
        sources=["cycle-1 engine formula", "research/SOURCE_INDEX.md#THR-011"],
        description="Total node electrical power, N packages x kW per package.",
    )


def compute_mass_per_node(
    n_packages: int,
    mass_per_pkg_t: float,
    node_mass_fixed_t: float,
    *,
    n_packages_path: FieldPath,
    mass_per_pkg_path: FieldPath,
    node_mass_fixed_path: FieldPath,
) -> ProvenanceCell:
    """Total node mass — N x mass_per_pkg + the fixed bus mass.

    Args:
        n_packages: Packages per node.
        mass_per_pkg_t: Per-package effective mass, tonnes.
        node_mass_fixed_t: Fixed per-node (bus) mass, tonnes.
        n_packages_path: JSON path of the upstream package-count cell.
        mass_per_pkg_path: JSON path of the upstream per-package-mass cell.
        node_mass_fixed_path: JSON path of the node-fixed-mass dial.

    Returns:
        A :class:`ProvenanceCell` carrying the total node mass in tonnes.
    """
    return cell(
        value=node_mass_fixed_t + n_packages * mass_per_pkg_t,
        unit="t",
        formula_name="mass_per_node_from_n_and_mass_per_pkg",
        uses=[n_packages_path, mass_per_pkg_path, node_mass_fixed_path],
        sources=["cycle-1 engine formula"],
        description="Total node mass, N x per-package mass plus the fixed bus mass.",
    )


def compute_mass_util(
    node_mass_t: float,
    mass_envelope_t: float,
    *,
    node_mass_path: FieldPath,
    mass_envelope_path: FieldPath,
) -> ProvenanceCell:
    """Mass utilisation — node mass as a percent of the mass envelope.

    The v8 cell carries a **percent** (0-100); cycle-1 carried a 0-1
    fraction. The conversion lives here so every consumer sees one
    convention.

    Args:
        node_mass_t: Total node mass, tonnes.
        mass_envelope_t: Neutron mass envelope to SSO, tonnes.
        node_mass_path: JSON path of the upstream node-mass cell.
        mass_envelope_path: JSON path of the mass-envelope dial.

    Returns:
        A :class:`ProvenanceCell` carrying the mass utilisation in percent;
        ``0.0`` if the envelope is not positive.
    """
    value = (node_mass_t / mass_envelope_t * 100.0) if mass_envelope_t > 0 else 0.0
    return cell(
        value=value,
        unit="percent",
        formula_name="mass_utilization",
        uses=[node_mass_path, mass_envelope_path],
        sources=["cycle-1 engine formula"],
        description="Percent of the Neutron mass envelope used by one node.",
    )


def compute_pf_per_node(
    n_packages: int,
    pf_per_pkg: float,
    *,
    n_packages_path: FieldPath,
    pf_per_pkg_path: FieldPath,
) -> ProvenanceCell:
    """Total node compute — N x PFLOPS/pkg.

    Args:
        n_packages: Packages per node.
        pf_per_pkg: The generation's dense-FP4 PFLOPS per package.
        n_packages_path: JSON path of the upstream package-count cell.
        pf_per_pkg_path: JSON path of the upstream per-package PFLOPS figure.

    Returns:
        A :class:`ProvenanceCell` carrying the node compute in PFLOPS.
    """
    return cell(
        value=n_packages * pf_per_pkg,
        unit="PFLOPS",
        formula_name="pf_per_node_from_n_and_pf_per_pkg",
        uses=[n_packages_path, pf_per_pkg_path],
        sources=["cycle-1 engine formula"],
        description="Total node compute, N packages x PFLOPS per package.",
    )


def compute_pf_per_kw(
    pf_node: float,
    node_kw: float,
    *,
    pf_node_path: FieldPath,
    node_kw_path: FieldPath,
) -> ProvenanceCell:
    """Compute density — PFLOPS per node kW.

    Args:
        pf_node: Total node compute, PFLOPS.
        node_kw: Total node electrical power, kW.
        pf_node_path: JSON path of the upstream node-PFLOPS cell.
        node_kw_path: JSON path of the upstream node-kW cell.

    Returns:
        A :class:`ProvenanceCell` carrying the compute density in PFLOPS/kW;
        ``0.0`` if node power is not positive.
    """
    value = (pf_node / node_kw) if node_kw > 0 else 0.0
    return cell(
        value=value,
        unit="PFLOPS/kW",
        formula_name="pf_per_kw_from_node_pf_and_kw",
        uses=[pf_node_path, node_kw_path],
        sources=["cycle-1 engine formula"],
        description="Compute density, node PFLOPS per node kW.",
    )


@dataclass(frozen=True)
class CostBreakdown:
    """The five per-node build/launch cost lines, each a :class:`ProvenanceCell`.

    Attributes:
        compute: Compute (all packages) build cost.
        bus: Bus build cost.
        solar: Solar-array build cost.
        radiator: Radiator build cost.
        launch: Launch cost (cadence-indexed).
    """

    compute: ProvenanceCell
    bus: ProvenanceCell
    solar: ProvenanceCell
    radiator: ProvenanceCell
    launch: ProvenanceCell


def compute_cost_per_node_breakdown(
    n_packages: int,
    usd_per_pkg: int,
    bus_musd: float,
    solar_musd: float,
    radiator_musd: float,
    launch_musd: float,
    *,
    n_packages_path: FieldPath,
    usd_per_pkg_path: FieldPath,
    kw_per_node_path: FieldPath,
    solar_cost_dial_path: FieldPath,
    radiator_cost_dial_path: FieldPath,
    launch_cost_path: FieldPath,
) -> CostBreakdown:
    """The five per-node cost lines as provenance cells.

    ``bus_musd`` / ``solar_musd`` / ``radiator_musd`` / ``launch_musd`` are
    pre-computed by the engine's per-year cost helpers and passed in; this
    function wraps each line (plus the compute line, derived from N x $/pkg)
    in a :class:`ProvenanceCell`.

    Args:
        n_packages: Packages per node.
        usd_per_pkg: The generation's per-package price, $.
        bus_musd: Bus build cost this year, $M (from ``bus_cost_for_year``).
        solar_musd: Solar-array build cost, $M.
        radiator_musd: Radiator build cost, $M.
        launch_musd: Launch cost this year, $M (cadence-indexed).
        n_packages_path: JSON path of the upstream package-count cell.
        usd_per_pkg_path: JSON path of the upstream per-package price.
        kw_per_node_path: JSON path of the upstream node-kW cell (solar +
            radiator costs scale off it).
        solar_cost_dial_path: JSON path of the solar-cost dial.
        radiator_cost_dial_path: JSON path of the radiator-cost dial.
        launch_cost_path: JSON path of the upstream cadence launch-cost cell.

    Returns:
        A :class:`CostBreakdown` of five provenance cells, all in $M.
    """
    compute_musd = n_packages * usd_per_pkg / USD_PER_MUSD
    return CostBreakdown(
        compute=cell(
            value=compute_musd,
            unit="MUSD",
            formula_name="compute_cost_from_n_and_usd_per_pkg",
            uses=[n_packages_path, usd_per_pkg_path],
            sources=["cycle-1 engine formula"],
            description="Per-node compute build cost (all packages).",
        ),
        bus=cell(
            value=bus_musd,
            unit="MUSD",
            formula_name="bus_cost_from_growth_and_flatten",
            uses=[
                "inputs.config.physical.bus_base_musd",
                "inputs.config.physical.bus_growth_pre",
            ],
            sources=["cycle-1 cost dial", "research/SOURCE_INDEX.md#THR-011"],
            description="Per-node bus build cost (declines then flattens).",
        ),
        solar=cell(
            value=solar_musd,
            unit="MUSD",
            formula_name="solar_cost_from_kw_and_dial",
            uses=[kw_per_node_path, solar_cost_dial_path],
            sources=["cycle-1 cost dial", "research/SOURCE_INDEX.md#THR-006"],
            description="Per-node solar-array build cost.",
        ),
        radiator=cell(
            value=radiator_musd,
            unit="MUSD",
            formula_name="radiator_cost_from_kw_and_dial",
            uses=[kw_per_node_path, radiator_cost_dial_path],
            sources=["cycle-1 cost dial", "research/SOURCE_INDEX.md#THR-003"],
            description="Per-node radiator build cost.",
        ),
        launch=cell(
            value=launch_musd,
            unit="MUSD",
            formula_name="launch_cost_musd_from_cadence_log_linear",
            uses=[launch_cost_path],
            sources=["research/SOURCE_INDEX.md#NTR-009"],
            description="Per-node launch cost (cadence-indexed log-linear curve).",
        ),
    )


def compute_node_total_cost(
    breakdown: CostBreakdown,
    *,
    cost_breakdown_path: FieldPath,
) -> ProvenanceCell:
    """Total per-node build + launch cost — the sum of the five lines.

    Args:
        breakdown: The five-line :class:`CostBreakdown`.
        cost_breakdown_path: JSON path of this year's ``cost_breakdown``
            sub-object — the five component cells it sums are addressed
            under it (``{cost_breakdown_path}.compute`` etc.).

    Returns:
        A :class:`ProvenanceCell` carrying the total per-node cost in $M.
    """
    total = (
        _cell_float(breakdown.compute)
        + _cell_float(breakdown.bus)
        + _cell_float(breakdown.solar)
        + _cell_float(breakdown.radiator)
        + _cell_float(breakdown.launch)
    )
    return cell(
        value=total,
        unit="MUSD",
        formula_name="node_total_cost_from_breakdown",
        uses=[
            f"{cost_breakdown_path}.compute",
            f"{cost_breakdown_path}.bus",
            f"{cost_breakdown_path}.solar",
            f"{cost_breakdown_path}.radiator",
            f"{cost_breakdown_path}.launch",
        ],
        sources=["cycle-1 engine formula"],
        description="Total per-node build + launch cost (sum of the five lines).",
    )


def compute_cost_annual_per_node(
    node_total_musd: float,
    service_life_years: int,
    *,
    node_total_path: FieldPath,
    service_life_path: FieldPath,
) -> ProvenanceCell:
    """Annualized per-node cost — total node cost spread over the service life.

    Args:
        node_total_musd: Total per-node build + launch cost, $M.
        service_life_years: Node operating life in years (D1 cliff).
        node_total_path: JSON path of the upstream node-total cell.
        service_life_path: JSON path of the service-life dial.

    Returns:
        A :class:`ProvenanceCell` carrying the annualized cost per node,
        $M/yr; ``0.0`` if the service life is not positive.
    """
    value = node_total_musd / service_life_years if service_life_years > 0 else 0.0
    return cell(
        value=value,
        unit="MUSD",
        formula_name="cost_annual_per_node_from_breakdown",
        uses=[node_total_path, service_life_path],
        sources=["cycle-1 engine formula", "research/SOURCE_INDEX.md#THR-008"],
        description="Annualized cost per node over the service life.",
    )


def compute_revenue_annual_per_node(
    cost_annual_musd: float,
    r_value: float,
    band: str,
    *,
    cost_annual_path: FieldPath,
    r_band_path: FieldPath,
) -> ProvenanceCell:
    """Annual per-node revenue at one R-band trajectory.

    Args:
        cost_annual_musd: Annualized per-node cost, $M/yr.
        r_value: The revenue-to-cost multiplier R for this band + year.
        band: The R-band trajectory name (``central`` / ``low`` / ``high``).
        cost_annual_path: JSON path of the upstream annual-cost cell.
        r_band_path: JSON path of the R-band trajectory anchors.

    Returns:
        A :class:`ProvenanceCell` carrying the annual per-node revenue at
        the given band, $M/yr.
    """
    return cell(
        value=cost_annual_musd * r_value,
        unit="MUSD",
        formula_name="revenue_annual_per_node_from_cost_and_r",
        uses=[cost_annual_path, r_band_path],
        sources=["research/SOURCE_INDEX.md#REV-008", "D4 owner-operator R-band scenario"],
        description=f"Annual per-node revenue at {band} R (cost x R).",
    )


def compute_gross_profit_annual_per_node(
    revenue_annual_musd: float,
    cost_annual_musd: float,
    band: str,
    *,
    revenue_path: FieldPath,
    cost_annual_path: FieldPath,
) -> ProvenanceCell:
    """Annual per-node gross profit at one R-band trajectory.

    Args:
        revenue_annual_musd: Annual per-node revenue at this band, $M/yr.
        cost_annual_musd: Annualized per-node cost, $M/yr.
        band: The R-band trajectory name (``central`` / ``low`` / ``high``).
        revenue_path: JSON path of the upstream revenue cell.
        cost_annual_path: JSON path of the upstream annual-cost cell.

    Returns:
        A :class:`ProvenanceCell` carrying the annual per-node gross profit
        at the given band, $M/yr.
    """
    return cell(
        value=revenue_annual_musd - cost_annual_musd,
        unit="MUSD",
        formula_name="gross_profit_annual_per_node_from_rev_and_cost",
        uses=[revenue_path, cost_annual_path],
        sources=["research/SOURCE_INDEX.md#REV-008", "cycle-2 R-band formula"],
        description=f"Annual per-node gross profit at {band} R (revenue - cost).",
    )


# ---------------------------------------------------------------------------
# Cycle-2 cadence wiring
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CadenceYear:
    """One model year's cadence outputs — launches and per-launch cost.

    Attributes:
        launches: Launches in this model year (logistic ramp), a cell.
        launch_cost_musd: Per-launch cost at this year's cadence, a cell.
    """

    launches: ProvenanceCell
    launch_cost_musd: ProvenanceCell


def compute_cadence_year(year_idx: int, config: ValuationConfig) -> CadenceYear:
    """Compute one model year's launches and cadence-indexed launch cost.

    Reads the launch-cadence dials from ``config.cadence`` and the
    launch-cost dials from ``config.launch_cost``; the launch cost is
    priced at the launches-per-year the cadence ramp produces.

    Args:
        year_idx: Zero-based model year index.
        config: The valuation config (provides ``cadence`` + ``launch_cost``).

    Returns:
        A :class:`CadenceYear` of two provenance cells.
    """
    cad = config.cadence
    lc = config.launch_cost
    launches_cell = compute_launches_per_year(
        year_idx,
        cadence_ceiling=cad.cadence_ceiling,
        launches_at_year_5=cad.launches_at_year_5,
        launches_at_year_10=cad.launches_at_year_10,
        first_launch_year=cad.first_launch_year,
    )
    launches = _cell_float(launches_cell)
    launch_cost_cell = compute_launch_cost_musd(
        launches,
        low_cadence_cost_musd=lc.low_cadence_cost_musd,
        high_cadence_cost_musd=lc.high_cadence_cost_musd,
        low_cadence_launches=lc.low_cadence_launches,
        high_cadence_launches=lc.high_cadence_launches,
    )
    return CadenceYear(launches=launches_cell, launch_cost_musd=launch_cost_cell)


# ---------------------------------------------------------------------------
# Cycle-2 volume wiring
# ---------------------------------------------------------------------------


def compute_volume_year(
    n_packages: int,
    mass_util_pct: float,
    kw_per_pkg: float,
    config: ValuationConfig,
    *,
    fy_path: FieldPath,
) -> VolumeBreakdown:
    """Compute one year's stowed-volume breakdown and binding constraint.

    Chains the volume-model cell producers: solar area per package, stowed
    volume per package, total node volume, fairing utilization, and the
    mass-vs-volume binding constraint. Reads dials from ``config.volume``.

    Args:
        n_packages: Packages per node this year (the mass-bound N).
        mass_util_pct: Mass utilization as a percent (0-100) — used for the
            binding-constraint comparison.
        kw_per_pkg: The frontier generation's per-package kW this year.
        config: The valuation config (provides the ``volume`` dial block).
        fy_path: JSON path of this fiscal year's physical block, e.g.
            ``physical.years."2036"`` — used to build the cell-to-cell
            ``uses`` back-pointers so they resolve to real cells.

    Returns:
        A :class:`VolumeBreakdown` of provenance cells.
    """
    vol = config.volume
    solar_area_cell = compute_solar_area_per_pkg(
        kw_per_pkg,
        vol.si_bol_efficiency,
        kw_per_pkg_path="inputs.config.generations[].kw_per_pkg",
        efficiency_path="inputs.config.volume.si_bol_efficiency",
    )
    volume_per_pkg_cell = compute_volume_per_pkg(
        _cell_float(solar_area_cell),
        vol.fold_ratio,
        vol.stowed_pitch_mm,
        solar_area_path=f"{fy_path}.solar_area_per_pkg_m2",
        fold_ratio_path="inputs.config.volume.fold_ratio",
        pitch_path="inputs.config.volume.stowed_pitch_mm",
    )
    volume_per_node_cell = compute_volume_per_node(
        n_packages,
        _cell_float(volume_per_pkg_cell),
        vol.mounting_overhead_pct,
        n_path=f"{fy_path}.gpus_per_node",
        vol_per_pkg_path=f"{fy_path}.volume_per_pkg_m3",
        mounting_path="inputs.config.volume.mounting_overhead_pct",
    )
    volume_util_cell = compute_volume_utilization(
        _cell_float(volume_per_node_cell),
        vol.neutron_fairing_usable_volume_m3,
        node_volume_path=f"{fy_path}.volume_per_node_m3",
        fairing_volume_path="inputs.config.volume.neutron_fairing_usable_volume_m3",
    )
    binding_cell = compute_binding_constraint(
        mass_util_pct,
        _cell_float(volume_util_cell),
        mass_util_path=f"{fy_path}.mass_utilization_pct",
        volume_util_path=f"{fy_path}.volume_utilization_pct",
    )
    return VolumeBreakdown(
        solar_area_per_pkg_m2=solar_area_cell,
        volume_per_pkg_m3=volume_per_pkg_cell,
        volume_per_node_m3=volume_per_node_cell,
        volume_utilization_pct=volume_util_cell,
        binding_constraint=binding_cell,
    )


# ---------------------------------------------------------------------------
# Per-year computation — the GPU-first formulas in one place
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class YearComputation:
    """One fiscal year's GPU-first per-node computation (engine-internal).

    The engine's per-year intermediate: the frontier generation chosen for
    the year plus the per-node :class:`PhysicalYear` of provenance cells.
    This is not an output model — it is consumed by the fleet rollup and
    by the v8 output assembly.

    Attributes:
        year_idx: Zero-based model year index.
        fy: Calendar fiscal year (``base_year + year_idx``).
        frontier: The frontier :class:`GenerationSpec` for the year.
        physical: The per-node :class:`PhysicalYear` of provenance cells.
        n_packages: Packages per node (the mass-bound N), unwrapped.
        node_kw: Total node electrical power, kW, unwrapped.
        node_total_musd: Total per-node build + launch cost, $M, unwrapped.
        cost_annual_musd: Annualized per-node cost, $M/yr, unwrapped.
    """

    year_idx: int
    fy: int
    frontier: GenerationSpec
    physical: PhysicalYear
    n_packages: int
    node_kw: float
    node_total_musd: float
    cost_annual_musd: float


def compute_year(
    year_idx: int,
    config: ValuationConfig,
    extended_gens: list[GenerationSpec],
) -> YearComputation:
    """Compute one fiscal year's GPU-first per-node economics.

    Implements the GPU-first formulas (see module docstring) against the
    frontier generation for the year, then assembles the per-node v8
    :class:`PhysicalYear` of provenance cells.

    Args:
        year_idx: Zero-based model year (0 = ``metadata.base_year``).
        config: The valuation config.
        extended_gens: The full generation list extended to cover the
            horizon's fiscal year (built once in :func:`run_valuation`).

    Returns:
        A :class:`YearComputation` for the year.
    """
    gospel = config.gospel
    fy_calendar = config.metadata.base_year + year_idx
    front: GenerationSpec = frontier_at(float(fy_calendar), extended_gens)
    fy_path = f'physical.years."{fy_calendar}"'

    # The radiator and mass terms (D11 Tjmax step).
    radiator_t_per_kw = radiator_t_per_kw_for_year(year_idx, gospel)
    mass_per_pkg_cell = compute_mass_per_pkg(
        front.kg_per_pkg / KG_PER_T,
        front.kw_per_pkg,
        gospel.solar_mass_t_per_kw,
        radiator_t_per_kw,
        gen_mass_path="inputs.config.generations[].kg_per_pkg",
        kw_per_pkg_path="inputs.config.generations[].kw_per_pkg",
        solar_dial_path="inputs.config.physical.solar_mass_t_per_kw",
        radiator_dial_path="inputs.config.physical.radiator_t_per_kw_post",
    )
    mass_per_pkg_t = _cell_float(mass_per_pkg_cell)
    mass_budget_t = gospel.mass_envelope_t - gospel.node_mass_fixed_t
    n_cell = compute_n_packages(
        mass_budget_t,
        mass_per_pkg_t,
        mass_budget_path="inputs.config.physical.mass_envelope_t",
        mass_per_pkg_path="inputs.config.generations[].kg_per_pkg",
    )
    n = _cell_int(n_cell)

    # The physical state — N, derived node power, derived mass, PFLOPS.
    kw_cell = compute_kw_per_node(
        n,
        front.kw_per_pkg,
        n_packages_path=f"{fy_path}.gpus_per_node",
        kw_per_pkg_path="inputs.config.generations[].kw_per_pkg",
    )
    node_kw = _cell_float(kw_cell)
    node_mass_cell = compute_mass_per_node(
        n,
        mass_per_pkg_t,
        gospel.node_mass_fixed_t,
        n_packages_path=f"{fy_path}.gpus_per_node",
        mass_per_pkg_path="inputs.config.generations[].kg_per_pkg",
        node_mass_fixed_path="inputs.config.physical.node_mass_fixed_t",
    )
    node_mass_t = _cell_float(node_mass_cell)
    mass_util_cell = compute_mass_util(
        node_mass_t,
        gospel.mass_envelope_t,
        node_mass_path=f"{fy_path}.mass_per_node_t",
        mass_envelope_path="inputs.config.physical.mass_envelope_t",
    )
    mass_util_pct = _cell_float(mass_util_cell)
    pf_node_cell = compute_pf_per_node(
        n,
        front.pf_per_pkg,
        n_packages_path=f"{fy_path}.gpus_per_node",
        pf_per_pkg_path="inputs.config.generations[].pf_per_pkg",
    )
    node_pf = _cell_float(pf_node_cell)
    pf_per_kw_cell = compute_pf_per_kw(
        node_pf,
        node_kw,
        pf_node_path=f"{fy_path}.pf_per_node",
        node_kw_path=f"{fy_path}.kw_per_node",
    )

    # The volume model (transparency — does not gate N, D6).
    volume = compute_volume_year(n, mass_util_pct, front.kw_per_pkg, config, fy_path=fy_path)

    # The cost decomposition — five build lines + total + annualized.
    cadence_year = compute_cadence_year(year_idx, config)
    launch_musd = _cell_float(cadence_year.launch_cost_musd)
    breakdown = compute_cost_per_node_breakdown(
        n,
        front.usd_per_pkg,
        bus_cost_for_year(year_idx, gospel),
        gospel.solar_cost_musd_per_kw * node_kw,
        gospel.radiator_cost_musd_per_kw * node_kw,
        launch_musd,
        n_packages_path=f"{fy_path}.gpus_per_node",
        usd_per_pkg_path="inputs.config.generations[].usd_per_pkg",
        kw_per_node_path=f"{fy_path}.kw_per_node",
        solar_cost_dial_path="inputs.config.physical.solar_cost_musd_per_kw",
        radiator_cost_dial_path="inputs.config.physical.radiator_cost_musd_per_kw",
        launch_cost_path=f'business.years."{fy_calendar}".launch_cost_this_year_musd',
    )
    node_total_cell = compute_node_total_cost(
        breakdown, cost_breakdown_path=f"{fy_path}.cost_breakdown"
    )
    node_total_musd = _cell_float(node_total_cell)
    service_life = config.fleet.service_life_years
    cost_annual_cell = compute_cost_annual_per_node(
        node_total_musd,
        service_life,
        node_total_path=f"{fy_path}.cost_breakdown.node_total",
        service_life_path="inputs.config.fleet.service_life_years",
    )
    cost_annual_musd = _cell_float(cost_annual_cell)

    # The revenue economics — an R band (low / central / high) of per-node
    # annual revenue and gross profit.
    r_central, r_low, r_high = r_at_year(config.r_band, fy_calendar)
    cost_annual_path = f"{fy_path}.cost_annual_per_node_musd"
    rev_central = compute_revenue_annual_per_node(
        cost_annual_musd,
        r_central,
        "central",
        cost_annual_path=cost_annual_path,
        r_band_path="inputs.config.revenue.central[]",
    )
    rev_low = compute_revenue_annual_per_node(
        cost_annual_musd,
        r_low,
        "low",
        cost_annual_path=cost_annual_path,
        r_band_path="inputs.config.revenue.low[]",
    )
    rev_high = compute_revenue_annual_per_node(
        cost_annual_musd,
        r_high,
        "high",
        cost_annual_path=cost_annual_path,
        r_band_path="inputs.config.revenue.high[]",
    )
    gp_central = compute_gross_profit_annual_per_node(
        _cell_float(rev_central),
        cost_annual_musd,
        "central",
        revenue_path=f"{fy_path}.revenue_annual_per_node_musd_central",
        cost_annual_path=cost_annual_path,
    )
    gp_low = compute_gross_profit_annual_per_node(
        _cell_float(rev_low),
        cost_annual_musd,
        "low",
        revenue_path=f"{fy_path}.revenue_annual_per_node_musd_low",
        cost_annual_path=cost_annual_path,
    )
    gp_high = compute_gross_profit_annual_per_node(
        _cell_float(rev_high),
        cost_annual_musd,
        "high",
        revenue_path=f"{fy_path}.revenue_annual_per_node_musd_high",
        cost_annual_path=cost_annual_path,
    )

    frontier_cell = cell(
        value=front.name,
        unit="-",
        formula_name="frontier_generation_from_cadence",
        uses=["inputs.config.generations[].year_available"],
        sources=["research/SOURCE_INDEX.md#GPU-001", "research/SOURCE_INDEX.md#GPU-012"],
        description=(
            f"Frontier generation for FY{fy_calendar} "
            f"(latest with year_available <= {fy_calendar})."
        ),
    )

    cost_breakdown = CostBreakdownBlock(
        compute=breakdown.compute,
        bus=breakdown.bus,
        solar=breakdown.solar,
        radiator=breakdown.radiator,
        launch=breakdown.launch,
        node_total=node_total_cell,
    )

    physical = PhysicalYear(
        year=fy_calendar,
        frontier_generation=frontier_cell,
        gpus_per_node=n_cell,
        kw_per_node=kw_cell,
        mass_per_node_t=node_mass_cell,
        solar_area_per_pkg_m2=volume.solar_area_per_pkg_m2,
        volume_per_pkg_m3=volume.volume_per_pkg_m3,
        volume_per_node_m3=volume.volume_per_node_m3,
        mass_utilization_pct=mass_util_cell,
        volume_utilization_pct=volume.volume_utilization_pct,
        binding_constraint=volume.binding_constraint,
        pf_per_node=pf_node_cell,
        pf_per_kw=pf_per_kw_cell,
        cost_breakdown=cost_breakdown,
        cost_annual_per_node_musd=cost_annual_cell,
        revenue_annual_per_node_musd_central=rev_central,
        revenue_annual_per_node_musd_low=rev_low,
        revenue_annual_per_node_musd_high=rev_high,
        gross_profit_annual_per_node_musd_central=gp_central,
        gross_profit_annual_per_node_musd_low=gp_low,
        gross_profit_annual_per_node_musd_high=gp_high,
    )

    return YearComputation(
        year_idx=year_idx,
        fy=fy_calendar,
        frontier=front,
        physical=physical,
        n_packages=n,
        node_kw=node_kw,
        node_total_musd=node_total_musd,
        cost_annual_musd=cost_annual_musd,
    )


# ---------------------------------------------------------------------------
# Cycle-2 fleet wiring
# ---------------------------------------------------------------------------


def _year_to_cohort(
    year: YearComputation,
    nodes_deployed: int,
    r_band: RBand,
) -> Cohort:
    """Build a deployment-year :class:`Cohort` from one per-node year.

    Per-node annual cost is the year's annualized cost (already computed in
    :func:`compute_year`); per-node annual revenue is that annual cost
    times the R-band value at the cohort's launch year, captured as a
    low/central/high triple.

    Args:
        year: The deployment year's :class:`YearComputation`.
        nodes_deployed: Node count for this cohort (1 node per launch, D8).
        r_band: The three-trajectory R band.

    Returns:
        A frozen :class:`Cohort` for the year.
    """
    cost_annual_per_node = year.cost_annual_musd
    r_central, r_low, r_high = r_at_year(r_band, year.fy)
    return Cohort(
        launch_year=year.fy,
        nodes_deployed=nodes_deployed,
        frontier_generation=year.frontier.name,
        kw_per_node=year.node_kw,
        pf_per_node=_cell_float(year.physical.pf_per_node),
        cost_annual_per_node_musd=cost_annual_per_node,
        rev_per_node_musd_central=cost_annual_per_node * r_central,
        rev_per_node_musd_low=cost_annual_per_node * r_low,
        rev_per_node_musd_high=cost_annual_per_node * r_high,
    )


def compute_fleet_trajectory(
    config: ValuationConfig,
    years: list[YearComputation],
) -> list[FleetYear]:
    """Build the per-year fleet rollup parallel to the per-node trajectory.

    For each model year: prices the cadence (launches + launch cost), turns
    the year's per-node economics into a deployment-year :class:`Cohort`
    (node count = launches, D8 1 node per launch), and rolls the living
    cohort set up via :func:`data_center.fleet.compute_fleet_year`,
    threading the running cumulative revenue across all three R bands.

    The cadence ramp emits integer launch counts. A cohort's
    ``nodes_deployed`` is therefore a true count, not a fractional rate.

    Args:
        config: The valuation config.
        years: The per-node :class:`YearComputation` trajectory.

    Returns:
        A list of :class:`FleetYear`, one per element of ``years``.
    """
    r_band = config.r_band
    cohorts: list[Cohort] = []
    fleet_years: list[FleetYear] = []
    cumul_central = 0.0
    cumul_low = 0.0
    cumul_high = 0.0
    for year in years:
        cadence_year = compute_cadence_year(year.year_idx, config)
        launches = int(_cell_float(cadence_year.launches))
        launch_cost = _cell_float(cadence_year.launch_cost_musd)
        nodes_deployed = launches
        cohorts.append(_year_to_cohort(year, nodes_deployed, r_band))
        fleet_year = compute_fleet_year(
            year.fy,
            cohorts,
            launches,
            launch_cost,
            cumul_central,
            cumul_low,
            cumul_high,
            year_path=f'business.years."{year.fy}"',
        )
        fleet_years.append(fleet_year)
        cumul_central = _cell_float(fleet_year.revenue_cumulative_musd_central)
        cumul_low = _cell_float(fleet_year.revenue_cumulative_musd_low)
        cumul_high = _cell_float(fleet_year.revenue_cumulative_musd_high)
    return fleet_years


def _fleet_year_to_business_year(fleet_year: FleetYear) -> BusinessYear:
    """Map a :class:`data_center.fleet.FleetYear` to a v8 :class:`BusinessYear`.

    Both carry the same 19 provenance-cell fields; this is a field-by-field
    transcription so the engine-internal ``FleetYear`` dataclass and the
    output ``BusinessYear`` Pydantic model stay decoupled.

    Args:
        fleet_year: The per-year fleet rollup from the fleet module.

    Returns:
        The equivalent v8 :class:`BusinessYear`.
    """
    return BusinessYear(
        year=fleet_year.year,
        launches=fleet_year.launches,
        nodes_deployed_this_year=fleet_year.nodes_deployed_this_year,
        living_fleet=fleet_year.living_fleet,
        kw_deployed_this_year=fleet_year.kw_deployed_this_year,
        kw_living_fleet=fleet_year.kw_living_fleet,
        kw_on_orbit=fleet_year.kw_on_orbit,
        pf_deployed_this_year=fleet_year.pf_deployed_this_year,
        pf_living_fleet=fleet_year.pf_living_fleet,
        pf_on_orbit=fleet_year.pf_on_orbit,
        launch_cost_this_year_musd=fleet_year.launch_cost_this_year_musd,
        cost_annual_fleet_musd=fleet_year.cost_annual_fleet_musd,
        revenue_annual_fleet_musd_central=fleet_year.revenue_annual_fleet_musd_central,
        revenue_annual_fleet_musd_low=fleet_year.revenue_annual_fleet_musd_low,
        revenue_annual_fleet_musd_high=fleet_year.revenue_annual_fleet_musd_high,
        revenue_cumulative_musd_central=fleet_year.revenue_cumulative_musd_central,
        revenue_cumulative_musd_low=fleet_year.revenue_cumulative_musd_low,
        revenue_cumulative_musd_high=fleet_year.revenue_cumulative_musd_high,
        gross_profit_annual_fleet_musd_central=fleet_year.gross_profit_annual_fleet_musd_central,
        gross_profit_annual_fleet_musd_low=fleet_year.gross_profit_annual_fleet_musd_low,
        gross_profit_annual_fleet_musd_high=fleet_year.gross_profit_annual_fleet_musd_high,
        margin_central_pct=fleet_year.margin_central_pct,
        margin_low_pct=fleet_year.margin_low_pct,
        margin_high_pct=fleet_year.margin_high_pct,
    )


# ---------------------------------------------------------------------------
# The top-level entry point
# ---------------------------------------------------------------------------


def run_valuation(
    config: ValuationConfig,
    *,
    source_scenario_path: str = "unrecorded",
    artifact_role: str = "draft",
) -> ValuationOutput:
    """Run the GPU-first valuation model end-to-end and return the v8 artifact.

    Resolves the frontier-generation list (using ``config.generations`` if
    provided, else extending ``KNOWN_GENS`` with ``config.slopes``),
    computes one :class:`YearComputation` per fiscal year from year 0 to
    ``metadata.horizon_years``, rolls the living fleet up by cohort, and
    delegates the v8 ``ValuationOutput`` assembly to
    :func:`data_center.json_output.build_output`.

    Args:
        config: The validated :class:`ValuationConfig`.
        source_scenario_path: Repository-relative source scenario path.
        artifact_role: Artifact role to stamp in output metadata.

    Returns:
        A frozen v8 :class:`ValuationOutput`.
    """
    # Local import — json_output imports engine types, so the import is
    # deferred to call time to keep the module-load order acyclic.
    from .json_output import build_output

    horizon_years = config.metadata.horizon_years

    # Generation list — scenario override or KNOWN_GENS extended to cover
    # the horizon's fiscal year.
    if config.generations is not None:
        base_gens: list[GenerationSpec] = list(config.generations)
    else:
        base_gens = list(KNOWN_GENS)
    target_yr = float(config.metadata.base_year + horizon_years + 1)
    extended_gens = extend_generations(
        base_gens, config.slopes, config.gospel.release_cadence_yr, target_yr
    )

    years = [compute_year(i, config, extended_gens) for i in range(horizon_years + 1)]
    fleet_years = compute_fleet_trajectory(config, years)

    physical_by_year = {str(y.fy): y.physical for y in years}
    business_by_year = {
        str(y.fy): _fleet_year_to_business_year(fy)
        for y, fy in zip(years, fleet_years, strict=True)
    }

    return build_output(
        config=config,
        extended_gens=extended_gens,
        physical_by_year=physical_by_year,
        business_by_year=business_by_year,
        generated_at=datetime.now(UTC).isoformat(),
        source_scenario_path=source_scenario_path,
        artifact_role=artifact_role,
    )


__all__ = [
    "CadenceYear",
    "CostBreakdown",
    "YearComputation",
    "bus_cost_for_year",
    "compute_cadence_year",
    "compute_cost_annual_per_node",
    "compute_cost_per_node_breakdown",
    "compute_fleet_trajectory",
    "compute_gross_profit_annual_per_node",
    "compute_kw_per_node",
    "compute_mass_per_node",
    "compute_mass_per_pkg",
    "compute_mass_util",
    "compute_n_packages",
    "compute_node_total_cost",
    "compute_pf_per_kw",
    "compute_pf_per_node",
    "compute_revenue_annual_per_node",
    "compute_volume_year",
    "compute_year",
    "radiator_t_per_kw_for_year",
    "run_valuation",
]
