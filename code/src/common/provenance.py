"""Provenance infrastructure: ProvenanceCell + FORMULAS lookup + cell() factory.

Every leaf numeric value in the cycle-2 output JSON is wrapped in a
:class:`ProvenanceCell`, carrying value + unit + formula + formula_name +
uses + sources + description. The :data:`FORMULAS` table is the authoritative
lookup for ``formula_name`` keys; V13 enforces that every used name exists
here.

The :func:`cell` factory hides ProvenanceCell-construction noise: a caller
passes a ``formula_name`` and the factory resolves the human-readable
``formula`` text from :data:`FORMULAS`. Engine / cadence / fleet / volume
code reads like bare-value math at the call site while still emitting a
fully provenance-annotated cell.

The output contract relies on two durable rules: every emitted formula name
must resolve through the catalog below, and every public numeric cell should
carry enough provenance for a reader to trace formula, inputs, sources, and
description without private lifecycle notes.
"""

from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from common.input_manifest import SourceStatus

# ---------------------------------------------------------------------------
# Semantic type aliases (CLAUDE.md "semantic-typed dict keys" / strategy 3.5)
# ---------------------------------------------------------------------------
#
# PEP 695 ``type`` statements (ruff UP040, project target py314). The
# strategy's section-0.10 snippet predates the py314 ruff config; the
# ``type`` keyword is the codebase-consistent form.

type FieldPath = str
"""A JSON path string, e.g. ``physical.years."2036".kw_per_node``."""

type GenerationName = str
"""A GPU generation name, e.g. ``B200``, ``Rubin Ultra``, ``Gen+4(extrap)``."""

type YearString = str
"""A JSON-string year, e.g. ``"2036"``."""

type LaunchesPerYear = int
"""Whole-number launches in one fiscal year."""


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class FormulaSpec(BaseModel):
    """One entry in the :data:`FORMULAS` lookup table.

    Attributes:
        formula: Human-readable formula (e.g. ``revenue = R x cost``).
        description: One-sentence plain-language meaning of the formula.
    """

    model_config = ConfigDict(frozen=True)
    formula: str
    description: str


class ProvenanceCell(BaseModel):
    """A typed wrapper for every leaf numeric value in the output JSON.

    Carries the value alongside its provenance: the unit, the formula that
    produced it (both human-readable text and the stable ``formula_name``
    key), the upstream cells/dials it consumed (``uses``), and the research
    citations or local provenance labels backing it (``sources``). Hard
    numbers should prefer `research/SOURCE_INDEX.md` claim IDs or durable
    research document paths.

    Attributes:
        value: The leaf value. ``float`` / ``int`` for numerics, ``str`` for
            enum-valued cells, ``bool`` for flags, ``None`` for not-yet-computed.
        unit: The unit string (e.g. ``kW``, ``MUSD``, ``PFLOPS/kW``).
        formula: Human-readable formula text (resolved from :data:`FORMULAS`).
        formula_name: The stable formula key; must exist in :data:`FORMULAS`.
        uses: JSON paths of the upstream cells / dials this value derives from.
        sources: Provenance citations or local derivation labels.
        source_status: Source classification for the computed output cell.
        description: One-sentence plain-language meaning of this cell.
        notes: Optional caveat for the computed output cell.
    """

    model_config = ConfigDict(frozen=True)
    value: float | int | str | bool | None
    unit: str
    formula: str
    formula_name: str
    uses: list[FieldPath]
    sources: list[str]
    source_status: SourceStatus = Field(default=SourceStatus.DERIVED_ESTIMATE)
    description: str
    notes: str | None = None


# ---------------------------------------------------------------------------
# FORMULAS: the authoritative formula_name lookup (plan section 0.8)
# ---------------------------------------------------------------------------
#
# Every formula_name a ProvenanceCell references must have an entry here.
# V13 (Phase 5) enforces this: any cell whose formula_name is missing from
# this table fails the validation rule. Sub-agents adding a new formula must
# add it here too.


