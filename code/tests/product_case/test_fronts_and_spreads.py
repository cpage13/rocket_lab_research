"""The Monte Carlo's tricky logic: the fronts, the pick, the percentiles and the ranks (B3).

Constructed summaries and values, so each rule is read alone (the design's E9 and D10; the
probes' walk W3 the fallback's model); the percentiles' exact cuts on every range a point, the
margin read in one unit by the usable test and the check, the single-tone test's dominance and a
terminal's off-peak downlink use on the synthetic run. Each test names what it exercises, its
sample and what counts as success.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from common.meta import ValidationSeverity
from product_case.checks import believability_results
from product_case.config import ProductCaseConfig, load_product_case_config
from product_case.constants import (
    PickBasis,
    ProductClass,
    SpreadField,
    SpreadNullReason,
    UsableTest,
)
from product_case.engine import run_product_case
from product_case.engineering import engineering_view_from_bytes
from product_case.monte_carlo import (
    ChoiceSummary,
    Fronts,
    YearOutcome,
    _basis_spread,
    central_market,
    fronts_of,
    outcome_in_market,
    pick_of,
    robust_floor_draws,
)
from product_case.offers import Choice


def _summary(
    choice_id: int, usable: int, median: float | None, *, candidate: bool = True
) -> ChoiceSummary:
    """A choice's summary over 2,000 draws with ``usable`` usable and the given median."""
    price = 10.0 if candidate else 9.0
    return ChoiceSummary(
        choice=Choice(
            choice_id=choice_id,
            end_prices={
                ProductClass.SMALL_TERMINAL: price,
                ProductClass.MOUNTED_TERMINAL: 50.0,
                ProductClass.MINIMAL_PACKET_IOT: 3.0,
                ProductClass.DATA_IOT: 6.0,
            },
            minimal_packet_scale=float(choice_id + 1),
            data_iot_scale=1.0,
            at_start_prices=candidate,
        ),
        usable_draws=usable,
        usable_share=usable / 2_000,
        median_summed_revenue_musd=median,
        median_last_year_revenue_musd=median,
        central_revenue_musd=(1.0,),
        central_summed_revenue_musd=1.0,
        central_usable=True,
        draws_failing=dict.fromkeys(UsableTest, 0),
    )


@pytest.fixture
def config(product_case_yaml: Path) -> ProductCaseConfig:
    """The shipped scenario (its robust floor, 0.75, and its usage scales)."""
    return load_product_case_config(product_case_yaml)


def test_the_front_sweep_breaks_ties_by_the_grids_order() -> None:
    """Objective: a front is round 3's sweep: by usable draws, then median, then the grid's order;
    a member joins on a strictly higher median; a choice with no usable draw is left out; of exact
    duplicates the earliest stands for them.

    Sample: six choices: two exact duplicates (ids 1 and 2), one less usable with a higher median
    (3), one less usable with an equal median (4), one with no usable draw (5), the most usable
    (0).

    Expected outcome: the front (0, 1, 3): id 2 a duplicate of 1, id 4 no higher than 1, id 5
    usable in no draw.
    """
    summaries = [
        _summary(0, 1_900, 100.0),
        _summary(1, 1_800, 200.0),
        _summary(2, 1_800, 200.0),
        _summary(3, 1_700, 300.0),
        _summary(4, 1_600, 200.0),
        _summary(5, 0, None),
    ]
    assert fronts_of(summaries).all_prices == (0, 1, 3)


