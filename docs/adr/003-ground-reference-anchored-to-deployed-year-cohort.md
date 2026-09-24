# 003 - Ground Reference Anchored To Deployed-Year Cohort

Status: Accepted

## Context

The space model reports both new deployed-year capacity and cumulative living
fleet capacity. Ground comparison becomes misleading if it compares a single
ground cohort against the full living fleet or against a market-share target.

## Decision

The ground reference anchors to the promoted space model's 2036 deployed-year
cohort: nodes deployed that year, GPU packages, kW, and service life. It does
not anchor to living-fleet capacity or market share.

## Consequences

The comparison is narrower and easier to audit. It answers whether the same
annual cohort is in the same rough cost scale on the ground, while leaving
fleet-wide and market-share questions out of scope.

## Amendment (2026-09-23)

The anchor year is now derived from the configuration instead of hardcoded:
the base year plus ten (the year the year-10 cadence dial pins), or the final
window year when the horizon is shorter, which is 2036 at the default. The
ground comparison window follows the anchor cohort's service life (five years
at the default); the separate comparison-period dial was removed. The decision
itself is unchanged: the ground reference anchors to the deployed-year cohort,
never to the living fleet or market share.
