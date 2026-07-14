"""Tests for the v8 engine-computed validation rules (V1..V17).

Two test families per rule:

1. **Passing case** — the default-scenario engine output trips no rule.
2. **Tripping case** — a copy-mutated v8 artifact triggers the rule.

Also locks the aggregator contract: :func:`compute_validation` returns
exactly 17 checks in V1..V17 declaration order and all pass on the default
scenario.

**Cycle-2 v8 re-pathing (V1-V10).** The cycle-1 V-rules are re-pointed at
the v8 output structure (``physical.years`` / ``business.years`` /
``inputs.generations``). V5 (was ``monotonic_compute_share``) and V10 (was
``decisions_populated``) lost their cycle-1 subject when the v8 schema
dropped the ``compute_share`` and ``decisions`` blocks, so they are
re-targeted — V5 to PF/kW monotonicity, V10 to the data-dictionary block.

**Cycle-2 new rules (V11-V17).** Seven new cross-check rules: V11
no-legacy-r-scalar, V12 operator/R consistency, V13 provenance formula
keys, V14 cadence monotonicity, V15 volume fits horizon, V16 fleet-cliff
consistency, V17 radiator-dial-matches-architecture (strategy § 5.1).

The tripping fixtures use Pydantic's ``model_copy(update=...)`` to build a
ProvenanceCell with an out-of-band value and re-key the per-year map —
exactly the kind of bad state the V-rules are designed to catch.
"""

from __future__ import annotations

import pytest

from data_center.config import RadiatorArchitecture, ValuationConfig, config_from_dict
from data_center.engine import run_valuation
from data_center.input_manifest import InputCell, InputPath
from data_center.output import (
    PhysicalYear,
    Severity,
    ValuationOutput,
)
from data_center.provenance import ProvenanceCell
from data_center.validation import (
    B2B_R_CENTRAL_FLOOR,
    COST_ANNUAL_MAX_MUSD,
    COST_ANNUAL_MIN_MUSD,
    LEGACY_R_SCALAR_FIELD,
    MASS_UTIL_MAX_PCT,
    MASS_UTIL_MIN_PCT,
    PF_PER_KW_MAX,
    PF_PER_KW_MIN,
    RADIATOR_T_PER_KW_CO_MOUNTED_MIN,
    USD_PER_PKG_MAX,
    check_cadence_monotonicity,
    check_cost_annual_per_node_in_band,
    check_data_dictionary_populated,
    check_fleet_cliff_consistency,
    check_gpu_count_positive,
    check_launch_cost_non_increasing,
    check_mass_utilization_in_band,
    check_monotonic_pf_per_kw,
    check_no_legacy_r_scalar,
    check_no_trillion_dollar_pkg,
    check_operator_r_consistency,
    check_pf_per_kw_in_band,
    check_positive_margin_floor,
    check_provenance_formula_keys,
    check_radiator_dial_arch_consistency,
    check_revenue_above_cost_per_node,
    check_volume_fits_horizon,
    compute_validation,
)

# ---------------------------------------------------------------------------
# Shared fixtures + mutation helper
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def default_output() -> ValuationOutput:
    """The default-scenario v8 engine output — every rule should pass."""
    return run_valuation(ValuationConfig())


def _set_cell(cell: ProvenanceCell, value: float | int | str) -> ProvenanceCell:
    """Return a copy of ``cell`` with its ``value`` replaced."""
    return cell.model_copy(update={"value": value})


def _mutate_physical(
    output: ValuationOutput, fy: str, field: str, value: float | int | str
) -> ValuationOutput:
    """Return a new output with one physical-year cell's value replaced."""
    py = output.physical.years[fy]
    new_py = py.model_copy(update={field: _set_cell(getattr(py, field), value)})
    new_years = dict(output.physical.years)
    new_years[fy] = new_py
    new_physical = output.physical.model_copy(update={"years": new_years})
    return output.model_copy(update={"physical": new_physical})


def _mutate_business(
    output: ValuationOutput, fy: str, field: str, value: float | int | str
) -> ValuationOutput:
    """Return a new output with one business-year cell's value replaced."""
    by = output.business.years[fy]
    new_by = by.model_copy(update={field: _set_cell(getattr(by, field), value)})
    new_years = dict(output.business.years)
    new_years[fy] = new_by
    new_business = output.business.model_copy(update={"years": new_years})
    return output.model_copy(update={"business": new_business})


