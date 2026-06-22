"""Tests for the comms ground reference module (the bottom-up ground cost, per density).

Exercises the ground config view, the per-density cost build (sparse fresh-build vs
dense incumbent-marginal), the space-reference by-value read, the input manifest,
the no-conclusion-label discipline, and the lean promote.
"""

from __future__ import annotations

import json

from common.input_manifest import InputCell
from common.provenance import FORMULAS, ProvenanceCell
from communications.config import CommsConfig
from communications.constants import MONTHS_PER_YEAR, REVENUE_MULTIPLE, DensityRegime
from communications.ground import (
    GroundComparisonAnchor,
    GroundCostByDensity,
    GroundCostResult,
    GroundReferenceConfig,
    GroundReferenceOutput,
    SourceCatalog,
    SpaceReferenceResult,
    _build_ground_cost_by_density,
    build_ground_reference_output,
    ground_config_from_comms_config,
    promote_default_ground_reference,
    render_ground_json,
)
from communications.output import CommsModelOutput


def _full_output(
    output: CommsModelOutput,
    config: CommsConfig,
    catalog: SourceCatalog,
) -> GroundReferenceOutput:
    """Build the full ground reference output from a space output and config."""
    ground_config = ground_config_from_comms_config(config)
    return build_ground_reference_output(output, ground_config, config.price_reference, catalog)


def test_ground_config_from_comms_config_reads_ground_block(
    default_comms_config: CommsConfig,
) -> None:
    """The ground config view equals the CommsConfig ground block (all eight dials)."""
    gc = ground_config_from_comms_config(default_comms_config)
    g = default_comms_config.ground
    assert gc.tower_cost_musd_per_site == g.tower_cost_musd_per_site
    assert gc.sites_per_million_subs == g.sites_per_million_subs
    assert gc.backhaul_cost_musd_per_site_year == g.backhaul_cost_musd_per_site_year
    assert gc.ground_opex_musd_per_site_year == g.ground_opex_musd_per_site_year
    assert gc.ground_amortization_years == g.ground_amortization_years
    assert gc.spectrum_cost_musd == g.spectrum_cost_musd
    assert gc.incumbent_marginal_fraction_of_arpu == g.incumbent_marginal_fraction_of_arpu
    assert (
        gc.starlink_disclosed_all_in_cost_usd_per_sub_year
        == g.starlink_disclosed_all_in_cost_usd_per_sub_year
    )


def test_ground_sparse_cost_result_sums_included_lines(
    default_ground_config: GroundReferenceConfig,
    default_comms_config: CommsConfig,
) -> None:
    """The sparse cost equals the sum of its included fresh-build lines and prices at 1.5x."""
    ground = _build_ground_cost_by_density(
        default_ground_config, default_comms_config.price_reference
    )
    assert ground.sparse.regime is DensityRegime.SPARSE
    included_sum = sum(c.cost.value for c in ground.sparse.component_costs if c.included)
    assert abs(ground.sparse.cost_annual_per_subscriber_usd.value - included_sum) < 1e-6
    assert (
        abs(
            ground.sparse.priced_cost_annual_per_subscriber_usd.value
            - ground.sparse.cost_annual_per_subscriber_usd.value * REVENUE_MULTIPLE
        )
        < 1e-6
    )


def test_ground_dense_cost_is_incumbent_marginal_floor(
    default_ground_config: GroundReferenceConfig,
    default_comms_config: CommsConfig,
) -> None:
    """The dense cost is the single incumbent-marginal line and lands in the COMM-101 band."""
    ground = _build_ground_cost_by_density(
        default_ground_config, default_comms_config.price_reference
    )
    assert ground.dense.regime is DensityRegime.DENSE
    included = [c for c in ground.dense.component_costs if c.included]
    assert len(included) == 1
    expected = (
        default_ground_config.incumbent_marginal_fraction_of_arpu
        * default_comms_config.price_reference.arpu_usd_per_month
        * MONTHS_PER_YEAR
    )
    assert abs(ground.dense.cost_annual_per_subscriber_usd.value - expected) < 1e-9
    # COMM-101 band: $84 to $180/sub/yr.
    assert 84.0 <= ground.dense.cost_annual_per_subscriber_usd.value <= 180.0


