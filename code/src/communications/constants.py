"""Module-level ``Final`` named constants for the communications CELLULAR model.

This module is the single source of truth for the comms config's "no bare
numeric literals" rule (CLAUDE.md). Every default the ``communications.config``
Pydantic blocks read lives here, each with a docstring carrying:

- A source class tag: SOURCED_FACT / SOURCED_ESTIMATE / ESTIMATE / SCENARIO /
  FOUNDER_SET / DERIVED.
- A citation: a global ``COMM-*`` claim id from ``research/SOURCE_INDEX.md``,
  a research-doc path, the coverage-sim findings, or a founder note.

The eight cadence / launch-cost defaults are NOT re-stated here: they are
IMPORTED from ``common.cadence`` (the shared spine both ventures consume) and
re-exported, so the comms config behaves identically to the data-center cadence
machinery and cannot drift from it (re-export, not a hand-copy, makes the
``test_config`` drift-guard trivially true). Importing from ``common`` is not a
venture dependency. This module never imports ``data_center`` (the cross-import
guard forbids it).

The FOUNDER-SET dials are recorded as real default VALUES
(``satellites_for_full_coverage = 340`` the coverage FLOOR, ``share_of_fleet =
0.18``, ``subscribers_at_full_coverage = 10,000,000`` the subscriber TARGET,
``subscribers_per_satellite = 75,000``, ``max_fleet_satellites = 2,000``,
``satellite_build_cost = 1.05`` $M, ``revenue_multiple = 1.5`` mirroring the DC R,
``arpu_usd_per_month = 50.0`` the supportable median); they stay configurable.
Because they are real
values, the Phase 5 placeholder check CANNOT use value-equals-default as the
placeholder signal (that would false-positive on the real defaults). Instead a
static per-dial flag map (:data:`PLACEHOLDER_DIAL_FLAGS`) records, per guarded dial,
whether its default is a real founder-set value (``False``) or an arbitrary sentinel
(``True``); all are ``False`` now. The Phase 5 ``check_no_placeholder_inputs`` reads
that map.

CAPACITY DIMENSION (founder-directed 2026-06-26, research COMM-535..560). The model
is sized to SERVE the subscriber base, not merely to cover it. The subscriber TARGET
(``subscribers_at_full_coverage``) is the INPUT; the fleet is sized to serve it at
``subscribers_per_satellite`` attached subscribers per satellite, floored by the
coverage floor and capped by the saturation cap ``max_fleet_satellites``. The fleet
target is ``min(max_fleet_satellites, max(satellites_for_full_coverage,
ceil(subscriber_target / subscribers_per_satellite)))``.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

# The eight cadence + launch-cost defaults are the shared spine's authority.
# Re-exported (not hand-copied) so the comms config is bit-identical to the
# data-center cadence machinery and cannot drift. ROUND_TO_NEAREST_OFFSET is the
# shared half-up rounding offset the Phase 2 comms-share re-rounding reuses.
from common.cadence import (
    CADENCE_CEILING_DEFAULT,
    FIRST_LAUNCH_YEAR_DEFAULT,
    HIGH_CADENCE_COST_MUSD_DEFAULT,
    HIGH_CADENCE_LAUNCHES_DEFAULT,
    LAUNCHES_AT_YEAR_5_DEFAULT,
    LAUNCHES_AT_YEAR_10_DEFAULT,
    LOW_CADENCE_COST_MUSD_DEFAULT,
    LOW_CADENCE_LAUNCHES_DEFAULT,
    ROUND_TO_NEAREST_OFFSET,
)

# ===========================================================================
# Density-regime enum (the two-regime ground interface, Phase 4)
# ===========================================================================


class DensityRegime(StrEnum):
    """The terrestrial density regime a ground cost-per-subscriber baseline is for.

    Declared in this leaf ``constants`` module so both ``config.py`` (the
    ``GroundInterfaceDials`` block, Phase 4) and ``ground.py`` (the comparison,
    Phase 4) import it without a cycle. ``SPARSE`` is the fresh-build regime whose
    cost the headline verdict reads (space below it is the niche); ``DENSE`` is the
    incumbent-marginal served regime.
    """

    SPARSE = "sparse"
    DENSE = "dense"


class BindingRegime(StrEnum):
    """Which constraint sets the fleet target: the coverage floor or the capacity need.

    The fleet target is ``min(max_fleet_satellites, max(coverage_floor,
    capacity_need))`` where ``capacity_need = ceil(subscriber_target /
    subscribers_per_satellite)``. This enum records which term binds, the founder's
    coverage-vs-capacity question:

    * ``COVERAGE`` -- the coverage floor binds (``capacity_need <= coverage_floor``);
      the subscriber base is small enough that covering the globe needs more
      satellites than serving the base does (the ~10M baseline, where 134 capacity
      satellites are below the 340 coverage floor).
    * ``CAPACITY`` -- the capacity need binds (``coverage_floor < capacity_need <
      max_fleet_satellites``); serving the base needs more satellites than coverage
      does (the ~50M and ~100M scenarios).
    * ``SATURATED`` -- the saturation cap binds (``capacity_need >=
      max_fleet_satellites``); the base would need more satellites than the cap
      allows, so the fleet pins at the cap and the served base is capacity-limited.
    """

    COVERAGE = "coverage"
    CAPACITY = "capacity"
    SATURATED = "saturated"


# ===========================================================================
# Year-bound constants (config Field bounds)
# ===========================================================================

MIN_FY: Final[int] = 2020
"""SCENARIO. Lower bound for any fiscal-year config field. Below this is
pre-venture; comms inputs cannot reference earlier years. Mirrors the DC
``MIN_FY`` bound for cross-model consistency."""

MAX_FY: Final[int] = 2100
"""SCENARIO. Upper bound for any fiscal-year config field. Beyond this the
launch-ramp and coverage extrapolation have no defensible basis."""

MIN_HORIZON_YEARS: Final[int] = 1
"""SCENARIO. Minimum analysis horizon (years after base year)."""

MAX_HORIZON_YEARS: Final[int] = 30
"""SCENARIO. Maximum analysis horizon (years after base year). Beyond this the
build-and-hold trajectory is pure speculation."""

# ===========================================================================
# Run metadata defaults
# ===========================================================================

BASE_YEAR_DEFAULT: Final[int] = 2026
"""SCENARIO. Calendar year for model year 0 (Neutron first-flight year),
matching the DC model's base year so the two share a timeline."""

