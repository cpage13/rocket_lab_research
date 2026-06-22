# Communications Default Assumptions

This is the human-readable ledger for the default communications-model
assumptions. The machine-readable default scenario is
`code/scenarios/comms_default.yaml`; the promoted space model is
`communications/models/space/default.json`; the promoted ground reference is
`communications/models/ground/default.json`; the claim ledger is
`research/SOURCE_INDEX.md`; the hand-written conclusion (Phase 6) is
`communications/models/conclusion.md`.

The project asks whether Neutron-launched space connectivity could plausibly
beat ground on COST (the per-density cost-to-cost comparison and the retail
undercut check), NOT a market-share thesis. Demand is assumed, not modeled: if
the delivered price undercuts ground and that price is collectable, uptake
follows. The customers-served figure falls out of the spectrum-capacity physics
as a band, never a demand estimate. The default scenario is creator-selected,
reviewable, and expected to improve.

The canonical default outputs are dynamic JSON. The conclusion is hand-written
editorial prose tied to the promoted defaults. If defaults change, update this
ledger and re-promote the JSON, then review `communications/models/conclusion.md`
before treating it as current.

## Source-Status Taxonomy

| Source status | Meaning |
|---|---|
| `certified` | Directly supported by a primary or official source. |
| `sourced_estimate` | Estimated from credible external sources, but not an official exact value. |
| `derived_estimate` | Computed from sourced or scenario inputs using a stated formula. |
| `projection` | A forward-looking market or technical projection from an external source. |
| `extrapolation` | A project extrapolation from known or sourced behavior. |
| `scenario` | A chosen modeling assumption for feasibility analysis. |
| `placeholder` | A known open slot that should not support settled public claims. |
| `stale` | Known old material retained only for historical context. |

Public documentation must not present `placeholder` or `stale` items as settled
evidence. The default scenario currently carries two `placeholder` inputs (the
two payload-power dials, the NEEDS-RESEARCH antenna and comms bill-of-materials
basis); the release-status validation check FAILS truthfully on them, which is
the founder-visible flag working as intended, not a build error.

## Default-Assumption Ledger

