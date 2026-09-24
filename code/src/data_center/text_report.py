"""Text rendering for the space artifact (a typed :class:`SpaceModelOutput`): the human view.

``render_text(output) -> str`` is the single public entry. It walks a
:class:`data_center.output.SpaceModelOutput` and emits a fixed-width
monospaced report covering, in order:

  1. Metadata (run identity).
  2. Provenance summary banner (key formula citations + cell count).
  3. Per-generation reference table.
  4. Per-year system metrics (frontier gen, mass, N, node kW, PFLOPS,
     mass-util %, volume-util %, binding constraint).
  5. Per-year per-node economics (cost / revenue / margin band).
  6. Per-year fleet rollup (launches, nodes, living fleet, kW,
     fleet revenue + profit + margin band).
  7. R-band block (the low / central / high revenue trajectory).
  8. Validation checks: every ``meta.validation_results`` entry (the V-rules,
     the model invariants, and the default guards when the run is the
     canonical default), the same list the embedded ``validation_warnings``
     jq query reads, so the report and the JSON cannot disagree on a verdict.

Every leaf value in the space artifact is a
:class:`common.provenance.ProvenanceCell`; this renderer reads each number
through the strict :func:`common.provenance.as_float` /
:func:`common.provenance.as_int`, so a cell holding a non-number where a number
belongs raises ``TypeError`` instead of printing a made-up 0.0. The provenance
banner counts cells with :func:`data_center.validation.collect_provenance_cells`,
the walker V13 uses, so the two report the same totals. Every section is total
over any artifact the engine builds: no ``KeyError``, no empty section.

Cycle-2 Phase 6 (T80-T84) rewrote this module for the cycle-2 fleet and
R-band layout, adding the provenance-summary banner and the dedicated R-band
trajectory block on top of the typed tables.
"""

from __future__ import annotations

import logging
from typing import Final

from common.meta import ValidationSeverity
from common.provenance import FormulaName, as_float, as_int
from data_center.input_manifest import revenue_anchors
from data_center.output import BusinessYear, PhysicalYear, SpaceModelOutput
from data_center.validation import collect_provenance_cells

logger = logging.getLogger(__name__)

# Fixed monospaced report width, in characters.
_WIDTH: Final[int] = 78

# Key formula_name keys cited in the provenance-summary banner: the
# load-bearing formulas a reader most wants to see traced. Each must exist
# in `common.provenance.FORMULAS`; the banner falls back gracefully if
# one is absent (e.g. a future schema rename).
_KEY_FORMULA_NAMES: Final[tuple[FormulaName, ...]] = (
    "n_packages_from_mass_envelope",
    "kw_per_node_from_n_and_kw_per_pkg",
    "cost_annual_per_node_from_breakdown",
    "revenue_annual_per_node_from_cost_and_r",
    "revenue_annual_fleet_from_cohorts",
    "living_fleet_from_cohort_cliff",
)


def _rule(char: str = "=") -> str:
    """A horizontal rule across the report width."""
    return char * _WIDTH


def _section_header(title: str) -> list[str]:
    """A two-line section header."""
    return ["", _rule(), f"  {title}", _rule()]


def _sorted_physical(output: SpaceModelOutput) -> list[tuple[int, PhysicalYear]]:
    """Return the ``physical.years`` map as a fy-sorted list of pairs."""
    return sorted(((int(fy), py) for fy, py in output.physical.years.items()), key=lambda kv: kv[0])


def _sorted_business(output: SpaceModelOutput) -> list[tuple[int, BusinessYear]]:
    """Return the ``business.years`` map as a fy-sorted list of pairs."""
    return sorted(((int(fy), by) for fy, by in output.business.years.items()), key=lambda kv: kv[0])


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------


