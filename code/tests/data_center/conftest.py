"""Shared fixtures for the data-center test suite.

Paths come from the repository-anchored fixtures in ``tests/conftest.py``
(``scenarios_dir``, ``repo_dir``), never from the working directory.

``default_output`` is the canonical default run, built once per session exactly
as ``rklb-value scenarios/default.yaml --json`` builds it: a draft run of
``code/scenarios/default.yaml`` recorded under that repository path (so it is
the default scenario, ``inputs.scenario.is_default``). Tests that only read the
default run share it instead of re-running the model. Outputs are frozen
pydantic models and the tests derive variants with ``model_copy``, so sharing
cannot leak a mutation between tests.

``ledger_statuses`` is the ``research/SOURCE_INDEX.md`` claim ledger read once
per session: every claim row's ID and source status, so citation tests check
the artifacts against the ledger itself.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from common.input_manifest import SourceStatus
from data_center.config import load_config
from data_center.engine import run_valuation
from data_center.input_manifest import DEFAULT_SCENARIO_PATH
from data_center.output import SpaceModelOutput

_LEDGER_ROW = re.compile(
    r"^\| `(?P<claim>[A-Z]+-[A-Za-z0-9_-]+)` \| .*? \| `(?P<status>"
    + "|".join(status.value for status in SourceStatus)
    + r")` \|"
)
"""One claim row of a ``research/SOURCE_INDEX.md`` ledger table: the claim ID
(first column) and its source status (third column)."""


@pytest.fixture(scope="session")
def default_output(scenarios_dir: Path) -> SpaceModelOutput:
    """The default scenario's run, as ``rklb-value scenarios/default.yaml --json`` builds it."""
    return run_valuation(
        load_config(scenarios_dir / "default.yaml"), source_scenario_path=DEFAULT_SCENARIO_PATH
    )


@pytest.fixture(scope="session")
def ledger_statuses(repo_dir: Path) -> dict[str, SourceStatus]:
    """Every claim's source status as the ``research/SOURCE_INDEX.md`` ledger records it."""
    ledger = (repo_dir / "research" / "SOURCE_INDEX.md").read_text(encoding="utf-8")
    rows = (_LEDGER_ROW.match(line) for line in ledger.splitlines())
    return {row["claim"]: SourceStatus(row["status"]) for row in rows if row is not None}
