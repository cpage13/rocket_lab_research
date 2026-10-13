"""B2, the offers: the choice grid, and what each choice sells each reported year, before a market.

Pure arithmetic on the scenario and the engineering view (method step 2). The grid holds every
combination of the small terminal's end prices, the mounted terminal's, minimal-packet IoT's,
minimal-packet IoT's usage scales and data IoT's, in that fixed order, the last varying fastest;
a choice's id is its index. A choice is a candidate (``at_start_prices``) when every end price
equals its start price: the investor's prices held flat. Data IoT's price is twice minimal-packet
IoT's in every year and choice (the investor's proportion, D15), never a setting.

Per choice, reported year t (t0 the first, t1 the last) and class:

- the price on its line, p(t) = p_start + (p_end - p_start) x (t - t0) / (t1 - t0), dollars a
  month, in fiscal years (montecarlo m3), data IoT's 2 x minimal-packet IoT's;
- a terminal's data a month: its busy-hour part the engineering usage's (the view's 2.7 or 27 GB,
  so its seats are the engineering case's), its off-peak part the scenario's monthly total less
  that (a total below the busy-hour part is refused, naming the field); its busy-hour rate
  r_busy = busy GB x 10^9 x 8 / (4 h x 3,600 s x 30 days) and off-peak rate
  r_off(t) = off-peak GB x 10^9 x 8 / (20 h x 3,600 s x 30 days), bits a second, the rates a
  terminal's downlink use is measured with;
- an IoT class's usage: its scenario path (minimal-packet IoT's messages a day, data IoT's bursts
  a day; data IoT's messages are one value) times the choice's usage scale's line factor
  f(t) = 1 + (scale - 1) x (t - t0) / (t1 - t0), the product taken exactly (the scale at its
  decimal value) and rounded half up by :func:`common.cadence.round_half_up` (x8 in FY2033 of
  FY2031 to FY2036: 72 x 3.8 = 273.6, so 274 messages, never the 240 a reported-year index
  would give; an exact half, 50 x 1.15 = 57.5, rounds up to 58); its bytes a day
  B(t) = messages x 340 + bursts x 100,000 (the sizes the engineering artifact publishes); its
  per-device loads: the uplink bits a second and random-access attempts a second in the busy
  hours and off-peak (messages spread over the day; bursts over the day, or over the 20
  off-peak hours when they go outside the busy hours; one attempt per message or burst) and its
  single-tone messages a second (its messages over the day);
- the service v(t): the data a month in all (a terminal) or the bytes a day (an IoT class) over
  the first reported year's at the same choice, the service term of the demand curve.

The operation order of every float follows round 3 of the product case's scratch exploration
(local), so the reproduction of round 3 lands on its counts; the usage line alone is exact,
which moves no usage of round 3's grids or the shipped grid (each product 0.1 or more from a
half). Every record is frozen and a value; nothing is kept in a module-level variable: every
price, path and scale comes from the config.
"""

from __future__ import annotations

import logging
import math
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from fractions import Fraction
from itertools import product

from common.cadence import round_half_up
from product_case.config import ClassPriceDials, ProductCaseConfig
from product_case.constants import (
    BITS_PER_BYTE,
    BUSY_HOURS_PER_DAY,
    BYTES_PER_GB,
    DATA_IOT_PRICE_MULTIPLE,
    DAYS_PER_MONTH,
    OFFPEAK_HOURS_PER_DAY,
    RELATIVE_TOLERANCE,
    SECONDS_PER_DAY,
    SECONDS_PER_HOUR,
    TERMINAL_DEVICE_CLASS,
    USAGE_SCALE_START,
    ProductClass,
)
from product_case.engineering import EngineeringView

logger = logging.getLogger(__name__)


class OfferError(ValueError):
    """The scenario's usage cannot be offered on the engineering network.

    Raised when a terminal's monthly total in a reported year is below its busy-hour part (the
    engineering usage) by more than the invariants' tolerance, or a usage, a price or a rate is
    not finite (a setting too large for the arithmetic), each naming the field and the year; or
    when the view's years are not the scenario's reported years.
    """


