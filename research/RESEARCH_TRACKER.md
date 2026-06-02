# Research Tracker

Research Wiki audit trail for the files under `research/`.

This tracker is intentionally research-only. It tracks every current file under
`research/` and does not track model-run summaries, promoted models, code
outputs, archived code reports, or current-state handoff files. Those artifacts
may be cited by research documents as historical inputs, but they are not
research files.

Status legend: `planned` · `in progress` · `draft` · `reviewed` · `stale`

## Scope Rules

Tracked here:

- Every file physically under `research/`, including navigation files, source
  research, synthesis/lint passes, adversarial debate, strategy notes, peer
  reviews, and the versioned thesis.
- Historical research artifacts that are superseded but still explain how the
  project learned.

Intentionally excluded:

- `data_center/conclusion.md` and any noncanonical model-run summary variants.
- `data_center/CURRENT_STATE.md`.
- `data_center/models/*.json`.
- `code/` and archived model reports under `code/archive/`.
- Root-level repository docs such as `README.md`.

## Research Navigation

| File | Status | Role | Audit note |
|---|---|---|---|
| [README.md](README.md) | reviewed | Research-wiki front door and navigation rules. | Added 2026-05-26 for Phase 1 source-status and public-claim contract. |
| [LIBRARY.md](LIBRARY.md) | reviewed | Catalog and glossary for the research corpus. | Rebuilt 2026-05-25 as a research-only catalog covering every file under `research/`. |
| [RESEARCH_TRACKER.md](RESEARCH_TRACKER.md) | reviewed | This audit trail and file coverage tracker. | Rebuilt 2026-05-25 to track every research file and only research files. |
| [SOURCE_INDEX.md](SOURCE_INDEX.md) | reviewed | Claim-level source ledger for hard numbers and scenario assumptions. | Added 2026-05-25 after focused source-agent audits; normalized 2026-05-26 to the public source-status taxonomy and `RLDC-*` claim IDs; expanded 2026-05-28 with per-input ground-reference statuses now used by the promoted ground JSON. |
| [vision/initial_thesis.md](vision/initial_thesis.md) | reviewed | Versioned thesis, append-only through Rev 7. | Rev 7 aligns the thesis with the new boundary: research is evidence; current conclusions and models live under `data_center/`. |
| [direct_communication/README.md](direct_communication/README.md) | draft | Front door for the communications workstream. | Navigation doc, not a sourced research memo. |

## Complete Research File Tracker

### Framing

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [README.md](README.md) | reviewed | Research-wiki front door. | Added 2026-05-26 to make the source base, claim ledger, tracker, and library relationship explicit. |
| [LIBRARY.md](LIBRARY.md) | reviewed | Catalog and glossary for the research corpus. | Research-only catalog; updated to include `SOURCE_INDEX.md`. |
| [RESEARCH_TRACKER.md](RESEARCH_TRACKER.md) | reviewed | Research Wiki tracker and file coverage audit. | Tracks every current file under `research/` and intentionally excludes generated outputs. |
| [SOURCE_INDEX.md](SOURCE_INDEX.md) | reviewed | Claim-level hard-number ledger. | Uses the public source-status taxonomy and records stable `RLDC-*` IDs for default assumptions and public model outputs. |
| [vision/initial_thesis.md](vision/initial_thesis.md) | reviewed | Append-only thesis and belief history. | Rev 7 preserves historical conclusion references as history while moving live outputs to `data_center/`. |
| [direct_communication/README.md](direct_communication/README.md) | draft | Communications workstream front door. | Navigation doc; no external source burden. |

### AI Hardware

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [ai_hardware/ai_hardware.md](ai_hardware/ai_hardware.md) | draft | Establishes NVIDIA rack-scale hardware, power, cooling, and networking baseline. | Source-status banner added 2026-05-25; GB300 mass/power and Rubin/CPX values are now qualified. |
| [ai_hardware/gpu_generational_roadmap.md](ai_hardware/gpu_generational_roadmap.md) | draft | GPU/package counts and power rise by generation; fixed-72 assumptions are not safe. | Source-status banner added 2026-05-25; Rubin Ultra/Feynman power now described as roadmap targets. |

### Competitors

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [competitors/starcloud.md](competitors/starcloud.md) | draft | Starcloud validates demand and sets the closest comparable orbital-DC competitor. | Has source section and external citations. |
| [competitors/starship_addendum.md](competitors/starship_addendum.md) | draft | Heavy-lift competition changes timing and scale, not the near-term Neutron learning case. | Has source section and external citations. |

