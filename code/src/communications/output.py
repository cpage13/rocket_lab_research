"""The comms five-key Pydantic output models (the comms analog of DC output.py).

The complete typed shape of one communications-model run: the five-key
``CommsModelOutput`` (``metadata`` / ``inputs`` / ``physical`` / ``business`` /
``meta``), mirroring the data-center ``SpaceModelOutput`` but dropping the
GPU/generation specifics and adding the comms business-block fields (the
customer bands, the space-side cost and priced revenue).

THE ``meta`` BLOCK IS INTENTIONALLY LEAN IN THIS PHASE (Phase 3): the
:class:`MetaBlock` carries a validation report, a source-status summary, and
schema notes, but NOT the introspection-driven data dictionary, the
query-examples cold-reader contract, the formula-definition catalog, or the
executable V-rule list. Phase 5's json_output / validation enrich the meta
block with that cold-reader scaffolding; the leanness here is by design so the
five-key artifact is structurally complete and serializes.

The model is Neutron-only and cost-driven: no capture-share field, no heavier-
than-Neutron vehicle value, no baked-in verdict or conclusion label (the
comparison numbers and any verdict are Phase 4 / Phase 6, never an emitted
comms-output field).
"""

from __future__ import annotations

import logging

from pydantic import BaseModel, ConfigDict, Field

from common.meta import (
    DataDictEntry,
    FormulaDefinition,
    QueryExample,
    SourceStatusSummary,
    ValidationReport,
    ValidationResult,
)
from common.provenance import ProvenanceCell
from communications.constants import (
    MAX_FY,
    MAX_HORIZON_YEARS,
    MIN_FY,
    MIN_HORIZON_YEARS,
)
from communications.input_manifest import InputManifest

logger = logging.getLogger(__name__)

type YearString = str
"""A JSON-string year key, e.g. ``"2036"`` (the comms-local alias; the DC alias
is not imported, per the architecture guard against a DC-venture dependency)."""


class RunMetadata(BaseModel):
    """The ``metadata`` block: the comms run's identity.

    Carries the comms schema version, scenario name, base year + horizon, the
    steady-state year the headline figure is read at, an ISO-8601 generated-at
    timestamp, and the model package / version / artifact-role stamps. It has NO
    workload / operator / radiator enums (those are GPU-venture locks with no
    comms analog).
    """

    model_config = ConfigDict(frozen=True)

    schema_version: str = Field(
        ..., description="The comms output JSON schema version (e.g. 'comms-v1')."
    )
    scenario_name: str = Field(
        ..., description="Human-readable scenario label from the YAML config."
    )
    base_year: int = Field(
        ..., description="Calendar year corresponding to model year 0.", ge=MIN_FY, le=MAX_FY
    )
    horizon_years: int = Field(
        ...,
        description=(
            "Number of fiscal-year steps after year 0; the physical / business "
            "'years' maps have 'horizon_years + 1' entries."
        ),
        ge=MIN_HORIZON_YEARS,
        le=MAX_HORIZON_YEARS,
    )
    steady_state_year: int = Field(
        ...,
        description="The calendar year the mature steady-state headline figure is read at.",
        ge=MIN_FY,
        le=MAX_FY,
    )
    generated_at: str = Field(
        ..., description="ISO-8601 UTC timestamp at which the artifact was generated."
    )
    model_package: str | None = Field(
        ..., description="Python package / console-script name that generated the artifact."
    )
    model_version: str | None = Field(
        ..., description="Installed model package version, when available."
    )
    artifact_role: str = Field(
        ..., description="Artifact role such as draft, promoted_default, or promoted_named."
    )
    source_scenario_path: str = Field(..., description="Repository-relative source scenario path.")


