"""The comms comparison block: the cost-vs-ground map (per density) plus fleet-wide checks.

This module builds the PER-DENSITY cost-to-cost ratio and price-undercut check
(reported separately for the SPARSE and DENSE regimes, DESIGN.md Section 7) plus
the FLEET-WIDE revenue-ceiling reconciliation and the Starlink-floor honesty
block. The two density ratios point in OPPOSITE directions (space wins the
unserved/remote fringe on cost, loses the dense served market), which is the
whole reason they are reported separately; the model NEVER blends them into a
single comms-wide ratio. The output is a MAP (where space wins/loses on cost),
not one number.

The module emits NO conclusion label, NO verdict string, NO recommendation: the
comparison carries the ratio NUMBERS and the comparison FLAGS (booleans), and the
editorial judgement is hand-written in Phase 6 (plan Section 0.9, the
baked-in-conclusion gate). Boolean cells are ``ProvenanceCell``s whose value is a
Python ``bool`` (a queryable comparison flag), NOT a verdict label.

IMPORT-DIRECTION DECISION (stated so the wiring is one-way and there is no runtime
import cycle): ``ground.py`` imports the comparison BUILDER and the
``CommsComparison`` type from this module at module level, and calls
:func:`build_comms_comparison` from inside its ``build_ground_reference_output``.
This module imports the ground RESULT types (``GroundCostByDensity``,
``GroundCostResult``, ``SpaceReferenceResult``) it needs ONLY for annotations under
``if TYPE_CHECKING`` (as forward-reference strings). The value-neutral
``DensityRegime`` enum, which BOTH modules need at class-build time (it is a Pydantic
field type and its members are read at runtime), lives in the leaf
``communications.constants`` module and is imported from there by both sides
(``communications.ground`` re-exports it). So the only module-load edge is
ground -> comparison; there is no cycle.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Final

from pydantic import BaseModel, ConfigDict, Field

from common.meta import ValidationResult, ValidationSeverity
from common.provenance import FieldPath, ProvenanceCell, cell
from communications.config import PriceReferenceDials
from communications.constants import (
    MONTHS_PER_YEAR,
    SPACE_MATERIALLY_CHEAPER_RATIO,
    DensityRegime,
)
from communications.output import CommsModelOutput, CustomerBandBlock

if TYPE_CHECKING:
    from communications.ground import (
        GroundCostByDensity,
        GroundCostResult,
        SpaceReferenceResult,
    )

logger = logging.getLogger(__name__)


# ===========================================================================
# Named constants (the "no bare literals" rule)
# ===========================================================================

EPSILON_RATIO_DENOMINATOR: Final[float] = 0.0
"""The zero-denominator guard value for the safe-ratio helper: a denominator
equal to this triggers the None / fail-fast path (mirroring the DC ground
ZERO_COST guard). A cost-to-cost denominator of zero is a build error, never a
silent ratio."""

STARLINK_FLOOR_HONESTY_NOTE: Final[str] = (
    "Both the bottom-up space chain figure and the disclosed all-in Starlink "
    "floor are shown and labeled. The model never claims the bottom-up chain "
    "beats the disclosed all-in Starlink number; being below the disclosed "
    "floor is reported, not asserted as a win."
)
"""The fixed honesty-note text for the dual-space-cost rule (plan Section 0.9).
Carried as a named constant so it is not a bare inline literal."""

_BOOL_UNIT: Final[str] = "bool"
"""The unit string for a boolean comparison-flag ProvenanceCell."""

_USD_UNIT: Final[str] = "USD"
"""The unit string for a per-subscriber annual cost / dollar ProvenanceCell."""

_RATIO_UNIT: Final[str] = "ratio"
"""The unit string for a dimensionless cost-to-cost ratio ProvenanceCell."""

_COST_RATIO_CLAIM: Final[str] = "research/economics/comms_ground_vs_space_cost_ratio.md"
"""The durable research doc backing the per-density cost-to-cost ratio."""


# ===========================================================================
# Data structures (frozen Pydantic models)
# ===========================================================================


class CostToCostComparison(BaseModel):
    """The cost-to-cost ratio for ONE density regime: space cost vs that regime's ground cost.

    The headline comparison (the data-center spine), computed once per density
    regime (sparse fresh-build, dense incumbent-marginal). Both sides carry the
    SAME 1.5x margin, so it cancels and what falls out is a pure cost-structure
    ratio; the ratio is computed on the UNPRICED per-subscriber costs. The ratio
    is a BAND because the space per-customer cost is a band (the ground cost is a
    scalar); the ratio band follows the space cost band ordering (ratio-low uses
    the space cost-low member, which is the served-high member). The SAME space
    cost feeds both regimes (coverage is flat); only the ground denominator
    differs. Emits NO conclusion label.
    """

    model_config = ConfigDict(frozen=True)

    regime: DensityRegime = Field(
        ..., description="Which density regime this ratio is for (sparse vs dense)."
    )
    space_cost_per_subscriber_usd: ProvenanceCell = Field(
        ...,
        description=(
            "Space bottom-up per-customer cost, MID band member, USD/yr (same both regimes)."
        ),
    )
    ground_cost_per_subscriber_usd: ProvenanceCell = Field(
        ..., description="This regime's ground bottom-up per-subscriber cost, USD/yr."
    )
    space_to_ground_ratio_low: ProvenanceCell = Field(
        ..., description="Space cost-low member / ground cost (the cheapest-space ratio)."
    )
    space_to_ground_ratio_mid: ProvenanceCell = Field(
        ..., description="Space cost-mid / ground cost (the headline ratio for this regime)."
    )
    space_to_ground_ratio_high: ProvenanceCell = Field(
        ..., description="Space cost-high member / ground cost."
    )
    ground_to_space_ratio_mid: ProvenanceCell = Field(
        ..., description="Ground cost / space cost-mid (the inverse headline ratio)."
    )
    absolute_delta_per_subscriber_usd: ProvenanceCell = Field(
        ..., description="Ground per-subscriber cost minus space per-customer cost (MID), USD/yr."
    )
    space_is_cheaper: ProvenanceCell = Field(
        ...,
        description=(
            "Boolean flag: does space cost less than ground in THIS regime at the MID band "
            "(ground_to_space_ratio_mid > 1.0). Expected True in sparse, False in dense. A "
            "comparison flag, NOT a verdict label."
        ),
    )
    notes: str = Field(
        ...,
        description=(
            "How to read the cost-to-cost ratio for this regime (same 1.5x both sides cancels; a "
            "pure cost-structure ratio; not a market prediction)."
        ),
    )


class PriceUndercutCheck(BaseModel):
    """The market test for ONE density regime: does the priced cost land under the price-to-beat.

    The space priced per-customer cost (cost x 1.5) vs the regime's price-to-beat.
    In the SPARSE regime the price-to-beat is the founder-set retail reference
    (about $100/month of full cell service, annualized; the unserved fringe has no
    incumbent floor). In the DENSE regime the price-to-beat is the incumbent's
    marginal defend cost (the served-market floor the entrant must beat, far below
    retail; COMM-096 / COMM-098). If under, we win by undercutting THAT regime.
    This is the market test emitted as NUMBERS and a boolean PER REGIME, NOT a
    verdict string.
    """

    model_config = ConfigDict(frozen=True)

    regime: DensityRegime = Field(
        ..., description="Which density regime this undercut check is for (sparse vs dense)."
    )
    space_priced_cost_per_subscriber_usd: ProvenanceCell = Field(
        ...,
        description="Space priced per-customer cost, MID band member (cost x 1.5), USD/yr.",
    )
    price_to_beat_usd_per_year: ProvenanceCell = Field(
        ...,
        description=(
            "This regime's price-to-beat annualized, USD/yr (sparse: the retail reference; dense: "
            "the incumbent marginal defend cost)."
        ),
    )
    price_to_beat_basis: str = Field(
        ...,
        description=(
            "What the price-to-beat is ('retail_reference' for sparse, "
            "'incumbent_marginal_defend_cost' for dense)."
        ),
    )
    undercut_headroom_usd_per_year: ProvenanceCell = Field(
        ...,
        description="Price-to-beat minus space priced cost, USD/yr (positive = undercuts).",
    )
    undercut_passes: ProvenanceCell = Field(
        ...,
        description=(
            "Boolean flag: does the space priced cost land under THIS regime's price-to-beat at "
            "the MID band. The market test, NOT a verdict label."
        ),
    )
    notes: str = Field(
        ...,
        description=(
            "How to read the undercut check for this regime (which price-to-beat applies and why; "
            "sparse beats retail, dense must beat the marginal floor)."
        ),
    )


class DensityRegimeComparison(BaseModel):
    """The complete comparison for ONE density regime: cost-to-cost, price undercut, capacity flag.

    Wraps the per-regime cost-to-cost ratio and price undercut, plus the
    ``space_capacity_binds`` flag stating whether the space capacity ceiling BINDS
    in this regime (SPECTRUM_spec.md Section 3): in the SPARSE regime coverage
    reaches everyone and capacity has headroom (binds = False); in the DENSE
    regime capacity binds because a beam cannot densify (binds = True). REPORTED
    per regime, no verdict string.
    """

    model_config = ConfigDict(frozen=True)

    regime: DensityRegime = Field(..., description="Which density regime (sparse vs dense).")
    cost_to_cost: CostToCostComparison = Field(
        ..., description="The cost-to-cost ratio for this regime."
    )
    price_undercut: PriceUndercutCheck = Field(
        ..., description="The price-undercut market test for this regime."
    )
    space_capacity_binds: ProvenanceCell = Field(
        ...,
        description=(
            "Boolean flag: does the space capacity ceiling bind in this regime (False in sparse, "
            "True in dense; SPECTRUM_spec.md Section 3). A reported physics flag, NOT a verdict."
        ),
    )
    notes: str = Field(
        ...,
        description=(
            "How to read this regime's comparison (sparse: space wins on cost, capacity has "
            "headroom; dense: space loses on cost, capacity binds)."
        ),
    )


class ComparisonByDensity(BaseModel):
    """The per-density comparison: the SPARSE regime and the DENSE regime side by side.

    Carries the two ``DensityRegimeComparison`` objects (DESIGN.md Section 7). The
    two ratios point in OPPOSITE directions (space wins sparse, loses dense), which
    is the whole point of reporting them separately; the model never blends them
    into a single comms-wide ratio. This is the structure the Phase-6 conclusion's
    MAP framing reads off.
    """

    model_config = ConfigDict(frozen=True)

    sparse: DensityRegimeComparison = Field(
        ...,
        description=(
            "The unserved/remote-fringe comparison (fresh-build ground; space wins on cost)."
        ),
    )
    dense: DensityRegimeComparison = Field(
        ...,
        description=(
            "The served-market comparison (incumbent marginal-cost floor; space loses on cost)."
        ),
    )


class RevenueCeilingReconciliation(BaseModel):
    """The revenue-ceiling reconciliation (the one genuinely-new check vs the DC ground module).

    The space priced per-customer revenue (cost x 1.5) reconciled against the
    collectable revenue (ARPU x operator-share, the ``arpu_collectable_revenue_usd``
    cell the engine emits) AND against the retail reference. The priced cost must
    land under BOTH to count as a collectable win (plan Section 0.9, the
    revenue-ceiling gate). A priced revenue presented as collectable above either
    ceiling is forbidden. This block REPORTS the reconciliation; the boolean gate
    flags whether it holds. It is fleet-wide (a property of the space cost and the
    ARPU, not of ground density), so it is reported once.
    """

    model_config = ConfigDict(frozen=True)

    priced_revenue_per_subscriber_usd: ProvenanceCell = Field(
        ...,
        description="The space priced per-customer revenue, MID band member (cost x 1.5), USD/yr.",
    )
    arpu_collectable_revenue_usd: ProvenanceCell = Field(
        ...,
        description=(
            "The collectable revenue ceiling (ARPU x 12 x operator-share), USD/yr, read off the "
            "space output."
        ),
    )
    retail_reference_usd_per_year: ProvenanceCell = Field(
        ..., description="The retail reference annualized, USD/yr."
    )
    priced_below_collectable: ProvenanceCell = Field(
        ...,
        description="Boolean flag: is the priced revenue at or below the ARPU-collectable ceiling.",
    )
    priced_below_retail: ProvenanceCell = Field(
        ..., description="Boolean flag: is the priced revenue at or below the retail reference."
    )
    collectable_win: ProvenanceCell = Field(
        ...,
        description=(
            "Boolean flag: priced revenue is at or below BOTH ceilings (the collectable-win gate)."
        ),
    )
    notes: str = Field(
        ...,
        description=(
            "How to read the reconciliation (the priced revenue is cost x 1.5; the ceilings are "
            "the retail reference and ARPU x operator-share; a collectable win needs the priced "
            "cost under both)."
        ),
    )


class StarlinkFloorHonesty(BaseModel):
    """The dual-space-cost rule: show the bottom-up chain figure AND the disclosed Starlink floor.

    Both the bottom-up space per-customer cost (the chain figure) AND the disclosed
    all-in Starlink floor are shown and labeled; the model NEVER asserts the chain
    beats the disclosed number as a win (plan Section 0.9, the Starlink-floor
    honesty gate). The ``chain_below_disclosed_floor`` flag is REPORTED with an
    explicit statement that being below the disclosed floor is NOT claimed as a
    win. It is fleet-wide (both figures are space supply costs, not ground density
    numbers), so it is reported once.
    """

    model_config = ConfigDict(frozen=True)

    bottom_up_chain_cost_usd_per_sub_year: ProvenanceCell = Field(
        ...,
        description=(
            "The bottom-up space per-customer cost (the chain figure), MID band member, USD/yr."
        ),
    )
    disclosed_starlink_floor_usd_per_sub_year: ProvenanceCell = Field(
        ...,
        description=(
            "The disclosed all-in Starlink floor, USD/yr (a third-party / disclosed-financials "
            "reference, not a Rocket Lab figure)."
        ),
    )
    chain_below_disclosed_floor: ProvenanceCell = Field(
        ...,
        description=(
            "Boolean flag: is the bottom-up chain figure below the disclosed Starlink floor. "
            "REPORTED only; being below is NOT asserted as a win."
        ),
    )
    honesty_note: str = Field(
        ...,
        description=(
            "Explicit statement that both figures are shown and labeled, and the model never "
            "claims the bottom-up chain beats the disclosed all-in Starlink number."
        ),
    )


class CommsComparison(BaseModel):
    """The complete comms comparison block: per-density faces plus fleet-wide faces, no verdict.

    Carries the PER-DENSITY comparison (the sparse and dense cost-to-cost ratios
    and price undercuts, in ``by_density``) AND the FLEET-WIDE faces that do not
    differ by density (the revenue-ceiling reconciliation and the Starlink-floor
    honesty block, which are space-side properties of the priced cost and the
    ARPU, not of ground density). Emits NO conclusion label, NO verdict, NO
    recommendation (plan Section 0.9, the baked-in-conclusion gate). The editorial
    judgement is Phase 6, hand-written.
    """

    model_config = ConfigDict(frozen=True)

    by_density: ComparisonByDensity = Field(
        ...,
        description=(
            "The per-density comparison: sparse and dense cost-to-cost ratios and price undercuts "
            "(DESIGN.md Section 7)."
        ),
    )
    revenue_ceiling: RevenueCeilingReconciliation = Field(
        ...,
        description="The revenue-ceiling reconciliation, fleet-wide (space-side, not per density).",
    )
    starlink_floor: StarlinkFloorHonesty = Field(
        ...,
        description="The dual-space-cost honesty block, fleet-wide (space-side, not per density).",
    )
    warnings: list[ValidationResult] = Field(
        ...,
        description="Comparison-scope warnings (including the density-split scope warning).",
    )


# ===========================================================================
# Unwrap / ratio helpers
# ===========================================================================


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


def _safe_ratio(numerator: float, denominator: float) -> float | None:
    """Return ``numerator / denominator`` or ``None`` when the denominator is zero."""
    if denominator == EPSILON_RATIO_DENOMINATOR:
        logger.warning("comms comparison ratio requested with zero denominator")
        return None
    return numerator / denominator


def _required_ratio(numerator: float, denominator: float, denominator_path: str) -> float:
    """Return a ratio, failing fast when a required denominator is zero."""
    ratio = _safe_ratio(numerator, denominator)
    if ratio is None:
        raise ValueError(f"{denominator_path} must be non-zero for the comms comparison")
    return ratio


def _flag_cell(
    *, value: bool, formula_name: str, uses: list[FieldPath], sources: list[str], description: str
) -> ProvenanceCell:
    """Build a boolean comparison-flag ProvenanceCell (unit 'bool')."""
    return cell(
        value=value,
        unit=_BOOL_UNIT,
        formula_name=formula_name,
        uses=uses,
        sources=sources,
        description=description,
    )


def _usd_cell(
    *, value: float, formula_name: str, uses: list[FieldPath], sources: list[str], description: str
) -> ProvenanceCell:
    """Build a USD/yr ProvenanceCell."""
    return cell(
        value=value,
        unit=_USD_UNIT,
        formula_name=formula_name,
        uses=uses,
        sources=sources,
        description=description,
    )


def _ratio_cell(
    *, value: float, formula_name: str, uses: list[FieldPath], sources: list[str], description: str
) -> ProvenanceCell:
    """Build a dimensionless ratio ProvenanceCell."""
    return cell(
        value=value,
        unit=_RATIO_UNIT,
        formula_name=formula_name,
        uses=uses,
        sources=sources,
        description=description,
    )


# ===========================================================================
# Per-regime and fleet-wide builders
# ===========================================================================


def _space_cost_band(space_output: CommsModelOutput) -> CustomerBandBlock:
    """Read the steady-state space per-customer cost band off the in-memory output."""
    key = str(space_output.metadata.steady_state_year)
    return space_output.business.years[key].cost_annual_per_customer_usd


def _space_priced_band(space_output: CommsModelOutput) -> CustomerBandBlock:
    """Read the steady-state space priced per-customer cost band off the in-memory output."""
    key = str(space_output.metadata.steady_state_year)
    return space_output.business.years[key].priced_cost_per_customer_usd


def _arpu_collectable_cell(space_output: CommsModelOutput) -> ProvenanceCell:
    """Read the steady-state ARPU-collectable revenue cell off the in-memory output."""
    key = str(space_output.metadata.steady_state_year)
    return space_output.business.years[key].arpu_collectable_revenue_usd


def _build_cost_to_cost(
    *,
    regime: DensityRegime,
    ground_cost: GroundCostResult,
    space_output: CommsModelOutput,
) -> CostToCostComparison:
    """Build the cost-to-cost ratio for one density regime.

    The ratio is computed on the UNPRICED per-subscriber costs (the SAME 1.5x both
    sides cancels). The ratio band follows the space cost band ordering: ratio-low
    uses the space cost-low member.
    """
    band = _space_cost_band(space_output)
    ground_path = f"ground.{regime.value}.cost_annual_per_subscriber_usd"
    space_path = "business.years.<steady>.cost_annual_per_customer_usd"

    space_low = _cell_float(band.low)
    space_mid = _cell_float(band.mid)
    space_high = _cell_float(band.high)
    ground_value = _cell_float(ground_cost.cost_annual_per_subscriber_usd)

    ratio_low = _required_ratio(space_low, ground_value, ground_path)
    ratio_mid = _required_ratio(space_mid, ground_value, ground_path)
    ratio_high = _required_ratio(space_high, ground_value, ground_path)
    ground_over_space_mid = _required_ratio(ground_value, space_mid, f"{space_path}.mid")
    absolute_delta = ground_value - space_mid
    space_is_cheaper = ground_over_space_mid > SPACE_MATERIALLY_CHEAPER_RATIO

    sources = [_COST_RATIO_CLAIM]
    return CostToCostComparison(
        regime=regime,
        space_cost_per_subscriber_usd=_usd_cell(
            value=space_mid,
            formula_name="comms_cost_to_cost_ratio_space_over_ground",
            uses=[f"{space_path}.mid"],
            sources=sources,
            description=(
                "Space bottom-up per-customer cost, MID band member (same on both regimes)."
            ),
        ),
        ground_cost_per_subscriber_usd=_usd_cell(
            value=ground_value,
            formula_name="comms_ground_total_per_sub_from_lines",
            uses=[ground_path],
            sources=sources,
            description=f"The {regime.value} ground bottom-up per-subscriber cost.",
        ),
        space_to_ground_ratio_low=_ratio_cell(
            value=ratio_low,
            formula_name="comms_cost_to_cost_ratio_space_over_ground",
            uses=[f"{space_path}.low", ground_path],
            sources=sources,
            description="Space cost-low member / ground cost (the cheapest-space ratio).",
        ),
        space_to_ground_ratio_mid=_ratio_cell(
            value=ratio_mid,
            formula_name="comms_cost_to_cost_ratio_space_over_ground",
            uses=[f"{space_path}.mid", ground_path],
            sources=sources,
            description="Space cost-mid / ground cost (the headline ratio for this regime).",
        ),
        space_to_ground_ratio_high=_ratio_cell(
            value=ratio_high,
            formula_name="comms_cost_to_cost_ratio_space_over_ground",
            uses=[f"{space_path}.high", ground_path],
            sources=sources,
            description="Space cost-high member / ground cost.",
        ),
        ground_to_space_ratio_mid=_ratio_cell(
            value=ground_over_space_mid,
            formula_name="comms_cost_to_cost_ratio_ground_over_space",
            uses=[ground_path, f"{space_path}.mid"],
            sources=sources,
            description="Ground cost / space cost-mid (the inverse headline ratio).",
        ),
        absolute_delta_per_subscriber_usd=_usd_cell(
            value=absolute_delta,
            formula_name="comms_cost_to_cost_absolute_delta",
            uses=[ground_path, f"{space_path}.mid"],
            sources=sources,
            description="Ground per-subscriber cost minus space per-customer cost (MID), USD/yr.",
        ),
        space_is_cheaper=_flag_cell(
            value=space_is_cheaper,
            formula_name="comms_space_is_cheaper_flag",
            uses=[ground_path, f"{space_path}.mid"],
            sources=sources,
            description=(
                "Comparison flag (not an editorial call): space costs less than ground at the "
                f"mid band in the {regime.value} regime."
            ),
        ),
        notes=(
            "The same 1.5x margin is applied to both sides, so it cancels and this is a pure "
            "cost-structure ratio (the data-center spine), not a market prediction. The space "
            "cost is the same on both density regimes (coverage is flat); only the ground "
            "denominator differs."
        ),
    )


def _build_price_undercut(
    *,
    regime: DensityRegime,
    ground_cost: GroundCostResult,
    space_output: CommsModelOutput,
    price_reference_config: PriceReferenceDials,
) -> PriceUndercutCheck:
    """Build the price-undercut check for one density regime.

    The price-to-beat differs by regime: SPARSE uses the founder-set retail
    reference (annualized); DENSE uses this regime's own ground cost (the incumbent
    marginal defend floor).
    """
    priced_band = _space_priced_band(space_output)
    space_priced_mid = _cell_float(priced_band.mid)
    space_priced_path = "business.years.<steady>.priced_cost_per_customer_usd.mid"

    if regime is DensityRegime.SPARSE:
        price_to_beat = price_reference_config.retail_reference_usd_per_month * MONTHS_PER_YEAR
        price_to_beat_basis = "retail_reference"
        price_to_beat_formula = "comms_retail_reference_annualized"
        price_to_beat_uses: list[FieldPath] = [
            "inputs.config.price_reference.retail_reference_usd_per_month"
        ]
        price_to_beat_sources = ["founder-set retail reference"]
        price_to_beat_desc = (
            "The founder-set retail reference annualized, the sparse-regime price-to-beat, USD/yr."
        )
    else:
        price_to_beat = _cell_float(ground_cost.cost_annual_per_subscriber_usd)
        price_to_beat_basis = "incumbent_marginal_defend_cost"
        price_to_beat_formula = "comms_ground_dense_incumbent_marginal_per_sub"
        price_to_beat_uses = ["ground.dense.cost_annual_per_subscriber_usd"]
        price_to_beat_sources = ["COMM-096", "COMM-098"]
        price_to_beat_desc = (
            "The dense-regime price-to-beat: the incumbent marginal defend cost (COMM-096), the "
            "served-market floor the entrant must beat, USD/yr."
        )

    headroom = price_to_beat - space_priced_mid
    undercut_passes = space_priced_mid <= price_to_beat

    return PriceUndercutCheck(
        regime=regime,
        space_priced_cost_per_subscriber_usd=_usd_cell(
            value=space_priced_mid,
            formula_name="comms_priced_cost_from_cost_and_multiple",
            uses=[space_priced_path],
            sources=[_COST_RATIO_CLAIM],
            description="Space priced per-customer cost, MID band member (cost x 1.5), USD/yr.",
        ),
        price_to_beat_usd_per_year=_usd_cell(
            value=price_to_beat,
            formula_name=price_to_beat_formula,
            uses=price_to_beat_uses,
            sources=price_to_beat_sources,
            description=price_to_beat_desc,
        ),
        price_to_beat_basis=price_to_beat_basis,
        undercut_headroom_usd_per_year=_usd_cell(
            value=headroom,
            formula_name="comms_price_undercut_headroom",
            uses=[space_priced_path],
            sources=price_to_beat_sources,
            description="Price-to-beat minus space priced cost, USD/yr (positive = undercuts).",
        ),
        undercut_passes=_flag_cell(
            value=undercut_passes,
            formula_name="comms_price_undercut_passes_flag",
            uses=[space_priced_path],
            sources=price_to_beat_sources,
            description=(
                "Market-test flag (not an editorial call): the space priced cost lands under "
                f"this regime's price-to-beat in the {regime.value} regime."
            ),
        ),
        notes=(
            "Sparse: the price-to-beat is the founder-set retail reference (the unserved fringe "
            "has no incumbent floor). Dense: the price-to-beat is the incumbent marginal defend "
            "floor, far below retail (COMM-096 / COMM-098); the entrant must beat the floor, not "
            "the list price."
        ),
    )


def _build_capacity_binds_cell(regime: DensityRegime) -> ProvenanceCell:
    """Build the per-regime space_capacity_binds physics flag (False sparse, True dense)."""
    binds = regime is DensityRegime.DENSE
    return _flag_cell(
        value=binds,
        formula_name="comms_space_capacity_binds_by_regime",
        uses=["business.years.<steady>.total_served"],
        sources=["research/direct_communication/spectrum_generations_and_availability.md"],
        description=(
            "Physics flag (not an editorial call, SPECTRUM_spec.md Section 3): the space "
            f"capacity ceiling binds in the {regime.value} regime "
            + ("(a beam cannot densify)." if binds else "(coverage has headroom).")
        ),
    )


def _build_regime_comparison(
    *,
    regime: DensityRegime,
    ground_cost: GroundCostResult,
    space_output: CommsModelOutput,
    price_reference_config: PriceReferenceDials,
) -> DensityRegimeComparison:
    """Build the complete comparison for one density regime."""
    cost_to_cost = _build_cost_to_cost(
        regime=regime, ground_cost=ground_cost, space_output=space_output
    )
    price_undercut = _build_price_undercut(
        regime=regime,
        ground_cost=ground_cost,
        space_output=space_output,
        price_reference_config=price_reference_config,
    )
    capacity_binds = _build_capacity_binds_cell(regime)
    if regime is DensityRegime.SPARSE:
        notes = (
            "Space wins on cost in the unserved/remote fringe (the fresh-build ground denominator "
            "is far above the modeled space cost) and capacity has headroom (coverage reaches "
            "everyone)."
        )
    else:
        notes = (
            "Space loses on cost in the served market (the incumbent marginal defend floor is far "
            "below the space cost) and capacity binds (a beam cannot densify below its footprint)."
        )
    return DensityRegimeComparison(
        regime=regime,
        cost_to_cost=cost_to_cost,
        price_undercut=price_undercut,
        space_capacity_binds=capacity_binds,
        notes=notes,
    )


def _build_revenue_ceiling(
    *,
    space_output: CommsModelOutput,
    price_reference_config: PriceReferenceDials,
) -> RevenueCeilingReconciliation:
    """Build the fleet-wide revenue-ceiling reconciliation."""
    priced_band = _space_priced_band(space_output)
    priced_mid = _cell_float(priced_band.mid)
    arpu_collectable_source = _arpu_collectable_cell(space_output)
    arpu_collectable = _cell_float(arpu_collectable_source)
    retail_annual = price_reference_config.retail_reference_usd_per_month * MONTHS_PER_YEAR

    priced_below_collectable = priced_mid <= arpu_collectable
    priced_below_retail = priced_mid <= retail_annual
    collectable_win = priced_below_collectable and priced_below_retail

    priced_path = "business.years.<steady>.priced_cost_per_customer_usd.mid"
    arpu_path = "business.years.<steady>.arpu_collectable_revenue_usd"
    retail_path = "inputs.config.price_reference.retail_reference_usd_per_month"

    return RevenueCeilingReconciliation(
        priced_revenue_per_subscriber_usd=_usd_cell(
            value=priced_mid,
            formula_name="comms_priced_cost_from_cost_and_multiple",
            uses=[priced_path],
            sources=[_COST_RATIO_CLAIM],
            description=(
                "The space priced per-customer revenue, MID band member (cost x 1.5), USD/yr."
            ),
        ),
        arpu_collectable_revenue_usd=_usd_cell(
            value=arpu_collectable,
            formula_name="comms_arpu_collectable_revenue_from_arpu_and_share",
            uses=[arpu_path],
            sources=["COMM-090"],
            description="The collectable revenue ceiling (ARPU x 12 x operator-share), USD/yr.",
        ),
        retail_reference_usd_per_year=_usd_cell(
            value=retail_annual,
            formula_name="comms_retail_reference_annualized",
            uses=[retail_path],
            sources=["founder-set retail reference"],
            description="The retail reference annualized, USD/yr.",
        ),
        priced_below_collectable=_flag_cell(
            value=priced_below_collectable,
            formula_name="comms_priced_below_collectable_flag",
            uses=[priced_path, arpu_path],
            sources=["COMM-090"],
            description="Flag: the priced revenue is at or below the ARPU-collectable ceiling.",
        ),
        priced_below_retail=_flag_cell(
            value=priced_below_retail,
            formula_name="comms_priced_below_retail_flag",
            uses=[priced_path, retail_path],
            sources=["founder-set retail reference"],
            description="Flag: the priced revenue is at or below the retail reference.",
        ),
        collectable_win=_flag_cell(
            value=collectable_win,
            formula_name="comms_collectable_win_flag",
            uses=[priced_path, arpu_path, retail_path],
            sources=["COMM-090", "founder-set retail reference"],
            description=(
                "Flag: the priced revenue is at or below BOTH the ARPU-collectable ceiling and the "
                "retail reference (the collectable-win gate)."
            ),
        ),
        notes=(
            "The priced revenue is the space per-customer cost x 1.5. The ceilings are the retail "
            "reference and ARPU x operator-share. A collectable win needs the priced cost under "
            "both ceilings (plan Section 0.9, the revenue-ceiling gate)."
        ),
    )


def _build_starlink_floor(
    *,
    space_output: CommsModelOutput,
    space_reference: SpaceReferenceResult,
) -> StarlinkFloorHonesty:
    """Build the fleet-wide Starlink-floor honesty block (the dual-space-cost rule)."""
    band = _space_cost_band(space_output)
    chain_mid = _cell_float(band.mid)
    disclosed_floor = _cell_float(space_reference.disclosed_starlink_floor_usd_per_sub_year)
    chain_below = chain_mid < disclosed_floor

    chain_path = "business.years.<steady>.cost_annual_per_customer_usd.mid"
    floor_path = "space_reference.disclosed_starlink_floor_usd_per_sub_year"

    return StarlinkFloorHonesty(
        bottom_up_chain_cost_usd_per_sub_year=_usd_cell(
            value=chain_mid,
            formula_name="comms_cost_to_cost_ratio_space_over_ground",
            uses=[chain_path],
            sources=[_COST_RATIO_CLAIM],
            description=(
                "The bottom-up space per-customer cost (the chain figure), MID member, USD/yr."
            ),
        ),
        disclosed_starlink_floor_usd_per_sub_year=_usd_cell(
            value=disclosed_floor,
            formula_name="comms_disclosed_starlink_floor_passthrough",
            uses=[floor_path],
            sources=["COMM-090", "COMM-103"],
            description=(
                "The disclosed all-in Starlink floor, USD/yr (a disclosed-financials reference, "
                "not a Rocket Lab figure)."
            ),
        ),
        chain_below_disclosed_floor=_flag_cell(
            value=chain_below,
            formula_name="comms_chain_below_disclosed_floor_flag",
            uses=[chain_path, floor_path],
            sources=["COMM-090", "COMM-103"],
            description=(
                "Flag (reported only): the bottom-up chain figure is below the disclosed Starlink "
                "floor. Being below is NOT claimed as a win."
            ),
        ),
        honesty_note=STARLINK_FLOOR_HONESTY_NOTE,
    )


def _comparison_scope_warnings() -> list[ValidationResult]:
    """Emit the comparison-scope warning, including the density-split note."""
    return [
        ValidationResult(
            validation_id="comms_comparison_order_of_magnitude_map",
            severity=ValidationSeverity.WARN,
            what_tested="Comparison interpretation and the sparse-vs-dense split.",
            expected_condition=(
                "The comparison is a per-density MAP (the two ratios point in opposite directions "
                "by design), the retail reference is founder-set, and the editorial judgement is "
                "hand-written in Phase 6."
            ),
            observed_result=(
                "Order-of-magnitude cost screen reported per density regime; the sparse-vs-dense "
                "crossover is a zone, not a sharp point (about the dense-suburban fringe, "
                "COMM-103); the editorial judgement is hand-written in Phase 6, not asserted here."
            ),
            related_json_paths=[
                "comparison.by_density.sparse",
                "comparison.by_density.dense",
            ],
            remediation_hint=(
                "Read the sparse and dense regimes separately; do not blend them into a single "
                "comms-wide ratio."
            ),
        )
    ]


# ===========================================================================
# Public builder
# ===========================================================================


def build_comms_comparison(
    *,
    ground: GroundCostByDensity,
    space_reference: SpaceReferenceResult,
    price_reference_config: PriceReferenceDials,
    space_output: CommsModelOutput,
) -> CommsComparison:
    """Build the comms comparison block from the per-density ground cost and space reference.

    Computes, FOR EACH density regime (sparse, dense), the cost-to-cost ratio
    (same ``REVENUE_MULTIPLE`` both sides, the SAME space cost on both, only the
    ground denominator differing) and the price undercut (sparse vs the retail
    reference, dense vs the incumbent marginal defend cost) plus the
    ``space_capacity_binds`` flag; then the FLEET-WIDE revenue-ceiling
    reconciliation (the priced revenue vs the ARPU-collectable cell read off
    ``space_output`` and vs the retail reference) and the Starlink-floor honesty
    block (the bottom-up chain figure vs the disclosed Starlink floor carried on
    ``space_reference``). Emits NO conclusion label and NO verdict string.

    Args:
        ground: The bottom-up ground per-subscriber cost in BOTH density regimes.
        space_reference: The space-model per-subscriber cost view (same on both regimes).
        price_reference_config: The price/collectability dials (retail reference, ARPU, share).
            Named ``price_reference`` per plan Amendment A1 (demand is assumed, not modeled).
        space_output: The in-memory comms space output (read for the ARPU-collectable cell and
            the steady-state per-customer cost band).

    Returns:
        A frozen :class:`CommsComparison`.
    """
    sparse = _build_regime_comparison(
        regime=DensityRegime.SPARSE,
        ground_cost=ground.sparse,
        space_output=space_output,
        price_reference_config=price_reference_config,
    )
    dense = _build_regime_comparison(
        regime=DensityRegime.DENSE,
        ground_cost=ground.dense,
        space_output=space_output,
        price_reference_config=price_reference_config,
    )
    revenue_ceiling = _build_revenue_ceiling(
        space_output=space_output, price_reference_config=price_reference_config
    )
    starlink_floor = _build_starlink_floor(
        space_output=space_output, space_reference=space_reference
    )
    return CommsComparison(
        by_density=ComparisonByDensity(sparse=sparse, dense=dense),
        revenue_ceiling=revenue_ceiling,
        starlink_floor=starlink_floor,
        warnings=_comparison_scope_warnings(),
    )


__all__ = [
    "CommsComparison",
    "ComparisonByDensity",
    "CostToCostComparison",
    "DensityRegimeComparison",
    "PriceUndercutCheck",
    "RevenueCeilingReconciliation",
    "StarlinkFloorHonesty",
    "build_comms_comparison",
]
