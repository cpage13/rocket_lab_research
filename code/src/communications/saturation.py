"""The saturation curve: how many co-channel beams a Walker shell keeps lit over people.

The one module that imports numpy (ADR 010). For each device class on one set of inputs
(:class:`~communications.saturation_curve.SaturationInputs`) it computes, at each fleet of
the sweep, L: the most co-channel beams the shell can keep lit over the places people live,
and their capacity. A 0 dBi phone-class device cannot tell satellites apart, so its
co-channel footprints must not overlap on the same ground; a directional terminal can, so
its class stacks further layers from satellites its beam separates (the small terminal and
the mounted terminal, by the saturation strategy's sky-sector rules D1 to D6). L rises with
the fleet, then flattens as every inhabited place is served by its best satellites; the
knee is the class's spectrum bound (ADR 005). Everything is computed with the band in
full-time use (d = 1, ADR 008) at the reference panel; the engine applies d and the
scenario's panel when it reads the curve.

The stages, numbered as the saturation strategy's locked stage order numbers them (its § 2),
for one class on one set of inputs; this version runs stages 2 to 11 for every class (stage
7 for the two directional classes) and stage 12 for the phone class's central curve:

1. **Inputs**, held by the contract: :class:`~communications.saturation_curve.SaturationInputs`.
2. **Demand cells.** Every cell of the shipped grid (ADR 009) with at least the threshold's
   people per km^2: its centre, its area on the sphere, its people, and its people cap in
   beams, people x take-up / people per beam, where people per beam is the spectrum times the
   class's central SE (a beam's rate) over the class's busy-hour load per person.
3. **The shell and the snapshots.** A circular Walker Delta shell: P = round(sqrt(N)) planes
   of S = round(N / P) satellites (Python's ``round``, an exact half to the even neighbour,
   the curve's pinned convention; the contract's ``walker_shape``), the realized fleet P x S
   keying the row and the request carried on it, phasing F = 1, two-body motion with the
   Earth turning under it. The snapshot times are drawn once per run,
   ``numpy.random.default_rng(seed).uniform(0, sidereal day, n)``, n the most snapshots any
   curve takes, and shared by every fleet and curve (a curve at fewer snapshots takes the first
   of them).
4. **The view and the beam.** The elevation mask's central-angle limit; a square aperture's
   half-power beam, beamwidth factor x wavelength / side, and its footprint, pi / 4 x (r
   theta) x (r theta / (cos(scan) sin(elevation))) with r the slant range, tabulated against
   the central angle and read by linear interpolation; the beams per satellite B derived
   from the capacity calibration and the panel, never set.
5. **The pairs in view.** Every satellite-cell pair whose cell centre sees the satellite
   above the mask; for a directional class, the elevation and azimuth at which the cell sees
   the satellite (they place the pair in a sky sector) and the direction between them.
6. **The allocation, phone class, smallest footprint first.** A snapshot's pairs fall into
   geometric footprint bands with edges ``geomspace(min footprint x 0.999, max footprint x
   1.001, bands + 1)``. Band by band from the smallest, each pair asks for min(one layer, the
   cell's area left / its footprint); a few alternating passes scale the band by every
   satellite's beams left, then by every cell's area and people left; the band is committed
   before the next. Limits: B beams per satellite; one co-channel layer per cell (its area);
   the cell's people cap; one layer per satellite per cell. Small overhead footprints fit
   the most beams into the same land, so this order maximizes capacity; a proportional
   fill stalls near saturation. At a directional class's own people cap it is that class's
   first layer (rule D2).
7. **The allocation, directional classes** (the strategy's rules D1 to D6). D1: the
   terminal's sky above the mask splits into sectors of equal solid angle, ring by ring from
   the zenith, each ring in equal azimuth wedges from north. D3: a satellite serves a cell
   when its committed layer covers at least f_serve = 1 / SINR_1 of the cell's area. D4: the
   remaining beams are spent by the same banded fill over (cell, sector) keys, a key's area
   the cell's less the first layer's from that sector, a pair's cap one layer less its
   first-layer beams; before each band its candidates, taken by (cell, footprint,
   satellite), are admitted only at least one terminal beamwidth from every satellite
   serving the cell in another sector and from every candidate of the cell admitted earlier
   in the band in another sector (same-sector satellites exempt).
8. **Capacity (d = 1).** A phone beam carries the spectrum times the class's central SE, so
   a snapshot's capacity is L times that. A directional cell's sub-pairs are priced by the
   full sum of its other layers (D5: first layers not against each other, nor same-sector
   layers; each weighted by its share of the cell at the terminal's Gaussian main lobe,
   floored at the pattern floor), and a cell keeps its stacked layers only when they do not
   lower its capacity (D6: the dropped beams stay spent, and L counts only kept beams).
9. **The rows.** At each fleet, the snapshot means of L and of capacity, the spread of L,
   the ocean factor U = L / (N x B), and the two bounds: the ceiling (each cell in view
   served by its smallest footprint in view, one layer for the phone class and one per sky
   sector for a directional class, capped by its people) and the supply (each satellite's
   beams, capped by what its cells could take); for a directional class, its kept stacked
   share (the share of L in the kept stacked layers of cells their first layer covers, each
   on a layer of another sector), their median separation from their cell's nearest layer in
   another sector and their mean full-sum interference.
10. **Maximum use**, in closed form and independent of the fleet: every cell served by the
    best satellite the shell can ever offer it, at central angle max(0, |latitude| -
    inclination), capped by its people; for a directional class one layer per sky sector,
    each at the best its ring allows (an upper bound: whether its azimuth is reachable is
    ignored).
11. **The markers**, on the rows: the elasticity of capacity, d ln C / d ln N, at each
    interval's geometric midpoint; the saturation number is the first crossing under 0.10,
    interpolated in ln N between the midpoints that straddle it and rounded half up (or the
    last fleet when it is not reached); beside it the crossing under 0.25 and the fleet at
    which L reaches 90 percent of maximum use (log-log between rows), each None when not
    reached, or when the rows cannot place it: the 0.25 crossing when it lies before the
    first midpoint (the geometric mean of the first two rows), the 90 percent fleet when the
    first row already reaches it (the curve's limits then say so). The markers read maximum
    use, never a sweep-dependent ceiling.
12. **The interference trim** (the phone class's central curve; a reported band the engine's
    people never read), at every row on the first snapshots of the draw: power control gives
    every beam equal flux at its target, so its power goes as r^2 / g(eta), g = cos^n of its
    scan angle; a victim cell's aggregate far-sidelobe interference over its own signal is x
    = gamma / G0 x the sum, over every lit satellite above its horizon, of the satellite's
    summed beam powers x g toward the victim / r^2, G0 the panel's broadside directivity;
    the victims are served cells drawn without replacement in proportion to their beams,
    from a fresh seeded draw at each row, so a row does not depend on the order of the
    fleets; the trim is 1 - the victims' mean of log2(1 + 1 / (1 + x)), at each far-sidelobe
    floor gamma. The directional classes carry none: each terminal's own pattern suppresses
    the leak (a stated limit).

**The band points.** Beside the phone class's central curve, one curve per band point, each
the central curve but for one changed input, at the bands' snapshots over the same fleets,
with its own rows, maximum use and markers: the taper (the beam's half-power width); the
taper with wider co-channel spacing (the ground a co-channel beam occupies over its 3 dB
footprint, scaling the area per beam in the fill, the two bounds and maximum use alike); 10
and 100 people per km^2 (the demand threshold); the 0.5 degree grid (the shipped cells summed
2 x 2); and 48 beams per satellite. They carry no trim.

The checks raise :class:`SaturationInvariantError`: the bounds (L at most min(ceiling,
supply) and the ceiling at most maximum use, at every snapshot of every class and band
point, 1e-9 relative); the stall floor (the phone class's central L at least the sweep's
floor x min(ceiling, supply) from 20,000 satellites up, at every snapshot and in the means;
not the band points); capacity per satellite never rising between consecutive rows of any
class or band point by more than 2 percent of the earlier row (the snapshots' noise).

The curves' snapshots run in separate processes, each task sent its own curve's demand cells
and limits. Each curve's largest task runs first and measures a worker's peak memory; then
as many workers run at once as keep the parent's peak plus their summed peaks under the 16 GB
budget, at most one per CPU: every other task in one pool when the budget allows a worker per
CPU, otherwise each curve in memory tiers down its fleets, each tier sized by its own largest
task (one process at a time only at the top of the grid). The curve records the wall time
and that bound (each worker reports its own peak; the bound is the parent's peak plus the
summed peaks of the largest set of workers alive at once).

**The command** promotes the curve, from ``code/``::

    uv run python -m communications.saturation scenarios/iridium.yaml \\
        communications/models/iridium/saturation_curve.json --version-stamp <stamp>

The full promotion of 2026-10-06 (the shipped scenario, 40 footprint bands, a shared machine
of 16 CPUs and 32 GB) measured 1,564 s of wall time, about 26 minutes, and a peak-memory bound
of 11,945 MB, under the 16 GB budget (``time -l`` reported a largest resident set of 7.14 GB);
the curve's ``provenance.run_measurement`` carries the same two figures.

It loads the scenario, narrows it to its Iridium dials (a scenario without an ``iridium:``
block is refused before anything runs), refuses a destination the shared writer would refuse
(before the computation, so a bad path costs no run), computes the curve those dials imply,
logs its summary, checks that it is complete and writes it through the shared writer. A
relative output path anchors to the repository root, a relative scenario path to the working
directory; the stamp defaults to today's ISO date. It follows the shared command conventions
(:mod:`common.cli`): status on stderr, an expected failure one ``ERROR:`` line and exit status
1 (a sweep that fails too: a saturation worker that dies, most likely out of memory, or runs
out of memory), a usage error exit status 2. It reads no curve, so a stale or missing curve
never blocks its own regeneration.

Public: :func:`load_population_grid`, :class:`PopulationGrid`, :func:`compute_saturation`,
:func:`promote_saturation_curve`, :func:`main`, :class:`PopulationGridError`,
:class:`SaturationInvariantError` and :class:`SaturationSweepError`. Everything else is
private; ``_allocate`` is the seam the tests drive with explicit satellite positions;
``_class_row`` and ``_band_row`` (one class's or one band point's row at one requested fleet)
are the seams the drift tests recompute a committed curve's rows through, and
``_plan_maximum_use`` on the curve's own plans (``_class_plan``, ``_band_plan``) what they
rebuild every class's and band point's maximum use through.
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
from collections.abc import Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from dataclasses import dataclass, replace
from datetime import date
from enum import StrEnum
from itertools import pairwise
from multiprocessing import get_context
from pathlib import Path
from typing import Final

import numpy as np
import numpy.typing as npt

from common.cadence import round_half_up
from common.cli import (
    EXIT_ERROR,
    EXIT_OK,
    CliArgumentParser,
    configure_cli_logging,
    describe_failure,
)
from common.file_io import (
    ModelFileError,
    SourceCheckout,
    artifact_write,
    locate_source_checkout,
    write_files_with_rollback,
)
from communications.config import load_comms_config
from communications.constants import (
    APERTURE_REFERENCE_M2,
    GBPS_TO_MBPS,
    GRID_AGGREGATION_SHIPPED,
    DeviceClass,
)
from communications.iridium import iridium_dials_of
from communications.saturation_curve import (
    SATURATION_CURVE_SCHEMA_VERSION,
    BandCurve,
    BandName,
    BandPoint,
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
    TrimAtFloor,
    TrimInputs,
    check_curve_complete,
    curve_input_hash,
    saturation_inputs_for,
)
from communications.saturation_curve import walker_shape as _walker_shape

logger = logging.getLogger(__name__)

type _CurveKey = DeviceClass | BandName
"""What one curve of the sweep is for: a class (its central curve) or one of the phone class's
band points. The two enums' values never coincide, so a key names one curve."""

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
"""The most satellites whose grid windows are searched at once; fewer when their windows
would exceed :data:`_PAIR_SEARCH_CHUNK_ELEMENTS`. The pairs found do not depend on it."""

_PAIR_SEARCH_CHUNK_ELEMENTS: Final[int] = 12_000_000
"""The most window elements (satellites x window rows x window columns) one chunk of the
pair search holds, which bounds its temporary arrays: about 80 bytes an element at the
worst, every window cell a demand cell (measured with ``tracemalloc``), so one chunk stays
under 1 GB, a sixteenth of the run's 16 GB budget (the strategy's budget, SR-21), and even
sixteen workers searching at once fit. A wide view near a pole spans every column, so it
takes fewer satellites a chunk; the central shell's 500-satellite chunks hold about 3.6
million. The pairs found do not depend on it."""

_SKY_CHUNK_PAIRS: Final[int] = 2_000_000
"""Pairs whose sky sectors are computed at once, which bounds the temporary arrays (about
ten of 8 bytes a pair, so about 160 MB); the sectors do not depend on it."""

_ZENITH_ELEVATION_RAD: Final[float] = math.pi / 2
"""The zenith's elevation, radians: the top of a terminal's sky and of its first ring."""

_WINDOW_MARGIN_CELLS: Final[int] = 1
"""Cells added beyond the view's reach on every side of a satellite's search window, so a
cell whose centre lies in view is never cut off by rounding."""

_WINDOW_LATITUDE_CAP_DEG: Final[float] = 89.0
"""The latitude from which a search window takes every column: a view's span in longitude
is its width over the cosine of its poleward edge's latitude, which grows without bound
toward a pole, so a satellite whose view reaches this latitude searches the whole turn. It
decides no pair (every pair in view is found either way); it bounds the search's work."""

_WINDOW_SIDES: Final[int] = 2
"""A search window reaches as many columns east of its satellite's column as west, so one
turn of longitude takes half the grid's columns (rounded up) on each side."""

_WINDOW_CENTRE_CELLS: Final[int] = 1
"""A search window's centre row or column, the one under its satellite: a window reaching h
rows (or columns) on each side spans 2h + 1."""

_MIN_CHUNK_SATELLITES: Final[int] = 1
"""The fewest satellites a pair-search chunk holds: one satellite whose window alone exceeds
:data:`_PAIR_SEARCH_CHUNK_ELEMENTS` is still searched, whole, in a chunk of its own."""

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

_GAUSSIAN_BEAM_SOLID_ANGLE_FACTOR: Final[float] = 1.133
"""SOURCED_FACT (standard antenna theory): a circular Gaussian beam's solid angle is pi / (4
ln 2), about 1.133, times the square of its half-power beamwidth. A terminal of directivity D
spans 4 pi / D sr, so its half-power beamwidth is sqrt(4 pi / (1.133 x D)): 60.3 degrees at
10 dBi and 33.9 at 15 dBi, COMM-718's main lobes. Four figures, the curve's pinned convention
(the saturation strategy's rule D4)."""

_SPHERE_SOLID_ANGLE_SR: Final[float] = 4 * math.pi
"""The whole sphere's solid angle, sr: a beam of directivity D spans it over D."""

_GAUSSIAN_LOBE_DB_PER_BEAMWIDTH_SQUARED: Final[float] = -12.0
"""SOURCED_FACT (standard antenna theory): a Gaussian main lobe's gain falls as -12 (theta /
HPBW)^2 dB, so -3 dB at half the beamwidth, the definition of the half-power beamwidth
(COMM-718's Gaussian main lobe; the saturation strategy's rule D5)."""

_DECIBELS_PER_DECADE: Final[float] = 10.0
"""A power ratio in decibels is ten times its base-10 logarithm."""

_SERVED_BEAMS_FLOOR: Final[float] = 1e-9
"""A pair places a layer when it places more than this many beams; less is the passes'
rounding dust, not a layer. The proportional passes leave satellites and cells with about
1e-13 beams, which a later band spreads over many pairs; this floor sits about four orders
above that dust and far below any real layer (one whole layer of a 0.25 degree cell holds from
about a tenth of a beam, at the mask, to four and a half, overhead). It decides which pairs
can be stage 2's candidates (rule D4), which sub-pairs the full sum prices and which cells
carry stacked beams (rules D5 and D6), and the main-satellite and any-share serving sets of
the diagnostic (rule D3)."""

_COVERED_SHORTFALL_SHARE: Final[float] = 1e-9
"""The most of a cell's area its first layer may leave uncovered and still cover the cell, as a
share of the area. Where a band's area binds a cell, the fill's scale sets the cell's first
layer to its area exactly in arithmetic, so only rounding leaves a hair uncovered (at most about
1e-12 of a cell's area on the shipped grid, a cell holding up to dozens of pairs); a cell its
people cap or the satellites leave short misses by far more (1e-7 at the least there, most by
over 1e-3). The stacked layers' statistics count only covered cells (rule D4's stage 2 may
complete a short cell's first layer instead of stacking on it)."""

_MEDIAN_WEIGHT_SHARE: Final[float] = 0.5
"""A weighted median is the value at which the cumulative weight first reaches half."""

_FULL_SUM_BATCH_PAIRS: Final[int] = 4_000_000
"""The most ordered pairs of sub-pairs the full-sum pricing expands at once (cells are
batched whole), which bounds its temporary arrays: about 150 bytes a pair at the peak, so
about 0.6 GB; the prices do not depend on it."""

_NO_NEIGHBOUR_COSINE: Final[float] = -2.0
"""Below any cosine: the nearest-layer cosine of a sub-pair whose cell holds no served
sub-pair in another sector."""

_OPERATING_SINR: Final[float] = 1.0
"""SOURCED_ESTIMATE (COMM-429, the anchor's own reading point). The phone class's central SE
is the anchor read at the measured median SINR of 0 dB, 1 in linear terms; the interference
trim's extra aggregate x lowers it to 1 / (1 + x)."""

_HORIZON_ELEVATION_SINE: Final[float] = 0.0
"""A satellite reaches a victim cell in the interference trim when it stands above the cell's
horizon: the sine of its elevation there is above this."""

_COSINE_UNIT_BOUNDS: Final[tuple[float, float]] = (0.0, 1.0)
"""The scan cosine toward a satellite above a victim's horizon lies in this range (the scan is
under 90 degrees); one below the horizon, which the horizon rule drops, can read negative, so
the cosine is clipped into it before its power is taken."""

