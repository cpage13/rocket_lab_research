"""Tests for the clean-rewrite communications config in ``config.py``.

Covers the slim ``CommsConfig`` dial tree: all-defaults construction, the frozen /
``extra="forbid"`` contract, the shared cadence and launch-cost blocks (the
``common.cadence`` classes themselves, with their load-time validators; the
classes' own defaults and bounds are tested once, in
``tests/common/test_cadence_move.py``), the satellite / coverage / comms-share /
ground blocks, the field bounds, the cross-field validators (coverage floor at or
below the cap, off-peak concurrency at or below the peak), and the YAML loader pair.
Mirrors the data-center
``test_config.py`` assertion style without importing ``data_center`` (forbidden).
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from common.cadence import CadenceDials, LaunchCostDials
from common.file_io import ModelFileError
from communications.config import (
    CommsCadenceDials,
    CommsConfig,
    CommsMetadataDials,
    CoverageDials,
    GroundInterfaceDials,
    IridiumDials,
    RevenueDials,
    SatelliteDials,
    SubscriberDials,
    comms_config_from_dict,
    load_comms_config,
)
from communications.constants import (
    ARPU_USD_PER_MONTH_DEFAULT,
    BASE_YEAR_DEFAULT,
    COMMS_SHARE_DEFAULT,
    GROUND_BASIS_DEFAULT,
    HORIZON_YEARS_DEFAULT,
    MAX_FLEET_SATELLITES_DEFAULT,
    REVENUE_MULTIPLE_DEFAULT,
    SATELLITE_BUILD_COST_MUSD_DEFAULT,
    SATELLITE_LIFETIME_YEARS_DEFAULT,
    SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
    SATELLITES_PER_LAUNCH_DEFAULT,
    SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT,
    SUBSCRIBERS_PER_SATELLITE_DEFAULT,
)

# -- all-defaults construction ----------------------------------------


def test_comms_config_default_construction_has_all_blocks() -> None:
    """A no-arg ``CommsConfig`` builds every block with valid defaults."""
    c = CommsConfig()
    assert isinstance(c.metadata, CommsMetadataDials)
    assert isinstance(c.cadence, CadenceDials)
    assert isinstance(c.comms_cadence, CommsCadenceDials)
    assert isinstance(c.launch_cost, LaunchCostDials)
    assert isinstance(c.satellite, SatelliteDials)
    assert isinstance(c.coverage, CoverageDials)
    assert isinstance(c.subscribers, SubscriberDials)
    assert isinstance(c.revenue, RevenueDials)
    # The ground interface is None by default so the cost side never blocks.
    assert c.ground is None


@pytest.mark.parametrize(
    ("block", "dials", "message"),
    [
        ("cadence", {"launches_at_year_5": 0}, "0 < launches_at_year_5 < launches_at_year_10"),
        (
            "launch_cost",
            {"low_cadence_launches": 100.0, "high_cadence_launches": 5.0},
            "low_cadence_launches < high_cadence_launches",
        ),
    ],
    ids=["cadence_anchor_zero", "reversed_launch_cost_anchors"],
)
def test_the_shared_cadence_validators_guard_the_comms_config(
    block: str, dials: dict[str, float], message: str
) -> None:
    """Objective: the comms config validates its cadence blocks like the data-center one.

    The comms copy of the two blocks used to accept a zero year-5 anchor (the run
    then raised mid-model) and reversed launch-cost anchors (the cost-down silently
    switched off). Both configs now hold the one :mod:`common.cadence` pair.
    Expected: each fails at load with the shared validator's message.
    """
    assert CommsConfig.model_fields[block].annotation in (CadenceDials, LaunchCostDials)
    with pytest.raises(ValidationError, match=message):
        comms_config_from_dict({block: dials})


def test_comms_config_default_metadata_is_central_case() -> None:
    """The metadata factory supplies base year 2026 and horizon 10."""
    c = CommsConfig()
    assert c.metadata.base_year == BASE_YEAR_DEFAULT
    assert c.metadata.horizon_years == HORIZON_YEARS_DEFAULT


# -- frozen contract --------------------------------------------------


def test_comms_config_is_frozen() -> None:
    """Mutating a declared top-level field on the frozen config raises."""
    c = CommsConfig()
    with pytest.raises(ValidationError):
        c.ground = GroundInterfaceDials()


def test_satellite_dials_frozen() -> None:
    """Mutating the satellite block raises ``ValidationError`` (frozen)."""
    sat = SatelliteDials()
    with pytest.raises(ValidationError):
        sat.satellite_build_cost_musd = 2.0


def test_revenue_dials_frozen() -> None:
    """Mutating the revenue block raises ``ValidationError`` (frozen)."""
    rev = RevenueDials()
    with pytest.raises(ValidationError):
        rev.revenue_multiple = 2.0


# -- extra=forbid -----------------------------------------------------


def test_comms_config_rejects_unknown_top_level_block() -> None:
    with pytest.raises(ValidationError):
        CommsConfig.model_validate({"bogus_block": {}})


def test_satellite_dials_rejects_unknown_field() -> None:
    with pytest.raises(ValidationError):
        SatelliteDials.model_validate({"bogus_dial": 1})


def test_revenue_dials_rejects_unknown_field() -> None:
    with pytest.raises(ValidationError):
        RevenueDials.model_validate({"bogus_dial": 1.0})


def test_ground_interface_dials_rejects_unknown_field() -> None:
    with pytest.raises(ValidationError):
        GroundInterfaceDials.model_validate({"bogus_dial": 1.0})


# -- the new dial defaults (the four investor-set values + spec dials) --


def test_satellite_dials_defaults() -> None:
    sat = SatelliteDials()
    assert sat.satellites_per_launch == SATELLITES_PER_LAUNCH_DEFAULT
    assert sat.satellite_lifetime_years == SATELLITE_LIFETIME_YEARS_DEFAULT
    assert sat.satellite_build_cost_musd == SATELLITE_BUILD_COST_MUSD_DEFAULT


def test_coverage_dials_default_floor_is_investor_set_340() -> None:
    """The coverage FLOOR default is the investor-set 340 (the lower fleet bound)."""
    cov = CoverageDials()
    assert cov.satellites_for_full_coverage == SATELLITES_FOR_FULL_COVERAGE_DEFAULT
    assert cov.satellites_for_full_coverage == 340


def test_coverage_dials_default_cap_is_investor_set_2000() -> None:
    """The saturation CAP default is the investor-set 2,000 (the upper fleet bound)."""
    cov = CoverageDials()
    assert cov.max_fleet_satellites == MAX_FLEET_SATELLITES_DEFAULT
    assert cov.max_fleet_satellites == 2_000


def test_comms_cadence_default_share_is_investor_set() -> None:
    cc = CommsCadenceDials()
    assert cc.share_of_fleet == COMMS_SHARE_DEFAULT
    assert cc.share_of_fleet == pytest.approx(0.18)


def test_subscriber_dials_defaults() -> None:
    """The subscriber target default is the investor baseline 10M; density 75,000."""
    subs = SubscriberDials()
    # The target (the base to serve) is the 10M baseline.
    assert subs.subscribers_at_full_coverage == SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT
    assert subs.subscribers_at_full_coverage == 10_000_000
    # The per-satellite attached density (the capacity dial) is the 75,000 central.
    assert subs.subscribers_per_satellite == SUBSCRIBERS_PER_SATELLITE_DEFAULT
    assert subs.subscribers_per_satellite == 75_000
    # The optional direct override defaults to None (the target is the served base).
    assert subs.subscribers_served_override is None


def test_revenue_dials_defaults() -> None:
    """The revenue multiple default is 1.5 (the DC R mirror); the ARPU is $50/mo."""
    rev = RevenueDials()
    assert rev.revenue_multiple == REVENUE_MULTIPLE_DEFAULT
    assert rev.revenue_multiple == pytest.approx(1.5)
    assert rev.arpu_usd_per_month == ARPU_USD_PER_MONTH_DEFAULT
    assert rev.arpu_usd_per_month == pytest.approx(50.0)


# -- ground interface block (declared in Phase 1, None-able baselines) -


def test_ground_interface_dials_defaults_are_none_able() -> None:
    """Both regime baselines default to None so either regime can be absent."""
    g = GroundInterfaceDials()
    assert g.dense_ground_cost_per_subscriber_usd is None
    assert g.sparse_ground_cost_per_subscriber_usd is None
    assert g.basis == GROUND_BASIS_DEFAULT


# -- field bounds bite ------------------------------------------------


def test_satellites_per_launch_rejects_above_sixteen() -> None:
    with pytest.raises(ValidationError):
        SatelliteDials(satellites_per_launch=17)


def test_satellite_build_cost_rejects_zero() -> None:
    with pytest.raises(ValidationError):
        SatelliteDials(satellite_build_cost_musd=0.0)


def test_satellite_lifetime_rejects_zero() -> None:
    with pytest.raises(ValidationError):
        SatelliteDials(satellite_lifetime_years=0)


def test_share_of_fleet_rejects_above_one() -> None:
    with pytest.raises(ValidationError):
        CommsCadenceDials(share_of_fleet=1.5)


def test_share_of_fleet_rejects_zero() -> None:
    with pytest.raises(ValidationError):
        CommsCadenceDials(share_of_fleet=0.0)


def test_coverage_rejects_zero() -> None:
    with pytest.raises(ValidationError):
        CoverageDials(satellites_for_full_coverage=0)


def test_max_fleet_satellites_rejects_zero() -> None:
    with pytest.raises(ValidationError):
        CoverageDials(max_fleet_satellites=0)


def test_subscribers_per_satellite_rejects_zero() -> None:
    with pytest.raises(ValidationError):
        SubscriberDials(subscribers_per_satellite=0)


def test_revenue_multiple_rejects_zero() -> None:
    with pytest.raises(ValidationError):
        RevenueDials(revenue_multiple=0.0)


def test_arpu_rejects_zero() -> None:
    with pytest.raises(ValidationError):
        RevenueDials(arpu_usd_per_month=0.0)


def test_metadata_rejects_out_of_range_horizon() -> None:
    with pytest.raises(ValidationError):
        CommsMetadataDials(base_year=BASE_YEAR_DEFAULT, horizon_years=0)


# -- YAML loaders -----------------------------------------------------


def test_comms_config_from_dict_empty_yields_all_defaults() -> None:
    """An empty mapping yields an all-defaults config equal to ``CommsConfig()``."""
    assert comms_config_from_dict({}) == CommsConfig()


def test_comms_config_from_dict_partial_fills_defaults() -> None:
    """A partial mapping overrides only the named field and fills the rest."""
    c = comms_config_from_dict({"satellite": {"satellites_per_launch": 16}})
    assert c.satellite.satellites_per_launch == 16
    # An unspecified field in the same block keeps its default.
    assert c.satellite.satellite_build_cost_musd == SATELLITE_BUILD_COST_MUSD_DEFAULT


def test_comms_config_from_dict_revenue_block_overrides() -> None:
    """A revenue-block mapping overrides the named revenue field and fills the rest."""
    c = comms_config_from_dict({"revenue": {"arpu_usd_per_month": 80.0}})
    assert c.revenue.arpu_usd_per_month == pytest.approx(80.0)
    # The unspecified multiple keeps its default.
    assert c.revenue.revenue_multiple == REVENUE_MULTIPLE_DEFAULT


def test_load_comms_config_empty_file_is_all_defaults(tmp_path: Path) -> None:
    """An empty YAML file loads as an all-defaults ``CommsConfig``."""
    empty = tmp_path / "empty.yaml"
    empty.write_text("")
    assert load_comms_config(empty) == CommsConfig()


def test_load_comms_config_missing_file_raises(tmp_path: Path) -> None:
    """A missing scenario file is the shared file-boundary error, naming the path."""
    with pytest.raises(ModelFileError, match="does_not_exist.yaml: file not found"):
        load_comms_config(tmp_path / "does_not_exist.yaml")


def test_load_comms_config_non_mapping_root_raises(tmp_path: Path) -> None:
    """A YAML list at the root is the shared file-boundary error, not a mapping."""
    bad = tmp_path / "bad.yaml"
    bad.write_text("- just\n- a\n- list\n")
    with pytest.raises(ModelFileError, match="the YAML root must be a mapping, got list"):
        load_comms_config(bad)


def test_load_comms_config_malformed_yaml_raises(tmp_path: Path) -> None:
    """Objective: malformed YAML fails through the shared loader, with its position.

    Expected: a ModelFileError naming the file and the line of the problem,
    not a raw PyYAML parser traceback.
    """
    bad = tmp_path / "malformed.yaml"
    bad.write_text("iridium:\n  aperture_m2: [1.0\n", encoding="utf-8")
    with pytest.raises(ModelFileError, match=r"malformed\.yaml: malformed YAML \(.* at line \d+"):
        load_comms_config(bad)


# -- cross-field validators (fail at load) ----------------------------


def test_coverage_floor_above_cap_fails_at_load(tmp_path: Path) -> None:
    """A coverage floor above the saturation cap fails at config load, with a clear message.

    Objective: the floor-at-or-below-cap rule. Before it existed, a 340 floor over a
    100 cap loaded silently, sized a 100-satellite fleet, and labeled it the coverage
    regime. Expected: that pair fails in a scenario YAML (load_comms_config) and as a
    bare block, naming both fields; a floor equal to the cap loads.
    """
    scenario = tmp_path / "floor_above_cap.yaml"
    scenario.write_text(
        "coverage:\n  satellites_for_full_coverage: 340\n  max_fleet_satellites: 100\n",
        encoding="utf-8",
    )
    with pytest.raises(ValidationError, match="must not exceed coverage.max_fleet_satellites"):
        load_comms_config(scenario)
    with pytest.raises(ValidationError, match="satellites_for_full_coverage"):
        CoverageDials(satellites_for_full_coverage=341, max_fleet_satellites=340)
    equal = CoverageDials(satellites_for_full_coverage=340, max_fleet_satellites=340)
    assert equal.satellites_for_full_coverage == equal.max_fleet_satellites


def test_offpeak_concurrency_above_peak_fails_at_load(tmp_path: Path) -> None:
    """An off-peak concurrency above the busy-hour peak fails at config load.

    Objective: the off-peak-at-or-below-peak rule (off peak is the quieter hour).
    Before it existed, 0.025 off peak over a 0.005 peak loaded and produced an
    off-peak per-user rate below the peak rate. Expected: that pair fails in a
    scenario YAML and as a bare block, naming both fields; equal values load.
    """
    scenario = tmp_path / "offpeak_above_peak.yaml"
    scenario.write_text(
        "iridium:\n  concurrency_peak: 0.005\n  concurrency_offpeak: 0.025\n",
        encoding="utf-8",
    )
    with pytest.raises(ValidationError, match="must not exceed iridium.concurrency_peak"):
        load_comms_config(scenario)
    with pytest.raises(ValidationError, match="concurrency_offpeak"):
        IridiumDials(concurrency_peak=0.01, concurrency_offpeak=0.02)
    equal = IridiumDials(concurrency_peak=0.01, concurrency_offpeak=0.01)
    assert equal.concurrency_offpeak == equal.concurrency_peak
