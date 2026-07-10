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


class DeviceClass(StrEnum):
    """The Iridium model (formerly Model B) device class, which sets the SE tier.

    The founder's three device categories (2026-07-07; the 9c device ladder).
    ``PHONE_CLASS`` is the cell phone: the 0-dBi in-chipset phone-form-factor baseline
    (SE band 0.5 to 0.8 bps/Hz, central :data:`PHONE_CLASS_SE_CENTRAL`).
    ``SMALL_TERMINAL_CLASS`` is the small boosted antenna: paperback/puck size, ~20 cm
    integrated patch, ~10 dBi, unpointed, purpose-built with NO chipset assumption
    (SE band 1.5 to 2.5, central :data:`SMALL_TERMINAL_CLASS_SE_CENTRAL`).
    ``TERMINAL_CLASS`` is the LARGE boosted / custom-antenna tier: mounted or pointed,
    15+ dBi (drones, fixed sites, vehicles; SE band 2.0 to 3.0, central
    :data:`TERMINAL_CLASS_SE_CENTRAL`). See the ecosystem assumption
    (:data:`ECOSYSTEM_ASSUMPTION_NOTE`): the Iridium model reaches purpose-built or
    in-chipset devices on Iridium's owned L-band (the MSS lane), NEVER an unmodified
    phone (that is the cellular lane, the High-Bandwidth Cellular Pure Play model,
    formerly Model A). One class per run in v1 (no mixed fleet).
    """

    PHONE_CLASS = "phone_class"
    SMALL_TERMINAL_CLASS = "small_terminal_class"
    TERMINAL_CLASS = "terminal_class"


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
"""ESTIMATE (COMM-097, the ~$200 to 260/sub/yr replacement split implies a
~5-year hardware lineage; corrected from COMM-091 per the traceability audit).
Satellite operating life, the cohort cliff: after this many years a cohort retires
and contributes zero coverage. A design/depreciation assumption (the Starlink
replacement-capex anchor), not a certified field life."""

