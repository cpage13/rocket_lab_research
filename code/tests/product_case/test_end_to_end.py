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
from product_case.config import ProductCaseConfig, load_product_case_config
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
                    assert basis["p10"] <= basis["p50"] <= basis["p90"], (year["year"], field)


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


type Change = Callable[[dict[str, Any]], None]
"""A change to a scenario's or an engineering artifact's mapping."""


def _anchors_prices(scenario: dict[str, Any]) -> None:
    """The terminals at their anchors' prices, $47 and $259, held flat (E6's sample)."""
    scenario["prices"]["small_terminal"] = {"start_usd_month": 47.0, "end_usd_month": [47.0]}
    scenario["prices"]["mounted_terminal"] = {"start_usd_month": 259.0, "end_usd_month": [259.0]}


def _tone_room_a_hundredth(engineering: dict[str, Any]) -> None:
    """A hundredth of IoT's single-tone room in every year, so the tone room binds."""
    for year in engineering["years"]:
        year["iot"]["single_tone_seconds_per_second"] /= 100


def _no_change(_: dict[str, Any]) -> None:
    """No change."""


STATED_SAMPLES: tuple[tuple[str, Change, Change, str, bool], ...] = (
    ("the synthetic case", _no_change, _no_change, "robust_floor_met", False),
    ("the anchors' prices, E6", _anchors_prices, _no_change, "most_usable_fallback", False),
    (
        "a hundredth of the tone room",
        _no_change,
        _tone_room_a_hundredth,
        "most_usable_fallback",
        True,
    ),
)
"""Each sample of the stated lines' test: its scenario change, its engineering change, the pick's
basis it reaches, and whether some draws pass the single-tone room alone."""


def _floor_draws(draws: int, robust: float) -> int:
    """The fewest usable draws that reach the robust floor, by the pick's own comparison."""
    return next(count for count in range(draws + 1) if count / draws >= robust)


