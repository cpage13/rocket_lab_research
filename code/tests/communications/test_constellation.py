"""Tests for the communications constellation module (comms Phase 2, T2.3).

Covers the four-area cost-out and the V3 cross-check band, the per-class
satellites-per-launch FORK (broadband mass-bound, direct-to-cell
antenna-stow-bound: the disaster gate), the cadence-indexed per-satellite launch
cost, the Wright-style learning-curve cost-down, the V4 capability step, the
total and annualized per-satellite cost, and the cohort service-life cliff.

Cell values are read DIRECTLY off ``c.value`` (the DC test idiom), with
``math.isclose`` / ``pytest.approx`` for floats and exact ``==`` for integer
counts and enum strings. The ``USD_PER_MUSD`` drift test pins the comms unit
conversion to the data-center value (importing data_center in a TEST is allowed;
the architecture guard is on src/).
"""

from __future__ import annotations

import math

import pytest

from common.cadence import compute_launch_cost_musd
from communications.config import ConstellationDials, LaunchDials
from communications.constants import USD_PER_MUSD
from communications.constellation import (
    SatelliteBindingConstraint,
    SatelliteCohort,
    compute_capability_after_v4_step,
    compute_launch_cost_per_satellite,
    compute_learning_curve_multiplier,
    compute_satellite_build_cost,
    compute_satellite_build_cost_after_learning,
    compute_satellite_cost_annual,
    compute_satellite_cost_breakdown,
    compute_satellite_total_cost,
    compute_satellites_per_launch,
)
from data_center.constants import USD_PER_MUSD as DC_USD_PER_MUSD

REL_TOL = 1e-9


def _broadband() -> ConstellationDials:
    """The default constellation dials (broadband + direct-to-cell defaults)."""
    return ConstellationDials()


def _launch() -> LaunchDials:
    """The default launch dials (cadence + Neutron-envelope defaults)."""
    return LaunchDials()


def test_usd_per_musd_matches_data_center() -> None:
    """The comms USD_PER_MUSD conversion equals the data-center value (drift guard)."""
    assert USD_PER_MUSD == DC_USD_PER_MUSD
    assert USD_PER_MUSD == 1_000_000.0


def test_four_area_breakdown_sums_to_class_cost() -> None:
    """Build cost = antenna + comms + solar(USD->$M) + radiator/bus + minor carry."""
    dials = _broadband().broadband
    breakdown = compute_satellite_cost_breakdown(dials, class_name="broadband", dials_path="x")
    build = compute_satellite_build_cost(breakdown, breakdown_path="x")
    solar_musd = dials.solar_cost_usd_per_kw * dials.payload_power_kw / USD_PER_MUSD
    four_area = (
        dials.antenna_cost_musd
        + dials.comms_electronics_cost_musd
        + solar_musd
        + dials.radiator_bus_cost_musd
    )
    expected = four_area + dials.minor_component_pct * four_area
    assert isinstance(build.value, float)
    assert math.isclose(build.value, expected, rel_tol=REL_TOL)
    assert build.unit == "MUSD"
    # The solar line is the USD->$M conversion, not the raw USD/kW dial.
    assert isinstance(breakdown.solar.value, float)
    assert math.isclose(breakdown.solar.value, solar_musd, rel_tol=REL_TOL)


def test_broadband_four_area_in_v3_band() -> None:
    """The broadband build cost (before launch) lands in the V3 band $0.8M to $1.5M."""
    dials = _broadband().broadband
    breakdown = compute_satellite_cost_breakdown(dials, class_name="broadband", dials_path="x")
    build = compute_satellite_build_cost(breakdown, breakdown_path="x")
    assert isinstance(build.value, float)
    assert 0.8 <= build.value <= 1.5, f"broadband build {build.value} MUSD outside V3 band"


