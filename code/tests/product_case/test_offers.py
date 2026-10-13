"""B2, the offers: the choice grid in its fixed order, and each choice's prices, usage, service
and per-device loads in each reported year, before any market.
"""

from __future__ import annotations

import copy
import dataclasses
import math
import pickle
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from product_case.config import ProductCaseConfig, load_product_case_config
from product_case.constants import ProductClass
from product_case.engineering import (
    EngineeringView,
    EngineeringYearReading,
    TerminalPool,
    build_engineering_view,
)
from product_case.offers import (
    Choice,
    EndPrices,
    OfferError,
    choice_grid,
    choice_offers,
    grid_offers,
    price_on_line,
    scaled_usage,
    usage_factor,
)

SHIPPED_YEARS = (2031, 2033, 2035, 2036)
"""The shipped scenario's reported years."""

ADOPTED_CHOICE = 12
"""The adopted case's choice id on the shipped grid (the plan's probe pB1): the investor's
prices held flat, minimal-packet IoT at x8 and data IoT at x1."""


def _view(years: tuple[int, ...]) -> EngineeringView:
    """An engineering view of round numbers for the given years (the offers read only its usage,
    sizes and years): the synthetic artifact's pools, 340-byte messages and 100 KB bursts."""
    readings = [
        EngineeringYearReading(
            year=year,
            living_fleet=500 * (index + 1),
            annual_cost_musd=200.0 * (index + 1),
            people_small_terminal=4_000_000.0 * (index + 1),
            people_mounted_terminal=500_000.0 * (index + 1),
            phone_useful_beams=20_000.0 * (index + 1),
            iot_payload_bits_per_second=7.0e9 * (index + 1),
            iot_access_attempts_per_second=1_140_000.0 * (index + 1),
            iot_single_tone_seconds_per_second=1.4e7 * (index + 1),
        )
        for index, year in enumerate(years)
    ]
    return build_engineering_view(
        path="synthetic/iridium.json",
        sha256="0" * 64,
        schema_version="iridium-v7",
        version_stamp="2030-01-01",
        coverage_floor_reached_year=years[0],
        small_terminal_pool=TerminalPool(10.0, 2.0, 0.025),
        mounted_terminal_pool=TerminalPool(12.5, 5.0, 0.1),
        message_bytes=340,
        burst_bytes=100_000,
        airtime_high_s=7.0,
        readings=readings,
    )


def test_the_shipped_grid_holds_300_choices_and_20_candidates() -> None:
    """Objective: the shipped grid expands in its fixed order (the small terminal's end prices,
    the mounted terminal's, minimal-packet IoT's, then minimal-packet IoT's usage scales, then
    data IoT's, the last varying fastest), each choice's id its index, a candidate exactly when
    every end price is its start price, data IoT's end price twice minimal-packet IoT's.

    Sample: the default scenario's grid (5 small, 3 mounted and 1 minimal-packet end prices; 5
    and 4 usage scales).

    Expected outcome: 300 choices with ids 0 to 299; 20 candidates, choices 0 to 19, all at $10,
    $50, $3 and $6; choice 1 the first data IoT step, choice 4 the first minimal-packet step,
    choice 20 the first mounted terminal step ($45), choice 60 the first small terminal step
    ($9); choice 12 the investor's prices at minimal-packet x8 and data IoT x1.
    """
    grid = choice_grid(ProductCaseConfig())
    assert len(grid) == 300
    assert [choice.choice_id for choice in grid] == list(range(300))
    candidates = [choice.choice_id for choice in grid if choice.at_start_prices]
    assert candidates == list(range(20))
    flat = {
        ProductClass.SMALL_TERMINAL: 10.0,
        ProductClass.MOUNTED_TERMINAL: 50.0,
        ProductClass.MINIMAL_PACKET_IOT: 3.0,
        ProductClass.DATA_IOT: 6.0,
    }
    for choice in grid[:20]:
        assert dict(choice.end_prices) == flat
        assert list(choice.end_prices) == list(ProductClass)
    assert (grid[1].minimal_packet_scale, grid[1].data_iot_scale) == (1.0, 2.0)
    assert (grid[4].minimal_packet_scale, grid[4].data_iot_scale) == (2.0, 1.0)
    assert grid[20].end_prices[ProductClass.MOUNTED_TERMINAL] == 45.0
    assert not grid[20].at_start_prices
    assert grid[60].end_prices[ProductClass.SMALL_TERMINAL] == 9.0
    adopted = grid[ADOPTED_CHOICE]
    assert adopted.at_start_prices
    assert (adopted.minimal_packet_scale, adopted.data_iot_scale) == (8.0, 1.0)


