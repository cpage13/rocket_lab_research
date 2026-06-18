# Cost and Unit Economics of Deploying and Upgrading Cellular Networks (5G Focus)

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:** This doc supplies the ground-network cost basis for a later space-vs-ground comparison. It borrows only the *comparison-framework shape* (capex per unit, capex as a percent of revenue, payback period) from [research/economics/ai_datacenter_tam.md](ai_datacenter_tam.md). It does not repeat that doc's data-center numbers. Everything below is terrestrial cellular (mobile) network economics, US-primary.

---

## Summary / Verdict

A terrestrial mobile network is a **high-capex, long-payback, capex-as-a-fraction-of-revenue business**, and that fraction is the single most portable number for comparing it to any alternative delivery method (including space). The headline anchors:

- **Capex intensity (capex as a percent of service revenue):** the most stable cross-operator metric. Global mobile peaked at **~19% in 2022** (the top of the 5G cycle) and is easing toward the mid-teens; North America ran **~16% in 2023-2024**, falling toward **~14-15%** by 2025-2026. [FACT]
- **Per cell site:** a **5G upgrade of an existing 4G macro site is ~$20K-$50K**; a **brand-new macro site is ~$100K-$300K all-in** (radios plus civil works plus tower), and complex/rural sites can exceed **$1M**. A small cell is **~$10K-$50K**. [FACT, multi-source on the ranges; the precise split is aggregator-sourced, see Confidence]
- **National 5G capex (US):** Accenture/CTIA's pre-rollout estimate was **~$275B over ~7 years** for nationwide 5G buildout; actual annual US wireless network capex has run **~$29-30B/yr** (CTIA) with total industry investment (including towers and indirect) around **~$63B in 2024** (WIA). [FACT]
- **Spectrum is a separate, very large line:** the US C-band auction alone raised **~$81B** (2021), the single most expensive mid-band 5G auction in the world. Spectrum is a one-time license cost layered on top of equipment capex. [FACT]
- **Cost structure:** the **RAN (radios plus baseband) is the dominant capex line at ~55-65% of 5G network capex** (up from ~45-50% in 4G); backhaul/transport is **~15-30%**; the rest is core, sites, and integration. On the opex side, **energy is ~20-40% of network opex** and a 5G site draws **~70-140% more power than a legacy 2/3/4G site**. [FACT on direction; component percentages are single-/aggregator-sourced, flagged below]
- **Payback:** operators and analysts cite a **~8-10 year breakeven** on 5G investment, consistent with a capital-intensive, slowly-monetized upgrade. [ESTIMATE / single-source, flagged]

**Confidence: medium-high** on capex intensity (multiple GSMA/PwC/MTN sources converge), the spectrum auction totals (FCC/S&P), and the macro-site upgrade-vs-newbuild ranges (multiple sources). **Medium** on the per-component cost-split percentages (RAN/backhaul/core), which lean on industry aggregators rather than audited operator disclosure. **Low-medium** on derived per-subscriber and per-POP figures (our own arithmetic, tagged [ESTIMATE]) and on the 8-10 year payback (thinly sourced).

---

## 1. Per Cell Site: Upgrade vs New Build, Macro vs Small Cell

This is the atomic unit of cellular cost. The single most important distinction is **upgrade an existing site** (cheap, reuses tower/power/backhaul) vs **build a new site** (expensive, full civil works).

| Site type | Cost (US) | What it covers | Tag |
|---|---|---|---|
| 5G **upgrade** of an existing 4G macro site | **~$20K-$50K** per site | swap/add radios on an existing tower; reuses structure, power, backhaul | [FACT] |
| **New** macro cell site, all-in | **~$100K-$300K** (avg often cited ~$250K) | radios + baseband + tower/structure + foundation + site acquisition + power + backhaul tie-in | [FACT] |
| Complex / specialty / difficult new site | **up to >$1M** | hard permitting, terrain, custom structure | [FACT] |
| **Small cell** (outdoor) | **~$10K-$50K** per node | low-power node on a pole/streetlight; site acquisition and power can exceed the radio cost | [FACT] |
| Rural macro site (vs urban) | **~2-3x** the per-site cost of urban | longer backhaul, power provisioning, lower site density | [ESTIMATE / aggregator] |

