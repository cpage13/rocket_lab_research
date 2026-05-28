"""v8 ``ValuationOutput`` — the cycle-2 output JSON schema.

This module is the single source of truth for the shape of the
``rklb-value <scenario> --json`` artifact. The v8 schema is a clean break
from the cycle-1 v7 shape (D24, no back-compat shim). The top-level
structure has exactly five keys (D21):

* ``metadata`` — the run's identity (schema version, base year, horizon,
  the three founder-locked enums, generated-at timestamp).
* ``inputs`` — the gospel anchors, the post-Feynman slopes, and the v8
  dial blocks (cadence / fleet / volume / R-band / launch-cost) plus the
  per-generation list.
* ``physical`` — the per-year per-node trajectory, each leaf wrapped in a
  :class:`data_center.provenance.ProvenanceCell`.
* ``business`` — the per-year living-fleet rollup, each leaf a
  ProvenanceCell. The cycle-1 ``summary`` block is dropped; its content
  lives here in ``business.years``.
* ``meta`` — the engine-computed validation report, the introspection-built
  data dictionary, the per-generation summary, and the ``query_examples``
  block (the cold-reader contract).

Every BaseModel here is ``model_config = ConfigDict(frozen=True)`` — the
output is immutable once built; downstream renderers and serializers may
read but not mutate.

Per-year data is keyed by a JSON-string year (``YearString``, e.g.
``"2036"``) in ``PhysicalBlock.years`` / ``BusinessBlock.years`` — this is
what a cold agent's ``jq`` queries address (``.physical.years."2036"``).

``ValidationCheck`` / ``Severity`` are the cycle-1 types, reused verbatim
for V1–V17 — cycle 2 does **not** define a new validation type.

References:
    strategy_05_20_cycle2.md § 3 — the v8 schema.
    plan_05_20_cycle2.md § 5 T50 — the v8 ``ValuationOutput`` sketch.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from data_center.config import (
    OperatorModel,
    RadiatorArchitecture,
    WorkloadType,
)
from data_center.constants import MAX_FY, MAX_HORIZON_YEARS, MIN_FY, MIN_HORIZON_YEARS
from data_center.input_manifest import InputManifest
from data_center.provenance import FieldPath, ProvenanceCell, YearString

# The v8 output JSON schema version. A bare constant — the single place the
# schema-version string is defined.
SCHEMA_VERSION: str = "v8"

# ---------------------------------------------------------------------------
# Enums (cycle-1 types — reused verbatim)
# ---------------------------------------------------------------------------


class FieldKind(StrEnum):
    """The semantic kind of one leaf field in the output JSON.

    Used in the ``data_dictionary`` so a reader knows what a number *is* —
    a dial they set (``INPUT``), a model constant (``CONSTANT``), a level
    prevailing in a year (``STATE``), a per-year flow (``FLOW``), a running
    total (``STOCK``), or a function of other fields (``DERIVED``).
    """

    INPUT = "input"
    CONSTANT = "constant"
    STATE = "state"
    FLOW = "flow"
    STOCK = "stock"
    DERIVED = "derived"


class Severity(StrEnum):
    """Severity tier for a :class:`ValidationCheck`.

    ``CRITICAL`` — model is invalid; do not quote.
    ``MAJOR`` — a substantive defect that affects the headline.
    ``MINOR`` — a soft check (range warning, secondary metric).
    """

    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"


class ValidationSeverity(StrEnum):
    """Public validation severity emitted in ``meta.validation_results``."""

    OK = "pass"
    WARN = "warn"
    FAIL = "fail"


class QueryAppliesTo(StrEnum):
    """Which public model family a query example applies to."""

    SPACE = "space"
    GROUND = "ground"
    BOTH = "both"


class SourceStatusSummary(BaseModel):
    """Known-shape count of input assumptions by source-status value."""

    model_config = ConfigDict(frozen=True)

    certified: int = Field(..., description="Certified source-backed input count.")
    sourced_estimate: int = Field(..., description="Sourced-estimate input count.")
    derived_estimate: int = Field(..., description="Derived-estimate input count.")
    projection: int = Field(..., description="Projection input count.")
    extrapolation: int = Field(..., description="Extrapolation input count.")
    scenario: int = Field(..., description="Scenario-authored input count.")
    placeholder: int = Field(
        ..., description="Placeholder input count; must be zero in promoted artifacts."
    )
    stale: int = Field(
        ..., description="Stale-source input count; must be zero in promoted artifacts."
    )


# ---------------------------------------------------------------------------
# Run metadata block
# ---------------------------------------------------------------------------


class RunMetadata(BaseModel):
    """The ``metadata`` block — the run's identity.

    Carries the v8 schema version, the base year + horizon, the three
    founder-locked enums (workload / operator / radiator architecture),
    the deployment philosophy, and an ISO-8601 generated-at timestamp.
    The enum locks + base year + horizon mirror
    :class:`data_center.config.MetadataConfig`; ``schema_version`` and
    ``generated_at`` are added at output-build time.
    """

    model_config = ConfigDict(frozen=True)

    schema_version: str = Field(
        ...,
        description="The output JSON schema version (e.g. 'v8').",
    )
    scenario_name: str = Field(
        ...,
        description="Human-readable scenario label from the YAML config.",
    )
    base_year: int = Field(
        ...,
        description="Calendar year corresponding to model year 0.",
        ge=MIN_FY,
        le=MAX_FY,
    )
    horizon_years: int = Field(
        ...,
        description=(
            "Number of fiscal-year steps after year 0; the physical / "
            "business 'years' maps have 'horizon_years + 1' entries."
        ),
        ge=MIN_HORIZON_YEARS,
        le=MAX_HORIZON_YEARS,
    )
    workload_type: WorkloadType = Field(
        ...,
        description="The compute workload the data centre serves (D14).",
    )
    operator_model: OperatorModel = Field(
        ...,
        description="The commercial operating model (D15).",
    )
    radiator_architecture: RadiatorArchitecture = Field(
        ...,
        description="The radiator mounting architecture (D16).",
    )
    deployment_philosophy: str = Field(
        ...,
        description="The deployment philosophy (e.g. 'ground_validated_before_launch').",
    )
    generated_at: str = Field(
        ...,
        description="ISO-8601 UTC timestamp at which the artifact was generated.",
    )
    model_package: str | None = Field(
        ...,
        description="Python package name that generated the artifact, when known.",
    )
    model_version: str | None = Field(
        ...,
        description="Installed model package version, when available.",
    )
    artifact_role: str = Field(
        ...,
        description="Artifact role such as draft, promoted_default, or promoted_named.",
    )
    source_scenario_path: str = Field(
        ...,
        description="Repository-relative source scenario path.",
    )


# ---------------------------------------------------------------------------
# Validation — cycle-1 ValidationCheck reused verbatim (no VRuleResult)
# ---------------------------------------------------------------------------


class ValidationCheck(BaseModel):
    """One engine-computed sanity check on the run.

    The cycle-1 validation type, reused verbatim for V1–V17. The
    ``meta.validation.rules`` block lets a reader run
    ``jq '.meta.validation.rules[] | select(.pass_check == false)'`` and
    see every failed check without reading the engine.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(
        ...,
        description="Short identifier for the check (e.g. 'mass_util_in_range').",
    )
    what_it_tests: str = Field(
        ...,
        description="One-sentence statement of what the check ensures.",
    )
    expected: str = Field(
        ...,
        description=("Human-readable expected value or range, e.g. 'in [0.85, 1.0]' or '> 0'."),
    )
    computed: str = Field(
        ...,
        description="Human-readable computed value as a formatted string.",
    )
    pass_check: bool = Field(
        ...,
        description="Whether the check passed (computed satisfies expected).",
    )
    severity: Severity = Field(
        ...,
        description="Severity tier if the check failed (CRITICAL / MAJOR / MINOR).",
    )