def test_satellites_per_launch_broadband_mass_bound() -> None:
    """Broadband binds on MASS, count = floor(mass_envelope_t / satellite_mass_t)."""
    constellation = _broadband()
    launch = _launch()
    packing = compute_satellites_per_launch(
        constellation.broadband,
        mass_envelope_t=launch.neutron_mass_envelope_t,
        fairing_volume_m3=launch.neutron_fairing_volume_m3,
        class_name="broadband",
        dials_path="x",
        launch_dials_path="y",
    )
    expected_mass = math.floor(
        launch.neutron_mass_envelope_t / constellation.broadband.satellite_mass_t
    )
    assert packing.binding_constraint.value == SatelliteBindingConstraint.MASS.value
    assert packing.satellites_per_launch.value == expected_mass
    assert packing.mass_bound_count.value == expected_mass
    # Mass is the tighter-or-equal envelope for broadband.
    assert isinstance(packing.mass_bound_count.value, int)
    assert isinstance(packing.volume_bound_count.value, int)
    assert packing.mass_bound_count.value <= packing.volume_bound_count.value


def test_satellites_per_launch_direct_to_cell_volume_bound() -> None:
    """Direct-to-cell binds on ANTENNA_STOW, count = floor(fairing / stowed)."""
    constellation = _broadband()
    launch = _launch()
    packing = compute_satellites_per_launch(
        constellation.direct_to_cell,
        mass_envelope_t=launch.neutron_mass_envelope_t,
        fairing_volume_m3=launch.neutron_fairing_volume_m3,
        class_name="direct_to_cell",
        dials_path="x",
        launch_dials_path="y",
    )
    expected_volume = math.floor(
        launch.neutron_fairing_volume_m3 / constellation.direct_to_cell.stowed_volume_m3
    )
    assert packing.binding_constraint.value == SatelliteBindingConstraint.ANTENNA_STOW.value
    assert packing.satellites_per_launch.value == expected_volume
    assert packing.volume_bound_count.value == expected_volume
    # Volume is the tighter envelope for direct-to-cell (and is about 1).
    assert isinstance(packing.volume_bound_count.value, int)
    assert isinstance(packing.mass_bound_count.value, int)
    assert packing.volume_bound_count.value < packing.mass_bound_count.value
    assert packing.satellites_per_launch.value == 1


def test_launch_cost_per_satellite_divides_cadence_cost() -> None:
    """Per-satellite launch cost = cadence launch cost / satellites_per_launch."""
    launch = _launch()
    launches_per_year = 90
    satellites_per_launch = 5
    per_sat = compute_launch_cost_per_satellite(
        satellites_per_launch,
        launches_per_year=launches_per_year,
        launch_dials=launch,
        dials_path="inputs.config.launch",
        satellites_per_launch_path="z",
    )
    launch_cost = compute_launch_cost_musd(
        launches_per_year,
        dials_path="inputs.config.launch",
        low_cadence_cost_musd=launch.low_cadence_cost_musd,
        high_cadence_cost_musd=launch.high_cadence_cost_musd,
        low_cadence_launches=launch.low_cadence_launches,
        high_cadence_launches=launch.high_cadence_launches,
    )
    assert isinstance(launch_cost.value, float)
    assert isinstance(per_sat.value, float)
    assert math.isclose(per_sat.value, launch_cost.value / satellites_per_launch, rel_tol=REL_TOL)


def test_launch_cost_per_satellite_raises_on_zero() -> None:
    """A non-positive satellites_per_launch raises ValueError."""
    launch = _launch()
    with pytest.raises(ValueError, match="satellites_per_launch must be positive"):
        compute_launch_cost_per_satellite(
            0,
            launches_per_year=90,
            launch_dials=launch,
            dials_path="x",
            satellites_per_launch_path="z",
        )


def test_learning_curve_multiplier_is_one_at_reference() -> None:
    """At cumulative_units == reference_units the multiplier is 1.0 for any rate."""
    c = compute_learning_curve_multiplier(
        10,
        learning_rate_per_doubling=0.2,
        reference_units=10,
        cost_down_path="x",
    )
    assert isinstance(c.value, float)
    assert math.isclose(c.value, 1.0, rel_tol=REL_TOL)
    assert c.unit == "multiplier"


def test_learning_curve_multiplier_is_one_at_zero_rate() -> None:
    """At learning_rate_per_doubling == 0.0 the multiplier is 1.0 for any count."""
    c = compute_learning_curve_multiplier(
        128,
        learning_rate_per_doubling=0.0,
        reference_units=1,
        cost_down_path="x",
    )
    assert isinstance(c.value, float)
    assert math.isclose(c.value, 1.0, rel_tol=REL_TOL)


