"""The dial schema and YAML loader for the communications model families.

This module defines the INPUT contract of the slim cost-to-serve model for a
Rocket Lab Neutron-launched communications constellation, shared by both model
families: the High-Bandwidth Cellular Pure Play model (the no-``iridium`` default,
cellular direct-to-cell on partner cellular spectrum) and the Iridium model (the
MSS lane on Iridium's owned L-band, selected by the ``iridium`` block). It mirrors
the data-center model's config shape: a top-level frozen :class:`CommsConfig`
(``extra="forbid"``) whose nested blocks are each their own frozen
``extra="forbid"`` BaseModel, every field with a named-constant default so a
no-argument construct is fully valid, plus the ``comms_config_from_dict`` /
``load_comms_config`` YAML loader pair. Every block this module defines refuses a
number that is not finite (``allow_inf_nan=False``), and so do the cadence and launch-cost
blocks, ``common.cadence``'s, shared with the data-center model (the launch cost's by the
same setting, the cadence's dials being whole numbers), each at load, naming the field. The
numeric fields of the Iridium blocks (the held spectrum, the panel, the downlink share and the
five prices), of the comms share and satellite blocks, and of the shared cadence and
launch-cost blocks are also strict: a boolean (a YAML ``true``, ``yes`` or ``on``) is refused
at load, naming the field, never read as 1, and so is a quoted number; an integer loads as a
float field's float, and a whole-number float (16.0) as an integer field's integer, as before
(a launch count, satellites per launch and the life are :data:`common.cadence.WholeNumber`).
Nothing here computes a cost, a coverage
fraction, a subscriber count, or a comparison; it is the contract the engine
(``communications.engine``), the Iridium family (``communications.iridium``), the
ground comparison (``communications.ground``), and the Iridium artifact writer
(``communications.json_output``) consume. Cross-field rules are model validators: the
coverage floor may not exceed the cellular fleet cap; on an Iridium config every field of
the ``coverage``, ``subscribers`` and ``revenue`` blocks keeps its default and ``ground``
stays unset (the Iridium path reads none of the cellular family's sizing and revenue dials,
and pins the coverage floor at 340); and (the shared dial blocks' own validators) the
cadence anchors must satisfy
``0 < launches_at_year_5 < launches_at_year_10 < cadence_ceiling`` and the
launch-cost anchors ``low_cadence_launches < high_cadence_launches``.

The subscriber unit is a PERSON, NOT a household, and IoT devices are never summed
with people. It is NOT a market-share, demand, or DCF model: revenue is a
cost-coupled multiple or a price applied to a sized base. The blocks:

* ``metadata: CommsMetadataDials`` -- base year, horizon, scenario name.
* ``cadence: CadenceDials`` -- the shared whole-fleet logistic launch ramp
  (:class:`common.cadence.CadenceDials`, the data-center block itself: ceiling
  150, year-5 14, year-10 90, first 1, with its load-time anchor validator).
  This prices the launch cost at the whole-fleet cadence (variable 2's ramp).
* ``comms_cadence: CommsCadenceDials`` -- the comms slice's SHARE of the fleet
  cadence (variable 2's share); how many launches comms flies.
* ``launch_cost: LaunchCostDials`` -- the cadence-indexed log-linear launch-cost
  curve (:class:`common.cadence.LaunchCostDials`, the data-center block itself:
  25.0 / 13.5 / 5.0 / 100.0, with its anchor-order validator) (variable 6).
* ``satellite: SatelliteDials`` -- the satellite spec both families read: satellites
  per launch (variable 1), lifetime (variable 4, the cohort cliff), and the flat
  mass-manufactured hardware build cost (variable 5).
* ``coverage: CoverageDials`` -- the cellular family's fleet-sizing bounds (variable 3):
  the coverage FLOOR the fleet must at least reach, and the fleet CAP it may not exceed.
  The Iridium path pins the floor at its default and has no cap.
* ``subscribers: SubscriberDials`` -- the cellular family's CAPACITY dimension: the
  subscriber TARGET (the base to serve, the INPUT), the attached
  subscribers-per-satellite density that divides the target into the capacity fleet
  need, plus an optional direct served-base override.
* ``revenue: RevenueDials`` -- the cellular family's two REVENUE cases: the COST-PLUS
  multiple (revenue = cost x multiple, mirroring the DC R) and the PRICES-TODAY ARPU
  (revenue = served base x monthly ARPU x 12), each with its margin per cohort and per
  year.
* ``ground: GroundInterfaceDials | None`` -- the marked, TWO-REGIME ground
  INTERFACE (Phase 4), default ``None`` so the cost side never blocks on a ground
  number. The dense + sparse baselines are individually None-able caller inputs. No
  Iridium run reads it, so an Iridium config refuses one.
* ``iridium: IridiumDials | None`` -- the optional Iridium model (formerly Model B;
  L-band max-outcome) MSS dials, default ``None`` so the config stays the
  High-Bandwidth Cellular Pure Play model (formerly Model A). Present, it selects the
  Iridium model, which reads every device class's people from the promoted saturation
  curve: the held spectrum, the panel, the label, the ``saturation`` block
  (:class:`SaturationDials`: the downlink time share and the curve's path) and the
  ``arpu`` block (:class:`IridiumArpuDials`: the five monthly prices). Each class's usage,
  its spectral efficiency and the two IoT lines' counts are named constants
  (:mod:`communications.constants`), not settings.

This model imports only from ``common.*`` and ``communications.*`` (never
``data_center``, per the cross-import guard) and uses none of the forbidden
demand-side tokens. YAML loading: scenario files are YAML mappings whose top-level
keys are the block names above, all optional (omitted = defaults), read through the
shared :func:`common.file_io.load_yaml_mapping`. ``extra="forbid"`` means a typo in a
scenario file fails loudly.
"""