_TRIM_CHUNK_ELEMENTS: Final[int] = 6_000_000
"""The most victim-satellite pairs the interference trim sums at once (victims x satellites),
which bounds its temporary arrays: about ten arrays of 8 bytes a pair (the offsets' three
components among them), so about 0.5 GB. At 3,000 victims a chunk holds 2,000 satellites; the
trim depends on it only through the rounding of its sums."""

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

_SWEEP_TIER_FLEET_RATIO: Final[float] = 2.0
"""A memory tier of the sweep spans one class's largest remaining requested fleet down to
that over this ratio. A worker's peak grows about linearly with the fleet (the strategy's
budget, SR-21), so a tier's measured largest task bounds the rest of it, and each lower tier
measures again and runs more workers at once (one process at a time only at the top of the
grid, where one worker's peak nears the budget)."""

_TRACEBACK_QUOTES: Final[str] = "'\""
"""The quote marks a process pool fences a cause's formatted traceback with (``'''`` or three
double quotes), which a sweep's error leaves out when it names the cause."""

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

_GRID_PARSE_ERRORS: Final[tuple[type[Exception], ...]] = (
    OSError,
    ValueError,
    TypeError,
    EOFError,
    zipfile.BadZipFile,
)
"""What parsing a malformed archive can raise (numpy's loader, its zip reader, a member that
is not a scalar); each becomes one :class:`~common.file_io.ModelFileError`."""


class PopulationGridError(ValueError):
    """A population grid the curve cannot use: not the one expected, or not a global grid."""


class SaturationInvariantError(ValueError):
    """A curve breaks one of its invariants or its markers cannot be placed on its rows."""


class SaturationSweepError(ValueError):
    """A sweep that could not finish: a saturation worker died or ran out of memory, or the
    sweep's process pool broke with a stated cause. Nothing was computed past it, so nothing was
    written.

    Attributes:
        task_count: The sweep's snapshot tasks.
    """

    def __init__(self, message: str, task_count: int) -> None:
        """Build the error from its one-line message and the sweep's task count."""
        super().__init__(message)
        self.task_count = task_count


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
    ``allow_pickle=False``. Only the parsing calls sit inside a ``try``, so each refusal
    is raised once, never caught and wrapped again.

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
    except _GRID_PARSE_ERRORS as exc:
        raise ModelFileError(path, f"not a readable population grid ({exc})") from exc
    if not isinstance(loaded, np.lib.npyio.NpzFile):
        raise ModelFileError(path, "not an .npz archive of named arrays")
    with loaded as archive:
        missing = [member for member in _GRID_MEMBERS if member not in archive.files]
        if missing:
            raise ModelFileError(path, f"the population grid lacks {missing}")
        try:
            population = np.asarray(archive["population"])
            lat_top_deg = float(archive["lat_top_deg"])
            lon_left_deg = float(archive["lon_left_deg"])
            cell_deg = float(archive["cell_deg"])
            source = str(archive["source"])
            citation = str(archive["citation"])
        except _GRID_PARSE_ERRORS as exc:
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
# Stages 2 to 4: the demand cells, the beam and the shell
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


def _demand_cells(
    population: PopulationGrid,
    density_threshold_per_km2: float,
    grid_aggregation: int = GRID_AGGREGATION_SHIPPED,
) -> _DemandCells:
    """Return the grid's demand cells: every cell with at least the threshold's density.

    Args:
        population: A global population grid.
        density_threshold_per_km2: A cell is demand at this many people per km^2 or more.
        grid_aggregation: The grid's cells summed per side first (the shipped grid as it is
            at :data:`~communications.constants.GRID_AGGREGATION_SHIPPED`; 2 sums each 2 x 2
            block of cells into one cell twice as wide, the 0.5 degree band point's grid).

    Returns:
        The demand cells, in row-major order of the (summed) grid.

    Raises:
        PopulationGridError: If the grid is not global, or its rows or columns do not divide
            by the aggregation.
    """
    _check_global(population)
    people_grid = population.population.astype(np.float64)
    n_lat, n_lon = people_grid.shape
    if n_lat % grid_aggregation or n_lon % grid_aggregation:
        raise PopulationGridError(
            f"{population.file_name}: {n_lat} x {n_lon} cells do not sum {grid_aggregation} x "
            f"{grid_aggregation}"
        )
    if grid_aggregation != GRID_AGGREGATION_SHIPPED:
        n_lat, n_lon = n_lat // grid_aggregation, n_lon // grid_aggregation
        people_grid = people_grid.reshape(n_lat, grid_aggregation, n_lon, grid_aggregation).sum(
            axis=(1, 3)
        )
    cell_deg = population.cell_deg * grid_aggregation
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
        orbit_radius_km: The shell's orbit radius, km (the Earth's radius plus the altitude).
        max_central_angle_rad: The largest central angle at which a cell sees a satellite
            above the mask.
        central_angle_rad: The footprint table's central angles, overhead to the mask.
        footprint_km2: The footprint at each, km^2.
    """

    orbit_radius_km: float
    max_central_angle_rad: float
    central_angle_rad: npt.NDArray[np.float64]
    footprint_km2: npt.NDArray[np.float64]


def _central_angle_limit(shell: ShellInputs) -> float:
    """Return the largest central angle at which a satellite stands above the mask, radians."""
    mask_rad = math.radians(shell.elevation_mask_deg)
    orbit_radius_km = _EARTH_RADIUS_KM + shell.altitude_km
    return math.acos(_EARTH_RADIUS_KM * math.cos(mask_rad) / orbit_radius_km) - mask_rad


def _elevation_rad(
    central_angle_rad: npt.NDArray[np.float64], orbit_radius_km: float
) -> npt.NDArray[np.float64]:
    """Return the elevation at which a ground point sees a satellite at each central angle.

    The satellite stands r cos(g) - R above the point's horizon plane and r sin(g) along it
    (R the Earth's radius, r the orbit's), so its elevation is the angle of that offset.
    """
    return np.arctan2(
        orbit_radius_km * np.cos(central_angle_rad) - _EARTH_RADIUS_KM,
        orbit_radius_km * np.sin(central_angle_rad),
    )


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
    elevation = _elevation_rad(central_angle, orbit_radius_km)
    cos_scan = np.sin(elevation + central_angle)
    wavelength_m = _SPEED_OF_LIGHT_M_S / shell.carrier_hz
    beamwidth_rad = shell.beamwidth_factor * wavelength_m / math.sqrt(shell.reference_aperture_m2)
    across_km = slant_km * beamwidth_rad
    along_km = across_km / (cos_scan * np.sin(elevation))
    return _BeamModel(
        orbit_radius_km=orbit_radius_km,
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
# Stages 5, 6, 9 and 10: the pairs, the allocation (the seam), its bounds, maximum use
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


def _window_half_rows(cells: _DemandCells, max_central_angle_rad: float) -> int:
    """Return the rows either side of a satellite's row that its search window spans: the
    view's reach in rows, plus the margin."""
    return math.ceil(math.degrees(max_central_angle_rad) / cells.cell_deg) + _WINDOW_MARGIN_CELLS


def _search_chunks(
    satellites: _SatellitePositions, cells: _DemandCells, max_central_angle_rad: float
) -> list[tuple[int, int, int]]:
    """Return the pair search's chunks: (first satellite, one past the last, window half-columns).

    Satellites are taken in order, at most :data:`_PAIR_SEARCH_CHUNK_SATELLITES` a chunk, and
    fewer when the chunk's windows would hold more than :data:`_PAIR_SEARCH_CHUNK_ELEMENTS`
    elements (never fewer than :data:`_MIN_CHUNK_SATELLITES`). Every satellite of a chunk
    searches the chunk's widest window: the columns its view spans at its poleward edge plus
    the margin, or one full turn when the view reaches :data:`_WINDOW_LATITUDE_CAP_DEG`, never
    more.

    Args:
        satellites: The satellites.
        cells: The demand cells (their grid's layout).
        max_central_angle_rad: The view's central-angle limit.

    Returns:
        The chunks, tiling the satellites in order.
    """
    n_lon = cells.index.shape[1]
    limit_deg = math.degrees(max_central_angle_rad)
    window_cap_rad = math.radians(_WINDOW_LATITUDE_CAP_DEG)
    full_turn_half_cols: int = math.ceil(n_lon / _WINDOW_SIDES)
    window_rows = (
        _WINDOW_SIDES * _window_half_rows(cells, max_central_angle_rad) + _WINDOW_CENTRE_CELLS
    )

    def widest_half_columns(lat: npt.NDArray[np.float64]) -> int:
        """The columns either side of centre that the widest window of these satellites spans."""
        edge_lat = np.abs(lat) + max_central_angle_rad
        if edge_lat.max() >= window_cap_rad:
            return full_turn_half_cols
        half_cols_each = np.ceil(limit_deg / np.cos(edge_lat) / cells.cell_deg).astype(np.int64)
        return min(int(half_cols_each.max()) + _WINDOW_MARGIN_CELLS, full_turn_half_cols)

    chunks = []
    start = 0
    while start < satellites.count:
        stop = min(start + _PAIR_SEARCH_CHUNK_SATELLITES, satellites.count)
        half_cols = widest_half_columns(satellites.lat_rad[start:stop])
        window_cols = _WINDOW_SIDES * half_cols + _WINDOW_CENTRE_CELLS
        allowed = max(
            _MIN_CHUNK_SATELLITES, _PAIR_SEARCH_CHUNK_ELEMENTS // (window_rows * window_cols)
        )
        if stop - start > allowed:
            stop = start + allowed
            half_cols = widest_half_columns(satellites.lat_rad[start:stop])
        chunks.append((start, stop, half_cols))
        start = stop
    return chunks


def _pairs_in_view(
    satellites: _SatellitePositions, cells: _DemandCells, max_central_angle_rad: float
) -> _Pairs:
    """Return every pair whose cell centre sees its satellite above the mask.

    Each satellite searches a window of grid cells around the cell under it: every row the
    view reaches, and the columns the view spans at the window's poleward edge, plus a
    margin; when the view reaches :data:`_WINDOW_LATITUDE_CAP_DEG`, every column. A window
    never spans more than one turn of longitude, and every satellite of a chunk searches the
    chunk's widest window; a chunk holds at most :data:`_PAIR_SEARCH_CHUNK_SATELLITES`
    satellites, and fewer when their windows would hold more than
    :data:`_PAIR_SEARCH_CHUNK_ELEMENTS` elements (at least one satellite). The demand cells
    within the central-angle limit are kept. A window can reach a cell twice (rows clipped at
    a pole, or columns wrapped past the antimeridian), so each pair is kept once.

    Args:
        satellites: The satellites.
        cells: The demand cells.
        max_central_angle_rad: The view's central-angle limit.

    Returns:
        The pairs, ordered by satellite, then cell.
    """
    n_lat, n_lon = cells.index.shape
    half_rows = _window_half_rows(cells, max_central_angle_rad)
    row_offsets = np.arange(-half_rows, half_rows + 1)
    cos_limit = math.cos(max_central_angle_rad)
    satellite_xyz = _unit_vectors(satellites.lat_rad, satellites.lon_rad)
    found_satellite: list[npt.NDArray[np.int64]] = [np.empty(0, dtype=np.int64)]
    found_cell: list[npt.NDArray[np.int64]] = [np.empty(0, dtype=np.int64)]
    found_angle: list[npt.NDArray[np.float64]] = [np.empty(0, dtype=np.float64)]
    cell_deg = cells.cell_deg
    for start, stop, half_cols in _search_chunks(satellites, cells, max_central_angle_rad):
        lat = satellites.lat_rad[start:stop]
        lon = satellites.lon_rad[start:stop]
        centre_row = np.floor((cells.lat_top_deg - np.degrees(lat)) / cell_deg).astype(np.int64)
        centre_col = np.floor((np.degrees(lon) - cells.lon_left_deg) / cell_deg).astype(np.int64)
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


@dataclass(frozen=True)
class _SectorLayout:
    """A directional class's sky sectors (the saturation strategy's rule D1).

    The terminal's sky above the elevation mask in sectors of equal solid angle, ring by
    ring from the zenith; each ring splits into equal azimuth wedges counted from north.

    Attributes:
        wedges_per_ring: Each ring's wedges, from the zenith down.
        lower_edges_rad: Each ring's lower elevation, radians, from the zenith down; the last
            is the mask.
    """

    wedges_per_ring: tuple[int, ...]
    lower_edges_rad: tuple[float, ...]

    @property
    def count(self) -> int:
        """The number of sectors."""
        return sum(self.wedges_per_ring)


def _sector_layout(wedges_per_ring: tuple[int, ...], elevation_mask_deg: float) -> _SectorLayout:
    """Return a class's sky sectors of equal solid angle (rule D1).

    The sky above the mask spans 2 pi (1 - sin(mask)) sr and each of the n sectors takes
    Omega, that over n. A zone between two elevations spans 2 pi |sin(top) - sin(bottom)|, so
    the rings' lower edges run top down from sin(low) = sin(high) - w x Omega / (2 pi), w the
    ring's wedges, and the last ring ends exactly at the mask (rounding aside).

    Args:
        wedges_per_ring: The class's wedges per ring, from the zenith down.
        elevation_mask_deg: The elevation mask, degrees.

    Returns:
        The layout.
    """
    mask_rad = math.radians(elevation_mask_deg)
    sector_share = (math.sin(_ZENITH_ELEVATION_RAD) - math.sin(mask_rad)) / sum(wedges_per_ring)
    edges = []
    sin_high = math.sin(_ZENITH_ELEVATION_RAD)
    for wedges in wedges_per_ring:
        sin_low = sin_high - wedges * sector_share
        edges.append(math.asin(sin_low))
        sin_high = sin_low
    edges[-1] = mask_rad
    return _SectorLayout(wedges_per_ring=wedges_per_ring, lower_edges_rad=tuple(edges))


def _sector_of(
    elevation_rad: npt.NDArray[np.float64],
    azimuth_rad: npt.NDArray[np.float64],
    layout: _SectorLayout,
) -> npt.NDArray[np.int64]:
    """Return the sky sector of each direction: its ring by elevation, then its azimuth wedge.

    A ring holds the elevations from its lower edge (included) up to the ring above's lower
    edge (excluded), the first ring up to the zenith; an elevation under the last edge (the
    mask, which rounding at the view's limit can cross) falls in the last ring. A wedge is an
    equal slice of the ring's azimuths, counted from north through east. Sectors are numbered
    ring by ring from the zenith, each ring's wedges from north.

    Args:
        elevation_rad: The directions' elevations, radians.
        azimuth_rad: Their azimuths from north through east, radians, in [0, 2 pi).
        layout: The class's sectors.

    Returns:
        Each direction's sector.
    """
    lower = np.array(layout.lower_edges_rad)
    ring: npt.NDArray[np.int64] = np.minimum(
        np.searchsorted(-lower, -elevation_rad, side="left"), len(layout.wedges_per_ring) - 1
    )
    ring_wedges = np.array(layout.wedges_per_ring, dtype=np.int64)
    wedges = ring_wedges[ring]
    first_of_ring = (np.cumsum(ring_wedges) - ring_wedges)[ring]
    wedge = np.minimum((azimuth_rad / (math.tau / wedges)).astype(np.int64), wedges - 1)
    sector: npt.NDArray[np.int64] = first_of_ring + wedge
    return sector


def _pair_sectors(
    pairs: _Pairs,
    satellites: _SatellitePositions,
    cells: _DemandCells,
    orbit_radius_km: float,
    layout: _SectorLayout,
) -> npt.NDArray[np.int64]:
    """Return each pair's sky sector as its cell sees its satellite (rule D1).

    The satellite's elevation follows from the pair's central angle; its azimuth is the
    initial bearing of the great circle from the cell's centre to the sub-satellite point,
    from north through east. Computed :data:`_SKY_CHUNK_PAIRS` pairs at a time.

    Args:
        pairs: The pairs in view.
        satellites: The satellites.
        cells: The demand cells.
        orbit_radius_km: The shell's orbit radius, km.
        layout: The class's sectors.

    Returns:
        Each pair's sector.
    """
    sector = np.empty(pairs.satellite.size, dtype=np.int64)
    for start in range(0, pairs.satellite.size, _SKY_CHUNK_PAIRS):
        part = slice(start, start + _SKY_CHUNK_PAIRS)
        satellite, cell = pairs.satellite[part], pairs.cell[part]
        lat_cell, lat_satellite = cells.lat_rad[cell], satellites.lat_rad[satellite]
        dlon = satellites.lon_rad[satellite] - cells.lon_rad[cell]
        azimuth = np.mod(
            np.arctan2(
                np.sin(dlon) * np.cos(lat_satellite),
                np.cos(lat_cell) * np.sin(lat_satellite)
                - np.sin(lat_cell) * np.cos(lat_satellite) * np.cos(dlon),
            ),
            math.tau,
        )
        elevation = _elevation_rad(pairs.central_angle_rad[part], orbit_radius_km)
        sector[part] = _sector_of(elevation, azimuth, layout)
    return sector


@dataclass(frozen=True, eq=False)
class _PairDirections:
    """Each pair's direction from its cell's centre to its satellite, computed when needed.

    The angle between two satellites as a cell sees them is the arccos of the dot product of
    their two directions from it; the directions are formed for the pairs a rule asks about,
    never stored for every pair.

    Attributes:
        satellite: Each pair's satellite index.
        cell: Each pair's demand-cell index.
        satellite_km: The satellites' Earth-centred positions, km.
        cell_km: The demand cells' Earth-centred centres, km.
    """

    satellite: npt.NDArray[np.int64]
    cell: npt.NDArray[np.int64]
    satellite_km: npt.NDArray[np.float64]
    cell_km: npt.NDArray[np.float64]

    def of(self, index: npt.NDArray[np.int64]) -> npt.NDArray[np.float64]:
        """Return the unit directions of the pairs at ``index``, one row each."""
        offset = self.satellite_km[self.satellite[index]] - self.cell_km[self.cell[index]]
        return offset / np.linalg.norm(offset, axis=1, keepdims=True)


