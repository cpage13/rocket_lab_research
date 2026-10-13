"""B3, the Monte Carlo: the markets drawn, every choice judged over them and at the central market,
the fronts, the pick and the pick's spreads (method steps 3 to 9).

The one product-case module that imports numpy (ADR 010 as ADR 012 widens it; guard N4), and no
array leaves it: every record it returns is frozen and holds plain numbers. Every price, usage
path, range and floor comes from the config, the engineering view and the offers; nothing is kept
in a module-level variable.

**The markets.** :func:`draw_markets` draws them with the standard library's generator (D9):
``random.Random(seed)`` and, for each draw in turn, gamma, epsilon then eta, each
``uniform(low, high)``, that is ``low + (high - low) x random()``: round 3's stream, from the one
part of Python's generator whose sequence is promised across versions. :func:`central_market`
holds each response at the middle of its range (D7), so it moves with neither the seed nor the
draw count.

**One evaluation.** A choice's offers (:mod:`product_case.offers`) are evaluated over many markets
at once, as arrays of the draw count, and in one market, as arrays of length one, by the same
code, so the headline and the draws cannot drift. In a market (gamma, epsilon, eta), in each
reported year t, on the engineering view's network (:mod:`product_case.engineering`):

3. the demand curve, D_c(t) = N_c x k(t)^gamma x (A_c / p_c(t))^epsilon x v_c(t)^eta, for each
   class c (:func:`_demand`);
4. sold: a terminal n_c = floor(min(D_c, S_c)) customers, never past its seats S_c; an IoT class
   n_c = floor(D_c) devices, uncapped, its sales held to IoT's room by the usable test. IoT's
   customers come from the demand curve in every market and year: no count is ever set;
5. the year's numbers: the busy-hour beams filled F(t) = s x n_small / S_small + (1 - s) x
   n_mounted / S_mounted; each class's revenue n_c x p_c x 12 / 10^6 and the year's
   Rev(t) = (the sum over the four classes of n_c x p_c) x 12 / 10^6, $M a year; the margin
   1 - C(t) / Rev(t), published x 100, with C(t) the fleet's annual cost; profit Rev(t) - C(t);
   IoT's uplink use in each period (the busy hours, off-peak), U(t) = the sum over the two IoT
   classes of n_c x (b_c / R(t)), with b_c a device's uplink bits a second in the period and R(t)
   the payload room; the access use, the larger period's sum of n_c x a_c over A(t), with a_c a
   device's random-access attempts a second (the same sum over L(t) is the attempts a second a
   beam); the single-tone use, the sum of n_c x q_c x the airtime's high end over T(t), with q_c a
   device's messages a second; the GB carried G(t), each terminal's customers x its data a month
   x 12 plus each IoT class's devices x its bytes a day x 30 x 12 / 10^9 (bytes add across the
   classes; people and devices never do); and the fleet's cost per GB carried, C(t) x 10^6 / G(t),
   dollars;
6. usable, in every reported year: F(t) at least the fill floor, the margin at least the margin
   floor, both uplink uses, the access use and the single-tone use at most 1 (each room used at
   most in full); and Rev(t) strictly rising from each reported year to the next. A market fails a
   test when the test's condition does not hold (a number that is not finite fails it) and
   records every test it fails (:class:`~product_case.constants.UsableTest`).

**Each choice, the fronts, the pick, the spreads** (steps 7 to 9). :func:`summarize_grid` reduces
each choice over the draws to its :class:`ChoiceSummary` and nothing more: its usable draws and
share; the ``statistics.median`` of its summed revenue (the built-in ``sum`` of Rev(t) over the
reported years, in year order, as round 3 summed it, compensated on Python 3.12 and later) and of
its last reported year's Rev, over its usable draws (None when none is usable); the draws failing
each test; and, through the same evaluation, the central market's Rev per reported year, summed,
and whether it is usable. :func:`fronts_of` sweeps the summaries (round 3's sweep: by usable share,
then median summed revenue, both descending, then the grid's order; a member joins when its median
is strictly above every earlier member's), over every choice and over the candidates (the choices
that hold every price at its start price, the investor's in the shipped scenario). :func:`pick_of`
takes the highest median among the candidates usable in at least the robust floor's share of the
draws, ties to the higher share, then the earlier choice; else the candidates' front's first member
(the most usable candidate, which the checks warn of); else no pick. The pick is evaluated again at
the central market for the headline (:func:`outcome_in_market`) and over the draws for its spreads
(:func:`spreads_of`).

**What stops the usage.** Every candidate holds the same terminal prices, so every candidate fails
the terminals' fill in the same weak markets, and IoT's own failures (its room or access, in the
strong markets, which earn the most) may take only the draws between the fill's share and the
robust floor. The pick's usage therefore rises while its median summed revenue rises and its usable
share stays at or above the floor, and stops at whichever comes first: the floor, or the median's
peak. It can move with a price or a terminal change, in steps; the prices never move.

**Operation order.** Every quantity floored or compared with a threshold is computed in round 3's
operation order (round 3 of the product case's scratch exploration, local): the curve, multiplied
left to right; the min and the floor at the seats; the fill; each room use as the devices x each
device's share of the room; the margin; the summed revenue. numpy's elementwise float64 arithmetic
is IEEE arithmetic, as Python's floats are, and its float64 power equals Python's on this platform.
The access use is read against the published access room A(t) (the design's form), which gives
round 3's per-beam verdict, 57 attempts a second a beam, in every choice, draw and year of round
3's grids and the shipped grid. The arithmetic runs with numpy's floating-point warnings off: a
setting past what a float holds gives an infinity or a NaN, which travels to the checks' walk of
the run's numbers, where the run is refused, naming the field, never an exception in the middle.

**Determinism.** The same scenario and engineering view give the same records, and the same bytes
when published, on this platform: the draws are the standard library's promised stream, and
numpy's float64 power equals Python's here. Another platform's vectorized power (numpy's SIMD path
on Linux x86_64 with AVX-512, say) is not promised to equal its libm to the last bit, so there a
floor at a demand within a few units in the last place of a whole number could move a count by one
(the review of 2026-10-12, montecarlo m6, local).
"""

from __future__ import annotations

import logging
import math
import random
import statistics
from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass
from itertools import pairwise
from typing import Final

import numpy as np
import numpy.typing as npt

from product_case.config import ProductCaseConfig, ResponseRange
from product_case.constants import (
    BYTES_PER_GB,
    BYTES_PER_MB,
    CLASS_KIND,
    DAYS_PER_MONTH,
    DEMAND_ANCHORS,
    DOLLARS_PER_MILLION,
    MIN_DRAWS,
    MONTHS_PER_YEAR,
    PERCENT,
    ClassKind,
    DemandAnchor,
    PickBasis,
    ProductClass,
    SpreadField,
    SpreadNullReason,
    UsableTest,
)
from product_case.engineering import EngineeringView, EngineeringYear
from product_case.offers import (
    Choice,
    ChoiceOffers,
    IotOffer,
    TerminalOffer,
    YearOffers,
    choice_offers,
)

logger = logging.getLogger(__name__)

