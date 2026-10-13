"""The product case's checks (``product_case.checks``, B4), on constructed outcomes.

A believable three-year headline at the shipped scenario's prices (every check passes) is built
here from plain numbers; each test changes one value and reads the result it moves. Each test
names what it exercises, its sample and what counts as success.
"""

from __future__ import annotations

import dataclasses
import math
from collections.abc import Callable
from pathlib import Path

import pytest

from common.meta import ValidationResult, ValidationSeverity
from product_case.checks import (
    InvariantError,
    NotFiniteError,
    believability_results,
    check_every_number_finite,
    check_headline_usable_flag,
    check_pick_holds_start_prices,
    check_pick_on_candidates_front,
    check_revenue,
    check_terminals_within_seats,
    check_whole_customers,
    warning_results,
)
from product_case.config import ProductCaseConfig, load_product_case_config
from product_case.constants import ClassKind, PickBasis, ProductClass, UsableTest
from product_case.monte_carlo import (
    ChoiceSummary,
    ClassOutcome,
    Fronts,
    IotOutcome,
    Market,
    MarketOutcome,
    Pick,
    TerminalOutcome,
    YearOutcome,
    YearTotals,
)
from product_case.offers import Choice

YEARS = (2031, 2032, 2033)
"""The constructed headline's reported years."""


def _revenue(customers: float, price: float) -> float:
    """customers x price x 12 / 10^6, $M a year (the class revenue formula)."""
    return customers * price * 12 / 1e6


def _terminal(
    product_class: ProductClass, customers: float, price: float, gb_busy: float, gb_off: float
) -> ClassOutcome:
    """A terminal selling every one of its seats (seats = customers)."""
    return ClassOutcome(
        product_class=product_class,
        kind=ClassKind.TERMINAL,
        price_usd_per_month=price,
        service=1.0,
        demand=customers * 2,
        customers=customers,
        revenue_musd=_revenue(customers, price),
        price_per_unit=price / (gb_busy + gb_off),
        terminal=TerminalOutcome(
            seats=customers,
            seats_filled=1.0,
            busy_hour_gb_per_month=gb_busy,
            offpeak_gb_per_month=gb_off,
            active_rate_mbps=2.0,
            offpeak_downlink_use=gb_off / 5 / gb_busy,
        ),
        iot=None,
    )


def _iot(
    product_class: ProductClass, devices: float, price: float, messages: int, bursts: int
) -> ClassOutcome:
    """An IoT class's entry at a usage of ``messages`` and ``bursts`` a day."""
    bytes_per_day = messages * 340 + bursts * 100_000
    return ClassOutcome(
        product_class=product_class,
        kind=ClassKind.IOT,
        price_usd_per_month=price,
        service=1.0,
        demand=devices + 0.5,
        customers=devices,
        revenue_musd=_revenue(devices, price),
        price_per_unit=price / (bytes_per_day * 30 / 1e6),
        terminal=None,
        iot=IotOutcome(
            messages_per_day=messages,
            bursts_per_day=bursts,
            bursts_outside_busy_hours=None if bursts == 0 else True,
            bytes_per_day=bytes_per_day,
            uplink_use_busy=0.05,
            uplink_use_offpeak=0.1,
        ),
    )


