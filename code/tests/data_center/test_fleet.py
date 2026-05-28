"""Tests for fleet module.

The fleet rollup (cycle-2 Phase 3) vintages cohorts under the 5-year
hard cliff (D1) and aggregates per-node economics across the living set
at low / central / high R. These tests pin the cliff arithmetic, the
R-band interpolation, and the per-year rollup with hand-computed values.
"""

from __future__ import annotations

import pytest

from data_center.config import RBand, YearRValue
from data_center.fleet import (
    Cohort,
    _r_at_year,  # noqa: PLC2701 — private helper under test
    compute_fleet_year,
    r_at_year,
)


def _make_cohort(year: int, nodes: int = 10) -> Cohort:
    """Build a uniform test cohort: 10 nodes, R band 12/15/18 $M per node."""
    return Cohort(
        launch_year=year,
        nodes_deployed=nodes,
        frontier_generation="B200",
        kw_per_node=200.0,
        pf_per_node=1000.0,
        cost_annual_per_node_musd=10.0,
        rev_per_node_musd_central=15.0,
        rev_per_node_musd_low=12.0,
        rev_per_node_musd_high=18.0,
    )


# -- Cohort cliff ------------------------------------------------------


def test_cohort_alive_at_launch_year() -> None:
    """A cohort is alive in its launch year."""
    c = _make_cohort(2026)
    assert c.is_alive_at(2026)


def test_cohort_alive_at_year_4_after_launch() -> None:
    """A cohort is alive 4 years after launch (last live year)."""
    c = _make_cohort(2026)
    assert c.is_alive_at(2030)


def test_cohort_dead_at_year_5_after_launch() -> None:
    """A cohort is dead 5 years after launch (the hard cliff, D1)."""
    c = _make_cohort(2026)
    assert not c.is_alive_at(2031)


def test_cohort_dead_before_launch() -> None:
    """A cohort is not alive before its launch year."""
    c = _make_cohort(2026)
    assert not c.is_alive_at(2025)


# -- R-band interpolation ---------------------------------------------


def test_r_at_year_at_anchor() -> None:
    """R equals the anchor value exactly at an anchor year."""
    anchors = [YearRValue(fy=2026, r=1.50), YearRValue(fy=2036, r=1.30)]
    assert _r_at_year(anchors, 2026) == 1.50
    assert _r_at_year(anchors, 2036) == 1.30


def test_r_at_year_interpolated() -> None:
    """R is linearly interpolated between adjacent anchors."""
    anchors = [YearRValue(fy=2026, r=1.50), YearRValue(fy=2036, r=1.30)]
    # 2031 is midway -> R = 1.40
    assert _r_at_year(anchors, 2031) == pytest.approx(1.40)


def test_r_at_year_clamps_before_first_anchor() -> None:
    """R clamps flat to the first anchor below the anchor range."""
    anchors = [YearRValue(fy=2026, r=1.50), YearRValue(fy=2036, r=1.30)]
    assert _r_at_year(anchors, 2020) == 1.50


def test_r_at_year_clamps_after_last_anchor() -> None:
    """R clamps flat to the last anchor above the anchor range."""
    anchors = [YearRValue(fy=2026, r=1.50), YearRValue(fy=2036, r=1.30)]
    assert _r_at_year(anchors, 2050) == 1.30


def test_r_at_year_band_returns_triple() -> None:
    """r_at_year returns (central, low, high) from the default R band."""
    central, low, high = r_at_year(RBand(), 2026)
    assert (central, low, high) == (1.50, 1.20, 1.80)


# -- Fleet-year rollup ------------------------------------------------


def test_fleet_year_single_cohort() -> None:
    """One cohort: living fleet and central revenue match the cohort."""
    cohorts = [_make_cohort(2026, nodes=10)]
    fy = compute_fleet_year(
        2026,
        cohorts,
        launches_this_year=10,
        launch_cost_musd=25.0,
        prev_cumulative_revenue_central_musd=0.0,
        year_path='business.years."2026"',
    )
    assert fy.living_fleet.value == 10
    assert fy.launches.value == 10
    assert fy.nodes_deployed_this_year.value == 10
    assert fy.revenue_annual_fleet_musd_central.value == 150.0  # 10 x 15


def test_fleet_year_rejects_fractional_launch_count() -> None:
    """Fleet rollups accept only whole-number mission counts."""
    with pytest.raises(TypeError):
        compute_fleet_year(2026, [], 10.5, 25.0, 0.0, year_path="x")


