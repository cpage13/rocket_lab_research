"""Communications cost model package: two selectable satellite-connectivity models.

A slim cost-to-serve model for a Rocket Lab Neutron-launched connectivity
constellation, with two selectable models sharing one engine:

* The High-Bandwidth Cellular Pure Play model (formerly Model A), the default:
  CELLULAR direct-to-cell (satellite-to-phone) on partner cellular spectrum. The
  satellite talks to ordinary phones in coverage gaps, so the subscriber unit is a
  PERSON (a phone subscriber), NOT a household.
* The Iridium model (formerly Model B), selected by a non-None ``iridium`` config
  block: the MSS lane on Iridium's owned L-band (purpose-built or in-chipset
  devices, never an unmodified phone). It DERIVES the per-satellite subscriber
  density from L-band physics, then runs the same fleet machinery.

The package mirrors the data-center model's shape and reuses the shared spine in
``common`` unchanged. It computes the total cost to build and hold the
constellation to its full-coverage size by FY2036, the cost PER PERSON (the
model's OWN computed figure, never Starlink's disclosed broadband per-sub number),
and a space-versus-ground cost ratio (the ground per-subscriber cost is a marked,
two-regime INTERFACE the caller supplies). It is NOT a market-share, demand, or
revenue/DCF model; subscribers are coverage-driven, not capacity-derived.

The live modules:

* :mod:`communications.config`      -- the slim frozen Pydantic config tree.
* :mod:`communications.constants`   -- the named ``Final`` defaults.
* :mod:`communications.engine`      -- the per-year cohort treadmill + derivations.
* :mod:`communications.ground`      -- the two-regime ground comparison.
* :mod:`communications.json_output` -- the promoted Iridium JSON artifact writer.

Units: money in $M; subscribers in PEOPLE; time in project years. Year 0 = FY2026
(Neutron first-flight year).
"""
