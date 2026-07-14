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
| `RLDC-NODE-POWER-400KW` | The current simplification is one roughly 400 kW node per launch. | `derived_estimate` | Model output, public doc claim | `physical.years."2036".kw_per_node` | The promoted output reports about 422 kW per node in 2036. Node is not the spacecraft bus. A single node per launch is a modeling simplification: splitting one roughly 400 kW node into two roughly 200 kW nodes would halve each node's power and mass but duplicate the fixed roughly 2.5 t bus, so the pair carries somewhat less compute per launch. The single node is the mass-efficient choice, and the difference is small enough that it is not modeled in detail. |
| `RLDC-SERVICE-LIFE-5Y` | Service life is five years in the default model. | `scenario` | Model input, public doc claim | `inputs.config.fleet.service_life_years`; `research/SOURCE_INDEX.md` `THR-008` | Design target and base-case assumption, not field-proven GPU service life. |
| `RLDC-REVENUE-MULTIPLE-1_5X` | The central default revenue band is flat at 1.5x annualized cost, with no taper. | `scenario` | Model input, public doc claim | `inputs.config.revenue.central`; `business.years."2036".margin_central_pct` | The promoted output is a flat 33.3 percent gross margin. Low and high R variants are sensitivities. The margin is a chosen operator-target assumption, broadly consistent with comparable cloud and GPU-operator margins (see research/economics/operating_margins_and_revenue_multiple_2026.md), not a market-validated figure. |
| `RLDC-MARKET-100GW-2036` | The rough mid-2030s AI data-center market reference is order-of-100 GW. | `projection` | Public scale sanity check | `research/economics/ai_datacenter_tam.md`; McKinsey 2030 AI-related capacity projection | This is context for scale, not a market-share thesis. |
| `RLDC-GROUND-COST-BASIS` | The ground comparison asks whether a five-year equivalent ground data-center cohort is in the same order of magnitude as the orbital cohort. | `derived_estimate` | Ground reference boundary, public doc claim | `data_center/models/ground/default.json`; `research/SOURCE_INDEX.md`; `research/economics/ground_infrastructure_electricity_costs_2036.md` | Current ground output labels the comparison `same_order_of_magnitude`. It supports a cost-scale screen, not parity or market validation. |
| `RLDC-SOLAR-RADIATOR-COST` | The current model uses solar and radiator cost dials of $0.04M/kW each. | `scenario` | Model input, open research question | `inputs.config.physical.solar_cost_musd_per_kw`; `inputs.config.physical.radiator_cost_musd_per_kw` | Treat this as unresolved until better sourced. |
| `RLDC-SOLAR-RADIATOR-MASS` | The model uses a solar mass of 0.011 t/kW and a radiator mass of 0.012 t/kW (0.013 before a year-5 thermal step). | `scenario` | Model input, binding sensitivity | `inputs.config.physical.solar_mass_t_per_kw`; `inputs.config.physical.radiator_t_per_kw_post` and `radiator_t_per_kw_pre`; `research/node_design/node_mass_model.md` | Mass is the binding feasibility lever: the model is mass-limited, so these dials set how much compute each launch carries. The radiator figure assumes chips tolerate a hot enough coolant loop (Tjmax headroom) to run the radiator hot; see `node_mass_model.md`. A modest miss (about +20 to 30 percent) is absorbable; being off by about 2x on either array would make orbital AI compute non-viable on any launch vehicle, not just Neutron. Solar and radiator are dead-weight support mass that earns no revenue of its own and is already most of the payload, so doubling it roughly halves the revenue per kg deployed, and that ratio is set by the node, not the rocket. |
| `RLDC-ORBITAL-TOKEN-PREMIUM-2036` | If ground and orbital providers target comparable margins, the current 2036 default implies an orbital token would need to cost roughly 90 percent more than a comparable ground token. | `derived_estimate` | Model output interpretation, public doc claim | `comparison.orbit_to_ground_ratio`; `comparison.ground_total_five_year_cost`; `comparison.orbital_total_five_year_cost`; `research/SOURCE_INDEX.md` `RLDC-GROUND-ORBIT-RATIO-2036` | The underlying ratio is about 1.92x. This is not an extra secure-compute markup; it is the modeled cost ratio. |
| `RLDC-SOLAR-RADIATOR-COSTDOWN-SENSITIVITY` | If both solar and radiator costs move from $40k/kW toward $20k/kW, the 2036 orbital/ground cost ratio falls from about 1.92x to about 1.50x. | `scenario` | Sensitivity interpretation, public doc claim | `inputs.config.physical.solar_cost_musd_per_kw`; `inputs.config.physical.radiator_cost_musd_per_kw`; `research/SOURCE_INDEX.md` `THR-013` and `THR-016` | This is a sensitivity, not the default. Solar cost-down is better supported than radiator cost-down. |
| `RLDC-AI1-EQUIVALENT` | An AI-1-equivalent scenario (SpaceX's June 2026 satellite specs mapped onto the model's dials: 0.10 t bus, 0.003 t/kW solar, 0.0015 t/kW radiator, silicon pinned at B300/GB300) brackets the default from above at about 1.29x orbit-to-ground; with solar and radiator cost at $0.02M/kW the same scenario reads about 0.91x. | `scenario` | Labeled upper bracket, public doc claim | `code/scenarios/ai1_equivalent.yaml`; `data_center/ai1_comparison.md`; `research/competitors/starship_addendum.md` | AI-1 is an unflown June 2026 design reveal; these dials sit 2 to 6x past the conservative defaults, and running the scenario trips three validation flags: the two intended brackets (pinned silicon; radiator dial below the co-mounted floor), the model labeling its own upper bracket, plus the default-calibration deployed-capacity check, which fires on any non-default scenario. Cost dials stay at the defaults. Never the default scenario; if AI-1 flies at its published radiator spec, `THR-014` (0.006-0.008 t/kW) is the promotion path. |
| `RLDC-THERMAL-PACKAGE-DENSITY-SENSITIVITY` | If thermal-path improvements free enough mass for three to four more packages per node, the 2036 deployed-year cohort rises from 3,330 packages to roughly 3,600-3,690 packages. | `scenario` | Sensitivity interpretation, open model-hardening item | `physical.years."2036".gpus_per_node`; `anchor.gpu_packages`; `research/SOURCE_INDEX.md` `THR-014`, `THR-015`, and `THR-020` | This is not yet implemented as a model scenario. It should be treated as package-density upside, not a booked cost saving. |
| `RLDC-DEPLOYED-CAPACITY-2036-40MW` | The default 2036 newly deployed capacity is about 38 MW, rounded to `~40 MW/year`. | `derived_estimate` | Model output, public doc claim | `business.years."2036".kw_deployed_this_year` | This is the 2036 deployed-year cohort, not the living fleet and not market share. |

