"""Module-level Final[T] named constants.

Every constant carries a docstring with:
- Source class: SOURCED_FACT / ESTIMATE / EXTRAPOLATION / SOURCED_DECISION
- Source citation (file path, research, D-decision)
- Sensitivity-band recommendation where applicable

This module is the single source of truth for the calculator's
"no bare numeric literals" rule (CLAUDE.md). Every dial that is a
fixed constant (not a YAML-tunable Pydantic field) lives here, except the
eight cadence and launch-cost defaults, which both ventures share and which
live once in :mod:`common.cadence`. Claim IDs refer to
`research/SOURCE_INDEX.md`.
"""

from __future__ import annotations

import logging
from typing import Final

from common.cadence import YEAR_10_ANCHOR_IDX

logger = logging.getLogger(__name__)

# ============================================================
# Year-bound constants
# ============================================================

MIN_FY: Final[int] = 2020
"""SOURCED_DECISION (cycle-1). Lower bound for any FY field. Below
this is pre-data-center era; calculator inputs cannot reference
years earlier."""

MAX_FY: Final[int] = 2080
"""SOURCED_DECISION (cycle-1). Upper bound for any FY field. Beyond
this the post-Feynman extrapolation slopes (D12) have no defensible
basis."""

MIN_HORIZON_YEARS: Final[int] = 5
"""SOURCED_DECISION (cycle-1). Minimum analysis horizon. Below
service-life (D1, 5y) the cliff dominates the trajectory and the
calculator is not informative."""

MAX_HORIZON_YEARS: Final[int] = 20
"""SOURCED_DECISION (cycle-1). Maximum analysis horizon. Beyond
this generation-extrapolation slopes are pure speculation."""

ANCHOR_MODEL_YEAR: Final[int] = int(YEAR_10_ANCHOR_IDX)
"""SOURCED_DECISION (NTR-010 year-10 cadence anchor; ADR-003). Model-year
index of the run's anchor year: the year the ``launches_at_year_10`` cadence
anchor pins, which is also the deployed-year cohort the ground reference
compares against and the year the headline checks and query examples read.
Taken from :data:`common.cadence.YEAR_10_ANCHOR_IDX` so the anchor year and
the cadence anchor cannot drift apart. With ``base_year`` 2026 it resolves to
FY2036. :func:`data_center.config.anchor_year` falls back to the final
window year when the horizon is shorter than this."""

GENERATION_EXTENSION_LOOKAHEAD_YEARS: Final[int] = 1
"""SOURCED_DECISION (cycle-1 engine rule). Years past the final window year
that the generation list is extended to cover, so the final year's frontier
generation is always resolved from a list that reaches beyond it. The window
end plus this lookahead must stay within :data:`MAX_FY`, the upper bound on
any generation's ``year_available``."""

# ============================================================
# Conversion constants
# ============================================================

KG_PER_T: Final[float] = 1000.0
"""SOURCED_FACT. Mass conversion: 1 metric tonne = 1000 kg."""

USD_PER_MUSD: Final[float] = 1_000_000.0
"""SOURCED_FACT. Cost conversion: $1M = $1,000,000."""

W_PER_KW: Final[float] = 1000.0
"""SOURCED_FACT. Power conversion: 1 kW = 1000 W."""

MM_PER_M: Final[float] = 1000.0
"""SOURCED_FACT. Length conversion: 1 m = 1000 mm."""

# ============================================================
# Numerical tolerances
# ============================================================

PACKAGE_FIT_TOLERANCE: Final[float] = 1e-9
"""SOURCED_DECISION (numerical). Slack, in packages, added before flooring
the package count (:func:`data_center.engine.compute_n_packages`). At an
exact fit the float division lands a few ulps short of the whole number
(``10.5 / 0.07500000000000001`` is ``139.99999999999997``) and a bare floor
would drop a package that fits. The price of the slack: a fit short by less
than a billionth of a package also keeps its last package, so an accepted
node can exceed the mass envelope by up to this fraction of one package's
mass (milligrams for a tonne-class package). V1 derives its upper-bound slack
from this value, so every fit the packer accepts passes V1."""

