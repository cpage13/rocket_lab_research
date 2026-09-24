"""Tests for the 12 mandatory ``query_examples`` (plan §5 T61).

The ``meta.query_examples`` block is the v8 cold-reader contract: a cold
agent runs these worked ``jq`` expressions to answer common questions
about a valuation run. This test guards that contract — for every one of
the 12 examples :func:`data_center.query_examples.build_query_examples`
builds for the default window's anchor year (FY2036) it:

1. runs the example's exact ``jq`` expression against a freshly-generated
   default-scenario output JSON, via the real ``jq`` binary; and
2. asserts the result is non-null and matches the example's declared
   ``expected_shape`` (scalar number, object, list, or provenance cell).

If a future schema change breaks a ``jq`` path, the corresponding case
fails here rather than silently shipping a broken cold-reader contract.

The default-scenario JSON is the session's default run (``default_output``
in ``conftest.py``) serialised with the production
:func:`data_center.json_output.render_json` to a temp file, so the test never
depends on a stale committed ``output/default.json``. Each example's ``jq``
expression runs once per module (:func:`jq_outcomes`); the execution and shape
tests read the same result.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from data_center.json_output import render_json
from data_center.output import QueryExample, SpaceModelOutput
from data_center.query_examples import build_query_examples

# Resolve `jq` once. The query_examples contract is jq-expressed, so the
# test needs the jq binary; skip cleanly (not fail) if it is absent.
_JQ: str | None = shutil.which("jq")

# Number of mandatory query examples — fixed by strategy §3.3 / plan T58.
_EXPECTED_COUNT = 12

# The default window (base year 2026, ten-year horizon) anchors at FY2036;
# the single-year examples address it and carry it in their names.
_DEFAULT_ANCHOR_YEAR = 2036
QUERY_EXAMPLES = build_query_examples(_DEFAULT_ANCHOR_YEAR)


@pytest.fixture(scope="module")
def default_json_path(
    default_output: SpaceModelOutput, tmp_path_factory: pytest.TempPathFactory
) -> Path:
    """Write the session's default run as JSON once for the module.

    Serialises the default run with the production :func:`render_json` to a
    temp file: the same content the CLI's ``--json`` path emits for
    ``scenarios/default.yaml`` (the ``output/default.json`` the plan's T61
    names), generated fresh so the test is hermetic.
    """
    path = tmp_path_factory.mktemp("query_examples") / "default.json"
    path.write_text(render_json(default_output), encoding="utf-8")
    return path


@pytest.fixture(scope="module")
def jq_outcomes(default_json_path: Path) -> dict[str, subprocess.CompletedProcess[str]]:
    """Run every example's ``jq`` expression once against the default JSON.

    Returns:
        The completed ``jq`` process for each example, keyed by example name;
        each test asserts on its own example's outcome.
    """
    if _JQ is None:
        pytest.skip("jq binary not installed")
    return {
        example.name: subprocess.run(  # noqa: S603 (_JQ is shutil.which output; args are static)
            [_JQ, example.jq, str(default_json_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        for example in QUERY_EXAMPLES
    }


def _jq_stdout(outcomes: dict[str, subprocess.CompletedProcess[str]], example: QueryExample) -> str:
    """Return one example's ``jq`` stdout, stripped of trailing whitespace.

    Args:
        outcomes: The module's ``jq`` outcomes, keyed by example name.
        example: The query example whose result to read.

    Returns:
        The raw ``jq`` stdout, stripped.

    Raises:
        AssertionError: If ``jq`` exited non-zero (the expression is invalid
            against the schema).
    """
    result = outcomes[example.name]
    assert result.returncode == 0, (
        f"jq failed for expression {example.jq!r}: {result.stderr.strip()}"
    )
    return result.stdout.strip()


# --------------------------------------------------------------------------
# Block-level checks — the list itself
# --------------------------------------------------------------------------


def test_query_examples_has_exactly_twelve_entries() -> None:
    """The built example list is the fixed 12-entry contract (strategy §3.3)."""
    assert len(QUERY_EXAMPLES) == _EXPECTED_COUNT


def test_query_examples_address_the_given_anchor_year() -> None:
    """Objective: the single-year examples follow the run's anchor year.

    Expected: built for FY2050 (a base-2040 window), no example mentions
    2036 and the anchor-year examples address ``business.years."2050"``.
    """
    examples = build_query_examples(2050)
    assert len(examples) == _EXPECTED_COUNT
    assert all("2036" not in e.model_dump_json() for e in examples)
    names = {e.name for e in examples}
    assert {"deployed_year_capacity_2050", "headline_2050_revenue_central"} <= names
    trace = next(e for e in examples if e.name == "trace_a_cell")
    assert trace.jq_expression == '.business.years."2050".revenue_annual_fleet_musd_central'


def test_query_example_names_are_unique() -> None:
    """Each example's ``name`` is a stable, unique key."""
    names = [q.name for q in QUERY_EXAMPLES]
    assert len(names) == len(set(names))


