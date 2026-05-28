"""Typed ground reference model for the public data-center comparison.

The ground reference model compares one terrestrial five-year data-center
cohort against the promoted space model's 2036 deployed-year cohort. It is a
small deep module: callers provide a typed :class:`SpaceModelOutput`, a typed
ground-assumption config, and a source catalog; this module owns the anchor
selection, input manifest, cost arithmetic, warnings, and output contract.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Final  # typing-acceptable: Any types the YAML boundary

import yaml
from pydantic import BaseModel, ConfigDict, Field

from data_center.input_manifest import (
    AssumptionRole,
    InputCell,
    InputPath,
    InputScalar,
    ScenarioIdentity,
    SourceRef,
    SourceRefType,
    SourceStatus,
)
from data_center.output import (
    DataDictEntry,
    QueryAppliesTo,
    QueryExample,
    RunMetadata,
    SourceStatusSummary,
    SpaceModelOutput,
    ValidationResult,
    ValidationSeverity,
)
from data_center.provenance import FieldPath, ProvenanceCell, cell

logger = logging.getLogger(__name__)

GROUND_SCHEMA_VERSION: Final[str] = "ground-v1"
"""Public schema version for the ground reference artifact."""

DEFAULT_GROUND_SCENARIO_PATH: Final[str] = "code/scenarios/ground_default.yaml"
"""Repository-relative location of the default ground assumptions."""

SPACE_MODEL_DEFAULT_PATH: Final[str] = "data_center/models/space/default.json"
"""Public promoted space model used by the default ground reference."""

ANCHOR_YEAR: Final[int] = 2036
"""Canonical comparison year: the default deployed-year cohort."""

ANCHOR_YEAR_KEY: Final[str] = str(ANCHOR_YEAR)
"""JSON object key for the canonical comparison year."""

ANCHOR_BASIS: Final[str] = "deployed_this_year"
"""Ground comparison basis; deliberately not the living fleet."""

ANCHOR_NOTE: Final[str] = "Annual deployment cohort, not living fleet market share."
"""Plain-language warning attached to the anchor."""

GROUND_COST_BASIS_CLAIM_ID: Final[str] = "RLDC-GROUND-COST-BASIS"
"""SOURCE_INDEX claim covering the overall ground-cost basis."""

GROUND_COST_RESEARCH_PATH: Final[str] = (
    "research/economics/ground_infrastructure_electricity_costs_2036.md"
)
"""Research note containing the current ground infrastructure cost basis."""

SOURCE_INDEX_PATH: Final[str] = "research/SOURCE_INDEX.md"
"""Public source ledger used by all promoted input cells."""

GROUND_GPU_PACKAGE_COST_BOUNDARY_CLAIM_ID: Final[str] = "RLDC-GROUND-GPU-PACKAGE-COST-BOUNDARY"
"""SOURCE_INDEX claim for the ground GPU package comparison boundary."""

GROUND_FACILITY_FITOUT_CLAIM_ID: Final[str] = "RLDC-GROUND-FACILITY-FITOUT-18M-MW"
"""SOURCE_INDEX claim for facility shell and fit-out cost."""

GROUND_RACKED_POWER_NETWORK_CLAIM_ID: Final[str] = "RLDC-GROUND-RACKED-POWER-NETWORK-80K-PACKAGE"
"""SOURCE_INDEX claim for racked power and networking cost."""

GROUND_ENERGY_PRICE_CLAIM_ID: Final[str] = "RLDC-GROUND-ENERGY-PRICE-85-MWH"
"""SOURCE_INDEX claim for delivered electricity price."""

GROUND_PUE_CLAIM_ID: Final[str] = "RLDC-GROUND-PUE-1_25"
"""SOURCE_INDEX claim for PUE."""

GROUND_UTILIZATION_CLAIM_ID: Final[str] = "RLDC-GROUND-UTILIZATION-0_85"
"""SOURCE_INDEX claim for utilization."""

GROUND_OPERATIONS_MAINTENANCE_CLAIM_ID: Final[str] = "RLDC-GROUND-O_AND_M-1_5M-MW-YR"
"""SOURCE_INDEX claim for operations, maintenance, and labor."""

GROUND_COOLING_CLAIM_ID: Final[str] = "RLDC-GROUND-COOLING-4M-MW"
"""SOURCE_INDEX claim for cooling infrastructure."""

GROUND_COMPARISON_PERIOD_CLAIM_ID: Final[str] = "RLDC-GROUND-COMPARISON-PERIOD-5Y"
"""SOURCE_INDEX claim for the five-year comparison period."""

DEFAULT_GPU_PACKAGE_COST_MULTIPLIER: Final[float] = 1.0
"""Ground GPU package cost multiplier; `1.0` means same package cost as space."""

DEFAULT_FACILITY_SHELL_FITOUT_MUSD_PER_MW: Final[float] = 18.0
"""Source-linked facility shell / fit-out allocation per MW."""

DEFAULT_RACKED_POWER_NETWORK_MUSD_PER_GPU_PACKAGE: Final[float] = 0.08
"""Scenario racked-power and networking allocation per GPU package."""

DEFAULT_ENERGY_PRICE_USD_PER_MWH: Final[float] = 85.0
"""Source-linked delivered electricity price in USD per MWh."""

DEFAULT_PUE: Final[float] = 1.25
"""Scenario power-usage-effectiveness assumption for AI data-center load."""

DEFAULT_UTILIZATION: Final[float] = 0.85
"""Scenario average IT-load utilization over the comparison window."""

DEFAULT_OPERATIONS_MAINTENANCE_MUSD_PER_MW_YEAR: Final[float] = 1.5
"""Scenario annual operations, maintenance, and labor allocation per MW."""

DEFAULT_COOLING_COST_MUSD_PER_MW: Final[float] = 4.0
"""Scenario liquid-cooling infrastructure allocation per MW."""

DEFAULT_COMPARISON_PERIOD_YEARS: Final[int] = 5
"""Default comparison window, aligned to the space model service life."""

ZERO_COUNT: Final[int] = 0
"""Initial counter value for source-status summaries."""

ONE_COUNT: Final[int] = 1
"""Counter increment for one input cell."""

ZERO_COST: Final[float] = 0.0
"""Zero-cost component value used for explicit exclusions and safe ratios."""

KW_PER_MW: Final[float] = 1_000.0
"""Unit conversion from kW to MW."""

KWH_PER_MWH: Final[float] = 1_000.0
"""Unit conversion from kWh to MWh."""

MUSD_PER_USD: Final[float] = 1_000_000.0
"""Unit conversion from USD to million USD."""

HOURS_PER_DAY: Final[float] = 24.0
"""Clock hours in one day."""

DAYS_PER_YEAR: Final[float] = 365.0
"""Model year length for order-of-magnitude energy cost."""

HOURS_PER_YEAR: Final[float] = HOURS_PER_DAY * DAYS_PER_YEAR
"""Clock hours in one model year."""

GROUND_MATERIALLY_CHEAPER_RATIO: Final[float] = 0.5
"""Ground/orbit ratio below which ground is materially cheaper."""

ORBITAL_MATERIALLY_CHEAPER_RATIO: Final[float] = 2.0
"""Ground/orbit ratio above which orbital is materially cheaper."""


class GroundConclusionLabel(StrEnum):
    """Plain-language conclusion labels for the comparison block."""

    SAME_ORDER = "same_order_of_magnitude"
    GROUND_CHEAPER = "ground_materially_cheaper"
    ORBITAL_CHEAPER = "orbital_materially_cheaper"


class GroundReferenceConfig(BaseModel):
    """Validated ground-reference assumptions loaded from YAML."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    scenario_name: str = Field(
        default="Default ground reference scenario",
        description="Human-readable label for the ground reference assumption set.",
    )
    gpu_package_cost_multiplier: float = Field(
        default=DEFAULT_GPU_PACKAGE_COST_MULTIPLIER,
        gt=ZERO_COST,
        description="Multiplier applied to the space model's 2036 package cost.",
    )
    facility_shell_fitout_musd_per_mw: float = Field(
        default=DEFAULT_FACILITY_SHELL_FITOUT_MUSD_PER_MW,
        ge=ZERO_COST,
        description="Five-year facility shell and fit-out allocation per MW.",
    )
    racked_power_network_musd_per_gpu_package: float = Field(
        default=DEFAULT_RACKED_POWER_NETWORK_MUSD_PER_GPU_PACKAGE,
        ge=ZERO_COST,
        description="Racked power and networking allocation per GPU package.",
    )
    energy_price_usd_per_mwh: float = Field(
        default=DEFAULT_ENERGY_PRICE_USD_PER_MWH,
        ge=ZERO_COST,
        description="Delivered electricity price for the ground cohort.",
    )
    pue: float = Field(
        default=DEFAULT_PUE,
        gt=ZERO_COST,
        description="Power usage effectiveness applied to IT load.",
    )
    utilization: float = Field(
        default=DEFAULT_UTILIZATION,
        ge=ZERO_COST,
        le=DEFAULT_GPU_PACKAGE_COST_MULTIPLIER,
        description="Average IT-load utilization during the comparison period.",
    )
    operations_maintenance_musd_per_mw_year: float = Field(
        default=DEFAULT_OPERATIONS_MAINTENANCE_MUSD_PER_MW_YEAR,
        ge=ZERO_COST,
        description="Annual operations, maintenance, and labor allocation per MW.",
    )
    cooling_cost_musd_per_mw: float = Field(
        default=DEFAULT_COOLING_COST_MUSD_PER_MW,
        ge=ZERO_COST,
        description="Cooling infrastructure allocation per MW.",
    )
    comparison_period_years: int = Field(
        default=DEFAULT_COMPARISON_PERIOD_YEARS,
        gt=ZERO_COUNT,
        description="Five-year comparison period aligned to service life.",
    )


