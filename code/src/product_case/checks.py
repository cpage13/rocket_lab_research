"""B4, the checks: the headline's believability, the run's warnings, and the invariants.

Every check is published as a :class:`common.meta.ValidationResult` in the artifact's
``meta.validation_results``:

- **Believability** (round 1 of the product case's scratch exploration's checks, local, on the
  headline): ``pass`` or ``warn`` per subject and reported year, a year-over-year check from the
  second reported year; a ``warn`` (round 1's FLAG) is a warning that never refuses the run. Per
  class: revenue rises; customers rise or hold; what a customer gets rises or holds (a terminal's
  rate while active, busy-hour and off-peak data; an IoT class's messages and bursts); the price
  per unit falls or holds; the price at or below the class's anchor ARPU (its reference named in
  the result: Iridium's voice-and-data $47, broadband $259 and IoT $7.78 today, COMM-618, and
  data IoT's $15.56 by the investor's proportion, COMM-726). Per terminal: its busy-hour and
  off-peak downlink use at most 100 percent. Per year: revenue rises; IoT's uplink use at most 100
  percent in each period; the access use and the single-tone use at most 100 percent; the
  busy-hour beams at most 100 percent; data IoT's customers above the small terminal's and below
  minimal-packet IoT's (the investor's ordering, 2026-10-04); the fleet's cost per GB carried
  falls (bytes add across the classes, people and devices do not); the margin at or above the
  floor. Round 1's tolerances: "rises" is above the year before x (1 + 1e-9), "falls" below it x
  (1 - 1e-9), "holds" within 1e-9 of it; a use is at most 1 and the margin at or above its floor
  exactly.
- **The run's warnings** (``warn`` when raised, ``pass`` when not): the pick on an upper usage
  edge (naming the class); the start prices under the robust floor, the fallback (naming the
  pick's usable draws beside the floor's own count, so a share just under the floor never reads
  as it, and each failing test's count; a draw may fail several, and the run never lowers a
  price); the central market unusable for the pick (E6: the headline is a reading, not a gate).
- **The invariants**, each a check function with the relative tolerance
  :data:`~product_case.constants.RELATIVE_TOLERANCE` where a float is compared: whole customers; a
  terminal never past its seats; each class's revenue equal to customers x price x 12 / 10^6 and
  the year's revenue to their sum; the pick holding the start prices; the pick on the candidates'
  front; the headline's usable flag agreeing with its failing tests; every number finite (the
  run's records walked in field order, the first non-finite field named with the settings it
  scales with, its class's when it is one class's number, E8; a run with no pick is walked too,
  :func:`refuse_not_finite`, before it is returned). One that fails raises
  :class:`InvariantError`, naming the year and the class or the field, and the run is refused;
  one that holds is a ``pass`` result.
"""

from __future__ import annotations

import logging
import math
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, fields, is_dataclass
from itertools import pairwise
from types import MappingProxyType
from typing import Final

from common.meta import ValidationResult, ValidationSeverity
from product_case.config import ProductCaseConfig
from product_case.constants import (
    DATA_IOT_PRICE_MULTIPLE,
    DEMAND_ANCHORS,
    DOLLARS_PER_MILLION,
    MONTHS_PER_YEAR,
    PERCENT,
    RELATIVE_TOLERANCE,
    PickBasis,
    ProductClass,
    SpreadField,
)
from product_case.monte_carlo import (
    FULL_USE,
    ChoiceSummary,
    ClassOutcome,
    FieldSpread,
    Fronts,
    MarketOutcome,
    Pick,
    YearOutcome,
    robust_floor_draws,
)

logger = logging.getLogger(__name__)

_CLASS_PATH: Final[str] = "headline.years[].classes[]"
"""The data-dictionary path of a headline class entry."""

_TOTALS_PATH: Final[str] = "headline.years[].totals"
"""The data-dictionary path of a headline year's totals."""

