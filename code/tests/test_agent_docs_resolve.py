"""Repository guard: every path and name the pages agents ground in spell resolves on the tree.

The documents guard forge-atlas recommends, the executable form of the atlas's first rule
("a page may be a sketch, but it states nothing untrue"). The pages are the ones an agent
grounds in: the charter ``AGENTS.md``, ``CLAUDE.md``, the glossary ``CONTEXT.md``,
``atlas/map.md`` and every page under ``atlas/``, and every ADR in ``docs/adr/``.

What it checks, on every line of every page:

* a line that names a ``.agent`` path, in any form (plain text, a backticked span, a link's
  target, a ``../.agent/`` path), carries the mark ``(local)``: ``.agent`` is the investor's
  local working record, absent from a fresh clone, so its paths are marked, never looked up;
* a Markdown link's target resolves from the page's folder (a web link is not looked up), and
  each ``@`` import in ``CLAUDE.md`` names a file at the repository root;
* every backticked span, word by word when it holds a command:

  - a path or a file name resolves: from the repository root, from ``code/`` (where the
    commands run) or from the page's folder; a bare file name anywhere in the repository; a
    glob matches at least one file. An absolute path, and a command's output after ``tee``,
    are not looked up;
  - a module path (``communications.saturation``, ``common.file_io.load_yaml_mapping``, the
    word after ``-m``) names a module under ``code/src/`` and then a name that module defines
    at its top level;
  - the word right after ``uv run`` is a command-line tool or an entry point that
    ``code/pyproject.toml`` declares under ``[project.scripts]`` (``rklb-value``);
  - a ``jq`` query's field names (``.name``, ``."key"``, ``["key"]`` and an object's shorthand
    ``{name}``) are keys of the JSON file it reads, or of a promoted artifact when it names
    none;
  - a test name (``test_...``) is a test function defined under ``code/tests/``;
  - a claim ID (``COMM-601``) is a row of ``research/SOURCE_INDEX.md``;
  - any other code name (``run_iridium_model``, ``fixed_books``,
    ``comms_cadence.share_of_fleet``) is, each dotted part, a code word: an identifier of the
    code (``code/src/``) or a word of a string literal there that is not a docstring, the
    source class a docstring opens with (``SOURCED_FACT``), a word of the scenarios or of the
    four promoted JSON artifacts, or a name a test module defines at its top level. A word
    the code keeps only in a comment or a docstring (a history note naming a removed field)
    is not a code word.

What counts as success: no span fails, and every page and source the guard reads exists, so
it cannot pass vacuously. On failure the message lists each ``page:line``, the span and why.

What it misses: a name that exists but is placed wrongly (a field said to live in the wrong
artifact, a dial that is an artifact field); numbers, counts and prose claims; a name written
outside backticks; a command's flags, an entry point that follows a flag
(``uv run --project code pytest``) and the values a ``jq`` filter compares against. The
human documents (the root ``README.md`` and the folders' documents) are not its pages.

Decided, not built: an accepted ADR may name a path or a field before the code that makes it
exists. :data:`_DECIDED_NOT_BUILT` lists each such span with the ADR that decides it; a
second test checks that each entry is still on its page and still does not resolve, so the
entry is removed in the change that builds it.

Superseded, history: an ADR under ``docs/adr/`` whose status line reads ``Superseded by ADR
N`` is history, and its code names are not checked. Why: an accepted ADR's body is never
edited (a decision changes only by a new ADR), and a superseded one records the old state, so
it keeps naming the code of its day, which the decision that replaced it may have removed (ADR
007 names ``fixed_books``, which ADR 011's code removes). Its links, paths, claim IDs and
``.agent`` marks are still checked as on any page; its code names (identifiers and fields,
module paths, test names, the word after ``uv run`` and a ``jq`` query's fields) are not. The
ADR its status names must exist under ``docs/adr/``, so the rule cannot excuse a page by a
status no ADR bears out.
"""

from __future__ import annotations

