"""Tests for the communications spectrum module (comms Phase 2, T2.5).

Covers the spectrum requirement (the per-beam width, independent of beams and
satellites), the empirical capacity anchor (120 Mbps at 40 MHz, linear), the
naive cross-check (lower than the empirical anchor, the naive-division gate), and
the customer chain as a low/mid/high band: the load-bearing 50,000 / 150,000 /
300,000 per-satellite sanity target under the inverted pairing, the inverted
pairing asserted directly, the three-cells band shape (the point-estimate gate),
and the total-served scaling.
"""

from __future__ import annotations

import math

from communications.config import BandTriple, SpectrumDials
from communications.spectrum import (
    CustomerBand,
    compute_customers_per_beam_band,
    compute_customers_per_sat_band,
    compute_naive_capacity_cross_check,
    compute_per_beam_capacity,
    compute_spectrum_to_acquire,
    compute_total_served_band,
)

REL_TOL = 1e-9


def test_spectrum_to_acquire_equals_leased_bandwidth() -> None:
    """The requirement is the per-beam width, independent of beams and satellites."""
    c40 = compute_spectrum_to_acquire(SpectrumDials(leased_bandwidth_mhz=40.0), dials_path="x")
    assert c40.value == 40.0
    assert c40.unit == "MHz"
    c65 = compute_spectrum_to_acquire(SpectrumDials(leased_bandwidth_mhz=65.0), dials_path="x")
    assert c65.value == 65.0


def test_per_beam_capacity_at_anchor() -> None:
    """Empirical capacity is 120 Mbps at 40 MHz and scales linearly (240 at 80)."""
    c40 = compute_per_beam_capacity(SpectrumDials(leased_bandwidth_mhz=40.0), dials_path="x")
    assert isinstance(c40.value, float)
    assert math.isclose(c40.value, 120.0, rel_tol=REL_TOL)
    assert c40.unit == "Mbps"
    c80 = compute_per_beam_capacity(SpectrumDials(leased_bandwidth_mhz=80.0), dials_path="x")
    assert isinstance(c80.value, float)
    assert math.isclose(c80.value, 240.0, rel_tol=REL_TOL)


def test_naive_capacity_is_cross_check_only() -> None:
    """The naive figure is 24 Mbps at 40 MHz x 0.6 bps/Hz and is below the empirical."""
    dials = SpectrumDials(leased_bandwidth_mhz=40.0, spectral_efficiency_bps_per_hz=0.6)
    naive = compute_naive_capacity_cross_check(dials, dials_path="x")
    assert isinstance(naive.value, float)
    assert math.isclose(naive.value, 24.0, rel_tol=REL_TOL)
    empirical = compute_per_beam_capacity(dials, dials_path="x")
    assert isinstance(empirical.value, float)
    # The naive figure understates the engineered cell; capacity is NOT generated
    # from it.
    assert naive.value < empirical.value


def test_customer_band_reproduces_target() -> None:
    """The default bands land EXACTLY 50,000 / 150,000 / 300,000 per satellite."""
    rate = BandTriple(low=2.0, mid=3.0, high=6.0)
    oversub = BandTriple(low=1.0, mid=1.5, high=2.0)
    per_beam = compute_customers_per_beam_band(
        120.0,
        rate,
        oversub,
        capacity_path="cap",
        rate_band_path="rate",
        oversubscription_band_path="oversub",
    )
    per_sat = compute_customers_per_sat_band(
        per_beam,
        2500,
        customers_per_beam_path="cpb",
        beams_per_sat_path="beams",
    )
    assert isinstance(per_sat.low.value, float)
    assert isinstance(per_sat.mid.value, float)
    assert isinstance(per_sat.high.value, float)
    # customer low  = 2500 * (120/6.0) * 1.0 =  50,000
    # customer mid  = 2500 * (120/3.0) * 1.5 = 150,000
    # customer high = 2500 * (120/2.0) * 2.0 = 300,000
    assert math.isclose(per_sat.low.value, 50_000.0, rel_tol=REL_TOL)
    assert math.isclose(per_sat.mid.value, 150_000.0, rel_tol=REL_TOL)
    assert math.isclose(per_sat.high.value, 300_000.0, rel_tol=REL_TOL)


def test_customer_band_inverted_pairing() -> None:
    """The customer LOW uses rate.high (fattest pipe), HIGH uses rate.low (thinnest)."""
    rate = BandTriple(low=1.0, mid=2.0, high=10.0)
    oversub = BandTriple(low=1.0, mid=1.0, high=1.0)
    per_beam = compute_customers_per_beam_band(
        100.0,
        rate,
        oversub,
        capacity_path="cap",
        rate_band_path="rate",
        oversubscription_band_path="oversub",
    )
    assert isinstance(per_beam.low.value, float)
    assert isinstance(per_beam.high.value, float)
    # low  = 100 / 10.0 * 1.0 = 10 (rate.high feeds customer LOW)
    # high = 100 /  1.0 * 1.0 = 100 (rate.low feeds customer HIGH)
    assert math.isclose(per_beam.low.value, 10.0, rel_tol=REL_TOL)
    assert math.isclose(per_beam.high.value, 100.0, rel_tol=REL_TOL)


def test_customer_band_is_three_cells() -> None:
    """The customer output is a band of three distinct subs cells (not a scalar)."""
    rate = BandTriple(low=2.0, mid=3.0, high=6.0)
    oversub = BandTriple(low=1.0, mid=1.5, high=2.0)
    per_beam = compute_customers_per_beam_band(
        120.0,
        rate,
        oversub,
        capacity_path="cap",
        rate_band_path="rate",
        oversubscription_band_path="oversub",
    )
    assert isinstance(per_beam, CustomerBand)
    members = [per_beam.low, per_beam.mid, per_beam.high]
    for member in members:
        assert member.unit == "subs"
    # Three distinct cells (distinct values under an asymmetric band).
    assert len({m.value for m in members}) == 3


def test_total_served_scales_with_satellite_count() -> None:
    """Each total-served member = the per-sat member x num_satellites."""
    rate = BandTriple(low=2.0, mid=3.0, high=6.0)
    oversub = BandTriple(low=1.0, mid=1.5, high=2.0)
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
    num_satellites = 450
    total = compute_total_served_band(
        per_sat,
        num_satellites,
        customers_per_sat_path="cps",
        num_satellites_path="n",
    )
    for sat_cell, total_cell in (
        (per_sat.low, total.low),
        (per_sat.mid, total.mid),
        (per_sat.high, total.high),
    ):
        assert isinstance(sat_cell.value, float)
        assert isinstance(total_cell.value, float)
        assert math.isclose(total_cell.value, sat_cell.value * num_satellites, rel_tol=REL_TOL)
        assert total_cell.unit == "subs"
