"""Reference-value test — the v8 engine vs the locked golden trajectory.

Locks the production GPU-first engine
(:func:`data_center.engine.run_valuation`) against the per-year reference
values of the **v8** default-scenario trajectory.

**Cycle-2 re-freeze (Phase 4A, D17).** Cycle-1's frozen trajectory used
the pre-correction radiator dial ``radiator_t_per_kw_post = 0.007``;
cycle-2's radiator correction (D17) lifts the post-Tjmax dial to 0.012.
The trajectory below is therefore re-recorded from the v8 engine at the
corrected dial — years 0-4 are unchanged (the dial does not bite until
the Tjmax-lift year 5), years 5-10 carry a smaller package count (the
heavier radiator leaves less mass budget). "Parity" in v8 means the v8
engine reproduces these v8 numbers; a future change that drifts from them
means the engine's behaviour has changed — intentionally (re-record below
+ commit the rationale) or by regression (debug the engine, not the test).

**Cycle-2 re-freeze (validation V-A, kw_growth_per_gen 0.30 -> 0.20).**
The per-package power-growth slope was corrected from 0.30 to 0.20 (the
0.30 figure was an assembly-level rate misapplied per package — see
``sourcing_audit_05_21.md``). The slower kW slope only bites on the
extrapolated generations, so years 0-4 (FY2026-FY2030) are unchanged;
years 5-10 (FY2031-FY2036) carry lighter packages, so each node now
packs more of them. The trajectory below is re-recorded at 0.20.

**Source-consistency re-freeze (2026-05-25).** ``first_launch_year`` clamps
pre-launch years to zero without shifting the year-5/year-10 anchors, so
FY2026 has zero deployed nodes and FY2036 stays pinned to the 90-launch
anchor. The cadence output is an integer mission count. The 12.5 t default
is explicitly a block-upgrade scenario, not a published SSO payload.

**Flat-R re-freeze (2026-05-29).** The default central R band is flat at 1.50
with no taper, so each cohort earns a constant 33.3% gross margin across its
five-year life. The central-revenue reference values below are recorded from
the flat default.

The v8 output is keyed by JSON-string fiscal year in
``physical.years`` / ``business.years``; every leaf is a
:class:`data_center.provenance.ProvenanceCell`, so the test reads each
cell's ``.value``.

Tolerances:
* **integer parity** on ``gpus_per_node`` — same N every year;
* **±0.5%** on every numeric reference value.
"""

from __future__ import annotations

import pytest

from data_center.config import ValuationConfig
from data_center.engine import run_valuation
from data_center.output import ValuationOutput

# Tolerance for numeric reference (±0.5%).
TOLERANCE: float = 0.005

# The v8 default-scenario fiscal years (FY2026..FY2036, horizon 10).
REFERENCE_YEARS: tuple[str, ...] = tuple(str(fy) for fy in range(2026, 2037))


# ---------------------------------------------------------------------------
# Reference trajectory — the v8 default-scenario golden numbers, recorded
# from the v8 engine at the 2026-07-14 investor rebase: AI-1-class deployed
# double-sided radiator at 0.00165 t/kW flat (Tjmax step inert) and the
# 0.02 $M/kW solar and radiator cost dials.
# ---------------------------------------------------------------------------

REFERENCE_N_BY_YEAR: tuple[int, ...] = (
    223,  # FY2026 (B300/GB300)
    178,  # FY2027 (Rubin VR200)
    133,  # FY2028 (Rubin Ultra)
    125,  # FY2029 (Feynman)
    125,  # FY2030 (Feynman)
    108,  # FY2031 (Gen+1 extrap)
    92,  # FY2032 (Gen+2 extrap)
    92,  # FY2033 (Gen+2 extrap)
    78,  # FY2034 (Gen+3 extrap)
    66,  # FY2035 (Gen+4 extrap)
    66,  # FY2036 (Gen+4 extrap)
)

REFERENCE_FRONTIER_NAMES: tuple[str, ...] = (
    "B300/GB300",
    "Rubin VR200",
    "Rubin Ultra",
    "Feynman",
    "Feynman",
    "Gen+1(extrap)",
    "Gen+2(extrap)",
    "Gen+2(extrap)",
    "Gen+3(extrap)",
    "Gen+4(extrap)",
    "Gen+4(extrap)",
)