import ast
import fnmatch
import json
import os
import re
import shlex
import tomllib
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cache
from pathlib import Path

import pytest

_ROOT_PAGES = ("AGENTS.md", "CLAUDE.md", "CONTEXT.md")
"""The pages at the repository root: the charter, its loader and the glossary."""

_PAGE_TREES = ("atlas", "docs/adr")
"""Folders whose every ``*.md`` is a page: the atlas and the ADRs."""

_ADR_DIR = "docs/adr"
"""The ADRs: the pages that carry a status line, and the only ones a status can make history."""

_STATUS_PREFIX = "Status:"
"""The start of an ADR's status line."""

_SUPERSEDED = re.compile(r"Status:\s*Superseded by ADR (\d+)\b")
"""A status line that makes its ADR history: the number of the ADR that replaced it."""

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

_PYPROJECT = "code/pyproject.toml"
"""The package configuration, whose ``[project.scripts]`` names the entry points."""

_LOCAL_DIR = ".agent"
"""The investor's local working record: never in a clone, so its paths are marked, not found."""

_LOCAL_MARK = "(local)"
"""The mark a line naming a ``.agent/`` path must carry (the atlas's rules)."""

_LOCAL_PATH = re.compile(r"(?<![\w.-])\.agent(?![\w-])[^\s`)\]]*")
"""A ``.agent`` path in any form (plain text, a span, a link's target, ``../.agent/``)."""

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
"""Command-line tools a page may name, in a span of its own or right after ``uv run``: names,
but not the code's."""

_OUTPUT_WORDS = frozenset({"tee", ">", ">>"})
"""Words after which a command's next word is the output it writes, not an input."""

_COMMAND_SEPARATORS = frozenset({"|", "||", "&&", ";"})
"""Words that end one command and start the next inside a span."""

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

_SOURCE_CLASS = re.compile(r"[A-Z][A-Z_]+\b")
"""The source class a constant's docstring opens with (``SOURCED_FACT``, ``ESTIMATE``)."""

_JQ_STRING = re.compile(r'"(?:[^"\\]|\\.)*"')
"""A string literal in a ``jq`` filter."""

_JQ_QUOTED_KEY = re.compile(r'(?:\.|\[)\s*"((?:[^"\\]|\\.)*)"')
"""A key a ``jq`` filter reads by its quoted name: ``."2036"`` or ``["key"]``."""

_JQ_FIELD = re.compile(r"\.([A-Za-z_][A-Za-z0-9_]*)")
"""A field a ``jq`` filter reads by name: ``.name``."""

_JQ_OBJECT = re.compile(r"\{([^{}]*)\}")
"""The body of an object a ``jq`` filter builds."""

_JQ_SHORTHAND = re.compile(r"\s*[A-Za-z_][A-Za-z0-9_]*\s*")
"""An object entry in shorthand, ``{name}``, which reads the field of that name."""


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
    """Return the code names a page may cite: the code words of every module under
    ``code/src/`` (:func:`_code_words`), every word of the scenarios and the promoted JSON
    artifacts, and every name a test module defines at its top level (never the words of a
    test's assertions, which may name what was removed)."""
    words: set[str] = set()
    for module_file in (repo_dir / "code" / "src").rglob("*.py"):
        words.update(_code_words(module_file))
    data = [*sorted((repo_dir / _SCENARIOS_DIR).glob("*.yaml"))]
    data += [repo_dir / name for name in _PROMOTED_ARTIFACTS]
    for source in data:
        words.update(_WORD.findall(source.read_text(encoding="utf-8")))
    for test_module in (repo_dir / "code" / "tests").rglob("*.py"):
        words.update(_top_level_names(test_module))
    return frozenset(words)


def _docstring_constants(tree: ast.Module) -> list[ast.Constant]:
    """Return every string that stands as a statement of its own: the docstrings of modules,
    classes and functions, and the docstrings written under constants."""
    return [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    ]


