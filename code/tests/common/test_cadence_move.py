"""Tests that the cadence machinery moved cleanly to ``common`` (Phase 0, T0.13)."""

from __future__ import annotations

from common import cadence as common_cadence
from common.cadence import compute_launch_cost_musd, compute_launches_per_year
from data_center import constants as dc_constants


def test_cadence_defaults_match_data_center_constants() -> None:
    # The eight cadence/launch-cost defaults are deliberately duplicated: defined
    # locally in common.cadence and (unchanged) in data_center.constants. This is
    # the guard that the verbatim copy did not drift (P0.2 move 3).
    names = (
        "CADENCE_CEILING_DEFAULT",
        "FIRST_LAUNCH_YEAR_DEFAULT",
        "HIGH_CADENCE_COST_MUSD_DEFAULT",
        "HIGH_CADENCE_LAUNCHES_DEFAULT",
        "LAUNCHES_AT_YEAR_5_DEFAULT",
        "LAUNCHES_AT_YEAR_10_DEFAULT",
        "LOW_CADENCE_COST_MUSD_DEFAULT",
        "LOW_CADENCE_LAUNCHES_DEFAULT",
    )
    for name in names:
        assert getattr(common_cadence, name) == getattr(dc_constants, name), name


def test_launches_per_year_year_zero_is_zero() -> None:
    assert compute_launches_per_year(0).value == 0


def test_launches_per_year_is_integer() -> None:
    result = compute_launches_per_year(8)
    assert isinstance(result.value, int)
    assert result.unit == "count"


def test_launch_cost_is_provenance_cell() -> None:
    result = compute_launch_cost_musd(50)
    assert isinstance(result.value, float)
    assert result.unit == "MUSD"
    assert result.formula_name == "launch_cost_musd_from_cadence_log_linear"
