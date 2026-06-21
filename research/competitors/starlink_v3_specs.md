# Starlink V3 Satellite and Constellation Specifications: the modern RF broadband benchmark

*Research date: June 2026. Communications research-wiki effort. Part of the Rocket Lab orbital communications feasibility study (companion to the orbital data-center track).*

**Builds on / does not duplicate:**
- [`research/economics/comms_space_supply_cost.md`](../economics/comms_space_supply_cost.md): the per-generation unit-cost trajectory (V1 ~$200-250k / V2 mini ~$800k / V3 ~$1.2M), the per-Gbps capital-cost-down (~$10k/Gbps V2 mini to ~$1.2k/Gbps V3), replacement-capex treadmill, and the launch-share-of-system-cost split. That doc owns the COST stack; this doc owns the CAPACITY-and-physical-spec stack and feeds its capacity inputs.
- [`research/laser_comms/rf_satcom.md`](../laser_comms/rf_satcom.md): RF band table (Ku/Ka/V/W), the spectrum-coordination constraint (ITU first-come-first-served, years to coordinate), and the laser-vs-RF head-to-head. That doc owns the spectrum-regulation argument; this doc does not re-litigate it.
- [`research/laser_comms/constellation_mesh.md`](../laser_comms/constellation_mesh.md) (referenced by the cost doc): Starlink laser-mesh topology (~3 laser terminals/sat, 100 Gbps/terminal, aggregate capacity growth).

This doc is the concrete cost-and-capacity benchmark for a **modern RF broadband constellation at the technology frontier**. Starlink V3 is the relevant yardstick because it is the only at-scale system with both disclosed operating financials (the May 2026 SpaceX S-1) and a publicly described next-generation satellite. It carries no go/no-go verdict on the Rocket Lab venture. China is excluded from all market totals (no Chinese system, Guowang/Qianfan, is used as a benchmark here).

The single most important fact for the Neutron-fit question handled by another agent: **V3 is a Starship-class satellite. It is ~3.3x the mass of a V2 mini and unfolds to roughly the width of a small section of the ISS. It does not fit a Falcon-9-class or Neutron-class fairing in any useful number.** The capacity story and the launch-vehicle story are inseparable: the per-bit cost-down is bought with mass that only a very large launcher can carry.

---

## Summary / Verdict

**Confidence: medium-high** on the headline V3 capacity numbers (1 Tbps down, ~160-200 Gbps up, ~60 Tbps per launch) because SpaceX stated them publicly and many independent outlets repeat them consistently; **medium** on the exact mass and dimensions (trade-press converges on ~1,900-2,000 kg and ~60 m wingspan, but an independent satellite catalog lists a lower ~1,200 kg estimate, a real spread that is flagged); **medium** on beam counts (the well-documented figure is the V2 baseline of 48 down / 16 up; V3 beam counts are described qualitatively as "dozens" with larger digital arrays, not given as a hard SpaceX number); **medium-low** on the customers-served derivations (built here from disclosed capacity and subscriber counts, sensitive to oversubscription assumptions).

1. **Per-satellite capacity: ~1 Tbps (1,000+ Gbps) downlink and ~160-200 Gbps uplink to users, plus ~4 Tbps total including RF-plus-laser backhaul.** That is roughly **10-13x the downlink and ~3-24x the uplink of a V2 mini** depending on which V2-mini baseline you use (~80-96 Gbps down). [FACT, multi-source]

2. **Per Starship launch: ~60 Tbps added to the network from ~60 V3 satellites, "more than 20x" what one Falcon 9 V2-mini launch adds today.** This is SpaceX's own stated figure. A separate analyst extrapolation (100 sats per fully-loaded Starship → 100 Tbps) exists and is flagged as the optimistic bound. [FACT for the 60 Tbps / 60-sat figure; ESTIMATE for the 100-sat case]

3. **Constellation: the Gen2 authorization SpaceX is building toward is up to 29,988 satellites across shells at ~340-360 km, ~525-535 km, and ~604-614 km.** The FCC has approved the system in tranches (7,500 in Dec 2022, another 7,500 in 2024). V3 deploys lower, into a ~350 km very-low-Earth-orbit (VLEO) shell. [FACT, multi-source]

4. **A separate, additional 15,000-satellite V3 constellation is filed specifically for direct-to-cell** (FCC SAT-LOA-20250916-00282, Sep 2025), at ~326-335 km, targeting ~700+ Gbps per satellite of direct-to-device capacity (vs an aggregate on the order of ~7 Gbps for the V2-mini direct-to-cell generation, a claimed >100x leap). Direct-to-cell is the lead market for this project's thesis, so this filing is the most strategically relevant single data point in the doc. [FACT, single-source filing + trade press]

5. **Total current network capacity is on the order of ~450 Tbps end-2025** and rising fast; V3 is the mechanism to push it toward the multi-petabit scale. The frontier RF broadband constellation is therefore a ~10,000-satellite (broadband) plus ~15,000-satellite (direct-to-cell) system, multi-hundred-Tbps today, multi-Pbps on the V3 roadmap, serving ~12M+ broadband subscribers as of June 2026. [FACT, multi-source]

**Numbers to treat with care (flagged in the claims ledger):** the V3 mass (~1,200 kg catalog estimate vs ~1,900-2,000 kg trade press); V3 beam counts (no hard SpaceX figure, V2 baseline used as a floor); the 100-sat/100-Tbps-per-launch case (analyst extrapolation, not SpaceX); the direct-to-cell 700 Gbps/sat (a projection in an FCC filing, not demonstrated); and all customers-per-satellite math (oversubscription-dependent).

---

## 1. Per-satellite specifications

### 1.1 Capacity

