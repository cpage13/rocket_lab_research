"""The space artifact's schema: :class:`SpaceModelOutput` and its blocks.

This module is the single source of truth for the shape of the
``rklb-value <scenario> --json`` artifact, versioned by
:data:`SCHEMA_VERSION`. Its cycle-2 layout was a clean break from the
cycle-1 v7 shape (D24, no back-compat shim). The top-level structure has
exactly five keys (D21):

* ``metadata``: the run's identity (schema version, base year, horizon,
  the three investor-locked enums, generated-at timestamp).
* ``inputs``: the gospel anchors, the post-Feynman slopes, and the
  dial blocks (cadence / fleet / volume / R-band / launch-cost) plus the
  per-generation list.
* ``physical``: the per-year per-node trajectory, each leaf wrapped in a
  :class:`common.provenance.ProvenanceCell`.
* ``business``: the per-year living-fleet rollup, each leaf a
  ProvenanceCell. The cycle-1 ``summary`` block is dropped; its content
  lives here in ``business.years``.
* ``meta``: the engine-computed validation report, the introspection-built
  data dictionary, the per-generation summary, and the ``query_examples``
  block (the cold-reader contract).

Every BaseModel here is ``model_config = ConfigDict(frozen=True)`` — the
output is immutable once built; downstream renderers and serializers may
read but not mutate.

Per-year data is keyed by a JSON-string year (``YearString``, e.g.
``"2036"``) in ``PhysicalBlock.years`` / ``BusinessBlock.years`` — this is
what a cold agent's ``jq`` queries address (``.physical.years."2036"``).

``ValidationCheck`` / ``Severity`` are the cycle-1 types, reused verbatim
for the 16 wired rules (V1-V10 and V12-V17; V11 retired): cycle 2 does
**not** define a new validation type.

References:
    strategy_05_20_cycle2.md § 3: the v8 schema.
    plan_05_20_cycle2.md § 5 T50: the v8 ``SpaceModelOutput`` sketch.
"""

from __future__ import annotations

import logging
from enum import StrEnum
from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from common.input_manifest import SourceStatus
from common.meta import (
    DataDictEntry,
    FormulaDefinition,
    QueryExample,
    SourceStatusSummary,
    ValidationReport,
    ValidationResult,
)
from common.provenance import ProvenanceCell, YearString
from data_center.config import (
    OperatorModel,
    RadiatorArchitecture,
    WorkloadType,
)
from data_center.constants import MAX_FY, MAX_HORIZON_YEARS, MIN_FY, MIN_HORIZON_YEARS
from data_center.input_manifest import InputManifest

logger = logging.getLogger(__name__)

SCHEMA_VERSION: Final[str] = "v9"
"""The space artifact's schema version, the single place it is defined (mirrors
``GROUND_SCHEMA_VERSION`` in ``ground.py``). ``v9`` (2026-09-23) removes the
duplicate ``business.years[].kw_on_orbit`` and ``pf_on_orbit`` (same values
and formulas as ``kw_living_fleet`` and ``pf_living_fleet``, which stay) and
publishes the data dictionary's ``source_class`` in lowercase
(``input`` / ``constant`` / ``derived``). ``v8`` was the cycle-2 five-block
schema."""

YEAR_UNIT: Final[str] = "year"
"""Declared data-dictionary unit for a calendar-year field (a non-cell leaf
declares its unit once in ``json_schema_extra``; cells carry their own)."""

YEARS_UNIT: Final[str] = "years"
"""Declared data-dictionary unit for a duration in years."""

# The cold-reader contract types the meta block holds (the validation, data-
# dictionary, query-example, and formula-definition models) live in
# :mod:`common.meta`; import them from there.


# ---------------------------------------------------------------------------
# Run metadata block
# ---------------------------------------------------------------------------


class ArtifactRole(StrEnum):
    """The role stamped in an artifact's ``metadata.artifact_role``.

    One vocabulary for the space artifact, the ground reference, and the CLI:

    * ``DRAFT``: a scratch run (the CLI's report and ``--json`` modes, the
      API default); a ground reference built from a draft is a draft too.
    * ``PROMOTED_DEFAULT`` / ``PROMOTED_NAMED``: a space artifact promoted as
      the public default or under a named stem.
    * ``PROMOTED_GROUND_DEFAULT`` / ``PROMOTED_GROUND_NAMED``: the ground
      reference built from such a promoted space artifact.
    """

    DRAFT = "draft"
    PROMOTED_DEFAULT = "promoted_default"
    PROMOTED_NAMED = "promoted_named"
    PROMOTED_GROUND_DEFAULT = "promoted_ground_default"
    PROMOTED_GROUND_NAMED = "promoted_ground_named"


