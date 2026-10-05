"""Module-level ``Final`` named constants for the communications model families.

This module is the single source of truth for the comms config's "no bare
numeric literals" rule (CLAUDE.md). Every default the ``communications.config``
Pydantic blocks read lives here, each with a docstring carrying:

- A source class tag: SOURCED_FACT / SOURCED_ESTIMATE / ESTIMATE / SCENARIO /
  INVESTOR_SET / DERIVED.
- A citation: a global ``COMM-*`` claim id from ``research/SOURCE_INDEX.md``,
  a research-doc path, the coverage-sim findings, or an investor note.

The eight cadence / launch-cost defaults and their dial blocks are NOT stated
here: they live once in ``common.cadence`` (the shared spine both ventures
consume), which the comms config imports directly, so the comms cadence cannot
drift from the data-center cadence. Importing from ``common`` is not a venture
dependency. This module never imports ``data_center`` (the cross-import guard
forbids it).

The INVESTOR-SET dials are recorded as real default VALUES
(``satellites_for_full_coverage = 340`` the coverage FLOOR, ``share_of_fleet =
0.18``, ``subscribers_at_full_coverage = 10,000,000`` the subscriber TARGET,
``subscribers_per_satellite = 75,000``, ``max_fleet_satellites = 2,000``,
``satellite_build_cost = 1.05`` $M, ``revenue_multiple = 1.5`` mirroring the DC R,
``arpu_usd_per_month = 50.0`` the supportable median); they stay configurable.

CAPACITY DIMENSION (investor-directed 2026-06-26, research COMM-535..560). The model
is sized to SERVE the subscriber base, not merely to cover it. The subscriber TARGET
(``subscribers_at_full_coverage``) is the INPUT; the fleet is sized to serve it at
``subscribers_per_satellite`` attached subscribers per satellite, floored by the
coverage floor and capped by the saturation cap ``max_fleet_satellites``. The fleet
target is ``min(max_fleet_satellites, max(satellites_for_full_coverage,
ceil(subscriber_target / subscribers_per_satellite)))``.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Final

from common.input_manifest import SourceStatus

logger = logging.getLogger(__name__)

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
    subscribers_per_satellite)``. This enum records which term binds, the investor's
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


class DeviceClass(StrEnum):
    """The Iridium model (formerly Model B) device class, which sets the SE tier.

    The investor's three device categories (2026-07-07; the 9c device ladder). The
    member order is the order every list of classes takes (E11: small terminal, mounted
    terminal, phone class), so every block that lists the classes iterates this enum.
    ``SMALL_TERMINAL_CLASS`` is the small boosted antenna: paperback/puck size, ~20 cm
    integrated patch, ~10 dBi on a self-orienting mount (a fixed tilt or switched
    elements; no user pointing, no moving parts; investor decision 2026-07-10),
    purpose-built with NO chipset assumption
    (SE band 1.5 to 2.5, central :data:`SMALL_TERMINAL_CLASS_SE_CENTRAL`).
    ``MOUNTED_TERMINAL_CLASS`` is the LARGE boosted / custom-antenna tier: mounted or pointed,
    15+ dBi (drones, fixed sites, vehicles; SE band 2.0 to 3.0, central
    :data:`MOUNTED_TERMINAL_CLASS_SE_CENTRAL`).
    ``PHONE_CLASS`` is the cell phone: the 0-dBi in-chipset phone-form-factor baseline
    (SE band 0.5 to 0.8 bps/Hz, central :data:`PHONE_CLASS_SE_CENTRAL`). See the ecosystem
    assumption (:data:`ECOSYSTEM_ASSUMPTION_NOTE`): the Iridium model reaches purpose-built
    or in-chipset devices on Iridium's owned L-band (the MSS lane), NEVER an unmodified
    phone (that is the cellular lane, the High-Bandwidth Cellular Pure Play model,
    formerly Model A). The engine runs one class per run today (no mixed fleet); the
    saturation curve carries every class.
    """

    SMALL_TERMINAL_CLASS = "small_terminal_class"
    MOUNTED_TERMINAL_CLASS = "mounted_terminal_class"
    PHONE_CLASS = "phone_class"


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
scalar. The mass basis is the MISSION LEO envelope (investor steering 2026-07-10;
this constellation does not target SSO): 12 x ~800 kg = ~9,600 kg loads the
certified ~13,000 kg LEO figure (NTR-001) at 73.8 percent, a comfortable
manifest. Recorded beside it: Neutron has had no block upgrade yet, one is
likely within about five years, and no 3x-class capacity multiples are assumed.
The ~9,500 kg SSO envelope (NTR-005, a sourced estimate) is the data-center
mission's basis and stays only as that note. Estimate-bound on the
single-source ~800 kg Flatellite mass read (COMM-253 / COMM-256)."""

SATELLITE_LIFETIME_YEARS_DEFAULT: Final[int] = 5
"""ESTIMATE (COMM-088, the Starlink ~5-year depreciation and replacement
treadmill; the ~$200 to 260/sub/yr split that lineage feeds is COMM-091. The
07-08 audit's move to COMM-097 read the supply-cost doc's internal ids, which
are offset from the global index; corrected 2026-07-09). Satellite operating
life, the cohort cliff: after this many years a cohort retires and contributes
zero coverage. A design/depreciation assumption (the Starlink replacement-capex
anchor), not a certified field life."""

ORBIT_ALTITUDE_KM_SCENARIO: Final[float] = 450.0
"""SCENARIO (Part 7 physics loop, 2026-07-10). The published fleet altitude, km.
Four couplings favor about 450 km (path loss, coverage economy, the saturation
ceiling, the sun-angle power floor), robustly on the link budget and latency.
A stated scenario input to the published orbit posture, NOT an engine input: the
engine computes nothing from it. The saturation curve's shell is computed at it
(the default of ``SaturationInputs.shell.altitude_km``). The promoted artifact
carries it in the labeled ``orbit_scenario`` block (schema iridium-v4) so the
public orbit claim has a typed model-contract anchor with its limitations
attached."""

ORBIT_INCLINATION_DEG_SCENARIO: Final[float] = 53.0
"""SCENARIO (Part 7 physics loop, 2026-07-10). The published fleet inclination,
degrees. Chosen because people live at mid-latitudes: the covered band holds
about 99.6 percent of the world's population, and the project coverage
simulation needs about 10 percent fewer satellites at 53 degrees than polar
(341 versus 375 at the 95 percent threshold, 450 km, 25 degree mask). Same
posture as the altitude: a stated scenario input, not an engine input; the
saturation curve's shell is computed at it (the default of
``SaturationInputs.shell.inclination_deg``)."""

ORBIT_SCENARIO_SOURCE_STATUS: Final[SourceStatus] = SourceStatus.SCENARIO
"""The assumptions-ledger source status carried on the promoted orbit block:
the orbit is a chosen modeling assumption on a computed (simulation-informed)
basis, per the public source-status taxonomy (the shared
:class:`common.input_manifest.SourceStatus`, which communications/assumptions.md
uses)."""

