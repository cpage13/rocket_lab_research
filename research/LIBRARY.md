# Library: Research Catalog & Glossary

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

- [vision/initial_thesis.md](vision/initial_thesis.md): append-only thesis
  through Revision 7.
- [synthesis/wave5_synthesis.md](synthesis/wave5_synthesis.md): latest full
  research synthesis in this folder; launch-cost framing is historical.
- [README.md](README.md): research-wiki front door and navigation rules.
- [SOURCE_INDEX.md](SOURCE_INDEX.md): claim-level source ledger for hard
  numbers and scenario assumptions.
- [RESEARCH_TRACKER.md](RESEARCH_TRACKER.md): file status, audit notes, and
  backlog.
- Topic folders below, source research and historical review artifacts.

For the communications workstream specifically (comms wave 1, ingested 2026-06-11),
start with [synthesis/comms_baseline_synthesis.md](synthesis/comms_baseline_synthesis.md)
(the neutral market-and-technology base) and the companion
[vision/comms_thesis.md](vision/comms_thesis.md) (Revision 1 belief record, no verdict).
The source docs sit under `economics/` (the `comms_*` market and deployment docs),
`direct_communication/` (spectrum and bands/hardware), `laser_comms/` (terrestrial
interconnect), and `competitors/` (the Falcon 9 cadence ramp).

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
| [vision/comms_thesis.md](vision/comms_thesis.md) | Communications thesis, Revision 1 (belief record only; comms wave 1). | The starting belief record for the comms track: working hypotheses (diminishing returns past baseline broadband; space as a possible step change gated on economics and new use cases; laser high-bandwidth but weather-limited and possibly fiber-dependent; security as a differentiator) and the open questions that test them. No verdict; built on the comms baseline synthesis. |
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
| [competitors/starship_addendum.md](competitors/starship_addendum.md) | Starship competitive addendum, with a dated 2026-06-09 update on the SpaceX AI-1 reveal. | The real near-term risk is capital/customer capture by Starship-gated rivals; the June 2026 AI-1 design reveal is the latest such signal. |
| [competitors/falcon9_cadence_ramp.md](competitors/falcon9_cadence_ramp.md) | Falcon 9 cadence ramp 2010-2026 and the Starship orbital-DC timeline read (comms wave 1). | Falcon 9 took ~14 years to reach a 165/yr record; high cadence arrived only once booster reuse was routine and Starlink filled the manifest. Starship must rerun a harder curve (upper-stage reuse), so "at least about 5 years" to significant orbital data centers is better supported than "about 3 years"; communications is the credible near-term Starship payload. |
| [competitors/starlink_v3_specs.md](competitors/starlink_v3_specs.md) | Starlink V3 as the concrete cost-and-capacity benchmark for a modern RF broadband constellation at the frontier: per-satellite specs, the V2-to-V3 jump, the Gen2 broadband and dedicated direct-to-cell fleets, and the Starship/Neutron-fit handoff (comms wave 4). | V3 is a Starship-class satellite (~3.3x V2-mini mass, ~60 m wingspan) delivering ~1 Tbps/sat down and ~60 Tbps per Starship launch, but its capacity story is inseparable from the launch vehicle: the per-bit cost-down is bought with mass only a very large launcher can carry, and the direct-to-cell capacity leap is a spectrum-acquisition story first (~$17B EchoStar buy, ~65 MHz). Owns the V3 spec stack the Neutron-fit doc references. |

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
| [economics/operating_margins_and_revenue_multiple_2026.md](economics/operating_margins_and_revenue_multiple_2026.md) | Operating vs gross margin, GPU-cloud operator margins and multiples, depreciation periods, and validation of the 1.5x revenue multiple. | R=1.5 is fair to mildly conservative. The right lens is the OPERATING margin: orbital's near-zero opex makes its 33% over depreciation an operating-equivalent, matching mature hyperscaler cloud operating margins (Google Cloud ~33%, AWS ~35-38%, Azure ~45%) and far above compressed neocloud operating margins (~1% or negative). R is still a markup over amortized cost (gross/operating/net definitions kept). We depreciate over 5 years, shorter and more conservative than operators' 6-year lives (Microsoft, Google, Oracle, Meta extensions; Amazon's 6->5 reversal), so the assumption does not flatter the margin. Replaces the stale Oracle 30-40% figure. |
| [economics/revenue_per_watt.md](economics/revenue_per_watt.md) | Revenue per GW/rack. | Separates IaaS economics from integrated inference-service economics. |
| [economics/comms_us_broadband_market.md](economics/comms_us_broadband_market.md) | US fixed-broadband market size, provider financials, and the diminishing-returns question (comms wave 1). | US fixed broadband is ~$70-95B/yr; the largest broadband subscriber bases (Comcast, Charter) carry the smallest market caps; willingness-to-pay for speed is sharply concave (~$2.34/Mbps at 4-10 Mbps to ~$0.02/Mbps at 100-1,000), so value rewards reach and reliability, not raw bandwidth. |
| [economics/comms_us_cellular_market.md](economics/comms_us_cellular_market.md) | US wireless/cellular market, the big-three carrier financials, and the MVNO/wholesale layer (comms wave 1). | US wireless service revenue is ~$326B/yr (single major source); the cable MVNOs prove a non-carrier can build 20M+ lines on rented capacity, the same wholesale logic behind carrier-hosted direct-to-cell. |
| [economics/comms_global_regional_market.md](economics/comms_global_regional_market.md) | Global and regional comms market (broadband plus cellular) by region, ex-China (comms wave 1). | Global telecom services are ~$2.0-2.1T/yr (mobile ~$1.19T, fixed broadband ~$360-390B); satellite is ~0.5% of fixed broadband; the GSMA $7.6T is GDP contribution, not operator revenue, and must not be summed with market-size lines. |
| [economics/comms_cellular_5g_deployment_economics.md](economics/comms_cellular_5g_deployment_economics.md) | Cost and unit economics of deploying/upgrading cellular (5G) networks (comms wave 1). | Mobile-network capex is ~14-19% of service revenue and declining; a 5G site upgrade is ~$20-50K, a new macro ~$100-300K; the C-band auction alone was ~$81B; payback is ~8-10 years and 5G delivered no ARPU premium. |
| [economics/comms_broadband_deployment_economics.md](economics/comms_broadband_deployment_economics.md) | Fixed-broadband deployment economics (fiber, cable, FWA) and the incremental-value question (comms wave 1). | A cable incumbent defends a passed home for ~$100-300 (vs ~$1,000+ fiber overbuild); the space value is in the unserved/remote tail ($3,000-6,000 rural up to ~$200,000+ extreme remote), not served markets. |
| [economics/comms_space_tam_claims.md](economics/comms_space_tam_claims.md) | The space-comms TAM clarified: cited headline vs bottoms-up served market (comms wave 1). | Cited connectivity TAMs (SpaceX $1.6T, AST ~$1.1T) and the realistically served slice are separated by ~2 orders of magnitude; Morningstar's realistic Starlink market is ~$129B; the default prior is a ~90% haircut (served ~5-10% of cited). |
| [economics/comms_rural_fringe_sizing.md](economics/comms_rural_fringe_sizing.md) | Sizes the satellite-addressable rural/remote fringe in dollars, bottoms-up from household counts and region-specific ARPU (comms wave 2). | The fringe is ~$40-55B/yr conservative to ~$95-130B/yr optimistic (ex-China, ILLUSTRATIVE), ~2.5-8% of the cited $1.6T and bracketing Morningstar's ~$129B; the structural finding is sharper than the number, the dollars are in the developed-world rural fringe and the high-ARPU mobility/enterprise verticals, NOT in the ~3.1B-person usage gap (an income problem satellite supply does not fix). Starlink's blended ARPU fell 33% in two years chasing that emerging-market tail. |
| [economics/comms_premium_sovereign_sizing.md](economics/comms_premium_sovereign_sizing.md) | Sizes the premium/sovereign niche in dollars, separating the gross spend pool from the slice open to a new commercial entrant (comms wave 2). | A ~$60-95B/yr gross premium/sovereign pool (ex-China): ~$60-70B sourced bottom-up from the components, up to ~$95B as an estimated ceiling (ESTIMATE, not a sourced figure at the top). Only ~$8-30B/yr is OPEN to a new commercial-services entrant (ILLUSTRATIVE): the cited flagship programs (IRIS2 EUR 10.6B, SDA tranches, the $2.29B SpaceX SDN award, GOVSATCOM) are closed prime/consortium builds, demand proof not addressable revenue. The niche trades addressable size (small) for margin and durability (high). Rocket Lab uniquely already sits on the closed-prime side (>$1.3B in SDA awards), a different business from the commercial niche sized here. |
| [economics/comms_addressable_sizing.md](economics/comms_addressable_sizing.md) | Consolidation: reconciles the rural/remote fringe and the premium/sovereign pools against the $1.6T and $129B anchors, de-duplicating the shared mobility/enterprise verticals (comms wave 2). | The two pools share the mobility/enterprise verticals, so they are reconciled (five non-overlapping buckets), not summed. The de-duplicated new-entrant-addressable pool is ~$45-60B/yr conservative to ~$110-150B/yr optimistic (ex-China, ILLUSTRATIVE): ~3-9% of the cited $1.6T and in the same band as the ~$129B realistic served estimate. Two independent methods (this bottoms-up consolidation and Morningstar's top-down rebuild) landing in the same band is the load-bearing cross-check; no verdict, no supply-side economics, no single-operator capture rate. |
| [economics/comms_space_supply_cost.md](economics/comms_space_supply_cost.md) | The space supply-side cost stack to DELIVER communications, built from the disclosed Starlink S-1 (comms wave 3). | The mature incumbent delivers for ~$480-680/subscriber/yr all-in (space-specific satellite+launch replacement ~$200-260/sub/yr) at a disclosed ~38.6% segment operating / ~63% segment EBITDA margin on $11.4B of 2025 Starlink revenue; network-average ~$0.05-0.30/GB but RISING with user density (the opposite of fiber, the permanent structural ceiling). The cost is dominated by the satellite fleet on a 5-year replacement treadmill (~$6-8B/yr, single-lineage flag), then launch (20-70% of system capital), then a small but availability-critical optical ground segment. Scale is the whole game: the same fixed stack is cheap per subscriber only at SpaceX scale. No verdict. |
| [economics/comms_incumbent_margins_competitive_floor.md](economics/comms_incumbent_margins_competitive_floor.md) | Ground incumbents' margins and the marginal-cost price floor a space entrant must beat in served markets (comms wave 3). | US carriers/cable run ~36-41% EBITDA margins and ~80-90% broadband gross margins, so in a SERVED market the incumbent defends an existing subscriber not at its list price but at its marginal cash cost: ~10-20% of ARPU (~$7-15/mo, ~$84-180/sub/yr) for fixed broadband and ~$0.50-1.50/GB for mobile (single-source flag), with ~30-40 points of EBITDA headroom to absorb the cut. The asymmetry versus the data-center 1.92x: that ground side is a fresh build paying full freight, while the comms served-market competitor has already sunk its plant. In the unserved fringe there is no such floor, which is exactly where the addressable dollars sit. No verdict. |
| [economics/comms_ground_vs_space_cost_ratio.md](economics/comms_ground_vs_space_cost_ratio.md) | The headline ground-vs-space delivery-cost ratio, the realistic-for-SpaceX cost level, and the competitive verdict (comms wave 3). | Communications has not one ratio but TWO that point in opposite directions, split by whether the ground plant already exists (the two-flavor asymmetry). Flavor (a), space vs a fresh ground build (unserved): space is CHEAPER by ~1.3-3.2x rural and ~65-90x in the extreme tail, the opposite direction to the data-center 1.92x. Flavor (b), space vs the incumbent's marginal cost (served): space is COSTLIER by ~3-8x. The ~$480-680/sub/yr cost level that earns the addressable pool at ~38% op / ~63% EBITDA is not aspirational, it is Starlink's disclosed 2025 actual, already achieved at SpaceX scale but unreachable for a small constellation (denominator-driven). Space wins on cost exactly where the wave-2 demand sits (the fringe and the premium/sovereign layer) and nowhere else; two independent lines (revenue and cost) land on the same map. No business verdict. |
| [economics/comms_4g_5g_transition_cost.md](economics/comms_4g_5g_transition_cost.md) | Isolates what the 4G-to-5G upgrade actually cost ground operators as a discrete cycle, per operator, defining the "X" a space alternative must beat on the next (6G) cycle (comms wave 4). | The cost "X" has three stacked layers, but the load-bearing one is the middle (deployment capex), because spectrum and already-sunk 4G plant are not what a new entrant displaces on the next cycle. The 5G cycle's deployment cost was carried overwhelmingly by new radio hardware on existing sites (US majors' incremental programs single-digit-to-low-double-digit billions: Verizon ~$10B, AT&T ~$6-8B, US Big-3 ~$26-35B), not by new sites, the core, or cash-capex spectrum. The forward 6G cycle repeats that shape, so X-on-the-next-cycle is roughly the next radio refresh per covered POP plus whatever new spectrum that generation demands. |
| [economics/comms_6g_demand_value.md](economics/comms_6g_demand_value.md) | What 6G actually is and whether users will pay a premium for it, testing the thesis that 6G is a forced cost users will not pay extra for (comms wave 4). | 6G is real as a standards program (ITU IMT-2030, specs ~end-2028, commercial ~2030) but its targets are an incremental extension of 5G's, not a step change, and the demand evidence (McKinsey: two-thirds will not pay >5 euros/mo even for 10x speed; PwC: only ~one-third would pay extra for 5G at ~$4.40-5.06/mo) shows users do not pay a premium for "more G." The likely shape is a forced cost, not a demand pull: a build operators must do for capacity and parity against a user base that will not pay extra, the exact margin squeeze the founder's thesis predicts, which widens the cost-down window for a cheaper delivery method competing on reach and reliability. On the $10/mo test, a typical user would almost certainly not pay an extra $10/mo for 6G. |
| [economics/comms_direct_to_cell.md](economics/comms_direct_to_cell.md) | The lead-market base doc on direct-to-cell (satellite-to-phone): market, spectrum, capacity limits, unit economics, and the home-broadband cannibalization question (comms wave 4). | The two pure-play benchmarks have diverged into opposite architectures (AST: few enormous satellites, Block 2 ~223 m2 arrays; Starlink: small payloads on many birds), with the same Shannon-and-beam-geometry ceiling; the spectrum model is shifting from "rent the carrier's spectrum" toward "own dedicated spectrum plus roam on the carrier's." The capacity ceiling is the whole story: satellite NTN delivery costs ~$5-9/GB versus ~$0.30/GB for terrestrial 5G (~20x, single named analyst), so D2C is the served sub-market where space is least disadvantaged but still well above the terrestrial floor, and it cannibalizes the thin rural/edge home connection, not the dense-market home-broadband line. On served revenue D2C is not yet larger than fixed broadband ex-China (~$12-14B by 2030 vs the ~$129B served slice), but on reach and 10-year optionality it is plausibly larger, contingent entirely on whether the per-GB capacity gap closes. |

### Direct Communication

| File | What it is | Key takeaway |
|---|---|---|
| [direct_communication/README.md](direct_communication/README.md) | Communications workstream front door. | The adjacent Rocket Lab communications thesis and its scope. |
| [direct_communication/spectrum_fundamentals_economics.md](direct_communication/spectrum_fundamentals_economics.md) | Spectrum fundamentals, the speed-versus-connections tradeoff, and auction cost today (comms wave 1). | Mid-band is the contested sweet spot; US C-band cost ~$0.94/MHz-POP (~$81B) while mmWave is hundreds of times cheaper; terrestrial cellular spectrum is effectively closed to a new entrant, so the spectrum fight belongs in the satellite domain (ITU door, not cash auction). |
| [direct_communication/bands_and_enabling_hardware.md](direct_communication/bands_and_enabling_hardware.md) | The non-traditional band ladder, the enabling silicon band by band, and a consolidated RF-vs-laser comparison (comms wave 1). | The silicon is not the bottleneck up through W-band (off-the-shelf Ka/V/E parts, emerging W-band, research-only sub-THz); the binding constraints are spectrum coordination, rain fade, and pointing; the settled architecture is optical primary plus an upper-microwave RF complement. |
| [direct_communication/spectrum_generations_and_availability.md](direct_communication/spectrum_generations_and_availability.md) | What a cellular "generation" actually is, spectrum refarming/DSS portability, what is left for 5G/6G (FR3, WRC-27), the satellite-beam capacity ceiling, and the buy-vs-partner spectrum-access question (comms wave 4). | A "generation" is a standard and capability set, not a frequency; a satellite beam is Shannon-times-footprint gated and cannot densify (~300x to ~30,000x less area-capacity than a terrestrial macro), so satellite direct-to-cell is a coverage/fill-in layer, not a capacity layer; and the realistic spectrum path for an entrant is the FCC SCS partner/lease model (ride a carrier's band), not buying a cellular band (SpaceX's ~$17B EchoStar buy is the deep-pocketed exception). |

### Laser Communications

| File | What it is | Key takeaway |
|---|---|---|
| [laser_comms/comms_business_case.md](laser_comms/comms_business_case.md) | Communications business case. | A focused B2B/B2G private orbital network is plausible; it is not Starlink. |
| [laser_comms/constellation_mesh.md](laser_comms/constellation_mesh.md) | Constellation and mesh design. | Laser range does not bind; service architecture and ground reach do. |
| [laser_comms/laser_terrestrial_interconnect.md](laser_comms/laser_terrestrial_interconnect.md) | Terrestrial laser/free-space-optical links for ground and data-center interconnect (comms wave 1). | A real shipping product class (Taara up to 25 Gbps over 10 km) but a gap-filler, not a fiber replacement; the same fog wall as the space link forces an RF backup for five-nines; strong where fiber does not exist, conditional (security, latency, fast deploy) where it does. |
| [laser_comms/laser_dc_interconnect_viability.md](laser_comms/laser_dc_interconnect_viability.md) | Whether a real direct laser (free-space-optical) data-center-to-data-center market exists, how it works, who pays, and the AI-buildout demand engine; a side track to the RF consumer model (comms wave 4). | A direct laser DC-to-DC market is real but narrow on the ground (a tens-of-Gbps supplement for gap-fill, redundancy, obstacle-hop, secure fast-deploy), explicitly NOT the petabit AI synchronous-training interconnect (FSO is 2-to-5 orders of magnitude short of the ~5 Pbit/s job, which belongs to trenched coherent fiber); the one arena where direct laser DC-to-DC links are the primary winning architecture is in orbit, where no fiber exists, the natural home for Rocket Lab's Mynaric optical terminals. Per-link, not per-subscriber. |
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
| [rocket_lab/neutron/neutron_comms_payload_fit.md](rocket_lab/neutron/neutron_comms_payload_fit.md) | Whether Neutron can carry a Starlink-V3-class broadband satellite and an AST-BlueBird-Block-2-class direct-to-cell satellite, how many fit per launch, and the launch-cost-per-satellite implication; Neutron only, no Starship-class vehicle assumed (comms wave 4). | Neutron can carry both classes but only a few of each: ~5 broadband V3-class per launch (mass-limited, ~$10-11M/sat) and ~1 direct-to-cell Block 2-class per launch (antenna-stow-limited at the ~223 m2 array, ~$50-55M/sat); for broadband it is out-scaled ~10x on $/satellite by a Starship-class batch lifter, and for the lead market (D2C) its 5.5 m fairing is the binding limit. Inherits the unresolved Neutron SSO-mass and usable-fairing-volume uncertainties. |
| [rocket_lab/overview.md](rocket_lab/overview.md) | Rocket Lab company overview. | Rocket Lab is unusually vertically integrated for this thesis. |
| [rocket_lab/space_hardware_capabilities.md](rocket_lab/space_hardware_capabilities.md) | Rocket Lab hardware capabilities. | Launch, bus, solar, mechanisms, and comms are strong; node-scale deployable radiators are pending in-house (no large-scale product yet, but thermal control already flies on its satellites). |
| [rocket_lab/vertical_integration_stack_2026.md](rocket_lab/vertical_integration_stack_2026.md) | Which spacecraft subsystems Rocket Lab builds in-house vs buys, with acquisition status (Mynaric, Geost, Motiv, SolAero, Sinclair, ASI, Precision Components) and the in-house electric propulsion (Gauss). | Rocket Lab makes nearly the whole satellite bus in-house, so the supplier margins an outsider would pay are captured internally; node-scale radiators and large-scale power are a question of scale, not capability or intent. |
| [rocket_lab/manufacturing_capability_2026.md](rocket_lab/manufacturing_capability_2026.md) | Rocket Lab's demonstrated manufacturing competency (Rutherford additive production, Rosie automated composites, Neutron AFP, Flatellite mass-manufacture) and how it transfers to building data-center nodes on a line. | Volume production of complex space hardware is already Rocket Lab's core business, so the production-line thesis carries low process-execution risk; no node has been built yet. |

### Strategy

| File | What it is | Key takeaway |
|---|---|---|
| [strategy/README.md](strategy/README.md) | Engineer/CFO strategy-loop rules. | Process artifact for the cooperative strategy debate. |
| [strategy/optimized_strategy.md](strategy/optimized_strategy.md) | Historical optimized build strategy. | Converges on a gated, demand-pulled ramp; old conclusion references are historical. |
| [strategy/self_launch_cadence_and_manufacturing_advantage_2026.md](strategy/self_launch_cadence_and_manufacturing_advantage_2026.md) | Self-launch as a supply guarantee (own the rocket, own the cadence), launch fixed-cost amortization, the manufacturing learning curve, and the production-line-vs-ground-megaproject contrast. | Owning the rocket converts cadence from a customer-driven output into a planned input, which enables a production line and amortizes fixed cost; ground data centers are bespoke megaprojects. |

### Synthesis

| File | What it is | Key takeaway |
|---|---|---|
| [synthesis/lint_report.md](synthesis/lint_report.md) | First wiki lint pass. | Historical health snapshot; later work superseded several fixes. |
| [synthesis/lint_report_2.md](synthesis/lint_report_2.md) | Second wiki lint pass. | Historical post-wave-5 health snapshot. |
| [synthesis/preliminary_findings.md](synthesis/preliminary_findings.md) | Wave-1 synthesis. | No physics wall found, but many numbers later changed. |
| [synthesis/wave4_synthesis.md](synthesis/wave4_synthesis.md) | Wave-4 synthesis. | Establishes payback/GPU-obsolescence as the crux; launch-cost framing is historical. |
| [synthesis/wave5_synthesis.md](synthesis/wave5_synthesis.md) | Wave-5 synthesis. | Latest full synthesis: flyability crossover resolves at the favorable generation, conditionally. |
| [synthesis/orbital_lifetime_5v7yr_synthesis.md](synthesis/orbital_lifetime_5v7yr_synthesis.md) | Synthesis of the 5-vs-7-year orbital-lifetime study (4 docs). | The mass/payload cost of longevity is single-digit percent on every lever; 5 years is not free at low SSO (needs ~700 km or propulsion) but 7 years is cheap either way; the real trade is radiation plus mandatory deorbit (fly high) vs continuous station-keeping (stay low); design life is likely revenue-limited (aging silicon), not orbit-limited; the 7-yr natural-life altitude is a band ~720 to 900 km pending a numerical propagation. Exploratory (2026-05-29). |
| [synthesis/comms_baseline_synthesis.md](synthesis/comms_baseline_synthesis.md) | Communications baseline synthesis: markets and the current state of the technologies (comms wave 1). | The neutral base for the comms track: the market is enormous, mobile-dominated, mature, and barely growing; diminishing returns past baseline broadband is the most robust finding; the served space-comms market is ~5-10% of the cited TAM; optical-primary-plus-RF is the settled architecture. No verdict; the founder's DC-vs-comms comparison falls out of the diminishing-returns and TAM findings. |
| [synthesis/comms_framework_synthesis.md](synthesis/comms_framework_synthesis.md) | Communications framework synthesis: lays out the shape of the comms model in the same form as the data-center conclusion, with the wave-4 numbers in their slots; isolated to comms, renders no verdict (comms wave 4). | The comms model is space cost per subscriber (density-aware, rising with user density, the inverse of terrestrial) times 1.5 for ~30% regular margin, compared FORWARD against ground's NEXT-upgrade (6G) cost; the output is not a single ratio (the data-center 1.92x mirror does not exist for comms) but a map: space wins on the forward comparison in the unserved/fringe and premium/sovereign layers and loses in dense served markets. Direct-to-cell is the lead market (by optionality, not current revenue); the forced 6G upgrade users will not pay extra for is the catalyst. A structure, not a populated model; the entrant-specific cost per subscriber stays the open gate. |
| [synthesis/comms_wave1_lint_report.md](synthesis/comms_wave1_lint_report.md) | Communications wave-1 lint pass: read-only QA over the wave-1 ingest docs, baseline synthesis, and thesis Rev 1. | Health snapshot for the comms wave-1 corpus (carrier-financial harmonization, post-Frontier subscriber reconciliation, the GSMA $7.6T GDP-vs-revenue guard); 0 blockers. |
| [synthesis/comms_wave2_lint_report.md](synthesis/comms_wave2_lint_report.md) | Communications wave-2 lint pass: read-only QA over the wave-2 sizing docs and thesis Rev 2. | Health snapshot for the wave-2 dollar sizing (rural/remote fringe, premium/sovereign, consolidated addressable); flags the colliding internal COMM namespaces for lead reconciliation; 0 blockers. |
| [synthesis/comms_wave3_lint_report.md](synthesis/comms_wave3_lint_report.md) | Communications wave-3 lint pass: read-only QA over the wave-3 cost docs and thesis Rev 3. | Health snapshot for the supply-side cost stack, the incumbent marginal-cost floor, and the ground-vs-space ratio; flags the single-lineage replacement-capex and single-source per-GB figures; resolves the $700-850 summary outlier and the gross-pool reconciliation to ~$60-95B. |
| [synthesis/comms_wave4_lint_report.md](synthesis/comms_wave4_lint_report.md) | Communications wave-4 lint pass: read-only QA over the seven wave-4 source docs, the framework synthesis, and thesis Rev 4. | The wave-4 set is strong and well-disciplined (0 blockers, 192 internal links resolved); one material issue, a numeric contradiction on the AST BlueBird Block 2 antenna-array area (corrected to ~223 m2), plus single-source FACT flags to carry into the ledger (D2C ~$5-9/GB single-analyst, AST beam/cell figures, Starlink per-beam throughput). |

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

**Research corpus**: the evidence base under `research/`: source research,
synthesis, lint passes, debate, strategy, peer review, and thesis history.

**Source index**: the claim-level ledger that records whether hard numbers are
certified facts, sourced estimates, derived estimates, external projections,
project extrapolations, scenarios, placeholders, or stale history.

**Static conclusion**: the reviewed human-readable conclusion for the promoted
defaults. It does not live in `research/`; the default data-center conclusion
lives under `data_center/`.

**Model JSON**: machine-readable model output. It is generated/promoted outside
`research/`, with the default data-center model under `data_center/models/`.

**Node**: the project product unit: one orbital spacecraft carrying GPU
packages plus bus, power, thermal, and comms. Older research sometimes says
"rack" when it means the product unit; that is historical terminology.

**Rack**: NVIDIA hardware terminology: a cabinet-scale compute product such as
NVL72. Use "rack" for NVIDIA hardware, not for the project product.

**Package**: the NVIDIA GPU package as sold and modelled, even when it carries
multiple compute dies.

**R band**: the model's revenue-to-cost band: `revenue = R * cost`, with low,
central, and high trajectories.

**Neutron**: Rocket Lab's reusable medium-lift rocket; the assumed launcher for
the data-center node.

**Electron**: Rocket Lab's operational small-lift rocket; context only for this
data-center thesis.

**SSO**: Sun-synchronous orbit. Dawn-dusk SSO is the enabling orbit because it
reduces eclipse and battery burden.

**Ballistic coefficient (BC):** mass per unit drag area (kg/m2) of a spacecraft.
A low BC means high drag relative to mass, so the node decays faster; the large
deployed area of a data-center node gives an unusually low BC and a short natural
orbital lifetime at low altitude.

**Single-event upset (SEU):** a transient bit-level error caused by an energetic
particle striking electronics (GPU/HBM logic or memory). The SEU rate rises with
altitude and is largely un-shieldable, which makes it a binding cost of flying
higher rather than a mass problem.

**Hot-loop radiator**: a thermal architecture that runs coolant/radiator
surfaces hotter so the radiator can reject more heat per square meter.

**Optical comms / laser comms**: free-space optical links used for high-rate
space-to-space or space-to-ground communication.

**RF sliver**: a limited radio-frequency service path kept as backup or a
focused B2B channel, not the main data-center product.

**Inference**: serving a trained model. This is the compute workload the
project targets.

**Training**: building a model. It is far more communication-intensive and is
not the initial workload.

**Build-to-learn**: the staged approach where early nodes prove the hard
subsystems and market premium before a scaled buildout.

**MVNO (Mobile Virtual Network Operator):** a brand that sells mobile service
to end users on rented wholesale capacity from a facilities-based carrier rather
than owning a radio network. The cable MVNOs (Xfinity Mobile, Spectrum Mobile)
prove a non-carrier can build tens of millions of lines on rented capacity, the
same wholesale logic behind carrier-hosted satellite direct-to-cell.

**ARPU (average revenue per user):** monthly revenue per subscriber line. The
comms base treats it as a falling benchmark (cable broadband ARPU ~$74 and
declining), not a static one. Distinct from ARPA (average revenue per account),
which spans multiple lines and runs roughly 3x ARPU.

**FWA (fixed wireless access):** home broadband delivered over a 5G radio link
from a cell site to a rooftop/window receiver, no per-home trenching. The
capex-light terrestrial option (~$300-800/subscriber) that is taking the majority
of US broadband net adds at "good-enough" speed.

**Direct-to-cell (D2D, direct-to-device):** letting an ordinary unmodified
smartphone connect to a satellite when no terrestrial tower is in range, via a
carrier wholesale/hosting arrangement (AST with AT&T/Verizon; Starlink with
T-Mobile). Large user counts but thin per-user revenue so far.

**Mid-band:** the 1-6 GHz spectrum tier (including C-band) that balances speed
and reach and penetrates walls, making it the contested "sweet spot" and the most
expensive cellular spectrum. Low-band (<1 GHz) buys reach and connection count;
mmWave (24 GHz+) buys peak speed but little coverage.

**Free-space optical (FSO):** a modulated laser beam (typically 1550 nm) sent
through open air between line-of-sight terminals, the same physics as a fiber link
with the glass removed. Used both space-to-ground and ground-to-ground; broken
(not degraded) by cloud/fog, so it needs site diversity or an RF backup path.

**Cited TAM vs served-addressable market:** the two non-comparable space-comms
market figures. A cited (total-market) TAM is population times spend (hundreds of
billions to trillions); the served-addressable (bottoms-up) market is the slice an
operator can realistically win after physics and competition (single-digit to
low-hundreds of billions). The comms base default prior is a ~90% haircut: the
served market is roughly 5-10% of the cited total.

**Diminishing returns past baseline broadband:** the comms base's most robust
finding. Willingness-to-pay for speed is sharply concave (about $2.34/Mbps at 4-10
Mbps collapsing to about $0.02/Mbps from 100 to 1,000 Mbps), so the value curve
rewards reach and reliability, not raw bandwidth past a low-hundreds-of-Mbps
threshold. It is the founder's contrast to data centers, where demand outruns
supply and capacity expansion is rewarded.

**Capex intensity:** network capex as a percent of service revenue, the most
portable metric for comparing a terrestrial network to an alternative. Mobile runs
~14-19% of service revenue and is declining; AI data-center capex is a multiple of
current revenue, which is why the ratio is the axis the comms-vs-DC comparison uses.

**Coverage gap vs usage gap:** the comms wave-2 distinction that decides what is
space-addressable revenue. The coverage gap (~300M people, ~4%) is the genuinely
unserved population with no terrestrial network in range; a satellite uniquely
serves it, so it is space-addressable supply. The usage gap (~3.1B people) is
people a network already covers but who do not buy service, an affordability and
device problem a satellite does not fix; it is NOT space-addressable revenue, only
headcount. The cited "billions of unconnected" TAMs are mostly the usage gap, which
is why the honest addressable number lands two orders of magnitude below the
headline.

**Premium/sovereign niche:** the scoped, higher-margin space-comms opportunity
(government/defense satcom, maritime and aero, critical-infrastructure, finance/
low-latency, orbital-DC backhaul) that sells on sovereignty, security posture,
dedicated capacity, resilience, and latency rather than bandwidth or price. Comms
wave 2 sizes it at a ~$60-95B/yr gross pool (lead-reconciled down from ~$75-95B as
the components roll up nearer the low end), of which only ~$8-30B/yr is OPEN to a
new commercial-services entrant; the rest is closed prime/consortium programs (IRIS2,
SDA/SDN, GOVSATCOM) that are demand proof, not contestable revenue. It trades
addressable size (far smaller than the mass market) for margin and durability.

**Marginal cost / defend floor:** the cash cost an entrenched incumbent actually
avoids by losing one already-connected subscriber, and therefore the lowest price it
will rationally cut to in order to defend that customer. Because the plant is sunk,
this floor is far below both the incumbent's all-in cost and its list price: comms
wave 3 puts it at ~10-20% of ARPU (~$7-15/sub/month, ~$84-180/sub/yr) for fixed
broadband and ~$0.50-1.50/GB for mobile. The distinction that matters: a space
entrant cheaper than the incumbent's all-in or list price has won nothing in a served
market, because the incumbent will price down to this defend floor (soaking the cut
out of ~30-40 points of EBITDA headroom) and the entrant must beat the floor, not the
sticker. In the unserved fringe there is no sunk plant, so there is no defend floor,
which is why the space-addressable dollars concentrate there.

**Two-flavor cost ratio:** the comms-track finding that the ground-vs-space cost to
deliver has not one ratio but two, pointing in opposite directions, split entirely by
whether the ground plant already exists at that location. Flavor (a), space vs a
fresh ground build (the unserved comparison, the true mirror of the data-center
track's 1.92x), has space CHEAPER by ~1.3-3.2x in ordinary rural areas and tens-fold
in the remote tail. Flavor (b), space vs the incumbent's marginal/defend cost (the
served comparison the data-center track never faces), has space COSTLIER by ~3-8x.
The asymmetry is the headline: space wins on cost where there is no sunk-plant floor
(the unserved/remote fringe and the premium/sovereign layer) and loses where there is
one (dense served markets), which is exactly the map the demand-side addressable
sizing independently found.