def test_ground_sparse_is_costlier_than_dense(
    default_ground_config: GroundReferenceConfig,
    default_comms_config: CommsConfig,
) -> None:
    """The sparse fresh build is far above the dense incumbent floor (the structural asymmetry)."""
    ground = _build_ground_cost_by_density(
        default_ground_config, default_comms_config.price_reference
    )
    assert (
        ground.sparse.cost_annual_per_subscriber_usd.value
        > ground.dense.cost_annual_per_subscriber_usd.value
    )
    # The sparse cost lands in the COMM-100 $875 to $1,540/sub/yr band.
    assert 875.0 <= ground.sparse.cost_annual_per_subscriber_usd.value <= 1540.0


def test_ground_crossover_note_is_populated(
    default_ground_config: GroundReferenceConfig,
    default_comms_config: CommsConfig,
) -> None:
    """The crossover note is a populated USD cell with a registered formula and COMM-103 order."""
    ground = _build_ground_cost_by_density(
        default_ground_config, default_comms_config.price_reference
    )
    note = ground.crossover_note_usd_per_sub_year
    assert isinstance(note, ProvenanceCell)
    assert note.unit == "USD"
    assert note.formula_name in FORMULAS
    assert 400.0 <= note.value <= 600.0  # about $490/sub/yr


def test_ground_spectrum_wash_is_explicit_zero(
    default_ground_config: GroundReferenceConfig,
    default_comms_config: CommsConfig,
) -> None:
    """The sparse spectrum line is an included explicit zero; the dense regime has none."""
    ground = _build_ground_cost_by_density(
        default_ground_config, default_comms_config.price_reference
    )
    spectrum = [c for c in ground.sparse.component_costs if c.name == "spectrum_wash"]
    assert len(spectrum) == 1
    assert spectrum[0].included is True
    assert spectrum[0].cost.value == 0.0
    assert spectrum[0].cost.unit == "USD"
    assert "nets out" in spectrum[0].cost.description
    # The dense regime carries no spectrum line at all.
    assert not any(c.name == "spectrum_wash" for c in ground.dense.component_costs)


def test_ground_cost_lines_carry_full_provenance(
    default_ground_config: GroundReferenceConfig,
    default_comms_config: CommsConfig,
) -> None:
    """Every ground cost line in both regimes carries full provenance."""
    ground = _build_ground_cost_by_density(
        default_ground_config, default_comms_config.price_reference
    )
    for result in (ground.sparse, ground.dense):
        for component in result.component_costs:
            c = component.cost
            assert c.formula_name in FORMULAS
            assert c.uses
            assert c.sources
            assert c.unit == "USD"


def test_ground_input_manifest_round_trips_and_indexes(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
    ground_source_catalog: SourceCatalog,
) -> None:
    """The manifest carries one full-field InputCell per ground dial and a matching flat index."""
    output = _full_output(default_comms_output, default_comms_config, ground_source_catalog)
    tree = output.inputs.config
    cells = [
        tree.tower_cost_musd_per_site,
        tree.sites_per_million_subs,
        tree.backhaul_cost_musd_per_site_year,
        tree.ground_opex_musd_per_site_year,
        tree.ground_amortization_years,
        tree.spectrum_cost_musd,
        tree.incumbent_marginal_fraction_of_arpu,
        tree.starlink_disclosed_all_in_cost_usd_per_sub_year,
    ]
    assert len(cells) == 8
    for cell_value in cells:
        assert isinstance(cell_value, InputCell)
        assert cell_value.path
        assert cell_value.label
        assert cell_value.description
        assert cell_value.assumption_role
        assert cell_value.source_status
        assert cell_value.source_refs
        assert cell_value.rationale
    index = output.inputs.assumption_index
    assert len(index) == len(cells)
    for key, cell_value in index.items():
        assert key == cell_value.path


