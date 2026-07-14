"""Regression tests for the v8 output naming convention (plan §5 T62).

Cycle-1 shipped a field ``annual_rev_per_node_musd`` that was *named*
revenue but *held* gross profit (revenue − cost). The investor caught it
when "2036 revenue" would not reconcile against the cost block. D25 fixed
it: v8 splits the per-node and fleet money lines into explicit
``revenue_*`` / ``cost_*`` / ``gross_profit_*`` fields.

This module guards that the bug cannot return. Three families:

1. **The old field is gone** — no field path anywhere in a v8
   ``ValuationOutput`` is named ``annual_rev_per_node_musd``.
2. **revenue ≠ profit** — a field named ``revenue_*`` carries revenue,
   not profit. Proven algebraically: ``revenue − gross_profit == cost``
   for every band, and ``revenue > gross_profit`` (since R > 1). A
   conflated field would break this identity.
3. **Unit-token consistency** — a field-name token implies its unit:
   ``kW`` not ``MW`` for power, ``t`` vs ``kg`` not swapped for mass.
   Checked against the generated ``meta.data_dictionary`` units and the
   per-cell ``ProvenanceCell.unit`` strings.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from data_center.config import load_config
from data_center.engine import run_valuation

# The packaged default scenario, resolved relative to this test file.
_DEFAULT_YAML = Path(__file__).resolve().parents[2] / "scenarios" / "default.yaml"

# The cycle-1 misnamed field — must not exist anywhere in v8 output.
_BANNED_FIELD = "annual_rev_per_node_musd"

# Unit families a field-name token must map to. A token in the field name
# (e.g. `kw`, `_t`, `kg`) constrains the declared unit to one of these.
_KW_UNITS = {"kW", "kW/pkg", "PFLOPS/kW", "MUSD/kW", "t/kW"}
_TONNE_UNITS = {"t"}
_KG_UNITS = {"kg", "kg/m2", "kg/pkg"}

# Tolerance for the revenue − profit == cost algebraic identity (floats).
_REL_TOL = 1e-9


@pytest.fixture(scope="module")
def default_output_json() -> dict[str, Any]:
    """The default scenario, run through the engine and dumped to a dict.

    The JSON-shaped dict (via ``model_dump_json`` → ``json.loads``) is
    what the CLI's ``--json`` path emits; the naming checks walk it.
    """
    output = run_valuation(load_config(str(_DEFAULT_YAML)))
    parsed: dict[str, Any] = json.loads(output.model_dump_json())
    return parsed


def _walk_field_paths(node: Any, prefix: str = "") -> Iterator[str]:
    """Yield every dotted field path in a nested JSON-shaped structure.

    Dict keys extend the path; list elements are walked under the same
    path (the index is not part of the name). Used to enumerate every
    field name a v8 output exposes.
    """
    if isinstance(node, dict):
        for key, value in node.items():
            child = f"{prefix}.{key}" if prefix else key
            yield child
            yield from _walk_field_paths(value, child)
    elif isinstance(node, list):
        for item in node:
            yield from _walk_field_paths(item, prefix)


# --------------------------------------------------------------------------
# Family 1 — the cycle-1 misnamed field is gone
# --------------------------------------------------------------------------


def test_banned_field_absent_everywhere(default_output_json: dict[str, Any]) -> None:
    """No field path in a v8 output is named ``annual_rev_per_node_musd``."""
    offending = [p for p in _walk_field_paths(default_output_json) if p.endswith(_BANNED_FIELD)]
    assert offending == [], f"cycle-1 misnamed field resurfaced at: {offending}"


def test_banned_field_absent_in_physical_and_business_years(
    default_output_json: dict[str, Any],
) -> None:
    """The per-year physical / business cells use explicit revenue/profit names."""
    for block in ("physical", "business"):
        for year, cells in default_output_json[block]["years"].items():
            assert _BANNED_FIELD not in cells, f"{block}.years.{year} still carries {_BANNED_FIELD}"


# --------------------------------------------------------------------------
# Family 2 — revenue ≠ profit (the D25 bug, proven algebraically)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("band", ["central", "low", "high"])
def test_per_node_revenue_is_not_profit(default_output_json: dict[str, Any], band: str) -> None:
    """`revenue_annual_per_node_musd_*` holds revenue, not profit.

    For every year and band: ``revenue − gross_profit == cost`` (the
    identity that holds only if the revenue field really is revenue) and
    ``revenue > gross_profit`` (R > 1). The cycle-1 bug — a revenue-named
    field holding profit — would fail both.
    """
    for year, cells in default_output_json["physical"]["years"].items():
        revenue = cells[f"revenue_annual_per_node_musd_{band}"]["value"]
        profit = cells[f"gross_profit_annual_per_node_musd_{band}"]["value"]
        cost = cells["cost_annual_per_node_musd"]["value"]
        assert revenue == pytest.approx(profit + cost, rel=_REL_TOL), (
            f"physical.years.{year} ({band}): revenue != profit + cost — "
            f"the revenue field is mislabelled"
        )
        assert revenue >= profit, (
            f"physical.years.{year} ({band}): revenue < gross_profit (R>1 violated)"
        )


@pytest.mark.parametrize("band", ["central", "low", "high"])
def test_fleet_revenue_is_not_profit(default_output_json: dict[str, Any], band: str) -> None:
    """`revenue_annual_fleet_musd_*` holds fleet revenue, not fleet profit."""
    for year, cells in default_output_json["business"]["years"].items():
        revenue = cells[f"revenue_annual_fleet_musd_{band}"]["value"]
        profit = cells[f"gross_profit_annual_fleet_musd_{band}"]["value"]
        cost = cells["cost_annual_fleet_musd"]["value"]
        assert revenue == pytest.approx(profit + cost, rel=_REL_TOL), (
            f"business.years.{year} ({band}): fleet revenue != profit + cost"
        )
        assert revenue >= profit, (
            f"business.years.{year} ({band}): fleet revenue < fleet gross_profit"
        )


def test_revenue_and_profit_fields_are_distinct_names(
    default_output_json: dict[str, Any],
) -> None:
    """Revenue and profit are separately-named fields, never one conflated field."""
    physical_2036 = default_output_json["physical"]["years"]["2036"]
    business_2036 = default_output_json["business"]["years"]["2036"]
    for cells in (physical_2036, business_2036):
        revenue_fields = {k for k in cells if k.startswith("revenue_")}
        profit_fields = {k for k in cells if k.startswith("gross_profit_")}
        # Both families exist, and no name is in both.
        assert revenue_fields, "no revenue_* field found"
        assert profit_fields, "no gross_profit_* field found"
        assert revenue_fields.isdisjoint(profit_fields)


# --------------------------------------------------------------------------
# Family 3 — unit-token consistency (kW ≠ MW, t ≠ kg)
# --------------------------------------------------------------------------


def _data_dictionary_units(output: dict[str, Any]) -> dict[str, str]:
    """Return ``{field_path: unit}`` from the generated data dictionary."""
    return {entry["path"]: entry["unit"] for entry in output["meta"]["data_dictionary"]}


def test_no_field_name_uses_megawatts(default_output_json: dict[str, Any]) -> None:
    """No field name uses an ``mw`` / megawatt token — power is in kW.

    The model is power-budgeted in kW per package and per node; an ``mw``
    token in a field name would be a unit-scale error.
    """
    for path in _walk_field_paths(default_output_json):
        leaf = path.rsplit(".", 1)[-1].lower()
        if "generation_slopes" in path:
            continue
        tokens = leaf.split("_")
        assert "mw" not in tokens, f"field {path!r} uses a megawatt token"


def test_kw_named_fields_have_kw_units(default_output_json: dict[str, Any]) -> None:
    """Every ``kw``-token field declares a kW-family unit (not MW, not kg)."""
    units = _data_dictionary_units(default_output_json)
    for path, unit in units.items():
        leaf = path.rsplit(".", 1)[-1].lower()
        if "generation_slopes" in path:
            continue
        if "kw" in leaf.split("_"):
            assert unit in _KW_UNITS, f"{path}: kw-named field has non-kW unit {unit!r}"


def test_mass_field_tonne_vs_kg_tokens_match_units(
    default_output_json: dict[str, Any],
) -> None:
    """A ``_t`` mass field carries tonnes; a ``kg`` field carries kg — not swapped.

    Mass appears at two scales: per-node in tonnes (``mass_per_node_t``)
    and per-package in kg. A field-name token of ``t`` or ``kg`` must
    agree with the declared unit so the two scales never get confused.
    """
    units = _data_dictionary_units(default_output_json)
    for path, unit in units.items():
        leaf = path.rsplit(".", 1)[-1].lower()
        if "generation_slopes" in path:
            continue
        # Token-split so `kg` matches only as a whole token — `kw_per_pkg`
        # contains the substring "kg" inside "pkg" but is not a mass field.
        tokens = leaf.split("_")
        if tokens[-1] == "t":  # trailing `_t` => tonnes
            assert unit in _TONNE_UNITS, f"{path}: `_t` field has non-tonne unit {unit!r}"
        if "kg" in tokens:  # `kg` as a token => kilograms (incl. kg/m2)
            assert unit in _KG_UNITS, f"{path}: `kg` field has non-kg unit {unit!r}"


def test_per_cell_unit_strings_match_field_name_tokens(
    default_output_json: dict[str, Any],
) -> None:
    """Per-year ProvenanceCell ``unit`` strings agree with their field-name tokens.

    Walks ``physical.years`` / ``business.years`` — the leaf cells the
    naming bug lived in — and checks each cell's own ``unit`` against the
    field name: ``kw`` ⇒ kW-family, trailing ``_t`` ⇒ tonnes,
    trailing ``_musd`` ⇒ MUSD, trailing ``_pct`` ⇒ percent.
    """

    def _check(field: str, node: dict[str, Any], where: str) -> None:
        """Check one node — a cell against its name, or recurse a sub-object.

        A leaf cell carries a ``unit`` key; a sub-object (e.g.
        ``cost_breakdown``) is a dict of cells and is walked recursively.
        """
        if not isinstance(node, dict):
            return
        if "unit" not in node:
            for sub_field, sub_node in node.items():
                _check(sub_field, sub_node, f"{where}.{sub_field}")
            return
        unit = node["unit"]
        tokens = field.lower().split("_")
        if "kw" in tokens:
            assert unit in _KW_UNITS, f"{where}: kw token, unit {unit!r}"
        if tokens[-1] == "t":
            assert unit in _TONNE_UNITS, f"{where}: `_t`, unit {unit!r}"
        if tokens[-1] == "musd":
            assert unit == "MUSD", f"{where}: `_musd`, unit {unit!r}"
        if tokens[-1] == "pct":
            assert unit == "percent", f"{where}: `_pct`, unit {unit!r}"

    for block in ("physical", "business"):
        for year, cells in default_output_json[block]["years"].items():
            for field, cell in cells.items():
                _check(field, cell, f"{block}.years.{year}.{field}")
