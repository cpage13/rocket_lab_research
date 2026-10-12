"""Repository guard: every path and name the pages agents ground in spell resolves on the tree.

The documents guard forge-atlas recommends, the executable form of the atlas's first rule
("a page may be a sketch, but it states nothing untrue"). The pages are the ones an agent
grounds in: the charter ``AGENTS.md``, ``CLAUDE.md``, the glossary ``CONTEXT.md``,
``atlas/map.md`` and every page under ``atlas/``, and every ADR in ``docs/adr/``.

What it checks, on every line of every page:

* a Markdown link's target resolves from the page's folder (a web link is not looked up), and
  each ``@`` import in ``CLAUDE.md`` names a file at the repository root;
* every backticked span, word by word when it holds a command:

  - a path or a file name resolves: from the repository root, from ``code/`` (where the
    commands run) or from the page's folder; a bare file name anywhere in the repository; a
    glob matches at least one file. A ``.agent/`` path is the investor's local working record,
    absent from a fresh clone, so it is not looked up: its line must carry the mark
    ``(local)`` instead. An absolute path, and a command's output after ``tee``, are not
    looked up;
  - a module path (``communications.saturation``, ``common.file_io.load_yaml_mapping``, the
    word after ``-m``) names a module under ``code/src/`` and then a name that module defines
    at its top level;
  - a test name (``test_...``) is a test function defined under ``code/tests/``;
  - a claim ID (``COMM-601``) is a row of ``research/SOURCE_INDEX.md``;
  - any other code name (``run_iridium_model``, ``fixed_books``,
    ``comms_cadence.share_of_fleet``) occurs, each dotted part, as a word in the code
    (``code/src/``), the scenarios or the four promoted JSON artifacts.

What counts as success: no span fails, and every page and source the guard reads exists, so
it cannot pass vacuously. On failure the message lists each ``page:line``, the span and why.

What it misses: a name that exists but is placed wrongly (a field said to live in the wrong
artifact, a dial that is an artifact field), numbers, counts and prose claims; a code name
that survives only in a comment or a docstring still resolves. The human documents (the
root ``README.md`` and the folders' documents) are not its pages.

Decided, not built: an accepted ADR may name a path or a field before the code that makes it
exists. :data:`_DECIDED_NOT_BUILT` lists each such span with the ADR that decides it; a
second test checks that each entry is still on its page and still does not resolve, so the
entry is removed in the change that builds it.
"""

from __future__ import annotations

import ast
import fnmatch
import os
import re
import shlex
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cache
from pathlib import Path

import pytest

_ROOT_PAGES = ("AGENTS.md", "CLAUDE.md", "CONTEXT.md")
"""The pages at the repository root: the charter, its loader and the glossary."""

_PAGE_TREES = ("atlas", "docs/adr")
"""Folders whose every ``*.md`` is a page: the atlas and the ADRs."""

_SOURCE_LEDGER = "research/SOURCE_INDEX.md"
"""The source ledger, whose rows the claim IDs name."""

_PROMOTED_ARTIFACTS = (
    "data_center/models/space/default.json",
    "data_center/models/ground/default.json",
    "communications/models/iridium/default.json",
    "communications/models/iridium/saturation_curve.json",
)
"""The four promoted JSON artifacts, whose keys and values are code names a page may cite."""

_SCENARIOS_DIR = "code/scenarios"
"""The scenario files, whose keys are the dials a page may cite."""

_LOCAL_DIR = ".agent"
"""The investor's local working record: never in a clone, so its paths are marked, not found."""

_LOCAL_MARK = "(local)"
"""The mark a line naming a ``.agent/`` path must carry (the atlas's rules)."""

_PACKAGES = ("common", "communications", "data_center")
"""The top-level packages under ``code/src/``; a dotted name headed by one is a module path."""

_FILE_EXTENSIONS = (
    ".md",
    ".py",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".lock",
    ".npz",
    ".txt",
    ".sh",
)
"""Extensions that make a span a file name rather than a code name."""

_COMMAND_TOOLS = frozenset(
    {"uv", "jq", "git", "pytest", "ruff", "mypy", "python", "python3", "tee", "cmp", "rm", "rmdir"}
)
"""Command-line tools a page may name in a span of its own: names, but not the code's."""