type _Floats = npt.NDArray[np.float64]
"""A float64 array over markets, one value a market."""

type _Flags = npt.NDArray[np.bool_]
"""A boolean array over markets, one flag a market."""

FULL_USE: Final[float] = 1.0
"""A room used in full: an IoT uplink, access or single-tone use above it sells past that room,
so the usable test holds each at or below it (a definition)."""

PERCENTILE_GROUPS: Final[int] = 10
"""``statistics.quantiles``' ``n`` for the spreads: ten groups, whose first cut is the 10th
percentile and whose last is the 90th (round 3's spread; a definition)."""

SPREAD_MIN_VALUES: Final[int] = MIN_DRAWS
"""The fewest values a spread's percentiles are published over, 9: below it the exclusive
method's 10th and 90th cuts fall outside the data (the design's D10), so a usable-draw spread
below it is null with its reason; the scenario's draws are never fewer (a definition)."""

TIE_WEIGHT: Final[float] = 0.5
"""The weight of a draw equal to the headline in the headline's mid-rank: the share strictly below
plus half the share equal, the one reading that treats ties evenly (the design's D10; a
definition)."""

RANGE_ENDS: Final[int] = 2
"""A range's two ends, whose mean is its middle, the central market's response (a definition)."""


# ---------------------------------------------------------------------------
# The records: plain numbers, frozen
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Market:
    """One market: the demand curve's three responses, drawn or at the middle of their ranges.

    Attributes:
        gamma: The response to the network's scale, the exponent on k(t).
        epsilon: The price response, the exponent on A_c / p_c(t).
        eta: The service response, the exponent on v_c(t).
    """

    gamma: float
    epsilon: float
    eta: float


@dataclass(frozen=True)
class TerminalOutcome:
    """A terminal's own block of a market's outcome in one reported year.

    Attributes:
        seats: S, its seats, unrounded (s x P_small(t) or (1 - s) x P_mounted(t)).
        seats_filled: Its busy-hour downlink use, customers x r_busy / (S x r_busy): the share of
            its seats sold.
        busy_hour_gb_per_month: Its busy-hour data a month, the engineering usage's, GB.
        offpeak_gb_per_month: Its off-peak data a month, GB.
        active_rate_mbps: Its rate while active, the engineering usage's, Mbps.
        offpeak_downlink_use: customers x r_off(t) / (S x r_busy): its off-peak load against the
            busy-hour budget of the same seats.
    """

    seats: float
    seats_filled: float
    busy_hour_gb_per_month: float
    offpeak_gb_per_month: float
    active_rate_mbps: float
    offpeak_downlink_use: float


@dataclass(frozen=True)
class IotOutcome:
    """An IoT class's own block of a market's outcome in one reported year: a usage, never a count.

    Attributes:
        messages_per_day: The messages a device sends a day.
        bursts_per_day: The 100 KB bursts a device sends a day (0 for minimal-packet IoT).
        bursts_outside_busy_hours: Whether the bursts go off-peak; None for a class that sends
            none (minimal-packet IoT).
        bytes_per_day: B(t), what a device sends a day, bytes.
        uplink_use_busy: The class's term of U(t) in the busy hours: devices x a device's busy-hour
            uplink bits a second / R(t).
        uplink_use_offpeak: Its term of U(t) off-peak.
    """

    messages_per_day: int
    bursts_per_day: int
    bursts_outside_busy_hours: bool | None
    bytes_per_day: int
    uplink_use_busy: float
    uplink_use_offpeak: float


@dataclass(frozen=True)
class ClassOutcome:
    """One class in one market and reported year: what it sells, at what price and service.

    Attributes:
        product_class: The class.
        kind: Terminal (sold up to its seats) or IoT (uncapped, held to IoT's room).
        price_usd_per_month: p_c(t), dollars a month.
        service: v_c(t), its data a month (a terminal) or bytes a day (IoT) over the first
            reported year's.
        demand: D_c(t), customers or devices a month before the seats.
        customers: n_c(t), its customers (a terminal) or devices (IoT), a whole number.
        revenue_musd: n_c x p_c x 12 / 10^6, $M a year.
        price_per_unit: Dollars a GB (a terminal: p over its data a month), a message
            (minimal-packet IoT: p over its messages a month) or a MB (data IoT: p over its bytes a
            month / 10^6).
        terminal: The terminal's block, or None for an IoT class.
        iot: The IoT class's block, or None for a terminal.
    """

    product_class: ProductClass
    kind: ClassKind
    price_usd_per_month: float
    service: float
    demand: float
    customers: float
    revenue_musd: float
    price_per_unit: float
    terminal: TerminalOutcome | None
    iot: IotOutcome | None


@dataclass(frozen=True)
class YearTotals:
    """A reported year's totals in one market (no total of customers: people and devices never add).

    Attributes:
        revenue_musd: Rev(t), $M a year.
        fleet_annual_cost_musd: C(t), the living fleet's annualized build and launch cost, $M.
        margin_pct: (1 - C(t) / Rev(t)) x 100, percent.
        profit_musd: Rev(t) - C(t), $M a year.
        busy_hour_beams_filled: F(t), the terminals' share of the busy-hour beams filled.
        iot_uplink_use_busy: U(t) in the busy hours, a share of the payload room.
        iot_uplink_use_offpeak: U(t) off-peak.
        access_use: The larger period's random-access attempts a second over A(t).
        access_attempts_per_second_per_beam: The same attempts over L(t).
        single_tone_use: The single-tone time used a second over T(t).
        gb_carried_per_year: G(t), GB a year (decimal).
        cost_per_gb_carried_usd: C(t) x 10^6 / G(t), dollars a GB.
    """

    revenue_musd: float
    fleet_annual_cost_musd: float
    margin_pct: float
    profit_musd: float
    busy_hour_beams_filled: float
    iot_uplink_use_busy: float
    iot_uplink_use_offpeak: float
    access_use: float
    access_attempts_per_second_per_beam: float
    single_tone_use: float
    gb_carried_per_year: float
    cost_per_gb_carried_usd: float


@dataclass(frozen=True)
class YearOutcome:
    """One reported year of a market's outcome: the four classes side by side and the totals.

    Attributes:
        year: The fiscal year.
        classes: The four classes, in :class:`~product_case.constants.ProductClass` order.
        totals: The year's totals.
    """

    year: int
    classes: tuple[ClassOutcome, ...]
    totals: YearTotals


@dataclass(frozen=True)
class MarketOutcome:
    """One choice's outcome in one market, every reported year (the headline is the pick's at the
    central market).

    Attributes:
        market: The market.
        usable: True when the market fails no usable test.
        failing_tests: The tests it fails, in :class:`~product_case.constants.UsableTest` order.
        years: Each reported year's outcome, in order.
    """

    market: Market
    usable: bool
    failing_tests: tuple[UsableTest, ...]
    years: tuple[YearOutcome, ...]


