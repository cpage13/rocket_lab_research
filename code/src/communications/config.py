"""The dial schema and YAML loader for the communications model.

This module defines the INPUT contract of the communications model: a typed,
validated Pydantic :class:`CommsConfig` whose blocks carry every founder-set
dial from the design, plus the ``config_from_dict`` / ``load_config`` YAML
loader pair. Nothing here computes a cost, a capacity, a customer count, or a
comparison; it is the contract the engine-room modules (Phase 2) and the engine
(Phase 3) consume.

The blocks:

* ``metadata: MetadataDials`` - base year, horizon, steady-state year.
* ``constellation: ConstellationDials`` - the two satellite classes (broadband,
  direct-to-cell), each with its four cost areas (antenna, comms electronics,
  solar, radiator/bus) and packing inputs (mass, stowed volume), plus the
  service-life cliff, the V4 capability step, and the Neutron-envelope options.
* ``launch: LaunchDials`` - the cadence and launch-cost dials reused verbatim
  from the shared ``common.cadence`` machinery, plus the Neutron mass/volume
  envelopes (baseline and upgraded).
* ``cost_down: CostDownDials`` - the satellite learning-curve dial (a fractional
  reduction per doubling of cumulative units built).
* ``spectrum: SpectrumDials`` - the spectrum mechanism dials (leased MHz, the
  cross-check spectral efficiency, beams per satellite, and the per-user-rate /
  oversubscription bands that force the customer output to a band).
* ``price_reference: PriceReferenceDials`` - the price/collectability references
  (the founder-set retail reference, ARPU, operator revenue share) and the
  geographic scope context. This block is NOT demand: demand is assumed, not
  modeled (plan Section 0.0 Amendment A1).
* ``ground: GroundDials`` - the bottom-up ground (cellular) cost build, the
  cost-to-cost denominator.
* ``scenario_levers: ScenarioLevers`` - the scenario identity.

The model is Neutron-only and cost-driven: no capture-share dial, the launch
vehicle is Neutron (with an upgraded-Neutron option) and nothing heavier, no
baked-in verdict, and (per Amendment A1) no demand lever of any kind (no
top-down market projection, growth dial, or take-up fraction). Demand is
assumed: if the delivered price undercuts what ground charges and that price is
collectable, the customers follow. The whole question the model answers is
whether the bottom-up cost compares favorably to ground.

YAML loading: scenario files are YAML mappings whose top-level keys are the
block names above, all optional (omitted = defaults). ``extra="forbid"`` means a
typo in a scenario file fails loudly.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any  # typing-acceptable: Any types the dict deserialization boundary

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

# The eight cadence / launch-cost defaults are re-exported by
# communications.constants from the shared common.cadence spine, so the comms
# config reads the same anchors the data-center cadence machinery uses.
from communications.constants import (
    ARPU_USD_PER_MONTH_DEFAULT,
    BASE_YEAR_DEFAULT,
    BEAMS_PER_SAT_DEFAULT,
    BROADBAND_ANTENNA_COST_MUSD_DEFAULT,
    BROADBAND_COMMS_ELECTRONICS_COST_MUSD_DEFAULT,
    BROADBAND_PAYLOAD_POWER_KW_DEFAULT,
    BROADBAND_RADIATOR_BUS_COST_MUSD_DEFAULT,
    BROADBAND_SATELLITE_MASS_T_DEFAULT,
    BROADBAND_SOLAR_COST_USD_PER_KW_DEFAULT,
    BROADBAND_STOWED_VOLUME_M3_DEFAULT,
    CADENCE_CEILING_DEFAULT,
    COST_DOWN_REFERENCE_UNITS_DEFAULT,
    DIRECT_TO_CELL_ANTENNA_COST_MUSD_DEFAULT,
    DIRECT_TO_CELL_COMMS_ELECTRONICS_COST_MUSD_DEFAULT,
    DIRECT_TO_CELL_PAYLOAD_POWER_KW_DEFAULT,
    DIRECT_TO_CELL_RADIATOR_BUS_COST_MUSD_DEFAULT,
    DIRECT_TO_CELL_SATELLITE_MASS_T_DEFAULT,
    DIRECT_TO_CELL_SOLAR_COST_USD_PER_KW_DEFAULT,
    DIRECT_TO_CELL_STOWED_VOLUME_M3_DEFAULT,
    FIRST_LAUNCH_YEAR_DEFAULT,
    GROUND_AMORTIZATION_YEARS_DEFAULT,
    GROUND_BACKHAUL_COST_MUSD_PER_SITE_YEAR_DEFAULT,
    GROUND_OPEX_MUSD_PER_SITE_YEAR_DEFAULT,
    GROUND_SITES_PER_MILLION_SUBS_DEFAULT,
    GROUND_SPECTRUM_COST_MUSD_DEFAULT,
    GROUND_TOWER_COST_MUSD_PER_SITE_DEFAULT,
    HIGH_CADENCE_COST_MUSD_DEFAULT,
    HIGH_CADENCE_LAUNCHES_DEFAULT,
    HORIZON_YEARS_DEFAULT,
    LAUNCHES_AT_YEAR_5_DEFAULT,
    LAUNCHES_AT_YEAR_10_DEFAULT,
    LEARNING_RATE_PER_DOUBLING_DEFAULT,
    LEASED_BANDWIDTH_MHZ_DEFAULT,
    LOW_CADENCE_COST_MUSD_DEFAULT,
    LOW_CADENCE_LAUNCHES_DEFAULT,
    MAX_FY,
    MAX_HORIZON_YEARS,
    MIN_FY,
    MIN_HORIZON_YEARS,
    MINOR_COMPONENT_PCT_DEFAULT,
    NEUTRON_FAIRING_VOLUME_M3_DEFAULT,
    NEUTRON_MASS_ENVELOPE_T_DEFAULT,
    OPERATOR_REVENUE_SHARE_DEFAULT,
    OVERSUBSCRIPTION_BAND_DEFAULT,
    RETAIL_REFERENCE_USD_PER_MONTH_DEFAULT,
    SATELLITE_LIFETIME_YEARS_DEFAULT,
    SCOPE_WEIGHT_SUM_TOLERANCE,
    SCOPE_WEIGHTS_DEFAULT,
    SPECTRAL_EFFICIENCY_BPS_PER_HZ_DEFAULT,
    STEADY_STATE_YEAR_DEFAULT,
    TARGET_PER_USER_RATE_BAND_DEFAULT,
    UPGRADED_NEUTRON_FAIRING_VOLUME_M3_DEFAULT,
    UPGRADED_NEUTRON_MASS_ENVELOPE_T_DEFAULT,
    V4_CAPABILITY_MULTIPLIER_DEFAULT,
)

logger = logging.getLogger(__name__)


# ===========================================================================
# 1. Small shared value blocks
# ===========================================================================


class BandTriple(BaseModel):
    """A generic ascending-magnitude (low <= mid <= high) triple of positive values.

    This is a GENERIC magnitude triple: the same validator serves the
    per-user-rate band and the oversubscription band. It is NOT a
    customer-band-semantic ordering. Both default triples are stored with their
    fields in raw ascending numeric order so the validator passes at
    construction. The "low/mid/high" label only flips meaning downstream, between
    this raw-magnitude input and the customer output (a higher per-user rate
    provisions a fatter pipe and serves FEWER subscribers, so the Phase-2 chain
    consumes the rate triple in reverse).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    low: float = Field(gt=0, description="The low (smallest-magnitude) band member.")
    mid: float = Field(gt=0, description="The mid band member.")
    high: float = Field(gt=0, description="The high (largest-magnitude) band member.")

    @model_validator(mode="after")
    def _ordered(self) -> BandTriple:
        """Enforce low <= mid <= high as raw magnitudes."""
        if not self.low <= self.mid <= self.high:
            raise ValueError("band must satisfy low <= mid <= high")
        return self


