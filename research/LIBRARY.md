# Library — Research Catalog & Glossary

This is the catalog for the `research/` corpus. It is intentionally
research-only: it catalogs files that live under `research/` and does not
catalog model-run summaries, promoted model JSON, code outputs, archived
model reports, or current-state handoffs.

For status, stale/superseded notes, stakeholder input, and open questions, read
[RESEARCH_TRACKER.md](RESEARCH_TRACKER.md). For the evolving belief record, read
[vision/initial_thesis.md](vision/initial_thesis.md). Generated data-center
outputs live outside this catalog under `data_center/`.

---

## How To Read The Research

Start with the versioned thesis, then the latest synthesis, then the source
docs behind any claim you want to inspect:

- [vision/initial_thesis.md](vision/initial_thesis.md) — append-only thesis
  through Revision 7.
- [synthesis/wave5_synthesis.md](synthesis/wave5_synthesis.md) — latest full
  research synthesis in this folder; launch-cost framing is historical.
- [README.md](README.md) — research-wiki front door and navigation rules.
- [SOURCE_INDEX.md](SOURCE_INDEX.md) — claim-level source ledger for hard
  numbers and scenario assumptions.
- [RESEARCH_TRACKER.md](RESEARCH_TRACKER.md) — file status, audit notes, and
  backlog.
- Topic folders below — source research and historical review artifacts.

---

## Complete Research Catalog

### Framing

| File | What it is | Read it for |
|---|---|---|
| [README.md](README.md) | Research-wiki front door. | How the source base, claim ledger, tracker, and library fit together. |
| [LIBRARY.md](LIBRARY.md) | This catalog. | Research navigation and glossary. |
| [RESEARCH_TRACKER.md](RESEARCH_TRACKER.md) | Research Wiki tracker. | Status, stale notes, stakeholder input, and open questions. |
| [SOURCE_INDEX.md](SOURCE_INDEX.md) | Claim-level hard-number source ledger. | Whether a number is `certified`, `sourced_estimate`, `derived_estimate`, `projection`, `extrapolation`, `scenario`, `placeholder`, or `stale`. |
| [vision/initial_thesis.md](vision/initial_thesis.md) | Versioned thesis. | The belief history and current research/output boundary. |
| [direct_communication/README.md](direct_communication/README.md) | Communications workstream front door. | The adjacent Rocket Lab communications thesis and its scope. |

### AI Hardware

| File | What it is | Key takeaway |
|---|---|---|
| [ai_hardware/ai_hardware.md](ai_hardware/ai_hardware.md) | NVIDIA rack-scale hardware baseline. | Power and heat dominate the payload problem. |
| [ai_hardware/gpu_generational_roadmap.md](ai_hardware/gpu_generational_roadmap.md) | GPU/package roadmap through 2036. | Package count and kW/GPU are step functions, not fixed rack constants. |

### Competitors

| File | What it is | Key takeaway |
|---|---|---|
| [competitors/starcloud.md](competitors/starcloud.md) | Starcloud and orbital data-center competitors. | Competitors validate demand; heavy lift changes economics and timing. |
| [competitors/starship_addendum.md](competitors/starship_addendum.md) | Starship competitive addendum. | The real near-term risk is capital/customer capture by Starship-gated rivals. |

### Debate

| File | What it is | Key takeaway |
|---|---|---|
| [debate/README.md](debate/README.md) | Bull/bear debate rules. | Process artifact for adversarial review. |
| [debate/bear_case.md](debate/bear_case.md) | Bear case, three rounds. | Historical economics are superseded; bounded R&D still survives. |
| [debate/bull_case.md](debate/bull_case.md) | Bull case, three rounds. | No physics wall; build-to-learn remains the narrowed case. |

### Economics

