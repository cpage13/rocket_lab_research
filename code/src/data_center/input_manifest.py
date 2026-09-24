"""Typed input manifest for the public space-model JSON artifact.

This module owns the ``inputs`` contract for the promoted space model. It turns
the validated scenario config and generated hardware roadmap into source-linked
``InputCell`` objects, then exposes both a nested typed tree and a flat path
index so agents can traverse assumptions without reading Python source.

The source metadata in the ``*_SPECS`` tables (claim ID, status, rationale)
describes the default values. A scenario value that differs from the default
(the code defaults, which ``code/scenarios/default.yaml`` mirrors) is
published as a scenario override instead: role ``scenario_override``, status
``scenario``, and the scenario YAML as its only source
(:func:`common.input_manifest._spec_cell`). Every cell, the R-band anchors
included, lands in the flat ``assumption_index`` (:func:`collect_input_cells`).
"""

from __future__ import annotations

import logging
from enum import StrEnum
from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from common.input_manifest import (
    AssumptionRole,
    CellSpec,
    ConfigFieldName,
    InputCell,
    InputPath,
    InputValue,
    SourceRef,
    SourceRefType,
    SourceStatus,
    SupportingClaim,
    _cell,
    _field_description,
    _research_ref,
    _source_index_ref,
    _spec_cell,
)
from common.provenance import FieldPath, as_float
from data_center.config import ValuationConfig, YearRValue
from data_center.generations import GenerationSpec, SourcingClass

logger = logging.getLogger(__name__)

DEFAULT_SCENARIO_PATH: Final[str] = "code/scenarios/default.yaml"
"""Repository-relative path of the canonical default scenario (see :func:`is_default_scenario`)."""
MARKET_REFERENCE_CAPACITY_GW: Final[float] = 100.0

CENTRAL_R_CLAIM_ID: Final[str] = "RLDC-REVENUE-MULTIPLE-1_5X"
"""SOURCE_INDEX claim describing the default central R band."""

SENSITIVITY_R_CLAIM_ID: Final[str] = "REV-008"
"""SOURCE_INDEX claim describing the default low and high R sensitivity bands."""

REVENUE_PATH_PREFIX: Final[FieldPath] = "inputs.config.revenue"
"""Public path of the R-band input tree; each anchor cell sits at
``<prefix>.<band>.<fiscal year>`` (:func:`revenue_anchor_path`)."""

RELEASE_CADENCE_PATH: Final[FieldPath] = "inputs.config.physical.release_cadence_yr"
"""Public path of the generation release cadence, which dates extrapolated generations."""


class GenerationField(StrEnum):
    """A numeric per-generation input field, as published under ``inputs.config.generations[i]``."""

    YEAR_AVAILABLE = "year_available"
    USD_PER_PKG = "usd_per_pkg"
    KW_PER_PKG = "kw_per_pkg"
    KG_PER_PKG = "kg_per_pkg"
    PF_PER_PKG = "pf_per_pkg"
    DIE_COUNT = "die_count"


GENERATION_SLOPE_PATHS: Final[dict[GenerationField, FieldPath]] = {
    GenerationField.USD_PER_PKG: "inputs.config.generation_slopes.usd_growth_per_gen",
    GenerationField.KW_PER_PKG: "inputs.config.generation_slopes.kw_growth_per_gen",
    GenerationField.KG_PER_PKG: "inputs.config.generation_slopes.kg_growth_per_gen",
    GenerationField.PF_PER_PKG: "inputs.config.generation_slopes.pf_growth_per_gen",
}
"""The growth slope each extrapolated per-package value compounds on."""


def generation_path(index: int, field: GenerationField) -> FieldPath:
    """Return the public path of one generation's input field."""
    return f"inputs.config.generations[{index}].{field.value}"


def extrapolation_sources(field: GenerationField, listed_count: int) -> list[FieldPath]:
    """Return the inputs an extrapolated generation's field is derived from.

    The k-th extrapolated generation applies the growth slopes to the
    previous generation's per-package values, step by step from the latest
    listed generation: kW, kg, and PF compound to ``latest x (1 + slope) ** k``
    up to float rounding, while the USD price is truncated to a whole dollar at
    every step (so it can sit a few dollars below that product). It is dated
    ``latest.year_available + k x release_cadence_yr`` and keeps the latest
    listed die count. So every extrapolated field derives from the latest
    listed generation's same field plus its slope or the cadence.

    Args:
        field: The per-generation field.
        listed_count: How many generations the run lists before extrapolation.

    Returns:
        The source input paths, the latest listed field first.
    """
    sources = [generation_path(listed_count - 1, field)]
    if field is GenerationField.YEAR_AVAILABLE:
        sources.append(RELEASE_CADENCE_PATH)
    elif field in GENERATION_SLOPE_PATHS:
        sources.append(GENERATION_SLOPE_PATHS[field])
    return sources


