"""The saturation curve's contract (foundation v2): its inputs, its result and its hash.

The saturation module (:mod:`communications.saturation`, the one module that imports
numpy, ADR 010) computes, for each device class, how many co-channel beams a Walker shell
keeps lit over the places people live as the fleet grows: the curve whose knee is each
class's spectrum bound (ADR 005). It is computed from the shipped population grid (ADR
009), with the band in full-time use (d = 1, ADR 008), at the reference panel. This module
holds the curve's contract and nothing that needs numpy, so the engine and the Iridium
family can read a curve without importing numpy:

* the inputs, :class:`SaturationInputs` and its parts, every field defaulting to its named
  constant in :mod:`communications.constants`, so ``SaturationInputs()`` is the default;
* the result, :class:`SaturationCurve` and its parts, schema
  :data:`SATURATION_CURVE_SCHEMA_VERSION`. It is also ``compute_saturation``'s return type,
  so the promoted curve has one schema and no mirror;
* :func:`saturation_inputs_for`, the inputs a config's Iridium dials imply (only the held
  spectrum), and :func:`curve_input_hash`, the SHA-256 of the inputs' canonical JSON;
* :func:`walker_shape`, the shell's pinned planes and satellites per plane for a requested
  fleet, which the module builds every shell with and the contract checks every row by;
* :func:`exceeds_bound` at :data:`BOUNDS_RELATIVE_TOLERANCE`, the one test of the curve's
  bounds, which the computation and the completeness check share;
* :func:`check_curve_complete`, what a promoted curve must carry (every row's useful beams,
  capacity and ocean factor and every maximum use above 0 among it, and necessary conditions
  on the markers its rows can give), and :func:`load_saturation_curve`, which reads a promoted
  curve and refuses one with a repeated key, a number out of range, another schema, a value
  pydantic's strict mode refuses (an integer field given a string, a float or a boolean; a
  float field given a string or a boolean, while a JSON integer there reads as the same
  float), altered parameters or input hash, or one that fails its completeness check, each
  with a :class:`SaturationCurveError` naming the file (a file it cannot read, or whose text
  Python's JSON parser cannot read as JSON, is the file boundary's ``ModelFileError``);
* :func:`check_curve_matches`, the identity check: a run reads only a curve computed for its
  own inputs, and a curve computed for others is refused with a
  :class:`SaturationCurveMismatchError` naming the first field that differs;
* the readings the engine takes from a class's curve at any fleet: :func:`useful_beams_at`
  and :func:`capacity_gbps_at` on the curve's own basis (d = 1, the reference panel),
  :func:`people_at` at a downlink share and a panel factor (the scenario's panel area over the
  curve's reference panel area), and :func:`read_fleet`, all of a fleet's readings at once (a
  :class:`FleetReading`), each fleet placed on the rows once. They follow the edge rules: at a
  row its own values; between rows log-log; below the first row linear through the origin (so
  U is flat there); at a fleet of 0 no beams and no U; past the class's last row a
  :class:`CurveBeyondLastRowError`, never an extrapolation or a clamp.

Every model is a frozen pydantic model with ``extra="forbid"`` that refuses a NaN or an
infinity, so a curve's JSON is standard JSON. The validators that belong to the contract:
the inputs carry exactly one class per :class:`~communications.constants.DeviceClass` and
one band point per :class:`BandName`, each in its enum's order; the sweep's fleets strictly
increase, as strict integers, and the mounted terminal's extension starts above the last of
them; a curve carries each class and each band point at most once, in its enum's order;
every tuple of rows strictly increases in fleet; each row's fleet is the realized P x S of
its requested fleet; and a directional row's two stacking statistics exist exactly when it
keeps stacked beams. A curve may lack classes, band points or trims while
it is being built (the phone class first, the directional classes, then the bands and the
trim); the promotion's completeness check is what a promoted curve must pass.

This module imports :mod:`communications.config`; ``config.py`` does not import it.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
from bisect import bisect_left
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from itertools import pairwise
from pathlib import Path
from types import MappingProxyType
from typing import Annotated, Final, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeInt,
    PositiveInt,
    ValidationError,
    model_validator,
)

from common.cadence import round_half_up
from common.file_io import TEXT_ENCODING, ModelFileError
from communications.config import IridiumDials
from communications.constants import (
    APERTURE_REFERENCE_M2,
    BAND_DENSITY_THRESHOLD_10_PER_KM2,
    BAND_DENSITY_THRESHOLD_100_PER_KM2,
    CARRIER_FREQUENCY_HZ,
    CLASS_SE_CENTRAL,
    CLASS_USAGE,
    DEMAND_DENSITY_THRESHOLD_PER_KM2,
    DEMAND_TAKE_UP,
    ELEVATION_MASK_DEG,
    GBPS_TO_MBPS,
    GRID_AGGREGATION_0P5_DEG,
    GRID_AGGREGATION_SHIPPED,
    IRIDIUM_NEXT_BEAMS_PER_SATELLITE,
    MOUNTED_TERMINAL_CLASS_DIRECTIVITY_DBI,
    MOUNTED_TERMINAL_CLASS_SECTOR_WEDGES_PER_RING,
    ORBIT_ALTITUDE_KM_SCENARIO,
    ORBIT_INCLINATION_DEG_SCENARIO,
    PHONE_CLASS_DIRECTIVITY_DBI,
    PHONE_CLASS_SECTOR_WEDGES_PER_RING,
    POPULATION_GRID_PATH,
    POPULATION_GRID_SHA256,
    REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE,
    SATURATION_FLEETS,
    SATURATION_FOOTPRINT_BANDS,
    SATURATION_MOUNTED_TERMINAL_EXTENSION,
    SATURATION_PASSES,
    SATURATION_SE_ANCHOR_BPS_PER_HZ,
    SATURATION_SEED,
    SATURATION_SNAPSHOTS_BANDS,
    SATURATION_SNAPSHOTS_DIRECTIONAL,
    SATURATION_SNAPSHOTS_PHONE_CENTRAL,
    SATURATION_SNAPSHOTS_TRIM,
    SATURATION_STALL_FLOOR,
    SMALL_TERMINAL_CLASS_DIRECTIVITY_DBI,
    SMALL_TERMINAL_CLASS_SECTOR_WEDGES_PER_RING,
    SPACING_AREA_FACTOR_TOUCHING,
    SPACING_AREA_FACTOR_WIDE,
    SPECTRUM_MHZ_DEFAULT,
    TAPER_BEAMWIDTH_FACTOR,
    TERMINAL_PATTERN_FLOOR_DB,
    TRIM_FLOORS_DBI,
    TRIM_SCAN_EXPONENT,
    TRIM_SEED,
    TRIM_VICTIMS,
    UNIFORM_BEAMWIDTH_FACTOR,
    DeviceClass,
)

logger = logging.getLogger(__name__)

SATURATION_CURVE_SCHEMA_VERSION: Final[str] = "saturation-v1"
"""The schema version of :class:`SaturationCurve` and of the promoted curve's JSON."""

_SHA256_HEX_PATTERN: Final[str] = "^[0-9a-f]{64}$"
"""A SHA-256 digest as lowercase hex: 64 characters, the form ``hashlib`` and ``shasum`` print."""

_CANONICAL_JSON_SEPARATORS: Final[tuple[str, str]] = (",", ":")
"""The canonical JSON's item and key separators, with no spaces (the input hash's form)."""

BOUNDS_RELATIVE_TOLERANCE: Final[float] = 1e-9
"""The relative tolerance of the curve's bounds (the saturation strategy's 1e-9 for every
invariant check): useful beams at most min(ceiling, supply) and the ceiling at most maximum use
hold exactly in arithmetic, and only rounding may carry them past. The computation checks every
snapshot by it and the completeness check every row's ceiling against maximum use, both through
:func:`exceeds_bound`, so a curve the computation passed passes the completeness check too."""

_PYDANTIC_VALUE_ERROR: Final[str] = "value_error"
"""Pydantic's error type for a ``ValueError`` raised inside a validator, whose message pydantic
leads with ``Value error,`` (the loader's refusals give the validator's own message, as
``common.cli.describe_failure`` does)."""

_RIGHT_ANGLE_DEG: Final[float] = 90.0
"""A right angle, degrees: the most an inclination or an elevation mask can be here (the
closed-form maximum use reads a prograde or polar shell's highest latitude as its
inclination)."""

_CONTRACT_MODEL_CONFIG: Final[ConfigDict] = ConfigDict(
    extra="forbid", frozen=True, allow_inf_nan=False
)
"""Every contract model's configuration: frozen, unknown keys refused, and only finite
floats, so the promoted curve is standard JSON."""


