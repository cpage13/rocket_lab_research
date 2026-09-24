"""End-to-end tests for the space artifact's ``inputs`` contract.

The input manifest publishes every scenario input as a source-linked cell in
a typed tree and a flat ``assumption_index``. These tests run real scenarios
and assert the contract a cold reader relies on:

* the flat index holds every cell of the typed tree, the R-band anchors
  included, and the source-status summary counts exactly those cells;
* the source metadata of the dials the 2026-07-14 rebase changed describes
  the current investor-set posture, and the cadence ceiling is described as
  the horizon-scoped parameter it is;
* the fairing-volume and solar-mass dials cite the ``RLDC-*`` rows that
  describe them, and every input citing an ``RLDC-*`` claim carries that
  claim's status in the ``research/SOURCE_INDEX.md`` ledger;
* a value a scenario changed from the default is published as a scenario
  override, never under the default's claim, rationale, or role, and labels
  are config-derived rather than tied to one calendar year;
* the generation summaries and the generation input cells use one
  source-status vocabulary.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

from common.input_manifest import InputCell, SourceRefType, SourceStatus
from data_center.config import ValuationConfig, load_config
from data_center.engine import run_valuation
from data_center.input_manifest import collect_input_cells
from data_center.output import SpaceModelOutput

# Default cell count: 101 scalar and generation cells plus the 18 R-band
# anchor cells (three bands of six anchors).
_DEFAULT_INDEX_SIZE = 119


type RunScenario = Callable[[str], SpaceModelOutput]
"""Run a shipped scenario by name (see :func:`run_scenario`)."""


@pytest.fixture(scope="module")
def run_scenario(scenarios_dir: Path) -> RunScenario:
    """Run shipped scenarios by name, each once per module, recording the path as the CLI does."""
    runs: dict[str, SpaceModelOutput] = {}

    def run(name: str) -> SpaceModelOutput:
        if name not in runs:
            runs[name] = run_valuation(
                load_config(scenarios_dir / f"{name}.yaml"),
                source_scenario_path=f"code/scenarios/{name}.yaml",
            )
        return runs[name]

    return run


def _claims(cell: InputCell) -> set[str]:
    """Return every claim ID a cell cites."""
    return {ref.claim_id for ref in cell.source_refs if ref.claim_id is not None}


def _primary_rldc_claim(cell: InputCell) -> str | None:
    """Return the cell's primary claim ID when it is an RLDC SOURCE_INDEX claim, else None."""
    primary = cell.source_refs[0]
    if primary.ref_type is not SourceRefType.SOURCE_INDEX or primary.claim_id is None:
        return None
    return primary.claim_id if primary.claim_id.startswith("RLDC-") else None


@pytest.mark.parametrize("name", ["default", "conservative", "ambitious"])
def test_assumption_index_holds_every_cell_of_the_typed_tree(
    name: str, run_scenario: RunScenario
) -> None:
    """Objective: the flat index is complete (the R-band anchors were missing).

    Expected: the index keys equal the paths of every cell in the typed
    tree, the central 2026 anchor is indexed, the source-status summary
    counts every indexed cell, and the default index has 119 entries.
    """
    output = run_scenario(name)
    tree_paths = [cell.path for cell in collect_input_cells(output.inputs.config)]
    assert len(tree_paths) == len(set(tree_paths))
    assert set(output.inputs.assumption_index) == set(tree_paths)
    assert "inputs.config.revenue.central.2026" in output.inputs.assumption_index
    summary = output.meta.source_status_summary
    assert sum(summary.model_dump().values()) == len(output.inputs.assumption_index)
    if name == "default":
        assert len(output.inputs.assumption_index) == _DEFAULT_INDEX_SIZE


def test_radiator_dials_describe_the_investor_set_deployed_radiator(
    run_scenario: RunScenario,
) -> None:
    """Objective: the rebased radiator dials carry current source metadata.

    Expected: both radiator mass cells cite RLDC-SOLAR-RADIATOR-MASS with
    status ``scenario`` and an investor-set deployed double-sided rationale;
    no cell or config description still calls the default the single-face
    co-mounted 0.012 posture.
    """
    output = run_scenario("default")
    physical = output.inputs.config.physical
    for cell in (physical.radiator_t_per_kw_pre, physical.radiator_t_per_kw_post):
        assert _claims(cell) == {"RLDC-SOLAR-RADIATOR-MASS"}
        assert cell.source_status == "scenario"
        assert "deployed double-sided" in cell.rationale
        assert "Investor-set (2026-07-14)" in cell.rationale
        assert "lifts this to 0.012" not in cell.description
        assert "co-mounted radiator dial" not in cell.rationale
    assert "inert" in physical.tjmax_lift_year.rationale


def test_cadence_ceiling_is_the_horizon_scoped_parameter(run_scenario: RunScenario) -> None:
    """Objective: the ceiling is not published as a hard cap on the system.

    Expected: the cell cites RLDC-CADENCE-CEILING-150, its description and
    rationale call it the window's infrastructure parameter, and the phrase
    "Hard cap" is gone from both.
    """
    ceiling = run_scenario("default").inputs.config.cadence.cadence_ceiling
    assert _claims(ceiling) == {"RLDC-CADENCE-CEILING-150"}
    assert "not a cap on the system" in ceiling.description
    assert "Hard cap" not in ceiling.description
    assert "re-set" in ceiling.rationale


