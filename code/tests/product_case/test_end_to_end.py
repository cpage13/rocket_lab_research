"""The product case end to end: the synthetic case through the command to the artifact.

The synthetic engineering artifact (FY2031 to FY2033, round numbers) and the small scenario (16
choices, 50 draws) promoted by ``main`` to a temporary file and read back as JSON. Each test names
what it exercises, its sample and what counts as success.
"""

from __future__ import annotations

import json
import math
import re
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from common.cli import EXIT_OK
from product_case.config import load_product_case_config
from product_case.constants import FORMULA_CATALOG, PATH_SEPARATOR, ProductClass
from product_case.engineering import engineering_view_from_bytes
from product_case.json_output import QUERY_EXAMPLES, main
from product_case.monte_carlo import draw_markets, outcome_in_market
from product_case.offers import choice_grid

type Writer = Callable[[dict[str, Any]], Path]
"""A fixture that writes a mapping to a temporary file and returns its path."""


def _promote(
    scenario: dict[str, Any],
    engineering: dict[str, Any],
    write_scenario: Writer,
    write_engineering: Writer,
    output: Path,
) -> tuple[dict[str, Any], Path]:
    """Promote the case and return the artifact and the scenario's path."""
    scenario["engineering_artifact_path"] = str(write_engineering(engineering))
    scenario_path = write_scenario(scenario)
    assert main([str(scenario_path), str(output), "--version-stamp", "2030-01-02"]) == EXIT_OK
    return json.loads(output.read_text(encoding="utf-8")), scenario_path


@pytest.fixture
def promoted(
    synthetic_scenario: dict[str, Any],
    synthetic_engineering: dict[str, Any],
    write_scenario: Writer,
    write_engineering: Writer,
    tmp_path: Path,
) -> tuple[dict[str, Any], Path]:
    """The synthetic case's artifact and its scenario's path."""
    return _promote(
        synthetic_scenario,
        synthetic_engineering,
        write_scenario,
        write_engineering,
        tmp_path / "case.json",
    )


def _value(cell: dict[str, Any]) -> Any:
    """A provenance cell's value."""
    return cell["value"]


def test_every_choice_reads_in_one_market_and_the_headline_is_the_pick_there(
    promoted: tuple[dict[str, Any], Path],
) -> None:
    """Objective: goal 5: every choice reads in one market; the headline is the pick there, so
    the headline and the draws cannot drift; the pick is a candidate on the candidates' front,
    its prices flat; the spreads are ordered.

    Sample: the synthetic case's artifact.

    Expected outcome: each choice one central revenue per reported year; the headline's market
    the ranges' midpoints; the pick's central revenue equal to the headline's revenue year by
    year; the pick at the start prices on ``fronts.at_start_prices``, its price cells flat; every
    spread's 10th at most its 50th at most its 90th.
    """
    artifact, _ = promoted
    years = [year["year"] for year in artifact["headline"]["years"]]
    assert all(len(choice["central_revenue_musd"]) == len(years) for choice in artifact["choices"])
    assert artifact["headline"]["market"] == {"gamma": 0.75, "epsilon": 1.0, "eta": 0.25}
    pick = artifact["choices"][artifact["pick"]["choice_id"]]
    headline_revenue = [
        _value(year["totals"]["revenue_musd"]) for year in artifact["headline"]["years"]
    ]
    assert pick["central_revenue_musd"] == headline_revenue
    assert pick["at_start_prices"] and pick["choice_id"] in artifact["fronts"]["at_start_prices"]
    for position in range(4):
        prices = {
            _value(year["classes"][position]["price_usd_per_month"])
            for year in artifact["headline"]["years"]
        }
        assert len(prices) == 1
    for year in artifact["spreads"]["years"]:
        for field in year["fields"]:
            for basis in (field["usable_draws"], field["all_draws"]):
                if basis["p10"] is not None:
                    # Ordered within float precision: in a tied distribution (a terminal at its
                    # seats) the quantiles' interpolation can land a unit in the last place off
                    # the median (the design's D10: the two functions may differ in the last bits).
                    low, mid, high = basis["p10"], basis["p50"], basis["p90"]
                    assert low <= mid or math.isclose(low, mid, rel_tol=1e-9)
                    assert mid <= high or math.isclose(mid, high, rel_tol=1e-9)


def test_the_last_data_iot_line_recomputes_by_hand(promoted: tuple[dict[str, Any], Path]) -> None:
    """Objective: the headline's last data IoT line is the demand curve's, recomputed by hand from
    the published inputs.

    Sample: the synthetic case's last reported year, data IoT at the central market.

    Expected outcome: floor(999,000 x k^0.75 x ($15.56 / p)^1.0 x v^0.25) equals the published
    devices, with k from ``network`` and p and v from the data IoT entry.
    """
    artifact, _ = promoted
    last = artifact["headline"]["years"][-1]
    data = next(entry for entry in last["classes"] if entry["product_class"] == "data_iot")
    scale = artifact["network"]["years"][-1]["network_scale"]
    demand = (
        999_000.0
        * scale**0.75
        * (15.56 / _value(data["price_usd_per_month"])) ** 1.0
        * _value(data["service"]) ** 0.25
    )
    assert _value(data["customers"]) == math.floor(demand)


