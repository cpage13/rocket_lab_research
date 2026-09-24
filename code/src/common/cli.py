"""Process conventions shared by the command-line entry points.

``rklb-value`` (:mod:`data_center.cli`) and the Iridium promotion command
(``python -m communications.json_output``) follow one convention:

* stdout carries only the command's product (a report, a JSON artifact, a
  schema); status and errors are log records on stderr, through the handler
  :func:`configure_cli_logging` installs;
* an expected failure (a missing or malformed file, an invalid scenario, a
  promotion refused for failing validation checks, a failed write) is one
  line built by :func:`describe_failure` and exit status :data:`EXIT_ERROR`,
  never a traceback;
* a usage error (conflicting or malformed flags, a promotion name that
  misstates the scenario) goes through :class:`CliArgumentParser`: the usage
  line, one ``error:`` line, and exit status :data:`EXIT_USAGE`.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Final, NoReturn

from pydantic import ValidationError

from common.file_io import ModelFileError

logger = logging.getLogger(__name__)

EXIT_OK: Final[int] = 0
"""Process exit code for a successful command."""

EXIT_ERROR: Final[int] = 1
"""Process exit code for an expected failure: a missing, unreadable, or invalid
input file, a scenario the model cannot run, a promotion refused for failing
validation checks, or a failed write."""

EXIT_USAGE: Final[int] = 2
"""Process exit code for a usage error: conflicting or malformed flags, or a
promotion output name that misstates the scenario. It equals argparse's own
parse-error status, and :class:`CliArgumentParser` exits with it for every
usage error, whether argparse or the command raises it."""

CLI_LOG_LEVEL: Final[int] = logging.INFO
"""Records at this level and above reach stderr: promotion status lines, warnings,
and errors. Model internals log at DEBUG and stay silent, so a successful report
or ``--json`` run writes nothing to stderr."""

CLI_LOG_FORMAT: Final[str] = "%(levelname)s: %(message)s"
"""One line per record, led by its level (``INFO: promoted ...``, ``ERROR: ...``)."""

_PYDANTIC_VALUE_ERROR: Final[str] = "value_error"
"""Pydantic's error type for a ``ValueError`` raised inside a validator."""


class CliArgumentParser(argparse.ArgumentParser):
    """An argument parser whose every usage error exits with :data:`EXIT_USAGE`."""

    def error(self, message: str) -> NoReturn:
        """Print the usage line and ``<prog>: error: <message>`` to stderr, then exit.

        Args:
            message: What is wrong with the arguments, in one line.
        """
        self.print_usage(sys.stderr)
        self.exit(EXIT_USAGE, f"{self.prog}: error: {message}\n")


def configure_cli_logging() -> None:
    """Route log records at :data:`CLI_LOG_LEVEL` and above to stderr, one line each.

    Uses :func:`logging.basicConfig`, which leaves an already-configured root
    logger alone (a host application's, or pytest's capture handler).
    """
    logging.basicConfig(level=CLI_LOG_LEVEL, format=CLI_LOG_FORMAT, stream=sys.stderr)


def _same_file(first: Path, second: Path) -> bool:
    """Return whether two paths name the same file (compared once resolved)."""
    return first.resolve() == second.resolve()


def describe_failure(exc: Exception, subject: Path | None = None) -> str:
    """Return a one-line description of an expected failure.

    A pydantic :class:`~pydantic.ValidationError` lists each error as
    ``location: message`` (a validator's own ``ValueError`` message without
    pydantic's ``Value error,`` prefix), joined by ``;``. A
    :class:`~common.file_io.ModelFileError` about ``subject`` itself gives only
    its reason, since the caller's message already names that file; one about
    another file (a generations file a scenario names, an artifact being
    written) keeps its path. Any other error is its message with line breaks
    and runs of whitespace collapsed.

    Args:
        exc: The failure to describe.
        subject: The file the caller's message is already about, if any.

    Returns:
        The one-line description.
    """
    if isinstance(exc, ValidationError):
        parts = []
        for error in exc.errors(include_url=False):
            context = error.get("ctx") or {}
            message = (
                str(context["error"])
                if error["type"] == _PYDANTIC_VALUE_ERROR and "error" in context
                else error["msg"]
            )
            location = ".".join(str(part) for part in error["loc"])
            parts.append(f"{location}: {message}" if location else message)
        return " ".join(f"invalid {exc.title}: {'; '.join(parts)}".split())
    if isinstance(exc, ModelFileError) and subject is not None and _same_file(exc.path, subject):
        return " ".join(exc.reason.split())
    return " ".join(str(exc).split())


__all__ = [
    "CLI_LOG_FORMAT",
    "CLI_LOG_LEVEL",
    "EXIT_ERROR",
    "EXIT_OK",
    "EXIT_USAGE",
    "CliArgumentParser",
    "configure_cli_logging",
    "describe_failure",
]
