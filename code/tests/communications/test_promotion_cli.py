"""Tests for the Iridium promotion command's failure handling and output streams.

``python -m communications.json_output <scenario> <output>`` follows the shared
command-line conventions (``common.cli``) and writes its one artifact through
the shared writer (``common.file_io.write_files_with_rollback``). The contract:

1. a malformed scenario or an unwritable destination is one error record and
   exit status 1, never a traceback;
2. a failed write (a read-only directory, a failed rename) leaves the existing
   artifact exactly as it was, with no staged or backup file left behind, and
   the error says no destination was changed;
3. a successful promotion prints nothing to stdout and logs one INFO record
   naming the written path.
"""

from __future__ import annotations

import errno
import logging
import os
import stat
from pathlib import Path

import pytest

from common.cli import EXIT_ERROR, EXIT_OK
from communications.json_output import main

_READ_ONLY_DIR_MODE = stat.S_IRUSR | stat.S_IXUSR
"""A directory the owner can list and enter but not write into."""


def _errors(caplog: pytest.LogCaptureFixture) -> list[str]:
    """Return the messages of the captured ERROR (and worse) records."""
    return [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]


def test_a_malformed_scenario_fails_with_one_clean_error(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Objective: malformed YAML is a clean failure, not a parser traceback.

    Expected: exit 1, one single-line error record naming the scenario and
    "malformed YAML", and no artifact written.
    """
    scenario = tmp_path / "broken.yaml"
    scenario.write_text("iridium:\n  aperture_m2: [1.0\n", encoding="utf-8")
    out_path = tmp_path / "out.json"

    assert main([str(scenario), str(out_path)]) == EXIT_ERROR

    errors = _errors(caplog)
    assert len(errors) == 1
    assert "\n" not in errors[0]
    assert f"could not promote {scenario}" in errors[0]
    assert "malformed YAML" in errors[0]
    assert not out_path.exists()


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory permissions")
def test_an_unwritable_destination_leaves_the_artifact_untouched(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, iridium_yaml: Path
) -> None:
    """Objective: a write failure is reported cleanly and changes nothing.

    The original trigger: the writer called ``write_text`` directly, so an
    I/O error escaped as a traceback. Expected: with the artifact's directory
    read-only, exit 1 with one error record naming the destination; the
    existing artifact keeps its content and no staged file appears.
    """
    locked = tmp_path / "models"
    locked.mkdir()
    artifact = locked / "default.json"
    artifact.write_text("previous artifact\n", encoding="utf-8")
    locked.chmod(_READ_ONLY_DIR_MODE)
    try:
        exit_code = main([str(iridium_yaml), str(artifact)])
    finally:
        locked.chmod(stat.S_IRWXU)

    assert exit_code == EXIT_ERROR
    errors = _errors(caplog)
    assert len(errors) == 1
    assert f"{artifact}: could not write" in errors[0]
    assert errors[0].endswith("no destination was changed")
    assert artifact.read_text(encoding="utf-8") == "previous artifact\n"
    assert [p.name for p in locked.iterdir()] == ["default.json"]


def test_a_failed_rename_leaves_the_artifact_untouched(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
    iridium_yaml: Path,
) -> None:
    """Objective: the single artifact is replaced by one rename or not at all.

    Expected: with the rename failing (injected EIO), exit 1 with one error
    record naming the destination and saying no destination was changed;
    the existing artifact keeps its content and no staged or backup file
    remains beside it.
    """
    models = tmp_path / "models"
    models.mkdir()
    artifact = models / "default.json"
    artifact.write_text("previous artifact\n", encoding="utf-8")
    real_replace = os.replace

    def replace(src: str | os.PathLike[str], dst: str | os.PathLike[str]) -> None:
        if Path(dst) == artifact and Path(src).suffix == ".tmp":
            raise OSError(errno.EIO, "injected failure")
        real_replace(src, dst)

    monkeypatch.setattr(os, "replace", replace)

    assert main([str(iridium_yaml), str(artifact)]) == EXIT_ERROR

    errors = _errors(caplog)
    assert len(errors) == 1
    assert errors[0].endswith(
        f"{artifact}: could not replace the file (injected failure); no destination was changed"
    )
    assert artifact.read_text(encoding="utf-8") == "previous artifact\n"
    assert [p.name for p in models.iterdir()] == ["default.json"]


def test_a_successful_promotion_logs_its_status_and_prints_nothing(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
    iridium_yaml: Path,
) -> None:
    """Objective: status is a log record; stdout stays empty.

    Expected: exit 0, an artifact at the given path, an empty stdout, and one
    INFO record naming the written path.
    """
    caplog.set_level(logging.INFO, logger="communications.json_output")
    out_path = tmp_path / "iridium.json"

    assert main([str(iridium_yaml), str(out_path), "--version-stamp", "test"]) == EXIT_OK

    assert out_path.is_file()
    assert capsys.readouterr().out == ""
    status = [r.getMessage() for r in caplog.records if r.name == "communications.json_output"]
    assert status == [f"promoted Iridium model artifact written to {out_path}"]
