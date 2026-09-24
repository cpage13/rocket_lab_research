"""Tests that the provenance spine moved cleanly to ``common`` (Phase 0, T0.11)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from common.input_manifest import AssumptionRole, InputCell, SourceStatus
from common.provenance import FORMULAS, FormulaSpec, ProvenanceCell, as_float, as_int, cell


def test_cell_factory_resolves_formula() -> None:
    result = cell(
        value=1.0,
        unit="MUSD",
        formula_name="total_cost_from_components",
        uses=[],
        sources=[],
        description="x",
    )
    assert isinstance(result, ProvenanceCell)
    assert result.formula == FORMULAS["total_cost_from_components"].formula
    assert result.formula_name == "total_cost_from_components"


def test_cell_factory_unknown_name_raises() -> None:
    with pytest.raises(KeyError):
        cell(
            value=1.0,
            unit="MUSD",
            formula_name="not_a_formula",
            uses=[],
            sources=[],
            description="x",
        )


def test_provenance_cell_is_frozen() -> None:
    result = cell(
        value=1.0,
        unit="MUSD",
        formula_name="total_cost_from_components",
        uses=[],
        sources=[],
        description="x",
    )
    with pytest.raises(ValidationError):
        result.value = 2.0  # type: ignore[misc]


def test_source_status_default_is_derived_estimate() -> None:
    result = cell(
        value=1.0,
        unit="MUSD",
        formula_name="total_cost_from_components",
        uses=[],
        sources=[],
        description="x",
    )
    assert result.source_status == SourceStatus.DERIVED_ESTIMATE


def test_formulas_nonempty() -> None:
    assert len(FORMULAS) > 0
    for spec in FORMULAS.values():
        assert isinstance(spec, FormulaSpec)
        assert spec.formula
        assert spec.description


def _cell_holding(value: float | int | str | bool | None) -> ProvenanceCell:
    """A computed cell holding ``value`` (the unwrap tests' subject)."""
    return cell(
        value=value,
        unit="count",
        formula_name="total_cost_from_components",
        uses=[],
        sources=[],
        description="a test cell",
    )


def test_as_float_reads_a_number_and_rejects_everything_else() -> None:
    """Objective: one strict way to read a number out of a cell.

    Expected: an int or float value reads as a float; a flag, a string, and a
    missing value raise ``TypeError`` naming the cell's formula.
    """
    assert as_float(_cell_holding(3)) == 3.0
    assert as_float(_cell_holding(2.5)) == 2.5
    for bad in (True, "2.5", None):
        with pytest.raises(TypeError, match="total_cost_from_components"):
            as_float(_cell_holding(bad))


def test_as_int_reads_only_an_integer() -> None:
    """Objective: a count is never truncated out of a fraction.

    Expected: an int reads back unchanged; a float (even a whole one like
    90.0, and a fractional one like 89.6 that the old ``int()`` unwrap
    truncated to 89), a flag, a string, and a missing value raise.
    """
    assert as_int(_cell_holding(90)) == 90
    for bad in (90.0, 89.6, True, "90", None):
        with pytest.raises(TypeError, match="is not an integer"):
            as_int(_cell_holding(bad))


def test_the_unwrap_reads_input_cells_too() -> None:
    """Objective: the same unwrap serves input cells, named by their path.

    Expected: a numeric input reads back; a list-valued input raises naming
    its path.
    """
    base = {
        "label": "x",
        "unit": None,
        "description": "x",
        "assumption_role": AssumptionRole.DEFAULT,
        "source_status": "scenario",
        "source_refs": [],
        "rationale": "x",
    }
    assert as_int(InputCell(path="inputs.config.fleet.service_life_years", value=5, **base)) == 5
    with pytest.raises(TypeError, match="input inputs.config.x is not numeric"):
        as_float(InputCell(path="inputs.config.x", value=[1, 2], **base))
