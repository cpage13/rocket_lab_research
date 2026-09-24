"""Tests for the ``rklb-value --promote`` flag.

The calculator has two output locations by design:

* ``code/outputs/data_center/runs/``: git-ignored scratch; ``--json`` is
  redirected there and rerun freely, each run carrying its own
  ``generated_at`` timestamp.
* ``data_center/models/space/`` and ``data_center/models/ground/``: the
  reviewed public artifacts, written only by ``--promote``.
* ``data_center/conclusion.md``: reviewed static prose, never overwritten.

These tests are the promotion contract:

1. the default promotion writes the space and ground artifacts (roles
   ``promoted_default`` / ``promoted_ground_default``), each ending in exactly
   one newline, and leaves the static conclusion alone;
2. a non-default scenario is promoted only under its own lowercase
   ``--output-name`` (role ``promoted_named``, no ground artifact), never as
   ``default`` in any spelling, and the default scenario only as ``default``
   (usage errors, ``EXIT_USAGE``); a mistyped scenario path is reported as a
   missing file;
3. a failing validation check refuses the promotion and writes nothing, and
   a default whose anchor-year cohort is empty (no ground reference can be
   built) is one clean error, not a traceback;
4. a write failure (a read-only ground directory, a failed second rename, a
   locked ground file) leaves both promoted artifacts exactly as they were,
   with no staged or backup file left behind, and the error line says so;
5. status lines are log records; stdout stays empty.

Every test passes ``models_dir`` (a temporary directory) to
:func:`data_center.cli.main`, so the suite never touches the committed
artifacts.
"""

from __future__ import annotations

import errno
import json
import logging
import os
import stat
from pathlib import Path

import pytest

from common.cadence import CadenceDials
from common.cli import EXIT_ERROR, EXIT_OK, EXIT_USAGE
from data_center import cli
from data_center.config import ValuationConfig
from data_center.constants import ANCHOR_MODEL_YEAR
from data_center.ground import GroundReferenceOutput
from data_center.output import SpaceModelOutput

_READ_ONLY_DIR_MODE = stat.S_IRUSR | stat.S_IXUSR
"""A directory the owner can list and enter but not write into."""

_ROOT_IGNORES_PERMISSIONS = os.geteuid() == 0
"""Root bypasses directory permissions and file flags, so those tests skip under root."""

_PREVIOUS_SPACE = b"previous space\n"
"""The bytes a pre-existing promoted space artifact holds before a failed promotion."""

_PREVIOUS_GROUND = b"previous ground\n"
"""The bytes a pre-existing promoted ground artifact holds before a failed promotion."""


def _promote(models_dir: Path, *args: str) -> int:
    """Run ``rklb-value <args> --promote`` against a temporary models directory."""
    return cli.main([*args, "--promote"], models_dir=models_dir)


def _errors(caplog: pytest.LogCaptureFixture) -> list[str]:
    """Return the messages of the captured ERROR (and worse) records."""
    return [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]


def _existing_default_pair(models_dir: Path) -> tuple[Path, Path]:
    """Create a promoted default pair with known previous content; return its paths."""
    space = models_dir / "space" / "default.json"
    ground = models_dir / "ground" / "default.json"
    space.parent.mkdir(parents=True)
    ground.parent.mkdir()
    space.write_bytes(_PREVIOUS_SPACE)
    ground.write_bytes(_PREVIOUS_GROUND)
    return space, ground


def _pair_is_untouched(space: Path, ground: Path) -> bool:
    """Whether both artifacts hold their previous bytes and nothing else sits beside them."""
    return (
        space.read_bytes() == _PREVIOUS_SPACE
        and ground.read_bytes() == _PREVIOUS_GROUND
        and [p.name for p in space.parent.iterdir()] == ["default.json"]
        and [p.name for p in ground.parent.iterdir()] == ["default.json"]
    )


