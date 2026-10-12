"""Structural tests for the communications engine (the cohort treadmill).

These run the High-Bandwidth Cellular Pure Play defaults (the config default) and
small synthetic configs through the real engine and check its contract: the
trajectory length, the build-and-hold cap (living fleet non-decreasing during
build-out and bounded by one launch's overshoot), the satellites-per-launch
identity, the build-out monotonicity of the comms launch sequence and the
whole-fleet cadence, the cumulative-cost identity, the replacement rule (only
retiring cohorts' replacement counts, never a build tranche), the low-target
sanity case (the target reached at the first launch, HOLD from the next year),
the cliff bite, and the launch-share rounding. They use the real shared cadence /
cohort spine (no mocks), so they also act as an integration check on the
``common.*`` seam. The shared fleet-and-cost loop (``run_fleet_loop``) has its own
tests at the end, under deployment rules written here: it refuses an impossible
deployment, and its cohort cost lines carry each living cohort at the cost locked at
its launch.

The frozen end-to-end numbers of the Iridium family, and the equality tripwire that
compares an Iridium run's shared fleet-and-cost record with a cellular run's whole, live
in ``test_iridium_model.py``; this file checks structural and counting invariants,
which are exact integers (no float tolerance needed except where a cost sum is
compared, where a tight relative tolerance is used).
"""

from __future__ import annotations

import math
from collections.abc import Callable
from enum import StrEnum
from typing import assert_never

import pytest

from common.cadence import ROUND_TO_NEAREST_OFFSET, CadenceDials
from communications.config import (
    CommsCadenceDials,
    CommsConfig,
    CommsMetadataDials,
    CoverageDials,
    RevenueDials,
    SatelliteDials,
    SubscriberDials,
)
from communications.constants import MONTHS_PER_YEAR
from communications.engine import (
    MARGIN_PERCENT_SCALE,
    MUSD_TO_USD,
    CellularRun,
    Deployment,
    DeploymentRuleError,
    DeploymentStep,
    cellular_rule,
    compute_fleet_target,
    first_year_at_target,
    margin_pct,
    per_satellite_annual_cost_musd,
    run_comms_model,
    run_fleet_loop,
)

# The default-config horizon is 10 years after the base year, so the trajectory
# spans FY2026..FY2036 inclusive (11 model years).
EXPECTED_DEFAULT_YEAR_COUNT = 11

# A tight relative tolerance for the one cost-sum identity check (floats sum in a
# different association order than the engine's running accumulation).
COST_SUM_REL_TOL = 1e-9

# A tiny subscriber target whose capacity need (ceil(target / 75,000) == 1) is below
# any coverage floor these tests set, so the fleet target equals the coverage floor.
# This lets a test drive the build target directly via ``satellites_for_full_coverage``
# (the floor), isolating the treadmill / cliff mechanics from the capacity sizing.
FLOOR_BINDING_SUBSCRIBER_TARGET = 1
_FLOOR_BINDING_SUBSCRIBERS = SubscriberDials(
    subscribers_at_full_coverage=FLOOR_BINDING_SUBSCRIBER_TARGET
)


def test_run_returns_trajectory_with_full_horizon() -> None:
    """The default run returns a CellularRun whose two records span FY2026..FY2036 (11 years)."""
    config = CommsConfig()
    run = run_comms_model(config)
    assert isinstance(run, CellularRun)
    for years in (run.fleet.years, run.cellular.years):
        assert len(years) == EXPECTED_DEFAULT_YEAR_COUNT
        assert years[0].year == config.metadata.base_year
        assert years[-1].year == config.metadata.base_year + config.metadata.horizon_years


def test_satellites_deployed_equals_launches_times_per_launch() -> None:
    """Every year: satellites_deployed == comms_launches_flown * satellites_per_launch."""
    config = CommsConfig()
    per_launch = config.satellite.satellites_per_launch
    run = run_comms_model(config)
    for year in run.fleet.years:
        assert year.satellites_deployed_this_year == (
            year.comms_launches_flown_this_year * per_launch
        )


def test_living_fleet_non_decreasing_during_build_out() -> None:
    """The living fleet never shrinks while the build-out is still filling the target.

    During build-out (up to and including the year the target is first reached) the
    default run's additions outpace its retirements, so the living count is
    non-decreasing year over year.
    """
    run = run_comms_model(CommsConfig())
    build_out_years = [
        fleet_year
        for fleet_year, cellular_year in zip(run.fleet.years, run.cellular.years, strict=True)
        if not cellular_year.is_hold_phase
    ]
    for earlier, later in zip(build_out_years, build_out_years[1:], strict=False):
        assert later.living_fleet >= earlier.living_fleet


def test_living_fleet_never_exceeds_target_by_more_than_one_launch() -> None:
    """The living fleet overshoots the FLEET TARGET by strictly less than one launch's worth.

    The overshoot rule rounds the final build cohort up to a whole launch, so the
    living count can sit above the fleet target but by less than
    ``satellites_per_launch``. The fleet target is the capacity-sized fleet the
    treadmill builds toward (the default 10M base floors it at the coverage floor).
    """
    config = CommsConfig()
    per_launch = config.satellite.satellites_per_launch
    run = run_comms_model(config)
    for year in run.fleet.years:
        assert year.living_fleet < run.cellular.fleet_target + per_launch


def test_comms_launch_sequence_non_decreasing_before_completion() -> None:
    """The comms launches flown are non-decreasing in the build years before completion.

    Objective: the cadence share, not the deficit, sets the flown count while the
    build is short of the target. Expected: on the default run (completion 2035) the
    flown count never drops across the years before the completion year. The
    completion year itself flies only the remaining deficit (the final tranche can be
    smaller), and HOLD years replace only the cliff losses, so neither is included.
    The whole-fleet cadence is checked separately (it is always non-decreasing).
    """
    run = run_comms_model(CommsConfig())
    completion_year = run.cellular.full_coverage_reached_year
    assert completion_year is not None
    pre_completion = [y for y in run.fleet.years if y.year < completion_year]
    for earlier, later in zip(pre_completion, pre_completion[1:], strict=False):
        assert later.comms_launches_flown_this_year >= earlier.comms_launches_flown_this_year


