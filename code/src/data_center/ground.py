"""Typed ground reference model for the public data-center comparison.

The ground reference model compares one terrestrial data-center cohort
against the space model's deployed-year cohort at the run's anchor year
(ADR-003): :func:`data_center.config.anchor_year` of the space run's window,
FY2036 for the default. The comparison period is the anchor cohort's service
life (``anchor.service_life_years``, five years for the default), derived
from the space run rather than set by a separate dial, so the ground energy
and operations lines always cover the life the orbital cohort is built for.

It is a small deep module: callers provide a typed :class:`SpaceModelOutput`,
a typed ground-assumption config, and the repository paths of the space
artifact and the ground scenario actually used; this module owns the anchor
selection, input manifest, cost arithmetic, validation, and output contract.

Provenance: every ``uses`` entry resolves. A path without a prefix resolves
inside the ground artifact (``anchor.*``, ``inputs.config.*``,
``ground.component_costs[i].cost``); a path prefixed ``space:``
(:data:`SPACE_PATH_PREFIX`) resolves inside the space artifact named by
``anchor.space_model_path``. The anchor's numeric fields are plain values, so
a cell that reads one cites both ``anchor.<quantity>`` and the space cells the
quantity is taken from (:func:`_anchor_uses`): a space dial that moves the
anchor cohort reaches every ground cost built on it.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Final  # typing-acceptable: Any types the YAML boundary

from pydantic import BaseModel, ConfigDict, Field

from common.file_io import load_yaml_mapping
from common.input_manifest import CellSpec, _field_description, _spec_cell
from common.meta import COUNT_UNIT, summarize_source_statuses
from data_center.config import anchor_year
from data_center.input_manifest import (
    AssumptionRole,
    InputCell,
    InputPath,
    ScenarioIdentity,
    SourceStatus,
    collect_input_cells,
)
from data_center.json_output import build_data_dictionary
from data_center.output import (
    YEAR_UNIT,
    YEARS_UNIT,
    ArtifactRole,
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

SPACE_PATH_PREFIX: Final[str] = "space:"
"""Prefix marking a ``uses`` path that resolves in the space artifact.

The ground reference cites space-model cells (the anchor cohort's per-node
cost lines, node counts, and power); those paths live in the space artifact
named by ``anchor.space_model_path``, not in the ground artifact, so they
carry this explicit cross-artifact prefix. Unprefixed paths resolve in the
ground artifact itself."""

SPACE_SERVICE_LIFE_PATH: Final[FieldPath] = "inputs.config.fleet.service_life_years"
"""Space-artifact path of the service life that sets the comparison period."""

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

MIN_PUE: Final[float] = 1.0
"""Lower bound on PUE: total facility power cannot be less than the IT load
it serves, so a PUE below one would understate energy cost."""

DEFAULT_UTILIZATION: Final[float] = 0.85
"""Scenario average IT-load utilization over the comparison window."""

MIN_UTILIZATION: Final[float] = 0.0
"""Lower bound on average IT-load utilization: an idle cohort draws no IT
load, and a negative fraction of the comparison period is meaningless."""

MAX_UTILIZATION: Final[float] = 1.0
"""Upper bound on average IT-load utilization: the fraction of the comparison
period the IT load runs at full power cannot exceed one."""

DEFAULT_OPERATIONS_MAINTENANCE_MUSD_PER_MW_YEAR: Final[float] = 1.5
"""Scenario annual operations, maintenance, and labor allocation per MW."""

DEFAULT_COOLING_COST_MUSD_PER_MW: Final[float] = 4.0
"""Scenario liquid-cooling infrastructure allocation per MW."""

GROUND_RESEARCH_NOTE: Final[str] = "Research basis for ground infrastructure and electricity costs."
"""What the ground research note supports, cited on every default ground input."""

GROUND_SOURCE_NOTE: Final[str] = "Per-input source ledger entry for the ground reference."
"""What each ground input's SOURCE_INDEX claim supports."""

ANCHOR_KW_RELATIVE_TOLERANCE: Final[float] = 1e-9
"""Relative tolerance for the anchor check's kW comparison. The anchor kW
(nodes x kW per node) and the space model's deployed-year kW cell are the
same product computed in two places, so they may differ only by float
rounding, far below a billionth of the value."""

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