@dataclass(frozen=True)
class EndPrices(Mapping[ProductClass, float]):
    """Each class's end price: a frozen record of the four prices that reads as a mapping.

    A small immutable ``Mapping[ProductClass, float]`` in :class:`ProductClass` order that is also
    a value: it hashes, deep-copies and pickles, and ``dataclasses.asdict`` writes it as the four
    prices by class name, so a :class:`Choice` that holds it is a value too (a set or a cache can
    key on a choice).

    Attributes:
        small_terminal: The small terminal's price a month by the last reported year.
        mounted_terminal: The mounted terminal's.
        minimal_packet_iot: Minimal-packet IoT's.
        data_iot: Data IoT's (in the grid, twice minimal-packet IoT's).
    """

    small_terminal: float
    mounted_terminal: float
    minimal_packet_iot: float
    data_iot: float

    def __getitem__(self, product_class: ProductClass) -> float:
        """The class's end price; a key that is not a product class raises ``KeyError``."""
        match product_class:
            case ProductClass.SMALL_TERMINAL:
                return self.small_terminal
            case ProductClass.MOUNTED_TERMINAL:
                return self.mounted_terminal
            case ProductClass.MINIMAL_PACKET_IOT:
                return self.minimal_packet_iot
            case ProductClass.DATA_IOT:
                return self.data_iot
        raise KeyError(product_class)

    def __iter__(self) -> Iterator[ProductClass]:
        """The four classes, in :class:`ProductClass` order."""
        return iter(ProductClass)

    def __len__(self) -> int:
        """Four: one end price per class."""
        return len(ProductClass)

    @classmethod
    def from_mapping(cls, prices: Mapping[ProductClass, float]) -> EndPrices:
        """The end prices of a mapping that holds every class's.

        Args:
            prices: An end price per :class:`ProductClass`.

        Returns:
            The frozen end prices.

        Raises:
            ValueError: If a class has no end price.
        """
        missing = [product_class for product_class in ProductClass if product_class not in prices]
        if missing:
            raise ValueError(
                f"a choice's end prices need every class; missing {[str(m) for m in missing]}"
            )
        return cls(
            small_terminal=prices[ProductClass.SMALL_TERMINAL],
            mounted_terminal=prices[ProductClass.MOUNTED_TERMINAL],
            minimal_packet_iot=prices[ProductClass.MINIMAL_PACKET_IOT],
            data_iot=prices[ProductClass.DATA_IOT],
        )


@dataclass(frozen=True)
class Choice:
    """One choice of the grid: each class's end price and each IoT class's usage scale.

    A value: it hashes, deep-copies, pickles and passes ``dataclasses.asdict``, whatever mapping
    of end prices it is built with, since it holds them as :class:`EndPrices`.

    Attributes:
        choice_id: The choice's index in the grid's fixed order.
        end_prices: Each class's price a month by the last reported year, in
            :class:`ProductClass` order (data IoT's twice minimal-packet IoT's); held as the
            immutable :class:`EndPrices`.
        minimal_packet_scale: Minimal-packet IoT's usage scale by the last reported year.
        data_iot_scale: Data IoT's usage scale by the last reported year.
        at_start_prices: True when every end price equals its start price (a candidate).
    """

    choice_id: int
    end_prices: Mapping[ProductClass, float]
    minimal_packet_scale: float
    data_iot_scale: float
    at_start_prices: bool

    def __post_init__(self) -> None:
        """Hold the end prices as :class:`EndPrices`, so the choice is a value."""
        if not isinstance(self.end_prices, EndPrices):
            object.__setattr__(self, "end_prices", EndPrices.from_mapping(self.end_prices))


@dataclass(frozen=True)
class TerminalOffer:
    """What a terminal sells in one reported year at one choice.

    Attributes:
        product_class: The terminal class.
        price_usd_month: p(t), dollars a month.
        gb_per_month: The data a month in all, GB.
        busy_hour_gb_per_month: The busy-hour part, the engineering usage's, GB a month.
        offpeak_gb_per_month: The rest, off-peak, GB a month.
        service: v(t), the data a month in all over the first reported year's.
        busy_hour_rate_bps: r_busy, the busy-hour data a month over 4 h x 30 days, bits a second.
        offpeak_rate_bps: r_off(t), the off-peak data a month over 20 h x 30 days, bits a second.
    """

    product_class: ProductClass
    price_usd_month: float
    gb_per_month: float
    busy_hour_gb_per_month: float
    offpeak_gb_per_month: float
    service: float
    busy_hour_rate_bps: float
    offpeak_rate_bps: float