_ANCHOR_REFERENCES: Final[Mapping[ProductClass, str]] = MappingProxyType(
    {
        ProductClass.SMALL_TERMINAL: "Iridium's voice-and-data ARPU today (COMM-618)",
        ProductClass.MOUNTED_TERMINAL: "Iridium's broadband ARPU today (COMM-618)",
        ProductClass.MINIMAL_PACKET_IOT: "Iridium's IoT ARPU today (COMM-618)",
        ProductClass.DATA_IOT: (
            "data IoT's anchor ARPU, twice Iridium's IoT ARPU today by the investor's proportion "
            "(COMM-726)"
        ),
    }
)
"""Each class's reference price in the anchor check, named (montecarlo m4); its value is the
class's anchor ARPU, :data:`~product_case.constants.DEMAND_ANCHORS`."""


class InvariantError(ValueError):
    """A run breaks an invariant and is refused: its message names the year and class, or field."""


class NotFiniteError(InvariantError):
    """A run holds a number that is not finite (E8): the message names the first such field, its
    value and the settings the run's numbers scale with."""


# ---------------------------------------------------------------------------
# Small helpers: round 1's comparisons, and one way to build a result
# ---------------------------------------------------------------------------


def _rises(previous: float, current: float) -> bool:
    """Strictly up: current > previous x (1 + tolerance)."""
    return current > previous * (1 + RELATIVE_TOLERANCE)


def _rises_or_holds(previous: float, current: float) -> bool:
    """Up, or the same: current >= previous x (1 - tolerance)."""
    return current >= previous * (1 - RELATIVE_TOLERANCE)


def _falls(previous: float, current: float) -> bool:
    """Strictly down: current < previous x (1 - tolerance)."""
    return current < previous * (1 - RELATIVE_TOLERANCE)


def _falls_or_holds(previous: float, current: float) -> bool:
    """Down, or the same: current <= previous x (1 + tolerance)."""
    return current <= previous * (1 + RELATIVE_TOLERANCE)


def _result(
    validation_id: str,
    holds: bool,
    what: str,
    expected: str,
    observed: str,
    paths: Sequence[str],
    hint: str | None = None,
) -> ValidationResult:
    """A ``pass`` result when ``holds``, else a ``warn`` with its hint: a warning never refuses."""
    return ValidationResult(
        validation_id=validation_id,
        severity=ValidationSeverity.OK if holds else ValidationSeverity.WARN,
        what_tested=what,
        expected_condition=expected,
        observed_result=observed,
        related_json_paths=list(paths),
        remediation_hint=None if holds else hint,
    )


def _class_of(year: YearOutcome, product_class: ProductClass) -> ClassOutcome:
    """The class's entry in a headline year."""
    for entry in year.classes:
        if entry.product_class is product_class:
            return entry
    raise InvariantError(f"FY{year.year}: the headline has no {product_class} entry")


_FLAG_HINT: Final[str] = (
    "A believability FLAG is a warning, never a refusal: the headline is published as it is; "
    "read the flagged line beside the class's others."
)
"""The hint every believability warning carries."""


# ---------------------------------------------------------------------------
# Believability (round 1's checks, on the headline)
# ---------------------------------------------------------------------------


def _year_over_year(
    check: str,
    subject: str,
    years: Sequence[YearOutcome],
    value: Callable[[YearOutcome], float],
    good: Callable[[float, float], bool],
    condition: str,
    path: str,
) -> list[ValidationResult]:
    """One result per step between consecutive reported years, from the second year on."""
    results: list[ValidationResult] = []
    for earlier, later in pairwise(years):
        before, after = value(earlier), value(later)
        results.append(
            _result(
                f"believability.{subject}.{check}.{earlier.year}_to_{later.year}",
                good(before, after),
                f"{subject}: {check.replace('_', ' ')}, FY{earlier.year} to FY{later.year}.",
                condition,
                f"{before!r} to {after!r}",
                [path],
                _FLAG_HINT,
            )
        )
    return results


def _each_year(
    check: str,
    subject: str,
    years: Sequence[YearOutcome],
    value: Callable[[YearOutcome], float],
    good: Callable[[float], bool],
    condition: str,
    path: str,
) -> list[ValidationResult]:
    """One result per reported year."""
    return [
        _result(
            f"believability.{subject}.{check}.{year.year}",
            good(value(year)),
            f"{subject}: {check.replace('_', ' ')}, FY{year.year}.",
            condition,
            repr(value(year)),
            [path],
            _FLAG_HINT,
        )
        for year in years
    ]