class AnchorQuantity(StrEnum):
    """A numeric quantity of the ground anchor, taken from the space output."""

    NODES = "nodes"
    GPU_PACKAGES = "gpu_packages"
    KW = "kw"
    SERVICE_LIFE_YEARS = "service_life_years"


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
        description="Multiplier applied to the space model's anchor-year package cost.",
    )
    facility_shell_fitout_musd_per_mw: float = Field(
        default=DEFAULT_FACILITY_SHELL_FITOUT_MUSD_PER_MW,
        ge=ZERO_COST,
        description="Facility shell and fit-out allocation per MW, charged to the anchor cohort.",
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
        ge=MIN_PUE,
        description="Power usage effectiveness applied to IT load.",
    )
    utilization: float = Field(
        default=DEFAULT_UTILIZATION,
        ge=MIN_UTILIZATION,
        le=MAX_UTILIZATION,
        description=(
            "Average IT-load utilization during the comparison period (the "
            "anchor cohort's service life)."
        ),
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


class GroundInputManifest(BaseModel):
    """Complete typed input manifest for the ground reference artifact."""

    model_config = ConfigDict(frozen=True)

    scenario: ScenarioIdentity = Field(..., description="Ground scenario identity metadata.")
    config: GroundAssumptionInputTree = Field(..., description="Ground assumption cells.")
    assumption_index: dict[InputPath, InputCell] = Field(
        ..., description="Flat path-indexed lookup for all ground input cells."
    )


class GroundComparisonAnchor(BaseModel):
    """The deployed-year cohort selected from the space model."""

    model_config = ConfigDict(frozen=True)

    space_model_path: str = Field(
        ...,
        description=(
            "Repository path of the space artifact this reference was built from; "
            "'uses' entries prefixed 'space:' resolve in it."
        ),
    )
    year: int = Field(..., description="Anchor year.", json_schema_extra={"unit": YEAR_UNIT})
    basis: str = Field(..., description="Anchor basis.")
    nodes: int = Field(
        ...,
        description="Nodes deployed in the anchor year.",
        json_schema_extra={"unit": COUNT_UNIT},
    )
    gpu_packages: int = Field(
        ...,
        description="GPU packages in the anchor cohort.",
        json_schema_extra={"unit": COUNT_UNIT},
    )
    kw: float = Field(
        ..., description="Anchor cohort IT load, kW.", json_schema_extra={"unit": "kW"}
    )
    service_life_years: int = Field(
        ...,
        description=(
            "Space model service life of the anchor cohort; the ground comparison period."
        ),
        json_schema_extra={"unit": YEARS_UNIT},
    )
    note: str = Field(..., description="Plain-language anchor note.")
    source_paths: list[str] = Field(
        ...,
        description=(
            "Space-model cells the anchor quantities are taken from, prefixed "
            "'space:' (they resolve in the space artifact at space_model_path)."
        ),
    )


class CostComponent(BaseModel):
    """One cost line in a ground or orbital reference result."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Stable component key.")
    label: str = Field(..., description="Human-readable component label.")
    cost: ProvenanceCell = Field(
        ..., description="Cost of this component over the comparison period."
    )
    included: bool = Field(..., description="Whether this component is included in totals.")
    source_paths: list[str] = Field(..., description="Source JSON paths or input cells.")
    notes: str | None = Field(default=None, description="Component caveat or treatment note.")


class GroundCostResult(BaseModel):
    """Ground-side cost result for the selected deployed-year cohort."""

    model_config = ConfigDict(frozen=True)

    component_costs: list[CostComponent] = Field(..., description="Ground cost components.")
    total_five_year_cost: ProvenanceCell = Field(
        ...,
        description=(
            "Total ground cost over the comparison period (the anchor cohort's "
            "service life; five years for the default)."
        ),
    )
    annualized_cost: ProvenanceCell = Field(..., description="Annualized ground cost.")
    cost_per_gpu_package_five_year: ProvenanceCell = Field(
        ..., description="Ground cost per GPU package over the comparison period."
    )
    cost_per_mw_five_year: ProvenanceCell = Field(
        ..., description="Ground cost per MW over the comparison period."
    )
    included_components: list[str] = Field(..., description="Explicitly included components.")
    excluded_components: list[str] = Field(..., description="Explicitly excluded components.")
    warnings: list[ValidationResult] = Field(..., description="Ground-side warnings.")


class OrbitalReferenceResult(BaseModel):
    """Space-model build/launch reference for the same deployed-year cohort."""

    model_config = ConfigDict(frozen=True)

    component_costs: list[CostComponent] = Field(..., description="Orbital cost components.")
    total_build_and_launch_cost: ProvenanceCell = Field(
        ..., description="Total build and launch cost for the anchor cohort."
    )
    five_year_cost_view: ProvenanceCell = Field(
        ...,
        description=(
            "Orbital cost over the comparison period: the cohort's build and "
            "launch cost, which covers its whole service life."
        ),
    )
    cost_per_gpu_package_five_year: ProvenanceCell = Field(
        ..., description="Orbital cost per GPU package over the comparison period."
    )
    cost_per_mw_five_year: ProvenanceCell = Field(
        ..., description="Orbital cost per MW over the comparison period."
    )
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
    """Direct comparison between ground and orbital costs over the comparison period."""

    model_config = ConfigDict(frozen=True)

    ground_total_five_year_cost: ProvenanceCell = Field(
        ..., description="Ground total cost over the comparison period."
    )
    orbital_total_five_year_cost: ProvenanceCell = Field(
        ..., description="Orbital total reference cost over the comparison period."
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
    conclusion_label: GroundConclusionLabel = Field(
        ..., description="Plain-language conclusion label."
    )
    warnings: list[ValidationResult] = Field(..., description="Comparison warnings.")


class GroundOutputMetadata(BaseModel):
    """Metadata that helps cold readers query and validate the ground output."""

    model_config = ConfigDict(frozen=True)

    data_dictionary: list[DataDictEntry] = Field(
        ...,
        description=(
            "One entry per emitted leaf field, generated from this artifact by "
            "the shared data-dictionary builder."
        ),
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
    anchor: GroundComparisonAnchor = Field(..., description="Anchor-year deployed cohort.")
    inputs: GroundInputManifest = Field(..., description="Ground assumption manifest.")
    ground: GroundCostResult = Field(..., description="Ground cost result.")
    orbital_reference: OrbitalReferenceResult = Field(
        ..., description="Comparable orbital reference result."
    )
    comparison: GroundSpaceComparison = Field(..., description="Ground/orbit comparison.")
    meta: GroundOutputMetadata = Field(..., description="Cold-reader metadata.")


def _ground_spec(
    *,
    label: str,
    unit: str,
    rationale: str,
    claim_id: str,
    source_status: SourceStatus,
    notes: str | None = None,
) -> CellSpec:
    """Build one ground input's default-value source metadata.

    Every ground input cites its SOURCE_INDEX claim and the ground research
    note (:data:`GROUND_COST_RESEARCH_PATH`).
    """
    return CellSpec(
        label=label,
        unit=unit,
        role=AssumptionRole.DEFAULT,
        source_status=source_status,
        claim_id=claim_id,
        source_note=GROUND_SOURCE_NOTE,
        rationale=rationale,
        notes=notes,
        research_path=GROUND_COST_RESEARCH_PATH,
        research_note=GROUND_RESEARCH_NOTE,
    )


GROUND_INPUT_SPECS: Final[dict[str, CellSpec]] = {
    "gpu_package_cost_multiplier": _ground_spec(
        label="GPU package cost multiplier",
        unit="ratio",
        rationale="Uses the same GPU package cost basis as the orbital cohort.",
        claim_id=GROUND_GPU_PACKAGE_COST_BOUNDARY_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
        notes="A value of 1.0 means ground and orbital compute hardware share the same price.",
    ),
    "facility_shell_fitout_musd_per_mw": _ground_spec(
        label="Facility shell and fit-out",
        unit="MUSD/MW",
        rationale="Captures terrestrial building and AI-hall fit-out costs.",
        claim_id=GROUND_FACILITY_FITOUT_CLAIM_ID,
        source_status=SourceStatus.SOURCED_ESTIMATE,
    ),
    "racked_power_network_musd_per_gpu_package": _ground_spec(
        label="Racked power and networking",
        unit="MUSD/package",
        rationale="Captures non-GPU rack-side electrical and network integration.",
        claim_id=GROUND_RACKED_POWER_NETWORK_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
    ),
    "energy_price_usd_per_mwh": _ground_spec(
        label="Energy price",
        unit="USD/MWh",
        rationale=(
            "Turns IT load, PUE, and utilization into an energy cost over the comparison period."
        ),
        claim_id=GROUND_ENERGY_PRICE_CLAIM_ID,
        source_status=SourceStatus.SOURCED_ESTIMATE,
    ),
    "pue": _ground_spec(
        label="PUE",
        unit="ratio",
        rationale="Converts IT load into total facility electricity consumption.",
        claim_id=GROUND_PUE_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
    ),
    "utilization": _ground_spec(
        label="Utilization",
        unit="fraction",
        rationale="Energy cost scales with the average utilized IT load.",
        claim_id=GROUND_UTILIZATION_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
    ),
    "operations_maintenance_musd_per_mw_year": _ground_spec(
        label="Operations, maintenance, and labor",
        unit="MUSD/MW-year",
        rationale="Keeps recurring terrestrial support cost explicit.",
        claim_id=GROUND_OPERATIONS_MAINTENANCE_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
        notes="Labor is represented in this line rather than as a separate cost component.",
    ),
    "cooling_cost_musd_per_mw": _ground_spec(
        label="Cooling infrastructure",
        unit="MUSD/MW",
        rationale="Represents liquid-cooling and heat-rejection infrastructure.",
        claim_id=GROUND_COOLING_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
    ),
}
"""Default-value source metadata for each ground input, keyed by config field."""


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

    The file is read through the shared
    :func:`common.file_io.load_yaml_mapping`; an empty file takes every
    default.

    Args:
        path: Filesystem path to the ground-reference YAML scenario.

    Returns:
        A validated :class:`GroundReferenceConfig`.

    Raises:
        common.file_io.ModelFileError: If the file is missing, unreadable,
            malformed, or not a YAML mapping.
        pydantic.ValidationError: If the content is not a valid ground config.
    """
    return ground_config_from_dict(load_yaml_mapping(Path(path)))


def build_ground_reference_output(
    space_output: SpaceModelOutput,
    ground_config: GroundReferenceConfig,
    *,
    space_model_path: str,
    ground_scenario_path: str,
) -> GroundReferenceOutput:
    """Build the complete ground reference output for one space-model run.

    Args:
        space_output: Typed space model output that supplies the anchor-year
            deployed cohort (:func:`data_center.config.anchor_year` of its
            window) and, through its service life, the comparison period.
        ground_config: Validated ground-reference assumptions.
        space_model_path: Repository path of the space artifact
            ``space_output`` is (or will be) written to; recorded as
            ``anchor.space_model_path`` so ``space:`` uses resolve.
        ground_scenario_path: Repository path of the ground scenario YAML
            ``ground_config`` was loaded from; recorded in the metadata and
            the input manifest, and compared with the default ground
            scenario path to decide ``inputs.scenario.is_default``.

    Returns:
        A frozen :class:`GroundReferenceOutput` ready for JSON serialization.
    """
    inputs = _build_ground_input_manifest(
        ground_config=ground_config,
        source_scenario_path=ground_scenario_path,
    )
    anchor = _build_anchor(space_output, space_model_path)
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
        *_anchor_validation_results(anchor, space_output),
        *orbital_reference.warnings,
        *_comparison_scope_warnings(),
    ]
    metadata = _build_ground_metadata(space_output.metadata, ground_config, ground_scenario_path)
    meta = GroundOutputMetadata(
        data_dictionary=[],
        validation_results=validation_results,
        query_examples=_ground_query_examples(),
        source_status_summary=summarize_source_statuses(
            input_cell.source_status for input_cell in inputs.assumption_index.values()
        ),
        schema_version_notes=(
            f"ground-v1 reference output anchored to the {anchor.year} deployed-year "
            "space-model cohort over its service life; ground assumptions are "
            "source-status tagged through the research wiki source ledger. A 'uses' "
            f"entry prefixed '{SPACE_PATH_PREFIX}' resolves in the space artifact at "
            "anchor.space_model_path; every other entry resolves in this artifact."
        ),
    )
    output = GroundReferenceOutput(
        metadata=metadata,
        anchor=anchor,
        inputs=inputs,
        ground=ground,
        orbital_reference=orbital_reference,
        comparison=comparison,
        meta=meta,
    )
    return output.model_copy(
        update={"meta": meta.model_copy(update={"data_dictionary": build_data_dictionary(output)})}
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
    )


