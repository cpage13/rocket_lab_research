"""The comms ground reference: the bottom-up ground cost built PER DENSITY REGIME.

This module is the SECOND half of the comms dual pipeline (the GROUND side that
meets the SPACE side at promoted JSON). It builds the bottom-up cost to serve a
subscriber on the ground, computed SEPARATELY for two density regimes because the
ground alternative is a different number depending on whether ground plant already
exists at the location (DESIGN.md Section 7):

- SPARSE (the unserved / remote fringe, no incumbent plant): the ground denominator
  is a FRESH GROUND BUILD (annualized tower/site capex + backhaul + opex + the
  spectrum wash), about $875 to $1,540/sub/yr (COMM-100 / COMM-102). Space is BELOW
  ground here.
- DENSE (the served market, an entrenched incumbent on sunk plant): the ground
  denominator is the INCUMBENT'S MARGINAL DEFEND COST (a fraction of ARPU), about
  $84 to $180/sub/yr (COMM-096 / COMM-101). Space is ABOVE ground here.

The two ratios point in OPPOSITE directions, which is exactly why they are reported
separately; the model never collapses them into a single comms-wide ratio.

The module mirrors the data-center ground module (``data_center/ground.py``): the
same deep-module shape (typed in-memory space output in, a frozen ground-reference
output out), the same anchor-then-cost-then-compare flow, the same source-linked
cell discipline, the same ``meta`` cold-reader scaffold. The load-bearing
divergences from the DC ground module, which the executor honors:

- NO ``conclusion_label`` anywhere (the DC ground carries one; the comms model
  emits the comparison NUMBERS and the comparison FLAGS, never a verdict; the
  editorial judgement is hand-written in Phase 6, plan Section 0.9).
- The comparison UNIT is per-SUBSCRIBER cost (USD/yr), not per-GPU-package/per-MW.
- The ground cost is a CELLULAR delivery build, not a data-center facility build.
- The comparison adds the retail-undercut check, the revenue-ceiling reconciliation,
  and the Starlink-floor honesty rule, none of which the DC ground module has.
- The ground cost and comparison are SPLIT BY DENSITY REGIME (sparse vs dense),
  which the DC ground module has no analog for (the DC builds one greenfield cost).
- THE SPACE-TO-GROUND HANDOFF IS IN-MEMORY AND BY VALUE (concern C10): the builder
  receives the ``CommsModelOutput`` object as a function argument and reads its
  cells; it does NOT re-read the promoted space JSON from disk.
- ONE SCENARIO YAML: the comms model carries the ground dials INSIDE the single
  ``CommsConfig`` YAML (``config.ground``), unlike the DC which loads a separate
  ``ground_default.yaml``. So this module builds the ground config FROM the loaded
  ``CommsConfig`` (``ground_config_from_comms_config``); there is no standalone
  ground YAML loader.

IMPORT DIRECTION (no runtime cycle): ``comparison.py`` imports this module's
value-neutral ``DensityRegime`` enum at module level (it reads the enum members at
runtime to label each regime's cells) and the ground RESULT types only under
``TYPE_CHECKING``. To keep the wiring one-way at module load, this module does NOT
import ``comparison.py`` at module top (that would re-enter a partially-initialized
``ground`` before ``DensityRegime`` is defined): it imports the ``CommsComparison``
type under ``TYPE_CHECKING`` for the output annotation and lazy-imports
``build_comms_comparison`` INSIDE ``build_ground_reference_output`` (the builder is
needed only at call time). So the only module-load edge is comparison -> ground, no
cycle.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from common.input_manifest import (
    AssumptionRole,
    InputCell,
    InputScalar,
    SourceRef,
    SourceRefType,
    SourceStatus,
)
from common.meta import (
    DataDictEntry,
    QueryAppliesTo,
    QueryExample,
    SourceStatusSummary,
    ValidationResult,
    ValidationSeverity,
)
from common.provenance import FieldPath, ProvenanceCell, cell
from communications.comparison import CommsComparison, build_comms_comparison
from communications.config import CommsConfig, PriceReferenceDials, load_config
from communications.constants import (
    DENSITY_CROSSOVER_USD_PER_SUB_YEAR,
    MONTHS_PER_YEAR,
    PROMOTED_DEFAULT_ARTIFACT_ROLE,
    REVENUE_MULTIPLE,
    SUBS_PER_MILLION,
    USD_PER_MUSD,
    DensityRegime,
)
from communications.engine import run_comms_model
from communications.input_manifest import ScenarioMeta
from communications.output import CommsModelOutput, CustomerBandBlock, RunMetadata

logger = logging.getLogger(__name__)


# ===========================================================================
# Named constants (the "no bare literals" rule)
# ===========================================================================

GROUND_SCHEMA_VERSION: Final[str] = "comms-ground-v1"
"""The comms ground artifact schema version (distinct from the space comms-v1 and
the DC ground-v1)."""

DEFAULT_GROUND_SCENARIO_PATH: Final[str] = "code/scenarios/comms_default.yaml"
"""The comms ground reference reads the SAME default scenario as the space model:
the ground dials live in the one CommsConfig YAML (unlike the DC, which has a
separate ground_default.yaml). This is the repository-relative path stamped on the
ground artifact's manifest."""

SPACE_MODEL_DEFAULT_PATH: Final[str] = "communications/models/space/default.json"
"""The promoted space-model path, recorded in the anchor for provenance ONLY (the
handoff is in-memory; this string is the path the in-memory object was / will be
promoted to, cited so a cold reader knows which space artifact corresponds). It is
NOT read from disk."""

SOURCE_INDEX_PATH: Final[str] = "research/SOURCE_INDEX.md"
"""The public source ledger used by all promoted input cells."""

GROUND_COST_RESEARCH_PATH: Final[str] = "research/economics/comms_4g_5g_transition_cost.md"
"""The durable research doc backing the cellular delivery cost basis."""

GROUND_COST_BASIS_CLAIM_ID: Final[str] = "COMM-029"
"""The SOURCE_INDEX claim covering the overall cellular ground-cost basis
(RAN/backhaul/core cost splits and derived per-subscriber/per-POP figures)."""

GROUND_TOWER_COST_CLAIM_ID: Final[str] = "COMM-100"
"""The SOURCE_INDEX claim for the sparse fresh-build tower/site capex line."""

GROUND_SITES_PER_MILLION_CLAIM_ID: Final[str] = "COMM-100"
"""The SOURCE_INDEX claim for the sparse fresh-build sites-per-million-subs line."""

GROUND_BACKHAUL_CLAIM_ID: Final[str] = "COMM-029"
"""The SOURCE_INDEX claim for the sparse fresh-build backhaul line."""

GROUND_OPEX_CLAIM_ID: Final[str] = "COMM-029"
"""The SOURCE_INDEX claim for the sparse fresh-build ground-opex line."""

GROUND_AMORTIZATION_CLAIM_ID: Final[str] = "COMM-102"
"""The SOURCE_INDEX claim for the fresh-build amortization basis (~25-yr fiber
asset life)."""

GROUND_SPECTRUM_WASH_CLAIM_ID: Final[str] = "COMM-100"
"""The SOURCE_INDEX claim under which the ground spectrum line is carried as an
explicit zero wash."""

STARLINK_DISCLOSED_FLOOR_CLAIM_ID: Final[str] = "COMM-090"
"""The SOURCE_INDEX claim for the disclosed all-in Starlink floor (the disclosed
SpaceX S-1 connectivity-segment financials)."""

GROUND_SPARSE_FRESH_BUILD_CLAIM_ID: Final[str] = "COMM-100"
"""The SOURCE_INDEX claim for the SPARSE fresh-build ratio (flavor a; COMM-102 the
annualization basis, COMM-032 the extreme-rural passing anchor)."""

