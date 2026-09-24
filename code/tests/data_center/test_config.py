"""Tests for the cycle-2 v8 config models in ``config.py``.

Covers the four enums, the data-center dial blocks (FleetDials, VolumeDials),
the R-band models (RBand, YearRValue), MetadataConfig, the extended
ValuationConfig (its ``cadence`` and ``launch_cost`` blocks are the shared
:mod:`common.cadence` classes, whose own defaults and bounds are tested in
``tests/common/test_cadence_move.py``; their load-time validators are
exercised here through ``config_from_dict``), and YAML scenario loading.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from common.cadence import CadenceDials, LaunchCostDials
from data_center.config import (
    BindingConstraint,
    FleetDials,
    MetadataConfig,
    OperatorModel,
    RadiatorArchitecture,
    RBand,
    ValuationConfig,
    VolumeDials,
    WorkloadType,
    YearRValue,
    config_from_dict,
    load_config,
)
from data_center.constants import SERVICE_LIFE_YEARS
from data_center.engine import run_valuation
from data_center.generations import KNOWN_GENS

# -- enums ------------------------------------------------------------


def test_workload_type_inference_only() -> None:
    """WorkloadType has exactly one member, INFERENCE (D14)."""
    assert WorkloadType.INFERENCE.value == "inference"
    assert [m.value for m in WorkloadType] == ["inference"]


def test_operator_model_b2b_dedicated() -> None:
    assert OperatorModel.B2B_DEDICATED_OPTICAL_RF.value == "b2b_dedicated_optical_rf"


def test_radiator_architecture_two_members() -> None:
    """RadiatorArchitecture has exactly the two real architecture classes.

    The co-mounted member is the D16 conservative posture; the deployed
    double-sided member is the AI-1-class default (investor decision
    2026-07-14). No MIXED member: one architecture per run.
    """
    assert RadiatorArchitecture.SINGLE_FACE_CO_MOUNTED.value == "single_face_co_mounted"
    assert RadiatorArchitecture.DEPLOYED_DOUBLE_SIDED.value == "deployed_double_sided"
    assert [m.value for m in RadiatorArchitecture] == [
        "single_face_co_mounted",
        "deployed_double_sided",
    ]


def test_binding_constraint_members() -> None:
    assert {m.value for m in BindingConstraint} == {"mass", "volume", "both", "neither"}


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
    assert v.stowed_pitch_mm > 0
    assert 0 < v.si_bol_efficiency < 1


def test_volume_dials_rejects_efficiency_above_one() -> None:
    with pytest.raises(ValidationError):
        VolumeDials(si_bol_efficiency=1.5)


def test_volume_dials_rejects_unknown_field() -> None:
    with pytest.raises(ValidationError):
        VolumeDials.model_validate({"bogus_dial": 1.0})


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


def test_metadata_config_enum_defaults_match_decisions() -> None:
    """Enum defaults: D14, D15, and the 2026-07-14 radiator-architecture rebase."""
    m = MetadataConfig(base_year=2026, horizon_years=10)
    assert m.workload_type is WorkloadType.INFERENCE
    assert m.operator_model is OperatorModel.B2B_DEDICATED_OPTICAL_RF
    assert m.radiator_architecture is RadiatorArchitecture.DEPLOYED_DOUBLE_SIDED
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


# -- Cross-field validators: invalid combinations fail at load ---------
#
# Each case below used to load cleanly and then either crash mid-run with a
# traceback or run into nonsense output. Every one must now fail at load
# with a ValidationError whose message names the broken rule.


def test_fixed_node_mass_at_or_above_envelope_fails_at_load() -> None:
    """Objective: a node whose fixed mass fills the envelope cannot be built.

    ``node_mass_fixed_t: 13.0`` on the 12.5 t envelope used to give N = -4,
    negative kW and cost, and positive revenue. Expected: it fails at load,
    as does a fixed mass exactly equal to the envelope.
    """
    with pytest.raises(ValidationError, match="node_mass_fixed_t must be below mass_envelope_t"):
        config_from_dict({"gospel": {"node_mass_fixed_t": 13.0}})
    with pytest.raises(ValidationError, match="node_mass_fixed_t must be below mass_envelope_t"):
        config_from_dict({"gospel": {"mass_envelope_t": 10.0, "node_mass_fixed_t": 10.0}})


@pytest.mark.parametrize(
    "cadence",
    [
        {"launches_at_year_5": 0},
        {"launches_at_year_5": 90, "launches_at_year_10": 90},
        {"launches_at_year_5": 50, "launches_at_year_10": 40},
        {"launches_at_year_10": 150},
        {"cadence_ceiling": 80},
    ],
    ids=["y5_zero", "y5_equals_y10", "y10_below_y5", "y10_at_ceiling", "ceiling_below_y10"],
)
def test_cadence_anchors_outside_the_logistic_range_fail_at_load(cadence: dict[str, int]) -> None:
    """Objective: cadence anchors must satisfy 0 < y5 < y10 < ceiling at load.

    These used to pass load and then raise a ValueError traceback from the
    logistic fit in ``common.cadence``. Expected: a ValidationError at load.
    """
    with pytest.raises(ValidationError, match="0 < launches_at_year_5 < launches_at_year_10"):
        config_from_dict({"cadence": cadence})


def test_reversed_launch_cost_anchors_fail_at_load() -> None:
    """Objective: the low-cost anchor must sit at the lower cadence.

    Reversed anchors used to flat-clamp every year to the low-cadence cost,
    silently switching the cost-down off (FY2036 revenue $8,184M instead of
    $7,419M). Expected: a ValidationError at load; equal cadences fail too.
    """
    with pytest.raises(ValidationError, match="low_cadence_launches < high_cadence_launches"):
        config_from_dict(
            {"launch_cost": {"low_cadence_launches": 100.0, "high_cadence_launches": 5.0}}
        )
    with pytest.raises(ValidationError, match="low_cadence_launches < high_cadence_launches"):
        config_from_dict(
            {"launch_cost": {"low_cadence_launches": 50.0, "high_cadence_launches": 50.0}}
        )


def test_r_band_out_of_order_fails_at_load() -> None:
    """Objective: the R band must keep low <= central <= high at shared years.

    ``low 3.0, central 1.5, high 1.1`` used to load and pass every rule.
    Expected: a ValidationError naming the out-of-order anchor year.
    """
    with pytest.raises(ValidationError, match="R band out of order at fy 2026"):
        config_from_dict(
            {
                "r_band": {
                    "low": [{"fy": 2026, "r": 3.0}, {"fy": 2036, "r": 3.0}],
                    "central": [{"fy": 2026, "r": 1.5}, {"fy": 2036, "r": 1.5}],
                    "high": [{"fy": 2026, "r": 1.1}, {"fy": 2036, "r": 1.1}],
                }
            }
        )


def test_r_band_central_above_high_fails_at_load() -> None:
    """Objective: central above high at one shared year fails at load.

    Expected: a ValidationError naming the anchor year (2036) where central
    exceeds high, even though every other year is in order.
    """
    with pytest.raises(ValidationError, match="R band out of order at fy 2036"):
        config_from_dict({"r_band": {"central": [{"fy": 2026, "r": 1.5}, {"fy": 2036, "r": 1.9}]}})


def test_r_band_duplicate_anchor_year_fails_at_load() -> None:
    """Objective: a repeated anchor year (which silently collapsed) fails at load.

    Expected: a ValidationError naming the repeated year.
    """
    with pytest.raises(ValidationError, match="must not repeat an anchor year"):
        RBand(
            central=[
                YearRValue(fy=2026, r=1.5),
                YearRValue(fy=2026, r=1.6),
                YearRValue(fy=2036, r=1.5),
            ]
        )


@pytest.mark.parametrize("bus_growth_pre", [-1.0, -1.5])
def test_bus_decline_of_100_percent_or_more_fails_at_load(bus_growth_pre: float) -> None:
    """Objective: ``bus_growth_pre <= -1`` would zero or sign-flip the bus cost.

    Expected: a ValidationError at load; -0.99 still loads.
    """
    with pytest.raises(ValidationError, match="bus_growth_pre"):
        config_from_dict({"gospel": {"bus_growth_pre": bus_growth_pre}})
    assert config_from_dict({"gospel": {"bus_growth_pre": -0.99}}).gospel.bus_growth_pre == -0.99


def test_window_past_max_fy_fails_at_load() -> None:
    """Objective: the generation extension of a late window must stay within MAX_FY.

    Expected: base year 2075 with a ten-year horizon (extension to 2086)
    fails at load; base year 2060 with a 19-year horizon (to 2080) loads.
    """
    with pytest.raises(ValidationError, match="must not exceed 2080"):
        MetadataConfig(base_year=2075, horizon_years=10)
    assert MetadataConfig(base_year=2060, horizon_years=19).base_year == 2060


def test_every_shipped_data_center_scenario_still_loads(scenarios_dir: Path) -> None:
    """Objective: the new validators reject no shipped scenario.

    Expected: all seven data-center scenario files load.
    """
    for name in (
        "default",
        "ai1_equivalent",
        "ambitious",
        "conservative",
        "upside_7yr",
        "volume_stress",
        "with_premium",
    ):
        assert load_config(scenarios_dir / f"{name}.yaml").scenario_name


@pytest.mark.parametrize("base_year", [2020, 2022, 2024])
def test_base_year_before_the_first_generation_fails_at_load(base_year: int) -> None:
    """Objective: every window year must have a frontier GPU generation.

    The bundled roadmap starts with B200/GB200, dated 2024.5. The original
    trigger: base years 2020 to 2024 loaded, then crashed mid-run with a
    ``NoFrontierAvailableError`` traceback. Expected: they fail at load with
    a ValidationError naming the earliest generation and the first valid
    base year (2025), which loads and runs.
    """
    metadata = {"base_year": base_year, "horizon_years": 10}
    with pytest.raises(ValidationError, match="base year must be 2025 or later"):
        config_from_dict({"metadata": metadata})
    first_valid = config_from_dict({"metadata": {"base_year": 2025, "horizon_years": 10}})
    assert run_valuation(first_valid).physical.years["2025"].gpus_per_node.value


def test_base_year_check_reads_the_scenarios_own_generation_list() -> None:
    """Objective: the base-year check follows a scenario's own roadmap.

    Expected: pinning the roadmap to the 2026.5 Rubin entry alone rejects
    base year 2026 (nothing flies that year) and accepts 2027.
    """
    rubin = next(g for g in KNOWN_GENS if g.name == "Rubin VR200").model_dump(mode="json")
    with pytest.raises(ValidationError, match="the earliest, Rubin VR200, is available in 2026.5"):
        config_from_dict({"generations": [rubin]})
    pinned = config_from_dict(
        {"generations": [rubin], "metadata": {"base_year": 2027, "horizon_years": 10}}
    )
    assert pinned.metadata.base_year == 2027
