"""Shared fixtures for the communications test suite.

It provides the Iridium scenario and the committed artifact's paths (from the
repository-anchored fixtures in ``tests/conftest.py``, never the working directory). The
suite covers the High-Bandwidth Cellular Pure Play model (formerly Model A), the Iridium
model (formerly Model B), the saturation curve, the ground comparison, and the
cross-import guard.

It also provides the saturation module's synthetic worlds: a builder of synthetic global
population grids and a builder of the curve's inputs for them
(``synthetic_population_grid``, ``synthetic_saturation_inputs``), session-scoped so a
test module can compute a world's curve once and share it.

And the curves the engine's tests read, session-scoped: the committed curve, loaded with the
loader (``committed_saturation_curve``); a builder of a synthetic curve for any Iridium dials,
its parameters the inputs those dials imply, so the identity check passes, and its rows
spanning the real grid, so every fleet a test reads sits inside it
(``synthetic_saturation_curve``); a builder of the same curve cut short at a given row, for a
reading past a class's last row (``short_saturation_curve``); and the cut itself, for any
curve (``cut_saturation_curve``).
"""

from __future__ import annotations

import hashlib
import math
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Protocol

import numpy as np
import pytest

from communications import saturation as sat
from communications.config import IridiumDials
from communications.constants import GBPS_TO_MBPS, SATURATION_CURVE_PATH_DEFAULT, DeviceClass
from communications.saturation import PopulationGrid
from communications.saturation_curve import (
    SATURATION_CURVE_SCHEMA_VERSION,
    BandCurve,
    BandName,
    ClassCurve,
    ClassMarkers,
    CurveProvenance,
    CurveRow,
    DemandInputs,
    DirectionalDiagnostics,
    RunMeasurement,
    SaturationCurve,
    SaturationInputs,
    ShellInputs,
    SweepInputs,
    TrimAtFloor,
    curve_input_hash,
    load_saturation_curve,
    saturation_inputs_for,
    walker_shape,
)

SYNTHETIC_NORTH_EDGE_DEG = 90.0
"""A synthetic grid's northern edge: it starts at the north pole, as the curve requires."""

SYNTHETIC_WEST_EDGE_DEG = -180.0
"""A synthetic grid's western edge."""

SYNTHETIC_LATITUDE_SPAN_DEG = 180.0
"""The latitudes a synthetic (global) grid spans."""

SYNTHETIC_LONGITUDE_SPAN_DEG = 360.0
"""The longitudes a synthetic (global) grid spans."""

SYNTHETIC_DENSITY_THRESHOLD_PER_KM2 = 1e-9
"""The synthetic worlds' demand threshold: every populated cell is demand, since their
cells may hold far fewer people per km^2 than the central threshold of 1."""

PeopleAt = Callable[[np.ndarray, np.ndarray], np.ndarray]
"""People per cell from the cell centres' latitudes and longitudes, degrees: two arrays of
the grid's shape in, one array of that shape out."""

SYNTHETIC_OCEAN_FACTOR = 1.0
"""The synthetic curve's ocean factor at every row: every beam over people, so L = N x B, the
no-ocean bound, and every reading is hand-workable (L, capacity and people linear in N)."""

SYNTHETIC_MAXIMUM_USE_OVER_LAST_ROW = 2.0
"""The synthetic curve's maximum use over its last row's useful beams. With L linear in N the
elasticity is 1 at every midpoint, so no crossing under 0.10 or 0.25 is reached, and L stays
under 90 percent of maximum use: the module's own marker rules (``_markers``, which give the
synthetic curve its markers) place no marker, each curve not reached by its last row."""

SYNTHETIC_TRIM = 0.0
"""The synthetic phone class's interference trim at every floor: none."""

SYNTHETIC_STAMP = "synthetic"
"""The synthetic curve's version stamp."""

NO_STACKED_BEAMS = DirectionalDiagnostics(
    kept_stacked_share=0.0, median_separation_deg=None, mean_full_sum_interference_db=None
)
"""A directional row's diagnostics when it keeps no stacked beam (the synthetic curve's)."""


SyntheticCurveBuilder = Callable[[IridiumDials], SaturationCurve]
"""The builder ``synthetic_saturation_curve`` returns: Iridium dials in, the curve whose
parameters they imply out (spelled the same way in the tests that take it, which cannot import
from this file)."""

ShortCurveBuilder = Callable[[IridiumDials, int], SaturationCurve]
"""The builder ``short_saturation_curve`` returns: Iridium dials and a last row's fleet in, the
synthetic curve for the dials with every curve ending at that row out."""