def _last_fy(output: ValuationOutput) -> str:
    """The latest fiscal year (JSON-string key) of the physical block."""
    return max(output.physical.years, key=int)


def _mutate_gospel(output: ValuationOutput, key: str, value: float | int) -> ValuationOutput:
    """Return a new output with one ``inputs.gospel`` key set/added."""
    path = InputPath(f"inputs.config.physical.{key}")
    if hasattr(output.inputs.config.physical, key):
        current = getattr(output.inputs.config.physical, key)
        assert isinstance(current, InputCell)
        new_cell = current.model_copy(update={"value": value})
        new_physical = output.inputs.config.physical.model_copy(update={key: new_cell})
        new_config = output.inputs.config.model_copy(update={"physical": new_physical})
    else:
        template = output.inputs.config.physical.mass_envelope_t
        new_cell = template.model_copy(update={"path": str(path), "label": key, "value": value})
        new_config = output.inputs.config
    new_index = dict(output.inputs.assumption_index)
    new_index[path] = new_cell
    new_inputs = output.inputs.model_copy(
        update={"config": new_config, "assumption_index": new_index}
    )
    return output.model_copy(update={"inputs": new_inputs})


def _mutate_physical_cell_attr(
    output: ValuationOutput, fy: str, field: str, attr: str, value: str
) -> ValuationOutput:
    """Return a new output with one physical-year cell's ``attr`` replaced.

    Unlike :func:`_mutate_physical` (which replaces a cell's ``value``),
    this replaces an arbitrary ProvenanceCell attribute — used by the V13
    test to inject a bad ``formula_name``.
    """
    py = output.physical.years[fy]
    cell = getattr(py, field)
    new_cell = cell.model_copy(update={attr: value})
    new_py = py.model_copy(update={field: new_cell})
    new_years = dict(output.physical.years)
    new_years[fy] = new_py
    new_physical = output.physical.model_copy(update={"years": new_years})
    return output.model_copy(update={"physical": new_physical})


# ---------------------------------------------------------------------------
# compute_validation — the aggregator
# ---------------------------------------------------------------------------


def test_compute_validation_returns_exactly_seventeen_checks(
    default_output: ValuationOutput,
) -> None:
    """The aggregator emits 17 checks (one per V1..V17)."""
    assert len(compute_validation(default_output)) == 17


def test_compute_validation_default_scenario_all_pass(
    default_output: ValuationOutput,
) -> None:
    """Every V1..V17 rule passes on the default scenario."""
    failing = [c for c in compute_validation(default_output) if not c.pass_check]
    assert not failing, f"unexpected failing checks: {[(c.name, c.computed) for c in failing]}"


def test_compute_validation_preserves_v1_to_v17_order(
    default_output: ValuationOutput,
) -> None:
    """Aggregator output order is the V1..V17 declaration order."""
    checks = compute_validation(default_output)
    expected = [
        "mass_utilization_in_band",
        "no_trillion_dollar_pkg",
        "positive_margin_floor",
        "gpu_count_positive",
        "monotonic_pf_per_kw",
        "pf_per_kw_in_band",
        "launch_cost_non_increasing",
        "revenue_above_cost_per_node",
        "cost_annual_per_node_in_band",
        "data_dictionary_populated",
        "no_legacy_r_scalar",
        "operator_r_consistency",
        "provenance_formula_keys",
        "cadence_monotonicity",
        "volume_fits_horizon",
        "fleet_cliff_consistency",
        "radiator_dial_matches_architecture",
    ]
    assert [c.name for c in checks] == expected