@dataclass(frozen=True)
class DrawsFailing(Mapping[UsableTest, int]):
    """The draws failing each usable test: a frozen record of the seven counts that reads as a
    mapping, in :class:`~product_case.constants.UsableTest` order.

    A value, as :class:`~product_case.offers.EndPrices` is: it hashes (the dataclass's hash of the
    seven counts) and compares as a mapping, equal to any mapping with the same items. A draw may
    fail several tests, so the counts overlap.

    Attributes:
        fill: Draws whose busy-hour beams filled fall under the fill floor in some year.
        margin: Draws whose margin falls under the margin floor in some year.
        iot_uplink_busy: Draws whose IoT uplink use in the busy hours passes 1 in some year.
        iot_uplink_offpeak: Draws whose IoT uplink use off-peak passes 1 in some year.
        random_access: Draws whose access use passes 1 in some year.
        single_tone_time: Draws whose single-tone use passes 1 in some year.
        revenue_rising: Draws whose revenue fails to rise strictly between two reported years.
    """

    fill: int
    margin: int
    iot_uplink_busy: int
    iot_uplink_offpeak: int
    random_access: int
    single_tone_time: int
    revenue_rising: int

    def __getitem__(self, test: UsableTest) -> int:
        """The draws failing ``test``; a key that is not a usable test raises ``KeyError``."""
        match test:
            case UsableTest.FILL:
                return self.fill
            case UsableTest.MARGIN:
                return self.margin
            case UsableTest.IOT_UPLINK_BUSY:
                return self.iot_uplink_busy
            case UsableTest.IOT_UPLINK_OFFPEAK:
                return self.iot_uplink_offpeak
            case UsableTest.RANDOM_ACCESS:
                return self.random_access
            case UsableTest.SINGLE_TONE_TIME:
                return self.single_tone_time
            case UsableTest.REVENUE_RISING:
                return self.revenue_rising
        raise KeyError(test)

    def __iter__(self) -> Iterator[UsableTest]:
        """The seven tests, in :class:`~product_case.constants.UsableTest` order."""
        return iter(UsableTest)

    def __len__(self) -> int:
        """Seven: one count per usable test."""
        return len(UsableTest)

    def __eq__(self, other: object) -> bool:
        """Equal to a mapping with the same items, as ``Mapping`` compares."""
        if isinstance(other, Mapping):
            return dict(self.items()) == dict(other.items())
        return NotImplemented

    @classmethod
    def from_mapping(cls, counts: Mapping[UsableTest, int]) -> DrawsFailing:
        """The counts of a mapping that holds every test's.

        Args:
            counts: The draws failing each :class:`~product_case.constants.UsableTest`.

        Returns:
            The frozen counts.

        Raises:
            ValueError: If a test has no count.
        """
        missing = [test for test in UsableTest if test not in counts]
        if missing:
            raise ValueError(
                f"the draws failing need every test; missing {[str(m) for m in missing]}"
            )
        return cls(
            fill=counts[UsableTest.FILL],
            margin=counts[UsableTest.MARGIN],
            iot_uplink_busy=counts[UsableTest.IOT_UPLINK_BUSY],
            iot_uplink_offpeak=counts[UsableTest.IOT_UPLINK_OFFPEAK],
            random_access=counts[UsableTest.RANDOM_ACCESS],
            single_tone_time=counts[UsableTest.SINGLE_TONE_TIME],
            revenue_rising=counts[UsableTest.REVENUE_RISING],
        )


@dataclass(frozen=True)
class ChoiceSummary:
    """A choice over the drawn markets and at the central market (method step 7), and nothing more.

    Attributes:
        choice: The choice.
        usable_draws: The draws in which it is usable.
        usable_share: Usable draws over the draws.
        median_summed_revenue_musd: ``statistics.median`` over its usable draws of Rev(t) summed
            over the reported years (the built-in ``sum``), $M; None when no draw is usable.
        median_last_year_revenue_musd: ``statistics.median`` over its usable draws of the last
            reported year's Rev, $M a year; None when no draw is usable.
        central_revenue_musd: Rev(t) at the central market, one value per reported year, in order.
        central_summed_revenue_musd: Their built-in ``sum``, $M.
        central_usable: True when the central market fails no usable test for it.
        draws_failing: The draws failing each test (a :class:`DrawsFailing`, whatever mapping it is
            built with).
    """

    choice: Choice
    usable_draws: int
    usable_share: float
    median_summed_revenue_musd: float | None
    median_last_year_revenue_musd: float | None
    central_revenue_musd: tuple[float, ...]
    central_summed_revenue_musd: float
    central_usable: bool
    draws_failing: Mapping[UsableTest, int]

    def __post_init__(self) -> None:
        """Hold the draws failing as :class:`DrawsFailing`, so the summary is a value."""
        if not isinstance(self.draws_failing, DrawsFailing):
            object.__setattr__(self, "draws_failing", DrawsFailing.from_mapping(self.draws_failing))


@dataclass(frozen=True)
class Fronts:
    """The two fronts (method step 8): choice ids, most usable first.

    Attributes:
        all_prices: The front over every choice: the context, what lower prices would do.
        at_start_prices: The candidates' front, on which the pick lies.
    """

    all_prices: tuple[int, ...]
    at_start_prices: tuple[int, ...]


@dataclass(frozen=True)
class Pick:
    """The pick among the candidates (method step 8).

    Attributes:
        choice_id: The picked choice's id.
        basis: The robust floor met, or the most usable candidate, warned.
        usage_edges: The IoT classes whose usage scale is the top of the grid's, in class order
            (normally none).
        dominated_in_context_by: The members of the front over every choice at least as usable as
            the pick with a median summed revenue at least as high, one of the two higher, in that
            front's order; empty when the pick is on it.
    """

    choice_id: int
    basis: PickBasis
    usage_edges: tuple[ProductClass, ...]
    dominated_in_context_by: tuple[int, ...]


@dataclass(frozen=True)
class BasisSpread:
    """One spread field over one basis (the pick's usable draws, or all draws) in one year.

    Attributes:
        p10: The 10th percentile, ``statistics.quantiles(values, n=10)``'s first cut (the
            exclusive method); None below :data:`SPREAD_MIN_VALUES` values.
        p50: ``statistics.median``; None below :data:`SPREAD_MIN_VALUES` values.
        p90: The 90th percentile, the last cut; None below :data:`SPREAD_MIN_VALUES` values.
        headline_rank: The headline's mid-rank among the values: the share strictly below plus
            half the share equal.
        null_reason: Why the percentiles are null, or None when they stand.
    """

    p10: float | None
    p50: float | None
    p90: float | None
    headline_rank: float
    null_reason: SpreadNullReason | None


@dataclass(frozen=True)
class EverySeat:
    """For a terminal's customers and revenue: the headline and the draws at every seat.

    Attributes:
        headline_sells_every_seat: True when the headline's customers equal floor(S).
        usable_draws_share: The share of the pick's usable draws whose customers equal floor(S).
        all_draws_share: The share of all draws whose customers equal floor(S).
    """

    headline_sells_every_seat: bool
    usable_draws_share: float
    all_draws_share: float


@dataclass(frozen=True)
class FieldSpread:
    """One headline value's spread in one reported year, over both bases.

    Attributes:
        field: The headline value it spreads.
        usable_draws: Over the pick's usable draws.
        all_draws: Over all draws, the usable test not applied.
        every_seat: For a terminal's customers and revenue; None for every other field.
    """

    field: SpreadField
    usable_draws: BasisSpread
    all_draws: BasisSpread
    every_seat: EverySeat | None