class SatelliteCostBreakdownBlock(BaseModel):
    """The per-satellite cost decomposition for one class: four areas + minor + build + launch.

    The comms analog of the DC ``CostBreakdownBlock``, with comms line items.
    Every field is a :class:`ProvenanceCell`, all $M.
    """

    model_config = ConfigDict(frozen=True)

    antenna: ProvenanceCell = Field(
        ..., description="Per-satellite antenna build cost (the dominant line), $M."
    )
    comms_electronics: ProvenanceCell = Field(
        ..., description="Per-satellite comms-electronics build cost, $M."
    )
    solar: ProvenanceCell = Field(..., description="Per-satellite solar-array build cost, $M.")
    radiator_bus: ProvenanceCell = Field(
        ..., description="Per-satellite radiator/bus build cost, $M."
    )
    minor_component: ProvenanceCell = Field(
        ..., description="Per-satellite minor-component carry, $M."
    )
    build_cost: ProvenanceCell = Field(
        ..., description="Per-satellite build cost (four areas + minor), $M."
    )
    build_cost_after_learning: ProvenanceCell = Field(
        ..., description="Per-satellite build cost after the learning-curve discount, $M."
    )
    launch_cost_per_satellite: ProvenanceCell = Field(
        ..., description="Per-satellite share of the cadence-indexed launch cost, $M."
    )
    satellite_total: ProvenanceCell = Field(
        ..., description="Total per-satellite cost (discounted build + launch), $M."
    )


class SatelliteClassPhysical(BaseModel):
    """One satellite class's per-year per-satellite physical + packing + cost cells.

    Every field is a :class:`ProvenanceCell` except ``cost_breakdown`` (a
    :class:`SatelliteCostBreakdownBlock`). Carries the per-class packing fork
    transparency (the mass-bound and volume-bound counts and the
    binding-constraint enum) so a cold reader sees why the per-launch count is
    what it is.
    """

    model_config = ConfigDict(frozen=True)

    satellites_per_launch: ProvenanceCell = Field(
        ..., description="Binding satellites-per-launch count for this class."
    )
    binding_constraint: ProvenanceCell = Field(
        ..., description="Which envelope binds (mass / antenna_stow / ...)."
    )
    mass_bound_count: ProvenanceCell = Field(
        ..., description="Mass-bound per-launch count (transparency)."
    )
    volume_bound_count: ProvenanceCell = Field(
        ..., description="Stowed-volume-bound per-launch count (transparency)."
    )
    cost_breakdown: SatelliteCostBreakdownBlock = Field(
        ..., description="The per-satellite cost decomposition for this class."
    )
    cost_annual_per_satellite_musd: ProvenanceCell = Field(
        ..., description="Annualized per-satellite cost over the service life, $M/yr."
    )
    capability: ProvenanceCell = Field(
        ..., description="Per-satellite capability after the optional V4 step."
    )


class PhysicalYear(BaseModel):
    """One model year's per-satellite physical state for both classes plus the spectrum cells.

    The spectrum cells (the requirement, the empirical per-beam capacity, the
    naive cross-check) are per-year but configuration-driven (they do not vary
    across years unless a scenario ramps the spectrum dials), and are carried in
    the physical block so the capacity engine is visible. Every leaf is a
    :class:`ProvenanceCell` or a sub-block of cells.
    """

    model_config = ConfigDict(frozen=True)

    year: int = Field(..., description="Calendar year for this physical record.")
    broadband: SatelliteClassPhysical = Field(
        ..., description="The broadband (V3-class, mass-bound) satellite physical record."
    )
    direct_to_cell: SatelliteClassPhysical = Field(
        ..., description="The direct-to-cell (antenna-stow-bound) satellite physical record."
    )
    learning_curve_multiplier: ProvenanceCell = Field(
        ..., description="The learning-curve cost multiplier at this year's cumulative units."
    )
    cumulative_satellites_built: ProvenanceCell = Field(
        ...,
        description="Cumulative satellites built through this year (drives the learning curve).",
    )
    spectrum_to_acquire_mhz: ProvenanceCell = Field(
        ...,
        description="The spectrum the constellation must acquire, MHz (a requirement, not cost).",
    )
    per_beam_capacity_mbps: ProvenanceCell = Field(
        ..., description="Per-beam capacity from the empirical AST anchor, Mbps."
    )
    naive_capacity_mbps: ProvenanceCell = Field(
        ..., description="Naive bandwidth-times-efficiency capacity, Mbps (cross-check only)."
    )