HORIZON_YEARS_DEFAULT: Final[int] = 10
"""SCENARIO. Default analysis horizon (FY2026 + 10 = FY2036, the full-coverage
target year), matching the DC model's 10-year horizon."""

# ===========================================================================
# Satellite spec dials (the fixed CELLULAR direct-to-cell bird)
# ===========================================================================

SATELLITES_PER_LAUNCH_DEFAULT: Final[int] = 12
"""DERIVED (COMM-258 / COMM-260). Satellites per Neutron launch, a DIRECT input
scalar. The mass-bound count for a Flatellite-class (~800 kg) bird against the
Neutron reusable SSO envelope (~9,500 kg) is ~12; the LEO envelope (~13,000 kg)
gives ~16. Default 12 (SSO), with ~16 the LEO upside. Estimate-bound on the
single-source ~800 kg Flatellite mass read (COMM-253 / COMM-256)."""

SATELLITE_LIFETIME_YEARS_DEFAULT: Final[int] = 5
"""ESTIMATE (COMM-091, the ~$200 to 260/sub/yr replacement split implies a
~5-year hardware lineage). Satellite operating life, the cohort cliff: after this
many years a cohort retires and contributes zero coverage. A design/depreciation
assumption (the Starlink replacement-capex anchor), not a certified field life."""

