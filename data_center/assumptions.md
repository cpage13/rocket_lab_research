# Data-Center Default Assumptions

This is the human-readable ledger for the default data-center assumptions. The
machine-readable default scenario is `code/scenarios/default.yaml`; the
promoted space model is `data_center/models/space/default.json`; the promoted
ground reference is `data_center/models/ground/default.json`; the claim ledger
is `research/SOURCE_INDEX.md`.

The project is not a DCF. It asks whether Rocket Lab should attack the
opportunity and whether Neutron-scale deployment could plausibly produce
revenue and margin under visible assumptions. The default scenario is
investor-selected, reviewable, and expected to improve.

The canonical default outputs are dynamic JSON. The conclusion is static
editorial prose tied to the promoted defaults. If defaults change, update this
ledger and the promoted JSON, then review `data_center/conclusion.md` before
treating it as current.

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
evidence.

## Default-Assumption Ledger

| Claim ID | Assumption | Source status | Role | Source or path | Notes |
|---|---|---|---|---|---|
| `RLDC-LAUNCH-COST-2036` | High-cadence launch cost is around $13M to $13.5M per Neutron launch once the model reaches target cadence. | `scenario` | Model input, public doc claim | `inputs.config.launch.high_cadence_cost_musd`; `research/SOURCE_INDEX.md` `NTR-009` | Cadence-indexed scenario conclusion, not official Rocket Lab cost guidance. |
| `RLDC-PAYLOAD-SSO-UPGRADE` | Payload capacity is 12.5 t to sun-synchronous orbit in the block-upgrade scenario. | `scenario` | Model input, public doc claim | `inputs.config.physical.mass_envelope_t`; `research/SOURCE_INDEX.md` `NTR-007` | Not a current published Neutron SSO guarantee. Anchored 2026-06-09 against the Neutron Payload User's Guide v1.0 (Jan 2025): its table publishes 13.0 t DRL at 500 km mid-inclination, and its performance charts read off to roughly 9.0-9.7 t DRL and 10.5-11.4 t expendable to SSO (chart read-offs, derived). The 12.5 t dial therefore sits roughly 10-19 percent above the published expendable read-offs and 29-39 percent above DRL: a block-upgrade scenario by design. Misses of a few percent are expected here; tracking them is what this ledger is for. |
| `RLDC-FAIRING-VOLUME-80M3` | The model carries 80 m3 of usable Neutron fairing volume as a transparency check; volume does not gate node sizing (mass binds). | `scenario` | Model input, transparency only | `code/scenarios/default.yaml` volume block; `code/src/data_center/constants.py` `NEUTRON_FAIRING_USABLE_VOLUME_M3`; `research/rocket_lab/neutron/neutron_specs.md` | Previously unsourced. Anchored 2026-06-09 against the Neutron Payload User's Guide v1.0 (Jan 2025), Figure 13: its dimensioned payload envelope integrates to roughly 185-190 m3 (read-off, derived), so the 80 m3 dial is roughly 2.3x conservative against the published envelope. A 2026-06-09 audit also found the model's stowed-volume bookkeeping understates array volume materially (rework pending approval); at flown stow ratios, volume would not bind this architecture below roughly 1 MW of node power against the published envelope, so mass remains the binding constraint under every accounting. |
| `RLDC-LAUNCH-SITE` | Launch is from Wallops (LC-3, MARS, Virginia) to start, the only built Neutron pad; the performance-optimal site for a sustained sun-synchronous campaign is a West Coast pad (Vandenberg-style), which the operator would relocate to. | `scenario` | Contextual assumption, not a model input | `research/rocket_lab/neutron/sso_us_launch_site_options.md`; `research/rocket_lab/neutron/sso_from_virginia_feasibility.md` | SSO from Wallops needs a southerly dogleg (~5 to 15% payload) and biases recovery to a droneship; a West Coast pad launches SSO straight south with no dogleg and re-enables RTLS. The model does not price launch site beyond launch cost; this is a forward assumption, not a current Rocket Lab plan. |
| `RLDC-CADENCE-90` | The target case uses 90 launches per year in 2036. | `scenario` | Model input, public doc claim | `inputs.config.cadence.launches_at_year_10`; `business.years."2036".launches` | Venture-model target, not Rocket Lab guidance. |
| `RLDC-CADENCE-CEILING-150` | The logistic launch ramp carries a 150 launches-per-year carrying-capacity parameter, scoped to the ten-year modeled window (investor clarification 2026-07-15): it stands for the launch pads and rocket production plausibly built within the window, not a cap on the system. Pads and rockets can both be built, so no cap applies beyond the window, and any longer-horizon projection must re-set this dial. | `scenario` | Model input (curve shape), public doc claim | `inputs.config.cadence.cadence_ceiling`; `research/SOURCE_INDEX.md` `NTR-010` | Within the promoted window the dial is nearly inert: the curve is pinned by the 14-at-2031 and 90-at-2036 anchors, and it shapes only the post-2036 slope: the 2040 extension (`RLDC-FORWARD-WINDOW-2040`) bends toward this dial, and a longer-horizon projection re-sets the dial and bends later. Real-world context: Falcon 9 has flown 165 launches in a year, with a roughly 209-per-year three-pad theoretical ceiling and per-pad turnaround as the binding factor (`research/peer_review/review_engineer.md`), so 150 per year on Neutron implies a comparable multi-pad operation. |
| `RLDC-NODE-POWER-400KW` | The current simplification is one roughly 750 kW node per launch (the claim id's 400 kW is the pre-rebase figure, kept for reference stability). | `derived_estimate` | Model output, public doc claim | `physical.years."2036".kw_per_node` | The promoted output reports about 753 kW per node in 2036 under the 2026-07-14 light-radiator rebase. Node is not the spacecraft bus. A single node per launch is a modeling simplification: splitting one node into smaller satellites duplicates the fixed roughly 2.5 t bus, so the single node is the mass-efficient choice; the architecture can move to smaller satellites over time without changing the modeling. |
| `RLDC-SERVICE-LIFE-5Y` | Service life is five years in the default model. | `scenario` | Model input, public doc claim | `inputs.config.fleet.service_life_years`; `research/SOURCE_INDEX.md` `THR-008` | Design target and base-case assumption, not field-proven GPU service life. |
| `RLDC-REVENUE-MULTIPLE-1_5X` | The central default revenue band is flat at 1.5x annualized cost, with no taper. | `scenario` | Model input, public doc claim | `inputs.config.revenue.central`; `business.years."2036".margin_central_pct` | The promoted output is a flat 33.3 percent gross margin. Low and high R variants are sensitivities. The margin is a chosen operator-target assumption, broadly consistent with comparable cloud and GPU-operator margins (see research/economics/operating_margins_and_revenue_multiple_2026.md), not a market-validated figure. |
| `RLDC-MARKET-100GW-2036` | The rough mid-2030s AI data-center market reference is order-of-100 GW. | `projection` | Public scale sanity check | `research/economics/ai_datacenter_tam.md`; McKinsey 2030 AI-related capacity projection | This is context for scale, not a market-share thesis. |
| `RLDC-GROUND-COST-BASIS` | The ground comparison asks whether a five-year equivalent ground data-center cohort is in the same order of magnitude as the orbital cohort. | `derived_estimate` | Ground reference boundary, public doc claim | `data_center/models/ground/default.json`; `research/SOURCE_INDEX.md`; `research/economics/ground_infrastructure_electricity_costs_2036.md` | Current ground output labels the comparison `same_order_of_magnitude`. It supports a cost-scale screen, not parity or market validation. |
| `RLDC-SOLAR-RADIATOR-COST` | The model uses solar and radiator cost dials of $0.02M/kW each (investor-set 2026-07-14; the prior $0.04M/kW pair was an uncited cycle-1 estimate and stays as the labeled conservative exception). | `scenario` | Model input, investor-set with sourced directional support | `inputs.config.physical.solar_cost_musd_per_kw`; `inputs.config.physical.radiator_cost_musd_per_kw`; `research/SOURCE_INDEX.md` `THR-013` and `THR-016` | The rationale is manufacturing scale on its own feet (vertical integration, internalized supplier margin, productized repetition, five-year life), deliberately not the temperature/area win, which is booked in the mass row below and never double-counted. Solar is the stronger leg (Rocket Lab's own silicon-array program); radiator is the weaker leg (no public $/kW data; the evidence gate stays a vendor quote or bottom-up BOM). A refreshed 2026-07 cost analysis is tracked in `research/node_design/`. |
| `RLDC-SOLAR-RADIATOR-MASS` | The model uses a solar mass of 0.011 t/kW and an AI-1-class radiator of 0.00165 t/kW, flat across years, on the deployed double-sided run-hot architecture (investor decision 2026-07-14; the prior co-mounted 0.012-0.013 posture is the labeled conservative exception). | `scenario` | Model input, binding sensitivity | `inputs.config.physical.solar_mass_t_per_kw`; `inputs.config.physical.radiator_t_per_kw_post` and `radiator_t_per_kw_pre`; `metadata.radiator_architecture`; `research/node_design/node_mass_model.md`; `research/SOURCE_INDEX.md` `THR-014` | Mass is the binding feasibility lever: the model is mass-limited, so these dials set how much compute each launch carries. The 0.00165 sits within 10 percent of AI-1's implied 0.0015 (110 m2 double-sided at 120 kW; the 70 kW/t whole-satellite budget forces the class) and requires the run-hot loop to close chip-side; see `node_mass_model.md`. With the light radiator, solar (0.011) is now most of the dead-weight support mass: a 2x radiator miss is absorbable, while a 2x solar miss would still gut the compute per launch on any vehicle. |
| `RLDC-ORBITAL-TOKEN-PREMIUM-2036` | If ground and orbital providers target comparable margins, the current 2036 default implies an orbital token would need to cost roughly 28 percent more than a comparable ground token. | `derived_estimate` | Model output interpretation, public doc claim | `comparison.orbit_to_ground_ratio`; `comparison.ground_total_five_year_cost`; `comparison.orbital_total_five_year_cost`; `research/SOURCE_INDEX.md` `RLDC-GROUND-ORBIT-RATIO-2036` | The underlying ratio is about 1.28x (2026-07-14 rebase; the prior default read 1.92x and is the labeled conservative exception). This is not an extra secure-compute markup; it is the modeled cost ratio. |
| `RLDC-SOLAR-RADIATOR-COSTDOWN-SENSITIVITY` | The conservative direction: returning both cost dials to $40k/kW raises the 2036 orbital/ground ratio from about 1.28x to about 1.69x, and the full prior posture (heavy co-mounted radiator plus $40k dials) reads about 1.92x. | `scenario` | Sensitivity interpretation, public doc claim (inverted 2026-07-14: the cost-down is now the default and the cost-up is the exception) | `inputs.config.physical.solar_cost_musd_per_kw`; `inputs.config.physical.radiator_cost_musd_per_kw`; `research/SOURCE_INDEX.md` `THR-013` and `THR-016` | Solar's $20k is better supported than radiator's; the ledger keeps the stress cases visible ($30-40k central-cautious, $60-100k radiator stress) so the model can fall back if the refreshed research or a vendor quote says so. |
| `RLDC-AI1-EQUIVALENT` | An AI-1-equivalent scenario (SpaceX's June 2026 satellite specs mapped onto the model's dials: 0.10 t bus, 0.003 t/kW solar, 0.0015 t/kW radiator, silicon pinned at B300/GB300) reads about 0.91x orbit-to-ground at the model's current $0.02M/kW cost dials (below ground parity), and about 1.29x at the old $0.04M/kW dials. | `scenario` | Labeled bracket, public doc claim | `code/scenarios/ai1_equivalent.yaml`; `data_center/ai1_comparison.md`; `research/competitors/starship_addendum.md` | AI-1 is an unflown June 2026 design reveal. Since the 2026-07-14 rebase the default itself carries the AI-1-class radiator (mass and architecture), so the equivalent now differs from the default mainly by pinned 2026 silicon and its lighter solar and bus; it trips the pinned-silicon and deployed-capacity validation flags by design. |
| `RLDC-THERMAL-PACKAGE-DENSITY-SENSITIVITY` | Superseded 2026-07-14: the thermal package-density upside this row tracked (a few extra packages per node from hot-loop mass savings) is now booked in the default via the AI-1-class radiator (66 packages per node in 2036, 5,940 in the cohort). | `stale` | Historical sensitivity, retained for context | `physical.years."2036".gpus_per_node`; `anchor.gpu_packages`; `research/SOURCE_INDEX.md` `THR-014`, `THR-015`, and `THR-020` | Kept so old references resolve; the live lever discussion is the mass row above. |
| `RLDC-DEPLOYED-CAPACITY-2036-40MW` | The default 2036 newly deployed capacity is about 68 MW (the claim id's 40 MW is the pre-rebase figure, kept for reference stability). | `derived_estimate` | Model output, public doc claim | `business.years."2036".kw_deployed_this_year` | This is the 2036 deployed-year cohort, not the living fleet and not market share. |
| `RLDC-FORWARD-WINDOW-2040` | Extending the default dials to a 2040 horizon (sole change: `metadata.horizon_years` from 10 to 14) reads 591 living nodes, about 448 MW, about $17.7B annual fleet revenue and $5.9B annual profit at the unchanged 33.3 percent margin, with cadence at 139 launches per year and still rising. The extension carries the ten-year infrastructure parameter (`RLDC-CADENCE-CEILING-150`) forward unchanged, so the curve bends toward that window's build-out; a longer-horizon projection re-sets the dial and bends later. | `extrapolation` | Labeled illustration, public doc claim | `code/scenarios/default.yaml` (`metadata.horizon_years`); the model's logistic cadence and five-year retirement | Not promoted output: 2037-2040 lean on silicon generations extrapolated past the last sourced one and trip the `pf_per_kw_in_band` validation flag by design (per-node density climbs to about 152 PF/kW by 2040). The 2036 row of the extended run matches the promoted default exactly. Recipe: copy the default scenario, set `horizon_years: 14`, run `rklb-value <copy> --json`. Verified 2026-07-15. |
| `RLDC-WRIGHTS-LAW-BAND` | The solar, radiator, and bus cost dials are flat across all years, so learning-curve decline is entirely unpriced. The corpus's analogue band (10 to 25 percent cost decline per doubling of cumulative units, weighted toward the shallow end; aerospace near 15 percent) is available as a labeled sensitivity on the built-hardware lines, never a booked saving. Cumulative nodes double about 2.4 times across 2032 to 2036 (55 built to 301), so even the shallow end implies a roughly one-quarter unbooked decline on those lines within the modeled window. | `sourced_estimate` | Labeled sensitivity, public doc claim | `research/strategy/self_launch_cadence_and_manufacturing_advantage_2026.md` Section 2 | External-industry analogues (Wright 1936 aircraft 20 percent, NASA aerospace about 15, solar PV about 20, Li-ion about 18, BCG cross-industry 10-25), never a measured Neutron or node figure. Learning rates are not reliably constant (Construction Physics 2024, in the same doc), so the band illustrates direction, not a plan. It scopes to the built-hardware lines only: NVIDIA silicon is bought, and launch already prices its own cadence learning. |

## Public Output Anchors

These values are derived from the promoted default JSON, not external facts.

| Claim ID | Output | Source status | Model path |
|---|---|---|---|
| `RLDC-SPACE-2036-GPU-PACKAGES-PER-NODE` | 66 GPU packages per node in 2036 | `derived_estimate` | `physical.years."2036".gpus_per_node` |
| `RLDC-SPACE-2036-LIVING-FLEET` | 268 living nodes in 2036 | `derived_estimate` | `business.years."2036".living_fleet` |
| `RLDC-SPACE-2036-ON-ORBIT-POWER` | About 200 MW active on-orbit node power in 2036 | `derived_estimate` | `business.years."2036".kw_living_fleet` |
| `RLDC-SPACE-2036-REVENUE-CENTRAL` | About $7.42B annual living-fleet revenue in 2036, central R band | `derived_estimate` | `business.years."2036".revenue_annual_fleet_musd_central` |
| `RLDC-SPACE-2036-MARGIN-CENTRAL` | A flat 33.3 percent gross margin, central R band | `derived_estimate` | `business.years."2036".margin_central_pct` |

## Ground Reference Boundary

The ground comparison is an order-of-magnitude screen for the same 2036
deployed-year GPU cohort. It currently reports about $6.56B of five-year ground
cost, about $8.40B of orbital build-and-launch reference cost, and a
ground/orbit ratio of about 0.78
(`comparison.ground_total_five_year_cost`;
`comparison.orbital_total_five_year_cost`;
`comparison.ground_to_orbit_ratio`). The output conclusion is
`same_order_of_magnitude`, and the input cells trace to per-input ground claims
in `research/SOURCE_INDEX.md`.

Do not use the ground comparison as a public parity claim. The research-backed
ground basis supports the current scale comparison; future work should refine
facility shell and fit-out, racked power and networking, electricity price, PUE,
utilization, cooling, operations, maintenance, and comparison-period scope.

## Premium And Sensitivity Boundary

For public wording, the clearest statement is that the current default implies a
roughly 28 percent token premium versus the comparable ground reference if both
providers target similar margins. The exact ratio is about 1.28x. This premium
comes from modeled cost, not a separate pricing feature.

The clean conservative sensitivity runs the other way (inverted 2026-07-14):
returning both cost dials to `$40k/kW` reads about 1.69x, and the full prior
posture (the heavy co-mounted radiator plus `$40k/kW` dials) reads about 1.92x,
the labeled conservative exception. The AI-1-equivalent bracket at the current
cost dials reads about 0.91x, below ground parity. The mass and cost channels
stay separate by design: the light radiator is booked in mass and architecture,
the 20/20 dials in manufacturing scale, never the same physics twice.

## Maintenance Rule

When a default assumption changes, update this ledger, update
`research/SOURCE_INDEX.md` if the claim/source trail changes, re-promote the
dynamic JSON, and then review `data_center/conclusion.md`. Promotion does not
rewrite the static conclusion for you.