| Claim ID | Assumption | Source status | Role | Source or path | Notes |
|---|---|---|---|---|---|
| `COMM-CADENCE-90` | The target case uses 90 launches per year in 2036 (the data-center cadence ramp, timelines aligned). | `scenario` | Model input, public doc claim | `inputs.config.launch.launches_at_year_10`; `business.years."2036".launches`; `research/SOURCE_INDEX.md` `COMM-082` | Venture-model target, reused from the data-center cadence machinery, not Rocket Lab guidance. |
| `COMM-LAUNCH-COST` | High-cadence launch cost is about $13.5M per Neutron flight at target cadence (about $13M to $13.5M band). | `scenario` | Model input, public doc claim | `inputs.config.launch.high_cadence_cost_musd`; `research/SOURCE_INDEX.md` `COMM-082` | Cadence-indexed scenario, reused from the data-center model, not official Rocket Lab cost guidance. |
| `COMM-SAT-LIFETIME-5Y` | Satellite service life is five years in the default model (test variant 7). | `scenario` | Model input, public doc claim | `inputs.config.constellation.satellite_lifetime_years`; `research/SOURCE_INDEX.md` `COMM-082` | Base-case design target, not field-proven satellite service life. |
| `COMM-FOUR-AREA-ANTENNA` | The antenna is the dominant per-satellite cost line: about $2.5M (direct-to-cell, the large folded array) and about $0.45M (broadband). | `scenario` | Model input, open research question (NEEDS-RESEARCH) | `inputs.config.constellation.direct_to_cell.antenna_cost_musd`; `inputs.config.constellation.broadband.antenna_cost_musd`; `research/SOURCE_INDEX.md` `COMM-082` | INTERIM bill-of-materials anchor pending research; the antenna is the one new comms research input. The associated payload-power dials are `placeholder`. |
| `COMM-FOUR-AREA-COMMS` | The comms electronics (modems, beam-forming, on-board processing, RF chain) is broken out: about $0.6M (direct-to-cell) and about $0.35M (broadband). | `scenario` | Model input, open research question | `inputs.config.constellation.direct_to_cell.comms_electronics_cost_musd`; `inputs.config.constellation.broadband.comms_electronics_cost_musd`; `research/SOURCE_INDEX.md` `COMM-082` | INTERIM bill-of-materials anchor pending research. |
| `COMM-FOUR-AREA-SOLAR` | The solar array is sized from the comms payload power draw at about $20k/kW (NOT the data-center $40k/kW, which the ledger flags as high). | `scenario` | Model input, public doc claim | `inputs.config.constellation.direct_to_cell.solar_cost_usd_per_kw`; `inputs.config.constellation.broadband.solar_cost_usd_per_kw`; `research/SOURCE_INDEX.md` `COMM-082` | Comms payload power is tens of kW, far below the data-center node's roughly 400 kW. |
| `COMM-FOUR-AREA-RADIATOR-BUS` | The radiator/bus (structure, avionics, propulsion plus thermal) is grouped and anchored light, AI-1-class: about $0.4M (direct-to-cell) and about $0.2M (broadband). | `scenario` | Model input, public doc claim | `inputs.config.constellation.direct_to_cell.radiator_bus_cost_musd`; `inputs.config.constellation.broadband.radiator_bus_cost_musd`; `research/SOURCE_INDEX.md` `COMM-082` | The radiator is minor at this power; grouped with the bus. |
| `COMM-COST-DOWN` | A learning-curve cost-down applies a 10 percent reduction per doubling of cumulative units built (from a reference of 1 unit). | `scenario` | Model input, public doc claim | `inputs.config.cost_down.learning_rate_per_doubling`; `inputs.config.cost_down.cost_down_reference_units`; `research/SOURCE_INDEX.md` `COMM-082` | INTERIM learning-curve form; per-unit cost falls as Rocket Lab builds volume. |
| `COMM-SPECTRUM-40MHZ` | The constellation leases one block of about 40 MHz under Supplemental Coverage from Space and reuses it across every beam; spectrum is a reported REQUIREMENT and a partner GATE, never a cost line (its leased cost is near zero, so it nets out). | `scenario` | Model input, public doc claim | `inputs.config.spectrum.leased_bandwidth_mhz`; `physical.years."2036".spectrum_to_acquire_mhz`; `research/SOURCE_INDEX.md` `COMM-082` | The requirement is always computed and emitted in MHz; the spectrum-as-cost disaster gate forbids a spectrum dollar line. |
| `COMM-PER-BEAM-CAPACITY` | Per-beam capacity comes from the empirical AST anchor (about 120 Mbps measured on about 40 MHz, scaled linearly with leased bandwidth), never from a naive bandwidth-times-spectral-efficiency division. | `derived_estimate` | Model output, public doc claim | `physical.years."2036".per_beam_capacity_mbps`; `physical.years."2036".naive_capacity_mbps`; `research/SOURCE_INDEX.md` `COMM-082` | The naive figure (spectral efficiency about 0.6 bps/Hz) is emitted only as a labeled cross-check. |
| `COMM-BEAMS-PER-SAT` | Each direct-to-cell satellite carries about 2,500 beams (the AST Block 2 design point). | `scenario` | Model input, public doc claim | `inputs.config.spectrum.beams_per_sat`; `research/SOURCE_INDEX.md` `COMM-082` | AST Block 2 reference design point. |
| `COMM-CUSTOMER-BAND` | The default per-satellite direct-to-cell planning band is 50,000 / 150,000 / 300,000 registered subscribers, from the per-user-rate and oversubscription band defaults under the inverted pairing. | `derived_estimate` | Model output, FOUNDER QUESTION (F-BAND) | `business.years."2036".total_served`; `research/SOURCE_INDEX.md` `COMM-082` | The biggest open question is the per-user rate. The output is always a band (low/mid/high), never a scalar; the band is inverse-paired with cost-per-customer. |
| `COMM-RATE-OVERSUB-BANDS` | The per-user-rate band is 2.0 / 3.0 / 6.0 Mbps and the oversubscription band is 1.0 / 1.5 / 2.0, both stored ascending; the customer band uses the inverted pairing (a higher rate provisions a fatter pipe and serves fewer subscribers). | `scenario` | Model input, public doc claim | `inputs.config.spectrum.target_per_user_rate_mbps`; `inputs.config.spectrum.oversubscription_factor`; `research/SOURCE_INDEX.md` `COMM-082` | The founder sets the engineering service level and the commercial packing independently. |
| `COMM-ARPU-SHARE` | The collectability reference is ARPU about $50/month and operator revenue share 0.5 (the collectable ceiling the revenue-ceiling reconciliation uses). | `scenario` | Model input, public doc claim (price reference, NOT demand) | `inputs.config.price_reference.arpu_usd_per_month`; `inputs.config.price_reference.operator_revenue_share`; `research/SOURCE_INDEX.md` `COMM-082` | A price/collectability reference, not a demand lever; demand is assumed. The collectable ceiling lands at about $300/sub/yr. |
| `COMM-RETAIL-REFERENCE` | The sparse-regime price-to-beat is the founder-set retail reference of about $100/month of full cell service. | `scenario` | Model input, FOUNDER-SET CONFIG | `inputs.config.price_reference.retail_reference_usd_per_month`; `research/SOURCE_INDEX.md` `COMM-082` | The founder's own chosen reference, not a sourced figure; the corpus carries individual ARPU around $50 and per-account ARPA around $147, so $100 sits between them. |
| `COMM-GROUND-COST-LINES` | The bottom-up ground cellular cost is built per density regime: the sparse fresh-build cost-out (towers about $0.25M/site, about 18,000 sites per million subs, backhaul, opex, amortized over 25 years) and the dense incumbent marginal defend floor (about 15 percent of ARPU). | `scenario` / `sourced_estimate` | Ground reference inputs, public doc claim | `inputs.config.ground.*`; `research/SOURCE_INDEX.md` `COMM-082`, `COMM-096` | The incumbent-marginal fraction (`COMM-096`) is `sourced_estimate`; the fresh-build lines are scenario anchors. The two regimes are reported separately and never blended. |
| `COMM-STARLINK-FLOOR` | The disclosed all-in Starlink cost floor is about $486/sub/yr (a third-party / disclosed-financials reference, not a Rocket Lab figure). | `sourced_estimate` | Ground reference input, honesty block | `inputs.config.ground.starlink_disclosed_all_in_cost_usd_per_sub_year`; `research/SOURCE_INDEX.md` `COMM-090` | The dual-space-cost honesty number: both the bottom-up chain figure and this disclosed floor are shown; the model never claims the chain beats the disclosed number as a win. |
| `COMM-TWO-CONSTELLATIONS-D2C-HEADLINE` | The model carries two parallel satellite classes (broadband, mass-bound, about 8 per launch; direct-to-cell, antenna-stow-bound, about 1 per launch) and takes the direct-to-cell customer band as the headline. | `scenario` | Modeling choice, flagged for founder confirmation (F22) | `physical.years."2036".broadband`; `physical.years."2036".direct_to_cell`; `research/SOURCE_INDEX.md` `COMM-082` | The per-class packing fork is explicit; which envelope binds depends on the class. The direct-to-cell band is the headline; the broadband fleet cost is tracked alongside. |