def test_the_pick_rules(config: ProductCaseConfig) -> None:
    """Objective: the pick: among candidates usable in at least the robust floor's share, the
    highest median, ties to the higher share, then the earlier choice; else the candidates'
    front's first member, which among candidates tied at the top share takes the higher median
    (the probes' walk W3), warned; else no pick; ``dominated_in_context_by`` at a fallback names
    the context front's members that beat it, each on that front.

    Sample: robust candidates tied at a median (1,600 and 1,700 usable); a fallback where seven
    candidates tie at 1,238 usable draws, beside a context choice at a lower price usable in 1,516
    with a higher median; candidates usable in no draw.

    Expected outcome: the more usable of the tied robust pair; the fallback the tied candidate with
    the highest median, on the candidates' front, beaten in context by the lower-priced choice;
    None when no candidate is usable.
    """
    robust = [_summary(0, 1_600, 500.0), _summary(1, 1_700, 500.0), _summary(2, 1_800, 400.0)]
    pick = pick_of(robust, fronts_of(robust), config)
    assert pick is not None and (pick.choice_id, pick.basis) == (1, PickBasis.ROBUST_FLOOR_MET)
    tied = [_summary(index, 1_238, 200.0 + index) for index in range(7)]
    context = _summary(7, 1_516, 300.0, candidate=False)
    fronts = fronts_of([*tied, context])
    fallback = pick_of([*tied, context], fronts, config)
    assert fallback is not None
    assert (fallback.choice_id, fallback.basis) == (6, PickBasis.MOST_USABLE_FALLBACK)
    assert fallback.choice_id in fronts.at_start_prices
    assert fallback.dominated_in_context_by == (7,)
    assert set(fallback.dominated_in_context_by) <= set(fronts.all_prices)
    unusable = [_summary(0, 0, None), _summary(1, 1_900, 100.0, candidate=False)]
    assert pick_of(unusable, fronts_of(unusable), config) is None
    assert fronts_of(unusable) == Fronts(all_prices=(1,), at_start_prices=())


@pytest.mark.parametrize(
    ("draws", "robust", "least"),
    [(2_000, 0.75, 1_500), (50, 0.75, 38), (2_000, 0.745, 1_490), (10, 0.7, 7), (9, 1.0, 9)],
)
def test_the_robust_floors_count_is_the_picks_own_comparison(
    draws: int, robust: float, least: int
) -> None:
    """Objective: the robust floor's count, which the warnings and the stated line print beside a
    pick's usable draws, is the least whole u with u / draws >= the floor, the comparison the
    pick makes on a usable share, at a floor whose product with the draws is not whole (37.5) or
    not exact in floats (0.745 and 0.7).

    Sample: 2,000 draws at 0.75; 50 at 0.75; 2,000 at 0.745; 10 at 0.7; 9 at 1.0.

    Expected outcome: 1,500, 38, 1,490, 7 and 9; the count reaches the floor and one fewer does
    not.
    """
    config = ProductCaseConfig.model_validate(
        {"market": {"draws": draws}, "floors": {"robust": robust}}
    )
    assert robust_floor_draws(config) == least
    assert least / draws >= robust > (least - 1) / draws


@pytest.mark.parametrize(("count", "stands"), [(2, False), (8, False), (9, True)])
def test_the_percentiles_are_null_below_9_values(count: int, stands: bool) -> None:
    """Objective: D10: the 10th and 90th by ``statistics.quantiles`` (exclusive) and the 50th by
    ``statistics.median`` are null below 9 values, with the reason; from 9 they stand inside the
    data.

    Sample: 2, 8 and 9 values evenly spread from 10,000 (the design's probe P7).

    Expected outcome: null with ``too_few_usable_draws`` at 2 and 8; at 9 the 10th 10,000 and the
    90th 90,000; the rank stands in every case.
    """
    values = np.arange(1, count + 1, dtype=np.float64) * 10_000
    spread = _basis_spread(values, 10_000.0)
    assert spread.headline_rank == 0.5 / count
    if stands:
        assert (spread.p10, spread.p50, spread.p90, spread.null_reason) == (
            10_000.0,
            50_000.0,
            90_000.0,
            None,
        )
    else:
        assert (spread.p10, spread.p50, spread.p90) == (None, None, None)
        assert spread.null_reason is SpreadNullReason.TOO_FEW_USABLE_DRAWS


