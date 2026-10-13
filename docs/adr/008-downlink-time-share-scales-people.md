# 008 - The Downlink Time Share Scales People Capacity

Status: Accepted (2026-10-04, with the saturation module's strategy, Revision 4); since ADR 011
(2026-10-13, `iridium-v7`), the Decision's "multiplies every people figure, and every capacity
figure except the satellite's peak, by d" holds for each people figure and each class's downlink
pool, while each class's off-peak per-user rate follows the pool only where the pool caps it, its
busy-hour per-user rate does not move with d, IoT's uplink, payload and single-tone rooms scale
with 1 - d and its random-access room with neither; and the Consequences' line on IoT staying far
from binding on the uplink share describes the IoT counts ADR 011 removed.

## Context

Iridium's 1616 to 1626.5 MHz block is time-division duplex: uplink and
downlink share the band in time, and Iridium's own frame is symmetric. The
capacity chain counted all 8 MHz as downlink.

## Decision

The downlink share d is a scenario setting, default 0.67 (Certus 700's 2 : 1
down-to-up rate split), with 0.5 (the symmetric frame) and 0.75 (an estimate)
as documented alternatives. The saturation curve is computed with the band in full-time use
(d = 1), and the engine multiplies every people figure, and every capacity
figure except the satellite's peak, by d, so any d runs on the one promoted
curve.

## Consequences

People at a given fleet scale with d, and each class's revenue with them;
the fleet does not change, since the cadence sets it. The rule ignores how d
relaxes each cell's people cap inside the curve: negligibly for the phone
class, and as a small under-count for the directional classes that grows
with the fleet, so their saturation numbers are conservative (the curve's
limits state it, and the saturation module's research note,
`research/direct_communication/iridium_saturation_module.md`, records the
measurement). IoT, mostly uplink, stays far from binding on the uplink share.
