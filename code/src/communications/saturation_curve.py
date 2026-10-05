"""The saturation curve's contract (foundation v1): its inputs, its result and its hash.

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
  spectrum), and :func:`curve_input_hash`, the SHA-256 of the inputs' canonical JSON.

Every model is a frozen pydantic model with ``extra="forbid"`` that refuses a NaN or an
infinity, so a curve's JSON is standard JSON. The validators that belong to the contract:
the inputs carry exactly one class per :class:`~communications.constants.DeviceClass` and
one band point per :class:`BandName`, each in its enum's order; the sweep's fleets strictly
increase and the mounted terminal's extension starts above the last of them; a curve
carries each class and each band point at most once, in its enum's order, and every tuple
of rows strictly increases in fleet. A curve may lack classes, band points or trims while
it is being built (the phone class first, the directional classes, then the bands and the
trim); the promotion's completeness check is what a promoted curve must pass.

This module imports :mod:`communications.config`; ``config.py`` does not import it.
"""

from __future__ import annotations

import hashlib
import json
import logging
from collections.abc import Mapping, Sequence
from enum import StrEnum
from itertools import pairwise
from types import MappingProxyType
from typing import Final, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeInt,
    PositiveInt,
    model_validator,
)

from common.file_io import TEXT_ENCODING
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
        elevation_mask_deg: The lowest elevation at which a device uses a satellite.
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
    elevation_mask_deg: float = Field(default=ELEVATION_MASK_DEG, ge=0, lt=_RIGHT_ANGLE_DEG)
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
        fleets: The requested fleets, strictly increasing (at least two, since a marker
            reads the elasticity between rows); each row is keyed by the realized fleet.
        mounted_terminal_extension: The mounted terminal's extra requested fleets,
            strictly increasing and above the last of ``fleets``.
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

    fleets: tuple[PositiveInt, ...] = Field(default=SATURATION_FLEETS, min_length=2)
    mounted_terminal_extension: tuple[PositiveInt, ...] = SATURATION_MOUNTED_TERMINAL_EXTENSION
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
            other layers, degrees.
        mean_full_sum_interference_db: The mean full-sum interference a beam sees from its
            cell's other layers, dB.
    """

    model_config = _CONTRACT_MODEL_CONFIG

    kept_stacked_share: float = Field(ge=0, le=1.0)
    median_separation_deg: float = Field(ge=0)
    mean_full_sum_interference_db: float


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
        fleet: The realized fleet, P x S.
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
    useful_beams: float = Field(ge=0)
    useful_beams_spread: float = Field(ge=0)
    capacity_gbps: float = Field(ge=0)
    ocean_factor: float = Field(ge=0)
    ceiling_beams: float = Field(ge=0)
    supply_beams: float = Field(ge=0)
    directional: DirectionalDiagnostics | None
    trim: tuple[TrimAtFloor, ...] | None


class ClassMarkers(BaseModel):
    """A curve's markers, each read on the rows against the N-independent maximum use.

    Attributes:
        maximum_use_beams: The most the shell could ever use: every cell served by the best
            satellite the shell can offer it, capped by its people.
        saturation_number: The fleet at the first elasticity crossing under 0.10, rounded
            half up: the spectrum bound (ADR 005). None when not reached.
        saturation_not_reached_by: The last row's fleet when the 0.10 crossing is not
            reached on the curve; None when it is.
        elasticity_under_0p25_fleet: The fleet at the first crossing under 0.25 (fragile to
            the demand definition), rounded half up; None when not reached.
        fleet_at_90pct_of_maximum_use: The fleet at which L reaches 90 percent of maximum
            use, rounded half up; None when not reached.
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


__all__ = [
    "SATURATION_CURVE_SCHEMA_VERSION",
    "BandCurve",
    "BandName",
    "BandPoint",
    "ClassCurve",
    "ClassInputs",
    "ClassMarkers",
    "CurveProvenance",
    "CurveRow",
    "DemandInputs",
    "DirectionalDiagnostics",
    "RunMeasurement",
    "SaturationCurve",
    "SaturationInputs",
    "ShellInputs",
    "SweepInputs",
    "TrimAtFloor",
    "TrimInputs",
    "curve_input_hash",
    "saturation_inputs_for",
]