def _service_parts(entry: ClassOutcome) -> tuple[tuple[str, float], ...]:
    """What a customer gets, part by part: a terminal's rate and data; an IoT class's usage."""
    if entry.terminal is not None:
        return (
            ("rate while active, Mbps", entry.terminal.active_rate_mbps),
            ("busy-hour GB a month", entry.terminal.busy_hour_gb_per_month),
            ("off-peak GB a month", entry.terminal.offpeak_gb_per_month),
        )
    if entry.iot is not None:
        return (
            ("messages a day", float(entry.iot.messages_per_day)),
            ("bursts a day", float(entry.iot.bursts_per_day)),
        )
    raise InvariantError(f"{entry.product_class}: a class entry with neither block")


def _service_results(
    product_class: ProductClass, years: Sequence[YearOutcome]
) -> list[ValidationResult]:
    """What a customer gets rises or holds, every part, from each reported year to the next."""
    results: list[ValidationResult] = []
    for earlier, later in pairwise(years):
        before = _service_parts(_class_of(earlier, product_class))
        after = _service_parts(_class_of(later, product_class))
        fallen = [
            f"{label} {old!r} to {new!r}"
            for (label, old), (_, new) in zip(before, after, strict=True)
            if not _rises_or_holds(old, new)
        ]
        results.append(
            _result(
                f"believability.{product_class}.service_rises_or_holds."
                f"{earlier.year}_to_{later.year}",
                not fallen,
                f"{product_class}: what a customer gets rises or holds, every part, "
                f"FY{earlier.year} to FY{later.year}.",
                "each part's value >= the year before's x (1 - 1e-9)",
                "; ".join(fallen) if fallen else "every part rises or holds",
                [f"{_CLASS_PATH}.terminal", f"{_CLASS_PATH}.iot"],
                _FLAG_HINT,
            )
        )
    return results


def _class_results(
    product_class: ProductClass, years: Sequence[YearOutcome]
) -> list[ValidationResult]:
    """A class's believability checks, every reported year."""
    anchor = DEMAND_ANCHORS[product_class].arpu_usd_month
    reference = _ANCHOR_REFERENCES[product_class]
    subject = str(product_class)
    results = _year_over_year(
        "revenue_rises",
        subject,
        years,
        lambda year: _class_of(year, product_class).revenue_musd,
        _rises,
        "revenue_musd > the year before's x (1 + 1e-9)",
        f"{_CLASS_PATH}.revenue_musd",
    )
    results += _year_over_year(
        "customers_rise_or_hold",
        subject,
        years,
        lambda year: _class_of(year, product_class).customers,
        _rises_or_holds,
        "customers >= the year before's x (1 - 1e-9)",
        f"{_CLASS_PATH}.customers",
    )
    results += _service_results(product_class, years)
    results += _year_over_year(
        "price_per_unit_falls_or_holds",
        subject,
        years,
        lambda year: _class_of(year, product_class).price_per_unit,
        _falls_or_holds,
        "price_per_unit <= the year before's x (1 + 1e-9)",
        f"{_CLASS_PATH}.price_per_unit",
    )
    results += _each_year(
        "price_at_or_below_anchor_arpu",
        subject,
        years,
        lambda year: _class_of(year, product_class).price_usd_per_month,
        lambda price: price <= anchor * (1 + RELATIVE_TOLERANCE),
        f"price_usd_per_month <= {anchor!r} x (1 + 1e-9), {reference}",
        f"{_CLASS_PATH}.price_usd_per_month",
    )
    if product_class in (ProductClass.SMALL_TERMINAL, ProductClass.MOUNTED_TERMINAL):
        results += _each_year(
            "busy_hour_downlink_use_at_most_full",
            subject,
            years,
            lambda year: _terminal_use(_class_of(year, product_class), busy=True),
            lambda use: use <= FULL_USE,
            "seats_filled = customers x r_busy / (seats x r_busy) <= 1",
            f"{_CLASS_PATH}.terminal.seats_filled",
        )
        results += _each_year(
            "offpeak_downlink_use_at_most_full",
            subject,
            years,
            lambda year: _terminal_use(_class_of(year, product_class), busy=False),
            lambda use: use <= FULL_USE,
            "offpeak_downlink_use = customers x r_off(t) / (seats x r_busy) <= 1",
            f"{_CLASS_PATH}.terminal.offpeak_downlink_use",
        )
    return results


