"""Tests for the 12 mandatory ``query_examples`` (plan §5 T61).

The ``meta.query_examples`` block is the v8 cold-reader contract: a cold
agent runs these worked ``jq`` expressions to answer common questions
about a valuation run. This test guards that contract — for every one of
the 12 :data:`data_center.query_examples.QUERY_EXAMPLES` it:

1. runs the example's exact ``jq`` expression against a freshly-generated
   default-scenario output JSON, via the real ``jq`` binary; and
2. asserts the result is non-null and matches the example's declared
   ``expected_shape`` (scalar number, object, list, or provenance cell).

If a future schema change breaks a ``jq`` path, the corresponding case
fails here rather than silently shipping a broken cold-reader contract.

The default-scenario JSON is generated fresh per test session (engine →
:func:`data_center.json_output.render_json`) and written to a temp file,
so the test never depends on a stale committed ``output/default.json``.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from data_center.config import load_config
from data_center.engine import run_valuation
from data_center.json_output import render_json
from data_center.output import QueryExample
from data_center.query_examples import QUERY_EXAMPLES

# Resolve `jq` once. The query_examples contract is jq-expressed, so the
# test needs the jq binary; skip cleanly (not fail) if it is absent.
_JQ: str | None = shutil.which("jq")

# The packaged default scenario, resolved relative to this test file so
# the test is independent of the process working directory.
_DEFAULT_YAML = Path(__file__).resolve().parents[2] / "scenarios" / "default.yaml"

# Number of mandatory query examples — fixed by strategy §3.3 / plan T58.
_EXPECTED_COUNT = 12


@pytest.fixture(scope="module")
def default_json_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Generate the default-scenario v8 output JSON once for the module.

    Runs the default scenario through the engine and serialises it with
    the production :func:`render_json`, writing to a temp file. This is
    the same content the CLI's ``--json`` path emits for
    ``scenarios/default.yaml`` — i.e. the ``output/default.json`` the
    plan's T61 names — but generated fresh so the test is hermetic.
    """
    output = run_valuation(load_config(str(_DEFAULT_YAML)))
    path = tmp_path_factory.mktemp("query_examples") / "default.json"
    path.write_text(render_json(output), encoding="utf-8")
    return path


def _run_jq(expression: str, json_path: Path) -> str:
    """Run a ``jq`` expression against a JSON file; return raw stdout.

    Args:
        expression: The jq program (one of the QUERY_EXAMPLES jq strings).
        json_path: Path to the JSON file to query.

    Returns:
        The raw ``jq`` stdout, stripped of trailing whitespace.

    Raises:
        AssertionError: If ``jq`` exits non-zero (the expression is
            invalid against the schema).
    """
    assert _JQ is not None  # guarded by the module-level skipif
    result = subprocess.run(  # noqa: S603 — _JQ is shutil.which output, args are static
        [_JQ, expression, str(json_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"jq failed for expression {expression!r}: {result.stderr.strip()}"
    )
    return result.stdout.strip()


# --------------------------------------------------------------------------
# Block-level checks — the list itself
# --------------------------------------------------------------------------


def test_query_examples_has_exactly_twelve_entries() -> None:
    """QUERY_EXAMPLES is the fixed 12-entry contract (strategy §3.3)."""
    assert len(QUERY_EXAMPLES) == _EXPECTED_COUNT


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
    example: QueryExample, default_json_path: Path
) -> None:
    """Every example's jq expression runs and yields a non-null result.

    ``jq`` returns the literal ``null`` for a missing path; a broken
    schema path would surface here. (An empty list ``[]`` is a valid
    non-null result — e.g. ``volume_binding_check`` is empty by D6.)
    """
    raw = _run_jq(example.jq, default_json_path)
    assert raw != "", f"{example.name}: jq produced empty output"
    assert raw != "null", f"{example.name}: jq path resolved to null"


@_SKIP_NO_JQ
@pytest.mark.parametrize("example", QUERY_EXAMPLES, ids=lambda e: e.name)
def test_query_example_result_matches_expected_shape(
    example: QueryExample, default_json_path: Path
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
    parsed = json.loads(_run_jq(example.jq, default_json_path))

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
