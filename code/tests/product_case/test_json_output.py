"""The product case's command (``product_case.json_output``, B6): the artifact and the refusals.

The synthetic engineering artifact (FY2031 to FY2033, round numbers) and the small scenario (16
choices, 50 draws) through ``main``, to temporary files. Each test names what it exercises, its
sample and what counts as success.
"""

from __future__ import annotations

import hashlib
import json
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from common.cli import EXIT_ERROR, EXIT_OK
from product_case.json_output import DEFAULT_ARTIFACT_PATH, main

type Writer = Callable[[dict[str, Any]], Path]
"""A fixture that writes a mapping to a temporary file and returns its path."""

STAMP = "2030-01-02"
"""The stamp the tests promote at."""


def _promote(
    scenario: dict[str, Any],
    engineering: dict[str, Any] | None,
    write_scenario: Writer,
    write_engineering: Writer,
    output: Path | str,
) -> int:
    """Point the scenario at a written engineering artifact (when given) and run the command."""
    if engineering is not None:
        scenario["engineering_artifact_path"] = str(write_engineering(engineering))
    return main([str(write_scenario(scenario)), str(output), "--version-stamp", STAMP])


def test_the_synthetic_case_promotes_and_a_second_promotion_is_byte_identical(
    synthetic_scenario: dict[str, Any],
    synthetic_engineering: dict[str, Any],
    synthetic_stamp: str,
    write_scenario: Writer,
    write_engineering: Writer,
    tmp_path: Path,
) -> None:
    """Objective: the command writes ``product-case-v1`` from the synthetic case, the metadata
    naming the engineering file's stamp and the SHA-256 of its bytes, and a second promotion
    writes the same bytes.

    Sample: the synthetic artifact and the small scenario, promoted twice at one stamp.

    Expected outcome: exit 0 twice; the two files equal byte for byte; the schema
    ``product-case-v1``; the engineering artifact's stamp and SHA-256 those of the file read; the
    top-level blocks in the foundation's order; the classes in class order.
    """
    engineering_path = write_engineering(synthetic_engineering)
    synthetic_scenario["engineering_artifact_path"] = str(engineering_path)
    scenario = write_scenario(synthetic_scenario)
    first, second = tmp_path / "first.json", tmp_path / "second.json"
    assert main([str(scenario), str(first), "--version-stamp", STAMP]) == EXIT_OK
    assert main([str(scenario), str(second), "--version-stamp", STAMP]) == EXIT_OK
    assert first.read_bytes() == second.read_bytes()
    artifact = json.loads(first.read_text(encoding="utf-8"))
    assert list(artifact) == [
        "metadata", "inputs", "network", "choices", "fronts", "pick", "headline", "spreads",
        "meta", "assumptions",
    ]  # fmt: skip
    metadata = artifact["metadata"]
    assert metadata["schema_version"] == "product-case-v1"
    assert metadata["version_stamp"] == STAMP
    read = metadata["engineering_artifact"]
    assert read["version_stamp"] == synthetic_stamp
    assert read["sha256"] == hashlib.sha256(engineering_path.read_bytes()).hexdigest()
    classes = [entry["product_class"] for entry in artifact["headline"]["years"][0]["classes"]]
    assert classes == ["small_terminal", "mounted_terminal", "minimal_packet_iot", "data_iot"]