@cache
def _code_words(module_file: Path) -> frozenset[str]:
    """Return a module's code words: every identifier it names (names, attributes,
    definitions, arguments, keywords, imports), every word of its string literals but its
    docstrings, and the source class each docstring may open with. A comment, and the rest of
    a docstring, add nothing: a history note naming a removed field must not revive it."""
    tree = ast.parse(module_file.read_text(encoding="utf-8"))
    docstrings = _docstring_constants(tree)
    skipped = {id(node) for node in docstrings}
    words: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            words.add(node.id)
        elif isinstance(node, ast.Attribute):
            words.add(node.attr)
        elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            words.add(node.name)
        elif isinstance(node, ast.arg | ast.keyword) and node.arg is not None:
            words.add(node.arg)
        elif isinstance(node, ast.alias):
            words.update(_WORD.findall(node.name))
            if node.asname is not None:
                words.add(node.asname)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            words.update(_WORD.findall(node.module))
        elif (
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and id(node) not in skipped
        ):
            words.update(_WORD.findall(node.value))
    for docstring in docstrings:
        if (source_class := _SOURCE_CLASS.match(str(docstring.value).lstrip())) is not None:
            words.add(source_class.group(0))
    return frozenset(words)


@cache
def _entry_points(repo_dir: Path) -> frozenset[str]:
    """Return the command names ``code/pyproject.toml`` declares under ``[project.scripts]``."""
    with (repo_dir / _PYPROJECT).open("rb") as handle:
        project = tomllib.load(handle)
    return frozenset(project.get("project", {}).get("scripts", {}))


@cache
def _json_keys(json_file: Path) -> frozenset[str]:
    """Return every object key, at any depth, of a JSON file."""
    keys: set[str] = set()
    pending: list[object] = [json.loads(json_file.read_text(encoding="utf-8"))]
    while pending:
        node = pending.pop()
        if isinstance(node, dict):
            keys.update(str(key) for key in node)
            pending.extend(node.values())
        elif isinstance(node, list):
            pending.extend(node)
    return frozenset(keys)


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
        missing = [part for part in rest[1:] if part not in _code_words(module_file)]
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


def _local_failure(where: str, number: int, line: str) -> Failure | None:
    """Return the failure of a line that names a ``.agent`` path without the mark, or None."""
    local = _LOCAL_PATH.search(line)
    if local is None or _LOCAL_MARK in line:
        return None
    why = f"a {_LOCAL_DIR} path whose line lacks {_LOCAL_MARK}"
    return Failure(where, number, local.group(0), why)


def _entry_point_problem(repo_dir: Path, word: str) -> str | None:
    """Return why the word after ``uv run`` names no tool or entry point, or None when it does."""
    if word in _COMMAND_TOOLS or word in _entry_points(repo_dir):
        return None
    return "no command-line tool or [project.scripts] entry of that name"


def _jq_fields(query: str) -> list[str]:
    """Return the field names a ``jq`` filter reads: ``.name``, ``."key"``, ``["key"]`` and an
    object's shorthand ``{name}``; a string it compares against is a value, not a field."""
    fields = _JQ_QUOTED_KEY.findall(query)
    bare = _JQ_STRING.sub('""', query)
    fields += _JQ_FIELD.findall(bare)
    for body in _JQ_OBJECT.findall(bare):
        fields += [entry.strip() for entry in body.split(",") if _JQ_SHORTHAND.fullmatch(entry)]
    return fields


def _jq_problems(repo_dir: Path, page: Path, arguments: list[str]) -> Iterator[tuple[str, str]]:
    """Yield (field, why) for each field a ``jq`` query reads that the JSON it reads lacks.

    ``arguments`` are the command's words after ``jq``: flags, the filter, then the files it
    reads, up to the next command. With no file that resolves to a JSON file, the fields are
    looked up in the four promoted artifacts.
    """
    operands: list[str] = []
    for word in arguments:
        if word in _COMMAND_SEPARATORS or word in _OUTPUT_WORDS:
            break
        if not word.startswith("-"):
            operands.append(word)
    if not operands:
        return
    query, files = operands[0], operands[1:]
    root = repo_dir.resolve()
    read = list(
        dict.fromkeys(
            candidate
            for name in files
            for base in (root, root / "code", page.parent.resolve())
            if (candidate := (base / name).resolve()).is_file() and candidate.suffix == ".json"
        )
    )
    targets = read or [root / name for name in _PROMOTED_ARTIFACTS]
    keys = frozenset[str]().union(*(_json_keys(target) for target in targets))
    named = ", ".join(path.relative_to(root).as_posix() for path in read)
    where = named or "the promoted artifacts"
    for field in _jq_fields(query):
        if field not in keys:
            yield field, f"no key {field!r} in {where}"


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


