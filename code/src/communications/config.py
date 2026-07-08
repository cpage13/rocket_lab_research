"""The dial schema and YAML loader for the communications CELLULAR cost model.

This module defines the INPUT contract of the slim, roughly 6-variable
cost-to-serve model for a Rocket Lab Neutron-launched CELLULAR direct-to-cell
(satellite-to-phone) constellation. It mirrors the data-center model's config
shape: a top-level frozen :class:`CommsConfig` (``extra="forbid"``) whose nested
blocks are each their own frozen ``extra="forbid"`` BaseModel, every field with a
named-constant default so a no-argument construct is fully valid, plus the
``comms_config_from_dict`` / ``load_comms_config`` YAML loader pair. Nothing here
computes a cost, a coverage fraction, a subscriber count, or a comparison; it is
the contract the engine (Phase 2), the coverage->subscribers logic (Phase 3), the
ground comparison (Phase 4), and the light output (Phase 5) consume.

The product is CELLULAR (the subscriber unit is a PERSON, a phone subscriber, NOT
a household). It is NOT a market-share, demand, or revenue/DCF model. The blocks:

* ``metadata: CommsMetadataDials`` -- base year, horizon, scenario name.
* ``cadence: CadenceDials`` -- the shared whole-fleet logistic launch ramp
  (the DC shape, REUSED verbatim: ceiling 150, year-5 14, year-10 90, first 1).
  This prices the launch cost at the whole-fleet cadence (variable 2's ramp).
* ``comms_cadence: CommsCadenceDials`` -- the comms slice's SHARE of the fleet
  cadence (variable 2's share); how many launches comms flies.
* ``launch_cost: LaunchCostDials`` -- the cadence-indexed log-linear launch-cost
  curve (the DC shape, REUSED verbatim: 25.0 / 13.5 / 5.0 / 100.0) (variable 6).
* ``satellite: SatelliteDials`` -- the fixed CELLULAR-satellite spec: satellites
  per launch (variable 1), lifetime (variable 4, the cohort cliff), and the flat
  mass-manufactured hardware build cost (variable 5).
* ``coverage: CoverageDials`` -- the fleet-sizing bounds (variable 3): the coverage
  FLOOR the fleet must at least reach, and the saturation CAP it may not exceed.
* ``subscribers: SubscriberDials`` -- the CAPACITY dimension (the engine consumes
  this): the subscriber TARGET (the base to serve, the INPUT), the attached
  subscribers-per-satellite density that divides the target into the capacity fleet
  need, plus an optional direct served-base override.
* ``revenue: RevenueDials`` -- the two REVENUE cases the engine computes on every
  run: the COST-PLUS multiple (revenue = cost x multiple, mirroring the DC R) and the
  PRICES-TODAY ARPU (revenue = served base x monthly ARPU x 12). Both yield revenue +
  gross margin per cohort and per year.
* ``ground: GroundInterfaceDials | None`` -- the marked, TWO-REGIME ground
  INTERFACE (Phase 4), default ``None`` so the cost side never blocks on a ground
  number. The dense + sparse baselines are individually None-able caller inputs.
* ``iridium: IridiumDials | None`` -- the optional Iridium model (formerly Model B;
  L-band max-outcome) MSS dials, default ``None`` so the config stays the
  High-Bandwidth Cellular Pure Play model (formerly Model A). Present, it selects
  the Iridium derivation (the per-satellite density is derived from L-band physics
  instead of read from the High-Bandwidth Cellular Pure Play model's fixed dial).

This model imports only from ``common.*`` and ``communications.*`` (never
``data_center``, per the cross-import guard) and uses none of the forbidden
demand-side tokens. YAML loading: scenario files are YAML mappings whose top-level
keys are the block names above, all optional (omitted = defaults). ``extra="forbid"``
means a typo in a scenario file fails loudly.
"""

from __future__ import annotations

import logging
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field

