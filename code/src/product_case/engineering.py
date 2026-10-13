"""B1, the engineering view: the one reader of the engineering artifact, and the network it gives.

The product case sells the network the engineering model builds, read only from its promoted
artifact (``communications/models/iridium/default.json``, schema ``iridium-v7``), as JSON: never
by importing the engineering code. :func:`engineering_view_from_bytes` takes the bytes the
command read once, hashes them (SHA-256, recorded so the artifact names the engineering run it
describes) and parses the same bytes through a narrow reader of the fields IoT foundation v1
lists for the product case, every other field ignored and the schema pinned
(:data:`~product_case.constants.ENGINEERING_SCHEMA_VERSION`). :func:`build_engineering_view` then
derives method step 1 from plain numbers, for each reported year t:

- the class split s: today's terminal mix (N_v 402,000 voice and data, N_b 16,100 broadband,
  COMM-617) turned into beam shares through each terminal class's people a beam
  u_c = beam_pool_mbps / (active_user_rate_mbps x concurrency_peak):
  s = (n_v / u_small) / (n_v / u_small + n_b / u_mounted), n_v = N_v / (N_v + N_b), n_b = 1 - n_v;
- the seats, unrounded: S_small(t) = s x P_small(t) and S_mounted(t) = (1 - s) x P_mounted(t),
  with P_c(t) the class's whole-fleet people (``years[].classes[].people_served``);
- the network's scale k(t) = (S_small(t) + S_mounted(t)) / 418,100, Iridium's terminal
  customers today;
- each terminal's busy-hour data a month from its engineering usage: the rate while active x the
  busy-hour share x 4 busy hours x 3,600 s x 30 days, in GB (2.7 and 27 on the committed artifact),
  so its busy-hour load and its seats are the engineering case's;
- IoT's three rooms, read as published: the payload bits a second R(t), the random-access attempts
  a second at the window's low end A(t) and the single-tone seconds a second T(t), with the phone
  class's useful beams L(t) that IoT rides.

It refuses, naming the field or the year, with :class:`EngineeringArtifactError`: bytes that are
not JSON; another schema (naming ``iridium-v7``); a field it reads missing or of the wrong type; a
null coverage floor year (no year of service in the horizon); a reported year absent from the
artifact, or before its coverage floor year; a reported year in which a terminal class has no
people (no seats, so the fill would divide by zero); a reported year whose IoT room is zero (a
downlink share of 1 leaves the uplink no time); a beam pool, a message or burst size or the
airtime that is not above 0 (each divides a quantity). The view is frozen and holds plain
numbers, so a test can build one from pinned values.
"""

from __future__ import annotations

import hashlib
import json
import logging
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Final  # typing-acceptable: Any types the parsed JSON before validation

from pydantic import BaseModel, ConfigDict, StrictFloat, StrictInt, StrictStr, ValidationError

from product_case.constants import (
    BITS_PER_BYTE,
    BITS_PER_MEGABIT,
    BUSY_HOURS_PER_DAY,
    BYTES_PER_GB,
    DAYS_PER_MONTH,
    ENGINEERING_SCHEMA_VERSION,
    PHONE_DEVICE_CLASS,
    SECONDS_PER_HOUR,
    TERMINAL_CUSTOMERS_TODAY,
    TERMINAL_DEVICE_CLASS,
    VOICE_DATA_CUSTOMERS_TODAY,
    ProductClass,
)

logger = logging.getLogger(__name__)


class EngineeringArtifactError(ValueError):
    """The engineering artifact cannot carry the product case.

    Raised by :func:`engineering_view_from_bytes` and :func:`build_engineering_view` for bytes
    that are not JSON, another schema, a field missing or of the wrong type, a null coverage
    floor year, a reported year absent or before the floor, a terminal class with no people in a
    reported year, a reported year whose IoT room is zero, or a pool, a size or the airtime that
    is not above 0. The message is one line naming the artifact and the field or the year.
    """


