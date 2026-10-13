"""End-to-end and seam tests of the saturation module and its contract (every class).

The saturation curve (``communications.saturation``, the one module that imports numpy)
counts how many co-channel beams a Walker shell keeps lit over people as the fleet grows, for
the small terminal, the mounted terminal and the phone class; its contract
(``communications.saturation_curve``) is numpy-free. These tests are the module's executable
specification, each naming what it exercises and what counts as success:

* through ``compute_saturation`` on synthetic global grids (a few fleets, one snapshot): a
  uniform band, where the supply bound is the time fraction over land and the 0.10 crossing
  is not reached; a two-band world, where maximum use matches its closed form; a dense
  mid-latitude band swept twice, where the 90 percent fleet reads maximum use, never a
  sweep's last ceiling; capacity that never falls between rows; determinism; and a world
  at one shared usage, where the classes order in aggregate and the sector-rule ceiling
  bounds every directional row;
* through the private seam ``_allocate`` with explicit satellite positions: one patch under
  one overhead satellite; the per-cell area and one-layer-per-pair invariants; and the
  directional rules: the serving set at f_serve, the pairwise admission, same-sector
  satellites exempt, the full-sum price against its closed form, the keep rule, the
  sector-rule ceiling and the first layer at each class's own people cap;
* the sky sectors (rule D1), the pairs' sky geometry, the pair search's chunk budget, and the
  vectorized admission against the rule taken candidate by candidate;
* the interference trim against its closed form (the horizon rule included), and each band
  point's one changed input (the beam, B, the demand threshold, the 2 x 2 grid);
* the real grid at a coarse, fast setting, every class and band point frozen at 1e-4
  relative, the phone class's trim with them;
* the committed curve against the code (the drift tests): every class's check rows and each
  band point's first row rebuilt through the drift seams, and every class's and band point's
  maximum use through the curve's own plans, at 1e-4, and its markers, limits and texts
  re-derived exactly; the coarse promotion, byte-identical but for its measurement; the curve
  loader's refusals; the saturation command's refusals and its writes (over an existing curve,
  under missing folders, a relative output anchored at the repository root);
* the markers' rules worked by hand: the first crossing under 0.10, interpolated in ln N
  (1,046 on rows at 342, 992 and 1,980; an elasticity of exactly 0.10 no crossing), a
  saturation number not reached named by the rows' last midpoint (2,803), and the crossings
  refused when capacity falls between rows or the elasticity crosses back over a threshold;
* the sweep's schedule: the memory tiers change no number, the worker count takes each
  worker at its reading times the margin (worked by hand), and every task runs in a fresh
  worker of its own, a pool's bound the sum of its largest task peaks, as many as its workers;
* numpy confinement (a subprocess), the people-per-beam arithmetic, the class constants,
  the checks' refusals, the grid loader's refusals and the contract's validators;
* the engine's side of the curve: the identity check, which names the first field of a run's
  inputs that differs from the curve's parameters, and the readings' edge rules (a row's own
  values at a row, log-log between rows, linear through the origin below the first row, no
  beams and no ocean factor at a fleet of 0, refused past a class's last row), on the
  committed curve and on hand-built ones.

Every synthetic world also passes the module's own checks (the bounds at every snapshot,
capacity per satellite never rising), so each is shaped for it: its capacity per satellite
falls between its rows for a physical reason (a people cap or the tiling binding), never by
the noise of one snapshot. The worlds' grids come from ``synthetic_population_grid`` and
their inputs from ``synthetic_saturation_inputs`` (``conftest.py``), without the mounted
terminal's extension and with the band points at the central values (``small_sweep``,
``central_bands``), so each band point's curve repeats the central one there.
"""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import logging
import math
import os
import pickle
import stat
import subprocess
import sys
import tracemalloc
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from enum import StrEnum
from functools import partial
from itertools import combinations, pairwise
from multiprocessing.context import BaseContext
from pathlib import Path
from typing import Protocol, assert_never

import numpy as np
import pytest
from pydantic import ValidationError

from common.cadence import round_half_up
from common.cli import EXIT_ERROR, EXIT_OK, EXIT_USAGE, describe_failure
from common.file_io import (
    ARTIFACT_FILE_END,
    ModelFileError,
    PendingWrite,
    SourceCheckout,
    render_artifact_json,
    write_files_with_rollback,
)
from communications import iridium, saturation_curve
from communications import saturation as sat
from communications.config import CommsConfig, IridiumDials, load_comms_config
from communications.constants import (
    APERTURE_M2_DEFAULT,
    CLASS_SE_CENTRAL,
    CLASS_USAGE,
    DOWNLINK_SHARE_DEFAULT,
    GBPS_TO_MBPS,
    PANEL_RULE_LIMITS_NOTE,
    POPULATION_GRID_PATH,
    POPULATION_GRID_SHA256,
    SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
    DeviceClass,
)
from communications.iridium import NotAnIridiumConfigError, iridium_dials_of
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
    BandPoint,
    ClassCurve,
    ClassInputs,
    ClassMarkers,
    CurveBeyondLastRowError,
    CurveProvenance,
    CurveRow,
    DirectionalDiagnostics,
    FleetReading,
    RunMeasurement,
    SaturationCurve,
    SaturationCurveError,
    SaturationCurveMismatchError,
    SaturationInputs,
    ShellInputs,
    SweepInputs,
    TrimAtFloor,
    TrimInputs,
    capacity_gbps_at,
    check_curve_complete,
    check_curve_matches,
    curve_input_hash,
    load_saturation_curve,
    people_at,
    read_fleet,
    saturation_inputs_for,
    useful_beams_at,
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
"""The phone class, which takes one co-channel layer."""

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


def central_bands(inputs: SaturationInputs) -> SaturationInputs:
    """The inputs with every band point at the central values (each keeps its name) and the
    bands at the phone class's central snapshots, so on a synthetic world each band point's
    curve repeats the central one.

    The synthetic worlds are shaped for the central curve's checks; the band points' own
    inputs (a 10 or 100 per km^2 threshold, 48 beams) would empty a synthetic world's demand
    or flatten its curve before the markers can place a crossing. The band points' changed
    inputs are tested at the seam and on the real grid.
    """
    points = [
        BandPoint(
            name=point.name,
            beamwidth_factor=inputs.shell.beamwidth_factor,
            spacing_area_factor=1.0,
            density_threshold_per_km2=inputs.demand.density_threshold_per_km2,
            grid_aggregation=1,
            beams_per_satellite=None,
        ).model_dump()
        for point in inputs.bands
    ]
    sweep = {**inputs.sweep.model_dump(), "snapshots_bands": inputs.sweep.snapshots_phone_central}
    return SaturationInputs.model_validate({**inputs.model_dump(), "bands": points, "sweep": sweep})


def small_sweep(inputs: SaturationInputs, snapshots_directional: int = 1) -> SaturationInputs:
    """The inputs with no mounted-terminal extension, the directional classes at the given
    snapshots and the band points at the central values (:func:`central_bands`), so a
    synthetic world's curve stays small and fast."""
    sweep = SweepInputs.model_validate(
        {
            **inputs.sweep.model_dump(),
            "mounted_terminal_extension": (),
            "snapshots_directional": snapshots_directional,
        }
    )
    return central_bands(inputs.model_copy(update={"sweep": sweep}))


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


def test_a_class_whose_crossing_is_not_reached_reports_its_last_measured_midpoint(
    uniform_band_curve: SaturationCurve,
) -> None:
    """Objective: a curve whose elasticity has not fallen under 0.10 at any midpoint reports no
    saturation number, and names as the fleet it is not reached by the last fleet its rows
    measure the elasticity at, never the last row's fleet (ADR 005).

    Sample: the uniform band's curve (fleets 992 and 10,000), whose capacity still grows
    with an elasticity well above 0.10 between its two rows.

    Expected outcome: no saturation number; ``saturation_not_reached_by`` is the rows' one
    midpoint, sqrt(992 x 10,000) = 3,149.6, rounded half up to 3,150; no crossing under 0.25
    either.
    """
    rows = phone_curve(uniform_band_curve).rows
    markers = phone_curve(uniform_band_curve).markers
    low, high = rows
    elasticity = math.log(high.capacity_gbps / low.capacity_gbps) / math.log(high.fleet / low.fleet)
    assert elasticity > 0.25
    assert markers.saturation_number is None
    assert markers.saturation_not_reached_by == round_half_up(math.sqrt(992 * 10_000)) == 3_150
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


def test_capacity_never_falls_between_rows_on_any_curve(
    mid_band_curves: tuple[SaturationCurve, ...],
    uniform_band_curve: SaturationCurve,
    two_band_world_curve: SaturationCurve,
) -> None:
    """Objective: capacity grows with the fleet, or holds, on every class's curve and every band
    point's (the markers' crossings rest on it, and the computation refuses a curve whose capacity
    falls).

    Sample: every synthetic curve here: the dense band's two sweeps, the uniform band and the
    two-band world, each with its three classes and six band points.

    Expected outcome: on every curve each row's capacity is at least the row before it.
    """
    for curve in (*mid_band_curves, uniform_band_curve, two_band_world_curve):
        every_curve = (*(entry.rows for entry in curve.classes), *(b.rows for b in curve.bands))
        for rows in every_curve:
            for earlier, later in pairwise(rows):
                assert later.capacity_gbps >= earlier.capacity_gbps


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
one 0.14 degree off it (over the patch's centre cell, in the overhead satellite's footprint
band, so the two share that cell), three farther out."""


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
    could take 289, so the satellite's 150 beams bind. The supply reads L; the ceiling reads the
    cell's room at the overhead footprint, cell area / 170.8 km^2 (4.5 and 289 beams), since no
    people cap binds.
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
    assert allocation.ceiling_beams == pytest.approx(area / overhead_footprint, rel=1e-9)


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


TRIM_CASE_LATITUDE_DEG = 0.125
"""The trim cases' cells sit on the equator's first row: 0.25 degree cells centred at 0.125
degrees north."""

TRIM_CASE_FIRST_LONGITUDE_DEG = 0.125
"""The first trim-case cell's centre longitude; the second cell lies east of it."""