### Debate

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [debate/README.md](debate/README.md) | reviewed | Rules for the bull/bear adversarial review. | Process doc; no external source burden. |
| [debate/bear_case.md](debate/bear_case.md) | stale | Bear case converges on bounded R&D, not immediate buildout. | Sourced, but economics are explicitly superseded by later launch-cost and service-life assumptions. |
| [debate/bull_case.md](debate/bull_case.md) | stale | Bull case preserves the build-to-learn argument. | Sourced, but economics are explicitly superseded by later launch-cost and service-life assumptions. |

### Economics

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [economics/ai_datacenter_tam.md](economics/ai_datacenter_tam.md) | draft | Sizes AI data-center demand and inference market context. | Source-status banner added 2026-05-25; analyst forecasts and illustrative TAM are explicitly labelled. |
| [economics/ambition_case.md](economics/ambition_case.md) | draft | Tests the ~$5B/yr go-for-it case; buildout is the constraint. | Source-status banner added 2026-05-25; inherited generated-model values are now labelled historical assumptions. |
| [economics/energy_operating_costs.md](economics/energy_operating_costs.md) | stale | Energy/water savings are real but second-order to launch and node capex. | Has sources; launch-share framing predates the internal-cost rebase. |
| [economics/ground_infrastructure_electricity_costs_2036.md](economics/ground_infrastructure_electricity_costs_2036.md) | draft | Audits the 2036 deployed-year ground infrastructure and five-year electricity basis behind the current ground reference. | Added 2026-05-28 from a focused research-wiki pass; reproduces the promoted JSON math, cites Epoch, EIA, Google, LBNL, JLL, Turner & Townsend, and utilization research, and documents the per-input source statuses now used by the promoted ground JSON. |
| [economics/gpu_cost_trajectory.md](economics/gpu_cost_trajectory.md) | draft | Replaces simple rack-price doubling with a GPU/package cost trajectory. | Source-status banner added 2026-05-25; rack-price estimates now carry source-date/conflict qualification. |
| [economics/gpu_hour_rental_rates.md](economics/gpu_hour_rental_rates.md) | draft | GPU-hour prices track acquisition cost more than performance. | Strong source density; key hard numbers appear well-supported. |
| [economics/hyperscaler_margins.md](economics/hyperscaler_margins.md) | draft | Margin pools at moat layers; orbital premium must be sold as a scarce attribute. | Has source section and external citations. |
| [economics/moonshot_150b.md](economics/moonshot_150b.md) | draft | $150B/yr is infeasible on Neutron; heavy lift is required. | Source-status banner added 2026-05-25; generated-model dependencies converted to historical assumptions. |
| [economics/moonshot_50b.md](economics/moonshot_50b.md) | draft | $50B/yr is infeasible on Neutron; Neutron ceiling is single-digit billions. | Source-status banner added 2026-05-25; generated-model dependencies converted to historical assumptions. |
| [economics/premium_value_case.md](economics/premium_value_case.md) | draft | Premium case rests on scarce capacity, sovereignty, zero water, and dedicated service. | Has source section and external citations. |
| [economics/rack_cost_trajectory.md](economics/rack_cost_trajectory.md) | stale | Early rack-cost trajectory; superseded by GPU/package cost trajectory. | Has sources and bannered staleness; keep as historical. |
| [economics/revenue_economics_2026.md](economics/revenue_economics_2026.md) | stale | Re-grounds current rack revenue layers. | Source-backed market data stands; calculator-critique sections are stale against cycle 2. |
| [economics/operating_margins_and_revenue_multiple_2026.md](economics/operating_margins_and_revenue_multiple_2026.md) | draft | Validates the 1.5x revenue multiple via the OPERATING-margin lens: orbital's near-zero opex makes its 33% over depreciation an operating-equivalent, matching hyperscaler cloud operating margins (33-45%) and far above compressed neocloud operating margins (~1%). Keeps gross/operating/net definitions; adds a depreciation-period section (our 5-year life vs operators' 6-year, so we do not flatter the margin). | Added 2026-05-30, revised same day. Multi-sourced (CoreWeave, Nebius, Oracle, AWS/Azure/GCP, NVIDIA; depreciation: Microsoft, Google, Oracle 8-K, Meta, Amazon 6->5 reversal); replaces the stale Oracle 30-40% figure; supports RLDC-REVENUE-MULTIPLE-1_5X / REV-008. |
| [economics/revenue_per_watt.md](economics/revenue_per_watt.md) | draft | Reconciles revenue per GW/rack and distinguishes IaaS vs inference service. | Source-status banner added 2026-05-25; derived IaaS and inference-service bands are distinguished. |

