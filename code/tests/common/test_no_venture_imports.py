"""Architecture guard: ``common`` must not depend on a model package (Phase 0, T0.15).

The binding invariant is that no ``common`` module IMPORTS the ``data_center``,
``communications`` or ``product_case`` package. The check is import-based rather
than a raw-substring scan because the package docstrings legitimately name the
models in prose (``common/__init__.py`` names the models it serves,
``common/cadence.py`` documents that its dial blocks are the ``cadence`` and
``launch_cost`` blocks of both ventures' configs, and ``common/input_manifest.py``
and ``common/meta.py`` name the product case among their users). Those prose
mentions are not dependencies; an ``import`` of a model package would be. See the
Phase 0 report for the deviation rationale.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

# Anchored from this file (not the shared ``code_dir`` fixture) because the
# parametrized guards below list the files at collection time, before any
# fixture exists.
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


@pytest.mark.parametrize("path", _COMMON_FILES, ids=lambda p: p.name)
def test_common_modules_do_not_import_the_product_case(path: Path) -> None:
    assert "product_case" not in _imported_modules(path.read_text())


def test_common_files_discovered() -> None:
    # Guard against the glob silently matching nothing (which would make the
    # parametrized tests vacuously pass).
    names = {p.name for p in _COMMON_FILES}
    assert {"provenance.py", "input_manifest.py", "cadence.py", "cohort.py", "meta.py"} <= names