FORMULAS: Final[dict[str, FormulaSpec]] = {
    "mass_per_pkg_from_gen_and_dials": FormulaSpec(
        formula=(
            "pkg_mass_kg + (solar_t_per_kw + radiator_t_per_kw_active(year)) x kw_per_pkg x 1000"
        ),
        description="Per-package effective mass including apportioned solar + radiator.",
    ),
    "n_packages_from_mass_envelope": FormulaSpec(
        formula="floor((mass_envelope_t - node_mass_fixed_t) x 1000 / mass_per_pkg_kg)",
        description="Packages per node, mass-bound under D6.",
    ),
    "kw_per_node_from_n_and_kw_per_pkg": FormulaSpec(
        formula="N x kw_per_pkg",
        description="Total node electrical power.",
    ),
    "mass_per_node_from_n_and_mass_per_pkg": FormulaSpec(
        formula="N x mass_per_pkg + node_mass_fixed_t",
        description="Total node mass including bus.",
    ),
    "mass_utilization": FormulaSpec(
        formula="mass_per_node_t / mass_envelope_t",
        description="Fraction of mass envelope used.",
    ),
    "solar_area_per_pkg_from_kw_and_eff": FormulaSpec(
        formula="kw_per_pkg x 1000 / (SOLAR_CONSTANT_W_M2 x si_bol_efficiency)",
        description="Solar collector area per package required to power it.",
    ),
    "volume_per_pkg_stowed": FormulaSpec(
        formula="(solar_area_m2_per_pkg / fold_ratio) x (stowed_pitch_mm / 1000)",
        description="Stowed volume per package (panel + co-mounted radiator).",
    ),
    "volume_per_node_from_n_and_vol_per_pkg": FormulaSpec(
        formula="N x volume_per_pkg + node_volume_fixed_m3 + mounting_overhead x array_volume",
        description="Total node stowed volume.",
    ),
    "volume_utilization": FormulaSpec(
        formula="volume_per_node_m3 / neutron_fairing_usable_volume_m3",
        description="Fraction of Neutron fairing volume used.",
    ),
    "binding_constraint_from_utilizations": FormulaSpec(
        formula="enum(mass_util > 1.0 ? MASS : 0, volume_util > 1.0 ? VOLUME : 0)",
        description="Which envelope (mass / volume / both / neither) is binding.",
    ),
    "pf_per_node_from_n_and_pf_per_pkg": FormulaSpec(
        formula="N x pf_per_pkg",
        description="Total node compute in PFLOPS.",
    ),
    "pf_per_kw_from_node_pf_and_kw": FormulaSpec(
        formula="pf_per_node / kw_per_node",
        description="Compute density in PFLOPS/kW.",
    ),
    "cost_annual_per_node_from_breakdown": FormulaSpec(
        formula="(compute + bus + solar + radiator + launch_cost(year)) / 5",
        description="Annualized cost per node over service life (D1).",
    ),
    "revenue_annual_per_node_from_cost_and_r": FormulaSpec(
        formula="cost_annual_per_node x R(year, band)",
        description="Annual gross revenue per node (owner-operator R-band scenario).",
    ),
    "gross_profit_annual_per_node_from_rev_and_cost": FormulaSpec(
        formula="revenue_annual - cost_annual",
        description="Annual gross profit per node.",
    ),
    "margin_pct_from_rev_and_cost": FormulaSpec(
        formula="(revenue - cost) / revenue x 100",
        description="Gross margin percentage.",
    ),
    "launches_per_year_from_logistic": FormulaSpec(
        formula=(
            "round(cadence_ceiling / (1 + exp(-k(t - t0)))) ; k and t0 from year-5/year-10 anchors"
        ),
        description="Integer launch ramp fit to scenario anchors.",
    ),
    "launch_cost_musd_from_cadence_log_linear": FormulaSpec(
        formula=(
            "log-linear interp between (low_launches, low_cost) and "
            "(high_launches, high_cost), flat-clamped"
        ),
        description="Cadence-indexed launch cost (SOURCE_INDEX NTR-009).",
    ),
    "nodes_deployed_this_year_from_launches": FormulaSpec(
        formula="integer launches x 1   # D8 GPU = package; 1 node per launch",
        description="Nodes deployed this year (1 node per Neutron flight).",
    ),
    "living_fleet_from_cohort_cliff": FormulaSpec(
        formula="sum(cohorts[Y-4..Y].nodes_deployed)",
        description="Living fleet under 5-year hard cliff (D1).",
    ),
    "kw_on_orbit_from_living_fleet": FormulaSpec(
        formula="sum(cohort.nodes x cohort.kw_per_node) for living cohorts",
        description="Total kW on orbit (living fleet).",
    ),
    "pf_on_orbit_from_living_fleet": FormulaSpec(
        formula="sum(cohort.nodes x cohort.pf_per_node) for living cohorts",
        description="Total PFLOPS on orbit (living fleet).",
    ),
    "kw_deployed_this_year_from_nodes": FormulaSpec(
        formula="nodes_deployed_this_year x kw_per_node",
        description="New deployed-year cohort power.",
    ),
    "pf_deployed_this_year_from_nodes": FormulaSpec(
        formula="nodes_deployed_this_year x pf_per_node",
        description="New deployed-year cohort compute.",
    ),
    "revenue_annual_fleet_from_cohorts": FormulaSpec(
        formula="sum(cohort.nodes x cohort.revenue_per_node_at_band) for living",
        description="Fleet annual revenue (cohort-vintaged).",
    ),
    "revenue_cumulative_fleet_from_annuals": FormulaSpec(
        formula="sum(year[Y'].revenue_annual for Y' in [base_year, Y])",
        description="Cumulative fleet revenue base_year through Y.",
    ),
    "cost_annual_fleet_from_cohorts": FormulaSpec(
        formula="sum(cohort.nodes x cohort.cost_per_node) for living",
        description="Fleet annual cost (cohort-vintaged).",
    ),
    "gross_profit_annual_fleet_from_rev_and_cost": FormulaSpec(
        formula="revenue - cost at fleet level",
        description="Fleet annual gross profit.",
    ),
    "r_at_year_from_band_anchors": FormulaSpec(
        formula="linear interpolation between band.anchors",
        description="R value at year Y interpolated from anchors.",
    ),
    # ---- Per-node cost-breakdown lines (cycle-2 Phase 2; the five build
    # lines the engine's CostBreakdown emits as individual cells). These
    # extend plan section 0.8, added when first used (plan section 0.8:
    # "sub-agents adding any new formula must also add it to FORMULAS").
    "compute_cost_from_n_and_usd_per_pkg": FormulaSpec(
        formula="N x usd_per_pkg / 1_000_000",
        description="Per-node compute build cost (all packages), $M.",
    ),
    "bus_cost_from_growth_and_flatten": FormulaSpec(
        formula="bus_base_musd x (1 + bus_growth_pre) ** min(year_idx, bus_flatten_after_yr)",
        description="Per-node bus build cost: declines then flattens (D12), $M.",
    ),
    "solar_cost_from_kw_and_dial": FormulaSpec(
        formula="solar_cost_musd_per_kw x kw_per_node",
        description="Per-node solar-array build cost, $M.",
    ),
    "radiator_cost_from_kw_and_dial": FormulaSpec(
        formula="radiator_cost_musd_per_kw x kw_per_node",
        description="Per-node radiator build cost, $M.",
    ),
    "launch_cost_musd_linear_ramp": FormulaSpec(
        formula="launch_y0_musd + (launch_y10_musd - launch_y0_musd) x (year_idx / 10)",
        description="Per-node launch cost: cycle-1 linear ramp year 0 to year 10, $M.",
    ),
    "node_total_cost_from_breakdown": FormulaSpec(
        formula="compute + bus + solar + radiator + launch",
        description="Total per-node build + launch cost (sum of the five lines), $M.",
    ),
    # ---- v8 output-assembly formula names (cycle-2 Phase 4A). Added when
    # first used by the v8 PhysicalYear cells (plan section 0.8: "sub-agents
    # adding any new formula must also add it to FORMULAS").
    "frontier_generation_from_cadence": FormulaSpec(
        formula="latest generation with year_available <= FY (18-month cadence rule)",
        description="The frontier GPU generation selected for a model year (D7).",
    ),
    # ---- Ground reference model formulas (Phase 3). These support the
    # ground-v1 public artifact and keep the terrestrial comparison traceable
    # through the same ProvenanceCell contract as the space model.
    "ground_anchor_gpu_packages_from_nodes_and_packages": FormulaSpec(
        formula="nodes_deployed_this_year x gpus_per_node",
        description="GPU packages in the deployed-year anchor cohort.",
    ),
    "ground_gpu_acquisition_from_space_package_cost": FormulaSpec(
        formula="anchor_gpu_packages x space_package_cost x ground_cost_multiplier",
        description="Ground GPU/package acquisition cost for the anchor cohort.",
    ),
    "ground_facility_cost_from_mw": FormulaSpec(
        formula="anchor_mw x facility_shell_fitout_musd_per_mw",
        description="Ground facility shell and fit-out allocation.",
    ),
    "ground_racked_power_network_from_package_count": FormulaSpec(
        formula="anchor_gpu_packages x racked_power_network_musd_per_gpu_package",
        description="Ground racked-power and networking allocation.",
    ),
    "ground_energy_cost_from_kw_pue_utilization": FormulaSpec(
        formula=(
            "anchor_kw x PUE x utilization x hours_per_year x years / 1000 "
            "x usd_per_mwh / 1_000_000"
        ),
        description="Ground electricity cost over the comparison period.",
    ),
    "ground_cooling_cost_from_mw": FormulaSpec(
        formula="anchor_mw x cooling_cost_musd_per_mw",
        description="Ground cooling infrastructure allocation.",
    ),
    "ground_operations_cost_from_mw_year": FormulaSpec(
        formula="anchor_mw x operations_maintenance_musd_per_mw_year x years",
        description="Ground operations, maintenance, and labor allocation.",
    ),
    "orbital_component_cost_from_space_node_component": FormulaSpec(
        formula="space_per_node_component_cost x anchor_nodes",
        description="Orbital component cost mirrored from the space model.",
    ),
    "orbital_total_cost_from_space_node_total": FormulaSpec(
        formula="sum(orbital cohort component costs)",
        description="Total orbital build and launch reference cost.",
    ),
    "total_cost_from_components": FormulaSpec(
        formula="sum(component_costs)",
        description="Total cost from included component costs.",
    ),
    "annualized_cost_from_total_and_period": FormulaSpec(
        formula="total_cost / comparison_period_years",
        description="Annualized cost over the comparison period.",
    ),
    "cost_per_unit_from_total": FormulaSpec(
        formula="total_cost / denominator",
        description="Cost per package, MW, or other comparison unit.",
    ),
    "absolute_delta_from_totals": FormulaSpec(
        formula="ground_cost - orbital_cost",
        description="Absolute cost delta between ground and orbital references.",
    ),
    "ratio_from_totals": FormulaSpec(
        formula="numerator / denominator",
        description="Ratio between two cost values.",
    ),
    "explicit_zero_cost_for_excluded_component": FormulaSpec(
        formula="0 by explicit scope treatment",
        description="Explicit zero cost for a component that does not apply in this scope.",
    ),
}


