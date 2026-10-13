"""Tests for the Iridium promotion command: its failure handling, its output streams and the
artifact's coverage of the run's records.

``python -m communications.json_output <scenario> <output>`` follows the shared
command-line conventions (``common.cli``) and writes its one artifact through
the shared writer (``common.file_io.write_files_with_rollback``). The contract:

1. a malformed scenario, an unwritable destination, a value the model cannot
   compute or an artifact that would hold a number that is not finite is one
   error record and exit status 1, never a traceback (and never a promoted
   artifact with a null cost); a run that would hold such a number is refused
   by the Iridium entry, the error naming the first such field and the
   settings behind it;
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
   inputs (the identity check), is one error record naming the curve file, and
   nothing is written; a final year's fleet past the fleet a class with no
   saturation number is not reached by is one error record naming the class,
   that label and the fleet, and nothing is written;
6. no field of the run's Iridium record can stay unpublished silently: each record the
   artifact publishes whole and its block carry the same fields in the same order, each year's
   Iridium lines sit in the year block, every field of the Iridium record has its home in the
   artifact, and every artifact field is required, so a field the writer forgets to map fails
   the build instead of publishing a default.
"""

from __future__ import annotations

import errno
import json
import logging
import os
import stat
from collections.abc import Callable
from dataclasses import fields
from pathlib import Path
from typing import Final, NoReturn, get_args

import pytest
from pydantic import BaseModel

from common.cli import EXIT_ERROR, EXIT_OK
from common.file_io import ARTIFACT_FILE_END, render_artifact_json
from communications import json_output
from communications.config import IridiumArpuDials, IridiumDials
from communications.constants import BASE_YEAR_DEFAULT, SATURATION_CURVE_PATH_DEFAULT
from communications.iridium import (
    ClassReadingRecord,
    ClassRecord,
    ClassYearRecord,
    IotClassCapacityRecord,
    IotClassRecord,
    IotRoomRecord,
    IridiumRecord,
    MarginalIntervalRecord,
    ReadingRecord,
    SaturationRecord,
    YearRecord,
)
from communications.json_output import (
    ClassBlock,
    ClassReadingBlock,
    ClassYearBlock,
    IotClassBlock,
    IotClassCapacityBlock,
    IotRoomBlock,
    IridiumModelArtifact,
    MarginalIntervalBlock,
    ReadingBlock,
    SaturationBlock,
    YearBlock,
    main,
)
from communications.saturation_curve import SaturationCurve

_NOT_AN_IRIDIUM_SCENARIO = (
    "the scenario does not select the Iridium model: it needs a top-level "
    "'iridium:' block (see scenarios/iridium.yaml)"
)
"""The family's refusal, word for word the command's message before the narrowing function."""

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


@pytest.mark.parametrize(
    ("iridium_dials", "reason"),
    [
        ("aperture_m2: 1.0e+308", "a value the model cannot compute ("),
        (
            "aperture_m2: 1.0e-323",
            "iridium.aperture_m2 (1e-323 m^2) over the saturation curve's reference panel (25.0 "
            "m^2) gives a panel factor of 0.0; it must be a positive finite number",
        ),
    ],
    ids=["a panel too large", "a panel so small its factor underflows to zero"],
)
def test_a_value_the_model_cannot_compute_is_one_error_line(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, iridium_dials: str, reason: str
) -> None:
    """Objective: a finite dial the model cannot compute with ends the command in one error
    record, never a traceback (before the fix the run's ``OverflowError``, and a
    ``ZeroDivisionError``, escaped as one).

    Sample: a scenario selecting the Iridium model with a panel of 1.0e308 m^2 (the people at a
    fleet overflow to infinity and cannot become a count), and one with a panel of 1.0e-323 m^2
    (its ratio to the reference panel underflows to zero, which the Iridium entry refuses,
    naming the setting); both finite, so both load, and neither is an input of the curve, so
    the identity check passes. (The one-usage dial whose product underflowed is retired.)

    Expected outcome: exit 1; exactly one ERROR record, on one line and with no exception
    attached, naming the scenario and the reason (a value the model cannot compute; the panel
    factor named with ``iridium.aperture_m2``); no artifact written.
    """
    scenario = tmp_path / "cannot_compute.yaml"
    scenario.write_text(f"iridium:\n  {iridium_dials}\n", encoding="utf-8")
    out_path = tmp_path / "out.json"

    assert main([str(scenario), str(out_path)]) == EXIT_ERROR

    records = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert len(records) == 1
    message = records[0].getMessage()
    assert "\n" not in message
    assert message.startswith(f"could not promote {scenario}: {reason}")
    assert records[0].exc_info is None
    assert not out_path.exists()