SATELLITE_BUILD_COST_MUSD_DEFAULT: Final[float] = 1.05
"""FOUNDER_SET (in-band; round 4, 2026-06-25). The flat MASS-MANUFACTURED
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
"""FOUNDER_SET (flagged; session state, Iridium spectrum reconciled). The Iridium
EXCLUSIVE L-band holding (~7.775 MHz rounded to 8.0), a WIDTH held, NOT a frequency
(the frequency is the ~1.6 GHz dial position). The coordinated 10.5 MHz span is the
documented variant (:data:`SPECTRUM_MHZ_COORDINATED`), not the default."""

SPECTRUM_MHZ_COORDINATED: Final[float] = 10.5
"""SCENARIO. The coordinated L-band span (1616 to 1626.5 MHz), a documented
Iridium-model variant WIDTH, not the default (the exclusive ~8 MHz is the default)."""

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
"""ESTIMATE (derived; brainstorming 9c device ladder). Central of the 1.5 to 2.5
bps/Hz band for the SMALL boosted-antenna device: paperback/puck size, ~20 cm
integrated patch, ~10 dBi, unpointed, purpose-built so NO chipset assumption (OUR
hardware; the founder's 10 to 20 Mbps tier in 9c). Derivation anchor: phone-class SE
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

TERMINAL_CLASS_SE_CENTRAL: Final[float] = 2.5
"""SOURCED_ESTIMATE (COMM-650). Central of the 2.0 to 3.0 bps/Hz band for the LARGE
boosted / custom-antenna tier: mounted or pointed, 15+ dBi (drones, fixed sites,
vehicles; the AST-class anchor). Value untouched from the corpus; wording updated for
the three-tier device ladder."""

TERMINAL_CLASS_SE_LOW: Final[float] = 2.0
"""SOURCED_ESTIMATE (COMM-650). Low edge of the documented large-tier
spectral-efficiency sweep band."""

TERMINAL_CLASS_SE_HIGH: Final[float] = 3.0
"""SOURCED_ESTIMATE (COMM-650). High edge of the documented large-tier
spectral-efficiency sweep band."""

REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE: Final[float] = 0.15
"""DERIVED (COMM-410). The per-satellite capacity calibration, in Gbps per (MHz x
bps/Hz), at the :data:`APERTURE_REFERENCE_M2` reference aperture. It is NOT a clean
unit conversion: it folds the effective ~150x beam-count-times-frequency-reuse
multiplier of a modern digital-beamforming satellite together with the Mbps-to-Gbps
scaling (0.15 Gbps per (MHz x bps/Hz) = 150 effective reuse x (1 Gbps / 1000 Mbps)).
CHOSEN so the corpus anchor reproduces: 25 MHz x 2.5 SE x 0.15 = 9.375 Gbps, the
central of the grounded ~5 to 15 Gbps-per-satellite range (COMM-410). It also
reproduces phone-class 8 MHz x 0.65 x 0.15 = 0.78 Gbps and terminal-class 8 MHz x 2.5
x 0.15 = 3.0 Gbps. Per-satellite capacity is this x spectrum_mhz x SE x (aperture_m2 /
:data:`APERTURE_REFERENCE_M2`)."""

ACTIVE_USER_RATE_MBPS_DEFAULT: Final[float] = 1.0
"""FOUNDER_SET (flagged; 6a input schema). The per-subscriber active data rate in
Mbps (standard smartphone activity when active); also the peak per-user rate by
construction (the service tier). :data:`ACTIVE_USER_RATE_MBPS_RICH` is the rich
variant."""

ACTIVE_USER_RATE_MBPS_RICH: Final[float] = 2.5
"""SCENARIO (6a input schema). The rich per-subscriber active-rate variant in Mbps, a
documented alternative to :data:`ACTIVE_USER_RATE_MBPS_DEFAULT`."""

CONCURRENCY_PEAK_DEFAULT: Final[float] = 0.025
"""FOUNDER_SET (flagged as the pair with :data:`CONCURRENCY_OFFPEAK_DEFAULT`; 6a input
schema, the DTC concurrency corpus). Busy-hour PEAK concurrency fraction (2.5% of
subscribers simultaneously active at peak)."""

CONCURRENCY_OFFPEAK_DEFAULT: Final[float] = 0.005
"""FOUNDER_SET (flagged as the pair with :data:`CONCURRENCY_PEAK_DEFAULT`; 6a input
schema, the DTC concurrency corpus). OFF-PEAK concurrency fraction (0.5% of
subscribers simultaneously active off-peak)."""

IOT_DEVICES_DEFAULT: Final[int] = 10_000_000
"""ESTIMATE (COMM-654 / COMM-659). A passthrough DEVICE counter (low end of "tens of
millions"), founder-owned (flagged). Counted as DEVICES, never folded into the people
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
no-deployable design (COMM-251); the AST precedent shows the fold path's cost (223 m^2
flies 1 per launch even on a 7 m fairing). Used ONLY by the assumptions caveat
(:data:`APERTURE_FOLD_CAVEAT_NOTE`), NEVER as a config bound: the above-limit what-if
stays computable."""

APERTURE_FOLD_CAVEAT_NOTE: Final[str] = (
    "The configured aperture exceeds the no-fold stow limit: a flat panel this large "
    "cannot stow in Neutron's 5.5 m fairing without folding, which contradicts the "
    "Flatellite no-deployable design (COMM-251), and the deployment-complexity penalty "
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
"""FOUNDER_SET (assumption). The Iridium model's operations cost assumed zero (the
High-Bandwidth Cellular Pure Play model carries no operations line, so the Iridium
model inherits zero): a fixed line to research and add later, stated explicitly in the
assumptions output rather than silently omitted."""

IRIDIUM_SCENARIO_NAME_DEFAULT: Final[str] = "Iridium L-band max-outcome (phone-class baseline)"
"""SCENARIO. The default Iridium-model scenario label, carried on the ``IridiumDials``
block (the optional block's single label home, mirroring ``GroundInterfaceDials``)."""

# ===========================================================================
# The Iridium four-bucket ARPU revenue case (founder-set, Sheet A, 2026-07-09)
# ===========================================================================
#
# The PUBLISHED Iridium ARPU case: four billable-connection buckets (standard
# personal / premium terminal / IoT devices / government), each a PERCENTAGE of one
# pool anchored to fleet CAPACITY (``fleet_target x subscribers_per_satellite``), so
# every bucket scales with the satellite count. The four mix percentages and the
# four monthly prices are the FOUNDER-SET dials below; the counts are DERIVED
# (:func:`communications.engine.derive_arpu_buckets`). Subscribers are PEOPLE (the
# standard and premium buckets consume the physics density); IoT are DEVICES;
# government is a contract line. The pool is a BILLABLE-CONNECTIONS accounting frame
# (Iridium's own reporting convention: its ~2.5M "billable subscribers" fold in ~2.0M
# IoT DEVICES, COMM-617), NOT one summed people population. Precedent frame: Iridium
# FY2025 billable mix (COMM-617/618/619). Sheet A (below) is the blessed default;
# Sheet B (18.7 / 2.5 / 78.55 / 0.25 at the same prices, the today's-device-ratio
# posture) is the documented alternative in ``scenarios/iridium.yaml``.

ARPU_STANDARD_MIX_PCT_DEFAULT: Final[float] = 15.0
"""FOUNDER_SET (Sheet A, 2026-07-09). The STANDARD personal (phone-class) bucket's
share of the billable-connection pool, percent. A PEOPLE bucket (it consumes the
physics density). Loosely anchored, paired with premium, on the FY2025 book's
like-for-like people share (COMM-617/618). One of the two people mixes, so its config
Field lower bound is strictly positive (``people_share`` cannot be zero)."""

ARPU_PREMIUM_MIX_PCT_DEFAULT: Final[float] = 2.0
"""FOUNDER_SET (Sheet A, 2026-07-09). The PREMIUM terminal bucket's share of the
pool, percent. A PEOPLE bucket: the gain-terminal tier (a Certus-class service on our
own hardware, COMM-618). The second of the two people mixes (strictly-positive Field
lower bound)."""

ARPU_IOT_MIX_PCT_DEFAULT: Final[float] = 82.805
"""FOUNDER_SET (Sheet A, 2026-07-09). The IoT DEVICE bucket's share of the pool,
percent: the RESIDUAL that closes the mix to 100. Counted as DEVICES, never folded
into the people count (COMM-654/659). At the baseline it implies about 51.7 million
devices, above the corpus tens-of-millions center, carried as a stated MARKET-SHAPE
assumption (contention-limited, zero fleet-sizing effect)."""

ARPU_GOVERNMENT_MIX_PCT_DEFAULT: Final[float] = 0.195
"""FOUNDER_SET (Sheet A, 2026-07-09). The GOVERNMENT bucket's share of the pool,
percent. Deliberately DE-ANCHORED from the FY2025 book's 4.8 percent down to 0.195,
calibrated so the baseline government line reproduces today's one fixed EMSS contract
(about 108 million dollars over about 121.7k connections, COMM-619) rather than
scaling a 4.8 percent share. Held uniform with the fleet as a stated scenario
assumption."""

ARPU_STANDARD_PRICE_USD_MONTH_DEFAULT: Final[float] = 15.0
"""FOUNDER_SET (Sheet A, 2026-07-09). The STANDARD personal monthly price, dollars:
the midpoint of the founder's stated 10-to-20 mass-market phone-class range
(COMM-618 context)."""

ARPU_PREMIUM_PRICE_USD_MONTH_DEFAULT: Final[float] = 100.0
"""FOUNDER_SET (Sheet A, 2026-07-09). The PREMIUM terminal monthly price, dollars:
between Iridium's reported voice/data 47 and Certus 259 for a 0.7 Mbps-class service
(COMM-618), while the modernized fleet delivers about 4 Mbps to the same buyer."""

ARPU_IOT_PRICE_USD_MONTH_DEFAULT: Final[float] = 8.0
"""FOUNDER_SET (Sheet A, 2026-07-09). The IoT DEVICE monthly price, dollars: the
founder's confirmed about-8 (Iridium's reported IoT ARPU is 7.78 today, COMM-618)."""

ARPU_GOVERNMENT_PRICE_USD_MONTH_DEFAULT: Final[float] = 74.0
"""FOUNDER_SET (Sheet A, 2026-07-09). The GOVERNMENT monthly price, dollars: today's
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
    # Iridium-model (L-band) input dials, all real in-band values (not sentinels).
    "iridium.spectrum_mhz": False,  # FOUNDER_SET 8.0 exclusive holding (not a sentinel)
    "iridium.aperture_m2": False,  # FOUNDER_SET 25.0 Flatellite reference (not a sentinel)
    "iridium.device_class": False,  # FOUNDER_SET PHONE_CLASS baseline (not a sentinel)
    "iridium.active_user_rate_mbps": False,  # FOUNDER_SET 1.0 Mbps (not a sentinel)
    "iridium.concurrency_peak": False,  # FOUNDER_SET 0.025 peak (not a sentinel)
    "iridium.concurrency_offpeak": False,  # FOUNDER_SET 0.005 off-peak (not a sentinel)
    "iridium.iot_devices": False,  # ESTIMATE 10M passthrough (not a sentinel)
    # Iridium four-bucket ARPU dials (Sheet A, founder-set 2026-07-09; not sentinels).
    "iridium.arpu.standard_mix_pct": False,  # FOUNDER_SET 15.0 percent (not a sentinel)
    "iridium.arpu.premium_mix_pct": False,  # FOUNDER_SET 2.0 percent (not a sentinel)
    "iridium.arpu.iot_mix_pct": False,  # FOUNDER_SET 82.805 percent residual (not a sentinel)
    "iridium.arpu.government_mix_pct": False,  # FOUNDER_SET 0.195 percent (not a sentinel)
    "iridium.arpu.standard_price_usd_month": False,  # FOUNDER_SET 15.0 dollars (not a sentinel)
    "iridium.arpu.premium_price_usd_month": False,  # FOUNDER_SET 100.0 dollars (not a sentinel)
    "iridium.arpu.iot_price_usd_month": False,  # FOUNDER_SET 8.0 dollars (not a sentinel)
    "iridium.arpu.government_price_usd_month": False,  # FOUNDER_SET 74.0 dollars (not a sentinel)
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
    # Iridium-model (L-band max-outcome) additions.
    "ACTIVE_USER_RATE_MBPS_DEFAULT",
    "ACTIVE_USER_RATE_MBPS_RICH",
    "APERTURE_FOLD_CAVEAT_NOTE",
    "APERTURE_NO_FOLD_LIMIT_M2",
    "APERTURE_REFERENCE_M2",
    # The Iridium four-bucket ARPU revenue case (Sheet A, founder-set 2026-07-09).
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
    "PHONE_CLASS_SE_CENTRAL",
    "PHONE_CLASS_SE_HIGH",
    "PHONE_CLASS_SE_LOW",
    "REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE",
    "SMALL_TERMINAL_CLASS_SE_CENTRAL",
    "SMALL_TERMINAL_CLASS_SE_HIGH",
    "SMALL_TERMINAL_CLASS_SE_LOW",
    "SPECTRUM_MHZ_COORDINATED",
    "SPECTRUM_MHZ_DEFAULT",
    "TERMINAL_CLASS_SE_CENTRAL",
    "TERMINAL_CLASS_SE_HIGH",
    "TERMINAL_CLASS_SE_LOW",
]