# ---------------------------------------------------------------------------
# The view: plain numbers, frozen
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TerminalPool:
    """A terminal class's beam pool and busy-hour load, as the engineering artifact publishes them.

    Attributes:
        beam_pool_mbps: The data a beam serves the class, Mbps (``classes[].beam_pool_mbps``).
        active_user_rate_mbps: The class's rate while active, Mbps (its engineering usage).
        concurrency_peak: The share of the class's people active in the busy hours.
    """

    beam_pool_mbps: float
    active_user_rate_mbps: float
    concurrency_peak: float

    @property
    def people_per_beam(self) -> float:
        """u_c = beam_pool_mbps / (active_user_rate_mbps x concurrency_peak), people a beam."""
        return self.beam_pool_mbps / (self.active_user_rate_mbps * self.concurrency_peak)

    @property
    def busy_hour_gb_per_month(self) -> float:
        """The busy-hour data a month: r x 10^6 x c x 4 h x 3,600 s x 30 days / 8 / 10^9, GB."""
        return (
            self.active_user_rate_mbps
            * BITS_PER_MEGABIT
            * self.concurrency_peak
            * BUSY_HOURS_PER_DAY
            * SECONDS_PER_HOUR
            * DAYS_PER_MONTH
            / BITS_PER_BYTE
            / BYTES_PER_GB
        )


@dataclass(frozen=True)
class EngineeringYearReading:
    """One reported year as the engineering artifact publishes it: the values B1 reads.

    Attributes:
        year: The fiscal year.
        living_fleet: The year's living fleet, satellites.
        annual_cost_musd: C(t), the living fleet's annualized build and launch cost, $M a year.
        people_small_terminal: P_small(t), the whole fleet sold to the small terminal alone.
        people_mounted_terminal: P_mounted(t), the whole fleet sold to the mounted terminal alone.
        phone_useful_beams: L(t), the phone class's useful beams, which IoT rides.
        iot_payload_bits_per_second: R(t), IoT's payload room, bits a second.
        iot_access_attempts_per_second: A(t), IoT's random-access room at the window's low end.
        iot_single_tone_seconds_per_second: T(t), IoT's single-tone room, tone-seconds a second.
    """

    year: int
    living_fleet: int
    annual_cost_musd: float
    people_small_terminal: float
    people_mounted_terminal: float
    phone_useful_beams: float
    iot_payload_bits_per_second: float
    iot_access_attempts_per_second: float
    iot_single_tone_seconds_per_second: float


@dataclass(frozen=True)
class EngineeringYear:
    """One reported year of the network the product case sells on (method step 1).

    Attributes:
        year: The fiscal year.
        living_fleet: The year's living fleet, satellites.
        annual_cost_musd: C(t), the fleet's annual cost, $M a year.
        people_small_terminal: P_small(t), whole-fleet people (a float, so a test can pin
            round 3's).
        people_mounted_terminal: P_mounted(t), whole-fleet people.
        seats_small_terminal: S_small(t) = s x P_small(t), unrounded.
        seats_mounted_terminal: S_mounted(t) = (1 - s) x P_mounted(t), unrounded.
        network_scale: k(t), the seats over Iridium's 418,100 terminal customers today.
        phone_useful_beams: L(t), the phone class's useful beams.
        iot_payload_bits_per_second: R(t), bits a second.
        iot_access_attempts_per_second: A(t), attempts a second.
        iot_single_tone_seconds_per_second: T(t), tone-seconds a second.
    """

    year: int
    living_fleet: int
    annual_cost_musd: float
    people_small_terminal: float
    people_mounted_terminal: float
    seats_small_terminal: float
    seats_mounted_terminal: float
    network_scale: float
    phone_useful_beams: float
    iot_payload_bits_per_second: float
    iot_access_attempts_per_second: float
    iot_single_tone_seconds_per_second: float


@dataclass(frozen=True)
class EngineeringView:
    """The network the product case sells on, every reported year (B1's output).

    Constructible from plain numbers, so a test can build one from pinned values.

    Attributes:
        path: The engineering artifact's path as the scenario names it.
        sha256: The SHA-256 of the bytes parsed, hex.
        schema_version: The artifact's schema, ``iridium-v7``.
        version_stamp: The artifact's version stamp.
        coverage_floor_reached_year: The first year the living fleet reaches the coverage floor.
        small_terminal_pool: The small terminal's beam pool and busy-hour load.
        mounted_terminal_pool: The mounted terminal's beam pool and busy-hour load.
        small_terminal_share: s, the small terminal's share of the busy-hour beams.
        busy_hour_gb_per_month_small: The small terminal's busy-hour data a month, GB.
        busy_hour_gb_per_month_mounted: The mounted terminal's busy-hour data a month, GB.
        message_bytes: The size of an IoT message, bytes.
        burst_bytes: The size of a data IoT burst, bytes.
        airtime_high_s: A message's single-tone airtime at its high end, seconds.
        years: The reported years, in order.
    """

    path: str
    sha256: str
    schema_version: str
    version_stamp: str
    coverage_floor_reached_year: int
    small_terminal_pool: TerminalPool
    mounted_terminal_pool: TerminalPool
    small_terminal_share: float
    busy_hour_gb_per_month_small: float
    busy_hour_gb_per_month_mounted: float
    message_bytes: int
    burst_bytes: int
    airtime_high_s: float
    years: tuple[EngineeringYear, ...]