GROUND_ROLE_FOR_SPACE_ROLE: Final[dict[ArtifactRole, ArtifactRole]] = {
    ArtifactRole.DRAFT: ArtifactRole.DRAFT,
    ArtifactRole.PROMOTED_DEFAULT: ArtifactRole.PROMOTED_GROUND_DEFAULT,
    ArtifactRole.PROMOTED_NAMED: ArtifactRole.PROMOTED_GROUND_NAMED,
}
"""The ground artifact's role for each space artifact role it can be built from."""


def _build_ground_metadata(
    space_metadata: RunMetadata,
    ground_config: GroundReferenceConfig,
    ground_scenario_path: str,
) -> RunMetadata:
    """Build metadata for the ground artifact from the space run metadata.

    Args:
        space_metadata: The space artifact's metadata.
        ground_config: The ground assumptions (supplies the scenario name).
        ground_scenario_path: The ground scenario YAML actually loaded.

    Returns:
        The ground artifact's metadata.

    Raises:
        ValueError: If the space artifact already carries a ground role.
    """
    ground_role = GROUND_ROLE_FOR_SPACE_ROLE.get(space_metadata.artifact_role)
    if ground_role is None:
        raise ValueError(
            "a ground reference is built from a space artifact; got artifact_role="
            f"{space_metadata.artifact_role.value}"
        )
    return space_metadata.model_copy(
        update={
            "schema_version": GROUND_SCHEMA_VERSION,
            "scenario_name": ground_config.scenario_name,
            "artifact_role": ground_role,
            "source_scenario_path": ground_scenario_path,
        }
    )