from communications.constants import (
    ACTIVE_USER_RATE_MBPS_DEFAULT,
    APERTURE_REFERENCE_M2,
    ARPU_USD_PER_MONTH_DEFAULT,
    BASE_YEAR_DEFAULT,
    CADENCE_CEILING_DEFAULT,
    COMMS_SHARE_DEFAULT,
    CONCURRENCY_OFFPEAK_DEFAULT,
    CONCURRENCY_PEAK_DEFAULT,
    FIRST_LAUNCH_YEAR_DEFAULT,
    GROUND_BASIS_DEFAULT,
    HIGH_CADENCE_COST_MUSD_DEFAULT,
    HIGH_CADENCE_LAUNCHES_DEFAULT,
    HORIZON_YEARS_DEFAULT,
    IOT_DEVICES_DEFAULT,
    IRIDIUM_SCENARIO_NAME_DEFAULT,
    LAUNCHES_AT_YEAR_5_DEFAULT,
    LAUNCHES_AT_YEAR_10_DEFAULT,
    LOW_CADENCE_COST_MUSD_DEFAULT,
    LOW_CADENCE_LAUNCHES_DEFAULT,
    MAX_FLEET_SATELLITES_DEFAULT,
    MAX_FY,
    MAX_HORIZON_YEARS,
    MIN_FY,
    MIN_HORIZON_YEARS,
    REVENUE_MULTIPLE_DEFAULT,
    SATELLITE_BUILD_COST_MUSD_DEFAULT,
    SATELLITE_LIFETIME_YEARS_DEFAULT,
    SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
    SATELLITES_PER_LAUNCH_DEFAULT,
    SPECTRUM_MHZ_DEFAULT,
    SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT,
    SUBSCRIBERS_PER_SATELLITE_DEFAULT,
    DeviceClass,
)

logger = logging.getLogger(__name__)

# ===========================================================================
# 1. Dial blocks (each its own frozen, extra-forbid BaseModel)
# ===========================================================================


class CommsMetadataDials(BaseModel):
    """Run metadata: base year, analysis horizon, and the scenario label.

    Mirrors the DC ``MetadataConfig`` base-year / horizon pattern (both REQUIRED,
    no field default; the all-defaults construct supplies them via the
    :func:`_default_comms_metadata` factory). The DC-specific enums (workload,
    operator, radiator architecture) are DROPPED: the satellite is a fixed spec
    with no workload/operator/radiator taxonomy.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    base_year: int = Field(
        ge=MIN_FY,
        le=MAX_FY,
        description="Calendar year corresponding to model year 0 (Neutron first-flight year).",
    )
    horizon_years: int = Field(
        ge=MIN_HORIZON_YEARS,
        le=MAX_HORIZON_YEARS,
        description="Number of fiscal-year steps after year 0 (base_year + horizon = final year).",
    )
    scenario_name: str = Field(
        default="Comms cellular direct-to-cell (central case)",
        description="Human-readable scenario label, surfaced in the output metadata.",
    )


class CadenceDials(BaseModel):
    """Whole-fleet launch-cadence dials feeding the shared logistic ramp.

    REUSED VERBATIM from the DC ``CadenceDials`` shape (same field names, same
    bounds, same named-constant defaults sourced from the shared
    ``common.cadence`` spine). This is the WHOLE-FLEET Neutron cadence (the 90/year
    FY2036 ramp) that prices the launch cost; the comms slice flies a SHARE of it
    (see :class:`CommsCadenceDials`). Consumed by
    ``common.cadence.compute_launches_per_year``.
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
        description="Integer logistic anchor: launches per year at model year 10.",
    )
    first_launch_year: int = Field(
        default=FIRST_LAUNCH_YEAR_DEFAULT,
        ge=0,
        description="Model-year index before which launch count is clamped to zero.",
    )


