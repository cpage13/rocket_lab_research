"""The ``rklb-value`` command-line entry point.

Usage::

    uv run rklb-value <config.yaml>            # full text report
    uv run rklb-value <config.yaml> --brief    # one-line GPU-first headline
    uv run rklb-value <config.yaml> --json     # typed JSON artifact
    uv run rklb-value --default                # the repository's scenarios/default.yaml
    uv run rklb-value --input-schema           # input schema (JSON)
    uv run rklb-value --promote                # promote the default space + ground JSON
    uv run rklb-value <config.yaml> --promote --output-name <stem>  # a named space artifact

The CLI reads a YAML config, runs the GPU-first valuation, and prints the
result. It is a thin shell over :mod:`data_center.config`,
:mod:`data_center.engine`, :mod:`data_center.json_output`, and
:mod:`data_center.text_report`; promotion adds :mod:`data_center.ground`,
imported only when a promotion runs.

Conventions (shared with the Iridium promotion command through
:mod:`common.cli`): stdout carries only the product (the report, the JSON
artifact, the schema); status and errors are log records on stderr. A
scenario that cannot be loaded or run, a promotion refused for failing
validation checks, or a failed write is one ``ERROR:`` line and exit status
:data:`~common.cli.EXIT_ERROR` (1), never a traceback. Usage errors exit with
:data:`~common.cli.EXIT_USAGE` (2): conflicting flags (``--default`` with a
config path, ``--brief`` with ``--json``, ``--output-name`` without
``--promote``, ``--brief`` or ``--json`` with ``--promote``, ``--input-schema``
with anything else), a malformed ``--output-name``, and an output name that
misstates the scenario.

Promotion rules (``--promote``):

* The scenario is loaded first, so a mistyped path is reported as the missing
  file it is.
* The artifact role derives from whether the scenario is the canonical
  default (:func:`data_center.input_manifest.is_default_scenario`), never
  from the output name. The name ``default`` belongs to
  ``scenarios/default.yaml`` alone: any other scenario needs
  ``--output-name``, and the default scenario is promoted only as
  ``default``. Output names are lowercase, so on a case-insensitive file
  system no spelling of another name can land on ``default.json``.
* Promotion refuses when any validation check fails: a ``fail`` in the space
  artifact's ``meta.validation_results`` (a critical or major V-rule, a model
  invariant, or a default guard) or in the ground reference's.
* Both artifacts are built completely in memory, then written through
  :func:`common.file_io.write_files_with_rollback`: each is staged in full
  beside its destination, the current files are preserved as backups, and
  the staged files are renamed into place one at a time. If a rename fails,
  the artifacts already replaced are restored from their backups, and the
  error line says which files were restored and which, if any, still hold new
  content. Each rename is atomic; the pair is restored on failure, not
  written in one indivisible step. A destination that is a symbolic link or
  not a regular file is refused before anything is written.

Output locations, by design (see ``code/README.md``, "Promote Public
Artifacts"):

* ``code/outputs/data_center/runs/`` is git-ignored scratch: redirect
  ``--json`` there and rerun freely; each run carries its own
  ``generated_at`` timestamp.
* ``data_center/models/space/`` holds reviewed space-model JSON artifacts.
* ``data_center/models/ground/`` holds the default ground-reference JSON
  artifact (only the default promotion writes one).
* ``data_center/conclusion.md`` is a reviewed static conclusion and is not
  overwritten by promotion.

The command runs from a source checkout only
(:func:`common.file_io.locate_source_checkout`): the scenarios and promoted
artifacts are repository files the wheel does not ship.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from collections.abc import Sequence
from pathlib import Path
from typing import Final

from common.cli import (
    EXIT_ERROR,
    EXIT_OK,
    CliArgumentParser,
    configure_cli_logging,
    describe_failure,
)
from common.file_io import (
    ModelFileError,
    SourceCheckout,
    artifact_write,
    locate_source_checkout,
    render_artifact_json,
    write_files_with_rollback,
)
from common.meta import ValidationResult, ValidationSeverity
from data_center.config import ValuationConfig, load_config
from data_center.engine import run_valuation
from data_center.input_manifest import DEFAULT_SCENARIO_PATH, is_default_scenario
from data_center.output import ArtifactRole
from data_center.text_report import render_headline, render_text

logger = logging.getLogger(__name__)

DEFAULT_OUTPUT_NAME: Final[str] = "default"
"""The promoted file stem, reserved for the canonical default scenario."""

OUTPUT_NAME_PATTERN: Final[re.Pattern[str]] = re.compile(r"[a-z0-9][a-z0-9_-]*")
"""A promoted file stem: a lowercase letter or digit, then lowercase letters, digits,
``_`` or ``-``. Lowercase only, because the file systems this runs on are often
case-insensitive (APFS by default): ``DEFAULT.json`` would be ``default.json``, so
allowing capitals would let a named promotion overwrite the reserved default."""

PROMOTED_MODELS_DIR: Final[str] = "data_center/models"
"""Repository-relative directory the promoted artifacts live under."""

SPACE_MODELS_SUBDIR: Final[str] = "space"
"""Subdirectory of the promoted models directory holding space-model artifacts."""

GROUND_MODELS_SUBDIR: Final[str] = "ground"
"""Subdirectory of the promoted models directory holding ground-reference artifacts."""


def _output_stem(value: str) -> str:
    """Validate an ``--output-name`` value as a lowercase file stem (argparse type)."""
    if OUTPUT_NAME_PATTERN.fullmatch(value) is None:
        raise argparse.ArgumentTypeError(
            f"{value!r} is not a valid output name: use lowercase letters, digits, "
            "underscores, or hyphens, starting with a letter or digit"
        )
    return value


def _build_parser() -> CliArgumentParser:
    """Build the command's argument parser (usage errors exit with EXIT_USAGE)."""
    parser = CliArgumentParser(
        prog="rklb-value",
        description=(
            "GPU-first valuation calculator for Rocket Lab's orbital "
            "AI-inference data-center venture. Reads a YAML config and "
            "outputs per-year per-node economics."
        ),
    )
    parser.add_argument(
        "config",
        nargs="?",
        help=(
            "Path to the YAML config. Omit it and pass --default to run the "
            "repository's default scenario (scenarios/default.yaml)."
        ),
    )
    parser.add_argument(
        "--default",
        action="store_true",
        help="Run the repository's default scenario (scenarios/default.yaml).",
    )
    report_format = parser.add_mutually_exclusive_group()
    report_format.add_argument(
        "--brief",
        action="store_true",
        help="Print only the one-line GPU-first headline.",
    )
    report_format.add_argument(
        "--json",
        action="store_true",
        help="Print the typed JSON artifact instead of the text report.",
    )
    parser.add_argument(
        "--input-schema",
        action="store_true",
        help="Print the GPU-first input schema (JSON) and exit. Takes no other option.",
    )
    parser.add_argument(
        "--promote",
        action="store_true",
        help=(
            "Run a scenario and promote its JSON model into data_center/models/space/; "
            "the default scenario also writes data_center/models/ground/default.json. "
            "Without a config path, promotes the repository's default scenario "
            "(scenarios/default.yaml); any other scenario needs --output-name. "
            "Refused when any validation check fails."
        ),
    )
    parser.add_argument(
        "--output-name",
        type=_output_stem,
        default=None,
        help=(
            "Promoted JSON file stem for a non-default scenario (with --promote only): "
            "lowercase letters, digits, underscores, or hyphens. "
            f"'{DEFAULT_OUTPUT_NAME}' is reserved for {DEFAULT_SCENARIO_PATH}."
        ),
    )
    return parser


