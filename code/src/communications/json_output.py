"""Promoted JSON artifact writer for the Iridium model (formerly Model B).

Runs an Iridium scenario through the Iridium entry,
:func:`communications.iridium.run_iridium_model`, on its saturation curve, and writes the
promoted JSON artifact, schema :data:`IRIDIUM_SCHEMA_VERSION`: a small provenance header,
the trajectory summary (the shared fleet-and-cost record's totals beside the Iridium
record's floor year and cost per satellite-year), the orbit scenario, the Iridium physics,
every device class's block (its price, usage, physics, markers, limit and marginal
intervals), every model year's lines (the shared fleet and cost beside each class's people,
revenue and own margin, and the two IoT lines), the fixed books, the saturation block (the
curve's identity, the downlink share and the panel factor, the readings at the reported
fleets, the phone class's band saturation numbers, the IoT check and the curve's limits)
and the stated assumptions. Every block that lists the classes lists them small terminal,
mounted terminal, phone class, never phone-first. It mirrors the data-center promotion
pattern (``data_center.json_output`` + the ``rklb-value --promote`` path): a typed Pydantic
artifact serialized by the shared :func:`common.file_io.render_artifact_json`, written into
the repo-root ``communications/models/`` folder.

The command is the Iridium promotion command only. It loads the scenario and
narrows it to its Iridium dials first
(:func:`communications.iridium.iridium_dials_of`), so a scenario without an
``iridium:`` block fails with the family's message before any curve is read or
any model runs. It then loads the promoted saturation curve that the scenario's
``iridium.saturation.curve_path`` names, with
:func:`communications.saturation_curve.load_saturation_curve` (an absolute path
is used as given; a relative one is anchored to the REPO ROOT, like the output
path), and runs the Iridium entry, which refuses a curve computed for other
inputs (the identity check) before the run; the command names the curve file
in that refusal, as the loader names it in its own. The cellular entry has no
command-line caller.

Command-line usage, from the repo root::

    uv run --directory code python -m communications.json_output \\
        scenarios/iridium.yaml communications/models/iridium/default.json

A relative OUTPUT path is anchored to the REPO ROOT (promoted artifacts live in
the repo-root ``communications/models/`` folder, never under ``code/``),
while a relative SCENARIO path resolves against the working directory as usual,
so the documented command works verbatim from ``code/``. The version stamp is
whatever string the caller passes (``--version-stamp``, e.g. a git-describe
output); it defaults to today's ISO date.

The command follows the shared CLI conventions (:mod:`common.cli`): the status
line and any error are log records on stderr; an unreadable or invalid
scenario, a scenario of the cellular family, a saturation curve that cannot be
read, was computed for other inputs, ends before a fleet the run reads or
measures no elasticity of capacity at the final year's fleet for a class it
gives no saturation number (that fleet past the one the curve names it not
reached by, so which limit binds there is not known), a
scenario the model cannot run (a value the model cannot compute among them), an
artifact that would hold a number that is not finite (the artifact's models refuse
one, so no value is ever written as null in its place), or a failed write is one
``ERROR:`` line and exit status 1, never a traceback; a usage error exits with status 2.
The one artifact is written through
:func:`common.file_io.write_files_with_rollback`: staged in full beside its
destination, then renamed over it in one atomic rename, so a failure leaves
the promoted file as it was (a destination that is a symbolic link or not a
regular file is refused). It runs from a source checkout only
(:func:`common.file_io.locate_source_checkout`).
"""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path
from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from common.cli import (
    EXIT_ERROR,
    EXIT_OK,
    CliArgumentParser,
    configure_cli_logging,
    describe_failure,
)
from common.file_io import (
    ModelFileError,
    artifact_write,
    locate_source_checkout,
    write_files_with_rollback,
)
from common.input_manifest import SourceStatus
from communications.config import load_comms_config
from communications.constants import (
    ORBIT_ALTITUDE_KM_SCENARIO,
    ORBIT_INCLINATION_DEG_SCENARIO,
    ORBIT_SCENARIO_BASIS,
    ORBIT_SCENARIO_SOURCE_STATUS,
    DeviceClass,
)
from communications.engine import FleetTrajectory
from communications.iridium import (
    BindingLimit,
    ClassReadingRecord,
    ClassRecord,
    ClassYearRecord,
    FixedBooksRecord,
    IotCheckRowRecord,
    IridiumRecord,
    MarginalIntervalRecord,
    ReadingRecord,
    SaturationRecord,
    iridium_dials_of,
    run_iridium_model,
)
from communications.saturation_curve import (
    BandName,
    SaturationCurveMismatchError,
    load_saturation_curve,
)

logger = logging.getLogger(__name__)

MODEL_NAME: Final[str] = "iridium"
"""The promoted artifact's model name (the provenance header's fixed identity)."""

