"""Every claim ID the product case cites has its row in the source ledger.

The product case cites research by claim ID (``COMM-<n>``) in its docstrings, cell specs and
stated lines, and its scenario cites the rows behind each value; the source ledger,
``research/SOURCE_INDEX.md``, holds one row per claim ID (its first cell the ID). A cited ID with
no row is a citation no reader can trace, against the charter's Objective 2. The communications
code's own test (``code/tests/communications/test_claim_citations.py``) is the pattern.
"""

from __future__ import annotations

import re
from pathlib import Path

CITED_CLAIM_ID = re.compile(r"\bCOMM-\d+\b")
"""A communications claim ID as the product case cites it."""

LEDGER_ROW_ID = re.compile(r"^\| *`(COMM-\d+)` *\|", re.MULTILINE)
"""A source-ledger table row whose first cell is a communications claim ID, in backticks."""

PRODUCT_CASE_ROWS = frozenset({"COMM-722", "COMM-723", "COMM-724", "COMM-725", "COMM-726"})
"""The five rows written for the product case (its prices, the Monte Carlo's settings, the usage
paths, the usable floors and data IoT's anchor), which its code and scenario cite."""


def test_every_comm_claim_id_the_product_case_cites_has_a_ledger_row(
    code_dir: Path, repo_dir: Path
) -> None:
    """Objective: every ``COMM-`` claim ID cited anywhere in the product case's package or its
    shipped scenario resolves to a row of the source ledger, so a citation added without its
    row, or a row renumbered away from its citations, fails here.

    Sample: every Python file under ``code/src/product_case/`` and
    ``code/scenarios/product_case.yaml``; the ledger's rows.

    Expected outcome: the files and the ledger are found and non-empty (so the check cannot pass
    on nothing: the package cites its five rows and Iridium's customers and ARPU today, and the
    ledger holds hundreds of rows); the five product-case rows are among the IDs cited; no cited
    ID lacks a row, and a failure names each missing ID and the files citing it.
    """
    sources = sorted((code_dir / "src" / "product_case").glob("*.py"))
    assert sources, "no product-case source file found"
    sources.append(code_dir / "scenarios" / "product_case.yaml")
    cited: dict[str, list[str]] = {}
    for source in sources:
        text = source.read_text(encoding="utf-8")
        assert text.strip(), f"{source.name} is empty"
        for claim_id in CITED_CLAIM_ID.findall(text):
            cited.setdefault(claim_id, []).append(source.name)
    rows = set(
        LEDGER_ROW_ID.findall((repo_dir / "research" / "SOURCE_INDEX.md").read_text("utf-8"))
    )
    assert set(cited) >= PRODUCT_CASE_ROWS, sorted(cited)
    assert set(cited) >= {"COMM-617", "COMM-618"}, sorted(cited)
    assert len(rows) > 100, len(rows)
    missing = {
        claim_id: sorted(set(files)) for claim_id, files in cited.items() if claim_id not in rows
    }
    assert missing == {}, missing
