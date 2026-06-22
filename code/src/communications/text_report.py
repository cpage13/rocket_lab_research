"""Text rendering for a typed :class:`CommsModelOutput` (the human view).

``render_comms_text(output)`` is the single public report entry; it walks a comms
space-model output and emits a fixed-width monospaced report covering, in order:

  1. Run identity (scenario, schema, horizon, steady-state year, generated-at).
  2. Provenance summary banner (key formula citations + the cell count).
  3. Per-year per-class physical / cost table (the two satellite classes, the
     packing fork, the per-satellite cost, plus the per-year spectrum cells).
  4. Per-year living-fleet rollup (launches, deployed, living fleet, fleet cost).
  5. Steady-state customer + cost band (the comms HEADLINE block).
  6. Validation checks (the enriched rule list, or a placeholder on a lean run).

When a :class:`communications.ground.GroundReferenceOutput` is supplied,
``render_comms_text`` ALSO renders the cost-to-cost comparison block (the SPARSE
and DENSE regimes side by side, the revenue-ceiling reconciliation, and the
Starlink-floor figures) as NUMBERS and FLAGS, never a verdict string (the
baked-in-conclusion gate; the editorial verdict is the hand-written Phase 6).

``render_comms_headline(output)`` is the one-line ``--brief`` headline. Every
section is total: no ``KeyError``, no exception, no empty section.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Final

from common.provenance import ProvenanceCell
from communications.output import BusinessYear, CommsModelOutput, PhysicalYear

if TYPE_CHECKING:
    from communications.ground import GroundReferenceOutput

logger = logging.getLogger(__name__)

_WIDTH: Final[int] = 78
"""The fixed monospaced report width, in characters."""

_KEY_FORMULA_NAMES: Final[tuple[str, ...]] = (
    "comms_satellite_build_cost_from_four_areas",
    "comms_satellite_total_cost_from_build_and_launch",
    "comms_living_fleet_satellites_from_cohort_cliff",
    "comms_cost_annual_per_customer_from_fleet_cost_and_served",
    "comms_per_beam_capacity_from_empirical_anchor",
    "comms_total_served_from_per_sat_and_count",
)
"""The load-bearing comms formula names cited in the provenance banner; the banner
falls back gracefully on any name the run's cells do not actually carry."""


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


def _flag(value: float | int | str | bool | None) -> str:
    """Render a boolean cell value as a yes/no flag string."""
    return "yes" if value is True else "no"


def _sorted_physical(output: CommsModelOutput) -> list[tuple[int, PhysicalYear]]:
    """Return the ``physical.years`` map as a fy-sorted list of pairs."""
    return sorted(((int(fy), py) for fy, py in output.physical.years.items()), key=lambda kv: kv[0])


def _sorted_business(output: CommsModelOutput) -> list[tuple[int, BusinessYear]]:
    """Return the ``business.years`` map as a fy-sorted list of pairs."""
    return sorted(((int(fy), by) for fy, by in output.business.years.items()), key=lambda kv: kv[0])


def _steady_state_business(output: CommsModelOutput) -> BusinessYear | None:
    """Return the steady-state-year business record, or None if absent."""
    return output.business.years.get(str(output.metadata.steady_state_year))


# ---------------------------------------------------------------------------
# Sections.
# ---------------------------------------------------------------------------


def _render_header(output: CommsModelOutput) -> list[str]:
    """The opening run-identity block."""
    md = output.metadata
    phys = _sorted_physical(output)
    fy0 = phys[0][0] if phys else md.base_year
    fyh = phys[-1][0] if phys else md.base_year
    return [
        _rule(),
        "  ROCKET LAB NEUTRON COMMUNICATIONS CONSTELLATION - COST-VS-GROUND MODEL",
        f"  scenario:        {md.scenario_name}",
        f"  schema:          {md.schema_version}",
        f"  horizon:         year 0 (FY{fy0}) .. year {md.horizon_years} (FY{fyh})",
        f"  steady state:    FY{md.steady_state_year}",
        f"  artifact role:   {md.artifact_role}",
        f"  generated at:    {md.generated_at}",
        _rule(),
        "",
        "  This model asks whether Neutron-launched space connectivity could",
        "  plausibly beat ground on COST (the cost-to-cost ratio and the retail",
        "  undercut). Demand is assumed, not modeled. The satellite is costed",
        "  bottom-up from four areas; customers fall out of the spectrum-capacity",
        "  physics as a band. The model bakes in no editorial conclusion.",
    ]


