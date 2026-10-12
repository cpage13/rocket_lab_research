"""Every claim ID the communications code cites has its row in the source ledger.

The code cites research by claim ID (``COMM-<n>``) in its docstrings, field descriptions and
stated assumptions, and the source ledger, ``research/SOURCE_INDEX.md``, holds one row per claim
ID (its first cell the ID). A cited ID with no row is a citation no reader can trace, against the
charter's Objective 2 (every published number traced to a claim ID).
"""

from __future__ import annotations

import re
from pathlib import Path

CITED_CLAIM_ID = re.compile(r"\bCOMM-\d+\b")
"""A communications claim ID as the code cites it (a range such as ``COMM-386..COMM-405`` is read
as its two ends)."""

LEDGER_ROW_ID = re.compile(r"^\| *`(COMM-\d+)` *\|", re.MULTILINE)
"""A source-ledger table row whose first cell is a communications claim ID, in backticks."""


def test_every_comm_claim_id_the_communications_code_cites_has_a_ledger_row(
    code_dir: Path, repo_dir: Path
) -> None:
    """Objective: every ``COMM-`` claim ID cited anywhere under ``code/src/communications/``
    resolves to a row of the source ledger, so a citation added without its row, or a row
    renumbered away from its citations, fails here.

    Sample: every Python file under ``code/src/communications/``; the ledger's rows.

    Expected outcome: the files and the ledger are found and non-empty (so the check cannot pass
    on nothing: the code cites dozens of IDs and the ledger holds hundreds of rows), and no cited
    ID lacks a row; a failure names each missing ID and the files citing it.
    """
    sources = sorted((code_dir / "src" / "communications").glob("*.py"))
    assert sources, "no communications source file found"
    cited: dict[str, list[str]] = {}
    for source in sources:
        for claim_id in CITED_CLAIM_ID.findall(source.read_text(encoding="utf-8")):
            cited.setdefault(claim_id, []).append(source.name)
    rows = set(
        LEDGER_ROW_ID.findall((repo_dir / "research" / "SOURCE_INDEX.md").read_text("utf-8"))
    )
    assert len(cited) > 10, sorted(cited)
    assert len(rows) > 100, len(rows)
    missing = {
        claim_id: sorted(set(files)) for claim_id, files in cited.items() if claim_id not in rows
    }
    assert missing == {}, missing