def test_fleet_cadence_non_decreasing_every_year() -> None:
    """The whole-fleet cadence (the cost-pricing series) is non-decreasing every year.

    Unlike the comms flown count, the whole-fleet cadence is the raw shared
    logistic ramp and is monotonic across the whole horizon, build-out and HOLD
    alike. The launch cost is priced at this series, so its non-increasing cost
    behaviour (the launch-cost invariant) rests on this monotonicity.
    """
    run = run_comms_model(CommsConfig())
    for earlier, later in zip(run.fleet.years, run.fleet.years[1:], strict=False):
        assert later.fleet_launches_this_year >= earlier.fleet_launches_this_year


def test_launch_cost_per_launch_non_increasing_with_cadence() -> None:
    """The per-launch cost is non-increasing as the fleet cadence ramps (the cost-down)."""
    run = run_comms_model(CommsConfig())
    for earlier, later in zip(run.fleet.years, run.fleet.years[1:], strict=False):
        assert later.launch_cost_per_launch_musd <= earlier.launch_cost_per_launch_musd + 0.0


def test_total_cost_is_sum_of_year_costs() -> None:
    """total_cost_through_final_year_musd equals the sum of the per-year total costs."""
    fleet = run_comms_model(CommsConfig()).fleet
    expected = sum(y.total_cost_this_year_musd for y in fleet.years)
    assert fleet.total_cost_through_final_year_musd == pytest.approx(expected, rel=COST_SUM_REL_TOL)


def test_per_year_total_cost_is_build_plus_launch() -> None:
    """Each year's total cost is exactly its build cost plus its launch cost."""
    run = run_comms_model(CommsConfig())
    for year in run.fleet.years:
        assert year.total_cost_this_year_musd == pytest.approx(
            year.build_cost_this_year_musd + year.launch_cost_this_year_musd,
            rel=COST_SUM_REL_TOL,
        )


def test_build_cost_uses_the_configured_build_cost_scalar() -> None:
    """Each year's build cost equals satellites_deployed * satellite_build_cost_musd."""
    config = CommsConfig()
    build_cost = config.satellite.satellite_build_cost_musd
    run = run_comms_model(config)
    for year in run.fleet.years:
        assert year.build_cost_this_year_musd == pytest.approx(
            year.satellites_deployed_this_year * build_cost, rel=COST_SUM_REL_TOL
        )