def test_promote_writes_default_space_and_ground_artifacts(tmp_path: Path) -> None:
    """Objective: ``--promote`` publishes the default pair.

    Expected: exit 0; ``space/default.json`` round-trips as a
    ``promoted_default`` space artifact of the default scenario and
    ``ground/default.json`` as a ``promoted_ground_default`` reference; both
    end in exactly one newline (clean git diffs); the models directory is
    created when absent.
    """
    models_dir = tmp_path / "models"

    assert _promote(models_dir) == EXIT_OK

    space_text = (models_dir / "space" / "default.json").read_text(encoding="utf-8")
    ground_text = (models_dir / "ground" / "default.json").read_text(encoding="utf-8")
    space = SpaceModelOutput.model_validate(json.loads(space_text))
    ground = GroundReferenceOutput.model_validate(json.loads(ground_text))
    assert space.metadata.schema_version == "v9"
    assert ground.metadata.schema_version == "ground-v2"
    assert space.metadata.artifact_role == "promoted_default"
    assert space.inputs.scenario.is_default
    assert ground.metadata.artifact_role == "promoted_ground_default"
    for text in (space_text, ground_text):
        assert text.endswith("\n")
        assert not text.endswith("\n\n")


def test_promote_does_not_overwrite_static_conclusion(tmp_path: Path) -> None:
    """Objective: promotion writes JSON artifacts and leaves reviewed prose alone.

    Expected: with the models directory laid out as in the repository, the
    conclusion beside it is byte-for-byte unchanged after a promotion.
    """
    data_center_dir = tmp_path / "data_center"
    conclusion_path = data_center_dir / "conclusion.md"
    conclusion_path.parent.mkdir(parents=True)
    original_text = "# Static conclusion\n\nReviewed prose stays put.\n"
    conclusion_path.write_text(original_text, encoding="utf-8")

    assert _promote(data_center_dir / "models") == EXIT_OK

    assert (data_center_dir / "models" / "space" / "default.json").is_file()
    assert (data_center_dir / "models" / "ground" / "default.json").is_file()
    assert conclusion_path.read_text(encoding="utf-8") == original_text


def test_promote_publishes_a_named_scenario_under_its_output_name(tmp_path: Path) -> None:
    """Objective: a non-default scenario promotes under its own stem.

    Expected: ``less_mass.yaml --promote --output-name less_mass`` exits 0,
    writes ``space/less_mass.json`` with role ``promoted_named`` (the role
    follows the scenario, not the name), and writes no ground artifact.
    """
    models_dir = tmp_path / "models"
    scenario = tmp_path / "less_mass.yaml"
    scenario.write_text('scenario_name: "Less mass"\n', encoding="utf-8")

    assert _promote(models_dir, str(scenario), "--output-name", "less_mass") == EXIT_OK

    rebuilt = SpaceModelOutput.model_validate(
        json.loads((models_dir / "space" / "less_mass.json").read_text(encoding="utf-8"))
    )
    assert rebuilt.metadata.scenario_name == "Less mass"
    assert rebuilt.metadata.artifact_role == "promoted_named"
    assert not rebuilt.inputs.scenario.is_default
    assert not (models_dir / "ground").exists()


@pytest.mark.parametrize(
    ("scenario_name", "extra_args", "message"),
    [
        ("conservative", [], "is not the default scenario: pass --output-name"),
        ("conservative", ["--output-name", "default"], "the output name 'default' is reserved"),
        ("conservative", ["--output-name", "DEFAULT"], "'DEFAULT' is not a valid output name"),
        ("conservative", ["--output-name", "Default"], "'Default' is not a valid output name"),
        ("conservative", ["--output-name", "Less_Mass"], "'Less_Mass' is not a valid output name"),
        ("default", ["--output-name", "copy"], "the default scenario is promoted only as"),
        (None, ["--output-name", "../bad"], "'../bad' is not a valid output name"),
    ],
    ids=[
        "non_default_unnamed",
        "non_default_as_default",
        "non_default_as_upper_default",
        "non_default_as_title_default",
        "mixed_case_name",
        "default_renamed",
        "path_like_name",
    ],
)
def test_promote_rejects_a_name_that_misstates_the_scenario(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    scenarios_dir: Path,
    scenario_name: str | None,
    extra_args: list[str],
    message: str,
) -> None:
    """Objective: ``default.json`` is written only for the default scenario.

    The original triggers: ``conservative.yaml --promote`` exited 0 and
    overwrote both default artifacts with the conservative run; then, on a
    case-insensitive file system (APFS), ``--output-name DEFAULT`` reached
    ``default.json`` past the case-sensitive reserved-name check. Expected:
    an unnamed non-default scenario, the name ``default`` in any spelling,
    any uppercase or path-like name, and the default scenario under another
    name are usage errors (``EXIT_USAGE``) naming the problem; an existing
    default pair keeps its exact content and nothing else is written.
    """
    models_dir = tmp_path / "models"
    space, ground = _existing_default_pair(models_dir)
    scenario_args = [] if scenario_name is None else [str(scenarios_dir / f"{scenario_name}.yaml")]

    with pytest.raises(SystemExit) as excinfo:
        _promote(models_dir, *scenario_args, *extra_args)

    assert excinfo.value.code == EXIT_USAGE
    assert message in capsys.readouterr().err
    assert _pair_is_untouched(space, ground)