def _collect_cells(output: CommsModelOutput) -> list[ProvenanceCell]:
    """Collect every per-year :class:`ProvenanceCell` (one level into sub-blocks).

    Args:
        output: The comms output.

    Returns:
        A flat list of every per-year provenance cell.
    """
    cells: list[ProvenanceCell] = []

    def _walk(record: object) -> None:
        if isinstance(record, ProvenanceCell):
            cells.append(record)
            return
        if hasattr(record, "__dict__"):
            for value in vars(record).values():
                if isinstance(value, ProvenanceCell):
                    cells.append(value)
                elif hasattr(value, "__dict__"):
                    _walk(value)

    for _, py in _sorted_physical(output):
        _walk(py)
    for _, by in _sorted_business(output):
        _walk(by)
    return cells


def _render_provenance_summary(output: CommsModelOutput) -> list[str]:
    """The provenance banner: cell coverage + key formula citations."""
    from common.provenance import FORMULAS  # noqa: PLC0415 - local lookup of shared registry

    cells = _collect_cells(output)
    distinct = {c.formula_name for c in cells}
    lines: list[str] = []
    lines += _section_header("PROVENANCE SUMMARY")
    lines.append("")
    lines.append("  Every leaf number is a typed ProvenanceCell (value + unit + formula +")
    lines.append("  upstream paths + sources). Cell coverage and key formulas:")
    lines.append("")
    lines.append(f"  cells emitted:       {len(cells)}")
    lines.append(f"  distinct formulas:   {len(distinct)}")
    lines.append("")
    lines.append("  key formulas:")
    for name in _KEY_FORMULA_NAMES:
        spec = FORMULAS.get(name)
        if spec is None:
            continue
        lines.append(f"    - {name}:")
        lines.append(f"        {spec.formula}")
    return lines


def _render_year_physical(output: CommsModelOutput) -> list[str]:
    """The per-year per-class physical / cost table plus the spectrum cells."""
    lines: list[str] = []
    lines += _section_header("PER-YEAR PER-CLASS PHYSICAL + COST (per-satellite $M, spectrum)")
    lines.append("")
    lines.append(
        f"  {'FY':>4} {'class':>14} {'/launch':>8} {'constraint':>12} "
        f"{'build$M':>9} {'total$M':>9} {'ann$M/yr':>9}"
    )
    lines.append(f"  {'-' * 4} {'-' * 14} {'-' * 8} {'-' * 12} {'-' * 9} {'-' * 9} {'-' * 9}")
    for fy, py in _sorted_physical(output):
        for class_name in ("broadband", "direct_to_cell"):
            cls = getattr(py, class_name)
            cb = cls.cost_breakdown
            lines.append(
                f"  {fy:4d} "
                f"{class_name:>14} "
                f"{int(_num(cls.satellites_per_launch.value)):8d} "
                f"{str(cls.binding_constraint.value):>12} "
                f"{_num(cb.build_cost_after_learning.value):9.2f} "
                f"{_num(cb.satellite_total.value):9.2f} "
                f"{_num(cls.cost_annual_per_satellite_musd.value):9.2f}"
            )
        lines.append(
            f"  {'':>4} {'spectrum':>14} "
            f"req {_num(py.spectrum_to_acquire_mhz.value):.0f} MHz; "
            f"per-beam {_num(py.per_beam_capacity_mbps.value):.0f} Mbps "
            f"(naive cross-check {_num(py.naive_capacity_mbps.value):.0f} Mbps)"
        )
    return lines


def _render_fleet(output: CommsModelOutput) -> list[str]:
    """The per-year living-fleet rollup table."""
    lines: list[str] = []
    lines += _section_header("PER-YEAR FLEET ROLLUP (launches, deployed, living fleet, fleet $M)")
    lines.append("")
    lines.append(
        f"  {'FY':>4} {'launch':>7} {'bb_dep':>7} {'d2c_dep':>7} "
        f"{'bb_live':>7} {'d2c_live':>8} {'bb$M/yr':>9} {'d2c$M/yr':>9}"
    )
    lines.append(
        f"  {'-' * 4} {'-' * 7} {'-' * 7} {'-' * 7} {'-' * 7} {'-' * 8} {'-' * 9} {'-' * 9}"
    )
    for fy, by in _sorted_business(output):
        lines.append(
            f"  {fy:4d} "
            f"{int(_num(by.launches.value)):7d} "
            f"{int(_num(by.broadband_satellites_deployed_this_year.value)):7d} "
            f"{int(_num(by.direct_to_cell_satellites_deployed_this_year.value)):7d} "
            f"{int(_num(by.broadband_living_fleet.value)):7d} "
            f"{int(_num(by.direct_to_cell_living_fleet.value)):8d} "
            f"{_num(by.broadband_cost_annual_fleet_musd.value):9.1f} "
            f"{_num(by.direct_to_cell_cost_annual_fleet_musd.value):9.1f}"
        )
    return lines


