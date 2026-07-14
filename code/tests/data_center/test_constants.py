"""Verify every Final constant in constants.py has a provenance docstring."""

from __future__ import annotations

import ast
from pathlib import Path

CONSTANTS_FILE = Path(__file__).parent.parent.parent / "src" / "data_center" / "constants.py"
REQUIRED_TOKENS = (
    "SOURCED_FACT",
    "ESTIMATE",
    "EXTRAPOLATION",
    "SOURCED_DECISION",
    "SOURCED",
    "INVESTOR_SET",
)


def _final_assignments() -> list[tuple[str, str | None]]:
    """Return list of (name, docstring) for every Final[...] assignment."""
    tree = ast.parse(CONSTANTS_FILE.read_text())
    result: list[tuple[str, str | None]] = []
    body = tree.body
    for i, node in enumerate(body):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            ann = ast.unparse(node.annotation)
            if "Final[" in ann:
                name = node.target.id
                # docstring is the next node if it's an Expr with a Str
                doc: str | None = None
                if i + 1 < len(body):
                    nxt = body[i + 1]
                    if (
                        isinstance(nxt, ast.Expr)
                        and isinstance(nxt.value, ast.Constant)
                        and isinstance(nxt.value.value, str)
                    ):
                        doc = nxt.value.value
                result.append((name, doc))
    return result


def test_every_final_has_docstring() -> None:
    for name, doc in _final_assignments():
        assert doc is not None, f"{name}: missing docstring"


def test_every_final_docstring_has_source_class() -> None:
    for name, doc in _final_assignments():
        assert doc is not None
        assert any(tok in doc for tok in REQUIRED_TOKENS), (
            f"{name}: docstring missing source class token (one of {REQUIRED_TOKENS})"
        )
