"""Module-level Final[T] named constants for the communications model config.

Every constant carries a docstring with:
- Source class: the design's EXISTS / INTERIM / NEEDS-RESEARCH / DERIVED tag,
  mapped to the plan Section 0.5 taxonomy where useful (EXISTS to
  sourced_estimate/certified, INTERIM to scenario, NEEDS-RESEARCH to
  placeholder/scenario, DERIVED to derived_estimate).
- A citation: a research path, a `COMM-*` claim ID from
  `research/SOURCE_INDEX.md`, or the founder-set note.

This module is the single source of truth for the communications config's
"no bare numeric literals" rule (CLAUDE.md). Every default that the
`communications.config` Pydantic blocks read lives here.

The eight cadence / launch-cost defaults are NOT re-stated here: they are
imported from `common.cadence` (the shared spine both ventures consume) and
re-exported, so the comms config behaves identically to the data-center
cadence machinery. Importing from `common` is not a venture dependency.
"""

from __future__ import annotations

from typing import Final

# The eight cadence / launch-cost defaults are imported from the shared
# `common.cadence` spine (plan P1.3 path (a)) and re-exported below so the
# comms config reads the SAME anchors the data-center cadence machinery uses.
from common.cadence import (
    CADENCE_CEILING_DEFAULT,
    FIRST_LAUNCH_YEAR_DEFAULT,
    HIGH_CADENCE_COST_MUSD_DEFAULT,
    HIGH_CADENCE_LAUNCHES_DEFAULT,
    LAUNCHES_AT_YEAR_5_DEFAULT,
    LAUNCHES_AT_YEAR_10_DEFAULT,
    LOW_CADENCE_COST_MUSD_DEFAULT,
    LOW_CADENCE_LAUNCHES_DEFAULT,
)

# ============================================================
# Year-bound constants
# ============================================================
# Defined locally (NOT imported from the DC venture) so the comms package carries
# no DC-venture dependency, mirroring the Phase-0 cadence-constants decision.
# A drift test (test_constants_alignment.py) asserts these equal the DC values.

MIN_FY: Final[int] = 2020
"""INTERIM (matches DC). Lower bound for any fiscal-year field; below this is
the pre-space era. Held equal to the DC MIN_FY value (drift-tested)."""

MAX_FY: Final[int] = 2080
"""INTERIM (matches DC). Upper bound for any fiscal-year field; beyond this the
forward trends have no defensible basis. Held equal to the DC value."""

MIN_HORIZON_YEARS: Final[int] = 5
"""INTERIM (matches DC). Minimum analysis horizon in years. Below the satellite
service-life cliff the trajectory is not informative. Held equal to the DC value."""

MAX_HORIZON_YEARS: Final[int] = 20
"""INTERIM (matches DC). Maximum analysis horizon in years; beyond this the
forward extrapolation is speculation. Held equal to the DC value."""

# ============================================================
# Metadata defaults
# ============================================================

BASE_YEAR_DEFAULT: Final[int] = 2026
"""INTERIM (scenario). Calendar year of model year 0: Neutron's first-flight
year, aligned to the data-center timeline (plan Section 0.8)."""

HORIZON_YEARS_DEFAULT: Final[int] = 10
"""INTERIM (scenario). Number of fiscal-year steps after year 0, so FY2036 is
the year-10 anchor matching the 90-launches-by-2036 cadence (plan Section 0.8)."""

STEADY_STATE_YEAR_DEFAULT: Final[int] = 2036
"""INTERIM (scenario). The year the headline mature steady-state figure is read
at; year 10 of the default window (plan Section 0.8, concern C1)."""

# ============================================================
# Neutron envelope constants (comms-specific, NOT in the DC)
# ============================================================

NEUTRON_MASS_ENVELOPE_T_DEFAULT: Final[float] = 13.0
"""INTERIM (scenario). The baseline Neutron mass envelope to low-inclination
LEO, tonnes. Low-inclination LEO carries more than the DC SSO 12.5 t case (plan
Section 0.8); anchored pending a payload-fit pin (neutron_comms_payload_fit.md)."""