_OUTPUT_WORDS = frozenset({"tee", ">", ">>"})
"""Words after which a command's next word is the output it writes, not an input."""

_CLAIM_ID = re.compile(r"(COMM|NTR|RLDC|GPU|REV|THR)-[A-Z0-9][A-Z0-9_.-]*")
"""A claim ID of the source ledger."""

_TEST_NAME = re.compile(r"test_[A-Za-z0-9_]+")
"""A test function's name."""

_IDENTIFIER_PART = r"[A-Za-z_][A-Za-z0-9_]*(\[\*?\]|\(\))?"
"""One part of a code name: an identifier, optionally followed by ``[]``, ``[*]`` or ``()``."""

_CODE_NAME = re.compile(rf"{_IDENTIFIER_PART}(\.{_IDENTIFIER_PART})*")
"""A code name: identifier parts joined by dots."""

_CODE_NAME_GLOB = re.compile(r"[A-Za-z0-9_*]*\*[A-Za-z0-9_*]*")
"""A code-name pattern such as ``*_DEFAULT`` or ``*_SPECS``."""

_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
"""A word of the code's vocabulary."""

_LINE_SUFFIX = re.compile(r":\d+(-\d+)?$")
"""A ``:line`` or ``:line-line`` suffix after a cited file."""

_SPAN = re.compile(r"`([^`\n]+)`")
"""A backticked span on one line."""

_LINK = re.compile(r"\]\(([^)\s]+)\)")
"""A Markdown link's target."""

_IMPORT = re.compile(r"^@(\S+)$")
"""A ``CLAUDE.md`` import line."""

_SHELL_OPERATORS = re.compile(r"[<>|&;]")
"""Characters that make a command word an operator or a redirection, not a path."""

_PLACEHOLDER = re.compile(r"[<>{}]")
"""Characters that mark a placeholder in a path (``<stamp>``, ``{type}``)."""


@dataclass(frozen=True)
class DecidedNotBuilt:
    """A span an accepted ADR names before the code that makes it exists.

    Attributes:
        page: The page, repository-relative.
        span: The backticked span, exactly as written.
        decided_by: The ADR that decides it.
    """

    page: str
    span: str
    decided_by: str


_ADR_011 = "docs/adr/011-iot-is-capacity-in-the-engineering-model.md"
"""ADR 011: IoT as capacity in the engineering model."""

_ADR_012 = "docs/adr/012-product-case-is-its-own-model.md"
"""ADR 012: the product case as its own model."""

_DECIDED_NOT_BUILT: tuple[DecidedNotBuilt, ...] = (
    DecidedNotBuilt(_ADR_011, "years[].iot", "ADR 011, the Iridium artifact's IoT capacity"),
    DecidedNotBuilt(_ADR_011, "saturation.readings[].iot", "ADR 011, the readings' IoT capacity"),
    DecidedNotBuilt(_ADR_012, "code/src/product_case/", "ADR 012, the product case's package"),
)
"""Each span that names what an accepted ADR decided and no code has built yet."""


@dataclass(frozen=True)
class Failure:
    """One span that does not resolve.

    Attributes:
        page: The page, repository-relative.
        line: The line number, from 1.
        span: The span or command word.
        why: Why it does not resolve.
    """

    page: str
    line: int
    span: str
    why: str

    def __str__(self) -> str:
        """Return the failure as ``page:line: `span`: why``."""
        return f"{self.page}:{self.line}: `{self.span}`: {self.why}"


def _pages(repo_dir: Path) -> list[Path]:
    """Return every page: the root pages, then every ``*.md`` under the atlas and the ADRs."""
    pages = [repo_dir / name for name in _ROOT_PAGES]
    for tree in _PAGE_TREES:
        pages.extend(sorted((repo_dir / tree).rglob("*.md")))
    return pages


@dataclass(frozen=True)
class RepoTree:
    """What the repository holds, ``.agent``, ``.git``, environments and caches left out.

    Attributes:
        files: Every file, repository-relative.
        file_names: Every file's base name.
        folder_names: Every folder's base name (a page may name a topic folder bare).
    """

    files: frozenset[str]
    file_names: frozenset[str]
    folder_names: frozenset[str]