class BandName(StrEnum):
    """The band points beside the phone class's central curve, in the order a curve lists them.

    Each point changes one input from the central values: the effective ground area per
    beam (the taper, then the taper with wider co-channel spacing), the demand definition
    (10 and 100 people per km^2, and the 0.5 degree grid; ADR 009), and the beams per
    satellite (48).
    """

    TAPER = "taper"
    TAPER_AND_SPACING = "taper_and_spacing"
    DENSITY_10_PER_KM2 = "density_10_per_km2"
    DENSITY_100_PER_KM2 = "density_100_per_km2"
    GRID_0P5_DEG = "grid_0p5_deg"
    BEAMS_48 = "beams_48"


def _check_enum_order[E: StrEnum](
    found: Sequence[E], order: type[E], what: str, *, every_member: bool
) -> None:
    """Refuse members out of their enum's order or repeated (and, if asked, any missing).

    Args:
        found: The members as a tuple of entries lists them.
        order: The enum whose member order the entries must follow.
        what: What the entries are, for the error message.
        every_member: Whether every member of the enum must appear.

    Raises:
        ValueError: If a member repeats or appears out of order, or, with
            ``every_member``, if one is missing.
    """
    members = list(order)
    positions = [members.index(member) for member in found]
    in_order = all(later > earlier for earlier, later in pairwise(positions))
    complete = len(found) == len(members)
    if not in_order or (every_member and not complete):
        need = "exactly one entry per member" if every_member else "each member at most once"
        raise ValueError(
            f"{what} must hold {need}, in the order {[member.value for member in members]}; "
            f"got {[member.value for member in found]}"
        )


def _check_strictly_increasing(values: Sequence[int], what: str) -> None:
    """Refuse a sequence of fleets that does not strictly increase.

    Args:
        values: The fleets, in the order they are listed.
        what: What the fleets are, for the error message.

    Raises:
        ValueError: If any value is not above the one before it.
    """
    if any(later <= earlier for earlier, later in pairwise(values)):
        raise ValueError(f"{what} must strictly increase; got {list(values)}")


_RequestedFleet = Annotated[int, Field(strict=True, gt=0)]
"""A requested fleet: a positive integer, strictly (a boolean or a whole float is refused)."""


def exceeds_bound(value: float, bound: float) -> bool:
    """Return whether a value lies above its bound by more than the bounds' tolerance.

    The one test of the curve's bounds, for the computation and the completeness check alike:
    above the bound, and not within :data:`BOUNDS_RELATIVE_TOLERANCE` of it, relative.

    Args:
        value: The bounded value (useful beams, or a ceiling).
        bound: Its bound (min(ceiling, supply), or maximum use).

    Returns:
        Whether the value breaks the bound.
    """
    return value > bound and not math.isclose(value, bound, rel_tol=BOUNDS_RELATIVE_TOLERANCE)


def walker_shape(requested_fleet: int) -> tuple[int, int]:
    """Return the Walker shell's planes and satellites per plane for a requested fleet.

    P = round(sqrt(N)) planes of S = round(N / P) satellites, with Python's ``round`` (an exact
    half goes to the even neighbour): the curve's pinned convention. The realized fleet P x S
    keys a row, but the request builds its shell, and a realized count requested again can
    build another shell (1,000 gives 32 x 31 = 992, while 992 gives 31 x 32). So a reader
    rebuilds a row from its ``requested_fleet``, never from its ``fleet``.

    Args:
        requested_fleet: The requested fleet N.

    Returns:
        The planes P and the satellites per plane S.
    """
    planes = round(math.sqrt(requested_fleet))
    return planes, round(requested_fleet / planes)


# ===========================================================================
# 1. The curve's inputs
# ===========================================================================


class ClassInputs(BaseModel):
    """One device class's inputs to the curve.

    Attributes:
        device_class: The class.
        spectral_efficiency_bps_per_hz: Its central spectral efficiency, bps/Hz.
        active_rate_mbps: Its data rate while a user is active, Mbps.
        concurrency_peak: Its busy-hour share of users active at once; with the rate it is
            the class's busy-hour load per person.
        directivity_dbi: Its antenna directivity, dBi.
        sector_wedges_per_ring: Its sky sectors' azimuth wedges per ring, from the zenith
            down; empty for the phone class, which takes one co-channel layer.
    """

    model_config = _CONTRACT_MODEL_CONFIG

    device_class: DeviceClass
    spectral_efficiency_bps_per_hz: float = Field(gt=0)
    active_rate_mbps: float = Field(gt=0)
    concurrency_peak: float = Field(gt=0, le=1.0)
    directivity_dbi: float
    sector_wedges_per_ring: tuple[PositiveInt, ...]


class ShellInputs(BaseModel):
    """The shell and the beam the curve is computed for.

    Attributes:
        altitude_km: The circular shell's altitude, km.
        inclination_deg: Its inclination, degrees.
        elevation_mask_deg: The lowest elevation at which a device uses a satellite,
            degrees, above 0 (a beam's footprint grows without bound toward the horizon).
        carrier_hz: The carrier, Hz.
        beamwidth_factor: The beam's half-power width, in wavelengths over the aperture's
            side (0.886 for uniform illumination, the central beam).
        reuse_calibration_gbps_per_mhz_per_se: The per-satellite capacity calibration at
            the reference panel; the beams per satellite derive from it and the panel.
        reference_aperture_m2: The panel the curve is computed at, a square of side
            sqrt(area); the engine scales the curve by the scenario's panel over it.
    """

    model_config = _CONTRACT_MODEL_CONFIG

    altitude_km: float = Field(default=ORBIT_ALTITUDE_KM_SCENARIO, gt=0)
    inclination_deg: float = Field(
        default=ORBIT_INCLINATION_DEG_SCENARIO, gt=0, le=_RIGHT_ANGLE_DEG
    )
    elevation_mask_deg: float = Field(default=ELEVATION_MASK_DEG, gt=0, lt=_RIGHT_ANGLE_DEG)
    carrier_hz: float = Field(default=CARRIER_FREQUENCY_HZ, gt=0)
    beamwidth_factor: float = Field(default=UNIFORM_BEAMWIDTH_FACTOR, gt=0)
    reuse_calibration_gbps_per_mhz_per_se: float = Field(
        default=REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE, gt=0
    )
    reference_aperture_m2: float = Field(default=APERTURE_REFERENCE_M2, gt=0)


class DemandInputs(BaseModel):
    """The demand map: the shipped grid and which of its cells are demand.

    Attributes:
        grid_path: The population grid, repository-relative.
        grid_sha256: The grid's SHA-256; a grid with another digest is refused.
        density_threshold_per_km2: A cell is demand at this many people per km^2 or more.
        take_up: The share of a demand cell's residents counted as potential users (1.0,
            every resident: the maximal-demand bound).
    """

    model_config = _CONTRACT_MODEL_CONFIG

    grid_path: str = Field(default=POPULATION_GRID_PATH, min_length=1)
    grid_sha256: str = Field(default=POPULATION_GRID_SHA256, pattern=_SHA256_HEX_PATTERN)
    density_threshold_per_km2: float = Field(default=DEMAND_DENSITY_THRESHOLD_PER_KM2, gt=0)
    take_up: float = Field(default=DEMAND_TAKE_UP, gt=0, le=1.0)


class SweepInputs(BaseModel):
    """The fleets and the numerical method the curve is computed with.

    Attributes:
        fleets: The requested fleets, strict integers, strictly increasing (at least two,
            since a marker reads the elasticity between rows); each row is keyed by its
            realized fleet and carries its request.
        mounted_terminal_extension: The mounted terminal's extra requested fleets, strict
            integers, strictly increasing and above the last of ``fleets``.
        snapshots_phone_central: Snapshot times averaged at each fleet of the phone
            class's central curve.
        snapshots_directional: The same for the two directional classes.
        snapshots_bands: The same for each band point.
        snapshots_trim: The snapshots the interference trim prices at each row.
        seed: The seed of the snapshot draw, drawn once per run.
        footprint_bands: The geometric footprint bands of the smallest-footprint-first fill.
        passes: The proportional passes inside each band.
        stall_floor: The least share of min(ceiling, supply) the phone class's useful beams
            reach at the large fleets.
    """

    model_config = _CONTRACT_MODEL_CONFIG

    fleets: tuple[_RequestedFleet, ...] = Field(default=SATURATION_FLEETS, min_length=2)
    mounted_terminal_extension: tuple[_RequestedFleet, ...] = SATURATION_MOUNTED_TERMINAL_EXTENSION
    snapshots_phone_central: PositiveInt = SATURATION_SNAPSHOTS_PHONE_CENTRAL
    snapshots_directional: PositiveInt = SATURATION_SNAPSHOTS_DIRECTIONAL
    snapshots_bands: PositiveInt = SATURATION_SNAPSHOTS_BANDS
    snapshots_trim: PositiveInt = SATURATION_SNAPSHOTS_TRIM
    seed: NonNegativeInt = SATURATION_SEED
    footprint_bands: PositiveInt = SATURATION_FOOTPRINT_BANDS
    passes: PositiveInt = SATURATION_PASSES
    stall_floor: float = Field(default=SATURATION_STALL_FLOOR, gt=0, le=1.0)

    @model_validator(mode="after")
    def _fleets_increase(self) -> Self:
        """Refuse fleets that do not strictly increase, or an extension that starts low."""
        _check_strictly_increasing(self.fleets, "sweep.fleets")
        _check_strictly_increasing(
            self.mounted_terminal_extension, "sweep.mounted_terminal_extension"
        )
        if (
            self.mounted_terminal_extension
            and self.mounted_terminal_extension[0] <= self.fleets[-1]
        ):
            raise ValueError(
                "sweep.mounted_terminal_extension must start above the last of sweep.fleets "
                f"({self.fleets[-1]}); got {list(self.mounted_terminal_extension)}"
            )
        return self