class ScopeWeights(BaseModel):
    """The geographic split of the served base across US / Europe / Asia-ex-China.

    The three fractions sum to 1 (validated within a small tolerance). This is
    GEOGRAPHIC CONTEXT only (which target regions the served base sits in); it
    does NOT weight or drive the cost-vs-ground verdict (plan Section 0.0
    Amendment A1).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    us: float = Field(ge=0, le=1, description="Fraction of the served base in the US.")
    europe: float = Field(ge=0, le=1, description="Fraction of the served base in Europe.")
    asia_ex_china: float = Field(
        ge=0,
        le=1,
        description="Fraction of the served base in Asia excluding China.",
    )

    @model_validator(mode="after")
    def _sums_to_one(self) -> ScopeWeights:
        """Enforce that the three scope weights sum to 1 within tolerance."""
        total = self.us + self.europe + self.asia_ex_china
        if abs(total - 1.0) > SCOPE_WEIGHT_SUM_TOLERANCE:
            raise ValueError(
                f"scope weights must sum to 1 (got {total}, tolerance {SCOPE_WEIGHT_SUM_TOLERANCE})"
            )
        return self


# ===========================================================================
# 2. The dial blocks
# ===========================================================================


class MetadataDials(BaseModel):
    """Run metadata: the base year, the horizon, and the steady-state year.

    Mirrors the data-center metadata block but carries NO workload / operator /
    radiator enums (those are GPU-venture locks with no comms analog). The
    steady-state year is the year the headline mature figure is read at; the
    headline-vs-timeseries choice itself is a Phase-3 decision (concern C1), but
    the year is a config input here.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    base_year: int = Field(
        ge=MIN_FY,
        le=MAX_FY,
        description="Calendar year corresponding to model year 0.",
    )
    horizon_years: int = Field(
        ge=MIN_HORIZON_YEARS,
        le=MAX_HORIZON_YEARS,
        description="Number of fiscal-year steps after year 0.",
    )
    steady_state_year: int = Field(
        ge=MIN_FY,
        le=MAX_FY,
        description="The year the headline mature steady-state figure is read at.",
    )

    @model_validator(mode="after")
    def _steady_state_within_window(self) -> MetadataDials:
        """Enforce base_year <= steady_state_year <= base_year + horizon_years."""
        if not self.base_year <= self.steady_state_year <= self.base_year + self.horizon_years:
            raise ValueError(
                "steady_state_year must satisfy "
                "base_year <= steady_state_year <= base_year + horizon_years"
            )
        return self