@pytest.mark.parametrize(
    ("shared_block", "named"),
    [
        (
            "satellite:\n  satellite_build_cost_musd: 1.0e+308",
            "the run's fleet.years[2].build_cost_this_year_musd is inf, not a finite number: "
            "the fleet-and-cost record scales with satellite.satellite_build_cost_musd (1e+308)",
        ),
        (
            "launch_cost:\n  high_cadence_cost_musd: .inf",
            "launch_cost.high_cadence_cost_musd: Input should be a finite number",
        ),
    ],
    ids=["a build cost that overflows", "an infinite launch cost in the common block"],
)
def test_an_artifact_never_holds_a_number_that_is_not_finite(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, shared_block: str, named: str
) -> None:
    """Objective: the command never writes an artifact whose numbers are not finite (before the
    fix such a run promoted, exit 0, with its cost fields written as null), and its one error
    line names the setting: the Iridium entry refuses a run that would hold one, naming the
    first such field and the settings behind it (the artifact's models refuse one too, whatever
    route made it).

    Sample: an Iridium scenario with a satellite build cost of 1.0e308 $M (finite, so it loads;
    the run's costs overflow to infinity, which the entry refuses), and one with an infinite
    launch cost in the ``launch_cost`` block, which ``common.cadence`` defines and the
    data-center model shares (refused at load, naming the field, before any run).

    Expected outcome: exit 1; exactly one ERROR record, on one line, naming the scenario and a
    number that is not finite: for the build cost, the fleet-and-cost record's first such field
    and the build cost with its value; for the launch cost, the field; no artifact written.
    """
    scenario = tmp_path / "not_finite_artifact.yaml"
    scenario.write_text(f"{shared_block}\niridium: {{}}\n", encoding="utf-8")
    out_path = tmp_path / "out.json"

    assert main([str(scenario), str(out_path)]) == EXIT_ERROR

    records = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert len(records) == 1
    message = records[0].getMessage()
    assert "\n" not in message
    assert message.startswith(f"could not promote {scenario}: ")
    assert named in message
    assert not out_path.exists()


