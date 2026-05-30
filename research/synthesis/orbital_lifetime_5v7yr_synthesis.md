# Synthesis: Orbital Lifetime, 5 vs 7 Years for a Large Heavy Node

> Exploratory study (2026-05-29). Question: can a large, heavy, high-drag
> orbital compute node last 5 years in LEO sun-synchronous orbit, could it do 7,
> and what would that require (station-keeping versus a higher orbit), including
> the Neutron payload cost of going higher? This did NOT change the model or the
> assumptions file; it is a think-through to size the trade.

## Bottom line

The mass and payload cost of buying orbital longevity is small (single-digit
percent on every lever). 5 years is feasible but NOT automatic at a low SSO: the
node's huge deployed area makes it decay 6 to 13x faster than a normal satellite,
so the 5-year life requires either ~700 km of altitude or active drag make-up
propulsion. Extending to 7 years is cheap either way. The real cost of going
higher is not mass, it is radiation (an un-shieldable rise in GPU/HBM
single-event-upset rate) and a mandatory active deorbit system above ~600 to
650 km. The likely reason the design point is 5 years is revenue (aging silicon),
not orbit physics.

## The four inputs

| Doc | Key finding |
|---|---|
| `orbital/leo_lifetime_large_node_5v7yr.md` | Low ballistic coefficient (~3.6 to 7.3 kg/m^2 vs ~45 normal), so the node decays 6 to 13x faster. At 500 to 600 km it lasts only ~1.3 to 5 yr (mean solar), ~0.4 to 2 yr through solar max. 5-yr natural life needs ~600 to 660 km (recommend ~700 km); 7-yr needs ~630 to 690 km (recommend ~720 to 750 km). |
| `node_design/electric_propulsion_stationkeeping_5v7yr.md` | EP station-keeping at 550 km costs ~150 kg (5 yr) to ~184 kg (7 yr), ~2 to 3% of an 8 t node, inside the existing 250 to 550 kg propulsion line. Marginal 5-to-7-yr cost ~25 to 35 kg. Power is a non-issue (~2% of the array); thrust duty cycle is the limiter. |
| `orbital/higher_orbit_tradeoffs_lifetime.md` | Raising orbit is cheap in delta-v (~160 m/s to 800 km; ~50 to 240 kg EP). Binding side effect is RADIATION: TID rises toward low-tens of krad/yr by ~1,200 km and the GPU/HBM SEU rate climbs with proton flux (un-shieldable). Above ~600 to 650 km, passive deorbit no longer meets the 5-year rule, so an active deorbit system is mandatory. 7-yr natural life put at ~800 to 900 km. |
| `rocket_lab/neutron/neutron_payload_vs_orbit.md` | Neutron ~13 t reusable LEO. Realistic LEO-to-SSO penalty ~25 to 30% (~9.5 t to SSO, matching the deep docs), not the 10 to 20% headline. Higher SSO is cheap: only ~5% from baseline to 700 to 800 km. "Halve the payload" refuted. 12.5 t is the expendable/block-upgrade figure, not baseline reusable. |

## Integrated answer

1. 5-year life at a low SSO is conditional, not free: needs ~700 km altitude or
   active station-keeping. The project budgets propulsion, so this is consistent.
2. 7 years is a small step beyond 5 on either path: ~25 to 35 kg of extra
   propellant if staying low, or a modest altitude bump (~720 to 900 km) if flying
   higher, the latter costing only ~5% payload.
3. Mass/payload impact is NOT significant. EP is ~2 to 3% of node mass; a higher
   orbit is ~5% payload; delta-v and power do not bind. The "halve the mass"
   scenario does not occur.
4. The real trade is qualitative: stay low (small continuous station-keeping cost,
   benign radiation, easy passive deorbit) versus fly high (natural longevity for
   ~5% payload, but more GPU radiation/SEU burden and a mandatory deorbit system).
   Lean: do not over-climb; ~700 to 800 km with light station-keeping.
5. The design life is most likely revenue-limited, not orbit-limited: by year 7
   the silicon is two generations old and earns commoditized rates (see the
   project's revenue-decay research). The orbit can do 7 years cheaply.

## Contradiction to reconcile (light lint)

The two lifetime studies disagree on the 7-year altitude: `leo_lifetime_large_node`
says ~720 to 750 km, `higher_orbit_tradeoffs` says ~800 to 900 km. The cause is
different assumed effective drag areas and ballistic-coefficient normalizations.
Both are derived estimates (good to roughly +/- 50 to 150 km), and both flag the
same fix. Treat the 7-year natural-life altitude as a band of ~720 to 900 km until
firmed.

## Recommended next step (only if hardening this)

A node-specific numerical orbit propagation (STK, GMAT, or NASA DAS) at the chosen
altitude and effective drag area, plus a radiation run (SPENVIS or CREME96) to pin
the SEU rate and shielding mass. Until then, the band above is sufficient for
thinking the trade through.

## Scope note

Exploratory only. No change was made to the model, the scenarios, the promoted
JSON, or `data_center/assumptions.md`. The 5-year service life and all results
stand as-is pending a decision to revisit.