class SatelliteClassDials(BaseModel):
    """The four cost areas and packing inputs for ONE satellite class.

    The comms model has TWO classes (the per-class fork): BROADBAND (V3-class,
    mass-bound, about 5 per launch) and DIRECT_TO_CELL (antenna-stow /
    volume-bound, about 1 per launch). The top-level config carries one
    instance per class. This block carries NO ``satellites_per_launch`` field:
    that is COMPUTED in Phase 2 from the mass and stowed-volume inputs against
    the Neutron envelope (the fork binds on mass for broadband, volume for
    direct-to-cell). A hand-set satellites-per-launch would be the
    blanket-mass-binds disaster the gate forbids.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    antenna_cost_musd: float = Field(
        gt=0,
        description=(
            "The phased-array aperture cost, $M; the dominant high-value line "
            "(the comms analog of the DC compute line). Bill-of-materials-"
            "derived, INTERIM until the antenna BOM lands."
        ),
    )
    comms_electronics_cost_musd: float = Field(
        gt=0,
        description=(
            "The comms electronics cost (modems, beam-forming, on-board "
            "processing, the RF chain), $M; broken out separately. Bill-of-"
            "materials-derived, INTERIM."
        ),
    )
    solar_cost_usd_per_kw: float = Field(
        gt=0,
        description=(
            "The power-array cost per kW of comms-payload power, USD per kW "
            "(NOT MUSD per kW; the engine converts). About $20k/kW, explicitly "
            "NOT the DC $40k/kW. INTERIM, configurable."
        ),
    )
    payload_power_kw: float = Field(
        gt=0,
        description=(
            "The comms-payload power draw, kW (tens of kW, far below the DC "
            "node's roughly 400 kW). Sizes the solar line in Phase 2. "
            "NEEDS-RESEARCH / INTERIM, per-class."
        ),
    )
    radiator_bus_cost_musd: float = Field(
        gt=0,
        description=(
            "The spacecraft bus (structure, avionics, propulsion) plus thermal "
            "cost, $M; grouped because the radiator is minor at this power. "
            "Anchored light and AI-1-class. INTERIM, configurable."
        ),
    )
    satellite_mass_t: float = Field(
        gt=0,
        description=(
            "The per-satellite wet mass, tonnes; the mass bound divides the "
            "Neutron mass envelope by this. Broadband about 1.5 t; direct-to-"
            "cell heavier (antenna-heavy)."
        ),
    )
    stowed_volume_m3: float = Field(
        gt=0,
        description=(
            "The per-satellite stowed (folded) volume in the fairing, cubic "
            "meters; the volume bound divides the fairing volume by this. "
            "Direct-to-cell is large (the folded antenna fills the fairing "
            "before the mass limit), broadband smaller."
        ),
    )
    minor_component_pct: float = Field(
        ge=0,
        lt=1,
        default=MINOR_COMPONENT_PCT_DEFAULT,
        description=(
            "A configurable fraction of the satellite carried for a minor "
            "component the model does not break out (about 1%). Applied in "
            "Phase 2."
        ),
    )


class ConstellationDials(BaseModel):
    """The constellation-level block: the two satellite classes plus lifetime, V4, vehicle.

    Holds the two :class:`SatelliteClassDials` (broadband, direct-to-cell), the
    service-life cliff, the V4 capability step, and the launch-envelope flags.
    The two classes use named builders because their defaults differ by class
    (broadband cheaper / lighter, direct-to-cell antenna-heavy).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    broadband: SatelliteClassDials = Field(
        default_factory=lambda: _default_broadband_class(),
        description="The V3-class broadband satellite (mass-bound, about 5 per launch).",
    )
    direct_to_cell: SatelliteClassDials = Field(
        default_factory=lambda: _default_direct_to_cell_class(),
        description=(
            "The direct-to-cell satellite (antenna-stow / volume-bound, about 1 per launch)."
        ),
    )
    satellite_lifetime_years: int = Field(
        default=SATELLITE_LIFETIME_YEARS_DEFAULT,
        ge=1,
        le=20,
        description="The satellite service-life cliff, years (5 default, test 7, NOT 3).",
    )
    v4_capability_multiplier: float = Field(
        default=V4_CAPABILITY_MULTIPLIER_DEFAULT,
        gt=0,
        description=(
            "The V4 capability step from the V1/V2/V3 trend; a dimensionless "
            "multiplier, 1.0 = no step (the base case is the V3-class anchor). "
            "Phase 2 applies it."
        ),
    )
    upgraded_neutron: bool = Field(
        default=False,
        description=(
            "The upgraded-Neutron option (bigger fairing, more mass). False = "
            "baseline Neutron; when True, Phase 2 uses the upgraded envelope."
        ),
    )
    low_inclination_leo: bool = Field(
        default=True,
        description=(
            "Comms does not need sun-synchronous orbit, so low-inclination LEO "
            "carries more mass than the SSO case. True = low-inclination LEO "
            "(the comms default)."
        ),
    )