@dataclass(frozen=True)
class IotOffer:
    """What an IoT class sells in one reported year at one choice: a usage, never a count.

    Attributes:
        product_class: The IoT class.
        price_usd_month: p(t), dollars a month.
        messages_per_day: The messages a device sends a day.
        bursts_per_day: The 100 KB bursts a device sends a day (0 for minimal-packet IoT).
        bursts_outside_busy_hours: Whether the bursts go outside the busy hours.
        bytes_per_day: B(t), what a device sends a day, bytes.
        service: v(t), B(t) over the first reported year's.
        uplink_bits_per_second_busy: A device's uplink load in the busy hours, bits a second.
        uplink_bits_per_second_offpeak: A device's uplink load off-peak, bits a second.
        access_attempts_per_second_busy: A device's random-access attempts a second, busy hours.
        access_attempts_per_second_offpeak: A device's random-access attempts a second, off-peak.
        single_tone_messages_per_second: A device's messages a second, each holding a tone.
    """

    product_class: ProductClass
    price_usd_month: float
    messages_per_day: int
    bursts_per_day: int
    bursts_outside_busy_hours: bool
    bytes_per_day: int
    service: float
    uplink_bits_per_second_busy: float
    uplink_bits_per_second_offpeak: float
    access_attempts_per_second_busy: float
    access_attempts_per_second_offpeak: float
    single_tone_messages_per_second: float


@dataclass(frozen=True)
class YearOffers:
    """One choice's offers in one reported year, the four classes side by side.

    Attributes:
        year: The reported fiscal year.
        small_terminal: The small terminal's offer.
        mounted_terminal: The mounted terminal's offer.
        minimal_packet_iot: Minimal-packet IoT's offer.
        data_iot: Data IoT's offer.
    """

    year: int
    small_terminal: TerminalOffer
    mounted_terminal: TerminalOffer
    minimal_packet_iot: IotOffer
    data_iot: IotOffer

    @property
    def classes(self) -> tuple[TerminalOffer | IotOffer, ...]:
        """The four offers in :class:`ProductClass` order (small, mounted, minimal, data)."""
        return (self.small_terminal, self.mounted_terminal, self.minimal_packet_iot, self.data_iot)


@dataclass(frozen=True)
class ChoiceOffers:
    """One choice and its offers in every reported year, in order.

    Attributes:
        choice: The choice.
        years: Its offers, one entry per reported year.
    """

    choice: Choice
    years: tuple[YearOffers, ...]


def price_on_line(start: float, end: float, year: int, first: int, last: int) -> float:
    """p(t) = p_start + (p_end - p_start) x (t - t0) / (t1 - t0), dollars a month.

    Args:
        start: p_start, the start price in the first reported year.
        end: p_end, the choice's end price in the last reported year.
        year: t, a reported fiscal year.
        first: t0, the first reported year.
        last: t1, the last reported year.

    Returns:
        The price a month in year t (the start price at t0, the end price at t1).
    """
    return start + (end - start) * (year - first) / (last - first)


def _decimal_value(value: float) -> Fraction:
    """A scenario number at its decimal value: its shortest ``repr``, as an exact fraction."""
    return Fraction(repr(value))


def usage_factor(scale: float, year: int, first: int, last: int) -> Fraction:
    """f(t) = 1 + (scale - 1) x (t - t0) / (t1 - t0), a usage path's multiplier in year t, exactly.

    The scale is taken at its decimal value (1.15 is 23/20, not the double nearest it) and the
    line runs in fiscal years, so the factor is the exact rational the formula gives.

    Args:
        scale: The choice's usage scale by the last reported year.
        year: t, a reported fiscal year.
        first: t0, the first reported year.
        last: t1, the last reported year.

    Returns:
        1 in the first reported year, the scale in the last, on a straight line in fiscal years.
    """
    start = _decimal_value(USAGE_SCALE_START)
    return start + (_decimal_value(scale) - start) * Fraction(year - first, last - first)


def scaled_usage(path_value: int, factor: Fraction) -> int:
    """A usage path's value times its line factor, in whole messages or bursts, rounded half up.

    ``round_half_up(path_value x factor)`` with the product exact: it is the nearest double to
    the exact product that :func:`common.cadence.round_half_up` rounds, and an exact half is a
    double, so it rounds up as the formula says (50 messages at x1.15 in the last year: 57.5, so
    58, where the product of doubles, 57.49999999999999, would give 57). x8's FY2033
    minimal-packet usage, 72 x 3.8 = 273.6, is 274 (round 3's ``scaled``). A product that is not
    a half lies at least 1 / (2 x 10^d x (t1 - t0)) from one, for a scale with d decimal places,
    so the double rounds it as the exact formula does while 10^d x (t1 - t0) x the product stays
    far below 10^15 (the double's precision); the shipped grid's scales are whole.

    Args:
        path_value: The scenario's messages or bursts a day in the year.
        factor: f(t), from :func:`usage_factor`.

    Returns:
        The messages or bursts a day a device sends in the year at the choice.

    Raises:
        OverflowError: If the product is beyond the range of a double (the offers refuse it,
            naming the field).
    """
    return round_half_up(float(path_value * factor))


