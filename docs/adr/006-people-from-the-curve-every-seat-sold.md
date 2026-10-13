# 006 - People Capacity Comes From The Saturation Curve, And Every Seat Is Sold On The Fleet The Cadence Builds

Status: Accepted (2026-10-04, with the saturation module's strategy, Revision 4); since ADR 011
(2026-10-13, `iridium-v7`), the Consequences' "with the IoT lines on their own" describes the IoT
lines ADR 011 removed, and, in ADR 011's words, its "with the IoT lines on their own and
government left out of revenue (ADR 007)" now reads "with IoT as capacity, its revenue the
product case's, and government left out of revenue".

## Context

The model multiplied a per-satellite subscriber density by the whole fleet, so
it counted beams over oceans and empty land as people capacity, though most
of a small fleet's beams land where nobody lives (the ocean factor, which
`default.json`'s readings carry). A subscriber target then fixed revenue, so
added satellites looked pointless: "You
wouldn't put these satellites up if your revenue is not going to increase"
(the investor, 2026-09-29).

## Decision

People capacity is read from the promoted saturation curve for every device
class in one run, times the downlink share (ADR 008) and the panel factor
(the scenario's `aperture_m2` / 25). There is no subscriber target and no
fleet target: the fleet grows at the comms share of the launch cadence. Every
seat is sold: each year each class serves the people its living fleet
carries, at its own monthly price held flat. Each class's column is the whole
fleet sold to that class. In the conclusions a mix weights the columns by
shares of the fleet's beams, shown only at shares the investor names; a
price haircut divides revenue only, since every seat is still sold; a market
haircut divides people and revenue; both together divide revenue by both
factors and people by the market factor alone. Each class's margin is its
own revenue against the whole fleet's annualized cost, and because that cost
does not move with a haircut or a mix, a margin is re-derived from the
divided or mixed revenue, never divided or averaged. Nothing is sold in a
year whose living fleet is below the coverage floor.

## Consequences

Revenue rises with the fleet: every class's own revenue rises every year
from the year the fleet reaches the coverage floor to the horizon's end,
with the IoT lines on their own and government left out of revenue (ADR
007); `default.json` carries
each class's people, revenue and margin by year. Every published people and
revenue figure moves, and they change only through the deliberate
conclusions review.