class SourceCatalog(BaseModel):
    """Public source references used by the ground reference input cells."""

    model_config = ConfigDict(frozen=True)

    source_index_path: str = Field(..., description="Repository-relative SOURCE_INDEX path.")
    ground_cost_basis_claim_id: str = Field(
        ..., description="SOURCE_INDEX claim ID for ground-cost basis."
    )
    ground_cost_research_path: str = Field(
        ..., description="Research note supporting the ground-cost framing."
    )


class GroundAssumptionInputTree(BaseModel):
    """Typed ground-reference assumption cells."""

    model_config = ConfigDict(frozen=True)

    gpu_package_cost_multiplier: InputCell = Field(
        ..., description="GPU package cost-basis multiplier."
    )
    facility_shell_fitout_musd_per_mw: InputCell = Field(
        ..., description="Facility shell / fit-out allocation input."
    )
    racked_power_network_musd_per_gpu_package: InputCell = Field(
        ..., description="Racked power and networking allocation input."
    )
    energy_price_usd_per_mwh: InputCell = Field(..., description="Energy-price input.")
    pue: InputCell = Field(..., description="Power-usage-effectiveness input.")
    utilization: InputCell = Field(..., description="Average utilization input.")
    operations_maintenance_musd_per_mw_year: InputCell = Field(
        ..., description="Operations, maintenance, and labor input."
    )
    cooling_cost_musd_per_mw: InputCell = Field(..., description="Cooling cost input.")
    comparison_period_years: InputCell = Field(..., description="Comparison-window input.")


class GroundInputManifest(BaseModel):
    """Complete typed input manifest for the ground reference artifact."""

    model_config = ConfigDict(frozen=True)

    scenario: ScenarioIdentity = Field(..., description="Ground scenario identity metadata.")
    config: GroundAssumptionInputTree = Field(..., description="Ground assumption cells.")
    assumption_index: dict[InputPath, InputCell] = Field(
        ..., description="Flat path-indexed lookup for all ground input cells."
    )


class GroundComparisonAnchor(BaseModel):
    """The deployed-year cohort selected from the promoted space model."""

    model_config = ConfigDict(frozen=True)

    space_model_path: str = Field(..., description="Promoted space model path.")
    year: int = Field(..., description="Anchor year.")
    basis: str = Field(..., description="Anchor basis.")
    nodes: int | float = Field(..., description="Nodes deployed in the anchor year.")
    gpu_packages: int | float = Field(..., description="GPU packages in the anchor cohort.")
    kw: int | float = Field(..., description="Anchor cohort IT load, kW.")
    service_life_years: int | float = Field(..., description="Space model service life.")
    note: str = Field(..., description="Plain-language anchor note.")
    source_paths: list[str] = Field(..., description="Space-model paths used for the anchor.")


class CostComponent(BaseModel):
    """One cost line in a ground or orbital reference result."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Stable component key.")
    label: str = Field(..., description="Human-readable component label.")
    cost: ProvenanceCell = Field(..., description="Five-year cost for this component.")
    included: bool = Field(..., description="Whether this component is included in totals.")
    source_paths: list[str] = Field(..., description="Source JSON paths or input cells.")
    notes: str | None = Field(default=None, description="Component caveat or treatment note.")


class GroundCostResult(BaseModel):
    """Ground-side cost result for the selected deployed-year cohort."""

    model_config = ConfigDict(frozen=True)

    component_costs: list[CostComponent] = Field(..., description="Ground cost components.")
    total_five_year_cost: ProvenanceCell = Field(..., description="Total five-year ground cost.")
    annualized_cost: ProvenanceCell = Field(..., description="Annualized ground cost.")
    cost_per_gpu_package_five_year: ProvenanceCell = Field(
        ..., description="Five-year ground cost per GPU package."
    )
    cost_per_mw_five_year: ProvenanceCell = Field(..., description="Five-year ground cost per MW.")
    included_components: list[str] = Field(..., description="Explicitly included components.")
    excluded_components: list[str] = Field(..., description="Explicitly excluded components.")
    source_status_summary: dict[str, int] = Field(
        ..., description="Counts of ground input assumptions by source-status."
    )
    warnings: list[ValidationResult] = Field(..., description="Ground-side warnings.")


class OrbitalReferenceResult(BaseModel):
    """Space-model build/launch reference for the same deployed-year cohort."""

    model_config = ConfigDict(frozen=True)

    component_costs: list[CostComponent] = Field(..., description="Orbital cost components.")
    total_build_and_launch_cost: ProvenanceCell = Field(
        ..., description="Total build and launch cost for the anchor cohort."
    )
    five_year_cost_view: ProvenanceCell = Field(
        ..., description="Five-year comparable orbital cost view."
    )
    cost_per_gpu_package_five_year: ProvenanceCell = Field(
        ..., description="Five-year orbital cost per GPU package."
    )
    cost_per_mw_five_year: ProvenanceCell = Field(..., description="Five-year orbital cost per MW.")
    kw: ProvenanceCell = Field(..., description="Anchor cohort kW.")
    gpu_packages: ProvenanceCell = Field(..., description="Anchor cohort GPU packages.")
    explicit_exclusions: list[str] = Field(..., description="Orbital exclusions.")
    warnings: list[ValidationResult] = Field(..., description="Orbital-reference warnings.")


class ComponentDelta(BaseModel):
    """One grouped component comparison between ground and orbital costs."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Stable component-delta key.")
    ground_cost: ProvenanceCell = Field(..., description="Ground cost for this group.")
    orbital_reference_cost: ProvenanceCell = Field(
        ..., description="Orbital reference cost for this group."
    )
    absolute_delta: ProvenanceCell = Field(
        ..., description="Ground minus orbital cost for this group."
    )
    ground_to_orbit_ratio: ProvenanceCell = Field(
        ..., description="Ground cost divided by orbital cost for this group."
    )
    notes: str = Field(..., description="How this grouping should be interpreted.")


