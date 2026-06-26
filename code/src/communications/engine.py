"""The communications CELLULAR cost engine: the per-year cohort treadmill.

``run_comms_model(config)`` drives the slim cost-to-serve model across the
horizon and returns a :class:`CommsTrajectory` of plain-numeric per-year rollups.
It mirrors the data-center model's fleet engine (the per-year loop in
``data_center/engine.py`` plus the living-cohort rollup in ``data_center/fleet.py``)
with three deliberate differences, all driven by the comms design:

1. Satellites per launch. The DC deploys one node per launch; comms deploys
   ``satellites_per_launch`` satellites per launch, so
   ``satellites_deployed_this_year = comms_launches_flown_this_year * satellites_per_launch``.
2. The build-and-hold cap (the treadmill). The DC fleet grows with cadence
   without bound. Comms builds toward the FLEET TARGET (the CAPACITY-sized fleet,
   :func:`compute_fleet_target`: the subscriber target divided by the per-satellite
   density, floored by the coverage floor and capped by the saturation cap) and
   then HOLDS: once the target is reached it deploys only enough whole launches to
   replace the cohorts ageing off the 5-year cliff, so the living count stays at (or
   as close as launch granularity allows to) the fleet target.
3. Two cadence roles. The shared whole-fleet logistic ramp
   (``common.cadence.compute_launches_per_year``, the 90/year FY2036 ramp) sets
   the WHOLE-fleet launch count. The comms slice flies a SHARE of it
   (``share_of_fleet``). The launch COST is priced at the WHOLE-fleet cadence
   (the cadence-indexed cost-down is a Neutron-production-scale effect shared
   across the whole program, not the comms slice's own rate); the comms share
   sets only how many launches comms flies. This is the load-bearing
   distinction: cost is priced at fleet cadence, the count flown is the comms
   share. (If the founder later wants the comms slice priced at its own lower
   cadence, that is a documented alternative; the default is fleet-cadence
   pricing.)

The cohort cliff is the shared ``common.cohort.LivedCohort`` /
``living_cohorts`` machinery, reused unchanged: a cohort is alive in the
half-open interval ``[launch_year, launch_year + satellite_lifetime_years)``.
The shared ``LivedCohort`` carries only ``launch_year`` + ``units_deployed``,
which is exactly what comms needs (no per-satellite economics ride on the
cohort, unlike the DC ``Cohort``), so comms uses it directly with no subclass.

The two shared ``common.cadence`` functions return a ``ProvenanceCell``; this
engine unwraps each ``.value`` to a plain ``float``/``int`` ONCE (via the
private ``_cell_float`` / ``_cell_int`` helpers, mirroring the DC engine) at the
single seam where the model touches a cell. Everything downstream is plain
numerics; the comms output stays light (no provenance envelope).

This module imports only from ``common.*`` and ``communications.*`` (never
``data_center``, per the cross-import guard) and uses none of the forbidden
demand-side tokens. It also carries the subscriber mapping
(:func:`subscribers_served_at`): subscribers are PEOPLE (phone subscribers, the
CELLULAR direct-to-cell unit, NOT households). The fleet is CAPACITY-SIZED to serve
the subscriber TARGET (the input base), and the served count RAMPS with the buildout
(``subscriber_target x min(1.0, living_fleet / fleet_target)``), reaching the target
at full deployment. This is a sized-base mapping, NOT the old spectrum -> capacity ->
demand chain (cut) and NOT the coverage-fraction-times-base mapping it replaced (the
served base is now the input, and the fleet is what is built toward). The engine
reports the served-people count at the FINAL year's buildout
(``CommsTrajectory.subscribers_served``) plus the annual cost per subscriber against
the target (``cost_per_subscriber_annual_usd``); the output layer (Phase 5) and the
ground ratio (Phase 4) consume the per-subscriber figure.

THE OVERSHOOT RULE (frozen here and in the parity test). Launches are granular
(a whole launch deploys ``satellites_per_launch`` satellites at once), so the
last build-out launch may push the living count slightly OVER the target. The
rule, applied uniformly in BOTH the build-out and HOLD phases: the satellites to
add this year are the deficit to the target (``target - living_before``) rounded
UP to a whole number of launches (``_ceil_to_launch``), capped by the comms
cadence share for the year (``would_be_deployed``). This lets the final build
cohort overshoot the target by strictly less than one launch's worth and never
deploys beyond what is needed to hold. During HOLD the deficit equals exactly
that year's cliff losses, so the same formula replaces only the ageing cohorts.

Units: money in $M; counts are integers; time in fiscal years (FY2026..FY2036,
year 0 = ``base_year``).
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass

from common.cadence import (
    ROUND_TO_NEAREST_OFFSET,
    compute_launch_cost_musd,
    compute_launches_per_year,
)
from common.cohort import LivedCohort, living_cohorts
from common.provenance import ProvenanceCell
from communications.config import CommsConfig
from communications.constants import BindingRegime

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Fixed model constants (named, never bare literals; see CLAUDE.md).
# ---------------------------------------------------------------------------

FULL_COVERAGE_FRACTION: float = 1.0
"""The coverage fraction at the coverage FLOOR: the living fleet is clamped to this
so the coverage metric (``living_fleet / coverage_floor``) never reports above 1.0
once the fleet meets or exceeds the floor (with a large base the fleet runs well
above the floor, so coverage saturates at 1.0 while the build continues toward the
capacity-sized fleet target)."""

NO_COVERAGE_FRACTION: float = 0.0
"""The lower clamp on the coverage fraction: a negative coverage fraction is
meaningless (the engine never produces one), so it floors at zero."""

FULL_BUILDOUT_FRACTION: float = 1.0
"""The buildout fraction at full deployment: the living fleet is clamped to this so
the served-subscribers mapping (``buildout_fraction x subscriber_target``) never
scales beyond the target when the build overshoots the fleet target by less than one
launch's worth."""

