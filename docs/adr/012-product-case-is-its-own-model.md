# 012 - The Product Case Is Its Own Model On The Engineering Artifact; Its Headline Is The Central Market

Status: Accepted (2026-10-07, the investor's approval of the product-case design, restated that
day at the investor's terminal prices; written 2026-10-12, before its code; its code built
2026-10-13, `code/src/product_case/` with its artifact's schema `product-case-v1`, the artifact
not yet promoted).

## Context

The engineering models answer what the fleet can carry, every seat sold (ADR 005, 006, 011).
The investor wants a separate case of what the communications network would sell, from a demand
curve and a Monte Carlo ("you don't want to mix your market with your engineering and your
production ... Keep it separate"; "Take the clearly usable ones and then pick where you are"),
at the investor's prices held flat ("These prices are fixed, and the service improves").

## Decision

The product case is its own package, `code/src/product_case/`. It reads only the engineering
model's promoted artifact, its schema pinned and its SHA-256 recorded, and nothing it computes
feeds that model; the demand curve, the market draws, the usable test, the Pareto fronts and the
pick live only there. numpy is its runtime dependency too, in one module (ADR 010's scope
widened). The investor's prices are held flat; the pick chooses only each IoT class's usage, the
most median revenue among the usages usable in at least three quarters of the markets, or, when
none is, the most usable, warned; lower prices appear only as context. Every usage at the
investor's prices shares the terminals' fill, so the usage rises while its median revenue rises
and IoT's room holds in enough of the markets the terminals fill to keep it above that floor; it
can move with a price or a terminal change, in steps: a change that carries IoT's failures in the
filled markets across the floor's slack, the fill under the floor, or the median's peak past a
step moves it, and others leave it. Its headline is the pick at the central market, each market
response at the middle of its range. With the responses drawn independently and uniformly, each
class's customers there are, in the population of markets, its median; in the drawn sample, within
sampling error. So the headline is the typical market; among the markets in which the pick is
usable, which lean strong, it sits below their median, and the artifact publishes both spreads and
the headline's rank in each. At the central market the price response is 1, so for a given usage
an uncapped class's price change shows there as customers, not revenue; the headline moves with a
price through the usage the pick then takes.

## Consequences

Two communications artifacts, promoted in order, the engineering first; the product case is
re-promoted whenever the engineering artifact's bytes change. The engineering case keeps one
maximum, and a haircut of its numbers stays a division in the conclusion; the market view is the
product case, read beside the engineering case and never added to it. A later skewed market
range would move the headline off the median and must revisit this record.