_SKIPPED_PARTS = frozenset(
    {_LOCAL_DIR, ".git", ".venv", "__pycache__", ".mypy_cache", ".ruff_cache", ".pytest_cache"}
)
"""Folders the tree leaves out: the local record, git's store, environments and caches."""


@cache
def _repo_tree(repo_dir: Path) -> RepoTree:
    """Return the repository's files and folders, the skipped folders pruned from the walk."""
    files: set[str] = set()
    file_names: set[str] = set()
    folder_names: set[str] = set()
    for folder, subfolders, names in os.walk(repo_dir):
        subfolders[:] = [name for name in subfolders if name not in _SKIPPED_PARTS]
        folder_names.update(subfolders)
        relative = Path(folder).relative_to(repo_dir)
        files.update((relative / name).as_posix() for name in names)
        file_names.update(names)
    return RepoTree(frozenset(files), frozenset(file_names), frozenset(folder_names))


@cache
def _vocabulary(repo_dir: Path) -> frozenset[str]:
    """Return the code names a page may cite: every word of the code (``code/src/``), the
    scenarios and the promoted JSON artifacts, and every name a test module defines at its
    top level (never the words of a test's assertions, which may name what was removed)."""
    sources = [*(repo_dir / "code" / "src").rglob("*.py")]
    sources += sorted((repo_dir / _SCENARIOS_DIR).glob("*.yaml"))
    sources += [repo_dir / name for name in _PROMOTED_ARTIFACTS]
    words: set[str] = set()
    for source in sources:
        words.update(_WORD.findall(source.read_text(encoding="utf-8")))
    for test_module in (repo_dir / "code" / "tests").rglob("*.py"):
        words.update(_top_level_names(test_module))
    return frozenset(words)


@cache
def _test_names(repo_dir: Path) -> frozenset[str]:
    """Return the name of every test function defined under ``code/tests/``."""
    names: set[str] = set()
    for source in (repo_dir / "code" / "tests").rglob("test_*.py"):
        tree = ast.parse(source.read_text(encoding="utf-8"))
        names.update(
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
            and node.name.startswith("test_")
        )
    return frozenset(names)


@cache
def _claim_ids(repo_dir: Path) -> frozenset[str]:
    """Return every claim ID that heads a row of the source ledger."""
    ledger = (repo_dir / _SOURCE_LEDGER).read_text(encoding="utf-8")
    return frozenset(re.findall(r"^\| `([^`]+)` \|", ledger, flags=re.MULTILINE))