NO_BUILDOUT_FRACTION: float = 0.0
"""The lower clamp on the buildout fraction fed to the served-subscribers mapping: a
negative buildout fraction is meaningless (the engine never produces one), so it
floors at zero before scaling the subscriber target."""

NO_REPLACEMENT_COST_MUSD: float = 0.0
"""The HOLD-phase replacement-cost line value during the BUILD-OUT phase: there is
no steady-state replacement line until the target is first reached, so build-out
years carry 0.0 on the replacement line (their cost is the build-out cost, not a
replacement cost)."""

MUSD_TO_USD: float = 1_000_000.0
"""Conversion from the model's internal money unit ($M) to whole USD. The
cost-per-subscriber figure is reported in USD per subscriber per year (the unit the
ground interface, Phase 4, is on), so the steady-state annual replacement cost (in
$M) is multiplied by this before dividing by the subscriber target."""

ZERO_SUBSCRIBER_TARGET_COST_USD: float = 0.0
"""The cost-per-subscriber value when the subscriber target is zero (it cannot be,
the dial is ``ge=1``, but the division is guarded for total safety) or the build-out
never reached steady state within the horizon (steady-state annual cost is 0.0, so
the per-subscriber figure is 0.0, a truthful below-steady-state output)."""


# ---------------------------------------------------------------------------
# ProvenanceCell unwrap seam (mirrors the DC engine's _cell_float / _cell_int).
# This is the ONLY place the comms model touches a ProvenanceCell; everything
# downstream is plain floats/ints.
# ---------------------------------------------------------------------------


def _cell_float(c: ProvenanceCell) -> float:
    """Unwrap a numeric :class:`ProvenanceCell` to a plain ``float``.

    Args:
        c: A ProvenanceCell whose ``value`` is numeric.

    Returns:
        The cell's value as a ``float``.

    Raises:
        TypeError: If the cell's value is a bool or not a real number.
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
        TypeError: If the cell's value is a bool or not an int.
    """
    if isinstance(c.value, bool) or not isinstance(c.value, int):
        raise TypeError(f"ProvenanceCell {c.formula_name!r} is not an int: {c.value!r}")
    return c.value


# ---------------------------------------------------------------------------
# Integer launch-count helpers (reuse the shared half-up offset; do not redefine).
# ---------------------------------------------------------------------------


