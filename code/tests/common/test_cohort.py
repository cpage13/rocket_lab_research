"""Tests for the generic cohort cliff in ``common.cohort`` (Phase 0, T0.10)."""

from __future__ import annotations

import dataclasses

import pytest

from common.cohort import LivedCohort, cohort_is_alive_at, living_cohorts


def test_alive_at_launch_year_true() -> None:
    assert LivedCohort(2030, 5).is_alive_at(2030, 5) is True


def test_alive_within_window_true() -> None:
    # launch 2030, life 5 -> alive 2030..2034 inclusive of 2030, exclusive of 2035.
    assert LivedCohort(2030, 5).is_alive_at(2034, 5) is True


def test_dead_at_cliff_year_false() -> None:
    # half-open upper bound: 2030 + 5 = 2035 is the first dead year.
    assert LivedCohort(2030, 5).is_alive_at(2035, 5) is False


def test_dead_before_launch_false() -> None:
    assert LivedCohort(2030, 5).is_alive_at(2029, 5) is False


def test_living_cohorts_filters_correctly() -> None:
    cohorts = [LivedCohort(2028, 10), LivedCohort(2030, 20), LivedCohort(2033, 30)]
    alive = living_cohorts(cohorts, 2034, service_life=5)
    # 2028 has retired (2028 + 5 = 2033 <= 2034); 2030 and 2033 survive.
    assert alive == [LivedCohort(2030, 20), LivedCohort(2033, 30)]


def test_service_life_is_required() -> None:
    with pytest.raises(TypeError):
        LivedCohort(2030, 5).is_alive_at(2030)  # type: ignore[call-arg]


def test_units_deployed_preserved() -> None:
    assert LivedCohort(2031, 7).units_deployed == 7


def test_frozen() -> None:
    cohort = LivedCohort(2030, 5)
    with pytest.raises(dataclasses.FrozenInstanceError):
        cohort.launch_year = 2031  # type: ignore[misc]


def test_cohort_is_alive_at_matches_method() -> None:
    # Option A was taken: the free function and the method must agree on a grid.
    for launch in (2028, 2030, 2033):
        for life in (3, 5, 7):
            for year in range(2025, 2045):
                cohort = LivedCohort(launch, 1)
                assert cohort.is_alive_at(year, life) == cohort_is_alive_at(launch, year, life)