def cells_people(centres_deg: Sequence[tuple[float, float]]) -> PeopleAt:
    """People in the given 0.25 degree cells only (far above any people cap), by centre."""

    def people(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
        inside = np.zeros(lat.shape, dtype=bool)
        for centre_lat, centre_lon in centres_deg:
            inside |= (np.abs(lat - centre_lat) < 0.125) & (np.abs(lon - centre_lon) < 0.125)
        return np.where(inside, DENSE_PEOPLE_PER_CELL, 0.0)

    return people


@pytest.mark.parametrize(
    ("separation_deg", "leaks"),
    [(22.0, False), (10.0, True)],
    ids=["below the horizon", "above the horizon, off axis"],
)
def test_the_trim_is_its_closed_form_and_drops_satellites_below_the_horizon(
    synthetic_population_grid: GridBuilder, separation_deg: float, leaks: bool
) -> None:
    """Objective: the interference trim (stage 12) prices each victim's aggregate leak by power
    control, the slant range squared over cos^1.3 of the scan angle and the gain toward the
    victim at that angle, and counts only the lit satellites above the victim's horizon.

    Sample: two 0.25 degree cells on the equator, 22 or 10 degrees of longitude apart, each under a
    satellite placed exactly over its centre, the phone allocation (each cell's area binds: about
    4.5 beams each, every beam overhead its own cell), the default trim settings (both cells are
    the victims, since 2 is under 3,000). At 22 degrees each satellite stands below the other
    cell's horizon (a 450 km shell's horizon stands 20.9 degrees away), though scanned under 90
    degrees toward it; at 10 degrees it stands above it, out of view of the other cell (the 25
    degree mask's 7.2 degrees), so it leaks into the other cell off axis.

    Expected outcome: a victim's own satellite overhead gives W = b x h^2 and reaches it as W /
    h^2, b; the other satellite, also W = b x h^2, reaches it, when above its horizon, as W x
    cos^1.3(eta) / r^2, r the slant range and eta the scan angle off its nadir toward the victim,
    worked by hand from the central angle g between the cells (r^2 = R^2 + (R + h)^2 - 2 R (R + h)
    cos g, sin eta = R sin g / r). So x = gamma / G0 x b x (1 + h^2 cos^1.3(eta) / r^2) when it
    leaks and gamma / G0 x b when not, G0 = 4 pi x 25 / (2.998e8 / 1.621e9)^2 (39.6 dBi); the trim
    at each floor is 1 - log2(1 + 1 / (1 + x)) within 1e-9 relative. The leak, worked by hand, is
    over 1 percent of x at 10 degrees; at 22 degrees it would add over 0.5 percent but for the
    horizon rule.
    """
    centres = (
        (TRIM_CASE_LATITUDE_DEG, TRIM_CASE_FIRST_LONGITUDE_DEG),
        (TRIM_CASE_LATITUDE_DEG, TRIM_CASE_FIRST_LONGITUDE_DEG + separation_deg),
    )
    grid = synthetic_population_grid(0.25, cells_people(centres))
    cells = sat._demand_cells(grid, 1.0)
    assert cells.count == 2
    over = list(zip(np.degrees(cells.lat_rad).tolist(), np.degrees(cells.lon_rad).tolist()))
    satellites = satellites_at(over)
    allocation = sat._allocate(satellites, cells, seam_limits(150.0))
    assert allocation.satellite.tolist() == [0, 1] == allocation.cell.tolist()
    beams = allocation.beams[0]
    assert beams == pytest.approx(allocation.beams[1], rel=1e-12)
    assert 4.0 < beams < 5.0
    inputs = SaturationInputs()
    shell = inputs.shell
    orbit_km = EARTH_RADIUS_KM + shell.altitude_km
    central = math.acos(float(cells.xyz[0] @ cells.xyz[1]))
    slant_squared = (
        EARTH_RADIUS_KM**2 + orbit_km**2 - 2 * EARTH_RADIUS_KM * orbit_km * math.cos(central)
    )
    sin_scan = EARTH_RADIUS_KM * math.sin(central) / math.sqrt(slant_squared)
    cos_scan = math.sqrt(1 - sin_scan**2)
    above_horizon = central < math.acos(EARTH_RADIUS_KM / orbit_km)
    assert above_horizon is leaks
    leak = shell.altitude_km**2 * cos_scan**inputs.trim.scan_exponent / slant_squared
    assert leak > 0.005 and (not leaks or leak > 0.01)
    trims = sat._interference_trim(satellites, allocation, cells, shell, inputs.trim)
    wavelength_m = SPEED_OF_LIGHT_M_S / shell.carrier_hz
    directivity = 4 * math.pi * shell.reference_aperture_m2 / wavelength_m**2
    assert 10 * math.log10(directivity) == pytest.approx(39.6, abs=0.05)
    for floor_dbi, trim in zip(inputs.trim.floors_dbi, trims, strict=True):
        extra = 10 ** (floor_dbi / 10) / directivity * beams * (1 + (leak if leaks else 0.0))
        assert trim == pytest.approx(1 - math.log2(1 + 1 / (1 + extra)), rel=1e-9)


BAND_CASE_PEOPLE = {
    (0.375, 0.125): 3_000.0,
    (0.375, 0.375): 30_000.0,
    (0.125, 0.125): 100_000.0,
    (0.125, 0.375): 300_000.0,
    (0.125, 0.625): 15_000.0,
}
"""People in five 0.25 degree cells of about 773 km^2 each, by centre (latitude, longitude):
the first four one 2 x 2 block of the 0.5 degree grid (densities about 3.9, 39, 129 and 388 per
km^2), the fifth in the next 0.5 degree cell east (about 19 per km^2)."""


def band_case_people(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    """People in the band case's five cells only."""
    people = np.zeros(lat.shape)
    for (centre_lat, centre_lon), count in BAND_CASE_PEOPLE.items():
        people = np.where(
            (np.abs(lat - centre_lat) < 0.125) & (np.abs(lon - centre_lon) < 0.125), count, people
        )
    return people


def test_each_band_point_changes_its_one_input(synthetic_population_grid: GridBuilder) -> None:
    """Objective: a band point's curve is the phone class's central curve but for its one
    changed input, and the spaced point's area factor reaches the fill and maximum use alike
    (both read the beam's footprint table).

    Sample: the default inputs' six band points against the phone class's own limits; the band
    case's five cells on a synthetic 0.25 degree grid, at the central threshold of 1 per km^2.

    Expected outcome: the taper's footprint table is the central one times (1.0934 / 0.886)^2
    (a footprint goes as the beamwidth squared) and the spaced point's the taper's times 1.5;
    every other point keeps the central table; B is 48 for the 48-beam point and the central
    150 for every other; every point keeps the phone class's people per beam and one layer (no
    sky sectors). The points that keep the central threshold and grid reuse the central cells;
    the 10 per km^2 point keeps the four cells at or above it and the 100 per km^2 point two;
    the 0.5 degree grid sums the block into one cell of 433,000 people beside the 15,000 cell,
    each with the 0.5 degree zone's area, half the rows and columns.
    """
    inputs = SaturationInputs()
    phone = sat._class_limits(inputs, PHONE)
    points = {point.name: point for point in inputs.bands}
    taper_area = (1.0934 / 0.886) ** 2
    scale = {
        BandName.TAPER: taper_area,
        BandName.TAPER_AND_SPACING: taper_area * 1.5,
    }
    for name, point in points.items():
        band_limits = sat._band_limits(inputs, point)
        np.testing.assert_allclose(
            band_limits.beam.footprint_km2,
            phone.beam.footprint_km2 * scale.get(name, 1.0),
            rtol=1e-12,
        )
        assert band_limits.beams_per_satellite == (48.0 if name is BandName.BEAMS_48 else 150.0)
        assert band_limits.people_per_beam == phone.people_per_beam
        assert band_limits.directional is None
    grid = synthetic_population_grid(0.25, band_case_people)
    central = sat._demand_cells(grid, 1.0)
    assert central.count == len(BAND_CASE_PEOPLE)
    cells = {name: sat._band_cells(grid, point, central, 1.0) for name, point in points.items()}
    for name in (BandName.TAPER, BandName.TAPER_AND_SPACING, BandName.BEAMS_48):
        assert cells[name] is central
    assert sorted(cells[BandName.DENSITY_10_PER_KM2].people.tolist()) == [
        15_000.0,
        30_000.0,
        100_000.0,
        300_000.0,
    ]
    assert sorted(cells[BandName.DENSITY_100_PER_KM2].people.tolist()) == [100_000.0, 300_000.0]
    coarse = cells[BandName.GRID_0P5_DEG]
    assert coarse.cell_deg == 0.5
    assert coarse.index.shape == (360, 720)
    assert coarse.people.tolist() == [433_000.0, 15_000.0]
    zone = cell_area_km2(0.5, 0.5, 720)
    assert coarse.area_km2 == pytest.approx([zone, zone], rel=1e-12)
    assert np.degrees(coarse.lat_rad) == pytest.approx([0.25, 0.25])
    assert np.degrees(coarse.lon_rad) == pytest.approx([0.25, 0.75])


# ---------------------------------------------------------------------------
# The real grid at a coarse, fast setting
# ---------------------------------------------------------------------------

COARSE_REAL_FLEETS = (340, 1_000, 2_000)
"""The coarse setting's requested fleets (realized 342, 992 and 1,980), one snapshot."""

COARSE_LAST_MIDPOINT = 1_401
"""The coarse rows' last midpoint, sqrt(992 x 1,980) = 1,401.48, rounded half up: the fleet each
coarse curve names as not reached by, since no curve's elasticity falls under 0.10 there."""

COARSE_REAL_ROWS = (
    (
        342,
        20648.821508692607,
        107.37387184520156,
        0.4025111405203237,
        102190.2125947176,
        21408.925531671954,
    ),
    (
        992,
        56132.873844223934,
        291.8909439899645,
        0.37723705540473074,
        196678.16776641438,
        61894.68547314836,
    ),
    (
        1980,
        101860.13574450975,
        529.6727058714507,
        0.3429634200151844,
        255760.63823593326,
        124345.18803992725,
    ),
)
"""The coarse rows at the default footprint band count, frozen: fleet, L, capacity Gbps, U,
ceiling, supply. Re-frozen 2026-10-06, when the count moved from 40 to 160 (the investor's
ruling): L, capacity and U moved under 0.01 percent, the ceiling and the supply (which do not
read the fill) not at all. As first computed at 40 bands (2026-10-05), they agreed at float
precision with the same snapshot of the saturation design's local prototype, which
``research/direct_communication/iridium_saturation_module.md`` names and which fills 40 bands."""

COARSE_REAL_TRIMS = (
    (0.017993748675121823, 0.012527386831419962, 0.003180633819415246),
    (0.03330810517514904, 0.023316062840522456, 0.005975989962072492),
    (0.056179393530459754, 0.03966498636703242, 0.010322814929000557),
)
"""The phone class's coarse interference trims at the default footprint band count, frozen: at
each row (342, 992 and 1,980), the trim at -0.4, -2 and -8 dBi, a fraction. First computed at 40
bands (2026-10-06); re-frozen the same day at 160, each moving under 0.01 percentage point."""

COARSE_REAL_MAXIMUM_USE = 380946.7365253218
"""The phone class's maximum use on the shipped grid at the investor's usage, beams."""

COARSE_DIRECTIONAL = {
    DeviceClass.SMALL_TERMINAL_CLASS: (
        684527.9051947582,
        (
            (
                342,
                20792.954169882873,
                331.97939685107104,
                0.40532074405229773,
                118922.09479969715,
                21404.93606919374,
                0.007258472386192219,
                73.77473900083181,
                -16.20556550724097,
            ),
            (
                992,
                57331.80892087483,
                911.914894500129,
                0.38529441479082543,
                284755.15413186094,
                61880.005071762134,
                0.021563899477550323,
                76.65064896736385,
                -16.215255082970614,
            ),
            (
                1980,
                105913.9452509351,
                1669.6992799649254,
                0.35661261027250873,
                415005.8943781192,
                124314.10789697223,
                0.039986848155697016,
                70.42832772191979,
                -15.360192562228939,
            ),
        ),
    ),
    DeviceClass.MOUNTED_TERMINAL_CLASS: (
        1943778.1165993125,
        (
            (
                342,
                21219.486529869715,
                421.58759052774246,
                0.4136352150072069,
                128941.14364361843,
                21410.423077577965,
                0.02671810359437245,
                59.14453682701641,
                -18.868750734096075,
            ),
            (
                992,
                59761.13650112314,
                1173.8679577910011,
                0.40162054100217165,
                364336.338927603,
                61905.084874337204,
                0.06011715221807194,
                52.934937163081955,
                -15.895460710816787,
            ),
            (
                1980,
                115709.53180300078,
                2225.2900025871227,
                0.38959438317508677,
                637680.7416468116,
                124373.22731681664,
                0.11791801998358391,
                47.40455087046911,
                -14.976246507274176,
            ),
        ),
    ),
}
"""The directional classes' coarse rows at the default footprint band count, frozen, with each
class's maximum use: fleet, L, capacity Gbps, U, the sector-rule ceiling, supply, the kept
stacked share, the median separation (degrees) and the mean full-sum interference (dB). First
computed at 40 bands (2026-10-05); re-frozen 2026-10-06 at 160: L moved under 0.13 percent and
the stacking diagnostics under 3 percent; the ceilings, supplies and maximum use (which do not
read the fill) not at all."""

COARSE_BANDS = {
    BandName.TAPER: (
        253261.3007391356,
        (
            (
                342,
                19268.86357941863,
                100.19809061297688,
                0.3756113758171273,
                67204.6866775107,
                20183.576871614907,
            ),
            (
                992,
                51985.154073872065,
                270.32280118413473,
                0.34936259458247354,
                129498.5403789101,
                58497.21294412446,
            ),
            (
                1980,
                90401.87206166257,
                470.08973472064537,
                0.30438340761502547,
                168586.02171164897,
                117183.53473941982,
            ),
        ),
    ),
    BandName.TAPER_AND_SPACING: (
        168882.15956754866,
        (
            (
                342,
                17884.335743744556,
                92.99854586747169,
                0.3486225291178276,
                44803.29111163624,
                18869.48870100613,
            ),
            (
                992,
                46289.50265445753,
                240.70541380317917,
                0.3110853673014619,
                86332.9002698339,
                54822.43062219184,
            ),
            (
                1980,
                78209.25668990148,
                406.6881347874877,
                0.26333083060572887,
                112391.94523636127,
                109737.6448195993,
            ),
        ),
    ),
    BandName.DENSITY_10_PER_KM2: (
        252829.7231940112,
        (
            (
                342,
                17231.9211424255,
                89.6059899406126,
                0.3359048955638499,
                66755.526511821,
                18421.37507649095,
            ),
            (
                992,
                45602.84155305654,
                237.13477607589402,
                0.3064707093619391,
                127802.00237942414,
                53892.43809956228,
            ),
            (
                1980,
                78926.89257450642,
                410.4198413874334,
                0.26574711304547616,
                167231.5596078611,
                107888.44036897024,
            ),
        ),
    ),
    BandName.DENSITY_100_PER_KM2: (
        92020.43406589914,
        (
            (
                342,
                10235.907286577887,
                53.226717890205016,
                0.19953035646350656,
                23577.929688830915,
                11298.508971539646,
            ),
            (
                992,
                25882.827805905396,
                134.59070459070807,
                0.17394373525474055,
                45897.65888676973,
                34617.11517424151,
            ),
            (
                1980,
                40635.598123603406,
                211.30511024273773,
                0.13682019570236836,
                60444.2866770497,
                69302.28966736834,
            ),
        ),
    ),
    BandName.GRID_0P5_DEG: (
        446507.1621288899,
        (
            (
                342,
                21602.31168039707,
                112.33202073806476,
                0.4210976935749916,
                119629.71416586779,
                22380.923093227226,
            ),
            (
                992,
                58812.17076199278,
                305.8232879623625,
                0.39524308307790845,
                230525.36179907064,
                64696.68530694656,
            ),
            (
                1980,
                109248.4607145345,
                568.0919957155795,
                0.3678399350657727,
                299752.75177026563,
                129548.80947020264,
            ),
        ),
    ),
    BandName.BEAMS_48: (
        380946.7365253218,
        (
            (
                342,
                7475.9854533204425,
                38.8751243572663,
                0.4554084705970055,
                102190.2125947176,
                7624.037949061897,
            ),
            (
                992,
                20910.97041359971,
                108.7370461507185,
                0.4391584848286229,
                196678.16776641438,
                22576.75501265761,
            ),
            (
                1980,
                39446.68674772166,
                205.12277108815263,
                0.415053522177206,
                255760.63823593326,
                44990.23618199112,
            ),
        ),
    ),
}
"""The phone class's band points' coarse rows at the default footprint band count, frozen, with
each point's maximum use: fleet, L, capacity Gbps, U, ceiling, supply. The 48-beam point keeps
the central maximum use and ceiling (neither depends on B); the two density points and the 0.5
degree grid change the demand, the taper and the spacing the area per beam. First computed at 40
bands (2026-10-06); re-frozen the same day at 160: L, capacity and U moved under 0.04 percent,
the ceilings, supplies and maximum use (which do not read the fill) not at all."""


COARSE_SWEEP = SweepInputs(
    fleets=COARSE_REAL_FLEETS,
    mounted_terminal_extension=(),
    snapshots_phone_central=1,
    snapshots_directional=1,
    snapshots_bands=1,
)
"""The coarse setting: fleets 340, 1,000 and 2,000, one snapshot for every class and band
point, no mounted extension."""


@pytest.fixture(scope="module")
def real_grid(repo_dir: Path) -> PopulationGrid:
    """The shipped population grid."""
    return load_population_grid(repo_dir / POPULATION_GRID_PATH, POPULATION_GRID_SHA256)


def coarse_inputs_for(iridium: IridiumDials) -> SaturationInputs:
    """The coarse setting's inputs for a config's Iridium dials: what the saturation command
    builds (``saturation_inputs_for``) with its sweep replaced by the coarse one, validated anew."""
    return SaturationInputs.model_validate(
        {**saturation_inputs_for(iridium).model_dump(), "sweep": COARSE_SWEEP}
    )


def promote_coarse(scenario: Path, output: Path) -> Path:
    """Promote the curve at the coarse setting through the saturation command's own function
    (its inputs builder patched to the coarse sweep), with the pinned stamp: computed and written
    through ``write_files_with_rollback``, as the full promotion is."""
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(sat, "saturation_inputs_for", coarse_inputs_for)
        return sat.promote_saturation_curve(scenario, output, version_stamp=STAMP)


def rendered_with_measurement(curve: SaturationCurve, measurement: RunMeasurement) -> bytes:
    """A curve's bytes as the promotion writes them (``render_artifact_json`` and
    ``ARTIFACT_FILE_END``), with the given run measurement copied in (``model_copy``)."""
    measured = curve.model_copy(
        update={"provenance": curve.provenance.model_copy(update={"run_measurement": measurement})}
    )
    return (render_artifact_json(measured) + ARTIFACT_FILE_END).encode("utf-8")


def curves_equal_but_measurement(first: Path, second: Path) -> bool:
    """Whether two promoted curves are byte-identical but for their run measurements (the plan's
    finding F2: a run's measured wall time and peak memory differ run to run).

    Both files are parsed as :class:`SaturationCurve`, and the comparison runs both ways: the
    second re-rendered with the first's measurement must be the first file's bytes, and the
    first re-rendered with the second's measurement the second file's bytes. One way alone
    compares only the second file's values, so a second file in another byte form (compact,
    without its closing newline, its keys in another order) would pass; both ways, each file
    must be the promotion's own rendering. Acceptance runs this same helper as a script.
    """
    one, two = (
        SaturationCurve.model_validate_json(path.read_text(encoding="utf-8"))
        for path in (first, second)
    )
    return (
        rendered_with_measurement(two, one.provenance.run_measurement) == first.read_bytes()
        and rendered_with_measurement(one, two.provenance.run_measurement) == second.read_bytes()
    )


@pytest.fixture(scope="module")
def coarse_curve_file(tmp_path_factory: pytest.TempPathFactory, iridium_yaml: Path) -> Path:
    """The shipped scenario's curve at the coarse setting, promoted once into a temporary
    folder for the tests that read it."""
    return promote_coarse(iridium_yaml, tmp_path_factory.mktemp("coarse") / "saturation_curve.json")


@pytest.fixture(scope="module")
def coarse_real_curve(coarse_curve_file: Path) -> SaturationCurve:
    """The coarse promoted curve, read back through ``load_saturation_curve``."""
    return load_saturation_curve(coarse_curve_file)


def test_the_real_grid_at_a_coarse_setting_is_frozen(coarse_real_curve: SaturationCurve) -> None:
    """Objective: the module's numbers on the shipped grid do not drift.

    Sample: the shipped scenario's curve (the investor's usage) at fleets 340, 1,000 and 2,000
    and one snapshot for every class and band point, promoted through the saturation command's
    own function and read back with ``load_saturation_curve``.

    Expected outcome: every class's rows (L, capacity, U, the ceiling, the supply, for the
    directional classes their stacking diagnostics, and for the phone class its interference
    trim at -0.4, -2 and -8 dBi) and maximum use within 1e-4 relative of the frozen values;
    the six band points in their order, each the inputs' point, its rows (no trim, no
    diagnostics) and maximum use within 1e-4 relative; no 0.10 crossing on any curve, each not
    reached by the rows' last midpoint (1,401), and no other marker on any curve (the
    directional classes' included); the curve's envelope: schema, stamp, the input hash of its
    parameters, the grid's name, digest, citations and licence, the four checks passed, the
    run measured, the ten stated limits (the curve's own; no marker unplaced), and the three
    classes (small terminal, mounted terminal, phone class).
    """
    inputs = SaturationInputs(sweep=COARSE_SWEEP)
    curve = coarse_real_curve
    rows = phone_curve(curve).rows
    assert [row.fleet for row in rows] == [frozen[0] for frozen in COARSE_REAL_ROWS]
    assert [row.requested_fleet for row in rows] == list(COARSE_REAL_FLEETS)
    for row, (_, useful, capacity, ocean, ceiling, supply), trims in zip(
        rows, COARSE_REAL_ROWS, COARSE_REAL_TRIMS, strict=True
    ):
        assert row.useful_beams == pytest.approx(useful, rel=1e-4)
        assert row.capacity_gbps == pytest.approx(capacity, rel=1e-4)
        assert row.ocean_factor == pytest.approx(ocean, rel=1e-4)
        assert row.ceiling_beams == pytest.approx(ceiling, rel=1e-4)
        assert row.supply_beams == pytest.approx(supply, rel=1e-4)
        assert row.useful_beams_spread == 0.0
        assert row.directional is None
        assert row.trim is not None
        assert [entry.floor_dbi for entry in row.trim] == [-0.4, -2.0, -8.0]
        for entry, trim in zip(row.trim, trims, strict=True):
            assert entry.trim == pytest.approx(trim, rel=1e-4)
    markers = phone_curve(curve).markers
    assert markers.maximum_use_beams == pytest.approx(COARSE_REAL_MAXIMUM_USE, rel=1e-4)
    assert markers.saturation_number is None
    assert markers.saturation_not_reached_by == COARSE_LAST_MIDPOINT
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
    assert len(provenance.checks_passed) == 4
    assert provenance.run_measurement.wall_time_s > 0
    assert provenance.run_measurement.peak_memory_mb > 0
    assert len(curve.limits) == 10
    assert [entry.device_class for entry in curve.classes] == list(DeviceClass)
    assert [band.point for band in curve.bands] == list(inputs.bands)
    assert [band.point.name for band in curve.bands] == list(BandName)
    for band in curve.bands:
        maximum_use, frozen_rows = COARSE_BANDS[band.point.name]
        assert band.markers.maximum_use_beams == pytest.approx(maximum_use, rel=1e-4)
        assert band.markers.saturation_not_reached_by == COARSE_LAST_MIDPOINT
        assert band.markers.elasticity_under_0p25_fleet is None
        assert band.markers.fleet_at_90pct_of_maximum_use is None
        for row, (fleet, useful, capacity, ocean, ceiling, supply) in zip(
            band.rows, frozen_rows, strict=True
        ):
            assert (row.fleet, row.requested_fleet) == (fleet, walker_request_of(fleet))
            assert row.useful_beams == pytest.approx(useful, rel=1e-4)
            assert row.capacity_gbps == pytest.approx(capacity, rel=1e-4)
            assert row.ocean_factor == pytest.approx(ocean, rel=1e-4)
            assert row.ceiling_beams == pytest.approx(ceiling, rel=1e-4)
            assert row.supply_beams == pytest.approx(supply, rel=1e-4)
            assert row.directional is None
            assert row.trim is None
    for device_class, (maximum_use, frozen_rows) in COARSE_DIRECTIONAL.items():
        directional = class_curve(curve, device_class)
        assert directional.markers.maximum_use_beams == pytest.approx(maximum_use, rel=1e-4)
        assert directional.markers.saturation_not_reached_by == COARSE_LAST_MIDPOINT
        assert directional.markers.elasticity_under_0p25_fleet is None
        assert directional.markers.fleet_at_90pct_of_maximum_use is None
        for row, frozen in zip(directional.rows, frozen_rows, strict=True):
            fleet, useful, capacity, ocean, ceiling, supply, share, separation, interference = (
                frozen
            )
            assert (row.fleet, row.requested_fleet) == (fleet, walker_request_of(fleet))
            assert row.useful_beams == pytest.approx(useful, rel=1e-4)
            assert row.capacity_gbps == pytest.approx(capacity, rel=1e-4)
            assert row.ocean_factor == pytest.approx(ocean, rel=1e-4)
            assert row.ceiling_beams == pytest.approx(ceiling, rel=1e-4)
            assert row.supply_beams == pytest.approx(supply, rel=1e-4)
            assert row.directional is not None
            assert row.directional.kept_stacked_share == pytest.approx(share, rel=1e-4)
            assert row.directional.median_separation_deg == pytest.approx(separation, rel=1e-4)
            assert row.directional.mean_full_sum_interference_db == pytest.approx(
                interference, rel=1e-4
            )
            assert row.trim is None


def walker_request_of(fleet: int) -> int:
    """The coarse setting's request for a realized fleet (340, 1,000 and 2,000)."""
    return dict(zip((342, 992, 1_980), COARSE_REAL_FLEETS, strict=True))[fleet]


# ---------------------------------------------------------------------------
# The drift test: the committed curve against the code
# ---------------------------------------------------------------------------

COMMITTED_CURVE = "communications/models/iridium/saturation_curve.json"
"""The promoted saturation curve, repository-relative."""

DRIFT_CHECK_ROWS = (
    (DeviceClass.SMALL_TERMINAL_CLASS, 342),
    (DeviceClass.MOUNTED_TERMINAL_CLASS, 342),
    (DeviceClass.PHONE_CLASS, 342),
    (DeviceClass.MOUNTED_TERMINAL_CLASS, 1_980),
)
"""The rows the drift test recomputes, by class and realized fleet: every class's first row and
the mounted terminal's 1,980 row, where rules D3 and D4 act (about 11 percent of its beams
stacked)."""


def flat_values(value: object, path: str = "") -> dict[str, object]:
    """A model dump's leaves by path, nested objects and lists flattened, so two rows compare
    field by field."""
    flat: dict[str, object] = {}
    if isinstance(value, dict):
        for key, item in value.items():
            flat.update(flat_values(item, f"{path}.{key}" if path else str(key)))
    elif isinstance(value, list | tuple):
        for index, item in enumerate(value):
            flat.update(flat_values(item, f"{path}[{index}]"))
    else:
        flat[path] = value
    return flat


def assert_rows_match(label: str, committed: CurveRow, recomputed: CurveRow, rel: float) -> None:
    """Compare a committed row with its recomputation: the same fields, every value (the
    diagnostics and the trim included) within ``rel`` relative (0: exactly), the curve and the
    row named in the message."""
    expected = flat_values(committed.model_dump())
    assert flat_values(recomputed.model_dump()) == pytest.approx(expected, rel=rel, abs=0), label


def drift_grid_and_cells(
    parameters: SaturationInputs, repo_dir: Path
) -> tuple[PopulationGrid, sat._DemandCells]:
    """A curve's grid, loaded once through the command's own grid load (``_inputs_grid``), and
    its central demand cells, which the curve's plans are built on, both as the drift seams take
    them (``_seam_grid_and_cells``)."""
    return sat._seam_grid_and_cells(
        parameters, sat._inputs_grid(SourceCheckout(repo_dir), parameters)
    )


def assert_check_rows_match(curve: SaturationCurve, repo_dir: Path, rel: float) -> None:
    """Rebuild a curve's check rows through the class seam, each from its requested fleet, and
    every class's maximum use through the class's own plan (``_class_plan``), at the curve's own
    settings from one grid load, and compare each within ``rel`` relative (0: exactly)."""
    parameters = curve.parameters
    population, cells = drift_grid_and_cells(parameters, repo_dir)
    for device_class, fleet in DRIFT_CHECK_ROWS:
        (committed,) = [row for row in class_curve(curve, device_class).rows if row.fleet == fleet]
        recomputed = sat._class_row(
            device_class, committed.requested_fleet, parameters, population=population
        )
        assert_rows_match(f"{device_class.value} row at {fleet}", committed, recomputed, rel)
    for entry in curve.classes:
        rebuilt = sat._plan_maximum_use(sat._class_plan(parameters, cells, entry.device_class))
        assert rebuilt == pytest.approx(entry.markers.maximum_use_beams, rel=rel, abs=0), (
            f"{entry.device_class.value} maximum use"
        )


def assert_band_rows_match(curve: SaturationCurve, repo_dir: Path, rel: float) -> None:
    """Rebuild every band point's first row through the band seam, from its requested fleet, and
    its maximum use through its own plan (``_band_plan``), at the curve's own settings from one
    grid load, and compare each within ``rel`` relative (0: exactly)."""
    parameters = curve.parameters
    population, cells = drift_grid_and_cells(parameters, repo_dir)
    for band in curve.bands:
        label = f"band point {band.point.name.value}"
        committed = band.rows[0]
        recomputed = sat._band_row(
            band.point, committed.requested_fleet, parameters, population=population
        )
        assert_rows_match(f"{label} row at {committed.fleet}", committed, recomputed, rel)
        rebuilt = sat._plan_maximum_use(sat._band_plan(parameters, population, cells, band.point))
        assert rebuilt == pytest.approx(band.markers.maximum_use_beams, rel=rel, abs=0), (
            f"{label} maximum use"
        )


def test_the_drift_seams_and_plans_rebuild_the_coarse_curve_exactly(
    coarse_real_curve: SaturationCurve, repo_dir: Path
) -> None:
    """Objective: the drift seams and the curve's own plans are the curve's computation: one
    class's or one band point's row at one requested fleet, rebuilt in this process from the
    row's request, is the curve's row, and each curve's maximum use rebuilt from its plan is the
    curve's.

    Sample: the coarse real-grid curve (one snapshot): every class's 342 row, the mounted
    terminal's 1,980 row (requested 2,000), every band point's 342 row, and every class's and
    band point's maximum use, from one grid load; and the small terminal's 342 row once more
    through the seam's own grid load (no grid passed), the path a reviewer's script takes.

    Expected outcome: every value of each row, the phone class's trim included, and every
    maximum use equal to the curve's exactly (the same code on the same draw, in another
    process), by either grid load.
    """
    assert_check_rows_match(coarse_real_curve, repo_dir, rel=0.0)
    assert_band_rows_match(coarse_real_curve, repo_dir, rel=0.0)
    committed = class_curve(coarse_real_curve, DeviceClass.SMALL_TERMINAL_CLASS).rows[0]
    recomputed = sat._class_row(
        DeviceClass.SMALL_TERMINAL_CLASS, committed.requested_fleet, coarse_real_curve.parameters
    )
    assert_rows_match(
        "small_terminal_class row by the seam's own grid load", committed, recomputed, 0.0
    )


def test_committed_curve_has_not_drifted(repo_dir: Path) -> None:
    """Objective: the committed curve's rows are what the code computes, so a change to the
    allocation, the directional rules or maximum use after its promotion fails here until the
    curve is re-promoted (the re-promotion rule). Its two neighbours guard the rest that can be
    recomputed cheaply: each band point's first row and maximum use, and every field derived
    from the rows and the parameters (the markers, the limits, the texts). Only the rows none of
    them rebuilds (and those rows' trims) rest on the re-promotion rule alone.

    Sample: ``communications/models/iridium/saturation_curve.json``, loaded with
    ``load_saturation_curve`` (so it also loads whole and unaltered), at its own settings (its
    parameters: the investor's usage, two snapshots for the directional classes and four for
    the phone class): every class's first row (342) and the mounted terminal's 1,980 row (where
    rules D3 and D4 act), each rebuilt through the drift seam from its requested fleet, and every
    class's maximum use (the small terminal's and the mounted terminal's by the directional
    rule), each rebuilt through the class's own plan; the grid loaded once. The three drift
    tests' budget is 90 s.

    Expected outcome: every value of each row (L, its spread, capacity, U, the ceiling, the
    supply, the directional diagnostics, the phone class's trim) and each class's maximum use
    within 1e-4 relative of the committed curve.
    """
    curve = load_saturation_curve(repo_dir / COMMITTED_CURVE)
    assert_check_rows_match(curve, repo_dir, rel=1e-4)


def test_committed_curve_has_not_drifted_in_its_band_rows(repo_dir: Path) -> None:
    """Objective: the committed band points are what the code computes, so a change to a band
    point's inputs (``_band_limits``, ``_band_cells``, the grid's aggregation) after the
    promotion fails here until the curve is re-promoted.

    Sample: the committed curve at its own settings (two snapshots for the band points): every
    band point's first row (342), rebuilt through the band seam from its requested fleet, and
    its maximum use, rebuilt through its own plan; the grid loaded once.

    Expected outcome: every value of each row (L, its spread, capacity, U, the ceiling, the
    supply, no diagnostics and no trim) and each maximum use within 1e-4 relative of the
    committed curve.
    """
    curve = load_saturation_curve(repo_dir / COMMITTED_CURVE)
    assert_band_rows_match(curve, repo_dir, rel=1e-4)


def test_committed_curve_has_not_drifted_in_its_derived_fields(repo_dir: Path) -> None:
    """Objective: every field of the committed curve that the code derives from its rows and
    its parameters is what the code derives today, so a change to the markers' rules, the stated
    limits or the curve's texts fails here until the curve is re-promoted.

    Sample: the committed curve: each class's and band point's rows and maximum use, and its
    parameters.

    Expected outcome, exactly: every class's and band point's markers are ``_markers`` of its own
    rows and maximum use; the limits are ``_stated_limits`` of the parameters and the curves (the
    assembly ``compute_saturation`` uses); the method, the checks passed, the citations and the
    licence are what the computation writes for these parameters.
    """
    curve = load_saturation_curve(repo_dir / COMMITTED_CURVE)
    parameters = curve.parameters
    for entry in curve.classes:
        rederived = sat._markers(entry.device_class, entry.rows, entry.markers.maximum_use_beams)
        assert rederived == entry.markers, entry.device_class
    for band in curve.bands:
        rederived = sat._markers(band.point.name, band.rows, band.markers.maximum_use_beams)
        assert rederived == band.markers, band.point.name
    assert curve.limits == sat._stated_limits(parameters, curve.classes, curve.bands)
    provenance = curve.provenance
    assert provenance.method == sat._method(parameters)
    assert provenance.checks_passed == sat._checks_passed(parameters)
    assert provenance.citations == sat._GRID_CITATIONS
    assert provenance.licence == sat._GRID_LICENCE


def test_the_curve_texts_name_the_reference_panel_and_take_the_measured_panel_note_whole() -> None:
    """Objective: the curve's published texts call the 25 m^2 panel the reference the engine scales
    from, never the model's panel, and its panel-rule limit is the measured note whole (the
    Iridium run's panel line states the same note), so the curve and the artifact cannot
    disagree about the panel rule.

    Sample: the default inputs' method and stated limits, as the computation writes them
    (``_method``, ``_curve_limits``).

    Expected outcome: the method names "a square aperture at the 25 m^2 reference panel" and no
    "square 25 m^2 aperture"; it says the taper-and-spacing point changes two inputs, and reads
    the 90 percent fleet between two rows, log-log; the panel limit is "Computed at the 25 m^2
    reference panel. The engine scales the curve linearly by the scenario's panel over it (the
    panel rule). " and ``PANEL_RULE_LIMITS_NOTE`` exactly; no limit calls the rule exact; one limit
    says what a null marker means.
    """
    inputs = SaturationInputs()
    method = sat._method(inputs)
    assert "a square aperture at the 25 m^2 reference panel" in method
    assert "square 25 m^2 aperture" not in method
    assert "but for one changed input (two for the taper with wider spacing)" in method
    assert "reach 0.9 of maximum use, read between two rows, log-log" in method
    limits = sat._curve_limits(inputs)
    panel = [limit for limit in limits if limit.startswith("Computed at the 25 m^2 reference")]
    assert panel == [
        "Computed at the 25 m^2 reference panel. The engine scales the curve linearly by the "
        f"scenario's panel over it (the panel rule). {PANEL_RULE_LIMITS_NOTE}"
    ]
    assert not any("exact in beams" in limit for limit in limits)
    null_markers = [limit for limit in limits if limit.startswith("A null marker is one the rows")]
    assert len(null_markers) == 1


def test_the_committed_curve_loads_whole_from_the_shipped_scenario(
    repo_dir: Path, iridium_yaml: Path
) -> None:
    """Objective: the committed curve is the one the shipped scenario implies, whole and
    unaltered, so the engine can read it.

    Sample: ``communications/models/iridium/saturation_curve.json`` and
    ``scenarios/iridium.yaml``.

    Expected outcome: the curve loads (schema, input hash, completeness), its parameters are
    exactly ``saturation_inputs_for`` of the scenario's Iridium dials, and it lists the three
    classes (small terminal first) and the six band points.
    """
    curve = load_saturation_curve(repo_dir / COMMITTED_CURVE)
    dials = load_comms_config(iridium_yaml).iridium
    assert dials is not None
    assert curve.parameters == saturation_inputs_for(dials)
    assert [entry.device_class for entry in curve.classes] == list(DeviceClass)
    assert [band.point.name for band in curve.bands] == list(BandName)


def test_a_second_promotion_at_the_coarse_setting_is_byte_identical(
    coarse_curve_file: Path, tmp_path: Path, iridium_yaml: Path
) -> None:
    """Objective: a promotion is deterministic: a second run of the saturation command's own
    function at the coarse setting, with the pinned stamp, writes the same bytes but for the run's
    own measurement (the plan's finding F2).

    Sample: the coarse promoted curve and a second promotion of the shipped scenario at the same
    setting, each computed and written through ``write_files_with_rollback``.

    Expected outcome: ``curves_equal_but_measurement`` holds; the two measurements are each a
    real measurement (a positive wall time and peak-memory bound).
    """
    second = promote_coarse(iridium_yaml, tmp_path / "saturation_curve.json")
    assert curves_equal_but_measurement(coarse_curve_file, second)
    for path in (coarse_curve_file, second):
        measured = load_saturation_curve(path).provenance.run_measurement
        assert measured.wall_time_s > 0
        assert measured.peak_memory_mb > 0


def test_the_byte_identity_helper_refuses_another_byte_form(
    coarse_curve_file: Path, tmp_path: Path
) -> None:
    """Objective: ``curves_equal_but_measurement`` passes two promotions that differ only in their
    run measurements and fails any other difference, in a value or in the bytes' form.

    Sample: the coarse promoted curve against five second files written from it: its run
    measurement changed; one row value changed by 1e-12 relative; the same values in compact
    JSON, without the closing newline, and with a key moved to the front.

    Expected outcome: equal for the measurement alone, in either order; not equal for each of the
    four others.
    """
    text = coarse_curve_file.read_text(encoding="utf-8")
    curve = SaturationCurve.model_validate_json(text)
    canonical = rendered_with_measurement(
        curve, RunMeasurement(wall_time_s=1.0, peak_memory_mb=2.0)
    ).decode("utf-8")
    data = json.loads(canonical)
    changed = json.loads(text)
    changed["classes"][2]["rows"][1]["useful_beams"] *= 1 + 1e-12
    seconds = {
        "only the measurement": (canonical, True),
        "one value": (json.dumps(changed, indent=2) + ARTIFACT_FILE_END, False),
        "compact": (json.dumps(data, separators=(",", ":")), False),
        "no closing newline": (canonical.removesuffix(ARTIFACT_FILE_END), False),
        "a key moved": (
            json.dumps({"version_stamp": data["version_stamp"], **data}, indent=2)
            + ARTIFACT_FILE_END,
            False,
        ),
    }
    for label, (second_text, equal) in seconds.items():
        second = tmp_path / f"{label.replace(' ', '_')}.json"
        second.write_text(second_text, encoding="utf-8")
        assert curves_equal_but_measurement(coarse_curve_file, second) is equal, label
        assert curves_equal_but_measurement(second, coarse_curve_file) is equal, label


# ---------------------------------------------------------------------------
# numpy confinement, the arithmetic and the constants
# ---------------------------------------------------------------------------

NUMPY_FREE_MODULES = (
    "communications.config",
    "communications.engine",
    "communications.ground",
    "communications.iridium",
    "communications.json_output",
    "communications.saturation_curve",
)
"""The communications modules that must load without numpy (ADR 010): the ones the Iridium
command loads and the cellular family's ground comparison, every one but the saturation module."""


def _loaded_after_each_import(
    steps: Sequence[tuple[str, ...]], probed: tuple[str, ...], code_dir: Path
) -> list[list[str]]:
    """Import each step's modules in turn in one fresh interpreter and return, after each step,
    which of the probed modules are in its ``sys.modules`` (in the probed order): transitive
    imports included, which a grep would miss."""
    source = "import json\nimport sys\nloaded = []\n"
    for step in steps:
        source += "".join(f"import {name}\n" for name in step)
        source += f"loaded.append([name for name in {probed!r} if name in sys.modules])\n"
    source += "print(json.dumps(loaded))\n"
    environment = {**os.environ, "PYTHONPATH": str(code_dir / "src")}
    result = subprocess.run(  # noqa: S603 (a fixed command: this interpreter and our source)
        [sys.executable, "-c", source],
        capture_output=True,
        text=True,
        check=False,
        env=environment,
    )
    assert result.returncode == 0, result.stderr
    loaded: list[list[str]] = json.loads(result.stdout)
    return loaded


def test_numpy_stays_inside_the_saturation_module(code_dir: Path) -> None:
    """Objective: numpy stays inside ``communications.saturation`` (ADR 010), transitive
    imports included, which a grep would miss.

    Sample: one fresh interpreter importing ``communications.config``, ``.engine``, ``.ground``,
    ``.iridium``, ``.json_output`` and ``.saturation_curve``; then, in the same interpreter,
    ``communications.saturation`` too, the control.

    Expected outcome: numpy is not in ``sys.modules`` after the first step, and is after the
    control (so the probe can see it).
    """
    assert _loaded_after_each_import(
        (NUMPY_FREE_MODULES, ("communications.saturation",)), ("numpy",), code_dir
    ) == [[], ["numpy"]]


FAMILY_MODULES = ("communications.iridium", "communications.saturation_curve")
"""The modules ``communications.engine`` must not import: the Iridium family and the curve's
contract."""


def test_engine_imports_no_family_module(code_dir: Path) -> None:
    """Objective: ``communications.engine`` imports neither the Iridium family nor the curve's
    contract, transitive imports included, which a grep would miss: the import half of keeping
    the shared fleet-and-cost loop family-neutral (the behavior half is the tripwire, which
    compares an Iridium run's and a cellular run's shared records whole).

    Sample: one fresh interpreter importing ``communications.engine`` alone; then, in the same
    interpreter, ``communications.iridium`` too, the control.

    Expected outcome: neither ``communications.iridium`` nor ``communications.saturation_curve``
    is in ``sys.modules`` after the first step; both are after the control (so the probe sees
    them).
    """
    assert _loaded_after_each_import(
        (("communications.engine",), ("communications.iridium",)), FAMILY_MODULES, code_dir
    ) == [[], list(FAMILY_MODULES)]


def test_the_command_refuses_a_scenario_without_an_iridium_block(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Objective: the saturation command narrows its scenario first, so a scenario of the
    cellular family fails with the family's message before anything runs.

    Sample: a scenario setting only the cellular satellite block; an output path in a temporary
    folder.

    Expected outcome: exit status 1; exactly one ERROR record, on one line, naming the scenario
    and the narrowing function's message; no file written.
    """
    scenario = tmp_path / "cellular.yaml"
    scenario.write_text("satellite:\n  satellites_per_launch: 12\n", encoding="utf-8")
    out_path = tmp_path / "saturation_curve.json"
    assert sat.main([str(scenario), str(out_path)]) == EXIT_ERROR
    errors = [record.getMessage() for record in caplog.records if record.levelno >= logging.ERROR]
    assert len(errors) == 1
    assert "\n" not in errors[0]
    assert f"could not promote the saturation curve from {scenario}" in errors[0]
    assert "the scenario does not select the Iridium model" in errors[0]
    assert sorted(tmp_path.iterdir()) == [scenario]


READ_ONLY_DIR_MODE = stat.S_IRUSR | stat.S_IXUSR
"""A folder this process can read and search but not write into (as the sibling suites name it)."""

OWNER_DIR_MODE = stat.S_IRWXU
"""A folder's mode restored after a test: its owner may read, write and search it."""

ROOT_IGNORES_PERMISSIONS = os.geteuid() == 0
"""Whether the tests run as root, which a folder's mode bits do not stop."""

OVER_LONG_NAME = "x" * 300
"""A folder name past every file system's 255-byte limit on one name."""


class UnusableDestination(StrEnum):
    """A destination the shared writer refuses, as the pre-flight tests make it."""

    DIRECTORY = "a directory"
    SYMBOLIC_LINK = "a symbolic link"
    READ_ONLY_FOLDER = "a read-only folder"
    PATH_UNDER_A_FILE = "a path under a file"
    OVER_LONG_FOLDER_NAME = "a folder name past the file system's limit"


def unusable_destination(tmp_path: Path, case: UnusableDestination) -> Path:
    """A destination the shared writer refuses, made in a temporary folder: a directory, a
    symbolic link to a file, a file in a folder this process cannot write into, a path under a
    regular file, or a path through a folder name past the file system's limit."""
    match case:
        case UnusableDestination.DIRECTORY:
            destination = tmp_path / "curve.json"
            destination.mkdir()
        case UnusableDestination.SYMBOLIC_LINK:
            (tmp_path / "target.json").write_text("ORIGINAL\n", encoding="utf-8")
            destination = tmp_path / "curve.json"
            destination.symlink_to(tmp_path / "target.json")
        case UnusableDestination.READ_ONLY_FOLDER:
            folder = tmp_path / "locked"
            folder.mkdir()
            destination = folder / "curve.json"
            destination.write_text("ORIGINAL\n", encoding="utf-8")
            folder.chmod(READ_ONLY_DIR_MODE)
        case UnusableDestination.PATH_UNDER_A_FILE:
            (tmp_path / "blocker").write_text("ORIGINAL\n", encoding="utf-8")
            destination = tmp_path / "blocker" / "curve.json"
        case UnusableDestination.OVER_LONG_FOLDER_NAME:
            destination = tmp_path / OVER_LONG_NAME / "curve.json"
        case _:
            assert_never(case)
    return destination


def unlock(tmp_path: Path, case: UnusableDestination) -> None:
    """Give the read-only folder its owner's mode back (the other cases change no mode)."""
    if case is UnusableDestination.READ_ONLY_FOLDER:
        (tmp_path / "locked").chmod(OWNER_DIR_MODE)


def the_tree(tmp_path: Path) -> list[tuple[str, bool, bytes | None]]:
    """Every path under a folder (no link followed): its name, whether it is a symbolic link, and
    a regular file's bytes."""
    return sorted(
        (
            str(path.relative_to(tmp_path)),
            path.is_symlink(),
            path.read_bytes() if path.is_file() and not path.is_symlink() else None,
        )
        for path in tmp_path.rglob("*")
    )


UNUSABLE_DESTINATIONS = [
    pytest.param(
        case,
        marks=pytest.mark.skipif(
            case is UnusableDestination.READ_ONLY_FOLDER and ROOT_IGNORES_PERMISSIONS,
            reason="root ignores directory permissions",
        ),
        id=case.value,
    )
    for case in UnusableDestination
]
"""Every unusable destination, the read-only folder skipped under root."""

PREFLIGHT_REASONS = {
    UnusableDestination.DIRECTORY: "exists and is not a regular file",
    UnusableDestination.SYMBOLIC_LINK: "is a symbolic link",
    UnusableDestination.READ_ONLY_FOLDER: "is not a directory this process can write into",
    UnusableDestination.PATH_UNDER_A_FILE: "is not a directory this process can write into",
    UnusableDestination.OVER_LONG_FOLDER_NAME: "could not be checked (File name too long)",
}
"""The pre-flight's reason for each unusable destination."""


@pytest.mark.parametrize("case", UNUSABLE_DESTINATIONS)
def test_a_destination_the_writer_would_refuse_is_refused_before_the_computation(
    tmp_path: Path,
    iridium_yaml: Path,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    case: UnusableDestination,
) -> None:
    """Objective: the saturation command refuses what the shared writer would refuse before it
    computes (a full promotion computes for tens of minutes first), and changes nothing.

    Sample: the shipped scenario with ``compute_saturation`` patched to fail the test if called,
    and a destination that is a directory, a symbolic link to a file, a file in a folder this
    process cannot write into (skipped under root), a path under a regular file, or a path
    through a folder name past the file system's limit (an error the system reports, never
    hidden as a missing path).

    Expected outcome: exit status 1; exactly one ERROR record, on one line, naming the scenario,
    the destination and the reason, and saying nothing was computed; the computation never
    called; every file and folder as it was.
    """

    def never(*args: object, **kwargs: object) -> SaturationCurve:
        pytest.fail("compute_saturation ran before the destination was checked")

    monkeypatch.setattr(sat, "compute_saturation", never)
    destination = unusable_destination(tmp_path, case)
    before = the_tree(tmp_path)
    try:
        status = sat.main([str(iridium_yaml), str(destination)])
    finally:
        unlock(tmp_path, case)
    assert status == EXIT_ERROR
    errors = [record.getMessage() for record in caplog.records if record.levelno >= logging.ERROR]
    assert len(errors) == 1
    assert "\n" not in errors[0]
    assert f"could not promote the saturation curve from {iridium_yaml}: {destination}" in errors[0]
    assert PREFLIGHT_REASONS[case] in errors[0]
    assert "no destination was changed and nothing was computed" in errors[0]
    assert the_tree(tmp_path) == before


@pytest.mark.parametrize("case", UNUSABLE_DESTINATIONS)
def test_the_shared_writer_refuses_every_destination_the_preflight_refuses(
    tmp_path: Path, case: UnusableDestination
) -> None:
    """Objective: the pre-flight's copy of the writer's rule refuses nothing the writer would
    write: each destination it refuses, the public writer refuses too.

    Sample: each unusable destination above, checked by the pre-flight and then written by
    ``write_files_with_rollback`` with one short text.

    Expected outcome: both raise ModelFileError naming the destination; the writer leaves every
    file and folder as it was (no staged or backup file beside the destination).
    """
    destination = unusable_destination(tmp_path, case)
    before = the_tree(tmp_path)
    try:
        with pytest.raises(ModelFileError) as preflight:
            sat._check_destination(destination)
        with pytest.raises(ModelFileError) as writer:
            write_files_with_rollback([PendingWrite(destination, "NEW\n")])
    finally:
        unlock(tmp_path, case)
    assert preflight.value.path == writer.value.path == destination
    assert the_tree(tmp_path) == before


CommandRun = tuple[SaturationInputs, str]
"""What the patched computation was given on a command run: the inputs and the grid's SHA-256."""


def command_promotes(
    monkeypatch: pytest.MonkeyPatch, curve: SaturationCurve, scenario: Path, output: str | Path
) -> list[CommandRun]:
    """Run the saturation command (``main``) on a scenario and an output, its computation patched
    to return ``curve`` (a curve the module computed once), so a test of the command's
    destinations and its exit status costs no run; assert it exits 0 and return what the
    computation was given."""
    given: list[CommandRun] = []

    def computed(
        inputs: SaturationInputs, population: PopulationGrid, *, version_stamp: str
    ) -> SaturationCurve:
        given.append((inputs, population.sha256))
        return curve

    monkeypatch.setattr(sat, "compute_saturation", computed)
    assert sat.main([str(scenario), str(output)]) == EXIT_OK
    return given


def promotion_bytes(curve: SaturationCurve) -> bytes:
    """A curve's bytes as the promotion writes them."""
    return (render_artifact_json(curve) + ARTIFACT_FILE_END).encode("utf-8")


@pytest.mark.parametrize("where", ["an existing curve", "under missing folders"])
def test_the_command_writes_its_curve_over_an_existing_one_and_under_missing_folders(
    tmp_path: Path,
    iridium_yaml: Path,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    coarse_real_curve: SaturationCurve,
    where: str,
) -> None:
    """Objective: the command's destination checks let through what every promotion needs: an
    existing curve, which each re-promotion replaces, and a path under folders not yet made,
    which the shared writer creates; the command exits 0 with the curve written.

    Sample: the shipped scenario, the computation patched to return the coarse curve (computed
    once by this module's coarse promotion: the destination and the exit are under test, not the
    computation); the destination a file holding older bytes, or a path two missing folders down.

    Expected outcome: exit status 0 and no ERROR record; the destination holds the curve exactly
    as the promotion renders it, alone in its folder (the writer's staged file renamed away); the
    computation given the shipped scenario's inputs and the shipped grid.
    """
    if where == "an existing curve":
        destination = tmp_path / "saturation_curve.json"
        destination.write_text("OLD\n", encoding="utf-8")
    else:
        destination = tmp_path / "models" / "iridium" / "saturation_curve.json"
    given = command_promotes(monkeypatch, coarse_real_curve, iridium_yaml, destination)
    dials = iridium_dials_of(load_comms_config(iridium_yaml))
    assert given == [(saturation_inputs_for(dials), POPULATION_GRID_SHA256)]
    assert not [record for record in caplog.records if record.levelno >= logging.ERROR]
    assert destination.read_bytes() == promotion_bytes(coarse_real_curve)
    assert list(destination.parent.iterdir()) == [destination]


def test_a_relative_output_is_written_under_the_repository_root(
    tmp_path: Path,
    iridium_yaml: Path,
    repo_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    coarse_real_curve: SaturationCurve,
) -> None:
    """Objective: the command anchors a relative output path at the repository root, never the
    working directory, and reads the grid its inputs name there too (``SourceCheckout.anchored``).

    Sample: the shipped scenario, given by its absolute path; the command's source checkout
    patched to a temporary repository root that holds only a link to the shipped grid at its
    repository path; the working directory another temporary folder; the output
    ``communications/models/iridium/saturation_curve.json``, relative; the computation patched to
    return the coarse curve.

    Expected outcome: exit status 0; the curve written under the temporary root at that path,
    as the promotion renders it (its folders made); the working directory still empty; the
    computation given the shipped grid, read through the root's link.
    """
    root = tmp_path / "checkout"
    grid_link = root / POPULATION_GRID_PATH
    grid_link.parent.mkdir(parents=True)
    grid_link.symlink_to(repo_dir / POPULATION_GRID_PATH)
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    monkeypatch.setattr(sat, "locate_source_checkout", lambda module_file: SourceCheckout(root))
    relative = Path("communications/models/iridium/saturation_curve.json")
    given = command_promotes(monkeypatch, coarse_real_curve, iridium_yaml, relative)
    assert [sha256 for _, sha256 in given] == [POPULATION_GRID_SHA256]
    assert (root / relative).read_bytes() == promotion_bytes(coarse_real_curve)
    assert list(work.iterdir()) == []


POOL_TERMINATED = (
    "A process in the process pool was terminated abruptly while the future was running or pending."
)
"""The message a process pool breaks with when one of its workers dies."""

WORKER_OUT_OF_MEMORY = (
    "Unable to allocate 7.11 PiB for an array with shape (999999993568952,) and data type int64"
)
"""numpy's message for an allocation no machine can make (the cross-process test's real one)."""

UNPICKLING_CAUSE = (
    "\n'''\nTraceback (most recent call last):\n  File \"connection.py\", line 1, in recv\n"
    "_pickle.UnpicklingError: pickle data was truncated\n'''"
)
"""A process pool's cause as it fences it: the formatted traceback of a failure in this
process (here, receiving a result), between triple quotes."""


def broken_pool_with_a_cause() -> BrokenProcessPool:
    """A process pool broken by a failure in this process, with its fenced cause attached."""
    broken = BrokenProcessPool(POOL_TERMINATED)
    broken.__cause__ = Exception(UNPICKLING_CAUSE)
    return broken


@pytest.mark.parametrize(
    ("failure", "reason"),
    [
        (
            lambda: BrokenProcessPool(POOL_TERMINATED),
            "a saturation worker died during a sweep of 27 snapshot tasks, most likely out of "
            "memory",
        ),
        (
            lambda: sat._WorkerMemoryError(WORKER_OUT_OF_MEMORY),
            "a saturation worker ran out of memory during a sweep of 27 snapshot tasks "
            f"({WORKER_OUT_OF_MEMORY})",
        ),
        (
            broken_pool_with_a_cause,
            "the saturation sweep's process pool broke during a sweep of 27 snapshot tasks "
            "(_pickle.UnpicklingError: pickle data was truncated)",
        ),
    ],
    ids=["a dead worker", "a worker out of memory", "a pool broken with a cause"],
)
def test_a_failed_sweep_is_one_error_line(
    tmp_path: Path,
    iridium_yaml: Path,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    failure: Callable[[], Exception],
    reason: str,
) -> None:
    """Objective: a sweep that fails (a saturation worker that dies, most likely killed out of
    memory; one that runs out of memory itself; or the process pool broken by a stated cause in
    this process) ends the command with one ERROR line, never a traceback, and only a worker's
    own failure is blamed on a worker.

    Sample: the shipped scenario at the coarse setting (nine curves at three fleets and one
    snapshot: 27 snapshot tasks), with the sweep's first pool patched to raise what the process
    pool raises in each case: ``BrokenProcessPool`` with no cause, the worker's marked
    MemoryError, ``BrokenProcessPool`` with a fenced cause (an unpickling error).

    Expected outcome: exit status 1; exactly one ERROR record, on one line, with no exception
    attached, naming the scenario, the sweep's task count and what failed (the cause's own line
    for a broken pool, with no worker named), and saying nothing was written; no file written.
    """

    def fails(*args: object, **kwargs: object) -> None:
        raise failure()

    monkeypatch.setattr(sat, "saturation_inputs_for", coarse_inputs_for)
    monkeypatch.setattr(sat, "_run_alone", fails)
    out_path = tmp_path / "saturation_curve.json"
    assert sat.main([str(iridium_yaml), str(out_path)]) == EXIT_ERROR
    errors = [record for record in caplog.records if record.levelno >= logging.ERROR]
    assert len(errors) == 1
    assert errors[0].exc_info is None
    assert (len(DeviceClass) + len(BandName)) * len(COARSE_REAL_FLEETS) == 27
    assert errors[0].getMessage() == (
        f"could not promote the saturation curve from {iridium_yaml}: {reason}; nothing was written"
    )
    assert not out_path.exists()


def test_a_memory_error_of_the_command_itself_is_not_blamed_on_a_worker(
    tmp_path: Path,
    iridium_yaml: Path,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Objective: the sweep's error names a worker only for a worker's own failure: a
    MemoryError the command's own process raises outside the pool's manager thread is left as
    it is (one there breaks the pool and is named as its cause).

    Sample: the shipped scenario at the coarse setting, with the sweep's first pool patched to
    raise a bare MemoryError, as this process's own allocation would (a worker's arrives marked).

    Expected outcome: the MemoryError itself leaves the command; no ERROR record, so no line
    blames a worker; no file written.
    """

    def runs_out(*args: object, **kwargs: object) -> None:
        raise MemoryError

    monkeypatch.setattr(sat, "saturation_inputs_for", coarse_inputs_for)
    monkeypatch.setattr(sat, "_run_alone", runs_out)
    out_path = tmp_path / "saturation_curve.json"
    with pytest.raises(MemoryError):
        sat.main([str(iridium_yaml), str(out_path)])
    assert not [record for record in caplog.records if record.levelno >= logging.ERROR]
    assert not out_path.exists()


def test_the_sweeps_error_survives_a_pickle_round_trip_and_a_copy() -> None:
    """Objective: the sweep's public error can cross a process boundary and be copied, so a
    caller running the computation in a pool of its own sees the sweep's message, never a
    TypeError rebuilding it.

    Sample: ``SaturationSweepError`` with a one-line message and a task count of 27.

    Expected outcome: a pickle round trip and ``copy.copy`` each give the same type, message and
    task count.
    """
    error = sat.SaturationSweepError(
        "a saturation worker died during a sweep of 27 snapshot tasks, most likely out of memory",
        27,
    )
    pickled = pickle.dumps(error)
    unpickled = pickle.loads(pickled)  # noqa: S301 (the bytes this test itself pickled)
    for rebuilt in (unpickled, copy.copy(error)):
        assert type(rebuilt) is sat.SaturationSweepError
        assert str(rebuilt) == str(error)
        assert rebuilt.task_count == error.task_count


UNBUILDABLE_FLEET = 10**15
"""A requested fleet no machine can hold: its shell's first array of that size (8 PB) is refused
at once, after a 0.25 GB array of its planes."""


def phone_snapshot_task(fleet_index: int, requested_fleet: int) -> sat._SnapshotTask:
    """One phone-class snapshot task at the draw's first snapshot, pricing no trim."""
    return sat._SnapshotTask(
        curve=PHONE,
        fleet_index=fleet_index,
        requested_fleet=requested_fleet,
        snapshot_index=0,
        time_s=0.0,
        prices_trim=False,
    )


def one_patch_context(synthetic_population_grid: GridBuilder) -> sat._SweepContext:
    """A phone-class snapshot context on one populated 2 degree cell (the default shell, B = 1)."""
    cells = sat._demand_cells(synthetic_population_grid(2.0, patch_people(2.0, 0)), 1.0)
    return sat._SweepContext(
        shell=ShellInputs(), cells=cells, limits=seam_limits(1.0), trim=TrimInputs()
    )


def test_a_workers_memory_error_is_marked_as_the_workers(
    monkeypatch: pytest.MonkeyPatch, synthetic_population_grid: GridBuilder
) -> None:
    """Objective: a pool's worker marks its own MemoryError, so the parent can tell it from one
    of its own, and passes every result through unchanged.

    Sample: the worker's entry, ``_run_snapshot_in_worker``, called in this process on one
    phone-class task, with ``_run_snapshot`` patched to raise numpy's out-of-memory message, then
    unpatched.

    Expected outcome: ``_WorkerMemoryError`` carrying numpy's message, the MemoryError as its
    cause; unpatched, the snapshot's own result (equal to ``_run_snapshot``'s).
    """
    task = phone_snapshot_task(0, 342)
    context = one_patch_context(synthetic_population_grid)
    unmarked = sat._run_snapshot(task, context)
    with monkeypatch.context() as patch:

        def raises(*args: object) -> sat._SnapshotResult:
            raise MemoryError(WORKER_OUT_OF_MEMORY)

        patch.setattr(sat, "_run_snapshot", raises)
        with pytest.raises(sat._WorkerMemoryError, match=r"Unable to allocate 7\.11 PiB") as marked:
            sat._run_snapshot_in_worker(task, context)
    assert isinstance(marked.value.__cause__, MemoryError)
    passed = sat._run_snapshot_in_worker(task, context)
    assert dataclasses.replace(passed, worker_peak_mb=unmarked.worker_peak_mb) == unmarked


def test_a_workers_memory_error_crosses_the_process_boundary_as_the_sweeps_error(
    synthetic_population_grid: GridBuilder,
) -> None:
    """Objective: a real worker's MemoryError reaches the parent as the sweep's own error, its
    message and the task count with it (the pool pickles the worker's exception and raises it
    again here).

    Sample: two phone-class snapshot tasks of 10^15 satellites run by ``_run_sweep`` in a spawned
    worker: the shell's first array of that size (8 PB) is refused at once, after a 0.25 GB array
    of its planes, so the worker raises numpy's real MemoryError.

    Expected outcome: ``SaturationSweepError`` (a ValueError) carrying the task count 2 and
    saying a saturation worker ran out of memory, with numpy's message.
    """
    tasks = [phone_snapshot_task(index, UNBUILDABLE_FLEET + index) for index in range(2)]
    context = one_patch_context(synthetic_population_grid)
    with pytest.raises(sat.SaturationSweepError) as failed:
        sat._run_sweep(tasks, {PHONE: context})
    assert isinstance(failed.value, ValueError)
    assert failed.value.task_count == 2
    assert str(failed.value).startswith(
        "a saturation worker ran out of memory during a sweep of 2 snapshot tasks (Unable to "
        "allocate"
    )
    assert str(failed.value).endswith("); nothing was written")


def test_the_command_exits_with_the_usage_status_on_a_usage_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Objective: a usage error follows the shared convention.

    Sample: the command with no arguments.

    Expected outcome: exit status 2 with the usage line on stderr.
    """
    with pytest.raises(SystemExit) as stopped:
        sat.main([])
    assert stopped.value.code == EXIT_USAGE
    assert "usage: python -m communications.saturation" in capsys.readouterr().err


def test_the_narrowing_function_returns_the_iridium_dials_or_refuses_a_cellular_config(
    iridium_yaml: Path,
) -> None:
    """Objective: one function narrows a config to its Iridium dials, and refuses a config of
    the cellular family with the Iridium promotion command's own message, as a ValueError.

    Sample: the shipped Iridium scenario; the default config (no ``iridium:`` block).

    Expected outcome: the scenario's own ``iridium`` block back; for the default config,
    NotAnIridiumConfigError with today's message, word for word.
    """
    config = load_comms_config(iridium_yaml)
    assert iridium_dials_of(config) is config.iridium
    with pytest.raises(NotAnIridiumConfigError) as refused:
        iridium_dials_of(CommsConfig())
    assert str(refused.value) == (
        "the scenario does not select the Iridium model: it needs a top-level "
        "'iridium:' block (see scenarios/iridium.yaml)"
    )
    assert isinstance(refused.value, ValueError)


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


ROW_BEAMS_PER_SATELLITE = 150.0
"""B at the default inputs (1,000 x the 0.15 calibration at the 25 m^2 reference panel), at
which a hand-built row's ocean factor is U = L / (N x B), as the computation writes it."""


def _row(fleet: int, useful: float, capacity: float) -> CurveRow:
    """A bare curve row for the checks' refusals, requested at its own realized fleet (each
    fleet used here realizes as itself when requested), its ceiling and supply equal to L and its
    ocean factor L / (N x B) at the default B."""
    return CurveRow(
        fleet=fleet,
        requested_fleet=fleet,
        useful_beams=useful,
        useful_beams_spread=0.0,
        capacity_gbps=capacity,
        ocean_factor=useful / (fleet * ROW_BEAMS_PER_SATELLITE),
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
        (
            lambda: sat._markers(
                PHONE, rows_with_elasticities(MARKER_FLEETS, (0.60, 0.09, 0.40), (1.0,) * 4), 10.0
            ),
            r"phone_class: the elasticity falls under 0.1 at the midpoint 1401 \(0.0900\) and is "
            r"back at 0.4000 at the later midpoint 2803",
        ),
        (
            lambda: sat._markers(
                BandName.TAPER,
                rows_with_elasticities(MARKER_FLEETS, (0.60, 0.24, 0.40), (1.0,) * 4),
                10.0,
            ),
            r"phone_class band point taper: the elasticity falls under 0.25 at the midpoint 1401 "
            r"\(0.2400\) and is back at 0.4000 at the later midpoint 2803",
        ),
        (
            lambda: sat._markers(
                PHONE, rows_with_elasticities(MARKER_FLEETS, (0.60, -0.10, 0.40), (1.0,) * 4), 10.0
            ),
            r"phone_class: capacity falls from .* Gbps at 992 satellites to .* Gbps at 1980 "
            r"\(an elasticity of -0.1000 at their midpoint\)",
        ),
    ],
    ids=[
        "L above min(ceiling, supply)",
        "ceiling above maximum use",
        "stalled allocation",
        "capacity per satellite rising",
        "saturation before the first midpoint",
        "the elasticity back over 0.10 after its crossing",
        "the elasticity back over 0.25 after its crossing",
        "capacity falling between rows",
    ],
)
def test_each_check_refuses_a_curve_that_breaks_it(
    refused: Callable[[], object], message: str
) -> None:
    """Objective: the guards fire: each check raises its typed error on a curve breaking it.

    Sample: hand-built snapshots or rows: L above min(ceiling, supply); a ceiling above
    maximum use; L at 0.90 of its bound at 20,022 satellites against the 0.98 floor; capacity
    per satellite rising from 1.0 / 342 to 4.0 / 992; an elasticity of 0.01 at the first
    midpoint (the saturation number cannot be placed); rows at 342, 992, 1,980 and 3,969
    whose elasticity runs 0.60, 0.09, 0.40 (under 0.10 at the midpoint 1,401, back over it at
    2,803), 0.60, 0.24, 0.40 (the same for 0.25, on a band point) and 0.60, -0.10, 0.40 (capacity
    falling from 992 to 1,980 satellites).

    Expected outcome: SaturationInvariantError, its message naming the breach: the curve, and
    for a crossing that does not hold the threshold, both midpoints and both elasticities, or
    for a fall the two rows and the elasticity between them.
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

    Sample: the default Iridium dials (a 15.4 m^2 panel); the same with the 25 m^2 reference
    panel and with a 10 m^2 panel, each another panel than the default; the same with 10.5 MHz.

    Expected outcome: the default dials give ``SaturationInputs()``, its classes in
    ``DeviceClass`` order and its band points in ``BandName`` order; another panel changes
    nothing (the engine applies it); the spectrum changes ``spectrum_mhz`` alone, and the
    input hash with it; the hash survives a JSON round trip.
    """
    default = SaturationInputs()
    assert IridiumDials().aperture_m2 == APERTURE_M2_DEFAULT == 15.4
    assert saturation_inputs_for(IridiumDials()) == default
    assert [entry.device_class for entry in default.classes] == list(DeviceClass)
    assert [point.name for point in default.bands] == list(BandName)
    for panel_m2 in (25.0, 10.0):
        assert saturation_inputs_for(IridiumDials(aperture_m2=panel_m2)) == default
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


BRUTE_FORCE_CHUNK_SATELLITES = 50
"""Satellites the brute-force search tests against every cell at once: at 0.5 degree cells
(259,200) a chunk's cosines take about 100 MB."""


def brute_force_pair_keys(
    satellites: sat._SatellitePositions, cells: sat._DemandCells, limit_rad: float, slack: float
) -> np.ndarray:
    """Every pair whose cosine is at least cos(limit) + slack, by testing every cell against
    every satellite (a chunk of satellites at a time), as sorted keys satellite x (cells + 1) +
    cell."""
    satellite_xyz = sat._unit_vectors(satellites.lat_rad, satellites.lon_rad)
    keys = []
    for start in range(0, satellites.count, BRUTE_FORCE_CHUNK_SATELLITES):
        cosine = cells.xyz @ satellite_xyz[start : start + BRUTE_FORCE_CHUNK_SATELLITES].T
        cell, satellite = np.nonzero(cosine >= math.cos(limit_rad) + slack)
        keys.append((satellite.astype(np.int64) + start) * (cells.count + 1) + cell)
    return np.sort(np.concatenate(keys))


def everywhere_people(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    """One resident in every cell."""
    return np.ones_like(lat)


@pytest.mark.parametrize(
    ("shell", "cell_deg", "times_s"),
    [
        (ShellInputs(), 1.0, (0.0, 4321.0)),
        (NARROW_VIEW_SHELL, 1.0, (0.0, 4321.0)),
        (ShellInputs(), 0.5, (0.0,)),
    ],
    ids=["central", "narrow view", "central, 0.5 degree cells"],
)
def test_pair_search_finds_exactly_the_pairs_a_brute_force_search_finds(
    synthetic_population_grid: Callable[[float, PeopleAt], PopulationGrid],
    shell: ShellInputs,
    cell_deg: float,
    times_s: tuple[float, ...],
) -> None:
    """Objective: the windowed pair search misses no pair in view and keeps none out of view,
    at the poles and across the antimeridian too, at the grid's cell sizes; no runtime check
    could see a miss, since L, the ceiling and the supply are built on the same pairs.

    Sample: every cell populated: 1 degree cells for the central shell and a narrow-view shell
    (300 km, a 60 degree mask), each at 400 requested satellites at two times; and 0.5 degree
    cells (the 0.5 degree band point sums the shipped 0.25 degree grid to them) for the central
    shell at one time; each with satellites placed at and near both poles and across the
    antimeridian.

    Expected outcome: the pairs equal a brute-force search over every cell and satellite, up
    to pairs within 1e-12 of the limit in cosine, each listed once, ordered by satellite then
    cell.
    """
    cells = sat._demand_cells(synthetic_population_grid(cell_deg, everywhere_people), 1e-12)
    limit = sat._central_angle_limit(shell)
    shells = [sat._walker_positions(shell, 400, time_s) for time_s in times_s]
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


BARE_LAST_MIDPOINT = 582
"""The bare rows' one midpoint, sqrt(342 x 992) = 582.46, rounded half up: the fleet bare markers
with no crossing are not reached by."""


def test_the_saturation_number_is_the_first_crossing_under_0p10_interpolated_in_ln_n(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Objective: the saturation number's rule, worked by hand: the elasticity of capacity at the
    rows' geometric midpoints, its first crossing under 0.10 interpolated in ln N between the two
    midpoints that straddle it, rounded half up; and an elasticity of exactly 0.10 is no crossing
    (the rule is strictly under).

    Sample: rows at 342, 992 and 1,980 satellites whose capacity's elasticity is 0.20 and 0.05
    over the two intervals; then the same rows read with the elasticity exactly 0.20 and 0.10 at
    their midpoints (the module's elasticity patched, since no rows give exactly 0.10 in floating
    point: log 2 / log 1,024 is 0.09999999999999999), and the rule's own crossing at 0.10 and at
    the float just under it.

    Expected outcome, worked by hand: the midpoints sqrt(342 x 992) = 582.464 and sqrt(992 x
    1,980) = 1,401.485; the crossing lies (0.20 - 0.10) / (0.20 - 0.05) = 2/3 of the way between
    them in ln N, 582.464 x (1,401.485 / 582.464)^(2/3) = 1,045.88, so the saturation number is
    1,046 (an interpolation linear in N would give 1,128). At exactly 0.10 there is no crossing:
    no saturation number, not reached by the last midpoint, 1,401; the float just under 0.10
    crosses at the last midpoint.
    """
    fleets = (342, 992, 1_980)
    rows = rows_with_elasticities(fleets, (0.20, 0.05), (100.0, 200.0, 300.0))
    markers = sat._markers(PHONE, rows, 1_000.0)
    assert markers.saturation_number == 1_046
    assert markers.saturation_not_reached_by is None
    midpoints = [math.sqrt(low * high) for low, high in pairwise(fleets)]
    assert midpoints == pytest.approx([582.464, 1_401.485], abs=1e-3)
    by_hand = midpoints[0] * (midpoints[1] / midpoints[0]) ** (2 / 3)
    assert by_hand == pytest.approx(1_045.88, abs=0.01)
    assert round_half_up(midpoints[0] + 2 / 3 * (midpoints[1] - midpoints[0])) == 1_128
    exact = [0.20, 0.10]
    assert sat._first_crossing_under(midpoints, exact, 0.10, "exactly 0.10") is None
    just_under = [0.20, math.nextafter(0.10, 0.0)]
    crossing = sat._first_crossing_under(midpoints, just_under, 0.10, "just under 0.10")
    assert crossing == pytest.approx(midpoints[1], rel=1e-12)
    monkeypatch.setattr(sat, "_elasticity", lambda curve, rows: (midpoints, exact))
    at_exactly = sat._markers(PHONE, rows, 1_000.0)
    assert at_exactly.saturation_number is None
    assert at_exactly.saturation_not_reached_by == 1_401


def test_a_saturation_number_not_reached_names_the_last_midpoint_the_rows_measure() -> None:
    """Objective: when the elasticity of capacity is under 0.10 at no midpoint, the curve has no
    saturation number, and the fleet it is not reached by is the last midpoint at which its rows
    measure the elasticity, never the last row's fleet: past that midpoint the rows measure
    nothing (ADR 005).

    Sample: hand-built rows at 342, 992, 1,980 and 3,969 satellites whose capacity's elasticity is
    0.60, 0.40 and 0.30 over the three intervals (never under 0.10, nor under 0.25), with L far
    under 90 percent of maximum use.

    Expected outcome, worked by hand: no saturation number; not reached by sqrt(1,980 x 3,969) =
    sqrt(7,858,620) = 2,803.32, rounded half up to 2,803, not by the last row's 3,969; no
    crossing under 0.25 and no 90 percent fleet.
    """
    rows = rows_with_elasticities(MARKER_FLEETS, (0.60, 0.40, 0.30), (100.0, 200.0, 300.0, 400.0))
    markers = sat._markers(PHONE, rows, 1_000.0)
    assert markers.saturation_number is None
    assert markers.saturation_not_reached_by == 2_803
    assert markers.saturation_not_reached_by != rows[-1].fleet == 3_969
    assert markers.elasticity_under_0p25_fleet is None
    assert markers.fleet_at_90pct_of_maximum_use is None


def bare_markers(**changes: int | None) -> ClassMarkers:
    """Markers with no crossing (not reached by the bare rows' midpoint, 582), but for the changes
    asked."""
    fields: dict[str, float | int | None] = {
        "maximum_use_beams": 1_000.0,
        "saturation_number": None,
        "saturation_not_reached_by": BARE_LAST_MIDPOINT,
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


COMPLETE_FLEETS = (342, 992)
"""The complete bare curve's requested fleets: each realizes as itself (18 x 19, 31 x 32)."""


NO_STACK = DirectionalDiagnostics(
    kept_stacked_share=0.0, median_separation_deg=None, mean_full_sum_interference_db=None
)
"""A directional row's diagnostics when it keeps no stacked beam."""


def band_rows(point: BandPoint) -> tuple[CurveRow, ...]:
    """The bare rows for a band point: its ocean factor at the point's own B when it sets one
    (the 48-beam point), else the bare rows as they are."""
    if point.beams_per_satellite is None:
        return BARE_ROWS
    return tuple(
        row.model_copy(
            update={"ocean_factor": row.useful_beams / (row.fleet * point.beams_per_satellite)}
        )
        for row in BARE_ROWS
    )


def complete_bare_curve() -> SaturationCurve:
    """A complete curve on hand-built rows: the default inputs but for the sweep (fleets 342
    and 992, no mounted extension), every class and every band point on the two bare rows (the
    48-beam point's ocean factor at its own B), the directional classes' rows with their
    diagnostics, the phone class's rows with a trim at the default floors, one citation, one
    stated limit and one check passed."""
    inputs = SaturationInputs(
        sweep=SweepInputs(fleets=COMPLETE_FLEETS, mounted_terminal_extension=())
    )
    trim = tuple(TrimAtFloor(floor_dbi=floor, trim=0.01) for floor in inputs.trim.floors_dbi)
    phone_rows = tuple(row.model_copy(update={"trim": trim}) for row in BARE_ROWS)
    directional_rows = tuple(row.model_copy(update={"directional": NO_STACK}) for row in BARE_ROWS)
    curve = bare_curve(
        tuple(
            ClassCurve(
                device_class=device_class,
                rows=phone_rows if device_class is PHONE else directional_rows,
                markers=bare_markers(),
            )
            for device_class in DeviceClass
        ),
        tuple(
            BandCurve(point=point, rows=band_rows(point), markers=bare_markers())
            for point in inputs.bands
        ),
    )
    return curve.model_copy(
        update={
            "parameters": inputs,
            "input_hash": curve_input_hash(inputs),
            "provenance": curve.provenance.model_copy(
                update={"checks_passed": ("a check",), "citations": ("a citation",)}
            ),
            "limits": ("a stated limit",),
        }
    )


def write_curve_json(path: Path, data: object) -> Path:
    """Write a curve's JSON document to a file and return the path."""
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def test_a_complete_curve_passes_its_check_and_loads(tmp_path: Path) -> None:
    """Objective: what the promotion writes, the loader reads back whole.

    Sample: the complete bare curve, written as the promotion renders it.

    Expected outcome: ``check_curve_complete`` passes it, and ``load_saturation_curve`` returns
    a curve equal to it.
    """
    curve = complete_bare_curve()
    check_curve_complete(curve)
    path = tmp_path / "saturation_curve.json"
    path.write_text(render_artifact_json(curve) + ARTIFACT_FILE_END, encoding="utf-8")
    assert load_saturation_curve(path) == curve


def with_phone_markers(curve: SaturationCurve, **changes: float | int | None) -> SaturationCurve:
    """The curve with the phone class's markers changed as asked."""
    phone = curve.classes[2]
    return curve.model_copy(
        update={
            "classes": (
                *curve.classes[:2],
                phone.model_copy(update={"markers": phone.markers.model_copy(update=changes)}),
            )
        }
    )


@pytest.mark.parametrize(
    "changes",
    [
        {"saturation_number": 582, "saturation_not_reached_by": None},
        {"elasticity_under_0p25_fleet": 582},
        {"fleet_at_90pct_of_maximum_use": 342},
        {"fleet_at_90pct_of_maximum_use": 992},
    ],
    ids=[
        "a saturation number at the midpoint",
        "a 0.25 crossing at the midpoint",
        "a 90 percent fleet at the first row",
        "a 90 percent fleet at the last row",
    ],
)
def test_markers_at_the_edges_of_their_spans_pass_the_completeness_check(
    changes: dict[str, int | None],
) -> None:
    """Objective: the completeness check's conditions on the markers are necessary only, and its
    spans are the ones the markers' definitions give: a crossing between the rows' first and last
    geometric midpoints, each rounded half up; the 90 percent fleet within the rows' span.

    Sample: the complete bare curve (rows at 342 and 992: one midpoint, sqrt(342 x 992) = 582.46,
    582 rounded) with the phone class's markers at the edges of those spans.

    Expected outcome: each passes ``check_curve_complete`` (whether ``_markers`` would give it is
    the derived-fields drift test's to say, on the committed curve).
    """
    check_curve_complete(with_phone_markers(complete_bare_curve(), **changes))


SMALL_TERMINAL_SECTORS = next(
    entry.sector_wedges_per_ring
    for entry in SaturationInputs().classes
    if entry.device_class is DeviceClass.SMALL_TERMINAL_CLASS
)
"""The small terminal's default sky sectors: its azimuth wedges per ring, from the zenith down."""


def complete_curve_with_sectors(small: tuple[int, ...], phone: tuple[int, ...]) -> SaturationCurve:
    """The complete bare curve with the small terminal's and the phone class's sky sectors set in
    its parameters, each row's diagnostics placed as the computation places them (on every row of
    a class with sky sectors, a band point's by the phone class's) and its input hash recomputed."""
    curve = complete_bare_curve()
    layouts = {DeviceClass.SMALL_TERMINAL_CLASS: small, PHONE: phone}
    classes = tuple(
        entry.model_copy(update={"sector_wedges_per_ring": layouts[entry.device_class]})
        if entry.device_class in layouts
        else entry
        for entry in curve.parameters.classes
    )
    parameters = SaturationInputs.model_validate(
        {**curve.parameters.model_dump(), "classes": classes}
    )
    sectored = {entry.device_class: bool(entry.sector_wedges_per_ring) for entry in classes}

    def placed(rows: tuple[CurveRow, ...], diagnostics: bool) -> tuple[CurveRow, ...]:
        return tuple(
            row.model_copy(update={"directional": NO_STACK if diagnostics else None})
            for row in rows
        )

    return curve.model_copy(
        update={
            "parameters": parameters,
            "input_hash": curve_input_hash(parameters),
            "classes": tuple(
                entry.model_copy(update={"rows": placed(entry.rows, sectored[entry.device_class])})
                for entry in curve.classes
            ),
            "bands": tuple(
                band.model_copy(update={"rows": placed(band.rows, sectored[PHONE])})
                for band in curve.bands
            ),
        }
    )


@pytest.mark.parametrize(
    ("small", "phone", "flip", "message"),
    [
        ((), (), (0, None), "small_terminal_class row at 342 satellites carries stacking"),
        (
            SMALL_TERMINAL_SECTORS,
            (1,),
            (None, 0),
            "band point taper row at 342 satellites lacks its stacking diagnostics",
        ),
    ],
    ids=["an omni small terminal", "a sectored phone class"],
)
def test_the_diagnostics_sit_where_the_parameters_sky_sectors_put_them(
    tmp_path: Path,
    small: tuple[int, ...],
    phone: tuple[int, ...],
    flip: tuple[int | None, int | None],
    message: str,
) -> None:
    """Objective: the completeness check places the stacking diagnostics by each class's sky
    sectors in the curve's parameters, as the computation does, never by the class's name, so a
    curve computed from contract-valid inputs is never refused after the run.

    Sample: the complete bare curve with a small terminal of no sky sectors (its rows without
    diagnostics), or a phone class of one sector (its rows and every band point's with them);
    then the same curve with one row's diagnostics flipped (the small terminal's first row given
    them, or the first band point's first row stripped of them).

    Expected outcome: each curve passes ``check_curve_complete`` and loads; the flipped one is
    refused naming the curve and the row.
    """
    curve = complete_curve_with_sectors(small, phone)
    check_curve_complete(curve)
    path = tmp_path / "saturation_curve.json"
    path.write_text(render_artifact_json(curve) + ARTIFACT_FILE_END, encoding="utf-8")
    assert load_saturation_curve(path) == curve
    class_index, band_index = flip
    data = json.loads(render_artifact_json(curve))
    if class_index is not None:
        data["classes"][class_index]["rows"][0]["directional"] = NO_STACK.model_dump()
    if band_index is not None:
        data["bands"][band_index]["rows"][0]["directional"] = None
    flipped = write_curve_json(tmp_path / "flipped.json", data)
    with pytest.raises(SaturationCurveError, match=message):
        load_saturation_curve(flipped)


def test_a_grid_named_otherwise_with_the_parameters_digest_loads(tmp_path: Path) -> None:
    """Objective: the grid is identified by its digest alone, as the computation identifies it;
    its file name is a label the parameters' path already gives.

    Sample: the complete bare curve with its provenance's grid file name changed, its digest kept.

    Expected outcome: the curve passes ``check_curve_complete`` and loads.
    """
    curve = complete_bare_curve()
    renamed = curve.model_copy(
        update={"provenance": curve.provenance.model_copy(update={"grid_file_name": "other.npz"})}
    )
    check_curve_complete(renamed)
    path = write_curve_json(tmp_path / "renamed.json", json.loads(render_artifact_json(renamed)))
    assert load_saturation_curve(path).provenance.grid_file_name == "other.npz"


def test_one_bounds_tolerance_serves_the_computation_and_the_completeness_check() -> None:
    """Objective: the computation's bounds check and the completeness check read one tolerance
    through one predicate, so a retune moves both (a one-sided one would refuse the computation's
    own curve after the full run).

    Sample: the module's names for the tolerance and the predicate; the complete bare curve with
    the phone class's maximum use set under its last row's ceiling by half the tolerance and by
    twice it.

    Expected outcome: the module's names are the contract's own objects; the curve passes at half
    the tolerance and is refused at twice it.
    """
    assert sat._BOUNDS_RELATIVE_TOLERANCE is saturation_curve.BOUNDS_RELATIVE_TOLERANCE
    assert sat.exceeds_bound is saturation_curve.exceeds_bound
    curve = complete_bare_curve()
    ceiling = curve.classes[2].rows[-1].ceiling_beams
    tolerance = saturation_curve.BOUNDS_RELATIVE_TOLERANCE
    check_curve_complete(with_phone_markers(curve, maximum_use_beams=ceiling * (1 - tolerance / 2)))
    with pytest.raises(SaturationCurveError, match="above its maximum use"):
        check_curve_complete(
            with_phone_markers(curve, maximum_use_beams=ceiling * (1 - 2 * tolerance))
        )


@pytest.mark.parametrize(
    ("alter", "message"),
    [
        (
            lambda d: d["classes"][0]["rows"][0].update(
                useful_beams=0.0, capacity_gbps=0.0, ocean_factor=0.0
            ),
            "the small_terminal_class row at 342 satellites has its useful beams at 0.0, not "
            "above 0",
        ),
        (
            lambda d: d["classes"][1]["rows"][1].update(capacity_gbps=0.0),
            "the mounted_terminal_class row at 992 satellites has its capacity at 0.0, not above 0",
        ),
        (
            lambda d: d["classes"][2]["rows"][0].update(ocean_factor=0.0),
            "the phone_class row at 342 satellites has its ocean factor at 0.0, not above 0",
        ),
        (
            lambda d: d["bands"][5]["rows"][1].update(useful_beams=0.0),
            "the band point beams_48 row at 992 satellites has its useful beams at 0.0, not "
            "above 0",
        ),
        (
            lambda d: d["classes"][0]["markers"].update(maximum_use_beams=0.0),
            "the small_terminal_class maximum use is 0.0 beams, not above 0",
        ),
        (
            lambda d: d["bands"][0]["markers"].update(maximum_use_beams=0.0),
            "the band point taper maximum use is 0.0 beams, not above 0",
        ),
    ],
    ids=[
        "a class's first row zeroed",
        "a class row's capacity at 0",
        "a class row's ocean factor at 0",
        "a band point row's useful beams at 0",
        "a class's maximum use at 0",
        "a band point's maximum use at 0",
    ],
)
def test_the_completeness_check_refuses_a_row_or_a_maximum_use_not_above_zero(
    tmp_path: Path, alter: Callable[[dict[str, object]], object], message: str
) -> None:
    """Objective: a curve the engine reads holds no zero where the computation never writes one
    (amendment A9): every row's useful beams, capacity and ocean factor and every maximum use are
    above 0, for every class and band point, so a curve file with a zeroed row no longer loads
    and reads zeros silently at and below that row (the readings take logarithms between rows
    and divide by maximum use).

    Sample: the complete bare curve's JSON with one quantity set to 0 in turn: the small
    terminal's first row zeroed whole (L, capacity and U, the review's case), a mounted terminal
    row's capacity, a phone row's ocean factor, a band point row's useful beams, a class's and a
    band point's maximum use; each checked as a curve and loaded from a file.

    Expected outcome: ``check_curve_complete`` refuses each with a SaturationCurveError naming
    the curve, the row (or its maximum use), the quantity and its value; the loader refuses the
    file with the same words after the file's path.
    """
    data = json.loads(render_artifact_json(complete_bare_curve()))
    alter(data)
    with pytest.raises(SaturationCurveError) as refused:
        check_curve_complete(SaturationCurve.model_validate(data))
    assert str(refused.value) == message
    path = write_curve_json(tmp_path / "zeroed.json", data)
    with pytest.raises(SaturationCurveError) as refused_at_load:
        load_saturation_curve(path)
    assert str(refused_at_load.value) == f"{path}: {message}"


def _phone_trim_json() -> list[dict[str, float]]:
    """The complete bare curve's phone trim, as JSON."""
    return [{"floor_dbi": floor, "trim": 0.01} for floor in SaturationInputs().trim.floors_dbi]


@pytest.mark.parametrize(
    ("alter", "message"),
    [
        (lambda d: d.update(input_hash="0" * 64), "the input hash 0000"),
        (lambda d: d["parameters"].update(spectrum_mhz=10.5), "the parameters or the hash"),
        (lambda d: d.update(schema_version="saturation-v2"), "schema is 'saturation-v2'"),
        (lambda d: d.update(classes=d["classes"][:2]), r"lacks the classes \['phone_class'\]"),
        (lambda d: d.update(bands=d["bands"][1:]), r"lacks the band points \['taper'\]"),
        (lambda d: d["classes"][2]["rows"][0].update(trim=None), "342 satellites lacks its trim"),
        (
            lambda d: d["classes"][0]["rows"][1].update(trim=_phone_trim_json()),
            "small_terminal_class row at 992 satellites carries a trim",
        ),
        (
            lambda d: d["bands"][5]["rows"][0].update(trim=_phone_trim_json()),
            "band point beams_48 row at 342 satellites carries a trim",
        ),
        (
            lambda d: d["classes"][2]["rows"][1]["trim"].pop(),
            r"floors \[-0.4, -2.0\], not the parameters' \[-0.4, -2.0, -8.0\]",
        ),
        (
            lambda d: d["bands"][0]["point"].update(beamwidth_factor=1.2),
            "band point taper is",
        ),
        (
            lambda d: d["classes"][1].update(rows=d["classes"][1]["rows"][:1]),
            r"mounted_terminal_class rows stand at the requested fleets \[342\]",
        ),
        (
            lambda d: d.update(classes=[d["classes"][1], d["classes"][0], d["classes"][2]]),
            r"not a saturation curve \(classes must hold each member at most once",
        ),
        (
            lambda d: d["classes"][2]["rows"][0].update(requested_fleet="342"),
            "requested_fleet: Input should be a valid integer",
        ),
        (
            lambda d: d["classes"][2]["rows"][0].update(fleet=342.0),
            "fleet: Input should be a valid integer",
        ),
        (
            lambda d: (
                d["parameters"]["bands"][0].update(grid_aggregation=True),
                d["bands"][0]["point"].update(grid_aggregation=True),
            ),
            "grid_aggregation: Input should be a valid integer",
        ),
        (
            lambda d: d["parameters"].update(spectrum_mhz="8.0"),
            "spectrum_mhz: Input should be a valid number",
        ),
        (
            lambda d: d["classes"][2]["rows"][0].update(useful_beams=float("nan")),
            "finite number",
        ),
        (lambda d: d["parameters"].update(sidelobe_floor_db=float("-inf")), "finite number"),
        (
            lambda d: d["classes"][2]["rows"][0].update(requested_fleet=10**309),
            "a number out of range: a row's requested_fleet is too large to build its shell from",
        ),
        (
            lambda d: d["classes"][0]["rows"][0].update(directional=None),
            "small_terminal_class row at 342 satellites lacks its stacking diagnostics",
        ),
        (
            lambda d: d["classes"][2]["rows"][0].update(directional=NO_STACK.model_dump()),
            "phone_class row at 342 satellites carries stacking diagnostics",
        ),
        (
            lambda d: d["bands"][0]["rows"][1].update(directional=NO_STACK.model_dump()),
            "band point taper row at 992 satellites carries stacking diagnostics",
        ),
        (lambda d: d.update(limits=[]), "the curve states no limits"),
        (lambda d: d["provenance"].update(checks_passed=[]), "names no checks passed"),
        (
            lambda d: d["provenance"].update(grid_sha256="0" * 64),
            "the provenance's grid digest 0000",
        ),
        (
            lambda d: d["bands"][5]["markers"].update(saturation_not_reached_by=992),
            "band point beams_48 saturation_not_reached_by is 992, not its last measured "
            r"midpoint, 582 \(the geometric mean of its last two rows' fleets, rounded half up\)",
        ),
        (
            lambda d: d["classes"][1]["markers"].update(saturation_not_reached_by=500),
            "mounted_terminal_class saturation_not_reached_by is 500, not its last measured "
            "midpoint, 582",
        ),
        (
            lambda d: d["classes"][0]["markers"].update(
                saturation_number=5_000, saturation_not_reached_by=None
            ),
            "saturation_number 5000 lies outside the span of its rows' geometric midpoints, 582 "
            "to 582",
        ),
        (
            lambda d: d["classes"][0]["markers"].update(
                saturation_number=500, saturation_not_reached_by=None
            ),
            "saturation_number 500 lies outside the span of its rows' geometric midpoints",
        ),
        (
            lambda d: d["bands"][1]["markers"].update(elasticity_under_0p25_fleet=900),
            "band point taper_and_spacing elasticity_under_0p25_fleet 900 lies outside the span",
        ),
        (
            lambda d: d["classes"][1]["markers"].update(fleet_at_90pct_of_maximum_use=1_000),
            "fleet_at_90pct_of_maximum_use 1000 lies outside its rows' span, 342 to 992",
        ),
        (
            lambda d: d["classes"][2]["markers"].update(maximum_use_beams=15.0),
            "phone_class row at 992 satellites has a ceiling of 20.0 beams, above its maximum use",
        ),
        (
            lambda d: d["classes"][2]["rows"][1].update(useful_beams=40.0),
            r"phone_class row at 992 satellites has useful beams of 40.0, above min\(ceiling 20.0, "
            r"supply 20.0\)",
        ),
        (
            lambda d: d["classes"][2]["rows"][0].update(ocean_factor=0.9),
            "phone_class row at 342 satellites has an ocean factor of 0.9, not its useful beams "
            "over its fleet's beams",
        ),
        (
            lambda d: d["bands"][5]["rows"][0].update(ocean_factor=10.0 / (342 * 150.0)),
            r"band point beams_48 row at 342 satellites has an ocean factor of .*, not its useful "
            r"beams over its fleet's beams, .* \(U = L / \(N x B\), B 48\)",
        ),
        (
            lambda d: d["provenance"].update(citations=[]),
            "the curve's provenance names no citation, or a blank one",
        ),
        (
            lambda d: d["provenance"].update(citations=["a citation", " "]),
            "the curve's provenance names no citation, or a blank one",
        ),
        (lambda d: d["provenance"].update(licence=" "), "the curve's provenance states no licence"),
        (lambda d: d["provenance"].update(method=""), "the curve's provenance states no method"),
    ],
    ids=[
        "an altered input hash",
        "an altered parameter",
        "an unknown schema",
        "a class missing",
        "a band point missing",
        "a phone row without its trim",
        "a directional row with a trim",
        "a band row with a trim",
        "a trim at other floors",
        "a band point not its parameters'",
        "rows missing",
        "a curve the contract refuses",
        "a fleet written as a string",
        "a fleet written as a float",
        "a count written as true",
        "a number written as a string",
        "NaN in a row",
        "minus infinity in a parameter",
        "a requested fleet out of range",
        "a directional row without its diagnostics",
        "a phone row with diagnostics",
        "a band row with diagnostics",
        "no stated limits",
        "no checks passed",
        "a grid digest not the parameters'",
        "not reached by the last row's fleet, past the last midpoint",
        "not reached by a fleet that is no midpoint",
        "a saturation number outside the rows",
        "a saturation number before the first midpoint",
        "a 0.25 crossing past the last midpoint",
        "a 90 percent fleet past the last row",
        "maximum use under a row's ceiling",
        "useful beams above min(ceiling, supply)",
        "an ocean factor not L / (N x B)",
        "the 48-beam point's ocean factor at the central B",
        "no citation",
        "a blank citation",
        "a blank licence",
        "no method",
    ],
)
def test_the_loader_refuses_a_curve_the_engine_must_not_read(
    tmp_path: Path, alter: Callable[[dict[str, object]], object], message: str
) -> None:
    """Objective: ``load_saturation_curve`` refuses a promoted curve whose parameters or hash
    were altered, one of another schema, one the contract refuses (a value of another JSON type
    than the contract writes, a NaN or an infinity, a number out of range), an incomplete one
    (diagnostics or a trim misplaced, no limits or checks, no citation, licence or method, a grid
    not the parameters'), one whose rows break what every computed row holds (useful beams above
    min(ceiling, supply), so possibly above maximum use; an ocean factor not L / (N x B) at the
    curve's B, the 48-beam point's own) and one whose markers its rows cannot give, each with a
    SaturationCurveError (a ValueError, so both commands catch it) naming the file.

    Sample: the complete bare curve's JSON with one change each.

    Expected outcome: SaturationCurveError whose message names the file and the breach.
    """
    data = json.loads(render_artifact_json(complete_bare_curve()))
    alter(data)
    path = write_curve_json(tmp_path / "altered.json", data)
    with pytest.raises(SaturationCurveError, match=message) as refused:
        load_saturation_curve(path)
    assert str(path) in str(refused.value)
    assert isinstance(refused.value, ValueError)
    assert "(: " not in str(refused.value)
    assert "Value error" not in str(refused.value)


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        (
            '"schema_version": "saturation-v1",',
            '"schema_version": "saturation-v2",\n  "schema_version": "saturation-v1",',
            "the key 'schema_version' appears twice in one JSON object",
        ),
        ('"capacity_gbps": 1.0,', '"capacity_gbps": 1e999,', "finite number"),
        ('"a stated limit"', '"\\ud800a stated limit"', r"not a saturation curve \(Invalid JSON"),
        (
            '"requested_fleet": 342,',
            f'"requested_fleet": 1{"0" * 4_999},',
            "a number out of range: Exceeds the limit",
        ),
    ],
    ids=[
        "a key written twice",
        "a number too large for a float",
        "a lone surrogate",
        "an integer past Python's digit limit",
    ],
)
def test_the_loader_refuses_json_text_the_promotion_never_writes(
    tmp_path: Path, old: str, new: str, message: str
) -> None:
    """Objective: the loader refuses JSON text Python's parser reads, but not as the promotion
    writes it: a key written twice in one object (Python's parser keeps the last, another
    reader may keep the first), a number beyond a float (Python's parser reads it as infinity),
    a lone surrogate escape (Python's parser keeps it, pydantic's refuses it with no location),
    and an integer past Python's limit on digits; each refusal reads as one clean clause.

    Sample: the complete bare curve as the promotion renders it, with ``schema_version`` written
    twice (another schema first), its first capacity written ``1e999``, its stated limit led by
    ``\\ud800``, or its first requested fleet written with 5,000 digits.

    Expected outcome: SaturationCurveError naming the file and the repeated key, the value not a
    finite number, pydantic's parser refusing the text (no empty location before it), or a
    number out of range.
    """
    text = render_artifact_json(complete_bare_curve()) + ARTIFACT_FILE_END
    assert old in text
    path = tmp_path / "altered.json"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    with pytest.raises(SaturationCurveError, match=message) as refused:
        load_saturation_curve(path)
    assert str(path) in str(refused.value)
    assert "(: " not in str(refused.value)


@pytest.mark.parametrize("digit_limit", [sys.get_int_max_str_digits(), 0], ids=["Python's", "none"])
def test_a_number_out_of_range_is_the_curves_error_whatever_pythons_digit_limit(
    tmp_path: Path, digit_limit: int
) -> None:
    """Objective: one rule sorts the loader's refusals, so a number out of range is the curve's
    error whether or not Python's parser reads it (its class never follows
    ``sys.set_int_max_str_digits``).

    Sample: the complete bare curve with its first requested fleet written with 5,000 digits,
    loaded under Python's default limit on an integer's digits (Python's parser refuses it) and
    with no limit (Python's parser reads it, and pydantic's refuses it).

    Expected outcome: SaturationCurveError naming the file, a number out of range, both times.
    """
    text = (render_artifact_json(complete_bare_curve()) + ARTIFACT_FILE_END).replace(
        '"requested_fleet": 342,', f'"requested_fleet": 1{"0" * 4_999},', 1
    )
    path = tmp_path / "long_integer.json"
    path.write_text(text, encoding="utf-8")
    default = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(digit_limit)
    try:
        with pytest.raises(SaturationCurveError, match="number out of range") as refused:
            load_saturation_curve(path)
    finally:
        sys.set_int_max_str_digits(default)
    assert str(path) in str(refused.value)


@pytest.mark.parametrize(
    ("text", "kind"),
    [
        ("[1, 2]", "an array"),
        ("null", "null"),
        ("true", "true"),
        ("false", "false"),
        ("3", "a number"),
        ("2.5", "a number"),
        ('"a curve"', "a string"),
    ],
    ids=["an array", "null", "true", "false", "an integer", "a decimal", "a string"],
)
def test_a_json_root_that_is_not_an_object_is_not_a_saturation_curve(
    tmp_path: Path, text: str, kind: str
) -> None:
    """Objective: text Python's parser reads is the curve's to refuse, so a JSON root that is not
    an object is the curve's error, not the file boundary's, and the refusal names the root in
    JSON's own words.

    Sample: a file holding each kind of JSON value that is not an object.

    Expected outcome: SaturationCurveError naming the file and the root's kind (null, true,
    false, a number, a string, an array), never a Python type's name.
    """
    path = tmp_path / "saturation_curve.json"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(
        SaturationCurveError, match=f"its JSON root is {kind}, not an object"
    ) as refused:
        load_saturation_curve(path)
    assert str(path) in str(refused.value)


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ('"requested_fleet": 342,', '"requested_fleet": "342",'),
        ('"device_class": "small_terminal_class"', '"device_class": "mounted_terminal_class"'),
        ('"a stated limit"', '"\\ud800a stated limit"'),
    ],
    ids=["a located error", "a refusal of the whole curve", "text pydantic's parser refuses"],
)
def test_the_loaders_one_line_reading_of_a_validation_error_is_the_shared_commands(
    old: str, new: str
) -> None:
    """Objective: the loader's one-line reading of a pydantic error (``_validation_summary``, a
    copy the rule keeping ``common/`` unchanged forces) stays the one the shared commands print
    (``common.cli.describe_failure``), so the two cannot drift apart unseen.

    Sample: the complete bare curve as the promotion renders it, with a requested fleet written
    as text (a located error), a class written twice (the curve's own validator refusing the
    whole curve, no location), or its stated limit led by a lone surrogate escape (pydantic's
    parser refusing the text, no location), each validated as the loader validates.

    Expected outcome: ``describe_failure`` of the error is ``invalid <title>:`` followed by the
    loader's reading, whitespace collapsed as ``describe_failure`` collapses it.
    """
    text = render_artifact_json(complete_bare_curve()) + ARTIFACT_FILE_END
    assert old in text
    with pytest.raises(ValidationError) as refused:
        SaturationCurve.model_validate_json(text.replace(old, new, 1), strict=True)
    error = refused.value
    summary = saturation_curve._validation_summary(error)
    assert describe_failure(error) == " ".join(f"invalid {error.title}: {summary}".split())


def test_a_code_defect_in_validation_is_never_reported_as_a_data_problem(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Objective: the loader turns only a requested fleet too large for a float (``walker_shape``'s
    OverflowError) into the curve's error; any other arithmetic failure in validation, a code
    defect, leaves as itself.

    Sample: the complete bare curve, loaded with ``walker_shape`` patched to divide by zero.

    Expected outcome: ZeroDivisionError, not SaturationCurveError.
    """
    path = tmp_path / "saturation_curve.json"
    path.write_text(
        render_artifact_json(complete_bare_curve()) + ARTIFACT_FILE_END, encoding="utf-8"
    )

    def divides_by_zero(requested_fleet: int) -> tuple[int, int]:
        return requested_fleet // 0, 1

    monkeypatch.setattr(saturation_curve, "walker_shape", divides_by_zero)
    with pytest.raises(ZeroDivisionError):
        load_saturation_curve(path)


def test_fleets_too_large_for_their_midpoint_are_the_curves_error_naming_the_file(
    tmp_path: Path,
) -> None:
    """Objective: the loader's one rule holds for every number out of range: two neighbouring
    rows' fleets whose product (the geometric midpoint's) a float cannot hold are the curve's error
    naming the file, never a raw OverflowError, though the contract admits each fleet (each one's
    shell builds).

    Sample: the complete bare curve's JSON with the sweep's requests moved to 10^160 and 4 x
    10^160, every row's request and realized fleet moved with them, each row's ocean factor L / (N
    x B) at its new fleet (B 150, or 48 for the 48-beam point), the input hash recomputed.

    Expected outcome: SaturationCurveError naming the file and a number out of range, the two
    neighbouring fleets' product.
    """
    requests = (10**160, 4 * 10**160)
    realized = [math.prod(walker_shape(request)) for request in requests]
    data = json.loads(render_artifact_json(complete_bare_curve()))
    data["parameters"]["sweep"]["fleets"] = list(requests)
    data["input_hash"] = curve_input_hash(SaturationInputs.model_validate(data["parameters"]))
    for entry in (*data["classes"], *data["bands"]):
        beams = 48.0 if entry.get("point", {}).get("beams_per_satellite") == 48 else 150.0
        for row, request, fleet in zip(entry["rows"], requests, realized, strict=True):
            row.update(
                requested_fleet=request,
                fleet=fleet,
                ocean_factor=row["useful_beams"] / (fleet * beams),
            )
    path = write_curve_json(tmp_path / "huge_fleets.json", data)
    with pytest.raises(
        SaturationCurveError, match="a number out of range: two neighbouring rows' fleets"
    ) as refused:
        load_saturation_curve(path)
    assert str(refused.value).startswith(f"{path}: not a saturation curve")


@pytest.mark.parametrize(
    ("content", "message"),
    [
        (None, "file not found"),
        ("{not json", "not a JSON document"),
        ("[" * 200_000 + "]" * 200_000, "nested too deeply"),
    ],
    ids=["missing", "not JSON", "nested past Python's parser"],
)
def test_the_loader_refuses_a_file_it_cannot_read_as_a_curve(
    tmp_path: Path, content: str | None, message: str
) -> None:
    """Objective: a curve file that cannot be read, or that Python's JSON parser refuses as JSON,
    is the shared file-boundary error.

    Sample: no file; text that is not JSON; an array nested 200,000 deep (Python's parser runs
    out of stack and raises RecursionError).

    Expected outcome: ModelFileError naming the file and the reason.
    """
    path = tmp_path / "saturation_curve.json"
    if content is not None:
        path.write_text(content, encoding="utf-8")
    with pytest.raises(ModelFileError, match=message) as refused:
        load_saturation_curve(path)
    assert refused.value.path == path


@pytest.mark.parametrize(
    ("fleets", "extension", "named"),
    [
        ((992, 993), (), r"\[992, 993\] realize as \[992, 992\]"),
        ((1_000, 3_969), (3_970,), r"\[1000, 3969, 3970\] realize as \[992, 3969, 3969\]"),
    ],
    ids=["two of the sweep's fleets", "the mounted extension's first and the sweep's last"],
)
def test_compute_saturation_refuses_requests_that_realize_one_row(
    uniform_band: PopulationGrid,
    synthetic_saturation_inputs: SaturationInputsBuilder,
    fleets: tuple[int, ...],
    extension: tuple[int, ...],
    named: str,
) -> None:
    """Objective: requests that strictly increase but realize the same P x S are refused
    before any computation, since each row is keyed by its realized fleet; one check covers the
    sweep's fleets and the mounted terminal's extension after them.

    Sample: the uniform band's inputs at the requests 992 and 993, both 31 x 32 = 992; then at
    1,000 and 3,969 with the mounted extension 3,970, which realizes as 63 x 63 = 3,969, the
    sweep's last row.

    Expected outcome: SaturationInvariantError naming the requests and the realized fleets, which
    do not strictly increase.
    """
    inputs = synthetic_saturation_inputs(uniform_band, fleets=fleets)
    sweep = inputs.sweep.model_copy(update={"mounted_terminal_extension": extension})
    with pytest.raises(SaturationInvariantError, match=named):
        compute_saturation(
            inputs.model_copy(update={"sweep": sweep}), uniform_band, version_stamp=STAMP
        )


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"lat_top_deg": 89.75}, "global grid from 90 degrees north"),
        ({"rows": 80}, r"global grid from 90 degrees north; got 80 x 180 cells of 2.0 degrees"),
        ({"columns": 170}, r"global grid from 90 degrees north; got 90 x 170 cells of 2.0 degrees"),
        ({"dimensions": 3}, "must be two-dimensional; got 3 dimensions"),
    ],
    ids=[
        "its north edge off the pole",
        "rows short of 180 degrees",
        "columns short of 360 degrees",
        "not two-dimensional",
    ],
)
def test_compute_saturation_refuses_a_grid_that_is_not_global(
    uniform_band: PopulationGrid,
    synthetic_saturation_inputs: SaturationInputsBuilder,
    change: dict[str, float],
    message: str,
) -> None:
    """Objective: the pair search wraps longitudes and clips at the poles, so the curve is
    computed only on a two-dimensional global grid from 90 degrees north: each of the guard's
    four conditions refuses on its own.

    Sample: the uniform band's grid (90 x 180 cells of 2 degrees) and digest, with one change
    each: its northern edge moved to 89.75 degrees; its first 80 rows only (160 degrees of
    latitude); its first 170 columns only (340 degrees of longitude); its array given a third
    dimension.

    Expected outcome: PopulationGridError asking for a global grid from 90 degrees north (naming
    the cells found), or for a two-dimensional grid.
    """
    population = uniform_band.population
    changed = dataclasses.replace(
        uniform_band,
        lat_top_deg=change.get("lat_top_deg", uniform_band.lat_top_deg),
        population=(
            population[None]
            if "dimensions" in change
            else population[: int(change.get("rows", population.shape[0])), :][
                :, : int(change.get("columns", population.shape[1]))
            ]
        ),
    )
    inputs = synthetic_saturation_inputs(uniform_band, fleets=BAND_FLEETS)
    with pytest.raises(PopulationGridError, match=message):
        compute_saturation(inputs, changed, version_stamp=STAMP)


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
column, the pair search's worst case for memory."""

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
    """Objective: the pair search's chunks bound its working memory where it is largest, a wide
    view near a pole: every chunk's windows hold at most the element budget, and chunking
    changes no pair.

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


# ---------------------------------------------------------------------------
# The directional classes through the _allocate seam (rules D2 to D6)
# ---------------------------------------------------------------------------

SE_ANCHOR = 0.65
"""The link mapping's anchor, SE = 0.65 x log2(1 + SINR) (the curve's default)."""

PATTERN_FLOOR_DB = -20.0
"""The terminal pattern's floor, dB (the curve's default)."""


def terminal_beamwidth_rad(device_class: DeviceClass) -> float:
    """The terminal's half-power beamwidth, sqrt(4 pi / (1.133 x D)), from its directivity."""
    directivity = 10 ** (class_inputs(device_class).directivity_dbi / 10)
    return math.sqrt(4 * math.pi / (1.133 * directivity))


