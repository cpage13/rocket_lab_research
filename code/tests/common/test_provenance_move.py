"""Tests that the provenance spine moved cleanly to ``common`` (Phase 0, T0.11)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from common.input_manifest import SourceStatus
from common.provenance import FORMULAS, FormulaSpec, ProvenanceCell, cell


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
