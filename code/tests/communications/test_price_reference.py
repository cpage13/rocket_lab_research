"""Tests for the communications price-reference module (comms Phase 2, T2.7).

RENAMED from ``test_demand`` by plan Section 0.0 Amendment A1 (the module is
``price_reference``, not ``demand``). Covers the priced per-customer revenue
(cost x 1.5), the ARPU-collectable ceiling (arpu x 12 x share), the
priced-may-exceed-ceiling documentation case (the reconciliation is Phase 4's
job, no clamping here), the scope split summing to the total, the bad-region
guard, and a formula-key smoke test that every formula_name the three Phase-2
modules emit is registered in ``common.provenance.FORMULAS``.

A1 deletes the market-size projection machinery, so there is NO
``test_market_size_grows_at_rate`` and NO ``compute_market_size_at_year`` to
test: a market-size projection with a growth dial is demand modeling, and demand
is assumed, not modeled.
"""

from __future__ import annotations

import math

import pytest

from common.provenance import FORMULAS
from communications.config import PriceReferenceDials, ScopeWeights
from communications.constants import MONTHS_PER_YEAR, REVENUE_MULTIPLE
from communications.price_reference import (
    compute_arpu_collectable_revenue,
    compute_priced_cost_per_customer,
    compute_scope_weighted_customers,
)

REL_TOL = 1e-9


def test_priced_cost_is_cost_times_multiple() -> None:
    """The priced cost is the per-customer cost times REVENUE_MULTIPLE (1.5)."""
    cost = 240.0
    c = compute_priced_cost_per_customer(cost, cost_path="x")
    assert isinstance(c.value, float)
    assert math.isclose(c.value, cost * REVENUE_MULTIPLE, rel_tol=REL_TOL)
    assert c.unit == "USD"


def test_arpu_collectable_is_arpu_times_share() -> None:
    """The collectable revenue is arpu x 12 x operator_revenue_share (300 USD/yr)."""
    dials = PriceReferenceDials(arpu_usd_per_month=50.0, operator_revenue_share=0.5)
    c = compute_arpu_collectable_revenue(dials, dials_path="x")
    assert isinstance(c.value, float)
    assert math.isclose(c.value, 50.0 * MONTHS_PER_YEAR * 0.5, rel_tol=REL_TOL)
    assert math.isclose(c.value, 300.0, rel_tol=REL_TOL)
    assert c.unit == "USD"


def test_priced_cost_can_exceed_arpu_ceiling() -> None:
    """The priced cost MAY exceed the ARPU ceiling; Phase 2 does NOT clamp it.

    The two cells are the two faces of the Phase-4 revenue-ceiling
    reconciliation; this module returns both raw, with no clamping (the
    reconciliation that compares them is Phase 4's job).
    """
    # A per-customer cost whose 1.5x priced figure exceeds the collectable ceiling.
    dials = PriceReferenceDials(arpu_usd_per_month=50.0, operator_revenue_share=0.5)
    collectable = compute_arpu_collectable_revenue(dials, dials_path="x")
    high_cost = 1000.0
    priced = compute_priced_cost_per_customer(high_cost, cost_path="y")
    assert isinstance(priced.value, float)
    assert isinstance(collectable.value, float)
    # Both return their raw values; priced is NOT clamped to the ceiling here.
    assert math.isclose(priced.value, high_cost * REVENUE_MULTIPLE, rel_tol=REL_TOL)
    assert priced.value > collectable.value


def test_scope_weighted_customers_sum_to_total() -> None:
    """The three regional cells sum to total_served (the weights sum to 1)."""
    scope = ScopeWeights(us=0.5, europe=0.3, asia_ex_china=0.2)
    total = 1_350_000.0
    cells = [
        compute_scope_weighted_customers(
            total,
            scope,
            region=region,
            total_served_path="t",
            scope_path="s",
        )
        for region in ("us", "europe", "asia_ex_china")
    ]
    values = [c.value for c in cells]
    for v in values:
        assert isinstance(v, float)
    assert math.isclose(sum(values), total, rel_tol=REL_TOL)  # type: ignore[arg-type]
    assert cells[0].unit == "subs"


def test_scope_weighted_customers_raises_on_bad_region() -> None:
    """An unknown region string raises ValueError (the enum-like guard)."""
    scope = ScopeWeights(us=0.5, europe=0.3, asia_ex_china=0.2)
    with pytest.raises(ValueError, match="region must be one of"):
        compute_scope_weighted_customers(
            1.0,
            scope,
            region="antarctica",
            total_served_path="t",
            scope_path="s",
        )


