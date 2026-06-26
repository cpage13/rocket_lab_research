"""Phase 3 tests for the coverage-to-subscribers mapping (the NEW logic).

These cover the plan's Phase 3 test list: the coverage-driven mapping is linear
in the coverage fraction (full coverage serves the base, half coverage serves
half), the optional direct override replaces the full-coverage base while still
scaling below full coverage, the engine reports the served-people count at the
FY2036 coverage, and no forbidden demand-side token appears in the comms src.

The subscriber unit is a PERSON (a phone subscriber), because the product is
CELLULAR direct-to-cell, NOT a household. The mapping is coverage-driven, NOT
capacity-derived: there is no spectrum / beam / capacity term anywhere in it.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import pytest

from communications.config import CommsConfig, CoverageDials, SubscriberDials
from communications.engine import run_comms_model, subscribers_served_at

# A representative full-coverage base distinct from the dialled default, so a test
# asserting "result == base" cannot pass by coincidence against the default.
SAMPLE_FULL_COVERAGE_SUBSCRIBERS = 40_000_000

# A representative direct override distinct from both the default and the sample
# base, so the override-vs-mapping precedence is unambiguous.
SAMPLE_OVERRIDE_SUBSCRIBERS = 12_000_000

# The comms src directory (anchored from this test file: tests/communications ->
# code -> src/communications), scanned by the forbidden-token guard below.
_COMMS_SRC = Path(__file__).resolve().parents[2] / "src" / "communications"
_COMMS_SRC_FILES = sorted(_COMMS_SRC.glob("*.py"))

# The same forbidden config-time / demand-lever tokens the architecture guard
# locks out (kept in sync with tests/communications/test_no_venture_cross_import.py),
# re-checked here against the Phase 3 code specifically.
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
# The mapping function (subscribers_served_at) in isolation.
# ---------------------------------------------------------------------------


def test_full_coverage_serves_the_full_base() -> None:
    """At coverage_fraction == 1.0 the mapping serves exactly the full-coverage base."""
    served = subscribers_served_at(
        1.0,
        subscribers_at_full_coverage=SAMPLE_FULL_COVERAGE_SUBSCRIBERS,
        override=None,
    )
    assert served == SAMPLE_FULL_COVERAGE_SUBSCRIBERS


def test_half_coverage_serves_half_the_base() -> None:
    """At coverage_fraction == 0.5 the mapping serves half the base (within rounding)."""
    served = subscribers_served_at(
        0.5,
        subscribers_at_full_coverage=SAMPLE_FULL_COVERAGE_SUBSCRIBERS,
        override=None,
    )
    assert served == SAMPLE_FULL_COVERAGE_SUBSCRIBERS // 2


def test_zero_coverage_serves_nobody() -> None:
    """At coverage_fraction == 0.0 the mapping serves zero people."""
    served = subscribers_served_at(
        0.0,
        subscribers_at_full_coverage=SAMPLE_FULL_COVERAGE_SUBSCRIBERS,
        override=None,
    )
    assert served == 0


def test_mapping_is_linear_in_the_coverage_fraction() -> None:
    """The served count scales linearly with the coverage fraction (half-up rounded)."""
    base = SAMPLE_FULL_COVERAGE_SUBSCRIBERS
    for fraction in (0.1, 0.25, 0.4, 0.75, 0.9):
        served = subscribers_served_at(fraction, subscribers_at_full_coverage=base, override=None)
        # round_half_up(fraction * base) == floor(fraction * base + 0.5).
        assert served == math.floor(fraction * base + 0.5)


def test_override_replaces_the_full_coverage_base() -> None:
    """When set, the override is the base at full coverage (not subscribers_at_full_coverage)."""
    served = subscribers_served_at(
        1.0,
        subscribers_at_full_coverage=SAMPLE_FULL_COVERAGE_SUBSCRIBERS,
        override=SAMPLE_OVERRIDE_SUBSCRIBERS,
    )
    assert served == SAMPLE_OVERRIDE_SUBSCRIBERS


def test_override_still_scales_below_full_coverage() -> None:
    """The override scales by the coverage fraction below full coverage (it is the base)."""
    served = subscribers_served_at(
        0.5,
        subscribers_at_full_coverage=SAMPLE_FULL_COVERAGE_SUBSCRIBERS,
        override=SAMPLE_OVERRIDE_SUBSCRIBERS,
    )
    assert served == SAMPLE_OVERRIDE_SUBSCRIBERS // 2


def test_coverage_fraction_clamps_above_one() -> None:
    """A coverage fraction above 1.0 is clamped: the served count never exceeds the base."""
    served = subscribers_served_at(
        1.5,
        subscribers_at_full_coverage=SAMPLE_FULL_COVERAGE_SUBSCRIBERS,
        override=None,
    )
    assert served == SAMPLE_FULL_COVERAGE_SUBSCRIBERS


def test_coverage_fraction_clamps_below_zero() -> None:
    """A negative coverage fraction is clamped to zero: the served count never goes negative."""
    served = subscribers_served_at(
        -0.3,
        subscribers_at_full_coverage=SAMPLE_FULL_COVERAGE_SUBSCRIBERS,
        override=None,
    )
    assert served == 0


# ---------------------------------------------------------------------------
# The reported subscribers-served on the trajectory (the FY2036-coverage value).
# ---------------------------------------------------------------------------


def test_reported_subscribers_equals_final_year_mapping() -> None:
    """CommsTrajectory.subscribers_served == the mapping applied to the FY2036 coverage."""
    config = CommsConfig()
    traj = run_comms_model(config)
    expected = subscribers_served_at(
        traj.years[-1].coverage_fraction,
        subscribers_at_full_coverage=config.subscribers.subscribers_at_full_coverage,
        override=config.subscribers.subscribers_served_override,
    )
    assert traj.subscribers_served == expected


def test_default_run_serves_full_base_after_completed_build_out() -> None:
    """The default build-out completes, so the reported served count is the full base."""
    config = CommsConfig()
    traj = run_comms_model(config)
    # The default coverage target is reached within the horizon, so FY2036 coverage
    # is clamped to 1.0 and the served count equals the configured full-coverage base.
    assert traj.full_coverage_reached_year is not None
    assert traj.years[-1].coverage_fraction == pytest.approx(1.0)
    assert traj.subscribers_served == config.subscribers.subscribers_at_full_coverage


def test_default_run_serves_fifty_million_people() -> None:
    """The default reported served count is the founder-set 50,000,000 people (the swing dial)."""
    traj = run_comms_model(CommsConfig())
    assert traj.subscribers_served == 50_000_000


def test_override_drives_the_reported_subscribers_at_full_coverage() -> None:
    """A configured override sets the reported served count once the build-out completes."""
    config = CommsConfig(
        subscribers=SubscriberDials(
            subscribers_at_full_coverage=SAMPLE_FULL_COVERAGE_SUBSCRIBERS,
            subscribers_served_override=SAMPLE_OVERRIDE_SUBSCRIBERS,
        )
    )
    traj = run_comms_model(config)
    assert traj.full_coverage_reached_year is not None
    assert traj.subscribers_served == SAMPLE_OVERRIDE_SUBSCRIBERS


def test_partial_coverage_reports_proportional_subscribers() -> None:
    """A target too high to complete reports the proportional partial-coverage served count."""
    unreachable_target = 100_000
    config = CommsConfig(coverage=CoverageDials(satellites_for_full_coverage=unreachable_target))
    traj = run_comms_model(config)
    # The build-out never completes, so FY2036 coverage is below 1.0 and the served
    # count is strictly below the full-coverage base (a truthful partial output).
    assert traj.full_coverage_reached_year is None
    assert traj.years[-1].coverage_fraction < 1.0
    assert traj.subscribers_served < config.subscribers.subscribers_at_full_coverage
    expected = subscribers_served_at(
        traj.years[-1].coverage_fraction,
        subscribers_at_full_coverage=config.subscribers.subscribers_at_full_coverage,
        override=None,
    )
    assert traj.subscribers_served == expected


# ---------------------------------------------------------------------------
# The forbidden-token guard, re-checked against the Phase 3 comms src.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("token", _FORBIDDEN_TOKENS)
def test_no_forbidden_token_in_comms_src(token: str) -> None:
    """No forbidden demand-lever / market token appears in any comms src file (Phase 3 included)."""
    pattern = re.compile(token, re.IGNORECASE)
    for src_file in _COMMS_SRC_FILES:
        assert not pattern.search(src_file.read_text()), f"{token} found in {src_file.name}"