GROUND_DENSE_INCUMBENT_MARGINAL_CLAIM_ID: Final[str] = "COMM-096"
"""The SOURCE_INDEX claim for the DENSE incumbent marginal defend floor (the
fixed-broadband defend floor; COMM-101 the flavor-b ratio, COMM-098 the
price-to-beat-by-territory)."""

GROUND_DENSITY_CROSSOVER_CLAIM_ID: Final[str] = "COMM-103"
"""The SOURCE_INDEX claim for the sparse-vs-dense crossover and asymmetry verdict."""

ZERO_COST: Final[float] = 0.0
"""Zero-cost component value used for the explicit-zero spectrum wash and safe
ratios."""

ZERO_COUNT: Final[int] = 0
"""Initial counter value for source-status summaries."""

ONE_COUNT: Final[int] = 1
"""Counter increment for one input cell."""

_USD_UNIT: Final[str] = "USD"
"""The unit string for a per-subscriber annual cost ProvenanceCell."""

# Promote-helper path constants (mirroring the Phase-3 engine path constants).
_CALCULATOR_DIR: Final[Path] = Path(__file__).resolve().parents[2]
"""The `code/` directory (two parents up from this module)."""

_PROJECT_DIR: Final[Path] = _CALCULATOR_DIR.parent
"""The repository root."""

_DEFAULT_YAML: Final[Path] = _CALCULATOR_DIR / "scenarios" / "comms_default.yaml"
"""The packaged default comms scenario YAML."""

_PROMOTED_GROUND_DIR: Final[Path] = _PROJECT_DIR / "communications" / "models" / "ground"
"""The promoted comms ground reference directory."""


# DensityRegime is defined in communications.constants (a leaf module) and imported
# above so that both ground.py and comparison.py can reference the enum at
# class-build time without a circular import. It is re-exported here (it appears in
# __all__) so `from communications.ground import DensityRegime` resolves, mirroring
# how the DC ground module owns its regime-key vocabulary.


# ===========================================================================
# Data structures (frozen Pydantic models)
# ===========================================================================


class GroundReferenceConfig(BaseModel):
    """Validated comms ground-reference assumptions, a thin view over the GroundDials block.

    The comms model carries the ground dials INSIDE the one CommsConfig YAML
    (config.ground), unlike the DC which loads a separate ground_default.yaml. This
    class is the comms ground module's own validated view of those dials (the
    sparse fresh-build cellular lines, the dense incumbent-marginal fraction, and
    the disclosed Starlink floor). It is constructed FROM the CommsConfig ground
    block (via :func:`ground_config_from_comms_config`), not loaded independently.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    scenario_name: str = Field(
        default="Comms default ground reference",
        description="Human-readable label for the ground-reference assumption set.",
    )
    # The SPARSE (fresh-build) denominator lines (COMM-100 / COMM-102):
    tower_cost_musd_per_site: float = Field(
        ...,
        gt=ZERO_COST,
        description="Amortized fresh cellular tower/site build cost, $M per site.",
    )
    sites_per_million_subs: float = Field(
        ...,
        gt=ZERO_COST,
        description="Cell sites needed per million subscribers in the sparse fresh-build density.",
    )
    backhaul_cost_musd_per_site_year: float = Field(
        ..., gt=ZERO_COST, description="Annual backhaul/transport cost per site, $M."
    )
    ground_opex_musd_per_site_year: float = Field(
        ..., gt=ZERO_COST, description="Annual operations and maintenance per site, $M."
    )
    ground_amortization_years: int = Field(
        ...,
        ge=1,
        le=40,
        description="Years over which the fresh-build site capex amortizes (~25-yr fiber life).",
    )
    spectrum_cost_musd: float = Field(
        default=ZERO_COST,
        ge=ZERO_COST,
        description="Ground-side spectrum cost; an explicit zero wash (spectrum nets out).",
    )
    # The DENSE (incumbent marginal-cost defend floor) denominator (COMM-096 / COMM-101):
    incumbent_marginal_fraction_of_arpu: float = Field(
        ...,
        gt=ZERO_COST,
        le=1.0,
        description=(
            "Incumbent marginal defend floor as a fraction of ARPU (the dense denominator)."
        ),
    )
    # The dual-space-cost reference (not a density denominator):
    starlink_disclosed_all_in_cost_usd_per_sub_year: float = Field(
        ...,
        gt=ZERO_COST,
        description="Disclosed all-in Starlink floor, USD/yr (shown alongside the chain figure).",
    )


class SourceCatalog(BaseModel):
    """Public source references used by the comms ground-reference input cells."""

    model_config = ConfigDict(frozen=True)

    source_index_path: str = Field(..., description="Repository-relative SOURCE_INDEX path.")
    ground_cost_basis_claim_id: str = Field(
        ..., description="SOURCE_INDEX claim ID for the cellular ground-cost basis."
    )
    ground_cost_research_path: str = Field(
        ..., description="Research note supporting the cellular ground-cost framing."
    )


class GroundCostComponent(BaseModel):
    """One cost line in the comms ground per-subscriber cost build.

    The comms analog of the DC ``CostComponent``: a stable key, a label, the cost
    cell (USD/yr), an included flag, the source paths, and an optional note.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Stable component key (e.g. 'tower_amortized').")
    label: str = Field(..., description="Human-readable component label.")
    cost: ProvenanceCell = Field(
        ..., description="Annual per-subscriber cost for this line, USD/yr."
    )
    included: bool = Field(
        ..., description="Whether this line is included in the per-subscriber total."
    )
    source_paths: list[str] = Field(..., description="Source JSON paths or input-cell paths.")
    notes: str | None = Field(default=None, description="Component caveat or treatment note.")


class GroundCostResult(BaseModel):
    """The bottom-up ground per-subscriber cost to serve one subscriber for a year, ONE regime.

    The comms analog of the DC ``GroundCostResult``, but the comms model builds it
    TWICE, once per density regime (the ``regime`` field), because the ground
    alternative differs by density (DESIGN.md Section 7): SPARSE uses the fresh-build
    cost-out lines; DENSE uses the incumbent marginal-cost defend floor (a fraction
    of ARPU). Per-SUBSCRIBER (USD/yr). Carries the regime key, the component lines,
    the per-subscriber annual total, the priced per-subscriber cost (total x the
    1.5x margin), the explicit included/excluded lists, the source-status summary,
    and warnings.
    """

    model_config = ConfigDict(frozen=True)

    regime: DensityRegime = Field(
        ...,
        description="Which density regime this ground cost is for (sparse fresh-build vs dense).",
    )
    component_costs: list[GroundCostComponent] = Field(
        ..., description="Ground cost lines for this regime."
    )
    cost_annual_per_subscriber_usd: ProvenanceCell = Field(
        ...,
        description="Total annual ground cost to serve one subscriber in this regime, USD/yr.",
    )
    priced_cost_annual_per_subscriber_usd: ProvenanceCell = Field(
        ...,
        description="Ground per-subscriber cost x the 1.5x margin, USD/yr (the cost-to-cost side).",
    )
    included_components: list[str] = Field(..., description="Explicitly included lines.")
    excluded_components: list[str] = Field(
        ...,
        description="Explicitly excluded lines (land, financing, taxes, customer-premises gear).",
    )
    source_status_summary: dict[str, int] = Field(
        ..., description="Counts of ground input assumptions by source-status."
    )
    warnings: list[ValidationResult] = Field(..., description="Ground-side warnings.")