def test_the_stated_assumptions_are_the_runs(
    promoted: tuple[dict[str, Any], Path],
    synthetic_engineering: dict[str, Any],
    as_engineering_bytes: Callable[[dict[str, Any]], bytes],
) -> None:
    """Objective: each stated line is present and built from the run: the data IoT anchor at twice
    Iridium's IoT revenue today; the population sentence; the all-draw count equal to the count
    recomputed from the pick's room and access uses in each of the 50 draws (montecarlo M2).

    Sample: the synthetic case (50 draws, so the shipped run's 73 cannot pass).

    Expected outcome: 13 lines; the anchor, population, usage-stop and engineering-hash lines as
    stated; the M2 line's count equal to the recount.
    """
    artifact, scenario_path = promoted
    lines = artifact["assumptions"]
    assert len(lines) == 13
    text = " ".join(lines)
    assert "twice Iridium's IoT revenue today ($373.1M a year against $186.5M)" in text
    assert "over the population of markets" in text and "within sampling error" in text
    assert artifact["metadata"]["engineering_artifact"]["sha256"] in text
    config = load_product_case_config(scenario_path)
    view = engineering_view_from_bytes(
        as_engineering_bytes(synthetic_engineering),
        path="synthetic",
        reported_years=config.reported_years,
    )
    choice = choice_grid(config)[artifact["pick"]["choice_id"]]
    past = 0
    for market in draw_markets(config):
        years = outcome_in_market(config, view, choice, market).years
        if any(
            max(
                year.totals.iot_uplink_use_busy,
                year.totals.iot_uplink_use_offpeak,
                year.totals.access_use,
            )
            > 1
            for year in years
        ):
            past += 1
    assert artifact["spreads"]["all_draws_basis"]["draws_past_iot_room"] == past
    assert f"in {past:,} of the 50 drawn markets" in text


def _leaves(node: Any, path: str) -> list[tuple[str, Any]]:
    """Every leaf of a JSON value with its data-dictionary path (``[]`` for list items)."""
    if isinstance(node, dict):
        if "formula_name" in node:
            return [(path, node)]
        return [
            leaf
            for key, child in node.items()
            for leaf in _leaves(child, f"{path}.{key}" if path else key)
        ]
    if isinstance(node, list):
        if node and all(isinstance(item, (int, float)) for item in node):
            return [(path, node)]
        return [leaf for item in node for leaf in _leaves(item, f"{path}[]")]
    return [(path, node)]


def test_every_number_is_linked_to_its_formula(promoted: tuple[dict[str, Any], Path]) -> None:
    """Objective: every numeric leaf outside ``inputs`` and ``metadata`` is a provenance cell whose
    formula is in the product case's catalog, or a plain field an entry's output names (the
    counterpart of the data center's V13).

    Sample: the synthetic case's artifact.

    Expected outcome: no unlinked number; every cell's ``formula_name`` a catalog entry.
    """
    artifact, _ = promoted
    outputs = [
        pattern
        for entry in FORMULA_CATALOG.values()
        for pattern in entry.output_path_pattern.split(PATH_SEPARATOR)
    ]
    names = {entry.formula_id for entry in FORMULA_CATALOG.values()}
    unlinked = []
    for path, leaf in _leaves(
        {k: v for k, v in artifact.items() if k not in ("inputs", "metadata")}, ""
    ):
        if isinstance(leaf, dict):
            assert leaf["formula_name"] in names, path
            continue
        numeric = isinstance(leaf, (int, float)) and not isinstance(leaf, bool)
        if (numeric or isinstance(leaf, list)) and not any(
            path == pattern or path.startswith((f"{pattern}.", f"{pattern}["))
            for pattern in outputs
        ):
            unlinked.append(path)
    assert not unlinked, sorted(set(unlinked))


def _resolve(document: dict[str, Any], ref: str) -> Any:
    """A ref such as ``years[year=2031].classes[device_class=x].people_served`` in a document."""
    node: Any = document
    for part in ref.split("."):
        match = re.fullmatch(r"(\w+)(?:\[(\w+)=(\w+)\])?", part)
        assert match, ref
        node = node[match.group(1)]
        if match.group(2):
            node = next(item for item in node if str(item[match.group(2)]) == match.group(3))
    return node


def test_every_engineering_cell_resolves_in_the_artifact_read(
    promoted: tuple[dict[str, Any], Path], synthetic_engineering: dict[str, Any]
) -> None:
    """Objective: every engineering input cell's ref names its value's place in ``iridium-v7``,
    its note the file's SHA-256, a per-year value one cell a year keyed ``<field>.<year>``.

    Sample: the synthetic case's ``inputs.engineering`` against the synthetic artifact.

    Expected outcome: each ref resolves to the cell's value; each note the recorded SHA-256; the
    small terminal's people a cell for each reported year.
    """
    artifact, _ = promoted
    sha = artifact["metadata"]["engineering_artifact"]["sha256"]
    cells = artifact["inputs"]["engineering"]
    for key, cell in cells.items():
        (source,) = cell["source_refs"]
        assert source["ref_type"] == "model_derivation" and source["note"] == sha, key
        assert _resolve(synthetic_engineering, source["ref"]) == cell["value"], key
    assert {f"people_small_terminal.{year}" for year in (2031, 2032, 2033)} <= set(cells)


