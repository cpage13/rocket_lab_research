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
| [competitors/starlink_v3_v4_spectrum_incorporation.md](competitors/starlink_v3_v4_spectrum_incorporation.md) | How much spectrum each Starlink generation actually incorporates: the band-by-band MHz/GHz inventory (broadband user link, gateway/backhaul, direct-to-cell) and the bandwidth-to-capacity link in a real platform (comms wave 5). | The user link is fixed and modest (~2 GHz Ku down, ~500 MHz Ku up, identical V1/V2/V3); the per-generation capacity leap is a beams-and-backhaul story (a V3 reuses the SAME 2 GHz across dozens of fully-digital beams at ~4-4.5 bits/Hz, fed by a wide Ka + E-band 10 GHz pipe, to reach ~1 Tbps), not a user-bandwidth story. The system incorporates >20 GHz of licensed RF (Ka+E+V) plus license-free optical ISLs. Direct-to-cell is two thin low-band slices: a 2x5 MHz SCS lease (entrant-realistic) and a ~65 MHz owned block costing ~$17B+ (the ~115 MHz often quoted is the full FCC deal; SpaceX got ~65 MHz, AT&T ~50 MHz). "V4" is not a disclosed spectrum generation. |
| [competitors/large_array_folding_and_stow.md](competitors/large_array_folding_and_stow.md) | How much a Starlink V3 folds versus a folding direct-to-cell array: the deployed-to-stowed fold ratio, the modular-tile count, and the general RF-array packing rule that decides launch fit (comms wave 5). | "Fold it twice" is roughly right for the V3 broadband aperture (it barely folds: the RF aperture is the flat ~7-8 m x ~3.5 m satellite body, and the ~60 m span is solar-wing-dominated, so the fold ratio is ~1x and it is mass-bound, fairing-agnostic). It badly underestimates a direct-to-cell array: AST's BlueBird Block 2 ~223 m2 aperture is ~220-265 modular ~0.84 m2 "Micron" tiles folding "phone-booth to studio-apartment" (dozens of fold lines), so it is size-bound and the fold geometry is what fills the fairing. General rule: a solar membrane stows to ~0.01% volume but a populated RF phased array packs only to ~34-48%, so a handset-closing aperture cannot fold like a solar wing. Exact fold-line counts and Block 2 folded dimensions are unpublished (flagged). |
| [competitors/starlink_v3_platform_and_starship.md](competitors/starlink_v3_platform_and_starship.md) | Starlink V3 (Gen3) as a physical platform: mass, stowed/deployed dimensions, the phased-array antenna, the direct-to-cell payload vs V2 Mini, and the load-bearing "why Starship, not Falcon 9" answer with the Neutron fairing-fit implication (comms wave 6). | V3 is a ~1,900 kg ~7 m flat slab that unfolds to a ~60 m mostly-solar wingspan; it flies on Starship because it is too LARGE for Falcon 9's 5.2 m fairing first (and ~3x V2 Mini mass second), ~54-100 per Starship (commonly ~60) vs ~21-24 V2 Mini per Falcon 9. A bare V3 slab fits a ~5.5 m Neutron fairing but is mass-bound at ~5/launch (~1/12 of a Starship batch), so the Neutron-rational design is a smaller flat-pack, the Flatellite, not a literal V3. V3 D2C is a dedicated up-to-15,000-sat 4G-equivalent constellation bought with owned ~65 MHz + a large deployable array; the broadband aperture area is undisclosed (the circulating ~25 m2 is the D2C array, not the broadband one). |

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
| [economics/ground_cellular_cost_per_subscriber.md](economics/ground_cellular_cost_per_subscriber.md) | The ground-cellular cost-per-subscriber base doc for the space-vs-ground direct-to-cell comparison: settles the comparison UNIT, the ground cost per subscriber per year in two regimes (dense-served vs sparse fresh-build, spectrum excluded), and the per-Mbps/per-GB translations and the niche where space could undercut (comms wave 7). | Use cost per subscriber per year as the unit (cross-check per GB, reject per Mbps, which flatters ground ~16-34x by pricing peak speed where the satellite has no served competitor). Ground cellular splits by regime: dense-served ~$84-310/sub/yr (the cheap many-subs-per-site regime, cross-checked against GSMA ~EUR35/connection capex and a ~$0.62/GB all-in) versus sparse fresh-build ~$875-44,500/sub/yr; the split is denominator-driven (subscribers-per-site), not a site-cost difference. Space (~$480-680/sub/yr, flat everywhere) sits BETWEEN the two, so it wins only the sparse/remote/unserved fringe; whether a ~$0.5B few-hundred-satellite constellation actually undercuts the niche-ground cost is an unmodeled scale question. No verdict. |

