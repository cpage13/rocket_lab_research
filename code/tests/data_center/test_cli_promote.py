"""Tests for the ``rklb-value --promote`` flag.

The calculator has two output locations by design:

* ``code/outputs/data_center/runs/`` — git-ignored scratch; ``--json`` is
  redirected there and rerun freely, each run carrying its own
  ``generated_at`` timestamp.
* ``data_center/models/space/`` — reviewed public space-model JSON artifacts.
* ``data_center/conclusion.md`` — reviewed static prose, not overwritten by
  promotion.

``--promote`` is the only command that writes the public artifacts. These
tests guard that contract:

1. ``--promote`` returns exit code 0 and creates the JSON artifact
   (including the parent directory if absent);
2. the written file is the same valid v8 artifact the ``--json`` path
   emits for ``scenarios/default.yaml`` — it round-trips through
   :class:`data_center.output.ValuationOutput`; and
3. promotion leaves the static conclusion untouched; and
4. the JSON file ends with exactly one trailing newline (clean git diffs).

Every test monkeypatches :data:`data_center.cli._PROMOTED_MODEL_DIR` to a
temp path, so the suite never touches the committed artifacts on disk.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_center import cli
from data_center.output import ValuationOutput


def test_promote_writes_default_space_model(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """``--promote`` returns 0 and writes a valid default space artifact.

    Redirects the promoted-artifact directory into a temp directory that
    does not yet exist, proving ``--promote`` creates the parent directory
    and writes the default scenario as a round-trippable v8 output.
    """
    model_dir = tmp_path / "models"
    monkeypatch.setattr(cli, "_PROMOTED_MODEL_DIR", model_dir)

    exit_code = cli.main(["--promote"])

    assert exit_code == 0
    model_path = model_dir / "default.json"
    conclusion_path = tmp_path / "conclusion.md"
    assert model_path.is_file()
    assert not conclusion_path.exists()
    rebuilt = ValuationOutput.model_validate(json.loads(model_path.read_text()))
    assert rebuilt.metadata.schema_version == "v8"
    assert rebuilt.metadata.artifact_role == "promoted_default"


def test_promoted_files_end_with_single_newline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The promoted files end with exactly one trailing newline.

    A single trailing newline keeps the git-tracked artifacts' diffs clean;
    a missing or doubled newline would churn the diff.
    """
    model_dir = tmp_path / "models"
    monkeypatch.setattr(cli, "_PROMOTED_MODEL_DIR", model_dir)

    cli.main(["--promote"])

    text = (model_dir / "default.json").read_text()
    assert text.endswith("\n")
    assert not text.endswith("\n\n")


def test_promote_does_not_overwrite_static_conclusion(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """``--promote`` writes JSON artifacts and leaves reviewed prose alone."""
    project_dir = tmp_path / "project"
    conclusion_path = project_dir / "data_center" / "conclusion.md"
    conclusion_path.parent.mkdir(parents=True)
    original_text = "# Static conclusion\n\nReviewed prose stays put.\n"
    conclusion_path.write_text(original_text, encoding="utf-8")

    monkeypatch.setattr(cli, "_PROJECT_DIR", project_dir)
    monkeypatch.setattr(
        cli,
        "_PROMOTED_MODEL_DIR",
        project_dir / "data_center" / "models" / "space",
    )

    exit_code = cli.main(["--promote"])

    assert exit_code == 0
    assert (project_dir / "data_center" / "models" / "space" / "default.json").is_file()
    assert (project_dir / "data_center" / "models" / "ground" / "default.json").is_file()
    assert conclusion_path.read_text(encoding="utf-8") == original_text


def test_promote_uses_custom_config_and_output_name(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """``--promote`` can publish a named scenario artifact.

    The default promotion publishes ``models/space/default.json``. A custom
    output name publishes ``models/space/<name>.json`` and leaves static docs
    alone.
    """
    model_dir = tmp_path / "models"
    scenario = tmp_path / "less_mass.yaml"
    scenario.write_text('scenario_name: "Less mass"\n', encoding="utf-8")
    monkeypatch.setattr(cli, "_PROMOTED_MODEL_DIR", model_dir)

    exit_code = cli.main([str(scenario), "--promote", "--output-name", "less_mass"])

    assert exit_code == 0
    model_path = model_dir / "less_mass.json"
    assert model_path.is_file()
    assert not (tmp_path / "conclusion_less_mass.md").exists()
    rebuilt = ValuationOutput.model_validate(json.loads(model_path.read_text()))
    assert rebuilt.metadata.scenario_name == "Less mass"
    assert rebuilt.metadata.artifact_role == "promoted_named"


def test_promote_rejects_unsafe_output_name(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """``--output-name`` is a file stem, not a path."""
    monkeypatch.setattr(cli, "_PROMOTED_MODEL_DIR", tmp_path / "models")

    exit_code = cli.main(["--promote", "--output-name", "../bad"])

    assert exit_code == 1