def _render_customer_band(output: CommsModelOutput) -> list[str]:
    """The steady-state direct-to-cell customer band + cost band (the headline)."""
    lines: list[str] = []
    lines += _section_header("STEADY-STATE DIRECT-TO-CELL CUSTOMER + COST BAND (the headline)")
    lines.append("")
    by = _steady_state_business(output)
    if by is None:
        lines.append("  (steady-state year not in the business map for this run.)")
        return lines
    fy = output.metadata.steady_state_year
    served = by.total_served
    cost = by.cost_annual_per_customer_usd
    priced = by.priced_cost_per_customer_usd
    lines.append(f"  steady-state year:              FY{fy}")
    lines.append(
        f"  direct-to-cell living fleet:    {int(_num(by.direct_to_cell_living_fleet.value)):,} "
        f"satellites"
    )
    lines.append("")
    lines.append(
        f"  {'band member':>14} {'served (subs)':>16} {'cost $/yr':>12} {'priced $/yr':>12}"
    )
    lines.append(f"  {'-' * 14} {'-' * 16} {'-' * 12} {'-' * 12}")
    for member in ("low", "mid", "high"):
        lines.append(
            f"  {member:>14} "
            f"{int(_num(getattr(served, member).value)):16,d} "
            f"{_num(getattr(cost, member).value):12,.2f} "
            f"{_num(getattr(priced, member).value):12,.2f}"
        )
    lines.append("")
    lines.append(
        f"  ARPU-collectable ceiling:       "
        f"{_num(by.arpu_collectable_revenue_usd.value):,.2f} USD/yr per customer"
    )
    return lines


def _render_validation(output: CommsModelOutput) -> list[str]:
    """The engine-computed validation-check block (or a lean placeholder)."""
    lines: list[str] = []
    lines += _section_header("VALIDATION CHECKS")
    lines.append("")
    rules = output.meta.validation.rules
    if not rules:
        lines.append("  validation: (run via --json or --promote for the full rule set)")
        return lines
    for v in rules:
        mark = "PASS" if v.pass_check else f"FAIL ({v.severity.value})"
        lines.append(f"  [{mark:>14}] {v.name}: {v.what_it_tests}")
        lines.append(f"                  expected {v.expected}, got {v.computed}")
    return lines


