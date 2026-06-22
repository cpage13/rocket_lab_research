"""Tests pinning the communications constants to their canonical anchors (T1.9).

The comms package deliberately duplicates the year bounds (local definition,
no DC import) and consumes the eight cadence/launch-cost defaults from
common.cadence; these tests are the drift guards. They also confirm the
broadband four-area defaults land inside the V3 sanity band and the
direct-to-cell sum is strictly greater. Importing data_center.constants in a
TEST is fine: the no-data_center architecture guard is on src/, not tests.
"""

from __future__ import annotations

from common import cadence as common_cadence
from communications import constants as comms
from data_center import constants as dc

# The MUSD-per-USD conversion for the solar line (solar_cost_usd_per_kw is in
# USD per kW; the four-area sum is in MUSD).
_USD_PER_MUSD = 1e6


def _four_area_sum_musd(
    antenna_musd: float,
    comms_electronics_musd: float,
    solar_usd_per_kw: float,
    payload_power_kw: float,
    radiator_bus_musd: float,
) -> float:
    """Sum the four cost areas in MUSD (the solar line converted from USD/kW)."""
    solar_musd = solar_usd_per_kw * payload_power_kw / _USD_PER_MUSD
    return antenna_musd + comms_electronics_musd + solar_musd + radiator_bus_musd


def test_year_bounds_match_data_center() -> None:
    """The comms year bounds equal the data_center bounds (the deliberate-duplication guard)."""
    assert comms.MIN_FY == dc.MIN_FY
    assert comms.MAX_FY == dc.MAX_FY
    assert comms.MIN_HORIZON_YEARS == dc.MIN_HORIZON_YEARS
    assert comms.MAX_HORIZON_YEARS == dc.MAX_HORIZON_YEARS


def test_cadence_defaults_match_data_center() -> None:
    """The eight cadence/launch-cost defaults the comms config uses equal the DC anchors.

    The load-bearing leg is comms == data_center (the canonical DC anchor). A
    secondary leg asserts comms == common.cadence, so a Phase-0 regression that
    moved common.cadence off the DC anchors is caught here too.
    """
    pairs = [
        ("CADENCE_CEILING_DEFAULT", 150),
        ("FIRST_LAUNCH_YEAR_DEFAULT", 1),
        ("HIGH_CADENCE_COST_MUSD_DEFAULT", 13.5),
        ("HIGH_CADENCE_LAUNCHES_DEFAULT", 100.0),
        ("LAUNCHES_AT_YEAR_5_DEFAULT", 14),
        ("LAUNCHES_AT_YEAR_10_DEFAULT", 90),
        ("LOW_CADENCE_COST_MUSD_DEFAULT", 25.0),
        ("LOW_CADENCE_LAUNCHES_DEFAULT", 5.0),
    ]
    for name, expected in pairs:
        comms_value = getattr(comms, name)
        # Load-bearing: comms == data_center (the canonical anchor).
        assert comms_value == getattr(dc, name), name
        # Secondary: comms == common.cadence (the Phase-0 spine leg).
        assert comms_value == getattr(common_cadence, name), name
        # And the plan-time verified value, so an in-lockstep drift is still caught.
        assert comms_value == expected, name


def test_broadband_four_area_in_v3_band() -> None:
    """The broadband four-area sum lands inside the V3 sanity band $0.8M to $1.5M."""
    total = _four_area_sum_musd(
        comms.BROADBAND_ANTENNA_COST_MUSD_DEFAULT,
        comms.BROADBAND_COMMS_ELECTRONICS_COST_MUSD_DEFAULT,
        comms.BROADBAND_SOLAR_COST_USD_PER_KW_DEFAULT,
        comms.BROADBAND_PAYLOAD_POWER_KW_DEFAULT,
        comms.BROADBAND_RADIATOR_BUS_COST_MUSD_DEFAULT,
    )
    assert 0.8 <= total <= 1.5, f"broadband four-area sum {total} MUSD outside V3 band"


def test_direct_to_cell_costs_more_than_broadband() -> None:
    """The direct-to-cell four-area sum is strictly greater than the broadband sum."""
    broadband = _four_area_sum_musd(
        comms.BROADBAND_ANTENNA_COST_MUSD_DEFAULT,
        comms.BROADBAND_COMMS_ELECTRONICS_COST_MUSD_DEFAULT,
        comms.BROADBAND_SOLAR_COST_USD_PER_KW_DEFAULT,
        comms.BROADBAND_PAYLOAD_POWER_KW_DEFAULT,
        comms.BROADBAND_RADIATOR_BUS_COST_MUSD_DEFAULT,
    )
    direct_to_cell = _four_area_sum_musd(
        comms.DIRECT_TO_CELL_ANTENNA_COST_MUSD_DEFAULT,
        comms.DIRECT_TO_CELL_COMMS_ELECTRONICS_COST_MUSD_DEFAULT,
        comms.DIRECT_TO_CELL_SOLAR_COST_USD_PER_KW_DEFAULT,
        comms.DIRECT_TO_CELL_PAYLOAD_POWER_KW_DEFAULT,
        comms.DIRECT_TO_CELL_RADIATOR_BUS_COST_MUSD_DEFAULT,
    )
    assert direct_to_cell > broadband