class CommsCadenceDials(BaseModel):
    """The comms slice's SHARE of the whole-fleet cadence (variable 2's share).

    The whole-fleet cadence (:class:`CadenceDials`) ramps to 90 launches/year by
    FY2036; the comms constellation flies a SHARE of those launches. Phase 2
    multiplies the shared per-year integer launch count by ``share_of_fleet`` and
    re-rounds to an integer (with the shared half-up offset) to get the comms
    launches flown per year. The launch COST is still priced at the whole-fleet
    cadence (the cost-down is a Neutron-production-scale effect, shared), not at
    the comms slice's own cadence.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    share_of_fleet: float = Field(
        default=COMMS_SHARE_DEFAULT,
        gt=0,
        le=1.0,
        description=(
            "Comms fraction of the whole-fleet per-year launch count. FOUNDER_SET "
            "to 0.18 (~16 of the 90 FY2036 launches/year); the founder's ~15 to 20 "
            "band maps to ~0.167 to ~0.222. Configurable."
        ),
    )


class LaunchCostDials(BaseModel):
    """Cadence-indexed launch-cost dials feeding the log-linear cost curve.

    REUSED VERBATIM from the DC ``LaunchCostDials`` shape (same field names, same
    bounds, same named-constant defaults from the shared ``common.cadence`` spine).
    The cost is priced at the WHOLE-FLEET cadence. Consumed by
    ``common.cadence.compute_launch_cost_musd``.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    low_cadence_cost_musd: float = Field(
        default=LOW_CADENCE_COST_MUSD_DEFAULT,
        gt=0,
        description="Launch cost at the low-cadence anchor, $M.",
    )
    high_cadence_cost_musd: float = Field(
        default=HIGH_CADENCE_COST_MUSD_DEFAULT,
        gt=0,
        description="Launch cost at the high-cadence anchor, $M.",
    )
    low_cadence_launches: float = Field(
        default=LOW_CADENCE_LAUNCHES_DEFAULT,
        gt=0,
        description="Cadence (launches/yr) at the low-cost anchor.",
    )
    high_cadence_launches: float = Field(
        default=HIGH_CADENCE_LAUNCHES_DEFAULT,
        gt=0,
        description="Cadence (launches/yr) at the high-cost anchor.",
    )


class SatelliteDials(BaseModel):
    """The fixed CELLULAR direct-to-cell satellite spec (variables 1, 4, 5).

    The satellite is a flat mass-manufactured satellite-to-phone bird (a fixed
    spec, NOT a re-spec'd frontier generation, so the DC ``generations`` /
    ``slopes`` engine is dropped). Three dials: satellites per launch (a direct
    input), the operating life (the cohort cliff), and the one flat hardware
    build-cost scalar.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    satellites_per_launch: int = Field(
        default=SATELLITES_PER_LAUNCH_DEFAULT,
        ge=1,
        le=16,
        description=(
            "Satellites per Neutron launch, a DIRECT input scalar (12 default, up "
            "to 16). Mass-bound count for a Flatellite-class bird: ~12 (SSO), ~16 "
            "(LEO). Source COMM-258 / COMM-260."
        ),
    )
    satellite_lifetime_years: int = Field(
        default=SATELLITE_LIFETIME_YEARS_DEFAULT,
        ge=1,
        le=20,
        description=(
            "Satellite operating life in years, the cohort cliff: after this a "
            "cohort retires and contributes zero coverage. ~5-year Starlink "
            "replacement anchor (COMM-091), a design assumption not a certified "
            "field life."
        ),
    )
    satellite_build_cost_musd: float = Field(
        default=SATELLITE_BUILD_COST_MUSD_DEFAULT,
        gt=0,
        description=(
            "The flat MASS-MANUFACTURED CELLULAR-SATELLITE HARDWARE cost, ONE "
            "scalar, ~$1.0 to 1.1M (FOUNDER_SET 1.05). A V3-class hardware analogy "
            "(Starlink V3 ~$1.2M, the upper anchor, COMM-080) for a direct-to-cell "
            "payload (bigger antenna and more power than a broadband panel, far "
            "smaller than AST's giant array, so AST ~$19 to 21M is the WRONG "
            "anchor). A hardware build-cost analogy, NOT a broadband-product claim. "
            "Configurable."
        ),
    )


class CoverageDials(BaseModel):
    """The fleet-sizing bounds: the coverage FLOOR and the saturation CAP (variable 3).

    The fleet target the build-out fills toward is the CAPACITY need (the subscriber
    target divided by the per-satellite density, see :class:`SubscriberDials`),
    FLOORED by ``satellites_for_full_coverage`` (everyone must be able to see a
    satellite) and CAPPED by ``max_fleet_satellites`` (past which the spread servable
    base is exhausted). At a small base the floor binds (the engine reports the
    coverage regime); at a large base the capacity need binds; at an enormous base
    the cap binds. The ELEVATION MASK is the underlying physical dial behind the floor
    (this default is the 25-degree quality-link, populated-band, 95%-coverage figure).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    satellites_for_full_coverage: int = Field(
        default=SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
        ge=1,
        description=(
            "The coverage FLOOR: the minimum fleet for everyone in the served band "
            "to SEE a satellite (the lower bound on the fleet target, NOT the whole "
            "fleet when the base is large). FOUNDER_SET to 340: the quality-link case "
            "(25 degree elevation mask, populated mid-latitude band +/-55 deg at 95%, "
            "~450 km, ~53 deg). Coverage sim (.agent/other/coverage_sim/FINDINGS.md: "
            "341, rounded to 340) plus COMM-209 / COMM-216 / COMM-217 and "
            "COMM-386..COMM-405. Configurable."
        ),
    )
    max_fleet_satellites: int = Field(
        default=MAX_FLEET_SATELLITES_DEFAULT,
        ge=1,
        description=(
            "The saturation CAP: the largest fleet the model sizes to (the upper "
            "bound on the fleet target). Past this the spread, low-density servable "
            "base is exhausted and more satellites stop buying servable subscribers "
            "(a dense cell saturates). FOUNDER_SET to 2,000: the ~100M ambitious "
            "target (1,334 satellites at 75,000/sat) sits just under it. Source "
            "COMM-535..560. Configurable."
        ),
    )