### Direct Communication

| File | What it is | Key takeaway |
|---|---|---|
| [direct_communication/README.md](direct_communication/README.md) | Communications workstream front door. | The adjacent Rocket Lab communications thesis and its scope. |
| [direct_communication/spectrum_fundamentals_economics.md](direct_communication/spectrum_fundamentals_economics.md) | Spectrum fundamentals, the speed-versus-connections tradeoff, and auction cost today (comms wave 1). | Mid-band is the contested sweet spot; US C-band cost ~$0.94/MHz-POP (~$81B) while mmWave is hundreds of times cheaper; terrestrial cellular spectrum is effectively closed to a new entrant, so the spectrum fight belongs in the satellite domain (ITU door, not cash auction). |
| [direct_communication/bands_and_enabling_hardware.md](direct_communication/bands_and_enabling_hardware.md) | The non-traditional band ladder, the enabling silicon band by band, and a consolidated RF-vs-laser comparison (comms wave 1). | The silicon is not the bottleneck up through W-band (off-the-shelf Ka/V/E parts, emerging W-band, research-only sub-THz); the binding constraints are spectrum coordination, rain fade, and pointing; the settled architecture is optical primary plus an upper-microwave RF complement. |
| [direct_communication/spectrum_generations_and_availability.md](direct_communication/spectrum_generations_and_availability.md) | What a cellular "generation" actually is, spectrum refarming/DSS portability, what is left for 5G/6G (FR3, WRC-27), the satellite-beam capacity ceiling, and the buy-vs-partner spectrum-access question (comms wave 4). | A "generation" is a standard and capability set, not a frequency; a satellite beam is Shannon-times-footprint gated and cannot densify (~300x to ~30,000x less area-capacity than a terrestrial macro), so satellite direct-to-cell is a coverage/fill-in layer, not a capacity layer; and the realistic spectrum path for an entrant is the FCC SCS partner/lease model (ride a carrier's band), not buying a cellular band (SpaceX's ~$17B EchoStar buy is the deep-pocketed exception). |
| [direct_communication/leo_constellation_coverage_minimums.md](direct_communication/leo_constellation_coverage_minimums.md) | The minimum LEO satellite count for CONTINUOUS (24/7) coverage of a target area: the coverage FLOOR, before capacity matters (comms wave 5). | A single LEO satellite covers a ~1,300-1,900 km circle and is overhead only ~2-8 min/pass, so continuity needs a string per plane and multiple planes tiled across the target's longitude span (streets-of-coverage). Coverage-floor counts (single 24/7, SOC, slightly conservative vs optimized Walker, validated against Iridium 66): CONUS ~50-150 (low tens optimized), US+Europe ~130-450, near-global mid-latitude band ~290-960. The floor is altitude/elevation-driven (550 to 350 km or 10 to 25 degree mask each ~2-3x's it). Founder-hypothesis verdict: adding satellites buys COVERAGE (geometry) up to a floor, then CAPACITY (Shannon x beams) beyond it, CORRECT as an ordering, with the sharpening that real systems overshoot the floor for capacity and VLEO raises the floor itself, so flown counts are capacity-dominated. A continuity-only US+Europe service is a few-hundred-satellite problem, distinct from the ~1,584-30,000-satellite capacity build. |
| [direct_communication/spectrum_purchase_and_6g.md](direct_communication/spectrum_purchase_and_6g.md) | Spectrum-purchase economics: how much MHz an operator must hold, the secondary-market price per MHz-POP, the total-dollar translation for a US+Europe footprint, and whether 6G/FR3 is decided-versus-open and accessible to a satellite entrant (comms wave 5). | GSMA benchmark is 80-100 MHz mid-band per operator to launch competitive 5G; US carriers actually hold ~280-375 MHz each, so the working quantities are ~100 MHz floor and ~200 MHz to match an incumbent. Mid-band trades at ~$0.65-1.03/MHz-POP on the secondary market (AT&T-UScellular ~$0.65, SpaceX-EchoStar ~$1.03), the same range as primary auctions with no entrant discount, which translates to ~$32-46B for 100 MHz US+Europe and ~$65-90B for 200 MHz, spectrum-only. 6G/FR3 (7.125-8.4 GHz golden band plus 4.4-4.8 and 14.8-15.35 GHz) is terrestrial greenfield, not yet allocated/auctioned/held, auctions ~2028-2032+, and a satellite NTN entrant should not count on accessing it (LEO-to-handset physics hostile; the satellite role is incumbent FSS coexistence). |
| [direct_communication/dtc_antenna_aperture_tradeoff.md](direct_communication/dtc_antenna_aperture_tradeoff.md) | The link-budget/gain-physics layer under direct-to-cell: why the satellite must supply all the gain, how the required aperture scales with the target service level, why AST goes giant while Starlink goes smaller-and-many, and whether DTC can flat-stack on Neutron (comms wave 6). | The bare phone (~23 dBm, ~0 dBi) cannot help close the link, so the satellite antenna supplies the ~25 dB the path eats; aperture is the service dial (~1 m2 = SMS, ~25 m2 = a few Mbps/beam, ~60+ m2 = broadband-to-phone). The load-bearing insight is the gain-placement asymmetry: a broadband customer's dish supplies the ground-side gain so the satellite antenna can be small and flat-pack (mass-bound, many/launch); a DTC bare phone supplies nothing so the gain lives on the satellite as a giant folded aperture (size-bound, ~1/launch). DTC flat-stacks many-per-Neutron only at the messaging/thin-data rung; broadband-to-phone is ~1/Neutron. |
| [direct_communication/dtc_per_phone_rate_and_latency.md](direct_communication/dtc_per_phone_rate_and_latency.md) | The PER-SINGLE-PHONE operating point (not the per-cell rate): the aperture that delivers ~25-50 Mbps to ONE phone, whether a flat ~25 m2 Flatellite already clears the ~25 Mbps bar, and the low-orbit latency advantage (comms wave 6). | Published DTC throughputs (AST ~120 Mbps) are PER-CELL, shared; a lightly-loaded cell hands the whole beam to one phone, so per-cell-when-alone = the single-phone peak. A ~50 m2 array at low orbit on ~20-40 MHz owned spectrum lands ~25-50 Mbps to one phone (only ~1.07 dB below the ~64 m2 BlueWalker 3 that already did ~21 Mbps, and low orbit hands back ~3.5-3.9 dB). The decision-critical result: a FLAT ~25 m2 Flatellite at ~350 km clears ~25 Mbps to one phone on its own (near-parity with the BW3 link), so you keep the flat many-per-launch stack and only fold to ~50 m2 for the top of the band; capped by the BW3 device-count unknown. Low orbit also gives ~5-10 ms propagation (inside ITU-T G.114's "good" voice band) that GEO structurally cannot match. |
| [direct_communication/dtc_coverage_geography.md](direct_communication/dtc_coverage_geography.md) | Where the people are and what that means for a direct-to-cell satellite count: population by latitude, why an inclined band covers all same-latitude regions at once, which inclination to fly, and what a 95%-of-population (not 100%-of-land) target does to the count (comms wave 6/7 geography). | ~95% of people live within +/-55 deg latitude (reconstructed ~96-97%), the same ~95% the ITU says already sits in a mobile-broadband footprint, so the band IS the demand base. An inclined constellation covers a global latitude BAND, not a region: "cover US + Europe latitudes" is geometrically identical to covering the ~53-deg mid-latitude band, getting Sao Paulo, Johannesburg, Mumbai, Shanghai, Sydney for free. Fly ~53 deg (the validated industry standard); add a 70/97.6-deg shell for the Nordics/Alaska rather than raising the base. A 95%-of-population target is a SINGLE ~53-deg band at the streets-of-coverage floor (a few-hundred satellites); the last few percent and the empty high-latitude edges are what add polar shells and the 2-4x multi-fold multiplier, so they are a separately-priced scope decision. |
| [direct_communication/dtc_system_model.md](direct_communication/dtc_system_model.md) | The single GOVERNING / source-of-truth model for a Neutron direct-to-cell satellite business: it fixes the link-budget relationships once, separates two service tiers (Tier-1 4G-grade data vs Tier-2 broadband), names which lever sets each, and resolves the earlier flip on "does a smaller antenna work if you fly lower" (comms wave 6 governing model, landed wave 7). | APERTURE plus OWNED SPECTRUM set which service tier a DTC satellite reaches; ALTITUDE is only a weak ~3.5-4 dB trim (550 to 350 km) and SATELLITE COUNT sets coverage and total capacity, never per-phone rate. A moderate ~25 m2 (V3-class) aperture reaches Tier-1 4G-grade data (~2-10 Mbps); the grounded single-phone operating point is ~25-50 Mbps to one lightly-loaded phone from a ~50 m2 aperture at low orbit on ~20-40 MHz owned spectrum (~3 sats/Neutron because ~50 m2 must fold); true Tier-2 broadband (~100+ Mbps) needs ~60-223 m2 (AST-class) with no buildable altitude substitute; below ~25 m2 you only text. Low orbit also gives a structural ~5-10 ms latency edge GEO cannot match. Owns COMM-315..335 + COMM-356..365. No verdict. |
| [direct_communication/dtc_capacity_supply.md](direct_communication/dtc_capacity_supply.md) | The supply-side per-satellite-capacity input for the Neutron DTC model: the total throughput of a flat ~20-24 m2 array on ~25 MHz, the spectrum-saturation ceiling (where adding satellites stops raising per-user speed), and the speed-vs-users tradeoff (comms wave 7). | A flat ~20-24 m2 array on ~25 MHz produces ~5-15 Gbps total per-satellite (central ~8-10 Gbps), set by ~200-450 beams x ~50-75 Mbps/cell x spatial reuse, bracketing Starlink V2-mini D2C (~7 Gbps) and far below AST Block 2 (~56 Gbps). The binding cap is OWNED SPECTRUM, not the processor. The saturation ceiling is real: per-user speed is capped at (25 MHz x SE) / users_active regardless of satellite count, and once the ground is tiled by one non-overlapping beam, more same-aperture satellites add interfering co-channel beams rather than capacity. ~20-30 Mbps sustained needs ~2-4 active users per cell (a low-concurrency headline). No verdict. |
| [direct_communication/spectrum_capacity_primer.md](direct_communication/spectrum_capacity_primer.md) | The authoritative, externally-sourced plain-language PRIMER on the radio physics behind satellite DTC, every fact verifiable from textbook/measurement sources independent of any in-house claim; answers seven questions (frequency vs bandwidth vs data rate, Shannon-Hartley, the contested "25 MHz -> 75 Mbps," carrier aggregation, OFDMA, spatial reuse, aperture) each with a one-line verdict (comms wave 7). | Band = reach, bandwidth = capacity ceiling, data rate = bandwidth x a link-dependent efficiency. The contested "25 MHz -> 75 Mbps" is NOT a hard cap; it is 25 MHz x ~3 bps/Hz (AST-claimed), and the honest real-phone per-cell range is ~13-20 Mbps at Starlink-measured ~0.5-0.8 bps/Hz up to ~75 Mbps at AST-claimed ~3. Carrier aggregation sums separate channels (real, raises peak); OFDMA subcarriers only SHARE one channel (no added capacity); system capacity multiplies by spatial reuse (more cells = smaller cells = bigger aperture / lower orbit, not more satellites once tiled); aperture is the master lever. No business verdict. |
| [direct_communication/channels_aggregate_answer.md](direct_communication/channels_aggregate_answer.md) | A short one-page externally-sourced answer to the standalone founder question "do many channels add up, or are you stuck with one channel's worth?"; a plain-language explainer cross-referencing the spectrum-capacity primer for its in-house grounding (comms wave 7 companion). | YES, they add up: total data capacity is the SUM of all separate frequency channels held (each ~bandwidth x efficiency), and modern phones combine multiple channels at once via carrier aggregation so rates add; the only limit is how much spectrum you have acquired (a licensing/business limit, not a per-channel physics cap). One distinction: splitting ONE channel into many subcarriers (OFDMA) does NOT add capacity; separate channels at different frequencies are different pies that add. Carries no COMM ids of its own; cross-refs the primer's COMM-427/428/433/434. |
| [direct_communication/dtc_spectrum_access.md](direct_communication/dtc_spectrum_access.md) | The DTC spectrum-ACCESS doc: can you use ANY spectrum, what is available, and how would you obtain it; takes the aperture-decouples-bandwidth premise as correct, then shows what re-couples an entrant to a narrow band set (the phone's radio, not the antenna), the realistic DTC band inventory with the carrier-owned gate, and three acquisition routes (SCS lease / outright purchase / auction-6G) (comms wave 7, ex-China). | No, you cannot use any spectrum. The antenna decouples bandwidth from aperture in physics, but the unmodified phone re-couples you to existing cellular bands (~600 MHz-2 GHz, per the FCC SCS Report and Order); a phone has no Ku/Ka/mmWave/MSS radio. The binding constraint is the carrier-owned gate, so realistic clean DTC holdings (2x5 MHz leased, ~65 MHz owned at the EchoStar extreme) sit one-to-two orders of magnitude below the ~100-200 MHz competitive benchmark. Two real doors: SCS lease (near-zero spectrum capex, partner-gated, thin) or multi-billion purchase (~$17B/~65 MHz US; ~$32-90B for 100-200 MHz US+Europe; distressed-MSS-only). Auction/6G/FR3 is not a near-term DTC door. No verdict. |
| [direct_communication/dtc_data_rate_vs_spectrum.md](direct_communication/dtc_data_rate_vs_spectrum.md) | The doc that pins the central model output, deliverable data rate to a phone and how it scales as owned bandwidth is swept 25 -> 50 -> 100 -> 200 MHz, and resolves whether BANDWIDTH or POWER binds as the channel widens (comms wave 7). | At 25 MHz a flat ~25 m2 array at ~400 km delivers ~25-50 Mbps single-phone peak and ~20-30 Mbps sustained at 2-4 active users. The bandwidth dial is LINEAR only if power grows with bandwidth (Case A: 25->200 MHz takes one phone to ~400-600 Mbps); at FIXED power (Case B) it SATURATES because a DTC link is power-limited at ~0 dB measured SINR, so 8x the spectrum buys only ~1.36x the rate, hard-capped at ~1.44x = log2(e). POWER becomes binding somewhere in ~50-100 MHz (bandwidth-limited at ~25-50 MHz, power-limited past ~50-100 MHz); the exact knee is the load-bearing UNKNOWN (entrant power budget unpublished). Wide spectrum still adds AGGREGATE (more-users) capacity; the regulatory PFD cap does not bind in-band first. No verdict. |
| [direct_communication/dtc_subscribers_per_satellite.md](direct_communication/dtc_subscribers_per_satellite.md) | The doc that pins SUBSCRIBERS PER SATELLITE for one flat ~25 m2 cellular (not broadband) D2C satellite, separating ATTACHED subscribers from SIMULTANEOUSLY-ACTIVE users (concurrency stated), what binds (antenna vs processor vs spectrum), how many channels/bands one satellite runs at once, and the implied CAPACITY fleet versus the coverage constellation (comms wave 7). | One flat ~25 m2 cellular D2C satellite on ~25 MHz puts ~5-15 Gbps (central ~8-10 Gbps) through ~200-450 beams; that total, not a per-person rate, is what subscribers divide. The 25 MHz binding limit is OWNED SPECTRUM (computation is the LEAST binding); one satellite runs MANY beams and MANY bands at once. Subs-per-sat is two numbers: ~250-2,000 simultaneously-ACTIVE at a usable ~5-30 Mbps, and ~25,000-150,000 ATTACHED (central ~50,000-100,000) at ~1-5% busy-hour concurrency, about an order of magnitude above Starlink's ~1,260 broadband subs/sat and inside Starlink's own V3 D2C math (~70,000 attached/sat). Capacity fleet = subscribers / ~50,000-100,000 (~100-200 sats for 10M, ~500-1,000 for 50M, all above the ~340 coverage floor); the coverage-to-capacity crossover is ~20-30M subscribers. The binding real-world limiter is that subscribers must be SPREAD, not piled into dense cells. No verdict. |
| [direct_communication/spectrum_band_designations.md](direct_communication/spectrum_band_designations.md) | The radio-frequency band-designations reference: the IEEE letter bands (L/S/C/X/Ku/K/Ka/V/W), the three parallel naming vocabularies (IEEE letter vs ITU numeric vs cellular), the WWII-secrecy naming origin, and the load-bearing naming confusions; the band-letter companion to the wave-8 fundamentals explainer (comms wave 9). | The same dial position has three names at once (1.9 GHz is "L-band" to a radar engineer, "UHF" to the ITU, "PCS/mid-band/n2" to a cellular engineer), which is the root of band confusion. The one that matters most: L-band MSS (~1.6 GHz, Iridium) is ADJACENT to cellular mid-band (PCS ~1.9 GHz) but a DIFFERENT allocation, and a phone has cellular radios and NO L-band MSS radio, so owning Iridium's L-band is not the cellular band a phone uses. Three lanes stay apart: broadband on high satellite letter-bands (Ku user, Ka feeder, to a dish), direct-to-cell on low terrestrial cellular UHF (to a bare phone), and Iridium on owned L-band MSS ~1.6 GHz (to a sat-phone). Owns COMM-625..634. |
| [direct_communication/lband_device_gate_and_ntn_roadmap.md](direct_communication/lband_device_gate_and_ntn_roadmap.md) | The device gate on Iridium's owned L-band: which device classes can actually receive 1616-1626.5 MHz today and on the 3GPP NTN roadmap, the service-tier ladder, and the structural ceiling on reaching an unmodified phone (comms wave 9). | Iridium's L-band is received only by PURPOSE-BUILT hardware (sat phones, Certus, SBD/IoT modules, embedded-modem messengers), never a standard smartphone, because a bare handset has no L-band MSS radio. On the roadmap, Iridium NTN Direct (Project Stardust) is narrowband NB-IoT NTN (kbps-class messaging/IoT/SOS, no voice) on a purpose-built Nordic nRF9151 module, and Iridium's 1616-1626.5 MHz TDD block is NOT a deployed 3GPP NTN band (the standard bands are n255/n256, which every shipping NTN chipset targets); the Qualcomm-Iridium silicon (2023) got zero phone adoption and was killed November 2023. So the mainstream-phone door on Iridium's native L-band is closed today and stays closed on the roadmap regardless of satellite count; the addressable set is the purpose-built-module base, not billions of handsets. Owns COMM-661..676 (COMM-677..685 reserved-unused). |
| [direct_communication/mss_spectrum_expansion_options.md](direct_communication/mss_spectrum_expansion_options.md) | The complete menu of MSS spectrum-expansion options for RKLB-Iridium: is there more L-band, is there S-band, and the ranked options if RKLB later wants cellular-like reach or video-grade data rates (comms wave 9). | There is no more L-band MSS to BUY or LEASE as of 2026-07-01: every usable slice is held (Iridium owned; Globalstar Apple-committed and Amazon-acquiring; Viasat-Inmarsat incumbent; Ligado leased to AST for 80+ years; Thuraya no Americas rights), and S-band/2 GHz MSS is likewise gone or committed (AWS-4 to SpaceX, Omnispace merging into Lynk-SES, Globalstar-S to Apple/Amazon). The only L-band avenues are regulatory (Iridium's contested FCC 1.6 GHz sharing petition). The ranked menu: (1) Ku/Ka broadband to terminals (abundant, but not phones), (2) cellular SCS lease (thin, per-country, reaches phones), (3) improve throughput within the owned ~8 MHz, (4) cellular outright buy (billions of dollars), (5) more L-band MSS (gone), (6) S-band (gone). Owned-global L-band reaches only terminals; rented-national cellular reaches every phone; they are complements, not substitutes. Owns COMM-686..710. |

> The wave-6 direct-to-cell architecture is governed by `direct_communication/dtc_system_model.md` (the single source-of-truth system model that fixes the link-budget relationships and the two service tiers once). That governing model and the wave-7 supply-side deep-dives above it (capacity supply, the spectrum-capacity primer, spectrum access, data-rate-vs-spectrum, subscribers-per-satellite, and the channels-aggregate companion) are now committed and catalogued; the model self-labels GOVERNING/source-of-truth with one open number (per-satellite total capacity).

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
| [rocket_lab/flatellite_platform.md](rocket_lab/flatellite_platform.md) | The Rocket Lab Flatellite as the broadband/direct-to-cell satellite platform: what it is, its (mostly unpublished) specs, whether it is comms/D2C, how many ride a Neutron, and its status; the Rocket-Lab-native counterpart to the V3/Block-2 fit doc, Neutron only (comms wave 6). | Flatellite (unveiled 27 Feb 2025) is Rocket Lab's own flat, stackable, high-power satellite, comms-first and explicitly pitched at 5G-NTN/direct-to-cell as "a large-aperture system without the need for deployable antennas" (the flat body IS the aperture). Its hard specs are unpublished: ~600-800 kg mass and ~16/Neutron are a single render-read (estimate-bound), so the candidate broadband sats-per-Neutron is ~12-16 (SSO-to-LEO), the corpus's most favorable but softest per-launch count. The open question is capacity per flat satellite, not fit. Corrects the corpus bus-naming error: Flatellite is NOT the $816M SDA tracking contract (that is the Lightning bus); the comms SDA award is the $515M Transport Layer-Beta Tranche 2 (Jan 2024). Real production program, 40+ backlog, not yet flown, gated by Neutron's maiden flight. |
| [rocket_lab/iridium_acquisition.md](rocket_lab/iridium_acquisition.md) | The Rocket Lab-Iridium acquisition (announced June 29, 2026), verified: the deal terms, Iridium as an asset (constellation, spectrum, business, services), and the factual hooks and non-hooks for the cellular thesis; comms wave 9, no verdict. | Rocket Lab agreed to acquire Iridium for ~$8.0B enterprise value ($54.00/share cash-and-stock, ~24% premium, close ~mid-2027 pending FCC transfer-of-control and other approvals). Iridium is a profitable LEO satcom operator: 66-satellite Iridium NEXT with a Ka cross-link mesh and pole-to-pole coverage, a globally coordinated L-band MSS allocation (1616-1626.5 MHz), FY2025 revenue $871.7M at a 56.8% OEBITDA margin, and 2.537M billable subscribers (mostly IoT). Owning it hands RKLB a constellation, owned spectrum, ground, ~2.5M customers, and an NB-IoT NTN foothold at ~$8.0B (versus the corpus's ~$32-90B spectrum-only cost for an owned cellular position), but NOT cellular low-band, partner-MNO spectrum, or broadband-to-unmodified-phone capability: Iridium's L-band MSS is not the cellular band a phone uses. Owns COMM-601..624. |
| [rocket_lab/iridium_lband_capacity_and_modernization.md](rocket_lab/iridium_lband_capacity_and_modernization.md) | The capacity-physics layer for the Iridium max-outcome model: Iridium NEXT as built, when it needs replacing, how capacity scales if the same 8-10.5 MHz flies on a modern digital-beamforming satellite, the regulatory constraints on a larger fleet, and the narrowband headroom (comms wave 9, no verdict). | Iridium NEXT is capacity-small by 1990s design (~2.6 Mbps voice payload per satellite, ~174 Mbps fleet, device-full but bit-empty on 2M low-duty IoT), and its ~17.5-year life (a 2024 extension) means replacement is needed by ~2035, the natural Neutron hook. The core result: the SAME ~8 MHz of owned L-band on a modern large-aperture digital-beamforming satellite rises roughly three orders of magnitude to ~1.6-4.8 Gbps/sat (central ~2.9), because more, smaller beams reuse the fixed MHz many more times (spatial reuse is the multiplier, not raw bandwidth). Video-grade subscribers scale linearly with held MHz (~3,000 subs/sat/MHz), giving ~8M subscribers at 340 satellites, ~24M at 1,000, ~48M at 2,000 on 8 MHz; narrowband headroom is effectively unlimited (billions of devices). Regulatory: same-band replacement has direct precedent, but a much larger fleet or a different altitude opens PFD and coordination questions, and the held MHz (~8 vs 10.5 vs expanded) is a live FCC dispute (Iridium vs Globalstar). Owns COMM-635..660. |

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
| [synthesis/comms_wave5_coverage_spectrum_synthesis.md](synthesis/comms_wave5_coverage_spectrum_synthesis.md) | Communications wave-5 synthesis: the coverage-floor satellite count, the V3 spectrum-incorporation and fold ratio, and the spectrum dollars, assembled for the COVERAGE-FIRST broadband model (comms wave 5). | Coverage is cheap and the cost is in the spectrum, not the count. The US+Europe continuous-coverage FLOOR is ~130-450 satellites (CONUS ~50-150, near-global mid-lat ~290-960), so full coverage is a few-hundred-satellite problem distinct from the ~1,584-30,000 capacity build. A V3 incorporates a fixed ~2 GHz Ku user link and folds ~1x (mass-bound), so spectrum and beams, not user bandwidth or stow, are the differentiators. The spectrum-to-buy line is now sourced: secondary-market mid-band is ~$0.65-1.03/MHz-POP, so ~$32-46B (100 MHz) to ~$65-90B (200 MHz) US+Europe if the model chooses OWNED spectrum, the alternative to the near-zero-capex SCS lease. Sources the coverage-floor count and the spectrum dollars that the .agent comms-model briefs previously asserted chat-only. |
| [synthesis/comms_wave6_dtc_architecture_synthesis.md](synthesis/comms_wave6_dtc_architecture_synthesis.md) | Communications wave-6 synthesis: ties together the direct-to-cell antenna architecture, the gain-placement asymmetry, the Flatellite flat-body aperture, the settled Tier-1 operating point, and the coverage result, around the WIP governing DTC system model (comms wave 6). | The big antenna is on the GROUND for broadband (the customer's dish) and in ORBIT for direct-to-cell (the bare phone supplies nothing), which is the cause underneath the corpus's mass-vs-size launch asymmetry. Aperture is the service ladder, splitting into two tiers (Tier 1 ~4G-grade ~2-50 Mbps at a moderate ~25-50 m2 aperture; Tier 2 ~100+ Mbps broadband-to-phone at ~60+ m2). The Flatellite's flat body is its own ~20-25 m2 aperture (no fold, ~16/Neutron). The settled Tier-1 operating point: low orbit ~450 km, ~30 Mbps to one phone, ~25 MHz owned spectrum, and a flat ~25 m2 array clears the ~25 Mbps single-phone bar on its own. Coverage: one ~53-deg shell at ~450 km, ~100-340 satellites at 95% covers ~95% of global mobile demand (validated vs Iridium 66->78). Biggest open numbers: per-satellite capacity, spectrum lease-vs-own, per-satellite cost. No verdict. |

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

**Coverage floor (continuous-coverage floor):** the comms wave-5 term for the
MINIMUM LEO satellite count that gives a target area continuous (24/7) single
coverage, BEFORE capacity matters. A single LEO satellite covers a ~1,300-1,900 km
circle and is overhead only ~2-8 minutes per pass, so continuity is bought with a
string of satellites per orbital plane and enough planes to tile the target's
longitude span (the streets-of-coverage construction). The floor is a few hundred
satellites for the US-plus-Europe target (~130-450, with CONUS ~50-150 and a
near-global mid-latitude band ~290-960), validated against Iridium's real 66. It is
altitude- and elevation-driven: dropping 550 to 350 km or raising the mask 10 to 25
degrees each roughly doubles-to-triples it. The load-bearing point for the model: full
coverage is CHEAP (a few-hundred-satellite problem), distinct from the
~1,584-to-30,000-satellite CAPACITY build, so what a satellite buys past the floor is
capacity (Shannon times beams), not coverage.

**Bandwidth-to-capacity link (user spectrum is not the differentiator):** the comms
wave-5 finding that a Starlink generation's capacity leap is NOT a user-bandwidth
story. The broadband user link is fixed and modest (~2 GHz Ku down, ~500 MHz Ku up,
identical V1/V2/V3); a V3 reaches ~1 Tbps by reusing that SAME ~2 GHz across dozens of
fully-digital beams at ~4-4.5 bits/Hz with high spatial reuse, fed by a wide Ka plus
E-band (10 GHz) backhaul pipe. So capacity equals user-pool times spectral efficiency
times spatial reuse times satellite count, and the differentiators are beams,
backhaul, and sat-count, not the user band. The whole system incorporates >20 GHz of
licensed RF (Ka+E+V) plus license-free optical inter-satellite links.

**Fold ratio (deployed-to-stowed):** the comms wave-5 mechanical measure of how much
a satellite's aperture collapses to fit a fairing. A Starlink V3 broadband aperture
barely folds (fold ratio ~1x: the RF aperture is the flat satellite body and the
~60 m span is solar-wing-dominated), so V3 is MASS-bound and fairing-agnostic. A
direct-to-cell array folds many times (AST BlueBird Block 2 ~223 m2 is ~220-265
modular ~0.84 m2 tiles folding phone-booth-to-studio-apartment), so it is SIZE-bound
and the fold geometry is what fills the fairing. The general rule: a solar membrane
stows to ~0.01% of deployed volume but a populated RF phased array packs only to
~34-48%, so a handset-closing aperture cannot fold like a solar wing. This is the
mechanical root of the V3-versus-direct-to-cell launch-fit asymmetry.

**Spectrum-to-buy (the owned-spectrum dollar line):** the comms wave-5 term for the
secondary-market cost of acquiring cellular spectrum OUTRIGHT, the priced alternative
to the near-zero-capex SCS lease. Mid-band trades at ~$0.65-1.03/MHz-POP (no entrant
discount versus primary auctions), so a US-plus-Europe footprint costs ~$32-46B for a
~100 MHz competitive floor and ~$65-90B for a ~200 MHz incumbent-match, spectrum-only.
Whether this line enters the model depends on the access mechanism: under the SCS
lease it is a near-zero wash, but if the model chooses owned spectrum (the SpaceX-
EchoStar ~$17B/~65 MHz path) it becomes a real, sourced capital line on the order of
tens of billions.