PERCENT_PER_FRACTION: Final[float] = 100.0
"""SOURCED_FACT (arithmetic). Conversion from a 0-1 fraction to a percent."""

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
for the cycle-2 volume model. Cycle-1 had no volume term.
Sensitivity: +/-2 m3."""

# ============================================================
# Cycle-1 cost dials (kept verbatim: engine cost-breakdown reads
# these; peer-review blocker 3: dropping them breaks the cost math)
# ============================================================

BUS_BASE_MUSD: Final[float] = 8.0
"""ESTIMATE (cycle-1). Bus cost base. Engine `bus_musd` formula:
bus_base_musd x (1 + bus_growth_pre) ** pre_years."""

BUS_GROWTH_PRE: Final[float] = -0.03
"""ESTIMATE (cycle-1). Bus cost growth rate before flatten year."""

BUS_GROWTH_PRE_FLOOR: Final[float] = -1.0
"""SOURCED_FACT (arithmetic). Exclusive lower bound on ``bus_growth_pre``:
the bus cost compounds as ``(1 + bus_growth_pre) ** years``, so a rate of
-100% zeroes the bus and anything below it flips the cost's sign year by
year."""

BUS_FLATTEN_AFTER_YR: Final[int] = 5
"""ESTIMATE (cycle-1). Year after which bus cost flattens."""

SOLAR_COST_MUSD_PER_KW: Final[float] = 0.02
"""INVESTOR_SET (2026-07-14; was the uncited cycle-1 0.04). Solar cost per
kW of flown power. Engine `solar_musd` = solar_cost_musd_per_kw x node_kw.
Rationale is manufacturing scale, deliberately NOT the thermal/area win
(that is booked in the mass dials): Rocket Lab's own silicon-array program
("low cost per watt at industrial scale", the SolAero vertical integration
internalizing supplier margin), a five-year LEO life against legacy
10-to-20-year space-grade references, and market signals near $11-15/W
(THR-013, research/node_design/space_solar_costdown_2030_2036.md: the
$20k/kW aggressive-but-plausible 2036 case, adopted as the investor-set
default; the old 0.04 stays the labeled conservative exception). A
refreshed 2026-07 cost analysis is tracked in research/node_design/."""

RADIATOR_COST_MUSD_PER_KW: Final[float] = 0.02
"""INVESTOR_SET (2026-07-14; was the uncited cycle-1 0.04, itself set equal
to solar by convenience and the ledger's least-sourced dial). Radiator cost
per kW of rejected power. Engine `radiator_musd` = radiator_cost_musd_per_kw
x node_kw. The weaker leg of the 20/20 pair and labeled so: no public $/kW
radiator data exists (THR-016; the stated evidence gate is a vendor quote or
bottom-up BOM, open research). Rationale is productized repetition at
assembly-line scale with in-house integration, NOT the temperature/area win
(booked in the mass dials). Sanity check, not justification: at the
1.65 kg/kW light radiator this dial pays about $12k per kg of hardware,
roughly 3.6x the per-kg rate the old 0.04 dial implied on the 12 kg/kW
co-mounted radiator, so it does not underprice the smaller hardware
(research/node_design/radiator_costdown_2030_2036.md carries the bands:
$20k upside / $30-40k central / $60-100k stress)."""

# ============================================================
# Solar + radiator MASS dials (R1 sourced + corrected)
# ============================================================

SOLAR_MASS_T_PER_KW: Final[float] = 0.011
"""SOURCED/ESTIMATE (RLDC-SOLAR-RADIATOR-MASS, ledger status scenario;
supporting THR-006, THR-007). Solar specific mass planning dial, not a
Rocket Lab array specification. Range 0.010-0.012 t/kW; central 0.011.
Cycle-1 field name `solar_mass_t_per_kw`."""

RADIATOR_T_PER_KW_PRE: Final[float] = 0.00165
"""INVESTOR_SET (2026-07-14). Radiator specific mass, held flat with the
post dial: the AI-1-class deployed double-sided run-hot radiator is
asserted from day one, so the Tjmax step is inert. Within 10 percent of
AI-1's implied 0.0015 t/kW (110 m2 double-sided at 120 kW, and the
whole-satellite 70 kW/t budget independently forcing the ~1.5 kg/kW
class). Pairs with RadiatorArchitecture.DEPLOYED_DOUBLE_SIDED; the old
co-mounted 0.013/0.012 posture (R1 band 0.010-0.014, D16/D17) stays the
labeled conservative exception, and V17 still enforces its floor whenever
the co-mounted architecture is selected."""

RADIATOR_T_PER_KW_POST: Final[float] = 0.00165
"""INVESTOR_SET (2026-07-14). Radiator specific mass post-Tjmax, equal to
the pre dial (see RADIATOR_T_PER_KW_PRE: the hot radiator is asserted now,
AI-1 style, not deferred to a year-5 step). The temperature/architecture
win is booked HERE in mass, never in the cost dials (the decomposition
discipline in research/node_design/gpu_temperature_cooling_limits.md)."""

TJMAX_LIFT_YEAR: Final[int] = 5
"""SOURCED_DECISION (D11). Year at which the radiator dial transitions
from pre-Tjmax to post-Tjmax value. Inert under the 2026-07-14 posture
(pre == post); kept for the conservative-exception scenario where the
step is real."""

# ============================================================
# Slopes (D12)
# ============================================================

USD_GROWTH_PER_GEN_DEFAULT: Final[float] = 0.30
"""EXTRAPOLATION (GPU-012). Default post-Feynman $/package growth per
generation (+30%). The single source for the
:class:`data_center.generations.GenerationSlopes` field default."""

KW_GROWTH_PER_GEN_DEFAULT: Final[float] = 0.20
"""EXTRAPOLATION (GPU-010). Default post-Feynman per-package power growth
per generation (+20%), corrected from 0.30 by validation V-A: 0.30 was the
assembly-level growth rate, which double-counts when applied per package.
The single source for the :class:`data_center.generations.GenerationSlopes`
field default."""

KG_GROWTH_PER_GEN_DEFAULT: Final[float] = -0.10
"""EXTRAPOLATION (GPU-010). Default post-Feynman per-package mass growth per
generation (-10%, denser packaging). The single source for the
:class:`data_center.generations.GenerationSlopes` field default."""

PF_GROWTH_PER_GEN_DEFAULT: Final[float] = 0.625
"""EXTRAPOLATION (GPU-010). Default post-Feynman per-package dense-FP4
PFLOPS growth per generation (+62.5%). The single source for the
:class:`data_center.generations.GenerationSlopes` field default."""

GENERATION_SLOPE_MIN: Final[float] = -0.5
"""SOURCED_DECISION (cycle-1). Lower bound on any per-generation growth
slope: a generation may lose at most half of a quantity; a steeper per-step
collapse has no roadmap basis."""

GENERATION_SLOPE_MAX: Final[float] = 2.0
"""SOURCED_DECISION (cycle-1). Upper bound on any per-generation growth
slope: at most a tripling per generation; beyond it the extrapolation is
pure speculation."""

# ============================================================
# Volume dials (R1 sourced)
# ============================================================

SI_BOL_EFFICIENCY: Final[float] = 0.20
"""SOURCED (THR-007). Si BOL AM0 efficiency planning dial for Rocket
Lab/Solestial-class silicon arrays."""

STOWED_PITCH_MM: Final[float] = 6.0
"""ESTIMATE (R1 build-up; not published). Per-panel stowed
thickness with Si + co-mounted radiator."""

MOUNTING_OVERHEAD_PCT: Final[float] = 0.30
"""SOURCED/ESTIMATE (THR-006). Mass/volume overhead from hinges,
yokes, motors."""

NEUTRON_FAIRING_USABLE_VOLUME_M3: Final[float] = 80.0
"""ESTIMATE (RLDC-FAIRING-VOLUME-80M3, ledger status scenario). Neutron
fairing usable payload volume for the volume transparency check. NOT
RKLB-published: the low end of the project's about 80 to 95 m3
practical-envelope estimate (research/node_design/node_mass_model.md
Section 7)."""

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
