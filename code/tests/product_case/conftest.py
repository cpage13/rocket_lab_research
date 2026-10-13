"""Fixtures shared by the product case's tests.

The shipped scenario (``code/scenarios/product_case.yaml``) as a path and as a fresh mapping a
test may change, and a writer that puts a changed scenario in a temporary folder, so a test
loads it through the real loader (``load_product_case_config``). A synthetic engineering
artifact of round numbers (:func:`synthetic_engineering_artifact`), the ``iridium-v7`` fields the
product case reads and nothing else, as a fresh mapping a test may change, with a writer of its
JSON bytes; the end-to-end case reuses it. Every path is anchored to the root ``conftest.py``'s
fixtures, never to the working directory, so the suite runs from ``code/`` and from the
repository root.
"""

from __future__ import annotations

import copy
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any, Final

import pytest
import yaml

from common.file_io import load_yaml_mapping

type ScenarioWriter = Callable[[dict[str, Any]], Path]
"""Writes a scenario mapping to a temporary YAML file and returns its path."""

type EngineeringWriter = Callable[[dict[str, Any]], Path]
"""Writes an engineering artifact mapping to a temporary JSON file and returns its path."""

SYNTHETIC_STAMP: Final[str] = "2030-01-01"
"""The synthetic engineering artifact's version stamp."""

SYNTHETIC_FLOOR_YEAR: Final[int] = 2031
"""The synthetic artifact's coverage floor year: its first year with people (2030 has none)."""

SYNTHETIC_REPORTED_YEARS: Final[tuple[int, ...]] = (2031, 2032, 2033)
"""The synthetic artifact's three years at or past its floor, the reported years a synthetic
scenario reads."""

SYNTHETIC_YEARS: Final[dict[int, dict[str, int | float]]] = {
    2030: {
        "living_fleet": 200,
        "annual_cost_musd": 80.0,
        "small": 0,
        "mounted": 0,
        "phone_beams": 8_000.0,
        "payload": 2.8e9,
        "access": 456_000.0,
        "tone": 5.6e6,
    },
    2031: {
        "living_fleet": 500,
        "annual_cost_musd": 200.0,
        "small": 4_000_000,
        "mounted": 500_000,
        "phone_beams": 20_000.0,
        "payload": 7.0e9,
        "access": 1_140_000.0,
        "tone": 1.4e7,
    },
    2032: {
        "living_fleet": 1_000,
        "annual_cost_musd": 400.0,
        "small": 8_000_000,
        "mounted": 1_000_000,
        "phone_beams": 40_000.0,
        "payload": 1.4e10,
        "access": 2_280_000.0,
        "tone": 2.8e7,
    },
    2033: {
        "living_fleet": 1_500,
        "annual_cost_musd": 600.0,
        "small": 12_000_000,
        "mounted": 1_500_000,
        "phone_beams": 60_000.0,
        "payload": 2.1e10,
        "access": 3_420_000.0,
        "tone": 4.2e7,
    },
}
"""The synthetic artifact's years, round numbers: each year's living fleet, its annual cost ($M),
the small and mounted terminals' whole-fleet people, the phone class's useful beams and IoT's
three rooms (payload bits, access attempts at 57 a beam and tone-seconds, each a second). FY2030
is below the floor: no people, as the engineering model sells nothing there, its room still
published."""