### Laser Communications

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [laser_comms/comms_business_case.md](laser_comms/comms_business_case.md) | draft | Direct communications can be a focused B2B/B2G line, not a Starlink clone. | Has source section; workstream spelling normalized to `direct_communication/` in the header. |
| [laser_comms/constellation_mesh.md](laser_comms/constellation_mesh.md) | draft | Laser range does not bind; ground reach and service architecture do. | Has source section and external citations. |
| [laser_comms/optical_comms.md](laser_comms/optical_comms.md) | draft | Optical is primary; terminal roadmap remains a gating risk. | Has source section and external citations. |
| [laser_comms/optical_ground_stations.md](laser_comms/optical_ground_stations.md) | draft | Geographic diversity beats one large ground station. | Has source section and external citations. |
| [laser_comms/rf_limited_service.md](laser_comms/rf_limited_service.md) | draft | A limited RF B2B backup/sliver may be attainable. | Has source section and external citations. |
| [laser_comms/rf_satcom.md](laser_comms/rf_satcom.md) | draft | RF is not the primary mass-market path for a new entrant. | Has source section and external citations. |

### LLM Compute

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [llm_compute/inference_scaling.md](llm_compute/inference_scaling.md) | draft | One NVL72-class rack can serve a frontier inference model; scaling is replica-heavy. | Has source section and external citations. |
| [llm_compute/minimum_viable_scale.md](llm_compute/minimum_viable_scale.md) | draft | Commercial service starts around a multi-node replica deployment. | Has source section and external citations. |
| [llm_compute/multi_rack_inference.md](llm_compute/multi_rack_inference.md) | draft | Laser-meshed satellites can support pipeline/expert/replica parallelism; tensor parallelism stays local. | Has source section and external citations. |

### Node Design

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [node_design/hot_chip_thermal_trajectory.md](node_design/hot_chip_thermal_trajectory.md) | draft | Hot-loop operation is the main mass lever, with reliability tradeoffs. | Source-status banner added 2026-05-25; radiator/flyability numbers are model-derived. |
| [node_design/node_mass_model.md](node_design/node_mass_model.md) | draft | One-rack node is mass-tight but feasible; two-rack Neutron node is not baseline. | Source-status banner added 2026-05-25; GB300 mass and derived solar/radiator values are qualified. |
| [node_design/rack_internals.md](node_design/rack_internals.md) | draft | Compute trays dominate mass; cabling is second-order. | Has source section and external citations. |
| [node_design/rack_splitting.md](node_design/rack_splitting.md) | draft | Smaller self-integrated inference nodes are plausible later. | Has source section and external citations. |
| [node_design/reliability_failure_handling.md](node_design/reliability_failure_handling.md) | draft | GPU attrition and coolant-loop reliability drive graceful-degradation architecture. | Source-status banner added 2026-05-25; AFR, service life, and burn-in claims are now qualified. |
| [node_design/self_built_rack.md](node_design/self_built_rack.md) | draft | Rocket Lab should integrate the spacecraft/power/thermal shell, not become a server OEM. | Has source section and external citations. |
| [node_design/solar_radiator_trajectory.md](node_design/solar_radiator_trajectory.md) | draft | Solar/radiator scaling is a mass wall before it is a cost wall. | Source-status banner added 2026-05-25; solar/radiator values remain model-derived. |
| [node_design/space_solar_costdown_2030_2036.md](node_design/space_solar_costdown_2030_2036.md) | draft | Tests whether solar can fall from `$40k/kW` to `$20k/kW` by 2030-2036 for Rocket Lab silicon orbital data-center arrays. | Public sources support `$20k/kW` as a scenario sensitivity, not a certified default; Rocket Lab has not published integrated array $/W, W/kg, W/m2, or EOL degradation. |
| [node_design/radiator_costdown_2030_2036.md](node_design/radiator_costdown_2030_2036.md) | draft | Tests whether radiator cost/mass can fall enough by 2030-2036 to narrow the orbital premium. | Physics and mass ranges are source-supported; `$ / kW` remains scenario-only pending vendor quote or bottom-up BOM. |
| [node_design/gpu_temperature_cooling_limits.md](node_design/gpu_temperature_cooling_limits.md) | draft | Clarifies GPU junction/coolant/radiator temperature definitions and tests whether hotter operation can reduce orbital radiator mass/cost by 2030. | Public evidence supports warmer liquid-cooling loops and T^4 radiator leverage; exact future GPU junction limits and chip-to-radiator thermal resistance remain unresolved. |
| [node_design/gpu_hotter_operation_reliability_2030_2036.md](node_design/gpu_hotter_operation_reliability_2030_2036.md) | draft | Tests whether future AI GPU/HBM packages can safely run `10-20 deg C` hotter for sustained orbital service and what that would mean for radiator sizing. | Public sources support warmer liquid cooling and HBM thermal-resistance improvements; exact future GPU/HBM sustained junction limits are not public, and `+20 deg C` hotter junction operation should be a stress sensitivity, not a default. |
| [node_design/electric_propulsion_stationkeeping_5v7yr.md](node_design/electric_propulsion_stationkeeping_5v7yr.md) | draft | Sizes electric-propulsion station-keeping mass for 5 vs 7 years at low SSO: ~150 kg (5 yr) to ~184 kg (7 yr) for an 8 t node, inside the existing 250 to 550 kg propulsion line, with only ~25 to 35 kg marginal 5-to-7-year cost. | Added 2026-05-29 from the exploratory orbital-lifetime study; propellant/mass figures are derived estimates pending a node-specific propulsion design. |