def _build_ground_input_manifest(
    *,
    ground_config: GroundReferenceConfig,
    source_scenario_path: str,
) -> GroundInputManifest:
    """Build the ground-reference input manifest from a typed config.

    Uses the shared input-cell builders, so a ground input carries the same
    reference vocabulary as a space input, and a value that differs from the
    default ground config is published as a scenario override without the
    default's claim, research note, or rationale.
    """
    default = _default_ground_config()
    cells = {
        key: _spec_cell(
            f"inputs.config.{key}",
            getattr(ground_config, key),
            getattr(default, key),
            _field_description(GroundReferenceConfig, key),
            spec,
            source_scenario_path,
        )
        for key, spec in GROUND_INPUT_SPECS.items()
    }
    input_tree = GroundAssumptionInputTree(**cells)
    assumption_index = {InputPath(c.path): c for c in collect_input_cells(input_tree)}
    is_default = source_scenario_path == DEFAULT_GROUND_SCENARIO_PATH
    scenario = ScenarioIdentity(
        name=ground_config.scenario_name,
        description=(
            "Canonical default ground reference scenario for the promoted space model."
            if is_default
            else "User-supplied ground reference scenario."
        ),
        path=source_scenario_path,
        is_default=is_default,
        owner_note=(
            "Investor-selected ground reference assumptions traced to the research wiki."
            if is_default
            else None
        ),
    )
    return GroundInputManifest(
        scenario=scenario,
        config=input_tree,
        assumption_index=assumption_index,
    )


def _space_path(path: FieldPath) -> FieldPath:
    """Prefix a space-artifact path so a ground ``uses`` entry names its artifact."""
    return f"{SPACE_PATH_PREFIX}{path}"