def _round_half_up(x: float) -> int:
    """Round a non-negative rate to an integer launch count, half up.

    Mirrors ``common.cadence._integer_launch_count`` using the shared
    ``ROUND_TO_NEAREST_OFFSET`` authority (imported from ``common.cadence``, not
    redefined): ``floor(x + 0.5)``. Used to turn the comms slice's fractional
    ``fleet_launches * share_of_fleet`` into a whole launch count.

    Args:
        x: A non-negative rate (the comms slice of the fleet launch count).

    Returns:
        The nearest whole-number launch count, rounded half up.
    """
    return math.floor(x + ROUND_TO_NEAREST_OFFSET)


def _ceil_to_launch(satellites_needed: int, satellites_per_launch: int) -> int:
    """Round a satellite deficit UP to a whole number of launches' worth.

    The build is granular: satellites are added a whole launch at a time. This
    rounds the satellite deficit to the target up to the next multiple of
    ``satellites_per_launch`` (the overshoot rule), so the final build launch may
    push the living count over the target by strictly less than one launch's
    worth.

    Args:
        satellites_needed: Satellites still needed to reach the target this year
            (already floored at 0 by the caller).
        satellites_per_launch: Satellites deployed per launch (a positive count).

    Returns:
        ``satellites_needed`` rounded up to the next multiple of
        ``satellites_per_launch`` (``0`` when nothing is needed).
    """
    if satellites_needed <= 0:
        return 0
    launches = math.ceil(satellites_needed / satellites_per_launch)
    return launches * satellites_per_launch


# ---------------------------------------------------------------------------
# The capacity-sizing of the fleet (the NEW capacity dimension).
#
# The fleet is sized to SERVE the subscriber base, not merely to cover it. The
# capacity NEED is the subscriber target divided by the per-satellite attached
# density (rounded UP, since a partial satellite's worth of need still requires a
# whole satellite of capacity). The fleet target floors that at the coverage floor
# (everyone must see a satellite) and caps it at the saturation cap (past which the
# spread servable base is exhausted). Which term binds is reported as the
# BindingRegime (the founder's coverage-vs-capacity question).
# ---------------------------------------------------------------------------


def compute_fleet_target(
    *,
    subscriber_target: int,
    subscribers_per_satellite: int,
    coverage_floor: int,
    max_fleet_satellites: int,
) -> tuple[int, BindingRegime]:
    """Size the fleet to serve the subscriber base, and report which constraint binds.

    The capacity need is ``ceil(subscriber_target / subscribers_per_satellite)``: the
    satellites required to carry the attached base at the per-satellite density. The
    fleet target floors that at ``coverage_floor`` and caps it at
    ``max_fleet_satellites``::

        fleet_target = min(max_fleet_satellites,
                           max(coverage_floor, capacity_need))

    Worked at the defaults (75,000 attached/sat, 340 floor, 2,000 cap):
    10M -> ceil(134) -> max(340, 134) = 340 (the coverage floor binds);
    50M -> 667 -> 667 (capacity binds); 100M -> 1,334 -> 1,334 (capacity binds,
    under the 2,000 cap).

    Args:
        subscriber_target: The subscriber base to serve (the input), people.
        subscribers_per_satellite: The attached subscribers one satellite carries.
        coverage_floor: The minimum fleet for everyone to see a satellite (the lower
            bound on the target).
        max_fleet_satellites: The saturation cap (the upper bound on the target).

    Returns:
        A 2-tuple ``(fleet_target, binding_regime)``: the capacity-sized fleet the
        build-out fills toward, and which constraint set it (the coverage floor, the
        capacity need, or the saturation cap).
    """
    capacity_need = math.ceil(subscriber_target / subscribers_per_satellite)
    floored = max(coverage_floor, capacity_need)
    fleet_target = min(max_fleet_satellites, floored)
    if capacity_need >= max_fleet_satellites:
        binding_regime = BindingRegime.SATURATED
    elif capacity_need <= coverage_floor:
        binding_regime = BindingRegime.COVERAGE
    else:
        binding_regime = BindingRegime.CAPACITY
    return fleet_target, binding_regime


