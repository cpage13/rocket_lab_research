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
``arpu_usd_per_month = 50.0`` the supportable median); they stay configurable on a
cellular config. On an Iridium config the cellular sizing and revenue dials keep these
defaults (the config refuses another value) and the coverage floor is pinned at 340.

CAPACITY DIMENSION, the cellular family's (investor-directed 2026-06-26, research
COMM-535..560). The High-Bandwidth Cellular Pure Play model is sized to SERVE its
subscriber base, not merely to cover it. The subscriber TARGET
(``subscribers_at_full_coverage``) is the INPUT; the fleet is sized to serve it at
``subscribers_per_satellite`` attached subscribers per satellite, floored by the
coverage floor and capped by the cellular family's fleet cap ``max_fleet_satellites``.
The fleet target is ``min(max_fleet_satellites, max(satellites_for_full_coverage,
ceil(subscriber_target / subscribers_per_satellite)))``.

THE IRIDIUM MODEL has no target and no cap: its fleet is every comms launch the cadence
share allows, each device class's people are read from the promoted saturation curve, and
its defaults are below: the five monthly prices, the panel, each class's usage and
spectral efficiency, the two IoT lines' fixed counts, and the IoT reading's constants.
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
    """The cellular family's regime: which constraint sets its fleet target.

    The High-Bandwidth Cellular Pure Play model's fleet target is
    ``min(max_fleet_satellites, max(coverage_floor, capacity_need))`` where
    ``capacity_need = ceil(subscriber_target / subscribers_per_satellite)``, its fixed
    per-satellite density dial. This enum records which term binds, the investor's
    coverage-vs-capacity question for that family (the Iridium model has no target, so no
    regime):

    * ``COVERAGE`` -- the coverage floor binds (``capacity_need <= coverage_floor``);
      the subscriber base is small enough that covering the globe needs more
      satellites than serving the base does (the ~10M baseline, where 134 capacity
      satellites are below the 340 coverage floor).
    * ``CAPACITY`` -- the capacity need binds (``coverage_floor < capacity_need <
      max_fleet_satellites``); serving the base needs more satellites than coverage
      does (the ~50M and ~100M scenarios).
    * ``SATURATED`` -- the cellular fleet cap binds (``capacity_need >=
      max_fleet_satellites``); the base would need more satellites than the cap
      allows, so the fleet pins at the cap and the served base is capacity-limited. The
      cap is an investor setting of the cellular family, never a derived spectrum bound
      (an Iridium class's saturation number is that, ADR 005).
    """

    COVERAGE = "coverage"
    CAPACITY = "capacity"
    SATURATED = "saturated"


