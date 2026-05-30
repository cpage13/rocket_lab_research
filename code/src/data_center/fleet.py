"""Fleet rollup: cohort vintaging under the service-life cliff + R-band aggregation.

A cohort is the set of nodes launched in a given calendar year. Each
cohort carries its launch-year gen-mix (frontier_generation),
per-node revenue/cost, and lifetime (service_life_years, default 5 per D1).

See `research/SOURCE_INDEX.md` for claim IDs and the code README for the
current algorithmic contract.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict

from data_center.config import RBand, YearRValue
from data_center.provenance import FieldPath, ProvenanceCell, cell

logger = logging.getLogger(__name__)


class Cohort(BaseModel):
    """All nodes launched in a single calendar year.

    Attributes:
        launch_year: The calendar year this cohort was launched.
        nodes_deployed: Number of nodes in this cohort.
        frontier_generation: The frontier GPU generation at launch year.
        kw_per_node: Per-node electrical power, kW (fixed at launch).
        pf_per_node: Per-node compute, PFLOPS (fixed at launch).
        cost_annual_per_node_musd: Annualized per-node cost, $M.
        rev_per_node_musd_central: Per-node annual revenue at central R.
        rev_per_node_musd_low: Per-node annual revenue at low R.
        rev_per_node_musd_high: Per-node annual revenue at high R.
    """

    model_config = ConfigDict(frozen=True)
    launch_year: int
    nodes_deployed: int
    frontier_generation: str
    kw_per_node: float
    pf_per_node: float
    cost_annual_per_node_musd: float
    # Per-node revenue derived from cost x R_at_launch_year per band; stored
    # as triple at construction to avoid recomputing.
    rev_per_node_musd_central: float
    rev_per_node_musd_low: float
    rev_per_node_musd_high: float

    def is_alive_at(self, year: int, service_life: int) -> bool:
        """True iff this cohort is still within the service-life cliff at ``year``.

        Args:
            year: The calendar year to test.
            service_life: Node operating life in years (the hard cliff, D1).
                Required, no default: callers pass the scenario's
                ``fleet.service_life_years`` so the cliff tracks the configured
                life and cannot silently fall back to a constant.

        Returns:
            ``True`` if ``launch_year <= year < launch_year + service_life``.
        """
        return self.launch_year <= year < self.launch_year + service_life


def _r_at_year(anchors: list[YearRValue], year: int) -> float:
    """Linear interpolation between R-band anchors.

    Args:
        anchors: The R-band trajectory's anchors, sorted by ``fy`` ascending.
        year: The calendar year at which to evaluate R.

    Returns:
        The R value at ``year``: clamped flat outside the anchor range,
        linearly interpolated between adjacent anchors otherwise.
    """
    if year <= anchors[0].fy:
        return anchors[0].r
    if year >= anchors[-1].fy:
        return anchors[-1].r
    for i in range(len(anchors) - 1):
        a, b = anchors[i], anchors[i + 1]
        if a.fy <= year <= b.fy:
            frac = (year - a.fy) / (b.fy - a.fy)
            return a.r + frac * (b.r - a.r)
    return anchors[-1].r  # unreachable


def r_at_year(r_band: RBand, year: int) -> tuple[float, float, float]:
    """Return (central, low, high) R values at ``year``.

    Args:
        r_band: The three-trajectory R band.
        year: The calendar year at which to evaluate each trajectory.

    Returns:
        A ``(central, low, high)`` tuple of interpolated R values.
    """
    return (
        _r_at_year(r_band.central, year),
        _r_at_year(r_band.low, year),
        _r_at_year(r_band.high, year),
    )


@dataclass(frozen=True)
class FleetYear:
    """Per-year fleet rollup. All ProvenanceCells.

    Attributes:
        year: Calendar year for this fleet record.
        launches: Launches in this calendar year.
        nodes_deployed_this_year: Nodes deployed this year (1 per launch, D8).
        living_fleet: Living fleet count under the 5-year cliff (D1).
        kw_deployed_this_year: Newly deployed node power this year.
        kw_living_fleet: Living-fleet node power this year.
        kw_on_orbit: Total kW on orbit (living fleet).
        pf_deployed_this_year: Newly deployed node compute this year.
        pf_living_fleet: Living-fleet node compute this year.
        pf_on_orbit: Total PFLOPS on orbit (living fleet).
        launch_cost_this_year_musd: Per-launch cost at this year's cadence.
        cost_annual_fleet_musd: Fleet annual cost (cohort-vintaged).
        revenue_annual_fleet_musd_central: Fleet annual revenue, central R.
        revenue_annual_fleet_musd_low: Fleet annual revenue, low R.
        revenue_annual_fleet_musd_high: Fleet annual revenue, high R.
        revenue_cumulative_musd_central: Cumulative revenue, central R.
        revenue_cumulative_musd_low: Cumulative revenue, low R.
        revenue_cumulative_musd_high: Cumulative revenue, high R.
        gross_profit_annual_fleet_musd_central: Fleet gross profit, central R.
        gross_profit_annual_fleet_musd_low: Fleet gross profit, low R.
        gross_profit_annual_fleet_musd_high: Fleet gross profit, high R.
        margin_central_pct: Fleet gross margin, central R.
        margin_low_pct: Fleet gross margin, low R.
        margin_high_pct: Fleet gross margin, high R.
    """

    year: int
    launches: ProvenanceCell
    nodes_deployed_this_year: ProvenanceCell
    living_fleet: ProvenanceCell
    kw_deployed_this_year: ProvenanceCell
    kw_living_fleet: ProvenanceCell
    kw_on_orbit: ProvenanceCell
    pf_deployed_this_year: ProvenanceCell
    pf_living_fleet: ProvenanceCell
    pf_on_orbit: ProvenanceCell
    launch_cost_this_year_musd: ProvenanceCell
    cost_annual_fleet_musd: ProvenanceCell
    revenue_annual_fleet_musd_central: ProvenanceCell
    revenue_annual_fleet_musd_low: ProvenanceCell
    revenue_annual_fleet_musd_high: ProvenanceCell
    revenue_cumulative_musd_central: ProvenanceCell
    revenue_cumulative_musd_low: ProvenanceCell
    revenue_cumulative_musd_high: ProvenanceCell
    gross_profit_annual_fleet_musd_central: ProvenanceCell
    gross_profit_annual_fleet_musd_low: ProvenanceCell
    gross_profit_annual_fleet_musd_high: ProvenanceCell
    margin_central_pct: ProvenanceCell
    margin_low_pct: ProvenanceCell
    margin_high_pct: ProvenanceCell


def compute_fleet_year(
    year: int,
    cohorts: list[Cohort],
    launches_this_year: int,
    launch_cost_musd: float,
    prev_cumulative_revenue_central_musd: float = 0.0,
    prev_cumulative_revenue_low_musd: float = 0.0,
    prev_cumulative_revenue_high_musd: float = 0.0,
    *,
    service_life_years: int,
    year_path: FieldPath,
) -> FleetYear:
    """Compose fleet rollup for one calendar year.

    Living cohorts are those with launch_year in
    ``[year - (service_life_years - 1), year]`` under the service-life hard
    cliff (D1). Per-cohort kW / PFLOPS / cost /
    revenue are summed over the living set; gross profit and margin
    follow; cumulative revenue extends the prior-year running total.

    Args:
        year: The calendar year of this rollup.
        cohorts: All cohorts launched so far (the function filters to the
            living set itself).
        launches_this_year: Whole-number launches in ``year`` (from the
            cadence model).
        launch_cost_musd: Per-launch cost at ``year``'s cadence.
        prev_cumulative_revenue_central_musd: Cumulative revenue through the
            prior year, central R.
        prev_cumulative_revenue_low_musd: Cumulative revenue through the
            prior year, low R.
        prev_cumulative_revenue_high_musd: Cumulative revenue through the
            prior year, high R.
        service_life_years: Node operating life in years (the hard cliff, D1),
            threaded from ``config.fleet.service_life_years``. Passed
            explicitly (no default) so the living set tracks the configured
            life.
        year_path: JSON path of this fleet-year block.

    Returns:
        A :class:`FleetYear` of provenance cells.
    """
    if isinstance(launches_this_year, bool) or not isinstance(launches_this_year, int):
        raise TypeError("launches_this_year must be an integer mission count")

    living = [c for c in cohorts if c.is_alive_at(year, service_life_years)]
    deployed = [c for c in cohorts if c.launch_year == year]
    living_count = sum(c.nodes_deployed for c in living)

    deployed_kw = sum(c.nodes_deployed * c.kw_per_node for c in deployed)
    deployed_pf = sum(c.nodes_deployed * c.pf_per_node for c in deployed)
    kw = sum(c.nodes_deployed * c.kw_per_node for c in living)
    pf = sum(c.nodes_deployed * c.pf_per_node for c in living)
    cost = sum(c.nodes_deployed * c.cost_annual_per_node_musd for c in living)
    rev_c = sum(c.nodes_deployed * c.rev_per_node_musd_central for c in living)
    rev_l = sum(c.nodes_deployed * c.rev_per_node_musd_low for c in living)
    rev_h = sum(c.nodes_deployed * c.rev_per_node_musd_high for c in living)
    gp_c = rev_c - cost
    gp_l = rev_l - cost
    gp_h = rev_h - cost
    margin_c = (gp_c / rev_c * 100.0) if rev_c > 0 else 0.0
    margin_l = (gp_l / rev_l * 100.0) if rev_l > 0 else 0.0
    margin_h = (gp_h / rev_h * 100.0) if rev_h > 0 else 0.0
    cumul_c = prev_cumulative_revenue_central_musd + rev_c
    cumul_l = prev_cumulative_revenue_low_musd + rev_l
    cumul_h = prev_cumulative_revenue_high_musd + rev_h

    # Cell-to-cell back-pointers. Every fleet cell is a cohort rollup of
    # the per-node physical trajectory, so its `uses` cite the specific
    # upstream cells it sums — the matching per-node `physical.years` cell
    # plus the `living_fleet` count — never the bare year container.
    phys_path = f'physical.years."{year}"'

    return FleetYear(
        year=year,
        launches=cell(
            value=launches_this_year,
            unit="count",
            formula_name="launches_per_year_from_logistic",
            uses=[
                "inputs.config.cadence.cadence_ceiling",
                "inputs.config.cadence.launches_at_year_5",
                "inputs.config.cadence.launches_at_year_10",
                "inputs.config.cadence.first_launch_year",
            ],
            sources=[
                "research/SOURCE_INDEX.md#NTR-010",
                "research/rocket_lab/neutron/launch_cost_economics.md",
            ],
            description=f"Whole-number launches in {year}.",
        ),
        nodes_deployed_this_year=cell(
            value=launches_this_year,
            unit="count",
            formula_name="nodes_deployed_this_year_from_launches",
            uses=[f"{year_path}.launches"],
            sources=["D8 1 node per launch"],
            description=f"Nodes deployed in {year}.",
        ),
        living_fleet=cell(
            value=living_count,
            unit="count",
            formula_name="living_fleet_from_cohort_cliff",
            uses=[
                f"{year_path}.nodes_deployed_this_year",
                "inputs.config.fleet.service_life_years",
            ],
            sources=[
                "research/SOURCE_INDEX.md#THR-008",
                "cohort sum over living vintages",
            ],
            description=f"Living fleet count at {year}.",
        ),
        kw_deployed_this_year=cell(
            value=deployed_kw,
            unit="kW",
            formula_name="kw_deployed_this_year_from_nodes",
            uses=[f"{year_path}.nodes_deployed_this_year", f"{phys_path}.kw_per_node"],
            sources=["deployment-year cohort power rollup"],
            description=f"Newly deployed kW in {year}.",
        ),
        kw_living_fleet=cell(
            value=kw,
            unit="kW",
            formula_name="kw_on_orbit_from_living_fleet",
            uses=[f"{year_path}.living_fleet", f"{phys_path}.kw_per_node"],
            sources=["cohort rollup of physical.years per-node kw_per_node"],
            description=f"Living-fleet kW at {year}.",
        ),
        kw_on_orbit=cell(
            value=kw,
            unit="kW",
            formula_name="kw_on_orbit_from_living_fleet",
            uses=[f"{year_path}.living_fleet", f"{phys_path}.kw_per_node"],
            sources=["cohort rollup of physical.years per-node kw_per_node"],
            description=f"Total kW on orbit at {year}.",
        ),
        pf_deployed_this_year=cell(
            value=deployed_pf,
            unit="PFLOPS",
            formula_name="pf_deployed_this_year_from_nodes",
            uses=[f"{year_path}.nodes_deployed_this_year", f"{phys_path}.pf_per_node"],
            sources=["deployment-year cohort compute rollup"],
            description=f"Newly deployed PFLOPS in {year}.",
        ),
        pf_living_fleet=cell(
            value=pf,
            unit="PFLOPS",
            formula_name="pf_on_orbit_from_living_fleet",
            uses=[f"{year_path}.living_fleet", f"{phys_path}.pf_per_node"],
            sources=["cohort rollup of physical.years per-node pf_per_node"],
            description=f"Living-fleet PFLOPS at {year}.",
        ),
        pf_on_orbit=cell(
            value=pf,
            unit="PFLOPS",
            formula_name="pf_on_orbit_from_living_fleet",
            uses=[f"{year_path}.living_fleet", f"{phys_path}.pf_per_node"],
            sources=["cohort rollup of physical.years per-node pf_per_node"],
            description=f"Total PFLOPS on orbit at {year}.",
        ),
        launch_cost_this_year_musd=cell(
            value=launch_cost_musd,
            unit="MUSD",
            formula_name="launch_cost_musd_from_cadence_log_linear",
            uses=[
                f"{year_path}.launches",
                "inputs.config.launch.low_cadence_cost_musd",
                "inputs.config.launch.high_cadence_cost_musd",
            ],
            sources=[
                "research/SOURCE_INDEX.md#NTR-009",
                "inputs.config.launch dials",
            ],
            description=f"Launch $/launch at {year} cadence.",
        ),
        cost_annual_fleet_musd=cell(
            value=cost,
            unit="MUSD",
            formula_name="cost_annual_fleet_from_cohorts",
            uses=[f"{year_path}.living_fleet", f"{phys_path}.cost_annual_per_node_musd"],
            sources=["cohort rollup of physical.years per-node cost_annual_per_node_musd"],
            description=f"Fleet annual cost at {year}.",
        ),
        revenue_annual_fleet_musd_central=cell(
            value=rev_c,
            unit="MUSD",
            formula_name="revenue_annual_fleet_from_cohorts",
            uses=[
                f"{year_path}.living_fleet",
                f"{phys_path}.revenue_annual_per_node_musd_central",
                "inputs.config.revenue.central[]",
            ],
            sources=[
                "research/SOURCE_INDEX.md#REV-008",
                "cohort rollup of per-node central revenue",
            ],
            description=f"Fleet annual revenue at {year}, central R.",
        ),
        revenue_annual_fleet_musd_low=cell(
            value=rev_l,
            unit="MUSD",
            formula_name="revenue_annual_fleet_from_cohorts",
            uses=[
                f"{year_path}.living_fleet",
                f"{phys_path}.revenue_annual_per_node_musd_low",
                "inputs.config.revenue.low[]",
            ],
            sources=[
                "research/SOURCE_INDEX.md#REV-008",
                "cohort rollup of per-node low revenue",
            ],
            description=f"Fleet annual revenue at {year}, low R.",
        ),
        revenue_annual_fleet_musd_high=cell(
            value=rev_h,
            unit="MUSD",
            formula_name="revenue_annual_fleet_from_cohorts",
            uses=[
                f"{year_path}.living_fleet",
                f"{phys_path}.revenue_annual_per_node_musd_high",
                "inputs.config.revenue.high[]",
            ],
            sources=[
                "research/SOURCE_INDEX.md#REV-008",
                "cohort rollup of per-node high revenue",
            ],
            description=f"Fleet annual revenue at {year}, high R.",
        ),
        revenue_cumulative_musd_central=cell(
            value=cumul_c,
            unit="MUSD",
            formula_name="revenue_cumulative_fleet_from_annuals",
            uses=[f"{year_path}.revenue_annual_fleet_musd_central"],
            sources=["running sum of revenue_annual_fleet_musd_central"],
            description=f"Cumulative revenue {year} (central).",
        ),
        revenue_cumulative_musd_low=cell(
            value=cumul_l,
            unit="MUSD",
            formula_name="revenue_cumulative_fleet_from_annuals",
            uses=[f"{year_path}.revenue_annual_fleet_musd_low"],
            sources=["running sum of revenue_annual_fleet_musd_low"],
            description=f"Cumulative revenue {year} (low).",
        ),
        revenue_cumulative_musd_high=cell(
            value=cumul_h,
            unit="MUSD",
            formula_name="revenue_cumulative_fleet_from_annuals",
            uses=[f"{year_path}.revenue_annual_fleet_musd_high"],
            sources=["running sum of revenue_annual_fleet_musd_high"],
            description=f"Cumulative revenue {year} (high).",
        ),
        gross_profit_annual_fleet_musd_central=cell(
            value=gp_c,
            unit="MUSD",
            formula_name="gross_profit_annual_fleet_from_rev_and_cost",
            uses=[
                f"{year_path}.revenue_annual_fleet_musd_central",
                f"{year_path}.cost_annual_fleet_musd",
            ],
            sources=["fleet revenue minus fleet cost (central R)"],
            description=f"Fleet annual gross profit {year} central.",
        ),
        gross_profit_annual_fleet_musd_low=cell(
            value=gp_l,
            unit="MUSD",
            formula_name="gross_profit_annual_fleet_from_rev_and_cost",
            uses=[
                f"{year_path}.revenue_annual_fleet_musd_low",
                f"{year_path}.cost_annual_fleet_musd",
            ],
            sources=["fleet revenue minus fleet cost (low R)"],
            description=f"Fleet annual gross profit {year} low.",
        ),
        gross_profit_annual_fleet_musd_high=cell(
            value=gp_h,
            unit="MUSD",
            formula_name="gross_profit_annual_fleet_from_rev_and_cost",
            uses=[
                f"{year_path}.revenue_annual_fleet_musd_high",
                f"{year_path}.cost_annual_fleet_musd",
            ],
            sources=["fleet revenue minus fleet cost (high R)"],
            description=f"Fleet annual gross profit {year} high.",
        ),
        margin_central_pct=cell(
            value=margin_c,
            unit="percent",
            formula_name="margin_pct_from_rev_and_cost",
            uses=[
                f"{year_path}.gross_profit_annual_fleet_musd_central",
                f"{year_path}.revenue_annual_fleet_musd_central",
            ],
            sources=["fleet gross profit over fleet revenue (central R)"],
            description=f"Margin {year} central R.",
        ),
        margin_low_pct=cell(
            value=margin_l,
            unit="percent",
            formula_name="margin_pct_from_rev_and_cost",
            uses=[
                f"{year_path}.gross_profit_annual_fleet_musd_low",
                f"{year_path}.revenue_annual_fleet_musd_low",
            ],
            sources=["fleet gross profit over fleet revenue (low R)"],
            description=f"Margin {year} low R.",
        ),
        margin_high_pct=cell(
            value=margin_h,
            unit="percent",
            formula_name="margin_pct_from_rev_and_cost",
            uses=[
                f"{year_path}.gross_profit_annual_fleet_musd_high",
                f"{year_path}.revenue_annual_fleet_musd_high",
            ],
            sources=["fleet gross profit over fleet revenue (high R)"],
            description=f"Margin {year} high R.",
        ),
    )


__all__ = [
    "Cohort",
    "FleetYear",
    "compute_fleet_year",
    "r_at_year",
]