class GroundSpaceComparison(BaseModel):
    """Direct comparison between ground and orbital five-year cost views."""

    model_config = ConfigDict(frozen=True)

    ground_total_five_year_cost: ProvenanceCell = Field(
        ..., description="Ground total five-year cost."
    )
    orbital_total_five_year_cost: ProvenanceCell = Field(
        ..., description="Orbital total five-year reference cost."
    )
    absolute_delta: ProvenanceCell = Field(..., description="Ground minus orbital total.")
    ground_to_orbit_ratio: ProvenanceCell = Field(..., description="Ground/orbit total ratio.")
    orbit_to_ground_ratio: ProvenanceCell = Field(..., description="Orbit/ground total ratio.")
    cost_per_gpu_package_delta: ProvenanceCell = Field(
        ..., description="Ground minus orbital cost per GPU package."
    )
    cost_per_mw_delta: ProvenanceCell = Field(..., description="Ground minus orbital cost per MW.")
    component_deltas: list[ComponentDelta] = Field(
        ..., description="Grouped component-level deltas."
    )
    conclusion_label: str = Field(..., description="Plain-language conclusion label.")
    warnings: list[ValidationResult] = Field(..., description="Comparison warnings.")


class GroundOutputMetadata(BaseModel):
    """Metadata that helps cold readers query and validate the ground output."""

    model_config = ConfigDict(frozen=True)

    data_dictionary: list[DataDictEntry] = Field(
        ..., description="Compact descriptions of important ground output paths."
    )
    validation_results: list[ValidationResult] = Field(
        ..., description="Public pass/warn/fail validation entries."
    )
    query_examples: list[QueryExample] = Field(
        ..., description="Worked jq queries for the ground reference output."
    )
    source_status_summary: SourceStatusSummary = Field(
        ..., description="Count of ground input assumptions by source-status value."
    )
    schema_version_notes: str = Field(..., description="Human-readable schema notes.")


class GroundReferenceOutput(BaseModel):
    """Complete typed ground reference artifact."""

    model_config = ConfigDict(frozen=True)

    metadata: RunMetadata = Field(..., description="Run identity for the ground artifact.")
    anchor: GroundComparisonAnchor = Field(..., description="2036 deployed-year anchor.")
    inputs: GroundInputManifest = Field(..., description="Ground assumption manifest.")
    ground: GroundCostResult = Field(..., description="Ground cost result.")
    orbital_reference: OrbitalReferenceResult = Field(
        ..., description="Comparable orbital reference result."
    )
    comparison: GroundSpaceComparison = Field(..., description="Ground/orbit comparison.")
    meta: GroundOutputMetadata = Field(..., description="Cold-reader metadata.")


@dataclass(frozen=True)
class GroundInputSpec:
    """Metadata needed to construct one ground input cell."""

    label: str
    unit: str | None
    description: str
    rationale: str
    claim_id: str
    source_status: SourceStatus
    notes: str | None = None


GROUND_INPUT_SPECS: Final[dict[str, GroundInputSpec]] = {
    "gpu_package_cost_multiplier": GroundInputSpec(
        label="GPU package cost multiplier",
        unit="ratio",
        description="Multiplier applied to the space model's 2036 package acquisition cost.",
        rationale="Uses the same GPU package cost basis as the orbital cohort.",
        claim_id=GROUND_GPU_PACKAGE_COST_BOUNDARY_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
        notes="A value of 1.0 means ground and orbital compute hardware share the same price.",
    ),
    "facility_shell_fitout_musd_per_mw": GroundInputSpec(
        label="Facility shell and fit-out",
        unit="MUSD/MW",
        description="Five-year facility shell and fit-out allocation per MW.",
        rationale="Captures terrestrial building and AI-hall fit-out costs.",
        claim_id=GROUND_FACILITY_FITOUT_CLAIM_ID,
        source_status=SourceStatus.SOURCED_ESTIMATE,
    ),
    "racked_power_network_musd_per_gpu_package": GroundInputSpec(
        label="Racked power and networking",
        unit="MUSD/package",
        description="Power distribution and networking allocation per GPU package.",
        rationale="Captures non-GPU rack-side electrical and network integration.",
        claim_id=GROUND_RACKED_POWER_NETWORK_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
    ),
    "energy_price_usd_per_mwh": GroundInputSpec(
        label="Energy price",
        unit="USD/MWh",
        description="Delivered electricity price for the ground cohort.",
        rationale="Turns IT load, PUE, and utilization into a five-year energy cost.",
        claim_id=GROUND_ENERGY_PRICE_CLAIM_ID,
        source_status=SourceStatus.SOURCED_ESTIMATE,
    ),
    "pue": GroundInputSpec(
        label="PUE",
        unit="ratio",
        description="Power usage effectiveness for total facility draw.",
        rationale="Converts IT load into total facility electricity consumption.",
        claim_id=GROUND_PUE_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
    ),
    "utilization": GroundInputSpec(
        label="Utilization",
        unit="fraction",
        description="Average IT-load utilization during the comparison window.",
        rationale="Energy cost scales with the average utilized IT load.",
        claim_id=GROUND_UTILIZATION_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
    ),
    "operations_maintenance_musd_per_mw_year": GroundInputSpec(
        label="Operations, maintenance, and labor",
        unit="MUSD/MW-year",
        description="Annual operations, maintenance, and labor allocation per MW.",
        rationale="Keeps recurring terrestrial support cost explicit.",
        claim_id=GROUND_OPERATIONS_MAINTENANCE_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
        notes="Labor is represented in this line rather than as a separate cost component.",
    ),
    "cooling_cost_musd_per_mw": GroundInputSpec(
        label="Cooling infrastructure",
        unit="MUSD/MW",
        description="Cooling infrastructure allocation per MW.",
        rationale="Represents liquid-cooling and heat-rejection infrastructure.",
        claim_id=GROUND_COOLING_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
    ),
    "comparison_period_years": GroundInputSpec(
        label="Comparison period",
        unit="years",
        description="Cost comparison window.",
        rationale="Aligns the terrestrial comparison to the orbital service-life view.",
        claim_id=GROUND_COMPARISON_PERIOD_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
    ),
}


def default_ground_source_catalog() -> SourceCatalog:
    """Return the default public source catalog for ground assumptions."""
    return SourceCatalog(
        source_index_path=SOURCE_INDEX_PATH,
        ground_cost_basis_claim_id=GROUND_COST_BASIS_CLAIM_ID,
        ground_cost_research_path=GROUND_COST_RESEARCH_PATH,
    )


def ground_config_from_dict(data: dict[str, Any]) -> GroundReferenceConfig:
    """Build a :class:`GroundReferenceConfig` from parsed YAML data.

    Args:
        data: YAML mapping parsed from a ground-reference scenario file.

    Returns:
        A frozen ground-reference config.

    Raises:
        ValueError: If the YAML root is not a mapping.
    """
    if not isinstance(data, dict):
        raise ValueError("ground config root must be a mapping (a YAML object)")
    return GroundReferenceConfig.model_validate(data)


def load_ground_config(path: str | Path) -> GroundReferenceConfig:
    """Load and validate ground-reference assumptions from YAML.

    Args:
        path: Filesystem path to the ground-reference YAML scenario.

    Returns:
        A validated :class:`GroundReferenceConfig`.

    Raises:
        FileNotFoundError: If ``path`` is absent.
        ValueError: If YAML parsing or validation fails.
    """
    config_path = Path(path)
    if not config_path.is_file():
        raise FileNotFoundError(f"ground config file not found: {config_path}")
    try:
        data = yaml.safe_load(config_path.read_text())
    except yaml.YAMLError as exc:
        raise ValueError(f"could not parse YAML config {config_path}: {exc}") from exc
    if data is None:
        return _default_ground_config()
    if not isinstance(data, dict):
        raise ValueError(
            f"ground config file {config_path} must contain a YAML mapping "
            f"(got {type(data).__name__})"
        )
    return ground_config_from_dict(data)


