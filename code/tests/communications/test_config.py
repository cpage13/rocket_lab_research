"""Tests for the clean-rewrite communications config in ``config.py``.

Covers the slim ``CommsConfig`` dial tree: all-defaults construction, the frozen /
``extra="forbid"`` contract, the reused cadence + launch-cost defaults (asserted
both against the comms named constants AND against the shared ``common.cadence``
authority, the drift guard), the new satellite / coverage / comms-share / ground
blocks, the field bounds, and the YAML loader pair. Mirrors the data-center
``test_config.py`` assertion style without importing ``data_center`` (forbidden).
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

# The shared-spine authority the comms cadence + launch-cost defaults must match.
# Importing from ``common`` is allowed; importing ``data_center`` is forbidden.
from common.cadence import (
    CADENCE_CEILING_DEFAULT as COMMON_CADENCE_CEILING_DEFAULT,
)
from common.cadence import (
    FIRST_LAUNCH_YEAR_DEFAULT as COMMON_FIRST_LAUNCH_YEAR_DEFAULT,
)
from common.cadence import (
    HIGH_CADENCE_COST_MUSD_DEFAULT as COMMON_HIGH_CADENCE_COST_MUSD_DEFAULT,
)
from common.cadence import (
    HIGH_CADENCE_LAUNCHES_DEFAULT as COMMON_HIGH_CADENCE_LAUNCHES_DEFAULT,
)
from common.cadence import (
    LAUNCHES_AT_YEAR_5_DEFAULT as COMMON_LAUNCHES_AT_YEAR_5_DEFAULT,
)
from common.cadence import (
    LAUNCHES_AT_YEAR_10_DEFAULT as COMMON_LAUNCHES_AT_YEAR_10_DEFAULT,
)
from common.cadence import (
    LOW_CADENCE_COST_MUSD_DEFAULT as COMMON_LOW_CADENCE_COST_MUSD_DEFAULT,
)
from common.cadence import (
    LOW_CADENCE_LAUNCHES_DEFAULT as COMMON_LOW_CADENCE_LAUNCHES_DEFAULT,
)
from communications.config import (
    CadenceDials,
    CommsCadenceDials,
    CommsConfig,
    CommsMetadataDials,
    CoverageDials,
    GroundInterfaceDials,
    LaunchCostDials,
    SatelliteDials,
    SubscriberDials,
    comms_config_from_dict,
    load_comms_config,
)
from communications.constants import (
    BASE_YEAR_DEFAULT,
    CADENCE_CEILING_DEFAULT,
    COMMS_SHARE_DEFAULT,
    FIRST_LAUNCH_YEAR_DEFAULT,
    GROUND_BASIS_DEFAULT,
    HIGH_CADENCE_COST_MUSD_DEFAULT,
    HORIZON_YEARS_DEFAULT,
    LAUNCHES_AT_YEAR_5_DEFAULT,
    LAUNCHES_AT_YEAR_10_DEFAULT,
    LOW_CADENCE_COST_MUSD_DEFAULT,
    MAX_FLEET_SATELLITES_DEFAULT,
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
    # The ground interface is None by default so the cost side never blocks.
    assert c.ground is None


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


def test_cadence_dials_frozen() -> None:
    """Mutating a frozen nested-block field raises ``ValidationError``."""
    cad = CadenceDials()
    with pytest.raises(ValidationError):
        cad.cadence_ceiling = 99


def test_satellite_dials_frozen() -> None:
    """Mutating the satellite block raises ``ValidationError`` (frozen)."""
    sat = SatelliteDials()
    with pytest.raises(ValidationError):
        sat.satellite_build_cost_musd = 2.0


# -- extra=forbid -----------------------------------------------------


def test_comms_config_rejects_unknown_top_level_block() -> None:
    with pytest.raises(ValidationError):
        CommsConfig.model_validate({"bogus_block": {}})


def test_cadence_dials_rejects_unknown_field() -> None:
    with pytest.raises(ValidationError):
        CadenceDials.model_validate({"bogus": 1})


def test_satellite_dials_rejects_unknown_field() -> None:
    with pytest.raises(ValidationError):
        SatelliteDials.model_validate({"bogus_dial": 1})


def test_ground_interface_dials_rejects_unknown_field() -> None:
    with pytest.raises(ValidationError):
        GroundInterfaceDials.model_validate({"bogus_dial": 1.0})


# -- cadence + launch-cost defaults match the named constants ---------


def test_cadence_dials_defaults() -> None:
    cad = CadenceDials()
    assert cad.cadence_ceiling == CADENCE_CEILING_DEFAULT
    assert cad.launches_at_year_5 == LAUNCHES_AT_YEAR_5_DEFAULT
    assert cad.launches_at_year_10 == LAUNCHES_AT_YEAR_10_DEFAULT
    assert cad.first_launch_year == FIRST_LAUNCH_YEAR_DEFAULT


def test_launch_cost_dials_defaults() -> None:
    lc = LaunchCostDials()
    assert lc.low_cadence_cost_musd == LOW_CADENCE_COST_MUSD_DEFAULT
    assert lc.high_cadence_cost_musd == HIGH_CADENCE_COST_MUSD_DEFAULT


def test_cadence_default_values_are_the_known_anchors() -> None:
    """The reused cadence anchors are the known venture-scenario integers."""
    cad = CadenceDials()
    assert cad.cadence_ceiling == 150
    assert cad.launches_at_year_5 == 14
    assert cad.launches_at_year_10 == 90
    assert cad.first_launch_year == 1


def test_launch_cost_default_values_are_the_known_anchors() -> None:
    """The reused launch-cost anchors are the known $M / cadence pairs."""
    lc = LaunchCostDials()
    assert lc.low_cadence_cost_musd == 25.0
    assert lc.high_cadence_cost_musd == 13.5
    assert lc.low_cadence_launches == 5.0
    assert lc.high_cadence_launches == 100.0


# -- drift guard: comms defaults == common.cadence authority ----------


def test_cadence_defaults_match_common_authority() -> None:
    """The comms cadence + launch-cost defaults equal the shared ``common.cadence``
    exports (the single authority), so the comms config cannot drift from the
    shared spine. Asserted against ``common.cadence``, never ``data_center``.
    """
    cad = CadenceDials()
    lc = LaunchCostDials()
    assert cad.cadence_ceiling == COMMON_CADENCE_CEILING_DEFAULT
    assert cad.launches_at_year_5 == COMMON_LAUNCHES_AT_YEAR_5_DEFAULT
    assert cad.launches_at_year_10 == COMMON_LAUNCHES_AT_YEAR_10_DEFAULT
    assert cad.first_launch_year == COMMON_FIRST_LAUNCH_YEAR_DEFAULT
    assert lc.low_cadence_cost_musd == COMMON_LOW_CADENCE_COST_MUSD_DEFAULT
    assert lc.high_cadence_cost_musd == COMMON_HIGH_CADENCE_COST_MUSD_DEFAULT
    assert lc.low_cadence_launches == COMMON_LOW_CADENCE_LAUNCHES_DEFAULT
    assert lc.high_cadence_launches == COMMON_HIGH_CADENCE_LAUNCHES_DEFAULT


# -- the new dial defaults (the four founder-set values + spec dials) --


def test_satellite_dials_defaults() -> None:
    sat = SatelliteDials()
    assert sat.satellites_per_launch == SATELLITES_PER_LAUNCH_DEFAULT
    assert sat.satellite_lifetime_years == SATELLITE_LIFETIME_YEARS_DEFAULT
    assert sat.satellite_build_cost_musd == SATELLITE_BUILD_COST_MUSD_DEFAULT


def test_coverage_dials_default_floor_is_founder_set_340() -> None:
    """The coverage FLOOR default is the founder-set 340 (the lower fleet bound)."""
    cov = CoverageDials()
    assert cov.satellites_for_full_coverage == SATELLITES_FOR_FULL_COVERAGE_DEFAULT
    assert cov.satellites_for_full_coverage == 340


def test_coverage_dials_default_cap_is_founder_set_2000() -> None:
    """The saturation CAP default is the founder-set 2,000 (the upper fleet bound)."""
    cov = CoverageDials()
    assert cov.max_fleet_satellites == MAX_FLEET_SATELLITES_DEFAULT
    assert cov.max_fleet_satellites == 2_000


def test_comms_cadence_default_share_is_founder_set() -> None:
    cc = CommsCadenceDials()
    assert cc.share_of_fleet == COMMS_SHARE_DEFAULT
    assert cc.share_of_fleet == pytest.approx(0.18)


def test_subscriber_dials_defaults() -> None:
    """The subscriber target default is the founder baseline 10M; density 75,000."""
    subs = SubscriberDials()
    # The target (the base to serve) is the 10M baseline.
    assert subs.subscribers_at_full_coverage == SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT
    assert subs.subscribers_at_full_coverage == 10_000_000
    # The per-satellite attached density (the capacity dial) is the 75,000 central.
    assert subs.subscribers_per_satellite == SUBSCRIBERS_PER_SATELLITE_DEFAULT
    assert subs.subscribers_per_satellite == 75_000
    # The optional direct override defaults to None (the target is the served base).
    assert subs.subscribers_served_override is None


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


def test_load_comms_config_empty_file_is_all_defaults(tmp_path: Path) -> None:
    """An empty YAML file loads as an all-defaults ``CommsConfig``."""
    empty = tmp_path / "empty.yaml"
    empty.write_text("")
    assert load_comms_config(empty) == CommsConfig()


def test_load_comms_config_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_comms_config(tmp_path / "does_not_exist.yaml")


def test_load_comms_config_non_mapping_root_raises(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("- just\n- a\n- list\n")
    with pytest.raises(ValueError, match="must contain a YAML mapping"):
        load_comms_config(bad)