def single_layer_sinr(device_class: DeviceClass) -> float:
    """SINR_1 = 2^(SE_central / 0.65) - 1, the class's single-layer operating point."""
    return 2 ** (class_inputs(device_class).spectral_efficiency_bps_per_hz / SE_ANCHOR) - 1


def angle_between_deg(first: tuple[float, float], second: tuple[float, float]) -> float:
    """The angle between two directions (elevation, azimuth), degrees, by spherical trigonometry."""
    e1, a1, e2, a2 = (math.radians(value) for value in (*first, *second))
    cosine = math.sin(e1) * math.sin(e2) + math.cos(e1) * math.cos(e2) * math.cos(a1 - a2)
    return math.degrees(math.acos(min(1.0, cosine)))


def directional_limits(
    device_class: DeviceClass,
    beams_per_satellite: float,
    serving_rule: sat._ServingRule = sat._ServingRule.AT_SERVING_SHARE,
) -> sat._AllocationLimits:
    """A directional class's allocation limits at the defaults, with a chosen B and serving rule."""
    inputs = SaturationInputs()
    entry = class_inputs(device_class)
    rules = sat._directional_rules(inputs, entry)
    assert rules is not None
    return sat._AllocationLimits(
        beams_per_satellite=beams_per_satellite,
        people_per_beam=sat._people_per_beam(inputs.spectrum_mhz, entry),
        take_up=inputs.demand.take_up,
        beam=sat._beam_model(inputs.shell),
        footprint_bands=inputs.sweep.footprint_bands,
        passes=inputs.sweep.passes,
        spectrum_mhz=inputs.spectrum_mhz,
        spectral_efficiency_bps_per_hz=entry.spectral_efficiency_bps_per_hz,
        directional=dataclasses.replace(rules, serving_rule=serving_rule),
    )


