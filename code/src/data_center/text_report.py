"""Text rendering for a typed v8 :class:`ValuationOutput` — the human view.

``render_text(output) -> str`` is the single public entry. It walks a
v8 :class:`data_center.output.ValuationOutput` and emits a fixed-width
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
  8. Validation checks (V1..V17, pass/fail).

Every leaf value in the v8 output is a
:class:`data_center.provenance.ProvenanceCell`; this renderer reads each
cell's ``.value``. Every section is total: no ``KeyError``, no
exceptions, no empty section.

Cycle-2 Phase 6 (T80–T84) rewrote this module for the v8 fleet +
R-band layout — adding the provenance-summary banner and the dedicated
R-band trajectory block on top of the v8-typed tables.
"""

from __future__ import annotations

from data_center.output import (
    BusinessYear,
    PhysicalYear,
    ValuationOutput,
)
from data_center.provenance import ProvenanceCell

_WIDTH = 78

# Key formula_name keys cited in the provenance-summary banner — the
# load-bearing formulas a reader most wants to see traced. Each must exist
# in `data_center.provenance.FORMULAS`; the banner falls back gracefully if
# one is absent (e.g. a future schema rename).
_KEY_FORMULA_NAMES: tuple[str, ...] = (
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


def _num(value: float | int | str | bool | None) -> float:
    """Unwrap a numeric :class:`ProvenanceCell` value to a ``float``.

    Args:
        value: A ProvenanceCell ``value`` field.

    Returns:
        The value as a ``float`` (``0.0`` for a non-numeric value).
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return 0.0
    return float(value)


def _sorted_physical(output: ValuationOutput) -> list[tuple[int, PhysicalYear]]:
    """Return the ``physical.years`` map as a fy-sorted list of pairs."""
    return sorted(((int(fy), py) for fy, py in output.physical.years.items()), key=lambda kv: kv[0])


def _sorted_business(output: ValuationOutput) -> list[tuple[int, BusinessYear]]:
    """Return the ``business.years`` map as a fy-sorted list of pairs."""
    return sorted(((int(fy), by) for fy, by in output.business.years.items()), key=lambda kv: kv[0])


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------


def _render_header(output: ValuationOutput) -> list[str]:
    """The opening identity block."""
    md = output.metadata
    phys = _sorted_physical(output)
    fy0 = phys[0][0] if phys else md.base_year
    fyh = phys[-1][0] if phys else md.base_year
    return [
        _rule(),
        "  ROCKET LAB ORBITAL DATA-CENTER VENTURE - STANDALONE VALUATION (GPU-FIRST v8)",
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


def _collect_cells(output: ValuationOutput) -> list[ProvenanceCell]:
    """Collect every per-year :class:`ProvenanceCell` in the output.

    Walks ``physical.years`` and ``business.years``; every field of a
    :class:`PhysicalYear` / :class:`BusinessYear` is a ProvenanceCell.

    Args:
        output: The v8 valuation output.

    Returns:
        A flat list of every per-year provenance cell, in iteration order.
    """
    cells: list[ProvenanceCell] = []
    for py in output.physical.years.values():
        cells.extend(v for v in py.__dict__.values() if isinstance(v, ProvenanceCell))
    for by in output.business.years.values():
        cells.extend(v for v in by.__dict__.values() if isinstance(v, ProvenanceCell))
    return cells


def _render_provenance_summary(output: ValuationOutput) -> list[str]:
    """Top-of-report provenance banner — cell coverage + key formula citations.

    Surfaces, before any table, that every leaf number in the v8
    artifact is a typed :class:`ProvenanceCell` (value + unit + formula
    + upstream paths + sources): how many cells the run produced, how
    many distinct formulas back them, and the human-readable text of
    the load-bearing formulas (N from the mass envelope, node kW, node
    cost, per-node revenue, fleet revenue, the living-fleet cliff).

    Args:
        output: The v8 valuation output.

    Returns:
        The provenance-summary section as a list of report lines.
    """
    lines: list[str] = []
    lines += _section_header("PROVENANCE SUMMARY")
    lines.append("")
    cells = _collect_cells(output)
    formula_names = {c.formula_name for c in cells}
    lines.append("  Every leaf value below is a typed ProvenanceCell: value + unit +")
    lines.append(f"  formula + upstream paths + sources. This run produced {len(cells)} cells")
    lines.append(
        f"  across {len(formula_names)} distinct formulas; "
        f"meta.data_dictionary has {len(output.meta.data_dictionary)} entries."
    )
    lines.append("")
    lines.append("  Key formulas (full catalog: inputs trace -> meta.data_dictionary):")
    for name in _KEY_FORMULA_NAMES:
        match = next((c for c in cells if c.formula_name == name), None)
        if match is None:
            continue
        lines.append(f"    {name}")
        lines.append(f"      {match.formula}")
    return lines


def _render_rband(output: ValuationOutput) -> list[str]:
    """The low / central / high R-band revenue trajectory.

    R is the revenue-to-cost multiplier (``revenue = R x cost``);
    cycle-2 models it as a band of three trajectories. This section
    shows, first, the input R anchors per trajectory (the
    source-of-truth dials a sweep would edit), then a per-year table of
    the implied R (fleet revenue / fleet cost) and the fleet annual
    revenue across all three bands, closing with the cumulative
    base-year-to-horizon revenue band.

    Args:
        output: The v8 valuation output.

    Returns:
        The R-band section as a list of report lines.
    """
    lines: list[str] = []
    lines += _section_header("R-BAND REVENUE TRAJECTORY")
    lines.append("")
    lines.append("  R is the revenue-to-cost multiplier (revenue = R x cost). Cycle-2")
    lines.append("  models R as a band; revenue tracks the three trajectories below.")
    lines.append("")

    # Input R anchors — the source-of-truth dials.
    rb = output.inputs.r_band
    for label, anchors in (("low", rb.low), ("central", rb.central), ("high", rb.high)):
        anchor_str = "  ".join(f"FY{a.fy}:{a.r:.2f}" for a in anchors)
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
        cost = _num(by.cost_annual_fleet_musd.value)
        rev_low = _num(by.revenue_annual_fleet_musd_low.value)
        rev_ctr = _num(by.revenue_annual_fleet_musd_central.value)
        rev_high = _num(by.revenue_annual_fleet_musd_high.value)
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
            f"low {_num(last.revenue_cumulative_musd_low.value):,.0f}  "
            f"central {_num(last.revenue_cumulative_musd_central.value):,.0f}  "
            f"high {_num(last.revenue_cumulative_musd_high.value):,.0f}"
        )
    return lines


def _render_generations(output: ValuationOutput) -> list[str]:
    """The per-generation reference table — what the model thinks each gen is."""
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
    for g in output.inputs.generations:
        lines.append(
            f"  {str(g['name']):<18} {float(g['year_available']):6.1f} "
            f"{int(g['usd_per_pkg']):9,d} {float(g['kw_per_pkg']):7.2f} "
            f"{float(g['kg_per_pkg']):7.2f} {float(g['pf_per_pkg']):7.1f} "
            f"{int(g['die_count']):5d} {str(g['source_class']):<12}"
        )
    lines.append("")
    lines.append("  All per-package values are ALL-IN (incl. networking, cooling, NVLink fabric;")
    lines.append("  not bare die TDP). die_count tracks NVIDIA's 'as sold' unit (D8).")
    return lines


def _render_year_physical(output: ValuationOutput) -> list[str]:
    """Per-year system metrics — frontier gen, mass + volume, N, power, PFLOPS.

    One row per fiscal year. Carries the frontier generation, the
    mass-bound package count N, per-node mass and stowed volume, the
    mass- and volume-utilization percentages (mass-util packs the
    Neutron envelope tight; volume-util stays low — D6 mass-only
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
            f"{int(_num(py.gpus_per_node.value)):4d} "
            f"{_num(py.mass_per_node_t.value):7.2f} "
            f"{_num(py.mass_utilization_pct.value):7.1f}% "
            f"{_num(py.volume_per_node_m3.value):8.2f} "
            f"{_num(py.volume_utilization_pct.value):6.1f}% "
            f"{_num(py.kw_per_node.value):8.1f} "
            f"{_num(py.pf_per_node.value):9.1f} "
            f"{_num(py.pf_per_kw.value):7.2f} "
            f"{str(py.binding_constraint.value):>9}"
        )
    return lines


def _render_year_economics(output: ValuationOutput) -> list[str]:
    """Per-year per-node economics — annual cost + revenue band + margin band."""
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
            f"{_num(py.cost_annual_per_node_musd.value):8.2f} "
            f"{_num(py.revenue_annual_per_node_musd_low.value):9.2f} "
            f"{_num(py.revenue_annual_per_node_musd_central.value):9.2f} "
            f"{_num(py.revenue_annual_per_node_musd_high.value):9.2f} "
            f"{_num(py.gross_profit_annual_per_node_musd_central.value):11.2f}"
        )
    return lines