class ValidationReport(BaseModel):
    """The ``meta.validation`` block — the full V-rule result list.

    A thin container so the validation block has a stable ``rules`` key
    a reader can address (``.meta.validation.rules[]``).
    """

    model_config = ConfigDict(frozen=True)

    rules: list[ValidationCheck] = Field(
        ...,
        description=(
            "All V-rule results in declaration order (V1..V17). Run "
            "`jq '.meta.validation.rules[] | select(.pass_check==false)'` "
            "to find any failure."
        ),
    )


# ---------------------------------------------------------------------------
# Inputs block
# ---------------------------------------------------------------------------


InputsBlock = InputManifest
"""Compatibility name for the Phase-2 ``InputManifest`` public input block."""


# ---------------------------------------------------------------------------
# Per-year blocks — physical (per-node) and business (fleet)
# ---------------------------------------------------------------------------


class CostBreakdownBlock(BaseModel):
    """The per-node cost decomposition — the five build/launch lines + total.

    Surfaces the cost intermediates the engine's
    :class:`data_center.engine.CostBreakdown` computes, so a cold agent can
    query the cost decomposition (and ``cost_annual_per_node_musd`` has real
    cells to cite in its ``uses``). Every field is a :class:`ProvenanceCell`.
    """

    model_config = ConfigDict(frozen=True)

    compute: ProvenanceCell = Field(
        ...,
        description="Per-node compute build cost — all packages, $M.",
    )
    bus: ProvenanceCell = Field(
        ...,
        description="Per-node bus build cost — declines then flattens (D12), $M.",
    )
    solar: ProvenanceCell = Field(
        ...,
        description="Per-node solar-array build cost, $M.",
    )
    radiator: ProvenanceCell = Field(
        ...,
        description="Per-node radiator build cost, $M.",
    )
    launch: ProvenanceCell = Field(
        ...,
        description="Per-node launch cost — cadence-indexed, $M.",
    )
    node_total: ProvenanceCell = Field(
        ...,
        description="Total per-node build + launch cost — sum of the five lines, $M.",
    )


