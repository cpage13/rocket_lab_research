"""Architecture guard: the product case imports ``common`` alone; only its Monte Carlo uses numpy.

The product case is its own model on the engineering artifact (ADR 012): it reads the promoted
JSON, never the engineering code, so no module of ``code/src/product_case/`` imports
``communications`` or ``data_center``; of the repository's packages it imports ``common`` and
itself alone. numpy is a runtime dependency confined to two modules (ADR 010 as ADR 012 widens
it): the saturation module and the product case's Monte Carlo, ``monte_carlo.py``, so no other
product-case module imports it. The checks read each module's imports from its syntax tree (a
prose mention of another package is not a dependency), and the file list is checked so the
parametrized tests cannot pass on nothing.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

_PRODUCT_CASE_SRC = Path(__file__).resolve().parents[2] / "src" / "product_case"
"""The product case's package, anchored from this file because the parametrized tests list its
modules at collection time, before any fixture exists."""

_PRODUCT_CASE_FILES = sorted(_PRODUCT_CASE_SRC.glob("*.py"))
"""Every module of the product case's package."""

_REPOSITORY_PACKAGES = frozenset({"common", "communications", "data_center", "product_case"})
"""The repository's own top-level packages under ``code/src/``."""

_ALLOWED_PACKAGES = frozenset({"common", "product_case"})
"""The repository packages a product-case module may import."""

_NUMPY_MODULE = "monte_carlo.py"
"""The one product-case module allowed to import numpy."""


def _imported_top_levels(source: str) -> set[str]:
    """The top-level names a module imports, absolute imports only (a relative import stays in
    the package)."""
    tree = ast.parse(source)
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None and node.level == 0:
            names.add(node.module.split(".")[0])
    return names


@pytest.mark.parametrize("module", _PRODUCT_CASE_FILES, ids=lambda path: path.name)
def test_the_product_case_imports_common_alone(module: Path) -> None:
    """Objective: no product-case module imports ``communications`` or ``data_center``; of the
    repository's packages it imports ``common`` and the product case alone (ADR 012).

    Sample: each module of ``code/src/product_case/``, its imports read from its syntax tree.

    Expected outcome: the repository packages it imports are among ``common`` and
    ``product_case``.
    """
    imported = _imported_top_levels(module.read_text(encoding="utf-8")) & _REPOSITORY_PACKAGES
    assert imported <= _ALLOWED_PACKAGES, f"{module.name} imports {sorted(imported)}"


@pytest.mark.parametrize(
    "module",
    [path for path in _PRODUCT_CASE_FILES if path.name != _NUMPY_MODULE],
    ids=lambda path: path.name,
)
def test_only_the_monte_carlo_imports_numpy(module: Path) -> None:
    """Objective: numpy enters the product case through its Monte Carlo alone (ADR 010 as ADR 012
    widens it); every other module is numpy-free.

    Sample: each module of ``code/src/product_case/`` but ``monte_carlo.py``.

    Expected outcome: the module imports no numpy.
    """
    assert "numpy" not in _imported_top_levels(module.read_text(encoding="utf-8")), module.name


def test_the_product_case_modules_are_found() -> None:
    """Objective: the guards above read the package's modules, so they cannot pass on nothing.

    Sample: the modules the glob finds.

    Expected outcome: the package's docstring module and the B-I modules are among them.
    """
    names = {path.name for path in _PRODUCT_CASE_FILES}
    assert {"__init__.py", "constants.py", "config.py", "engineering.py", "offers.py"} <= names