class TrimInputs(BaseModel):
    """The interference trim's settings (the phone class's central curve only).

    Attributes:
        victims: The served cells sampled at each row.
        seed: The seed of each row's fresh victim draw.
        floors_dbi: The far-sidelobe floors the trim is reported at, dBi.
        scan_exponent: The exponent of the scan roll-off, cos^exponent of the scan angle.
    """

    model_config = _CONTRACT_MODEL_CONFIG

    victims: PositiveInt = TRIM_VICTIMS
    seed: NonNegativeInt = TRIM_SEED
    floors_dbi: tuple[float, ...] = Field(default=TRIM_FLOORS_DBI, min_length=1)
    scan_exponent: float = Field(default=TRIM_SCAN_EXPONENT, ge=0)


class BandPoint(BaseModel):
    """One band point: the central values but its one changed input.

    Attributes:
        name: Which point.
        beamwidth_factor: The beam's half-power width, wavelengths over the aperture's side.
        spacing_area_factor: The ground area a co-channel beam occupies over its 3 dB
            footprint (1.0 when co-channel footprints touch).
        density_threshold_per_km2: The demand threshold, people per km^2.
        grid_aggregation: Shipped cells summed per side (1, or 2 for the 0.5 degree grid).
        beams_per_satellite: The beams per satellite; None derives them from the
            calibration and the panel, as the central curve does.
    """

    model_config = _CONTRACT_MODEL_CONFIG

    name: BandName
    beamwidth_factor: float = Field(gt=0)
    spacing_area_factor: float = Field(gt=0)
    density_threshold_per_km2: float = Field(gt=0)
    grid_aggregation: PositiveInt
    beams_per_satellite: PositiveInt | None


_CLASS_DIRECTIVITY_DBI: Final[Mapping[DeviceClass, float]] = MappingProxyType(
    {
        DeviceClass.SMALL_TERMINAL_CLASS: SMALL_TERMINAL_CLASS_DIRECTIVITY_DBI,
        DeviceClass.MOUNTED_TERMINAL_CLASS: MOUNTED_TERMINAL_CLASS_DIRECTIVITY_DBI,
        DeviceClass.PHONE_CLASS: PHONE_CLASS_DIRECTIVITY_DBI,
    }
)
"""Each class's directivity, read from its named constant."""

_CLASS_SECTOR_WEDGES_PER_RING: Final[Mapping[DeviceClass, tuple[int, ...]]] = MappingProxyType(
    {
        DeviceClass.SMALL_TERMINAL_CLASS: SMALL_TERMINAL_CLASS_SECTOR_WEDGES_PER_RING,
        DeviceClass.MOUNTED_TERMINAL_CLASS: MOUNTED_TERMINAL_CLASS_SECTOR_WEDGES_PER_RING,
        DeviceClass.PHONE_CLASS: PHONE_CLASS_SECTOR_WEDGES_PER_RING,
    }
)
"""Each class's sky-sector layout, read from its named constant."""


def _default_class_inputs() -> tuple[ClassInputs, ...]:
    """Return each class's inputs from its named constants, in :class:`DeviceClass` order."""
    return tuple(
        ClassInputs(
            device_class=device_class,
            spectral_efficiency_bps_per_hz=CLASS_SE_CENTRAL[device_class],
            active_rate_mbps=CLASS_USAGE[device_class].active_rate_mbps,
            concurrency_peak=CLASS_USAGE[device_class].concurrency_peak,
            directivity_dbi=_CLASS_DIRECTIVITY_DBI[device_class],
            sector_wedges_per_ring=_CLASS_SECTOR_WEDGES_PER_RING[device_class],
        )
        for device_class in DeviceClass
    )


def _band_point(
    name: BandName,
    *,
    beamwidth_factor: float = UNIFORM_BEAMWIDTH_FACTOR,
    spacing_area_factor: float = SPACING_AREA_FACTOR_TOUCHING,
    density_threshold_per_km2: float = DEMAND_DENSITY_THRESHOLD_PER_KM2,
    grid_aggregation: int = GRID_AGGREGATION_SHIPPED,
    beams_per_satellite: int | None = None,
) -> BandPoint:
    """Return a band point: the central values, but for the inputs the caller changes."""
    return BandPoint(
        name=name,
        beamwidth_factor=beamwidth_factor,
        spacing_area_factor=spacing_area_factor,
        density_threshold_per_km2=density_threshold_per_km2,
        grid_aggregation=grid_aggregation,
        beams_per_satellite=beams_per_satellite,
    )


def _default_band_points() -> tuple[BandPoint, ...]:
    """Return the band points, one per :class:`BandName` in its order."""
    return (
        _band_point(BandName.TAPER, beamwidth_factor=TAPER_BEAMWIDTH_FACTOR),
        _band_point(
            BandName.TAPER_AND_SPACING,
            beamwidth_factor=TAPER_BEAMWIDTH_FACTOR,
            spacing_area_factor=SPACING_AREA_FACTOR_WIDE,
        ),
        _band_point(
            BandName.DENSITY_10_PER_KM2,
            density_threshold_per_km2=BAND_DENSITY_THRESHOLD_10_PER_KM2,
        ),
        _band_point(
            BandName.DENSITY_100_PER_KM2,
            density_threshold_per_km2=BAND_DENSITY_THRESHOLD_100_PER_KM2,
        ),
        _band_point(BandName.GRID_0P5_DEG, grid_aggregation=GRID_AGGREGATION_0P5_DEG),
        _band_point(BandName.BEAMS_48, beams_per_satellite=IRIDIUM_NEXT_BEAMS_PER_SATELLITE),
    )


class SaturationInputs(BaseModel):
    """Everything the curve depends on; every field defaults to its named constant.

    Not d, not the scenario's panel and no economics: the curve is computed with the band in
    full-time use at the reference panel, and the engine applies both factors (ADR 008).

    Attributes:
        spectrum_mhz: The held L-band width, MHz.
        se_anchor_bps_per_hz: The anchor of the link mapping, SE = anchor x log2(1 + SINR).
        sidelobe_floor_db: The directional terminals' pattern floor, dB below the peak.
        classes: Each class's inputs, exactly one per class, in :class:`DeviceClass` order.
        shell: The shell and the beam.
        demand: The demand map.
        sweep: The fleets and the numerical method.
        trim: The interference trim's settings.
        bands: The band points, exactly one per :class:`BandName`, in its order.
    """

    model_config = _CONTRACT_MODEL_CONFIG

    spectrum_mhz: float = Field(default=SPECTRUM_MHZ_DEFAULT, gt=0)
    se_anchor_bps_per_hz: float = Field(default=SATURATION_SE_ANCHOR_BPS_PER_HZ, gt=0)
    sidelobe_floor_db: float = Field(default=TERMINAL_PATTERN_FLOOR_DB, le=0)
    classes: tuple[ClassInputs, ...] = Field(default_factory=_default_class_inputs)
    shell: ShellInputs = Field(default_factory=ShellInputs)
    demand: DemandInputs = Field(default_factory=DemandInputs)
    sweep: SweepInputs = Field(default_factory=SweepInputs)
    trim: TrimInputs = Field(default_factory=TrimInputs)
    bands: tuple[BandPoint, ...] = Field(default_factory=_default_band_points)

    @model_validator(mode="after")
    def _one_entry_per_class_and_band(self) -> Self:
        """Refuse classes or band points that are not exactly one per member, in order."""
        _check_enum_order(
            [entry.device_class for entry in self.classes],
            DeviceClass,
            "classes",
            every_member=True,
        )
        _check_enum_order(
            [entry.name for entry in self.bands], BandName, "bands", every_member=True
        )
        return self


# ===========================================================================
# 2. The curve
# ===========================================================================


class DirectionalDiagnostics(BaseModel):
    """A directional class's stacking at one row.

    Attributes:
        kept_stacked_share: The share of the kept useful beams that are stacked layers.
        median_separation_deg: The median separation of a stacked layer from the cell's
            other layers, degrees; None exactly when the row keeps no stacked beam (a
            statistic of no beams does not exist).
        mean_full_sum_interference_db: The mean full-sum interference a beam sees from its
            cell's other layers, dB; None exactly when the row keeps no stacked beam.
    """

    model_config = _CONTRACT_MODEL_CONFIG

    kept_stacked_share: float = Field(ge=0, le=1.0)
    median_separation_deg: Annotated[float, Field(ge=0)] | None
    mean_full_sum_interference_db: float | None

    @model_validator(mode="after")
    def _statistics_exactly_when_stacked(self) -> Self:
        """Refuse statistics of no stacked beams, or stacked beams without their statistics."""
        stacked = self.kept_stacked_share > 0
        present = (
            self.median_separation_deg is not None,
            self.mean_full_sum_interference_db is not None,
        )
        if present != (stacked, stacked):
            raise ValueError(
                "the median separation and the mean full-sum interference must be set exactly "
                f"when stacked beams are kept; got a kept stacked share of "
                f"{self.kept_stacked_share} with {self.median_separation_deg} and "
                f"{self.mean_full_sum_interference_db}"
            )
        return self


