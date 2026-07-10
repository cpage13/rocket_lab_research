"""Tests for the Iridium model (formerly Model B): L-band max-outcome, the MSS lane.

These cover the additive Iridium path: the pure L-band derivations (spectral
efficiency from the device class, per-satellite capacity with the aperture factor,
the derived per-satellite subscriber density, the per-user peak/off-peak rates, the
aperture-coupled effective satellites-per-launch), the end-to-end engine run behind
the ``config.iridium`` branch, the scenario YAML the existing loader parses
unchanged, the stated-assumptions accessor, and the promoted-JSON export.

Two structural facts anchor the suite. First, the High-Bandwidth Cellular Pure Play
model (formerly Model A) is untouched: the default config (no ``iridium`` block)
still yields ``trajectory.iridium is None`` and every High-Bandwidth Cellular Pure
Play number is unchanged. Second, THE STRONG EQUALITY CHECK: because the Iridium
phone-class baseline and the High-Bandwidth Cellular Pure Play default 10M run BOTH
bind at the 340 coverage floor, and at the default 25 m^2 aperture the effective
satellites-per-launch equals the configured 12 (the launch-coupling identity), their
entire cost / cohort / revenue trajectories are IDENTICAL; only the per-satellite
density and the new Iridium physics block differ. The 60 m^2 what-if breaks that
identity by design (the launch granularity changes), so it freezes the derived
physics and the fleet target only, not the deployment-year or cost outcomes.

Subscribers are PEOPLE; ``iot_devices`` is a separate DEVICE passthrough, never
folded into the people count. The Iridium model is the MSS lane (purpose-built or
in-chipset devices on owned L-band), never the cellular unmodified-phone lane (the
High-Bandwidth Cellular Pure Play model).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from communications.config import CommsConfig, IridiumArpuDials, IridiumDials, load_comms_config
from communications.constants import (
    APERTURE_FOLD_CAVEAT_NOTE,
    ARPU_MIX_TOTAL_PCT,
    BASE_YEAR_DEFAULT,
    ECOSYSTEM_ASSUMPTION_NOTE,
    HORIZON_YEARS_DEFAULT,
    IRIDIUM_SCENARIO_NAME_DEFAULT,
    MONTHS_PER_YEAR,
    SUBSCRIBERS_PER_SATELLITE_DEFAULT,
    BindingRegime,
    DeviceClass,
)
from communications.engine import (
    MUSD_TO_USD,
    derive_arpu_buckets,
    derive_iridium_per_user_rates,
    derive_iridium_satellites_per_launch,
    derive_iridium_subscribers_per_satellite,
    derive_per_satellite_capacity_gbps,
    iridium_assumptions,
    resolve_device_spectral_efficiency,
    run_comms_model,
)
from communications.json_output import (
    MODEL_NAME,
    build_iridium_artifact,
    export_iridium_json,
    render_json,
)

# ---------------------------------------------------------------------------
# The frozen Iridium-model phone-class baseline (spectrum 8.0, aperture 25.0,
# phone_class, SE 0.65, active 1.0 Mbps, concurrency 0.025 / 0.005, target 10M,
# floor 340, cap 2,000). At aperture 25.0 the aperture factor is 1.0 and the launch
# coupling is the identity, so every number here is the pre-aperture-dial value
# exactly.
# ---------------------------------------------------------------------------
BASELINE_SPECTRUM_MHZ = 8.0
BASELINE_SE_BPS_PER_HZ = 0.65
BASELINE_ACTIVE_RATE_MBPS = 1.0
BASELINE_CONCURRENCY_PEAK = 0.025
BASELINE_CONCURRENCY_OFFPEAK = 0.005
DEFAULT_APERTURE_M2 = 25.0
CONFIGURED_SATELLITES_PER_LAUNCH = 12  # the shared satellites-per-launch config dial.

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

# The one intended difference from the High-Bandwidth Cellular Pure Play model: the
# derived density vs the fixed dial.
HB_CELLULAR_SUBS_PER_SAT = SUBSCRIBERS_PER_SATELLITE_DEFAULT  # 75,000.

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

# ---------------------------------------------------------------------------
# The four-bucket ARPU revenue case, Sheet A (founder-set 2026-07-09). The frozen
# baseline at 340 satellites: people capacity 10,608,000 = 340 x 31,200. Mixes
# 15.0 / 2.0 / 82.805 / 0.195 (sum 100); prices 15 / 100 / 8 / 74 dollars per month.
# Every value below is exact (the float pool 62,400,000 lands on integers).
# ---------------------------------------------------------------------------
ARPU_PEOPLE_CAPACITY_BASELINE = 10_608_000  # 340 x 31,200.
ARPU_POOL_BASELINE = 62_400_000  # 10,608,000 / 0.17, exact.
ARPU_STANDARD_COUNT = 9_360_000  # people (the residual: 10,608,000 - premium).
ARPU_PREMIUM_COUNT = 1_248_000  # people (round_half_up(62,400,000 x 0.02)).
ARPU_IOT_COUNT = 51_670_320  # devices (round_half_up(62,400,000 x 0.82805)).
ARPU_GOVERNMENT_COUNT = 121_680  # contracts (round_half_up(62,400,000 x 0.00195)).
ARPU_STANDARD_REVENUE_MUSD = 1_684.8  # 9,360,000 x 15 x 12 / 1e6.
ARPU_PREMIUM_REVENUE_MUSD = 1_497.6  # 1,248,000 x 100 x 12 / 1e6.
ARPU_IOT_REVENUE_MUSD = 4_960.350_72  # 51,670,320 x 8 x 12 / 1e6.
ARPU_GOVERNMENT_REVENUE_MUSD = 108.051_84  # 121,680 x 74 x 12 / 1e6.
ARPU_TOTAL_REVENUE_MUSD = 8_250.802_56  # the four summed.

# ---------------------------------------------------------------------------
# The FLAT cost model (founder simplification 2026-07-09). The iridium scenario
# overrides the shared cost spine with a flat 13.0 $M launch (both cadence anchors
# equal) and a 1.0 $M satellite build cost. Frozen exact at the 340-satellite
# baseline (432 satellites across 36 launches over the horizon). These are SCENARIO
# values, not the config defaults (25 to 13.5 $M and 1.05 $M), which are untouched.
# ---------------------------------------------------------------------------
FLAT_BUILD_AND_HOLD_COST_MUSD = 900.0  # 432 satellites x 1.0 + 36 launches x 13.0.
FLAT_STEADY_STATE_REPLACEMENT_COST_MUSD = 75.0  # the final-year hold-phase replacement.
FLAT_COST_PER_SUBSCRIBER_ANNUAL_USD = 7.5  # 75.0 M USD / 10,000,000 subscribers.
FLAT_STEADY_STATE_ANNUAL_COST_MUSD = 145.0  # the annualized fleet cost basis.
# The published ARPU margin against that flat-cost steady-state annual cost:
# (8,250.80256 - 145.0) / 8,250.80256 x 100.
ARPU_MARGIN_VS_STEADY_STATE_COST_PCT = 98.242_595_202_762_91

# Test-3 scaling base: a non-frozen capacity whose float pool is NOT integral, so the
# round-half-up genuinely exercises the plus-or-minus-1 count tolerance at 2X.
ARPU_SCALING_CAPACITY_X = 7_000_000
ARPU_REVENUE_FLOAT_EPS_MUSD = 1e-9  # float slack on the one-count-quantum revenue bound.

# The scenario YAML (anchored from this test file: tests/communications -> code ->
# scenarios/iridium.yaml).
_SCENARIO_YAML = Path(__file__).resolve().parents[2] / "scenarios" / "iridium.yaml"


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
# The High-Bandwidth Cellular Pure Play model stays untouched (the None-iridium
# path).
# ---------------------------------------------------------------------------


def test_hb_cellular_default_has_no_iridium_block() -> None:
    """The default High-Bandwidth Cellular Pure Play config produces no Iridium block."""
    traj = run_comms_model(CommsConfig())
    assert traj.iridium is None


# ---------------------------------------------------------------------------
# The Iridium model end-to-end (behind the config.iridium branch).
# ---------------------------------------------------------------------------


def test_iridium_baseline_physics_frozen() -> None:
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


def test_iridium_baseline_shares_hb_cellular_trajectory() -> None:
    """The Iridium baseline shares the High-Bandwidth Cellular Pure Play trajectory.

    The two runs differ only in the per-satellite density (the strong equality
    check).
    """
    hb_cellular = run_comms_model(CommsConfig())
    iridium_run = run_comms_model(CommsConfig(iridium=IridiumDials()))
    # The shared build / cost / revenue fields are identical (the strong equality check).
    assert iridium_run.fleet_target == hb_cellular.fleet_target
    assert iridium_run.binding_regime is hb_cellular.binding_regime
    assert iridium_run.subscribers_served == hb_cellular.subscribers_served
    assert iridium_run.full_coverage_reached_year == hb_cellular.full_coverage_reached_year
    assert iridium_run.total_build_and_hold_cost_musd == pytest.approx(
        hb_cellular.total_build_and_hold_cost_musd
    )
    assert iridium_run.cost_per_subscriber_annual_usd == pytest.approx(
        hb_cellular.cost_per_subscriber_annual_usd
    )
    assert iridium_run.steady_state_revenue_cost_plus_musd == pytest.approx(
        hb_cellular.steady_state_revenue_cost_plus_musd
    )
    assert iridium_run.steady_state_gross_margin_cost_plus_pct == pytest.approx(
        hb_cellular.steady_state_gross_margin_cost_plus_pct
    )
    # The one intended difference: the derived density vs the fixed dial.
    assert iridium_run.subscribers_per_satellite == EXPECTED_SUBS_PER_SAT_PHONE_BASELINE
    assert hb_cellular.subscribers_per_satellite == HB_CELLULAR_SUBS_PER_SAT
    assert iridium_run.subscribers_per_satellite != hb_cellular.subscribers_per_satellite


def test_iridium_rich_tier_flips_to_capacity() -> None:
    """The rich 2.5 Mbps tier shrinks the density and flips to the capacity regime."""
    traj = run_comms_model(
        CommsConfig(iridium=IridiumDials(active_user_rate_mbps=RICH_ACTIVE_RATE_MBPS))
    )
    assert traj.subscribers_per_satellite == EXPECTED_SUBS_PER_SAT_RICH
    assert traj.fleet_target == EXPECTED_FLEET_TARGET_RICH
    assert traj.binding_regime is BindingRegime.CAPACITY


def test_iridium_terminal_class_capacity() -> None:
    """The large-terminal class resolves SE 2.5 and reproduces the 3.0 Gbps per-satellite anchor."""
    traj = run_comms_model(
        CommsConfig(iridium=IridiumDials(device_class=DeviceClass.TERMINAL_CLASS))
    )
    assert traj.iridium is not None
    assert traj.iridium.spectral_efficiency_bps_per_hz == pytest.approx(EXPECTED_SE_TERMINAL)
    assert traj.iridium.per_satellite_capacity_gbps == pytest.approx(
        EXPECTED_TERMINAL_CAPACITY_GBPS
    )


def test_iridium_aperture_60_what_if() -> None:
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
    """The Iridium scenario YAML loads (iridium, factory metadata) and runs the baseline."""
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
    """With the ARPU case on, assumptions state ecosystem, ops-zero, the PUBLISHED case,
    full sell-through, and the IoT supersession; no fold caveat at the reference aperture.
    """
    lines = iridium_assumptions(IridiumDials(arpu=IridiumArpuDials()))
    assert lines
    assert ECOSYSTEM_ASSUMPTION_NOTE in lines
    joined = " ".join(lines).lower()
    assert "in-chipset" in joined
    assert "unmodified" in joined
    assert "operations" in joined
    assert "zero" in joined
    assert "arpu" in joined
    # The deferred line is replaced by the published-case, sell-through, and
    # supersession statements when the four-bucket case is set.
    assert "published" in joined
    assert "sell-through" in joined
    assert "superseded" in joined
    assert "deferred" not in joined
    # 25.0 is AT, not above, the no-fold limit, so the default output omits the fold caveat.
    assert APERTURE_FOLD_CAVEAT_NOTE not in lines


# ---------------------------------------------------------------------------
# The promoted-JSON export (communications.json_output).
# ---------------------------------------------------------------------------


def test_promoted_json_export_writes_frozen_baseline(tmp_path: Path) -> None:
    """The export runs the Iridium scenario and the JSON carries the frozen baseline.

    Objective: the promoted-JSON writer end to end (scenario YAML in, artifact
    file out). Success: the file exists, the provenance names the model
    'iridium', echoes the stamp, and carries schema iridium-v3; the frozen
    baseline keys/values are in the payload (subscribers_per_satellite 31,200 in
    both blocks, fleet target 340, the stated-assumptions lines present); the
    flat-cost model (founder simplification 2026-07-09) freezes exact (900.0 M
    build-and-hold, 75.0 M replacement, 7.5 USD/sub, 145.0 M annual cost); the two
    cost-plus revenue fields are ABSENT from the trajectory summary (schema
    iridium-v3, founder direction 2026-07-10; the engine still computes them for the
    cellular family and the equality tripwire); the two inherited placeholder ARPU
    fields are gone; and the published four-bucket revenue_arpu_buckets block carries
    the frozen Sheet A values plus the published margin (98.2 percent) against the
    steady-state cost.
    """
    out_path = tmp_path / "iridium_default.json"
    written = export_iridium_json(_SCENARIO_YAML, out_path, version_stamp="test-stamp")
    assert written == out_path
    payload = json.loads(written.read_text(encoding="utf-8"))
    assert payload["provenance"]["model_name"] == MODEL_NAME
    assert payload["provenance"]["version_stamp"] == "test-stamp"
    assert payload["provenance"]["scenario_name"] == IRIDIUM_SCENARIO_NAME_DEFAULT
    assert payload["provenance"]["schema_version"] == "iridium-v3"
    assert (
        payload["trajectory_summary"]["subscribers_per_satellite"]
        == EXPECTED_SUBS_PER_SAT_PHONE_BASELINE
    )
    assert payload["trajectory_summary"]["fleet_target"] == EXPECTED_FLEET_TARGET_BASELINE
    # The flat-cost model (founder simplification 2026-07-09), frozen exact from the
    # scenario's flat 13.0 $M launch and 1.0 $M build overrides.
    ts = payload["trajectory_summary"]
    assert ts["total_build_and_hold_cost_musd"] == pytest.approx(FLAT_BUILD_AND_HOLD_COST_MUSD)
    assert ts["steady_state_annual_replacement_cost_musd"] == pytest.approx(
        FLAT_STEADY_STATE_REPLACEMENT_COST_MUSD
    )
    assert ts["cost_per_subscriber_annual_usd"] == pytest.approx(
        FLAT_COST_PER_SUBSCRIBER_ANNUAL_USD
    )
    assert ts["steady_state_annual_cost_musd"] == pytest.approx(FLAT_STEADY_STATE_ANNUAL_COST_MUSD)
    # The two cost-plus revenue fields are ABSENT from the artifact (schema iridium-v3,
    # founder direction 2026-07-10); the engine still computes them on the shared
    # trajectory for the cellular family and the equality tripwire (see
    # test_iridium_baseline_shares_hb_cellular_trajectory).
    assert "steady_state_revenue_cost_plus_musd" not in ts
    assert "steady_state_gross_margin_cost_plus_pct" not in ts
    assert (
        payload["iridium_physics"]["subscribers_per_satellite"]
        == EXPECTED_SUBS_PER_SAT_PHONE_BASELINE
    )
    assert payload["iridium_physics"]["per_satellite_capacity_gbps"] == pytest.approx(
        EXPECTED_PER_SAT_CAPACITY_GBPS
    )
    assert ECOSYSTEM_ASSUMPTION_NOTE in payload["assumptions"]
    # The two inherited placeholder ARPU fields are gone from the trajectory summary
    # (schema iridium-v2; they were the cellular-family $50 default, never Iridium's).
    assert "steady_state_revenue_arpu_musd" not in payload["trajectory_summary"]
    assert "steady_state_gross_margin_arpu_pct" not in payload["trajectory_summary"]
    # The published four-bucket ARPU case, frozen Sheet A values.
    buckets = payload["revenue_arpu_buckets"]
    assert buckets["standard"]["count"] == ARPU_STANDARD_COUNT
    assert buckets["standard"]["annual_revenue_musd"] == pytest.approx(ARPU_STANDARD_REVENUE_MUSD)
    assert buckets["premium"]["count"] == ARPU_PREMIUM_COUNT
    assert buckets["premium"]["annual_revenue_musd"] == pytest.approx(ARPU_PREMIUM_REVENUE_MUSD)
    assert buckets["iot"]["count"] == ARPU_IOT_COUNT
    assert buckets["iot"]["annual_revenue_musd"] == pytest.approx(ARPU_IOT_REVENUE_MUSD)
    assert buckets["government"]["count"] == ARPU_GOVERNMENT_COUNT
    assert buckets["government"]["annual_revenue_musd"] == pytest.approx(
        ARPU_GOVERNMENT_REVENUE_MUSD
    )
    assert buckets["total_connections"] == ARPU_POOL_BASELINE
    assert buckets["arpu_revenue_total_musd"] == pytest.approx(ARPU_TOTAL_REVENUE_MUSD)
    # The published ARPU margin against the flat-cost steady-state annual cost (145.0 M).
    assert buckets["arpu_margin_vs_steady_state_cost_pct"] == pytest.approx(
        ARPU_MARGIN_VS_STEADY_STATE_COST_PCT
    )
    # IoT supersession (one IoT truth): the physics IoT count is the bucket count.
    assert payload["iridium_physics"]["iot_devices"] == ARPU_IOT_COUNT


# ---------------------------------------------------------------------------
# The four-bucket ARPU revenue case (derive_arpu_buckets and the artifact wiring).
# ---------------------------------------------------------------------------


def test_arpu_buckets_frozen_sheet_a() -> None:
    """derive_arpu_buckets reproduces the frozen Sheet A baseline exactly.

    Objective: the pure pool algebra at the blessed default (people capacity
    10,608,000). Success: the four counts, the four revenues, the pool total, and
    the summed revenue equal the founder-frozen Sheet A values.
    """
    result = derive_arpu_buckets(ARPU_PEOPLE_CAPACITY_BASELINE, IridiumArpuDials())
    assert result.total_connections == ARPU_POOL_BASELINE
    assert result.standard.count == ARPU_STANDARD_COUNT
    assert result.premium.count == ARPU_PREMIUM_COUNT
    assert result.iot.count == ARPU_IOT_COUNT
    assert result.government.count == ARPU_GOVERNMENT_COUNT
    assert result.standard.revenue_musd_yr == pytest.approx(ARPU_STANDARD_REVENUE_MUSD)
    assert result.premium.revenue_musd_yr == pytest.approx(ARPU_PREMIUM_REVENUE_MUSD)
    assert result.iot.revenue_musd_yr == pytest.approx(ARPU_IOT_REVENUE_MUSD)
    assert result.government.revenue_musd_yr == pytest.approx(ARPU_GOVERNMENT_REVENUE_MUSD)
    assert result.arpu_revenue_total_musd_yr == pytest.approx(ARPU_TOTAL_REVENUE_MUSD)


def test_arpu_people_identity_exact_including_awkward_mix() -> None:
    """standard_count + premium_count == people_capacity exactly (the residual rule).

    Objective: the people identity holds by construction (standard is the residual),
    so it is exact even on a deliberately awkward mix and a non-round capacity, where
    independently rounding both people buckets would drift off by a person. Success:
    the two people counts sum to the input capacity exactly, at the baseline and on
    the awkward sheet.
    """
    baseline = derive_arpu_buckets(ARPU_PEOPLE_CAPACITY_BASELINE, IridiumArpuDials())
    assert baseline.standard.count + baseline.premium.count == ARPU_PEOPLE_CAPACITY_BASELINE
    awkward = IridiumArpuDials(
        standard_mix_pct=11.5,
        premium_mix_pct=3.5,
        iot_mix_pct=84.7,
        government_mix_pct=0.3,
        standard_price_usd_month=15.0,
        premium_price_usd_month=100.0,
        iot_price_usd_month=8.0,
        government_price_usd_month=74.0,
    )
    result = derive_arpu_buckets(ARPU_SCALING_CAPACITY_X, awkward)
    assert result.standard.count + result.premium.count == ARPU_SCALING_CAPACITY_X


def test_arpu_buckets_scale_linearly_with_capacity() -> None:
    """derive_arpu_buckets scales with the fleet capacity (the founder's requirement).

    Objective: called directly at X and 2X capacity (no dial-perturbation ambiguity),
    the case scales. Success: the float pool doubles exactly (it is linear in
    capacity), every integer count doubles within plus-or-minus 1 (independent
    round-half-up of the pool slice), and every bucket revenue doubles within one
    count quantum (its price times 12 over 1e6). X is a non-round base so the 2X
    rounding genuinely exercises the plus-or-minus-1 tolerance.
    """
    dials = IridiumArpuDials()
    people_share = (dials.standard_mix_pct + dials.premium_mix_pct) / ARPU_MIX_TOTAL_PCT
    result_x = derive_arpu_buckets(ARPU_SCALING_CAPACITY_X, dials)
    result_2x = derive_arpu_buckets(2 * ARPU_SCALING_CAPACITY_X, dials)
    # The float pool is linear in capacity, so it doubles exactly.
    pool_x = ARPU_SCALING_CAPACITY_X / people_share
    pool_2x = (2 * ARPU_SCALING_CAPACITY_X) / people_share
    assert pool_2x == pytest.approx(2 * pool_x)
    # Every integer count doubles within +-1, every bucket revenue within one quantum.
    pairs = (
        (result_x.standard, result_2x.standard),
        (result_x.premium, result_2x.premium),
        (result_x.iot, result_2x.iot),
        (result_x.government, result_2x.government),
    )
    for bucket_x, bucket_2x in pairs:
        assert abs(bucket_2x.count - 2 * bucket_x.count) <= 1
        quantum = bucket_x.price_usd_month * MONTHS_PER_YEAR / MUSD_TO_USD
        assert abs(bucket_2x.revenue_musd_yr - 2 * bucket_x.revenue_musd_yr) <= (
            quantum + ARPU_REVENUE_FLOAT_EPS_MUSD
        )
    assert abs(result_2x.total_connections - 2 * result_x.total_connections) <= 1


def test_arpu_validator_rejects_bad_sheet() -> None:
    """The config validator rejects a sheet that does not sum to 100 and a zero people mix.

    Objective: the pool algebra needs a partition (sum 100) and a non-zero people
    share. Success: a mix summing to 99 fails the model validator, and a standard mix
    at zero fails its strictly-positive Field bound; both raise ValidationError at
    construction.
    """
    with pytest.raises(ValidationError):
        IridiumArpuDials(
            standard_mix_pct=15.0,
            premium_mix_pct=2.0,
            iot_mix_pct=81.805,
            government_mix_pct=0.195,
        )  # sums to 99.0, off by 1.0.
    with pytest.raises(ValidationError):
        IridiumArpuDials(
            standard_mix_pct=0.0,  # fails gt=0 (people_share could go to zero).
            premium_mix_pct=17.0,
            iot_mix_pct=82.805,
            government_mix_pct=0.195,
        )


def test_arpu_none_path_omits_block_and_keeps_iot_passthrough() -> None:
    """No arpu block: the result and artifact omit the case, the IoT passthrough stands.

    Objective: the None path is inert. Success: IridiumResult.arpu is None, the
    promoted artifact omits revenue_arpu_buckets (None in the model and the JSON), and
    iridium_physics.iot_devices reports the fixed 10M passthrough, not a bucket count.
    """
    config = CommsConfig(iridium=IridiumDials())
    trajectory = run_comms_model(config)
    assert trajectory.iridium is not None
    assert trajectory.iridium.arpu is None
    artifact = build_iridium_artifact(
        config=config,
        trajectory=trajectory,
        source_scenario_path="scenarios/iridium.yaml",
        version_stamp="test",
    )
    assert artifact.revenue_arpu_buckets is None
    assert artifact.iridium_physics.iot_devices == EXPECTED_IOT_DEVICES
    payload = json.loads(render_json(artifact))
    assert payload.get("revenue_arpu_buckets") is None


def test_arpu_supersession_one_iot_truth() -> None:
    """With the ARPU case on, the artifact carries exactly one IoT count (the bucket).

    Objective: the IoT supersession at the output layer. Success: the artifact's
    iridium_physics.iot_devices equals the revenue mix's IoT bucket count (the frozen
    51,670,320), so no artifact ever carries two IoT counts.
    """
    config = CommsConfig(iridium=IridiumDials(arpu=IridiumArpuDials()))
    trajectory = run_comms_model(config)
    artifact = build_iridium_artifact(
        config=config,
        trajectory=trajectory,
        source_scenario_path="scenarios/iridium.yaml",
        version_stamp="test",
    )
    assert artifact.revenue_arpu_buckets is not None
    assert artifact.iridium_physics.iot_devices == artifact.revenue_arpu_buckets.iot.count
    assert artifact.iridium_physics.iot_devices == ARPU_IOT_COUNT
