"""The product case's entry (``product_case.engine``, B5): a run carries its state to the end.

Named ``test_run_product_case.py``, not ``test_engine.py``, a basename the data-center and
communications test packages share. Each test names what it exercises, its sample and what counts
as success.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from common.meta import ValidationSeverity
from product_case.config import load_product_case_config
from product_case.constants import ProductClass, RunState, UsableTest
from product_case.engine import most_failed_test, run_product_case
from product_case.engineering import EngineeringView, engineering_view_from_bytes


def _view(
    synthetic_engineering: dict[str, Any],
    as_engineering_bytes: Callable[[dict[str, Any]], bytes],
    synthetic_reported_years: tuple[int, ...],
) -> EngineeringView:
    """The synthetic artifact's engineering view of FY2031 to FY2033."""
    return engineering_view_from_bytes(
        as_engineering_bytes(synthetic_engineering),
        path="synthetic.json",
        reported_years=synthetic_reported_years,
    )


def test_a_synthetic_run_reaches_a_pick_with_a_headline_and_spreads(
    synthetic_scenario: dict[str, Any],
    write_scenario: Callable[[dict[str, Any]], Path],
    synthetic_engineering: dict[str, Any],
    as_engineering_bytes: Callable[[dict[str, Any]], bytes],
    synthetic_reported_years: tuple[int, ...],
) -> None:
    """Objective: a run composes the offers, the Monte Carlo and the checks and ends ``picked``,
    with a pick at the start prices, a headline, spreads and every invariant held.

    Sample: the synthetic artifact (FY2031 to FY2033, round numbers) and the small scenario (16
    choices, 4 candidates, 50 draws).

    Expected outcome: state ``picked``; 16 summaries; the pick a candidate on the candidates'
    front; a headline and spreads of three years, the headline's classes in class order; the
    invariants first among the validation results, each ``pass``; no result a failure.
    """
    config = load_product_case_config(write_scenario(synthetic_scenario))
    run = run_product_case(
        config, _view(synthetic_engineering, as_engineering_bytes, synthetic_reported_years)
    )
    assert run.state is RunState.PICKED
    assert len(run.choices) == 16
    assert run.pick is not None and run.headline is not None and run.spreads is not None
    picked = run.choices[run.pick.choice_id].choice
    assert picked.at_start_prices and run.pick.choice_id in run.fronts.at_start_prices
    assert [year.year for year in run.headline.years] == list(synthetic_reported_years)
    assert [entry.product_class for entry in run.headline.years[0].classes] == list(ProductClass)
    assert [year.year for year in run.spreads.years] == list(synthetic_reported_years)
    invariants = [r for r in run.validation_results if r.validation_id.startswith("invariant.")]
    assert len(invariants) == 7 and all(r.severity is ValidationSeverity.OK for r in invariants)
    assert run.validation_results[: len(invariants)] == tuple(invariants)
    assert ValidationSeverity.FAIL not in {r.severity for r in run.validation_results}
    assert run.headline_failing_tests == run.headline.failing_tests


def test_no_usable_candidate_runs_to_no_usable_choice_raising_nothing(
    synthetic_scenario: dict[str, Any],
    write_scenario: Callable[[dict[str, Any]], Path],
    synthetic_engineering: dict[str, Any],
    as_engineering_bytes: Callable[[dict[str, Any]], bytes],
    synthetic_reported_years: tuple[int, ...],
) -> None:
    """Objective: when no candidate is usable in any draw the run ends ``no_usable_choice`` with
    no pick, headline, spreads or checks, a state carried to the end, never an exception; the
    most failed test is the one the command names.

    Sample: the small scenario with the margin floor at 99.9 percent, which no draw reaches.

    Expected outcome: state ``no_usable_choice``; pick, headline and spreads None; no validation
    result; the summaries still published; the most failed test the margin.
    """
    synthetic_scenario["floors"]["margin_pct"] = 99.9
    config = load_product_case_config(write_scenario(synthetic_scenario))
    run = run_product_case(
        config, _view(synthetic_engineering, as_engineering_bytes, synthetic_reported_years)
    )
    assert run.state is RunState.NO_USABLE_CHOICE
    assert run.pick is None and run.headline is None and run.spreads is None
    assert run.validation_results == () and run.headline_failing_tests == ()
    assert len(run.choices) == 16 and all(summary.usable_draws == 0 for summary in run.choices)
    assert most_failed_test(run) is UsableTest.MARGIN