def test_severity_classifications(default_output: ValuationOutput) -> None:
    """Each rule's severity matches its tier."""
    by_name = {c.name: c for c in compute_validation(default_output)}
    assert by_name["mass_utilization_in_band"].severity == Severity.CRITICAL
    assert by_name["no_trillion_dollar_pkg"].severity == Severity.CRITICAL
    assert by_name["positive_margin_floor"].severity == Severity.CRITICAL
    assert by_name["gpu_count_positive"].severity == Severity.CRITICAL
    assert by_name["monotonic_pf_per_kw"].severity == Severity.MAJOR
    assert by_name["pf_per_kw_in_band"].severity == Severity.MAJOR
    assert by_name["launch_cost_non_increasing"].severity == Severity.MINOR
    assert by_name["revenue_above_cost_per_node"].severity == Severity.CRITICAL
    assert by_name["cost_annual_per_node_in_band"].severity == Severity.MAJOR
    assert by_name["data_dictionary_populated"].severity == Severity.MAJOR
    # V11-V17 — all MAJOR (cycle-2 consistency / cross-check rules).
    assert by_name["no_legacy_r_scalar"].severity == Severity.MAJOR
    assert by_name["operator_r_consistency"].severity == Severity.MAJOR
    assert by_name["provenance_formula_keys"].severity == Severity.MAJOR
    assert by_name["cadence_monotonicity"].severity == Severity.MAJOR
    assert by_name["volume_fits_horizon"].severity == Severity.MAJOR
    assert by_name["fleet_cliff_consistency"].severity == Severity.MAJOR
    assert by_name["radiator_dial_matches_architecture"].severity == Severity.MAJOR


# ---------------------------------------------------------------------------
# V1 — mass_utilization_in_band
# ---------------------------------------------------------------------------


def test_v1_default_scenario_passes(default_output: ValuationOutput) -> None:
    """Default-scenario mass utilisation is tight in every year."""
    check = check_mass_utilization_in_band(default_output)
    assert check.pass_check
    assert check.severity == Severity.CRITICAL


def test_v1_trips_when_mass_util_below_floor(default_output: ValuationOutput) -> None:
    """A year with mass_utilization_pct = 50 trips V1."""
    mutated = _mutate_physical(default_output, "2029", "mass_utilization_pct", 50.0)
    assert not check_mass_utilization_in_band(mutated).pass_check


def test_v1_trips_when_mass_util_above_ceiling(default_output: ValuationOutput) -> None:
    """A year with mass_utilization_pct = 105 trips V1."""
    mutated = _mutate_physical(default_output, "2026", "mass_utilization_pct", 105.0)
    assert not check_mass_utilization_in_band(mutated).pass_check


def test_v1_band_constants() -> None:
    """V1 band is [85, 100] percent."""
    assert MASS_UTIL_MIN_PCT == 85.0
    assert MASS_UTIL_MAX_PCT == 100.0


# ---------------------------------------------------------------------------
# V2 — no_trillion_dollar_pkg
# ---------------------------------------------------------------------------


def test_v2_default_scenario_passes(default_output: ValuationOutput) -> None:
    """Every generation's $/pkg is well under the V2 ceiling."""
    check = check_no_trillion_dollar_pkg(default_output)
    assert check.pass_check
    assert check.severity == Severity.CRITICAL


def test_v2_trips_when_usd_per_pkg_above_ceiling() -> None:
    """A scenario with usd_per_pkg = 10_000_000 trips V2."""
    cfg = config_from_dict(
        {
            "generations": [
                {
                    "name": "MoonPriceGen",
                    "year_available": 2026.0,
                    "usd_per_pkg": 10_000_000,
                    "kw_per_pkg": 2.0,
                    "kg_per_pkg": 18.0,
                    "pf_per_pkg": 15.0,
                    "die_count": 2,
                    "source": {
                        "doc_path": "tests/test_validation.py",
                        "sourcing": "estimate",
                    },
                }
            ]
        }
    )
    check = check_no_trillion_dollar_pkg(run_valuation(cfg))
    assert not check.pass_check
    assert "MoonPriceGen" in check.computed


def test_v2_usd_per_pkg_max_constant() -> None:
    """V2 ceiling is $5M / pkg."""
    assert USD_PER_PKG_MAX == 5_000_000


# ---------------------------------------------------------------------------
# V3 — positive_margin_floor
# ---------------------------------------------------------------------------


def test_v3_default_scenario_passes(default_output: ValuationOutput) -> None:
    """Default active-fleet central margin stays above the 25% floor."""
    check = check_positive_margin_floor(default_output)
    assert check.pass_check
    assert check.severity == Severity.CRITICAL


def test_v3_trips_when_margin_negative(default_output: ValuationOutput) -> None:
    """An active year below the margin floor trips V3."""
    mutated = _mutate_business(default_output, "2030", "margin_central_pct", 24.0)
    assert not check_positive_margin_floor(mutated).pass_check


# ---------------------------------------------------------------------------
# V4 — gpu_count_positive
# ---------------------------------------------------------------------------


def test_v4_default_scenario_passes(default_output: ValuationOutput) -> None:
    """Default scenario fits many packages every year."""
    check = check_gpu_count_positive(default_output)
    assert check.pass_check
    assert check.severity == Severity.CRITICAL