OneCell = tuple[sat._DemandCells, tuple[float, float]]
"""One populated 0.25 degree cell's demand cells and its centre (latitude, longitude), degrees."""


@pytest.fixture(scope="module")
def one_cell(synthetic_population_grid: GridBuilder) -> OneCell:
    """One densely populated 0.25 degree cell at (0.125, 0.125), about 773 km^2 (no people cap
    binds), and its centre."""
    cells = sat._demand_cells(synthetic_population_grid(0.25, patch_people(0.25, 0)), 1.0)
    return cells, (float(np.degrees(cells.lat_rad[0])), float(np.degrees(cells.lon_rad[0])))


def allocate_seen_at(
    one_cell: OneCell,
    directions_deg: Sequence[tuple[float, float]],
    limits: sat._AllocationLimits,
) -> sat._Allocation:
    """Allocate the one cell among satellites placed where its centre sees them at the given
    (elevation, azimuth) directions, degrees, in that order (pair i is satellite i)."""
    cells, centre = one_cell
    shell = SaturationInputs().shell
    points = [satellite_seen_at(centre, el, az, shell) for el, az in directions_deg]
    satellites = satellites_at(points)
    allocation = sat._allocate(satellites, cells, limits)
    assert allocation.satellite.tolist() == list(range(len(directions_deg)))
    return allocation


