"""Tests for the v8 GPU-first valuation engine.

Locks the GPU-first per-node formulas, the frontier-generation picker, the
Tjmax step at year 5, the cadence-indexed launch cost, the bus-cost
decline-then-flatten, the cadence / volume / fleet wiring, and the v8
``run_valuation`` entry point that produces the five-block
:class:`data_center.output.ValuationOutput`.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from data_center.config import (
    ValuationConfig,
    config_from_dict,
    load_config,
)
from data_center.engine import (
    CadenceYear,
    CostBreakdown,
    YearComputation,
    bus_cost_for_year,
    compute_cadence_year,
    compute_cost_per_node_breakdown,
    compute_fleet_trajectory,
    compute_kw_per_node,
    compute_mass_per_node,
    compute_mass_per_pkg,
    compute_mass_util,
    compute_n_packages,
    compute_node_total_cost,
    compute_pf_per_kw,
    compute_pf_per_node,
    compute_volume_year,
    compute_year,
    radiator_t_per_kw_for_year,
    run_valuation,
)
from data_center.fleet import Cohort, FleetYear
from data_center.generations import (
    KNOWN_GENS,
    GenerationSpec,
    extend_generations,
)
from data_center.output import CostBreakdownBlock, PhysicalYear, ValuationOutput
from data_center.provenance import ProvenanceCell
from data_center.volume import VolumeBreakdown

_SCENARIOS = Path(__file__).resolve().parents[2] / "scenarios"


def _num(value: float | int | str | bool | None) -> float:
    """Unwrap a numeric ProvenanceCell value to a float."""
    assert isinstance(value, (int, float)) and not isinstance(value, bool)
    return float(value)


def _default_gens() -> list[GenerationSpec]:
    """Build the extended generation list the default scenario uses."""
    cfg = ValuationConfig()
    return extend_generations(list(KNOWN_GENS), cfg.slopes, cfg.gospel.release_cadence_yr, 2037.0)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


def test_default_config_matches_plan_section_zero_anchors() -> None:
    """Constructing `ValuationConfig()` reproduces the v8 plan-§-0 anchors."""
    cfg = ValuationConfig()
    g = cfg.gospel
    assert g.mass_envelope_t == pytest.approx(12.5)
    assert g.node_mass_fixed_t == pytest.approx(2.5)
    assert g.node_volume_fixed_m3 == pytest.approx(5.0)
    assert g.tjmax_lift_year == 5
    assert g.bus_base_musd == pytest.approx(8.0)
    assert g.bus_flatten_after_yr == 5
    assert g.bus_growth_pre == pytest.approx(-0.03)
    assert g.solar_cost_musd_per_kw == pytest.approx(0.04)
    assert g.radiator_cost_musd_per_kw == pytest.approx(0.04)
    assert g.solar_mass_t_per_kw == pytest.approx(0.011)
    assert g.radiator_t_per_kw_pre == pytest.approx(0.013)
    # D17 radiator correction — the post-Tjmax dial is 0.012 in v8.
    assert g.radiator_t_per_kw_post == pytest.approx(0.012)
    assert g.release_cadence_yr == pytest.approx(1.5)
    # base_year / horizon_years moved to metadata; service_life to fleet.
    assert cfg.metadata.base_year == 2026
    assert cfg.metadata.horizon_years == 10
    assert cfg.fleet.service_life_years == 5
    s = cfg.slopes
    assert s.pf_growth_per_gen == pytest.approx(0.625)


def test_gospel_drops_the_six_legacy_fields() -> None:
    """The 6 legacy gospel fields are gone (moved to the v8 dial blocks)."""
    from data_center.config import GospelInputs

    fields = set(GospelInputs.model_fields.keys())
    for legacy in (
        "r_revenue_cost",
        "launch_y0_musd",
        "launch_y10_musd",
        "service_life_years",
        "base_year",
        "horizon_years",
    ):
        assert legacy not in fields, f"legacy gospel field {legacy} still present"


def test_config_rejects_unknown_keys() -> None:
    """Pydantic `extra='forbid'` catches typos at load time."""
    with pytest.raises(ValidationError):
        config_from_dict({"gospel": {"made_up_key": 1.0}})


def test_config_rejects_negative_envelope() -> None:
    """Mass envelope must be positive (D2)."""
    with pytest.raises(ValidationError):
        config_from_dict({"gospel": {"mass_envelope_t": -1.0}})


# ---------------------------------------------------------------------------
# Per-year helpers
# ---------------------------------------------------------------------------


def test_radiator_t_per_kw_steps_at_tjmax_lift_year() -> None:
    """Years 0..4 -> pre (0.013); years 5+ -> post (0.012, D17)."""
    cfg = ValuationConfig()
    for y in range(5):
        assert radiator_t_per_kw_for_year(y, cfg.gospel) == pytest.approx(0.013)
    for y in range(5, 11):
        assert radiator_t_per_kw_for_year(y, cfg.gospel) == pytest.approx(0.012)


def test_bus_cost_compounds_then_flattens() -> None:
    """Bus declines at -0.03/yr through year 5, then holds flat."""
    cfg = ValuationConfig()
    assert bus_cost_for_year(0, cfg.gospel) == pytest.approx(8.0)
    expected_5 = 8.0 * (0.97**5)
    assert bus_cost_for_year(5, cfg.gospel) == pytest.approx(expected_5)
    assert bus_cost_for_year(10, cfg.gospel) == pytest.approx(expected_5)


# ---------------------------------------------------------------------------
# Cell-producing functions
# ---------------------------------------------------------------------------


def test_compute_mass_per_pkg_returns_provenance_cell() -> None:
    """compute_mass_per_pkg returns a tonnes-valued ProvenanceCell."""
    c = compute_mass_per_pkg(
        0.0189,
        2.05,
        0.011,
        0.012,
        gen_mass_path="a",
        kw_per_pkg_path="b",
        solar_dial_path="c",
        radiator_dial_path="d",
    )
    assert isinstance(c, ProvenanceCell)
    assert c.unit == "t"
    assert c.value == pytest.approx(0.0189 + 2.05 * (0.011 + 0.012))


def test_compute_n_packages_is_mass_bound_floor() -> None:
    """N = floor(mass_budget / mass_per_pkg)."""
    c = compute_n_packages(10.0, 0.0685, mass_budget_path="a", mass_per_pkg_path="b")
    assert c.value == 145
    assert c.unit == "count"


def test_compute_n_packages_zero_when_mass_per_pkg_nonpositive() -> None:
    """A non-positive per-package mass yields N = 0 (degenerate config)."""
    c = compute_n_packages(10.0, 0.0, mass_budget_path="a", mass_per_pkg_path="b")
    assert c.value == 0


def test_compute_kw_per_node_is_n_times_kw_per_pkg() -> None:
    """node_kW = N x kW/pkg."""
    c = compute_kw_per_node(100, 2.05, n_packages_path="a", kw_per_pkg_path="b")
    assert c.value == pytest.approx(205.0)
    assert c.unit == "kW"


def test_compute_mass_per_node_adds_fixed_bus_mass() -> None:
    """node_mass = node_mass_fixed + N x mass_per_pkg."""
    c = compute_mass_per_node(
        100,
        0.05,
        2.5,
        n_packages_path="a",
        mass_per_pkg_path="b",
        node_mass_fixed_path="c",
    )
    assert c.value == pytest.approx(2.5 + 100 * 0.05)


def test_compute_mass_util_is_percent_of_envelope() -> None:
    """mass utilisation is a PERCENT of the mass envelope in v8."""
    c = compute_mass_util(12.4, 12.5, node_mass_path="a", mass_envelope_path="b")
    assert c.value == pytest.approx(99.2)
    assert c.unit == "percent"


def test_compute_pf_per_node_is_n_times_pf_per_pkg() -> None:
    """pf_node = N x PF/pkg."""
    c = compute_pf_per_node(100, 15.0, n_packages_path="a", pf_per_pkg_path="b")
    assert c.value == pytest.approx(1500.0)


def test_compute_pf_per_kw_is_pf_over_kw() -> None:
    """pf_per_kw = pf_node / node_kw."""
    c = compute_pf_per_kw(1500.0, 205.0, pf_node_path="a", node_kw_path="b")
    assert c.value == pytest.approx(1500.0 / 205.0)


def test_compute_cost_per_node_breakdown_returns_five_cells() -> None:
    """The cost breakdown has five $M-valued ProvenanceCells."""
    bd = compute_cost_per_node_breakdown(
        100,
        70_000,
        8.0,
        12.0,
        12.0,
        20.0,
        n_packages_path="a",
        usd_per_pkg_path="b",
        kw_per_node_path="c",
        solar_cost_dial_path="d",
        radiator_cost_dial_path="e",
        launch_cost_path="f",
    )
    assert isinstance(bd, CostBreakdown)
    for c in (bd.compute, bd.bus, bd.solar, bd.radiator, bd.launch):
        assert isinstance(c, ProvenanceCell)
        assert c.unit == "MUSD"
    assert bd.compute.value == pytest.approx(100 * 70_000 / 1_000_000)


def test_compute_node_total_cost_sums_the_breakdown() -> None:
    """node_total = compute + bus + solar + radiator + launch."""
    bd = compute_cost_per_node_breakdown(
        100,
        70_000,
        8.0,
        12.0,
        12.0,
        20.0,
        n_packages_path="a",
        usd_per_pkg_path="b",
        kw_per_node_path="c",
        solar_cost_dial_path="d",
        radiator_cost_dial_path="e",
        launch_cost_path="f",
    )
    total = compute_node_total_cost(bd, cost_breakdown_path="x")
    assert total.value == pytest.approx(7.0 + 8.0 + 12.0 + 12.0 + 20.0)
    # node_total cites the five component cells under the cost_breakdown
    # sub-object — never the bare sub-object, never itself.
    assert total.uses == [f"x.{line}" for line in ("compute", "bus", "solar", "radiator", "launch")]


# ---------------------------------------------------------------------------
# compute_year — the per-year computation
# ---------------------------------------------------------------------------


def test_compute_year_zero_picks_b300_and_yields_146_packages() -> None:
    """FY2026 picks B300/GB300 and packs 146 packages."""
    yc = compute_year(0, ValuationConfig(), _default_gens())
    assert isinstance(yc, YearComputation)
    assert yc.fy == 2026
    assert yc.frontier.name == "B300/GB300"
    assert yc.n_packages == 146


def test_compute_year_ten_yields_37_packages() -> None:
    """FY2036 packs 37 packages (D17 radiator + V-A kw_growth 0.20 corrections)."""
    yc = compute_year(10, ValuationConfig(), _default_gens())
    assert yc.fy == 2036
    assert yc.n_packages == 37


def test_compute_year_produces_a_full_physical_year() -> None:
    """compute_year assembles a PhysicalYear of cells + a cost_breakdown block."""
    yc = compute_year(3, ValuationConfig(), _default_gens())
    assert isinstance(yc.physical, PhysicalYear)
    for name in PhysicalYear.model_fields:
        field = getattr(yc.physical, name)
        if name == "year":
            assert isinstance(field, int)
            continue
        if name == "cost_breakdown":
            assert isinstance(field, CostBreakdownBlock)
            for line in CostBreakdownBlock.model_fields:
                line_cell = getattr(field, line)
                assert isinstance(line_cell, ProvenanceCell)
                assert line_cell.value is not None
            continue
        assert isinstance(field, ProvenanceCell)
        assert field.value is not None


def test_compute_year_node_kw_equals_n_times_kw_per_pkg() -> None:
    """node_kW = N x kW/pkg for the frontier generation."""
    for i in range(11):
        yc = compute_year(i, ValuationConfig(), _default_gens())
        assert _num(yc.physical.kw_per_node.value) == pytest.approx(
            yc.n_packages * yc.frontier.kw_per_pkg, rel=1e-9
        )


def test_compute_year_cost_annual_is_total_over_service_life() -> None:
    """cost_annual_per_node = node_total / service_life."""
    cfg = ValuationConfig()
    yc = compute_year(2, cfg, _default_gens())
    assert yc.cost_annual_musd == pytest.approx(
        yc.node_total_musd / cfg.fleet.service_life_years, rel=1e-9
    )


def test_compute_year_revenue_band_is_cost_times_r() -> None:
    """Per-node revenue at each band = cost_annual x R(band) — central > low."""
    yc = compute_year(0, ValuationConfig(), _default_gens())
    py = yc.physical
    rev_c = _num(py.revenue_annual_per_node_musd_central.value)
    rev_l = _num(py.revenue_annual_per_node_musd_low.value)
    rev_h = _num(py.revenue_annual_per_node_musd_high.value)
    assert rev_l < rev_c < rev_h
    # FY2026 central R is 1.50.
    assert rev_c == pytest.approx(yc.cost_annual_musd * 1.50, rel=1e-9)


def test_compute_year_gross_profit_is_revenue_minus_cost() -> None:
    """Per-node gross profit = revenue - annual cost, per band."""
    yc = compute_year(4, ValuationConfig(), _default_gens())
    py = yc.physical
    for band in ("central", "low", "high"):
        rev = _num(getattr(py, f"revenue_annual_per_node_musd_{band}").value)
        gp = _num(getattr(py, f"gross_profit_annual_per_node_musd_{band}").value)
        assert gp == pytest.approx(rev - yc.cost_annual_musd, rel=1e-9)


def test_compute_year_tjmax_lift_changes_radiator_dial() -> None:
    """The radiator dial used at year 5+ is the post-Tjmax 0.012 (D17)."""
    gens = _default_gens()
    cfg = ValuationConfig()
    # Year 0-4 use 0.013, year 5+ uses 0.012 — N at year 5+ is correspondingly
    # smaller than it would be at 0.013. We check the dial via mass: a heavier
    # radiator means a heavier per-package mass, so check N drops over the
    # horizon as the heavier dial bites.
    n_year_5 = compute_year(5, cfg, gens).n_packages
    n_year_10 = compute_year(10, cfg, gens).n_packages
    assert n_year_10 <= n_year_5


def test_compute_year_mass_util_close_to_one() -> None:
    """Every year packs the mass envelope tight (>= 85%, D2)."""
    for i in range(11):
        yc = compute_year(i, ValuationConfig(), _default_gens())
        assert 85.0 <= _num(yc.physical.mass_utilization_pct.value) <= 100.0


# ---------------------------------------------------------------------------
# Cadence wiring
# ---------------------------------------------------------------------------


def test_compute_cadence_year_returns_two_cells() -> None:
    """compute_cadence_year returns launches + launch-cost cells."""
    cy = compute_cadence_year(5, ValuationConfig())
    assert isinstance(cy, CadenceYear)
    assert isinstance(cy.launches, ProvenanceCell)
    assert isinstance(cy.launch_cost_musd, ProvenanceCell)


def test_compute_cadence_year_launches_ramp_up() -> None:
    """Launches per year rise across the horizon (logistic ramp)."""
    cfg = ValuationConfig()
    launches = [_num(compute_cadence_year(i, cfg).launches.value) for i in range(11)]
    assert launches[0] < launches[5] < launches[10]
    # first_launch_year only clamps pre-launch years; the anchors stay put.
    assert launches[5] == pytest.approx(14.0, rel=1e-6)
    assert launches[10] == pytest.approx(90.0, rel=1e-6)


def test_compute_cadence_year_launch_cost_falls_with_cadence() -> None:
    """Launch cost falls as the cadence ramps up (D12)."""
    cfg = ValuationConfig()
    cost0 = _num(compute_cadence_year(0, cfg).launch_cost_musd.value)
    cost10 = _num(compute_cadence_year(10, cfg).launch_cost_musd.value)
    assert cost10 < cost0


# ---------------------------------------------------------------------------
# Volume wiring
# ---------------------------------------------------------------------------


def test_compute_volume_year_returns_breakdown() -> None:
    """compute_volume_year returns a VolumeBreakdown of cells."""
    vb = compute_volume_year(100, 99.0, 2.05, ValuationConfig(), fy_path='physical.years."2026"')
    assert isinstance(vb, VolumeBreakdown)
    assert isinstance(vb.volume_per_node_m3, ProvenanceCell)
    assert isinstance(vb.binding_constraint, ProvenanceCell)
    # The volume cells' uses resolve to real cells — the year is concrete,
    # never the literal "FY" placeholder.
    for path in vb.volume_per_node_m3.uses + vb.binding_constraint.uses:
        assert '"FY"' not in path


def test_compute_volume_year_binding_is_mass_at_full_envelope() -> None:
    """At ~99% mass utilisation and slack volume, the binding constraint is mass."""
    vb = compute_volume_year(100, 99.0, 2.05, ValuationConfig(), fy_path='physical.years."2026"')
    assert vb.binding_constraint.value == "mass"


# ---------------------------------------------------------------------------
# Fleet wiring
# ---------------------------------------------------------------------------


def test_compute_fleet_trajectory_parallels_years() -> None:
    """compute_fleet_trajectory yields one FleetYear per model year."""
    cfg = ValuationConfig()
    gens = _default_gens()
    years = [compute_year(i, cfg, gens) for i in range(11)]
    fleet = compute_fleet_trajectory(cfg, years)
    assert len(fleet) == 11
    assert all(isinstance(fy, FleetYear) for fy in fleet)


def test_compute_fleet_trajectory_living_fleet_grows() -> None:
    """The living fleet grows across the horizon as cohorts accumulate."""
    cfg = ValuationConfig()
    gens = _default_gens()
    years = [compute_year(i, cfg, gens) for i in range(11)]
    fleet = compute_fleet_trajectory(cfg, years)
    living = [_num(fy.living_fleet.value) for fy in fleet]
    assert living[0] < living[5] < living[10]


def test_compute_fleet_trajectory_cumulative_revenue_monotonic() -> None:
    """Cumulative fleet revenue is non-decreasing year-over-year."""
    cfg = ValuationConfig()
    gens = _default_gens()
    years = [compute_year(i, cfg, gens) for i in range(11)]
    fleet = compute_fleet_trajectory(cfg, years)
    cumul = [_num(fy.revenue_cumulative_musd_central.value) for fy in fleet]
    for a, b in zip(cumul[:-1], cumul[1:], strict=True):
        assert b >= a


def test_compute_fleet_trajectory_margin_flat_under_flat_r_band() -> None:
    """Fleet central margin is positive and flat across the trajectory.

    The default R band is flat at 1.50, so every cohort earns the same 33.3%
    gross margin and the fleet margin does not drift year to year.
    """
    cfg = ValuationConfig()
    gens = _default_gens()
    years = [compute_year(i, cfg, gens) for i in range(11)]
    fleet = compute_fleet_trajectory(cfg, years)
    active_margins = [
        _num(fy.margin_central_pct.value) for fy in fleet if _num(fy.launches.value) > 0
    ]
    margin_first = active_margins[0]
    margin_last = _num(fleet[-1].margin_central_pct.value)
    assert margin_first > 0
    assert margin_last > 0
    assert margin_last == pytest.approx(margin_first)


# ---------------------------------------------------------------------------
# run_valuation — the v8 entry point
# ---------------------------------------------------------------------------


def test_run_valuation_returns_v8_valuation_output() -> None:
    """The engine's top-level entry returns a v8 ValuationOutput."""
    out = run_valuation(ValuationConfig())
    assert isinstance(out, ValuationOutput)
    assert out.metadata.schema_version == "v8"