def test_every_block_holds_the_foundations_keys_in_order(
    synthetic_scenario: dict[str, Any],
    synthetic_engineering: dict[str, Any],
    write_scenario: Writer,
    write_engineering: Writer,
    tmp_path: Path,
) -> None:
    """Objective: the artifact is the foundation's ``product-case-v1``, key by key in its order
    below the top level too (the spec lens's S2 and m4): each block's keys, the classes and the
    spread fields in their enums' orders, a terminal's or an IoT class's block by its kind, the
    all-draw basis's record, and so no key the foundation does not name (no total of customers).

    Sample: the synthetic case's artifact.

    Expected outcome: every block's keys equal the foundation's list, in order.
    """
    output = tmp_path / "keys.json"
    assert (
        _promote(
            synthetic_scenario, synthetic_engineering, write_scenario, write_engineering, output
        )
        == EXIT_OK
    )
    artifact = json.loads(output.read_text(encoding="utf-8"))
    classes = ["small_terminal", "mounted_terminal", "minimal_packet_iot", "data_iot"]
    tests = [
        "fill", "margin", "iot_uplink_busy", "iot_uplink_offpeak", "random_access",
        "single_tone_time", "revenue_rising",
    ]  # fmt: skip
    fields = [
        "small_terminal.customers", "small_terminal.revenue_musd", "mounted_terminal.customers",
        "mounted_terminal.revenue_musd", "minimal_packet_iot.customers",
        "minimal_packet_iot.revenue_musd", "data_iot.customers", "data_iot.revenue_musd",
        "revenue_musd", "margin_pct", "iot_uplink_use_busy", "iot_uplink_use_offpeak",
    ]  # fmt: skip
    assert list(artifact["metadata"]) == [
        "model", "schema_version", "scenario_name", "source_scenario_path", "version_stamp",
        "engineering_artifact",
    ]  # fmt: skip
    assert list(artifact["metadata"]["engineering_artifact"]) == [
        "path", "schema_version", "version_stamp", "sha256",
    ]  # fmt: skip
    assert list(artifact["inputs"]) == ["scenario", "constants", "engineering"]
    assert list(artifact["network"]) == ["small_terminal_share", "years"]
    for year in artifact["network"]["years"]:
        assert list(year) == [
            "year", "seats_small_terminal", "seats_mounted_terminal", "network_scale",
        ]  # fmt: skip
    for choice in artifact["choices"]:
        assert list(choice) == [
            "choice_id", "end_prices", "minimal_packet_scale", "data_iot_scale",
            "at_start_prices", "usable_draws", "usable_share", "median_summed_revenue_musd",
            "median_last_year_revenue_musd", "central_revenue_musd",
            "central_summed_revenue_musd", "central_usable", "draws_failing",
        ]  # fmt: skip
        assert list(choice["end_prices"]) == classes
        assert list(choice["draws_failing"]) == tests
    assert list(artifact["fronts"]) == ["all_prices", "at_start_prices"]
    assert list(artifact["pick"]) == [
        "choice_id",
        "basis",
        "usage_edges",
        "dominated_in_context_by",
    ]
    headline = artifact["headline"]
    assert list(headline) == ["market", "usable", "failing_tests", "years"]
    assert list(headline["market"]) == ["gamma", "epsilon", "eta"]
    for year in headline["years"]:
        assert list(year) == ["year", "classes", "totals"]
        assert [entry["product_class"] for entry in year["classes"]] == classes
        for entry in year["classes"]:
            assert list(entry) == [
                "product_class", "kind", "price_usd_per_month", "service", "demand",
                "customers", "revenue_musd", "price_per_unit", "terminal", "iot",
            ]  # fmt: skip
            if entry["kind"] == "terminal":
                assert entry["iot"] is None
                assert list(entry["terminal"]) == [
                    "seats", "seats_filled", "busy_hour_gb_per_month", "offpeak_gb_per_month",
                    "active_rate_mbps", "offpeak_downlink_use",
                ]  # fmt: skip
            else:
                assert entry["terminal"] is None
                assert list(entry["iot"]) == [
                    "messages_per_day", "bursts_per_day", "bursts_outside_busy_hours",
                    "bytes_per_day", "uplink_use_busy", "uplink_use_offpeak",
                ]  # fmt: skip
        assert list(year["totals"]) == [
            "revenue_musd", "fleet_annual_cost_musd", "margin_pct", "profit_musd",
            "busy_hour_beams_filled", "iot_uplink_use_busy", "iot_uplink_use_offpeak",
            "access_use", "access_attempts_per_second_per_beam", "single_tone_use",
            "gb_carried_per_year", "cost_per_gb_carried_usd",
        ]  # fmt: skip
    spreads = artifact["spreads"]
    assert list(spreads) == ["all_draws_basis", "years"]
    assert list(spreads["all_draws_basis"]) == ["label", "draws", "draws_past_iot_room"]
    for year in spreads["years"]:
        assert list(year) == ["year", "fields"]
        assert [field["field"] for field in year["fields"]] == fields
        for field in year["fields"]:
            assert list(field) == ["field", "usable_draws", "all_draws", "every_seat"]
            assert list(field["usable_draws"]) == [
                "p10", "p50", "p90", "headline_rank", "null_reason",
            ]  # fmt: skip
            assert list(field["all_draws"]) == ["p10", "p50", "p90", "headline_rank"]
            if field["field"].split(".")[0] in classes[:2]:
                assert list(field["every_seat"]) == [
                    "headline_sells_every_seat", "usable_draws_share", "all_draws_share",
                ]  # fmt: skip
            else:
                assert field["every_seat"] is None
    assert list(artifact["meta"]) == [
        "formulas", "validation_results", "data_dictionary", "query_examples",
        "source_status_summary",
    ]  # fmt: skip
    assert all(isinstance(line, str) for line in artifact["assumptions"])