def test_fleet_year_living_count_under_5y_cliff() -> None:
    """In 2031, cohorts 2027-2031 are alive; 2026 has dropped (D1)."""
    cohorts = [_make_cohort(y, nodes=10) for y in range(2026, 2032)]
    fy = compute_fleet_year(
        2031,
        cohorts,
        launches_this_year=10,
        launch_cost_musd=15.0,
        prev_cumulative_revenue_central_musd=0.0,
        year_path="x",
    )
    assert fy.living_fleet.value == 50  # 5 cohorts x 10 nodes


def test_fleet_year_cohort_2026_drops_in_2031() -> None:
    """5y cliff: cohort 2026 is alive 2026..2030 (5 years), dead 2031."""
    cohorts = [_make_cohort(2026, nodes=10)]
    fy_2030 = compute_fleet_year(2030, cohorts, 0, 25.0, 0.0, year_path="x")
    fy_2031 = compute_fleet_year(2031, cohorts, 0, 25.0, 0.0, year_path="x")
    assert fy_2030.living_fleet.value == 10
    assert fy_2031.living_fleet.value == 0


def test_fleet_year_revenue_band_low_central_high() -> None:
    """Fleet revenue scales each cohort's per-node R-band triple."""
    cohorts = [_make_cohort(2026, nodes=10)]
    fy = compute_fleet_year(2026, cohorts, 10, 25.0, 0.0, year_path="x")
    # Per cohort: rev_low=12, central=15, high=18 -> x10
    assert fy.revenue_annual_fleet_musd_low.value == 120.0
    assert fy.revenue_annual_fleet_musd_central.value == 150.0
    assert fy.revenue_annual_fleet_musd_high.value == 180.0


def test_fleet_year_margin_central() -> None:
    """Central margin = (revenue - cost) / revenue x 100."""
    cohorts = [_make_cohort(2026, nodes=10)]
    fy = compute_fleet_year(2026, cohorts, 10, 25.0, 0.0, year_path="x")
    # Revenue 150, Cost 100, GP 50, Margin 33.3%
    assert fy.margin_central_pct.value == pytest.approx(33.333, abs=0.1)


def test_fleet_year_cumulative_revenue_central() -> None:
    """Cumulative central revenue extends the prior-year running total."""
    cohorts = [_make_cohort(2026, nodes=10)]
    fy_2027 = compute_fleet_year(
        2027,
        cohorts,
        0,
        25.0,
        prev_cumulative_revenue_central_musd=150.0,
        year_path="x",
    )
    # 150 + (10x15) = 300
    assert fy_2027.revenue_cumulative_musd_central.value == 300.0


def test_fleet_year_cumulative_revenue_low_and_high() -> None:
    """F5 regression — cumulative low/high computed, not just central."""
    cohorts = [_make_cohort(2026, nodes=10)]
    fy = compute_fleet_year(
        2027,
        cohorts,
        0,
        25.0,
        prev_cumulative_revenue_central_musd=150.0,
        prev_cumulative_revenue_low_musd=120.0,
        prev_cumulative_revenue_high_musd=180.0,
        year_path="x",
    )
    # low: 120 + 10x12 = 240 ; high: 180 + 10x18 = 360
    assert fy.revenue_cumulative_musd_low.value == 240.0
    assert fy.revenue_cumulative_musd_high.value == 360.0


def test_fleet_year_kw_on_orbit_sums_cohorts() -> None:
    """kW on orbit sums every living cohort's nodes x kw_per_node."""
    cohorts = [_make_cohort(2026, nodes=10), _make_cohort(2027, nodes=5)]
    fy = compute_fleet_year(2027, cohorts, 5, 25.0, 0.0, year_path="x")
    # 10 x 200 + 5 x 200 = 3000 kW
    assert fy.kw_on_orbit.value == 3000.0


def test_fleet_year_empty_cohort_history() -> None:
    """No cohorts: living fleet 0, revenue 0, margin 0 (no divide-by-zero)."""
    fy = compute_fleet_year(
        2026,
        [],
        launches_this_year=0,
        launch_cost_musd=25.0,
        prev_cumulative_revenue_central_musd=0.0,
        year_path="x",
    )
    assert fy.living_fleet.value == 0
    assert fy.revenue_annual_fleet_musd_central.value == 0.0
    assert fy.margin_central_pct.value == 0.0