@cache
def _top_level_names(module_file: Path) -> frozenset[str]:
    """Return the names a module defines at its top level (functions, classes, assignments,
    imports)."""
    tree = ast.parse(module_file.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
        elif isinstance(node, ast.Import | ast.ImportFrom):
            names.update((alias.asname or alias.name).split(".")[0] for alias in node.names)
    return frozenset(names)


def _module_file(source_dir: Path, parts: list[str]) -> Path | None:
    """Return the file of the module the dotted parts name under ``code/src/``, if any."""
    base = source_dir.joinpath(*parts)
    if (base / "__init__.py").is_file():
        return base / "__init__.py"
    if base.with_suffix(".py").is_file():
        return base.with_suffix(".py")
    return None


def _module_problem(repo_dir: Path, dotted: str) -> str | None:
    """Return why a module path does not resolve, or None when it does."""
    parts = dotted.split(".")
    source_dir = repo_dir / "code" / "src"
    for cut in range(len(parts), 0, -1):
        module_file = _module_file(source_dir, parts[:cut])
        if module_file is None:
            continue
        rest = parts[cut:]
        if not rest:
            return None
        if rest[0] not in _top_level_names(module_file):
            return f"{'.'.join(parts[:cut])} defines no top-level {rest[0]}"
        text_words = set(_WORD.findall(module_file.read_text(encoding="utf-8")))
        missing = [part for part in rest[1:] if part not in text_words]
        return f"{'.'.join(parts[:cut])} has no {missing[0]}" if missing else None
    return "no such module under code/src"


def _is_path_like(span: str) -> bool:
    """Return whether a span is a path or a file name rather than a code name."""
    return "/" in span or span.endswith(_FILE_EXTENSIONS)


def _path_problem(repo_dir: Path, page: Path, span: str) -> str | None:
    """Return why a path or file name does not resolve, or None when it does."""
    tree = _repo_tree(repo_dir)
    clean = _LINE_SUFFIX.sub("", span.split("#")[0]).rstrip("/")
    if not clean:
        return None
    root = repo_dir.resolve()
    bases = [root, root / "code", page.parent.resolve()]
    if "*" in clean:
        patterns = [
            (base / clean).relative_to(root).as_posix()
            for base in bases
            if (base / clean).is_relative_to(root)
        ]
        hits = [
            name
            for name in tree.files
            if any(fnmatch.fnmatch(name, pattern) for pattern in patterns)
            or ("/" not in clean and fnmatch.fnmatch(Path(name).name, clean))
        ]
        return None if hits else "no file matches the glob"
    for base in bases:
        candidate = (base / clean).resolve()
        if candidate.is_relative_to(root) and candidate.exists():
            return None
    if "/" not in clean and clean in tree.file_names:
        return None
    return "no such file or folder"


def _local_problem(line: str) -> str | None:
    """Return why a ``.agent/`` path's line breaks the local rule, or None when it holds."""
    return None if _LOCAL_MARK in line else f"a {_LOCAL_DIR}/ path whose line lacks {_LOCAL_MARK}"


def _name_problem(repo_dir: Path, span: str) -> str | None:
    """Return why a code name does not resolve, or None when it does (or when it is no name)."""
    if _CLAIM_ID.fullmatch(span):
        return None if span in _claim_ids(repo_dir) else "no row of the source ledger"
    if _TEST_NAME.fullmatch(span):
        return None if span in _test_names(repo_dir) else "no test function of that name"
    if span in _COMMAND_TOOLS:
        return None
    if _CODE_NAME_GLOB.fullmatch(span) and _WORD.search(span):
        hits = [word for word in _vocabulary(repo_dir) if fnmatch.fnmatchcase(word, span)]
        return None if hits else "no word of the code matches the pattern"
    if not _CODE_NAME.fullmatch(span):
        return None
    parts = [re.sub(r"(\[\*?\]|\(\))$", "", part) for part in span.split(".")]
    if parts[0] in _PACKAGES and len(parts) > 1:
        return _module_problem(repo_dir, ".".join(parts))
    if len(parts) == 1 and parts[0] in _repo_tree(repo_dir).folder_names:
        return None
    missing = [part for part in parts if part not in _vocabulary(repo_dir)]
    return f"{missing[0]} is no word of the code, scenarios or artifacts" if missing else None


def _command_words(span: str) -> Iterator[tuple[str, str | None]]:
    """Yield each word of a command span, shell quoting respected, with the word before it."""
    try:
        words = shlex.split(span)
    except ValueError:
        words = span.split()
    previous: str | None = None
    for word in words:
        yield word, previous
        previous = word


def _span_problems(repo_dir: Path, page: Path, line: str, span: str) -> Iterator[tuple[str, str]]:
    """Yield (word, why) for each part of a span that does not resolve."""
    if not any(ch.isspace() for ch in span):
        why = _single_problem(repo_dir, page, line, span)
        if why is not None:
            yield span, why
        return
    for word, previous in _command_words(span):
        if previous == "-m":
            why = _module_problem(repo_dir, word)
        elif previous in _OUTPUT_WORDS or word.startswith("/") or any(c.isspace() for c in word):
            continue
        elif word.startswith(_LOCAL_DIR):
            why = _local_problem(line)
        elif _SHELL_OPERATORS.search(word) or _PLACEHOLDER.search(word) or word.startswith("-"):
            continue
        elif _is_path_like(word) and not word.startswith(("'", '"', ".")):
            why = _path_problem(repo_dir, page, word)
        else:
            continue
        if why is not None:
            yield word, why


def _single_problem(repo_dir: Path, page: Path, line: str, span: str) -> str | None:
    """Return why a span with no white space does not resolve, or None when it does."""
    if span.startswith(_LOCAL_DIR):
        return _local_problem(line)
    if "::" in span:
        file_part, _, test_part = span.partition("::")
        return _path_problem(repo_dir, page, file_part) or _name_problem(repo_dir, test_part)
    if span.startswith((".", "-", "'", '"', "/")) or _PLACEHOLDER.search(span):
        return None
    if _is_path_like(span):
        return _path_problem(repo_dir, page, span)
    return _name_problem(repo_dir, span)


def _link_problem(page: Path, target: str) -> str | None:
    """Return why a Markdown link's target does not resolve, or None when it does."""
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    path = (page.parent / target.split("#")[0]).resolve()
    return None if path.exists() else "the link's target does not exist"


def _failures(repo_dir: Path, page: Path) -> Iterator[Failure]:
    """Yield every failure on one page."""
    where = page.relative_to(repo_dir).as_posix()
    exceptions = {entry.span for entry in _DECIDED_NOT_BUILT if entry.page == where}
    for number, line in enumerate(page.read_text(encoding="utf-8").splitlines(), start=1):
        imported = _IMPORT.match(line.strip()) if page.name == "CLAUDE.md" else None
        if imported is not None and not (repo_dir / imported.group(1)).is_file():
            yield Failure(where, number, line.strip(), "the import names no file")
        for target in _LINK.findall(line):
            if (why := _link_problem(page, target)) is not None:
                yield Failure(where, number, target, why)
        for span in _SPAN.findall(line):
            if span in exceptions:
                continue
            for word, why in _span_problems(repo_dir, page, line, span):
                yield Failure(where, number, word, why)


def test_every_path_and_name_the_agent_pages_spell_resolves(repo_dir: Path) -> None:
    """Objective: every link, path, module, test, claim ID and code name the charter, the
    glossary, the atlas and the ADRs spell resolves on the tree, and every ``.agent/`` path
    they name is marked ``(local)`` on its line.

    Sample: the pages on disk (``AGENTS.md``, ``CLAUDE.md``, ``CONTEXT.md``, every ``*.md``
    under ``atlas/`` and ``docs/adr/``), against the tree they describe.

    Expected outcome: every page and every source the guard reads exists (it cannot pass
    vacuously), and no span fails; the message lists each ``page:line``, the span and why.
    """
    pages = _pages(repo_dir)
    sources = [repo_dir / _SOURCE_LEDGER, *(repo_dir / name for name in _PROMOTED_ARTIFACTS)]
    missing = [path for path in pages + sources if not path.is_file()]
    assert not missing, f"the guard names pages or sources that do not exist: {missing}"
    assert all(any((repo_dir / tree).rglob("*.md")) for tree in _PAGE_TREES), (
        f"a page tree holds no page: {_PAGE_TREES}"
    )
    assert _vocabulary(repo_dir), "the code's vocabulary is empty"
    assert _test_names(repo_dir), "no test function found under code/tests"

    failures = [failure for page in pages for failure in _failures(repo_dir, page)]
    assert not failures, (
        f"{len(failures)} span(s) on the agent pages do not resolve; fix the page (or, for "
        "what an accepted ADR decided and no code has built yet, add it to "
        "_DECIDED_NOT_BUILT):\n" + "\n".join(str(failure) for failure in failures)
    )


@pytest.mark.parametrize("entry", _DECIDED_NOT_BUILT, ids=lambda entry: entry.span)
def test_every_decided_not_built_exception_is_still_needed(
    repo_dir: Path, entry: DecidedNotBuilt
) -> None:
    """Objective: each span the documents guard excuses as decided, not built, is still on its
    page and still names nothing on the tree, so no stale exception outlives the code it waits
    for.

    Sample: each entry of :data:`_DECIDED_NOT_BUILT`.

    Expected outcome: the page holds the span, and the span does not resolve; once the code an
    ADR decided lands, this fails until the entry is removed.
    """
    page = repo_dir / entry.page
    text = page.read_text(encoding="utf-8")
    assert f"`{entry.span}`" in text, f"{entry.page} no longer spells `{entry.span}`"
    line = next(line for line in text.splitlines() if f"`{entry.span}`" in line)
    assert list(_span_problems(repo_dir, page, line, entry.span)), (
        f"`{entry.span}` ({entry.decided_by}) now resolves: remove its _DECIDED_NOT_BUILT entry"
    )