from __future__ import annotations

import logging
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator

from common.cadence import CadenceDials, LaunchCostDials, WholeNumber
from common.file_io import load_yaml_mapping
from communications.constants import (
    APERTURE_M2_DEFAULT,
    APERTURE_REFERENCE_M2,
    APERTURE_VALIDATED_STACK_LIMIT_M2,
    ARPU_PRICE_CEILING_USD_MONTH,
    ARPU_USD_PER_MONTH_DEFAULT,
    BASE_YEAR_DEFAULT,
    COMMS_SHARE_DEFAULT,
    DATA_IOT_PRICE_USD_MONTH_DEFAULT,
    DOWNLINK_SHARE_DEFAULT,
    GROUND_BASIS_DEFAULT,
    HORIZON_YEARS_DEFAULT,
    IRIDIUM_SCENARIO_NAME_DEFAULT,
    MAX_FLEET_SATELLITES_DEFAULT,
    MAX_FY,
    MAX_HORIZON_YEARS,
    MIN_FY,
    MIN_HORIZON_YEARS,
    MINIMAL_PACKET_IOT_PRICE_USD_MONTH_DEFAULT,
    MOUNTED_TERMINAL_CLASS_PRICE_USD_MONTH_DEFAULT,
    PHONE_CLASS_PRICE_USD_MONTH_DEFAULT,
    REVENUE_MULTIPLE_DEFAULT,
    SATELLITE_BUILD_COST_MUSD_DEFAULT,
    SATELLITE_LIFETIME_YEARS_DEFAULT,
    SATELLITE_LIFETIME_YEARS_MAX,
    SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
    SATELLITES_PER_LAUNCH_DEFAULT,
    SATELLITES_PER_LAUNCH_MAX,
    SATELLITES_PER_LAUNCH_MIN,
    SATURATION_CURVE_PATH_DEFAULT,
    SMALL_TERMINAL_CLASS_PRICE_USD_MONTH_DEFAULT,
    SPECTRUM_MHZ_DEFAULT,
    SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT,
    SUBSCRIBERS_PER_SATELLITE_DEFAULT,
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

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

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


class CommsCadenceDials(BaseModel):
    """The comms slice's SHARE of the whole-fleet cadence.

    The whole-fleet cadence (:class:`CadenceDials`) ramps to 90 launches/year by
    FY2036; the comms constellation flies a SHARE of those launches. The engine
    multiplies the shared per-year integer launch count by ``share_of_fleet`` and
    re-rounds to an integer (with the shared half-up offset) to get the comms
    launches flown per year. The launch COST is still priced at the whole-fleet
    cadence (the cost-down is a Neutron-production-scale effect, shared), not at
    the comms slice's own cadence. The share is strict: a YAML boolean or a quoted
    number is refused at load, naming the field, and an integer loads as its float.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    share_of_fleet: float = Field(
        default=COMMS_SHARE_DEFAULT,
        gt=0,
        le=1.0,
        strict=True,
        description=(
            "Comms fraction of the whole-fleet per-year launch count. INVESTOR_SET "
            "to 0.18 (~16 of the 90 FY2036 launches/year); the investor's ~15 to 20 "
            "band maps to ~0.167 to ~0.222. Configurable."
        ),
    )


class SatelliteDials(BaseModel):
    """The satellite spec both families read; its defaults are the cellular family's.

    The satellite is a flat mass-manufactured Flatellite-class bird (a fixed spec,
    NOT a re-spec'd frontier generation, so the DC ``generations`` / ``slopes``
    engine is dropped). Three dials: satellites per launch (a direct input), the
    operating life (the cohort cliff), and the one flat hardware build-cost scalar.
    The Iridium scenario sets all three. No field takes a YAML boolean or a quoted
    number: each is refused at load, naming the field (never read as 1 satellite, a
    1-year life or a $1M build); an integer loads as the build cost's float, and a
    whole-number float (16.0) as a count's integer, as before.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    satellites_per_launch: WholeNumber = Field(
        default=SATELLITES_PER_LAUNCH_DEFAULT,
        ge=SATELLITES_PER_LAUNCH_MIN,
        le=SATELLITES_PER_LAUNCH_MAX,
        description=(
            "Satellites per Neutron launch, a DIRECT input scalar (default "
            f"{SATELLITES_PER_LAUNCH_DEFAULT}, the cellular family's; bounds "
            f"{SATELLITES_PER_LAUNCH_MIN} to {SATELLITES_PER_LAUNCH_MAX}, the upper bound the "
            "validated stack with the block upgrade, COMM-713). The Iridium scenario sets 16, "
            "on the bound: the validated Flatellite stack with the Neutron block upgrade "
            "assumed from the first launch, for the stack kept in the fairing's cylinder at "
            "calculation C's pitch on a rod-held base (COMM-713); 15 is the mass-bound "
            "count today without the upgrade (COMM-712). The older render-read ~16 is "
            "COMM-258 / COMM-260; 12 loads about 9,600 kg of the ~13,000 kg LEO envelope."
        ),
    )
    satellite_lifetime_years: WholeNumber = Field(
        default=SATELLITE_LIFETIME_YEARS_DEFAULT,
        ge=1,
        le=SATELLITE_LIFETIME_YEARS_MAX,
        description=(
            "Satellite operating life in years, the cohort cliff: after this a "
            "cohort retires and contributes zero coverage. ~5-year Starlink "
            "depreciation and replacement-treadmill anchor (COMM-088; the "
            "separate COMM-091 is the per-subscriber cost split that lineage "
            "feeds), a design assumption not a certified field life. At most "
            f"{SATELLITE_LIFETIME_YEARS_MAX}, a sanity bound, not a sourced life."
        ),
    )
    satellite_build_cost_musd: float = Field(
        default=SATELLITE_BUILD_COST_MUSD_DEFAULT,
        gt=0,
        strict=True,
        description=(
            "The flat mass-manufactured hardware cost of one satellite, $M, ONE scalar, "
            "read by both families. The default, "
            f"{SATELLITE_BUILD_COST_MUSD_DEFAULT:g}, is the cellular family's (INVESTOR_SET, "
            "~$1.0 to 1.1M): a V3-class hardware analogy (Starlink V3 ~$1.2M, the upper "
            "anchor, COMM-080) for a direct-to-cell payload (bigger antenna and more power "
            "than a broadband panel, far smaller than AST's giant array, so AST ~$19 to 21M "
            "is the WRONG anchor), a hardware build-cost analogy, NOT a broadband-product "
            "claim. The Iridium scenario sets its own Flatellite's build cost. Configurable."
        ),
    )


