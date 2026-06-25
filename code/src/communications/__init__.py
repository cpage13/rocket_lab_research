"""Communications CELLULAR (direct-to-cell) cost model package.

A slim, roughly 6-variable cost-to-serve model for a Rocket Lab Neutron-launched
CELLULAR direct-to-cell (satellite-to-phone) constellation. The product is
cellular: the satellite talks to ordinary phones in coverage gaps, so the
subscriber unit is a PERSON (a phone subscriber), NOT a household. It mirrors the
data-center model's shape and reuses the shared spine in ``common`` unchanged.

It computes the total cost to build and hold the constellation to its
full-coverage size by FY2036, the cellular cost PER PERSON (the model's OWN
computed figure, never Starlink's disclosed broadband per-sub number), and a
space-versus-ground cost ratio (the ground per-subscriber cost is a marked,
two-regime INTERFACE the caller supplies). It is NOT a market-share, demand, or
revenue/DCF model; subscribers are coverage-driven, not capacity-derived.

The modules (built phase by phase):

* :mod:`communications.config`    -- the slim frozen Pydantic config tree.
* :mod:`communications.constants` -- the named ``Final`` defaults.
* :mod:`communications.engine`    -- the per-year cohort treadmill (Phase 2).
* :mod:`communications.ground`    -- the two-regime ground comparison (Phase 4).
* :mod:`communications.output`    -- the light typed output (Phase 5).

Units: money in $M; subscribers in PEOPLE; time in project years. Year 0 = FY2026
(Neutron first-flight year).
"""