def _render_fleet(output: ValuationOutput) -> list[str]:
    """Per-year fleet rollup — launches, nodes, living fleet, kW, revenue band, margin band.

    The fleet table is the headline operational view: one row per
    fiscal year carrying the launch cadence, nodes deployed, the living
    fleet under the 5-year cliff, kW on orbit, the fleet annual revenue
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
            f"{_num(by.margin_low_pct.value):.0f}/"
            f"{_num(by.margin_central_pct.value):.0f}/"
            f"{_num(by.margin_high_pct.value):.0f}"
        )
        lines.append(
            f"  {fy:4d} "
            f"{int(_num(by.launches.value)):7d} "
            f"{int(_num(by.nodes_deployed_this_year.value)):6d} "
            f"{int(_num(by.living_fleet.value)):7d} "
            f"{_num(by.kw_on_orbit.value):10.0f} "
            f"{_num(by.revenue_annual_fleet_musd_low.value):10.1f} "
            f"{_num(by.revenue_annual_fleet_musd_central.value):10.1f} "
            f"{_num(by.revenue_annual_fleet_musd_high.value):10.1f} "
            f"{margin_band:>16}"
        )
    return lines


def _render_validation(output: ValuationOutput) -> list[str]:
    """Render the engine-computed validation-check block."""
    lines: list[str] = []
    lines += _section_header("VALIDATION CHECKS")
    lines.append("")
    rules = output.meta.validation.rules
    if not rules:
        lines.append("  (No engine-computed checks for this run.)")
        return lines
    for v in rules:
        mark = "PASS" if v.pass_check else f"FAIL ({v.severity.value})"
        lines.append(f"  [{mark:>14}] {v.name}: {v.what_it_tests}")
        lines.append(f"                  expected {v.expected}, got {v.computed}")
    return lines


# ---------------------------------------------------------------------------
# Public entry
# ---------------------------------------------------------------------------


def render_text(output: ValuationOutput) -> str:
    """Render the full text report for one v8 :class:`ValuationOutput`.

    Produces a fixed-width monospaced string covering, in order: the
    metadata header, the provenance-summary banner, the per-generation
    reference table, per-year system metrics, per-year per-node
    economics, the per-year fleet rollup, the R-band revenue
    trajectory, and the validation block. No exceptions, no
    ``KeyError``, no empty sections.

    Args:
        output: The v8 valuation output to render.

    Returns:
        The full text report as a single string.
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


def render_headline(output: ValuationOutput) -> str:
    """Render a one-line GPU-first headline for the ``--brief`` CLI mode.

    Reports the operational trajectory a reader scans: the package-count
    trajectory, the living-fleet trajectory, and the central-R fleet
    revenue + margin at the horizon year.

    Args:
        output: The v8 valuation output.

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
    n0 = int(_num(py0.gpus_per_node.value))
    nh = int(_num(pyh.gpus_per_node.value))
    living = int(_num(byh.living_fleet.value))
    rev = _num(byh.revenue_annual_fleet_musd_central.value)
    margin = _num(byh.margin_central_pct.value)
    return (
        f"GPU-first trajectory @ FY{fyh}: "
        f"N {n0} -> {nh} packages/node; "
        f"living fleet {living} nodes; "
        f"fleet annual revenue ${rev:,.0f}M (central R); "
        f"gross margin {margin:.0f}%"
    )
