"""B5, the entry: one product-case run, from the scenario and the engineering view to its record.

:func:`run_product_case` composes the boxes in order: the offers (B2,
:func:`~product_case.offers.grid_offers`), the drawn markets and each choice's summary (B3,
:func:`~product_case.monte_carlo.summarize_grid`), the two fronts and the pick; then, with a pick,
the headline (the pick at the central market), the pick's spreads, and the checks (B4: the
invariants, which refuse a run that breaks one, the believability checks and the run's warnings,
which never refuse). It returns a frozen :class:`ProductCaseRun` carrying its state to the end:
when no candidate is usable in any draw the state is ``no_usable_choice``, with no pick, headline,
spreads or checks, and nothing is raised (the command refuses to publish such a run, naming the
test most of the candidates' draws fail, :func:`most_failed_test`), unless the run holds a number
that is not finite, which is refused naming its field in that state too
(:func:`~product_case.checks.refuse_not_finite`), since such a number can leave every candidate
unusable.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from common.meta import ValidationResult, ValidationSeverity
from product_case.checks import (
    believability_results,
    check_every_number_finite,
    check_headline_usable_flag,
    check_pick_holds_start_prices,
    check_pick_on_candidates_front,
    check_revenue,
    check_terminals_within_seats,
    check_whole_customers,
    refuse_not_finite,
    warning_results,
)
from product_case.config import ProductCaseConfig
from product_case.constants import RunState, UsableTest
from product_case.engineering import EngineeringView
from product_case.monte_carlo import (
    ChoiceSummary,
    Fronts,
    MarketOutcome,
    Pick,
    Spreads,
    central_market,
    draw_markets,
    fronts_of,
    outcome_in_market,
    pick_of,
    spreads_of,
    summarize_grid,
)
from product_case.offers import grid_offers

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProductCaseRun:
    """One product-case run, frozen, its state carried to the end.

    Attributes:
        state: ``picked``, or ``no_usable_choice`` when no candidate is usable in any draw.
        config: The scenario it ran.
        engineering: The engineering view it ran on.
        choices: Every choice's summary, in the grid's order.
        fronts: The front over every choice and the candidates' front.
        pick: The pick; None in ``no_usable_choice``.
        headline: The pick at the central market; None in ``no_usable_choice``.
        spreads: The pick's spreads over the draws; None in ``no_usable_choice``.
        validation_results: The invariants (each held), the believability checks and the run's
            warnings, in that order; empty in ``no_usable_choice``.
    """

    state: RunState
    config: ProductCaseConfig
    engineering: EngineeringView
    choices: tuple[ChoiceSummary, ...]
    fronts: Fronts
    pick: Pick | None
    headline: MarketOutcome | None
    spreads: Spreads | None
    validation_results: tuple[ValidationResult, ...]

    @property
    def headline_failing_tests(self) -> tuple[UsableTest, ...]:
        """The usable tests the headline's market fails for the pick (empty with no headline)."""
        return () if self.headline is None else self.headline.failing_tests

    @property
    def warnings(self) -> tuple[ValidationResult, ...]:
        """The validation results that warn: believability FLAGs and raised run warnings."""
        return tuple(
            result
            for result in self.validation_results
            if result.severity is ValidationSeverity.WARN
        )


def _summary_of(choices: tuple[ChoiceSummary, ...], choice_id: int) -> ChoiceSummary:
    """The summary of the choice with ``choice_id``."""
    for summary in choices:
        if summary.choice.choice_id == choice_id:
            return summary
    raise KeyError(choice_id)


def run_product_case(config: ProductCaseConfig, engineering: EngineeringView) -> ProductCaseRun:
    """Run the product case: method steps 2 to 9 on the engineering view, then the checks.

    Args:
        config: The scenario.
        engineering: The engineering view of the scenario's reported years
            (:func:`~product_case.engineering.engineering_view_from_bytes`).

    Returns:
        The run: ``picked`` with its pick, headline, spreads and validation results, or
        ``no_usable_choice`` with none of them (nothing raised but a number that is not finite).

    Raises:
        product_case.offers.OfferError: If the scenario's usage cannot be offered on the view
            (a monthly total below its busy-hour part, a value past what a float holds, the view's
            years not the scenario's), naming the field and the year.
        product_case.checks.InvariantError: If the run breaks an invariant, naming the year and
            the class or the field; ``NotFiniteError`` (one) for a number that is not finite, in
            either state, naming it and the settings it scales with.
    """
    grid = grid_offers(config, engineering)
    markets = draw_markets(config)
    choices = summarize_grid(config, engineering, grid, markets)
    fronts = fronts_of(choices)
    pick = pick_of(choices, fronts, config)
    if pick is None:
        # A number past what a float holds can leave every candidate unusable (an IoT price of
        # 5e-324 sells infinite devices): it is refused naming its field, never published as
        # no usable choice.
        refuse_not_finite(
            config, (("engineering", engineering), ("choices", choices), ("fronts", fronts))
        )
        logger.info("no candidate is usable in any of the %d draws: no pick", len(markets))
        return ProductCaseRun(
            state=RunState.NO_USABLE_CHOICE,
            config=config,
            engineering=engineering,
            choices=choices,
            fronts=fronts,
            pick=None,
            headline=None,
            spreads=None,
            validation_results=(),
        )
    summary = _summary_of(choices, pick.choice_id)
    headline = outcome_in_market(config, engineering, summary.choice, central_market(config))
    spreads = spreads_of(config, engineering, summary.choice, markets, headline)
    invariants = (
        check_every_number_finite(
            config,
            (
                ("engineering", engineering),
                ("choices", choices),
                ("fronts", fronts),
                ("pick", pick),
                ("headline", headline),
                ("spreads", spreads),
            ),
            ("inputs.engineering", "network", "choices", "fronts", "pick", "headline", "spreads"),
        ),
        check_whole_customers(headline),
        check_terminals_within_seats(headline),
        check_revenue(headline),
        check_pick_holds_start_prices(config, summary, headline),
        check_pick_on_candidates_front(pick, fronts),
        check_headline_usable_flag(headline),
    )
    results = (
        *invariants,
        *believability_results(config, headline),
        *warning_results(config, pick, summary, headline),
    )
    logger.info(
        "picked choice %d (%s), usable in %d of %d draws",
        pick.choice_id,
        pick.basis,
        summary.usable_draws,
        len(markets),
    )
    return ProductCaseRun(
        state=RunState.PICKED,
        config=config,
        engineering=engineering,
        choices=choices,
        fronts=fronts,
        pick=pick,
        headline=headline,
        spreads=spreads,
        validation_results=results,
    )


def most_failed_test(run: ProductCaseRun) -> UsableTest:
    """The test the candidates' draws fail most: each test's failing draws summed over the
    candidates (the choices at the start prices), ties to the earlier test in
    :class:`~product_case.constants.UsableTest` order. A ``no_usable_choice`` refusal names it.

    Args:
        run: A run (in practice one in ``no_usable_choice``).

    Returns:
        The most failed test.
    """
    candidates = [summary for summary in run.choices if summary.choice.at_start_prices]
    totals = {
        test: sum(summary.draws_failing[test] for summary in candidates) for test in UsableTest
    }
    return max(UsableTest, key=lambda test: totals[test])


__all__ = ["ProductCaseRun", "most_failed_test", "run_product_case"]
