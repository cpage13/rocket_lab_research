"""The saturation curve: how many co-channel beams a Walker shell keeps lit over people.

The one module that imports numpy (ADR 010). For a device class on one set of inputs
(:class:`~communications.saturation_curve.SaturationInputs`) it computes, at each fleet of
the sweep, L: the most co-channel beams the shell can keep lit over the places people live
without two co-channel footprints overlapping on the same ground (a 0 dBi device cannot
tell satellites apart). L rises with the fleet, then flattens as every inhabited place is
served by its best satellite; the knee is the class's spectrum bound (ADR 005). Everything
is computed with the band in full-time use (d = 1, ADR 008) at the reference panel; the
engine applies d and the scenario's panel when it reads the curve. This version computes
the phone class's central curve, whose allocation is also the first layer every
directional class builds on.

The stages, for one class on one set of inputs:

1. **Demand cells.** Every cell of the shipped grid (ADR 009) with at least the threshold's
   people per km^2: its centre, its area on the sphere, its people, and its people cap in
   beams, people x take-up / people per beam, where people per beam is the spectrum times the
   class's central SE (a beam's rate) over the class's busy-hour load per person.
2. **The shell and the snapshots.** A circular Walker Delta shell: P = round(sqrt(N)) planes
   of S = round(N / P) satellites (Python's ``round``, an exact half to the even neighbour,
   as the reference shell has it; the contract's ``walker_shape``), the realized fleet P x S
   keying the row and the request carried on it, phasing F = 1,
   two-body motion with the Earth turning under it. The snapshot times are drawn once per
   run, ``numpy.random.default_rng(seed).uniform(0, sidereal day, n)``, and shared by every
   fleet.
3. **The view and the beam.** The elevation mask's central-angle limit; a square aperture's
   half-power beam, beamwidth factor x wavelength / side, and its footprint, pi / 4 x (r
   theta) x (r theta / (cos(scan) sin(elevation))) with r the slant range, tabulated against
   the central angle and read by linear interpolation; the beams per satellite B derived
   from the capacity calibration and the panel, never set.
4. **The pairs in view.** Every satellite-cell pair whose cell centre sees the satellite
   above the mask.
5. **The allocation, smallest footprint first.** A snapshot's pairs fall into geometric
   footprint bands with edges ``geomspace(min footprint x 0.999, max footprint x 1.001,
   bands + 1)``. Band by band from the smallest, each pair asks for min(one layer, the
   cell's area left / its footprint); a few alternating passes scale the band by every
   satellite's beams left, then by every cell's area and people left; the band is committed
   before the next. Limits: B beams per satellite; one co-channel layer per cell (its area);
   the cell's people cap; one layer per satellite per cell. Small overhead footprints fit
   the most beams into the same land, so this order maximizes capacity; a proportional
   fill stalls near saturation.
6. **The rows.** At each fleet, the snapshot means of L and of capacity (L x the spectrum x
   the class's SE), the spread of L, the ocean factor U = L / (N x B), and the two bounds:
   the ceiling (each cell in view served by its smallest footprint in view, capped by its
   people) and the supply (each satellite's beams, capped by what its cells could take).
7. **Maximum use**, in closed form and independent of the fleet: every cell served by the
   best satellite the shell can ever offer it, at central angle max(0, |latitude| -
   inclination), capped by its people.
8. **The markers**, on the rows: the elasticity of capacity, d ln C / d ln N, at each
   interval's geometric midpoint; the saturation number is the first crossing under 0.10,
   interpolated in ln N between the midpoints that straddle it and rounded half up (or the
   last fleet when it is not reached); beside it the crossing under 0.25 and the fleet at
   which L reaches 90 percent of maximum use (log-log between rows). The markers read
   maximum use, never a sweep-dependent ceiling.

The checks raise :class:`SaturationInvariantError`: the bounds (L at most min(ceiling,
supply) and the ceiling at most maximum use, at every snapshot, 1e-9 relative); the stall
floor (the phone class's L at least the sweep's floor x min(ceiling, supply) from 20,000
satellites up, at every snapshot and in the means); capacity per satellite never rising
between consecutive rows by more than 2 percent of the earlier row (the snapshots' noise).

The fleets' snapshots run in separate processes. The largest fleet's first snapshot runs
alone and measures a worker's peak memory; then as many workers run at once as keep the
parent's peak plus their summed peaks under the 16 GB budget, at most one per CPU. The
curve records the wall time and that bound (each worker reports its own peak; the bound is
the parent's peak plus the summed peaks of the largest set of workers alive at once).

Public: :func:`load_population_grid`, :class:`PopulationGrid`, :func:`compute_saturation`,
:class:`PopulationGridError` and :class:`SaturationInvariantError`. Everything else is
private; ``_allocate`` is the seam the tests drive with explicit satellite positions.
"""

from __future__ import annotations

import hashlib
import io
import logging
import math
import os
import resource
import sys
import time
import zipfile
from collections.abc import Sequence
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from dataclasses import dataclass
from itertools import pairwise, repeat
from multiprocessing import get_context
from pathlib import Path
from typing import Final

import numpy as np
import numpy.typing as npt

from common.cadence import round_half_up
from common.file_io import ModelFileError
from communications.constants import APERTURE_REFERENCE_M2, GBPS_TO_MBPS, DeviceClass
from communications.saturation_curve import (
    SATURATION_CURVE_SCHEMA_VERSION,
    ClassCurve,
    ClassInputs,
    ClassMarkers,
    CurveProvenance,
    CurveRow,
    RunMeasurement,
    SaturationCurve,
    SaturationInputs,
    ShellInputs,
    curve_input_hash,
)
from communications.saturation_curve import walker_shape as _walker_shape

logger = logging.getLogger(__name__)

# ===========================================================================
# Physical constants and the curve's pinned conventions
# ===========================================================================

_EARTH_RADIUS_KM: Final[float] = 6371.0
"""SOURCED_FACT (standard geodesy): the Earth's mean radius, km."""

_MU_EARTH_KM3_S2: Final[float] = 398600.4418
"""SOURCED_FACT (standard geodesy, WGS 84): the Earth's gravitational parameter, km^3/s^2."""

_SIDEREAL_DAY_S: Final[float] = 86164.0905
"""SOURCED_FACT (standard astronomy): one sidereal day, s, the Earth's rotation period."""

_SPEED_OF_LIGHT_M_S: Final[float] = 2.998e8
"""SOURCED_FACT (standard physics): the speed of light, m/s, to four figures, the
convention the curve is pinned to."""

_KEPLER_THIRD_LAW_POWER: Final[int] = 3
"""Kepler's third law: the square of a circular orbit's period grows as its radius cubed."""

_ELLIPSE_AREA_FACTOR: Final[float] = math.pi / 4
"""An ellipse's area over the product of its two axes: a footprint is this times its
cross-range and along-range widths."""

_ZONE_AREA_PER_SINE_KM2: Final[float] = math.tau * _EARTH_RADIUS_KM**2
"""The area of a zone of the sphere between two latitudes, km^2, per unit difference of
their sines (Archimedes: 2 pi R^2 x |sin(top) - sin(bottom)|)."""

_WALKER_PHASING: Final[int] = 1
"""The Walker Delta phasing F: plane j's satellites lead plane j - 1's by F x 360 / N
degrees of orbit (the curve's pinned convention)."""

_DAY_START_S: Final[float] = 0.0
"""The start of the sidereal day the snapshot times are drawn over, s."""

_OVERHEAD_CENTRAL_ANGLE_RAD: Final[float] = 0.0
"""The central angle of a satellite directly overhead: the smallest a pair can have."""

_FOOTPRINT_TABLE_POINTS: Final[int] = 4001
"""Central angles the footprint table holds from overhead to the mask; a footprint between
two of them is read by linear interpolation (the curve's pinned convention)."""

_CELL_CENTRE_FRACTION: Final[float] = 0.5
"""A grid cell's centre lies half a cell in from its northern and western edges."""

_NOT_DEMAND: Final[int] = -1
"""The demand-cell index a grid cell holds when it is not demand."""

_PAIR_SEARCH_CHUNK_SATELLITES: Final[int] = 500
"""Satellites whose grid windows are searched at once, which bounds the search's
temporary arrays; the pairs found do not depend on it."""

_WINDOW_MARGIN_CELLS: Final[int] = 1
"""Cells added beyond the view's reach on every side of a satellite's search window, so a
cell whose centre lies in view is never cut off by rounding."""