@dataclass(frozen=True)
class YearSpreads:
    """The spreads of one reported year, one entry per :class:`~product_case.constants.SpreadField`.

    Attributes:
        year: The fiscal year.
        fields: The fields, in :class:`~product_case.constants.SpreadField` order.
    """

    year: int
    fields: tuple[FieldSpread, ...]


@dataclass(frozen=True)
class Spreads:
    """The pick's spreads over the drawn markets (method step 9).

    Attributes:
        draws: All drawn markets.
        usable_draws: The pick's usable draws.
        draws_past_iot_room: The drawn markets, all of them, the usable test not applied, in which
            the pick's IoT uplink use in either period, or its access use, passes 1 in at least
            one reported year (a market counts once; the single-tone test is not in the count):
            the all-draw basis's label (montecarlo M2).
        years: Each reported year's spreads, in order.
    """

    draws: int
    usable_draws: int
    draws_past_iot_room: int
    years: tuple[YearSpreads, ...]


# ---------------------------------------------------------------------------
# The markets
# ---------------------------------------------------------------------------


def draw_markets(config: ProductCaseConfig) -> tuple[Market, ...]:
    """The drawn markets, in draw order: round 3's stream (D9).

    ``random.Random(seed)``; for each draw in turn gamma, epsilon then eta, each
    ``uniform(low, high)`` = low + (high - low) x ``random()`` over its range. The seed 20261006
    and 2,000 draws give round 3's markets (the first 0.747400500183258, 1.174028063465549,
    0.45858404147883625; draw 1134 0.66408629754288, 1.355751487391255, 0.493833971708313).

    Args:
        config: The scenario (its ``market`` block: the draws, the seed and the three ranges).

    Returns:
        ``market.draws`` markets.
    """
    market = config.market
    stream = random.Random(market.seed)  # noqa: S311  a reproducible simulation stream (D9), never a secret
    drawn = tuple(
        Market(
            gamma=stream.uniform(market.gamma.low, market.gamma.high),
            epsilon=stream.uniform(market.epsilon.low, market.epsilon.high),
            eta=stream.uniform(market.eta.low, market.eta.high),
        )
        for _ in range(market.draws)
    )
    logger.debug("drew %d markets from seed %d", len(drawn), market.seed)
    return drawn


def _middle(response: ResponseRange) -> float:
    """(low + high) / 2, a range's middle."""
    return (response.low + response.high) / RANGE_ENDS


def central_market(config: ProductCaseConfig) -> Market:
    """The central market: each response at the middle of its range (D7).

    gamma = (gamma_low + gamma_high) / 2, and so epsilon and eta; with the shipped ranges 0.75,
    1.0 and 0.25. Every choice reads in it, and it moves with neither the seed nor the draw count.

    Args:
        config: The scenario (its ``market`` ranges).

    Returns:
        The central market.
    """
    market = config.market
    return Market(
        gamma=_middle(market.gamma), epsilon=_middle(market.epsilon), eta=_middle(market.eta)
    )


# ---------------------------------------------------------------------------
# The evaluation over markets (private: numpy arrays never leave the module)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, eq=False)
class _MarketArrays:
    """The markets' three responses as float64 arrays, one value a market."""

    gamma: _Floats
    epsilon: _Floats
    eta: _Floats

    @classmethod
    def of(cls, markets: Sequence[Market]) -> _MarketArrays:
        """The arrays of a sequence of markets, in its order."""
        return cls(
            gamma=np.array([market.gamma for market in markets], dtype=np.float64),
            epsilon=np.array([market.epsilon for market in markets], dtype=np.float64),
            eta=np.array([market.eta for market in markets], dtype=np.float64),
        )


@dataclass(frozen=True, eq=False)
class _YearArrays:
    """One reported year's numbers in every market, as arrays (each per-class tuple in class order).

    The per-class tuples run small terminal, mounted terminal, minimal-packet IoT, data IoT; the two
    IoT uplink tuples run minimal-packet IoT, data IoT.
    """

    demand: tuple[_Floats, ...]
    sold: tuple[_Floats, ...]
    revenue_by_class: tuple[_Floats, ...]
    uplink_busy_by_class: tuple[_Floats, ...]
    uplink_offpeak_by_class: tuple[_Floats, ...]
    fill: _Floats
    revenue: _Floats
    margin: _Floats
    uplink_busy: _Floats
    uplink_offpeak: _Floats
    access_use: _Floats
    attempts_per_beam: _Floats
    tone_use: _Floats
    gb_carried: _Floats
    cost_per_gb: _Floats


@dataclass(frozen=True, eq=False)
class _Failures:
    """For each usable test, the markets that fail it in some reported year."""

    fill: _Flags
    margin: _Flags
    iot_uplink_busy: _Flags
    iot_uplink_offpeak: _Flags
    random_access: _Flags
    single_tone_time: _Flags
    revenue_rising: _Flags

    def of(self, test: UsableTest) -> _Flags:
        """The markets failing ``test``."""
        match test:
            case UsableTest.FILL:
                return self.fill
            case UsableTest.MARGIN:
                return self.margin
            case UsableTest.IOT_UPLINK_BUSY:
                return self.iot_uplink_busy
            case UsableTest.IOT_UPLINK_OFFPEAK:
                return self.iot_uplink_offpeak
            case UsableTest.RANDOM_ACCESS:
                return self.random_access
            case UsableTest.SINGLE_TONE_TIME:
                return self.single_tone_time
            case UsableTest.REVENUE_RISING:
                return self.revenue_rising
        raise KeyError(test)

    def any_test(self) -> _Flags:
        """The markets failing at least one test (the unusable ones)."""
        failing = np.zeros_like(self.fill)
        for test in UsableTest:
            failing = failing | self.of(test)
        return failing

    def past_iot_room(self) -> _Flags:
        """The markets selling IoT past its uplink room in either period or past its access room."""
        return self.iot_uplink_busy | self.iot_uplink_offpeak | self.random_access


@dataclass(frozen=True, eq=False)
class _Evaluation:
    """A choice evaluated in a set of markets: each reported year's arrays, the failures, usable."""

    years: tuple[_YearArrays, ...]
    failures: _Failures
    usable: _Flags


def _demand(
    anchor: DemandAnchor, scale: float, price: float, service: float, markets: _MarketArrays
) -> _Floats:
    """The demand curve, D_c(t) = N_c x k(t)^gamma x (A_c / p_c(t))^epsilon x v_c(t)^eta, a market.

    Customers (a terminal) or devices (an IoT class) a month before the seats: (N_c, A_c) the
    class's anchor, its customers today at its ARPU today, dollars a month; k(t) the network's
    scale; p_c(t) the price, dollars a month; v_c(t) the service; multiplied left to right, round
    3's order. The worked line round 3 checked by hand, at full precision (round 3's own
    engineering inputs, the strategy's 40-band prototype rows, local; draw 1134; data IoT in FY2036
    at round 3's $4 and $8 pick): 999,000 x 46.72238475413305 ^ 0.66408629754288 x
    ($15.56 / $8) ^ 1.355751487391255 x 1.4900039200313602 ^ 0.493833971708313 =
    38,503,763.15498622..., so 38,503,763 devices, uncapped (the reproduction of round 3 pins
    it).

    Args:
        anchor: The class's anchor (N_c, A_c).
        scale: k(t).
        price: p_c(t), dollars a month.
        service: v_c(t).
        markets: The markets' responses.

    Returns:
        D_c(t) in each market.
    """
    return (
        anchor.customers
        * np.power(scale, markets.gamma)
        * np.power(anchor.arpu_usd_month / price, markets.epsilon)
        * np.power(service, markets.eta)
    )