### Orbital

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [orbital/orbit_types_primer.md](orbital/orbit_types_primer.md) | reviewed | Primer for orbit types, relays, satellites, and launch. | Has source section; reference doc. |
| [orbital/orbits_environment.md](orbital/orbits_environment.md) | draft | Dawn-dusk SSO reduces eclipse and keeps radiation manageable. | Has source section and external citations. |
| [orbital/thermal_analysis.md](orbital/thermal_analysis.md) | stale | Early thermal sizing; later mass-model/lint work supersedes radiator-area numbers. | Source-status banner added 2026-05-25; historical sizing remains superseded. |
| [orbital/leo_lifetime_large_node_5v7yr.md](orbital/leo_lifetime_large_node_5v7yr.md) | draft | LEO natural lifetime vs altitude for a large high-drag node: a very low ballistic coefficient decays it 6 to 13x faster, so 500 to 600 km lasts only ~1.3 to 5 yr (~0.4 to 2 yr through solar max); a 5-yr natural life needs ~700 km and 7 yr needs ~720 to 750 km. | Added 2026-05-29 from the exploratory orbital-lifetime study; lifetime figures are first-order estimates pending a numerical orbit propagation. |
| [orbital/higher_orbit_tradeoffs_lifetime.md](orbital/higher_orbit_tradeoffs_lifetime.md) | draft | Higher-orbit tradeoffs for a 7-year natural life: delta-v is not binding (~160 m/s to 800 km); radiation (rising TID and an un-shieldable GPU/HBM SEU rate) is binding, and above ~600 to 650 km a mandatory active deorbit system is required; 7-yr natural life put at ~800 to 900 km. | Added 2026-05-29 from the exploratory orbital-lifetime study; radiation and altitude bands are estimates pending a SPENVIS/CREME96 run. |

### Peer Review

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [peer_review/README.md](peer_review/README.md) | reviewed | Describes the peer-review pass. | Process doc; no external source burden. |
| [peer_review/consistency_review.md](peer_review/consistency_review.md) | stale | Cross-file consistency review of an older data-center/conclusion shape. | Historical-layout banner added 2026-05-25; retained as history, not current navigation. |
| [peer_review/peer_review_1.md](peer_review/peer_review_1.md) | reviewed | First independent research-corpus audit. | Review artifact; mostly cites project docs rather than external sources. |
| [peer_review/peer_review_2.md](peer_review/peer_review_2.md) | reviewed | Second independent research-corpus audit. | Review artifact; mostly cites project docs rather than external sources. |
| [peer_review/peer_review_3.md](peer_review/peer_review_3.md) | reviewed | Third independent research-corpus audit. | Review artifact; mostly cites project docs rather than external sources. |
| [peer_review/peer_review_4.md](peer_review/peer_review_4.md) | stale | End-document peer review focused on the old root conclusion. | Useful as history; conclusion target has moved. |
| [peer_review/review_economist.md](peer_review/review_economist.md) | reviewed | Independent economic review of the superseded M5 model. | Review artifact; hard numbers are derived from model/doc references. |
| [peer_review/review_engineer.md](peer_review/review_engineer.md) | reviewed | Independent engineering review of the superseded M5 model. | Review artifact; hard numbers are derived from model/doc references. |
| [peer_review/structural_review.md](peer_review/structural_review.md) | stale | Structural walkability review of a prior repo layout. | Historical-layout banner added 2026-05-25; old path references are retained as review history. |
| [peer_review/triage_and_fix_plan.md](peer_review/triage_and_fix_plan.md) | stale | Fix plan from older peer-review cycle. | Historical maintenance plan; several targets have since moved or been removed. |

