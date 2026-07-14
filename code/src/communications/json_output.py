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
from communications.engine import (
    CommsTrajectory,
    IridiumArpuBucket,
    IridiumArpuResult,
    arpu_stated_assumptions,
    iridium_assumptions,
    run_comms_model,
)

logger = logging.getLogger(__name__)

MODEL_NAME: Final[str] = "iridium"
"""The promoted artifact's model name (the provenance header's fixed identity)."""

IRIDIUM_SCHEMA_VERSION: Final[str] = "iridium-v3"
"""The promoted Iridium artifact's schema version tag. ``iridium-v3`` (2026-07-10)
removes the two cost-plus revenue fields (``steady_state_revenue_cost_plus_musd``,
``steady_state_gross_margin_cost_plus_pct``) from the trajectory summary: the Iridium
model now has a real published revenue case (the four-bucket ARPU case), so the
synthetic cost-plus line is off every Iridium-facing surface (it stays the cellular
family's shared-engine cost-recovery convention). The prior ``iridium-v2`` (2026-07-09)
removed the two inherited placeholder ARPU fields and added the published four-bucket
``revenue_arpu_buckets`` block, which carries the per-bucket lines plus the published
ARPU margin against the fleet's steady-state annual cost
(``arpu_margin_vs_steady_state_cost_pct``, unchanged: measured against cost, not
cost-plus)."""

JSON_INDENT: Final[int] = 2
"""Indentation for the emitted JSON (the house ``model_dump_json`` convention)."""

ARPU_MARGIN_PERCENT_SCALE: Final[float] = 100.0
"""Percent scale for the published ARPU margin: ``(revenue - cost) / revenue`` times
this yields a percentage (e.g. 0.982 -> 98.2), mirroring the model's fleet-margin
convention so every margin in the workstream reads in the same unit."""