# Per-year per-node physical reference — (year_idx → field → value).
REFERENCE_PHYSICAL: tuple[dict[str, float], ...] = (
    {"kw_per_node": 457.150, "mass_per_node_t": 12.4976, "pf_per_node": 3345.0},
    {"kw_per_node": 462.800, "mass_per_node_t": 12.4484, "pf_per_node": 6052.0},
    {"kw_per_node": 554.610, "mass_per_node_t": 12.4418, "pf_per_node": 6916.0},
    {"kw_per_node": 687.500, "mass_per_node_t": 12.4469, "pf_per_node": 12500.0},
    {"kw_per_node": 687.500, "mass_per_node_t": 12.4469, "pf_per_node": 12500.0},
    {"kw_per_node": 712.800, "mass_per_node_t": 12.4889, "pf_per_node": 17550.0},
    {"kw_per_node": 728.640, "mass_per_node_t": 12.4625, "pf_per_node": 24293.75},
    {"kw_per_node": 728.640, "mass_per_node_t": 12.4625, "pf_per_node": 24293.75},
    {"kw_per_node": 741.312, "mass_per_node_t": 12.4462, "pf_per_node": 33469.9219},
    {"kw_per_node": 752.7168, "mass_per_node_t": 12.4549, "pf_per_node": 46021.1426},
    {"kw_per_node": 752.7168, "mass_per_node_t": 12.4549, "pf_per_node": 46021.1426},
)

# Per-year per-node annualized economics, central R band (flat 1.50x cost).
REFERENCE_NODE_ECONOMICS: tuple[dict[str, float], ...] = (
    {"cost_annual_per_node_musd": 13.37920, "revenue_annual_per_node_musd_central": 20.06880},
    {"cost_annual_per_node_musd": 12.74640, "revenue_annual_per_node_musd_central": 19.11960},
    {"cost_annual_per_node_musd": 15.73032, "revenue_annual_per_node_musd_central": 23.59548},
    {"cost_annual_per_node_musd": 17.58528, "revenue_annual_per_node_musd_central": 26.37792},
    {"cost_annual_per_node_musd": 17.09019, "revenue_annual_per_node_musd_central": 25.63529},
    {"cost_annual_per_node_musd": 17.60388, "revenue_annual_per_node_musd_central": 26.40581},
    {"cost_annual_per_node_musd": 18.06218, "revenue_annual_per_node_musd_central": 27.09327},
    {"cost_annual_per_node_musd": 17.70570, "revenue_annual_per_node_musd_central": 26.55856},
    {"cost_annual_per_node_musd": 18.23291, "revenue_annual_per_node_musd_central": 27.34936},
    {"cost_annual_per_node_musd": 18.85216, "revenue_annual_per_node_musd_central": 28.27824},
    {"cost_annual_per_node_musd": 18.65921, "revenue_annual_per_node_musd_central": 27.98882},
)

# Per-year fleet rollup reference, living fleet + central-R fleet revenue (flat).
REFERENCE_FLEET: tuple[dict[str, float], ...] = (
    {"living_fleet": 0, "revenue_annual_fleet_musd_central": 0.0000},
    {"living_fleet": 2, "revenue_annual_fleet_musd_central": 38.2392},
    {"living_fleet": 5, "revenue_annual_fleet_musd_central": 109.0256},
    {"living_fleet": 10, "revenue_annual_fleet_musd_central": 240.9152},
    {"living_fleet": 19, "revenue_annual_fleet_musd_central": 471.6328},
    {"living_fleet": 33, "revenue_annual_fleet_musd_central": 841.3142},
    {"living_fleet": 53, "revenue_annual_fleet_musd_central": 1399.1269},
    {"living_fleet": 85, "revenue_annual_fleet_musd_central": 2257.8899},
    {"living_fleet": 131, "revenue_annual_fleet_musd_central": 3520.8177},
    {"living_fleet": 192, "revenue_annual_fleet_musd_central": 5269.5769},
    {"living_fleet": 268, "revenue_annual_fleet_musd_central": 7418.8890},
)


def _within_tolerance(a: float, b: float, tol: float = TOLERANCE) -> bool:
    """Return True if a and b agree within `tol` (relative)."""
    return abs(a - b) / max(abs(a), abs(b), 1.0) <= tol