def build_ground_reference_output(
    space_output: SpaceModelOutput,
    ground_config: GroundReferenceConfig,
    source_catalog: SourceCatalog,
) -> GroundReferenceOutput:
    """Build the complete ground reference output for one space-model run.

    Args:
        space_output: Typed space model output that supplies the 2036 cohort.
        ground_config: Validated ground-reference assumptions.
        source_catalog: Public source references for ground input cells.

    Returns:
        A frozen :class:`GroundReferenceOutput` ready for JSON serialization.
    """
    inputs = _build_ground_input_manifest(
        ground_config=ground_config,
        source_catalog=source_catalog,
        source_scenario_path=DEFAULT_GROUND_SCENARIO_PATH,
    )
    anchor = _build_anchor(space_output)
    ground = _build_ground_cost_result(anchor, space_output, inputs)
    orbital_reference = _build_orbital_reference_result(anchor, space_output)
    comparison_warnings = [
        *_comparison_scope_warnings(),
        *orbital_reference.warnings,
    ]
    comparison = _build_comparison(
        ground=ground,
        orbital_reference=orbital_reference,
        warnings=comparison_warnings,
    )
    validation_results = [
        *_anchor_validation_results(anchor),
        *orbital_reference.warnings,
        *_comparison_scope_warnings(),
    ]
    metadata = _build_ground_metadata(space_output.metadata, ground_config)
    meta = GroundOutputMetadata(
        data_dictionary=_ground_data_dictionary(),
        validation_results=validation_results,
        query_examples=_ground_query_examples(),
        source_status_summary=_source_status_summary_model(inputs),
        schema_version_notes=(
            "ground-v1 reference output anchored to the 2036 deployed-year "
            "space-model cohort; ground assumptions are source-status tagged "
            "through the research wiki source ledger."
        ),
    )
    return GroundReferenceOutput(
        metadata=metadata,
        anchor=anchor,
        inputs=inputs,
        ground=ground,
        orbital_reference=orbital_reference,
        comparison=comparison,
        meta=meta,
    )


def render_ground_json(output: GroundReferenceOutput) -> str:
    """Serialize a :class:`GroundReferenceOutput` as indented JSON."""
    return output.model_dump_json(indent=2)


def _default_ground_config() -> GroundReferenceConfig:
    """Build the fully named default config for mypy-strict Pydantic calls."""
    return GroundReferenceConfig(
        scenario_name="Default ground reference scenario",
        gpu_package_cost_multiplier=DEFAULT_GPU_PACKAGE_COST_MULTIPLIER,
        facility_shell_fitout_musd_per_mw=DEFAULT_FACILITY_SHELL_FITOUT_MUSD_PER_MW,
        racked_power_network_musd_per_gpu_package=(
            DEFAULT_RACKED_POWER_NETWORK_MUSD_PER_GPU_PACKAGE
        ),
        energy_price_usd_per_mwh=DEFAULT_ENERGY_PRICE_USD_PER_MWH,
        pue=DEFAULT_PUE,
        utilization=DEFAULT_UTILIZATION,
        operations_maintenance_musd_per_mw_year=(DEFAULT_OPERATIONS_MAINTENANCE_MUSD_PER_MW_YEAR),
        cooling_cost_musd_per_mw=DEFAULT_COOLING_COST_MUSD_PER_MW,
        comparison_period_years=DEFAULT_COMPARISON_PERIOD_YEARS,
    )


def _build_ground_metadata(
    space_metadata: RunMetadata, ground_config: GroundReferenceConfig
) -> RunMetadata:
    """Build metadata for the ground artifact from the space run metadata."""
    return space_metadata.model_copy(
        update={
            "schema_version": GROUND_SCHEMA_VERSION,
            "scenario_name": ground_config.scenario_name,
            "artifact_role": (
                "promoted_ground_default"
                if space_metadata.artifact_role == "promoted_default"
                else "promoted_ground_named"
            ),
            "source_scenario_path": DEFAULT_GROUND_SCENARIO_PATH,
        }
    )


def _build_ground_input_manifest(
    *,
    ground_config: GroundReferenceConfig,
    source_catalog: SourceCatalog,
    source_scenario_path: str,
) -> GroundInputManifest:
    """Build the ground-reference input manifest from a typed config."""
    input_values: dict[str, InputScalar] = {
        "gpu_package_cost_multiplier": ground_config.gpu_package_cost_multiplier,
        "facility_shell_fitout_musd_per_mw": ground_config.facility_shell_fitout_musd_per_mw,
        "racked_power_network_musd_per_gpu_package": (
            ground_config.racked_power_network_musd_per_gpu_package
        ),
        "energy_price_usd_per_mwh": ground_config.energy_price_usd_per_mwh,
        "pue": ground_config.pue,
        "utilization": ground_config.utilization,
        "operations_maintenance_musd_per_mw_year": (
            ground_config.operations_maintenance_musd_per_mw_year
        ),
        "cooling_cost_musd_per_mw": ground_config.cooling_cost_musd_per_mw,
        "comparison_period_years": ground_config.comparison_period_years,
    }
    cells = {
        key: _input_cell(
            key=key,
            value=value,
            spec=GROUND_INPUT_SPECS[key],
            source_catalog=source_catalog,
            source_scenario_path=source_scenario_path,
        )
        for key, value in input_values.items()
    }
    input_tree = GroundAssumptionInputTree(**cells)
    assumption_index = {InputPath(cell.path): cell for cell in _collect_ground_cells(input_tree)}
    scenario = ScenarioIdentity(
        name=ground_config.scenario_name,
        description=("Canonical default ground reference scenario for the promoted space model."),
        path=source_scenario_path,
        is_default=source_scenario_path == DEFAULT_GROUND_SCENARIO_PATH,
        owner_note="Creator-selected ground reference assumptions traced to the research wiki.",
    )
    return GroundInputManifest(
        scenario=scenario,
        config=input_tree,
        assumption_index=assumption_index,
    )


def _input_cell(
    *,
    key: str,
    value: InputScalar,
    spec: GroundInputSpec,
    source_catalog: SourceCatalog,
    source_scenario_path: str,
) -> InputCell:
    """Construct one ground-reference input cell."""
    path = f"inputs.config.{key}"
    return InputCell(
        path=path,
        label=spec.label,
        value=value,
        unit=spec.unit,
        description=spec.description,
        assumption_role=AssumptionRole.DEFAULT,
        source_status=spec.source_status,
        source_refs=[
            SourceRef(
                ref_type=SourceRefType.SOURCE_INDEX,
                ref=f"{source_catalog.source_index_path}#{spec.claim_id}",
                claim_id=spec.claim_id,
                note="Per-input source ledger entry for the ground reference.",
            ),
            SourceRef(
                ref_type=SourceRefType.RESEARCH_DOC,
                ref=source_catalog.ground_cost_research_path,
                claim_id=spec.claim_id,
                note="Research basis for ground infrastructure and electricity costs.",
            ),
            SourceRef(
                ref_type=SourceRefType.MODEL_DERIVATION,
                ref=source_scenario_path,
                claim_id=spec.claim_id,
                note="Ground scenario YAML value used for this model run.",
            ),
        ],
        rationale=spec.rationale,
        notes=spec.notes,
    )


def _collect_ground_cells(input_tree: GroundAssumptionInputTree) -> list[InputCell]:
    """Collect all ground input cells in stable field order."""
    return [
        input_tree.gpu_package_cost_multiplier,
        input_tree.facility_shell_fitout_musd_per_mw,
        input_tree.racked_power_network_musd_per_gpu_package,
        input_tree.energy_price_usd_per_mwh,
        input_tree.pue,
        input_tree.utilization,
        input_tree.operations_maintenance_musd_per_mw_year,
        input_tree.cooling_cost_musd_per_mw,
        input_tree.comparison_period_years,
    ]