def _anchor_space_sources(year: int) -> dict[AnchorQuantity, list[FieldPath]]:
    """Return the space cells (``space:``-prefixed) each anchor quantity is taken from.

    Nodes are the anchor year's deployed nodes; GPU packages and kW are those
    nodes times the year's per-node packages and power; the service life is
    the space run's dial.

    Args:
        year: The anchor year.

    Returns:
        The source paths per anchor quantity.
    """
    key = str(year)
    nodes = _space_path(f'business.years."{key}".nodes_deployed_this_year')
    return {
        AnchorQuantity.NODES: [nodes],
        AnchorQuantity.GPU_PACKAGES: [nodes, _space_path(f'physical.years."{key}".gpus_per_node')],
        AnchorQuantity.KW: [nodes, _space_path(f'physical.years."{key}".kw_per_node')],
        AnchorQuantity.SERVICE_LIFE_YEARS: [_space_path(SPACE_SERVICE_LIFE_PATH)],
    }


def _anchor_uses(anchor: GroundComparisonAnchor, quantity: AnchorQuantity) -> list[FieldPath]:
    """Cite one anchor quantity and the space cells it is taken from.

    The anchor's numeric fields are plain values, so a ground cell that reads
    one also cites its space sources; a space dial that moves the anchor
    cohort then reaches every ground cost built on it.
    """
    return [f"anchor.{quantity.value}", *_anchor_space_sources(anchor.year)[quantity]]


def _build_anchor(space_output: SpaceModelOutput, space_model_path: str) -> GroundComparisonAnchor:
    """Select the anchor-year deployed cohort from the typed space output.

    The anchor year is :func:`data_center.config.anchor_year` of the space
    run's window (the year-10 cadence anchor, or the final window year for a
    shorter horizon; FY2036 for the default), so it always exists in the
    space output. Per ADR-003 the anchor is the deployed-year cohort, never
    the living fleet. Its service life is the comparison period.
    """
    year = anchor_year(space_output.metadata.base_year, space_output.metadata.horizon_years)
    key = str(year)
    business_year = space_output.business.years[key]
    physical_year = space_output.physical.years[key]
    nodes = _int_cell_value(
        business_year.nodes_deployed_this_year,
        f'business.years."{key}".nodes_deployed_this_year',
    )
    gpus_per_node = _int_cell_value(
        physical_year.gpus_per_node,
        f'physical.years."{key}".gpus_per_node',
    )
    kw_per_node = _float_cell_value(physical_year.kw_per_node)
    service_life_years = _int_input_value(space_output.inputs.config.fleet.service_life_years)
    return GroundComparisonAnchor(
        space_model_path=space_model_path,
        year=year,
        basis=ANCHOR_BASIS,
        nodes=nodes,
        gpu_packages=nodes * gpus_per_node,
        kw=nodes * kw_per_node,
        service_life_years=service_life_years,
        note=ANCHOR_NOTE,
        source_paths=list(
            dict.fromkeys(path for paths in _anchor_space_sources(year).values() for path in paths)
        ),
    )


def _build_ground_cost_result(
    anchor: GroundComparisonAnchor,
    space_output: SpaceModelOutput,
    inputs: GroundInputManifest,
) -> GroundCostResult:
    """Compute the ground cost of the anchor cohort over its service life."""
    component_costs = _ground_components(anchor, space_output, inputs)
    included = [
        (index, component) for index, component in enumerate(component_costs) if component.included
    ]
    total = _total_cell(
        value=sum(_float_cell_value(component.cost) for _, component in included),
        uses=[f"ground.component_costs[{index}].cost" for index, _ in included],
        description="Total ground cost for the anchor cohort over the comparison period.",
    )
    period = float(anchor.service_life_years)
    annualized = _provenance_cell(
        value=_safe_ratio(_float_cell_value(total), period),
        unit="MUSD/year",
        formula_name="annualized_cost_from_total_and_period",
        uses=[
            "ground.total_five_year_cost",
            *_anchor_uses(anchor, AnchorQuantity.SERVICE_LIFE_YEARS),
        ],
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
            uses=[
                "ground.total_five_year_cost",
                *_anchor_uses(anchor, AnchorQuantity.GPU_PACKAGES),
            ],
            description="Ground cost per GPU package over the comparison period.",
        ),
        cost_per_mw_five_year=_cost_per_unit_cell(
            value=_safe_ratio(_float_cell_value(total), anchor_mw),
            unit="MUSD/MW",
            uses=["ground.total_five_year_cost", *_anchor_uses(anchor, AnchorQuantity.KW)],
            description="Ground cost per MW over the comparison period.",
        ),
        included_components=[
            "GPU/package acquisition",
            "facility shell or fit-out allocation",
            "racked power and networking",
            "energy over the comparison period with PUE and utilization",
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
        warnings=[],
    )