def _command_words(span: str) -> list[str]:
    """Return the words of a command span, shell quoting respected."""
    try:
        return shlex.split(span)
    except ValueError:
        return span.split()


def _span_problems(
    repo_dir: Path, page: Path, span: str, *, history: bool = False
) -> Iterator[tuple[str, str]]:
    """Yield (word, why) for each part of a span that does not resolve; on a superseded ADR
    (``history``) its code names are not checked, its paths and claim IDs are."""
    if not any(ch.isspace() for ch in span):
        why = _single_problem(repo_dir, page, span, history=history)
        if why is not None:
            yield span, why
        return
    words = _command_words(span)
    for index, word in enumerate(words):
        previous = words[index - 1] if index > 0 else None
        before = words[index - 2] if index > 1 else None
        entry_point = previous == "run" and before == "uv" and not word.startswith("-")
        if history and (previous == "-m" or entry_point):
            continue
        if previous == "-m":
            why = _module_problem(repo_dir, word)
        elif entry_point:
            why = _entry_point_problem(repo_dir, word)
        elif word == "jq" and (previous is None or previous in _COMMAND_SEPARATORS):
            if not history:
                yield from _jq_problems(repo_dir, page, words[index + 1 :])
            continue
        elif (
            previous in _OUTPUT_WORDS
            or word.startswith(("/", "-"))
            or any(c.isspace() for c in word)
            or _LOCAL_PATH.search(word)
            or _SHELL_OPERATORS.search(word)
            or _PLACEHOLDER.search(word)
        ):
            continue
        elif _is_path_like(word) and not word.startswith(("'", '"', ".")):
            why = _path_problem(repo_dir, page, word)
        else:
            continue
        if why is not None:
            yield word, why


def _single_problem(repo_dir: Path, page: Path, span: str, *, history: bool = False) -> str | None:
    """Return why a span with no white space does not resolve, or None when it does (a
    ``.agent`` path is never looked up: its line's mark is checked once, for the line; on a
    superseded ADR, ``history``, a code name is not looked up, a path or a claim ID is)."""
    if _LOCAL_PATH.search(span):
        return None
    if "::" in span:
        file_part, _, test_part = span.partition("::")
        if history:
            return _path_problem(repo_dir, page, file_part)
        return _path_problem(repo_dir, page, file_part) or _name_problem(repo_dir, test_part)
    if span.startswith((".", "-", "'", '"', "/")) or _PLACEHOLDER.search(span):
        return None
    if _is_path_like(span):
        return _path_problem(repo_dir, page, span)
    if history and not _CLAIM_ID.fullmatch(span):
        return None
    return _name_problem(repo_dir, span)


def _link_problem(page: Path, target: str) -> str | None:
    """Return why a Markdown link's target does not resolve, or None when it does (a web link
    and a ``.agent`` path are not looked up; the line check holds a local link to its mark)."""
    if target.startswith(("http://", "https://", "mailto:", "#")) or _LOCAL_PATH.search(target):
        return None
    path = (page.parent / target.split("#")[0]).resolve()
    return None if path.exists() else "the link's target does not exist"


@dataclass(frozen=True)
class Supersession:
    """A superseded ADR's status line.

    Attributes:
        line: The status line's number, from 1.
        by: The number of the ADR that replaced this one, as the status line writes it.
    """

    line: int
    by: str