class CustomerBandBlock(BaseModel):
    """A low/mid/high planning band of one customer-chain quantity, three sibling cells.

    The output-model analog of the Phase-2 ``CustomerBand`` dataclass (Finding
    F17): three sibling :class:`ProvenanceCell`s, each with its own formula,
    uses, and sources, so a cold reader queries ``...low`` / ``...mid`` /
    ``...high`` by path. NEVER a single triple-valued cell.
    """

    model_config = ConfigDict(frozen=True)

    low: ProvenanceCell = Field(
        ...,
        description="Band-low member (fewest subscribers: the fattest pipe, conservative packing).",
    )
    mid: ProvenanceCell = Field(..., description="Band-mid member.")
    high: ProvenanceCell = Field(
        ...,
        description="Band-high member (most subscribers: the thinnest pipe, aggressive packing).",
    )


class BusinessYear(BaseModel):
    """One model year's living-fleet rollup and the customer / cost / priced-revenue lines.

    Every leaf is a :class:`ProvenanceCell` or a :class:`CustomerBandBlock`. The
    customer chain is the DIRECT-TO-CELL chain (the SPECTRUM_spec 2,500-beam
    anchor); the broadband fleet cost is tracked alongside but the customer band
    is the direct-to-cell band (plan P3.5). This block carries NO cost-to-cost
    ratio and NO retail-undercut check (those are Phase 4) and NO verdict /
    conclusion label (the model never bakes in a conclusion).
    """

    model_config = ConfigDict(frozen=True)

    year: int = Field(..., description="Calendar year for this business record.")
    launches: ProvenanceCell = Field(
        ..., description="Whole-number launches in this calendar year."
    )
    broadband_satellites_deployed_this_year: ProvenanceCell = Field(
        ..., description="Broadband satellites deployed this year."
    )
    direct_to_cell_satellites_deployed_this_year: ProvenanceCell = Field(
        ..., description="Direct-to-cell satellites deployed this year."
    )
    broadband_living_fleet: ProvenanceCell = Field(
        ..., description="Broadband living-fleet satellite count under the service-life cliff."
    )
    direct_to_cell_living_fleet: ProvenanceCell = Field(
        ..., description="Direct-to-cell living-fleet satellite count under the service-life cliff."
    )
    broadband_cost_annual_fleet_musd: ProvenanceCell = Field(
        ..., description="Broadband living-fleet annual cost, $M/yr."
    )
    direct_to_cell_cost_annual_fleet_musd: ProvenanceCell = Field(
        ..., description="Direct-to-cell living-fleet annual cost, $M/yr."
    )
    total_served: CustomerBandBlock = Field(
        ..., description="Total registered direct-to-cell customers served (a planning band)."
    )
    cost_annual_per_customer_usd: CustomerBandBlock = Field(
        ...,
        description=(
            "Annual direct-to-cell cost to serve one customer, USD/yr (a band; "
            "per-customer cost falls as the served band rises)."
        ),
    )
    priced_cost_per_customer_usd: CustomerBandBlock = Field(
        ...,
        description=(
            "Priced per-customer revenue (cost x 1.5 for a 33.3% regular margin), USD/yr (a band)."
        ),
    )
    arpu_collectable_revenue_usd: ProvenanceCell = Field(
        ...,
        description=(
            "Annual per-customer revenue the operator can collect (ARPU x operator share), USD/yr."
        ),
    )


class PhysicalBlock(BaseModel):
    """The ``physical`` block: the per-year per-satellite trajectory, keyed by JSON-string year."""

    model_config = ConfigDict(frozen=True)

    years: dict[YearString, PhysicalYear] = Field(
        ..., description="Per-year per-satellite trajectory, keyed by JSON-string fiscal year."
    )


class BusinessBlock(BaseModel):
    """The ``business`` block: the per-year living-fleet rollup and customer band, by year."""

    model_config = ConfigDict(frozen=True)

    years: dict[YearString, BusinessYear] = Field(
        ...,
        description="Per-year fleet rollup and customer band, keyed by JSON-string fiscal year.",
    )