_WINDOW_LATITUDE_CAP_DEG: Final[float] = 89.0
"""The latitude a search window's width is computed at when the view reaches nearer a
pole, so the window stays finite (the curve's pinned convention)."""

_COSINE_BOUNDS: Final[tuple[float, float]] = (-1.0, 1.0)
"""A cosine's range: a dot product of unit vectors is clipped into it before the arccos,
since rounding can carry it a hair outside."""

_BAND_EDGE_LOW_FACTOR: Final[float] = 0.999
"""The lowest band edge sits this far under the snapshot's smallest footprint, so that
footprint falls inside the first band (the curve's pinned convention)."""

_BAND_EDGE_HIGH_FACTOR: Final[float] = 1.001
"""The highest band edge sits this far over the snapshot's largest footprint, so that
footprint falls inside the last band (the curve's pinned convention)."""

_FULL_SCALE: Final[float] = 1.0
"""A band's beams are only ever scaled down: a pass's scale factor is at most this."""

_DIVISION_FLOOR: Final[float] = 1e-12
"""A floor under a pass's demand totals before they divide, so a satellite or a cell
nobody asks of does not divide by zero (its scale is then capped at the full scale)."""

_NONE_LEFT: Final[float] = 0.0
"""The least a satellite's beams, a cell's area or its people can have left; a commit's
subtraction can round a hair below it."""

_GRID_DIMENSIONS: Final[int] = 2
"""A population grid is a two-dimensional array: rows of latitude, columns of longitude."""

_NORTH_POLE_LATITUDE_DEG: Final[float] = 90.0
"""The latitude a global grid's first row starts at, degrees."""

_GLOBE_LATITUDE_SPAN_DEG: Final[float] = 180.0
"""The latitudes a global grid spans, degrees."""

_GLOBE_LONGITUDE_SPAN_DEG: Final[float] = 360.0
"""The longitudes a global grid spans, degrees."""

_HZ_PER_GHZ: Final[float] = 1e9
"""Hertz per gigahertz, for stating the carrier in the method text."""

# ===========================================================================
# The checks, the markers and the run's memory budget
# ===========================================================================

_BOUNDS_RELATIVE_TOLERANCE: Final[float] = 1e-9
"""The relative tolerance of the bounds check: L <= min(ceiling, supply) and ceiling <=
maximum use hold exactly in arithmetic, and only rounding may carry them past."""

_CAPACITY_PER_SATELLITE_RISE_TOLERANCE: Final[float] = 0.02
"""A design rule (the build's amendment A6, from its numerics review of this module, finding
M2): the most capacity per satellite may rise from one row to the next, relative to the
earlier row, before the check refuses the curve. The reason is snapshot noise: on the
shipped grid one snapshot's spread of L at the first row (342 satellites) measured 1.9
percent, about as much as capacity per satellite falls over the first interval, so a
tighter tolerance refused correct curves on some draws of the snapshot times. At 2 percent
a first row under-filled by 10 percent is still refused on every draw."""

_STALL_FLOOR_FROM_FLEET: Final[int] = 20_000
"""The realized fleet from which the stall floor applies (the saturation design's rule:
the converged allocation sits close to its bounds there, so a stall would show)."""

_SATURATION_ELASTICITY: Final[float] = 0.10
"""The saturation number's threshold (ADR 005): one more satellite adds less than this
share of an average satellite's capacity."""

_SUPPORTING_ELASTICITY: Final[float] = 0.25
"""The supporting marker's threshold (the saturation design's § 1.5), fragile to the
demand definition and labeled so."""

_MAXIMUM_USE_MARKER_SHARE: Final[float] = 0.90
"""The gradualness marker: the fleet at which L reaches this share of maximum use (the
saturation design's § 1.5)."""

_MEMORY_BUDGET_MB: Final[float] = 16_000.0
"""The run's memory budget, MB: half the shared machine's 32 GB, across the parent and
every worker alive at once (the strategy's budget, SR-21; decimal megabytes, so the budget
holds under either reading of a gigabyte)."""

_BYTES_PER_MB: Final[int] = 1_000_000
"""Bytes per megabyte (decimal), the unit every memory figure here is stated in."""

_RU_MAXRSS_UNIT_BYTES_MACOS: Final[int] = 1
"""macOS reports ``ru_maxrss`` in bytes."""

_RU_MAXRSS_UNIT_BYTES_OTHER: Final[int] = 1024
"""Linux and the other Unix systems report ``ru_maxrss`` in kibibytes."""

_MIN_WORKERS: Final[int] = 1
"""The fewest workers a sweep runs with, even when one worker's peak alone exceeds the
budget (the bound then exceeds it too, and the run says so)."""

# ===========================================================================
# The grid's provenance and the curve's stated limits
# ===========================================================================

_GRID_CITATIONS: Final[tuple[str, ...]] = (
    "Schiavina, Freire, Carioli, MacManus (2023), GHS-POP R2023A, "
    "doi:10.2905/2FF68A52-5B5B-4A22-8F40-C41DA8332CFE",
    "Pesaresi et al. (2024), Advances on the Global Human Settlement Layer by joint "
    "assessment of Earth Observation and population survey data, International Journal of "
    "Digital Earth 17(1), doi:10.1080/17538947.2024.2390454",
)
"""The shipped grid's two citations: the dataset and the release's reference paper
(``communications/data/ATTRIBUTION.md``)."""

_GRID_LICENCE: Final[str] = "CC BY 4.0"
"""The shipped grid's licence, the source's (``communications/data/ATTRIBUTION.md``)."""

_GRID_MEMBERS: Final[tuple[str, ...]] = (
    "population",
    "lat_top_deg",
    "lon_left_deg",
    "cell_deg",
    "source",
    "citation",
)
"""The members a population grid archive holds (``communications/data/ATTRIBUTION.md``)."""


class PopulationGridError(ValueError):
    """A population grid the curve cannot use: not the one expected, or not a global grid."""


class SaturationInvariantError(ValueError):
    """A curve breaks one of its invariants or its markers cannot be placed on its rows."""


@dataclass(frozen=True, eq=False)
class PopulationGrid:
    """A population grid: residents per cell of a regular latitude-longitude grid.

    Attributes:
        population: Residents per cell, float32; rows run south from ``lat_top_deg`` and
            columns east from ``lon_left_deg``.
        lat_top_deg: The grid's northern edge, degrees.
        lon_left_deg: Its western edge, degrees.
        cell_deg: The cell's side, degrees.
        source: The source dataset and the change made, as the file states them.
        citation: The dataset citation the file carries.
        file_name: The file's name.
        sha256: The file's SHA-256, lowercase hex.
    """

    population: npt.NDArray[np.float32]
    lat_top_deg: float
    lon_left_deg: float
    cell_deg: float
    source: str
    citation: str
    file_name: str
    sha256: str


def load_population_grid(path: Path, expected_sha256: str) -> PopulationGrid:
    """Load a population grid archive, refusing one that is not the grid expected.

    The archive is read once, its SHA-256 checked, then parsed from those bytes with
    ``allow_pickle=False``.

    Args:
        path: The archive (an ``.npz`` holding the members ATTRIBUTION.md lists).
        expected_sha256: The SHA-256 the archive must have, lowercase hex.

    Returns:
        The grid.

    Raises:
        ModelFileError: If the file is missing, unreadable, or not a population grid
            archive (a member missing or of the wrong shape).
        PopulationGridError: If the file's SHA-256 is not ``expected_sha256``.
    """
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise ModelFileError(
            path, f"could not read the population grid ({exc.strerror or exc})"
        ) from exc
    digest = hashlib.sha256(data).hexdigest()
    if digest != expected_sha256:
        raise PopulationGridError(
            f"{path}: the population grid's SHA-256 is {digest}, but {expected_sha256} is expected"
        )
    try:
        loaded = np.load(io.BytesIO(data), allow_pickle=False)
        if not isinstance(loaded, np.lib.npyio.NpzFile):
            raise ModelFileError(path, "not an .npz archive of named arrays")
        with loaded as archive:
            missing = [member for member in _GRID_MEMBERS if member not in archive.files]
            if missing:
                raise ModelFileError(path, f"the population grid lacks {missing}")
            population = np.asarray(archive["population"])
            lat_top_deg = float(archive["lat_top_deg"])
            lon_left_deg = float(archive["lon_left_deg"])
            cell_deg = float(archive["cell_deg"])
            source = str(archive["source"])
            citation = str(archive["citation"])
    except (OSError, ValueError, TypeError, EOFError, zipfile.BadZipFile) as exc:
        raise ModelFileError(path, f"not a readable population grid ({exc})") from exc
    if population.ndim != _GRID_DIMENSIONS or population.dtype != np.float32:
        raise ModelFileError(
            path,
            "the population member must be a two-dimensional float32 array; got "
            f"{population.ndim} dimensions of {population.dtype}",
        )
    logger.debug("loaded the population grid %s (%s)", path.name, digest)
    return PopulationGrid(
        population=population,
        lat_top_deg=lat_top_deg,
        lon_left_deg=lon_left_deg,
        cell_deg=cell_deg,
        source=source,
        citation=citation,
        file_name=path.name,
        sha256=digest,
    )