# ---------------------------------------------------------------------------
# The buildout-to-subscribers mapping (the NEW capacity-sized logic).
#
# Subscribers are PEOPLE (phone subscribers, the CELLULAR direct-to-cell unit),
# NOT households (a household is the broadband unit). The served count RAMPS with
# the buildout: the subscriber TARGET is the base, and the fraction served is the
# fraction of the capacity-sized FLEET TARGET on orbit. At full deployment it
# equals the target. This is a sized-base map (target x living/fleet_target), NOT
# the old spectrum -> capacity -> demand chain (cut) and NOT the prior
# coverage-fraction-times-base map (the served base is now the input, and the fleet
# is what is built toward). There is no beam, spectral-efficiency, or capacity term.
# ---------------------------------------------------------------------------


def subscribers_served_at(
    buildout_fraction: float,
    *,
    subscriber_target: int,
    override: int | None,
) -> int:
    """Map a fleet-buildout fraction to the served-PERSON count (the cellular subscribers).

    The mapping is linear in the buildout fraction: at full deployment
    (``buildout_fraction == 1.0``) the fully-built constellation serves the whole
    subscriber target; at partial deployment it serves proportionally fewer people.
    The base is the optional direct override when supplied, otherwise the subscriber
    ``subscriber_target`` dial.

    Subscribers are PEOPLE (phone subscribers), not households, because the product
    is CELLULAR direct-to-cell. The figure is a sized served-base count (the target
    scaled by how much of the capacity-sized fleet is on orbit), NOT a demand or
    market estimate, and it carries no capacity/spectrum/beam term.

    Args:
        buildout_fraction: The fraction of the capacity-sized fleet target currently
            on orbit (``living_fleet / fleet_target``, the engine's per-year
            ``CommsYear.buildout_fraction``). Clamped to ``[0.0, 1.0]`` before
            scaling, so an out-of-range value (the engine never produces one) cannot
            push the served count below zero or above the base.
        subscriber_target: The served-PERSON count at full deployment (the configured
            subscriber target). Used when ``override`` is ``None``.
        override: The OPTIONAL direct served-base scalar. When not ``None`` it
            replaces ``subscriber_target`` as the full-deployment base (the model
            serves this absolute count at full deployment; below it the count still
            scales by the buildout fraction).

    Returns:
        The served-PERSON count at the given buildout fraction, rounded half up to a
        whole person (``round_half_up(clamped_buildout_fraction * base)``).
    """
    base = override if override is not None else subscriber_target
    clamped = min(FULL_BUILDOUT_FRACTION, max(NO_BUILDOUT_FRACTION, buildout_fraction))
    return _round_half_up(clamped * base)


def _cost_per_subscriber_annual_usd(
    steady_state_annual_cost_musd: float, subscriber_target: int
) -> float:
    """Divide the steady-state annual cost ($M) by the subscriber target into USD/sub/yr.

    The cost per subscriber is the steady-state annual replacement cost (converted
    from $M to whole USD via :data:`MUSD_TO_USD`) over the subscriber TARGET (the
    full-deployment base, per the spec, not the partial served count). A zero target
    (impossible under the ``ge=1`` dial bound, but guarded) or a zero steady-state
    cost (the build never reached steady state within the horizon) yields
    :data:`ZERO_SUBSCRIBER_TARGET_COST_USD`.

    Args:
        steady_state_annual_cost_musd: The representative HOLD-phase annual cost, $M.
        subscriber_target: The subscriber target (the full-deployment served base).

    Returns:
        The annual cost per subscriber, USD per subscriber per year.
    """
    if subscriber_target <= 0:
        return ZERO_SUBSCRIBER_TARGET_COST_USD
    return steady_state_annual_cost_musd * MUSD_TO_USD / subscriber_target


