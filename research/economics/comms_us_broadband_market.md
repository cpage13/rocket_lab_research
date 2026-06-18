# US Broadband Market, Size, Provider Financials & the Diminishing-Returns Question

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:** [research/economics/ai_datacenter_tam.md](./ai_datacenter_tam.md) (template and house style; that doc sizes AI compute demand, this one sizes the terrestrial broadband market that a space-based comms business would compete with or sell into).

> **Reading guide:** Each hard number is tagged **[FACT]** (reported / filed 2025–26 data), **[ESTIMATE]** (third-party market-research sizing or our own arithmetic), or **[PROJECTION]** (forward forecast). Hard numbers are cross-checked against 2+ independent sources where possible; single-source figures are flagged inline as **single source**.

> **Scope note:** This doc covers the **US fixed (ground) broadband market**: cable, fiber-to-the-home (FTTH), DSL/copper, and terrestrial fixed wireless access (FWA). Satellite broadband (Starlink, etc.) is treated only as a competitive reference, not sized here. **China is excluded** from the analysis; see the single aside in Section 1.

---

## Summary / Verdict

- **Market size.** The US fixed broadband services market is roughly **$63–92 billion in annual revenue (2025)** depending on definition. [Grand View Research](https://www.grandviewresearch.com/horizon/outlook/fixed-broadband-services-market/united-states) puts US **fixed broadband services at ~$63.6B (2025)**; [Statista](https://www.statista.com/topics/12786/fixed-broadband-in-the-united-states/) reports **~$92B of US fixed data revenue (2023)** across a broader subscription set; [Mordor](https://www.mordorintelligence.com/industry-reports/north-america-fixed-broadband-market) sizes **all of North America at ~$100.5B (2025)**. **[ESTIMATE]**, market-research figures, definitions vary. A defensible single number for **US residential + business fixed broadband is ~$70–95B/yr**.
- **Subscribers.** There are roughly **~115–130 million US fixed broadband connections**. The top providers (cable + telco + FWA, ~96% of the market) account for **~114.7M subscribers**, of which top cable is **~76M** ([Leichtman](https://www.lightreading.com/broadband/about-3-5m-added-broadband-from-top-providers-in-2023-leichtman-research-group)). **[FACT/ESTIMATE]**
- **Who leads.** By subscribers the order is **Comcast (31.3M) > Charter (29.7M) > Verizon (16.3M post-Frontier) > AT&T (~14.3M) > T-Mobile FWA (~8M) > Cox (~6M) > Altice/Optimum (4.2M)**. By **market cap** the order inverts toward the wireless-heavy telcos: **T-Mobile (~$216B) > Verizon (~$191-201B) > AT&T (~$156-160B) > Comcast (~$81B) > Charter (~$20B)**. The pure-play cable broadband operators are the *smallest* by market cap despite the *largest* subscriber bases. **[FACT]**
- **The market is consolidating and shrinking at the top.** Cable broadband (Comcast, Charter) is **losing subscribers** to FWA and fiber. Two megadeals are in flight: **Charter–Cox** (~$34.5B, creates the new #1 with ~26% of connections) and **Verizon–Frontier** (~$20B, closed Feb 2026, ~16.3M combined broadband connections). **[FACT]**
- **Diminishing returns is real and well-evidenced.** Willingness-to-pay for speed is **sharply concave**: a peer-reviewed discrete-choice study finds households value **~$0.02 per Mbps** going from 100 to 1,000 Mbps, versus **~$2.34 per Mbps** at the low end (4→10 Mbps). Despite **91% gigabit availability, only ~30% of homes subscribe to gigabit**; most pick **200–500 Mbps**, and many **refuse a ~$30/mo premium** for gigabit. **ARPU is flat-to-declining** at the largest operators (Comcast broadband ARPU **-3.1% YoY to $73.65** in Q1 2026). **[FACT]**

**Confidence: medium-high.** Provider financials and subscriber counts come directly from 2025–26 SEC filings and earnings (high confidence). Total-market revenue is medium confidence (research-firm definitions diverge by ~40%). The diminishing-returns conclusion is high confidence: multiple independent academic and industry sources converge.

---

## 1. Total US Broadband Market Size & Revenue

### Market revenue (2025), by source

| Source | Scope | Annual revenue | Tag |
|---|---|---|---|
| [Grand View Research](https://www.grandviewresearch.com/horizon/outlook/fixed-broadband-services-market/united-states) | US fixed broadband services | **~$63.6B (2025)** | [ESTIMATE] |
| [Statista](https://www.statista.com/topics/12786/fixed-broadband-in-the-united-states/) | US fixed data revenue | **~$92B (2023)** | [ESTIMATE] |
| [Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/north-america-fixed-broadband-market) | North America fixed broadband (all) | **~$100.5B (2025)**, → ~$159.8B by 2030 | [ESTIMATE/PROJECTION] |
| [Precedence Research](https://www.precedenceresearch.com/broadband-services-market) | Global broadband services | → ~$1,397.9B by 2035 (global) | [PROJECTION] |

The spread (~$63.6B to ~$100.5B) is a **definitional** artifact: the narrow figure is residential + business *fixed broadband access service*; the broader figures fold in adjacent fixed data, bundled video/voice attach, and (for Mordor) Canada and Mexico. **A defensible US-only residential + business fixed broadband number is ~$70–95B/yr.** **[ESTIMATE]**

### Segmentation

- **Residential vs. business.** Residential is the large majority. [Mordor](https://www.mordorintelligence.com/industry-reports/north-america-fixed-broadband-market) reports **residential = 85.5% of the North America fixed broadband market (2024)**, with commercial growing faster (~11.5% CAGR 2025–30). **[ESTIMATE]**
- **By technology.** Fiber is now the largest connection type by revenue: [Grand View](https://www.grandviewresearch.com/horizon/outlook/fixed-broadband-services-market/united-states) puts **fiber at ~55.75% of 2025 revenue**, with cable (DOCSIS) the other major share and DSL/copper in terminal decline. **[ESTIMATE]**
- **By share of connections (Q3 2025).** Top **cable** providers hold **~62.5% of broadband connections** ([Leichtman via Light Reading](https://www.lightreading.com/broadband/top-us-broadband-operators-added-840k-subs-in-q2)); telco fiber/DSL and FWA split the rest. **[FACT]**

> **China aside (excluded from analysis):** China is the world's largest fixed-broadband market by subscribers (hundreds of millions of FTTH lines, state-directed operators China Telecom / China Mobile / China Unicom). It is structurally walled off from US providers and irrelevant to a Rocket Lab serving thesis, so it is noted here once and excluded everywhere below.

### Subscriber base (US)

| Metric | Value | Tag |
|---|---|---|
| US fixed broadband connections (total) | **~115–130M** | [ESTIMATE] |
| Top-provider subscribers (~96% of market) | **~114.7M** | [FACT] |
| Top **cable** broadband subscribers | **~76M** | [FACT] |
| Top **wireline/telco** broadband subscribers | **~30.7M** | [FACT] |
| Top **fixed wireless (FWA)** subscribers | **~13–14M** (and rising fast) | [FACT] |

Subscriber-base totals are from [Leichtman Research Group](https://www.lightreading.com/broadband/about-3-5m-added-broadband-from-top-providers-in-2023-leichtman-research-group) (2023 base of ~114.7M; FWA has grown materially since). **[FACT/ESTIMATE]**

---

## 2. Provider-by-Provider Financial Benchmarks

> All market caps and stock prices are **as of June 17, 2026** unless noted; revenue/net income are **full-year 2025** unless noted; subscriber and ARPU figures are the most recent reported (Q4 2025 or Q1 2026). Market caps and TTM financials from [stockanalysis.com](https://stockanalysis.com/) and [companiesmarketcap.com](https://companiesmarketcap.com/); subscriber/ARPU from company earnings.
>
> **Important:** These are **whole-company** financials. Comcast and AT&T/Verizon revenue and net income include large non-broadband segments (media/theme parks for Comcast; wireless for AT&T/Verizon). Broadband is a *segment* inside these, not the whole company. The pure-play comparators are Charter, Altice, and (private) Cox.

### 2.1 Comcast / Xfinity (NASDAQ: CMCSA), broadband #1 by subscribers

| Benchmark | Value | Tag |
|---|---|---|
| Market cap | **~$81B** | [FACT] |
| Stock price | **~$22.69** (down ~4% on the day; near 52-wk lows) | [FACT] |
| Revenue (FY2025) | **~$123.7B** (flat YoY) | [FACT] |
| Net income (FY2025) | **~$20.0B** (+~24% YoY) | [FACT] |
| Net margin | **~16%** | [FACT] |
| Domestic broadband subscribers | **31.3M** (−711K in 2025) | [FACT] |
| Broadband ARPU | **$73.65** (−3.1% YoY, Q1 2026) | [FACT] |
| P/E | ~4.6 (deeply value-rated) | [FACT] |

Comcast is the **subscriber leader but is losing broadband customers** and is priced like a declining business (P/E ~4.6, ~5.8% dividend yield). Whole-company net income is high because of NBCUniversal/theme parks, not broadband growth. Sources: [stockanalysis.com (CMCSA)](https://stockanalysis.com/stocks/cmcsa/), [Comcast FY2025 10-K (SEC)](https://www.sec.gov/Archives/edgar/data/0001166691/000162828026004994/cmcsa-20251231.htm), [Fierce Network, Q1 2026 ARPU](https://www.fierce-network.com/broadband/comcasts-q1-2026-broadband-losses-were-less-bad-expected). **[FACT]**

### 2.2 Charter / Spectrum (NASDAQ: CHTR), broadband #2; the cleanest broadband pure-play

| Benchmark | Value | Tag |
|---|---|---|
| Market cap | **~$20B** | [FACT] |
| Stock price | **~$142** (down ~14% post-Q1-2026 earnings) | [FACT] |
| Revenue (FY2025) | **~$54.8B** (−0.6% YoY) | [FACT] |
| Net income (FY2025) | **~$5.0B** | [FACT] |
| Net margin | **~9%** | [FACT] |
| Internet customers | **29.7M** (−455K YoY by Q1 2026) | [FACT] |
| Adjusted EBITDA (FY2025) | **~$22.7B** (+0.6%) | [FACT] |

Charter is the best read on **standalone broadband economics**: ~$55B revenue, ~$5B net income, ~$22.7B EBITDA. It is **shrinking in subscribers** and the market has punished it hard (market cap ~$20B against ~$55B revenue; the stock fell ~14% on Q1 2026 results). Sources: [Charter FY2025 results](https://corporate.charter.com/newsroom/charter-announces-fourth-quarter-and-full-year-2025-results), [Charter Q1 2026 10-Q (SEC)](https://www.sec.gov/Archives/edgar/data/0001091667/000109166726000028/chtr-20260331.htm), [companiesmarketcap.com (CHTR)](https://companiesmarketcap.com/charter-communications/marketcap/). **[FACT]**

### 2.3 AT&T (NYSE: T), #3 broadband; telco with large wireless

| Benchmark | Value | Tag |
|---|---|---|
| Market cap | **~$156-160B** | [FACT] |
| Stock price | **~$22.44** | [FACT] |
| Revenue (FY2025, whole company) | **~$125.7B** (+2.7%) | [FACT] |
| Net income (FY2025, whole company) | **~$21.9B** (sharp YoY rise) | [FACT] |
| Net margin (whole company) | **~17%** | [FACT] |
| Fiber subscribers | **~10.4M** (end-2025) | [FACT] |
| FWA ("Internet Air") subscribers | growing; ~292K added in Q1 2026 | [FACT] |
| Combined broadband subs (fiber + FWA) | **~14.3M** (single source, see note) | [ESTIMATE] |
| Fiber locations passed | **>37M** | [FACT] |

AT&T is a **broadband *grower*** (record 584K internet net adds in Q1 2026: 292K fiber + 292K FWA), unlike cable. Note: the whole-company revenue/net income includes its large **wireless** business; broadband is a minority of the total. AT&T is also **acquiring Lumen's ~1M-subscriber consumer fiber business** for ~$5.75B. Sources: [stockanalysis.com (T)](https://stockanalysis.com/stocks/t/), [AT&T Q1 2026 earnings](https://about.att.com/story/2026/1q-earnings.html), [BigGo, record fiber+FWA adds](https://finance.biggo.com/news/US_T_2026-04-22). The ~14.3M combined figure (10.4M fiber + ~3.9M FWA) is **single source** synthesis, the lead should confirm the FWA count. **[ESTIMATE]**

### 2.4 Verizon, Fios + FWA; #3-4 broadband, now bigger post-Frontier (NYSE: VZ)

| Benchmark | Value | Tag |
|---|---|---|
| Market cap | **~$191-201B** | [FACT] |
| Stock price | **~$45.84** | [FACT] |
| Revenue (FY2025, whole company) | **~$138.2B** (+2.5%) | [FACT] |
| Net income (FY2025, whole company) | **~$17.2-17.6B** (−1.9%) | [FACT] |
| Net margin (whole company) | **~12%** | [FACT] |
| Fios internet connections | **7.328M** (end-2025) | [FACT] |
| FWA subscribers | **~5.7M** (Q4 2025) | [FACT] |
| Total broadband (post-Frontier close) | **>16.3M** fiber + FWA | [FACT] |
| Consumer Fios revenue | **~$2.9B/quarter** (Q1 2025) | [FACT] |

Verizon **closed the ~$20B Frontier acquisition in Feb 2026**, adding ~2.2M fiber subs and pushing combined broadband past **16.3M connections**. Like AT&T, whole-company financials are wireless-dominated. Sources: [stockanalysis.com (VZ)](https://stockanalysis.com/stocks/vz/), [Verizon Q4/FY2025 8-K (SEC)](https://www.sec.gov/Archives/edgar/data/0000732712/000073271226000003/a2025q4exhibit99.htm), [Verizon, Frontier close](https://www.verizon.com/about/news/verizon-and-frontier-regulatory-approval). **[FACT]**

### 2.5 T-Mobile, FWA challenger (NASDAQ: TMUS)

| Benchmark | Value | Tag |
|---|---|---|
| Market cap | **~$216B** (largest of the group) | [FACT] |
| FWA broadband subscribers | **~8M** (Q3 2025) | [FACT] |
| FWA net adds (2025) | **~1.8M** | [FACT] |
| Long-term FWA target | **~12M by 2028** | [PROJECTION] |

T-Mobile has **no legacy fixed plant**: its home broadband is entirely **5G fixed wireless**, which is why it is taking the *majority of new broadband net adds* nationally. Whole-company financials are overwhelmingly wireless; FWA is a small but fast-growing slice. Note: T-Mobile FWA delivers ~100–300 Mbps typical, *below* fiber/cable peaks, which ties directly to the diminishing-returns thesis (Section 3): customers accept "good enough" speed for price. Sources: [Light Reading, FWA 2025 review](https://www.lightreading.com/fixed-wireless-access/2025-in-review-fwa-s-fangs-stay-sharp), [Fierce, FWA capacity](https://www.fierce-network.com/broadband/big-3-now-have-room-32m-fwa-customers), [MacroTrends (TMUS market cap)](https://www.macrotrends.net/stocks/charts/TMUS/t-mobile-us/market-cap). **[FACT/PROJECTION]**

### 2.6 Smaller / private / consolidating ground providers

| Provider | Broadband subs | Revenue | Status | Tag |
|---|---|---|---|---|
| **Cox Communications** (private) | **~6M** residences+businesses | **~$6.7B** | Private (Cox Enterprises); **merging with Charter** (~$34.5B combined value, Charter/Spectrum brand) | [FACT/ESTIMATE] |
| **Altice USA / Optimum** (NYSE: OPTU) | **4.2M** (Q3 2025; −58K in quarter) | ~$2.11B/quarter (−5.4% YoY) | Public, shrinking; fiber base ~703K | [FACT] |
| **Frontier** | **~2.2M fiber** (25 states) | derives >50% of revenue from fiber | **Acquired by Verizon (closed Feb 2026)** | [FACT] |
| **Lumen** (mass-market fiber) | **~1M** subs (>4M locations) | n/a (segment) | **Being acquired by AT&T (~$5.75B)** | [FACT] |

Cox figures are **single source** ([Cox fact sheet / Wikipedia](https://en.wikipedia.org/wiki/Cox_Communications)); as a private company its financials are not filed. The lead should treat Cox's ~$6.7B revenue and ~6M subs as approximate. Altice: [Q3 2025 results](https://investors.optimum.com/news-events/press-releases/detail/225/altice-usa-reports-third-quarter-2025-results). Frontier/Lumen consolidation: [Verizon–Frontier](https://www.verizon.com/about/news/verizon-to-acquire-frontier), [AT&T–Lumen](https://broadbandbreakfast.com/at-t-paying-5-75-billion-for-lumens-consumer-fiber-business/). **[FACT/ESTIMATE]**

### 2.7 Cross-provider summary

| Provider | Broadband subs | Market cap | FY2025 revenue (co.) | FY2025 net income (co.) | Notes |
|---|---|---|---|---|---|
| Comcast | **31.3M** | ~$81B | ~$123.7B | ~$20.0B | Subs declining; media-heavy |
| Charter | **29.7M** | ~$20B | ~$54.8B | ~$5.0B | Cleanest pure-play; subs declining |
| Verizon | **16.3M** | ~$191-201B | ~$138.2B | ~$17.2-17.6B | +Frontier; wireless-heavy |
| AT&T | **~14.3M** | ~$156-160B | ~$125.7B | ~$21.9B | Broadband grower; wireless-heavy |
| T-Mobile | **~8M (FWA)** | ~$216B | (wireless co.) | (wireless co.) | All-FWA; fastest net adds |
| Cox | **~6M** | private | ~$6.7B | n/a | Merging into Charter |
| Altice/Optimum | **4.2M** | small-cap | ~$8.4B (annualized) | n/a | Shrinking |

**The structural read:** the largest *broadband* subscriber bases (Comcast, Charter) carry the *smallest* market caps and the *weakest* growth. Investor value sits with the **wireless** balance sheets (T-Mobile, Verizon, AT&T). A new entrant selling *broadband connectivity* is entering a market where the incumbents' core product is **flat-to-shrinking and de-rated**. **[FACT]**

---

## 3. The Diminishing-Returns Question

**Verdict on this section: high confidence.** The evidence that broadband value *plateaus* past a few hundred Mbps is strong and converges across a peer-reviewed willingness-to-pay study, industry pricing behavior, and operator ARPU trends.

### 3.1 Willingness-to-pay is sharply concave in speed

The cleanest evidence is the discrete-choice study **Liu, Prince & Wallsten, "Distinguishing Bandwidth and Latency in Households' Willingness-to-Pay for Broadband Internet Speed"** ([SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2942236), [Information Economics and Policy 2018](https://ideas.repec.org/a/eee/iepoli/v45y2018icp1-15.html), [Tech Policy Institute PDF](https://techpolicyinstitute.org/wp-content/uploads/2017/08/Distinguishing-Bandwidth-and-Latency-in-Households-Willingness-to-Pay-for.pdf)). Marginal willingness-to-pay per Mbps **collapses as speed rises**:

| Speed increment | Total WTP for the step | WTP per Mbps | Tag |
|---|---|---|---|
| 4 → 10 Mbps | ~$14/mo | **~$2.34/Mbps** | [FACT] |
| 10 → 25 Mbps | ~$24/mo | **~$1.57/Mbps** | [FACT] |
| 100 → 1,000 Mbps | ~$19/mo | **~$0.02/Mbps** | [FACT] |

The marginal value of a megabit **falls by ~100x** from the low end to the high end. Households value the *first* megabits enormously (getting connected) and the *900 extra* megabits from 100 to gigabit almost not at all (~2 cents each). The study explicitly concludes valuation is "**highly concave, with relatively little added value beyond 100 Mbps.**" **[FACT]**

A separate 2022 Wisconsin survey ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0308596124001708)) reaches the same shape: households will pay **$45–$334/mo** to go from no-internet to 25–1,000 Mbps, but "**the value consumers place on speed is diminishing**," and they pay *more for reliability gains* than for speed gains once connected. **[FACT]**

### 3.2 Revealed behavior matches: gigabit is available but unbought

[Truth on the Market, "Gigabit or Bust" (Feb 2026)](https://truthonthemarket.com/2026/02/26/gigabit-or-bust-the-mirage-of-insufficient-broadband-competition/) reports the revealed-preference side:

| Evidence | Value | Tag |
|---|---|---|
| US homes/businesses that **can** get gigabit | **>91%** | [FACT] |
| US homes that **actually subscribe** to gigabit | **~30%** | [FACT] |
| Modal chosen tier | **200–500 Mbps** | [FACT] |
| Bandwidth to stream two 4K videos + kids gaming | **~60 Mbps** | [FACT] |
| FCC broadband definition | **100 / 20 Mbps** | [FACT] |
| Customer response to ~$80 gigabit promo (~$30 over benchmark) | **many decline, drop to lower tier** | [FACT] |
| Competitive benchmark price for "high-speed" service | **~$51/mo** (Cal Advocates) | [FACT] |

So even where gigabit is free to *choose*, **~70% of households decline it** and sit at 200–500 Mbps, because everyday demand (4K streaming, video calls, gaming) saturates well under 100 Mbps. **The willingness-to-pay curve and the actual purchase curve agree: value plateaus in the low hundreds of Mbps.** **[FACT]**

### 3.3 The plateau shows up in operator ARPU

If speed commanded a premium, ARPU would rise as networks got faster. It does not:

- **Comcast** broadband ARPU **fell 3.1% YoY to $73.65** (Q1 2026), driven by simplified pricing and bundled-free wireless lines, not by selling faster tiers ([Fierce Network](https://www.fierce-network.com/broadband/comcasts-q1-2026-broadband-losses-were-less-bad-expected), [Light Reading](https://www.lightreading.com/cable-technology/comcast-faces-arpu-pressure-as-broadband-losses-start-to-stabilize)). **[FACT]**
- Industry-wide, **broadband ARPU is flat-to-declining** and "the usual tactics like speed upgrades, contract hikes, and new bundles aren't working like they used to" ([Blackdice](https://www.blackdice.ai/broadband-arpu-is-stalling/)). **[FACT]**
- The growth engine for the telcos is **bundled wireless / convergence**, not higher broadband speed tiers (Comcast: 9.7M wireless lines, 16% penetration of its broadband base). **[FACT]**

### 3.4 Implication for a space-based comms thesis

The diminishing-returns finding cuts two ways, and the source doc states both neutrally:

1. **Against a "premium speed" play.** A new entrant cannot expect to charge a meaningful premium for *more raw Mbps* to mainstream consumers past ~a few hundred Mbps. The marginal household values gigabit at ~$0.02/Mbps over 100 Mbps and ~70% refuse to buy it even when available. Selling "faster" into the served market does not command price. **[ESTIMATE, interpretation]**
2. **For a "coverage / good-enough" play.** The same evidence shows demand is about **getting connected at all** and **reliability**, where WTP is large ($45–$334/mo to go from nothing to service; reliability valued highly). This is exactly where **FWA and satellite** are winning: T-Mobile/Verizon FWA at ~100–300 Mbps take the majority of net adds because "good-enough speed at a good price / in an unserved location" is what the market actually pays for. A space-based comms offering competes on the **coverage and reliability** axis (unserved/underserved geography, redundancy), **not** on beating fiber's peak speed. **[ESTIMATE, interpretation]**

This is a base-layer observation for the shared library: **the ground-broadband value curve rewards reach and reliability, not raw bandwidth past a low-hundreds-of-Mbps threshold.** Where exactly a Rocket Lab comms business would sit on that curve is a track-specific question left open here.

---

## Sources

*Market size & subscribers*
- [Grand View Research, US Fixed Broadband Services Market](https://www.grandviewresearch.com/horizon/outlook/fixed-broadband-services-market/united-states)
- [Statista, Fixed broadband in the United States](https://www.statista.com/topics/12786/fixed-broadband-in-the-united-states/)
- [Mordor Intelligence, North America Fixed Broadband Market](https://www.mordorintelligence.com/industry-reports/north-america-fixed-broadband-market)
- [Precedence Research, Broadband Services Market](https://www.precedenceresearch.com/broadband-services-market)
- [Leichtman Research Group (via Light Reading), top providers' subscriber base](https://www.lightreading.com/broadband/about-3-5m-added-broadband-from-top-providers-in-2023-leichtman-research-group)
- [Light Reading, top US broadband operators Q2 net adds / 62.5% cable share](https://www.lightreading.com/broadband/top-us-broadband-operators-added-840k-subs-in-q2)
- [Analysys Mason, US fixed market consolidation & FMC](https://www.analysysmason.com/research/content/articles/us-consolidation-fmc-rdcs0-rddj1/)

*Provider financials (filings, earnings, market data)*
- [stockanalysis.com, Comcast (CMCSA)](https://stockanalysis.com/stocks/cmcsa/)
- [Comcast FY2025 Form 10-K (SEC)](https://www.sec.gov/Archives/edgar/data/0001166691/000162828026004994/cmcsa-20251231.htm)
- [Fierce Network, Comcast Q1 2026 broadband / ARPU](https://www.fierce-network.com/broadband/comcasts-q1-2026-broadband-losses-were-less-bad-expected)
- [Charter, Q4 & Full Year 2025 results](https://corporate.charter.com/newsroom/charter-announces-fourth-quarter-and-full-year-2025-results)
- [Charter Q1 2026 Form 10-Q (SEC)](https://www.sec.gov/Archives/edgar/data/0001091667/000109166726000028/chtr-20260331.htm)
- [companiesmarketcap.com, Charter (CHTR)](https://companiesmarketcap.com/charter-communications/marketcap/)
- [stockanalysis.com, AT&T (T)](https://stockanalysis.com/stocks/t/)
- [AT&T, Q1 2026 financial results](https://about.att.com/story/2026/1q-earnings.html)
- [BigGo, AT&T record fiber + FWA adds Q1 2026](https://finance.biggo.com/news/US_T_2026-04-22)
- [AT&T–Lumen consumer fiber acquisition](https://broadbandbreakfast.com/at-t-paying-5-75-billion-for-lumens-consumer-fiber-business/)
- [stockanalysis.com, Verizon (VZ)](https://stockanalysis.com/stocks/vz/)
- [Verizon Q4/FY2025 8-K (SEC)](https://www.sec.gov/Archives/edgar/data/0000732712/000073271226000003/a2025q4exhibit99.htm)
- [Verizon, Frontier acquisition close](https://www.verizon.com/about/news/verizon-and-frontier-regulatory-approval)
- [MacroTrends, T-Mobile US market cap](https://www.macrotrends.net/stocks/charts/TMUS/t-mobile-us/market-cap)
- [Light Reading, FWA 2025 in review](https://www.lightreading.com/fixed-wireless-access/2025-in-review-fwa-s-fangs-stay-sharp)
- [Fierce Network, Big 3 FWA capacity](https://www.fierce-network.com/broadband/big-3-now-have-room-32m-fwa-customers)
- [Altice USA, Q3 2025 results](https://investors.optimum.com/news-events/press-releases/detail/225/altice-usa-reports-third-quarter-2025-results)
- [Cox Communications, Wikipedia / fact sheet](https://en.wikipedia.org/wiki/Cox_Communications)

*Diminishing returns / willingness-to-pay*
- [Liu, Prince & Wallsten, WTP for bandwidth & latency (SSRN)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2942236)
- [Same study, Information Economics and Policy 2018 (RePEc)](https://ideas.repec.org/a/eee/iepoli/v45y2018icp1-15.html)
- [Same study, Tech Policy Institute PDF](https://techpolicyinstitute.org/wp-content/uploads/2017/08/Distinguishing-Bandwidth-and-Latency-in-Households-Willingness-to-Pay-for.pdf)
- [Willingness to pay for broadband: Wisconsin case study (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S0308596124001708)
- [Truth on the Market, Gigabit or Bust (Feb 2026)](https://truthonthemarket.com/2026/02/26/gigabit-or-bust-the-mirage-of-insufficient-broadband-competition/)
- [Light Reading, Comcast ARPU pressure](https://www.lightreading.com/cable-technology/comcast-faces-arpu-pressure-as-broadband-losses-start-to-stabilize)
- [Blackdice, Broadband ARPU is stalling](https://www.blackdice.ai/broadband-arpu-is-stalling/)

---

## Confidence

- **Provider financials & subscriber counts: high.** Drawn from 2025–26 SEC filings (10-K, 10-Q, 8-K) and earnings releases, cross-checked against market-data aggregators. Market caps/prices are point-in-time (June 17, 2026) and move daily.
- **Total-market revenue: medium.** Research-firm sizing diverges ~40% by definition ($63.6B narrow to $100.5B North-America-wide). The ~$70–95B US figure is a reasoned midpoint, not a filed number.
- **Diminishing-returns conclusion: high.** A peer-reviewed discrete-choice study, an independent academic survey, an industry policy analysis, and operator ARPU trends all converge on the same plateau. This is the most robust finding in the doc.
- **Single-source flags:** Cox financials (private, ~$6.7B / ~6M subs); AT&T's ~14.3M combined fiber+FWA subscriber synthesis (fiber 10.4M is filed; FWA count is inferred). The lead should double-check both.

---

## Open Questions

1. **Exact US-only fixed broadband revenue.** The ~$63.6B (narrow) vs ~$92B (broad) vs ~$100.5B (North America) spread needs one agreed definition before any TAM math. Which boundary does the comms track want: access-service-only, or access + bundled attach?
2. **Business / enterprise broadband sizing.** This doc leans residential (the bigger, better-reported segment). Dedicated enterprise/wholesale/backhaul broadband (a more natural fit for some space-comms architectures) is under-sized here and may warrant its own source doc.
3. **FWA trajectory and ceiling.** FWA is taking the majority of net adds now but operators say adds will taper from 2026 as spectrum/capacity fills (Big 3 capacity ~32M). How much of the "good-enough coverage" market is already being captured terrestrially before a space entrant arrives?
4. **Where space competes on the value curve.** Section 3 establishes that value rewards *reach + reliability*, not *raw speed*. Quantifying the *unserved/underserved US households* and their WTP (the part of the curve where WTP is high) is the natural next source doc and is left for the comms-track sizing.
5. **Pricing per subscriber vs. the incumbents.** Cable ARPU is ~$74 and declining; FWA undercuts it. Any space-comms unit economics must be benchmarked against a **falling** incumbent ARPU, not a static one.
6. **Consolidation endpoint.** With Charter–Cox and Verizon–Frontier closing, the 2027 market will have fewer, larger players. The competitive set a space entrant faces is consolidating, worth re-checking subscriber/share splits after both deals fully integrate.

---

## Claims

| COMM- id | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-001 | US fixed broadband services market revenue (narrow) | ~$63.6B (2025) | [ESTIMATE] | Grand View Research |
| COMM-002 | US fixed data revenue (broad) | ~$92B (2023) | [ESTIMATE] single source | Statista |
| COMM-003 | North America fixed broadband market revenue | ~$100.5B (2025), → ~$159.8B by 2030 | [ESTIMATE/PROJECTION] | Mordor Intelligence |
| COMM-004 | Defensible US residential+business fixed broadband revenue | ~$70–95B/yr | [ESTIMATE] | derived from COMM-001/002/003 |
| COMM-005 | Residential share of NA fixed broadband market | 85.5% (2024) | [ESTIMATE] | Mordor Intelligence |
| COMM-006 | Fiber share of US fixed broadband revenue | ~55.75% (2025) | [ESTIMATE] | Grand View Research |
| COMM-007 | Top cable share of US broadband connections | ~62.5% (Q3 2025) | [FACT] | Leichtman / Light Reading |
| COMM-008 | Top-provider US broadband subscriber base | ~114.7M (~76M cable, ~30.7M telco, ~13–14M FWA) | [FACT] | Leichtman Research Group |
| COMM-009 | Comcast domestic broadband subscribers | 31.3M (end-2025, −711K YoY) | [FACT] | Comcast 10-K |
| COMM-010 | Comcast FY2025 revenue / net income | ~$123.7B / ~$20.0B | [FACT] | stockanalysis.com / Comcast 10-K |
| COMM-011 | Comcast broadband ARPU | $73.65 (−3.1% YoY, Q1 2026) | [FACT] | Fierce / Light Reading |
| COMM-012 | Comcast market cap | ~$81B (Jun 17 2026) | [FACT] | stockanalysis.com |
| COMM-013 | Charter internet customers | 29.7M (end-2025) | [FACT] | Charter FY2025 results |
| COMM-014 | Charter FY2025 revenue / net income / EBITDA | ~$54.8B / ~$5.0B / ~$22.7B | [FACT] | Charter FY2025 results |
| COMM-015 | Charter market cap | ~$20B (Jun 2026) | [FACT] | companiesmarketcap.com |
| COMM-016 | AT&T fiber subscribers | ~10.4M (end-2025) | [FACT] | AT&T earnings |
| COMM-017 | AT&T combined fiber+FWA broadband subs | ~14.3M | [ESTIMATE] single source | AT&T earnings (FWA inferred) |
| COMM-018 | AT&T FY2025 revenue / net income (whole co.) | ~$125.7B / ~$21.9B | [FACT] | stockanalysis.com |
| COMM-019 | AT&T market cap | ~$156-160B (Jun 17 2026) | [FACT] | stockanalysis.com |
| COMM-020 | Verizon Fios internet connections | 7.328M (end-2025) | [FACT] | Verizon 8-K |
| COMM-021 | Verizon FWA subscribers | ~5.7M (Q4 2025) | [FACT] | Verizon 8-K |
| COMM-022 | Verizon total broadband post-Frontier | >16.3M | [FACT] | Verizon |
| COMM-023 | Verizon FY2025 revenue / net income (whole co.) | ~$138.2B / ~$17.2-17.6B | [FACT] | stockanalysis.com |
| COMM-024 | Verizon market cap | ~$191-201B (Jun 17 2026) | [FACT] | stockanalysis.com |
| COMM-025 | T-Mobile FWA subscribers | ~8M (Q3 2025); target ~12M by 2028 | [FACT/PROJECTION] | Light Reading / Fierce |
| COMM-026 | T-Mobile market cap | ~$216B (Jun 2026) | [FACT] | MacroTrends |
| COMM-027 | Cox broadband customers / revenue | ~6M / ~$6.7B | [ESTIMATE] single source | Cox fact sheet / Wikipedia |
| COMM-028 | Altice/Optimum broadband subscribers | 4.2M (Q3 2025) | [FACT] | Altice Q3 2025 |
| COMM-029 | Frontier fiber subscribers (acquired by Verizon) | ~2.2M | [FACT] | Verizon / Frontier |
| COMM-030 | Lumen mass-market fiber subs (acquired by AT&T) | ~1M | [FACT] | Broadband Breakfast |
| COMM-031 | Charter–Cox merger value | ~$34.5B combined | [FACT] | Cox / Charter |
| COMM-032 | Verizon–Frontier acquisition value | ~$20B (closed Feb 2026) | [FACT] | Verizon |
| COMM-033 | WTP per Mbps, 4→10 Mbps | ~$2.34/Mbps | [FACT] | Liu/Prince/Wallsten |
| COMM-034 | WTP per Mbps, 100→1,000 Mbps | ~$0.02/Mbps | [FACT] | Liu/Prince/Wallsten |
| COMM-035 | US homes that can get gigabit | >91% | [FACT] | Truth on the Market |
| COMM-036 | US homes subscribing to gigabit | ~30% | [FACT] | Truth on the Market |
| COMM-037 | Modal chosen broadband tier | 200–500 Mbps | [FACT] | Truth on the Market |
| COMM-038 | Bandwidth for two 4K streams + gaming | ~60 Mbps | [FACT] | Truth on the Market |
| COMM-039 | WTP to go from no-internet to 25–1,000 Mbps (Wisconsin) | $45–$334/mo by income | [FACT] | ScienceDirect (Wisconsin) |
| COMM-040 | Competitive benchmark price, high-speed service | ~$51/mo | [FACT] single source | Cal Advocates via Truth on the Market |
