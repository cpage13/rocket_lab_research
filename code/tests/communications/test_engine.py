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
    RevenueDials,
    SubscriberDials,
)
from communications.constants import MONTHS_PER_YEAR
from communications.engine import CommsTrajectory, run_comms_model

# The default-config horizon is 10 years after the base year, so the trajectory
# spans FY2026..FY2036 inclusive (11 model years).
EXPECTED_DEFAULT_YEAR_COUNT = 11

# A tight relative tolerance for the one cost-sum identity check (floats sum in a
# different association order than the engine's running accumulation).
COST_SUM_REL_TOL = 1e-9

# The $M -> USD conversion the engine uses for the ARPU revenue (ARPU is in USD/mo,
# revenue is reported in $M). Mirrors the engine's ``MUSD_TO_USD``.
MUSD_TO_USD = 1_000_000.0

# The percent scale for a gross margin (the engine's ``MARGIN_PERCENT_SCALE``).
MARGIN_PERCENT_SCALE = 100.0

# A tiny subscriber target whose capacity need (ceil(target / 75,000) == 1) is below
# any coverage floor these tests set, so the fleet target equals the coverage floor.
# This lets a test drive the build target directly via ``satellites_for_full_coverage``
# (the floor), isolating the treadmill / cliff mechanics from the capacity sizing.
FLOOR_BINDING_SUBSCRIBER_TARGET = 1
_FLOOR_BINDING_SUBSCRIBERS = SubscriberDials(
    subscribers_at_full_coverage=FLOOR_BINDING_SUBSCRIBER_TARGET
)


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
    """The living fleet overshoots the FLEET TARGET by strictly less than one launch's worth.

    The overshoot rule rounds the final build cohort up to a whole launch, so the
    living count can sit above the fleet target but by less than
    ``satellites_per_launch``. The fleet target is the capacity-sized fleet the
    treadmill builds toward (the default 10M base floors it at the coverage floor).
    """
    config = CommsConfig()
    per_launch = config.satellite.satellites_per_launch
    traj = run_comms_model(config)
    for year in traj.years:
        assert year.living_fleet < traj.fleet_target + per_launch


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


def test_coverage_fraction_is_living_over_floor_clamped() -> None:
    """coverage_fraction == min(1.0, living_fleet / coverage_floor) every year."""
    config = CommsConfig()
    coverage_floor = config.coverage.satellites_for_full_coverage
    traj = run_comms_model(config)
    for year in traj.years:
        assert year.coverage_fraction == pytest.approx(
            min(1.0, year.living_fleet / coverage_floor), rel=COST_SUM_REL_TOL
        )
        assert 0.0 <= year.coverage_fraction <= 1.0


def test_buildout_fraction_is_living_over_fleet_target_clamped() -> None:
    """buildout_fraction == min(1.0, living_fleet / fleet_target) every year."""
    config = CommsConfig()
    traj = run_comms_model(config)
    for year in traj.years:
        assert year.buildout_fraction == pytest.approx(
            min(1.0, year.living_fleet / traj.fleet_target), rel=COST_SUM_REL_TOL
        )
        assert 0.0 <= year.buildout_fraction <= 1.0


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
    # Drive the fleet target to one launch's worth via the coverage floor; the tiny
    # subscriber target keeps the capacity need below the floor so the floor binds.
    low_target_config = config.model_copy(
        update={
            "coverage": CoverageDials(satellites_for_full_coverage=per_launch),
            "subscribers": _FLOOR_BINDING_SUBSCRIBERS,
        }
    )
    traj = run_comms_model(low_target_config)
    assert traj.fleet_target == per_launch

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
        coverage=CoverageDials(
            satellites_for_full_coverage=never_capped_target,
            max_fleet_satellites=never_capped_target,
        ),
        subscribers=_FLOOR_BINDING_SUBSCRIBERS,
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
        # Floor the fleet at 100,000 and lift the saturation cap above it so the floor
        # (not the cap) is the fleet target; the tiny base keeps capacity below it.
        coverage=CoverageDials(
            satellites_for_full_coverage=unreachable_target,
            max_fleet_satellites=unreachable_target,
        ),
        subscribers=_FLOOR_BINDING_SUBSCRIBERS,
    )
    traj = run_comms_model(config)
    assert traj.fleet_target == unreachable_target
    assert traj.full_coverage_reached_year is None
    assert len(traj.years) == EXPECTED_DEFAULT_YEAR_COUNT
    # No year reaches HOLD, so the steady-state replacement line is zero.
    assert all(not y.is_hold_phase for y in traj.years)
    assert traj.steady_state_annual_replacement_cost_musd == 0.0


