"""Tests for the comms comparison module (the cost-vs-ground map, per density).

These tests exercise the per-density cost-to-cost ratio and price-undercut check
plus the fleet-wide revenue-ceiling reconciliation and Starlink-floor honesty
block. Several cases build a CONTROLLED CommsModelOutput (overriding the
steady-state per-customer cost band) so the opposite-direction map and the
band-ordering / margin-cancellation properties can be asserted deterministically,
independent of the optimistic default modeled space cost.
"""

from __future__ import annotations

from common.provenance import FORMULAS, ProvenanceCell, cell
from communications.comparison import (
    CommsComparison,
    ComparisonByDensity,
    CostToCostComparison,
    DensityRegimeComparison,
    PriceUndercutCheck,
    RevenueCeilingReconciliation,
    StarlinkFloorHonesty,
    build_comms_comparison,
)
from communications.config import CommsConfig
from communications.constants import MONTHS_PER_YEAR, REVENUE_MULTIPLE, DensityRegime
from communications.ground import (
    GroundReferenceConfig,
    _build_ground_cost_by_density,
    _build_space_reference_result,
    build_ground_reference_output,
    default_ground_source_catalog,
    ground_config_from_comms_config,
)
from communications.output import CommsModelOutput, CustomerBandBlock


def _num_cell(value: float, unit: str = "USD") -> ProvenanceCell:
    """Build a numeric provenance cell with a registered formula name."""
    return cell(
        value=value,
        unit=unit,
        formula_name="comms_cost_to_cost_ratio_space_over_ground",
        uses=["test"],
        sources=["test"],
        description="test cell",
    )


def _output_with_space_costs(
    base: CommsModelOutput,
    *,
    cost_low: float,
    cost_mid: float,
    cost_high: float,
    priced_mid: float,
    arpu_collectable: float | None = None,
) -> CommsModelOutput:
    """Return a copy of ``base`` with the steady-state space cost band overridden.

    Overrides the steady-state ``cost_annual_per_customer_usd`` band (low/mid/high)
    and the priced-cost MID member so the comparison arithmetic can be pinned. The
    priced low/high members are scaled from the cost members by REVENUE_MULTIPLE.
    """
    key = str(base.metadata.steady_state_year)
    by = base.business.years[key]
    cost_band = CustomerBandBlock(
        low=_num_cell(cost_low),
        mid=_num_cell(cost_mid),
        high=_num_cell(cost_high),
    )
    priced_band = CustomerBandBlock(
        low=_num_cell(cost_low * REVENUE_MULTIPLE),
        mid=_num_cell(priced_mid),
        high=_num_cell(cost_high * REVENUE_MULTIPLE),
    )
    updates: dict[str, object] = {
        "cost_annual_per_customer_usd": cost_band,
        "priced_cost_per_customer_usd": priced_band,
    }
    if arpu_collectable is not None:
        updates["arpu_collectable_revenue_usd"] = _num_cell(arpu_collectable)
    new_by = by.model_copy(update=updates)
    new_years = {**base.business.years, key: new_by}
    new_business = base.business.model_copy(update={"years": new_years})
    return base.model_copy(update={"business": new_business})


def _build_comparison_for(
    output: CommsModelOutput,
    config: CommsConfig,
) -> CommsComparison:
    """Build the full comparison block for a (possibly controlled) output."""
    ground_config = ground_config_from_comms_config(config)
    ground = _build_ground_cost_by_density(ground_config, config.price_reference)
    space_reference = _build_space_reference_result(output, ground_config)
    return build_comms_comparison(
        ground=ground,
        space_reference=space_reference,
        price_reference_config=config.price_reference,
        space_output=output,
    )


