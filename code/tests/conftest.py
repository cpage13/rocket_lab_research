"""Repository-anchored paths shared by every test package.

Each path is anchored to this file, never to the working directory, so the
suite passes from ``code/`` (``uv run pytest``) and from the repository root
(``uv run --project code pytest code/tests``). Test modules take these
fixtures instead of re-deriving the anchor themselves.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_CODE_DIR = Path(__file__).resolve().parents[1]
"""The repository's ``code/`` directory (this file lives in ``code/tests/``)."""


@pytest.fixture(scope="session")
def code_dir() -> Path:
    """The repository's ``code/`` directory."""
    return _CODE_DIR


@pytest.fixture(scope="session")
def repo_dir() -> Path:
    """The repository root, the parent of ``code/``."""
    return _CODE_DIR.parent


@pytest.fixture(scope="session")
def scenarios_dir() -> Path:
    """The bundled scenario YAML files, ``code/scenarios/``."""
    return _CODE_DIR / "scenarios"