def test_a_run_that_would_hold_a_number_that_is_not_finite_names_the_panel(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Objective: when an absurd panel puts a number that is not finite in the run, the
    command's one error line names the setting a reader can change (before the fix it named the
    artifact field the artifact's models refused, an invalid class-year block's
    ``revenue_musd``, and not the setting).

    Sample: an Iridium scenario with a panel of 2.5e300 m^2 (finite, so it loads; the people
    stay finite and the IoT room's uplink bits a second overflow to infinity, first in FY2028,
    whose 12 satellites at the defaults' 0.18 share are the first fleet; re-derived by running
    it, 2026-10-13).

    Expected outcome: exit 1; exactly one ERROR record, on one line and with no exception
    attached, naming the scenario, the first field that is not finite and
    ``iridium.aperture_m2`` with its value beside the three prices; no artifact written.
    """
    scenario = tmp_path / "huge_panel.yaml"
    scenario.write_text("iridium:\n  aperture_m2: 2.5e+300\n", encoding="utf-8")
    out_path = tmp_path / "out.json"

    assert main([str(scenario), str(out_path)]) == EXIT_ERROR

    records = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert len(records) == 1
    message = records[0].getMessage()
    assert "\n" not in message
    assert message.startswith(
        f"could not promote {scenario}: the run's "
        "iridium.years[2].iot.uplink_bits_per_second is inf, not a finite number: "
        "the Iridium record scales with iridium.aperture_m2 (2.5e+300), "
    )
    for name in IridiumArpuDials.model_fields:
        assert f"iridium.arpu.{name} (" in message
    assert records[0].exc_info is None
    assert not out_path.exists()


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


def test_a_curve_computed_for_other_inputs_fails_the_command_naming_the_curve_and_the_field(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, repo_dir: Path
) -> None:
    """Objective: the identity check runs inside the command: a scenario whose curve inputs
    differ from its curve's is refused before the run, naming the curve file its curve path
    resolved to (as the loader's refusals name their file) and the first field that differs.

    Sample: a scenario selecting the Iridium model at 10.5 MHz, its curve path the default (the
    committed curve, computed for the held spectrum the shipped scenario sets), so it resolves
    under the repository root.

    Expected outcome: exit 1; exactly one ERROR record, on one line, naming the scenario, the
    resolved curve file and the mismatch at ``spectrum_mhz`` (10.5 for this run); no artifact
    written.
    """
    scenario = tmp_path / "coordinated.yaml"
    scenario.write_text("iridium:\n  spectrum_mhz: 10.5\n", encoding="utf-8")
    out_path = tmp_path / "out.json"

    assert main([str(scenario), str(out_path)]) == EXIT_ERROR

    errors = _errors(caplog)
    assert len(errors) == 1
    assert "\n" not in errors[0]
    assert errors[0].startswith(
        f"could not promote {scenario}: {repo_dir / SATURATION_CURVE_PATH_DEFAULT}: the "
        "saturation curve was computed for other inputs: spectrum_mhz is 10.5 for this run but "
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
    repository root's ``communications/models/iridium/saturation_curve.json`` (the default
    curve path, ``SATURATION_CURVE_PATH_DEFAULT``).
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
    assert loaded == [repo_dir / SATURATION_CURVE_PATH_DEFAULT]


def test_a_scenario_runs_on_a_curve_computed_for_its_inputs(
    tmp_path: Path, synthetic_saturation_curve: Callable[[IridiumDials], SaturationCurve]
) -> None:
    """Objective: a held spectrum the committed curve was not computed for promotes once the
    scenario's curve path names a curve computed for it (an absolute path, used as given).

    Sample: a synthetic curve stamped for the Iridium dials at 10.5 MHz, written as the
    promotion writes a curve to a temporary folder; a scenario at 10.5 MHz whose
    ``iridium.saturation.curve_path`` is that file's absolute path.

    Expected outcome: exit 0 and the artifact written, its physics at 10.5 MHz and the phone
    class's satellite peak at the default 15.4 m^2 panel, 0.630630 Gbps (10.5 x 0.65 x 0.15 x
    0.616).
    """
    curve_path = tmp_path / "coordinated_curve.json"
    curve = synthetic_saturation_curve(IridiumDials(spectrum_mhz=10.5))
    curve_path.write_text(render_artifact_json(curve) + ARTIFACT_FILE_END, encoding="utf-8")
    scenario = tmp_path / "coordinated.yaml"
    scenario.write_text(
        f"iridium:\n  spectrum_mhz: 10.5\n  saturation:\n    curve_path: {curve_path}\n",
        encoding="utf-8",
    )
    out_path = tmp_path / "coordinated.json"

    assert main([str(scenario), str(out_path), "--version-stamp", "test"]) == EXIT_OK

    payload = json.loads(out_path.read_text(encoding="utf-8"))
    assert payload["iridium_physics"]["spectrum_mhz"] == 10.5
    phone = payload["classes"][2]
    assert phone["device_class"] == "phone_class"
    assert phone["per_satellite_capacity_gbps"] == pytest.approx(10.5 * 0.65 * 0.15 * 0.616)


PAST_LABEL_HORIZON_YEARS = 30
"""The horizon of the run whose final fleet passes a no-number class's label (with the shipped
scenario's all-in share and 16 satellites per launch, and the life below, its final year's
living fleet is 38,160: past the synthetic curve's 36,900, inside its 40,000 last row, at the
reported fleets too)."""

PAST_LABEL_SATELLITE_LIFETIME_YEARS = 16
"""That run's satellite life, years."""

