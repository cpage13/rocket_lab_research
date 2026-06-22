"""Architecture guard: ``common`` must not depend on either venture (Phase 0, T0.15).

The binding invariant is that no ``common`` module IMPORTS the ``data_center`` or
``communications`` package. The check is import-based rather than a raw-substring
scan because the package docstrings legitimately name both ventures in prose
(e.g. ``common/__init__.py``: "Shared code imported by both the data_center and
communications models"), and ``common/cadence.py`` documents in a comment that its
eight cadence defaults are copied from ``data_center/constants.py``. Those prose
mentions are not dependencies; an ``import`` of a venture would be. See the Phase 0
report for the deviation rationale.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

_COMMON_DIR = Path(__file__).resolve().parents[2] / "src" / "common"
_COMMON_FILES = sorted(_COMMON_DIR.glob("*.py"))


def _imported_modules(source: str) -> set[str]:
    """Return the top-level module names imported by ``source``."""
    tree = ast.parse(source)
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module is not None and node.level == 0:
            modules.add(node.module.split(".")[0])
    return modules


@pytest.mark.parametrize("path", _COMMON_FILES, ids=lambda p: p.name)
def test_common_modules_do_not_import_data_center(path: Path) -> None:
    assert "data_center" not in _imported_modules(path.read_text())


@pytest.mark.parametrize("path", _COMMON_FILES, ids=lambda p: p.name)
def test_common_modules_do_not_import_communications(path: Path) -> None:
    assert "communications" not in _imported_modules(path.read_text())


def test_common_files_discovered() -> None:
    # Guard against the glob silently matching nothing (which would make the
    # parametrized tests vacuously pass).
    names = {p.name for p in _COMMON_FILES}
    assert {"provenance.py", "input_manifest.py", "cadence.py", "cohort.py", "meta.py"} <= names
