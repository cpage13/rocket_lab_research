"""Shared fixtures for the communications test suite (clean-rewrite, slim).

This conftest is the slim rewrite version: it provides ONLY the default
``CommsConfig`` fixture, built purely on the rewritten ``communications.config``.
The old conftest imported the whole old pipeline (``engine``, ``ground``,
``json_output``, ``output``, plus the cut ``price_reference`` block), which the
clean rewrite supersedes; importing those at conftest load broke collection of the
new tests once ``config.py`` / ``constants.py`` were rewritten (the old modules
import names the slim config no longer defines).

Per the plan's Phase 8a remedy (write a new slim conftest for the rewrite so the
new tests collect and run cleanly), this trims the conftest to the rewrite's
needs. The superseded old comms test files are retired/quarantined only in the
SEPARATE, founder-gated Phase 8b/8a step (not here, not mid-build); until then
they may fail at their own imports, which is expected. Later phases add fixtures
for the engine output and the ground interface as those modules land.
"""

from __future__ import annotations

import pytest

from communications.config import CommsConfig


@pytest.fixture
def default_comms_config() -> CommsConfig:
    """Return the default (central-case) comms config."""
    return CommsConfig()
