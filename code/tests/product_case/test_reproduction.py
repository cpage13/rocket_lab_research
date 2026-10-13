"""Round 3 of the product case's scratch exploration reproduced on its own fixtures.

Round 3's own engineering inputs (the strategy's 40-band prototype rows, local), pinned as floats
at full precision as the plan's probe of round 3's inputs printed them (local), build the
engineering view directly: each year's seats as round 3 took them, the network's scale in round
2's order (s x P_small + m x P_mounted, m round 1's mounted share), and IoT's rooms in round 3's
and part A's orders. Round 3's two scenarios are the YAML fixtures beside this file (its own
prices and paths, never the shipped scenario's). Checked at round 3's printed precision and its
integer counts exactly; the fronts' sizes hold at seed 20261006 only (they move with the seed).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from product_case.config import ProductCaseConfig, load_product_case_config
from product_case.constants import ProductClass, SpreadField
from product_case.engine import ProductCaseRun, run_product_case
from product_case.engineering import EngineeringView, EngineeringYear, TerminalPool
from product_case.monte_carlo import draw_markets, outcome_in_market

FIXTURES = Path(__file__).resolve().parent / "fixtures"
"""Round 3's scenarios."""

SHARE = 0.757347400150716
"""s, round 1's small-terminal share of the beams (from 320 and 40 people a beam)."""

MOUNTED_SHARE = 0.24265259984928406
"""Round 1's mounted share, need_mounted / (need_small + need_mounted), read by round 2's scale."""

ROUND3_YEARS: tuple[tuple[int, int, float, float, float, float], ...] = (
    (2031, 528, 191.4, 4138028.423146129, 526484.8784141438, 19165.632210997504),
    (2033, 1360, 493.0, 9910620.856074534, 1295112.0159616182, 45630.19485848207),
    (2035, 3072, 1113.6, 19256124.431942146, 2689454.0287930863, 88324.15372106557),
    (2036, 4288, 1554.3999999999999, 24649018.300221622, 3572016.7033080384, 112430.3487853968),
)
"""Round 3's inputs per year: fleet, the fleet's cost ($M), small and mounted whole-fleet people,
the phone class's useful beams (round 3's own inputs, local)."""

SPECTRUM_HZ = 8.0e6
"""W, the held width (round 1's constant)."""

SPECTRAL_EFFICIENCY = 0.65
"""The phone class's spectral efficiency (COMM-429, round 1's)."""

DOWNLINK_SHARE = 0.67
"""d, the downlink's share of the frame (round 1's)."""

MAC_EFFICIENCY = 0.20
"""The MAC efficiency (COMM-659)."""

ACCESS_WINDOW = 57.0
"""Random-access attempts a beam a window, the window's low end, one window a second (COMM-654)."""

TONE_HZ = 3_750.0
"""The NB-IoT tone (COMM-714)."""


def _year(
    year: int, fleet: int, cost: float, small: float, mounted: float, beams: float
) -> EngineeringYear:
    """One pinned year: round 3's seats, round 2's scale, the rooms in their orders."""
    return EngineeringYear(
        year=year,
        living_fleet=fleet,
        annual_cost_musd=cost,
        people_small_terminal=small,
        people_mounted_terminal=mounted,
        seats_small_terminal=SHARE * small,
        seats_mounted_terminal=(1.0 - SHARE) * mounted,
        network_scale=(SHARE * small + MOUNTED_SHARE * mounted) / 418_100,
        phone_useful_beams=beams,
        iot_payload_bits_per_second=beams
        * SPECTRUM_HZ
        * SPECTRAL_EFFICIENCY
        * (1.0 - DOWNLINK_SHARE)
        * MAC_EFFICIENCY,
        iot_access_attempts_per_second=beams * ACCESS_WINDOW * 1.0,
        iot_single_tone_seconds_per_second=beams * SPECTRUM_HZ / TONE_HZ * (1.0 - DOWNLINK_SHARE),
    )


def _view() -> EngineeringView:
    """Round 3's network, built directly from the pinned floats (pools at 320 and 40 a beam)."""
    return EngineeringView(
        path="round 3's own inputs",
        sha256="none: pinned floats",
        schema_version="iridium-v7",
        version_stamp="round 3",
        coverage_floor_reached_year=2031,
        small_terminal_pool=TerminalPool(
            beam_pool_mbps=16.0, active_user_rate_mbps=2.0, concurrency_peak=0.025
        ),
        mounted_terminal_pool=TerminalPool(
            beam_pool_mbps=20.0, active_user_rate_mbps=5.0, concurrency_peak=0.1
        ),
        small_terminal_share=SHARE,
        busy_hour_gb_per_month_small=2.7,
        busy_hour_gb_per_month_mounted=27.0,
        message_bytes=340,
        burst_bytes=100_000,
        airtime_high_s=7.0,
        years=tuple(_year(*row) for row in ROUND3_YEARS),
    )