NEUTRON_FAIRING_VOLUME_M3_DEFAULT: Final[float] = 80.0
"""EXISTS (sourced_estimate). The baseline Neutron fairing usable volume, cubic
meters; carried as a comms constant equal to the DC fairing-volume
constant NEUTRON_FAIRING_USABLE_VOLUME_M3 (80.0)."""

UPGRADED_NEUTRON_MASS_ENVELOPE_T_DEFAULT: Final[float] = 15.0
"""INTERIM (scenario). The upgraded-Neutron mass envelope (bigger fairing, more
mass), tonnes, used when ConstellationDials.upgraded_neutron is True. Anchored
above the baseline pending the upgraded-vehicle spec."""

UPGRADED_NEUTRON_FAIRING_VOLUME_M3_DEFAULT: Final[float] = 100.0
"""INTERIM (scenario). The upgraded-Neutron fairing usable volume, cubic meters.
Anchored above the baseline 80.0 pending the upgraded-vehicle spec."""

# ============================================================
# Four-area satellite cost defaults: BROADBAND (V3-class, mass-bound)
# ============================================================
# The four-area sum these defaults imply lands inside the V3 sanity band
# $0.8M to $1.5M (DESIGN.md Section 3; comms_space_supply_cost.md COMM-082):
#   antenna 0.45 + comms-electronics 0.35 + solar (20_000 * 10 / 1e6 = 0.20)
#   + radiator/bus 0.20 = 1.20 MUSD, the about-$1.2M V3 anchor.

BROADBAND_ANTENNA_COST_MUSD_DEFAULT: Final[float] = 0.45
"""NEEDS-RESEARCH (scenario, INTERIM). The broadband phased-array aperture cost,
$M; the dominant high-value line. Bill-of-materials-derived, anchored pending the
antenna BOM (DESIGN.md Section 3)."""

BROADBAND_COMMS_ELECTRONICS_COST_MUSD_DEFAULT: Final[float] = 0.35
"""NEEDS-RESEARCH (scenario, INTERIM). The broadband comms electronics cost
(modems, beam-forming, on-board processing, RF chain), $M. Bill-of-materials-
derived, anchored pending the BOM (DESIGN.md Section 3)."""

BROADBAND_SOLAR_COST_USD_PER_KW_DEFAULT: Final[float] = 20_000.0
"""INTERIM (scenario). The comms solar array cost per kW, USD/kW; explicitly NOT
the DC $40k/kW (the DC ledger flags that high). DESIGN.md Section 3,
RLDC-SOLAR-RADIATOR-COSTDOWN-SENSITIVITY."""

BROADBAND_PAYLOAD_POWER_KW_DEFAULT: Final[float] = 10.0
"""NEEDS-RESEARCH (scenario, INTERIM). The broadband comms-payload power draw,
kW; tens of kW, far below the DC node's roughly 400 kW (DESIGN.md Section 3,
Section 11 item 2). Sizes the solar line."""

BROADBAND_RADIATOR_BUS_COST_MUSD_DEFAULT: Final[float] = 0.20
"""INTERIM (scenario). The broadband spacecraft bus plus thermal cost, $M;
anchored light and AI-1-class (RLDC-AI1-EQUIVALENT, the 0.10 t bus; DESIGN.md
Section 3)."""

BROADBAND_SATELLITE_MASS_T_DEFAULT: Final[float] = 1.5
"""EXISTS (sourced_estimate). The broadband (V3-class) per-satellite wet mass,
tonnes (about 1,500 kg; comms_space_supply_cost.md COMM-082). Mass-bound against
the Neutron envelope (about 5 per launch)."""

BROADBAND_STOWED_VOLUME_M3_DEFAULT: Final[float] = 8.0
"""INTERIM (scenario). The broadband per-satellite stowed (folded) volume, cubic
meters; smaller than direct-to-cell so broadband binds on mass, not volume
(neutron_comms_payload_fit.md). Anchored so 80.0/8.0 = 10 volume slots leaves
mass (13.0/1.5 ~= 8.7, about 5 effective) the binding constraint."""