# ===========================================================================
# 1. Demand cells, the beam and the shell
# ===========================================================================


@dataclass(frozen=True, eq=False)
class _DemandCells:
    """The demand cells of one grid at one density threshold.

    Attributes:
        lat_top_deg: The grid's northern edge, degrees.
        lon_left_deg: Its western edge, degrees.
        cell_deg: Its cell's side, degrees.
        index: Each grid cell's demand-cell index, :data:`_NOT_DEMAND` where it is not
            demand.
        lat_rad: The demand cells' centre latitudes.
        lon_rad: Their centre longitudes.
        xyz: Their centres' unit vectors.
        area_km2: Their areas on the sphere.
        people: Their residents.
    """

    lat_top_deg: float
    lon_left_deg: float
    cell_deg: float
    index: npt.NDArray[np.int64]
    lat_rad: npt.NDArray[np.float64]
    lon_rad: npt.NDArray[np.float64]
    xyz: npt.NDArray[np.float64]
    area_km2: npt.NDArray[np.float64]
    people: npt.NDArray[np.float64]

    @property
    def count(self) -> int:
        """The number of demand cells."""
        return int(self.area_km2.size)


def _unit_vectors(
    lat_rad: npt.NDArray[np.float64], lon_rad: npt.NDArray[np.float64]
) -> npt.NDArray[np.float64]:
    """Return the Earth-centred unit vectors of points given by latitude and longitude."""
    cos_lat = np.cos(lat_rad)
    return np.stack([cos_lat * np.cos(lon_rad), cos_lat * np.sin(lon_rad), np.sin(lat_rad)], axis=1)


def _check_global(population: PopulationGrid) -> None:
    """Refuse a grid that does not cover the globe from the north pole.

    The pair search wraps columns around the globe and clips rows at the poles, so it needs
    every longitude and every latitude.

    Raises:
        PopulationGridError: If the grid is not two-dimensional or does not span 180
            degrees of latitude from 90 north and 360 degrees of longitude.
    """
    if population.population.ndim != _GRID_DIMENSIONS:
        raise PopulationGridError(
            f"{population.file_name}: the population grid must be two-dimensional; got "
            f"{population.population.ndim} dimensions"
        )
    n_lat, n_lon = population.population.shape
    global_grid = (
        math.isclose(population.lat_top_deg, _NORTH_POLE_LATITUDE_DEG)
        and math.isclose(n_lat * population.cell_deg, _GLOBE_LATITUDE_SPAN_DEG)
        and math.isclose(n_lon * population.cell_deg, _GLOBE_LONGITUDE_SPAN_DEG)
    )
    if not global_grid:
        raise PopulationGridError(
            f"{population.file_name}: the curve needs a global grid from 90 degrees north; "
            f"got {n_lat} x {n_lon} cells of {population.cell_deg} degrees from "
            f"{population.lat_top_deg} degrees"
        )


def _demand_cells(population: PopulationGrid, density_threshold_per_km2: float) -> _DemandCells:
    """Return the grid's demand cells: every cell with at least the threshold's density.

    Args:
        population: A global population grid.
        density_threshold_per_km2: A cell is demand at this many people per km^2 or more.

    Returns:
        The demand cells, in row-major order of the grid.

    Raises:
        PopulationGridError: If the grid is not global.
    """
    _check_global(population)
    people_grid = population.population.astype(np.float64)
    n_lat, n_lon = people_grid.shape
    cell_deg = population.cell_deg
    lat_edges = np.radians(population.lat_top_deg - np.arange(n_lat + 1) * cell_deg)
    row_area = _ZONE_AREA_PER_SINE_KM2 * np.abs(np.diff(np.sin(lat_edges))) / n_lon
    density = people_grid / row_area[:, None]
    rows, cols = np.nonzero(density >= density_threshold_per_km2)
    index = np.full(people_grid.shape, _NOT_DEMAND, dtype=np.int64)
    index[rows, cols] = np.arange(rows.size)
    lat_rad = np.radians(population.lat_top_deg - (rows + _CELL_CENTRE_FRACTION) * cell_deg)
    lon_rad = np.radians(population.lon_left_deg + (cols + _CELL_CENTRE_FRACTION) * cell_deg)
    return _DemandCells(
        lat_top_deg=population.lat_top_deg,
        lon_left_deg=population.lon_left_deg,
        cell_deg=cell_deg,
        index=index,
        lat_rad=lat_rad,
        lon_rad=lon_rad,
        xyz=_unit_vectors(lat_rad, lon_rad),
        area_km2=row_area[rows],
        people=people_grid[rows, cols],
    )


@dataclass(frozen=True, eq=False)
class _BeamModel:
    """The view's limit and the beam's footprint against the central angle.

    Attributes:
        max_central_angle_rad: The largest central angle at which a cell sees a satellite
            above the mask.
        central_angle_rad: The footprint table's central angles, overhead to the mask.
        footprint_km2: The footprint at each, km^2.
    """

    max_central_angle_rad: float
    central_angle_rad: npt.NDArray[np.float64]
    footprint_km2: npt.NDArray[np.float64]


def _central_angle_limit(shell: ShellInputs) -> float:
    """Return the largest central angle at which a satellite stands above the mask, radians."""
    mask_rad = math.radians(shell.elevation_mask_deg)
    orbit_radius_km = _EARTH_RADIUS_KM + shell.altitude_km
    return math.acos(_EARTH_RADIUS_KM * math.cos(mask_rad) / orbit_radius_km) - mask_rad


def _beam_model(shell: ShellInputs) -> _BeamModel:
    """Return the beam model: the view's limit and the footprint table.

    Seen from a point on the ground, a satellite at central angle g stands at height
    r cos(g) - R above the horizon plane and r sin(g) along it (R the Earth's radius, r the
    orbit's): its slant range and elevation follow, and the beam's scan angle off the
    satellite's nadir is 90 degrees less the elevation and g. A square aperture of side
    sqrt(area) forms a beam of half-power width beamwidth factor x wavelength / side; its
    footprint is an ellipse, slant range x width across, stretched along the scan by
    1 / (cos(scan) sin(elevation)).

    Args:
        shell: The shell and the beam.

    Returns:
        The beam model.
    """
    limit_rad = _central_angle_limit(shell)
    central_angle = np.linspace(_OVERHEAD_CENTRAL_ANGLE_RAD, limit_rad, _FOOTPRINT_TABLE_POINTS)
    orbit_radius_km = _EARTH_RADIUS_KM + shell.altitude_km
    height_km = orbit_radius_km * np.cos(central_angle) - _EARTH_RADIUS_KM
    offset_km = orbit_radius_km * np.sin(central_angle)
    slant_km = np.hypot(height_km, offset_km)
    elevation = np.arctan2(height_km, offset_km)
    cos_scan = np.sin(elevation + central_angle)
    wavelength_m = _SPEED_OF_LIGHT_M_S / shell.carrier_hz
    beamwidth_rad = shell.beamwidth_factor * wavelength_m / math.sqrt(shell.reference_aperture_m2)
    across_km = slant_km * beamwidth_rad
    along_km = across_km / (cos_scan * np.sin(elevation))
    return _BeamModel(
        max_central_angle_rad=limit_rad,
        central_angle_rad=central_angle,
        footprint_km2=_ELLIPSE_AREA_FACTOR * across_km * along_km,
    )