def _pair_directions(
    pairs: _Pairs, satellites: _SatellitePositions, cells: _DemandCells, orbit_radius_km: float
) -> _PairDirections:
    """Return the pairs' directions, from the satellites' and the cells' positions."""
    return _PairDirections(
        satellite=pairs.satellite,
        cell=pairs.cell,
        satellite_km=orbit_radius_km * _unit_vectors(satellites.lat_rad, satellites.lon_rad),
        cell_km=_EARTH_RADIUS_KM * cells.xyz,
    )


@dataclass(frozen=True, eq=False)
class _AllocationLimits:
    """What limits one class's allocation besides the cells' own areas, and how it is priced.

    Attributes:
        beams_per_satellite: B, the beams each satellite can light.
        people_per_beam: The people one beam serves at d = 1 (the class's).
        take_up: The share of a cell's residents counted as potential users.
        beam: The view's limit and the footprint table.
        footprint_bands: The fill's geometric footprint bands.
        passes: The proportional passes inside each band.
        spectrum_mhz: The held spectrum, MHz: a beam carries it times its SE.
        spectral_efficiency_bps_per_hz: The class's central SE, a one-layer beam's.
        directional: The class's rules D1 to D6; None for the phone class, which takes one
            co-channel layer.
    """

    beams_per_satellite: float
    people_per_beam: float
    take_up: float
    beam: _BeamModel
    footprint_bands: int
    passes: int
    spectrum_mhz: float
    spectral_efficiency_bps_per_hz: float
    directional: _DirectionalRules | None


@dataclass(frozen=True, eq=False)
class _Allocation:
    """One snapshot's allocation (d = 1), pair by pair, with its capacity and its two bounds.

    Attributes:
        satellite: Each pair's satellite index (the pairs in view, by satellite then cell).
        cell: Each pair's demand-cell index.
        footprint_km2: Each pair's footprint.
        beams: The beams each pair placed: its first layer, and for a directional class its
            stacked beams too, kept or dropped.
        useful_beams: L, the beams placed and kept.
        capacity_mbps: The beams' capacity: a phone beam carries the spectrum times the
            central SE; a directional cell, its kept layers priced by the full sum.
        ceiling_beams: The most the cells in view could use: each served by its smallest
            footprint in view, one layer for the phone class, one per sky sector for a
            directional class (the sector-rule ceiling), capped by its people.
        supply_beams: The most the satellites could place: each satellite's B, capped by
            what its cells could take one layer at a time.
        directional: The directional class's layers, prices and statistics; None for the
            phone class.
    """

    satellite: npt.NDArray[np.int64]
    cell: npt.NDArray[np.int64]
    footprint_km2: npt.NDArray[np.float64]
    beams: npt.NDArray[np.float64]
    useful_beams: float
    capacity_mbps: float
    ceiling_beams: float
    supply_beams: float
    directional: _DirectionalAllocation | None


@dataclass(frozen=True, eq=False)
class _FootprintBands:
    """A snapshot's geometric footprint bands, which order every fill smallest footprint first.

    Attributes:
        order: The pairs sorted by band (stable, so by pair index within a band).
        starts: Band b's pairs are ``order[starts[b]:starts[b + 1]]``.
    """

    order: npt.NDArray[np.int64]
    starts: npt.NDArray[np.int64]

    @property
    def count(self) -> int:
        """The number of bands."""
        return int(self.starts.size) - 1

    def members(self, band: int) -> npt.NDArray[np.int64]:
        """Return the pairs of one band."""
        return self.order[self.starts[band] : self.starts[band + 1]]


def _footprint_bands(footprint_km2: npt.NDArray[np.float64], bands: int) -> _FootprintBands:
    """Return the snapshot's footprint bands: edges ``geomspace(min footprint x 0.999, max
    footprint x 1.001, bands + 1)`` over every pair in view (none when no pair is in view)."""
    if footprint_km2.size == 0:
        return _FootprintBands(
            order=np.empty(0, dtype=np.int64), starts=np.zeros(bands + 1, dtype=np.int64)
        )
    edges = np.geomspace(
        footprint_km2.min() * _BAND_EDGE_LOW_FACTOR,
        footprint_km2.max() * _BAND_EDGE_HIGH_FACTOR,
        bands + 1,
    )
    band = np.clip(np.searchsorted(edges, footprint_km2, side="right") - 1, 0, bands - 1)
    order = np.argsort(band, kind="stable")
    return _FootprintBands(order=order, starts=np.searchsorted(band[order], np.arange(bands + 1)))


@dataclass(frozen=True, eq=False)
class _Remaining:
    """What the fills have left, drawn down in place band by band.

    Attributes:
        satellite_beams: Each satellite's beams left.
        key_area_km2: Each key's co-channel area left: a cell's for the first layer (one layer
            each), a cell's sky sector's for the stacked layers (rule D4).
        cell_beams: Each cell's people cap left, beams.
    """

    satellite_beams: npt.NDArray[np.float64]
    key_area_km2: npt.NDArray[np.float64]
    cell_beams: npt.NDArray[np.float64]


def _fill_band(
    asked_cap: npt.NDArray[np.float64],
    satellite: npt.NDArray[np.int64],
    key: npt.NDArray[np.int64],
    cell: npt.NDArray[np.int64],
    footprint_km2: npt.NDArray[np.float64],
    remaining: _Remaining,
    passes: int,
) -> npt.NDArray[np.float64]:
    """Fill one footprint band's pairs; draw ``remaining`` down in place; return their beams.

    Each pair asks for min(its cap, its key's area left / its footprint); the passes scale
    the band by every satellite's beams left, then by the tighter of every key's area left and
    every cell's people cap left (each scale at most 1); then the band is committed, so the
    next band sees only what remains. With a cell as its own key this is the phone
    allocation's band (the phone class's arithmetic, step for step).

    Args:
        asked_cap: Each pair's cap, beams.
        satellite: Each pair's satellite.
        key: Each pair's key (an index into ``remaining.key_area_km2``).
        cell: Each pair's cell.
        footprint_km2: Each pair's footprint.
        remaining: What is left, drawn down in place.
        passes: The proportional passes.

    Returns:
        Each pair's beams placed.
    """
    n_satellites = remaining.satellite_beams.size
    n_keys = remaining.key_area_km2.size
    n_cells = remaining.cell_beams.size
    satellite_beams = remaining.satellite_beams[satellite]
    key_area_km2 = remaining.key_area_km2[key]
    cell_beams = remaining.cell_beams[cell]
    asked = np.minimum(asked_cap, key_area_km2 / footprint_km2)
    for _ in range(passes):
        satellite_want = np.bincount(satellite, weights=asked, minlength=n_satellites)[satellite]
        asked = asked * np.minimum(
            _FULL_SCALE, satellite_beams / np.maximum(satellite_want, _DIVISION_FLOOR)
        )
        area_want = np.bincount(key, weights=asked * footprint_km2, minlength=n_keys)[key]
        beam_want = np.bincount(cell, weights=asked, minlength=n_cells)[cell]
        key_scale = np.minimum(_FULL_SCALE, key_area_km2 / np.maximum(area_want, _DIVISION_FLOOR))
        cell_scale = np.minimum(_FULL_SCALE, cell_beams / np.maximum(beam_want, _DIVISION_FLOOR))
        asked = asked * np.minimum(key_scale, cell_scale)
    np.subtract(
        remaining.satellite_beams,
        np.bincount(satellite, weights=asked, minlength=n_satellites),
        out=remaining.satellite_beams,
    )
    np.subtract(
        remaining.key_area_km2,
        np.bincount(key, weights=asked * footprint_km2, minlength=n_keys),
        out=remaining.key_area_km2,
    )
    np.subtract(
        remaining.cell_beams,
        np.bincount(cell, weights=asked, minlength=n_cells),
        out=remaining.cell_beams,
    )
    np.maximum(remaining.satellite_beams, _NONE_LEFT, out=remaining.satellite_beams)
    np.maximum(remaining.key_area_km2, _NONE_LEFT, out=remaining.key_area_km2)
    np.maximum(remaining.cell_beams, _NONE_LEFT, out=remaining.cell_beams)
    return asked


@dataclass(frozen=True, eq=False)
class _FirstLayer:
    """Stage 1's result: one co-channel layer per cell (the phone allocation; rule D2).

    Attributes:
        beams: Each pair's beams.
        useful_beams: L, summed band by band.
        remaining: What it leaves: each satellite's beams, each cell's area and people cap.
    """

    beams: npt.NDArray[np.float64]
    useful_beams: float
    remaining: _Remaining


def _first_layer(
    n_satellites: int,
    pairs: _Pairs,
    footprint_km2: npt.NDArray[np.float64],
    cells: _DemandCells,
    people_cap: npt.NDArray[np.float64],
    bands: _FootprintBands,
    limits: _AllocationLimits,
) -> _FirstLayer:
    """Fill one snapshot's pairs one layer deep, smallest footprint first (stage 6; rule D2).

    Band by band from the smallest footprints, each pair's cap is one layer (the cell's area
    over its footprint) and its key is its cell: per satellite at most B beams, per cell its
    area once and its people cap. The phone class's allocation, and, at a directional class's
    own people cap, that class's first layer.

    Args:
        n_satellites: The satellites in the snapshot.
        pairs: The pairs in view.
        footprint_km2: Each pair's footprint.
        cells: The demand cells.
        people_cap: Each cell's people cap, beams (the class's).
        bands: The snapshot's footprint bands.
        limits: B and the passes.

    Returns:
        The first layer and what it leaves.
    """
    beams = np.zeros(footprint_km2.size)
    remaining = _Remaining(
        satellite_beams=np.full(n_satellites, limits.beams_per_satellite),
        key_area_km2=cells.area_km2.copy(),
        cell_beams=people_cap.copy(),
    )
    one_layer = cells.area_km2[pairs.cell] / footprint_km2
    placed = 0.0
    for band in range(bands.count):
        members = bands.members(band)
        if members.size == 0:
            continue
        cell = pairs.cell[members]
        asked = _fill_band(
            one_layer[members],
            pairs.satellite[members],
            cell,
            cell,
            footprint_km2[members],
            remaining,
            limits.passes,
        )
        beams[members] = asked
        placed += float(asked.sum())
    return _FirstLayer(beams=beams, useful_beams=placed, remaining=remaining)


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


def _sector_ceiling(
    pairs: _Pairs,
    footprint_km2: npt.NDArray[np.float64],
    sector: npt.NDArray[np.int64],
    n_sectors: int,
    cells: _DemandCells,
    people_cap: npt.NDArray[np.float64],
) -> float:
    """Return the sector-rule ceiling (stage 9): the most a directional class's cells in view
    could use. Per cell in view, the sum over its sky sectors of its area over the sector's
    smallest footprint in view (a sector with no pair in view adds nothing), capped by its
    people cap.
    """
    best = np.full(cells.count * n_sectors, np.inf)
    np.minimum.at(best, pairs.cell * n_sectors + sector, footprint_km2)
    per_sector = np.repeat(cells.area_km2, n_sectors) / best
    per_cell = per_sector.reshape(cells.count, n_sectors).sum(axis=1)
    seen = np.bincount(pairs.cell, minlength=cells.count) > 0
    return float(np.minimum(per_cell[seen], people_cap[seen]).sum())


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
    """Allocate one snapshot's beams, smallest footprint first, price them and bound them.

    The private seam: it takes explicit satellite positions, so a test can place a
    satellite where it chooses. Stage 1 lays one layer at the class's people cap (rule D2;
    the phone class's whole allocation, a beam carrying the spectrum times its central SE);
    a directional class then stacks, prices and keeps by rules D1 and D3 to D6.

    Args:
        satellites: The satellites' sub-satellite points.
        cells: The demand cells.
        limits: B, the people per beam and take-up, the beam model, the bands and passes,
            the spectrum and the central SE, and a directional class's rules.

    Returns:
        The allocation, pair by pair, with L, its capacity, the ceiling and the supply.
    """
    pairs = _pairs_in_view(satellites, cells, limits.beam.max_central_angle_rad)
    footprint_km2 = np.interp(
        pairs.central_angle_rad, limits.beam.central_angle_rad, limits.beam.footprint_km2
    )
    people_cap = _people_cap(cells, limits)
    bands = _footprint_bands(footprint_km2, limits.footprint_bands)
    first = _first_layer(satellites.count, pairs, footprint_km2, cells, people_cap, bands, limits)
    supply_beams = _supply(
        satellites.count, pairs, footprint_km2, cells, people_cap, limits.beams_per_satellite
    )
    rules = limits.directional
    if rules is None:
        return _Allocation(
            satellite=pairs.satellite,
            cell=pairs.cell,
            footprint_km2=footprint_km2,
            beams=first.beams,
            useful_beams=first.useful_beams,
            capacity_mbps=first.useful_beams
            * limits.spectrum_mhz
            * limits.spectral_efficiency_bps_per_hz,
            ceiling_beams=_ceiling(pairs, footprint_km2, cells, people_cap),
            supply_beams=supply_beams,
            directional=None,
        )
    directional = _directional_allocation(
        satellites,
        pairs,
        footprint_km2,
        cells,
        first,
        bands,
        limits.beam.orbit_radius_km,
        limits.spectrum_mhz,
        rules,
        limits.passes,
    )
    return _Allocation(
        satellite=pairs.satellite,
        cell=pairs.cell,
        footprint_km2=footprint_km2,
        beams=directional.first_layer_beams + directional.stacked_beams,
        useful_beams=directional.useful_beams,
        capacity_mbps=directional.capacity_mbps,
        ceiling_beams=_sector_ceiling(
            pairs, footprint_km2, directional.sector, rules.layout.count, cells, people_cap
        ),
        supply_beams=supply_beams,
        directional=directional,
    )


def _maximum_use(cells: _DemandCells, limits: _AllocationLimits, inclination_deg: float) -> float:
    """Return maximum use: every cell served by the best satellites the shell can offer it.

    A shell of inclination i never flies above latitude i, so the best a cell at latitude
    lat can see is a satellite at central angle max(0, |lat| - i); a cell beyond the view's
    limit from there adds nothing. For the phone class, one layer from that satellite. For a
    directional class (stage 10), one layer per sky sector: the zenith cap's at that best
    satellite, each lower ring's at the ring's top edge, or at the best satellite where that
    stands lower, every wedge of a ring at its ring's footprint (an upper bound: whether each
    sector's azimuth is reachable is ignored), a ring the best satellite cannot reach adding
    nothing. Either way capped by the cell's people; it does not depend on the fleet.
    """
    best_angle = np.maximum(
        _OVERHEAD_CENTRAL_ANGLE_RAD, np.abs(cells.lat_rad) - math.radians(inclination_deg)
    )
    reachable = best_angle <= limits.beam.max_central_angle_rad
    people_cap = _people_cap(cells, limits)
    rules = limits.directional
    if rules is None:
        best_footprint = np.interp(
            best_angle[reachable], limits.beam.central_angle_rad, limits.beam.footprint_km2
        )
        return float(
            np.minimum(cells.area_km2[reachable] / best_footprint, people_cap[reachable]).sum()
        )
    orbit_radius_km = limits.beam.orbit_radius_km
    best_elevation = _elevation_rad(best_angle, orbit_radius_km)
    beams = np.zeros(cells.count)
    top = _ZENITH_ELEVATION_RAD
    for low, wedges in zip(rules.layout.lower_edges_rad, rules.layout.wedges_per_ring, strict=True):
        within = reachable & (np.minimum(best_elevation, top) >= low)
        top_angle = math.acos(_EARTH_RADIUS_KM * math.cos(top) / orbit_radius_km) - top
        angle = np.where(best_elevation <= top, best_angle, top_angle)[within]
        footprint = np.interp(angle, limits.beam.central_angle_rad, limits.beam.footprint_km2)
        beams[within] += wedges * cells.area_km2[within] / footprint
        top = low
    return float(np.minimum(beams, people_cap)[reachable].sum())


# ===========================================================================
# Stage 7: the directional classes' allocation (the saturation strategy's rules D1 to D6)
# ===========================================================================


class _ServingRule(StrEnum):
    """Which satellites serve a cell: the reference set of the pairwise admission (rule D3).

    The module allocates at :attr:`AT_SERVING_SHARE`. The other two exist for the mounted
    terminal's diagnostic (the saturation strategy's reproduction protocol), which reruns the
    module's allocation with the set at the cell's main satellite only and at any positive
    share.
    """

    AT_SERVING_SHARE = "at_serving_share"
    """A satellite serves a cell when its committed layer covers at least f_serve of the
    cell's area (rule D3)."""

    MAIN_SATELLITE = "main_satellite"
    """Only the cell's main first-layer satellite (the most first-layer area) serves it, and
    no stacked layer joins: the main satellite as the reference set, within this module's
    admission (its band-mate rule and same-sector exemption kept, a cell without a main
    satellite free to stack). It is the reference set of the saturation design's local
    prototype, which ``research/direct_communication/iridium_saturation_module.md`` names, but
    not that prototype's rule."""

    ANY_SHARE = "any_share"
    """Every satellite that places a layer in the cell serves it."""


@dataclass(frozen=True)
class _DirectionalRules:
    """A directional class's rules D1 to D6, each value derived from the curve's inputs.

    Attributes:
        layout: The terminal's sky sectors (D1).
        beamwidth_rad: Its half-power beamwidth, sqrt(4 pi / (1.133 x D)), D the linear
            directivity (D4, D5).
        single_layer_sinr: SINR_1 = 2^(SE_central / anchor) - 1, the single-layer operating
            point that gives the class's central SE (D5).
        serving_share: f_serve = 1 / SINR_1, the share at which a co-directional interferer
            alone costs a victim 3 dB (D3).
        se_anchor_bps_per_hz: The link mapping's anchor, SE = anchor x log2(1 + SINR) (D5).
        se_central_bps_per_hz: The class's central SE: a first-layer beam alone (D6).
        pattern_floor_db: The terminal pattern's floor, dB below its peak (D5).
        serving_rule: Which satellites serve a cell (D3); the module's is
            :attr:`_ServingRule.AT_SERVING_SHARE`.
    """

    layout: _SectorLayout
    beamwidth_rad: float
    single_layer_sinr: float
    serving_share: float
    se_anchor_bps_per_hz: float
    se_central_bps_per_hz: float
    pattern_floor_db: float
    serving_rule: _ServingRule