def test_the_query_examples_run(promoted: tuple[dict[str, Any], Path], tmp_path: Path) -> None:
    """Objective: each worked ``jq`` query runs on the artifact and answers.

    Sample: the synthetic case's artifact, each of the six queries.

    Expected outcome: ``jq`` exits 0 with output for each.
    """
    artifact, _ = promoted
    path = tmp_path / "read_back.json"
    path.write_text(json.dumps(artifact), encoding="utf-8")
    for query in QUERY_EXAMPLES:
        command = ["jq", "-c", query.jq_expression, str(path)]  # noqa: S607  jq from the PATH
        done = subprocess.run(  # noqa: S603  the artifact's own queries on a test's own file
            command,
            capture_output=True,
            text=True,
            check=False,
        )  # noqa: S603, S607
        assert done.returncode == 0 and done.stdout.strip(), (query.name, done.stderr)


def test_iot_customers_move_with_the_draw_and_the_year(
    synthetic_scenario: dict[str, Any],
    write_scenario: Writer,
    synthetic_engineering: dict[str, Any],
    as_engineering_bytes: Callable[[dict[str, Any]], bytes],
) -> None:
    """Objective: no IoT count is ever set: each IoT class's devices come from the demand curve and
    differ between two draws and between two reported years.

    Sample: the small scenario's first choice in draws 0 and 1, every reported year.

    Expected outcome: each IoT class's devices differ between the two draws in the last year, and
    between the first and the last year in a draw.
    """
    config = load_product_case_config(write_scenario(synthetic_scenario))
    view = engineering_view_from_bytes(
        as_engineering_bytes(synthetic_engineering),
        path="synthetic",
        reported_years=config.reported_years,
    )
    choice = choice_grid(config)[0]
    first, second = (
        outcome_in_market(config, view, choice, market) for market in draw_markets(config)[:2]
    )
    for position in (2, 3):
        assert (
            first.years[-1].classes[position].customers
            != second.years[-1].classes[position].customers
        )
        assert (
            first.years[0].classes[position].customers
            != first.years[-1].classes[position].customers
        )


def test_a_central_market_unusable_for_the_pick_is_published_and_warned(
    synthetic_scenario: dict[str, Any],
    synthetic_engineering: dict[str, Any],
    write_scenario: Writer,
    write_engineering: Writer,
    tmp_path: Path,
) -> None:
    """Objective: E6: when the central market fails a usable test for the pick, the headline is a
    reading, not a gate: published with ``usable`` false and its failing tests, warned; and the
    fallback is warned with its share.

    Sample: the small scenario at the anchors' prices ($47 and $259 held flat): at the ranges'
    midpoints the terminals fill under three quarters of their busy-hour beams.

    Expected outcome: exit 0 and the artifact written; ``headline.usable`` false naming the fill;
    the E6 and fallback warnings ``warn``.
    """
    synthetic_scenario["prices"]["small_terminal"] = {
        "start_usd_month": 47.0,
        "end_usd_month": [47.0],
    }
    synthetic_scenario["prices"]["mounted_terminal"] = {
        "start_usd_month": 259.0,
        "end_usd_month": [259.0],
    }
    artifact, _ = _promote(
        synthetic_scenario,
        synthetic_engineering,
        write_scenario,
        write_engineering,
        tmp_path / "e6.json",
    )
    assert (
        artifact["headline"]["usable"] is False and "fill" in artifact["headline"]["failing_tests"]
    )
    results = {r["validation_id"]: r["severity"] for r in artifact["meta"]["validation_results"]}
    assert results["warning.central_market_unusable_for_pick"] == "warn"
    assert results["warning.start_prices_under_robust_floor"] == "warn"


def test_a_believability_flag_never_refuses(
    synthetic_scenario: dict[str, Any],
    synthetic_engineering: dict[str, Any],
    write_scenario: Writer,
    write_engineering: Writer,
    tmp_path: Path,
) -> None:
    """Objective: a believability FLAG is a warning: the command still writes the artifact.

    Sample: the small scenario with the small terminal at $48, above its anchor ARPU ($47).

    Expected outcome: exit 0; the anchor check ``warn`` in every reported year.
    """
    synthetic_scenario["prices"]["small_terminal"] = {
        "start_usd_month": 48.0,
        "end_usd_month": [48.0],
    }
    artifact, _ = _promote(
        synthetic_scenario,
        synthetic_engineering,
        write_scenario,
        write_engineering,
        tmp_path / "flag.json",
    )
    results = {r["validation_id"]: r["severity"] for r in artifact["meta"]["validation_results"]}
    for year in (2031, 2032, 2033):
        assert (
            results[
                f"believability.{ProductClass.SMALL_TERMINAL}.price_at_or_below_anchor_arpu.{year}"
            ]
            == "warn"
        )