def test_the_cuts_are_exact_so_nine_values_give_the_lowest_and_highest() -> None:
    """Objective: D10's exclusive method computed exactly: at 9 values the 10th percentile is the
    lowest value and the 90th the highest, to the bit, and the three fall in order (the numerics
    lens's M1: the standard library's float arithmetic gives 903.4968 x 10 / 10 =
    903.4968000000001 and 3659.343708 x 10 / 10 = 3659.3437079999994).

    Sample: 9 values that are not round, from 903.4968 to 3659.343708, unsorted.

    Expected outcome: p10 903.4968 and p90 3659.343708 exactly; p50 the fifth value, 1,800.9;
    p10 <= p50 <= p90.
    """
    values = np.array(
        [2236.32984, 903.4968, 1500.3, 3659.343708, 1000.1, 2500.5, 1800.9, 1200.7, 3000.25],
        dtype=np.float64,
    )
    spread = _basis_spread(values, 1800.9)
    assert (spread.p10, spread.p50, spread.p90) == (903.4968, 1800.9, 3659.343708)
    assert spread.p10 is not None and spread.p50 is not None and spread.p90 is not None
    assert spread.p10 <= spread.p50 <= spread.p90


def _headline_value(year: YearOutcome, field: SpreadField) -> float:
    """The headline's value a spread field names: a class's customers or revenue, or a total."""
    owner, _, attribute = field.value.rpartition(".")
    if owner:
        entry = next(entry for entry in year.classes if entry.product_class == owner)
        return float(getattr(entry, attribute))
    return float(getattr(year.totals, attribute))


def test_every_range_a_point_gives_each_spread_its_one_value(
    synthetic_scenario: dict[str, Any],
    write_scenario: Callable[[dict[str, Any]], Path],
    synthetic_engineering: dict[str, Any],
    as_engineering_bytes: Callable[[dict[str, Any]], bytes],
) -> None:
    """Objective: with every market response's range a point, every drawn market is the central
    market, so each spread over either basis is the one value every draw holds: its 10th, 50th
    and 90th equal the headline's value exactly (the exclusive method computed exactly, D10),
    and the headline's mid-rank is a half.

    Sample: the synthetic case with gamma 0.75 to 0.75, epsilon 1 to 1 and eta 0.25 to 0.25 (the
    small scenario's midpoints), 50 draws.

    Expected outcome: the run picks, usable in all 50 draws; in every reported year and spread
    field, both bases' p10, p50 and p90 equal the headline's value, and the rank is 0.5.
    """
    for response, middle in (("gamma", 0.75), ("epsilon", 1.0), ("eta", 0.25)):
        synthetic_scenario["market"][response] = {"low": middle, "high": middle}
    config = load_product_case_config(write_scenario(synthetic_scenario))
    view = engineering_view_from_bytes(
        as_engineering_bytes(synthetic_engineering),
        path="synthetic",
        reported_years=config.reported_years,
    )
    run = run_product_case(config, view)
    assert run.headline is not None and run.spreads is not None
    assert run.spreads.usable_draws == run.spreads.draws == 50
    for headline_year, spread_year in zip(run.headline.years, run.spreads.years, strict=True):
        for spread in spread_year.fields:
            value = _headline_value(headline_year, spread.field)
            for basis in (spread.usable_draws, spread.all_draws):
                assert (basis.p10, basis.p50, basis.p90) == (value, value, value), spread.field
                assert basis.headline_rank == 0.5, spread.field


def test_the_usable_test_and_the_check_read_one_margin(
    synthetic_scenario: dict[str, Any],
    write_scenario: Callable[[dict[str, Any]], Path],
    synthetic_engineering: dict[str, Any],
    as_engineering_bytes: Callable[[dict[str, Any]], bytes],
) -> None:
    """Objective: one floor, one comparison (the numerics lens's m1): the usable test compares
    the margin in percent, the number the artifact publishes and the believability check reads,
    so at a floor equal to a published margin both pass and at the next float above it both
    fail. On this sample the margin as a fraction against the floor over 100 failed the usable
    test at FY2032's own published margin while the check passed.

    Sample: the synthetic case with FY2031's fleet cost at $100M (FY2032's margin the lowest);
    the pick at the central market under a margin floor equal to FY2032's published margin, then
    the next float above it.

    Expected outcome: at the margin, no margin failure and every margin check passes; at the next
    float, the margin fails and FY2032's margin check warns, the other years' pass.
    """
    for year in synthetic_engineering["years"]:
        if year["year"] == 2031:
            year["annual_cost_musd"] = 100.0
    config = load_product_case_config(write_scenario(synthetic_scenario))
    view = engineering_view_from_bytes(
        as_engineering_bytes(synthetic_engineering),
        path="synthetic",
        reported_years=config.reported_years,
    )
    run = run_product_case(config, view)
    assert run.pick is not None and run.headline is not None
    lowest = min(run.headline.years, key=lambda year: year.totals.margin_pct)
    assert lowest.year == 2032
    choice = run.choices[run.pick.choice_id].choice
    floor = lowest.totals.margin_pct
    for margin_floor, holds in ((floor, True), (math.nextafter(floor, math.inf), False)):
        synthetic_scenario["floors"]["margin_pct"] = margin_floor
        side = load_product_case_config(write_scenario(synthetic_scenario))
        headline = outcome_in_market(side, view, choice, central_market(side))
        assert (UsableTest.MARGIN not in headline.failing_tests) is holds
        checks = {
            result.validation_id.rsplit(".", 1)[-1]: result.severity
            for result in believability_results(side, headline)
            if ".margin_at_or_above_floor." in result.validation_id
        }
        expected = ValidationSeverity.OK if holds else ValidationSeverity.WARN
        assert checks == {
            "2031": ValidationSeverity.OK,
            "2032": expected,
            "2033": ValidationSeverity.OK,
        }


