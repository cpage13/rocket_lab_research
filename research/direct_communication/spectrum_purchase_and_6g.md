# Spectrum Purchase Economics: How Much You Must Hold, What It Costs, From Whom, and the 6G Question

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:**
- [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md): what spectrum is and why it is scarce, the speed-vs-connections tradeoff, the low/mid/mmWave tiers, the per-MHz-POP **auction** prices (US C-band ~$0.94, Auction 110 ~$0.72, AWS-3 ~$2.72 paired, mmWave near a floor; Europe mid-band ~EUR 0.08 to 0.36), who holds which US tier, and the verdict that buying terrestrial cellular spectrum outright is closed to a new entrant. This doc does **not** re-derive those auction prices; it **uses** them to answer a new question.
- [`spectrum_generations_and_availability.md`](spectrum_generations_and_availability.md): what a "generation" is, refarming/DSS, the FR3 / 7 to 15 GHz "golden band" and WRC-27 study bands at a high level, and the SCS partner/lease model (AST on AT&T/Verizon 850 MHz, Starlink on T-Mobile PCS G-block). This doc does **not** repeat the SCS mechanics or the generation definitions.
- [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md): the EchoStar ~$17B / ~65 MHz and AST/Ligado ~45 MHz deals as the "own dedicated D2D spectrum" shift, and the ~20x per-GB capacity gap. This doc does **not** re-derive those; it converts them into **$/MHz-POP benchmarks** the prior doc did not compute.

**The NEW contribution here is three things those docs leave open:**
1. **The quantity question.** *How much* spectrum (MHz) must an operator actually hold to run a competitive broadband or D2C service over a target area? (The prior docs price spectrum but never state the required quantity.)
2. **The total-dollar translation.** Multiply $/MHz-POP by the required MHz and the POP base to get a single headline number for **US-plus-Europe** coverage at a competitive bandwidth, and add the **secondary-market** $/MHz-POP benchmarks (the prior doc flagged "what does a lease actually cost" as an open question; this doc answers it with three 2024-26 deals).
3. **The sharpened 6G access question.** Not just "what is FR3" (prior doc) but specifically: is 6G spectrum **decided or open**, **auctioned or already held**, and **can a satellite NTN entrant get any of it** (decided vs open, explicitly).

> **Reading guide.** Every hard number is tagged **[FACT]** (2+ independent sources), **[FACT, single-source]**, **[ESTIMATE]** (third-party model/sizing), or **[DERIVED]** (my own arithmetic on cited inputs). China is excluded. No verdict on the Rocket Lab business is rendered; this is a neutral economics base doc.

---

## Summary / Verdict

**How much spectrum must you hold?** The industry's own benchmark, from the GSMA, is **80 to 100 MHz of contiguous mid-band per operator just to launch competitive 5G**, rising to a planning target of **~2 GHz of mid-band per country by 2030** across all operators, plus low-band for coverage [FACT]. The revealed-preference check confirms it: the three US carriers actually hold **~280 to 375 MHz each** of low-plus-mid-band (population-weighted), with mid-band depth of ~120 to 320 MHz [FACT]. So a credible competitive build is **roughly 100 MHz at the floor, 200+ MHz to match an incumbent**, in the sub-7-GHz bands that penetrate and cover.

**What does that cost, and from whom?** Three doors, each with a real per-MHz-POP price:
- **Primary auction** (from the government, the FCC/Ofcom): US mid-band ran **~$0.72 to $0.94 per MHz-POP** (Auction 110 / C-band), the AWS-3 outlier ~$2.72 paired; European mid-band far cheaper at **~EUR 0.08 to 0.36** [FACT, all from the prior doc]. **But there is no greenfield US mid-band left to auction**, so this door is closed in practice.
- **Secondary market** (from a carrier or a holder): real 2024-26 deals price mid-band at **~$0.65 to ~$1.03 per MHz-POP**. AT&T bought UScellular 3.45 GHz + 700 MHz at **~$0.65/MHz-POP** ($1.018B for 1,581M MHz-POPs) [FACT, DERIVED]; SpaceX's EchoStar AWS-4/H-block (~$17B) implies **~$1.03/MHz-POP** for nationwide D2D spectrum [FACT, single-source on the decimal]. This is the realistic door, and it prices in the same range as the primary auctions.
- **A distressed/MSS holder** (EchoStar, Ligado): the source of the two D2D deals above. EchoStar sold to SpaceX; Ligado leased ~45 MHz of L-band to AST. These are the rare blocks a satellite entrant can actually buy or lease, because they were satellite/MSS spectrum to begin with.

**The total-dollar headline for US-plus-Europe at a competitive 100 MHz** [DERIVED, from sourced $/MHz-POP and POP bases]:
- **US** (~342M POPs): 100 MHz x 342M = 34,200M MHz-POPs x ~$0.65 to $1.03 = **~$22B to $35B**.
- **Europe** (~520M POPs, EU-27 ~450M + UK ~68M): 100 MHz x 520M = 52,000M MHz-POPs x ~EUR 0.19 avg = **~EUR 9.9B (~$10.7B)**.
- **Combined: ~$32B to ~$46B for a single 100 MHz nationwide-equivalent layer across the US and Europe.** Doubling to ~200 MHz (incumbent-matching depth) roughly doubles it to **~$65B to ~$90B**. These are spectrum-only figures, before any satellites, ground, or network.

**This is why no one buys their way in at full scale.** The number lands in the same tens-of-billions range as the [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md) verdict, now with the quantity and the geography pinned. SpaceX's ~$17B EchoStar buy purchased only ~65 MHz over the US alone, and that is a hyperscale exception. The realistic entrant path remains the SCS partner/lease (prior docs), where you ride a carrier's existing 5 to 40 MHz rather than assembling a 100 MHz national position.