### Rocket Lab

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [rocket_lab/electron/electron_specs.md](rocket_lab/electron/electron_specs.md) | reviewed | Electron specs and role as context/possible relay launcher. | Has source section and external citations. |
| [rocket_lab/neutron/launch_cost_economics.md](rocket_lab/neutron/launch_cost_economics.md) | draft | Internal launch-cost estimate for Rocket Lab flying its own payloads. | Source-status banner added 2026-05-25; cadence-specific internal cost is an estimate. |
| [rocket_lab/neutron/neutron_specs.md](rocket_lab/neutron/neutron_specs.md) | draft | Neutron specs and published payload/fairing facts. | Source-status banner added 2026-05-25; LEO/polar values vs SSO estimates are separated. |
| [rocket_lab/neutron/payload_and_block_upgrade.md](rocket_lab/neutron/payload_and_block_upgrade.md) | draft | Re-baselines SSO payload estimate and block-upgrade envelope. | Source-status banner added 2026-05-25; SSO/block-upgrade figures remain estimates/scenarios. |
| [rocket_lab/neutron/neutron_payload_vs_orbit.md](rocket_lab/neutron/neutron_payload_vs_orbit.md) | draft | Neutron payload vs orbit: ~13 t reusable to LEO, a ~25 to 30% LEO-to-SSO penalty (~9.5 t to SSO), and cheap higher SSO (~5% to 700 to 800 km); refutes "halve the payload" and treats 12.5 t as expendable/block-upgrade, not baseline reusable. | Added 2026-05-29 from the exploratory orbital-lifetime study; payload-vs-orbit figures are estimates consistent with the existing deep Neutron docs. |
| [rocket_lab/neutron/sso_recovery_cadence_falcon_analogue.md](rocket_lab/neutron/sso_recovery_cadence_falcon_analogue.md) | draft | SSO recovery via the Falcon analogue: SSO does not force expendable (Falcon recovers boosters on SSO/polar; Neutron RTLS-primary at Wallops), so the ~25 to 30% SSO penalty stands with no expendable surcharge; RTLS suits high cadence. | Added 2026-05-29; Falcon-analogue evidence solid, Neutron RTLS-primary stated. Top open question: the Wallops SSO launch azimuth (possible dogleg) is undocumented and would add to the penalty. |
| [rocket_lab/neutron/sso_from_virginia_feasibility.md](rocket_lab/neutron/sso_from_virginia_feasibility.md) | draft | SSO from Virginia (Wallops LC-3): probable-yes-with-a-dogleg, not a guarantee. Pad confirmed (ribbon-cut Aug 2025); SSO (~98) is outside the 38 to 60 degree corridor and needs a southerly-Atlantic dogleg (PUG and VSA say reachable; Falcon SAOCOM 1B precedent). | Added 2026-05-29. Caveats: no orbital SSO ever flown from Wallops (stated-but-unflown); dogleg adds an estimated ~5 to 15% payload on top of the ~25 to 30% SSO penalty. Confirm with Rocket Lab: a Wallops-specific SSO performance curve. |
| [rocket_lab/neutron/sso_us_launch_site_options.md](rocket_lab/neutron/sso_us_launch_site_options.md) | draft | Best US SSO launch site: Wallops is good enough to start (only built Neutron pad) but not SSO-optimal (dogleg ~5 to 15% penalty, droneship-biased recovery); Vandenberg/West Coast is the performance-optimal relocation (direct south, no dogleg, RTLS), though Rocket Lab has no public West Coast Neutron plan. Corrects "south toward the equator" (backwards for SSO; an unobstructed retrograde azimuth over open ocean is what matters). | Added 2026-05-30. Treats Wallops as the start assumption and relocation as the likely future move; no precise payload math (single-digit-percent reasoning only). Open: Rocket Lab has not announced a West Coast Neutron pad. |
| [rocket_lab/overview.md](rocket_lab/overview.md) | draft | Rocket Lab company overview and vertical integration. | Has source section and external citations. |
| [rocket_lab/space_hardware_capabilities.md](rocket_lab/space_hardware_capabilities.md) | draft | Rocket Lab has much of the stack; deployable radiators remain the gap. | Has source section and external citations. |
| [rocket_lab/vertical_integration_stack_2026.md](rocket_lab/vertical_integration_stack_2026.md) | draft | What Rocket Lab builds in-house vs buys across the satellite-bus stack, with acquisition statuses and the in-house electric propulsion (Gauss); margin-capture implication for a node. | Added 2026-06-01. 2+ sources per hard claim, CLOSED/PENDING stated per deal; margin capture kept qualitative (no invented percentage). |
| [rocket_lab/manufacturing_capability_2026.md](rocket_lab/manufacturing_capability_2026.md) | draft | Rocket Lab's demonstrated manufacturing competency (Rutherford additive, Rosie composites, Neutron AFP, Flatellite) and its transfer to node production. | Added 2026-06-01. Sourced; explicit boundaries (no node built, Neutron-class line installed but not flight-proven, node costs unproven). |