class GroundCostByDensity(BaseModel):
    """The bottom-up ground per-subscriber cost in BOTH density regimes (DESIGN.md Section 7).

    Carries the SPARSE fresh-build ground cost and the DENSE incumbent-marginal
    ground cost as two ``GroundCostResult`` objects, plus the crossover note (the
    dense-suburban fringe where the two roughly meet, about $490/sub/yr; COMM-103).
    The comms ground reference reports both, because the ground alternative is a
    different number depending on whether ground plant already exists; the model
    never blends them into one. This wrapper has no DC analog (the DC builds one
    greenfield ground cost).
    """

    model_config = ConfigDict(frozen=True)

    sparse: GroundCostResult = Field(
        ...,
        description="Fresh-build ground cost (the unserved/remote-fringe denominator, COMM-100).",
    )
    dense: GroundCostResult = Field(
        ...,
        description=(
            "Incumbent marginal-cost defend floor (the served-market denominator, COMM-096)."
        ),
    )
    crossover_note_usd_per_sub_year: ProvenanceCell = Field(
        ...,
        description=(
            "The approximate sparse-vs-dense crossover ground cost (about $490/sub/yr at the "
            "dense-suburban fringe, a zone not a point; COMM-103), USD/yr."
        ),
    )


class SpaceReferenceResult(BaseModel):
    """The space-model per-subscriber cost view for the same steady-state year.

    The comms analog of the DC ``OrbitalReferenceResult``. Mirrors the space side's
    per-customer cost (read off the in-memory CommsModelOutput at the steady-state
    year) so the comparison has a clean space-side object. Per-SUBSCRIBER (USD/yr).
    Carries the bottom-up space per-customer cost (the MID band member as headline
    plus the band), the priced space per-customer cost, the disclosed Starlink floor
    (the dual-space-cost reference), the steady-state living-fleet satellite count
    and annual fleet cost for context, the explicit exclusions, and warnings.
    """

    model_config = ConfigDict(frozen=True)

    cost_annual_per_subscriber_usd: ProvenanceCell = Field(
        ..., description="Space bottom-up per-customer cost, headline (MID band member), USD/yr."
    )
    cost_annual_per_subscriber_band: CustomerBandBlock = Field(
        ..., description="Space per-customer cost band (low/mid/high), USD/yr."
    )
    priced_cost_annual_per_subscriber_usd: ProvenanceCell = Field(
        ..., description="Space priced per-customer cost, headline (MID band member), USD/yr."
    )
    disclosed_starlink_floor_usd_per_sub_year: ProvenanceCell = Field(
        ...,
        description=(
            "The disclosed all-in Starlink floor shown alongside the bottom-up chain figure (NOT "
            "a target the chain beats), USD/yr."
        ),
    )
    living_fleet_satellites: ProvenanceCell = Field(
        ..., description="Steady-state direct-to-cell living-fleet satellite count."
    )
    cost_annual_fleet_musd: ProvenanceCell = Field(
        ..., description="Steady-state direct-to-cell living-fleet annual cost, $M/yr."
    )
    explicit_exclusions: list[str] = Field(
        ...,
        description=(
            "Space-side exclusions (orbital ops beyond build+launch+operate, insurance, ...)."
        ),
    )
    warnings: list[ValidationResult] = Field(..., description="Space-reference warnings.")


class GroundComparisonAnchor(BaseModel):
    """The steady-state cohort selected from the in-memory space output.

    The comms analog of the DC ``GroundComparisonAnchor``. Records WHICH space-model
    year and basis the comparison anchors on (the steady-state year, the living-fleet
    basis), the served-customer band the ground cost is compared per, the space-model
    path (for provenance, not a disk read), and the source paths the anchor was read
    from.
    """

    model_config = ConfigDict(frozen=True)

    space_model_path: str = Field(
        ...,
        description="Promoted space-model path (provenance reference; the handoff is in-memory).",
    )
    year: int = Field(..., description="Steady-state anchor year.")
    basis: str = Field(..., description="Anchor basis (e.g. 'living_fleet_steady_state').")
    total_served_mid: float = Field(
        ..., description="Steady-state served-customer MID band member (the comparison basis)."
    )
    note: str = Field(..., description="Plain-language anchor note.")
    source_paths: list[str] = Field(..., description="Space-output paths the anchor was read from.")


class GroundAssumptionInputTree(BaseModel):
    """Typed comms ground-reference assumption cells (one InputCell per ground dial)."""

    model_config = ConfigDict(frozen=True)

    tower_cost_musd_per_site: InputCell = Field(..., description="Tower/site build-cost input.")
    sites_per_million_subs: InputCell = Field(..., description="Sites-per-million-subs input.")
    backhaul_cost_musd_per_site_year: InputCell = Field(..., description="Backhaul-cost input.")
    ground_opex_musd_per_site_year: InputCell = Field(..., description="Ground-opex input.")
    ground_amortization_years: InputCell = Field(
        ..., description="Ground-amortization-years input."
    )
    spectrum_cost_musd: InputCell = Field(..., description="Ground spectrum-cost wash input.")
    incumbent_marginal_fraction_of_arpu: InputCell = Field(
        ..., description="Dense incumbent marginal defend-floor fraction-of-ARPU input."
    )
    starlink_disclosed_all_in_cost_usd_per_sub_year: InputCell = Field(
        ..., description="Disclosed all-in Starlink floor reference input."
    )


class GroundInputManifest(BaseModel):
    """The complete typed input manifest for the comms ground reference artifact."""

    model_config = ConfigDict(frozen=True)

    scenario: ScenarioMeta = Field(..., description="Ground scenario-identity metadata.")
    config: GroundAssumptionInputTree = Field(..., description="Ground assumption cells.")
    assumption_index: dict[str, InputCell] = Field(
        ..., description="Flat path-indexed lookup for all ground input cells."
    )


class GroundOutputMetadata(BaseModel):
    """Cold-reader metadata that helps query and validate the ground output."""

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
    """The complete comms ground reference artifact (the seven-key ground JSON).

    The comms analog of the DC ``GroundReferenceOutput``. Top-level shape: metadata,
    anchor, inputs, ground, space_reference, comparison, meta. (The DC names the
    space side 'orbital_reference'; the comms names it 'space_reference'.) The
    ``ground`` key is a ``GroundCostByDensity`` (BOTH density regimes), not a single
    ``GroundCostResult``, and the ``comparison`` carries the per-density ratios;
    these are the comms divergences from the DC's single greenfield ground cost
    (DESIGN.md Section 7). Frozen; serialize via ``model_dump_json(indent=2)``.
    """

    model_config = ConfigDict(frozen=True)

    metadata: RunMetadata = Field(..., description="Run identity for the ground artifact.")
    anchor: GroundComparisonAnchor = Field(..., description="Steady-state anchor.")
    inputs: GroundInputManifest = Field(..., description="Ground assumption manifest.")
    ground: GroundCostByDensity = Field(
        ...,
        description="Bottom-up ground per-subscriber cost in BOTH density regimes (sparse, dense).",
    )
    space_reference: SpaceReferenceResult = Field(
        ...,
        description="Space-model per-subscriber cost view (the same space cost on both regimes).",
    )
    comparison: CommsComparison = Field(
        ...,
        description=(
            "The per-density cost-to-cost ratio and retail undercut, plus the fleet-wide "
            "revenue-ceiling reconciliation and Starlink-floor honesty block."
        ),
    )
    meta: GroundOutputMetadata = Field(..., description="Cold-reader metadata.")


# ===========================================================================
# The input-spec table (the comms analog of the DC GROUND_INPUT_SPECS)
# ===========================================================================


@dataclass(frozen=True)
class GroundInputSpec:
    """Metadata needed to construct one comms ground input cell."""

    label: str
    unit: str | None
    description: str
    rationale: str
    claim_id: str
    source_status: SourceStatus
    notes: str | None = None