def _terminal_use(entry: ClassOutcome, *, busy: bool) -> float:
    """A terminal's busy-hour or off-peak downlink use."""
    if entry.terminal is None:
        raise InvariantError(f"{entry.product_class}: a terminal with no terminal block")
    return entry.terminal.seats_filled if busy else entry.terminal.offpeak_downlink_use


def _ordering_holds(year: YearOutcome) -> bool:
    """Data IoT's customers above the small terminal's and below minimal-packet IoT's."""
    small = _class_of(year, ProductClass.SMALL_TERMINAL).customers
    data = _class_of(year, ProductClass.DATA_IOT).customers
    minimal = _class_of(year, ProductClass.MINIMAL_PACKET_IOT).customers
    return small < data < minimal


def believability_results(
    config: ProductCaseConfig, headline: MarketOutcome
) -> tuple[ValidationResult, ...]:
    """Round 1's believability checks on the headline, each ``pass`` or ``warn``, never refusing.

    Args:
        config: The scenario (its margin floor).
        headline: The pick at the central market.

    Returns:
        Every class's checks in class order, then the year's checks, each per reported year or
        per step between consecutive reported years.
    """
    years = headline.years
    results: list[ValidationResult] = []
    for product_class in ProductClass:
        results += _class_results(product_class, years)
    totals = _TOTALS_PATH
    results += _year_over_year(
        "revenue_rises",
        "the_year",
        years,
        lambda year: year.totals.revenue_musd,
        _rises,
        "revenue_musd > the year before's x (1 + 1e-9)",
        f"{totals}.revenue_musd",
    )
    each_year_uses: tuple[tuple[str, str, Callable[[YearOutcome], float]], ...] = (
        (
            "iot_uplink_use_busy_at_most_full",
            "iot_uplink_use_busy",
            lambda year: year.totals.iot_uplink_use_busy,
        ),
        (
            "iot_uplink_use_offpeak_at_most_full",
            "iot_uplink_use_offpeak",
            lambda year: year.totals.iot_uplink_use_offpeak,
        ),
        ("access_use_at_most_full", "access_use", lambda year: year.totals.access_use),
        (
            "single_tone_use_at_most_full",
            "single_tone_use",
            lambda year: year.totals.single_tone_use,
        ),
        (
            "busy_hour_beams_at_most_full",
            "busy_hour_beams_filled",
            lambda year: year.totals.busy_hour_beams_filled,
        ),
    )
    for check, field, use_of in each_year_uses:
        results += _each_year(
            check,
            "the_year",
            years,
            use_of,
            lambda use: use <= FULL_USE,
            f"{field} <= 1",
            f"{totals}.{field}",
        )
    results += [
        _result(
            f"believability.the_year.data_iot_between_small_terminal_and_minimal_packet_iot.{year.year}",
            _ordering_holds(year),
            "Data IoT's customers above the small terminal's and below minimal-packet IoT's "
            f"(the investor's ordering, 2026-10-04), FY{year.year}.",
            "small terminal < data IoT < minimal-packet IoT, customers",
            ", ".join(
                f"{entry.product_class} {entry.customers!r}"
                for entry in year.classes
                if entry.product_class is not ProductClass.MOUNTED_TERMINAL
            ),
            [f"{_CLASS_PATH}.customers"],
            _FLAG_HINT,
        )
        for year in years
    ]
    results += _year_over_year(
        "cost_per_gb_carried_falls",
        "the_year",
        years,
        lambda year: year.totals.cost_per_gb_carried_usd,
        _falls,
        "cost_per_gb_carried_usd < the year before's x (1 - 1e-9)",
        f"{totals}.cost_per_gb_carried_usd",
    )
    floor = config.floors.margin_pct
    results += _each_year(
        "margin_at_or_above_floor",
        "the_year",
        years,
        lambda year: year.totals.margin_pct,
        lambda margin: margin >= floor,
        f"margin_pct >= {floor!r}, the margin floor on the whole business",
        f"{totals}.margin_pct",
    )
    flagged = sum(1 for result in results if result.severity is ValidationSeverity.WARN)
    logger.debug("believability: %d results, %d flagged", len(results), flagged)
    return tuple(results)


# ---------------------------------------------------------------------------
# The run's warnings
# ---------------------------------------------------------------------------


