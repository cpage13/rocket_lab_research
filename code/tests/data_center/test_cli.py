"""Tests for the ``rklb-value`` run modes: flags, failures, and output streams.

The command-line contract (``data_center.cli``, conventions in
``common.cli``):

1. conflicting flags are usage errors (``EXIT_USAGE``) that name the
   conflict, never silently resolved;
2. an expected failure is one error record and ``EXIT_ERROR``, never a
   traceback: a scenario that cannot be loaded (missing, malformed, invalid,
   a broken generations file, a base year before the first GPU generation)
   reads ``could not load <scenario>: <reason>``, naming the scenario once;
   one the model cannot run (a release cadence whose generation extension
   overflows) reads ``could not run <scenario>: <reason>``;
3. stdout carries only the product (report, headline, JSON), and a
   successful run logs nothing at INFO or above; the real process writes
   exactly one ``ERROR:`` line to stderr on failure;
4. a scenario's ``generations: <path>`` resolves beside the scenario file,
   whatever the working directory;
5. a plain run does not import the ground reference module (only promotion
   needs it).
"""

from __future__ import annotations

import json
import logging
import subprocess
import sys
from pathlib import Path

import pytest

from common.cli import EXIT_ERROR, EXIT_OK, EXIT_USAGE
from data_center import cli

_DEFAULT_SCENARIO_ARG = "<scenarios/default.yaml>"
"""Placeholder in a parametrized argv for the repository's default scenario path."""


def _errors(caplog: pytest.LogCaptureFixture) -> list[str]:
    """Return the messages of the captured ERROR (and worse) records."""
    return [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]


def _write(path: Path, text: str) -> Path:
    """Write a small synthetic scenario file and return its path."""
    path.write_text(text, encoding="utf-8")
    return path


@pytest.mark.parametrize(
    ("argv", "message"),
    [
        ([_DEFAULT_SCENARIO_ARG, "--default"], "pass a config path or --default, not both"),
        ([_DEFAULT_SCENARIO_ARG, "--brief", "--json"], "not allowed with argument"),
        (
            [_DEFAULT_SCENARIO_ARG, "--output-name", "x"],
            "--output-name applies only with --promote",
        ),
        (["--promote", "--json"], "--promote writes artifacts instead"),
        (["--input-schema", "--default"], "--input-schema takes no scenario"),
        ([], "provide a YAML config path, or use --default"),
    ],
    ids=[
        "default_with_config",
        "brief_with_json",
        "output_name_without_promote",
        "promote_with_json",
        "schema_with_default",
        "nothing_to_run",
    ],
)
def test_conflicting_flags_fail_loudly(
    capsys: pytest.CaptureFixture[str], scenarios_dir: Path, argv: list[str], message: str
) -> None:
    """Objective: contradictory flags are rejected, not silently resolved.

    The original trigger: ``--default`` silently overrode a positional config,
    and ``--output-name`` without ``--promote`` and ``--brief`` with
    ``--json`` were silently dropped. Expected: each combination is a usage
    error (``EXIT_USAGE``) whose message names the conflict; nothing is
    printed to stdout.
    """
    default_yaml = str(scenarios_dir / "default.yaml")
    argv = [default_yaml if arg == _DEFAULT_SCENARIO_ARG else arg for arg in argv]

    with pytest.raises(SystemExit) as excinfo:
        cli.main(argv)

    assert excinfo.value.code == EXIT_USAGE
    captured = capsys.readouterr()
    assert message in captured.err
    assert captured.out == ""


@pytest.mark.parametrize(
    ("scenario_text", "reason"),
    [
        ("gospel:\n  mass_envelope_t: [12.5\n", "malformed YAML ("),
        ("- a\n- list\n", "the YAML root must be a mapping, got list"),
        ("gospel:\n  node_mass_fixed_t: 13.0\n", "invalid ValuationConfig: gospel:"),
        (
            "metadata:\n  base_year: 2022\n  horizon_years: 10\n",
            "invalid ValuationConfig: metadata.base_year 2022 precedes every listed generation",
        ),
        ("generations: missing_generations.yaml\n", "missing_generations.yaml: file not found"),
        ("generations: broken_generations.yaml\n", "broken_generations.yaml: malformed YAML ("),
        ("generations: keyless_generations.yaml\n", "missing top-level key 'generations'"),
    ],
    ids=[
        "malformed_yaml",
        "list_root",
        "invalid_dial",
        "base_year_before_first_generation",
        "missing_generations_file",
        "malformed_generations_file",
        "generations_file_without_key",
    ],
)
def test_a_scenario_that_cannot_load_fails_with_one_clean_error(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
    scenario_text: str,
    reason: str,
) -> None:
    """Objective: a bad scenario is one error line and ``EXIT_ERROR``.

    The original triggers: a malformed generations file raised a raw PyYAML
    ``ParserError`` traceback, and base years 2020 to 2024 crashed mid-run
    with ``NoFrontierAvailableError``. Expected: every case exits 1 with
    exactly one single-line error record, ``could not load <scenario>:``
    followed by the problem (a generations file's own path where it is that
    file's problem), naming the scenario once; stdout stays empty.
    """
    _write(tmp_path / "broken_generations.yaml", "generations:\n  - name: [B200\n")
    _write(tmp_path / "keyless_generations.yaml", "gens: []\n")
    scenario = _write(tmp_path / "scenario.yaml", scenario_text)

    exit_code = cli.main([str(scenario), "--json"])

    assert exit_code == EXIT_ERROR
    errors = _errors(caplog)
    assert len(errors) == 1
    assert "\n" not in errors[0]
    assert errors[0].startswith(f"could not load {scenario}: ")
    assert errors[0].count(str(scenario)) == 1
    assert reason in errors[0]
    assert capsys.readouterr().out == ""