CurveCut = Callable[[SaturationCurve, int], SaturationCurve]
"""The cut ``cut_saturation_curve`` returns: any curve and a row's fleet in, the curve with every
curve ending at that row out."""

MIN_ROWS_FOR_MARKERS = 2
"""The fewest rows a curve's markers can be read on: the elasticity is read between two rows
(as the sweep's at least two fleets give every computed curve)."""


def _synthetic_rows(
    requested: Sequence[int],
    beams_per_satellite: float,
    gbps_per_beam: float,
    *,
    sectored: bool,
    trim_floors_dbi: tuple[float, ...] | None,
) -> tuple[CurveRow, ...]:
    """One synthetic curve's rows at the requested fleets: L = N x B at U = 1, its ceiling and
    supply equal to L, capacity L x the beam's rate; diagnostics with nothing stacked where the
    class has sky sectors, and a trim of 0 at each floor where one is asked."""
    rows = []
    for requested_fleet in requested:
        fleet = math.prod(walker_shape(requested_fleet))
        beams = SYNTHETIC_OCEAN_FACTOR * fleet * beams_per_satellite
        rows.append(
            CurveRow(
                fleet=fleet,
                requested_fleet=requested_fleet,
                useful_beams=beams,
                useful_beams_spread=0.0,
                capacity_gbps=beams * gbps_per_beam,
                ocean_factor=SYNTHETIC_OCEAN_FACTOR,
                ceiling_beams=beams,
                supply_beams=beams,
                directional=NO_STACKED_BEAMS if sectored else None,
                trim=(
                    None
                    if trim_floors_dbi is None
                    else tuple(
                        TrimAtFloor(floor_dbi=floor, trim=SYNTHETIC_TRIM)
                        for floor in trim_floors_dbi
                    )
                ),
            )
        )
    return tuple(rows)


def _synthetic_markers(curve_key: DeviceClass | BandName, rows: Sequence[CurveRow]) -> ClassMarkers:
    """A synthetic curve's markers: the module's own (``_markers``) on its rows, against its
    maximum use, :data:`SYNTHETIC_MAXIMUM_USE_OVER_LAST_ROW` x the last row's L (derived here
    alone, for every class and band point)."""
    maximum_use = SYNTHETIC_MAXIMUM_USE_OVER_LAST_ROW * rows[-1].useful_beams
    return sat._markers(curve_key, rows, maximum_use)


def build_synthetic_curve(dials: IridiumDials) -> SaturationCurve:
    """Return a synthetic curve whose parameters are ``saturation_inputs_for(dials)``.

    Every class and band point at the parameters' requested fleets (the real grid, 342 to
    40,000 realized; the mounted terminal with its extension, to 64,009), each row L = N x B
    at U = 1 with capacity L x the spectrum x the class's central SE (the phone class's for a
    band point, B a band point's own when it sets one), its markers the module's own on its rows
    (none placed), so the identity check passes for the dials and the curve passes the
    completeness check the loader runs. It is a valid curve for the engine's tests, not an
    oracle of the marker rules, which are tested where they live.
    """
    parameters = saturation_inputs_for(dials)
    sweep = parameters.sweep
    central_beams = sat._beams_per_satellite(parameters.shell)
    sectored = {
        entry.device_class: bool(entry.sector_wedges_per_ring) for entry in parameters.classes
    }
    gbps_per_beam = {
        entry.device_class: parameters.spectrum_mhz
        * entry.spectral_efficiency_bps_per_hz
        / GBPS_TO_MBPS
        for entry in parameters.classes
    }
    classes = []
    for device_class in DeviceClass:
        requested = (
            sweep.fleets + sweep.mounted_terminal_extension
            if device_class is DeviceClass.MOUNTED_TERMINAL_CLASS
            else sweep.fleets
        )
        rows = _synthetic_rows(
            requested,
            central_beams,
            gbps_per_beam[device_class],
            sectored=sectored[device_class],
            trim_floors_dbi=(
                parameters.trim.floors_dbi if device_class is DeviceClass.PHONE_CLASS else None
            ),
        )
        classes.append(
            ClassCurve(
                device_class=device_class,
                rows=rows,
                markers=_synthetic_markers(device_class, rows),
            )
        )
    bands = []
    for point in parameters.bands:
        rows = _synthetic_rows(
            sweep.fleets,
            central_beams if point.beams_per_satellite is None else point.beams_per_satellite,
            gbps_per_beam[DeviceClass.PHONE_CLASS],
            sectored=sectored[DeviceClass.PHONE_CLASS],
            trim_floors_dbi=None,
        )
        bands.append(
            BandCurve(point=point, rows=rows, markers=_synthetic_markers(point.name, rows))
        )
    return SaturationCurve(
        schema_version=SATURATION_CURVE_SCHEMA_VERSION,
        version_stamp=SYNTHETIC_STAMP,
        parameters=parameters,
        input_hash=curve_input_hash(parameters),
        provenance=CurveProvenance(
            grid_file_name=Path(parameters.demand.grid_path).name,
            grid_sha256=parameters.demand.grid_sha256,
            citations=(),
            licence="none (synthetic)",
            method=(
                "synthetic, built by the test suite, never computed: L = N x B at every row "
                "(U = 1), capacity L x the spectrum x the class's central SE"
            ),
            checks_passed=(
                "L at most min(ceiling, supply) and the ceiling at most maximum use at every "
                "row, by construction",
            ),
            run_measurement=RunMeasurement(wall_time_s=0.0, peak_memory_mb=0.0),
        ),
        classes=tuple(classes),
        bands=tuple(bands),
        limits=(
            "A synthetic test curve: every beam over people (U = 1), so L, capacity and people "
            "are linear in N and no marker is placed.",
        ),
    )


