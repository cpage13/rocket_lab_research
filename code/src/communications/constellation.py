"""The per-satellite four-area cost-out, the satellites-per-launch fork, the
learning-curve cost-down, the V4 capability step, and the cohort container.

This is the comms analog of the data-center per-node physical-and-cost stack
(``data_center/engine.py``'s ``CostBreakdown`` + the ``compute_cost_*``
functions). It turns the validated Phase-1 ``ConstellationDials`` /
``LaunchDials`` / ``CostDownDials`` (and the per-class ``SatelliteClassDials``)
into source-linked :class:`ProvenanceCell`s, one pure function per computed
leaf. NOTHING here runs the horizon loop or rolls up the living fleet; the
engine (Phase 3) orchestrates these per-class, per-year functions and the
cohort treadmill. This module provides the per-class cohort CONTAINER
(:class:`SatelliteCohort`) and the per-year cost helpers the engine calls.

The two design pieces this module owns (the disaster gates in plan Section 0.9):

* The satellites-per-launch FORK. Satellites-per-launch FORKS by class: a
  broadband (V3-class) satellite is MASS-bound against the Neutron envelope
  (about 5 per launch); a direct-to-cell satellite is ANTENNA-STOW
  (volume)-bound (about 1 per launch) because its large folded antenna fills
  the fairing before the mass limit. BOTH bounds are computed and the smaller
  binds; this is NOT a blanket mass-only path.
* The four-area cost-out. The satellite is costed bottom-up from exactly four
  areas (antenna, comms electronics, solar at about $20k/kW, radiator/bus),
  plus a minor-component carry, summed to a per-satellite build cost that is
  cross-checked against the external V3 estimate of about $1.2M (sweep band
  $0.8M to $1.5M).

The model is Neutron-only and cost-driven: there is no GPU-generation roadmap
engine (the V4 step is a single configurable multiplier, not a multi-generation
frontier), no heavier-than-Neutron vehicle, and no hand-set per-launch count.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from enum import StrEnum

from common.cadence import compute_launch_cost_musd
from common.cohort import LivedCohort
from common.provenance import FieldPath, ProvenanceCell, cell
from communications.config import (
    LaunchDials,
    SatelliteClassDials,
)
from communications.constants import USD_PER_MUSD

logger = logging.getLogger(__name__)


# ===========================================================================
# 1. The binding-constraint enum (the comms fork's extension of the DC enum)
# ===========================================================================


class SatelliteBindingConstraint(StrEnum):
    """Which Neutron envelope binds the satellites-per-launch count for a class.

    Mirrors the data-center ``BindingConstraint`` (the four DC members are
    carried for parity and so a future scenario can report ``BOTH`` /
    ``NEITHER`` / ``VOLUME`` without a schema change) and adds ``ANTENNA_STOW``,
    the direct-to-cell binding where the large folded antenna fills the fairing
    before the mass limit. In practice the comms model emits only ``MASS``
    (broadband) and ``ANTENNA_STOW`` (direct-to-cell).
    """

    MASS = "mass"
    VOLUME = "volume"
    BOTH = "both"
    NEITHER = "neither"
    ANTENNA_STOW = "antenna_stow"


# ===========================================================================
# 2. The data structures (frozen dataclasses of cells)
# ===========================================================================


@dataclass(frozen=True)
class SatelliteCostBreakdown:
    """The four cost areas plus the minor-component carry, each a ProvenanceCell.

    The comms analog of the DC five-line ``CostBreakdown`` (engine.py), with
    comms line items. All cells are in $M.

    Attributes:
        antenna: The phased-array aperture build cost (the dominant line).
        comms_electronics: Modems, beam-forming, processing, the RF chain.
        solar: The power-array build cost, sized from payload power.
        radiator_bus: The spacecraft bus plus thermal.
        minor_component: The minor-component carry (a fraction of the four-area sum).
    """

    antenna: ProvenanceCell
    comms_electronics: ProvenanceCell
    solar: ProvenanceCell
    radiator_bus: ProvenanceCell
    minor_component: ProvenanceCell


@dataclass(frozen=True)
class SatellitePacking:
    """The satellites-per-launch fork result for one satellite class.

    Attributes:
        satellites_per_launch: The binding (smaller) per-launch count, a cell
            whose integer value is the per-launch satellite count.
        binding_constraint: A cell whose value is a
            :class:`SatelliteBindingConstraint` enum string (MASS for broadband,
            ANTENNA_STOW for direct-to-cell).
        mass_bound_count: The mass-bound per-launch count, a cell (transparency).
        volume_bound_count: The stowed-volume-bound per-launch count, a cell
            (transparency).
    """

    satellites_per_launch: ProvenanceCell
    binding_constraint: ProvenanceCell
    mass_bound_count: ProvenanceCell
    volume_bound_count: ProvenanceCell


@dataclass(frozen=True)
class SatelliteCohort:
    """A cohort of satellites launched in one calendar year, with its payload.

    The comms analog of the DC ``Cohort``, composing the generic service-life
    cliff (the launch year and unit count, reused from
    ``common.cohort.LivedCohort``) with the comms per-satellite economics this
    cohort carries forward (its annualized cost and its per-satellite customer
    band, fixed at launch). The engine (Phase 3) builds one per launch year and
    rolls up the living set; this module defines the container and the cliff
    test, not the horizon roll-up.

    Attributes:
        launch_year: Calendar year this cohort was launched.
        satellites_deployed: Number of satellites in this cohort.
        cost_annual_per_satellite_musd: Annualized per-satellite cost, $M/yr
            (fixed at launch).
        customers_per_sat_low: Registered customers per satellite, band-low.
        customers_per_sat_mid: Registered customers per satellite, band-mid.
        customers_per_sat_high: Registered customers per satellite, band-high.
    """

    launch_year: int
    satellites_deployed: int
    cost_annual_per_satellite_musd: float
    customers_per_sat_low: float
    customers_per_sat_mid: float
    customers_per_sat_high: float

    def is_alive_at(self, year: int, service_life: int) -> bool:
        """True iff this cohort is within the service-life cliff at ``year``.

        Delegates to the generic half-open cliff so there is one definition of
        the interval ``[launch_year, launch_year + service_life)``.

        Args:
            year: Calendar year to test.
            service_life: Satellite operating life in years (the hard cliff).
                Required, no default, so the cliff tracks the configured life.

        Returns:
            ``True`` iff ``launch_year <= year < launch_year + service_life``.
        """
        return LivedCohort(
            launch_year=self.launch_year, units_deployed=self.satellites_deployed
        ).is_alive_at(year, service_life)


# ===========================================================================
# 3. The four-area cost-out
# ===========================================================================


def compute_satellite_cost_breakdown(
    dials: SatelliteClassDials,
    *,
    class_name: str,
    dials_path: FieldPath,
) -> SatelliteCostBreakdown:
    """The four cost areas plus the minor-component carry for one class, $M.

    The solar line is sized from payload power: ``solar_cost_usd_per_kw x
    payload_power_kw`` converted USD -> $M by ``USD_PER_MUSD``. The
    minor-component line is ``minor_component_pct`` times the sum of the four
    areas (antenna + comms_electronics + solar + radiator_bus), NOT a fraction
    of the grand total including itself (to avoid a self-referential
    definition). The antenna, comms-electronics, and radiator-bus lines are the
    configured $M dials.

    Args:
        dials: The per-class cost dials.
        class_name: ``"broadband"`` or ``"direct_to_cell"`` (for descriptions).
        dials_path: JSON path of this class's dials block (e.g.
            ``inputs.config.constellation.broadband``).

    Returns:
        A :class:`SatelliteCostBreakdown` of five provenance cells, all $M.
    """
    antenna = cell(
        value=dials.antenna_cost_musd,
        unit="MUSD",
        formula_name="comms_cost_area_line_from_dial",
        uses=[f"{dials_path}.antenna_cost_musd"],
        sources=["research/comms_model_design/DESIGN.md#section-3"],
        description=f"{class_name} phased-array aperture build cost (the dominant line), $M.",
    )
    comms_electronics = cell(
        value=dials.comms_electronics_cost_musd,
        unit="MUSD",
        formula_name="comms_cost_area_line_from_dial",
        uses=[f"{dials_path}.comms_electronics_cost_musd"],
        sources=["research/comms_model_design/DESIGN.md#section-3"],
        description=(
            f"{class_name} comms electronics build cost (modems, beam-forming, RF chain), $M."
        ),
    )
    solar_value = dials.solar_cost_usd_per_kw * dials.payload_power_kw / USD_PER_MUSD
    solar = cell(
        value=solar_value,
        unit="MUSD",
        formula_name="comms_solar_cost_from_power_and_dial",
        uses=[
            f"{dials_path}.solar_cost_usd_per_kw",
            f"{dials_path}.payload_power_kw",
        ],
        sources=["research/comms_model_design/DESIGN.md#section-3"],
        description=(
            f"{class_name} solar-array build cost, sized from comms payload power "
            f"at about $20k/kW (USD converted to $M), $M."
        ),
    )
    radiator_bus = cell(
        value=dials.radiator_bus_cost_musd,
        unit="MUSD",
        formula_name="comms_cost_area_line_from_dial",
        uses=[f"{dials_path}.radiator_bus_cost_musd"],
        sources=["research/comms_model_design/DESIGN.md#section-3"],
        description=f"{class_name} spacecraft bus plus thermal build cost (anchored light), $M.",
    )
    four_area_sum = (
        dials.antenna_cost_musd
        + dials.comms_electronics_cost_musd
        + solar_value
        + dials.radiator_bus_cost_musd
    )
    minor_component = cell(
        value=dials.minor_component_pct * four_area_sum,
        unit="MUSD",
        formula_name="comms_minor_component_cost_from_pct",
        uses=[
            f"{dials_path}.minor_component_pct",
            f"{dials_path}.antenna_cost_musd",
            f"{dials_path}.comms_electronics_cost_musd",
            f"{dials_path}.solar_cost_usd_per_kw",
            f"{dials_path}.payload_power_kw",
            f"{dials_path}.radiator_bus_cost_musd",
        ],
        sources=["research/comms_model_design/DESIGN.md#section-3"],
        description=(
            f"{class_name} minor-component carry, a fraction of the four-area sum "
            f"(not of the grand total including itself), $M."
        ),
    )
    return SatelliteCostBreakdown(
        antenna=antenna,
        comms_electronics=comms_electronics,
        solar=solar,
        radiator_bus=radiator_bus,
        minor_component=minor_component,
    )


def compute_satellite_build_cost(
    breakdown: SatelliteCostBreakdown,
    *,
    breakdown_path: FieldPath,
) -> ProvenanceCell:
    """Per-satellite build cost: the sum of the four areas plus the minor carry, $M.

    The comms analog of the DC ``compute_node_total_cost``, but the build cost
    only (launch is added by ``compute_satellite_total_cost``).

    Args:
        breakdown: The five-line :class:`SatelliteCostBreakdown`.
        breakdown_path: JSON path of this class's cost-breakdown sub-object.

    Returns:
        A :class:`ProvenanceCell` carrying the per-satellite build cost, $M.
    """
    total = (
        _cell_float(breakdown.antenna)
        + _cell_float(breakdown.comms_electronics)
        + _cell_float(breakdown.solar)
        + _cell_float(breakdown.radiator_bus)
        + _cell_float(breakdown.minor_component)
    )
    return cell(
        value=total,
        unit="MUSD",
        formula_name="comms_satellite_build_cost_from_four_areas",
        uses=[
            f"{breakdown_path}.antenna",
            f"{breakdown_path}.comms_electronics",
            f"{breakdown_path}.solar",
            f"{breakdown_path}.radiator_bus",
            f"{breakdown_path}.minor_component",
        ],
        sources=[
            "research/comms_model_design/DESIGN.md#section-3",
            "research/SOURCE_INDEX.md#COMM-082",
        ],
        description=(
            "Per-satellite build cost: the sum of the four areas plus the "
            "minor-component carry, $M."
        ),
    )


# ===========================================================================
# 4. The satellites-per-launch fork (the per-class binding decision)
# ===========================================================================


def compute_satellites_per_launch(
    dials: SatelliteClassDials,
    *,
    mass_envelope_t: float,
    fairing_volume_m3: float,
    class_name: str,
    dials_path: FieldPath,
    launch_dials_path: FieldPath,
) -> SatellitePacking:
    """The satellites-per-launch fork for one class (mass or stowed-volume bound).

    Computes BOTH the mass-bound count ``floor(mass_envelope_t /
    satellite_mass_t)`` and the stowed-volume-bound count
    ``floor(fairing_volume_m3 / stowed_volume_m3)``, takes the SMALLER as the
    binding count, and records which envelope binds (``MASS`` if the mass count
    is the smaller-or-equal, else ``ANTENNA_STOW``). This is the explicit
    per-class fork the disaster gate requires: broadband binds on mass (about 5
    per launch), direct-to-cell binds on stowed antenna volume (about 1 per
    launch). The caller (the engine) passes the active mass and fairing
    envelopes (baseline or upgraded-Neutron, chosen by
    ``ConstellationDials.upgraded_neutron``); this function does not pick the
    envelope, so the envelope choice is one place.

    Args:
        dials: The per-class packing dials (mass and stowed volume).
        mass_envelope_t: The active Neutron mass envelope to low-inclination
            LEO, tonnes (baseline or upgraded, chosen by the caller).
        fairing_volume_m3: The active Neutron fairing usable volume, m3.
        class_name: ``"broadband"`` or ``"direct_to_cell"``.
        dials_path: JSON path of this class's dials block.
        launch_dials_path: JSON path of the launch-envelope dials block.

    Returns:
        A :class:`SatellitePacking` (the binding count, the binding-constraint
        enum cell, and the two transparency counts).

    Raises:
        ValueError: If ``satellite_mass_t`` or ``stowed_volume_m3`` is not
            positive (the config bounds already guarantee ``gt=0``, but the
            guard makes the division safe and the failure explicit).
    """
    if dials.satellite_mass_t <= 0:
        raise ValueError(
            f"satellite_mass_t must be positive for {class_name} (got {dials.satellite_mass_t})"
        )
    if dials.stowed_volume_m3 <= 0:
        raise ValueError(
            f"stowed_volume_m3 must be positive for {class_name} (got {dials.stowed_volume_m3})"
        )
    mass_bound = math.floor(mass_envelope_t / dials.satellite_mass_t)
    volume_bound = math.floor(fairing_volume_m3 / dials.stowed_volume_m3)
    binding = min(mass_bound, volume_bound)
    constraint = (
        SatelliteBindingConstraint.MASS
        if mass_bound <= volume_bound
        else SatelliteBindingConstraint.ANTENNA_STOW
    )
    mass_bound_cell = cell(
        value=mass_bound,
        unit="count",
        formula_name="comms_satellites_per_launch_mass_bound",
        uses=[
            f"{launch_dials_path}.neutron_mass_envelope_t",
            f"{dials_path}.satellite_mass_t",
        ],
        sources=["research/comms_model_design/DESIGN.md#section-4"],
        description=(
            f"{class_name} satellites per launch when mass-bound (floor of envelope / sat mass)."
        ),
    )
    volume_bound_cell = cell(
        value=volume_bound,
        unit="count",
        formula_name="comms_satellites_per_launch_volume_bound",
        uses=[
            f"{launch_dials_path}.neutron_fairing_volume_m3",
            f"{dials_path}.stowed_volume_m3",
        ],
        sources=["research/comms_model_design/DESIGN.md#section-4"],
        description=(
            f"{class_name} satellites per launch when stowed-antenna-volume-bound "
            f"(floor of fairing volume / stowed volume)."
        ),
    )
    binding_cell = cell(
        value=binding,
        unit="count",
        formula_name="comms_satellites_per_launch_fork",
        uses=[
            f"{dials_path}.mass_bound_count",
            f"{dials_path}.volume_bound_count",
        ],
        sources=["research/comms_model_design/DESIGN.md#section-4"],
        description=(
            f"{class_name} satellites per launch: the smaller of the mass-bound "
            f"and the stowed-volume-bound count."
        ),
    )
    constraint_cell = cell(
        value=constraint.value,
        unit="enum",
        formula_name="comms_satellite_binding_constraint",
        uses=[
            f"{dials_path}.mass_bound_count",
            f"{dials_path}.volume_bound_count",
        ],
        sources=["research/comms_model_design/DESIGN.md#section-4"],
        description=(
            f"Which envelope binds {class_name} satellites-per-launch "
            f"(mass for broadband, antenna-stow for direct-to-cell)."
        ),
    )
    return SatellitePacking(
        satellites_per_launch=binding_cell,
        binding_constraint=constraint_cell,
        mass_bound_count=mass_bound_cell,
        volume_bound_count=volume_bound_cell,
    )


def compute_launch_cost_per_satellite(
    satellites_per_launch: int,
    *,
    launches_per_year: int,
    launch_dials: LaunchDials,
    dials_path: FieldPath,
    satellites_per_launch_path: FieldPath,
) -> ProvenanceCell:
    """Per-satellite share of the cadence-indexed Neutron launch cost, $M.

    Calls ``common.cadence.compute_launch_cost_musd(launches_per_year, ...)``
    (REUSED VERBATIM) to price the launch at this year's cadence, then divides
    by ``satellites_per_launch``. This is the one thin comms wrapper around the
    reused cadence machinery.

    Args:
        satellites_per_launch: The binding per-launch satellite count.
        launches_per_year: This year's cadence (whole-number launches).
        launch_dials: The launch-cost dials (for ``compute_launch_cost_musd``).
        dials_path: JSON path of the launch-cost dials block.
        satellites_per_launch_path: JSON path of the per-launch-count cell.

    Returns:
        A :class:`ProvenanceCell` carrying the per-satellite launch cost, $M.

    Raises:
        ValueError: If ``satellites_per_launch`` is not positive.
    """
    if satellites_per_launch <= 0:
        raise ValueError(f"satellites_per_launch must be positive (got {satellites_per_launch})")
    launch_cost = compute_launch_cost_musd(
        launches_per_year,
        dials_path=dials_path,
        low_cadence_cost_musd=launch_dials.low_cadence_cost_musd,
        high_cadence_cost_musd=launch_dials.high_cadence_cost_musd,
        low_cadence_launches=launch_dials.low_cadence_launches,
        high_cadence_launches=launch_dials.high_cadence_launches,
    )
    per_satellite = _cell_float(launch_cost) / satellites_per_launch
    return cell(
        value=per_satellite,
        unit="MUSD",
        formula_name="comms_launch_cost_per_satellite_from_cadence",
        uses=[
            f"{dials_path}.launch_cost_musd",
            satellites_per_launch_path,
        ],
        sources=[
            "research/SOURCE_INDEX.md#NTR-009",
            "research/rocket_lab/neutron/launch_cost_economics.md",
        ],
        description="Per-satellite share of the cadence-indexed Neutron launch cost, $M.",
    )


# ===========================================================================
# 5. The learning-curve cost-down and the V4 capability step
# ===========================================================================


def compute_learning_curve_multiplier(
    cumulative_units: int,
    *,
    learning_rate_per_doubling: float,
    reference_units: int,
    cost_down_path: FieldPath,
) -> ProvenanceCell:
    """The Wright-style learning-curve cost multiplier at a cumulative-units count.

    Multiplier ``= (cumulative_units / reference_units) **
    log2(1 - learning_rate_per_doubling)``. At ``learning_rate_per_doubling =
    0`` the exponent is ``log2(1) = 0`` so the multiplier is ``1.0`` (no
    learning, flat cost) for any cumulative count. At ``cumulative_units =
    reference_units`` the ratio is ``1`` so the multiplier is ``1.0`` (the
    un-discounted anchor). This is the FORM concern C2 pins in Phase 1 (the
    dial) and registers here (the formula): a fractional reduction per DOUBLING
    of cumulative units built.

    Args:
        cumulative_units: Cumulative satellites built through this point
            (``>= 1``; the engine passes the running cumulative deployed count).
        learning_rate_per_doubling: The fractional reduction per doubling
            (``[0, 1)``; 0.0 = no learning, 0.2 = an 80-percent learning curve).
        reference_units: The reference cumulative-units count N0 at which the
            cost equals the un-discounted configured cost (``>= 1``).
        cost_down_path: JSON path of the cost-down dials block.

    Returns:
        A :class:`ProvenanceCell` carrying the dimensionless cost multiplier
        (unit ``"multiplier"``).

    Raises:
        ValueError: If ``cumulative_units`` or ``reference_units`` is not
            positive, or ``learning_rate_per_doubling`` is not in ``[0, 1)``.
    """
    if cumulative_units <= 0:
        raise ValueError(f"cumulative_units must be positive (got {cumulative_units})")
    if reference_units <= 0:
        raise ValueError(f"reference_units must be positive (got {reference_units})")
    if not 0.0 <= learning_rate_per_doubling < 1.0:
        raise ValueError(
            f"learning_rate_per_doubling must be in [0, 1) (got {learning_rate_per_doubling})"
        )
    exponent = math.log2(1.0 - learning_rate_per_doubling)
    multiplier = (cumulative_units / reference_units) ** exponent
    return cell(
        value=multiplier,
        unit="multiplier",
        formula_name="comms_learning_curve_multiplier",
        uses=[
            f"{cost_down_path}.learning_rate_per_doubling",
            f"{cost_down_path}.cost_down_reference_units",
        ],
        sources=["research/comms_model_design/DESIGN.md#section-3"],
        description=(
            "Wright-style learning-curve cost multiplier at a cumulative-units "
            "count (dimensionless)."
        ),
    )


def compute_satellite_build_cost_after_learning(
    build_cost_musd: float,
    learning_multiplier: float,
    *,
    build_cost_path: FieldPath,
    learning_multiplier_path: FieldPath,
) -> ProvenanceCell:
    """Per-satellite build cost after the learning-curve discount, $M.

    Args:
        build_cost_musd: The un-discounted per-satellite build cost, $M.
        learning_multiplier: The learning-curve cost multiplier (dimensionless).
        build_cost_path: JSON path of the un-discounted build-cost cell.
        learning_multiplier_path: JSON path of the learning-multiplier cell.

    Returns:
        A :class:`ProvenanceCell` carrying the discounted build cost, $M.
    """
    return cell(
        value=build_cost_musd * learning_multiplier,
        unit="MUSD",
        formula_name="comms_satellite_build_cost_after_learning",
        uses=[build_cost_path, learning_multiplier_path],
        sources=["research/comms_model_design/DESIGN.md#section-3"],
        description="Per-satellite build cost after the learning-curve discount, $M.",
    )


def compute_capability_after_v4_step(
    base_capability: float,
    v4_capability_multiplier: float,
    *,
    base_capability_path: FieldPath,
    multiplier_path: FieldPath,
    capability_unit: str,
) -> ProvenanceCell:
    """Per-satellite capability after the optional V4 capability-step multiplier.

    The V4 step is a single configurable multiplier on a V3-class base
    capability (NOT a multi-generation frontier engine, which is dropped for
    comms). Default multiplier 1.0 leaves the base unchanged (the V3 anchor).
    ``base_capability`` and ``capability_unit`` are passed by the caller so this
    function is unit-agnostic (the engine decides what capability quantity the
    V4 step scales, e.g. per-beam capacity or per-satellite throughput).

    Args:
        base_capability: The V3-class base capability value.
        v4_capability_multiplier: The dimensionless V4 step (``> 0``; 1.0 = no step).
        base_capability_path: JSON path of the base-capability cell/dial.
        multiplier_path: JSON path of the V4-multiplier dial.
        capability_unit: The unit string of the capability quantity.

    Returns:
        A :class:`ProvenanceCell` carrying the stepped capability.
    """
    return cell(
        value=base_capability * v4_capability_multiplier,
        unit=capability_unit,
        formula_name="comms_capability_after_v4_step",
        uses=[base_capability_path, multiplier_path],
        sources=["research/comms_model_design/DESIGN.md#section-8"],
        description="Per-satellite capability after the optional V4 capability-step multiplier.",
    )


# ===========================================================================
# 6. The total per-satellite cost and the annualized cost
# ===========================================================================


def compute_satellite_total_cost(
    build_cost_after_learning_musd: float,
    launch_cost_per_satellite_musd: float,
    *,
    build_cost_path: FieldPath,
    launch_cost_path: FieldPath,
) -> ProvenanceCell:
    """Total per-satellite cost: discounted build cost plus the launch share, $M.

    The comms analog of summing the DC node build + launch.

    Args:
        build_cost_after_learning_musd: Discounted per-satellite build cost, $M.
        launch_cost_per_satellite_musd: Per-satellite launch share, $M.
        build_cost_path: JSON path of the discounted build-cost cell.
        launch_cost_path: JSON path of the per-satellite launch-cost cell.

    Returns:
        A :class:`ProvenanceCell` carrying the total per-satellite cost, $M.
    """
    return cell(
        value=build_cost_after_learning_musd + launch_cost_per_satellite_musd,
        unit="MUSD",
        formula_name="comms_satellite_total_cost_from_build_and_launch",
        uses=[build_cost_path, launch_cost_path],
        sources=["research/comms_model_design/DESIGN.md#section-3"],
        description=(
            "Total per-satellite cost: discounted build cost plus the "
            "per-satellite launch share, $M."
        ),
    )


def compute_satellite_cost_annual(
    satellite_total_musd: float,
    satellite_lifetime_years: int,
    *,
    satellite_total_path: FieldPath,
    lifetime_path: FieldPath,
) -> ProvenanceCell:
    """Annualized per-satellite cost over the service life, $M/yr.

    Mirrors the DC ``compute_cost_annual_per_node``: the total per-satellite
    cost spread over the service-life cliff. ``0.0`` if the lifetime is not
    positive (the guarded zero, matching the DC zero-guard).

    Args:
        satellite_total_musd: Total per-satellite cost, $M.
        satellite_lifetime_years: The service-life cliff in years.
        satellite_total_path: JSON path of the total-cost cell.
        lifetime_path: JSON path of the lifetime dial.

    Returns:
        A :class:`ProvenanceCell` carrying the annualized per-satellite cost,
        $M/yr.
    """
    if satellite_lifetime_years <= 0:
        annual = 0.0
    else:
        annual = satellite_total_musd / satellite_lifetime_years
    return cell(
        value=annual,
        unit="MUSD",
        formula_name="comms_satellite_cost_annual_from_total_and_life",
        uses=[satellite_total_path, lifetime_path],
        sources=["research/comms_model_design/DESIGN.md#section-3"],
        description="Annualized per-satellite cost over the service-life cliff, $M/yr.",
    )


# ===========================================================================
# 7. Private helpers
# ===========================================================================


def _cell_float(c: ProvenanceCell) -> float:
    """Read a numeric cell value as a plain float for downstream math.

    Args:
        c: A provenance cell whose value is a number.

    Returns:
        The cell value coerced to ``float``.

    Raises:
        TypeError: If the cell value is not a real number (None, str, bool).
    """
    value = c.value
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"cell value is not numeric: {value!r} (cell: {c.formula_name})")
    return float(value)


__all__ = [
    "SatelliteBindingConstraint",
    "SatelliteCohort",
    "SatelliteCostBreakdown",
    "SatellitePacking",
    "compute_capability_after_v4_step",
    "compute_launch_cost_per_satellite",
    "compute_learning_curve_multiplier",
    "compute_satellite_build_cost",
    "compute_satellite_build_cost_after_learning",
    "compute_satellite_cost_annual",
    "compute_satellite_cost_breakdown",
    "compute_satellite_total_cost",
    "compute_satellites_per_launch",
]
