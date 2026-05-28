"""Tests for ``data_center.generations`` — the typed per-generation input layer.

Coverage:
    - KNOWN_GENS parity: every field of every entry matches plan § 0's table.
    - YAML round-trip: dump → load → equal-to-original (via the in-memory
      string round-trip, and via the bundled ``scenarios/generations.yaml``).
    - extend_generations: empty-list rejection; correct cadence + count;
      Gen+1 / Gen+5 numeric parity with the prototype.
    - frontier_at: B300 / Rubin VR200 picks; extrapolated frontier at 2031;
      empty-list and no-available-generation error cases.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Final

import pytest
import yaml
from pydantic import ValidationError

from data_center.generations import (
    DEFAULT_GENERATIONS_DOC,
    GENERATIONS_YAML_KEY,
    KNOWN_GENS,
    GenerationSlopes,
    GenerationSpec,
    NoFrontierAvailableError,
    Source,
    SourcingClass,
    dump_generations_yaml,
    extend_generations,
    frontier_at,
    load_generations_yaml,
)

# Plan § 0 KNOWN_GENS table — replicated here to assert parity. Any change
# to the gospel must update both the production list and this fixture.
EXPECTED_KNOWN_GENS: Final[list[dict[str, object]]] = [
    {
        "name": "B200/GB200",
        "year_available": 2024.5,
        "usd_per_pkg": 50_000,
        "kw_per_pkg": 1.75,
        "kg_per_pkg": 18.9,
        "pf_per_pkg": 9.0,
        "die_count": 2,
        "sourcing": SourcingClass.FACT,
    },
    {
        "name": "B300/GB300",
        "year_available": 2025.5,
        "usd_per_pkg": 70_000,
        "kw_per_pkg": 2.05,
        "kg_per_pkg": 18.9,
        "pf_per_pkg": 15.0,
        "die_count": 2,
        "sourcing": SourcingClass.FACT,
    },
    {
        "name": "Rubin VR200",
        "year_available": 2026.5,
        "usd_per_pkg": 70_000,
        "kw_per_pkg": 2.60,
        "kg_per_pkg": 23.0,
        "pf_per_pkg": 34.0,
        "die_count": 2,
        "sourcing": SourcingClass.ESTIMATE,
    },
    {
        "name": "Rubin Ultra",
        "year_available": 2027.5,
        "usd_per_pkg": 180_000,
        "kw_per_pkg": 4.17,
        "kg_per_pkg": 22.0,
        "pf_per_pkg": 52.0,
        "die_count": 4,
        "sourcing": SourcingClass.ESTIMATE,
    },
    {
        "name": "Feynman",
        "year_available": 2029.0,
        "usd_per_pkg": 225_000,
        "kw_per_pkg": 5.50,
        "kg_per_pkg": 10.0,
        "pf_per_pkg": 100.0,
        "die_count": 8,
        "sourcing": SourcingClass.EXTRAPOLATION,
    },
]


# Numeric tolerance for float comparisons in extrapolation assertions.
EXTRAP_TOLERANCE: Final[float] = 1e-9


# ---------------------------------------------------------------------
# KNOWN_GENS parity
# ---------------------------------------------------------------------


def test_known_gens_count():
    assert len(KNOWN_GENS) == 5


def test_known_gens_fields_match_plan_table():
    """Every field of every KNOWN_GENS entry matches plan § 0's table."""
    assert len(KNOWN_GENS) == len(EXPECTED_KNOWN_GENS)
    for gen, expected in zip(KNOWN_GENS, EXPECTED_KNOWN_GENS):
        assert gen.name == expected["name"]
        assert gen.year_available == expected["year_available"]
        assert gen.usd_per_pkg == expected["usd_per_pkg"]
        assert gen.kw_per_pkg == expected["kw_per_pkg"]
        assert gen.kg_per_pkg == expected["kg_per_pkg"]
        assert gen.pf_per_pkg == expected["pf_per_pkg"]
        assert gen.die_count == expected["die_count"]
        assert gen.source.sourcing == expected["sourcing"]
        assert gen.source.doc_path == DEFAULT_GENERATIONS_DOC


def test_known_gens_is_frozen():
    """GenerationSpec entries are immutable."""
    with pytest.raises(ValidationError):
        KNOWN_GENS[0].name = "should-fail"  # type: ignore[misc]


def test_known_gens_year_strictly_monotonic():
    """The five known generations are in strictly increasing year order."""
    years = [g.year_available for g in KNOWN_GENS]
    assert years == sorted(years)
    assert len(set(years)) == len(years)


# ---------------------------------------------------------------------
# Validation: bounds and required fields
# ---------------------------------------------------------------------


def test_year_available_lower_bound_rejected():
    """year_available below 2020.0 is rejected."""
    with pytest.raises(ValidationError):
        GenerationSpec(
            name="Too old",
            year_available=2019.5,
            usd_per_pkg=10_000,
            kw_per_pkg=1.0,
            kg_per_pkg=10.0,
            pf_per_pkg=1.0,
            die_count=1,
            source=Source(
                doc_path="x",
                anchor=None,
                quoted_figure=None,
                sourcing=SourcingClass.FACT,
            ),
        )