GROUND_INPUT_SPECS: Final[dict[str, GroundInputSpec]] = {
    "tower_cost_musd_per_site": GroundInputSpec(
        label="Tower / site build cost",
        unit="MUSD/site",
        description="Amortized fresh cellular tower/site build cost in the sparse fresh-build.",
        rationale="The capex line of the sparse fresh-build ground denominator (COMM-100).",
        claim_id=GROUND_TOWER_COST_CLAIM_ID,
        source_status=SourceStatus.SOURCED_ESTIMATE,
    ),
    "sites_per_million_subs": GroundInputSpec(
        label="Sites per million subscribers",
        unit="sites/M-subs",
        description="Cell sites needed per million subscribers in the sparse fresh-build density.",
        rationale="Many sites serve few subscribers in the unserved fringe (COMM-100).",
        claim_id=GROUND_SITES_PER_MILLION_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
        notes="An anchored sparse-density choice that lands the COMM-100 fresh-build band.",
    ),
    "backhaul_cost_musd_per_site_year": GroundInputSpec(
        label="Backhaul cost per site-year",
        unit="MUSD/site-year",
        description="Annual backhaul/transport cost per site.",
        rationale="The recurring transport line of the fresh-build ground denominator.",
        claim_id=GROUND_BACKHAUL_CLAIM_ID,
        source_status=SourceStatus.SOURCED_ESTIMATE,
    ),
    "ground_opex_musd_per_site_year": GroundInputSpec(
        label="Ground opex per site-year",
        unit="MUSD/site-year",
        description="Annual operations and maintenance per site.",
        rationale="The recurring operating line of the fresh-build ground denominator.",
        claim_id=GROUND_OPEX_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
    ),
    "ground_amortization_years": GroundInputSpec(
        label="Ground amortization years",
        unit="years",
        description="Years over which the fresh-build site capex amortizes (~25-yr fiber life).",
        rationale="The annualization basis for the sparse fresh-build denominator (COMM-102).",
        claim_id=GROUND_AMORTIZATION_CLAIM_ID,
        source_status=SourceStatus.SOURCED_ESTIMATE,
    ),
    "spectrum_cost_musd": GroundInputSpec(
        label="Ground spectrum-cost wash",
        unit="MUSD",
        description="Ground-side spectrum cost; an explicit zero wash (spectrum nets out).",
        rationale="Spectrum nets out of the cost comparison by construction; a visible zero wash.",
        claim_id=GROUND_SPECTRUM_WASH_CLAIM_ID,
        source_status=SourceStatus.SCENARIO,
        notes="Carried as an explicit zero so the wash is visible, not a hidden omission.",
    ),
    "incumbent_marginal_fraction_of_arpu": GroundInputSpec(
        label="Incumbent marginal defend floor (fraction of ARPU)",
        unit="fraction",
        description="The dense incumbent marginal defend floor as a fraction of ARPU.",
        rationale=(
            "The dense-regime ground denominator: the incumbent's cash cost to defend a connected "
            "subscriber, the price-to-beat in served territory (COMM-096), not the list price."
        ),
        claim_id=GROUND_DENSE_INCUMBENT_MARGINAL_CLAIM_ID,
        source_status=SourceStatus.SOURCED_ESTIMATE,
    ),
    "starlink_disclosed_all_in_cost_usd_per_sub_year": GroundInputSpec(
        label="Disclosed all-in Starlink floor",
        unit="USD/yr",
        description="Disclosed all-in Starlink cost to serve one subscriber for a year.",
        rationale=(
            "The disclosed all-in floor shown alongside the bottom-up chain figure (COMM-090 / "
            "COMM-103); a third-party disclosed-financials reference, not a Rocket Lab figure."
        ),
        claim_id=STARLINK_DISCLOSED_FLOOR_CLAIM_ID,
        source_status=SourceStatus.SOURCED_ESTIMATE,
    ),
}


# ===========================================================================
# Public functions
# ===========================================================================


def ground_config_from_comms_config(config: CommsConfig) -> GroundReferenceConfig:
    """Build the comms GroundReferenceConfig from the one CommsConfig YAML's ground block.

    Reads ``config.ground`` (the cellular delivery dials, the dense incumbent
    marginal fraction, and the disclosed Starlink floor) and ``config.scenario_levers``
    (the scenario name) and returns the typed ground-reference view. The comms model
    carries the ground dials inside the single CommsConfig, so there is NO separate
    ground YAML loader.

    Args:
        config: The validated CommsConfig (its ``ground`` and ``scenario_levers`` blocks).

    Returns:
        A frozen GroundReferenceConfig.
    """
    g = config.ground
    return GroundReferenceConfig(
        scenario_name=config.scenario_levers.scenario_name,
        tower_cost_musd_per_site=g.tower_cost_musd_per_site,
        sites_per_million_subs=g.sites_per_million_subs,
        backhaul_cost_musd_per_site_year=g.backhaul_cost_musd_per_site_year,
        ground_opex_musd_per_site_year=g.ground_opex_musd_per_site_year,
        ground_amortization_years=g.ground_amortization_years,
        spectrum_cost_musd=g.spectrum_cost_musd,
        incumbent_marginal_fraction_of_arpu=g.incumbent_marginal_fraction_of_arpu,
        starlink_disclosed_all_in_cost_usd_per_sub_year=(
            g.starlink_disclosed_all_in_cost_usd_per_sub_year
        ),
    )


def default_ground_source_catalog() -> SourceCatalog:
    """Return the default public source catalog for the comms ground assumptions."""
    return SourceCatalog(
        source_index_path=SOURCE_INDEX_PATH,
        ground_cost_basis_claim_id=GROUND_COST_BASIS_CLAIM_ID,
        ground_cost_research_path=GROUND_COST_RESEARCH_PATH,
    )


def build_ground_reference_output(
    space_output: CommsModelOutput,
    ground_config: GroundReferenceConfig,
    price_reference_config: PriceReferenceDials,
    source_catalog: SourceCatalog,
) -> GroundReferenceOutput:
    """Build the complete comms ground reference output for one space-model run.

    Mirrors the DC ``build_ground_reference_output``. Receives the in-memory
    CommsModelOutput BY VALUE (concern C10; it does NOT re-read the promoted space
    JSON from disk), the typed ground config, the price/collectability dials (for
    the retail reference and the ARPU reconciliation references; named
    ``price_reference`` per plan Amendment A1, demand is assumed not modeled), and
    the source catalog. Selects the steady-state anchor, builds the bottom-up ground
    per-subscriber cost PER DENSITY REGIME, builds the space-reference per-subscriber
    cost view (reading the steady-state cells off ``space_output``), delegates to
    :func:`communications.comparison.build_comms_comparison` for the comparison block,
    assembles the input manifest and the meta block, and returns the frozen
    GroundReferenceOutput. Emits NO conclusion label and NO verdict string.

    Args:
        space_output: The in-memory comms space-model output (read by value).
        ground_config: The typed comms ground-reference config.
        price_reference_config: The price/collectability dials (retail reference, ARPU, share).
        source_catalog: Public source references for the ground input cells.

    Returns:
        A frozen GroundReferenceOutput ready for JSON serialization.
    """
    inputs = _build_ground_input_manifest(
        ground_config=ground_config,
        source_catalog=source_catalog,
        source_scenario_path=DEFAULT_GROUND_SCENARIO_PATH,
    )
    anchor = _build_anchor(space_output)
    ground = _build_ground_cost_by_density(ground_config, price_reference_config)
    space_reference = _build_space_reference_result(space_output, ground_config)
    comparison = build_comms_comparison(
        ground=ground,
        space_reference=space_reference,
        price_reference_config=price_reference_config,
        space_output=space_output,
    )
    metadata = _build_ground_metadata(space_output.metadata, ground_config)
    validation_results = [
        *_anchor_validation_results(anchor),
        *ground.sparse.warnings,
        *ground.dense.warnings,
        *space_reference.warnings,
        *_density_split_scope_warnings(),
        *comparison.warnings,
    ]
    meta = GroundOutputMetadata(
        data_dictionary=_ground_data_dictionary(),
        validation_results=validation_results,
        query_examples=_ground_query_examples(),
        source_status_summary=_source_status_summary_model(inputs),
        schema_version_notes=(
            "comms-ground-v1 reference output anchored to the steady-state living-fleet "
            "space-model cohort; the ground per-subscriber cost is built PER DENSITY REGIME "
            "(sparse fresh-build vs dense incumbent-marginal, DESIGN.md Section 7), and the "
            "comparison reports the two regimes separately with no blended comms-wide ratio."
        ),
    )
    return GroundReferenceOutput(
        metadata=metadata,
        anchor=anchor,
        inputs=inputs,
        ground=ground,
        space_reference=space_reference,
        comparison=comparison,
        meta=meta,
    )