IRIDIUM_SCHEMA_VERSION: Final[str] = "iridium-v6"
"""The promoted Iridium artifact's schema version tag. ``iridium-v6`` (2026-10-06, the
saturation module's switch, approved 2026-10-04) publishes the Iridium model on the promoted
saturation curve and the launch cadence: every device class side by side (``classes``, each
with its price, usage, physics, markers, binding limit and marginal intervals), each model
year's people, revenue and own margin per class beside the shared fleet and cost and the two
IoT lines (``years``), the two IoT lines' fixed books (``fixed_books``), and the curve's
identity, readings, band saturation numbers, IoT check and limits (``saturation``). The
trajectory summary renames ``total_build_and_hold_cost_musd`` to
``total_cost_through_final_year_musd`` and ``steady_state_annual_cost_musd`` to
``final_year_annual_cost_musd``, replaces ``full_coverage_reached_year`` with
``coverage_floor_reached_year`` and adds ``cost_per_satellite_year_musd``; the physics block
keeps the spectrum, the panel, the operations cost and the ecosystem assumption and renames
``effective_satellites_per_launch`` to ``satellites_per_launch``. Removed: the target,
regime, completion and built-fleet fields, the per-person cost fields, the density and the
fleet aggregate, the IoT passthrough, the one device class and its physics (each class's now
in ``classes``), the served base ``subscribers_served`` and the living fleet's people capacity
``people_capacity_living_fleet_final_year`` (each class's people now in ``years`` and the
readings), and the four-bucket ``revenue_arpu_buckets`` block. Earlier versions, in
brief: ``iridium-v5`` (2026-09-23) made the edge cases honest (nullable final-year cash
figures, the built fleet's annualized cost as the ARPU margin's basis); ``iridium-v4``
(2026-07-14) named the cost bases and exposed the denominators the prose quoted, and added
the orbit scenario block; ``iridium-v3`` (2026-07-10) removed the cost-plus revenue fields;
``iridium-v2`` (2026-07-09) added the four-bucket ARPU block."""

_BLOCK_CONFIG: Final[ConfigDict] = ConfigDict(frozen=True, allow_inf_nan=False)
"""Every artifact block's configuration: frozen, and only finite numbers, so the artifact
never holds an infinity or a NaN (a quantity that does not exist is a null instead)."""


class IridiumProvenance(BaseModel):
    """The promoted artifact's small provenance header.

    Records what produced the artifact: the model name, the schema version, the
    scenario label and YAML path, and the caller-supplied version stamp (a
    git-describe string or a date).
    """

    model_config = _BLOCK_CONFIG

    model_name: str = Field(description="The model this artifact belongs to: 'iridium'.")
    schema_version: str = Field(description="The promoted Iridium artifact schema version.")
    scenario_name: str = Field(
        description="The scenario label (from the IridiumDials scenario_name single home)."
    )
    source_scenario_path: str = Field(
        description=(
            "The scenario YAML this artifact was run from: repository-relative, or its absolute "
            "path when it lies outside the repository."
        )
    )
    version_stamp: str = Field(
        description="Caller-supplied stamp (git-describe or a date string; default today)."
    )


class TrajectorySummaryBlock(BaseModel):
    """The trajectory's headline fields: the shared fleet-and-cost record's totals and final
    year, with the year the coverage floor is reached and the cost per satellite-year.

    The fleet is every comms launch the cadence share allows: there is no fleet target, no
    hold and no completion year. People, revenue and margins are per class, in ``years`` and
    the readings.
    """

    model_config = _BLOCK_CONFIG

    total_cost_through_final_year_musd: float = Field(
        description="The cumulative deployment cash (build and launch) over the horizon, $M."
    )
    final_year_annual_cost_musd: float = Field(
        description=(
            "The final model year's annualized fleet cost, $M a year: each living cohort's "
            "build and launch cost spread over the satellite life, at its launch year's price "
            "(0.0 with nothing on orbit). Not the steady state, which is a reading."
        )
    )
    final_year_replacement_cost_musd: float | None = Field(
        description=(
            "The final model year's cash replacement cost, $M: the satellites that replace "
            "that year's retiring cohort, at their build cost plus their launches at the "
            "year's price; cohort-timed and lumpy, not an annualized basis. None when the "
            "final year replaced no retiring cohort."
        )
    )
    living_fleet_final_year: int = Field(
        description="Living satellites at the final model year (the horizon-end reach)."
    )
    cumulative_launches_final_year: int = Field(
        description="Cumulative comms launches flown through the final model year."
    )
    coverage_floor_reached_year: int | None = Field(
        description=(
            "The first fiscal year the living fleet is at or above the coverage floor, when "
            "every class and both IoT lines start selling; None when the floor is never "
            "reached."
        )
    )
    cost_per_satellite_year_musd: float = Field(
        description=(
            "One satellite's annualized cost at the final year's launch price, $M a year: what "
            "a final-year cohort would lock in (defined even when no cohort flies). The basis "
            "of the marginal intervals and of the readings at fleets the trajectory does not "
            "hold."
        )
    )