ARPU_MARGIN_UNDEFINED_PCT: Final[float] = 0.0
"""The ARPU margin when revenue is non-positive (an empty pool): undefined, so it
reports 0.0 rather than dividing by zero. The block only exists on a populated pool
(revenue strictly positive), so this guard is defensive, mirroring the engine's
zero-revenue margin guard."""

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
    the build-and-hold cost, the fleet sizing and its binding regime, and the
    steady-state cost basis. After schema iridium-v3 (investor direction
    2026-07-10) this block carries the cost and fleet story ONLY, no revenue
    case: the two cost-plus revenue fields were removed from the Iridium
    artifact (the cellular family still earns cost-plus on the shared engine),
    and the published Iridium revenue is the four-bucket ``revenue_arpu_buckets``
    block on the artifact. The two inherited placeholder ARPU fields (from the
    cellular family's $50 default) were removed earlier in schema iridium-v2.
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
    # Two families of shared-engine fields are computed-but-unpublished for Iridium:
    # removed from this block but KEPT on the engine's shared CommsTrajectory (the
    # cellular family reads them, and the equality tripwire rides that shared
    # trajectory), so they must NOT be removed from the engine path:
    #   - the cost-plus revenue case (steady_state_revenue_cost_plus_musd,
    #     steady_state_gross_margin_cost_plus_pct), REMOVED here in schema iridium-v3
    #     (investor direction 2026-07-10): the Iridium model now has a real published
    #     revenue case, so the synthetic cost-plus line is off every Iridium-facing
    #     surface, while it stays the cellular family's cost-recovery convention;
    #   - the two inherited placeholder ARPU fields (steady_state_revenue_arpu_musd,
    #     steady_state_gross_margin_arpu_pct), REMOVED in schema iridium-v2: computed
    #     from the cellular family's $50/month default, they never described Iridium.
    # The published Iridium revenue is the revenue_arpu_buckets block below.


class ArpuBucketBlock(BaseModel):
    """One published ARPU revenue bucket (a mix slice of the billable-connection pool).

    Counts are people for standard/premium, DEVICES for IoT, contracts for
    government: never summed as one population (the pool is an accounting frame).
    """

    model_config = ConfigDict(frozen=True)

    mix_pct: float = Field(
        description="The bucket's share of the billable-connection pool, percent."
    )
    price_usd_per_month: float = Field(
        description="The bucket's monthly price, USD per connection per month."
    )
    count: int = Field(
        description="The derived connection count (people, IoT devices, or contracts)."
    )
    annual_revenue_musd: float = Field(description="The bucket's annual revenue, $M/yr.")


class RevenueArpuBucketsBlock(BaseModel):
    """The published four-bucket ARPU revenue case (a top-level artifact block).

    Present only when the scenario carries an ``arpu`` block; the whole block is
    omitted (the artifact field is None) on the no-ARPU path. The four buckets
    partition ONE pool anchored to fleet capacity, so every count scales with the
    satellite count. Subscribers are PEOPLE (standard, premium); IoT are DEVICES;
    government is a contract line: ``total_connections`` is a billable-connections
    accounting total, NOT one summed people population.
    """

    model_config = ConfigDict(frozen=True)

    standard: ArpuBucketBlock = Field(
        description="The standard personal (phone-class) people bucket."
    )
    premium: ArpuBucketBlock = Field(
        description="The premium terminal (gain-antenna) people bucket."
    )
    iot: ArpuBucketBlock = Field(description="The IoT DEVICE bucket (the mix residual to 100).")
    government: ArpuBucketBlock = Field(description="The government contract bucket.")
    total_connections: int = Field(
        description="The billable-connection pool size (people + devices + contracts)."
    )
    arpu_revenue_total_musd: float = Field(
        description="The summed annual revenue across the four buckets, $M/yr."
    )
    arpu_margin_vs_steady_state_cost_pct: float = Field(
        description=(
            "The published ARPU margin: ARPU revenue less the fleet's full steady-state "
            "annual cost (build, launch, replacement), over ARPU revenue, percent. "
            "Operations is the explicit zero and corporate overhead is excluded: an "
            "operating-style margin, not a gross margin and not a net margin."
        )
    )
    stated_assumptions: tuple[str, ...] = Field(
        description=(
            "The ARPU case's stated-assumption strings (full sell-through, the mix "
            "posture, the built-fleet convention), from arpu_stated_assumptions()."
        )
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
    revenue_arpu_buckets: RevenueArpuBucketsBlock | None = Field(
        default=None,
        description=(
            "The published four-bucket ARPU revenue case; None (omitted) when the "
            "scenario carries no arpu block."
        ),
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


def _arpu_bucket_block(bucket: IridiumArpuBucket) -> ArpuBucketBlock:
    """Map one engine ARPU bucket onto its promoted-artifact block."""
    return ArpuBucketBlock(
        mix_pct=bucket.mix_pct,
        price_usd_per_month=bucket.price_usd_month,
        count=bucket.count,
        annual_revenue_musd=bucket.revenue_musd_yr,
    )


def _arpu_margin_vs_steady_state_cost_pct(
    arpu_revenue_total_musd: float, steady_state_annual_cost_musd: float
) -> float:
    """The published ARPU margin against the fleet's full steady-state annual cost.

    ``(revenue - cost) / revenue x 100``. The cost basis is the fleet's full
    build-launch-replacement steady-state annual cost; operations is the explicit
    zero and corporate overhead is excluded, so this is an operating-style margin,
    not a gross margin and not a net margin. Mirrors the engine's zero-revenue guard.

    Args:
        arpu_revenue_total_musd: The summed four-bucket ARPU revenue, $M/yr.
        steady_state_annual_cost_musd: The fleet's representative HOLD-phase
            annualized cost, $M/yr (build, launch, replacement).

    Returns:
        The margin in percent, or :data:`ARPU_MARGIN_UNDEFINED_PCT` when revenue is
        not positive.
    """
    if arpu_revenue_total_musd <= 0.0:
        return ARPU_MARGIN_UNDEFINED_PCT
    return (
        (arpu_revenue_total_musd - steady_state_annual_cost_musd)
        / arpu_revenue_total_musd
        * ARPU_MARGIN_PERCENT_SCALE
    )


def _build_arpu_buckets_block(
    result: IridiumArpuResult,
    steady_state_annual_cost_musd: float,
    stated_assumptions: tuple[str, ...],
) -> RevenueArpuBucketsBlock:
    """Map the engine's IridiumArpuResult onto the promoted revenue_arpu_buckets block.

    Args:
        result: The engine's computed four-bucket ARPU result.
        steady_state_annual_cost_musd: The trajectory's steady-state annual fleet cost,
            $M/yr, the margin's cost basis.
        stated_assumptions: The ARPU-case posture strings (from
            :func:`~communications.engine.arpu_stated_assumptions`), carried inline.

    Returns:
        The populated :class:`RevenueArpuBucketsBlock`.
    """
    return RevenueArpuBucketsBlock(
        standard=_arpu_bucket_block(result.standard),
        premium=_arpu_bucket_block(result.premium),
        iot=_arpu_bucket_block(result.iot),
        government=_arpu_bucket_block(result.government),
        total_connections=result.total_connections,
        arpu_revenue_total_musd=result.arpu_revenue_total_musd_yr,
        arpu_margin_vs_steady_state_cost_pct=_arpu_margin_vs_steady_state_cost_pct(
            result.arpu_revenue_total_musd_yr, steady_state_annual_cost_musd
        ),
        stated_assumptions=stated_assumptions,
    )


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
    )
    # IoT SUPERSESSION (one IoT truth): with the ARPU case on, the published IoT device
    # count is the revenue mix's IoT bucket count; the fixed iot_devices passthrough
    # reports only on the no-ARPU path.
    published_iot_devices = (
        physics.arpu.iot.count if physics.arpu is not None else physics.iot_devices
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
        iot_devices=published_iot_devices,
        operations_cost_musd=physics.operations_cost_musd,
        ecosystem_assumption=physics.ecosystem_assumption,
    )
    revenue_arpu_buckets = (
        _build_arpu_buckets_block(
            physics.arpu,
            trajectory.steady_state_annual_cost_musd,
            arpu_stated_assumptions(config.iridium.arpu),
        )
        if physics.arpu is not None and config.iridium.arpu is not None
        else None
    )
    return IridiumModelArtifact(
        provenance=provenance,
        trajectory_summary=trajectory_summary,
        iridium_physics=iridium_physics,
        revenue_arpu_buckets=revenue_arpu_buckets,
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
