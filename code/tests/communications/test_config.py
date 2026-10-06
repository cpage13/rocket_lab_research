"""Tests for the clean-rewrite communications config in ``config.py``.

Covers the slim ``CommsConfig`` dial tree: all-defaults construction, the frozen /
``extra="forbid"`` contract, the shared cadence and launch-cost blocks (the
``common.cadence`` classes themselves, with their load-time validators; the
classes' own defaults and bounds are tested once, in
``tests/common/test_cadence_move.py``), the satellite / coverage / comms-share /
ground blocks, the field bounds, the cross-field validators (coverage floor at or
below the cap, the fleet cap at its default on an Iridium config, off-peak concurrency at
or below the peak), every float dial of an Iridium config finite, the YAML loader pair,
and the Iridium saturation block (its defaults, the shipped scenario's block, its bounds).
Mirrors the data-center
``test_config.py`` assertion style without importing ``data_center`` (forbidden).
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import get_args

import pytest
import yaml
from pydantic import BaseModel, ValidationError

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
    SaturationDials,
    SubscriberDials,
    comms_config_from_dict,
    load_comms_config,
)
from communications.constants import (
    ARPU_USD_PER_MONTH_DEFAULT,
    BASE_YEAR_DEFAULT,
    COMMS_SHARE_DEFAULT,
    DOWNLINK_SHARE_DEFAULT,
    GROUND_BASIS_DEFAULT,
    HORIZON_YEARS_DEFAULT,
    MAX_FLEET_SATELLITES_DEFAULT,
    REVENUE_MULTIPLE_DEFAULT,
    SATELLITE_BUILD_COST_MUSD_DEFAULT,
    SATELLITE_LIFETIME_YEARS_DEFAULT,
    SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
    SATELLITES_PER_LAUNCH_DEFAULT,
    SATURATION_CURVE_PATH_DEFAULT,
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


@pytest.mark.parametrize("cap", [MAX_FLEET_SATELLITES_DEFAULT - 1, 3_000])
def test_an_iridium_config_refuses_a_fleet_cap_other_than_its_default(
    tmp_path: Path, cap: int
) -> None:
    """Objective: the fleet cap is a setting of the cellular family only; an Iridium config keeps
    it at its default (2,000), which still caps the Iridium model's fleet until that model sizes
    its own, and is refused at load otherwise, naming the field. The test is on the value, so a
    config written out whole (every field set) still loads.

    Sample: a scenario with an ``iridium:`` block and ``coverage.max_fleet_satellites`` at
    1,999, then 3,000; the same scenario without the ``iridium:`` block; an Iridium scenario
    writing the cap at its default; the default Iridium config round-tripped through
    ``model_dump`` and ``model_validate``.

    Expected outcome: the Iridium scenario fails at load (a ValidationError, a ValueError)
    naming ``coverage.max_fleet_satellites``, its default and the value; the cellular one loads
    with the value; the cap written at its default and the round trip both load.
    """
    scenario = tmp_path / "capped.yaml"
    scenario.write_text(
        f"coverage:\n  max_fleet_satellites: {cap}\niridium:\n  spectrum_mhz: 8.0\n",
        encoding="utf-8",
    )
    with pytest.raises(ValidationError) as refused:
        load_comms_config(scenario)
    assert (
        "coverage.max_fleet_satellites is not a setting on an Iridium config (one with an "
        f"'iridium:' block): it keeps its default, {MAX_FLEET_SATELLITES_DEFAULT}, the "
        "cellular family's fleet cap, which also caps the Iridium model's fleet until that "
        f"model sizes its own; got {cap}"
    ) in str(refused.value)
    scenario.write_text(f"coverage:\n  max_fleet_satellites: {cap}\n", encoding="utf-8")
    assert load_comms_config(scenario).coverage.max_fleet_satellites == cap
    scenario.write_text(
        f"coverage:\n  max_fleet_satellites: {MAX_FLEET_SATELLITES_DEFAULT}\n"
        "iridium:\n  spectrum_mhz: 8.0\n",
        encoding="utf-8",
    )
    assert load_comms_config(scenario).coverage.max_fleet_satellites == (
        MAX_FLEET_SATELLITES_DEFAULT
    )
    whole = CommsConfig(iridium=IridiumDials()).model_dump()
    assert CommsConfig.model_validate(whole).iridium == IridiumDials()


def _float_dial_paths(block: type[BaseModel]) -> list[tuple[str, ...]]:
    """Every float field's path in a dial block and in the blocks nested in it, walked from the
    block's own fields (so a field added later is walked too)."""
    paths: list[tuple[str, ...]] = []
    for name, field in block.model_fields.items():
        members = get_args(field.annotation) or (field.annotation,)
        nested = [
            member
            for member in members
            if isinstance(member, type) and issubclass(member, BaseModel)
        ]
        if nested:
            paths += [(name, *path) for path in _float_dial_paths(nested[0])]
        elif float in members:
            paths.append((name,))
    return paths


