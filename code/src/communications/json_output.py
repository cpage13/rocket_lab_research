"""Promoted JSON artifact writer for the Iridium model (formerly Model B).

Runs the Iridium scenario through :func:`communications.engine.run_comms_model`
and writes the promoted JSON artifact: a small provenance header, the shared
trajectory summary (the headline fields every comms run reports), the Iridium
physics block (the :class:`~communications.engine.IridiumResult` fields), and
the stated-assumptions lines from
:func:`~communications.engine.iridium_assumptions`. It mirrors the data-center
promotion pattern (``data_center.json_output`` + the ``rklb-value --promote``
path): a typed Pydantic artifact serialized with ``model_dump_json(indent=2)``,
written into the repo-root ``communications/models/`` workstream.

Command-line usage, from the repo root::

    uv run --directory code python -m communications.json_output \\
        scenarios/iridium.yaml communications/models/iridium/default.json

A relative OUTPUT path is anchored to the REPO ROOT (promoted artifacts live in
the repo-root ``communications/models/`` workstream, never under ``code/``),
while a relative SCENARIO path resolves against the working directory as usual,
so the documented command works verbatim from ``code/``. The version stamp is
whatever string the caller passes (``--version-stamp``, e.g. a git-describe
output); it defaults to today's ISO date.
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date
from pathlib import Path
from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from communications.config import CommsConfig, load_comms_config
from communications.constants import BindingRegime, DeviceClass
from communications.engine import CommsTrajectory, iridium_assumptions, run_comms_model

logger = logging.getLogger(__name__)

MODEL_NAME: Final[str] = "iridium"
"""The promoted artifact's model name (the provenance header's fixed identity)."""

IRIDIUM_SCHEMA_VERSION: Final[str] = "iridium-v1"
"""The promoted Iridium artifact's schema version tag."""

JSON_INDENT: Final[int] = 2
"""Indentation for the emitted JSON (the house ``model_dump_json`` convention)."""

EXIT_OK: Final[int] = 0
"""Process exit code for a successful promotion."""

EXIT_ERROR: Final[int] = 1
"""Process exit code when the scenario fails to load or run."""

# The repo root, anchored from this file: src/communications -> src -> code -> root.
_REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[3]


class IridiumProvenance(BaseModel):
    """The promoted artifact's small provenance header.

    Records what produced the artifact: the model name, the schema version, the
    scenario label and YAML path, and the caller-supplied version stamp (a
    git-describe string or a date).
    """

    model_config = ConfigDict(frozen=True)

    model_name: str = Field(description="The model this artifact belongs to: 'iridium'.")
    schema_version: str = Field(description="The promoted Iridium artifact schema version.")
    scenario_name: str = Field(
        description="The scenario label (from the IridiumDials scenario_name single home)."
    )
    source_scenario_path: str = Field(
        description="Repo-relative path to the scenario YAML this artifact was run from."
    )
    version_stamp: str = Field(
        description="Caller-supplied stamp (git-describe or a date string; default today)."
    )


