"""File I/O at the models' process boundary: YAML scenarios in, JSON artifacts out.

Every scenario loader in the repository (the data-center config and the
generations file it may reference, the ground reference, the communications
config) reads YAML through :func:`load_yaml_mapping`. Both promotion commands
(``rklb-value --promote`` and ``python -m communications.json_output``) write
their artifacts through :func:`write_files_with_rollback` (every file, or every
destination put back as it was) and find the repository through
:func:`locate_source_checkout`. All three report failure as one
:class:`ModelFileError` carrying the path and a one-line reason: the single
file-boundary error type every command-line entry point catches.

YAML is parsed with PyYAML's libyaml-backed ``CSafeLoader`` when this PyYAML
build includes libyaml (about ten times faster on the default scenario), else
with the pure-Python ``SafeLoader``. Both construct only plain Python types
(mappings, lists, strings, numbers, booleans, None), never arbitrary objects.
"""

from __future__ import annotations

import logging
import os
import shutil
import uuid
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final  # typing-acceptable: Any types the YAML deserialization boundary

import yaml

logger = logging.getLogger(__name__)

TEXT_ENCODING: Final[str] = "utf-8"
"""Encoding of every scenario YAML read and every artifact written."""

_YAML_LOADER: Final[type[yaml.SafeLoader] | type[yaml.CSafeLoader]] = (
    yaml.CSafeLoader if yaml.__with_libyaml__ else yaml.SafeLoader
)
"""The safe YAML loader: libyaml's C implementation when available."""

_ONE_BASED_OFFSET: Final[int] = 1
"""Added to PyYAML's zero-based line and column marks to report them as an editor does."""

_HIDDEN_PREFIX: Final[str] = "."
"""Staged and backup files are hidden files beside their destination."""

_STAGED_SUFFIX: Final[str] = ".tmp"
"""Suffix of a destination's complete new content, staged beside it before the rename."""

_BACKUP_SUFFIX: Final[str] = ".bak"
"""Suffix of a destination's preserved previous content, kept until the write completes."""

_MODULE_DEPTH_BELOW_CODE_DIR: Final[int] = 2
"""How far a model module sits below ``code/``: ``code/src/<package>/<module>.py``
has ``code/`` as its third parent (index 2 in ``Path.parents``)."""

_SOURCE_DIR_NAME: Final[str] = "src"
"""The source directory every model package lives in, inside ``code/``."""

_CHECKOUT_MARKERS: Final[tuple[str, ...]] = ("pyproject.toml", "scenarios")
"""Entries a ``code/`` directory of a source checkout always holds (the wheel ships neither)."""


class ModelFileError(Exception):
    """A scenario, generations, or artifact file could not be read, parsed, or written.

    Raised for a missing or unreadable file, text that is not UTF-8, malformed
    YAML, a YAML root that is not a mapping, a file whose content has the
    wrong top-level shape, a failed artifact write, and a package running
    outside a source checkout. The message is one line: ``<path>: <reason>``.

    Attributes:
        path: The file or directory the failure concerns.
        reason: One line saying what went wrong.
    """

    def __init__(self, path: Path, reason: str) -> None:
        """Build the error from the path it concerns and a one-line reason."""
        super().__init__(f"{path}: {reason}")
        self.path = path
        self.reason = reason


def _os_reason(exc: OSError) -> str:
    """Return the operating system's short reason for an I/O failure."""
    return exc.strerror or str(exc)


def _describe_yaml_error(exc: yaml.YAMLError) -> str:
    """Return a one-line description of a YAML parse failure, with its position."""
    if isinstance(exc, yaml.MarkedYAMLError) and exc.problem and exc.problem_mark:
        mark = exc.problem_mark
        return (
            f"{exc.problem} at line {mark.line + _ONE_BASED_OFFSET}, "
            f"column {mark.column + _ONE_BASED_OFFSET}"
        )
    return " ".join(str(exc).split())


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    """Read a UTF-8 YAML file whose root is a mapping.

    An empty file (or one holding only comments) reads as an empty mapping,
    so a scenario that sets nothing takes every default.

    Args:
        path: The YAML file to read.

    Returns:
        The parsed top-level mapping.

    Raises:
        ModelFileError: If the file is missing or unreadable, is not valid
            UTF-8, is malformed YAML, or has a root that is not a mapping.
    """
    try:
        text = path.read_text(encoding=TEXT_ENCODING)
    except FileNotFoundError as exc:
        raise ModelFileError(path, "file not found") from exc
    except OSError as exc:
        raise ModelFileError(path, f"could not read the file ({_os_reason(exc)})") from exc
    except UnicodeDecodeError as exc:
        raise ModelFileError(
            path, f"not valid {TEXT_ENCODING} text ({exc.reason} at byte {exc.start})"
        ) from exc
    try:
        loaded: Any = yaml.load(text, Loader=_YAML_LOADER)  # noqa: S506 (a safe loader)
    except yaml.YAMLError as exc:
        raise ModelFileError(path, f"malformed YAML ({_describe_yaml_error(exc)})") from exc
    if loaded is None:
        logger.debug("empty YAML file %s reads as an empty mapping", path)
        return {}
    if not isinstance(loaded, dict):
        raise ModelFileError(path, f"the YAML root must be a mapping, got {type(loaded).__name__}")
    logger.debug("loaded YAML mapping with %d top-level keys from %s", len(loaded), path)
    return loaded