def _year_arrays(
    network: EngineeringYear,
    offered: YearOffers,
    share: float,
    airtime_s: float,
    markets: _MarketArrays,
) -> _YearArrays:
    """One reported year's numbers in every market (method steps 3 to 5), in round 3's order.

    Args:
        network: The year's network: seats, scale, cost and IoT's rooms.
        offered: The choice's offers in the year (prices, services and per-device loads).
        share: s, the small terminal's share of the busy-hour beams.
        airtime_s: A message's single-tone airtime at its high end, seconds.
        markets: The markets' responses.

    Returns:
        The year's arrays.
    """
    small, mounted = offered.small_terminal, offered.mounted_terminal
    minimal, data = offered.minimal_packet_iot, offered.data_iot
    demand = tuple(
        _demand(
            DEMAND_ANCHORS[offer.product_class],
            network.network_scale,
            offer.price_usd_month,
            offer.service,
            markets,
        )
        for offer in offered.classes
    )
    small_seats = network.seats_small_terminal
    mounted_seats = network.seats_mounted_terminal
    n_small = np.floor(np.minimum(demand[0], small_seats))
    n_mounted = np.floor(np.minimum(demand[1], mounted_seats))
    n_minimal = np.floor(demand[2])
    n_data = np.floor(demand[3])
    sold = (n_small, n_mounted, n_minimal, n_data)
    fill = share * n_small / small_seats + (1.0 - share) * n_mounted / mounted_seats
    revenue = (
        (
            n_small * small.price_usd_month
            + n_mounted * mounted.price_usd_month
            + n_minimal * minimal.price_usd_month
            + n_data * data.price_usd_month
        )
        * MONTHS_PER_YEAR
        / DOLLARS_PER_MILLION
    )
    revenue_by_class = tuple(
        count * offer.price_usd_month * MONTHS_PER_YEAR / DOLLARS_PER_MILLION
        for count, offer in zip(sold, offered.classes, strict=True)
    )
    room = network.iot_payload_bits_per_second
    busy_by_class = (
        n_minimal * (minimal.uplink_bits_per_second_busy / room),
        n_data * (data.uplink_bits_per_second_busy / room),
    )
    offpeak_by_class = (
        n_minimal * (minimal.uplink_bits_per_second_offpeak / room),
        n_data * (data.uplink_bits_per_second_offpeak / room),
    )
    attempts = np.maximum(
        n_minimal * minimal.access_attempts_per_second_busy
        + n_data * data.access_attempts_per_second_busy,
        n_minimal * minimal.access_attempts_per_second_offpeak
        + n_data * data.access_attempts_per_second_offpeak,
    )
    tone_use = (
        (
            n_minimal * minimal.single_tone_messages_per_second
            + n_data * data.single_tone_messages_per_second
        )
        * airtime_s
        / network.iot_single_tone_seconds_per_second
    )
    gb_carried = (
        n_small * small.gb_per_month + n_mounted * mounted.gb_per_month
    ) * MONTHS_PER_YEAR + (
        n_minimal * minimal.bytes_per_day + n_data * data.bytes_per_day
    ) * DAYS_PER_MONTH * MONTHS_PER_YEAR / BYTES_PER_GB
    return _YearArrays(
        demand=demand,
        sold=sold,
        revenue_by_class=revenue_by_class,
        uplink_busy_by_class=busy_by_class,
        uplink_offpeak_by_class=offpeak_by_class,
        fill=fill,
        revenue=revenue,
        margin=1.0 - network.annual_cost_musd / revenue,
        uplink_busy=busy_by_class[0] + busy_by_class[1],
        uplink_offpeak=offpeak_by_class[0] + offpeak_by_class[1],
        access_use=attempts / network.iot_access_attempts_per_second,
        attempts_per_beam=attempts / network.phone_useful_beams,
        tone_use=tone_use,
        gb_carried=gb_carried,
        cost_per_gb=network.annual_cost_musd * DOLLARS_PER_MILLION / gb_carried,
    )


def _any_year(years: Sequence[_YearArrays], fails: Callable[[_YearArrays], _Flags]) -> _Flags:
    """The markets in which ``fails`` holds in at least one reported year."""
    failing = fails(years[0])
    for year in years[1:]:
        failing = failing | fails(year)
    return failing


def _failures(years: Sequence[_YearArrays], fill_floor: float, margin_floor: float) -> _Failures:
    """Each usable test's failing markets (method step 6): a test's condition not held fails it.

    Args:
        years: Each reported year's arrays, in order (at least two).
        fill_floor: The fill floor, a share of the busy-hour beams.
        margin_floor: The margin floor, a fraction (the scenario's percent over 100).

    Returns:
        The failing markets of each test.
    """
    rising = ~(years[1].revenue > years[0].revenue)
    for earlier, later in pairwise(years[1:]):
        rising = rising | ~(later.revenue > earlier.revenue)
    return _Failures(
        fill=_any_year(years, lambda year: ~(year.fill >= fill_floor)),
        margin=_any_year(years, lambda year: ~(year.margin >= margin_floor)),
        iot_uplink_busy=_any_year(years, lambda year: ~(year.uplink_busy <= FULL_USE)),
        iot_uplink_offpeak=_any_year(years, lambda year: ~(year.uplink_offpeak <= FULL_USE)),
        random_access=_any_year(years, lambda year: ~(year.access_use <= FULL_USE)),
        single_tone_time=_any_year(years, lambda year: ~(year.tone_use <= FULL_USE)),
        revenue_rising=rising,
    )


def _evaluate(
    config: ProductCaseConfig,
    engineering: EngineeringView,
    offers: ChoiceOffers,
    markets: _MarketArrays,
) -> _Evaluation:
    """One choice in every market of ``markets``: each year's numbers, the failures, usable.

    numpy's floating-point warnings are off here: a setting past what a float holds gives an
    infinity or a NaN, never an exception, and the checks refuse the run that holds one.
    """
    with np.errstate(all="ignore"):
        years = tuple(
            _year_arrays(
                network,
                offered,
                engineering.small_terminal_share,
                engineering.airtime_high_s,
                markets,
            )
            for network, offered in zip(engineering.years, offers.years, strict=True)
        )
        failures = _failures(years, config.floors.fill, config.floors.margin_pct / PERCENT)
    return _Evaluation(years=years, failures=failures, usable=~failures.any_test())