# ============================================================
# Four-area satellite cost defaults: DIRECT_TO_CELL (antenna-stow, volume-bound)
# ============================================================
# Antenna-heavy: the large direct-to-cell array (AST BlueBird Block 2 is about
# 223 square meters; comms_direct_to_cell.md) dominates and the folded antenna
# fills the fairing before the mass limit. The four-area sum is strictly greater
# than the broadband sum:
#   antenna 2.50 + comms-electronics 0.60 + solar (20_000 * 15 / 1e6 = 0.30)
#   + radiator/bus 0.40 = 3.80 MUSD (antenna-heavy, its own anchor).

DIRECT_TO_CELL_ANTENNA_COST_MUSD_DEFAULT: Final[float] = 2.50
"""NEEDS-RESEARCH (scenario, INTERIM). The direct-to-cell phased-array aperture
cost, $M; the large AST Block 2-class array (about 223 square meters,
comms_direct_to_cell.md) dominates. Anchored higher than broadband, pending the
antenna BOM (DESIGN.md Section 3, Section 4)."""

DIRECT_TO_CELL_COMMS_ELECTRONICS_COST_MUSD_DEFAULT: Final[float] = 0.60
"""NEEDS-RESEARCH (scenario, INTERIM). The direct-to-cell comms electronics
cost, $M; higher than broadband (more beams, more processing). Anchored pending
the BOM (DESIGN.md Section 3)."""

DIRECT_TO_CELL_SOLAR_COST_USD_PER_KW_DEFAULT: Final[float] = 20_000.0
"""INTERIM (scenario). The direct-to-cell solar array cost per kW, USD/kW; the
same about-$20k/kW comms anchor as broadband (DESIGN.md Section 3)."""

DIRECT_TO_CELL_PAYLOAD_POWER_KW_DEFAULT: Final[float] = 15.0
"""NEEDS-RESEARCH (scenario, INTERIM). The direct-to-cell comms-payload power
draw, kW; higher than broadband (the larger array draws more), still tens of kW
(DESIGN.md Section 3)."""

DIRECT_TO_CELL_RADIATOR_BUS_COST_MUSD_DEFAULT: Final[float] = 0.40
"""INTERIM (scenario). The direct-to-cell spacecraft bus plus thermal cost, $M;
heavier bus than broadband, anchored light and AI-1-class (DESIGN.md Section 3)."""

DIRECT_TO_CELL_SATELLITE_MASS_T_DEFAULT: Final[float] = 6.0
"""INTERIM (scenario). The direct-to-cell per-satellite wet mass, tonnes;
antenna-heavy, heavier than the broadband 1.5 t (DESIGN.md Section 4). Mass alone
would allow 13.0/6.0 ~= 2 per launch, but volume binds first (about 1)."""

DIRECT_TO_CELL_STOWED_VOLUME_M3_DEFAULT: Final[float] = 70.0
"""INTERIM (scenario). The direct-to-cell per-satellite stowed (folded) volume,
cubic meters; the large folded antenna fills the fairing (80.0/70.0 ~= 1) before
the mass limit, making direct-to-cell volume-bound (neutron_comms_payload_fit.md,
DESIGN.md Section 4)."""

# ============================================================
# Other constellation defaults
# ============================================================

MINOR_COMPONENT_PCT_DEFAULT: Final[float] = 0.01
"""INTERIM (scenario). A configurable percentage of the satellite carried for a
minor component the model does not break out (about 1%; DESIGN.md Section 3)."""

SATELLITE_LIFETIME_YEARS_DEFAULT: Final[int] = 5
"""INTERIM (scenario). The satellite service-life cliff, years (5 default, test
7, NOT 3; plan Section 0.8). Drives the common.cohort cliff in Phase 3."""

