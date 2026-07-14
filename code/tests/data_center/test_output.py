"""Tests for the v8 typed Pydantic output models in :mod:`data_center.output`.

Three test families:

1. **Schema shape** — the v8 ``ValuationOutput`` has exactly the five
   top-level keys ``{metadata, inputs, physical, business, meta}`` (D21);
   ``physical.years`` / ``business.years`` carry ProvenanceCell-wrapped
   per-year data; the ``meta`` block carries the four sub-blocks.
2. **Construction + round-trip** — a hand-built minimal v8
   ``ValuationOutput`` serialises via ``model_dump_json`` and re-validates.
3. **Engine integration** — running the default scenario through the
   engine produces a structurally-valid v8 artifact and a populated
   data dictionary.
"""

from __future__ import annotations

import json

import pytest
from pydantic import BaseModel, ValidationError

from data_center.config import (
    ValuationConfig,
)
from data_center.generations import KNOWN_GENS
from data_center.input_manifest import build_input_manifest
from data_center.output import (
    SCHEMA_VERSION,
    BusinessBlock,
    BusinessYear,
    CostBreakdownBlock,
    DataDictEntry,
    FieldKind,
    MetaBlock,
    PhysicalBlock,
    PhysicalYear,
    RunMetadata,
    Severity,
    SourceStatusSummary,
    ValidationCheck,
    ValidationReport,
    ValuationOutput,
)
from data_center.provenance import ProvenanceCell

# Top-level keys of the v8 artifact (D21).
V8_TOP_LEVEL_KEYS = {"metadata", "inputs", "physical", "business", "meta"}

# Every per-year cell field on PhysicalYear / BusinessYear.
PHYSICAL_YEAR_FIELDS = set(PhysicalYear.model_fields.keys())
BUSINESS_YEAR_FIELDS = set(BusinessYear.model_fields.keys())


# ---------------------------------------------------------------------------
# Helpers — a hand-built minimal v8 ValuationOutput
# ---------------------------------------------------------------------------


def _num_cell(value: float, unit: str = "kW") -> ProvenanceCell:
    """A minimal numeric ProvenanceCell for fixture construction."""
    return ProvenanceCell(
        value=value,
        unit=unit,
        formula="x = y",
        formula_name="kw_per_node_from_n_and_kw_per_pkg",
        uses=["inputs.test"],
        sources=["unit test"],
        description="A test cell.",
    )


def _str_cell(value: str) -> ProvenanceCell:
    """A minimal string ProvenanceCell for fixture construction."""
    return ProvenanceCell(
        value=value,
        unit="-",
        formula="pick",
        formula_name="frontier_generation_from_cadence",
        uses=["inputs.generations[].year_available"],
        sources=["unit test"],
        description="A test enum cell.",
    )


def _make_cost_breakdown() -> CostBreakdownBlock:
    """A minimal :class:`CostBreakdownBlock` — every line a ProvenanceCell."""
    return CostBreakdownBlock(
        compute=_num_cell(40.0, "MUSD"),
        bus=_num_cell(8.0, "MUSD"),
        solar=_num_cell(9.0, "MUSD"),
        radiator=_num_cell(9.0, "MUSD"),
        launch=_num_cell(14.0, "MUSD"),
        node_total=_num_cell(80.0, "MUSD"),
    )


def _make_physical_year() -> PhysicalYear:
    """A minimal :class:`PhysicalYear` — every leaf a ProvenanceCell."""
    return PhysicalYear(
        year=2026,
        frontier_generation=_str_cell("B300/GB300"),
        gpus_per_node=_num_cell(120.0, "count"),
        kw_per_node=_num_cell(300.0, "kW"),
        mass_per_node_t=_num_cell(12.4, "t"),
        solar_area_per_pkg_m2=_num_cell(7.5, "m2"),
        volume_per_pkg_m3=_num_cell(0.04, "m3"),
        volume_per_node_m3=_num_cell(5.1, "m3"),
        mass_utilization_pct=_num_cell(99.2, "percent"),
        volume_utilization_pct=_num_cell(6.4, "percent"),
        binding_constraint=_str_cell("mass"),
        pf_per_node=_num_cell(1800.0, "PFLOPS"),
        pf_per_kw=_num_cell(6.0, "PFLOPS/kW"),
        cost_breakdown=_make_cost_breakdown(),
        cost_annual_per_node_musd=_num_cell(13.0, "MUSD"),
        revenue_annual_per_node_musd_central=_num_cell(19.5, "MUSD"),
        revenue_annual_per_node_musd_low=_num_cell(15.6, "MUSD"),
        revenue_annual_per_node_musd_high=_num_cell(23.4, "MUSD"),
        gross_profit_annual_per_node_musd_central=_num_cell(6.5, "MUSD"),
        gross_profit_annual_per_node_musd_low=_num_cell(2.6, "MUSD"),
        gross_profit_annual_per_node_musd_high=_num_cell(10.4, "MUSD"),
    )