class OrbitScenarioBlock(BaseModel):
    """The published orbit posture, carried as a labeled SCENARIO block.

    No config dial sets these values: they are named constants, and the saturation curve's
    shell is computed at them (450 km, 53 degrees, the 25 degree mask), so the readings rest
    on this posture. The block (introduced in iridium-v4) gives the public orbit claim in the
    conclusion and the assumptions ledger a typed model-contract anchor that travels with its
    limitations. Values and basis text come from :mod:`communications.constants`.
    """

    model_config = _BLOCK_CONFIG

    altitude_km: float = Field(
        description="The published fleet altitude, km (a stated scenario, not derived)."
    )
    inclination_deg: float = Field(
        description="The published fleet inclination, degrees (a stated scenario, not derived)."
    )
    source_status: SourceStatus = Field(
        description="The assumptions-ledger source status for the orbit: 'scenario'."
    )
    basis: str = Field(
        description=(
            "The simulation support and its honest bounds (metric, phasing, "
            "weighting, availability limitations), carried verbatim."
        )
    )


class IridiumPhysicsBlock(BaseModel):
    """The run's Iridium settings and the two stated physics notes; each class's physics is in
    its own block in ``classes``."""

    model_config = _BLOCK_CONFIG

    spectrum_mhz: float = Field(description="The held L-band width, MHz (a width).")
    aperture_m2: float = Field(
        description="The satellite's flat panel, m^2, applied linearly on the curve."
    )
    satellites_per_launch: int = Field(
        description="The satellites one launch carries, the scenario's direct value."
    )
    operations_cost_musd: float = Field(
        description="The Iridium model's operations cost, $M (0.0, an explicit assumption)."
    )
    ecosystem_assumption: str = Field(
        description="The stated ecosystem assumption behind the phone class."
    )


class MarginalIntervalBlock(BaseModel):
    """One interval of a class's curve rows and what one more satellite adds across it."""

    model_config = _BLOCK_CONFIG

    lower_fleet: int = Field(description="The interval's lower fleet (0 for the first).")
    upper_fleet: int = Field(description="Its upper fleet, a row of the class's curve.")
    people_added_per_satellite: float = Field(
        description=(
            "The people one more satellite adds across the interval, at the downlink share "
            "and the panel factor: the chord of the class's people between the two fleets."
        )
    )
    revenue_per_satellite_year_musd: float = Field(
        description="Those people at the class's price for a year, $M."
    )
    pays: bool = Field(
        description=(
            "Whether that revenue is at least the cost per satellite-year (full price; a "
            "haircut moves every stop earlier)."
        )
    )


class ClassBlock(BaseModel):
    """One device class: its price, usage, physics, markers, binding limit and intervals.

    The class's column is the whole fleet sold to that class alone. Its markers are the
    curve's own (fleets on the curve's basis; the maximum use times the panel factor).
    """

    model_config = _BLOCK_CONFIG

    device_class: DeviceClass = Field(description="The class.")
    price_usd_per_month: float = Field(description="Its flat monthly price, dollars.")
    active_user_rate_mbps: float = Field(description="Its rate while active, Mbps (its usage).")
    concurrency_peak: float = Field(description="Its busy-hour share of users active at once.")
    concurrency_offpeak: float = Field(description="Its off-peak share of users active.")
    spectral_efficiency_bps_per_hz: float = Field(
        description="Its central spectral efficiency, bps/Hz."
    )
    per_satellite_capacity_gbps: float = Field(
        description=(
            "The satellite's peak for the class, every beam lit and used and the band full "
            "time, times the panel factor, Gbps."
        )
    )
    beam_pool_mbps: float = Field(description="One beam's downlink pool, W x SE x d, Mbps.")
    per_user_rate_peak_mbps: float = Field(
        description="The peak per-user rate, Mbps (the rate while active)."
    )
    per_user_rate_offpeak_mbps: float = Field(
        description=(
            "The off-peak per-user rate, Mbps: the lower of the pool and the rate times the "
            "busy-hour share over the off-peak share."
        )
    )
    maximum_use_beams: float = Field(
        description=(
            "The most beams the shell could ever use for the class, times the panel factor."
        )
    )
    saturation_number: int | None = Field(
        description=(
            "The class's spectrum bound: the fleet at which one more satellite adds less than "
            "10 percent of an average satellite's capacity; None when not reached on the curve."
        )
    )
    saturation_not_reached_by: int | None = Field(
        description=(
            "When the saturation number is not reached, the last fleet at which the curve's "
            "rows measure the elasticity (their last midpoint, the geometric mean of the last two "
            "rows' fleets, rounded half up); else None."
        )
    )
    elasticity_under_0p25_fleet: int | None = Field(
        description="The fleet at the first elasticity crossing under 0.25, or None."
    )
    fleet_at_90pct_of_maximum_use: int | None = Field(
        description="The fleet at which useful beams reach 90 percent of maximum use, or None."
    )
    binding_limit_at_horizon_end: BindingLimit = Field(
        description=(
            "What bounds the class's fleet at the horizon's end: spectrum when the final "
            "year's living fleet is at or past the saturation number, else the launch "
            "cadence. Reported only: no saturation number caps the build."
        )
    )
    marginal_intervals: tuple[MarginalIntervalBlock, ...] = Field(
        description=(
            "Every interval of the class's curve rows, from 0 to the first row and then "
            "between consecutive rows."
        )
    )