def test_year_available_upper_bound_rejected():
    """year_available above 2050.0 is rejected."""
    with pytest.raises(ValidationError):
        GenerationSpec(
            name="Too new",
            year_available=2051.0,
            usd_per_pkg=10_000,
            kw_per_pkg=1.0,
            kg_per_pkg=10.0,
            pf_per_pkg=1.0,
            die_count=1,
            source=Source(
                doc_path="x",
                anchor=None,
                quoted_figure=None,
                sourcing=SourcingClass.FACT,
            ),
        )


def test_positive_constraints_rejected():
    """Non-positive numeric fields are rejected."""
    with pytest.raises(ValidationError):
        GenerationSpec(
            name="Zero kW",
            year_available=2026.0,
            usd_per_pkg=10_000,
            kw_per_pkg=0.0,
            kg_per_pkg=10.0,
            pf_per_pkg=1.0,
            die_count=1,
            source=Source(
                doc_path="x",
                anchor=None,
                quoted_figure=None,
                sourcing=SourcingClass.FACT,
            ),
        )


# ---------------------------------------------------------------------
# YAML round-trip
# ---------------------------------------------------------------------


def test_yaml_round_trip_in_memory():
    """Dump KNOWN_GENS to a YAML string, reload, equal to original."""
    dumped = yaml.safe_dump(
        {GENERATIONS_YAML_KEY: [g.model_dump(mode="json") for g in KNOWN_GENS]},
        sort_keys=False,
    )
    reloaded_dict = yaml.safe_load(dumped)
    reloaded = [
        GenerationSpec.model_validate(entry) for entry in reloaded_dict[GENERATIONS_YAML_KEY]
    ]
    assert reloaded == list(KNOWN_GENS)


def test_yaml_round_trip_via_disk(tmp_path):
    """Dump → file → load via the public helpers returns equal generations."""
    path = tmp_path / "round_trip.yaml"
    dump_generations_yaml(list(KNOWN_GENS), path)
    reloaded = load_generations_yaml(path)
    assert reloaded == list(KNOWN_GENS)


def test_bundled_generations_yaml_matches_known_gens():
    """The committed ``scenarios/generations.yaml`` must equal KNOWN_GENS."""
    bundled = Path(__file__).parent.parent.parent / "scenarios" / "generations.yaml"
    assert bundled.exists(), f"missing bundled file: {bundled}"
    loaded = load_generations_yaml(bundled)
    assert loaded == list(KNOWN_GENS)


def test_load_generations_yaml_rejects_non_mapping_root(tmp_path):
    path = tmp_path / "list_root.yaml"
    path.write_text("- not a mapping\n", encoding="utf-8")
    with pytest.raises(ValueError, match="must be a mapping"):
        load_generations_yaml(path)


def test_load_generations_yaml_rejects_missing_top_key(tmp_path):
    path = tmp_path / "no_key.yaml"
    path.write_text("other_key: []\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing top-level key"):
        load_generations_yaml(path)


def test_load_generations_yaml_rejects_non_list_value(tmp_path):
    path = tmp_path / "scalar_value.yaml"
    path.write_text("generations: not-a-list\n", encoding="utf-8")
    with pytest.raises(ValueError, match="must be a list"):
        load_generations_yaml(path)


# ---------------------------------------------------------------------
# extend_generations
# ---------------------------------------------------------------------


def test_extend_generations_empty_raises():
    with pytest.raises(ValueError, match="at least one known generation"):
        extend_generations([], GenerationSlopes(), 1.5, 2037.0)


def test_extend_generations_target_before_next_returns_input_unchanged():
    """target_yr earlier than (last.year + cadence) yields no extrapolations."""
    # Feynman = 2029.0; next at +1.5 = 2030.5; target 2030.4 → no extension.
    out = extend_generations(list(KNOWN_GENS), GenerationSlopes(), 1.5, 2030.4)
    assert out == list(KNOWN_GENS)


def test_extend_generations_default_target_yields_five_extraps():
    """target_yr 2037.0, cadence 1.5 → 5 extrapolated generations.

    Cadence schedule from Feynman (2029.0):
        Gen+1 @ 2030.5
        Gen+2 @ 2032.0
        Gen+3 @ 2033.5
        Gen+4 @ 2035.0
        Gen+5 @ 2036.5
        Gen+6 @ 2038.0 → past 2037, stop.
    """
    out = extend_generations(list(KNOWN_GENS), GenerationSlopes(), 1.5, 2037.0)
    extrapolated = out[len(KNOWN_GENS) :]
    assert len(extrapolated) == 5
    assert out[: len(KNOWN_GENS)] == list(KNOWN_GENS)

    expected_years = [2030.5, 2032.0, 2033.5, 2035.0, 2036.5]
    expected_names = [f"Gen+{i}(extrap)" for i in range(1, 6)]
    for gen, year, name in zip(extrapolated, expected_years, expected_names):
        assert gen.name == name
        assert gen.year_available == pytest.approx(year, abs=1e-12)
        assert gen.source.sourcing == SourcingClass.EXTRAPOLATION
        # die_count inherited from Feynman (held constant beyond known).
        assert gen.die_count == 8