# ---------------------------------------------------------------------------
# Method step 1, from plain numbers
# ---------------------------------------------------------------------------


def class_split(small: TerminalPool, mounted: TerminalPool) -> float:
    """The class split s, the small terminal's share of the terminals' busy-hour beams.

    Today's terminal mix (COMM-617) turned into beam shares through each class's people a beam:
    with n_v = N_v / (N_v + N_b) and n_b = 1 - n_v,
    s = (n_v / u_small) / (n_v / u_small + n_b / u_mounted), unitless (the engineering case's
    split, 0.757347400150716 on the committed artifact, equal to round 1's to the bit).

    Args:
        small: The small terminal's pool.
        mounted: The mounted terminal's pool.

    Returns:
        s, between 0 and 1; the mounted terminal's share is 1 - s.
    """
    personal = VOICE_DATA_CUSTOMERS_TODAY / TERMINAL_CUSTOMERS_TODAY
    need_small = personal / small.people_per_beam
    need_mounted = (1.0 - personal) / mounted.people_per_beam
    return need_small / (need_small + need_mounted)


def _refuse_unsellable(path: str, floor_year: int, reading: EngineeringYearReading) -> None:
    """Refuse a reported year the product case cannot sell in, naming the year and the field."""
    year = reading.year
    if year < floor_year:
        raise EngineeringArtifactError(
            f"{path}: FY{year} is before the coverage floor year FY{floor_year} "
            "(trajectory_summary.coverage_floor_reached_year): nothing is sold below the floor, "
            "so the year has no seats and the fill would divide by zero"
        )
    people = {
        TERMINAL_DEVICE_CLASS[ProductClass.SMALL_TERMINAL]: reading.people_small_terminal,
        TERMINAL_DEVICE_CLASS[ProductClass.MOUNTED_TERMINAL]: reading.people_mounted_terminal,
    }
    for device_class, count in people.items():
        if not count > 0:
            raise EngineeringArtifactError(
                f"{path}: FY{year}: {device_class} has no people (years[].classes[]"
                f".people_served is {count!r}), so it has no seats and the fill would divide "
                "by zero"
            )
    rooms = {
        "years[].iot.uplink_payload_bits_per_second": reading.iot_payload_bits_per_second,
        "years[].iot.access_attempts_per_second_low": reading.iot_access_attempts_per_second,
        "years[].iot.single_tone_seconds_per_second": reading.iot_single_tone_seconds_per_second,
        f"years[].classes[].useful_beams of {PHONE_DEVICE_CLASS}": reading.phone_useful_beams,
    }
    for field, room in rooms.items():
        if not room > 0:
            raise EngineeringArtifactError(
                f"{path}: FY{year}: IoT's room is zero ({field} is {room!r}): a downlink share "
                "of 1 leaves the uplink no time, so no IoT device fits"
            )


def _refuse_unusable_sizes(
    path: str,
    pools: dict[str, TerminalPool],
    message_bytes: int,
    burst_bytes: int,
    airtime_high_s: float,
) -> None:
    """Refuse a pool, a size or the airtime not above 0 (each divides a quantity), naming it."""
    values: dict[str, float] = {
        "iridium_physics.iot_message_bytes": message_bytes,
        "iridium_physics.iot_burst_bytes": burst_bytes,
        "iridium_physics.iot_message_airtime_high_s": airtime_high_s,
    }
    for device_class, pool in pools.items():
        values[f"classes[].beam_pool_mbps of {device_class}"] = pool.beam_pool_mbps
        values[f"classes[].active_user_rate_mbps of {device_class}"] = pool.active_user_rate_mbps
        values[f"classes[].concurrency_peak of {device_class}"] = pool.concurrency_peak
    for field, value in values.items():
        if not value > 0:
            raise EngineeringArtifactError(
                f"{path}: {field} is {value!r}; the product case needs it above 0"
            )


