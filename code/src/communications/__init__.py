"""Communications model package: two model families on one shared fleet-and-cost loop.

A slim cost-to-serve model for a Rocket Lab Neutron-launched connectivity
constellation, with two families sharing one fleet-and-cost loop:

* The Iridium model (formerly Model B), the published family, selected by a
  non-None ``iridium`` config block: the MSS lane on Iridium's owned L-band
  (purpose-built or in-chipset devices, never an unmodified phone). Its fleet is
  every comms launch the Neutron cadence share allows, with no target and no cap.
  Every device class (the small terminal, the mounted terminal, the phone class)
  reads its people from the promoted saturation curve, the useful co-channel beams
  over the places people live, times the downlink share and the panel factor, and
  every seat is sold at the class's flat price, side by side in one run; IoT is
  published as capacity (ADR 011): the room on the phone class's useful beams and
  each IoT class's device capacity alone, never a count sold or revenue; each
  class's saturation number, its spectrum bound, is reported beside the cadence.
  The promoted artifact is ``communications/models/iridium/default.json``.
* The High-Bandwidth Cellular Pure Play model (formerly Model A), the kept second
  family and the config default (no ``iridium`` block): CELLULAR direct-to-cell on
  partner cellular spectrum, with a fixed subscriber-density dial, its fleet sized
  to a subscriber target, floored by coverage and capped by its fleet cap, then held.
  It has no scenario file or promoted artifact. The equality tripwire test runs it on
  its defaults with the subscriber target raised to 150,000,000 (a fleet target the
  horizon never reaches, so it flies every launch the cadence allows) and requires its
  shared fleet-and-cost record to equal that of an Iridium run on the config defaults with
  a default ``iridium`` block, not the shipped Iridium scenario.

The package mirrors the data-center model's shape and reuses the shared spine in
``common`` unchanged. Each family's record sits beside the shared fleet-and-cost
record (the deployment, the living fleet, the build, launch and replacement cost
lines and the annualized cost). The Iridium record carries each class's people,
revenue, own margin and useful beams by year, IoT's room and capacities by year and
at the readings, the readings at the reported fleets and the marginal intervals; the
cellular record carries its target, its served
base, its two revenue cases and its cost per person, which the ground comparison
sets against a ground cost (a marked, two-regime INTERFACE the caller supplies). It
is NOT a market-share, demand, or DCF model. People are PEOPLE, never households and
never summed with IoT devices.

The live modules:

* :mod:`communications.config`           -- the slim frozen Pydantic config tree.
* :mod:`communications.constants`        -- the named ``Final`` defaults.
* :mod:`communications.engine`           -- the shared fleet-and-cost loop and the
  cellular family.
* :mod:`communications.iridium`          -- the Iridium family: its entry, full-cadence
  rule, record and economics.
* :mod:`communications.saturation`       -- the saturation curve's computation and its
  command (the one module that imports numpy).
* :mod:`communications.saturation_curve` -- the curve's contract, loader, identity check
  and readings.
* :mod:`communications.ground`           -- the two-regime ground comparison.
* :mod:`communications.json_output`      -- the promoted Iridium JSON artifact writer.

Units: money in $M; people in PEOPLE; time in project years. Year 0 = FY2026
(Neutron first-flight year).
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