def test_comparison_reports_both_density_regimes(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
) -> None:
    """The comparison carries by_density.sparse and by_density.dense, plus the fleet-wide blocks."""
    comparison = _build_comparison_for(default_comms_output, default_comms_config)
    assert isinstance(comparison.by_density, ComparisonByDensity)
    assert comparison.by_density.sparse.regime is DensityRegime.SPARSE
    assert comparison.by_density.dense.regime is DensityRegime.DENSE
    assert isinstance(comparison.by_density.sparse, DensityRegimeComparison)
    assert isinstance(comparison.by_density.dense, DensityRegimeComparison)
    # The fleet-wide blocks are present at the top level (not duplicated per regime).
    assert isinstance(comparison.revenue_ceiling, RevenueCeilingReconciliation)
    assert isinstance(comparison.starlink_floor, StarlinkFloorHonesty)


def test_sparse_space_cheaper_dense_space_costlier(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
) -> None:
    """With a space cost between the dense floor and the sparse build, the flags oppose.

    The opposite-direction map: space wins the sparse fresh-build (far above space)
    and loses the dense incumbent floor (far below space). A controlled space cost
    of $300/sub/yr sits above the dense $90 floor and below the sparse $1080 build.
    """
    controlled = _output_with_space_costs(
        default_comms_output,
        cost_low=200.0,
        cost_mid=300.0,
        cost_high=400.0,
        priced_mid=450.0,
    )
    comparison = _build_comparison_for(controlled, default_comms_config)
    assert comparison.by_density.sparse.cost_to_cost.space_is_cheaper.value is True
    assert comparison.by_density.dense.cost_to_cost.space_is_cheaper.value is False


def test_cost_to_cost_ratio_uses_same_margin_both_sides(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
) -> None:
    """The ratio on unpriced costs equals the ratio on priced costs (the 1.5x cancels)."""
    comparison = _build_comparison_for(default_comms_output, default_comms_config)
    ctc = comparison.by_density.sparse.cost_to_cost
    space_unpriced = ctc.space_cost_per_subscriber_usd.value
    ground_unpriced = ctc.ground_cost_per_subscriber_usd.value
    assert isinstance(space_unpriced, float)
    assert isinstance(ground_unpriced, float)
    ratio_unpriced = space_unpriced / ground_unpriced
    ratio_priced = (space_unpriced * REVENUE_MULTIPLE) / (ground_unpriced * REVENUE_MULTIPLE)
    assert abs(ratio_unpriced - ratio_priced) < 1e-12
    assert abs(ctc.space_to_ground_ratio_mid.value - ratio_unpriced) < 1e-12


def test_cost_to_cost_ratio_band_follows_space_cost_band(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
) -> None:
    """The ratio band follows the space cost band; the same space cost feeds both regimes."""
    controlled = _output_with_space_costs(
        default_comms_output,
        cost_low=10.0,
        cost_mid=30.0,
        cost_high=90.0,
        priced_mid=45.0,
    )
    comparison = _build_comparison_for(controlled, default_comms_config)
    sparse_ctc = comparison.by_density.sparse.cost_to_cost
    ground = sparse_ctc.ground_cost_per_subscriber_usd.value
    assert isinstance(ground, float)
    # ratio_low uses the space cost-LOW member (10.0), ratio_high uses cost-HIGH (90.0).
    assert abs(sparse_ctc.space_to_ground_ratio_low.value - 10.0 / ground) < 1e-9
    assert abs(sparse_ctc.space_to_ground_ratio_high.value - 90.0 / ground) < 1e-9
    assert sparse_ctc.space_to_ground_ratio_low.value < sparse_ctc.space_to_ground_ratio_high.value
    # The SAME space cost feeds both regimes (coverage is flat).
    assert (
        comparison.by_density.sparse.cost_to_cost.space_cost_per_subscriber_usd.value
        == comparison.by_density.dense.cost_to_cost.space_cost_per_subscriber_usd.value
    )