def test_v4_trips_when_no_packages_fit() -> None:
    """An absurd mass envelope floors N to 0 every year and trips V4."""
    cfg = config_from_dict({"gospel": {"mass_envelope_t": 2.55, "node_mass_fixed_t": 2.5}})
    assert not check_gpu_count_positive(run_valuation(cfg)).pass_check


# ---------------------------------------------------------------------------
# V5 — monotonic_pf_per_kw (re-targeted from compute_share)
# ---------------------------------------------------------------------------


def test_v5_default_scenario_passes(default_output: ValuationOutput) -> None:
    """PF/kW is near-monotonic up on the default trajectory."""
    check = check_monotonic_pf_per_kw(default_output)
    assert check.pass_check
    assert check.severity == Severity.MAJOR


def test_v5_trips_when_pf_per_kw_drops_sharply(default_output: ValuationOutput) -> None:
    """A sharp PF/kW drop year-over-year trips V5."""
    # Drop the last year's PF/kW well below the prior year's.
    mutated = _mutate_physical(default_output, _last_fy(default_output), "pf_per_kw", 1.0)
    assert not check_monotonic_pf_per_kw(mutated).pass_check


# ---------------------------------------------------------------------------
# V6 — pf_per_kw_in_band
# ---------------------------------------------------------------------------


def test_v6_default_scenario_passes(default_output: ValuationOutput) -> None:
    """Default last-year PF/kW lies inside [20, 80]."""
    check = check_pf_per_kw_in_band(default_output)
    assert check.pass_check
    assert check.severity == Severity.MAJOR


def test_v6_trips_when_last_year_pf_per_kw_below_band(
    default_output: ValuationOutput,
) -> None:
    """A last-year PF/kW = 10 trips V6 (below the 20-floor)."""
    mutated = _mutate_physical(default_output, _last_fy(default_output), "pf_per_kw", 10.0)
    assert not check_pf_per_kw_in_band(mutated).pass_check


def test_v6_trips_when_last_year_pf_per_kw_above_band(
    default_output: ValuationOutput,
) -> None:
    """A last-year PF/kW = 200 trips V6 (above the 80-ceiling)."""
    mutated = _mutate_physical(default_output, _last_fy(default_output), "pf_per_kw", 200.0)
    assert not check_pf_per_kw_in_band(mutated).pass_check


def test_v6_band_constants() -> None:
    """V6 band is [20, 80] PFLOPS/kW."""
    assert PF_PER_KW_MIN == 20.0
    assert PF_PER_KW_MAX == 80.0


# ---------------------------------------------------------------------------
# V7 — launch_cost_non_increasing
# ---------------------------------------------------------------------------


def test_v7_default_scenario_passes(default_output: ValuationOutput) -> None:
    """Default scenario's launch cost ramps down monotonically."""
    check = check_launch_cost_non_increasing(default_output)
    assert check.pass_check
    assert check.severity == Severity.MINOR


def test_v7_trips_when_launch_cost_jumps_up(default_output: ValuationOutput) -> None:
    """A year-on-year jump up in launch cost trips V7."""
    # Drop an early year's launch cost low so the next transition is a jump up.
    mutated = _mutate_business(default_output, "2029", "launch_cost_this_year_musd", 1.0)
    assert not check_launch_cost_non_increasing(mutated).pass_check


# ---------------------------------------------------------------------------
# V8 — revenue_above_cost_per_node (re-pathed from per-pkg)
# ---------------------------------------------------------------------------


def test_v8_default_scenario_passes(default_output: ValuationOutput) -> None:
    """Default R band > 1 → per-node central revenue > annual cost every year."""
    check = check_revenue_above_cost_per_node(default_output)
    assert check.pass_check
    assert check.severity == Severity.CRITICAL


def test_v8_trips_when_revenue_below_cost(default_output: ValuationOutput) -> None:
    """A year whose central revenue falls below its annual cost trips V8."""
    mutated = _mutate_physical(default_output, "2031", "revenue_annual_per_node_musd_central", 0.1)
    assert not check_revenue_above_cost_per_node(mutated).pass_check


# ---------------------------------------------------------------------------
# V9 — cost_annual_per_node_in_band (re-pathed from node_total)
# ---------------------------------------------------------------------------