def _render_header(output: SpaceModelOutput) -> list[str]:
    """The opening identity block."""
    md = output.metadata
    phys = _sorted_physical(output)
    fy0 = phys[0][0] if phys else md.base_year
    fyh = phys[-1][0] if phys else md.base_year
    return [
        _rule(),
        "  ROCKET LAB ORBITAL DATA-CENTER VENTURE - STANDALONE VALUATION "
        f"(GPU-FIRST {md.schema_version})",
        f"  schema:          {md.schema_version}",
        f"  horizon:         year 0 (FY{fy0}) .. year {md.horizon_years} (FY{fyh})",
        f"  workload:        {md.workload_type.value}",
        f"  operator model:  {md.operator_model.value}",
        f"  radiator:        {md.radiator_architecture.value}",
        f"  generated at:    {md.generated_at}",
        _rule(),
        "",
        "  This values the orbital AI-inference data-center venture ON ITS",
        "  OWN - not Rocket Lab the whole company. The model is GPU-first:",
        "  the package (NVIDIA's 'as sold' unit) is the core unit; N packages",
        "  are bound by the default block-upgrade Neutron SSO mass-envelope",
        "  scenario; every node-cost line follows. Revenue is an R band",
        "  (low / central / high).",
    ]


def _render_provenance_summary(output: SpaceModelOutput) -> list[str]:
    """Top-of-report provenance banner: cell coverage + key formula citations.

    Surfaces, before any table, that every leaf number in the space
    artifact is a typed :class:`ProvenanceCell` (value + unit + formula
    + upstream paths + sources): how many cells the run produced, how
    many distinct formulas back them, and the human-readable text of
    the load-bearing formulas (N from the mass envelope, node kW, node
    cost, per-node revenue, fleet revenue, the living-fleet cliff).

    Args:
        output: The space artifact.

    Returns:
        The provenance-summary section as a list of report lines.
    """
    lines: list[str] = []
    lines += _section_header("PROVENANCE SUMMARY")
    lines.append("")
    cells = collect_provenance_cells(output)
    formula_names = {c.formula_name for c in cells}
    lines.append("  Every leaf value below is a typed ProvenanceCell: value + unit +")
    lines.append(f"  formula + upstream paths + sources. This run produced {len(cells)} cells")
    lines.append(
        f"  across {len(formula_names)} distinct formulas; "
        f"meta.data_dictionary has {len(output.meta.data_dictionary)} entries."
    )
    lines.append("")
    lines.append("  Key formulas (full catalog: meta.formula_definitions):")
    for name in _KEY_FORMULA_NAMES:
        match = next((c for c in cells if c.formula_name == name), None)
        if match is None:
            continue
        lines.append(f"    {name}")
        lines.append(f"      {match.formula}")
    return lines