def _supersession(repo_dir: Path, page: Path, lines: list[str]) -> Supersession | None:
    """Return the status of an ADR that a later ADR replaced, or None for any other page (an
    ADR whose status says otherwise, and every page outside ``docs/adr/``)."""
    if page.relative_to(repo_dir).parent.as_posix() != _ADR_DIR:
        return None
    for number, line in enumerate(lines, start=1):
        if line.startswith(_STATUS_PREFIX):
            superseded = _SUPERSEDED.match(line)
            return None if superseded is None else Supersession(number, superseded.group(1))
    return None


def _missing_successor(repo_dir: Path, supersession: Supersession) -> bool:
    """Return whether no ADR under ``docs/adr/`` has the number a status line names."""
    numbered = f"{int(supersession.by):03d}-*.md"
    return not any((repo_dir / _ADR_DIR).glob(numbered))


def _failures(repo_dir: Path, page: Path) -> Iterator[Failure]:
    """Yield every failure on one page (a superseded ADR's code names excepted: the module
    docstring's history rule)."""
    where = page.relative_to(repo_dir).as_posix()
    exceptions = {entry.span for entry in _DECIDED_NOT_BUILT if entry.page == where}
    lines = page.read_text(encoding="utf-8").splitlines()
    supersession = _supersession(repo_dir, page, lines)
    if supersession is not None and _missing_successor(repo_dir, supersession):
        yield Failure(
            where,
            supersession.line,
            f"Superseded by ADR {supersession.by}",
            f"no ADR numbered {supersession.by} under {_ADR_DIR}",
        )
    history = supersession is not None
    for number, line in enumerate(lines, start=1):
        if (local := _local_failure(where, number, line)) is not None:
            yield local
        imported = _IMPORT.match(line.strip()) if page.name == "CLAUDE.md" else None
        if imported is not None and not (repo_dir / imported.group(1)).is_file():
            yield Failure(where, number, line.strip(), "the import names no file")
        for target in _LINK.findall(line):
            if (why := _link_problem(page, target)) is not None:
                yield Failure(where, number, target, why)
        for span in _SPAN.findall(line):
            if span in exceptions:
                continue
            for word, why in _span_problems(repo_dir, page, span, history=history):
                yield Failure(where, number, word, why)


def test_every_path_and_name_the_agent_pages_spell_resolves(repo_dir: Path) -> None:
    """Objective: every link, path, module, entry point, ``jq`` field, test, claim ID and code
    name the charter, the glossary, the atlas and the ADRs spell resolves on the tree (a
    superseded ADR's code names excepted: they are history, as the module docstring says), and
    every line that names a ``.agent`` path, in any form, is marked ``(local)``.

    Sample: the pages on disk (``AGENTS.md``, ``CLAUDE.md``, ``CONTEXT.md``, every ``*.md``
    under ``atlas/`` and ``docs/adr/``), against the tree they describe.

    Expected outcome: every page and every source the guard reads exists (it cannot pass
    vacuously), and no span fails; the message lists each ``page:line``, the span and why.
    """
    pages = _pages(repo_dir)
    sources = [
        repo_dir / _SOURCE_LEDGER,
        repo_dir / _PYPROJECT,
        *(repo_dir / name for name in _PROMOTED_ARTIFACTS),
    ]
    missing = [path for path in pages + sources if not path.is_file()]
    assert not missing, f"the guard names pages or sources that do not exist: {missing}"
    assert all(any((repo_dir / tree).rglob("*.md")) for tree in _PAGE_TREES), (
        f"a page tree holds no page: {_PAGE_TREES}"
    )
    assert _vocabulary(repo_dir), "the code's vocabulary is empty"
    assert _test_names(repo_dir), "no test function found under code/tests"
    assert _entry_points(repo_dir), f"{_PYPROJECT} declares no [project.scripts] entry"

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
    assert list(_span_problems(repo_dir, page, entry.span)), (
        f"`{entry.span}` ({entry.decided_by}) now resolves: remove its _DECIDED_NOT_BUILT entry"
    )