def choice_grid(config: ProductCaseConfig) -> tuple[Choice, ...]:
    """The choice grid, in its fixed order, each choice's id its index.

    The order: the small terminal's end prices, then the mounted terminal's, minimal-packet IoT's,
    minimal-packet IoT's usage scales, then data IoT's (the last varying fastest). Data IoT's end
    price is :data:`~product_case.constants.DATA_IOT_PRICE_MULTIPLE` times minimal-packet IoT's.

    Args:
        config: The scenario.

    Returns:
        Every choice; the shipped scenario gives 5 x 3 x 1 x 5 x 4 = 300, 20 of them candidates.
    """
    prices = config.prices
    usage = config.usage
    grid: list[Choice] = []
    combinations = product(
        prices.small_terminal.end_usd_month,
        prices.mounted_terminal.end_usd_month,
        prices.minimal_packet_iot.end_usd_month,
        usage.minimal_packet_iot.scales,
        usage.data_iot.scales,
    )
    for index, (small, mounted, minimal, minimal_scale, data_scale) in enumerate(combinations):
        grid.append(
            Choice(
                choice_id=index,
                end_prices=EndPrices(
                    small_terminal=small,
                    mounted_terminal=mounted,
                    minimal_packet_iot=minimal,
                    data_iot=DATA_IOT_PRICE_MULTIPLE * minimal,
                ),
                minimal_packet_scale=minimal_scale,
                data_iot_scale=data_scale,
                at_start_prices=(
                    small == prices.small_terminal.start_usd_month
                    and mounted == prices.mounted_terminal.start_usd_month
                    and minimal == prices.minimal_packet_iot.start_usd_month
                ),
            )
        )
    logger.debug(
        "the choice grid: %d choices, %d candidates",
        len(grid),
        sum(choice.at_start_prices for choice in grid),
    )
    return tuple(grid)


def _finite(value: float, quantity: str, field: str, year: int) -> float:
    """``value`` when it is finite; else an :class:`OfferError` naming its field and the year."""
    if not math.isfinite(value):
        raise OfferError(
            f"{field}: FY{year}'s {quantity} is {value!r}, not a finite number (a setting too "
            "large for the arithmetic)"
        )
    return value


def _usage_on_line(
    path_value: int, scale: float, years: tuple[int, ...], index: int, field: str
) -> int:
    """The usage a choice sends a day in the reported year at ``index`` (:func:`scaled_usage`).

    A product beyond the range of a double is refused, naming the field and the year.
    """
    year = years[index]
    try:
        return scaled_usage(path_value, usage_factor(scale, year, years[0], years[-1]))
    except OverflowError as error:
        raise OfferError(
            f"{field}: FY{year}'s usage at the scale x{scale!r} is beyond the range of a double "
            "(a setting too large for the arithmetic)"
        ) from error


