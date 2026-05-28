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

**Margin-floor re-freeze (2026-05-25).** The default central R band now decays
from 1.50 to 1.40, not 1.30, so the five-year operating plan remains above
the 25% active-fleet gross-margin floor.

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
# from the v8 engine at the corrected radiator dial 0.012 (D17).
# ---------------------------------------------------------------------------

REFERENCE_N_BY_YEAR: tuple[int, ...] = (
    146,  # FY2026 (B300/GB300)
    117,  # FY2027 (Rubin VR200)
    81,  # FY2028 (Rubin Ultra)
    70,  # FY2029 (Feynman)
    70,  # FY2030 (Feynman)
    62,  # FY2031 (Gen+1 extrap) — radiator 0.012 + kw_growth 0.20 from year 5
    52,  # FY2032 (Gen+2 extrap)
    52,  # FY2033 (Gen+2 extrap)
    44,  # FY2034 (Gen+3 extrap)
    37,  # FY2035 (Gen+4 extrap)
    37,  # FY2036 (Gen+4 extrap)
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
    {"kw_per_node": 299.300, "mass_per_node_t": 12.4426, "pf_per_node": 2190.0},
    {"kw_per_node": 304.200, "mass_per_node_t": 12.4918, "pf_per_node": 3978.0},
    {"kw_per_node": 337.770, "mass_per_node_t": 12.3885, "pf_per_node": 4212.0},
    {"kw_per_node": 385.000, "mass_per_node_t": 12.4400, "pf_per_node": 7000.0},
    {"kw_per_node": 385.000, "mass_per_node_t": 12.4400, "pf_per_node": 7000.0},
    {"kw_per_node": 409.200, "mass_per_node_t": 12.4696, "pf_per_node": 10075.0},
    {"kw_per_node": 411.840, "mass_per_node_t": 12.3935, "pf_per_node": 13731.25},
    {"kw_per_node": 411.840, "mass_per_node_t": 12.3935, "pf_per_node": 13731.25},
    {"kw_per_node": 418.176, "mass_per_node_t": 12.4388, "pf_per_node": 18880.4688},
    {"kw_per_node": 421.978, "mass_per_node_t": 12.4482, "pf_per_node": 25799.7314},
    {"kw_per_node": 421.978, "mass_per_node_t": 12.4482, "pf_per_node": 25799.7314},
)

# Per-year per-node annualized economics — central R band.
REFERENCE_NODE_ECONOMICS: tuple[dict[str, float], ...] = (
    {"cost_annual_per_node_musd": 13.43280, "revenue_annual_per_node_musd_central": 20.14920},
    {"cost_annual_per_node_musd": 13.05720, "revenue_annual_per_node_musd_central": 19.45523},
    {"cost_annual_per_node_musd": 14.82576, "revenue_annual_per_node_musd_central": 21.94212},
    {"cost_annual_per_node_musd": 15.77028, "revenue_annual_per_node_musd_central": 23.18231},
    {"cost_annual_per_node_musd": 15.27519, "revenue_annual_per_node_musd_central": 22.30178},
    {"cost_annual_per_node_musd": 15.75768, "revenue_annual_per_node_musd_central": 22.84863},
    {"cost_annual_per_node_musd": 15.78050, "revenue_annual_per_node_musd_central": 22.72392},
    {"cost_annual_per_node_musd": 15.42402, "revenue_annual_per_node_musd_central": 22.05636},
    {"cost_annual_per_node_musd": 15.63182, "revenue_annual_per_node_musd_central": 22.19718},
    {"cost_annual_per_node_musd": 15.85486, "revenue_annual_per_node_musd_central": 22.35535},
    {"cost_annual_per_node_musd": 15.66191, "revenue_annual_per_node_musd_central": 21.92667},
)

# Per-year fleet rollup reference — living fleet + central-R fleet revenue.
REFERENCE_FLEET: tuple[dict[str, float], ...] = (
    {"living_fleet": 0, "revenue_annual_fleet_musd_central": 0.0000},
    {"living_fleet": 2, "revenue_annual_fleet_musd_central": 38.9105},
    {"living_fleet": 5, "revenue_annual_fleet_musd_central": 104.7368},
    {"living_fleet": 10, "revenue_annual_fleet_musd_central": 220.6484},
    {"living_fleet": 19, "revenue_annual_fleet_musd_central": 421.3644},
    {"living_fleet": 33, "revenue_annual_fleet_musd_central": 741.2452},
    {"living_fleet": 53, "revenue_annual_fleet_musd_central": 1202.2609},
    {"living_fleet": 85, "revenue_annual_fleet_musd_central": 1908.4070},
    {"living_fleet": 131, "revenue_annual_fleet_musd_central": 2924.5516},
    {"living_fleet": 192, "revenue_annual_fleet_musd_central": 4288.7102},
    {"living_fleet": 268, "revenue_annual_fleet_musd_central": 5942.2301},
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


def test_year_zero_n_is_146(engine_output: ValuationOutput) -> None:
    """Year 0 (FY2026) -> N = 146 (radiator dial not yet active)."""
    assert int(_num(engine_output.physical.years["2026"].gpus_per_node.value)) == 146


def test_year_ten_n_is_37(engine_output: ValuationOutput) -> None:
    """Year 10 (FY2036) -> N = 37 (kw_growth 0.20 correction, up from the 0.30-era 27)."""
    assert int(_num(engine_output.physical.years["2036"].gpus_per_node.value)) == 37


def test_year_ten_node_kw_in_corrected_band(engine_output: ValuationOutput) -> None:
    """Year 10 node_kw ~422 kW — D17 radiator + V-A kw_growth 0.20 corrections."""
    kw = _num(engine_output.physical.years["2036"].kw_per_node.value)
    assert 418.0 <= kw <= 426.0, f"FY2036 node_kw {kw} outside the corrected band"