### Strategy

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [strategy/README.md](strategy/README.md) | reviewed | Rules for the Engineer/CFO strategy loop. | Process doc; no external source burden. |
| [strategy/optimized_strategy.md](strategy/optimized_strategy.md) | stale | Historical converged strategy loop. | Root-conclusion links were converted to historical plain-text citations on 2026-05-25; strategy remains historical. |
| [strategy/self_launch_cadence_and_manufacturing_advantage_2026.md](strategy/self_launch_cadence_and_manufacturing_advantage_2026.md) | draft | Self-launch as a supply guarantee, fixed-cost amortization, the manufacturing learning curve, and the production-line-vs-ground-megaproject contrast. | Added 2026-06-01. Cadence/fixed-cost faithfully sourced to launch_cost_economics.md; learning-rate figures tagged as external analogues with the honest "not guaranteed" caveat. |

### Synthesis

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [synthesis/lint_report.md](synthesis/lint_report.md) | stale | First wiki-health lint pass. | Superseded snapshot; cites project docs rather than external sources. |
| [synthesis/lint_report_2.md](synthesis/lint_report_2.md) | stale | Second wiki-health lint pass after wave 5. | Superseded snapshot; cites project docs rather than external sources. |
| [synthesis/preliminary_findings.md](synthesis/preliminary_findings.md) | stale | Wave-1 synthesis; no physics wall, but numbers later changed. | Superseded snapshot; hard numbers need source-doc trace rather than standalone sourcing. |
| [synthesis/wave4_synthesis.md](synthesis/wave4_synthesis.md) | stale | Wave-4 economics synthesis; baseline-Neutron payback problem. | Superseded launch-cost/service-life basis. |
| [synthesis/wave5_synthesis.md](synthesis/wave5_synthesis.md) | stale | Latest full research synthesis in `research/`, resolving flyability crossover. | Physics/flyability findings stand, but launch-cost basis is superseded. |
| [synthesis/orbital_lifetime_5v7yr_synthesis.md](synthesis/orbital_lifetime_5v7yr_synthesis.md) | draft | Synthesizes the 5-vs-7-year orbital-lifetime study: longevity costs single-digit percent on every lever; 5 years is conditional on ~700 km or propulsion while 7 years is cheap either way; the real trade is radiation plus mandatory deorbit (fly high) vs continuous station-keeping (stay low); design life is likely revenue-limited, not orbit-limited. | Added 2026-05-29 as the synthesis of the exploratory orbital-lifetime study; the 7-yr natural-life band (~720 to 900 km) is unresolved pending a numerical propagation and radiation run. |

### Valuation

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [valuation/ai_compute_trajectory.md](valuation/ai_compute_trajectory.md) | draft | Compute trajectory over the model horizon. | Has source section; still references old conclusion/code companions. |
| [valuation/projection_2026_2036.md](valuation/projection_2026_2036.md) | stale | Projection narrative for an older calculator path/default. | Historical-path banner added 2026-05-25; retained as research history, not the current run contract. |
| [valuation/rklb_baseline_financials.md](valuation/rklb_baseline_financials.md) | draft | Rocket Lab reported financial baseline. | Has source section and primary/filing citations. |
| [valuation/rklb_forward_trajectory.md](valuation/rklb_forward_trajectory.md) | draft | Rocket Lab forward consensus and Neutron economics context. | Source-status banner added 2026-05-25; price, cost, cadence, and SSO claims now point to `SOURCE_INDEX.md`. |
| [valuation/trajectory_notes.md](valuation/trajectory_notes.md) | draft | Working notes from trajectory critique and model directives. | Scratchpad, not a finished sourced research memo. |

