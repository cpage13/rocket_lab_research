# The Space Supply-Side Cost Stack to Deliver Communications

*Research date: June 2026. Communications research-wiki effort, wave 3 (shared library).*

**Builds on / does not duplicate:**
- [`research/laser_comms/optical_ground_stations.md`](../laser_comms/optical_ground_stations.md) (optical ground-segment capex: ~$3-5M per OGS, ~$100-500M per hub network; the "downlink deficit")
- [`research/laser_comms/constellation_mesh.md`](../laser_comms/constellation_mesh.md) (Starlink topology: ~9,000+ sats, ~3 laser terminals each, 100 Gbps/terminal, ~5.6 Tbps aggregate in early 2024; ISL ranges)
- [`research/laser_comms/rf_limited_service.md`](../laser_comms/rf_limited_service.md) (capacity per RF beam: ~0.2-3 Gbps from a 100-250 MHz sliver; the large-antenna advantage; spectrum cost is "years and money")
- [`research/rocket_lab/neutron/launch_cost_economics.md`](../rocket_lab/neutron/launch_cost_economics.md) (Neutron internal cost ~$25M low cadence, ~$13.5M high cadence; Falcon 9 internal ~$11-20M; $/kg benchmarks)
- [`research/competitors/falcon9_cadence_ramp.md`](../competitors/falcon9_cadence_ramp.md) (Falcon 9 cadence ramp; Falcon 9 second stage always expendable; reuse history)

This doc is the SPACE side of the ground-vs-space delivery-cost ratio. It builds the all-in cost to DELIVER communications from orbit, using Starlink as the benchmark because it is the only mega-constellation with disclosed financials (the May 2026 SpaceX IPO S-1). It carries no go/no-go verdict on the Rocket Lab venture. It is written neutrally for any track to pull from. China is excluded except as a noted aside.

---

## Summary / Verdict

**Confidence: medium-high** on the incumbent's disclosed financials (the SpaceX S-1 is an audited filing, cross-checked across multiple readers); **medium** on the per-satellite unit costs (estimated, not disclosed; multiple converging third-party estimates); **medium** on the derived per-subscriber and per-GB cost stack (built here from disclosed revenue/EBITDA plus estimated capex inputs); **low-medium** on the conservative new-entrant case (a small constellation cannot reach Starlink's amortization scale and the numbers are model-dependent).

The space cost to deliver communications is **dominated by two things: the satellite fleet (built and continuously replaced on a ~5-year life) and the launches to put it there.** Ground segment and operations are real but second-order. The headline numbers, all for the mature SpaceX-scale incumbent:

1. **Per subscriber, the mature incumbent delivers for roughly $480-680/yr all-in and charges roughly $790/yr** (ARPU ~$66/mo in Q1 2026), at a disclosed **~38.6% segment operating margin** and **~63% segment adjusted EBITDA margin** on $11.4B of 2025 Starlink revenue [FACT, S-1]. The all-in delivery cost is therefore on the order of **$480-490/subscriber/yr** (revenue minus operating income), of which the **space-specific capital-and-launch replacement piece is roughly $200-260/subscriber/yr** [DERIVED/ESTIMATE]. This is the mature, fully-scaled floor, not the early-build cost.

2. **Per GB, the space delivery cost is cheap at the network level and expensive at the capacity-constrained edge.** At network scale the marginal cost of bulk delivered data is on the order of **$0.05-0.30/GB** [ESTIMATE], well below the ~$0.50/GB that Starlink's metered Roam plans charge [FACT]. But this average is an illusion where users concentrate: a satellite beam serves a fixed pool of capacity over a fixed ground footprint, so **cost-per-user rises with user density**, the exact opposite of terrestrial fiber/cable economics. This is the single most important structural difference and it caps how cheaply space can ever serve a dense market.

3. **The build is enormous and front-loaded; the steady state is a replacement treadmill.** Cumulative Starlink constellation capex is on the order of **$15-25B+** through 2024 [ESTIMATE], and steady-state **satellite-replacement capex runs ~$6-8B/yr** at ~1,000-2,000 sats replaced per year on the 5-year life [ESTIMATE]. Launch is **20-40% of system capital** depending on the cost case; the satellites are the larger share.

4. **For a new entrant at small scale, the per-subscriber economics are far worse.** Without Starlink's tens-of-millions-of-subscribers denominator, the same fixed constellation-plus-launch capital spreads over far fewer users, so the conservative new-entrant delivered cost is **multiples higher per subscriber** than the mature incumbent. Scale is the whole game on the space side.

**Single-source / soft figures the lead should double-check** (flagged in the claims table): the ~$6-8B/yr satellite-replacement capex and the ~1,000 sats/yr replacement rate (one analyst lineage, Motley Fool); the cumulative ~$15-25B constellation capex (a reconstructed estimate, not a disclosed line); the V1 ~$200-250k / V2 mini ~$800k / V3 ~$1.2M per-satellite costs (Quilty Space estimates, not SpaceX disclosures, and two source lineages disagree by ~2x on V2); and the derived per-GB cost (depends on assumed utilization of disclosed capacity).

---

## 1. Constellation capex: the satellite fleet is the largest line

### 1.1 Per-satellite unit cost trajectory (Starlink as the benchmark)

SpaceX does not disclose per-satellite cost. The figures below are third-party estimates (principally Quilty Space, repeated across trade press). **Two source lineages disagree by roughly 2x on the V2 mini**, which is flagged.