class LaunchDials(BaseModel):
    """The cadence and launch-cost reuse dials plus the Neutron envelopes.

    The cadence and launch-cost fields carry the SAME names, bounds, and
    defaults the shared ``common.cadence`` machinery consumes, so
    ``common.cadence.compute_launches_per_year`` and
    ``common.cadence.compute_launch_cost_musd`` consume them unchanged. The
    Neutron mass / fairing-volume envelopes (baseline and upgraded) are
    comms-specific and feed the Phase-2 satellites-per-launch fork. There is no
    heavier-vehicle envelope: the vehicle is Neutron with an upgraded-Neutron
    option only.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    cadence_ceiling: int = Field(
        default=CADENCE_CEILING_DEFAULT,
        gt=0,
        description="Hard cap on whole-number launches per year.",
    )
    launches_at_year_5: int = Field(
        default=LAUNCHES_AT_YEAR_5_DEFAULT,
        ge=0,
        description="Integer logistic anchor: launches per year at model year 5.",
    )
    launches_at_year_10: int = Field(
        default=LAUNCHES_AT_YEAR_10_DEFAULT,
        ge=0,
        description=(
            "Integer logistic anchor: launches per year at model year 10 "
            "(the 90-launches-by-2036 cadence)."
        ),
    )
    first_launch_year: int = Field(
        default=FIRST_LAUNCH_YEAR_DEFAULT,
        ge=0,
        description="Model-year index before which launch count is clamped to zero.",
    )
    low_cadence_cost_musd: float = Field(
        default=LOW_CADENCE_COST_MUSD_DEFAULT,
        gt=0,
        description="Launch cost at the low-cadence anchor, $M.",
    )
    high_cadence_cost_musd: float = Field(
        default=HIGH_CADENCE_COST_MUSD_DEFAULT,
        gt=0,
        description=(
            "Launch cost at the high-cadence anchor, $M (about $13M to $13.5M "
            "per Neutron flight at target cadence)."
        ),
    )
    low_cadence_launches: float = Field(
        default=LOW_CADENCE_LAUNCHES_DEFAULT,
        gt=0,
        description="Cadence at the low-cost anchor (launches per year).",
    )
    high_cadence_launches: float = Field(
        default=HIGH_CADENCE_LAUNCHES_DEFAULT,
        gt=0,
        description="Cadence at the high-cost anchor (launches per year).",
    )
    neutron_mass_envelope_t: float = Field(
        default=NEUTRON_MASS_ENVELOPE_T_DEFAULT,
        gt=0,
        description=(
            "The baseline Neutron mass envelope to low-inclination LEO, tonnes "
            "(the satellites-per-launch mass bound divides this by "
            "satellite_mass_t). Low-inclination LEO carries more than the DC "
            "SSO 12.5 t case. INTERIM."
        ),
    )
    neutron_fairing_volume_m3: float = Field(
        default=NEUTRON_FAIRING_VOLUME_M3_DEFAULT,
        gt=0,
        description=(
            "The baseline Neutron fairing usable volume, cubic meters (the "
            "volume bound divides this by stowed_volume_m3)."
        ),
    )
    upgraded_neutron_mass_envelope_t: float = Field(
        default=UPGRADED_NEUTRON_MASS_ENVELOPE_T_DEFAULT,
        gt=0,
        description=(
            "The upgraded-Neutron mass envelope (bigger fairing, more mass), "
            "tonnes, used when ConstellationDials.upgraded_neutron is True. "
            "INTERIM."
        ),
    )
    upgraded_neutron_fairing_volume_m3: float = Field(
        default=UPGRADED_NEUTRON_FAIRING_VOLUME_M3_DEFAULT,
        gt=0,
        description="The upgraded-Neutron fairing usable volume, cubic meters. INTERIM.",
    )


class CostDownDials(BaseModel):
    """The satellite cost-down (learning-curve) dial, with the form pinned.

    The form is a Wright-style learning curve expressed as a fractional cost
    reduction per DOUBLING of cumulative units built. The form is fixed here so
    it cannot be silently reintroduced as something else later; the FORMULA that
    applies it is registered and computed in Phase 2.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    learning_rate_per_doubling: float = Field(
        default=LEARNING_RATE_PER_DOUBLING_DEFAULT,
        ge=0,
        lt=1,
        description=(
            "Fractional cost reduction per doubling of cumulative units; "
            "0.0 = no learning, 0.2 = a 20-percent reduction per doubling (an "
            "80-percent learning curve). The cost multiplier at cumulative N is "
            "(N / N0) ** log2(1 - learning_rate_per_doubling) against a "
            "reference cumulative N0. Phase 2 registers and computes this."
        ),
    )
    cost_down_reference_units: int = Field(
        default=COST_DOWN_REFERENCE_UNITS_DEFAULT,
        ge=1,
        description=(
            "The reference cumulative-units count N0 at which the four-area "
            "cost equals the un-discounted per-satellite cost (the curve's "
            "anchor point); 1 = the first unit is the un-discounted anchor."
        ),
    )