@dataclass(frozen=True)
class PendingWrite:
    """One artifact to write: its destination path and its complete text.

    Attributes:
        path: Where the artifact goes; missing parent directories are created.
        text: The full file content, written as UTF-8.
    """

    path: Path
    text: str


@dataclass(frozen=True)
class _PreparedWrite:
    """A write ready to rename: its destination, its staged new content, and its backup.

    Attributes:
        destination: The artifact's path.
        staged: The hidden file beside it holding the complete new content.
        backup: The hidden file beside it preserving the previous content, or
            None when the destination did not exist before this write.
    """

    destination: Path
    staged: Path
    backup: Path | None


def _sibling(destination: Path, suffix: str) -> Path:
    """Return a new, uniquely named hidden file path beside ``destination``."""
    return destination.with_name(f"{_HIDDEN_PREFIX}{destination.name}.{uuid.uuid4().hex}{suffix}")


def _remove_created(paths: Iterable[Path]) -> None:
    """Remove staged or backup files this write created (best effort, each failure logged)."""
    for path in paths:
        try:
            path.unlink(missing_ok=True)
        except OSError as exc:
            logger.warning("could not remove %s (%s)", path, _os_reason(exc))


def _leftovers(prepared: Iterable[_PreparedWrite]) -> list[Path]:
    """Return the staged and backup files of writes that will not complete."""
    paths: list[Path] = []
    for item in prepared:
        paths.append(item.staged)
        if item.backup is not None:
            paths.append(item.backup)
    return paths


def _stage(write: PendingWrite) -> Path:
    """Write one artifact in full, flushed to disk, to a hidden file beside it.

    Returns:
        The staged file's path.

    Raises:
        OSError: If the directory or the staged file cannot be written (a
            partially written staged file is removed first).
    """
    staged = _sibling(write.path, _STAGED_SUFFIX)
    try:
        write.path.parent.mkdir(parents=True, exist_ok=True)
        with staged.open("x", encoding=TEXT_ENCODING) as handle:
            handle.write(write.text)
            handle.flush()
            os.fsync(handle.fileno())
    except OSError:
        _remove_created([staged])
        raise
    return staged


def _preserve(destination: Path) -> Path | None:
    """Keep a destination's current content in a hidden backup file beside it.

    A hard link keeps the very file, content and metadata, at no copying cost.
    Where the file system refuses one (a locked or append-only file, a file
    system without hard links), a byte copy with the same permission bits is
    kept instead; the copy deliberately leaves out file flags, so the backup of
    a locked file can still be removed.

    Returns:
        The backup's path, or None when the destination does not exist yet.

    Raises:
        OSError: If neither a hard link nor a copy can be made (a partial copy
            is removed first).
    """
    if not destination.exists():
        return None
    backup = _sibling(destination, _BACKUP_SUFFIX)
    try:
        os.link(destination, backup)
    except OSError:
        try:
            shutil.copyfile(destination, backup)
            shutil.copymode(destination, backup)
        except OSError:
            _remove_created([backup])
            raise
    return backup


def _roll_back(replaced: Sequence[_PreparedWrite]) -> str:
    """Put every replaced destination back as it was; describe the outcome in one line.

    A destination with a backup is restored by renaming the backup over it; a
    destination that did not exist before the write is removed. A destination
    that cannot be put back keeps its new content, and its backup is kept for
    recovery.

    Args:
        replaced: The writes whose rename already succeeded, in rename order.

    Returns:
        The outcome clause for the error message: which destinations were
        restored and which, if any, still hold new content.
    """
    restored: list[str] = []
    unrestored: list[str] = []
    for item in reversed(replaced):
        try:
            if item.backup is None:
                item.destination.unlink()
            else:
                os.replace(item.backup, item.destination)
        except OSError as exc:
            kept = (
                f"its previous content is kept at {item.backup}"
                if item.backup is not None
                else "it did not exist before this write"
            )
            unrestored.append(
                f"{item.destination} still holds the new content "
                f"(rollback failed: {_os_reason(exc)}); {kept}"
            )
        else:
            restored.append(str(item.destination))
    if not restored and not unrestored:
        return "no destination was changed"
    restored_clause = f"restored the previous state of {', '.join(restored)}" if restored else ""
    if not unrestored:
        return f"{restored_clause}; no destination remains changed"
    return "; ".join(clause for clause in (restored_clause, *unrestored) if clause)


