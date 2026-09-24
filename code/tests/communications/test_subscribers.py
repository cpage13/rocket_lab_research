"""Tests for the capacity dimension: fleet sizing and the buildout-to-subscribers map.

These cover the capacity-sized model: the fleet target is the subscriber target
divided by the per-satellite density, floored by the coverage floor and capped by
the saturation cap (:func:`compute_fleet_target`), with the binding regime reported;
the served count RAMPS with the buildout (the subscriber target, or the served
override, capped at the fleet target's people capacity and scaled by the fraction of
the capacity-sized fleet on orbit); the engine reports the served-people count at the
FY2036 buildout and the final-year cash cost per served person; the regime labels
stay consistent with the served count (only the saturated regime serves below the
target); and no forbidden demand-side token appears in the comms src.

The subscriber unit is a PERSON, NOT a household. The fleet is capacity-SIZED to
SERVE the base; the served base is a sized INPUT, NOT a demand estimate, and the
capacity enters the mapping only as the ceiling on that base.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import pytest

from communications.config import CommsConfig, IridiumDials, SubscriberDials
from communications.constants import (
    MAX_FLEET_SATELLITES_DEFAULT,
    SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
    SUBSCRIBERS_PER_SATELLITE_DEFAULT,
    BindingRegime,
)
from communications.engine import (
    MUSD_TO_USD,
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

# A people capacity above every base these isolated mapping tests use, so the
# capacity ceiling does not bind and the tests exercise the ramp alone.
NON_BINDING_PEOPLE_CAPACITY = 1_000_000_000

# A people capacity below the sample base, so the ceiling binds.
BINDING_PEOPLE_CAPACITY = 25_000_000

# The Iridium phone-class tier at a 10 Mbps active rate: density 780 / (10 x 0.025)
# = 3,120 per satellite, so the 10M target needs 3,206 satellites, above the 2,000
# cap (saturated); the capped fleet carries 2,000 x 3,120 = 6,240,000 people.
SATURATING_ACTIVE_RATE_MBPS = 10.0
SATURATED_DENSITY_PER_SATELLITE = 3_120
SATURATED_PEOPLE_CAPACITY = 6_240_000

# The three investor scenarios: the 10M baseline plus the 50M / 100M targets.
BASELINE_TARGET = 10_000_000
SCENARIO_50M_TARGET = 50_000_000
SCENARIO_100M_TARGET = 100_000_000

# Targets at and past the saturation cap on the cellular defaults (75,000 per
# satellite, 2,000-satellite cap): 150M needs exactly the 2,000 satellites (the
# boundary: the cap binds, and its capacity still carries the whole target, so
# it is served in full); 200M needs 2,667, so the capped fleet serves only 150M.
AT_CAP_TARGET = 150_000_000
ABOVE_CAP_TARGET = 200_000_000

# The spec's worked fleet targets at the defaults (75,000/sat, 340 floor, 2,000 cap):
# 10M -> ceil(133.3)=134 -> max(340,134)=340; 50M -> 667; 100M -> 1,334.
EXPECTED_FLEET_TARGET_10M = 340
EXPECTED_FLEET_TARGET_50M = 667
EXPECTED_FLEET_TARGET_100M = 1_334


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
        people_capacity=NON_BINDING_PEOPLE_CAPACITY,
    )
    assert served == SAMPLE_SUBSCRIBER_TARGET


def test_half_deployment_serves_half_the_target() -> None:
    """At buildout_fraction == 0.5 the mapping serves half the target (within rounding)."""
    served = subscribers_served_at(
        0.5,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=None,
        people_capacity=NON_BINDING_PEOPLE_CAPACITY,
    )
    assert served == SAMPLE_SUBSCRIBER_TARGET // 2


def test_zero_deployment_serves_nobody() -> None:
    """At buildout_fraction == 0.0 the mapping serves zero people."""
    served = subscribers_served_at(
        0.0,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=None,
        people_capacity=NON_BINDING_PEOPLE_CAPACITY,
    )
    assert served == 0


def test_mapping_is_linear_in_the_buildout_fraction() -> None:
    """The served count scales linearly with the buildout fraction (half-up rounded)."""
    base = SAMPLE_SUBSCRIBER_TARGET
    for fraction in (0.1, 0.25, 0.4, 0.75, 0.9):
        served = subscribers_served_at(
            fraction,
            subscriber_target=base,
            override=None,
            people_capacity=NON_BINDING_PEOPLE_CAPACITY,
        )
        # round_half_up(fraction * base) == floor(fraction * base + 0.5).
        assert served == math.floor(fraction * base + 0.5)


def test_override_replaces_the_full_deployment_base() -> None:
    """When set, the override is the base at full deployment (not subscriber_target)."""
    served = subscribers_served_at(
        1.0,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=SAMPLE_OVERRIDE_SUBSCRIBERS,
        people_capacity=NON_BINDING_PEOPLE_CAPACITY,
    )
    assert served == SAMPLE_OVERRIDE_SUBSCRIBERS


def test_override_still_scales_below_full_deployment() -> None:
    """The override scales by the buildout fraction below full deployment (it is the base)."""
    served = subscribers_served_at(
        0.5,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=SAMPLE_OVERRIDE_SUBSCRIBERS,
        people_capacity=NON_BINDING_PEOPLE_CAPACITY,
    )
    assert served == SAMPLE_OVERRIDE_SUBSCRIBERS // 2


def test_buildout_fraction_clamps_above_one() -> None:
    """A buildout fraction above 1.0 is clamped: the served count never exceeds the base."""
    served = subscribers_served_at(
        1.5,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=None,
        people_capacity=NON_BINDING_PEOPLE_CAPACITY,
    )
    assert served == SAMPLE_SUBSCRIBER_TARGET


def test_buildout_fraction_clamps_below_zero() -> None:
    """A negative buildout fraction is clamped to zero: the served count never goes negative."""
    served = subscribers_served_at(
        -0.3,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=None,
        people_capacity=NON_BINDING_PEOPLE_CAPACITY,
    )
    assert served == 0


def test_served_base_is_capped_at_the_people_capacity() -> None:
    """A base above the fleet's people capacity serves the capacity, never more.

    Objective: the capacity ceiling on the served base. Expected: with a 40M target
    and a 25M capacity, full deployment serves 25M and half deployment serves 12.5M
    (the ramp scales the capped base).
    """
    full = subscribers_served_at(
        1.0,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=None,
        people_capacity=BINDING_PEOPLE_CAPACITY,
    )
    half = subscribers_served_at(
        0.5,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=None,
        people_capacity=BINDING_PEOPLE_CAPACITY,
    )
    assert full == BINDING_PEOPLE_CAPACITY
    assert half == BINDING_PEOPLE_CAPACITY // 2


def test_override_is_capped_at_the_people_capacity() -> None:
    """A served override above the fleet's people capacity is capped at the capacity.

    Objective: the override cannot bypass capacity. Expected: an override of 40M on
    a 25M capacity serves 25M at full deployment, while an override below the
    capacity (12M) is served in full.
    """
    capped = subscribers_served_at(
        1.0,
        subscriber_target=SAMPLE_OVERRIDE_SUBSCRIBERS,
        override=SAMPLE_SUBSCRIBER_TARGET,
        people_capacity=BINDING_PEOPLE_CAPACITY,
    )
    uncapped = subscribers_served_at(
        1.0,
        subscriber_target=SAMPLE_SUBSCRIBER_TARGET,
        override=SAMPLE_OVERRIDE_SUBSCRIBERS,
        people_capacity=BINDING_PEOPLE_CAPACITY,
    )
    assert capped == BINDING_PEOPLE_CAPACITY
    assert uncapped == SAMPLE_OVERRIDE_SUBSCRIBERS


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
        people_capacity=traj.fleet_target * traj.subscribers_per_satellite,
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


def test_default_run_cash_cost_per_subscriber_is_final_year_over_served() -> None:
    """The default final-year cash per subscriber is the final-year replacement over served.

    Objective: the cash per-person figure on the default run. Expected: the final-year
    replacement (USD) over the 10M served base, a positive figure (the final year
    replaces a retiring cohort).
    """
    traj = run_comms_model(CommsConfig())
    assert traj.subscribers_served == BASELINE_TARGET
    assert traj.final_year_replacement_cost_musd is not None
    expected_usd = traj.final_year_replacement_cost_musd * MUSD_TO_USD / BASELINE_TARGET
    assert traj.final_year_cash_cost_per_subscriber_usd == pytest.approx(expected_usd)
    assert expected_usd > 0.0


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
        people_capacity=traj.fleet_target * traj.subscribers_per_satellite,
    )
    assert traj.subscribers_served == expected
    # The final year is still a build year: its cash replacement is only the cohort
    # retiring that year (never the build tranche), over the partial served base.
    final = traj.years[-1]
    assert traj.final_year_replacement_cost_musd == final.replacement_cost_this_year_musd
    assert traj.final_year_replacement_cost_musd is not None
    assert traj.final_year_replacement_cost_musd < final.total_cost_this_year_musd
    assert traj.final_year_cash_cost_per_subscriber_usd == pytest.approx(
        traj.final_year_replacement_cost_musd * MUSD_TO_USD / traj.subscribers_served
    )


def test_saturated_regime_serves_at_most_the_fleet_capacity() -> None:
    """A saturated run serves the capped fleet's people capacity, not the full target.

    Objective: the served base never exceeds what the fleet carries. On the Iridium
    phone-class tier at a 10 Mbps active rate the density is 3,120 per satellite, so
    the 10M target needs 3,206 satellites and the fleet pins at the 2,000 cap.
    Expected: the regime is saturated and the run (all-in share, so the build
    completes) serves 6,240,000 people (2,000 x 3,120), below the 10M target.
    """
    config = CommsConfig.model_validate(
        {
            "comms_cadence": {"share_of_fleet": 1.0},
            "iridium": IridiumDials(active_user_rate_mbps=SATURATING_ACTIVE_RATE_MBPS).model_dump(),
        }
    )
    traj = run_comms_model(config)
    assert traj.subscribers_per_satellite == SATURATED_DENSITY_PER_SATELLITE
    assert traj.fleet_target == MAX_FLEET_SATELLITES_DEFAULT
    assert traj.binding_regime is BindingRegime.SATURATED
    assert traj.full_coverage_reached_year is not None
    assert traj.subscribers_served == SATURATED_PEOPLE_CAPACITY
    assert traj.subscribers_served < config.subscribers.subscribers_at_full_coverage


@pytest.mark.parametrize(
    "subscriber_target",
    [BASELINE_TARGET, SCENARIO_50M_TARGET, SCENARIO_100M_TARGET, AT_CAP_TARGET, ABOVE_CAP_TARGET],
)
def test_served_below_target_only_in_the_saturated_regime(subscriber_target: int) -> None:
    """The regime label and the served count agree: only saturation serves below target.

    Objective: regime-label consistency across the coverage, capacity, and saturated
    regimes on the cellular defaults (75,000 per satellite, 340 floor, 2,000 cap),
    with an all-in share so every build completes. Expected: the full-deployment
    served count equals the target unless the capacity need exceeds the cap, in which
    case the regime is saturated and the served count is the cap's people capacity.
    """
    config = CommsConfig.model_validate(
        {
            "comms_cadence": {"share_of_fleet": 1.0},
            "subscribers": {"subscribers_at_full_coverage": subscriber_target},
        }
    )
    traj = run_comms_model(config)
    assert traj.full_coverage_reached_year is not None
    capacity_need = math.ceil(subscriber_target / SUBSCRIBERS_PER_SATELLITE_DEFAULT)
    if capacity_need > MAX_FLEET_SATELLITES_DEFAULT:
        assert traj.binding_regime is BindingRegime.SATURATED
        assert traj.subscribers_served == (
            MAX_FLEET_SATELLITES_DEFAULT * SUBSCRIBERS_PER_SATELLITE_DEFAULT
        )
        assert traj.subscribers_served < subscriber_target
    else:
        assert traj.subscribers_served == subscriber_target


def test_override_above_capacity_is_capped_and_warned(caplog: pytest.LogCaptureFixture) -> None:
    """A served override above the fleet's capacity is capped and logged as a warning.

    Objective: the override cannot bypass capacity on a real run. The fleet is sized
    from the 10M target (340 satellites at 75,000, a 25,500,000 capacity). Expected:
    a 40M override serves 25,500,000 people and logs a WARNING naming the override.
    """
    config = CommsConfig(
        subscribers=SubscriberDials(subscribers_served_override=SAMPLE_SUBSCRIBER_TARGET)
    )
    with caplog.at_level("WARNING", logger="communications.engine"):
        traj = run_comms_model(config)
    capacity = EXPECTED_FLEET_TARGET_10M * SUBSCRIBERS_PER_SATELLITE_DEFAULT
    assert traj.subscribers_served == capacity
    assert "subscribers_served_override" in caplog.text


# ---------------------------------------------------------------------------
# The forbidden-token guard, re-checked against the comms src.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("token", _FORBIDDEN_TOKENS)
def test_no_forbidden_token_in_comms_src(token: str, code_dir: Path) -> None:
    """No forbidden demand-lever / market token appears in any comms src file."""
    pattern = re.compile(token, re.IGNORECASE)
    src_files = sorted((code_dir / "src" / "communications").glob("*.py"))
    assert src_files, "no comms src file found"
    for src_file in src_files:
        assert not pattern.search(src_file.read_text()), f"{token} found in {src_file.name}"