def robust_floor_text(config: ProductCaseConfig) -> str:
    """The robust floor in words, its own count beside its share, the one form the warnings and
    the stated assumptions print: "the robust floor's 1,500 (75 percent of the draws)".

    The count is :func:`~product_case.monte_carlo.robust_floor_draws`'s, the fewest usable draws
    that reach the floor; the share is printed with ``:g``, so a floor of 0.745 reads 74.5.

    Args:
        config: The scenario (its draws and its robust floor).

    Returns:
        The phrase.
    """
    return (
        f"the robust floor's {robust_floor_draws(config):,} "
        f"({PERCENT * config.floors.robust:g} percent of the draws)"
    )


def warning_results(
    config: ProductCaseConfig, pick: Pick, summary: ChoiceSummary, headline: MarketOutcome
) -> tuple[ValidationResult, ...]:
    """The run's three warnings, each ``warn`` when raised and ``pass`` when not.

    Args:
        config: The scenario (its draws and its robust floor).
        pick: The pick.
        summary: The pick's summary over the draws.
        headline: The pick at the central market.

    Returns:
        The usage-edge warning, the fallback warning and the central-market warning (E6).
    """
    edges = ", ".join(str(product_class) for product_class in pick.usage_edges)
    failing = "; ".join(f"{test} {count:,}" for test, count in summary.draws_failing.items())
    draws = config.market.draws
    floor = robust_floor_text(config)
    return (
        _result(
            "warning.pick_on_upper_usage_edge",
            not pick.usage_edges,
            "The pick's usage sits inside each IoT class's usage scales, not on the top.",
            "no IoT class at the top of its usage scales",
            f"on the top: {edges}" if edges else "inside the scales for both IoT classes",
            ["pick.usage_edges", "choices[].minimal_packet_scale", "choices[].data_iot_scale"],
            "The usable test did not stop the usage there: a larger scale might serve more.",
        ),
        _result(
            "warning.start_prices_under_robust_floor",
            pick.basis is PickBasis.ROBUST_FLOOR_MET,
            "The start prices are usable in at least the robust floor's share of the draws.",
            f"pick.basis {PickBasis.ROBUST_FLOOR_MET}: usable in at least {floor}",
            (
                "no candidate reaches the robust floor: the most usable, the pick, is usable in "
                f"{summary.usable_draws:,} of the {draws:,} draws, under {floor}; its draws fail: "
                f"{failing} (a draw may fail several tests); the run never lowers a price"
                if pick.basis is PickBasis.MOST_USABLE_FALLBACK
                else (
                    f"usable in {summary.usable_draws:,} of the {draws:,} draws, at or above "
                    f"{floor}"
                )
            ),
            ["pick.basis", "choices[].usable_share", "choices[].draws_failing"],
            "The fallback is published, warned; the prices stay the scenario's start prices.",
        ),
        _result(
            "warning.central_market_unusable_for_pick",
            headline.usable,
            "The central market is usable for the pick (E6).",
            "headline.usable true",
            "usable"
            if headline.usable
            else "fails " + ", ".join(str(test) for test in headline.failing_tests),
            ["headline.usable", "headline.failing_tests"],
            "The headline is a reading, not a gate: it is published with its failing tests.",
        ),
    )


# ---------------------------------------------------------------------------
# The invariants (refusing)
# ---------------------------------------------------------------------------


def _invariant_pass(
    validation_id: str, what: str, expected: str, paths: Sequence[str]
) -> ValidationResult:
    """The ``pass`` result of an invariant that holds."""
    return _result(validation_id, True, what, expected, "holds", paths)


def _close(value: float, target: float) -> bool:
    """Equal within the invariants' relative tolerance."""
    return math.isclose(value, target, rel_tol=RELATIVE_TOLERANCE, abs_tol=0.0)


def check_whole_customers(headline: MarketOutcome) -> ValidationResult:
    """Every class's customers are a whole number in every reported year.

    Raises:
        InvariantError: Naming the year, the class and the value.
    """
    for year in headline.years:
        for entry in year.classes:
            if not _close(entry.customers, float(round(entry.customers))):
                raise InvariantError(
                    f"FY{year.year}: {entry.product_class}'s customers, {entry.customers!r}, are "
                    "not a whole number"
                )
    return _invariant_pass(
        "invariant.whole_customers",
        "Every class's customers are a whole number in every reported year.",
        "customers = round(customers), within 1e-9 relative",
        [f"{_CLASS_PATH}.customers"],
    )


