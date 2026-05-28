# AI Data Center Market — Size, Growth & TAM Framing

*Research date: May 2026. Prepared for the Rocket Lab orbital AI-inference data center feasibility project.*

> **Scope note:** This document focuses specifically on **AI / GPU-accelerated compute** ("AI data centers", "AI factories"). It deliberately separates AI-specific capacity from general-purpose CPU cloud (ordinary AWS/EC2-style workloads). Where a figure covers *all* data centers, it is labeled as such.

> **Reading guide:** Each claim is tagged **[FACT]** (observed / reported 2025–26 data), **[PROJECTION]** (analyst forecast — speculative), or **[ILLUSTRATIVE]** (our own arithmetic for order-of-magnitude framing only). Hard numbers are cross-checked against ≥2 independent sources.

> **Source status (2026-05-26):** See [SOURCE_INDEX.md](../SOURCE_INDEX.md) claim IDs REV-004, REV-012, and RLDC-MARKET-100GW-2036. McKinsey-style 2030 numbers are analyst projections, not future facts. Paid-report snippets support market framing but should not be used alone as hard certification. The illustrative space TAM remains an order-of-magnitude framing device.

---

## Summary

- **Current AI DC scale (2026):** Global AI data center power capacity is roughly **~30 GW operational** (late 2025), rising fast as 2026 brings the first wave of **1 GW+ "AI factories"** online. Total (AI + non-AI) global data center capacity is ~103–122 GW; AI workloads are ~44 GW of the 2026 mix. The US holds ~90% of Americas capacity and ~80 GW of all-data-center capacity.
- **Capex:** The top 5 hyperscalers (Microsoft, Alphabet, Amazon, Meta, Oracle) are committing **~$600–750B in total capex in 2026**, of which **~75% (~$450–560B) is AI infrastructure**. Building 1 GW of AI data center costs roughly **$35–60B all-in** (facility + IT/GPUs); infrastructure-only is ~$15–20B/GW.
- **2030 projection:** Analysts (McKinsey) project **~156 GW of AI-specific** data center demand by 2030 (~200–219 GW all-in), with cumulative AI-related investment of **~$5.2T**. ~33%/yr growth for AI-ready capacity. Treat as speculative — see caveats.
- **Inference share:** Inference is **~55–67% of AI compute today** and is expected to **dominate by 2030** (~93 GW of AI inference vs ~62 GW training in one 2030 scenario). Inference is the relevant slice for an orbital-serving thesis.
- **Illustrative space TAM:** IF ~90 GW of AI *inference* capacity exists ~2030, then **0.1% / 1% / 10% served from orbit = ~0.09 / 0.9 / 9 GW**, corresponding very roughly to **~$0.3B / ~$3B / ~$30B** of annual inference-service revenue (see assumptions in the Illustrative section — order-of-magnitude only).
- **Why space is interesting:** Terrestrial buildout is increasingly **supply-constrained** — US interconnection queues exceed **2,300–2,600 GW** with **~5-year median waits** (data centers face up to **12 years**), transformer lead times stretch to **~5 years**, water is now the #2 constraint after power, and **11 states + dozens of municipalities** introduced moratorium/restriction bills in 2026.

**Confidence:** Moderate-high on current scale and capex (multiple converging sources). Moderate on the AI-vs-total capacity split (definitions vary by analyst). Low-to-moderate on 2030 projections (genuine forecast uncertainty + possible bubble dynamics). The illustrative space TAM is a framing device, not a forecast.

---

## 1. Current Scale (2026)

### Global & US capacity in gigawatts

| Metric | Value | Tag |
|---|---|---|
| Global AI DC power capacity, operational (late 2025) | **~30 GW** | [FACT] |
| Global total DC capacity (AI + non-AI), 2025 | ~103 GW (JLL) / ~122 GW installed IT power (other) | [FACT] |
| Global 2026 workload split | non-AI ~38 GW; **AI ~44 GW** | [FACT/PROJECTION] |
| Under construction globally (Sep 2025) | ~23 GW across ~831 sites (~17 GW in the Americas) | [FACT] |
| US total DC power draw (2025) | ~41 GW actual draw; ~80 GW capacity | [FACT] |
| US share of Americas capacity | ~90% | [FACT] |

The industry now measures AI data centers in **gigawatts of power**, not square footage or server count, because power (and grid access) is the binding constraint. ~30 GW of *AI-specific* capacity is "comparable to the peak power usage of New York State" (Epoch AI).