def test_space_is_cheaper_flag_is_boolean_not_label(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
) -> None:
    """space_is_cheaper is a bool cell (unit 'bool'), True exactly when ground/space mid > 1."""
    # Case A: space cheaper than the sparse build.
    cheaper = _output_with_space_costs(
        default_comms_output,
        cost_low=50.0,
        cost_mid=100.0,
        cost_high=200.0,
        priced_mid=150.0,
    )
    comp_a = _build_comparison_for(cheaper, default_comms_config)
    flag_a = comp_a.by_density.sparse.cost_to_cost.space_is_cheaper
    assert isinstance(flag_a.value, bool)
    assert flag_a.unit == "bool"
    assert flag_a.value is True
    ratio_a = comp_a.by_density.sparse.cost_to_cost.ground_to_space_ratio_mid.value
    assert isinstance(ratio_a, float)
    assert (ratio_a > 1.0) is flag_a.value
    # Case B: space costlier than the dense floor.
    costlier = _output_with_space_costs(
        default_comms_output,
        cost_low=300.0,
        cost_mid=400.0,
        cost_high=500.0,
        priced_mid=600.0,
    )
    comp_b = _build_comparison_for(costlier, default_comms_config)
    flag_b = comp_b.by_density.dense.cost_to_cost.space_is_cheaper
    assert flag_b.value is False


def test_price_undercut_uses_regime_price_to_beat(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
) -> None:
    """Sparse price-to-beat is the retail reference; dense is the incumbent marginal floor."""
    # Space priced cost $95/sub/yr: below the $1200 sparse retail, above the $90 dense floor.
    controlled = _output_with_space_costs(
        default_comms_output,
        cost_low=40.0,
        cost_mid=60.0,
        cost_high=80.0,
        priced_mid=95.0,
    )
    comparison = _build_comparison_for(controlled, default_comms_config)
    sparse_uc = comparison.by_density.sparse.price_undercut
    dense_uc = comparison.by_density.dense.price_undercut
    retail_annual = (
        default_comms_config.price_reference.retail_reference_usd_per_month * MONTHS_PER_YEAR
    )
    assert sparse_uc.price_to_beat_basis == "retail_reference"
    assert abs(sparse_uc.price_to_beat_usd_per_year.value - retail_annual) < 1e-9
    assert dense_uc.price_to_beat_basis == "incumbent_marginal_defend_cost"
    ground_config = ground_config_from_comms_config(default_comms_config)
    ground = _build_ground_cost_by_density(ground_config, default_comms_config.price_reference)
    assert (
        dense_uc.price_to_beat_usd_per_year.value
        == ground.dense.cost_annual_per_subscriber_usd.value
    )
    # Below retail (pass) but above the dense floor (fail): the asymmetry.
    assert sparse_uc.undercut_passes.value is True
    assert dense_uc.undercut_passes.value is False


def test_space_capacity_binds_flag_by_regime(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
) -> None:
    """Capacity has headroom in sparse (False) and binds in dense (True)."""
    comparison = _build_comparison_for(default_comms_output, default_comms_config)
    sparse_flag = comparison.by_density.sparse.space_capacity_binds
    dense_flag = comparison.by_density.dense.space_capacity_binds
    assert sparse_flag.value is False
    assert dense_flag.value is True
    assert sparse_flag.unit == "bool"
    assert dense_flag.unit == "bool"
    assert sparse_flag.formula_name in FORMULAS
    assert dense_flag.formula_name in FORMULAS


def test_revenue_ceiling_collectable_win_needs_both_ceilings(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
) -> None:
    """A collectable win needs the priced revenue under BOTH ceilings (concern C8)."""
    # Case A: priced revenue below both the collectable ($300) and retail ($1200).
    win = _output_with_space_costs(
        default_comms_output,
        cost_low=100.0,
        cost_mid=150.0,
        cost_high=200.0,
        priced_mid=200.0,
        arpu_collectable=300.0,
    )
    rc_win = _build_comparison_for(win, default_comms_config).revenue_ceiling
    assert rc_win.collectable_win.value is True
    # Case B: below retail but ABOVE the collectable ceiling: not a collectable win.
    no_win = _output_with_space_costs(
        default_comms_output,
        cost_low=300.0,
        cost_mid=400.0,
        cost_high=500.0,
        priced_mid=500.0,
        arpu_collectable=300.0,
    )
    rc_no = _build_comparison_for(no_win, default_comms_config).revenue_ceiling
    assert rc_no.priced_below_retail.value is True
    assert rc_no.priced_below_collectable.value is False
    assert rc_no.collectable_win.value is False


