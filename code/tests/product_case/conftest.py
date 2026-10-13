"""Fixtures shared by the product case's tests.

The shipped scenario (``code/scenarios/product_case.yaml``) as a path and as a fresh mapping a
test may change, and a writer that puts a changed scenario in a temporary folder, so a test
loads it through the real loader (``load_product_case_config``). Every path is anchored to the
root ``conftest.py``'s fixtures, never to the working directory, so the suite runs from
``code/`` and from the repository root.
"""

from __future__ import annotations

import copy
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
import yaml

from common.file_io import load_yaml_mapping

type ScenarioWriter = Callable[[dict[str, Any]], Path]
"""Writes a scenario mapping to a temporary YAML file and returns its path."""


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