class SubscriberDials(BaseModel):
    """The CAPACITY dimension: the subscriber TARGET and the per-satellite density.

    The unit is a PERSON (a phone subscriber), NOT a household (cellular is
    per-person). The subscriber TARGET (``subscribers_at_full_coverage``) is the
    INPUT, the base to SERVE; the engine sizes the fleet to serve it at
    ``subscribers_per_satellite`` attached subscribers per satellite (the capacity
    need), then floors by the coverage floor and caps by the saturation cap. The
    served count then RAMPS with the buildout (target x living-fleet / fleet-target),
    reaching the target at full deployment. This is capacity-SIZED (the fleet tracks
    the base), NOT capacity-DERIVED in the old sense (no spectrum -> capacity ->
    demand chain; the served base is a sized input, not a demand estimate). None of
    the field names use a forbidden demand-side token.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    subscribers_at_full_coverage: int = Field(
        default=SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT,
        ge=1,
        description=(
            "The SUBSCRIBER TARGET: the served-PERSON base (phone subscribers) the "
            "fleet is sized to serve, the model's INPUT, NOT a demand estimate, NOT a "
            "household count. FOUNDER_SET to a 10,000,000-person BASELINE (50,000,000 "
            "and 100,000,000 are the scenarios) and flagged as the SWING DIAL that "
            "most moves cost-per-subscriber. Niche basis: the ~300M global "
            "coverage-gap people (COMM-021 / COMM-390) plus the developed-world "
            "remote/unserved layer (household tiers, e.g. COMM-065, converted at ~2.5 "
            "people/household). The base grows over time. Configurable. (The field "
            "name is retained for config-schema stability; it now means the target.)"
        ),
    )
    subscribers_per_satellite: int = Field(
        default=SUBSCRIBERS_PER_SATELLITE_DEFAULT,
        ge=1,
        description=(
            "ATTACHED subscribers per cellular satellite: the central of the grounded "
            "~50,000 to 100,000 range (75,000 default). Divides the subscriber target "
            "into the CAPACITY fleet need (ceil(target / this)). ~50x a Starlink "
            "BROADBAND satellite because a cellular subscriber sips data. On 25 MHz "
            "the spectrum binds first, the antenna power past ~50 to 100 MHz, the "
            "onboard chip last. Source COMM-535..560. Configurable."
        ),
    )
    subscribers_served_override: int | None = Field(
        default=None,
        ge=1,
        description=(
            "OPTIONAL direct served-base scalar. If set, it overrides the subscriber "
            "TARGET as the base the served count ramps toward (the model serves this "
            "absolute count at full deployment; below full deployment it still scales "
            "by the buildout fraction). The fleet target is still sized from the "
            "TARGET dial, not this override. Default None means use the target."
        ),
    )


class RevenueDials(BaseModel):
    """The two REVENUE cases that ride the cohort treadmill (revenue + gross margin).

    The engine computes BOTH cases on every run (they are not mutually exclusive
    dials; each is a separate lens on the same fleet), mirroring the data-center
    model's revenue/margin pattern but adapted to the comms model's lighter
    single-value (no R-band) style:

    * COST-PLUS / MARGIN-TARGET (``revenue_multiple``): annual revenue = annual cost
      x the multiple, the same owner-operator basis as the DC central R (1.5 -> 33.3%
      gross margin). A cost-coupled case (revenue tracks the cost basis).
    * PRICES-TODAY / ARPU (``arpu_usd_per_month``): annual revenue = served
      subscribers x the monthly ARPU x 12, a retail price applied to the served base.

    Gross margin in BOTH cases is ``(revenue - cost) / revenue`` against the same
    annualized cost basis the engine carries per cohort (the per-satellite lifetime
    cost spread over the satellite life, matching the DC annualized convention). The
    revenue is a cost-coupled multiple or a price-times-served-base figure, NEVER a
    demand, market-size, or willingness-to-pay estimate (no forbidden demand-side
    token appears on this block).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    revenue_multiple: float = Field(
        default=REVENUE_MULTIPLE_DEFAULT,
        gt=0,
        description=(
            "The COST-PLUS / MARGIN-TARGET revenue multiple: annual revenue = annual "
            "cost x this. FOUNDER_SET to 1.5 (cost+50%, an implied (1.5 - 1) / 1.5 = "
            "33.3% gross margin), mirroring the data-center central R = 1.5 "
            "(research/SOURCE_INDEX.md#REV-008). Each 5-year cohort earns this margin "
            "across its life. Configurable."
        ),
    )
    arpu_usd_per_month: float = Field(
        default=ARPU_USD_PER_MONTH_DEFAULT,
        gt=0,
        description=(
            "The PRICES-TODAY / ARPU monthly revenue per subscriber: annual revenue = "
            "served subscribers x this x 12 months. Default $50/month, a supportable "
            "median that sits BELOW the ~$80 to 100/month terrestrial mobile plan "
            "(documented in the assumptions), the headroom assuming direct-to-cell "
            "prices drop toward and below today's terrestrial floor as the service "
            "scales. A retail price on the SERVED base, NOT a demand estimate. "
            "Configurable."
        ),
    )


