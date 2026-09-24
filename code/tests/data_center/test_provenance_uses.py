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

The ground reference artifact is held to the same contract: every ``uses``
entry resolves, either inside the ground artifact (``anchor.*``,
``inputs.config.*``, ``ground.component_costs[i].cost``) or, when prefixed
``space:``, inside the space artifact the ground reference was built from.

Finally, perturbation checks prove the ``uses`` graph is sufficient, not
only resolvable: moving a dial may change only cells whose transitive ``uses``
closure reaches that dial. A focused set names the dials the Phase 2 review
found unreachable; a full sweep perturbs every numeric settable dial of the
space and ground artifacts (the generation roadmap included) and follows
``space:`` pointers across artifacts, so a new cell that forgets a dependency
fails here.
"""

from __future__ import annotations

import copy
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import pytest
import yaml
from pydantic import ValidationError

from data_center.config import config_from_dict, load_config
from data_center.engine import run_valuation
from data_center.generations import KNOWN_GENS
from data_center.ground import (
    DEFAULT_GROUND_SCENARIO_PATH,
    SPACE_PATH_PREFIX,
    build_ground_reference_output,
    ground_config_from_dict,
    load_ground_config,
    render_ground_json,
)
from data_center.json_output import render_json
from data_center.output import SpaceModelOutput

_SCENARIO_NAMES = (
    "default",
    "conservative",
    "ambitious",
    "upside_7yr",
    "with_premium",
    "volume_stress",
    "ai1_equivalent",
)
_INDEX_TOKEN = re.compile(r"^(?P<key>[^\[]+)\[(?P<index>\d+)\]$")

# The seven fields that mark a serialised dict as a ProvenanceCell.
_CELL_KEYS = frozenset(
    {"value", "unit", "formula", "formula_name", "uses", "sources", "description"}
)


def _is_cell(node: Any) -> bool:
    """True if ``node`` is a serialised :class:`ProvenanceCell` dict."""
    return isinstance(node, dict) and node.keys() >= _CELL_KEYS


def _tokenise(path: str) -> list[str]:
    """Split a ``uses[]`` path into segments.

    Handles the four path forms a ``uses`` entry can take: plain dotted
    segments (``inputs.r_band.central``), double-quoted year segments
    (``physical.years."2036".kw_per_node``), a trailing ``[]`` list
    wildcard (``inputs.generations[].kw_per_pkg``), and a list index
    (``ground.component_costs[3].cost``).

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
        ``[]`` wildcard descends into the list's first element; ``[N]``
        descends into element ``N``.
    """
    node: Any = doc
    for token in _tokenise(path):
        indexed = _INDEX_TOKEN.match(token)
        if indexed is not None:
            key, index = indexed.group("key"), int(indexed.group("index"))
            if not isinstance(node, dict) or key not in node:
                return None
            node = node[key]
            if not isinstance(node, list) or index >= len(node):
                return None
            node = node[index]
        elif token.endswith("[]"):
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
        resolves to a non-cell object or list outside ``inputs``; ``"ok"``
        if it resolves to a cell, an ``inputs.*`` dial, or a scalar leaf
        (for example ``anchor.kw`` in the ground artifact).
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
    if not isinstance(node, (dict, list)):
        return "ok"
    return "container"


@pytest.fixture(scope="module", params=_SCENARIO_NAMES)
def scenario_doc(request: pytest.FixtureRequest, scenarios_dir: Path) -> dict[str, Any]:
    """Build + serialise one scenario's v8 artifact, parametrised over every scenario."""
    name: str = request.param
    config = load_config(scenarios_dir / f"{name}.yaml")
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


# --------------------------------------------------------------------------
# The ground reference artifact
# --------------------------------------------------------------------------