| Metric | V3 value | Source / status |
|---|---|---|
| Downlink capacity to users | **~1 Tbps (1,000+ Gbps)** | [FACT, multi-source] |
| Uplink capacity to users | **~160 Gbps** (some sources state **up to 200 Gbps**) | [FACT, multi-source; the 160 vs 200 spread is real] |
| Total incl. RF + laser backhaul | **~4 Tbps per satellite** | [FACT, single primary lineage repeated] |
| Latency target | **below ~20 ms** | [FACT, single-source] |
| User-facing speed | **gigabit** to a single user (terminal hardware upgrade required) | [FACT, multi-source] |

Sources: [Tom's Hardware: V3 1 Tbps/sat, 60 Tbps/launch, gigabit to users](https://www.tomshardware.com/service-providers/network-providers/spacex-shows-off-massive-new-v3-starlink-satellites-expanded-technology-will-deliver-gigabit-internet-to-customers-for-the-first-time-and-enable-60-tera-bits-per-second-downlink-capacity); [Basenor V3 spec breakdown (1 Tbps down, 160-200 Gbps up, ~4 Tbps incl. laser, <20 ms, gigabit user speed, terminal upgrade)](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean); [DataCenterDynamics: Starlink targets 2026 for terabit satellites](https://www.datacenterdynamics.com/en/news/starlink-targets-2026-for-terabit-satellites-for-launch-with-starship/); [Universe Magazine: V3 with 1 Tbps speeds](https://universemagazine.com/en/spacex-presents-starlink-v3-satellites-with-1-tbps-speeds/).

**Note on "1 Tbps":** this is the satellite's *aggregate downlink capacity to all users in view*, shared across all its beams and all users in its footprint. It is not a per-user rate (the per-user headline is "gigabit"). Per [`rf_satcom.md`](../laser_comms/rf_satcom.md), HTS per-satellite figures are always shared, coordinated capacity, not a dedicated pipe. The ~4 Tbps "total" figure adds the satellite's laser inter-satellite links and gateway backhaul on top of the user-facing ~1 Tbps.

### 1.2 Physical: mass, size, power, propulsion

| Spec | V3 value | Source / status |
|---|---|---|
| Mass | **~1,900-2,000 kg** (trade-press consensus); **~1,200 kg** (independent catalog estimate) | [FACT/ESTIMATE; the ~1.2 t vs ~2 t spread is flagged] |
| Body / stowed dimensions | **~7-8 m long base, ~3.5 m wide** | [FACT, multi-source] |
| Deployed wingspan | **~60 m** (vs ISS ~75-109 m wide for scale) | [FACT, multi-source] |
| Solar | **dual deployable arrays, larger than prior gens** | [FACT] |
| Propulsion | **argon Hall-effect / ion thrusters** (station-keeping) | [FACT, multi-source] |
| Onboard | next-gen computers, modems, digital phased-array beamforming, switching fabric, optical ISLs | [FACT] |

Sources: [Basenor (~2,000 kg, argon Hall thrusters, larger arrays, next-gen processing)](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean); [Gunter's Space Page, Starlink Block v3.0 (independent catalog: ~1,200 kg estimate, 7 m x 3.5 m, Ku/Ka/E bands, optical ISL, argon ion thrusters, Starship-only)](https://space.skyrocket.de/doc_sdat/starlink-v2-0-ss.htm); [NextBigFuture (Gen3 unfolds to ~60 m wingspan, ISS ~75 m wide, >2 tons, 7-8 m base)](https://www.nextbigfuture.com/2024/03/spacex-starship-launched-starlink-gen-3-unfolded-nearly-as-wide-as-the-space-station.html); [NextBigFuture (V2 mini 575 kg, V3 ~1,900 kg)](https://www.nextbigfuture.com/2025/02/spacex-version-3-starship-and-version-3-starlink-both-arrive-in-2025.html).

**Mass spread, flagged.** The independent satellite catalog (Gunter's Space Page) lists ~1,200 kg with a question mark; the trade press (Basenor, NextBigFuture, Tom's Hardware) converges on ~1,900-2,000 kg. The cost doc [`comms_space_supply_cost.md`](../economics/comms_space_supply_cost.md) uses ~1,500 kg as a midpoint. The true number is unconfirmed (SpaceX has not published a datasheet), but **every estimate is several times a V2 mini (575 kg) and far beyond any Falcon-9 or Neutron-class per-satellite mass budget at useful batch sizes.** The exact value does not change that conclusion.

### 1.3 Frequency bands

| Link | Band(s) | Role |
|---|---|---|
| User downlink/uplink | **Ku-band** (~10.7-12.7 GHz down, ~14 GHz up) | Primary broadband user link |
| Gateway / feeder | **Ka-band** (~17.8-19.3 / 27-30 GHz) | Ground-station backhaul |
| Backhaul (next-gen) | **E-band** (~71-76 / 81-86 GHz) | High-capacity gateway/backhaul, new on V-class hardware |
| Inter-satellite | **Optical (laser)**, not RF | Mesh backbone, ~100 Gbps/terminal, ~3-4 terminals/sat |
| Direct-to-cell | **MSS / cellular bands**, ~1.9 GHz (EchoStar AWS-3/AWS-4/H-block, ~65 MHz US) | Direct-to-phone (separate fleet, see Section 4) |

Sources: [Gunter's Space Page (Ku, Ka, E bands; optical ISL; phased-array digital beamforming)](https://space.skyrocket.de/doc_sdat/starlink-v2-0-ss.htm); [Basenor (Ku user, Ka + E-band gateway/backhaul, phased arrays)](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean); for direct-to-cell spectrum: [NextBigFuture / FCC EchoStar 65 MHz AWS-3/AWS-4/H-block deal](https://www.nextbigfuture.com/2025/09/spacex-15000-v3-starlink-direct-to-cellphone-satellites.html), [Basenor: FCC approves SpaceX direct-to-phone 5G spectrum deal](https://www.basenor.com/blogs/news/fcc-approves-spacex-direct-to-phone-5g-spectrum-deal).

Band-by-band capacity, rain-fade tradeoffs, and the new-entrant spectrum-coordination problem are covered in [`rf_satcom.md`](../laser_comms/rf_satcom.md) and not repeated here. The relevant point for this benchmark: **V3 stays in the same Ku-user / Ka-gateway envelope as prior Starlink, adds E-band for backhaul, and gets its capacity jump from a much larger digital phased array and more spectrum reuse via more/narrower beams, not from moving users to an exotic band.** This matters for a new entrant: the capacity leap is an antenna-and-processing story (mass and power), not a free-spectrum story.

### 1.4 Beams

| Quantity | Value | Source / status |
|---|---|---|
| V2 baseline (well-documented) | **48 downlink beams, 16 uplink beams** (3 down + 1 up antennas, 8 beams x 2 polarizations) | [FACT, single technical lineage] |
| V3 | larger fully-digital phased arrays "illuminating dozens of targets simultaneously," flexible power allocation; **more beams than V2, exact count not disclosed by SpaceX** | [ESTIMATE; no hard SpaceX figure] |
| Gen2 vs Gen1 mobile arrays | **~16x the beams per satellite** (V2 vs V1, for the direct-to-cell/mobile array) | [FACT, single-source SpaceX-attributed] |

Sources: [Grokipedia-sourced search summary, V2 beam architecture (48 down / 16 up)](https://grokipedia.com/page/Starlink_V3_satellites); [SDxCentral: Gen2 ~16x beams/sat, mobile throughput >100 Gb/s down / 50 Gb/s up](https://www.sdxcentral.com/news/starlink-targets-25m-users-by-year-end-as-gen2-satellite-plan-promises-100x-data-density/); [Mike Puchol, independent Starlink capacity model (beam/cell methodology)](https://mikepuchol.com/modeling-starlink-capacity-843b2387f501).

**Beam count is the weakest-sourced spec.** SpaceX has not published a V3 beam count. The reliable anchor is the V2 architecture (48 down / 16 up). V3's contribution is a *fully digital* phased array (vs the partly analog earlier design) that can place more, narrower, dynamically-steered beams and shift power to demand. The capacity jump to ~1 Tbps is consistent with substantially more usable beams x more bandwidth per beam x more spectrum reuse, but the exact beam number is not a hard fact and is flagged.

---

## 2. The V2-to-V3 generational jump (the capacity multiple)

This is the headline the project asked for: how much bigger is V3 than the generation it replaces.

| Dimension | V2 mini | V3 | Multiple |
|---|---|---|---|
| Mass | 575 kg | ~1,900-2,000 kg | **~3.3x** |
| Downlink/sat | ~80-96 Gbps | ~1,000 Gbps | **~10-13x** |
| Uplink/sat | (V2 mobile array ~50 Gbps) | ~160-200 Gbps | **~3-4x** (vs mobile array); higher vs early V2 |
| Per Starship launch (network capacity added) | one Falcon 9 V2-mini launch ≈ ~2.5-3 Tbps | **~60 Tbps** | **>20x per launch** |
| Capital cost per Gbps of capacity | ~$10k/Gbps | ~$1.2k/Gbps | **~8x cheaper per bit** (see cost doc) |

Sources: [Tom's Hardware (V3 10x+ per-sat, 20x per-launch, 1 Tbps down)](https://www.tomshardware.com/service-providers/network-providers/spacex-shows-off-massive-new-v3-starlink-satellites-expanded-technology-will-deliver-gigabit-internet-to-customers-for-the-first-time-and-enable-60-tera-bits-per-second-downlink-capacity); [Basenor (>10x downlink, 24x uplink vs V2 gen; 60 Tbps/launch >20x)](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean); [NextBigFuture (V2 mini 575 kg, V3 ~1,900 kg, 1 Tbps down, 160 Gbps up)](https://www.nextbigfuture.com/2025/02/spacex-version-3-starship-and-version-3-starlink-both-arrive-in-2025.html); per-Gbps capital cost from [`comms_space_supply_cost.md`](../economics/comms_space_supply_cost.md).

**The clean statement of the jump: ~10x the per-satellite downlink, >20x the network capacity per launch, at ~3.3x the mass and ~8x lower capital cost per delivered bit/s.** The two multiples that differ (10x per-sat vs 20x per-launch) reconcile through the launch vehicle: Starship carries enough V3 mass that even though each V3 is "only" ~10x a V2 mini, a single Starship launch puts up far more total capacity than a single Falcon 9 can. **The generational jump is as much a launch-vehicle jump as a satellite jump.** A program without a Starship-class launcher captures the ~10x per-satellite gain only if it can fly the ~2-tonne satellite at all, and captures none of the ~20x-per-launch economics.

Note: some sources phrase the V2 mini downlink as ~80 Gbps and others as ~96 Gbps; one source frames the per-satellite leap as "96 Gbps to 1,024 Gbps" (~10.7x). The cost doc uses ~80 Gbps. The multiple is ~10-13x either way.

---

## 3. The constellation SpaceX is building (broadband Gen2)

V3 satellites populate SpaceX's second-generation (Gen2) authorization. The constellation structure is set by the FCC filings, which are authoritative on counts, shells, altitudes, and inclinations.

| Constellation parameter | Value | Source / status |
|---|---|---|
| Gen2 satellites requested | **29,988** (filed May 26, 2020, range 328-614 km) | [FACT] |
| Shell: ~525-535 km | **~10,000 sats** (525 km / 53 deg, 530 km / 43 deg, 535 km / 33 deg) | [FACT] |
| Shell: ~340-360 km | **~20,000 sats** (lower, VLEO) | [FACT] |
| Shell: ~604-614 km | **~500 sats** | [FACT] |
| FCC approval, tranche 1 | **7,500 sats** (Dec 1, 2022 order, at 525/530/535 km) | [FACT] |
| FCC approval, tranche 2 | **+7,500 sats** (2024, lower shells ~340-365 km and ~475-485 km) | [FACT] |
| V3 deployment shell | **~350 km** (VLEO, lower than the current ~550 km operational shell) | [FACT, multi-source] |

Sources: [SpaceNews: FCC partial approval of Starlink Gen2 (29,988 requested; 7,500 approved Dec 2022; shells 525/530/535 km at 53/43/33 deg)](https://spacenews.com/fcc-grants-partial-approval-for-starlink-second-generation-constellation/); [DataCenterDynamics: FCC approves Gen2 7,500](https://www.datacenterdynamics.com/en/news/fcc-approves-spacexs-starlink-gen2-application-for-7500-satellites/); [FCC-22-91 Gen2 order (primary)](https://docs.fcc.gov/public/attachments/FCC-22-91A1.pdf); [Tom's Hardware: FCC approves +7,500 Gen2 at lower shells ~340-365 / 475-485 km](https://www.tomshardware.com/tech-industry/fcc-approves-7500-additional-starlink-gen2-satellites); [Basenor: V3 deploys at ~350 km VLEO](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean).

**Why V3 goes lower (~350 km).** A lower orbit shortens the path, which (a) cuts latency toward the <20 ms target, (b) raises usable capacity per unit spectrum (stronger link budget, tighter beams, more frequency reuse over a smaller footprint), and (c) means faster natural deorbit at end of life (less debris liability). The cost is that lower satellites cover less ground each, so **more satellites are needed for global coverage**, which is exactly why the Gen2 plan is ~30,000 satellites versus ~4,400 for Gen1. The VLEO shell is a deliberate capacity-density-over-coverage-efficiency trade enabled by cheap Starship launch. (Orbit-altitude tradeoffs are developed in [`research/orbital/higher_orbit_tradeoffs_lifetime.md`](../orbital/higher_orbit_tradeoffs_lifetime.md); not repeated here.)

### 3.1 Total system throughput today and on the V3 roadmap

| Quantity | Value | Source / status |
|---|---|---|
| Current aggregate network capacity | **~450 Tbps** (end-2025), up from ~5.6 Tbps early 2024 | [FACT, multi-source] |
| Capacity added per V3 Starship launch | **~60 Tbps** (60 sats) | [FACT] |
| V3 roadmap implication | a few dozen Starship V3 launches add multiple Pbps; system heads toward **multi-petabit** scale | [DERIVED] |
| Operational satellites (all gens) | **~9,500** (of ~10,700 in orbit, ~12,300 launched cumulatively) | [FACT, June 2026] |

Sources: [DISHYtech: ~450 Tbps end-2025, ~5 Tbps/week additions](https://www.dishytech.com/starlink-just-had-a-massive-2025-and-2026-could-be-even-bigger/); [`comms_space_supply_cost.md`](../economics/comms_space_supply_cost.md) (fleet counts, ~450 Tbps); [Tom's Hardware (60 Tbps/launch)](https://www.tomshardware.com/service-providers/network-providers/spacex-shows-off-massive-new-v3-starlink-satellites-expanded-technology-will-deliver-gigabit-internet-to-customers-for-the-first-time-and-enable-60-tera-bits-per-second-downlink-capacity).

**Derivation [DERIVED].** At ~60 Tbps per Starship launch, ~17 V3 launches add ~1 Pbps. Even at a modest early V3 cadence (say ~20-40 Starship launches across 2026-2027), the system roughly doubles to triples its end-2025 ~450 Tbps and pushes past 1 Pbps. The exact pace depends entirely on Starship cadence (covered in [`research/competitors/starship_addendum.md`](starship_addendum.md): Starship V3 first flew with dummy payloads May 22, 2026; "weekly" cadence is a long-horizon goal, not yet demonstrated). The capacity ceiling is set by spectrum (Shannon) reused across beams and orbits, not by satellite count alone.

---

## 4. The direct-to-cell V3 constellation (the lead-market benchmark)

Direct-to-cell is this project's lead market, so SpaceX's dedicated V3 direct-to-cell filing is the most strategically pointed data in this doc. It is a *separate, additional* constellation from the broadband Gen2 fleet.

| Parameter | Value | Source / status |
|---|---|---|
| Filing | **FCC SAT-LOA-20250916-00282**, filed Sep 16, 2025 | [FACT, single-source filing] |
| Satellites | **up to 15,000** additional V3 satellites, dedicated to direct-to-cell | [FACT] |
| Altitude | **~326-335 km**, ~53 deg inclination | [FACT] |
| Direct-to-cell capacity per sat (target) | **~700+ Gbps** | [ESTIMATE/PROJECTION, filing] |
| Improvement vs V2 direct-to-cell | **>100x** (from an aggregate on the order of ~7 Gbps for the V2-mini D2C generation) | [ESTIMATE] |
| V2-mini direct-to-cell baseline | **48 beams x ~7 Mbps** per beam (a fronthaul-limited ~0.3 Gbps usable, ~7 Gbps aggregate cited) | [FACT/ESTIMATE, single technical lineage] |
| User experience target | **4G-LTE-equivalent**: up to ~100 Mbps peak, ~2-10 Mbps sustained | [FACT, filing] |
| Spectrum | **~65 MHz** nationwide from EchoStar (15 MHz AWS-3, 40 MHz AWS-4, 10 MHz H-block), ~1.9 GHz, FCC-approved May 12, 2026 | [FACT, multi-source] |
| Total V3 plan (broadband + D2C) | **~44,988** V3 satellites (29,988 broadband + 15,000 D2C) | [DERIVED from the two filings] |

Sources: [NextBigFuture: 15,000 V3 direct-to-cell sats, FCC SAT-LOA-20250916-00282, ~700 Gbps/sat, 326-335 km, MSS bands ~1.9 GHz, >100x vs V2 D2C](https://www.nextbigfuture.com/2025/09/spacex-15000-v3-starlink-direct-to-cellphone-satellites.html); [Basenor: FCC approves SpaceX direct-to-phone 5G spectrum deal (~65 MHz EchoStar: 15 AWS-3 + 40 AWS-4 + 10 H-block)](https://www.basenor.com/blogs/news/fcc-approves-spacex-direct-to-phone-5g-spectrum-deal); [thexlab.org Starlink capacity working paper (V2 D2C fronthaul ~48 beams x 7 Mbps)](https://thexlab.org/wp-content/uploads/2025/07/Starlink_Analysis_Working_Paper_v0.2.pdf); [SDxCentral: Gen2 mobile ~16x beams, ~100 Gb/s down / 50 Gb/s up, 150 Mbps/user peak](https://www.sdxcentral.com/news/starlink-targets-25m-users-by-year-end-as-gen2-satellite-plan-promises-100x-data-density/).

**Why this is the benchmark that matters for the thesis.** The project's working view is that direct-to-cell is likely a larger market than home broadband and may cannibalize it. SpaceX is making exactly that bet structurally: it filed for a **15,000-satellite dedicated direct-to-cell fleet** on top of broadband, bought ~65 MHz of clean terrestrial cellular spectrum (the EchoStar deal) to escape the MSS-power constraints that capped V2 direct-to-cell, and is targeting genuine 4G/LTE-class service (not just SMS/emergency). The per-satellite direct-to-cell capacity leap (~7 Gbps-class aggregate to ~700 Gbps/sat) is the direct-to-cell analogue of the broadband ~10x jump. The spectrum point is decisive and connects to [`rf_satcom.md`](../laser_comms/rf_satcom.md): SpaceX did not win this capacity by getting free spectrum, it *bought* a nationwide cellular block. A new entrant's direct-to-cell capacity ceiling is a spectrum-acquisition problem first and a satellite problem second.

---

## 5. How many customers could it serve

This is intrinsically a [DERIVED] section: SpaceX does not publish a customers-per-satellite figure, and the answer depends on oversubscription (residential broadband is sold many-to-one against peak capacity). Three independent angles are shown so the lead can pick an assumption.

**Angle A: top-down from disclosed subscribers and capacity.** ~12M+ active subscribers (June 2026) are served by ~9,500 operational satellites and ~450 Tbps of aggregate capacity. That is **~1,260 subscribers per operational satellite** and **~37.5 Mbps of aggregate network capacity per subscriber** on average across the fleet today [DERIVED]. On a V3 satellite at ~1 Tbps, the same ~1,260-subs/sat loading would imply ~790 Mbps aggregate per subscriber, i.e. **V3 multiplies headroom per subscriber by ~10x or lets one V3 carry ~10x the subscribers of the fleet average** at constant per-user experience.

Sources for the inputs: [Basenor: Starlink hits 12M active customers, 160+ countries (June 2026)](https://www.basenor.com/blogs/news/starlink-hits-12-million-active-customers-across-160-countries); [Yahoo/Finance: 12M customers across 160 countries](https://finance.yahoo.com/markets/stocks/articles/spacex-starlink-surpasses-12m-customers-000951284.html); fleet counts and ~450 Tbps from [`comms_space_supply_cost.md`](../economics/comms_space_supply_cost.md).

**Angle B: bottom-up from a beam/cell model.** An independent technical analysis models a Starlink cell at **~672 Mbps capacity serving ~296 subscribers** (an early-generation, oversubscribed figure). Scaling a single cell's capacity to V3's larger per-satellite throughput, and holding the same per-subscriber experience, a V3 satellite's ~1 Tbps could serve **very roughly ~5,000-15,000 subscribers** depending on oversubscription and how concentrated they are [DERIVED, wide band]. The width of that band is the point: it is set by assumptions, not physics.

Sources: [Mike Puchol, independent Starlink capacity model](https://mikepuchol.com/modeling-starlink-capacity-843b2387f501); [SatMagazine bandwidth-of-the-constellation analysis (per-cell capacity, subscriber-per-cell)](http://www.satmagazine.com/story.php?number=1026762698).

**Angle C: the structural caveat (the load-bearing one).** Per [`comms_space_supply_cost.md`](../economics/comms_space_supply_cost.md), a satellite beam serves a *fixed pool of capacity over a fixed ground footprint*, so **cost-per-user rises with user density**, the opposite of fiber. "Customers per satellite" is therefore not a single number: it is high where users are sparse (rural/remote, where one satellite's footprint holds few people) and capacity-bound where users concentrate (a city's worth of demand cannot all be served by the handful of satellites over it at once). The ~1,260-subs/sat fleet average is dominated by the fact that most of the planet (and most of Starlink's coverage) is sparsely populated. **V3's ~10x capacity raises the density ceiling by ~10x but does not remove it.** This is the single most important structural fact for the Rocket Lab thesis: a space constellation's customer count is capacity-and-geography-bound, and the binding constraint in dense markets is shared spectrum (Shannon), not satellite count.

**Net for the model:** use **~1,000-1,500 subscribers per current-gen satellite** and **~5,000-15,000 per V3 satellite** as planning bands, always with the density caveat, and treat aggregate capacity (Tbps) divided by target per-user experience (Mbps) as the real ceiling rather than any fixed subs-per-satellite constant.

---

## 6. Starship-class design (the Neutron-fit handoff)

Flagged explicitly for the separate Neutron-fit agent. **This doc establishes only the satellite's physical envelope; it does not assess Neutron.**

- **Mass: ~1,900-2,000 kg per satellite** (trade press), ~1,200-1,500 kg on lower estimates. Every estimate is **~3.3x a V2 mini (575 kg)**.
- **Deployed wingspan ~60 m**, stowed on a ~7-8 m x ~3.5 m body, deployed flat-pack ("PEZ dispenser") from Starship.
- **Designed Starship-only.** Independent catalog and trade press both state Starship is the *only* vehicle intended to carry V3, because the satellite's mass and stowed volume do not close on Falcon 9. A fully-loaded Starship is described as carrying **~60 V3 (SpaceX) up to ~100 V3 (analyst extrapolation at ~200 t/launch)** per flight.
- **Implication for the Neutron question (stated, not assessed here):** Neutron's payload class (~13 t to LEO, ~3 m fairing) is far below a Starship's, so the *number* of ~2-tonne V3-class satellites a Neutron could carry per launch is small, and the >20x-per-launch economics that depend on Starship batch size do not transfer. The per-satellite ~10x capacity gain is a satellite-design gain that in principle any launcher able to fly the satellite could carry, but the launch *economics* of the V3 generation are Starship-bound. The detailed fairing/mass fit is the other agent's task.

Sources: [NextBigFuture (Gen3 ~60 m wingspan, ~200 t/launch → ~100 sats, deployed footprint 60 m x 700 m)](https://www.nextbigfuture.com/2024/03/spacex-starship-launched-starlink-gen-3-unfolded-nearly-as-wide-as-the-space-station.html); [Gunter's Space Page (Starship the only vehicle for the 2nd-gen satellites)](https://space.skyrocket.de/doc_sdat/starlink-v2-0-ss.htm); [Converge Digest: Starship PEZ dispenser unlocks multi-Tbps Starlink](https://convergedigest.com/starships-pez-dispenser-unlocks-starlinks-multi-tbps-future/); Starship status from [`research/competitors/starship_addendum.md`](starship_addendum.md).

---

## 7. Deployment status (June 2026)

- **Starship V3 first flight: May 22, 2026**, carrying ~20 dummy Starlink-simulator satellites (plus a pair of modified observation satellites); no operational V3 deployed yet. [FACT]
- **Operational V3 deployment: targeted H2 2026**, gated by Starship cadence and FCC clearance. [FACT, multi-source]
- **Gigabit user speeds require a terminal hardware upgrade**; existing dishes cannot exploit the full V3 downlink. [FACT, multi-source]

Sources: [Basenor (Starship V3 debut May 22, 2026 with dummy sats; operational V3 H2 2026)](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean); [DataCenterDynamics (2026 target for terabit sats on Starship)](https://www.datacenterdynamics.com/en/news/starlink-targets-2026-for-terabit-satellites-for-launch-with-starship/); [`research/competitors/starship_addendum.md`](starship_addendum.md) (Flight 12 / Block 3 status, dummy-payload deploy test).

This matches the cost doc's flag: the V3 ~$1.2k/Gbps and ~60 Tbps/launch figures are **projections over a vehicle that first flew V3-class in May 2026 with dummy payloads**. The capacity numbers are SpaceX's design targets; none of the V3 numbers in this doc are yet demonstrated in revenue service.

---

## 8. What this benchmark gives the model

1. **A concrete frontier RF capacity point:** ~1 Tbps/sat down, ~160-200 Gbps up, ~60 Tbps per launch, ~450 Tbps system today heading to multi-Pbps. This is the capacity yardstick any Rocket Lab RF concept is measured against.
2. **The generational-jump shape:** ~10x per-satellite capacity per generation, bought with ~3.3x mass and a ~10x-cheaper-per-bit launch, i.e. capacity-per-dollar improves ~8x per generation. The engine of the cost-down is mass on a cheap heavy launcher (cross-reference the cost doc).
3. **The direct-to-cell benchmark for the lead market:** a 15,000-satellite dedicated fleet, ~700 Gbps/sat target, enabled by *buying* ~65 MHz of cellular spectrum. Direct-to-cell capacity is spectrum-bound first.
4. **The customer-count discipline:** there is no fixed subs-per-satellite; aggregate-Tbps-over-per-user-Mbps is the ceiling, and it is geography-dependent (cheap where sparse, capacity-bound where dense). This is the structural fact that governs how the per-subscriber cost model behaves.
5. **The launch-vehicle coupling for Neutron-fit:** the per-launch economics of the V3 generation are Starship-bound; a mass-limited launcher captures little of them. (Fit assessment is another agent's task.)

---

## Open questions / uncertainties

- **True V3 mass.** ~1,200 kg (catalog) vs ~1,900-2,000 kg (trade press) is a ~1.6x spread that matters for any launch-fit math. No SpaceX datasheet exists.
- **V3 beam count.** No hard SpaceX figure; only the V2 baseline (48 down / 16 up) and qualitative "dozens, fully digital." The capacity-per-beam x beam-count decomposition of the ~1 Tbps is not publicly pinned.
- **Realized vs design capacity.** ~1 Tbps and ~60 Tbps/launch are design targets; demonstrated V3 in-service capacity is zero as of June 2026. Usable/sellable capacity is typically well below theoretical (the independent models show a large theoretical-to-usable gap).
- **Direct-to-cell 700 Gbps/sat.** A projection in an FCC filing, not demonstrated; the V2 D2C baseline (~7 Gbps aggregate) is itself a single technical lineage.
- **Per-launch sat count.** SpaceX says ~60 V3/launch (→60 Tbps); an analyst extrapolation says ~100/launch at ~200 t (→100 Tbps). The gap is Starship-payload-realization-dependent.
- **Customers per satellite.** Oversubscription and user geography dominate; the ~5,000-15,000/V3-sat band is wide by nature and should be treated as a planning range, not a fact.

---

## Claims ledger

For the catalog step to ingest (no COMM- IDs assigned here). Each hard claim with its two-or-more independent sources.

1. **V3 per-satellite downlink capacity ~1 Tbps (1,000+ Gbps).** [FACT] Sources: [Tom's Hardware](https://www.tomshardware.com/service-providers/network-providers/spacex-shows-off-massive-new-v3-starlink-satellites-expanded-technology-will-deliver-gigabit-internet-to-customers-for-the-first-time-and-enable-60-tera-bits-per-second-downlink-capacity), [Basenor](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean), [DataCenterDynamics](https://www.datacenterdynamics.com/en/news/starlink-targets-2026-for-terabit-satellites-for-launch-with-starship/).

2. **V3 per-satellite uplink ~160-200 Gbps to users.** [FACT] Sources: [Basenor (160-200 Gbps)](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean), [SDxCentral / Starlink statement (200 Gbps up)](https://www.sdxcentral.com/news/starlink-targets-25m-users-by-year-end-as-gen2-satellite-plan-promises-100x-data-density/), [NextBigFuture (160 Gbps)](https://www.nextbigfuture.com/2025/02/spacex-version-3-starship-and-version-3-starlink-both-arrive-in-2025.html).

3. **V3 total capacity incl. RF + laser backhaul ~4 Tbps/sat.** [FACT, single primary lineage] Sources: [Basenor](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean), [NextBigFuture D2C piece (~4 Tbps combined RF/laser)](https://www.nextbigfuture.com/2025/09/spacex-15000-v3-starlink-direct-to-cellphone-satellites.html).

4. **~60 Tbps of network capacity added per Starship V3 launch (~60 sats), >20x a Falcon 9 V2-mini launch.** [FACT] Sources: [Tom's Hardware](https://www.tomshardware.com/service-providers/network-providers/spacex-shows-off-massive-new-v3-starlink-satellites-expanded-technology-will-deliver-gigabit-internet-to-customers-for-the-first-time-and-enable-60-tera-bits-per-second-downlink-capacity), [Basenor](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean), [Universe Magazine](https://universemagazine.com/en/spacex-presents-starlink-v3-satellites-with-1-tbps-speeds/).

5. **Alternative per-launch case: ~100 V3 sats / ~100 Tbps at ~200 t Starship payload.** [ESTIMATE, analyst extrapolation] Sources: [NextBigFuture 2024](https://www.nextbigfuture.com/2024/03/spacex-starship-launched-starlink-gen-3-unfolded-nearly-as-wide-as-the-space-station.html), [NextBigFuture 2025](https://www.nextbigfuture.com/2025/02/spacex-version-3-starship-and-version-3-starlink-both-arrive-in-2025.html).

6. **V3 mass ~1,900-2,000 kg (trade press); ~1,200 kg (independent catalog estimate); ~3.3x a V2 mini (575 kg).** [FACT/ESTIMATE, spread flagged] Sources: [Basenor (~2,000 kg)](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean), [NextBigFuture (~1,900 kg)](https://www.nextbigfuture.com/2025/02/spacex-version-3-starship-and-version-3-starlink-both-arrive-in-2025.html), [Gunter's Space Page (~1,200 kg)](https://space.skyrocket.de/doc_sdat/starlink-v2-0-ss.htm).

7. **V3 deployed wingspan ~60 m, stowed body ~7-8 m x ~3.5 m.** [FACT] Sources: [NextBigFuture (60 m wingspan, ISS ~75 m)](https://www.nextbigfuture.com/2024/03/spacex-starship-launched-starlink-gen-3-unfolded-nearly-as-wide-as-the-space-station.html), [Gunter's Space Page (7 m x 3.5 m)](https://space.skyrocket.de/doc_sdat/starlink-v2-0-ss.htm), [Basenor (7-8 m base)](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean).

8. **V3 frequency bands: Ku user, Ka + E-band gateway/backhaul, optical inter-satellite links.** [FACT] Sources: [Gunter's Space Page (Ku, Ka, E; optical ISL)](https://space.skyrocket.de/doc_sdat/starlink-v2-0-ss.htm), [Basenor (Ku user, Ka/E gateway)](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean).

9. **V3 propulsion: argon Hall-effect / ion thrusters.** [FACT] Sources: [Basenor (argon Hall thrusters)](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean), [Gunter's Space Page (argon ion thrusters)](https://space.skyrocket.de/doc_sdat/starlink-v2-0-ss.htm).

10. **V2 beam baseline: 48 downlink / 16 uplink beams (3 down + 1 up antennas, 8 beams x 2 pol).** [FACT, single technical lineage + corroboration] Sources: [Grokipedia-sourced summary](https://grokipedia.com/page/Starlink_V3_satellites), [SDxCentral (Gen2 ~16x beams vs V1)](https://www.sdxcentral.com/news/starlink-targets-25m-users-by-year-end-as-gen2-satellite-plan-promises-100x-data-density/).

11. **Generational jump: ~10x per-sat downlink and >20x per-launch network capacity at ~3.3x mass.** [FACT/DERIVED] Sources: [Tom's Hardware](https://www.tomshardware.com/service-providers/network-providers/spacex-shows-off-massive-new-v3-starlink-satellites-expanded-technology-will-deliver-gigabit-internet-to-customers-for-the-first-time-and-enable-60-tera-bits-per-second-downlink-capacity), [Basenor (>10x down, 24x up)](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean), [`comms_space_supply_cost.md`](../economics/comms_space_supply_cost.md) (~8x cheaper per Gbps).

12. **Gen2 constellation: 29,988 satellites requested (filed May 2020), shells ~340-360 km (~20,000), ~525-535 km (~10,000), ~604-614 km (~500).** [FACT] Sources: [SpaceNews](https://spacenews.com/fcc-grants-partial-approval-for-starlink-second-generation-constellation/), [FCC-22-91 order](https://docs.fcc.gov/public/attachments/FCC-22-91A1.pdf), [DataCenterDynamics](https://www.datacenterdynamics.com/en/news/fcc-approves-spacexs-starlink-gen2-application-for-7500-satellites/).

13. **FCC Gen2 approvals: 7,500 (Dec 2022) + 7,500 (2024) at progressively lower shells.** [FACT] Sources: [SpaceNews (Dec 2022, 7,500 at 525/530/535 km)](https://spacenews.com/fcc-grants-partial-approval-for-starlink-second-generation-constellation/), [Tom's Hardware (+7,500 at ~340-365 / 475-485 km)](https://www.tomshardware.com/tech-industry/fcc-approves-7500-additional-starlink-gen2-satellites).

14. **V3 deploys into a ~350 km VLEO shell (lower than the ~550 km operational shell).** [FACT] Sources: [Basenor (~350 km)](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean), [SpaceNews / FCC (lower Gen2 shells 340-360 km)](https://spacenews.com/fcc-grants-partial-approval-for-starlink-second-generation-constellation/).

15. **Current aggregate network capacity ~450 Tbps (end-2025), up from ~5.6 Tbps early 2024.** [FACT] Sources: [DISHYtech](https://www.dishytech.com/starlink-just-had-a-massive-2025-and-2026-could-be-even-bigger/), [`comms_space_supply_cost.md`](../economics/comms_space_supply_cost.md).

16. **Operational fleet ~9,500 satellites of ~10,700 in orbit (~12,300 launched cumulatively), June 2026.** [FACT] Sources: [`comms_space_supply_cost.md`](../economics/comms_space_supply_cost.md), [HighSpeedInternet satellite count](https://www.highspeedinternet.com/resources/how-many-starlink-satellites-are-in-orbit-june-12-2026).

17. **~12M+ active Starlink subscribers across 160+ countries (June 2026).** [FACT] Sources: [Basenor (12M, June 4 2026)](https://www.basenor.com/blogs/news/starlink-hits-12-million-active-customers-across-160-countries), [Yahoo Finance (12M, 160 countries)](https://finance.yahoo.com/markets/stocks/articles/spacex-starlink-surpasses-12m-customers-000951284.html).

18. **Direct-to-cell V3 fleet: up to 15,000 satellites (FCC SAT-LOA-20250916-00282, Sep 2025) at ~326-335 km, ~700+ Gbps/sat target, >100x V2 D2C.** [FACT for the filing/count; ESTIMATE for 700 Gbps] Sources: [NextBigFuture](https://www.nextbigfuture.com/2025/09/spacex-15000-v3-starlink-direct-to-cellphone-satellites.html), [Applying AI (FCC greenlights 15,000 D2C sats)](https://applyingai.com/2026/01/fcc-greenlights-spacexs-ambitious-starlink-expansion-to-15000-satellites-for-global-direct-to-cell-coverage/).

19. **Direct-to-cell spectrum: ~65 MHz from EchoStar (15 AWS-3 + 40 AWS-4 + 10 H-block), ~1.9 GHz, FCC-approved May 12, 2026.** [FACT] Sources: [Basenor (EchoStar deal, 65 MHz breakdown)](https://www.basenor.com/blogs/news/fcc-approves-spacex-direct-to-phone-5g-spectrum-deal), [NextBigFuture (1.91-1.995 GHz, EchoStar)](https://www.nextbigfuture.com/2025/09/spacex-15000-v3-starlink-direct-to-cellphone-satellites.html).

20. **V2-mini direct-to-cell baseline: 48 beams x ~7 Mbps (fronthaul-limited), ~7 Gbps aggregate class.** [FACT/ESTIMATE, single lineage] Sources: [thexlab.org capacity working paper](https://thexlab.org/wp-content/uploads/2025/07/Starlink_Analysis_Working_Paper_v0.2.pdf), [NextBigFuture (>100x from ~7 Gbps to 700+ Gbps)](https://www.nextbigfuture.com/2025/09/spacex-15000-v3-starlink-direct-to-cellphone-satellites.html).

21. **Subscribers per satellite (fleet average) ~1,260; ~37.5 Mbps aggregate capacity per subscriber.** [DERIVED] Inputs: ~12M subs / ~9,500 op sats; ~450 Tbps / ~12M subs. Sources for inputs: [Basenor subscribers](https://www.basenor.com/blogs/news/starlink-hits-12-million-active-customers-across-160-countries), [`comms_space_supply_cost.md`](../economics/comms_space_supply_cost.md) (fleet, capacity).

22. **Per-cell/per-subscriber bottom-up anchor: ~672 Mbps cell serving ~296 subscribers (early-gen, oversubscribed).** [ESTIMATE] Sources: [SatMagazine constellation-bandwidth analysis](http://www.satmagazine.com/story.php?number=1026762698), [Mike Puchol capacity model](https://mikepuchol.com/modeling-starlink-capacity-843b2387f501).

23. **Starship V3 first flight May 22, 2026 (dummy payloads); operational V3 targeted H2 2026; gigabit user speeds need a terminal upgrade.** [FACT] Sources: [Basenor (debut May 22, 2026; H2 2026 operational; terminal upgrade)](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean), [`research/competitors/starship_addendum.md`](starship_addendum.md) (Flight 12 / Block 3, 22-sat deploy test), [DataCenterDynamics (2026 terabit-sat target)](https://www.datacenterdynamics.com/en/news/starlink-targets-2026-for-terabit-satellites-for-launch-with-starship/).

24. **V3 is designed Starship-only; mass and stowed volume do not close on Falcon 9.** [FACT] Sources: [Gunter's Space Page (Starship the only vehicle for 2nd-gen sats)](https://space.skyrocket.de/doc_sdat/starlink-v2-0-ss.htm), [Basenor (Starship-only economics)](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean), [Converge Digest (Starship PEZ dispenser)](https://convergedigest.com/starships-pez-dispenser-unlocks-starlinks-multi-tbps-future/).