def _beams_per_satellite(shell: ShellInputs) -> float:
    """Return B: the calibration in effective reuses (x 1000), scaled to the curve's panel.

    The calibration's 0.15 Gbps per (MHz x bps/Hz) is 150 effective full-band reuses at
    :data:`~communications.constants.APERTURE_REFERENCE_M2`, linear in the panel's area.
    """
    return (
        GBPS_TO_MBPS
        * shell.reuse_calibration_gbps_per_mhz_per_se
        * shell.reference_aperture_m2
        / APERTURE_REFERENCE_M2
    )


def _people_per_beam(spectrum_mhz: float, class_inputs: ClassInputs) -> float:
    """Return the people one beam serves at d = 1.

    A beam's rate is the spectrum times the class's central SE (MHz x bps/Hz = Mbps); each
    person's busy-hour load is the class's rate while active times its busy-hour share.

    Args:
        spectrum_mhz: The held spectrum, MHz.
        class_inputs: The class.

    Returns:
        People per beam.
    """
    beam_rate_mbps = spectrum_mhz * class_inputs.spectral_efficiency_bps_per_hz
    load_per_person_mbps = class_inputs.active_rate_mbps * class_inputs.concurrency_peak
    return beam_rate_mbps / load_per_person_mbps


@dataclass(frozen=True, eq=False)
class _SatellitePositions:
    """The sub-satellite points of one snapshot.

    Attributes:
        lat_rad: Each satellite's sub-satellite latitude.
        lon_rad: Its longitude, in [-pi, pi).
    """

    lat_rad: npt.NDArray[np.float64]
    lon_rad: npt.NDArray[np.float64]

    @property
    def count(self) -> int:
        """The number of satellites."""
        return int(self.lat_rad.size)


def _walker_positions(
    shell: ShellInputs, requested_fleet: int, time_s: float
) -> _SatellitePositions:
    """Return the sub-satellite points of a Walker Delta shell at one time.

    Circular two-body orbits: plane p's ascending node at 360 x p / P degrees, slot s's
    argument of latitude 360 x (s / S + F x p / (P x S)) degrees at time 0, advancing at the
    mean motion; the Earth turns under them at the sidereal rate.

    Args:
        shell: The shell.
        requested_fleet: The requested fleet N.
        time_s: The snapshot time, s.

    Returns:
        The P x S sub-satellite points.
    """
    planes, per_plane = _walker_shape(requested_fleet)
    total = planes * per_plane
    orbit_radius_km = _EARTH_RADIUS_KM + shell.altitude_km
    period_s = math.tau * math.sqrt(orbit_radius_km**_KEPLER_THIRD_LAW_POWER / _MU_EARTH_KM3_S2)
    mean_motion = math.tau / period_s
    earth_rate = math.tau / _SIDEREAL_DAY_S
    inclination = math.radians(shell.inclination_deg)
    plane = np.repeat(np.arange(planes), per_plane)
    slot = np.tile(np.arange(per_plane), planes)
    ascending_node = math.tau * plane / planes
    argument = (
        math.tau * slot / per_plane
        + math.tau * _WALKER_PHASING * plane / total
        + mean_motion * time_s
    )
    lat_rad = np.arcsin(math.sin(inclination) * np.sin(argument))
    lon_rad = (
        ascending_node
        + np.arctan2(math.cos(inclination) * np.sin(argument), np.cos(argument))
        - earth_rate * time_s
    )
    lon_rad = (lon_rad + math.pi) % math.tau - math.pi
    return _SatellitePositions(lat_rad=lat_rad, lon_rad=lon_rad)


# ===========================================================================
# 2. The allocation (the seam) and its bounds
# ===========================================================================


@dataclass(frozen=True, eq=False)
class _Pairs:
    """Every satellite-cell pair in view, ordered by satellite, then cell.

    Attributes:
        satellite: Each pair's satellite index.
        cell: Its demand-cell index.
        central_angle_rad: The central angle between them.
    """

    satellite: npt.NDArray[np.int64]
    cell: npt.NDArray[np.int64]
    central_angle_rad: npt.NDArray[np.float64]


def _pairs_in_view(
    satellites: _SatellitePositions, cells: _DemandCells, max_central_angle_rad: float
) -> _Pairs:
    """Return every pair whose cell centre sees its satellite above the mask.

    Each satellite searches a window of grid cells around the cell under it, wide enough to
    hold its whole view at the window's poleward edge, and keeps the demand cells within
    the central-angle limit. A window can reach a cell twice (rows clipped at a pole, or
    columns wrapped past the antimeridian), so each pair is kept once.

    Args:
        satellites: The satellites.
        cells: The demand cells.
        max_central_angle_rad: The view's central-angle limit.

    Returns:
        The pairs, ordered by satellite, then cell.
    """
    n_lat, n_lon = cells.index.shape
    cell_deg = cells.cell_deg
    limit_deg = math.degrees(max_central_angle_rad)
    half_rows = math.ceil(limit_deg / cell_deg) + _WINDOW_MARGIN_CELLS
    row_offsets = np.arange(-half_rows, half_rows + 1)
    cos_limit = math.cos(max_central_angle_rad)
    window_cap_rad = math.radians(_WINDOW_LATITUDE_CAP_DEG)
    satellite_xyz = _unit_vectors(satellites.lat_rad, satellites.lon_rad)
    found_satellite: list[npt.NDArray[np.int64]] = [np.empty(0, dtype=np.int64)]
    found_cell: list[npt.NDArray[np.int64]] = [np.empty(0, dtype=np.int64)]
    found_angle: list[npt.NDArray[np.float64]] = [np.empty(0, dtype=np.float64)]
    for start in range(0, satellites.count, _PAIR_SEARCH_CHUNK_SATELLITES):
        lat = satellites.lat_rad[start : start + _PAIR_SEARCH_CHUNK_SATELLITES]
        lon = satellites.lon_rad[start : start + _PAIR_SEARCH_CHUNK_SATELLITES]
        centre_row = np.floor((cells.lat_top_deg - np.degrees(lat)) / cell_deg).astype(np.int64)
        centre_col = np.floor((np.degrees(lon) - cells.lon_left_deg) / cell_deg).astype(np.int64)
        edge_lat = np.minimum(np.abs(lat) + max_central_angle_rad, window_cap_rad)
        half_cols_each = np.ceil(limit_deg / np.cos(edge_lat) / cell_deg).astype(np.int64)
        half_cols = int(half_cols_each.max()) + _WINDOW_MARGIN_CELLS
        col_offsets = np.arange(-half_cols, half_cols + 1)
        rows = np.clip(centre_row[:, None, None] + row_offsets[None, :, None], 0, n_lat - 1)
        cols = (centre_col[:, None, None] + col_offsets[None, None, :]) % n_lon
        cell = cells.index[rows, cols]
        satellite = np.broadcast_to(np.arange(start, start + lat.size)[:, None, None], cell.shape)
        demand = cell != _NOT_DEMAND
        cell, satellite = cell[demand], satellite[demand]
        cos_angle = np.einsum("ij,ij->i", cells.xyz[cell], satellite_xyz[satellite])
        visible = cos_angle >= cos_limit
        found_satellite.append(satellite[visible])
        found_cell.append(cell[visible])
        found_angle.append(np.arccos(np.clip(cos_angle[visible], *_COSINE_BOUNDS)))
    satellite_all = np.concatenate(found_satellite)
    cell_all = np.concatenate(found_cell)
    angle_all = np.concatenate(found_angle)
    key = satellite_all * (cells.count + 1) + cell_all
    _, first = np.unique(key, return_index=True)
    return _Pairs(
        satellite=satellite_all[first], cell=cell_all[first], central_angle_rad=angle_all[first]
    )


@dataclass(frozen=True, eq=False)
class _AllocationLimits:
    """What limits one class's allocation besides the cells' own areas.

    Attributes:
        beams_per_satellite: B, the beams each satellite can light.
        people_per_beam: The people one beam serves at d = 1.
        take_up: The share of a cell's residents counted as potential users.
        beam: The view's limit and the footprint table.
        footprint_bands: The fill's geometric footprint bands.
        passes: The proportional passes inside each band.
    """

    beams_per_satellite: float
    people_per_beam: float
    take_up: float
    beam: _BeamModel
    footprint_bands: int
    passes: int