def _year(index: int) -> YearOutcome:
    """Year ``index`` of the believable headline: every class grows, every unit price falls."""
    step = index + 1
    classes = (
        _terminal(ProductClass.SMALL_TERMINAL, 1e6 * step, 10.0, 2.7, 2.7 + step),
        _terminal(ProductClass.MOUNTED_TERMINAL, 1e5 * step, 50.0, 27.0, 27.0 + 10 * step),
        _iot(ProductClass.MINIMAL_PACKET_IOT, 2e7 * step, 3.0, 48 * step, 0),
        _iot(ProductClass.DATA_IOT, 5e6 * step, 6.0, 48, 8 + 2 * step),
    )
    revenue = math.fsum(entry.revenue_musd for entry in classes)
    cost = 100.0 * step
    return YearOutcome(
        year=YEARS[index],
        classes=classes,
        totals=YearTotals(
            revenue_musd=revenue,
            fleet_annual_cost_musd=cost,
            margin_pct=(1 - cost / revenue) * 100,
            profit_musd=revenue - cost,
            busy_hour_beams_filled=1.0,
            iot_uplink_use_busy=0.1,
            iot_uplink_use_offpeak=0.2,
            access_use=0.1,
            access_attempts_per_second_per_beam=5.7,
            single_tone_use=0.05,
            gb_carried_per_year=1e8 * step**2,
            cost_per_gb_carried_usd=cost * 1e6 / (1e8 * step**2),
        ),
    )


def _headline(*, usable: bool = True, failing: tuple[UsableTest, ...] = ()) -> MarketOutcome:
    """The believable headline (or one with its usable flag and failing tests as given)."""
    return MarketOutcome(
        market=Market(0.75, 1.0, 0.25),
        usable=usable,
        failing_tests=failing,
        years=tuple(_year(index) for index in range(len(YEARS))),
    )


def _summary(
    *, at_start: bool = True, mounted_end: float = 50.0, share: float = 0.872
) -> ChoiceSummary:
    """The pick's summary: choice 12, by default at the shipped scenario's start prices."""
    choice = Choice(
        choice_id=12,
        end_prices={
            ProductClass.SMALL_TERMINAL: 10.0,
            ProductClass.MOUNTED_TERMINAL: mounted_end,
            ProductClass.MINIMAL_PACKET_IOT: 3.0,
            ProductClass.DATA_IOT: 6.0,
        },
        minimal_packet_scale=8.0,
        data_iot_scale=1.0,
        at_start_prices=at_start,
    )
    return ChoiceSummary(
        choice=choice,
        usable_draws=round(share * 2000),
        usable_share=share,
        median_summed_revenue_musd=33_000.0,
        median_last_year_revenue_musd=13_000.0,
        central_revenue_musd=(1.0, 2.0, 3.0),
        central_summed_revenue_musd=6.0,
        central_usable=True,
        draws_failing={test: index for index, test in enumerate(UsableTest)},
    )


@pytest.fixture
def config(product_case_yaml: Path) -> ProductCaseConfig:
    """The shipped scenario (its floors and start prices)."""
    return load_product_case_config(product_case_yaml)


def _by_id(results: tuple[ValidationResult, ...]) -> dict[str, ValidationResult]:
    """The results by their ids (every id is unique)."""
    found = {result.validation_id: result for result in results}
    assert len(found) == len(results), "two results share an id"
    return found


def test_a_believable_headline_passes_every_check(config: ProductCaseConfig) -> None:
    """Objective: on a believable headline every believability check, warning and invariant
    passes, and none is a failure.

    Sample: the constructed three-year headline at $10, $50, $3 and $6, every class growing.

    Expected outcome: every believability and warning result ``pass``; every invariant returns
    its ``pass`` result; the believability ids are unique and per subject and year.
    """
    headline = _headline()
    believability = believability_results(config, headline)
    assert {result.severity for result in believability} == {ValidationSeverity.OK}
    ids = _by_id(believability)
    assert "believability.small_terminal.revenue_rises.2031_to_2032" in ids
    assert "believability.data_iot.price_at_or_below_anchor_arpu.2033" in ids
    assert "believability.the_year.cost_per_gb_carried_falls.2032_to_2033" in ids
    pick = Pick(12, PickBasis.ROBUST_FLOOR_MET, (), ())
    warnings = warning_results(config, pick, _summary(), headline)
    assert {result.severity for result in warnings} == {ValidationSeverity.OK}
    for result in (
        check_whole_customers(headline),
        check_terminals_within_seats(headline),
        check_revenue(headline),
        check_pick_holds_start_prices(config, _summary(), headline),
        check_pick_on_candidates_front(pick, Fronts((12,), (12,))),
        check_headline_usable_flag(headline),
        check_every_number_finite(config, [("headline", headline)]),
    ):
        assert result.severity is ValidationSeverity.OK