def write_files_with_rollback(writes: Sequence[PendingWrite]) -> None:
    """Write every artifact, or put every destination back as it was.

    The write runs in three steps:

    1. Stage: each text is written in full, and flushed to disk, to a hidden
       ``.tmp`` file beside its destination (missing parent directories are
       created and left in place).
    2. Preserve: each existing destination is kept beside itself as a hidden
       ``.bak`` file (a hard link, or a byte copy where hard links are refused).
    3. Replace: each staged file is renamed over its destination with
       :func:`os.replace`, one at a time, in ``writes`` order.

    Each rename is atomic within its directory, so a reader never sees a
    half-written file; the set of renames is not atomic, so between two
    renames the destinations briefly hold a mix of new and previous content.
    A failure in step 1 or 2 changes no destination. A failure in step 3
    rolls back: every destination already replaced is restored from its backup
    (one that did not exist before is removed), and the error states which
    destinations were restored and which, if any, still hold new content and
    where their previous content is kept. Every staged and backup file this
    call created is removed, except a backup still needed for recovery; on
    success the backups are removed. The rollback runs in this process: if the
    process is killed between two renames, the hidden ``.bak`` files beside the
    destinations hold the previous content.

    Args:
        writes: The artifacts to write, in rename order.

    Raises:
        ModelFileError: If any artifact cannot be staged, preserved, or
            renamed. The one-line message names the failing destination, the
            operating system's reason, and the outcome for every destination.
    """
    prepared: list[_PreparedWrite] = []
    for write in writes:
        try:
            staged = _stage(write)
        except OSError as exc:
            _remove_created(_leftovers(prepared))
            raise ModelFileError(
                write.path, f"could not write ({_os_reason(exc)}); no destination was changed"
            ) from exc
        try:
            backup = _preserve(write.path)
        except OSError as exc:
            _remove_created([staged, *_leftovers(prepared)])
            raise ModelFileError(
                write.path,
                f"could not preserve the current file ({_os_reason(exc)}); "
                "no destination was changed",
            ) from exc
        prepared.append(_PreparedWrite(destination=write.path, staged=staged, backup=backup))

    for index, item in enumerate(prepared):
        try:
            os.replace(item.staged, item.destination)
        except OSError as exc:
            outcome = _roll_back(prepared[:index])
            _remove_created(_leftovers(prepared[index:]))
            raise ModelFileError(
                item.destination, f"could not replace the file ({_os_reason(exc)}); {outcome}"
            ) from exc
        logger.debug("wrote %s", item.destination)
    _remove_created(item.backup for item in prepared if item.backup is not None)


@dataclass(frozen=True)
class SourceCheckout:
    """The repository checkout a model package runs from.

    Attributes:
        repo_dir: The repository root: the parent of ``code/``, under which
            the scenarios (``code/scenarios/``) and the promoted artifacts
            (``data_center/models/``, ``communications/models/``) live.
    """

    repo_dir: Path

    def repo_relative(self, path: Path) -> str:
        """Return ``path`` as a repository-relative POSIX path, the provenance form.

        Args:
            path: A file path (relative paths resolve against the working
                directory).

        Returns:
            The path relative to the repository root, or its absolute POSIX
            form when it lies outside the repository.
        """
        resolved = path.resolve()
        try:
            return resolved.relative_to(self.repo_dir).as_posix()
        except ValueError:
            return resolved.as_posix()


def locate_source_checkout(module_file: str | Path) -> SourceCheckout:
    """Locate the source checkout a model module was imported from.

    The scenarios and the promoted artifacts are repository files, not package
    data: the wheel ships only the three Python packages. The command-line
    entry points therefore work only from a source checkout, where ``uv run``
    installs the package in editable mode and a module's ``__file__`` stays at
    ``code/src/<package>/<module>.py``. From an installed wheel the module
    sits in ``site-packages``, and anchoring there would silently read and
    write inside the virtual environment, so this function refuses instead.

    Args:
        module_file: The calling module's ``__file__``.

    Returns:
        The checkout, anchored at its repository root.

    Raises:
        ModelFileError: If the module does not sit in a source checkout's
            ``code/src/`` tree.
    """
    module_path = Path(module_file).resolve()
    parents = module_path.parents
    if len(parents) > _MODULE_DEPTH_BELOW_CODE_DIR:
        code_dir = parents[_MODULE_DEPTH_BELOW_CODE_DIR]
        in_source_tree = parents[_MODULE_DEPTH_BELOW_CODE_DIR - 1] == code_dir / _SOURCE_DIR_NAME
        if in_source_tree and all((code_dir / marker).exists() for marker in _CHECKOUT_MARKERS):
            return SourceCheckout(repo_dir=code_dir.parent)
    raise ModelFileError(
        module_path,
        "not running from a source checkout (expected code/src/<package>/ beside "
        "code/pyproject.toml and code/scenarios/); run the command from the "
        "repository's code/ directory with `uv run`",
    )


__all__ = [
    "TEXT_ENCODING",
    "ModelFileError",
    "PendingWrite",
    "SourceCheckout",
    "load_yaml_mapping",
    "locate_source_checkout",
    "write_files_with_rollback",
]