def build_engineering_view(
    *,
    path: str,
    sha256: str,
    schema_version: str,
    version_stamp: str,
    coverage_floor_reached_year: int,
    small_terminal_pool: TerminalPool,
    mounted_terminal_pool: TerminalPool,
    message_bytes: int,
    burst_bytes: int,
    airtime_high_s: float,
    readings: Sequence[EngineeringYearReading],
) -> EngineeringView:
    """Derive method step 1, the network each reported year, from plain numbers.

    s from the two pools (:func:`class_split`); per reported year t the seats
    S_small(t) = s x P_small(t) and S_mounted(t) = (1 - s) x P_mounted(t), unrounded, and the
    network's scale k(t) = (S_small(t) + S_mounted(t)) / 418,100; each terminal's busy-hour data
    a month from its pool (:attr:`TerminalPool.busy_hour_gb_per_month`, GB); L(t) and IoT's
    three rooms as read.

    Args:
        path: The engineering artifact's path as the scenario names it.
        sha256: The SHA-256 of the bytes the readings came from, hex.
        schema_version: The artifact's schema.
        version_stamp: The artifact's version stamp.
        coverage_floor_reached_year: The first year the living fleet reaches the coverage floor.
        small_terminal_pool: The small terminal's pool.
        mounted_terminal_pool: The mounted terminal's pool.
        message_bytes: The size of an IoT message, bytes.
        burst_bytes: The size of a data IoT burst, bytes.
        airtime_high_s: A message's single-tone airtime at its high end, seconds.
        readings: The reported years as read, in order.

    Returns:
        The frozen view.

    Raises:
        EngineeringArtifactError: If a pool, a size or the airtime is not above 0, a reported year
            is before the coverage floor year, a terminal class has no people in it, or its IoT
            room or the phone class's beams are zero.
    """
    _refuse_unusable_sizes(
        path,
        {
            TERMINAL_DEVICE_CLASS[ProductClass.SMALL_TERMINAL]: small_terminal_pool,
            TERMINAL_DEVICE_CLASS[ProductClass.MOUNTED_TERMINAL]: mounted_terminal_pool,
        },
        message_bytes,
        burst_bytes,
        airtime_high_s,
    )
    for reading in readings:
        _refuse_unsellable(path, coverage_floor_reached_year, reading)
    share = class_split(small_terminal_pool, mounted_terminal_pool)
    years = tuple(_engineering_year(share, reading) for reading in readings)
    view = EngineeringView(
        path=path,
        sha256=sha256,
        schema_version=schema_version,
        version_stamp=version_stamp,
        coverage_floor_reached_year=coverage_floor_reached_year,
        small_terminal_pool=small_terminal_pool,
        mounted_terminal_pool=mounted_terminal_pool,
        small_terminal_share=share,
        busy_hour_gb_per_month_small=small_terminal_pool.busy_hour_gb_per_month,
        busy_hour_gb_per_month_mounted=mounted_terminal_pool.busy_hour_gb_per_month,
        message_bytes=message_bytes,
        burst_bytes=burst_bytes,
        airtime_high_s=airtime_high_s,
        years=years,
    )
    logger.debug(
        "the engineering view of %s (%s): s %r, years %s",
        path,
        version_stamp,
        share,
        [year.year for year in years],
    )
    return view


def _engineering_year(share: float, reading: EngineeringYearReading) -> EngineeringYear:
    """One reported year's network: the seats and the network's scale beside the values read."""
    seats_small = share * reading.people_small_terminal
    seats_mounted = (1.0 - share) * reading.people_mounted_terminal
    return EngineeringYear(
        year=reading.year,
        living_fleet=reading.living_fleet,
        annual_cost_musd=reading.annual_cost_musd,
        people_small_terminal=reading.people_small_terminal,
        people_mounted_terminal=reading.people_mounted_terminal,
        seats_small_terminal=seats_small,
        seats_mounted_terminal=seats_mounted,
        network_scale=(seats_small + seats_mounted) / TERMINAL_CUSTOMERS_TODAY,
        phone_useful_beams=reading.phone_useful_beams,
        iot_payload_bits_per_second=reading.iot_payload_bits_per_second,
        iot_access_attempts_per_second=reading.iot_access_attempts_per_second,
        iot_single_tone_seconds_per_second=reading.iot_single_tone_seconds_per_second,
    )


# ---------------------------------------------------------------------------
# The narrow reader of iridium-v7 (IoT foundation v1's fields for part B, and nothing else)
# ---------------------------------------------------------------------------

_READER_CONFIG: Final[ConfigDict] = ConfigDict(extra="ignore", frozen=True, allow_inf_nan=False)
"""The reader's settings: every field it does not read ignored, a non-finite number refused."""