def _change_class(
    year_index: int, product_class: ProductClass, **changes: object
) -> Callable[[MarketOutcome], MarketOutcome]:
    """A change of one class's fields in one year of a headline."""

    def change(headline: MarketOutcome) -> MarketOutcome:
        years = list(headline.years)
        year = years[year_index]
        classes = tuple(
            dataclasses.replace(entry, **changes) if entry.product_class is product_class else entry
            for entry in year.classes
        )
        years[year_index] = dataclasses.replace(year, classes=classes)
        return dataclasses.replace(headline, years=tuple(years))

    return change


def _change_totals(year_index: int, **changes: object) -> Callable[[MarketOutcome], MarketOutcome]:
    """A change of one year's totals."""

    def change(headline: MarketOutcome) -> MarketOutcome:
        years = list(headline.years)
        years[year_index] = dataclasses.replace(
            years[year_index], totals=dataclasses.replace(years[year_index].totals, **changes)
        )
        return dataclasses.replace(headline, years=tuple(years))

    return change


def _change_block(
    year_index: int, product_class: ProductClass, block: str, **changes: object
) -> Callable[[MarketOutcome], MarketOutcome]:
    """A change of one class's terminal or IoT block in one year."""

    def change(headline: MarketOutcome) -> MarketOutcome:
        entry = next(
            e for e in headline.years[year_index].classes if e.product_class is product_class
        )
        inner = dataclasses.replace(getattr(entry, block), **changes)
        return _change_class(year_index, product_class, **{block: inner})(headline)

    return change


FLAGS: tuple[tuple[str, Callable[[MarketOutcome], MarketOutcome]], ...] = (
    (
        "believability.small_terminal.revenue_rises.2032_to_2033",
        _change_class(2, ProductClass.SMALL_TERMINAL, revenue_musd=1.0),
    ),
    (
        "believability.mounted_terminal.customers_rise_or_hold.2032_to_2033",
        _change_class(2, ProductClass.MOUNTED_TERMINAL, customers=1.0),
    ),
    (
        "believability.data_iot.service_rises_or_holds.2031_to_2032",
        _change_block(1, ProductClass.DATA_IOT, "iot", bursts_per_day=1),
    ),
    (
        "believability.minimal_packet_iot.price_per_unit_falls_or_holds.2032_to_2033",
        _change_class(2, ProductClass.MINIMAL_PACKET_IOT, price_per_unit=100.0),
    ),
    (
        "believability.small_terminal.price_at_or_below_anchor_arpu.2031",
        _change_class(0, ProductClass.SMALL_TERMINAL, price_usd_per_month=48.0),
    ),
    (
        "believability.small_terminal.busy_hour_downlink_use_at_most_full.2032",
        _change_block(1, ProductClass.SMALL_TERMINAL, "terminal", seats_filled=1.01),
    ),
    (
        "believability.mounted_terminal.offpeak_downlink_use_at_most_full.2033",
        _change_block(2, ProductClass.MOUNTED_TERMINAL, "terminal", offpeak_downlink_use=1.2),
    ),
    ("believability.the_year.revenue_rises.2031_to_2032", _change_totals(1, revenue_musd=1.0)),
    (
        "believability.the_year.iot_uplink_use_busy_at_most_full.2031",
        _change_totals(0, iot_uplink_use_busy=1.5),
    ),
    (
        "believability.the_year.iot_uplink_use_offpeak_at_most_full.2033",
        _change_totals(2, iot_uplink_use_offpeak=1.5),
    ),
    ("believability.the_year.access_use_at_most_full.2032", _change_totals(1, access_use=1.1)),
    (
        "believability.the_year.single_tone_use_at_most_full.2032",
        _change_totals(1, single_tone_use=1.1),
    ),
    (
        "believability.the_year.busy_hour_beams_at_most_full.2031",
        _change_totals(0, busy_hour_beams_filled=1.1),
    ),
    (
        "believability.the_year.data_iot_between_small_terminal_and_minimal_packet_iot.2032",
        _change_class(1, ProductClass.DATA_IOT, customers=1e9),
    ),
    (
        "believability.the_year.cost_per_gb_carried_falls.2032_to_2033",
        _change_totals(2, cost_per_gb_carried_usd=10.0),
    ),
    (
        "believability.the_year.margin_at_or_above_floor.2031",
        _change_totals(0, margin_pct=49.9),
    ),
)
"""Each believability check, the change that flags it (one value moved)."""