class ClassYearBlock(BaseModel):
    """One class's line in one model year."""

    model_config = _BLOCK_CONFIG

    device_class: DeviceClass = Field(description="The class.")
    people_served: int = Field(
        description=(
            "Every person the living fleet carries for the class (every seat sold); 0 below "
            "the coverage floor."
        )
    )
    revenue_musd: float = Field(
        description="Those people at the class's price for the year, $M; 0.0 below the floor."
    )
    own_margin_pct: float | None = Field(
        description=(
            "The class's own revenue against the year's whole-fleet annualized cost, percent "
            "(the IoT lines never inside it); null when the revenue is 0.0."
        )
    )


class YearBlock(BaseModel):
    """One model year: the shared fleet and cost, the two IoT lines and each class's line."""

    model_config = _BLOCK_CONFIG

    year: int = Field(description="The fiscal year.")
    comms_launches_flown: int = Field(description="The comms launches flown this year.")
    living_fleet: int = Field(description="The living satellites this year.")
    annual_cost_musd: float = Field(
        description="The year's annualized fleet cost, $M (the margins' cost basis)."
    )
    minimal_packet_iot_revenue_musd: float = Field(
        description="Minimal-packet IoT's book, $M; 0.0 below the coverage floor."
    )
    data_iot_revenue_musd: float = Field(
        description="Data IoT's book, $M; 0.0 below the coverage floor."
    )
    classes: tuple[ClassYearBlock, ...] = Field(description="Each class's line, in class order.")


class FixedBooksBlock(BaseModel):
    """The two IoT lines (ADR 007): fixed counts at their prices, each its own line; there is
    no combined total and no government line."""

    model_config = _BLOCK_CONFIG

    minimal_packet_iot_devices: int = Field(description="Minimal-packet IoT's fixed count.")
    minimal_packet_iot_price_usd_per_month: float = Field(
        description="Its monthly price per device, dollars."
    )
    minimal_packet_iot_annual_revenue_musd: float = Field(
        description="Its book, $M a year, from the year the coverage floor is reached."
    )
    data_iot_devices: int = Field(description="Data IoT's fixed count.")
    data_iot_price_usd_per_month: float = Field(
        description="Its monthly price per device, dollars."
    )
    data_iot_annual_revenue_musd: float = Field(
        description="Its book, $M a year, from the year the coverage floor is reached."
    )
    basis: str = Field(description="Where the counts come from and how the lines are sold.")


class ClassReadingBlock(BaseModel):
    """One class at one reported fleet."""

    model_config = _BLOCK_CONFIG

    device_class: DeviceClass = Field(description="The class.")
    useful_beams: float = Field(
        description="The co-channel beams over people at the fleet, times the panel factor."
    )
    share_of_maximum_use: float = Field(description="Useful beams over the maximum use.")
    ocean_factor: float | None = Field(
        description=(
            "U, the share of the beams offered that lie over people; null at a fleet of 0."
        )
    )
    people: int = Field(description="The people the fleet carries for the class.")
    revenue_musd: float = Field(
        description="Those people at the class's price for a year, $M; 0.0 below the floor."
    )
    own_margin_pct: float | None = Field(
        description="That revenue against the reading's fleet cost, percent; null at 0.0."
    )


class ReadingBlock(BaseModel):
    """Every class at one reported fleet."""

    model_config = _BLOCK_CONFIG

    label: str = Field(description="What the fleet is.")
    fleet: int = Field(description="The fleet, satellites.")
    fleet_annual_cost_musd: float = Field(
        description=(
            "The reading's cost, $M a year: the final year's annualized cost at the "
            "horizon-end reach, else the fleet times the cost per satellite-year."
        )
    )
    classes: tuple[ClassReadingBlock, ...] = Field(
        description="Each class's reading, in class order."
    )


