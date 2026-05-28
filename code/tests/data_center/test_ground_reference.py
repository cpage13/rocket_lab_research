"""Tests for the typed ground reference model and promoted JSON contract."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_center import cli
from data_center.config import load_config
from data_center.engine import run_valuation
from data_center.ground import (
    ANCHOR_YEAR,
    GroundReferenceOutput,
    build_ground_reference_output,
    default_ground_source_catalog,
    load_ground_config,
    render_ground_json,
)
from data_center.output import SpaceModelOutput

ANCHOR_YEAR_KEY = str(ANCHOR_YEAR)
DEFAULT_SCENARIO = Path("scenarios/default.yaml")
GROUND_SCENARIO = Path("scenarios/ground_default.yaml")
REQUIRED_GROUND_INPUTS = {
    "inputs.config.gpu_package_cost_multiplier",
    "inputs.config.facility_shell_fitout_musd_per_mw",
    "inputs.config.racked_power_network_musd_per_gpu_package",
    "inputs.config.energy_price_usd_per_mwh",
    "inputs.config.pue",
    "inputs.config.utilization",
    "inputs.config.operations_maintenance_musd_per_mw_year",
    "inputs.config.cooling_cost_musd_per_mw",
    "inputs.config.comparison_period_years",
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
        default_ground_source_catalog(),
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
    assert rebuilt.ground.source_status_summary["placeholder"] == 0
    assert rebuilt.ground.source_status_summary["sourced_estimate"] == 2
    assert rebuilt.ground.source_status_summary["scenario"] == 7
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