def test_a_choice_and_its_offers_are_values(product_case_yaml: Path) -> None:
    """Objective: a choice and its offers are values that every later box can key, copy and
    serialize: each hashes, deep-copies, pickles and passes ``dataclasses.asdict``, and a choice
    built from a plain mapping of end prices holds them as the immutable ``EndPrices``.

    Sample: the shipped grid's choice 12 (the investor's prices, minimal-packet x8, data IoT x1)
    and its offers on an engineering view of round numbers; the same choice built from a dict.

    Expected outcome: equal copies hash equal and fall in one set; a deep copy and a pickle
    round trip equal the original; ``asdict`` writes the end prices by class name ($10, $50, $3,
    $6) for the choice and inside its offers; the dict-built choice equals the grid's, holds
    ``EndPrices`` and reads as a mapping in class order.
    """
    config = load_product_case_config(product_case_yaml)
    choice = choice_grid(config)[ADOPTED_CHOICE]
    offers = choice_offers(config, _view(SHIPPED_YEARS), choice)
    prices = {"small_terminal": 10.0, "mounted_terminal": 50.0, "minimal_packet_iot": 3.0}
    prices["data_iot"] = 6.0
    for value in (choice, offers):
        assert hash(value) == hash(copy.deepcopy(value))
        assert copy.deepcopy(value) == value
        assert pickle.loads(pickle.dumps(value)) == value  # noqa: S301 (the bytes this test pickled)
        assert len({value, copy.deepcopy(value)}) == 1
    assert dataclasses.asdict(choice) == {
        "choice_id": ADOPTED_CHOICE,
        "end_prices": prices,
        "minimal_packet_scale": 8.0,
        "data_iot_scale": 1.0,
        "at_start_prices": True,
    }
    assert dataclasses.asdict(offers)["choice"]["end_prices"] == prices
    rebuilt = Choice(
        choice_id=ADOPTED_CHOICE,
        end_prices={ProductClass(name): price for name, price in prices.items()},
        minimal_packet_scale=8.0,
        data_iot_scale=1.0,
        at_start_prices=True,
    )
    assert isinstance(rebuilt.end_prices, EndPrices)
    assert rebuilt == choice
    assert hash(rebuilt) == hash(choice)
    assert list(rebuilt.end_prices.items()) == [(ProductClass(n), p) for n, p in prices.items()]


def test_the_adopted_choice_paths_are_pb1s(product_case_yaml: Path) -> None:
    """Objective: the adopted case's usage paths, the line factor in fiscal years rounded half
    up: minimal-packet IoT at x8 sends 48, 274, 634 and 768 messages a day and data IoT at x1 8,
    10, 12 and 13 bursts (the plan's probe pB1), its 48 messages in every year and its bursts
    outside the busy hours from FY2033; the prices flat at $10, $50, $3 and $6.

    Sample: the shipped scenario, choice 12, on an engineering view of round numbers for the
    four reported years.

    Expected outcome: the paths, the flags and the flat prices as stated.
    """
    config = load_product_case_config(product_case_yaml)
    offers = choice_offers(config, _view(SHIPPED_YEARS), choice_grid(config)[ADOPTED_CHOICE])
    assert [year.year for year in offers.years] == list(SHIPPED_YEARS)
    assert [year.minimal_packet_iot.messages_per_day for year in offers.years] == [
        48,
        274,
        634,
        768,
    ]
    assert [year.minimal_packet_iot.bursts_per_day for year in offers.years] == [0, 0, 0, 0]
    assert [year.data_iot.bursts_per_day for year in offers.years] == [8, 10, 12, 13]
    assert [year.data_iot.messages_per_day for year in offers.years] == [48, 48, 48, 48]
    assert [year.data_iot.bursts_outside_busy_hours for year in offers.years] == [
        False,
        True,
        True,
        True,
    ]
    for year in offers.years:
        assert [offer.price_usd_month for offer in year.classes] == [10.0, 50.0, 3.0, 6.0]
        assert [offer.product_class for offer in year.classes] == list(ProductClass)