@pytest.fixture(scope="module")
def default_space_and_ground_docs(
    default_output: SpaceModelOutput, scenarios_dir: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Serialise the session's default run and the ground reference built from it."""
    space = default_output
    ground = build_ground_reference_output(
        space,
        load_ground_config(scenarios_dir / "ground_default.yaml"),
        space_model_path="data_center/models/space/default.json",
        ground_scenario_path=DEFAULT_GROUND_SCENARIO_PATH,
    )
    return json.loads(render_json(space)), json.loads(render_ground_json(ground))


def test_every_ground_uses_pointer_resolves(
    default_space_and_ground_docs: tuple[dict[str, Any], dict[str, Any]],
) -> None:
    """Objective: the chain behind the ground ratio never dead-ends.

    The original trigger: 66 of 112 ground ``uses`` entries were prose
    descriptions or unprefixed space paths. Expected: every entry resolves,
    a ``space:`` entry against the space artifact and every other entry
    against the ground artifact, with no self, dangling, or bare-container
    pointer; both prefixed and ground-local entries occur.
    """
    space_doc, ground_doc = default_space_and_ground_docs
    cells = _walk_cells(ground_doc)
    assert cells, "ground artifact has no provenance cells"
    broken: list[tuple[str, str, str]] = []
    prefixed = local = 0
    for cell_path, cell in cells:
        for use_path in cell["uses"]:
            if use_path.startswith(SPACE_PATH_PREFIX):
                prefixed += 1
                verdict = _classify(space_doc, "", use_path.removeprefix(SPACE_PATH_PREFIX))
            else:
                local += 1
                verdict = _classify(ground_doc, cell_path, use_path)
            if verdict != "ok":
                broken.append((verdict, cell_path, use_path))
    assert prefixed > 0 and local > 0
    assert not broken, f"{len(broken)} broken ground uses pointers: {broken[:5]}"


# --------------------------------------------------------------------------
# Sufficiency: a dial's movements stay inside the closure of the cells citing it
# --------------------------------------------------------------------------

_HEAVY_PRE_LIFT_RADIATOR: dict[str, Any] = {"gospel": {"radiator_t_per_kw_pre": 0.003}}

# A cadence ceiling far enough from the default 150 to move launches. The
# logistic ramp is fit through the year-5 and year-10 anchors, so a unit move
# of the ceiling shifts every other year's fitted rate by well under half a
# launch and integer rounding absorbs it; 200 reshapes the ramp enough to move
# whole launches.
_MOVING_CADENCE_CEILING = 200

# (dial path, base config mapping, perturbed config mapping). The Tjmax case
# starts from a heavier pre-lift dial, since the default holds pre == post
# and the lift year would move nothing.
_PERTURBATIONS: tuple[tuple[str, dict[str, Any], dict[str, Any]], ...] = (
    (
        "inputs.config.physical.solar_mass_t_per_kw",
        {},
        {"gospel": {"solar_mass_t_per_kw": 0.0121}},
    ),
    (
        "inputs.config.physical.radiator_t_per_kw_pre",
        {},
        _HEAVY_PRE_LIFT_RADIATOR,
    ),
    (
        "inputs.config.physical.radiator_t_per_kw_post",
        {},
        {"gospel": {"radiator_t_per_kw_post": 0.003}},
    ),
    (
        "inputs.config.physical.tjmax_lift_year",
        _HEAVY_PRE_LIFT_RADIATOR,
        {"gospel": {"radiator_t_per_kw_pre": 0.003, "tjmax_lift_year": 3}},
    ),
    (
        "inputs.config.physical.node_mass_fixed_t",
        {},
        {"gospel": {"node_mass_fixed_t": 3.0}},
    ),
    (
        "inputs.config.physical.bus_flatten_after_yr",
        {},
        {"gospel": {"bus_flatten_after_yr": 3}},
    ),
    (
        "inputs.config.launch.low_cadence_launches",
        {},
        {"launch_cost": {"low_cadence_launches": 3.0}},
    ),
    (
        "inputs.config.launch.high_cadence_launches",
        {},
        {"launch_cost": {"high_cadence_launches": 120.0}},
    ),
    (
        "inputs.config.fleet.service_life_years",
        {},
        {"fleet": {"service_life_years": 6}},
    ),
    (
        "inputs.config.cadence.cadence_ceiling",
        {},
        {"cadence": {"cadence_ceiling": _MOVING_CADENCE_CEILING}},
    ),
)


def _closure(doc: dict[str, Any], start: str) -> set[str]:
    """Return every path reachable from ``start`` by following ``uses``."""
    seen: set[str] = set()
    frontier = [start]
    while frontier:
        path = frontier.pop()
        if path in seen:
            continue
        seen.add(path)
        node = _resolve(doc, path)
        if _is_cell(node):
            frontier.extend(node["uses"])
    return seen


@pytest.mark.parametrize(
    ("dial", "base", "perturbed"),
    _PERTURBATIONS,
    ids=[p[0].rsplit(".", 1)[-1] for p in _PERTURBATIONS],
)
def test_a_dial_moves_only_cells_whose_uses_reach_it(
    dial: str, base: dict[str, Any], perturbed: dict[str, Any]
) -> None:
    """Objective: every cell a dial moves cites that dial, directly or transitively.

    The original triggers: the solar-mass and radiator dials, the Tjmax lift
    year, and the bus flattening year appeared in no ``uses`` chain; the
    fleet launch cost dropped two launch-cost anchors; fleet rollups cited
    only the current year's per-node cells, and then lost the service life
    that selects the living vintages. Expected: the perturbation moves at
    least one cell, and every moved cell's transitive ``uses`` closure
    contains the dial's path.
    """
    base_doc = json.loads(render_json(run_valuation(config_from_dict(base))))
    moved_doc = json.loads(render_json(run_valuation(config_from_dict(perturbed))))
    base_cells = dict(_walk_cells(base_doc))
    moved = [
        path
        for path, cell in _walk_cells(moved_doc)
        if path in base_cells and cell["value"] != base_cells[path]["value"]
    ]
    assert moved, f"perturbing {dial} moved no cell"
    unreached = [path for path in moved if dial not in _closure(moved_doc, path)]
    assert not unreached, f"{len(unreached)} moved cells never reach {dial}: {unreached[:5]}"


# --------------------------------------------------------------------------
# Full sweep: every numeric settable dial, space and ground, across artifacts
# --------------------------------------------------------------------------

_SPACE = "space"
_GROUND = "ground"
type _Node = tuple[str, str]
"""A cell or dial address: (artifact, path in that artifact)."""

# Config blocks by their public input-tree name.
_CONFIG_BLOCKS: dict[str, str] = {
    "cadence": "cadence",
    "fleet": "fleet",
    "volume": "volume",
    "launch": "launch_cost",
    "physical": "gospel",
    "generation_slopes": "slopes",
}

# Relative moves tried in order on a float dial, stopping at the first that
# moves a cell; a zero dial is set to a small positive value instead.
_FLOAT_FACTORS = (1.1, 0.9, 1.5)
_ZERO_DIAL_VALUE = 0.01

# Availability years move additively: a relative move of a calendar year
# leaves the fiscal window. Three quarters of a year moves a half-year date
# across a fiscal year while keeping the listed roadmap (dates at least a
# year apart) strictly ordered.
_YEAR_SHIFT = 0.75

_REVENUE_ANCHOR = re.compile(r"^(inputs\.config\.revenue\.(?:central|low|high))\.\d+$")

# Dials the sweep expects to move nothing on the default, with the reason.
# Anything else that moves nothing fails the sweep (a silent perturbation
# would make the closure check vacuous).
_EXPECTED_INERT_DIALS: dict[str, str] = {
    "inputs.config.physical.tjmax_lift_year": "the default holds pre == post radiator mass",
    "inputs.config.generations[0].year_available": "B200 is never the frontier",
    "inputs.config.generations[0].usd_per_pkg": "B200 is never the frontier",
    "inputs.config.generations[0].kw_per_pkg": "B200 is never the frontier",
    "inputs.config.generations[0].kg_per_pkg": "B200 is never the frontier",
    "inputs.config.generations[0].pf_per_pkg": "B200 is never the frontier",
    **{
        f"inputs.config.generations[{index}].die_count": "die count sizes nothing"
        for index in range(len(KNOWN_GENS))
    },
}


def _default_mappings(scenarios_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return the default space and ground scenario mappings.

    The space mapping lists the bundled generations explicitly so the
    sweep can move a generation's field; the roadmap is unchanged.
    """
    space = yaml.safe_load((scenarios_dir / "default.yaml").read_text(encoding="utf-8"))
    space["generations"] = [g.model_dump(mode="json") for g in KNOWN_GENS]
    ground = yaml.safe_load((scenarios_dir / "ground_default.yaml").read_text(encoding="utf-8"))
    return space, ground


def _build_docs(space: dict[str, Any], ground: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Run the space model and the ground reference; return both serialised."""
    output = run_valuation(config_from_dict(copy.deepcopy(space)))
    reference = build_ground_reference_output(
        output,
        ground_config_from_dict(copy.deepcopy(ground)),
        space_model_path="scratch/space.json",
        ground_scenario_path=DEFAULT_GROUND_SCENARIO_PATH,
    )
    return {_SPACE: output.model_dump(mode="json"), _GROUND: reference.model_dump(mode="json")}


# Top-level blocks that hold no provenance cell (the sweep skips walking them).
_CELL_FREE_BLOCKS = frozenset({"metadata", "inputs", "meta"})


def _artifact_cells(doc: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """Return ``(path, cell)`` for every provenance cell of one serialised artifact."""
    cells: list[tuple[str, dict[str, Any]]] = []
    for block, node in doc.items():
        if block not in _CELL_FREE_BLOCKS:
            cells.extend(_walk_cells(node, block))
    return cells


def _cell_values(docs: dict[str, dict[str, Any]]) -> dict[_Node, Any]:
    """Return every cell's value, keyed by artifact and path."""
    return {
        (art, path): cell["value"]
        for art, doc in docs.items()
        for path, cell in _artifact_cells(doc)
    }


def _cells_citing(docs: dict[str, dict[str, Any]], seeds: set[_Node]) -> set[_Node]:
    """Return every cell whose transitive ``uses`` reach one of ``seeds``.

    Walks the ``uses`` graph backwards from the seeds; a ``space:`` entry in
    the ground artifact is an edge into the space artifact.
    """
    citers: dict[_Node, list[_Node]] = defaultdict(list)
    for art, doc in docs.items():
        for path, cell in _artifact_cells(doc):
            for use in cell["uses"]:
                if use.startswith(SPACE_PATH_PREFIX):
                    target = (_SPACE, use.removeprefix(SPACE_PATH_PREFIX))
                else:
                    target = (art, use)
                citers[target].append((art, path))
    reached: set[_Node] = set()
    frontier = list(seeds)
    while frontier:
        node = frontier.pop()
        for citer in citers.get(node, []):
            if citer not in reached:
                reached.add(citer)
                frontier.append(citer)
    return reached


def _dial_forms(dial: str) -> set[str]:
    """Return every path under which a cell may cite a dial.

    A generation or R-band dial is also cited through its ``[]`` list form
    (``inputs.config.generations[].year_available``,
    ``inputs.config.revenue.central[]``).
    """
    forms = {dial, re.sub(r"\[\d+\]", "[]", dial)}
    band = _REVENUE_ANCHOR.match(dial)
    if band is not None:
        forms.add(f"{band.group(1)}[]")
    return forms


def _space_dials(doc: dict[str, Any]) -> list[str]:
    """Return every numeric dial a scenario can set, from the assumption index.

    Skips the validation-only market reference, generation names, and
    extrapolated generation rows (derived by the model, not settable).
    """
    dials = []
    for path, cell in doc["inputs"]["assumption_index"].items():
        value = cell["value"]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            continue
        if path.startswith("inputs.config.market_sanity_check"):
            continue
        if cell["assumption_role"] == "derived_input":
            continue
        dials.append(path)
    return dials


# Dials whose generic unit or relative move is absorbed by rounding, with the
# move that exercises them instead.
_DIAL_CANDIDATES: dict[str, tuple[int | float, ...]] = {
    "inputs.config.cadence.cadence_ceiling": (_MOVING_CADENCE_CEILING,),
}


def _candidate_values(dial: str, value: int | float) -> list[int | float]:
    """Return the perturbed values to try for one dial, in order."""
    if dial in _DIAL_CANDIDATES:
        return list(_DIAL_CANDIDATES[dial])
    if dial.endswith(".year_available"):
        return [value + _YEAR_SHIFT, value - _YEAR_SHIFT]
    if isinstance(value, int):
        return [value + 1, value - 1]
    if value == 0:
        return [_ZERO_DIAL_VALUE]
    return [value * factor for factor in _FLOAT_FACTORS]


def _set_space_dial(space: dict[str, Any], dial: str, value: int | float) -> dict[str, Any]:
    """Return a copy of the space mapping with one dial set."""
    out = copy.deepcopy(space)
    parts = dial.split(".")
    block = parts[2]
    if block in _CONFIG_BLOCKS:
        out.setdefault(_CONFIG_BLOCKS[block], {})[parts[3]] = value
    elif block == "revenue":
        band, fy = parts[3], int(parts[4])
        for anchor in out["r_band"][band]:
            if anchor["fy"] == fy:
                anchor["r"] = value
    else:
        indexed = _INDEX_TOKEN.match(block)
        assert indexed is not None, f"unmapped dial {dial}"
        out["generations"][int(indexed.group("index"))][parts[3]] = value
    return out


def _moved_and_unreached(
    base: dict[_Node, Any],
    space: dict[str, Any],
    ground: dict[str, Any],
    dial_node: tuple[str, str],
) -> tuple[list[_Node], list[_Node]] | None:
    """Build one perturbed run; return its moved cells and those not citing the dial.

    Returns ``None`` when the perturbed scenario is invalid (the caller
    tries the next candidate value).
    """
    try:
        docs = _build_docs(space, ground)
    except ValidationError, ValueError:
        return None
    values = _cell_values(docs)
    moved = [node for node, value in values.items() if node in base and value != base[node]]
    art, dial = dial_node
    reaching = _cells_citing(docs, {(art, form) for form in _dial_forms(dial)})
    return moved, [node for node in moved if node not in reaching]


def test_every_dial_moves_only_cells_that_cite_it_across_both_artifacts(
    scenarios_dir: Path,
) -> None:
    """Objective: the ``uses`` graph is sufficient for every settable dial.

    Perturbs every numeric dial of the default space scenario (cadence,
    fleet, volume, launch cost, physical, slopes, the release cadence, each
    R anchor, each listed generation field) and every ground dial, one at a
    time, and follows ``space:`` pointers from the ground artifact into the
    space artifact. Expected: every cell that moves, in either artifact,
    cites the dial directly or transitively (zero closure misses), and the
    only dials that move nothing are the documented inert ones.
    """
    space, ground = _default_mappings(scenarios_dir)
    base_docs = _build_docs(space, ground)
    base = _cell_values(base_docs)
    unreached: dict[str, list[_Node]] = {}
    inert: set[str] = set()
    moved_total = 0

    for dial in _space_dials(base_docs[_SPACE]):
        value = base_docs[_SPACE]["inputs"]["assumption_index"][dial]["value"]
        for candidate in _candidate_values(dial, value):
            outcome = _moved_and_unreached(
                base, _set_space_dial(space, dial, candidate), ground, (_SPACE, dial)
            )
            if outcome is not None and outcome[0]:
                moved_total += len(outcome[0])
                if outcome[1]:
                    unreached[dial] = outcome[1]
                break
        else:
            inert.add(dial)

    for dial in base_docs[_GROUND]["inputs"]["assumption_index"]:
        key = dial.rsplit(".", 1)[-1]
        outcome = _moved_and_unreached(
            base, space, {**ground, key: ground[key] * _FLOAT_FACTORS[1]}, (_GROUND, dial)
        )
        assert outcome is not None, f"perturbing {dial} made the ground scenario invalid"
        moved_total += len(outcome[0])
        if outcome[1]:
            unreached[dial] = outcome[1]
        if not outcome[0]:
            inert.add(dial)

    assert moved_total > 0
    assert not unreached, {dial: nodes[:3] for dial, nodes in unreached.items()}
    assert inert == set(_EXPECTED_INERT_DIALS), sorted(inert ^ set(_EXPECTED_INERT_DIALS))
