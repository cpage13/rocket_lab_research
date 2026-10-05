"""End-to-end and seam tests of the saturation module and its contract (the phone class).

The saturation curve (``communications.saturation``, the one module that imports numpy)
counts how many co-channel beams a Walker shell keeps lit over people as the fleet grows;
its contract (``communications.saturation_curve``) is numpy-free. These tests are the
module's executable specification for the phone class, each naming what it exercises and
what counts as success:

* through ``compute_saturation`` on synthetic global grids (a few fleets, one snapshot): a
  uniform band, where the supply bound is the time fraction over land and the 0.10 crossing
  is not reached; a two-band world, where maximum use matches its closed form; a dense
  mid-latitude band swept twice, where the 90 percent fleet reads maximum use, never a
  sweep's last ceiling; capacity that does not fall between rows; determinism;
* through the private seam ``_allocate`` with explicit satellite positions: one patch under
  one overhead satellite; the per-cell area and one-layer-per-pair invariants;
* the real grid at a coarse, fast setting, frozen at 1e-4 relative;
* numpy confinement (a subprocess), the people-per-beam arithmetic, the class constants,
  the checks' refusals, the grid loader's refusals and the contract's validators.

Every synthetic world also passes the module's own checks (the bounds at every snapshot,
capacity per satellite never rising), so each is shaped for it: its capacity per satellite
falls between its rows for a physical reason (a people cap or the tiling binding), never by
the noise of one snapshot. The worlds' grids come from ``synthetic_population_grid`` and
their inputs from ``synthetic_saturation_inputs`` (``conftest.py``).
"""

from __future__ import annotations

import dataclasses
import hashlib
import math
import os
import subprocess
import sys
import tracemalloc
from collections.abc import Callable, Sequence
from itertools import combinations, pairwise
from pathlib import Path
from typing import Protocol

import numpy as np
import pytest

from common.cadence import round_half_up
from common.file_io import ModelFileError
from communications import saturation as sat
from communications.config import IridiumDials
from communications.constants import (
    CLASS_SE_CENTRAL,
    CLASS_USAGE,
    POPULATION_GRID_PATH,
    POPULATION_GRID_SHA256,
    DeviceClass,
)
from communications.saturation import (
    PopulationGrid,
    PopulationGridError,
    SaturationInvariantError,
    compute_saturation,
    load_population_grid,
)
from communications.saturation_curve import (
    SATURATION_CURVE_SCHEMA_VERSION,
    BandCurve,
    BandName,
    ClassCurve,
    ClassInputs,
    ClassMarkers,
    CurveProvenance,
    CurveRow,
    DirectionalDiagnostics,
    RunMeasurement,
    SaturationCurve,
    SaturationInputs,
    ShellInputs,
    SweepInputs,
    curve_input_hash,
    saturation_inputs_for,
    walker_shape,
)

# ---------------------------------------------------------------------------
# Closed forms the tests check the module against (derived here, independently)
# ---------------------------------------------------------------------------

EARTH_RADIUS_KM = 6371.0
"""The Earth's mean radius, km (the curve's pinned value)."""

SPEED_OF_LIGHT_M_S = 2.998e8
"""The speed of light, m/s, to the curve's pinned four figures."""

STAMP = "test"
"""The version stamp every curve here is computed with."""

PHONE = DeviceClass.PHONE_CLASS
"""The class this part computes."""

PeopleAt = Callable[[np.ndarray, np.ndarray], np.ndarray]
"""People per cell from the cell centres' latitudes and longitudes, degrees (the input of
``conftest.py``'s grid builder)."""

GridBuilder = Callable[[float, PeopleAt], PopulationGrid]
"""The ``synthetic_population_grid`` fixture: a cell size and the people per cell in, a
global grid out."""


class SaturationInputsBuilder(Protocol):
    """The ``synthetic_saturation_inputs`` fixture (``conftest.py`` defines the same shape)."""

    def __call__(
        self,
        grid: PopulationGrid,
        *,
        fleets: tuple[int, ...],
        snapshots: int = ...,
        beams_per_satellite: float | None = ...,
    ) -> SaturationInputs:
        """Return the inputs for a synthetic grid at the given sweep."""
        ...


def _phone_inputs() -> ClassInputs:
    """The phone class's default inputs."""
    return next(entry for entry in SaturationInputs().classes if entry.device_class is PHONE)


PHONE_PEOPLE_PER_BEAM = (
    SaturationInputs().spectrum_mhz
    * _phone_inputs().spectral_efficiency_bps_per_hz
    / (_phone_inputs().active_rate_mbps * _phone_inputs().concurrency_peak)
)
"""The phone class's people per beam at d = 1 (8 MHz x 0.65 / (0.75 x 0.025) = 277.333)."""


def view_limit_rad(shell: ShellInputs) -> float:
    """The central angle at which a satellite stands on the elevation mask."""
    mask = math.radians(shell.elevation_mask_deg)
    return (
        math.acos(EARTH_RADIUS_KM * math.cos(mask) / (EARTH_RADIUS_KM + shell.altitude_km)) - mask
    )


def footprint_km2(shell: ShellInputs, central_angle_rad: float) -> float:
    """A beam's 3 dB footprint at a central angle, by the laws of cosines and sines."""
    orbit = EARTH_RADIUS_KM + shell.altitude_km
    slant = math.sqrt(
        EARTH_RADIUS_KM**2 + orbit**2 - 2 * EARTH_RADIUS_KM * orbit * math.cos(central_angle_rad)
    )
    sin_elevation = (orbit * math.cos(central_angle_rad) - EARTH_RADIUS_KM) / slant
    sin_scan = EARTH_RADIUS_KM * math.sqrt(1 - sin_elevation**2) / orbit
    cos_scan = math.sqrt(1 - sin_scan**2)
    width = (
        shell.beamwidth_factor
        * (SPEED_OF_LIGHT_M_S / shell.carrier_hz)
        / math.sqrt(shell.reference_aperture_m2)
    )
    return math.pi / 4 * (slant * width) * (slant * width / (cos_scan * sin_elevation))


def cell_area_km2(top_deg: float, cell_deg: float, columns: int) -> float:
    """The area of one cell of a row between two latitudes (a zone of the sphere, split)."""
    zone = abs(math.sin(math.radians(top_deg)) - math.sin(math.radians(top_deg - cell_deg)))
    return 2 * math.pi * EARTH_RADIUS_KM**2 * zone / columns


def log_log_fleet(rows: tuple[CurveRow, ...], target: float) -> float | None:
    """The fleet at which L first reaches the target, log-log between rows."""
    for low, high in pairwise(rows):
        if low.useful_beams < target <= high.useful_beams:
            share = math.log(target / low.useful_beams) / math.log(
                high.useful_beams / low.useful_beams
            )
            return math.exp(math.log(low.fleet) + share * math.log(high.fleet / low.fleet))
    return None


def small_sweep(inputs: SaturationInputs, snapshots_directional: int = 1) -> SaturationInputs:
    """The inputs with no mounted-terminal extension and the directional classes at the given
    snapshots, so a synthetic world's curve stays small and fast."""
    sweep = SweepInputs.model_validate(
        {
            **inputs.sweep.model_dump(),
            "mounted_terminal_extension": (),
            "snapshots_directional": snapshots_directional,
        }
    )
    return inputs.model_copy(update={"sweep": sweep})


def phone_curve(curve: SaturationCurve) -> ClassCurve:
    """The phone class's curve, found by its key (a curve lists every class it has)."""
    (found,) = [entry for entry in curve.classes if entry.device_class is PHONE]
    return found


# ---------------------------------------------------------------------------
# The synthetic worlds
# ---------------------------------------------------------------------------

BAND_CELL_DEG = 2.0
"""The uniform band's cell: 2 degrees, so its rows centre on odd latitudes."""

BAND_HALF_WIDTH_DEG = 4.0
"""The band holds the cells centred within 4 degrees of the equator (at 1 and 3 degrees,
north and south): 720 cells."""

BAND_CAP_BEAMS = 1.25
"""Each band cell's people cap, beams: small, so the cap binds as the fleet grows."""

ONE_BEAM = 1.0
"""B for the band worlds: one beam per satellite makes the supply bound count satellites."""

BAND_FLEETS = (1_000, 10_000)
"""The band worlds' requested fleets (realized 992 and 10,000)."""

DENSE_ROWS_DEG = (55.0, 63.0)
"""The two-band world's dense rows lie between these latitudes north: cells centred at 57,
59 and 61 degrees, 4, 6 and 8 degrees beyond the 53 degree inclination."""

DENSE_PEOPLE_PER_CELL = 1e6
"""People in each dense cell: a people cap of about 3,600 beams, far above what tiles it."""

MID_BAND_CELL_DEG = 0.5
"""The dense mid-latitude band's cell: small, so one satellite can tile one, as on the
real grid's 0.25 degree cells."""

MID_BAND_DEG = (40.0, 42.0)
"""The dense mid-latitude band's latitudes, north, where a 53 degree shell flies densely."""

MID_BAND_SWEEPS = (
    (500, 1_000, 2_000, 4_000, 8_000, 16_000),
    (500, 1_000, 2_000, 4_000, 8_000, 12_000),
)
"""The dense band's two sweeps: the same rows to 8,000, then 16,000 or 12,000."""