# ---------------------------------------------------------------------------
# Per-year and whole-trajectory data structures (frozen, plain numerics).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CommsYear:
    """One fiscal year's cost-and-counts rollup (plain numerics, no cells).

    Attributes:
        year: The fiscal year (e.g. 2036).
        fleet_launches_this_year: The whole-fleet integer cadence this year (the
            shared logistic ramp output). The launch cost is priced at this.
        comms_launches_flown_this_year: The comms launches actually flown this
            year, after the cadence share and the build-and-hold cap.
        satellites_deployed_this_year: Satellites added this year
            (= ``comms_launches_flown_this_year * satellites_per_launch``).
        living_fleet: Living satellites at this year under the 5-year cliff,
            counted AFTER this year's cohort is added.
        coverage_fraction: ``living_fleet / coverage_floor``, clamped to 1.0. The
            coverage metric (can everyone see a satellite). With a large subscriber
            base the fleet target exceeds the coverage floor, so this saturates at
            1.0 while the build continues toward the capacity-sized fleet target.
        buildout_fraction: ``living_fleet / fleet_target``, clamped to 1.0. The
            fraction of the capacity-sized fleet on orbit; it drives the served
            subscriber count (the subscriber target scaled by this).
        launch_cost_per_launch_musd: Per-launch cost at the whole-fleet cadence
            this year, $M.
        build_cost_this_year_musd: Satellite hardware build cost this year, $M
            (= ``satellites_deployed_this_year * satellite_build_cost_musd``).
        launch_cost_this_year_musd: Launch cost this year, $M
            (= ``comms_launches_flown_this_year * launch_cost_per_launch_musd``).
        total_cost_this_year_musd: ``build_cost_this_year_musd +
            launch_cost_this_year_musd``.
        is_hold_phase: ``True`` once the build-out target was first reached (this
            year and every year thereafter).
        replacement_cost_this_year_musd: The HOLD-phase ongoing replacement line,
            $M; ``0.0`` during build-out, the year's total cost once in HOLD.
    """

    year: int
    fleet_launches_this_year: int
    comms_launches_flown_this_year: int
    satellites_deployed_this_year: int
    living_fleet: int
    coverage_fraction: float
    buildout_fraction: float
    launch_cost_per_launch_musd: float
    build_cost_this_year_musd: float
    launch_cost_this_year_musd: float
    total_cost_this_year_musd: float
    is_hold_phase: bool
    replacement_cost_this_year_musd: float


@dataclass(frozen=True)
class CommsTrajectory:
    """The whole build-and-hold run: the per-year rollups plus the headlines.

    Attributes:
        years: The per-year rollups, one per model year (FY2026..FY2036).
        total_build_and_hold_cost_musd: The cumulative cost over the trajectory
            (the sum of every year's ``total_cost_this_year_musd``), $M.
        fleet_target: The capacity-sized fleet the build-out fills toward
            (:func:`compute_fleet_target`: the subscriber target divided by the
            per-satellite density, floored by the coverage floor, capped by the
            saturation cap). The treadmill builds and holds to THIS, not the floor.
        subscribers_per_satellite: The attached-subscribers-per-satellite density
            used to size the fleet (echoed from the config for transparency).
        binding_regime: Which constraint set the fleet target (the coverage floor,
            the capacity need, or the saturation cap), the founder's
            coverage-vs-capacity answer for this scenario.
        full_coverage_reached_year: The first fiscal year the living fleet hit the
            FLEET TARGET (full deployment), or ``None`` if it is never reached within
            the horizon (a truthful below-target output, not an error).
        steady_state_annual_replacement_cost_musd: The representative HOLD-phase
            annual replacement cost, $M. Defined as the final model year's
            ``replacement_cost_this_year_musd`` (the steady state once the build
            completes); ``0.0`` if the build never completes within the horizon.
        subscribers_served: The served-PERSON count (cellular phone subscribers) at
            the FINAL year's buildout fraction (FY2036), the buildout mapping
            (:func:`subscribers_served_at`) applied to the subscriber target (or the
            direct override). When the build-out completed, the final buildout
            fraction is ``1.0`` and this equals the target; when it did not, it is
            the proportional partial-deployment count.
        cost_per_subscriber_annual_usd: The steady-state annual cost per subscriber,
            USD/sub/yr: ``steady_state_annual_replacement_cost_musd`` (converted to
            USD) divided by the subscriber TARGET (the full-deployment base, per the
            spec, not the partial served count). ``0.0`` when the build never reached
            steady state within the horizon (the steady-state cost is ``0.0``). This
            is the space side of the ground comparison (Phase 4) and the headline
            cost-to-serve figure.
    """

    years: tuple[CommsYear, ...]
    total_build_and_hold_cost_musd: float
    fleet_target: int
    subscribers_per_satellite: int
    binding_regime: BindingRegime
    full_coverage_reached_year: int | None
    steady_state_annual_replacement_cost_musd: float
    subscribers_served: int
    cost_per_subscriber_annual_usd: float


