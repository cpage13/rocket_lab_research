"""Communications model package: two model families on one shared engine.

A slim cost-to-serve model for a Rocket Lab Neutron-launched connectivity
constellation, with two families sharing one engine:

* The Iridium model (formerly Model B), the published family, selected by a
  non-None ``iridium`` config block: the MSS lane on Iridium's owned L-band
  (purpose-built or in-chipset devices, never an unmodified phone). It DERIVES the
  per-satellite subscriber density from L-band physics, runs the shared fleet
  machinery, and publishes the four-bucket ARPU revenue case in the promoted
  artifact (``communications/models/iridium/default.json``).
* The High-Bandwidth Cellular Pure Play model (formerly Model A), the kept second
  family and the config default (no ``iridium`` block): CELLULAR direct-to-cell on
  partner cellular spectrum, with a fixed subscriber-density dial. It has no
  scenario file or promoted artifact; the equality tripwire test rides its defaults.

The package mirrors the data-center model's shape and reuses the shared spine in
``common`` unchanged. It computes the total cost to build and hold the
constellation (the fleet sized to serve a subscriber target, floored by coverage and
capped by saturation), the cost PER PERSON (the model's OWN computed figure, never
Starlink's disclosed broadband per-sub number), revenue as a price applied to a
sized base or to the built fleet's capacity, and a space-versus-ground cost ratio
(the ground per-subscriber cost is a marked, two-regime INTERFACE the caller
supplies). It is NOT a market-share, demand, or DCF model. Subscribers are PEOPLE,
never households and never summed with IoT devices.

The live modules:

* :mod:`communications.config`      -- the slim frozen Pydantic config tree.
* :mod:`communications.constants`   -- the named ``Final`` defaults.
* :mod:`communications.engine`      -- the per-year cohort treadmill + derivations.
* :mod:`communications.ground`      -- the two-regime ground comparison.
* :mod:`communications.json_output` -- the promoted Iridium JSON artifact writer.

Units: money in $M; subscribers in PEOPLE; time in project years. Year 0 = FY2026
(Neutron first-flight year).
"""