def _make_business_year() -> BusinessYear:
    """A minimal :class:`BusinessYear` — every field a ProvenanceCell."""
    return BusinessYear(
        year=2026,
        launches=_num_cell(14.0, "count"),
        nodes_deployed_this_year=_num_cell(14.0, "count"),
        living_fleet=_num_cell(40.0, "count"),
        kw_deployed_this_year=_num_cell(4200.0, "kW"),
        kw_living_fleet=_num_cell(12000.0, "kW"),
        kw_on_orbit=_num_cell(12000.0, "kW"),
        pf_deployed_this_year=_num_cell(25200.0, "PFLOPS"),
        pf_living_fleet=_num_cell(72000.0, "PFLOPS"),
        pf_on_orbit=_num_cell(72000.0, "PFLOPS"),
        launch_cost_this_year_musd=_num_cell(18.0, "MUSD"),
        cost_annual_fleet_musd=_num_cell(520.0, "MUSD"),
        revenue_annual_fleet_musd_central=_num_cell(780.0, "MUSD"),
        revenue_annual_fleet_musd_low=_num_cell(624.0, "MUSD"),
        revenue_annual_fleet_musd_high=_num_cell(936.0, "MUSD"),
        revenue_cumulative_musd_central=_num_cell(2000.0, "MUSD"),
        revenue_cumulative_musd_low=_num_cell(1600.0, "MUSD"),
        revenue_cumulative_musd_high=_num_cell(2400.0, "MUSD"),
        gross_profit_annual_fleet_musd_central=_num_cell(260.0, "MUSD"),
        gross_profit_annual_fleet_musd_low=_num_cell(104.0, "MUSD"),
        gross_profit_annual_fleet_musd_high=_num_cell(416.0, "MUSD"),
        margin_central_pct=_num_cell(33.3, "percent"),
        margin_low_pct=_num_cell(16.7, "percent"),
        margin_high_pct=_num_cell(44.4, "percent"),
    )


def _make_minimal_output() -> ValuationOutput:
    """A minimum-valid v8 ValuationOutput — one physical + one business year."""
    metadata = RunMetadata(
        schema_version=SCHEMA_VERSION,
        scenario_name="Test scenario",
        base_year=2026,
        horizon_years=10,
        workload_type="inference",  # type: ignore[arg-type]
        operator_model="b2b_dedicated_optical_rf",  # type: ignore[arg-type]
        radiator_architecture="single_face_co_mounted",  # type: ignore[arg-type]
        deployment_philosophy="ground_validated_before_launch",
        generated_at="2026-05-20T12:00:00+00:00",
        model_package="rklb-value",
        model_version=None,
        artifact_role="draft",
        source_scenario_path="unit-test",
    )
    inputs = build_input_manifest(
        config=ValuationConfig(),
        extended_gens=list(KNOWN_GENS),
        source_scenario_path="unit-test",
    )
    physical = PhysicalBlock(years={"2026": _make_physical_year()})
    business = BusinessBlock(years={"2026": _make_business_year()})
    meta = MetaBlock(
        validation=ValidationReport(
            rules=[
                ValidationCheck(
                    name="r_above_one",
                    what_it_tests="Revenue/cost ratio is above the floor.",
                    expected="> 1.0",
                    computed="1.50",
                    pass_check=True,
                    severity=Severity.CRITICAL,
                )
            ]
        ),
        data_dictionary=[
            DataDictEntry(
                path="physical.years[].kw_per_node",
                description="Total node electrical power, kW.",
                unit="kW",
                type="cell",
                source_class="DERIVED",
            )
        ],
        formula_definitions=[],
        validation_results=[],
        generations_dictionary=[],
        query_examples=[],
        source_status_summary=SourceStatusSummary(
            certified=0,
            sourced_estimate=0,
            derived_estimate=0,
            projection=0,
            extrapolation=0,
            scenario=0,
            placeholder=0,
            stale=0,
        ),
        schema_version_notes="unit test",
    )
    return ValuationOutput(
        metadata=metadata,
        inputs=inputs,
        physical=physical,
        business=business,
        meta=meta,
    )