class IotCheckRowBlock(BaseModel):
    """One IoT line at one reported fleet; every field but ``fleet`` null below the floor."""

    model_config = _BLOCK_CONFIG

    fleet: int = Field(description="The fleet, satellites.")
    devices_per_useful_beam: float | None = Field(
        description="The line's devices over the phone class's useful beams."
    )
    uplink_bits_share: float | None = Field(
        description=(
            "A beam's daily bits for the line over its uplink's daily bits (the frame's "
            "share 1 - d), a fraction; null with no uplink time."
        )
    )
    uplink_bits_share_with_mac: float | None = Field(
        description="The same over the MAC efficiency, a fraction."
    )
    access_attempts_per_second_per_beam: float | None = Field(
        description="One access attempt per message or burst, a second a beam."
    )
    uplink_tone_share_low: float | None = Field(
        description=(
            "The messages' channel time over the uplink's tone time at the low airtime, a "
            "fraction. Null for data IoT: its bursts are not single-tone messages, and the "
            "tone time of the single-tone messages it sends beside them goes unreported."
        )
    )
    uplink_tone_share_high: float | None = Field(
        description=(
            "The same at the high airtime, a fraction; null for data IoT, whose messages' "
            "tone time goes unreported (as above)."
        )
    )


class IotCheckBlock(BaseModel):
    """The IoT check at the reported fleets, each line on its own."""

    model_config = _BLOCK_CONFIG

    minimal_packet_iot: tuple[IotCheckRowBlock, ...] = Field(
        description="Minimal-packet IoT's rows, one per reported fleet."
    )
    data_iot: tuple[IotCheckRowBlock, ...] = Field(
        description="Data IoT's rows, one per reported fleet."
    )


class SaturationBlock(BaseModel):
    """The curve the run read and what it read from it."""

    model_config = _BLOCK_CONFIG

    curve_path: str = Field(
        description="The scenario's curve path (repository-relative, or absolute as given)."
    )
    curve_schema_version: str = Field(description="The curve's schema version.")
    curve_version_stamp: str = Field(description="The curve's version stamp.")
    input_hash: str = Field(description="The curve's input hash.")
    downlink_share: float = Field(description="The downlink share d the run read the curve at.")
    panel_factor: float = Field(
        description="The scenario's panel over the curve's reference panel."
    )
    readings: tuple[ReadingBlock, ...] = Field(
        description=(
            "The readings at the coverage floor, the retired cap (kept for comparison), the "
            "horizon-end full-cadence reach and the steady state beyond the horizon."
        )
    )
    band_saturation_numbers: dict[BandName, int | None] = Field(
        description=(
            "The phone class's band points' saturation numbers (null when not reached), in "
            "band order."
        )
    )
    iot_check: IotCheckBlock = Field(description="The IoT check.")
    limits: tuple[str, ...] = Field(description="The curve's stated limits, carried over.")


class IridiumModelArtifact(BaseModel):
    """The complete promoted Iridium JSON artifact (the file's top level)."""

    model_config = _BLOCK_CONFIG

    provenance: IridiumProvenance = Field(description="The small provenance header.")
    trajectory_summary: TrajectorySummaryBlock = Field(
        description="The trajectory's headline fields."
    )
    orbit_scenario: OrbitScenarioBlock = Field(
        description="The published orbit posture (a labeled scenario with its limitations)."
    )
    iridium_physics: IridiumPhysicsBlock = Field(
        description="The run's Iridium settings and stated physics notes."
    )
    classes: tuple[ClassBlock, ...] = Field(description="Each device class's block, in order.")
    years: tuple[YearBlock, ...] = Field(description="Each model year's lines.")
    fixed_books: FixedBooksBlock = Field(description="The two IoT lines' books.")
    saturation: SaturationBlock = Field(description="The curve and its readings.")
    assumptions: tuple[str, ...] = Field(description="The stated-assumptions lines, in order.")


def _interval_block(interval: MarginalIntervalRecord) -> MarginalIntervalBlock:
    """Map one marginal interval onto its block."""
    return MarginalIntervalBlock(
        lower_fleet=interval.lower_fleet,
        upper_fleet=interval.upper_fleet,
        people_added_per_satellite=interval.people_added_per_satellite,
        revenue_per_satellite_year_musd=interval.revenue_per_satellite_year_musd,
        pays=interval.pays,
    )