class CoverageDials(BaseModel):
    """The fleet-sizing bounds: the coverage FLOOR and the cellular fleet CAP (variable 3).

    In the cellular family the fleet target the build-out fills toward is the CAPACITY
    need (the subscriber target divided by the per-satellite density, see
    :class:`SubscriberDials`), FLOORED by ``satellites_for_full_coverage`` (everyone must
    be able to see a satellite) and CAPPED by ``max_fleet_satellites`` (past which the
    spread servable base is exhausted). At a small base the floor binds (the engine
    reports the coverage regime); at a large base the capacity need binds; at an enormous
    base the cap binds. The floor may not exceed the cap (a model validator rejects it at
    load), so the three regime labels stay consistent with the fleet the engine sizes.
    The ELEVATION MASK is the underlying physical dial behind the floor (this default
    is the 25-degree quality-link, populated-band, 95%-coverage figure).

    On an Iridium config both fields keep their defaults (:class:`CommsConfig` refuses
    another value): the Iridium path pins the floor (nothing is sold in a year whose living
    fleet is below it) and has no cap.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    satellites_for_full_coverage: int = Field(
        default=SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
        ge=1,
        description=(
            "The coverage FLOOR: the minimum fleet for everyone in the served band "
            "to SEE a satellite (the lower bound on the fleet target, NOT the whole "
            "fleet when the base is large; at most max_fleet_satellites). "
            "INVESTOR_SET to 340: the quality-link case (25 degree elevation mask, "
            "populated mid-latitude band +/-55 deg at 95%, ~450 km, ~53 deg). The "
            "project coverage simulation (341, rounded to 340; the coverage-floor row "
            "of communications/assumptions.md carries the result and its honest "
            "bounds) plus COMM-209 / COMM-216 / COMM-217 and COMM-386..COMM-405. "
            "Configurable on a cellular config; pinned at this default on an Iridium "
            "config, where nothing is sold in a year whose living fleet is below it "
            "(another value there is refused at load)."
        ),
    )
    max_fleet_satellites: int = Field(
        default=MAX_FLEET_SATELLITES_DEFAULT,
        ge=1,
        description=(
            "The cellular family's fleet CAP: the largest fleet that family sizes to (the "
            "upper bound on its fleet target), never a saturation cap. Past this the "
            "spread, low-density servable base is exhausted and more satellites stop "
            "buying servable subscribers (a dense cell saturates). INVESTOR_SET to 2,000: "
            "the ~100M ambitious target (1,334 satellites at 75,000/sat) sits just under "
            "it. Source: the attached-subscribers answer (COMM-545) and the fleet-sizing rule "
            "(COMM-560). Configurable on a cellular config; an Iridium "
            "config, whose fleet has no cap, leaves it at this default (another value "
            "there is refused at load)."
        ),
    )

    @model_validator(mode="after")
    def _floor_at_or_below_cap(self) -> CoverageDials:
        """Reject a coverage floor above the fleet cap.

        The fleet target is ``min(cap, max(floor, capacity_need))``: with the floor
        above the cap the target silently becomes the cap while the binding regime
        still reads "coverage" and the coverage fraction never reaches 1.0, so the
        pair is rejected at config load.
        """
        if self.satellites_for_full_coverage > self.max_fleet_satellites:
            raise ValueError(
                "coverage.satellites_for_full_coverage "
                f"({self.satellites_for_full_coverage}) must not exceed "
                f"coverage.max_fleet_satellites ({self.max_fleet_satellites}): the "
                "coverage floor is the lower bound on the fleet target and the "
                "fleet cap the upper bound"
            )
        return self


class SubscriberDials(BaseModel):
    """The cellular family's CAPACITY dimension: the subscriber TARGET and the density.

    The unit is a PERSON (a phone subscriber), NOT a household (cellular is
    per-person). The subscriber TARGET (``subscribers_at_full_coverage``) is the
    INPUT, the base to SERVE; the engine sizes the fleet to serve it at
    ``subscribers_per_satellite`` attached subscribers per satellite (the capacity
    need), then floors by the coverage floor and caps by the fleet cap. The
    served count then RAMPS with the buildout (target x living-fleet / fleet-target),
    reaching the target at full deployment, and never exceeds the fleet target's
    people capacity (the cap binds in the saturated regime, and on an override larger
    than the fleet carries). This is capacity-SIZED (the fleet tracks
    the base), NOT capacity-DERIVED in the old sense (no spectrum -> capacity ->
    demand chain; the served base is a sized input, not a demand estimate). None of
    the field names use a forbidden demand-side token.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    subscribers_at_full_coverage: int = Field(
        default=SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT,
        ge=1,
        description=(
            "The SUBSCRIBER TARGET: the served-PERSON base (phone subscribers) the "
            "fleet is sized to serve, the model's INPUT, NOT a demand estimate, NOT a "
            "household count. INVESTOR_SET to a 10,000,000-person BASELINE (50,000,000 "
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
            "onboard chip last. DERIVED: the attached-subscribers answer's central band "
            "(COMM-545), sized by the fleet-sizing rule (COMM-560). Configurable."
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
            "TARGET dial, not this override, so an override above the fleet target's "
            "people capacity is capped at that capacity (with a logged warning). "
            "Default None means use the target."
        ),
    )