### Typical and largest facilities

- **Typical large AI DC today:** 100–300 MW. xAI's original Colossus was the "world's largest" at ~300 MW.
- **2026 — the first 1 GW+ "AI factories":** Five facilities are reported to cross **1 GW** in 2026 — Anthropic–Amazon New Carlisle (Jan), xAI Colossus 2 (Feb), Microsoft Fayetteville (Mar), Meta Prometheus (May), OpenAI Stargate Abilene (Jul). [FACT/near-term]
- **Largest 2026 facility:** xAI Colossus 2 — compute equivalent of ~1.4M H100-class GPUs, power draw heading past ~1.6 GW.
- **Mega-campuses:** OpenAI's **Stargate** program (with Oracle/SoftBank) targets ~**5.5 GW** across multiple sites, headline figure ~$500B. The US is projected to need ~20–30 GW of AI DC power by late 2027.

---

## 2. Capex & Spend

### Hyperscaler AI infrastructure spend (2026)

| Source | Top-5 hyperscaler 2026 capex | Notes |
|---|---|---|
| Consensus / company guidance | **~$660–690B** | ~2× 2025 levels |
| CreditSights (revised up) | **~$750B** | ~67% YoY increase |
| IEEE/Comsoc, Introl | **>$600B** | ~36% YoY increase |

[FACT — company guidance + multiple analysts converge on a $600–750B range.]

**AI share:** ~**75%** of aggregate hyperscaler capex is AI infrastructure → roughly **$450–560B of AI-specific capex in 2026** from the top 5 alone. Company plans: Amazon ~$200B, Alphabet ~$175–185B, Meta ~$115–135B, Microsoft ~$120B+, Oracle ~$50B. All hyperscalers report being **supply-constrained, not demand-constrained**.

### Cost to build 1 GW of AI data center

Estimates vary widely by scope (infrastructure-only vs. including GPUs/IT) and design:

| Estimate | $ per GW | Scope |
|---|---|---|
| Infrastructure only (shell, power, cooling) | ~$15–20B | building + electrical/cooling, no IT |
| Bernstein | ~$35B | |
| "Typical" all-in | ~$38B | facility + IT capex |
| Mid-range "fully built-out ecosystem" | ~$45–55B | |
| Nvidia (FY-Q2 2026 call) | ~$50–60B | |
| IBM CEO | ~$80B | facility + fully populated with IT |

**Working figure: ~$35–60B all-in per GW** (the IT/GPU equipment is the majority of cost; the shell is ~$15–20B). [FACT — reported ranges, cross-checked.]

### Inference vs. training split of spend

By **compute hours**, inference is the larger share; by **dollar spend**, training clusters carry a heavier per-unit footprint, so the split looks more even. Rough read: inference is already **~55%+ of AI GPU workload** and growing toward clear dominance (Section 4).

---

## 3. Growth Projections (≈2030)

> **[PROJECTION] — speculative.** These are analyst forecasts made amid an investment supercycle with active debate about an "AI bubble." Treat as scenario framing, not certainty.

**McKinsey** (the most-cited framework):
- Total data center demand: ~82 GW (2025) → **~171–219 GW by 2030** (~19–22%/yr).
- **AI-specific capacity: ~156 GW of AI-related demand by 2030**, ~125 GW of that *incremental* vs 2025. AI-ready capacity growing ~**33%/yr** (2023–30).
- Cumulative investment to 2030: **~$6.7T total**, of which **~$5.2T for AI-specific data centers**.

**JLL / BloombergNEF:** global (all) data center capacity ~doubling to **~200 GW by 2030** (~+97 GW 2025–30).