| File | What it is | Key takeaway |
|---|---|---|
| [economics/ai_datacenter_tam.md](economics/ai_datacenter_tam.md) | AI data-center market and TAM. | A small share of inference demand can still be a large business. |
| [economics/ambition_case.md](economics/ambition_case.md) | The roughly $5B/yr scenario. | Buildout, cadence, and capital constrain the go-for-it case. |
| [economics/energy_operating_costs.md](economics/energy_operating_costs.md) | Energy, water, and operating costs. | Avoided terrestrial opex is real but second-order to launch/node capex. |
| [economics/ground_infrastructure_electricity_costs_2036.md](economics/ground_infrastructure_electricity_costs_2036.md) | Ground infrastructure and electricity cost basis for the 2036 deployed-year cohort. | Current ground reference is about `$3.68B` over five years; electricity is only about `$150M`, and promoted JSON now carries per-input source statuses. |
| [economics/gpu_cost_trajectory.md](economics/gpu_cost_trajectory.md) | GPU/package acquisition-cost trajectory. | Cost growth is lumpy and package-driven, not a simple rack doubling. |
| [economics/gpu_hour_rental_rates.md](economics/gpu_hour_rental_rates.md) | GPU-hour rental rates over time. | Rental rates track acquisition cost more than FLOPS. |
| [economics/hyperscaler_margins.md](economics/hyperscaler_margins.md) | Margin pools and premium logic. | Premium must attach to scarce attributes, not commodity FLOPS. |
| [economics/moonshot_150b.md](economics/moonshot_150b.md) | $150B/yr moonshot stress test. | Neutron is short by roughly an order of magnitude-plus for this tier. |
| [economics/moonshot_50b.md](economics/moonshot_50b.md) | $50B/yr moonshot stress test. | $50B/yr needs a fundamentally larger launch vehicle. |
| [economics/premium_value_case.md](economics/premium_value_case.md) | Why customers might pay for orbital compute. | Sovereignty, scarce capacity, and zero water are the premium legs. |
| [economics/rack_cost_trajectory.md](economics/rack_cost_trajectory.md) | Early rack-cost trajectory. | Historical; superseded by GPU/package cost work. |
| [economics/revenue_economics_2026.md](economics/revenue_economics_2026.md) | 2026 frontier-compute revenue layers. | Market data stands; old calculator critique sections are stale. |
| [economics/revenue_per_watt.md](economics/revenue_per_watt.md) | Revenue per GW/rack. | Separates IaaS economics from integrated inference-service economics. |

### Laser Communications

| File | What it is | Key takeaway |
|---|---|---|
| [laser_comms/comms_business_case.md](laser_comms/comms_business_case.md) | Communications business case. | A focused B2B/B2G private orbital network is plausible; it is not Starlink. |
| [laser_comms/constellation_mesh.md](laser_comms/constellation_mesh.md) | Constellation and mesh design. | Laser range does not bind; service architecture and ground reach do. |
| [laser_comms/optical_comms.md](laser_comms/optical_comms.md) | Optical comms baseline. | Optical is primary; terminal roadmap remains a gating risk. |
| [laser_comms/optical_ground_stations.md](laser_comms/optical_ground_stations.md) | Optical ground stations. | Geographic diversity beats one large telescope. |
| [laser_comms/rf_limited_service.md](laser_comms/rf_limited_service.md) | Limited RF B2B service. | A modest RF sliver can be a backup/complement, not the primary product. |
| [laser_comms/rf_satcom.md](laser_comms/rf_satcom.md) | RF satcom comparison. | RF is unattractive as the main path for a new mass-market entrant. |

### LLM Compute

| File | What it is | Key takeaway |
|---|---|---|
| [llm_compute/inference_scaling.md](llm_compute/inference_scaling.md) | Production inference scaling. | One NVL72-class rack can serve a frontier inference model. |
| [llm_compute/minimum_viable_scale.md](llm_compute/minimum_viable_scale.md) | Minimum viable service scale. | Commercial service starts around a multi-node replica deployment. |
| [llm_compute/multi_rack_inference.md](llm_compute/multi_rack_inference.md) | Multi-rack inference over laser mesh. | Replica/pipeline/expert parallelism can span satellites; tensor parallelism stays local. |

### Node Design