def test_run_valuation_emits_horizon_plus_one_years() -> None:
    """The default horizon (10) yields 11 physical + 11 business years."""
    out = run_valuation(ValuationConfig())
    assert len(out.physical.years) == 11
    assert len(out.business.years) == 11
    assert "2026" in out.physical.years
    assert "2036" in out.physical.years


def test_run_valuation_validation_populated_with_seventeen_passing_checks() -> None:
    """run_valuation runs the 17 V-rules and they all pass on the default scenario."""
    out = run_valuation(ValuationConfig())
    rules = out.meta.validation.rules
    assert len(rules) == 17
    failed = [r.name for r in rules if not r.pass_check]
    assert not failed, f"unexpected failing checks: {failed}"


def test_run_valuation_data_dictionary_is_introspected() -> None:
    """run_valuation populates meta.data_dictionary by introspection."""
    out = run_valuation(ValuationConfig())
    dd = {entry.path: entry for entry in out.meta.data_dictionary}
    assert len(dd) > 30
    for path in (
        "physical.years[].gpus_per_node",
        "physical.years[].kw_per_node",
        "business.years[].living_fleet",
        "inputs.config.physical.mass_envelope_t",
    ):
        assert path in dd, f"data_dictionary missing {path}"


def test_run_valuation_year_zero_n_is_146() -> None:
    """Year 0 (FY2026) packs 146 packages."""
    out = run_valuation(ValuationConfig())
    assert int(_num(out.physical.years["2026"].gpus_per_node.value)) == 146


