"""Repository guard: the writing convention's ban on em-dashes (U+2014).

``AGENTS.md`` sets a repository-wide writing convention: no em-dash anywhere,
use a comma, a colon, parentheses, or a new sentence instead. This module is
the executable form of that convention for the files it has been swept over,
so an em-dash cannot quietly return to the code, the scenarios, the promoted
artifacts, the public documents, or the repository's configuration files.

Coverage (paths relative to the repository root):

* every file under ``code/src/``, ``code/tests/``, and ``code/scenarios/``.
  Every tracked file there is covered; the walk skips only ``__pycache__``
  bytecode caches, which git ignores;
* ``code/README.md``, ``code/CHANGELOG.md``, and ``code/pyproject.toml``;
* the three promoted JSON artifacts: ``data_center/models/space/default.json``,
  ``data_center/models/ground/default.json``, and
  ``communications/models/iridium/default.json``;
* the root ``README.md``, ``AGENTS.md``, ``CONTEXT.md``,
  ``rocket_lab_primer.md``, and ``.gitignore``;
* every ``*.md`` under ``docs/``, ``data_center/``, and ``communications/``;
* the research front door ``research/README.md`` and the research ledgers
  ``research/SOURCE_INDEX.md``, ``research/LIBRARY.md``, and
  ``research/RESEARCH_TRACKER.md``.

The rest of ``research/`` is excluded on purpose (see
:data:`_RESEARCH_FILES`). The em-dash is built from its code point, so this
file itself contains none.
"""

from __future__ import annotations

from pathlib import Path

EM_DASH_CODE_POINT = 0x2014
"""Unicode code point of the em-dash."""

EM_DASH = chr(EM_DASH_CODE_POINT)
"""The em-dash, built from its code point so this file holds none."""

_EM_DASH_UTF8 = EM_DASH.encode("utf-8")
"""The em-dash's UTF-8 bytes, searched for before any file is decoded."""

_WALKED_CODE_DIRS = ("src", "tests")
"""Directories under ``code/`` whose every file is covered (``scenarios/`` comes
from the shared ``scenarios_dir`` fixture)."""

_SKIPPED_DIR_NAME = "__pycache__"
"""The one directory name the walk skips: git-ignored bytecode caches."""

_CODE_FILES = ("README.md", "CHANGELOG.md", "pyproject.toml")
"""Files directly under ``code/``: its two documents and the package configuration."""

_PROMOTED_ARTIFACTS = (
    "data_center/models/space/default.json",
    "data_center/models/ground/default.json",
    "communications/models/iridium/default.json",
)
"""The three promoted JSON artifacts, repository-relative."""

_ROOT_FILES = ("README.md", "AGENTS.md", "CONTEXT.md", "rocket_lab_primer.md", ".gitignore")
"""Files at the repository root: its documents and the git ignore rules."""

_MARKDOWN_TREES = ("docs", "data_center", "communications")
"""Repository directories whose every ``*.md`` (at any depth) is covered."""

_RESEARCH_FILES = (
    "research/README.md",
    "research/SOURCE_INDEX.md",
    "research/LIBRARY.md",
    "research/RESEARCH_TRACKER.md",
)
"""The only ``research/`` files covered: the wiki's front door and its three ledgers.

Every other file under ``research/`` is deliberately excluded: those are the
legacy research write-ups, whose em-dashes predate the convention, and
sweeping them is a pending investor decision. Add them here once that decision
is made.
"""


def _walk(root: Path) -> list[Path]:
    """Return every file under ``root``, skipping ``__pycache__`` directories."""
    return [
        path
        for path in root.rglob("*")
        if path.is_file() and _SKIPPED_DIR_NAME not in path.relative_to(root).parts
    ]


def _em_dash_lines(path: Path, repo_dir: Path) -> list[str]:
    """Return one ``file:line`` entry per line of ``path`` that holds an em-dash."""
    data = path.read_bytes()
    if _EM_DASH_UTF8 not in data:
        return []
    where = path.relative_to(repo_dir).as_posix()
    lines = data.decode("utf-8", errors="replace").splitlines()
    return [
        f"{where}:{number}: {line.count(EM_DASH)} em-dash(es)"
        for number, line in enumerate(lines, start=1)
        if EM_DASH in line
    ]


def test_no_em_dash_in_swept_files(repo_dir: Path, code_dir: Path, scenarios_dir: Path) -> None:
    """Objective: the swept files hold no em-dash (U+2014), as ``AGENTS.md`` requires.

    Expected outcome: every named file and every walked tree exists (so the
    guard cannot pass vacuously), and no covered file contains an em-dash. On
    failure the message lists each offending ``file:line`` so the dash can be
    replaced with a comma, a colon, parentheses, or a new sentence.
    """
    walked_roots = [code_dir / name for name in _WALKED_CODE_DIRS] + [scenarios_dir]
    named = (
        [code_dir / name for name in _CODE_FILES]
        + [repo_dir / name for name in _PROMOTED_ARTIFACTS]
        + [repo_dir / name for name in _ROOT_FILES]
        + [repo_dir / name for name in _RESEARCH_FILES]
    )
    markdown_roots = [repo_dir / name for name in _MARKDOWN_TREES]

    missing = [p for p in named if not p.is_file()]
    missing += [p for p in walked_roots + markdown_roots if not p.is_dir()]
    assert not missing, f"guard coverage names paths that do not exist: {missing}"

    covered: set[Path] = set(named)
    for root in walked_roots:
        files = _walk(root)
        assert files, f"no files found under {root}"
        covered.update(files)
    for root in markdown_roots:
        documents = list(root.rglob("*.md"))
        assert documents, f"no *.md files found under {root}"
        covered.update(documents)

    offenders = [entry for path in sorted(covered) for entry in _em_dash_lines(path, repo_dir)]
    assert not offenders, (
        f"{len(offenders)} line(s) hold an em-dash (U+2014), banned by AGENTS.md. "
        "Use a comma, a colon, parentheses, or a new sentence:\n" + "\n".join(offenders)
    )