class PhysicalYear(BaseModel):
    """One model year's per-node physical + per-node economics state.

    Every field is a :class:`ProvenanceCell` — value plus the formula,
    units, upstream paths, and sources that produced it — except
    ``cost_breakdown``, which is a :class:`CostBreakdownBlock` of six cells.
    The per-node revenue / gross-profit lines are split into explicit
    ``_central`` / ``_low`` / ``_high`` fields (one per R-band trajectory)
    — the cycle-1 ``annual_rev_per_node_musd`` field (which conflated
    revenue and profit) is gone (D25).
    """

    model_config = ConfigDict(frozen=True)

    year: int = Field(
        ...,
        description="Calendar year for this physical record.",
    )
    frontier_generation: ProvenanceCell = Field(
        ...,
        description="The frontier GPU generation chosen for this year.",
    )
    gpus_per_node: ProvenanceCell = Field(
        ...,
        description="Packages per node this year (the mass-bound N).",
    )
    kw_per_node: ProvenanceCell = Field(
        ...,
        description="Total node electrical power, kW.",
    )
    mass_per_node_t: ProvenanceCell = Field(
        ...,
        description="Total flown node mass, tonnes.",
    )
    solar_area_per_pkg_m2: ProvenanceCell = Field(
        ...,
        description="Solar collector area per package, m2.",
    )
    volume_per_pkg_m3: ProvenanceCell = Field(
        ...,
        description="Stowed volume per package, m3.",
    )
    volume_per_node_m3: ProvenanceCell = Field(
        ...,
        description="Total node stowed volume, m3.",
    )
    mass_utilization_pct: ProvenanceCell = Field(
        ...,
        description="Mass utilization, percent of the Neutron mass envelope.",
    )
    volume_utilization_pct: ProvenanceCell = Field(
        ...,
        description="Volume utilization, percent of the Neutron fairing volume.",
    )
    binding_constraint: ProvenanceCell = Field(
        ...,
        description="Which envelope (mass / volume / both / neither) binds N.",
    )
    pf_per_node: ProvenanceCell = Field(
        ...,
        description="Total node compute, dense-FP4 PFLOPS.",
    )
    pf_per_kw: ProvenanceCell = Field(
        ...,
        description="Compute density, PFLOPS per node kW.",
    )
    cost_breakdown: CostBreakdownBlock = Field(
        ...,
        description="Per-node cost decomposition — the five build/launch lines + total.",
    )
    cost_annual_per_node_musd: ProvenanceCell = Field(
        ...,
        description="Annualized cost per node over the service life, $M/yr.",
    )
    revenue_annual_per_node_musd_central: ProvenanceCell = Field(
        ...,
        description="Annual revenue per node at central R, $M/yr.",
    )
    revenue_annual_per_node_musd_low: ProvenanceCell = Field(
        ...,
        description="Annual revenue per node at low R, $M/yr.",
    )
    revenue_annual_per_node_musd_high: ProvenanceCell = Field(
        ...,
        description="Annual revenue per node at high R, $M/yr.",
    )
    gross_profit_annual_per_node_musd_central: ProvenanceCell = Field(
        ...,
        description="Annual gross profit per node at central R, $M/yr.",
    )
    gross_profit_annual_per_node_musd_low: ProvenanceCell = Field(
        ...,
        description="Annual gross profit per node at low R, $M/yr.",
    )
    gross_profit_annual_per_node_musd_high: ProvenanceCell = Field(
        ...,
        description="Annual gross profit per node at high R, $M/yr.",
    )