# ---------------------------------------------------------------------------
# Schema shape — the v8 five-block structure
# ---------------------------------------------------------------------------


def test_v8_top_level_has_exactly_five_keys() -> None:
    """ValuationOutput has exactly {metadata, inputs, physical, business, meta}."""
    assert set(ValuationOutput.model_fields.keys()) == V8_TOP_LEVEL_KEYS


def test_v8_top_level_keys_match_in_serialised_json() -> None:
    """The serialised artifact's top-level keys are the v8 five (D21)."""
    out = _make_minimal_output()
    parsed = json.loads(out.model_dump_json())
    assert set(parsed.keys()) == V8_TOP_LEVEL_KEYS


def test_v8_drops_cycle1_summary_and_decisions_blocks() -> None:
    """The cycle-1 `summary` / `decisions` / `manifest` / `about` blocks are gone."""
    fields = set(ValuationOutput.model_fields.keys())
    for cycle1_only in ("summary", "decisions", "manifest", "about", "years"):
        assert cycle1_only not in fields


def test_physical_year_has_twenty_leaf_fields() -> None:
    """PhysicalYear carries 19 per-node ProvenanceCells + the cost_breakdown block.

    The cycle-2 provenance-wiring fix added three leaves to the original
    17: ``solar_area_per_pkg_m2`` and ``volume_per_pkg_m3`` (the volume
    intermediates a cell's ``uses`` cite), plus ``cost_breakdown`` — a
    :class:`CostBreakdownBlock` of the six cost-decomposition cells.
    """
    assert len(PHYSICAL_YEAR_FIELDS) == 21
    for name, info in PhysicalYear.model_fields.items():
        if name == "year":
            assert info.annotation is int
            continue
        if name == "cost_breakdown":
            assert info.annotation is CostBreakdownBlock
            continue
        assert info.annotation is ProvenanceCell, f"{name} is not a ProvenanceCell"


def test_cost_breakdown_block_has_six_cell_fields() -> None:
    """CostBreakdownBlock carries the five cost lines + the node total, all cells."""
    fields = CostBreakdownBlock.model_fields
    assert set(fields.keys()) == {"compute", "bus", "solar", "radiator", "launch", "node_total"}
    for name, info in fields.items():
        assert info.annotation is ProvenanceCell, f"{name} is not a ProvenanceCell"


def test_business_year_has_nineteen_cell_fields() -> None:
    """BusinessYear carries the 19 per-fleet ProvenanceCell fields."""
    assert len(BUSINESS_YEAR_FIELDS) == 24
    for name, info in BusinessYear.model_fields.items():
        if name == "year":
            assert info.annotation is int
            continue
        assert info.annotation is ProvenanceCell, f"{name} is not a ProvenanceCell"


def test_revenue_fields_are_band_split_central_low_high() -> None:
    """Revenue / profit fields are explicit central/low/high — no `annual_rev_per_node_musd`."""
    # The cycle-1 misleading field name (D25) does not exist on either block.
    assert "annual_rev_per_node_musd" not in PHYSICAL_YEAR_FIELDS
    for band in ("central", "low", "high"):
        assert f"revenue_annual_per_node_musd_{band}" in PHYSICAL_YEAR_FIELDS
        assert f"gross_profit_annual_per_node_musd_{band}" in PHYSICAL_YEAR_FIELDS
        assert f"revenue_annual_fleet_musd_{band}" in BUSINESS_YEAR_FIELDS
        assert f"margin_{band}_pct" in BUSINESS_YEAR_FIELDS


def test_meta_block_has_four_sub_blocks() -> None:
    """MetaBlock carries validation, dictionary, formulas, queries, and summaries."""
    assert set(MetaBlock.model_fields.keys()) == {
        "validation",
        "data_dictionary",
        "formula_definitions",
        "validation_results",
        "generations_dictionary",
        "query_examples",
        "source_status_summary",
        "schema_version_notes",
    }