def _class_block(record: ClassRecord) -> ClassBlock:
    """Map one class's record onto its block."""
    return ClassBlock(
        device_class=record.device_class,
        price_usd_per_month=record.price_usd_per_month,
        active_user_rate_mbps=record.active_user_rate_mbps,
        concurrency_peak=record.concurrency_peak,
        concurrency_offpeak=record.concurrency_offpeak,
        spectral_efficiency_bps_per_hz=record.spectral_efficiency_bps_per_hz,
        per_satellite_capacity_gbps=record.per_satellite_capacity_gbps,
        beam_pool_mbps=record.beam_pool_mbps,
        per_user_rate_peak_mbps=record.per_user_rate_peak_mbps,
        per_user_rate_offpeak_mbps=record.per_user_rate_offpeak_mbps,
        maximum_use_beams=record.maximum_use_beams,
        saturation_number=record.saturation_number,
        saturation_not_reached_by=record.saturation_not_reached_by,
        elasticity_under_0p25_fleet=record.elasticity_under_0p25_fleet,
        fleet_at_90pct_of_maximum_use=record.fleet_at_90pct_of_maximum_use,
        binding_limit_at_horizon_end=record.binding_limit_at_horizon_end,
        marginal_intervals=tuple(_interval_block(each) for each in record.marginal_intervals),
    )


def _class_year_block(line: ClassYearRecord) -> ClassYearBlock:
    """Map one class's line in a year onto its block."""
    return ClassYearBlock(
        device_class=line.device_class,
        people_served=line.people_served,
        revenue_musd=line.revenue_musd,
        own_margin_pct=line.own_margin_pct,
    )


def _year_blocks(fleet: FleetTrajectory, iridium: IridiumRecord) -> tuple[YearBlock, ...]:
    """Each model year: the shared record's year beside the Iridium record's year of the same
    index (both run over the same horizon, oldest first, keyed by the fiscal year).

    Raises:
        ValueError: If the two records' years do not match one for one (they always do for a
            run of the Iridium entry; a mismatch is a caller's error, never published).
    """
    if [year.year for year in fleet.years] != [year.year for year in iridium.years]:
        raise ValueError(
            "the shared record's years and the Iridium record's years must match one for one; "
            f"got {[year.year for year in fleet.years]} and "
            f"{[year.year for year in iridium.years]}"
        )
    return tuple(
        YearBlock(
            year=fleet_year.year,
            comms_launches_flown=fleet_year.comms_launches_flown_this_year,
            living_fleet=fleet_year.living_fleet,
            annual_cost_musd=fleet_year.annual_cost_this_year_musd,
            minimal_packet_iot_revenue_musd=iridium_year.minimal_packet_iot_revenue_musd,
            data_iot_revenue_musd=iridium_year.data_iot_revenue_musd,
            classes=tuple(_class_year_block(line) for line in iridium_year.classes),
        )
        for fleet_year, iridium_year in zip(fleet.years, iridium.years, strict=True)
    )


def _fixed_books_block(books: FixedBooksRecord) -> FixedBooksBlock:
    """Map the two IoT lines onto their block."""
    return FixedBooksBlock(
        minimal_packet_iot_devices=books.minimal_packet_iot_devices,
        minimal_packet_iot_price_usd_per_month=books.minimal_packet_iot_price_usd_per_month,
        minimal_packet_iot_annual_revenue_musd=books.minimal_packet_iot_annual_revenue_musd,
        data_iot_devices=books.data_iot_devices,
        data_iot_price_usd_per_month=books.data_iot_price_usd_per_month,
        data_iot_annual_revenue_musd=books.data_iot_annual_revenue_musd,
        basis=books.basis,
    )


def _class_reading_block(line: ClassReadingRecord) -> ClassReadingBlock:
    """Map one class's reading onto its block."""
    return ClassReadingBlock(
        device_class=line.device_class,
        useful_beams=line.useful_beams,
        share_of_maximum_use=line.share_of_maximum_use,
        ocean_factor=line.ocean_factor,
        people=line.people,
        revenue_musd=line.revenue_musd,
        own_margin_pct=line.own_margin_pct,
    )


def _reading_block(reading: ReadingRecord) -> ReadingBlock:
    """Map one reported fleet's readings onto its block."""
    return ReadingBlock(
        label=reading.label,
        fleet=reading.fleet,
        fleet_annual_cost_musd=reading.fleet_annual_cost_musd,
        classes=tuple(_class_reading_block(line) for line in reading.classes),
    )


def _iot_row_block(row: IotCheckRowRecord) -> IotCheckRowBlock:
    """Map one IoT check row onto its block."""
    return IotCheckRowBlock(
        fleet=row.fleet,
        devices_per_useful_beam=row.devices_per_useful_beam,
        uplink_bits_share=row.uplink_bits_share,
        uplink_bits_share_with_mac=row.uplink_bits_share_with_mac,
        access_attempts_per_second_per_beam=row.access_attempts_per_second_per_beam,
        uplink_tone_share_low=row.uplink_tone_share_low,
        uplink_tone_share_high=row.uplink_tone_share_high,
    )