def test_all_phase2_formula_names_registered() -> None:
    """Every formula_name the three Phase-2 modules emit is present in FORMULAS.

    Mirrors the DC provenance-uses discipline: build one cell of each kind and
    confirm its formula_name resolves through the table, so a forgotten FORMULAS
    append is caught here (before the Phase-5 V13-analog does).
    """
    from communications.config import (  # local import to keep the test self-contained
        BandTriple,
        ConstellationDials,
        LaunchDials,
    )
    from communications.constellation import (
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
    from communications.spectrum import (
        compute_customers_per_beam_band,
        compute_customers_per_sat_band,
        compute_naive_capacity_cross_check,
        compute_per_beam_capacity,
        compute_spectrum_to_acquire,
        compute_total_served_band,
    )

    constellation = ConstellationDials()
    launch = LaunchDials()
    dials = constellation.broadband

    breakdown = compute_satellite_cost_breakdown(dials, class_name="broadband", dials_path="x")
    build = compute_satellite_build_cost(breakdown, breakdown_path="x")
    packing = compute_satellites_per_launch(
        dials,
        mass_envelope_t=launch.neutron_mass_envelope_t,
        fairing_volume_m3=launch.neutron_fairing_volume_m3,
        class_name="broadband",
        dials_path="x",
        launch_dials_path="y",
    )
    launch_cost = compute_launch_cost_per_satellite(
        5,
        launches_per_year=90,
        launch_dials=launch,
        dials_path="x",
        satellites_per_launch_path="z",
    )
    learning = compute_learning_curve_multiplier(
        2, learning_rate_per_doubling=0.1, reference_units=1, cost_down_path="x"
    )
    discounted = compute_satellite_build_cost_after_learning(
        1.2, 0.9, build_cost_path="x", learning_multiplier_path="y"
    )
    capability = compute_capability_after_v4_step(
        120.0, 1.0, base_capability_path="x", multiplier_path="y", capability_unit="Mbps"
    )
    total = compute_satellite_total_cost(1.08, 2.6, build_cost_path="x", launch_cost_path="y")
    annual = compute_satellite_cost_annual(3.68, 5, satellite_total_path="x", lifetime_path="y")

    spectrum_dials = constellation_spectrum_dials()
    rate = BandTriple(low=2.0, mid=3.0, high=6.0)
    oversub = BandTriple(low=1.0, mid=1.5, high=2.0)
    to_acquire = compute_spectrum_to_acquire(spectrum_dials, dials_path="x")
    per_beam_cap = compute_per_beam_capacity(spectrum_dials, dials_path="x")
    naive = compute_naive_capacity_cross_check(spectrum_dials, dials_path="x")
    per_beam = compute_customers_per_beam_band(
        120.0,
        rate,
        oversub,
        capacity_path="cap",
        rate_band_path="rate",
        oversubscription_band_path="oversub",
    )
    per_sat = compute_customers_per_sat_band(
        per_beam, 2500, customers_per_beam_path="cpb", beams_per_sat_path="beams"
    )
    served = compute_total_served_band(
        per_sat, 100, customers_per_sat_path="cps", num_satellites_path="n"
    )

    price_dials = PriceReferenceDials()
    priced = compute_priced_cost_per_customer(240.0, cost_path="x")
    collectable = compute_arpu_collectable_revenue(price_dials, dials_path="x")
    scoped = compute_scope_weighted_customers(
        1.0, price_dials.scope, region="us", total_served_path="t", scope_path="s"
    )

    single_cells = [
        build,
        packing.satellites_per_launch,
        packing.binding_constraint,
        packing.mass_bound_count,
        packing.volume_bound_count,
        breakdown.antenna,
        breakdown.comms_electronics,
        breakdown.solar,
        breakdown.radiator_bus,
        breakdown.minor_component,
        launch_cost,
        learning,
        discounted,
        capability,
        total,
        annual,
        to_acquire,
        per_beam_cap,
        naive,
        priced,
        collectable,
        scoped,
    ]
    band_cells = [
        per_beam.low,
        per_beam.mid,
        per_beam.high,
        per_sat.low,
        per_sat.mid,
        per_sat.high,
        served.low,
        served.mid,
        served.high,
    ]
    for c in [*single_cells, *band_cells]:
        assert c.formula_name in FORMULAS, c.formula_name


def constellation_spectrum_dials():  # type: ignore[no-untyped-def]
    """Return a default SpectrumDials (a tiny test helper kept out of the test body)."""
    from communications.config import SpectrumDials

    return SpectrumDials()