def cut_curve_short(curve: SaturationCurve, last_fleet: int) -> SaturationCurve:
    """Return a curve with every class's and band point's rows cut after the row at
    ``last_fleet``, each curve's markers recomputed from its kept rows and its own maximum use
    by the module's ``_markers`` (so they are valid on any curve: each marker is the one the
    kept rows place, and a saturation number they no longer reach becomes not reached by the
    cut), its parameters unchanged (so the identity check still passes, while the completeness
    check refuses its short rows).

    Raises:
        ValueError: If ``last_fleet`` is not the fleet of a row every curve holds, or keeps
            fewer than :data:`MIN_ROWS_FOR_MARKERS` rows (the markers read the elasticity
            between rows).
    """
    holding = [entry.rows for entry in curve.classes] + [band.rows for band in curve.bands]
    if any(last_fleet not in [row.fleet for row in rows] for rows in holding):
        raise ValueError(
            f"{last_fleet} is not a row of every curve; the phone class's rows are "
            f"{[row.fleet for row in curve.classes[-1].rows]}"
        )

    def kept(rows: tuple[CurveRow, ...]) -> tuple[CurveRow, ...]:
        cut = tuple(row for row in rows if row.fleet <= last_fleet)
        if len(cut) < MIN_ROWS_FOR_MARKERS:
            raise ValueError(
                f"a cut at {last_fleet} keeps {len(cut)} row, and a curve's markers need "
                f"{MIN_ROWS_FOR_MARKERS}"
            )
        return cut

    classes = []
    for entry in curve.classes:
        rows = kept(entry.rows)
        markers = sat._markers(entry.device_class, rows, entry.markers.maximum_use_beams)
        classes.append(entry.model_copy(update={"rows": rows, "markers": markers}))
    bands = []
    for band in curve.bands:
        rows = kept(band.rows)
        markers = sat._markers(band.point.name, rows, band.markers.maximum_use_beams)
        bands.append(band.model_copy(update={"rows": rows, "markers": markers}))
    return curve.model_copy(update={"classes": tuple(classes), "bands": tuple(bands)})


class SaturationInputsBuilder(Protocol):
    """The builder ``synthetic_saturation_inputs`` returns: a grid and the sweep in, the
    curve's inputs out."""

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


@pytest.fixture(scope="session")
def iridium_yaml(scenarios_dir: Path) -> Path:
    """The promoted Iridium scenario, ``scenarios/iridium.yaml``."""
    return scenarios_dir / "iridium.yaml"


@pytest.fixture(scope="session")
def promoted_iridium_artifact(repo_dir: Path) -> Path:
    """The committed promoted artifact, ``communications/models/iridium/default.json``."""
    return repo_dir / "communications" / "models" / "iridium" / "default.json"