def _build_anchor(space_output: SpaceModelOutput) -> GroundComparisonAnchor:
    """Select the 2036 deployed-year cohort from the typed space output."""
    business_year = space_output.business.years[ANCHOR_YEAR_KEY]
    physical_year = space_output.physical.years[ANCHOR_YEAR_KEY]
    nodes = _numeric_cell_value(
        business_year.nodes_deployed_this_year,
        f'business.years."{ANCHOR_YEAR_KEY}".nodes_deployed_this_year',
    )
    gpus_per_node = _numeric_cell_value(
        physical_year.gpus_per_node,
        f'physical.years."{ANCHOR_YEAR_KEY}".gpus_per_node',
    )
    kw_per_node = _numeric_cell_value(
        physical_year.kw_per_node,
        f'physical.years."{ANCHOR_YEAR_KEY}".kw_per_node',
    )
    service_life_years = _numeric_input_value(
        space_output.inputs.config.fleet.service_life_years,
        "inputs.config.fleet.service_life_years",
    )
    return GroundComparisonAnchor(
        space_model_path=SPACE_MODEL_DEFAULT_PATH,
        year=ANCHOR_YEAR,
        basis=ANCHOR_BASIS,
        nodes=nodes,
        gpu_packages=nodes * gpus_per_node,
        kw=nodes * kw_per_node,
        service_life_years=service_life_years,
        note=ANCHOR_NOTE,
        source_paths=[
            f'business.years."{ANCHOR_YEAR_KEY}".nodes_deployed_this_year',
            f'physical.years."{ANCHOR_YEAR_KEY}".gpus_per_node',
            f'physical.years."{ANCHOR_YEAR_KEY}".kw_per_node',
            "inputs.config.fleet.service_life_years",
        ],
    )


def _build_ground_cost_result(
    anchor: GroundComparisonAnchor,
    space_output: SpaceModelOutput,
    inputs: GroundInputManifest,
) -> GroundCostResult:
    """Compute the five-year ground cost for the anchor cohort."""
    component_costs = _ground_components(anchor, space_output, inputs)
    included_costs = [component.cost for component in component_costs if component.included]
    total = _total_cell(
        value=sum(_float_cell_value(cost) for cost in included_costs),
        uses=[component.cost.description for component in component_costs if component.included],
        description="Total five-year ground cost for the anchor cohort.",
    )
    period = _float_input_value(inputs.config.comparison_period_years)
    annualized = _provenance_cell(
        value=_safe_ratio(_float_cell_value(total), period),
        unit="MUSD/year",
        formula_name="annualized_cost_from_total_and_period",
        uses=["ground.total_five_year_cost", "inputs.config.comparison_period_years"],
        sources=[GROUND_COST_BASIS_CLAIM_ID],
        source_status=SourceStatus.DERIVED_ESTIMATE,
        description="Ground total annualized over the comparison period.",
    )
    gpu_packages = float(anchor.gpu_packages)
    anchor_mw = float(anchor.kw) / KW_PER_MW
    return GroundCostResult(
        component_costs=component_costs,
        total_five_year_cost=total,
        annualized_cost=annualized,
        cost_per_gpu_package_five_year=_cost_per_unit_cell(
            value=_safe_ratio(_float_cell_value(total), gpu_packages),
            unit="MUSD/package",
            uses=["ground.total_five_year_cost", "anchor.gpu_packages"],
            description="Five-year ground cost per GPU package.",
        ),
        cost_per_mw_five_year=_cost_per_unit_cell(
            value=_safe_ratio(_float_cell_value(total), anchor_mw),
            unit="MUSD/MW",
            uses=["ground.total_five_year_cost", "anchor.kw"],
            description="Five-year ground cost per MW.",
        ),
        included_components=[
            "GPU/package acquisition",
            "facility shell or fit-out allocation",
            "racked power and networking",
            "energy over five years with PUE and utilization",
            "cooling infrastructure",
            "operations, maintenance, and labor",
        ],
        excluded_components=[
            "land acquisition",
            "financing costs",
            "taxes",
            "water costs",
            "depreciation accounting",
        ],
        source_status_summary=_source_status_summary_dict(inputs),
        warnings=[],
    )


def _ground_components(
    anchor: GroundComparisonAnchor,
    space_output: SpaceModelOutput,
    inputs: GroundInputManifest,
) -> list[CostComponent]:
    """Build all included ground cost components."""
    physical_year = space_output.physical.years[ANCHOR_YEAR_KEY]
    compute_cost_per_node = _float_cell_value(physical_year.cost_breakdown.compute)
    gpus_per_node = _float_cell_value(physical_year.gpus_per_node)
    package_cost_musd = _required_ratio(
        compute_cost_per_node,
        gpus_per_node,
        f'physical.years."{ANCHOR_YEAR_KEY}".gpus_per_node',
    )
    gpu_packages = float(anchor.gpu_packages)
    anchor_mw = float(anchor.kw) / KW_PER_MW
    period = _float_input_value(inputs.config.comparison_period_years)
    multiplier = _float_input_value(inputs.config.gpu_package_cost_multiplier)
    facility_rate = _float_input_value(inputs.config.facility_shell_fitout_musd_per_mw)
    rack_network_rate = _float_input_value(inputs.config.racked_power_network_musd_per_gpu_package)
    energy_price = _float_input_value(inputs.config.energy_price_usd_per_mwh)
    pue = _float_input_value(inputs.config.pue)
    utilization = _float_input_value(inputs.config.utilization)
    operations_rate = _float_input_value(inputs.config.operations_maintenance_musd_per_mw_year)
    cooling_rate = _float_input_value(inputs.config.cooling_cost_musd_per_mw)
    energy_musd = (
        float(anchor.kw)
        * pue
        * utilization
        * HOURS_PER_YEAR
        * period
        / KWH_PER_MWH
        * energy_price
        / MUSD_PER_USD
    )
    return [
        _component(
            name="gpu_package_acquisition",
            label="GPU/package acquisition",
            cost=_provenance_cell(
                value=gpu_packages * package_cost_musd * multiplier,
                unit="MUSD",
                formula_name="ground_gpu_acquisition_from_space_package_cost",
                uses=[
                    "anchor.gpu_packages",
                    f'physical.years."{ANCHOR_YEAR_KEY}".cost_breakdown.compute',
                    f'physical.years."{ANCHOR_YEAR_KEY}".gpus_per_node',
                    "inputs.config.gpu_package_cost_multiplier",
                ],
                sources=[GROUND_GPU_PACKAGE_COST_BOUNDARY_CLAIM_ID],
                source_status=SourceStatus.DERIVED_ESTIMATE,
                description="Ground acquisition cost for the same GPU package count.",
            ),
            source_paths=[
                "anchor.gpu_packages",
                f'physical.years."{ANCHOR_YEAR_KEY}".cost_breakdown.compute',
                "inputs.config.gpu_package_cost_multiplier",
            ],
            notes="Uses the space model's same-generation package cost basis.",
        ),
        _component(
            name="facility_shell_fitout",
            label="Facility shell / fit-out allocation",
            cost=_provenance_cell(
                value=anchor_mw * facility_rate,
                unit="MUSD",
                formula_name="ground_facility_cost_from_mw",
                uses=["anchor.kw", "inputs.config.facility_shell_fitout_musd_per_mw"],
                sources=[GROUND_FACILITY_FITOUT_CLAIM_ID, GROUND_COST_RESEARCH_PATH],
                source_status=SourceStatus.DERIVED_ESTIMATE,
                description="Ground facility shell and AI-hall fit-out allocation.",
            ),
            source_paths=["anchor.kw", "inputs.config.facility_shell_fitout_musd_per_mw"],
            notes="Source-linked facility allocation; not a site-specific construction estimate.",
        ),
        _component(
            name="racked_power_networking",
            label="Racked power and networking",
            cost=_provenance_cell(
                value=gpu_packages * rack_network_rate,
                unit="MUSD",
                formula_name="ground_racked_power_network_from_package_count",
                uses=[
                    "anchor.gpu_packages",
                    "inputs.config.racked_power_network_musd_per_gpu_package",
                ],
                sources=[GROUND_RACKED_POWER_NETWORK_CLAIM_ID],
                source_status=SourceStatus.DERIVED_ESTIMATE,
                description="Racked power distribution and networking allocation.",
            ),
            source_paths=[
                "anchor.gpu_packages",
                "inputs.config.racked_power_network_musd_per_gpu_package",
            ],
            notes="Scenario non-GPU rack allocation with sourced support.",
        ),
        _component(
            name="energy",
            label="Five-year energy",
            cost=_provenance_cell(
                value=energy_musd,
                unit="MUSD",
                formula_name="ground_energy_cost_from_kw_pue_utilization",
                uses=[
                    "anchor.kw",
                    "inputs.config.energy_price_usd_per_mwh",
                    "inputs.config.pue",
                    "inputs.config.utilization",
                    "inputs.config.comparison_period_years",
                ],
                sources=[
                    GROUND_ENERGY_PRICE_CLAIM_ID,
                    GROUND_PUE_CLAIM_ID,
                    GROUND_UTILIZATION_CLAIM_ID,
                    GROUND_COMPARISON_PERIOD_CLAIM_ID,
                    GROUND_COST_RESEARCH_PATH,
                ],
                source_status=SourceStatus.DERIVED_ESTIMATE,
                description="Five-year electricity cost using PUE and utilization.",
            ),
            source_paths=[
                "anchor.kw",
                "inputs.config.energy_price_usd_per_mwh",
                "inputs.config.pue",
                "inputs.config.utilization",
            ],
            notes="Energy cost is order-of-magnitude and excludes site-specific tariffs.",
        ),
        _component(
            name="cooling",
            label="Cooling infrastructure",
            cost=_provenance_cell(
                value=anchor_mw * cooling_rate,
                unit="MUSD",
                formula_name="ground_cooling_cost_from_mw",
                uses=["anchor.kw", "inputs.config.cooling_cost_musd_per_mw"],
                sources=[GROUND_COOLING_CLAIM_ID, GROUND_COST_RESEARCH_PATH],
                source_status=SourceStatus.DERIVED_ESTIMATE,
                description="Cooling infrastructure allocation for the ground cohort.",
            ),
            source_paths=["anchor.kw", "inputs.config.cooling_cost_musd_per_mw"],
            notes="Water cost is excluded separately rather than included here.",
        ),
        _component(
            name="operations_maintenance_labor",
            label="Operations, maintenance, and labor",
            cost=_provenance_cell(
                value=anchor_mw * operations_rate * period,
                unit="MUSD",
                formula_name="ground_operations_cost_from_mw_year",
                uses=[
                    "anchor.kw",
                    "inputs.config.operations_maintenance_musd_per_mw_year",
                    "inputs.config.comparison_period_years",
                ],
                sources=[GROUND_OPERATIONS_MAINTENANCE_CLAIM_ID],
                source_status=SourceStatus.DERIVED_ESTIMATE,
                description="Five-year operations, maintenance, and labor allocation.",
            ),
            source_paths=[
                "anchor.kw",
                "inputs.config.operations_maintenance_musd_per_mw_year",
            ],
            notes="Labor is represented in this combined recurring-cost line.",
        ),
    ]


