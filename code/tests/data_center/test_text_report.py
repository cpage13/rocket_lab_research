"""Tests for the v8 text report (cycle-2 Phase 6, T85).

``data_center.text_report.render_text`` walks a typed v8
:class:`data_center.output.ValuationOutput` and emits the human-readable
fixed-width report. After cycle-2 Phase 6 (T80-T84) that report has
eight sections in a fixed order: the metadata header, the
provenance-summary banner, the per-generation reference table, the
per-year system-metrics table (now carrying volume-util), the per-year
per-node economics table, the per-year fleet rollup (now carrying the
full revenue + margin band), the R-band revenue-trajectory block, and
the validation block.

These tests guard that layout:

1. every section header is present, in order;
2. the renderer is total — no exception, no ``KeyError``, no empty
   section, on the real default-scenario output;
3. the v8-specific content lands — the provenance banner cites
   formulas, the physical table shows volume-util, the fleet table
   shows the revenue band, the R-band block shows all three
   trajectories;
4. ``render_headline`` produces the one-line ``--brief`` view.

The fixture runs the default scenario through the real engine, so the
tests exercise the renderer against a genuine v8 artifact rather than a
hand-built stub.
"""

from __future__ import annotations

import pytest

from data_center.config import load_config
from data_center.engine import run_valuation
from data_center.output import ValuationOutput
from data_center.text_report import render_headline, render_text

# The eight v8 section headers, in render order (T80 section ordering).
_SECTION_HEADERS: tuple[str, ...] = (
    "ROCKET LAB ORBITAL DATA-CENTER VENTURE",
    "PROVENANCE SUMMARY",
    "PER-GENERATION REFERENCE TABLE",
    "PER-YEAR SYSTEM METRICS",
    "PER-YEAR PER-NODE ECONOMICS",
    "PER-YEAR FLEET ROLLUP",
    "R-BAND REVENUE TRAJECTORY",
    "VALIDATION CHECKS",
)


@pytest.fixture(scope="module")
def default_output() -> ValuationOutput:
    """Run the default scenario through the v8 engine once for the module."""
    return run_valuation(load_config("scenarios/default.yaml"))


@pytest.fixture(scope="module")
def default_report(default_output: ValuationOutput) -> str:
    """Render the default-scenario text report once for the module."""
    return render_text(default_output)


# ---------------------------------------------------------------------------
# Section presence + ordering
# ---------------------------------------------------------------------------


def test_render_text_returns_a_nonempty_string(default_report: str) -> None:
    """render_text produces a non-trivial multi-line report."""
    assert isinstance(default_report, str)
    assert len(default_report.splitlines()) > 50


def test_all_eight_sections_present(default_report: str) -> None:
    """Every one of the eight v8 section headers appears in the report."""
    for header in _SECTION_HEADERS:
        assert header in default_report, f"missing section: {header}"


def test_sections_appear_in_render_order(default_report: str) -> None:
    """The eight sections appear in the fixed v8 order (T80)."""
    positions = [default_report.index(h) for h in _SECTION_HEADERS]
    assert positions == sorted(positions)


def test_provenance_summary_precedes_generation_table(default_report: str) -> None:
    """The provenance banner is a top-of-report banner (before the gen table)."""
    assert default_report.index("PROVENANCE SUMMARY") < default_report.index(
        "PER-GENERATION REFERENCE TABLE"
    )


# ---------------------------------------------------------------------------
# Renderer is total — no exception, no empty section
# ---------------------------------------------------------------------------


def test_render_text_raises_no_exception(default_output: ValuationOutput) -> None:
    """render_text is total — it does not raise on a real v8 artifact."""
    render_text(default_output)


def test_no_section_is_empty(default_report: str) -> None:
    """No section header is immediately followed by another (every section has body)."""
    headers_only = set(_SECTION_HEADERS)
    lines = default_report.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped in headers_only:
            # Find the next non-blank, non-rule line within the next 6 lines.
            body = [
                ln.strip() for ln in lines[i + 1 : i + 8] if ln.strip() and set(ln.strip()) != {"="}
            ]
            assert body, f"section {stripped!r} has no body"


# ---------------------------------------------------------------------------
# Provenance summary banner (T83)
# ---------------------------------------------------------------------------


def test_provenance_summary_states_cell_count(default_report: str) -> None:
    """The provenance banner reports a positive ProvenanceCell count."""
    banner = default_report.split("PROVENANCE SUMMARY", 1)[1]
    assert "ProvenanceCell" in banner
    assert "cells" in banner