# ---------------------------------------------------------------------------
# cell() factory
# ---------------------------------------------------------------------------


def cell(
    *,
    value: float | int | str | bool | None,
    unit: str,
    formula_name: str,
    uses: list[FieldPath],
    sources: list[str],
    description: str,
) -> ProvenanceCell:
    """Build a :class:`ProvenanceCell`, resolving ``formula`` text from FORMULAS.

    The factory is the single construction point for provenance cells. It
    looks up the human-readable ``formula`` string from :data:`FORMULAS`
    using ``formula_name`` so call sites never duplicate formula text.

    Args:
        value: The leaf value (numeric / enum string / flag / ``None``).
        unit: The unit string (e.g. ``kW``, ``MUSD``).
        formula_name: The stable formula key; must exist in :data:`FORMULAS`.
        uses: JSON paths of upstream cells / dials this value derives from.
        sources: Provenance citations backing the value.
        description: One-sentence plain-language meaning of this cell.

    Returns:
        A frozen :class:`ProvenanceCell` with ``formula`` resolved from the
        FORMULAS table.

    Raises:
        KeyError: If ``formula_name`` is not present in :data:`FORMULAS`.
    """
    if formula_name not in FORMULAS:
        raise KeyError(
            f"formula_name {formula_name!r} not in FORMULAS table; add it to FORMULAS before using."
        )
    spec = FORMULAS[formula_name]
    return ProvenanceCell(
        value=value,
        unit=unit,
        formula=spec.formula,
        formula_name=formula_name,
        uses=uses,
        sources=sources,
        description=description,
    )


__all__ = [
    "FORMULAS",
    "FieldPath",
    "FormulaSpec",
    "GenerationName",
    "LaunchesPerYear",
    "ProvenanceCell",
    "YearString",
    "cell",
]