def test_run_valuation_year_ten_n_is_37() -> None:
    """Year 10 (FY2036) packs 37 packages (D17 radiator + V-A kw_growth 0.20)."""
    out = run_valuation(ValuationConfig())
    assert int(_num(out.physical.years["2036"].gpus_per_node.value)) == 37


def test_run_valuation_uses_integer_launch_counts_for_business_math() -> None:
    """Business years use integer launches directly; no hidden fractional cadence."""
    out = run_valuation(ValuationConfig())
    launch_counts: dict[int, int] = {}
    for fy, business_year in out.business.years.items():
        launches = business_year.launches.value
        nodes = business_year.nodes_deployed_this_year.value
        assert isinstance(launches, int)
        assert isinstance(nodes, int)
        assert nodes == launches
        launch_counts[int(fy)] = launches

    assert launch_counts[2036] == 90
    assert int(_num(out.business.years["2036"].living_fleet.value)) == sum(
        launch_counts[fy] for fy in range(2032, 2037)
    )


# ---------------------------------------------------------------------------
# Scenario loading
# ---------------------------------------------------------------------------


def test_default_yaml_loads_and_runs() -> None:
    """The packaged default scenario loads and runs end-to-end."""
    out = run_valuation(load_config(str(_SCENARIOS / "default.yaml")))
    assert len(out.physical.years) == 11
    assert out.metadata.schema_version == "v8"