class GroundInterfaceDials(BaseModel):
    """The marked, TWO-REGIME CELLULAR-ground cost INTERFACE (Phase 4).

    INTERFACE INPUTS. These two ground baselines (dense-served incumbent-marginal
    and sparse fresh-build) come from the ground research wave; the founder owns the
    final ground call and is still unsure about the comparison. Do not hardcode
    settled values in the comms src; supply them per-scenario. Either or both may be
    None, in which case that regime's ratio is skipped and the model still reports
    the space cost per subscriber.

    The space side of the comparison is the model's OWN COMPUTED cellular annual
    cost-per-subscriber (Phase 3), NEVER Starlink's disclosed broadband per-sub
    number. This block is declared in Phase 1 (the ``ground`` field defaults to
    None on :class:`CommsConfig`); Phase 4 consumes it in ``ground.py``.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    dense_ground_cost_per_subscriber_usd: float | None = Field(
        default=None,
        gt=0,
        description=(
            "Dense-served incumbent-marginal CELLULAR ground cost per subscriber "
            "(the mobile-network all-in cost per human subscriber), grounded ~$140 "
            "to 310/sub/yr. MARKED INTERFACE INPUT; optional (None-able) so the cost "
            "side never blocks. Sources COMM-096 / COMM-098 and "
            "research/economics/ground_cellular_cost_per_subscriber.md Section 2.4."
        ),
    )
    sparse_ground_cost_per_subscriber_usd: float | None = Field(
        default=None,
        gt=0,
        description=(
            "Sparse fresh-build ground cost per subscriber, grounded ~$875 to "
            "1,540/sub/yr rural (up to the ~$44,500 extreme tail). MARKED INTERFACE "
            "INPUT; optional. This is the regime the HEADLINE verdict reads: space "
            "below this number is the niche. Source COMM-100."
        ),
    )
    basis: str = Field(
        default=GROUND_BASIS_DEFAULT,
        description=(
            "Label stating which basis the ground numbers are on (default "
            "'annual_cost_per_subscriber'), so the Phase 4 comparison matches "
            "like-for-like with the space side (it asserts the bases match)."
        ),
    )
    scenario_name: str = Field(
        default="ground interface (research-grounded, founder owns the call)",
        description="Human-readable label for the supplied ground-interface scenario.",
    )
    source_note: str = Field(
        default="",
        description="Free-text record of the research provenance once firm (empty by default).",
    )


class IridiumDials(BaseModel):
    """The Iridium model's (L-band max-outcome) input dials: the MSS lane.

    Present (non-None on :class:`CommsConfig`) selects the Iridium derivation: the
    engine DERIVES the per-satellite subscriber density from L-band physics (held
    spectrum, device spectral efficiency, active rate, busy-hour concurrency) instead
    of reading the High-Bandwidth Cellular Pure Play model's fixed
    ``subscribers_per_satellite`` dial, then feeds the SAME ``compute_fleet_target``.
    The subscriber TARGET is the existing ``subscribers.subscribers_at_full_coverage``
    dial (not duplicated here). Subscribers are PEOPLE; ``iot_devices`` is a separate
    DEVICE passthrough. ``spectrum_mhz`` is a WIDTH held (not a frequency). See the
    ecosystem assumption: this is the MSS lane (purpose-built or in-chipset devices on
    owned L-band), never an unmodified phone (that is the cellular lane, the
    High-Bandwidth Cellular Pure Play model).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    spectrum_mhz: float = Field(
        default=SPECTRUM_MHZ_DEFAULT,
        gt=0,
        description=(
            "The L-band WIDTH held in MHz (a width, NOT a frequency; the frequency is "
            "the ~1.6 GHz dial position). FOUNDER_SET to 8.0, the Iridium exclusive "
            "holding (~7.775 rounded); 10.5 is the coordinated-span variant. Flagged. "
            "Configurable."
        ),
    )
    aperture_m2: float = Field(
        default=APERTURE_REFERENCE_M2,
        gt=0,
        description=(
            "The satellite flat phased-array AREA in m^2. Default 25.0, which by design "
            "IS the calibration reference (APERTURE_REFERENCE_M2) AND the no-fold stow "
            "limit (APERTURE_NO_FOLD_LIMIT_M2). Capacity scales linearly with it "
            "(conservative: it ignores the per-link SNR lift a larger aperture also "
            "gives); satellites-per-launch couples inversely (fewer, bigger satellites "
            "per launch). Above APERTURE_NO_FOLD_LIMIT_M2 the assumptions output carries "
            "the fold caveat, deliberately NOT a bound so the what-if stays computable. "
            "FOUNDER-DIRECTED. Configurable."
        ),
    )
    device_class: DeviceClass = Field(
        default=DeviceClass.PHONE_CLASS,
        description=(
            "The device class that sets the spectral-efficiency tier: PHONE_CLASS "
            "(0 dBi in-chipset, the ecosystem-assumption baseline, SE ~0.65), "
            "SMALL_TERMINAL_CLASS (paperback/puck ~10 dBi purpose-built, SE ~2.0), or "
            "TERMINAL_CLASS (large boosted / custom antenna, 15+ dBi, SE ~2.5). Default "
            "PHONE_CLASS; one class per run in v1 (no mixed fleet). Flagged. "
            "Configurable."
        ),
    )
    spectral_efficiency_bps_per_hz: float | None = Field(
        default=None,
        gt=0,
        description=(
            "OPTIONAL spectral-efficiency override in bps/Hz. None (default) resolves to "
            "the device_class central tier; set it to sweep within the class band "
            "(phone 0.5 to 0.8, small terminal 1.5 to 2.5, large terminal 2.0 to 3.0). "
            "Configurable."
        ),
    )
    active_user_rate_mbps: float = Field(
        default=ACTIVE_USER_RATE_MBPS_DEFAULT,
        gt=0,
        description=(
            "The per-subscriber active data rate in Mbps (the service tier; also the "
            "peak per-user rate by construction). FOUNDER_SET to 1.0 (standard "
            "smartphone activity); 2.5 is the rich variant. Flagged. Configurable."
        ),
    )
    concurrency_peak: float = Field(
        default=CONCURRENCY_PEAK_DEFAULT,
        gt=0,
        le=1.0,
        description=(
            "The busy-hour PEAK concurrency fraction (share of subscribers "
            "simultaneously active at peak). FOUNDER_SET to 0.025 (2.5%). Flagged as "
            "the pair with concurrency_offpeak. Configurable."
        ),
    )
    concurrency_offpeak: float = Field(
        default=CONCURRENCY_OFFPEAK_DEFAULT,
        gt=0,
        le=1.0,
        description=(
            "The OFF-PEAK concurrency fraction. FOUNDER_SET to 0.005 (0.5%). Flagged as "
            "the pair with concurrency_peak. Configurable."
        ),
    )
    iot_devices: int = Field(
        default=IOT_DEVICES_DEFAULT,
        ge=0,
        description=(
            "A separate DEVICE passthrough counter (NOT people, NOT folded into the "
            "subscriber count): IoT is negligible-load and does NOT affect fleet "
            "sizing. ESTIMATE 10,000,000 (low end of tens of millions); founder-owned. "
            "Configurable."
        ),
    )
    scenario_name: str = Field(
        default=IRIDIUM_SCENARIO_NAME_DEFAULT,
        description=(
            "The Iridium-model scenario label's SINGLE home (mirroring the "
            "GroundInterfaceDials.scenario_name precedent: an optional block carries "
            "its own label). The Iridium scenario YAML sets no metadata block, so the "
            "Iridium-model label lives here. Configurable."
        ),
    )


