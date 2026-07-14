"""Tests for the capacity dimension: fleet sizing and the buildout-to-subscribers map.

These cover the capacity-sized model: the fleet target is the subscriber target
divided by the per-satellite density, floored by the coverage floor and capped by
the saturation cap (:func:`compute_fleet_target`), with the binding regime reported;
the served count RAMPS with the buildout (the subscriber target scaled by the
fraction of the capacity-sized fleet on orbit, reaching the target at full
deployment); the engine reports the served-people count at the FY2036 buildout and
the annual cost per subscriber against the target; and no forbidden demand-side
token appears in the comms src.

The subscriber unit is a PERSON (a phone subscriber), because the product is
CELLULAR direct-to-cell, NOT a household. The fleet is capacity-SIZED to SERVE the
base; the served base is a sized INPUT, NOT a demand estimate, and there is no
spectrum / beam / capacity term in the mapping itself.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import pytest

from communications.config import CommsConfig, SubscriberDials
from communications.constants import (
    MAX_FLEET_SATELLITES_DEFAULT,
    SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
    SUBSCRIBERS_PER_SATELLITE_DEFAULT,
    BindingRegime,
)
from communications.engine import (
    compute_fleet_target,
    run_comms_model,
    subscribers_served_at,
)

# A representative subscriber target distinct from the dialled default, so a test
# asserting "result == base" cannot pass by coincidence against the default.
SAMPLE_SUBSCRIBER_TARGET = 40_000_000

# A representative direct override distinct from both the default and the sample
# base, so the override-vs-target precedence is unambiguous.
SAMPLE_OVERRIDE_SUBSCRIBERS = 12_000_000

# The three investor scenarios: the 10M baseline plus the 50M / 100M targets.
BASELINE_TARGET = 10_000_000
SCENARIO_50M_TARGET = 50_000_000
SCENARIO_100M_TARGET = 100_000_000

# The spec's worked fleet targets at the defaults (75,000/sat, 340 floor, 2,000 cap):
# 10M -> ceil(133.3)=134 -> max(340,134)=340; 50M -> 667; 100M -> 1,334.
EXPECTED_FLEET_TARGET_10M = 340
EXPECTED_FLEET_TARGET_50M = 667
EXPECTED_FLEET_TARGET_100M = 1_334

# The comms src directory (anchored from this test file: tests/communications ->
# code -> src/communications), scanned by the forbidden-token guard below.
_COMMS_SRC = Path(__file__).resolve().parents[2] / "src" / "communications"
_COMMS_SRC_FILES = sorted(_COMMS_SRC.glob("*.py"))

# The same forbidden config-time / demand-lever tokens the architecture guard
# locks out (kept in sync with tests/communications/test_no_venture_cross_import.py),
# re-checked here against the capacity-dimension code specifically.
_FORBIDDEN_TOKENS = [
    "starship",
    "capture_share",
    "share_pct",
    "market_share",
    "market_size",
    "market_growth",
    "compute_market_size",
    "adoption",
    "take_rate",
    "uptake",
]


# ---------------------------------------------------------------------------
# The fleet-sizing function (compute_fleet_target) in isolation.
# ---------------------------------------------------------------------------


def test_fleet_target_coverage_floor_binds_for_small_base() -> None:
    """A small base needs fewer capacity satellites than the floor: the floor binds."""
    fleet_target, regime = compute_fleet_target(
        subscriber_target=BASELINE_TARGET,
        subscribers_per_satellite=SUBSCRIBERS_PER_SATELLITE_DEFAULT,
        coverage_floor=SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
        max_fleet_satellites=MAX_FLEET_SATELLITES_DEFAULT,
    )
    assert fleet_target == EXPECTED_FLEET_TARGET_10M
    assert regime is BindingRegime.COVERAGE


def test_fleet_target_capacity_binds_for_mid_base() -> None:
    """A mid base needs more capacity satellites than the floor, under the cap: capacity binds."""
    fleet_target, regime = compute_fleet_target(
        subscriber_target=SCENARIO_50M_TARGET,
        subscribers_per_satellite=SUBSCRIBERS_PER_SATELLITE_DEFAULT,
        coverage_floor=SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
        max_fleet_satellites=MAX_FLEET_SATELLITES_DEFAULT,
    )
    assert fleet_target == EXPECTED_FLEET_TARGET_50M
    assert regime is BindingRegime.CAPACITY


def test_fleet_target_100m_capacity_binds_under_cap() -> None:
    """The 100M target needs 1,334 satellites, under the 2,000 cap: capacity binds."""
    fleet_target, regime = compute_fleet_target(
        subscriber_target=SCENARIO_100M_TARGET,
        subscribers_per_satellite=SUBSCRIBERS_PER_SATELLITE_DEFAULT,
        coverage_floor=SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
        max_fleet_satellites=MAX_FLEET_SATELLITES_DEFAULT,
    )
    assert fleet_target == EXPECTED_FLEET_TARGET_100M
    assert regime is BindingRegime.CAPACITY


def test_fleet_target_capacity_need_is_ceiling_division() -> None:
    """The capacity need rounds UP (a partial satellite's worth still needs a whole one)."""
    # 10,000,001 / 75,000 = 133.33.. -> ceil 134, but the floor (340) still binds here.
    # Use a base just over a 75,000 multiple above the floor to see the ceiling bite.
    base = SATELLITES_FOR_FULL_COVERAGE_DEFAULT * SUBSCRIBERS_PER_SATELLITE_DEFAULT + 1
    fleet_target, regime = compute_fleet_target(
        subscriber_target=base,
        subscribers_per_satellite=SUBSCRIBERS_PER_SATELLITE_DEFAULT,
        coverage_floor=SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
        max_fleet_satellites=MAX_FLEET_SATELLITES_DEFAULT,
    )
    # ceil((340*75000 + 1) / 75000) = 341.
    assert fleet_target == SATELLITES_FOR_FULL_COVERAGE_DEFAULT + 1
    assert regime is BindingRegime.CAPACITY


def test_fleet_target_saturates_at_the_cap() -> None:
    """An enormous base needs more than the cap: the fleet pins at the cap (saturated)."""
    huge_base = MAX_FLEET_SATELLITES_DEFAULT * SUBSCRIBERS_PER_SATELLITE_DEFAULT * 2
    fleet_target, regime = compute_fleet_target(
        subscriber_target=huge_base,
        subscribers_per_satellite=SUBSCRIBERS_PER_SATELLITE_DEFAULT,
        coverage_floor=SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
        max_fleet_satellites=MAX_FLEET_SATELLITES_DEFAULT,
    )
    assert fleet_target == MAX_FLEET_SATELLITES_DEFAULT
    assert regime is BindingRegime.SATURATED


# ---------------------------------------------------------------------------
# The buildout-to-subscribers mapping (subscribers_served_at) in isolation.
# ---------------------------------------------------------------------------


def test_full_deployment_serves_the_whole_target() -> None:
    """At buildout_fraction == 1.0 the mapping serves exactly the subscriber target."""
    served = subscribers_served_at(
        1.0,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=None,
    )
    assert served == SAMPLE_SUBSCRIBER_TARGET


def test_half_deployment_serves_half_the_target() -> None:
    """At buildout_fraction == 0.5 the mapping serves half the target (within rounding)."""
    served = subscribers_served_at(
        0.5,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=None,
    )
    assert served == SAMPLE_SUBSCRIBER_TARGET // 2


def test_zero_deployment_serves_nobody() -> None:
    """At buildout_fraction == 0.0 the mapping serves zero people."""
    served = subscribers_served_at(
        0.0,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=None,
    )
    assert served == 0


def test_mapping_is_linear_in_the_buildout_fraction() -> None:
    """The served count scales linearly with the buildout fraction (half-up rounded)."""
    base = SAMPLE_SUBSCRIBER_TARGET
    for fraction in (0.1, 0.25, 0.4, 0.75, 0.9):
        served = subscribers_served_at(fraction, subscriber_target=base, override=None)
        # round_half_up(fraction * base) == floor(fraction * base + 0.5).
        assert served == math.floor(fraction * base + 0.5)


def test_override_replaces_the_full_deployment_base() -> None:
    """When set, the override is the base at full deployment (not subscriber_target)."""
    served = subscribers_served_at(
        1.0,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=SAMPLE_OVERRIDE_SUBSCRIBERS,
    )
    assert served == SAMPLE_OVERRIDE_SUBSCRIBERS


def test_override_still_scales_below_full_deployment() -> None:
    """The override scales by the buildout fraction below full deployment (it is the base)."""
    served = subscribers_served_at(
        0.5,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=SAMPLE_OVERRIDE_SUBSCRIBERS,
    )
    assert served == SAMPLE_OVERRIDE_SUBSCRIBERS // 2


def test_buildout_fraction_clamps_above_one() -> None:
    """A buildout fraction above 1.0 is clamped: the served count never exceeds the base."""
    served = subscribers_served_at(
        1.5,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=None,
    )
    assert served == SAMPLE_SUBSCRIBER_TARGET


def test_buildout_fraction_clamps_below_zero() -> None:
    """A negative buildout fraction is clamped to zero: the served count never goes negative."""
    served = subscribers_served_at(
        -0.3,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=None,
    )
    assert served == 0


# ---------------------------------------------------------------------------
# The fleet target + served-subscribers + cost-per-subscriber on the trajectory.
# ---------------------------------------------------------------------------


def test_trajectory_surfaces_the_fleet_target_and_regime() -> None:
    """The default trajectory reports the 340-satellite fleet target in the coverage regime."""
    traj = run_comms_model(CommsConfig())
    assert traj.fleet_target == EXPECTED_FLEET_TARGET_10M
    assert traj.binding_regime is BindingRegime.COVERAGE
    assert traj.subscribers_per_satellite == SUBSCRIBERS_PER_SATELLITE_DEFAULT


def test_reported_subscribers_equals_final_year_mapping() -> None:
    """CommsTrajectory.subscribers_served == the mapping applied to the FY2036 buildout."""
    config = CommsConfig()
    traj = run_comms_model(config)
    expected = subscribers_served_at(
        traj.years[-1].buildout_fraction,
        subscriber_target=config.subscribers.subscribers_at_full_coverage,
        override=config.subscribers.subscribers_served_override,
    )
    assert traj.subscribers_served == expected


def test_default_run_serves_full_target_after_completed_build_out() -> None:
    """The default build-out completes, so the reported served count is the whole target."""
    config = CommsConfig()
    traj = run_comms_model(config)
    # The default fleet target (340, coverage-floor-bound) is reached within the
    # horizon, so FY2036 buildout is clamped to 1.0 and the served count is the target.
    assert traj.full_coverage_reached_year is not None
    assert traj.years[-1].buildout_fraction == pytest.approx(1.0)
    assert traj.subscribers_served == config.subscribers.subscribers_at_full_coverage


def test_default_run_serves_ten_million_people() -> None:
    """The default reported served count is the investor baseline 10,000,000 people."""
    traj = run_comms_model(CommsConfig())
    assert traj.subscribers_served == BASELINE_TARGET


def test_default_run_cost_per_subscriber_is_steady_state_over_target() -> None:
    """The default cost per subscriber is steady-state annual cost (USD) over the target."""
    traj = run_comms_model(CommsConfig())
    expected_usd = traj.steady_state_annual_replacement_cost_musd * 1_000_000.0 / BASELINE_TARGET
    assert traj.cost_per_subscriber_annual_usd == pytest.approx(expected_usd)
    # The 10M baseline completes, so the figure is a positive single-digit $/sub/yr.
    assert traj.cost_per_subscriber_annual_usd > 0.0


def test_override_drives_the_reported_subscribers_at_full_deployment() -> None:
    """A configured override sets the reported served count once the build-out completes.

    The override is a SERVED-BASE override, not a fleet-sizing override: the fleet is
    still sized from the subscriber target. Use the baseline target (whose 340-fleet
    completes) so the build reaches full deployment and the override is fully served.
    """
    config = CommsConfig(
        subscribers=SubscriberDials(
            subscribers_at_full_coverage=BASELINE_TARGET,
            subscribers_served_override=SAMPLE_OVERRIDE_SUBSCRIBERS,
        )
    )
    traj = run_comms_model(config)
    assert traj.full_coverage_reached_year is not None
    # The fleet target is still sized from the 10M target (coverage floor 340).
    assert traj.fleet_target == EXPECTED_FLEET_TARGET_10M
    assert traj.subscribers_served == SAMPLE_OVERRIDE_SUBSCRIBERS


def test_partial_deployment_reports_proportional_subscribers() -> None:
    """A fleet target too high to complete reports the proportional partial-deployment count.

    The 100M target sizes a 1,334-satellite fleet, which the default 0.18 cadence
    share cannot build within the 10-year horizon, so FY2036 buildout is below 1.0
    and the served count is strictly below the target (a truthful partial output).
    """
    config = CommsConfig(
        subscribers=SubscriberDials(subscribers_at_full_coverage=SCENARIO_100M_TARGET)
    )
    traj = run_comms_model(config)
    assert traj.fleet_target == EXPECTED_FLEET_TARGET_100M
    assert traj.full_coverage_reached_year is None
    assert traj.years[-1].buildout_fraction < 1.0
    assert traj.subscribers_served < SCENARIO_100M_TARGET
    expected = subscribers_served_at(
        traj.years[-1].buildout_fraction,
        subscriber_target=SCENARIO_100M_TARGET,
        override=None,
    )
    assert traj.subscribers_served == expected
    # An incomplete build never reaches steady state, so the per-subscriber figure
    # is the truthful 0.0 (no steady-state cost line yet).
    assert traj.steady_state_annual_replacement_cost_musd == 0.0
    assert traj.cost_per_subscriber_annual_usd == 0.0


# ---------------------------------------------------------------------------
# The forbidden-token guard, re-checked against the comms src.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("token", _FORBIDDEN_TOKENS)
def test_no_forbidden_token_in_comms_src(token: str) -> None:
    """No forbidden demand-lever / market token appears in any comms src file."""
    pattern = re.compile(token, re.IGNORECASE)
    for src_file in _COMMS_SRC_FILES:
        assert not pattern.search(src_file.read_text()), f"{token} found in {src_file.name}"