def _stated_lines(artifact: dict[str, Any], config: ProductCaseConfig) -> list[str]:
    """The 13 stated lines as this run must state them, each number read from the artifact's
    published values (its constants' input cells, network, choices, pick, headline, spreads and
    metadata) or the scenario, never the shipped run's, so a line true only at the shipped
    settings fails."""
    constants = {key: cell["value"] for key, cell in artifact["inputs"]["constants"].items()}

    def anchor(product_class: str) -> str:
        customers = constants[f"anchors.{product_class}.customers"]
        return f"{customers:,.0f} at ${constants[f'anchors.{product_class}.arpu_usd_month']:g}"

    minimal_today = (
        constants["anchors.minimal_packet_iot.customers"]
        * constants["anchors.minimal_packet_iot.arpu_usd_month"]
        * 12
        / 1e6
    )
    data_anchor = (
        constants["anchors.data_iot.customers"] * constants["anchors.data_iot.arpu_usd_month"] * 12
    ) / 1e6
    network = artifact["network"]["years"]
    market, prices = config.market, config.prices
    pick = artifact["pick"]
    chosen = next(c for c in artifact["choices"] if c["choice_id"] == pick["choice_id"])
    floor = (
        f"the robust floor's {_floor_draws(market.draws, config.floors.robust):,} "
        f"({100 * config.floors.robust:g} percent of the draws)"
    )
    if pick["basis"] == "robust_floor_met":
        why = (
            "What stops the usage: the pick's IoT usage rises while its median summed revenue "
            f"rises and its usable draws stay at or above {floor}; every candidate shares the "
            "terminals' fill, so IoT's own failures may take only the draws between the fill's "
            "share and that floor."
        )
    else:
        why = (
            f"What stops the usage: no candidate reaches {floor}, so the pick is the most usable "
            "candidate, the first on the candidates' front, ties to the higher median, and its "
            "usage is that candidate's; the run warns of it and never lowers a price."
        )
    last = artifact["headline"]["years"][-1]
    iot = {entry["product_class"]: entry["iot"] for entry in last["classes"] if entry["iot"]}
    basis = artifact["spreads"]["all_draws_basis"]
    engineering = artifact["metadata"]["engineering_artifact"]
    return [
        "Each class's customers come from the demand curve D = N x k^gamma x (A / p)^epsilon x "
        "v^eta, anchored on Iridium's customers and ARPU today (COMM-617, COMM-618): the small "
        f"terminal {anchor('small_terminal')}, the mounted terminal {anchor('mounted_terminal')}, "
        f"minimal-packet IoT {anchor('minimal_packet_iot')} (Iridium's one reported commercial "
        "IoT segment, taken whole).",
        "Data IoT is anchored beside that segment at the investor's proportion (2026-10-04), half "
        f"the count at double the ARPU, {anchor('data_iot')} (COMM-726), so the two IoT classes "
        "start from twice Iridium's IoT revenue today, a run rate at today's count and ARPU "
        f"(${minimal_today + data_anchor:,.1f}M a year against ${minimal_today:,.1f}M).",
        "The network's scale k is the terminals' seats over Iridium's "
        f"{constants['terminal_customers_today']:,} terminal customers today, the seats read from "
        f"the engineering artifact: k = {network[0]['network_scale']:.1f} in "
        f"FY{network[0]['year']} and {network[-1]['network_scale']:.1f} in "
        f"FY{network[-1]['year']}.",
        "The prices are held flat in nominal dollars at the scenario's start prices (the small "
        f"terminal ${prices.small_terminal.start_usd_month:g}, the mounted terminal "
        f"${prices.mounted_terminal.start_usd_month:g}, minimal-packet IoT "
        f"${prices.minimal_packet_iot.start_usd_month:g}, data IoT "
        f"${constants['data_iot_price_multiple'] * prices.minimal_packet_iot.start_usd_month:g}); "
        "inflation is not modeled.",
        "The market's three responses are drawn independently and uniformly over their ranges "
        f"(gamma {market.gamma.low:g} to {market.gamma.high:g}, epsilon {market.epsilon.low:g} to "
        f"{market.epsilon.high:g}, eta {market.eta.low:g} to {market.eta.high:g}; "
        f"{market.draws:,} draws, seed {market.seed}), so each class's customers at the central "
        f"market are its median over the population of markets and, in the {market.draws:,} "
        "drawn markets, within sampling error of it.",
        "IoT is uncapped: each IoT class sells every device its demand curve gives, bounded by its "
        "uplink room, its random access and its single-tone time, which the usable test checks; "
        "no IoT count is ever set.",
        f"{why} This run's pick: minimal-packet IoT x{chosen['minimal_packet_scale']:g} and data "
        f"IoT x{chosen['data_iot_scale']:g}, usable in {chosen['usable_draws']:,} of "
        f"{market.draws:,} draws ({pick['basis']}).",
        "Each IoT class's usage and time basis differ from the engineering capacity's: the "
        "engineering artifact counts each class's devices alone at its reference usage, averaged "
        "over the day; the product case sells at the pick's usage by period "
        f"({iot['minimal_packet_iot']['messages_per_day']['value']:,} messages a day for "
        f"minimal-packet IoT and {iot['data_iot']['bursts_per_day']['value']:,} bursts a day for "
        f"data IoT in FY{last['year']}), so its devices are never divided by that capacity.",
        "IoT's room is the whole uplink in its share of the frame after the MAC efficiency, with "
        "the random-access window and the single-tone room; the terminals' own upload is not "
        "subtracted.",
        "The all-draw spreads cover every drawn market, the usable test not applied: in "
        f"{basis['draws_past_iot_room']:,} of the {basis['draws']:,} drawn markets the pick sells "
        "IoT past its uplink, access or single-tone room in some reported year.",
        "People and devices are never added: no total of customers is published; bytes add "
        "across the classes in the GB carried.",
        "Government is left out of revenue.",
        f"The engineering inputs are read from {engineering['path']} "
        f"({engineering['schema_version']}, stamp {engineering['version_stamp']}) at SHA-256 "
        f"{engineering['sha256']}; the product case never feeds the engineering model.",
    ]


