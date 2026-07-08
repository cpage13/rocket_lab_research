"""Architecture guard: the comms src must not import the data_center venture (T1.10).

The comms package may depend on common (the shared spine), but not on the DC
venture. The data_center check is IMPORT-based (an AST scan), not a raw-substring
scan, because comms docstrings legitimately name the data-center model in prose
(this package mirrors it); a prose mention is not a dependency, an ``import`` of the
venture would be (the same rationale as the Phase 0 common/ guard, finding
F-P0-EXEC-4). It also locks the config-time disaster tokens (starship, capture or
market share, market-size or demand-lever machinery) out of the comms src and the
default YAML; those ARE raw-substring scans because the tokens must never appear at
all, so a regression is caught early in CI.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

# The comms src directory and the default comms scenario (the Iridium scenario,
# scenarios/iridium.yaml), repo-anchored from this file.
_REPO_CODE = Path(__file__).resolve().parents[2]
_COMMS_SRC = _REPO_CODE / "src" / "communications"
_DEFAULT_YAML = _REPO_CODE / "scenarios" / "iridium.yaml"

_COMMS_SRC_FILES = sorted(_COMMS_SRC.glob("*.py"))

# The forbidden config-time tokens (case-insensitive). The verdict/conclusion
# token set guards the OUTPUT JSON (a Phase-5 deliverable that does not exist
# yet) and is intentionally not enforced here.
_FORBIDDEN_TOKENS = [
    "starship",
    "capture_share",
    "share_pct",
    "market_share",
    "market_size",
    "market_growth",
    "compute_market_size",
    "adoption",
    "take_rate",
    "uptake",
]


def _imported_modules(source: str) -> set[str]:
    """Return the top-level module names imported by ``source`` (AST-based)."""
    tree = ast.parse(source)
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module is not None and node.level == 0:
            modules.add(node.module.split(".")[0])
    return modules


@pytest.mark.parametrize("src_file", _COMMS_SRC_FILES, ids=lambda p: p.name)
def test_comms_src_does_not_import_data_center(src_file: Path) -> None:
    """No comms src file IMPORTS the data_center venture (prose mentions are allowed)."""
    assert "data_center" not in _imported_modules(src_file.read_text()), (
        f"{src_file.name} imports data_center"
    )


@pytest.mark.parametrize("token", _FORBIDDEN_TOKENS)
def test_no_forbidden_token_in_comms_src(token: str) -> None:
    """No forbidden capture-share / market-size / demand-lever token appears in comms src.

    Prose comments stating demand is assumed are allowed to mention 'demand'
    itself, but the specific machinery tokens above must not appear at all (they
    are field names, function names, or YAML keys when present).
    """
    pattern = re.compile(token, re.IGNORECASE)
    for src_file in _COMMS_SRC_FILES:
        assert not pattern.search(src_file.read_text()), f"{token} found in {src_file.name}"


@pytest.mark.parametrize("token", _FORBIDDEN_TOKENS)
def test_no_forbidden_token_in_default_yaml(token: str) -> None:
    """No forbidden token appears in the default comms scenario YAML (iridium.yaml)."""
    pattern = re.compile(token, re.IGNORECASE)
    assert not pattern.search(_DEFAULT_YAML.read_text()), f"{token} found in iridium.yaml"


def test_comms_src_files_discovered() -> None:
    # Guard against the glob silently matching nothing (which would make the
    # parametrized tests vacuously pass).
    names = {p.name for p in _COMMS_SRC_FILES}
    assert {"__init__.py", "config.py", "constants.py"} <= names
