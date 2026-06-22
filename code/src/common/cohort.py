"""Generic service-life cohort cliff shared by both ventures: the half-open
[launch_year, launch_year + service_life) survival test and the living-cohort
filter."""

from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass

logger = logging.getLogger(__name__)


def cohort_is_alive_at(launch_year: int, year: int, service_life: int) -> bool:
    """The half-open service-life cliff test, as a free function.

    Args:
        launch_year: Cohort deployment year.
        year: Calendar year to test.
        service_life: Operating life in years (the hard cliff). Required.

    Returns:
        ``True`` iff ``launch_year <= year < launch_year + service_life``.
    """
    return launch_year <= year < launch_year + service_life


@dataclass(frozen=True)
class LivedCohort:
    """A set of units deployed in one calendar year, with a service-life cliff.

    The generic cohort shared by both ventures. Venture-specific payload
    (per-node GPU figures, per-satellite comms figures) lives on the
    venture's own cohort type; this carries only the launch year, the unit
    count, and the survival test.

    Attributes:
        launch_year: Calendar year this cohort was deployed.
        units_deployed: Number of units in this cohort (nodes, satellites).
    """

    launch_year: int
    units_deployed: int

    def is_alive_at(self, year: int, service_life: int) -> bool:
        """True iff this cohort is within the service-life cliff at ``year``.

        Args:
            year: Calendar year to test.
            service_life: Operating life in years (the hard cliff). Required,
                no default: the caller passes the configured life so the
                cliff cannot silently fall back to a constant.

        Returns:
            ``True`` iff ``launch_year <= year < launch_year + service_life``.
        """
        return cohort_is_alive_at(self.launch_year, year, service_life)


def living_cohorts(
    cohorts: Sequence[LivedCohort],
    year: int,
    service_life: int,
) -> list[LivedCohort]:
    """Return the cohorts alive at ``year`` under the service-life cliff.

    Args:
        cohorts: All cohorts deployed so far (any order).
        year: Calendar year to evaluate.
        service_life: Operating life in years (the hard cliff). Required.

    Returns:
        The sublist of ``cohorts`` whose half-open survival interval
        ``[launch_year, launch_year + service_life)`` contains ``year``.
    """
    return [c for c in cohorts if c.is_alive_at(year, service_life)]


__all__ = ["LivedCohort", "cohort_is_alive_at", "living_cohorts"]
