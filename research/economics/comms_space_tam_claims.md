# The Space-Communications TAM, Clarified: What Investors and Companies Actually Cite

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:**
[`research/laser_comms/rf_limited_service.md`](../laser_comms/rf_limited_service.md) (the AST direct-to-device precedent and the limited-allocation logic),
[`research/competitors/starship_addendum.md`](../competitors/starship_addendum.md) (SpaceX's orbital mesh and the June 2026 AI-1 reveal),
and [`research/laser_comms/comms_business_case.md`](../laser_comms/comms_business_case.md) (the satcom TAM reference points already collected, e.g. IRIS2 EUR 10.6B, SDA USD 1.3B, the $14.8B LEO-satcom forecast). Those docs answer "is there a business" and "how does the technology work." This doc answers one narrow question: **when AST SpaceMobile, SpaceX, Amazon, and the broader space-comms bull case cite a TAM number, what is that number, where does it come from, and how much of it is real.**

---

## Summary / Verdict

**The space-comms TAM you hear quoted is almost always one of two very different things, and the gap between them is roughly two orders of magnitude.** On one side sit the **total-market claims**: SpaceX's IPO filing puts its connectivity TAM at **$1.6 trillion** [FACT] and its all-in TAM (mostly AI) at **$28.5 trillion** [FACT]; AST SpaceMobile cites **~$1.1 trillion/year** [FACT] from GSMA data. On the other side sit the **bottoms-up served-market estimates**: Morningstar models Starlink's realistically addressable connectivity market at **~$129 billion** [PROJECTION], and independent direct-to-device (D2D) forecasts land at **$2.6B-$13.8B by 2030-2031** [PROJECTION]. The headline numbers are population-times-spend ceilings; the bottoms-up numbers are what physics, capacity, and competition actually leave reachable.

The single cleanest illustration is Morningstar versus SpaceX on the *same* market: SpaceX's **$1.6T** connectivity claim aggregates the entire global telecom wallet (excluding China and Russia); Morningstar's **~$129B** keeps only the low-density "niche" and carrier "add-on" tiers where a LEO network can actually win, and explicitly throws out the **~$1.17 trillion** [FACT] "core telecom" tier that satellite cannot economically serve in dense areas. That is the whole story in one comparison: **the realistic served slice is on the order of 5-10% of the cited total.**

**Own framing (the number to use):** for a LEO connectivity business, **anchor on the served-addressable tier (~$80-130B global for broadband-class connectivity; ~$3-14B near-term for D2D), not the cited trillion.** The trillion-dollar figures are real as *population-and-spend ceilings* and useful as narrative, but they are not the market any single operator can address. Named analysts call the connectivity headline "completely off-track" and "90% or more out of reach due to the physics of LEO communications."

**Confidence: medium-high.** The cited headline figures are documented in primary filings and investor decks (high confidence on what is claimed). The served-market estimates are themselves analyst models with stated assumptions, so the *exact* served number is medium confidence, but the **direction and rough magnitude of the haircut (90%+) is corroborated by multiple independent analysts** (Morningstar, Eurospace, Novaspace, Frost & Sullivan) and is high confidence.

---

## 1. The Two Kinds of "TAM" (read this first)

The confusion the founder is pointing at is real and it is structural. A cited space-comms TAM is almost always one of these, and they are not comparable:

| Type | What it measures | How it is built | Typical magnitude | What it is good for |
|---|---|---|---|---|
| **Total-market / cited TAM** | The entire spend pool the service *could in principle* touch | Population (or subscribers, or households) x annual spend/ARPU, summed across all geographies and segments | Hundreds of billions to trillions | Narrative, IPO positioning, "size of the prize" |
| **Served-addressable / bottoms-up** | The slice an operator can *realistically* win, after physics and competition | Reachable users x plausible share x plausible ARPU, with capacity and density constraints applied | Single-digit to low-hundreds of billions | Revenue modeling, business cases, valuation |

Three traps recur in the cited-TAM numbers, and every section below flags them:

1. **Counting the whole telecom wallet.** A LEO network is capacity-constrained in dense areas (one beam, finite bandwidth, congestion). It competes well only where terrestrial economics break down: low density, remote, mobile, underserved. Citing the *full* mobile or broadband market counts cities the satellite physically cannot serve at competitive quality.
2. **Counting people who cannot pay the ARPU.** "3.5 billion underserved" or "the next billion users" are largely low-income populations. Multiplying that count by a developed-market ARPU produces a number no one will actually spend.
3. **Counting a market shared by many operators as if one captures it.** Starlink, Kuiper, AST, Eutelsat, Telesat, and others split the same pie. No single company captures a $1.6T market; analysts note such figures are "ultimately unfalsifiable."

---

## 2. AST SpaceMobile (ASTS): the direct-to-device TAM

ASTS is the purest "total addressable connections" pitch, because its product (broadband direct to an unmodified phone) maps onto the entire global mobile-subscriber base. This is also the precedent [`rf_limited_service.md`](../laser_comms/rf_limited_service.md) cites for D2D spectrum (AST using AT&T/Verizon terrestrial spectrum via FCC approval).

### What ASTS officially cites

| Figure | Value | Source / derivation | Tag |
|---|---|---|---|
| Global market opportunity | **~$1.1 trillion/year** | ASTS investor presentation, attributed to GSMA market data | [FACT] (as a claim) |
| Underserved population | **~3.5 billion people (42% of world)** with little/no mobile access | GSMA, cited by ASTS | [FACT] |
| Reachable devices | **~5.5 billion** cellular devices when out of coverage | ASTS positioning | [FACT] |
| MNO partner reach | **~3 billion subscribers** across ~50-60 MNO agreements | ASTS Q1 2026 deck | [FACT] |
| Revenue-share model | **50/50** with the MNO | ASTS | [FACT] |

**How the headline is derived:** it is a total-addressable-connections claim. Take the world's mobile subscribers / underserved population, attach an annual connectivity spend, and you reach ~$1.1T. It is the "every phone on Earth is a potential customer when it loses signal" framing.

### The bottoms-up version (what investors actually model)

The widely-circulated investor model for the **commercial (MNO-serving) business** is explicit and much smaller [ESTIMATE]:

- **3.2B subscriber TAM** (across 52 MNOs) x **10% uptake** x **$4/month ARPU** x 12 = **~$15.4B annual revenue** at maturity, with claimed +90% gross and +85% EBITDA margins.

> **FLAGGED ESTIMATE / single source.** The $15.4B figure traces to an analyst/investor model circulated publicly ([spacanpanman on X](https://x.com/spacanpanman/status/1939170494709633105)), not an ASTS guidance number. Its *inputs* (3B+ subs, ~52 MNOs) are independently sourced to ASTS, but the 10% uptake and $4 ARPU are the modeler's assumptions. Treat $15.4B as an illustrative bottoms-up bull case, not a fact. The lead should double-check this one.

Bank of America's published model brackets the range more conservatively and shows the method cleanly:

| BofA scenario | World subs | ASTS share | ARPU/mo | Annual TAM-to-ASTS |
|---|---|---|---|---|
| **Bull** | 5,400M | 50% | $3.00 | **~$97B** |
| **Base** | 5,400M | 25% | $1.50 | **~$32B** |
| **Bear** | 5,400M | 10% | $0.50 | **~$3B** |

Formula: **subscribers x share x monthly ARPU x 12** ([BofA Global Research on ASTS](https://astsinvestors.com/wp-content/uploads/2025/06/bofa_asts_2025_06_25-1.pdf)). World population assumed 8,062M, of which 5,400M hold a subscription.

**The takeaway for ASTS:** the cited TAM is **~$1.1T**; the *modeled revenue an analyst assigns to ASTS itself* spans **~$3B (bear) to ~$97B (bull)**, i.e. **0.3%-9% of the cited TAM**. The cited number is the ceiling; the bottoms-up share is the business. Note that the BofA "bull" $97B is itself a revenue-to-ASTS figure, not a market size, and even it assumes a heroic 50% global share at a $3 ARPU.

### Reality check from actuals

ASTS reported **full-year 2025 revenue of ~$70.9M** against a ~$274M operating loss, and a Q1 print of **$14.7M vs ~$36.6M expected**. The gap between a $1.1T cited TAM (or even a $15-32B bottoms-up case) and ~$70M of actual revenue is the execution risk the bears price in. This is not a knock on the TAM method; it is the reminder that **cited TAM and realized revenue are separated by years of deployment and adoption.**

---

## 3. SpaceX / Starlink: the IPO TAM and the Morningstar rebuttal

This is the richest case because, days before its IPO, SpaceX published an explicit TAM and a credible analyst (Morningstar) published a same-market bottoms-up rebuttal. The two together are the clearest possible answer to the founder's question.

### What SpaceX cites (IPO S-1 / roadshow, May 2026)

SpaceX states it has identified **"the largest actionable total addressable market in human history."** The quantified figure is **$28.5 trillion** [FACT], broken down as ([Fortune](https://fortune.com/2026/05/20/spacex-ipo-filing-s1-total-addressable-market-make-life-multiplanetary/), [Via Satellite](https://www.satellitetoday.com/finance/2026/06/03/assessing-spacex-finances-addressable-market-and-the-ai-pitch-ahead-of-ipo/), [Stocktwits / Sawyer Merritt quoting the filing](https://stocktwits.com/news-articles/markets/equity/asts-lunr-fly-sats-spacex-ipo-space-economy-largest-tam/cZXzxlNReF9)):

| Segment | TAM | Notes | Tag |
|---|---|---|---|
| **Space-enabled solutions** | **$370B** | Launch + space-enabled services | [FACT] (as claimed) |
| **Connectivity** | **$1.6T** | Starlink broadband **$870B** + Starlink mobile **$740B** (+ unquantified enterprise/gov) | [FACT] (as claimed) |
| **AI** | **$26.5T** | Enterprise AI apps **$22.7T**, AI infra **$2.4T**, consumer subs **$760B**, digital ads **$600B** | [FACT] (as claimed) |
| **Total** | **$28.5T** | Estimates **exclude China and Russia** | [FACT] (as claimed) |

**Two structural observations.** First, **93% of the headline ($26.5T of $28.5T) is AI, not connectivity** (ties to [`starship_addendum.md`](../competitors/starship_addendum.md): SpaceX is repositioning as an AI/compute company via the AI-1 satellite and the 1M-satellite FCC filing). Second, the connectivity number itself ($1.6T) is the one relevant to a comms business, and it is the one analysts attack hardest.

### What is actually reachable (Morningstar, June 2026)

Morningstar's report ["Testing the Sky's Limits: Our Realistic Starlink Market Sizing"](https://d1e00ek4ebabms.cloudfront.net/production/uploaded-files/Our_Realistic_Starlink_Market_Sizing-915d25bb-5968-4e1f-ae0b-ad5999a9aa87.pdf) takes SpaceX's own $1.6T and rebuilds it bottoms-up. Its framework splits every connectivity segment into three tiers and keeps only the two a LEO network can win:

| Tier | What it is | Can Starlink win it? | Global size [PROJECTION] |
|---|---|---|---|
| **Niche** (greenfield, no incumbent) | Dead/low-density zones, rural, maritime, remote ops, disaster recovery | Yes (primary opportunity) | **~$84B** |
| **Add-on** (carrier bolt-on) | Carrier satellite-to-phone bolt-on, $10-15/mo premium tier | Yes (low acquisition cost) | **~$45B** |
| **Core telecom** (mass market) | Urban mobile, cable/fiber incumbents, enterprise | **No** (capacity-constrained, uncompetitive in dense areas) | **~$1.17T (excluded)** |
| **Realistic total (Niche + Add-on)** | | | **~$129B** |

Morningstar's geographic split of the ~$129B: **~$43B US** (Niche ~$28B + Add-on ~$15B) plus **~$86B international**, with global opportunity estimated at roughly **3x the US** realistically-addressable market. Its base case has Starlink reaching **~$85B revenue by 2035**, which implies capturing **~45% of that realistic $129B market** (not of the $1.6T).

**The simplest version of the haircut**, in Morningstar's own words: about **5% of the global population lives in the highly dispersed environments** best-suited to satellite; applying that 5% to SpaceX's $1.6T gives a **conservative floor of ~$80B** in directly addressable global market. So two independent paths (the tier framework and the 5%-of-population shortcut) both land near **$80-130B**, against the cited **$1.6T**. **The realistic served slice is ~5-8% of the cited connectivity TAM.**

### Why the dense-market wallet is unreachable (the physics, briefly)

Morningstar's core argument (consistent with the capacity logic in [`rf_limited_service.md`](../laser_comms/rf_limited_service.md)): a satellite beam has **finite bandwidth shared across everyone under it**. In dense areas this is the *opposite* of terrestrial economics: as users concentrate, the satellite congests and quality falls (Starlink's measured broadband-quality score drops to ~60% in peak hours in the densest areas, making it uncompetitive there), while fiber/5G get *cheaper* per user. So the entire urban "core telecom" wallet, which is most of the $1.6T, is structurally closed to LEO. Satellite wins exactly where terrestrial infrastructure cannot be justified: the last ~5-20% of population by density.

### What the critics say about the headline itself

The connectivity figure is not just trimmed by Morningstar; named industry analysts reject it as a market measure ([Via Satellite](https://www.satellitetoday.com/finance/2026/06/03/assessing-spacex-finances-addressable-market-and-the-ai-pitch-ahead-of-ipo/)):

- **Pierre Lionnet (Eurospace):** "90% or more of that opportunity is out of reach due to the physics of LEO communications"; calls the TAM narrative "completely off-track" and "misleading."
- **Nathan de Ruiter (Novaspace):** the TAM is "more of a narrative tool than a precise financial estimate"; SpaceX "would not capture the full value generated by application-layer platforms."
- **Pravin Pradeep (Frost & Sullivan):** "TAM figures this large are ultimately unfalsifiable. No single company captures a majority of a $28 trillion market."

That is three independent experts, plus Morningstar, all making the same point: **the cited connectivity TAM overstates the reachable market by roughly an order of magnitude.**

---

## 4. Amazon Kuiper (now "Amazon Leo"): the unconnected-households TAM

Kuiper's TAM is the **household** version of the same template: count the homes without good broadband, attach an ARPU.

| Figure | Value | Source / derivation | Tag |
|---|---|---|---|
| Unconnected households (addressable) | **400-500 million** worldwide without high-speed internet | Multiple ([CNBC](https://www.cnbc.com/2025/08/11/amazons-big-investment-in-kuiper-is-proving-to-be-a-smart-bet.html), market studies) | [FACT] |
| Target unconnected consumers | **~300 million** | Amazon framing | [FACT] |
| Bottoms-up revenue (Quilty) | **~$36B/yr** = **100M subs x $30/mo x 12** | [Quilty Space, Dec 2024](https://www.geekwire.com/2024/market-study-amazon-cost-project-kuiper-satellite-quilty/) | [PROJECTION] |
| Internal revenue target | **~$20B/yr by 2030** | Reported Amazon internal projection | [PROJECTION] |
| Sector revenue opportunity | **~$40B by 2030** | Analyst estimate for satellite comms | [PROJECTION] |

**How it is derived and where it is honest vs. not.** The Kuiper case is comparatively disciplined: the **$36B** figure is a clean **subscribers x ARPU** (100M x $30/mo), and the **$20B by 2030** is an internal target, not a population-times-spend ceiling. The softness is in the **100M subscribers** assumption: that is ~20-25% of the 400-500M unconnected-household pool, at a $30 ARPU many of those (low-income, emerging-market) households cannot pay. So Kuiper's bottoms-up numbers are more credible than a trillion-dollar ceiling, but they still embed an optimistic capture rate and a developed-market ARPU applied to a partly-emerging-market base. **Note the convergence:** Kuiper ($20-36B), the satellite-sector "$40B by 2030" estimate, and Morningstar's Starlink ($129B for a more mature constellation across more tiers) are all in the **tens of billions**, an order of magnitude below the cited trillions.

*Status note: Amazon rebranded Project Kuiper to "Amazon Leo" and began commercial beta in April 2026; the TAM framing predates and survives the rebrand.*

---

## 5. The broader bull case and the bottoms-up reality

### The "largest TAM in human history" framing

SpaceX's IPO pitch ("largest actionable total addressable market in human history," $28.5T) is the apex of the bull case, and it has pulled the whole sector's framing upward. Coverage explicitly groups the D2D/satcom names under "space economy = largest TAM" ([Stocktwits](https://stocktwits.com/news-articles/markets/equity/asts-lunr-fly-sats-spacex-ipo-space-economy-largest-tam/cZXzxlNReF9)). A bank note cited a combined **~$200 billion** market that AST, Starlink, and Kuiper are jointly "targeting" ([Advanced Television, Sep 2025](https://www.advanced-television.com/2025/09/23/bank-ast-starlink-kuiper-targeting-200bn-market/)).

> **Single source / flag.** The **$200B "combined target market"** comes through one trade-press summary of a bank note; the underlying bank report and its derivation were not directly reachable (the page rate-limited on fetch). Treat the $200B as a directional sell-side figure, not a verified bottoms-up number. The lead should source the underlying bank note if this figure is used. It is, notably, consistent in *order of magnitude* with the bottoms-up estimates below (tens to low-hundreds of billions), which is itself informative.

### The bottoms-up D2D market (the credible floor)

For the specific direct-to-device segment, independent market-research houses (which build bottoms-up, segment-by-segment) cluster tightly and far below the headline claims:

| Source | D2D market size | Year | Tag |
|---|---|---|---|
| MarketsandMarkets | **$0.57B (2025) -> $2.64B** (35.6% CAGR) | 2030 | [PROJECTION] |
| ABI Research | **$11.6B** direct-to-cellular (+ $4B IoT) | 2030 | [PROJECTION] |
| Mordor Intelligence | **$5.03B (2026) -> $13.80B** (22.4% CAGR) | 2031 | [PROJECTION] |

These are **single-digit to low-double-digit billions**, i.e. **~1%** of ASTS's cited $1.1T. Even granting that D2D is a young market that will grow, the bottoms-up forecasts say the *near-term* served D2D market is ~$3-14B, not a trillion. (Each of these is a single commercial-research-house number; they are listed together because their *agreement* is the signal. Any one in isolation is single-source.)

### One table: cited vs. served, every player

| Player | Cited / headline TAM | Bottoms-up / served estimate | Served as % of cited | Method of the headline |
|---|---|---|---|---|
| **AST SpaceMobile** | **~$1.1T/yr** (GSMA) | ~$3B-$97B revenue-to-ASTS (BofA); ~$15.4B model (single source) | ~0.3-9% | Global mobile subscribers x annual spend |
| **SpaceX / Starlink (connectivity)** | **$1.6T** ($870B broadband + $740B mobile) | **~$129B** realistic (Morningstar); ~$80B floor | **~5-8%** | Entire telecom wallet ex-China/Russia |
| **SpaceX (all-in)** | **$28.5T** (93% AI) | n/a (mostly AI, not comms) | n/a | Population/enterprise x spend across all sectors |
| **Amazon Kuiper / Leo** | 400-500M unconnected households | **~$20-36B/yr** (Quilty/internal) | tens of $B | Unconnected households x ARPU |
| **D2D segment (bottoms-up)** | (sector) | **$2.6B-$13.8B** | n/a | Segment-by-segment research-house build |
| **Sector "bull" framing** | "largest TAM in history"; ~$200B combined | tens-to-low-hundreds of $B | order-of-magnitude lower | Sum of the above headlines |

---

## 6. Own framing: the served-addressable slice vs. the cited total

The founder asked for a clean own-framing. Here it is, for any track (comms or data center) that needs to cite a space-comms market number.

**1. Name which number you are citing.** Never quote a trillion-dollar figure without saying it is a *total-market ceiling*, not a served market. The honest sentence is: "The cited TAM is $X trillion (population x spend); the realistically served market is ~$Y billion (reachable users x plausible share x ARPU), roughly Z% of the headline."

**2. Use the served tier, not the wallet.** For LEO connectivity, the defensible served market is the **Niche + Add-on** tiers: low-density/remote/maritime/disaster, plus carrier D2D bolt-on. Morningstar sizes that at **~$80-130B globally** for broadband-class connectivity, and bottoms-up D2D forecasts put the *near-term* direct-to-device slice at **~$3-14B**. These are the numbers a business case should run on.

**3. Apply the ~90% haircut as the default prior.** Across SpaceX (Morningstar, Eurospace), the pattern is consistent: **the served market is ~5-10% of the cited total.** When you encounter a fresh space-comms TAM with no bottoms-up backing, a 90% haircut is the reasonable starting assumption until a real served-market model exists.

**4. Three structural discounts to apply to any cited TAM:**
- **Density discount.** Remove the dense-urban "core telecom" wallet a beam cannot serve at competitive quality (this alone is ~70-80% of the connectivity TAM).
- **ARPU-reality discount.** Do not multiply low-income "underserved billions" by a developed-market ARPU.
- **Shared-market discount.** The pie is split among Starlink, Kuiper, AST, Eutelsat, Telesat, and others; no single operator captures the segment.

**5. For Rocket Lab specifically (cross-ref [`comms_business_case.md`](../laser_comms/comms_business_case.md)):** none of these mass-market TAMs is Rocket Lab's market. Its scoped opportunity is the **premium private/secure/sovereign orbital network** (defense, sovereign government, finance, critical-infrastructure, orbital-DC backhaul), whose reference points are the **EUR 10.6B IRIS2**, the **$1.3B** of SDA optical-mesh contracts, and the **$14.8B** LEO-satcom forecast already in the business-case doc, not the $1.1T-$1.6T consumer/D2D ceilings. The lesson from this TAM analysis is the same either way: **size on the served slice, and state the haircut explicitly.**

---

## Sources

- [BofA Global Research on AST SpaceMobile (TAM bull/base/bear, ARPU, share method)](https://astsinvestors.com/wp-content/uploads/2025/06/bofa_asts_2025_06_25-1.pdf)
- [AST SpaceMobile investor / Q1 2026 presentation references, $1.1T GSMA, 3B+ subs, 50/50 share](https://www.marketscreener.com/news/ast-spacemobile-q1-2026-earnings-presentation-ce7f5adad18df42d)
- [spacanpanman on X, ASTS commercial-model math ($15.4B), single source](https://x.com/spacanpanman/status/1939170494709633105)
- [Morningstar, "Testing the Sky's Limits: Our Realistic Starlink Market Sizing" (~$129B, tier framework, June 2026)](https://d1e00ek4ebabms.cloudfront.net/production/uploaded-files/Our_Realistic_Starlink_Market_Sizing-915d25bb-5968-4e1f-ae0b-ad5999a9aa87.pdf)
- [Fortune, SpaceX IPO S-1, $28.5T TAM and breakdown](https://fortune.com/2026/05/20/spacex-ipo-filing-s1-total-addressable-market-make-life-multiplanetary/)
- [Via Satellite, Assessing SpaceX Finances, Addressable Market, and the AI Pitch (analyst skepticism)](https://www.satellitetoday.com/finance/2026/06/03/assessing-spacex-finances-addressable-market-and-the-ai-pitch-ahead-of-ipo/)
- [Stocktwits, SpaceX IPO "largest TAM in human history," $28.5T, segment quote](https://stocktwits.com/news-articles/markets/equity/asts-lunr-fly-sats-spacex-ipo-space-economy-largest-tam/cZXzxlNReF9)
- [SpaceX IPO Roadshow Presentation (primary; too large to fetch directly, figures corroborated above)](https://s21.q4cdn.com/184289198/files/doc_events/SpaceX_IPO_Roadshow_Final.pdf)
- [CNBC, Amazon's Kuiper investment, 400-500M unconnected households](https://www.cnbc.com/2025/08/11/amazons-big-investment-in-kuiper-is-proving-to-be-a-smart-bet.html)
- [GeekWire / Quilty Space, Kuiper $36B at 100M subs x $30 ARPU](https://www.geekwire.com/2024/market-study-amazon-cost-project-kuiper-satellite-quilty/)
- [Advanced Television, bank note, ~$200B combined AST/Starlink/Kuiper target (single source)](https://www.advanced-television.com/2025/09/23/bank-ast-starlink-kuiper-targeting-200bn-market/)
- [MarketsandMarkets, Direct-to-Device (D2D) market $0.57B (2025) to $2.64B (2030)](https://www.marketsandmarkets.com/Market-Reports/satellite-direct-to-device-d2d-market-176759878.html)
- [Mordor Intelligence, D2D satellite connectivity $5.03B (2026) to $13.80B (2031)](https://www.mordorintelligence.com/industry-reports/direct-to-device-satellite-connectivity-market)
- [Benzinga, ASTS "$30B bet requiring flawless execution" (FY2025 revenue ~$70.9M, loss)](https://www.benzinga.com/Opinion/26/02/50391831/ast-spacemobile-a-30-billion-bet-requiring-flawless-execution)

## Confidence

- **What is claimed (the cited TAMs): high.** Every headline figure (SpaceX $28.5T/$1.6T/$370B/$26.5T; ASTS $1.1T; Kuiper household pool) is documented in primary filings, investor decks, or direct quotes of the filing, cross-checked across 2+ outlets.
- **The served-market estimates: medium.** Morningstar's ~$129B and the D2D ~$3-14B are analyst/research-house models with stated but debatable assumptions (penetration, ARPU, tier boundaries). The exact figure is uncertain; the method is transparent.
- **The size of the haircut (~90%, served ~5-10% of cited): high.** This is the load-bearing finding and it is corroborated by four independent analysts (Morningstar, Eurospace, Novaspace, Frost & Sullivan) plus the convergence of bottoms-up estimates into the tens of billions.
- **Single-source items flagged in-line: low-to-medium.** The $15.4B ASTS model and the $200B combined-bank figure each rest on one reachable source and are tagged accordingly.

## Open Questions / Uncertainties

- **The $200B combined bank figure** needs its underlying report sourced (the trade-press page rate-limited). What bank, what year, D2D-only or all-satcom, and how derived?
- **The $15.4B ASTS commercial model** is one public investor model; ASTS has not guided to it. A check against any sell-side consensus revenue-at-maturity for ASTS would firm it up.
- **ARPU realism by geography.** None of the cited TAMs cleanly separates payable ARPU by region. A served-market model that applies region-specific ARPU to the reachable population would sharpen the "ARPU-reality discount" from a qualitative caveat to a number.
- **D2D vs. broadband boundary.** ASTS (D2D-to-phone) and Starlink/Kuiper (broadband-to-terminal) are partly different markets; the $1.1T (ASTS) and $1.6T (SpaceX connectivity) overlap in ways not cleanly decomposed here. A unified served-market map that de-duplicates D2D and fixed broadband is a useful next step.
- **Where the served number lands for a *premium/sovereign* niche** (Rocket Lab's actual market) is not sized here; it is the subject of [`comms_business_case.md`](../laser_comms/comms_business_case.md) and the `economics/` workstream, and is a different (smaller, higher-margin, government-weighted) market than the consumer TAMs clarified above.

## Claims Table

| ID | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-001 | SpaceX IPO S-1 total addressable market | $28.5 trillion (ex-China/Russia) | [FACT] (as claimed) | Fortune; Via Satellite; Stocktwits |
| COMM-002 | SpaceX IPO connectivity TAM | $1.6 trillion ($870B broadband + $740B mobile) | [FACT] (as claimed) | Fortune; Via Satellite; Stocktwits; Morningstar |
| COMM-003 | SpaceX IPO Space-enabled-solutions TAM | $370 billion | [FACT] (as claimed) | Fortune; Stocktwits |
| COMM-004 | SpaceX IPO AI TAM (share of total) | $26.5 trillion (93% of $28.5T) | [FACT] (as claimed) | Fortune; Via Satellite |
| COMM-005 | Morningstar realistic Starlink served connectivity market | ~$129 billion global (~$43B US + ~$86B intl) | [PROJECTION] | Morningstar (primary PDF) |
| COMM-006 | Morningstar Niche + Add-on tier sizes | ~$84B (Niche) + ~$45B (Add-on) | [PROJECTION] | Morningstar (primary PDF) |
| COMM-007 | Morningstar "core telecom" tier excluded as unreachable | ~$1.17 trillion global | [FACT] (Morningstar estimate) | Morningstar (primary PDF) |
| COMM-008 | Morningstar 5%-of-population shortcut floor on $1.6T | ~$80 billion | [PROJECTION] | Morningstar (primary PDF) |
| COMM-009 | Morningstar base-case Starlink 2035 revenue (=45% of realistic market) | ~$85 billion | [PROJECTION] | Morningstar (primary PDF) |
| COMM-010 | Analyst view: connectivity TAM ~90%+ unreachable (LEO physics) | "90% or more out of reach" | [FACT] (attributed quote) | Via Satellite (Lionnet/Eurospace) |
| COMM-011 | ASTS cited global market opportunity | ~$1.1 trillion/year (GSMA) | [FACT] (as claimed) | ASTS deck; multiple |
| COMM-012 | ASTS underserved population | ~3.5 billion people / 42% of world | [FACT] | GSMA via ASTS |
| COMM-013 | ASTS MNO partner subscriber reach | ~3 billion across ~50-60 MNOs | [FACT] | ASTS Q1 2026 deck |
| COMM-014 | BofA ASTS revenue scenarios (bull/base/bear) | ~$97B / ~$32B / ~$3B | [ESTIMATE] | BofA (primary PDF) |
| COMM-015 | BofA ASTS method | subscribers x share x ARPU x 12 (5,400M subs; share 50/25/10%; ARPU $3.00/$1.50/$0.50) | [FACT] (method) | BofA (primary PDF) |
| COMM-016 | ASTS viral commercial-model revenue | ~$15.4B/yr (3.2B x 10% x $4/mo x 12) | [ESTIMATE], single source | spacanpanman (X) |
| COMM-017 | ASTS actual FY2025 revenue | ~$70.9M (operating loss ~$274M) | [FACT] | Benzinga; search corroboration |
| COMM-018 | Kuiper addressable unconnected households | 400-500 million worldwide | [FACT] | CNBC; market studies |
| COMM-019 | Kuiper bottoms-up revenue (Quilty) | ~$36B/yr (100M subs x $30/mo x 12) | [PROJECTION] | Quilty Space via GeekWire |
| COMM-020 | Kuiper internal revenue target | ~$20B/yr by 2030 | [PROJECTION] | reported internal projection |
| COMM-021 | Bottoms-up D2D market (near-term) | $2.6B (2030, M&M) / $13.8B (2031, Mordor) / $11.6B (2030, ABI) | [PROJECTION] | MarketsandMarkets; Mordor; ABI |
| COMM-022 | Bank note combined AST/Starlink/Kuiper target market | ~$200 billion | [ESTIMATE], single source | Advanced Television |
| COMM-023 | Served-vs-cited ratio (load-bearing finding) | served ~5-10% of cited total | [ESTIMATE] (synthesis) | Morningstar; Via Satellite; bottoms-up convergence |