# ===========================================================================
# 2. The top-level CommsConfig
# ===========================================================================


class CommsConfig(BaseModel):
    """The complete configuration for one communications cellular cost run.

    Construct one (the defaults reproduce the central case), or load one from YAML
    with :func:`load_comms_config`. Hand it to ``run_comms_model`` (Phase 2) /
    ``build_comms_output`` (Phase 5).

    Every block defaults via ``default_factory`` (or, for ``ground`` and ``iridium``,
    a plain None) so a config constructed with no arguments, or a YAML omitting a
    block, gets a fully valid all-default block. The ``ground`` field is ``None`` by
    default, which is what makes the cost side run with no ground number; the
    ``iridium`` field is ``None`` by default, which selects the High-Bandwidth
    Cellular Pure Play path (a non-None ``iridium`` selects the Iridium MSS
    derivation).
    """

    model_config = ConfigDict(extra="forbid", frozen=True, validate_assignment=True)

    metadata: CommsMetadataDials = Field(
        default_factory=lambda: _default_comms_metadata(),
        description="Run metadata: base year, horizon, scenario name.",
    )
    cadence: CadenceDials = Field(
        default_factory=CadenceDials,
        description="Whole-fleet launch-cadence dials (shared logistic ramp; prices launch cost).",
    )
    comms_cadence: CommsCadenceDials = Field(
        default_factory=CommsCadenceDials,
        description="The comms slice's share of the fleet cadence (how many launches comms flies).",
    )
    launch_cost: LaunchCostDials = Field(
        default_factory=LaunchCostDials,
        description="Cadence-indexed launch-cost dials (log-linear, priced at fleet cadence).",
    )
    satellite: SatelliteDials = Field(
        default_factory=SatelliteDials,
        description="The fixed cellular-satellite spec: per-launch count, lifetime, build cost.",
    )
    coverage: CoverageDials = Field(
        default_factory=CoverageDials,
        description="The fleet-sizing bounds: the coverage floor and the saturation cap.",
    )
    subscribers: SubscriberDials = Field(
        default_factory=SubscriberDials,
        description="The capacity dimension: subscriber target, per-satellite density, override.",
    )
    revenue: RevenueDials = Field(
        default_factory=RevenueDials,
        description="The two revenue cases: the cost-plus multiple and the prices-today ARPU.",
    )
    ground: GroundInterfaceDials | None = Field(
        default=None,
        description=(
            "The marked, TWO-REGIME ground interface (Phase 4). None by default so "
            "the cost side runs with no ground number; supply it per-scenario."
        ),
    )
    iridium: IridiumDials | None = Field(
        default=None,
        description=(
            "The Iridium model's (L-band max-outcome) dials. None by default so the "
            "config is the High-Bandwidth Cellular Pure Play model (cellular "
            "direct-to-cell); set it to select the Iridium MSS derivation."
        ),
    )


