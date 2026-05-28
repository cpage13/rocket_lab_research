"""Regression guard for the v8 provenance ``uses[]`` back-pointer graph.

The cycle-2 v8 JSON is meant to be *traceable*: a cold agent starting at
any cell can follow ``uses[]`` back to the input dials. That only works if
every ``uses`` path resolves to a *real* upstream — a specific
:class:`data_center.provenance.ProvenanceCell` or an ``inputs.*`` dial —
never to a placeholder, never to itself, never to a bare year-container.

This module rebuilds the v8 artifact for every committed scenario,
serialises it, extracts every ``uses[]`` entry across every cell, and
resolves each one against the JSON. It asserts the three defects the
``json_audit_05_21.md`` audit found are gone and stay gone:

* zero **dangling** pointers — every path exists (no ``"FY"`` placeholder,
  no reference to a field that was never emitted);
* zero **self-referential** pointers — no cell cites its own path;
* zero **bare year-container** pointers — every path lands on a leaf cell
  or an input, never on a ``physical.years."YYYY"`` / ``business.years``
  object.

It also walks the headline 2036 fleet-revenue cell end-to-end and asserts
the provenance walk terminates at input dials with no broken edge.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

from data_center.config import load_config
from data_center.engine import run_valuation
from data_center.json_output import render_json

_SCENARIOS = Path(__file__).resolve().parents[2] / "scenarios"
_SCENARIO_NAMES = (
    "default",
    "conservative",
    "ambitious",
    "upside_7yr",
    "with_premium",
    "volume_stress",
)

# The seven fields that mark a serialised dict as a ProvenanceCell.
_CELL_KEYS = frozenset(
    {"value", "unit", "formula", "formula_name", "uses", "sources", "description"}
)


def _is_cell(node: Any) -> bool:
    """True if ``node`` is a serialised :class:`ProvenanceCell` dict."""
    return isinstance(node, dict) and node.keys() >= _CELL_KEYS


def _tokenise(path: str) -> list[str]:
    """Split a ``uses[]`` path into segments.

    Handles the three path forms a ``uses`` entry can take: plain dotted
    segments (``inputs.r_band.central``), double-quoted year segments
    (``physical.years."2036".kw_per_node``), and a trailing ``[]`` list
    wildcard (``inputs.generations[].kw_per_pkg``).

    Args:
        path: A ``uses[]`` JSON-path string.

    Returns:
        The path's ordered segments; a ``[]`` wildcard stays on its segment.
    """
    tokens: list[str] = []
    i = 0
    while i < len(path):
        if path[i] == '"':
            j = path.index('"', i + 1)
            tokens.append(path[i + 1 : j])
            i = j + 1
        else:
            m = re.match(r'([^."]+)', path[i:])
            assert m is not None, f"un-tokenisable path segment in {path!r}"
            tokens.append(m.group(1))
            i += len(m.group(1))
        if i < len(path) and path[i] == ".":
            i += 1
    return tokens


def _resolve(doc: dict[str, Any], path: str) -> Any | None:
    """Resolve a ``uses[]`` path against the serialised artifact.

    Args:
        doc: The full serialised v8 artifact.
        path: A ``uses[]`` JSON-path string.

    Returns:
        The node the path addresses, or ``None`` if the path dangles. A
        ``[]`` wildcard descends into the list's first element.
    """
    node: Any = doc
    for token in _tokenise(path):
        if token.endswith("[]"):
            key = token[:-2]
            if not isinstance(node, dict) or key not in node:
                return None
            node = node[key]
            if isinstance(node, list):
                if not node:
                    return None
                node = node[0]
        elif isinstance(node, dict) and token in node:
            node = node[token]
        else:
            return None
    return node


def _walk_cells(node: Any, path: str = "") -> list[tuple[str, dict[str, Any]]]:
    """Collect ``(concrete_path, cell)`` for every cell in the artifact.

    Year maps (``physical.years`` / ``business.years``) key by a JSON-string
    year, so a child of a ``*.years`` node gets a quoted path segment — the
    exact form a ``uses`` self-reference would take.

    Args:
        node: The current node in the serialised artifact.
        path: The concrete dotted path accumulated so far.

    Returns:
        Every ``(path, cell-dict)`` pair in the artifact.
    """
    out: list[tuple[str, dict[str, Any]]] = []
    if _is_cell(node):
        out.append((path, node))
        return out
    if isinstance(node, dict):
        for key, value in node.items():
            child = f'{path}."{key}"' if path.endswith("years") else f"{path}.{key}"
            out.extend(_walk_cells(value, child if path else key))
    elif isinstance(node, list):
        for idx, value in enumerate(node):
            out.extend(_walk_cells(value, f"{path}[{idx}]"))
    return out


def _classify(doc: dict[str, Any], cell_path: str, use_path: str) -> str:
    """Classify one ``uses`` pointer.

    Args:
        doc: The full serialised artifact.
        cell_path: Concrete path of the citing cell.
        use_path: One of the citing cell's ``uses[]`` entries.

    Returns:
        ``"self"`` if the pointer is the citing cell's own path;
        ``"dangling"`` if it resolves to nothing; ``"container"`` if it
        resolves to a non-cell object inside ``physical`` / ``business``;
        ``"ok"`` if it resolves to a cell or an ``inputs.*`` dial.
    """
    if use_path == cell_path:
        return "self"
    node = _resolve(doc, use_path)
    if node is None:
        return "dangling"
    if _is_cell(node):
        return "ok"
    head = use_path.split(".", 1)[0]
    if head == "inputs":
        return "ok"
    return "container"


@pytest.fixture(scope="module", params=_SCENARIO_NAMES)
def scenario_doc(request: pytest.FixtureRequest) -> dict[str, Any]:
    """Build + serialise one scenario's v8 artifact, parametrised over all six."""
    name: str = request.param
    config = load_config(_SCENARIOS / f"{name}.yaml")
    return json.loads(render_json(run_valuation(config)))  # type: ignore[no-any-return]


