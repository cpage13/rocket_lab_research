"""The committed product case: its regeneration test and its worked queries.

The one test module that reads the shipped scenario and the committed engineering artifact
together and runs the whole product case on them. The regeneration test is the only test that
freezes the promoted file's numbers: every other test reads a synthetic case, round 3's own
fixtures or one module. Each test names what it exercises, its sample and what counts as success.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

from product_case.json_output import (
    DEFAULT_ARTIFACT_PATH,
    QUERY_EXAMPLES,
    export_product_case_json,
)

type Answers = list[Any]
"""A worked query's answers: one parsed JSON value per line ``jq -c`` prints."""


def test_the_committed_product_case_equals_a_fresh_promotion(
    repo_dir: Path, product_case_yaml: Path, tmp_path: Path
) -> None:
    """Objective: the committed ``communications/models/product_case/default.json`` is exactly what
    the current code writes from the shipped scenario on the committed engineering artifact, and
    it describes that artifact as it stands: when the engineering artifact's bytes moved since the
    promotion, the failure names the SHA-256 the product case recorded and the file's current one
    (the engineering artifact is promoted first, then the product case, every time).

    Sample: ``code/scenarios/product_case.yaml`` promoted to a temporary file at the committed
    artifact's own version stamp, on the engineering artifact it names.

    Expected outcome: the engineering artifact's SHA-256 equals the recorded one; the fresh file
    parses to the same JSON document (compared first, for a readable difference) and is the same
    file byte for byte. Byte for byte holds on this platform: the draws are the standard
    library's promised stream and numpy's float64 power equals Python's here; another platform's
    vectorized power could move a floor at a near-whole demand by one, so a count could differ
    there with no change to the code.
    """
    committed_bytes = (repo_dir / DEFAULT_ARTIFACT_PATH).read_bytes()
    committed = json.loads(committed_bytes)
    read = committed["metadata"]["engineering_artifact"]
    current = hashlib.sha256((repo_dir / read["path"]).read_bytes()).hexdigest()
    assert current == read["sha256"], (
        f"{read['path']} moved since the product case was promoted: it recorded SHA-256 "
        f"{read['sha256']} and the file now has {current}; re-promote the product case after "
        "the engineering artifact"
    )
    written = export_product_case_json(
        product_case_yaml, tmp_path / "default.json", committed["metadata"]["version_stamp"]
    )
    assert json.loads(written.read_text(encoding="utf-8")) == committed
    assert written.read_bytes() == committed_bytes


def _number(value: Any) -> bool:
    """Whether a JSON value is a number (a boolean is not)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _one(answers: Answers, keys: set[str]) -> dict[str, Any] | None:
    """The single object a query answers with, when it holds exactly ``keys``; else None."""
    if len(answers) == 1 and isinstance(answers[0], dict) and set(answers[0]) == keys:
        only: dict[str, Any] = answers[0]
        return only
    return None


def _headline(answers: Answers) -> bool:
    """One object: the year a whole number, the revenue and the margin numbers."""
    entry = _one(answers, {"year", "revenue_musd", "margin_pct"})
    return (
        entry is not None
        and isinstance(entry["year"], int)
        and _number(entry["revenue_musd"])
        and _number(entry["margin_pct"])
    )


def _classes(answers: Answers) -> bool:
    """One list of the four classes in their order, each with whole customers and its revenue."""
    if len(answers) != 1 or not isinstance(answers[0], list):
        return False
    order = ["small_terminal", "mounted_terminal", "minimal_packet_iot", "data_iot"]
    return [entry.get("product_class") for entry in answers[0]] == order and all(
        set(entry) == {"product_class", "customers", "revenue_musd"}
        and isinstance(entry["customers"], int)
        and _number(entry["revenue_musd"])
        for entry in answers[0]
    )


def _pick(answers: Answers) -> bool:
    """One object: the choice id a whole number, the basis text, the usage edges a list of text."""
    entry = _one(answers, {"choice_id", "basis", "usage_edges"})
    return (
        entry is not None
        and isinstance(entry["choice_id"], int)
        and isinstance(entry["basis"], str)
        and isinstance(entry["usage_edges"], list)
        and all(isinstance(edge, str) for edge in entry["usage_edges"])
    )


def _usable_share(answers: Answers) -> bool:
    """One object: the usable draws a whole number, the share a number."""
    entry = _one(answers, {"usable_draws", "usable_share"})
    return (
        entry is not None
        and isinstance(entry["usable_draws"], int)
        and _number(entry["usable_share"])
    )


def _spreads(answers: Answers) -> bool:
    """One object a spread field, each with its field's name and its two bases."""
    return bool(answers) and all(
        isinstance(entry, dict)
        and set(entry) == {"field", "usable_draws", "all_draws"}
        and isinstance(entry["field"], str)
        and isinstance(entry["usable_draws"], dict)
        and isinstance(entry["all_draws"], dict)
        for entry in answers
    )


def _engineering(answers: Answers) -> bool:
    """One object of four texts: the path, the schema, the stamp and the SHA-256."""
    entry = _one(answers, {"path", "schema_version", "version_stamp", "sha256"})
    return entry is not None and all(isinstance(value, str) for value in entry.values())


STATED_SHAPES: dict[str, Callable[[Answers], bool]] = {
    "headline_last_year_revenue_and_margin": _headline,
    "classes_side_by_side_last_year": _classes,
    "pick_and_basis": _pick,
    "pick_usable_share": _usable_share,
    "spreads_last_year": _spreads,
    "engineering_artifact_read": _engineering,
}
"""Each worked query's stated shape (its ``expected_shape``) as a check of its answers, by name."""


def test_the_committed_artifacts_worked_queries_answer_in_their_stated_shape(
    repo_dir: Path,
) -> None:
    """Objective: each worked ``jq`` query the artifact carries runs on the committed artifact and
    answers in the shape it states, so a reader can run them as written; and every query has its
    shape check here, so a query added later is checked too.

    Sample: the committed ``communications/models/product_case/default.json`` and each entry of
    ``QUERY_EXAMPLES``, run by ``jq -c``.

    Expected outcome: the artifact's ``meta.query_examples`` are the code's; each query exits 0
    and its answers pass its stated shape; no number is frozen here.
    """
    path = repo_dir / DEFAULT_ARTIFACT_PATH
    carried = json.loads(path.read_text(encoding="utf-8"))["meta"]["query_examples"]
    assert [entry["jq_expression"] for entry in carried] == [
        query.jq_expression for query in QUERY_EXAMPLES
    ]
    assert set(STATED_SHAPES) == {query.name for query in QUERY_EXAMPLES}
    for query in QUERY_EXAMPLES:
        command = ["jq", "-c", query.jq_expression, str(path)]  # noqa: S607  jq from the PATH
        done = subprocess.run(  # noqa: S603  the artifact's own queries on the committed file
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        assert done.returncode == 0, (query.name, done.stderr)
        answers = [json.loads(line) for line in done.stdout.splitlines() if line.strip()]
        assert STATED_SHAPES[query.name](answers), (query.name, query.expected_shape)