def test_revenue_ceiling_reads_arpu_collectable_off_space_output(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
) -> None:
    """The reconciliation reads the ARPU-collectable cell off the space output (= 300.0 default)."""
    comparison = _build_comparison_for(default_comms_output, default_comms_config)
    key = str(default_comms_output.metadata.steady_state_year)
    expected = default_comms_output.business.years[key].arpu_collectable_revenue_usd.value
    assert comparison.revenue_ceiling.arpu_collectable_revenue_usd.value == expected
    assert expected == 300.0


def test_starlink_floor_shows_both_figures_and_never_claims_a_win(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
) -> None:
    """The Starlink-floor block shows both figures, flags chain<floor, and never claims a win."""
    comparison = _build_comparison_for(default_comms_output, default_comms_config)
    sf = comparison.starlink_floor
    assert isinstance(sf.bottom_up_chain_cost_usd_per_sub_year.value, float)
    assert isinstance(sf.disclosed_starlink_floor_usd_per_sub_year.value, float)
    assert isinstance(sf.chain_below_disclosed_floor.value, bool)
    assert sf.honesty_note  # non-empty
    assert "never claims" in sf.honesty_note
    assert "not asserted as a win" in sf.honesty_note


def test_comparison_has_no_verdict_field(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
) -> None:
    """No comparison model carries a verdict / conclusion / capture-share field name."""
    forbidden = {
        "conclusion_label",
        "verdict",
        "space_wins",
        "ground_wins",
        "recommended",
        "recommendation",
        "capture_share",
        "share_pct",
        "market_share",
    }
    models = [
        CommsComparison,
        ComparisonByDensity,
        DensityRegimeComparison,
        CostToCostComparison,
        PriceUndercutCheck,
        RevenueCeilingReconciliation,
        StarlinkFloorHonesty,
    ]
    for model in models:
        assert forbidden.isdisjoint(model.model_fields.keys()), model.__name__


def _walk_cells(value: object) -> list[ProvenanceCell]:
    """Recursively collect every ProvenanceCell reachable from a Pydantic model."""
    from pydantic import BaseModel

    cells: list[ProvenanceCell] = []
    if isinstance(value, ProvenanceCell):
        cells.append(value)
    elif isinstance(value, BaseModel):
        for name in type(value).model_fields:
            cells.extend(_walk_cells(getattr(value, name)))
    elif isinstance(value, list):
        for item in value:
            cells.extend(_walk_cells(item))
    return cells


def test_comparison_cells_carry_registered_formula_names(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
) -> None:
    """Every ProvenanceCell in the comparison carries a formula_name present in FORMULAS."""
    comparison = _build_comparison_for(default_comms_output, default_comms_config)
    cells = _walk_cells(comparison)
    assert cells  # the walk found cells
    for c in cells:
        assert c.formula_name in FORMULAS, c.formula_name


def test_full_ground_output_comparison_is_wired(
    default_comms_output: CommsModelOutput,
    default_ground_config: GroundReferenceConfig,
    default_comms_config: CommsConfig,
) -> None:
    """The top-level build_ground_reference_output assembles the same comparison block."""
    output = build_ground_reference_output(
        default_comms_output,
        default_ground_config,
        default_comms_config.price_reference,
        default_ground_source_catalog(),
    )
    assert isinstance(output.comparison, CommsComparison)
    assert isinstance(output.comparison.by_density.sparse, DensityRegimeComparison)
    assert isinstance(output.comparison.by_density.dense, DensityRegimeComparison)