def _render_rband(output: SpaceModelOutput) -> list[str]:
    """The low / central / high R-band revenue trajectory.

    R is the revenue-to-cost multiplier (``revenue = R x cost``);
    cycle-2 models it as a band of three trajectories. This section
    shows, first, the input R anchors per trajectory (the
    source-of-truth dials a sweep would edit), then a per-year table of
    the implied R (fleet revenue / fleet cost) and the fleet annual
    revenue across all three bands, closing with the cumulative
    base-year-to-horizon revenue band.

    Args:
        output: The space artifact.

    Returns:
        The R-band section as a list of report lines.
    """
    lines: list[str] = []
    lines += _section_header("R-BAND REVENUE TRAJECTORY")
    lines.append("")
    lines.append("  R is the revenue-to-cost multiplier (revenue = R x cost). Cycle-2")
    lines.append("  models R as a band; revenue tracks the three trajectories below.")
    lines.append("")

    # Input R anchors: the source-of-truth dials.
    revenue = output.inputs.config.revenue
    for label, cells in (
        ("low", revenue.low),
        ("central", revenue.central),
        ("high", revenue.high),
    ):
        anchor_str = "  ".join(f"FY{a.fy}:{a.r:.2f}" for a in revenue_anchors(cells))
        lines.append(f"  R anchors ({label:>7}): {anchor_str}")
    lines.append("")

    # Per-year implied R + fleet revenue band.
    lines.append(
        f"  {'FY':>4} {'cost':>10} "
        f"{'R_low':>7} {'R_ctr':>7} {'R_high':>7} "
        f"{'rev_low':>11} {'rev_ctr':>11} {'rev_high':>11}"
    )
    lines.append(
        f"  {'-' * 4} {'-' * 10} {'-' * 7} {'-' * 7} {'-' * 7} {'-' * 11} {'-' * 11} {'-' * 11}"
    )
    for fy, by in _sorted_business(output):
        cost = as_float(by.cost_annual_fleet_musd)
        rev_low = as_float(by.revenue_annual_fleet_musd_low)
        rev_ctr = as_float(by.revenue_annual_fleet_musd_central)
        rev_high = as_float(by.revenue_annual_fleet_musd_high)
        # Implied R = fleet revenue / fleet cost (0.0 in a no-fleet year).
        r_low = rev_low / cost if cost else 0.0
        r_ctr = rev_ctr / cost if cost else 0.0
        r_high = rev_high / cost if cost else 0.0
        lines.append(
            f"  {fy:4d} {cost:10.1f} "
            f"{r_low:7.3f} {r_ctr:7.3f} {r_high:7.3f} "
            f"{rev_low:11.1f} {rev_ctr:11.1f} {rev_high:11.1f}"
        )

    # Cumulative revenue band at the horizon.
    biz = _sorted_business(output)
    if biz:
        _, last = biz[-1]
        lines.append("")
        lines.append(
            f"  Cumulative fleet revenue, base year -> FY{biz[-1][0]} ($M): "
            f"low {as_float(last.revenue_cumulative_musd_low):,.0f}  "
            f"central {as_float(last.revenue_cumulative_musd_central):,.0f}  "
            f"high {as_float(last.revenue_cumulative_musd_high):,.0f}"
        )
    return lines


def _render_generations(output: SpaceModelOutput) -> list[str]:
    """The per-generation reference table: what the model thinks each gen is."""
    lines: list[str] = []
    lines += _section_header("PER-GENERATION REFERENCE TABLE")
    lines.append("")
    lines.append(
        f"  {'Name':<18} {'Year':>6} {'$/pkg':>9} {'kW/pkg':>7} "
        f"{'kg/pkg':>7} {'PF/pkg':>7} {'dies':>5} {'class':<12}"
    )
    lines.append(
        f"  {'-' * 18} {'-' * 6} {'-' * 9} {'-' * 7} {'-' * 7} {'-' * 7} {'-' * 5} {'-' * 12}"
    )
    for g in output.inputs.config.generations:
        lines.append(
            f"  {str(g.name.value):<18} {as_float(g.year_available):6.1f} "
            f"{as_int(g.usd_per_pkg):9,d} {as_float(g.kw_per_pkg):7.2f} "
            f"{as_float(g.kg_per_pkg):7.2f} {as_float(g.pf_per_pkg):7.1f} "
            f"{as_int(g.die_count):5d} {g.name.source_status.value:<12}"
        )
    lines.append("")
    lines.append("  All per-package values are ALL-IN (incl. networking, cooling, NVLink fabric;")
    lines.append("  not bare die TDP). die_count tracks NVIDIA's 'as sold' unit (D8).")
    return lines


