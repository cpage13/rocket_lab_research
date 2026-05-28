"""Tests for the provenance module — ProvenanceCell + FORMULAS + cell() factory.

Locks the Phase 2 provenance infrastructure: the frozen ProvenanceCell /
FormulaSpec models, the FORMULAS lookup table, and the cell() factory's
formula-text resolution + unknown-formula KeyError contract.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from data_center.provenance import (
    FORMULAS,
    FieldPath,
    FormulaSpec,
    ProvenanceCell,
    cell,
)


def test_cell_factory_constructs_provenance_cell() -> None:
    """cell() builds a ProvenanceCell carrying the passed value + unit."""
    c = cell(
        value=42.0,
        unit="kW",
        formula_name="kw_per_node_from_n_and_kw_per_pkg",
        uses=['physical.years."2036".n_packages'],
        sources=["cycle-1"],
        description="test",
    )
    assert isinstance(c, ProvenanceCell)
    assert c.value == 42.0
    assert c.unit == "kW"


def test_cell_factory_raises_on_unknown_formula_name() -> None:
    """An unknown formula_name fails fast with a KeyError."""
    with pytest.raises(KeyError, match="not in FORMULAS"):
        cell(
            value=0.0,
            unit="-",
            formula_name="this_does_not_exist",
            uses=[],
            sources=[],
            description="test",
        )


def test_cell_resolves_formula_text_from_formulas_table() -> None:
    """cell() copies the human-readable formula text out of FORMULAS."""
    c = cell(
        value=1.0,
        unit="-",
        formula_name="mass_utilization",
        uses=[],
        sources=[],
        description="test",
    )
    assert c.formula == FORMULAS["mass_utilization"].formula
    assert c.formula_name == "mass_utilization"


def test_provenance_cell_is_frozen() -> None:
    """ProvenanceCell is immutable — assigning a field raises."""
    c = cell(
        value=1.0,
        unit="-",
        formula_name="mass_utilization",
        uses=[],
        sources=[],
        description="test",
    )
    with pytest.raises(ValidationError):
        c.value = 2.0  # type: ignore[misc]


def test_formulas_table_nonempty() -> None:
    """FORMULAS covers every formula_name listed in plan section 0.8."""
    assert len(FORMULAS) >= 25


def test_formulas_entries_are_frozen() -> None:
    """Each FormulaSpec in FORMULAS is immutable."""
    spec = next(iter(FORMULAS.values()))
    with pytest.raises(ValidationError):
        spec.formula = "tampered"  # type: ignore[misc]


def test_cell_serializes_to_json() -> None:
    """A ProvenanceCell round-trips cleanly through model_dump_json."""
    c = cell(
        value=1.5,
        unit="ratio",
        formula_name="r_at_year_from_band_anchors",
        uses=["inputs.r_band.central"],
        sources=["R2"],
        description="R at 2026",
    )
    j = c.model_dump_json()
    assert '"value":1.5' in j
    assert '"formula_name":"r_at_year_from_band_anchors"' in j


def test_field_path_is_alias_for_str() -> None:
    """FieldPath is a str alias — a concrete path is a real str."""
    p: FieldPath = 'physical.years."2036".kw_per_node'
    assert isinstance(p, str)


def test_formula_spec_has_formula_and_description() -> None:
    """Every FormulaSpec carries a non-empty formula + description."""
    spec = FORMULAS["kw_per_node_from_n_and_kw_per_pkg"]
    assert spec.formula
    assert spec.description


def test_cell_with_none_value() -> None:
    """A not-yet-computed cell carries value=None."""
    c = cell(
        value=None,
        unit="-",
        formula_name="binding_constraint_from_utilizations",
        uses=[],
        sources=[],
        description="not computed yet",
    )
    assert c.value is None


def test_cell_with_string_value() -> None:
    """An enum-valued cell carries a str value."""
    c = cell(
        value="MASS",
        unit="enum",
        formula_name="binding_constraint_from_utilizations",
        uses=[],
        sources=[],
        description="enum case",
    )
    assert c.value == "MASS"


def test_every_formulas_entry_is_a_formula_spec() -> None:
    """Every value in FORMULAS is a FormulaSpec (typed table integrity)."""
    for name, spec in FORMULAS.items():
        assert isinstance(spec, FormulaSpec), f"FORMULAS[{name!r}] is not a FormulaSpec"