**The 6G question, decided vs open:**
- **What it will use:** the **upper mid-band, FR3 (7.125 to 24.25 GHz)**, with the **"golden band" 7.125 to 8.4 GHz** the lead candidate, plus 4.4 to 4.8 GHz and 14.8 to 15.35 GHz [FACT]. **Decided** that these are the WRC-27 study bands; **open** which exact slices get identified for IMT at WRC-27 (late 2027) and how much.
- **Auctioned or held:** **neither yet.** FR3 IMT bands are **not allocated, not auctioned, and not owned by anyone for mobile** today: they are under ITU sharing/compatibility study, currently occupied by incumbent **Fixed-Satellite Service (FSS), Fixed Service, and federal/military** users [FACT]. This is the one greenfield where the "all the good spectrum is already filed" wall is **not yet built**. National auctions would follow WRC-27 identification, so **~2028 to 2032+** before any FR3 mobile licenses are sold [DERIVED from the WRC cycle].
- **Can a satellite entrant get it?** **Largely no, and the trajectory is terrestrial-only.** WRC-27 Agenda Item 1.7 is framed for the **terrestrial component of IMT**, not satellite [FACT]. Worse, the physics cuts against a phone-to-LEO link at 7 to 15 GHz: "higher path loss for fixed antenna gains... difficult to deliver data to handheld devices, especially on the uplink under non-line-of-sight" [FACT, single-source: arXiv 2506.18672]. FSS/NTN already hold *adjacent* slices (e.g. 10.7 to 12.7 GHz space-to-Earth, 13.85 to 14 GHz uplinks), so a satellite operator's FR3 role is **coexistence as an incumbent neighbor, not a new mobile allocation** it can build a D2C service on. **Decided:** FR3's mobile identification is terrestrial-led. **Open:** the exact TN/NTN coexistence rules, which WRC-27 is meant to settle.

**Confidence: medium-high.** The GSMA quantity benchmark, the carrier holdings, the three secondary-market $/MHz-POP deals, and the FR3/WRC-27 status are each carried by 2+ independent sources or a primary filing. The total-dollar translations are my own [DERIVED] arithmetic on sourced inputs and are order-of-magnitude (they assume a flat $/MHz-POP across a national footprint, which real auctions vary by market). The "satellite cannot get FR3" read is medium-high in direction (terrestrial framing + physics are well-attested) but the door is not formally shut, so it is a trajectory call, not a settled fact.

---

## 1. The Quantity Question: How Much Spectrum Must an Operator Hold?

The prior docs price spectrum exhaustively but never state *how much you need*. Here is the answer, from two angles that agree.

### 1.1 The industry benchmark (GSMA)

The GSMA, the global mobile-operator trade body, publishes the canonical "how much" figures:

