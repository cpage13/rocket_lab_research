"""Phase 2 tests for the comms CELLULAR engine (the cohort treadmill).

These cover the engine's contract from the plan's Phase 2 test list: the
trajectory length, the build-and-hold cap (living fleet non-decreasing during
build-out and bounded by one launch's overshoot), the satellites-per-launch
identity, the build-out monotonicity of the comms launch sequence and the
whole-fleet cadence, the cumulative-cost identity, the low-target sanity case
(immediate HOLD), and the 5-year cliff bite. They use the real shared cadence /
cohort spine (no mocks), so they also act as an integration check on the
``common.*`` seam.

The golden cost-per-subscriber parity trajectory is frozen separately in
``test_parity.py`` (Phase 7); this file checks the engine's structural and
counting invariants, which are exact integers (no float tolerance needed except
where a cost sum is compared, where a tight relative tolerance is used).
"""

from __future__ import annotations

import math

import pytest

from common.cadence import ROUND_TO_NEAREST_OFFSET
from communications.config import (
    CadenceDials,
    CommsCadenceDials,
    CommsConfig,
    CoverageDials,
)
from communications.engine import CommsTrajectory, run_comms_model

# The default-config horizon is 10 years after the base year, so the trajectory
# spans FY2026..FY2036 inclusive (11 model years).
EXPECTED_DEFAULT_YEAR_COUNT = 11

# A tight relative tolerance for the one cost-sum identity check (floats sum in a
# different association order than the engine's running accumulation).
COST_SUM_REL_TOL = 1e-9


def test_run_returns_trajectory_with_full_horizon() -> None:
    """The default run returns a CommsTrajectory spanning FY2026..FY2036 (11 years)."""
    traj = run_comms_model(CommsConfig())
    assert isinstance(traj, CommsTrajectory)
    assert len(traj.years) == EXPECTED_DEFAULT_YEAR_COUNT
    assert traj.years[0].year == 2026
    assert traj.years[-1].year == 2036


def test_satellites_deployed_equals_launches_times_per_launch() -> None:
    """Every year: satellites_deployed == comms_launches_flown * satellites_per_launch."""
    config = CommsConfig()
    per_launch = config.satellite.satellites_per_launch
    traj = run_comms_model(config)
    for year in traj.years:
        assert year.satellites_deployed_this_year == (
            year.comms_launches_flown_this_year * per_launch
        )


def test_living_fleet_non_decreasing_during_build_out() -> None:
    """The living fleet never shrinks while the build-out is still filling the target.

    During build-out (before the target is first reached) the treadmill only adds
    satellites, so the living count is non-decreasing year over year.
    """
    traj = run_comms_model(CommsConfig())
    build_out_years = [y for y in traj.years if not y.is_hold_phase]
    for earlier, later in zip(build_out_years, build_out_years[1:], strict=False):
        assert later.living_fleet >= earlier.living_fleet


def test_living_fleet_never_exceeds_target_by_more_than_one_launch() -> None:
    """The living fleet overshoots the target by strictly less than one launch's worth.

    The overshoot rule rounds the final build cohort up to a whole launch, so the
    living count can sit above the target but by less than ``satellites_per_launch``.
    """
    config = CommsConfig()
    target = config.coverage.satellites_for_full_coverage
    per_launch = config.satellite.satellites_per_launch
    traj = run_comms_model(config)
    for year in traj.years:
        assert year.living_fleet < target + per_launch


def test_comms_launch_sequence_non_decreasing_during_build_out() -> None:
    """The comms launches flown are non-decreasing during build-out.

    This is the cadence-monotonicity the Phase 5 invariant enforces. NOTE: during
    HOLD the flown count can DROP (only the cliff losses are replaced), so the
    strict monotonicity is asserted on the build-out phase only. The whole-fleet
    cadence is checked separately (it is always non-decreasing).
    """
    traj = run_comms_model(CommsConfig())
    build_out_years = [y for y in traj.years if not y.is_hold_phase]
    for earlier, later in zip(build_out_years, build_out_years[1:], strict=False):
        assert later.comms_launches_flown_this_year >= earlier.comms_launches_flown_this_year


def test_fleet_cadence_non_decreasing_every_year() -> None:
    """The whole-fleet cadence (the cost-pricing series) is non-decreasing every year.

    Unlike the comms flown count, the whole-fleet cadence is the raw shared
    logistic ramp and is monotonic across the whole horizon, build-out and HOLD
    alike. The launch cost is priced at this series, so its non-increasing cost
    behaviour (the Phase 5 invariant) rests on this monotonicity.
    """
    traj = run_comms_model(CommsConfig())
    for earlier, later in zip(traj.years, traj.years[1:], strict=False):
        assert later.fleet_launches_this_year >= earlier.fleet_launches_this_year


def test_launch_cost_per_launch_non_increasing_with_cadence() -> None:
    """The per-launch cost is non-increasing as the fleet cadence ramps (the cost-down)."""
    traj = run_comms_model(CommsConfig())
    for earlier, later in zip(traj.years, traj.years[1:], strict=False):
        assert later.launch_cost_per_launch_musd <= earlier.launch_cost_per_launch_musd + 0.0