SATELLITE_BUILD_COST_MUSD_DEFAULT: Final[float] = 1.05
"""FOUNDER_SET (in-band; round 4, 2026-06-25). The flat MASS-MANUFACTURED
CELLULAR-SATELLITE HARDWARE cost, ONE scalar, ~$1.0 to 1.1M (1.05 is the in-band
default). This is a V3-CLASS HARDWARE analogy: the Starlink V3 per-satellite
hardware cost is ~$1.2M (~1,500 kg), the upper hardware anchor (COMM-080). A
CELLULAR direct-to-cell payload is a bigger antenna and more power than a
broadband panel, but FAR smaller than AST's giant phased array (so AST's
~$19 to 21M giant-array figure is the WRONG anchor). It is a HARDWARE
build-cost analogy ONLY, NOT a broadband-product cost claim. CONFIGURABLE."""

# ===========================================================================
# Coverage target dial (the NEW constellation-size target, variable 3)
# ===========================================================================

SATELLITES_FOR_FULL_COVERAGE_DEFAULT: Final[int] = 340
"""FOUNDER_SET (round 4, 2026-06-25). The COVERAGE FLOOR: the minimum constellation
size for everyone in the served band to SEE a satellite (a quality link), the lower
bound on the fleet target. This is NOT the fleet the build fills toward when the
subscriber base is large: the capacity dimension (see
:data:`SUBSCRIBERS_PER_SATELLITE_DEFAULT`) can require more satellites than this to
SERVE the base, in which case the capacity need binds and the fleet target rises
above the floor. The floor is the quality-link case (a 25 degree elevation mask over
the populated mid-latitude band, +/-55 deg, at 95% coverage, ~450 km, ~53 deg
inclined). Backed by the coverage sim (.agent/other/coverage_sim/FINDINGS.md:
populated band, 450 km, 25 deg mask, 95% = 341 sats, founder-rounded to 340) and the
corpus (COMM-209 / COMM-216 / COMM-217 from leo_constellation_coverage_minimums; the
DTC coverage-geography band COMM-386..COMM-405). 340 sits inside the analytic ~290 to
960 global-band floor (COMM-216) and the sim's populated-band 95% figure. The
ELEVATION MASK is the physical dial: raising the mask or lowering altitude roughly
doubles to triples the floor (COMM-217). CONFIGURABLE."""

MAX_FLEET_SATELLITES_DEFAULT: Final[int] = 2_000
"""FOUNDER_SET (2026-06-26). The SATURATION CAP on the fleet target: the largest
constellation the model will size to, the upper bound on the fleet target. Past this
the spread, low-density servable base is exhausted and adding satellites stops buying
servable subscribers (a dense cell saturates and cannot be served by adding more
satellites, the density caveat in research/direct_communication/
dtc_subscribers_per_satellite.md, COMM-535..560). The implied capacity fleets are
~1,000 to 2,000 satellites at 50M to 100M attached, so 2,000 is the cap the ~100M
ambitious target sits just under (1,334 at the 75,000 density). CONFIGURABLE."""

# ===========================================================================
# Comms cadence share (variable 2's share of the whole-fleet ramp)
# ===========================================================================

COMMS_SHARE_DEFAULT: Final[float] = 0.18
"""FOUNDER_SET (round 4, 2026-06-25). The comms slice's SHARE of the whole-fleet
Neutron cadence: ~16 of the 90 FY2036 launches/year (the 90/year is the shared
whole-fleet cadence; comms flies a share of it). The founder's ~15 to 20 band maps
to a share of ~0.167 to ~0.222; 0.18 (~16/90) is the in-band default. CONFIGURABLE.
Phase 2 applies this as a multiplier on the shared per-year integer launch count,
re-rounded to an integer with the shared half-up offset."""

# ===========================================================================
# Subscriber target + per-satellite capacity (the capacity dimension)
# ===========================================================================

SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT: Final[int] = 10_000_000
"""FOUNDER_SET (2026-06-26). The SUBSCRIBER TARGET: the base to SERVE (phone
subscribers, NOT households: cellular is per-person), the model's INPUT. The fleet
is sized to serve this base at :data:`SUBSCRIBERS_PER_SATELLITE_DEFAULT` per
satellite (the capacity dimension), so the fleet target and the cost track the base.
10,000,000 is the founder's BASELINE; 50,000,000 and 100,000,000 (the ambitious
target) are the scenarios, set per-config. A served-base figure, NOT a demand
estimate. The people-sized cellular niche basis: the ~300M global mobile
coverage-gap PEOPLE (COMM-021 / COMM-390, already a people count) plus the US and
developed-world remote/unserved layer, with any household-stated tier (e.g.
developed-ex-US ~30 to 45M households, COMM-065) converted at ~2.5 people per
household before summing. 10M is a conservative phone-shaped slice of that pool, the
founder's starting baseline. Note the served base GROWS over time. CONFIGURABLE.
This dial most moves cost-per-subscriber, so surface it as the swing dial."""

SUBSCRIBERS_PER_SATELLITE_DEFAULT: Final[int] = 75_000
"""SOURCED_ESTIMATE (COMM-535..560, research/direct_communication/
dtc_subscribers_per_satellite.md). ATTACHED subscribers per flat ~25 m^2 cellular
satellite: the central of the grounded ~50,000 to 100,000 range (with ~250 to 2,000
simultaneously ACTIVE at ~2-3% busy-hour concurrency). ~50x a Starlink BROADBAND
satellite (~1,260/sat) because a cellular subscriber sips data versus a broadband
household (Starlink's own V3 D2C plan implies ~70,000 attached/sat). On 25 MHz the
SPECTRUM binds first; the antenna POWER binds past ~50 to 100 MHz; the onboard
COMPUTATION binds last (>100 to 200 MHz), so the chip is the LEAST binding. This
density divides the subscriber target into the CAPACITY fleet need. Only the SPREAD,
low-density subscriber is servable (a dense cell saturates). CONFIGURABLE."""

# ===========================================================================
# Revenue + gross-margin dials (the two revenue cases; mirrors the DC R multiple)
# ===========================================================================

REVENUE_MULTIPLE_DEFAULT: Final[float] = 1.5
"""FOUNDER_SET (mirrors the DC central R = 1.5, research/SOURCE_INDEX.md#REV-008).
The COST-PLUS / MARGIN-TARGET revenue case: annual revenue = annual cost x this
multiple. 1.5 is cost+50%, an implied gross margin of (1.5 - 1) / 1.5 = 33.3%, the
same owner-operator margin the data-center model carries as its central R. Each
5-year cohort earns this margin across its life (the multiple is flat, no taper).
A cost-coupled revenue case (revenue tracks the cost basis), NOT a market estimate.
CONFIGURABLE."""

ARPU_USD_PER_MONTH_DEFAULT: Final[float] = 50.0
"""SCENARIO (the supportable median; documented in the assumptions). The
PRICES-TODAY / ARPU revenue case: annual revenue = served subscribers x this ARPU x
12 months. $50/month is a supportable median that sits BELOW the ~$80 to 100/month
terrestrial mobile plan (the all-in retail price a developed-market subscriber pays
today), the headroom assuming direct-to-cell prices drop toward and below today's
terrestrial floor as the service scales. A per-subscriber retail price applied to
the SERVED base, NOT a demand or willingness-to-pay estimate (the served base is the
sized model input, not a market-sizing output). CONFIGURABLE."""

MONTHS_PER_YEAR: Final[int] = 12
"""Calendar months per year, the ARPU annualization factor (monthly ARPU x this =
annual revenue per subscriber). A fixed unit-conversion constant, not a tunable."""

# ===========================================================================
# Ground interface basis label (the two-regime ground interface, Phase 4)
# ===========================================================================

GROUND_BASIS_DEFAULT: Final[str] = "annual_cost_per_subscriber"
"""SCENARIO. The like-for-like basis label for the two-regime ground interface
(Phase 4), matching the settled primary unit (cost per subscriber per year). The
Phase 4 comparison asserts the space and ground bases match before computing a
ratio, so a build-and-hold space cost is never compared against an annual ground
cost."""

# ===========================================================================
# Output schema version (Phase 5)
# ===========================================================================