# ---------------------------------------------------------------------------
# The cadence-share seam: how many launches the comms slice flies this year.
# ---------------------------------------------------------------------------


def _comms_launches_for_year(year_idx: int, config: CommsConfig) -> tuple[int, int, float]:
    """Price one model year's cadence: fleet launches, comms launches, launch cost.

    Calls the two shared ``common.cadence`` functions and unwraps their cells.
    The whole-fleet cadence drives BOTH the comms launch count (via the share)
    and the launch-cost pricing; the comms model never prices launches at its own
    lower slice cadence.

    Args:
        year_idx: Zero-based model year index.
        config: The comms config (provides the cadence, comms-cadence, and
            launch-cost dial blocks).

    Returns:
        A 3-tuple ``(fleet_launches, comms_launches, launch_cost_per_launch_musd)``:
        the whole-fleet integer launch count, the comms slice's integer launch
        count (``round_half_up(fleet_launches * share_of_fleet)``), and the
        per-launch cost in $M priced at the whole-fleet cadence.
    """
    cad = config.cadence
    fleet_launches = _cell_int(
        compute_launches_per_year(
            year_idx,
            cadence_ceiling=cad.cadence_ceiling,
            launches_at_year_5=cad.launches_at_year_5,
            launches_at_year_10=cad.launches_at_year_10,
            first_launch_year=cad.first_launch_year,
        )
    )
    comms_launches = _round_half_up(fleet_launches * config.comms_cadence.share_of_fleet)
    lc = config.launch_cost
    launch_cost_per_launch_musd = _cell_float(
        compute_launch_cost_musd(
            float(fleet_launches),
            low_cadence_cost_musd=lc.low_cadence_cost_musd,
            high_cadence_cost_musd=lc.high_cadence_cost_musd,
            low_cadence_launches=lc.low_cadence_launches,
            high_cadence_launches=lc.high_cadence_launches,
        )
    )
    return fleet_launches, comms_launches, launch_cost_per_launch_musd


# ---------------------------------------------------------------------------
# The build-and-hold treadmill: one model year.
# ---------------------------------------------------------------------------