def test_the_usage_line_runs_in_fiscal_years() -> None:
    """Objective: the usage line's factor runs on fiscal years, not on the reported years'
    index (montecarlo m3): x8 in FY2033 of FY2031 to FY2036 is 1 + 7 x 2 / 5 = 3.8, so 72
    messages become 273.6, rounded half up to 274, never the 240 an index of 1 of 3 would give;
    an exact half rounds up.

    Sample: the factor at x8 in FY2033 over FY2031 to FY2036; 72 and 96 messages scaled; 2.5.

    Expected outcome: 3.8 within a float's rounding; 274 and 634 (FY2035's 96 x 6.6); 3.
    """
    factor = usage_factor(8.0, 2033, 2031, 2036)
    assert math.isclose(factor, 3.8, rel_tol=1e-15)
    assert scaled_usage(72, factor) == 274
    assert scaled_usage(72, factor) != 240
    assert scaled_usage(96, usage_factor(8.0, 2035, 2031, 2036)) == 634
    assert usage_factor(8.0, 2031, 2031, 2036) == 1.0
    assert usage_factor(8.0, 2036, 2031, 2036) == 8.0
    assert scaled_usage(5, 0.5) == 3


def test_the_price_line_runs_from_the_start_to_the_end_price() -> None:
    """Objective: a price runs on a straight line in fiscal years from its start price in the
    first reported year to the choice's end price in the last, and data IoT pays twice
    minimal-packet IoT's in every year and choice.

    Sample: the small terminal from $10 to $6 over FY2031 to FY2036; a side scenario whose
    minimal-packet IoT end prices are $3 and $2, its choice at $2.

    Expected outcome: $10, $8.40, $6.80 and $6 (within a float's rounding); data IoT's price twice
    minimal-packet IoT's in each reported year of the $2 choice, $6 falling to $4.
    """
    expected = [10.0, 8.4, 6.8, 6.0]
    assert [price_on_line(10.0, 6.0, year, 2031, 2036) for year in SHIPPED_YEARS] == pytest.approx(
        expected, rel=1e-15
    )
    config = ProductCaseConfig.model_validate(
        {"prices": {"minimal_packet_iot": {"start_usd_month": 3.0, "end_usd_month": [3.0, 2.0]}}}
    )
    lower = next(
        choice
        for choice in choice_grid(config)
        if choice.end_prices[ProductClass.MINIMAL_PACKET_IOT] == 2.0
    )
    assert lower.end_prices[ProductClass.DATA_IOT] == 4.0
    assert not lower.at_start_prices
    offers = choice_offers(config, _view(SHIPPED_YEARS), lower)
    for year in offers.years:
        assert year.data_iot.price_usd_month == 2 * year.minimal_packet_iot.price_usd_month
    assert offers.years[0].data_iot.price_usd_month == 6.0
    assert offers.years[-1].data_iot.price_usd_month == 4.0