PAST_LABEL_SCENARIO = (
    "metadata:\n"
    f"  base_year: {BASE_YEAR_DEFAULT}\n"
    f"  horizon_years: {PAST_LABEL_HORIZON_YEARS}\n"
    "comms_cadence:\n"
    "  share_of_fleet: 1.0\n"
    "satellite:\n"
    "  satellites_per_launch: 16\n"
    f"  satellite_lifetime_years: {PAST_LABEL_SATELLITE_LIFETIME_YEARS}\n"
    "iridium:\n"
    "  saturation:\n"
    "    curve_path: {curve_path}\n"
)
"""That run's scenario, its curve path to be filled in: the shipped scenario's all-in share
(1.0) and 16 satellites per launch, at that horizon and life."""


def test_a_final_fleet_past_a_no_number_classs_label_is_one_error_line(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
    synthetic_saturation_curve: Callable[[IridiumDials], SaturationCurve],
) -> None:
    """Objective: a run whose final year's living fleet passes the fleet a class with no
    saturation number is not reached by ends the command in one ERROR line, never a traceback,
    naming the class, that label and the fleet: the curve does not measure the elasticity of
    capacity past the label, so which limit binds there is not known (ADR 005).

    Sample: the synthetic curve for the default dials (no saturation number on any class; the
    small terminal not reached by 36,900, its last row 40,000), written as the promotion writes
    a curve; a scenario naming it, at the shipped all-in share and 16 satellites per launch over
    a 30-year horizon with a 16-year satellite life, so the final year's living fleet is 38,160.

    Expected outcome: exit 1; exactly one ERROR record, on one line and with no exception
    attached, naming the scenario, the small terminal's curve, 36,900 and 38,160; no artifact
    written.
    """
    curve_path = tmp_path / "synthetic_curve.json"
    curve = synthetic_saturation_curve(IridiumDials())
    curve_path.write_text(render_artifact_json(curve) + ARTIFACT_FILE_END, encoding="utf-8")
    scenario = tmp_path / "past_label.yaml"
    scenario.write_text(PAST_LABEL_SCENARIO.format(curve_path=curve_path), encoding="utf-8")
    out_path = tmp_path / "past_label.json"

    assert main([str(scenario), str(out_path)]) == EXIT_ERROR

    records = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert len(records) == 1
    message = records[0].getMessage()
    assert "\n" not in message
    assert message.startswith(
        f"could not promote {scenario}: the small_terminal_class curve reaches no saturation "
        "number and is not reached by 36900 satellites"
    )
    assert "the final year's living fleet of 38160 satellites lies past it" in message
    assert records[0].exc_info is None
    assert not out_path.exists()


# --------------------------------------------------------------------------
# Every field of the run's records reaches the artifact (contract item 6)
# --------------------------------------------------------------------------

_RECORDS_AND_BLOCKS: Final[tuple[tuple[type, type[BaseModel]], ...]] = (
    (ClassRecord, ClassBlock),
    (MarginalIntervalRecord, MarginalIntervalBlock),
    (ClassYearRecord, ClassYearBlock),
    (ReadingRecord, ReadingBlock),
    (ClassReadingRecord, ClassReadingBlock),
    (IotRoomRecord, IotRoomBlock),
    (IotClassCapacityRecord, IotClassCapacityBlock),
    (IotClassRecord, IotClassBlock),
    (SaturationRecord, SaturationBlock),
)
"""Each Iridium record the artifact publishes whole, beside the block the writer maps it onto
field for field."""

_IRIDIUM_RECORD_HOMES: Final[dict[str, str | None]] = {
    "scenario_name": "provenance",
    "spectrum_mhz": "iridium_physics",
    "aperture_m2": "iridium_physics",
    "satellites_per_launch": "iridium_physics",
    "operations_cost_musd": "iridium_physics",
    "ecosystem_assumption": "iridium_physics",
    "coverage_floor_reached_year": "trajectory_summary",
    "cost_per_satellite_year_musd": "trajectory_summary",
    "classes": None,
    "iot_classes": None,
    "years": None,
    "saturation": None,
    "assumptions": None,
}
"""Where each field of the Iridium record is published, under its own name: the artifact's
block that holds it, or None for a field of the artifact's top level."""