def directional_of(allocation: sat._Allocation) -> sat._DirectionalAllocation:
    """The allocation's directional part (a directional class's)."""
    assert allocation.directional is not None
    return allocation.directional


SERVING_CASE_DEG = ((90.0, 0.0), (35.0, 170.0), (32.0, 270.0), (27.0, 195.0))
"""The serving-set case: the zenith satellite, the stage-1 sliver, and two stage-2 candidates
in the other ring half of the small terminal's sky."""


def test_the_serving_set_holds_the_satellites_whose_layer_reaches_f_serve(
    one_cell: OneCell,
) -> None:
    """Objective: rule D3: a satellite serves a cell when its committed layer covers at least
    f_serve = 1 / SINR_1 (0.134 for the small terminal) of the cell's area; a thinner sliver
    does not serve, and so never blocks a stacked candidate.

    Sample: the small terminal, one cell, B = 4: a satellite at the zenith (its 4 beams cover
    88.4 percent of the cell), one at (35, 170) degrees that takes the remaining 11.6 percent in
    stage 1, and two stage-2 candidates in the other half of the ring: (32, 270), 58 degrees
    from the zenith, and (27, 195), 63 degrees from the zenith but 22.8 from the sliver.

    Expected outcome: every pair serves exactly when its first-layer and stacked beams cover at
    least f_serve of the cell: the zenith satellite and the admitted candidate serve, the
    sliver (share between 0 and f_serve) does not; the sliver's own stacking is refused (55
    degrees from the zenith satellite, under a beamwidth) and so is the candidate at (32, 270);
    the candidate at (27, 195) stacks, since the sliver is no serving satellite. With every
    first-layer satellite serving (the diagnostic's any-share rule), the sliver blocks it. With
    only the cell's main first-layer satellite serving (the diagnostic's main-satellite rule),
    the serving set is exactly the zenith pair at the end of stage 2, so it was after stage 1
    too (a set that only grows) and no stacked pair joined it: the candidate at (27, 195)
    stacks but does not serve.
    """
    allocation = allocate_seen_at(one_cell, SERVING_CASE_DEG, directional_limits(SMALL, 4.0))
    layers = directional_of(allocation)
    cells, _ = one_cell
    f_serve = 1 / single_layer_sinr(SMALL)
    assert f_serve == pytest.approx(0.1344, abs=1e-4)
    share = (layers.first_layer_beams + layers.stacked_beams) * allocation.footprint_km2
    share = share / cells.area_km2[0]
    assert layers.serving.tolist() == (share >= f_serve).tolist() == [True, False, False, True]
    sliver = layers.first_layer_beams[1] * allocation.footprint_km2[1] / cells.area_km2[0]
    assert 0 < sliver < f_serve
    assert layers.first_layer_beams[0] == pytest.approx(4.0, rel=1e-12)
    beamwidth_deg = math.degrees(terminal_beamwidth_rad(SMALL))
    zenith, sliver_at, near, far = SERVING_CASE_DEG
    assert angle_between_deg(sliver_at, zenith) < beamwidth_deg
    assert angle_between_deg(near, zenith) < beamwidth_deg
    assert angle_between_deg(far, zenith) > beamwidth_deg > angle_between_deg(far, sliver_at)
    assert layers.sector[1] != layers.sector[3]
    assert layers.stacked_beams[1] == layers.stacked_beams[2] == 0.0
    assert layers.stacked_beams[3] > 0
    any_share = allocate_seen_at(
        one_cell, SERVING_CASE_DEG, directional_limits(SMALL, 4.0, sat._ServingRule.ANY_SHARE)
    )
    assert directional_of(any_share).stacked_beams[3] == 0.0
    main_only = directional_of(
        allocate_seen_at(
            one_cell,
            SERVING_CASE_DEG,
            directional_limits(SMALL, 4.0, sat._ServingRule.MAIN_SATELLITE),
        )
    )
    assert main_only.stacked_beams[3] > 0
    assert main_only.serving.tolist() == [True, False, False, False]