| File | What it is | Key takeaway |
|---|---|---|
| [node_design/hot_chip_thermal_trajectory.md](node_design/hot_chip_thermal_trajectory.md) | Hot-loop thermal trajectory. | Hotter coolant loops shrink radiator mass but trade against reliability. |
| [node_design/node_mass_model.md](node_design/node_mass_model.md) | Node mass and fairing fit. | One-rack nodes are mass-tight but feasible; two-rack Neutron nodes are not baseline. |
| [node_design/rack_internals.md](node_design/rack_internals.md) | Rack component/mass breakdown. | Compute trays dominate mass; cabling is second-order. |
| [node_design/rack_splitting.md](node_design/rack_splitting.md) | Rack splitting and fractional inference nodes. | Smaller inference nodes are plausible later, especially with optical/NVLink evolution. |
| [node_design/reliability_failure_handling.md](node_design/reliability_failure_handling.md) | Reliability and graceful degradation. | GPU attrition and coolant-loop failures drive architecture. |
| [node_design/self_built_rack.md](node_design/self_built_rack.md) | Self-integrated rack strategy. | Rocket Lab should integrate spacecraft/power/thermal around bought compute, not become a server OEM. |
| [node_design/solar_radiator_trajectory.md](node_design/solar_radiator_trajectory.md) | Solar/radiator scaling. | Solar and radiator mass become the wall before cost does. |
| [node_design/space_solar_costdown_2030_2036.md](node_design/space_solar_costdown_2030_2036.md) | Fresh solar cost-down research for 2030-2036. | `$20k/kW` solar is plausible as a 2036 sensitivity, but `$40k/kW` should remain the public default until Rocket Lab publishes integrated array cost/performance or the project builds a bottom-up internal-cost model. |
| [node_design/radiator_costdown_2030_2036.md](node_design/radiator_costdown_2030_2036.md) | Radiator cost-down and hot-loop trajectory. | `$40k/kW` remains a cautious default; `$20k/kW` and `0.006-0.008 t/kW` are useful 2036 upside sensitivities, but cost evidence remains weak and GPU temperature limits require a chip-to-panel thermal model. |
| [node_design/gpu_temperature_cooling_limits.md](node_design/gpu_temperature_cooling_limits.md) | GPU/package temperature, liquid-cooling, and orbital radiator-temperature research. | Warmer coolant and hotter radiator operation are plausible high-leverage levers, but junction temperature, coolant temperature, and radiator surface temperature must be kept separate. |
| [node_design/gpu_hotter_operation_reliability_2030_2036.md](node_design/gpu_hotter_operation_reliability_2030_2036.md) | GPU/HBM hotter-operation and reliability research for 2030-2036. | Public evidence supports warmer coolant, lower thermal resistance, and hotter radiator surfaces more strongly than it supports a literal `+10-20 deg C` sustained GPU junction lift; `+20 deg C` should remain unsafe for the default five-year orbital model. |
| [node_design/electric_propulsion_stationkeeping_5v7yr.md](node_design/electric_propulsion_stationkeeping_5v7yr.md) | Electric-propulsion station-keeping mass for 5 vs 7 years at low SSO. | About `150 kg` (5 yr) to `184 kg` (7 yr) for an 8 t node, roughly 2 to 3% of mass and inside the existing 250 to 550 kg propulsion line; the marginal 5-to-7-year cost is only ~25 to 35 kg and power is a non-issue. Exploratory (2026-05-29). |

### Orbital

| File | What it is | Key takeaway |
|---|---|---|
| [orbital/orbit_types_primer.md](orbital/orbit_types_primer.md) | Orbit primer. | SSO is a LEO subtype; relay layers change contact time. |
| [orbital/orbits_environment.md](orbital/orbits_environment.md) | SSO, radiation, and debris environment. | Dawn-dusk SSO reduces eclipse; SSO payload remains estimated. |
| [orbital/thermal_analysis.md](orbital/thermal_analysis.md) | Early thermal sizing. | Historical; later mass/lint work supersedes radiator-area numbers. |
| [orbital/leo_lifetime_large_node_5v7yr.md](orbital/leo_lifetime_large_node_5v7yr.md) | LEO natural lifetime vs altitude for a large high-drag node (5 vs 7 yr). | The huge deployed area gives a very low ballistic coefficient (~3.6 to 7.3 vs ~45 kg/m2), so the node decays 6 to 13x faster; 500 to 600 km lasts only ~1.3 to 5 yr (~0.4 to 2 yr through solar max); a 5-yr natural life needs ~700 km and 7 yr needs ~720 to 750 km. Exploratory (2026-05-29). |
| [orbital/higher_orbit_tradeoffs_lifetime.md](orbital/higher_orbit_tradeoffs_lifetime.md) | Higher-orbit tradeoffs for a 7-year natural life. | Delta-v is not binding (~160 m/s to 800 km); the binding side effect is radiation (rising TID and an un-shieldable GPU/HBM single-event-upset rate that climbs with altitude); above ~600 to 650 km a mandatory active deorbit system is required; 7-yr natural life put at ~800 to 900 km. Exploratory (2026-05-29). |