def render_ground_json(output: GroundReferenceOutput) -> str:
    """Serialize a :class:`GroundReferenceOutput` as indented JSON."""
    return output.model_dump_json(indent=2)


def promote_default_ground_reference(*, config_path: Path | None = None) -> Path:
    """Run the default comms scenario and write the promoted ground reference JSON to disk.

    Loads the default scenario (``code/scenarios/comms_default.yaml`` when
    ``config_path`` is None) via the comms config loader, runs ``run_comms_model`` to
    get the in-memory space output, builds the ground reference (in-memory, by value),
    and writes its JSON to ``<repo_root>/communications/models/ground/default.json``
    (creating the ``ground/`` directory if absent). This is the lean Phase-4 promote;
    Phase 5's CLI supersedes it with the ``rklb-comms`` console script and the
    dual-promote.

    Args:
        config_path: Scenario YAML to run; defaults to the packaged comms_default.yaml.

    Returns:
        The path the promoted ground JSON was written to.

    Raises:
        FileNotFoundError: If the scenario file does not exist.
        ValueError: If the scenario fails to load or validate.
    """
    yaml_path = config_path if config_path is not None else _DEFAULT_YAML
    config = load_config(yaml_path)
    space_output = run_comms_model(
        config,
        source_scenario_path=_repo_relative(yaml_path),
        artifact_role=PROMOTED_DEFAULT_ARTIFACT_ROLE,
    )
    ground_config = ground_config_from_comms_config(config)
    output = build_ground_reference_output(
        space_output,
        ground_config,
        config.price_reference,
        default_ground_source_catalog(),
    )
    path = _PROMOTED_GROUND_DIR / "default.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_ground_json(output) + "\n", encoding="utf-8")
    logger.info("promoted comms ground reference -> %s", path)
    return path


# ===========================================================================
# Build-flow helpers
# ===========================================================================


def _repo_relative(path: Path) -> str:
    """Return a repository-relative path string for the source-scenario stamp."""
    try:
        return path.relative_to(_PROJECT_DIR).as_posix()
    except ValueError:
        return path.as_posix()


def _cell_float(c: ProvenanceCell) -> float:
    """Return a numeric :class:`ProvenanceCell`'s value as ``float``.

    Args:
        c: A ProvenanceCell whose ``value`` is numeric (not None/str/bool).

    Returns:
        The cell's value as a ``float``.

    Raises:
        ValueError: If the cell's value is non-numeric.
    """
    value = c.value
    if isinstance(value, bool) or value is None or isinstance(value, str):
        raise ValueError(f"cell {c.description!r} is not numeric: {value!r}")
    return float(value)


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
                if space_metadata.artifact_role == PROMOTED_DEFAULT_ARTIFACT_ROLE
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
        "tower_cost_musd_per_site": ground_config.tower_cost_musd_per_site,
        "sites_per_million_subs": ground_config.sites_per_million_subs,
        "backhaul_cost_musd_per_site_year": ground_config.backhaul_cost_musd_per_site_year,
        "ground_opex_musd_per_site_year": ground_config.ground_opex_musd_per_site_year,
        "ground_amortization_years": ground_config.ground_amortization_years,
        "spectrum_cost_musd": ground_config.spectrum_cost_musd,
        "incumbent_marginal_fraction_of_arpu": ground_config.incumbent_marginal_fraction_of_arpu,
        "starlink_disclosed_all_in_cost_usd_per_sub_year": (
            ground_config.starlink_disclosed_all_in_cost_usd_per_sub_year
        ),
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
    assumption_index = {
        cell_value.path: cell_value for cell_value in _collect_ground_cells(input_tree)
    }
    scenario = ScenarioMeta(
        name=ground_config.scenario_name,
        description="Canonical default comms ground reference for the promoted space model.",
        path=source_scenario_path,
        is_default=source_scenario_path == DEFAULT_GROUND_SCENARIO_PATH,
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
    """Construct one comms ground-reference input cell (the full InputCell field list)."""
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
                note="Per-input source ledger entry for the comms ground reference.",
            ),
            SourceRef(
                ref_type=SourceRefType.RESEARCH_DOC,
                ref=source_catalog.ground_cost_research_path,
                claim_id=spec.claim_id,
                note="Research basis for the cellular ground-delivery cost.",
            ),
            SourceRef(
                ref_type=SourceRefType.MODEL_DERIVATION,
                ref=source_scenario_path,
                claim_id=spec.claim_id,
                note="Comms ground scenario value used for this model run.",
            ),
        ],
        rationale=spec.rationale,
        notes=spec.notes,
    )


def _collect_ground_cells(input_tree: GroundAssumptionInputTree) -> list[InputCell]:
    """Collect all ground input cells in stable field order."""
    return [
        input_tree.tower_cost_musd_per_site,
        input_tree.sites_per_million_subs,
        input_tree.backhaul_cost_musd_per_site_year,
        input_tree.ground_opex_musd_per_site_year,
        input_tree.ground_amortization_years,
        input_tree.spectrum_cost_musd,
        input_tree.incumbent_marginal_fraction_of_arpu,
        input_tree.starlink_disclosed_all_in_cost_usd_per_sub_year,
    ]


def _build_anchor(space_output: CommsModelOutput) -> GroundComparisonAnchor:
    """Select the steady-state living-fleet cohort from the typed space output (by value)."""
    key = str(space_output.metadata.steady_state_year)
    business_year = space_output.business.years[key]
    total_served_mid = _cell_float(business_year.total_served.mid)
    return GroundComparisonAnchor(
        space_model_path=SPACE_MODEL_DEFAULT_PATH,
        year=space_output.metadata.steady_state_year,
        basis="living_fleet_steady_state",
        total_served_mid=total_served_mid,
        note=(
            "The steady-state living-fleet cohort; the per-subscriber comparison basis. The space "
            "cost is the same on both density regimes (coverage is flat across geography)."
        ),
        source_paths=[
            f"business.years.{key}.total_served.mid",
            f"business.years.{key}.cost_annual_per_customer_usd",
        ],
    )


# ===========================================================================
# The ground cost arithmetic (forks by density regime)
# ===========================================================================


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
    """Build a provenance cell with an explicit source status and notes."""
    built = cell(
        value=value,
        unit=unit,
        formula_name=formula_name,
        uses=uses,
        sources=sources,
        description=description,
    )
    return built.model_copy(update={"source_status": source_status, "notes": notes})