@pytest.mark.parametrize(("flagged", "change"), FLAGS, ids=[flag for flag, _ in FLAGS])
def test_each_believability_flag_is_a_warning_that_never_refuses(
    config: ProductCaseConfig, flagged: str, change: Callable[[MarketOutcome], MarketOutcome]
) -> None:
    """Objective: each believability check FLAGs its own subject and year as a ``warn`` result,
    never a failure and never an exception (a FLAG never refuses).

    Sample: the believable headline with one value moved to break one check.

    Expected outcome: that check's result is ``warn`` with a hint; no result is ``fail``.
    """
    results = _by_id(believability_results(config, change(_headline())))
    assert results[flagged].severity is ValidationSeverity.WARN
    assert results[flagged].remediation_hint
    assert ValidationSeverity.FAIL not in {result.severity for result in results.values()}


def test_the_run_warnings_name_what_raised_them(config: ProductCaseConfig) -> None:
    """Objective: the three warnings: an upper usage edge names the class; the fallback names the
    share, each failing test's count, that a draw may fail several and that no price is lowered;
    E6 names the central market's failing tests.

    Sample: a pick on minimal-packet IoT's top scale by the fallback, usable in 61.9 percent of
    the draws, and a headline failing the fill and the margin.

    Expected outcome: three ``warn`` results, each text naming its cause.
    """
    pick = Pick(12, PickBasis.MOST_USABLE_FALLBACK, (ProductClass.MINIMAL_PACKET_IOT,), ())
    headline = _headline(usable=False, failing=(UsableTest.FILL, UsableTest.MARGIN))
    results = _by_id(warning_results(config, pick, _summary(share=0.619), headline))
    assert {result.severity for result in results.values()} == {ValidationSeverity.WARN}
    assert "minimal_packet_iot" in results["warning.pick_on_upper_usage_edge"].observed_result
    fallback = results["warning.start_prices_under_robust_floor"].observed_result
    assert "61.9 percent" in fallback and "75.0 percent" in fallback
    assert "fill 0; margin 1; iot_uplink_busy 2" in fallback
    assert "a draw may fail several tests" in fallback and "never lowers a price" in fallback
    assert (
        results["warning.central_market_unusable_for_pick"].observed_result == "fails fill, margin"
    )


type HeadlineCheck = Callable[[MarketOutcome], ValidationResult]
"""An invariant's check on a headline."""

INVARIANTS: tuple[tuple[str, Callable[[MarketOutcome], MarketOutcome], HeadlineCheck, str], ...] = (
    (
        "whole customers",
        _change_class(1, ProductClass.MINIMAL_PACKET_IOT, customers=40_000_000.5),
        check_whole_customers,
        "FY2032: minimal_packet_iot's customers",
    ),
    (
        "within seats",
        _change_block(2, ProductClass.MOUNTED_TERMINAL, "terminal", seats=1.0),
        check_terminals_within_seats,
        "FY2033: mounted_terminal sells",
    ),
    (
        "class revenue",
        _change_class(0, ProductClass.DATA_IOT, revenue_musd=1.0),
        check_revenue,
        "FY2031: data_iot's revenue",
    ),
    (
        "year revenue",
        _change_totals(1, revenue_musd=1.0),
        check_revenue,
        "FY2032: the year's revenue",
    ),
)
"""Each headline invariant: the change that breaks it, its check and what the refusal names."""