class _ProvenanceSlice(BaseModel):
    """``provenance``: the schema (pinned) and the stamp."""

    model_config = _READER_CONFIG
    schema_version: StrictStr
    version_stamp: StrictStr


class _SchemaProbe(BaseModel):
    """The artifact's schema alone, read before anything else so another schema is named."""

    model_config = _READER_CONFIG
    provenance: _ProvenanceSlice


class _TrajectorySlice(BaseModel):
    """``trajectory_summary``: the coverage floor year (null when the fleet never reaches it)."""

    model_config = _READER_CONFIG
    coverage_floor_reached_year: StrictInt | None


class _PhysicsSlice(BaseModel):
    """``iridium_physics``: the message's and the burst's size and the airtime's high end."""

    model_config = _READER_CONFIG
    iot_message_bytes: StrictInt
    iot_burst_bytes: StrictInt
    iot_message_airtime_high_s: StrictFloat


class _ClassSlice(BaseModel):
    """One ``classes[]`` entry: a device class's beam pool and busy-hour load."""

    model_config = _READER_CONFIG
    device_class: StrictStr
    beam_pool_mbps: StrictFloat
    active_user_rate_mbps: StrictFloat
    concurrency_peak: StrictFloat


class _YearClassSlice(BaseModel):
    """One ``years[].classes[]`` entry: a device class's people and useful beams that year."""

    model_config = _READER_CONFIG
    device_class: StrictStr
    people_served: StrictInt
    useful_beams: StrictFloat


class _YearIotSlice(BaseModel):
    """``years[].iot``: IoT's three rooms that year."""

    model_config = _READER_CONFIG
    uplink_payload_bits_per_second: StrictFloat
    access_attempts_per_second_low: StrictFloat
    single_tone_seconds_per_second: StrictFloat


class _YearSlice(BaseModel):
    """One ``years[]`` entry: the fleet, its cost, each class's people and beams, IoT's room."""

    model_config = _READER_CONFIG
    year: StrictInt
    living_fleet: StrictInt
    annual_cost_musd: StrictFloat
    classes: tuple[_YearClassSlice, ...]
    iot: _YearIotSlice


class _EngineeringSlice(BaseModel):
    """The engineering artifact's fields the product case reads, and nothing else."""

    model_config = _READER_CONFIG
    provenance: _ProvenanceSlice
    trajectory_summary: _TrajectorySlice
    iridium_physics: _PhysicsSlice
    classes: tuple[_ClassSlice, ...]
    years: tuple[_YearSlice, ...]


def _first_error(error: ValidationError) -> str:
    """The first validation error as ``field: reason``, its location dotted."""
    first = error.errors()[0]
    location = ".".join(str(part) for part in first["loc"]) or "the root"
    return f"{location}: {first['msg']}"


def _parse(path: str, data: bytes) -> _EngineeringSlice:
    """Parse the bytes as JSON, pin the schema, then read the fields B1 needs."""
    try:
        parsed: Any = json.loads(data)
    except ValueError as error:  # json.JSONDecodeError and UnicodeDecodeError
        raise EngineeringArtifactError(f"{path}: not JSON ({error})") from error
    try:
        found = _SchemaProbe.model_validate(parsed).provenance.schema_version
    except ValidationError as error:
        raise EngineeringArtifactError(
            f"{path}: not an engineering artifact the product case reads (it needs schema "
            f"{ENGINEERING_SCHEMA_VERSION}): {_first_error(error)}"
        ) from error
    if found != ENGINEERING_SCHEMA_VERSION:
        raise EngineeringArtifactError(
            f"{path}: provenance.schema_version is {found!r}; the product case reads only "
            f"{ENGINEERING_SCHEMA_VERSION!r} (a schema bump lands with a product-case change "
            "that re-pins it)"
        )
    try:
        return _EngineeringSlice.model_validate(parsed)
    except ValidationError as error:
        raise EngineeringArtifactError(
            f"{path}: a field the product case reads is missing or invalid: {_first_error(error)}"
        ) from error


def _terminal_pool(path: str, artifact: _EngineeringSlice, device_class: str) -> TerminalPool:
    """A terminal class's pool from ``classes[]``, refused when the class is absent."""
    for entry in artifact.classes:
        if entry.device_class == device_class:
            return TerminalPool(
                beam_pool_mbps=entry.beam_pool_mbps,
                active_user_rate_mbps=entry.active_user_rate_mbps,
                concurrency_peak=entry.concurrency_peak,
            )
    raise EngineeringArtifactError(f"{path}: classes[] has no {device_class} entry")