@pytest.fixture(scope="module")
def four_and_eight() -> tuple[ProductCaseConfig, ProductCaseRun]:
    """Round 3's $4 and $8 grid, run (432 choices over 2,000 draws)."""
    config = load_product_case_config(FIXTURES / "round3_four_and_eight.yaml")
    return config, run_product_case(config, _view())


def _money(value: float | None) -> str:
    """Round 3's printed precision, $M with one decimal."""
    assert value is not None
    return f"{value:,.1f}"


def test_round_3s_four_and_eight_grid_is_reproduced(
    four_and_eight: tuple[ProductCaseConfig, ProductCaseRun],
) -> None:
    """Objective: the Monte Carlo reproduces round 3's $4 and $8 pick on round 3's own inputs.

    Sample: round 3's $4 and $8 grid (432 choices; $15, $100 and $4 at the start; usage x1, x2,
    x4), seed 20261006, 2,000 draws, no upload reserve.

    Expected outcome: the pick holds $15, $100, $4 and $8 flat with minimal-packet x4 and data IoT
    x1, usable in 1,539 of 2,000 draws, median summed revenue $38,857.6M; its FY2036 revenue over
    the usable draws $10,377.4M at the 10th percentile and $27,150.4M at the 90th; the front over
    every choice 16 members.
    """
    _, run = four_and_eight
    assert run.pick is not None and run.spreads is not None
    summary = run.choices[run.pick.choice_id]
    assert summary.choice.end_prices == {
        ProductClass.SMALL_TERMINAL: 15.0,
        ProductClass.MOUNTED_TERMINAL: 100.0,
        ProductClass.MINIMAL_PACKET_IOT: 4.0,
        ProductClass.DATA_IOT: 8.0,
    }
    assert (summary.choice.minimal_packet_scale, summary.choice.data_iot_scale) == (4.0, 1.0)
    assert summary.usable_draws == 1_539
    assert _money(summary.median_summed_revenue_musd) == "38,857.6"
    revenue = next(f for f in run.spreads.years[-1].fields if f.field is SpreadField.REVENUE)
    assert (_money(revenue.usable_draws.p10), _money(revenue.usable_draws.p90)) == (
        "10,377.4",
        "27,150.4",
    )
    assert len(run.fronts.all_prices) == 16


def test_round_3s_draw_1134_counts_through_one_market(
    four_and_eight: tuple[ProductCaseConfig, ProductCaseRun],
) -> None:
    """Objective: one market read through ``outcome_in_market`` gives round 3's own counts (the
    draws' evaluation on arrays of length one).

    Sample: the $4 and $8 pick at draw 1134 (gamma 0.66408629754288, epsilon 1.355751487391255,
    eta 0.493833971708313), FY2036.

    Expected outcome: 18,667,869 small terminals; 866,759 mounted terminals; 176,597,219
    minimal-packet IoT devices; 38,503,763 data IoT devices, uncapped (the demand curve's
    docstring line).
    """
    config, run = four_and_eight
    assert run.pick is not None
    market = draw_markets(config)[1134]
    outcome = outcome_in_market(config, _view(), run.choices[run.pick.choice_id].choice, market)
    counts = [entry.customers for entry in outcome.years[-1].classes]
    assert counts == [18_667_869.0, 866_759.0, 176_597_219.0, 38_503_763.0]


def test_round_3s_three_and_six_grid_is_reproduced() -> None:
    """Objective: the Monte Carlo reproduces round 3's $3 and $6 pick and its central market.

    Sample: round 3's $3 and $6 grid (144 choices), seed 20261006, 2,000 draws.

    Expected outcome: the pick at x4 and x1, usable in 1,539 draws, median $38,311.5M; the front
    over every choice 15 members; at the central market FY2036 18,667,869, 824,692, 155,729,207
    and 51,152,213 customers and devices, $13,639.1M.
    """
    config = load_product_case_config(FIXTURES / "round3_three_and_six.yaml")
    run = run_product_case(config, _view())
    assert run.pick is not None and run.headline is not None
    summary = run.choices[run.pick.choice_id]
    assert (summary.choice.minimal_packet_scale, summary.choice.data_iot_scale) == (4.0, 1.0)
    assert summary.usable_draws == 1_539
    assert _money(summary.median_summed_revenue_musd) == "38,311.5"
    assert len(run.fronts.all_prices) == 15
    last = run.headline.years[-1]
    assert [entry.customers for entry in last.classes] == [
        18_667_869.0,
        824_692.0,
        155_729_207.0,
        51_152_213.0,
    ]
    assert _money(last.totals.revenue_musd) == "13,639.1"
