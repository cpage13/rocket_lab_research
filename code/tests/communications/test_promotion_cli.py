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
   naming the written path;
4. the command is the Iridium promotion command only: it narrows the scenario
   first, so a scenario without an ``iridium:`` block is one error record (the
   family's message) before any curve is read or any model runs;
5. it loads the saturation curve the scenario's ``iridium.saturation.curve_path``
   names (a relative path anchored to the repository root, an absolute one as
   given) and runs the Iridium entry: a missing curve, or one computed for other
   inputs (the identity check), is one error record naming it, and nothing is
   written.
"""

from __future__ import annotations

import errno
import logging
import os
import stat
from pathlib import Path
from typing import NoReturn

import pytest

from common.cli import EXIT_ERROR, EXIT_OK
from communications import json_output
from communications.json_output import main
from communications.saturation_curve import SaturationCurve

_NOT_AN_IRIDIUM_SCENARIO = (
    "the scenario does not select the Iridium model: it needs a top-level "
    "'iridium:' block (see scenarios/iridium.yaml)"
)
"""The family's refusal, word for word the command's message before the narrowing function."""

_COMMITTED_CURVE = Path("communications") / "models" / "iridium" / "saturation_curve.json"
"""The promoted saturation curve, repository-relative (the shipped scenario's curve path)."""

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


def test_a_scenario_without_an_iridium_block_fails_before_any_run(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Objective: the command narrows its scenario first, so a scenario of the cellular family
    fails with the family's message before any curve is read or any model runs.

    Sample: a scenario setting only the cellular satellite block; the command's curve loader
    and its Iridium entry replaced by stand-ins that fail the test if either is called.

    Expected outcome: exit 1; exactly one ERROR record, on one line, naming the scenario and
    the family's message word for word; neither stand-in called; no artifact written.
    """

    def never(*args: object, **kwargs: object) -> NoReturn:
        pytest.fail("the command went past the narrowing on a scenario of the cellular family")

    monkeypatch.setattr(json_output, "load_saturation_curve", never)
    monkeypatch.setattr(json_output, "run_iridium_model", never)
    scenario = tmp_path / "cellular.yaml"
    scenario.write_text("satellite:\n  satellites_per_launch: 12\n", encoding="utf-8")
    out_path = tmp_path / "out.json"

    assert main([str(scenario), str(out_path)]) == EXIT_ERROR

    errors = _errors(caplog)
    assert len(errors) == 1
    assert "\n" not in errors[0]
    assert errors[0] == f"could not promote {scenario}: {_NOT_AN_IRIDIUM_SCENARIO}"
    assert not out_path.exists()


def test_a_curve_computed_for_other_inputs_fails_the_command_naming_the_field(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Objective: the identity check runs inside the command: a scenario whose curve inputs
    differ from its curve's is refused before the run, naming the first field that differs.

    Sample: a scenario selecting the Iridium model at 10.5 MHz, its curve path the default (the
    committed curve, computed for the held spectrum the shipped scenario sets).

    Expected outcome: exit 1; exactly one ERROR record, on one line, naming the scenario and
    the mismatch at ``spectrum_mhz`` (10.5 for this run); no artifact written.
    """
    scenario = tmp_path / "coordinated.yaml"
    scenario.write_text("iridium:\n  spectrum_mhz: 10.5\n", encoding="utf-8")
    out_path = tmp_path / "out.json"

    assert main([str(scenario), str(out_path)]) == EXIT_ERROR

    errors = _errors(caplog)
    assert len(errors) == 1
    assert "\n" not in errors[0]
    assert errors[0].startswith(
        f"could not promote {scenario}: the saturation curve was computed for other inputs: "
        "spectrum_mhz is 10.5 for this run but "
    )
    assert not out_path.exists()


def test_a_missing_curve_fails_the_command_naming_the_curve(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Objective: a curve path that names no file is one clean error, never a traceback, and an
    absolute curve path is used as given.

    Sample: a scenario selecting the Iridium model whose ``iridium.saturation.curve_path`` is an
    absolute path in a temporary folder with no file there.

    Expected outcome: exit 1; exactly one ERROR record, on one line, naming the scenario, the
    curve's path and "file not found"; no artifact written.
    """
    absent = tmp_path / "absent_curve.json"
    scenario = tmp_path / "no_curve.yaml"
    scenario.write_text(f"iridium:\n  saturation:\n    curve_path: {absent}\n", encoding="utf-8")
    out_path = tmp_path / "out.json"

    assert main([str(scenario), str(out_path)]) == EXIT_ERROR

    errors = _errors(caplog)
    assert len(errors) == 1
    assert "\n" not in errors[0]
    assert errors[0] == f"could not promote {scenario}: {absent}: file not found"
    assert not out_path.exists()


def test_a_relative_curve_path_is_anchored_to_the_repository_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, iridium_yaml: Path, repo_dir: Path
) -> None:
    """Objective: the scenario's relative curve path is read from the repository root, whatever
    the working directory, as a relative output path is written there.

    Sample: the shipped scenario (its curve path ``communications/models/iridium/
    saturation_curve.json``), promoted from a temporary working directory, the command's curve
    loader wrapped to record the path it is given.

    Expected outcome: exit 0, the artifact written, and the curve read once, from the
    repository root's ``communications/models/iridium/saturation_curve.json``.
    """
    loaded: list[Path] = []
    load = json_output.load_saturation_curve

    def recording_load(path: Path) -> SaturationCurve:
        loaded.append(path)
        return load(path)

    monkeypatch.setattr(json_output, "load_saturation_curve", recording_load)
    monkeypatch.chdir(tmp_path)
    out_path = tmp_path / "iridium.json"

    assert main([str(iridium_yaml), str(out_path), "--version-stamp", "test"]) == EXIT_OK

    assert out_path.is_file()
    assert loaded == [repo_dir / _COMMITTED_CURVE]
