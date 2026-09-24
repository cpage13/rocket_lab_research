"""Tests for the Iridium model (formerly Model B): L-band max-outcome, the MSS lane.

These cover the additive Iridium path: the pure L-band derivations (spectral
efficiency from the device class, per-satellite capacity with the aperture factor,
the derived per-satellite subscriber density, the per-user peak/off-peak rates, the
aperture-coupled effective satellites-per-launch), the end-to-end engine run behind
the ``config.iridium`` branch, the scenario YAML the existing loader parses
unchanged, the stated-assumptions accessor, the promoted-JSON export, the
documented variants (the rich tier, the coordinated spectrum, the device ladder),
the edge cases the artifact must publish honestly (a build completing in the final
year, a satellite life longer than the horizon, a near-zero share, an incomplete
build, a degenerate density), the saturation companion end to end, and the drift
guard that regenerates the committed promoted artifact.

Two structural facts anchor the suite. First, the High-Bandwidth Cellular Pure Play
model (formerly Model A) is untouched: the default config (no ``iridium`` block)
still yields ``trajectory.iridium is None`` and every High-Bandwidth Cellular Pure
Play number is unchanged. Second, THE EQUALITY TRIPWIRE: because the Iridium
phone-class baseline and the High-Bandwidth Cellular Pure Play default 10M run BOTH
bind at the 340 coverage floor, and at the default 25 m^2 aperture the effective
satellites-per-launch equals the configured 12 (the launch-coupling identity), their
entire cost / cohort / revenue trajectories are IDENTICAL, per-year rollup by
per-year rollup and headline by headline; only the per-satellite density and the
Iridium physics block differ. The 60 m^2 what-if breaks that identity by design
(the launch granularity changes), so it freezes the derived physics and the fleet
target only, not the deployment-year or cost outcomes.

Subscribers are PEOPLE; ``iot_devices`` is a separate DEVICE passthrough, never
folded into the people count. The Iridium model is the MSS lane (purpose-built or
in-chipset devices on owned L-band), never the cellular unmodified-phone lane (the
High-Bandwidth Cellular Pure Play model).
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from common.cli import EXIT_ERROR
from common.file_io import render_artifact_json
from communications.config import CommsConfig, IridiumArpuDials, IridiumDials, load_comms_config
from communications.constants import (
    APERTURE_FOLD_CAVEAT_NOTE,
    ARPU_MIX_TOTAL_PCT,
    BASE_YEAR_DEFAULT,
    ECOSYSTEM_ASSUMPTION_NOTE,
    HORIZON_YEARS_DEFAULT,
    IRIDIUM_SCENARIO_NAME_DEFAULT,
    MONTHS_PER_YEAR,
    ORBIT_ALTITUDE_KM_SCENARIO,
    ORBIT_INCLINATION_DEG_SCENARIO,
    ORBIT_SCENARIO_BASIS,
    ORBIT_SCENARIO_SOURCE_STATUS,
    SUBSCRIBERS_PER_SATELLITE_DEFAULT,
    BindingRegime,
    DeviceClass,
)
from communications.engine import (
    MUSD_TO_USD,
    CommsTrajectory,
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
    IridiumModelArtifact,
    build_iridium_artifact,
    export_iridium_json,
    main,
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

# The device-class spectral-efficiency centrals (the investor's three categories).
EXPECTED_SE_PHONE = 0.65
EXPECTED_SE_SMALL_TERMINAL = 2.0
EXPECTED_SE_TERMINAL = 2.5
SE_OVERRIDE_BPS_PER_HZ = 0.8  # an in-band override that beats the class central.

# The two capacity sanity anchors at the default aperture (COMM-647).
EXPECTED_SMALL_TERMINAL_CAPACITY_GBPS = 2.4  # 8 x 2.0 x 0.15.
EXPECTED_TERMINAL_CAPACITY_GBPS = 3.0  # 8 x 2.5 x 0.15.

# The investor's fewer-bigger vs more-smaller what-if: a 60 m^2 aperture (factor 2.4).
WHAT_IF_APERTURE_M2 = 60.0
EXPECTED_PER_SAT_CAPACITY_60M2_GBPS = 1.872  # 0.78 x 2.4 (float reprs 1.8719999999999999).
EXPECTED_SUBS_PER_SAT_60M2 = 74_880  # 1.872 x 1000 / (1.0 x 0.025).
EXPECTED_EFFECTIVE_SPL_60M2 = 5  # max(1, floor(12 x 25 / 60)).
EXPECTED_FLEET_AGGREGATE_60M2_GBPS = 636.48  # 1.872 x 340.

# A very large aperture that flies one satellite per launch (the AST pattern).
VERY_LARGE_APERTURE_M2 = 400.0
EXPECTED_EFFECTIVE_SPL_LARGE = 1  # max(1, floor(12 x 25 / 400)) = max(1, 0).

# ---------------------------------------------------------------------------
# The four-bucket ARPU revenue case, Sheet A (investor-set 2026-07-09). The frozen
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
# The FLAT cost model (investor simplification 2026-07-09) under the all-in
# manifest share (pedal to the metal, investor-set 2026-07-14). The iridium
# scenario overrides the shared cost spine with a flat 13.0 $M launch (both
# cadence anchors equal), a 1.0 $M satellite build cost, and an all-in
# comms_cadence share of 1.0. Frozen exact at the 340-satellite baseline: the
# build completes in 2031 (29 launches, 348 satellites), and by FY2036 the
# five-year treadmill has replaced the whole fleet exactly once (58 cumulative
# launches, 696 satellite units). These are SCENARIO values, not the config
# defaults (25 to 13.5 $M, 1.05 $M, 0.18 share), which are untouched.
# ---------------------------------------------------------------------------
FLAT_BUILD_AND_HOLD_COST_MUSD = 1450.0  # 696 satellites x 1.0 + 58 launches x 13.0.
# The FY2036 final-year cash replacement (the 2031 cohort retiring): 120 satellites
# x 1.0 + 10 launches x 13.0.
FLAT_FINAL_YEAR_REPLACEMENT_COST_MUSD = 250.0
# 250.0 M USD / 10,000,000 served people: the final-year cash basis.
FLAT_FINAL_YEAR_CASH_COST_PER_SUBSCRIBER_USD = 25.0
FLAT_STEADY_STATE_ANNUAL_COST_MUSD = 145.0  # the annualized basis (share-independent).
FULL_COVERAGE_YEAR_ALL_IN = 2031  # the 340-satellite build: 29 launches at 12 per launch.
# The per-year cash replacement lines FY2032..FY2036 (each year replaces the cohort
# launched five years earlier: 2, 3, 5, 9, 10 launches of 12 at 1.0 + 13.0 per launch).
FLAT_HOLD_REPLACEMENT_LINES_MUSD = (50.0, 75.0, 125.0, 225.0, 250.0)
COMPLETION_YEAR_SATELLITES = 120  # FY2031, the final build tranche (10 launches).
# The schema-v4 denominators, frozen exact at the all-in baseline.
ANNUALIZED_COST_PER_SUBSCRIBER_USD = 14.5  # 145.0 M USD / 10,000,000 people.
LIVING_FLEET_FINAL_YEAR = 348  # 29 whole launches x 12 satellites.
CUM_LAUNCHES_TO_COMPLETION = 29  # cumulative launches through the 2031 completion.
CUM_LAUNCHES_FINAL_YEAR = 58  # the 2031 build replaced exactly once by FY2036.
PEOPLE_CAPACITY_TARGET_FLEET = 10_608_000  # 340 x 31,200.
PEOPLE_CAPACITY_LIVING_FLEET = 10_857_600  # 348 x 31,200.
# The published ARPU margin against the built fleet's annualized cost (the 348
# satellites on orbit in FY2036, 145.0 M USD): (8,250.80256 - 145.0) / 8,250.80256 x 100.
ARPU_MARGIN_VS_STEADY_STATE_COST_PCT = 98.242_595_202_762_91
# The artifact schema this suite freezes.
EXPECTED_SCHEMA_VERSION = "iridium-v5"
# The ARPU case's stated assumptions: sell-through, mix posture, the built-fleet
# convention, and the margin definition.
ARPU_STATED_ASSUMPTION_COUNT = 4

# The equality tripwire's frozen value: the cellular default's final-year cash per
# subscriber (FY2036 replaces the 36-satellite 2031 cohort, 79.51... M USD, over the
# 10M served people), carried identically by the Iridium bare-dials run.
TRIPWIRE_CASH_COST_PER_SUBSCRIBER_USD = 7.951337204338448

# The rich tier at the config-default 0.18 share builds only 576 of its 802-satellite
# fleet by FY2036 (reported truthfully); the all-in share completes it in 2033 with
# 804 satellites (67 whole launches).
RICH_TIER_LIVING_AT_DEFAULT_SHARE = 576
RICH_TIER_COMPLETION_YEAR_ALL_IN = 2033
RICH_TIER_BUILT_FLEET = 804

# The documented density variants at the 340 floor: the coordinated 10.5 MHz span
# (10.5 x 0.65 x 0.15 = 1.02375 Gbps / 0.025 Mbps) and the device ladder (8 MHz at
# SE 2.0 and 2.5: 2.4 and 3.0 Gbps).
COORDINATED_SPECTRUM_MHZ = 10.5
EXPECTED_SUBS_PER_SAT_COORDINATED = 40_950
EXPECTED_SUBS_PER_SAT_SMALL_TERMINAL = 96_000
EXPECTED_SUBS_PER_SAT_TERMINAL = 120_000

# A degenerate aperture: at full peak concurrency the derived density rounds to zero
# (8 x 0.65 x 0.15 x 0.0004 = 0.000312 Gbps = 0.312 Mbps over a 1.0 Mbps load).
DEGENERATE_APERTURE_M2 = 0.01
FULL_PEAK_CONCURRENCY = 1.0

# The near-zero share: 0.001 of every whole-fleet cadence rounds to zero launches.
NEAR_ZERO_SHARE = 0.001
# A satellite life longer than the horizon (no cohort retires by FY2036).
LONG_LIFE_YEARS = 10
LONG_LIFE_ANNUAL_COST_MUSD = 72.5  # 348 x (1.0 + 13.0 / 12) / 10.
# A horizon that ends on the 2031 completion year.
COMPLETION_YEAR_HORIZON = 5

# Test-3 scaling base: a non-frozen capacity whose float pool is NOT integral, so the
# round-half-up genuinely exercises the plus-or-minus-1 count tolerance at 2X.
ARPU_SCALING_CAPACITY_X = 7_000_000
ARPU_REVENUE_FLOAT_EPS_MUSD = 1e-9  # float slack on the one-count-quantum revenue bound.

# ---------------------------------------------------------------------------
# The saturation companion (scenarios/iridium_saturation.yaml): the baseline dials
# with the subscriber target raised to the cap-binding 62,400,000 (2,000 x 31,200).
# Frozen from the published column: the 2,000-satellite build completes in 2035
# (2,004 living on whole launches, 186 launches to completion, 200 through FY2036).
# ---------------------------------------------------------------------------
SATURATION_TARGET_PEOPLE = 62_400_000
SATURATION_FLEET_TARGET = 2_000
SATURATION_COMPLETION_YEAR = 2035
SATURATION_LIVING_FLEET_FINAL_YEAR = 2_004
SATURATION_CUM_LAUNCHES_TO_COMPLETION = 186
SATURATION_CUM_LAUNCHES_FINAL_YEAR = 200
SATURATION_BUILD_AND_HOLD_COST_MUSD = 5_000.0
SATURATION_ANNUAL_COST_MUSD = 835.0  # 2,004 x (1.0 + 13.0 / 12) / 5.
SATURATION_FINAL_YEAR_REPLACEMENT_COST_MUSD = 350.0  # 168 satellites + 14 launches.
SATURATION_PEOPLE_CAPACITY_LIVING_FLEET = 62_524_800  # 2,004 x 31,200.
SATURATION_STANDARD_COUNT = 55_058_824
SATURATION_PREMIUM_COUNT = 7_341_176
SATURATION_IOT_COUNT = 303_943_059
SATURATION_GOVERNMENT_COUNT = 715_765
SATURATION_POOL = 367_058_824  # 62,400,000 / 0.17, rounded half up.
SATURATION_REVENUE_TOTAL_MUSD = 48_534.132_504
SATURATION_MARGIN_PCT = 98.279_561_296_513_99

# The scenario YAMLs and the committed promoted artifact come from the
# repository-anchored fixtures in conftest.py (iridium_yaml,
# iridium_saturation_yaml, promoted_iridium_artifact).


def _iridium_scenario_with(scenario: Path, block: str, **fields: object) -> CommsConfig:
    """Load an Iridium scenario with one block's fields replaced (re-validated).

    Args:
        scenario: The scenario YAML to start from (the promoted
            ``iridium.yaml``).
        block: The top-level config block to edit (e.g. ``"satellite"``).
        **fields: The fields to set inside that block.

    Returns:
        The validated variant config.
    """
    data = load_comms_config(scenario).model_dump()
    data[block] = {**(data.get(block) or {}), **fields}
    return CommsConfig.model_validate(data)


def _artifact_for(config: CommsConfig) -> IridiumModelArtifact:
    """Run a config and assemble its promoted artifact (no file IO).

    Args:
        config: An Iridium-selecting config.

    Returns:
        The assembled artifact.
    """
    return build_iridium_artifact(
        config=config,
        trajectory=run_comms_model(config),
        source_scenario_path="test",
        version_stamp="test",
    )


# ---------------------------------------------------------------------------
# The pure derivations (called directly with the worked inputs).
# ---------------------------------------------------------------------------


def test_device_class_resolves_all_three_central_se_values() -> None:
    """The device-class resolver returns the three investor-category SE centrals."""
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
    """THE EQUALITY TRIPWIRE: the Iridium baseline equals the cellular default, field by field.

    Objective: prove the shared machinery. On config defaults both families bind at
    the 340 coverage floor with the 12-per-launch identity at 25.0 m^2, so a shared
    engine drift moves both together while anything that moves one family alone
    breaks here. Expected: every per-year rollup is equal (the whole ``years``
    tuple, cohort lines included), every other trajectory field is exactly equal
    except the two intended differences (the per-satellite density, and the Iridium
    physics block present on one side only), and the final-year cash cost per
    subscriber is 7.951337204338448 dollars on both. Fields are enumerated from the
    dataclass, so a new trajectory field joins the comparison automatically.
    """
    hb_cellular = run_comms_model(CommsConfig())
    iridium_run = run_comms_model(CommsConfig(iridium=IridiumDials()))
    assert iridium_run.years == hb_cellular.years
    intended_differences = {"subscribers_per_satellite", "iridium"}
    compared = [
        field.name
        for field in dataclasses.fields(CommsTrajectory)
        if field.name not in intended_differences | {"years"}
    ]
    for name in compared:
        assert getattr(iridium_run, name) == getattr(hb_cellular, name), name
    assert hb_cellular.final_year_cash_cost_per_subscriber_usd == (
        TRIPWIRE_CASH_COST_PER_SUBSCRIBER_USD
    )
    # The intended differences: the derived density vs the fixed dial, and the block.
    assert iridium_run.subscribers_per_satellite == EXPECTED_SUBS_PER_SAT_PHONE_BASELINE
    assert hb_cellular.subscribers_per_satellite == HB_CELLULAR_SUBS_PER_SAT
    assert iridium_run.iridium is not None
    assert hb_cellular.iridium is None


def test_iridium_rich_tier_flips_to_capacity() -> None:
    """The rich 2.5 Mbps tier shrinks the density and flips to the capacity regime."""
    traj = run_comms_model(
        CommsConfig(iridium=IridiumDials(active_user_rate_mbps=RICH_ACTIVE_RATE_MBPS))
    )
    assert traj.subscribers_per_satellite == EXPECTED_SUBS_PER_SAT_RICH
    assert traj.fleet_target == EXPECTED_FLEET_TARGET_RICH
    assert traj.binding_regime is BindingRegime.CAPACITY


def test_rich_tier_reports_below_target_truthfully_then_completes_all_in(
    iridium_yaml: Path,
) -> None:
    """The rich tier's 802-satellite fleet: 576 by FY2036 at 0.18, complete in 2033 all-in.

    Objective: the model reports below-target deployment truthfully (the documented
    honesty feature). Expected: at the config-default 0.18 share the build never
    reaches the 802 target (no full-coverage year, 576 living in FY2036, the
    artifact publishes build_completes_in_horizon false); on the promoted scenario's
    all-in share it completes in 2033 with 804 satellites (67 whole launches).
    """
    default_share = run_comms_model(
        CommsConfig(iridium=IridiumDials(active_user_rate_mbps=RICH_ACTIVE_RATE_MBPS))
    )
    assert default_share.fleet_target == EXPECTED_FLEET_TARGET_RICH
    assert default_share.full_coverage_reached_year is None
    assert default_share.years[-1].living_fleet == RICH_TIER_LIVING_AT_DEFAULT_SHARE
    all_in_config = _iridium_scenario_with(
        iridium_yaml, "iridium", active_user_rate_mbps=RICH_ACTIVE_RATE_MBPS
    )
    all_in = run_comms_model(all_in_config)
    assert all_in.full_coverage_reached_year == RICH_TIER_COMPLETION_YEAR_ALL_IN
    assert all_in.years[-1].living_fleet == RICH_TIER_BUILT_FLEET
    incomplete = _iridium_scenario_with(
        iridium_yaml, "iridium", active_user_rate_mbps=RICH_ACTIVE_RATE_MBPS
    ).model_copy(update={"comms_cadence": CommsConfig().comms_cadence})
    assert _artifact_for(incomplete).trajectory_summary.build_completes_in_horizon is False


@pytest.mark.parametrize(
    ("dials", "expected_density"),
    [
        (IridiumDials(spectrum_mhz=COORDINATED_SPECTRUM_MHZ), EXPECTED_SUBS_PER_SAT_COORDINATED),
        (
            IridiumDials(device_class=DeviceClass.SMALL_TERMINAL_CLASS),
            EXPECTED_SUBS_PER_SAT_SMALL_TERMINAL,
        ),
        (IridiumDials(device_class=DeviceClass.TERMINAL_CLASS), EXPECTED_SUBS_PER_SAT_TERMINAL),
    ],
    ids=["coordinated_10_5_mhz", "small_terminal", "terminal"],
)
def test_documented_density_variants(dials: IridiumDials, expected_density: int) -> None:
    """The documented variants' densities: 40,950 (10.5 MHz), 96,000 and 120,000 (ladder).

    Objective: freeze the variant densities the conclusion quotes. Expected: each
    variant derives its density exactly and, at the 10M target, still binds at the
    340 coverage floor (more capacity per satellite buys nothing at this base).
    """
    traj = run_comms_model(CommsConfig(iridium=dials))
    assert traj.subscribers_per_satellite == expected_density
    assert traj.fleet_target == EXPECTED_FLEET_TARGET_BASELINE
    assert traj.binding_regime is BindingRegime.COVERAGE


def test_degenerate_density_fails_with_a_clear_error(tmp_path: Path) -> None:
    """Dials that derive less than one subscriber per satellite fail clearly, not by division.

    Objective: the derived density must be at least one person. A 0.01 m^2 aperture
    at full peak concurrency derives 0.312 Mbps of capacity over a 1.0 Mbps load,
    which rounds to zero and used to crash the fleet sizing with ZeroDivisionError.
    Expected: the engine raises a ValueError naming the problem, and the promotion
    command exits with the error code without writing an artifact (no traceback).
    """
    dials = IridiumDials(
        aperture_m2=DEGENERATE_APERTURE_M2,
        concurrency_peak=FULL_PEAK_CONCURRENCY,
    )
    with pytest.raises(ValueError, match="fewer than one subscriber per satellite"):
        run_comms_model(CommsConfig(iridium=dials))
    scenario = tmp_path / "degenerate.yaml"
    scenario.write_text(
        f"iridium:\n  aperture_m2: {DEGENERATE_APERTURE_M2}\n"
        f"  concurrency_peak: {FULL_PEAK_CONCURRENCY}\n",
        encoding="utf-8",
    )
    out_path = tmp_path / "degenerate.json"
    assert main([str(scenario), str(out_path)]) == EXIT_ERROR
    assert not out_path.exists()


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


def test_iridium_yaml_scenario_loads_and_runs(iridium_yaml: Path) -> None:
    """The Iridium scenario YAML loads (iridium, factory metadata) and runs the baseline."""
    config = load_comms_config(iridium_yaml)
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


def test_promoted_json_export_writes_frozen_baseline(tmp_path: Path, iridium_yaml: Path) -> None:
    """The export runs the Iridium scenario and the JSON carries the frozen baseline.

    Objective: the promoted-JSON writer end to end (scenario YAML in, artifact
    file out). Success: the file exists, the provenance names the model
    'iridium', echoes the stamp, and carries schema iridium-v5; the frozen
    baseline keys/values are in the payload (subscribers_per_satellite 31,200 in
    both blocks, fleet target 340, full coverage reached 2031 under the all-in
    share and so build_completes_in_horizon true, the stated-assumptions lines
    present); the flat-cost model (investor simplification 2026-07-09) under the
    all-in share freezes exact (1,450.0 M build-and-hold, 250.0 M final-year
    replacement, 25.0 USD/sub final-year cash beside the 14.50 annualized basis,
    145.0 M annual cost, equal to the built fleet's annualized cost); the v4
    denominators are exposed (348 living, 29 launches to completion, 58 through
    FY2036, 10,608,000 and 10,857,600 people capacity); the orbit scenario block
    carries the published 450 km / 53 degree posture with its basis text; the two
    cost-plus revenue fields are ABSENT from the trajectory summary (since schema
    iridium-v3; the engine still computes them for the cellular family and the
    equality tripwire); the two inherited placeholder ARPU fields are gone; and
    the published four-bucket revenue_arpu_buckets block carries the frozen Sheet
    A values plus the published margin (98.2 percent) against the built fleet's
    annualized cost.
    """
    out_path = tmp_path / "iridium_default.json"
    written = export_iridium_json(iridium_yaml, out_path, version_stamp="test-stamp")
    assert written == out_path
    payload = json.loads(written.read_text(encoding="utf-8"))
    assert payload["provenance"]["model_name"] == MODEL_NAME
    assert payload["provenance"]["version_stamp"] == "test-stamp"
    assert payload["provenance"]["scenario_name"] == IRIDIUM_SCENARIO_NAME_DEFAULT
    assert payload["provenance"]["schema_version"] == EXPECTED_SCHEMA_VERSION
    assert (
        payload["trajectory_summary"]["subscribers_per_satellite"]
        == EXPECTED_SUBS_PER_SAT_PHONE_BASELINE
    )
    assert payload["trajectory_summary"]["fleet_target"] == EXPECTED_FLEET_TARGET_BASELINE
    assert payload["trajectory_summary"]["full_coverage_reached_year"] == FULL_COVERAGE_YEAR_ALL_IN
    # The flat-cost model (investor simplification 2026-07-09), frozen exact from the
    # scenario's flat 13.0 $M launch, 1.0 $M build, and all-in share overrides.
    ts = payload["trajectory_summary"]
    assert ts["build_completes_in_horizon"] is True
    assert ts["total_build_and_hold_cost_musd"] == pytest.approx(FLAT_BUILD_AND_HOLD_COST_MUSD)
    assert ts["final_year_replacement_cost_musd"] == pytest.approx(
        FLAT_FINAL_YEAR_REPLACEMENT_COST_MUSD
    )
    assert ts["final_year_cash_cost_per_subscriber_usd"] == pytest.approx(
        FLAT_FINAL_YEAR_CASH_COST_PER_SUBSCRIBER_USD
    )
    assert ts["built_fleet_annual_cost_musd"] == ts["steady_state_annual_cost_musd"]
    assert ts["cost_per_subscriber_annualized_usd"] == pytest.approx(
        ANNUALIZED_COST_PER_SUBSCRIBER_USD
    )
    # The schema-v4 fleet, launch, and capacity denominators (the bases the prose
    # quotes), frozen exact at the all-in baseline.
    assert ts["living_fleet_final_year"] == LIVING_FLEET_FINAL_YEAR
    assert ts["cumulative_launches_to_completion"] == CUM_LAUNCHES_TO_COMPLETION
    assert ts["cumulative_launches_final_year"] == CUM_LAUNCHES_FINAL_YEAR
    assert ts["people_capacity_target_fleet"] == PEOPLE_CAPACITY_TARGET_FLEET
    assert ts["people_capacity_living_fleet_final_year"] == PEOPLE_CAPACITY_LIVING_FLEET
    # The orbit scenario block: the published posture with its limitations attached.
    orbit = payload["orbit_scenario"]
    assert orbit["altitude_km"] == pytest.approx(ORBIT_ALTITUDE_KM_SCENARIO)
    assert orbit["inclination_deg"] == pytest.approx(ORBIT_INCLINATION_DEG_SCENARIO)
    assert orbit["source_status"] == ORBIT_SCENARIO_SOURCE_STATUS
    assert orbit["basis"] == ORBIT_SCENARIO_BASIS
    assert ts["steady_state_annual_cost_musd"] == pytest.approx(FLAT_STEADY_STATE_ANNUAL_COST_MUSD)
    # The two cost-plus revenue fields are ABSENT from the artifact (schema iridium-v3,
    # investor direction 2026-07-10); the engine still computes them on the shared
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
    # The published ARPU margin against the built fleet's annualized cost (145.0 M).
    assert buckets["arpu_margin_vs_steady_state_cost_pct"] == pytest.approx(
        ARPU_MARGIN_VS_STEADY_STATE_COST_PCT
    )
    assert len(buckets["stated_assumptions"]) == ARPU_STATED_ASSUMPTION_COUNT
    # IoT supersession (one IoT truth): the physics IoT count is the bucket count.
    assert payload["iridium_physics"]["iot_devices"] == ARPU_IOT_COUNT


# ---------------------------------------------------------------------------
# The four-bucket ARPU revenue case (derive_arpu_buckets and the artifact wiring).
# ---------------------------------------------------------------------------


def test_arpu_buckets_frozen_sheet_a() -> None:
    """derive_arpu_buckets reproduces the frozen Sheet A baseline exactly.

    Objective: the pure pool algebra at the blessed default (people capacity
    10,608,000). Success: the four counts, the four revenues, the pool total, and
    the summed revenue equal the investor-frozen Sheet A values.
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
    """derive_arpu_buckets scales with the fleet capacity (the investor's requirement).

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
    payload = json.loads(render_artifact_json(artifact))
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


# ---------------------------------------------------------------------------
# The replacement line and the final-year cash pair on the promoted scenario and its
# edge cases (only retiring cohorts' replacement counts; no 0.0 published as real).
# ---------------------------------------------------------------------------


def test_completion_year_is_a_build_year_on_the_promoted_scenario(iridium_yaml: Path) -> None:
    """The 2031 completion tranche is build, never replacement; HOLD years replace cohorts.

    Objective: the replacement rule on the promoted scenario. FY2031 deploys the final
    120-satellite tranche with nothing retiring yet. Expected: FY2031 is not HOLD, has
    no replaced satellites and a 0.0 replacement line against its 250.0 M cash; the
    HOLD years FY2032..FY2036 replace the cohorts launched five years earlier, with
    replacement lines 50, 75, 125, 225, and 250 M, each equal to the year's cash.
    """
    traj = run_comms_model(load_comms_config(iridium_yaml))
    by_year = {year.year: year for year in traj.years}
    completion = by_year[FULL_COVERAGE_YEAR_ALL_IN]
    assert completion.is_hold_phase is False
    assert completion.satellites_deployed_this_year == COMPLETION_YEAR_SATELLITES
    assert completion.satellites_replaced_this_year == 0
    assert completion.replacement_cost_this_year_musd == 0.0
    assert completion.total_cost_this_year_musd == pytest.approx(
        FLAT_FINAL_YEAR_REPLACEMENT_COST_MUSD
    )
    hold_years = [year for year in traj.years if year.year > FULL_COVERAGE_YEAR_ALL_IN]
    assert all(year.is_hold_phase for year in hold_years)
    assert [year.replacement_cost_this_year_musd for year in hold_years] == pytest.approx(
        FLAT_HOLD_REPLACEMENT_LINES_MUSD
    )
    for year in hold_years:
        assert year.replacement_cost_this_year_musd == year.total_cost_this_year_musd


def test_horizon_ending_on_completion_publishes_no_cash_replacement(iridium_yaml: Path) -> None:
    """A horizon that ends on the completion year publishes no final-year cash replacement.

    Objective: the final-year cash pair never carries a build tranche. Before the
    fix, a 5-year horizon (final year FY2031, the completion year, nothing retired)
    published the 250.0 M build tranche as "final_year_replacement_cost_musd" and 25.0
    USD as the cash cost per subscriber. Expected: both fields are None, while the
    annualized basis (145.0 M, 14.50 USD per person) still publishes.
    """
    config = _iridium_scenario_with(
        iridium_yaml, "metadata", base_year=BASE_YEAR_DEFAULT, horizon_years=COMPLETION_YEAR_HORIZON
    )
    summary = _artifact_for(config).trajectory_summary
    assert summary.full_coverage_reached_year == FULL_COVERAGE_YEAR_ALL_IN
    assert summary.final_year_replacement_cost_musd is None
    assert summary.final_year_cash_cost_per_subscriber_usd is None
    assert summary.steady_state_annual_cost_musd == pytest.approx(
        FLAT_STEADY_STATE_ANNUAL_COST_MUSD
    )
    assert summary.cost_per_subscriber_annualized_usd == pytest.approx(
        ANNUALIZED_COST_PER_SUBSCRIBER_USD
    )


def test_long_satellite_life_publishes_no_cash_replacement(iridium_yaml: Path) -> None:
    """A satellite life longer than the horizon publishes no 0.0 cash cost as a real figure.

    Objective: with a 10-year life no cohort retires by FY2036, so the final year
    replaces nothing. Before the fix the artifact published 0.0 M and 0.0 USD per
    subscriber as if serving cost nothing. Expected: the final-year cash pair is None
    and the annualized basis carries the real cost (72.5 M a year for 348 satellites).
    """
    config = _iridium_scenario_with(
        iridium_yaml, "satellite", satellite_lifetime_years=LONG_LIFE_YEARS
    )
    summary = _artifact_for(config).trajectory_summary
    assert summary.final_year_replacement_cost_musd is None
    assert summary.final_year_cash_cost_per_subscriber_usd is None
    assert summary.steady_state_annual_cost_musd == pytest.approx(LONG_LIFE_ANNUAL_COST_MUSD)


def test_near_zero_share_does_not_publish_a_full_margin_on_an_empty_fleet(
    iridium_yaml: Path,
) -> None:
    """A share that never launches publishes the built fleet's margin, flagged incomplete.

    Objective: the ARPU margin pairs revenue and cost on the same (built) fleet.
    Before the fix a 0.001 share (zero launches, an empty fleet) published the
    8,250.8 M built-fleet revenue at a 100 percent margin against a 0.0 cost.
    Expected: the artifact flags build_completes_in_horizon false, the final-year
    annualized cost is 0.0 (nothing on orbit) but the built fleet's annualized cost is
    145.0 M (348 whole-launch satellites at the flat price), the margin is the
    baseline's 98.24 percent (not 100), and the per-person and final-year cash
    figures are None (nobody served, nothing replaced).
    """
    config = _iridium_scenario_with(iridium_yaml, "comms_cadence", share_of_fleet=NEAR_ZERO_SHARE)
    artifact = _artifact_for(config)
    summary = artifact.trajectory_summary
    assert summary.build_completes_in_horizon is False
    assert summary.living_fleet_final_year == 0
    assert summary.subscribers_served == 0
    assert summary.steady_state_annual_cost_musd == 0.0
    assert summary.built_fleet_annual_cost_musd == pytest.approx(FLAT_STEADY_STATE_ANNUAL_COST_MUSD)
    assert summary.cost_per_subscriber_annualized_usd is None
    assert summary.final_year_replacement_cost_musd is None
    assert summary.final_year_cash_cost_per_subscriber_usd is None
    assert artifact.revenue_arpu_buckets is not None
    assert artifact.revenue_arpu_buckets.arpu_margin_vs_steady_state_cost_pct == pytest.approx(
        ARPU_MARGIN_VS_STEADY_STATE_COST_PCT
    )


def test_incomplete_build_margin_equals_the_completed_build_margin(iridium_yaml: Path) -> None:
    """The margin describes the built fleet whether or not the horizon reaches it.

    Objective: consistency of the built-fleet convention. The rich tier on the flat
    costs builds an 802-satellite target (804 on whole launches): all-in it completes
    in 2033; at the 0.18 share it reaches only 576 by FY2036. Expected: the same
    revenue and, within float tolerance, the same margin in both runs (the
    incomplete run projects the 804-satellite built fleet at the flat price instead of
    pricing the 576 on orbit), and only the incomplete run is flagged.
    """
    complete_config = _iridium_scenario_with(
        iridium_yaml, "iridium", active_user_rate_mbps=RICH_ACTIVE_RATE_MBPS
    )
    incomplete_config = complete_config.model_copy(
        update={"comms_cadence": CommsConfig().comms_cadence}
    )
    complete = _artifact_for(complete_config)
    incomplete = _artifact_for(incomplete_config)
    assert complete.trajectory_summary.build_completes_in_horizon is True
    assert incomplete.trajectory_summary.build_completes_in_horizon is False
    assert incomplete.trajectory_summary.living_fleet_final_year == (
        RICH_TIER_LIVING_AT_DEFAULT_SHARE
    )
    assert incomplete.trajectory_summary.built_fleet_annual_cost_musd == pytest.approx(
        complete.trajectory_summary.built_fleet_annual_cost_musd
    )
    assert complete.revenue_arpu_buckets is not None
    assert incomplete.revenue_arpu_buckets is not None
    assert (
        incomplete.revenue_arpu_buckets.arpu_revenue_total_musd
        == complete.revenue_arpu_buckets.arpu_revenue_total_musd
    )
    assert incomplete.revenue_arpu_buckets.arpu_margin_vs_steady_state_cost_pct == pytest.approx(
        complete.revenue_arpu_buckets.arpu_margin_vs_steady_state_cost_pct
    )


# ---------------------------------------------------------------------------
# The saturation companion and the scenario pair.
# ---------------------------------------------------------------------------


def test_saturation_companion_end_to_end(tmp_path: Path, iridium_saturation_yaml: Path) -> None:
    """The saturation companion's published column, frozen end to end.

    Objective: scenarios/iridium_saturation.yaml through the promotion writer
    (YAML in, artifact file out), freezing the second column of the published
    verdict. Expected: the 2,000-satellite cap binds (saturated regime) and the build
    completes in 2035 with 2,004 living satellites, 186 launches to completion and
    200 through FY2036; 62,400,000 people served (exactly the capped fleet's people
    capacity); 5,000.0 M build-and-hold and an 835.0 M annualized fleet cost (equal
    to the built fleet's); a 350.0 M FY2036 cash replacement; the Sheet A buckets
    (55,058,824 standard and 7,341,176 premium people, 303,943,059 IoT devices,
    715,765 government contracts, a 367,058,824 billable-connection pool) totaling
    48,534.132504 M a year at a 98.28 percent margin; people and devices never summed.
    """
    written = export_iridium_json(iridium_saturation_yaml, tmp_path / "saturation.json")
    payload = json.loads(written.read_text(encoding="utf-8"))
    ts = payload["trajectory_summary"]
    assert ts["fleet_target"] == SATURATION_FLEET_TARGET
    assert ts["binding_regime"] == BindingRegime.SATURATED.value
    assert ts["full_coverage_reached_year"] == SATURATION_COMPLETION_YEAR
    assert ts["build_completes_in_horizon"] is True
    assert ts["living_fleet_final_year"] == SATURATION_LIVING_FLEET_FINAL_YEAR
    assert ts["cumulative_launches_to_completion"] == SATURATION_CUM_LAUNCHES_TO_COMPLETION
    assert ts["cumulative_launches_final_year"] == SATURATION_CUM_LAUNCHES_FINAL_YEAR
    assert ts["subscribers_served"] == SATURATION_TARGET_PEOPLE
    assert ts["people_capacity_target_fleet"] == SATURATION_TARGET_PEOPLE
    assert ts["people_capacity_living_fleet_final_year"] == (
        SATURATION_PEOPLE_CAPACITY_LIVING_FLEET
    )
    assert ts["total_build_and_hold_cost_musd"] == pytest.approx(
        SATURATION_BUILD_AND_HOLD_COST_MUSD
    )
    assert ts["steady_state_annual_cost_musd"] == pytest.approx(SATURATION_ANNUAL_COST_MUSD)
    assert ts["built_fleet_annual_cost_musd"] == ts["steady_state_annual_cost_musd"]
    assert ts["final_year_replacement_cost_musd"] == pytest.approx(
        SATURATION_FINAL_YEAR_REPLACEMENT_COST_MUSD
    )
    buckets = payload["revenue_arpu_buckets"]
    assert buckets["standard"]["count"] == SATURATION_STANDARD_COUNT
    assert buckets["premium"]["count"] == SATURATION_PREMIUM_COUNT
    assert buckets["standard"]["count"] + buckets["premium"]["count"] == SATURATION_TARGET_PEOPLE
    assert buckets["iot"]["count"] == SATURATION_IOT_COUNT
    assert buckets["government"]["count"] == SATURATION_GOVERNMENT_COUNT
    assert buckets["total_connections"] == SATURATION_POOL
    assert buckets["arpu_revenue_total_musd"] == pytest.approx(SATURATION_REVENUE_TOTAL_MUSD)
    assert buckets["arpu_margin_vs_steady_state_cost_pct"] == pytest.approx(SATURATION_MARGIN_PCT)
    assert payload["iridium_physics"]["iot_devices"] == SATURATION_IOT_COUNT


def test_the_two_scenarios_differ_only_in_target_and_label(
    iridium_yaml: Path, iridium_saturation_yaml: Path
) -> None:
    """The saturation companion moves exactly one dial (and its label) from the baseline.

    Objective: the two hand-repeated YAMLs stay in step. Expected: loaded configs are
    identical except ``subscribers.subscribers_at_full_coverage`` (10M versus the
    cap-binding 62.4M) and ``iridium.scenario_name``.
    """
    baseline = load_comms_config(iridium_yaml).model_dump()
    saturation = load_comms_config(iridium_saturation_yaml).model_dump()
    assert saturation["subscribers"].pop("subscribers_at_full_coverage") == (
        SATURATION_TARGET_PEOPLE
    )
    baseline["subscribers"].pop("subscribers_at_full_coverage")
    assert saturation["iridium"].pop("scenario_name") != baseline["iridium"].pop("scenario_name")
    assert saturation == baseline


# ---------------------------------------------------------------------------
# The committed promoted artifact regenerates from the code (the drift guard).
# ---------------------------------------------------------------------------


def test_regenerated_default_artifact_matches_committed(
    tmp_path: Path, iridium_yaml: Path, promoted_iridium_artifact: Path
) -> None:
    """Regenerating the promoted Iridium artifact reproduces the committed file.

    Objective: the committed communications/models/iridium/default.json is exactly
    what the current code writes from scenarios/iridium.yaml (the conclusion quotes
    it). Expected: a fresh export, stamped with the committed version stamp,
    parses to the same JSON document, key for key and value for value.
    """
    committed = json.loads(promoted_iridium_artifact.read_text(encoding="utf-8"))
    written = export_iridium_json(
        iridium_yaml,
        tmp_path / "default.json",
        version_stamp=committed["provenance"]["version_stamp"],
    )
    regenerated = json.loads(written.read_text(encoding="utf-8"))
    assert regenerated == committed