## Public Output Anchors

These values are derived from the promoted default JSON, not external facts.

| Claim ID | Output | Source status | Model path |
|---|---|---|---|
| `RLDC-SPACE-2036-GPU-PACKAGES-PER-NODE` | 37 GPU packages per node in 2036 | `derived_estimate` | `physical.years."2036".gpus_per_node` |
| `RLDC-SPACE-2036-LIVING-FLEET` | 268 living nodes in 2036 | `derived_estimate` | `business.years."2036".living_fleet` |
| `RLDC-SPACE-2036-ON-ORBIT-POWER` | About 112 MW active on-orbit node power in 2036 | `derived_estimate` | `business.years."2036".kw_living_fleet` |
| `RLDC-SPACE-2036-REVENUE-CENTRAL` | About $6.31B annual living-fleet revenue in 2036, central R band | `derived_estimate` | `business.years."2036".revenue_annual_fleet_musd_central` |
| `RLDC-SPACE-2036-MARGIN-CENTRAL` | A flat 33.3 percent gross margin, central R band | `derived_estimate` | `business.years."2036".margin_central_pct` |

## Ground Reference Boundary

The ground comparison is an order-of-magnitude screen for the same 2036
deployed-year GPU cohort. It currently reports about $3.68B of five-year ground
cost, about $7.05B of orbital build-and-launch reference cost, and a
ground/orbit ratio of about 0.52
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
roughly 90 percent token premium versus the comparable ground reference if both
providers target similar margins. The exact ratio is about 1.92x. This premium
comes from modeled cost, not a separate pricing feature.

The clean cost-down sensitivity is solar plus radiator together. Halving only
one line moves the ratio partway. Halving both modeled lines from `$40k/kW` to
`$20k/kW` moves the ratio to about 1.50x, or roughly a 50 percent token premium.
Thermal-path improvements should be kept separate: they can improve mass margin
and package density, but the current promoted JSON does not yet turn that into
a full cost scenario.

## Maintenance Rule

When a default assumption changes, update this ledger, update
`research/SOURCE_INDEX.md` if the claim/source trail changes, re-promote the
dynamic JSON, and then review `data_center/conclusion.md`. Promotion does not
rewrite the static conclusion for you.