# ===========================================================================
# 3. Default-builder helpers
# ===========================================================================


def _default_comms_metadata() -> CommsMetadataDials:
    """Build the default :class:`CommsMetadataDials` for the central case.

    A named builder is required because :class:`CommsMetadataDials` has two
    required fields (``base_year``, ``horizon_years``) with no field defaults, so
    ``default_factory=CommsMetadataDials`` would fail. Mirrors the DC
    ``_default_metadata`` pattern; supplies base year 2026 and horizon 10.
    """
    return CommsMetadataDials(base_year=BASE_YEAR_DEFAULT, horizon_years=HORIZON_YEARS_DEFAULT)


# ===========================================================================
# 4. YAML loaders
# ===========================================================================


def comms_config_from_dict(data: dict[str, object]) -> CommsConfig:
    """Build a :class:`CommsConfig` from an already-parsed YAML mapping.

    Top-level keys are the block names (``metadata``, ``cadence``,
    ``comms_cadence``, ``launch_cost``, ``satellite``, ``coverage``,
    ``subscribers``, ``revenue``, ``ground``), all optional (omitted = defaults). An
    empty dict yields an all-defaults config.

    Validation is Pydantic's: an unknown key, a wrong type, an out-of-bounds value,
    or a missing required field raises :class:`pydantic.ValidationError` with a
    precise location.
    """
    if not isinstance(data, dict):
        raise ValueError("config root must be a mapping (a YAML object)")
    return CommsConfig.model_validate(data)