class TrimAtFloor(BaseModel):
    """The interference trim at one far-sidelobe floor.

    Attributes:
        floor_dbi: The floor, dBi.
        trim: The capacity lost, a fraction: 1 - mean log2(1 + 1 / (1 + x)) over the
            victims, x being a victim's aggregate interference over its own signal.
    """

    model_config = _CONTRACT_MODEL_CONFIG

    floor_dbi: float
    trim: float = Field(ge=0, le=1.0)


class CurveRow(BaseModel):
    """One fleet's row of a curve (d = 1, the reference panel).

    Attributes:
        fleet: The realized fleet, P x S of the request: the row's key.
        requested_fleet: The requested fleet N the row's shell is built from
            (:func:`walker_shape`). A reader rebuilds a row from it, never from ``fleet``.
        useful_beams: L, the snapshot mean of the co-channel beams placed over demand.
        useful_beams_spread: The snapshot spread of L (the standard deviation).
        capacity_gbps: The snapshot mean of the beams' capacity, Gbps.
        ocean_factor: U = L / (fleet x beams per satellite).
        ceiling_beams: The snapshot mean of the most the cells in view could use.
        supply_beams: The snapshot mean of the most the satellites could place.
        directional: The stacking diagnostics, for the two directional classes only.
        trim: The interference trim at each floor, for the phone class's central curve.
    """

    model_config = _CONTRACT_MODEL_CONFIG

    fleet: PositiveInt
    requested_fleet: PositiveInt
    useful_beams: float = Field(ge=0)
    useful_beams_spread: float = Field(ge=0)
    capacity_gbps: float = Field(ge=0)
    ocean_factor: float = Field(ge=0)
    ceiling_beams: float = Field(ge=0)
    supply_beams: float = Field(ge=0)
    directional: DirectionalDiagnostics | None
    trim: tuple[TrimAtFloor, ...] | None

    @model_validator(mode="after")
    def _fleet_is_the_realized_request(self) -> Self:
        """Refuse a row whose fleet is not the realized P x S of its requested fleet."""
        realized = math.prod(walker_shape(self.requested_fleet))
        if self.fleet != realized:
            raise ValueError(
                f"a row's fleet must be the realized P x S of its requested fleet: "
                f"{self.requested_fleet} realizes as {realized}, but the row's fleet is "
                f"{self.fleet}"
            )
        return self


class ClassMarkers(BaseModel):
    """A curve's markers, each read on the rows against the N-independent maximum use.

    Attributes:
        maximum_use_beams: The most the shell could ever use: every cell served by the best
            satellite the shell can offer it, capped by its people.
        saturation_number: The fleet at the first elasticity crossing under 0.10, rounded
            half up: the spectrum bound (ADR 005). None when not reached.
        saturation_not_reached_by: When the 0.10 crossing is not reached, the last midpoint
            at which the rows measure the elasticity: the geometric mean of the last two rows'
            fleets, rounded half up (the rows measure nothing past it, so it is never the last
            row's fleet); None when the crossing is reached.
        elasticity_under_0p25_fleet: The fleet at the first crossing under 0.25 (fragile to
            the demand definition), rounded half up; None when not reached by the last row,
            or when the crossing lies before the first midpoint (the geometric mean of the
            first two rows), where the rows cannot place it (the curve's limits then say so).
        fleet_at_90pct_of_maximum_use: The fleet at which L reaches 90 percent of maximum
            use, rounded half up; None when not reached by the last row, or when the first
            row already reaches it (the curve's limits then say so).
    """

    model_config = _CONTRACT_MODEL_CONFIG

    maximum_use_beams: float = Field(ge=0)
    saturation_number: PositiveInt | None
    saturation_not_reached_by: PositiveInt | None
    elasticity_under_0p25_fleet: PositiveInt | None
    fleet_at_90pct_of_maximum_use: PositiveInt | None

    @model_validator(mode="after")
    def _one_saturation_reading(self) -> Self:
        """Refuse markers that set both or neither of the saturation number and its absence."""
        if (self.saturation_number is None) == (self.saturation_not_reached_by is None):
            raise ValueError(
                "markers must set exactly one of saturation_number and "
                f"saturation_not_reached_by; got {self.saturation_number} and "
                f"{self.saturation_not_reached_by}"
            )
        return self


class ClassCurve(BaseModel):
    """One class's curve.

    Attributes:
        device_class: The class.
        rows: Its rows, strictly increasing in fleet.
        markers: Its markers.
    """

    model_config = _CONTRACT_MODEL_CONFIG

    device_class: DeviceClass
    rows: tuple[CurveRow, ...] = Field(min_length=1)
    markers: ClassMarkers

    @model_validator(mode="after")
    def _rows_increase(self) -> Self:
        """Refuse rows that do not strictly increase in fleet."""
        _check_strictly_increasing(
            [row.fleet for row in self.rows], f"the {self.device_class.value} rows' fleets"
        )
        return self


class BandCurve(BaseModel):
    """One band point's curve (the phone class).

    Attributes:
        point: The band point.
        rows: Its rows, strictly increasing in fleet.
        markers: Its markers.
    """

    model_config = _CONTRACT_MODEL_CONFIG

    point: BandPoint
    rows: tuple[CurveRow, ...] = Field(min_length=1)
    markers: ClassMarkers

    @model_validator(mode="after")
    def _rows_increase(self) -> Self:
        """Refuse rows that do not strictly increase in fleet."""
        _check_strictly_increasing(
            [row.fleet for row in self.rows], f"the {self.point.name.value} rows' fleets"
        )
        return self


class RunMeasurement(BaseModel):
    """What the run that computed the curve measured of itself.

    The one part of a curve that differs between two runs of the same inputs, so every
    byte-identity check sets it to the other file's before comparing.

    Attributes:
        wall_time_s: The computation's wall time, seconds.
        peak_memory_mb: An upper bound on its peak memory, MB (10^6 bytes): the parent
            process's peak plus the sum of the peaks of the largest set of workers alive at
            once.
    """

    model_config = _CONTRACT_MODEL_CONFIG

    wall_time_s: float = Field(ge=0)
    peak_memory_mb: float = Field(ge=0)


class CurveProvenance(BaseModel):
    """Where a curve comes from.

    Attributes:
        grid_file_name: The population grid's file name.
        grid_sha256: The grid's SHA-256.
        citations: The grid's citations.
        licence: The grid's licence.
        method: How the curve is computed, stated as the rule.
        checks_passed: The checks the computation passed, each stated as its rule.
        run_measurement: The run's measured wall time and peak memory.
    """

    model_config = _CONTRACT_MODEL_CONFIG

    grid_file_name: str
    grid_sha256: str = Field(pattern=_SHA256_HEX_PATTERN)
    citations: tuple[str, ...]
    licence: str
    method: str
    checks_passed: tuple[str, ...]
    run_measurement: RunMeasurement


class SaturationCurve(BaseModel):
    """The saturation curve: every class's rows and markers, and the band points'.

    Attributes:
        schema_version: :data:`SATURATION_CURVE_SCHEMA_VERSION`.
        version_stamp: The stamp the computation was given.
        parameters: The inputs the curve was computed from.
        input_hash: The SHA-256 of ``parameters``' canonical JSON (:func:`curve_input_hash`).
        provenance: Where the curve comes from.
        classes: The class curves, each class at most once, in :class:`DeviceClass` order.
        bands: The band points' curves (the phone class), each at most once, in
            :class:`BandName` order.
        limits: The curve's stated limits, each stated as its rule.
    """

    model_config = _CONTRACT_MODEL_CONFIG

    schema_version: str
    version_stamp: str
    parameters: SaturationInputs
    input_hash: str = Field(pattern=_SHA256_HEX_PATTERN)
    provenance: CurveProvenance
    classes: tuple[ClassCurve, ...]
    bands: tuple[BandCurve, ...]
    limits: tuple[str, ...]

    @model_validator(mode="after")
    def _classes_and_bands_in_order(self) -> Self:
        """Refuse a class or band point listed twice or out of its enum's order."""
        _check_enum_order(
            [curve.device_class for curve in self.classes],
            DeviceClass,
            "classes",
            every_member=False,
        )
        _check_enum_order(
            [curve.point.name for curve in self.bands], BandName, "bands", every_member=False
        )
        return self


