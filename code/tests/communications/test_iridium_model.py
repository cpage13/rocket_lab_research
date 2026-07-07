"""Tests for Model B (the Iridium L-band max-outcome scenario, the MSS lane).

These cover the additive Model B path: the pure L-band derivations (spectral
efficiency from the device class, per-satellite capacity with the aperture factor,
the derived per-satellite subscriber density, the per-user peak/off-peak rates, the
aperture-coupled effective satellites-per-launch), the end-to-end engine run behind
the ``config.iridium`` branch, the minimal scenario YAML the existing loader parses
unchanged, and the stated-assumptions accessor.

Two structural facts anchor the suite. First, Model A is untouched: the default
config (no ``iridium`` block) still yields ``trajectory.iridium is None`` and every
Model A number is unchanged. Second, THE STRONG EQUALITY CHECK: because the Model B
phone-class baseline and the Model A default 10M run BOTH bind at the 340 coverage
floor, and at the default 25 m^2 aperture the effective satellites-per-launch equals
the configured 12 (the launch-coupling identity), their entire cost / cohort /
revenue trajectories are IDENTICAL; only the per-satellite density and the new
Iridium physics block differ. The 60 m^2 what-if breaks that identity by design (the
launch granularity changes), so it freezes the derived physics and the fleet target
only, not the deployment-year or cost outcomes.

Subscribers are PEOPLE; ``iot_devices`` is a separate DEVICE passthrough, never
folded into the people count. Model B is the MSS lane (purpose-built or in-chipset
devices on owned L-band), never the cellular unmodified-phone lane (Model A).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from communications.config import CommsConfig, IridiumDials, load_comms_config
from communications.constants import (
    APERTURE_FOLD_CAVEAT_NOTE,
    BASE_YEAR_DEFAULT,
    ECOSYSTEM_ASSUMPTION_NOTE,
    HORIZON_YEARS_DEFAULT,
    IRIDIUM_SCENARIO_NAME_DEFAULT,
    SUBSCRIBERS_PER_SATELLITE_DEFAULT,
    BindingRegime,
    DeviceClass,
)
from communications.engine import (
    derive_iridium_per_user_rates,
    derive_iridium_satellites_per_launch,
    derive_iridium_subscribers_per_satellite,
    derive_per_satellite_capacity_gbps,
    iridium_assumptions,
    resolve_device_spectral_efficiency,
    run_comms_model,
)

# ---------------------------------------------------------------------------
# The frozen Model B phone-class baseline (spectrum 8.0, aperture 25.0, phone_class,
# SE 0.65, active 1.0 Mbps, concurrency 0.025 / 0.005, target 10M, floor 340, cap
# 2,000). At aperture 25.0 the aperture factor is 1.0 and the launch coupling is the
# identity, so every number here is the pre-aperture-dial value exactly.
# ---------------------------------------------------------------------------
BASELINE_SPECTRUM_MHZ = 8.0
BASELINE_SE_BPS_PER_HZ = 0.65
BASELINE_ACTIVE_RATE_MBPS = 1.0
BASELINE_CONCURRENCY_PEAK = 0.025
BASELINE_CONCURRENCY_OFFPEAK = 0.005
DEFAULT_APERTURE_M2 = 25.0
CONFIGURED_SATELLITES_PER_LAUNCH = 12  # the Model A satellites-per-launch dial.

EXPECTED_PER_SAT_CAPACITY_GBPS = 0.78  # 8 x 0.65 x 0.15 x (25 / 25).
EXPECTED_SUBS_PER_SAT_PHONE_BASELINE = 31_200  # 0.78 x 1000 / (1.0 x 0.025).
EXPECTED_FLEET_TARGET_BASELINE = 340  # capacity need 321, the 340 floor binds.
EXPECTED_FLEET_AGGREGATE_GBPS = 265.2  # 0.78 x 340.
EXPECTED_BEAM_POOL_MBPS = 5.2  # 8 x 0.65.
EXPECTED_PEAK_RATE_MBPS = 1.0  # the active rate, by construction.
EXPECTED_OFFPEAK_RATE_MBPS = 5.0  # min(5.2, 1.0 x 0.025 / 0.005).
EXPECTED_EFFECTIVE_SPL_BASELINE = 12  # max(1, floor(12 x 25 / 25)), the identity.
EXPECTED_IOT_DEVICES = 10_000_000  # the passthrough counter (zero sizing effect).
EXPECTED_OPERATIONS_COST_MUSD = 0.0  # the explicit stated ops-zero assumption.

# The one intended difference from Model A: the derived density vs the fixed dial.
MODEL_A_SUBS_PER_SAT = SUBSCRIBERS_PER_SATELLITE_DEFAULT  # 75,000.

# The rich variant: a 2.5 Mbps active rate raises offered load, shrinks the density,
# and pushes the fleet target above the floor (the capacity regime binds).
RICH_ACTIVE_RATE_MBPS = 2.5
EXPECTED_SUBS_PER_SAT_RICH = 12_480  # 0.78 x 1000 / (2.5 x 0.025).
EXPECTED_FLEET_TARGET_RICH = 802  # ceil(10,000,000 / 12,480).

# The device-class spectral-efficiency centrals (the founder's three categories).
EXPECTED_SE_PHONE = 0.65
EXPECTED_SE_SMALL_TERMINAL = 2.0
EXPECTED_SE_TERMINAL = 2.5
SE_OVERRIDE_BPS_PER_HZ = 0.8  # an in-band override that beats the class central.

# The two capacity sanity anchors at the default aperture (COMM-647).
EXPECTED_SMALL_TERMINAL_CAPACITY_GBPS = 2.4  # 8 x 2.0 x 0.15.
EXPECTED_TERMINAL_CAPACITY_GBPS = 3.0  # 8 x 2.5 x 0.15.

# The founder's fewer-bigger vs more-smaller what-if: a 60 m^2 aperture (factor 2.4).
WHAT_IF_APERTURE_M2 = 60.0
EXPECTED_PER_SAT_CAPACITY_60M2_GBPS = 1.872  # 0.78 x 2.4 (float reprs 1.8719999999999999).
EXPECTED_SUBS_PER_SAT_60M2 = 74_880  # 1.872 x 1000 / (1.0 x 0.025).
EXPECTED_EFFECTIVE_SPL_60M2 = 5  # max(1, floor(12 x 25 / 60)).
EXPECTED_FLEET_AGGREGATE_60M2_GBPS = 636.48  # 1.872 x 340.

# A very large aperture that flies one satellite per launch (the AST pattern).
VERY_LARGE_APERTURE_M2 = 400.0
EXPECTED_EFFECTIVE_SPL_LARGE = 1  # max(1, floor(12 x 25 / 400)) = max(1, 0).

# The scenario YAML (anchored from this test file: tests/communications -> code ->
# scenarios/iridium_model_b.yaml).
_SCENARIO_YAML = Path(__file__).resolve().parents[2] / "scenarios" / "iridium_model_b.yaml"


# ---------------------------------------------------------------------------
# The pure derivations (called directly with the worked inputs).
# ---------------------------------------------------------------------------


def test_device_class_resolves_all_three_central_se_values() -> None:
    """The device-class resolver returns the three founder-category SE centrals."""
    phone = resolve_device_spectral_efficiency(IridiumDials(device_class=DeviceClass.PHONE_CLASS))
    small = resolve_device_spectral_efficiency(
        IridiumDials(device_class=DeviceClass.SMALL_TERMINAL_CLASS)
    )
    terminal = resolve_device_spectral_efficiency(
        IridiumDials(device_class=DeviceClass.TERMINAL_CLASS)
    )
    assert phone == pytest.approx(EXPECTED_SE_PHONE)
    assert small == pytest.approx(EXPECTED_SE_SMALL_TERMINAL)
    assert terminal == pytest.approx(EXPECTED_SE_TERMINAL)


def test_spectral_efficiency_override_wins() -> None:
    """An explicit spectral-efficiency override beats the device-class central."""
    resolved = resolve_device_spectral_efficiency(
        IridiumDials(spectral_efficiency_bps_per_hz=SE_OVERRIDE_BPS_PER_HZ)
    )
    assert resolved == pytest.approx(SE_OVERRIDE_BPS_PER_HZ)


def test_per_satellite_capacity_worked_products() -> None:
    """Capacity reproduces the baseline, both class anchors, and the 60 m^2 case."""
    baseline = derive_per_satellite_capacity_gbps(
        BASELINE_SPECTRUM_MHZ, EXPECTED_SE_PHONE, DEFAULT_APERTURE_M2
    )
    small_terminal = derive_per_satellite_capacity_gbps(
        BASELINE_SPECTRUM_MHZ, EXPECTED_SE_SMALL_TERMINAL, DEFAULT_APERTURE_M2
    )
    terminal = derive_per_satellite_capacity_gbps(
        BASELINE_SPECTRUM_MHZ, EXPECTED_SE_TERMINAL, DEFAULT_APERTURE_M2
    )
    aperture_60 = derive_per_satellite_capacity_gbps(
        BASELINE_SPECTRUM_MHZ, EXPECTED_SE_PHONE, WHAT_IF_APERTURE_M2
    )
    assert baseline == pytest.approx(EXPECTED_PER_SAT_CAPACITY_GBPS)
    assert small_terminal == pytest.approx(EXPECTED_SMALL_TERMINAL_CAPACITY_GBPS)
    assert terminal == pytest.approx(EXPECTED_TERMINAL_CAPACITY_GBPS)
    assert aperture_60 == pytest.approx(EXPECTED_PER_SAT_CAPACITY_60M2_GBPS)


def test_derived_subscribers_per_satellite_worked() -> None:
    """Density reproduces the baseline, the rich tier, and the 60 m^2 case (exact ints)."""
    baseline = derive_iridium_subscribers_per_satellite(
        per_satellite_capacity_gbps=EXPECTED_PER_SAT_CAPACITY_GBPS,
        active_user_rate_mbps=BASELINE_ACTIVE_RATE_MBPS,
        concurrency_peak=BASELINE_CONCURRENCY_PEAK,
    )
    rich = derive_iridium_subscribers_per_satellite(
        per_satellite_capacity_gbps=EXPECTED_PER_SAT_CAPACITY_GBPS,
        active_user_rate_mbps=RICH_ACTIVE_RATE_MBPS,
        concurrency_peak=BASELINE_CONCURRENCY_PEAK,
    )
    aperture_60 = derive_iridium_subscribers_per_satellite(
        per_satellite_capacity_gbps=EXPECTED_PER_SAT_CAPACITY_60M2_GBPS,
        active_user_rate_mbps=BASELINE_ACTIVE_RATE_MBPS,
        concurrency_peak=BASELINE_CONCURRENCY_PEAK,
    )
    assert baseline == EXPECTED_SUBS_PER_SAT_PHONE_BASELINE
    assert rich == EXPECTED_SUBS_PER_SAT_RICH
    assert aperture_60 == EXPECTED_SUBS_PER_SAT_60M2


def test_per_user_rates_worked() -> None:
    """Per-user rates are (peak, off-peak) = (1.0, 5.0) at the baseline (ratio binds)."""
    peak, offpeak = derive_iridium_per_user_rates(
        spectrum_mhz=BASELINE_SPECTRUM_MHZ,
        spectral_efficiency_bps_per_hz=BASELINE_SE_BPS_PER_HZ,
        active_user_rate_mbps=BASELINE_ACTIVE_RATE_MBPS,
        concurrency_peak=BASELINE_CONCURRENCY_PEAK,
        concurrency_offpeak=BASELINE_CONCURRENCY_OFFPEAK,
    )
    assert peak == pytest.approx(EXPECTED_PEAK_RATE_MBPS)
    assert offpeak == pytest.approx(EXPECTED_OFFPEAK_RATE_MBPS)


def test_per_user_offpeak_caps_at_the_beam_pool() -> None:
    """When the ratio rate tops the beam pool, the off-peak rate caps at the pool."""
    # active 10.0 gives ratio rate 10.0 x 0.025 / 0.005 = 50.0, above the 5.2 pool.
    peak, offpeak = derive_iridium_per_user_rates(
        spectrum_mhz=BASELINE_SPECTRUM_MHZ,
        spectral_efficiency_bps_per_hz=BASELINE_SE_BPS_PER_HZ,
        active_user_rate_mbps=10.0,
        concurrency_peak=BASELINE_CONCURRENCY_PEAK,
        concurrency_offpeak=BASELINE_CONCURRENCY_OFFPEAK,
    )
    assert peak == pytest.approx(10.0)
    assert offpeak == pytest.approx(EXPECTED_BEAM_POOL_MBPS)


def test_effective_satellites_per_launch_coupling_points() -> None:
    """Launch coupling gives 12 at 25 m^2, 5 at 60 m^2, and 1 at a large aperture."""
    identity = derive_iridium_satellites_per_launch(
        configured_satellites_per_launch=CONFIGURED_SATELLITES_PER_LAUNCH,
        aperture_m2=DEFAULT_APERTURE_M2,
    )
    coupled_60 = derive_iridium_satellites_per_launch(
        configured_satellites_per_launch=CONFIGURED_SATELLITES_PER_LAUNCH,
        aperture_m2=WHAT_IF_APERTURE_M2,
    )
    very_large = derive_iridium_satellites_per_launch(
        configured_satellites_per_launch=CONFIGURED_SATELLITES_PER_LAUNCH,
        aperture_m2=VERY_LARGE_APERTURE_M2,
    )
    assert identity == EXPECTED_EFFECTIVE_SPL_BASELINE
    assert coupled_60 == EXPECTED_EFFECTIVE_SPL_60M2
    assert very_large == EXPECTED_EFFECTIVE_SPL_LARGE


# ---------------------------------------------------------------------------
# Model A stays untouched (the None-iridium path).
# ---------------------------------------------------------------------------


def test_model_a_default_has_no_iridium_block() -> None:
    """The default Model A config produces no Iridium result block (the path is untouched)."""
    traj = run_comms_model(CommsConfig())
    assert traj.iridium is None


# ---------------------------------------------------------------------------
# Model B end-to-end (behind the config.iridium branch).
# ---------------------------------------------------------------------------


def test_model_b_baseline_physics_frozen() -> None:
    """The phone-class baseline freezes every derived physics number (aperture invariant)."""
    traj = run_comms_model(CommsConfig(iridium=IridiumDials()))
    assert traj.iridium is not None
    iridium = traj.iridium
    # The derived density and the fleet it sizes.
    assert traj.subscribers_per_satellite == EXPECTED_SUBS_PER_SAT_PHONE_BASELINE
    assert traj.fleet_target == EXPECTED_FLEET_TARGET_BASELINE
    assert traj.binding_regime is BindingRegime.COVERAGE
    # The Iridium physics block.
    assert iridium.device_class is DeviceClass.PHONE_CLASS
    assert iridium.spectral_efficiency_bps_per_hz == pytest.approx(BASELINE_SE_BPS_PER_HZ)
    assert iridium.per_satellite_capacity_gbps == pytest.approx(EXPECTED_PER_SAT_CAPACITY_GBPS)
    assert iridium.subscribers_per_satellite == EXPECTED_SUBS_PER_SAT_PHONE_BASELINE
    assert iridium.fleet_aggregate_capacity_gbps == pytest.approx(EXPECTED_FLEET_AGGREGATE_GBPS)
    assert iridium.beam_pool_mbps == pytest.approx(EXPECTED_BEAM_POOL_MBPS)
    assert iridium.per_user_rate_peak_mbps == pytest.approx(EXPECTED_PEAK_RATE_MBPS)
    assert iridium.per_user_rate_offpeak_mbps == pytest.approx(EXPECTED_OFFPEAK_RATE_MBPS)
    assert iridium.aperture_m2 == pytest.approx(DEFAULT_APERTURE_M2)
    assert iridium.effective_satellites_per_launch == EXPECTED_EFFECTIVE_SPL_BASELINE
    assert iridium.iot_devices == EXPECTED_IOT_DEVICES
    assert iridium.operations_cost_musd == pytest.approx(EXPECTED_OPERATIONS_COST_MUSD)


def test_model_b_baseline_shares_model_a_trajectory() -> None:
    """Model B baseline shares Model A's trajectory, differing only in the density."""
    model_a = run_comms_model(CommsConfig())
    model_b = run_comms_model(CommsConfig(iridium=IridiumDials()))
    # The shared build / cost / revenue fields are identical (the strong equality check).
    assert model_b.fleet_target == model_a.fleet_target
    assert model_b.binding_regime is model_a.binding_regime
    assert model_b.subscribers_served == model_a.subscribers_served
    assert model_b.full_coverage_reached_year == model_a.full_coverage_reached_year
    assert model_b.total_build_and_hold_cost_musd == pytest.approx(
        model_a.total_build_and_hold_cost_musd
    )
    assert model_b.cost_per_subscriber_annual_usd == pytest.approx(
        model_a.cost_per_subscriber_annual_usd
    )
    assert model_b.steady_state_revenue_cost_plus_musd == pytest.approx(
        model_a.steady_state_revenue_cost_plus_musd
    )
    assert model_b.steady_state_gross_margin_cost_plus_pct == pytest.approx(
        model_a.steady_state_gross_margin_cost_plus_pct
    )
    # The one intended difference: the derived density vs the fixed Model A dial.
    assert model_b.subscribers_per_satellite == EXPECTED_SUBS_PER_SAT_PHONE_BASELINE
    assert model_a.subscribers_per_satellite == MODEL_A_SUBS_PER_SAT
    assert model_b.subscribers_per_satellite != model_a.subscribers_per_satellite