def _build_orbital_reference_result(
    anchor: GroundComparisonAnchor,
    space_output: SpaceModelOutput,
) -> OrbitalReferenceResult:
    """Mirror the space model's 2036 build and launch components."""
    physical_year = space_output.physical.years[ANCHOR_YEAR_KEY]
    nodes = float(anchor.nodes)
    component_costs = [
        _orbital_component(
            "compute", "Compute hardware", physical_year.cost_breakdown.compute, nodes
        ),
        _orbital_component("bus", "Bus/platform", physical_year.cost_breakdown.bus, nodes),
        _orbital_component("solar", "Solar/power", physical_year.cost_breakdown.solar, nodes),
        _orbital_component(
            "radiator", "Radiator/thermal", physical_year.cost_breakdown.radiator, nodes
        ),
        _orbital_component(
            "launch", "Launch allocation", physical_year.cost_breakdown.launch, nodes
        ),
    ]
    total = _provenance_cell(
        value=sum(_float_cell_value(component.cost) for component in component_costs),
        unit="MUSD",
        formula_name="orbital_total_cost_from_space_node_total",
        uses=[component.cost.description for component in component_costs],
        sources=["space model cost_breakdown"],
        source_status=SourceStatus.DERIVED_ESTIMATE,
        description="Total orbital build and launch cost for the anchor cohort.",
    )
    anchor_mw = float(anchor.kw) / KW_PER_MW
    warnings = _orbital_scope_warnings()
    return OrbitalReferenceResult(
        component_costs=component_costs,
        total_build_and_launch_cost=total,
        five_year_cost_view=total,
        cost_per_gpu_package_five_year=_cost_per_unit_cell(
            value=_safe_ratio(_float_cell_value(total), float(anchor.gpu_packages)),
            unit="MUSD/package",
            uses=["orbital_reference.five_year_cost_view", "anchor.gpu_packages"],
            description="Five-year orbital reference cost per GPU package.",
        ),
        cost_per_mw_five_year=_cost_per_unit_cell(
            value=_safe_ratio(_float_cell_value(total), anchor_mw),
            unit="MUSD/MW",
            uses=["orbital_reference.five_year_cost_view", "anchor.kw"],
            description="Five-year orbital reference cost per MW.",
        ),
        kw=_provenance_cell(
            value=anchor.kw,
            unit="kW",
            formula_name="kw_deployed_this_year_from_nodes",
            uses=[
                f'business.years."{ANCHOR_YEAR_KEY}".nodes_deployed_this_year',
                f'physical.years."{ANCHOR_YEAR_KEY}".kw_per_node',
            ],
            sources=["space model deployed-year cohort"],
            source_status=SourceStatus.DERIVED_ESTIMATE,
            description="Anchor cohort deployed kW.",
        ),
        gpu_packages=_provenance_cell(
            value=anchor.gpu_packages,
            unit="count",
            formula_name="ground_anchor_gpu_packages_from_nodes_and_packages",
            uses=[
                f'business.years."{ANCHOR_YEAR_KEY}".nodes_deployed_this_year',
                f'physical.years."{ANCHOR_YEAR_KEY}".gpus_per_node',
            ],
            sources=["space model deployed-year cohort"],
            source_status=SourceStatus.DERIVED_ESTIMATE,
            description="Anchor cohort GPU packages.",
        ),
        explicit_exclusions=[
            "orbital operations beyond modeled build and launch",
            "insurance",
            "financing costs",
            "taxes",
            "customer ground-station integration",
        ],
        warnings=warnings,
    )


def _build_comparison(
    *,
    ground: GroundCostResult,
    orbital_reference: OrbitalReferenceResult,
    warnings: list[ValidationResult],
) -> GroundSpaceComparison:
    """Build total and component-level ground/orbit deltas."""
    ground_total = _float_cell_value(ground.total_five_year_cost)
    orbital_total = _float_cell_value(orbital_reference.five_year_cost_view)
    ground_per_package = _float_cell_value(ground.cost_per_gpu_package_five_year)
    orbital_per_package = _float_cell_value(orbital_reference.cost_per_gpu_package_five_year)
    ground_per_mw = _float_cell_value(ground.cost_per_mw_five_year)
    orbital_per_mw = _float_cell_value(orbital_reference.cost_per_mw_five_year)
    ratio = _safe_ratio(ground_total, orbital_total)
    return GroundSpaceComparison(
        ground_total_five_year_cost=ground.total_five_year_cost,
        orbital_total_five_year_cost=orbital_reference.five_year_cost_view,
        absolute_delta=_delta_cell(
            value=ground_total - orbital_total,
            uses=["ground.total_five_year_cost", "orbital_reference.five_year_cost_view"],
            description="Ground five-year total minus orbital five-year reference total.",
        ),
        ground_to_orbit_ratio=_ratio_cell(
            value=ratio,
            uses=["ground.total_five_year_cost", "orbital_reference.five_year_cost_view"],
            description="Ground five-year total divided by orbital five-year reference total.",
        ),
        orbit_to_ground_ratio=_ratio_cell(
            value=_safe_ratio(orbital_total, ground_total),
            uses=["orbital_reference.five_year_cost_view", "ground.total_five_year_cost"],
            description="Orbital five-year reference total divided by ground five-year total.",
        ),
        cost_per_gpu_package_delta=_delta_cell(
            value=ground_per_package - orbital_per_package,
            uses=[
                "ground.cost_per_gpu_package_five_year",
                "orbital_reference.cost_per_gpu_package_five_year",
            ],
            description="Ground minus orbital cost per GPU package.",
        ),
        cost_per_mw_delta=_delta_cell(
            value=ground_per_mw - orbital_per_mw,
            uses=["ground.cost_per_mw_five_year", "orbital_reference.cost_per_mw_five_year"],
            description="Ground minus orbital cost per MW.",
        ),
        component_deltas=_component_deltas(ground, orbital_reference),
        conclusion_label=_conclusion_label(ratio),
        warnings=warnings,
    )