class SpectrumDials(BaseModel):
    """The spectrum mechanism dials (SPECTRUM_spec.md Section 4).

    These feed the Phase-2 spectrum module (the requirement formula, the
    empirical capacity anchor, the customer chain). The per-user-rate and
    oversubscription BANDS are :class:`BandTriple`s (low/mid/high), not scalars,
    because they are the two inputs that force the customer output to a band (the
    point-estimate disaster gate). The spectral efficiency is carried ONLY as a
    cross-check on the empirical anchor, never to generate capacity.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    leased_bandwidth_mhz: float = Field(
        default=LEASED_BANDWIDTH_MHZ_DEFAULT,
        gt=0,
        description=(
            "The per-beam channel width leased under the FCC SCS framework, MHz "
            "(the capacity layer vs the 2x5 MHz messaging floor); the AST "
            "40-MHz-to-120-Mbps anchor."
        ),
    )
    spectral_efficiency_bps_per_hz: float = Field(
        default=SPECTRAL_EFFICIENCY_BPS_PER_HZ_DEFAULT,
        gt=0,
        description=(
            "The D2C median spectral efficiency, bits per second per Hz. USED "
            "ONLY as a cross-check on the empirical capacity anchor, NEVER to "
            "generate capacity (the Phase-2 spectrum module emits the naive "
            "figure as a labeled cross-check only)."
        ),
    )
    beams_per_sat: int = Field(
        default=BEAMS_PER_SAT_DEFAULT,
        gt=0,
        description="The beams per satellite (AST Block 2 is about 2,500 adjustable beams).",
    )
    target_per_user_rate_mbps: BandTriple = Field(
        default_factory=lambda: _default_per_user_rate_band(),
        description=(
            "The per-user service level the beam is provisioned against (the "
            "sustained shared rate, the biggest open question), as a low/mid/"
            "high triple stored ascending in Mbps. Consumed INVERTED by the "
            "Phase-2 chain (rate.high feeds the customer-LOW member). "
            "INTERIM / NEEDS-FOUNDER."
        ),
    )
    oversubscription_factor: BandTriple = Field(
        default_factory=lambda: _default_oversubscription_band(),
        description=(
            "Registered subscribers run many times the simultaneously active "
            "users (many-to-one packing; direct-to-cell demand is trip-shaped), "
            "as a low/mid/high triple stored ascending, every member >= 1. "
            "Consumed forward by the Phase-2 chain. INTERIM / NEEDS-FOUNDER."
        ),
    )


class PriceReferenceDials(BaseModel):
    """The price / collectability references and the geographic scope context.

    RENAMED from the design's ``DemandDials`` by plan Section 0.0 Amendment A1
    (the config key ``demand`` becomes ``price_reference``). Demand is ASSUMED,
    not modeled: if the delivered price undercuts what ground charges and that
    price is collectable, the customers follow. This block therefore carries
    ONLY price/collectability references and scope-as-context, NOT a demand,
    top-down-market, growth, or capture-share lever. The top-down market
    projection fields and the forward-projection machinery the pre-A1 design
    described are DELETED by A1 and are not built.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    retail_reference_usd_per_month: float = Field(
        default=RETAIL_REFERENCE_USD_PER_MONTH_DEFAULT,
        gt=0,
        description=(
            "FOUNDER-SET CONFIG, not sourced: about $100/month of full cell "
            "service (the founder's own bill, a chosen reference). The retail-"
            "undercut denominator (the price to beat), kept distinct from the "
            "bottom-up ground cost. The corpus carries individual phone ARPU "
            "around $50 and per-account ARPA around $147, so $100 sits between."
        ),
    )
    arpu_usd_per_month: float = Field(
        default=ARPU_USD_PER_MONTH_DEFAULT,
        gt=0,
        description=(
            "The average revenue per user reference used in the revenue-ceiling "
            "reconciliation (the priced cost is checked against the retail "
            "reference AND against ARPU times operator-share). The individual-"
            "phone ARPU the corpus carries."
        ),
    )
    operator_revenue_share: float = Field(
        default=OPERATOR_REVENUE_SHARE_DEFAULT,
        gt=0,
        le=1,
        description=(
            "The fraction of ARPU the space operator collects under an SCS "
            "revenue-share lease (the rest stays with the carrier). Used in the "
            "Phase-4/5 revenue-ceiling reconciliation. INTERIM."
        ),
    )
    scope: ScopeWeights = Field(
        default_factory=lambda: _default_scope_weights(),
        description=(
            "The geographic CONTEXT split of the served base across US / Europe "
            "/ Asia-ex-China (a premium US/EU mix, ex-China). Context only: it "
            "does NOT weight or drive the cost-vs-ground verdict."
        ),
    )