| Generation | Mass | Estimated unit cost | Capacity (downlink) | Notes |
|---|---|---|---|---|
| **V1 / V1.5** (2019-2022) | ~260-295 kg | **~$200-250k** (one lineage); ~$500k-1M early (another) | ~17-20 Gbps | First-gen; cost fell fast with volume [ESTIMATE] |
| **V2 mini** (2023-2025) | ~730-800 kg | **~$800k** (Quilty); ~$250k (alt lineage) | ~80 Gbps | Larger, more capable; the ~2x source disagreement lives here [ESTIMATE] |
| **V3** (2026+) | ~1,500 kg | **~$1.2M** (Quilty projection) | **~1 Tbps** down, 160-200 Gbps up; ~4 Tbps incl. laser backhaul | Starship-class; ~12x the per-sat capacity of V2 mini [ESTIMATE/PROJECTION] |

Sources: [Quilty/SpaceNews via NextBigFuture](https://www.nextbigfuture.com/2025/08/starlink-is-now-the-spacex-cash-machine.html), [Planet Tech News (~$250k)](https://www.planettechnews.com/spacex-starlink-satellites-could-cost-250000-each-and-falcon-9-costs-less-than-30-million/), [Tom's Hardware (V3 60 Tbps/launch, 1 Tbps/sat)](https://www.tomshardware.com/service-providers/network-providers/spacex-shows-off-massive-new-v3-starlink-satellites-expanded-technology-will-deliver-gigabit-internet-to-customers-for-the-first-time-and-enable-60-tera-bits-per-second-downlink-capacity), [Basenor V3 specs](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean).

**The key trend: cost per satellite rises across generations, but cost per delivered bit/s falls sharply.** A V2 mini at ~$800k delivers ~80 Gbps (~$10k per Gbps); a V3 at ~$1.2M delivers ~1,000 Gbps (~$1.2k per Gbps). That ~8x improvement in capital efficiency per unit of capacity, generation over generation, is the engine of the whole cost-down story. It depends on a heavier, cheaper-per-kg launch vehicle (Starship for V3); a mass-limited launcher cannot fly the high-capacity satellites that drive the per-bit cost down.

### 1.2 Fleet size and full constellation capex

| Quantity | Value | Source / status |
|---|---|---|
| Satellites launched (cumulative) | **12,318** | June 2026 [FACT] |
| Satellites in orbit | **~10,676** | June 2026 [FACT] |
| Operational satellites | **~9,542** | June 2026 [FACT] |
| Laser terminals per satellite | **~3** | [FACT, constellation_mesh.md] |
| Aggregate network capacity | **~450 Tbps** end-2025 (from ~5.6 Tbps early 2024) | [FACT, ~80x growth in ~2 yr] |

Sources: [HighSpeedInternet satellite count](https://www.highspeedinternet.com/resources/how-many-starlink-satellites-are-in-orbit-june-12-2026), [DISHYtech capacity](https://www.dishytech.com/starlink-just-had-a-massive-2025-and-2026-could-be-even-bigger/), [constellation_mesh.md](../laser_comms/constellation_mesh.md).

**Full constellation capex (cumulative, satellites only).** SpaceX's own May 2018 estimate to design, build, and deploy the constellation was **"at least $10B"** [FACT, [Wikipedia/Starlink](https://en.wikipedia.org/wiki/Starlink)]. Reconstructing from unit costs: ~12,300 sats launched, blended ~$0.3-0.6M each across generations, gives **~$4-7B of satellite hardware** through mid-2026 [DERIVED/ESTIMATE]. Adding launch (Section 2) and ground segment (Section 3) puts cumulative all-in constellation capex on the order of **$15-25B+ through 2024-2026** [ESTIMATE]. This is a reconstructed figure, not a disclosed S-1 line, and is flagged as such. The point that matters: the constellation is a multi-tens-of-billions front-loaded capital project before it earns a dollar, which is exactly why prior waves refused to assume it and why scale is decisive.

---

## 2. Launch: needed, cost, and share of system cost

### 2.1 Launches needed and cost per launch

Starlink flies on Falcon 9 today (V3 transitions to Starship). The relevant cost is SpaceX's **internal/marginal** Falcon 9 cost, not the ~$70M list price, because SpaceX flies its own payloads, exactly as the Neutron model treats the data-center venture flying its own racks ([launch_cost_economics.md](../rocket_lab/neutron/launch_cost_economics.md)).

| Launch metric | Value | Source / status |
|---|---|---|
| Falcon 9 internal/marginal cost (reused booster) | **~$15-20M** (NBF low end ~$11M) | [ESTIMATE, multiple] |
| Sats per Falcon 9 (V2 mini) | **~23** | [FACT] |
| All-in launch + sats per Falcon 9 Starlink mission | **~$62M** | [ESTIMATE, implies ~$2.7M delivered per sat] |
| Falcon 9 second stage | **Expendable every flight** | [FACT, falcon9_cadence_ramp.md] |
| Starship V3 capacity added per launch | **~60 Tbps** (>20x a Falcon 9 V2-mini launch) | [FACT/PROJECTION] |

Sources: [SpaceNexus launch cost guide](https://spacenexus.us/guide/space-launch-cost-comparison), [NextBigFuture Falcon 9 ~$11M](https://www.nextbigfuture.com/2026/02/spacex-falcon-9-true-cost-to-launch-is-about-300-per-pound-which-is-25-of-selling-price-to-customers.html), [launch_cost_economics.md](../rocket_lab/neutron/launch_cost_economics.md), [Via Satellite Starship/V3](https://www.satellitetoday.com/launch/2025/08/27/starships-payload-milestone-in-test-flight-gives-a-preview-of-v3-starlink-launches/).

**Launches needed to build the fleet.** At ~23 V2-mini per Falcon 9 (or 60 per earlier V1.5 batch), the ~12,300 satellites launched required **roughly 250-300 dedicated Starlink Falcon 9 flights** over ~6 years [DERIVED/ESTIMATE]. That is the headline reason SpaceX needed to drive Falcon 9 cadence to a record 165 launches in 2025 (falcon9_cadence_ramp.md): the internal Starlink manifest IS the cadence.

### 2.2 Launch as a share of system cost

Per delivered satellite at the ~$62M/23-sat figure: launch is ~$2.7M total delivered cost, of which the satellite is ~$0.8M (V2 mini) and launch is the rest (~$1.9M including share of an expendable upper stage and ops). At that snapshot, **launch is the majority of per-sat delivered cost (~60-70%)** for the cheap V2 mini.

But the system-level share is different and falls over time:

| Cost case | Satellite share | Launch share | Driver |
|---|---|---|---|
| **Conservative (cheap satellites, Falcon 9)** | ~30-40% | **~60-70%** | A $0.8M sat on a ~$1.9M launch slice |
| **Aggressive (V3 on Starship, mature)** | ~50-60% | **~20-40%** | Heavier $1.2M sat amortizes a cheaper Starship launch over far more capacity |

[DERIVED/ESTIMATE]. The trajectory: **as the satellites get more capable and the launcher gets cheaper per kg, launch shrinks as a share of system cost and the satellite hardware grows.** Launch is never a rounding error (unlike propellant in the launch-cost doc), but it is not the dominant lifetime cost once a constellation is mature, because launch is paid once per satellite while the satellite must be continuously rebuilt (Section 4). The reusable booster is what makes any of this work: an expendable launcher would multiply the launch share several-fold.

---

## 3. Ground segment: optical and RF capex and opex

The ground segment is the smallest of the three capital buckets, but it is real and (for optical) it is currently the industry's *binding* constraint (the "downlink deficit," [optical_ground_stations.md](../laser_comms/optical_ground_stations.md)).

### 3.1 RF ground segment (the Starlink model)

Starlink's customer link is RF; its ground side is a network of gateway/teleport stations plus tens of millions of user terminals.

| Ground element | Quantity / cost | Source / status |
|---|---|---|
| Gateway/teleport stations | **~150 operational, ~170 incl. construction** | early 2026 [FACT] |
| User terminal production cost | **~$2,400 (2020) → ~$500-600 (2023) → sold $349** | [FACT/ESTIMATE; subsidized below cost early] |
| Gateway radome dish | up to ~15 ft, steerable | [FACT] |

Sources: [Tesmanian/Starlinkinsider gateways](https://starlinkinsider.com/starlink-gateway-locations/), [Basenor terminal cost trajectory](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean).

The **user-terminal subsidy was a major early drag** (a ~$2,400 terminal sold at $499) and is a genuine ground-segment cost line that a B2B service with professional terminals partly avoids ([rf_limited_service.md](../laser_comms/rf_limited_service.md): large high-gain antennas are commodity-adjacent and customer-funded). As the terminal cost fell toward ~$500-600 the subsidy shrank, which the S-1 readers cite as one of three margin tailwinds.

### 3.2 Optical ground segment (the laser-mesh / data-center-adjacent model)

For an optical-downlink architecture (the data-center track and any laser-mesh comms play), ground costs come straight from [optical_ground_stations.md](../laser_comms/optical_ground_stations.md):

| Optical ground element | Cost | Source / status |
|---|---|---|
| Single production-class OGS | **~$3-5M** | [FACT, Cailabs/DataPath ~$61M for ~12+ units] |
| AO-equipped sub-meter station (HOGS) | **£2.5M (~$3.3M)** | [FACT] |
| Multi-terminal capable hub | **~$20-60M** | [ESTIMATE, flagged in source doc] |
| Full ~4-12 site operator network | **~$100-500M** | [ESTIMATE, flagged in source doc] |

So an optical ground network for a single operator is a **~$100-500M capex line, plus opex** (fiber backhaul, AO maintenance, site staff). Against a $15-25B constellation, **the ground segment is ~1-3% of system capital.** It is small in dollars but it is the *availability* bottleneck (weather diversity needs >=4 sites, ~10-12 for three-nines), so it cannot be skipped, only sized. RF backup adds modest cost and lifts availability when optical is clouded out.

### 3.3 Ground opex

Ground operations (gateway/teleport O&M, fiber backhaul leases, network operations centers, customer support) are not separately disclosed by Starlink. They are folded into the segment operating cost that the S-1 captures at the bottom line (Section 5). For modeling, ground opex is a low-single-digit-percent-of-revenue line, dwarfed by satellite depreciation and replacement.

---

## 4. Operations, the 5-year life as continuous replacement capex, and spectrum

### 4.1 The 5-year life is the defining operating cost

This is the line that makes space communications structurally different from a terrestrial network. **Starlink satellites are depreciated over ~5 years** [FACT, [SpaceXChart](https://spacexchart.com/starlink)], and the orbit physically de-orbits them on roughly that timescale. The constellation is therefore **not a built asset that then runs cheaply; it is a treadmill that must be entirely rebuilt every ~5 years.**

| Replacement metric | Value | Source / status |
|---|---|---|
| Satellite operating life | **~5 years** | [FACT] |
| Satellites replaced per year | **~1,000-2,000** | [ESTIMATE; ~1,000 single-lineage, but ~12,300 launched / 5 yr implies ~2,000+] |
| Annual satellite-replacement capex | **~$6-8B/yr** | [ESTIMATE, single analyst lineage] |

Sources: [Motley Fool ~$8B/yr replacement, ~1,000 sats/yr](https://www.fool.com/investing/2024/02/22/spacex-secret-could-cost-musk-82-billion-a-year/), [SpaceXChart 5-yr depreciation](https://spacexchart.com/starlink).

**Reconciliation note (flagged).** The "~1,000 sats/yr, ~$8B/yr" figure is one analyst lineage (Motley Fool, 2024). It is internally a bit low: a ~10,000-sat operational fleet on a 5-year life mechanically requires **~2,000 replacements/yr** just to hold steady, and SpaceX has been launching ~2,000-3,000/yr. The ~$8B/yr is best read as a 2024-vintage maintenance-capex estimate that will rise as the fleet grows and shift cheaper per-unit as V3-on-Starship lowers launch and per-bit cost. Either way, **steady-state replacement capex is multiple billions per year** and is the dominant recurring space cost. As a sanity check it is ~25% of the ~$32B forward revenue the same source assumes, vs. <10% of revenue for terrestrial cable capex, which is the capital-intensity gap in one number.

### 4.2 Operations and spectrum

- **Operations** (constellation flight ops, collision avoidance, network management, customer ops) are bundled into the segment operating cost. Not separately disclosed; second-order vs. depreciation/replacement.
- **Spectrum** for the RF customer link is, for a new entrant, **"years and real money"** but attainable as a narrow sliver ([rf_limited_service.md](../laser_comms/rf_limited_service.md)). For the incumbent, spectrum is a held asset (Ku/Ka priority filings) and not a large recurring cash cost. For a Rocket Lab-style entrant it is a real capital-and-time line item, modeled in the RF doc, not re-priced here.

---

## 5. The all-in cost: per subscriber, per GB, per delivered Gbps

This is the synthesis. Two cases: the **mature SpaceX-scale incumbent** (anchored to disclosed S-1 financials) and a **conservative new-entrant** (small scale, no amortization denominator).

### 5.0 Critical framing: segment vs. whole company

The SpaceX S-1 (May 2026) is easy to misread, so the distinction is stated up front:

| 2025 figure | SpaceX whole company | Starlink connectivity segment |
|---|---|---|
| Revenue | **$18.7B** | **$11.4B** |
| Operating income | **−$2.6B (loss)** | **+$4.42B** |
| Net income | **−$4.9B (loss)** | (not segment-disclosed) |
| Adjusted EBITDA | **$6.6B** | **$7.17B (segment)** |
| Operating margin | negative | **~38.6%** |
| Adjusted EBITDA margin | ~35% | **~63%** |

Sources: [Via Satellite S-1 readout](https://www.satellitetoday.com/finance/2026/05/20/spacexs-ipo-filing-gives-first-look-into-companys-financials/), [SpaceXChart](https://spacexchart.com/starlink), [New Space Economy](https://newspaceeconomy.ca/2026/05/30/what-is-starlinks-financial-performance/).

**The whole company lost money in 2025 because Starship R&D (~$3B) and xAI burn swamp the profitable Starlink segment.** The communications-delivery economics live entirely in the *connectivity segment*, which is solidly profitable. All per-subscriber and per-GB figures below use the **segment** numbers. This is the correct denominator for "what does it cost to deliver communications from space."

### 5.1 Per subscriber per year

| Metric | Value | Basis |
|---|---|---|
| Subscribers (end 2025 / Q1 2026) | **8.9M / 10.3M** | [FACT] |
| ARPU | **$99/mo (2023) → $81 (2025) → $66 (Q1 2026)** | [FACT; falling as mix shifts to lower-priced/residential] |
| Revenue per subscriber per year | **~$790-1,100/yr** | ARPU x 12 [DERIVED] |
| Operating income per subscriber per year | **~$300-430/yr** | $4.42B / ~10M at 38.6% margin [DERIVED] |
| **All-in delivery cost per subscriber per year** | **~$480-680/yr** | revenue minus operating income [DERIVED] |
| of which space capital + launch replacement | **~$200-260/yr** | ~$6-8B replacement capex / ~30M-ish capacity-subscribers [DERIVED/ESTIMATE] |

[DERIVED from S-1]. The honest read: **the mature incumbent delivers a subscriber's service for roughly $480-680/yr all-in and sells it for ~$790/yr**, and the *space-specific* (satellite + launch replacement) portion of that cost is on the order of **$200-260/subscriber/yr**. The rest is ground, terminals, support, and SG&A. ARPU is *falling* (mix shift to cheaper residential and roam plans), so the margin is held up by the cost side falling faster: constellation amortization rolling off, terminal subsidy shrinking, and launch $/kg dropping. These are the three S-1-cited margin tailwinds.

### 5.2 Per GB

There is no disclosed cost-per-GB; it must be derived from capacity, and it splits into two very different numbers.

**Network-average (the optimistic number).** Aggregate capacity ~450 Tbps end-2025. If the network ran flat-out continuously, that is ~450 Tbps x 1 Gb = ~56 TB/s = on the order of **~4,800 PB/day** of theoretical capacity. Real utilization is far below peak (capacity is provisioned for peak/geography, not average), so usable delivered volume is a fraction of that. Against ~$6-8B/yr replacement capex plus opex spread over realistic delivered volume, the **marginal space cost of bulk delivered data lands on the order of $0.05-0.30/GB** [ESTIMATE, utilization-dependent]. For comparison, Starlink's metered Roam plans **charge ~$0.50/GB** ([US Mobile](https://www.usmobile.com/blog/starlink-cost/)), so retail price sits above marginal space cost, as expected.

**Capacity-constrained edge (the real-world number, and the structural point).** This average is misleading wherever users concentrate, and that is the heart of the supply-side story:

> **A beam serves a fixed pool of capacity over a fixed ground footprint. Cost per user therefore RISES with user density, the exact opposite of terrestrial fiber/cable, where density LOWERS cost per user.**

Concrete evidence: Starlink capacity analyses find oversubscription kicks in at roughly **~30 beam-service-locations per square mile**, and "~700 Gbps is plenty for several thousand people" but not for a city ([XLab capacity working paper](https://thexlab.org/wp-content/uploads/2025/07/Starlink_Analysis_Working_Paper_v0.2-1.pdf), [Jeff Geerling](https://www.jeffgeerling.com/blog/2022/starlinks-current-problem-capacity/)). The system is "highly dependent on extremely low customer density." In a dense market the *effective* cost per delivered GB rises sharply because each beam's fixed capacity is shared among more users, forcing either deprioritization or more satellites overhead (which the orbital geometry caps). **Terrestrial networks add a fiber strand to add capacity; space networks cannot add a beam to a hot spot without adding satellites to the whole orbital shell.** This is the permanent structural ceiling on space communications economics and the reason space wins in low-density / mobile / unserved markets and loses in dense urban ones.

### 5.3 Per delivered Gbps (capital efficiency)

| Generation/system | Capital per Gbps of capacity | Basis |
|---|---|---|
| V2 mini satellite | **~$10k/Gbps** | $0.8M / 80 Gbps [DERIVED/ESTIMATE] |
| V3 satellite | **~$1.2k/Gbps** | $1.2M / 1,000 Gbps [DERIVED/PROJECTION] |
| Whole constellation (V2-mini era) | **~$33-55k/Gbps** | ~$15-25B / 450 Tbps [DERIVED/ESTIMATE, includes launch + ground] |

[DERIVED/ESTIMATE]. The satellite-only and system-wide numbers differ ~3-5x because system capital includes launch, ground, and replacement, not just the bare satellite. The trend is the headline: **per-Gbps capital cost is falling roughly an order of magnitude per satellite generation**, driven by bigger satellites on a cheaper-per-kg launcher. A mass-limited launcher (which cannot fly the 1.5-tonne V3-class satellite that drives the per-Gbps cost down) is structurally stuck near the top of this curve.

### 5.4 Conservative new-entrant case vs. aggressive mature case

| Dimension | Conservative new entrant (small scale) | Aggressive SpaceX-scale mature |
|---|---|---|
| Subscribers / denominator | thousands to low-millions | tens of millions |
| Per-satellite cost | higher (low volume, no vertical integration) | $0.8-1.2M (Quilty est.) |
| Launch | Falcon 9 / Neutron internal ~$13-25M | Falcon 9 ~$15M, Starship cheaper/kg |
| Constellation amortization per subscriber | **multiples higher** (few users carry the fixed fleet) | low (huge denominator) |
| All-in delivered cost per subscriber | **likely several x the incumbent** | ~$480-680/yr |
| Per-GB at the edge | worse (fewer satellites, less beam diversity) | $0.05-0.30/GB network avg, higher at density |
| EBITDA margin achievable | thin to negative until scale | ~63% segment (disclosed) |

[ESTIMATE]. The conservative case is *not* a scaled-down copy of the aggressive case with the same unit economics. **The space cost stack is overwhelmingly fixed (build and continuously replace a fleet, launch it, run a ground network), so per-subscriber cost is dominated by the denominator.** A boutique B2B entrant ([rf_limited_service.md](../laser_comms/rf_limited_service.md)) with thousands of high-value users can still work *because the users are high-ARPU*, not because the per-subscriber cost is low. This is the central asymmetry the ground-vs-space ratio must capture: **space delivery is cheap per subscriber only at SpaceX scale, and expensive per subscriber at any smaller scale**, and it is cheap per GB only in low-density markets.

---

## 6. What this means for the ground-vs-space ratio (handoff, not a verdict)

This doc supplies the SPACE numerator. The ratio itself (ground-vs-space cost to deliver communications) needs the ground denominator, which is a separate doc. The space side, summarized for that synthesis:

- **Mature incumbent space delivery: ~$480-680/subscriber/yr all-in**, ~$200-260 of which is space-specific capital/launch replacement, at a disclosed ~63% segment EBITDA margin and ~38.6% segment operating margin on $11.4B revenue.
- **Network-average space delivery: ~$0.05-0.30/GB**, but **rising sharply at user density** (the capacity-per-beam constraint), which is the opposite of terrestrial density economics.
- **The space cost is dominated by the satellite fleet and its 5-year replacement treadmill (~$6-8B/yr at incumbent scale), then launch (20-70% of system capital depending on case), then a small (~1-3% of capital) but availability-critical ground segment.**
- **Scale is the entire game.** The same fixed space stack is cheap per subscriber at tens of millions of users and expensive at thousands. A new entrant's space delivery cost per subscriber is structurally higher; its path to viability is high-ARPU niches, not low per-subscriber cost.

The mirror to the data-center track's orbit-to-ground ratio (1.92x in the launch-cost doc's LEO $/kg sense) is: **on the communications side, space is cost-competitive with ground only in the markets ground serves badly (low density, mobile, unserved), and is structurally more expensive per delivered GB everywhere ground fiber already reaches.** Quantifying that crossover against terrestrial cost is the next doc's job.

---

## Sources

- [SpaceX IPO filing readout, Via Satellite (May 2026)](https://www.satellitetoday.com/finance/2026/05/20/spacexs-ipo-filing-gives-first-look-into-companys-financials/): $18.7B total rev, $11.4B Starlink, minus $4.9B net, $6.6B adj EBITDA, subs/ARPU trajectory
- [SpaceXChart, Starlink unit economics](https://spacexchart.com/starlink): $11.4B FY25 rev, $4.4B operating profit, 38.6% operating margin, 10.3M subs, 5-yr depreciation, ~9,600 active sats
- [New Space Economy, Starlink financial performance](https://newspaceeconomy.ca/2026/05/30/what-is-starlinks-financial-performance/): $7.17B segment adj EBITDA, ~63% margin
- [Value Add VC, Starlink revenue 2026](https://valueaddvc.com/blog/starlink-revenue-2025-2026-subscriber-count-arpu-and-the-path-to-profitability): run-rate, subscriber, ARPU detail
- [NextBigFuture, Starlink is the SpaceX cash machine](https://www.nextbigfuture.com/2025/08/starlink-is-now-the-spacex-cash-machine.html): per-sat cost trajectory, Falcon 9 cost, $62M/launch
- [NextBigFuture, Falcon 9 true cost ~$11M](https://www.nextbigfuture.com/2026/02/spacex-falcon-9-true-cost-to-launch-is-about-300-per-pound-which-is-25-of-selling-price-to-customers.html): Falcon 9 internal cost components
- [Planet Tech News, Starlink sats ~$250k, Falcon 9 under $30M](https://www.planettechnews.com/spacex-starlink-satellites-could-cost-250000-each-and-falcon-9-costs-less-than-30-million/): alternate per-sat lineage
- [Tom's Hardware, V3 satellites 60 Tbps/launch, 1 Tbps/sat](https://www.tomshardware.com/service-providers/network-providers/spacex-shows-off-massive-new-v3-starlink-satellites-expanded-technology-will-deliver-gigabit-internet-to-customers-for-the-first-time-and-enable-60-tera-bits-per-second-downlink-capacity)
- [Basenor, Starlink V3 specs and cost trajectory](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean): terminal cost trajectory, satellite lifespan
- [Via Satellite, Starship/V3 payload milestone](https://www.satellitetoday.com/launch/2025/08/27/starships-payload-milestone-in-test-flight-gives-a-preview-of-v3-starlink-launches/)
- [Motley Fool, $8.2B/yr replacement capex](https://www.fool.com/investing/2024/02/22/spacex-secret-could-cost-musk-82-billion-a-year/): satellite replacement rate and capex
- [HighSpeedInternet, Starlink satellites in orbit (June 2026)](https://www.highspeedinternet.com/resources/how-many-starlink-satellites-are-in-orbit-june-12-2026): fleet counts
- [DISHYtech, Starlink 2025 capacity](https://www.dishytech.com/starlink-just-had-a-massive-2025-and-2026-could-be-even-bigger/): ~450 Tbps aggregate
- [Starlink Insider, gateway locations](https://starlinkinsider.com/starlink-gateway-locations/): ~150 operational gateways
- [US Mobile, Starlink plans and pricing](https://www.usmobile.com/blog/starlink-cost/): ~$0.50/GB metered Roam
- [XLab, Starlink capacity working paper](https://thexlab.org/wp-content/uploads/2025/07/Starlink_Analysis_Working_Paper_v0.2-1.pdf): oversubscription / beam-density constraint
- [Jeff Geerling, Starlink's capacity problem](https://www.jeffgeerling.com/blog/2022/starlinks-current-problem-capacity/): capacity vs. density
- [Wikipedia, Starlink](https://en.wikipedia.org/wiki/Starlink): May 2018 "at least $10B" constellation estimate
- Internal: [optical_ground_stations.md](../laser_comms/optical_ground_stations.md), [constellation_mesh.md](../laser_comms/constellation_mesh.md), [rf_limited_service.md](../laser_comms/rf_limited_service.md), [launch_cost_economics.md](../rocket_lab/neutron/launch_cost_economics.md), [falcon9_cadence_ramp.md](../competitors/falcon9_cadence_ramp.md)

---

## Confidence

**Medium-high on the incumbent's disclosed financials.** The SpaceX S-1 (May 2026) is an audited filing; revenue ($11.4B Starlink, $18.7B total), the −$4.9B company net loss, the $4.42B segment operating income, the ~63% segment adjusted EBITDA margin, subscriber counts (8.9M end-2025, 10.3M Q1 2026), and the ARPU trajectory ($99 to $66) are cross-checked across multiple independent readers (Via Satellite, SpaceXChart, New Space Economy, Value Add VC) that agree. The segment-vs-whole-company distinction is the main interpretation risk and is handled explicitly.

**Medium on per-satellite unit costs.** SpaceX discloses none; the V1 ~$200-250k / V2 mini ~$800k / V3 ~$1.2M figures are Quilty Space estimates repeated in trade press, and a second lineage puts V2 mini near ~$250k, a ~2x disagreement. The *trend* (rising per-sat cost, falling per-bit cost) is robust regardless of which point estimate is right.

**Medium on the derived per-subscriber stack and low-medium on per-GB.** The per-subscriber all-in cost is anchored to disclosed revenue and operating income (solid) but the space-specific split (~$200-260/yr) leans on the estimated ~$6-8B/yr replacement capex (single lineage). The per-GB number depends on an assumed utilization of disclosed peak capacity and is the softest figure here, given as a range.

**Low-medium on the conservative new-entrant case.** It is a structural argument (fixed-cost-dominated stack, denominator-driven per-subscriber cost) rather than a sourced model; the direction is high-confidence, the magnitudes are illustrative.

---

## Open Questions

1. **Actual delivered data volume (for a hard per-GB number).** Disclosed figures are *capacity* (450 Tbps) and *revenue*, not delivered petabytes/day. A real cost-per-GB needs the network's actual average utilization, which SpaceX does not publish. The ~$0.05-0.30/GB range would tighten materially with a disclosed throughput figure.
2. **The replacement-capex figure and rate.** ~$6-8B/yr and ~1,000 sats/yr come from one 2024 analyst lineage and are arithmetically low against a ~10,000-sat fleet on a 5-year life (which implies ~2,000+/yr). The true steady-state replacement capex, and how it falls as V3-on-Starship lowers per-bit cost, is unresolved and load-bearing for the per-subscriber space cost.
3. **Per-satellite unit cost (~2x source disagreement on V2 mini).** Quilty's ~$800k vs. the alternate ~$250k materially changes the satellite share of system cost. A firmer estimate (or any SpaceX disclosure) would resolve the satellite-vs-launch share split.
4. **The density crossover point.** At what user density does space delivery cost per GB cross above terrestrial? This is the crux of the ground-vs-space ratio and needs the ground denominator (separate doc) plus a beam-capacity model. The ~30 BSL/sq-mi oversubscription threshold is a starting anchor.
5. **New-entrant unit economics at realistic scale.** The conservative case is structural, not modeled. A concrete small-constellation model (N satellites, M subscribers, fixed-cost spread) would convert the "multiples higher per subscriber" claim into numbers, and connects to the RF-sliver B2B concept in rf_limited_service.md.
6. **V3-on-Starship cost realization.** The ~$1.2k/Gbps V3 figure and ~60 Tbps/launch are projections over a vehicle that first flew V3-class in May 2026 with dummy payloads. Whether the per-bit cost-down actually lands depends on Starship reaching cadence and on V3 production cost, both unconfirmed.

---

## Claims table

| COMM- id | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-080 | Starlink V1 satellite unit cost (estimate) | ~$200-250k (alt lineage ~$500k-1M early) | ESTIMATE | [NBF](https://www.nextbigfuture.com/2025/08/starlink-is-now-the-spacex-cash-machine.html), [Planet Tech News](https://www.planettechnews.com/spacex-starlink-satellites-could-cost-250000-each-and-falcon-9-costs-less-than-30-million/) |
| COMM-081 | Starlink V2 mini satellite unit cost (estimate, ~2x source disagreement) | ~$800k (Quilty) vs ~$250k (alt) | ESTIMATE (double-check) | [NBF](https://www.nextbigfuture.com/2025/08/starlink-is-now-the-spacex-cash-machine.html), [Planet Tech News](https://www.planettechnews.com/spacex-starlink-satellites-could-cost-250000-each-and-falcon-9-costs-less-than-30-million/) |
| COMM-082 | Starlink V3 satellite unit cost (projection) | ~$1.2M, ~1,500 kg | PROJECTION | [NBF/Quilty](https://www.nextbigfuture.com/2025/08/starlink-is-now-the-spacex-cash-machine.html), [Basenor](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean) |
| COMM-083 | Starlink V3 per-satellite downlink capacity | ~1 Tbps down (~4 Tbps incl. laser); ~60 Tbps added per Starship launch | FACT/PROJECTION | [Tom's Hardware](https://www.tomshardware.com/service-providers/network-providers/spacex-shows-off-massive-new-v3-starlink-satellites-expanded-technology-will-deliver-gigabit-internet-to-customers-for-the-first-time-and-enable-60-tera-bits-per-second-downlink-capacity), [Via Satellite](https://www.satellitetoday.com/launch/2025/08/27/starships-payload-milestone-in-test-flight-gives-a-preview-of-v3-starlink-launches/) |
| COMM-084 | Starlink satellites launched cumulative (June 2026) | 12,318 | FACT | [HighSpeedInternet](https://www.highspeedinternet.com/resources/how-many-starlink-satellites-are-in-orbit-june-12-2026) |
| COMM-085 | Starlink satellites operational (June 2026) | ~9,542 (~10,676 in orbit) | FACT | [HighSpeedInternet](https://www.highspeedinternet.com/resources/how-many-starlink-satellites-are-in-orbit-june-12-2026) |
| COMM-086 | Starlink aggregate network capacity end-2025 | ~450 Tbps (from ~5.6 Tbps early 2024) | FACT | [DISHYtech](https://www.dishytech.com/starlink-just-had-a-massive-2025-and-2026-could-be-even-bigger/), [constellation_mesh.md](../laser_comms/constellation_mesh.md) |
| COMM-087 | SpaceX original Starlink constellation cost estimate (May 2018) | "at least $10B" | FACT | [Wikipedia](https://en.wikipedia.org/wiki/Starlink) |
| COMM-088 | Cumulative Starlink constellation capex (reconstructed) | ~$15-25B+ through 2024-2026 | ESTIMATE (reconstructed, not disclosed) | [Wikipedia](https://en.wikipedia.org/wiki/Starlink), this doc derivation |
| COMM-089 | Falcon 9 internal/marginal launch cost (reused) | ~$15-20M (low end ~$11M) | ESTIMATE | [SpaceNexus](https://spacenexus.us/guide/space-launch-cost-comparison), [NBF](https://www.nextbigfuture.com/2026/02/spacex-falcon-9-true-cost-to-launch-is-about-300-per-pound-which-is-25-of-selling-price-to-customers.html), [launch_cost_economics.md](../rocket_lab/neutron/launch_cost_economics.md) |
| COMM-090 | Starlink Falcon 9 mission: sats per launch and delivered cost | ~23 V2 mini, ~$62M/launch (~$2.7M delivered/sat) | ESTIMATE | [NBF](https://www.nextbigfuture.com/2025/08/starlink-is-now-the-spacex-cash-machine.html), [SpaceNexus](https://spacenexus.us/guide/space-launch-cost-comparison) |
| COMM-091 | Dedicated Starlink Falcon 9 flights to build fleet | ~250-300 over ~6 yr | DERIVED | this doc (12,300 sats / batch sizes) |
| COMM-092 | Launch share of system cost | ~60-70% (cheap-sat case) to ~20-40% (V3/Starship mature) | DERIVED/ESTIMATE | this doc |
| COMM-093 | Single production-class optical ground station cost | ~$3-5M | FACT | [optical_ground_stations.md](../laser_comms/optical_ground_stations.md) |
| COMM-094 | Full operator optical ground network capex | ~$100-500M (~1-3% of system capital) | ESTIMATE | [optical_ground_stations.md](../laser_comms/optical_ground_stations.md) |
| COMM-095 | Starlink operational gateway stations | ~150 (~170 incl. construction), early 2026 | FACT | [Starlink Insider](https://starlinkinsider.com/starlink-gateway-locations/) |
| COMM-096 | Starlink user terminal production cost trajectory | ~$2,400 (2020) → ~$500-600 (2023), sold $349 | FACT/ESTIMATE | [Basenor](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean) |
| COMM-097 | Starlink satellite operating life / depreciation | ~5 years | FACT | [SpaceXChart](https://spacexchart.com/starlink) |
| COMM-098 | Starlink annual satellite-replacement capex | ~$6-8B/yr (~1,000-2,000 sats/yr) | ESTIMATE (single lineage, double-check) | [Motley Fool](https://www.fool.com/investing/2024/02/22/spacex-secret-could-cost-musk-82-billion-a-year/), [SpaceXChart](https://spacexchart.com/starlink) |
| COMM-099 | SpaceX 2025 total revenue (whole company) | $18.7B ($11.4B Starlink, $4B Space, $3.2B AI) | FACT | [Via Satellite S-1](https://www.satellitetoday.com/finance/2026/05/20/spacexs-ipo-filing-gives-first-look-into-companys-financials/) |
| COMM-100 | SpaceX 2025 whole-company net / operating result | −$4.9B net loss; −$2.6B operating loss; $6.6B adj EBITDA | FACT | [Via Satellite S-1](https://www.satellitetoday.com/finance/2026/05/20/spacexs-ipo-filing-gives-first-look-into-companys-financials/) |
| COMM-101 | Starlink connectivity SEGMENT 2025 operating income | $4.42B on $11.4B revenue (~38.6% operating margin) | FACT | [SpaceXChart](https://spacexchart.com/starlink), [New Space Economy](https://newspaceeconomy.ca/2026/05/30/what-is-starlinks-financial-performance/) |
| COMM-102 | Starlink connectivity SEGMENT 2025 adjusted EBITDA margin | ~63% ($7.17B on $11.4B) | FACT | [New Space Economy](https://newspaceeconomy.ca/2026/05/30/what-is-starlinks-financial-performance/) |
| COMM-103 | Starlink subscribers | 8.9M (end 2025), 10.3M (Q1 2026) | FACT | [Via Satellite S-1](https://www.satellitetoday.com/finance/2026/05/20/spacexs-ipo-filing-gives-first-look-into-companys-financials/), [SpaceXChart](https://spacexchart.com/starlink) |
| COMM-104 | Starlink ARPU trajectory | $99/mo (2023) → $81 (2025) → $66 (Q1 2026) | FACT | [Via Satellite S-1](https://www.satellitetoday.com/finance/2026/05/20/spacexs-ipo-filing-gives-first-look-into-companys-financials/) |
| COMM-105 | Implied all-in delivery cost per subscriber per year (incumbent) | ~$480-680/yr (space-specific portion ~$200-260/yr) | DERIVED/ESTIMATE | this doc, from S-1 + replacement capex |
| COMM-106 | Network-average space cost per delivered GB (incumbent) | ~$0.05-0.30/GB (vs ~$0.50/GB metered retail) | ESTIMATE | this doc; [US Mobile retail](https://www.usmobile.com/blog/starlink-cost/) |
| COMM-107 | Capital cost per Gbps of capacity (trend) | ~$10k/Gbps (V2 mini) → ~$1.2k/Gbps (V3); ~$33-55k/Gbps system-wide | DERIVED/ESTIMATE | this doc |
| COMM-108 | Beam capacity / density constraint (cost rises with user density) | oversubscription ~30 BSL/sq-mi; ~700 Gbps serves "several thousand" | FACT/ESTIMATE | [XLab](https://thexlab.org/wp-content/uploads/2025/07/Starlink_Analysis_Working_Paper_v0.2-1.pdf), [Jeff Geerling](https://www.jeffgeerling.com/blog/2022/starlinks-current-problem-capacity/) |
