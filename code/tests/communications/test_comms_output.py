"""Tests for the comms five-key output models (the schema-level disaster gates).

These pin that the output round-trips JSON with every required leaf present
(including the band leaves, the scalar ARPU cell, and the capability cells),
that the customer-band leaf is three sibling cells, that the BusinessYear model
carries NO verdict / ratio / capture-share fields, that the metadata carries NO
DC-venture enums, and that the meta block is lean.
"""

from __future__ import annotations

import json

from communications.config import CommsConfig
from communications.engine import render_comms_json, run_comms_model
from communications.output import BusinessYear, CustomerBandBlock, MetaBlock, RunMetadata


def test_comms_model_output_round_trips_json() -> None:
    """The output serialises and every required leaf (incl. the three additions) round-trips."""
    out = run_comms_model(CommsConfig())
    parsed = json.loads(render_comms_json(out))
    assert sorted(parsed.keys()) == ["business", "inputs", "meta", "metadata", "physical"]

    business_2036 = parsed["business"]["years"]["2036"]
    for member in ("low", "mid", "high"):
        assert isinstance(business_2036["total_served"][member]["value"], (int, float))
        assert isinstance(
            business_2036["cost_annual_per_customer_usd"][member]["value"], (int, float)
        )
        assert isinstance(
            business_2036["priced_cost_per_customer_usd"][member]["value"], (int, float)
        )
    # the scalar ARPU-collectable cell (this-round defect-1)
    assert isinstance(business_2036["arpu_collectable_revenue_usd"]["value"], (int, float))
    assert "low" not in business_2036["arpu_collectable_revenue_usd"]

    physical_2036 = parsed["physical"]["years"]["2036"]
    for class_name in ("direct_to_cell", "broadband"):
        cap = physical_2036[class_name]["capability"]
        assert isinstance(cap["value"], (int, float))
        assert cap["unit"] == "Mbps"


def test_customer_band_block_is_three_cells() -> None:
    """A CustomerBandBlock has three distinct ProvenanceCell fields (the band-leaf shape)."""
    field_names = set(CustomerBandBlock.model_fields.keys())
    assert field_names == {"low", "mid", "high"}


def test_business_year_has_no_verdict_or_ratio_fields() -> None:
    """BusinessYear carries no baked-in-conclusion / capture-share field (schema-level gate)."""
    field_names = set(BusinessYear.model_fields.keys())
    forbidden = {
        "conclusion_label",
        "verdict",
        "cost_ratio",
        "space_wins",
        "ground_wins",
        "recommended",
        "recommendation",
        "capture_share",
        "share_pct",
        "market_share",
    }
    assert field_names.isdisjoint(forbidden)


def test_metadata_has_no_dc_enums() -> None:
    """The comms RunMetadata has none of the GPU-venture lock fields."""
    field_names = set(RunMetadata.model_fields.keys())
    forbidden = {
        "workload_type",
        "operator_model",
        "radiator_architecture",
        "deployment_philosophy",
    }
    assert field_names.isdisjoint(forbidden)


def test_meta_block_is_lean() -> None:
    """The comms MetaBlock has the three lean fields and none of the Phase-5 enrichment fields."""
    field_names = set(MetaBlock.model_fields.keys())
    assert field_names == {"validation", "source_status_summary", "schema_version_notes"}
    forbidden = {
        "data_dictionary",
        "query_examples",
        "formula_definitions",
        "validation_results",
        "generations_dictionary",
    }
    assert field_names.isdisjoint(forbidden)