def _reject_conflicting_flags(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """Fail loudly (a usage error, EXIT_USAGE) on flags that contradict each other.

    ``--brief`` with ``--json`` is rejected by the parser's mutually exclusive
    group; this covers the combinations that group cannot express.
    """
    if args.input_schema and (
        args.config
        or args.default
        or args.promote
        or args.brief
        or args.json
        or args.output_name is not None
    ):
        parser.error("--input-schema takes no scenario and no other option")
    if args.config and args.default:
        parser.error("pass a config path or --default, not both")
    if args.output_name is not None and not args.promote:
        parser.error("--output-name applies only with --promote")
    if args.promote and (args.brief or args.json):
        parser.error("--brief and --json format a report; --promote writes artifacts instead")
    if not (args.input_schema or args.promote or args.config or args.default):
        parser.error("provide a YAML config path, or use --default")


def _promotion_output_name(
    parser: argparse.ArgumentParser, requested: str | None, scenario_ref: str
) -> str:
    """Return the promoted file stem, enforcing that ``default`` means the default scenario.

    A name that misstates the scenario is a usage error (EXIT_USAGE).

    Args:
        parser: The parser, for usage errors.
        requested: The ``--output-name`` value (already a valid lowercase
            stem), or None when not given.
        scenario_ref: The scenario's repository-relative path.

    Returns:
        ``default`` for the canonical default scenario, else the requested stem.
    """
    if is_default_scenario(scenario_ref):
        if requested not in (None, DEFAULT_OUTPUT_NAME):
            parser.error(
                f"the default scenario is promoted only as '{DEFAULT_OUTPUT_NAME}'; "
                "drop --output-name"
            )
        return DEFAULT_OUTPUT_NAME
    if requested is None:
        parser.error(
            f"{scenario_ref} is not the default scenario: pass --output-name <stem> to "
            "promote it under its own name"
        )
    if requested == DEFAULT_OUTPUT_NAME:
        parser.error(
            f"the output name '{DEFAULT_OUTPUT_NAME}' is reserved for {DEFAULT_SCENARIO_PATH}; "
            "choose another --output-name"
        )
    return requested


def _render_input_schema_json() -> str:
    """Render the GPU-first input schema as JSON.

    Dumps the :class:`data_center.config.ValuationConfig` schema: every
    field's type, bounds, default, and description. Emitted by
    ``rklb-value --input-schema``.
    """
    return json.dumps(ValuationConfig.model_json_schema(), indent=2, ensure_ascii=False)


def _failed_checks(results: Sequence[ValidationResult]) -> list[str]:
    """Return the ids of the validation results that fail."""
    return [
        result.validation_id for result in results if result.severity == ValidationSeverity.FAIL
    ]


def _report(config: ValuationConfig, scenario_ref: str, *, brief: bool, as_json: bool) -> int:
    """Run one loaded scenario and print its report, headline, or JSON artifact to stdout.

    Args:
        config: The loaded scenario.
        scenario_ref: Its repository-relative path, recorded as the source.
        brief: Print the one-line headline.
        as_json: Print the typed JSON artifact.

    Returns:
        :data:`~common.cli.EXIT_OK`, or :data:`~common.cli.EXIT_ERROR` when the
        model cannot run the scenario.
    """
    try:
        output = run_valuation(config, source_scenario_path=scenario_ref)
    except ValueError as exc:
        logger.error("could not run %s: %s", scenario_ref, describe_failure(exc))
        return EXIT_ERROR
    if brief:
        print(render_headline(output))
    elif as_json:
        print(render_artifact_json(output))
    else:
        print(render_text(output))
    return EXIT_OK


def _promote(
    config: ValuationConfig,
    scenario_ref: str,
    output_name: str,
    checkout: SourceCheckout,
    models_dir: Path,
) -> int:
    """Promote one loaded scenario to public JSON artifacts, or refuse and change nothing.

    Runs the scenario (role ``promoted_default`` for the canonical default,
    else ``promoted_named``) and, for the default, builds the ground
    reference from it; checks every validation result of both; then writes
    the files through :func:`common.file_io.write_files_with_rollback`, which
    restores any artifact already replaced if a later one cannot be. This
    command never writes ``data_center/conclusion.md``, the reviewed
    editorial prose tied to the promoted JSON.

    Args:
        config: The loaded scenario.
        scenario_ref: Its repository-relative path.
        output_name: The promoted file stem (checked by
            :func:`_promotion_output_name`).
        checkout: The source checkout, for the ground scenario and the
            recorded repository paths.
        models_dir: Directory holding the ``space/`` and ``ground/`` artifact
            directories.

    Returns:
        :data:`~common.cli.EXIT_OK`, or :data:`~common.cli.EXIT_ERROR` when the
        model cannot run the scenario, the ground scenario cannot be loaded, a
        validation check fails, or an artifact cannot be written.
    """
    # Imported here: only promotion builds the ground reference, so a report
    # or --json run does not pay for importing it.
    from data_center.ground import (
        DEFAULT_GROUND_SCENARIO_PATH,
        build_ground_reference_output,
        load_ground_config,
    )

    is_default = is_default_scenario(scenario_ref)
    role = ArtifactRole.PROMOTED_DEFAULT if is_default else ArtifactRole.PROMOTED_NAMED
    space_path = models_dir / SPACE_MODELS_SUBDIR / f"{output_name}.json"
    try:
        output = run_valuation(config, source_scenario_path=scenario_ref, artifact_role=role)
        writes = [artifact_write(space_path, output)]
        failed = _failed_checks(output.meta.validation_results)
        if is_default:
            ground_scenario = checkout.repo_dir / DEFAULT_GROUND_SCENARIO_PATH
            ground = build_ground_reference_output(
                output,
                load_ground_config(ground_scenario),
                space_model_path=checkout.repo_relative(space_path),
                ground_scenario_path=checkout.repo_relative(ground_scenario),
            )
            ground_path = models_dir / GROUND_MODELS_SUBDIR / f"{output_name}.json"
            writes.append(artifact_write(ground_path, ground))
            failed.extend(_failed_checks(ground.meta.validation_results))
    except (ModelFileError, ValueError) as exc:
        logger.error("could not promote %s: %s", scenario_ref, describe_failure(exc))
        return EXIT_ERROR
    if failed:
        logger.error(
            "refusing to promote %s: %d validation check(s) fail (%s); nothing was written",
            scenario_ref,
            len(failed),
            ", ".join(failed),
        )
        return EXIT_ERROR
    try:
        write_files_with_rollback(writes)
    except ModelFileError as exc:
        # The writer's message states the outcome for every artifact.
        logger.error("could not promote %s: %s", scenario_ref, describe_failure(exc))
        return EXIT_ERROR
    for write in writes:
        logger.info("promoted %s", write.path)
    return EXIT_OK


def main(argv: list[str] | None = None, *, models_dir: Path | None = None) -> int:
    """CLI entry point. Returns a process exit code.

    Args:
        argv: The arguments (defaults to ``sys.argv[1:]``).
        models_dir: Directory ``--promote`` writes ``space/`` and ``ground/``
            under; defaults to the checkout's ``data_center/models/``. Tests
            pass a temporary directory.

    Returns:
        :data:`~common.cli.EXIT_OK` on success, :data:`~common.cli.EXIT_ERROR`
        on an expected failure. Usage errors exit through
        :class:`~common.cli.CliArgumentParser` with
        :data:`~common.cli.EXIT_USAGE`.
    """
    configure_cli_logging()
    parser = _build_parser()
    args = parser.parse_args(argv)
    _reject_conflicting_flags(parser, args)

    if args.input_schema:
        print(_render_input_schema_json())
        return EXIT_OK

    try:
        checkout = locate_source_checkout(__file__)
    except ModelFileError as exc:
        logger.error("%s", describe_failure(exc))
        return EXIT_ERROR
    scenario = Path(args.config) if args.config else checkout.repo_dir / DEFAULT_SCENARIO_PATH
    scenario_ref = checkout.repo_relative(scenario)
    try:
        config = load_config(scenario)
    except (ModelFileError, ValueError) as exc:
        logger.error("could not load %s: %s", scenario_ref, describe_failure(exc, scenario))
        return EXIT_ERROR

    if args.promote:
        output_name = _promotion_output_name(parser, args.output_name, scenario_ref)
        target = models_dir if models_dir is not None else checkout.repo_dir / PROMOTED_MODELS_DIR
        return _promote(config, scenario_ref, output_name, checkout, target)
    return _report(config, scenario_ref, brief=args.brief, as_json=args.json)


if __name__ == "__main__":
    raise SystemExit(main())