def test_a_terminal_keeps_its_busy_hour_data_and_sends_the_rest_off_peak(
    product_case_yaml: Path,
) -> None:
    """Objective: each terminal's busy-hour data is the engineering usage's in every year (so its
    load and seats are the engineering case's) and its off-peak data the scenario's monthly total
    less it; its rates are those data over 4 h x 30 days and 20 h x 30 days ("A terminal's
    downlink use"); its service is its monthly total over the first reported year's.

    Sample: the shipped scenario's choice 12; the small terminal at 5.4 GB in FY2031 and 9.0 in
    FY2036, the mounted terminal at 54 and 90 GB.

    Expected outcome: busy 2.7 and 27 GB in every year; off-peak 2.7 and 27 in FY2031, 6.3 and
    63 in FY2036; r_busy 50,000 and 500,000 bits a second; in FY2036 the off-peak rate is
    (6.3 / 20) / (2.7 / 4) of the busy-hour rate, the 46.7 percent off-peak downlink use at every
    seat sold (pB1); the services 1 in FY2031 and 9 / 5.4 and 90 / 54 in FY2036.
    """
    config = load_product_case_config(product_case_yaml)
    offers = choice_offers(config, _view(SHIPPED_YEARS), choice_grid(config)[ADOPTED_CHOICE])
    first, last = offers.years[0], offers.years[-1]
    for year in offers.years:
        assert year.small_terminal.busy_hour_gb_per_month == 2.7
        assert year.mounted_terminal.busy_hour_gb_per_month == 27.0
        assert year.small_terminal.busy_hour_rate_bps == 50_000.0
        assert year.mounted_terminal.busy_hour_rate_bps == 500_000.0
    assert (
        first.small_terminal.offpeak_gb_per_month,
        last.small_terminal.offpeak_gb_per_month,
    ) == (
        2.7,
        6.3,
    )
    assert (
        first.mounted_terminal.offpeak_gb_per_month,
        last.mounted_terminal.offpeak_gb_per_month,
    ) == (27.0, 63.0)
    for terminal in (last.small_terminal, last.mounted_terminal):
        use = terminal.offpeak_rate_bps / terminal.busy_hour_rate_bps
        assert math.isclose(use, (6.3 / 20) / (2.7 / 4), rel_tol=1e-12)
        assert round(100 * use, 1) == 46.7
    assert (first.small_terminal.service, first.mounted_terminal.service) == (1.0, 1.0)
    assert last.small_terminal.service == 9.0 / 5.4
    assert last.mounted_terminal.service == 90.0 / 54.0


def test_an_iot_device_loads_its_room_by_period(product_case_yaml: Path) -> None:
    """Objective: an IoT device's per-device loads: its messages spread over the day; its bursts
    over the day, or over the 20 off-peak hours when they go outside the busy hours (none in the
    busy hours then); one random-access attempt per message or burst; its messages a second its
    single-tone load; its bytes a day and its service against the first reported year's.

    Sample: the shipped scenario's choice 12: data IoT in FY2031 (48 messages, 8 bursts at any
    hour) and FY2033 (10 bursts outside the busy hours); minimal-packet IoT in FY2036 (768
    messages).

    Expected outcome: data IoT FY2031 sends (48 x 340 + 8 x 100,000) bytes a day, 816,320, at
    130,560 / 86,400 + 6,400,000 / 86,400 bits a second in both periods (round 1's order);
    FY2033's busy-hour load is its messages' alone and its off-peak load adds 10 x 800,000 /
    72,000 bits a second; attempts likewise; its FY2036 bytes 1,316,320 and service 1,316,320 /
    816,320. Minimal-packet IoT FY2036 sends 261,120 bytes a day, 768 x 2,720 / 86,400 bits and
    768 / 86,400 attempts and tone messages a second in both periods.
    """
    config = load_product_case_config(product_case_yaml)
    offers = choice_offers(config, _view(SHIPPED_YEARS), choice_grid(config)[ADOPTED_CHOICE])
    data_2031 = offers.years[0].data_iot
    assert data_2031.bytes_per_day == 816_320
    assert data_2031.uplink_bits_per_second_busy == 130_560 / 86_400 + 6_400_000 / 86_400
    assert data_2031.uplink_bits_per_second_offpeak == data_2031.uplink_bits_per_second_busy
    assert data_2031.access_attempts_per_second_busy == 48 / 86_400 + 8 / 86_400
    assert data_2031.service == 1.0
    data_2033 = offers.years[1].data_iot
    messages = 130_560 / 86_400
    assert data_2033.uplink_bits_per_second_busy == messages
    assert data_2033.uplink_bits_per_second_offpeak == messages + 8_000_000 / 72_000
    assert data_2033.access_attempts_per_second_busy == 48 / 86_400
    assert data_2033.access_attempts_per_second_offpeak == 48 / 86_400 + 10 / 72_000
    assert data_2033.single_tone_messages_per_second == 48 / 86_400
    data_2036 = offers.years[-1].data_iot
    assert data_2036.bytes_per_day == 1_316_320
    assert data_2036.service == 1_316_320 / 816_320
    minimal_2036 = offers.years[-1].minimal_packet_iot
    assert minimal_2036.bytes_per_day == 261_120
    assert minimal_2036.uplink_bits_per_second_busy == 768 * 2_720 / 86_400
    assert minimal_2036.uplink_bits_per_second_offpeak == 768 * 2_720 / 86_400
    assert minimal_2036.access_attempts_per_second_offpeak == 768 / 86_400
    assert minimal_2036.single_tone_messages_per_second == 768 / 86_400
    assert minimal_2036.service == 768 / 48