def test_fairing_volume_and_solar_mass_dials_cite_their_rldc_claims(
    run_scenario: RunScenario,
) -> None:
    """Objective: the two dials cite the ledger rows that describe them.

    The original trigger: the fairing-volume cell cited NTR-004 (a payload
    mass claim, no volume evidence) as ``sourced_estimate``, and the
    solar-mass cell cited THR-006 alone, while ``RLDC-FAIRING-VOLUME-80M3``
    and ``RLDC-SOLAR-RADIATOR-MASS`` (both ``scenario``) describe the two
    dials. Expected: each cell cites its RLDC claim first with status
    ``scenario``; the fairing cell drops NTR-004 and cites the research note
    behind its envelope estimate; the solar cell keeps THR-006 as a
    supporting SOURCE_INDEX reference; the scenario YAML stays the last
    reference of both.
    """
    config = run_scenario("default").inputs.config
    fairing = config.volume.neutron_fairing_usable_volume_m3
    solar = config.physical.solar_mass_t_per_kw
    assert fairing.source_status == SourceStatus.SCENARIO
    assert solar.source_status == SourceStatus.SCENARIO
    assert [(ref.ref_type, ref.ref) for ref in fairing.source_refs] == [
        (SourceRefType.SOURCE_INDEX, "research/SOURCE_INDEX.md#RLDC-FAIRING-VOLUME-80M3"),
        (SourceRefType.RESEARCH_DOC, "research/node_design/node_mass_model.md"),
        (SourceRefType.RESEARCH_DOC, "code/scenarios/default.yaml"),
    ]
    assert "NTR-004" not in _claims(fairing)
    assert [(ref.ref_type, ref.claim_id) for ref in solar.source_refs] == [
        (SourceRefType.SOURCE_INDEX, "RLDC-SOLAR-RADIATOR-MASS"),
        (SourceRefType.SOURCE_INDEX, "THR-006"),
        (SourceRefType.RESEARCH_DOC, None),
    ]


def test_rldc_cited_inputs_carry_the_ledger_source_status(
    run_scenario: RunScenario, ledger_statuses: dict[str, SourceStatus]
) -> None:
    """Objective: an input's status agrees with the RLDC row it cites.

    The ``RLDC-*`` rows of ``research/SOURCE_INDEX.md`` describe the default
    model inputs, so a default cell whose primary claim is an RLDC claim must
    publish that row's status. Expected: every such cell's primary claim has
    a ledger row, and the cell's ``source_status`` equals the row's status
    (the fairing-volume, solar-mass, and bus cost dials included).
    """
    ledger = ledger_statuses
    cells = run_scenario("default").inputs.assumption_index.values()
    cited = {
        cell.path: (claim, cell.source_status)
        for cell in cells
        if (claim := _primary_rldc_claim(cell)) is not None
    }
    assert "inputs.config.volume.neutron_fairing_usable_volume_m3" in cited
    assert "inputs.config.physical.solar_mass_t_per_kw" in cited
    assert cited["inputs.config.physical.bus_base_musd"][0] == "RLDC-BUS-COST"
    mismatched = {
        path: (claim, status, ledger.get(claim))
        for path, (claim, status) in cited.items()
        if ledger.get(claim) != status
    }
    assert mismatched == {}


def test_default_scenario_publishes_no_override_and_no_calendar_labels(
    run_scenario: RunScenario,
) -> None:
    """Objective: every default value keeps its claim; labels are config-derived.

    Expected: no cell of the default run is a scenario override, and no
    label names the calendar year 2036 (the year-10 anchor label reads
    "Launches at the year-10 anchor").
    """
    output = run_scenario("default")
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
    name: str, path: str, default_claim: str, run_scenario: RunScenario
) -> None:
    """Objective: an overridden value is marked, not dressed in the default's claim.

    The original trigger: conservative's 3-year life cited
    RLDC-SERVICE-LIFE-5Y (a five-year claim); its 1.40 R and ambitious's
    120 launches and co-mounted radiator dial cited default-value claims.
    Expected: each such cell is a ``scenario_override`` with status
    ``scenario``, cites only the scenario YAML, and its rationale names the
    default it replaced.
    """
    cell = run_scenario(name).inputs.assumption_index[path]
    assert cell.assumption_role == "scenario_override"
    assert cell.source_status == "scenario"
    assert default_claim not in _claims(cell)
    assert [ref.ref for ref in cell.source_refs] == [f"code/scenarios/{name}.yaml"]
    assert "Scenario override" in cell.rationale
    assert "the default is" in cell.rationale


def test_unchanged_values_in_a_scenario_keep_their_default_claim(run_scenario: RunScenario) -> None:
    """Objective: override marking is per value, not per scenario.

    Expected: conservative leaves the cadence ceiling at the default, so
    that cell still cites its claim with the default role.
    """
    ceiling = run_scenario("conservative").inputs.config.cadence.cadence_ceiling
    assert ceiling.value == ValuationConfig().cadence.cadence_ceiling
    assert ceiling.assumption_role == "default"
    assert _claims(ceiling) == {"RLDC-CADENCE-CEILING-150"}


def test_generations_dictionary_uses_the_input_source_status_vocabulary(
    run_scenario: RunScenario,
) -> None:
    """Objective: one generations vocabulary across meta and inputs.

    The original trigger: ``meta.generations_dictionary`` published the
    internal ``fact`` / ``estimate`` tiers while the inputs said
    ``certified`` / ``sourced_estimate``. Expected: each summary's
    ``source_class`` equals the source status of the same generation's
    input cells.
    """
    output = run_scenario("default")
    summaries = output.meta.generations_dictionary
    generations = output.inputs.config.generations
    assert len(summaries) == len(generations)
    for summary, generation in zip(summaries, generations, strict=True):
        assert summary.name == generation.name.value
        assert summary.source_class == generation.name.source_status