def _directional_rules(
    inputs: SaturationInputs, class_inputs: ClassInputs
) -> _DirectionalRules | None:
    """Return a class's directional rules, or None for a class without sky sectors (the phone
    class, which takes one co-channel layer).

    Args:
        inputs: The curve's inputs (the SE anchor, the pattern floor, the mask).
        class_inputs: The class (its central SE, directivity and sector layout).

    Returns:
        The rules, at the module's serving rule.
    """
    if not class_inputs.sector_wedges_per_ring:
        return None
    directivity = 10 ** (class_inputs.directivity_dbi / _DECIBELS_PER_DECADE)
    single_layer_sinr = (
        2 ** (class_inputs.spectral_efficiency_bps_per_hz / inputs.se_anchor_bps_per_hz) - 1
    )
    return _DirectionalRules(
        layout=_sector_layout(class_inputs.sector_wedges_per_ring, inputs.shell.elevation_mask_deg),
        beamwidth_rad=math.sqrt(
            _SPHERE_SOLID_ANGLE_SR / (_GAUSSIAN_BEAM_SOLID_ANGLE_FACTOR * directivity)
        ),
        single_layer_sinr=single_layer_sinr,
        serving_share=1 / single_layer_sinr,
        se_anchor_bps_per_hz=inputs.se_anchor_bps_per_hz,
        se_central_bps_per_hz=class_inputs.spectral_efficiency_bps_per_hz,
        pattern_floor_db=inputs.sidelobe_floor_db,
        serving_rule=_ServingRule.AT_SERVING_SHARE,
    )


def _layer_share(
    beams: npt.NDArray[np.float64],
    footprint_km2: npt.NDArray[np.float64],
    cell_area_km2: npt.NDArray[np.float64],
) -> npt.NDArray[np.float64]:
    """Return the share of its cell's area each pair's beams cover: beams x footprint / area."""
    return beams * footprint_km2 / cell_area_km2


def _main_first_layer_pairs(
    cell: npt.NDArray[np.int64],
    first_beams: npt.NDArray[np.float64],
    footprint_km2: npt.NDArray[np.float64],
) -> npt.NDArray[np.bool_]:
    """Return which pairs are their cell's main first-layer satellite: the most first-layer
    area in the cell (the lowest pair index on a tie), when it places a layer."""
    main = np.zeros(cell.size, dtype=bool)
    if cell.size == 0:
        return main
    order = np.lexsort((-(first_beams * footprint_km2), cell))
    sorted_cell = cell[order]
    main[order[np.r_[True, sorted_cell[1:] != sorted_cell[:-1]]]] = True
    return main & (first_beams > _SERVED_BEAMS_FLOOR)


def _initial_serving_set(
    pairs: _Pairs,
    footprint_km2: npt.NDArray[np.float64],
    cells: _DemandCells,
    first_beams: npt.NDArray[np.float64],
    rules: _DirectionalRules,
) -> npt.NDArray[np.bool_]:
    """Return which pairs serve their cell after stage 1 (rule D3).

    At the module's rule, a cell's first-layer satellites whose layer covers at least f_serve
    of its area; at the diagnostic's, its main first-layer satellite, or every first-layer
    satellite that places a layer.

    Args:
        pairs: The pairs in view.
        footprint_km2: Each pair's footprint.
        cells: The demand cells.
        first_beams: Each pair's first-layer beams.
        rules: The class's rules.

    Returns:
        Whether each pair serves its cell.
    """
    match rules.serving_rule:
        case _ServingRule.AT_SERVING_SHARE:
            share = _layer_share(first_beams, footprint_km2, cells.area_km2[pairs.cell])
            serving: npt.NDArray[np.bool_] = share >= rules.serving_share
            return serving
        case _ServingRule.MAIN_SATELLITE:
            return _main_first_layer_pairs(pairs.cell, first_beams, footprint_km2)
        case _ServingRule.ANY_SHARE:
            placing: npt.NDArray[np.bool_] = first_beams > _SERVED_BEAMS_FLOOR
            return placing


def _joins_serving_set(
    first_beams: npt.NDArray[np.float64],
    stacked_beams: npt.NDArray[np.float64],
    footprint_km2: npt.NDArray[np.float64],
    cell_area_km2: npt.NDArray[np.float64],
    rules: _DirectionalRules,
) -> npt.NDArray[np.bool_]:
    """Return which of a band's admitted pairs join their cell's serving set after its fill
    (rule D3): at the module's rule, when the pair's first-layer and stacked beams together
    cover at least f_serve of the cell; at the diagnostic's any-share rule, when it placed a
    stacked layer; at its main-satellite rule, never.

    Args:
        first_beams: The admitted pairs' first-layer beams.
        stacked_beams: Their stacked beams, just placed.
        footprint_km2: Their footprints.
        cell_area_km2: Their cells' areas.
        rules: The class's rules.

    Returns:
        Whether each admitted pair joins.
    """
    match rules.serving_rule:
        case _ServingRule.AT_SERVING_SHARE:
            share = _layer_share(first_beams + stacked_beams, footprint_km2, cell_area_km2)
            joins: npt.NDArray[np.bool_] = share >= rules.serving_share
            return joins
        case _ServingRule.MAIN_SATELLITE:
            return np.zeros(first_beams.size, dtype=bool)
        case _ServingRule.ANY_SHARE:
            placing: npt.NDArray[np.bool_] = stacked_beams > _SERVED_BEAMS_FLOOR
            return placing


@dataclass(frozen=True, eq=False)
class _ServingIndex:
    """The serving pairs grouped by cell, for the pairwise admission's lookups.

    Attributes:
        pairs: The serving pairs, ordered by cell (by pair index within a cell).
        counts: Each cell's number of serving pairs.
        starts: Where each cell's serving pairs start in ``pairs``.
    """

    pairs: npt.NDArray[np.int64]
    counts: npt.NDArray[np.int64]
    starts: npt.NDArray[np.int64]


def _serving_index(
    serving_pairs: npt.NDArray[np.int64], pair_cell: npt.NDArray[np.int64], n_cells: int
) -> _ServingIndex:
    """Return the serving pairs grouped by cell."""
    cell = pair_cell[serving_pairs]
    counts = np.bincount(cell, minlength=n_cells)
    return _ServingIndex(
        pairs=serving_pairs[np.argsort(cell, kind="stable")],
        counts=counts,
        starts=np.cumsum(counts) - counts,
    )


def _admitted(
    candidates: npt.NDArray[np.int64],
    pair_cell: npt.NDArray[np.int64],
    sector: npt.NDArray[np.int64],
    directions: _PairDirections,
    serving: _ServingIndex,
    cos_beamwidth: float,
) -> npt.NDArray[np.bool_]:
    """Return which of a band's candidates the pairwise rule admits (rule D4).

    The candidates come in the order (cell, footprint, satellite index). A candidate is
    admitted only if its satellite sits at least one terminal beamwidth from every satellite
    serving its cell in another sector, and from every candidate of its cell admitted earlier
    in the band in another sector; satellites in the same sector tile that sector's one layer,
    so they are exempt from each other. The angle is between the unit directions from the
    cell to the two satellites (closer than a beamwidth when its cosine exceeds the
    beamwidth's). The second test is sequential within a cell, so the candidates are taken
    rank by rank within their cells, every cell at once.

    Args:
        candidates: The band's candidates, in the order above.
        pair_cell: Every pair's cell.
        sector: Every pair's sector.
        directions: The pairs' directions.
        serving: The serving pairs, grouped by cell.
        cos_beamwidth: The cosine of the terminal's half-power beamwidth.

    Returns:
        Whether each candidate is admitted.
    """
    cand_cell = pair_cell[candidates]
    cand_sector = sector[candidates]
    cand_direction = directions.of(candidates)
    blocked = np.zeros(candidates.size, dtype=bool)
    per_candidate = serving.counts[cand_cell]
    total = int(per_candidate.sum())
    if total:
        row = np.repeat(np.arange(candidates.size), per_candidate)
        offset = np.arange(total) - np.repeat(
            np.cumsum(per_candidate) - per_candidate, per_candidate
        )
        server = serving.pairs[serving.starts[cand_cell[row]] + offset]
        close = np.einsum("ij,ij->i", directions.of(server), cand_direction[row]) > cos_beamwidth
        blocked[row[close & (sector[server] != cand_sector[row])]] = True
    alive = np.flatnonzero(~blocked)
    admitted = np.zeros(candidates.size, dtype=bool)
    if alive.size == 0:
        return admitted
    alive_cell = cand_cell[alive]
    opens_group = np.r_[True, alive_cell[1:] != alive_cell[:-1]]
    group_start = np.flatnonzero(opens_group)
    group = np.cumsum(opens_group) - 1
    rank = np.arange(alive.size) - group_start[group]
    kept = rank == 0
    top_rank = int(rank.max())
    if top_rank:
        by_rank = np.argsort(rank, kind="stable")
        rank_starts = np.searchsorted(rank[by_rank], np.arange(top_rank + 2))
        alive_direction = cand_direction[alive]
        alive_sector = cand_sector[alive]
        for at_rank in range(1, top_rank + 1):
            at = by_rank[rank_starts[at_rank] : rank_starts[at_rank + 1]]
            earlier = group_start[group[at]][:, None] + np.arange(at_rank)
            close_earlier = (
                np.einsum("ijk,ik->ij", alive_direction[earlier], alive_direction[at])
                > cos_beamwidth
            )
            other_sector = alive_sector[earlier] != alive_sector[at][:, None]
            kept[at] = ~np.any(kept[earlier] & other_sector & close_earlier, axis=1)
    admitted[alive[kept]] = True
    return admitted


@dataclass(frozen=True, eq=False)
class _StackedLayers:
    """Stage 2's result: the stacked layers (rule D4).

    Attributes:
        beams: Each pair's stacked beams as placed (rule D6 may later drop a cell's).
        serving: Whether each pair's satellite serves its cell at the end of stage 2.
    """

    beams: npt.NDArray[np.float64]
    serving: npt.NDArray[np.bool_]


def _stacked_layers(
    pairs: _Pairs,
    footprint_km2: npt.NDArray[np.float64],
    sector: npt.NDArray[np.int64],
    directions: _PairDirections,
    cells: _DemandCells,
    first: _FirstLayer,
    bands: _FootprintBands,
    rules: _DirectionalRules,
    passes: int,
) -> _StackedLayers:
    """Spend the satellites' remaining beams on extra layers, one per sky sector (rule D4).

    The same banded fill as stage 1, on the snapshot's band edges, over (cell, sector) keys,
    all keys at once: a key's area is its cell's area less the first layer's area from that
    sector's satellites; a pair's cap is one layer less its first-layer beams; the people cap
    and each satellite's remaining beams carry over from stage 1. Before each band's fill its
    candidates, the pairs that could place more than :data:`_SERVED_BEAMS_FLOOR` beams at the
    band's start (by their cap, their key's area, their satellite's beams and their cell's
    people cap left), are taken in the order (cell, footprint, satellite index) and admitted
    by the pairwise rule (:func:`_admitted`); only the admitted fill. After the fill, an
    admitted pair joins its cell's serving set by the serving rule (rule D3).

    Args:
        pairs: The pairs in view.
        footprint_km2: Each pair's footprint.
        sector: Each pair's sky sector.
        directions: The pairs' directions.
        cells: The demand cells.
        first: Stage 1's layer and what it left.
        bands: The snapshot's footprint bands.
        rules: The class's rules.
        passes: The proportional passes.

    Returns:
        The stacked beams and the final serving set.
    """
    n_sectors = rules.layout.count
    key_area_km2 = np.repeat(cells.area_km2, n_sectors) - np.bincount(
        pairs.cell * n_sectors + sector,
        weights=first.beams * footprint_km2,
        minlength=cells.count * n_sectors,
    )
    remaining = _Remaining(
        satellite_beams=first.remaining.satellite_beams.copy(),
        key_area_km2=np.maximum(key_area_km2, _NONE_LEFT),
        cell_beams=first.remaining.cell_beams.copy(),
    )
    stacked = np.zeros(footprint_km2.size)
    serving = _initial_serving_set(pairs, footprint_km2, cells, first.beams, rules)
    serving_pairs = np.flatnonzero(serving)
    serving_lookup = _serving_index(serving_pairs, pairs.cell, cells.count)
    cos_beamwidth = math.cos(rules.beamwidth_rad)
    for band in range(bands.count):
        members = bands.members(band)
        if members.size == 0:
            continue
        cell = pairs.cell[members]
        footprint = footprint_km2[members]
        cap = np.maximum(cells.area_km2[cell] / footprint - first.beams[members], _NONE_LEFT)
        could_place = np.minimum(
            np.minimum(cap, remaining.key_area_km2[cell * n_sectors + sector[members]] / footprint),
            np.minimum(
                remaining.satellite_beams[pairs.satellite[members]], remaining.cell_beams[cell]
            ),
        )
        candidates = members[could_place > _SERVED_BEAMS_FLOOR]
        if candidates.size == 0:
            continue
        candidates = candidates[
            np.lexsort(
                (pairs.satellite[candidates], footprint_km2[candidates], pairs.cell[candidates])
            )
        ]
        chosen = np.sort(
            candidates[
                _admitted(candidates, pairs.cell, sector, directions, serving_lookup, cos_beamwidth)
            ]
        )
        if chosen.size == 0:
            continue
        chosen_cell = pairs.cell[chosen]
        chosen_footprint = footprint_km2[chosen]
        placed = _fill_band(
            np.maximum(
                cells.area_km2[chosen_cell] / chosen_footprint - first.beams[chosen], _NONE_LEFT
            ),
            pairs.satellite[chosen],
            chosen_cell * n_sectors + sector[chosen],
            chosen_cell,
            chosen_footprint,
            remaining,
            passes,
        )
        stacked[chosen] = placed
        joins = chosen[
            _joins_serving_set(
                first.beams[chosen],
                placed,
                chosen_footprint,
                cells.area_km2[chosen_cell],
                rules,
            )
            & ~serving[chosen]
        ]
        if joins.size:
            serving[joins] = True
            serving_pairs = np.concatenate([serving_pairs, joins])
            serving_lookup = _serving_index(serving_pairs, pairs.cell, cells.count)
    return _StackedLayers(beams=stacked, serving=serving)


def _pattern_gain(
    cos_angle: npt.NDArray[np.float64], rules: _DirectionalRules
) -> npt.NDArray[np.float64]:
    """Return the terminal's gain relative to its peak at the given angles off its beam's axis:
    a Gaussian main lobe, 10^(max(-12 (theta / HPBW)^2, floor) / 10) (rule D5)."""
    theta = np.arccos(np.clip(cos_angle, *_COSINE_BOUNDS))
    gain_db = np.maximum(
        _GAUSSIAN_LOBE_DB_PER_BEAMWIDTH_SQUARED * (theta / rules.beamwidth_rad) ** 2,
        rules.pattern_floor_db,
    )
    gain: npt.NDArray[np.float64] = 10 ** (gain_db / _DECIBELS_PER_DECADE)
    return gain


@dataclass(frozen=True, eq=False)
class _Pricing:
    """The full-sum pricing of one snapshot's layers (rule D5).

    A sub-pair is a pair's first-layer part or its stacked part, priced when it places more
    than :data:`_SERVED_BEAMS_FLOOR` beams: every stacked sub-pair, and the first-layer
    sub-pairs of the cells that carry stacked beams (elsewhere every beam is a first-layer
    beam at the central SE).

    Attributes:
        pair: Each sub-pair's pair, the sub-pairs ordered by cell.
        is_first_layer: Whether it is a first-layer sub-pair.
        beams: Its beams.
        interference: Its full-sum interference over its own signal: the sum over the cell's
            other sub-pairs p it counts of p's share of the cell x the gain toward p.
        nearest_cosine: The cosine of the angle to the nearest served sub-pair of its cell in
            another sector (:data:`_NO_NEIGHBOUR_COSINE` when there is none).
        spectral_efficiency: Its SE, anchor x log2(1 + SINR), SINR = 1 / (1 / SINR_1 +
            interference), bps/Hz.
        stacked_capacity: Each cell's sum of beams x SE over its sub-pairs (beams x bps/Hz;
            zero for a cell without stacked beams).
        has_stack: Whether each cell carries stacked beams (more than the floor).
    """

    pair: npt.NDArray[np.int64]
    is_first_layer: npt.NDArray[np.bool_]
    beams: npt.NDArray[np.float64]
    interference: npt.NDArray[np.float64]
    nearest_cosine: npt.NDArray[np.float64]
    spectral_efficiency: npt.NDArray[np.float64]
    stacked_capacity: npt.NDArray[np.float64]
    has_stack: npt.NDArray[np.bool_]