def test_trajectory_surfaces_fleet_target_and_regime() -> None:
    """The trajectory carries the capacity-sized fleet target and its binding regime."""
    traj = run_comms_model(CommsConfig())
    # The default 10M base floors the fleet at the coverage floor (340), coverage regime.
    assert traj.fleet_target == CommsConfig().coverage.satellites_for_full_coverage
    assert traj.binding_regime.value == "coverage"
    assert traj.subscribers_per_satellite == CommsConfig().subscribers.subscribers_per_satellite


def test_capacity_base_builds_beyond_the_coverage_floor() -> None:
    """A large subscriber base sizes the fleet above the coverage floor (capacity binds).

    With the 50M target the fleet target is 667 satellites (capacity-bound, above the
    340 coverage floor), so the treadmill builds toward 667 and the living fleet runs
    past the coverage floor. Coverage saturates at 1.0 well before full deployment.
    """
    config = CommsConfig(subscribers=SubscriberDials(subscribers_at_full_coverage=50_000_000))
    traj = run_comms_model(config)
    coverage_floor = config.coverage.satellites_for_full_coverage
    assert traj.fleet_target == 667
    assert traj.binding_regime.value == "capacity"
    # The build pushes the living fleet past the coverage floor (it is sizing capacity).
    assert max(y.living_fleet for y in traj.years) > coverage_floor
    # Coverage saturates at 1.0 once the floor is met, before full deployment.
    final = traj.years[-1]
    assert final.coverage_fraction == pytest.approx(1.0)
    assert final.buildout_fraction <= 1.0


def test_cost_per_subscriber_is_steady_state_over_target() -> None:
    """cost_per_subscriber_annual_usd == steady-state annual cost (USD) / subscriber target."""
    config = CommsConfig()
    traj = run_comms_model(config)
    target = config.subscribers.subscribers_at_full_coverage
    expected = traj.steady_state_annual_replacement_cost_musd * 1_000_000.0 / target
    assert traj.cost_per_subscriber_annual_usd == pytest.approx(expected, rel=COST_SUM_REL_TOL)


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
    traj = run_comms_model(config)
    for year in traj.years:
        expected = math.floor(year.fleet_launches_this_year * 1.0 + ROUND_TO_NEAREST_OFFSET)
        assert year.comms_launches_flown_this_year == expected


# -- the revenue + gross-margin overlay (the two cases, per cohort + fleet) --