class RevenueDials(BaseModel):
    """The two REVENUE cases that ride the cohort treadmill (revenue and margin).

    The engine computes BOTH cases on every run (they are not mutually exclusive
    dials; each is a separate lens on the same fleet), mirroring the data-center
    model's revenue/margin pattern but adapted to the comms model's lighter
    single-value (no R-band) style:

    * COST-PLUS / MARGIN-TARGET (``revenue_multiple``): annual revenue = annual cost
      x the multiple, the same owner-operator basis as the DC central R (1.5 -> a 33.3%
      margin). A cost-coupled case (revenue tracks the cost basis).
    * PRICES-TODAY / ARPU (``arpu_usd_per_month``): annual revenue = served
      subscribers x the monthly ARPU x 12, a retail price applied to the served base.

    The margin in BOTH cases is ``(revenue - cost) / revenue`` against the same
    annualized cost basis the engine carries per cohort (the per-satellite lifetime
    cost spread over the satellite life, matching the DC annualized convention). The
    revenue is a cost-coupled multiple or a price-times-served-base figure, NEVER a
    demand, market-size, or willingness-to-pay estimate (no forbidden demand-side
    token appears on this block).
    """

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    revenue_multiple: float = Field(
        default=REVENUE_MULTIPLE_DEFAULT,
        gt=0,
        description=(
            "The COST-PLUS / MARGIN-TARGET revenue multiple: annual revenue = annual "
            "cost x this. INVESTOR_SET to 1.5 (cost+50%, an implied (1.5 - 1) / 1.5 = "
            "33.3% margin), mirroring the data-center central R = 1.5 "
            "(research/SOURCE_INDEX.md, RLDC-REVENUE-MULTIPLE-1_5X). Each 5-year "
            "cohort earns this margin "
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
    and sparse fresh-build) come from the ground research wave; the investor owns the
    final ground call and is still unsure about the comparison. Do not hardcode
    settled values in the comms src; supply them per-scenario. Either or both may be
    None, in which case that regime's ratio is skipped and the model still reports
    the space cost per subscriber.

    The space side of the comparison is the model's OWN COMPUTED cellular annual
    cost-per-subscriber (Phase 3), NEVER Starlink's disclosed broadband per-sub
    number. This block is declared in Phase 1 (the ``ground`` field defaults to
    None on :class:`CommsConfig`); Phase 4 consumes it in ``ground.py``.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    dense_ground_cost_per_subscriber_usd: float | None = Field(
        default=None,
        gt=0,
        description=(
            "Dense-served incumbent-marginal CELLULAR ground cost per subscriber "
            "(the mobile-network all-in cost per human subscriber), grounded ~$140 "
            "to 310/sub/yr. MARKED INTERFACE INPUT; optional (None-able) so the cost "
            "side never blocks. Source COMM-530 (the dense-served regime row) and "
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
        default="ground interface (research-grounded, investor owns the call)",
        description="Human-readable label for the supplied ground-interface scenario.",
    )
    source_note: str = Field(
        default="",
        description="Free-text record of the research provenance once firm (empty by default).",
    )


class IridiumArpuDials(BaseModel):
    """The Iridium model's five monthly prices, held flat (investor-set; the YAML's ``arpu:``).

    Each device class sells every seat its living fleet carries at its own price, and each
    of the two IoT lines is a fixed book at its own (their device counts are named constants,
    :data:`~communications.constants.MINIMAL_PACKET_IOT_DEVICES` and
    :data:`~communications.constants.DATA_IOT_DEVICES`, ADR 007, not settings). The classes
    run small terminal, mounted terminal, phone class, never phone-first. Every price is
    above 0 and at most :data:`~communications.constants.ARPU_PRICE_CEILING_USD_MONTH`, and
    a number, never a boolean (each field is strict: a YAML ``true`` is refused, not read as
    a price of 1).
    Government is left out of revenue (2026-10-04): there is no government price. A lower
    price or a smaller market is a division in the conclusions, never a setting here.

    Nested as the ``arpu`` field of :class:`IridiumDials`, defaulted, so every Iridium
    config carries the prices and the model has one shape.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    small_terminal_class_price_usd_month: float = Field(
        default=SMALL_TERMINAL_CLASS_PRICE_USD_MONTH_DEFAULT,
        gt=0,
        le=ARPU_PRICE_CEILING_USD_MONTH,
        strict=True,
        description=(
            "The small terminal's monthly price, dollars, held flat. INVESTOR_SET to "
            f"{SMALL_TERMINAL_CLASS_PRICE_USD_MONTH_DEFAULT:g} (2026-10-07; it was 15, set "
            "2026-10-03), the low end of the investor's 10-to-20 mass-market range (COMM-618 "
            "context). Configurable."
        ),
    )
    mounted_terminal_class_price_usd_month: float = Field(
        default=MOUNTED_TERMINAL_CLASS_PRICE_USD_MONTH_DEFAULT,
        gt=0,
        le=ARPU_PRICE_CEILING_USD_MONTH,
        strict=True,
        description=(
            "The mounted terminal's monthly price, dollars, held flat. INVESTOR_SET to "
            f"{MOUNTED_TERMINAL_CLASS_PRICE_USD_MONTH_DEFAULT:g} (2026-10-07; it was 100, set "
            "2026-10-03), near Iridium's voice and data $47 and well under Certus $259 "
            "(COMM-618). Configurable."
        ),
    )
    phone_class_price_usd_month: float = Field(
        default=PHONE_CLASS_PRICE_USD_MONTH_DEFAULT,
        gt=0,
        le=ARPU_PRICE_CEILING_USD_MONTH,
        strict=True,
        description=(
            "The phone class's monthly price, dollars, held flat. INVESTOR_SET to "
            f"{PHONE_CLASS_PRICE_USD_MONTH_DEFAULT:g} (2026-10-03), its floor: no price "
            "haircut takes it lower. Configurable."
        ),
    )
    minimal_packet_iot_price_usd_month: float = Field(
        default=MINIMAL_PACKET_IOT_PRICE_USD_MONTH_DEFAULT,
        gt=0,
        le=ARPU_PRICE_CEILING_USD_MONTH,
        strict=True,
        description=(
            "Minimal-packet IoT's monthly price per device, dollars. INVESTOR_SET to "
            f"{MINIMAL_PACKET_IOT_PRICE_USD_MONTH_DEFAULT:g} (the investor's trial price, "
            "2026-10-04). Configurable."
        ),
    )
    data_iot_price_usd_month: float = Field(
        default=DATA_IOT_PRICE_USD_MONTH_DEFAULT,
        gt=0,
        le=ARPU_PRICE_CEILING_USD_MONTH,
        strict=True,
        description=(
            "Data IoT's monthly price per device, dollars. INVESTOR_SET to "
            f"{DATA_IOT_PRICE_USD_MONTH_DEFAULT:g} (the investor's trial price, 2026-10-04; "
            "Iridium's IoT ARPU is 7.78 today, COMM-618). Configurable."
        ),
    )


class SaturationDials(BaseModel):
    """The Iridium model's saturation block: the downlink time share and the promoted curve.

    Nested as the ``saturation`` field of :class:`IridiumDials`, with every field defaulted, so
    every Iridium config carries the block (the shipped scenario writes it out). Neither field
    is an input of the curve: the curve is computed with the band in full-time use (d = 1, ADR
    008), and one promoted file serves every value of d; the curve's inputs are the held
    spectrum and the named constants
    (:func:`communications.saturation_curve.saturation_inputs_for`).
    """

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    downlink_share: float = Field(
        default=DOWNLINK_SHARE_DEFAULT,
        gt=0,
        le=1.0,
        strict=True,
        description=(
            "The downlink time share d of Iridium's time-division duplex band, a fraction "
            "above 0 and at most 1 (ADR 008). Default 0.67, Certus 700's 2 : 1 down-to-up rate "
            "split (COMM-620); 0.5 is the symmetric frame and 0.75 an estimated alternative. "
            "Configurable."
        ),
    )
    curve_path: str = Field(
        default=SATURATION_CURVE_PATH_DEFAULT,
        min_length=1,
        description=(
            "The promoted saturation curve's path, repository-relative (an absolute path is "
            "allowed, so a test can point at a temporary curve). Default "
            "communications/models/iridium/saturation_curve.json, where the saturation "
            "command writes it."
        ),
    )


class IridiumDials(BaseModel):
    """The Iridium model's (L-band max-outcome) input dials: the MSS lane.

    Present (non-None on :class:`CommsConfig`) selects the Iridium model. It reads every
    device class's people from the promoted saturation curve, side by side in one run, on
    the fleet the comms share of the launch cadence builds, and sells every seat at each
    class's flat price. Its settings are the held spectrum (``spectrum_mhz``, a WIDTH, not a
    frequency, which the curve's identity check pins), the panel (``aperture_m2``, applied
    linearly on the curve), the label, the ``saturation`` block (the downlink time share and
    the curve's path) and the ``arpu`` block (the five monthly prices). Each class's usage,
    its central spectral efficiency and the two IoT lines' device counts are named constants
    (:mod:`communications.constants`), not settings; a scenario still setting a retired one
    fails at load, naming it (``extra="forbid"``). The Iridium model is the MSS lane
    (purpose-built or in-chipset devices on owned L-band), never an unmodified phone (that is
    the cellular lane, the High-Bandwidth Cellular Pure Play model).

    Every number here is finite: a NaN or an infinity is refused at load, naming the field
    (``allow_inf_nan=False``, as the saturation curve's contract models refuse them), so no
    run starts from one. The nested ``saturation`` and ``arpu`` blocks refuse them the same
    way. No number here or in those blocks is a boolean: each numeric field is strict, so a
    YAML ``true`` (or ``yes``, ``on``) is refused at load, naming the field, rather than read
    as 1 (a 1 m^2 panel, d = 1, a price of 1), and so is a quoted number; an integer still
    loads as its float.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    spectrum_mhz: float = Field(
        default=SPECTRUM_MHZ_DEFAULT,
        gt=0,
        strict=True,
        description=(
            "The L-band WIDTH held in MHz (a width, NOT a frequency; the frequency is "
            "the ~1.6 GHz dial position). INVESTOR_SET to 8.0, the Iridium exclusive "
            "holding (~7.775 rounded). The saturation curve is computed at it: another "
            "width runs only on a curve computed for it (the identity check). The "
            "coordinated 10.5 MHz span is not modeled (a conclusions note)."
        ),
    )
    aperture_m2: float = Field(
        default=APERTURE_M2_DEFAULT,
        gt=0,
        strict=True,
        description=(
            f"The satellite's flat panel area in m^2. Default {APERTURE_M2_DEFAULT:g}, the "
            "validated Flatellite body (COMM-711, the investor's approved default of "
            "2026-10-03), an upper bound. The saturation curve is computed at the "
            f"{APERTURE_REFERENCE_M2:g} m^2 reference panel and applied linearly: people, "
            "useful beams, capacity and maximum use scale with this over the reference (the "
            "panel factor), while the saturation numbers, the ocean factor and satellites per "
            "launch do not move. What the linear rule gives against the panel computed "
            "outright, measured, is stated with the run's assumptions (below the reference "
            "panel every class carries at least what the rule gives; above it the rule gives "
            "more useful beams than the panel would). Above "
            f"{APERTURE_VALIDATED_STACK_LIMIT_M2:g} m^2, the largest flat panel the validated "
            "stack holds, the assumptions carry the stack caveat, deliberately NOT a bound, "
            "so a larger panel stays computable. INVESTOR-DIRECTED. Configurable."
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
    saturation: SaturationDials = Field(
        default_factory=SaturationDials,
        description=(
            "The saturation block (:class:`SaturationDials`): the downlink time share and the "
            "promoted saturation curve's path. Defaulted, so every Iridium config carries it."
        ),
    )
    arpu: IridiumArpuDials = Field(
        default_factory=IridiumArpuDials,
        description=(
            "The five monthly prices (:class:`IridiumArpuDials`): the small terminal's, the "
            "mounted terminal's, the phone class's, minimal-packet IoT's and data IoT's. "
            "Defaulted, so every Iridium config carries the prices and the two IoT lines, "
            "and every consumer reads one shape."
        ),
    )


# ===========================================================================
# 2. The top-level CommsConfig
# ===========================================================================


class CommsConfig(BaseModel):
    """The complete configuration for one communications cost run (either family).

    Construct one (the defaults reproduce the High-Bandwidth Cellular Pure Play
    central case), or load one from YAML with :func:`load_comms_config`. Hand a
    cellular config to the cellular entry, ``communications.engine.run_comms_model``,
    and an Iridium config, with its saturation curve, to the Iridium entry,
    ``communications.iridium.run_iridium_model``; the Iridium artifact writer
    (``communications.json_output``) assembles the promoted JSON from the run. On an
    Iridium config every field of the ``coverage``, ``subscribers`` and ``revenue`` blocks
    keeps its default and ``ground`` stays None
    (:meth:`_iridium_keeps_the_cellular_dials_at_their_defaults`).

    Every block defaults via ``default_factory`` (or, for ``ground`` and ``iridium``,
    a plain None) so a config constructed with no arguments, or a YAML omitting a
    block, gets a fully valid all-default block. The ``ground`` field is ``None`` by
    default, which is what makes the cost side run with no ground number; the
    ``iridium`` field is ``None`` by default, which selects the High-Bandwidth
    Cellular Pure Play path (a non-None ``iridium`` selects the Iridium model).
    """

    model_config = ConfigDict(
        extra="forbid", frozen=True, validate_assignment=True, allow_inf_nan=False
    )

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
        description="The satellite spec both families read: per-launch count, life, build cost.",
    )
    coverage: CoverageDials = Field(
        default_factory=CoverageDials,
        description=(
            "The cellular family's fleet-sizing bounds: the coverage floor (pinned on the "
            "Iridium path) and the fleet cap."
        ),
    )
    subscribers: SubscriberDials = Field(
        default_factory=SubscriberDials,
        description=(
            "The cellular family's capacity dimension: subscriber target, per-satellite "
            "density, override."
        ),
    )
    revenue: RevenueDials = Field(
        default_factory=RevenueDials,
        description=(
            "The cellular family's two revenue cases: the cost-plus multiple and the "
            "prices-today ARPU."
        ),
    )
    ground: GroundInterfaceDials | None = Field(
        default=None,
        description=(
            "The marked, TWO-REGIME ground interface (Phase 4). None by default so "
            "the cost side runs with no ground number; supply it per-scenario on a "
            "cellular config (an Iridium config refuses one)."
        ),
    )
    iridium: IridiumDials | None = Field(
        default=None,
        description=(
            "The Iridium model's (L-band max-outcome) dials. None by default so the "
            "config is the High-Bandwidth Cellular Pure Play model (cellular "
            "direct-to-cell); set it to select the Iridium model."
        ),
    )

    @model_validator(mode="after")
    def _iridium_keeps_the_cellular_dials_at_their_defaults(self) -> CommsConfig:
        """Refuse, on an Iridium config, a cellular sizing or revenue dial off its default, and
        a ground block.

        The Iridium path reads none of the cellular family's sizing and revenue dials (its
        fleet is the cadence's, its people the saturation curve's, its prices the ``arpu``
        block's) and pins the coverage floor (one shell, one floor; the IoT counts are sized
        at it, ADR 007). So on an Iridium config every field of the ``coverage``,
        ``subscribers`` and ``revenue`` blocks keeps its default, and ``ground``, which no
        Iridium run reads, stays None. The check walks each block's own fields against a
        block built with its defaults, so a field added later is refused with no edit here;
        each refusal names the field, its default and the value.

        The check is on the value, not on whether the field was written: the test helpers
        round-trip configs through ``model_dump`` and ``model_validate``, which marks every
        field as set, so a config written out whole still loads. It runs when a config is
        loaded or validated (a construction or a ``model_validate``); a ``model_copy``
        update is not validated, by pydantic's design (it trusts the data it is given).
        """
        if self.iridium is None:
            return self
        blocks: tuple[tuple[str, BaseModel], ...] = (
            ("coverage", self.coverage),
            ("subscribers", self.subscribers),
            ("revenue", self.revenue),
        )
        for block_name, block in blocks:
            defaults = type(block)()
            for field_name in type(block).model_fields:
                value = getattr(block, field_name)
                default = getattr(defaults, field_name)
                if value != default:
                    raise ValueError(
                        f"{block_name}.{field_name} is not a setting on an Iridium config (one "
                        "with an 'iridium:' block): the Iridium path reads none of the cellular "
                        "family's sizing and revenue dials and pins the coverage floor, so it "
                        f"keeps its default, {default!r}; got {value!r}"
                    )
        if self.ground is not None:
            raise ValueError(
                "ground is not a setting on an Iridium config (one with an 'iridium:' block): "
                "no Iridium run reads the cellular ground interface, so it stays unset; got a "
                "ground block"
            )
        return self


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
    ``subscribers``, ``revenue``, ``ground``, ``iridium``), all optional (omitted =
    defaults). An empty dict yields an all-defaults config.

    Validation is Pydantic's: an unknown key, a wrong type, an out-of-bounds value,
    or a missing required field raises :class:`pydantic.ValidationError` with a
    precise location.
    """
    if not isinstance(data, dict):
        raise ValueError("config root must be a mapping (a YAML object)")
    return CommsConfig.model_validate(data)


def load_comms_config(path: str | Path) -> CommsConfig:
    """Load and validate a :class:`CommsConfig` from a YAML file.

    The file is read through the shared
    :func:`common.file_io.load_yaml_mapping`; an empty file yields an
    all-defaults :class:`CommsConfig`.

    Args:
        path: The scenario YAML file.

    Returns:
        The validated config.

    Raises:
        common.file_io.ModelFileError: If the file is missing, unreadable,
            malformed, or not a YAML mapping.
        pydantic.ValidationError: If the content is not a valid config.
    """
    return comms_config_from_dict(load_yaml_mapping(Path(path)))


# Re-export the public config surface so external callers (engine, ground, output,
# tests) import from one place.
__all__ = [
    "CommsCadenceDials",
    "CommsConfig",
    "CommsMetadataDials",
    "CoverageDials",
    "GroundInterfaceDials",
    "IridiumArpuDials",
    "IridiumDials",
    "RevenueDials",
    "SatelliteDials",
    "SaturationDials",
    "SubscriberDials",
    "comms_config_from_dict",
    "load_comms_config",
]