- **To launch competitive 5G: 80 to 100 MHz of contiguous mid-band spectrum per operator**, in the prime bands (the 3.3 to 3.8 GHz core) [FACT] ([GSMA 5G Spectrum Guide](https://www.gsma.com/connectivity-for-good/spectrum/5g-spectrum-guide-2/), [Nokia - 5G spectrum bands](https://www.nokia.com/thought-leadership/articles/spectrum-bands-5g-world/)). "100 MHz of spectrum per operator is needed to launch 5G in the first place."
- **Plus ~1 GHz per operator in mmWave** for hotspot capacity (cheap per MHz, tiny coverage, optional) [FACT] ([GSMA](https://www.gsma.com/connectivity-for-good/spectrum/5g-spectrum-guide-2/)).
- **National planning target: ~2 GHz of mid-band per country by 2030**, the aggregate across all operators needed to meet the IMT-2020 100 Mbps requirement city-wide [FACT] ([GSMA Vision 2030](https://www.gsma.com/connectivity-for-good/spectrum/vision-2030-spectrum-needs-for-5g/), [Fierce - 2 GHz mid-band by 2030](https://www.fierce-network.com/5g/mobile-industry-needs-2-ghz-mid-band-spectrum-by-2030-gsma)).
- **Forward (to 2032): at least ~1,400 MHz of *additional* mid-band** industry-wide to keep up with traffic [FACT, single-source] ([GSMA mid-band needs](https://www.gsma.com/connectivity-for-good/spectrum/gsma_resources/5g-mid-band-spectrum-needs-vision-2030/)).

Plus low-band for coverage and penetration: a competitive operator also needs a low-band layer (600/700/850 MHz, typically ~2x10 MHz to ~2x20 MHz) to reach rural areas and inside buildings (the speed-vs-connections tradeoff in [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md)).

**The working number this doc carries:** **~100 MHz of mid-band at the competitive floor; ~200 MHz of total low-plus-mid to match an incumbent.**

### 1.2 The revealed-preference check (actual US carrier holdings)

What the incumbents actually hold confirms the benchmark. Population-weighted, excluding mmWave [FACT, multi-source]:

| Carrier | Total low + mid-band held | Mid-band depth | Source |
|---|---|---|---|
| **AT&T** | ~375 MHz (2nd largest after the EchoStar trade) | ~100 to 120 MHz C-band/3.45 GHz | [PolicyTracker - spectrum snapshot](https://www.policytracker.com/blog/spectrum-snapshot-att-becomes-the-second-largest-spectrum-holder-in-the-us-after-echostar-trade/) |
| **T-Mobile** | ~350+ MHz overall | ~320 MHz (2.5 GHz depth) | [Motley Fool - T-Mobile spectrum advantage](https://www.fool.com/investing/2021/03/17/t-mobile-spectrum-advantage-over-verizon-att/), [Fierce](https://www.fierce-network.com/operators/at-t-touts-mmwave-spectrum-gains-verizon-still-has-nearly-2x-as-much) |
| **Verizon** | ~279 to 295 MHz | ~140 to 161 MHz C-band avg nationwide | [PolicyTracker](https://www.policytracker.com/blog/spectrum-snapshot-att-becomes-the-second-largest-spectrum-holder-in-the-us-after-echostar-trade/) |

Sources cross-checked: [PolicyTracker spectrum snapshot](https://www.policytracker.com/blog/spectrum-snapshot-att-becomes-the-second-largest-spectrum-holder-in-the-us-after-echostar-trade/), [DCD - Verizon/AT&T full C-band](https://www.datacenterdynamics.com/en/news/verizon-and-att-receive-full-access-to-entire-c-band-spectrum/), [Fierce - mmWave holdings](https://www.fierce-network.com/operators/at-t-touts-mmwave-spectrum-gains-verizon-still-has-nearly-2x-as-much).

**The read:** a real competitive operator runs on **~280 to 375 MHz of sub-7-GHz spectrum**, of which ~100 to 320 MHz is the prized mid-band. The GSMA's 80 to 100 MHz "to launch" is the *floor*; the incumbents sit well above it. A new entrant aiming to be a peer, not a niche player, is therefore sizing a **100 to 200 MHz acquisition**, which is what the dollar math in Section 3 prices.

---

## 2. From Whom You Buy or Lease, and the $/MHz-POP Benchmarks

Three doors. The prior doc covered the *auction* door's prices; this doc adds the *secondary-market* and *holder* doors, which the prior doc flagged as open questions.

### 2.1 Door 1: the primary auction (from the government) - closed for greenfield

The FCC (US), Ofcom (UK), Bundesnetzagentur (Germany) clear a band and auction it. Prices, all from [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md) [FACT]:

| Region / band | $/MHz-POP | Note |
|---|---|---|
| US C-band (Auction 107) | ~$0.94 | most expensive mid-band auction ever |
| US 3.45 GHz (Auction 110) | ~$0.72 | |
| US AWS-3 (Auction 97) | ~$2.72 paired | outlier high |
| US mmWave | ~$0.002 to $0.007 | near floor |
| Europe mid-band | ~EUR 0.08 to 0.36 (avg ~EUR 0.19) | far below US |

**Why this door is closed in practice:** there is no comparable unassigned greenfield US mid-band block left to auction (the next greenfield is FR3/6G, Section 4, years away). To use this door you would have to wait for the FR3 auctions ~2028 to 2032+.

### 2.2 Door 2: the secondary market (from a carrier or holder) - the realistic door

Spectrum licenses can be bought, sold, and leased post-auction, subject to FCC approval. The prior doc flagged "what does a lease/transfer actually cost per MHz-POP?" as unanswered. Three 2024-26 deals answer it, and they price **in the same range as the primary auctions**:

| Deal (year) | Buyer <- Seller | Spectrum | Price | Implied $/MHz-POP | Status |
|---|---|---|---|---|---|
| **UScellular sale (Dec 2024)** | AT&T <- UScellular | 1,250M MHz-POPs of 3.45 GHz + 331M MHz-POPs of 700 MHz B/C (1,581M total) | $1.018B | **~$0.65** [DERIVED] | done |
| **UScellular sale (2024)** | Verizon <- UScellular | 663M MHz-POPs of 850 MHz | ~$1B | **~$1.5** [DERIVED, low-band premium] | done |
| **EchoStar D2D (2025-26)** | SpaceX <- EchoStar | ~65 MHz nationwide (AWS-4 + H-block + AWS-3), ~342M POPs | ~$17B | **~$1.03** [FACT, single-source on decimal] | approved May 2026 |

Sources: AT&T deal [RCR Wireless](https://www.rcrwireless.com/20241108/carriers/att-uscellular-spectrum) ($1.018B / 1,581M MHz-POPs = $0.644); Verizon deal [Light Reading - Verizon snapping up spectrum](https://www.lightreading.com/5g/verizon-keeps-snapping-up-spectrum-and-small-carriers); EchoStar implied ~$1.03/MHz-POP [SDxCentral - SpaceX grabs EchoStar spectrum](https://www.sdxcentral.com/news/spacex-grabs-more-echostar-spectrum/), [DCD - SpaceX EchoStar $17B](https://www.datacenterdynamics.com/en/news/spacex-acquires-echostars-aws-4-and-h-block-spectrum-for-17bn/) (deal value double-sourced; the per-MHz-POP decimal is single-source and should be treated as ESTIMATE).

**The finding:** secondary-market **mid-band trades at ~$0.65 to ~$1.03 per MHz-POP**, bracketing the primary-auction range, and **low-band trades at a premium (~$1.5/MHz-POP)** because of its coverage value (the speed-vs-connections tradeoff priced in dollars). The secondary market does **not** offer an entrant a discount: you pay roughly auction prices, you just avoid waiting for an auction. The FCC reviews any transfer that would push a buyer over ~one-third of the suitable-and-available spectrum below 1 GHz ("enhanced factor" case-by-case review) [FACT] ([FCC - mobile spectrum holdings policies](https://www.fcc.gov/wireless/bureau-divisions/competition-infrastructure-policy-division/policies-regarding-mobile)), which is a barrier to a large entrant aggregating low-band but not to a moderate position.

### 2.3 Door 3: a distressed / MSS spectrum holder (EchoStar, Ligado) - the satellite entrant's door

The blocks a *satellite* entrant can actually get are the ones that were satellite/MSS spectrum to begin with, held by financially-pressed owners:
- **EchoStar** (AWS-4, H-block, AWS-3, plus S-band/MSS): sold the AWS-4/H-block to SpaceX (~$17B) and is selling more, under FCC pressure over its build-out obligations [FACT] ([EchoStar IR](https://ir.echostar.com/news-releases/news-release-details/echostar-announces-spectrum-sale-and-commercial-agreement-spacex), [Octus - EchoStar $19B S-band to SpaceX](https://octus.com/resources/articles/echostar-expects-to-resolve-fcc-inquiries-with-19b-s-band-spectrum-sale-to-spacex/)).
- **Ligado** (L-band MSS, ~1.5/1.6 GHz): leased AST up to ~45 MHz on 80+ year terms [FACT] (prior doc [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md)).

**This is the only door where a non-hyperscale entrant has historically gotten dedicated mid/low spectrum** without a national auction, precisely because these are distressed MSS holdings, not prime cellular bands. But the supply is finite (a handful of holders) and the recent buyer (SpaceX) is hyperscale, so the price is set by deep pockets.

---

## 3. The Total-Dollar Translation: US-plus-Europe at a Competitive Bandwidth

This is the headline computation the prior docs set up but never performed: take the **required MHz** (Section 1), the **$/MHz-POP** (Section 2), and the **POP base**, and produce a single dollar figure.

**POP bases** [FACT]:
- **US: ~342M** (Census Jan 2025 projection 341.1M; mid-2025 ~341.8M) ([Census - new year population](https://www.census.gov/library/stories/2024/12/new-year-population.html)).
- **Europe (EU-27 + UK): ~518M** (EU-27 ~450.4M Jan 2025 + UK ~68M) ([Eurostat - EU population 450.4M](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20250711-1), [AA - EU exceeds 450M](https://www.aa.com.tr/en/europe/eus-population-exceeds-450m-in-2025/3628268)).

### 3.1 The arithmetic [DERIVED]

**For a single competitive 100 MHz mid-band layer:**

| Region | MHz | POPs | MHz-POPs | $/MHz-POP | Total |
|---|---|---|---|---|---|
| **US** | 100 | 342M | 34,200M | $0.65 (secondary low) | **~$22B** |
| **US** | 100 | 342M | 34,200M | $0.94 (C-band) | **~$32B** |
| **US** | 100 | 342M | 34,200M | $1.03 (EchoStar) | **~$35B** |
| **Europe** | 100 | 518M | 51,800M | EUR 0.19 (avg) | **~EUR 9.8B (~$10.6B)** |
| **Europe** | 100 | 518M | 51,800M | EUR 0.36 (Italy high) | **~EUR 18.6B (~$20B)** |

**Combined US + Europe, 100 MHz mid-band:**
- **Low case (US secondary $0.65 + Europe avg EUR 0.19): ~$22B + ~$11B = ~$33B.**
- **High case (US EchoStar $1.03 + Europe high EUR 0.36): ~$35B + ~$20B = ~$55B.**
- **Central: ~$32B to ~$46B.**

**Doubling to ~200 MHz (incumbent-matching depth) roughly doubles it: ~$65B to ~$90B.**

### 3.2 What the number means

- **Spectrum-only.** This is the price of the *licenses alone*, before satellites, ground stations, network, or operations. It is the entry ticket, not the build.
- **It dwarfs the SpaceX EchoStar buy.** SpaceX paid ~$17B for ~65 MHz over the US *only*. A 100 MHz US-plus-Europe position is ~$33B+; a 200 MHz one ~$65B+. Even the largest private spectrum buy in history bought a fraction of a "competitive national-plus" position over two continents.
- **It confirms the prior verdict with numbers attached.** [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md) concluded "buying terrestrial spectrum outright is not a realistic path" and "the last greenfield slice cost $81B." This doc pins it: **a competitive US-plus-Europe spectrum position is a ~$30B to ~$90B line item, spectrum-only**, which is why every realistic entrant (AST, Starlink) leases under SCS instead.
- **Europe is the cheaper half** (~EUR 0.19 vs US ~$0.94 mid-band), so a Europe-weighted strategy lowers the bill, but Europe is also 27+ separate national auctions, not one.

**Caveat on the method:** these are flat-$/MHz-POP estimates. Real auctions vary 2 to 3x by market (top US metros hit ~$1.30/MHz-POP for C-band); a true build would weight expensive metros higher. The figures are order-of-magnitude entry-cost anchors, not a bid model.

---

## 4. The 6G Question: Decided vs Open

The prior doc introduced FR3 and WRC-27 at a high level. This section answers the three specific sub-questions the topic asks: **what spectrum, auctioned-or-held, and can a satellite entrant get it**, each split into *decided* and *open*.

### 4.1 What spectrum will 6G use?

**Decided:**
- 6G's new spectrum is the **upper mid-band, FR3 (7.125 to 24.25 GHz)** in 3GPP terms, sitting between FR1 (<7.125 GHz) and FR2 mmWave (24.25 to 71 GHz) [FACT] ([Murata - FR3 for 6G](https://article.murata.com/en-us/article/band-fr3-for-6g), [arXiv 2502.17914 - upper mid-band for 6G](https://arxiv.org/html/2502.17914)).
- The **WRC-27 Agenda Item 1.7 study bands** (agreed at WRC-23) are **7.125 to 8.4 GHz, 4.4 to 4.8 GHz, and 14.8 to 15.35 GHz** [FACT] ([GSOA - WRC-27 AI 1.7](https://gsoasatellite.com/wp-content/uploads/WRC-27-AGENDA-ITEM-1.7.pdf), [Transfinite - WRC-27 agenda](https://www.transfinite.com/content/wrc2027a8), [Samsung Research - upper mid-band for 6G](https://research.samsung.com/blog/Upper-Mid-Band-Spectrum-for-6G-Opportunities-and-Key-Enablers)).
- The **"golden band" 7.125 to 8.4 GHz** is the lead candidate, valued for "favorable propagation and wider spectrum chunks without adjacent incumbents," able to offer **>400 MHz per operator vs ~100 MHz in FR1** [FACT] ([arXiv 2506.18672](https://arxiv.org/html/2506.18672v1), [Nokia - 6G mid-band](https://www.nokia.com/6g/6g-mid-band-spectrum-technology-explained/)).

**Open:**
- **Which exact slices** get identified for IMT at WRC-27 (Nov-Dec 2027), and **how much** of each. ITU-R sharing/compatibility studies are still in progress; conclusions are expected *at* WRC-27, not before [FACT] ([ITU-R WRC-27 studies](https://www.itu.int/en/ITU-R/study-groups/rcpm/Pages/wrc-27-studies.aspx), [GSMA - road to WRC-27](https://www.gsma.com/connectivity-for-good/spectrum/the-road-to-wrc-27-a-new-cycle-begins/)).

### 4.2 Is it auctioned, or already held?

**Decided: neither, yet.** FR3 IMT bands are **not allocated to mobile, not auctioned, and owned by no carrier** for mobile use today. They are currently occupied by **incumbents**: Fixed-Satellite Service (FSS), Fixed Service (point-to-point microwave links), and federal/military users [FACT] ([arXiv 2506.18672](https://arxiv.org/html/2506.18672v1), [npj Wireless - spectrum opportunities](https://www.nature.com/articles/s44459-025-00008-9)).

This is the structurally important fact for a forward-looking (~10 year) thesis: **FR3 is the one place where the "all the good spectrum is already filed/owned" wall is *not yet* built.** Unlike C-band or AWS, which an entrant can only buy on the secondary market at full price, FR3 mobile licenses **do not exist yet** and will be created fresh.

**Open / timeline [DERIVED from the WRC cycle]:** the sequence is (1) WRC-27 identifies the bands for IMT (Nov-Dec 2027), (2) national regulators (FCC, Ofcom) then clear incumbents and write service rules, (3) national auctions follow. Realistically **~2028 to 2032+** before any FR3 mobile licenses are sold, consistent with 6G commercial launches "later in the decade." Whoever wants to participate must be at the table during the WRC-27 and national-rulemaking phases *now*.

### 4.3 Can a satellite (NTN) entrant access FR3? (the decision-relevant question)

**Decided / strong trajectory: largely no for a new mobile-from-space service, for two reasons.**

1. **The regulatory framing is terrestrial.** WRC-27 AI 1.7 is explicitly for "the **terrestrial component** of IMT" [FACT] ([GSOA - WRC-27 AI 1.7](https://gsoasatellite.com/wp-content/uploads/WRC-27-AGENDA-ITEM-1.7.pdf), [Transfinite](https://www.transfinite.com/content/wrc2027a8)). The new identifications are being shaped for ground networks, not for a satellite operator to acquire a national mobile license.
2. **The physics is hostile to a phone-to-LEO link at 7 to 15 GHz.** "Satellite transmission links in this range suffer higher path loss for fixed antenna gains... making it difficult to deliver data to handheld devices, especially on the uplink under non-line-of-sight scenarios" [FACT, single-source: arXiv 2506.18672]. The higher frequency that gives FR3 its wide channels also makes it worse for a wide satellite beam to a handset than today's sub-1-GHz D2C bands.

**Where the satellite role actually is [FACT]:** FSS/NTN already hold **adjacent** FR3 slices, e.g. **10.7 to 12.7 GHz** (space-to-Earth) and **13.85 to 14 GHz** (uplinks) ([arXiv 2506.18672](https://arxiv.org/html/2506.18672v1)). So a satellite operator's relationship to FR3 is as an **incumbent neighbor to be protected/coordinated**, and the live regulatory work is **TN/NTN coexistence** (terrestrial 6G not interfering with the satellites already there), not a new mobile allocation a D2C entrant could build on. The FCC has proposed TN/NTN sharing rules and arXiv work on interference nulling for TN/NTN co-existence in the upper mid-band is active [FACT] ([npj Wireless](https://www.nature.com/articles/s44459-025-00008-9), [arXiv 2510.08824 - TN/NTN coexistence](https://arxiv.org/html/2510.08824)).

**Open:** the **exact TN/NTN coexistence conditions** are unsettled and are precisely what WRC-27 is meant to standardize [FACT] ([ITU-R WRC-27 studies](https://www.itu.int/en/ITU-R/study-groups/rcpm/Pages/wrc-27-studies.aspx)). It is *not formally impossible* that a future NTN identification appears, and 3GPP NTN is advancing (Release 19 store-and-forward/regenerative payloads, Release 20 bundling 6G NTN studies) [FACT] ([Ericsson - Rel-19 NTN](https://www.ericsson.com/en/blog/2024/10/ntn-payload-architecture), [InterDigital - Rel-20 6G](https://www.interdigital.com/post/paving-the-path-to-6g-key-takeaways-for-3gpp-release-20)). But NTN in 6G is being designed as a **complementary coverage tier integrated with terrestrial**, on its own MSS/FSS bands, not as a satellite claim on the FR3 mobile pie.

**The verdict for the model:** **6G/FR3 is a terrestrial greenfield, opening ~2028 to 2032+, that a satellite entrant should not count on owning.** The satellite path stays where the prior docs put it: lease a carrier's existing sub-7-GHz band under SCS (today), or hold dedicated MSS/FSS spectrum (EchoStar/Ligado model). FR3 changes the *terrestrial* competitive landscape (new capacity for the carriers a space layer competes with), but it does not open a new door for space-based mobile.

---

## 5. What This Adds to the Model

1. **The required quantity is ~100 MHz (floor) to ~200 MHz (incumbent-matching).** GSMA's 80 to 100 MHz to launch, confirmed by carriers actually holding ~280 to 375 MHz. This is the missing multiplier the prior docs lacked.
2. **The total entry ticket is ~$32B to ~$46B for a 100 MHz US-plus-Europe position, ~$65B to ~$90B for 200 MHz, spectrum-only.** A single [DERIVED] headline from sourced $/MHz-POP and POP bases.
3. **The secondary-market price is ~$0.65 to ~$1.03/MHz-POP for mid-band (low-band a premium), the same range as primary auctions.** The secondary door (the realistic one) offers no discount; it only avoids waiting. This answers the prior doc's open question on lease/transfer cost with three real 2024-26 deals.
4. **The satellite entrant's only buy/lease door is distressed MSS holders (EchoStar, Ligado), and the recent buyer was hyperscale.** Finite supply, deep-pocket pricing.
5. **6G/FR3 is a terrestrial greenfield opening ~2028 to 2032+, not yet auctioned or held, and a satellite entrant should not plan on accessing it.** Decided: terrestrial-led, physics-hostile to LEO-to-handset. Open: TN/NTN coexistence rules. The space path remains SCS lease + owned MSS spectrum, unchanged by 6G.

---

## 6. Sources

Quantity benchmark:
- [GSMA - 5G Spectrum Guide](https://www.gsma.com/connectivity-for-good/spectrum/5g-spectrum-guide-2/)
- [GSMA - Vision 2030: Spectrum Needs for 5G](https://www.gsma.com/connectivity-for-good/spectrum/vision-2030-spectrum-needs-for-5g/)
- [GSMA - 5G Mid-Band Spectrum Needs Vision 2030](https://www.gsma.com/connectivity-for-good/spectrum/gsma_resources/5g-mid-band-spectrum-needs-vision-2030/)
- [Fierce - Mobile industry needs 2 GHz of mid-band by 2030 (GSMA)](https://www.fierce-network.com/5g/mobile-industry-needs-2-ghz-mid-band-spectrum-by-2030-gsma)
- [Nokia - 5G spectrum bands explained](https://www.nokia.com/thought-leadership/articles/spectrum-bands-5g-world/)

Carrier holdings:
- [PolicyTracker - AT&T second-largest spectrum holder after EchoStar trade](https://www.policytracker.com/blog/spectrum-snapshot-att-becomes-the-second-largest-spectrum-holder-in-the-us-after-echostar-trade/)
- [Fierce - AT&T mmWave gains, Verizon nearly 2x](https://www.fierce-network.com/operators/at-t-touts-mmwave-spectrum-gains-verizon-still-has-nearly-2x-as-much)
- [DCD - Verizon and AT&T full access to entire C-band](https://www.datacenterdynamics.com/en/news/verizon-and-att-receive-full-access-to-entire-c-band-spectrum/)
- [Motley Fool - T-Mobile spectrum advantage](https://www.fool.com/investing/2021/03/17/t-mobile-spectrum-advantage-over-verizon-att/)

Secondary-market deals:
- [RCR Wireless - AT&T buys UScellular spectrum $1.018B](https://www.rcrwireless.com/20241108/carriers/att-uscellular-spectrum)
- [Light Reading - Verizon keeps snapping up spectrum and small carriers](https://www.lightreading.com/5g/verizon-keeps-snapping-up-spectrum-and-small-carriers)
- [SDxCentral - SpaceX grabs more EchoStar spectrum](https://www.sdxcentral.com/news/spacex-grabs-more-echostar-spectrum/)
- [DCD - SpaceX acquires EchoStar AWS-4/H-block $17B](https://www.datacenterdynamics.com/en/news/spacex-acquires-echostars-aws-4-and-h-block-spectrum-for-17bn/)
- [EchoStar IR - spectrum sale and commercial agreement with SpaceX](https://ir.echostar.com/news-releases/news-release-details/echostar-announces-spectrum-sale-and-commercial-agreement-spacex)
- [Octus - EchoStar $19B S-band sale to SpaceX](https://octus.com/resources/articles/echostar-expects-to-resolve-fcc-inquiries-with-19b-s-band-spectrum-sale-to-spacex/)
- [FCC - Policies regarding mobile spectrum holdings](https://www.fcc.gov/wireless/bureau-divisions/competition-infrastructure-policy-division/policies-regarding-mobile)

POP bases:
- [US Census - new year population (341.1M Jan 2025)](https://www.census.gov/library/stories/2024/12/new-year-population.html)
- [Eurostat - EU population 450.4M Jan 2025](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20250711-1)
- [AA - EU population exceeds 450M in 2025](https://www.aa.com.tr/en/europe/eus-population-exceeds-450m-in-2025/3628268)

6G / FR3 / WRC-27:
- [GSOA - WRC-27 Agenda Item 1.7](https://gsoasatellite.com/wp-content/uploads/WRC-27-AGENDA-ITEM-1.7.pdf)
- [Transfinite - Agenda for WRC-2027](https://www.transfinite.com/content/wrc2027a8)
- [ITU-R - Preparatory studies for WRC-27](https://www.itu.int/en/ITU-R/study-groups/rcpm/Pages/wrc-27-studies.aspx)
- [GSMA - The road to WRC-27](https://www.gsma.com/connectivity-for-good/spectrum/the-road-to-wrc-27-a-new-cycle-begins/)
- [Samsung Research - Upper mid-band spectrum for 6G](https://research.samsung.com/blog/Upper-Mid-Band-Spectrum-for-6G-Opportunities-and-Key-Enablers)
- [Nokia - 6G mid-band spectrum technology explained](https://www.nokia.com/6g/6g-mid-band-spectrum-technology-explained/)
- [Murata - FR3 frequency band for 6G](https://article.murata.com/en-us/article/band-fr3-for-6g)
- [arXiv 2506.18672 - Spectrum opportunities: D2D satellite to 6G](https://arxiv.org/html/2506.18672v1)
- [npj Wireless - Spectrum opportunities for the wireless future](https://www.nature.com/articles/s44459-025-00008-9)
- [arXiv 2502.17914 - Upper mid-band spectrum for 6G](https://arxiv.org/html/2502.17914)
- [arXiv 2510.08824 - TN/NTN downlink coexistence in upper mid-band](https://arxiv.org/html/2510.08824)
- [Ericsson - 5G NTN in 3GPP Rel-19](https://www.ericsson.com/en/blog/2024/10/ntn-payload-architecture)
- [InterDigital - Paving the path to 6G: 3GPP Release 20](https://www.interdigital.com/post/paving-the-path-to-6g-key-takeaways-for-3gpp-release-20)

---

## 7. Confidence

**Overall: medium-high.**

- **High:** the GSMA 80 to 100 MHz "to launch" and 2 GHz/country-by-2030 benchmarks; the US carrier holdings (~280 to 375 MHz); the FR3 study bands and WRC-27 AI 1.7 terrestrial framing; the EchoStar ~$17B deal value. Each is 2+ independent sources or a primary filing.
- **Medium-high:** the secondary-market $/MHz-POP decimals. The AT&T-UScellular ~$0.65 is a clean [DERIVED] from a double-sourced $1.018B/1,581M MHz-POPs. The EchoStar ~$1.03/MHz-POP decimal is single-source (SDxCentral) and should be treated as ESTIMATE; the deal value is double-sourced. The Verizon-UScellular ~$1.5 is [DERIVED] from a single $1B/663M MHz-POP figure.
- **Medium (DERIVED arithmetic):** the total-dollar US-plus-Europe figures. They assume a flat $/MHz-POP across a national footprint; real auctions vary 2 to 3x by market, so treat ~$32B to ~$46B (100 MHz) as an order-of-magnitude entry-cost anchor, not a bid.
- **Medium-high in direction, not formally settled:** "a satellite entrant cannot get FR3." The terrestrial framing and the LEO-to-handset physics are well-attested, but WRC-27 has not concluded and a future NTN identification is not impossible. It is a trajectory call.

---

## 8. Open Questions

- **Market-weighted total cost.** The Section 3 figures are flat-rate. A metro-weighted build (top US markets at ~$1.30/MHz-POP) would raise the US number; a rural-only footprint would lower it. A weighted model would sharpen the entry-cost anchor.
- **What fraction of a 100 MHz position can be assembled from distressed MSS holders alone?** EchoStar + Ligado are finite. After SpaceX's buy, how much dedicated mid/low spectrum is still available to a new entrant via the "Door 3" path, and at what price?
- **The Europe path cost in practice.** Europe is ~EUR 0.19/MHz-POP but 27+ national auctions. The real cost and timeline of assembling a pan-European 100 MHz position (vs the single-auction US) is not quantified here.
- **Will any FR3 band carry an NTN identification?** The single most decision-relevant open item for the 10-year thesis: whether WRC-27 or a later cycle opens any upper-mid-band slice to satellite mobile, or whether NTN stays confined to MSS/FSS bands and SCS leases. Worth tracking through the WRC-27 conclusion (late 2027).
- **6G's effect on the *terrestrial* competitor.** FR3 gives carriers >400 MHz/operator of new capacity. How much does that widen the terrestrial cost/capacity advantage over a space layer (the [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) ~20x per-GB gap)? A 6G-era re-run of that gap is unresolved.

---

## 9. Claims Created (COMM-229 .. COMM-248)

| Claim ID | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-229 | GSMA: mid-band per operator to launch competitive 5G | 80 to 100 MHz contiguous | FACT | [GSMA 5G Spectrum Guide](https://www.gsma.com/connectivity-for-good/spectrum/5g-spectrum-guide-2/), [Nokia](https://www.nokia.com/thought-leadership/articles/spectrum-bands-5g-world/) |
| COMM-230 | GSMA: mmWave per operator recommendation | ~1 GHz | FACT (single-source) | [GSMA 5G Spectrum Guide](https://www.gsma.com/connectivity-for-good/spectrum/5g-spectrum-guide-2/) |
| COMM-231 | GSMA: national mid-band planning target by 2030 | ~2 GHz per country | FACT | [GSMA Vision 2030](https://www.gsma.com/connectivity-for-good/spectrum/vision-2030-spectrum-needs-for-5g/), [Fierce](https://www.fierce-network.com/5g/mobile-industry-needs-2-ghz-mid-band-spectrum-by-2030-gsma) |
| COMM-232 | GSMA: additional mid-band needed industry-wide by 2032 | at least ~1,400 MHz | FACT (single-source) | [GSMA mid-band needs](https://www.gsma.com/connectivity-for-good/spectrum/gsma_resources/5g-mid-band-spectrum-needs-vision-2030/) |
| COMM-233 | AT&T total low+mid-band held (pop-weighted) | ~375 MHz (2nd largest US holder post-EchoStar trade) | FACT | [PolicyTracker](https://www.policytracker.com/blog/spectrum-snapshot-att-becomes-the-second-largest-spectrum-holder-in-the-us-after-echostar-trade/) |
| COMM-234 | T-Mobile total / mid-band depth | ~350+ MHz total; ~320 MHz mid-band depth | FACT | [Motley Fool](https://www.fool.com/investing/2021/03/17/t-mobile-spectrum-advantage-over-verizon-att/), [Fierce](https://www.fierce-network.com/operators/at-t-touts-mmwave-spectrum-gains-verizon-still-has-nearly-2x-as-much) |
| COMM-235 | Verizon total low+mid-band held | ~279 to 295 MHz; ~140 to 161 MHz C-band avg | FACT | [PolicyTracker](https://www.policytracker.com/blog/spectrum-snapshot-att-becomes-the-second-largest-spectrum-holder-in-the-us-after-echostar-trade/), [DCD](https://www.datacenterdynamics.com/en/news/verizon-and-att-receive-full-access-to-entire-c-band-spectrum/) |
| COMM-236 | Competitive operator working spectrum quantity | ~100 MHz mid-band floor; ~200 MHz total to match incumbent | DERIVED | GSMA + carrier holdings (COMM-229..235) |
| COMM-237 | AT&T <- UScellular secondary deal (Dec 2024) | $1.018B for 1,581M MHz-POps (1,250M @3.45GHz + 331M @700MHz) | FACT | [RCR Wireless](https://www.rcrwireless.com/20241108/carriers/att-uscellular-spectrum) |
| COMM-238 | AT&T-UScellular implied secondary price | ~$0.65 per MHz-POP | DERIVED | [RCR Wireless](https://www.rcrwireless.com/20241108/carriers/att-uscellular-spectrum) ($1.018B / 1,581M) |
| COMM-239 | Verizon <- UScellular 850 MHz deal | ~$1B for 663M MHz-POPs; ~$1.5/MHz-POP (low-band premium) | FACT (deal) / DERIVED (decimal) | [Light Reading](https://www.lightreading.com/5g/verizon-keeps-snapping-up-spectrum-and-small-carriers) |
| COMM-240 | SpaceX <- EchoStar AWS-4/H-block implied price | ~$1.03 per MHz-POP (~$17B / ~65 MHz / ~342M POPs) | FACT (deal value) / ESTIMATE (decimal, single-source) | [SDxCentral](https://www.sdxcentral.com/news/spacex-grabs-more-echostar-spectrum/), [DCD](https://www.datacenterdynamics.com/en/news/spacex-acquires-echostars-aws-4-and-h-block-spectrum-for-17bn/) |
| COMM-241 | Secondary-market mid-band price range | ~$0.65 to ~$1.03 per MHz-POP (low-band a premium ~$1.5); same range as primary auctions | DERIVED | COMM-238..240 + auction prices (COMM-002..006) |
| COMM-242 | FCC below-1-GHz aggregation review threshold | "enhanced factor" case-by-case review if holding ~1/3+ of suitable/available sub-1-GHz | FACT | [FCC mobile spectrum holdings](https://www.fcc.gov/wireless/bureau-divisions/competition-infrastructure-policy-division/policies-regarding-mobile) |
| COMM-243 | US POP base | ~342M (Census Jan 2025 projection 341.1M) | FACT | [US Census](https://www.census.gov/library/stories/2024/12/new-year-population.html) |
| COMM-244 | Europe POP base (EU-27 + UK) | ~518M (EU-27 ~450.4M + UK ~68M) | FACT | [Eurostat](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20250711-1), [AA](https://www.aa.com.tr/en/europe/eus-population-exceeds-450m-in-2025/3628268) |
| COMM-245 | Total spectrum cost, 100 MHz US+Europe | ~$32B to ~$46B (US ~$22-35B + Europe ~$11-20B), spectrum-only | DERIVED | $/MHz-POP (COMM-002, 238-241) x POPs (COMM-243-244) |
| COMM-246 | Total spectrum cost, 200 MHz US+Europe | ~$65B to ~$90B, spectrum-only | DERIVED | 2x COMM-245 |
| COMM-247 | 6G WRC-27 AI 1.7 study bands (terrestrial IMT) | 7.125-8.4 GHz ("golden band"), 4.4-4.8 GHz, 14.8-15.35 GHz; not allocated/auctioned/owned for mobile, currently FSS/FS/federal incumbents; auctions ~2028-2032+ | FACT (bands/status) / DERIVED (timeline) | [GSOA](https://gsoasatellite.com/wp-content/uploads/WRC-27-AGENDA-ITEM-1.7.pdf), [Transfinite](https://www.transfinite.com/content/wrc2027a8), [arXiv 2506.18672](https://arxiv.org/html/2506.18672v1), [ITU-R](https://www.itu.int/en/ITU-R/study-groups/rcpm/Pages/wrc-27-studies.aspx) |
| COMM-248 | Satellite (NTN) access to FR3/6G mobile spectrum | Largely no: WRC-27 AI 1.7 framed for terrestrial IMT; LEO-to-handset physics hostile at 7-15 GHz (high path loss, NLOS uplink); satellite role is incumbent FSS/NTN coexistence (10.7-12.7 GHz, 13.85-14 GHz adjacent), not a new mobile allocation; TN/NTN coexistence rules open at WRC-27 | FACT (framing/physics) / trajectory call | [GSOA](https://gsoasatellite.com/wp-content/uploads/WRC-27-AGENDA-ITEM-1.7.pdf), [arXiv 2506.18672](https://arxiv.org/html/2506.18672v1), [npj Wireless](https://www.nature.com/articles/s44459-025-00008-9), [arXiv 2510.08824](https://arxiv.org/html/2510.08824) |