def test_run_metadata_carries_schema_version_and_generated_at() -> None:
    """RunMetadata adds schema_version + generated_at to the config enum locks."""
    fields = set(RunMetadata.model_fields.keys())
    assert "schema_version" in fields
    assert "generated_at" in fields
    for enum_lock in ("workload_type", "operator_model", "radiator_architecture"):
        assert enum_lock in fields


# ---------------------------------------------------------------------------
# Construction + round-trip
# ---------------------------------------------------------------------------


def test_minimal_valuation_output_constructs() -> None:
    """A minimum-valid v8 ValuationOutput can be built."""
    out = _make_minimal_output()
    assert out.metadata.schema_version == "v8"
    assert "2026" in out.physical.years
    assert "2026" in out.business.years
    assert len(out.meta.validation.rules) == 1


def test_round_trip_serialises_and_validates() -> None:
    """A v8 ValuationOutput round-trips: dump -> load -> validate yields equal."""
    original = _make_minimal_output()
    text = original.model_dump_json(indent=2)
    rebuilt = ValuationOutput.model_validate(json.loads(text))
    assert rebuilt == original


def test_frozen_instances_reject_mutation() -> None:
    """Every v8 model is frozen — mutation raises ValidationError."""
    out = _make_minimal_output()
    with pytest.raises(ValidationError):
        out.metadata.schema_version = "evil"  # type: ignore[misc]


def test_provenance_cell_is_the_per_year_leaf() -> None:
    """Per-year fields are ProvenanceCell instances carrying value + provenance."""
    out = _make_minimal_output()
    cell = out.physical.years["2026"].kw_per_node
    assert isinstance(cell, ProvenanceCell)
    assert cell.value == 300.0
    assert cell.unit == "kW"
    assert cell.formula_name
    assert isinstance(cell.uses, list)
    assert isinstance(cell.sources, list)


def test_schema_introspection_produces_a_json_schema() -> None:
    """ValuationOutput.model_json_schema() works and surfaces the v8 keys."""
    schema = ValuationOutput.model_json_schema()
    assert schema["type"] == "object"
    for key in V8_TOP_LEVEL_KEYS:
        assert key in schema["properties"], f"top-level key missing: {key}"


def test_enums_are_string_typed() -> None:
    """FieldKind and Severity are StrEnums — their values are strings."""
    assert FieldKind.INPUT == "input"
    assert Severity.CRITICAL == "critical"
    assert Severity.MINOR == "minor"


# ---------------------------------------------------------------------------
# Engine integration
# ---------------------------------------------------------------------------


def _run_default() -> ValuationOutput:
    """Run the default scenario through the v8 engine."""
    from data_center.config import load_config
    from data_center.engine import run_valuation

    return run_valuation(load_config("scenarios/default.yaml"))


def test_engine_produces_v8_top_level_structure() -> None:
    """The engine's run_valuation emits the v8 five-block artifact."""
    out = _run_default()
    parsed = json.loads(out.model_dump_json())
    assert set(parsed.keys()) == V8_TOP_LEVEL_KEYS


def test_engine_emits_eleven_physical_and_business_years() -> None:
    """The default scenario (horizon 10) emits 11 physical + 11 business years."""
    out = _run_default()
    assert len(out.physical.years) == 11
    assert len(out.business.years) == 11
    assert "2026" in out.physical.years
    assert "2036" in out.physical.years
    assert "2026" in out.business.years
    assert "2036" in out.business.years


def test_engine_metadata_schema_version_is_v8() -> None:
    """The engine stamps the artifact schema_version as 'v8'."""
    out = _run_default()
    assert out.metadata.schema_version == "v8"
    assert out.metadata.base_year == 2026
    assert out.metadata.horizon_years == 10


def test_engine_per_year_cells_carry_values_and_provenance() -> None:
    """Every physical-year leaf is a ProvenanceCell with a value + formula_name."""
    out = _run_default()
    py = out.physical.years["2030"]
    for name in PHYSICAL_YEAR_FIELDS:
        field = getattr(py, name)
        if name == "year":
            assert isinstance(field, int)
            continue
        cells = list(vars(field).values()) if isinstance(field, CostBreakdownBlock) else [field]
        for cell in cells:
            assert isinstance(cell, ProvenanceCell), f"{name} is not a ProvenanceCell"
            assert cell.value is not None, f"{name} has a None value"
            assert cell.formula_name, f"{name} has no formula_name"


