"""The ``rklb-comms`` command-line entry point.

Usage::

    uv run rklb-comms <config.yaml>            # full text report
    uv run rklb-comms <config.yaml> --brief    # one-line customer-first headline
    uv run rklb-comms <config.yaml> --json      # enriched typed JSON artifact
    uv run rklb-comms --input-schema            # input schema (JSON)
    uv run rklb-comms --default                 # packaged default scenario
    uv run rklb-comms --promote                 # dual-promote default public JSON

The CLI reads a single comms YAML config, runs the space model, and prints the
result. It is a thin shell over :mod:`communications.config`,
:mod:`communications.engine`, :mod:`communications.json_output`,
:mod:`communications.ground`, and :mod:`communications.text_report`.

Two output locations, by design (mirroring the data-center "Run output vs.
promoted model" distinction):

* ``code/outputs/communications/runs/`` is git-ignored scratch (redirect
  ``--json`` there and rerun freely; each run carries its own ``generated_at``).
* ``communications/models/space/`` holds the reviewed space-model JSON.
* ``communications/models/ground/`` holds the reviewed ground-reference JSON.
* ``communications/models/conclusion.md`` is the hand-written Phase-6 conclusion
  and is NEVER overwritten by promotion.

There is NO separate ground YAML: the ground dials live in the single
``comms_default.yaml`` (the one-YAML model), so the dual-promote reads the same
file for both the space and the ground pipeline.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from pathlib import Path
from typing import Final

from communications.config import CommsConfig, load_config
from communications.constants import PROMOTED_DEFAULT_ARTIFACT_ROLE
from communications.engine import render_comms_json, run_comms_model
from communications.ground import (
    build_ground_reference_output,
    default_ground_source_catalog,
    ground_config_from_comms_config,
    render_ground_json,
)
from communications.json_output import enrich_comms_output
from communications.text_report import render_comms_headline, render_comms_text

logger = logging.getLogger(__name__)

# Path constants, resolved relative to this file so paths are found whether the
# package is run from a checkout or an installed wheel.
_CALCULATOR_DIR: Final[Path] = Path(__file__).resolve().parents[2]
"""The ``code/`` directory (holds ``scenarios/`` and ``pyproject.toml``)."""

_PROJECT_DIR: Final[Path] = _CALCULATOR_DIR.parent
"""The repository root."""

_DEFAULT_YAML: Final[Path] = _CALCULATOR_DIR / "scenarios" / "comms_default.yaml"
"""The packaged default comms scenario (carries BOTH the space and ground dials)."""

_PROMOTED_SPACE_DIR: Final[Path] = _PROJECT_DIR / "communications" / "models" / "space"
"""The promoted space-model JSON directory."""

_PROMOTED_GROUND_DIR: Final[Path] = _PROJECT_DIR / "communications" / "models" / "ground"
"""The promoted ground-reference JSON directory."""

_DEFAULT_OUTPUT_NAME: Final[str] = "default"
"""The default promoted-file stem."""

_OUTPUT_NAME_PATTERN: Final[re.Pattern[str]] = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
"""The safe file-stem guard for the promoted output name."""


def _repo_relative(path: Path) -> str:
    """Return a repository-relative path for the source-scenario stamp."""
    try:
        return path.relative_to(_PROJECT_DIR).as_posix()
    except ValueError:
        return path.as_posix()


def _promoted_space_path(output_name: str) -> Path:
    """Return the promoted space-model JSON path for an output name.

    Args:
        output_name: File stem for the promoted JSON. The default stem is
            ``default`` and writes ``communications/models/space/default.json``.

    Raises:
        ValueError: If ``output_name`` is not a safe file stem.
    """
    if _OUTPUT_NAME_PATTERN.fullmatch(output_name) is None:
        raise ValueError(
            "output name must start with a letter or number and contain only "
            "letters, numbers, underscores, or hyphens"
        )
    return _PROMOTED_SPACE_DIR / f"{output_name}.json"


def _promoted_ground_path(output_name: str) -> Path:
    """Return the promoted ground-reference JSON path for an output name.

    Args:
        output_name: File stem for the promoted JSON.

    Raises:
        ValueError: If ``output_name`` is not a safe file stem.
    """
    if _OUTPUT_NAME_PATTERN.fullmatch(output_name) is None:
        raise ValueError(
            "output name must start with a letter or number and contain only "
            "letters, numbers, underscores, or hyphens"
        )
    return _PROMOTED_GROUND_DIR / f"{output_name}.json"


def _render_input_schema_json() -> str:
    """Render the comms input schema as JSON.

    Dumps the :class:`communications.config.CommsConfig` Pydantic schema (every
    field's type, bounds, default, and description). Emitted by
    ``rklb-comms --input-schema``.
    """
    return json.dumps(CommsConfig.model_json_schema(), indent=2, ensure_ascii=False)


def _build_parser() -> argparse.ArgumentParser:
    """Build the ``rklb-comms`` argparse parser."""
    parser = argparse.ArgumentParser(
        prog="rklb-comms",
        description=(
            "Cost-vs-ground model for Rocket Lab's Neutron-launched communications "
            "constellation. Reads one comms YAML config and outputs the per-year "
            "per-class cost-out, the steady-state customer band, and (on --promote) "
            "the ground reference."
        ),
    )
    parser.add_argument(
        "config",
        nargs="?",
        help="Path to the comms YAML config. Omit and pass --default for the packaged scenario.",
    )
    parser.add_argument(
        "--default",
        action="store_true",
        help="Run the packaged default scenario (scenarios/comms_default.yaml).",
    )
    parser.add_argument(
        "--brief",
        action="store_true",
        help="Print only the one-line customer-first headline.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the enriched typed JSON artifact instead of the text report.",
    )
    parser.add_argument(
        "--input-schema",
        action="store_true",
        help="Print the comms input schema (JSON) and exit. Needs no config.",
    )
    parser.add_argument(
        "--promote",
        action="store_true",
        help=(
            "Run a scenario and dual-promote its JSON into communications/models/. "
            "The default output writes BOTH space/default.json and ground/default.json. "
            "Defaults to the packaged default scenario."
        ),
    )
    parser.add_argument(
        "--output-name",
        default=_DEFAULT_OUTPUT_NAME,
        help="Promoted JSON file stem. Defaults to 'default'.",
    )
    return parser


def _promote_model(config_path: Path, output_name: str) -> int:
    """Promote one comms scenario to the public space + ground JSON artifacts.

    Loads the comms scenario, runs the space model, ENRICHES the space output's
    meta block (:func:`communications.json_output.enrich_comms_output`), and writes
    the enriched space JSON to ``communications/models/space/<output_name>.json``.
    For the default output name, it ALSO builds the ground reference (from the SAME
    single comms config, the one-YAML model, reading the in-memory space output BY
    VALUE) and writes it to ``communications/models/ground/default.json``. This is
    the DUAL-PROMOTE that supersedes the lean Phase-3 / Phase-4 library promote
    helpers (which stay for tests). It does NOT overwrite
    ``communications/models/conclusion.md`` (the Phase-6 hand-written prose).

    Args:
        config_path: Comms YAML scenario to run.
        output_name: Promoted JSON file stem (default 'default').

    Returns:
        Process exit code: 0 on success, 1 if the scenario fails to load or the
        output name is invalid.
    """
    try:
        space_path = _promoted_space_path(output_name)
        config = load_config(config_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    artifact_role = (
        PROMOTED_DEFAULT_ARTIFACT_ROLE if output_name == _DEFAULT_OUTPUT_NAME else "promoted_named"
    )
    space_output = run_comms_model(
        config,
        source_scenario_path=_repo_relative(config_path.resolve()),
        artifact_role=artifact_role,
    )
    enriched = enrich_comms_output(space_output)
    space_path.parent.mkdir(parents=True, exist_ok=True)
    space_path.write_text(render_comms_json(enriched) + "\n", encoding="utf-8")
    logger.info("promoted comms space model -> %s", space_path)
    print(f"promoted comms space model -> {space_path}", file=sys.stderr)

    if output_name == _DEFAULT_OUTPUT_NAME:
        # Build the ground reference from the SAME config and the LEAN in-memory
        # space output (by value, concern C10). The ground builder reads the
        # steady-state space CELLS, identical in the lean and enriched outputs;
        # the enrichment only touches the meta block, which the ground builder
        # does not read.
        ground_config = ground_config_from_comms_config(config)
        ground_output = build_ground_reference_output(
            space_output,
            ground_config,
            config.price_reference,
            default_ground_source_catalog(),
        )
        ground_path = _promoted_ground_path(output_name)
        ground_path.parent.mkdir(parents=True, exist_ok=True)
        ground_path.write_text(render_ground_json(ground_output) + "\n", encoding="utf-8")
        logger.info("promoted comms ground reference -> %s", ground_path)
        print(f"promoted comms ground reference -> {ground_path}", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    """The ``rklb-comms`` CLI entry point. Returns a process exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.input_schema:
        print(_render_input_schema_json())
        return 0

    if args.promote:
        promote_config = Path(args.config) if args.config else _DEFAULT_YAML
        return _promote_model(promote_config, str(args.output_name))

    if args.default:
        config_path: Path = _DEFAULT_YAML
    elif args.config:
        config_path = Path(args.config)
    else:
        parser.print_usage(sys.stderr)
        print("error: provide a comms YAML config path, or use --default", file=sys.stderr)
        return 2

    try:
        config = load_config(config_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    space_output = run_comms_model(
        config, source_scenario_path=_repo_relative(config_path.resolve())
    )

    if args.brief:
        print(render_comms_headline(space_output))
    elif args.json:
        print(render_comms_json(enrich_comms_output(space_output)))
    else:
        print(render_comms_text(space_output))
    return 0


__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
