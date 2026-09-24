"""Shared fixtures for the data-center test suite.

Paths come from the repository-anchored fixtures in ``tests/conftest.py``
(``scenarios_dir``), never from the working directory.

``default_output`` is the canonical default run, built once per session exactly
as ``rklb-value scenarios/default.yaml --json`` builds it: a draft run of
``code/scenarios/default.yaml`` recorded under that repository path (so it is
the default scenario, ``inputs.scenario.is_default``). Tests that only read the
default run share it instead of re-running the model. Outputs are frozen
pydantic models and the tests derive variants with ``model_copy``, so sharing
cannot leak a mutation between tests.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from data_center.config import load_config
from data_center.engine import run_valuation
from data_center.input_manifest import DEFAULT_SCENARIO_PATH
from data_center.output import SpaceModelOutput


@pytest.fixture(scope="session")
def default_output(scenarios_dir: Path) -> SpaceModelOutput:
    """The default scenario's run, as ``rklb-value scenarios/default.yaml --json`` builds it."""
    return run_valuation(
        load_config(scenarios_dir / "default.yaml"), source_scenario_path=DEFAULT_SCENARIO_PATH
    )