@pytest.mark.parametrize(
    ("name", "change", "check", "named"), INVARIANTS, ids=[case[0] for case in INVARIANTS]
)
def test_each_invariant_refuses_naming_the_year_and_class(
    name: str,
    change: Callable[[MarketOutcome], MarketOutcome],
    check: HeadlineCheck,
    named: str,
) -> None:
    """Objective: a headline that breaks an invariant is refused, the refusal naming the year and
    the class (the invariants refuse; the believability checks only warn).

    Sample: the believable headline with one value broken: a fractional count, a terminal past
    its seats, a class's revenue or the year's not matching its formula.

    Expected outcome: an ``InvariantError`` whose message names the year and the class.
    """
    assert check(_headline()).severity is ValidationSeverity.OK
    with pytest.raises(InvariantError, match=named):
        check(change(_headline()))


def test_the_pick_invariants_refuse(config: ProductCaseConfig) -> None:
    """Objective: the pick off its start prices (in its choice, or in a headline year), the pick
    off the candidates' front and a usable flag that disagrees with the failing tests are each
    refused, naming what broke.

    Sample: a pick not at the start prices; one marked at them whose mounted terminal ends at $45;
    a headline pricing FY2033's small terminal at $9; a front without the pick; a headline marked
    usable with a failing test.

    Expected outcome: five ``InvariantError`` refusals, each naming the choice, the class and year,
    the front or the flag.
    """
    with pytest.raises(InvariantError, match="choice 12, is not at the start prices"):
        check_pick_holds_start_prices(config, _summary(at_start=False), _headline())
    with pytest.raises(InvariantError, match="ends mounted_terminal at 45.0"):
        check_pick_holds_start_prices(config, _summary(mounted_end=45.0), _headline())
    off_price = _change_class(2, ProductClass.SMALL_TERMINAL, price_usd_per_month=9.0)(_headline())
    with pytest.raises(InvariantError, match="FY2033: the headline prices small_terminal at 9.0"):
        check_pick_holds_start_prices(config, _summary(), off_price)
    with pytest.raises(InvariantError, match=r"not on the candidates' front \[3\]"):
        check_pick_on_candidates_front(
            Pick(12, PickBasis.ROBUST_FLOOR_MET, (), ()), Fronts((12,), (3,))
        )
    with pytest.raises(InvariantError, match="usable flag, True, disagrees"):
        check_headline_usable_flag(_headline(failing=(UsableTest.FILL,)))


def test_a_number_that_is_not_finite_is_refused_naming_it_and_the_settings(
    config: ProductCaseConfig,
) -> None:
    """Objective: E8: a run holding an infinity or a NaN is refused, naming the first non-finite
    field (walked in field order) and the settings the run's numbers scale with, with values.

    Sample: the believable headline with FY2032's cost per GB carried an infinity and FY2033's
    margin a NaN.

    Expected outcome: a ``NotFiniteError`` naming FY2032's field (the first walked), its value,
    and the prices among the settings.
    """
    broken = _change_totals(2, margin_pct=math.nan)(
        _change_totals(1, cost_per_gb_carried_usd=math.inf)(_headline())
    )
    with pytest.raises(NotFiniteError) as refused:
        check_every_number_finite(config, [("headline", broken)])
    message = str(refused.value)
    assert message.startswith("the run's headline.years[1].totals.cost_per_gb_carried_usd is inf")
    assert "prices.small_terminal.start_usd_month (10.0)" in message
    assert "market.gamma.low (0.5)" in message
