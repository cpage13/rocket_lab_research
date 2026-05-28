"""Worked jq examples for the public space-model JSON.

The ``meta.query_examples`` block is the cold-reader contract: a new agent can
run these expressions against the promoted JSON and answer common questions
without reconstructing the schema from source code.
"""

from __future__ import annotations

import logging
from typing import Final

from data_center.output import QueryAppliesTo, QueryExample

logger = logging.getLogger(__name__)

TARGET_YEAR: Final[str] = "2036"
"""Default target year used by the public query examples."""

QUERY_EXAMPLES: Final[list[QueryExample]] = [
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
        name="deployed_year_capacity_2036",
        question_answered="How much new orbital node power is deployed in 2036?",
        jq_expression=f'.business.years."{TARGET_YEAR}".kw_deployed_this_year.value',
        expected_shape="single number (kW/year)",
        important_paths=[f'business.years."{TARGET_YEAR}".kw_deployed_this_year'],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="deployed_vs_living_kw_2036",
        question_answered="How does 2036 deployed-year power compare with living-fleet power?",
        jq_expression=(
            f'.business.years."{TARGET_YEAR}" | '
            "{deployed_kw: .kw_deployed_this_year.value, "
            "living_fleet_kw: .kw_living_fleet.value}"
        ),
        expected_shape="object {deployed_kw, living_fleet_kw}",
        important_paths=[
            f'business.years."{TARGET_YEAR}".kw_deployed_this_year',
            f'business.years."{TARGET_YEAR}".kw_living_fleet',
        ],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="validation_warnings",
        question_answered="Which validation results warn or fail?",
        jq_expression='[.meta.validation_results[] | select(.severity != "pass")]',
        expected_shape="zero or more validation result objects",
        important_paths=["meta.validation_results"],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="trace_launch_cost_assumption",
        question_answered="What supports the high-cadence launch-cost assumption?",
        jq_expression=('.inputs.assumption_index["inputs.config.launch.high_cadence_cost_musd"]'),
        expected_shape="InputCell object",
        important_paths=["inputs.config.launch.high_cadence_cost_musd"],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="trace_revenue_multiple_assumption",
        question_answered="What supports the default central revenue multiple?",
        jq_expression=(
            ".inputs.config.revenue.central[] | select(.path == "
            '"inputs.config.revenue.central.2026")'
        ),
        expected_shape="InputCell object",
        important_paths=["inputs.config.revenue.central"],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="headline_2036_revenue_central",
        question_answered="What is total fleet revenue in 2036, central R case?",
        jq_expression=f'.business.years."{TARGET_YEAR}".revenue_annual_fleet_musd_central.value',
        expected_shape="single number (MUSD)",
        important_paths=[f'business.years."{TARGET_YEAR}".revenue_annual_fleet_musd_central'],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="headline_2036_profit_central",
        question_answered="What is 2036 fleet annual gross profit, central R case?",
        jq_expression=(
            f'.business.years."{TARGET_YEAR}".gross_profit_annual_fleet_musd_central.value'
        ),
        expected_shape="single number (MUSD)",
        important_paths=[f'business.years."{TARGET_YEAR}".gross_profit_annual_fleet_musd_central'],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="margin_band_2036",
        question_answered="What is 2036 gross margin under low, central, and high R?",
        jq_expression=(
            f'.business.years."{TARGET_YEAR}" | '
            "{central: .margin_central_pct.value, low: .margin_low_pct.value, "
            "high: .margin_high_pct.value}"
        ),
        expected_shape="object {central, low, high}",
        important_paths=[
            f'business.years."{TARGET_YEAR}".margin_central_pct',
            f'business.years."{TARGET_YEAR}".margin_low_pct',
            f'business.years."{TARGET_YEAR}".margin_high_pct',
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
        jq_expression=f'.business.years."{TARGET_YEAR}".revenue_annual_fleet_musd_central',
        expected_shape="{value, unit, formula, formula_name, uses, sources, source_status}",
        important_paths=[f'business.years."{TARGET_YEAR}".revenue_annual_fleet_musd_central'],
        applies_to=QueryAppliesTo.SPACE,
    ),
]

__all__ = ["QUERY_EXAMPLES"]
