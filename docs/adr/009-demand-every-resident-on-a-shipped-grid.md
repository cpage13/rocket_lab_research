# 009 - Demand Is Every Resident Of An Inhabited Cell, On A Shipped Population Grid

Status: Accepted (2026-10-04, with the saturation module's strategy, Revision 4)

## Context

The saturation curve needs a demand map. The model assumes the capacity it
finds is used; a market or take-up model is out of scope.

## Decision

Demand is every resident of a 0.25 degree cell with at least 1 person per
km^2 (take-up 1.0, the maximal-demand bound), from the EC JRC GHS-POP R2023A
2030 projection, aggregated and shipped in the repository under CC BY 4.0
with its attribution file.

## Consequences

The saturation number is robust to this choice across density thresholds, a
subscriber share and grid sizes: the curve's bands carry the thresholds' and
the grid's spread, and the saturation module's research note,
`research/direct_communication/iridium_saturation_module.md`, records the
subscriber-share run. The maximum use and the share of beams over people are
not: they are upper bounds, reported as bands.