def _saturation_block(record: SaturationRecord) -> SaturationBlock:
    """Map the curve's identity and readings onto the saturation block."""
    return SaturationBlock(
        curve_path=record.curve_path,
        curve_schema_version=record.curve_schema_version,
        curve_version_stamp=record.curve_version_stamp,
        input_hash=record.input_hash,
        downlink_share=record.downlink_share,
        panel_factor=record.panel_factor,
        readings=tuple(_reading_block(reading) for reading in record.readings),
        band_saturation_numbers=dict(record.band_saturation_numbers),
        iot_check=IotCheckBlock(
            minimal_packet_iot=tuple(
                _iot_row_block(row) for row in record.iot_check.minimal_packet_iot
            ),
            data_iot=tuple(_iot_row_block(row) for row in record.iot_check.data_iot),
        ),
        limits=record.limits,
    )


def build_iridium_artifact(
    *,
    fleet: FleetTrajectory,
    iridium: IridiumRecord,
    source_scenario_path: str,
    version_stamp: str,
) -> IridiumModelArtifact:
    """Assemble the promoted artifact from an Iridium run's two records.

    Pure assembly: no IO and no config. The cost totals, the final year and each year's
    launches, living fleet and annualized cost come from the shared fleet-and-cost record
    (``fleet``); everything else, the settings it publishes among it, from the Iridium
    record (``iridium``), so the artifact always describes exactly the run it was built from.

    Args:
        fleet: The run's shared fleet-and-cost record (``IridiumRun.fleet``).
        iridium: The run's Iridium record (``IridiumRun.iridium``).
        source_scenario_path: The provenance path string for the scenario YAML.
        version_stamp: The caller-supplied stamp (git-describe or a date string).

    Returns:
        The populated, frozen :class:`IridiumModelArtifact`.

    Raises:
        ValueError: If a value is not finite (the artifact's models refuse one), or the two
            records' years do not match one for one.
    """
    final_year = fleet.years[-1]
    return IridiumModelArtifact(
        provenance=IridiumProvenance(
            model_name=MODEL_NAME,
            schema_version=IRIDIUM_SCHEMA_VERSION,
            scenario_name=iridium.scenario_name,
            source_scenario_path=source_scenario_path,
            version_stamp=version_stamp,
        ),
        trajectory_summary=TrajectorySummaryBlock(
            total_cost_through_final_year_musd=fleet.total_cost_through_final_year_musd,
            final_year_annual_cost_musd=fleet.final_year_annual_cost_musd,
            final_year_replacement_cost_musd=fleet.final_year_replacement_cost_musd,
            living_fleet_final_year=final_year.living_fleet,
            cumulative_launches_final_year=sum(
                year.comms_launches_flown_this_year for year in fleet.years
            ),
            coverage_floor_reached_year=iridium.coverage_floor_reached_year,
            cost_per_satellite_year_musd=iridium.cost_per_satellite_year_musd,
        ),
        orbit_scenario=OrbitScenarioBlock(
            altitude_km=ORBIT_ALTITUDE_KM_SCENARIO,
            inclination_deg=ORBIT_INCLINATION_DEG_SCENARIO,
            source_status=ORBIT_SCENARIO_SOURCE_STATUS,
            basis=ORBIT_SCENARIO_BASIS,
        ),
        iridium_physics=IridiumPhysicsBlock(
            spectrum_mhz=iridium.spectrum_mhz,
            aperture_m2=iridium.aperture_m2,
            satellites_per_launch=iridium.satellites_per_launch,
            operations_cost_musd=iridium.operations_cost_musd,
            ecosystem_assumption=iridium.ecosystem_assumption,
        ),
        classes=tuple(_class_block(record) for record in iridium.classes),
        years=_year_blocks(fleet, iridium),
        fixed_books=_fixed_books_block(iridium.fixed_books),
        saturation=_saturation_block(iridium.saturation),
        assumptions=iridium.assumptions,
    )


