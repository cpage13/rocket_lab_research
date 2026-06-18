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
| [vision/comms_thesis.md](vision/comms_thesis.md) | draft | Communications thesis: starting belief record for the comms track (four working hypotheses plus the open questions that test them); no verdict for or against a Rocket Lab space-comms business. | Added 2026-06-11, comms wave-1 ingest. Revision 2 appended (2026-06-11): the two missing dollar numbers are now sized (rural/remote fringe and premium/sovereign niche), updating the confirm/break notes for Hypotheses 2 and 4; Revision 1 unchanged, still no verdict, the sizes are demand-side and ILLUSTRATIVE. Revision 3 appended (2026-06-17): the cost side now has a test (the ground-vs-space cost ratio and the incumbent marginal-cost floor); updates Hypothesis 2's confirm/break notes (supply economics close for *scaled* space in the fringe and do not close in served markets; the gate narrows to whether a specific entrant at realistic scale reaches the cost level), leaving Hypotheses 1, 3, 4 unchanged; still no verdict, the entrant-specific cost stack is unmodeled. Belief record only; carries no external source burden of its own, pointing to `synthesis/comms_baseline_synthesis.md`, the three wave-2 `economics/comms_*_sizing.md` docs, and the three wave-3 `economics/comms_*` cost docs for the sourced base. |
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
| [competitors/starship_addendum.md](competitors/starship_addendum.md) | draft | Heavy-lift competition changes timing and scale, not the near-term Neutron learning case. | Has source section and external citations. Updated 2026-06-09 with a dated section on the SpaceX AI-1 design reveal (confirmed/derived/press tagging); the Musk timing hedge is now marked historical, and the dedicated AI-1 analysis has landed as `data_center/ai1_comparison.md` (2026-06-10). |
| [competitors/falcon9_cadence_ramp.md](competitors/falcon9_cadence_ramp.md) | draft | Falcon 9 cadence took ~14 years to reach 165/yr and bent up only once booster reuse was routine and Starlink filled the manifest; Starship must rerun a harder (upper-stage reuse) curve, so "at least about 5 years" to significant orbital data centers beats "about 3 years," with communications the credible near-term Starship payload. | Added 2026-06-11, comms wave-1 ingest, multi-source, estimates flagged. Historical cadence is counted public fact (Wikipedia/ElonX/Data Explained); forward Starship inference is a reasoned projection consistent with `starship_addendum.md` (2028-2031 window, Starbase 25-launch cap). Builds on starship_addendum, launch_cost_economics, review_engineer. |

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
| [economics/comms_us_broadband_market.md](economics/comms_us_broadband_market.md) | draft | US fixed broadband is ~$70-95B/yr; the biggest broadband subscriber bases carry the smallest market caps; willingness-to-pay for speed is sharply concave (~$2.34/Mbps to ~$0.02/Mbps), so value rewards reach and reliability, not raw bandwidth. | Added 2026-06-11, comms wave-1 ingest, multi-source, estimates flagged. Carrier financials from 2025-26 SEC filings; total-market revenue and Cox/AT&T-FWA figures flagged single-source. |
| [economics/comms_us_cellular_market.md](economics/comms_us_cellular_market.md) | draft | US wireless service revenue ~$326B/yr (single major source); cable MVNOs prove a non-carrier can run 20M+ lines on rented capacity, the wholesale logic behind carrier-hosted direct-to-cell. | Added 2026-06-11, comms wave-1 ingest, multi-source, estimates flagged. Carrier financials double-sourced; the ~$326B headline and the MVNO sizing are flagged single-source/methodology-dependent. |
| [economics/comms_global_regional_market.md](economics/comms_global_regional_market.md) | draft | Global telecom services ~$2.0-2.1T/yr (mobile ~$1.19T, fixed broadband ~$360-390B); satellite ~0.5% of fixed broadband; the GSMA $7.6T is GDP contribution, not operator revenue. | Added 2026-06-11, comms wave-1 ingest, multi-source, estimates flagged. Mobile/subscriptions/satellite-share are primary-body; regional dollar splits and the ex-China Asia figure are softer than the shares. |
| [economics/comms_cellular_5g_deployment_economics.md](economics/comms_cellular_5g_deployment_economics.md) | draft | Mobile-network capex is ~14-19% of service revenue and declining; site upgrade ~$20-50K vs new macro ~$100-300K; C-band auction ~$81B; ~8-10 year payback and no 5G ARPU premium. | Added 2026-06-11, comms wave-1 ingest, multi-source, estimates flagged. Capex intensity and auction totals well-corroborated; per-component cost splits and the 8-10 year payback are aggregator/single-source. |
| [economics/comms_broadband_deployment_economics.md](economics/comms_broadband_deployment_economics.md) | draft | A cable incumbent defends a passed home for ~$100-300 vs ~$1,000+ fiber overbuild; the space value is in the unserved/remote tail ($3,000-6,000 rural up to ~$200,000+), not served markets. | Added 2026-06-11, comms wave-1 ingest, multi-source, estimates flagged. Per-foot/cable-upgrade/FWA/take-rate are multi-source; the ~$200K extreme-rural passing and ~4% overbuild ROI rest on single primary sources. |
| [economics/comms_space_tam_claims.md](economics/comms_space_tam_claims.md) | draft | Cited connectivity TAMs (SpaceX $1.6T, AST ~$1.1T) and the bottoms-up served market are ~2 orders of magnitude apart; Morningstar realistic Starlink ~$129B; default prior is a ~90% haircut (served ~5-10% of cited). | Added 2026-06-11, comms wave-1 ingest, multi-source, estimates flagged. Cited figures are primary filings; the ~90% haircut is corroborated by four analysts; the $15.4B ASTS model and $200B combined-bank figure are flagged single-source. |
| [economics/comms_rural_fringe_sizing.md](economics/comms_rural_fringe_sizing.md) | draft | Sizes the satellite-addressable rural/remote fringe at ~$40-55B/yr conservative to ~$95-130B/yr optimistic (ex-China), ~2.5-8% of the cited $1.6T and bracketing Morningstar's ~$129B; the dollars are in the developed-world rural fringe and high-ARPU mobility/enterprise verticals, NOT in the ~3.1B-person usage gap. | Added 2026-06-11, wave-2 sizing, multi-source, illustrative flagged. Bottoms-up on sourced household counts and region-specific ARPU; the dollar cases are explicitly ILLUSTRATIVE and the value is the structure plus the four-anchor cross-checked band (Starlink $11.39B revenue, Morningstar ~$129B, Quilty 25-30M cap, Oxford 78M-421M users). Single-source flags: the ~$2,000/yr residential ARPU, the Value Add VC developed-vs-emerging split, the Quilty cap, the Oxford range, and the Morningstar ~$10B US-Niche sub-figure. Carries internal COMM-057..081, reconciled into SOURCE_INDEX by the lead. |
| [economics/comms_premium_sovereign_sizing.md](economics/comms_premium_sovereign_sizing.md) | draft | Sizes the premium/sovereign niche at a ~$75-95B/yr gross pool but only ~$8-30B/yr OPEN to a new commercial entrant (ex-China); the flagship programs (IRIS2 EUR 10.6B, SDA tranches, $2.29B SpaceX SDN, GOVSATCOM) are closed prime/consortium builds, demand proof not addressable revenue. | Added 2026-06-11, wave-2 sizing, multi-source, illustrative flagged. The ~$50B government+military envelope is the load-bearing total (2-firm corroboration within ~4%); the served open slice is a reasoned haircut, not a bid model, flagged ILLUSTRATIVE. Single-source/scope flags: the enterprise-satcom umbrella, the finance/low-latency attributable spend (dated TABB 2010), the open-government annual-outlay estimate (ceiling-vs-outlay trap), and orbital-DC backhaul (assumption-set fraction). Rocket Lab's >$1.3B SDA prime position recorded as context, not scored. Carries internal COMM-057..078 (collides with the rural doc), reconciled by the lead. |
| [economics/comms_addressable_sizing.md](economics/comms_addressable_sizing.md) | draft | Consolidation: the de-duplicated new-entrant-addressable pool is ~$45-60B/yr conservative to ~$110-150B/yr optimistic (ex-China), ~3-9% of the cited $1.6T and in the same band as the ~$129B realistic served estimate; the two pools share the mobility/enterprise verticals and are reconciled (five non-overlapping buckets), not summed. | Added 2026-06-11, wave-2 sizing, multi-source, illustrative flagged. Reconciles the two sizing docs against the $1.6T and $129B anchors; the consolidated band inherits both inputs' ILLUSTRATIVE status plus a reasoned (not modeled) overlap de-duplication. Load-bearing cross-check: two independent methods (this bottoms-up consolidation and Morningstar's top-down rebuild) landing in the same band. No verdict, no supply-side economics, no single-operator capture rate. Carries internal COMM-082..090, remapped into the continuous global sequence by the lead. |
| [economics/comms_space_supply_cost.md](economics/comms_space_supply_cost.md) | draft | The space supply-side cost stack to deliver communications, from the disclosed Starlink S-1: mature incumbent ~$480-680/sub/yr all-in (~$200-260 space-specific) at ~38.6% segment op / ~63% segment EBITDA on $11.4B revenue; ~$0.05-0.30/GB network-average but rising with user density; dominated by the satellite fleet on a 5-year replacement treadmill (~$6-8B/yr), then launch, then a small availability-critical optical ground segment; scale is the whole game. | Added 2026-06-17, wave-3 cost stack, multi-source, derived ranges. Segment financials are audited S-1, cross-checked across three readers; the per-satellite unit costs are third-party estimates (V2 mini carries a ~2x source disagreement). Single-source/soft flags: the ~$6-8B/yr replacement capex and ~1,000 sats/yr rate (one 2024 Motley Fool lineage, arithmetically low against a ~10,000-sat fleet), the reconstructed ~$15-25B cumulative capex, and the utilization-dependent per-GB number. Carries internal COMM-080..108, reconciled into SOURCE_INDEX (global COMM-080..092) by the lead. |
| [economics/comms_incumbent_margins_competitive_floor.md](economics/comms_incumbent_margins_competitive_floor.md) | draft | Ground incumbents' margins and the marginal-cost defend floor a space entrant must beat in served markets: US carriers/cable run ~36-41% EBITDA and ~80-90% broadband gross margins, so the served-market defend floor is the incumbent's marginal cash cost (~10-20% of ARPU, ~$7-15/mo, ~$84-180/sub/yr fixed; ~$0.50-1.50/GB mobile), not the list price, with ~30-40 points of EBITDA headroom to cut; no such floor exists in the unserved fringe, which is why the dollars sit there. | Added 2026-06-17, wave-3 cost ratio, multi-source, derived ranges. EBITDA margins are computed from each company's own FY2025 release and cross-checked. Single-source/soft flags: the ~80-90% broadband gross margin is triangulated across four press/operator outlets (some pre-2015), not one audited decomposition; the mobile ~$0.50-1.50/GB delivery cost is single-source (cross-checked only against MVNO wholesale logic). The asymmetry-vs-1.92x and the per-sub floors are interpretation grounded in the sourced margins. Carries internal COMM-080..103 (with gaps; collides with the supply-cost doc), reconciled into SOURCE_INDEX (global COMM-093..099) by the lead. |
| [economics/comms_ground_vs_space_cost_ratio.md](economics/comms_ground_vs_space_cost_ratio.md) | draft | The headline ground-vs-space delivery-cost ratio: TWO opposed ratios split by whether ground plant exists (the two-flavor asymmetry). Flavor (a) space vs a fresh ground build (unserved): space CHEAPER ~1.3-3.2x rural to ~65-90x tail (opposite the data-center 1.92x). Flavor (b) space vs incumbent marginal (served): space COSTLIER ~3-8x. The ~$480-680/sub/yr level that earns the addressable pool is Starlink's disclosed actual, scale-dependent and unreachable for a small constellation. Space wins on cost exactly where the wave-2 demand sits. | Added 2026-06-17, wave-3 cost ratio, multi-source, derived ranges. The wave-3 CONSOLIDATION doc: no new cost build, it puts the space numerator and ground stacks on a common per-sub/yr basis. The asymmetry (the headline) is medium-high and corroborated by 2025-26 BEAD procurement choosing satellite in the high-cost tail; the point ratios are medium (arithmetic on sourced ranges, flavor (a) annualized at a stated ~25-yr fiber life / ~9% capital charge that is conservative against space). The realistic-for-SpaceX fact is high; the small-constellation scale caveat is carried from the supply-cost doc. No business verdict; the entrant-specific (non-Starlink) cost stack is unmodeled. Carries internal COMM-109..117, reconciled into SOURCE_INDEX (global COMM-100..103) by the lead. |