# ---------------------------------------------------------------------------
# One market: the outcome the headline publishes
# ---------------------------------------------------------------------------


def _terminal_outcome(
    offer: TerminalOffer,
    arrays: _YearArrays,
    position: int,
    seats: float,
    active_rate_mbps: float,
) -> ClassOutcome:
    """A terminal's outcome in a one-market evaluation's year (its arrays hold one value)."""
    customers = float(arrays.sold[position][0])
    busy_budget = seats * offer.busy_hour_rate_bps
    return ClassOutcome(
        product_class=offer.product_class,
        kind=CLASS_KIND[offer.product_class],
        price_usd_per_month=offer.price_usd_month,
        service=offer.service,
        demand=float(arrays.demand[position][0]),
        customers=customers,
        revenue_musd=float(arrays.revenue_by_class[position][0]),
        price_per_unit=offer.price_usd_month / offer.gb_per_month,
        terminal=TerminalOutcome(
            seats=seats,
            seats_filled=customers * offer.busy_hour_rate_bps / busy_budget,
            busy_hour_gb_per_month=offer.busy_hour_gb_per_month,
            offpeak_gb_per_month=offer.offpeak_gb_per_month,
            active_rate_mbps=active_rate_mbps,
            offpeak_downlink_use=customers * offer.offpeak_rate_bps / busy_budget,
        ),
        iot=None,
    )


def _iot_price_per_unit(offer: IotOffer) -> float:
    """Dollars a message (minimal-packet IoT) or a MB (data IoT): the price over a month's usage."""
    if offer.product_class is ProductClass.MINIMAL_PACKET_IOT:
        return offer.price_usd_month / (offer.messages_per_day * DAYS_PER_MONTH)
    return offer.price_usd_month / (offer.bytes_per_day * DAYS_PER_MONTH / BYTES_PER_MB)


def _iot_outcome(
    offer: IotOffer, arrays: _YearArrays, position: int, iot_position: int
) -> ClassOutcome:
    """An IoT class's outcome in a one-market evaluation's year (its arrays hold one value)."""
    return ClassOutcome(
        product_class=offer.product_class,
        kind=CLASS_KIND[offer.product_class],
        price_usd_per_month=offer.price_usd_month,
        service=offer.service,
        demand=float(arrays.demand[position][0]),
        customers=float(arrays.sold[position][0]),
        revenue_musd=float(arrays.revenue_by_class[position][0]),
        price_per_unit=_iot_price_per_unit(offer),
        terminal=None,
        iot=IotOutcome(
            messages_per_day=offer.messages_per_day,
            bursts_per_day=offer.bursts_per_day,
            bursts_outside_busy_hours=offer.bursts_outside_busy_hours,
            bytes_per_day=offer.bytes_per_day,
            uplink_use_busy=float(arrays.uplink_busy_by_class[iot_position][0]),
            uplink_use_offpeak=float(arrays.uplink_offpeak_by_class[iot_position][0]),
        ),
    )


def _year_outcome(
    arrays: _YearArrays,
    offered: YearOffers,
    network: EngineeringYear,
    engineering: EngineeringView,
) -> YearOutcome:
    """One reported year of a one-market evaluation as plain numbers."""
    revenue = float(arrays.revenue[0])
    return YearOutcome(
        year=offered.year,
        classes=(
            _terminal_outcome(
                offered.small_terminal,
                arrays,
                0,
                network.seats_small_terminal,
                engineering.small_terminal_pool.active_user_rate_mbps,
            ),
            _terminal_outcome(
                offered.mounted_terminal,
                arrays,
                1,
                network.seats_mounted_terminal,
                engineering.mounted_terminal_pool.active_user_rate_mbps,
            ),
            _iot_outcome(offered.minimal_packet_iot, arrays, 2, 0),
            _iot_outcome(offered.data_iot, arrays, 3, 1),
        ),
        totals=YearTotals(
            revenue_musd=revenue,
            fleet_annual_cost_musd=network.annual_cost_musd,
            margin_pct=float(arrays.margin[0] * PERCENT),
            profit_musd=revenue - network.annual_cost_musd,
            busy_hour_beams_filled=float(arrays.fill[0]),
            iot_uplink_use_busy=float(arrays.uplink_busy[0]),
            iot_uplink_use_offpeak=float(arrays.uplink_offpeak[0]),
            access_use=float(arrays.access_use[0]),
            access_attempts_per_second_per_beam=float(arrays.attempts_per_beam[0]),
            single_tone_use=float(arrays.tone_use[0]),
            gb_carried_per_year=float(arrays.gb_carried[0]),
            cost_per_gb_carried_usd=float(arrays.cost_per_gb[0]),
        ),
    )


def _market_outcome(
    config: ProductCaseConfig,
    engineering: EngineeringView,
    offers: ChoiceOffers,
    market: Market,
) -> MarketOutcome:
    """A choice's offers in one market, through the draws' evaluation on arrays of length one."""
    evaluation = _evaluate(config, engineering, offers, _MarketArrays.of((market,)))
    failing = tuple(test for test in UsableTest if bool(evaluation.failures.of(test)[0]))
    return MarketOutcome(
        market=market,
        usable=not failing,
        failing_tests=failing,
        years=tuple(
            _year_outcome(arrays, offered, network, engineering)
            for arrays, offered, network in zip(
                evaluation.years, offers.years, engineering.years, strict=True
            )
        ),
    )


def outcome_in_market(
    config: ProductCaseConfig,
    engineering: EngineeringView,
    choice: Choice,
    market: Market,
) -> MarketOutcome:
    """One choice in one market, every reported year: the four classes side by side and the totals.

    The same evaluation as the draws (arrays of length one), so a market among the draws reads
    the same here: the headline is the pick's outcome at :func:`central_market`, and the
    reproduction of round 3 reads draw 1134's counts through it.

    Args:
        config: The scenario.
        engineering: The engineering view of the scenario's reported years.
        choice: A choice of the grid (:func:`~product_case.offers.choice_grid`).
        market: The market.

    Returns:
        The choice's outcome in the market.

    Raises:
        product_case.offers.OfferError: As :func:`~product_case.offers.choice_offers`.
    """
    return _market_outcome(config, engineering, choice_offers(config, engineering, choice), market)


# ---------------------------------------------------------------------------
# Each choice over the draws (method step 7)
# ---------------------------------------------------------------------------


def _summary(
    config: ProductCaseConfig,
    engineering: EngineeringView,
    offers: ChoiceOffers,
    markets: _MarketArrays,
    central: _MarketArrays,
) -> ChoiceSummary:
    """One choice over the drawn markets and at the central market, reduced to its summary."""
    drawn = _evaluate(config, engineering, offers, markets)
    revenue_by_draw = np.column_stack([year.revenue for year in drawn.years])
    usable_rows: list[list[float]] = revenue_by_draw[drawn.usable].tolist()
    summed = [sum(row) for row in usable_rows]
    last_year = [row[-1] for row in usable_rows]
    at_centre = _evaluate(config, engineering, offers, central)
    central_revenue = tuple(float(year.revenue[0]) for year in at_centre.years)
    draws = len(drawn.usable)
    return ChoiceSummary(
        choice=offers.choice,
        usable_draws=len(usable_rows),
        usable_share=len(usable_rows) / draws,
        median_summed_revenue_musd=statistics.median(summed) if summed else None,
        median_last_year_revenue_musd=statistics.median(last_year) if last_year else None,
        central_revenue_musd=central_revenue,
        central_summed_revenue_musd=sum(central_revenue),
        central_usable=bool(at_centre.usable[0]),
        draws_failing=DrawsFailing.from_mapping(
            {test: int(np.count_nonzero(drawn.failures.of(test))) for test in UsableTest}
        ),
    )