def _price_layers(
    pairs: _Pairs,
    footprint_km2: npt.NDArray[np.float64],
    sector: npt.NDArray[np.int64],
    directions: _PairDirections,
    cells: _DemandCells,
    first_beams: npt.NDArray[np.float64],
    stacked_beams: npt.NDArray[np.float64],
    rules: _DirectionalRules,
) -> _Pricing:
    """Price every served sub-pair of the cells that carry stacked beams by the full sum (D5).

    For each sub-pair q, SINR_q = 1 / (1 / SINR_1 + the sum over the cell's other sub-pairs p
    of f_p x g(theta_pq)), f_p the share of the cell p covers and g the victim terminal's gain
    toward p's satellite (:func:`_pattern_gain`). First-layer sub-pairs do not count against
    each other (they tile the cell as one layer), nor do sub-pairs in the same sector (they
    tile the sector's layer). SE_q = anchor x log2(1 + SINR_q). The ordered pairs of each cell's
    sub-pairs are expanded :data:`_FULL_SUM_BATCH_PAIRS` at most at a time, whole cells.

    Args:
        pairs: The pairs in view.
        footprint_km2: Each pair's footprint.
        sector: Each pair's sky sector.
        directions: The pairs' directions.
        cells: The demand cells.
        first_beams: Each pair's first-layer beams.
        stacked_beams: Each pair's stacked beams.
        rules: The class's rules.

    Returns:
        The pricing.
    """
    has_stack = (
        np.bincount(pairs.cell, weights=stacked_beams, minlength=cells.count) > _SERVED_BEAMS_FLOOR
    )
    first_part = np.flatnonzero((first_beams > _SERVED_BEAMS_FLOOR) & has_stack[pairs.cell])
    stacked_part = np.flatnonzero(stacked_beams > _SERVED_BEAMS_FLOOR)
    pair = np.concatenate([first_part, stacked_part])
    is_first = np.concatenate(
        [np.ones(first_part.size, dtype=bool), np.zeros(stacked_part.size, dtype=bool)]
    )
    beams = np.concatenate([first_beams[first_part], stacked_beams[stacked_part]])
    by_cell = np.argsort(pairs.cell[pair], kind="stable")
    pair, is_first, beams = pair[by_cell], is_first[by_cell], beams[by_cell]
    cell = pairs.cell[pair]
    share = _layer_share(beams, footprint_km2[pair], cells.area_km2[cell])
    sub_sector = sector[pair]
    direction = directions.of(pair)
    interference = np.zeros(pair.size)
    nearest_cosine = np.full(pair.size, _NO_NEIGHBOUR_COSINE)
    if pair.size:
        opens = np.flatnonzero(np.r_[True, cell[1:] != cell[:-1]])
        sizes = np.diff(np.r_[opens, pair.size])
        expanded = np.cumsum(sizes.astype(np.int64) ** 2)
        first_cell = 0
        while first_cell < sizes.size:
            before = expanded[first_cell - 1] if first_cell else 0
            last_cell = max(
                first_cell + 1,
                int(np.searchsorted(expanded, before + _FULL_SUM_BATCH_PAIRS, side="right")),
            )
            low = int(opens[first_cell])
            high = int(opens[last_cell]) if last_cell < sizes.size else pair.size
            batch_sizes = sizes[first_cell:last_cell]
            run = np.repeat(batch_sizes, batch_sizes)
            u = np.repeat(np.arange(low, high), run)
            run_start = np.repeat(np.repeat(opens[first_cell:last_cell], batch_sizes), run)
            segment = np.cumsum(run) - run
            v = run_start + np.arange(u.size) - np.repeat(segment, run)
            counted = (u != v) & (sub_sector[u] != sub_sector[v]) & ~(is_first[u] & is_first[v])
            cosine = np.einsum("ij,ij->i", direction[u], direction[v])
            contribution = np.where(counted, share[v] * _pattern_gain(cosine, rules), 0.0)
            interference[low:high] = np.add.reduceat(contribution, segment)
            nearest_cosine[low:high] = np.maximum.reduceat(
                np.where(counted, cosine, _NO_NEIGHBOUR_COSINE), segment
            )
            first_cell = last_cell
    spectral_efficiency = rules.se_anchor_bps_per_hz * np.log2(
        1 + 1 / (1 / rules.single_layer_sinr + interference)
    )
    return _Pricing(
        pair=pair,
        is_first_layer=is_first,
        beams=beams,
        interference=interference,
        nearest_cosine=nearest_cosine,
        spectral_efficiency=spectral_efficiency,
        stacked_capacity=np.bincount(
            cell, weights=beams * spectral_efficiency, minlength=cells.count
        ),
        has_stack=has_stack,
    )


@dataclass(frozen=True, eq=False)
class _StackStatistics:
    """The kept stacked layers' statistics in one snapshot (the curve's directional diagnostics).

    A kept stacked layer here is a stacked sub-pair of a cell that keeps its stack and that its
    first layer covers, sitting on a layer of another sector in its cell. In a covered cell
    every stage-2 beam overlaps another sector's first layer, so it stacks; in a cell its first
    layer leaves short, stage 2 may complete that first layer instead, which the fluid
    allocation cannot tell from stacking, so those beams count in L, not here. A stacked
    sub-pair that shares its sector with every other layer of its cell completes that sector's
    one layer (rule D5 prices it so) and counts in L, not here.

    Attributes:
        beams: The kept stacked layers' beams.
        median_separation_deg: Their beam-weighted median separation from their cell's nearest
            layer of another sector, degrees; None when there are none.
        mean_interference_db: Their beam-weighted mean full-sum interference, dB; None when
            there are none.
    """

    beams: float
    median_separation_deg: float | None
    mean_interference_db: float | None


def _stack_statistics(
    pricing: _Pricing,
    keeps_stack: npt.NDArray[np.bool_],
    first_layer_covers: npt.NDArray[np.bool_],
    pair_cell: npt.NDArray[np.int64],
) -> _StackStatistics:
    """Return the kept stacked layers' beams, median separation and mean interference.

    Args:
        pricing: The full-sum pricing (rule D5).
        keeps_stack: Whether each cell keeps its stacked beams (rule D6).
        first_layer_covers: Whether each cell's first layer covers it
            (:data:`_COVERED_SHORTFALL_SHARE`).
        pair_cell: Every pair's cell.

    Returns:
        The statistics of the stacked sub-pairs :class:`_StackStatistics` counts.
    """
    cell = pair_cell[pricing.pair]
    kept = (
        ~pricing.is_first_layer
        & keeps_stack[cell]
        & first_layer_covers[cell]
        & (pricing.nearest_cosine > _NO_NEIGHBOUR_COSINE)
    )
    weight = pricing.beams[kept]
    total = float(weight.sum())
    if total <= _NONE_LEFT:
        return _StackStatistics(beams=0.0, median_separation_deg=None, mean_interference_db=None)
    separation = np.degrees(np.arccos(np.clip(pricing.nearest_cosine[kept], *_COSINE_BOUNDS)))
    order = np.argsort(separation)
    cumulative = np.cumsum(weight[order]) / total
    median = float(separation[order][np.searchsorted(cumulative, _MEDIAN_WEIGHT_SHARE)])
    mean_interference = float(np.sum(weight * pricing.interference[kept]) / total)
    return _StackStatistics(
        beams=total,
        median_separation_deg=median,
        mean_interference_db=_DECIBELS_PER_DECADE * math.log10(mean_interference),
    )


@dataclass(frozen=True, eq=False)
class _DirectionalAllocation:
    """The directional part of one snapshot's allocation (rules D1 to D6), d = 1.

    Attributes:
        sector: Each pair's sky sector (D1).
        first_layer_beams: Each pair's first-layer beams (D2).
        stacked_beams: Each pair's stacked beams as placed, kept or dropped (D4); a dropped
            cell's stay spent from their satellites.
        serving: Whether each pair's satellite serves its cell at the end of stage 2 (D3).
        keeps_stack: Whether each cell keeps its stacked beams (D6).
        stacked_capacity_mbps: Each cell's capacity with its stacked layers, by the full sum
            (D5); its first layer alone where it carries none.
        cell_capacity_mbps: Each cell's capacity as kept (D6).
        useful_beams: L: every first-layer beam and the kept stacked beams.
        capacity_mbps: The cells' capacity as kept.
        statistics: The kept stacked layers' beams, separation and interference.
    """

    sector: npt.NDArray[np.int64]
    first_layer_beams: npt.NDArray[np.float64]
    stacked_beams: npt.NDArray[np.float64]
    serving: npt.NDArray[np.bool_]
    keeps_stack: npt.NDArray[np.bool_]
    stacked_capacity_mbps: npt.NDArray[np.float64]
    cell_capacity_mbps: npt.NDArray[np.float64]
    useful_beams: float
    capacity_mbps: float
    statistics: _StackStatistics


def _directional_allocation(
    satellites: _SatellitePositions,
    pairs: _Pairs,
    footprint_km2: npt.NDArray[np.float64],
    cells: _DemandCells,
    first: _FirstLayer,
    bands: _FootprintBands,
    orbit_radius_km: float,
    spectrum_mhz: float,
    rules: _DirectionalRules,
    passes: int,
) -> _DirectionalAllocation:
    """Allocate a directional class's stacked layers on its first layer and price the cells.

    Rules D1 (the sectors), D3 and D4 (stage 2 under the pairwise admission), D5 (the full-sum
    pricing) and D6, the keep rule: a cell whose priced capacity with its stacked layers is
    below its first layer alone (every first-layer beam at the central SE) keeps its first
    layer only. Its dropped stacked beams stay spent, never returned or re-spent (nothing is
    filled after the keep rule), and L counts only kept beams, so L can fall while capacity
    rises. A beam carries the spectrum times its SE.

    Args:
        satellites: The satellites.
        pairs: The pairs in view.
        footprint_km2: Each pair's footprint.
        cells: The demand cells.
        first: Stage 1's layer at the class's people cap (D2) and what it left.
        bands: The snapshot's footprint bands.
        orbit_radius_km: The shell's orbit radius, km.
        spectrum_mhz: The held spectrum, MHz.
        rules: The class's rules.
        passes: The proportional passes.

    Returns:
        The directional allocation.
    """
    sector = _pair_sectors(pairs, satellites, cells, orbit_radius_km, rules.layout)
    directions = _pair_directions(pairs, satellites, cells, orbit_radius_km)
    stacked = _stacked_layers(
        pairs, footprint_km2, sector, directions, cells, first, bands, rules, passes
    )
    pricing = _price_layers(
        pairs, footprint_km2, sector, directions, cells, first.beams, stacked.beams, rules
    )
    first_alone = (
        np.bincount(pairs.cell, weights=first.beams, minlength=cells.count)
        * rules.se_central_bps_per_hz
    )
    keeps_stack = pricing.has_stack & (pricing.stacked_capacity >= first_alone)
    stacked_capacity = np.where(pricing.has_stack, pricing.stacked_capacity, first_alone)
    cell_capacity = np.where(keeps_stack, pricing.stacked_capacity, first_alone)
    cell_capacity_mbps = cell_capacity * spectrum_mhz
    first_layer_covers = first.remaining.key_area_km2 <= _COVERED_SHORTFALL_SHARE * cells.area_km2
    return _DirectionalAllocation(
        sector=sector,
        first_layer_beams=first.beams,
        stacked_beams=stacked.beams,
        serving=stacked.serving,
        keeps_stack=keeps_stack,
        stacked_capacity_mbps=stacked_capacity * spectrum_mhz,
        cell_capacity_mbps=cell_capacity_mbps,
        useful_beams=first.useful_beams + float(stacked.beams[keeps_stack[pairs.cell]].sum()),
        capacity_mbps=float(cell_capacity_mbps.sum()),
        statistics=_stack_statistics(pricing, keeps_stack, first_layer_covers, pairs.cell),
    )


# ===========================================================================
# Stage 12: the interference trim (the phone class's central curve)
# ===========================================================================


def _broadside_directivity(shell: ShellInputs) -> float:
    """Return G0, the panel's broadside directivity, linear: 4 pi x area / wavelength^2.

    Standard antenna theory for an aperture of that area; 39.6 dBi at the 25 m^2 reference
    panel and 1.621 GHz.
    """
    wavelength_m = _SPEED_OF_LIGHT_M_S / shell.carrier_hz
    return _SPHERE_SOLID_ANGLE_SR * shell.reference_aperture_m2 / wavelength_m**2