def _component(
    *,
    name: str,
    label: str,
    cost: ProvenanceCell,
    source_paths: list[str],
    notes: str,
) -> CostComponent:
    """Build one included cost component."""
    return CostComponent(
        name=name,
        label=label,
        cost=cost,
        included=True,
        source_paths=source_paths,
        notes=notes,
    )


def _orbital_component(
    name: str, label: str, per_node_cost: ProvenanceCell, nodes: float
) -> CostComponent:
    """Build one orbital reference component from a per-node space cell."""
    return CostComponent(
        name=name,
        label=label,
        cost=_provenance_cell(
            value=_float_cell_value(per_node_cost) * nodes,
            unit="MUSD",
            formula_name="orbital_component_cost_from_space_node_component",
            uses=[f'physical.years."{ANCHOR_YEAR_KEY}".cost_breakdown.{name}', "anchor.nodes"],
            sources=per_node_cost.sources,
            source_status=per_node_cost.source_status,
            description=f"Anchor-cohort orbital {label.lower()} cost.",
        ),
        included=True,
        source_paths=[f'physical.years."{ANCHOR_YEAR_KEY}".cost_breakdown.{name}'],
        notes="Mirrors the promoted space model's per-node component.",
    )


def _component_deltas(
    ground: GroundCostResult, orbital_reference: OrbitalReferenceResult
) -> list[ComponentDelta]:
    """Build grouped component deltas that keep unlike line items legible."""
    ground_by_name = {component.name: component.cost for component in ground.component_costs}
    orbital_by_name = {
        component.name: component.cost for component in orbital_reference.component_costs
    }
    return [
        _component_delta(
            name="compute",
            ground_cost=ground_by_name["gpu_package_acquisition"],
            orbital_cost=orbital_by_name["compute"],
            notes="Compares like-for-like GPU/package acquisition.",
        ),
        _component_delta(
            name="platform_vs_facility",
            ground_cost=_sum_group_cell(
                name="ground facility plus rack infrastructure",
                costs=[
                    ground_by_name["facility_shell_fitout"],
                    ground_by_name["racked_power_networking"],
                ],
            ),
            orbital_cost=orbital_by_name["bus"],
            notes="Compares terrestrial facility/rack integration against orbital bus.",
        ),
        _component_delta(
            name="power_thermal_operations",
            ground_cost=_sum_group_cell(
                name="ground energy plus cooling plus operations",
                costs=[
                    ground_by_name["energy"],
                    ground_by_name["cooling"],
                    ground_by_name["operations_maintenance_labor"],
                ],
            ),
            orbital_cost=_sum_group_cell(
                name="orbital solar plus radiator",
                costs=[orbital_by_name["solar"], orbital_by_name["radiator"]],
            ),
            notes="Compares terrestrial recurring support against orbital power/thermal capex.",
        ),
        _component_delta(
            name="launch",
            ground_cost=_provenance_cell(
                value=ZERO_COST,
                unit="MUSD",
                formula_name="explicit_zero_cost_for_excluded_component",
                uses=[],
                sources=["ground reference explicit non-applicability"],
                source_status=SourceStatus.SCENARIO,
                description="Ground launch cost is not applicable.",
            ),
            orbital_cost=orbital_by_name["launch"],
            notes="Launch is an orbital-only cost line.",
        ),
    ]


def _component_delta(
    *,
    name: str,
    ground_cost: ProvenanceCell,
    orbital_cost: ProvenanceCell,
    notes: str,
) -> ComponentDelta:
    """Build one component delta."""
    ground_value = _float_cell_value(ground_cost)
    orbital_value = _float_cell_value(orbital_cost)
    return ComponentDelta(
        name=name,
        ground_cost=ground_cost,
        orbital_reference_cost=orbital_cost,
        absolute_delta=_delta_cell(
            value=ground_value - orbital_value,
            uses=[ground_cost.description, orbital_cost.description],
            description=f"Ground minus orbital cost for {name}.",
        ),
        ground_to_orbit_ratio=_ratio_cell(
            value=_safe_ratio(ground_value, orbital_value),
            uses=[ground_cost.description, orbital_cost.description],
            description=f"Ground/orbital ratio for {name}.",
        ),
        notes=notes,
    )


def _sum_group_cell(name: str, costs: list[ProvenanceCell]) -> ProvenanceCell:
    """Build a provenance cell for a grouped component subtotal."""
    return _provenance_cell(
        value=sum(_float_cell_value(cost) for cost in costs),
        unit="MUSD",
        formula_name="total_cost_from_components",
        uses=[cost.description for cost in costs],
        sources=["ground reference grouped component subtotal"],
        source_status=SourceStatus.DERIVED_ESTIMATE,
        description=f"Grouped cost subtotal for {name}.",
    )


def _total_cell(value: float, uses: list[str], description: str) -> ProvenanceCell:
    """Build a total-cost provenance cell."""
    return _provenance_cell(
        value=value,
        unit="MUSD",
        formula_name="total_cost_from_components",
        uses=uses,
        sources=[GROUND_COST_BASIS_CLAIM_ID],
        source_status=SourceStatus.DERIVED_ESTIMATE,
        description=description,
    )


def _cost_per_unit_cell(
    *, value: float | None, unit: str, uses: list[str], description: str
) -> ProvenanceCell:
    """Build a cost-per-unit provenance cell."""
    return _provenance_cell(
        value=value,
        unit=unit,
        formula_name="cost_per_unit_from_total",
        uses=uses,
        sources=[GROUND_COST_BASIS_CLAIM_ID],
        source_status=SourceStatus.DERIVED_ESTIMATE,
        description=description,
    )


def _delta_cell(value: float, uses: list[str], description: str) -> ProvenanceCell:
    """Build a delta provenance cell."""
    return _provenance_cell(
        value=value,
        unit="MUSD",
        formula_name="absolute_delta_from_totals",
        uses=uses,
        sources=["ground reference comparison arithmetic"],
        source_status=SourceStatus.DERIVED_ESTIMATE,
        description=description,
    )


def _ratio_cell(value: float | None, uses: list[str], description: str) -> ProvenanceCell:
    """Build a ratio provenance cell."""
    return _provenance_cell(
        value=value,
        unit="ratio",
        formula_name="ratio_from_totals",
        uses=uses,
        sources=["ground reference comparison arithmetic"],
        source_status=SourceStatus.DERIVED_ESTIMATE,
        description=description,
    )


def _provenance_cell(
    *,
    value: float | int | str | bool | None,
    unit: str,
    formula_name: str,
    uses: list[FieldPath],
    sources: list[str],
    source_status: SourceStatus,
    description: str,
    notes: str | None = None,
) -> ProvenanceCell:
    """Build a provenance cell with source status and notes."""
    built = cell(
        value=value,
        unit=unit,
        formula_name=formula_name,
        uses=uses,
        sources=sources,
        description=description,
    )
    return built.model_copy(update={"source_status": source_status, "notes": notes})