V4_CAPABILITY_MULTIPLIER_DEFAULT: Final[float] = 1.0
"""INTERIM (scenario). The V4 capability step from the V1/V2/V3 trend; 1.0 = no
step (the base case is the V3-class anchor), configurable (DESIGN.md Section 8)."""

# ============================================================
# Cost-down (learning-curve) defaults
# ============================================================

LEARNING_RATE_PER_DOUBLING_DEFAULT: Final[float] = 0.10
"""INTERIM (scenario). The fractional reduction in per-satellite four-area cost
per doubling of cumulative units built (a 90% learning curve). Not yet research-
pinned; the founder may set it (DESIGN.md Section 3, strategy Section 2)."""

COST_DOWN_REFERENCE_UNITS_DEFAULT: Final[int] = 1
"""INTERIM (scenario). The reference cumulative-units count N0 at which the
four-area cost equals the un-discounted per-satellite cost (the curve's anchor
point); the first unit is the un-discounted anchor."""

# ============================================================
# Spectrum defaults (SPECTRUM_spec.md Section 4)
# ============================================================

LEASED_BANDWIDTH_MHZ_DEFAULT: Final[float] = 40.0
"""EXISTS (sourced_estimate). The per-beam channel width leased under the FCC SCS
framework, MHz (the capacity layer vs the 2x5 MHz messaging floor); the AST
40-MHz-to-120-Mbps anchor (SPECTRUM_spec.md Section 1.3)."""

SPECTRAL_EFFICIENCY_BPS_PER_HZ_DEFAULT: Final[float] = 0.6
"""EXISTS (sourced_estimate). The D2C median spectral efficiency, bps/Hz (the
0.52 to 0.61 phone-to-LEO median; SPECTRUM_spec.md Section 4). USED ONLY as a
cross-check on the empirical capacity anchor, NEVER to generate capacity."""

BEAMS_PER_SAT_DEFAULT: Final[int] = 2500
"""EXISTS (sourced_estimate). The beams per satellite; AST Block 2 is designed
for about 2,500 adjustable beams (SPECTRUM_spec.md Section 2.3)."""

PER_BEAM_CAPACITY_ANCHOR_MBPS: Final[float] = 120.0
"""EXISTS (sourced_estimate). The empirical per-beam capacity anchor, Mbps,
measured on 40 MHz (AST). Paired with PER_BEAM_CAPACITY_ANCHOR_MHZ; the Phase-2
spectrum module scales capacity linearly from this point (SPECTRUM_spec.md)."""

PER_BEAM_CAPACITY_ANCHOR_MHZ: Final[float] = 40.0
"""EXISTS (sourced_estimate). The bandwidth at which the 120 Mbps per-beam
capacity was measured, MHz (the AST 40-MHz-to-120-Mbps anchor point)."""

# The per-user-rate and oversubscription BAND defaults, stored ASCENDING BY
# MAGNITUDE (so the BandTriple low <= mid <= high validator passes at
# construction; plan P1.2 block 6). The customer band the Phase-2 chain forms is
# INVERTED on the rate (a higher per-user rate provisions a fatter pipe and
# serves FEWER subscribers): rate.high feeds the customer-LOW member.
#
# Under these defaults, with per_beam_capacity = 120 Mbps and beams_per_sat =
# 2500 (so the aggregate is 2500 * 120 = 300,000 subscriber-Mbps), the Phase-2
# inverted pairing lands the direct-to-cell planning order EXACTLY:
#   customer low  = 2500 * (120 / 6.0) * 1.0 = 300000 / 6.0 * 1.0 =  50,000
#   customer mid  = 2500 * (120 / 3.0) * 1.5 = 300000 / 3.0 * 1.5 = 150,000
#   customer high = 2500 * (120 / 2.0) * 2.0 = 300000 / 2.0 * 2.0 = 300,000