def _ground_components(
    anchor: GroundComparisonAnchor,
    space_output: SpaceModelOutput,
    inputs: GroundInputManifest,
) -> list[CostComponent]:
    """Build all included ground cost components."""
    key = str(anchor.year)
    physical_year = space_output.physical.years[key]
    compute_cost_per_node = _float_cell_value(physical_year.cost_breakdown.compute)
    gpus_per_node = _float_cell_value(physical_year.gpus_per_node)
    package_cost_musd = _required_ratio(
        compute_cost_per_node,
        gpus_per_node,
        f'physical.years."{key}".gpus_per_node',
    )
    gpu_packages = float(anchor.gpu_packages)
    anchor_mw = float(anchor.kw) / KW_PER_MW
    period = float(anchor.service_life_years)
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
                    *_anchor_uses(anchor, AnchorQuantity.GPU_PACKAGES),
                    _space_path(f'physical.years."{key}".cost_breakdown.compute'),
                    _space_path(f'physical.years."{key}".gpus_per_node'),
                    "inputs.config.gpu_package_cost_multiplier",
                ],
                sources=[GROUND_GPU_PACKAGE_COST_BOUNDARY_CLAIM_ID],
                source_status=SourceStatus.DERIVED_ESTIMATE,
                description="Ground acquisition cost for the same GPU package count.",
            ),
            source_paths=[
                "anchor.gpu_packages",
                _space_path(f'physical.years."{key}".cost_breakdown.compute'),
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
                uses=[
                    *_anchor_uses(anchor, AnchorQuantity.KW),
                    "inputs.config.facility_shell_fitout_musd_per_mw",
                ],
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
                    *_anchor_uses(anchor, AnchorQuantity.GPU_PACKAGES),
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
            label="Energy over the comparison period",
            cost=_provenance_cell(
                value=energy_musd,
                unit="MUSD",
                formula_name="ground_energy_cost_from_kw_pue_utilization",
                uses=[
                    *_anchor_uses(anchor, AnchorQuantity.KW),
                    "inputs.config.energy_price_usd_per_mwh",
                    "inputs.config.pue",
                    "inputs.config.utilization",
                    *_anchor_uses(anchor, AnchorQuantity.SERVICE_LIFE_YEARS),
                ],
                sources=[
                    GROUND_ENERGY_PRICE_CLAIM_ID,
                    GROUND_PUE_CLAIM_ID,
                    GROUND_UTILIZATION_CLAIM_ID,
                    GROUND_COST_RESEARCH_PATH,
                ],
                source_status=SourceStatus.DERIVED_ESTIMATE,
                description=(
                    "Electricity cost over the comparison period using PUE and utilization."
                ),
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
                uses=[
                    *_anchor_uses(anchor, AnchorQuantity.KW),
                    "inputs.config.cooling_cost_musd_per_mw",
                ],
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
                    *_anchor_uses(anchor, AnchorQuantity.KW),
                    "inputs.config.operations_maintenance_musd_per_mw_year",
                    *_anchor_uses(anchor, AnchorQuantity.SERVICE_LIFE_YEARS),
                ],
                sources=[GROUND_OPERATIONS_MAINTENANCE_CLAIM_ID],
                source_status=SourceStatus.DERIVED_ESTIMATE,
                description=(
                    "Operations, maintenance, and labor allocation over the comparison period."
                ),
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
    """Mirror the space model's anchor-year build and launch components."""
    key = str(anchor.year)
    physical_year = space_output.physical.years[key]
    breakdown = physical_year.cost_breakdown
    component_costs = [
        _orbital_component("compute", "Compute hardware", breakdown.compute, anchor),
        _orbital_component("bus", "Bus/platform", breakdown.bus, anchor),
        _orbital_component("solar", "Solar/power", breakdown.solar, anchor),
        _orbital_component("radiator", "Radiator/thermal", breakdown.radiator, anchor),
        _orbital_component("launch", "Launch allocation", breakdown.launch, anchor),
    ]
    total = _provenance_cell(
        value=sum(_float_cell_value(component.cost) for component in component_costs),
        unit="MUSD",
        formula_name="orbital_total_cost_from_space_node_total",
        uses=[
            f"orbital_reference.component_costs[{index}].cost"
            for index in range(len(component_costs))
        ],
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
            uses=[
                "orbital_reference.five_year_cost_view",
                *_anchor_uses(anchor, AnchorQuantity.GPU_PACKAGES),
            ],
            description="Orbital reference cost per GPU package over the comparison period.",
        ),
        cost_per_mw_five_year=_cost_per_unit_cell(
            value=_safe_ratio(_float_cell_value(total), anchor_mw),
            unit="MUSD/MW",
            uses=[
                "orbital_reference.five_year_cost_view",
                *_anchor_uses(anchor, AnchorQuantity.KW),
            ],
            description="Orbital reference cost per MW over the comparison period.",
        ),
        kw=_provenance_cell(
            value=anchor.kw,
            unit="kW",
            formula_name="kw_deployed_this_year_from_nodes",
            uses=[
                _space_path(f'business.years."{key}".nodes_deployed_this_year'),
                _space_path(f'physical.years."{key}".kw_per_node'),
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
                _space_path(f'business.years."{key}".nodes_deployed_this_year'),
                _space_path(f'physical.years."{key}".gpus_per_node'),
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
            description="Ground total minus orbital reference total over the comparison period.",
        ),
        ground_to_orbit_ratio=_ratio_cell(
            value=ratio,
            uses=["ground.total_five_year_cost", "orbital_reference.five_year_cost_view"],
            description="Ground total divided by orbital reference total.",
        ),
        orbit_to_ground_ratio=_ratio_cell(
            value=_safe_ratio(orbital_total, ground_total),
            uses=["orbital_reference.five_year_cost_view", "ground.total_five_year_cost"],
            description="Orbital reference total divided by ground total.",
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
    name: str, label: str, per_node_cost: ProvenanceCell, anchor: GroundComparisonAnchor
) -> CostComponent:
    """Build one orbital reference component from a per-node space cell.

    The component is the anchor year's per-node space cell times the anchor
    cohort's nodes, and cites both.
    """
    anchor_key = str(anchor.year)
    return CostComponent(
        name=name,
        label=label,
        cost=_provenance_cell(
            value=_float_cell_value(per_node_cost) * float(anchor.nodes),
            unit="MUSD",
            formula_name="orbital_component_cost_from_space_node_component",
            uses=[
                _space_path(f'physical.years."{anchor_key}".cost_breakdown.{name}'),
                *_anchor_uses(anchor, AnchorQuantity.NODES),
            ],
            sources=per_node_cost.sources,
            source_status=per_node_cost.source_status,
            description=f"Anchor-cohort orbital {label.lower()} cost.",
        ),
        included=True,
        source_paths=[_space_path(f'physical.years."{anchor_key}".cost_breakdown.{name}')],
        notes="Mirrors the promoted space model's per-node component.",
    )


@dataclass(frozen=True)
class _CitedCell:
    """A cost cell together with its path in the ground artifact."""

    path: FieldPath
    cell: ProvenanceCell


def _component_deltas(
    ground: GroundCostResult, orbital_reference: OrbitalReferenceResult
) -> list[ComponentDelta]:
    """Build grouped component deltas that keep unlike line items legible.

    A grouped subtotal cites the component cells it sums by their paths in
    this artifact; a delta or ratio cites its own group's two cost cells.
    """
    ground_cells = {
        component.name: _CitedCell(f"ground.component_costs[{index}].cost", component.cost)
        for index, component in enumerate(ground.component_costs)
    }
    orbital_cells = {
        component.name: _CitedCell(
            f"orbital_reference.component_costs[{index}].cost", component.cost
        )
        for index, component in enumerate(orbital_reference.component_costs)
    }
    groups: list[tuple[str, ProvenanceCell, ProvenanceCell, str]] = [
        (
            "compute",
            ground_cells["gpu_package_acquisition"].cell,
            orbital_cells["compute"].cell,
            "Compares like-for-like GPU/package acquisition.",
        ),
        (
            "platform_vs_facility",
            _sum_group_cell(
                name="ground facility plus rack infrastructure",
                costs=[
                    ground_cells["facility_shell_fitout"],
                    ground_cells["racked_power_networking"],
                ],
            ),
            orbital_cells["bus"].cell,
            "Compares terrestrial facility/rack integration against orbital bus.",
        ),
        (
            "power_thermal_operations",
            _sum_group_cell(
                name="ground energy plus cooling plus operations",
                costs=[
                    ground_cells["energy"],
                    ground_cells["cooling"],
                    ground_cells["operations_maintenance_labor"],
                ],
            ),
            _sum_group_cell(
                name="orbital solar plus radiator",
                costs=[orbital_cells["solar"], orbital_cells["radiator"]],
            ),
            "Compares terrestrial recurring support against orbital power/thermal capex.",
        ),
        (
            "launch",
            _provenance_cell(
                value=ZERO_COST,
                unit="MUSD",
                formula_name="explicit_zero_cost_for_excluded_component",
                uses=[],
                sources=["ground reference explicit non-applicability"],
                source_status=SourceStatus.SCENARIO,
                description="Ground launch cost is not applicable.",
            ),
            orbital_cells["launch"].cell,
            "Launch is an orbital-only cost line.",
        ),
    ]
    return [
        _component_delta(
            index=index,
            name=name,
            ground_cost=ground_cost,
            orbital_cost=orbital_cost,
            notes=notes,
        )
        for index, (name, ground_cost, orbital_cost, notes) in enumerate(groups)
    ]


def _component_delta(
    *,
    index: int,
    name: str,
    ground_cost: ProvenanceCell,
    orbital_cost: ProvenanceCell,
    notes: str,
) -> ComponentDelta:
    """Build one component delta, published at ``comparison.component_deltas[index]``."""
    ground_value = _float_cell_value(ground_cost)
    orbital_value = _float_cell_value(orbital_cost)
    delta_path = f"comparison.component_deltas[{index}]"
    pair_uses = [f"{delta_path}.ground_cost", f"{delta_path}.orbital_reference_cost"]
    return ComponentDelta(
        name=name,
        ground_cost=ground_cost,
        orbital_reference_cost=orbital_cost,
        absolute_delta=_delta_cell(
            value=ground_value - orbital_value,
            uses=pair_uses,
            description=f"Ground minus orbital cost for {name}.",
        ),
        ground_to_orbit_ratio=_ratio_cell(
            value=_safe_ratio(ground_value, orbital_value),
            uses=pair_uses,
            description=f"Ground/orbital ratio for {name}.",
        ),
        notes=notes,
    )


def _sum_group_cell(name: str, costs: list[_CitedCell]) -> ProvenanceCell:
    """Build a provenance cell for a grouped component subtotal.

    Args:
        name: Plain-language name of the group.
        costs: The component cells summed, each with its path.

    Returns:
        The subtotal cell, citing each summed component by path.
    """
    return _provenance_cell(
        value=sum(_float_cell_value(cost.cell) for cost in costs),
        unit="MUSD",
        formula_name="total_cost_from_components",
        uses=[cost.path for cost in costs],
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
    """Build a provenance cell with source status and notes (repeated uses dropped)."""
    built = cell(
        value=value,
        unit=unit,
        formula_name=formula_name,
        uses=list(dict.fromkeys(uses)),
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


def _anchor_validation_results(
    anchor: GroundComparisonAnchor, space_output: SpaceModelOutput
) -> list[ValidationResult]:
    """Check the anchor against the space output it was taken from.

    The expected year is the space run's own anchor year
    (:func:`data_center.config.anchor_year` of its window); the expected
    cohort is that year's deployed-year cells in the space output: the
    node count, the deployed kW (an independent cell, so a disagreement in
    the node-power product shows), the GPU packages (nodes x packages per
    node), and the service life that sets the comparison period.

    Args:
        anchor: The ground artifact's anchor.
        space_output: The space output the ground reference was built from.

    Returns:
        One result, ``pass`` when every anchor field matches the space
        output, else ``fail`` naming the observed values.
    """
    md = space_output.metadata
    expected_year = anchor_year(md.base_year, md.horizon_years)
    key = str(expected_year)
    business_year = space_output.business.years[key]
    physical_year = space_output.physical.years[key]
    space_nodes = _int_cell_value(
        business_year.nodes_deployed_this_year,
        f'business.years."{key}".nodes_deployed_this_year',
    )
    space_packages = space_nodes * _int_cell_value(
        physical_year.gpus_per_node, f'physical.years."{key}".gpus_per_node'
    )
    space_kw = _float_cell_value(business_year.kw_deployed_this_year)
    space_life = _int_input_value(space_output.inputs.config.fleet.service_life_years)
    passed = (
        anchor.year == expected_year
        and anchor.basis == ANCHOR_BASIS
        and anchor.nodes == space_nodes
        and anchor.gpu_packages == space_packages
        and math.isclose(anchor.kw, space_kw, rel_tol=ANCHOR_KW_RELATIVE_TOLERANCE)
        and anchor.service_life_years == space_life
    )
    observed = (
        f"year={anchor.year}; basis={anchor.basis}; nodes={anchor.nodes} "
        f"(space {space_nodes}); gpu_packages={anchor.gpu_packages} "
        f"(space {space_packages}); kw={anchor.kw:g} (space {space_kw:g}); "
        f"service_life_years={anchor.service_life_years} (space {space_life})."
    )
    return [
        ValidationResult(
            validation_id=f"ground_anchor_{expected_year}_deployed_year",
            severity=ValidationSeverity.OK if passed else ValidationSeverity.FAIL,
            what_tested=("The ground anchor is the space run's anchor-year deployed-year cohort."),
            expected_condition=(
                f"year={expected_year}, basis={ANCHOR_BASIS}, and nodes, GPU packages, "
                "kW, and service life equal the space output's anchor-year cohort."
            ),
            observed_result=observed,
            related_json_paths=["anchor.year", "anchor.basis", *anchor.source_paths],
            remediation_hint=(
                None if passed else "Rebuild the ground reference from the space output it cites."
            ),
        )
    ]


def _conclusion_label(ratio: float | None) -> GroundConclusionLabel:
    """Choose a plain conclusion label for the comparison result."""
    if ratio is None:
        raise ValueError("ground/orbital ratio must be computable to label the comparison")
    if ratio < GROUND_MATERIALLY_CHEAPER_RATIO:
        return GroundConclusionLabel.GROUND_CHEAPER
    if ratio > ORBITAL_MATERIALLY_CHEAPER_RATIO:
        return GroundConclusionLabel.ORBITAL_CHEAPER
    return GroundConclusionLabel.SAME_ORDER


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
            question_answered=(
                "What are the total ground and orbital costs over the comparison period?"
            ),
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


def _int_cell_value(cell_value: ProvenanceCell, path: str) -> int:
    """Return a provenance cell's integer value (a count such as nodes).

    Raises:
        ValueError: If the cell does not hold an integer.
    """
    value = cell_value.value
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{path} is not an integer count: {value!r}")
    return value


def _int_input_value(cell_value: InputCell) -> int:
    """Return an input cell's integer value (such as the service life).

    Raises:
        ValueError: If the cell does not hold an integer.
    """
    value = cell_value.value
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{cell_value.path} is not an integer: {value!r}")
    return value


def _float_cell_value(cell_value: ProvenanceCell) -> float:
    """Return a provenance cell's numeric value as ``float``.

    Raises:
        ValueError: If the cell does not hold a number.
    """
    value = cell_value.value
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{cell_value.description} is not numeric: {value!r}")
    return float(value)


def _float_input_value(cell_value: InputCell) -> float:
    """Return an input cell's numeric value as ``float``.

    Raises:
        ValueError: If the cell does not hold a number.
    """
    value = cell_value.value
    if isinstance(value, (bool, str, list)):
        raise ValueError(f"{cell_value.path} is not numeric: {value!r}")
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
    "DEFAULT_GROUND_SCENARIO_PATH",
    "GroundReferenceConfig",
    "GroundReferenceOutput",
    "build_ground_reference_output",
    "ground_config_from_dict",
    "load_ground_config",
    "render_ground_json",
]