def test_meta_block_carries_all_twelve_examples(default_json_path: Path) -> None:
    """The emitted output's ``meta.query_examples`` holds all 12 entries."""
    parsed = json.loads(default_json_path.read_text(encoding="utf-8"))
    emitted = parsed["meta"]["query_examples"]
    assert len(emitted) == _EXPECTED_COUNT
    assert [e["name"] for e in emitted] == [q.name for q in QUERY_EXAMPLES]


# --------------------------------------------------------------------------
# Per-example execution — every jq expression runs and returns non-null
# --------------------------------------------------------------------------

_SKIP_NO_JQ = pytest.mark.skipif(_JQ is None, reason="jq binary not installed")


@_SKIP_NO_JQ
@pytest.mark.parametrize("example", QUERY_EXAMPLES, ids=lambda e: e.name)
def test_query_example_jq_runs_and_is_non_null(
    example: QueryExample, jq_outcomes: dict[str, subprocess.CompletedProcess[str]]
) -> None:
    """Every example's jq expression runs and yields a non-null result.

    ``jq`` returns the literal ``null`` for a missing path; a broken
    schema path would surface here. (An empty list ``[]`` is a valid
    non-null result — e.g. ``volume_binding_check`` is empty by D6.)
    """
    raw = _jq_stdout(jq_outcomes, example)
    assert raw != "", f"{example.name}: jq produced empty output"
    assert raw != "null", f"{example.name}: jq path resolved to null"


@_SKIP_NO_JQ
@pytest.mark.parametrize("example", QUERY_EXAMPLES, ids=lambda e: e.name)
def test_query_example_result_matches_expected_shape(
    example: QueryExample, jq_outcomes: dict[str, subprocess.CompletedProcess[str]]
) -> None:
    """Each example's result has the structure its ``expected_shape`` claims.

    The 12 examples fall into four shape families, keyed by ``name``:

    * scalar number — a single MUSD figure;
    * object ``{central, low, high}`` — the margin band;
    * list — a per-year trajectory or a list of FYs;
    * provenance cell — the ``trace_a_cell`` template, a dict with the
      seven ProvenanceCell keys.
    """
    name = example.name
    parsed = json.loads(_jq_stdout(jq_outcomes, example))

    scalar_number_examples = {
        "deployed_year_capacity_2036",
        "headline_2036_revenue_central",
        "headline_2036_profit_central",
    }
    list_examples = {
        "list_default_inputs_and_source_statuses",
        "validation_warnings",
        "trajectory_launches",
        "living_fleet_per_year",
    }

    if name in scalar_number_examples:
        assert isinstance(parsed, (int, float)) and not isinstance(parsed, bool)
    elif name == "margin_band_2036":
        assert isinstance(parsed, dict)
        assert set(parsed.keys()) == {"central", "low", "high"}
        for band_value in parsed.values():
            assert isinstance(band_value, (int, float)) and not isinstance(band_value, bool)
    elif name in list_examples:
        assert isinstance(parsed, list)
    elif name == "deployed_vs_living_kw_2036":
        assert isinstance(parsed, dict)
        assert set(parsed.keys()) == {"deployed_kw", "living_fleet_kw"}
    elif name in {"trace_launch_cost_assumption", "trace_revenue_multiple_assumption"}:
        assert isinstance(parsed, dict)
        assert {
            "path",
            "label",
            "value",
            "unit",
            "source_status",
            "source_refs",
            "rationale",
        } <= set(parsed.keys())
    elif name == "trace_a_cell":
        assert isinstance(parsed, dict)
        assert {
            "value",
            "unit",
            "formula",
            "formula_name",
            "uses",
            "sources",
            "description",
            "source_status",
        } <= set(parsed.keys())
    else:  # pragma: no cover - defensive: a new example needs a shape branch
        pytest.fail(f"no shape assertion defined for query example {name!r}")
