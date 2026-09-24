"""Tests for the shared file boundary (``common.file_io``).

The contract every loader and both promotion commands rely on:

1. :func:`load_yaml_mapping` reads every bundled scenario exactly as PyYAML's
   reference safe loader does, reads an empty file as ``{}``, and turns every
   failure (missing file, non-UTF-8 text, malformed YAML, a non-mapping root)
   into one ``ModelFileError`` naming the file;
2. :func:`write_files_with_rollback` writes every artifact, or restores the
   destinations it already replaced byte for byte and says so truthfully: a
   failed stage or a failed rename (injected, or a locked file) leaves no
   destination changed and no staged or backup file behind, and a rollback
   that itself fails is reported with where the previous content is kept; its
   staged and backup files never land on, or remove, a file the call did not
   create (a random name that collides is skipped); and a symbolic link or
   other non-regular destination is refused before anything is written;
3. :func:`locate_source_checkout` finds the checkout from a module under
   ``code/src/`` and refuses a module installed anywhere else.
"""

from __future__ import annotations

import errno
import os
import stat
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml

from common import file_io
from common.file_io import (
    ModelFileError,
    PendingWrite,
    SourceCheckout,
    load_yaml_mapping,
    locate_source_checkout,
    write_files_with_rollback,
)

_READ_ONLY_DIR_MODE = stat.S_IRUSR | stat.S_IXUSR
"""A directory the owner can list and enter but not write into."""

_ROOT_IGNORES_PERMISSIONS = os.geteuid() == 0
"""Root bypasses directory permissions and file flags, so those tests skip under root."""

type ReplaceFunction = Callable[[str | os.PathLike[str], str | os.PathLike[str]], None]
"""The signature of :func:`os.replace` as the tests call and patch it."""


def test_every_bundled_scenario_parses_as_the_reference_safe_loader_does(
    scenarios_dir: Path,
) -> None:
    """Objective: the fast loader changes no parsed value.

    Expected: every bundled scenario (at least the default, ground, and
    Iridium files) reads through the shared loader, libyaml's
    ``CSafeLoader`` when available, exactly as ``yaml.safe_load`` reads it.
    """
    paths = sorted(scenarios_dir.glob("*.yaml"))
    assert {"default.yaml", "ground_default.yaml", "iridium.yaml"} <= {p.name for p in paths}
    mismatched = [
        p.name
        for p in paths
        if load_yaml_mapping(p) != yaml.safe_load(p.read_text(encoding="utf-8"))
    ]
    assert not mismatched


def test_the_c_loader_is_used_when_libyaml_is_present() -> None:
    """Objective: the shared loader is libyaml's when this PyYAML build has it.

    Expected: ``CSafeLoader`` with libyaml, else the pure-Python ``SafeLoader``.
    """
    expected = yaml.CSafeLoader if yaml.__with_libyaml__ else yaml.SafeLoader
    assert file_io._YAML_LOADER is expected


def test_an_empty_file_reads_as_an_empty_mapping(tmp_path: Path) -> None:
    """Objective: an empty scenario takes every default. Expected: ``{}``."""
    path = tmp_path / "empty.yaml"
    path.write_text("# only a comment\n", encoding="utf-8")
    assert load_yaml_mapping(path) == {}


@pytest.mark.parametrize(
    ("content", "reason"),
    [
        (None, "file not found"),
        (b"cadence: \xff\xfe\n", "not valid utf-8 text"),
        (b"cadence:\n  cadence_ceiling: [150\n", "malformed YAML ("),
        (b"- a\n- list\n", "the YAML root must be a mapping, got list"),
        (b"just a string\n", "the YAML root must be a mapping, got str"),
    ],
    ids=["missing", "not_utf8", "malformed", "list_root", "scalar_root"],
)
def test_every_read_failure_is_one_model_file_error(
    tmp_path: Path, content: bytes | None, reason: str
) -> None:
    """Objective: one error type for every way a scenario file can be unreadable.

    Expected: a ``ModelFileError`` whose one-line message is
    ``<path>: <reason>``; a malformed file's reason carries the line number.
    """
    path = tmp_path / "scenario.yaml"
    if content is not None:
        path.write_bytes(content)
    with pytest.raises(ModelFileError) as excinfo:
        load_yaml_mapping(path)
    message = str(excinfo.value)
    assert message.startswith(f"{path}: {reason}")
    assert "\n" not in message
    assert excinfo.value.path == path
    if reason.startswith("malformed"):
        assert "at line 3, column 1" in message


