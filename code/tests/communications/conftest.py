"""Shared fixtures for the communications test suite (clean-rewrite, slim).

This conftest is the slim rewrite version: it provides the default ``CommsConfig``
fixture, built purely on the rewritten ``communications.config``, and the Iridium
scenario and artifact paths (from the repository-anchored fixtures in
``tests/conftest.py``, never the working directory).
The pre-rewrite old tree (its src modules, test files, and scenario YAML) was
retired in the investor-directed 2026-07-07 alignment cleanup, so the whole
``tests/communications/`` directory now collects and runs cleanly. The live suite
covers the High-Bandwidth Cellular Pure Play model (formerly Model A), the Iridium
model (formerly Model B), the ground comparison, and the cross-import guard.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from communications.config import CommsConfig


@pytest.fixture
def default_comms_config() -> CommsConfig:
    """Return the default (central-case) comms config."""
    return CommsConfig()


@pytest.fixture(scope="session")
def iridium_yaml(scenarios_dir: Path) -> Path:
    """The promoted Iridium scenario, ``scenarios/iridium.yaml``."""
    return scenarios_dir / "iridium.yaml"


@pytest.fixture(scope="session")
def iridium_saturation_yaml(scenarios_dir: Path) -> Path:
    """The saturation companion scenario, ``scenarios/iridium_saturation.yaml``."""
    return scenarios_dir / "iridium_saturation.yaml"


@pytest.fixture(scope="session")
def promoted_iridium_artifact(repo_dir: Path) -> Path:
    """The committed promoted artifact, ``communications/models/iridium/default.json``."""
    return repo_dir / "communications" / "models" / "iridium" / "default.json"