def _interference_trim(
    satellites: _SatellitePositions,
    allocation: _Allocation,
    cells: _DemandCells,
    shell: ShellInputs,
    trim: TrimInputs,
) -> tuple[float, ...]:
    """Return one snapshot's interference trim at each far-sidelobe floor (stage 12).

    The share of capacity the aggregate far-sidelobe leak of the lit beams costs a served
    cell, on the phone allocation's own lit-beam map. Power control gives every beam equal
    flux at its target, so a beam's power goes as r^2 / g(eta), r its slant range and g(eta) =
    cos^n of its scan angle (n the scan exponent); a satellite's power W_s is the sum over its
    beams. A pair above the mask is scanned less than 90 degrees, so its scan cosine is
    positive (at least about 0.53 on the central shell). Victims: served cells (more than
    :data:`_SERVED_BEAMS_FLOOR` beams) drawn without replacement in proportion to their beams,
    from a fresh ``default_rng(seed)``, so a row does not depend on the order of the fleets. A
    victim's aggregate over its own signal is x = gamma / G0 x the sum, over every lit
    satellite above the victim's horizon, of W_s x g(eta toward the victim) / r^2, G0 the
    panel's broadside directivity and gamma a floor's average far-sidelobe gain. The extra
    aggregate lowers the operating SINR of 1 to 1 / (1 + x), so a victim keeps log2(1 + 1 /
    (1 + x)) of its capacity; the trim is one less the victims' mean of that.

    Args:
        satellites: The snapshot's satellites.
        allocation: The phone class's allocation of that snapshot (its pairs and beams).
        cells: The demand cells.
        shell: The shell and the beam (the orbit, the carrier and the reference panel).
        trim: The victims, the seed, the floors and the scan exponent.

    Returns:
        The trim at each of ``trim.floors_dbi``, a fraction, in their order.

    Raises:
        SaturationInvariantError: If the snapshot serves no cell, so no victim can be drawn.
    """
    orbit_radius_km = _EARTH_RADIUS_KM + shell.altitude_km
    satellite_unit = _unit_vectors(satellites.lat_rad, satellites.lon_rad)
    satellite_km = orbit_radius_km * satellite_unit
    to_cell_km = _EARTH_RADIUS_KM * cells.xyz[allocation.cell] - satellite_km[allocation.satellite]
    slant_km = np.linalg.norm(to_cell_km, axis=1)
    scan_cosine = (
        np.einsum("ij,ij->i", -satellite_unit[allocation.satellite], to_cell_km) / slant_km
    )
    power = np.bincount(
        allocation.satellite,
        weights=allocation.beams * slant_km**2 / scan_cosine**trim.scan_exponent,
        minlength=satellites.count,
    )
    served = np.bincount(allocation.cell, weights=allocation.beams, minlength=cells.count)
    candidates = np.flatnonzero(served > _SERVED_BEAMS_FLOOR)
    if candidates.size == 0:
        raise SaturationInvariantError(
            f"the interference trim at {satellites.count} satellites: the snapshot serves no "
            "cell, so no victim can be drawn"
        )
    weight = served[candidates]
    victims = np.random.default_rng(trim.seed).choice(
        candidates,
        size=min(trim.victims, candidates.size),
        replace=False,
        p=weight / weight.sum(),
    )
    victim_unit = cells.xyz[victims]
    victim_km = _EARTH_RADIUS_KM * victim_unit
    lit = np.flatnonzero(power > _NONE_LEFT)
    per_chunk = max(_MIN_CHUNK_SATELLITES, _TRIM_CHUNK_ELEMENTS // victims.size)
    aggregate = np.zeros(victims.size)
    for start in range(0, lit.size, per_chunk):
        chunk = lit[start : start + per_chunk]
        offset_km = satellite_km[chunk][None, :, :] - victim_km[:, None, :]
        distance_km = np.linalg.norm(offset_km, axis=2)
        above = (
            np.einsum("vsj,vj->vs", offset_km, victim_unit) / distance_km > _HORIZON_ELEVATION_SINE
        )
        toward_cosine = np.einsum("vsj,sj->vs", offset_km, satellite_unit[chunk]) / distance_km
        gain = np.clip(toward_cosine, *_COSINE_UNIT_BOUNDS) ** trim.scan_exponent
        aggregate += np.sum(above * (power[chunk][None, :] * gain / distance_km**2), axis=1)
    directivity = _broadside_directivity(shell)
    trims = []
    for floor_dbi in trim.floors_dbi:
        extra = 10 ** (floor_dbi / _DECIBELS_PER_DECADE) / directivity * aggregate
        kept = np.log2(1 + _OPERATING_SINR / (1 + _OPERATING_SINR * extra)) / math.log2(
            1 + _OPERATING_SINR
        )
        trims.append(float(_FULL_SCALE - np.mean(kept)))
    return tuple(trims)


# ===========================================================================
# The sweep, in separate processes under the memory budget
# ===========================================================================


@dataclass(frozen=True)
class _SnapshotTask:
    """One curve (a class's, or a band point's) at one fleet at one snapshot time.

    Attributes:
        curve: The class or the band point.
        fleet_index: The fleet's position in the curve's sweep.
        requested_fleet: The requested fleet N.
        snapshot_index: The snapshot's position in the draw.
        time_s: The snapshot time, s.
        prices_trim: Whether the task also prices the interference trim (the phone class's
            central curve, on the first snapshots of the draw).
    """

    curve: _CurveKey
    fleet_index: int
    requested_fleet: int
    snapshot_index: int
    time_s: float
    prices_trim: bool


@dataclass(frozen=True, eq=False)
class _SweepContext:
    """What one curve's snapshot tasks need: the shell, the curve's demand cells and limits, and
    the interference trim's settings.

    Each task is sent its own curve's context only, so a band point with its own demand cells
    adds nothing to the other curves' tasks.
    """

    shell: ShellInputs
    cells: _DemandCells
    limits: _AllocationLimits
    trim: TrimInputs


@dataclass(frozen=True)
class _SnapshotResult:
    """One snapshot task's result, with the measure of the worker that ran it.

    Attributes:
        task: The task.
        realized_fleet: The realized fleet, P x S.
        useful_beams: L.
        capacity_mbps: The capacity, d = 1.
        ceiling_beams: The ceiling (the sector-rule ceiling for a directional class).
        supply_beams: The supply.
        statistics: A directional class's kept stacked layers; None for the phone class.
        trims: The interference trim at each floor, when the task prices it; None otherwise.
        worker_pid: The worker's process id.
        worker_peak_mb: The worker's peak resident memory so far, MB.
    """

    task: _SnapshotTask
    realized_fleet: int
    useful_beams: float
    capacity_mbps: float
    ceiling_beams: float
    supply_beams: float
    statistics: _StackStatistics | None
    trims: tuple[float, ...] | None
    worker_pid: int
    worker_peak_mb: float


def _own_peak_mb() -> float:
    """Return this process's peak resident memory so far, MB (``ru_maxrss``, by platform)."""
    unit_bytes = (
        _RU_MAXRSS_UNIT_BYTES_MACOS if sys.platform == "darwin" else _RU_MAXRSS_UNIT_BYTES_OTHER
    )
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * unit_bytes / _BYTES_PER_MB


def _run_snapshot(task: _SnapshotTask, context: _SweepContext) -> _SnapshotResult:
    """Run one curve at one fleet at one snapshot time (a worker's task), pricing the
    interference trim on its allocation when the task asks."""
    satellites = _walker_positions(context.shell, task.requested_fleet, task.time_s)
    allocation = _allocate(satellites, context.cells, context.limits)
    trims = (
        _interference_trim(satellites, allocation, context.cells, context.shell, context.trim)
        if task.prices_trim
        else None
    )
    return _SnapshotResult(
        task=task,
        realized_fleet=satellites.count,
        useful_beams=allocation.useful_beams,
        capacity_mbps=allocation.capacity_mbps,
        ceiling_beams=allocation.ceiling_beams,
        supply_beams=allocation.supply_beams,
        statistics=None if allocation.directional is None else allocation.directional.statistics,
        trims=trims,
        worker_pid=os.getpid(),
        worker_peak_mb=_own_peak_mb(),
    )


class _WorkerMemoryError(Exception):
    """A saturation worker's own MemoryError, raised again in the worker under this type: the
    process pool re-raises a worker's exception in the parent, where a bare MemoryError could be
    the parent's own."""


def _run_snapshot_in_worker(task: _SnapshotTask, context: _SweepContext) -> _SnapshotResult:
    """Run one snapshot task in a pool's worker: :func:`_run_snapshot`, with a MemoryError marked
    as the worker's own.

    Raises:
        _WorkerMemoryError: If the worker runs out of memory (its message kept).
    """
    try:
        return _run_snapshot(task, context)
    except MemoryError as exc:
        raise _WorkerMemoryError(str(exc) or type(exc).__name__) from exc


def _cause_summary(exc: BaseException) -> str | None:
    """Return the last line of an exception's cause (the error itself: a process pool's cause is a
    formatted traceback fenced in quote marks), or None when it has no cause."""
    if exc.__cause__ is None:
        return None
    lines = [line.strip() for line in str(exc.__cause__).splitlines()]
    stated = [line for line in lines if line.strip(_TRACEBACK_QUOTES)]
    return stated[-1] if stated else type(exc.__cause__).__name__


@dataclass(frozen=True)
class _SweepRun:
    """A sweep's results with what its workers measured.

    Attributes:
        results: Every task's result, in the tasks' order.
        workers: The most workers any tier ran at once.
        workers_peak_mb: The largest summed peak of a set of workers alive at once, MB (the
            tiers run one after another, so the largest of their bounds).
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


def _memory_binds(task_peak_mb: float) -> bool:
    """Return whether the budget, not the CPUs, limits the workers at this worker peak."""
    cpus = os.process_cpu_count() or _MIN_WORKERS
    return math.floor((_MEMORY_BUDGET_MB - _own_peak_mb()) / task_peak_mb) < cpus


def _sector_count(limits: _AllocationLimits) -> int:
    """Return a curve's sky sectors (none for the phone class and its band points): the sweep
    measures the curves in this order, the lightest first, since stage 2's keys grow with it."""
    return 0 if limits.directional is None else limits.directional.layout.count


def _run_pool(
    indices: Sequence[int],
    tasks: Sequence[_SnapshotTask],
    contexts: Mapping[_CurveKey, _SweepContext],
    task_peak_mb: float,
    results: dict[int, _SnapshotResult],
) -> tuple[int, float]:
    """Run the tasks at ``indices`` in a fresh pool sized to ``task_peak_mb``; store their results.

    Each task is sent with its own curve's context.

    Returns:
        The pool's worker count and the summed peaks of its workers, MB (they are alive at
        once; a process's peak only grows, so each worker's last report is its peak).
    """
    workers = _worker_count(task_peak_mb, len(indices))
    worker_peaks: dict[int, float] = {}
    with ProcessPoolExecutor(max_workers=workers, mp_context=get_context("spawn")) as pool:
        for index, result in zip(
            indices,
            pool.map(
                _run_snapshot_in_worker,
                [tasks[i] for i in indices],
                [contexts[tasks[i].curve] for i in indices],
            ),
            strict=True,
        ):
            results[index] = result
            worker_peaks[result.worker_pid] = max(
                worker_peaks.get(result.worker_pid, result.worker_peak_mb),
                result.worker_peak_mb,
            )
    return workers, sum(worker_peaks.values())


def _run_alone(
    indices: Sequence[int],
    tasks: Sequence[_SnapshotTask],
    contexts: Mapping[_CurveKey, _SweepContext],
    results: dict[int, _SnapshotResult],
) -> None:
    """Run the tasks at ``indices`` one after another in one fresh process; store their results.

    The process's peak only grows, so each result's worker peak bounds its own task's.
    """
    with ProcessPoolExecutor(max_workers=_MIN_WORKERS, mp_context=get_context("spawn")) as alone:
        for index in indices:
            task = tasks[index]
            results[index] = alone.submit(
                _run_snapshot_in_worker, task, contexts[task.curve]
            ).result()


def _run_sweep(
    tasks: Sequence[_SnapshotTask], contexts: Mapping[_CurveKey, _SweepContext]
) -> _SweepRun:
    """Run every task in separate processes, the largest tasks first and measured.

    A worker's peak grows about linearly with the fleet and differs by curve. Each curve's
    largest task runs first, the lightest curve's first, one after another in one fresh
    process, so each one's reading bounds every other task of its curve. When the budget does
    not limit the workers at the largest reading, every other task then runs in one pool
    under it. Otherwise each curve runs from its largest fleet down in tiers: a tier holds the
    tasks whose requested fleet exceeds its largest over :data:`_SWEEP_TIER_FLEET_RATIO` and
    runs under its largest's reading, each lower tier's largest task running alone first in a
    fresh process, until the budget no longer limits the workers and the rest of the curve
    runs in one pool. Every pool is fresh, a pool's workers are alive at once so their peaks
    sum, and the pools run one after another. The curves keep the order their tasks first
    appear in.

    The sweep's failures are its own error, each naming the sweep's task count: a worker that
    dies (the pool breaks with no cause; most likely the system killed it out of memory), a
    worker that runs out of memory (its MemoryError, which the worker marks as its own), and a
    pool that breaks with a stated cause (sending a task or receiving a result failed in this
    process), whose cause the message names without blaming a worker. A MemoryError of this
    process is not a worker's and is left as it is.

    Raises:
        SaturationSweepError: If a worker dies or runs out of memory, or the pool breaks with a
            cause (the command logs it as its one ERROR line).
    """
    results: dict[int, _SnapshotResult] = {}
    by_curve: dict[_CurveKey, list[int]] = {}
    for index, task in enumerate(tasks):
        by_curve.setdefault(task.curve, []).append(index)
    for order in by_curve.values():
        order.sort(key=lambda i: (-tasks[i].requested_fleet, i))
    tops = [
        order[0]
        for _, order in sorted(
            by_curve.items(), key=lambda item: _sector_count(contexts[item[0]].limits)
        )
    ]
    widest = _MIN_WORKERS
    try:
        _run_alone(tops, tasks, contexts, results)
        bounds = {curve: results[order[0]].worker_peak_mb for curve, order in by_curve.items()}
        peak_bound_mb = max(bounds.values(), default=0.0)
        rest = [i for order in by_curve.values() for i in order[1:]]
        if rest and not _memory_binds(peak_bound_mb):
            widest, pool_peak_mb = _run_pool(rest, tasks, contexts, peak_bound_mb, results)
            peak_bound_mb = max(peak_bound_mb, pool_peak_mb)
        elif rest:
            for curve, order in by_curve.items():
                bound_mb = bounds[curve]
                floor_fleet = tasks[order[0]].requested_fleet / _SWEEP_TIER_FLEET_RATIO
                pending = order[1:]
                while pending:
                    if _memory_binds(bound_mb):
                        tier = [i for i in pending if tasks[i].requested_fleet > floor_fleet]
                        pending = [i for i in pending if tasks[i].requested_fleet <= floor_fleet]
                    else:
                        tier, pending = pending, []
                    if tier:
                        workers, pool_peak_mb = _run_pool(tier, tasks, contexts, bound_mb, results)
                        widest = max(widest, workers)
                        peak_bound_mb = max(peak_bound_mb, pool_peak_mb)
                    if pending:
                        top, pending = pending[0], pending[1:]
                        _run_alone([top], tasks, contexts, results)
                        bound_mb = results[top].worker_peak_mb
                        peak_bound_mb = max(peak_bound_mb, bound_mb)
                        floor_fleet = tasks[top].requested_fleet / _SWEEP_TIER_FLEET_RATIO
    except BrokenProcessPool as exc:
        cause = _cause_summary(exc)
        failure = (
            f"a saturation worker died during a sweep of {len(tasks):,} snapshot tasks, most "
            "likely out of memory"
            if cause is None
            else f"the saturation sweep's process pool broke during a sweep of {len(tasks):,} "
            f"snapshot tasks ({cause})"
        )
        raise SaturationSweepError(f"{failure}; nothing was written", len(tasks)) from exc
    except _WorkerMemoryError as exc:
        raise SaturationSweepError(
            f"a saturation worker ran out of memory during a sweep of {len(tasks):,} snapshot "
            f"tasks ({exc}); nothing was written",
            len(tasks),
        ) from exc
    return _SweepRun(
        results=tuple(results[i] for i in range(len(tasks))),
        workers=widest,
        workers_peak_mb=peak_bound_mb,
    )


# ===========================================================================
# Stages 8, 9 and 11: the rows, the checks and the markers
# ===========================================================================


@dataclass(frozen=True)
class _FleetSnapshots:
    """One class's fleet's snapshots, in the draw's order.

    Attributes:
        fleet: The realized fleet, P x S.
        useful_beams: L at each snapshot.
        ceiling_beams: The ceiling at each.
        supply_beams: The supply at each.
        capacity_mbps: The capacity at each, d = 1.
        statistics: A directional class's kept stacked layers at each; empty for the phone
            class.
        trims: The interference trim at each floor, at each snapshot that priced it (the
            phone class's central curve); empty otherwise.
    """

    fleet: int
    useful_beams: tuple[float, ...]
    ceiling_beams: tuple[float, ...]
    supply_beams: tuple[float, ...]
    capacity_mbps: tuple[float, ...]
    statistics: tuple[_StackStatistics, ...]
    trims: tuple[tuple[float, ...], ...] = ()


def _by_fleet(results: Sequence[_SnapshotResult], n_fleets: int) -> tuple[_FleetSnapshots, ...]:
    """Group one class's snapshot results by fleet, each fleet's snapshots in the draw's order."""
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
                capacity_mbps=tuple(result.capacity_mbps for result in snapshots),
                statistics=tuple(
                    result.statistics for result in snapshots if result.statistics is not None
                ),
                trims=tuple(result.trims for result in snapshots if result.trims is not None),
            )
        )
    return tuple(fleets)


def _exceeds(value: float, bound: float, relative_tolerance: float) -> bool:
    """Return whether ``value`` lies above ``bound`` by more than the relative tolerance."""
    return value > bound and not math.isclose(value, bound, rel_tol=relative_tolerance)


def _curve_label(curve: _CurveKey) -> str:
    """Return a curve's name in messages and limits: its class's key, or for a band point the
    phone class's key and the point's name."""
    if isinstance(curve, BandName):
        return f"{DeviceClass.PHONE_CLASS.value} band point {curve.value}"
    return curve.value


def _check_bounds(curve: _CurveKey, fleets: Sequence[_FleetSnapshots], maximum_use: float) -> None:
    """Refuse a snapshot whose L exceeds min(ceiling, supply) or whose ceiling exceeds maximum use.

    Raises:
        SaturationInvariantError: Naming the curve, the fleet, the snapshot and the values.
    """
    name = _curve_label(curve)
    for fleet in fleets:
        for snapshot, (useful, ceiling, supply) in enumerate(
            zip(fleet.useful_beams, fleet.ceiling_beams, fleet.supply_beams, strict=True)
        ):
            if _exceeds(useful, min(ceiling, supply), _BOUNDS_RELATIVE_TOLERANCE):
                raise SaturationInvariantError(
                    f"{name} at {fleet.fleet} satellites, snapshot {snapshot}: "
                    f"useful beams {useful} exceed min(ceiling {ceiling}, supply {supply})"
                )
            if _exceeds(ceiling, maximum_use, _BOUNDS_RELATIVE_TOLERANCE):
                raise SaturationInvariantError(
                    f"{name} at {fleet.fleet} satellites, snapshot {snapshot}: "
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


def _directional_diagnostics(fleet: _FleetSnapshots) -> DirectionalDiagnostics:
    """Return a directional row's stacking diagnostics, from its snapshots.

    The kept stacked share is the snapshot mean of each snapshot's kept stacked layers over
    its L; the median separation and the mean full-sum interference are the means over the
    snapshots that keep stacked layers, None when none does.
    """
    shares = [
        statistics.beams / useful if useful > _NONE_LEFT else _NONE_LEFT
        for statistics, useful in zip(fleet.statistics, fleet.useful_beams, strict=True)
    ]
    separations = [
        statistics.median_separation_deg
        for statistics in fleet.statistics
        if statistics.median_separation_deg is not None
    ]
    interference = [
        statistics.mean_interference_db
        for statistics in fleet.statistics
        if statistics.mean_interference_db is not None
    ]
    return DirectionalDiagnostics(
        kept_stacked_share=float(np.mean(shares)),
        median_separation_deg=float(np.mean(separations)) if separations else None,
        mean_full_sum_interference_db=float(np.mean(interference)) if interference else None,
    )


def _row_trim(fleet: _FleetSnapshots, floors_dbi: Sequence[float]) -> tuple[TrimAtFloor, ...]:
    """Return a row's interference trim at each floor: the mean over the snapshots that priced it.

    Raises:
        SaturationInvariantError: If no snapshot of the row priced the trim.
    """
    if not fleet.trims:
        raise SaturationInvariantError(
            f"the interference trim at {fleet.fleet} satellites: no snapshot priced it"
        )
    means = np.mean(np.array(fleet.trims), axis=0)
    return tuple(
        TrimAtFloor(floor_dbi=floor_dbi, trim=float(mean))
        for floor_dbi, mean in zip(floors_dbi, means, strict=True)
    )


def _class_rows(
    fleets: Sequence[_FleetSnapshots],
    requested_fleets: Sequence[int],
    *,
    beams_per_satellite: float,
    directional: bool,
    trim_floors_dbi: Sequence[float] | None,
) -> tuple[CurveRow, ...]:
    """Return a class's rows: the snapshot means, the spread of L, U, the bounds and, for a
    directional class, its stacking diagnostics; for the phone class's central curve, the
    interference trim at each floor.

    Each row carries the request its shell was built from (the sweep's fleet, in the order
    the tasks were made), so a reader can rebuild it. Each snapshot's capacity is its own (a
    phone beam carries the spectrum times the class's central SE; a directional cell, its
    kept layers by the full sum), and the row's is their mean (Gbps).
    """
    rows = []
    for fleet, requested_fleet in zip(fleets, requested_fleets, strict=True):
        useful = np.array(fleet.useful_beams)
        capacity_gbps = np.array(fleet.capacity_mbps) / GBPS_TO_MBPS
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
                directional=_directional_diagnostics(fleet) if directional else None,
                trim=None if trim_floors_dbi is None else _row_trim(fleet, trim_floors_dbi),
            )
        )
    return tuple(rows)


def _check_capacity_per_satellite(curve: _CurveKey, rows: Sequence[CurveRow]) -> None:
    """Refuse a curve whose capacity per satellite rises between consecutive rows.

    A rise of up to :data:`_CAPACITY_PER_SATELLITE_RISE_TOLERANCE` of the earlier row's value
    is the snapshots' noise and passes; a larger one means an allocation that under-fills a
    row (which the stall floor, from 20,000 satellites up, cannot see).

    Raises:
        SaturationInvariantError: Naming the curve, the two fleets and the two values.
    """
    for earlier, later in pairwise(rows):
        before = earlier.capacity_gbps / earlier.fleet
        after = later.capacity_gbps / later.fleet
        if after - before > _CAPACITY_PER_SATELLITE_RISE_TOLERANCE * before:
            raise SaturationInvariantError(
                f"{_curve_label(curve)}: capacity per satellite rises from {before} Gbps at "
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
    fleets: Sequence[int], useful_beams: Sequence[float], target: float
) -> float | None:
    """Return the fleet at which L first reaches the target (log-log between rows), or None.

    The caller handles a target the first row already reaches (:func:`_reached_at_first_row`).
    """
    for (low_fleet, low_beams), (high_fleet, high_beams) in pairwise(
        zip(fleets, useful_beams, strict=True)
    ):
        if low_beams < target <= high_beams:
            share = math.log(target / low_beams) / math.log(high_beams / low_beams)
            return math.exp(math.log(low_fleet) + share * math.log(high_fleet / low_fleet))
    return None


def _elasticity(curve: _CurveKey, rows: Sequence[CurveRow]) -> tuple[list[float], list[float]]:
    """Return the rows' interval midpoints and the elasticity of capacity at each.

    The elasticity ln(C_i+1 / C_i) / ln(N_i+1 / N_i) sits at the interval's geometric
    midpoint, sqrt(N_i x N_i+1).

    Raises:
        SaturationInvariantError: If a row's capacity is not positive (the elasticity needs
            its logarithm).
    """
    fleets = [row.fleet for row in rows]
    capacity = [row.capacity_gbps for row in rows]
    if min(capacity) <= 0:
        raise SaturationInvariantError(
            f"{_curve_label(curve)}: capacity must be positive at every row to read the "
            f"elasticity; got {capacity}"
        )
    midpoints = [math.sqrt(low * high) for low, high in pairwise(fleets)]
    elasticity = [
        math.log(high_capacity / low_capacity) / math.log(high_fleet / low_fleet)
        for (low_fleet, low_capacity), (high_fleet, high_capacity) in pairwise(
            zip(fleets, capacity, strict=True)
        )
    ]
    return midpoints, elasticity