def _build_sparse_components(
    ground_config: GroundReferenceConfig,
) -> list[GroundCostComponent]:
    """Build the SPARSE fresh-build cost lines (USD/yr), each a GroundCostComponent."""
    base = "inputs.config"
    sites_per_sub = ground_config.sites_per_million_subs / SUBS_PER_MILLION
    tower = (
        sites_per_sub
        * ground_config.tower_cost_musd_per_site
        * USD_PER_MUSD
        / ground_config.ground_amortization_years
    )
    backhaul = sites_per_sub * ground_config.backhaul_cost_musd_per_site_year * USD_PER_MUSD
    opex = sites_per_sub * ground_config.ground_opex_musd_per_site_year * USD_PER_MUSD
    spectrum = ground_config.spectrum_cost_musd * USD_PER_MUSD

    return [
        GroundCostComponent(
            name="tower_amortized",
            label="Amortized fresh tower/site capex",
            cost=_provenance_cell(
                value=tower,
                unit=_USD_UNIT,
                formula_name="comms_ground_tower_amortized_per_sub",
                uses=[
                    f"{base}.sites_per_million_subs",
                    f"{base}.tower_cost_musd_per_site",
                    f"{base}.ground_amortization_years",
                ],
                sources=[GROUND_TOWER_COST_CLAIM_ID, GROUND_AMORTIZATION_CLAIM_ID],
                source_status=SourceStatus.DERIVED_ESTIMATE,
                description="Per-subscriber annual amortized cellular tower/site capex, USD/yr.",
            ),
            included=True,
            source_paths=[f"{base}.tower_cost_musd_per_site"],
        ),
        GroundCostComponent(
            name="backhaul",
            label="Backhaul / transport",
            cost=_provenance_cell(
                value=backhaul,
                unit=_USD_UNIT,
                formula_name="comms_ground_backhaul_per_sub",
                uses=[
                    f"{base}.sites_per_million_subs",
                    f"{base}.backhaul_cost_musd_per_site_year",
                ],
                sources=[GROUND_BACKHAUL_CLAIM_ID],
                source_status=SourceStatus.DERIVED_ESTIMATE,
                description="Per-subscriber annual cellular backhaul cost, USD/yr.",
            ),
            included=True,
            source_paths=[f"{base}.backhaul_cost_musd_per_site_year"],
        ),
        GroundCostComponent(
            name="ground_opex",
            label="Operations and maintenance",
            cost=_provenance_cell(
                value=opex,
                unit=_USD_UNIT,
                formula_name="comms_ground_opex_per_sub",
                uses=[
                    f"{base}.sites_per_million_subs",
                    f"{base}.ground_opex_musd_per_site_year",
                ],
                sources=[GROUND_OPEX_CLAIM_ID],
                source_status=SourceStatus.DERIVED_ESTIMATE,
                description=(
                    "Per-subscriber annual cellular operations and maintenance cost, USD/yr."
                ),
            ),
            included=True,
            source_paths=[f"{base}.ground_opex_musd_per_site_year"],
        ),
        GroundCostComponent(
            name="spectrum_wash",
            label="Spectrum (explicit zero wash)",
            cost=_provenance_cell(
                value=spectrum,
                unit=_USD_UNIT,
                formula_name="comms_ground_spectrum_wash_per_sub",
                uses=[f"{base}.spectrum_cost_musd"],
                sources=[GROUND_SPECTRUM_WASH_CLAIM_ID],
                source_status=SourceStatus.SCENARIO,
                description=(
                    "Per-subscriber annual ground-side spectrum cost. Spectrum nets out of the "
                    "cost comparison by construction; carried as an explicit zero, not a cost "
                    "numerator line."
                ),
            ),
            included=True,
            source_paths=[f"{base}.spectrum_cost_musd"],
            notes="An explicit zero so the wash is visible, not a hidden omission.",
        ),
    ]


def _build_dense_components(
    ground_config: GroundReferenceConfig,
    price_reference_config: PriceReferenceDials,
) -> list[GroundCostComponent]:
    """Build the DENSE incumbent marginal-cost defend-floor line (USD/yr), one component."""
    base = "inputs.config"
    incumbent_marginal = (
        ground_config.incumbent_marginal_fraction_of_arpu
        * price_reference_config.arpu_usd_per_month
        * MONTHS_PER_YEAR
    )
    return [
        GroundCostComponent(
            name="incumbent_marginal_defend",
            label="Incumbent marginal defend cost",
            cost=_provenance_cell(
                value=incumbent_marginal,
                unit=_USD_UNIT,
                formula_name="comms_ground_dense_incumbent_marginal_per_sub",
                uses=[
                    f"{base}.incumbent_marginal_fraction_of_arpu",
                    "inputs.config.price_reference.arpu_usd_per_month",
                ],
                sources=[GROUND_DENSE_INCUMBENT_MARGINAL_CLAIM_ID, GROUND_COST_RESEARCH_PATH],
                source_status=SourceStatus.SOURCED_ESTIMATE,
                description=(
                    "The dense-regime incumbent marginal-cost defend floor, USD/yr (about 10 to "
                    "20% of ARPU, COMM-096): the price-to-beat in served markets, NOT the list "
                    "price; the incumbent has 30 to 40 points of EBITDA headroom to hold it "
                    "(COMM-097)."
                ),
            ),
            included=True,
            source_paths=[f"{base}.incumbent_marginal_fraction_of_arpu"],
        )
    ]


def _build_ground_cost_result(
    *,
    regime: DensityRegime,
    components: list[GroundCostComponent],
    source_status_summary: dict[str, int],
) -> GroundCostResult:
    """Sum a regime's included lines, price them at the 1.5x margin, and assemble the result."""
    included = [c for c in components if c.included]
    total = sum(_cell_float(c.cost) for c in included)
    priced = total * REVENUE_MULTIPLE
    base_uses = [f"ground.{regime.value}.component_costs"]

    total_cell = _provenance_cell(
        value=total,
        unit=_USD_UNIT,
        formula_name="comms_ground_total_per_sub_from_lines",
        uses=base_uses,
        sources=[GROUND_COST_BASIS_CLAIM_ID],
        source_status=SourceStatus.DERIVED_ESTIMATE,
        description=f"Total bottom-up {regime.value} ground per-subscriber annual cost, USD/yr.",
    )
    priced_cell = _provenance_cell(
        value=priced,
        unit=_USD_UNIT,
        formula_name="comms_ground_priced_per_sub_from_cost_and_multiple",
        uses=[f"ground.{regime.value}.cost_annual_per_subscriber_usd"],
        sources=[GROUND_COST_BASIS_CLAIM_ID],
        source_status=SourceStatus.DERIVED_ESTIMATE,
        description=(
            f"The {regime.value} ground per-subscriber cost marked up by the 1.5x margin, USD/yr "
            "(the cost-to-cost ground side)."
        ),
    )
    if regime is DensityRegime.SPARSE:
        excluded = [
            "land_acquisition",
            "financing_costs",
            "taxes",
            "customer_premises_equipment",
            "retail_margin_beyond_1_5x",
            "corporate_overhead",
        ]
    else:
        excluded = [
            "fresh_build_capex_plant_already_sunk",
            "land_acquisition",
            "financing_costs",
            "taxes",
            "customer_premises_equipment",
            "retail_margin_beyond_1_5x",
            "corporate_overhead",
        ]
    return GroundCostResult(
        regime=regime,
        component_costs=components,
        cost_annual_per_subscriber_usd=total_cell,
        priced_cost_annual_per_subscriber_usd=priced_cell,
        included_components=[c.name for c in included],
        excluded_components=excluded,
        source_status_summary=source_status_summary,
        warnings=_ground_scope_warnings(regime),
    )