def test_a_missing_scenario_names_its_path_once(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Objective: a scenario path that does not exist is a clean error.

    The original trigger printed the path twice (``could not run X: X: file
    not found``). Expected: exit 1 and exactly the line
    ``could not load <path>: file not found``.
    """
    missing = tmp_path / "nowhere.yaml"

    assert cli.main([str(missing)]) == EXIT_ERROR

    assert _errors(caplog) == [f"could not load {missing}: file not found"]


def test_a_scenario_the_model_cannot_run_fails_with_one_clean_error(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Objective: a run-time model failure is a clean error, not a traceback.

    The original trigger: ``release_cadence_yr`` 0.001 (valid at load, since
    the dial is only bounded above zero) needs thousands of extrapolated
    generations, whose compounding overflowed and crashed with an
    ``OverflowError`` traceback. Expected: exit 1 with one record,
    ``could not run <scenario>:`` naming the overflow and the dial to change.
    """
    scenario = _write(tmp_path / "fast_cadence.yaml", "gospel:\n  release_cadence_yr: 0.001\n")

    assert cli.main([str(scenario)]) == EXIT_ERROR

    errors = _errors(caplog)
    assert len(errors) == 1
    assert errors[0].startswith(f"could not run {scenario}: the generation extension overflows")
    assert "gospel.release_cadence_yr" in errors[0]


def test_the_real_process_writes_one_error_line_and_exits_1(tmp_path: Path) -> None:
    """Objective: the installed handler, not only the log records, behaves.

    Expected: ``python -m data_center.cli <missing.yaml>`` in a fresh process
    (the real stderr handler, from an unrelated working directory) exits 1,
    prints nothing on stdout, and writes exactly one stderr line,
    ``ERROR: could not load <path>: file not found``.
    """
    missing = tmp_path / "nowhere.yaml"
    result = subprocess.run(  # noqa: S603 (the running interpreter and a static module)
        [sys.executable, "-m", "data_center.cli", str(missing)],
        capture_output=True,
        text=True,
        check=False,
        cwd=tmp_path,
    )
    assert result.returncode == EXIT_ERROR
    assert result.stdout == ""
    assert result.stderr == f"ERROR: could not load {missing}: file not found\n"


@pytest.mark.parametrize("flag", [None, "--brief", "--json"])
def test_a_successful_run_prints_only_its_product(
    capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture, flag: str | None
) -> None:
    """Objective: stdout is the product; a clean run logs nothing at INFO or above.

    Expected: the report, the one-line headline, or a parseable JSON
    artifact on stdout (``--default`` runs ``scenarios/default.yaml``),
    nothing on stderr, and no INFO-or-worse record.
    """
    caplog.set_level(logging.INFO)
    argv = ["--default"] if flag is None else ["--default", flag]

    assert cli.main(argv) == EXIT_OK

    captured = capsys.readouterr()
    assert captured.err == ""
    assert not [r for r in caplog.records if r.levelno >= logging.INFO]
    if flag == "--json":
        assert json.loads(captured.out)["inputs"]["scenario"]["is_default"] is True
    elif flag == "--brief":
        assert len(captured.out.strip().splitlines()) == 1
    else:
        assert "VALIDATION CHECKS" in captured.out


def test_generations_path_resolves_beside_the_scenario(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    scenarios_dir: Path,
) -> None:
    """Objective: ``generations: <relative path>`` is read beside the scenario file.

    The original trigger: the path resolved against the working directory.
    Expected: run from an unrelated directory, a scenario naming
    ``gens.yaml`` (a copy of the bundled roadmap with the first entry
    renamed) exits 0 and the artifact lists the renamed generation.
    """
    bundled = (scenarios_dir / "generations.yaml").read_text(encoding="utf-8")
    assert "B200/GB200" in bundled
    project = tmp_path / "project"
    project.mkdir()
    _write(project / "gens.yaml", bundled.replace("B200/GB200", "Renamed B200", 1))
    scenario = _write(project / "scenario.yaml", "generations: gens.yaml\n")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)

    assert cli.main([str(scenario), "--json"]) == EXIT_OK

    artifact = json.loads(capsys.readouterr().out)
    names = [g["name"]["value"] for g in artifact["inputs"]["config"]["generations"]]
    assert names[0] == "Renamed B200"


def test_a_plain_run_does_not_import_the_ground_module() -> None:
    """Objective: only promotion pays for importing the ground reference.

    Expected: importing the CLI module in a fresh interpreter leaves
    ``data_center.ground`` unimported.
    """
    probe = "import sys, data_center.cli; print('data_center.ground' in sys.modules)"
    result = subprocess.run(  # noqa: S603 (the running interpreter and a static probe)
        [sys.executable, "-c", probe],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "False"