ORBIT_SCENARIO_BASIS: Final[str] = (
    "Simulation-informed scenario, not an engine derivation: the project "
    "coverage simulation's 95 percent column reads 341 satellites at 450 km, "
    "53 degrees, and a 25 degree elevation mask (investor-rounded to the 340 "
    "dial), and no polar candidate below 375 passed. Honest bounds (2026-07-14 "
    "audit): a fuller integer-phasing search finds 320 passing the same stored "
    "geographic metric, the saved 341 case is the robust one under equal-area "
    "weighting, the metric is geographic rather than population-weighted, the "
    "production minimum-search screens a single phasing family, and finite "
    "sampled periods do not prove continuous operational availability. 340 is "
    "a supported conservative scenario; the exact floor is an engineering "
    "decision."
)
"""The orbit block's basis paragraph: the simulation support and every honest
bound recorded by the 2026-07-14 calculation audit, carried verbatim on the
promoted artifact so the limitations travel with the numbers."""

SATELLITE_BUILD_COST_MUSD_DEFAULT: Final[float] = 1.05
"""INVESTOR_SET (in-band; round 4, 2026-06-25). The flat MASS-MANUFACTURED
CELLULAR-SATELLITE HARDWARE cost, ONE scalar, ~$1.0 to 1.1M (1.05 is the in-band
default). This is a V3-CLASS HARDWARE analogy: the Starlink V3 per-satellite
hardware cost is ~$1.2M (~1,500 kg), the upper hardware anchor (COMM-080, the
consolidated unit-cost trajectory row). A
CELLULAR direct-to-cell payload is a bigger antenna and more power than a
broadband panel, but FAR smaller than AST's giant phased array (so AST's
~$19 to 21M giant-array figure is the WRONG anchor). It is a HARDWARE
build-cost analogy ONLY, NOT a broadband-product cost claim. CONFIGURABLE."""

# ===========================================================================
# Coverage target dial (the NEW constellation-size target, variable 3)
# ===========================================================================

SATELLITES_FOR_FULL_COVERAGE_DEFAULT: Final[int] = 340
"""INVESTOR_SET (round 4, 2026-06-25). The COVERAGE FLOOR: the minimum constellation
size for everyone in the served band to SEE a satellite (a quality link), the lower
bound on the fleet target. This is NOT the fleet the build fills toward when the
subscriber base is large: the capacity dimension (see
:data:`SUBSCRIBERS_PER_SATELLITE_DEFAULT`) can require more satellites than this to
SERVE the base, in which case the capacity need binds and the fleet target rises
above the floor. The floor is the quality-link case (a 25 degree elevation mask over
the populated mid-latitude band, +/-55 deg, at 95% coverage, ~450 km, ~53 deg
inclined). Backed by the project coverage simulation (populated band, 450 km, 25 deg
mask, 95% = 341 sats, investor-rounded to 340; the coverage-floor row of
communications/assumptions.md carries the result and its honest bounds) and the
corpus (COMM-209 / COMM-216 / COMM-217 from leo_constellation_coverage_minimums; the
DTC coverage-geography band COMM-386..COMM-405). 340 sits inside the analytic ~290 to
960 global-band floor (COMM-216) and the sim's populated-band 95% figure. The
ELEVATION MASK is the physical dial: raising the mask or lowering altitude roughly
doubles to triples the floor (COMM-217). CONFIGURABLE."""