def test_each_cell_names_its_kinds_uses_and_its_sources(
    synthetic_scenario: dict[str, Any],
    synthetic_engineering: dict[str, Any],
    write_scenario: Writer,
    write_engineering: Writer,
    tmp_path: Path,
) -> None:
    """Objective: each headline cell traces what it reads (the spec lens's m8): a class's cells
    use only its own kind's paths (an IoT class no terminal seats, a terminal no IoT bytes and no
    MB size); the customers cells cite data IoT's anchor row (COMM-726), the margin and profit
    cells the prices' row (COMM-722) as revenue does; the decimal MB is an input cell beside the
    GB (COMM-724), which data IoT's price per unit uses.

    Sample: the synthetic case's artifact, every headline year and class.

    Expected outcome: no IoT class's cell uses a path under ``terminal.`` and no terminal's one
    under ``iot.`` or the MB's size; every customers cell's sources hold COMM-726 and every
    margin and profit cell's COMM-722; ``inputs.constants.bytes_per_mb`` holds 1,000,000, status
    ``scenario``, citing COMM-724; data IoT's price-per-unit cells use it.
    """
    output = tmp_path / "cells.json"
    assert (
        _promote(
            synthetic_scenario, synthetic_engineering, write_scenario, write_engineering, output
        )
        == EXIT_OK
    )
    artifact = json.loads(output.read_text(encoding="utf-8"))
    classes = "headline.years[].classes[]"
    others = {
        "terminal": (f"{classes}.iot.", "inputs.constants.bytes_per_mb"),
        "iot": (f"{classes}.terminal.",),
    }
    for year in artifact["headline"]["years"]:
        for entry in year["classes"]:
            blocks = [entry, *(entry[name] for name in ("terminal", "iot") if entry[name])]
            for block in blocks:
                for key, cell in block.items():
                    if isinstance(cell, dict) and "formula_name" in cell:
                        used = [
                            use for use in cell["uses"] if use.startswith(others[entry["kind"]])
                        ]
                        assert used == [], (entry["product_class"], key, used)
            assert "COMM-726" in entry["customers"]["sources"], entry["product_class"]
        for name in ("margin_pct", "profit_musd"):
            assert "COMM-722" in year["totals"][name]["sources"], name
        data = next(entry for entry in year["classes"] if entry["product_class"] == "data_iot")
        assert "inputs.constants.bytes_per_mb" in data["price_per_unit"]["uses"]
    megabyte = artifact["inputs"]["constants"]["bytes_per_mb"]
    assert (megabyte["value"], megabyte["source_status"]) == (1_000_000, "scenario")
    assert megabyte["source_refs"][0]["claim_id"] == "COMM-724"


def _set(path: tuple[str, ...], value: object) -> Callable[[dict[str, Any]], None]:
    """A change setting one key of a nested mapping."""

    def change(mapping: dict[str, Any]) -> None:
        target = mapping
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value

    return change


def _zero_rooms(year: int) -> Callable[[dict[str, Any]], None]:
    """A downlink share of 1 in ``year``: the payload and single-tone rooms zero."""

    def change(artifact: dict[str, Any]) -> None:
        for entry in artifact["years"]:
            if entry["year"] == year:
                entry["iot"]["uplink_payload_bits_per_second"] = 0.0
                entry["iot"]["single_tone_seconds_per_second"] = 0.0

    return change


def _keep(_: dict[str, Any]) -> None:
    """No change."""


REFUSALS: tuple[
    tuple[str, Callable[[dict[str, Any]], None], Callable[[dict[str, Any]], None], str], ...
] = (
    (
        "an IoT count in the scenario",
        _set(("usage", "minimal_packet_iot", "devices"), 1_000_000),
        _keep,
        "usage.minimal_packet_iot.devices",
    ),
    (
        "an engineering artifact of another schema",
        _keep,
        _set(("provenance", "schema_version"), "iridium-v6"),
        "iridium-v7",
    ),
    (
        "a null coverage floor year",
        _keep,
        _set(("trajectory_summary", "coverage_floor_reached_year"), None),
        "coverage_floor_reached_year is null",
    ),
    (
        "a reported year before the floor",
        _set(("reported_years",), [2030, 2031, 2032]),
        _keep,
        "FY2030",
    ),
    ("a zero room (d = 1)", _keep, _zero_rooms(2032), "FY2032"),
    (
        "no usable choice",
        _set(("floors", "margin_pct"), 99.9),
        _keep,
        "the test their draws fail most is margin",
    ),
    (
        "a number that is not finite",
        _set(("prices", "small_terminal"), {"start_usd_month": 5e-324, "end_usd_month": [5e-324]}),
        _keep,
        "not a finite number: small_terminal's numbers scale with prices.small_terminal.",
    ),
    (
        "a number that is not finite, an IoT price",
        _set(
            ("prices", "minimal_packet_iot"), {"start_usd_month": 5e-324, "end_usd_month": [5e-324]}
        ),
        _keep,
        "the run's choices[0].central_revenue_musd[0] is inf, not a finite number",
    ),
)
"""Each refusal: its change to the scenario, its change to the engineering artifact, what the one
error line names."""