@dataclass(frozen=True, eq=False)
class _Allocation:
    """One snapshot's allocation (d = 1), pair by pair, with its two bounds.

    Attributes:
        satellite: Each pair's satellite index (the pairs in view, by satellite then cell).
        cell: Each pair's demand-cell index.
        footprint_km2: Each pair's footprint.
        beams: The beams each pair placed.
        useful_beams: L, the beams placed in all.
        ceiling_beams: The most the cells in view could use: each served by its smallest
            footprint in view, one layer, capped by its people.
        supply_beams: The most the satellites could place: each satellite's B, capped by
            what its cells could take one layer at a time.
    """

    satellite: npt.NDArray[np.int64]
    cell: npt.NDArray[np.int64]
    footprint_km2: npt.NDArray[np.float64]
    beams: npt.NDArray[np.float64]
    useful_beams: float
    ceiling_beams: float
    supply_beams: float


def _fill_smallest_footprint_first(
    n_satellites: int,
    pairs: _Pairs,
    footprint_km2: npt.NDArray[np.float64],
    cells: _DemandCells,
    people_cap: npt.NDArray[np.float64],
    limits: _AllocationLimits,
) -> tuple[npt.NDArray[np.float64], float]:
    """Fill one snapshot's pairs smallest footprint first; return each pair's beams and L.

    Band by band from the smallest footprints, each pair asks for min(one layer, the cell's
    area left / its footprint); the passes scale the band by every satellite's beams left,
    then by every cell's area and people left (each scale at most 1); the band is committed
    and the next sees only what remains. L is summed band by band.
    """
    beams = np.zeros(footprint_km2.size)
    if footprint_km2.size == 0:
        return beams, 0.0
    n_cells = cells.count
    satellite_left = np.full(n_satellites, limits.beams_per_satellite)
    area_left = cells.area_km2.copy()
    people_left = people_cap.copy()
    one_layer = cells.area_km2[pairs.cell] / footprint_km2
    edges = np.geomspace(
        footprint_km2.min() * _BAND_EDGE_LOW_FACTOR,
        footprint_km2.max() * _BAND_EDGE_HIGH_FACTOR,
        limits.footprint_bands + 1,
    )
    band = np.clip(
        np.searchsorted(edges, footprint_km2, side="right") - 1, 0, limits.footprint_bands - 1
    )
    order = np.argsort(band, kind="stable")
    starts = np.searchsorted(band[order], np.arange(limits.footprint_bands + 1))
    placed = 0.0
    for band_index in range(limits.footprint_bands):
        members = order[starts[band_index] : starts[band_index + 1]]
        if members.size == 0:
            continue
        satellite = pairs.satellite[members]
        cell = pairs.cell[members]
        footprint = footprint_km2[members]
        asked = np.minimum(one_layer[members], area_left[cell] / footprint)
        for _ in range(limits.passes):
            satellite_want = np.bincount(satellite, weights=asked, minlength=n_satellites)
            satellite_scale = np.minimum(
                _FULL_SCALE, satellite_left / np.maximum(satellite_want, _DIVISION_FLOOR)
            )
            asked = asked * satellite_scale[satellite]
            area_want = np.bincount(cell, weights=asked * footprint, minlength=n_cells)
            beam_want = np.bincount(cell, weights=asked, minlength=n_cells)
            cell_scale = np.minimum(
                _FULL_SCALE,
                np.minimum(
                    area_left / np.maximum(area_want, _DIVISION_FLOOR),
                    people_left / np.maximum(beam_want, _DIVISION_FLOOR),
                ),
            )
            asked = asked * cell_scale[cell]
        satellite_left -= np.bincount(satellite, weights=asked, minlength=n_satellites)
        area_left -= np.bincount(cell, weights=asked * footprint, minlength=n_cells)
        people_left -= np.bincount(cell, weights=asked, minlength=n_cells)
        np.maximum(satellite_left, _NONE_LEFT, out=satellite_left)
        np.maximum(area_left, _NONE_LEFT, out=area_left)
        np.maximum(people_left, _NONE_LEFT, out=people_left)
        beams[members] = asked
        placed += float(asked.sum())
    return beams, placed


def _ceiling(
    pairs: _Pairs,
    footprint_km2: npt.NDArray[np.float64],
    cells: _DemandCells,
    people_cap: npt.NDArray[np.float64],
) -> float:
    """Return the ceiling: each cell in view served by its smallest footprint in view.

    One layer for the phone class, capped by the cell's people.
    """
    best = np.full(cells.count, np.inf)
    np.minimum.at(best, pairs.cell, footprint_km2)
    seen = np.bincount(pairs.cell, minlength=cells.count) > 0
    return float(np.minimum(cells.area_km2[seen] / best[seen], people_cap[seen]).sum())


def _supply(
    n_satellites: int,
    pairs: _Pairs,
    footprint_km2: npt.NDArray[np.float64],
    cells: _DemandCells,
    people_cap: npt.NDArray[np.float64],
    beams_per_satellite: float,
) -> float:
    """Return the supply: each satellite's B, capped by what its cells could take.

    A satellite's reach is the sum over its pairs of min(one layer, the cell's people cap).
    """
    reach = np.bincount(
        pairs.satellite,
        weights=np.minimum(cells.area_km2[pairs.cell] / footprint_km2, people_cap[pairs.cell]),
        minlength=n_satellites,
    )
    return float(np.minimum(reach, beams_per_satellite).sum())


def _people_cap(cells: _DemandCells, limits: _AllocationLimits) -> npt.NDArray[np.float64]:
    """Return each cell's people cap in beams: people x take-up / people per beam."""
    return cells.people * limits.take_up / limits.people_per_beam


def _allocate(
    satellites: _SatellitePositions, cells: _DemandCells, limits: _AllocationLimits
) -> _Allocation:
    """Allocate one snapshot's beams, smallest footprint first, and compute its bounds.

    The private seam: it takes explicit satellite positions, so a test can place a
    satellite where it chooses.

    Args:
        satellites: The satellites' sub-satellite points.
        cells: The demand cells.
        limits: B, the people per beam and take-up, the beam model, the bands and passes.

    Returns:
        The allocation, pair by pair, with L, the ceiling and the supply.
    """
    pairs = _pairs_in_view(satellites, cells, limits.beam.max_central_angle_rad)
    footprint_km2 = np.interp(
        pairs.central_angle_rad, limits.beam.central_angle_rad, limits.beam.footprint_km2
    )
    people_cap = _people_cap(cells, limits)
    beams, useful_beams = _fill_smallest_footprint_first(
        satellites.count, pairs, footprint_km2, cells, people_cap, limits
    )
    return _Allocation(
        satellite=pairs.satellite,
        cell=pairs.cell,
        footprint_km2=footprint_km2,
        beams=beams,
        useful_beams=useful_beams,
        ceiling_beams=_ceiling(pairs, footprint_km2, cells, people_cap),
        supply_beams=_supply(
            satellites.count, pairs, footprint_km2, cells, people_cap, limits.beams_per_satellite
        ),
    )


def _maximum_use(cells: _DemandCells, limits: _AllocationLimits, inclination_deg: float) -> float:
    """Return maximum use: every cell served by the best satellite the shell can offer it.

    A shell of inclination i never flies above latitude i, so the best a cell at latitude
    lat can see is a satellite at central angle max(0, |lat| - i); a cell beyond the view's
    limit from there adds nothing. One layer, capped by the cell's people. It does not
    depend on the fleet.
    """
    best_angle = np.maximum(
        _OVERHEAD_CENTRAL_ANGLE_RAD, np.abs(cells.lat_rad) - math.radians(inclination_deg)
    )
    reachable = best_angle <= limits.beam.max_central_angle_rad
    best_footprint = np.interp(
        best_angle[reachable], limits.beam.central_angle_rad, limits.beam.footprint_km2
    )
    people_cap = _people_cap(cells, limits)[reachable]
    return float(np.minimum(cells.area_km2[reachable] / best_footprint, people_cap).sum())


# ===========================================================================
# 3. The sweep, in separate processes under the memory budget
# ===========================================================================


@dataclass(frozen=True)
class _SnapshotTask:
    """One fleet at one snapshot time.

    Attributes:
        fleet_index: The fleet's position in the sweep.
        requested_fleet: The requested fleet N.
        snapshot_index: The snapshot's position in the draw.
        time_s: The snapshot time, s.
    """

    fleet_index: int
    requested_fleet: int
    snapshot_index: int
    time_s: float


