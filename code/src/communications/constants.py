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

The four FOUNDER-SET dials (round 4, 2026-06-25) are recorded as real default
VALUES (``satellites_for_full_coverage = 340``, ``share_of_fleet = 0.18``,
``subscribers_at_full_coverage = 50,000,000`` people, ``satellite_build_cost
= 1.05`` $M); they stay configurable. Because they are real values, the Phase 5
placeholder check CANNOT use value-equals-default as the placeholder signal (that
would false-positive on the real defaults). Instead a static per-dial flag map
(:data:`PLACEHOLDER_DIAL_FLAGS`) records, per guarded dial, whether its default
is a real founder-set value (``False``) or an arbitrary sentinel (``True``); all
four are ``False`` now. The Phase 5 ``check_no_placeholder_inputs`` reads that map.
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
"""FOUNDER_SET (round 4, 2026-06-25). The constellation-size target the build-out
fills toward: the quality-link case (a 25 degree elevation mask over the populated
mid-latitude band, +/-55 deg, at 95% coverage, ~450 km, ~53 deg inclined). Backed
by the coverage sim (.agent/other/coverage_sim/FINDINGS.md: populated band, 450 km,
25 deg mask, 95% = 341 sats, founder-rounded to 340) and the corpus (COMM-209 /
COMM-216 / COMM-217 from leo_constellation_coverage_minimums; the DTC
coverage-geography band COMM-386..COMM-405). 340 sits inside the analytic ~290 to
960 global-band floor (COMM-216) and the sim's populated-band 95% figure. The
ELEVATION MASK is the physical dial: raising the mask or lowering altitude roughly
doubles to triples the floor (COMM-217). CONFIGURABLE."""

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
# Subscriber denominator (variable for the per-PERSON cost unit)
# ===========================================================================

SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT: Final[int] = 50_000_000
"""FOUNDER_SET (round 4, 2026-06-25). The SWING DIAL. The served-PERSON count
(phone subscribers, NOT households: cellular is per-person) when coverage reaches
1.0. A coverage-driven capacity-of-coverage figure, NOT a demand estimate. The
people-sized cellular niche basis: the ~300M global mobile coverage-gap PEOPLE
(COMM-021 / COMM-390, already a people count) plus the US and developed-world
remote/unserved layer, with any household-stated tier (e.g. developed-ex-US
~30 to 45M households, COMM-065) converted at ~2.5 people per household before
summing. 50M is a conservative phone-shaped slice of that pool (well below the
~300M coverage gap), a starting point the founder can move. Note the served base
GROWS over time. CONFIGURABLE. This dial most moves cost-per-subscriber, so surface
it as the swing dial."""

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
    "coverage.satellites_for_full_coverage": False,  # FOUNDER_SET 340 (not a sentinel)
    "comms_cadence.share_of_fleet": False,  # FOUNDER_SET 0.18 (not a sentinel)
    "subscribers.subscribers_at_full_coverage": False,  # FOUNDER_SET 50M (not a sentinel)
}
"""FOUNDER_SET status per guarded dial. ``True`` = still an arbitrary placeholder
sentinel; ``False`` = a real founder-set value. All four are ``False`` (round 4,
2026-06-25). ``satellites_per_launch`` and ``satellite_lifetime_years`` were never
placeholders, so they are not inspected. Add a future placeholder dial here as
``True`` and the Phase 5 check will catch it."""


__all__ = [
    "BASE_YEAR_DEFAULT",
    "CADENCE_CEILING_DEFAULT",
    "COMMS_SHARE_DEFAULT",
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
    "MAX_FY",
    "MAX_HORIZON_YEARS",
    "MIN_FY",
    "MIN_HORIZON_YEARS",
    "PLACEHOLDER_DIAL_FLAGS",
    "ROUND_TO_NEAREST_OFFSET",
    "SATELLITES_FOR_FULL_COVERAGE_DEFAULT",
    "SATELLITES_PER_LAUNCH_DEFAULT",
    "SATELLITE_BUILD_COST_MUSD_DEFAULT",
    "SATELLITE_LIFETIME_YEARS_DEFAULT",
    "SCHEMA_VERSION",
    "SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT",
]