TARGET_PER_USER_RATE_BAND_DEFAULT: Final[tuple[float, float, float]] = (2.0, 3.0, 6.0)
"""INTERIM (scenario, NEEDS-FOUNDER). The per-user service level the beam is
provisioned against (the sustained shared rate), low/mid/high in Mbps, stored
ascending (2.0 / 3.0 / 6.0). The biggest open question; the founder may set it.
Consumed INVERTED by the Phase-2 customer chain (rate.high feeds customer LOW),
landing the 50,000 / 150,000 / 300,000 target (SPECTRUM_spec.md Section 2.2)."""

OVERSUBSCRIPTION_BAND_DEFAULT: Final[tuple[float, float, float]] = (1.0, 1.5, 2.0)
"""INTERIM (scenario, NEEDS-FOUNDER). Registered subscribers run many times the
simultaneously active users (many-to-one packing; D2C demand is trip-shaped),
low/mid/high stored ascending (1.0 / 1.5 / 2.0, every member >= 1). Consumed
forward by the Phase-2 chain (oversub.low feeds customer LOW). Held near 1 to hit
the stated target at sustained rates (SPECTRUM_spec.md Section 2.4; see F-BAND)."""

# ============================================================
# Price-reference defaults (price/collectability, NOT demand; plan Section 0.0 A1)
# ============================================================

RETAIL_REFERENCE_USD_PER_MONTH_DEFAULT: Final[float] = 100.0
"""FOUNDER-SET CONFIG (scenario, not sourced). The retail reference: about
$100/month of full cell service, the founder's own bill, the price to beat in the
undercut check. The corpus carries individual phone ARPU around $50 and per-
account ARPA around $147, so $100 sits between them (DESIGN.md Section 7)."""

ARPU_USD_PER_MONTH_DEFAULT: Final[float] = 50.0
"""EXISTS (sourced_estimate). The average revenue per user reference used in the
revenue-ceiling reconciliation; the individual-phone ARPU the corpus carries
(DESIGN.md Section 7, plan Section 0.9 / concern C8)."""

OPERATOR_REVENUE_SHARE_DEFAULT: Final[float] = 0.5
"""INTERIM (scenario). The fraction of ARPU the space operator collects under an
SCS revenue-share lease (the rest stays with the carrier). Used in the Phase-4/5
revenue-ceiling reconciliation."""

SCOPE_WEIGHTS_DEFAULT: Final[tuple[float, float, float]] = (0.5, 0.3, 0.2)
"""INTERIM (scenario). The geographic CONTEXT split of the served base across
US / Europe / Asia-ex-China, summing to 1 (a premium US/EU mix; DESIGN.md
Section 8). Context only: it does NOT weight or drive the cost-vs-ground
verdict (plan Section 0.0 A1)."""

# ============================================================
# Ground bottom-up cost defaults (cost-to-cost denominator; DESIGN.md Section 7)
# ============================================================

GROUND_TOWER_COST_MUSD_PER_SITE_DEFAULT: Final[float] = 0.25
"""INTERIM (scenario). The amortized cellular tower/site build cost, $M per site;
the cost-to-cost denominator capex line (DESIGN.md Section 7). Anchored pending
the Phase-4 ground build."""

GROUND_SITES_PER_MILLION_SUBS_DEFAULT: Final[float] = 300.0
"""INTERIM (scenario). The number of cell sites needed per million subscribers in
the served density; sets how many sites the ground alternative must build to
serve the same customers (DESIGN.md Section 7). Anchored, configurable."""

GROUND_BACKHAUL_COST_MUSD_PER_SITE_YEAR_DEFAULT: Final[float] = 0.02
"""INTERIM (scenario). The annual backhaul/transport cost per site, $M (DESIGN.md
Section 7). Anchored pending the Phase-4 ground build."""

GROUND_OPEX_MUSD_PER_SITE_YEAR_DEFAULT: Final[float] = 0.03
"""INTERIM (scenario). The annual operations and maintenance cost per site, $M
(DESIGN.md Section 7). Anchored pending the Phase-4 ground build."""