# --------------------------------------------------------------------------
# write_files_with_rollback
# --------------------------------------------------------------------------


def _two_existing_artifacts(tmp_path: Path) -> tuple[Path, Path]:
    """Create two destinations with known previous content, in two directories."""
    first = tmp_path / "space" / "default.json"
    second = tmp_path / "ground" / "default.json"
    first.parent.mkdir()
    second.parent.mkdir()
    first.write_text("previous first\n", encoding="utf-8")
    second.write_text("previous second\n", encoding="utf-8")
    return first, second


def _new_content(first: Path, second: Path) -> list[PendingWrite]:
    """The pair of writes the rollback tests attempt."""
    return [PendingWrite(first, "new first\n"), PendingWrite(second, "new second\n")]


def _only_the_destinations_remain(*destinations: Path) -> bool:
    """Whether each destination's directory holds nothing but the destination."""
    return all([p.name for p in d.parent.iterdir()] == [d.name] for d in destinations)


def _failing_replace(
    monkeypatch: pytest.MonkeyPatch, fail_when: Callable[[Path, Path], bool]
) -> None:
    """Patch ``os.replace`` to raise EIO for the calls ``fail_when`` selects."""
    real_replace: ReplaceFunction = os.replace

    def replace(src: str | os.PathLike[str], dst: str | os.PathLike[str]) -> None:
        if fail_when(Path(src), Path(dst)):
            raise OSError(errno.EIO, "injected failure")
        real_replace(src, dst)

    monkeypatch.setattr(os, "replace", replace)


def test_the_writer_creates_directories_and_writes_every_file(tmp_path: Path) -> None:
    """Objective: a successful call writes each text exactly, creating parents.

    Expected: both files hold their new text; neither directory keeps a
    staged or backup file, including over an existing destination.
    """
    first = tmp_path / "a" / "one.json"
    second = tmp_path / "b" / "two.json"
    second.parent.mkdir()
    second.write_text("old two\n", encoding="utf-8")
    write_files_with_rollback([PendingWrite(first, "{}\n"), PendingWrite(second, "[]\n")])
    assert first.read_text(encoding="utf-8") == "{}\n"
    assert second.read_text(encoding="utf-8") == "[]\n"
    assert _only_the_destinations_remain(first, second)


@pytest.mark.skipif(_ROOT_IGNORES_PERMISSIONS, reason="root ignores directory permissions")
def test_a_staging_failure_changes_no_destination(tmp_path: Path) -> None:
    """Objective: nothing is replaced until every file is staged.

    Expected: when the second destination's directory is read-only, the call
    raises ``ModelFileError`` naming it and saying no destination changed;
    the first destination keeps its content, and neither directory holds a
    staged or backup file.
    """
    first, second = _two_existing_artifacts(tmp_path)
    second.parent.chmod(_READ_ONLY_DIR_MODE)
    try:
        with pytest.raises(ModelFileError) as excinfo:
            write_files_with_rollback(_new_content(first, second))
    finally:
        second.parent.chmod(stat.S_IRWXU)
    assert str(excinfo.value).startswith(f"{second}: could not write (")
    assert str(excinfo.value).endswith("no destination was changed")
    assert first.read_text(encoding="utf-8") == "previous first\n"
    assert second.read_text(encoding="utf-8") == "previous second\n"
    assert _only_the_destinations_remain(first, second)