### Peer Review

| File | What it is | Key takeaway |
|---|---|---|
| [peer_review/README.md](peer_review/README.md) | Peer-review folder guide. | Process entry point for the QA passes. |
| [peer_review/consistency_review.md](peer_review/consistency_review.md) | Historical consistency review. | Useful audit of an older data-center analysis shape. |
| [peer_review/peer_review_1.md](peer_review/peer_review_1.md) | Independent audit 1. | Source/consistency review of the research corpus. |
| [peer_review/peer_review_2.md](peer_review/peer_review_2.md) | Independent audit 2. | Source/consistency review of the research corpus. |
| [peer_review/peer_review_3.md](peer_review/peer_review_3.md) | Independent audit 3. | Source/consistency review of the research corpus. |
| [peer_review/peer_review_4.md](peer_review/peer_review_4.md) | Historical end-document review. | Audits the former root conclusion and thesis state. |
| [peer_review/review_economist.md](peer_review/review_economist.md) | Economist review of the superseded M5 model. | Finds depreciation, capital, and double-count risks. |
| [peer_review/review_engineer.md](peer_review/review_engineer.md) | Engineering review of the superseded M5 model. | Flags cadence, service-life, and two-rack assumptions. |
| [peer_review/structural_review.md](peer_review/structural_review.md) | Historical structure review. | Useful for repository-cleanliness history, not current navigation. |
| [peer_review/triage_and_fix_plan.md](peer_review/triage_and_fix_plan.md) | Peer-review triage plan. | Historical fix plan; many targets have moved or been retired. |

### Rocket Lab