GROUND_AMORTIZATION_YEARS_DEFAULT: Final[int] = 10
"""INTERIM (scenario). The years over which the ground site capex is amortized
(DESIGN.md Section 7). Anchored, configurable."""

GROUND_SPECTRUM_COST_MUSD_DEFAULT: Final[float] = 0.0
"""DERIVED (the wash). The ground-side spectrum cost line, carried as an EXPLICIT
zero: spectrum nets out of the cost comparison by construction (plan Section 0.7,
Section 0.9). Not a hidden omission, a visible wash."""

# ============================================================
# Fixed model constants and unit conversions (NOT tunable dials)
# ============================================================

USD_PER_MUSD: Final[float] = 1_000_000.0
"""DERIVED (fixed unit conversion). USD per $M; the solar line is configured in
USD per kW but the four-area sum is in $M, so the solar line is divided by this
to convert USD to $M. Held equal to the data-center USD_PER_MUSD (drift-tested
in test_constants_alignment.py)."""

REVENUE_MULTIPLE: Final[float] = 1.5
"""SCENARIO (fixed model constant). The 1.5x revenue multiple for a 33.3% regular
margin (revenue minus the item's full build-plus-launch-plus-operate cost), held
equal on both the space and the ground side so the comparison is a pure cost-
structure ratio (DESIGN.md Section 7; the comms analog of the DC
RLDC-REVENUE-MULTIPLE-1_5X). Carried as a module constant here, not a config dial;
the founder may move it to config if a sensitivity sweep is wanted."""

MONTHS_PER_YEAR: Final[int] = 12
"""DERIVED (fixed calendar constant). Months per year, used to annualize the
monthly ARPU into the per-customer collectable revenue (arpu_usd_per_month x
MONTHS_PER_YEAR x operator_revenue_share)."""

# ============================================================
# Schema / package / artifact-role constants (Phase 3)
# ============================================================
# The comms analog of the data-center output.py SCHEMA_VERSION and the
# json_output.py MODEL_PACKAGE_NAME / artifact-role labels. Carried here as
# named constants (the "no bare literals" rule) so the engine's metadata and
# meta blocks stamp them without inline literals.

SCHEMA_VERSION: Final[str] = "comms-v1"
"""The comms output JSON schema version (the comms analog of the data-center
output.py SCHEMA_VERSION = 'v8'); distinct so the comms artifact is
unambiguously not the DC v8 artifact."""

MODEL_PACKAGE_NAME: Final[str] = "rklb-comms"
"""The comms model package / console-script name (the Phase-5 rklb-comms entry
point), carried now so the metadata block can stamp it."""

DEFAULT_ARTIFACT_ROLE: Final[str] = "draft"
"""The default artifact-role label for an un-promoted run (the comms analog of
the DC json_output.py DEFAULT_ARTIFACT_ROLE)."""

PROMOTED_DEFAULT_ARTIFACT_ROLE: Final[str] = "promoted_default"
"""The artifact-role label stamped on the promoted default space model (the
comms analog of the DC json_output.py PROMOTED_DEFAULT_ARTIFACT_ROLE)."""

# ============================================================
# Validator tolerances
# ============================================================

SCOPE_WEIGHT_SUM_TOLERANCE: Final[float] = 1e-9
"""DERIVED (epsilon). The absolute tolerance the ScopeWeights validator allows on
abs(us + europe + asia_ex_china - 1.0); a floating-point sum epsilon."""

