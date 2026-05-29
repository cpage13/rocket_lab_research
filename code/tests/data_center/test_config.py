"""Tests for the cycle-2 v8 config models in ``config.py``.

Covers the four enums, the four dial blocks (CadenceDials, FleetDials,
VolumeDials, LaunchCostDials), the R-band models (RBand, YearRValue),
MetadataConfig, the extended ValuationConfig, and YAML scenario loading.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from data_center.config import (
    BindingConstraint,
    CadenceDials,
    FleetDials,
    LaunchCostDials,
    MetadataConfig,
    OperatorModel,
    RadiatorArchitecture,
    RBand,
    ValuationConfig,
    VolumeDials,
    WorkloadType,
    YearRValue,
    config_from_dict,
)
from data_center.constants import (
    CADENCE_CEILING_DEFAULT,
    FIRST_LAUNCH_YEAR_DEFAULT,
    HIGH_CADENCE_COST_MUSD_DEFAULT,
    LOW_CADENCE_COST_MUSD_DEFAULT,
    SERVICE_LIFE_YEARS,
)

# -- enums ------------------------------------------------------------


def test_workload_type_inference_only() -> None:
    """WorkloadType has exactly one member, INFERENCE (D14)."""
    assert WorkloadType.INFERENCE.value == "inference"
    assert [m.value for m in WorkloadType] == ["inference"]


def test_operator_model_b2b_dedicated() -> None:
    assert OperatorModel.B2B_DEDICATED_OPTICAL_RF.value == "b2b_dedicated_optical_rf"


def test_radiator_architecture_single_face_only() -> None:
    """RadiatorArchitecture has exactly one member (D16, no proliferation)."""
    assert RadiatorArchitecture.SINGLE_FACE_CO_MOUNTED.value == "single_face_co_mounted"
    assert [m.value for m in RadiatorArchitecture] == ["single_face_co_mounted"]


def test_binding_constraint_members() -> None:
    assert {m.value for m in BindingConstraint} == {"mass", "volume", "both", "neither"}


# -- CadenceDials -----------------------------------------------------


def test_cadence_dials_defaults() -> None:
    c = CadenceDials()
    assert c.cadence_ceiling == CADENCE_CEILING_DEFAULT
    assert c.first_launch_year == FIRST_LAUNCH_YEAR_DEFAULT


def test_cadence_dials_rejects_unknown_field() -> None:
    with pytest.raises(ValidationError):
        CadenceDials.model_validate({"bogus": 1})


def test_cadence_dials_rejects_nonpositive_ceiling() -> None:
    with pytest.raises(ValidationError):
        CadenceDials(cadence_ceiling=0.0)


def test_cadence_dials_frozen() -> None:
    c = CadenceDials()
    with pytest.raises(ValidationError):
        c.cadence_ceiling = 99.0


# -- FleetDials -------------------------------------------------------


def test_fleet_dials_default_service_life() -> None:
    assert FleetDials().service_life_years == SERVICE_LIFE_YEARS


def test_fleet_dials_rejects_out_of_range_service_life() -> None:
    with pytest.raises(ValidationError):
        FleetDials(service_life_years=0)
    with pytest.raises(ValidationError):
        FleetDials(service_life_years=21)


# -- VolumeDials ------------------------------------------------------


def test_volume_dials_defaults() -> None:
    v = VolumeDials()
    assert v.fold_ratio > 0
    assert 0 < v.si_bol_efficiency < 1


def test_volume_dials_rejects_efficiency_above_one() -> None:
    with pytest.raises(ValidationError):
        VolumeDials(si_bol_efficiency=1.5)


def test_volume_dials_rejects_unknown_field() -> None:
    with pytest.raises(ValidationError):
        VolumeDials.model_validate({"bogus_dial": 1.0})


# -- LaunchCostDials --------------------------------------------------


def test_launch_cost_dials_defaults() -> None:
    lc = LaunchCostDials()
    assert lc.low_cadence_cost_musd == LOW_CADENCE_COST_MUSD_DEFAULT
    assert lc.high_cadence_cost_musd == HIGH_CADENCE_COST_MUSD_DEFAULT


def test_launch_cost_dials_rejects_old_v7_field_name() -> None:
    """The v7 field name ``launch_y0_musd`` must fail-fast (D24, no shim)."""
    with pytest.raises(ValidationError):
        LaunchCostDials.model_validate({"launch_y0_musd": 25.0})


# -- RBand / YearRValue -----------------------------------------------


def test_rband_defaults_have_six_anchors_per_band() -> None:
    rb = RBand()
    assert len(rb.central) == 6
    assert len(rb.low) == 6
    assert len(rb.high) == 6


def test_rband_default_central_starts_at_1_50() -> None:
    rb = RBand()
    assert rb.central[0].fy == 2026
    assert rb.central[0].r == pytest.approx(1.50)
    assert rb.central[-1].fy == 2036
    assert rb.central[-1].r == pytest.approx(1.50)


def test_rband_default_high_above_central_above_low() -> None:
    rb = RBand()
    assert rb.high[0].r > rb.central[0].r > rb.low[0].r


def test_rband_rejects_single_anchor() -> None:
    with pytest.raises(ValidationError):
        RBand(central=[YearRValue(fy=2026, r=1.5)])


def test_rband_rejects_unsorted_anchors() -> None:
    with pytest.raises(ValidationError):
        RBand(
            central=[
                YearRValue(fy=2030, r=1.4),
                YearRValue(fy=2026, r=1.5),
            ]
        )


def test_year_r_value_rejects_nonpositive_r() -> None:
    with pytest.raises(ValidationError):
        YearRValue(fy=2026, r=0.0)


def test_year_r_value_rejects_out_of_range_fy() -> None:
    with pytest.raises(ValidationError):
        YearRValue(fy=1999, r=1.5)


# -- MetadataConfig ---------------------------------------------------


def test_metadata_config_enum_defaults_match_d14_d16() -> None:
    m = MetadataConfig(base_year=2026, horizon_years=10)
    assert m.workload_type is WorkloadType.INFERENCE
    assert m.operator_model is OperatorModel.B2B_DEDICATED_OPTICAL_RF
    assert m.radiator_architecture is RadiatorArchitecture.SINGLE_FACE_CO_MOUNTED
    assert m.deployment_philosophy == "ground_validated_before_launch"


def test_metadata_config_requires_base_year_and_horizon() -> None:
    with pytest.raises(ValidationError):
        MetadataConfig.model_validate({})


def test_metadata_config_rejects_out_of_range_horizon() -> None:
    with pytest.raises(ValidationError):
        MetadataConfig(base_year=2026, horizon_years=3)
    with pytest.raises(ValidationError):
        MetadataConfig(base_year=2026, horizon_years=25)


def test_metadata_config_rejects_unknown_field() -> None:
    with pytest.raises(ValidationError):
        MetadataConfig.model_validate({"base_year": 2026, "horizon_years": 10, "bogus": 1})


# -- ValuationConfig v8 blocks ----------------------------------------


def test_valuation_config_default_construction_has_all_v8_blocks() -> None:
    """ValuationConfig() with no args yields every v8 block as a default."""
    cfg = ValuationConfig()
    assert isinstance(cfg.metadata, MetadataConfig)
    assert isinstance(cfg.cadence, CadenceDials)
    assert isinstance(cfg.fleet, FleetDials)
    assert isinstance(cfg.volume, VolumeDials)
    assert isinstance(cfg.r_band, RBand)
    assert isinstance(cfg.launch_cost, LaunchCostDials)


def test_valuation_config_default_metadata_is_central_case() -> None:
    cfg = ValuationConfig()
    assert cfg.metadata.base_year == 2026
    assert cfg.metadata.horizon_years == 10
    assert cfg.metadata.workload_type is WorkloadType.INFERENCE


def test_valuation_config_rejects_unknown_top_level_block() -> None:
    with pytest.raises(ValidationError):
        ValuationConfig.model_validate({"bogus_block": {}})


def test_valuation_config_accepts_v8_blocks_from_dict() -> None:
    """A v8-shaped mapping round-trips through model_validate."""
    cfg = ValuationConfig.model_validate(
        {
            "metadata": {"base_year": 2026, "horizon_years": 10},
            "cadence": {"cadence_ceiling": 120.0},
            "r_band": {
                "central": [
                    {"fy": 2026, "r": 1.5},
                    {"fy": 2036, "r": 1.3},
                ]
            },
        }
    )
    assert cfg.cadence.cadence_ceiling == pytest.approx(120.0)
    assert len(cfg.r_band.central) == 2


# -- v8 field-rename fail-fast (T21) ----------------------------------


def test_scenario_with_old_launch_y0_field_fails_fast() -> None:
    """A scenario using the v7 ``launch_y0_musd`` name must fail-fast (D24)."""
    with pytest.raises(ValidationError) as exc:
        config_from_dict({"launch_cost": {"launch_y0_musd": 25.0}})
    assert "launch_y0_musd" in str(exc.value)


def test_scenario_with_old_launch_y10_field_fails_fast() -> None:
    """The v7 ``launch_y10_musd`` name must fail-fast in launch_cost."""
    with pytest.raises(ValidationError):
        config_from_dict({"launch_cost": {"launch_y10_musd": 13.5}})


def test_scenario_with_unknown_cadence_field_fails_fast() -> None:
    """An unknown key in the cadence block fails-fast (extra='forbid')."""
    with pytest.raises(ValidationError):
        config_from_dict({"cadence": {"bogus_cadence_dial": 1.0}})