def test_extend_generations_gen_plus_one_values_match_prototype():
    """Gen+1 values must match the prototype's `extend()` output exactly.

    Feynman base: usd=225_000, kw=5.50, kg=10.0, pf=100.0.
    Slopes (defaults): usd=+30%, kw=+20%, kg=-10%, pf=+62.5%.
    (kw corrected 0.30 -> 0.20 per validation V-A, sourcing_audit_05_21.md.)
    """
    out = extend_generations(list(KNOWN_GENS), GenerationSlopes(), 1.5, 2031.0)
    assert len(out) == len(KNOWN_GENS) + 1
    gen1 = out[-1]
    assert gen1.name == "Gen+1(extrap)"
    assert gen1.year_available == pytest.approx(2030.5, abs=1e-12)
    # int(225000 * 1.30) = int(292500.0) = 292500
    assert gen1.usd_per_pkg == 292_500
    assert math.isclose(gen1.kw_per_pkg, 5.50 * 1.20, abs_tol=EXTRAP_TOLERANCE)
    assert math.isclose(gen1.kg_per_pkg, 10.0 * 0.90, abs_tol=EXTRAP_TOLERANCE)
    assert math.isclose(gen1.pf_per_pkg, 100.0 * 1.625, abs_tol=EXTRAP_TOLERANCE)


def test_extend_generations_gen_plus_five_compounds_correctly():
    """Gen+5 values must match 5 compound applications of the slopes."""
    out = extend_generations(list(KNOWN_GENS), GenerationSlopes(), 1.5, 2037.0)
    gen5 = out[-1]
    assert gen5.name == "Gen+5(extrap)"
    # Compound usd: int(int(int(int(int(225000*1.30)*1.30)*1.30)*1.30)*1.30)
    expected_usd = 225_000
    for _ in range(5):
        expected_usd = int(expected_usd * 1.30)
    assert gen5.usd_per_pkg == expected_usd
    # Floats: simple compounding (no int truncation).
    # kw slope corrected 0.30 -> 0.20 per validation V-A (sourcing_audit_05_21.md).
    assert math.isclose(gen5.kw_per_pkg, 5.50 * (1.20**5), abs_tol=1e-6)
    assert math.isclose(gen5.kg_per_pkg, 10.0 * (0.90**5), abs_tol=1e-6)
    assert math.isclose(gen5.pf_per_pkg, 100.0 * (1.625**5), abs_tol=1e-6)


def test_extend_generations_does_not_mutate_input():
    """The input list is not mutated; a fresh list is returned."""
    known = list(KNOWN_GENS)
    original_id = id(known)
    out = extend_generations(known, GenerationSlopes(), 1.5, 2037.0)
    assert id(out) != original_id
    assert known == list(KNOWN_GENS)  # unchanged
    assert len(out) > len(known)


# ---------------------------------------------------------------------
# frontier_at
# ---------------------------------------------------------------------


def test_frontier_at_2026_is_b300():
    """FY2026: only B200 (2024.5) and B300 (2025.5) are available."""
    gen = frontier_at(2026.0, list(KNOWN_GENS))
    assert gen.name == "B300/GB300"


def test_frontier_at_2026_5_is_rubin_vr200():
    """FY2026.5: Rubin VR200 (2026.5) just arrives."""
    gen = frontier_at(2026.5, list(KNOWN_GENS))
    assert gen.name == "Rubin VR200"


def test_frontier_at_2031_returns_gen_plus_one():
    """FY2031 (after extending past 2031): Gen+1 (2030.5) is the frontier."""
    extended = extend_generations(list(KNOWN_GENS), GenerationSlopes(), 1.5, 2037.0)
    gen = frontier_at(2031.0, extended)
    assert gen.name == "Gen+1(extrap)"
    assert gen.year_available == pytest.approx(2030.5, abs=1e-12)


def test_frontier_at_exact_year_boundary_picks_that_generation():
    """A year matching exactly Feynman's release picks Feynman, not earlier."""
    gen = frontier_at(2029.0, list(KNOWN_GENS))
    assert gen.name == "Feynman"


def test_frontier_at_empty_list_raises():
    with pytest.raises(NoFrontierAvailableError):
        frontier_at(2024.0, [])


def test_frontier_at_before_first_gen_raises():
    """A year earlier than the earliest known generation raises."""
    with pytest.raises(NoFrontierAvailableError):
        frontier_at(2020.0, list(KNOWN_GENS))