@pytest.mark.parametrize(
    ("name", "scenario_change", "engineering_change", "basis", "tone_binds"),
    STATED_SAMPLES,
    ids=[sample[0] for sample in STATED_SAMPLES],
)
def test_the_stated_assumptions_are_the_runs_line_by_line(
    name: str,
    scenario_change: Change,
    engineering_change: Change,
    basis: str,
    tone_binds: bool,
    synthetic_scenario: dict[str, Any],
    synthetic_engineering: dict[str, Any],
    write_scenario: Writer,
    write_engineering: Writer,
    as_engineering_bytes: Callable[[dict[str, Any]], bytes],
    tmp_path: Path,
) -> None:
    """Objective: every stated line is the run's, line by line (task 9's list; a line true only at
    the shipped settings is the failure code_switch M1 found in p6): the 13 lines equal the lines
    this test writes from the artifact's own published values and the scenario, never the shipped
    run's; the usage-stop line follows the pick's basis (the spec lens's M1: the robust floor's
    mechanism, or the fallback in the design's D19 words); the data IoT anchor at twice Iridium's
    IoT revenue today, a run rate (montecarlo M1, the spec lens's m1); the population sentence
    (m5); the all-draw count equal to the count this test recomputes from the pick's four uses in
    each of the 50 draws (montecarlo M2), the single-tone room among them (the numerics lens's
    m4).

    Sample: the synthetic case (robust_floor_met), the anchors' prices, $47 and $259 held flat
    (E6, most_usable_fallback), and a hundredth of the single-tone room (most_usable_fallback,
    some draws past the tone room alone); each 50 draws, so a count copied from the shipped 73
    cannot pass.

    Expected outcome: the pick's basis as the sample reaches it; the artifact's assumptions equal
    the 13 lines written from the run; the label's count equal to the recount; where the tone room
    binds, the recount without it smaller (the tone room counted).
    """
    scenario_change(synthetic_scenario)
    engineering_change(synthetic_engineering)
    artifact, scenario_path = _promote(
        synthetic_scenario,
        synthetic_engineering,
        write_scenario,
        write_engineering,
        tmp_path / "stated.json",
    )
    config = load_product_case_config(scenario_path)
    assert artifact["pick"]["basis"] == basis
    assert artifact["assumptions"] == _stated_lines(artifact, config)
    view = engineering_view_from_bytes(
        as_engineering_bytes(synthetic_engineering),
        path="synthetic",
        reported_years=config.reported_years,
    )
    choice = choice_grid(config)[artifact["pick"]["choice_id"]]
    past = past_room_or_access = 0
    for market in draw_markets(config):
        years = outcome_in_market(config, view, choice, market).years
        room_or_access = any(
            not use <= 1
            for year in years
            for use in (
                year.totals.iot_uplink_use_busy,
                year.totals.iot_uplink_use_offpeak,
                year.totals.access_use,
            )
        )
        tone = any(not year.totals.single_tone_use <= 1 for year in years)
        past += room_or_access or tone
        past_room_or_access += room_or_access
    assert artifact["spreads"]["all_draws_basis"]["draws_past_iot_room"] == past
    assert (past_room_or_access < past) is tone_binds


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


COUNT_MAPS: tuple[str, ...] = ("choices[].draws_failing", "meta.source_status_summary")
"""The two catalog outputs that name a map of counts, each count under one linked by its prefix:
the draws failing each usable test, and the input cells counted by source status. Every other
plain number is linked only by an output path that names it exactly (the spec lens's m4: a
prefix such as ``headline.years[]`` would admit any number under a headline year)."""


def _unlinked(artifact: dict[str, Any]) -> list[str]:
    """Each plain number (or list of numbers) outside ``inputs`` and ``metadata`` that no catalog
    output names, exactly or under one of the count maps; provenance cells are left to the
    caller."""
    outputs = {
        pattern
        for entry in FORMULA_CATALOG.values()
        for pattern in entry.output_path_pattern.split(PATH_SEPARATOR)
    }
    under_maps = tuple(f"{prefix}." for prefix in COUNT_MAPS)
    unlinked = []
    for path, leaf in _leaves(
        {k: v for k, v in artifact.items() if k not in ("inputs", "metadata")}, ""
    ):
        if isinstance(leaf, dict):
            continue
        numeric = isinstance(leaf, (int, float)) and not isinstance(leaf, bool)
        if (
            (numeric or isinstance(leaf, list))
            and path not in outputs
            and not path.startswith(under_maps)
        ):
            unlinked.append(path)
    return unlinked


def test_every_number_is_linked_to_its_formula(promoted: tuple[dict[str, Any], Path]) -> None:
    """Objective: every numeric leaf outside ``inputs`` and ``metadata`` is a provenance cell whose
    formula is in the product case's catalog, or a plain field an entry's output names exactly,
    or a count in one of the two maps of counts (the counterpart of the data center's V13); and
    the check is not vacuous: a plain number added where no output names it is reported (the
    spec lens's m4: a customers total under a headline year, a number under the all-draw basis,
    a number under a choice).

    Sample: the synthetic case's artifact, then three copies each with one plain number added.

    Expected outcome: no unlinked number and every cell's ``formula_name`` a catalog entry; each
    added number reported unlinked at its own path.
    """
    artifact, _ = promoted
    names = {entry.formula_id for entry in FORMULA_CATALOG.values()}
    for path, leaf in _leaves(
        {k: v for k, v in artifact.items() if k not in ("inputs", "metadata")}, ""
    ):
        if isinstance(leaf, dict):
            assert leaf["formula_name"] in names, path
    assert _unlinked(artifact) == []
    added: tuple[tuple[tuple[str | int, ...], str, str], ...] = (
        (("headline", "years", 0), "customers_total", "headline.years[].customers_total"),
        (
            ("spreads", "all_draws_basis"),
            "draws_at_seats",
            "spreads.all_draws_basis.draws_at_seats",
        ),
        (("choices", 0), "typical_draw", "choices[].typical_draw"),
    )
    for where, key, path in added:
        changed = json.loads(json.dumps(artifact))
        node: Any = changed
        for step in where:
            node = node[step]
        node[key] = 1
        assert _unlinked(changed) == [path], path


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