class DeviceClass(StrEnum):
    """The Iridium model's device classes: the key that names each class (never a setting).

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
    formerly Model A). One Iridium run reports every class side by side, each class's
    column the whole fleet sold to that class alone; the saturation curve carries every
    class, and each class's usage and central spectral efficiency are named constants
    (:data:`CLASS_USAGE`, :data:`CLASS_SE_CENTRAL`).
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
"""SCENARIO. Default analysis horizon (FY2026 + 10 = FY2036, the horizon's final
year), matching the DC model's 10-year horizon."""

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
single-source ~800 kg Flatellite mass read (COMM-253 / COMM-256). The cellular family's
default; the Iridium scenario sets 16 on the bound, the validated Flatellite stack with the
Neutron block upgrade assumed (COMM-713; 15 without it, COMM-712), which the
``satellites_per_launch`` field's description states."""

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
The physics loop weighed four couplings (path loss, coverage economy, the altitude
dependence of the all-lit interference wall, which the saturation module replaces,
and the sun-angle power floor) and favors about 450 km robustly on the link budget and
latency. A stated scenario input to the published orbit posture, set by no config
dial: the saturation curve's shell is computed at it (the default of
``SaturationInputs.shell.altitude_km``), so the readings the Iridium model takes from
the curve rest on it; nothing else computes from it. The promoted artifact carries it
in the labeled ``orbit_scenario`` block (schema iridium-v4) so the public orbit claim
has a typed model-contract anchor with its limitations attached."""

ORBIT_INCLINATION_DEG_SCENARIO: Final[float] = 53.0
"""SCENARIO (Part 7 physics loop, 2026-07-10). The published fleet inclination,
degrees. Chosen because people live at mid-latitudes: the covered band holds
about 99.6 percent of the world's population, and the project coverage
simulation needs about 10 percent fewer satellites at 53 degrees than polar
(341 versus 375 at the 95 percent threshold, 450 km, 25 degree mask). Same
posture as the altitude: a stated scenario input, set by no config dial; the
saturation curve's shell is computed at it (the default of
``SaturationInputs.shell.inclination_deg``)."""

ORBIT_SCENARIO_SOURCE_STATUS: Final[SourceStatus] = SourceStatus.SCENARIO
"""The assumptions-ledger source status carried on the promoted orbit block:
the orbit is a chosen modeling assumption on a computed (simulation-informed)
basis, per the public source-status taxonomy (the shared
:class:`common.input_manifest.SourceStatus`, which communications/assumptions.md
uses)."""

ORBIT_SCENARIO_BASIS: Final[str] = (
    "Simulation-informed scenario, set by no config dial (the saturation curve's "
    "shell is computed at it): the project "
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
size for everyone in the served band to SEE a satellite (a quality link). In the cellular
family it is the lower bound on the fleet target, NOT the fleet the build fills toward
when the subscriber base is large: the capacity dimension (see
:data:`SUBSCRIBERS_PER_SATELLITE_DEFAULT`) can require more satellites than this to
SERVE the base, in which case the capacity need binds and the fleet target rises
above the floor. On the Iridium path it is pinned at this value (one shell, one floor;
the IoT counts are sized at it, ADR 007): nothing is sold in a year whose living fleet
is below it, and it is the first of the reported fleets. The floor is the quality-link
case (a 25 degree elevation mask over
the populated mid-latitude band, +/-55 deg, at 95% coverage, ~450 km, ~53 deg
inclined). Backed by the project coverage simulation (populated band, 450 km, 25 deg
mask, 95% = 341 sats, investor-rounded to 340; the coverage-floor row of
communications/assumptions.md carries the result and its honest bounds) and the
corpus (COMM-209 / COMM-216 / COMM-217 from leo_constellation_coverage_minimums; the
DTC coverage-geography band COMM-386..COMM-405). 340 sits inside the analytic ~290 to
960 global-band floor (COMM-216) and the sim's populated-band 95% figure. The
ELEVATION MASK is the physical dial: raising the mask or lowering altitude roughly
doubles to triples the floor (COMM-217). CONFIGURABLE on a cellular config."""

MAX_FLEET_SATELLITES_DEFAULT: Final[int] = 2_000
"""INVESTOR_SET (2026-06-26). The cellular family's FLEET CAP on its fleet target: the
largest constellation the High-Bandwidth Cellular Pure Play model will size to, the upper
bound on its fleet target, never a saturation cap. Past this the spread, low-density
servable base is exhausted and adding satellites stops buying servable subscribers (a
dense cell saturates and cannot be served by adding more satellites, the density caveat in
research/direct_communication/dtc_subscribers_per_satellite.md, COMM-535..560). The
implied capacity fleets are ~1,000 to 2,000 satellites at 50M to 100M attached, so 2,000
is the cap the ~100M ambitious target sits just under (1,334 at the 75,000 density).
CONFIGURABLE on a cellular config. The Iridium path has no cap: an Iridium config keeps
this default and nothing reads it there; the 2,000 the Iridium model once inherited is a
reading kept for comparison (:data:`RETIRED_CAP_READING_FLEET`), and each device class's
spectrum bound is its saturation number (ADR 005)."""

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
# The Iridium model: L-band max-outcome scenario (the MSS lane) dials + physics
# ===========================================================================
#
# The Iridium model reads each device class's people from the promoted saturation curve
# (useful co-channel beams over people, computed once at the reference panel and the held
# spectrum), on the fleet the comms share of the launch cadence builds, with every seat
# sold at the class's flat price. These are its named-constant defaults and physics
# calibrations. THE THREE LANES stay separate: the Iridium model is the MSS lane
# (purpose-built or in-chipset devices on owned L-band), NOT cellular direct-to-cell to an
# unmodified phone (the High-Bandwidth Cellular Pure Play model) and NOT broadband.