def _render_year_physical(output: SpaceModelOutput) -> list[str]:
    """Per-year system metrics: frontier gen, mass + volume, N, power, PFLOPS.

    One row per fiscal year. Carries the frontier generation, the
    mass-bound package count N, per-node mass and stowed volume, the
    mass- and volume-utilization percentages (mass-util packs the
    Neutron envelope tight; volume-util stays low: D6 mass-only
    binding), the per-node kW and PFLOPS, compute density, and the
    binding constraint.
    """
    lines: list[str] = []
    lines += _section_header("PER-YEAR SYSTEM METRICS")
    lines.append("")
    lines.append(
        f"  {'FY':>4} {'frontier':<14} {'N':>4} "
        f"{'node_t':>7} {'mass_u%':>8} {'node_m3':>8} {'vol_u%':>7} {'node_kW':>8} "
        f"{'PF_node':>9} {'PF/kW':>7} {'binding':>9}"
    )
    lines.append(
        f"  {'-' * 4} {'-' * 14} {'-' * 4} "
        f"{'-' * 7} {'-' * 8} {'-' * 8} {'-' * 7} {'-' * 8} "
        f"{'-' * 9} {'-' * 7} {'-' * 9}"
    )
    for fy, py in _sorted_physical(output):
        lines.append(
            f"  {fy:4d} {str(py.frontier_generation.value):<14} "
            f"{as_int(py.gpus_per_node):4d} "
            f"{as_float(py.mass_per_node_t):7.2f} "
            f"{as_float(py.mass_utilization_pct):7.1f}% "
            f"{as_float(py.volume_per_node_m3):8.2f} "
            f"{as_float(py.volume_utilization_pct):6.1f}% "
            f"{as_float(py.kw_per_node):8.1f} "
            f"{as_float(py.pf_per_node):9.1f} "
            f"{as_float(py.pf_per_kw):7.2f} "
            f"{str(py.binding_constraint.value):>9}"
        )
    return lines


def _render_year_economics(output: SpaceModelOutput) -> list[str]:
    """Per-year per-node economics: annual cost + revenue band + margin band."""
    lines: list[str] = []
    lines += _section_header("PER-YEAR PER-NODE ECONOMICS (annualized, $M/yr)")
    lines.append("")
    lines.append(
        f"  {'FY':>4} {'cost':>8} {'rev_low':>9} {'rev_ctr':>9} {'rev_high':>9} {'profit_ctr':>11}"
    )
    lines.append(f"  {'-' * 4} {'-' * 8} {'-' * 9} {'-' * 9} {'-' * 9} {'-' * 11}")
    for fy, py in _sorted_physical(output):
        lines.append(
            f"  {fy:4d} "
            f"{as_float(py.cost_annual_per_node_musd):8.2f} "
            f"{as_float(py.revenue_annual_per_node_musd_low):9.2f} "
            f"{as_float(py.revenue_annual_per_node_musd_central):9.2f} "
            f"{as_float(py.revenue_annual_per_node_musd_high):9.2f} "
            f"{as_float(py.gross_profit_annual_per_node_musd_central):11.2f}"
        )
    return lines


def _render_fleet(output: SpaceModelOutput) -> list[str]:
    """Per-year fleet rollup: launches, nodes, living fleet, kW, revenue band, margin band.

    The fleet table is the headline operational view: one row per
    fiscal year carrying the launch cadence, nodes deployed, the living
    fleet under the service-life cliff, kW on orbit, the fleet annual revenue
    across the full R band (low / central / high), and the gross-margin
    band. ``mgn l/c/h`` packs the three R-band margins into one column.
    """
    lines: list[str] = []
    lines += _section_header("PER-YEAR FLEET ROLLUP (living fleet, revenue $M, margin band)")
    lines.append("")
    lines.append(
        f"  {'FY':>4} {'launch':>7} {'nodes':>6} {'living':>7} {'kW_orbit':>10} "
        f"{'rev_low':>10} {'rev_ctr':>10} {'rev_high':>10} {'mgn l/c/h %':>16}"
    )
    lines.append(
        f"  {'-' * 4} {'-' * 7} {'-' * 6} {'-' * 7} {'-' * 10} "
        f"{'-' * 10} {'-' * 10} {'-' * 10} {'-' * 16}"
    )
    for fy, by in _sorted_business(output):
        margin_band = (
            f"{as_float(by.margin_low_pct):.0f}/"
            f"{as_float(by.margin_central_pct):.0f}/"
            f"{as_float(by.margin_high_pct):.0f}"
        )
        lines.append(
            f"  {fy:4d} "
            f"{as_int(by.launches):7d} "
            f"{as_int(by.nodes_deployed_this_year):6d} "
            f"{as_int(by.living_fleet):7d} "
            f"{as_float(by.kw_living_fleet):10.0f} "
            f"{as_float(by.revenue_annual_fleet_musd_low):10.1f} "
            f"{as_float(by.revenue_annual_fleet_musd_central):10.1f} "
            f"{as_float(by.revenue_annual_fleet_musd_high):10.1f} "
            f"{margin_band:>16}"
        )
    return lines


