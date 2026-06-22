"""Tests for the comms meta enrichment (the data dictionary, formula catalog, results).

Pins that the introspection walk covers every leaf, that the formula catalog is
the comms-scoped registry slice, that ``enrich_comms_output`` fills the four
enrichment fields while preserving the engine's summary and schema notes, that the
enrichment is pure (no cell value changes), and that the engine output is lean
while the enriched output is full (the revised Phase-3 lean-meta contract).
"""

from __future__ import annotations

import json

from common.meta import QueryAppliesTo
from common.provenance import FORMULAS, ProvenanceCell
from communications.engine import render_comms_json
from communications.json_output import (
    QUERY_EXAMPLES,
    _build_formula_definitions,
    build_comms_data_dictionary,
    enrich_comms_output,
)
from communications.output import CommsModelOutput

REL_TOL = 1e-9


def _all_cells(output: CommsModelOutput) -> dict[str, float | int | str | bool | None]:
    """Return every physical/business ProvenanceCell value keyed by a stable path."""
    out: dict[str, float | int | str | bool | None] = {}

    def _walk(record: object, prefix: str) -> None:
        for field_name in type(record).model_fields:  # type: ignore[attr-defined]
            value = getattr(record, field_name)
            path = f"{prefix}.{field_name}"
            if isinstance(value, ProvenanceCell):
                out[path] = value.value
            elif hasattr(type(value), "model_fields"):
                _walk(value, path)

    for fy, py in output.physical.years.items():
        _walk(py, f"physical.{fy}")
    for fy, by in output.business.years.items():
        _walk(by, f"business.{fy}")
    return out


def test_data_dictionary_covers_every_leaf() -> None:
    """The data dictionary is non-empty and every entry is well-formed."""
    entries = build_comms_data_dictionary(CommsModelOutput)
    assert len(entries) >= 30
    valid_classes = {"INPUT", "CONSTANT", "DERIVED"}
    by_path = {e.path: e for e in entries}
    for e in entries:
        assert e.path
        assert e.unit is not None
        assert e.type
        assert e.source_class in valid_classes
    assert by_path["metadata.schema_version"].source_class == "CONSTANT"
    assert any(p.startswith("inputs.") and e.source_class == "INPUT" for p, e in by_path.items())
    assert any(
        p.startswith("business.years[]") and e.source_class == "DERIVED" for p, e in by_path.items()
    )


def test_data_dictionary_flattens_year_maps() -> None:
    """Per-year maps flatten to one [] entry per leaf shape, not one per calendar year."""
    paths = {e.path for e in build_comms_data_dictionary(CommsModelOutput)}
    assert any(p.startswith("business.years[]") for p in paths)
    assert any(p.startswith("physical.years[]") for p in paths)
    # No per-calendar-year entry leaked in.
    assert not any('years."2036"' in p for p in paths)


def test_formula_definitions_cover_comms_registry() -> None:
    """The formula catalog is one entry per comms_-prefixed FORMULAS key (DC excluded)."""
    defs = _build_formula_definitions()
    comms_keys = sorted(k for k in FORMULAS if k.startswith("comms_"))
    assert len(defs) == len(comms_keys)
    ids = {d.formula_id for d in defs}
    assert ids == set(comms_keys)
    # No data-center formula id leaked into the comms catalog.
    assert all(d.formula_id.startswith("comms_") for d in defs)
    for d in defs:
        assert d.formula_text
        assert d.description
    assert "comms_per_beam_capacity_from_empirical_anchor" in ids
    assert "comms_satellite_build_cost_from_four_areas" in ids


def test_enrich_fills_meta_scaffold(default_comms_output: CommsModelOutput) -> None:
    """Enrichment fills the four scaffold fields and preserves the engine's summary/notes."""
    enriched = enrich_comms_output(default_comms_output)
    m = enriched.meta
    assert m.data_dictionary
    assert m.formula_definitions
    assert m.validation_results
    assert m.query_examples
    assert m.source_status_summary == default_comms_output.meta.source_status_summary
    assert m.schema_version_notes == default_comms_output.meta.schema_version_notes


def test_engine_meta_is_lean_enrichment_fills_it(default_comms_output: CommsModelOutput) -> None:
    """The ENGINE output is lean (four enrichment fields empty); enrichment fills them.

    The revised Phase-3 lean-meta contract: the fields exist on the schema and
    default empty, the engine leaves them empty, and ``enrich_comms_output`` fills
    them.
    """
    lean = default_comms_output.meta
    assert lean.data_dictionary == []
    assert lean.formula_definitions == []
    assert lean.validation_results == []
    assert lean.query_examples == []
    assert lean.validation.rules == []
    assert lean.source_status_summary is not None
    assert lean.schema_version_notes
    enriched = enrich_comms_output(default_comms_output).meta
    assert enriched.data_dictionary
    assert enriched.formula_definitions
    assert enriched.validation_results
    assert enriched.query_examples
    assert enriched.validation.rules


def test_enrich_is_pure_no_new_numbers(default_comms_output: CommsModelOutput) -> None:
    """Enriching changes no physical/business cell value (it only touches meta)."""
    before = _all_cells(default_comms_output)
    after = _all_cells(enrich_comms_output(default_comms_output))
    assert before.keys() == after.keys()
    for path in before:
        assert before[path] == after[path]


def test_validation_results_map_checks_to_public_severities(
    default_enriched_output: CommsModelOutput,
) -> None:
    """Each public result mirrors a rule check with the severity mapped."""
    rules = default_enriched_output.meta.validation.rules
    results = default_enriched_output.meta.validation_results
    assert len(results) == len(rules)
    for rule, result in zip(rules, results, strict=True):
        assert result.validation_id == rule.name
        if rule.pass_check:
            assert result.severity.value == "pass"
        elif rule.severity.value == "minor":
            assert result.severity.value == "warn"
        else:
            assert result.severity.value == "fail"


def test_query_examples_are_well_formed() -> None:
    """Every query example is well-formed and applies to the space family."""
    assert QUERY_EXAMPLES
    names = {q.name for q in QUERY_EXAMPLES}
    for q in QUERY_EXAMPLES:
        assert q.name
        assert q.question_answered
        assert q.jq_expression
        assert q.expected_shape
        assert q.applies_to == QueryAppliesTo.SPACE
    assert "steady_state_customer_band_2036" in names
    assert "steady_state_cost_per_customer_band_2036" in names
    assert "spectrum_requirement" in names
    assert "per_beam_capacity_vs_naive_cross_check" in names
    assert "validation_warnings" in names


def test_enriched_output_round_trips_through_model(
    default_comms_output: CommsModelOutput,
) -> None:
    """The enriched JSON re-validates as a CommsModelOutput with a populated dictionary."""
    enriched = enrich_comms_output(default_comms_output)
    rebuilt = CommsModelOutput.model_validate(json.loads(render_comms_json(enriched)))
    assert rebuilt.meta.data_dictionary
    assert rebuilt.meta.formula_definitions