SPECTRUM_MHZ_DEFAULT: Final[float] = 8.0
"""INVESTOR_SET (flagged; session state, Iridium spectrum reconciled). The Iridium
EXCLUSIVE L-band holding (~7.775 MHz rounded to 8.0), a WIDTH held, NOT a frequency
(the frequency is the ~1.6 GHz dial position). The saturation curve is computed at it, so
the curve's identity check refuses a run at another width unless the scenario's curve
path names a curve computed for that width. The coordinated 10.5 MHz span (1616 to 1626.5
MHz) is not modeled: it is a conclusions note (linear in spectrum, about +31 percent)."""

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
reproduces the phone class's 8 MHz x 0.65 x 0.15 = 0.78 Gbps and the mounted terminal's
8 MHz x 2.5 x 0.15 = 3.0 Gbps. A satellite's peak (every beam lit and used, the band full
time) is this x spectrum_mhz x SE x the panel factor (``aperture_m2`` /
:data:`APERTURE_REFERENCE_M2`); the saturation curve's beams per satellite derive from it
(``SaturationInputs.shell``)."""

APERTURE_REFERENCE_M2: Final[float] = 25.0
"""SOURCED_ESTIMATE (COMM-408 / COMM-410, the corpus flat ~25 m^2-class array;
official Flatellite dimensions are unpublished, and the ~800 kg MASS read is
COMM-253 / COMM-256, which do not state an area). The CALIBRATION ANCHOR and the
saturation curve's computation basis: the corpus per-satellite capacity chain (COMM-410,
:data:`REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE`) is calibrated AT this panel, and the curve is
computed at it (``SaturationInputs.shell.reference_aperture_m2``). The Iridium model scales
the curve and the satellite's peak linearly by the scenario's ``aperture_m2`` over this,
the panel factor (0.616 at the default :data:`APERTURE_M2_DEFAULT`). The linear rule is
conservative only above this panel, where it ignores the per-link SNR lift a larger panel
also gives; below it the curve's stated limits apply (the directional classes carry more
than the rule gives, the rule is exact in beams for the phone class, and each beam's rate
is held at its value here)."""

APERTURE_M2_DEFAULT: Final[float] = 15.4
"""DERIVED (COMM-711; the investor's approved default, 2026-10-03). The Iridium model's
panel, m^2: the validated Flatellite body, a chamfered near-square octagon about 4.1 by
4.0 m sized to Neutron's 4.79 m usable lower fairing band (calculation C, 15.40 m^2;
validation D, 15.42 m^2). An upper bound: the body's corners touch the envelope (14.0 to
15.4 m^2 with clearance). Applied linearly on the curve, a panel factor of 15.4 / 25 =
0.616."""

APERTURE_VALIDATED_STACK_LIMIT_M2: Final[float] = 15.4
"""DERIVED (COMM-711, COMM-713). The largest flat panel the validated 16-satellite
Flatellite stack holds, m^2: the stack kept in the fairing's cylinder at calculation C's
pitch carries panels up to this size (calculation C, 15.40 m^2), so it equals
:data:`APERTURE_M2_DEFAULT` by the investor's choice of the validated panel. A larger panel
exceeds the validated stack at the scenario's satellites per launch and needs its own stack
calculation, which the model does not make: the assumptions then carry
:data:`APERTURE_STACK_CAVEAT_NOTE`. Used only by that caveat, never as a config bound, so a
larger panel stays computable. The single 25 m^2 panel stowed edge-wise, one satellite per
launch (the July 2026 physics loop's supported case), is a different configuration, which
this limit does not describe."""

APERTURE_STACK_CAVEAT_NOTE: Final[str] = (
    "The configured panel exceeds the largest flat panel the validated Flatellite stack "
    f"holds ({APERTURE_VALIDATED_STACK_LIMIT_M2} m^2, COMM-711, COMM-713): at the "
    "scenario's satellites per launch it needs its own stack calculation, which the model "
    f"does not make. The single {APERTURE_REFERENCE_M2:g} m^2 panel stowed edge-wise, one "
    "satellite per launch, is a different configuration. A documented caveat, not a "
    "validation error."
)
"""SCENARIO (the caveat text). Stated in the Iridium model's assumptions when
``aperture_m2`` exceeds :data:`APERTURE_VALIDATED_STACK_LIMIT_M2`, and not at it. A
documented note, not an error, so a larger panel stays computable."""

GBPS_TO_MBPS: Final[float] = 1000.0
"""Fixed unit conversion (Gbps to Mbps), the offered-load and per-user-rate
denominator scaling. A unit constant, not a tunable."""

HZ_PER_MHZ: Final[float] = 1_000_000.0
"""Fixed unit conversion (MHz to Hz): the held width over the IoT tone's width counts the
tones. A unit constant, not a tunable."""

SECONDS_PER_DAY: Final[int] = 86_400
"""Fixed unit conversion: a day's seconds, for the IoT reading's daily volumes and access
rates. A unit constant, not a tunable."""

BITS_PER_BYTE: Final[int] = 8
"""Fixed unit conversion: bits in a byte, for the IoT reading's daily volumes. A unit
constant, not a tunable."""

ECOSYSTEM_ASSUMPTION_NOTE: Final[str] = (
    "The Iridium model's phone-class tier assumes phone-form-factor devices with in-chipset "
    "support for Iridium's 1616 to 1626.5 MHz L-band (0 dBi, no external antenna). A "
    "literally-unmodified 2026 phone receives nothing on this band: no phone has an "
    "L-band MSS radio and the band is not a deployed 3GPP NTN band (COMM-668 / COMM-669 "
    "/ COMM-670). Today's real in-chipset path on this band is Project Stardust "
    "(NB-IoT NTN): messaging and IoT, kbps-class, no voice (COMM-661 to COMM-676). The "
    "phone class's data-grade service (its own usage, a named constant) is therefore a "
    "forward assumption: a future where standard chipsets include the band grown up from the "
    "Stardust path, 0 dBi, no external antenna, at the cost of the low phone-class SE "
    "tier (a knowingly-taken ~4x capacity haircut versus a gain terminal). "
    "Boosted-antenna devices are purpose-built (our hardware, no chipset assumption). "
    "The Iridium model is the MSS lane and never claims to reach an unmodified handset; "
    "the unmodified-phone lane stays on cellular spectrum (the High-Bandwidth Cellular "
    "Pure Play model)."
)
"""SOURCED_ESTIMATE (0.8 ecosystem assumption; COMM-661 to COMM-676). The stated
ecosystem assumption behind the Iridium model's phone class, carried on the Iridium
record and published in the artifact's physics block and first among its assumptions.
Keeps the three lanes
separate: the Iridium model is the MSS lane, never the unmodified-phone cellular lane
(the High-Bandwidth Cellular Pure Play model)."""

IRIDIUM_OPERATIONS_COST_MUSD: Final[float] = 0.0
"""INVESTOR_SET (assumption). The Iridium model's operations cost assumed zero (the
High-Bandwidth Cellular Pure Play model carries no operations line, so the Iridium
model inherits zero): a fixed line to research and add later, stated explicitly in the
assumptions output rather than silently omitted."""

IRIDIUM_SCENARIO_NAME_DEFAULT: Final[str] = "Iridium L-band max-outcome (every device class)"
"""SCENARIO. The default Iridium-model scenario label, carried on the ``IridiumDials``
block (the optional block's single label home, mirroring ``GroundInterfaceDials``): one run
reports every device class side by side."""

RETIRED_CAP_READING_FLEET: Final[int] = 2_000
"""INVESTOR_SET (2026-06-26, the cellular family's fleet cap then, which the Iridium model
inherited through ``iridium-v5``). The 2,000-satellite fleet the Iridium model once took from
the cellular family as a cap, which the saturation module retires for Iridium (ADR 005): the
Iridium model reads the curve at this fleet, labeled the retired cap, and keeps it for
comparison only. It caps nothing. It is its own constant, not
:data:`MAX_FLEET_SATELLITES_DEFAULT`, so a later change to the cellular family's live fleet cap
never moves this historical reading."""

# ===========================================================================
# The Iridium model's prices (investor-set, 2026-10-03 and 2026-10-04; the two terminal
# prices 2026-10-07): each class's and each IoT line's monthly price, held flat
# ===========================================================================
#
# Each device class sells every seat its living fleet carries at its own price, and the two
# IoT lines are fixed books at theirs (the counts below). A lower price or a smaller market
# is a division in the conclusions, never in the model; a margin is re-derived there, never
# divided. Government is left out of revenue (2026-10-04): no government count, price or
# line.

SMALL_TERMINAL_CLASS_PRICE_USD_MONTH_DEFAULT: Final[float] = 10.0
"""INVESTOR_SET (the investor, 2026-10-07 (A14): "Yes, let's use the $10 and $50"; it was $15, the
midpoint of the investor's 10-to-20 mass-market range set 2026-10-03, Sheet A's standard
price of 2026-07-09 renamed for the small terminal). The small terminal's monthly price,
dollars: $10, the low end of that range (COMM-618 context), held flat in every year."""

MOUNTED_TERMINAL_CLASS_PRICE_USD_MONTH_DEFAULT: Final[float] = 50.0
"""INVESTOR_SET (the investor, 2026-10-07 (A14): "Yes, let's use the $10 and $50"; it was $100, set
2026-10-03, Sheet A's premium price of 2026-07-09 renamed for the mounted terminal). The
mounted terminal's monthly price, dollars: $50, near Iridium's reported voice and data $47
and well under Certus $259 for a 0.7 Mbps-class service (COMM-618), held flat in every
year."""

PHONE_CLASS_PRICE_USD_MONTH_DEFAULT: Final[float] = 15.0
"""INVESTOR_SET (the investor, 2026-10-03; corrected 2026-10-04 from an unapproved $5). The
phone class's monthly price, dollars: Sheet A's standard $15 and the investor's floor, held
flat; no price haircut takes it lower. Its own constant, since Sheet A's standard price went
to the small terminal, whose own price is now the investor's $10 (2026-10-07)."""

MINIMAL_PACKET_IOT_PRICE_USD_MONTH_DEFAULT: Final[float] = 4.0
"""INVESTOR_SET (the investor's trial price, 2026-10-04). Minimal-packet IoT's monthly price
per device, dollars."""

DATA_IOT_PRICE_USD_MONTH_DEFAULT: Final[float] = 8.0
"""INVESTOR_SET (the investor's trial price, 2026-10-04; Sheet A's IoT price of 2026-07-09,
the investor's confirmed about-8 against Iridium's 7.78 IoT ARPU today, COMM-618, renamed for
data IoT). Data IoT's monthly price per device, dollars."""

ARPU_PRICE_CEILING_USD_MONTH: Final[float] = 5000.0
"""The upper Field bound on every monthly price (the three classes' and the two IoT
lines'), dollars: a generous sanity ceiling well above the Certus 259 anchor (COMM-618),
guarding a fat-fingered price without constraining any real MSS tier. A fixed bound, not a
tunable."""

# ===========================================================================
# The two IoT lines (ADR 007): fixed counts, and the IoT reading's constants
# ===========================================================================
#
# IoT is two fixed books, each its own revenue line, never inside a device class's margin,
# sold from the first year the living fleet reaches the coverage floor. Their counts are
# named constants, not settings, and never move with the fleet, the class, the downlink
# share, the panel or satellites per launch. The IoT reading (the saturation strategy's E8)
# spreads each line's count over the phone class's useful beams (IoT devices are low gain,
# so their reuse follows the phone rule) and reports its share of a beam's uplink.

MINIMAL_PACKET_IOT_DEVICES: Final[int] = 51_670_320
"""INVESTOR_SET (the investor, 2026-10-04; held as a stated assumption, ADR 007).
Minimal-packet IoT's fixed device count, the capable count: today's model's Sheet A IoT
count at the 340-satellite coverage floor, not Iridium's own IoT book of 1,998,000 devices
(COMM-617). Nothing physical caps the count short of billions of devices (COMM-659), so any
count is a stated assumption."""

DATA_IOT_DEVICES: Final[int] = 25_835_160
"""INVESTOR_SET (the investor, 2026-10-04: "somewhere in proportion"; held as a stated
assumption, ADR 007). Data IoT's fixed device count: half the minimal-packet count at double
its price, so the two books are equal. Iridium's own tiers run close to that inverse
proportion (IoT 1,998,000 devices at $7.78 a month against voice and data 402,000 at $47,
COMM-617, COMM-618)."""

MINIMAL_PACKET_IOT_MESSAGE_BYTES: Final[int] = 340
"""SOURCED_FACT (COMM-620, certified: Iridium's SBD IoT messages, about 340 bytes, the
volume engine; COMM-659). One minimal-packet IoT message, bytes."""

MINIMAL_PACKET_IOT_MESSAGES_PER_DAY: Final[int] = 48
"""INVESTOR_SET (the investor's usage table, 2026-10-04). Minimal-packet IoT's messages a day
per device: 48 of 340 bytes is about 1.5 bits a second, the top of COMM-659's 0.03 to 1.5
bits a second for a low-duty narrowband device. Data IoT sends them too, beside its bursts."""

DATA_IOT_BURSTS_PER_DAY: Final[int] = 4
"""INVESTOR_SET (the investor's usage, 2026-10-04, an assumption). Data IoT's bursts a day per
device, each :data:`DATA_IOT_BURST_BYTES`, beside its 48 messages. The line's rate of about
88 kbps describes it and enters no computation."""

DATA_IOT_BURST_BYTES: Final[int] = 100_000
"""INVESTOR_SET (the investor's usage, 2026-10-04, an assumption). One data IoT burst, bytes
(100 KB)."""

IOT_RANDOM_ACCESS_WINDOW_DEVICES_LOW: Final[int] = 57
"""SOURCED_ESTIMATE (COMM-654). The low end of the devices one NB-IoT NTN random-access window
serves, by mode: the IoT reading's access attempts a second a beam are read against this
window (a per-opportunity contention figure, not a population cap)."""

IOT_RANDOM_ACCESS_WINDOW_DEVICES_HIGH: Final[int] = 1_650
"""SOURCED_ESTIMATE (COMM-654). The high end of the devices one NB-IoT NTN random-access window
serves, by mode."""

IOT_RANDOM_ACCESS_WINDOWS_PER_SECOND: Final[int] = 1
"""ESTIMATE (an assumption, the saturation strategy's E8). The random-access windows a beam
offers a second, against which the access attempts a second a beam are read."""

IOT_MAC_EFFICIENCY: Final[float] = 0.20
"""ESTIMATE (COMM-659). The share of a beam's uplink bits that carry payload after the MAC
layer's overhead: the IoT reading reports the uplink bits share without it and with it (the
share over this)."""

IOT_MESSAGE_AIRTIME_LOW_S: Final[float] = 4.0
"""ESTIMATE (COMM-719, a ``scenario`` row: the design reviewer's figure, not investor-set).
The low end of the time one 340-byte minimal-packet IoT message holds one uplink tone,
seconds."""

IOT_MESSAGE_AIRTIME_HIGH_S: Final[float] = 7.0
"""ESTIMATE (COMM-719, a ``scenario`` row). The high end of the time one 340-byte
minimal-packet IoT message holds one uplink tone, seconds."""

NB_IOT_TONE_HZ: Final[float] = 3_750.0
"""SOURCED_FACT (COMM-714, certified). NB-IoT's narrowest uplink allocation, one single-tone
subcarrier, Hz: the held width over it counts the tones (about 2,133 in 8 MHz), and the
uplink holds the share 1 - d of them (the downlink share d, ADR 008)."""

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
"""DERIVED (the saturation strategy's rule D1, the sky sectors, from
:data:`SMALL_TERMINAL_CLASS_DIRECTIVITY_DBI`). The small terminal's sky above the
elevation mask in sectors of equal solid angle, ring by ring from the zenith: a zenith cap,
then one ring in two azimuth halves. A beam of directivity D spans about 4 pi / D sr, so
about 3 such beams fit in the sky above the mask, one per sector."""

MOUNTED_TERMINAL_CLASS_SECTOR_WEDGES_PER_RING: Final[tuple[int, ...]] = (1, 3, 5)
"""DERIVED (the saturation strategy's rule D1, the sky sectors, from
:data:`MOUNTED_TERMINAL_CLASS_DIRECTIVITY_DBI`). The mounted terminal's sky above the
elevation mask in sectors of equal solid angle, ring by ring from the zenith: a zenith cap,
a ring of 3, then a ring of 5 down to the mask. About 9 of its beams fit in the sky above
the mask, one per sector."""

PHONE_CLASS_SECTOR_WEDGES_PER_RING: Final[tuple[int, ...]] = ()
"""DERIVED (the saturation strategy's rule D1, the sky sectors, from
:data:`PHONE_CLASS_DIRECTIVITY_DBI`). No sky sectors: a 0 dBi device takes one co-channel
layer, so co-channel footprints on the same ground must not overlap."""

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

SATURATION_FOOTPRINT_BANDS: Final[int] = 160
"""SCENARIO (the saturation design's allocation rule; 160 by the investor's ruling of
2026-10-06, in place of the design's 40). Smallest footprint first fills each snapshot's
satellite-cell pairs in this many geometric footprint bands, committing each band before the
next. The count is a numerical convention the fill converges in. Why 160: the fill shares a
cell's first layer among every satellite of its smallest occupied band, so a wide band lets
several near-zenith satellites reach the serving share and serve the cell, and each serving
satellite keeps another sector's stacked layers a beamwidth away (rule D3's serving set). The
numerics review of the directional classes (its finding B1) measured the mounted terminal's
saturation number moving with the count at 40 bands, and 160 near converged: 320 bands adds
0.3 to 0.5 percent of the mounted terminal's capacity over 160 (at 40,000 and 64,009
satellites, at one shared usage of 1 Mbps x 2.5 percent). On the promoted curves of 2026-10-06,
from 40 to 160 bands, the small terminal's saturation number rises 0.3 percent, the mounted
terminal's moves from 48,912 to not reached by 64,009 (its last row), and the phone class's
rises 1.2 percent and its band points' up to 2.3 percent, while both terminals' capacity at 528
to 7,200 satellites moves 0.0 to 0.4 percent."""

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

# ===========================================================================
# The Iridium scenario's saturation block (ADRs 005 and 008): the downlink share and the
# promoted curve's path, the two defaults of ``communications.config.SaturationDials``
# ===========================================================================

DOWNLINK_SHARE_DEFAULT: Final[float] = 0.67
"""SCENARIO (ADR 008, ``docs/adr/008-downlink-time-share-scales-people.md``; COMM-620,
COMM-662). The downlink time share d of Iridium's time-division duplex band (COMM-662: the
uplink and the downlink share its tones in time): Certus 700's 2 : 1 down-to-up rate split
(COMM-620: 704 kbps down, 352 up), 704 / (704 + 352) to two figures. The saturation curve is
computed at d = 1; ADR 008 scales people, and every capacity but the satellite's peak, by d
when the curve is read. ADR 008's documented alternatives: 0.5, the symmetric frame, and 0.75,
an estimate. A scenario setting."""

SATURATION_CURVE_PATH_DEFAULT: Final[str] = "communications/models/iridium/saturation_curve.json"
"""The promoted saturation curve, repository-relative (ADR 005: ``saturation_curve.json``
carries each class's spectrum bound), where ``python -m communications.saturation`` writes it.
A scenario may name an absolute path instead (a test's temporary curve). A fixed file location,
not a tunable."""

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
    "SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT",
    "SUBSCRIBERS_PER_SATELLITE_DEFAULT",
    # Iridium-model (L-band max-outcome) additions.
    "APERTURE_M2_DEFAULT",
    "APERTURE_REFERENCE_M2",
    "APERTURE_STACK_CAVEAT_NOTE",
    "APERTURE_VALIDATED_STACK_LIMIT_M2",
    "BITS_PER_BYTE",
    "DeviceClass",
    "ECOSYSTEM_ASSUMPTION_NOTE",
    "GBPS_TO_MBPS",
    "HZ_PER_MHZ",
    "IRIDIUM_OPERATIONS_COST_MUSD",
    "IRIDIUM_SCENARIO_NAME_DEFAULT",
    "RETIRED_CAP_READING_FLEET",
    "SECONDS_PER_DAY",
    # The Iridium model's prices (2026-10-03 and 2026-10-04; the two terminal prices 2026-10-07).
    "ARPU_PRICE_CEILING_USD_MONTH",
    "DATA_IOT_PRICE_USD_MONTH_DEFAULT",
    "MINIMAL_PACKET_IOT_PRICE_USD_MONTH_DEFAULT",
    "MOUNTED_TERMINAL_CLASS_PRICE_USD_MONTH_DEFAULT",
    "PHONE_CLASS_PRICE_USD_MONTH_DEFAULT",
    "SMALL_TERMINAL_CLASS_PRICE_USD_MONTH_DEFAULT",
    # The two IoT lines and the IoT reading (ADR 007).
    "DATA_IOT_BURSTS_PER_DAY",
    "DATA_IOT_BURST_BYTES",
    "DATA_IOT_DEVICES",
    "IOT_MAC_EFFICIENCY",
    "IOT_MESSAGE_AIRTIME_HIGH_S",
    "IOT_MESSAGE_AIRTIME_LOW_S",
    "IOT_RANDOM_ACCESS_WINDOWS_PER_SECOND",
    "IOT_RANDOM_ACCESS_WINDOW_DEVICES_HIGH",
    "IOT_RANDOM_ACCESS_WINDOW_DEVICES_LOW",
    "MINIMAL_PACKET_IOT_DEVICES",
    "MINIMAL_PACKET_IOT_MESSAGES_PER_DAY",
    "MINIMAL_PACKET_IOT_MESSAGE_BYTES",
    "NB_IOT_TONE_HZ",
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
    # The Iridium scenario's saturation block (ADRs 005 and 008).
    "DOWNLINK_SHARE_DEFAULT",
    "SATURATION_CURVE_PATH_DEFAULT",
]