class GroundDials(BaseModel):
    """The bottom-up ground (cellular) cost build, the cost-to-cost denominator.

    Carried by config in Phase 1 and consumed by the Phase-4 ground module. The
    bottom-up cellular delivery cost is the cost-to-cost denominator (the retail
    $100 is the price to beat, set in the price_reference block). The exact line
    set may be refined in Phase 4; a defensible bottom-up cellular line set is
    carried here so the config is complete and the YAML round-trips.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    tower_cost_musd_per_site: float = Field(
        default=GROUND_TOWER_COST_MUSD_PER_SITE_DEFAULT,
        gt=0,
        description="The amortized cellular tower/site build cost, $M per site. INTERIM.",
    )
    sites_per_million_subs: float = Field(
        default=GROUND_SITES_PER_MILLION_SUBS_DEFAULT,
        gt=0,
        description=(
            "The number of cell sites needed per million subscribers in the "
            "served density (sets how many sites the ground alternative must "
            "build to serve the same customers). INTERIM."
        ),
    )
    backhaul_cost_musd_per_site_year: float = Field(
        default=GROUND_BACKHAUL_COST_MUSD_PER_SITE_YEAR_DEFAULT,
        gt=0,
        description="The annual backhaul/transport cost per site, $M. INTERIM.",
    )
    ground_opex_musd_per_site_year: float = Field(
        default=GROUND_OPEX_MUSD_PER_SITE_YEAR_DEFAULT,
        gt=0,
        description="The annual operations and maintenance cost per site, $M. INTERIM.",
    )
    ground_amortization_years: int = Field(
        default=GROUND_AMORTIZATION_YEARS_DEFAULT,
        ge=1,
        le=40,
        description="The years over which the ground site capex is amortized. INTERIM.",
    )
    spectrum_cost_musd: float = Field(
        default=GROUND_SPECTRUM_COST_MUSD_DEFAULT,
        ge=0,
        description=(
            "The ground-side spectrum cost line. Spectrum nets out of the cost "
            "comparison by construction; carried as an explicit zero, not a "
            "cost numerator line."
        ),
    )


class ScenarioLevers(BaseModel):
    """The scenario-identity block (the comms analog of the DC scenario_name)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    scenario_name: str = Field(
        default="Communications default (central case)",
        description="Human-readable scenario label, surfaced in the report and the JSON manifest.",
    )


