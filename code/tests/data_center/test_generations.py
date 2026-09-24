"""Tests for ``data_center.generations`` — the typed per-generation input layer.

Coverage:
    - KNOWN_GENS parity: every field of every entry matches plan § 0's table.
    - YAML round-trip: dump → load → equal-to-original (via the in-memory
      string round-trip, and via the bundled ``scenarios/generations.yaml``).
    - extend_generations: empty-list rejection; correct cadence + count;
      Gen+1 / Gen+5 numeric parity with the prototype.
    - frontier_at: B300 / Rubin VR200 picks; extrapolated frontier at 2031;
      empty-list and no-available-generation error cases.
    - Robustness: extrapolated years are latest + k x cadence (not
      accumulated) and a generation due exactly in a year flies that year;
      the list must be ordered; typos in slopes / generations / sources
      fail loudly; ``year_available`` spans the full MIN_FY..MAX_FY range;
      the slope defaults have one source.
"""

from __future__ import annotations

import math
import re
from typing import Final

import pytest
import yaml
from pydantic import ValidationError

from common.file_io import ModelFileError
from data_center.config import ValuationConfig, config_from_dict
from data_center.constants import (
    KG_GROWTH_PER_GEN_DEFAULT,
    KW_GROWTH_PER_GEN_DEFAULT,
    MAX_FY,
    PF_GROWTH_PER_GEN_DEFAULT,
    USD_GROWTH_PER_GEN_DEFAULT,
)
from data_center.engine import run_valuation
from data_center.generations import (
    DEFAULT_GENERATIONS_DOC,
    GENERATIONS_YAML_KEY,
    KNOWN_GENS,
    GenerationSlopes,
    GenerationSpec,
    NoFrontierAvailableError,
    Source,
    SourcingClass,
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
    """year_available above MAX_FY (2080) is rejected."""
    with pytest.raises(ValidationError):
        GenerationSpec(
            name="Too new",
            year_available=MAX_FY + 1.0,
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


def test_bundled_generations_yaml_matches_known_gens(scenarios_dir):
    """The committed ``scenarios/generations.yaml`` must equal KNOWN_GENS."""
    bundled = scenarios_dir / "generations.yaml"
    assert bundled.exists(), f"missing bundled file: {bundled}"
    loaded = load_generations_yaml(bundled)
    assert loaded == list(KNOWN_GENS)


@pytest.mark.parametrize(
    ("text", "reason"),
    [
        ("- not a mapping\n", "the YAML root must be a mapping, got list"),
        ("other_key: []\n", "missing top-level key 'generations'"),
        ("generations: not-a-list\n", "'generations' must be a list, got str"),
        ("generations:\n  - name: [B200\n", "malformed YAML"),
        ("", "missing top-level key 'generations'"),
    ],
    ids=["list_root", "missing_key", "scalar_value", "malformed", "empty"],
)
def test_load_generations_yaml_rejects_a_misshapen_file(tmp_path, text, reason):
    """Objective: a generations file of the wrong shape fails through the shared loader.

    The original trigger: malformed YAML here raised a raw PyYAML
    ``ParserError`` traceback, unlike the other loaders. Expected: every
    misshapen file raises the one file-boundary error, ``ModelFileError``,
    naming the file and the problem.
    """
    path = tmp_path / "generations.yaml"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ModelFileError, match=f"generations.yaml: {re.escape(reason)}"):
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


# ---------------------------------------------------------------------
# Robustness: cadence arithmetic, ordering, strict schemas, bounds
# ---------------------------------------------------------------------


def _spec_dict(name: str, year: float) -> dict[str, object]:
    """A minimal valid generation-spec mapping for scenario-style configs."""
    return {
        "name": name,
        "year_available": year,
        "usd_per_pkg": 70_000,
        "kw_per_pkg": 2.05,
        "kg_per_pkg": 18.9,
        "pf_per_pkg": 15.0,
        "die_count": 2,
        "source": {"doc_path": "tests/test_generations.py", "sourcing": "fact"},
    }


def test_extrapolated_years_are_latest_plus_k_times_cadence():
    """Objective: extrapolated availability years do not accumulate float error.

    With a 1.4-year cadence from Feynman (2029.0), the fifth extrapolated
    generation is due in 2036. Stepwise addition gives 2036.0000000000005.
    Expected: Gen+5 is dated 2029.0 + 5 x 1.4 and every Gen+k matches
    2029.0 + k x 1.4 exactly.
    """
    out = extend_generations(list(KNOWN_GENS), GenerationSlopes(), 1.4, 2037.0)
    extrapolated = out[len(KNOWN_GENS) :]
    for k, gen in enumerate(extrapolated, start=1):
        assert gen.year_available == 2029.0 + k * 1.4
    assert extrapolated[4].name == "Gen+5(extrap)"


def test_generation_due_exactly_in_a_year_flies_that_year():
    """Objective: a generation whose float year lands a few ulps late is available.

    Expected: ``frontier_at(2036.0)`` picks a generation dated
    2036.0000000000005 (the accumulated 1.4-cadence value).
    """
    late_by_ulps = KNOWN_GENS[-1].model_copy(
        update={"name": "Due-2036", "year_available": 2036.0000000000005}
    )
    assert frontier_at(2036.0, [*KNOWN_GENS, late_by_ulps]).name == "Due-2036"


def test_release_cadence_1_4_flies_the_due_generation_in_fy2036():
    """Objective: the cadence-1.4 trigger end to end.

    Expected: with ``release_cadence_yr: 1.4`` the FY2036 frontier is
    Gen+5(extrap) (due 2029.0 + 5 x 1.4 = 2036), not Gen+4.
    """
    cfg = config_from_dict({"gospel": {"release_cadence_yr": 1.4}})
    fy2036 = run_valuation(cfg).physical.years["2036"]
    assert fy2036.frontier_generation.value == "Gen+5(extrap)"


def test_extend_generations_rejects_an_unordered_list():
    """Objective: extrapolation never extends from an older entry.

    Expected: a newest-first list raises ValueError naming the ordering rule.
    """
    with pytest.raises(ValueError, match="oldest first"):
        extend_generations(list(reversed(KNOWN_GENS)), GenerationSlopes(), 1.5, 2037.0)


def test_newest_first_generations_fail_at_load():
    """Objective: a scenario's unordered generations list fails at load.

    Expected: config_from_dict raises a ValidationError on a newest-first list.
    """
    with pytest.raises(ValidationError, match="oldest first"):
        config_from_dict(
            {"generations": [_spec_dict("Newer", 2026.5), _spec_dict("Older", 2025.5)]}
        )


def test_duplicate_generation_years_fail_at_load():
    """Objective: two generations with the same year make the frontier ambiguous.

    Expected: config_from_dict raises a ValidationError.
    """
    with pytest.raises(ValidationError, match="strictly increasing"):
        config_from_dict({"generations": [_spec_dict("A", 2025.5), _spec_dict("B", 2025.5)]})


def test_empty_generations_list_fails_at_load():
    """Objective: an empty override list has nothing to extend from.

    Expected: config_from_dict raises a ValidationError at load.
    """
    with pytest.raises(ValidationError, match="at least one generation"):
        config_from_dict({"generations": []})


def test_slopes_typo_fails_at_load():
    """Objective: a misspelled slope is not silently ignored.

    Expected: ``slopes: {pf_growth: 0.1}`` raises a ValidationError naming
    the unknown key.
    """
    with pytest.raises(ValidationError, match="pf_growth"):
        config_from_dict({"slopes": {"pf_growth": 0.1}})


def test_generation_entry_typo_fails_at_load():
    """Objective: a misspelled generation field is not silently ignored.

    Expected: an extra ``kw_per_package`` key raises a ValidationError.
    """
    entry = _spec_dict("Typo", 2025.5)
    entry["kw_per_package"] = 3.0
    with pytest.raises(ValidationError, match="kw_per_package"):
        config_from_dict({"generations": [entry]})


def test_source_typo_fails_at_load():
    """Objective: a misspelled source field is not silently ignored.

    Expected: an extra ``doc`` key in a generation's source raises a
    ValidationError.
    """
    entry = _spec_dict("Typo", 2025.5)
    entry["source"] = {"doc_path": "x", "sourcing": "fact", "doc": "y"}
    with pytest.raises(ValidationError, match="doc"):
        config_from_dict({"generations": [entry]})


def test_late_window_extends_generations_past_2050():
    """Objective: every window the config accepts can be extrapolated.

    A 2031 base year with a 20-year horizon needs generations dated past
    2050 (the old bound). Expected: the run completes and its FY2051 frontier
    is an extrapolated generation.
    """
    cfg = config_from_dict({"metadata": {"base_year": 2031, "horizon_years": 20}})
    out = run_valuation(cfg)
    assert str(out.physical.years["2051"].frontier_generation.value).endswith("(extrap)")


def test_slope_defaults_have_one_source():
    """Objective: the default slopes are defined once.

    Expected: ``GenerationSlopes()`` equals the named default constants and
    ``ValuationConfig().slopes`` is exactly ``GenerationSlopes()``.
    """
    slopes = GenerationSlopes()
    assert slopes.usd_growth_per_gen == USD_GROWTH_PER_GEN_DEFAULT
    assert slopes.kw_growth_per_gen == KW_GROWTH_PER_GEN_DEFAULT
    assert slopes.kg_growth_per_gen == KG_GROWTH_PER_GEN_DEFAULT
    assert slopes.pf_growth_per_gen == PF_GROWTH_PER_GEN_DEFAULT
    assert ValuationConfig().slopes == slopes


def test_extend_generations_reports_an_overflowing_extension():
    """Objective: a release cadence too short to extrapolate is a clean error.

    The original trigger: ``release_cadence_yr`` 0.001 needs about 8,000
    extrapolated generations to cover the default window; compounding the
    slopes overflowed to infinity and ``int(inf)`` crashed with an
    ``OverflowError`` traceback. Expected: a ValueError that names the
    overflow and the dial to change, raised before any infinite value enters
    the list.
    """
    with pytest.raises(ValueError, match=r"generation extension overflows.*release_cadence_yr"):
        extend_generations(list(KNOWN_GENS), GenerationSlopes(), 0.001, 2037.0)