## Key Findings

- The research thesis is not that conclusions live in `research/`. Research is
  the evidence base. Conclusions are synthesized outputs generated or maintained
  outside this folder.
- Neutron-class orbital AI inference is not blocked by a known physics wall in
  the research corpus; the central constraints are mass to SSO, thermal
  rejection, launch cadence, service life, and willingness-to-pay.
- Dawn-dusk SSO, a hot-loop radiator, and one node per launch are the current
  physical architecture backbone.
- The current language should distinguish NVIDIA hardware "racks" from the
  project product unit "node". Older research still uses rack-as-product
  language as historical terminology.
- The latest full research synthesis inside `research/` is
  [synthesis/wave5_synthesis.md](synthesis/wave5_synthesis.md), but it is still
  stale on launch-cost framing.
- The versioned thesis has an append-only history through Rev 7, including the
  2026-05-25 boundary alignment for model-run summaries and model outputs.
- The peer-review folder is valuable as a historical QA record, not as the
  current live repo map.
- `research/LIBRARY.md` now mirrors this tracker’s research-only boundary.
- Exploratory orbital-lifetime study (2026-05-29), not a model change: a 5-year
  natural life is conditional, not free, at low SSO. The node's large deployed
  area gives a very low ballistic coefficient, so it needs ~700 km of altitude
  or continuous electric-propulsion station-keeping to reach 5 years.
- Exploratory orbital-lifetime study (2026-05-29): extending from 5 to 7 years
  is single-digit-percent cheap on both paths. Station-keeping adds only ~25 to
  35 kg (about 0.4% of an 8 t node), and the natural-life path costs only modest
  extra altitude.
- Exploratory orbital-lifetime study (2026-05-29): the binding cost of flying
  higher is radiation, not mass. Delta-v stays small (~160 m/s to 800 km), but
  rising TID and an un-shieldable GPU/HBM single-event-upset rate, plus a
  mandatory active deorbit system above ~600 to 650 km, are what constrain
  altitude.
- Exploratory orbital-lifetime study (2026-05-29): Neutron's LEO-to-SSO payload
  penalty is ~25 to 30% (~13 t LEO to ~9.5 t SSO), matching the deep Neutron
  docs and refuting the 10 to 20% headline; higher SSO is cheap (~5% to 700 to
  800 km). The node's design life is therefore likely revenue-limited (aging
  silicon), not orbit-limited.

## Stakeholder Input Trail

Founder/stakeholder input is present throughout the research history. This
tracker preserves the audit trail at the wave level; the detailed arguments are
in the linked docs and prior versioned artifacts.

| Wave / cycle | Input captured | Where it landed |
|---|---|---|
| Pre-synthesis | Whole racks as the Starcloud differentiator; build-to-learn as product; possible compute/networking rack roles; hubs-not-homes ground link framing. | Early thesis and wave-1 research docs. |
| Wave 3 | Limited RF sliver; orbit primer; standard rack geometry; fairing modification tolerance; radiator/solar co-mounting hypothesis. | `laser_comms/`, `orbital/`, `node_design/`. |
| Wave 4 | Multi-generation build-to-learn framing and a simple rack-cost to revenue gut-check chain. | `synthesis/wave4_synthesis.md`, economics workstream. |
| Wave 5 | Rack cost trajectory, block-upgrade possibilities, rack internals, solar/radiator mass-vs-volume, and energy/water cost questions. | `economics/`, `node_design/`, `synthesis/wave5_synthesis.md`. |
| Wave 6 | Neutron cadence as a distribution advantage; possible orbital inference-routing optimization. | Backlog and constellation/strategy docs. |
| Wave 7 | Electron-launched relay concept; Neutron reusability economics; 5-year service-life assumption; premium sweep. | Reliability, debate, economics, and thesis revisions. |
| Wave 8 | 5-year life as base case, 2-3 years as downside; debate re-run framing; revenue/cost derivation. | Debate and economics docs. |
| Wave 9 | Internal marginal launch cost instead of customer price; investor trajectory request; no separate CPU rack needed. | Launch-cost, valuation, and model workstreams. |
| Wave 10 | V1 as a premium-premium product; minimum viable deployment scale; peer-review QA mechanism. | `llm_compute/minimum_viable_scale.md`, `peer_review/`. |
| Wave 11 | Radiator ownership preference; conservative plus ambition cases; buildout-limited framing. | `economics/ambition_case.md`, thesis Rev 5/6. |
| Wave 12 | Valuation workstream grounded in reported financials; M5 superseded; labelled dials; 15-year view; economist/engineer review process. | `valuation/`, `peer_review/review_*`. |
| GPU-grounding cycle | Model GPU packages and kW, not racks; question fixed 72; expensive silicon helps space; count GPUs as sold; R-band revenue framing. | `ai_hardware/gpu_generational_roadmap.md`, `economics/gpu_cost_trajectory.md`, `economics/gpu_hour_rental_rates.md`, calculator docs outside `research/`. |