def test_the_mid_rank_treats_ties_evenly() -> None:
    """Objective: the mid-rank is the share strictly below plus half the share equal (D10), the
    reading for a terminal whose headline ties most draws at its seats (the probe P12's FY2031
    small terminal: 1,958 of 2,000 tied, 2.1 percent below, mid-rank 51.0).

    Sample: 2,000 values, 42 below the headline and 1,958 equal to it.

    Expected outcome: the mid-rank (42 + 0.5 x 1,958) / 2,000 = 0.5105.
    """
    values = np.concatenate([np.full(42, 1.0), np.full(1_958, 2.0)])
    assert _basis_spread(values, 2.0).headline_rank == (42 + 0.5 * 1_958) / 2_000


def test_the_tone_test_is_dominated_and_the_offpeak_use_is_the_foundations(
    synthetic_scenario: dict[str, Any],
    write_scenario: Callable[[dict[str, Any]], Path],
    synthetic_engineering: dict[str, Any],
    as_engineering_bytes: Callable[[dict[str, Any]], bytes],
) -> None:
    """Objective: the single-tone use stays at most 7 s x A(t) / T(t) of the access use (each
    message is an access attempt), which at the shipped defaults' constants is 0.567 (the design's
    probe P6: W(1 - d) / 3.75 kHz = 704 tone-seconds a second a beam against 57 attempts); a
    terminal's off-peak downlink use is customers x r_off / (seats x r_busy) (the foundation's "A
    terminal's downlink use").

    Sample: the synthetic run's headline, every reported year.

    Expected outcome: tone use at most the bound in every year; the bound 0.567 at 8 MHz, d 0.67,
    57 attempts and 7 s; each terminal's off-peak use equal to its formula from its own block.
    """
    config = load_product_case_config(write_scenario(synthetic_scenario))
    view = engineering_view_from_bytes(
        as_engineering_bytes(synthetic_engineering),
        path="synthetic",
        reported_years=config.reported_years,
    )
    run = run_product_case(config, view)
    assert run.headline is not None
    for outcome, network in zip(run.headline.years, view.years, strict=True):
        bound = (
            view.airtime_high_s
            * network.iot_access_attempts_per_second
            / network.iot_single_tone_seconds_per_second
        )
        assert outcome.totals.single_tone_use <= bound * outcome.totals.access_use
        for entry in outcome.classes[:2]:
            assert entry.terminal is not None
            r_busy = entry.terminal.busy_hour_gb_per_month * 1e9 * 8 / (4 * 3_600 * 30)
            r_off = entry.terminal.offpeak_gb_per_month * 1e9 * 8 / (20 * 3_600 * 30)
            expected = entry.customers * r_off / (entry.terminal.seats * r_busy)
            assert entry.terminal.offpeak_downlink_use == pytest.approx(expected, rel=1e-12)
    assert round(7.0 * 57.0 / (8.0e6 * (1 - 0.67) / 3_750.0), 3) == 0.567