class BusinessYear(BaseModel):
    """One model year's living-fleet rollup.

    Every field is a :class:`ProvenanceCell`. The fleet revenue / gross
    profit / margin lines are split into explicit ``_central`` / ``_low``
    / ``_high`` fields (one per R-band trajectory). This block carries
    what the cycle-1 ``summary`` block used to surface — but per-year,
    where it belongs.
    """

    model_config = ConfigDict(frozen=True)

    year: int = Field(
        ...,
        description="Calendar year for this business record.",
    )
    launches: ProvenanceCell = Field(
        ...,
        description="Whole-number launches in this calendar year (rounded logistic cadence ramp).",
    )
    nodes_deployed_this_year: ProvenanceCell = Field(
        ...,
        description="Nodes deployed this year (1 node per launch, D8).",
    )
    living_fleet: ProvenanceCell = Field(
        ...,
        description="Living fleet count under the 5-year hard cliff (D1).",
    )
    kw_deployed_this_year: ProvenanceCell = Field(
        ...,
        description="Newly deployed node power in this year, kW.",
    )
    kw_living_fleet: ProvenanceCell = Field(
        ...,
        description="Living-fleet node power in this year, kW.",
    )
    kw_on_orbit: ProvenanceCell = Field(
        ...,
        description="Total kW on orbit (living fleet).",
    )
    pf_deployed_this_year: ProvenanceCell = Field(
        ...,
        description="Newly deployed node compute in this year, PFLOPS.",
    )
    pf_living_fleet: ProvenanceCell = Field(
        ...,
        description="Living-fleet node compute in this year, PFLOPS.",
    )
    pf_on_orbit: ProvenanceCell = Field(
        ...,
        description="Total PFLOPS on orbit (living fleet).",
    )
    launch_cost_this_year_musd: ProvenanceCell = Field(
        ...,
        description="Per-launch cost at this year's cadence, $M.",
    )
    cost_annual_fleet_musd: ProvenanceCell = Field(
        ...,
        description="Fleet annual cost (cohort-vintaged), $M.",
    )
    revenue_annual_fleet_musd_central: ProvenanceCell = Field(
        ...,
        description="Fleet annual revenue at central R, $M.",
    )
    revenue_annual_fleet_musd_low: ProvenanceCell = Field(
        ...,
        description="Fleet annual revenue at low R, $M.",
    )
    revenue_annual_fleet_musd_high: ProvenanceCell = Field(
        ...,
        description="Fleet annual revenue at high R, $M.",
    )
    revenue_cumulative_musd_central: ProvenanceCell = Field(
        ...,
        description="Cumulative fleet revenue base-year through this year, central R, $M.",
    )
    revenue_cumulative_musd_low: ProvenanceCell = Field(
        ...,
        description="Cumulative fleet revenue base-year through this year, low R, $M.",
    )
    revenue_cumulative_musd_high: ProvenanceCell = Field(
        ...,
        description="Cumulative fleet revenue base-year through this year, high R, $M.",
    )
    gross_profit_annual_fleet_musd_central: ProvenanceCell = Field(
        ...,
        description="Fleet annual gross profit at central R, $M.",
    )
    gross_profit_annual_fleet_musd_low: ProvenanceCell = Field(
        ...,
        description="Fleet annual gross profit at low R, $M.",
    )
    gross_profit_annual_fleet_musd_high: ProvenanceCell = Field(
        ...,
        description="Fleet annual gross profit at high R, $M.",
    )
    margin_central_pct: ProvenanceCell = Field(
        ...,
        description="Fleet gross margin at central R, percent.",
    )
    margin_low_pct: ProvenanceCell = Field(
        ...,
        description="Fleet gross margin at low R, percent.",
    )
    margin_high_pct: ProvenanceCell = Field(
        ...,
        description="Fleet gross margin at high R, percent.",
    )