PAIRWISE_CASE_DEG = ((90.0, 0.0), (28.0, 190.0), (28.05, 170.0), (40.0, 270.0))
"""The pairwise case: the zenith satellite, two candidates of one band either side of the ring
halves' boundary, and a candidate within a beamwidth of the zenith. The two candidates'
footprints differ by 0.5 percent, inside one band at 40, 160 or 320 footprint bands (at 160 a
band spans 1.7 percent here; the smaller-footprint candidate sat at 28.3 degrees, 3.1 percent
apart, while the fill had 40 bands). The larger footprint (28.0 degrees) is on the lower
satellite index, so the candidates' order by footprint and by satellite index differ."""


def test_a_stacked_candidate_needs_a_beamwidth_from_the_serving_set_and_the_bands_admitted(
    one_cell: OneCell,
) -> None:
    """Objective: rule D4's pairwise admission: a candidate is admitted only at least one
    terminal beamwidth (60.3 degrees for the small terminal) from every satellite serving its
    cell in another sector and from every candidate of its cell admitted earlier in the band
    in another sector; a band's candidates are taken by (cell, footprint, satellite index), so
    the smaller footprint is taken first whatever its satellite's index.

    Sample: the small terminal, one cell, B = 150: a zenith satellite that covers the cell
    alone in stage 1; candidates at (28.0, 190) degrees (satellite 1) and (28.05, 170) (satellite
    2, the smaller footprint), in one footprint band and in the two halves of the ring, 17.6
    degrees apart, each over 60.3 from the zenith; one at (40, 270), 50 degrees from the zenith.
    Then the same without the (28.05, 170) satellite.

    Expected outcome: the two band-mates share a band, the smaller footprint on the higher index;
    it is taken first and stacks; its band-mate, the lower index, closer to it than a beamwidth in
    the other sector, is refused (an order by satellite index alone would stack it instead); the
    candidate at (40, 270) is refused by the serving zenith satellite. Without the smaller
    footprint, its band-mate stacks, so it was the earlier admitted candidate that refused it.
    """
    allocation = allocate_seen_at(one_cell, PAIRWISE_CASE_DEG, directional_limits(SMALL, 150.0))
    layers = directional_of(allocation)
    bands = sat._footprint_bands(allocation.footprint_km2, SaturationInputs().sweep.footprint_bands)
    band_of = np.empty(allocation.satellite.size, dtype=np.int64)
    for band in range(bands.count):
        band_of[bands.members(band)] = band
    assert band_of[1] == band_of[2]
    assert allocation.footprint_km2[2] < allocation.footprint_km2[1]
    assert layers.sector[1] != layers.sector[2]
    beamwidth_deg = math.degrees(terminal_beamwidth_rad(SMALL))
    zenith, larger, smaller, steep = PAIRWISE_CASE_DEG
    assert angle_between_deg(larger, smaller) < beamwidth_deg
    from_zenith = (angle_between_deg(larger, zenith), angle_between_deg(smaller, zenith))
    assert min(from_zenith) > beamwidth_deg
    assert angle_between_deg(steep, zenith) < beamwidth_deg
    assert layers.serving[0]
    assert layers.stacked_beams[2] > 0
    assert layers.stacked_beams[1] == layers.stacked_beams[3] == 0.0
    without_smaller = allocate_seen_at(
        one_cell, (zenith, larger, steep), directional_limits(SMALL, 150.0)
    )
    assert directional_of(without_smaller).stacked_beams[1] > 0


KEY_AREA_CASE_DEG = ((90.0, 0.0), (35.0, 90.0), (28.0, 150.0))
"""The key-area case (the small terminal, B = 2): the zenith satellite, whose 2 beams cover
part of the cell (its sky's cap sector); a satellite at (35, 90) in the first half of the ring
(55 degrees from the zenith, under a beamwidth), which completes the cell's first layer; and a
satellite at (28, 150) in the same half (62 degrees from the zenith, over a beamwidth; its
sector-mate is exempt), whose larger footprint comes too late for the first layer."""


def test_a_stacked_layer_fills_at_most_what_its_sectors_first_layer_left_of_the_cell(
    one_cell: OneCell,
) -> None:
    """Objective: rule D4's key area: a stacked candidate's key is its cell's sky sector, whose
    area is the cell's less the first layer from that sector, so a sector's first and stacked
    layers together never cover more than the cell.

    Sample: the small terminal, one cell (about 773 km^2), B = 2: the zenith satellite covers
    2 x 170.8 km^2 of it in stage 1 (the cap sector); the (35, 90) satellite, next by footprint,
    completes the first layer from the ring's first half (sector 1); the (28, 150) satellite, in
    the same sector, gets no first layer (rounding dust under the module's served floor). In
    stage 2 the (35, 90) satellite is refused (55 degrees from the serving zenith satellite) and
    the (28, 150) one, 62 degrees from it and exempt from its sector-mate, stacks.

    Expected outcome: the first layer covers the cell; the (28, 150) satellite stacks, and sector
    1's first and stacked layers cover the cell's area exactly (within 1e-9): its key area, the
    cell less sector 1's first layer, binds; a key of the whole cell would let it cover more.
    """
    allocation = allocate_seen_at(one_cell, KEY_AREA_CASE_DEG, directional_limits(SMALL, 2.0))
    layers = directional_of(allocation)
    cells, _ = one_cell
    area = float(cells.area_km2[0])
    footprint = allocation.footprint_km2
    assert layers.sector[1] == layers.sector[2] != layers.sector[0]
    assert layers.first_layer_beams[0] == pytest.approx(2.0, rel=1e-12)
    assert layers.first_layer_beams[2] < SERVED_BEAMS_FLOOR
    first_area = float((layers.first_layer_beams * footprint).sum())
    assert first_area == pytest.approx(area, rel=1e-9)
    assert layers.stacked_beams[1] == 0.0
    assert layers.stacked_beams[2] > 0
    in_sector = layers.sector == layers.sector[1]
    layer_area = (layers.first_layer_beams + layers.stacked_beams) * footprint
    sector_area = float(layer_area[in_sector].sum())
    assert sector_area <= area * (1 + 1e-9)
    assert sector_area == pytest.approx(area, rel=1e-9)


def test_satellites_in_the_same_sector_are_exempt_from_each_other(one_cell: OneCell) -> None:
    """Objective: satellites in one sky sector tile that sector's one layer, so the pairwise
    rule never sets them against each other (rule D4).

    Sample: the small terminal, one cell, B = 150: a zenith satellite covering the cell, and two
    candidates of one band in the same half of the ring, at (28.05, 60) and (28.0, 80) degrees,
    17.6 degrees apart (under a beamwidth), each over a beamwidth from the zenith; their
    footprints differ by 0.5 percent, inside one band at 40, 160 or 320 footprint bands.

    Expected outcome: both stack, sharing their sector's area: their stacked shares of the cell
    sum to one layer, each positive.
    """
    directions = ((90.0, 0.0), (28.05, 60.0), (28.0, 80.0))
    allocation = allocate_seen_at(one_cell, directions, directional_limits(SMALL, 150.0))
    layers = directional_of(allocation)
    cells, _ = one_cell
    assert layers.sector[1] == layers.sector[2]
    assert angle_between_deg(directions[1], directions[2]) < math.degrees(
        terminal_beamwidth_rad(SMALL)
    )
    stacked_share = layers.stacked_beams * allocation.footprint_km2 / cells.area_km2[0]
    assert stacked_share[1] > 0 and stacked_share[2] > 0
    assert stacked_share[1] + stacked_share[2] == pytest.approx(1.0, rel=1e-9)


FULL_SUM_CASE_DEG = ((90.0, 0.0), (62.0, 120.0), (45.0, 300.0), (45.0, 330.0), (40.0, 200.0))
"""The full-sum case (the mounted terminal): a first layer split between the zenith and the
ring of 3; two stacked layers sharing one sector of the ring of 5; one in another sector."""


def full_sum_capacity_mbps(
    allocation: sat._Allocation,
    cell_area_km2: float,
    directions_deg: Sequence[tuple[float, float]],
    *,
    exclusions: bool,
) -> float:
    """The cell's capacity by rule D5's closed form, independently: for each served sub-pair q,
    SINR_q = 1 / (1 / SINR_1 + the sum over the other sub-pairs p of f_p x g(theta_pq)), g a
    Gaussian main lobe floored at -20 dB, the angles from the intended directions; with
    ``exclusions``, two first-layer sub-pairs and two sub-pairs of one sector are left out."""
    layers = directional_of(allocation)
    beamwidth = terminal_beamwidth_rad(MOUNTED)
    sinr_1 = single_layer_sinr(MOUNTED)
    sub_pairs = [
        (pair, is_first, beams)
        for pair in range(allocation.satellite.size)
        for is_first, beams in (
            (True, float(layers.first_layer_beams[pair])),
            (False, float(layers.stacked_beams[pair])),
        )
        if beams > 0
    ]
    capacity = 0.0
    for pair, is_first, beams in sub_pairs:
        interference = 0.0
        for other, other_first, other_beams in sub_pairs:
            if (other, other_first) == (pair, is_first):
                continue
            same_sector = layers.sector[other] == layers.sector[pair]
            if exclusions and (same_sector or (is_first and other_first)):
                continue
            theta = math.radians(angle_between_deg(directions_deg[pair], directions_deg[other]))
            gain_db = max(-12.0 * (theta / beamwidth) ** 2, PATTERN_FLOOR_DB)
            share = other_beams * float(allocation.footprint_km2[other]) / cell_area_km2
            interference += share * 10 ** (gain_db / 10)
        sinr = 1 / (1 / sinr_1 + interference)
        capacity += beams * SE_ANCHOR * math.log2(1 + sinr)
    return capacity * SaturationInputs().spectrum_mhz


def test_a_cells_capacity_is_the_full_sum_closed_form_at_the_realized_gains(
    one_cell: OneCell,
) -> None:
    """Objective: rule D5: each served sub-pair is priced against the full sum of its cell's
    other layers at the victim terminal's gain toward each, first-layer sub-pairs not against
    each other and same-sector sub-pairs not against each other.

    Sample: the mounted terminal (33.9 degree beamwidth), one cell, B = 2: satellites where the
    cell centre sees them at (90, 0) and (62, 120) degrees (the first layer: the zenith's two
    beams and the rest from the ring of 3), (45, 300) and (45, 330) (one sector of the ring of
    5, sharing its stacked layer, 21 degrees apart) and (40, 200) (another sector).

    Expected outcome: two first-layer sub-pairs in two sectors and three stacked ones, two in
    one sector; the module's capacity with the stack equals the closed form at the realized
    layers and the angles of the intended directions within 1e-7 relative; counting the
    excluded pairs too would give a capacity more than 1 percent lower; the stack is kept, and
    the stacked layers' median separation from their nearest layer of another sector is 45
    degrees (the zenith satellite's).
    """
    allocation = allocate_seen_at(one_cell, FULL_SUM_CASE_DEG, directional_limits(MOUNTED, 2.0))
    layers = directional_of(allocation)
    cells, _ = one_cell
    assert layers.first_layer_beams[0] == pytest.approx(2.0, rel=1e-12)
    assert layers.first_layer_beams[1] > 0 and np.all(layers.first_layer_beams[2:] == 0)
    assert np.all(layers.stacked_beams[:2] == 0) and np.all(layers.stacked_beams[2:] > 0)
    assert layers.sector[2] == layers.sector[3] != layers.sector[4]
    assert len({int(layers.sector[0]), int(layers.sector[1]), int(layers.sector[4])}) == 3
    expected = full_sum_capacity_mbps(
        allocation, float(cells.area_km2[0]), FULL_SUM_CASE_DEG, exclusions=True
    )
    assert layers.stacked_capacity_mbps[0] == pytest.approx(expected, rel=1e-7)
    without_exclusions = full_sum_capacity_mbps(
        allocation, float(cells.area_km2[0]), FULL_SUM_CASE_DEG, exclusions=False
    )
    assert without_exclusions < 0.99 * expected
    assert layers.keeps_stack[0]
    assert layers.cell_capacity_mbps[0] == layers.stacked_capacity_mbps[0]
    assert allocation.capacity_mbps == pytest.approx(expected, rel=1e-7)
    assert layers.statistics.median_separation_deg == pytest.approx(45.0, abs=1e-6)


@pytest.mark.parametrize(
    ("device_class", "stacked_at", "kept"),
    [(SMALL, (29.0, 90.0), False), (MOUNTED, (40.0, 90.0), True)],
    ids=["the small terminal drops", "the mounted terminal keeps"],
)
def test_the_keep_rule_drops_a_stack_that_lowers_capacity_and_its_beams_stay_spent(
    one_cell: OneCell, device_class: DeviceClass, stacked_at: tuple[float, float], kept: bool
) -> None:
    """Objective: rule D6: a cell whose capacity with its stacked layers is below its first
    layer alone (every first-layer beam at the central SE) keeps its first layer only; the
    dropped stacked beams stay spent (never returned or re-spent) and L counts only kept beams.

    Sample: one cell covered at the zenith (B = 150) and one stacked satellite that covers it
    again: for the small terminal at (29, 90) degrees, 61 degrees from the zenith, just past its
    60.3 degree beamwidth (a gain of -12.3 dB between the layers); for the mounted terminal at
    (40, 90), 50 degrees off, past its 33.9 degree beamwidth (the -20 dB floor).

    Expected outcome: the small terminal's stack lowers the cell's capacity, so it is dropped:
    the cell carries exactly its first layer alone, L is the first layer's beams, and the
    stacked beams stay placed on their satellite. The mounted terminal's raises it, so it is
    kept: the cell carries the stacked capacity and L counts the stacked beams.
    """
    allocation = allocate_seen_at(
        one_cell, ((90.0, 0.0), stacked_at), directional_limits(device_class, 150.0)
    )
    layers = directional_of(allocation)
    first_alone = (
        float(layers.first_layer_beams.sum())
        * class_inputs(device_class).spectral_efficiency_bps_per_hz
        * SaturationInputs().spectrum_mhz
    )
    stacked = float(layers.stacked_beams[1])
    assert stacked > 0
    assert allocation.beams[1] == stacked
    assert bool(layers.keeps_stack[0]) is kept
    if kept:
        assert layers.stacked_capacity_mbps[0] > first_alone
        assert layers.cell_capacity_mbps[0] == layers.stacked_capacity_mbps[0]
        assert allocation.useful_beams == pytest.approx(
            float(layers.first_layer_beams.sum()) + stacked, rel=1e-12
        )
    else:
        assert layers.stacked_capacity_mbps[0] < first_alone
        assert layers.cell_capacity_mbps[0] == pytest.approx(first_alone, rel=1e-12)
        assert allocation.useful_beams == pytest.approx(
            float(layers.first_layer_beams.sum()), rel=1e-12
        )
        assert layers.statistics.beams == 0.0
    assert allocation.capacity_mbps == pytest.approx(float(layers.cell_capacity_mbps.sum()))


SATELLITE_LIMITED_BAND_DEG = (20.0, 40.0)
"""The satellite-limited world's band of 0.5 degree cells, degrees north."""

SATELLITE_LIMITED_PEOPLE = 30.0
"""People in each cell of the satellite-limited world: under one beam of every class at the
investor's usage (the mounted terminal's people cap is 0.75 beams)."""

SATELLITE_LIMITED_FLEET = 600
"""The satellite-limited world's requested fleet (realized 600): too few satellites for the
mounted terminal's people caps, so many cells stay under their caps after stage 1 (5,083 of its
28,800). At 160 footprint bands the first-layer fill leaves stage 2 beams to complete short cells
at this fleet; at 306 satellites (requested 300), this world's fleet while the fill had 40
bands, the finer bands leave it none."""

SIDEREAL_DAY_S = 86164.0905
"""One sidereal day, s, the span the snapshot times are drawn over (the curve's pinned value)."""

SERVED_BEAMS_FLOOR = 1e-9
"""A sub-pair places a layer when it places more than this many beams (the module's floor)."""

COVERED_SHORTFALL_SHARE = 1e-9
"""A cell's first layer covers it when it leaves at most this share of the cell uncovered (the
module's convention; in the satellite-limited world a covered cell misses by rounding only and
a short one by more than 1e-5 of its area)."""


