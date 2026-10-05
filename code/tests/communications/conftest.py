"""Shared fixtures for the communications test suite (clean-rewrite, slim).

This conftest is the slim rewrite version: it provides the default ``CommsConfig``
fixture, built purely on the rewritten ``communications.config``, and the Iridium
scenario and artifact paths (from the repository-anchored fixtures in
``tests/conftest.py``, never the working directory).
The pre-rewrite old tree (its src modules, test files, and scenario YAML) was
retired in the investor-directed 2026-07-07 alignment cleanup, so the whole
``tests/communications/`` directory now collects and runs cleanly. The live suite
covers the High-Bandwidth Cellular Pure Play model (formerly Model A), the Iridium
model (formerly Model B), the ground comparison, and the cross-import guard.

It also provides the saturation module's synthetic worlds: a builder of synthetic global
population grids and a builder of the curve's inputs for them
(``synthetic_population_grid``, ``synthetic_saturation_inputs``), session-scoped so a
test module can compute a world's curve once and share it.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from pathlib import Path
from typing import Protocol

import numpy as np
import pytest

from communications.config import CommsConfig
from communications.constants import GBPS_TO_MBPS
from communications.saturation import PopulationGrid
from communications.saturation_curve import (
    DemandInputs,
    SaturationInputs,
    ShellInputs,
    SweepInputs,
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


@pytest.fixture
def default_comms_config() -> CommsConfig:
    """Return the default (central-case) comms config."""
    return CommsConfig()


@pytest.fixture(scope="session")
def iridium_yaml(scenarios_dir: Path) -> Path:
    """The promoted Iridium scenario, ``scenarios/iridium.yaml``."""
    return scenarios_dir / "iridium.yaml"


@pytest.fixture(scope="session")
def iridium_saturation_yaml(scenarios_dir: Path) -> Path:
    """The saturation companion scenario, ``scenarios/iridium_saturation.yaml``."""
    return scenarios_dir / "iridium_saturation.yaml"


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