def test_promote_reports_a_mistyped_scenario_path_as_missing(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, scenarios_dir: Path
) -> None:
    """Objective: a typo is reported as the missing file it is.

    Expected: ``scenarios/defualt.yaml --promote`` exits 1 with one error
    record saying the file was not found (not a usage error about the output
    name), naming the path once, and writes nothing.
    """
    models_dir = tmp_path / "models"
    typo = scenarios_dir / "defualt.yaml"

    assert _promote(models_dir, str(typo)) == EXIT_ERROR

    assert _errors(caplog) == ["could not load code/scenarios/defualt.yaml: file not found"]
    assert not models_dir.exists()


def test_promote_refuses_a_scenario_with_a_failing_validation_check(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, scenarios_dir: Path
) -> None:
    """Objective: a failing validation check blocks promotion.

    ``volume_stress.yaml`` fails the major ``volume_fits_horizon`` rule by
    design. Expected: promoting it exits 1 with one error record naming the
    failing check, and writes nothing.
    """
    models_dir = tmp_path / "models"
    scenario = str(scenarios_dir / "volume_stress.yaml")

    exit_code = _promote(models_dir, scenario, "--output-name", "volume_stress")

    assert exit_code == EXIT_ERROR
    errors = _errors(caplog)
    assert len(errors) == 1
    assert "refusing to promote" in errors[0]
    assert "volume_fits_horizon" in errors[0]
    assert not models_dir.exists()