# ===========================================================================
# 3. The inputs a config implies, and the input hash
# ===========================================================================


def saturation_inputs_for(iridium: IridiumDials) -> SaturationInputs:
    """Return the curve's inputs a config's Iridium dials imply.

    Only the held spectrum comes from the dials. The panel (``aperture_m2``) does not: the
    curve is computed at the reference panel and the engine scales it by the scenario's
    panel over that one. Every other field comes from its named constant.

    Args:
        iridium: A config's Iridium dials.

    Returns:
        The default inputs with the dials' spectrum.
    """
    return SaturationInputs(spectrum_mhz=iridium.spectrum_mhz)


def curve_input_hash(parameters: SaturationInputs) -> str:
    """Return the SHA-256 of the inputs' canonical JSON, as lowercase hex.

    The canonical JSON is the inputs' JSON form with sorted keys and compact separators, so
    the digest depends on the values only, never on field order or formatting.

    Args:
        parameters: The curve's inputs.

    Returns:
        The digest, 64 hex characters.
    """
    canonical = json.dumps(
        parameters.model_dump(mode="json"),
        sort_keys=True,
        separators=_CANONICAL_JSON_SEPARATORS,
        allow_nan=False,
    )
    return hashlib.sha256(canonical.encode(TEXT_ENCODING)).hexdigest()


# ===========================================================================
# 4. The promoted curve: what it must carry, and its loader
# ===========================================================================


class SaturationCurveError(ValueError):
    """A saturation curve that cannot be used: a key repeated in one JSON object, a number out of
    range, another schema, a JSON type or a shape the contract refuses, altered parameters or input
    hash, or a curve that fails its completeness check (something missing or misplaced, a quantity
    not above 0, or markers its rows cannot give). The base of the curve's errors."""


def _check_rows_requested(name: str, rows: Sequence[CurveRow], requested: Sequence[int]) -> None:
    """Refuse a curve's rows unless they stand at exactly the sweep's requested fleets.

    Raises:
        SaturationCurveError: Naming the curve and both lists.
    """
    found = [row.requested_fleet for row in rows]
    if found != list(requested):
        raise SaturationCurveError(
            f"the {name} rows stand at the requested fleets {found}, not the sweep's "
            f"{list(requested)}"
        )


def _check_markers_on_rows(name: str, rows: Sequence[CurveRow], markers: ClassMarkers) -> None:
    """Refuse markers that their own rows cannot give, by necessary conditions only.

    Each condition follows from how the computation reads the markers on the rows
    (``communications.saturation._markers``): the 0.10 and 0.25 crossings are interpolated in
    ln N between consecutive geometric midpoints of the rows' fleets, sqrt(N_i x N_i+1), and
    rounded half up, so each lies between the first and the last midpoint, each rounded half
    up; a saturation number not reached names exactly the last midpoint, rounded half up (the
    last fleet at which the rows measure the elasticity); the 90 percent fleet is
    interpolated between two rows and rounded half up, so it lies within the rows' span; and
    maximum use, the most the shell could ever use, is at least every row's ceiling (by
    :func:`exceeds_bound`). A marker that meets them all may still not be the one its rows give
    (a saturation number moved within its span, say): the exact re-derivation is ``_markers``
    itself, which the drift tests run on the committed curve. The rows hold two or more fleets
    (the completeness check refuses rows off the sweep's requested fleets first, and a sweep
    requests two or more), so every span holds at least one midpoint.

    Raises:
        SaturationCurveError: Naming the curve, the marker or row, and the values.
    """
    fleets = [row.fleet for row in rows]
    midpoints = [round_half_up(math.sqrt(low * high)) for low, high in pairwise(fleets)]
    if markers.saturation_not_reached_by not in (None, midpoints[-1]):
        raise SaturationCurveError(
            f"the {name} saturation_not_reached_by is {markers.saturation_not_reached_by}, not "
            f"its last measured midpoint, {midpoints[-1]} (the geometric mean of its last two "
            "rows' fleets, rounded half up)"
        )
    between_midpoints = "the span of its rows' geometric midpoints"
    for field, fleet, where, span in (
        ("saturation_number", markers.saturation_number, between_midpoints, midpoints),
        (
            "elasticity_under_0p25_fleet",
            markers.elasticity_under_0p25_fleet,
            between_midpoints,
            midpoints,
        ),
        (
            "fleet_at_90pct_of_maximum_use",
            markers.fleet_at_90pct_of_maximum_use,
            "its rows' span",
            fleets,
        ),
    ):
        if fleet is None:
            continue
        if not span[0] <= fleet <= span[-1]:
            raise SaturationCurveError(
                f"the {name} {field} {fleet} lies outside {where}, {span[0]} to {span[-1]}"
            )
    for row in rows:
        if exceeds_bound(row.ceiling_beams, markers.maximum_use_beams):
            raise SaturationCurveError(
                f"the {name} row at {row.fleet} satellites has a ceiling of {row.ceiling_beams} "
                f"beams, above its maximum use of {markers.maximum_use_beams}"
            )


def _check_positive(name: str, rows: Sequence[CurveRow], markers: ClassMarkers) -> None:
    """Refuse a curve whose maximum use, or any row's useful beams, capacity or ocean factor, is
    not above 0.

    A computed curve's never is: the computation refuses a row whose capacity is not positive
    (its markers read the capacity's elasticity), a row with capacity has lit beams over people
    (so L and U are positive too), and maximum use is at least every row's ceiling, which is at
    least its L. The readings take the logarithms of these values between rows and divide by
    maximum use, so a file holding a 0 would read zeros at and below its row, silently.

    Raises:
        SaturationCurveError: Naming the curve, the row (or its maximum use), the quantity and
            its value.
    """
    if markers.maximum_use_beams <= 0:
        raise SaturationCurveError(
            f"the {name} maximum use is {markers.maximum_use_beams} beams, not above 0"
        )
    for row in rows:
        for quantity, value in (
            ("useful beams", row.useful_beams),
            ("capacity", row.capacity_gbps),
            ("ocean factor", row.ocean_factor),
        ):
            if value <= 0:
                raise SaturationCurveError(
                    f"the {name} row at {row.fleet} satellites has its {quantity} at {value}, "
                    "not above 0"
                )


def _check_row_placement(name: str, row: CurveRow, *, directional: bool, trim: bool) -> None:
    """Refuse a row whose stacking diagnostics or trim are not where the contract puts them.

    Raises:
        SaturationCurveError: Naming the curve, the row and what is missing or misplaced.
    """
    if directional and row.directional is None:
        raise SaturationCurveError(
            f"the {name} row at {row.fleet} satellites lacks its stacking diagnostics (its class "
            "has sky sectors)"
        )
    if not directional and row.directional is not None:
        raise SaturationCurveError(
            f"the {name} row at {row.fleet} satellites carries stacking diagnostics, though its "
            "class has no sky sectors"
        )
    if trim and row.trim is None:
        raise SaturationCurveError(f"the {name} row at {row.fleet} satellites lacks its trim")
    if not trim and row.trim is not None:
        raise SaturationCurveError(
            f"the {name} row at {row.fleet} satellites carries a trim, which only the phone "
            "class's central rows carry"
        )