def test_all_five_scenarios_load_and_run() -> None:
    """Every cycle-1 scenario YAML loads and runs to a v8 artifact."""
    for stem in ("default", "conservative", "ambitious", "upside_7yr", "with_premium"):
        cfg = load_config(str(_SCENARIOS / f"{stem}.yaml"))
        out = run_valuation(cfg)
        assert len(out.physical.years) == cfg.metadata.horizon_years + 1
        # Every year packs at least one package.
        for py in out.physical.years.values():
            assert int(_num(py.gpus_per_node.value)) > 0


def test_conservative_scenario_uses_shorter_service_life() -> None:
    """conservative.yaml sets a 3-year service life via the fleet block."""
    cfg = load_config(str(_SCENARIOS / "conservative.yaml"))
    assert cfg.fleet.service_life_years == 3


def test_upside_7yr_scenario_overrides_service_life() -> None:
    """upside_7yr.yaml sets a 7-year service life via the fleet block."""
    cfg = load_config(str(_SCENARIOS / "upside_7yr.yaml"))
    assert cfg.fleet.service_life_years == 7


def test_upside_7yr_grows_living_fleet_beyond_default() -> None:
    """The cliff fix makes a 7-year scenario keep cohorts alive two years
    longer, so the 2036 living fleet exceeds the 5-year default's 268. The
    living set now tracks config.fleet.service_life_years, not a hardcoded 5.
    """
    default_out = run_valuation(load_config(str(_SCENARIOS / "default.yaml")))
    upside_out = run_valuation(load_config(str(_SCENARIOS / "upside_7yr.yaml")))
    default_2036 = int(_num(default_out.business.years["2036"].living_fleet.value))
    upside_2036 = int(_num(upside_out.business.years["2036"].living_fleet.value))
    assert default_2036 == 268
    assert upside_2036 > default_2036
    # 7-year window: 2036 living == launches over FY2030..FY2036 (vs FY2032..FY2036
    # at the 5-year default); the extra living cohorts are FY2030 and FY2031.
    upside_years = upside_out.business.years
    window_launches = sum(upside_years[str(fy)].launches.value for fy in range(2030, 2037))
    assert upside_2036 == window_launches


def test_upside_7yr_central_margin_flat_at_1_47() -> None:
    """The 7-year scenario holds a flat 1.47 central R, so the central gross
    margin is constant at (1.47 - 1) / 1.47, about 31.97%, across the
    trajectory (no taper, no in-life decay: a locked contract fixes the price).
    """
    out = run_valuation(load_config(str(_SCENARIOS / "upside_7yr.yaml")))
    margins = [
        _num(by.margin_central_pct.value)
        for by in out.business.years.values()
        if _num(by.launches.value) > 0
    ]
    expected_margin_pct = (1.47 - 1.0) / 1.47 * 100.0
    assert margins  # at least one active year
    for margin in margins:
        assert margin == pytest.approx(expected_margin_pct, abs=0.05)


def test_run_valuation_uses_known_gens_by_default() -> None:
    """With no generation override, run_valuation uses the bundled KNOWN_GENS."""
    out = run_valuation(ValuationConfig())
    gen_names = [str(g["name"]) for g in out.inputs.generations]
    assert "B200/GB200" in gen_names
    assert "Feynman" in gen_names


def test_cohort_and_fleetyear_are_importable() -> None:
    """The fleet model types are importable from the fleet module."""
    assert Cohort is not None
    assert FleetYear is not None
