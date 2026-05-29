"""Module-level Final[T] named constants.

Every constant carries a docstring with:
- Source class: SOURCED_FACT / ESTIMATE / EXTRAPOLATION / SOURCED_DECISION
- Source citation (file path, research, D-decision)
- Sensitivity-band recommendation where applicable

This module is the single source of truth for the calculator's
"no bare numeric literals" rule (CLAUDE.md). Every dial that is a
fixed constant (not a YAML-tunable Pydantic field) lives here. Claim IDs
refer to `research/SOURCE_INDEX.md`.
"""

from __future__ import annotations

from typing import Final

# ============================================================
# Year-bound constants
# ============================================================

MIN_FY: Final[int] = 2020
"""SOURCED_DECISION (cycle-1). Lower bound for any FY field. Below
this is pre-data-center era; calculator inputs cannot reference
years earlier."""

MAX_FY: Final[int] = 2080
"""SOURCED_DECISION (cycle-1). Upper bound for any FY field. Beyond
this the extrapolation slopes (D12, 25%/gen) have no defensible
basis."""

MIN_HORIZON_YEARS: Final[int] = 5
"""SOURCED_DECISION (cycle-1). Minimum analysis horizon. Below
service-life (D1, 5y) the cliff dominates the trajectory and the
calculator is not informative."""

MAX_HORIZON_YEARS: Final[int] = 20
"""SOURCED_DECISION (cycle-1). Maximum analysis horizon. Beyond
this generation-extrapolation slopes are pure speculation."""

# ============================================================
# Conversion constants
# ============================================================

KG_PER_T: Final[float] = 1000.0
"""SOURCED_FACT. Mass conversion: 1 metric tonne = 1000 kg."""

USD_PER_MUSD: Final[float] = 1_000_000.0
"""SOURCED_FACT. Cost conversion: $1M = $1,000,000."""

# ============================================================
# Physics constants
# ============================================================

SOLAR_CONSTANT_W_M2: Final[float] = 1361.0
"""SOURCED_FACT (THR-002). Solar irradiance at Earth's orbit (AM0).
Used in solar-area-from-kW calculations before array efficiency,
attitude, degradation, and packing losses."""

# ============================================================
# Service life + cadence (D-decisions)
# ============================================================

SERVICE_LIFE_YEARS: Final[int] = 5
"""ESTIMATE/SCENARIO (THR-008, D1). Base-case hard cliff for node
lifetime. After 5 years a node contributes zero revenue; this is a design
target, not a certified GPU field-life fact."""

RELEASE_CADENCE_YR: Final[float] = 1.5
"""SOURCED_DECISION (D7). Time between successive GPU generation
releases (frontier-gen rule), 1.5 yr = 18 months. Cycle-1 field
name `release_cadence_yr` kept."""

# ============================================================
# Trajectory horizon anchor
# ============================================================

HORIZON_ANCHOR_YEARS: Final[int] = 10
"""SOURCED_DECISION (cycle-1 D1 service life). Trajectory horizon
anchor — the cycle-1 linear launch-cost ramp is defined relative to
a fixed 10-year anchor. Migrated from engine.py's Phase-0 temporary
`_HORIZON_ANCHOR_YEARS`."""

# ============================================================
# Mass envelope + bus (D-decisions / R1 estimates)
# ============================================================

MASS_ENVELOPE_T: Final[float] = 12.5
"""ESTIMATE/SCENARIO (NTR-007, D3). Block-upgraded reusable Neutron
SSO mass envelope. This is the default model case, not a Rocket Lab
published payload figure."""

NODE_MASS_FIXED_T: Final[float] = 2.5
"""ESTIMATE. Fixed node mass (bus + structure + ADCS). Cycle-1
value 2.5 KEPT verbatim (peer-review blocker 3: an earlier draft
wrongly set this to 2.0, a silent 20% model change). Cycle-1 field
name `node_mass_fixed_t`."""

NODE_VOLUME_FIXED_M3: Final[float] = 5.0
"""ESTIMATE. Fixed node stowed volume (bus + structure). NEW field
for the cycle-2 volume model — cycle-1 had no volume term.
Sensitivity: +/-2 m3."""