def _num(value: float | int | str | bool | None) -> float:
    """Unwrap a numeric ProvenanceCell value to a float."""
    assert isinstance(value, (int, float)) and not isinstance(value, bool)
    return float(value)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def engine_output() -> ValuationOutput:
    """Run the v8 GPU-first engine with default config (once per session)."""
    return run_valuation(ValuationConfig())


# ---------------------------------------------------------------------------
# Reference-value tests
# ---------------------------------------------------------------------------


def test_n_integer_matches_reference_every_year(engine_output: ValuationOutput) -> None:
    """Integer reference: N (gpus_per_node) matches the locked v8 trajectory."""
    actual = tuple(
        int(_num(engine_output.physical.years[fy].gpus_per_node.value)) for fy in REFERENCE_YEARS
    )
    assert actual == REFERENCE_N_BY_YEAR, f"engine N {actual} != reference {REFERENCE_N_BY_YEAR}"


def test_frontier_generations_match_reference(engine_output: ValuationOutput) -> None:
    """Every year picks the same frontier-generation name as the reference."""
    actual = tuple(
        engine_output.physical.years[fy].frontier_generation.value for fy in REFERENCE_YEARS
    )
    assert actual == REFERENCE_FRONTIER_NAMES, (
        f"engine frontier {actual} != reference {REFERENCE_FRONTIER_NAMES}"
    )


def test_physical_block_matches_reference(engine_output: ValuationOutput) -> None:
    """Physical block: kw_per_node, mass_per_node_t, pf_per_node within 0.5%."""
    for fy, ref in zip(REFERENCE_YEARS, REFERENCE_PHYSICAL, strict=True):
        py = engine_output.physical.years[fy]
        for field, ref_val in ref.items():
            actual = _num(getattr(py, field).value)
            assert _within_tolerance(actual, ref_val), (
                f"FY{fy} physical.{field}: engine {actual} vs reference {ref_val}"
            )


def test_node_economics_match_reference(engine_output: ValuationOutput) -> None:
    """Per-node economics: annualized cost + central revenue within 0.5%."""
    for fy, ref in zip(REFERENCE_YEARS, REFERENCE_NODE_ECONOMICS, strict=True):
        py = engine_output.physical.years[fy]
        for field, ref_val in ref.items():
            actual = _num(getattr(py, field).value)
            assert _within_tolerance(actual, ref_val), (
                f"FY{fy} physical.{field}: engine {actual} vs reference {ref_val}"
            )


def test_fleet_rollup_matches_reference(engine_output: ValuationOutput) -> None:
    """Fleet rollup: living-fleet count + central-R fleet revenue within 0.5%."""
    for fy, ref in zip(REFERENCE_YEARS, REFERENCE_FLEET, strict=True):
        by = engine_output.business.years[fy]
        # living_fleet is an integer count — exact match.
        assert int(_num(by.living_fleet.value)) == int(ref["living_fleet"]), (
            f"FY{fy} living_fleet: engine {by.living_fleet.value} vs reference "
            f"{ref['living_fleet']}"
        )
        actual_rev = _num(by.revenue_annual_fleet_musd_central.value)
        ref_rev = ref["revenue_annual_fleet_musd_central"]
        assert _within_tolerance(actual_rev, ref_rev), (
            f"FY{fy} revenue_annual_fleet_musd_central: engine {actual_rev} vs reference {ref_rev}"
        )


# ---------------------------------------------------------------------------
# Spot checks on the headline trajectory (the values the project reads)
# ---------------------------------------------------------------------------


def test_year_zero_n_is_223(engine_output: ValuationOutput) -> None:
    """Year 0 (FY2026) -> N = 223 (AI-1-class radiator dial, flat from day one)."""
    assert int(_num(engine_output.physical.years["2026"].gpus_per_node.value)) == 223


def test_year_ten_n_is_66(engine_output: ValuationOutput) -> None:
    """Year 10 (FY2036) -> N = 66 (2026-07-14 radiator rebase; was 37 at 0.012)."""
    assert int(_num(engine_output.physical.years["2036"].gpus_per_node.value)) == 66


def test_year_ten_node_kw_in_rebased_band(engine_output: ValuationOutput) -> None:
    """Year 10 node_kw ~753 kW under the 2026-07-14 light-radiator rebase."""
    kw = _num(engine_output.physical.years["2036"].kw_per_node.value)
    assert 748.0 <= kw <= 757.0, f"FY2036 node_kw {kw} outside the rebased band"