def band_people(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    """People per cell of the uniform band: 1.25 beams' worth within 4 degrees of the equator."""
    return np.where(np.abs(lat) < BAND_HALF_WIDTH_DEG, BAND_CAP_BEAMS * PHONE_PEOPLE_PER_BEAM, 0.0)


def two_band_people(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    """The uniform band plus three dense rows beyond the inclination."""
    dense = (lat > DENSE_ROWS_DEG[0]) & (lat < DENSE_ROWS_DEG[1])
    return np.where(dense, DENSE_PEOPLE_PER_CELL, band_people(lat, lon))


def mid_band_people(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    """A dense band of small cells from 40 to 42 degrees north."""
    inside = (lat > MID_BAND_DEG[0]) & (lat < MID_BAND_DEG[1])
    return np.where(inside, DENSE_PEOPLE_PER_CELL, 0.0)


@pytest.fixture(scope="module")
def uniform_band(synthetic_population_grid: GridBuilder) -> PopulationGrid:
    """The uniform band's grid."""
    return synthetic_population_grid(BAND_CELL_DEG, band_people)


@pytest.fixture(scope="module")
def uniform_band_curve(
    uniform_band: PopulationGrid, synthetic_saturation_inputs: SaturationInputsBuilder
) -> SaturationCurve:
    """The uniform band's curve: B = 1, fleets 1,000 and 10,000, one snapshot."""
    inputs = synthetic_saturation_inputs(
        uniform_band, fleets=BAND_FLEETS, beams_per_satellite=ONE_BEAM
    )
    return compute_saturation(small_sweep(inputs), uniform_band, version_stamp=STAMP)


@pytest.fixture(scope="module")
def two_band_world(synthetic_population_grid: GridBuilder) -> PopulationGrid:
    """The two-band world's grid."""
    return synthetic_population_grid(BAND_CELL_DEG, two_band_people)


@pytest.fixture(scope="module")
def two_band_world_curve(
    two_band_world: PopulationGrid, synthetic_saturation_inputs: SaturationInputsBuilder
) -> SaturationCurve:
    """The two-band world's curve: B = 1, fleets 1,000 and 10,000, one snapshot."""
    inputs = synthetic_saturation_inputs(
        two_band_world, fleets=BAND_FLEETS, beams_per_satellite=ONE_BEAM
    )
    return compute_saturation(small_sweep(inputs), two_band_world, version_stamp=STAMP)


@pytest.fixture(scope="module")
def mid_band_curves(
    synthetic_population_grid: GridBuilder, synthetic_saturation_inputs: SaturationInputsBuilder
) -> tuple[SaturationCurve, ...]:
    """The dense mid-latitude band's two curves, one per sweep, at the central B (150)."""
    grid = synthetic_population_grid(MID_BAND_CELL_DEG, mid_band_people)
    return tuple(
        compute_saturation(
            small_sweep(synthetic_saturation_inputs(grid, fleets=fleets)), grid, version_stamp=STAMP
        )
        for fleets in MID_BAND_SWEEPS
    )


# ---------------------------------------------------------------------------
# Through compute_saturation on synthetic grids
# ---------------------------------------------------------------------------


def test_supply_bound_on_a_uniform_band_is_the_time_fraction_over_land(
    uniform_band_curve: SaturationCurve,
) -> None:
    """Objective: the supply bound counts a satellite's beams where it can reach people.

    Sample: the uniform band (2 degree cells within 4 degrees of the equator, 1.25 beams of
    people each), one beam per satellite (B = 1), fleets 1,000 and 10,000 (realized 992 and
    10,000), one snapshot.

    Expected outcome: with B = 1 a satellite adds one beam of supply exactly when a
    populated cell centre is in view, so supply / (N x B) is the share of satellite time with
    the band in view. A Walker shell spaces its arguments of latitude evenly, so that share is
    (2 / pi) asin(sin(phi) / sin(i)), phi the outer cells' centres (3 degrees) plus the
    view's central-angle limit: within 1 percent at both fleets (a cell centre is up to a
    degree of longitude off, which pulls the edge in by under 0.07 degree). At 992
    satellites, far under the band's people cap, every such satellite places its beam, so L
    equals the supply and U is the same share.
    """
    shell = uniform_band_curve.parameters.shell
    phi = math.radians(BAND_HALF_WIDTH_DEG - BAND_CELL_DEG / 2) + view_limit_rad(shell)
    share = 2 / math.pi * math.asin(math.sin(phi) / math.sin(math.radians(shell.inclination_deg)))
    rows = phone_curve(uniform_band_curve).rows
    assert [row.fleet for row in rows] == [992, 10_000]
    for row in rows:
        assert row.supply_beams / (row.fleet * ONE_BEAM) == pytest.approx(share, rel=0.01)
    first = rows[0]
    assert first.useful_beams == pytest.approx(first.supply_beams, rel=1e-9)
    assert first.ocean_factor == pytest.approx(share, rel=0.01)


def test_a_class_whose_crossing_is_not_reached_reports_the_last_fleet(
    uniform_band_curve: SaturationCurve,
) -> None:
    """Objective: a curve that has not flattened by its last row reports no spectrum bound.

    Sample: the uniform band's curve (fleets 992 and 10,000), whose capacity still grows
    with an elasticity well above 0.10 between its two rows.

    Expected outcome: no saturation number; ``saturation_not_reached_by`` is the last row's
    fleet, 10,000; no crossing under 0.25 either.
    """
    rows = phone_curve(uniform_band_curve).rows
    markers = phone_curve(uniform_band_curve).markers
    low, high = rows
    elasticity = math.log(high.capacity_gbps / low.capacity_gbps) / math.log(high.fleet / low.fleet)
    assert elasticity > 0.25
    assert markers.saturation_number is None
    assert markers.saturation_not_reached_by == rows[-1].fleet == 10_000
    assert markers.elasticity_under_0p25_fleet is None


def test_maximum_use_matches_its_closed_form_on_a_two_band_world(
    two_band_world: PopulationGrid, two_band_world_curve: SaturationCurve
) -> None:
    """Objective: maximum use is the closed form, every cell served by the best satellite the
    shell can ever offer it, one layer, capped by its people; it ignores the fleet.

    Sample: the uniform band (its people cap binds) plus dense rows centred at 57, 59 and 61
    degrees north (tiling binds), B = 1, fleets 1,000 and 10,000, one snapshot.

    Expected outcome: maximum use equals the sum over cells of min(cell area /
    footprint(max(0, |lat| - 53 degrees)), people cap), within 1e-6 relative (the module
    interpolates a footprint table): the band's cells at their cap; the 57 and 59 degree rows
    tiled at 4 and 6 degrees from the best satellite the shell offers; the 61 degree row, 8
    degrees beyond the inclination and past the view's 7.165 degree limit, adding nothing.
    """
    shell = two_band_world_curve.parameters.shell
    limit = view_limit_rad(shell)
    inclination = math.radians(shell.inclination_deg)
    n_lat, n_lon = two_band_world.population.shape
    expected = 0.0
    regimes: dict[str, list[float]] = {"capped": [], "tiled": [], "beyond reach": []}
    for row in range(n_lat):
        people = float(two_band_world.population[row, 0])
        if people == 0.0:
            continue
        top = 90.0 - row * BAND_CELL_DEG
        centre = math.radians(top - BAND_CELL_DEG / 2)
        best = max(0.0, abs(centre) - inclination)
        if best > limit:
            regimes["beyond reach"].append(math.degrees(centre))
            continue
        tiled = cell_area_km2(top, BAND_CELL_DEG, n_lon) / footprint_km2(shell, best)
        capped = people / PHONE_PEOPLE_PER_BEAM
        regimes["tiled" if tiled < capped else "capped"].append(math.degrees(centre))
        expected += n_lon * min(tiled, capped)
    assert regimes["tiled"] == pytest.approx([59.0, 57.0])
    assert regimes["beyond reach"] == pytest.approx([61.0])
    assert regimes["capped"] == pytest.approx([3.0, 1.0, -1.0, -3.0])
    markers = phone_curve(two_band_world_curve).markers
    assert markers.maximum_use_beams == pytest.approx(expected, rel=1e-6)


def test_ninety_percent_fleet_reads_maximum_use_never_a_sweeps_last_ceiling(
    mid_band_curves: tuple[SaturationCurve, ...],
) -> None:
    """Objective: the 90 percent marker's denominator is maximum use, which does not move with
    the sweep (the strategy's failure mode "The denominator moves with the sweep").

    Sample: a dense band of 0.5 degree cells from 40 to 42 degrees north (tiling binds, as on
    the real grid), the central B of 150, swept twice: 500 to 16,000 and 500 to 12,000, the
    same rows to 8,000, one snapshot.

    Expected outcome: both sweeps report the same maximum use and the same 90 percent fleet,
    and it is the log-log reading of the rows at 0.9 x maximum use, rounded half up. The same
    reading at 0.9 x a sweep's last ceiling gives two different fleets, so a sweep-dependent
    denominator would be caught.
    """
    readings = []
    for curve in mid_band_curves:
        rows = phone_curve(curve).rows
        markers = phone_curve(curve).markers
        at_maximum_use = log_log_fleet(rows, 0.9 * markers.maximum_use_beams)
        assert at_maximum_use is not None
        assert markers.fleet_at_90pct_of_maximum_use == round_half_up(at_maximum_use)
        at_last_ceiling = log_log_fleet(rows, 0.9 * rows[-1].ceiling_beams)
        assert at_last_ceiling is not None
        readings.append((markers, round_half_up(at_last_ceiling)))
    (longer, longer_by_ceiling), (shorter, shorter_by_ceiling) = readings
    assert longer.maximum_use_beams == shorter.maximum_use_beams
    assert longer.fleet_at_90pct_of_maximum_use == shorter.fleet_at_90pct_of_maximum_use
    assert longer_by_ceiling != shorter_by_ceiling


def test_capacity_does_not_fall_more_than_two_percent_between_rows(
    mid_band_curves: tuple[SaturationCurve, ...],
    uniform_band_curve: SaturationCurve,
    two_band_world_curve: SaturationCurve,
) -> None:
    """Objective: capacity grows with the fleet, or holds, up to the snapshots' spread.

    Sample: every synthetic curve here: the dense band's two sweeps, the uniform band and the
    two-band world.

    Expected outcome: each row's capacity is at least 0.98 of the row before it.
    """
    for curve in (*mid_band_curves, uniform_band_curve, two_band_world_curve):
        for earlier, later in pairwise(phone_curve(curve).rows):
            assert later.capacity_gbps >= 0.98 * earlier.capacity_gbps


def test_two_runs_under_the_fixed_seed_are_equal(
    uniform_band: PopulationGrid, synthetic_saturation_inputs: SaturationInputsBuilder
) -> None:
    """Objective: the curve is deterministic: the snapshot draw is fixed by the seed and the
    order the workers finish in changes nothing.

    Sample: the uniform band at two snapshots, computed twice.

    Expected outcome: the two curves are equal in everything but the run's own measurement
    of wall time and memory (which the comparison sets to the first run's), and the two
    snapshots differ (a spread above zero), so the comparison covers the shared draw.
    """
    inputs = small_sweep(
        synthetic_saturation_inputs(
            uniform_band, fleets=BAND_FLEETS, snapshots=2, beams_per_satellite=ONE_BEAM
        ),
        snapshots_directional=2,
    )
    first = compute_saturation(inputs, uniform_band, version_stamp=STAMP)
    second = compute_saturation(inputs, uniform_band, version_stamp=STAMP)
    measured_as_first = second.model_copy(
        update={
            "provenance": second.provenance.model_copy(
                update={"run_measurement": first.provenance.run_measurement}
            )
        }
    )
    assert measured_as_first == first
    assert any(row.useful_beams_spread > 0 for row in phone_curve(first).rows)


def test_compute_saturation_refuses_a_grid_its_inputs_do_not_name(
    uniform_band: PopulationGrid,
) -> None:
    """Objective: a curve is computed only on the grid its inputs name.

    Sample: the default inputs, which name the shipped grid's SHA-256, with the uniform band.

    Expected outcome: PopulationGridError naming both digests, before any computation.
    """
    with pytest.raises(PopulationGridError, match=uniform_band.sha256) as refused:
        compute_saturation(SaturationInputs(), uniform_band, version_stamp=STAMP)
    assert POPULATION_GRID_SHA256 in str(refused.value)


# ---------------------------------------------------------------------------
# Through the _allocate seam, with explicit positions
# ---------------------------------------------------------------------------

PATCH_CENTRE_DEG = (0.125, 0.125)
"""The populated patch's centre: the 0.25 degree cell just north and east of (0, 0)."""

CROWD_OFFSETS_DEG = ((0.0, 0.0), (0.1, 0.1), (2.0, 0.0), (0.0, -3.0), (-5.0, 2.0))
"""Satellite offsets from the patch's centre, degrees (latitude, longitude): one overhead,
one 0.14 degree off it (the same footprint band), three farther out."""


def seam_limits(beams_per_satellite: float) -> sat._AllocationLimits:
    """The phone class's allocation limits at the defaults, with a chosen B."""
    inputs = SaturationInputs()
    return sat._AllocationLimits(
        beams_per_satellite=beams_per_satellite,
        people_per_beam=PHONE_PEOPLE_PER_BEAM,
        take_up=inputs.demand.take_up,
        beam=sat._beam_model(inputs.shell),
        footprint_bands=inputs.sweep.footprint_bands,
        passes=inputs.sweep.passes,
        spectrum_mhz=inputs.spectrum_mhz,
        spectral_efficiency_bps_per_hz=_phone_inputs().spectral_efficiency_bps_per_hz,
        directional=None,
    )


def satellites_at(points_deg: Sequence[tuple[float, float]]) -> sat._SatellitePositions:
    """Satellites over the given (latitude, longitude) points, degrees."""
    lat, lon = np.radians(np.array(points_deg, dtype=np.float64)).T
    return sat._SatellitePositions(
        lat_rad=np.ascontiguousarray(lat), lon_rad=np.ascontiguousarray(lon)
    )


def patch_people(cell_deg: float, half_cells: int) -> PeopleAt:
    """People in a square patch of cells around the patch centre (half_cells either side)."""
    reach = (half_cells + 0.5) * cell_deg

    def people(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
        inside = (np.abs(lat - PATCH_CENTRE_DEG[0]) < reach) & (
            np.abs(lon - PATCH_CENTRE_DEG[1]) < reach
        )
        return np.where(inside, DENSE_PEOPLE_PER_CELL, 0.0)

    return people


@pytest.mark.parametrize(
    ("cell_deg", "beams_per_satellite", "binding"),
    [(0.25, 150.0, "the cell's area"), (2.0, 150.0, "the satellite's beams")],
)
def test_one_patch_under_one_overhead_satellite(
    synthetic_population_grid: GridBuilder,
    cell_deg: float,
    beams_per_satellite: float,
    binding: str,
) -> None:
    """Objective: a satellite overhead a populated patch fills it one layer deep, up to its
    beams.

    Sample: a global grid with one populated cell (people far above any cap) centred at
    (0.125, 0.125) for 0.25 degree cells, or the 2 degree cell around it, and one satellite
    placed exactly over that centre, B = 150.

    Expected outcome: L = min(B, cell area / the overhead footprint), the overhead footprint
    pi / 4 x (450 km x 0.886 lambda / 5 m)^2 = 170.8 km^2: a 0.25 degree cell (about 773
    km^2) takes 4.5 beams, so the cell's area binds; a 2 degree cell (about 49,400 km^2)
    could take 289, so the satellite's 150 beams bind. The supply and the ceiling read the
    same here.
    """
    grid = synthetic_population_grid(cell_deg, patch_people(cell_deg, 0))
    cells = sat._demand_cells(grid, 1.0)
    assert cells.count == 1
    shell = SaturationInputs().shell
    centre_row = int((90.0 - PATCH_CENTRE_DEG[0]) // cell_deg)
    area = cell_area_km2(90.0 - centre_row * cell_deg, cell_deg, grid.population.shape[1])
    satellite_over = (float(np.degrees(cells.lat_rad[0])), float(np.degrees(cells.lon_rad[0])))
    allocation = sat._allocate(
        satellites_at([satellite_over]), cells, seam_limits(beams_per_satellite)
    )
    overhead_footprint = footprint_km2(shell, 0.0)
    assert overhead_footprint == pytest.approx(170.82, abs=0.01)
    expected = min(beams_per_satellite, area / overhead_footprint)
    assert allocation.useful_beams == pytest.approx(expected, rel=1e-9)
    binds_on_beams = area / overhead_footprint > beams_per_satellite
    assert binds_on_beams == (binding == "the satellite's beams")
    assert allocation.supply_beams == pytest.approx(expected, rel=1e-9)


@pytest.fixture(scope="module")
def crowded_patch(
    synthetic_population_grid: GridBuilder,
) -> tuple[sat._DemandCells, sat._Allocation]:
    """A 3 x 3 patch of 0.25 degree cells under five satellites (CROWD_OFFSETS_DEG), B = 150.

    Returns the demand cells and the allocation.
    """
    grid = synthetic_population_grid(0.25, patch_people(0.25, 1))
    cells = sat._demand_cells(grid, 1.0)
    points = [
        (PATCH_CENTRE_DEG[0] + d_lat, PATCH_CENTRE_DEG[1] + d_lon)
        for d_lat, d_lon in CROWD_OFFSETS_DEG
    ]
    return cells, sat._allocate(satellites_at(points), cells, seam_limits(150.0))


def test_co_channel_area_never_exceeds_a_cells_area(
    crowded_patch: tuple[sat._DemandCells, sat._Allocation],
) -> None:
    """Objective: one co-channel layer per cell for a 0 dBi device: the footprints placed on
    a cell never cover more than the cell.

    Sample: the crowded patch: nine cells under five satellites with 750 beams between them,
    against the patch's room for about 40 overhead beams, so the area binds.

    Expected outcome: in every cell, the sum over its pairs of beams x footprint is at most
    the cell's area (1e-9 relative), and equals it in all nine (the bound binds); at least one
    cell is shared by two satellites, so the sum is over more than one.
    """
    cells, allocation = crowded_patch
    assert cells.count == 9
    covered = np.bincount(
        allocation.cell, weights=allocation.beams * allocation.footprint_km2, minlength=cells.count
    )
    assert np.all(covered <= cells.area_km2 * (1 + 1e-9))
    assert covered == pytest.approx(cells.area_km2, rel=1e-9)
    placing = allocation.beams > 0
    satellites_per_cell = [
        len(set(allocation.satellite[placing & (allocation.cell == cell)].tolist()))
        for cell in range(cells.count)
    ]
    assert max(satellites_per_cell) >= 2


def test_one_satellite_adds_at_most_one_layer_to_a_cell(
    crowded_patch: tuple[sat._DemandCells, sat._Allocation],
) -> None:
    """Objective: one satellite adds at most one layer to a cell.

    Sample: the crowded patch.

    Expected outcome: for every satellite-cell pair, its beams x its footprint is at most the
    cell's area (1e-9 relative), and the beams placed are positive (the test covers placed
    pairs).
    """
    cells, allocation = crowded_patch
    assert allocation.beams.sum() > 0
    layer = allocation.beams * allocation.footprint_km2 / cells.area_km2[allocation.cell]
    assert np.all(layer <= 1 + 1e-9)


# ---------------------------------------------------------------------------
# The real grid at a coarse, fast setting
# ---------------------------------------------------------------------------

COARSE_REAL_FLEETS = (340, 1_000, 2_000)
"""The coarse setting's requested fleets (realized 342, 992 and 1,980), one snapshot."""

COARSE_REAL_ROWS = (
    (
        342,
        20650.005817588586,
        107.38003025146064,
        0.4025342264637151,
        102190.2125947176,
        21408.925531671954,
    ),
    (
        992,
        56128.776221076834,
        291.8696363495996,
        0.3772095176147637,
        196678.16776641438,
        61894.68547314836,
    ),
    (
        1980,
        101851.76200360352,
        529.6291624187384,
        0.34293522560135864,
        255760.63823593326,
        124345.18803992725,
    ),
)
"""The coarse rows as first computed (2026-10-05), frozen: fleet, L, capacity Gbps, U,
ceiling, supply. They agree with the reference prototype's same snapshot at float
precision."""

COARSE_REAL_MAXIMUM_USE = 380946.7365253218
"""The phone class's maximum use on the shipped grid at the investor's usage, beams."""


@pytest.fixture(scope="module")
def real_grid(repo_dir: Path) -> PopulationGrid:
    """The shipped population grid."""
    return load_population_grid(repo_dir / POPULATION_GRID_PATH, POPULATION_GRID_SHA256)


def test_the_real_grid_at_a_coarse_setting_is_frozen(real_grid: PopulationGrid) -> None:
    """Objective: the module's numbers on the shipped grid do not drift.

    Sample: the default inputs (the investor's usage) at fleets 340, 1,000 and 2,000 and one
    snapshot.

    Expected outcome: every row (L, capacity, U, the ceiling, the supply) and maximum use
    within 1e-4 relative of the frozen values; no 0.10 crossing by 1,980 and no other marker;
    the curve's envelope: schema, stamp, the input hash of its parameters, the grid's name,
    digest, citations and licence, the three checks passed, the run measured, the stated
    limits, and the phone class alone with no band yet.
    """
    inputs = SaturationInputs(
        sweep=SweepInputs(
            fleets=COARSE_REAL_FLEETS,
            mounted_terminal_extension=(),
            snapshots_phone_central=1,
            snapshots_directional=1,
        )
    )
    curve = compute_saturation(inputs, real_grid, version_stamp=STAMP)
    rows = phone_curve(curve).rows
    assert [row.fleet for row in rows] == [frozen[0] for frozen in COARSE_REAL_ROWS]
    assert [row.requested_fleet for row in rows] == list(COARSE_REAL_FLEETS)
    for row, (_, useful, capacity, ocean, ceiling, supply) in zip(
        rows, COARSE_REAL_ROWS, strict=True
    ):
        assert row.useful_beams == pytest.approx(useful, rel=1e-4)
        assert row.capacity_gbps == pytest.approx(capacity, rel=1e-4)
        assert row.ocean_factor == pytest.approx(ocean, rel=1e-4)
        assert row.ceiling_beams == pytest.approx(ceiling, rel=1e-4)
        assert row.supply_beams == pytest.approx(supply, rel=1e-4)
        assert row.useful_beams_spread == 0.0
        assert row.directional is None
        assert row.trim is None
    markers = phone_curve(curve).markers
    assert markers.maximum_use_beams == pytest.approx(COARSE_REAL_MAXIMUM_USE, rel=1e-4)
    assert markers.saturation_number is None
    assert markers.saturation_not_reached_by == 1_980
    assert markers.elasticity_under_0p25_fleet is None
    assert markers.fleet_at_90pct_of_maximum_use is None
    assert curve.schema_version == SATURATION_CURVE_SCHEMA_VERSION == "saturation-v1"
    assert curve.version_stamp == STAMP
    assert curve.parameters == inputs
    assert curve.input_hash == curve_input_hash(inputs)
    provenance = curve.provenance
    assert provenance.grid_file_name == "ghs_pop_e2030_0p25deg.npz"
    assert provenance.grid_sha256 == POPULATION_GRID_SHA256
    assert len(provenance.citations) == 2
    assert "doi:10.2905/2FF68A52-5B5B-4A22-8F40-C41DA8332CFE" in provenance.citations[0]
    assert "doi:10.1080/17538947.2024.2390454" in provenance.citations[1]
    assert provenance.licence == "CC BY 4.0"
    assert len(provenance.checks_passed) == 3
    assert provenance.run_measurement.wall_time_s > 0
    assert provenance.run_measurement.peak_memory_mb > 0
    assert len(curve.limits) == 8
    assert [entry.device_class for entry in curve.classes] == list(DeviceClass)
    assert curve.bands == ()


# ---------------------------------------------------------------------------
# numpy confinement, the arithmetic and the constants
# ---------------------------------------------------------------------------

NUMPY_FREE_MODULES = (
    "communications.config",
    "communications.engine",
    "communications.json_output",
    "communications.saturation_curve",
)
"""The communications modules that must load without numpy (ADR 010)."""


def _numpy_loaded_after_importing(modules: tuple[str, ...], code_dir: Path) -> bool:
    """Whether a fresh interpreter has numpy loaded after importing the modules."""
    source = "import sys\n" + "".join(f"import {name}\n" for name in modules)
    source += "sys.exit(0 if 'numpy' in sys.modules else 3)\n"
    environment = {**os.environ, "PYTHONPATH": str(code_dir / "src")}
    result = subprocess.run(  # noqa: S603 (a fixed command: this interpreter and our source)
        [sys.executable, "-c", source],
        capture_output=True,
        text=True,
        check=False,
        env=environment,
    )
    assert result.returncode in (0, 3), result.stderr
    return result.returncode == 0


def test_numpy_stays_inside_the_saturation_module(code_dir: Path) -> None:
    """Objective: numpy stays inside ``communications.saturation`` (ADR 010), transitive
    imports included, which a grep would miss.

    Sample: a fresh interpreter importing ``communications.config``, ``.engine``,
    ``.json_output`` and ``.saturation_curve``; then one importing
    ``communications.saturation`` too, the control.

    Expected outcome: numpy is not in ``sys.modules`` after the first, and is after the
    control (so the probe can see it).
    """
    assert not _numpy_loaded_after_importing(NUMPY_FREE_MODULES, code_dir)
    assert _numpy_loaded_after_importing(
        (*NUMPY_FREE_MODULES, "communications.saturation"), code_dir
    )


@pytest.mark.parametrize(
    ("device_class", "people_per_beam"),
    [
        (DeviceClass.SMALL_TERMINAL_CLASS, 320.0),
        (DeviceClass.MOUNTED_TERMINAL_CLASS, 40.0),
        (DeviceClass.PHONE_CLASS, 832.0 / 3.0),
    ],
)
def test_people_per_beam_is_the_beam_rate_over_the_busy_hour_load(
    device_class: DeviceClass, people_per_beam: float
) -> None:
    """Objective: people per beam at d = 1 is 8 MHz x the class's central SE over its busy-hour
    load (its rate while active x its busy-hour share).

    Sample: the default inputs, each class.

    Expected outcome, worked by hand: the small terminal 8 x 2.0 / (2.0 x 0.025) = 320; the
    mounted terminal 8 x 2.5 / (5.0 x 0.10) = 40; the phone class 8 x 0.65 / (0.75 x 0.025)
    = 277.333 (832 / 3).
    """
    inputs = SaturationInputs()
    class_inputs = next(entry for entry in inputs.classes if entry.device_class is device_class)
    assert sat._people_per_beam(inputs.spectrum_mhz, class_inputs) == pytest.approx(
        people_per_beam, rel=1e-12
    )


def test_each_class_off_peak_share_is_at_most_its_busy_hour_share() -> None:
    """Objective: the class constants are whole and coherent.

    Sample: ``CLASS_USAGE`` and ``CLASS_SE_CENTRAL``.

    Expected outcome: one entry per class, in the class key's order (small terminal, mounted
    terminal, phone class), and each class's off-peak share at most its busy-hour share.
    """
    assert list(CLASS_USAGE) == list(DeviceClass)
    assert list(CLASS_SE_CENTRAL) == list(DeviceClass)
    assert [member.value for member in DeviceClass] == [
        "small_terminal_class",
        "mounted_terminal_class",
        "phone_class",
    ]
    for usage in CLASS_USAGE.values():
        assert 0 < usage.concurrency_offpeak <= usage.concurrency_peak <= 1


def _row(fleet: int, useful: float, capacity: float) -> CurveRow:
    """A bare curve row for the checks' refusals, requested at its own realized fleet (each
    fleet used here realizes as itself when requested)."""
    return CurveRow(
        fleet=fleet,
        requested_fleet=fleet,
        useful_beams=useful,
        useful_beams_spread=0.0,
        capacity_gbps=capacity,
        ocean_factor=0.1,
        ceiling_beams=useful,
        supply_beams=useful,
        directional=None,
        trim=None,
    )


@pytest.mark.parametrize(
    ("refused", "message"),
    [
        (
            lambda: sat._check_bounds(
                PHONE, (sat._FleetSnapshots(342, (11.0,), (10.0,), (20.0,), (1.0,), ()),), 100.0
            ),
            "useful beams 11.0 exceed",
        ),
        (
            lambda: sat._check_bounds(
                PHONE, (sat._FleetSnapshots(342, (5.0,), (150.0,), (20.0,), (1.0,), ()),), 100.0
            ),
            "the ceiling 150.0 exceeds maximum use",
        ),
        (
            lambda: sat._check_stall_floor(
                (sat._FleetSnapshots(20_022, (90.0,), (100.0,), (200.0,), (1.0,), ()),), 0.98
            ),
            "under the stall floor",
        ),
        (
            lambda: sat._check_capacity_per_satellite(
                PHONE, (_row(342, 10.0, 1.0), _row(992, 40.0, 4.0))
            ),
            "capacity per satellite rises",
        ),
        (
            lambda: sat._markers(
                PHONE,
                (_row(342, 100.0, 1.0), _row(992, 101.0, 1.01), _row(1_980, 102.0, 1.02)),
                1_000.0,
            ),
            "the saturation number: the elasticity is already",
        ),
    ],
    ids=[
        "L above min(ceiling, supply)",
        "ceiling above maximum use",
        "stalled allocation",
        "capacity per satellite rising",
        "saturation before the first midpoint",
    ],
)
def test_each_check_refuses_a_curve_that_breaks_it(
    refused: Callable[[], object], message: str
) -> None:
    """Objective: the guards fire: each check raises its typed error on a curve breaking it.

    Sample: hand-built snapshots or rows: L above min(ceiling, supply); a ceiling above
    maximum use; L at 0.90 of its bound at 20,022 satellites against the 0.98 floor; capacity
    per satellite rising from 1.0 / 342 to 4.0 / 992; an elasticity of 0.01 at the first
    midpoint (the saturation number cannot be placed).

    Expected outcome: SaturationInvariantError, its message naming the breach.
    """
    with pytest.raises(SaturationInvariantError, match=message):
        refused()


# ---------------------------------------------------------------------------
# The grid loader and the contract
# ---------------------------------------------------------------------------


def test_load_population_grid_reads_the_shipped_grid(real_grid: PopulationGrid) -> None:
    """Objective: the shipped grid loads as ATTRIBUTION.md describes it.

    Sample: ``communications/data/ghs_pop_e2030_0p25deg.npz`` with its recorded SHA-256.

    Expected outcome: 720 x 1440 float32 cells of 0.25 degree from 90 north and 180 west,
    about 8.546 billion people, the file's name, digest, source and citation.
    """
    assert real_grid.population.shape == (720, 1440)
    assert real_grid.population.dtype == np.float32
    assert (real_grid.lat_top_deg, real_grid.lon_left_deg, real_grid.cell_deg) == (
        90.0,
        -180.0,
        0.25,
    )
    assert float(real_grid.population.astype(np.float64).sum()) == pytest.approx(8.546e9, rel=1e-3)
    assert real_grid.file_name == "ghs_pop_e2030_0p25deg.npz"
    assert real_grid.sha256 == POPULATION_GRID_SHA256
    assert "GHS-POP R2023A" in real_grid.source
    assert "Schiavina" in real_grid.citation


@pytest.mark.parametrize("case", ["missing file", "another digest", "not an archive"])
def test_load_population_grid_refuses_a_file_it_cannot_trust(
    tmp_path: Path, repo_dir: Path, case: str
) -> None:
    """Objective: the loader refuses what it cannot read, and a grid that is not the one
    expected, with the typed error the commands report.

    Sample: a path that does not exist; the shipped grid against another digest; a text file
    against its own digest.

    Expected outcome: ModelFileError for the missing file and for the file that is no grid
    archive; PopulationGridError naming both digests for the other digest.
    """
    if case == "missing file":
        with pytest.raises(ModelFileError, match="could not read"):
            load_population_grid(tmp_path / "absent.npz", POPULATION_GRID_SHA256)
    elif case == "another digest":
        other = "0" * 64
        with pytest.raises(PopulationGridError, match=other) as refused:
            load_population_grid(repo_dir / POPULATION_GRID_PATH, other)
        assert POPULATION_GRID_SHA256 in str(refused.value)
    else:
        text = tmp_path / "not_a_grid.npz"
        text.write_bytes(b"not a population grid")
        digest = hashlib.sha256(text.read_bytes()).hexdigest()
        with pytest.raises(ModelFileError, match="not a readable population grid"):
            load_population_grid(text, digest)


def test_saturation_inputs_for_reads_only_the_held_spectrum() -> None:
    """Objective: a config's Iridium dials reach the curve's inputs only through the held
    spectrum; the defaults are the named constants in the class key's order.

    Sample: the default Iridium dials; the same with a 15.4 m^2 panel; the same with 10.5 MHz.

    Expected outcome: the default dials give ``SaturationInputs()``, its classes in
    ``DeviceClass`` order and its band points in ``BandName`` order; the panel changes
    nothing (the engine applies it); the spectrum changes ``spectrum_mhz`` alone, and the
    input hash with it; the hash survives a JSON round trip.
    """
    default = SaturationInputs()
    assert saturation_inputs_for(IridiumDials()) == default
    assert [entry.device_class for entry in default.classes] == list(DeviceClass)
    assert [point.name for point in default.bands] == list(BandName)
    assert saturation_inputs_for(IridiumDials(aperture_m2=15.4)) == default
    wider = saturation_inputs_for(IridiumDials(spectrum_mhz=10.5))
    assert wider == default.model_copy(update={"spectrum_mhz": 10.5})
    assert curve_input_hash(wider) != curve_input_hash(default)
    round_trip = SaturationInputs.model_validate_json(default.model_dump_json())
    assert curve_input_hash(round_trip) == curve_input_hash(default)


@pytest.mark.parametrize(
    "build",
    [
        lambda d: SaturationInputs(classes=tuple(reversed(d.classes))),
        lambda d: SaturationInputs(classes=d.classes[:2]),
        lambda d: SaturationInputs(bands=d.bands[1:]),
        lambda d: SweepInputs(fleets=(500, 340)),
        lambda d: SweepInputs(fleets=(340,)),
        lambda d: SweepInputs(fleets=(340, 50_000)),
        lambda d: SaturationInputs(spectrum_mhz=float("nan")),
        lambda d: SweepInputs(fleets=(True, 340)),
        lambda d: SweepInputs(fleets=(340.0, 500)),
        lambda d: SweepInputs(mounted_terminal_extension=(48_000.0, 64_000)),
    ],
    ids=[
        "classes out of order",
        "a class missing",
        "a band point missing",
        "fleets not increasing",
        "one fleet",
        "the mounted extension below the last fleet",
        "a NaN",
        "a boolean fleet",
        "a whole float fleet",
        "a whole float in the mounted extension",
    ],
)
def test_the_contract_refuses_inputs_out_of_shape(
    build: Callable[[SaturationInputs], object],
) -> None:
    """Objective: the contract's validators hold the inputs to their shape.

    Sample: the default inputs with one rule broken each.

    Expected outcome: a pydantic ValidationError (a ValueError, which the commands report as
    one line).
    """
    with pytest.raises(ValueError, match="validation error"):
        build(SaturationInputs())


TRANSPOSING_REQUESTS = (
    (1_000, (32, 31)),
    (1_500, (39, 38)),
    (2_000, (45, 44)),
    (12_000, (110, 109)),
)
"""The grid's requests whose realized count, requested again, builds the transposed shell."""


def test_a_row_is_rebuilt_from_its_request_never_from_its_key() -> None:
    """Objective: each row carries the request its shell is built from, and the contract
    checks the row's key is that request realized (foundation v2, amendment A5).

    Sample: the grid's requests 1,000, 1,500, 2,000 and 12,000, whose realized counts (992,
    1,482, 1,980, 11,990), requested again, build the transposed shells; rows keyed 992.

    Expected outcome: each request gives its shell and the realized count gives the
    transpose (so the key alone cannot rebuild the row); a row of fleet 992 on request 1,000
    validates; a row of fleet 1,000 on request 1,000 is refused, naming the realized 992.
    """
    for requested, shape in TRANSPOSING_REQUESTS:
        assert walker_shape(requested) == shape
        assert walker_shape(math.prod(shape)) == shape[::-1]
    row = CurveRow.model_validate({**_row(992, 1.0, 1.0).model_dump(), "requested_fleet": 1_000})
    assert (row.fleet, row.requested_fleet) == (992, 1_000)
    with pytest.raises(ValueError, match="1000 realizes as 992"):
        CurveRow.model_validate(
            {**_row(992, 1.0, 1.0).model_dump(), "fleet": 1_000, "requested_fleet": 1_000}
        )


@pytest.mark.parametrize(
    ("share", "separation_deg", "interference_db", "valid"),
    [
        (0.0, None, None, True),
        (0.1, 60.0, -18.0, True),
        (0.0, 60.0, -18.0, False),
        (0.0, None, -18.0, False),
        (0.1, None, None, False),
        (0.1, 60.0, None, False),
    ],
    ids=[
        "nothing stacked, no statistics",
        "stacked, both statistics",
        "nothing stacked, both statistics",
        "nothing stacked, one statistic",
        "stacked, no statistics",
        "stacked, one statistic",
    ],
)
def test_directional_statistics_exist_exactly_when_stacked_beams_are_kept(
    share: float, separation_deg: float | None, interference_db: float | None, valid: bool
) -> None:
    """Objective: a row that keeps no stacked beam has no stacking statistics, never a made-up
    value (foundation v2, amendment A5).

    Sample: a kept stacked share of 0 or 0.1 with each combination of the median separation
    and the mean full-sum interference set or None.

    Expected outcome: valid exactly when both statistics are None at a share of 0, or both set
    at a positive share; otherwise a validation error.
    """

    def build() -> DirectionalDiagnostics:
        return DirectionalDiagnostics(
            kept_stacked_share=share,
            median_separation_deg=separation_deg,
            mean_full_sum_interference_db=interference_db,
        )

    if valid:
        assert build().kept_stacked_share == share
    else:
        with pytest.raises(ValueError, match="exactly when stacked beams are kept"):
            build()


def test_strict_fleets_still_load_from_json() -> None:
    """Objective: the strict integer fleets refuse a boolean or a float, yet a curve's inputs
    still load from their own JSON (a promoted curve's parameters).

    Sample: the default inputs dumped to JSON text and to a JSON-shaped mapping (lists).

    Expected outcome: both load back equal to the default.
    """
    default = SaturationInputs()
    assert SaturationInputs.model_validate_json(default.model_dump_json()) == default
    assert SaturationInputs.model_validate(default.model_dump(mode="json")) == default


def test_capacity_per_satellite_may_rise_within_the_snapshot_noise() -> None:
    """Objective: capacity per satellite may rise between consecutive rows by up to 2 percent
    of the earlier row, the snapshots' noise, and no more (amendment A6).

    Sample: rows at 342 and 992 satellites whose capacity per satellite rises 1.9 and 2.1
    percent.

    Expected outcome: the 1.9 percent rise passes; the 2.1 percent rise raises
    SaturationInvariantError naming the rise.
    """
    per_satellite = 1.0 / 342

    def rows(rise: float) -> tuple[CurveRow, CurveRow]:
        return (_row(342, 10.0, 1.0), _row(992, 10.0, 992 * per_satellite * (1 + rise)))

    sat._check_capacity_per_satellite(PHONE, rows(0.019))
    with pytest.raises(SaturationInvariantError, match="capacity per satellite rises"):
        sat._check_capacity_per_satellite(PHONE, rows(0.021))


# ---------------------------------------------------------------------------
# The pair search against brute force, and every limit element by element
# ---------------------------------------------------------------------------

NARROW_VIEW_SHELL = ShellInputs(altitude_km=300.0, inclination_deg=30.0, elevation_mask_deg=60.0)
"""A shell with a narrow view (about 1.48 degrees): near a pole its view reaches past the
search window's cap latitude while spanning only a few degrees."""

EDGE_SATELLITES_DEG = (
    (90.0, 0.0),
    (-90.0, 45.0),
    (89.99, 123.0),
    (-89.9, -170.0),
    (88.0, 180.0),
    (0.0, -180.0),
    (0.0, 179.9999),
    (45.0, 180.0),
    (85.0, 90.0),
    (60.2, 0.0),
)
"""Hand-placed satellites at the poles, near them, and across the antimeridian, degrees."""

BOUNDARY_SLACK = 1e-12
"""Pairs within this of the view's limit, in cosine, may fall either way under rounding."""


def brute_force_pair_keys(
    satellites: sat._SatellitePositions, cells: sat._DemandCells, limit_rad: float, slack: float
) -> np.ndarray:
    """Every pair whose cosine is at least cos(limit) + slack, by testing every cell against
    every satellite, as sorted keys satellite x (cells + 1) + cell."""
    satellite_xyz = sat._unit_vectors(satellites.lat_rad, satellites.lon_rad)
    cosine = cells.xyz @ satellite_xyz.T
    cell, satellite = np.nonzero(cosine >= math.cos(limit_rad) + slack)
    return np.sort(satellite.astype(np.int64) * (cells.count + 1) + cell)


def everywhere_people(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    """One resident in every cell."""
    return np.ones_like(lat)


@pytest.mark.parametrize(
    "shell", [ShellInputs(), NARROW_VIEW_SHELL], ids=["central", "narrow view"]
)
def test_pair_search_finds_exactly_the_pairs_a_brute_force_search_finds(
    synthetic_population_grid: Callable[[float, PeopleAt], PopulationGrid], shell: ShellInputs
) -> None:
    """Objective: the windowed pair search misses no pair in view and keeps none out of view,
    at the poles and across the antimeridian too; no runtime check could see a miss, since L,
    the ceiling and the supply are built on the same pairs.

    Sample: every 1 degree cell populated; the central shell and a narrow-view shell (300 km,
    a 60 degree mask), each at 400 requested satellites at two times, plus satellites placed
    at and near both poles and across the antimeridian.

    Expected outcome: the pairs equal a brute-force search over every cell and satellite, up
    to pairs within 1e-12 of the limit in cosine, each listed once, ordered by satellite then
    cell.
    """
    cells = sat._demand_cells(synthetic_population_grid(1.0, everywhere_people), 1e-12)
    limit = sat._central_angle_limit(shell)
    shells = [sat._walker_positions(shell, 400, time_s) for time_s in (0.0, 4321.0)]
    edges = satellites_at(EDGE_SATELLITES_DEG)
    satellites = sat._SatellitePositions(
        lat_rad=np.concatenate([part.lat_rad for part in (*shells, edges)]),
        lon_rad=np.concatenate([part.lon_rad for part in (*shells, edges)]),
    )
    pairs = sat._pairs_in_view(satellites, cells, limit)
    found = pairs.satellite * (cells.count + 1) + pairs.cell
    assert np.all(np.diff(found) > 0)
    surely_in = brute_force_pair_keys(satellites, cells, limit, BOUNDARY_SLACK)
    maybe_in = brute_force_pair_keys(satellites, cells, limit, -BOUNDARY_SLACK)
    assert np.setdiff1d(surely_in, found).size == 0
    assert np.setdiff1d(found, maybe_in).size == 0


def test_every_limit_holds_satellite_by_satellite_and_cell_by_cell(
    real_grid: PopulationGrid,
) -> None:
    """Objective: no limit is broken where the totals would hide it: no satellite over B, no
    cell over its area or its people cap, no pair over one layer, no negative beam.

    Sample: the shipped grid at the investor's usage, 992 satellites (requested 1,000) at one
    time, B = 150.

    Expected outcome: per satellite at most B, and some satellite at B (the limit binds); per
    cell at most its area and its people cap; per pair at most one layer (1e-9 relative); no
    negative beam; L the sum of the pairs' beams and at most min(ceiling, supply).
    """
    cells = sat._demand_cells(real_grid, SaturationInputs().demand.density_threshold_per_km2)
    limits = seam_limits(150.0)
    satellites = sat._walker_positions(SaturationInputs().shell, 1_000, 1_111.0)
    allocation = sat._allocate(satellites, cells, limits)
    beams = allocation.beams
    assert np.all(beams >= 0)
    per_satellite = np.bincount(allocation.satellite, weights=beams, minlength=satellites.count)
    assert per_satellite.max() <= 150.0 * (1 + 1e-9)
    assert per_satellite.max() == pytest.approx(150.0, rel=1e-9)
    footprint = allocation.footprint_km2
    covered = np.bincount(allocation.cell, weights=beams * footprint, minlength=cells.count)
    assert np.all(covered <= cells.area_km2 * (1 + 1e-9))
    per_cell = np.bincount(allocation.cell, weights=beams, minlength=cells.count)
    assert np.all(per_cell <= cells.people / PHONE_PEOPLE_PER_BEAM * (1 + 1e-9) + 1e-12)
    assert np.all(beams * footprint / cells.area_km2[allocation.cell] <= 1 + 1e-9)
    assert allocation.useful_beams == pytest.approx(float(beams.sum()), rel=1e-12)
    assert allocation.useful_beams <= min(allocation.ceiling_beams, allocation.supply_beams)


def rows_with_elasticities(
    fleets: tuple[int, ...], elasticities: tuple[float, ...], useful_beams: tuple[float, ...]
) -> tuple[CurveRow, ...]:
    """Rows at the given fleets whose capacity has the given elasticity over each interval."""
    capacity = [100.0]
    for (low, high), elasticity in zip(pairwise(fleets), elasticities, strict=True):
        capacity.append(capacity[-1] * (high / low) ** elasticity)
    return tuple(
        _row(fleet, useful, value)
        for fleet, useful, value in zip(fleets, useful_beams, capacity, strict=True)
    )


MARKER_FLEETS = (342, 992, 1_980, 3_969)
"""Fleets for the hand-built marker rows (each realizes as itself when requested)."""


def test_a_supporting_marker_before_the_first_row_never_takes_the_saturation_number() -> None:
    """Objective: the saturation number is placed first and is the one marker that refuses a
    curve; a supporting marker the rows cannot place is None, and the curve's limits say so
    (the numerics review's m2); a supporting marker the rows can place is placed, with no
    limit.

    Sample: rows whose elasticity falls 0.20, 0.12, 0.02 (under 0.25 already at the first
    midpoint, crossing 0.10 between the second and third), with L at 950, 960, 970 and 980
    beams against a maximum use of 1,000 (90 percent reached at the first row); then the same
    elasticities with L far under 90 percent.

    Expected outcome: the saturation number is placed (between the second and third
    midpoints); the 0.25 marker and the 90 percent fleet are None; the unplaced-marker limits
    name both; with L under 90 percent at the first row, only the 0.25 limit is stated. Rows
    falling 0.40, 0.20, 0.05 with L under 90 percent place the 0.25 marker between the first
    two midpoints (the crossing's value rounded half up), the saturation number between the
    second and third, and state no limit.
    """
    elasticities = (0.20, 0.12, 0.02)
    rows = rows_with_elasticities(MARKER_FLEETS, elasticities, (950.0, 960.0, 970.0, 980.0))
    markers = sat._markers(PHONE, rows, 1_000.0)
    midpoints = [math.sqrt(low * high) for low, high in pairwise(MARKER_FLEETS)]
    assert markers.saturation_number is not None
    assert midpoints[1] < markers.saturation_number < midpoints[2]
    assert markers.elasticity_under_0p25_fleet is None
    assert markers.fleet_at_90pct_of_maximum_use is None
    limits = sat._unplaced_marker_limits(PHONE, rows, 1_000.0)
    assert len(limits) == 2
    assert limits[0].startswith("The phone class's crossing under 0.25 lies before the first")
    assert "first midpoint (the geometric mean of the first two rows), where the rows" in limits[0]
    assert "at or before the first row" in limits[1]
    low_rows = rows_with_elasticities(MARKER_FLEETS, elasticities, (100.0, 200.0, 300.0, 400.0))
    assert len(sat._unplaced_marker_limits(PHONE, low_rows, 1_000.0)) == 1
    placed_rows = rows_with_elasticities(
        MARKER_FLEETS, (0.40, 0.20, 0.05), (100.0, 200.0, 300.0, 400.0)
    )
    placed = sat._markers(PHONE, placed_rows, 1_000.0)
    module_midpoints, module_elasticity = sat._elasticity(PHONE, placed_rows)
    crossing = sat._first_crossing_under(module_midpoints, module_elasticity, 0.25, "0.25")
    assert crossing is not None
    assert placed.elasticity_under_0p25_fleet == round_half_up(crossing)
    assert midpoints[0] < placed.elasticity_under_0p25_fleet < midpoints[1]
    assert placed.saturation_number is not None
    assert midpoints[1] < placed.saturation_number < midpoints[2]
    assert sat._unplaced_marker_limits(PHONE, placed_rows, 1_000.0) == ()


def bare_markers(**changes: int | None) -> ClassMarkers:
    """Markers with no crossing (not reached by 992), but for the changes asked."""
    fields: dict[str, float | int | None] = {
        "maximum_use_beams": 1_000.0,
        "saturation_number": None,
        "saturation_not_reached_by": 992,
        "elasticity_under_0p25_fleet": None,
        "fleet_at_90pct_of_maximum_use": None,
    }
    return ClassMarkers.model_validate({**fields, **changes})


BARE_ROWS = (_row(342, 10.0, 1.0), _row(992, 20.0, 2.0))
"""Two valid rows, 342 and 992 satellites."""


def bare_class_curve(
    device_class: DeviceClass, rows: tuple[CurveRow, ...] = BARE_ROWS
) -> ClassCurve:
    """A class curve on the bare rows and markers."""
    return ClassCurve(device_class=device_class, rows=rows, markers=bare_markers())


def bare_band_curve(name: BandName, rows: tuple[CurveRow, ...] = BARE_ROWS) -> BandCurve:
    """A band point's curve (its default point) on the bare rows and markers."""
    (point,) = [entry for entry in SaturationInputs().bands if entry.name is name]
    return BandCurve(point=point, rows=rows, markers=bare_markers())


def bare_curve(classes: tuple[ClassCurve, ...], bands: tuple[BandCurve, ...]) -> SaturationCurve:
    """A curve of the default inputs holding the given class and band curves."""
    inputs = SaturationInputs()
    return SaturationCurve(
        schema_version=SATURATION_CURVE_SCHEMA_VERSION,
        version_stamp=STAMP,
        parameters=inputs,
        input_hash=curve_input_hash(inputs),
        provenance=CurveProvenance(
            grid_file_name="ghs_pop_e2030_0p25deg.npz",
            grid_sha256=POPULATION_GRID_SHA256,
            citations=(),
            licence="CC BY 4.0",
            method="test",
            checks_passed=(),
            run_measurement=RunMeasurement(wall_time_s=0.0, peak_memory_mb=0.0),
        ),
        classes=classes,
        bands=bands,
        limits=(),
    )


def test_a_curve_built_in_order_validates() -> None:
    """Objective: the curve-side validators accept what the contract allows, so their
    refusals below are refusals of the broken rule alone.

    Sample: the three classes in the class key's order and two band points in their order,
    each on two increasing rows; and a curve with no class or band yet (a curve being built).

    Expected outcome: both validate, the classes small terminal, mounted terminal, phone class.
    """
    curve = bare_curve(
        tuple(bare_class_curve(device_class) for device_class in DeviceClass),
        (bare_band_curve(BandName.TAPER), bare_band_curve(BandName.BEAMS_48)),
    )
    assert [entry.device_class for entry in curve.classes] == list(DeviceClass)
    assert bare_curve((), ()).classes == ()


@pytest.mark.parametrize(
    "build",
    [
        lambda: bare_curve((bare_class_curve(PHONE), bare_class_curve(PHONE)), ()),
        lambda: bare_curve(
            (bare_class_curve(PHONE), bare_class_curve(DeviceClass.SMALL_TERMINAL_CLASS)), ()
        ),
        lambda: bare_curve(
            (), (bare_band_curve(BandName.BEAMS_48), bare_band_curve(BandName.TAPER))
        ),
        lambda: bare_class_curve(PHONE, (BARE_ROWS[1], BARE_ROWS[0])),
        lambda: bare_band_curve(BandName.TAPER, (BARE_ROWS[0], BARE_ROWS[0])),
        lambda: bare_markers(saturation_number=20_000),
        lambda: bare_markers(saturation_not_reached_by=None),
    ],
    ids=[
        "a class twice",
        "classes out of the class key's order",
        "band points out of their order",
        "a class's rows falling",
        "a band's rows repeating",
        "markers with both saturation readings",
        "markers with neither saturation reading",
    ],
)
def test_the_contract_refuses_a_curve_out_of_shape(build: Callable[[], object]) -> None:
    """Objective: the curve-side validators of the frozen contract hold (p3, p4 and p6 edit
    the contract, and a broken validator would go unseen).

    Sample: the bare curve above with one rule broken each.

    Expected outcome: a pydantic ValidationError (a ValueError).
    """
    with pytest.raises(ValueError, match="validation error"):
        build()


def test_compute_saturation_refuses_requests_that_realize_one_row(
    uniform_band: PopulationGrid, synthetic_saturation_inputs: SaturationInputsBuilder
) -> None:
    """Objective: requests that strictly increase but realize the same P x S are refused
    before any computation, since each row is keyed by its realized fleet.

    Sample: the uniform band's inputs at the requests 992 and 993, both 31 x 32 = 992.

    Expected outcome: SaturationInvariantError naming both, the realized fleets not strictly
    increasing.
    """
    inputs = synthetic_saturation_inputs(uniform_band, fleets=(992, 993))
    with pytest.raises(SaturationInvariantError, match="do not strictly increase"):
        compute_saturation(inputs, uniform_band, version_stamp=STAMP)


def test_compute_saturation_refuses_a_grid_that_is_not_global(
    uniform_band: PopulationGrid, synthetic_saturation_inputs: SaturationInputsBuilder
) -> None:
    """Objective: the pair search wraps longitudes and clips at the poles, so the curve is
    computed only on a global grid from 90 degrees north.

    Sample: the uniform band's grid and digest, its northern edge moved to 89.75 degrees.

    Expected outcome: PopulationGridError asking for a global grid from 90 degrees north.
    """
    shifted = dataclasses.replace(uniform_band, lat_top_deg=89.75)
    inputs = synthetic_saturation_inputs(uniform_band, fleets=BAND_FLEETS)
    with pytest.raises(PopulationGridError, match="global grid from 90 degrees north"):
        compute_saturation(inputs, shifted, version_stamp=STAMP)


def test_load_population_grid_names_a_missing_member_once(tmp_path: Path) -> None:
    """Objective: the loader's own refusal of a malformed archive reaches the caller as it
    was raised, never caught and wrapped again by the parse errors' handler.

    Sample: an ``.npz`` holding only a population array, against its own digest.

    Expected outcome: ModelFileError naming the missing members, its message the path once
    and the reason, with no "not a readable population grid" wrapper.
    """
    archive = tmp_path / "population_only.npz"
    np.savez(archive, population=np.zeros((2, 2), dtype=np.float32))
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    with pytest.raises(ModelFileError, match="the population grid lacks") as refused:
        load_population_grid(archive, digest)
    message = str(refused.value)
    assert "not a readable population grid" not in message
    assert message.count(str(archive)) == 1


# ---------------------------------------------------------------------------
# The sky sectors (rule D1), the pairs' sky geometry and the pair search's chunks
# ---------------------------------------------------------------------------

SMALL = DeviceClass.SMALL_TERMINAL_CLASS
"""The small terminal, the first directional class."""

MOUNTED = DeviceClass.MOUNTED_TERMINAL_CLASS
"""The mounted terminal, the second directional class."""

MASK_DEG = SaturationInputs().shell.elevation_mask_deg
"""The default elevation mask, 25 degrees."""


def class_inputs(device_class: DeviceClass) -> ClassInputs:
    """A class's default inputs."""
    return next(entry for entry in SaturationInputs().classes if entry.device_class is device_class)


def satellite_seen_at(
    cell_deg: tuple[float, float], elevation_deg: float, azimuth_deg: float, shell: ShellInputs
) -> tuple[float, float]:
    """The sub-satellite point, (latitude, longitude) degrees, of a satellite that a cell centre
    sees at the given elevation and azimuth (from north through east): the point at the central
    angle of that elevation, along the great circle leaving the cell at that bearing."""
    orbit = EARTH_RADIUS_KM + shell.altitude_km
    elevation = math.radians(elevation_deg)
    central = math.acos(EARTH_RADIUS_KM * math.cos(elevation) / orbit) - elevation
    lat1, lon1 = math.radians(cell_deg[0]), math.radians(cell_deg[1])
    azimuth = math.radians(azimuth_deg)
    lat2 = math.asin(
        math.sin(lat1) * math.cos(central) + math.cos(lat1) * math.sin(central) * math.cos(azimuth)
    )
    lon2 = lon1 + math.atan2(
        math.sin(azimuth) * math.sin(central) * math.cos(lat1),
        math.cos(central) - math.sin(lat1) * math.sin(lat2),
    )
    return math.degrees(lat2), math.degrees(lon2)


@pytest.mark.parametrize(
    ("device_class", "edges_deg"), [(SMALL, (53.9, 25.0)), (MOUNTED, (69.4, 48.0, 25.0))]
)
def test_sky_sectors_split_the_sky_above_the_mask_into_equal_solid_angles(
    device_class: DeviceClass, edges_deg: tuple[float, ...]
) -> None:
    """Objective: rule D1: a directional terminal's sky above the mask splits into sectors of
    equal solid angle, ring by ring from the zenith, the last ring ending exactly at the mask.

    Sample: each directional class's default wedges per ring, (1, 2) and (1, 3, 5), at the
    default 25 degree mask.

    Expected outcome: the strategy's ring edges (the small terminal's cap above 53.9 degrees;
    the mounted terminal's cap above 69.4 and its ring of 3 down to 48.0), within 0.05 degree,
    the last edge exactly the mask; every sector's solid angle, 2 pi (sin(top) - sin(bottom))
    over its ring's wedges, equal to the sky's 2 pi (1 - sin 25 degrees) over the sector count
    (1e-12 relative).
    """
    wedges = class_inputs(device_class).sector_wedges_per_ring
    layout = sat._sector_layout(wedges, MASK_DEG)
    assert [math.degrees(edge) for edge in layout.lower_edges_rad] == pytest.approx(
        edges_deg, abs=0.05
    )
    assert layout.lower_edges_rad[-1] == math.radians(MASK_DEG)
    assert layout.count == sum(wedges)
    sky_per_sector = 2 * math.pi * (1 - math.sin(math.radians(MASK_DEG))) / sum(wedges)
    tops = (math.pi / 2, *layout.lower_edges_rad[:-1])
    for top, bottom, count in zip(tops, layout.lower_edges_rad, wedges, strict=True):
        solid_angle = 2 * math.pi * (math.sin(top) - math.sin(bottom)) / count
        assert solid_angle == pytest.approx(sky_per_sector, rel=1e-12)


def test_a_direction_falls_in_its_ring_by_elevation_then_its_azimuth_wedge() -> None:
    """Objective: rule D1's assignment: a direction's sector is its ring by elevation (each
    ring's lower edge included), then its equal azimuth wedge counted from north through east.

    Sample: the mounted terminal's layout (a cap; a ring of 3 wedges of 120 degrees down to
    48.0 degrees; a ring of 5 wedges of 72 degrees down to the mask), its sectors numbered from
    the cap (0), the ring of 3 (1 to 3), the ring of 5 (4 to 8); directions at the zenith, on
    and a hair under each lower edge, either side of wedge boundaries, and a hair under the
    mask (rounding at the view's limit).

    Expected outcome: the zenith 0; on the cap's lower edge at 200 degrees 0, a hair under it
    2; at 60 degrees elevation, azimuth 0 gives 1, 239.9 gives 2 and 240.1 gives 3; on the ring
    of 3's lower edge at 359 degrees, 3; at 30 degrees elevation, 71.9 gives 4, 72.1 gives 5
    and 359.9 gives 8; on the mask at 144.1 degrees, 6; a hair under it at 300 degrees, 8.
    """
    layout = sat._sector_layout(class_inputs(MOUNTED).sector_wedges_per_ring, MASK_DEG)
    cap_edge, ring_edge, mask = layout.lower_edges_rad
    hair = 1e-9
    cases = (
        (math.pi / 2, 0.0, 0),
        (cap_edge, 200.0, 0),
        (cap_edge - hair, 200.0, 2),
        (math.radians(60.0), 0.0, 1),
        (math.radians(60.0), 239.9, 2),
        (math.radians(60.0), 240.1, 3),
        (ring_edge, 359.0, 3),
        (math.radians(30.0), 71.9, 4),
        (math.radians(30.0), 72.1, 5),
        (math.radians(30.0), 359.9, 8),
        (mask, 144.1, 6),
        (mask - hair, 300.0, 8),
    )
    elevation = np.array([case[0] for case in cases])
    azimuth = np.radians([case[1] for case in cases])
    assert sat._sector_of(elevation, azimuth, layout).tolist() == [case[2] for case in cases]


SKY_DIRECTIONS_DEG = ((90.0, 0.0), (60.0, 10.0), (60.0, 130.0), (30.0, 200.0), (27.0, 75.0))
"""Directions (elevation, azimuth from north) at which the sky-geometry test places its
satellites, as the patch's cell centre sees them."""


def test_each_pair_sees_its_satellite_in_its_sector_at_the_true_angles(
    synthetic_population_grid: GridBuilder,
) -> None:
    """Objective: the pairs' sky geometry: the elevation and azimuth a cell sees each satellite
    at place the pair in its sector (rule D1), and the angle between two satellites seen from a
    cell is the true one (the separations of rule D4 and the gains of rule D5).

    Sample: one populated 0.25 degree cell; five satellites placed where its centre sees them at
    (elevation, azimuth) (90, 0), (60, 10), (60, 130), (30, 200) and (27, 75) degrees; the
    mounted terminal's sectors.

    Expected outcome: each pair's sector is that of its intended direction (0, 1, 2, 6 and 5);
    the angle between every two of them, from the pairs' directions, equals the spherical
    angle between their intended directions, cos = sin e1 sin e2 + cos e1 cos e2 cos(a1 - a2),
    within 1e-9 radian.
    """
    grid = synthetic_population_grid(0.25, patch_people(0.25, 0))
    cells = sat._demand_cells(grid, 1.0)
    shell = SaturationInputs().shell
    centre = (float(np.degrees(cells.lat_rad[0])), float(np.degrees(cells.lon_rad[0])))
    satellites = satellites_at(
        [satellite_seen_at(centre, el, az, shell) for el, az in SKY_DIRECTIONS_DEG]
    )
    beam = sat._beam_model(shell)
    pairs = sat._pairs_in_view(satellites, cells, beam.max_central_angle_rad)
    assert pairs.satellite.tolist() == list(range(len(SKY_DIRECTIONS_DEG)))
    layout = sat._sector_layout(class_inputs(MOUNTED).sector_wedges_per_ring, MASK_DEG)
    intended = sat._sector_of(
        np.radians([el for el, _ in SKY_DIRECTIONS_DEG]),
        np.radians([az for _, az in SKY_DIRECTIONS_DEG]),
        layout,
    )
    assert intended.tolist() == [0, 1, 2, 6, 5]
    sectors = sat._pair_sectors(pairs, satellites, cells, beam.orbit_radius_km, layout)
    assert sectors.tolist() == intended.tolist()
    directions = sat._pair_directions(pairs, satellites, cells, beam.orbit_radius_km).of(
        np.arange(pairs.satellite.size)
    )
    for (u, (e1, a1)), (v, (e2, a2)) in combinations(enumerate(SKY_DIRECTIONS_DEG), 2):
        e1, a1, e2, a2 = (math.radians(angle) for angle in (e1, a1, e2, a2))
        expected = math.acos(
            math.sin(e1) * math.sin(e2) + math.cos(e1) * math.cos(e2) * math.cos(a1 - a2)
        )
        found = math.acos(min(1.0, float(directions[u] @ directions[v])))
        assert found == pytest.approx(expected, abs=1e-9)


WIDE_VIEW_SHELL = ShellInputs(altitude_km=1200.0, inclination_deg=70.0, elevation_mask_deg=5.0)
"""A wide-view shell (about a 28 degree view): near a pole its search windows span every
column, the pair search's worst case for memory (the p1 review's scenario S1.8)."""

LOWERED_CHUNK_ELEMENTS = 700_000
"""A lowered element budget: two of the wide view's polar windows (229 rows x 1,441 columns,
about 330,000 elements each) to a chunk."""

BYTES_PER_WINDOW_ELEMENT = 80
"""The pair search's working memory per window element at the worst, every window cell a
demand cell (measured with tracemalloc at about 70 bytes, 80 with the pairs found)."""

BYTES_PER_PAIR_FOUND = 120
"""The memory a pair found holds by the end of the search: its satellite, cell and angle as
found and as kept, and the deduplication's keys and sort (measured at about 107 bytes)."""


def test_the_pair_search_chunks_hold_their_element_budget_and_change_no_pair(
    synthetic_population_grid: GridBuilder, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Objective: the pair search's chunks bound its working memory (the p1 review's scenario
    S1.8): every chunk's windows hold at most the element budget, and chunking changes no pair.

    Sample: every 0.25 degree cell populated (every window cell a demand cell, the worst case
    for memory); the wide-view shell (1,200 km, a 5 degree mask), whose view near a pole spans
    the whole turn of longitude; 8 satellites at 70 degrees north; the budget lowered to
    700,000 elements; then the central shell at 5,400 requested satellites at the default
    budget.

    Expected outcome: the wide view's chunks tile the satellites in order, two to a chunk, each
    within the lowered budget; the pairs equal those of one unbudgeted chunk; the traced peak
    stays within 80 bytes a budgeted element plus 120 bytes a pair found, which one chunk of
    all eight windows (2.6 million elements) would break; the central shell keeps chunks of
    500 satellites (the last 402), well within the default budget.
    """
    cells = sat._demand_cells(synthetic_population_grid(0.25, everywhere_people), 1e-12)
    limit = sat._central_angle_limit(WIDE_VIEW_SHELL)
    satellites = satellites_at([(70.0, lon) for lon in np.linspace(-170.0, 170.0, 8)])
    window_rows = 2 * sat._window_half_rows(cells, limit) + 1
    monkeypatch.setattr(sat, "_PAIR_SEARCH_CHUNK_ELEMENTS", 10**12)
    unbudgeted = sat._pairs_in_view(satellites, cells, limit)
    monkeypatch.setattr(sat, "_PAIR_SEARCH_CHUNK_ELEMENTS", LOWERED_CHUNK_ELEMENTS)
    chunks = sat._search_chunks(satellites, cells, limit)
    assert [(start, stop) for start, stop, _ in chunks] == [(0, 2), (2, 4), (4, 6), (6, 8)]
    for start, stop, half_cols in chunks:
        assert (stop - start) * window_rows * (2 * half_cols + 1) <= LOWERED_CHUNK_ELEMENTS
    tracemalloc.start()
    budgeted = sat._pairs_in_view(satellites, cells, limit)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    for field in ("satellite", "cell", "central_angle_rad"):
        assert np.array_equal(getattr(budgeted, field), getattr(unbudgeted, field))
    bound = (
        LOWERED_CHUNK_ELEMENTS * BYTES_PER_WINDOW_ELEMENT
        + budgeted.satellite.size * BYTES_PER_PAIR_FOUND
    )
    one_chunk = satellites.count * window_rows * (2 * chunks[0][2] + 1)
    assert peak <= bound < one_chunk * BYTES_PER_WINDOW_ELEMENT
    monkeypatch.undo()
    central = sat._walker_positions(SaturationInputs().shell, 5_400, 0.0)
    central_chunks = sat._search_chunks(
        central, cells, sat._central_angle_limit(SaturationInputs().shell)
    )
    assert [stop - start for start, stop, _ in central_chunks] == [500] * 10 + [402]