**IEA (energy):** data center electricity use → **~945 TWh by 2030** (~Japan's total consumption); ~11.7% of US power demand.

**Caveats / how speculative:** (1) "AI capacity" definitions differ across analysts — compare ranges, not point estimates. (2) Forecasts assume sustained demand and financing; Axios reported in Feb 2026 that some buildout is *stalling*. (3) ~$5T+ of projected capex depends on AI revenue scaling to justify it — a genuine open risk.

---

## 4. The Inference Share — Why It Dominates

| Period | Inference share of AI compute | Training share |
|---|---|---|
| 2026 | **~55–67%** | ~33–45% |
| 2030 | **Dominant** — inference > training | ~30% of total DC demand |

[FACT for today's ~55–67%; PROJECTION for 2030.]

One widely-cited 2030 scenario (Introl, citing the 2025–30 buildout):
- **AI inference: 20.9 GW (2025) → 93.3 GW (2030)** — ~35% CAGR.
- **AI training: 23.1 GW (2025) → 62.2 GW (2030)** — ~22% CAGR.

So inference overtakes training and becomes the single largest AI workload class. By compute *hours*, inference may be ~65% by 2030. **Why this matters for the orbital thesis:** inference is steady-state, latency-tolerant for many batch/async workloads, geographically distributable, and the fastest-growing slice — a better fit for a novel remote (orbital) compute venue than tightly-coupled, network-intensive training runs.

**AI inference market in $ terms** (services/hardware revenue, not power): MarketsandMarkets ~$106B (2025) → **~$255B by 2030** (~19% CAGR); Grand View Research ~$254B by 2030 (~17.5% CAGR); Fortune Business Insights ~$118B (2026). Multiple firms converge near **~$250B by 2030**.

---

## 5. Illustrative Space TAM

> **[ILLUSTRATIVE] — This entire section is our own arithmetic for order-of-magnitude framing. Every number is an assumption, labeled. It is NOT a forecast or a market estimate.**

> **Superseded as a revenue figure (wave-4, 2026-05-17).** The ~$3B/GW-yr proxy
> (assumption A3) was **retired as a revenue figure** by `synthesis/wave4_synthesis.md`
> §3 — it conflates a top-down services-market total with capacity, and is not
> what a capacity owner actually bills. For payback/revenue work use the
> bottom-up figures: **~$15–20B/GW-yr gross IaaS** (~$8M/rack-yr) and
> **~$25–50B/GW-yr gross inference-service** (~$16M/rack-yr) from
> `economics/revenue_per_watt.md`. The ~$3B/GW figure is kept below only for
> order-of-magnitude market sizing, not as a business case.

### Assumptions

| # | Assumption | Value | Basis |
|---|---|---|---|
| A1 | AI *inference* capacity, ~2030 | **~90 GW** | Midpoint of Section 4 (93 GW inference scenario; McKinsey implies similar order) |
| A2 | Orbital-served fraction (scenario lever) | **0.1% / 1% / 10%** | Pure scenario range — chosen to bracket order of magnitude |
| A3 | Annual inference-service revenue per GW | **~$3B/GW/yr** | Derived: ~$250B (2030 inference market, Section 4) ÷ ~90 GW ≈ ~$2.8B/GW; rounded to $3B |

> A3 caveat: this conflates a *services revenue* figure with a *power capacity* figure as a crude bridge. It is a rough proxy only — actual revenue/GW depends on utilization, model mix, and pricing. Use for magnitude, not for a business case.

### Arithmetic

**Capacity served from orbit** = A1 × A2:

| Orbital share (A2) | GW served from orbit |
|---|---|
| 0.1% | 90 GW × 0.001 = **~0.09 GW (~90 MW)** |
| 1% | 90 GW × 0.01 = **~0.9 GW** |
| 10% | 90 GW × 0.10 = **~9 GW** |

**Annual revenue proxy** = (GW served) × A3 ($3B/GW/yr):

| Orbital share | GW in orbit | Illustrative annual revenue |
|---|---|---|
| 0.1% | ~0.09 GW | ~$0.27B (**~$0.3B/yr**) |
| 1% | ~0.9 GW | ~$2.7B (**~$3B/yr**) |
| 10% | ~9 GW | ~$27B (**~$30B/yr**) |

**Capex-side cross-check (alternative framing):** at ~$35–60B to build 1 GW terrestrially, the *equivalent* build-out value of orbital capacity at the 1% scenario (~0.9 GW) is ~$30–55B of one-time capex-equivalent — though orbital economics (launch, power-per-kg, thermal) differ entirely and this is only a scale anchor.

### Takeaway

Even a **fraction of a percent** of 2030 inference capacity served from orbit is a **multi-hundred-million to multi-billion dollar/yr** opportunity; **1%** lands in the **~$3B/yr** range; an aggressive **10%** would be **~$30B/yr**. The thesis does not require capturing a large share to be material — that is the key framing point. The binding questions are on the *supply/feasibility* side (launch cost, orbital power, thermal rejection, latency, comms — covered elsewhere in this project), not on whether the addressable demand exists.

---

## 6. Constraints Driving Interest in Space ("push" factors)

Terrestrial AI data center buildout is increasingly **supply-constrained**. Quantified bottlenecks:

**Power / grid interconnection**
- US interconnection queue backlog: **~2,300–2,600 GW** of generation/storage waiting — *more than the entire installed US power capacity*. [FACT]
- Median time to commercial operation: **~5 years**; data center projects can face up to **~12 years**. Projects average **>3 years** to an interconnection agreement, then **~4 more years** to come online.
- Tech Insider reports a **~7 GW** US AI DC "capacity crisis" of delays/cancellations tied to power.

**Supply chain**
- Substation transformer lead times: **~24–30 months pre-2020 → ~5 years (≈160 weeks) in 2026**. [FACT]

**Water / cooling**
- US data centers consumed **~17–20 billion gallons** of water directly (2024–25); projected to **quadruple by 2030** (WestWater: +170% by end of decade).
- A single hyperscale facility can use **1–5 million gallons/day**.
- Water is now the **#2 constraint after power** — already causing permit denials, community opposition, and multi-year redesigns.

**Land, permitting & politics**
- 2026: **moratorium bills in 11 states**; dozens of municipalities enacted local construction pauses.
- New federal EPA cooling-water rules (NPDES permits) take full effect 2026; states (Florida, Minnesota, etc.) adding water-disclosure and zoning constraints.
- Water rights in the Southwest/West (prior-appropriation regimes) expose junior-rights data centers to curtailment risk.

**Implication for the project:** These are the "push" factors. Orbital compute sidesteps grid interconnection queues, transformer lead times, water-cooling permits, and local land politics entirely — at the cost of launch, orbital power generation, and radiative thermal management. The terrestrial constraints are real and quantified; whether orbital economics can beat them is the project's central open question.

---

## Sources

*Current scale & capacity*
- [JLL — Global data center sector to nearly double to 200GW](https://www.jll.com/en-us/newsroom/global-data-center-sector-to-nearly-double-to-200gw-amid-ai-infrastructure-boom)
- [BloombergNEF — AI Data Center Build Advances at Full Speed](https://about.bnef.com/insights/commodities/ai-data-center-build-advances-at-full-speed-five-things-to-know/)
- [Epoch AI — Global AI power capacity comparable to New York State](https://epoch.ai/data-insights/ai-datacenter-power)
- [JLL — 2026 Global Data Center Outlook](https://www.jll.com/en-us/insights/market-outlook/data-center-outlook)
- [Programs.com — Data Center Statistics 2026](https://programs.com/resources/data-center-statistics/)

*Gigawatt-scale facilities*
- [NextBigFuture — First Five AI Data Centers Over 1 GW, 2026–27](https://www.nextbigfuture.com/2025/11/first-five-ai-data-center-with-over-one-gigawatt-of-power-arriving-in-2026-2027.html)
- [The Data Center Engineer — Five AI data centers to reach 1 GW in 2026](https://thedatacenterengineer.com/news/five-ai-data-centers-to-reach-1-gw-power-capacity-in-2026-new-analysis-shows/)
- [Sherwood News — Biggest AI data center projects](https://sherwood.news/tech/clash-of-the-titans-here-are-the-biggest-ai-data-center-projects/)
- [Tom's Hardware — OpenAI / xAI Colossus scale](https://www.tomshardware.com/tech-industry/artificial-intelligence/openais-gargantuan-data-center-is-even-bigger-than-elon-musks-xai-colossus-worlds-largest-300-mw-ai-data-center-in-texas-could-reach-record-1-gigawatt-scale-by-next-year)

*Capex & spend*
- [CreditSights — Hyperscaler Capex 2026 Estimates](https://know.creditsights.com/insights/technology-hyperscaler-capex-2026-estimates/)
- [Futurum — AI Capex 2026: The $690B Infrastructure Sprint](https://futurumgroup.com/insights/ai-capex-2026-the-690b-infrastructure-sprint/)
- [IEEE ComSoc — Hyperscaler capex > $600bn in 2026](https://techblog.comsoc.org/2025/12/22/hyperscaler-capex-600-bn-in-2026-a-36-increase-over-2025-while-global-spending-on-cloud-infrastructure-services-skyrockets/)
- [Goldman Sachs — Why AI Companies May Invest More than $500B in 2026](https://www.goldmansachs.com/insights/articles/why-ai-companies-may-invest-more-than-500-billion-in-2026)
- [CNBC — Tech AI spending approaches $700B in 2026](https://www.cnbc.com/2026/02/06/google-microsoft-meta-amazon-ai-cash.html)

*Cost per GW*
- [Epoch AI — Total cost of ownership of a 1 GW AI data center](https://epoch.ai/data-insights/ai-datacenter-cost-breakdown)
- [Investing.com — How much does a GW of data center capacity cost](https://www.investing.com/news/stock-market-news/how-much-does-a-gw-of-data-center-capacity-actually-cost-4314046)
- [DCD — IBM CEO on gigawatt data center costs](https://www.datacenterdynamics.com/en/news/ibms-ceo-says-theres-no-way-for-gigawatt-data-centers-to-turn-a-profit/)

*Growth projections*
- [McKinsey — AI power: Expanding data center capacity to meet demand](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/ai-power-expanding-data-center-capacity-to-meet-growing-demand)
- [McKinsey — The cost of compute: a $7 trillion race](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/the-cost-of-compute-a-7-trillion-dollar-race-to-scale-data-centers)
- [Axios — Why the global AI data center boom is stalling](https://www.axios.com/2026/02/24/ai-data-center-boom-projects-numbers)

*Inference vs. training*
- [McKinsey — The next big shifts in AI workloads](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/the-next-big-shifts-in-ai-workloads-and-hyperscaler-strategies)
- [Introl — AI Inference vs Training Infrastructure Economics](https://introl.com/blog/ai-inference-vs-training-infrastructure-economics-diverging)
- [Deloitte — AI's next phase will demand more compute power](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/compute-power-ai.html)
- [MarketsandMarkets — AI Inference Market Size 2025–2030](https://www.marketsandmarkets.com/Market-Reports/ai-inference-market-189921964.html)
- [Grand View Research — AI Inference Market Report to 2030](https://www.grandviewresearch.com/industry-analysis/artificial-intelligence-ai-inference-market-report)

*Terrestrial constraints*
- [RMI — Interconnection queue as a barrier](https://rmi.org/interconnection-reform-ai-data-centers-generator-queues/)
- [Data Center Knowledge — Why AI DC projects face years of delays](https://www.datacenterknowledge.com/energy-power-supply/why-ai-data-center-projects-face-years-of-delays-after-approval)
- [Tech Insider — US AI Data Center Delays: 7 GW Capacity Crisis](https://tech-insider.org/us-ai-data-center-delays-cancellations-7gw-capacity-crisis-2026/)
- [Climate Solutions Law — Water rights and data center development](https://www.climatesolutionslaw.com/2026/04/the-new-battleground-water-rights-and-data-center-development-in-the-ai-era/)
- [MultiState — State Data Center Laws vs Federal AI Push 2026](https://www.multistate.us/insider/2026/4/14/federal-ai-data-center-policy-meets-resistance-from-state-lawmakers)
- [EESI — Data Centers and Water Consumption](https://www.eesi.org/articles/view/data-centers-and-water-consumption)

---

## Open Questions

1. **AI vs. total capacity definition.** Analysts disagree on what counts as "AI capacity" (GPU racks only? whole AI-purpose campuses?). The ~30 GW (2026 operational AI) vs. ~44 GW (2026 AI workload) vs. ~156 GW (2030 AI) figures use different boundaries. A reconciled definition would tighten the TAM.
2. **Bubble risk.** ~$5T+ of projected 2030 AI capex assumes AI revenue scales to justify it. Axios already reports stalling projects. The orbital thesis should stress-test against a slower-growth scenario.
3. **Revenue-per-GW proxy (A3).** We bridged a $-denominated services market to a GW-denominated capacity figure. A proper unit economics model (utilization, tokens/GW, pricing) would replace this crude proxy.
4. **Which inference workloads are orbit-suitable?** Latency-tolerant batch/async inference is the realistic target; real-time low-latency inference likely is not. Sizing the *orbit-addressable* subset of the ~90 GW inference figure is the next refinement.
5. **Orbital cost stack not addressed here.** This doc sizes *demand only*. Whether orbital compute beats terrestrial requires the launch/power/thermal cost model from the other project workstreams.
6. **Power vs. compute units.** Industry uses GW (power) as the unit; ultimately the product sold is compute (tokens/FLOPs). Efficiency gains (better GPUs/$/W) could decouple GW growth from compute growth and shift the TAM.