# ============================================================
# Cycle-1 cost dials (kept verbatim — engine cost-breakdown reads
# these; peer-review blocker 3: dropping them breaks the cost math)
# ============================================================

BUS_BASE_MUSD: Final[float] = 8.0
"""ESTIMATE (cycle-1). Bus cost base. Engine `bus_musd` formula:
bus_base_musd x (1 + bus_growth_pre) ** pre_years."""

BUS_GROWTH_PRE: Final[float] = -0.03
"""ESTIMATE (cycle-1). Bus cost growth rate before flatten year."""

BUS_FLATTEN_AFTER_YR: Final[int] = 5
"""ESTIMATE (cycle-1). Year after which bus cost flattens."""

SOLAR_COST_MUSD_PER_KW: Final[float] = 0.04
"""ESTIMATE (cycle-1). Solar cost per kW. Engine `solar_musd` =
solar_cost_musd_per_kw x node_kw."""

RADIATOR_COST_MUSD_PER_KW: Final[float] = 0.04
"""ESTIMATE (cycle-1). Radiator cost per kW. Engine `radiator_musd`
= radiator_cost_musd_per_kw x node_kw."""

# ============================================================
# Solar + radiator MASS dials (R1 sourced + corrected)
# ============================================================

SOLAR_MASS_T_PER_KW: Final[float] = 0.011
"""SOURCED/ESTIMATE (THR-006, THR-007). Solar specific mass planning
dial. Range 0.010-0.012 t/kW; central 0.011. Cycle-1 field name
`solar_mass_t_per_kw`."""

RADIATOR_T_PER_KW_PRE: Final[float] = 0.013
"""ESTIMATE (cycle-1). Radiator specific mass before Tjmax lift.
Active for years 0..TJMAX_LIFT_YEAR-1."""

RADIATOR_T_PER_KW_POST: Final[float] = 0.012
"""SOURCED_ESTIMATE (R1). Radiator specific mass for single-face
co-mounted architecture (D16) post-Tjmax. Central of 0.010-0.014
R1 band. Replaces cycle-1's 0.007 (which was the optimistic
two-face value). Active for years TJMAX_LIFT_YEAR and beyond."""

TJMAX_LIFT_YEAR: Final[int] = 5
"""SOURCED_DECISION (D11). Year at which radiator dial transitions
from pre-Tjmax to post-Tjmax value."""

# ============================================================
# Slopes (D12)
# ============================================================

FLOPS_PER_KW_PCT_PER_GEN_POST_FEYNMAN: Final[float] = 0.25
"""EXTRAPOLATION (D12). FLOPS/kW improvement per generation post-
Feynman. Central 25%; sensitivity 15-35%."""

# ============================================================
# Cadence defaults (scenario dials retained from v7 archaeology, commit 8fdc210)
# ============================================================

CADENCE_CEILING_DEFAULT: Final[int] = 150
"""ESTIMATE/SCENARIO (NTR-010; v7 archaeology). Hard cap on launches
per year; venture-model scenario, not Rocket Lab guidance."""

LAUNCHES_AT_YEAR_5_DEFAULT: Final[int] = 14
"""ESTIMATE/SCENARIO (NTR-010; v7 archaeology). Logistic anchor at
model year 5. Public launch counts are integer missions, not fractional
rates."""

LAUNCHES_AT_YEAR_10_DEFAULT: Final[int] = 90
"""ESTIMATE/SCENARIO (NTR-010; v7 archaeology). Logistic anchor at
model year 10; high-cadence venture scenario. With base year 2026, this
anchors FY2036 at about 90 launches."""

FIRST_LAUNCH_YEAR_DEFAULT: Final[int] = 1
"""ESTIMATE/SCENARIO (NTR-011; v7 archaeology). First venture launch
index (FY2027 if base_year=2026), downstream of Rocket Lab's forward-
looking late-2026 Neutron first-flight target."""

# ============================================================
# Launch cost dials (lifted verbatim from v7)
# ============================================================