def _render_validation(output: SpaceModelOutput) -> list[str]:
    """Render every ``meta.validation_results`` entry with its verdict.

    Reads the public verdict list (not ``meta.validation.rules`` alone), so
    the report shows exactly the pass / warn / fail set the JSON publishes.
    """
    lines: list[str] = []
    lines += _section_header("VALIDATION CHECKS")
    lines.append("")
    results = output.meta.validation_results
    if not results:
        lines.append("  (No validation results for this run.)")
        return lines
    for result in results:
        mark = result.severity.value.upper()
        lines.append(f"  [{mark:>4}] {result.validation_id}: {result.what_tested}")
        lines.append(f"         expected {result.expected_condition}, got {result.observed_result}")
    not_passing = [r for r in results if r.severity is not ValidationSeverity.OK]
    lines.append("")
    lines.append(f"  {len(results) - len(not_passing)} of {len(results)} checks pass.")
    return lines


# ---------------------------------------------------------------------------
# Public entry
# ---------------------------------------------------------------------------


def render_text(output: SpaceModelOutput) -> str:
    """Render the full text report for one space artifact.

    Produces a fixed-width monospaced string covering, in order: the
    metadata header, the provenance-summary banner, the per-generation
    reference table, per-year system metrics, per-year per-node
    economics, the per-year fleet rollup, the R-band revenue
    trajectory, and the validation block. Over any artifact the engine
    builds: no ``KeyError``, no empty sections.

    Args:
        output: The space artifact to render.

    Returns:
        The full text report as a single string.

    Raises:
        TypeError: If a cell the report reads as a number holds a non-number
            (a hand-edited artifact; the strict unwrap never prints a made-up
            0.0).
    """
    lines: list[str] = []
    lines += _render_header(output)
    lines += _render_provenance_summary(output)
    lines += _render_generations(output)
    lines += _render_year_physical(output)
    lines += _render_year_economics(output)
    lines += _render_fleet(output)
    lines += _render_rband(output)
    lines += _render_validation(output)
    lines.append("")
    return "\n".join(lines)


def render_headline(output: SpaceModelOutput) -> str:
    """Render a one-line GPU-first headline for the ``--brief`` CLI mode.

    Reports the operational trajectory a reader scans: the package-count
    trajectory, the living-fleet trajectory, and the central-R fleet
    revenue + margin at the horizon year.

    Args:
        output: The space artifact.

    Returns:
        A one-line headline string.
    """
    phys = _sorted_physical(output)
    biz = _sorted_business(output)
    if not phys or not biz:
        return "GPU-first trajectory: (no years emitted)"
    fy0, py0 = phys[0]
    fyh, pyh = phys[-1]
    _, byh = biz[-1]
    n0 = as_int(py0.gpus_per_node)
    nh = as_int(pyh.gpus_per_node)
    living = as_int(byh.living_fleet)
    rev = as_float(byh.revenue_annual_fleet_musd_central)
    margin = as_float(byh.margin_central_pct)
    return (
        f"GPU-first trajectory @ FY{fyh}: "
        f"N {n0} -> {nh} packages/node; "
        f"living fleet {living} nodes; "
        f"fleet annual revenue ${rev:,.0f}M (central R); "
        f"gross margin {margin:.0f}%"
    )