def check_terminals_within_seats(headline: MarketOutcome) -> ValidationResult:
    """No terminal sells past its seats in any reported year.

    Raises:
        InvariantError: Naming the year, the terminal, its customers and its seats.
    """
    for year in headline.years:
        for entry in year.classes:
            if entry.terminal is None:
                continue
            if entry.customers > entry.terminal.seats * (1 + RELATIVE_TOLERANCE):
                raise InvariantError(
                    f"FY{year.year}: {entry.product_class} sells {entry.customers!r}, past its "
                    f"{entry.terminal.seats!r} seats"
                )
    return _invariant_pass(
        "invariant.terminals_within_seats",
        "No terminal sells past its seats in any reported year.",
        "customers <= seats x (1 + 1e-9)",
        [f"{_CLASS_PATH}.customers", f"{_CLASS_PATH}.terminal.seats"],
    )


def check_revenue(headline: MarketOutcome) -> ValidationResult:
    """Each class's revenue is customers x price x 12 / 10^6 and the year's revenue their sum.

    Raises:
        InvariantError: Naming the year and the class, or the year's total, and both values.
    """
    for year in headline.years:
        for entry in year.classes:
            expected = (
                entry.customers * entry.price_usd_per_month * MONTHS_PER_YEAR / DOLLARS_PER_MILLION
            )
            if not _close(entry.revenue_musd, expected):
                raise InvariantError(
                    f"FY{year.year}: {entry.product_class}'s revenue, {entry.revenue_musd!r} $M, "
                    f"is not its customers x price x 12 / 10^6, {expected!r}"
                )
        total = math.fsum(entry.revenue_musd for entry in year.classes)
        if not _close(year.totals.revenue_musd, total):
            raise InvariantError(
                f"FY{year.year}: the year's revenue, {year.totals.revenue_musd!r} $M, is not the "
                f"sum of its classes', {total!r}"
            )
    return _invariant_pass(
        "invariant.revenue_is_customers_times_price",
        "Each class's revenue is its customers x its price x 12 / 10^6 and the year's revenue is "
        "their sum, in every reported year.",
        "within 1e-9 relative",
        [f"{_CLASS_PATH}.revenue_musd", f"{_TOTALS_PATH}.revenue_musd"],
    )


def check_pick_holds_start_prices(
    config: ProductCaseConfig, summary: ChoiceSummary, headline: MarketOutcome
) -> ValidationResult:
    """The pick holds every class's start price, in its choice and in every headline year.

    Raises:
        InvariantError: Naming the class (and the year) whose price is not its start price.
    """
    prices = config.prices
    starts = {
        ProductClass.SMALL_TERMINAL: prices.small_terminal.start_usd_month,
        ProductClass.MOUNTED_TERMINAL: prices.mounted_terminal.start_usd_month,
        ProductClass.MINIMAL_PACKET_IOT: prices.minimal_packet_iot.start_usd_month,
        ProductClass.DATA_IOT: DATA_IOT_PRICE_MULTIPLE * prices.minimal_packet_iot.start_usd_month,
    }
    choice = summary.choice
    if not choice.at_start_prices:
        raise InvariantError(f"the pick, choice {choice.choice_id}, is not at the start prices")
    for product_class, start in starts.items():
        if choice.end_prices[product_class] != start:
            raise InvariantError(
                f"the pick, choice {choice.choice_id}, ends {product_class} at "
                f"{choice.end_prices[product_class]!r}, not its start price {start!r}"
            )
        for year in headline.years:
            price = _class_of(year, product_class).price_usd_per_month
            if not _close(price, start):
                raise InvariantError(
                    f"FY{year.year}: the headline prices {product_class} at {price!r}, not its "
                    f"start price {start!r}"
                )
    return _invariant_pass(
        "invariant.pick_holds_start_prices",
        "The pick holds every class's start price (the investor's, in the shipped scenario) in "
        "every reported year.",
        "each end price equal to its start price; each headline price within 1e-9 of it",
        ["choices[].at_start_prices", "choices[].end_prices", f"{_CLASS_PATH}.price_usd_per_month"],
    )