# ===========================================================================
# 3. The top-level CommsConfig
# ===========================================================================


class CommsConfig(BaseModel):
    """The complete configuration for one communications-model run.

    Construct one (the defaults reproduce the central design-Section-8 case),
    or load one from YAML with :func:`load_config`. Hand it to
    :func:`communications.engine.run_comms_model` (built in a later phase).

    Each block defaults via Pydantic's ``default_factory`` so a config
    constructed with no arguments, or a YAML omitting a block, gets a fully
    valid all-default block. The model is Neutron-only and cost-driven: no
    capture-share dial, no heavier-than-Neutron vehicle envelope, no baked-in
    verdict, and no demand lever of any kind (demand is assumed, not modeled).
    """

    model_config = ConfigDict(extra="forbid", frozen=True, validate_assignment=True)

    metadata: MetadataDials = Field(
        default_factory=lambda: _default_comms_metadata(),
        description="Run metadata: base year, horizon, steady-state year.",
    )
    constellation: ConstellationDials = Field(
        default_factory=ConstellationDials,
        description=(
            "The two satellite classes (broadband, direct-to-cell), each with "
            "its four cost areas and packing inputs, plus lifetime, the V4 step, "
            "and the Neutron-envelope options."
        ),
    )
    launch: LaunchDials = Field(
        default_factory=LaunchDials,
        description="Cadence and launch-cost reuse dials plus the Neutron envelopes.",
    )
    cost_down: CostDownDials = Field(
        default_factory=CostDownDials,
        description="The satellite learning-curve dial (reduction per doubling).",
    )
    spectrum: SpectrumDials = Field(
        default_factory=SpectrumDials,
        description="The spectrum mechanism dials (leased MHz, capacity bands, beams).",
    )
    price_reference: PriceReferenceDials = Field(
        default_factory=PriceReferenceDials,
        description=(
            "Price/collectability references (the founder-set retail reference, "
            "ARPU, operator share) and geographic scope context. NOT demand: "
            "demand is assumed, not modeled (Amendment A1)."
        ),
    )
    ground: GroundDials = Field(
        default_factory=GroundDials,
        description="The bottom-up ground (cellular) cost build for the cost-to-cost ratio.",
    )
    scenario_levers: ScenarioLevers = Field(
        default_factory=ScenarioLevers,
        description="Scenario identity and any named levers.",
    )


# ===========================================================================
# 4. Default-builder helpers
# ===========================================================================


def _default_comms_metadata() -> MetadataDials:
    """Build the default :class:`MetadataDials` for the central case.

    A named builder is required because :class:`MetadataDials` has three
    required fields with no Pydantic defaults, so ``default_factory=MetadataDials``
    would fail.
    """
    return MetadataDials(
        base_year=BASE_YEAR_DEFAULT,
        horizon_years=HORIZON_YEARS_DEFAULT,
        steady_state_year=STEADY_STATE_YEAR_DEFAULT,
    )


def _default_broadband_class() -> SatelliteClassDials:
    """Build the default broadband (V3-class, mass-bound) satellite class block."""
    return SatelliteClassDials(
        antenna_cost_musd=BROADBAND_ANTENNA_COST_MUSD_DEFAULT,
        comms_electronics_cost_musd=BROADBAND_COMMS_ELECTRONICS_COST_MUSD_DEFAULT,
        solar_cost_usd_per_kw=BROADBAND_SOLAR_COST_USD_PER_KW_DEFAULT,
        payload_power_kw=BROADBAND_PAYLOAD_POWER_KW_DEFAULT,
        radiator_bus_cost_musd=BROADBAND_RADIATOR_BUS_COST_MUSD_DEFAULT,
        satellite_mass_t=BROADBAND_SATELLITE_MASS_T_DEFAULT,
        stowed_volume_m3=BROADBAND_STOWED_VOLUME_M3_DEFAULT,
        minor_component_pct=MINOR_COMPONENT_PCT_DEFAULT,
    )