def test_a_failed_second_rename_restores_the_first(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Objective: the pair is written or restored, never left half promoted.

    The original trigger: after the first rename succeeded, a failed second
    rename left the first file replaced while the message claimed nothing
    changed. Expected: with the second rename failing (injected EIO), the
    error names the second destination, says the first was restored and no
    destination remains changed; both destinations are byte-identical to
    their previous content and no staged or backup file remains.
    """
    first, second = _two_existing_artifacts(tmp_path)
    _failing_replace(monkeypatch, lambda src, dst: dst == second and src.suffix == ".tmp")

    with pytest.raises(ModelFileError) as excinfo:
        write_files_with_rollback(_new_content(first, second))

    message = str(excinfo.value)
    assert message.startswith(f"{second}: could not replace the file (injected failure)")
    assert f"restored the previous state of {first}" in message
    assert message.endswith("no destination remains changed")
    assert first.read_bytes() == b"previous first\n"
    assert second.read_bytes() == b"previous second\n"
    assert _only_the_destinations_remain(first, second)


def test_a_failed_second_rename_removes_a_first_file_that_was_new(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Objective: rolling back a destination that did not exist removes it.

    Expected: the first destination, absent before the call, is absent after
    the failed second rename; the second keeps its previous content; no
    staged or backup file remains.
    """
    first = tmp_path / "space" / "named.json"
    second = tmp_path / "ground" / "default.json"
    second.parent.mkdir()
    second.write_text("previous second\n", encoding="utf-8")
    _failing_replace(monkeypatch, lambda src, dst: dst == second and src.suffix == ".tmp")

    with pytest.raises(ModelFileError, match="no destination remains changed"):
        write_files_with_rollback(_new_content(first, second))

    assert not first.exists()
    assert list(first.parent.iterdir()) == []
    assert second.read_bytes() == b"previous second\n"
    assert _only_the_destinations_remain(second)


def test_a_failed_rollback_is_reported_with_the_kept_backup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Objective: when a rollback itself fails, the message says so truthfully.

    Expected: with the second rename failing and the first destination's
    restore failing too, the error says the first still holds the new
    content and names the backup that keeps its previous content; that
    backup exists and holds the previous bytes; the second is unchanged.
    """
    first, second = _two_existing_artifacts(tmp_path)
    _failing_replace(
        monkeypatch,
        lambda src, dst: (dst == second and src.suffix == ".tmp") or src.suffix == ".bak",
    )

    with pytest.raises(ModelFileError) as excinfo:
        write_files_with_rollback(_new_content(first, second))

    message = str(excinfo.value)
    assert f"{first} still holds the new content (rollback failed: injected failure)" in message
    assert "no destination remains changed" not in message
    kept = [p for p in first.parent.iterdir() if p.suffix == ".bak"]
    assert len(kept) == 1
    assert f"its previous content is kept at {kept[0]}" in message
    assert kept[0].read_bytes() == b"previous first\n"
    assert first.read_bytes() == b"new first\n"
    assert second.read_bytes() == b"previous second\n"
    assert [p.name for p in second.parent.iterdir()] == [second.name]


@pytest.mark.skipif(
    not hasattr(os, "chflags") or _ROOT_IGNORES_PERMISSIONS,
    reason="needs BSD file flags (macOS) and a non-root user",
)
def test_a_locked_second_destination_leaves_both_untouched(tmp_path: Path) -> None:
    """Objective: a naturally failing rename (a locked file) rolls back cleanly.

    ``chflags uchg`` makes the second destination immutable: it cannot be
    hard-linked (the backup falls back to a copy) or replaced. Expected: the
    error names the locked file and says the first was restored; both
    destinations are byte-identical to their previous content and no staged
    or backup file remains.
    """
    first, second = _two_existing_artifacts(tmp_path)
    os.chflags(second, stat.UF_IMMUTABLE)
    try:
        with pytest.raises(ModelFileError) as excinfo:
            write_files_with_rollback(_new_content(first, second))
    finally:
        os.chflags(second, 0)
    message = str(excinfo.value)
    assert message.startswith(f"{second}: could not replace the file (")
    assert message.endswith(
        f"restored the previous state of {first}; no destination remains changed"
    )
    assert first.read_bytes() == b"previous first\n"
    assert second.read_bytes() == b"previous second\n"
    assert _only_the_destinations_remain(first, second)


# --------------------------------------------------------------------------
# Staged and backup names never land on a file the call did not create
# --------------------------------------------------------------------------

_BYSTANDER_TEXT = "not the writer's\n"
"""Content of an unrelated file that already holds a name the writer draws."""


def _draw_tokens(monkeypatch: pytest.MonkeyPatch, *tokens: str) -> None:
    """Make the writer draw these random name tokens, in this order."""
    queue = list(tokens)
    monkeypatch.setattr(file_io, "_random_token", lambda: queue.pop(0))


def _bystander(destination: Path, token: str, suffix: str) -> Path:
    """Create an unrelated file at the hidden name the writer builds from ``token``."""
    path = destination.with_name(f".{destination.name}.{token}{suffix}")
    path.write_text(_BYSTANDER_TEXT, encoding="utf-8")
    return path


def test_a_staged_name_collision_leaves_the_existing_file_untouched(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Objective: the writer never removes a file it did not create.

    The original trigger: when the staged file's random name was already
    taken, the exclusive open failed and the error path deleted that
    unrelated file. Expected: the first name is skipped, the write succeeds
    under a fresh one, and the unrelated file keeps its content; nothing else
    is left beside the destination.
    """
    destination = tmp_path / "default.json"
    destination.write_text("previous\n", encoding="utf-8")
    bystander = _bystander(destination, "taken", ".tmp")
    _draw_tokens(monkeypatch, "taken", "staged", "backup")

    write_files_with_rollback([PendingWrite(destination, "new\n")])

    assert destination.read_text(encoding="utf-8") == "new\n"
    assert bystander.read_text(encoding="utf-8") == _BYSTANDER_TEXT
    assert sorted(p.name for p in tmp_path.iterdir()) == sorted([bystander.name, destination.name])


@pytest.mark.parametrize("hard_links_refused", [False, True], ids=["hard_link", "copy_fallback"])
def test_a_backup_name_collision_leaves_the_existing_file_untouched(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, hard_links_refused: bool
) -> None:
    """Objective: the backup never overwrites a file it did not create.

    The original trigger: when the backup's random name was taken, the
    hard link failed, the fallback copy overwrote the unrelated file, and a
    successful write then deleted it. Expected, with hard links allowed and
    with them refused (the copy path): the taken name is skipped, the write
    succeeds, and the unrelated file keeps its content.
    """
    destination = tmp_path / "default.json"
    destination.write_text("previous\n", encoding="utf-8")
    bystander = _bystander(destination, "taken", ".bak")
    _draw_tokens(monkeypatch, "staged", "taken", "backup")
    if hard_links_refused:

        def refuse_link(src: str | os.PathLike[str], dst: str | os.PathLike[str]) -> None:
            raise OSError(errno.EPERM, "hard links refused")

        monkeypatch.setattr(os, "link", refuse_link)

    write_files_with_rollback([PendingWrite(destination, "new\n")])

    assert destination.read_text(encoding="utf-8") == "new\n"
    assert bystander.read_text(encoding="utf-8") == _BYSTANDER_TEXT
    assert sorted(p.name for p in tmp_path.iterdir()) == sorted([bystander.name, destination.name])


def test_when_every_name_is_taken_the_write_fails_and_removes_nothing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Objective: giving up on names is a clean failure, not a deletion.

    Every name the writer draws is already taken. Expected: ``ModelFileError``
    saying no free name was found and no destination changed; the destination
    and the unrelated file keep their content.
    """
    destination = tmp_path / "default.json"
    destination.write_text("previous\n", encoding="utf-8")
    bystander = _bystander(destination, "taken", ".tmp")
    monkeypatch.setattr(file_io, "_random_token", lambda: "taken")

    with pytest.raises(ModelFileError) as excinfo:
        write_files_with_rollback([PendingWrite(destination, "new\n")])

    assert "no free name" in str(excinfo.value)
    assert str(excinfo.value).endswith("no destination was changed")
    assert destination.read_text(encoding="utf-8") == "previous\n"
    assert bystander.read_text(encoding="utf-8") == _BYSTANDER_TEXT


@pytest.mark.parametrize("kind", ["symbolic_link", "directory"])
def test_a_non_regular_destination_is_refused_before_anything_is_written(
    tmp_path: Path, kind: str
) -> None:
    """Objective: a promoted artifact only ever replaces a regular file.

    Renaming over a symbolic link would replace the link itself and leave
    its target stale. Expected: ``ModelFileError`` naming the destination,
    raised before any write of the call (the first, valid destination is not
    created); the link and its target, or the directory, are unchanged, and no
    staged or backup file appears.
    """
    first = tmp_path / "space.json"
    target = tmp_path / "real.json"
    target.write_text("previous\n", encoding="utf-8")
    destination = tmp_path / "ground.json"
    if kind == "symbolic_link":
        destination.symlink_to(target)
    else:
        destination.mkdir()
    reason = "is a symbolic link" if kind == "symbolic_link" else "is not a regular file"

    with pytest.raises(ModelFileError, match=reason) as excinfo:
        write_files_with_rollback(
            [PendingWrite(first, "new first\n"), PendingWrite(destination, "x")]
        )

    assert str(excinfo.value).startswith(f"{destination}: ")
    assert str(excinfo.value).endswith("no destination was changed")
    assert not first.exists()
    assert target.read_text(encoding="utf-8") == "previous\n"
    if kind == "symbolic_link":
        assert destination.is_symlink()
        assert destination.resolve() == target.resolve()
    else:
        assert destination.is_dir()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["ground.json", "real.json"]


# --------------------------------------------------------------------------
# locate_source_checkout
# --------------------------------------------------------------------------


def test_the_checkout_is_found_from_a_module_under_code_src(code_dir: Path, repo_dir: Path) -> None:
    """Objective: the anchor resolves from a real source module.

    Expected: the checkout's root is this repository; a path inside the
    repository reads back repository-relative, one outside as an absolute
    POSIX path.
    """
    checkout = locate_source_checkout(file_io.__file__)
    assert checkout == SourceCheckout(repo_dir=repo_dir)
    assert checkout.repo_relative(code_dir / "scenarios" / "default.yaml") == (
        "code/scenarios/default.yaml"
    )
    outside = Path("/") / "elsewhere" / "x.yaml"
    assert checkout.repo_relative(outside) == outside.as_posix()


def test_an_installed_module_is_not_a_source_checkout(tmp_path: Path) -> None:
    """Objective: never resolve repository paths into a virtual environment.

    The original trigger: from an installed wheel the anchor landed in
    ``<venv>/lib``, and ``--promote --output-name`` wrote there with exit 0.
    Expected: a module under ``site-packages`` (even beside a stray
    ``pyproject.toml``) raises ``ModelFileError`` saying it is not a source
    checkout.
    """
    site_packages = tmp_path / "lib" / "python3.14" / "site-packages"
    module = site_packages / "data_center" / "cli.py"
    module.parent.mkdir(parents=True)
    module.write_text("", encoding="utf-8")
    (tmp_path / "lib" / "python3.14" / "pyproject.toml").write_text("", encoding="utf-8")
    with pytest.raises(ModelFileError, match="not running from a source checkout"):
        locate_source_checkout(module)