def summarize_grid(
    config: ProductCaseConfig,
    engineering: EngineeringView,
    grid: Sequence[ChoiceOffers],
    markets: Sequence[Market],
) -> tuple[ChoiceSummary, ...]:
    """Each choice over the drawn markets and at the central market (method step 7).

    Each choice is evaluated over every draw at once and at the central market through the same
    evaluation, and reduced to its :class:`ChoiceSummary`: the usable draws U and share U / draws;
    the medians over the usable draws of the summed revenue (the built-in ``sum`` of Rev(t) over
    the reported years, in year order) and of the last reported year's Rev; the draws failing each
    test; the central market's Rev per reported year, summed, and its usable flag.

    Args:
        config: The scenario (its floors).
        engineering: The engineering view of the scenario's reported years.
        grid: Every choice with its offers, in the grid's order
            (:func:`~product_case.offers.grid_offers`).
        markets: The drawn markets (:func:`draw_markets`).

    Returns:
        One summary per choice, in the grid's order.
    """
    drawn = _MarketArrays.of(markets)
    central = _MarketArrays.of((central_market(config),))
    summaries = tuple(_summary(config, engineering, offers, drawn, central) for offers in grid)
    logger.debug(
        "summarized %d choices over %d markets: %d usable in at least one",
        len(summaries),
        len(markets),
        sum(1 for summary in summaries if summary.usable_draws),
    )
    return summaries


# ---------------------------------------------------------------------------
# The fronts and the pick (method step 8)
# ---------------------------------------------------------------------------


def _median(summary: ChoiceSummary) -> float:
    """The summary's median summed revenue; a choice with no usable draw has none."""
    median = summary.median_summed_revenue_musd
    if median is None:
        raise ValueError(
            f"choice {summary.choice.choice_id} is usable in no draw, so it has no median "
            "summed revenue and stands on no front"
        )
    return median


def _front(summaries: Sequence[ChoiceSummary]) -> tuple[int, ...]:
    """Round 3's sweep over ``summaries``: the members' ids, most usable first."""
    ranked = sorted(
        (summary for summary in summaries if summary.usable_draws),
        key=lambda summary: (-summary.usable_draws, -_median(summary), summary.choice.choice_id),
    )
    members: list[int] = []
    best = -math.inf
    for summary in ranked:
        median = _median(summary)
        if median > best:
            members.append(summary.choice.choice_id)
            best = median
    return tuple(members)


def fronts_of(summaries: Sequence[ChoiceSummary]) -> Fronts:
    """The front over every choice and the candidates' front (method step 8; D16, D19, D21).

    A front is round 3's sweep: the choices usable in at least one draw, sorted by usable share,
    then median summed revenue, both descending, then the grid's order (the usable draws stand
    for the share: every choice shares the draws); a choice joins when its median is strictly
    above every earlier member's. So no member is beaten by another choice on both axes, and of
    exact ties the earliest in the grid's order stands for them.

    Args:
        summaries: Every choice's summary, in the grid's order.

    Returns:
        Both fronts: over every choice (the context) and over the candidates.
    """
    return Fronts(
        all_prices=_front(summaries),
        at_start_prices=_front(
            [summary for summary in summaries if summary.choice.at_start_prices]
        ),
    )


def _usage_edges(choice: Choice, config: ProductCaseConfig) -> tuple[ProductClass, ...]:
    """The IoT classes whose usage scale is the top of its list, in class order."""
    tops = (
        (
            ProductClass.MINIMAL_PACKET_IOT,
            choice.minimal_packet_scale,
            config.usage.minimal_packet_iot.scales[-1],
        ),
        (ProductClass.DATA_IOT, choice.data_iot_scale, config.usage.data_iot.scales[-1]),
    )
    return tuple(product_class for product_class, scale, top in tops if scale == top)


def _beats(member: ChoiceSummary, pick: ChoiceSummary) -> bool:
    """At least as usable, a median at least as high, one of the two higher."""
    member_median, pick_median = _median(member), _median(pick)
    at_least = member.usable_draws >= pick.usable_draws and member_median >= pick_median
    higher = member.usable_draws > pick.usable_draws or member_median > pick_median
    return at_least and higher


def pick_of(
    summaries: Sequence[ChoiceSummary], fronts: Fronts, config: ProductCaseConfig
) -> Pick | None:
    """The pick among the candidates (method step 8; D17, D19).

    Among the candidates (every price at its start price) usable in at least the robust floor's
    share of the draws, the highest median summed revenue, ties to the higher usable share, then
    the earlier choice (``robust_floor_met``); when none reaches the floor, the candidates'
    front's first member, the most usable candidate, ties to the higher median, then the grid's
    order (``most_usable_fallback``, which the checks warn of); when no candidate is usable in any
    draw, no pick. Either branch lies on the candidates' front. ``usage_edges`` names each IoT
    class whose usage scale is its list's top; ``dominated_in_context_by`` the members of the
    front over every choice that beat the pick (at least as usable, a median at least as high,
    one of them higher), whose list is short since any choice that beats the pick is beaten or
    matched by such a member.

    Args:
        summaries: Every choice's summary, in the grid's order.
        fronts: Their fronts (:func:`fronts_of`).
        config: The scenario (its robust floor and usage scales).

    Returns:
        The pick, or None when no candidate is usable in any draw (state ``no_usable_choice``).
    """
    by_id = {summary.choice.choice_id: summary for summary in summaries}
    robust = [
        summary
        for summary in summaries
        if summary.choice.at_start_prices
        and summary.usable_draws
        and summary.usable_share >= config.floors.robust
    ]
    if robust:
        chosen = max(
            robust,
            key=lambda summary: (
                _median(summary),
                summary.usable_draws,
                -summary.choice.choice_id,
            ),
        )
        basis = PickBasis.ROBUST_FLOOR_MET
    elif fronts.at_start_prices:
        chosen = by_id[fronts.at_start_prices[0]]
        basis = PickBasis.MOST_USABLE_FALLBACK
    else:
        logger.debug("no candidate is usable in any draw: no pick")
        return None
    return Pick(
        choice_id=chosen.choice.choice_id,
        basis=basis,
        usage_edges=_usage_edges(chosen.choice, config),
        dominated_in_context_by=tuple(
            member for member in fronts.all_prices if _beats(by_id[member], chosen)
        ),
    )


# ---------------------------------------------------------------------------
# The pick's spreads (method step 9)
# ---------------------------------------------------------------------------