def test_replacement_line_never_books_a_build_tranche() -> None:
    """Only retiring cohorts' replacement counts as replacement, never a build tranche.

    Objective: the replacement rule on the default run, which builds through 2035
    while its first cohorts already retire (from 2032). Expected: in build-out years
    (the completion year included) the replaced satellites are exactly
    ``min(deployed, retired)`` and the replacement line costs just those satellites
    and their whole launches, strictly below the year's cost whenever the year also
    builds; in HOLD years every deployed satellite is replacement and the line equals
    the year's total cost. The retired count is re-derived from the living-fleet
    bookkeeping (prior living + deployed - living).
    """
    config = CommsConfig()
    per_launch = config.satellite.satellites_per_launch
    build_cost = config.satellite.satellite_build_cost_musd
    run = run_comms_model(config)
    previous_living = 0
    saw_build_year_replacement = False
    for year, cellular_year in zip(run.fleet.years, run.cellular.years, strict=True):
        deployed = year.satellites_deployed_this_year
        retired = previous_living + deployed - year.living_fleet
        replaced = year.satellites_replaced_this_year
        if cellular_year.is_hold_phase:
            assert replaced == deployed
            assert year.replacement_cost_this_year_musd == pytest.approx(
                year.total_cost_this_year_musd, rel=COST_SUM_REL_TOL
            )
        else:
            assert replaced == min(deployed, retired)
            expected = (
                replaced * build_cost + (replaced // per_launch) * year.launch_cost_per_launch_musd
            )
            assert year.replacement_cost_this_year_musd == pytest.approx(
                expected, rel=COST_SUM_REL_TOL
            )
            if 0 < replaced < deployed:
                saw_build_year_replacement = True
                assert year.replacement_cost_this_year_musd < year.total_cost_this_year_musd
        previous_living = year.living_fleet
    # The default run exercises the mixed case (a build year that also replaces).
    assert saw_build_year_replacement


def test_coverage_fraction_is_living_over_floor_clamped() -> None:
    """coverage_fraction == min(1.0, living_fleet / coverage_floor) every year."""
    config = CommsConfig()
    coverage_floor = config.coverage.satellites_for_full_coverage
    run = run_comms_model(config)
    for year in run.fleet.years:
        assert year.coverage_fraction == pytest.approx(
            min(1.0, year.living_fleet / coverage_floor), rel=COST_SUM_REL_TOL
        )
        assert 0.0 <= year.coverage_fraction <= 1.0


def test_buildout_fraction_is_living_over_fleet_target_clamped() -> None:
    """buildout_fraction == min(1.0, living_fleet / fleet_target) every year."""
    config = CommsConfig()
    run = run_comms_model(config)
    for fleet_year, year in zip(run.fleet.years, run.cellular.years, strict=True):
        assert year.buildout_fraction == pytest.approx(
            min(1.0, fleet_year.living_fleet / run.cellular.fleet_target), rel=COST_SUM_REL_TOL
        )
        assert 0.0 <= year.buildout_fraction <= 1.0


def test_hold_phase_starts_the_year_after_full_coverage() -> None:
    """HOLD begins the year AFTER the target is first reached; the completion year builds.

    Objective: the completion year carries the final build tranche, so it is the last
    build-out year. Expected: on the default run the first HOLD year is
    ``full_coverage_reached_year + 1``, the completion year is not HOLD, and its
    living fleet has reached the target.
    """
    run = run_comms_model(CommsConfig())
    completion_year = run.cellular.full_coverage_reached_year
    assert completion_year is not None
    hold_years = [y.year for y in run.cellular.years if y.is_hold_phase]
    assert hold_years[0] == completion_year + 1
    completion = next(y for y in run.cellular.years if y.year == completion_year)
    assert completion.is_hold_phase is False
    completion_fleet = next(y for y in run.fleet.years if y.year == completion_year)
    assert completion_fleet.living_fleet >= run.cellular.fleet_target


def test_final_year_replacement_is_the_final_year_replacement_line() -> None:
    """The final-year replacement headline is the final model year's replacement line.

    Objective: the headline reads the last year's cash replacement. Expected: on the
    default run (HOLD in the final year, a cohort retiring) the headline equals the
    final year's replacement line, which equals that year's total cost.
    """
    fleet = run_comms_model(CommsConfig()).fleet
    final = fleet.years[-1]
    assert final.satellites_replaced_this_year > 0
    assert fleet.final_year_replacement_cost_musd == final.replacement_cost_this_year_musd
    assert fleet.final_year_replacement_cost_musd == pytest.approx(
        final.total_cost_this_year_musd, rel=COST_SUM_REL_TOL
    )


def test_low_target_reached_at_first_launch_then_holds() -> None:
    """A one-launch-worth target is reached at the first comms launch, then HOLD holds.

    With ``satellites_for_full_coverage`` set to exactly one launch's worth, the
    target is reached the first year a comms launch flies (that year is the
    completion year, still a build year); from the next year on the model is in HOLD,
    and from the completion year on the living fleet pins at the target (the sanity
    of the cap logic). The build-out phase before the first comms launch deploys
    nothing.
    """
    config = CommsConfig()
    per_launch = config.satellite.satellites_per_launch
    # Drive the fleet target to one launch's worth via the coverage floor; the tiny
    # subscriber target keeps the capacity need below the floor so the floor binds.
    low_target_config = config.model_copy(
        update={
            "coverage": CoverageDials(satellites_for_full_coverage=per_launch),
            "subscribers": _FLOOR_BINDING_SUBSCRIBERS,
        }
    )
    run = run_comms_model(low_target_config)
    assert run.cellular.fleet_target == per_launch

    hold_by_year = {y.year: y.is_hold_phase for y in run.cellular.years}
    first_deploy_year = next(y for y in run.fleet.years if y.satellites_deployed_this_year > 0)
    # The target is reached the moment the first comms launch flies; that year is the
    # completion year (a build year, no replacement: nothing has retired yet).
    assert hold_by_year[first_deploy_year.year] is False
    assert first_deploy_year.satellites_replaced_this_year == 0
    assert first_deploy_year.living_fleet == per_launch
    assert run.cellular.full_coverage_reached_year == first_deploy_year.year
    # From the reached year onward the living fleet pins at exactly one launch's
    # worth (the target); every LATER year is HOLD.
    for year in run.fleet.years:
        if year.year >= first_deploy_year.year:
            assert year.living_fleet == per_launch
        if year.year > first_deploy_year.year:
            assert hold_by_year[year.year] is True


def test_five_year_cliff_retires_an_early_cohort() -> None:
    """A cohort launched in FY2026 is gone by FY2031 (the 5-year cliff).

    The default share flies no comms launch in FY2026, so this uses a config that
    forces an early launch (first_launch_year=0, full fleet share) with a target
    high enough that the build-out never caps, isolating the cliff effect. The
    FY2026 cohort is alive in [2026, 2031); at FY2031 it drops out, so the living
    count at FY2031 equals the FY2030 living count plus the FY2031 deployment
    minus the FY2026 cohort that aged off.
    """
    never_capped_target = 100_000
    config = CommsConfig(
        cadence=CadenceDials(
            first_launch_year=0,
            launches_at_year_5=14,
            launches_at_year_10=90,
            cadence_ceiling=150,
        ),
        comms_cadence=CommsCadenceDials(share_of_fleet=1.0),
        coverage=CoverageDials(
            satellites_for_full_coverage=never_capped_target,
            max_fleet_satellites=never_capped_target,
        ),
        subscribers=_FLOOR_BINDING_SUBSCRIBERS,
    )
    run = run_comms_model(config)
    by_year = {y.year: y for y in run.fleet.years}

    fy2026 = by_year[2026]
    fy2030 = by_year[2030]
    fy2031 = by_year[2031]
    # The early cohort actually carries satellites (so the cliff has something to drop).
    assert fy2026.satellites_deployed_this_year > 0
    # The FY2026 cohort (alive [2026, 2031)) is no longer counted at FY2031.
    expected_living_2031 = (
        fy2030.living_fleet
        + fy2031.satellites_deployed_this_year
        - fy2026.satellites_deployed_this_year
    )
    assert fy2031.living_fleet == expected_living_2031


def test_unreached_target_reports_none_and_runs() -> None:
    """A target too high to reach within the horizon still runs, reporting None."""
    unreachable_target = 100_000
    config = CommsConfig(
        # Floor the fleet at 100,000 and lift the cellular fleet cap above it so the floor
        # (not the cap) is the fleet target; the tiny base keeps capacity below it.
        coverage=CoverageDials(
            satellites_for_full_coverage=unreachable_target,
            max_fleet_satellites=unreachable_target,
        ),
        subscribers=_FLOOR_BINDING_SUBSCRIBERS,
    )
    run = run_comms_model(config)
    assert run.cellular.fleet_target == unreachable_target
    assert run.cellular.full_coverage_reached_year is None
    assert len(run.fleet.years) == EXPECTED_DEFAULT_YEAR_COUNT
    # No year reaches HOLD. The final year still builds, and it also replaces the
    # cohort retiring that year: the final-year replacement is that cohort's cost
    # alone, strictly below the year's build-plus-replacement cash.
    assert all(not y.is_hold_phase for y in run.cellular.years)
    final = run.fleet.years[-1]
    assert 0 < final.satellites_replaced_this_year < final.satellites_deployed_this_year
    assert run.fleet.final_year_replacement_cost_musd == final.replacement_cost_this_year_musd
    assert run.fleet.final_year_replacement_cost_musd is not None
    assert run.fleet.final_year_replacement_cost_musd < final.total_cost_this_year_musd


def test_trajectory_surfaces_fleet_target_and_regime() -> None:
    """The cellular record carries the capacity-sized fleet target and its binding regime."""
    cellular = run_comms_model(CommsConfig()).cellular
    # The default 10M base floors the fleet at the coverage floor (340), coverage regime.
    assert cellular.fleet_target == CommsConfig().coverage.satellites_for_full_coverage
    assert cellular.binding_regime.value == "coverage"
    assert cellular.subscribers_per_satellite == CommsConfig().subscribers.subscribers_per_satellite


def test_capacity_base_builds_beyond_the_coverage_floor() -> None:
    """A large subscriber base sizes the fleet above the coverage floor (capacity binds).

    With the 50M target the fleet target is 667 satellites (capacity-bound, above the
    340 coverage floor), so the treadmill builds toward 667 and the living fleet runs
    past the coverage floor. Coverage saturates at 1.0 well before full deployment.
    """
    config = CommsConfig(subscribers=SubscriberDials(subscribers_at_full_coverage=50_000_000))
    run = run_comms_model(config)
    coverage_floor = config.coverage.satellites_for_full_coverage
    assert run.cellular.fleet_target == 667
    assert run.cellular.binding_regime.value == "capacity"
    # The build pushes the living fleet past the coverage floor (it is sizing capacity).
    assert max(y.living_fleet for y in run.fleet.years) > coverage_floor
    # Coverage saturates at 1.0 once the floor is met, before full deployment.
    assert run.fleet.years[-1].coverage_fraction == pytest.approx(1.0)
    assert run.cellular.years[-1].buildout_fraction <= 1.0


def test_final_year_cash_per_subscriber_is_over_the_served_base() -> None:
    """The final-year cash per subscriber divides the final-year replacement by the served base.

    Objective: the cash per-person figure uses the served base (the same base the
    annualized per-person figure uses), not the configured target. Expected: on the
    default run it equals the final-year replacement (USD) over
    ``subscribers_served``; with a served override of half the target it doubles
    (the fleet, and so the replacement cash, is unchanged).
    """
    config = CommsConfig()
    run = run_comms_model(config)
    assert run.fleet.final_year_replacement_cost_musd is not None
    expected = (
        run.fleet.final_year_replacement_cost_musd * MUSD_TO_USD / run.cellular.subscribers_served
    )
    assert run.cellular.final_year_cash_cost_per_subscriber_usd == pytest.approx(
        expected, rel=COST_SUM_REL_TOL
    )
    half_base = config.subscribers.subscribers_at_full_coverage // 2
    overridden = run_comms_model(
        CommsConfig(subscribers=SubscriberDials(subscribers_served_override=half_base))
    )
    assert overridden.cellular.subscribers_served == half_base
    assert (
        overridden.fleet.final_year_replacement_cost_musd
        == run.fleet.final_year_replacement_cost_musd
    )
    assert overridden.cellular.final_year_cash_cost_per_subscriber_usd == pytest.approx(
        2.0 * expected, rel=COST_SUM_REL_TOL
    )


def test_comms_share_matches_shared_half_up_rounding() -> None:
    """The comms flown count tracks round_half_up(fleet * share) outside the cap.

    With share == 1.0 and a target so high the build-out never caps, the comms
    launches flown equal the whole-fleet cadence exactly (round_half_up of an
    integer is the integer), confirming the cadence-share seam reuses the shared
    half-up offset rather than re-deriving it.
    """
    never_capped_target = 100_000
    config = CommsConfig(
        cadence=CadenceDials(
            first_launch_year=0,
            launches_at_year_5=14,
            launches_at_year_10=90,
            cadence_ceiling=150,
        ),
        comms_cadence=CommsCadenceDials(share_of_fleet=1.0),
        coverage=CoverageDials(
            satellites_for_full_coverage=never_capped_target,
            max_fleet_satellites=never_capped_target,
        ),
        subscribers=_FLOOR_BINDING_SUBSCRIBERS,
    )
    run = run_comms_model(config)
    for year in run.fleet.years:
        expected = math.floor(year.fleet_launches_this_year * 1.0 + ROUND_TO_NEAREST_OFFSET)
        assert year.comms_launches_flown_this_year == expected


def test_comms_share_exact_half_rounds_up() -> None:
    """An exact half of a launch rounds UP, despite binary representation error.

    Objective: the launch-share rounding tolerance. A 0.35 share of the 90-launch
    FY2036 whole-fleet cadence is exactly 31.5 launches, but the float product is
    31.499999999999996, which plain half-up rounding sends to 31. Expected: with the
    build never capped (a 100,000-satellite floor and cap), FY2036 flies 32 comms
    launches.
    """
    never_capped_target = 100_000
    share = 0.35
    expected_fy2036_launches = 32  # round_half_up(0.35 x 90 = 31.5).
    config = CommsConfig(
        comms_cadence=CommsCadenceDials(share_of_fleet=share),
        coverage=CoverageDials(
            satellites_for_full_coverage=never_capped_target,
            max_fleet_satellites=never_capped_target,
        ),
        subscribers=_FLOOR_BINDING_SUBSCRIBERS,
    )
    run = run_comms_model(config)
    final = run.fleet.years[-1]
    # The default window's final year is the year-10 cadence anchor (FY2036), where
    # the whole-fleet ramp flies exactly the year-10 dial (90 launches).
    assert final.year == config.metadata.base_year + config.metadata.horizon_years
    assert final.fleet_launches_this_year == config.cadence.launches_at_year_10
    assert (
        final.fleet_launches_this_year * share < expected_fy2036_launches - ROUND_TO_NEAREST_OFFSET
    )
    assert final.comms_launches_flown_this_year == expected_fy2036_launches


# -- the revenue + gross-margin overlay (the two cases, per cohort + fleet) --


def test_cost_plus_revenue_is_annual_cost_times_multiple() -> None:
    """Each year: cost-plus revenue == annualized fleet cost x the revenue multiple."""
    config = CommsConfig()
    multiple = config.revenue.revenue_multiple
    run = run_comms_model(config)
    for fleet_year, year in zip(run.fleet.years, run.cellular.years, strict=True):
        assert year.cost_plus_revenue_this_year_musd == pytest.approx(
            fleet_year.annual_cost_this_year_musd * multiple, rel=COST_SUM_REL_TOL
        )


def test_cost_plus_margin_is_the_multiples_implied_margin() -> None:
    """The cost-plus margin is the flat ``(multiple - 1) / multiple`` once a fleet exists.

    Before any satellite is on orbit the revenue is zero and the margin reports 0.0;
    from the first living satellite on, every year carries the multiple's implied
    margin (33.3% at the 1.5 default), the same flat margin the DC central R earns.
    """
    config = CommsConfig()
    multiple = config.revenue.revenue_multiple
    expected_margin_pct = (multiple - 1.0) / multiple * MARGIN_PERCENT_SCALE
    run = run_comms_model(config)
    for fleet_year, year in zip(run.fleet.years, run.cellular.years, strict=True):
        if fleet_year.annual_cost_this_year_musd > 0.0:
            assert year.cost_plus_gross_margin_pct == pytest.approx(
                expected_margin_pct, rel=COST_SUM_REL_TOL
            )
        else:
            assert year.cost_plus_gross_margin_pct == 0.0


def test_arpu_revenue_is_served_base_times_arpu_annualized() -> None:
    """Each year: ARPU revenue == served subscribers x monthly ARPU x 12, in $M."""
    config = CommsConfig()
    arpu = config.revenue.arpu_usd_per_month
    run = run_comms_model(config)
    for year in run.cellular.years:
        expected_musd = year.subscribers_served_this_year * arpu * MONTHS_PER_YEAR / MUSD_TO_USD
        assert year.arpu_revenue_this_year_musd == pytest.approx(
            expected_musd, rel=COST_SUM_REL_TOL
        )


def test_gross_margin_is_revenue_minus_cost_over_revenue() -> None:
    """Both margins follow ``(revenue - cost) / revenue x 100`` against the annual cost."""
    config = CommsConfig()
    run = run_comms_model(config)
    for fleet_year, year in zip(run.fleet.years, run.cellular.years, strict=True):
        cost = fleet_year.annual_cost_this_year_musd
        for revenue, margin in (
            (year.cost_plus_revenue_this_year_musd, year.cost_plus_gross_margin_pct),
            (year.arpu_revenue_this_year_musd, year.arpu_gross_margin_pct),
        ):
            if revenue > 0.0:
                expected = (revenue - cost) / revenue * MARGIN_PERCENT_SCALE
                assert margin == pytest.approx(expected, rel=COST_SUM_REL_TOL)
            else:
                assert margin == 0.0


def test_subscribers_served_this_year_scales_with_buildout() -> None:
    """The per-year served count is the subscriber target scaled by the buildout fraction."""
    config = CommsConfig()
    target = config.subscribers.subscribers_at_full_coverage
    cellular = run_comms_model(config).cellular
    for year in cellular.years:
        assert year.subscribers_served_this_year == round(year.buildout_fraction * target)
    # The final year's per-year served count is the trajectory headline subscribers_served.
    assert cellular.years[-1].subscribers_served_this_year == cellular.subscribers_served


def test_annual_cost_basis_is_sum_of_living_cohort_annualized_cost() -> None:
    """The annualized fleet cost equals the sum of the per-cohort annualized cost lines."""
    run = run_comms_model(CommsConfig())
    for year in run.fleet.years:
        cohort_cost = sum(line.annual_cost_musd for line in year.cohort_costs)
        assert year.annual_cost_this_year_musd == pytest.approx(cohort_cost, rel=COST_SUM_REL_TOL)


def test_cohort_revenue_sums_to_the_year_revenue_both_cases() -> None:
    """Per-cohort revenues (both cases) sum to the fleet revenue line every year."""
    run = run_comms_model(CommsConfig())
    for year in run.cellular.years:
        cost_plus = sum(line.cost_plus_revenue_musd for line in year.cohort_revenue)
        arpu = sum(line.arpu_revenue_musd for line in year.cohort_revenue)
        assert cost_plus == pytest.approx(
            year.cost_plus_revenue_this_year_musd, rel=COST_SUM_REL_TOL
        )
        assert arpu == pytest.approx(year.arpu_revenue_this_year_musd, rel=COST_SUM_REL_TOL)


def test_cohort_arpu_subscribers_sum_to_year_served_exactly() -> None:
    """The per-cohort allocated subscribers sum EXACTLY to the year's served count.

    The last living cohort absorbs the rounding remainder, so the integer parts sum
    with no drift versus the fleet-level served base.
    """
    run = run_comms_model(CommsConfig())
    for year in run.cellular.years:
        allocated = sum(line.arpu_subscribers_served for line in year.cohort_revenue)
        assert allocated == year.subscribers_served_this_year


def test_cohort_costs_track_living_cohorts_under_the_cliff() -> None:
    """Each year's cohort lines are exactly the cohorts alive under the 5-year cliff.

    The cohort lines carry one entry per living cohort, and their living-satellite
    counts sum to the year's living fleet (the same cliff the cost treadmill uses).
    """
    config = CommsConfig()
    life = config.satellite.satellite_lifetime_years
    run = run_comms_model(config)
    for year in run.fleet.years:
        # Every cohort line is within the cliff window of this year.
        for line in year.cohort_costs:
            assert line.launch_year <= year.year < line.launch_year + life
            assert line.living_satellites > 0
        # The living-satellite counts sum to the year's living fleet.
        assert sum(line.living_satellites for line in year.cohort_costs) == year.living_fleet


def test_cohort_cost_plus_margin_is_flat_across_cohorts() -> None:
    """Every living cohort earns the same flat cost-plus margin (cost-coupled revenue)."""
    config = CommsConfig()
    multiple = config.revenue.revenue_multiple
    expected_margin_pct = (multiple - 1.0) / multiple * MARGIN_PERCENT_SCALE
    run = run_comms_model(config)
    for year in run.cellular.years:
        for line in year.cohort_revenue:
            assert line.cost_plus_gross_margin_pct == pytest.approx(
                expected_margin_pct, rel=COST_SUM_REL_TOL
            )


def test_steady_state_revenue_headlines_are_final_year_lines() -> None:
    """The trajectory steady-state revenue/margin headlines equal the final year's lines."""
    run = run_comms_model(CommsConfig())
    cellular = run.cellular
    final = cellular.years[-1]
    assert run.fleet.final_year_annual_cost_musd == pytest.approx(
        run.fleet.years[-1].annual_cost_this_year_musd
    )
    assert cellular.steady_state_revenue_cost_plus_musd == pytest.approx(
        final.cost_plus_revenue_this_year_musd
    )
    assert cellular.steady_state_gross_margin_cost_plus_pct == pytest.approx(
        final.cost_plus_gross_margin_pct
    )
    assert cellular.steady_state_revenue_arpu_musd == pytest.approx(
        final.arpu_revenue_this_year_musd
    )
    assert cellular.steady_state_gross_margin_arpu_pct == pytest.approx(final.arpu_gross_margin_pct)


def test_higher_arpu_lifts_arpu_revenue_and_margin() -> None:
    """Doubling the ARPU dial doubles the ARPU revenue and raises its margin.

    The cost-plus case is unchanged by the ARPU dial (revenue is cost-coupled), so the
    two cases are independent lenses, as designed.
    """
    base = run_comms_model(CommsConfig()).cellular
    higher = run_comms_model(CommsConfig(revenue=RevenueDials(arpu_usd_per_month=100.0))).cellular
    # ARPU revenue doubles (50 -> 100); the served base and cost are unchanged.
    assert higher.steady_state_revenue_arpu_musd == pytest.approx(
        2.0 * base.steady_state_revenue_arpu_musd, rel=COST_SUM_REL_TOL
    )
    assert higher.steady_state_gross_margin_arpu_pct > base.steady_state_gross_margin_arpu_pct
    # The cost-plus case is untouched by the ARPU dial.
    assert higher.steady_state_revenue_cost_plus_musd == pytest.approx(
        base.steady_state_revenue_cost_plus_musd, rel=COST_SUM_REL_TOL
    )


# -- the shared fleet-and-cost loop under a deployment rule (run_fleet_loop) --


def _fly_every_launch(step: DeploymentStep) -> Deployment:
    """A family-neutral test rule: fly every launch the cadence share allows, and count as
    replacement only the part that matches the year's retirements."""
    added = step.launches_allowed * step.satellites_per_launch
    return Deployment(
        satellites_added=added, satellites_replaced=min(added, step.retiring_this_year)
    )


def _adds_part_of_a_launch(step: DeploymentStep) -> Deployment:
    """Adds one satellite short of the allowance once any launch is allowed."""
    added = max(0, step.launches_allowed * step.satellites_per_launch - 1)
    return Deployment(satellites_added=added, satellites_replaced=0)


def _adds_a_negative_count(step: DeploymentStep) -> Deployment:
    """Adds minus one launch's worth (a multiple of the launch, but not a count)."""
    return Deployment(satellites_added=-step.satellites_per_launch, satellites_replaced=0)


def _adds_a_float_count(step: DeploymentStep) -> Deployment:
    """Adds the allowance as a float, against the type (a count is an integer)."""
    added = float(step.launches_allowed * step.satellites_per_launch)
    return Deployment(satellites_added=added, satellites_replaced=0)


def _adds_beyond_the_cadence(step: DeploymentStep) -> Deployment:
    """Adds one whole launch more than the cadence share allows."""
    added = (step.launches_allowed + 1) * step.satellites_per_launch
    return Deployment(satellites_added=added, satellites_replaced=0)


def _replaces_part_of_a_launch(step: DeploymentStep) -> Deployment:
    """Adds the allowance and counts one satellite of it as replacement."""
    added = step.launches_allowed * step.satellites_per_launch
    return Deployment(satellites_added=added, satellites_replaced=1)


def _replaces_more_than_it_adds(step: DeploymentStep) -> Deployment:
    """Adds the allowance and counts one launch more than it as replacement."""
    added = step.launches_allowed * step.satellites_per_launch
    return Deployment(
        satellites_added=added, satellites_replaced=added + step.satellites_per_launch
    )


@pytest.mark.parametrize(
    ("rule", "broken"),
    [
        pytest.param(
            _adds_part_of_a_launch,
            r"in 20[0-9]{2} does not add whole launches: satellites added \d+, ",
            id="part_of_a_launch",
        ),
        pytest.param(
            _adds_a_negative_count,
            "in 2026 does not add whole launches: satellites added -12, ",
            id="negative",
        ),
        pytest.param(
            _adds_a_float_count,
            r"in 2026 does not add whole launches: satellites added 0\.0, ",
            id="float",
        ),
        pytest.param(
            _adds_beyond_the_cadence,
            r"in 2026 adds more than the cadence share allows: satellites added 12, at most 0 \(",
            id="beyond_the_cadence",
        ),
        pytest.param(
            _replaces_part_of_a_launch,
            "in 2026 does not replace whole launches: satellites replaced 1, ",
            id="replaces_part_of_a_launch",
        ),
        pytest.param(
            _replaces_more_than_it_adds,
            "in 2026 replaces more than it adds: satellites replaced 12, satellites added 0",
            id="replaces_more_than_it_adds",
        ),
    ],
)
def test_the_loop_refuses_an_impossible_deployment(
    rule: Callable[[DeploymentStep], Deployment], broken: str
) -> None:
    """The loop checks every deployment its rule returns.

    Objective: a deployment adds whole launches (a count of zero or more, a multiple of the
    satellites a launch carries), at most the launches the cadence share allows, and counts
    whole launches of that addition, at most all of it, as replacement; the loop refuses
    anything else with a typed error (a ValueError, so the promotion command reports it as
    one ERROR line) naming the year and the broken condition.

    Sample: the config defaults (12 per launch; FY2026 allows no comms launch) under six
    rules, each wrong in one way: part of a launch, a negative count, a float count, a launch
    beyond the cadence, a replacement of part of a launch, and more replacement than addition.

    Expected: each raises DeploymentRuleError naming the year and the condition it breaks
    (the five that are wrong from the first year name FY2026).
    """
    config = CommsConfig()
    with pytest.raises(DeploymentRuleError, match=broken) as refused:
        run_fleet_loop(config, rule, satellites_per_launch=config.satellite.satellites_per_launch)
    assert isinstance(refused.value, ValueError)


class BreakYear(StrEnum):
    """The year a test rule turns wrong in: the first year the cadence share allows a launch,
    or the horizon's final year (both with launches allowed, so the bounds are above zero)."""

    FIRST_WITH_LAUNCHES = "first_with_launches"
    FINAL = "final"


def _steps_of(config: CommsConfig) -> list[DeploymentStep]:
    """The steps the loop hands a rule that deploys nothing, one per model year."""
    seen: list[DeploymentStep] = []

    def deploys_nothing(step: DeploymentStep) -> Deployment:
        seen.append(step)
        return Deployment(satellites_added=0, satellites_replaced=0)

    run_fleet_loop(
        config, deploys_nothing, satellites_per_launch=config.satellite.satellites_per_launch
    )
    return seen


def _break_year(config: CommsConfig, when: BreakYear) -> int:
    """The model year a test rule turns wrong in."""
    match when:
        case BreakYear.FIRST_WITH_LAUNCHES:
            return next(step.year for step in _steps_of(config) if step.launches_allowed > 0)
        case BreakYear.FINAL:
            return config.metadata.base_year + config.metadata.horizon_years
        case _:
            assert_never(when)


def _wrong_from(
    year: int, wrong: Callable[[DeploymentStep], Deployment]
) -> Callable[[DeploymentStep], Deployment]:
    """A rule that flies every allowed launch before ``year`` and is ``wrong`` from it on."""

    def rule(step: DeploymentStep) -> Deployment:
        return _fly_every_launch(step) if step.year < year else wrong(step)

    return rule


def _adds_a_bool(step: DeploymentStep) -> Deployment:
    """Adds ``True`` (a bool is not a count, though it passes a multiple test at one)."""
    return Deployment(satellites_added=True, satellites_replaced=0)


def _replaces_a_bool(step: DeploymentStep) -> Deployment:
    """Adds one satellite and counts ``True`` of it as replacement."""
    return Deployment(satellites_added=1, satellites_replaced=True)


@pytest.mark.parametrize(
    ("satellites_per_launch", "when", "wrong", "condition"),
    [
        pytest.param(
            12,
            BreakYear.FIRST_WITH_LAUNCHES,
            _adds_beyond_the_cadence,
            "adds more than the cadence share allows",
            id="beyond the cadence, first year with launches",
        ),
        pytest.param(
            12,
            BreakYear.FINAL,
            _adds_beyond_the_cadence,
            "adds more than the cadence share allows",
            id="beyond the cadence, final year",
        ),
        pytest.param(
            12,
            BreakYear.FIRST_WITH_LAUNCHES,
            _replaces_more_than_it_adds,
            "replaces more than it adds",
            id="more replaced than added, a nonzero addition",
        ),
        pytest.param(
            1,
            BreakYear.FIRST_WITH_LAUNCHES,
            _adds_a_bool,
            "does not add whole launches",
            id="a bool addition at one per launch",
        ),
        pytest.param(
            1,
            BreakYear.FIRST_WITH_LAUNCHES,
            _replaces_a_bool,
            "does not replace whole launches",
            id="a bool replacement at one per launch",
        ),
    ],
)
def test_the_loop_refuses_an_impossible_deployment_where_launches_are_allowed(
    satellites_per_launch: int,
    when: BreakYear,
    wrong: Callable[[DeploymentStep], Deployment],
    condition: str,
) -> None:
    """The rule check holds where its bounds are above zero, and refuses a bool count.

    Objective: the refusals above break in FY2026, where the default share allows no launch, so
    their bounds are 0; these break where launches are allowed (the first such year and the
    final year), and at one satellite per launch, where a bool would pass a multiple test.

    Sample: the config defaults (or one satellite per launch) under a rule that flies every
    allowed launch before the break year and is wrong in one way from it on.

    Expected: DeploymentRuleError (a ValueError) naming the break year and the condition.
    """
    config = CommsConfig(satellite=SatelliteDials(satellites_per_launch=satellites_per_launch))
    year = _break_year(config, when)
    assert next(s.launches_allowed for s in _steps_of(config) if s.year == year) > 0
    with pytest.raises(DeploymentRuleError, match=f"in {year} {condition}") as refused:
        run_fleet_loop(
            config, _wrong_from(year, wrong), satellites_per_launch=satellites_per_launch
        )
    assert isinstance(refused.value, ValueError)


@pytest.mark.parametrize(
    ("satellites_per_launch", "shown"),
    [(0, "0"), (12.0, "12.0"), (True, "True")],
    ids=["no satellite", "a float", "a bool"],
)
def test_the_loop_refuses_a_count_per_launch_that_is_not_whole(
    satellites_per_launch: int, shown: str
) -> None:
    """The loop deploys whole launches, so a launch carries a whole number of satellites.

    Objective: the loop refuses its own count per launch when it is not an integer of at least
    one (a bool or a float is not one), naming the argument, rather than running a bool as one
    per launch or blaming the rule for a float.

    Sample: the config defaults with 0, 12.0 and True satellites per launch.

    Expected: a ValueError naming the bound and the count given, before any year runs.
    """
    with pytest.raises(
        ValueError, match=rf"satellites_per_launch must be an integer of at least 1; got {shown}$"
    ):
        run_fleet_loop(
            CommsConfig(), _fly_every_launch, satellites_per_launch=satellites_per_launch
        )


def test_an_empty_year_carries_a_float_annualized_cost() -> None:
    """The shared record's types hold in a year with no living cohort.

    Objective: ``FleetYear.annual_cost_this_year_musd`` and
    ``FleetTrajectory.final_year_annual_cost_musd`` are floats as declared, 0.0 where no cohort
    is alive (the sum of no cohort lines starts from ``NO_ANNUAL_COST_MUSD``), never the int 0.

    Sample: the config defaults' first years (no comms launch before the share allows one), and
    a one-year horizon at the default share (no comms launch at all).

    Expected: every empty year's annualized cost, and the empty final year's, is the float 0.0.
    """
    per_launch = CommsConfig().satellite.satellites_per_launch
    target = CommsConfig().coverage.satellites_for_full_coverage
    fleet = run_fleet_loop(CommsConfig(), cellular_rule(target), satellites_per_launch=per_launch)
    empty = [year for year in fleet.years if not year.cohort_costs]
    assert empty
    assert {type(year.annual_cost_this_year_musd) for year in empty} == {float}
    short = run_fleet_loop(
        CommsConfig(metadata=CommsMetadataDials(base_year=2026, horizon_years=1)),
        cellular_rule(target),
        satellites_per_launch=per_launch,
    )
    assert not short.years[-1].cohort_costs
    assert type(short.final_year_annual_cost_musd) is float
    assert short.final_year_annual_cost_musd == 0.0


def test_the_cohort_cost_lines_are_each_living_cohort_at_its_locked_cost() -> None:
    """The shared record's cohort cost lines: each living cohort at the cost locked at launch.

    Objective: the per-cohort lock-in. A cohort's per-satellite annual cost is fixed at its
    launch year's launch price, so a later year's cadence cost-down never reprices it, and
    the annualized fleet cost is the sum of the living cohorts' lines.

    Sample: the config defaults (a launch price that falls as the whole-fleet cadence
    ramps) under a test rule that flies every launch the cadence share allows, so cohorts
    launched at different prices live side by side.

    Expected: every year, one line per living cohort, oldest first, each within the 5-year
    cliff and holding every satellite its launch year deployed; each line's cost is its
    satellites times the per-satellite cost at its launch year's price, exactly; the lines'
    satellites sum to the living fleet and their costs to the annualized fleet cost; some year
    carries cohorts locked at two prices (so a line priced at the current year's launch price
    would fail here); and the replacement split under this family-neutral rule, the one the
    Iridium family's full-cadence rule reads: each year replaces the lesser of its deployment
    and the deployment one life earlier (the step's retirements), its replacement line those
    satellites at the build cost plus their launches at the year's price, and some year replaces
    satellites.
    """
    config = CommsConfig()
    per_launch = config.satellite.satellites_per_launch
    life = config.satellite.satellite_lifetime_years
    fleet = run_fleet_loop(config, _fly_every_launch, satellites_per_launch=per_launch)
    by_year = {year.year: year for year in fleet.years}
    saw_two_prices = False
    saw_a_replacement = False
    for year in fleet.years:
        launch_years = [line.launch_year for line in year.cohort_costs]
        assert launch_years == sorted(set(launch_years))
        for line in year.cohort_costs:
            assert line.launch_year <= year.year < line.launch_year + life
            launched = by_year[line.launch_year]
            assert line.living_satellites == launched.satellites_deployed_this_year
            assert line.living_satellites > 0
            locked_cost_per_satellite = per_satellite_annual_cost_musd(
                satellite_build_cost_musd=config.satellite.satellite_build_cost_musd,
                launch_cost_per_launch_musd=launched.launch_cost_per_launch_musd,
                satellites_per_launch=per_launch,
                satellite_lifetime_years=life,
            )
            assert line.annual_cost_musd == line.living_satellites * locked_cost_per_satellite
        assert sum(line.living_satellites for line in year.cohort_costs) == year.living_fleet
        assert year.annual_cost_this_year_musd == pytest.approx(
            sum(line.annual_cost_musd for line in year.cohort_costs), rel=COST_SUM_REL_TOL
        )
        launch_prices = {
            by_year[line.launch_year].launch_cost_per_launch_musd for line in year.cohort_costs
        }
        saw_two_prices = saw_two_prices or len(launch_prices) > 1
        retiring = (
            by_year[year.year - life].satellites_deployed_this_year
            if year.year - life in by_year
            else 0
        )
        replaced = min(year.satellites_deployed_this_year, retiring)
        assert year.satellites_replaced_this_year == replaced
        assert year.replacement_cost_this_year_musd == pytest.approx(
            replaced * config.satellite.satellite_build_cost_musd
            + replaced // per_launch * year.launch_cost_per_launch_musd,
            rel=COST_SUM_REL_TOL,
        )
        saw_a_replacement = saw_a_replacement or replaced > 0
    assert saw_two_prices
    assert saw_a_replacement


def test_margin_is_none_where_revenue_is_not_positive() -> None:
    """The one margin function is undefined without revenue.

    Objective: ``margin_pct`` returns None where revenue is not positive, never a number
    published as if it were a margin; the cellular record shows its published 0.0 there (the
    cost-plus margin tests and the margin-formula test above).

    Sample: revenue 0.0 and -1.0 against a 1.0 cost; revenue 4.0 against 1.0.

    Expected: None, None, and 75.0 percent.
    """
    assert margin_pct(0.0, 1.0) is None
    assert margin_pct(-1.0, 1.0) is None
    assert margin_pct(4.0, 1.0) == pytest.approx(75.0)


def test_a_rule_keeps_no_state_between_runs() -> None:
    """A rule reads only its step, so the loop run twice with one rule gives one record.

    Objective: a deployment rule keeps no state between calls. The cellular rule is the one
    that reads the years already computed (its hold), so it is the one a remembered
    "target reached" flag would break.

    Sample: the config defaults' fleet target (340, the coverage floor binding the 10M base),
    one ``cellular_rule`` object, the loop run twice with it.

    Expected: the two shared records are equal, every year and cohort line included. The run
    reaches the target (in FY2035) with build years before it that replace less than they add,
    so a rule that remembered reaching the target would count the second run's build as
    replacement and fail here.
    """
    config = CommsConfig()
    per_launch = config.satellite.satellites_per_launch
    fleet_target, _ = compute_fleet_target(
        subscriber_target=config.subscribers.subscribers_at_full_coverage,
        subscribers_per_satellite=config.subscribers.subscribers_per_satellite,
        coverage_floor=config.coverage.satellites_for_full_coverage,
        max_fleet_satellites=config.coverage.max_fleet_satellites,
    )
    rule = cellular_rule(fleet_target)
    first = run_fleet_loop(config, rule, satellites_per_launch=per_launch)
    second = run_fleet_loop(config, rule, satellites_per_launch=per_launch)
    assert first == second
    reached = first_year_at_target(first.years, fleet_target)
    assert reached is not None
    assert any(
        year.year <= reached
        and year.satellites_replaced_this_year < year.satellites_deployed_this_year
        for year in first.years
    )