class PhysicalBlock(BaseModel):
    """The ``physical`` block — the per-year per-node trajectory.

    ``years`` is keyed by JSON-string year (``"2026"`` .. ``"2036"``);
    a cold agent addresses one year as ``.physical.years."2036"``.
    """

    model_config = ConfigDict(frozen=True)

    years: dict[YearString, PhysicalYear] = Field(
        ...,
        description="Per-year per-node trajectory, keyed by JSON-string fiscal year.",
    )


class BusinessBlock(BaseModel):
    """The ``business`` block — the per-year living-fleet rollup.

    ``years`` is keyed by JSON-string year; a cold agent addresses one
    year as ``.business.years."2036"``.
    """

    model_config = ConfigDict(frozen=True)

    years: dict[YearString, BusinessYear] = Field(
        ...,
        description="Per-year fleet rollup, keyed by JSON-string fiscal year.",
    )


# ---------------------------------------------------------------------------
# Meta block — validation, data dictionary, generation summary, query examples
# ---------------------------------------------------------------------------


class DataDictEntry(BaseModel):
    """One ``data_dictionary`` entry — the meaning of a single output field.

    Built by the ``build_data_dictionary`` helper from typed-model
    field-info introspection.
    """

    model_config = ConfigDict(frozen=True)

    path: FieldPath = Field(
        ...,
        description="Public JSON path this dictionary entry describes.",
    )
    description: str = Field(
        ...,
        description="One-sentence plain-English description of the field.",
    )
    unit: str = Field(
        ...,
        description=(
            "Unit string, e.g. 'MUSD', 'kW', 't', 'count', 'percent', or '-' for a unitless value."
        ),
    )
    type: str = Field(
        ...,
        description="The leaf value's wire type (e.g. 'number', 'integer', 'string').",
    )
    source_class: str = Field(
        ...,
        description=("Provenance class of the field — INPUT / CONSTANT / DERIVED."),
    )


class GenerationSummary(BaseModel):
    """One entry of the ``meta.generations_dictionary`` — a compact gen view.

    A flattened, render-friendly view of one GPU generation: the headline
    per-package physical + cost numbers a reader scans without walking the
    full ``inputs.generations`` list.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="The generation's human label (e.g. 'Feynman').")
    year_available: float = Field(..., description="Approximate calendar year of availability.")
    die_count: int = Field(..., description="Number of dies on the package (D8 GPU = package).")
    kw_per_pkg: float = Field(..., description="All-in per-package electrical power, kW.")
    pkg_mass_kg: float = Field(..., description="All-in per-package mass, kg.")
    pkg_cost_musd: float = Field(..., description="Per-package price, $M.")
    pf_per_pkg: float = Field(..., description="Dense-FP4 PFLOPS per package.")
    source_class: str = Field(..., description="Source confidence class for this generation.")
    source_doc_path: str = Field(..., description="Durable research source path for this entry.")


class QueryExample(BaseModel):
    """One worked ``jq`` query in the ``meta.query_examples`` block.

    The ``query_examples`` block is the cold-reader contract: a cold agent
    runs these ``jq`` expressions to answer common questions without
    reverse-engineering the schema.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Stable key, e.g. 'headline_2036_revenue_central'.")
    question_answered: str = Field(..., description="Plain-language question this query answers.")
    jq_expression: str = Field(..., description="The exact jq expression.")
    expected_shape: str = Field(..., description="What the query result looks like.")
    important_paths: list[str] = Field(..., description="Important JSON paths touched.")
    applies_to: QueryAppliesTo = Field(..., description="Model family this query applies to.")

    @property
    def jq(self) -> str:
        """Return the jq expression for existing test and renderer helpers."""
        return self.jq_expression


class FormulaDefinition(BaseModel):
    """One public formula-definition metadata entry."""

    model_config = ConfigDict(frozen=True)

    formula_id: str = Field(..., description="Stable formula identifier.")
    formula_text: str = Field(..., description="Human-readable formula text.")
    description: str = Field(..., description="What this formula computes.")
    input_path_pattern: str = Field(..., description="Input-path pattern this formula consumes.")
    output_path_pattern: str = Field(..., description="Output-path pattern this formula emits.")
    unit_behavior: str = Field(..., description="How units flow through the formula.")
    scenario_notes: str | None = Field(default=None, description="Scenario caveats.")