def _default_direct_to_cell_class() -> SatelliteClassDials:
    """Build the default direct-to-cell (antenna-stow, volume-bound) class block."""
    return SatelliteClassDials(
        antenna_cost_musd=DIRECT_TO_CELL_ANTENNA_COST_MUSD_DEFAULT,
        comms_electronics_cost_musd=DIRECT_TO_CELL_COMMS_ELECTRONICS_COST_MUSD_DEFAULT,
        solar_cost_usd_per_kw=DIRECT_TO_CELL_SOLAR_COST_USD_PER_KW_DEFAULT,
        payload_power_kw=DIRECT_TO_CELL_PAYLOAD_POWER_KW_DEFAULT,
        radiator_bus_cost_musd=DIRECT_TO_CELL_RADIATOR_BUS_COST_MUSD_DEFAULT,
        satellite_mass_t=DIRECT_TO_CELL_SATELLITE_MASS_T_DEFAULT,
        stowed_volume_m3=DIRECT_TO_CELL_STOWED_VOLUME_M3_DEFAULT,
        minor_component_pct=MINOR_COMPONENT_PCT_DEFAULT,
    )


def _default_per_user_rate_band() -> BandTriple:
    """Build the default per-user-rate band (2.0 / 3.0 / 6.0 Mbps, ascending)."""
    low, mid, high = TARGET_PER_USER_RATE_BAND_DEFAULT
    return BandTriple(low=low, mid=mid, high=high)


def _default_oversubscription_band() -> BandTriple:
    """Build the default oversubscription band (1.0 / 1.5 / 2.0, ascending)."""
    low, mid, high = OVERSUBSCRIPTION_BAND_DEFAULT
    return BandTriple(low=low, mid=mid, high=high)


def _default_scope_weights() -> ScopeWeights:
    """Build the default scope weights (0.5 / 0.3 / 0.2, summing to 1)."""
    us, europe, asia_ex_china = SCOPE_WEIGHTS_DEFAULT
    return ScopeWeights(us=us, europe=europe, asia_ex_china=asia_ex_china)


# ===========================================================================
# 5. YAML loader
# ===========================================================================


def config_from_dict(data: dict[str, Any]) -> CommsConfig:
    """Build a :class:`CommsConfig` from an already-parsed YAML mapping.

    Top-level keys are the block names (``metadata``, ``constellation``,
    ``launch``, ``cost_down``, ``spectrum``, ``price_reference``, ``ground``,
    ``scenario_levers``), all optional. Validation is Pydantic's: an unknown
    key, a wrong type, an out-of-bounds value, or a missing required field
    raises :class:`pydantic.ValidationError` with a precise location.
    """
    if not isinstance(data, dict):
        raise ValueError("config root must be a mapping (a YAML object)")
    return CommsConfig.model_validate(data)


def load_config(path: str | Path) -> CommsConfig:
    """Load and validate a :class:`CommsConfig` from a YAML file.

    Raises :class:`FileNotFoundError` if the path does not exist and
    :class:`ValueError` (a :class:`pydantic.ValidationError` or a YAML parse
    error wrapped with context) on any malformed or invalid content. An empty
    file is treated as all-defaults.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"config file not found: {p}")
    try:
        data = yaml.safe_load(p.read_text())
    except yaml.YAMLError as exc:
        raise ValueError(f"could not parse YAML config {p}: {exc}") from exc
    if data is None:
        # An empty scenario file = all defaults.
        return CommsConfig()
    if not isinstance(data, dict):
        raise ValueError(f"config file {p} must contain a YAML mapping (got {type(data).__name__})")
    return config_from_dict(data)


# Re-export the public config surface so external callers (CLI, tests,
# downstream modules) import from one place.
__all__ = [
    "BandTriple",
    "CommsConfig",
    "ConstellationDials",
    "CostDownDials",
    "GroundDials",
    "LaunchDials",
    "MetadataDials",
    "PriceReferenceDials",
    "SatelliteClassDials",
    "ScenarioLevers",
    "ScopeWeights",
    "SpectrumDials",
    "config_from_dict",
    "load_config",
]
