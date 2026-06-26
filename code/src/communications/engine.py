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
   without bound. Comms builds toward a fixed coverage target
   (``satellites_for_full_coverage``) and then HOLDS: once the target is reached
   it deploys only enough whole launches to replace the cohorts ageing off the
   5-year cliff, so the living count stays at (or as close as launch granularity
   allows to) the target.
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
demand-side tokens: subscribers are added by the Phase 3 / Phase 5 output
assembly, not here. The engine is a clean cost-and-counts module; the output
layer (Phase 5) wraps this trajectory and adds the coverage-to-subscriber
mapping (Phase 3) and the ground ratio (Phase 4).

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

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Fixed model constants (named, never bare literals; see CLAUDE.md).
# ---------------------------------------------------------------------------

FULL_COVERAGE_FRACTION: float = 1.0
"""The coverage fraction at the full-coverage target: the living fleet is clamped
to this so coverage never reports above 1.0 when the build overshoots the target
by less than one launch's worth."""

NO_REPLACEMENT_COST_MUSD: float = 0.0
"""The HOLD-phase replacement-cost line value during the BUILD-OUT phase: there is
no steady-state replacement line until the target is first reached, so build-out
years carry 0.0 on the replacement line (their cost is the build-out cost, not a
replacement cost)."""


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
        coverage_fraction: ``living_fleet / satellites_for_full_coverage``,
            clamped to 1.0. Drives the coverage-driven subscriber count (Phase 3).
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
        full_coverage_reached_year: The first fiscal year the living fleet hit
            the coverage target, or ``None`` if the target is never reached
            within the horizon (a truthful below-target output, not an error).
        steady_state_annual_replacement_cost_musd: The representative HOLD-phase
            annual replacement cost, $M. Defined as the final model year's
            ``replacement_cost_this_year_musd`` (the steady state once the build
            completes); ``0.0`` if the build never completes within the horizon.
    """

    years: tuple[CommsYear, ...]
    total_build_and_hold_cost_musd: float
    full_coverage_reached_year: int | None
    steady_state_annual_replacement_cost_musd: float


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
    target_already_reached: bool,
) -> tuple[CommsYear, bool]:
    """Roll up one model year: deploy toward the target, hold, and cost it.

    Applies the build-and-hold cap in launch-year order:

    1. Price the cadence (fleet launches, comms launches, launch cost).
    2. ``would_be_deployed = comms_launches * satellites_per_launch`` (the
       cadence-share cap on the build rate this year).
    3. ``living_before`` = the living fleet from PRIOR cohorts under the cliff at
       ``fy`` (cohorts that aged off are already excluded).
    4. ``satellites_added = min(would_be_deployed, ceil_to_launch(max(0,
       target - living_before), satellites_per_launch))`` (the overshoot rule:
       the deficit rounded up to whole launches, capped by the cadence share).
       During HOLD the deficit equals that year's cliff losses, so this replaces
       only the ageing cohorts.
    5. Append ``LivedCohort(fy, satellites_added)`` and re-derive ``living_after``
       under the cliff (so the living count tracks the cohort window).

    Args:
        year_idx: Zero-based model year index (for the cadence ramp).
        fy: The fiscal year (``base_year + year_idx``), the cohort launch year.
        config: The comms config.
        cohorts: The cohort list so far (this year's cohort is appended in place).
        target_already_reached: Whether the build-out target was reached in a
            PRIOR year (carries the HOLD-phase flag forward across years).

    Returns:
        A 2-tuple ``(comms_year, target_reached_now_or_before)``: the year's
        rollup and the updated "target reached" flag to thread to the next year.
    """
    satellites_per_launch = config.satellite.satellites_per_launch
    life = config.satellite.satellite_lifetime_years
    target = config.coverage.satellites_for_full_coverage

    fleet_launches, comms_launches, launch_cost_per_launch_musd = _comms_launches_for_year(
        year_idx, config
    )
    would_be_deployed = comms_launches * satellites_per_launch

    living_before = sum(c.units_deployed for c in living_cohorts(cohorts, fy, life))
    deficit = max(0, target - living_before)
    satellites_added = min(would_be_deployed, _ceil_to_launch(deficit, satellites_per_launch))
    # The launches actually flown for cost is the whole-launch count we deployed
    # (an integer, since satellites_added is a whole-launch multiple). The cadence
    # share may have allowed more launches than the cap used near the end of the
    # build-out; only the flown launches are costed.
    comms_launches_flown = satellites_added // satellites_per_launch

    cohorts.append(LivedCohort(launch_year=fy, units_deployed=satellites_added))
    living_after = sum(c.units_deployed for c in living_cohorts(cohorts, fy, life))

    coverage_fraction = min(FULL_COVERAGE_FRACTION, living_after / target)
    target_reached_now = target_already_reached or living_after >= target

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
    the defaults), deploying satellites toward the coverage target, holding the
    constellation once reached (replacing the 5-year-cliff losses), and summing
    the satellite build cost plus the cadence-indexed launch cost over the
    trajectory.

    The launch cost is priced at the WHOLE-fleet Neutron cadence (the shared
    90/year FY2036 ramp drives the cost-down); the comms cadence share sets only
    how many launches comms flies. If the coverage target is too high for the
    chosen cadence share to reach within the horizon, the model still runs and
    reports a living fleet below the target at the final year (a truthful output,
    surfaced via ``full_coverage_reached_year is None`` and a WARNING log), not an
    error.

    Args:
        config: The comms config (the slim, roughly 6-dial frozen Pydantic tree).
            The all-defaults config reproduces the central case.

    Returns:
        A :class:`CommsTrajectory`: the per-year rollups plus the cumulative
        build-and-hold cost, the first full-coverage year (or ``None``), and the
        steady-state annual replacement cost.
    """
    base_year = config.metadata.base_year
    horizon_years = config.metadata.horizon_years

    cohorts: list[LivedCohort] = []
    years: list[CommsYear] = []
    target_reached = False
    full_coverage_reached_year: int | None = None

    for year_idx in range(horizon_years + 1):
        fy = base_year + year_idx
        comms_year, target_reached = _compute_comms_year(
            year_idx, fy, config, cohorts, target_reached
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

    if full_coverage_reached_year is None:
        logger.warning(
            "Comms build-out did not reach the coverage target (%d satellites) within the "
            "%d-year horizon at share_of_fleet=%.3f; living fleet at FY%d is %d. This is a "
            "truthful below-target output, not an error.",
            config.coverage.satellites_for_full_coverage,
            horizon_years,
            config.comms_cadence.share_of_fleet,
            years[-1].year if years else base_year,
            years[-1].living_fleet if years else 0,
        )

    return CommsTrajectory(
        years=tuple(years),
        total_build_and_hold_cost_musd=total_build_and_hold_cost_musd,
        full_coverage_reached_year=full_coverage_reached_year,
        steady_state_annual_replacement_cost_musd=steady_state_annual_replacement_cost_musd,
    )


__all__ = [
    "CommsTrajectory",
    "CommsYear",
    "run_comms_model",
]