### Direct Communication

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [direct_communication/spectrum_fundamentals_economics.md](direct_communication/spectrum_fundamentals_economics.md) | draft | Mid-band is the contested sweet spot; US C-band ~$0.94/MHz-POP (~$81B) vs mmWave hundreds of times cheaper; terrestrial cellular spectrum is effectively closed to a new entrant, so the spectrum fight belongs in the satellite domain (ITU door, not cash auction). | Added 2026-06-11, comms wave-1 ingest, multi-source, estimates flagged. US auction totals and the speed-vs-connections physics are well-sourced; several European per-MHz-POP decimals and the global $140B/$37.7B totals are flagged single-source. Builds on rf_satcom and rf_limited_service. |
| [direct_communication/bands_and_enabling_hardware.md](direct_communication/bands_and_enabling_hardware.md) | draft | The silicon is not the bottleneck up through W-band (off-the-shelf Ka/V/E, emerging W-band, research-only sub-THz); the binding constraints are spectrum coordination, rain fade, and pointing; optical-primary-plus-RF-complement is the settled architecture. | Added 2026-06-11, comms wave-1 ingest, multi-source, estimates flagged. Chip-availability mapping rests on catalog parts and NASA/peer-reviewed results; W-band PA numbers and the NTT 300 GHz record are single-demo/single-vendor. Extends rf_satcom's band table and space_hardware_capabilities. |

