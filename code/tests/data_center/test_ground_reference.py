"""Tests for the typed ground reference model and promoted JSON contract."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from data_center import cli
from data_center.config import config_from_dict, load_config
from data_center.engine import run_valuation
from data_center.ground import (
    DEFAULT_GROUND_SCENARIO_PATH,
    HOURS_PER_YEAR,
    GroundReferenceOutput,
    build_ground_reference_output,
    ground_config_from_dict,
    load_ground_config,
    render_ground_json,
)
from data_center.output import ArtifactRole, SpaceModelOutput

# The default window (base year 2026, ten-year horizon) anchors at FY2036.
ANCHOR_YEAR = 2036
ANCHOR_YEAR_KEY = str(ANCHOR_YEAR)
DEFAULT_SCENARIO = Path("scenarios/default.yaml")
GROUND_SCENARIO = Path("scenarios/ground_default.yaml")
SPACE_MODEL_PATH = "data_center/models/space/default.json"

# The recorded default ground invariant (plan invariant table, 2026-09-23).
DEFAULT_GROUND_TOTAL_MUSD = 6558.813903312
DEFAULT_ORBITAL_TOTAL_MUSD = 8396.644819805533
DEFAULT_ORBIT_TO_GROUND_RATIO = 1.2802078155572436
REQUIRED_GROUND_INPUTS = {
    "inputs.config.gpu_package_cost_multiplier",
    "inputs.config.facility_shell_fitout_musd_per_mw",
    "inputs.config.racked_power_network_musd_per_gpu_package",
    "inputs.config.energy_price_usd_per_mwh",
    "inputs.config.pue",
    "inputs.config.utilization",
    "inputs.config.operations_maintenance_musd_per_mw_year",
    "inputs.config.cooling_cost_musd_per_mw",
}


@pytest.fixture(scope="module")
def default_space_output() -> SpaceModelOutput:
    """Run the default space model once for ground-reference tests."""
    return run_valuation(
        load_config(DEFAULT_SCENARIO),
        source_scenario_path="code/scenarios/default.yaml",
        artifact_role="promoted_default",
    )


@pytest.fixture(scope="module")
def default_ground_output(default_space_output: SpaceModelOutput) -> GroundReferenceOutput:
    """Build the default ground reference output once for the module."""
    return build_ground_reference_output(
        default_space_output,
        load_ground_config(GROUND_SCENARIO),
        space_model_path=SPACE_MODEL_PATH,
        ground_scenario_path=DEFAULT_GROUND_SCENARIO_PATH,
    )


def test_ground_anchor_matches_2036_deployed_year_cohort(
    default_space_output: SpaceModelOutput,
    default_ground_output: GroundReferenceOutput,
) -> None:
    """The ground anchor is exactly the 2036 deployed-year cohort, not fleet stock."""
    business_year = default_space_output.business.years[ANCHOR_YEAR_KEY]
    physical_year = default_space_output.physical.years[ANCHOR_YEAR_KEY]
    anchor = default_ground_output.anchor

    assert anchor.year == ANCHOR_YEAR
    assert anchor.basis == "deployed_this_year"
    assert anchor.nodes == business_year.nodes_deployed_this_year.value
    assert anchor.gpu_packages == (
        business_year.nodes_deployed_this_year.value * physical_year.gpus_per_node.value
    )
    assert anchor.kw == (
        business_year.nodes_deployed_this_year.value * physical_year.kw_per_node.value
    )
    assert anchor.service_life_years == (
        default_space_output.inputs.config.fleet.service_life_years.value
    )
    assert "kw_living_fleet" not in anchor.source_paths
    assert "living_fleet" not in anchor.source_paths


def test_ground_reference_contract_is_complete(
    default_ground_output: GroundReferenceOutput,
) -> None:
    """The ground artifact carries inputs, components, costs, warnings, and queries."""
    dumped = json.loads(render_ground_json(default_ground_output))
    rebuilt = GroundReferenceOutput.model_validate(dumped)

    assert set(dumped) == {
        "metadata",
        "anchor",
        "inputs",
        "ground",
        "orbital_reference",
        "comparison",
        "meta",
    }
    assert set(rebuilt.inputs.assumption_index) == REQUIRED_GROUND_INPUTS
    assert rebuilt.ground.total_five_year_cost.value is not None
    assert rebuilt.orbital_reference.five_year_cost_view.value is not None
    assert rebuilt.comparison.ground_to_orbit_ratio.value is not None
    assert rebuilt.ground.included_components
    assert rebuilt.ground.excluded_components
    assert "land acquisition" in rebuilt.ground.excluded_components
    assert "financing costs" in rebuilt.ground.excluded_components
    assert "taxes" in rebuilt.ground.excluded_components
    assert "water costs" in rebuilt.ground.excluded_components
    assert "depreciation accounting" in rebuilt.ground.excluded_components
    assert rebuilt.meta.source_status_summary.placeholder == 0
    assert rebuilt.meta.source_status_summary.sourced_estimate == 2
    assert rebuilt.meta.source_status_summary.scenario == 6
    assert "source_status_summary" not in dumped["ground"]
    assert not rebuilt.ground.warnings
    assert rebuilt.comparison.conclusion_label == "same_order_of_magnitude"
    assert any(query.applies_to == "ground" for query in rebuilt.meta.query_examples)


def test_promote_writes_ground_reference_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Default promotion writes a round-trippable ground reference artifact."""
    model_dir = tmp_path / "models"
    monkeypatch.setattr(cli, "_PROMOTED_MODEL_DIR", model_dir)

    exit_code = cli.main(["--promote"])

    assert exit_code == 0
    ground_path = tmp_path / "ground" / "default.json"
    assert ground_path.is_file()
    rebuilt = GroundReferenceOutput.model_validate(json.loads(ground_path.read_text()))
    assert rebuilt.anchor.year == ANCHOR_YEAR
    assert rebuilt.anchor.basis == "deployed_this_year"
    assert rebuilt.comparison.ground_to_orbit_ratio.value is not None