class IridiumPhysicsBlock(BaseModel):
    """The Iridium physics result block (the ``IridiumResult`` fields, one for one).

    All derived quantities are estimate-tier. Subscribers are PEOPLE;
    ``iot_devices`` is a separate DEVICE passthrough, never folded into the
    people count.
    """

    model_config = ConfigDict(frozen=True)

    spectrum_mhz: float = Field(description="The held L-band width used, MHz (a width).")
    aperture_m2: float = Field(description="The satellite flat-array area used, m^2.")
    device_class: DeviceClass = Field(
        description="The device class that set the spectral-efficiency tier."
    )
    spectral_efficiency_bps_per_hz: float = Field(
        description="The resolved spectral efficiency used, bps/Hz."
    )
    per_satellite_capacity_gbps: float = Field(
        description="The derived per-satellite capacity, Gbps."
    )
    fleet_aggregate_capacity_gbps: float = Field(
        description="Per-satellite capacity times the fleet target, Gbps."
    )
    subscribers_per_satellite: int = Field(
        description="The derived per-satellite density (people) that sized the fleet."
    )
    effective_satellites_per_launch: int = Field(
        description="The aperture-coupled per-launch count the deployment used."
    )
    active_user_rate_mbps: float = Field(
        description="The per-subscriber active data rate, Mbps (the service tier)."
    )
    concurrency_peak: float = Field(description="The busy-hour peak concurrency fraction.")
    concurrency_offpeak: float = Field(description="The off-peak concurrency fraction.")
    beam_pool_mbps: float = Field(
        description="The single-beam Shannon pool (spectrum times SE), Mbps."
    )
    per_user_rate_peak_mbps: float = Field(
        description="The peak per-user rate, Mbps (the active rate by construction)."
    )
    per_user_rate_offpeak_mbps: float = Field(
        description="The off-peak per-user rate, Mbps (capped by the beam pool)."
    )
    iot_devices: int = Field(
        description="The passthrough IoT DEVICE count (not people; zero sizing effect)."
    )
    operations_cost_musd: float = Field(
        description="The Iridium model's operations cost, $M (0.0, an explicit assumption)."
    )
    ecosystem_assumption: str = Field(
        description="The stated ecosystem assumption behind the phone-class tier."
    )


class TrajectorySummaryBlock(BaseModel):
    """The shared trajectory headline fields (the ``CommsTrajectory`` summary).

    These are the fields every comms run reports (the fleet machinery the
    Iridium model shares with the High-Bandwidth Cellular Pure Play model):
    the build-and-hold cost, the fleet sizing and its binding regime, the
    steady-state cost basis, and the two revenue cases.
    """

    model_config = ConfigDict(frozen=True)

    total_build_and_hold_cost_musd: float = Field(
        description="Cumulative build-and-hold cost over the trajectory, $M."
    )
    fleet_target: int = Field(
        description="The capacity-sized fleet the build-out fills toward (satellites)."
    )
    subscribers_per_satellite: int = Field(
        description="The per-satellite density that sized the fleet (people)."
    )
    binding_regime: BindingRegime = Field(
        description="Which constraint set the fleet target: coverage, capacity, or saturated."
    )
    full_coverage_reached_year: int | None = Field(
        description="First fiscal year the living fleet hit the target; None if never."
    )
    steady_state_annual_replacement_cost_musd: float = Field(
        description="Representative HOLD-phase annual replacement cost, $M."
    )
    subscribers_served: int = Field(
        description="Served people at the final year's buildout fraction."
    )
    cost_per_subscriber_annual_usd: float = Field(
        description="Steady-state annual cost per subscriber, USD/sub/yr (the headline)."
    )
    steady_state_annual_cost_musd: float = Field(
        description="Representative HOLD-phase ANNUALIZED fleet cost, $M/yr."
    )
    steady_state_revenue_cost_plus_musd: float = Field(
        description="Steady-state COST-PLUS annual revenue, $M/yr (the load-bearing case)."
    )
    steady_state_gross_margin_cost_plus_pct: float = Field(
        description="Steady-state COST-PLUS gross margin, percent."
    )
    steady_state_revenue_arpu_musd: float = Field(
        description="Steady-state PRICES-TODAY ARPU annual revenue, $M/yr (deferred case)."
    )
    steady_state_gross_margin_arpu_pct: float = Field(
        description="Steady-state ARPU gross margin, percent (deferred case)."
    )


class IridiumModelArtifact(BaseModel):
    """The complete promoted Iridium JSON artifact (the file's top level)."""

    model_config = ConfigDict(frozen=True)

    provenance: IridiumProvenance = Field(description="The small provenance header.")
    trajectory_summary: TrajectorySummaryBlock = Field(
        description="The shared trajectory headline fields."
    )
    iridium_physics: IridiumPhysicsBlock = Field(
        description="The Iridium physics result block (the IridiumResult fields)."
    )
    assumptions: tuple[str, ...] = Field(
        description="The stated-assumptions lines from iridium_assumptions(), in order."
    )