@dataclass(frozen=True, eq=False)
class _SweepContext:
    """What every snapshot task needs: the shell, the demand cells and the class's limits."""

    shell: ShellInputs
    cells: _DemandCells
    limits: _AllocationLimits


@dataclass(frozen=True)
class _SnapshotResult:
    """One snapshot task's result, with the measure of the worker that ran it.

    Attributes:
        task: The task.
        realized_fleet: The realized fleet, P x S.
        useful_beams: L.
        ceiling_beams: The ceiling.
        supply_beams: The supply.
        worker_pid: The worker's process id.
        worker_peak_mb: The worker's peak resident memory so far, MB.
    """

    task: _SnapshotTask
    realized_fleet: int
    useful_beams: float
    ceiling_beams: float
    supply_beams: float
    worker_pid: int
    worker_peak_mb: float


def _own_peak_mb() -> float:
    """Return this process's peak resident memory so far, MB (``ru_maxrss``, by platform)."""
    unit_bytes = (
        _RU_MAXRSS_UNIT_BYTES_MACOS if sys.platform == "darwin" else _RU_MAXRSS_UNIT_BYTES_OTHER
    )
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * unit_bytes / _BYTES_PER_MB


def _run_snapshot(task: _SnapshotTask, context: _SweepContext) -> _SnapshotResult:
    """Run one fleet at one snapshot time (a worker's task)."""
    satellites = _walker_positions(context.shell, task.requested_fleet, task.time_s)
    allocation = _allocate(satellites, context.cells, context.limits)
    return _SnapshotResult(
        task=task,
        realized_fleet=satellites.count,
        useful_beams=allocation.useful_beams,
        ceiling_beams=allocation.ceiling_beams,
        supply_beams=allocation.supply_beams,
        worker_pid=os.getpid(),
        worker_peak_mb=_own_peak_mb(),
    )


@dataclass(frozen=True)
class _SweepRun:
    """A sweep's results with what its workers measured.

    Attributes:
        results: Every task's result, in the tasks' order.
        workers: The workers that ran at once after the first task.
        workers_peak_mb: The summed peaks of the largest set of workers alive at once, MB.
    """

    results: tuple[_SnapshotResult, ...]
    workers: int
    workers_peak_mb: float


def _worker_count(task_peak_mb: float, remaining_tasks: int) -> int:
    """Return how many workers may run at once: the budget over one worker's peak.

    At most one per CPU and one per remaining task, and at least one.
    """
    affordable = math.floor((_MEMORY_BUDGET_MB - _own_peak_mb()) / task_peak_mb)
    cpus = os.process_cpu_count() or _MIN_WORKERS
    return max(_MIN_WORKERS, min(affordable, cpus, remaining_tasks))


def _run_sweep(tasks: Sequence[_SnapshotTask], context: _SweepContext) -> _SweepRun:
    """Run every task in separate processes, the largest fleet's first task alone.

    The largest fleet's first snapshot runs first, alone, and its worker's peak sets how
    many workers then run at once under the budget. Each worker reports its own peak (a
    process's peak only grows, so its last report is its peak); the workers of the second
    pool are alive at once, so their peaks sum.

    Raises:
        BrokenProcessPool: If a worker dies (logged with the task count before it rises).
    """
    order = sorted(range(len(tasks)), key=lambda i: (-tasks[i].requested_fleet, i))
    spawn = get_context("spawn")
    results: dict[int, _SnapshotResult] = {}
    try:
        with ProcessPoolExecutor(max_workers=_MIN_WORKERS, mp_context=spawn) as first_pool:
            first = first_pool.submit(_run_snapshot, tasks[order[0]], context).result()
        results[order[0]] = first
        rest = order[1:]
        workers = _worker_count(first.worker_peak_mb, len(rest)) if rest else _MIN_WORKERS
        worker_peaks: dict[int, float] = {}
        if rest:
            with ProcessPoolExecutor(max_workers=workers, mp_context=spawn) as pool:
                for index, result in zip(
                    rest,
                    pool.map(_run_snapshot, [tasks[i] for i in rest], repeat(context)),
                    strict=True,
                ):
                    results[index] = result
                    worker_peaks[result.worker_pid] = max(
                        worker_peaks.get(result.worker_pid, result.worker_peak_mb),
                        result.worker_peak_mb,
                    )
    except BrokenProcessPool:
        logger.error("a saturation worker died during a sweep of %d snapshot tasks", len(tasks))
        raise
    return _SweepRun(
        results=tuple(results[i] for i in range(len(tasks))),
        workers=workers,
        workers_peak_mb=max(first.worker_peak_mb, sum(worker_peaks.values())),
    )


# ===========================================================================
# 4. The rows, the checks and the markers
# ===========================================================================


@dataclass(frozen=True)
class _FleetSnapshots:
    """One fleet's snapshots, in the draw's order.

    Attributes:
        fleet: The realized fleet, P x S.
        useful_beams: L at each snapshot.
        ceiling_beams: The ceiling at each.
        supply_beams: The supply at each.
    """

    fleet: int
    useful_beams: tuple[float, ...]
    ceiling_beams: tuple[float, ...]
    supply_beams: tuple[float, ...]


def _by_fleet(results: Sequence[_SnapshotResult], n_fleets: int) -> tuple[_FleetSnapshots, ...]:
    """Group the snapshot results by fleet, each fleet's snapshots in the draw's order."""
    grouped: list[list[_SnapshotResult]] = [[] for _ in range(n_fleets)]
    for result in results:
        grouped[result.task.fleet_index].append(result)
    fleets = []
    for snapshots in grouped:
        snapshots.sort(key=lambda result: result.task.snapshot_index)
        fleets.append(
            _FleetSnapshots(
                fleet=snapshots[0].realized_fleet,
                useful_beams=tuple(result.useful_beams for result in snapshots),
                ceiling_beams=tuple(result.ceiling_beams for result in snapshots),
                supply_beams=tuple(result.supply_beams for result in snapshots),
            )
        )
    return tuple(fleets)


def _exceeds(value: float, bound: float, relative_tolerance: float) -> bool:
    """Return whether ``value`` lies above ``bound`` by more than the relative tolerance."""
    return value > bound and not math.isclose(value, bound, rel_tol=relative_tolerance)


def _check_bounds(
    device_class: DeviceClass, fleets: Sequence[_FleetSnapshots], maximum_use: float
) -> None:
    """Refuse a snapshot whose L exceeds min(ceiling, supply) or whose ceiling exceeds maximum use.

    Raises:
        SaturationInvariantError: Naming the class, the fleet, the snapshot and the values.
    """
    for fleet in fleets:
        for snapshot, (useful, ceiling, supply) in enumerate(
            zip(fleet.useful_beams, fleet.ceiling_beams, fleet.supply_beams, strict=True)
        ):
            if _exceeds(useful, min(ceiling, supply), _BOUNDS_RELATIVE_TOLERANCE):
                raise SaturationInvariantError(
                    f"{device_class.value} at {fleet.fleet} satellites, snapshot {snapshot}: "
                    f"useful beams {useful} exceed min(ceiling {ceiling}, supply {supply})"
                )
            if _exceeds(ceiling, maximum_use, _BOUNDS_RELATIVE_TOLERANCE):
                raise SaturationInvariantError(
                    f"{device_class.value} at {fleet.fleet} satellites, snapshot {snapshot}: "
                    f"the ceiling {ceiling} exceeds maximum use {maximum_use}"
                )


def _check_stall_floor(fleets: Sequence[_FleetSnapshots], stall_floor: float) -> None:
    """Refuse the phone class's curve if its allocation stalls at the large fleets.

    From :data:`_STALL_FLOOR_FROM_FLEET` satellites up, L must reach ``stall_floor`` x
    min(ceiling, supply) at every snapshot and in the snapshot means.

    Raises:
        SaturationInvariantError: Naming the fleet, the snapshot (or the means) and the share.
    """
    for fleet in fleets:
        if fleet.fleet < _STALL_FLOOR_FROM_FLEET:
            continue
        readings = [
            (f"snapshot {snapshot}", useful, min(ceiling, supply))
            for snapshot, (useful, ceiling, supply) in enumerate(
                zip(fleet.useful_beams, fleet.ceiling_beams, fleet.supply_beams, strict=True)
            )
        ]
        readings.append(
            (
                "the snapshot means",
                float(np.mean(fleet.useful_beams)),
                min(float(np.mean(fleet.ceiling_beams)), float(np.mean(fleet.supply_beams))),
            )
        )
        for where, useful, bound in readings:
            if useful < stall_floor * bound:
                raise SaturationInvariantError(
                    f"{DeviceClass.PHONE_CLASS.value} at {fleet.fleet} satellites, {where}: "
                    f"useful beams {useful} are {useful / bound:.4f} of min(ceiling, supply) "
                    f"{bound}, under the stall floor {stall_floor}"
                )