| File | What it is | Key takeaway |
|---|---|---|
| [rocket_lab/electron/electron_specs.md](rocket_lab/electron/electron_specs.md) | Electron specs. | Electron is operational context and possible light-relay launcher, not the data-center launcher. |
| [rocket_lab/neutron/launch_cost_economics.md](rocket_lab/neutron/launch_cost_economics.md) | Internal Neutron launch-cost estimate. | Internal marginal cost is estimated and remains a key uncertainty. |
| [rocket_lab/neutron/neutron_specs.md](rocket_lab/neutron/neutron_specs.md) | Neutron specs. | Published LEO/fairing data are known; SSO payload is not published. |
| [rocket_lab/neutron/payload_and_block_upgrade.md](rocket_lab/neutron/payload_and_block_upgrade.md) | SSO payload and block-upgrade estimate. | Working SSO payload and block-upgrade values are estimates, not RL-published facts. |
| [rocket_lab/neutron/neutron_payload_vs_orbit.md](rocket_lab/neutron/neutron_payload_vs_orbit.md) | Neutron payload vs orbit (LEO, SSO, higher SSO). | About 13 t reusable to LEO; the LEO-to-SSO penalty is ~25 to 30% (~9.5 t to SSO, matching the deep docs), not the 10 to 20% headline; higher SSO is cheap (~5% to 700 to 800 km); "halve the payload" is refuted and the 12.5 t figure is expendable/block-upgrade, not baseline reusable. Exploratory (2026-05-29). |
| [rocket_lab/neutron/sso_recovery_cadence_falcon_analogue.md](rocket_lab/neutron/sso_recovery_cadence_falcon_analogue.md) | SSO launch and booster recovery for Neutron, via the Falcon 9 analogue. | SSO does not force expendable: Falcon recovers boosters on SSO/polar missions (RTLS for light-to-moderate, drone ship ~600 to 675 km for heavy), and Neutron's primary mode is RTLS at Wallops, so the ~25 to 30% SSO penalty already assumes recovery (no expendable surcharge); RTLS suits high cadence. Open question: whether Neutron can reach SSO from Wallops (~38 to 60 degree corridor) without a dogleg that adds to the penalty. Exploratory (2026-05-29). |
| [rocket_lab/neutron/sso_from_virginia_feasibility.md](rocket_lab/neutron/sso_from_virginia_feasibility.md) | Can Neutron reach SSO from its Virginia (Wallops LC-3) site? | Probable-yes-with-a-dogleg, not a guarantee. LC-3 (MARS, Wallops, Virginia) confirmed as Neutron's pad (ribbon-cut Aug 2025). SSO (~98 degrees) is outside the standard 38 to 60 degree Wallops corridor, so it needs a southerly-Atlantic dogleg; the PUG and the Virginia Spaceport Authority say it is reachable, and Falcon's SAOCOM 1B flew ~98 degrees from the East Coast. Caveats: no orbital SSO has ever flown from Wallops (stated-but-unflown), and the dogleg adds an estimated ~5 to 15% payload on top of the ~25 to 30% SSO penalty (reusable Virginia-SSO budget ~8 to 9.5 t). Exploratory (2026-05-29). |
| [rocket_lab/neutron/sso_us_launch_site_options.md](rocket_lab/neutron/sso_us_launch_site_options.md) | Best US launch site for a high-cadence Neutron SSO campaign: stay at Wallops or relocate, and where. | Wallops is good enough to START (near-term mandatory: LC-3 is the only built Neutron pad) but not SSO-optimal, since the East-Coast dogleg costs an estimated extra ~5 to 15% payload and biases recovery to a droneship. Vandenberg (West Coast) is the performance-optimal relocation (launches SSO straight south over open Pacific, no dogleg, RTLS re-enabled), though Rocket Lab has no public West Coast Neutron plan yet. Geography correction: "south toward the equator" helps eastward low-inclination launches, not SSO (~98 degrees regardless of latitude); what matters is an unobstructed retrograde azimuth over open ocean. Recovery tiers (15 t expendable / 13 t droneship / 8.5 t RTLS-to-LEO) make recovery mode a first-order payload driver. Exploratory (2026-05-30). |
| [rocket_lab/overview.md](rocket_lab/overview.md) | Rocket Lab company overview. | Rocket Lab is unusually vertically integrated for this thesis. |
| [rocket_lab/space_hardware_capabilities.md](rocket_lab/space_hardware_capabilities.md) | Rocket Lab hardware capabilities. | Launch, bus, solar, mechanisms, and comms are strong; deployable radiators are the gap. |

### Strategy

| File | What it is | Key takeaway |
|---|---|---|
| [strategy/README.md](strategy/README.md) | Engineer/CFO strategy-loop rules. | Process artifact for the cooperative strategy debate. |
| [strategy/optimized_strategy.md](strategy/optimized_strategy.md) | Historical optimized build strategy. | Converges on a gated, demand-pulled ramp; old conclusion references are historical. |

### Synthesis

| File | What it is | Key takeaway |
|---|---|---|
| [synthesis/lint_report.md](synthesis/lint_report.md) | First wiki lint pass. | Historical health snapshot; later work superseded several fixes. |
| [synthesis/lint_report_2.md](synthesis/lint_report_2.md) | Second wiki lint pass. | Historical post-wave-5 health snapshot. |
| [synthesis/preliminary_findings.md](synthesis/preliminary_findings.md) | Wave-1 synthesis. | No physics wall found, but many numbers later changed. |
| [synthesis/wave4_synthesis.md](synthesis/wave4_synthesis.md) | Wave-4 synthesis. | Establishes payback/GPU-obsolescence as the crux; launch-cost framing is historical. |
| [synthesis/wave5_synthesis.md](synthesis/wave5_synthesis.md) | Wave-5 synthesis. | Latest full synthesis: flyability crossover resolves at the favorable generation, conditionally. |
| [synthesis/orbital_lifetime_5v7yr_synthesis.md](synthesis/orbital_lifetime_5v7yr_synthesis.md) | Synthesis of the 5-vs-7-year orbital-lifetime study (4 docs). | The mass/payload cost of longevity is single-digit percent on every lever; 5 years is not free at low SSO (needs ~700 km or propulsion) but 7 years is cheap either way; the real trade is radiation plus mandatory deorbit (fly high) vs continuous station-keeping (stay low); design life is likely revenue-limited (aging silicon), not orbit-limited; the 7-yr natural-life altitude is a band ~720 to 900 km pending a numerical propagation. Exploratory (2026-05-29). |