def check_pick_on_candidates_front(pick: Pick, fronts: Fronts) -> ValidationResult:
    """The pick lies on the candidates' front.

    Raises:
        InvariantError: Naming the pick and the front.
    """
    if pick.choice_id not in fronts.at_start_prices:
        raise InvariantError(
            f"the pick, choice {pick.choice_id}, is not on the candidates' front "
            f"{list(fronts.at_start_prices)}"
        )
    return _invariant_pass(
        "invariant.pick_on_candidates_front",
        "The pick lies on the candidates' front.",
        "pick.choice_id in fronts.at_start_prices",
        ["pick.choice_id", "fronts.at_start_prices"],
    )


def check_headline_usable_flag(headline: MarketOutcome) -> ValidationResult:
    """The headline's usable flag agrees with its failing tests.

    Raises:
        InvariantError: Naming the flag and the tests.
    """
    if headline.usable != (not headline.failing_tests):
        raise InvariantError(
            f"the headline's usable flag, {headline.usable}, disagrees with its failing tests "
            f"{[str(test) for test in headline.failing_tests]}"
        )
    return _invariant_pass(
        "invariant.headline_usable_flag_agrees",
        "The headline's usable flag agrees with its failing tests.",
        "headline.usable true exactly when headline.failing_tests is empty",
        ["headline.usable", "headline.failing_tests"],
    )


_SPREAD_FIELD_CLASS: Final[Mapping[SpreadField, ProductClass]] = MappingProxyType(
    {
        SpreadField.SMALL_TERMINAL_CUSTOMERS: ProductClass.SMALL_TERMINAL,
        SpreadField.SMALL_TERMINAL_REVENUE: ProductClass.SMALL_TERMINAL,
        SpreadField.MOUNTED_TERMINAL_CUSTOMERS: ProductClass.MOUNTED_TERMINAL,
        SpreadField.MOUNTED_TERMINAL_REVENUE: ProductClass.MOUNTED_TERMINAL,
        SpreadField.MINIMAL_PACKET_IOT_CUSTOMERS: ProductClass.MINIMAL_PACKET_IOT,
        SpreadField.MINIMAL_PACKET_IOT_REVENUE: ProductClass.MINIMAL_PACKET_IOT,
        SpreadField.DATA_IOT_CUSTOMERS: ProductClass.DATA_IOT,
        SpreadField.DATA_IOT_REVENUE: ProductClass.DATA_IOT,
    }
)
"""The class a spread field's numbers belong to (a read-only mapping); the year's totals, the
margin and IoT's uplink uses belong to no single class."""

_PRICE_SETTING_CLASS: Final[Mapping[ProductClass, ProductClass]] = MappingProxyType(
    {
        ProductClass.SMALL_TERMINAL: ProductClass.SMALL_TERMINAL,
        ProductClass.MOUNTED_TERMINAL: ProductClass.MOUNTED_TERMINAL,
        ProductClass.MINIMAL_PACKET_IOT: ProductClass.MINIMAL_PACKET_IOT,
        ProductClass.DATA_IOT: ProductClass.MINIMAL_PACKET_IOT,
    }
)
"""The class whose price setting prices each class (a read-only mapping): data IoT pays twice
minimal-packet IoT's price, so its price is no setting of its own."""


@dataclass(frozen=True)
class _NotFinite:
    """The first float a walk finds that is not finite.

    Attributes:
        path: Its path in the run's records.
        value: The infinity or NaN.
        product_class: The class whose record holds it (a class's headline entry or spread
            field), or None when it is no single class's number.
    """

    path: str
    value: float
    product_class: ProductClass | None


def _owner(value: object, owner: ProductClass | None) -> ProductClass | None:
    """The class a record belongs to: a class's headline entry's own, a spread field's, else the
    class of the record that holds it."""
    if isinstance(value, ClassOutcome):
        return value.product_class
    if isinstance(value, FieldSpread):
        return _SPREAD_FIELD_CLASS.get(value.field)
    return owner