def _crosses_before_first_midpoint(elasticity: Sequence[float], threshold: float) -> bool:
    """Return whether the elasticity is already under the threshold at the first midpoint."""
    return elasticity[0] < threshold


def _reached_at_first_row(useful_beams: Sequence[float], target: float) -> bool:
    """Return whether L already reaches the target at the first row."""
    return useful_beams[0] >= target


def _markers(curve: _CurveKey, rows: Sequence[CurveRow], maximum_use: float) -> ClassMarkers:
    """Return a curve's markers, read on its rows against maximum use.

    The saturation number, placed first, is the first crossing of the elasticity under 0.10,
    rounded half up, or, when not reached, the last row's fleet as
    ``saturation_not_reached_by``; it is the one marker that refuses a curve whose rows cannot
    place it. Beside it, the first crossing under 0.25 and the fleet at which L reaches 90
    percent of maximum use: each is None when not reached, and None too when the rows cannot
    place it (the 0.25 crossing before the first midpoint, the 90 percent fleet at or before
    the first row; :func:`_unplaced_marker_limits` states that in the curve's limits).

    Raises:
        SaturationInvariantError: If a row's capacity is not positive (the elasticity needs
            its logarithm), or the saturation number's crossing lies before the first
            midpoint.
    """
    fleets = [row.fleet for row in rows]
    midpoints, elasticity = _elasticity(curve, rows)
    name = _curve_label(curve)
    saturation = _first_crossing_under(
        midpoints, elasticity, _SATURATION_ELASTICITY, f"{name}, the saturation number"
    )
    supporting = (
        None
        if _crosses_before_first_midpoint(elasticity, _SUPPORTING_ELASTICITY)
        else _first_crossing_under(
            midpoints, elasticity, _SUPPORTING_ELASTICITY, f"{name}, the crossing under 0.25"
        )
    )
    useful_beams = [row.useful_beams for row in rows]
    target = _MAXIMUM_USE_MARKER_SHARE * maximum_use
    ninety = (
        None
        if _reached_at_first_row(useful_beams, target)
        else _fleet_reaching(fleets, useful_beams, target)
    )
    return ClassMarkers(
        maximum_use_beams=maximum_use,
        saturation_number=None if saturation is None else round_half_up(saturation),
        saturation_not_reached_by=fleets[-1] if saturation is None else None,
        elasticity_under_0p25_fleet=None if supporting is None else round_half_up(supporting),
        fleet_at_90pct_of_maximum_use=None if ninety is None else round_half_up(ninety),
    )


def _unplaced_marker_limits(
    curve: _CurveKey, rows: Sequence[CurveRow], maximum_use: float
) -> tuple[str, ...]:
    """Return the limits a curve states for its supporting markers that its rows cannot place.

    Such a marker is None in the markers, like one not reached; this says which it is, naming
    the class or the band point.
    """
    _, elasticity = _elasticity(curve, rows)
    name = _curve_label(curve)
    limits = []
    if _crosses_before_first_midpoint(elasticity, _SUPPORTING_ELASTICITY):
        curve_in_prose = name.replace("_", " ")
        limits.append(
            f"The {curve_in_prose}'s crossing under {_SUPPORTING_ELASTICITY:g} lies before the "
            "first midpoint (the geometric mean of the first two rows), where the rows cannot "
            "place it, so it is not reported; a sweep starting lower would place it."
        )
    if _reached_at_first_row(
        [row.useful_beams for row in rows], _MAXIMUM_USE_MARKER_SHARE * maximum_use
    ):
        limits.append(
            f"The {name} useful beams already reach {_MAXIMUM_USE_MARKER_SHARE:g} of maximum "
            "use at the first row, so the fleet at which they reach it lies at or before the "
            "first row and is not reported; a sweep starting lower would place it."
        )
    return tuple(limits)


# ===========================================================================
# The curve
# ===========================================================================


def _check_grid(population: PopulationGrid, inputs: SaturationInputs) -> None:
    """Refuse a population grid that is not the one the inputs name (by its SHA-256).

    Raises:
        PopulationGridError: Naming the grid and both digests.
    """
    if population.sha256 != inputs.demand.grid_sha256:
        raise PopulationGridError(
            f"the population grid {population.file_name} has SHA-256 {population.sha256}, "
            f"but the inputs expect {inputs.demand.grid_sha256}"
        )


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


def _class_limits(inputs: SaturationInputs, device_class: DeviceClass) -> _AllocationLimits:
    """Return one class's allocation limits as the curve's inputs set them.

    The one place they are built, so the curve and every recomputation of one of its rows
    allocate alike: B from the capacity calibration and the reference panel, the class's
    people per beam (the spectrum times its central SE over its busy-hour load), the take-up,
    the beam model, the fill's bands and passes, the spectrum and the class's central SE, and
    a directional class's rules D1 to D6 at the module's serving rule (None for the phone
    class).

    Args:
        inputs: The curve's inputs (one entry per class, the contract guarantees).
        device_class: The class.

    Returns:
        The class's limits.
    """
    entry = next(entry for entry in inputs.classes if entry.device_class is device_class)
    return _AllocationLimits(
        beams_per_satellite=_beams_per_satellite(inputs.shell),
        people_per_beam=_people_per_beam(inputs.spectrum_mhz, entry),
        take_up=inputs.demand.take_up,
        beam=_beam_model(inputs.shell),
        footprint_bands=inputs.sweep.footprint_bands,
        passes=inputs.sweep.passes,
        spectrum_mhz=inputs.spectrum_mhz,
        spectral_efficiency_bps_per_hz=entry.spectral_efficiency_bps_per_hz,
        directional=_directional_rules(inputs, entry),
    )


def _band_limits(inputs: SaturationInputs, point: BandPoint) -> _AllocationLimits:
    """Return a band point's allocation limits: the phone class's, but for the point's beam.

    The beam's half-power width is the point's, and its footprint is scaled by the point's
    spacing area factor (the ground a co-channel beam occupies over its 3 dB footprint), so
    the fill, the two bounds and maximum use read the same effective area per beam. B is the
    point's own count, or the calibration's at the reference panel when it sets none. The
    point's demand threshold and grid set its demand cells (:func:`_band_cells`).

    Args:
        inputs: The curve's inputs.
        point: The band point.

    Returns:
        The point's limits.
    """
    phone = _class_limits(inputs, DeviceClass.PHONE_CLASS)
    beam = _beam_model(inputs.shell.model_copy(update={"beamwidth_factor": point.beamwidth_factor}))
    return replace(
        phone,
        beams_per_satellite=(
            _beams_per_satellite(inputs.shell)
            if point.beams_per_satellite is None
            else float(point.beams_per_satellite)
        ),
        beam=replace(beam, footprint_km2=beam.footprint_km2 * point.spacing_area_factor),
    )


def _band_cells(
    population: PopulationGrid,
    point: BandPoint,
    central: _DemandCells,
    central_threshold_per_km2: float,
) -> _DemandCells:
    """Return a band point's demand cells: the central ones when the point keeps the central
    threshold and the shipped grid, else the grid (summed as the point says) at its threshold.

    Args:
        population: The population grid.
        point: The band point.
        central: The central curve's demand cells.
        central_threshold_per_km2: The central curve's demand threshold.

    Returns:
        The point's demand cells.
    """
    if (
        point.density_threshold_per_km2 == central_threshold_per_km2
        and point.grid_aggregation == GRID_AGGREGATION_SHIPPED
    ):
        return central
    return _demand_cells(population, point.density_threshold_per_km2, point.grid_aggregation)


@dataclass(frozen=True, eq=False)
class _CurvePlan:
    """One curve the sweep computes: a class's central curve or a band point's.

    Attributes:
        key: The class or the band point.
        fleets: Its requested fleets, in order.
        snapshots: Its snapshots at each fleet.
        context: What its snapshot tasks need: the shell, its demand cells and limits, the
            trim's settings.
        point: The band point, for a band point's curve; None for a class's.
    """

    key: _CurveKey
    fleets: tuple[int, ...]
    snapshots: int
    context: _SweepContext
    point: BandPoint | None


def _class_plan(
    inputs: SaturationInputs, cells: _DemandCells, device_class: DeviceClass
) -> _CurvePlan:
    """Return one class's plan: the mounted terminal over the sweep's fleets and its extension,
    every other class over the fleets; the phone class at its central snapshots, the directional
    classes at the directional snapshots.

    Args:
        inputs: The curve's inputs.
        cells: The central demand cells.
        device_class: The class.

    Returns:
        The class's plan.
    """
    sweep = inputs.sweep
    limits = _class_limits(inputs, device_class)
    return _CurvePlan(
        key=device_class,
        fleets=(
            sweep.fleets + sweep.mounted_terminal_extension
            if device_class is DeviceClass.MOUNTED_TERMINAL_CLASS
            else sweep.fleets
        ),
        snapshots=(
            sweep.snapshots_phone_central
            if limits.directional is None
            else sweep.snapshots_directional
        ),
        context=_SweepContext(shell=inputs.shell, cells=cells, limits=limits, trim=inputs.trim),
        point=None,
    )


def _band_plan(
    inputs: SaturationInputs, population: PopulationGrid, cells: _DemandCells, point: BandPoint
) -> _CurvePlan:
    """Return one band point's plan: over the sweep's fleets at the bands' snapshots, with its own
    demand cells (:func:`_band_cells`) and limits (:func:`_band_limits`).

    Args:
        inputs: The curve's inputs.
        population: The population grid (a band point may sum it or set its own threshold).
        cells: The central demand cells.
        point: The band point.

    Returns:
        The band point's plan.
    """
    return _CurvePlan(
        key=point.name,
        fleets=inputs.sweep.fleets,
        snapshots=inputs.sweep.snapshots_bands,
        context=_SweepContext(
            shell=inputs.shell,
            cells=_band_cells(population, point, cells, inputs.demand.density_threshold_per_km2),
            limits=_band_limits(inputs, point),
            trim=inputs.trim,
        ),
        point=point,
    )


def _curve_plans(
    inputs: SaturationInputs, population: PopulationGrid, cells: _DemandCells
) -> tuple[_CurvePlan, ...]:
    """Return the curves a run computes: every class in its key's order, then every band point.

    Each is built by :func:`_class_plan` or :func:`_band_plan`, which the drift seams also build
    their one row's plan with.

    Args:
        inputs: The curve's inputs.
        population: The population grid (a band point may sum it or set its own threshold).
        cells: The central demand cells.

    Returns:
        The plans, classes first.
    """
    return (
        *(_class_plan(inputs, cells, entry.device_class) for entry in inputs.classes),
        *(_band_plan(inputs, population, cells, point) for point in inputs.bands),
    )


def _snapshot_times(sweep: SweepInputs) -> npt.NDArray[np.float64]:
    """Return the run's snapshot times, drawn once from the sweep's seed.

    ``numpy.random.default_rng(seed).uniform(0, sidereal day, n)``, n the most snapshots any curve
    takes (the phone class's central curve, the directional classes or the band points), so a
    curve at fewer snapshots takes the first of them. The curve and both drift seams draw here, so
    a recomputed row reads the curve's own times.
    """
    return np.random.default_rng(sweep.seed).uniform(
        _DAY_START_S,
        _SIDEREAL_DAY_S,
        max(sweep.snapshots_phone_central, sweep.snapshots_directional, sweep.snapshots_bands),
    )


def _plan_tasks(
    plan: _CurvePlan,
    fleet_index: int,
    fleet: int,
    times: npt.NDArray[np.float64],
    snapshots_trim: int,
) -> list[_SnapshotTask]:
    """Return one curve's snapshot tasks at one requested fleet, one per snapshot of its plan in
    the draw's order; the phone class's central curve prices the trim on the first
    ``snapshots_trim`` of them."""
    return [
        _SnapshotTask(
            curve=plan.key,
            fleet_index=fleet_index,
            requested_fleet=fleet,
            snapshot_index=snapshot_index,
            time_s=float(times[snapshot_index]),
            prices_trim=plan.key is DeviceClass.PHONE_CLASS and snapshot_index < snapshots_trim,
        )
        for snapshot_index in range(plan.snapshots)
    ]


def _plan_rows(
    plan: _CurvePlan, fleets: Sequence[_FleetSnapshots], requested_fleets: Sequence[int]
) -> tuple[CurveRow, ...]:
    """Return one curve's rows from its fleets' snapshots (:func:`_class_rows` at the plan's B, the
    directional diagnostics for a directional class, the trim for the phone class's central
    curve)."""
    limits = plan.context.limits
    return _class_rows(
        fleets,
        requested_fleets,
        beams_per_satellite=limits.beams_per_satellite,
        directional=limits.directional is not None,
        trim_floors_dbi=(
            plan.context.trim.floors_dbi if plan.key is DeviceClass.PHONE_CLASS else None
        ),
    )


def _plan_maximum_use(plan: _CurvePlan) -> float:
    """Return one curve's maximum use (stage 10) from its plan: its demand cells and limits, at its
    shell's inclination. The curve reads its markers against it, and the drift tests rebuild every
    curve's maximum use through the curve's own plans."""
    context = plan.context
    return _maximum_use(context.cells, context.limits, context.shell.inclination_deg)


def _stated_limits(
    inputs: SaturationInputs, classes: Sequence[ClassCurve], bands: Sequence[BandCurve]
) -> tuple[str, ...]:
    """Return a curve's stated limits: the curve's own (:func:`_curve_limits`), then each class's
    and then each band point's supporting markers its rows cannot place
    (:func:`_unplaced_marker_limits`), in the curve's order.

    Args:
        inputs: The curve's inputs.
        classes: Its class curves, in their order.
        bands: Its band points' curves, in their order.

    Returns:
        The stated limits.
    """
    keyed: list[tuple[_CurveKey, ClassCurve | BandCurve]] = [
        *((entry.device_class, entry) for entry in classes),
        *((band.point.name, band) for band in bands),
    ]
    return (
        *_curve_limits(inputs),
        *(
            limit
            for key, entry in keyed
            for limit in _unplaced_marker_limits(key, entry.rows, entry.markers.maximum_use_beams)
        ),
    )


def _method(inputs: SaturationInputs) -> str:
    """Return the method, stated as the rule, at the inputs' values."""
    shell, sweep, trim = inputs.shell, inputs.sweep, inputs.trim
    floors = ", ".join(f"{floor_dbi:g}" for floor_dbi in trim.floors_dbi)
    return (
        "Smallest footprint first, per snapshot: the satellite-cell pairs in view are filled "
        f"in {sweep.footprint_bands} geometric footprint bands from the smallest, "
        f"{sweep.passes} proportional passes in each, every band committed before the next; "
        "per satellite at most its beams, per cell one co-channel layer (its area) and the "
        "class's people cap, per pair one layer: the phone class's allocation, and each "
        "directional class's first layer at its own people cap. A directional class then "
        "stacks layers under sky sectors: its terminal's sky above the mask split into "
        "sectors of equal solid angle, ring by ring from the zenith; a second banded fill on "
        "the same band edges over (cell, sector) keys, a key's area the cell's less its first "
        "layer's from that sector, a pair's cap one layer less its first-layer beams; before "
        "each band its candidates are taken by (cell, footprint, satellite), and one is "
        "admitted only at least one terminal beamwidth, sqrt(4 pi / (1.133 x D)), from every "
        "satellite serving its cell in another sector and from every candidate of its cell "
        "admitted earlier in the band in another sector (a satellite serves a cell when its "
        "layer covers at least 1 / SINR_1 of it). Each served sub-pair is priced by the full "
        "sum of its cell's other layers in other sectors (first layers not against each "
        "other), each weighted by its share of the cell at the terminal's Gaussian main lobe "
        f"floored at {inputs.sidelobe_floor_db:g} dB: SE = {inputs.se_anchor_bps_per_hz:g} x "
        "log2(1 + SINR), the single-layer SINR_1 = 2^(central SE / that anchor) - 1; a cell "
        "keeps its stacked layers only when they do not lower its capacity, the dropped beams "
        "spent. Each directional row reports its kept stacked share (the share of L in the kept "
        "stacked sub-pairs, in cells their first layer covers, that the full sum prices against "
        "a layer of another sector), their beam-weighted median separation from the nearest "
        "such layer and their beam-weighted mean full-sum interference in dB, none of them "
        "measured against the cell's main satellite alone. A circular Walker Delta shell at "
        f"{shell.altitude_km:g} km and {shell.inclination_deg:g} degrees (P = round(sqrt(N)) "
        "planes of S = round(N / P), the realized N = P x S, phasing F = 1) with a "
        f"{shell.elevation_mask_deg:g} degree mask; a square {shell.reference_aperture_m2:g} "
        f"m^2 aperture at {shell.carrier_hz / _HZ_PER_GHZ:g} GHz, half-power beamwidth "
        f"{shell.beamwidth_factor:g} wavelengths over its side, the beams per satellite "
        "derived from the capacity calibration and the panel. Each fleet's row averages its "
        "snapshots, drawn once over a sidereal day from seed "
        f"{sweep.seed}. Maximum use in closed form (every cell served by the best satellite "
        "the shell can ever offer it; for a directional class one layer per sky sector, each "
        "at the best its ring allows, whether its azimuth is reachable ignored); the markers "
        "on the elasticity of capacity at the geometric midpoints of the rows, interpolated "
        "in ln N. The phone class's central rows carry the interference trim, priced on the "
        f"first {sweep.snapshots_trim} snapshot(s) of each row: power control gives every beam "
        "equal flux at its target, so a beam's power goes as its slant range squared over g, "
        f"g = cos^{trim.scan_exponent:g} of its scan angle; a victim cell's aggregate "
        "far-sidelobe interference over its own signal is x = gamma / G0 x the sum, over "
        "every lit satellite above the victim's horizon, of the satellite's summed beam "
        "powers x g toward the victim / the slant range squared, G0 the panel's broadside "
        "directivity (4 pi x its area / the wavelength squared); "
        f"{trim.victims:,} served cells are the victims, drawn without replacement in "
        f"proportion to their beams, a fresh draw from seed {trim.seed} at each row; the trim "
        "is 1 - the victims' mean of log2(1 + 1 / (1 + x)), at each floor gamma of "
        f"{floors} dBi. Each band point of the phone class is its central curve but for one "
        f"changed input, at {sweep.snapshots_bands} snapshot(s) a row over the same fleets, "
        "with its own rows and markers: the beam's half-power width (the taper), the ground a "
        "co-channel beam occupies over its 3 dB footprint (wider co-channel spacing, scaling "
        "the area per beam in the fill, the bounds and maximum use alike), the demand "
        "threshold, the grid (the shipped cells summed k x k), or the beams per satellite."
    )


