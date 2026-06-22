"""Tests locking the communications config default values (T1.6).

These pin the central-case defaults the schema reproduces with no arguments,
so a silent drift in a constant or a builder is caught.
"""

from __future__ import annotations

from communications.config import (
    CommsConfig,
    ConstellationDials,
    CostDownDials,
    GroundDials,
    LaunchDials,
    MetadataDials,
    PriceReferenceDials,
    SatelliteClassDials,
    ScenarioLevers,
    SpectrumDials,
)
from communications.constants import LEARNING_RATE_PER_DOUBLING_DEFAULT


def test_default_construct_succeeds() -> None:
    """CommsConfig() constructs with no arguments (every default_factory yields a valid block)."""
    cfg = CommsConfig()
    assert isinstance(cfg, CommsConfig)


def test_default_blocks_present() -> None:
    """The constructed config has all eight blocks of their expected types."""
    cfg = CommsConfig()
    assert isinstance(cfg.metadata, MetadataDials)
    assert isinstance(cfg.constellation, ConstellationDials)
    assert isinstance(cfg.launch, LaunchDials)
    assert isinstance(cfg.cost_down, CostDownDials)
    assert isinstance(cfg.spectrum, SpectrumDials)
    assert isinstance(cfg.price_reference, PriceReferenceDials)
    assert isinstance(cfg.ground, GroundDials)
    assert isinstance(cfg.scenario_levers, ScenarioLevers)


def test_metadata_defaults() -> None:
    """base_year, horizon_years, steady_state_year are 2026 / 10 / 2036."""
    meta = CommsConfig().metadata
    assert meta.base_year == 2026
    assert meta.horizon_years == 10
    assert meta.steady_state_year == 2036


def test_satellite_lifetime_default_is_five() -> None:
    """The service-life cliff defaults to 5 years (plan Section 0.8: 5 default, NOT 3)."""
    assert CommsConfig().constellation.satellite_lifetime_years == 5


def test_two_satellite_classes_present() -> None:
    """Both classes are present and direct-to-cell is antenna-heavy and volume-larger."""
    constellation = CommsConfig().constellation
    assert isinstance(constellation.broadband, SatelliteClassDials)
    assert isinstance(constellation.direct_to_cell, SatelliteClassDials)
    # The per-class fork at config level: direct-to-cell is antenna-heavy and
    # volume-bound, so its antenna cost and stowed volume strictly exceed broadband's.
    broadband = constellation.broadband
    direct_to_cell = constellation.direct_to_cell
    assert direct_to_cell.antenna_cost_musd > broadband.antenna_cost_musd
    assert direct_to_cell.stowed_volume_m3 > broadband.stowed_volume_m3


def test_spectrum_defaults() -> None:
    """leased_bandwidth_mhz / beams_per_sat / spectral_efficiency are 40.0 / 2500 / 0.6."""
    spectrum = CommsConfig().spectrum
    assert spectrum.leased_bandwidth_mhz == 40.0
    assert spectrum.beams_per_sat == 2500
    assert spectrum.spectral_efficiency_bps_per_hz == 0.6


def test_band_defaults_stored_ascending() -> None:
    """The two band triples store ascending magnitudes (2/3/6 Mbps, 1/1.5/2 oversub)."""
    spectrum = CommsConfig().spectrum
    rate = spectrum.target_per_user_rate_mbps
    oversub = spectrum.oversubscription_factor
    assert (rate.low, rate.mid, rate.high) == (2.0, 3.0, 6.0)
    assert (oversub.low, oversub.mid, oversub.high) == (1.0, 1.5, 2.0)


def test_retail_reference_default_is_hundred() -> None:
    """The founder-set retail reference defaults to $100/month."""
    assert CommsConfig().price_reference.retail_reference_usd_per_month == 100.0


def test_high_cadence_cost_default() -> None:
    """The high-cadence launch cost defaults to $13.5M (the target-cadence Neutron flight)."""
    assert CommsConfig().launch.high_cadence_cost_musd == 13.5


def test_cost_down_rate_in_unit_range() -> None:
    """The learning rate is in [0, 1) and equals its named default."""
    rate = CommsConfig().cost_down.learning_rate_per_doubling
    assert 0.0 <= rate < 1.0
    assert rate == LEARNING_RATE_PER_DOUBLING_DEFAULT