def _phone_rows(
    fleets: Sequence[_FleetSnapshots],
    requested_fleets: Sequence[int],
    *,
    spectrum_mhz: float,
    spectral_efficiency_bps_per_hz: float,
    beams_per_satellite: float,
) -> tuple[CurveRow, ...]:
    """Return the phone class's rows: the snapshot means, the spread of L, U and the bounds.

    Each row carries the request its shell was built from (the sweep's fleet, in the order
    the tasks were made), so a reader can rebuild it. A phone beam carries the spectrum times
    the class's central SE, so a snapshot's capacity is L times that (Gbps).
    """
    rows = []
    for fleet, requested_fleet in zip(fleets, requested_fleets, strict=True):
        useful = np.array(fleet.useful_beams)
        capacity_gbps = useful * spectrum_mhz * spectral_efficiency_bps_per_hz / GBPS_TO_MBPS
        useful_mean = float(np.mean(useful))
        rows.append(
            CurveRow(
                fleet=fleet.fleet,
                requested_fleet=requested_fleet,
                useful_beams=useful_mean,
                useful_beams_spread=float(np.std(useful)),
                capacity_gbps=float(np.mean(capacity_gbps)),
                ocean_factor=useful_mean / (fleet.fleet * beams_per_satellite),
                ceiling_beams=float(np.mean(fleet.ceiling_beams)),
                supply_beams=float(np.mean(fleet.supply_beams)),
                directional=None,
                trim=None,
            )
        )
    return tuple(rows)


def _check_capacity_per_satellite(device_class: DeviceClass, rows: Sequence[CurveRow]) -> None:
    """Refuse a curve whose capacity per satellite rises between consecutive rows.

    A rise of up to :data:`_CAPACITY_PER_SATELLITE_RISE_TOLERANCE` of the earlier row's value
    is the snapshots' noise and passes; a larger one means an allocation that under-fills a
    row (which the stall floor, from 20,000 satellites up, cannot see).

    Raises:
        SaturationInvariantError: Naming the class, the two fleets and the two values.
    """
    for earlier, later in pairwise(rows):
        before = earlier.capacity_gbps / earlier.fleet
        after = later.capacity_gbps / later.fleet
        if after - before > _CAPACITY_PER_SATELLITE_RISE_TOLERANCE * before:
            raise SaturationInvariantError(
                f"{device_class.value}: capacity per satellite rises from {before} Gbps at "
                f"{earlier.fleet} satellites to {after} Gbps at {later.fleet}, more than "
                f"{_CAPACITY_PER_SATELLITE_RISE_TOLERANCE:g} relative"
            )


def _first_crossing_under(
    midpoints: Sequence[float], elasticity: Sequence[float], threshold: float, what: str
) -> float | None:
    """Return the fleet where the elasticity first falls under the threshold, or None.

    The crossing is interpolated in ln N between the two midpoints that straddle it.

    Raises:
        SaturationInvariantError: If the elasticity is already under the threshold at the
            first midpoint, so the crossing lies before the rows can place it.
    """
    for i, value in enumerate(elasticity):
        if value < threshold:
            if i == 0:
                raise SaturationInvariantError(
                    f"{what}: the elasticity is already {value:.4f}, under {threshold}, at the "
                    f"first midpoint ({midpoints[0]:.0f} satellites), so the crossing lies "
                    "before the curve's rows can place it; the sweep must start lower"
                )
            share = (elasticity[i - 1] - threshold) / (elasticity[i - 1] - value)
            low, high = math.log(midpoints[i - 1]), math.log(midpoints[i])
            return math.exp(low + share * (high - low))
    return None


def _fleet_reaching(
    fleets: Sequence[int], useful_beams: Sequence[float], target: float, what: str
) -> float | None:
    """Return the fleet at which L first reaches the target (log-log between rows), or None.

    Raises:
        SaturationInvariantError: If the first row already reaches the target, so the fleet
            lies at or below the curve's first row.
    """
    if useful_beams[0] >= target:
        raise SaturationInvariantError(
            f"{what}: L is already {useful_beams[0]} at the first row ({fleets[0]} satellites), "
            f"at or above the target {target}; the sweep must start lower"
        )
    for (low_fleet, low_beams), (high_fleet, high_beams) in pairwise(
        zip(fleets, useful_beams, strict=True)
    ):
        if low_beams < target <= high_beams:
            share = math.log(target / low_beams) / math.log(high_beams / low_beams)
            return math.exp(math.log(low_fleet) + share * math.log(high_fleet / low_fleet))
    return None


def _markers(
    device_class: DeviceClass, rows: Sequence[CurveRow], maximum_use: float
) -> ClassMarkers:
    """Return a curve's markers, read on its rows against maximum use.

    The elasticity of capacity, ln(C_i+1 / C_i) / ln(N_i+1 / N_i), sits at each interval's
    geometric midpoint. The saturation number is the first crossing under 0.10 rounded half
    up, or, when not reached, the last row's fleet as ``saturation_not_reached_by``; beside it
    the first crossing under 0.25 and the fleet at which L reaches 90 percent of maximum use.

    Raises:
        SaturationInvariantError: If a row's capacity is not positive (the elasticity needs
            its logarithm), or a marker lies before the rows can place it.
    """
    fleets = [row.fleet for row in rows]
    capacity = [row.capacity_gbps for row in rows]
    if min(capacity) <= 0:
        raise SaturationInvariantError(
            f"{device_class.value}: capacity must be positive at every row to read the "
            f"elasticity; got {capacity}"
        )
    midpoints = [math.sqrt(low * high) for low, high in pairwise(fleets)]
    elasticity = [
        math.log(high_capacity / low_capacity) / math.log(high_fleet / low_fleet)
        for (low_fleet, low_capacity), (high_fleet, high_capacity) in pairwise(
            zip(fleets, capacity, strict=True)
        )
    ]
    name = device_class.value
    saturation = _first_crossing_under(
        midpoints, elasticity, _SATURATION_ELASTICITY, f"{name}, the saturation number"
    )
    supporting = _first_crossing_under(
        midpoints, elasticity, _SUPPORTING_ELASTICITY, f"{name}, the crossing under 0.25"
    )
    ninety = _fleet_reaching(
        fleets,
        [row.useful_beams for row in rows],
        _MAXIMUM_USE_MARKER_SHARE * maximum_use,
        f"{name}, the 90 percent fleet",
    )
    return ClassMarkers(
        maximum_use_beams=maximum_use,
        saturation_number=None if saturation is None else round_half_up(saturation),
        saturation_not_reached_by=fleets[-1] if saturation is None else None,
        elasticity_under_0p25_fleet=None if supporting is None else round_half_up(supporting),
        fleet_at_90pct_of_maximum_use=None if ninety is None else round_half_up(ninety),
    )


# ===========================================================================
# 5. The curve
# ===========================================================================


def _class_inputs(inputs: SaturationInputs, device_class: DeviceClass) -> ClassInputs:
    """Return one class's inputs (the contract holds exactly one per class)."""
    return next(entry for entry in inputs.classes if entry.device_class is device_class)


def _check_realized_fleets(requested: Sequence[int]) -> None:
    """Refuse requested fleets whose realized fleets, P x S, do not strictly increase.

    Raises:
        SaturationInvariantError: Naming the requested and the realized fleets.
    """
    realized = [math.prod(_walker_shape(fleet)) for fleet in requested]
    if any(later <= earlier for earlier, later in pairwise(realized)):
        raise SaturationInvariantError(
            f"the requested fleets {list(requested)} realize as {realized} (P x S), which do "
            "not strictly increase; each row is keyed by its realized fleet"
        )