def test_model_b_rich_tier_flips_to_capacity() -> None:
    """The rich 2.5 Mbps tier shrinks the density and flips to the capacity regime."""
    traj = run_comms_model(
        CommsConfig(iridium=IridiumDials(active_user_rate_mbps=RICH_ACTIVE_RATE_MBPS))
    )
    assert traj.subscribers_per_satellite == EXPECTED_SUBS_PER_SAT_RICH
    assert traj.fleet_target == EXPECTED_FLEET_TARGET_RICH
    assert traj.binding_regime is BindingRegime.CAPACITY


def test_model_b_terminal_class_capacity() -> None:
    """The large-terminal class resolves SE 2.5 and reproduces the 3.0 Gbps per-satellite anchor."""
    traj = run_comms_model(
        CommsConfig(iridium=IridiumDials(device_class=DeviceClass.TERMINAL_CLASS))
    )
    assert traj.iridium is not None
    assert traj.iridium.spectral_efficiency_bps_per_hz == pytest.approx(EXPECTED_SE_TERMINAL)
    assert traj.iridium.per_satellite_capacity_gbps == pytest.approx(
        EXPECTED_TERMINAL_CAPACITY_GBPS
    )


def test_model_b_aperture_60_what_if() -> None:
    """The 60 m^2 what-if freezes the fewer-bigger physics and carries the fold caveat."""
    traj = run_comms_model(CommsConfig(iridium=IridiumDials(aperture_m2=WHAT_IF_APERTURE_M2)))
    assert traj.iridium is not None
    iridium = traj.iridium
    assert iridium.per_satellite_capacity_gbps == pytest.approx(EXPECTED_PER_SAT_CAPACITY_60M2_GBPS)
    assert iridium.subscribers_per_satellite == EXPECTED_SUBS_PER_SAT_60M2
    # The extra capacity buys nothing at 10M: capacity need 134, the 340 floor still binds.
    assert traj.fleet_target == EXPECTED_FLEET_TARGET_BASELINE
    assert traj.binding_regime is BindingRegime.COVERAGE
    assert iridium.effective_satellites_per_launch == EXPECTED_EFFECTIVE_SPL_60M2
    assert iridium.fleet_aggregate_capacity_gbps == pytest.approx(
        EXPECTED_FLEET_AGGREGATE_60M2_GBPS
    )
    # The single-beam pool is aperture-independent, so the beam pool and off-peak are unchanged.
    assert iridium.beam_pool_mbps == pytest.approx(EXPECTED_BEAM_POOL_MBPS)
    assert iridium.per_user_rate_offpeak_mbps == pytest.approx(EXPECTED_OFFPEAK_RATE_MBPS)
    # Above the 25.0 no-fold limit, the assumptions output carries the fold caveat.
    caveat_lines = iridium_assumptions(IridiumDials(aperture_m2=WHAT_IF_APERTURE_M2))
    assert APERTURE_FOLD_CAVEAT_NOTE in caveat_lines