def _compute_comms_year(
    year_idx: int,
    fy: int,
    config: CommsConfig,
    cohorts: list[LivedCohort],
    fleet_target: int,
    target_already_reached: bool,
) -> tuple[CommsYear, bool]:
    """Roll up one model year: deploy toward the fleet target, hold, and cost it.

    Applies the build-and-hold cap in launch-year order:

    1. Price the cadence (fleet launches, comms launches, launch cost).
    2. ``would_be_deployed = comms_launches * satellites_per_launch`` (the
       cadence-share cap on the build rate this year).
    3. ``living_before`` = the living fleet from PRIOR cohorts under the cliff at
       ``fy`` (cohorts that aged off are already excluded).
    4. ``satellites_added = min(would_be_deployed, ceil_to_launch(max(0,
       fleet_target - living_before), satellites_per_launch))`` (the overshoot rule:
       the deficit rounded up to whole launches, capped by the cadence share).
       During HOLD the deficit equals that year's cliff losses, so this replaces
       only the ageing cohorts.
    5. Append ``LivedCohort(fy, satellites_added)`` and re-derive ``living_after``
       under the cliff (so the living count tracks the cohort window).

    The fleet target is the CAPACITY-sized fleet (:func:`compute_fleet_target`); the
    treadmill builds and holds to it. The coverage metric is reported separately
    against the coverage floor (it can saturate at 1.0 well before full deployment
    when the fleet target exceeds the floor).

    Args:
        year_idx: Zero-based model year index (for the cadence ramp).
        fy: The fiscal year (``base_year + year_idx``), the cohort launch year.
        config: The comms config.
        cohorts: The cohort list so far (this year's cohort is appended in place).
        fleet_target: The capacity-sized fleet the build-out fills toward.
        target_already_reached: Whether the fleet target was reached in a PRIOR year
            (carries the HOLD-phase flag forward across years).

    Returns:
        A 2-tuple ``(comms_year, target_reached_now_or_before)``: the year's
        rollup and the updated "target reached" flag to thread to the next year.
    """
    satellites_per_launch = config.satellite.satellites_per_launch
    life = config.satellite.satellite_lifetime_years
    coverage_floor = config.coverage.satellites_for_full_coverage

    fleet_launches, comms_launches, launch_cost_per_launch_musd = _comms_launches_for_year(
        year_idx, config
    )
    would_be_deployed = comms_launches * satellites_per_launch

    living_before = sum(c.units_deployed for c in living_cohorts(cohorts, fy, life))
    deficit = max(0, fleet_target - living_before)
    satellites_added = min(would_be_deployed, _ceil_to_launch(deficit, satellites_per_launch))
    # The launches actually flown for cost is the whole-launch count we deployed
    # (an integer, since satellites_added is a whole-launch multiple). The cadence
    # share may have allowed more launches than the cap used near the end of the
    # build-out; only the flown launches are costed.
    comms_launches_flown = satellites_added // satellites_per_launch

    cohorts.append(LivedCohort(launch_year=fy, units_deployed=satellites_added))
    living_after = sum(c.units_deployed for c in living_cohorts(cohorts, fy, life))

    coverage_fraction = min(FULL_COVERAGE_FRACTION, living_after / coverage_floor)
    buildout_fraction = min(FULL_BUILDOUT_FRACTION, living_after / fleet_target)
    target_reached_now = target_already_reached or living_after >= fleet_target

    build_cost_this_year_musd = satellites_added * config.satellite.satellite_build_cost_musd
    launch_cost_this_year_musd = comms_launches_flown * launch_cost_per_launch_musd
    total_cost_this_year_musd = build_cost_this_year_musd + launch_cost_this_year_musd
    # The replacement line is the ongoing HOLD-phase cost: 0.0 during build-out,
    # the year's total cost once the target has been reached (this year's cost in
    # HOLD is exactly the replacement of the cohorts that aged off).
    replacement_cost_this_year_musd = (
        total_cost_this_year_musd if target_reached_now else NO_REPLACEMENT_COST_MUSD
    )

    comms_year = CommsYear(
        year=fy,
        fleet_launches_this_year=fleet_launches,
        comms_launches_flown_this_year=comms_launches_flown,
        satellites_deployed_this_year=satellites_added,
        living_fleet=living_after,
        coverage_fraction=coverage_fraction,
        buildout_fraction=buildout_fraction,
        launch_cost_per_launch_musd=launch_cost_per_launch_musd,
        build_cost_this_year_musd=build_cost_this_year_musd,
        launch_cost_this_year_musd=launch_cost_this_year_musd,
        total_cost_this_year_musd=total_cost_this_year_musd,
        is_hold_phase=target_reached_now,
        replacement_cost_this_year_musd=replacement_cost_this_year_musd,
    )
    return comms_year, target_reached_now


# ---------------------------------------------------------------------------
# The engine entry point.
# ---------------------------------------------------------------------------