def _render_comparison(ground_output: GroundReferenceOutput) -> list[str]:
    """The cost-to-cost comparison block: SPARSE and DENSE regimes side by side.

    Renders the per-regime ground vs space per-subscriber cost, the cost-to-cost
    ratio, the cheaper / undercut / capacity-binds flags, then the fleet-wide
    revenue-ceiling reconciliation and the Starlink-floor honesty figures. NUMBERS
    and FLAGS only, never a verdict string (the editorial verdict is Phase 6).

    Args:
        ground_output: The in-memory comms ground reference.

    Returns:
        The comparison-block report lines.
    """
    lines: list[str] = []
    lines += _section_header("COST-TO-COST COMPARISON (per density regime; NUMBERS and FLAGS only)")
    lines.append("")
    by_density = ground_output.comparison.by_density
    ground = ground_output.ground
    regimes = (
        ("SPARSE (unserved fresh-build)", by_density.sparse, ground.sparse),
        ("DENSE (incumbent marginal floor)", by_density.dense, ground.dense),
    )
    for label, regime, ground_regime in regimes:
        c2c = regime.cost_to_cost
        undercut = regime.price_undercut
        ground_cost = _num(ground_regime.cost_annual_per_subscriber_usd.value)
        space_cost = _num(c2c.space_cost_per_subscriber_usd.value)
        lines.append(f"  {label}")
        lines.append(f"    ground per-sub cost:     {ground_cost:,.2f} USD/yr")
        lines.append(f"    space per-customer cost: {space_cost:,.2f} USD/yr (mid)")
        lines.append(
            f"    cost-to-cost ratio:      "
            f"low {_num(c2c.space_to_ground_ratio_low.value):.2f} / "
            f"mid {_num(c2c.space_to_ground_ratio_mid.value):.2f} / "
            f"high {_num(c2c.space_to_ground_ratio_high.value):.2f}"
        )
        lines.append(
            f"    space cheaper here:      {_flag(c2c.space_is_cheaper.value)}; "
            f"undercut passes: {_flag(undercut.undercut_passes.value)}; "
            f"capacity binds: {_flag(regime.space_capacity_binds.value)}"
        )
        lines.append("")
    rc = ground_output.comparison.revenue_ceiling
    priced = _num(rc.priced_revenue_per_subscriber_usd.value)
    ceiling = _num(rc.arpu_collectable_revenue_usd.value)
    retail = _num(rc.retail_reference_usd_per_year.value)
    lines.append("  REVENUE-CEILING RECONCILIATION (fleet-wide)")
    lines.append(f"    priced revenue (cost x1.5):  {priced:,.2f} USD/yr")
    lines.append(f"    ARPU-collectable ceiling:    {ceiling:,.2f} USD/yr")
    lines.append(f"    retail reference:            {retail:,.2f} USD/yr")
    lines.append(
        f"    priced below collectable:    {_flag(rc.priced_below_collectable.value)}; "
        f"below retail: {_flag(rc.priced_below_retail.value)}; "
        f"collectable win: {_flag(rc.collectable_win.value)}"
    )
    lines.append("")
    sf = ground_output.comparison.starlink_floor
    chain_cost = _num(sf.bottom_up_chain_cost_usd_per_sub_year.value)
    floor_cost = _num(sf.disclosed_starlink_floor_usd_per_sub_year.value)
    lines.append("  STARLINK-FLOOR HONESTY (fleet-wide; both figures shown, no win claimed)")
    lines.append(f"    bottom-up chain cost:        {chain_cost:,.2f} USD/yr")
    lines.append(f"    disclosed Starlink floor:    {floor_cost:,.2f} USD/yr")
    lines.append(
        f"    chain below disclosed floor: {_flag(sf.chain_below_disclosed_floor.value)} "
        "(reported only; not claimed as a win)"
    )
    return lines


# ---------------------------------------------------------------------------
# Public entries.
# ---------------------------------------------------------------------------


def render_comms_text(
    output: CommsModelOutput,
    ground_output: GroundReferenceOutput | None = None,
) -> str:
    """Render a comms space-model output as a fixed-width monospaced report.

    Walks the typed :class:`CommsModelOutput` and emits the run identity, the
    provenance summary banner, the per-year per-class physical / cost table, the
    per-year living-fleet rollup, the steady-state customer + cost band (the
    headline), and the validation checks. When a
    :class:`communications.ground.GroundReferenceOutput` is supplied, ALSO renders
    the cost-to-cost comparison block (the per-regime ratio, the retail undercut,
    the revenue-ceiling reconciliation, and the Starlink-floor figures) as NUMBERS
    and FLAGS, never a verdict string. Every section is total: no ``KeyError``, no
    exception, no empty section.

    Args:
        output: The comms space-model output.
        ground_output: An optional ground reference; when supplied, the comparison
            block is appended.

    Returns:
        The report as a single newline-joined string.
    """
    lines: list[str] = []
    lines += _render_header(output)
    lines += _render_provenance_summary(output)
    lines += _render_year_physical(output)
    lines += _render_fleet(output)
    lines += _render_customer_band(output)
    lines += _render_validation(output)
    if ground_output is not None:
        lines += _render_comparison(ground_output)
    lines.append("")
    return "\n".join(lines)


def render_comms_headline(output: CommsModelOutput) -> str:
    """Render the one-line comms headline (the ``--brief`` output).

    A single line stating the steady-state year, the direct-to-cell living-fleet
    satellite count, and the steady-state served-customer MID band and per-customer
    cost MID band (the headline figures the founder leads with), customer-first.

    Args:
        output: The comms space-model output.

    Returns:
        A one-line headline string.
    """
    by = _steady_state_business(output)
    fy = output.metadata.steady_state_year
    if by is None:
        return f"Comms trajectory @ FY{fy}: (no steady-state year emitted)"
    living = int(_num(by.direct_to_cell_living_fleet.value))
    served_mid = int(_num(by.total_served.mid.value))
    cost_mid = _num(by.cost_annual_per_customer_usd.mid.value)
    return (
        f"Comms trajectory @ FY{fy}: "
        f"direct-to-cell living fleet {living:,} satellites; "
        f"served {served_mid:,} subscribers (mid); "
        f"cost ${cost_mid:,.2f}/customer/yr (mid)"
    )


__all__ = [
    "render_comms_headline",
    "render_comms_text",
]