def test_provenance_summary_cites_key_formulas(default_report: str) -> None:
    """The provenance banner cites the load-bearing formula names."""
    banner = default_report.split("PROVENANCE SUMMARY", 1)[1].split("PER-GENERATION", 1)[0]
    assert "n_packages_from_mass_envelope" in banner
    assert "revenue_annual_per_node_from_cost_and_r" in banner


# ---------------------------------------------------------------------------
# Per-year physical table (T82) — volume-util column
# ---------------------------------------------------------------------------


def test_physical_table_has_volume_utilization_column(default_report: str) -> None:
    """The per-year system-metrics table carries the volume-util column (T82)."""
    metrics = default_report.split("PER-YEAR SYSTEM METRICS", 1)[1].split("PER-YEAR PER-NODE", 1)[0]
    assert "vol_u%" in metrics
    assert "node_m3" in metrics
    assert "mass_u%" in metrics


def test_physical_table_renders_every_year(
    default_report: str, default_output: ValuationOutput
) -> None:
    """The physical table renders one row per fiscal year."""
    metrics = default_report.split("PER-YEAR SYSTEM METRICS", 1)[1].split("PER-YEAR PER-NODE", 1)[0]
    for fy in default_output.physical.years:
        assert fy in metrics


# ---------------------------------------------------------------------------
# Per-year fleet rollup (T81) — revenue + margin band
# ---------------------------------------------------------------------------


def test_fleet_table_shows_full_revenue_band(default_report: str) -> None:
    """The fleet rollup table carries the low / central / high revenue band (T81)."""
    fleet = default_report.split("PER-YEAR FLEET ROLLUP", 1)[1].split("R-BAND REVENUE", 1)[0]
    assert "rev_low" in fleet
    assert "rev_ctr" in fleet
    assert "rev_high" in fleet


def test_fleet_table_shows_margin_band_and_nodes(default_report: str) -> None:
    """The fleet rollup table carries the margin band and the nodes column (T81)."""
    fleet = default_report.split("PER-YEAR FLEET ROLLUP", 1)[1].split("R-BAND REVENUE", 1)[0]
    assert "mgn l/c/h" in fleet
    assert "nodes" in fleet
    assert "living" in fleet


# ---------------------------------------------------------------------------
# R-band block (T84)
# ---------------------------------------------------------------------------


def test_rband_block_shows_three_trajectories(default_report: str) -> None:
    """The R-band block names all three trajectories (low / central / high)."""
    rband = default_report.split("R-BAND REVENUE TRAJECTORY", 1)[1].split("VALIDATION CHECKS", 1)[0]
    assert "low" in rband
    assert "central" in rband
    assert "high" in rband


def test_rband_block_shows_input_anchors(default_report: str) -> None:
    """The R-band block surfaces the input R anchors."""
    rband = default_report.split("R-BAND REVENUE TRAJECTORY", 1)[1].split("VALIDATION CHECKS", 1)[0]
    assert "R anchors" in rband
    # The default central band starts at R = 1.50 in FY2026.
    assert "FY2026:1.50" in rband


def test_rband_block_shows_cumulative_revenue(default_report: str) -> None:
    """The R-band block closes with the cumulative revenue band."""
    rband = default_report.split("R-BAND REVENUE TRAJECTORY", 1)[1].split("VALIDATION CHECKS", 1)[0]
    assert "Cumulative fleet revenue" in rband


# ---------------------------------------------------------------------------
# Validation block
# ---------------------------------------------------------------------------


def test_validation_block_renders_every_rule(
    default_report: str, default_output: ValuationOutput
) -> None:
    """The validation block renders one line per V-rule (17 on the default scenario)."""
    validation = default_report.split("VALIDATION CHECKS", 1)[1]
    rules = default_output.meta.validation.rules
    assert len(rules) == 17
    for rule in rules:
        assert rule.name in validation


def test_validation_block_marks_passing_rules(default_report: str) -> None:
    """All V-rules pass on the default scenario, so the block shows PASS marks."""
    validation = default_report.split("VALIDATION CHECKS", 1)[1]
    assert "PASS" in validation
    assert "FAIL" not in validation


# ---------------------------------------------------------------------------
# Headline (--brief)
# ---------------------------------------------------------------------------


def test_render_headline_is_one_line(default_output: ValuationOutput) -> None:
    """render_headline produces a single-line GPU-first headline."""
    headline = render_headline(default_output)
    assert isinstance(headline, str)
    assert "\n" not in headline
    assert "GPU-first" in headline


def test_render_headline_reports_fleet_revenue(default_output: ValuationOutput) -> None:
    """The headline reports the horizon-year fleet revenue and margin."""
    headline = render_headline(default_output)
    assert "fleet annual revenue" in headline
    assert "gross margin" in headline