def test_v9_default_scenario_passes(default_output: ValuationOutput) -> None:
    """Default-scenario per-node annual cost sits in [5, 60] every year."""
    check = check_cost_annual_per_node_in_band(default_output)
    assert check.pass_check
    assert check.severity == Severity.MAJOR


def test_v9_trips_when_cost_too_high(default_output: ValuationOutput) -> None:
    """A per-node annual cost of $500M trips V9."""
    mutated = _mutate_physical(default_output, "2028", "cost_annual_per_node_musd", 500.0)
    assert not check_cost_annual_per_node_in_band(mutated).pass_check


def test_v9_trips_when_cost_too_low(default_output: ValuationOutput) -> None:
    """A per-node annual cost of $1M trips V9 (below floor)."""
    mutated = _mutate_physical(default_output, "2028", "cost_annual_per_node_musd", 1.0)
    assert not check_cost_annual_per_node_in_band(mutated).pass_check


def test_v9_band_constants() -> None:
    """V9 band is [5, 60] $M for the annualized per-node cost."""
    assert COST_ANNUAL_MIN_MUSD == 5.0
    assert COST_ANNUAL_MAX_MUSD == 60.0


# ---------------------------------------------------------------------------
# V10 — data_dictionary_populated (re-targeted from decisions_populated)
# ---------------------------------------------------------------------------


def test_v10_default_scenario_passes(default_output: ValuationOutput) -> None:
    """The engine populates a substantial data dictionary."""
    check = check_data_dictionary_populated(default_output)
    assert check.pass_check
    assert check.severity == Severity.MAJOR


def test_v10_trips_when_data_dictionary_empty(default_output: ValuationOutput) -> None:
    """An empty data dictionary trips V10."""
    empty_meta = default_output.meta.model_copy(update={"data_dictionary": {}})
    mutated = default_output.model_copy(update={"meta": empty_meta})
    assert not check_data_dictionary_populated(mutated).pass_check


# ---------------------------------------------------------------------------
# V11 — no_legacy_r_scalar
# ---------------------------------------------------------------------------


def test_v11_default_scenario_passes(default_output: ValuationOutput) -> None:
    """The default v8 inputs carry no legacy scalar R field."""
    check = check_no_legacy_r_scalar(default_output)
    assert check.pass_check
    assert check.severity == Severity.MAJOR


def test_v11_trips_when_r_revenue_cost_readded(
    default_output: ValuationOutput,
) -> None:
    """A scenario that re-adds the legacy `r_revenue_cost` field trips V11."""
    mutated = _mutate_gospel(default_output, LEGACY_R_SCALAR_FIELD, 1.5)
    check = check_no_legacy_r_scalar(mutated)
    assert not check.pass_check
    assert LEGACY_R_SCALAR_FIELD in check.computed


def test_v11_trips_when_bare_r_scalar_present(
    default_output: ValuationOutput,
) -> None:
    """A bare `r` scalar leaking into the gospel block also trips V11."""
    mutated = _mutate_gospel(default_output, "r", 1.4)
    assert not check_no_legacy_r_scalar(mutated).pass_check


# ---------------------------------------------------------------------------
# V12 — operator_r_consistency
# ---------------------------------------------------------------------------


def test_v12_default_scenario_passes(default_output: ValuationOutput) -> None:
    """The default B2B run starts central R at 1.50 — above the 1.40 floor."""
    check = check_operator_r_consistency(default_output)
    assert check.pass_check
    assert check.severity == Severity.MAJOR


def test_v12_trips_when_b2b_central_r_below_floor() -> None:
    """A B2B scenario whose central R starts below 1.40 trips V12."""
    cfg = config_from_dict(
        {
            "metadata": {"base_year": 2026, "horizon_years": 10},
            "r_band": {
                "central": [
                    {"fy": 2026, "r": 1.25},
                    {"fy": 2036, "r": 1.20},
                ]
            },
        }
    )
    check = check_operator_r_consistency(run_valuation(cfg))
    assert not check.pass_check
    assert "1.25" in check.computed


def test_v12_passes_when_b2b_central_r_exactly_at_floor() -> None:
    """A B2B scenario whose central R starts exactly at 1.40 passes V12."""
    cfg = config_from_dict(
        {
            "metadata": {"base_year": 2026, "horizon_years": 10},
            "r_band": {
                "central": [
                    {"fy": 2026, "r": B2B_R_CENTRAL_FLOOR},
                    {"fy": 2036, "r": 1.40},
                ]
            },
        }
    )
    assert check_operator_r_consistency(run_valuation(cfg)).pass_check