**Tower / civil works component (new build).** A new tower's *structure* cost depends on type: monopole **~$150K-$250K**, lattice **~$200K-$350K**, guyed **~$100K-$200K**, rooftop install **~$50K-$150K**. International comparison for the all-in tower build: **US ~$250K, Western Europe ~$135K, Latin America ~$110K**. 5G makes towers *more* expensive than 4G because the heavier/denser radio payload raises foundation and structural loads. [FACT on ranges; single dgtlinfra source for the international split, flagged]

**Equipment (radio + baseband) component.** A 5G macro base station's hardware (radio unit plus baseband unit) is **~$18K-$35K** in the US (2026). Open RAN / disaggregated units run **~15-25% lower hardware cost** but add integration expense. Larger "base station deployment" figures of **$100K-$500K** that appear in some sources are effectively *site-level* costs (equipment plus civil plus spectrum loading), not the radio box alone, which is the main reason quoted "per base station" numbers vary so widely. [FACT, with the definitional caveat]

**Why the upgrade path dominates the US story.** Most US 5G to date is mid-band overlay on **existing** macro towers, which is why annual network capex (~$29-30B/yr) is far below what a from-scratch national build would imply: operators are mostly paying the **$20K-$50K upgrade** cost per site, not the **$250K new-build** cost.

---

## 2. Cost Structure: Where the Money Goes (Equipment / Civil / Backhaul / Spectrum)

5G network capex splits into four buckets. The RAN dominates; spectrum is a separate one-time license layer.

| Component | Share of 5G network capex | Notes | Tag |
|---|---|---|---|
| **RAN** (radios + baseband) | **~55-65%** | up from ~45-50% in 4G; the dominant line | [FACT direction / aggregator on the exact %] |
| **Backhaul / transport** (fiber, microwave) | **~15-30%** | 5G needs ≥10 Gbps per site; C-RAN needs 25-100 Gbps fronthaul; underground fiber ~$25K-$150K per km | [FACT direction / aggregator] |
| **Core network** (incl. 5G Standalone core) | meaningful minority | a 5G SA core program is cited at **~$1B-$3B per operator** | [FACT / single-source] |
| **Civil works / sites** (towers, foundations, site acquisition, power) | varies; **up to ~40% of small-cell TCO** | for small cells, site acquisition + power can exceed the radio cost itself | [FACT / aggregator] |
| **Spectrum** | *separate one-time license* (see below) | not "network capex" but often the largest single cash outlay | [FACT] |

**Backhaul detail.** Fiber backhaul is **~15-30% of total deployment cost**; a single km of underground fiber can run **$25K-$150K+** depending on terrain and method. Every 5G-era site needs at least **10 Gbps**; centralized-RAN (C-RAN) architectures push fronthaul to **25-100 Gbps**. Satellite backhaul (relevant to the space comparison) is cited at **up to ~$500 per Mbps** for remote sites where fiber is impractical. [FACT, single-/aggregator-sourced]

### Spectrum: a large, separate, one-time cost

Spectrum licenses are bought at auction and sit *on top of* equipment capex. They are the reason national 5G economics can swing by tens of billions before a single radio is installed.