# ---------------------------------------------------------------------------
# The scenario YAML loads and runs (the loader path, unchanged).
# ---------------------------------------------------------------------------


def test_iridium_yaml_scenario_loads_and_runs() -> None:
    """The minimal Model B YAML loads (iridium, factory metadata) and runs the baseline."""
    config = load_comms_config(_SCENARIO_YAML)
    assert config.iridium is not None
    assert config.iridium.scenario_name == IRIDIUM_SCENARIO_NAME_DEFAULT
    # No metadata block in the file: the default factory supplies base year 2026, horizon 10.
    assert config.metadata.base_year == BASE_YEAR_DEFAULT
    assert config.metadata.horizon_years == HORIZON_YEARS_DEFAULT
    traj = run_comms_model(config)
    assert traj.iridium is not None
    assert traj.subscribers_per_satellite == EXPECTED_SUBS_PER_SAT_PHONE_BASELINE
    assert traj.fleet_target == EXPECTED_FLEET_TARGET_BASELINE
    assert traj.binding_regime is BindingRegime.COVERAGE
    assert traj.iridium.per_satellite_capacity_gbps == pytest.approx(EXPECTED_PER_SAT_CAPACITY_GBPS)


# ---------------------------------------------------------------------------
# The stated-assumptions accessor.
# ---------------------------------------------------------------------------


def test_iridium_assumptions_states_ecosystem_and_ops() -> None:
    """Default assumptions state ecosystem, ops-zero, and deferred-ARPU, no fold caveat."""
    lines = iridium_assumptions(IridiumDials())
    assert lines
    assert ECOSYSTEM_ASSUMPTION_NOTE in lines
    joined = " ".join(lines).lower()
    assert "in-chipset" in joined
    assert "unmodified" in joined
    assert "operations" in joined
    assert "zero" in joined
    assert "arpu" in joined
    assert "deferred" in joined
    # 25.0 is AT, not above, the no-fold limit, so the default output omits the fold caveat.
    assert APERTURE_FOLD_CAVEAT_NOTE not in lines