def _first_not_finite(
    value: object, path: str, owner: ProductClass | None = None
) -> _NotFinite | None:
    """The first float in a record that is an infinity or a NaN, with its path and class, else None.

    Depth first in field order: a dataclass by its fields, a mapping by its keys, a tuple or a
    list by index; any other value (an int, a string, an enum, a flag, None) holds no float. A
    class's headline entry or spread field passes its class to what it holds.
    """
    if isinstance(value, float):
        return None if math.isfinite(value) else _NotFinite(path, value, owner)
    children: Iterable[tuple[str, object]]
    if is_dataclass(value) and not isinstance(value, type):
        children = [(f"{path}.{field.name}", getattr(value, field.name)) for field in fields(value)]
    elif isinstance(value, Mapping):
        children = [(f"{path}[{key}]", child) for key, child in value.items()]
    elif isinstance(value, tuple | list):
        children = [(f"{path}[{index}]", child) for index, child in enumerate(value)]
    else:
        return None
    holder = _owner(value, owner)
    for child_path, child in children:
        found = _first_not_finite(child, child_path, holder)
        if found is not None:
            return found
    return None


def _settings_text(config: ProductCaseConfig, product_class: ProductClass | None) -> str:
    """The settings a number scales with, each with its value: its class's price and usage (data
    IoT's price is minimal-packet IoT's, twice), or every class's when the number is no single
    class's; then the market's ranges."""
    parts: list[str] = []

    def flatten(prefix: str, value: object) -> None:
        if isinstance(value, Mapping):
            for key, child in value.items():
                flatten(f"{prefix}.{key}", child)
        else:
            parts.append(f"{prefix} ({value!r})")

    prices = config.prices.model_dump()
    usage = config.usage.model_dump()
    if product_class is None:
        price_keys, usage_keys = list(prices), list(usage)
    else:
        price_keys = [str(_PRICE_SETTING_CLASS[product_class])]
        usage_keys = [str(product_class)]
    for key in price_keys:
        flatten(f"prices.{key}", prices[key])
    for key in usage_keys:
        flatten(f"usage.{key}", usage[key])
    for response in ("gamma", "epsilon", "eta"):
        flatten(f"market.{response}", getattr(config.market, response).model_dump())
    return ", ".join(parts)


def refuse_not_finite(config: ProductCaseConfig, records: Sequence[tuple[str, object]]) -> None:
    """Refuse a run holding a number that is not finite (E8), at any point of the run.

    Args:
        config: The scenario (the settings named in a refusal).
        records: The run's records, each with the name its paths start with, walked in order.

    Raises:
        NotFiniteError: Naming the first field that is not finite, its value, and the settings it
            scales with, each with its value: its class's when the field is one class's (a
            headline entry or a spread field), else every class's; no setting this far out is
            one the model can compute.
    """
    for name, record in records:
        found = _first_not_finite(record, name)
        if found is not None:
            whose = "the run's" if found.product_class is None else f"{found.product_class}'s"
            raise NotFiniteError(
                f"the run's {found.path} is {found.value!r}, not a finite number: {whose} "
                f"numbers scale with {_settings_text(config, found.product_class)}, and one of "
                "them is past what the model can compute"
            )


def check_every_number_finite(
    config: ProductCaseConfig,
    records: Sequence[tuple[str, object]],
    json_paths: Sequence[str],
) -> ValidationResult:
    """Every number of the run's records is finite (E8): :func:`refuse_not_finite`, then its
    ``pass`` result.

    Args:
        config: The scenario (the settings named in a refusal).
        records: The run's records, each with the name its paths start with, walked in order.
        json_paths: The artifact paths the records are published under (the result's related
            paths: the engineering view's are ``inputs.engineering`` and ``network``).

    Returns:
        The ``pass`` result.

    Raises:
        NotFiniteError: As :func:`refuse_not_finite`.
    """
    refuse_not_finite(config, records)
    return _invariant_pass(
        "invariant.every_number_finite",
        "Every number of the run is finite (no infinity, no NaN).",
        "every float finite",
        json_paths,
    )


__all__ = [
    "InvariantError",
    "NotFiniteError",
    "believability_results",
    "check_every_number_finite",
    "check_headline_usable_flag",
    "check_pick_holds_start_prices",
    "check_pick_on_candidates_front",
    "check_revenue",
    "check_terminals_within_seats",
    "check_whole_customers",
    "refuse_not_finite",
    "robust_floor_text",
    "warning_results",
]