MAX_FLEET_SATELLITES_DEFAULT: Final[int] = 2_000
"""INVESTOR_SET (2026-06-26). The SATURATION CAP on the fleet target: the largest
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
"""INVESTOR_SET (round 4, 2026-06-25). The comms slice's SHARE of the whole-fleet
Neutron cadence: ~16 of the 90 FY2036 launches/year (the 90/year is the shared
whole-fleet cadence; comms flies a share of it). The investor's ~15 to 20 band maps
to a share of ~0.167 to ~0.222; 0.18 (~16/90) is the in-band default. CONFIGURABLE.
Phase 2 applies this as a multiplier on the shared per-year integer launch count,
re-rounded to an integer with the shared half-up offset."""

# ===========================================================================
# Subscriber target + per-satellite capacity (the capacity dimension)
# ===========================================================================

SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT: Final[int] = 10_000_000
"""INVESTOR_SET (2026-06-26). The SUBSCRIBER TARGET: the base to SERVE (phone
subscribers, NOT households: cellular is per-person), the model's INPUT. The fleet
is sized to serve this base at :data:`SUBSCRIBERS_PER_SATELLITE_DEFAULT` per
satellite (the capacity dimension), so the fleet target and the cost track the base.
10,000,000 is the investor's BASELINE; 50,000,000 and 100,000,000 (the ambitious
target) are the scenarios, set per-config. A served-base figure, NOT a demand
estimate. The people-sized cellular niche basis: the ~300M global mobile
coverage-gap PEOPLE (COMM-021 / COMM-390, already a people count) plus the US and
developed-world remote/unserved layer, with any household-stated tier (e.g.
developed-ex-US ~30 to 45M households, COMM-065) converted at ~2.5 people per
household before summing. 10M is a conservative phone-shaped slice of that pool, the
investor's starting baseline. Note the served base GROWS over time. CONFIGURABLE.
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
"""INVESTOR_SET (mirrors the DC central R = 1.5, research/SOURCE_INDEX.md
RLDC-REVENUE-MULTIPLE-1_5X).
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
# The Iridium model: L-band max-outcome scenario (the MSS lane) dials + physics
# ===========================================================================
#
# The Iridium model DERIVES the per-satellite subscriber density from L-band physics
# (held spectrum, device spectral efficiency, active rate, busy-hour concurrency)
# instead of reading the High-Bandwidth Cellular Pure Play model's fixed
# ``subscribers_per_satellite`` dial, then feeds the SAME ``compute_fleet_target``.
# These are its named-constant defaults and physics calibrations. THE THREE LANES
# stay separate: the Iridium model is the MSS lane (purpose-built or in-chipset
# devices on owned L-band), NOT cellular direct-to-cell to an unmodified phone (the
# High-Bandwidth Cellular Pure Play model) and NOT broadband.

SPECTRUM_MHZ_DEFAULT: Final[float] = 8.0
"""INVESTOR_SET (flagged; session state, Iridium spectrum reconciled). The Iridium
EXCLUSIVE L-band holding (~7.775 MHz rounded to 8.0), a WIDTH held, NOT a frequency
(the frequency is the ~1.6 GHz dial position). The coordinated 10.5 MHz span (1616 to
1626.5 MHz) is a documented variant a scenario can set, not the default."""

PHONE_CLASS_SE_CENTRAL: Final[float] = 0.65
"""SOURCED_ESTIMATE (COMM-428 / COMM-429). Central of the 0.5 to 0.8 bps/Hz
phone-class spectral-efficiency band (the Starlink-D2C measured 0-dBi anchor). The
phone-class tier is the 0-dBi in-chipset baseline (the ecosystem assumption)."""

PHONE_CLASS_SE_LOW: Final[float] = 0.5
"""SOURCED_ESTIMATE (COMM-428 / COMM-429). Low edge of the documented phone-class
spectral-efficiency sweep band."""

PHONE_CLASS_SE_HIGH: Final[float] = 0.8
"""SOURCED_ESTIMATE (COMM-428 / COMM-429). High edge of the documented phone-class
spectral-efficiency sweep band."""

SMALL_TERMINAL_CLASS_SE_CENTRAL: Final[float] = 2.0
"""ESTIMATE (derived; brainstorming 9c device ladder; device spec re-based by
investor decision 2026-07-10). Central of the 1.5 to 2.5 bps/Hz band for the SMALL
boosted-antenna device: paperback/puck size, ~20 cm integrated patch, ~10 dBi on a
self-orienting mount (a fixed tilt or a few switched elements; no user pointing, no
moving parts), purpose-built so NO chipset assumption (OUR hardware; the investor's
10 to 20 Mbps tier in 9c). The mount is part of the spec because patch gain is
directional: a bare flat face-up patch realizes the full ~10 dBi only at high
elevations and slides toward phone-class at low ones (physics loop C-122 / C-213);
the self-orienting spec recovers most of the gain at typical link elevations.
Derivation anchor: phone-class SE
0.65 implies SNR ~0.57 (2 ** 0.65 - 1); +10 dB of antenna gain is SNR ~5.7; Shannon
log2(1 + 5.7) ~2.7; real systems reach ~60 to 80 percent of Shannon (~1.65 to 2.19),
so ~2.0 central."""

SMALL_TERMINAL_CLASS_SE_LOW: Final[float] = 1.5
"""ESTIMATE (brainstorming 9c). Low edge of the documented small-terminal
spectral-efficiency sweep band."""

SMALL_TERMINAL_CLASS_SE_HIGH: Final[float] = 2.5
"""ESTIMATE (brainstorming 9c). High edge of the documented small-terminal
spectral-efficiency sweep band (it meets the large tier's central; the bands overlap,
the centrals are ordered 0.65 < 2.0 < 2.5)."""

MOUNTED_TERMINAL_CLASS_SE_CENTRAL: Final[float] = 2.5
"""SOURCED_ESTIMATE (COMM-650). Central of the 2.0 to 3.0 bps/Hz band for the LARGE
boosted / custom-antenna tier: mounted or pointed, 15+ dBi (drones, fixed sites,
vehicles; the AST-class anchor). Value untouched from the corpus; wording updated for
the three-tier device ladder."""

MOUNTED_TERMINAL_CLASS_SE_LOW: Final[float] = 2.0
"""SOURCED_ESTIMATE (COMM-650). Low edge of the documented large-tier
spectral-efficiency sweep band."""

MOUNTED_TERMINAL_CLASS_SE_HIGH: Final[float] = 3.0
"""SOURCED_ESTIMATE (COMM-650). High edge of the documented large-tier
spectral-efficiency sweep band."""

REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE: Final[float] = 0.15
"""DERIVED (COMM-410 / COMM-411). The per-satellite capacity calibration, in Gbps per
(MHz x bps/Hz), at the :data:`APERTURE_REFERENCE_M2` reference aperture. It is NOT a
clean unit conversion: it folds the effective ~150x beam-count-times-frequency-reuse
multiplier of a modern digital-beamforming satellite (inside COMM-411's 130 to 200x
effective-reuse band) together with the Mbps-to-Gbps
scaling (0.15 Gbps per (MHz x bps/Hz) = 150 effective reuse x (1 Gbps / 1000 Mbps)).
CHOSEN so the corpus anchor reproduces: 25 MHz x 2.5 SE x 0.15 = 9.375 Gbps, the
central of the grounded ~5 to 15 Gbps-per-satellite range (COMM-410). It also
reproduces phone-class 8 MHz x 0.65 x 0.15 = 0.78 Gbps and terminal-class 8 MHz x 2.5
x 0.15 = 3.0 Gbps. Per-satellite capacity is this x spectrum_mhz x SE x (aperture_m2 /
:data:`APERTURE_REFERENCE_M2`)."""

ACTIVE_USER_RATE_MBPS_DEFAULT: Final[float] = 1.0
"""INVESTOR_SET (flagged; 6a input schema). The per-subscriber active data rate in
Mbps (standard smartphone activity when active); also the peak per-user rate by
construction (the service tier). The rich 2.5 Mbps tier is a documented variant a
scenario can set, not the default."""

CONCURRENCY_PEAK_DEFAULT: Final[float] = 0.025
"""INVESTOR_SET (flagged as the pair with :data:`CONCURRENCY_OFFPEAK_DEFAULT`; 6a input
schema, the DTC concurrency corpus). Busy-hour PEAK concurrency fraction (2.5% of
subscribers simultaneously active at peak)."""

CONCURRENCY_OFFPEAK_DEFAULT: Final[float] = 0.005
"""INVESTOR_SET (flagged as the pair with :data:`CONCURRENCY_PEAK_DEFAULT`; 6a input
schema, the DTC concurrency corpus). OFF-PEAK concurrency fraction (0.5% of
subscribers simultaneously active off-peak)."""

IOT_DEVICES_DEFAULT: Final[int] = 10_000_000
"""ESTIMATE (COMM-654 / COMM-659). A passthrough DEVICE counter (low end of "tens of
millions"), investor-owned (flagged). Counted as DEVICES, never folded into the people
subscriber count; it is negligible-load and contention-limited, so it has ZERO effect
on fleet sizing (its value is cosmetic on the result). SUPERSEDED WHEN THE ARPU CASE
IS ON: with a populated :class:`~communications.config.IridiumArpuDials` block, the
published IoT DEVICE count derives from the revenue mix (the IoT bucket count), and
this fixed passthrough is reported only on the None-ARPU path (one IoT truth per
artifact; see :func:`communications.engine.derive_arpu_buckets`)."""

APERTURE_REFERENCE_M2: Final[float] = 25.0
"""SOURCED_ESTIMATE (COMM-408 / COMM-410, the corpus flat ~25 m^2-class array;
official Flatellite dimensions are unpublished, and the ~800 kg MASS read is
COMM-253 / COMM-256, which do not state an area). The CALIBRATION ANCHOR: the corpus
per-satellite capacity chain (COMM-410, :data:`REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE`)
is calibrated AT this aperture, so the capacity aperture factor is aperture_m2 / this
and equals 1.0 at the default. It is ALSO the ``aperture_m2`` Field default (the dial
defaults TO the reference), and by design coincides with
:data:`APERTURE_NO_FOLD_LIMIT_M2` (all three meanings are 25.0). Capacity is linear in
aperture area (the reuse term), which is CONSERVATIVE: it ignores the additional
per-link SNR lift a larger aperture also gives (brainstorming 9c)."""

APERTURE_NO_FOLD_LIMIT_M2: Final[float] = 25.0
"""SOURCED_ESTIMATE (brainstorming 9c). The largest flat aperture that stows in
Neutron's 5.5 m fairing WITHOUT folding. Grounding: Neutron's fairing is 5.5 m payload
diameter; a 60 m^2 flat panel is ~7.7 m in its smallest square dimension, so it cannot
stow flat; folding a coherent array across hinges contradicts the Flatellite
no-deployable design (COMM-262/263); the AST precedent shows the fold path's cost (223 m^2
flies 1 per launch even on a 7 m fairing). Used ONLY by the assumptions caveat
(:data:`APERTURE_FOLD_CAVEAT_NOTE`), NEVER as a config bound: the above-limit what-if
stays computable."""

APERTURE_FOLD_CAVEAT_NOTE: Final[str] = (
    "The configured aperture exceeds the no-fold stow limit: a flat panel this large "
    "cannot stow in Neutron's 5.5 m fairing without folding, which contradicts the "
    "Flatellite no-deployable design (COMM-262/263), and the deployment-complexity penalty "
    "of folding is not otherwise modeled. This is a documented what-if caveat, not a "
    "validation error."
)
"""SCENARIO (0.8a caveat text). Emitted by the Iridium-model assumptions output when
``aperture_m2`` exceeds :data:`APERTURE_NO_FOLD_LIMIT_M2`. A documented note, not an
error, so the above-limit what-if stays computable."""

GBPS_TO_MBPS: Final[float] = 1000.0
"""Fixed unit conversion (Gbps to Mbps), the offered-load and per-user-rate
denominator scaling. A unit constant, not a tunable."""

ECOSYSTEM_ASSUMPTION_NOTE: Final[str] = (
    "The Iridium model's phone-class tier assumes phone-form-factor devices with in-chipset "
    "support for Iridium's 1616 to 1626.5 MHz L-band (0 dBi, no external antenna). A "
    "literally-unmodified 2026 phone receives nothing on this band: no phone has an "
    "L-band MSS radio and the band is not a deployed 3GPP NTN band (COMM-668 / COMM-669 "
    "/ COMM-670). Today's real in-chipset path on this band is Project Stardust "
    "(NB-IoT NTN): messaging and IoT, kbps-class, no voice (COMM-661 to COMM-676). The "
    "phone-class data-grade tier (active rate ~1 Mbps) is therefore a forward "
    "assumption: a future where standard chipsets include the band grown up from the "
    "Stardust path, 0 dBi, no external antenna, at the cost of the low phone-class SE "
    "tier (a knowingly-taken ~4x capacity haircut versus a gain terminal). "
    "Boosted-antenna devices are purpose-built (our hardware, no chipset assumption). "
    "The Iridium model is the MSS lane and never claims to reach an unmodified handset; "
    "the unmodified-phone lane stays on cellular spectrum (the High-Bandwidth Cellular "
    "Pure Play model)."
)
"""SOURCED_ESTIMATE (0.8 ecosystem assumption; COMM-661 to COMM-676). The stated
ecosystem assumption behind the Iridium model's phone-class tier, carried on the
Iridium-model result and surfaced in the assumptions output. Keeps the three lanes
separate: the Iridium model is the MSS lane, never the unmodified-phone cellular lane
(the High-Bandwidth Cellular Pure Play model)."""

IRIDIUM_OPERATIONS_COST_MUSD: Final[float] = 0.0
"""INVESTOR_SET (assumption). The Iridium model's operations cost assumed zero (the
High-Bandwidth Cellular Pure Play model carries no operations line, so the Iridium
model inherits zero): a fixed line to research and add later, stated explicitly in the
assumptions output rather than silently omitted."""

IRIDIUM_SCENARIO_NAME_DEFAULT: Final[str] = "Iridium L-band max-outcome (phone-class baseline)"
"""SCENARIO. The default Iridium-model scenario label, carried on the ``IridiumDials``
block (the optional block's single label home, mirroring ``GroundInterfaceDials``)."""

# ===========================================================================
# The Iridium four-bucket ARPU revenue case (investor-set, Sheet A, 2026-07-09)
# ===========================================================================
#
# The PUBLISHED Iridium ARPU case: four billable-connection buckets (standard
# personal / premium terminal / IoT devices / government), each a PERCENTAGE of one
# pool anchored to fleet CAPACITY (``fleet_target x subscribers_per_satellite``), so
# every bucket scales with the satellite count. The four mix percentages and the
# four monthly prices are the INVESTOR-SET dials below; the counts are DERIVED
# (:func:`communications.engine.derive_arpu_buckets`). Subscribers are PEOPLE (the
# standard and premium buckets consume the physics density); IoT are DEVICES;
# government is a contract line. The pool is a BILLABLE-CONNECTIONS accounting frame
# (Iridium's own reporting convention: its ~2.5M "billable subscribers" fold in ~2.0M
# IoT DEVICES, COMM-617), NOT one summed people population. Precedent frame: Iridium
# FY2025 billable mix (COMM-617/618/619). Sheet A (below) is the blessed default;
# Sheet B (18.7 / 2.5 / 78.55 / 0.25 at the same prices, the today's-device-ratio
# posture) is the documented alternative in ``scenarios/iridium.yaml``.

ARPU_STANDARD_MIX_PCT_DEFAULT: Final[float] = 15.0
"""INVESTOR_SET (Sheet A, 2026-07-09). The STANDARD personal (phone-class) bucket's
share of the billable-connection pool, percent. A PEOPLE bucket (it consumes the
physics density). Loosely anchored, paired with premium, on the FY2025 book's
like-for-like people share (COMM-617/618). One of the two people mixes, so its config
Field lower bound is strictly positive (``people_share`` cannot be zero)."""

ARPU_PREMIUM_MIX_PCT_DEFAULT: Final[float] = 2.0
"""INVESTOR_SET (Sheet A, 2026-07-09). The PREMIUM terminal bucket's share of the
pool, percent. A PEOPLE bucket: the gain-terminal tier (a Certus-class service on our
own hardware, COMM-618). The second of the two people mixes (strictly-positive Field
lower bound)."""

ARPU_IOT_MIX_PCT_DEFAULT: Final[float] = 82.805
"""INVESTOR_SET (Sheet A, 2026-07-09). The IoT DEVICE bucket's share of the pool,
percent: the RESIDUAL that closes the mix to 100. Counted as DEVICES, never folded
into the people count (COMM-654/659). At the baseline it implies about 51.7 million
devices, above the corpus tens-of-millions center, carried as a stated MARKET-SHAPE
assumption (contention-limited, zero fleet-sizing effect)."""

ARPU_GOVERNMENT_MIX_PCT_DEFAULT: Final[float] = 0.195
"""INVESTOR_SET (Sheet A, 2026-07-09). The GOVERNMENT bucket's share of the pool,
percent. Deliberately DE-ANCHORED from the FY2025 book's 4.8 percent down to 0.195,
calibrated so the baseline government line reproduces today's one fixed EMSS contract
(about 108 million dollars over about 121.7k connections, COMM-619) rather than
scaling a 4.8 percent share. Held uniform with the fleet as a stated scenario
assumption."""

ARPU_STANDARD_PRICE_USD_MONTH_DEFAULT: Final[float] = 15.0
"""INVESTOR_SET (Sheet A, 2026-07-09). The STANDARD personal monthly price, dollars:
the midpoint of the investor's stated 10-to-20 mass-market phone-class range
(COMM-618 context)."""

ARPU_PREMIUM_PRICE_USD_MONTH_DEFAULT: Final[float] = 100.0
"""INVESTOR_SET (Sheet A, 2026-07-09). The PREMIUM terminal monthly price, dollars:
between Iridium's reported voice/data 47 and Certus 259 for a 0.7 Mbps-class service
(COMM-618), while the modernized fleet delivers about 4 Mbps to the same buyer."""

ARPU_IOT_PRICE_USD_MONTH_DEFAULT: Final[float] = 8.0
"""INVESTOR_SET (Sheet A, 2026-07-09). The IoT DEVICE monthly price, dollars: the
investor's confirmed about-8 (Iridium's reported IoT ARPU is 7.78 today, COMM-618)."""

ARPU_GOVERNMENT_PRICE_USD_MONTH_DEFAULT: Final[float] = 74.0
"""INVESTOR_SET (Sheet A, 2026-07-09). The GOVERNMENT monthly price, dollars: today's
per-connection equivalent on the EMSS book (about 74, COMM-619)."""

ARPU_PRICE_CEILING_USD_MONTH: Final[float] = 5000.0
"""The upper Field bound on every ARPU bucket monthly price, dollars: a generous
sanity ceiling well above the Certus 259 premium anchor (COMM-618), guarding a
fat-fingered price without constraining any real MSS tier. A fixed bound, not a
tunable."""

ARPU_MIX_TOTAL_PCT: Final[float] = 100.0
"""The billable-connection mix total, percent. Two roles, one constant: the four
bucket mixes must SUM to this (the config validator, within
:data:`ARPU_MIX_SUM_EPSILON`), and the engine DIVIDES each percentage mix by this to
get its fraction of the pool (the percent-to-fraction base). A fixed unit constant,
not a tunable."""

ARPU_MIX_SUM_EPSILON: Final[float] = 1e-9
"""The absolute tolerance on the four-mix sum-to-100 validation (the config model
validator): it absorbs float representation error (e.g. 82.805 has no exact binary
form) without admitting a materially wrong sheet (a 99- or 101-sum sheet fails
loudly, off by 1.0). A fixed epsilon, not a tunable."""

# ===========================================================================
# The shipped population grid (the saturation curve's demand map, ADR 009)
# ===========================================================================

POPULATION_GRID_PATH: Final[str] = "communications/data/ghs_pop_e2030_0p25deg.npz"
"""The shipped population grid, repository-relative: people per 0.25 degree cell
(720 rows from 90N, 1440 columns from 180W, float32), the EC JRC GHS-POP R2023A
2030 projection summed from 30 arc-seconds, shared under CC BY 4.0 with its credit,
citations and the change made in ``communications/data/ATTRIBUTION.md``. The demand
map of ADR 009 (``docs/adr/009-demand-every-resident-on-a-shipped-grid.md``): every
resident of an inhabited cell. A fixed file location, not a tunable."""

POPULATION_GRID_SHA256: Final[str] = (
    "33a42880010757c1eb5c19ef6e092111753866b670d9bc38fa9e802aa8d12e25"
)
"""The SHA-256 of the grid at :data:`POPULATION_GRID_PATH` as shipped (705,701 bytes),
recorded when it was committed with ``communications/data/ATTRIBUTION.md`` (ADR 009):
the file's identity, so a reader can confirm the grid it loads is the one shipped. A
fixed identity, not a tunable."""

# ===========================================================================
# The saturation curve's inputs (ADRs 005, 008, 009): each class's usage and antenna,
# the shell and the beam, the demand map, the sweep, the trim and the bands
# ===========================================================================
#
# Every default of ``communications.saturation_curve.SaturationInputs`` lives here. The
# curve is computed with the band in full-time use (d = 1, ADR 008) at the reference
# panel :data:`APERTURE_REFERENCE_M2`; a scenario sets none of these values. The classes
# run in :class:`DeviceClass` order (small terminal, mounted terminal, phone class).

SMALL_TERMINAL_CLASS_ACTIVE_RATE_MBPS: Final[float] = 2.0
"""INVESTOR_SET (the investor's usage table, 2026-10-04). The small terminal's data rate
while its user is active, Mbps; its busy-hour load per person is this times
:data:`SMALL_TERMINAL_CLASS_CONCURRENCY_PEAK`."""

SMALL_TERMINAL_CLASS_CONCURRENCY_PEAK: Final[float] = 0.025
"""INVESTOR_SET (the investor's usage table, 2026-10-04). The small terminal's busy-hour
share: the fraction of its users active at once in the busy hour."""

SMALL_TERMINAL_CLASS_CONCURRENCY_OFFPEAK: Final[float] = 0.005
"""INVESTOR_SET (the investor's usage table, 2026-10-04). The small terminal's off-peak
share, at most its busy-hour share (off peak is the quieter hour)."""

MOUNTED_TERMINAL_CLASS_ACTIVE_RATE_MBPS: Final[float] = 5.0
"""INVESTOR_SET (the investor's usage table, 2026-10-04). The mounted terminal's data rate
while its user is active, Mbps; its busy-hour load per person is this times
:data:`MOUNTED_TERMINAL_CLASS_CONCURRENCY_PEAK`."""

MOUNTED_TERMINAL_CLASS_CONCURRENCY_PEAK: Final[float] = 0.10
"""INVESTOR_SET (the investor's usage table, 2026-10-04). The mounted terminal's busy-hour
share: the fraction of its users active at once in the busy hour."""

MOUNTED_TERMINAL_CLASS_CONCURRENCY_OFFPEAK: Final[float] = 0.02
"""INVESTOR_SET (the investor's usage table, 2026-10-04). The mounted terminal's off-peak
share, at most its busy-hour share (off peak is the quieter hour)."""

PHONE_CLASS_ACTIVE_RATE_MBPS: Final[float] = 0.75
"""INVESTOR_SET (the investor's usage table, 2026-10-04). The phone class's data rate while
its user is active, Mbps; its busy-hour load per person is this times
:data:`PHONE_CLASS_CONCURRENCY_PEAK`."""

PHONE_CLASS_CONCURRENCY_PEAK: Final[float] = 0.025
"""INVESTOR_SET (the investor's usage table, 2026-10-04). The phone class's busy-hour share:
the fraction of its users active at once in the busy hour."""

PHONE_CLASS_CONCURRENCY_OFFPEAK: Final[float] = 0.005
"""INVESTOR_SET (the investor's usage table, 2026-10-04). The phone class's off-peak share,
at most its busy-hour share (off peak is the quieter hour)."""


@dataclass(frozen=True)
class ClassUsage:
    """One device class's usage: its rate while active and its two concurrency shares.

    Attributes:
        active_rate_mbps: The data rate while a user is active, Mbps.
        concurrency_peak: The busy-hour share of users active at once.
        concurrency_offpeak: The off-peak share, at most ``concurrency_peak``.
    """

    active_rate_mbps: float
    concurrency_peak: float
    concurrency_offpeak: float


CLASS_USAGE: Final[Mapping[DeviceClass, ClassUsage]] = MappingProxyType(
    {
        DeviceClass.SMALL_TERMINAL_CLASS: ClassUsage(
            active_rate_mbps=SMALL_TERMINAL_CLASS_ACTIVE_RATE_MBPS,
            concurrency_peak=SMALL_TERMINAL_CLASS_CONCURRENCY_PEAK,
            concurrency_offpeak=SMALL_TERMINAL_CLASS_CONCURRENCY_OFFPEAK,
        ),
        DeviceClass.MOUNTED_TERMINAL_CLASS: ClassUsage(
            active_rate_mbps=MOUNTED_TERMINAL_CLASS_ACTIVE_RATE_MBPS,
            concurrency_peak=MOUNTED_TERMINAL_CLASS_CONCURRENCY_PEAK,
            concurrency_offpeak=MOUNTED_TERMINAL_CLASS_CONCURRENCY_OFFPEAK,
        ),
        DeviceClass.PHONE_CLASS: ClassUsage(
            active_rate_mbps=PHONE_CLASS_ACTIVE_RATE_MBPS,
            concurrency_peak=PHONE_CLASS_CONCURRENCY_PEAK,
            concurrency_offpeak=PHONE_CLASS_CONCURRENCY_OFFPEAK,
        ),
    }
)
"""INVESTOR_SET (the investor's usage table, 2026-10-04). Each class's usage, one entry per
:class:`DeviceClass` in its order, read-only: the named constants above, assembled."""

CLASS_SE_CENTRAL: Final[Mapping[DeviceClass, float]] = MappingProxyType(
    {
        DeviceClass.SMALL_TERMINAL_CLASS: SMALL_TERMINAL_CLASS_SE_CENTRAL,
        DeviceClass.MOUNTED_TERMINAL_CLASS: MOUNTED_TERMINAL_CLASS_SE_CENTRAL,
        DeviceClass.PHONE_CLASS: PHONE_CLASS_SE_CENTRAL,
    }
)
"""Each class's central spectral efficiency, bps/Hz, one entry per :class:`DeviceClass` in
its order, read-only: the one home the saturation curve reads. Each value keeps its own
constant's source class (:data:`SMALL_TERMINAL_CLASS_SE_CENTRAL`,
:data:`MOUNTED_TERMINAL_CLASS_SE_CENTRAL`, :data:`PHONE_CLASS_SE_CENTRAL`)."""

SMALL_TERMINAL_CLASS_DIRECTIVITY_DBI: Final[float] = 10.0
"""INVESTOR_SET (the device spec of 2026-07-10, as :data:`SMALL_TERMINAL_CLASS_SE_CENTRAL`
states). The small terminal's antenna directivity, dBi: a ~20 cm integrated patch on a
self-orienting mount. It sets the terminal's beamwidth and its sky sectors."""

MOUNTED_TERMINAL_CLASS_DIRECTIVITY_DBI: Final[float] = 15.0
"""INVESTOR_SET (the device ladder's 15+ dBi tier, taken at its floor; COMM-650 for the
tier's SE band). The mounted terminal's antenna directivity, dBi: a mounted or pointed
antenna. It sets the terminal's beamwidth and its sky sectors."""

PHONE_CLASS_DIRECTIVITY_DBI: Final[float] = 0.0
"""SOURCED_ESTIMATE (COMM-428 / COMM-429). The phone class's antenna directivity, dBi: the
0 dBi in-chipset antenna of a phone-form-factor device (COMM-429: a weak terminal, about
0.2 W into about 0 dBi), which cannot tell satellites apart, so one co-channel layer
serves a place."""

SMALL_TERMINAL_CLASS_SECTOR_WEDGES_PER_RING: Final[tuple[int, ...]] = (1, 2)
"""DERIVED (the saturation design's rule D1, from
:data:`SMALL_TERMINAL_CLASS_DIRECTIVITY_DBI`). The small terminal's sky above the
elevation mask in sectors of equal solid angle, ring by ring from the zenith: a zenith cap,
then one ring in two azimuth halves. A beam of directivity D spans about 4 pi / D sr, so
about 3 such beams fit in the sky above the mask, one per sector."""

MOUNTED_TERMINAL_CLASS_SECTOR_WEDGES_PER_RING: Final[tuple[int, ...]] = (1, 3, 5)
"""DERIVED (the saturation design's rule D1, from
:data:`MOUNTED_TERMINAL_CLASS_DIRECTIVITY_DBI`). The mounted terminal's sky above the
elevation mask in sectors of equal solid angle, ring by ring from the zenith: a zenith cap,
a ring of 3, then a ring of 5 down to the mask. About 9 of its beams fit in the sky above
the mask, one per sector."""

PHONE_CLASS_SECTOR_WEDGES_PER_RING: Final[tuple[int, ...]] = ()
"""DERIVED (the saturation design's rule D1, from :data:`PHONE_CLASS_DIRECTIVITY_DBI`). No
sky sectors: a 0 dBi device takes one co-channel layer, so co-channel footprints on the
same ground must not overlap."""

SATURATION_SE_ANCHOR_BPS_PER_HZ: Final[float] = 0.65
"""SOURCED_ESTIMATE (COMM-428 / COMM-429). The anchor of the curve's link mapping, SE =
anchor x log2(1 + SINR), bps/Hz: a 0 dBi device at the measured median SINR of 0 dB
(COMM-429) reads it. Each directional class's single-layer SINR follows from its central SE
through it."""

TERMINAL_PATTERN_FLOOR_DB: Final[float] = -20.0
"""ESTIMATE (COMM-718, a ``scenario`` row: an engineering choice, not investor-set). The
directional terminals' pattern floor, dB below the main-lobe peak, under a Gaussian main
lobe; optimistic for the small terminal, whose side levels may sit at -10 to -15 dB."""

ELEVATION_MASK_DEG: Final[float] = 25.0
"""SCENARIO (the coverage floor's basis: the coverage-floor row of
``communications/assumptions.md``, the project coverage simulation at a 25 degree mask;
COMM-217 for how the mask moves the floor). The lowest elevation at which a device uses a
satellite, degrees: it sets the view's central-angle limit and the largest footprint."""

CARRIER_FREQUENCY_HZ: Final[float] = 1.621e9
"""DERIVED (COMM-611). The carrier, Hz: the centre of Iridium's 1616 to 1626.5 MHz L-band
block (1,621.25 MHz) to four figures. With the aperture it sets the beam's width."""

UNIFORM_BEAMWIDTH_FACTOR: Final[float] = 0.886
"""SOURCED_FACT (standard antenna theory). The half-power beamwidth of a uniformly
illuminated aperture, in wavelengths over the aperture's side: the curve's central beam
(uniform illumination, co-channel footprints touching)."""

DEMAND_DENSITY_THRESHOLD_PER_KM2: Final[float] = 1.0
"""SCENARIO (ADR 009). A grid cell is demand when it holds at least this many people per
km^2; the band points :data:`BAND_DENSITY_THRESHOLD_10_PER_KM2` and
:data:`BAND_DENSITY_THRESHOLD_100_PER_KM2` sit beside it."""

DEMAND_TAKE_UP: Final[float] = 1.0
"""SCENARIO (ADR 009). The share of an inhabited cell's residents counted as potential
users: every resident, the maximal-demand bound, since the capacity the curve finds is
assumed used (the model has no purchase or market model)."""

SATURATION_FLEETS: Final[tuple[int, ...]] = (
    340,
    500,
    750,
    1_000,
    1_500,
    2_000,
    3_000,
    4_000,
    5_400,
    6_000,
    8_000,
    10_000,
    12_000,
    14_000,
    16_000,
    18_000,
    20_000,
    22_000,
    24_000,
    26_000,
    28_000,
    30_000,
    34_000,
    40_000,
)
"""SCENARIO (the saturation design's fleet grid, a design rule). The requested fleets every
class's curve is computed at: from the coverage floor (340) to 40,000, dense where the
markers fall. A curve's rows are keyed by the realized fleet, P x S."""

SATURATION_MOUNTED_TERMINAL_EXTENSION: Final[tuple[int, ...]] = (48_000, 64_000)
"""SCENARIO (the saturation design's fleet grid, a design rule). The mounted terminal's
two requested fleets past :data:`SATURATION_FLEETS`, whose rows its 0.10 crossing needs,
since its narrow beam keeps stacking useful layers to near the common grid's end."""

SATURATION_SNAPSHOTS_PHONE_CENTRAL: Final[int] = 4
"""SCENARIO (design rule). The snapshot times averaged at each fleet of the phone class's
central curve."""

SATURATION_SNAPSHOTS_DIRECTIONAL: Final[int] = 2
"""SCENARIO (design rule). The snapshot times averaged at each fleet of the two directional
classes' curves."""

SATURATION_SNAPSHOTS_BANDS: Final[int] = 2
"""SCENARIO (design rule). The snapshot times averaged at each fleet of a band point's
curve."""

SATURATION_SNAPSHOTS_TRIM: Final[int] = 1
"""SCENARIO (design rule). The snapshots the interference trim prices at each row: the
first of the draw."""

SATURATION_SEED: Final[int] = 20260928
"""SCENARIO (design rule). The seed of the snapshot draw, numpy's
``default_rng(seed).uniform`` over one sidereal day, drawn once per run and shared by every
fleet, so a run repeats exactly."""

SATURATION_FOOTPRINT_BANDS: Final[int] = 40
"""SCENARIO (the saturation design's allocation rule). Smallest footprint first fills each
snapshot's satellite-cell pairs in this many geometric footprint bands, committing each
band before the next."""

SATURATION_PASSES: Final[int] = 4
"""SCENARIO (the saturation design's allocation rule). The alternating proportional
passes inside each footprint band: each scales the band's beams by every satellite's
remaining beams, then by every cell's remaining area and people."""

SATURATION_STALL_FLOOR: Final[float] = 0.98
"""SCENARIO (design rule). From 20,000 satellites up the phone class's useful beams must
reach at least this share of min(ceiling, supply) at every snapshot, so a stalled
allocation cannot fake a plateau."""

TRIM_VICTIMS: Final[int] = 3_000
"""SCENARIO (design rule). The served cells the interference trim samples at each row,
drawn without replacement in proportion to their beams."""

TRIM_SEED: Final[int] = 11
"""SCENARIO (design rule). The seed of each row's fresh victim draw, so a row does not
depend on the order of the fleets."""

TRIM_FLOOR_CONSERVATIVE_DBI: Final[float] = -0.4
"""DERIVED (COMM-715). The panel's conservative far-sidelobe floor, dBi: the interference
trim's conservative edge."""

TRIM_FLOOR_CALIBRATED_HIGH_DBI: Final[float] = -2.0
"""DERIVED (COMM-716). The high end of a calibrated array's far-sidelobe band, dBi."""

TRIM_FLOOR_CALIBRATED_LOW_DBI: Final[float] = -8.0
"""DERIVED (COMM-716). The low end of a calibrated array's far-sidelobe band, dBi."""

TRIM_FLOORS_DBI: Final[tuple[float, ...]] = (
    TRIM_FLOOR_CONSERVATIVE_DBI,
    TRIM_FLOOR_CALIBRATED_HIGH_DBI,
    TRIM_FLOOR_CALIBRATED_LOW_DBI,
)
"""DERIVED (COMM-715, COMM-716). The far-sidelobe floors the interference trim is reported
at: the conservative edge, then the calibrated band's two ends."""

TRIM_SCAN_EXPONENT: Final[float] = 1.3
"""ESTIMATE (COMM-717, a ``scenario`` row: an engineering choice, not investor-set). The
exponent of the array's scan roll-off, g = cos^exponent of the scan angle, weighting each
beam's power and sidelobes in the interference trim."""

TAPER_BEAMWIDTH_FACTOR: Final[float] = 1.0934
"""DERIVED (COMM-720). The tapered array's half-power beamwidth, in wavelengths over the
aperture's side, against the uniform :data:`UNIFORM_BEAMWIDTH_FACTOR`: its footprint is
1.52 times the uniform beam's. The band's taper point."""

SPACING_AREA_FACTOR_TOUCHING: Final[float] = 1.0
"""SCENARIO (design rule). The ground area a co-channel beam occupies over its 3 dB
footprint when co-channel footprints touch: the central curve's, and every band point's but
the spaced one."""

SPACING_AREA_FACTOR_WIDE: Final[float] = 1.5
"""ESTIMATE (COMM-721, a ``scenario`` row: an engineering choice, not investor-set). Wider
co-channel spacing gives each beam this times its ground area; the band's third point,
with the taper."""

BAND_DENSITY_THRESHOLD_10_PER_KM2: Final[float] = 10.0
"""SCENARIO (ADR 009: the curve's bands carry the density thresholds' spread). A band
point's demand threshold, people per km^2."""

BAND_DENSITY_THRESHOLD_100_PER_KM2: Final[float] = 100.0
"""SCENARIO (ADR 009: the curve's bands carry the density thresholds' spread). A band
point's demand threshold, people per km^2."""

GRID_AGGREGATION_SHIPPED: Final[int] = 1
"""SCENARIO (ADR 009). The shipped grid as it is (no aggregation): the central curve's and
every band point's but the coarse-grid one."""

GRID_AGGREGATION_0P5_DEG: Final[int] = 2
"""SCENARIO (ADR 009: the curve's bands carry the grid's spread). The coarse-grid band
point: the shipped 0.25 degree grid summed 2 x 2 into 0.5 degree cells."""

IRIDIUM_NEXT_BEAMS_PER_SATELLITE: Final[int] = 48
"""SOURCED_FACT (COMM-635). Iridium NEXT's single L-band phased array forms 48 beams
(Starlink's flying direct-to-cell array forms 48 too, COMM-408): the band's low beam
count, against the central count the calibration derives at the reference panel."""

__all__ = [
    "ARPU_USD_PER_MONTH_DEFAULT",
    "BASE_YEAR_DEFAULT",
    "COMMS_SHARE_DEFAULT",
    "BindingRegime",
    "DensityRegime",
    "GROUND_BASIS_DEFAULT",
    "HORIZON_YEARS_DEFAULT",
    "MAX_FLEET_SATELLITES_DEFAULT",
    "MAX_FY",
    "MAX_HORIZON_YEARS",
    "MIN_FY",
    "MIN_HORIZON_YEARS",
    "MONTHS_PER_YEAR",
    "REVENUE_MULTIPLE_DEFAULT",
    "SATELLITES_FOR_FULL_COVERAGE_DEFAULT",
    "SATELLITES_PER_LAUNCH_DEFAULT",
    "SATELLITE_BUILD_COST_MUSD_DEFAULT",
    "SATELLITE_LIFETIME_YEARS_DEFAULT",
    "SCHEMA_VERSION",
    "SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT",
    "SUBSCRIBERS_PER_SATELLITE_DEFAULT",
    # Iridium-model (L-band max-outcome) additions.
    "ACTIVE_USER_RATE_MBPS_DEFAULT",
    "APERTURE_FOLD_CAVEAT_NOTE",
    "APERTURE_NO_FOLD_LIMIT_M2",
    "APERTURE_REFERENCE_M2",
    # The Iridium four-bucket ARPU revenue case (Sheet A, investor-set 2026-07-09).
    "ARPU_GOVERNMENT_MIX_PCT_DEFAULT",
    "ARPU_GOVERNMENT_PRICE_USD_MONTH_DEFAULT",
    "ARPU_IOT_MIX_PCT_DEFAULT",
    "ARPU_IOT_PRICE_USD_MONTH_DEFAULT",
    "ARPU_MIX_SUM_EPSILON",
    "ARPU_MIX_TOTAL_PCT",
    "ARPU_PREMIUM_MIX_PCT_DEFAULT",
    "ARPU_PREMIUM_PRICE_USD_MONTH_DEFAULT",
    "ARPU_PRICE_CEILING_USD_MONTH",
    "ARPU_STANDARD_MIX_PCT_DEFAULT",
    "ARPU_STANDARD_PRICE_USD_MONTH_DEFAULT",
    "CONCURRENCY_OFFPEAK_DEFAULT",
    "CONCURRENCY_PEAK_DEFAULT",
    "DeviceClass",
    "ECOSYSTEM_ASSUMPTION_NOTE",
    "GBPS_TO_MBPS",
    "IOT_DEVICES_DEFAULT",
    "IRIDIUM_OPERATIONS_COST_MUSD",
    "IRIDIUM_SCENARIO_NAME_DEFAULT",
    "MOUNTED_TERMINAL_CLASS_SE_CENTRAL",
    "MOUNTED_TERMINAL_CLASS_SE_HIGH",
    "MOUNTED_TERMINAL_CLASS_SE_LOW",
    "PHONE_CLASS_SE_CENTRAL",
    "PHONE_CLASS_SE_HIGH",
    "PHONE_CLASS_SE_LOW",
    "REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE",
    "SMALL_TERMINAL_CLASS_SE_CENTRAL",
    "SMALL_TERMINAL_CLASS_SE_HIGH",
    "SMALL_TERMINAL_CLASS_SE_LOW",
    "SPECTRUM_MHZ_DEFAULT",
    # The shipped population grid (ADR 009).
    "POPULATION_GRID_PATH",
    "POPULATION_GRID_SHA256",
    # The saturation curve's inputs (ADRs 005, 008, 009).
    "BAND_DENSITY_THRESHOLD_100_PER_KM2",
    "BAND_DENSITY_THRESHOLD_10_PER_KM2",
    "CARRIER_FREQUENCY_HZ",
    "CLASS_SE_CENTRAL",
    "CLASS_USAGE",
    "ClassUsage",
    "DEMAND_DENSITY_THRESHOLD_PER_KM2",
    "DEMAND_TAKE_UP",
    "ELEVATION_MASK_DEG",
    "GRID_AGGREGATION_0P5_DEG",
    "GRID_AGGREGATION_SHIPPED",
    "IRIDIUM_NEXT_BEAMS_PER_SATELLITE",
    "MOUNTED_TERMINAL_CLASS_ACTIVE_RATE_MBPS",
    "MOUNTED_TERMINAL_CLASS_CONCURRENCY_OFFPEAK",
    "MOUNTED_TERMINAL_CLASS_CONCURRENCY_PEAK",
    "MOUNTED_TERMINAL_CLASS_DIRECTIVITY_DBI",
    "MOUNTED_TERMINAL_CLASS_SECTOR_WEDGES_PER_RING",
    "PHONE_CLASS_ACTIVE_RATE_MBPS",
    "PHONE_CLASS_CONCURRENCY_OFFPEAK",
    "PHONE_CLASS_CONCURRENCY_PEAK",
    "PHONE_CLASS_DIRECTIVITY_DBI",
    "PHONE_CLASS_SECTOR_WEDGES_PER_RING",
    "SATURATION_FLEETS",
    "SATURATION_FOOTPRINT_BANDS",
    "SATURATION_MOUNTED_TERMINAL_EXTENSION",
    "SATURATION_PASSES",
    "SATURATION_SE_ANCHOR_BPS_PER_HZ",
    "SATURATION_SEED",
    "SATURATION_SNAPSHOTS_BANDS",
    "SATURATION_SNAPSHOTS_DIRECTIONAL",
    "SATURATION_SNAPSHOTS_PHONE_CENTRAL",
    "SATURATION_SNAPSHOTS_TRIM",
    "SATURATION_STALL_FLOOR",
    "SMALL_TERMINAL_CLASS_ACTIVE_RATE_MBPS",
    "SMALL_TERMINAL_CLASS_CONCURRENCY_OFFPEAK",
    "SMALL_TERMINAL_CLASS_CONCURRENCY_PEAK",
    "SMALL_TERMINAL_CLASS_DIRECTIVITY_DBI",
    "SMALL_TERMINAL_CLASS_SECTOR_WEDGES_PER_RING",
    "SPACING_AREA_FACTOR_TOUCHING",
    "SPACING_AREA_FACTOR_WIDE",
    "TAPER_BEAMWIDTH_FACTOR",
    "TERMINAL_PATTERN_FLOOR_DB",
    "TRIM_FLOOR_CALIBRATED_HIGH_DBI",
    "TRIM_FLOOR_CALIBRATED_LOW_DBI",
    "TRIM_FLOOR_CONSERVATIVE_DBI",
    "TRIM_FLOORS_DBI",
    "TRIM_SCAN_EXPONENT",
    "TRIM_SEED",
    "TRIM_VICTIMS",
    "UNIFORM_BEAMWIDTH_FACTOR",
]