def _build_ground_cost_by_density(
    ground_config: GroundReferenceConfig,
    price_reference_config: PriceReferenceDials,
) -> GroundCostByDensity:
    """Build the ground per-subscriber cost for BOTH density regimes plus the crossover note."""
    sparse_components = _build_sparse_components(ground_config)
    dense_components = _build_dense_components(ground_config, price_reference_config)
    sparse = _build_ground_cost_result(
        regime=DensityRegime.SPARSE,
        components=sparse_components,
        source_status_summary={},
    )
    dense = _build_ground_cost_result(
        regime=DensityRegime.DENSE,
        components=dense_components,
        source_status_summary={},
    )
    crossover = _provenance_cell(
        value=DENSITY_CROSSOVER_USD_PER_SUB_YEAR,
        unit=_USD_UNIT,
        formula_name="comms_ground_density_crossover_reference",
        uses=[
            "ground.sparse.cost_annual_per_subscriber_usd",
            "ground.dense.cost_annual_per_subscriber_usd",
        ],
        sources=[GROUND_DENSITY_CROSSOVER_CLAIM_ID],
        source_status=SourceStatus.SOURCED_ESTIMATE,
        description=(
            "The approximate sparse-vs-dense crossover ground cost (about $490/sub/yr at the "
            "dense-suburban fringe, a zone not a sharp point; COMM-103), USD/yr."
        ),
    )
    return GroundCostByDensity(
        sparse=sparse, dense=dense, crossover_note_usd_per_sub_year=crossover
    )


def _build_space_reference_result(
    space_output: CommsModelOutput, ground_config: GroundReferenceConfig
) -> SpaceReferenceResult:
    """Read the steady-state space per-customer cost view off the in-memory output (by value)."""
    key = str(space_output.metadata.steady_state_year)
    business_year = space_output.business.years[key]
    cost_band = business_year.cost_annual_per_customer_usd
    priced_band = business_year.priced_cost_per_customer_usd
    disclosed = _provenance_cell(
        value=ground_config.starlink_disclosed_all_in_cost_usd_per_sub_year,
        unit=_USD_UNIT,
        formula_name="comms_disclosed_starlink_floor_passthrough",
        uses=["inputs.config.starlink_disclosed_all_in_cost_usd_per_sub_year"],
        sources=[STARLINK_DISCLOSED_FLOOR_CLAIM_ID, GROUND_DENSITY_CROSSOVER_CLAIM_ID],
        source_status=SourceStatus.SOURCED_ESTIMATE,
        description=(
            "The disclosed all-in Starlink floor shown alongside the bottom-up chain figure (a "
            "disclosed-financials reference, NOT a Rocket Lab figure and NOT a target the chain "
            "beats), USD/yr."
        ),
    )
    return SpaceReferenceResult(
        cost_annual_per_subscriber_usd=cost_band.mid,
        cost_annual_per_subscriber_band=cost_band,
        priced_cost_annual_per_subscriber_usd=priced_band.mid,
        disclosed_starlink_floor_usd_per_sub_year=disclosed,
        living_fleet_satellites=business_year.direct_to_cell_living_fleet,
        cost_annual_fleet_musd=business_year.direct_to_cell_cost_annual_fleet_musd,
        explicit_exclusions=[
            "orbital_ops_beyond_build_launch_operate",
            "insurance",
            "financing",
            "taxes",
            "corporate_overhead",
        ],
        warnings=_space_reference_scope_warnings(),
    )


# ===========================================================================
# Warnings, meta helpers, and source-status summary
# ===========================================================================


def _ground_scope_warnings(regime: DensityRegime) -> list[ValidationResult]:
    """Emit the per-regime ground-scope warning."""
    if regime is DensityRegime.SPARSE:
        observed = (
            "The sparse fresh-build ground cost is an order-of-magnitude annualized rural-build "
            "screen (the annualization assumptions, COMM-102), not a site-specific construction "
            "estimate."
        )
    else:
        observed = (
            "The dense incumbent-marginal floor is the firmer of the two ground numbers, but the "
            "entrant must beat the marginal defend cost, NOT the incumbent's list price (COMM-096)."
        )
    return [
        ValidationResult(
            validation_id=f"comms_ground_{regime.value}_order_of_magnitude",
            severity=ValidationSeverity.WARN,
            what_tested=f"The {regime.value} ground-cost interpretation.",
            expected_condition="The ground reference avoids precise site-specific parity claims.",
            observed_result=observed,
            related_json_paths=[f"ground.{regime.value}.cost_annual_per_subscriber_usd"],
            remediation_hint="Use sourced site-specific inputs before precise parity claims.",
        )
    ]


def _space_reference_scope_warnings() -> list[ValidationResult]:
    """Emit the space-reference scope warning (build+launch+operate only)."""
    return [
        ValidationResult(
            validation_id="comms_space_reference_scope_build_launch_operate_only",
            severity=ValidationSeverity.WARN,
            what_tested="The space-reference scope.",
            expected_condition="The space reference states what is excluded.",
            observed_result=(
                "The space reference mirrors the modeled build+launch+operate cost only."
            ),
            related_json_paths=["space_reference.explicit_exclusions"],
            remediation_hint=(
                "Add orbital operating-cost assumptions before using this as full TCO."
            ),
        )
    ]


def _density_split_scope_warnings() -> list[ValidationResult]:
    """Emit the sparse-vs-dense density-split scope warning."""
    return [
        ValidationResult(
            validation_id="comms_ground_density_split_is_a_map_not_one_ratio",
            severity=ValidationSeverity.WARN,
            what_tested="The sparse-vs-dense density split.",
            expected_condition=(
                "The two ratios are reported separately and point opposite directions."
            ),
            observed_result=(
                "The sparse-vs-dense crossover is a zone, not a sharp point (about the "
                "dense-suburban fringe, COMM-103); the comparison is a MAP (space wins sparse, "
                "loses dense), never a single blended comms-wide ratio."
            ),
            related_json_paths=[
                "ground.sparse.cost_annual_per_subscriber_usd",
                "ground.dense.cost_annual_per_subscriber_usd",
                "ground.crossover_note_usd_per_sub_year",
            ],
            remediation_hint="Read the sparse and dense regimes separately.",
        )
    ]


def _anchor_validation_results(anchor: GroundComparisonAnchor) -> list[ValidationResult]:
    """Build the public validation result for the steady-state anchor."""
    return [
        ValidationResult(
            validation_id="comms_ground_anchor_steady_state_living_fleet",
            severity=ValidationSeverity.OK,
            what_tested="The ground anchor uses the steady-state living-fleet cohort.",
            expected_condition="basis=living_fleet_steady_state at the steady-state year.",
            observed_result=f"year={anchor.year}; basis={anchor.basis}.",
            related_json_paths=["anchor.year", "anchor.basis", *anchor.source_paths],
            remediation_hint=None,
        )
    ]


def _source_status_summary_dict(inputs: GroundInputManifest) -> dict[str, int]:
    """Count the ground assumptions by source-status string."""
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


