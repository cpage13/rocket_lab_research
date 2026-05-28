"""Tests for cadence module — launches per year + cadence-indexed launch cost.

Cycle-2 Phase 2: the two public functions return a ``ProvenanceCell``; the
assertions unwrap ``.value``. ``_log_interp`` stays a bare-float helper.
"""

from __future__ import annotations

import pytest

from data_center.cadence import (
    _log_interp,
    compute_launch_cost_musd,
    compute_launches_per_year,
)
from data_center.constants import (
    CADENCE_CEILING_DEFAULT,
    HIGH_CADENCE_COST_MUSD_DEFAULT,
    LAUNCHES_AT_YEAR_5_DEFAULT,
    LAUNCHES_AT_YEAR_10_DEFAULT,
    LOW_CADENCE_COST_MUSD_DEFAULT,
)
from data_center.provenance import ProvenanceCell

# -- compute_launches_per_year ----------------------------------------


def test_launches_returns_provenance_cell() -> None:
    """compute_launches_per_year returns a count-valued ProvenanceCell."""
    c = compute_launches_per_year(5)
    assert isinstance(c, ProvenanceCell)
    assert c.unit == "count"
    assert c.formula_name == "launches_per_year_from_logistic"


def test_launches_at_year_0_is_small() -> None:
    """Year 0 is clamped to zero by the first-launch-year dial."""
    v = compute_launches_per_year(0).value
    assert isinstance(v, int)
    assert v == 0


def test_launches_at_year_5_near_anchor() -> None:
    v = compute_launches_per_year(5).value
    assert isinstance(v, int)
    assert v == LAUNCHES_AT_YEAR_5_DEFAULT


def test_launches_at_year_10_near_90() -> None:
    """Year 10 is the explicit default 90-launch anchor."""
    v = compute_launches_per_year(10).value
    assert isinstance(v, int)
    assert v == LAUNCHES_AT_YEAR_10_DEFAULT


def test_launches_clamped_at_ceiling_for_very_high_year() -> None:
    v = compute_launches_per_year(100).value
    assert v == CADENCE_CEILING_DEFAULT


def test_launches_zero_for_negative_year() -> None:
    assert compute_launches_per_year(-1).value == 0


def test_launches_monotonic_increasing() -> None:
    prev = -1
    for y in range(20):
        cur = compute_launches_per_year(y).value
        assert isinstance(cur, int)
        assert cur >= prev
        prev = cur


# -- compute_launch_cost_musd -----------------------------------------


def test_launch_cost_returns_provenance_cell() -> None:
    """compute_launch_cost_musd returns a MUSD-valued ProvenanceCell."""
    c = compute_launch_cost_musd(5.0)
    assert isinstance(c, ProvenanceCell)
    assert c.unit == "MUSD"
    assert c.formula_name == "launch_cost_musd_from_cadence_log_linear"


def test_launch_cost_at_low_anchor() -> None:
    v = compute_launch_cost_musd(5.0).value
    assert v == pytest.approx(LOW_CADENCE_COST_MUSD_DEFAULT)


def test_launch_cost_at_high_anchor() -> None:
    v = compute_launch_cost_musd(100.0).value
    assert v == pytest.approx(HIGH_CADENCE_COST_MUSD_DEFAULT)


def test_launch_cost_flat_clamp_below_low_anchor() -> None:
    v = compute_launch_cost_musd(1.0).value
    assert v == pytest.approx(LOW_CADENCE_COST_MUSD_DEFAULT)


def test_launch_cost_flat_clamp_above_high_anchor() -> None:
    v = compute_launch_cost_musd(500.0).value
    assert v == pytest.approx(HIGH_CADENCE_COST_MUSD_DEFAULT)


def test_launch_cost_y10_cadence_matches_default_source_index_anchor() -> None:
    """The default y10 cadence of 90/yr prices near $13.9M/launch."""
    v = compute_launch_cost_musd(90.0).value
    assert isinstance(v, float)
    assert 13.5 < v < 14.5


def test_launch_cost_monotonic_decreasing_in_cadence() -> None:
    prev = float("inf")
    for cadence in [5, 10, 20, 50, 80, 100]:
        cur = compute_launch_cost_musd(float(cadence)).value
        assert isinstance(cur, float)
        assert cur <= prev
        prev = cur


# -- _log_interp ------------------------------------------------------


def test_log_interp_at_endpoints() -> None:
    assert _log_interp(2.0, 1.0, 10.0, 100.0, 200.0) == pytest.approx(130.103, abs=0.1)
    assert _log_interp(1.0, 1.0, 10.0, 100.0, 200.0) == 100.0
    assert _log_interp(10.0, 1.0, 10.0, 100.0, 200.0) == 200.0