@pytest.mark.parametrize(
    ("name", "scenario_change", "engineering_change", "named"),
    REFUSALS,
    ids=[case[0] for case in REFUSALS],
)
def test_each_refusal_is_one_error_line_exit_1_and_no_file(
    name: str,
    scenario_change: Callable[[dict[str, Any]], None],
    engineering_change: Callable[[dict[str, Any]], None],
    named: str,
    synthetic_scenario: dict[str, Any],
    synthetic_engineering: dict[str, Any],
    write_scenario: Writer,
    write_engineering: Writer,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Objective: every expected failure of the command is one ``ERROR:`` line naming its cause,
    exit status 1, and no file written.

    Sample: the synthetic case with one change each: an IoT device count in the scenario (an
    unknown key), ``iridium-v6``, a null floor year, a reported year before the floor, a zero
    room at a downlink share of 1, a margin floor no draw reaches, a small-terminal price of
    5e-324 dollars (its demand overflows while it sells every seat, E8: refused naming the field
    and the small terminal's settings), and a minimal-packet IoT price of 5e-324 dollars (its
    devices overflow, so no candidate is usable: refused as a number that is not finite, never as
    no usable choice, the spec lens's m5).

    Expected outcome: exit 1; one ERROR record naming the cause; the output file absent.
    """
    scenario_change(synthetic_scenario)
    engineering_change(synthetic_engineering)
    output = tmp_path / "refused.json"
    with caplog.at_level(logging.INFO):
        status = _promote(
            synthetic_scenario, synthetic_engineering, write_scenario, write_engineering, output
        )
    errors = [record for record in caplog.records if record.levelno >= logging.ERROR]
    assert status == EXIT_ERROR
    assert len(errors) == 1 and named in errors[0].getMessage(), errors[0].getMessage()
    assert not output.exists()


def test_the_file_refusals(
    synthetic_scenario: dict[str, Any],
    synthetic_engineering: dict[str, Any],
    write_scenario: Writer,
    write_engineering: Writer,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Objective: the command refuses an engineering artifact that is missing or not JSON, the
    default artifact's path from a scenario other than the shipped one (before anything is read),
    and a symbolic-link destination, each one ``ERROR:`` line, exit 1, nothing written.

    Sample: the synthetic case pointed at a missing file and at a file of text; the default path
    as the output; a symbolic link as the output.

    Expected outcome: four refusals, each naming its cause; the default path's file unchanged
    (absent before and after, or the same bytes); the link's target never created.
    """
    cases: list[tuple[str, Path | str, str]] = []
    missing = dict(synthetic_scenario, engineering_artifact_path=str(tmp_path / "missing.json"))
    cases.append(("missing", tmp_path / "a.json", "cannot read the engineering artifact"))
    text = tmp_path / "text.json"
    text.write_text("not json", encoding="utf-8")
    not_json = dict(synthetic_scenario, engineering_artifact_path=str(text))
    cases.append(("not JSON", tmp_path / "b.json", "not JSON"))
    target = tmp_path / "target.json"
    link = tmp_path / "link.json"
    link.symlink_to(target)
    for scenario, (_, output, named) in zip((missing, not_json), cases, strict=True):
        caplog.clear()
        assert main([str(write_scenario(scenario)), str(output)]) == EXIT_ERROR
        assert [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR][0].count(
            named
        )
        assert not Path(output).exists()
    caplog.clear()
    default_before = _bytes_or_none(DEFAULT_ARTIFACT_PATH)
    assert (
        _promote(
            synthetic_scenario,
            synthetic_engineering,
            write_scenario,
            write_engineering,
            DEFAULT_ARTIFACT_PATH,
        )
        == EXIT_ERROR
    )
    assert (
        "is written only from code/scenarios/product_case.yaml" in caplog.records[-1].getMessage()
    )
    assert _bytes_or_none(DEFAULT_ARTIFACT_PATH) == default_before
    caplog.clear()
    assert (
        _promote(synthetic_scenario, synthetic_engineering, write_scenario, write_engineering, link)
        == EXIT_ERROR
    )
    assert "symbolic link" in caplog.records[-1].getMessage()
    assert not target.exists()


def _bytes_or_none(repository_path: str) -> bytes | None:
    """The bytes of a repository file, or None when it does not exist."""
    path = Path(__file__).resolve().parents[3] / repository_path
    return path.read_bytes() if path.exists() else None