def test_total_cost_is_sum_of_year_costs() -> None:
    """total_build_and_hold_cost_musd equals the sum of the per-year total costs."""
    traj = run_comms_model(CommsConfig())
    expected = sum(y.total_cost_this_year_musd for y in traj.years)
    assert traj.total_build_and_hold_cost_musd == pytest.approx(expected, rel=COST_SUM_REL_TOL)


def test_per_year_total_cost_is_build_plus_launch() -> None:
    """Each year's total cost is exactly its build cost plus its launch cost."""
    traj = run_comms_model(CommsConfig())
    for year in traj.years:
        assert year.total_cost_this_year_musd == pytest.approx(
            year.build_cost_this_year_musd + year.launch_cost_this_year_musd,
            rel=COST_SUM_REL_TOL,
        )


def test_build_cost_uses_the_configured_build_cost_scalar() -> None:
    """Each year's build cost equals satellites_deployed * satellite_build_cost_musd."""
    config = CommsConfig()
    build_cost = config.satellite.satellite_build_cost_musd
    traj = run_comms_model(config)
    for year in traj.years:
        assert year.build_cost_this_year_musd == pytest.approx(
            year.satellites_deployed_this_year * build_cost, rel=COST_SUM_REL_TOL
        )


def test_replacement_line_zero_during_build_out_nonzero_in_hold() -> None:
    """The replacement line is 0.0 during build-out and equals the year cost in HOLD."""
    traj = run_comms_model(CommsConfig())
    for year in traj.years:
        if year.is_hold_phase:
            assert year.replacement_cost_this_year_musd == pytest.approx(
                year.total_cost_this_year_musd, rel=COST_SUM_REL_TOL
            )
        else:
            assert year.replacement_cost_this_year_musd == 0.0


def test_coverage_fraction_is_living_over_target_clamped() -> None:
    """coverage_fraction == min(1.0, living_fleet / target) every year."""
    config = CommsConfig()
    target = config.coverage.satellites_for_full_coverage
    traj = run_comms_model(config)
    for year in traj.years:
        assert year.coverage_fraction == pytest.approx(
            min(1.0, year.living_fleet / target), rel=COST_SUM_REL_TOL
        )
        assert 0.0 <= year.coverage_fraction <= 1.0


def test_full_coverage_reached_year_is_first_hold_year() -> None:
    """full_coverage_reached_year is the first fiscal year HOLD is entered (target hit)."""
    traj = run_comms_model(CommsConfig())
    hold_years = [y.year for y in traj.years if y.is_hold_phase]
    assert traj.full_coverage_reached_year == hold_years[0]


def test_steady_state_replacement_is_final_year_replacement_line() -> None:
    """The steady-state annual replacement cost is the final model year's replacement line."""
    traj = run_comms_model(CommsConfig())
    assert traj.steady_state_annual_replacement_cost_musd == pytest.approx(
        traj.years[-1].replacement_cost_this_year_musd, rel=COST_SUM_REL_TOL
    )


def test_low_target_enters_hold_immediately() -> None:
    """A one-launch-worth target is reached at the first comms launch, then HOLD holds.

    With ``satellites_for_full_coverage`` set to exactly one launch's worth, the
    target is reached the first year a comms launch flies; from that year on the
    model is in HOLD and the living fleet pins at the target (the sanity of the
    cap logic). The build-out phase before the first comms launch deploys nothing.
    """
    config = CommsConfig()
    per_launch = config.satellite.satellites_per_launch
    low_target_config = config.model_copy(
        update={"coverage": CoverageDials(satellites_for_full_coverage=per_launch)}
    )
    traj = run_comms_model(low_target_config)

    first_deploy_year = next(y for y in traj.years if y.satellites_deployed_this_year > 0)
    # The target is reached the moment the first comms launch flies.
    assert first_deploy_year.is_hold_phase is True
    assert first_deploy_year.living_fleet == per_launch
    assert traj.full_coverage_reached_year == first_deploy_year.year
    # From the reached year onward, every year is HOLD and the living fleet pins
    # at exactly one launch's worth (the target).
    for year in traj.years:
        if year.year >= first_deploy_year.year:
            assert year.is_hold_phase is True
            assert year.living_fleet == per_launch


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
        coverage=CoverageDials(satellites_for_full_coverage=never_capped_target),
    )
    traj = run_comms_model(config)
    by_year = {y.year: y for y in traj.years}

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
        coverage=CoverageDials(satellites_for_full_coverage=unreachable_target),
    )
    traj = run_comms_model(config)
    assert traj.full_coverage_reached_year is None
    assert len(traj.years) == EXPECTED_DEFAULT_YEAR_COUNT
    # No year reaches HOLD, so the steady-state replacement line is zero.
    assert all(not y.is_hold_phase for y in traj.years)
    assert traj.steady_state_annual_replacement_cost_musd == 0.0


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
        coverage=CoverageDials(satellites_for_full_coverage=never_capped_target),
    )
    traj = run_comms_model(config)
    for year in traj.years:
        expected = math.floor(year.fleet_launches_this_year * 1.0 + ROUND_TO_NEAREST_OFFSET)
        assert year.comms_launches_flown_this_year == expected