def _field_values(field: SpreadField, arrays: _YearArrays) -> _Floats:
    """The headline value ``field`` names, in every market of an evaluation's year."""
    match field:
        case SpreadField.SMALL_TERMINAL_CUSTOMERS:
            return arrays.sold[0]
        case SpreadField.SMALL_TERMINAL_REVENUE:
            return arrays.revenue_by_class[0]
        case SpreadField.MOUNTED_TERMINAL_CUSTOMERS:
            return arrays.sold[1]
        case SpreadField.MOUNTED_TERMINAL_REVENUE:
            return arrays.revenue_by_class[1]
        case SpreadField.MINIMAL_PACKET_IOT_CUSTOMERS:
            return arrays.sold[2]
        case SpreadField.MINIMAL_PACKET_IOT_REVENUE:
            return arrays.revenue_by_class[2]
        case SpreadField.DATA_IOT_CUSTOMERS:
            return arrays.sold[3]
        case SpreadField.DATA_IOT_REVENUE:
            return arrays.revenue_by_class[3]
        case SpreadField.REVENUE:
            return arrays.revenue
        case SpreadField.MARGIN:
            return arrays.margin * PERCENT
        case SpreadField.IOT_UPLINK_USE_BUSY:
            return arrays.uplink_busy
        case SpreadField.IOT_UPLINK_USE_OFFPEAK:
            return arrays.uplink_offpeak
    raise KeyError(field)


def _terminal_position(field: SpreadField) -> int | None:
    """The terminal a customers or revenue field belongs to (0 small, 1 mounted), else None."""
    match field:
        case SpreadField.SMALL_TERMINAL_CUSTOMERS | SpreadField.SMALL_TERMINAL_REVENUE:
            return 0
        case SpreadField.MOUNTED_TERMINAL_CUSTOMERS | SpreadField.MOUNTED_TERMINAL_REVENUE:
            return 1
    return None


def _basis_spread(values: _Floats, headline: float) -> BasisSpread:
    """The percentiles of ``values`` and the headline's mid-rank among them (D10).

    rank = (below + 0.5 x equal) / count, with below and equal the values strictly below and equal
    to the headline; p50 by ``statistics.median``; p10 and p90 the first and last cut of
    ``statistics.quantiles(values, n=10)`` (exclusive); the three null below
    :data:`SPREAD_MIN_VALUES` values, with the reason.
    """
    count = int(values.size)
    below = int(np.count_nonzero(values < headline))
    equal = int(np.count_nonzero(values == headline))
    rank = (below + TIE_WEIGHT * equal) / count
    if count < SPREAD_MIN_VALUES:
        return BasisSpread(
            p10=None,
            p50=None,
            p90=None,
            headline_rank=rank,
            null_reason=SpreadNullReason.TOO_FEW_USABLE_DRAWS,
        )
    listed: list[float] = values.tolist()
    cuts = statistics.quantiles(listed, n=PERCENTILE_GROUPS)
    return BasisSpread(
        p10=cuts[0],
        p50=statistics.median(listed),
        p90=cuts[-1],
        headline_rank=rank,
        null_reason=None,
    )


def _every_seat(
    field: SpreadField,
    drawn: _YearArrays,
    centre: _YearArrays,
    network: EngineeringYear,
    usable: _Flags,
) -> EverySeat | None:
    """For a terminal's customers or revenue: the headline and the draws at floor(S); else None."""
    position = _terminal_position(field)
    if position is None:
        return None
    seats = network.seats_small_terminal if position == 0 else network.seats_mounted_terminal
    every = float(math.floor(seats))
    at_every_seat = drawn.sold[position] == every
    return EverySeat(
        headline_sells_every_seat=bool(centre.sold[position][0] == every),
        usable_draws_share=int(np.count_nonzero(at_every_seat[usable]))
        / int(np.count_nonzero(usable)),
        all_draws_share=int(np.count_nonzero(at_every_seat)) / int(at_every_seat.size),
    )


def spreads_of(
    config: ProductCaseConfig,
    engineering: EngineeringView,
    choice: Choice,
    markets: Sequence[Market],
    headline: MarketOutcome,
) -> Spreads:
    """The pick's spreads over the drawn markets (method step 9; D10).

    The pick is evaluated again over the draws and at the headline's market, through the same
    evaluation. Per reported year and :class:`~product_case.constants.SpreadField`, over the pick's
    usable draws (the percentiles null below :data:`SPREAD_MIN_VALUES`, with the reason) and over
    all draws: the 10th, 50th and 90th percentiles and the headline's mid-rank; for a terminal's
    customers and revenue, whether the headline sells every seat (customers = floor(S)) and the
    share of each basis's draws that do. Beside them, the all-draw basis's label count: the draws
    in which the pick sells IoT past its uplink room in either period or past its access room in
    some reported year (montecarlo M2; the single-tone test is not in it).

    Args:
        config: The scenario.
        engineering: The engineering view of the scenario's reported years.
        choice: The pick's choice; it has at least one usable draw.
        markets: The drawn markets (:func:`draw_markets`).
        headline: The pick's outcome at the central market (:func:`outcome_in_market`): its
            market is the one the ranks are read in.

    Returns:
        The pick's spreads.

    Raises:
        ZeroDivisionError: If the choice is usable in no draw (a pick always is in one).
        product_case.offers.OfferError: As :func:`~product_case.offers.choice_offers`.
    """
    offers = choice_offers(config, engineering, choice)
    drawn = _evaluate(config, engineering, offers, _MarketArrays.of(markets))
    centre = _evaluate(config, engineering, offers, _MarketArrays.of((headline.market,)))
    years: list[YearSpreads] = []
    for drawn_year, centre_year, network in zip(
        drawn.years, centre.years, engineering.years, strict=True
    ):
        fields: list[FieldSpread] = []
        for field in SpreadField:
            values = _field_values(field, drawn_year)
            headline_value = float(_field_values(field, centre_year)[0])
            fields.append(
                FieldSpread(
                    field=field,
                    usable_draws=_basis_spread(values[drawn.usable], headline_value),
                    all_draws=_basis_spread(values, headline_value),
                    every_seat=_every_seat(field, drawn_year, centre_year, network, drawn.usable),
                )
            )
        years.append(YearSpreads(year=network.year, fields=tuple(fields)))
    return Spreads(
        draws=len(markets),
        usable_draws=int(np.count_nonzero(drawn.usable)),
        draws_past_iot_room=int(np.count_nonzero(drawn.failures.past_iot_room())),
        years=tuple(years),
    )


__all__ = [
    "FULL_USE",
    "PERCENTILE_GROUPS",
    "RANGE_ENDS",
    "SPREAD_MIN_VALUES",
    "TIE_WEIGHT",
    "BasisSpread",
    "ChoiceSummary",
    "ClassOutcome",
    "DrawsFailing",
    "EverySeat",
    "FieldSpread",
    "Fronts",
    "IotOutcome",
    "Market",
    "MarketOutcome",
    "Pick",
    "Spreads",
    "TerminalOutcome",
    "YearOutcome",
    "YearSpreads",
    "YearTotals",
    "central_market",
    "draw_markets",
    "fronts_of",
    "outcome_in_market",
    "pick_of",
    "spreads_of",
    "summarize_grid",
]