## Public Output Anchors

These values are derived from the promoted default JSON, not external facts.

| Output | Value | Source status | Model path |
|---|---|---|---|
| Steady-state direct-to-cell living fleet (2036) | 268 satellites | `derived_estimate` | `business.years."2036".direct_to_cell_living_fleet` |
| Steady-state served band (2036) | 13.4M / 40.2M / 80.4M subscribers (low/mid/high) | `derived_estimate` | `business.years."2036".total_served` |
| Steady-state cost per customer (2036) | $11.57 / $23.14 / $69.42 per year (low/mid/high) | `derived_estimate` | `business.years."2036".cost_annual_per_customer_usd` |
| Steady-state priced cost (cost x 1.5) (2036) | $17.36 / $34.71 / $104.13 per year (low/mid/high) | `derived_estimate` | `business.years."2036".priced_cost_per_customer_usd` |
| Collectable ceiling (ARPU x share x 12) | $300 per sub-year | `derived_estimate` | `business.years."2036".arpu_collectable_revenue_usd` |
| Sparse cost-to-cost ratio (mid) | about 0.02 (space far cheaper than a fresh ground build) | `derived_estimate` | `comparison.by_density.sparse.cost_to_cost.space_to_ground_ratio_mid` |
| Dense cost-to-cost ratio (mid) | about 0.26 (space below the incumbent marginal floor at the mid band) | `derived_estimate` | `comparison.by_density.dense.cost_to_cost.space_to_ground_ratio_mid` |
| Sparse retail undercut | passes (priced cost lands under the retail reference) | `derived_estimate` | `comparison.by_density.sparse.price_undercut.undercut_passes` |
| Revenue-ceiling collectable win | true (priced cost lands under both the collectable ceiling and retail) | `derived_estimate` | `comparison.revenue_ceiling.collectable_win` |
| Chain below disclosed Starlink floor | true (reported only; not claimed as a win) | `derived_estimate` | `comparison.starlink_floor.chain_below_disclosed_floor` |

## Maintenance Rule

When a default assumption changes, update this ledger, update
`research/SOURCE_INDEX.md` if the claim or source trail changes, re-promote both
the space and ground JSON with `uv run rklb-comms --promote`, and then review
`communications/models/conclusion.md`. Promotion does not rewrite the hand-written
conclusion for you. The default scenario's `placeholder` inputs (the payload-power
and antenna bill-of-materials basis) are the priority research items.