@pytest.mark.parametrize("pue", [0.5, 0.99])
def test_ground_pue_below_one_fails_at_load(pue: float) -> None:
    """Objective: a PUE below 1 (facility power below the IT load) is rejected.

    Expected: ``ground_config_from_dict`` raises a ValidationError naming pue.
    """
    with pytest.raises(ValidationError, match="pue"):
        ground_config_from_dict({"pue": pue})


def test_ground_utilization_above_one_fails_at_load() -> None:
    """Objective: average IT utilization above 1 is rejected by its own bound.

    Expected: ``ground_config_from_dict`` raises a ValidationError naming
    utilization; exactly 1.0 (always at full load) is accepted.
    """
    with pytest.raises(ValidationError, match="utilization"):
        ground_config_from_dict({"utilization": 1.01})
    assert ground_config_from_dict({"utilization": 1.0}).utilization == 1.0


def _ground_for(space: SpaceModelOutput) -> GroundReferenceOutput:
    """Build the default-assumption ground reference for one space output."""
    return build_ground_reference_output(
        space,
        load_ground_config(GROUND_SCENARIO),
        space_model_path=SPACE_MODEL_PATH,
        ground_scenario_path=DEFAULT_GROUND_SCENARIO_PATH,
    )


def test_default_ground_reproduces_the_recorded_invariant(
    default_ground_output: GroundReferenceOutput,
) -> None:
    """Objective: the default ground comparison stays on its recorded numbers.

    Expected: ground total 6558.813903312, orbital total 8396.644819805533,
    orbit-to-ground ratio 1.2802078155572436, over the default anchor's
    five-year service life, labeled same_order_of_magnitude.
    """
    comparison = default_ground_output.comparison
    assert comparison.ground_total_five_year_cost.value == pytest.approx(
        DEFAULT_GROUND_TOTAL_MUSD, rel=1e-12
    )
    assert comparison.orbital_total_five_year_cost.value == pytest.approx(
        DEFAULT_ORBITAL_TOTAL_MUSD, rel=1e-12
    )
    assert comparison.orbit_to_ground_ratio.value == pytest.approx(
        DEFAULT_ORBIT_TO_GROUND_RATIO, rel=1e-12
    )
    assert default_ground_output.anchor.service_life_years == 5
    assert comparison.conclusion_label == "same_order_of_magnitude"


@pytest.mark.parametrize("service_life_years", [3, 7])
def test_comparison_period_follows_the_anchor_service_life(service_life_years: int) -> None:
    """Objective: the ground window is the anchor cohort's service life.

    With default dials and a 3- or 7-year service life, the ground energy
    and operations lines cover that many years (no separate period dial).
    Expected: ``anchor.service_life_years`` equals the configured life, the
    energy line equals kW x PUE x utilization x hours x life x price, the
    O&M line equals MW x rate x life, and both cite
    ``anchor.service_life_years``.
    """
    space = run_valuation(config_from_dict({"fleet": {"service_life_years": service_life_years}}))
    ground = _ground_for(space)
    assert ground.anchor.service_life_years == service_life_years
    cfg = load_ground_config(GROUND_SCENARIO)
    costs = {c.name: c.cost for c in ground.ground.component_costs}
    expected_energy = (
        ground.anchor.kw
        * cfg.pue
        * cfg.utilization
        * HOURS_PER_YEAR
        * service_life_years
        / 1_000.0
        * cfg.energy_price_usd_per_mwh
        / 1_000_000.0
    )
    assert costs["energy"].value == pytest.approx(expected_energy, rel=1e-12)
    assert costs["operations_maintenance_labor"].value == pytest.approx(
        ground.anchor.kw
        / 1_000.0
        * cfg.operations_maintenance_musd_per_mw_year
        * service_life_years,
        rel=1e-12,
    )
    assert "anchor.service_life_years" in costs["energy"].uses
    assert "anchor.service_life_years" in costs["operations_maintenance_labor"].uses