def check_curve_complete(curve: SaturationCurve) -> None:
    """Refuse a curve that lacks anything a promoted curve must carry, or holds what it must not.

    A promoted curve carries every class, in :class:`~communications.constants.DeviceClass`
    order, and every band point, in :class:`BandName` order, each band point the one its
    parameters name; its stated limits and the checks it passed (neither empty), and the grid
    its parameters name (the provenance's digest, the grid's identity; its file name is a label
    the parameters' path already gives); each curve's rows at exactly the sweep's requested
    fleets (the mounted terminal's with its extension); the stacking diagnostics on every row of
    a class whose parameters give it sky sectors (a band point's rows by the phone class's) and
    on no other row, as the computation places them; the interference trim, at the parameters'
    floors, on every row of the phone class's central curve and on no other row; every row's
    useful beams, capacity and ocean factor, and every class's and band point's maximum use,
    above 0, as a computed curve's always are (:func:`_check_positive`); and markers that meet
    the necessary conditions of :func:`_check_markers_on_rows`.

    Args:
        curve: The curve.

    Raises:
        SaturationCurveError: Naming the curve and what is missing or misplaced (a class, a band
            point, the limits, the checks, the grid's digest, a row, its diagnostics or its
            trim), a quantity not above 0, or a marker its rows cannot give.
    """
    parameters = curve.parameters
    sweep = parameters.sweep
    found_classes = [entry.device_class for entry in curve.classes]
    missing_classes = [member.value for member in DeviceClass if member not in found_classes]
    if missing_classes:
        raise SaturationCurveError(f"the curve lacks the classes {missing_classes}")
    found_bands = [entry.point.name for entry in curve.bands]
    missing_bands = [member.value for member in BandName if member not in found_bands]
    if missing_bands:
        raise SaturationCurveError(f"the curve lacks the band points {missing_bands}")
    if not curve.limits:
        raise SaturationCurveError("the curve states no limits")
    provenance = curve.provenance
    if not provenance.checks_passed:
        raise SaturationCurveError("the curve's provenance names no checks passed")
    if provenance.grid_sha256 != parameters.demand.grid_sha256:
        raise SaturationCurveError(
            f"the provenance's grid digest {provenance.grid_sha256} is not the parameters' "
            f"{parameters.demand.grid_sha256}"
        )
    sectored = {
        entry.device_class: bool(entry.sector_wedges_per_ring) for entry in parameters.classes
    }
    floors = list(parameters.trim.floors_dbi)
    for entry in curve.classes:
        name = entry.device_class.value
        _check_rows_requested(
            name,
            entry.rows,
            sweep.fleets + sweep.mounted_terminal_extension
            if entry.device_class is DeviceClass.MOUNTED_TERMINAL_CLASS
            else sweep.fleets,
        )
        phone = entry.device_class is DeviceClass.PHONE_CLASS
        for row in entry.rows:
            _check_row_placement(name, row, directional=sectored[entry.device_class], trim=phone)
            if row.trim is not None and [at_floor.floor_dbi for at_floor in row.trim] != floors:
                raise SaturationCurveError(
                    f"the {name} row at {row.fleet} satellites carries its trim at the floors "
                    f"{[at_floor.floor_dbi for at_floor in row.trim]}, not the parameters' "
                    f"{floors}"
                )
        _check_positive(name, entry.rows, entry.markers)
        _check_markers_on_rows(name, entry.rows, entry.markers)
    for band, point in zip(curve.bands, parameters.bands, strict=True):
        name = f"band point {band.point.name.value}"
        if band.point != point:
            raise SaturationCurveError(
                f"the {name} is {band.point.model_dump()}, not its parameters' {point.model_dump()}"
            )
        _check_rows_requested(name, band.rows, sweep.fleets)
        for row in band.rows:
            _check_row_placement(
                name, row, directional=sectored[DeviceClass.PHONE_CLASS], trim=False
            )
        _check_positive(name, band.rows, band.markers)
        _check_markers_on_rows(name, band.rows, band.markers)


