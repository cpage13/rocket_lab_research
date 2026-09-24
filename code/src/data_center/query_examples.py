"""Worked jq examples for the public space-model JSON.

The ``meta.query_examples`` block is the cold-reader contract: a new agent can
run these expressions against the promoted JSON and answer common questions
without reconstructing the schema from source code.

The examples that address one year address the run's anchor year
(:func:`data_center.config.anchor_year`, FY2036 for the default window), so
every example resolves against any valid run window. :func:`build_query_examples`
builds the fixed twelve-entry list for a given anchor year.
"""

from __future__ import annotations

import logging

from common.meta import QueryAppliesTo, QueryExample, ValidationSeverity

logger = logging.getLogger(__name__)


def build_query_examples(anchor_fy: int) -> list[QueryExample]:
    """Build the twelve worked jq examples for a run with the given anchor year.

    Args:
        anchor_fy: The run's anchor fiscal year (see
            :func:`data_center.config.anchor_year`); the single-year examples
            address it and carry it in their names and questions.

    Returns:
        The twelve :class:`QueryExample` entries, in their stable order.
    """
    year = str(anchor_fy)
    return [
        QueryExample(
            name="list_default_inputs_and_source_statuses",
            question_answered="Which default inputs were used, and how are they source-classed?",
            jq_expression=(
                ".inputs.assumption_index | to_entries | "
                "map({path: .key, value: .value.value, unit: .value.unit, "
                "source_status: .value.source_status})"
            ),
            expected_shape="list of {path, value, unit, source_status}",
            important_paths=["inputs.assumption_index"],
            applies_to=QueryAppliesTo.SPACE,
        ),
        QueryExample(
            name=f"deployed_year_capacity_{year}",
            question_answered=f"How much new orbital node power is deployed in {year}?",
            jq_expression=f'.business.years."{year}".kw_deployed_this_year.value',
            expected_shape="single number (kW/year)",
            important_paths=[f'business.years."{year}".kw_deployed_this_year'],
            applies_to=QueryAppliesTo.SPACE,
        ),
        QueryExample(
            name=f"deployed_vs_living_kw_{year}",
            question_answered=(
                f"How does {year} deployed-year power compare with living-fleet power?"
            ),
            jq_expression=(
                f'.business.years."{year}" | '
                "{deployed_kw: .kw_deployed_this_year.value, "
                "living_fleet_kw: .kw_living_fleet.value}"
            ),
            expected_shape="object {deployed_kw, living_fleet_kw}",
            important_paths=[
                f'business.years."{year}".kw_deployed_this_year',
                f'business.years."{year}".kw_living_fleet',
            ],
            applies_to=QueryAppliesTo.SPACE,
        ),
        QueryExample(
            name="validation_warnings",
            question_answered="Which validation results warn or fail?",
            jq_expression=(
                "[.meta.validation_results[] | "
                f'select(.severity != "{ValidationSeverity.OK.value}")]'
            ),
            expected_shape="zero or more validation result objects",
            important_paths=["meta.validation_results"],
            applies_to=QueryAppliesTo.SPACE,
        ),
        QueryExample(
            name="trace_launch_cost_assumption",
            question_answered="What supports the high-cadence launch-cost assumption?",
            jq_expression=(
                '.inputs.assumption_index["inputs.config.launch.high_cadence_cost_musd"]'
            ),
            expected_shape="InputCell object",
            important_paths=["inputs.config.launch.high_cadence_cost_musd"],
            applies_to=QueryAppliesTo.SPACE,
        ),
        QueryExample(
            name="trace_revenue_multiple_assumption",
            question_answered=(
                "What supports the central revenue multiple (its first anchor year)?"
            ),
            jq_expression=".inputs.config.revenue.central[0]",
            expected_shape="InputCell object",
            important_paths=["inputs.config.revenue.central"],
            applies_to=QueryAppliesTo.SPACE,
        ),
        QueryExample(
            name=f"headline_{year}_revenue_central",
            question_answered=f"What is total fleet revenue in {year}, central R case?",
            jq_expression=f'.business.years."{year}".revenue_annual_fleet_musd_central.value',
            expected_shape="single number (MUSD)",
            important_paths=[f'business.years."{year}".revenue_annual_fleet_musd_central'],
            applies_to=QueryAppliesTo.SPACE,
        ),
        QueryExample(
            name=f"headline_{year}_profit_central",
            question_answered=f"What is {year} fleet annual gross profit, central R case?",
            jq_expression=(
                f'.business.years."{year}".gross_profit_annual_fleet_musd_central.value'
            ),
            expected_shape="single number (MUSD)",
            important_paths=[f'business.years."{year}".gross_profit_annual_fleet_musd_central'],
            applies_to=QueryAppliesTo.SPACE,
        ),
        QueryExample(
            name=f"margin_band_{year}",
            question_answered=f"What is {year} gross margin under low, central, and high R?",
            jq_expression=(
                f'.business.years."{year}" | '
                "{central: .margin_central_pct.value, low: .margin_low_pct.value, "
                "high: .margin_high_pct.value}"
            ),
            expected_shape="object {central, low, high}",
            important_paths=[
                f'business.years."{year}".margin_central_pct',
                f'business.years."{year}".margin_low_pct',
                f'business.years."{year}".margin_high_pct',
            ],
            applies_to=QueryAppliesTo.SPACE,
        ),
        QueryExample(
            name="trajectory_launches",
            question_answered="What launch cadence does the model emit each year?",
            jq_expression=(
                "[.business.years | to_entries[] | "
                "{fy: (.key|tonumber), launches: .value.launches.value}]"
            ),
            expected_shape="list of {fy, launches}",
            important_paths=["business.years"],
            applies_to=QueryAppliesTo.SPACE,
        ),
        QueryExample(
            name="living_fleet_per_year",
            question_answered="How many active nodes are in the living fleet each year?",
            jq_expression=(
                "[.business.years | to_entries[] | "
                "{fy: (.key|tonumber), living: .value.living_fleet.value}]"
            ),
            expected_shape="list of {fy, living}",
            important_paths=["business.years"],
            applies_to=QueryAppliesTo.SPACE,
        ),
        QueryExample(
            name="trace_a_cell",
            question_answered="How can a user inspect one computed cell's provenance?",
            jq_expression=f'.business.years."{year}".revenue_annual_fleet_musd_central',
            expected_shape="{value, unit, formula, formula_name, uses, sources, source_status}",
            important_paths=[f'business.years."{year}".revenue_annual_fleet_musd_central'],
            applies_to=QueryAppliesTo.SPACE,
        ),
    ]


__all__ = ["build_query_examples"]