def _repo_relative(path: Path) -> str:
    """Return a repo-relative POSIX path when under the repo root, else as-posix.

    Args:
        path: The resolved filesystem path to describe.

    Returns:
        The provenance-friendly path string.
    """
    try:
        return path.relative_to(_REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def build_iridium_artifact(
    *,
    config: CommsConfig,
    trajectory: CommsTrajectory,
    source_scenario_path: str,
    version_stamp: str,
) -> IridiumModelArtifact:
    """Assemble the promoted artifact from a completed Iridium run.

    Pure assembly: no IO. The caller loads the config, runs the model, and
    passes both in (so the artifact always describes exactly the run it was
    built from).

    Args:
        config: The loaded scenario config (its ``iridium`` block must be set).
        trajectory: The completed run for that config.
        source_scenario_path: The provenance path string for the scenario YAML.
        version_stamp: The caller-supplied stamp (git-describe or a date string).

    Returns:
        The populated, frozen :class:`IridiumModelArtifact`.

    Raises:
        ValueError: If the config or trajectory does not carry the Iridium
            block (the scenario did not select the Iridium model).
    """
    if config.iridium is None or trajectory.iridium is None:
        raise ValueError(
            "the scenario does not select the Iridium model: it needs a top-level "
            "'iridium:' block (see scenarios/iridium.yaml)"
        )
    physics = trajectory.iridium
    provenance = IridiumProvenance(
        model_name=MODEL_NAME,
        schema_version=IRIDIUM_SCHEMA_VERSION,
        scenario_name=config.iridium.scenario_name,
        source_scenario_path=source_scenario_path,
        version_stamp=version_stamp,
    )
    trajectory_summary = TrajectorySummaryBlock(
        total_build_and_hold_cost_musd=trajectory.total_build_and_hold_cost_musd,
        fleet_target=trajectory.fleet_target,
        subscribers_per_satellite=trajectory.subscribers_per_satellite,
        binding_regime=trajectory.binding_regime,
        full_coverage_reached_year=trajectory.full_coverage_reached_year,
        steady_state_annual_replacement_cost_musd=(
            trajectory.steady_state_annual_replacement_cost_musd
        ),
        subscribers_served=trajectory.subscribers_served,
        cost_per_subscriber_annual_usd=trajectory.cost_per_subscriber_annual_usd,
        steady_state_annual_cost_musd=trajectory.steady_state_annual_cost_musd,
        steady_state_revenue_cost_plus_musd=trajectory.steady_state_revenue_cost_plus_musd,
        steady_state_gross_margin_cost_plus_pct=(
            trajectory.steady_state_gross_margin_cost_plus_pct
        ),
        steady_state_revenue_arpu_musd=trajectory.steady_state_revenue_arpu_musd,
        steady_state_gross_margin_arpu_pct=trajectory.steady_state_gross_margin_arpu_pct,
    )
    iridium_physics = IridiumPhysicsBlock(
        spectrum_mhz=physics.spectrum_mhz,
        aperture_m2=physics.aperture_m2,
        device_class=physics.device_class,
        spectral_efficiency_bps_per_hz=physics.spectral_efficiency_bps_per_hz,
        per_satellite_capacity_gbps=physics.per_satellite_capacity_gbps,
        fleet_aggregate_capacity_gbps=physics.fleet_aggregate_capacity_gbps,
        subscribers_per_satellite=physics.subscribers_per_satellite,
        effective_satellites_per_launch=physics.effective_satellites_per_launch,
        active_user_rate_mbps=physics.active_user_rate_mbps,
        concurrency_peak=physics.concurrency_peak,
        concurrency_offpeak=physics.concurrency_offpeak,
        beam_pool_mbps=physics.beam_pool_mbps,
        per_user_rate_peak_mbps=physics.per_user_rate_peak_mbps,
        per_user_rate_offpeak_mbps=physics.per_user_rate_offpeak_mbps,
        iot_devices=physics.iot_devices,
        operations_cost_musd=physics.operations_cost_musd,
        ecosystem_assumption=physics.ecosystem_assumption,
    )
    return IridiumModelArtifact(
        provenance=provenance,
        trajectory_summary=trajectory_summary,
        iridium_physics=iridium_physics,
        assumptions=iridium_assumptions(config.iridium),
    )


def render_json(artifact: IridiumModelArtifact) -> str:
    """Serialize the promoted artifact as indented JSON (the house convention).

    Args:
        artifact: The assembled promoted artifact.

    Returns:
        The artifact as an indented JSON string.
    """
    return artifact.model_dump_json(indent=JSON_INDENT)


def export_iridium_json(
    scenario_path: str | Path,
    output_path: str | Path,
    version_stamp: str | None = None,
) -> Path:
    """Run an Iridium scenario and write the promoted JSON artifact.

    Loads the scenario, runs :func:`~communications.engine.run_comms_model`,
    assembles the artifact, and writes it. A relative ``output_path`` is
    anchored to the REPO ROOT (the promoted ``communications/models/``
    workstream lives there, never under ``code/``); an absolute path is used
    as-is. The ``scenario_path`` resolves against the working directory as
    usual.

    Args:
        scenario_path: The scenario YAML to run (must select the Iridium model).
        output_path: Where to write the promoted JSON (relative = repo-root
            anchored).
        version_stamp: Optional stamp for the provenance header (git-describe
            or any string); defaults to today's ISO date.

    Returns:
        The resolved path the artifact was written to.

    Raises:
        FileNotFoundError: If the scenario YAML does not exist.
        ValueError: If the YAML is invalid or does not select the Iridium model.
    """
    scenario = Path(scenario_path)
    config = load_comms_config(scenario)
    trajectory = run_comms_model(config)
    stamp = version_stamp if version_stamp is not None else date.today().isoformat()
    artifact = build_iridium_artifact(
        config=config,
        trajectory=trajectory,
        source_scenario_path=_repo_relative(scenario.resolve()),
        version_stamp=stamp,
    )
    out = Path(output_path)
    if not out.is_absolute():
        out = _REPO_ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_json(artifact) + "\n", encoding="utf-8")
    logger.info("promoted Iridium model artifact written to %s", out)
    return out


