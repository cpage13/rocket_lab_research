# 011 - IoT Is Capacity In The Engineering Model; Its Customers Come From The Product Case

Status: Accepted (2026-10-07, the investor's approval of the product-case design; written
2026-10-12, before its code: until that lands, `default.json` still carries ADR 007's two IoT
lines). Supersedes ADR 007. Replaces the consequence of ADR 006 that names the IoT lines.

## Context

ADR 007 held IoT as two lines of their own in the Iridium model, sold from the coverage floor.
Its reading that IoT uses a small share of a beam's uplink held for minimal-packet IoT alone: at
the coverage floor, the IoT check that `default.json` publishes at `iridium-v6`, on the device
counts of the two lines this decision removes, puts minimal-packet IoT at 1.8 percent of a
beam's uplink bits with the 20 percent MAC efficiency (0.4 percent without; its tones 1.3 to 2.3
percent), data IoT at 23.0 percent with it and 4.6 percent without, and the two lines together
at 24.8 and 5.0 percent. On 2026-10-06 the investor decided that IoT is two device classes,
minimal-packet IoT and data IoT, beside the small and mounted terminals, whose customers and
usage come from the product case's Monte Carlo ("If we barely use any of the network, then we
just increase usage as is ... So we just do a Pareto. That is why we do the Monte Carlo"). The
owned spectrum does not bound IoT the way it bounds people: its IoT room holds far more devices
than any market, so selling every IoT seat would publish revenue no market supports. The
investor keeps market assumptions out of the engineering model ("you don't want to mix your
market with your engineering and your production ... Keep it separate").

## Decision

The engineering model carries no IoT device count, no IoT price and no IoT revenue. For every
year and every reading it publishes IoT's room on the phone class's useful beams in the
uplink's share of the frame (payload bits after the MAC efficiency, random-access attempts,
single-tone time) and, for each IoT class alone at its engineering usage, the devices that room
holds by each view, the least of them and the view that binds. Below the coverage floor the
capacity is null, since IoT needs continuous coverage. IoT's customers, usage and revenue are
the product case's, which reads this model's promoted artifact and never feeds it. Each people
class still sells every seat its living fleet carries (ADR 006). Government stays out of
revenue, as ADR 007 decided: no government count, price or line, and the conclusions name the
EMSS contract.

## Consequences

The engineering case's revenue is its people classes' columns; its IoT is a capacity. The IoT
prices move to the product case's scenario. ADR 006's consequence "with the IoT lines on their
own and government left out of revenue (ADR 007)" now reads "with IoT as capacity, its revenue
the product case's, and government left out of revenue". `default.json` carries the room and
the capacities (`years[].iot`, `saturation.readings[].iot`); the conclusions show the
engineering and product cases side by side and never add IoT and government.