def test_engine_business_year_cells_carry_values() -> None:
    """Every business-year leaf is a ProvenanceCell with a value."""
    out = _run_default()
    by = out.business.years["2032"]
    for name in BUSINESS_YEAR_FIELDS:
        cell = getattr(by, name)
        if name == "year":
            assert isinstance(cell, int)
            continue
        assert isinstance(cell, ProvenanceCell), f"{name} is not a ProvenanceCell"
        assert cell.value is not None, f"{name} has a None value"


def test_engine_emits_populated_data_dictionary() -> None:
    """run_valuation populates meta.data_dictionary with described entries."""
    out = _run_default()
    dd = out.meta.data_dictionary
    assert len(dd) > 30
    for entry in dd:
        assert entry.path
        assert entry.description.strip(), f"empty description for {entry.path}"
        assert entry.type, f"empty type for {entry.path}"
        assert entry.source_class, f"empty source_class for {entry.path}"


def test_data_dictionary_describes_per_year_cells_as_leaves() -> None:
    """The data dictionary treats a ProvenanceCell as a leaf (one entry per field)."""
    out = _run_default()
    dd = {entry.path: entry for entry in out.meta.data_dictionary}
    # The cell field gets one entry typed `cell`; its machinery is not walked.
    assert dd["physical.years[].kw_per_node"].type == "cell"
    assert "physical.years[].kw_per_node.formula_name" not in dd
    assert dd["business.years[].living_fleet"].type == "cell"


def test_engine_inputs_block_carries_v8_dial_blocks() -> None:
    """inputs carries gospel + slopes + the five v8 dial blocks + generations."""
    out = _run_default()
    inp = out.inputs
    assert "inputs.config.physical.mass_envelope_t" in inp.assumption_index
    assert "pf_growth_per_gen" in inp.slopes
    assert inp.cadence.cadence_ceiling > 0
    assert inp.fleet.service_life_years > 0
    assert inp.volume.fold_ratio > 0
    assert len(inp.r_band.central) >= 2
    assert inp.launch_cost.low_cadence_cost_musd > 0
    assert len(inp.generations) >= 5


def test_engine_generations_dictionary_summarises_each_generation() -> None:
    """meta.generations_dictionary has one compact summary per generation."""
    out = _run_default()
    gd = out.meta.generations_dictionary
    assert len(gd) == len(out.inputs.generations)
    first = gd[0]
    assert first.name
    assert first.die_count >= 1
    assert first.kw_per_pkg > 0
    assert first.source_doc_path.startswith("research/")


def test_engine_validation_report_has_seventeen_rules() -> None:
    """meta.validation.rules carries the 17 wired V1..V17 checks."""
    out = _run_default()
    rules = out.meta.validation.rules
    assert len(rules) == 17
    assert all(isinstance(r, ValidationCheck) for r in rules)


def test_engine_output_roundtrips_via_model_validate() -> None:
    """The engine's v8 output round-trips through JSON."""
    out = _run_default()
    rebuilt = ValuationOutput.model_validate(json.loads(out.model_dump_json()))
    assert rebuilt.metadata.schema_version == "v8"
    assert len(rebuilt.physical.years) == 11
    assert rebuilt.physical.years["2026"].gpus_per_node.value == 223


# ---------------------------------------------------------------------------
# Schema introspection — every leaf field has a description
# ---------------------------------------------------------------------------


def _walk_fields(model_cls: type[BaseModel]) -> list[tuple[str, str | None]]:
    """Return (path, description) pairs for every leaf field in a model tree.

    A ProvenanceCell is treated as a leaf — it is the model's output field.
    """
    out: list[tuple[str, str | None]] = []

    def walk(cls: type[BaseModel], prefix: str) -> None:
        for name, info in cls.model_fields.items():
            path = f"{prefix}.{name}" if prefix else name
            ann = info.annotation
            if isinstance(ann, type) and issubclass(ann, ProvenanceCell):
                out.append((path, info.description))
                continue
            if isinstance(ann, type) and issubclass(ann, BaseModel):
                walk(ann, path)
                continue
            out.append((path, info.description))

    walk(model_cls, "")
    return out


def test_every_leaf_field_has_a_description() -> None:
    """Every leaf Field on ValuationOutput carries a non-empty description."""
    leaves = _walk_fields(ValuationOutput)
    assert len(leaves) > 30
    missing = [path for path, desc in leaves if not desc or not desc.strip()]
    assert not missing, f"fields missing description: {missing}"