## Open Questions And Backlog

Highest-priority research gaps:

- Rocket Lab’s true reusable SSO payload and usable fairing volume.
- The true internal marginal Neutron launch cost at scale.
- Customer willingness-to-pay for orbital inference and the real premium band.
- Deployable radiator cost, supplier availability, ownership path, and
  hot-loop reliability.
- Chip-to-coolant-to-panel thermal resistance model to narrow radiator mass.
- Coolant-loop and CDU reliability in an unserviceable 5-year mission.
- Mynaric 100 Gbps-class terminal timeline, mass, power, and procurement risk.
- Optical ground-network cost and availability model.
- Specific RF filing/band/link-budget path for the limited RF service.
- R-band and radiator-cost dials used by the current calculator.
- Ground-side cost refinement for a 2036 equivalent cohort: split rack-side
  power/networking, cooling, and operations/support scopes so the model avoids
  double counting while preserving the current conservative comparison.
- Solar/radiator cost uncertainty. Prior work suggested `$40,000/kW` may be
  high and `$20,000/kW` may be plausible, but this remains unresolved until
  sourced.
- GPU definition drift. Future model and public docs must clarify whether
  "GPU" means die, package, accelerator module, rack-scale GPU, or another
  unit; the current default ledger uses GPU package.
- AI data-center capacity projection around 2036. Keep the `~100 GW`
  comparison as a scale sanity check only, sourced through `RLDC-MARKET-100GW-2036`.
- Exploratory orbital-lifetime study (2026-05-29): the 7-year natural-life
  altitude band (~720 to 900 km) differs between the two lifetime docs
  (`orbital/leo_lifetime_large_node_5v7yr.md` puts it at ~720 to 750 km,
  `orbital/higher_orbit_tradeoffs_lifetime.md` at ~800 to 900 km) because of
  differing drag-area assumptions. Resolving it needs a numerical orbit
  propagation plus a radiation (SPENVIS/CREME96) run.

Tracker hygiene backlog:

- Continue the claim-level hard-number source audit beyond the high-risk
  Neutron/GPU/revenue/thermal claims covered in `SOURCE_INDEX.md`.
- Continue adding historical-layout banners when old peer-review or synthesis
  docs are touched.
- Refresh or retire historical calculator/projection narratives when the current
  `code/` generator contract changes again.

## Research Wiki Compliance Snapshot

Current verdict: structurally compliant after the tracker/library rebuild,
source-ledger addition, targeted stale-path cleanup, and ground-reference JSON
handoff. The current release-critical ground reference has source-status
coverage and per-input claim IDs.

Compliant or improved:

- Every current file under `research/` is now tracked.
- The tracker no longer treats code outputs, promoted models, model-run
  summaries, or current-state handoffs as research files.
- Synthesis, lint, debate, and peer-review docs are classified as historical
  research artifacts rather than current conclusions.
- Known stale documents are marked as stale instead of silently presenting them
  as current.
- `research/LIBRARY.md` now catalogs every current file under `research/` and
  excludes generated outputs and code artifacts.
- `research/SOURCE_INDEX.md` now provides a claim-level hard-number ledger for
  the highest-risk Neutron, GPU, revenue, thermal, default-assumption, and
  public-output claims, including per-input ground-reference statuses.
- High-risk primary docs now carry source-status banners pointing back to the
  ledger.
- The thesis has an appended Rev 7 boundary note.
- Broken root-conclusion markdown links in `strategy/optimized_strategy.md`
  were removed without rewriting the historical strategy.

Continuing maintenance:

- Older synthesis, debate, and peer-review documents remain historical research
  artifacts. When one is promoted into a current public claim, route it through
  `SOURCE_INDEX.md` and cite the original external sources.
- Append-only historical documents still mention retired conclusion artifacts
  and old repo paths as part of their audit history. The current tracker/library
  no longer treats those retired artifacts as research files or live navigation.