# ---------------------------------------------------------------------------
# V13 — provenance_formula_keys
# ---------------------------------------------------------------------------


def test_v13_default_scenario_passes(default_output: ValuationOutput) -> None:
    """Every ProvenanceCell in the default output references a known formula."""
    check = check_provenance_formula_keys(default_output)
    assert check.pass_check
    assert check.severity == Severity.MAJOR


def test_v13_trips_on_unknown_formula_name(default_output: ValuationOutput) -> None:
    """A cell whose formula_name is absent from FORMULAS trips V13."""
    mutated = _mutate_physical_cell_attr(
        default_output, "2030", "kw_per_node", "formula_name", "totally_made_up_formula"
    )
    check = check_provenance_formula_keys(mutated)
    assert not check.pass_check
    assert "totally_made_up_formula" in check.computed


def test_v13_counts_every_cell(default_output: ValuationOutput) -> None:
    """V13's computed string reports the number of cells walked."""
    check = check_provenance_formula_keys(default_output)
    # 11 years x (25 physical + 23 business) cells = 528. Physical has 25:
    # the 19 standalone per-node cells (17 original + solar_area_per_pkg_m2
    # + volume_per_pkg_m3) plus the 6-cell cost_breakdown sub-object.
    assert "528 cells" in check.computed


# ---------------------------------------------------------------------------
# V14 — cadence_monotonicity
# ---------------------------------------------------------------------------


def test_v14_default_scenario_passes(default_output: ValuationOutput) -> None:
    """Default-scenario launches ramp up monotonically within the ceiling."""
    check = check_cadence_monotonicity(default_output)
    assert check.pass_check
    assert check.severity == Severity.MAJOR


def test_v14_trips_when_launches_dip(default_output: ValuationOutput) -> None:
    """A year-over-year dip in launches trips V14."""
    # Force an early year's launches high so the next transition is a drop.
    mutated = _mutate_business(default_output, "2027", "launches", 999.0)
    assert not check_cadence_monotonicity(mutated).pass_check


def test_v14_trips_when_launches_are_fractional(default_output: ValuationOutput) -> None:
    """A fractional launch count means a raw cadence rate leaked into output."""
    mutated = _mutate_business(default_output, "2027", "launches", 2.5)
    check = check_cadence_monotonicity(mutated)
    assert not check.pass_check
    assert "fractional" in check.computed


def test_v14_trips_when_nodes_do_not_match_launches(default_output: ValuationOutput) -> None:
    """One launch deploys one node in this model; the public counts must match."""
    mutated = _mutate_business(default_output, "2027", "nodes_deployed_this_year", 3)
    check = check_cadence_monotonicity(mutated)
    assert not check.pass_check
    assert "mismatches" in check.computed


def test_v14_trips_when_launches_exceed_ceiling(
    default_output: ValuationOutput,
) -> None:
    """A year whose launches exceed the cadence ceiling trips V14."""
    # The last year is the cadence peak; pushing it past the 150 ceiling
    # keeps the series non-decreasing but busts the ceiling clause.
    mutated = _mutate_business(default_output, _last_fy(default_output), "launches", 5000.0)
    assert not check_cadence_monotonicity(mutated).pass_check


# ---------------------------------------------------------------------------
# V15 — volume_fits_horizon
# ---------------------------------------------------------------------------


def test_v15_default_scenario_passes(default_output: ValuationOutput) -> None:
    """No default-scenario year is volume-only-bound (D6 — mass binds)."""
    check = check_volume_fits_horizon(default_output)
    assert check.pass_check
    assert check.severity == Severity.MAJOR


def test_v15_trips_when_a_year_is_volume_only_bound(
    default_output: ValuationOutput,
) -> None:
    """A year whose binding_constraint is sole 'volume' trips V15."""
    mutated = _mutate_physical(default_output, "2031", "binding_constraint", "volume")
    check = check_volume_fits_horizon(mutated)
    assert not check.pass_check
    assert "2031" in check.computed


def test_v15_passes_for_both_and_neither(default_output: ValuationOutput) -> None:
    """'both' and 'neither' bindings are accepted — only sole 'volume' fails."""
    once = _mutate_physical(default_output, "2030", "binding_constraint", "both")
    twice = _mutate_physical(once, "2031", "binding_constraint", "neither")
    assert check_volume_fits_horizon(twice).pass_check


