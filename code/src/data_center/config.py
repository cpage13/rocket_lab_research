"""The dial schema and YAML loader for the GPU-first valuation calculator.

The cycle-2 v8 schema extends the GPU-first per-node dial set with the
fleet / volume / cadence / R-band blocks:

* :class:`ValuationConfig` carries:
    * ``gospel: GospelInputs`` — the locked numeric anchors (mass envelope,
      bus dynamics, solar/radiator $/kW, radiator t/kW pre/post Tjmax lift,
      release cadence).
    * ``slopes: GenerationSlopes`` — post-Feynman per-generation growth
      slopes used to extrapolate generations beyond ``KNOWN_GENS``.
    * ``generations: list[GenerationSpec] | None`` — optional per-generation
      override. ``None`` (the default) means use the bundled ``KNOWN_GENS``.
    * ``scenario_name: str`` — human-readable label shown in the report.
    * ``metadata: MetadataConfig`` — the three founder-locked enums plus
      base year + horizon.
    * ``cadence: CadenceDials`` — launch-cadence logistic-ramp dials.
    * ``fleet: FleetDials`` — fleet-rollup service-life cliff dial.
    * ``volume: VolumeDials`` — stowed-volume-envelope dials.
    * ``r_band: RBand`` — the three R trajectories (low/central/high).
    * ``launch_cost: LaunchCostDials`` — cadence-indexed launch-cost dials.

Cycle-2 categorical enums (:class:`WorkloadType`, :class:`OperatorModel`,
:class:`RadiatorArchitecture`, :class:`BindingConstraint`) are defined
here too.

YAML loading: scenario files are YAML mappings whose top-level keys are
the block names above — all optional (omitted = defaults). ``extra="forbid"``
means a typo in a scenario file fails loudly.
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any  # typing-acceptable: Any types the dict deserialization boundary

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator

from data_center.constants import (
    CADENCE_CEILING_DEFAULT,
    FIRST_LAUNCH_YEAR_DEFAULT,
    FOLD_RATIO,
    HIGH_CADENCE_COST_MUSD_DEFAULT,
    HIGH_CADENCE_LAUNCHES_DEFAULT,
    LAUNCHES_AT_YEAR_5_DEFAULT,
    LAUNCHES_AT_YEAR_10_DEFAULT,
    LOW_CADENCE_COST_MUSD_DEFAULT,
    LOW_CADENCE_LAUNCHES_DEFAULT,
    MAX_FY,
    MAX_HORIZON_YEARS,
    MIN_FY,
    MIN_HORIZON_YEARS,
    MOUNTING_OVERHEAD_PCT,
    NEUTRON_FAIRING_USABLE_VOLUME_M3,
    R_BAND_CENTRAL_ANCHORS_DEFAULT,
    R_BAND_HIGH_ANCHORS_DEFAULT,
    R_BAND_LOW_ANCHORS_DEFAULT,
    RADIATOR_SOLAR_AREA_RATIO,
    SERVICE_LIFE_YEARS,
    SI_AREAL_DENSITY_KG_M2,
    SI_BOL_EFFICIENCY,
    STOWED_PITCH_MM,
)
from data_center.generations import (
    GENERATIONS_YAML_KEY,
    GenerationSlopes,
    GenerationSpec,
    load_generations_yaml,
)

# ===========================================================================
# 0. Cycle-2 v8 categorical enums
# ===========================================================================


class WorkloadType(StrEnum):
    """The compute workload the data centre serves.

    Locked to ``INFERENCE`` by D14 (founder decision). No ``TRAINING``
    member — the venture does not model a training-workload framing.
    """

    INFERENCE = "inference"


class OperatorModel(StrEnum):
    """The commercial operating model for the data centre.

    Locked to ``B2B_DEDICATED_OPTICAL_RF`` by D15 — business-to-business
    with a dedicated optical/RF uplink (the premium-driver narrative).
    Further operator models may be added in later cycles.
    """

    B2B_DEDICATED_OPTICAL_RF = "b2b_dedicated_optical_rf"


class RadiatorArchitecture(StrEnum):
    """The radiator mounting architecture.

    Locked to ``SINGLE_FACE_CO_MOUNTED`` by D16 (founder: "solar is on
    one side and the radiator is on the other"). No ``TWO_FACE_DEDICATED``
    or ``MIXED`` members — the founder rejected enum proliferation; one
    architecture only.
    """

    SINGLE_FACE_CO_MOUNTED = "single_face_co_mounted"


class BindingConstraint(StrEnum):
    """Which physical envelope constraint binds the node's package count.

    Mass-only binding is the model rule (D6); ``VOLUME`` (sole) appearing
    is a model-consistency failure surfaced by V15.
    """

    MASS = "mass"
    VOLUME = "volume"
    BOTH = "both"
    NEITHER = "neither"


# ===========================================================================
# 1. Cycle-2 v8 dial blocks
# ===========================================================================


class CadenceDials(BaseModel):
    """Launch-cadence dials feeding the logistic launches-per-year ramp.

    Defaults are the v7-archaeology values (commit 8fdc210), but the
    default is now explicitly a source-indexed scenario: ``launches_at_year_5``
    and ``launches_at_year_10`` fit the logistic curve to integer mission
    counts. ``first_launch_year`` only clamps earlier years to zero; it does
    not move the year-5 or year-10 anchors. Consumed by
    :func:`data_center.cadence.compute_launches_per_year`.
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


class FleetDials(BaseModel):
    """Fleet-rollup dials governing the cohort-vintaging cliff.

    Consumed by the Phase 3 fleet rollup; the service-life value sets the
    hard cliff after which a cohort contributes zero revenue.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    service_life_years: int = Field(
        default=SERVICE_LIFE_YEARS,
        ge=1,
        le=20,
        description=(
            "Node operating life in years; hard cliff. Scenario assumption "
            "from SOURCE_INDEX THR-008, not certified GPU field life."
        ),
    )


class VolumeDials(BaseModel):
    """Volume-envelope dials for the stowed solar+radiator volume check.

    All defaults are R1-sourced. Consumed by the Phase 3 volume module;
    the volume check is for transparency and does NOT gate package count
    (mass-only binding, D6).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    si_areal_density_kg_m2: float = Field(
        default=SI_AREAL_DENSITY_KG_M2,
        gt=0,
        description="Full Si array areal density including structure, kg/m2.",
    )
    si_bol_efficiency: float = Field(
        default=SI_BOL_EFFICIENCY,
        gt=0,
        lt=1,
        description="Si beginning-of-life AM0 conversion efficiency.",
    )
    fold_ratio: float = Field(
        default=FOLD_RATIO,
        gt=0,
        description="Deployed-to-stowed solar-array area ratio.",
    )
    stowed_pitch_mm: float = Field(
        default=STOWED_PITCH_MM,
        gt=0,
        description="Per-panel stowed thickness (Si + co-mounted radiator), mm.",
    )
    radiator_solar_area_ratio: float = Field(
        default=RADIATOR_SOLAR_AREA_RATIO,
        gt=0,
        description="Radiator area / solar area for single-face co-mounted.",
    )
    mounting_overhead_pct: float = Field(
        default=MOUNTING_OVERHEAD_PCT,
        ge=0,
        lt=1,
        description="Mass/volume overhead from hinges, yokes, motors.",
    )
    neutron_fairing_usable_volume_m3: float = Field(
        default=NEUTRON_FAIRING_USABLE_VOLUME_M3,
        gt=0,
        description="Neutron fairing usable payload volume, m3.",
    )


class LaunchCostDials(BaseModel):
    """Cadence-indexed launch-cost dials feeding the log-linear cost curve.

    Defaults are the v7-archaeology values. Consumed by
    :func:`data_center.cadence.compute_launch_cost_musd`.
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


class GospelInputs(BaseModel):
    """The locked numeric anchors — gospel constants from plan § 0.

    The v8 gospel block is the cycle-1 gospel verbatim **minus the six
    fields that moved to dedicated v8 blocks** (D18/D24): ``r_revenue_cost``
    (→ :class:`RBand`), ``launch_y0_musd`` / ``launch_y10_musd`` (→
    :class:`LaunchCostDials`), ``service_life_years`` (→ :class:`FleetDials`),
    and ``base_year`` / ``horizon_years`` (→ :class:`MetadataConfig`). What
    remains is the genuinely-gospel physical + cost-dial set: the mass and
    volume envelopes, the Tjmax-lift state, the solar / radiator t/kW, the
    bus + solar + radiator cost dials, and the generation release cadence.

    Defaults reproduce plan § 0's central case exactly — so a config
    constructed with no arguments, or a YAML omitting the ``gospel`` block,
    is fully valid.

    Excludes the per-generation values (in the engine's generation list)
    and the post-Feynman growth slopes (in :class:`GenerationSlopes`).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    mass_envelope_t: float = Field(
        default=12.5,
        description=(
            "Neutron block-upgrade reusable SSO payload scenario, tonnes "
            "(SOURCE_INDEX NTR-007) — the model's hard physical constraint "
            "on the node, not a published Rocket Lab SSO payload."
        ),
        gt=0.0,
    )
    node_mass_fixed_t: float = Field(
        default=2.5,
        description=(
            "Fixed-per-node mass overhead (bus + propulsion + structure), "
            "tonnes — subtracted from the envelope before packing GPUs."
        ),
        ge=0.0,
    )
    node_volume_fixed_m3: float = Field(
        default=5.0,
        description=(
            "Fixed-per-node stowed volume overhead (bus + structure), m3 "
            "— added to the stowed package-array volume in the cycle-2 "
            "volume-envelope check. New in v8; cycle-1 had no volume term."
        ),
        ge=0.0,
    )
    tjmax_lift_year: int = Field(
        default=5,
        description=(
            "Year index (0-based) at which the radiator hot-loop arrives "
            "and radiator t/kW steps down (D11)."
        ),
        ge=0,
    )
    bus_base_musd: float = Field(
        default=8.0,
        description="Year-0 bus cost (vehicle + avionics + propulsion), $M.",
        gt=0.0,
    )
    bus_flatten_after_yr: int = Field(
        default=5,
        description=(
            "Year (0-based) after which bus cost holds flat instead of "
            "continuing its real decline (D12)."
        ),
        ge=0,
    )
    bus_growth_pre: float = Field(
        default=-0.03,
        description=(
            "Bus real-cost growth per year between year 0 and "
            "'bus_flatten_after_yr' (negative = decline)."
        ),
    )
    solar_cost_musd_per_kw: float = Field(
        default=0.04,
        description="Solar-array cost per kilowatt of flown power, $M/kW.",
        gt=0.0,
    )
    radiator_cost_musd_per_kw: float = Field(
        default=0.04,
        description="Radiator cost per kilowatt of flown power, $M/kW.",
        gt=0.0,
    )
    solar_mass_t_per_kw: float = Field(
        default=0.011,
        description="Solar-array mass per kilowatt of flown power, t/kW.",
        gt=0.0,
    )
    radiator_t_per_kw_pre: float = Field(
        default=0.013,
        description=(
            "Radiator t/kW before the Tjmax lift (pre 'tjmax_lift_year') — "
            "the conservative t/kW (D11)."
        ),
        gt=0.0,
    )
    radiator_t_per_kw_post: float = Field(
        default=0.012,
        description=(
            "Radiator t/kW after the Tjmax lift (post 'tjmax_lift_year') — "
            "the hot-loop coolant arrives and lowers t/kW (D11). Cycle-2 "
            "lifts this to 0.012 (central of the R1 0.010-0.014 band) for "
            "the single-face co-mounted architecture (D16/D17); cycle-1's "
            "value was 0.007."
        ),
        gt=0.0,
    )
    release_cadence_yr: float = Field(
        default=1.5,
        description=("Years per generation, used to extrapolate post-Feynman generations (D6)."),
        gt=0.0,
    )


class YearRValue(BaseModel):
    """A single (fiscal year, R) anchor on an R-band trajectory.

    R is the revenue-to-cost multiplier; ``revenue = R x cost``. The
    engine linearly interpolates R between adjacent anchors.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    fy: int = Field(
        ge=MIN_FY,
        le=MAX_FY,
        description="Fiscal (calendar) year of this anchor.",
    )
    r: float = Field(
        gt=0,
        description="Revenue-to-cost multiplier R at this fiscal year.",
    )


def _anchors_to_models(anchors: tuple[tuple[int, float], ...]) -> list[YearRValue]:
    """Convert a tuple of ``(fy, r)`` pairs to a list of :class:`YearRValue`."""
    return [YearRValue(fy=fy, r=r) for fy, r in anchors]


class RBand(BaseModel):
    """The three R trajectories (low / central / high) with year anchors.

    Each trajectory is a list of :class:`YearRValue` anchors, sorted by
    ``fy`` ascending, with at least two anchors. The engine interpolates R
    linearly between adjacent anchors. Defaults are scenario assumptions tied
    to SOURCE_INDEX REV-008, not observed orbital-compute pricing.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    central: list[YearRValue] = Field(
        default_factory=lambda: _anchors_to_models(R_BAND_CENTRAL_ANCHORS_DEFAULT),
        description="Central R trajectory anchors.",
    )
    low: list[YearRValue] = Field(
        default_factory=lambda: _anchors_to_models(R_BAND_LOW_ANCHORS_DEFAULT),
        description="Low (bear-case) R trajectory anchors.",
    )
    high: list[YearRValue] = Field(
        default_factory=lambda: _anchors_to_models(R_BAND_HIGH_ANCHORS_DEFAULT),
        description="High (bull-case) R trajectory anchors.",
    )

    @field_validator("central", "low", "high")
    @classmethod
    def _at_least_two_anchors_sorted(cls, v: list[YearRValue]) -> list[YearRValue]:
        """Each trajectory needs >= 2 anchors, sorted by fy ascending."""
        if len(v) < 2:
            raise ValueError("Each R-band trajectory needs at least 2 anchors")
        years = [a.fy for a in v]
        if years != sorted(years):
            raise ValueError("R-band anchors must be sorted by fy ascending")
        return v


class MetadataConfig(BaseModel):
    """The run metadata block: the three enum locks + base year + horizon.

    The three enums (workload, operator, radiator architecture) are
    founder-locked (D14-D16); their defaults are the only valid members.
    ``base_year`` and ``horizon_years`` move here from the cycle-1 gospel
    block in the v8 schema.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    workload_type: WorkloadType = WorkloadType.INFERENCE
    operator_model: OperatorModel = OperatorModel.B2B_DEDICATED_OPTICAL_RF
    radiator_architecture: RadiatorArchitecture = RadiatorArchitecture.SINGLE_FACE_CO_MOUNTED
    deployment_philosophy: str = "ground_validated_before_launch"
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


# ===========================================================================
# 2. The top-level GPU-first ValuationConfig
# ===========================================================================


class ValuationConfig(BaseModel):
    """The complete configuration for one GPU-first valuation run.

    Construct one (the defaults reproduce the central plan-§-0 case), or
    load one from YAML with :func:`load_config`. Hand it to
    :func:`data_center.engine.run_valuation`.

    Each block defaults via Pydantic's ``default_factory`` so a config
    constructed with no arguments — or a YAML omitting a block — gets a
    fully valid all-default block.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    gospel: GospelInputs = Field(
        default_factory=GospelInputs,
        description=(
            "Locked numeric anchors from plan § 0 (mass envelope, R, "
            "launch endpoints, bus dynamics, solar/radiator $/kW, radiator "
            "t/kW pre/post Tjmax lift, release cadence, horizon)."
        ),
    )

    slopes: GenerationSlopes = Field(
        default_factory=lambda: _default_slopes(),
        description=(
            "Post-Feynman per-generation growth slopes used to extrapolate "
            "generations beyond the last sourced generation."
        ),
    )

    generations: list[GenerationSpec] | None = Field(
        default=None,
        description=(
            "Optional override of the per-generation GPU spec list. "
            "None (the default) means use the bundled KNOWN_GENS. "
            "A scenario can supply a full or partial list to model "
            "delayed/accelerated roadmaps."
        ),
    )

    scenario_name: str = Field(
        default="Default (central case)",
        description=(
            "Human-readable scenario label, surfaced in the report header "
            "and in the JSON output's manifest.scenario field."
        ),
    )

    # --- cycle-2 v8 blocks ------------------------------------------------
    metadata: MetadataConfig = Field(
        default_factory=lambda: _default_metadata(),
        description=(
            "Run metadata: the three founder-locked enums (workload, "
            "operator model, radiator architecture) plus base year and "
            "horizon (which move here from the cycle-1 gospel block)."
        ),
    )

    cadence: CadenceDials = Field(
        default_factory=CadenceDials,
        description="Launch-cadence dials feeding the logistic launch ramp.",
    )

    fleet: FleetDials = Field(
        default_factory=FleetDials,
        description="Fleet-rollup dials (cohort service-life cliff).",
    )

    volume: VolumeDials = Field(
        default_factory=VolumeDials,
        description="Volume-envelope dials for the stowed-volume check.",
    )

    r_band: RBand = Field(
        default_factory=RBand,
        description="The three R trajectories (low/central/high) with anchors.",
    )

    launch_cost: LaunchCostDials = Field(
        default_factory=LaunchCostDials,
        description="Cadence-indexed launch-cost dials (log-linear curve).",
    )


# ===========================================================================
# 3. Default-builder helpers
# ===========================================================================


def _default_slopes() -> GenerationSlopes:
    """Build a default `GenerationSlopes` matching plan-§-0 growth rates.

    The named constructor exists to satisfy mypy --strict + Pydantic v2:
    `GenerationSlopes()` (no args) is rejected at strict check time
    because mypy treats Pydantic field defaults as not satisfying the
    call-arg requirement. Naming every kwarg here side-steps that quirk
    while keeping `ValuationConfig.slopes` constructible via a no-arg
    default_factory. Phase 4 can fold this back when mypy/Pydantic
    settle the call-arg rule for `BaseModel` field defaults.
    """
    return GenerationSlopes(
        usd_growth_per_gen=0.30,
        # 0.20 — per-package power growth/gen; corrected from 0.30
        # (assembly-rate misapplied) per validation V-A,
        # sourcing_audit_05_21.md.
        kw_growth_per_gen=0.20,
        kg_growth_per_gen=-0.10,
        pf_growth_per_gen=0.625,
    )


def _default_metadata() -> MetadataConfig:
    """Build a default :class:`MetadataConfig` for the central case.

    A named builder is required because :class:`MetadataConfig` has two
    required fields (``base_year``, ``horizon_years``) with no defaults,
    so ``default_factory=MetadataConfig`` would fail. The three enum
    locks fall to their (only) members; base year / horizon reproduce
    the cycle-1 central case.
    """
    return MetadataConfig(base_year=2026, horizon_years=10)


# ===========================================================================
# 4. YAML loader
# ===========================================================================


def config_from_dict(data: dict[str, Any]) -> ValuationConfig:
    """Build a :class:`ValuationConfig` from an already-parsed YAML mapping.

    Top-level keys are the v8 block names — ``gospel``, ``slopes``,
    ``generations``, ``scenario_name``, ``metadata``, ``cadence``,
    ``fleet``, ``volume``, ``r_band``, ``launch_cost`` — all optional.
    ``generations`` may be a list of per-generation specs (each validated
    against `GenerationSpec`) or a string path to a YAML file containing a
    top-level ``generations: [...]`` mapping.

    Validation is Pydantic's: an unknown key, a wrong type, an
    out-of-bounds value, or a missing required field raises
    :class:`pydantic.ValidationError` with a precise location.
    """
    if not isinstance(data, dict):
        raise ValueError("config root must be a mapping (a YAML object)")
    # If `generations` is a string, treat it as a path to a generations YAML
    # file and load it. Lets a scenario point at the bundled
    # `scenarios/generations.yaml` (or a custom file) instead of inlining the
    # whole list.
    gens_raw = data.get("generations")
    if isinstance(gens_raw, str):
        data = dict(data)  # don't mutate the caller's dict
        data["generations"] = load_generations_yaml(Path(gens_raw))
    return ValuationConfig.model_validate(data)


def load_config(path: str | Path) -> ValuationConfig:
    """Load and validate a :class:`ValuationConfig` from a YAML file.

    Raises :class:`FileNotFoundError` if the path does not exist and
    :class:`ValueError` (specifically a :class:`pydantic.ValidationError`)
    on any malformed or invalid content.
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
        return ValuationConfig()
    if not isinstance(data, dict):
        raise ValueError(f"config file {p} must contain a YAML mapping (got {type(data).__name__})")
    return config_from_dict(data)


# Re-export the public config surface so external callers (CLI, tests,
# downstream modules) import from one place.
__all__ = [
    "GENERATIONS_YAML_KEY",
    "BindingConstraint",
    "CadenceDials",
    "FleetDials",
    "GospelInputs",
    "LaunchCostDials",
    "MetadataConfig",
    "OperatorModel",
    "RBand",
    "RadiatorArchitecture",
    "ValuationConfig",
    "VolumeDials",
    "WorkloadType",
    "YearRValue",
    "config_from_dict",
    "load_config",
]
