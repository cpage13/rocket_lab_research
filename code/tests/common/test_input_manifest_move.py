"""Tests that the input-cell vocabulary moved cleanly to ``common`` (Phase 0, T0.12)."""

from __future__ import annotations

import pytest

from common.input_manifest import (
    AssumptionRole,
    CellSpec,
    InputCell,
    SourceRef,
    SourceRefType,
    SourceStatus,
    _cell,
    _int_value,
)


def test_input_cell_full_field_list() -> None:
    ref = SourceRef(
        ref_type=SourceRefType.SOURCE_INDEX,
        ref="research/SOURCE_INDEX.md#COMM-001",
        claim_id="COMM-001",
        note="supports the value",
    )
    cell_obj = InputCell(
        path="inputs.config.cadence.ceiling",
        label="Cadence ceiling",
        value=150,
        unit="count",
        description="Hard cap on launches per year.",
        assumption_role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        source_refs=[ref],
        rationale="Founder-set scenario cap.",
        notes="Sensitivity dial.",
    )
    dumped = cell_obj.model_dump()
    expected_keys = {
        "path",
        "label",
        "value",
        "unit",
        "description",
        "assumption_role",
        "source_status",
        "source_refs",
        "rationale",
        "notes",
    }
    assert expected_keys.issubset(dumped.keys())
    assert cell_obj.path == "inputs.config.cadence.ceiling"
    assert cell_obj.value == 150
    assert cell_obj.unit == "count"
    assert cell_obj.assumption_role == AssumptionRole.DEFAULT
    assert cell_obj.source_status == SourceStatus.SCENARIO
    assert cell_obj.source_refs[0].claim_id == "COMM-001"
    assert cell_obj.notes == "Sensitivity dial."


def test_source_status_eight_values() -> None:
    assert {s.value for s in SourceStatus} == {
        "certified",
        "sourced_estimate",
        "derived_estimate",
        "projection",
        "extrapolation",
        "scenario",
        "placeholder",
        "stale",
    }


def test_assumption_role_four_values() -> None:
    assert {r.value for r in AssumptionRole} == {
        "default",
        "sensitivity",
        "validation_only",
        "derived_input",
    }


def test_source_ref_type_four_values() -> None:
    assert {t.value for t in SourceRefType} == {
        "source_index",
        "research_doc",
        "external_url",
        "model_derivation",
    }


def test_cell_builder_round_trip() -> None:
    spec = CellSpec(
        label="Cadence ceiling",
        unit="count",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="COMM-001",
        source_note="supports the value",
        rationale="Founder-set scenario cap.",
    )
    cell_obj = _cell("inputs.config.cadence.ceiling", 150, "Hard cap.", spec)
    assert isinstance(cell_obj, InputCell)
    assert cell_obj.source_refs[0].ref_type is SourceRefType.SOURCE_INDEX
    assert cell_obj.source_refs[0].claim_id == "COMM-001"


def test_int_value_rejects_bool() -> None:
    spec = CellSpec(
        label="A flag",
        unit=None,
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="COMM-001",
        source_note="note",
        rationale="rationale",
    )
    bool_cell = _cell("inputs.flag", True, "A flag.", spec)
    with pytest.raises(TypeError):
        _int_value(bool_cell)
