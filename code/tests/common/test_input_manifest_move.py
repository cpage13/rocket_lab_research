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
)
from common.provenance import as_float, as_int


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
        rationale="Investor-set scenario cap.",
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


def test_assumption_role_values() -> None:
    """Objective: the public assumption-role vocabulary is exactly these five.

    Expected: the four modeling roles plus ``scenario_override``, the marker
    for a value a scenario changed from the default.
    """
    assert {r.value for r in AssumptionRole} == {
        "default",
        "sensitivity",
        "validation_only",
        "derived_input",
        "scenario_override",
    }


def test_source_ref_type_three_values() -> None:
    """Objective: the source-reference vocabulary is exactly the kinds the builders emit.

    Expected: a SOURCE_INDEX claim, a research document, or a model derivation.
    """
    assert {t.value for t in SourceRefType} == {
        "source_index",
        "research_doc",
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
        rationale="Investor-set scenario cap.",
    )
    cell_obj = _cell("inputs.config.cadence.ceiling", 150, "Hard cap.", spec)
    assert isinstance(cell_obj, InputCell)
    assert cell_obj.source_refs[0].ref_type is SourceRefType.SOURCE_INDEX
    assert cell_obj.source_refs[0].claim_id == "COMM-001"


def test_the_strict_unwrap_rejects_a_flag_input() -> None:
    """Objective: an input cell's flag is never read as a number.

    Expected: ``as_int`` and ``as_float`` both raise ``TypeError`` naming the
    input's path for a ``True`` value.
    """
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
    with pytest.raises(TypeError, match="input inputs.flag is not an integer"):
        as_int(bool_cell)
    with pytest.raises(TypeError, match="input inputs.flag is not numeric"):
        as_float(bool_cell)