def run_comms_model(config: CommsConfig) -> CommsTrajectory:
    """Run the build-and-hold cost trajectory for one comms cellular scenario.

    Iterates the model years 0..``horizon_years`` inclusive (FY2026..FY2036 at
    the defaults), deploying satellites toward the CAPACITY-sized FLEET TARGET
    (:func:`compute_fleet_target`: the subscriber target divided by the per-satellite
    density, floored by the coverage floor, capped by the saturation cap), holding
    the constellation once reached (replacing the 5-year-cliff losses), and summing
    the satellite build cost plus the cadence-indexed launch cost over the
    trajectory.

    The launch cost is priced at the WHOLE-fleet Neutron cadence (the shared
    90/year FY2036 ramp drives the cost-down); the comms cadence share sets only
    how many launches comms flies. If the fleet target is too high for the chosen
    cadence share to reach within the horizon, the model still runs and reports a
    living fleet below the target at the final year (a truthful output, surfaced via
    ``full_coverage_reached_year is None`` and a WARNING log), not an error.

    Args:
        config: The comms config (the slim, roughly 6-dial frozen Pydantic tree).
            The all-defaults config reproduces the central case.

    Returns:
        A :class:`CommsTrajectory`: the per-year rollups plus the cumulative
        build-and-hold cost, the fleet target and its binding regime, the first
        full-deployment year (or ``None``), the steady-state annual replacement cost,
        the served-subscriber count, and the annual cost per subscriber.
    """
    base_year = config.metadata.base_year
    horizon_years = config.metadata.horizon_years
    subscriber_target = config.subscribers.subscribers_at_full_coverage
    subscribers_per_satellite = config.subscribers.subscribers_per_satellite

    # Size the fleet to SERVE the subscriber base (the capacity dimension): the
    # treadmill below builds and holds to this fleet target, not the coverage floor.
    fleet_target, binding_regime = compute_fleet_target(
        subscriber_target=subscriber_target,
        subscribers_per_satellite=subscribers_per_satellite,
        coverage_floor=config.coverage.satellites_for_full_coverage,
        max_fleet_satellites=config.coverage.max_fleet_satellites,
    )

    cohorts: list[LivedCohort] = []
    years: list[CommsYear] = []
    target_reached = False
    full_coverage_reached_year: int | None = None

    for year_idx in range(horizon_years + 1):
        fy = base_year + year_idx
        comms_year, target_reached = _compute_comms_year(
            year_idx, fy, config, cohorts, fleet_target, target_reached
        )
        years.append(comms_year)
        if full_coverage_reached_year is None and target_reached:
            full_coverage_reached_year = fy

    total_build_and_hold_cost_musd = sum(y.total_cost_this_year_musd for y in years)
    # The steady-state annual replacement cost is the final model year's
    # replacement line (the representative HOLD-phase annual cost once the build
    # completes); 0.0 if the build never completed within the horizon.
    steady_state_annual_replacement_cost_musd = (
        years[-1].replacement_cost_this_year_musd if years else NO_REPLACEMENT_COST_MUSD
    )
    # The reported subscribers served is the buildout mapping applied to the FINAL
    # year's buildout fraction (FY2036). At a completed build-out the final buildout
    # fraction is 1.0 and this equals the subscriber target (or the override); below
    # full deployment it is the proportional partial-deployment count.
    final_buildout_fraction = years[-1].buildout_fraction if years else NO_BUILDOUT_FRACTION
    subscribers_served = subscribers_served_at(
        final_buildout_fraction,
        subscriber_target=subscriber_target,
        override=config.subscribers.subscribers_served_override,
    )
    # Cost per subscriber per year (the headline cost-to-serve, the space side of the
    # ground comparison): the steady-state annual cost in USD over the subscriber
    # TARGET (the full-deployment base, per the spec). 0.0 when steady state was not
    # reached within the horizon (the steady-state cost is 0.0 then).
    cost_per_subscriber_annual_usd = _cost_per_subscriber_annual_usd(
        steady_state_annual_replacement_cost_musd, subscriber_target
    )

    if full_coverage_reached_year is None:
        logger.warning(
            "Comms build-out did not reach the fleet target (%d satellites, %s regime) within "
            "the %d-year horizon at share_of_fleet=%.3f; living fleet at FY%d is %d. This is a "
            "truthful below-target output, not an error.",
            fleet_target,
            binding_regime.value,
            horizon_years,
            config.comms_cadence.share_of_fleet,
            years[-1].year if years else base_year,
            years[-1].living_fleet if years else 0,
        )

    return CommsTrajectory(
        years=tuple(years),
        total_build_and_hold_cost_musd=total_build_and_hold_cost_musd,
        fleet_target=fleet_target,
        subscribers_per_satellite=subscribers_per_satellite,
        binding_regime=binding_regime,
        full_coverage_reached_year=full_coverage_reached_year,
        steady_state_annual_replacement_cost_musd=steady_state_annual_replacement_cost_musd,
        subscribers_served=subscribers_served,
        cost_per_subscriber_annual_usd=cost_per_subscriber_annual_usd,
    )


__all__ = [
    "CommsTrajectory",
    "CommsYear",
    "compute_fleet_target",
    "run_comms_model",
    "subscribers_served_at",
]
