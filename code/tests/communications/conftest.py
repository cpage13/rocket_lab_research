"""Shared fixtures for the communications test suite (clean-rewrite, slim).

This conftest is the slim rewrite version: it provides ONLY the default
``CommsConfig`` fixture, built purely on the rewritten ``communications.config``.
The pre-rewrite old tree (its src modules, test files, and scenario YAML) was
retired in the founder-directed 2026-07-07 alignment cleanup, so the whole
``tests/communications/`` directory now collects and runs cleanly. The live suite
covers the High-Bandwidth Cellular Pure Play model (formerly Model A), the Iridium
model (formerly Model B), the ground comparison, and the cross-import guard.
"""

from __future__ import annotations

import pytest

from communications.config import CommsConfig


@pytest.fixture
def default_comms_config() -> CommsConfig:
    """Return the default (central-case) comms config."""
    return CommsConfig()
