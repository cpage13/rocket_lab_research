"""The product case's Monte Carlo (``product_case.monte_carlo``, B3): the markets and the method.

Each test names what it exercises, its sample and what counts as success. Round 3's values come
from round 3 of the product case's scratch exploration (local), at full precision as the plan's
probe of round 3's inputs printed them (local).
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from product_case.config import load_product_case_config
from product_case.monte_carlo import Market, central_market, draw_markets

ROUND3_FIRST_DRAW = Market(
    gamma=0.747400500183258, epsilon=1.174028063465549, eta=0.45858404147883625
)
"""Round 3's first market at seed 20261006, its ranges round 2's."""

ROUND3_DRAW_1134 = Market(gamma=0.66408629754288, epsilon=1.355751487391255, eta=0.493833971708313)
"""Round 3's draw 1134, the typical draw of its $4 and $8 pick."""


def test_the_draws_are_round_3s_stream(product_case_yaml: Path) -> None:
    """Objective: the markets are round 3's stream (D9): ``random.Random(seed)`` and, per draw,
    gamma, epsilon then eta, each ``uniform(low, high)``.

    Sample: the shipped scenario (seed 20261006, 2,000 draws, gamma 0.5 to 1.0, epsilon 0.5 to
    1.5, eta 0 to 0.5, round 3's settings).

    Expected outcome: 2,000 markets; the first and draw 1134 equal round 3's to the bit.
    """
    markets = draw_markets(load_product_case_config(product_case_yaml))
    assert len(markets) == 2_000
    assert markets[0] == ROUND3_FIRST_DRAW
    assert markets[1134] == ROUND3_DRAW_1134


def test_the_central_market_is_each_range_middle(
    product_case_yaml: Path,
    shipped_scenario: dict[str, Any],
    write_scenario: Callable[[dict[str, Any]], Path],
) -> None:
    """Objective: the central market holds each response at the middle of its range (D7), and
    moves with neither the seed nor the draw count.

    Sample: the shipped scenario; a side scenario with gamma 0.3 to 0.8 and epsilon 0.5 to 1.0,
    another seed and 50 draws.

    Expected outcome: (0.75, 1.0, 0.25) for the shipped ranges; (0.55, 0.75, 0.25) for the side
    ranges, whatever the seed and the draws.
    """
    assert central_market(load_product_case_config(product_case_yaml)) == Market(0.75, 1.0, 0.25)
    shipped_scenario["market"].update(
        {
            "seed": 7,
            "draws": 50,
            "gamma": {"low": 0.3, "high": 0.8},
            "epsilon": {"low": 0.5, "high": 1.0},
        }
    )
    side = load_product_case_config(write_scenario(shipped_scenario))
    assert central_market(side) == Market((0.3 + 0.8) / 2, (0.5 + 1.0) / 2, 0.25)
    assert len(draw_markets(side)) == 50
