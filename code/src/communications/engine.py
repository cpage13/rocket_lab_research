"""The communications-model engine: the orchestrator and the promoted space JSON.

``run_comms_model(config, ...)`` drives the Phase-2 engine-room modules across
the horizon and assembles the five-key :class:`CommsModelOutput`. It:
(1) computes the per-satellite four-area cost-out (with the learning-curve
discount and the per-class satellites-per-launch fork) for BOTH satellite
classes at each model year, (2) rolls the per-year cohorts up into the living
fleet via the service-life treadmill (the cohort cliff reused from
``common.cohort``), (3) computes the spectrum requirement, the empirical
per-beam capacity, and the customer-chain planning band, mapping the
direct-to-cell living-fleet satellite count to a served-customer band, and
(4) assembles the typed five-key output, which the lean
:func:`promote_default_space_model` helper serialises to
``communications/models/space/default.json``.

THE C1 RESOLUTION (the headline is the STEADY-STATE figure). The headline mature
per-customer cost, priced revenue, and served-customer band are read at
``config.metadata.steady_state_year`` (default 2036). The engine ALSO emits the
full per-year ``physical`` and ``business`` trajectories across the horizon as a
coarse fill-out ramp for context, exactly as the DC emits per-year blocks; the
steady-state figure is simply the ``business.years."<steady_state_year>"``
record. ``RunMetadata`` carries ``steady_state_year`` so a cold reader (and
Phase 4) knows which year to read.

THE TWO-PARALLEL-CONSTELLATIONS MODELLING CHOICE (load-bearing, founder-
confirmable). The model has TWO satellite classes (broadband, direct-to-cell).
The engine treats them as TWO PARALLEL constellations (each gets the full
cadence of launches), reports each class's cohort, fleet, and cost SEPARATELY,
and reports the DIRECT-TO-CELL customer band as the headline customer number
(the SPECTRUM_spec 2,500-beam chain is the direct-to-cell relationship; mapping
it onto broadband would misapply the anchor). The broadband class is costed and
its fleet tracked, but the D2C customer chain is not forced onto it.

THE V4 STEP IS CAPABILITY-SURFACING, NOT COST- OR CUSTOMER-MOVING in this phase.
The required ``capability`` cell is always populated (its base is the
per-satellite aggregate throughput ``per_beam_capacity_mbps x beams_per_sat``,
scaled by ``v4_capability_multiplier``, an identity at the default 1.0); it does
not feed the cost or the customer band here.

THE ``meta`` BLOCK IS INTENTIONALLY LEAN in this phase (an empty validation
report, the source-status summary, the schema notes); Phase 5 enriches it.

The model is Neutron-only and cost-driven (Amendment A1: demand is assumed, not
modelled): this phase emits NO cost-to-cost ratio, NO retail-undercut check, NO
verdict, NO conclusion label, NO capture-share, NO market-share, and no
heavier-than-Neutron vehicle. The space-side cost, the priced revenue
(cost x 1.5), and the ARPU-collectable revenue are emitted as space-side cells;
the COMPARISON against ground is Phase 4.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Final

from common.cadence import compute_launches_per_year
from common.input_manifest import SourceStatus
from common.meta import SourceStatusSummary, ValidationReport
from common.provenance import FieldPath, ProvenanceCell, cell
from communications.config import (
    CommsConfig,
    SatelliteClassDials,
    load_config,
)
from communications.constants import (
    DEFAULT_ARTIFACT_ROLE,
    MODEL_PACKAGE_NAME,
    PROMOTED_DEFAULT_ARTIFACT_ROLE,
    SCHEMA_VERSION,
    USD_PER_MUSD,
)
from communications.constellation import (
    SatelliteCohort,
    SatelliteCostBreakdown,
    SatellitePacking,
    compute_capability_after_v4_step,
    compute_launch_cost_per_satellite,
    compute_learning_curve_multiplier,
    compute_satellite_build_cost,
    compute_satellite_build_cost_after_learning,
    compute_satellite_cost_annual,
    compute_satellite_cost_breakdown,
    compute_satellite_total_cost,
    compute_satellites_per_launch,
)
from communications.input_manifest import InputManifest, build_comms_input_manifest
from communications.output import (
    BusinessBlock,
    BusinessYear,
    CommsModelOutput,
    CustomerBandBlock,
    MetaBlock,
    PhysicalBlock,
    PhysicalYear,
    RunMetadata,
    SatelliteClassPhysical,
    SatelliteCostBreakdownBlock,
)
from communications.price_reference import (
    compute_arpu_collectable_revenue,
    compute_priced_cost_band,
)
from communications.spectrum import (
    compute_customers_per_beam_band,
    compute_customers_per_sat_band,
    compute_naive_capacity_cross_check,
    compute_per_beam_capacity,
    compute_spectrum_to_acquire,
    compute_total_served_band,
)

logger = logging.getLogger(__name__)

SCHEMA_VERSION_NOTES: Final[str] = (
    "comms-v1 space output: per-year per-class four-area cost-out, the cohort treadmill, "
    "the direct-to-cell customer band, the source-status summary, and a lean (Phase-3) "
    "validation report enriched in Phase 5."
)
"""The schema-version notes literal stamped into the meta block (a named constant
so it is not a bare inline string)."""

# Path constants, resolved relative to this module file (the DC cli.py pattern)
# so the paths are found from a checkout or an installed wheel.
_CALCULATOR_DIR: Final[Path] = Path(__file__).resolve().parents[2]
_PROJECT_DIR: Final[Path] = _CALCULATOR_DIR.parent
_DEFAULT_YAML: Final[Path] = _CALCULATOR_DIR / "scenarios" / "comms_default.yaml"
_PROMOTED_MODEL_DIR: Final[Path] = _PROJECT_DIR / "communications" / "models" / "space"

# The two satellite class names (used to key the per-class records).
_BROADBAND: Final[str] = "broadband"
_DIRECT_TO_CELL: Final[str] = "direct_to_cell"


# ===========================================================================
# 1. Unwrap helpers
# ===========================================================================


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


# ===========================================================================
# 2. The per-class per-year computation
# ===========================================================================


@dataclass(frozen=True)
class SatelliteClassYear:
    """One satellite class's per-year computed state (the in-engine intermediate).

    Holds the per-satellite cost breakdown, the packing fork, the discounted
    per-satellite cost and its annualized form, and the per-launch count, all as
    ProvenanceCells (or the Phase-2 dataclasses of cells). The engine builds one
    per class per year and turns it into a cohort.

    Attributes:
        class_name: ``"broadband"`` or ``"direct_to_cell"``.
        satellites_per_launch: The binding per-launch count (an int, unwrapped).
        packing: The Phase-2 :class:`SatellitePacking` (the fork cells).
        cost_breakdown: The Phase-2 :class:`SatelliteCostBreakdown`.
        build_cost_after_learning_musd: The discounted build cost (a float).
        satellite_total_musd: The total per-satellite cost (a float).
        cost_annual_per_satellite_musd: The annualized per-satellite cost (a float).
        physical: The :class:`SatelliteClassPhysical` output sub-block for this class.
    """

    class_name: str
    satellites_per_launch: int
    packing: SatellitePacking
    cost_breakdown: SatelliteCostBreakdown
    build_cost_after_learning_musd: float
    satellite_total_musd: float
    cost_annual_per_satellite_musd: float
    physical: SatelliteClassPhysical


def compute_satellite_class_year(
    dials: SatelliteClassDials,
    *,
    class_name: str,
    year_idx: int,
    launches_this_year: int,
    cumulative_units_before: int,
    config: CommsConfig,
    mass_envelope_t: float,
    fairing_volume_m3: float,
    per_beam_capacity_mbps: float,
) -> SatelliteClassYear:
    """Compute one satellite class's per-year per-satellite cost and packing.

    Builds the four-area cost breakdown, the per-class satellites-per-launch
    fork (using the active Neutron envelope the caller passes), the
    learning-curve multiplier at the running cumulative-units count, the
    discounted build cost, the per-satellite launch share at this year's
    cadence, the total per-satellite cost, and the annualized cost over the
    service life. ALSO builds the REQUIRED ``capability`` cell via
    :func:`communications.constellation.compute_capability_after_v4_step` (the
    base is the per-satellite aggregate throughput ``per_beam_capacity_mbps x
    beams_per_sat``, unit ``"Mbps"``, scaled by ``v4_capability_multiplier``),
    so the assembled :class:`SatelliteClassPhysical` has every required field
    populated. Returns the in-engine intermediate plus the assembled output
    sub-block.

    Args:
        dials: The per-class cost and packing dials.
        class_name: ``"broadband"`` or ``"direct_to_cell"``.
        year_idx: Model-year index (0 = base year).
        launches_this_year: Whole-number launches in this calendar year.
        cumulative_units_before: Cumulative satellites of this class built before
            this year (the learning-curve count is taken at start-of-year).
        config: The whole comms config (for lifetime, cost-down, launch dials, V4).
        mass_envelope_t: The active Neutron mass envelope (baseline or upgraded).
        fairing_volume_m3: The active Neutron fairing volume (baseline or upgraded).
        per_beam_capacity_mbps: The year's empirical per-beam capacity (Mbps),
            passed so this function can form the aggregate-throughput base for
            the required ``capability`` cell.

    Returns:
        A :class:`SatelliteClassYear`.
    """
    dials_path: FieldPath = f"inputs.config.constellation.{class_name}"
    launch_dials_path: FieldPath = "inputs.config.launch"
    cost_down_path: FieldPath = "inputs.config.cost_down"
    breakdown_path: FieldPath = (
        f'physical.years."{config.metadata.base_year + year_idx}".{class_name}.cost_breakdown'
    )

    breakdown = compute_satellite_cost_breakdown(
        dials, class_name=class_name, dials_path=dials_path
    )
    build_cost = compute_satellite_build_cost(breakdown, breakdown_path=breakdown_path)

    packing = compute_satellites_per_launch(
        dials,
        mass_envelope_t=mass_envelope_t,
        fairing_volume_m3=fairing_volume_m3,
        class_name=class_name,
        dials_path=dials_path,
        launch_dials_path=launch_dials_path,
    )
    satellites_per_launch = _cell_int(packing.satellites_per_launch)

    learning_multiplier = compute_learning_curve_multiplier(
        cumulative_units_before,
        learning_rate_per_doubling=config.cost_down.learning_rate_per_doubling,
        reference_units=config.cost_down.cost_down_reference_units,
        cost_down_path=cost_down_path,
    )
    build_cost_after_learning = compute_satellite_build_cost_after_learning(
        _cell_float(build_cost),
        _cell_float(learning_multiplier),
        build_cost_path=f"{breakdown_path}.build_cost",
        learning_multiplier_path=(
            f'physical.years."{config.metadata.base_year + year_idx}".learning_curve_multiplier'
        ),
    )

    launch_cost_per_satellite = compute_launch_cost_per_satellite(
        satellites_per_launch,
        launches_per_year=launches_this_year,
        launch_dials=config.launch,
        dials_path=launch_dials_path,
        satellites_per_launch_path=f"{breakdown_path}.satellites_per_launch",
    )
    satellite_total = compute_satellite_total_cost(
        _cell_float(build_cost_after_learning),
        _cell_float(launch_cost_per_satellite),
        build_cost_path=f"{breakdown_path}.build_cost_after_learning",
        launch_cost_path=f"{breakdown_path}.launch_cost_per_satellite",
    )
    cost_annual = compute_satellite_cost_annual(
        _cell_float(satellite_total),
        config.constellation.satellite_lifetime_years,
        satellite_total_path=f"{breakdown_path}.satellite_total",
        lifetime_path="inputs.config.constellation.satellite_lifetime_years",
    )

    base_capability = per_beam_capacity_mbps * config.spectrum.beams_per_sat
    capability = compute_capability_after_v4_step(
        base_capability,
        config.constellation.v4_capability_multiplier,
        base_capability_path=(
            f'physical.years."{config.metadata.base_year + year_idx}".per_beam_capacity_mbps'
        ),
        multiplier_path="inputs.config.constellation.v4_capability_multiplier",
        capability_unit="Mbps",
    )

    cost_breakdown_block = SatelliteCostBreakdownBlock(
        antenna=breakdown.antenna,
        comms_electronics=breakdown.comms_electronics,
        solar=breakdown.solar,
        radiator_bus=breakdown.radiator_bus,
        minor_component=breakdown.minor_component,
        build_cost=build_cost,
        build_cost_after_learning=build_cost_after_learning,
        launch_cost_per_satellite=launch_cost_per_satellite,
        satellite_total=satellite_total,
    )
    physical = SatelliteClassPhysical(
        satellites_per_launch=packing.satellites_per_launch,
        binding_constraint=packing.binding_constraint,
        mass_bound_count=packing.mass_bound_count,
        volume_bound_count=packing.volume_bound_count,
        cost_breakdown=cost_breakdown_block,
        cost_annual_per_satellite_musd=cost_annual,
        capability=capability,
    )
    return SatelliteClassYear(
        class_name=class_name,
        satellites_per_launch=satellites_per_launch,
        packing=packing,
        cost_breakdown=breakdown,
        build_cost_after_learning_musd=_cell_float(build_cost_after_learning),
        satellite_total_musd=_cell_float(satellite_total),
        cost_annual_per_satellite_musd=_cell_float(cost_annual),
        physical=physical,
    )


@dataclass(frozen=True)
class CommsYear:
    """One model year's full computed state across both classes plus the spectrum cells.

    Attributes:
        year_idx: Model-year index (0 = base year).
        fy: Calendar year (base_year + year_idx).
        launches_this_year: Whole-number launches this year (an int).
        launch_cost_musd: Per-launch cost at this year's cadence (a float).
        broadband: The broadband :class:`SatelliteClassYear`.
        direct_to_cell: The direct-to-cell :class:`SatelliteClassYear`.
        physical: The assembled :class:`PhysicalYear` output block for this year.
    """

    year_idx: int
    fy: int
    launches_this_year: int
    broadband: SatelliteClassYear
    direct_to_cell: SatelliteClassYear
    physical: PhysicalYear


def compute_comms_year(
    year_idx: int,
    config: CommsConfig,
    *,
    cumulative_broadband_before: int,
    cumulative_direct_to_cell_before: int,
) -> CommsYear:
    """Compute one model year across both satellite classes and the spectrum cells.

    Prices the cadence (launches via ``common.cadence``), picks the active
    Neutron envelope (upgraded vs baseline, the one place this choice lives),
    computes the year's spectrum cells FIRST (the requirement, the empirical
    per-beam capacity, the naive cross-check) so the empirical per-beam capacity
    value is available to thread into both classes' capability bases, then
    computes each class's :class:`SatelliteClassYear`, and assembles those cells
    plus the learning-curve multiplier and the cumulative-built count into the
    :class:`PhysicalYear` output block.

    Args:
        year_idx: Model-year index (0 = base year).
        config: The validated comms config.
        cumulative_broadband_before: Cumulative broadband satellites built before
            this year (threaded by the trajectory loop).
        cumulative_direct_to_cell_before: Cumulative direct-to-cell satellites
            built before this year (threaded by the trajectory loop).

    Returns:
        A :class:`CommsYear`.
    """
    fy = config.metadata.base_year + year_idx
    launches_cell = compute_launches_per_year(
        year_idx,
        dials_path="inputs.config.launch",
        cadence_ceiling=config.launch.cadence_ceiling,
        launches_at_year_5=config.launch.launches_at_year_5,
        launches_at_year_10=config.launch.launches_at_year_10,
        first_launch_year=config.launch.first_launch_year,
    )
    launches_this_year = _cell_int(launches_cell)

    if config.constellation.upgraded_neutron:
        mass_envelope_t = config.launch.upgraded_neutron_mass_envelope_t
        fairing_volume_m3 = config.launch.upgraded_neutron_fairing_volume_m3
    else:
        mass_envelope_t = config.launch.neutron_mass_envelope_t
        fairing_volume_m3 = config.launch.neutron_fairing_volume_m3

    spectrum_path: FieldPath = "inputs.config.spectrum"
    spectrum_to_acquire = compute_spectrum_to_acquire(config.spectrum, dials_path=spectrum_path)
    per_beam_capacity = compute_per_beam_capacity(config.spectrum, dials_path=spectrum_path)
    naive_capacity = compute_naive_capacity_cross_check(config.spectrum, dials_path=spectrum_path)
    per_beam_capacity_mbps = _cell_float(per_beam_capacity)

    broadband = compute_satellite_class_year(
        config.constellation.broadband,
        class_name=_BROADBAND,
        year_idx=year_idx,
        launches_this_year=launches_this_year,
        cumulative_units_before=cumulative_broadband_before,
        config=config,
        mass_envelope_t=mass_envelope_t,
        fairing_volume_m3=fairing_volume_m3,
        per_beam_capacity_mbps=per_beam_capacity_mbps,
    )
    direct_to_cell = compute_satellite_class_year(
        config.constellation.direct_to_cell,
        class_name=_DIRECT_TO_CELL,
        year_idx=year_idx,
        launches_this_year=launches_this_year,
        cumulative_units_before=cumulative_direct_to_cell_before,
        config=config,
        mass_envelope_t=mass_envelope_t,
        fairing_volume_m3=fairing_volume_m3,
        per_beam_capacity_mbps=per_beam_capacity_mbps,
    )

    # The learning-curve multiplier and cumulative-built cells are the same
    # across the two classes only in form; the engine surfaces the broadband
    # cumulative count + multiplier in the physical block (the per-class
    # discounted cost already used each class's own cumulative count, threaded
    # via compute_satellite_class_year). The block-level cells report the
    # direct-to-cell-relevant cumulative built (the headline class), which keeps
    # one cell per year while the per-class discount used the per-class count.
    learning_multiplier_cell = compute_learning_curve_multiplier(
        cumulative_direct_to_cell_before,
        learning_rate_per_doubling=config.cost_down.learning_rate_per_doubling,
        reference_units=config.cost_down.cost_down_reference_units,
        cost_down_path="inputs.config.cost_down",
    )
    cumulative_built_cell = cell(
        value=cumulative_direct_to_cell_before,
        unit="count",
        formula_name="comms_satellites_deployed_passthrough",
        uses=["inputs.config.cost_down.cost_down_reference_units"],
        sources=["research/comms_model_design/DESIGN.md#section-3"],
        description=(
            "Cumulative direct-to-cell satellites built before this year "
            "(the start-of-year learning-curve count)."
        ),
    )

    physical = PhysicalYear(
        year=fy,
        broadband=broadband.physical,
        direct_to_cell=direct_to_cell.physical,
        learning_curve_multiplier=learning_multiplier_cell,
        cumulative_satellites_built=cumulative_built_cell,
        spectrum_to_acquire_mhz=spectrum_to_acquire,
        per_beam_capacity_mbps=per_beam_capacity,
        naive_capacity_mbps=naive_capacity,
    )
    return CommsYear(
        year_idx=year_idx,
        fy=fy,
        launches_this_year=launches_this_year,
        broadband=broadband,
        direct_to_cell=direct_to_cell,
        physical=physical,
    )


# ===========================================================================
# 3. The cohort rollup and the per-year fleet business block
# ===========================================================================


def _comms_year_to_cohorts(
    year: CommsYear,
    config: CommsConfig,
) -> tuple[SatelliteCohort, SatelliteCohort]:
    """Build the (broadband, direct_to_cell) deployment-year cohorts for one year.

    Each cohort carries its launch year, its satellites-deployed count
    (``launches_this_year x satellites_per_launch`` for the class), its
    annualized per-satellite cost (fixed at launch), and its per-satellite
    customer band (three ``customers_per_sat_low/mid/high`` floats).

    THE PER-SATELLITE CUSTOMER-BAND FIELDS ARE CARRIED FOR COHORT-LEVEL
    TRANSPARENCY / FUTURE USE AND ARE INTENTIONALLY NOT THE SOURCE OF THE
    SERVED-CUSTOMER BAND. The authoritative served-customer band is computed at
    the FLEET level in :func:`compute_comms_fleet_trajectory` from the
    direct-to-cell LIVING-FLEET satellite count; the rollup does NOT sum these
    cohort per-sat fields. They exist so a future cohort-vintaged customer view
    (or a cross-check) has the data, and because the Phase-2
    :class:`SatelliteCohort` declares them required, so the engine MUST populate
    them. The direct-to-cell cohort populates them with the spectrum-chain
    per-sat band; the broadband cohort populates them with ``0.0`` (the customer
    chain is not applied to broadband), a truthful "no D2C chain on this class"
    marker, never summed into any reported customer number.

    Args:
        year: The model year's :class:`CommsYear`.
        config: The comms config (for the spectrum dials and beams-per-sat).

    Returns:
        A ``(broadband_cohort, direct_to_cell_cohort)`` tuple.
    """
    spectrum_path: FieldPath = "inputs.config.spectrum"
    per_beam_capacity = compute_per_beam_capacity(config.spectrum, dials_path=spectrum_path)
    per_beam_band = compute_customers_per_beam_band(
        _cell_float(per_beam_capacity),
        config.spectrum.target_per_user_rate_mbps,
        config.spectrum.oversubscription_factor,
        capacity_path=f"{spectrum_path}.per_beam_capacity",
        rate_band_path=f"{spectrum_path}.target_per_user_rate_mbps",
        oversubscription_band_path=f"{spectrum_path}.oversubscription_factor",
    )
    per_sat_band = compute_customers_per_sat_band(
        per_beam_band,
        config.spectrum.beams_per_sat,
        customers_per_beam_path=f"{spectrum_path}.customers_per_beam",
        beams_per_sat_path=f"{spectrum_path}.beams_per_sat",
    )

    broadband_deployed = year.launches_this_year * year.broadband.satellites_per_launch
    direct_to_cell_deployed = year.launches_this_year * year.direct_to_cell.satellites_per_launch

    broadband_cohort = SatelliteCohort(
        launch_year=year.fy,
        satellites_deployed=broadband_deployed,
        cost_annual_per_satellite_musd=year.broadband.cost_annual_per_satellite_musd,
        customers_per_sat_low=0.0,
        customers_per_sat_mid=0.0,
        customers_per_sat_high=0.0,
    )
    direct_to_cell_cohort = SatelliteCohort(
        launch_year=year.fy,
        satellites_deployed=direct_to_cell_deployed,
        cost_annual_per_satellite_musd=year.direct_to_cell.cost_annual_per_satellite_musd,
        customers_per_sat_low=_cell_float(per_sat_band.low),
        customers_per_sat_mid=_cell_float(per_sat_band.mid),
        customers_per_sat_high=_cell_float(per_sat_band.high),
    )
    return broadband_cohort, direct_to_cell_cohort


@dataclass(frozen=True)
class CommsFleetYear:
    """One calendar year's living-fleet rollup for both classes plus the customer band.

    Attributes:
        year: Calendar year for this rollup.
        broadband_living_satellites: Living broadband satellite count (an int).
        direct_to_cell_living_satellites: Living direct-to-cell satellite count (an int).
        business: The assembled :class:`BusinessYear` output block for this year.
    """

    year: int
    broadband_living_satellites: int
    direct_to_cell_living_satellites: int
    business: BusinessYear


def _living_count_and_cost(
    cohorts: list[SatelliteCohort],
    year: int,
    service_life: int,
) -> tuple[int, float]:
    """Return the living satellite count and the cohort-vintaged annual cost for a class.

    Args:
        cohorts: All cohorts of one class deployed so far.
        year: Calendar year to evaluate.
        service_life: The service-life cliff in years.

    Returns:
        A ``(living_satellites, cost_annual_fleet_musd)`` tuple over the cohorts
        within the half-open service-life cliff at ``year``.
    """
    living = [c for c in cohorts if c.is_alive_at(year, service_life)]
    count = sum(c.satellites_deployed for c in living)
    cost = sum(c.satellites_deployed * c.cost_annual_per_satellite_musd for c in living)
    return count, cost


def _per_customer_cost_value(cost_annual_fleet_musd: float, served: float) -> float:
    """Annual per-customer cost, USD/yr: fleet annual cost spread over served customers.

    A NEGATIVE served count is a programming error (a count cannot be negative)
    and raises. A served count of EXACTLY zero is the legitimate early-ramp case
    (no living fleet yet, so no customers and zero fleet cost): the guarded zero
    (``0.0``) is returned rather than a divide-by-zero, matching the DC
    zero-guard philosophy. Under valid dials the steady-state served band is
    strictly positive.

    Args:
        cost_annual_fleet_musd: The living-fleet annual cost, $M/yr.
        served: A served-customer band member (a non-negative count).

    Returns:
        ``cost_annual_fleet_musd x USD_PER_MUSD / served`` USD/yr when ``served``
        is positive, else ``0.0`` when ``served`` is exactly zero.

    Raises:
        ValueError: If ``served`` is negative.
    """
    if served < 0:
        raise ValueError(f"served customers cannot be negative (got {served})")
    if served == 0:
        return 0.0
    return cost_annual_fleet_musd * USD_PER_MUSD / served


def _band_block(
    *,
    low_value: float,
    mid_value: float,
    high_value: float,
    unit: str,
    formula_name: str,
    uses: list[FieldPath],
    sources: list[str],
    description_stub: str,
) -> CustomerBandBlock:
    """Build a :class:`CustomerBandBlock` from three float values plus shared cell metadata.

    Args:
        low_value: The band-low member value.
        mid_value: The band-mid member value.
        high_value: The band-high member value.
        unit: The unit string for all three cells.
        formula_name: The FORMULAS key for all three cells.
        uses: The upstream JSON paths the band derives from.
        sources: Provenance citations for all three cells.
        description_stub: The leading phrase for each member's description.

    Returns:
        A :class:`CustomerBandBlock` of three sibling cells.
    """
    return CustomerBandBlock(
        low=cell(
            value=low_value,
            unit=unit,
            formula_name=formula_name,
            uses=uses,
            sources=sources,
            description=f"{description_stub}, band-low.",
        ),
        mid=cell(
            value=mid_value,
            unit=unit,
            formula_name=formula_name,
            uses=uses,
            sources=sources,
            description=f"{description_stub}, band-mid.",
        ),
        high=cell(
            value=high_value,
            unit=unit,
            formula_name=formula_name,
            uses=uses,
            sources=sources,
            description=f"{description_stub}, band-high.",
        ),
    )


def compute_comms_fleet_trajectory(
    config: CommsConfig,
    years: list[CommsYear],
) -> list[CommsFleetYear]:
    """Build the per-year living-fleet rollup parallel to the per-satellite trajectory.

    For each model year: turns the year's per-class economics into deployment
    cohorts (via :func:`_comms_year_to_cohorts`), rolls the living cohort set up
    under the service-life cliff (the cohort treadmill, reusing the
    ``common.cohort`` cliff), sums each class's living-fleet satellite count and
    annual cost, computes the direct-to-cell served-customer band from the
    direct-to-cell living-fleet satellite count and the spectrum chain, derives
    the per-customer cost band and the priced-cost band, computes the
    ARPU-collectable revenue cell, and assembles the :class:`BusinessYear`
    output block. Threads the two cohort lists across the loop.

    Args:
        config: The comms config.
        years: The per-year :class:`CommsYear` trajectory.

    Returns:
        A list of :class:`CommsFleetYear`, one per element of ``years``.
    """
    service_life = config.constellation.satellite_lifetime_years
    spectrum_path: FieldPath = "inputs.config.spectrum"
    price_reference_path: FieldPath = "inputs.config.price_reference"

    # The per-beam / per-sat customer band is configuration-driven and constant
    # across years, so compute it once outside the loop.
    per_beam_capacity = compute_per_beam_capacity(config.spectrum, dials_path=spectrum_path)
    per_beam_band = compute_customers_per_beam_band(
        _cell_float(per_beam_capacity),
        config.spectrum.target_per_user_rate_mbps,
        config.spectrum.oversubscription_factor,
        capacity_path=f"{spectrum_path}.per_beam_capacity",
        rate_band_path=f"{spectrum_path}.target_per_user_rate_mbps",
        oversubscription_band_path=f"{spectrum_path}.oversubscription_factor",
    )
    per_sat_band = compute_customers_per_sat_band(
        per_beam_band,
        config.spectrum.beams_per_sat,
        customers_per_beam_path=f"{spectrum_path}.customers_per_beam",
        beams_per_sat_path=f"{spectrum_path}.beams_per_sat",
    )

    broadband_cohorts: list[SatelliteCohort] = []
    direct_to_cell_cohorts: list[SatelliteCohort] = []
    fleet_years: list[CommsFleetYear] = []

    for year in years:
        broadband_cohort, direct_to_cell_cohort = _comms_year_to_cohorts(year, config)
        broadband_cohorts.append(broadband_cohort)
        direct_to_cell_cohorts.append(direct_to_cell_cohort)

        broadband_living, broadband_cost = _living_count_and_cost(
            broadband_cohorts, year.fy, service_life
        )
        direct_to_cell_living, direct_to_cell_cost = _living_count_and_cost(
            direct_to_cell_cohorts, year.fy, service_life
        )

        year_path: FieldPath = f'business.years."{year.fy}"'

        total_served = compute_total_served_band(
            per_sat_band,
            direct_to_cell_living,
            customers_per_sat_path=f"{spectrum_path}.customers_per_sat",
            num_satellites_path=f"{year_path}.direct_to_cell_living_fleet",
        )
        served_low = _cell_float(total_served.low)
        served_mid = _cell_float(total_served.mid)
        served_high = _cell_float(total_served.high)

        # The per-customer cost band is the INVERSE pairing on the served band:
        # cost-low uses the served-HIGH count (more customers spreads the fleet
        # cost thinner, so cost-per-customer is lowest at the highest served).
        cost_uses: list[FieldPath] = [
            f"{year_path}.direct_to_cell_cost_annual_fleet_musd",
            f"{year_path}.total_served.low",
            f"{year_path}.total_served.mid",
            f"{year_path}.total_served.high",
        ]
        cost_per_customer = _band_block(
            low_value=_per_customer_cost_value(direct_to_cell_cost, served_high),
            mid_value=_per_customer_cost_value(direct_to_cell_cost, served_mid),
            high_value=_per_customer_cost_value(direct_to_cell_cost, served_low),
            unit="USD",
            formula_name="comms_cost_annual_per_customer_from_fleet_cost_and_served",
            uses=cost_uses,
            sources=["research/comms_model_design/DESIGN.md#section-7"],
            description_stub="Annual direct-to-cell cost to serve one customer, USD/yr",
        )

        # The priced-cost band routes the 1.5x markup through the canonical
        # price_reference.compute_priced_cost_band helper (single production
        # source of the revenue multiple), preserving the full cost-band uses set.
        priced_uses: list[FieldPath] = [
            f"{year_path}.cost_annual_per_customer_usd.low",
            f"{year_path}.cost_annual_per_customer_usd.mid",
            f"{year_path}.cost_annual_per_customer_usd.high",
        ]
        priced_cost = compute_priced_cost_band(
            cost_low=_cell_float(cost_per_customer.low),
            cost_mid=_cell_float(cost_per_customer.mid),
            cost_high=_cell_float(cost_per_customer.high),
            band_uses=priced_uses,
        )

        arpu_collectable = compute_arpu_collectable_revenue(
            config.price_reference, dials_path=price_reference_path
        )

        business = BusinessYear(
            year=year.fy,
            launches=cell(
                value=year.launches_this_year,
                unit="count",
                formula_name="comms_satellites_deployed_passthrough",
                uses=[
                    "inputs.config.launch.cadence_ceiling",
                    "inputs.config.launch.launches_at_year_5",
                    "inputs.config.launch.launches_at_year_10",
                    "inputs.config.launch.first_launch_year",
                ],
                sources=["research/SOURCE_INDEX.md#NTR-010"],
                description="Whole-number launches in this calendar year.",
            ),
            broadband_satellites_deployed_this_year=cell(
                value=year.launches_this_year * year.broadband.satellites_per_launch,
                unit="count",
                formula_name="comms_satellites_deployed_this_year_from_launches_and_per_launch",
                uses=[
                    f"{year_path}.launches",
                    f'physical.years."{year.fy}".broadband.satellites_per_launch',
                ],
                sources=["research/comms_model_design/DESIGN.md#section-4"],
                description="Broadband satellites deployed this year.",
            ),
            direct_to_cell_satellites_deployed_this_year=cell(
                value=year.launches_this_year * year.direct_to_cell.satellites_per_launch,
                unit="count",
                formula_name="comms_satellites_deployed_this_year_from_launches_and_per_launch",
                uses=[
                    f"{year_path}.launches",
                    f'physical.years."{year.fy}".direct_to_cell.satellites_per_launch',
                ],
                sources=["research/comms_model_design/DESIGN.md#section-4"],
                description="Direct-to-cell satellites deployed this year.",
            ),
            broadband_living_fleet=cell(
                value=broadband_living,
                unit="count",
                formula_name="comms_living_fleet_satellites_from_cohort_cliff",
                uses=[f"{year_path}.broadband_satellites_deployed_this_year"],
                sources=["research/comms_model_design/DESIGN.md#section-4"],
                description="Broadband living-fleet satellite count under the service-life cliff.",
            ),
            direct_to_cell_living_fleet=cell(
                value=direct_to_cell_living,
                unit="count",
                formula_name="comms_living_fleet_satellites_from_cohort_cliff",
                uses=[f"{year_path}.direct_to_cell_satellites_deployed_this_year"],
                sources=["research/comms_model_design/DESIGN.md#section-4"],
                description=(
                    "Direct-to-cell living-fleet satellite count under the service-life cliff."
                ),
            ),
            broadband_cost_annual_fleet_musd=cell(
                value=broadband_cost,
                unit="MUSD",
                formula_name="comms_cost_annual_fleet_from_living_cohorts",
                uses=[
                    f"{year_path}.broadband_living_fleet",
                    f'physical.years."{year.fy}".broadband.cost_annual_per_satellite_musd',
                ],
                sources=["research/comms_model_design/DESIGN.md#section-3"],
                description="Broadband living-fleet annual cost, $M/yr.",
            ),
            direct_to_cell_cost_annual_fleet_musd=cell(
                value=direct_to_cell_cost,
                unit="MUSD",
                formula_name="comms_cost_annual_fleet_from_living_cohorts",
                uses=[
                    f"{year_path}.direct_to_cell_living_fleet",
                    f'physical.years."{year.fy}".direct_to_cell.cost_annual_per_satellite_musd',
                ],
                sources=["research/comms_model_design/DESIGN.md#section-3"],
                description="Direct-to-cell living-fleet annual cost, $M/yr.",
            ),
            total_served=CustomerBandBlock(
                low=total_served.low, mid=total_served.mid, high=total_served.high
            ),
            cost_annual_per_customer_usd=cost_per_customer,
            priced_cost_per_customer_usd=priced_cost,
            arpu_collectable_revenue_usd=arpu_collectable,
        )
        fleet_years.append(
            CommsFleetYear(
                year=year.fy,
                broadband_living_satellites=broadband_living,
                direct_to_cell_living_satellites=direct_to_cell_living,
                business=business,
            )
        )
    return fleet_years


# ===========================================================================
# 4. The top-level run and the output assembly
# ===========================================================================


def _model_version() -> str | None:
    """Return the installed package version when import metadata is available.

    The comms analog of the DC ``_model_version``: ``version(MODEL_PACKAGE_NAME)``
    guarded by ``except PackageNotFoundError: return None`` (so an editable
    checkout that was never pip-installed returns ``None``, which is expected).
    """
    try:
        return version(MODEL_PACKAGE_NAME)
    except PackageNotFoundError:
        return None


def _source_status_summary(manifest: InputManifest) -> SourceStatusSummary:
    """Count input assumptions by source-status value.

    Tallies every :class:`InputCell` in the manifest's flat ``assumption_index``
    by its ``source_status`` and returns the eight-count
    :class:`SourceStatusSummary`. The comms analog of the DC
    ``_source_status_summary``: it counts INPUT cells (not the computed
    provenance cells in physical / business).

    Args:
        manifest: The comms input manifest.

    Returns:
        The eight-count source-status summary.
    """
    summary = dict.fromkeys(SourceStatus, 0)
    for input_cell in manifest.assumption_index.values():
        summary[input_cell.source_status] += 1
    return SourceStatusSummary(
        certified=summary[SourceStatus.CERTIFIED],
        sourced_estimate=summary[SourceStatus.SOURCED_ESTIMATE],
        derived_estimate=summary[SourceStatus.DERIVED_ESTIMATE],
        projection=summary[SourceStatus.PROJECTION],
        extrapolation=summary[SourceStatus.EXTRAPOLATION],
        scenario=summary[SourceStatus.SCENARIO],
        placeholder=summary[SourceStatus.PLACEHOLDER],
        stale=summary[SourceStatus.STALE],
    )


def run_comms_model(
    config: CommsConfig,
    *,
    source_scenario_path: str = "unrecorded",
    artifact_role: str = DEFAULT_ARTIFACT_ROLE,
) -> CommsModelOutput:
    """Run the communications model end-to-end and return the comms artifact.

    Computes one :class:`CommsYear` per model year from year 0 to
    ``metadata.horizon_years`` (threading the cumulative-built counts per class
    for the learning curve), rolls the living fleet up by cohort, builds the
    source-linked input manifest, and assembles the five-key
    :class:`CommsModelOutput`. The headline mature figure is the steady-state
    year's record (the C1 resolution); the per-year ramp is carried as context.
    Computes NO cost-to-cost ratio and NO retail-undercut check (Phase 4) and NO
    verdict (the model never bakes in a conclusion).

    Args:
        config: The validated :class:`CommsConfig`.
        source_scenario_path: Repository-relative source scenario path.
        artifact_role: Artifact role to stamp in the output metadata.

    Returns:
        A frozen :class:`CommsModelOutput`.
    """
    reference_units = config.cost_down.cost_down_reference_units
    cumulative_broadband = reference_units
    cumulative_direct_to_cell = reference_units

    years: list[CommsYear] = []
    for year_idx in range(config.metadata.horizon_years + 1):
        comms_year = compute_comms_year(
            year_idx,
            config,
            cumulative_broadband_before=cumulative_broadband,
            cumulative_direct_to_cell_before=cumulative_direct_to_cell,
        )
        years.append(comms_year)
        cumulative_broadband += (
            comms_year.launches_this_year * comms_year.broadband.satellites_per_launch
        )
        cumulative_direct_to_cell += (
            comms_year.launches_this_year * comms_year.direct_to_cell.satellites_per_launch
        )

    fleet_years = compute_comms_fleet_trajectory(config, years)

    physical_by_year: dict[str, PhysicalYear] = {str(y.fy): y.physical for y in years}
    business_by_year: dict[str, BusinessYear] = {str(fy.year): fy.business for fy in fleet_years}

    manifest = build_comms_input_manifest(config=config, source_scenario_path=source_scenario_path)
    source_status_summary = _source_status_summary(manifest)
    meta = MetaBlock(
        validation=ValidationReport(rules=[]),
        source_status_summary=source_status_summary,
        schema_version_notes=SCHEMA_VERSION_NOTES,
    )
    metadata = RunMetadata(
        schema_version=SCHEMA_VERSION,
        scenario_name=config.scenario_levers.scenario_name,
        base_year=config.metadata.base_year,
        horizon_years=config.metadata.horizon_years,
        steady_state_year=config.metadata.steady_state_year,
        generated_at=datetime.now(UTC).isoformat(),
        model_package=MODEL_PACKAGE_NAME,
        model_version=_model_version(),
        artifact_role=artifact_role,
        source_scenario_path=source_scenario_path,
    )
    return CommsModelOutput(
        metadata=metadata,
        inputs=manifest,
        physical=PhysicalBlock(years=physical_by_year),
        business=BusinessBlock(years=business_by_year),
        meta=meta,
    )


# ===========================================================================
# 5. The lean serialize-and-promote helper
# ===========================================================================


def render_comms_json(output: CommsModelOutput) -> str:
    """Serialise a :class:`CommsModelOutput` as indented JSON.

    Wraps ``output.model_dump_json(indent=2)``. The returned string is what the
    promote helper writes and what Phase 5's ``--json`` path will emit.

    Args:
        output: The comms model output to serialise.

    Returns:
        The indented JSON string.
    """
    return output.model_dump_json(indent=2)


def _repo_relative(path: Path) -> str:
    """Return a repository-relative path string for the source-scenario stamp."""
    try:
        return path.relative_to(_PROJECT_DIR).as_posix()
    except ValueError:
        return path.as_posix()


def promote_default_space_model(
    *,
    config_path: Path | None = None,
) -> Path:
    """Run the default comms scenario and write the promoted space JSON to disk.

    Loads the default scenario (``code/scenarios/comms_default.yaml`` when
    ``config_path`` is None), runs :func:`run_comms_model` with the
    promoted-default artifact role, and writes the JSON to
    ``<repo_root>/communications/models/space/default.json`` (creating the
    ``space/`` directory if absent). This is the lean Phase-3 promote so the
    space model genuinely promotes; Phase 5's CLI supersedes it with the
    ``rklb-comms`` console script and the dual-promote (space + ground).

    Args:
        config_path: Scenario YAML to run; defaults to the packaged
            ``comms_default.yaml``.

    Returns:
        The path the promoted JSON was written to.

    Raises:
        FileNotFoundError: If the scenario file does not exist.
        ValueError: If the scenario fails to load or validate.
    """
    yaml_path = config_path if config_path is not None else _DEFAULT_YAML
    config = load_config(yaml_path)
    output = run_comms_model(
        config,
        source_scenario_path=_repo_relative(yaml_path),
        artifact_role=PROMOTED_DEFAULT_ARTIFACT_ROLE,
    )
    path = _PROMOTED_MODEL_DIR / "default.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_comms_json(output) + "\n", encoding="utf-8")
    logger.info("promoted comms space model -> %s", path)
    return path


__all__ = [
    "CommsFleetYear",
    "CommsYear",
    "SatelliteClassYear",
    "compute_comms_fleet_trajectory",
    "compute_comms_year",
    "compute_satellite_class_year",
    "promote_default_space_model",
    "render_comms_json",
    "run_comms_model",
]