### Laser Communications

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [laser_comms/comms_business_case.md](laser_comms/comms_business_case.md) | draft | Direct communications can be a focused B2B/B2G line, not a Starlink clone. | Has source section; workstream spelling normalized to `direct_communication/` in the header. |
| [laser_comms/constellation_mesh.md](laser_comms/constellation_mesh.md) | draft | Laser range does not bind; ground reach and service architecture do. | Has source section and external citations. |
| [laser_comms/laser_terrestrial_interconnect.md](laser_comms/laser_terrestrial_interconnect.md) | draft | Terrestrial laser/FSO is a real shipping product class (Taara up to 25 Gbps over 10 km) but a gap-filler, not a fiber replacement; the same fog wall forces an RF backup for five-nines; strong where fiber is absent, conditional (security, latency, fast deploy) where it exists. | Added 2026-06-11, comms wave-1 ingest, multi-source, estimates flagged. Product specs and weather/hybrid-FSO-RF physics are well-sourced and consistent with `optical_ground_stations.md`; market-size dollars and the DC-interconnect use are flagged nascent/single-vendor. |
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
| [rocket_lab/space_hardware_capabilities.md](rocket_lab/space_hardware_capabilities.md) | draft | Rocket Lab has much of the stack; node-scale deployable radiators are pending in-house development. | Has source section and external citations. |
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
| [synthesis/comms_baseline_synthesis.md](synthesis/comms_baseline_synthesis.md) | draft | Neutral comms-track base: the market is enormous, mobile-dominated, mature, and barely growing; diminishing returns past baseline broadband is the most robust finding; the served space-comms market is ~5-10% of cited TAM; optical-primary-plus-RF is the settled architecture; no verdict offered. | Added 2026-06-11, comms wave-1 ingest, multi-source, estimates flagged. Pulls the ten ingest docs plus the existing comms corpus by path; tags every number FACT/ESTIMATE/PROJECTION; carries its own COMM-S## claims namespace reconciled into SOURCE_INDEX by the lead. |

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
| Communications wave 1 (commissioned 2026-06; ingested 2026-06-11) | Founder commissioned an isolated communications research effort sharing the library: size the broadband/cellular/global markets ex-China; clarify the ASTS/SpaceX cited-vs-served TAM; test the diminishing-returns-past-baseline-broadband hypothesis and the data-center-vs-comms premium contrast; assess laser (weather-limited, possibly fiber-dependent) and security as a differentiator; supply a Falcon 9 cadence analogue for the Starship orbital-DC timeline. No verdict requested at this stage. | `economics/comms_*` (6 docs), `direct_communication/` (spectrum, bands/hardware), `laser_comms/laser_terrestrial_interconnect.md`, `competitors/falcon9_cadence_ramp.md`, `synthesis/comms_baseline_synthesis.md`, `vision/comms_thesis.md`. |

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
- Communications wave 1 (2026-06-11), the biggest open numbers the base could
  not close, carried for later comms waves:
  - US-only fixed-broadband revenue boundary. The $63.6B (narrow) vs ~$92B
    (broad) vs $100.5B (North America) spread needs one agreed definition
    (access-only or access-plus-bundled-attach) before any comms TAM math
    (`economics/comms_us_broadband_market.md`).
  - Ex-China Asia split. Published Asia Pacific totals include China; a clean
    ex-China Asia (India plus Southeast Asia plus developed Asia) figure is not
    directly published and needs a bottom-up build
    (`economics/comms_global_regional_market.md`).
  - Dollar size of the satellite-addressable rural/remote fringe. ANSWERED in
    wave 2 (2026-06-11): sized at ~$40-55B/yr conservative to ~$95-130B/yr
    optimistic (ex-China, ILLUSTRATIVE), with the structural finding that the
    dollars are in the developed-world rural fringe and high-ARPU mobility/
    enterprise verticals, not the ~3.1B-person usage gap. See
    `economics/comms_rural_fringe_sizing.md` and the consolidation
    `economics/comms_addressable_sizing.md`.
  - Premium/sovereign niche size. ANSWERED in wave 2 (2026-06-11): a ~$75-95B/yr
    gross spend pool, of which only ~$8-30B/yr is open to a new commercial
    entrant once the closed flagship programs (IRIS2 EUR 10.6B, SDA tranches,
    $2.29B SpaceX SDN, GOVSATCOM) are removed as demand proof rather than
    addressable revenue. See `economics/comms_premium_sovereign_sizing.md` and
    the consolidation `economics/comms_addressable_sizing.md`.
  - Communications wave 2 (2026-06-11), the new open questions the consolidation
    surfaced, carried for later comms waves:
    - Single-operator capture rate. The consolidated ~$45-60B to ~$110-150B/yr is
      the all-operators contestable pie; what share a specific new entrant wins
      against Starlink/Starshield, Eutelsat/OneWeb, SES, Viasat, Amazon Leo, and
      Kepler is a competitive-share question neither sizing doc answers
      (`economics/comms_addressable_sizing.md`).
    - Supply-side space economics. The wave-2 pools are demand-side only; whether
      the constellation capex, optical ground network, and launch cadence close
      against these revenues is a separate workstream, explicitly not assumed.
      This was the load-bearing gate on Hypothesis 2; PARTIALLY ADDRESSED in wave 3
      (2026-06-11 commission, ingested 2026-06-17): the cost ratio favors space in
      the fringe/premium layer and not in served markets, but only for SCALED
      (Starlink-scale) space, so the gate narrows to the entrant-specific cost level
      (`economics/comms_addressable_sizing.md`, `vision/comms_thesis.md` Rev 2-3,
      and the wave-3 `economics/comms_*` cost docs below).
    - Whether carrier direct-to-cell belongs in a space-comms addressable number
      at all. It is a bolt-on across the general mobile base, not rural-fringe
      broadband; it carries ~$20-30B of the optimistic case (stripping it gives a
      rural-plus-premium-proper optimistic ceiling of ~$90-120B). This is a
      definitional call for the lead (`economics/comms_rural_fringe_sizing.md`,
      `economics/comms_addressable_sizing.md`).
  - Communications wave 3 (commissioned 2026-06; ingested 2026-06-17), the new open
    questions the ground-vs-space cost ratio surfaced, carried for later comms waves:
    - The exact density crossover. The fresh-build-vs-space crossover sits around the
      dense-suburban fringe (~$490/sub/yr annualized ground ~= ~$480-680 space), but
      the precise homes-per-mile (or $/passing) at which a fresh ground build crosses
      above the space cost is the single number that sizes the cost-advantaged fringe;
      it needs the density-cost model both base docs flag
      (`economics/comms_ground_vs_space_cost_ratio.md` OQ1,
      `economics/comms_space_supply_cost.md` OQ4,
      `economics/comms_broadband_deployment_economics.md`).
    - A hard space cost-per-GB. The flavor-(b) per-GB ratio rests on the
      ~$0.05-0.30/GB space figure, the softest (utilization-dependent) number in the
      space stack; a disclosed Starlink throughput (petabytes/day) would tighten both
      the per-GB ratio and the crossover point
      (`economics/comms_space_supply_cost.md` OQ1,
      `economics/comms_ground_vs_space_cost_ratio.md` OQ2).
    - The NON-SpaceX (small-constellation) cost level. The wave-3 space numerator is
      the MATURE incumbent (Starlink); a concrete small-constellation cost model (N
      satellites, M subscribers, fixed-cost spread) would convert "multiples higher
      per subscriber" into a number and let the ratios be re-run for a Rocket Lab-
      scale entrant. This is the number the thesis ultimately needs and the narrowed
      gate on Hypothesis 2 (`economics/comms_ground_vs_space_cost_ratio.md` OQ3,
      `economics/comms_space_supply_cost.md` OQ5).
    - How aggressively incumbents actually price to defend against satellite. The
      flavor-(b) floor is the price the incumbent COULD cut to; whether it does so
      against a LEO competitor (versus relying on latency/bundle defenses) is a
      market-conduct question that bears on how much of the served market is truly
      closed to space on price (`economics/comms_incumbent_margins_competitive_floor.md`
      OQ4, `economics/comms_ground_vs_space_cost_ratio.md` OQ4).
    - Mobile / direct-to-cell as the narrowest gap. The space network-average per-GB
      can sit at or below the mobile ~$0.50-1.50/GB delivery cost, the one served
      comparison where the gap nearly closes; whether direct-to-cell / mobile-
      augmentation is therefore the served sub-market where space is least
      disadvantaged on cost (distinct from fixed broadband, where it is 5-30x+ above)
      is worth a dedicated pass, and ties to the direct-to-cell bucket in the
      addressable doc (`economics/comms_ground_vs_space_cost_ratio.md` OQ5).
  - Direct-to-cell revenue per user. Starlink reports 16M D2D users but no clean
    per-user revenue for the D2D layer, and AST is pre-scale (~$70.9M FY2025
    against a ~$1.1T cited TAM); the unit economics of "fill the dead zones"
    remain unproven (`economics/comms_us_cellular_market.md`).

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