def _reading(path: str, entry: _YearSlice) -> EngineeringYearReading:
    """One year's reading, each class it needs found by its ``device_class``."""
    by_class = {item.device_class: item for item in entry.classes}
    needed = (
        TERMINAL_DEVICE_CLASS[ProductClass.SMALL_TERMINAL],
        TERMINAL_DEVICE_CLASS[ProductClass.MOUNTED_TERMINAL],
        PHONE_DEVICE_CLASS,
    )
    for device_class in needed:
        if device_class not in by_class:
            raise EngineeringArtifactError(
                f"{path}: FY{entry.year}: years[].classes[] has no {device_class} entry"
            )
    return EngineeringYearReading(
        year=entry.year,
        living_fleet=entry.living_fleet,
        annual_cost_musd=entry.annual_cost_musd,
        people_small_terminal=float(by_class[needed[0]].people_served),
        people_mounted_terminal=float(by_class[needed[1]].people_served),
        phone_useful_beams=by_class[PHONE_DEVICE_CLASS].useful_beams,
        iot_payload_bits_per_second=entry.iot.uplink_payload_bits_per_second,
        iot_access_attempts_per_second=entry.iot.access_attempts_per_second_low,
        iot_single_tone_seconds_per_second=entry.iot.single_tone_seconds_per_second,
    )


def engineering_view_from_bytes(
    data: bytes, *, path: str, reported_years: tuple[int, ...]
) -> EngineeringView:
    """Read the engineering artifact's bytes into the view of the reported years.

    The bytes are hashed (SHA-256) and the same bytes parsed: as JSON, the schema pinned to
    ``iridium-v7``, then the fields the product case reads; then
    :func:`build_engineering_view` derives the network each reported year.

    Args:
        data: The engineering artifact's bytes, read once by the caller.
        path: The artifact's path as the scenario names it (recorded and named in errors).
        reported_years: The scenario's reported years, in order.

    Returns:
        The frozen view.

    Raises:
        EngineeringArtifactError: If the bytes are not JSON or not ``iridium-v7``, a field read is
            missing or invalid, the coverage floor year is null, a reported year is absent from
            the artifact or before its floor year, a terminal class has no people in a reported
            year, a reported year's IoT room or the phone class's beams are zero, or a pool, a size
            or the airtime is not above 0.
    """
    sha256 = hashlib.sha256(data).hexdigest()
    artifact = _parse(path, data)
    floor_year = artifact.trajectory_summary.coverage_floor_reached_year
    if floor_year is None:
        raise EngineeringArtifactError(
            f"{path}: trajectory_summary.coverage_floor_reached_year is null: the fleet never "
            "reaches the coverage floor in the horizon, so no year has seats to sell"
        )
    by_year = {entry.year: entry for entry in artifact.years}
    readings: list[EngineeringYearReading] = []
    for year in reported_years:
        if year not in by_year:
            span = f"FY{min(by_year)} to FY{max(by_year)}" if by_year else "none: years[] is empty"
            raise EngineeringArtifactError(
                f"{path}: FY{year} is a reported year but not a year of the engineering "
                f"artifact (its years run {span})"
            )
        readings.append(_reading(path, by_year[year]))
    return build_engineering_view(
        path=path,
        sha256=sha256,
        schema_version=artifact.provenance.schema_version,
        version_stamp=artifact.provenance.version_stamp,
        coverage_floor_reached_year=floor_year,
        small_terminal_pool=_terminal_pool(
            path, artifact, TERMINAL_DEVICE_CLASS[ProductClass.SMALL_TERMINAL]
        ),
        mounted_terminal_pool=_terminal_pool(
            path, artifact, TERMINAL_DEVICE_CLASS[ProductClass.MOUNTED_TERMINAL]
        ),
        message_bytes=artifact.iridium_physics.iot_message_bytes,
        burst_bytes=artifact.iridium_physics.iot_burst_bytes,
        airtime_high_s=artifact.iridium_physics.iot_message_airtime_high_s,
        readings=readings,
    )


__all__ = [
    "EngineeringArtifactError",
    "EngineeringView",
    "EngineeringYear",
    "EngineeringYearReading",
    "TerminalPool",
    "build_engineering_view",
    "class_split",
    "engineering_view_from_bytes",
]