class MetaBlock(BaseModel):
    """The ``meta`` block: the cold-reader scaffold.

    The engine (Phase 3) builds this LEAN: it populates ``validation`` (an empty
    rules list), ``source_status_summary``, and ``schema_version_notes``, and
    leaves the four enrichment fields at their empty defaults. Phase 5's
    :func:`communications.json_output.enrich_comms_output` fills the four
    enrichment fields (the data dictionary, the formula catalog, the public
    validation results, and the query-example cold-reader contract) via
    ``model_copy``. Both the lean (engine) and the enriched (json_output)
    constructions are valid against this one schema, because the four enrichment
    fields default to empty.

    The comms meta block deliberately has NO ``generations_dictionary`` (a
    GPU-venture field with no comms analog) and NO ``conclusion_label`` /
    ``verdict`` field (the baked-in-conclusion disaster gate; the comparison
    numbers live in the ground artifact, the editorial verdict is Phase 6).
    """

    model_config = ConfigDict(frozen=True)

    validation: ValidationReport = Field(
        ...,
        description=(
            "The engine-computed validation report (lean empty rules list from the engine; the "
            "executable rules are filled by json_output enrichment in Phase 5)."
        ),
    )
    source_status_summary: SourceStatusSummary = Field(
        ..., description="Count of input assumptions by source-status value."
    )
    schema_version_notes: str = Field(
        ..., description="Human-readable schema notes for this artifact version."
    )
    data_dictionary: list[DataDictEntry] = Field(
        default_factory=list,
        description=(
            "One entry per emitted leaf field, built by the json_output introspection walk "
            "(empty until Phase-5 enrichment)."
        ),
    )
    formula_definitions: list[FormulaDefinition] = Field(
        default_factory=list,
        description=(
            "Formula catalog for the formula_name references in output cells "
            "(empty until Phase-5 enrichment)."
        ),
    )
    validation_results: list[ValidationResult] = Field(
        default_factory=list,
        description=("Public pass/warn/fail validation entries (empty until Phase-5 enrichment)."),
    )
    query_examples: list[QueryExample] = Field(
        default_factory=list,
        description=(
            "Worked jq queries a cold agent runs to answer common questions, the cold-reader "
            "contract (empty until Phase-5 enrichment)."
        ),
    )


class CommsModelOutput(BaseModel):
    """The complete output of one communications-model run: the five-key artifact.

    Top-level shape (parallel to the DC ``SpaceModelOutput``):
    1. ``metadata`` - the run's identity (schema version, base year, horizon,
       steady-state year, generated-at).
    2. ``inputs`` - every dial and constant the run consumed, as source-linked cells.
    3. ``physical`` - the per-year per-satellite trajectory (both classes).
    4. ``business`` - the per-year living-fleet rollup and the direct-to-cell
       customer band.
    5. ``meta`` - the (lean in Phase 3) cold-reader scaffold.

    Frozen. Serialize via ``model_dump_json(indent=2)``. The model is
    Neutron-only and cost-driven: no capture-share, no heavier-than-Neutron
    vehicle, no baked-in verdict.
    """

    model_config = ConfigDict(frozen=True)

    metadata: RunMetadata = Field(..., description="The run's identity.")
    inputs: InputManifest = Field(
        ..., description="Every dial and constant the run consumed, source-linked."
    )
    physical: PhysicalBlock = Field(..., description="The per-year per-satellite trajectory.")
    business: BusinessBlock = Field(
        ..., description="The per-year living-fleet rollup and the direct-to-cell customer band."
    )
    meta: MetaBlock = Field(
        ..., description="The cold-reader scaffold (lean in Phase 3, enriched in Phase 5)."
    )


__all__ = [
    "BusinessBlock",
    "BusinessYear",
    "CommsModelOutput",
    "CustomerBandBlock",
    "MetaBlock",
    "PhysicalBlock",
    "PhysicalYear",
    "RunMetadata",
    "SatelliteClassPhysical",
    "SatelliteCostBreakdownBlock",
    "YearString",
]