def test_a_monthly_total_below_the_busy_hour_part_is_refused_naming_the_field(
    shipped_scenario: dict[str, Any],
    write_scenario: Callable[[dict[str, Any]], Path],
) -> None:
    """Objective: a terminal's monthly total below its busy-hour part (the engineering usage the
    seats are sized for) is refused when the offers are built, naming the field and the year.

    Sample: the shipped scenario with the small terminal at 2.0 GB a month in FY2031 (its
    busy-hour part is 2.7 GB).

    Expected outcome: an ``OfferError`` naming ``usage.small_terminal.gb_per_month``, FY2031,
    2.0 and 2.7.
    """
    shipped_scenario["usage"]["small_terminal"]["gb_per_month"] = [2.0, 6.7, 8.1, 9.0]
    config = load_product_case_config(write_scenario(shipped_scenario))
    with pytest.raises(OfferError) as caught:
        grid_offers(config, _view(SHIPPED_YEARS))
    message = str(caught.value)
    assert message.startswith("usage.small_terminal.gb_per_month: FY2031's 2.0 GB a month"), message
    assert "busy-hour part, 2.7 GB" in message, message


def test_a_view_of_other_years_is_refused() -> None:
    """Objective: the offers are built only on a view of the scenario's own reported years.

    Sample: the default scenario against a view of FY2031 to FY2033.

    Expected outcome: an ``OfferError`` naming both lists of years.
    """
    config = ProductCaseConfig()
    with pytest.raises(OfferError, match=r"\[2031, 2032, 2033\].*\[2031, 2033, 2035, 2036\]"):
        choice_offers(config, _view((2031, 2032, 2033)), choice_grid(config)[0])


def test_every_choice_has_offers_in_every_reported_year() -> None:
    """Objective: the grid's offers cover every choice in the grid's order and every reported
    year in order, the four classes side by side, never phone-first.

    Sample: the default scenario's 300 choices on an engineering view of round numbers.

    Expected outcome: 300 entries in id order, each with the four reported years and the four
    classes in ``ProductClass`` order.
    """
    every = grid_offers(ProductCaseConfig(), _view(SHIPPED_YEARS))
    assert [offers.choice.choice_id for offers in every] == list(range(300))
    for offers in every:
        assert [year.year for year in offers.years] == list(SHIPPED_YEARS)
        for year in offers.years:
            assert [offer.product_class for offer in year.classes] == list(ProductClass)