def _orbital_scope_warnings() -> list[ValidationResult]:
    """Emit warnings for the orbital reference scope."""
    return [
        ValidationResult(
            validation_id="orbital_reference_scope_build_launch_only",
            severity=ValidationSeverity.WARN,
            what_tested="Orbital reference scope.",
            expected_condition="The orbital reference states what is excluded.",
            observed_result="The reference mirrors modeled build and launch cost only.",
            related_json_paths=["orbital_reference.explicit_exclusions"],
            remediation_hint=(
                "Add orbital operating-cost assumptions before using this as a full TCO."
            ),
        )
    ]


def _comparison_scope_warnings() -> list[ValidationResult]:
    """Emit warnings for order-of-magnitude comparison scope."""
    return [
        ValidationResult(
            validation_id="ground_reference_order_of_magnitude_only",
            severity=ValidationSeverity.WARN,
            what_tested="Ground comparison interpretation.",
            expected_condition="The output avoids DCF or precise parity claims.",
            observed_result="Ground reference is an order-of-magnitude cost screen.",
            related_json_paths=["comparison.conclusion_label"],
            remediation_hint=(
                "Use sourced site-specific inputs before making precise parity claims."
            ),
        )
    ]


def _anchor_validation_results(anchor: GroundComparisonAnchor) -> list[ValidationResult]:
    """Build public validation results for the canonical anchor."""
    return [
        ValidationResult(
            validation_id="ground_anchor_2036_deployed_year",
            severity=ValidationSeverity.OK,
            what_tested="Ground anchor uses the canonical deployed-year cohort.",
            expected_condition="year=2036 and basis=deployed_this_year.",
            observed_result=f"year={anchor.year}; basis={anchor.basis}.",
            related_json_paths=["anchor.year", "anchor.basis", *anchor.source_paths],
            remediation_hint=None,
        )
    ]


def _source_status_summary_dict(inputs: GroundInputManifest) -> dict[str, int]:
    """Count ground assumptions by source-status string."""
    counts = {status.value: ZERO_COUNT for status in SourceStatus}
    for cell_value in inputs.assumption_index.values():
        counts[cell_value.source_status.value] += ONE_COUNT
    return counts


def _source_status_summary_model(inputs: GroundInputManifest) -> SourceStatusSummary:
    """Build the known-shape source-status summary model."""
    counts = _source_status_summary_dict(inputs)
    return SourceStatusSummary(
        certified=counts[SourceStatus.CERTIFIED.value],
        sourced_estimate=counts[SourceStatus.SOURCED_ESTIMATE.value],
        derived_estimate=counts[SourceStatus.DERIVED_ESTIMATE.value],
        projection=counts[SourceStatus.PROJECTION.value],
        extrapolation=counts[SourceStatus.EXTRAPOLATION.value],
        scenario=counts[SourceStatus.SCENARIO.value],
        placeholder=counts[SourceStatus.PLACEHOLDER.value],
        stale=counts[SourceStatus.STALE.value],
    )


def _conclusion_label(ratio: float | None) -> str:
    """Choose a plain conclusion label for the comparison result."""
    if ratio is None:
        raise ValueError("ground/orbital ratio must be computable to label the comparison")
    if ratio < GROUND_MATERIALLY_CHEAPER_RATIO:
        return GroundConclusionLabel.GROUND_CHEAPER.value
    if ratio > ORBITAL_MATERIALLY_CHEAPER_RATIO:
        return GroundConclusionLabel.ORBITAL_CHEAPER.value
    return GroundConclusionLabel.SAME_ORDER.value


def _ground_data_dictionary() -> list[DataDictEntry]:
    """Return compact data dictionary entries for high-value ground paths."""
    return [
        DataDictEntry(
            path="anchor",
            description="The 2036 deployed-year cohort selected from the space model.",
            unit="-",
            type="object",
            source_class="DERIVED",
        ),
        DataDictEntry(
            path="ground.total_five_year_cost",
            description="Total five-year terrestrial cost for the anchor cohort.",
            unit="MUSD",
            type="cell",
            source_class="DERIVED",
        ),
        DataDictEntry(
            path="orbital_reference.five_year_cost_view",
            description="Comparable five-year build/launch cost view from the space model.",
            unit="MUSD",
            type="cell",
            source_class="DERIVED",
        ),
        DataDictEntry(
            path="comparison.ground_to_orbit_ratio",
            description="Ground five-year total divided by orbital five-year reference total.",
            unit="ratio",
            type="cell",
            source_class="DERIVED",
        ),
        DataDictEntry(
            path="inputs.assumption_index",
            description="Flat index of every ground assumption input cell.",
            unit="-",
            type="object",
            source_class="INPUT",
        ),
    ]


def _ground_query_examples() -> list[QueryExample]:
    """Return ground-specific jq examples for cold readers."""
    return [
        QueryExample(
            name="ground_anchor",
            question_answered="What cohort does the ground reference compare against?",
            jq_expression=".anchor",
            expected_shape="object with year, basis, nodes, gpu_packages, kw",
            important_paths=["anchor"],
            applies_to=QueryAppliesTo.GROUND,
        ),
        QueryExample(
            name="ground_assumptions",
            question_answered="What ground assumptions feed the comparison?",
            jq_expression=(
                ".inputs.assumption_index | to_entries[] | "
                "{path: .key, value: .value.value, status: .value.source_status}"
            ),
            expected_shape="stream of assumption path/value/status objects",
            important_paths=["inputs.assumption_index"],
            applies_to=QueryAppliesTo.GROUND,
        ),
        QueryExample(
            name="ground_cost_summary",
            question_answered="What are the total ground and orbital five-year costs?",
            jq_expression="{ground: .ground.total_five_year_cost, orbital: "
            ".orbital_reference.five_year_cost_view}",
            expected_shape="object with two ProvenanceCell values",
            important_paths=[
                "ground.total_five_year_cost",
                "orbital_reference.five_year_cost_view",
            ],
            applies_to=QueryAppliesTo.GROUND,
        ),
        QueryExample(
            name="ground_space_ratio",
            question_answered="What is the ground/orbit comparison ratio?",
            jq_expression=".comparison.ground_to_orbit_ratio",
            expected_shape="ProvenanceCell ratio",
            important_paths=["comparison.ground_to_orbit_ratio"],
            applies_to=QueryAppliesTo.GROUND,
        ),
    ]


def _numeric_cell_value(cell_value: ProvenanceCell, path: str) -> int | float:
    """Return a provenance cell's numeric value, preserving int when present."""
    value = cell_value.value
    if isinstance(value, bool) or value is None or isinstance(value, str):
        raise ValueError(f"{path} is not numeric")
    return value


def _numeric_input_value(cell_value: InputCell, path: str) -> int | float:
    """Return an input cell's numeric value, preserving int when present."""
    value = cell_value.value
    if isinstance(value, (bool, str, list)):
        raise ValueError(f"{path} is not numeric")
    return value


def _float_cell_value(cell_value: ProvenanceCell) -> float:
    """Return a provenance cell's numeric value as ``float``."""
    value = _numeric_cell_value(cell_value, cell_value.description)
    return float(value)


def _float_input_value(cell_value: InputCell) -> float:
    """Return an input cell's numeric value as ``float``."""
    value = _numeric_input_value(cell_value, cell_value.path)
    return float(value)


def _safe_ratio(numerator: float, denominator: float) -> float | None:
    """Return ``numerator / denominator`` or ``None`` when denominator is zero."""
    if denominator == ZERO_COST:
        logger.warning("ground reference ratio requested with zero denominator")
        return None
    return numerator / denominator


def _required_ratio(numerator: float, denominator: float, denominator_path: str) -> float:
    """Return a ratio, failing fast when a required denominator is zero."""
    ratio = _safe_ratio(numerator, denominator)
    if ratio is None:
        raise ValueError(f"{denominator_path} must be non-zero for ground reference output")
    return ratio


__all__ = [
    "ANCHOR_YEAR",
    "DEFAULT_GROUND_SCENARIO_PATH",
    "GroundReferenceConfig",
    "GroundReferenceOutput",
    "SourceCatalog",
    "build_ground_reference_output",
    "default_ground_source_catalog",
    "ground_config_from_dict",
    "load_ground_config",
    "render_ground_json",
]
