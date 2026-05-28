"""Draft Markdown summary rendering for data-center model outputs.

The JSON artifact is the machine-readable source of truth, and
``data_center/conclusion.md`` is reviewed static prose. This module can render
a noncanonical Markdown draft from a typed
:class:`data_center.output.ValuationOutput` for local review or scratch use.
"""

from __future__ import annotations

import logging

from .output import BusinessYear, PhysicalYear, ValuationOutput
from .provenance import ProvenanceCell

_LOGGER = logging.getLogger(__name__)

MUSD_PER_BUSD = 1_000.0
"""Millions of USD in one billion USD, used only for display formatting."""

DECIMAL_PLACES_WHOLE = 0
"""Display precision for large whole-number model quantities."""

DECIMAL_PLACES_STANDARD = 1
"""Display precision for ordinary scalar quantities."""

DECIMAL_PLACES_BUSD = 2
"""Display precision for billion-dollar headline quantities."""


def _numeric_value(cell: ProvenanceCell) -> float:
    """Return a provenance cell's numeric value as ``float``.

    Args:
        cell: A provenance cell expected to carry an ``int`` or ``float``.

    Raises:
        TypeError: If the cell carries a non-numeric value.
    """
    value = cell.value
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise TypeError(f"expected numeric provenance cell, got {type(value).__name__}")
    return float(value)


def _text_value(cell: ProvenanceCell) -> str:
    """Return a provenance cell's value as human-readable text."""
    return str(cell.value)


def _year_key(output: ValuationOutput) -> str:
    """Return the terminal fiscal year key for the output horizon."""
    return str(output.metadata.base_year + output.metadata.horizon_years)


def _busd(musd: float) -> str:
    """Format millions of dollars as billions of dollars."""
    return f"${musd / MUSD_PER_BUSD:,.{DECIMAL_PLACES_BUSD}f}B"


def _musd(musd: float) -> str:
    """Format millions of dollars."""
    return f"${musd:,.{DECIMAL_PLACES_STANDARD}f}M"


def _count(value: float) -> str:
    """Format a count-like model quantity."""
    return f"{value:,.{DECIMAL_PLACES_WHOLE}f}"


def _one_decimal(value: float) -> str:
    """Format a scalar with one decimal place."""
    return f"{value:,.{DECIMAL_PLACES_STANDARD}f}"


def render_conclusion_markdown(
    output: ValuationOutput,
    *,
    model_path: str,
    scenario_path: str,
) -> str:
    """Render a noncanonical Markdown draft for one model output.

    Args:
        output: The typed valuation output to summarize.
        model_path: Repository-relative path to the JSON artifact this draft
            describes.
        scenario_path: Repository-relative path to the YAML scenario used to
            generate the output.

    Returns:
        A Markdown document ending with a single trailing newline.
    """
    fy = _year_key(output)
    physical: PhysicalYear = output.physical.years[fy]
    business: BusinessYear = output.business.years[fy]

    failed_rules = [rule.name for rule in output.meta.validation.rules if not rule.pass_check]
    validation_summary = (
        "all validation checks pass"
        if not failed_rules
        else f"validation has failing checks: {', '.join(failed_rules)}"
    )

    scenario_name = output.metadata.scenario_name
    revenue = _numeric_value(business.revenue_annual_fleet_musd_central)
    profit = _numeric_value(business.gross_profit_annual_fleet_musd_central)
    cumulative_revenue = _numeric_value(business.revenue_cumulative_musd_central)
    margin = _numeric_value(business.margin_central_pct)
    launches = int(_numeric_value(business.launches))
    living_fleet = _numeric_value(business.living_fleet)
    node_power = _numeric_value(physical.kw_per_node)
    packages = _numeric_value(physical.gpus_per_node)
    node_cost = _numeric_value(physical.cost_breakdown.node_total)
    generation = _text_value(physical.frontier_generation)
    binding_constraint = _text_value(physical.binding_constraint)
    mass_envelope = output.inputs.gospel.get("mass_envelope_t")

    lines = [
        f"# Data Center Preliminary Conclusion - {scenario_name}",
        "",
        "This file is a noncanonical Markdown draft for one data-center model",
        "run. The JSON remains the machine-readable source of truth, and",
        "`data_center/conclusion.md` remains the reviewed static conclusion.",
        "",
        "## Source",
        "",
        f"- Model JSON: `{model_path}`",
        f"- Scenario YAML: `{scenario_path}`",
        f"- Schema: `{output.metadata.schema_version}`",
        f"- Generated: `{output.metadata.generated_at}`",
        f"- Validation: {validation_summary}",
        "",
        f"## Headline {fy} Numbers",
        "",
        f"- Frontier generation: {generation}",
        f"- Packages per node: {_count(packages)}",
        f"- Node power: {_one_decimal(node_power)} kW",
        f"- Node build + launch cost: {_musd(node_cost)}",
        f"- Launches in {fy}: {_count(launches)}",
        f"- Living fleet: {_count(living_fleet)} nodes",
        f"- Annual fleet revenue, central R band: {_busd(revenue)}",
        f"- Annual fleet gross profit, central R band: {_busd(profit)}",
        f"- Annual fleet gross margin, central R band: {_one_decimal(margin)}%",
        f"- Cumulative revenue through {fy}, central R band: {_busd(cumulative_revenue)}",
        f"- Binding physical constraint: {binding_constraint}",
        "",
        "## Interpretation",
        "",
        "The default model describes an owner-operated orbital inference fleet",
        "where revenue is coupled to cost through the R band: R is the revenue",
        "multiple applied to annualized cost, so R=1.40 implies a 28.6% gross",
        f"margin. The promoted default uses a {mass_envelope} t block-upgraded",
        "reusable-Neutron SSO",
        "mass-envelope scenario; that mass envelope is a scenario assumption,",
        "not a published Rocket Lab SSO payload. The model is mass-bound rather",
        "than volume-bound: the JSON should be queried for the full year-by-year",
        "physical trajectory before treating a headline number as a decision.",
        "",
        "## Caveats",
        "",
        "- This draft is not research evidence and is not the reviewed static conclusion.",
        "- The 12.5 t mass envelope is tied to SOURCE_INDEX NTR-007, a block-upgrade scenario.",
        "- The JSON is authoritative and carries formulas, units, upstream inputs,",
        "  sources, and query examples.",
        "- DCF, enterprise value, free cash flow, and terminal valuation are outside",
        "  this model's scope.",
        "",
        "## Query The Model",
        "",
        "The JSON embeds agent-ready `jq` examples at `meta.query_examples`.",
        "For example:",
        "",
        "```sh",
        f"jq '.business.years.\"{fy}\".revenue_annual_fleet_musd_central.value' {model_path}",
        f"jq '.meta.query_examples[] | {{name, jq_expression}}' {model_path}",
        "```",
        "",
    ]
    return "\n".join(lines)