SCHEMA_VERSION: Final[str] = "comms-v1"
"""The light comms-output schema version tag, surfaced in the output metadata
(Phase 5). ``v1`` is the clean-rewrite schema (no provenance envelope)."""

# ===========================================================================
# Placeholder-dial flag map (read by Phase 5 ``check_no_placeholder_inputs``)
# ===========================================================================
#
# Each guarded dial maps to a flag: True means its current default is still an
# arbitrary placeholder SENTINEL; False means a real value the founder set. The
# four founder dials below are all False (set round 4). The Phase 5 check reports
# any dial whose flag is True, so it PASSES on the default config yet still guards
# against any FUTURE dial left on a placeholder. The keys are dotted config paths
# for the report; the check does not read live config values under this mechanism.

type DialPath = str
"""A dotted ``block.field`` path naming a guarded config dial (placeholder map key)."""

PLACEHOLDER_DIAL_FLAGS: Final[dict[DialPath, bool]] = {
    "satellite.satellite_build_cost_musd": False,  # FOUNDER_SET 1.05 (not a sentinel)
    "coverage.satellites_for_full_coverage": False,  # FOUNDER_SET 340 floor (not a sentinel)
    "coverage.max_fleet_satellites": False,  # FOUNDER_SET 2,000 cap (not a sentinel)
    "comms_cadence.share_of_fleet": False,  # FOUNDER_SET 0.18 (not a sentinel)
    "subscribers.subscribers_at_full_coverage": False,  # FOUNDER_SET 10M target (not a sentinel)
    "subscribers.subscribers_per_satellite": False,  # SOURCED_ESTIMATE 75,000 (not a sentinel)
    "revenue.revenue_multiple": False,  # FOUNDER_SET 1.5 (mirrors the DC R; not a sentinel)
    "revenue.arpu_usd_per_month": False,  # SCENARIO 50.0 supportable median (not a sentinel)
}
"""FOUNDER_SET status per guarded dial. ``True`` = still an arbitrary placeholder
sentinel; ``False`` = a real founder-set (or sourced) value. All are ``False``.
``satellites_per_launch`` and ``satellite_lifetime_years`` were never placeholders,
so they are not inspected. Add a future placeholder dial here as ``True`` and the
Phase 5 check will catch it."""


__all__ = [
    "ARPU_USD_PER_MONTH_DEFAULT",
    "BASE_YEAR_DEFAULT",
    "CADENCE_CEILING_DEFAULT",
    "COMMS_SHARE_DEFAULT",
    "BindingRegime",
    "DensityRegime",
    "DialPath",
    "FIRST_LAUNCH_YEAR_DEFAULT",
    "GROUND_BASIS_DEFAULT",
    "HIGH_CADENCE_COST_MUSD_DEFAULT",
    "HIGH_CADENCE_LAUNCHES_DEFAULT",
    "HORIZON_YEARS_DEFAULT",
    "LAUNCHES_AT_YEAR_5_DEFAULT",
    "LAUNCHES_AT_YEAR_10_DEFAULT",
    "LOW_CADENCE_COST_MUSD_DEFAULT",
    "LOW_CADENCE_LAUNCHES_DEFAULT",
    "MAX_FLEET_SATELLITES_DEFAULT",
    "MAX_FY",
    "MAX_HORIZON_YEARS",
    "MIN_FY",
    "MIN_HORIZON_YEARS",
    "MONTHS_PER_YEAR",
    "PLACEHOLDER_DIAL_FLAGS",
    "REVENUE_MULTIPLE_DEFAULT",
    "ROUND_TO_NEAREST_OFFSET",
    "SATELLITES_FOR_FULL_COVERAGE_DEFAULT",
    "SATELLITES_PER_LAUNCH_DEFAULT",
    "SATELLITE_BUILD_COST_MUSD_DEFAULT",
    "SATELLITE_LIFETIME_YEARS_DEFAULT",
    "SCHEMA_VERSION",
    "SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT",
    "SUBSCRIBERS_PER_SATELLITE_DEFAULT",
]