class ValidationResult(BaseModel):
    """One public validation-result metadata entry."""

    model_config = ConfigDict(frozen=True)

    validation_id: str = Field(..., description="Stable validation identifier.")
    severity: ValidationSeverity = Field(..., description="pass, warn, or fail.")
    what_tested: str = Field(..., description="Plain-language test description.")
    expected_condition: str = Field(..., description="Expected condition.")
    observed_result: str = Field(..., description="Observed result.")
    related_json_paths: list[str] = Field(..., description="Related JSON paths.")
    remediation_hint: str | None = Field(default=None, description="Suggested remediation.")


class MetaBlock(BaseModel):
    """The ``meta`` block — validation, data dictionary, generation summary,
    and the ``query_examples`` cold-reader contract.
    """

    model_config = ConfigDict(frozen=True)

    validation: ValidationReport = Field(
        ...,
        description="The engine-computed V-rule report (V1..V17).",
    )
    data_dictionary: list[DataDictEntry] = Field(
        ...,
        description=(
            "One entry per emitted leaf field — built by the introspection "
            "helper from this module's `Field(description=...)` metadata."
        ),
    )
    formula_definitions: list[FormulaDefinition] = Field(
        ...,
        description="Formula catalog for formula_name references in output cells.",
    )
    validation_results: list[ValidationResult] = Field(
        ...,
        description="Public pass/warn/fail validation entries.",
    )
    generations_dictionary: list[GenerationSummary] = Field(
        ...,
        description="Compact per-generation summary view.",
    )
    query_examples: list[QueryExample] = Field(
        ...,
        description=(
            "Worked jq queries a cold agent can run to answer common "
            "questions (the cold-reader contract)."
        ),
    )
    source_status_summary: SourceStatusSummary = Field(
        ...,
        description="Count of input assumptions by source-status value.",
    )
    schema_version_notes: str = Field(
        ...,
        description="Human-readable schema notes for this artifact version.",
    )


# ---------------------------------------------------------------------------
# Top-level container
# ---------------------------------------------------------------------------


class SpaceModelOutput(BaseModel):
    """The complete output of one valuation run — the v8 artifact.

    Top-level shape, in strategy § 3.1 order (D21 — two data sections plus
    meta, no cycle-1 ``summary``):

    1. ``metadata`` — the run's identity (schema version, base year,
       horizon, the three founder-locked enums, generated-at timestamp).
    2. ``inputs`` — gospel anchors + slopes + the v8 dial blocks +
       the per-generation list.
    3. ``physical`` — the per-year per-node trajectory (ProvenanceCells).
    4. ``business`` — the per-year living-fleet rollup (ProvenanceCells).
    5. ``meta`` — validation report, data dictionary, generation summary,
       query_examples.

    Frozen — once built the artifact is immutable. Serialize via
    ``model_dump_json(indent=2)``.
    """

    model_config = ConfigDict(frozen=True)

    metadata: RunMetadata = Field(
        ...,
        description="The run's identity — schema version, base year, horizon, the enum locks.",
    )
    inputs: InputManifest = Field(
        ...,
        description="Every dial and constant the run consumed.",
    )
    physical: PhysicalBlock = Field(
        ...,
        description="The per-year per-node trajectory (ProvenanceCell-wrapped).",
    )
    business: BusinessBlock = Field(
        ...,
        description="The per-year living-fleet rollup (ProvenanceCell-wrapped).",
    )
    meta: MetaBlock = Field(
        ...,
        description="Validation report, data dictionary, generation summary, query_examples.",
    )


ValuationOutput = SpaceModelOutput
"""Historical internal name for :class:`SpaceModelOutput`."""


__all__ = [
    "SCHEMA_VERSION",
    "BusinessBlock",
    "BusinessYear",
    "CostBreakdownBlock",
    "DataDictEntry",
    "FieldKind",
    "FormulaDefinition",
    "GenerationSummary",
    "InputsBlock",
    "MetaBlock",
    "PhysicalBlock",
    "PhysicalYear",
    "QueryAppliesTo",
    "QueryExample",
    "RunMetadata",
    "Severity",
    "SpaceModelOutput",
    "SourceStatusSummary",
    "ValidationCheck",
    "ValidationResult",
    "ValidationSeverity",
    "ValidationReport",
    "ValuationOutput",
]