| Auction / market | Total raised | Notable bidders | Tag |
|---|---|---|---|
| **US C-band (Auction 107, 2020-21)** | **~$81B** gross (world's costliest mid-band auction; ~$0.94/MHz-pop) | Verizon ~$45.5B, AT&T ~$23.4B, T-Mobile ~$9.3B | [FACT, FCC/S&P] |
| US FCC auctions, cumulative | **>$80B** (C-band) within a larger multi-auction history | | [FACT] |
| Germany 5G (2019) | **~€6.5-6.6B** (~$0.16/MHz-pop) | DT ~€2.2B, Vodafone ~€1.9B, Telefónica ~€1.4B, Drillisch ~€1.1B | [FACT] |
| UK 3.4 GHz (2018) | ~$0.15/MHz-pop (price benchmark) | | [FACT] |
| India (2022 + 2024 combined) | **~₹1.71 lakh crore (~$20.5B)** | Jio ~$11B on spectrum; Airtel ~$5.2B | [FACT] |
| Brazil multi-band (2021) | **~$8.5B** commitments (BRL ~47.2B), heavy coverage *obligations* in lieu of cash | Vivo, Claro, TIM | [FACT] |

**Framing for the comparison:** in major markets a single operator can pay **>$1B** (often far more) just for spectrum rights. The US is an outlier on the high side ($81B C-band), Europe lower per MHz-pop, and emerging markets (Brazil) increasingly substitute **rollout obligations** for cash.

---

## 3. National / Aggregate Capex (US primary)

| Metric | Value | Source basis | Tag |
|---|---|---|---|
| US nationwide 5G buildout (pre-rollout estimate) | **~$275B over ~7 years** | Accenture for CTIA | [FACT / single framework, widely cited] |
| US annual wireless *network* capex (recent) | **~$29-30B/yr** (2024: ~$29B CTIA; ~$30B in 2020) | CTIA annual survey | [FACT] |
| US total wireless *infrastructure* investment (2024) | **~$63B** (incl. towers, indirect) | WIA 2024 | [FACT] |
| US total telco capex (mobile + fixed, 2024) | **~$80.5B**; capital intensity ~15.9% | MTN/industry | [FACT] |
| Big-3 mobile capex (2024) | AT&T ~$22.1B (incl. vendor financing), Verizon ~$17.1B, T-Mobile ~$8.8-9B | company guidance/results | [FACT] |
| North America mobile capex (2022-2025) | **~$204B** total; ~99% of it 5G | GSMA | [FACT] |

**US installed base (context for per-site and per-POP math):** ~**154,800** purpose-built towers and ~**248,050** macrocell sites at end-2024, plus ~**197,850** outdoor small cells and ~**802,500** indoor small-cell nodes; ~**651,000** total structures support wireless. ~**579M** total US wireless connections (2024), nearly half 5G. [FACT, WIA/CTIA]

---

## 4. Ongoing Opex and the Energy Line

Opex is where 5G quietly gets more expensive per site even as capex/site (upgrades) stays modest.

| Opex fact | Value | Tag |
|---|---|---|
| US wireless network operating expense (2024) | **~$53B/yr** | [FACT, WIA] |
| Energy as a share of network opex | **~20-40%** (some cite ~15-20% specific to 5G; ~4% of *total* telco opex in 2021 on a broader base) | [FACT range / sources differ] |
| 5G site power vs legacy site | **~+70%** (typical 5G site ~11.5 kW) up to **~2x** a 4G site; high-performance 5G up to **+140%** | [FACT] |
| RAN share of network energy | **~73%** of network energy is RAN; O-RAN radio units alone ~**60-80%** of total | [FACT / aggregator] |
| 5G opex vs 4G | **~+30-50%** higher operating cost | [ESTIMATE / aggregator] |
| Energy consumption 5G vs 4G | **~3-4x** higher | [ESTIMATE / aggregator] |

**Why this matters for a space comparison:** on the ground, **energy and the RAN dominate both capex and opex**. The RAN is ~55-65% of capex and ~73% of network energy; the radio is the cost center. Any alternative delivery (including orbital) is competing primarily against the RAN-plus-energy stack, not against the core or the spectrum line.

---

## 5. Financial Profile and Unit Economics

This section holds the most portable comparison metrics: **capex as a percent of revenue**, **cost per subscriber**, and **payback**.

### Capex intensity (capex as a percent of service revenue)

The single most stable cross-operator, cross-country metric.

| Region / scope | Capex intensity | Period | Tag |
|---|---|---|---|
| Global mobile (cycle peak) | **~19%** | end-2022 | [FACT, GSMA] |
| North America mobile | 17% (2022) → **16% (2023-2024)** → ~15% (2025) | trend | [FACT, GSMA] |
| US total telco | **~15.9%** | 2024 | [FACT, MTN] |
| Europe (total telco, highest region) | **~17.8%** | 3Q24 | [FACT, MTN] |
| Global all-telco, long-lived assets as % of revenue | 26.9% (2022) → **22.9% (2024)** | trend | [FACT, MTN] |

**Interpretation:** mobile-network capex runs **~14-19% of service revenue**, declining post-2022 as the heavy 5G build phase matured. This is the steady-state "cost to keep a terrestrial network competitive" expressed as a fraction of the revenue it produces. (Contrast framing only: AI data-center capex is a *multiple* of current revenue, not a low-teens percent of it; see [ai_datacenter_tam.md](ai_datacenter_tam.md). The two businesses sit at opposite ends of the capex-intensity spectrum, which is exactly why the ratio is the right axis to compare on.)

### Cost per subscriber (DERIVED)

> **FLAGGED ESTIMATE.** No clean per-subscriber capex benchmark surfaced in the sources; the figures below are our own arithmetic from aggregate capex and connection counts. Treat as order-of-magnitude, not a sourced fact.

| Derived metric | Arithmetic | Result | Tag |
|---|---|---|---|
| US annual network capex per connection | ~$29B / ~579M connections | **~$50/connection/yr** | [ESTIMATE] |
| US annual total infra investment per connection | ~$63B / ~579M connections | **~$110/connection/yr** | [ESTIMATE] |
| Europe capex per connection (sourced) | GSMA states **~€35/connection**, vs **~€70** for global "connectivity leaders" | €35 / €70 | [FACT, GSMA] |

The GSMA's **€35 vs €70 capex-per-connection** contrast (Europe vs leaders) is the cleanest *sourced* per-subscriber capex figure available and is the one to lead with; the US derived ~$50/connection/yr is consistent in magnitude. [FACT for the GSMA figure; ESTIMATE for the US derivation.]

### Cost per covered POP (DERIVED)

> **FLAGGED ESTIMATE.** "Cost per covered POP" is not directly reported in the sources. As a rough bound: ~$275B nationwide buildout (Accenture) over a US population of ~335M implies **~$820 per POP** for full 5G buildout *capex* (one-time, spectrum-inclusive framing). Spectrum auctions are independently benchmarked at **~$0.10-$3.00 per MHz per capita** internationally (US C-band ~$0.94/MHz-pop). [ESTIMATE for the $/POP; FACT for the $/MHz-pop benchmark.]

### Payback

- Cited 5G investment **breakeven ~8-10 years**. [ESTIMATE / single-source aggregator, flagged for the lead to corroborate.] This is consistent with a low-teens-percent capex-intensity business whose 5G revenue uplift has been slow to materialize (ARPU has been flat-to-declining in most markets, see below).
- **ARPU pressure** undercuts payback: global ARPU is forecast to **decline ~2%/yr to 2028**; European mobile ARPU adjusted for GDP was *lower* in 2024 (€14.9) than 2015 (€15.3). 5G has largely **not** delivered an ARPU premium, which is why payback is long and capex intensity is falling rather than rising. [FACT]

---

## 6. International and Global Context

US-primary above; this section adds the requested major countries and the global envelope. **China is excluded from the main analysis and noted separately at the end.**

| Market | 5G capex / investment | Spectrum cost | Notes | Tag |
|---|---|---|---|---|
| **United States** | ~$275B nationwide (Accenture); ~$29-30B/yr network capex | C-band ~$81B | upgrade-led; high spectrum cost | [FACT] |
| **Europe (region)** | **~€475B needed to 2035** for best-in-class; only ~€270B (57%) likely to materialize → **~€205B gap** | varies by country | capex/connection only **€35** vs €70 leaders; 5G SA reaches only ~2% of population | [FACT, GSMA] |
| **Germany** | operators said the auction left them short of build funds | **~€6.5-6.6B** | criticized as a "disaster"; ~$0.16/MHz-pop | [FACT] |
| **UK** | (part of European envelope) | 3.4 GHz ~$0.15/MHz-pop | benchmark only | [FACT] |
| **France** | (part of European envelope) | not isolated in sources | flagged gap, see Open Questions | [n/a] |
| **Japan** | **~$14B+** combined (4 carriers, ~5 yrs); Docomo ~$4.9B/yr (FY24); Rakuten ~¥1.8T (~$11.8B) cumulative from scratch | bundled / administrative | Rakuten built cloud-native from zero; KDDI-SoftBank share infra to cut capex | [FACT] |
| **India** | Jio ~$24B program (~$11B spectrum); Airtel peak ~₹25,300 cr/yr; industry ~$11-17B (2022-27) | ~$20.5B (2022+2024) | ~275K 5G base stations by mid-2023; now *scaling back* capex | [FACT] |
| **Brazil** | heavy *coverage obligations* substitute for cash | ~$8.5B commitments | obligations: capitals by 2022, then tiered city deadlines to 2028 | [FACT] |

### Global envelope

- **Global mobile operator capex 2023-2030: ~$1.5 trillion**, >75% of it 5G-related. [FACT, GSMA Intelligence], *single primary source (GSMA); widely requoted. Lead should note it is one institution's projection.*
- Global telecom (all-operator) revenue **~$1.78T (2024)**, roughly flat; global telco capex **dipped below ~$300B/yr** in 2024 (~$294.6B annualized 3Q24, -7.7% YoY). [FACT, MTN/PwC]
- Global 5G-specific spend cited at **~$10B (2022)** rising to **>$1.1T cumulative by 2025** and **>$2T by 2030** in one aggregator framing. [ESTIMATE / aggregator, treat the cumulative figures as soft.]

### China (separate note, excluded from main analysis)

China is excluded from the comparison set above. For context only: China Mobile alone targeted ~**2.35M 5G base stations** by end-2024, and China leads the world on 5G Standalone reach (~80% of population in Greater China per GSMA). China's scale and state-directed buildout make its per-site and per-POP economics non-comparable to the Western operator model this doc uses, which is why it is held aside.

---

## Sources

*Per-site, equipment, civil works, cost structure*
- [PatentPC, 5G Infrastructure Costs: What Telcos Are Paying](https://patentpc.com/blog/5g-infrastructure-costs-what-telcos-are-paying)
- [dgtlinfra, How Much Does it Cost to Build a Cell Tower?](https://dgtlinfra.com/how-much-does-it-cost-to-build-a-cell-tower/)
- [Bankai Infotech, C-RAN & Open RAN Cut 5G Deployment Costs](https://bankaiinfotech.com/blogs/how-ran-solutions-enable-5g-growth/)
- [IndexBox, US 5G Base Station Market (hardware pricing)](https://www.indexbox.io/store/united-states-5g-base-station-market-analysis-forecast-size-trends-and-insights/)

*National / aggregate capex and infrastructure counts*
- [Accenture (for CTIA), ~$275B nationwide 5G; ~$500B GDP](https://www.thefastmode.com/technology-and-solution-trends/9791-wireless-operators-in-us-to-invest-275-billion-to-build-out-nationwide-5g-network-accenture-strategy)
- [CTIA, 2024 Annual Survey Highlights](https://www.ctia.org/news/2024-annual-survey-highlights)
- [WIA, Wireless Infrastructure By the Numbers 2024](https://wia.org/wireless-infrastructure-by-the-numbers-2024/)
- [Wireless Estimator, Inside WIA's 2024 numbers ($63B)](https://wirelessestimator.com/articles/2025/inside-wias-2024-numbers-63%E2%80%AFbillion-and-368750-jobs-are-powering-5g/)

*Capex intensity and operator financials*
- [GSMA (via TelecomLead), 5G to account for all NA mobile capex; 16% capex/revenue](https://telecomlead.com/5g/5g-to-account-for-all-mobile-capex-in-north-america-gsma-106720)
- [GSMA Intelligence, Mobile capex to reach $1.5 trillion 2023-2030](https://www.gsmaintelligence.com/research/the-spend-of-an-era-mobile-capex-to-reach-1-5-trillion-for-2023-2030)
- [MTN Consulting / ResearchAndMarkets, Global telco capex below $300B; capital intensity](https://www.businesswire.com/news/home/20250210133868/en/Telecommunications-Network-Operators-2024-Market-Review-Telco-Topline-Rebounds-But-Annualized-Capex-Dips-Below-%24300B-Mark-Amid-Continued-Spending-Cuts---ResearchAndMarkets.com)
- [Wireless Estimator, Big-3 carrier capex 2024](https://wirelessestimator.com/articles/2024/capex-climbs-at-big-3-carriers-offering-the-industry-niche-opportunities/)
- [TeleGeography, 2025 Mobile Market Summary (capex/ARPU)](https://resources.telegeography.com/2025-mobile-market-summary)
- [PwC, Global telecoms revenue $1.1T+, ARPU outlook](https://www.pwc.com/gx/en/news-room/press-releases/2025/pwc-global-telecoms-outlook.html)

*Spectrum auctions*
- [S&P Global, US C-band, world's costliest mid-band auction](https://www.spglobal.com/market-intelligence/en/news-insights/research/us-c-band-auction-becomes-worlds-costliest-mid-band-5g-auction-yet)
- [Telecompetitor, C-band auction ~$81B](https://www.telecompetitor.com/c-band-spectrum-auction-ends-with-haul-of-almost-81-billion-shattering-records/)
- [FCC, C-band winning bidders](https://www.fcc.gov/document/fcc-announces-winning-bidders-c-band-auction)
- [Fierce Network, Germany 5G auction €6.6B](https://www.fierce-network.com/regulatory/germany-ends-5g-spectrum-auction-eu6-6-billion-revenue)
- [RCR Wireless, Brazil raises $8.5B in 5G auction](https://www.rcrwireless.com/20211108/featured/brazil-raises-total-8-billion-5g-spectrum-auction)

*Opex and energy*
- [GSMA, Energy Efficiency: An Overview](https://www.gsma.com/solutions-and-impact/technologies/networks/gsma_resources/energy-efficiency-an-overview/)
- [STL Partners, Telco Network Energy Efficiency: the RAN](https://stlpartners.com/articles/network-innovation/telco-network-energy-efficiency-ran/)
- [TelecomLead, 5G operator strategies to cut power cost](https://telecomlead.com/5g/5g-mobile-operator-strategies-to-cut-their-huge-power-cost-94645)

*International (Europe, Japan, India, Brazil)*
- [GSMA, €475B required for Europe's 5G journey (€205B gap; €35 vs €70/connection)](https://www.gsma.com/newsroom/press-release/e475-billion-required-for-europe-to-complete-its-5g-journey-and-regain-digital-leadership-new-gsma-study-finds/)
- [US Dept of Commerce, Japan's 5G Networks (~$14B, 4 carriers)](https://www.trade.gov/market-intelligence/japans-5g-networks)
- [LightReading, How India's Jio and Airtel are funding 5G](https://www.lightreading.com/broadband/how-india-s-jio-and-airtel-are-funding-5g)
- [Business Standard, India 5G expansion slowdown, Jio/Airtel capex](https://www.business-standard.com/industry/news/india-5g-expansion-slowdown-jio-airtel-capex-125030700219_1.html)
- [Developing Telecoms, Brazil 5G spectrum auction concluded](https://developingtelecoms.com/telecom-business/market-reports-with-buddecom/12733-brazil-s-regulator-concludes-5g-spectrum-auction.html)

---

## Confidence

**Medium-high (well-corroborated):**
- Capex intensity ~14-19% of revenue, peaking 2022 (GSMA, MTN, PwC converge).
- Spectrum auction totals: US C-band ~$81B, Germany ~€6.5B, Brazil ~$8.5B, India ~$20.5B (FCC, S&P, national regulators).
- Macro-site economics: **$20K-$50K upgrade** vs **$100K-$300K new build** vs **$10K-$50K small cell** (multiple independent sources agree on the ranges).
- US infrastructure counts and aggregate capex (CTIA, WIA, primary industry bodies).

**Medium (single-source or aggregator, corroborate before load-bearing use):**
- The **RAN ~55-65% / backhaul ~15-30%** capex-split percentages come from industry aggregators (PatentPC, Bankai), not audited operator filings. The *direction* (RAN dominant, rising from 4G) is well established; the exact percentages are soft.
- The McKinsey "**~60% capex increase 2020-2025, roughly doubling TCO**" figure for a European country is referenced in this research via a quoting search result; the primary McKinsey page ("The road to 5G") was not directly retrievable (timeout/403). Stated in this doc's narrative but **not** placed in the claims table pending primary confirmation.
- Energy as 20-40% of opex, 5G opex +30-50% vs 4G, energy 3-4x: aggregator-sourced; ranges vary by source.
- 5G core ~$1B-$3B/operator, satellite backhaul ~$500/Mbps: single-source.

**Low-medium (our own arithmetic, explicitly derived):**
- Per-subscriber (~$50-$110/connection/yr US) and per-POP (~$820/POP) figures are derived from aggregate capex divided by counts. The only *sourced* per-subscriber figure is GSMA's €35 vs €70/connection.
- The ~8-10 year payback is thinly sourced (one aggregator); flagged for corroboration.

---

## Open Questions

1. **Primary McKinsey "road to 5G" TCO figure.** The ~60% capex increase / TCO-doubling number is currently second-hand. Retrieve the primary McKinsey report to confirm the percentage and the country/scope it applies to before treating it as a hard claim.
2. **RAN/backhaul/core cost-split provenance.** The 55-65% RAN share is aggregator-sourced. An operator-disclosed or analyst-firm (Dell'Oro, Omdia) breakdown would harden it.
3. **France (and UK) isolated figures.** Both are folded into the European €475B envelope; standalone national 5G capex and spectrum figures for France in particular did not surface cleanly and should be filled if a per-country European comparison is needed.
4. **Clean per-subscriber and per-POP capex.** Replace the derived US figures with a sourced operator benchmark (capex / net adds, or capex / covered POPs) if one can be found; GSMA's €35/€70 is the current anchor.
5. **Payback corroboration.** The 8-10 year breakeven needs a second source; payback is highly sensitive to ARPU (which is flat-to-declining), so a scenario range may be more honest than a point estimate.
6. **Spectrum treatment in any comparison.** Spectrum is a one-time license, not recurring network capex, and varies ~30x per MHz-pop across markets (US ~$0.94 vs Germany ~$0.16). A later synthesis must decide whether to include or exclude spectrum when comparing ground-network cost to an alternative that needs no terrestrial spectrum license.

---

## Claims Table

| COMM- id | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-001 | Mobile capex intensity (capex as % of service revenue), global peak | ~19% at end-2022 | [FACT] | GSMA Intelligence; GSMA via TelecomLead |
| COMM-002 | North America mobile capex/revenue | 17% (2022) → ~16% (2023-24) → ~15% (2025) | [FACT] | GSMA via TelecomLead |
| COMM-003 | US total telco capital intensity | ~15.9% (2024) | [FACT] | MTN/ResearchAndMarkets |
| COMM-004 | 5G upgrade of existing 4G macro site | ~$20K-$50K per site | [FACT] | PatentPC; whatsag/search corroboration |
| COMM-005 | New macro cell site, all-in (US) | ~$100K-$300K (avg ~$250K); up to >$1M complex | [FACT] | PatentPC; dgtlinfra |
| COMM-006 | Small cell (outdoor) deployment | ~$10K-$50K per node | [FACT] | PatentPC; FCC catalog |
| COMM-007 | 5G macro base station hardware (radio+baseband) | ~$18K-$35K (US, 2026) | [FACT] | IndexBox/search |
| COMM-008 | Tower build all-in, international | US ~$250K; W.Europe ~$135K; LatAm ~$110K | [FACT] single-source | dgtlinfra |
| COMM-009 | RAN share of 5G network capex | ~55-65% (up from ~45-50% in 4G) | [FACT direction / aggregator] | PatentPC; Bankai |
| COMM-010 | Backhaul/transport share of deployment | ~15-30%; fiber ~$25K-$150K/km | [FACT / aggregator] | PatentPC |
| COMM-011 | 5G Standalone core program per operator | ~$1B-$3B | [FACT] single-source | PatentPC |
| COMM-012 | US C-band spectrum auction total | ~$81B gross (~$0.94/MHz-pop) | [FACT] | S&P Global; FCC; Telecompetitor |
| COMM-013 | US C-band bidders | Verizon ~$45.5B; AT&T ~$23.4B; T-Mobile ~$9.3B | [FACT] | S&P Global; FCC |
| COMM-014 | Germany 5G spectrum auction | ~€6.5-6.6B (~$0.16/MHz-pop) | [FACT] | Fierce; PolicyTracker |
| COMM-015 | India 5G spectrum (2022+2024) | ~₹1.71 lakh cr (~$20.5B) | [FACT] | LightReading; Business Standard |
| COMM-016 | Brazil 5G auction commitments | ~$8.5B (BRL ~47.2B), obligation-heavy | [FACT] | RCR Wireless; Developing Telecoms |
| COMM-017 | US nationwide 5G buildout estimate | ~$275B over ~7 years | [FACT] single framework | Accenture for CTIA |
| COMM-018 | US annual wireless network capex (recent) | ~$29-30B/yr | [FACT] | CTIA |
| COMM-019 | US total wireless infrastructure investment (2024) | ~$63B | [FACT] | WIA; Wireless Estimator |
| COMM-020 | US wireless network opex (2024) | ~$53B/yr | [FACT] | WIA |
| COMM-021 | Energy as share of mobile network opex | ~20-40% | [FACT range] | GSMA; STL Partners |
| COMM-022 | 5G site power vs legacy site | +~70% (~11.5 kW typical) up to ~2x; up to +140% high-perf | [FACT] | TelecomLead; GSMA |
| COMM-023 | RAN share of network energy | ~73% (O-RAN radio units ~60-80%) | [FACT / aggregator] | STL Partners |
| COMM-024 | 5G opex vs 4G | ~+30-50% | [ESTIMATE / aggregator] | PatentPC |
| COMM-025 | Global mobile operator capex 2023-2030 | ~$1.5 trillion (>75% 5G) | [FACT] single primary (GSMA) | GSMA Intelligence |
| COMM-026 | Europe 5G investment need to 2035 | ~€475B needed; ~€270B likely; ~€205B gap | [FACT] | GSMA |
| COMM-027 | Europe capex per connection vs leaders | ~€35 vs ~€70 | [FACT] | GSMA |
| COMM-028 | Japan 5G capex (4 carriers, ~5 yrs) | ~$14B+ combined; Rakuten ~$11.8B cumulative from scratch | [FACT] | US Dept of Commerce |
| COMM-029 | US wireless connections (2024) | ~579M (nearly half 5G) | [FACT] | CTIA/WIA |
| COMM-030 | US macrocell sites / towers (end-2024) | ~248,050 macrocell sites; ~154,800 purpose-built towers | [FACT] | WIA |
| COMM-031 | 5G investment payback / breakeven | ~8-10 years | [ESTIMATE] single-source | PatentPC |
| COMM-032 | Derived US network capex per connection | ~$50-$110/connection/yr | [ESTIMATE] own arithmetic | derived (CTIA/WIA ÷ connections) |
| COMM-033 | Derived US 5G buildout per POP | ~$820/POP (one-time) | [ESTIMATE] own arithmetic | derived ($275B ÷ ~335M) |
| COMM-034 | Global telecom (all-operator) revenue / capex | ~$1.78T revenue (2024); capex ~<$300B/yr | [FACT] | MTN; PwC |
| COMM-035 | (China, separate note) China Mobile 5G base stations target | ~2.35M by end-2024 | [FACT] | search/TelecomLead |