def test_an_empty_anchor_cohort_fails_promotion_with_one_clean_error(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Objective: a default that deploys nothing in its anchor year fails cleanly.

    The original trigger: the default scenario with its first launch after the
    anchor year (``cadence.first_launch_year: 11``) deploys no node in FY2036,
    the ground reference's per-package cells came out None, and ``--promote``
    ended in a TypeError traceback. Expected: exit 1 with exactly one error
    record, ``could not promote code/scenarios/default.yaml:`` naming the empty
    anchor cohort, no warning, and nothing written.
    """
    load_default = cli.load_config

    def load_with_no_launch_in_the_window(path: str | Path) -> ValuationConfig:
        config = load_default(path)
        cadence = CadenceDials.model_validate(
            {**config.cadence.model_dump(), "first_launch_year": ANCHOR_MODEL_YEAR + 1}
        )
        return config.model_copy(update={"cadence": cadence})

    monkeypatch.setattr(cli, "load_config", load_with_no_launch_in_the_window)
    models_dir = tmp_path / "models"

    assert _promote(models_dir) == EXIT_ERROR

    errors = _errors(caplog)
    assert len(errors) == 1
    assert errors[0].startswith("could not promote code/scenarios/default.yaml: ")
    assert "anchor-year cohort (FY2036) is empty" in errors[0]
    assert not [r for r in caplog.records if r.levelno == logging.WARNING]
    assert not models_dir.exists()


@pytest.mark.skipif(_ROOT_IGNORES_PERMISSIONS, reason="root ignores directory permissions")
def test_a_read_only_ground_directory_leaves_both_artifacts_untouched(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Objective: a staging failure changes neither artifact.

    The original trigger: with a read-only ground directory, the space
    artifact was overwritten, then the ground write raised a PermissionError
    traceback. Expected: exit 1 with one error record naming the ground path
    and saying no destination was changed; both artifacts keep their exact
    content and no staged or backup file is left in either directory.
    """
    models_dir = tmp_path / "models"
    space, ground = _existing_default_pair(models_dir)
    ground.parent.chmod(_READ_ONLY_DIR_MODE)
    try:
        exit_code = _promote(models_dir)
    finally:
        ground.parent.chmod(stat.S_IRWXU)

    assert exit_code == EXIT_ERROR
    errors = _errors(caplog)
    assert len(errors) == 1
    assert f"{ground}: could not write (" in errors[0]
    assert errors[0].endswith("no destination was changed")
    assert _pair_is_untouched(space, ground)


def test_a_failed_ground_rename_restores_the_space_artifact(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Objective: the pair is promoted or put back, and the message is true.

    The original trigger: when the ground rename failed after the space
    rename succeeded, the space artifact stayed replaced while the log said
    "no promoted artifact was changed". Expected: with the ground rename
    failing (injected EIO), exit 1 with one error record that names the
    ground path, says the space artifact was restored and no destination
    remains changed; both artifacts are byte-identical to their previous
    content and no staged or backup file remains.
    """
    models_dir = tmp_path / "models"
    space, ground = _existing_default_pair(models_dir)
    real_replace = os.replace

    def replace(src: str | os.PathLike[str], dst: str | os.PathLike[str]) -> None:
        if Path(dst) == ground and Path(src).suffix == ".tmp":
            raise OSError(errno.EIO, "injected failure")
        real_replace(src, dst)

    monkeypatch.setattr(os, "replace", replace)

    assert _promote(models_dir) == EXIT_ERROR

    errors = _errors(caplog)
    assert len(errors) == 1
    assert f"{ground}: could not replace the file (injected failure)" in errors[0]
    assert errors[0].endswith(
        f"restored the previous state of {space}; no destination remains changed"
    )
    assert "no promoted artifact was changed" not in errors[0]
    assert _pair_is_untouched(space, ground)


@pytest.mark.skipif(
    not hasattr(os, "chflags") or _ROOT_IGNORES_PERMISSIONS,
    reason="needs BSD file flags (macOS) and a non-root user",
)
def test_a_locked_ground_artifact_leaves_both_artifacts_untouched(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Objective: the natural macOS trigger (``chflags uchg``) rolls back cleanly.

    Expected: with the ground artifact immutable, exit 1 with one error
    record naming it and saying the space artifact was restored; both
    artifacts are byte-identical to their previous content and no staged or
    backup file remains.
    """
    models_dir = tmp_path / "models"
    space, ground = _existing_default_pair(models_dir)
    os.chflags(ground, stat.UF_IMMUTABLE)
    try:
        exit_code = _promote(models_dir)
    finally:
        os.chflags(ground, 0)

    assert exit_code == EXIT_ERROR
    errors = _errors(caplog)
    assert len(errors) == 1
    assert f"{ground}: could not replace the file (" in errors[0]
    assert errors[0].endswith(
        f"restored the previous state of {space}; no destination remains changed"
    )
    assert _pair_is_untouched(space, ground)


def test_promotion_status_goes_to_the_log_not_stdout(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture
) -> None:
    """Objective: stdout carries only product output; promotion prints none.

    Expected: a successful promotion leaves stdout empty and logs one INFO
    record per written artifact, naming its path.
    """
    models_dir = tmp_path / "models"
    caplog.set_level(logging.INFO, logger="data_center.cli")

    assert _promote(models_dir) == EXIT_OK

    assert capsys.readouterr().out == ""
    status = [r.getMessage() for r in caplog.records if r.name == "data_center.cli"]
    assert status == [
        f"promoted {models_dir / 'space' / 'default.json'}",
        f"promoted {models_dir / 'ground' / 'default.json'}",
    ]