def _object_refusing_repeated_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Build one JSON object, refusing a key it holds twice (``json.loads`` would keep the last
    value silently, and another reader might keep the first).

    Raises:
        SaturationCurveError: Naming the repeated key.
    """
    built: dict[str, object] = {}
    for key, value in pairs:
        if key in built:
            raise SaturationCurveError(
                f"the key {key!r} appears twice in one JSON object, so a reader could take "
                "either value"
            )
        built[key] = value
    return built


def _validation_summary(exc: ValidationError) -> str:
    """Return a pydantic validation error as one line, read as :func:`common.cli.describe_failure`
    reads one: each error's location and message joined by ``;``, only the message where the
    error has no location (a refusal of the whole curve, or text pydantic's parser refuses), and
    a validator's own message without pydantic's ``Value error,`` prefix."""
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
    return "; ".join(parts)


def _json_root_kind(value: object) -> str:
    """Name a value Python's JSON parser produced in JSON's own words (null, true, false, a
    number, a string, an array), for a refusal of a root that is not an object."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int | float):
        return "a number"
    if isinstance(value, str):
        return "a string"
    return "an array"


def load_saturation_curve(path: Path) -> SaturationCurve:
    """Load a promoted saturation curve, refusing one the engine must not read.

    The file is read as UTF-8 text and parsed by Python's JSON parser with no key repeated in
    any object; its root must be an object whose ``schema_version`` is
    :data:`SATURATION_CURVE_SCHEMA_VERSION` (checked first, so a curve of another schema is named
    as such whatever its shape); it is validated as :class:`SaturationCurve` in pydantic's strict
    mode, so an integer field refuses a string, a float or a boolean, a float field refuses a
    string or a boolean (and reads a JSON integer as the same float), and a text field refuses a
    number or a boolean; its ``input_hash`` must be :func:`curve_input_hash` of its own
    parameters, so an altered parameter or hash fails; and it must pass
    :func:`check_curve_complete`.

    One rule sorts the refusals: a file that cannot be read, or whose text Python's JSON parser
    cannot read as JSON (malformed, or nested past its stack), is the file boundary's
    :class:`~common.file_io.ModelFileError`; every other refusal is a
    :class:`SaturationCurveError`, Python's parser's own for a repeated key or an integer past
    its limit on digits included, and so is any other number out of range (a requested fleet
    too large to build its shell from, a float past a float's range) and text pydantic's
    parser refuses where Python's read it (a lone surrogate, nesting past pydantic's depth).

    Args:
        path: The curve's JSON file.

    Returns:
        The curve.

    Raises:
        ModelFileError: If the file is missing or unreadable, not UTF-8, or not a JSON document
            Python's parser reads (malformed, or nested too deeply for it).
        SaturationCurveError: Naming the file, for a repeated key, a number out of range, a root
            that is not an object, another schema, a JSON type or a shape the contract refuses,
            an input hash that does not match the parameters, or a curve that fails
            :func:`check_curve_complete`.
    """
    try:
        text = path.read_text(encoding=TEXT_ENCODING)
    except FileNotFoundError as exc:
        raise ModelFileError(path, "file not found") from exc
    except OSError as exc:
        raise ModelFileError(
            path, f"could not read the saturation curve ({exc.strerror or exc})"
        ) from exc
    except UnicodeDecodeError as exc:
        raise ModelFileError(
            path, f"not valid {TEXT_ENCODING} text ({exc.reason} at byte {exc.start})"
        ) from exc
    try:
        data = json.loads(text, object_pairs_hook=_object_refusing_repeated_keys)
    except SaturationCurveError as exc:
        raise SaturationCurveError(f"{path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ModelFileError(path, f"not a JSON document ({exc})") from exc
    except RecursionError as exc:
        raise ModelFileError(
            path, f"not a JSON document Python's parser can read (nested too deeply: {exc})"
        ) from exc
    except ValueError as exc:
        raise SaturationCurveError(
            f"{path}: not a saturation curve (a number out of range: {exc})"
        ) from exc
    if not isinstance(data, dict):
        raise SaturationCurveError(
            f"{path}: not a saturation curve (its JSON root is {_json_root_kind(data)}, not an "
            "object)"
        )
    schema = data.get("schema_version")
    if schema != SATURATION_CURVE_SCHEMA_VERSION:
        raise SaturationCurveError(
            f"{path}: the curve's schema is {schema!r}, not {SATURATION_CURVE_SCHEMA_VERSION!r}"
        )
    try:
        curve = SaturationCurve.model_validate_json(text, strict=True)
    except ValidationError as exc:
        raise SaturationCurveError(
            f"{path}: not a saturation curve ({_validation_summary(exc)})"
        ) from exc
    except OverflowError as exc:
        raise SaturationCurveError(
            f"{path}: not a saturation curve (a number out of range: a row's requested_fleet is "
            f"too large to build its shell from, {exc})"
        ) from exc
    expected_hash = curve_input_hash(curve.parameters)
    if curve.input_hash != expected_hash:
        raise SaturationCurveError(
            f"{path}: the input hash {curve.input_hash} is not the hash of the curve's "
            f"parameters ({expected_hash}); the parameters or the hash were altered"
        )
    try:
        check_curve_complete(curve)
    except SaturationCurveError as exc:
        raise SaturationCurveError(f"{path}: {exc}") from exc
    logger.debug("loaded the saturation curve %s (input hash %s)", path, curve.input_hash)
    return curve


# ===========================================================================
# 5. The identity check and the readings (the engine's side of the curve)
# ===========================================================================


class SaturationCurveMismatchError(SaturationCurveError):
    """A curve used with inputs it was not computed for.

    The identity check (:func:`check_curve_matches`) raises it naming the first field of the
    inputs that differs from the curve's parameters, as a dotted path (``spectrum_mhz``, or
    ``classes.2.concurrency_peak`` inside a tuple), with both values.
    """


class CurveBeyondLastRowError(SaturationCurveError):
    """A reading at a fleet past a class's last row; the message names the fleet, the class and
    the last row's fleet. A curve is never extrapolated or clamped: a fleet past its last row
    needs a curve whose sweep reaches it."""


_EMPTY_FLEET: Final[int] = 0
"""A fleet of no satellites, the readings' lower edge: it places no beam."""

_EMPTY_FLEET_READING: Final[float] = 0.0
"""Useful beams, capacity, people and the share of maximum use at a fleet of 0 (its ocean
factor, the share of the beams offered that lie over people, does not exist, and is read as
None)."""

_FULL_TIME_DOWNLINK_SHARE: Final[float] = 1.0
"""The largest downlink share d: the band in full-time downlink use, the curve's own basis
(ADR 008)."""


def _first_difference(
    path: str, expected: object, found: object
) -> tuple[str, object, object] | None:
    """Return where two JSON-form values first differ, or None when they are equal.

    Objects are walked in their keys' order and arrays element by element, so the difference
    found first is the first in the inputs' field order; an array whose length differs is
    itself the difference.

    Args:
        path: The dotted path of the two values (empty at the root).
        expected: The value the run's inputs hold.
        found: The value the curve's parameters hold.

    Returns:
        The first differing value's dotted path and its two values, or None.
    """
    if isinstance(expected, dict) and isinstance(found, dict):
        for key, value in expected.items():
            child = f"{path}.{key}" if path else str(key)
            difference = _first_difference(child, value, found.get(key))
            if difference is not None:
                return difference
        return None
    if isinstance(expected, list) and isinstance(found, list) and len(expected) == len(found):
        for index, (one, other) in enumerate(zip(expected, found, strict=True)):
            difference = _first_difference(f"{path}.{index}", one, other)
            if difference is not None:
                return difference
        return None
    return None if expected == found else (path, expected, found)


def check_curve_matches(inputs: SaturationInputs, curve: SaturationCurve) -> None:
    """Refuse a curve computed for other inputs than a run's own: the identity check.

    The run's inputs (``saturation_inputs_for`` of its Iridium dials) are compared with the
    curve's parameters field by field, in the inputs' field order, so a run at another value of
    an input the curve depends on (another held spectrum, say) never reads a curve computed for
    a different value. The loader ties the curve's input hash to its parameters; this check ties
    the parameters to the run.

    Args:
        inputs: The run's curve inputs.
        curve: The curve the run would read.

    Raises:
        SaturationCurveMismatchError: Naming the first field that differs, as a dotted path,
            with the run's value and the curve's.
    """
    difference = _first_difference(
        "", inputs.model_dump(mode="json"), curve.parameters.model_dump(mode="json")
    )
    if difference is None:
        return
    path, expected, found = difference
    raise SaturationCurveMismatchError(
        f"the saturation curve was computed for other inputs: {path} is {json.dumps(expected)} "
        f"for this run but {json.dumps(found)} in the curve's parameters; a run reads only a "
        "curve computed for its own inputs (promote one with python -m communications.saturation "
        "and name it in iridium.saturation.curve_path)"
    )


@dataclass(frozen=True)
class FleetReading:
    """One class's readings at one fleet, at a downlink share d and a panel factor.

    The panel factor is the scenario's panel area over the curve's reference panel area
    (``curve.parameters.shell.reference_aperture_m2``, the panel the curve is computed at): a
    ratio, never an area. Useful beams scale with the panel factor alone; capacity with d and
    the panel factor, scaled once, and people derive from that scaled capacity; the share of
    maximum use and the ocean factor do not scale (each is a ratio on the curve's own basis).

    Attributes:
        fleet: The fleet read, satellites.
        useful_beams: L x the panel factor.
        capacity_gbps: The capacity x d x the panel factor, Gbps.
        share_of_maximum_use: L over the class's maximum use (the panel factor cancels); 0.0 at
            a fleet of 0.
        ocean_factor: U = L / (N x B), read from the curve's rows; None at a fleet of 0.
        people: That scaled capacity over the class's busy-hour load per person, unrounded (a
            caller rounds half up where it publishes a count).
    """

    fleet: int
    useful_beams: float
    capacity_gbps: float
    share_of_maximum_use: float
    ocean_factor: float | None
    people: float


class _BelowFirstRow(StrEnum):
    """How a row quantity reads at a fleet below a class's first row."""

    THROUGH_THE_ORIGIN = "linear through the origin"
    """N x the first row's value over its fleet: useful beams and capacity."""

    FLAT = "flat"
    """The first row's value: the ocean factor, flat where L is linear in N."""


@dataclass(frozen=True)
class _RowQuantity:
    """One quantity a curve's rows carry, as the readings read it.

    Attributes:
        name: Its name, for a message.
        value_of: Its value at a row.
        below_first_row: How it reads below the class's first row.
    """

    name: str
    value_of: Callable[[CurveRow], float]
    below_first_row: _BelowFirstRow


_USEFUL_BEAMS: Final[_RowQuantity] = _RowQuantity(
    "useful beams", lambda row: row.useful_beams, _BelowFirstRow.THROUGH_THE_ORIGIN
)
"""L, beams on the curve's own basis: linear through the origin below the first row."""

_CAPACITY: Final[_RowQuantity] = _RowQuantity(
    "capacity", lambda row: row.capacity_gbps, _BelowFirstRow.THROUGH_THE_ORIGIN
)
"""The capacity, Gbps on the curve's own basis: linear through the origin below the first row."""

_OCEAN_FACTOR: Final[_RowQuantity] = _RowQuantity(
    "ocean factor", lambda row: row.ocean_factor, _BelowFirstRow.FLAT
)
"""U: flat below the first row, where L is linear in N and B is fixed."""

_NOT_BETWEEN_ROWS: Final[float] = 0.0
"""The fraction a bracket carries at a row and below the first row, where no reading uses it."""


@dataclass(frozen=True)
class _Bracket:
    """A positive fleet's place on a class's central curve, found once for every quantity read
    there: the class's curve looked up, the fleet's range checked and the rows bisected once.

    Attributes:
        curve: The class's central curve.
        fleet: The fleet, above 0 and at most the class's last row's.
        high: The row at the fleet, or the first row above it.
        low: The row below the fleet when the fleet lies between two rows; None at a row and
            below the first row.
        fraction: Between two rows, ln(N / N_low) / ln(N_high / N_low), the fleet's place
            between them in ln N; :data:`_NOT_BETWEEN_ROWS` otherwise.
    """

    curve: ClassCurve
    fleet: int
    high: CurveRow
    low: CurveRow | None
    fraction: float

    def read(self, quantity: _RowQuantity) -> float:
        """Return a quantity at the fleet, by the edge rules: at a row, the row's own value;
        below the first row, as the quantity's rule says; between two rows, log-log (the
        quantity's logarithm linear in ln N).

        Raises:
            SaturationCurveError: Between two rows at which the quantity is not positive at
                both (its logarithm does not exist). A loaded curve's rows never are (the
                completeness check refuses one), so this guards a curve built in Python.
        """
        high, low = self.high, self.low
        if high.fleet == self.fleet:
            return quantity.value_of(high)
        if low is None:
            if quantity.below_first_row is _BelowFirstRow.FLAT:
                return quantity.value_of(high)
            return self.fleet * quantity.value_of(high) / high.fleet
        low_value, high_value = quantity.value_of(low), quantity.value_of(high)
        if low_value <= 0 or high_value <= 0:
            raise SaturationCurveError(
                f"the {self.curve.device_class.value} curve's {quantity.name} must be positive "
                f"at both rows around {self.fleet} satellites to read between them log-log; got "
                f"{low_value} at {low.fleet} satellites and {high_value} at {high.fleet}"
            )
        return math.exp(math.log(low_value) + self.fraction * math.log(high_value / low_value))


def _class_curve_of(curve: SaturationCurve, device_class: DeviceClass) -> ClassCurve:
    """Return a class's curve: the central one, which the engine reads (never a band point's).

    Raises:
        SaturationCurveError: If the curve holds no curve for the class.
    """
    for entry in curve.classes:
        if entry.device_class is device_class:
            return entry
    raise SaturationCurveError(f"the saturation curve holds no {device_class.value} curve to read")


def _bracket(curve: SaturationCurve, device_class: DeviceClass, fleet: int) -> _Bracket | None:
    """Find a fleet's place on a class's central curve, once for every quantity read there.

    Args:
        curve: The curve.
        device_class: The class, whose central curve is read.
        fleet: The fleet, satellites, at least 0.

    Returns:
        The fleet's place, or None at a fleet of 0, which places no beam.

    Raises:
        SaturationCurveError: If the curve holds no curve for the class.
        ValueError: For a negative fleet.
        CurveBeyondLastRowError: For a fleet past the class's last row (a curve is never
            extrapolated or clamped).
    """
    entry = _class_curve_of(curve, device_class)
    if fleet < _EMPTY_FLEET:
        raise ValueError(f"a fleet is a count of satellites, at least 0; got {fleet}")
    if fleet == _EMPTY_FLEET:
        return None
    rows = entry.rows
    last = rows[-1]
    if fleet > last.fleet:
        raise CurveBeyondLastRowError(
            f"the {device_class.value} curve's last row is at {last.fleet} satellites, and a "
            f"reading at {fleet} satellites lies past it: a curve is never extrapolated or "
            "clamped, so a fleet past its last row needs a curve whose sweep reaches it"
        )
    index = bisect_left(rows, fleet, key=lambda row: row.fleet)
    high = rows[index]
    if high.fleet == fleet or index == 0:
        return _Bracket(curve=entry, fleet=fleet, high=high, low=None, fraction=_NOT_BETWEEN_ROWS)
    low = rows[index - 1]
    fraction = math.log(fleet / low.fleet) / math.log(high.fleet / low.fleet)
    return _Bracket(curve=entry, fleet=fleet, high=high, low=low, fraction=fraction)


def _reading(bracket: _Bracket | None, quantity: _RowQuantity) -> float:
    """Return a quantity at a fleet :func:`_bracket` placed: 0.0 at a fleet of 0 (no beams and
    no capacity), else the bracket's reading."""
    return _EMPTY_FLEET_READING if bracket is None else bracket.read(quantity)


def _check_factors(downlink_share: float, panel_factor: float) -> None:
    """Refuse a downlink share outside (0, 1], or a panel factor that is not a positive number.

    Raises:
        ValueError: Naming the factor and its value.
    """
    if not 0 < downlink_share <= _FULL_TIME_DOWNLINK_SHARE:
        raise ValueError(
            f"the downlink share d must be above 0 and at most {_FULL_TIME_DOWNLINK_SHARE:g}; "
            f"got {downlink_share}"
        )
    if not (math.isfinite(panel_factor) and panel_factor > 0):
        raise ValueError(f"the panel factor must be a positive finite number; got {panel_factor}")


def _busy_hour_load_mbps(curve: SaturationCurve, device_class: DeviceClass) -> float:
    """Return a class's busy-hour load per person, Mbps: its rate while active times its
    busy-hour share, read from the curve's parameters (which the identity check ties to the
    named constants; they hold exactly one entry per class, so the class is always found)."""
    return next(
        entry.active_rate_mbps * entry.concurrency_peak
        for entry in curve.parameters.classes
        if entry.device_class is device_class
    )


def _scaled_capacity_and_people(
    capacity_gbps: float, load_mbps: float, *, downlink_share: float, panel_factor: float
) -> tuple[float, float]:
    """Scale a capacity on the curve's basis (d = 1, the reference panel) to d and the panel
    factor, once, and derive the people that scaled capacity serves: the one place both scale.

    Args:
        capacity_gbps: The capacity on the curve's basis, Gbps.
        load_mbps: The class's busy-hour load per person, Mbps.
        downlink_share: The downlink share d.
        panel_factor: The scenario's panel area over the curve's reference panel area.

    Returns:
        The scaled capacity, Gbps, and the people it serves (it over the load), unrounded.
    """
    scaled_gbps = capacity_gbps * downlink_share * panel_factor
    return scaled_gbps, scaled_gbps * GBPS_TO_MBPS / load_mbps


def useful_beams_at(curve: SaturationCurve, device_class: DeviceClass, fleet: int) -> float:
    """Return a class's useful beams L at a fleet, on the curve's own basis (d = 1, the
    reference panel).

    By the edge rules: at a row its own L; between rows log-log; below the first row linear
    through the origin; 0 at a fleet of 0; past the class's last row refused.

    Args:
        curve: The curve.
        device_class: The class, whose central curve is read.
        fleet: The fleet, satellites, at least 0.

    Returns:
        L, beams.

    Raises:
        CurveBeyondLastRowError: For a fleet past the class's last row.
        SaturationCurveError: If the curve holds no curve for the class, or L is not positive
            at both rows around the fleet.
        ValueError: For a negative fleet.
    """
    return _reading(_bracket(curve, device_class, fleet), _USEFUL_BEAMS)


def capacity_gbps_at(curve: SaturationCurve, device_class: DeviceClass, fleet: int) -> float:
    """Return a class's capacity at a fleet, Gbps, on the curve's own basis (d = 1, the
    reference panel), by the same edge rules as :func:`useful_beams_at`.

    Args:
        curve: The curve.
        device_class: The class, whose central curve is read.
        fleet: The fleet, satellites, at least 0.

    Returns:
        The capacity, Gbps.

    Raises:
        CurveBeyondLastRowError: For a fleet past the class's last row.
        SaturationCurveError: If the curve holds no curve for the class, or the capacity is not
            positive at both rows around the fleet.
        ValueError: For a negative fleet.
    """
    return _reading(_bracket(curve, device_class, fleet), _CAPACITY)


def people_at(
    curve: SaturationCurve,
    device_class: DeviceClass,
    fleet: int,
    *,
    downlink_share: float,
    panel_factor: float,
) -> float:
    """Return the people a class's curve serves at a fleet, unrounded.

    The capacity at the fleet (:func:`capacity_gbps_at`) x the downlink share d x the panel
    factor, over the class's busy-hour load per person (its rate while active times its
    busy-hour share, from the curve's parameters). The panel factor is the scenario's panel
    area over the curve's reference panel area (``curve.parameters.shell.reference_aperture_m2``):
    a ratio, never an area. People stay floats here; a caller rounds half up where it
    publishes a count.

    Args:
        curve: The curve.
        device_class: The class, whose central curve is read.
        fleet: The fleet, satellites, at least 0.
        downlink_share: The downlink share d, above 0 and at most 1.
        panel_factor: The scenario's panel area over the curve's reference panel area, above 0.

    Returns:
        People, unrounded.

    Raises:
        CurveBeyondLastRowError: For a fleet past the class's last row.
        SaturationCurveError: If the curve holds no curve for the class, or the capacity is not
            positive at both rows around the fleet.
        ValueError: For a negative fleet, or a factor out of its range.
    """
    _check_factors(downlink_share, panel_factor)
    _, people = _scaled_capacity_and_people(
        _reading(_bracket(curve, device_class, fleet), _CAPACITY),
        _busy_hour_load_mbps(curve, device_class),
        downlink_share=downlink_share,
        panel_factor=panel_factor,
    )
    return people


def read_fleet(
    curve: SaturationCurve,
    device_class: DeviceClass,
    fleet: int,
    *,
    downlink_share: float,
    panel_factor: float,
) -> FleetReading:
    """Return all of a class's readings at a fleet, by the edge rules, from one bracketing of
    the fleet.

    Useful beams as :func:`useful_beams_at` reads them, x the panel factor; capacity as
    :func:`capacity_gbps_at` reads it, x d x the panel factor, and people from that scaled
    capacity, as :func:`people_at` gives them; the share of maximum use, L over the class's
    maximum use on the curve's own basis; the ocean factor U, read from the rows like L
    (log-log between rows, since U = L / (N x B) with B fixed) but flat below the first row. At
    a fleet of 0 the readings are 0 and U is None. The panel factor is the scenario's panel
    area over the curve's reference panel area (``curve.parameters.shell.reference_aperture_m2``).

    Args:
        curve: The curve.
        device_class: The class, whose central curve is read.
        fleet: The fleet, satellites, at least 0.
        downlink_share: The downlink share d, above 0 and at most 1.
        panel_factor: The scenario's panel area over the curve's reference panel area, above 0.

    Returns:
        The readings.

    Raises:
        CurveBeyondLastRowError: For a fleet past the class's last row.
        SaturationCurveError: If the curve holds no curve for the class, a quantity is not
            positive at both rows around the fleet, or the class's maximum use is 0 (never on
            a loaded curve: the completeness check refuses one).
        ValueError: For a negative fleet, or a factor out of its range.
    """
    _check_factors(downlink_share, panel_factor)
    bracket = _bracket(curve, device_class, fleet)
    useful_beams = _reading(bracket, _USEFUL_BEAMS)
    capacity_gbps, people = _scaled_capacity_and_people(
        _reading(bracket, _CAPACITY),
        _busy_hour_load_mbps(curve, device_class),
        downlink_share=downlink_share,
        panel_factor=panel_factor,
    )
    if bracket is None:
        share_of_maximum_use, ocean_factor = _EMPTY_FLEET_READING, None
    else:
        maximum_use = bracket.curve.markers.maximum_use_beams
        if maximum_use <= 0:
            raise SaturationCurveError(
                f"the {device_class.value} curve's maximum use is {maximum_use} beams, so no "
                "share of it can be read"
            )
        share_of_maximum_use = useful_beams / maximum_use
        ocean_factor = bracket.read(_OCEAN_FACTOR)
    return FleetReading(
        fleet=fleet,
        useful_beams=useful_beams * panel_factor,
        capacity_gbps=capacity_gbps,
        share_of_maximum_use=share_of_maximum_use,
        ocean_factor=ocean_factor,
        people=people,
    )


__all__ = [
    "BOUNDS_RELATIVE_TOLERANCE",
    "SATURATION_CURVE_SCHEMA_VERSION",
    "BandCurve",
    "BandName",
    "BandPoint",
    "ClassCurve",
    "ClassInputs",
    "ClassMarkers",
    "CurveBeyondLastRowError",
    "CurveProvenance",
    "CurveRow",
    "DemandInputs",
    "DirectionalDiagnostics",
    "FleetReading",
    "RunMeasurement",
    "SaturationCurve",
    "SaturationCurveError",
    "SaturationCurveMismatchError",
    "SaturationInputs",
    "ShellInputs",
    "SweepInputs",
    "TrimAtFloor",
    "TrimInputs",
    "capacity_gbps_at",
    "check_curve_complete",
    "check_curve_matches",
    "curve_input_hash",
    "exceeds_bound",
    "load_saturation_curve",
    "people_at",
    "read_fleet",
    "saturation_inputs_for",
    "useful_beams_at",
    "walker_shape",
]