def _build_parser() -> argparse.ArgumentParser:
    """Build the module's command-line parser."""
    parser = argparse.ArgumentParser(
        prog="python -m communications.json_output",
        description=(
            "Run the Iridium model (formerly Model B) from a scenario YAML and write "
            "the promoted JSON artifact into the repo-root communications/models/ "
            "workstream."
        ),
    )
    parser.add_argument(
        "scenario",
        help="Scenario YAML to run (must select the Iridium model), e.g. scenarios/iridium.yaml.",
    )
    parser.add_argument(
        "output",
        help=(
            "Promoted JSON path, e.g. communications/models/iridium/default.json "
            "(relative paths anchor to the repo root)."
        ),
    )
    parser.add_argument(
        "--version-stamp",
        default=None,
        help="Provenance stamp (git-describe or any string). Defaults to today's ISO date.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point. Returns a process exit code.

    Args:
        argv: Argument list (defaults to ``sys.argv[1:]``).

    Returns:
        ``EXIT_OK`` on success, ``EXIT_ERROR`` if the scenario fails to load
        or does not select the Iridium model.
    """
    args = _build_parser().parse_args(argv)
    try:
        written = export_iridium_json(args.scenario, args.output, args.version_stamp)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_ERROR
    print(f"promoted model -> {written}", file=sys.stderr)
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