class RunMetadata(BaseModel):
    """The ``metadata`` block — the run's identity.

    Carries the artifact's schema version, the base year + horizon, the three
    investor-locked enums (workload / operator / radiator architecture),
    the deployment philosophy, and an ISO-8601 generated-at timestamp.
    The enum locks + base year + horizon mirror
    :class:`data_center.config.MetadataConfig`; ``schema_version`` and
    ``generated_at`` are added at output-build time.
    """

    model_config = ConfigDict(frozen=True)

    schema_version: str = Field(
        ...,
        description=(
            "The artifact's JSON schema version ('v9' for the space model, "
            "'ground-v2' for the ground reference)."
        ),
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
        json_schema_extra={"unit": YEAR_UNIT},
    )
    horizon_years: int = Field(
        ...,
        description=(
            "Number of fiscal-year steps after year 0; the physical / "
            "business 'years' maps have 'horizon_years + 1' entries."
        ),
        ge=MIN_HORIZON_YEARS,
        le=MAX_HORIZON_YEARS,
        json_schema_extra={"unit": YEARS_UNIT},
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
    artifact_role: ArtifactRole = Field(
        ...,
        description=(
            "Artifact role: draft, promoted_default, promoted_named, or (on a "
            "ground reference) promoted_ground_default / promoted_ground_named."
        ),
    )
    source_scenario_path: str = Field(
        ...,
        description="Repository-relative source scenario path.",
    )


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
        description="Per-node compute build cost, all packages, $M.",
    )
    bus: ProvenanceCell = Field(
        ...,
        description="Per-node bus build cost, declines then flattens (D12), $M.",
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
        description="Per-node launch cost, cadence-indexed, $M.",
    )
    node_total: ProvenanceCell = Field(
        ...,
        description="Total per-node build + launch cost, the sum of the five lines, $M.",
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
        json_schema_extra={"unit": YEAR_UNIT},
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
        description="Per-node cost decomposition: the five build/launch lines + total.",
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
        json_schema_extra={"unit": YEAR_UNIT},
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
        description="Living fleet count under the service_life_years hard cliff (D1).",
    )
    kw_deployed_this_year: ProvenanceCell = Field(
        ...,
        description="Newly deployed node power in this year, kW.",
    )
    kw_living_fleet: ProvenanceCell = Field(
        ...,
        description="Living-fleet node power in this year, kW.",
    )
    pf_deployed_this_year: ProvenanceCell = Field(
        ...,
        description="Newly deployed node compute in this year, PFLOPS.",
    )
    pf_living_fleet: ProvenanceCell = Field(
        ...,
        description="Living-fleet node compute in this year, PFLOPS.",
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


class GenerationSummary(BaseModel):
    """One entry of the ``meta.generations_dictionary`` — a compact gen view.

    A flattened, render-friendly view of one GPU generation: the headline
    per-package physical + cost numbers a reader scans without walking the
    full ``inputs.config.generations`` list.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="The generation's human label (e.g. 'Feynman').")
    year_available: float = Field(
        ...,
        description="Approximate calendar year of availability.",
        json_schema_extra={"unit": YEAR_UNIT},
    )
    die_count: int = Field(
        ...,
        description="Number of dies on the package (D8 GPU = package).",
        json_schema_extra={"unit": "dies/package"},
    )
    kw_per_pkg: float = Field(
        ...,
        description="All-in per-package electrical power, kW.",
        json_schema_extra={"unit": "kW/package"},
    )
    pkg_mass_kg: float = Field(
        ...,
        description="All-in per-package mass, kg.",
        json_schema_extra={"unit": "kg/package"},
    )
    pkg_cost_musd: float = Field(
        ...,
        description="Per-package price, $M.",
        json_schema_extra={"unit": "MUSD/package"},
    )
    pf_per_pkg: float = Field(
        ...,
        description="Dense-FP4 PFLOPS per package.",
        json_schema_extra={"unit": "PFLOPS/package"},
    )
    source_class: SourceStatus = Field(
        ...,
        description=(
            "Public source status of this generation (the SourceStatus vocabulary "
            "the generation input cells use)."
        ),
    )
    source_doc_path: str = Field(..., description="Durable research source path for this entry.")


class MetaBlock(BaseModel):
    """The ``meta`` block — validation, data dictionary, generation summary,
    and the ``query_examples`` cold-reader contract.
    """

    model_config = ConfigDict(frozen=True)

    validation: ValidationReport = Field(
        ...,
        description=(
            "The engine-computed V-rule report: 16 rules, V1-V10 and V12-V17 (V11 retired)."
        ),
    )
    data_dictionary: list[DataDictEntry] = Field(
        ...,
        description=(
            "One entry per emitted leaf field, built by the introspection "
            "helper from this module's `Field(description=...)` metadata."
        ),
    )
    formula_definitions: list[FormulaDefinition] = Field(
        ...,
        description="Formula catalog for formula_name references in output cells.",
    )
    validation_results: list[ValidationResult] = Field(
        ...,
        description=(
            "The one public pass/warn/fail verdict list: every V-rule, the model "
            "invariants, and (for the canonical default scenario only) the "
            "default guards."
        ),
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
    """The complete output of one valuation run: the space artifact.

    Top-level shape, in strategy § 3.1 order (D21 — two data sections plus
    meta, no cycle-1 ``summary``):

    1. ``metadata``: the run's identity (schema version, base year,
       horizon, the three investor-locked enums, generated-at timestamp).
    2. ``inputs``: gospel anchors + slopes + the dial blocks +
       the per-generation list.
    3. ``physical``: the per-year per-node trajectory (ProvenanceCells).
    4. ``business``: the per-year living-fleet rollup (ProvenanceCells).
    5. ``meta``: validation report, data dictionary, generation summary,
       query_examples.

    Frozen — once built the artifact is immutable. Serialize via
    :func:`common.file_io.render_artifact_json`.
    """

    model_config = ConfigDict(frozen=True)

    metadata: RunMetadata = Field(
        ...,
        description="The run's identity: schema version, base year, horizon, the enum locks.",
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


__all__ = [
    "SCHEMA_VERSION",
    "YEARS_UNIT",
    "YEAR_UNIT",
    "ArtifactRole",
    "BusinessBlock",
    "BusinessYear",
    "CostBreakdownBlock",
    "GenerationSummary",
    "MetaBlock",
    "PhysicalBlock",
    "PhysicalYear",
    "RunMetadata",
    "SpaceModelOutput",
]