def _terminal_offer(
    product_class: ProductClass,
    prices: ClassPriceDials,
    end_price: float,
    gb_per_month: tuple[float, ...],
    busy_hour_gb: float,
    years: tuple[int, ...],
    index: int,
) -> TerminalOffer:
    """A terminal's offer in the reported year at ``index``.

    The off-peak part is the monthly total less the busy-hour part. A total below the busy-hour
    part by more than :data:`~product_case.constants.RELATIVE_TOLERANCE` of it is refused, naming
    the field and the year; a smaller shortfall is the float rounding of the busy-hour part (a
    product of the engineering usage's doubles, 0.37800000000000006 GB for 0.1 Mbps at 7
    percent), so a total equal to it in decimals has an off-peak part of 0. A price, a service
    or a rate that is not finite is refused, naming its field and the year.
    """
    year, first, last = years[index], years[0], years[-1]
    usage_field = f"usage.{product_class}.gb_per_month"
    total = gb_per_month[index]
    offpeak = total - busy_hour_gb
    if offpeak < 0:
        if -offpeak > RELATIVE_TOLERANCE * busy_hour_gb:
            raise OfferError(
                f"{usage_field}: FY{year}'s {total!r} GB a month is below its busy-hour part, "
                f"{busy_hour_gb!r} GB (the engineering usage over the {BUSY_HOURS_PER_DAY} busy "
                "hours, which the seats are sized for)"
            )
        offpeak = 0.0
    price = price_on_line(prices.start_usd_month, end_price, year, first, last)
    busy_rate = (
        busy_hour_gb
        * BYTES_PER_GB
        * BITS_PER_BYTE
        / (BUSY_HOURS_PER_DAY * SECONDS_PER_HOUR * DAYS_PER_MONTH)
    )
    offpeak_rate = (
        offpeak
        * BYTES_PER_GB
        * BITS_PER_BYTE
        / (OFFPEAK_HOURS_PER_DAY * SECONDS_PER_HOUR * DAYS_PER_MONTH)
    )
    return TerminalOffer(
        product_class=product_class,
        price_usd_month=_finite(price, "price a month", f"prices.{product_class}", year),
        gb_per_month=total,
        busy_hour_gb_per_month=busy_hour_gb,
        offpeak_gb_per_month=offpeak,
        service=_finite(total / gb_per_month[0], "service", usage_field, year),
        busy_hour_rate_bps=_finite(
            busy_rate,
            "busy-hour rate",
            f"the engineering usage of {TERMINAL_DEVICE_CLASS[product_class]}",
            year,
        ),
        offpeak_rate_bps=_finite(offpeak_rate, "off-peak rate", usage_field, year),
    )


def _iot_offer(
    product_class: ProductClass,
    price_usd_month: float,
    messages_per_day: int,
    bursts_per_day: int,
    bursts_outside_busy_hours: bool,
    first_bytes_per_day: int,
    engineering: EngineeringView,
    year: int,
) -> IotOffer:
    """An IoT class's offer in a reported year: its usage, bytes, service and per-device loads.

    Uplink bits a second: messages x 340 x 8 / 86,400, plus the bursts' bits over the day, or,
    outside the busy hours, none in the busy hours and their bits over the 20 off-peak hours;
    attempts a second the same way, one per message or burst; tone messages a second, the
    messages over the day (round 1's order). A usage whose loads or service are beyond the range
    of a double, or a price that is not finite, is refused, naming the field and the year.
    """
    usage_field = f"usage.{product_class}"
    try:
        message_bits = (
            messages_per_day * engineering.message_bytes * BITS_PER_BYTE / SECONDS_PER_DAY
        )
        burst_bits = bursts_per_day * engineering.burst_bytes * BITS_PER_BYTE
        message_attempts = messages_per_day / SECONDS_PER_DAY
        offpeak_seconds = OFFPEAK_HOURS_PER_DAY * SECONDS_PER_HOUR
        if bursts_outside_busy_hours:
            bits_busy = message_bits
            bits_offpeak = message_bits + burst_bits / offpeak_seconds
            attempts_busy = message_attempts
            attempts_offpeak = message_attempts + bursts_per_day / offpeak_seconds
        else:
            bits_busy = bits_offpeak = message_bits + burst_bits / SECONDS_PER_DAY
            attempts_busy = attempts_offpeak = message_attempts + bursts_per_day / SECONDS_PER_DAY
        bytes_per_day = (
            messages_per_day * engineering.message_bytes + bursts_per_day * engineering.burst_bytes
        )
        service = bytes_per_day / first_bytes_per_day
    except OverflowError as error:
        raise OfferError(
            f"{usage_field}: FY{year}'s messages and bursts a day are beyond the range of a "
            "double in its loads (a setting too large for the arithmetic)"
        ) from error
    loads = (bits_busy, bits_offpeak, attempts_busy, attempts_offpeak, message_attempts, service)
    for value in loads:
        _finite(value, "per-device loads", usage_field, year)
    return IotOffer(
        product_class=product_class,
        price_usd_month=_finite(
            price_usd_month,
            "price a month"
            if product_class is ProductClass.MINIMAL_PACKET_IOT
            else "data IoT price a month (twice minimal-packet IoT's)",
            "prices.minimal_packet_iot",
            year,
        ),
        messages_per_day=messages_per_day,
        bursts_per_day=bursts_per_day,
        bursts_outside_busy_hours=bursts_outside_busy_hours,
        bytes_per_day=bytes_per_day,
        service=service,
        uplink_bits_per_second_busy=bits_busy,
        uplink_bits_per_second_offpeak=bits_offpeak,
        access_attempts_per_second_busy=attempts_busy,
        access_attempts_per_second_offpeak=attempts_offpeak,
        single_tone_messages_per_second=message_attempts,
    )