def test_cost_plus_revenue_is_annual_cost_times_multiple() -> None:
    """Each year: cost-plus revenue == annualized fleet cost x the revenue multiple."""
    config = CommsConfig()
    multiple = config.revenue.revenue_multiple
    traj = run_comms_model(config)
    for year in traj.years:
        assert year.cost_plus_revenue_this_year_musd == pytest.approx(
            year.annual_cost_this_year_musd * multiple, rel=COST_SUM_REL_TOL
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
    traj = run_comms_model(config)
    for year in traj.years:
        if year.annual_cost_this_year_musd > 0.0:
            assert year.cost_plus_gross_margin_pct == pytest.approx(
                expected_margin_pct, rel=COST_SUM_REL_TOL
            )
        else:
            assert year.cost_plus_gross_margin_pct == 0.0


def test_arpu_revenue_is_served_base_times_arpu_annualized() -> None:
    """Each year: ARPU revenue == served subscribers x monthly ARPU x 12, in $M."""
    config = CommsConfig()
    arpu = config.revenue.arpu_usd_per_month
    traj = run_comms_model(config)
    for year in traj.years:
        expected_musd = year.subscribers_served_this_year * arpu * MONTHS_PER_YEAR / MUSD_TO_USD
        assert year.arpu_revenue_this_year_musd == pytest.approx(
            expected_musd, rel=COST_SUM_REL_TOL
        )


def test_gross_margin_is_revenue_minus_cost_over_revenue() -> None:
    """Both margins follow ``(revenue - cost) / revenue x 100`` against the annual cost."""
    config = CommsConfig()
    traj = run_comms_model(config)
    for year in traj.years:
        cost = year.annual_cost_this_year_musd
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
    traj = run_comms_model(config)
    for year in traj.years:
        assert year.subscribers_served_this_year == round(year.buildout_fraction * target)
    # The final year's per-year served count is the trajectory headline subscribers_served.
    assert traj.years[-1].subscribers_served_this_year == traj.subscribers_served


def test_annual_cost_basis_is_sum_of_living_cohort_annualized_cost() -> None:
    """The annualized fleet cost equals the sum of the per-cohort annualized cost lines."""
    traj = run_comms_model(CommsConfig())
    for year in traj.years:
        cohort_cost = sum(line.annual_cost_musd for line in year.cohort_lines)
        assert year.annual_cost_this_year_musd == pytest.approx(cohort_cost, rel=COST_SUM_REL_TOL)


def test_cohort_lines_sum_to_fleet_revenue_both_cases() -> None:
    """Per-cohort revenues (both cases) sum to the fleet revenue line every year."""
    traj = run_comms_model(CommsConfig())
    for year in traj.years:
        cost_plus = sum(line.cost_plus_revenue_musd for line in year.cohort_lines)
        arpu = sum(line.arpu_revenue_musd for line in year.cohort_lines)
        assert cost_plus == pytest.approx(
            year.cost_plus_revenue_this_year_musd, rel=COST_SUM_REL_TOL
        )
        assert arpu == pytest.approx(year.arpu_revenue_this_year_musd, rel=COST_SUM_REL_TOL)


def test_cohort_arpu_subscribers_sum_to_year_served_exactly() -> None:
    """The per-cohort allocated subscribers sum EXACTLY to the year's served count.

    The last living cohort absorbs the rounding remainder, so the integer parts sum
    with no drift versus the fleet-level served base.
    """
    traj = run_comms_model(CommsConfig())
    for year in traj.years:
        allocated = sum(line.arpu_subscribers_served for line in year.cohort_lines)
        assert allocated == year.subscribers_served_this_year


def test_cohort_lines_track_living_cohorts_under_the_cliff() -> None:
    """Each year's cohort lines are exactly the cohorts alive under the 5-year cliff.

    The cohort lines carry one entry per living cohort, and their living-satellite
    counts sum to the year's living fleet (the same cliff the cost treadmill uses).
    """
    config = CommsConfig()
    life = config.satellite.satellite_lifetime_years
    traj = run_comms_model(config)
    for year in traj.years:
        # Every cohort line is within the cliff window of this year.
        for line in year.cohort_lines:
            assert line.launch_year <= year.year < line.launch_year + life
            assert line.living_satellites > 0
        # The living-satellite counts sum to the year's living fleet.
        assert sum(line.living_satellites for line in year.cohort_lines) == year.living_fleet


def test_cohort_cost_plus_margin_is_flat_across_cohorts() -> None:
    """Every living cohort earns the same flat cost-plus margin (cost-coupled revenue)."""
    config = CommsConfig()
    multiple = config.revenue.revenue_multiple
    expected_margin_pct = (multiple - 1.0) / multiple * MARGIN_PERCENT_SCALE
    traj = run_comms_model(config)
    for year in traj.years:
        for line in year.cohort_lines:
            assert line.cost_plus_gross_margin_pct == pytest.approx(
                expected_margin_pct, rel=COST_SUM_REL_TOL
            )


def test_steady_state_revenue_headlines_are_final_year_lines() -> None:
    """The trajectory steady-state revenue/margin headlines equal the final year's lines."""
    traj = run_comms_model(CommsConfig())
    final = traj.years[-1]
    assert traj.steady_state_annual_cost_musd == pytest.approx(final.annual_cost_this_year_musd)
    assert traj.steady_state_revenue_cost_plus_musd == pytest.approx(
        final.cost_plus_revenue_this_year_musd
    )
    assert traj.steady_state_gross_margin_cost_plus_pct == pytest.approx(
        final.cost_plus_gross_margin_pct
    )
    assert traj.steady_state_revenue_arpu_musd == pytest.approx(final.arpu_revenue_this_year_musd)
    assert traj.steady_state_gross_margin_arpu_pct == pytest.approx(final.arpu_gross_margin_pct)


def test_higher_arpu_lifts_arpu_revenue_and_margin() -> None:
    """Doubling the ARPU dial doubles the ARPU revenue and raises its margin.

    The cost-plus case is unchanged by the ARPU dial (revenue is cost-coupled), so the
    two cases are independent lenses, as designed.
    """
    base = run_comms_model(CommsConfig())
    higher = run_comms_model(CommsConfig(revenue=RevenueDials(arpu_usd_per_month=100.0)))
    # ARPU revenue doubles (50 -> 100); the served base and cost are unchanged.
    assert higher.steady_state_revenue_arpu_musd == pytest.approx(
        2.0 * base.steady_state_revenue_arpu_musd, rel=COST_SUM_REL_TOL
    )
    assert higher.steady_state_gross_margin_arpu_pct > base.steady_state_gross_margin_arpu_pct
    # The cost-plus case is untouched by the ARPU dial.
    assert higher.steady_state_revenue_cost_plus_musd == pytest.approx(
        base.steady_state_revenue_cost_plus_musd, rel=COST_SUM_REL_TOL
    )
