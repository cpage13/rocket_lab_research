"""End-to-end tests for the space artifact's ``inputs`` contract.

The input manifest publishes every scenario input as a source-linked cell in
a typed tree and a flat ``assumption_index``. These tests run real scenarios
and assert the contract a cold reader relies on:

* the flat index holds every cell of the typed tree, the R-band anchors
  included, and the source-status summary counts exactly those cells;
* the source metadata of the dials the 2026-07-14 rebase changed describes
  the current investor-set posture, and the cadence ceiling is described as
  the horizon-scoped parameter it is;
* a value a scenario changed from the default is published as a scenario
  override, never under the default's claim, rationale, or role, and labels
  are config-derived rather than tied to one calendar year;
* the generation summaries and the generation input cells use one
  source-status vocabulary.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from data_center.config import ValuationConfig, load_config
from data_center.engine import run_valuation
from data_center.input_manifest import InputCell, collect_input_cells
from data_center.output import ValuationOutput

_SCENARIOS = Path(__file__).resolve().parents[2] / "scenarios"

# Default cell count: 101 scalar and generation cells plus the 18 R-band
# anchor cells (three bands of six anchors).
_DEFAULT_INDEX_SIZE = 119


def _run(name: str) -> ValuationOutput:
    """Run one shipped scenario, recording its repository path as the CLI does."""
    return run_valuation(
        load_config(_SCENARIOS / f"{name}.yaml"),
        source_scenario_path=f"code/scenarios/{name}.yaml",
    )


def _claims(cell: InputCell) -> set[str]:
    """Return every claim ID a cell cites."""
    return {ref.claim_id for ref in cell.source_refs if ref.claim_id is not None}


@pytest.mark.parametrize("name", ["default", "conservative", "ambitious"])
def test_assumption_index_holds_every_cell_of_the_typed_tree(name: str) -> None:
    """Objective: the flat index is complete (the R-band anchors were missing).

    Expected: the index keys equal the paths of every cell in the typed
    tree, the central 2026 anchor is indexed, the source-status summary
    counts every indexed cell, and the default index has 119 entries.
    """
    output = _run(name)
    tree_paths = [cell.path for cell in collect_input_cells(output.inputs.config)]
    assert len(tree_paths) == len(set(tree_paths))
    assert set(output.inputs.assumption_index) == set(tree_paths)
    assert "inputs.config.revenue.central.2026" in output.inputs.assumption_index
    summary = output.meta.source_status_summary
    assert sum(summary.model_dump().values()) == len(output.inputs.assumption_index)
    if name == "default":
        assert len(output.inputs.assumption_index) == _DEFAULT_INDEX_SIZE


def test_radiator_dials_describe_the_investor_set_deployed_radiator() -> None:
    """Objective: the rebased radiator dials carry current source metadata.

    Expected: both radiator mass cells cite RLDC-SOLAR-RADIATOR-MASS with
    status ``scenario`` and an investor-set deployed double-sided rationale;
    no cell or config description still calls the default the single-face
    co-mounted 0.012 posture.
    """
    output = _run("default")
    physical = output.inputs.config.physical
    for cell in (physical.radiator_t_per_kw_pre, physical.radiator_t_per_kw_post):
        assert _claims(cell) == {"RLDC-SOLAR-RADIATOR-MASS"}
        assert cell.source_status == "scenario"
        assert "deployed double-sided" in cell.rationale
        assert "Investor-set (2026-07-14)" in cell.rationale
        assert "lifts this to 0.012" not in cell.description
        assert "co-mounted radiator dial" not in cell.rationale
    assert "inert" in physical.tjmax_lift_year.rationale


def test_cadence_ceiling_is_the_horizon_scoped_parameter() -> None:
    """Objective: the ceiling is not published as a hard cap on the system.

    Expected: the cell cites RLDC-CADENCE-CEILING-150, its description and
    rationale call it the window's infrastructure parameter, and the phrase
    "Hard cap" is gone from both.
    """
    ceiling = _run("default").inputs.config.cadence.cadence_ceiling
    assert _claims(ceiling) == {"RLDC-CADENCE-CEILING-150"}
    assert "not a cap on the system" in ceiling.description
    assert "Hard cap" not in ceiling.description
    assert "re-set" in ceiling.rationale


def test_default_scenario_publishes_no_override_and_no_calendar_labels() -> None:
    """Objective: every default value keeps its claim; labels are config-derived.

    Expected: no cell of the default run is a scenario override, and no
    label names the calendar year 2036 (the year-10 anchor label reads
    "Launches at the year-10 anchor").
    """
    output = _run("default")
    cells = output.inputs.assumption_index.values()
    assert not [c.path for c in cells if c.assumption_role == "scenario_override"]
    assert not [c.label for c in cells if "2036 launches" in c.label]
    anchor = output.inputs.config.cadence.launches_at_year_10
    assert anchor.label == "Launches at the year-10 anchor"
    assert _claims(anchor) == {"RLDC-CADENCE-90"}


@pytest.mark.parametrize(
    ("name", "path", "default_claim"),
    [
        ("conservative", "inputs.config.fleet.service_life_years", "RLDC-SERVICE-LIFE-5Y"),
        ("conservative", "inputs.config.revenue.central.2026", "RLDC-REVENUE-MULTIPLE-1_5X"),
        ("ambitious", "inputs.config.cadence.launches_at_year_10", "RLDC-CADENCE-90"),
        ("ambitious", "inputs.config.physical.radiator_t_per_kw_post", "RLDC-SOLAR-RADIATOR-MASS"),
    ],
)
def test_overridden_values_do_not_carry_the_default_claim(
    name: str, path: str, default_claim: str
) -> None:
    """Objective: an overridden value is marked, not dressed in the default's claim.

    The original trigger: conservative's 3-year life cited
    RLDC-SERVICE-LIFE-5Y (a five-year claim); its 1.40 R and ambitious's
    120 launches and co-mounted radiator dial cited default-value claims.
    Expected: each such cell is a ``scenario_override`` with status
    ``scenario``, cites only the scenario YAML, and its rationale names the
    default it replaced.
    """
    cell = _run(name).inputs.assumption_index[path]
    assert cell.assumption_role == "scenario_override"
    assert cell.source_status == "scenario"
    assert default_claim not in _claims(cell)
    assert [ref.ref for ref in cell.source_refs] == [f"code/scenarios/{name}.yaml"]
    assert "Scenario override" in cell.rationale
    assert "the default is" in cell.rationale


def test_unchanged_values_in_a_scenario_keep_their_default_claim() -> None:
    """Objective: override marking is per value, not per scenario.

    Expected: conservative leaves the cadence ceiling at the default, so
    that cell still cites its claim with the default role.
    """
    ceiling = _run("conservative").inputs.config.cadence.cadence_ceiling
    assert ceiling.value == ValuationConfig().cadence.cadence_ceiling
    assert ceiling.assumption_role == "default"
    assert _claims(ceiling) == {"RLDC-CADENCE-CEILING-150"}


def test_generations_dictionary_uses_the_input_source_status_vocabulary() -> None:
    """Objective: one generations vocabulary across meta and inputs.

    The original trigger: ``meta.generations_dictionary`` published the
    internal ``fact`` / ``estimate`` tiers while the inputs said
    ``certified`` / ``sourced_estimate``. Expected: each summary's
    ``source_class`` equals the source status of the same generation's
    input cells.
    """
    output = _run("default")
    summaries = output.meta.generations_dictionary
    generations = output.inputs.config.generations
    assert len(summaries) == len(generations)
    for summary, generation in zip(summaries, generations, strict=True):
        assert summary.name == generation.name.value
        assert summary.source_class == generation.name.source_status