LOW_CADENCE_COST_MUSD_DEFAULT: Final[float] = 25.0
"""ESTIMATE (NTR-009). Launch cost at low cadence (<=5 launches/yr).
Use as a cadence-specific model estimate, not a certified internal
Rocket Lab cost."""

HIGH_CADENCE_COST_MUSD_DEFAULT: Final[float] = 13.5
"""ESTIMATE (NTR-009). Launch cost at high cadence (>=100 launches/yr).
Learning-curve scenario inside the $12-15M very-high-cadence band."""

LOW_CADENCE_LAUNCHES_DEFAULT: Final[float] = 5.0
"""ESTIMATE (NTR-009). Cadence at low-cost anchor."""

HIGH_CADENCE_LAUNCHES_DEFAULT: Final[float] = 100.0
"""ESTIMATE (NTR-009, NTR-010). Cadence at high-cost anchor; model
scenario, not published Rocket Lab guidance."""

# ============================================================
# Volume dials (R1 sourced)
# ============================================================

SI_AREAL_DENSITY_KG_M2: Final[float] = 2.0
"""SOURCED/ESTIMATE (THR-006, THR-007). Published/planning central
of 1.6-2.0 kg/m2; peer-review correction from earlier 1.8 draft. Full
Si array areal density including structure."""

SI_BOL_EFFICIENCY: Final[float] = 0.20
"""SOURCED (THR-007). Si BOL AM0 efficiency planning dial for Rocket
Lab/Solestial-class silicon arrays."""

FOLD_RATIO: Final[float] = 80.0
"""SOURCED (THR-006). Deployed-to-stowed area ratio for ROSA-class
deployable-array planning."""

STOWED_PITCH_MM: Final[float] = 6.0
"""ESTIMATE (R1 build-up; not published). Per-panel stowed
thickness with Si + co-mounted radiator."""

RADIATOR_SOLAR_AREA_RATIO: Final[float] = 0.70
"""SOURCED/ESTIMATE (THR-003, THR-004). Radiator area / solar area
for the single-face co-mounted architecture."""

MOUNTING_OVERHEAD_PCT: Final[float] = 0.30
"""SOURCED/ESTIMATE (THR-006). Mass/volume overhead from hinges,
yokes, motors."""

NEUTRON_FAIRING_USABLE_VOLUME_M3: Final[float] = 80.0
"""ESTIMATE (R1 from wiki). Neutron fairing usable payload
volume. NOT RKLB-published; needs follow-up source."""

# ============================================================
# R-band defaults (scenario revenue-to-cost trajectories)
# ============================================================

R_BAND_CENTRAL_ANCHORS_DEFAULT: Final[tuple[tuple[int, float], ...]] = (
    (2026, 1.50),
    (2028, 1.50),
    (2030, 1.50),
    (2032, 1.50),
    (2034, 1.50),
    (2036, 1.50),
)
"""ESTIMATE/SCENARIO (REV-008). Central R trajectory anchors (6
anchors). Engine linearly interpolates between adjacent anchors. Flat at
R=1.50 with no taper: each cohort launches fresh and earns a constant 33.3%
gross margin across its five-year life. Kept as six anchors so any year can
be re-shaped per scenario (see scenarios/default.yaml)."""

R_BAND_LOW_ANCHORS_DEFAULT: Final[tuple[tuple[int, float], ...]] = (
    (2026, 1.20),
    (2028, 1.20),
    (2030, 1.20),
    (2032, 1.20),
    (2034, 1.20),
    (2036, 1.20),
)
"""ESTIMATE/SCENARIO (REV-008). Low R trajectory (6 anchors, flat at
1.20). Bear case sits near the neocloud post-depreciation survival floor."""

R_BAND_HIGH_ANCHORS_DEFAULT: Final[tuple[tuple[int, float], ...]] = (
    (2026, 1.80),
    (2028, 1.80),
    (2030, 1.80),
    (2032, 1.80),
    (2034, 1.80),
    (2036, 1.80),
)
"""ESTIMATE/SCENARIO (REV-008). High R trajectory (6 anchors, flat at
1.80). Bull case holds a durable premium with no modeled taper."""