@pytest.fixture(scope="session")
def synthetic_population_grid() -> Callable[[float, PeopleAt], PopulationGrid]:
    """Return a builder of synthetic global population grids for the saturation tests.

    The builder takes a cell size, degrees, and the people per cell as a function of the
    cell centres' latitudes and longitudes, and returns a global grid from the north pole and
    180 degrees west, float32 like the shipped grid. Its SHA-256 is the digest of its array's
    bytes, a content identity the synthetic inputs carry in ``demand.grid_sha256``.
    """

    def build(cell_deg: float, people_at: PeopleAt) -> PopulationGrid:
        n_lat = round(SYNTHETIC_LATITUDE_SPAN_DEG / cell_deg)
        n_lon = round(SYNTHETIC_LONGITUDE_SPAN_DEG / cell_deg)
        latitudes = SYNTHETIC_NORTH_EDGE_DEG - (np.arange(n_lat) + 0.5) * cell_deg
        longitudes = SYNTHETIC_WEST_EDGE_DEG + (np.arange(n_lon) + 0.5) * cell_deg
        lat_grid, lon_grid = np.meshgrid(latitudes, longitudes, indexing="ij")
        people = np.asarray(people_at(lat_grid, lon_grid), dtype=np.float32)
        return PopulationGrid(
            population=people,
            lat_top_deg=SYNTHETIC_NORTH_EDGE_DEG,
            lon_left_deg=SYNTHETIC_WEST_EDGE_DEG,
            cell_deg=cell_deg,
            source="synthetic",
            citation="synthetic",
            file_name=f"synthetic_{cell_deg:g}_deg",
            sha256=hashlib.sha256(people.tobytes()).hexdigest(),
        )

    return build


@pytest.fixture(scope="session")
def synthetic_saturation_inputs() -> SaturationInputsBuilder:
    """Return a builder of the curve's inputs for a synthetic grid.

    The builder takes the grid and, by keyword, the requested ``fleets``, the phone class's
    ``snapshots`` (default 1) and ``beams_per_satellite`` (default None, the central 150 the
    calibration gives; another B sets the calibration to B / 1000 at the reference panel).
    Every other input is the default but the demand: the grid's SHA-256 and a threshold that
    counts every populated cell.
    """

    def build(
        grid: PopulationGrid,
        *,
        fleets: tuple[int, ...],
        snapshots: int = 1,
        beams_per_satellite: float | None = None,
    ) -> SaturationInputs:
        shell = (
            ShellInputs()
            if beams_per_satellite is None
            else ShellInputs(
                reuse_calibration_gbps_per_mhz_per_se=beams_per_satellite / GBPS_TO_MBPS
            )
        )
        return SaturationInputs(
            shell=shell,
            demand=DemandInputs(
                grid_sha256=grid.sha256,
                density_threshold_per_km2=SYNTHETIC_DENSITY_THRESHOLD_PER_KM2,
            ),
            sweep=SweepInputs(fleets=fleets, snapshots_phone_central=snapshots),
        )

    return build


@pytest.fixture(scope="session")
def committed_saturation_curve(repo_dir: Path) -> SaturationCurve:
    """The committed promoted curve, ``communications/models/iridium/saturation_curve.json``,
    loaded with ``load_saturation_curve`` (its schema, input hash and completeness checked).

    Its numbers are the promotion's. The curve's own tests read what they need from it and
    freeze none of them; the Iridium model's end-to-end tests (``test_iridium_model.py``)
    freeze the people and markers the engine reads from it, as the committed ``default.json``
    does, so a re-promotion re-freezes those on purpose (the re-promotion rule).
    """
    return load_saturation_curve(repo_dir / SATURATION_CURVE_PATH_DEFAULT)


@pytest.fixture(scope="session")
def synthetic_saturation_curve() -> SyntheticCurveBuilder:
    """Return a builder of a synthetic curve for any Iridium dials (``build_synthetic_curve``).

    Its parameters are ``saturation_inputs_for(dials)`` with a valid input hash, so the
    identity check passes for those dials; its rows span the real grid (342 to 40,000, and
    64,009 for the mounted terminal), so every fleet a test reads (2,000 and every scenario's
    steady state among them) sits inside it; it passes the completeness check the loader runs,
    so it can be written to a file a scenario's ``iridium.saturation.curve_path`` names.
    """
    return build_synthetic_curve


@pytest.fixture(scope="session")
def short_saturation_curve() -> ShortCurveBuilder:
    """Return a builder of the synthetic curve for any Iridium dials cut short at a given row
    (``cut_curve_short``, each curve's markers recomputed from its kept rows), for a reading
    past a class's last row: its parameters are still the dials' (the identity check passes),
    while the completeness check refuses its rows, so it is read in Python, never loaded from a
    file."""

    def build(dials: IridiumDials, last_fleet: int) -> SaturationCurve:
        return cut_curve_short(build_synthetic_curve(dials), last_fleet)

    return build


@pytest.fixture(scope="session")
def cut_saturation_curve() -> CurveCut:
    """Return the cut itself (``cut_curve_short``), for a test that cuts a curve other than the
    synthetic one: the committed curve, say, whose markers reach saturation, so the cut's
    markers are shown recomputed from the kept rows (the test modules cannot import this file,
    under the suite's importlib import mode)."""
    return cut_curve_short