# ---------------------------------------------------------------------------
# V16 — fleet_cliff_consistency
# ---------------------------------------------------------------------------


def test_v16_default_scenario_passes(default_output: ValuationOutput) -> None:
    """Default-scenario living_fleet matches the cohort-cliff sum every year."""
    check = check_fleet_cliff_consistency(default_output)
    assert check.pass_check
    assert check.severity == Severity.MAJOR


def test_v16_trips_when_living_fleet_inconsistent(
    default_output: ValuationOutput,
) -> None:
    """A living_fleet value that breaks the cliff arithmetic trips V16."""
    mutated = _mutate_business(default_output, "2032", "living_fleet", 9999)
    check = check_fleet_cliff_consistency(mutated)
    assert not check.pass_check
    assert "2032" in check.computed


# ---------------------------------------------------------------------------
# V17 — radiator_dial_matches_architecture
# ---------------------------------------------------------------------------


def _force_co_mounted(output: ValuationOutput) -> ValuationOutput:
    """Return a copy with the co-mounted architecture (to exercise V17's floor)."""
    new_md = output.metadata.model_copy(
        update={"radiator_architecture": RadiatorArchitecture.SINGLE_FACE_CO_MOUNTED}
    )
    return output.model_copy(update={"metadata": new_md})


def test_v17_default_scenario_passes(default_output: ValuationOutput) -> None:
    """The deployed double-sided default takes V17's not-applicable pass path."""
    check = check_radiator_dial_arch_consistency(default_output)
    assert check.pass_check
    assert check.severity == Severity.MAJOR
    assert "not applicable" in check.computed


def test_v17_trips_when_radiator_dial_below_floor(
    default_output: ValuationOutput,
) -> None:
    """A co-mounted run with radiator_t_per_kw_post below 0.010 trips V17."""
    mutated = _force_co_mounted(_mutate_gospel(default_output, "radiator_t_per_kw_post", 0.005))
    check = check_radiator_dial_arch_consistency(mutated)
    assert not check.pass_check
    assert "0.005" in check.computed


def test_v17_passes_at_exact_floor(default_output: ValuationOutput) -> None:
    """A co-mounted radiator dial exactly at the 0.010 floor passes V17."""
    mutated = _force_co_mounted(
        _mutate_gospel(default_output, "radiator_t_per_kw_post", RADIATOR_T_PER_KW_CO_MOUNTED_MIN)
    )
    assert check_radiator_dial_arch_consistency(mutated).pass_check


# ---------------------------------------------------------------------------
# Aggregator on a multi-rule trip
# ---------------------------------------------------------------------------


def test_aggregator_surfaces_multiple_concurrent_failures(
    default_output: ValuationOutput,
) -> None:
    """Trip V1 and V9 simultaneously — both surface in the aggregated list."""
    once = _mutate_physical(default_output, "2028", "mass_utilization_pct", 10.0)
    twice = _mutate_physical(once, "2028", "cost_annual_per_node_musd", 500.0)
    failing = {c.name for c in compute_validation(twice) if not c.pass_check}
    assert "mass_utilization_in_band" in failing
    assert "cost_annual_per_node_in_band" in failing


# ---------------------------------------------------------------------------
# Computed-message readability
# ---------------------------------------------------------------------------


def test_every_check_emits_non_empty_computed_string(
    default_output: ValuationOutput,
) -> None:
    """`computed` is a reader-facing string — no rule may leave it blank."""
    blanks = [c.name for c in compute_validation(default_output) if not c.computed.strip()]
    assert not blanks, f"checks with empty 'computed': {blanks}"


def test_every_check_emits_known_severity(default_output: ValuationOutput) -> None:
    """Severity is a known string-enum value."""
    for c in compute_validation(default_output):
        assert c.severity in {Severity.CRITICAL, Severity.MAJOR, Severity.MINOR}


def test_physical_year_has_expected_cell_fields() -> None:
    """Sanity: the V-rules read PhysicalYear cell fields that exist."""
    fields = set(PhysicalYear.model_fields.keys())
    for needed in (
        "mass_utilization_pct",
        "gpus_per_node",
        "pf_per_kw",
        "cost_annual_per_node_musd",
        "revenue_annual_per_node_musd_central",
    ):
        assert needed in fields
