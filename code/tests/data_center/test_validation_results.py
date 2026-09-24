"""End-to-end tests for ``meta.validation_results``, the one public verdict list.

The list mirrors every V-rule, then adds the model invariants that hold for
any scenario (read against the run's own config), then, for the canonical
default scenario only, the default guards that compare the promoted default
with the code defaults. A scenario that differs from the default by design is
never failed for that difference, and the text report and the embedded
``validation_warnings`` jq query read the same list.

These tests drive every shipped data-center scenario through the real engine
and assert the published verdicts by value.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

from data_center.config import config_from_dict, load_config
from data_center.engine import run_valuation
from data_center.input_manifest import DEFAULT_SCENARIO_PATH
from data_center.json_output import render_json
from data_center.output import ValuationOutput
from data_center.query_examples import build_query_examples
from data_center.text_report import render_text

_JQ: str | None = shutil.which("jq")

# The default guards, emitted only for the canonical default scenario.
_DEFAULT_GUARD_IDS = {
    "default_2036_deployed_capacity_around_70mw",
    "default_revenue_multiple_is_1_5x",
    "default_service_life_is_five_years",
}

# Every shipped non-default scenario, with the checks it is expected to fail
# for a real model reason (never for differing from the default).
_EXPECTED_FAILURES: dict[str, set[str]] = {
    "ambitious": set(),
    "conservative": set(),
    "upside_7yr": set(),
    "with_premium": set(),
    "volume_stress": {"volume_fits_horizon"},
    "ai1_equivalent": {"pf_per_kw_in_band"},
}


type RunScenario = Callable[[str], ValuationOutput]
"""Run a shipped scenario by name (see :func:`run_scenario`)."""


@pytest.fixture(scope="module")
def run_scenario(scenarios_dir: Path) -> RunScenario:
    """Run shipped scenarios by name, each once per module, recording the path as the CLI does."""
    runs: dict[str, ValuationOutput] = {}

    def run(name: str) -> ValuationOutput:
        if name not in runs:
            runs[name] = run_valuation(
                load_config(scenarios_dir / f"{name}.yaml"),
                source_scenario_path=f"code/scenarios/{name}.yaml",
            )
        return runs[name]

    return run


def _not_passing(output: ValuationOutput) -> set[str]:
    """Return the ids of every result that warns or fails."""
    return {r.validation_id for r in output.meta.validation_results if r.severity != "pass"}


def test_default_scenario_passes_every_check_including_the_default_guards(
    run_scenario: RunScenario,
) -> None:
    """Objective: the canonical default passes all 22 published checks.

    Expected: 16 mirrored V-rules, the three model invariants (year-10
    cadence, living fleet distinct from the deployed cohort, no placeholder
    or stale input), and the three default guards, every one ``pass``.
    """
    output = run_scenario("default")
    assert output.inputs.scenario.path == DEFAULT_SCENARIO_PATH
    ids = [r.validation_id for r in output.meta.validation_results]
    assert len(ids) == 22
    assert set(ids) >= _DEFAULT_GUARD_IDS
    assert {
        "anchor_year_launches_match_year_10_dial",
        "living_fleet_distinct_from_deployed_year_cohort",
        "release_critical_inputs_have_no_placeholder_or_stale_status",
    } <= set(ids)
    assert not _not_passing(output)


@pytest.mark.parametrize("name", sorted(_EXPECTED_FAILURES))
def test_shipped_scenarios_carry_no_default_pinned_check(
    name: str, run_scenario: RunScenario
) -> None:
    """Objective: a scenario is never failed for differing from the default.

    Expected: no default guard is emitted for a non-default scenario, the
    year-10 cadence invariant passes against the scenario's own dial, and
    the only non-passing checks are the documented real ones (volume_stress
    overfills the fairing; ai1_equivalent's pinned silicon sits below the
    PF/kW band).
    """
    output = run_scenario(name)
    ids = {r.validation_id for r in output.meta.validation_results}
    assert not [vid for vid in ids if vid.startswith("default_")]
    assert _not_passing(output) == _EXPECTED_FAILURES[name]
    cadence = next(
        r
        for r in output.meta.validation_results
        if r.validation_id == "anchor_year_launches_match_year_10_dial"
    )
    assert cadence.severity == "pass"


@pytest.mark.parametrize(
    "overrides",
    [
        {"fleet": {"service_life_years": 1}},
        {"cadence": {"first_launch_year": 10}},
    ],
    ids=["one_year_life", "first_launch_in_anchor_year"],
)
def test_distinctness_invariant_is_skipped_when_no_earlier_cohort_lives(
    overrides: dict[str, dict[str, int]],
) -> None:
    """Objective: an invariant that cannot hold by construction is not emitted.

    With a one-year service life, or a first launch in the anchor year
    itself, no earlier cohort is alive at the anchor year, so the living
    fleet is the deployed-year cohort. Expected: no
    ``living_fleet_distinct_from_deployed_year_cohort`` result, and nothing
    fails (both configs are valid).
    """
    output = run_valuation(config_from_dict(overrides))
    ids = {r.validation_id for r in output.meta.validation_results}
    assert "living_fleet_distinct_from_deployed_year_cohort" not in ids
    assert not _not_passing(output)


def test_year_10_cadence_invariant_catches_a_ramp_that_misses_its_dial() -> None:
    """Objective: the cadence invariant reads the run's dial, not a constant.

    A first launch year after model year 10 clamps the anchor year to zero
    launches. Expected: ``anchor_year_launches_match_year_10_dial`` fails,
    naming the dial it expected.
    """
    output = run_valuation(config_from_dict({"cadence": {"first_launch_year": 11}}))
    check = next(
        r
        for r in output.meta.validation_results
        if r.validation_id == "anchor_year_launches_match_year_10_dial"
    )
    assert check.severity == "fail"
    assert "(90)" in check.expected_condition
    assert check.observed_result == "0 launches in FY2036"


def test_report_query_and_json_agree_on_the_ambitious_verdict(
    tmp_path: Path, run_scenario: RunScenario
) -> None:
    """Objective: one verdict source (the original ambitious trigger).

    Before the fix the text report showed 16 of 16 rules passing while the
    embedded ``validation_warnings`` query returned two default-pinned
    failures. Expected: the query's result equals the non-passing subset
    of ``meta.validation_results`` (empty for ambitious), and the report's
    summary line counts the same list.
    """
    output = run_scenario("ambitious")
    published = json.loads(render_json(output))
    expected = [r for r in published["meta"]["validation_results"] if r["severity"] != "pass"]
    assert expected == []
    report = render_text(output)
    total = len(published["meta"]["validation_results"])
    assert f"{total} of {total} checks pass." in report
    if _JQ is None:
        pytest.skip("jq binary not installed")
    query = next(
        q for q in build_query_examples(2036) if q.name == "validation_warnings"
    ).jq_expression
    path = tmp_path / "ambitious.json"
    path.write_text(render_json(output), encoding="utf-8")
    raw = subprocess.run(  # noqa: S603 (_JQ is shutil.which output; the query is ours)
        [_JQ, "-c", query, str(path)], capture_output=True, text=True, check=True
    ).stdout
    assert json.loads(raw) == expected