def test_learning_curve_multiplier_halves_per_doublings() -> None:
    """At a 50% reduction per doubling, the multiplier halves at each doubling."""
    at_2x = compute_learning_curve_multiplier(
        2, learning_rate_per_doubling=0.5, reference_units=1, cost_down_path="x"
    )
    at_4x = compute_learning_curve_multiplier(
        4, learning_rate_per_doubling=0.5, reference_units=1, cost_down_path="x"
    )
    assert isinstance(at_2x.value, float)
    assert isinstance(at_4x.value, float)
    assert math.isclose(at_2x.value, 0.5, rel_tol=REL_TOL)
    assert math.isclose(at_4x.value, 0.25, rel_tol=REL_TOL)


def test_learning_curve_multiplier_raises_on_bad_inputs() -> None:
    """Non-positive counts or an out-of-range rate raise ValueError."""
    with pytest.raises(ValueError, match="cumulative_units must be positive"):
        compute_learning_curve_multiplier(
            0, learning_rate_per_doubling=0.1, reference_units=1, cost_down_path="x"
        )
    with pytest.raises(ValueError, match="reference_units must be positive"):
        compute_learning_curve_multiplier(
            10, learning_rate_per_doubling=0.1, reference_units=0, cost_down_path="x"
        )
    with pytest.raises(ValueError, match="learning_rate_per_doubling must be in"):
        compute_learning_curve_multiplier(
            10, learning_rate_per_doubling=1.0, reference_units=1, cost_down_path="x"
        )


def test_build_cost_after_learning_applies_multiplier() -> None:
    """The discounted build cost is build_cost x learning_multiplier."""
    c = compute_satellite_build_cost_after_learning(
        1.2, 0.9, build_cost_path="x", learning_multiplier_path="y"
    )
    assert isinstance(c.value, float)
    assert math.isclose(c.value, 1.2 * 0.9, rel_tol=REL_TOL)
    assert c.unit == "MUSD"


def test_satellite_total_cost_is_build_plus_launch() -> None:
    """Total per-satellite cost = discounted build cost + per-satellite launch cost."""
    c = compute_satellite_total_cost(1.08, 2.6, build_cost_path="x", launch_cost_path="y")
    assert isinstance(c.value, float)
    assert math.isclose(c.value, 1.08 + 2.6, rel_tol=REL_TOL)
    assert c.unit == "MUSD"


def test_satellite_cost_annual_spreads_over_life() -> None:
    """Annualized cost = total / lifetime, and 0.0 for a non-positive lifetime."""
    c = compute_satellite_cost_annual(3.68, 5, satellite_total_path="x", lifetime_path="y")
    assert isinstance(c.value, float)
    assert math.isclose(c.value, 3.68 / 5, rel_tol=REL_TOL)
    zero = compute_satellite_cost_annual(3.68, 0, satellite_total_path="x", lifetime_path="y")
    assert zero.value == 0.0


def test_capability_after_v4_step_default_is_identity() -> None:
    """A V4 multiplier of 1.0 leaves the base capability unchanged (the default)."""
    c = compute_capability_after_v4_step(
        120.0,
        1.0,
        base_capability_path="x",
        multiplier_path="y",
        capability_unit="Mbps",
    )
    assert isinstance(c.value, float)
    assert math.isclose(c.value, 120.0, rel_tol=REL_TOL)
    assert c.unit == "Mbps"
    stepped = compute_capability_after_v4_step(
        120.0,
        1.5,
        base_capability_path="x",
        multiplier_path="y",
        capability_unit="Mbps",
    )
    assert isinstance(stepped.value, float)
    assert math.isclose(stepped.value, 180.0, rel_tol=REL_TOL)


def test_satellite_cohort_cliff() -> None:
    """The cohort survival cliff is half-open [launch_year, launch_year + life)."""
    cohort = SatelliteCohort(
        launch_year=2030,
        satellites_deployed=50,
        cost_annual_per_satellite_musd=0.7,
        customers_per_sat_low=50_000.0,
        customers_per_sat_mid=150_000.0,
        customers_per_sat_high=300_000.0,
    )
    assert cohort.is_alive_at(2030, 5) is True
    assert cohort.is_alive_at(2034, 5) is True
    assert cohort.is_alive_at(2035, 5) is False
    assert cohort.is_alive_at(2029, 5) is False