def _checks_passed(inputs: SaturationInputs) -> tuple[str, ...]:
    """Return the checks a computed curve passed, each stated as its rule."""
    return (
        "bounds: at every snapshot of every class and band point, useful beams at most "
        "min(ceiling, supply) and the ceiling at most maximum use (for a directional class, "
        "the sector-rule ceiling and its maximum use), within "
        f"{_BOUNDS_RELATIVE_TOLERANCE:g} relative",
        f"stall floor: from {_STALL_FLOOR_FROM_FLEET:,} satellites up, the phone class's "
        f"central useful beams at least {inputs.sweep.stall_floor:g} x min(ceiling, supply), "
        "at every snapshot and in the snapshot means",
        "capacity per satellite never rises between consecutive rows of any class or band "
        f"point by more than {_CAPACITY_PER_SATELLITE_RISE_TOLERANCE:g} relative to the "
        "earlier row (the snapshots' noise)",
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
    """Compute the saturation curve on a population grid: every class, then every band point.

    Runs stages 2 to 11 of the module docstring for each class, the small terminal and the
    mounted terminal by rules D1 to D6 at the sweep's directional snapshots (the mounted
    terminal over its extension too) and the phone class at its central snapshots, and stage
    12, the interference trim, on the phone class's central rows; then each band point of
    the phone class, the central curve but for its one changed input, at the bands'
    snapshots. Every curve's tasks share one sweep. Checks the bounds and capacity per
    satellite for every class and band point and the stall floor for the phone class's
    central curve; reads each curve's markers against its own maximum use, states any
    supporting marker the rows cannot place among the limits, and records the run's wall
    time and peak-memory bound.

    Args:
        inputs: The curve's inputs.
        population: The population grid; its SHA-256 must be ``inputs.demand.grid_sha256``.
        version_stamp: The stamp the curve carries.

    Returns:
        The curve, with every class's rows and markers and every band point's.

    Raises:
        PopulationGridError: If the grid is not the one the inputs name, not global, or not
            divisible by a band point's aggregation.
        SaturationInvariantError: If a check fails, the realized fleets do not strictly
            increase, a saturation number lies before the rows can place it, or the trim asks
            for more snapshots than the phone class's central curve computes.
        SaturationSweepError: If a saturation worker dies or runs out of memory, or the sweep's
            process pool breaks with a stated cause.
    """
    started = time.perf_counter()
    _check_grid(population, inputs)
    sweep = inputs.sweep
    if sweep.snapshots_trim > sweep.snapshots_phone_central:
        raise SaturationInvariantError(
            f"the interference trim prices the first {sweep.snapshots_trim} snapshots of the "
            f"phone class's central curve, which computes {sweep.snapshots_phone_central}: "
            "sweep.snapshots_trim must not exceed sweep.snapshots_phone_central"
        )
    _check_realized_fleets(sweep.fleets)
    _check_realized_fleets(sweep.fleets + sweep.mounted_terminal_extension)
    cells = _demand_cells(population, inputs.demand.density_threshold_per_km2)
    plans = _curve_plans(inputs, population, cells)
    times = _snapshot_times(sweep)
    tasks = [
        task
        for plan in plans
        for fleet_index, fleet in enumerate(plan.fleets)
        for task in _plan_tasks(plan, fleet_index, fleet, times, sweep.snapshots_trim)
    ]
    logger.info(
        "saturation: %d classes and %d band points, %d snapshot tasks on %d demand cells of %s",
        len(inputs.classes),
        len(inputs.bands),
        len(tasks),
        cells.count,
        population.file_name,
    )
    run = _run_sweep(tasks, {plan.key: plan.context for plan in plans})
    curves: list[ClassCurve] = []
    bands: list[BandCurve] = []
    for plan in plans:
        fleets = _by_fleet(
            [result for result in run.results if result.task.curve is plan.key], len(plan.fleets)
        )
        maximum_use = _plan_maximum_use(plan)
        _check_bounds(plan.key, fleets, maximum_use)
        if plan.key is DeviceClass.PHONE_CLASS:
            _check_stall_floor(fleets, sweep.stall_floor)
        rows = _plan_rows(plan, fleets, plan.fleets)
        _check_capacity_per_satellite(plan.key, rows)
        markers = _markers(plan.key, rows, maximum_use)
        if plan.point is not None:
            bands.append(BandCurve(point=plan.point, rows=rows, markers=markers))
        elif isinstance(plan.key, DeviceClass):
            curves.append(ClassCurve(device_class=plan.key, rows=rows, markers=markers))
        logger.info(
            "saturation: %s, maximum use %.0f beams, saturation number %s",
            _curve_label(plan.key),
            maximum_use,
            markers.saturation_number
            if markers.saturation_number is not None
            else f"not reached by {markers.saturation_not_reached_by}",
        )
    wall_time_s = time.perf_counter() - started
    peak_memory_mb = _own_peak_mb() + run.workers_peak_mb
    logger.info(
        "saturation: at most %d workers at once; peak memory bound %.0f MB (budget %.0f MB); "
        "%.1f s",
        run.workers,
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
        classes=tuple(curves),
        bands=tuple(bands),
        limits=_stated_limits(inputs, curves, bands),
    )


def _inputs_grid(checkout: SourceCheckout, inputs: SaturationInputs) -> PopulationGrid:
    """Return the population grid the inputs name, anchored at the repository root and checked
    against its SHA-256: the one grid load of the command and the drift seams.

    Args:
        checkout: The source checkout whose repository root a relative grid path anchors to.
        inputs: The curve's inputs (their demand names the grid and its digest).

    Returns:
        The grid.

    Raises:
        ModelFileError: If the grid is missing, unreadable or not a population grid archive.
        PopulationGridError: If the grid is not the one the inputs name.
    """
    return load_population_grid(
        _anchored(checkout, inputs.demand.grid_path), inputs.demand.grid_sha256
    )


def _seam_grid_and_cells(
    inputs: SaturationInputs, population: PopulationGrid | None
) -> tuple[PopulationGrid, _DemandCells]:
    """Return the grid the inputs name and its central demand cells, as a drift seam reads them:
    the caller's grid when it has one loaded (checked against the inputs' digest), else the grid
    loaded here (:func:`_inputs_grid`).

    Raises:
        ModelFileError: If the module is not in a source checkout or the grid is unreadable.
        PopulationGridError: If the grid is not the one the inputs name.
    """
    if population is None:
        population = _inputs_grid(locate_source_checkout(__file__), inputs)
    else:
        _check_grid(population, inputs)
    return population, _demand_cells(population, inputs.demand.density_threshold_per_km2)


def _plan_row(plan: _CurvePlan, fleet: int, sweep: SweepInputs) -> CurveRow:
    """Return one curve's row at one requested fleet, computed in this process as the curve
    computes it: its plan's snapshots from the run's draw (:func:`_snapshot_times`), each through
    :func:`_run_snapshot`, grouped and built into the row as the curve's rows are."""
    times = _snapshot_times(sweep)
    results = [
        _run_snapshot(task, plan.context)
        for task in _plan_tasks(plan, 0, fleet, times, sweep.snapshots_trim)
    ]
    (row,) = _plan_rows(plan, _by_fleet(results, 1), (fleet,))
    return row


def _class_row(
    class_key: DeviceClass,
    fleet: int,
    inputs: SaturationInputs,
    *,
    population: PopulationGrid | None = None,
) -> CurveRow:
    """Return one class's row at one fleet, as the curve computes it: a drift seam.

    ``fleet`` is the requested fleet the row's shell is built from (a row's
    ``requested_fleet``, never its realized key, which can build another shell). The row is
    computed in this process at the inputs' own settings: the grid they name, the class's plan
    (:func:`_class_plan`: its limits and snapshots), its snapshots from the run's draw, and on
    the phone class's first snapshots the interference trim; so it equals the curve's row for
    that request.

    Args:
        class_key: The class.
        fleet: The requested fleet.
        inputs: The curve's inputs (a committed curve's ``parameters``).
        population: The grid the inputs name, when the caller has it loaded (a drift check
            rebuilding several rows loads it once, through :func:`_inputs_grid`); None loads it.

    Returns:
        The class's row at that request.

    Raises:
        ModelFileError: If the module is not in a source checkout or the grid is unreadable.
        PopulationGridError: If the grid is not the one the inputs name.
    """
    _, cells = _seam_grid_and_cells(inputs, population)
    return _plan_row(_class_plan(inputs, cells, class_key), fleet, inputs.sweep)


def _band_row(
    point: BandPoint,
    fleet: int,
    inputs: SaturationInputs,
    *,
    population: PopulationGrid | None = None,
) -> CurveRow:
    """Return one band point's row at one fleet, as the curve computes it: a drift seam.

    ``fleet`` is the requested fleet. The row is computed in this process at the inputs' own
    settings: the grid they name, the point's plan (:func:`_band_plan`: its demand cells, its
    limits and the bands' snapshots) and its snapshots from the run's draw; so it equals the
    curve's row for that request.

    Args:
        point: The band point (a committed curve's band point, which is its parameters').
        fleet: The requested fleet.
        inputs: The curve's inputs (a committed curve's ``parameters``).
        population: The grid the inputs name, when the caller has it loaded (a drift check
            rebuilding several rows loads it once, through :func:`_inputs_grid`); None loads it.

    Returns:
        The band point's row at that request.

    Raises:
        ModelFileError: If the module is not in a source checkout or the grid is unreadable.
        PopulationGridError: If the grid is not the one the inputs name, or does not divide by
            the point's aggregation.
    """
    grid, cells = _seam_grid_and_cells(inputs, population)
    return _plan_row(_band_plan(inputs, grid, cells, point), fleet, inputs.sweep)


# ===========================================================================
# The command: compute the curve a scenario implies and promote it
# ===========================================================================


def _anchored(checkout: SourceCheckout, path: str | Path) -> Path:
    """Return a path anchored at the repository root when it is relative, else as given."""
    candidate = Path(path)
    return candidate if candidate.is_absolute() else checkout.repo_dir / candidate


def _log_summary(curve: SaturationCurve) -> None:
    """Log the curve's summary: each class's saturation number, or the last row it is not
    reached by, and its maximum use, in the class key's order; then the run's wall time and
    peak-memory bound."""
    for entry in curve.classes:
        markers = entry.markers
        reading = (
            f"saturation number {markers.saturation_number:,}"
            if markers.saturation_number is not None
            else f"not reached by {markers.saturation_not_reached_by:,}"
        )
        logger.info(
            "saturation curve: %s, %s, maximum use %.0f beams",
            entry.device_class.value,
            reading,
            markers.maximum_use_beams,
        )
    measured = curve.provenance.run_measurement
    logger.info(
        "saturation curve: computed in %.1f s, peak memory bound %.0f MB (budget %.0f MB)",
        measured.wall_time_s,
        measured.peak_memory_mb,
        _MEMORY_BUDGET_MB,
    )


def _check_destination(out: Path) -> None:
    """Refuse, before anything is computed, a destination the shared writer would refuse.

    The writer (:func:`common.file_io.write_files_with_rollback`) refuses a symbolic link and an
    existing file that is not a regular file, and stages its file beside the destination,
    creating the missing parent directories; so the destination's nearest existing ancestor must
    be a directory this process can write into and search. A full promotion computes for about
    26 minutes before it writes, so this refuses what it can know first; the writer keeps its own
    checks at the write.

    Args:
        out: The anchored destination.

    Raises:
        ModelFileError: Naming the destination, saying nothing was changed or computed.
    """
    untouched = "no destination was changed and nothing was computed"
    if out.is_symlink():
        raise ModelFileError(
            out,
            "is a symbolic link, and an artifact replaces only a regular file (point the output "
            f"at the link's target); {untouched}",
        )
    if out.exists() and not out.is_file():
        raise ModelFileError(out, f"exists and is not a regular file; {untouched}")
    ancestor = out.parent
    while not ancestor.exists(follow_symlinks=False):
        ancestor = ancestor.parent
    if not ancestor.is_dir() or not os.access(ancestor, os.W_OK | os.X_OK):
        raise ModelFileError(
            out,
            f"could not write: its nearest existing parent, {ancestor}, is not a directory this "
            f"process can write into; {untouched}",
        )


def promote_saturation_curve(
    scenario_path: str | Path, output_path: str | Path, version_stamp: str | None = None
) -> Path:
    """Compute the saturation curve a scenario implies and write it, promoted.

    Loads the scenario, narrows it to its Iridium dials (a scenario without an ``iridium:``
    block is refused before anything runs), builds the curve's inputs from those dials (the
    held spectrum; every other input its named constant), loads the population grid the inputs
    name, anchored at the repository root and checked against its SHA-256, computes the curve,
    logs its summary, checks that it is complete and writes it through
    :func:`common.file_io.write_files_with_rollback`: staged in full beside the destination,
    then renamed over it, so a failure leaves any existing file as it was. A destination the
    writer would refuse (a symbolic link, an existing file that is not a regular file, a nearest
    existing parent that is not a writable directory) is refused before the computation, and
    the writer checks again at the write. It reads no curve, so a stale or missing curve never
    blocks its own regeneration.

    Args:
        scenario_path: The scenario YAML (it must select the Iridium model); a relative path
            resolves against the working directory.
        output_path: Where to write the curve; a relative path anchors to the repository root.
        version_stamp: The curve's stamp; today's ISO date when None.

    Returns:
        The path written.

    Raises:
        ModelFileError: If the module is not running from a source checkout, the scenario or
            the grid is missing, unreadable or malformed, or the destination is refused or the
            curve cannot be written.
        ValueError: If the scenario is invalid (a :class:`pydantic.ValidationError`) or does
            not select the Iridium model (:class:`~communications.iridium.NotAnIridiumConfigError`),
            the grid is not the one the inputs name (:class:`PopulationGridError`), a check
            fails (:class:`SaturationInvariantError`), the sweep fails (a saturation worker
            dies or runs out of memory, or its process pool breaks with a stated cause:
            :class:`SaturationSweepError`), or the curve fails its completeness check
            (:class:`~communications.saturation_curve.SaturationCurveError`).
    """
    checkout = locate_source_checkout(__file__)
    config = load_comms_config(Path(scenario_path))
    inputs = saturation_inputs_for(iridium_dials_of(config))
    out = _anchored(checkout, output_path)
    _check_destination(out)
    population = _inputs_grid(checkout, inputs)
    stamp = version_stamp if version_stamp is not None else date.today().isoformat()
    logger.info("saturation curve: computing from %s, stamp %s", scenario_path, stamp)
    curve = compute_saturation(inputs, population, version_stamp=stamp)
    _log_summary(curve)
    check_curve_complete(curve)
    write_files_with_rollback([artifact_write(out, curve)])
    logger.info("promoted saturation curve written to %s", out)
    return out


def _build_parser() -> CliArgumentParser:
    """Build the command's parser (usage errors exit with EXIT_USAGE)."""
    parser = CliArgumentParser(
        prog="python -m communications.saturation",
        description=(
            "Compute the saturation curve a scenario's Iridium dials imply (every class and "
            "band point) and write it, promoted, into the repo-root communications/models/ "
            "workstream."
        ),
    )
    parser.add_argument(
        "scenario",
        help="Scenario YAML (must select the Iridium model), e.g. scenarios/iridium.yaml.",
    )
    parser.add_argument(
        "output",
        help=(
            "Curve JSON path, e.g. communications/models/iridium/saturation_curve.json "
            "(relative paths anchor to the repo root)."
        ),
    )
    parser.add_argument(
        "--version-stamp",
        default=None,
        help="The curve's stamp (any string). Defaults to today's ISO date.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point. Returns a process exit code.

    Args:
        argv: Argument list (defaults to ``sys.argv[1:]``).

    Returns:
        :data:`~common.cli.EXIT_OK` on success; :data:`~common.cli.EXIT_ERROR` (after one
        ``ERROR:`` log line, no traceback) when the scenario cannot be read, is invalid or does
        not select the Iridium model, the destination is one the writer would refuse (found
        before the computation), the grid is not the one expected, a check fails, the sweep
        fails (a saturation worker dies, most likely out of memory, or runs out of memory, or
        the sweep's process pool breaks with a stated cause; the line carries the sweep's task
        count, and nothing is written), the curve is incomplete, or the curve cannot be written.
        Every one is a :class:`~common.file_io.ModelFileError` or a ``ValueError``, so one
        handler logs them all. Usage errors exit through
        :class:`~common.cli.CliArgumentParser` with :data:`~common.cli.EXIT_USAGE`.
    """
    configure_cli_logging()
    args = _build_parser().parse_args(argv)
    try:
        promote_saturation_curve(args.scenario, args.output, args.version_stamp)
    except (ModelFileError, ValueError) as exc:
        scenario = Path(args.scenario)
        logger.error(
            "could not promote the saturation curve from %s: %s",
            scenario,
            describe_failure(exc, scenario),
        )
        return EXIT_ERROR
    return EXIT_OK


__all__ = [
    "PopulationGrid",
    "PopulationGridError",
    "SaturationInvariantError",
    "SaturationSweepError",
    "compute_saturation",
    "load_population_grid",
    "main",
    "promote_saturation_curve",
]


if __name__ == "__main__":
    raise SystemExit(main())