def test_ground_comparison_period_dial_is_gone() -> None:
    """Objective: the redundant comparison-period dial no longer exists.

    Expected: a ground YAML that still sets it fails at load (typos and
    retired dials fail loudly).
    """
    with pytest.raises(ValidationError, match="comparison_period_years"):
        ground_config_from_dict({"comparison_period_years": 5})


def test_ground_metadata_reflects_the_scenario_actually_loaded(tmp_path: Path) -> None:
    """Objective: a non-default ground YAML is recorded as itself.

    A copy of the default ground assumptions with PUE 1.4, loaded from a
    scratch path. Expected: metadata and ``inputs.scenario`` carry that
    path, the scenario is not the default, the changed PUE cell is a
    scenario override citing only the scenario YAML, and an unchanged cell
    keeps its default claim.
    """
    data = yaml.safe_load(GROUND_SCENARIO.read_text())
    data["pue"] = 1.4
    path = tmp_path / "ground_pue.yaml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    space = run_valuation(load_config(DEFAULT_SCENARIO))
    ground = build_ground_reference_output(
        space,
        load_ground_config(path),
        space_model_path="scratch/space.json",
        ground_scenario_path="scratch/ground_pue.yaml",
    )
    assert ground.metadata.source_scenario_path == "scratch/ground_pue.yaml"
    assert ground.anchor.space_model_path == "scratch/space.json"
    assert ground.inputs.scenario.path == "scratch/ground_pue.yaml"
    assert ground.inputs.scenario.is_default is False
    pue = ground.inputs.config.pue
    assert pue.assumption_role == "scenario_override"
    assert [ref.ref for ref in pue.source_refs] == ["scratch/ground_pue.yaml"]
    energy_price = ground.inputs.config.energy_price_usd_per_mwh
    assert energy_price.assumption_role == "default"
    assert energy_price.source_refs[0].claim_id == "RLDC-GROUND-ENERGY-PRICE-85-MWH"


@pytest.mark.parametrize(
    ("space_role", "ground_role"),
    [
        (ArtifactRole.DRAFT, ArtifactRole.DRAFT),
        (ArtifactRole.PROMOTED_DEFAULT, ArtifactRole.PROMOTED_GROUND_DEFAULT),
        (ArtifactRole.PROMOTED_NAMED, ArtifactRole.PROMOTED_GROUND_NAMED),
    ],
)
def test_ground_artifact_role_follows_the_space_role(
    space_role: ArtifactRole, ground_role: ArtifactRole
) -> None:
    """Objective: one role vocabulary maps a space role to its ground role.

    Expected: a draft space run yields a draft ground reference (never a
    promoted label), and each promoted space role its promoted ground role.
    """
    space = run_valuation(load_config(DEFAULT_SCENARIO), artifact_role=space_role)
    assert _ground_for(space).metadata.artifact_role is ground_role


def test_anchor_check_compares_against_the_space_output(
    default_space_output: SpaceModelOutput,
) -> None:
    """Objective: the anchor check is a real comparison, not a constant pass.

    Expected: the default passes; a space output whose anchor-year deployed
    kW cell disagrees with nodes x kW per node fails the check.
    """
    assert _ground_for(default_space_output).meta.validation_results[0].severity == "pass"
    year = default_space_output.business.years[ANCHOR_YEAR_KEY]
    tampered_year = year.model_copy(
        update={
            "kw_deployed_this_year": year.kw_deployed_this_year.model_copy(update={"value": 1.0})
        }
    )
    tampered = default_space_output.model_copy(
        update={
            "business": default_space_output.business.model_copy(
                update={
                    "years": {
                        **default_space_output.business.years,
                        ANCHOR_YEAR_KEY: tampered_year,
                    }
                }
            )
        }
    )
    result = _ground_for(tampered).meta.validation_results[0]
    assert result.validation_id == f"ground_anchor_{ANCHOR_YEAR}_deployed_year"
    assert result.severity == "fail"


def test_ground_data_dictionary_is_generated_from_the_artifact(
    default_ground_output: GroundReferenceOutput,
) -> None:
    """Objective: the shared builder generates the ground data dictionary.

    Expected: one entry per ground leaf (far more than the old five
    hand-written entries), numeric anchor fields typed as numbers (not the
    old int|float "string"), and cell units equal to the cells' own units.
    """
    entries = {e.path: e for e in default_ground_output.meta.data_dictionary}
    assert len(entries) > 100
    assert entries["anchor.nodes"].type == "integer"
    assert entries["anchor.kw"].type == "number"
    assert entries["anchor.service_life_years"].unit == "years"
    assert entries["ground.total_five_year_cost"].unit == (
        default_ground_output.ground.total_five_year_cost.unit
    )
    assert entries["comparison.ground_to_orbit_ratio"].unit == "ratio"
    assert entries["inputs.config.utilization"].unit == "fraction"