def _types_in(annotation: object) -> list[object]:
    """Return an annotation and every type argument inside it, depth first."""
    return [annotation, *(inner for arg in get_args(annotation) for inner in _types_in(arg))]


def _blocks_under(model: type[BaseModel]) -> list[type[BaseModel]]:
    """Return ``model`` and every block model its fields reach, each once, in the order found."""
    found = [model]
    index = 0
    while index < len(found):
        for info in found[index].model_fields.values():
            for inner in _types_in(info.annotation):
                if isinstance(inner, type) and issubclass(inner, BaseModel) and inner not in found:
                    found.append(inner)
        index += 1
    return found


@pytest.mark.parametrize(
    ("record", "block"),
    _RECORDS_AND_BLOCKS,
    ids=[record.__name__ for record, _ in _RECORDS_AND_BLOCKS],
)
def test_each_record_and_its_block_carry_the_same_fields_in_the_same_order(
    record: type, block: type[BaseModel]
) -> None:
    """Objective: a field added to one of the Iridium records the artifact publishes whole
    cannot stay unpublished silently, since the regeneration test compares only what is
    published: the block the writer maps the record onto carries the record's every field,
    under the same name and in the same order (the artifact's key order), and no other.

    Sample: the nine record and block pairs the writer maps field for field (classes and their
    intervals, each year's class lines, the readings and their class lines, IoT's room and each
    IoT class's capacity in it, each IoT class's engineering usage, the saturation block).

    Expected outcome: the record's field names, in order, equal the block's.
    """
    assert [field.name for field in fields(record)] == list(block.model_fields)


def test_every_field_of_the_iridium_record_and_its_years_reaches_the_artifact() -> None:
    """Objective: the Iridium record's own fields, and each year's Iridium lines, are published
    too: none can be added without a home in the artifact.

    Sample: the Iridium record's thirteen fields and their homes (``_IRIDIUM_RECORD_HOMES``,
    ``iot_classes`` a field of the artifact's top level); the year record's fields against the
    year block, which also carries the shared record's launches, living fleet and annualized
    cost beside them.

    Expected outcome: the homes name exactly the Iridium record's fields; each home is a field
    of the artifact's top level, or of the block it names, under the same name; every field of
    the year record is a field of the year block.
    """
    assert set(_IRIDIUM_RECORD_HOMES) == {field.name for field in fields(IridiumRecord)}
    top_level = IridiumModelArtifact.model_fields
    for name, block in _IRIDIUM_RECORD_HOMES.items():
        if block is None:
            assert name in top_level, name
            continue
        holder = top_level[block].annotation
        assert isinstance(holder, type), block
        assert issubclass(holder, BaseModel), block
        assert name in holder.model_fields, f"{block}.{name}"
    assert {field.name for field in fields(YearRecord)} <= set(YearBlock.model_fields)


def test_every_artifact_field_is_required_so_a_field_left_unmapped_fails_the_build() -> None:
    """Objective: the writer maps each record onto its block by name, so a field it forgets
    must fail the artifact's construction rather than publish a default: no field of the
    artifact, or of any block under it, has a default.

    Sample: the artifact model and every block model its fields reach, walked through their
    annotations (tuples, unions and dictionaries included), the three IoT blocks among them.

    Expected outcome: the walk reaches exactly the block models ``json_output`` defines (so no
    block escapes the check), and every field of each is required.
    """
    blocks = _blocks_under(IridiumModelArtifact)
    defined = {
        value
        for value in vars(json_output).values()
        if isinstance(value, type)
        and issubclass(value, BaseModel)
        and value.__module__ == json_output.__name__
    }
    assert set(blocks) == defined
    with_a_default = [
        f"{block.__name__}.{name}"
        for block in blocks
        for name, info in block.model_fields.items()
        if not info.is_required()
    ]
    assert with_a_default == []