def synthetic_engineering_artifact() -> dict[str, Any]:
    """A synthetic ``iridium-v7`` engineering artifact of round numbers, as a fresh mapping.

    It holds only the fields the product case reads (the reader ignores every other field):
    the provenance, the coverage floor year (FY2031), the message's and burst's sizes and the
    airtime's high end, the three classes' pools (the small terminal 10 Mbps a beam at 2 Mbps
    and 2.5 percent busy, 200 people a beam; the mounted terminal 12.5 at 5 Mbps and 10
    percent, 25 a beam; the phone class's, unread), and the years FY2030 to FY2033
    (:data:`SYNTHETIC_YEARS`).

    Returns:
        The artifact's mapping, which a test may change before writing it.
    """
    years = []
    for year, row in SYNTHETIC_YEARS.items():
        years.append(
            {
                "year": year,
                "living_fleet": row["living_fleet"],
                "annual_cost_musd": row["annual_cost_musd"],
                "classes": [
                    {
                        "device_class": "small_terminal_class",
                        "people_served": row["small"],
                        "useful_beams": row["phone_beams"],
                    },
                    {
                        "device_class": "mounted_terminal_class",
                        "people_served": row["mounted"],
                        "useful_beams": row["phone_beams"],
                    },
                    {
                        "device_class": "phone_class",
                        "people_served": 0,
                        "useful_beams": row["phone_beams"],
                    },
                ],
                "iot": {
                    "uplink_payload_bits_per_second": row["payload"],
                    "access_attempts_per_second_low": row["access"],
                    "single_tone_seconds_per_second": row["tone"],
                },
            }
        )
    return {
        "provenance": {
            "model_name": "iridium",
            "schema_version": "iridium-v7",
            "scenario_name": "a synthetic engineering run",
            "version_stamp": SYNTHETIC_STAMP,
        },
        "trajectory_summary": {"coverage_floor_reached_year": SYNTHETIC_FLOOR_YEAR},
        "iridium_physics": {
            "iot_message_bytes": 340,
            "iot_burst_bytes": 100_000,
            "iot_message_airtime_high_s": 7.0,
        },
        "classes": [
            {
                "device_class": "small_terminal_class",
                "beam_pool_mbps": 10.0,
                "active_user_rate_mbps": 2.0,
                "concurrency_peak": 0.025,
            },
            {
                "device_class": "mounted_terminal_class",
                "beam_pool_mbps": 12.5,
                "active_user_rate_mbps": 5.0,
                "concurrency_peak": 0.1,
            },
            {
                "device_class": "phone_class",
                "beam_pool_mbps": 3.25,
                "active_user_rate_mbps": 0.75,
                "concurrency_peak": 0.025,
            },
        ],
        "years": years,
    }


def engineering_bytes(artifact: dict[str, Any]) -> bytes:
    """An engineering artifact mapping as the JSON bytes the command would read."""
    return json.dumps(artifact, indent=2).encode("utf-8")


@pytest.fixture(scope="session")
def product_case_yaml(scenarios_dir: Path) -> Path:
    """The shipped product-case scenario, ``code/scenarios/product_case.yaml``."""
    return scenarios_dir / "product_case.yaml"


@pytest.fixture
def shipped_scenario(product_case_yaml: Path) -> dict[str, Any]:
    """The shipped scenario as a fresh mapping (a deep copy a test may change)."""
    return copy.deepcopy(load_yaml_mapping(product_case_yaml))


@pytest.fixture
def write_scenario(tmp_path: Path) -> ScenarioWriter:
    """A writer of scenario mappings to YAML files in the test's temporary folder."""
    written: list[Path] = []

    def write(data: dict[str, Any]) -> Path:
        path = tmp_path / f"scenario_{len(written)}.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        written.append(path)
        return path

    return write


@pytest.fixture
def synthetic_engineering() -> dict[str, Any]:
    """The synthetic engineering artifact as a fresh mapping a test may change."""
    return synthetic_engineering_artifact()


@pytest.fixture(scope="session")
def synthetic_years() -> dict[int, dict[str, int | float]]:
    """The synthetic artifact's years as a table (a copy): what each year's fields hold."""
    return copy.deepcopy(SYNTHETIC_YEARS)


@pytest.fixture(scope="session")
def synthetic_reported_years() -> tuple[int, ...]:
    """The synthetic artifact's reported years, FY2031 to FY2033."""
    return SYNTHETIC_REPORTED_YEARS


@pytest.fixture(scope="session")
def synthetic_stamp() -> str:
    """The synthetic artifact's version stamp."""
    return SYNTHETIC_STAMP


@pytest.fixture(scope="session")
def as_engineering_bytes() -> Callable[[dict[str, Any]], bytes]:
    """The function that turns an engineering artifact mapping into the JSON bytes it reads as."""
    return engineering_bytes


@pytest.fixture
def write_engineering(tmp_path: Path) -> EngineeringWriter:
    """A writer of engineering artifact mappings to JSON files in the test's temporary folder."""
    written: list[Path] = []

    def write(artifact: dict[str, Any]) -> Path:
        path = tmp_path / f"engineering_{len(written)}.json"
        path.write_bytes(engineering_bytes(artifact))
        written.append(path)
        return path

    return write