__all__ = [
    "ARPU_USD_PER_MONTH_DEFAULT",
    "BASE_YEAR_DEFAULT",
    "BEAMS_PER_SAT_DEFAULT",
    "BROADBAND_ANTENNA_COST_MUSD_DEFAULT",
    "BROADBAND_COMMS_ELECTRONICS_COST_MUSD_DEFAULT",
    "BROADBAND_PAYLOAD_POWER_KW_DEFAULT",
    "BROADBAND_RADIATOR_BUS_COST_MUSD_DEFAULT",
    "BROADBAND_SATELLITE_MASS_T_DEFAULT",
    "BROADBAND_SOLAR_COST_USD_PER_KW_DEFAULT",
    "BROADBAND_STOWED_VOLUME_M3_DEFAULT",
    "CADENCE_CEILING_DEFAULT",
    "COST_DOWN_REFERENCE_UNITS_DEFAULT",
    "DEFAULT_ARTIFACT_ROLE",
    "DIRECT_TO_CELL_ANTENNA_COST_MUSD_DEFAULT",
    "DIRECT_TO_CELL_COMMS_ELECTRONICS_COST_MUSD_DEFAULT",
    "DIRECT_TO_CELL_PAYLOAD_POWER_KW_DEFAULT",
    "DIRECT_TO_CELL_RADIATOR_BUS_COST_MUSD_DEFAULT",
    "DIRECT_TO_CELL_SATELLITE_MASS_T_DEFAULT",
    "DIRECT_TO_CELL_SOLAR_COST_USD_PER_KW_DEFAULT",
    "DIRECT_TO_CELL_STOWED_VOLUME_M3_DEFAULT",
    "FIRST_LAUNCH_YEAR_DEFAULT",
    "GROUND_AMORTIZATION_YEARS_DEFAULT",
    "GROUND_BACKHAUL_COST_MUSD_PER_SITE_YEAR_DEFAULT",
    "GROUND_OPEX_MUSD_PER_SITE_YEAR_DEFAULT",
    "GROUND_SITES_PER_MILLION_SUBS_DEFAULT",
    "GROUND_SPECTRUM_COST_MUSD_DEFAULT",
    "GROUND_TOWER_COST_MUSD_PER_SITE_DEFAULT",
    "HIGH_CADENCE_COST_MUSD_DEFAULT",
    "HIGH_CADENCE_LAUNCHES_DEFAULT",
    "HORIZON_YEARS_DEFAULT",
    "LAUNCHES_AT_YEAR_5_DEFAULT",
    "LAUNCHES_AT_YEAR_10_DEFAULT",
    "LEARNING_RATE_PER_DOUBLING_DEFAULT",
    "LEASED_BANDWIDTH_MHZ_DEFAULT",
    "LOW_CADENCE_COST_MUSD_DEFAULT",
    "LOW_CADENCE_LAUNCHES_DEFAULT",
    "MAX_FY",
    "MAX_HORIZON_YEARS",
    "MINOR_COMPONENT_PCT_DEFAULT",
    "MIN_FY",
    "MIN_HORIZON_YEARS",
    "MODEL_PACKAGE_NAME",
    "MONTHS_PER_YEAR",
    "NEUTRON_FAIRING_VOLUME_M3_DEFAULT",
    "NEUTRON_MASS_ENVELOPE_T_DEFAULT",
    "OPERATOR_REVENUE_SHARE_DEFAULT",
    "OVERSUBSCRIPTION_BAND_DEFAULT",
    "PER_BEAM_CAPACITY_ANCHOR_MBPS",
    "PER_BEAM_CAPACITY_ANCHOR_MHZ",
    "PROMOTED_DEFAULT_ARTIFACT_ROLE",
    "RETAIL_REFERENCE_USD_PER_MONTH_DEFAULT",
    "REVENUE_MULTIPLE",
    "SATELLITE_LIFETIME_YEARS_DEFAULT",
    "SCHEMA_VERSION",
    "SCOPE_WEIGHTS_DEFAULT",
    "SCOPE_WEIGHT_SUM_TOLERANCE",
    "SPECTRAL_EFFICIENCY_BPS_PER_HZ_DEFAULT",
    "STEADY_STATE_YEAR_DEFAULT",
    "TARGET_PER_USER_RATE_BAND_DEFAULT",
    "UPGRADED_NEUTRON_FAIRING_VOLUME_M3_DEFAULT",
    "UPGRADED_NEUTRON_MASS_ENVELOPE_T_DEFAULT",
    "USD_PER_MUSD",
    "V4_CAPABILITY_MULTIPLIER_DEFAULT",
]
