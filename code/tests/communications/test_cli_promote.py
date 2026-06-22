"""Tests for the rklb-comms CLI: the dual-promote, the schema, and the run paths.

The promote tests monkeypatch the promoted directories to a temp path so the
suite never touches the committed default artifacts.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from communications import cli
from communications.ground import GroundReferenceOutput
from communications.output import CommsModelOutput


def _patch_promote_dirs(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> tuple[Path, Path]:
    """Redirect the promoted space/ground dirs to temp paths and return them."""
    space_dir = tmp_path / "space"
    ground_dir = tmp_path / "ground"
    monkeypatch.setattr(cli, "_PROMOTED_SPACE_DIR", space_dir)
    monkeypatch.setattr(cli, "_PROMOTED_GROUND_DIR", ground_dir)
    return space_dir, ground_dir


def test_promote_writes_default_space_and_ground(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The dual-promote writes both artifacts, round-tripping, and not the conclusion."""
    space_dir, ground_dir = _patch_promote_dirs(monkeypatch, tmp_path)
    assert cli.main(["--promote"]) == 0

    space_file = space_dir / "default.json"
    ground_file = ground_dir / "default.json"
    assert space_file.exists()
    assert ground_file.exists()

    space = CommsModelOutput.model_validate(json.loads(space_file.read_text(encoding="utf-8")))
    assert space.metadata.schema_version == "comms-v1"
    assert space.metadata.artifact_role == "promoted_default"
    ground = GroundReferenceOutput.model_validate(
        json.loads(ground_file.read_text(encoding="utf-8"))
    )
    assert ground.metadata.schema_version

    assert not (tmp_path / "conclusion.md").exists()


def test_promoted_space_meta_is_enriched(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """The promoted space JSON carries the enriched meta scaffold."""
    space_dir, _ = _patch_promote_dirs(monkeypatch, tmp_path)
    assert cli.main(["--promote"]) == 0
    meta = json.loads((space_dir / "default.json").read_text(encoding="utf-8"))["meta"]
    assert meta["data_dictionary"]
    assert meta["formula_definitions"]
    assert meta["validation_results"]
    assert meta["query_examples"]


def test_promoted_files_end_with_single_newline(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Both promoted files end with exactly one trailing newline (clean git diffs)."""
    space_dir, ground_dir = _patch_promote_dirs(monkeypatch, tmp_path)
    assert cli.main(["--promote"]) == 0
    for path in (space_dir / "default.json", ground_dir / "default.json"):
        text = path.read_text(encoding="utf-8")
        assert text.endswith("\n")
        assert not text.endswith("\n\n")


def test_promote_is_deterministic(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Two promotes differ only in metadata.generated_at."""
    space_dir, ground_dir = _patch_promote_dirs(monkeypatch, tmp_path)
    assert cli.main(["--promote"]) == 0
    space_a = (space_dir / "default.json").read_text(encoding="utf-8")
    ground_a = (ground_dir / "default.json").read_text(encoding="utf-8")
    assert cli.main(["--promote"]) == 0
    space_b = (space_dir / "default.json").read_text(encoding="utf-8")
    ground_b = (ground_dir / "default.json").read_text(encoding="utf-8")

    def _strip_generated_at(blob: str) -> dict[str, object]:
        data = json.loads(blob)
        data["metadata"]["generated_at"] = "<stripped>"
        return data

    assert _strip_generated_at(space_a) == _strip_generated_at(space_b)
    assert _strip_generated_at(ground_a) == _strip_generated_at(ground_b)


def test_cli_default_brief_and_json(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """--brief prints one line; --json prints a five-key enriched object."""
    assert cli.main(["--default", "--brief"]) == 0
    brief = capsys.readouterr().out
    assert brief.strip()
    assert "\n" not in brief.strip()

    assert cli.main(["--default", "--json"]) == 0
    parsed = json.loads(capsys.readouterr().out)
    assert sorted(parsed.keys()) == ["business", "inputs", "meta", "metadata", "physical"]
    assert parsed["meta"]["data_dictionary"]


def test_cli_input_schema(capsys: pytest.CaptureFixture[str]) -> None:
    """--input-schema prints the CommsConfig JSON schema."""
    assert cli.main(["--input-schema"]) == 0
    parsed = json.loads(capsys.readouterr().out)
    assert "properties" in parsed


def test_cli_no_config_errors() -> None:
    """No config and no --default is a usage error (exit 2)."""
    assert cli.main([]) == 2