def test_the_iridium_dials_refuse_a_number_that_is_not_finite_naming_the_field(
    tmp_path: Path,
) -> None:
    """Objective: no run starts from a NaN or an infinity: every float dial of an Iridium config
    is refused at load when it is not finite, naming the field (before the fix an infinite
    aperture or spectral efficiency loaded and ended the promotion command in a traceback, and
    an infinite spectrum was refused naming an internal model, not the field).

    Sample: every float field of the Iridium dials and of the blocks nested in them (the
    saturation and ARPU blocks), walked from the model's own fields, each written in a scenario
    YAML as ``.inf``, ``-.inf`` and ``.nan`` in turn.

    Expected outcome: the walk finds the spectrum and the aperture among others; each scenario
    fails at load with one ValidationError, located at that field (``iridium.aperture_m2``,
    say).
    """
    paths = _float_dial_paths(IridiumDials)
    assert {("spectrum_mhz",), ("aperture_m2",), ("saturation", "downlink_share")} <= set(paths)
    scenario = tmp_path / "not_finite.yaml"
    for path in paths:
        for value in (math.inf, -math.inf, math.nan):
            dials: object = value
            for key in reversed(path):
                dials = {key: dials}
            scenario.write_text(yaml.safe_dump({"iridium": dials}), encoding="utf-8")
            with pytest.raises(ValidationError) as refused:
                load_comms_config(scenario)
            located = [".".join(map(str, error["loc"])) for error in refused.value.errors()]
            assert located == [".".join(("iridium", *path))], (path, value)


# -- the Iridium saturation block (ADRs 005 and 008) ---------------------


def test_every_iridium_config_carries_the_saturation_block(iridium_yaml: Path) -> None:
    """Objective: the saturation block is defaulted on every Iridium config, and the shipped
    scenario writes it out.

    Sample: bare ``IridiumDials()``; ``scenarios/iridium.yaml``.

    Expected outcome: the defaults are the named constants, 0.67 and the promoted curve's
    repository-relative path; the shipped scenario sets the block explicitly
    (``saturation:`` with both fields) and it loads equal to the defaults.
    """
    dials = SaturationDials()
    assert dials.downlink_share == DOWNLINK_SHARE_DEFAULT == 0.67
    assert dials.curve_path == SATURATION_CURVE_PATH_DEFAULT
    assert SATURATION_CURVE_PATH_DEFAULT == "communications/models/iridium/saturation_curve.json"
    assert IridiumDials().saturation == dials
    text = iridium_yaml.read_text(encoding="utf-8")
    assert "\n  saturation:\n    downlink_share: 0.67" in text
    assert "    curve_path: communications/models/iridium/saturation_curve.json" in text
    loaded = load_comms_config(iridium_yaml).iridium
    assert loaded is not None
    assert loaded.saturation == dials


@pytest.mark.parametrize("share", [0.0, 1.5])
def test_a_downlink_share_out_of_bounds_fails_at_load(tmp_path: Path, share: float) -> None:
    """Objective: the downlink share is a fraction above 0 and at most 1.

    Sample: a scenario setting ``iridium.saturation.downlink_share`` to 0, then to 1.5.

    Expected outcome: each fails at load with the field named; 1.0, the band in full-time
    use, loads.
    """
    scenario = tmp_path / "share.yaml"
    scenario.write_text(f"iridium:\n  saturation:\n    downlink_share: {share}\n", encoding="utf-8")
    with pytest.raises(ValidationError, match=r"iridium\.saturation\.downlink_share"):
        load_comms_config(scenario)
    scenario.write_text("iridium:\n  saturation:\n    downlink_share: 1.0\n", encoding="utf-8")
    loaded = load_comms_config(scenario).iridium
    assert loaded is not None
    assert loaded.saturation.downlink_share == 1.0


def test_the_saturation_block_is_frozen_and_refuses_unknown_keys(tmp_path: Path) -> None:
    """Objective: the block follows the config's contract (frozen, ``extra="forbid"``), and its
    curve path may be absolute.

    Expected outcome: assignment and an unknown key raise ValidationError; an absolute path
    loads as given.
    """
    dials = SaturationDials()
    with pytest.raises(ValidationError):
        dials.downlink_share = 0.5
    with pytest.raises(ValidationError):
        SaturationDials.model_validate({"bogus_dial": 1.0})
    absolute = str(tmp_path / "curve.json")
    assert SaturationDials(curve_path=absolute).curve_path == absolute