def test_every_uses_pointer_resolves(scenario_doc: dict[str, Any]) -> None:
    """No ``uses[]`` pointer dangles, self-references, or hits a bare container.

    The single load-bearing assertion: across every cell of the artifact,
    100 % of ``uses[]`` entries resolve to a real upstream cell or an
    ``inputs.*`` dial.
    """
    cells = _walk_cells(scenario_doc)
    assert cells, "artifact has no provenance cells"

    dangling: list[tuple[str, str]] = []
    self_ref: list[tuple[str, str]] = []
    container: list[tuple[str, str]] = []
    total = 0

    for cell_path, cell in cells:
        for use_path in cell["uses"]:
            total += 1
            verdict = _classify(scenario_doc, cell_path, use_path)
            if verdict == "self":
                self_ref.append((cell_path, use_path))
            elif verdict == "dangling":
                dangling.append((cell_path, use_path))
            elif verdict == "container":
                container.append((cell_path, use_path))

    assert total > 0, "no uses pointers found"
    assert not dangling, f"{len(dangling)} dangling uses pointers: {dangling[:5]}"
    assert not self_ref, f"{len(self_ref)} self-referential uses pointers: {self_ref[:5]}"
    assert not container, f"{len(container)} bare-container uses pointers: {container[:5]}"


def test_every_cell_has_nonempty_sources(scenario_doc: dict[str, Any]) -> None:
    """Every cell carries at least one ``sources`` citation (no empty arrays)."""
    empty = [path for path, cell in _walk_cells(scenario_doc) if not cell["sources"]]
    assert not empty, f"{len(empty)} cells with empty sources: {empty[:8]}"


def test_cost_intermediates_are_emitted_as_cells(scenario_doc: dict[str, Any]) -> None:
    """The five cost lines + per-package volume surface as real cells per year."""
    years = scenario_doc["physical"]["years"]
    assert years, "no physical years in artifact"
    for fy, year in years.items():
        breakdown = year["cost_breakdown"]
        for line in ("compute", "bus", "solar", "radiator", "launch", "node_total"):
            assert _is_cell(breakdown[line]), f"{fy}: cost_breakdown.{line} is not a cell"
        assert _is_cell(year["solar_area_per_pkg_m2"]), f"{fy}: solar_area not a cell"
        assert _is_cell(year["volume_per_pkg_m3"]), f"{fy}: volume_per_pkg not a cell"


def test_2036_fleet_revenue_provenance_walk_terminates(
    scenario_doc: dict[str, Any],
) -> None:
    """The cold-agent walk from 2036 fleet revenue reaches input dials, no break.

    Breadth-first from ``business.years."2036".revenue_annual_fleet_musd_central``,
    following ``uses[]``: every hop must land on a real cell or an input
    dial, the walk must reach at least one ``inputs.*`` terminus, and no
    edge may dangle.
    """
    if "2036" not in scenario_doc["business"]["years"]:
        pytest.skip("scenario horizon does not reach 2036")

    start = 'business.years."2036".revenue_annual_fleet_musd_central'
    visited: set[str] = set()
    frontier: list[str] = [start]
    cells_seen = 0
    dials_seen = 0

    while frontier:
        path = frontier.pop(0)
        if path in visited:
            continue
        visited.add(path)
        node = _resolve(scenario_doc, path)
        assert node is not None, f"provenance walk hit a broken edge at {path!r}"
        if _is_cell(node):
            cells_seen += 1
            frontier.extend(node["uses"])
        else:
            dials_seen += 1

    assert cells_seen >= 3, f"walk reached only {cells_seen} cells — too shallow"
    assert dials_seen >= 1, "walk never reached an input dial — does not terminate"