def _ground_data_dictionary() -> list[DataDictEntry]:
    """Return compact data-dictionary entries for high-value ground paths, both regimes."""
    return [
        DataDictEntry(
            path="anchor",
            description="The steady-state living-fleet cohort selected from the space model.",
            unit="-",
            type="object",
            source_class="DERIVED",
        ),
        DataDictEntry(
            path="ground.sparse.cost_annual_per_subscriber_usd",
            description="Sparse fresh-build ground cost to serve one subscriber for a year.",
            unit="USD",
            type="cell",
            source_class="DERIVED",
        ),
        DataDictEntry(
            path="ground.dense.cost_annual_per_subscriber_usd",
            description="Dense incumbent marginal-cost defend floor to serve one subscriber.",
            unit="USD",
            type="cell",
            source_class="DERIVED",
        ),
        DataDictEntry(
            path="ground.crossover_note_usd_per_sub_year",
            description="The approximate sparse-vs-dense crossover ground cost (a zone, COMM-103).",
            unit="USD",
            type="cell",
            source_class="DERIVED",
        ),
        DataDictEntry(
            path="space_reference.cost_annual_per_subscriber_usd",
            description="Space bottom-up per-customer cost, MID member (same on both regimes).",
            unit="USD",
            type="cell",
            source_class="DERIVED",
        ),
        DataDictEntry(
            path="comparison.by_density.sparse.cost_to_cost.space_to_ground_ratio_mid",
            description="The sparse cost-to-cost ratio (space wins the unserved fringe).",
            unit="ratio",
            type="cell",
            source_class="DERIVED",
        ),
        DataDictEntry(
            path="comparison.by_density.dense.cost_to_cost.space_to_ground_ratio_mid",
            description="The dense cost-to-cost ratio (space loses the served market).",
            unit="ratio",
            type="cell",
            source_class="DERIVED",
        ),
        DataDictEntry(
            path="comparison.by_density.sparse.price_undercut.undercut_passes",
            description="Does the space priced cost undercut the sparse retail reference (flag).",
            unit="bool",
            type="cell",
            source_class="DERIVED",
        ),
        DataDictEntry(
            path="comparison.by_density.dense.price_undercut.undercut_passes",
            description="Does the space priced cost undercut the dense marginal floor (flag).",
            unit="bool",
            type="cell",
            source_class="DERIVED",
        ),
        DataDictEntry(
            path="comparison.by_density.dense.space_capacity_binds",
            description="Does the space capacity ceiling bind in the dense regime (physics flag).",
            unit="bool",
            type="cell",
            source_class="DERIVED",
        ),
        DataDictEntry(
            path="comparison.revenue_ceiling",
            description="The fleet-wide revenue-ceiling reconciliation (the collectable-win gate).",
            unit="-",
            type="object",
            source_class="DERIVED",
        ),
        DataDictEntry(
            path="space_reference.disclosed_starlink_floor_usd_per_sub_year",
            description="The disclosed all-in Starlink floor shown alongside the chain figure.",
            unit="USD",
            type="cell",
            source_class="INPUT",
        ),
        DataDictEntry(
            path="inputs.assumption_index",
            description="Flat index of every comms ground assumption input cell.",
            unit="-",
            type="object",
            source_class="INPUT",
        ),
    ]


def _ground_query_examples() -> list[QueryExample]:
    """Return ground-specific jq examples for cold readers (both regimes side by side)."""
    return [
        QueryExample(
            name="ground_anchor",
            question_answered="What cohort does the ground reference compare against?",
            jq_expression=".anchor",
            expected_shape="object with year, basis, total_served_mid",
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
            name="ground_cost_by_density",
            question_answered="What are the sparse and dense ground per-subscriber costs?",
            jq_expression=(
                "{sparse: .ground.sparse.cost_annual_per_subscriber_usd.value, "
                "dense: .ground.dense.cost_annual_per_subscriber_usd.value}"
            ),
            expected_shape="object with the two density ground costs (sparse >> dense)",
            important_paths=[
                "ground.sparse.cost_annual_per_subscriber_usd",
                "ground.dense.cost_annual_per_subscriber_usd",
            ],
            applies_to=QueryAppliesTo.GROUND,
        ),
        QueryExample(
            name="cost_to_cost_map_both_regimes",
            question_answered="Where does space win and lose on cost (the opposite-direction map)?",
            jq_expression=(
                ".comparison.by_density | {sparse: "
                ".sparse.cost_to_cost.space_to_ground_ratio_mid.value, dense: "
                ".dense.cost_to_cost.space_to_ground_ratio_mid.value}"
            ),
            expected_shape="object with the sparse and dense cost-to-cost ratios",
            important_paths=[
                "comparison.by_density.sparse.cost_to_cost.space_to_ground_ratio_mid",
                "comparison.by_density.dense.cost_to_cost.space_to_ground_ratio_mid",
            ],
            applies_to=QueryAppliesTo.GROUND,
        ),
        QueryExample(
            name="sparse_cost_to_cost_ratio",
            question_answered="What is the sparse cost-to-cost ratio (where space wins)?",
            jq_expression=".comparison.by_density.sparse.cost_to_cost.space_to_ground_ratio_mid",
            expected_shape="ProvenanceCell ratio",
            important_paths=["comparison.by_density.sparse.cost_to_cost.space_to_ground_ratio_mid"],
            applies_to=QueryAppliesTo.GROUND,
        ),
        QueryExample(
            name="dense_cost_to_cost_ratio",
            question_answered="What is the dense cost-to-cost ratio (where space loses)?",
            jq_expression=".comparison.by_density.dense.cost_to_cost.space_to_ground_ratio_mid",
            expected_shape="ProvenanceCell ratio",
            important_paths=["comparison.by_density.dense.cost_to_cost.space_to_ground_ratio_mid"],
            applies_to=QueryAppliesTo.GROUND,
        ),
        QueryExample(
            name="price_undercut_flags",
            question_answered="Does the space priced cost undercut each regime's price-to-beat?",
            jq_expression=(
                "{sparse: .comparison.by_density.sparse.price_undercut.undercut_passes.value, "
                "dense: .comparison.by_density.dense.price_undercut.undercut_passes.value}"
            ),
            expected_shape="object with the two per-regime undercut flags",
            important_paths=[
                "comparison.by_density.sparse.price_undercut.undercut_passes",
                "comparison.by_density.dense.price_undercut.undercut_passes",
            ],
            applies_to=QueryAppliesTo.GROUND,
        ),
        QueryExample(
            name="dense_capacity_binds",
            question_answered="Does the space capacity ceiling bind in the dense regime?",
            jq_expression=".comparison.by_density.dense.space_capacity_binds.value",
            expected_shape="boolean (true in dense)",
            important_paths=["comparison.by_density.dense.space_capacity_binds"],
            applies_to=QueryAppliesTo.GROUND,
        ),
        QueryExample(
            name="revenue_ceiling_reconciliation",
            question_answered="Is the priced revenue collectable (under both ceilings)?",
            jq_expression=".comparison.revenue_ceiling.collectable_win.value",
            expected_shape="boolean (the collectable-win gate)",
            important_paths=["comparison.revenue_ceiling"],
            applies_to=QueryAppliesTo.GROUND,
        ),
        QueryExample(
            name="starlink_floor_honesty",
            question_answered="What is the chain figure vs the disclosed Starlink floor?",
            jq_expression=(
                "{chain: .comparison.starlink_floor.bottom_up_chain_cost_usd_per_sub_year.value, "
                "floor: .comparison.starlink_floor.disclosed_starlink_floor_usd_per_sub_year.value}"
            ),
            expected_shape="object with both figures shown and labeled",
            important_paths=["comparison.starlink_floor"],
            applies_to=QueryAppliesTo.GROUND,
        ),
        QueryExample(
            name="density_crossover_note",
            question_answered="Where do sparse and dense roughly cross over?",
            jq_expression=".ground.crossover_note_usd_per_sub_year",
            expected_shape="ProvenanceCell (about $490/sub/yr, COMM-103)",
            important_paths=["ground.crossover_note_usd_per_sub_year"],
            applies_to=QueryAppliesTo.GROUND,
        ),
    ]


__all__ = [
    "DEFAULT_GROUND_SCENARIO_PATH",
    "DensityRegime",
    "GroundComparisonAnchor",
    "GroundCostByDensity",
    "GroundCostComponent",
    "GroundCostResult",
    "GroundReferenceConfig",
    "GroundReferenceOutput",
    "SourceCatalog",
    "SpaceReferenceResult",
    "build_ground_reference_output",
    "default_ground_source_catalog",
    "ground_config_from_comms_config",
    "promote_default_ground_reference",
    "render_ground_json",
]