def load_comms_config(path: str | Path) -> CommsConfig:
    """Load and validate a :class:`CommsConfig` from a YAML file.

    Raises :class:`FileNotFoundError` if the path does not exist and
    :class:`ValueError` (a :class:`pydantic.ValidationError` for schema problems)
    on any malformed or invalid content. An empty file yields an all-defaults
    :class:`CommsConfig`.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"comms config file not found: {p}")
    try:
        data = yaml.safe_load(p.read_text())
    except yaml.YAMLError as exc:
        raise ValueError(f"could not parse YAML comms config {p}: {exc}") from exc
    if data is None:
        # An empty scenario file = all defaults.
        return CommsConfig()
    if not isinstance(data, dict):
        raise ValueError(
            f"comms config file {p} must contain a YAML mapping (got {type(data).__name__})"
        )
    return comms_config_from_dict(data)


# Re-export the public config surface so external callers (engine, ground, output,
# tests) import from one place.
__all__ = [
    "CadenceDials",
    "CommsCadenceDials",
    "CommsConfig",
    "CommsMetadataDials",
    "CoverageDials",
    "GroundInterfaceDials",
    "IridiumDials",
    "LaunchCostDials",
    "RevenueDials",
    "SatelliteDials",
    "SubscriberDials",
    "comms_config_from_dict",
    "load_comms_config",
]