def generation_field_uses(index: int, field: GenerationField, listed_count: int) -> list[FieldPath]:
    """Return what a cell reading one generation's field must cite.

    The generation's own input cell, plus, when the generation is
    extrapolated (``index >= listed_count``), the inputs it is derived from
    (:func:`extrapolation_sources`), so a slope or cadence change reaches every
    cell it moves.

    Args:
        index: The generation's position in the extended list.
        field: The field read.
        listed_count: How many generations the run lists before extrapolation.

    Returns:
        The paths to cite, the generation's own field first.
    """
    uses = [generation_path(index, field)]
    if index >= listed_count:
        uses.extend(extrapolation_sources(field, listed_count))
    return uses


class ScenarioIdentity(BaseModel):
    """Scenario identity for the input manifest."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Human-readable scenario name.")
    description: str = Field(..., description="What the scenario represents.")
    path: str = Field(..., description="Repository-relative source scenario path.")
    is_default: bool = Field(..., description="Whether this is the canonical default scenario.")
    owner_note: str | None = Field(default=None, description="Maintainer note for this scenario.")


class CadenceInputTree(BaseModel):
    """Typed cadence-input cells."""

    model_config = ConfigDict(frozen=True)

    cadence_ceiling: InputCell = Field(..., description="Launch cadence ceiling input.")
    launches_at_year_5: InputCell = Field(..., description="Year-5 launch-count anchor input.")
    launches_at_year_10: InputCell = Field(..., description="Year-10 launch-count anchor input.")
    first_launch_year: InputCell = Field(..., description="First launch model-year input.")


class FleetInputTree(BaseModel):
    """Typed fleet-service-life input cells."""

    model_config = ConfigDict(frozen=True)

    service_life_years: InputCell = Field(..., description="Node service-life input.")


class VolumeInputTree(BaseModel):
    """Typed stowed-volume-envelope input cells."""

    model_config = ConfigDict(frozen=True)

    si_bol_efficiency: InputCell = Field(..., description="Solar-array BOL efficiency input.")
    stowed_pitch_mm: InputCell = Field(..., description="Panel stowed-pitch input.")
    mounting_overhead_pct: InputCell = Field(..., description="Array mounting overhead input.")
    neutron_fairing_usable_volume_m3: InputCell = Field(..., description="Fairing volume input.")


class LaunchInputTree(BaseModel):
    """Typed cadence-indexed launch-cost input cells."""

    model_config = ConfigDict(frozen=True)

    low_cadence_cost_musd: InputCell = Field(..., description="Low-cadence launch cost input.")
    high_cadence_cost_musd: InputCell = Field(..., description="High-cadence launch cost input.")
    low_cadence_launches: InputCell = Field(..., description="Low-cadence launch-count input.")
    high_cadence_launches: InputCell = Field(..., description="High-cadence launch-count input.")


class PhysicalInputTree(BaseModel):
    """Typed physical-envelope and per-node cost input cells."""

    model_config = ConfigDict(frozen=True)

    mass_envelope_t: InputCell = Field(..., description="Payload mass-envelope input.")
    node_mass_fixed_t: InputCell = Field(..., description="Fixed node mass input.")
    node_volume_fixed_m3: InputCell = Field(..., description="Fixed node stowed-volume input.")
    tjmax_lift_year: InputCell = Field(..., description="Radiator hot-loop arrival input.")
    radiator_t_per_kw_pre: InputCell = Field(..., description="Pre-hot-loop radiator mass input.")
    radiator_t_per_kw_post: InputCell = Field(..., description="Post-hot-loop radiator mass input.")
    solar_mass_t_per_kw: InputCell = Field(..., description="Solar mass per kW input.")
    bus_base_musd: InputCell = Field(..., description="Year-zero bus cost input.")
    bus_flatten_after_yr: InputCell = Field(..., description="Bus-cost flattening year input.")
    bus_growth_pre: InputCell = Field(..., description="Pre-flattening bus-cost trend input.")
    solar_cost_musd_per_kw: InputCell = Field(..., description="Solar cost per kW input.")
    radiator_cost_musd_per_kw: InputCell = Field(..., description="Radiator cost per kW input.")
    release_cadence_yr: InputCell = Field(..., description="GPU generation cadence input.")


class RevenueInputTree(BaseModel):
    """Typed revenue-multiple input cells."""

    model_config = ConfigDict(frozen=True)

    central: list[InputCell] = Field(..., description="Central R-band anchor cells.")
    low: list[InputCell] = Field(..., description="Low sensitivity R-band anchor cells.")
    high: list[InputCell] = Field(..., description="High sensitivity R-band anchor cells.")


class GenerationSlopesInputTree(BaseModel):
    """Typed post-Feynman generation-slope input cells."""

    model_config = ConfigDict(frozen=True)

    usd_growth_per_gen: InputCell = Field(..., description="Cost growth per generation input.")
    kw_growth_per_gen: InputCell = Field(..., description="Power growth per generation input.")
    kg_growth_per_gen: InputCell = Field(..., description="Mass growth per generation input.")
    pf_growth_per_gen: InputCell = Field(..., description="Compute growth per generation input.")


class GenerationInputTree(BaseModel):
    """Typed input cells for one GPU package generation."""

    model_config = ConfigDict(frozen=True)

    name: InputCell = Field(..., description="Generation name input.")
    year_available: InputCell = Field(..., description="Generation availability-year input.")
    usd_per_pkg: InputCell = Field(..., description="Generation package-cost input.")
    kw_per_pkg: InputCell = Field(..., description="Generation package-power input.")
    kg_per_pkg: InputCell = Field(..., description="Generation package-mass input.")
    pf_per_pkg: InputCell = Field(..., description="Generation package-compute input.")
    die_count: InputCell = Field(..., description="Generation die-count input.")


class MarketSanityInputTree(BaseModel):
    """Validation-only market-reference inputs."""

    model_config = ConfigDict(frozen=True)

    reference_capacity_gw: InputCell = Field(
        ...,
        description="Mid-2030s AI data-center capacity sanity-check input.",
    )


class TypedInputTree(BaseModel):
    """Nested typed mirror of all known scenario input blocks."""

    model_config = ConfigDict(frozen=True)

    cadence: CadenceInputTree = Field(..., description="Launch cadence inputs.")
    fleet: FleetInputTree = Field(..., description="Fleet/service-life inputs.")
    volume: VolumeInputTree = Field(..., description="Stowed volume-envelope inputs.")
    launch: LaunchInputTree = Field(..., description="Launch-cost inputs.")
    physical: PhysicalInputTree = Field(..., description="Physical-envelope and cost inputs.")
    revenue: RevenueInputTree = Field(..., description="Revenue-multiple inputs.")
    generation_slopes: GenerationSlopesInputTree = Field(
        ...,
        description="Post-Feynman generation-slope inputs.",
    )
    generations: list[GenerationInputTree] = Field(
        ..., description="GPU package generation inputs."
    )
    market_sanity_check: MarketSanityInputTree = Field(
        ...,
        description="Validation-only market sanity-check inputs.",
    )


class InputManifest(BaseModel):
    """Complete typed input object for the space-model JSON."""

    model_config = ConfigDict(frozen=True)

    scenario: ScenarioIdentity = Field(..., description="Scenario identity metadata.")
    config: TypedInputTree = Field(..., description="Nested typed input tree.")
    assumption_index: dict[InputPath, InputCell] = Field(
        ...,
        description="Flat path-indexed lookup for all input cells.",
    )


def revenue_anchor_path(band_name: str, fy: int) -> InputPath:
    """Return the public path of one R-band anchor cell.

    The one definition of the anchor-path format,
    ``inputs.config.revenue.<band>.<fiscal year>``: the manifest builds each
    anchor cell's path here and :func:`revenue_anchors` reads the year back
    from it.

    Args:
        band_name: ``central``, ``low``, or ``high``.
        fy: The anchor's fiscal year.

    Returns:
        The anchor cell's stable public path.
    """
    return InputPath(f"{REVENUE_PATH_PREFIX}.{band_name}.{fy}")


def revenue_anchors(cells: list[InputCell]) -> list[YearRValue]:
    """Return one R band's anchors from its input cells, in cell order.

    The R value is the cell's value; the fiscal year is the final segment of
    the cell's path (:func:`revenue_anchor_path`), the only place the typed
    input tree records it.

    Args:
        cells: One band of ``inputs.config.revenue`` (``central``, ``low``,
            or ``high``).

    Returns:
        The band's :class:`~data_center.config.YearRValue` anchors.

    Raises:
        ValueError: If a cell's path is not an R-band anchor path.
    """
    anchors: list[YearRValue] = []
    for anchor_cell in cells:
        prefix, _, fy_text = anchor_cell.path.rpartition(".")
        if not prefix.startswith(f"{REVENUE_PATH_PREFIX}.") or not fy_text.isdigit():
            raise ValueError(f"{anchor_cell.path} is not an R-band anchor path")
        anchors.append(YearRValue(fy=int(fy_text), r=as_float(anchor_cell)))
    return anchors


def generation_source_status(sourcing: SourcingClass) -> SourceStatus:
    """Map a generation's internal sourcing tier to the public source-status taxonomy.

    The one mapping from :class:`data_center.generations.SourcingClass` to
    :class:`SourceStatus`, used by the generation input cells and by
    ``meta.generations_dictionary`` so both publish one vocabulary.

    Args:
        sourcing: The generation's sourcing tier.

    Returns:
        ``certified`` for a sourced fact, ``sourced_estimate`` for an
        estimate, ``extrapolation`` otherwise.
    """
    if sourcing is SourcingClass.FACT:
        return SourceStatus.CERTIFIED
    if sourcing is SourcingClass.ESTIMATE:
        return SourceStatus.SOURCED_ESTIMATE
    return SourceStatus.EXTRAPOLATION


def _source_refs_for_generation(generation: GenerationSpec) -> list[SourceRef]:
    """Build source refs for a generation input cell."""
    if generation.source.sourcing is SourcingClass.FACT:
        claim_id = "GPU-001"
    elif generation.source.sourcing is SourcingClass.ESTIMATE:
        claim_id = "GPU-012"
    else:
        claim_id = "GPU-010"
    return [
        _source_index_ref(claim_id, "Source-status support for this hardware generation."),
        _research_ref(
            generation.source.doc_path,
            "Durable research note for generation values.",
            claim_id=claim_id,
        ),
    ]


def _generation_cell(
    *,
    path: str,
    label: str,
    value: InputValue,
    unit: str | None,
    description: str,
    generation: GenerationSpec,
    derived_from: list[FieldPath] | None,
) -> InputCell:
    """Construct one generation input cell.

    A listed generation's cell is a roadmap input (role ``default``). An
    extrapolated generation's cell is derived, not set (role
    ``derived_input``): it cites each input it is computed from as a
    ``model_derivation`` reference, beside the generation's claim.

    Args:
        path: Public path of the cell.
        label: Short label.
        value: The generation's value for this field.
        unit: Unit string, or ``None`` for text.
        description: Plain-language meaning of the field.
        generation: The generation the cell belongs to.
        derived_from: ``None`` for a listed generation; for an extrapolated
            one, the input paths the value is derived from (empty for the
            generated name).

    Returns:
        A frozen :class:`InputCell`.
    """
    refs = _source_refs_for_generation(generation)
    if derived_from is None:
        return InputCell(
            path=path,
            label=label,
            value=value,
            unit=unit,
            description=description,
            assumption_role=AssumptionRole.DEFAULT,
            source_status=generation_source_status(generation.source.sourcing),
            source_refs=refs,
            rationale=(
                "Listed generation from the run's hardware roadmap (the bundled "
                "list or the scenario's own)."
            ),
            notes=generation.source.quoted_figure,
        )
    derivation_refs = [
        SourceRef(
            ref_type=SourceRefType.MODEL_DERIVATION,
            ref=source,
            claim_id=None,
            note="Input this extrapolated value is derived from.",
        )
        for source in derived_from
    ]
    return InputCell(
        path=path,
        label=label,
        value=value,
        unit=unit,
        description=description,
        assumption_role=AssumptionRole.DERIVED_INPUT,
        source_status=generation_source_status(generation.source.sourcing),
        source_refs=[*refs, *derivation_refs],
        rationale=(
            "Extrapolated generation: the latest listed generation's value compounded "
            "on the configured growth slope (per-package values), or dated on the "
            "release cadence (availability year). Derived by the model, not set by "
            "the scenario."
        ),
        notes=generation.source.quoted_figure,
    )


CADENCE_SPECS: Final[dict[ConfigFieldName, CellSpec]] = {
    "cadence_ceiling": CellSpec(
        label="Cadence ceiling",
        unit="launches/year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-CADENCE-CEILING-150",
        source_note=(
            "Horizon-scoped infrastructure parameter: the launch pads and rocket "
            "production plausibly built within the ten-year window, not a cap on "
            "the system."
        ),
        rationale=(
            "The logistic launch ramp's carrying capacity for the modeled window. "
            "Launches are clamped to it inside the window; a longer-horizon run "
            "must re-set it, since pads and rockets can both be built."
        ),
    ),
    "launches_at_year_5": CellSpec(
        label="Launches at the year-5 anchor",
        unit="launches/year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="NTR-010",
        source_note="Supports the launch-ramp scenario shape.",
        rationale="This anchor shapes the midpoint of the venture-model cadence ramp.",
    ),
    "launches_at_year_10": CellSpec(
        label="Launches at the year-10 anchor",
        unit="launches/year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-CADENCE-90",
        source_note="Public claim for the default year-10 target cadence.",
        rationale=(
            "The year-10 anchor sets the launches, and so the deployed-year cohort, "
            "at the run's anchor year."
        ),
    ),
    "first_launch_year": CellSpec(
        label="First launch year index",
        unit="model year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="NTR-011",
        source_note="Public schedule context for the first-flight model year.",
        rationale="The first launch clamp prevents year-zero deployment before Neutron service.",
    ),
}

FLEET_SPECS: Final[dict[ConfigFieldName, CellSpec]] = {
    "service_life_years": CellSpec(
        label="Service life",
        unit="years",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-SERVICE-LIFE-5Y",
        source_note="Public claim for the default five-year service life.",
        rationale="The default models a hard five-year cohort cliff.",
    )
}

LAUNCH_SPECS: Final[dict[ConfigFieldName, CellSpec]] = {
    "low_cadence_cost_musd": CellSpec(
        label="Low-cadence launch cost",
        unit="MUSD/launch",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="NTR-009",
        source_note="Supports cadence-indexed Neutron cost assumptions.",
        rationale="The launch-cost curve starts at a higher low-cadence cost.",
    ),
    "high_cadence_cost_musd": CellSpec(
        label="High-cadence launch cost",
        unit="MUSD/launch",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-LAUNCH-COST-2036",
        source_note="Public claim for high-cadence launch cost.",
        rationale="The default uses a lower internal cost once cadence is high.",
    ),
    "low_cadence_launches": CellSpec(
        label="Low-cadence anchor",
        unit="launches/year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="NTR-009",
        source_note="Supports the low-cadence cost anchor.",
        rationale="This anchor identifies where the high-cost end of the curve applies.",
    ),
    "high_cadence_launches": CellSpec(
        label="High-cadence anchor",
        unit="launches/year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="NTR-009",
        source_note="Supports the high-cadence cost anchor.",
        rationale="This anchor identifies where the lower steady-state cost applies.",
    ),
}

PHYSICAL_SPECS: Final[dict[ConfigFieldName, CellSpec]] = {
    "mass_envelope_t": CellSpec(
        label="Reusable SSO mass envelope",
        unit="t",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-PAYLOAD-SSO-UPGRADE",
        source_note="Public claim for the block-upgrade SSO payload scenario.",
        rationale="The node packing model is mass-bound to this reusable SSO scenario.",
    ),
    "node_mass_fixed_t": CellSpec(
        label="Fixed node mass",
        unit="t",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.DERIVED_ESTIMATE,
        claim_id="THR-011",
        source_note="Supports flyable node power and mass-envelope assumptions.",
        rationale="Fixed mass accounts for bus, structure, propulsion, and integration overhead.",
    ),
    "node_volume_fixed_m3": CellSpec(
        label="Fixed node volume",
        unit="m3",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.DERIVED_ESTIMATE,
        claim_id="THR-011",
        source_note="Supports node envelope assumptions.",
        rationale="Fixed volume accounts for bus and structure before packed arrays.",
    ),
    "tjmax_lift_year": CellSpec(
        label="Tjmax lift year",
        unit="model year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="THR-003",
        source_note="Supports the hot-loop radiator-improvement assumption.",
        rationale=(
            "The radiator dial switches from the pre-lift to the post-lift value at "
            "this model year (D11). The investor-set default holds the two dials "
            "equal, so the step is inert; it moves the result only in a scenario "
            "with a heavier pre-lift dial."
        ),
    ),
    "radiator_t_per_kw_pre": CellSpec(
        label="Radiator mass before the Tjmax lift",
        unit="t/kW",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-SOLAR-RADIATOR-MASS",
        source_note=("Investor-set deployed double-sided run-hot radiator mass (2026-07-14)."),
        rationale=(
            "Investor-set (2026-07-14): the AI-1-class deployed double-sided radiator "
            "run hot is asserted from day one, so the pre-lift dial equals the "
            "post-lift dial (about 1.65 kg/kW, within 10 percent of AI-1's implied "
            "1.5 kg/kW) and the Tjmax step is inert."
        ),
        notes=(
            "The single-face co-mounted 0.012 to 0.013 t/kW posture is the labeled "
            "conservative exception; V17 enforces its floor when that architecture "
            "is selected."
        ),
    ),
    "radiator_t_per_kw_post": CellSpec(
        label="Radiator mass after the Tjmax lift",
        unit="t/kW",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-SOLAR-RADIATOR-MASS",
        source_note=("Investor-set deployed double-sided run-hot radiator mass (2026-07-14)."),
        rationale=(
            "Investor-set (2026-07-14): the AI-1-class deployed double-sided radiator "
            "run hot, about 1.65 kg/kW. The temperature and architecture win is "
            "booked in this mass dial, never in the cost dials."
        ),
        notes=(
            "The single-face co-mounted 0.012 to 0.013 t/kW posture is the labeled "
            "conservative exception; V17 enforces its floor when that architecture "
            "is selected."
        ),
    ),
    "solar_mass_t_per_kw": CellSpec(
        label="Solar mass per kW",
        unit="t/kW",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-SOLAR-RADIATOR-MASS",
        source_note=(
            "Public claim for the solar-array mass dial (the row covers the radiator "
            "and solar mass dials together)."
        ),
        rationale=(
            "A planning dial inside the deployable-array mass range, not a Rocket Lab "
            "array specification. Solar mass is apportioned per package through node "
            "power; beside the light radiator it is most of the node's dead-weight "
            "support mass, so this dial is a binding feasibility lever."
        ),
        supporting_claims=(
            SupportingClaim(
                claim_id="THR-006",
                note="Supports the deployable solar-array specific-mass range.",
            ),
        ),
    ),
    "bus_base_musd": CellSpec(
        label="Base bus cost",
        unit="MUSD",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-BUS-COST",
        source_note="Public claim for the bus cost dial.",
        rationale=(
            "The bus cost dial gives every node a platform-cost base (vehicle, "
            "avionics, and propulsion; solar and radiator are priced on their own "
            "dials). A cycle-1 estimate with no quote behind it."
        ),
    ),
    "bus_flatten_after_yr": CellSpec(
        label="Bus cost flattening year",
        unit="model year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-BUS-COST",
        source_note="Public claim for the bus cost curve.",
        rationale="The model stops compounding bus-cost decline after the flattening year.",
    ),
    "bus_growth_pre": CellSpec(
        label="Bus cost trend before flattening",
        unit="fraction/year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-BUS-COST",
        source_note="Public claim for the bus cost curve.",
        rationale="This dial applies modest real cost decline before the flattening year.",
    ),
    "solar_cost_musd_per_kw": CellSpec(
        label="Solar cost per kW",
        unit="MUSD/kW",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-SOLAR-RADIATOR-COST",
        source_note="Public claim for solar/radiator cost dials.",
        rationale="The default keeps the solar cost dial explicit pending better sourcing.",
    ),
    "radiator_cost_musd_per_kw": CellSpec(
        label="Radiator cost per kW",
        unit="MUSD/kW",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-SOLAR-RADIATOR-COST",
        source_note="Public claim for solar/radiator cost dials.",
        rationale="The default keeps the radiator cost dial explicit pending better sourcing.",
    ),
    "release_cadence_yr": CellSpec(
        label="GPU generation cadence",
        unit="years/generation",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="GPU-010",
        source_note="Supports the long-run generation cadence projection.",
        rationale="The model extrapolates post-Feynman generations on this cadence.",
    ),
}

VOLUME_SPECS: Final[dict[ConfigFieldName, CellSpec]] = {
    "si_bol_efficiency": CellSpec(
        label="Solar-array BOL efficiency",
        unit="fraction",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.CERTIFIED,
        claim_id="THR-007",
        source_note="Supports solar-array technology relevance.",
        rationale="This efficiency connects node power to required collector area.",
    ),
    "stowed_pitch_mm": CellSpec(
        label="Stowed panel pitch",
        unit="mm",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SOURCED_ESTIMATE,
        claim_id="THR-006",
        source_note="Supports deployable array packaging assumptions.",
        rationale="Panel pitch turns deployed area into stowed volume.",
    ),
    "mounting_overhead_pct": CellSpec(
        label="Mounting overhead",
        unit="fraction",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SOURCED_ESTIMATE,
        claim_id="THR-006",
        source_note="Supports deployable-array packaging overhead.",
        rationale="The volume model reserves margin for yokes, hinges, and deployment hardware.",
    ),
    "neutron_fairing_usable_volume_m3": CellSpec(
        label="Neutron usable fairing volume",
        unit="m3",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-FAIRING-VOLUME-80M3",
        source_note="Public claim for the usable fairing-volume transparency check.",
        rationale=(
            "The volume check compares stowed node volume with usable fairing volume; "
            "volume does not gate node sizing (mass binds). Rocket Lab publishes no "
            "usable fairing volume, so the dial is the low end of the project's "
            "practical-envelope estimate."
        ),
        research_path="research/node_design/node_mass_model.md",
        research_note=(
            "Section 7: the about 80 to 95 m3 practical usable envelope this dial "
            "takes the low end of."
        ),
    ),
}

SLOPE_SPECS: Final[dict[ConfigFieldName, CellSpec]] = {
    "usd_growth_per_gen": CellSpec(
        label="Package cost growth per generation",
        unit="fraction/generation",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.EXTRAPOLATION,
        claim_id="GPU-012",
        source_note="Supports GPU cost trajectory estimates.",
        rationale="Post-Feynman package cost is extrapolated from the hardware roadmap.",
    ),
    "kw_growth_per_gen": CellSpec(
        label="Package power growth per generation",
        unit="fraction/generation",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.EXTRAPOLATION,
        claim_id="GPU-010",
        source_note="Supports long-run package-power projection.",
        rationale="This corrected per-package growth avoids double-counting assembly growth.",
    ),
    "kg_growth_per_gen": CellSpec(
        label="Package mass growth per generation",
        unit="fraction/generation",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.EXTRAPOLATION,
        claim_id="GPU-010",
        source_note="Supports long-run hardware roadmap projection.",
        rationale="The model assumes packaging density improves after Feynman.",
    ),
    "pf_growth_per_gen": CellSpec(
        label="Package compute growth per generation",
        unit="fraction/generation",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.EXTRAPOLATION,
        claim_id="GPU-010",
        source_note="Supports long-run hardware roadmap projection.",
        rationale="Compute growth drives the post-Feynman performance trajectory.",
    ),
}


def _block_cells(
    *,
    prefix: str,
    block: BaseModel,
    default_block: BaseModel,
    specs: dict[ConfigFieldName, CellSpec],
    scenario_path: str,
) -> dict[ConfigFieldName, InputCell]:
    """Build one config block's input cells, marking changed values as overrides.

    Each cell's description is the config field's own description; a value
    that differs from the default block's value is a scenario override
    (:func:`common.input_manifest._spec_cell`).

    Args:
        prefix: Public path prefix of the block, e.g. ``inputs.config.cadence``.
        block: The run's config block (e.g. ``config.cadence``).
        default_block: The same block of the default config.
        specs: Source metadata per field, describing the default values.
        scenario_path: Repository-relative scenario YAML path.

    Returns:
        The block's input cells, keyed by field name.
    """
    return {
        key: _spec_cell(
            f"{prefix}.{key}",
            getattr(block, key),
            getattr(default_block, key),
            _field_description(type(block), key),
            spec,
            scenario_path,
        )
        for key, spec in specs.items()
    }


def _revenue_cells(
    *,
    scenario_path: str,
    band_name: str,
    anchors: list[YearRValue],
    default_anchors: list[YearRValue],
    role: AssumptionRole,
    claim_id: str,
) -> list[InputCell]:
    """Build typed R-band anchor cells for one trajectory.

    An anchor whose year and value match the default band's anchor carries
    the band's claim; any other anchor is a scenario override.

    Args:
        scenario_path: Repository-relative scenario YAML path.
        band_name: ``central``, ``low``, or ``high``.
        anchors: The run's anchors for this band.
        default_anchors: The default config's anchors for this band.
        role: The band's role (the default central band or a sensitivity).
        claim_id: The claim describing the default band's values.

    Returns:
        One input cell per anchor, in anchor order.
    """
    default_by_year = {anchor.fy: anchor.r for anchor in default_anchors}
    cells: list[InputCell] = []
    for anchor in anchors:
        spec = CellSpec(
            label=f"{band_name} R anchor {anchor.fy}",
            unit="ratio",
            role=role,
            source_status=SourceStatus.SCENARIO,
            claim_id=claim_id,
            source_note="Supports the revenue-to-cost multiple trajectory.",
            rationale=(
                "The central R band is the public default; low/high bands are sensitivities."
            ),
            notes="R is revenue divided by annualized cost.",
        )
        cells.append(
            _spec_cell(
                revenue_anchor_path(band_name, anchor.fy),
                anchor.r,
                default_by_year.get(anchor.fy),
                "Revenue-to-cost multiple anchor for one fiscal year.",
                spec,
                scenario_path,
            )
        )
    return cells


def _revenue_tree(
    config: ValuationConfig, default: ValuationConfig, scenario_path: str
) -> RevenueInputTree:
    """Build typed revenue input cells for the three R bands."""
    return RevenueInputTree(
        central=_revenue_cells(
            scenario_path=scenario_path,
            band_name="central",
            anchors=config.r_band.central,
            default_anchors=default.r_band.central,
            role=AssumptionRole.DEFAULT,
            claim_id=CENTRAL_R_CLAIM_ID,
        ),
        low=_revenue_cells(
            scenario_path=scenario_path,
            band_name="low",
            anchors=config.r_band.low,
            default_anchors=default.r_band.low,
            role=AssumptionRole.SENSITIVITY,
            claim_id=SENSITIVITY_R_CLAIM_ID,
        ),
        high=_revenue_cells(
            scenario_path=scenario_path,
            band_name="high",
            anchors=config.r_band.high,
            default_anchors=default.r_band.high,
            role=AssumptionRole.SENSITIVITY,
            claim_id=SENSITIVITY_R_CLAIM_ID,
        ),
    )


def _generation_tree(
    generation: GenerationSpec, index: int, listed_count: int
) -> GenerationInputTree:
    """Build typed input cells for one generation row.

    Args:
        generation: The generation.
        index: Its position in the extended generation list.
        listed_count: How many generations the run lists before
            extrapolation; a row at or past it is extrapolated.

    Returns:
        The row's input cells.
    """
    extrapolated = index >= listed_count

    def field_cell(field: GenerationField, label: str, unit: str) -> InputCell:
        """Build the cell for one numeric field of this generation."""
        return _generation_cell(
            path=generation_path(index, field),
            label=f"{generation.name} {label}",
            value=getattr(generation, field.value),
            unit=unit,
            description=_field_description(GenerationSpec, field.value),
            generation=generation,
            derived_from=extrapolation_sources(field, listed_count) if extrapolated else None,
        )

    return GenerationInputTree(
        name=_generation_cell(
            path=f"inputs.config.generations[{index}].name",
            label=f"{generation.name} name",
            value=generation.name,
            unit=None,
            description=_field_description(GenerationSpec, "name"),
            generation=generation,
            derived_from=[] if extrapolated else None,
        ),
        year_available=field_cell(GenerationField.YEAR_AVAILABLE, "availability year", "year"),
        usd_per_pkg=field_cell(GenerationField.USD_PER_PKG, "package cost", "USD/package"),
        kw_per_pkg=field_cell(GenerationField.KW_PER_PKG, "package power", "kW/package"),
        kg_per_pkg=field_cell(GenerationField.KG_PER_PKG, "package mass", "kg/package"),
        pf_per_pkg=field_cell(GenerationField.PF_PER_PKG, "package compute", "PFLOPS/package"),
        die_count=field_cell(GenerationField.DIE_COUNT, "die count", "dies/package"),
    )


def _market_tree() -> MarketSanityInputTree:
    """Build validation-only market sanity-check inputs."""
    spec = CellSpec(
        label="Mid-2030s AI data-center market reference",
        unit="GW",
        role=AssumptionRole.VALIDATION_ONLY,
        source_status=SourceStatus.PROJECTION,
        claim_id="RLDC-MARKET-100GW-2036",
        source_note="Public market-scale sanity check, not a market-share thesis.",
        rationale="The default deployment is compared against broad external market scale.",
        notes="Used only for scale sanity checking.",
    )
    return MarketSanityInputTree(
        reference_capacity_gw=_cell(
            "inputs.config.market_sanity_check.reference_capacity_gw",
            MARKET_REFERENCE_CAPACITY_GW,
            "Order-of-magnitude AI data-center capacity reference for sanity checking.",
            spec,
        )
    )


def collect_input_cells(node: BaseModel | list[BaseModel]) -> list[InputCell]:
    """Collect every ``InputCell`` leaf from a typed input tree, in field order.

    A field holds either one cell, a nested tree, or a list whose items are
    cells (the R-band anchors) or nested trees (the generations). A list item
    that is itself an ``InputCell`` is a leaf and is collected as is; only
    non-cell models are walked further.

    Args:
        node: A typed input tree, or a list of cells or trees.

    Returns:
        Every input cell under ``node``, in declaration order.
    """
    if isinstance(node, InputCell):
        return [node]
    cells: list[InputCell] = []
    if isinstance(node, list):
        for item in node:
            cells.extend(collect_input_cells(item))
        return cells
    for value in node.__dict__.values():
        if isinstance(value, (BaseModel, list)):
            cells.extend(collect_input_cells(value))
    return cells


def is_default_scenario(source_scenario_path: str) -> bool:
    """Return whether a run's scenario is the canonical default.

    The one predicate behind ``inputs.scenario.is_default`` and the promotion
    rules of ``rklb-value --promote``: a scenario is the default exactly when
    its repository-relative path is :data:`DEFAULT_SCENARIO_PATH`.

    Args:
        source_scenario_path: The run's repository-relative scenario path.

    Returns:
        True for ``code/scenarios/default.yaml``, else False.
    """
    return source_scenario_path == DEFAULT_SCENARIO_PATH


def build_input_manifest(
    *,
    config: ValuationConfig,
    extended_gens: list[GenerationSpec],
    source_scenario_path: str,
) -> InputManifest:
    """Build the complete typed input manifest for a space-model run.

    Every scenario-valued cell is compared with the default config's value at
    the same path; a changed value is published as a scenario override
    without the default's claim, rationale, or role. Generation rows past the
    listed roadmap (``config.listed_generations()``) are extrapolated: their
    cells are ``derived_input`` and cite the slopes, cadence, and latest
    listed values they are computed from.

    Args:
        config: Validated scenario config used by the model run.
        extended_gens: Hardware generation list after extrapolation to horizon.
        source_scenario_path: Repository-relative source scenario path.

    Returns:
        A frozen :class:`InputManifest` with nested config cells and a flat
        assumption index keyed by stable public paths.
    """
    is_default = is_default_scenario(source_scenario_path)
    default = ValuationConfig()
    listed_count = len(config.listed_generations())

    def block(
        prefix: str,
        run_block: BaseModel,
        default_block: BaseModel,
        specs: dict[ConfigFieldName, CellSpec],
    ) -> dict[ConfigFieldName, InputCell]:
        """Build one block's cells against its default block."""
        return _block_cells(
            prefix=prefix,
            block=run_block,
            default_block=default_block,
            specs=specs,
            scenario_path=source_scenario_path,
        )

    config_tree = TypedInputTree(
        cadence=CadenceInputTree(
            **block("inputs.config.cadence", config.cadence, default.cadence, CADENCE_SPECS)
        ),
        fleet=FleetInputTree(
            **block("inputs.config.fleet", config.fleet, default.fleet, FLEET_SPECS)
        ),
        volume=VolumeInputTree(
            **block("inputs.config.volume", config.volume, default.volume, VOLUME_SPECS)
        ),
        launch=LaunchInputTree(
            **block("inputs.config.launch", config.launch_cost, default.launch_cost, LAUNCH_SPECS)
        ),
        physical=PhysicalInputTree(
            **block("inputs.config.physical", config.gospel, default.gospel, PHYSICAL_SPECS)
        ),
        revenue=_revenue_tree(config, default, source_scenario_path),
        generation_slopes=GenerationSlopesInputTree(
            **block("inputs.config.generation_slopes", config.slopes, default.slopes, SLOPE_SPECS)
        ),
        generations=[
            _generation_tree(generation, index, listed_count)
            for index, generation in enumerate(extended_gens)
        ],
        market_sanity_check=_market_tree(),
    )
    cells = collect_input_cells(config_tree)
    assumption_index = {InputPath(cell.path): cell for cell in cells}
    scenario = ScenarioIdentity(
        name=config.scenario_name,
        description=(
            "Canonical default orbital AI-inference data-center scenario."
            if is_default
            else "User-supplied orbital AI-inference data-center scenario."
        ),
        path=source_scenario_path,
        is_default=is_default,
        owner_note="Investor-selected default assumption set." if is_default else None,
    )
    return InputManifest(scenario=scenario, config=config_tree, assumption_index=assumption_index)


__all__ = [
    "DEFAULT_SCENARIO_PATH",
    "InputManifest",
    "ScenarioIdentity",
    "TypedInputTree",
    "build_input_manifest",
    "GenerationField",
    "collect_input_cells",
    "extrapolation_sources",
    "generation_field_uses",
    "generation_path",
    "generation_source_status",
    "is_default_scenario",
    "revenue_anchor_path",
    "revenue_anchors",
]