def satellite_limited_people(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    """30 people in every cell between 20 and 40 degrees north."""
    inside = (lat > SATELLITE_LIMITED_BAND_DEG[0]) & (lat < SATELLITE_LIMITED_BAND_DEG[1])
    return np.where(inside, SATELLITE_LIMITED_PEOPLE, 0.0)


def counted_stacked_beams(
    allocation: sat._Allocation, cells: sat._DemandCells, sectors: int, *, covered_only: bool
) -> float:
    """The stacked beams the statistics count, computed independently: every stacked sub-pair
    over the floor of a cell that keeps its stack (and with ``covered_only``, that its first
    layer covers) whose cell holds a served sub-pair in another sector."""
    layers = directional_of(allocation)
    cell = allocation.cell
    stacked = layers.stacked_beams > SERVED_BEAMS_FLOOR
    served = stacked | (layers.first_layer_beams > SERVED_BEAMS_FLOOR)
    served_keys = np.unique(cell[served] * sectors + layers.sector[served])
    sectors_served = np.bincount(served_keys // sectors, minlength=cells.count)
    first_area = np.bincount(
        cell, weights=layers.first_layer_beams * allocation.footprint_km2, minlength=cells.count
    )
    covers = first_area >= cells.area_km2 * (1 - COVERED_SHORTFALL_SHARE)
    counted = stacked & layers.keeps_stack[cell] & (sectors_served[cell] >= 2)
    if covered_only:
        counted &= covers[cell]
    return float(layers.stacked_beams[counted].sum())


def test_the_statistics_count_stacks_only_in_cells_their_first_layer_covers(
    synthetic_population_grid: GridBuilder, synthetic_saturation_inputs: SaturationInputsBuilder
) -> None:
    """Objective: the kept stacked share and its two statistics count a stacked layer only in a
    cell its first layer covers. In a covered cell every stage-2 beam overlaps another sector's
    first layer; in a cell its first layer leaves short, stage 2 may complete that first layer
    instead, which the fluid allocation cannot tell from stacking, so those beams count in L,
    never as stacked layers.

    Sample: 0.5 degree cells between 20 and 40 degrees north, 30 people each, so the mounted
    terminal's people caps (0.75 beams) outrun 600 satellites (requested 600) at the snapshot
    draw's first time; the default B, the investor's usage and the default footprint bands.

    Expected outcome: cells the first layer leaves short keep stage-2 beams beside a served
    layer of another sector, more than ten times the stacked beams of the covered cells (these
    completions are what the statistics would count without the rule); the statistics' beams
    equal, within 1e-12 relative, an independent count of the kept stacked sub-pairs over the
    floor of the covered cells that sit beside a served sub-pair of another sector.
    """
    grid = synthetic_population_grid(MID_BAND_CELL_DEG, satellite_limited_people)
    inputs = synthetic_saturation_inputs(grid, fleets=SHARED_USAGE_FLEETS)
    cells = sat._demand_cells(grid, inputs.demand.density_threshold_per_km2)
    first_time = float(np.random.default_rng(inputs.sweep.seed).uniform(0.0, SIDEREAL_DAY_S))
    satellites = sat._walker_positions(inputs.shell, SATELLITE_LIMITED_FLEET, first_time)
    assert satellites.count == 600
    allocation = sat._allocate(satellites, cells, directional_limits(MOUNTED, 150.0))
    sectors = sum(class_inputs(MOUNTED).sector_wedges_per_ring)
    covered = counted_stacked_beams(allocation, cells, sectors, covered_only=True)
    every_cell = counted_stacked_beams(allocation, cells, sectors, covered_only=False)
    assert every_cell > 10 * covered
    assert directional_of(allocation).statistics.beams == pytest.approx(covered, rel=1e-12, abs=0.0)


def test_the_sector_rule_ceiling_sums_each_sectors_smallest_footprint(one_cell: OneCell) -> None:
    """Objective: the sector-rule ceiling (stage 9): per cell in view, the sum over its sky
    sectors of the cell's area over the sector's smallest footprint in view, capped by its
    people; it bounds a directional class's L where a one-layer ceiling would not.

    Sample: the full-sum case (the mounted terminal, B = 2): satellites in four sectors, two of
    them sharing one (at equal footprints).

    Expected outcome: the ceiling equals the cell's area over each sector's smallest footprint,
    summed over the four sectors (1e-12 relative); L is at most the ceiling and more than one
    layer at the smallest footprint in view (the phone class's ceiling for this cell).
    """
    allocation = allocate_seen_at(one_cell, FULL_SUM_CASE_DEG, directional_limits(MOUNTED, 2.0))
    layers = directional_of(allocation)
    cells, _ = one_cell
    area = float(cells.area_km2[0])
    smallest: dict[int, float] = {}
    for sector, footprint in zip(
        layers.sector.tolist(), allocation.footprint_km2.tolist(), strict=True
    ):
        smallest[sector] = min(smallest.get(sector, math.inf), footprint)
    assert len(smallest) == 4
    expected = sum(area / footprint for footprint in smallest.values())
    assert allocation.ceiling_beams == pytest.approx(expected, rel=1e-12)
    assert area / float(allocation.footprint_km2.min()) < allocation.useful_beams
    assert allocation.useful_beams <= allocation.ceiling_beams


@pytest.mark.parametrize("device_class", [SMALL, MOUNTED])
def test_a_directional_first_layer_is_the_phone_allocation_at_its_own_people_cap(
    synthetic_population_grid: GridBuilder, device_class: DeviceClass
) -> None:
    """Objective: rule D2: a directional class's first layer is the phone allocation run with
    the class's own people cap.

    Sample: a 3 x 3 patch of 0.25 degree cells, 1,000 people each, under the five
    crowded-patch satellites, B = 150. About 4.5 beams tile a cell; at the investor's usage the
    small terminal's people cap is 3.1 beams and the phone class's 3.6 (both bind), the mounted
    terminal's 25 (it does not).

    Expected outcome: the class's first-layer beams equal, pair by pair, the beams the phone
    allocation places at the class's people per beam (exactly: the same fill), and differ from
    the phone class's own allocation at its people per beam (832 / 3).
    """
    grid = synthetic_population_grid(0.25, patch_people_of(1_000.0))
    cells = sat._demand_cells(grid, 1.0)
    points = [
        (PATCH_CENTRE_DEG[0] + d_lat, PATCH_CENTRE_DEG[1] + d_lon)
        for d_lat, d_lon in CROWD_OFFSETS_DEG
    ]
    limits = directional_limits(device_class, 150.0)
    directional = directional_of(sat._allocate(satellites_at(points), cells, limits))
    at_class_cap = sat._allocate(
        satellites_at(points), cells, dataclasses.replace(limits, directional=None)
    )
    assert np.array_equal(directional.first_layer_beams, at_class_cap.beams)
    assert at_class_cap.beams.sum() > 0
    phone_own = sat._allocate(satellites_at(points), cells, seam_limits(150.0))
    assert not np.allclose(directional.first_layer_beams, phone_own.beams)


def patch_people_of(people_per_cell: float) -> PeopleAt:
    """A 3 x 3 patch of 0.25 degree cells around the patch centre, the given people each."""

    def people(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
        inside = (np.abs(lat - PATCH_CENTRE_DEG[0]) < 0.375) & (
            np.abs(lon - PATCH_CENTRE_DEG[1]) < 0.375
        )
        return np.where(inside, people_per_cell, 0.0)

    return people


def admitted_one_by_one(
    candidates: np.ndarray,
    pair_cell: np.ndarray,
    sector: np.ndarray,
    direction: np.ndarray,
    serving: np.ndarray,
    cos_beamwidth: float,
) -> np.ndarray:
    """Rule D4's admission taken candidate by candidate, as the rule reads (the reference for
    the module's vectorized form)."""
    admitted = np.zeros(candidates.size, dtype=bool)
    taken: dict[int, list[int]] = {}
    for position, candidate in enumerate(candidates.tolist()):
        cell = int(pair_cell[candidate])
        references = [int(p) for p in np.flatnonzero(serving & (pair_cell == cell))]
        references += taken.get(cell, [])
        clear = all(
            sector[other] == sector[candidate]
            or float(direction[other] @ direction[candidate]) <= cos_beamwidth
            for other in references
        )
        if clear:
            admitted[position] = True
            taken.setdefault(cell, []).append(candidate)
    return admitted


@pytest.mark.parametrize("seed", [1, 2, 3])
@pytest.mark.parametrize("device_class", [SMALL, MOUNTED])
def test_the_vectorized_admission_equals_the_rule_taken_candidate_by_candidate(
    seed: int, device_class: DeviceClass
) -> None:
    """Objective: the module's admission, vectorized rank by rank within cells, is rule D4's
    sequential admission exactly (the trickiest code of stage 2).

    Sample: random cells (five, with 40 satellites in view each, at random directions above the
    mask), the class's sectors, a random tenth of the pairs serving their cells and a random
    three fifths of them as one band's candidates in a random order within each cell.

    Expected outcome: the admitted candidates equal those of the rule taken candidate by
    candidate (the serving set's satellites and the earlier admitted candidates of the cell, in
    other sectors, each at least a beamwidth away), for every seed and both classes; some are
    refused and some admitted.
    """
    rng = np.random.default_rng(seed)
    n_cells, per_cell = 5, 40
    pair_cell = np.repeat(np.arange(n_cells), per_cell)
    elevation = np.radians(rng.uniform(MASK_DEG, 90.0, pair_cell.size))
    azimuth = rng.uniform(0.0, 2 * math.pi, pair_cell.size)
    direction = np.stack(
        [
            np.cos(elevation) * np.sin(azimuth),
            np.cos(elevation) * np.cos(azimuth),
            np.sin(elevation),
        ],
        axis=1,
    )
    layout = sat._sector_layout(class_inputs(device_class).sector_wedges_per_ring, MASK_DEG)
    sector = sat._sector_of(elevation, azimuth, layout)
    serving = rng.random(pair_cell.size) < 0.1
    chosen = np.flatnonzero(rng.random(pair_cell.size) < 0.6)
    candidates = chosen[np.lexsort((rng.random(chosen.size), pair_cell[chosen]))]
    directions = sat._PairDirections(
        satellite=np.arange(pair_cell.size),
        cell=pair_cell,
        satellite_km=direction,
        cell_km=np.zeros((n_cells, 3)),
    )
    cos_beamwidth = math.cos(terminal_beamwidth_rad(device_class))
    serving_lookup = sat._serving_index(np.flatnonzero(serving), pair_cell, n_cells)
    found = sat._admitted(candidates, pair_cell, sector, directions, serving_lookup, cos_beamwidth)
    expected = admitted_one_by_one(candidates, pair_cell, sector, direction, serving, cos_beamwidth)
    assert found.tolist() == expected.tolist()
    assert 0 < found.sum() < found.size


@pytest.mark.parametrize("bands", [160, 300], ids=["an unsigned byte key", "a two-byte key"])
def test_the_footprint_bands_order_is_the_stable_order_of_the_band_index(bands: int) -> None:
    """Objective: the footprint bands' sort on the smallest unsigned key that holds the band index
    (a radix sort) gives the stable order of the 64-bit band index exactly, so every fill takes
    its pairs in the same order.

    Sample: 200,000 random footprints from 170 to 3,300 km^2 (seed 7), at 160 bands (a byte key,
    the default) and 300 (a two-byte key).

    Expected outcome: the order equals numpy's stable argsort of the 64-bit band index, at the
    pinned edges ``geomspace(min x 0.999, max x 1.001, bands + 1)``, and so do the band starts.
    """
    footprint = np.random.default_rng(7).uniform(170.0, 3_300.0, 200_000)
    found = sat._footprint_bands(footprint, bands)
    edges = np.geomspace(footprint.min() * 0.999, footprint.max() * 1.001, bands + 1)
    band = np.clip(np.searchsorted(edges, footprint, side="right") - 1, 0, bands - 1)
    expected = np.argsort(band, kind="stable")
    assert np.array_equal(found.order, expected)
    assert np.array_equal(found.starts, np.searchsorted(band[expected], np.arange(bands + 1)))


def test_the_serving_index_merged_band_by_band_is_the_index_sorted_from_every_server() -> None:
    """Objective: the serving index kept sorted by cell, each band's joins merged in, is the index
    sorted afresh from every serving pair in the order they joined, so the admission reads the
    same servers at every band.

    Sample: 400 cells and 30,000 pairs with random cells (seed 3), a random tenth of the pairs
    serving at first, then five bands, each joining a random twentieth of the pairs not yet
    serving, in pair index order.

    Expected outcome: after every band the merged index's pairs, counts and starts equal those of
    ``_serving_index`` over the initial servers and every band's joins appended.
    """
    rng = np.random.default_rng(3)
    n_cells, n_pairs = 400, 30_000
    pair_cell = rng.integers(0, n_cells, n_pairs).astype(np.int64)
    serving = rng.random(n_pairs) < 0.1
    joined = np.flatnonzero(serving)
    index = sat._serving_index(joined, pair_cell, n_cells)
    for _ in range(5):
        joins = np.flatnonzero(~serving & (rng.random(n_pairs) < 0.05))
        serving[joins] = True
        index = sat._with_joins(index, joins, pair_cell)
        joined = np.concatenate([joined, joins])
        rebuilt = sat._serving_index(joined, pair_cell, n_cells)
        for field in ("pairs", "counts", "starts"):
            assert np.array_equal(getattr(index, field), getattr(rebuilt, field)), field


def shared_usage(inputs: SaturationInputs) -> SaturationInputs:
    """The inputs with every class at one shared usage, 1 Mbps x 2.5 percent, so the
    classes' people per beam differ only by their central SE (640, 800 and 208)."""
    classes = [
        {**entry.model_dump(), "active_rate_mbps": 1.0, "concurrency_peak": 0.025}
        for entry in inputs.classes
    ]
    return SaturationInputs.model_validate({**inputs.model_dump(), "classes": classes})


SHARED_USAGE_FLEETS = (1_000, 4_000)
"""The shared-usage world's requested fleets (realized 992 and 3,969)."""

CAPPED_BAND_PEOPLE = 1.25 * 208.0
"""People in each cell of the shared-usage world's equatorial band: 1.25 phone beams at 208
people per beam, so every class's people cap binds there."""


def shared_usage_people(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    """A dense band of 0.5 degree cells from 40 to 42 north (tiling binds) and a sparse band
    within 2 degrees of the equator (the people caps bind)."""
    dense = (lat > MID_BAND_DEG[0]) & (lat < MID_BAND_DEG[1])
    return np.where(
        dense, DENSE_PEOPLE_PER_CELL, np.where(np.abs(lat) < 2.0, CAPPED_BAND_PEOPLE, 0.0)
    )


@pytest.fixture(scope="module")
def shared_usage_curve(
    synthetic_population_grid: GridBuilder, synthetic_saturation_inputs: SaturationInputsBuilder
) -> SaturationCurve:
    """The shared-usage world's curve: every class at 1 Mbps x 2.5 percent, fleets 1,000 and
    4,000, one snapshot, no mounted extension."""
    grid = synthetic_population_grid(MID_BAND_CELL_DEG, shared_usage_people)
    inputs = shared_usage(
        small_sweep(synthetic_saturation_inputs(grid, fleets=SHARED_USAGE_FLEETS))
    )
    return compute_saturation(inputs, grid, version_stamp=STAMP)


def class_curve(curve: SaturationCurve, device_class: DeviceClass) -> ClassCurve:
    """One class's curve, found by its key."""
    (found,) = [entry for entry in curve.classes if entry.device_class is device_class]
    return found


def test_at_one_shared_usage_the_classes_order_in_aggregate(
    shared_usage_curve: SaturationCurve,
) -> None:
    """Objective: the class ordering in aggregate at one shared usage (the strategy's § 5,
    Phase 2): with every class at 1 Mbps x 2.5 percent the people served follow capacity, the
    small terminal's at least the phone class's and the mounted terminal's at least the small
    terminal's, at every fleet.

    Sample: a synthetic world of 0.5 degree cells: a dense band at 40 to 42 north, where tiling
    binds, and a sparse equatorial band, where every class's people cap binds (equal capacity
    there); fleets 1,000 and 4,000, one snapshot.

    Expected outcome: the curve lists the small terminal, the mounted terminal and the phone
    class; at both fleets capacity orders mounted terminal >= small terminal >= phone class
    (1e-9 relative), the directional classes strictly above the phone class.
    """
    assert [entry.device_class for entry in shared_usage_curve.classes] == list(DeviceClass)
    rows = {
        device_class: class_curve(shared_usage_curve, device_class).rows
        for device_class in DeviceClass
    }
    for small, mounted, phone in zip(rows[SMALL], rows[MOUNTED], rows[PHONE], strict=True):
        assert small.fleet == mounted.fleet == phone.fleet
        assert small.capacity_gbps >= phone.capacity_gbps * (1 - 1e-9)
        assert mounted.capacity_gbps >= small.capacity_gbps * (1 - 1e-9)
        assert small.capacity_gbps > phone.capacity_gbps


def test_the_sector_rule_ceiling_bounds_each_directional_row(
    shared_usage_curve: SaturationCurve,
) -> None:
    """Objective: the sector-rule ceiling bounds a directional class's L at every row, and
    maximum use bounds the ceiling; each directional row carries its stacking diagnostics, the
    phone class's none.

    Sample: the shared-usage world's curve (fleets 1,000 and 4,000, one snapshot).

    Expected outcome: for both directional classes, at every row, L <= min(ceiling, supply)
    and ceiling <= maximum use (1e-9 relative), and the diagnostics exist (their statistics
    present exactly when stacked beams are kept); the phone class's rows carry none.
    """
    for device_class in (SMALL, MOUNTED):
        curve = class_curve(shared_usage_curve, device_class)
        for row in curve.rows:
            assert row.useful_beams <= min(row.ceiling_beams, row.supply_beams) * (1 + 1e-9)
            assert row.ceiling_beams <= curve.markers.maximum_use_beams * (1 + 1e-9)
            assert row.directional is not None
            stacked = row.directional.kept_stacked_share > 0
            assert (row.directional.median_separation_deg is not None) == stacked
    for row in class_curve(shared_usage_curve, PHONE).rows:
        assert row.directional is None


EXTENSION_TEST_FLEETS = (500, 1_000)
"""The extension test's requested fleets (realized 506 and 992): two, the fewest the contract
takes, since a marker reads the elasticity between rows."""

EXTENSION_TEST_MOUNTED = (4_000,)
"""The extension test's mounted-terminal extension (realized 3,969)."""


def test_the_mounted_terminal_runs_over_its_extension_through_compute_saturation(
    synthetic_population_grid: GridBuilder, synthetic_saturation_inputs: SaturationInputsBuilder
) -> None:
    """Objective: compute_saturation runs the mounted terminal over the sweep's fleets and its
    extension, every other class over the fleets alone, each row keyed by its realized fleet
    and carrying its request, and each class's markers read its own rows.

    Sample: the shared-usage world (every class at 1 Mbps x 2.5 percent) at fleets 500 and
    1,000 (realized 506 and 992) with the mounted terminal's extension 4,000 (realized 3,969),
    one snapshot, with a second fleet under 1,000, since the contract
    takes two fleets at least; the band points at the central values (:func:`central_bands`).

    Expected outcome: the classes in the class key's order; the mounted terminal's rows 506,
    992 and 3,969, requested 500, 1,000 and 4,000, its 3,969 row a directional row with its
    diagnostics; the small terminal's and the phone class's rows 506 and 992, requested 500 and
    1,000; each class's 0.10 crossing not reached by its own rows' last midpoint (capacity still
    rises steeply here): sqrt(992 x 3,969) = 1,984.25, rounded half up to 1,984, for the
    mounted terminal and sqrt(506 x 992) = 708.49, rounded to 708, for the others.
    """
    grid = synthetic_population_grid(MID_BAND_CELL_DEG, shared_usage_people)
    inputs = shared_usage(synthetic_saturation_inputs(grid, fleets=EXTENSION_TEST_FLEETS))
    sweep = SweepInputs.model_validate(
        {
            **inputs.sweep.model_dump(),
            "mounted_terminal_extension": EXTENSION_TEST_MOUNTED,
            "snapshots_directional": 1,
        }
    )
    curve = compute_saturation(
        central_bands(inputs.model_copy(update={"sweep": sweep})), grid, version_stamp=STAMP
    )
    assert [entry.device_class for entry in curve.classes] == list(DeviceClass)
    fleets_rows = [(506, 500), (992, 1_000)]
    expected = {SMALL: fleets_rows, MOUNTED: [*fleets_rows, (3_969, 4_000)], PHONE: fleets_rows}
    not_reached_by = {SMALL: 708, MOUNTED: 1_984, PHONE: 708}
    for device_class, keyed in expected.items():
        entry = class_curve(curve, device_class)
        assert [(row.fleet, row.requested_fleet) for row in entry.rows] == keyed
        assert entry.markers.saturation_number is None
        assert entry.markers.saturation_not_reached_by == not_reached_by[device_class]
    assert class_curve(curve, MOUNTED).rows[-1].directional is not None


TIER_TEST_CPUS = 8
"""The CPU count the memory-tier test pins (``os.process_cpu_count``, as the module reads it),
so the schedule it checks does not depend on the machine's CPUs."""


def test_the_memory_tiers_change_no_number(
    uniform_band: PopulationGrid,
    synthetic_saturation_inputs: SaturationInputsBuilder,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Objective: the sweep's schedule changes no number: when the memory budget limits the
    workers, each class runs down its fleets in memory tiers (each tier's largest task alone
    first, the schedule the real grid's top fleets take), and the curve equals the one run
    with a worker per CPU.

    Sample: the uniform band (B = 1) at 1,000 and 10,000 requested satellites (realized 992
    and 10,000), one snapshot, the CPU count pinned to 8; computed once at the default budget
    and once with the budget lowered to this process's peak plus two of the task peaks the
    first run measured, each taken times the margin as the worker count takes it, so whether
    the budget binds depends on neither the machine's CPUs nor a worker's own peak.

    Expected outcome: at the default budget (room for at least eight task peaks at the margin)
    the nine curves' largest tasks (three classes, six band points) run alone, in one run, and
    one pool runs the rest; with the budget binding (room for about two), each curve's 992
    task, a tier of its own (under half of 10,000), runs alone too: ten runs alone. The two
    curves are equal in everything but the run's own measurement.
    """
    monkeypatch.setattr(sat.os, "process_cpu_count", lambda: TIER_TEST_CPUS)
    inputs = small_sweep(
        synthetic_saturation_inputs(uniform_band, fleets=BAND_FLEETS, beams_per_satellite=ONE_BEAM)
    )
    alone_runs: list[list[float]] = []
    run_alone = sat._run_alone

    def counted_run_alone(
        indices: Sequence[int],
        tasks: Sequence[sat._SnapshotTask],
        contexts: Mapping[sat._CurveKey, sat._SweepContext],
        results: dict[int, sat._SnapshotResult],
    ) -> None:
        run_alone(indices, tasks, contexts, results)
        alone_runs.append([results[index].worker_peak_mb for index in indices])

    monkeypatch.setattr(sat, "_run_alone", counted_run_alone)
    free = compute_saturation(inputs, uniform_band, version_stamp=STAMP)
    assert len(alone_runs) == 1
    counted_mb = max(alone_runs[0]) * sat._WORKER_PEAK_MARGIN
    room = (sat._MEMORY_BUDGET_MB - sat._own_peak_mb()) / counted_mb
    assert room >= TIER_TEST_CPUS
    monkeypatch.setattr(sat, "_MEMORY_BUDGET_MB", sat._own_peak_mb() + 2 * counted_mb)
    tiered = compute_saturation(inputs, uniform_band, version_stamp=STAMP)
    assert len(alone_runs) == 1 + 1 + len(DeviceClass) + len(BandName)
    measured_as_free = tiered.model_copy(
        update={
            "provenance": tiered.provenance.model_copy(
                update={"run_measurement": free.provenance.run_measurement}
            )
        }
    )
    assert measured_as_free == free


def test_the_worker_count_takes_each_worker_at_its_reading_times_the_margin(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Objective: the worker count is what the budget holds at a task reading taken times the
    margin (a fresh worker's peak varies between runs of one task), at most one per CPU and one
    per remaining task, and at least one; the budget binds when it holds fewer than the CPUs.

    Sample: the parent's peak pinned at 1,000 MB under the 16,000 MB budget (15,000 MB of
    room), 16 CPUs, the margin 1.25; readings of 1,000, 760, 750 and 20,000 MB.

    Expected outcome, by hand: 1,000 MB counts as 1,250, so 12 workers (15 without the margin)
    and the budget binds; 760 MB counts as 950, so 15 (15.79 floored), and it binds; 750 MB
    counts as 937.5, so 16, the CPUs, and it does not bind; with 5 tasks left, 5; 20,000 MB
    counts as 25,000, past the room, so the one worker a sweep always runs.
    """
    monkeypatch.setattr(sat, "_own_peak_mb", lambda: 1_000.0)
    monkeypatch.setattr(sat.os, "process_cpu_count", lambda: 16)
    assert sat._MEMORY_BUDGET_MB == 16_000.0
    assert sat._WORKER_PEAK_MARGIN == 1.25
    assert sat._worker_count(1_000.0, 100) == 12
    assert sat._memory_binds(1_000.0)
    assert sat._worker_count(760.0, 100) == 15
    assert sat._memory_binds(760.0)
    assert sat._worker_count(750.0, 100) == 16
    assert not sat._memory_binds(750.0)
    assert sat._worker_count(750.0, 5) == 5
    assert sat._worker_count(20_000.0, 100) == 1


POOL_TEST_CPUS = 2
"""The CPU count the pool test pins, so its pool of three tasks runs two workers at once."""

POOL_TEST_READING_MB = 200.0
"""The task reading the pool test sizes its pool to: the budget holds far more than two
workers at it, so the pinned CPUs set the count."""


def recording_pool(built: list[tuple[int, int | None]]) -> type[ProcessPoolExecutor]:
    """A process pool class that appends each pool's workers and tasks per worker to ``built``
    before building it as the module would (the module builds its pools through
    ``sat.ProcessPoolExecutor``, which a test patches with this)."""

    class RecordedPool(ProcessPoolExecutor):
        """The process pool, recording how it is built."""

        def __init__(
            self,
            max_workers: int,
            mp_context: BaseContext,
            *,
            max_tasks_per_child: int | None = None,
        ) -> None:
            built.append((max_workers, max_tasks_per_child))
            super().__init__(max_workers, mp_context, max_tasks_per_child=max_tasks_per_child)

    return RecordedPool


def test_every_task_runs_in_a_fresh_worker_and_a_pool_counts_its_largest_peaks(
    monkeypatch: pytest.MonkeyPatch, synthetic_population_grid: GridBuilder
) -> None:
    """Objective: the sweep runs each snapshot task in a fresh worker of its own, in a pool and
    alone, since a process keeps memory its tasks freed (a worker kept for several tasks peaks
    above any one of them); a pool's bound is what its workers can hold at once: the sum of its
    largest task peaks, as many as its workers.

    Sample: three phone-class tasks of 342 satellites on one populated 2 degree cell, run by
    ``_run_pool`` at a reading of 200 MB with the CPU count pinned to 2, then two of them by
    ``_run_alone``, the module's process pool patched to record how each pool is built.

    Expected outcome: a pool of two workers, each running one task (``max_tasks_per_child``
    1), then the runs alone one worker at a time, each running one task; the count 2; every
    task's result stored; the pool's bound the sum of the two largest of its three task peaks,
    below the sum of all three.
    """
    built: list[tuple[int, int | None]] = []
    monkeypatch.setattr(sat, "ProcessPoolExecutor", recording_pool(built))
    monkeypatch.setattr(sat.os, "process_cpu_count", lambda: POOL_TEST_CPUS)
    tasks = [phone_snapshot_task(index, 342) for index in range(3)]
    context = one_patch_context(synthetic_population_grid)
    results: dict[int, sat._SnapshotResult] = {}
    workers, bound_mb = sat._run_pool(
        range(3), tasks, {PHONE: context}, POOL_TEST_READING_MB, results
    )
    alone: dict[int, sat._SnapshotResult] = {}
    sat._run_alone([0, 1], tasks, {PHONE: context}, alone)
    assert built == [(POOL_TEST_CPUS, 1), (1, 1)]
    assert workers == POOL_TEST_CPUS
    assert sorted(results) == [0, 1, 2]
    assert sorted(alone) == [0, 1]
    peaks = sorted((result.worker_peak_mb for result in results.values()), reverse=True)
    assert bound_mb == peaks[0] + peaks[1]
    assert bound_mb < sum(peaks)


# ---------------------------------------------------------------------------
# The identity check and the readings (the engine's side of the curve)
# ---------------------------------------------------------------------------

READING_PANEL_FACTOR = 0.616
"""The panel factor the readings below are taken at where the panel is not the point (d is then
the default, ``DOWNLINK_SHARE_DEFAULT``): 15.4 m^2, the investor's approved panel and the Iridium
dials' default (``APERTURE_M2_DEFAULT``), over the curve's 25 m^2 reference panel (ADR 005)."""

POWER_LAW_FLEETS = (342, 992)
"""The fleets of the hand-built reading curve's two rows (each realizes as itself)."""

POWER_LAW_FIRST_BEAMS = 1_000.0
"""Its useful beams at its first row, 342 satellites."""

POWER_LAW_EXPONENT = 0.5
"""The power of N its useful beams follow, L = 1,000 x (N / 342)^0.5: log-log reads it exactly,
a chord in N would not."""

POWER_LAW_MAXIMUM_USE = 4_000.0
"""Its maximum use, above both rows' ceilings."""

PHONE_GBPS_PER_BEAM = 8.0 * 0.65 / 1_000.0
"""A phone-class beam's capacity at the default inputs: 8 MHz x 0.65 bps/Hz = 5.2 Mbps."""

DEFAULT_BEAMS_PER_SATELLITE = 150.0
"""B at the default inputs: 1,000 x the 0.15 calibration at the reference panel."""


def power_law_rows() -> tuple[CurveRow, ...]:
    """Two phone-class rows at 342 and 992 satellites whose useful beams follow
    L = 1,000 x (N / 342)^0.5, with the phone class's capacity per beam and U = L / (N x B), as
    the module writes U; ceiling and supply equal L."""
    rows = []
    for fleet in POWER_LAW_FLEETS:
        beams = POWER_LAW_FIRST_BEAMS * (fleet / POWER_LAW_FLEETS[0]) ** POWER_LAW_EXPONENT
        rows.append(
            _row(fleet, beams, beams * PHONE_GBPS_PER_BEAM).model_copy(
                update={"ocean_factor": beams / (fleet * DEFAULT_BEAMS_PER_SATELLITE)}
            )
        )
    return tuple(rows)


def power_law_curve(
    rows: tuple[CurveRow, ...] | None = None, maximum_use: float = POWER_LAW_MAXIMUM_USE
) -> SaturationCurve:
    """A curve of the default inputs holding one phone-class curve on the given rows (the
    power-law rows by default) and maximum use."""
    return bare_curve(
        (
            ClassCurve(
                device_class=PHONE,
                rows=power_law_rows() if rows is None else rows,
                markers=bare_markers(maximum_use_beams=maximum_use),
            ),
        ),
        (),
    )


def test_the_identity_check_names_the_first_field_that_differs(
    committed_saturation_curve: SaturationCurve,
) -> None:
    """Objective: a curve is read only with the inputs it was computed for; the identity check
    names the first field, in the inputs' field order, whose value differs, as a dotted path,
    with the run's value and the curve's.

    Sample: the committed curve and its own parameters; the same at 10.5 MHz; with the phone
    class's busy-hour share doubled; with the sweep's first fleet moved, then with one fleet
    dropped; with both the spectrum and the first fleet changed.

    Expected outcome: the curve's own parameters pass. Each other case refuses with a
    SaturationCurveMismatchError (a SaturationCurveError and a ValueError) naming, in turn,
    ``spectrum_mhz``, ``classes.2.concurrency_peak`` (the phone class is the third class),
    ``sweep.fleets.0`` and ``sweep.fleets`` (a list whose length differs is itself the
    difference), with both values; the two changes name ``spectrum_mhz``, the earlier field.
    """
    curve = committed_saturation_curve
    inputs = curve.parameters
    check_curve_matches(inputs, curve)
    phone_index = list(DeviceClass).index(PHONE)
    phone = inputs.classes[phone_index]
    busier_phone = phone.model_copy(update={"concurrency_peak": 2 * phone.concurrency_peak})
    busier = tuple(busier_phone if entry is phone else entry for entry in inputs.classes)
    fleets = inputs.sweep.fleets
    moved = inputs.sweep.model_copy(update={"fleets": (fleets[0] + 1, *fleets[1:])})
    dropped = inputs.sweep.model_copy(update={"fleets": fleets[1:]})
    cases = [
        (
            inputs.model_copy(update={"spectrum_mhz": 10.5}),
            "spectrum_mhz",
            10.5,
            inputs.spectrum_mhz,
        ),
        (
            inputs.model_copy(update={"classes": busier}),
            f"classes.{phone_index}.concurrency_peak",
            busier_phone.concurrency_peak,
            phone.concurrency_peak,
        ),
        (inputs.model_copy(update={"sweep": moved}), "sweep.fleets.0", fleets[0] + 1, fleets[0]),
        (inputs.model_copy(update={"sweep": dropped}), "sweep.fleets", fleets[1:], fleets),
        (
            inputs.model_copy(update={"spectrum_mhz": 10.5, "sweep": moved}),
            "spectrum_mhz",
            10.5,
            inputs.spectrum_mhz,
        ),
    ]
    for changed, path, run_value, curve_value in cases:
        with pytest.raises(SaturationCurveMismatchError) as refused:
            check_curve_matches(changed, curve)
        assert (
            f"{path} is {json.dumps(run_value)} for this run but {json.dumps(curve_value)} in "
            "the curve's parameters"
        ) in str(refused.value), path
        assert isinstance(refused.value, SaturationCurveError)
        assert isinstance(refused.value, ValueError)


def test_a_reading_below_the_first_row_is_linear_through_the_origin(
    committed_saturation_curve: SaturationCurve,
) -> None:
    """Objective: below a class's first row a reading is linear through the origin, so the
    ocean factor U is flat there; the coverage floor (340) reads there, under the first row.

    Sample: the committed curve, every class, at 1 satellite, at half its first row's fleet and
    at the coverage floor.

    Expected outcome: useful beams and capacity are the fleet over the first row's fleet times
    the first row's values (to 1e-12 relative); U is the first row's exactly; the fleet's
    readings scale useful beams by the panel factor and capacity by d and the panel factor;
    people follow capacity (the scaled capacity over the class's busy-hour load from the curve's
    parameters, and ``people_at`` gives the same); the share of maximum use follows L.
    """
    curve = committed_saturation_curve
    load_mbps = {
        entry.device_class: entry.active_rate_mbps * entry.concurrency_peak
        for entry in curve.parameters.classes
    }
    for entry in curve.classes:
        first = entry.rows[0]
        assert first.fleet > SATELLITES_FOR_FULL_COVERAGE_DEFAULT
        for fleet in (1, first.fleet // 2, SATELLITES_FOR_FULL_COVERAGE_DEFAULT):
            share = fleet / first.fleet
            beams = useful_beams_at(curve, entry.device_class, fleet)
            assert beams == pytest.approx(share * first.useful_beams, rel=1e-12)
            capacity = capacity_gbps_at(curve, entry.device_class, fleet)
            assert capacity == pytest.approx(share * first.capacity_gbps, rel=1e-12)
            reading = read_fleet(
                curve,
                entry.device_class,
                fleet,
                downlink_share=DOWNLINK_SHARE_DEFAULT,
                panel_factor=READING_PANEL_FACTOR,
            )
            assert reading.ocean_factor == first.ocean_factor
            assert reading.useful_beams == pytest.approx(beams * READING_PANEL_FACTOR, rel=1e-12)
            assert reading.capacity_gbps == pytest.approx(
                capacity * DOWNLINK_SHARE_DEFAULT * READING_PANEL_FACTOR, rel=1e-12
            )
            assert reading.people == pytest.approx(
                reading.capacity_gbps * GBPS_TO_MBPS / load_mbps[entry.device_class], rel=1e-12
            )
            assert reading.people == people_at(
                curve,
                entry.device_class,
                fleet,
                downlink_share=DOWNLINK_SHARE_DEFAULT,
                panel_factor=READING_PANEL_FACTOR,
            )
            assert reading.share_of_maximum_use == pytest.approx(
                beams / entry.markers.maximum_use_beams, rel=1e-12
            )


def test_a_reading_at_a_fleet_of_zero_has_no_beams_and_no_ocean_factor(
    committed_saturation_curve: SaturationCurve,
) -> None:
    """Objective: an empty fleet places no beam: L, capacity, people and the share of maximum
    use are 0, and the ocean factor, beams over people per beam offered, does not exist.

    Sample: the committed curve, every class, at a fleet of 0.

    Expected outcome: each reading 0.0, and the fleet's readings with U None.
    """
    curve = committed_saturation_curve
    for device_class in DeviceClass:
        assert useful_beams_at(curve, device_class, 0) == 0.0
        assert capacity_gbps_at(curve, device_class, 0) == 0.0
        assert (
            people_at(
                curve,
                device_class,
                0,
                downlink_share=DOWNLINK_SHARE_DEFAULT,
                panel_factor=READING_PANEL_FACTOR,
            )
            == 0.0
        )
        assert read_fleet(
            curve,
            device_class,
            0,
            downlink_share=DOWNLINK_SHARE_DEFAULT,
            panel_factor=READING_PANEL_FACTOR,
        ) == FleetReading(
            fleet=0,
            useful_beams=0.0,
            capacity_gbps=0.0,
            share_of_maximum_use=0.0,
            ocean_factor=None,
            people=0.0,
        )


@pytest.mark.parametrize(
    "read",
    [
        useful_beams_at,
        capacity_gbps_at,
        partial(
            people_at, downlink_share=DOWNLINK_SHARE_DEFAULT, panel_factor=READING_PANEL_FACTOR
        ),
        partial(
            read_fleet, downlink_share=DOWNLINK_SHARE_DEFAULT, panel_factor=READING_PANEL_FACTOR
        ),
    ],
    ids=["useful beams", "capacity", "people", "the fleet's readings"],
)
def test_a_reading_past_a_classs_last_row_is_refused_naming_the_fleet_the_class_and_the_row(
    committed_saturation_curve: SaturationCurve,
    read: Callable[[SaturationCurve, DeviceClass, int], object],
) -> None:
    """Objective: a curve is never extrapolated or clamped: a reading past a class's last row
    is refused with a typed error naming the fleet, the class and the last row's fleet.

    Sample: the committed curve, every class, at its last row's fleet (read from the curve) and
    one satellite past it.

    Expected outcome: at the last row the reading is given; one satellite past it, a
    CurveBeyondLastRowError (a SaturationCurveError and a ValueError) naming the class, the
    last row's fleet and the fleet read.
    """
    curve = committed_saturation_curve
    for entry in curve.classes:
        last = entry.rows[-1]
        read(curve, entry.device_class, last.fleet)
        past = last.fleet + 1
        with pytest.raises(CurveBeyondLastRowError) as refused:
            read(curve, entry.device_class, past)
        assert (
            f"the {entry.device_class.value} curve's last row is at {last.fleet} satellites, and "
            f"a reading at {past} satellites lies past it"
        ) in str(refused.value)
        assert isinstance(refused.value, SaturationCurveError)
        assert isinstance(refused.value, ValueError)


def test_between_rows_a_reading_is_log_log() -> None:
    """Objective: between two rows a reading is log-log (ln L linear in ln N, and the same for
    capacity and U), never a chord in N; at a row it is the row's own value.

    Sample: a phone-class curve of two rows, 342 and 992 satellites, whose useful beams follow
    L = 1,000 x (N / 342)^0.5, its capacity 5.2 Mbps a beam and U = L / (N x 150); read at 582
    (the rows' geometric midpoint, rounded) and at 700.

    Expected outcome: L, capacity and U equal the power law at both fleets (to 1e-12), each at
    least 1 percent off the chord in N; at each row, the row's own values exactly.
    """
    curve = power_law_curve()
    low, high = power_law_rows()

    def chord(value_of: Callable[[CurveRow], float], fleet: int) -> float:
        """The value at the fleet on the straight line in N through the two rows' values."""
        share = (fleet - low.fleet) / (high.fleet - low.fleet)
        return value_of(low) + share * (value_of(high) - value_of(low))

    for fleet in (582, 700):
        beams = POWER_LAW_FIRST_BEAMS * (fleet / low.fleet) ** POWER_LAW_EXPONENT
        read = useful_beams_at(curve, PHONE, fleet)
        assert read == pytest.approx(beams, rel=1e-12)
        assert abs(read - chord(lambda row: row.useful_beams, fleet)) > 0.01 * read
        capacity = capacity_gbps_at(curve, PHONE, fleet)
        assert capacity == pytest.approx(beams * PHONE_GBPS_PER_BEAM, rel=1e-12)
        assert abs(capacity - chord(lambda row: row.capacity_gbps, fleet)) > 0.01 * capacity
        ocean_factor = read_fleet(
            curve, PHONE, fleet, downlink_share=1.0, panel_factor=1.0
        ).ocean_factor
        assert ocean_factor is not None
        assert ocean_factor == pytest.approx(
            beams / (fleet * DEFAULT_BEAMS_PER_SATELLITE), rel=1e-12
        )
        assert abs(ocean_factor - chord(lambda row: row.ocean_factor, fleet)) > 0.01 * ocean_factor
    for row in (low, high):
        assert useful_beams_at(curve, PHONE, row.fleet) == row.useful_beams
        assert capacity_gbps_at(curve, PHONE, row.fleet) == row.capacity_gbps
        at_row = read_fleet(curve, PHONE, row.fleet, downlink_share=1.0, panel_factor=1.0)
        assert at_row.ocean_factor == row.ocean_factor


def test_the_phone_class_reads_ninety_percent_of_maximum_use_at_its_ninety_percent_marker(
    committed_saturation_curve: SaturationCurve,
) -> None:
    """Objective: the log-log rule's two copies agree: the saturation module places the 90
    percent marker by it (``_fleet_reaching``, the fleet where L reaches 90 percent of maximum
    use, rounded half up) and the readings read L by it, so a reading at the marker gives 0.90
    of maximum use within the marker's rounding to a whole fleet.

    Sample: the committed curve's phone class at its 90 percent marker (read from the curve,
    never frozen) and one satellite either side, at d = 1 and the reference panel.

    Expected outcome: the marker is placed; the share of maximum use is under 0.90 one satellite
    below the marker and over it one satellite above (the crossing lies within half a satellite
    of the marker); at the marker it is 0.90 within half a satellite's change of the share (the
    larger of the two one-satellite steps, halved).
    """
    curve = committed_saturation_curve
    (phone,) = [entry for entry in curve.classes if entry.device_class is PHONE]
    marker = phone.markers.fleet_at_90pct_of_maximum_use
    assert marker is not None
    below, at, above = (
        read_fleet(curve, PHONE, fleet, downlink_share=1.0, panel_factor=1.0).share_of_maximum_use
        for fleet in (marker - 1, marker, marker + 1)
    )
    assert below < 0.9 < above
    assert at == pytest.approx(0.9, abs=max(at - below, above - at) / 2)


def test_people_are_the_capacity_over_the_busy_hour_load_times_d_and_the_panel() -> None:
    """Objective: people at a fleet are the capacity over the class's busy-hour load per person
    (its rate while active times its busy-hour share, from the curve's parameters), times the
    downlink share d and the panel factor, unrounded; a fleet's readings scale useful beams with
    the panel and capacity with d and the panel, and leave the share of maximum use and U on
    the curve's own basis.

    Sample: the power-law phone curve at its first row (342 satellites: 1,000 beams, 5.2 Gbps),
    d = 0.5 and the panel factor 0.616 (15.4 m^2 over 25).

    Expected outcome, worked by hand: people 1,000 beams x 277.333 people a beam (8 x 0.65 /
    (0.75 x 0.025)) x 0.5 x 0.616 = 85,418.67, unrounded; useful beams 616.0; capacity 5.2 x
    0.5 x 0.616 = 1.6016 Gbps; the share of maximum use 1,000 / 4,000 = 0.25; U the row's own.
    """
    curve = power_law_curve()
    first = power_law_rows()[0]
    people = people_at(curve, PHONE, first.fleet, downlink_share=0.5, panel_factor=0.616)
    assert people == pytest.approx(1_000.0 * (832.0 / 3.0) * 0.5 * 0.616, rel=1e-12)
    reading = read_fleet(curve, PHONE, first.fleet, downlink_share=0.5, panel_factor=0.616)
    assert reading == FleetReading(
        fleet=first.fleet,
        useful_beams=pytest.approx(616.0, rel=1e-12),
        capacity_gbps=pytest.approx(1.6016, rel=1e-12),
        share_of_maximum_use=pytest.approx(0.25, rel=1e-12),
        ocean_factor=first.ocean_factor,
        people=people,
    )


@pytest.mark.parametrize(
    ("downlink_share", "panel_factor", "named"),
    [
        (0.0, 1.0, "the downlink share d"),
        (1.5, 1.0, "the downlink share d"),
        (math.nan, 1.0, "the downlink share d"),
        (DOWNLINK_SHARE_DEFAULT, 0.0, "the panel factor"),
        (DOWNLINK_SHARE_DEFAULT, -1.0, "the panel factor"),
        (DOWNLINK_SHARE_DEFAULT, math.inf, "the panel factor"),
    ],
    ids=["d of 0", "d above 1", "d not a number", "a panel of 0", "a negative panel", "no panel"],
)
def test_the_readings_refuse_a_factor_out_of_its_range(
    downlink_share: float, panel_factor: float, named: str
) -> None:
    """Objective: d is a fraction above 0 and at most 1, the panel factor a positive number;
    the readings refuse anything else rather than publish people from it.

    Sample: the power-law curve at its first row, with each factor out of its range in turn.

    Expected outcome: ``people_at`` and ``read_fleet`` each raise ValueError naming the factor.
    """
    curve = power_law_curve()
    for read in (people_at, read_fleet):
        with pytest.raises(ValueError, match=named):
            read(curve, PHONE, 342, downlink_share=downlink_share, panel_factor=panel_factor)


def test_a_reading_the_curve_cannot_give_is_refused_with_a_typed_error() -> None:
    """Objective: a reading the curve cannot give is a typed error naming why, never a bare
    arithmetic failure.

    Sample: the power-law curve (the phone class only) read for the small terminal; at a fleet
    of -1; with its first row's L, capacity and U at 0, read between the rows; with a maximum
    use of 0, read at a row.

    Expected outcome: the curve holds no small terminal curve (a SaturationCurveError naming
    the class); a negative fleet is a ValueError; reading log-log through a row at 0 is a
    SaturationCurveError naming the quantity and both rows (a logarithm of 0 does not exist),
    while the row at 0 itself still reads; a share of a maximum use of 0 is a
    SaturationCurveError.
    """
    curve = power_law_curve()
    with pytest.raises(SaturationCurveError, match="holds no small_terminal_class curve"):
        useful_beams_at(curve, DeviceClass.SMALL_TERMINAL_CLASS, 342)
    with pytest.raises(ValueError, match="at least 0; got -1"):
        useful_beams_at(curve, PHONE, -1)
    low, high = power_law_rows()
    empty_low = low.model_copy(
        update={
            "useful_beams": 0.0,
            "capacity_gbps": 0.0,
            "ocean_factor": 0.0,
            "ceiling_beams": 0.0,
            "supply_beams": 0.0,
        }
    )
    through_zero = power_law_curve((empty_low, high))
    assert useful_beams_at(through_zero, PHONE, low.fleet) == 0.0
    with pytest.raises(SaturationCurveError, match="useful beams must be positive at both rows"):
        useful_beams_at(through_zero, PHONE, 582)
    with pytest.raises(SaturationCurveError, match="capacity must be positive at both rows"):
        capacity_gbps_at(through_zero, PHONE, 582)
    with pytest.raises(SaturationCurveError, match="maximum use is 0.0 beams"):
        read_fleet(
            power_law_curve(maximum_use=0.0), PHONE, 342, downlink_share=1.0, panel_factor=1.0
        )


ROWS_TOO_FAR_APART = "the two rows' values lie too far apart for this reading's arithmetic"
"""The refusal's cause between two rows whose ratio leaves a float's range."""

FIRST_ROW_TOO_LARGE = "that value is too large for this reading's arithmetic"
"""The refusal's cause below the first row when the fleet times its value leaves a float's range."""

READING_NEAR_FLOAT_MAX = (
    "the reading lies so near a float's largest value that this reading's arithmetic rounds past it"
)
"""The refusal's cause between two rows whose ratio is finite when the reading's exponential rounds
past the largest float."""

NEAR_FLOAT_MAX_LOW_BEAMS = 1.7976931348622133e308
"""A first row's useful beams just under the largest float: with the largest float at the second
row, their ratio is finite (1.000000000000057) and the reading at 991 satellites, within rounding
of the largest float, rounds past it in the exponential (checked by command)."""


@pytest.mark.parametrize(
    ("low_beams", "high_beams", "fleet", "cause"),
    [
        (5e-324, 1e300, 582, ROWS_TOO_FAR_APART),
        (1e300, 5e-324, 582, ROWS_TOO_FAR_APART),
        (1.5e308, 1.5e308, 341, FIRST_ROW_TOO_LARGE),
        (NEAR_FLOAT_MAX_LOW_BEAMS, sys.float_info.max, 991, READING_NEAR_FLOAT_MAX),
    ],
    ids=[
        "a ratio past a float's range",
        "a ratio under a float's range",
        "below the first row",
        "a reading rounding past the largest float",
    ],
)
def test_a_reading_past_a_floats_range_is_refused_with_a_typed_error(
    low_beams: float, high_beams: float, fleet: int, cause: str
) -> None:
    """Objective: a reading whose arithmetic leaves a float's range (the rows' values too far
    apart, or the fleet times the first row's value too large) is the curve's typed error naming
    that cause, never an infinity published as a number or a bare arithmetic ValueError, though
    the reading itself may be a finite number.

    Sample: a phone-class curve of two rows, 342 and 992 satellites, its useful beams 5e-324 and
    1e300 (their ratio past a float's range; the reading at 582 is 7.6e-13), then 1e300 and
    5e-324 (their ratio under it, 0; the reading 6.5e-12), each read at 582 between the rows;
    then 1.5e308 at the first row, read at 341 below it (341 x 1.5e308 past a float's range; the
    reading 1.4956e308); then 1.7976931348622133e308 and the largest float, read at 991 between
    them (their ratio finite, the reading within rounding of the largest float, which the
    exponential rounds past: the guard that keeps a bare OverflowError from leaving the reader).

    Expected outcome: SaturationCurveError naming the class's useful beams, the fleet and the
    cause: the rows' values too far apart between the rows, the first row's value too large
    below it, the reading too near a float's largest value at 991; at each row the row's own
    value still reads.
    """
    low, high = _row(342, low_beams, 1.0), _row(992, high_beams, 2.0)
    curve = power_law_curve((low, high))
    with pytest.raises(
        SaturationCurveError,
        match=f"the phone_class curve's useful beams at {fleet} satellites, .*: {cause}",
    ):
        useful_beams_at(curve, PHONE, fleet)
    assert useful_beams_at(curve, PHONE, 342) == low_beams
    assert useful_beams_at(curve, PHONE, 992) == high_beams


def test_the_readings_and_the_iridium_family_find_a_class_curve_by_one_lookup() -> None:
    """Objective: one lookup finds a class's central curve, for the readings and for the Iridium
    family's class blocks, which keeps no copy of its own.

    Sample: the power-law curve (the phone class only); the Iridium module.

    Expected outcome: the contract's ``class_curve_of`` returns the phone class's curve and
    refuses the small terminal naming it; the Iridium module's lookup is that very function, and
    it holds no ``_class_curve``.
    """
    curve = power_law_curve()
    assert saturation_curve.class_curve_of(curve, PHONE) is curve.classes[0]
    with pytest.raises(SaturationCurveError, match="holds no small_terminal_class curve to read"):
        saturation_curve.class_curve_of(curve, DeviceClass.SMALL_TERMINAL_CLASS)
    assert iridium.class_curve_of is saturation_curve.class_curve_of
    assert not hasattr(iridium, "_class_curve")


def test_the_synthetic_curve_fixture_matches_its_dials_and_loads_as_promoted(
    synthetic_saturation_curve: Callable[[IridiumDials], SaturationCurve], tmp_path: Path
) -> None:
    """Objective: the synthetic-curve fixture stamps matching parameters for any Iridium dials
    and builds a curve the loader accepts as promoted, its rows spanning the real grid and every
    row hand-workable (its markers are the module's own, ``_markers``, by construction: the
    fixture is a valid curve for the engine's tests, not an oracle of the marker rules).

    Sample: the default Iridium dials, the same at 10.5 MHz, and at the 25 m^2 reference panel
    (another panel than the default 15.4 m^2).

    Expected outcome: each curve's parameters are ``saturation_inputs_for`` of its dials with a
    valid input hash, so the identity check passes for its dials (and the 10.5 MHz curve is
    refused for the default dials, naming ``spectrum_mhz``); it passes the completeness check
    and, written as the promotion writes it, loads equal; every class's rows run from 342 to
    40,000 satellites (to 64,009 for the mounted terminal); at every row L = N x 150 (U = 1) and
    capacity is L x the spectrum x the class's central SE / 1,000.
    """
    default_dials = IridiumDials()
    for dials in (default_dials, IridiumDials(spectrum_mhz=10.5), IridiumDials(aperture_m2=25.0)):
        curve = synthetic_saturation_curve(dials)
        assert curve.parameters == saturation_inputs_for(dials)
        assert curve.input_hash == curve_input_hash(curve.parameters)
        check_curve_matches(saturation_inputs_for(dials), curve)
        check_curve_complete(curve)
        path = tmp_path / "synthetic_curve.json"
        path.write_text(render_artifact_json(curve) + ARTIFACT_FILE_END, encoding="utf-8")
        assert load_saturation_curve(path) == curve
        central_se = {
            entry.device_class: entry.spectral_efficiency_bps_per_hz
            for entry in curve.parameters.classes
        }
        for entry in curve.classes:
            last = 64_009 if entry.device_class is DeviceClass.MOUNTED_TERMINAL_CLASS else 40_000
            assert (entry.rows[0].fleet, entry.rows[-1].fleet) == (342, last)
            for row in entry.rows:
                assert row.useful_beams == pytest.approx(row.fleet * 150.0, rel=1e-12)
                assert row.ocean_factor == 1.0
                assert row.capacity_gbps == pytest.approx(
                    row.useful_beams * dials.spectrum_mhz * central_se[entry.device_class] / 1e3,
                    rel=1e-12,
                )
    wider = synthetic_saturation_curve(IridiumDials(spectrum_mhz=10.5))
    with pytest.raises(SaturationCurveMismatchError, match="spectrum_mhz is 8.0 for this run"):
        check_curve_matches(saturation_inputs_for(default_dials), wider)


def test_the_short_curve_fixture_ends_at_its_row_and_refuses_a_reading_past_it(
    short_saturation_curve: Callable[[IridiumDials, int], SaturationCurve],
) -> None:
    """Objective: the short-curve variant ends every curve at a given row and keeps the dials'
    parameters, so the identity check passes and a reading past its last row is refused.

    Sample: the default dials cut at 3,025 satellites (the realized fleet of the 3,000
    request); a fleet past it, 3,072; a cut at 3,000, which is no row; a cut at 342, the first
    row, which keeps one row.

    Expected outcome: every class's and band point's rows end at 3,025, each not reached by its
    kept rows' last midpoint, sqrt(1,980 x 3,025) = 2,447.3, rounded half up to 2,447; the
    identity check passes; the completeness check refuses the short rows; a reading
    at 3,025 is given (L = 3,025 x 150), and one at 3,072 is a CurveBeyondLastRowError naming
    the class, 3,025 and 3,072; the cut at 3,000 is a ValueError, and so is the cut at 342 (a
    curve's markers read the elasticity between two rows).
    """
    dials = IridiumDials()
    curve = short_saturation_curve(dials, 3_025)
    curves = [(entry.rows, entry.markers) for entry in curve.classes]
    curves += [(band.rows, band.markers) for band in curve.bands]
    for rows, markers in curves:
        assert (rows[-2].fleet, rows[-1].fleet) == (1_980, 3_025)
        assert markers.saturation_not_reached_by == 2_447
    check_curve_matches(saturation_inputs_for(dials), curve)
    with pytest.raises(SaturationCurveError, match="rows stand at the requested fleets"):
        check_curve_complete(curve)
    for device_class in DeviceClass:
        assert useful_beams_at(curve, device_class, 3_025) == pytest.approx(3_025 * 150.0)
        with pytest.raises(
            CurveBeyondLastRowError,
            match=(
                f"the {device_class.value} curve's last row is at 3025 satellites, and a "
                "reading at 3072 satellites lies past it"
            ),
        ):
            useful_beams_at(curve, device_class, 3_072)
    with pytest.raises(ValueError, match="3000 is not a row of every curve"):
        short_saturation_curve(dials, 3_000)
    with pytest.raises(ValueError, match="a cut at 342 keeps 1 row"):
        short_saturation_curve(dials, 342)


def test_a_curve_cut_short_carries_the_markers_its_kept_rows_give(
    committed_saturation_curve: SaturationCurve,
    cut_saturation_curve: Callable[[SaturationCurve, int], SaturationCurve],
) -> None:
    """Objective: the short-curve builder recomputes each curve's markers from its kept rows
    and its own maximum use (the module's ``_markers``), so a cut is a valid curve whatever
    markers the full curve placed: a saturation number past the cut becomes not reached by it
    (setting only ``saturation_not_reached_by``, as the builder once did, would leave a curve
    with both, which the contract refuses).

    Sample: the committed curve, whose markers reach saturation (read from it, never frozen),
    cut at 3,025 satellites (the 3,000 request, before every saturation number it places) and
    at the sweep's last fleet (the mounted terminal's extension cut away).

    Expected outcome: at each cut, every class's and band point's rows are its rows up to the
    cut, its markers ``_markers`` of those rows at its maximum use, valid as the contract's; a
    curve whose rows are all kept keeps the committed markers; a saturation number the full
    curve places past the cut is not reached, by the kept rows' last midpoint (the geometric
    mean of the last two kept rows' fleets, rounded half up).
    """
    curve = committed_saturation_curve
    full = [(entry.device_class, entry.rows, entry.markers) for entry in curve.classes]
    full += [(band.point.name, band.rows, band.markers) for band in curve.bands]
    early_cut = 3_025
    assert any(
        markers.saturation_number is not None and markers.saturation_number > early_cut
        for _, _, markers in full
    )
    sweep_last = math.prod(walker_shape(curve.parameters.sweep.fleets[-1]))
    for last_fleet in (early_cut, sweep_last):
        cut = cut_saturation_curve(curve, last_fleet)
        kept = [(entry.rows, entry.markers) for entry in cut.classes]
        kept += [(band.rows, band.markers) for band in cut.bands]
        for (key, full_rows, full_markers), (rows, markers) in zip(full, kept, strict=True):
            assert rows == tuple(row for row in full_rows if row.fleet <= last_fleet)
            assert markers == sat._markers(key, rows, full_markers.maximum_use_beams)
            assert ClassMarkers.model_validate(markers.model_dump()) == markers
            if rows == full_rows:
                assert markers == full_markers
            if full_markers.saturation_number is not None and (
                full_markers.saturation_number > last_fleet
            ):
                assert markers.saturation_number is None
                assert markers.saturation_not_reached_by == round_half_up(
                    math.sqrt(rows[-2].fleet * rows[-1].fleet)
                )