def test_space_reference_reads_steady_state_cells(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
    ground_source_catalog: SourceCatalog,
) -> None:
    """The space reference reads the steady-state per-customer cost band by value."""
    output = _full_output(default_comms_output, default_comms_config, ground_source_catalog)
    sr = output.space_reference
    key = str(default_comms_output.metadata.steady_state_year)
    by = default_comms_output.business.years[key]
    assert sr.cost_annual_per_subscriber_usd.value == by.cost_annual_per_customer_usd.mid.value
    assert sr.cost_annual_per_subscriber_band.low.value == by.cost_annual_per_customer_usd.low.value
    assert sr.cost_annual_per_subscriber_band.mid.value == by.cost_annual_per_customer_usd.mid.value
    assert (
        sr.cost_annual_per_subscriber_band.high.value == by.cost_annual_per_customer_usd.high.value
    )


def test_anchor_is_steady_state_living_fleet(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
    ground_source_catalog: SourceCatalog,
) -> None:
    """The anchor records the steady-state year, the living-fleet basis, and total_served.mid."""
    output = _full_output(default_comms_output, default_comms_config, ground_source_catalog)
    anchor = output.anchor
    assert isinstance(anchor, GroundComparisonAnchor)
    assert anchor.year == default_comms_output.metadata.steady_state_year
    assert anchor.basis == "living_fleet_steady_state"
    key = str(default_comms_output.metadata.steady_state_year)
    served_mid = default_comms_output.business.years[key].total_served.mid.value
    assert anchor.total_served_mid == served_mid


def test_ground_output_has_no_conclusion_label(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
    ground_source_catalog: SourceCatalog,
) -> None:
    """No ground / comparison model carries a verdict / conclusion / capture-share field name."""
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
        GroundReferenceOutput,
        GroundCostByDensity,
        GroundCostResult,
        SpaceReferenceResult,
        GroundComparisonAnchor,
    ]
    for model in models:
        assert forbidden.isdisjoint(model.model_fields.keys()), model.__name__
    # "sparse" / "dense" regime keys are descriptive, not forbidden tokens.
    assert "regime" in GroundCostResult.model_fields


def test_ground_promote_writes_json() -> None:
    """The promote writes the seven-key ground JSON carrying both density regimes."""
    path = promote_default_ground_reference()
    assert path.name == "default.json"
    assert path.parent.name == "ground"
    assert path.is_file()
    data = json.loads(path.read_text())
    assert sorted(data.keys()) == [
        "anchor",
        "comparison",
        "ground",
        "inputs",
        "meta",
        "metadata",
        "space_reference",
    ]
    assert "sparse" in data["ground"]
    assert "dense" in data["ground"]
    assert "sparse" in data["comparison"]["by_density"]
    assert "dense" in data["comparison"]["by_density"]


def test_ground_promote_is_deterministic() -> None:
    """Re-running the promote regenerates the same content except metadata.generated_at."""
    path_a = promote_default_ground_reference()
    text_a = path_a.read_text()
    path_b = promote_default_ground_reference()
    text_b = path_b.read_text()
    data_a = json.loads(text_a)
    data_b = json.loads(text_b)
    data_a["metadata"]["generated_at"] = "PINNED"
    data_b["metadata"]["generated_at"] = "PINNED"
    assert data_a == data_b


def test_render_ground_json_is_valid_json(
    default_comms_output: CommsModelOutput,
    default_comms_config: CommsConfig,
    ground_source_catalog: SourceCatalog,
) -> None:
    """render_ground_json emits parseable indented JSON."""
    output = _full_output(default_comms_output, default_comms_config, ground_source_catalog)
    text = render_ground_json(output)
    parsed = json.loads(text)
    assert parsed["metadata"]["schema_version"] == "comms-ground-v1"