def export_iridium_json(
    scenario_path: str | Path,
    output_path: str | Path,
    version_stamp: str | None = None,
) -> Path:
    """Run an Iridium scenario on its saturation curve and write the promoted JSON artifact.

    Loads the scenario and narrows it to its Iridium dials before anything else
    (:func:`~communications.iridium.iridium_dials_of`: a scenario without an
    ``iridium:`` block fails there, before any curve is read or any model runs);
    loads the saturation curve its ``iridium.saturation.curve_path`` names with
    :func:`~communications.saturation_curve.load_saturation_curve`; runs the
    Iridium entry, :func:`~communications.iridium.run_iridium_model`, which first
    checks that the curve was computed for the scenario's own inputs (a refusal
    names the curve file by its anchored path, as the loader's refusals do);
    assembles the artifact from the run's two records, and writes it through
    :func:`common.file_io.write_files_with_rollback` (staged in full, then one
    atomic rename, so a failed write leaves any existing file as it was; an
    output path that is a symbolic link or not a regular file is refused). A
    relative ``output_path`` or curve path is anchored to the REPO ROOT of the
    source checkout (the promoted ``communications/models/`` folder lives
    there, never under ``code/``); an absolute path is used as-is
    (:meth:`common.file_io.SourceCheckout.anchored`). The
    ``scenario_path`` resolves against the working directory as usual and is
    recorded in the provenance header repository-relative, or as its absolute
    path when it lies outside the repository
    (:meth:`common.file_io.SourceCheckout.repo_relative`).

    Args:
        scenario_path: The scenario YAML to run (must select the Iridium model).
        output_path: Where to write the promoted JSON (relative = repo-root
            anchored).
        version_stamp: Optional stamp for the provenance header (git-describe
            or any string); defaults to today's ISO date.

    Returns:
        The path the artifact was written to: the output path anchored at the repository
        root when it is relative, else as given, and not resolved.

    Raises:
        common.file_io.ModelFileError: If the module is not running from a
            source checkout, the scenario YAML or the saturation curve is
            missing, unreadable, or not parseable, or the artifact cannot be
            written.
        ValueError: If the scenario is invalid (a
            :class:`pydantic.ValidationError`) or does not select the Iridium
            model (:class:`~communications.iridium.NotAnIridiumConfigError`), its
            saturation curve is refused (a
            :class:`~communications.saturation_curve.SaturationCurveError`:
            another schema, altered, incomplete, or computed for other inputs,
            each naming the curve file; a fleet the run reads past a class's last
            row; or the final year's fleet past the fleet a class with no
            saturation number is not reached by, where the curve measures no
            elasticity of capacity,
            :class:`~communications.iridium.BindingLimitUnmeasuredError`), or it
            cannot be run.
        ArithmeticError: If a value the model cannot compute arises (an
            ``OverflowError``, say).
    """
    checkout = locate_source_checkout(__file__)
    scenario = Path(scenario_path)
    config = load_comms_config(scenario)
    dials = iridium_dials_of(config)
    curve_path = checkout.anchored(dials.saturation.curve_path)
    curve = load_saturation_curve(curve_path)
    try:
        run = run_iridium_model(config, curve)
    except SaturationCurveMismatchError as exc:
        raise SaturationCurveMismatchError(f"{curve_path}: {exc}") from exc
    stamp = version_stamp if version_stamp is not None else date.today().isoformat()
    artifact = build_iridium_artifact(
        fleet=run.fleet,
        iridium=run.iridium,
        source_scenario_path=checkout.repo_relative(scenario),
        version_stamp=stamp,
    )
    out = checkout.anchored(output_path)
    write_files_with_rollback([artifact_write(out, artifact)])
    logger.info("promoted Iridium model artifact written to %s", out)
    return out


def _build_parser() -> CliArgumentParser:
    """Build the module's command-line parser (usage errors exit with EXIT_USAGE)."""
    parser = CliArgumentParser(
        prog="python -m communications.json_output",
        description=(
            "Run the Iridium model (formerly Model B) from a scenario YAML, on the "
            "saturation curve its iridium.saturation.curve_path names, and write "
            "the promoted JSON artifact into the repo-root communications/models/ "
            "folder."
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
        :data:`~common.cli.EXIT_OK` on success; :data:`~common.cli.EXIT_ERROR`
        (after one ``ERROR:`` log line, no traceback) when the scenario cannot
        be read, is invalid, or does not select the Iridium model, its
        saturation curve cannot be read, was computed for other inputs, ends
        before a fleet the run reads or measures no elasticity of capacity at
        the final year's fleet for a class it gives no saturation number (that
        fleet past the one the curve names it not reached by), the model cannot
        run (a value it cannot compute among them: an ``ArithmeticError``, such
        as an overflow), the artifact would hold a number that is not finite
        (its models refuse one), or the artifact cannot be written. Usage
        errors exit through :class:`~common.cli.CliArgumentParser` with
        :data:`~common.cli.EXIT_USAGE`.
    """
    configure_cli_logging()
    args = _build_parser().parse_args(argv)
    scenario = Path(args.scenario)
    try:
        export_iridium_json(scenario, args.output, args.version_stamp)
    except (ModelFileError, ValueError) as exc:
        logger.error("could not promote %s: %s", scenario, describe_failure(exc, scenario))
        return EXIT_ERROR
    except ArithmeticError as exc:
        logger.error(
            "could not promote %s: a value the model cannot compute (%s)",
            scenario,
            describe_failure(exc, scenario),
        )
        return EXIT_ERROR
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