def _method(inputs: SaturationInputs) -> str:
    """Return the method, stated as the rule, at the inputs' values."""
    shell, sweep = inputs.shell, inputs.sweep
    return (
        "Smallest footprint first, per snapshot: the satellite-cell pairs in view are filled "
        f"in {sweep.footprint_bands} geometric footprint bands from the smallest, "
        f"{sweep.passes} proportional passes in each, every band committed before the next; "
        "per satellite at most its beams, per cell one co-channel layer for the phone class "
        "(its area) and its people cap, per pair one layer. A circular Walker Delta shell at "
        f"{shell.altitude_km:g} km and {shell.inclination_deg:g} degrees (P = round(sqrt(N)) "
        "planes of S = round(N / P), the realized N = P x S, phasing F = 1) with a "
        f"{shell.elevation_mask_deg:g} degree mask; a square {shell.reference_aperture_m2:g} "
        f"m^2 aperture at {shell.carrier_hz / _HZ_PER_GHZ:g} GHz, half-power beamwidth "
        f"{shell.beamwidth_factor:g} wavelengths over its side, the beams per satellite "
        "derived from the capacity calibration and the panel. Each fleet's row averages its "
        "snapshots, drawn once over a sidereal day from seed "
        f"{sweep.seed}. Maximum use in closed form (every cell served by the best satellite "
        "the shell can ever offer it); the markers on the elasticity of capacity at the "
        "geometric midpoints of the rows, interpolated in ln N."
    )


def _checks_passed(inputs: SaturationInputs) -> tuple[str, ...]:
    """Return the checks a computed curve passed, each stated as its rule."""
    return (
        "bounds: at every snapshot of every class, useful beams at most min(ceiling, supply) "
        f"and the ceiling at most maximum use, within {_BOUNDS_RELATIVE_TOLERANCE:g} relative",
        f"stall floor: from {_STALL_FLOOR_FROM_FLEET:,} satellites up, the phone class's useful "
        f"beams at least {inputs.sweep.stall_floor:g} x min(ceiling, supply), at every "
        "snapshot and in the snapshot means",
        "capacity per satellite never rises between consecutive rows of any class by more "
        f"than {_CAPACITY_PER_SATELLITE_RISE_TOLERANCE:g} relative to the earlier row (the "
        "snapshots' noise)",
    )


def _curve_limits(inputs: SaturationInputs) -> tuple[str, ...]:
    """Return the curve's stated limits, each stated as its rule, never a magnitude."""
    return (
        "Fluid (fractional) beams, idealized 3 dB footprints and one circular shell.",
        "Residential (night-time) population, every place at its busy hour at once.",
        "No terrain or building blockage, and no interference from other systems.",
        f"Take-up {inputs.demand.take_up:g} is the maximal-demand bound: the capacity found "
        "is assumed used. The fluid model credits a beam hanging over a coast with its land "
        "share only (the coastal under-credit).",
        "Computed with the band in full-time use (d = 1): the engine scales people and "
        "capacity by the downlink share d, and so ignores how d relaxes each cell's people "
        "cap inside the curve (ADR 008).",
        "No interference trim for the directional classes: each terminal's own pattern "
        "suppresses the far-sidelobe leak.",
        f"The directional terminals' pattern floor ({inputs.sidelobe_floor_db:g} dB) is an "
        "estimate, optimistic for the small terminal.",
        f"Computed at the {inputs.shell.reference_aperture_m2:g} m^2 reference panel. The "
        "engine scales the curve linearly by the scenario's panel over it: below it the "
        "directional classes carry more than the rule gives, because their people caps do "
        "not shrink with the panel; the rule is exact in beams for the phone class; and each "
        "beam's rate is held at its reference-panel value, so the link effect of another "
        "array size is not modeled.",
    )


def compute_saturation(
    inputs: SaturationInputs, population: PopulationGrid, *, version_stamp: str
) -> SaturationCurve:
    """Compute the saturation curve on a population grid.

    Runs the stages of the module docstring for the phone class, checks the bounds, the
    stall floor and capacity per satellite, reads the markers against maximum use, and
    records the run's wall time and peak-memory bound.

    Args:
        inputs: The curve's inputs.
        population: The population grid; its SHA-256 must be ``inputs.demand.grid_sha256``.
        version_stamp: The stamp the curve carries.

    Returns:
        The curve, with the phone class's rows and markers.

    Raises:
        PopulationGridError: If the grid is not the one the inputs name, or not global.
        SaturationInvariantError: If a check fails, the realized fleets do not strictly
            increase, or a marker lies before the rows can place it.
    """
    started = time.perf_counter()
    if population.sha256 != inputs.demand.grid_sha256:
        raise PopulationGridError(
            f"the population grid {population.file_name} has SHA-256 {population.sha256}, "
            f"but the inputs expect {inputs.demand.grid_sha256}"
        )
    _check_realized_fleets(inputs.sweep.fleets)
    device_class = DeviceClass.PHONE_CLASS
    phone = _class_inputs(inputs, device_class)
    cells = _demand_cells(population, inputs.demand.density_threshold_per_km2)
    limits = _AllocationLimits(
        beams_per_satellite=_beams_per_satellite(inputs.shell),
        people_per_beam=_people_per_beam(inputs.spectrum_mhz, phone),
        take_up=inputs.demand.take_up,
        beam=_beam_model(inputs.shell),
        footprint_bands=inputs.sweep.footprint_bands,
        passes=inputs.sweep.passes,
    )
    maximum_use = _maximum_use(cells, limits, inputs.shell.inclination_deg)
    times = np.random.default_rng(inputs.sweep.seed).uniform(
        _DAY_START_S, _SIDEREAL_DAY_S, inputs.sweep.snapshots_phone_central
    )
    tasks = [
        _SnapshotTask(
            fleet_index=fleet_index,
            requested_fleet=fleet,
            snapshot_index=snapshot_index,
            time_s=float(time_s),
        )
        for fleet_index, fleet in enumerate(inputs.sweep.fleets)
        for snapshot_index, time_s in enumerate(times)
    ]
    logger.info(
        "saturation: %s, %d fleets x %d snapshots on %d demand cells of %s; maximum use %.0f beams",
        device_class.value,
        len(inputs.sweep.fleets),
        len(times),
        cells.count,
        population.file_name,
        maximum_use,
    )
    sweep = _run_sweep(tasks, _SweepContext(shell=inputs.shell, cells=cells, limits=limits))
    fleets = _by_fleet(sweep.results, len(inputs.sweep.fleets))
    _check_bounds(device_class, fleets, maximum_use)
    _check_stall_floor(fleets, inputs.sweep.stall_floor)
    rows = _phone_rows(
        fleets,
        inputs.sweep.fleets,
        spectrum_mhz=inputs.spectrum_mhz,
        spectral_efficiency_bps_per_hz=phone.spectral_efficiency_bps_per_hz,
        beams_per_satellite=limits.beams_per_satellite,
    )
    _check_capacity_per_satellite(device_class, rows)
    markers = _markers(device_class, rows, maximum_use)
    wall_time_s = time.perf_counter() - started
    peak_memory_mb = _own_peak_mb() + sweep.workers_peak_mb
    logger.info(
        "saturation: %s saturation number %s; %d workers at once after the first task; peak "
        "memory bound %.0f MB (budget %.0f MB); %.1f s",
        device_class.value,
        markers.saturation_number
        if markers.saturation_number is not None
        else f"not reached by {markers.saturation_not_reached_by}",
        sweep.workers,
        peak_memory_mb,
        _MEMORY_BUDGET_MB,
        wall_time_s,
    )
    if peak_memory_mb > _MEMORY_BUDGET_MB:
        logger.warning(
            "saturation: the peak memory bound %.0f MB exceeds the %.0f MB budget",
            peak_memory_mb,
            _MEMORY_BUDGET_MB,
        )
    return SaturationCurve(
        schema_version=SATURATION_CURVE_SCHEMA_VERSION,
        version_stamp=version_stamp,
        parameters=inputs,
        input_hash=curve_input_hash(inputs),
        provenance=CurveProvenance(
            grid_file_name=population.file_name,
            grid_sha256=population.sha256,
            citations=_GRID_CITATIONS,
            licence=_GRID_LICENCE,
            method=_method(inputs),
            checks_passed=_checks_passed(inputs),
            run_measurement=RunMeasurement(wall_time_s=wall_time_s, peak_memory_mb=peak_memory_mb),
        ),
        classes=(ClassCurve(device_class=device_class, rows=rows, markers=markers),),
        bands=(),
        limits=_curve_limits(inputs),
    )


__all__ = [
    "PopulationGrid",
    "PopulationGridError",
    "SaturationInvariantError",
    "compute_saturation",
    "load_population_grid",
]