### Valuation

| File | What it is | Key takeaway |
|---|---|---|
| [valuation/ai_compute_trajectory.md](valuation/ai_compute_trajectory.md) | Compute trajectory research. | FLOPS gains mostly accrue to buyers unless revenue tracks cost. |
| [valuation/projection_2026_2036.md](valuation/projection_2026_2036.md) | Historical fleet projection narrative. | Retained as research history; current generator/output paths are outside `research/`. |
| [valuation/rklb_baseline_financials.md](valuation/rklb_baseline_financials.md) | Reported Rocket Lab financial baseline. | Grounds company revenue, margins, backlog, cash, and profitability in filings. |
| [valuation/rklb_forward_trajectory.md](valuation/rklb_forward_trajectory.md) | Forward Rocket Lab trajectory. | Neutron cadence/cost and market sizing are central uncertainties. |
| [valuation/trajectory_notes.md](valuation/trajectory_notes.md) | Trajectory scratchpad. | Working notes, not a finished sourced memo. |

---

## Glossary

**Research corpus** — the evidence base under `research/`: source research,
synthesis, lint passes, debate, strategy, peer review, and thesis history.

**Source index** — the claim-level ledger that records whether hard numbers are
certified facts, sourced estimates, derived estimates, external projections,
project extrapolations, scenarios, placeholders, or stale history.

**Static conclusion** — the reviewed human-readable conclusion for the promoted
defaults. It does not live in `research/`; the default data-center conclusion
lives under `data_center/`.

**Model JSON** — machine-readable model output. It is generated/promoted outside
`research/`, with the default data-center model under `data_center/models/`.

**Node** — the project product unit: one orbital spacecraft carrying GPU
packages plus bus, power, thermal, and comms. Older research sometimes says
"rack" when it means the product unit; that is historical terminology.

**Rack** — NVIDIA hardware terminology: a cabinet-scale compute product such as
NVL72. Use "rack" for NVIDIA hardware, not for the project product.

**Package** — the NVIDIA GPU package as sold and modelled, even when it carries
multiple compute dies.

**R band** — the model's revenue-to-cost band: `revenue = R * cost`, with low,
central, and high trajectories.

**Neutron** — Rocket Lab's reusable medium-lift rocket; the assumed launcher for
the data-center node.

**Electron** — Rocket Lab's operational small-lift rocket; context only for this
data-center thesis.

**SSO** — Sun-synchronous orbit. Dawn-dusk SSO is the enabling orbit because it
reduces eclipse and battery burden.

**Ballistic coefficient (BC):** mass per unit drag area (kg/m2) of a spacecraft.
A low BC means high drag relative to mass, so the node decays faster; the large
deployed area of a data-center node gives an unusually low BC and a short natural
orbital lifetime at low altitude.

**Single-event upset (SEU):** a transient bit-level error caused by an energetic
particle striking electronics (GPU/HBM logic or memory). The SEU rate rises with
altitude and is largely un-shieldable, which makes it a binding cost of flying
higher rather than a mass problem.

**Hot-loop radiator** — a thermal architecture that runs coolant/radiator
surfaces hotter so the radiator can reject more heat per square meter.

**Optical comms / laser comms** — free-space optical links used for high-rate
space-to-space or space-to-ground communication.

**RF sliver** — a limited radio-frequency service path kept as backup or a
focused B2B channel, not the main data-center product.

**Inference** — serving a trained model. This is the compute workload the
project targets.

**Training** — building a model. It is far more communication-intensive and is
not the initial workload.

**Build-to-learn** — the staged approach where early nodes prove the hard
subsystems and market premium before a scaled buildout.