def choice_offers(
    config: ProductCaseConfig, engineering: EngineeringView, choice: Choice
) -> ChoiceOffers:
    """One choice's offers in every reported year, the four classes side by side (method step 2).

    Args:
        config: The scenario.
        engineering: The engineering view of the scenario's reported years.
        choice: A choice of :func:`choice_grid`.

    Returns:
        The choice's offers, one entry per reported year.

    Raises:
        OfferError: If the view's years are not the scenario's reported years; a terminal's
            monthly total in a reported year is below its busy-hour part by more than the
            invariants' tolerance; or a usage, a price or a rate is not finite (each naming the
            field and the year).
    """
    years = config.reported_years
    viewed = tuple(year.year for year in engineering.years)
    if viewed != years:
        raise OfferError(
            f"the engineering view holds the years {list(viewed)}; the scenario reports "
            f"{list(years)} (reported_years)"
        )
    prices = config.prices
    usage = config.usage
    first, last = years[0], years[-1]
    minimal_messages = usage.minimal_packet_iot.messages_per_day
    data_bursts = usage.data_iot.bursts_per_day
    data_messages = usage.data_iot.messages_per_day
    minimal_field = "usage.minimal_packet_iot"
    data_field = "usage.data_iot"
    minimal_first = _usage_on_line(
        minimal_messages[0], choice.minimal_packet_scale, years, 0, minimal_field
    )
    data_first = _usage_on_line(data_bursts[0], choice.data_iot_scale, years, 0, data_field)
    minimal_first_bytes = minimal_first * engineering.message_bytes
    data_first_bytes = (
        data_messages * engineering.message_bytes + data_first * engineering.burst_bytes
    )
    offers: list[YearOffers] = []
    for index, year in enumerate(years):
        minimal_price = price_on_line(
            prices.minimal_packet_iot.start_usd_month,
            choice.end_prices[ProductClass.MINIMAL_PACKET_IOT],
            year,
            first,
            last,
        )
        offers.append(
            YearOffers(
                year=year,
                small_terminal=_terminal_offer(
                    ProductClass.SMALL_TERMINAL,
                    prices.small_terminal,
                    choice.end_prices[ProductClass.SMALL_TERMINAL],
                    usage.small_terminal.gb_per_month,
                    engineering.busy_hour_gb_per_month_small,
                    years,
                    index,
                ),
                mounted_terminal=_terminal_offer(
                    ProductClass.MOUNTED_TERMINAL,
                    prices.mounted_terminal,
                    choice.end_prices[ProductClass.MOUNTED_TERMINAL],
                    usage.mounted_terminal.gb_per_month,
                    engineering.busy_hour_gb_per_month_mounted,
                    years,
                    index,
                ),
                minimal_packet_iot=_iot_offer(
                    ProductClass.MINIMAL_PACKET_IOT,
                    minimal_price,
                    _usage_on_line(
                        minimal_messages[index],
                        choice.minimal_packet_scale,
                        years,
                        index,
                        minimal_field,
                    ),
                    0,
                    False,
                    minimal_first_bytes,
                    engineering,
                    year,
                ),
                data_iot=_iot_offer(
                    ProductClass.DATA_IOT,
                    DATA_IOT_PRICE_MULTIPLE * minimal_price,
                    data_messages,
                    _usage_on_line(
                        data_bursts[index], choice.data_iot_scale, years, index, data_field
                    ),
                    usage.data_iot.bursts_outside_busy_hours[index],
                    data_first_bytes,
                    engineering,
                    year,
                ),
            )
        )
    return ChoiceOffers(choice=choice, years=tuple(offers))


def grid_offers(
    config: ProductCaseConfig, engineering: EngineeringView
) -> tuple[ChoiceOffers, ...]:
    """Every choice of the grid with its offers, in the grid's order.

    Args:
        config: The scenario.
        engineering: The engineering view of the scenario's reported years.

    Returns:
        One :class:`ChoiceOffers` per choice of :func:`choice_grid`.

    Raises:
        OfferError: As :func:`choice_offers`.
    """
    return tuple(choice_offers(config, engineering, choice) for choice in choice_grid(config))


__all__ = [
    "Choice",
    "ChoiceOffers",
    "EndPrices",
    "IotOffer",
    "OfferError",
    "TerminalOffer",
    "YearOffers",
    "choice_grid",
    "choice_offers",
    "grid_offers",
    "price_on_line",
    "scaled_usage",
    "usage_factor",
]
