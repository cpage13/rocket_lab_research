# Fixed Broadband Deployment Economics, Cost and Unit Economics of Fiber, Cable, and Fixed Wireless

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:** mirrors the structure of [research/economics/ai_datacenter_tam.md](ai_datacenter_tam.md) (the data-center track's TAM-framing doc). That doc sizes AI-compute demand and the terrestrial-constraint "push" factors; this doc is the parallel cost-and-unit-economics base for the COMMUNICATIONS track. Where this doc references a space alternative, it does so only to answer the founder's incremental-value question and does not duplicate any space-side cost stack.

> **Scope note:** This document covers the cost of building **fixed terrestrial broadband** to a home: fiber (FTTH/FTTP), cable (HFC/DOCSIS), and fixed wireless access (FWA). It is US-primary, then Europe and other major markets where data exists. It then addresses the founder's framing question: where fiber or cable already exists, does a space alternative add value, or is the value only in unserved, underserved, and remote areas. **No verdict on the space business is offered here**, this is base material for the shared library.

> **Reading guide:** Each hard number is tagged **[FACT]** (reported / observed 2024–26 data), **[ESTIMATE]** (a number that varies by operator and is given as a working range), or **[PROJECTION]** (forward forecast). Hard numbers are cross-checked against 2+ independent sources; any single-source figure is flagged "single source".

> **China is excluded** from the main analysis (see the China aside in Section 7).

---

## Summary / Verdict

- **Fiber (FTTH) cost per home passed:** roughly **$700–$1,500 in urban/suburban areas and $3,000–$6,000 in rural areas** [FACT, multi-source], with a typical "average" passing often quoted near **$1,000–$1,250** [FACT]. On top of passing cost, the **per-home-connected (drop + install)** adds roughly **$500–$700** [FACT]. Underground build runs **~$18/ft** and aerial **~$8/ft** (2025 medians, up 3% and 14% YoY) [FACT]. **Labor is 64–72% of deployment cost** [FACT].
- **Cable / HFC upgrade is far cheaper per home than new fiber:** a **DOCSIS 4.0 / mid-split upgrade is ~$100–$300 per home passed** [FACT, multi-source] because the coax plant already exists. This is the central asymmetry: incumbents already passing a home can defend it for a small fraction of a greenfield fiber build.
- **Fixed wireless access (FWA) is the most capex-light:** roughly **$300–$800 per subscriber all-in** (radio share of network + customer equipment), versus fiber's **$800–$6,000+ per home** [FACT/ESTIMATE]. FWA's economic catch is that capacity is shared spectrum, so it competes best in lower-density pockets and as a fast share-grab, not as an unlimited-capacity pipe.
- **Unit economics turn on take-rate.** US fiber take-rates average **~46–47%** [FACT], so **more than half of homes passed generate no revenue**. Target IRRs are **~10–15%** with **payback often 10+ years** [ESTIMATE]; at 40–50% penetration retail returns reach **18–25%/yr** [ESTIMATE], but a **third overbuilder into a two-incumbent market earns only ~4% unlevered pre-tax ROI** [FACT, single primary source]. Monthly residential ARPU is **~$50–$150** [FACT].
- **Where ground broadband is uneconomic:** cost per passing scales inversely with density. The extreme rural tail reaches **~$200,000–$230,000 per passing** [FACT, single primary source], far beyond any payback. As of mid-2025, **~4.2 million US locations remained BEAD-eligible** (unserved/underserved) [FACT], down ~65% from the ~13.8M (~7.8M unserved + ~6M underserved) counted in 2023 [FACT]. Roughly **6% of US households are "broadband deserts"** with no or only legacy-DSL terrestrial options [FACT].
- **Incremental-value answer (preview of Section 6):** Where fiber or upgraded cable already passes a home, a space alternative adds **little economic value**, the incumbent's defend-cost is tiny ($100–$300/home for cable, sunk for fiber) and its ARPU and latency beat satellite. The space value concentrates in the **unserved/underserved/remote tail** where per-passing cost runs into the thousands-to-hundreds-of-thousands of dollars and no terrestrial business case closes. That tail is **single-digit-percent of US households but a large absolute count** (millions of locations), and it is where LEO satellite has already taken root.

**Confidence: medium-high.** The per-foot build costs, cable-upgrade costs, FWA capex range, take-rate, and the unserved-location counts are each multi-source and converge. **Medium** on cost-per-home-passed point figures (operator- and density-dependent; ranges are solid, point values vary) and on the extreme-rural and overbuild-ROI figures (each rests on a single primary analyst source; flagged in-line). Europe figures are directional. ARPU and IRR/payback are working ranges, not audited industry constants.

---

## 1. Fiber (FTTH/FTTP), Cost per Home Passed and Connected

Fiber is the gold-standard fixed technology (highest capacity, lowest latency, longest asset life) and the most capital-intensive to build. Cost is dominated by civil works (digging/hanging), and civil works scale with route distance per home, which is why density is destiny.

### Per-unit build cost (US, 2024–25)

| Metric | Value | Tag | Notes |
|---|---|---|---|
| Cost per home passed, urban/suburban | **$700–$1,500** | [FACT] | Lower end dense urban; quoted as low as ~$800 in dense neighborhoods |
| Cost per home passed, rural | **$3,000–$6,000+** | [FACT] | Low density, long drops |
| "Typical/average" cost per home passed | **~$1,000–$1,250** | [FACT] | Also expressed as ~$60,000–$80,000 per route mile |
| Cost per home **connected** (drop + install, on top of passing) | **~$500–$700** | [FACT] | The marginal cost to actually hook up a signed customer |
| Underground build, median | **~$18.00/ft** (2025), +3% YoY | [FACT] | Cartesian/FBA 2025 report |
| Aerial build, median | **~$8.00/ft** (2025), +14% YoY | [FACT] | Cartesian/FBA 2025 report |
| Labor share of deployment cost | **72% underground / 64% aerial** | [FACT] | Median labor ~$12.23/ft underground, ~$4.50/ft aerial |
| Underground vs aerial | Underground ~**2x** aerial cost | [FACT] | Trenching is the most expensive method (~60% costlier than plowing) |

Sources converge: the Fiber Broadband Association / Cartesian *2025 Fiber Deployment Cost Annual Report* sets the per-foot and labor-share figures; multiple infrastructure write-ups put the per-home-passed range at $700–$1,500 urban and $3,000–$6,000 rural, with the ~$1,000–$1,250 "typical" passing and ~$500–$700 connect cost. [FACT, cross-checked.]

### Why the spread is so wide

The single biggest swing factor is **homes per route mile**. In a dense urban block, one mile of fiber passes hundreds of homes, so the per-home share of a ~$60,000–$80,000 route mile is small. In a rural area the same mile may pass a handful of homes, so the per-home cost multiplies. Underground-vs-aerial (a ~2x swing), make-ready work on existing poles, permitting delays, and rock/terrain are the secondary drivers. Labor at 64–72% of cost means wage inflation flows almost directly into deployment cost; **88% of operators surveyed expect costs to rise again in 2026** [FACT].

### Scale reached

US fiber passed **~88 million homes by end-2024** (a record ~10.3M added that year) and crossed **~60% of US households / near 100 million homes** through 2025 (with **11.8M additional passings in 2025**, ~8.1M of them unique homes) [FACT, multi-source]. The implication for the COMMS track: the easy, dense, economic homes are largely already built; the remaining greenfield is progressively rural and expensive.

---

## 2. Cable / HFC (DOCSIS), The Cheap-to-Defend Incumbent

Most US homes are already passed by a hybrid fiber-coax (HFC) cable plant. The relevant cost is therefore **not** a greenfield build but an **upgrade** of existing coax to deliver fiber-like speeds (DOCSIS 3.1 high-split, then DOCSIS 4.0). This is dramatically cheaper than overbuilding with fiber.

| Upgrade / metric | Cost per home passed | Tag | Source operator/analyst |
|---|---|---|---|
| Charter network-evolution plan | **~$100/home passed** | [FACT] | Charter |
| Comcast mid-split + D4.0 groundwork | **< $200/home passed** | [FACT] | Comcast |
| Cable One D4.0 upgrade | **~$200/home passed** | [FACT] | Cable One |
| Credit Suisse D4.0 estimate | **~$180/home passed** | [FACT] | Credit Suisse |
| Analyst range, incremental D4.0 | **$150–$300/home passed** | [FACT] | Multiple |
| Full transition incl. mid/high-split + new modem | **~$250–$400/home passed** | [ESTIMATE] | New modem adds $150–$300/home |
| Prior DOCSIS 3.1 upgrade | **~$10/home** | [FACT] | For context |
| For comparison: FTTP overbuild | **~$1,000/home passed + $500–$700 connect** | [FACT] | See Section 1 |

[FACT, multi-source: Charter, Comcast, Cable One, and Credit Suisse figures all reported independently.]

**This is the structural point of the whole doc.** A cable incumbent can defend a home it already passes for **~$100–$300**, roughly **3x to 10x cheaper** than a fiber overbuilder's ~$1,000+ greenfield passing cost (and far cheaper still than the connect-inclusive total). Where coax already exists, the marginal cost of keeping a customer at competitive speed is small. That is the cost wall any *new* entrant (fiber overbuilder, FWA, or space) faces in already-served territory.

---

## 3. Fixed Wireless Access (FWA), Capex-Light, Capacity-Constrained

FWA delivers broadband over a wireless link from a cell site to a rooftop/window receiver. It rides existing mobile infrastructure, so it avoids the per-home civil works that dominate fiber. It is the capex-light option, with the trade-off that it shares finite radio capacity.

| Metric | Value | Tag | Notes |
|---|---|---|---|
| FWA capex per subscriber (radio share + CPE) | **~$300–$800** | [FACT] | Includes radio and customer-premises equipment |
| Wireless transport network capex component | **~$100–$400** | [ESTIMATE] | vs $500–$1,000 for FTTx per subscriber (same source) |
| Cost-per-bit to connect a household | up to **~74% lower** than wireline | [FACT] | GSMA, single primary source, flag |
| FWA OPEX | can exceed FTTx OPEX | [FACT] | Rental, power, spectrum-licence costs |
| For comparison: fiber per-home | **$800–$6,000+** | [FACT] | Section 1 |

[FACT, FWA $300–$800/subscriber and the fiber $800–$6,000 contrast appear across GSMA and operator/analyst coverage.]

**FWA economics in one line:** very low capex and fast to deploy, but capacity is shared spectrum, so the per-subscriber economics degrade as a sector fills. Operators (T-Mobile, Verizon, AT&T) therefore steer FWA toward **lower-density pockets and quick share-gains** and reserve fiber for high-usage clusters and enterprise. Note one tension in the sources: FWA wins decisively on **capex**, but its **opex** (tower rental, power, spectrum licences) can run *higher* than fiber, so the lifetime-cost advantage is smaller than the build-cost advantage. FWA is best read as the **fast, cheap, lower-density** terrestrial answer, not an unlimited pipe.

### Technology cost ladder (US, summary)

| Technology | Per-home build/upgrade cost | Capacity / quality | Best fit |
|---|---|---|---|
| Cable D4.0 upgrade (existing coax) | **~$100–$300** passed | High (multi-Gig) | Defending already-passed homes |
| FWA | **~$300–$800** / subscriber | Medium, shared | Fast share-grab, lower-density pockets |
| Fiber, urban/suburban | **~$700–$1,500** passed + $500–$700 connect | Highest | Dense greenfield, premium ARPU |
| Fiber, rural | **~$3,000–$6,000+** passed | Highest | Only with subsidy |
| Fiber, extreme rural tail | **up to ~$200,000+** passed | Highest | No business case (Section 5) |

---

## 4. Unit Economics, Take-Rate, ARPU, Payback, Returns

Build cost is only half the equation. A passing earns nothing until a household subscribes, and **fewer than half do**.

| Metric | Value | Tag | Notes |
|---|---|---|---|
| US fiber take-rate (one provider in market) | **~46–47%** | [FACT] | Averaged ~46.5% in 2024 |
| Take-rate, two fiber providers in market | total adoption **~61%** | [FACT] | But split between them |
| Early-launch take-rate (altnets/small ILECs) | low- to mid-teens | [FACT] | Ramps over years |
| Residential monthly ARPU | **~$50–$150** | [FACT] | Enterprise $200–$2,000+/mo; wholesale $15–$40/sub/mo |
| Target IRR | **~10–15%** | [ESTIMATE] | Industry working range |
| Payback period | **often 10+ years** | [ESTIMATE] | Urban/suburban high-single-digits; rural far longer |
| Retail return at 40–50% penetration | **~18–25%/yr** | [ESTIMATE] | The reward for filling a build |
| Wholesale-only return | **~12–18%/yr** | [ESTIMATE] | Steadier, lower |
| Third overbuilder into 2-incumbent market | **~4% unlevered pre-tax ROI** | [FACT] | Single primary source, flag |
| EY viability yield hurdle | **12%+ yield** (gross margin / build capex) | [FACT] | EY's TAM screen for new fiber |

[FACT for take-rate, ARPU, and the overbuild/yield figures; ESTIMATE for the IRR/payback/return ranges, which are operator- and assumption-dependent.]

### The take-rate trap

Because take-rate averages **~46–47%**, **more than half of homes passed generate no revenue at all**. A build is underwritten on the expectation of filling, and when penetration drifts below **~35%** a large share of builds cannot clear their cost of capital. The 2024–26 market is repricing this: capital that once accepted "build now, fill later, refinance along the way" now demands unit-level discipline early. Roughly **16% of US locations sit in overbuild zones** (two or three networks chasing one home), and the **third entrant earns only ~4% unlevered pre-tax ROI** [single primary source, flag for the lead]. The lesson for the COMMS track: even the best terrestrial technology has **fragile economics when fought house-by-house in already-served territory**, exactly the territory a space alternative would be competing for if it targeted served homes.

---

## 5. Where Ground Broadband Is Uneconomic, The Density Cliff

Per-passing cost is a function of density and remoteness. There is a smooth gradient from cheap dense urban to a vertical cliff in the remote tail.

| Setting | Cost per home passed | Business case |
|---|---|---|
| Dense urban | **~$700–$800** | Strong (if take-rate holds) |
| Suburban | **~$1,000–$1,500** | Workable |
| Rural | **~$3,000–$6,000** | Needs subsidy (BEAD/RDOF) |
| Remote / extreme high-cost tail | **up to ~$200,000–$230,000** | No private case at all |

[FACT for the urban–rural gradient (multi-source); the **~$200,000–$230,000 extreme-rural** figure rests on a single primary report and is flagged.]

The driver is explicit: cost scales with **distance to the nearest fiber divided by the number of homes served**. Low density means high per-location cost spread over few customers and low aggregate revenue, so the payback never closes without subsidy. This is why public money exists: BEAD's framework requires each state to set an **"extreme high-cost per location threshold"** above which cheaper-than-fiber alternatives are allowed, precisely because some locations cost more to reach with fiber than any model can justify.

### How big is the uneconomic tail?

| Metric | Value | Tag | Vintage |
|---|---|---|---|
| US broadband-serviceable locations (FCC map) | **~113 million** | [FACT] | ~2023 baseline |
| Unserved + underserved (initial estimate) | **~13.8M** (~7.8M unserved + ~6M underserved) | [FACT] | 2023 |
| BEAD-eligible locations remaining | **~4.2 million** | [FACT] | mid-2025 |
| Decline in eligible locations since Dec 2022 | **~65%** (~7.7M fewer) | [FACT] | through 2025 |
| US "broadband deserts" (no/limited terrestrial option) | **~6% of households** | [FACT] | of which half no terrestrial broadband, half DSL-only |
| Locations likely never to get fiber | **~2–3 million households** | [ESTIMATE] | prohibitive per-home cost |

[FACT for the location counts (multi-source across NTIA/FCC-map coverage and broadband trackers); the "~2–3M never-fiber" is an analyst estimate.]

The tail is shrinking as subsidy and private builds chip away at it, but a residual core of **~1–3 million locations** is widely expected to remain economically unreachable by fiber even after BEAD. That residual is the natural home of a non-terrestrial solution.

---

## 6. The Founder's Question, Does a Space Alternative Add Incremental Value?

The founder asks: where fiber or cable already exists, does a space alternative add value, or is the value only in unserved, underserved, and remote areas. The economics in Sections 1–5 answer this cleanly, in two parts.

### A. In already-served territory: little incremental value

Where a home is already passed by fiber or upgraded cable, a space alternative faces three walls at once:

1. **Incumbent defend-cost is tiny.** A cable operator keeps a passed home competitive for **~$100–$300** (Section 2); a fiber operator's passing is already sunk. The incumbent's marginal cost to hold the customer is far below any new entrant's cost to win it.
2. **Quality gap.** Fiber delivers **300 Mbps–1 Gbps at ~5–14 ms latency**; cable D4.0 is multi-Gig; LEO satellite trades higher latency and shared capacity for ubiquity. In a head-to-head where both exist, the wireline product wins on price-per-quality.
3. **Overbuild economics are already brutal for terrestrial entrants.** A third terrestrial overbuilder earns **~4% ROI** (Section 4). A space entrant fighting for the same served household inherits the same unfavorable demand split with worse per-quality positioning.

So in served areas the incremental value of a space alternative is **low**, it is a price-taker against an incumbent who can defend cheaply.

### B. In unserved / underserved / remote territory: this is where the value is

The exact same cost structure that makes space uncompetitive downtown makes it compelling in the tail:

- Per-passing cost runs from **$3,000–$6,000 (rural)** up to **~$200,000+ (extreme remote)**, against ARPU of only **$50–$150/month**, the terrestrial payback **never closes** without subsidy.
- A residual **~1–3 million US locations** are expected to remain unreachable by fiber even post-BEAD; **~6% of households are broadband deserts** today.
- A space service turns the rural "special construction" problem (a one-off five- or six-figure fiber extension) into a **standardized consumer purchase**, no per-home civil works at all. That is precisely why LEO adoption is already concentrated in rural and suburban-fringe geographies where FTTP and cable are economically impractical, and why regulators treat LEO as the immediate answer for remote areas.

### Bottom line for the COMMS base

The incremental value of a space alternative for fixed broadband is **concentrated in the unserved/underserved/remote tail, not in served markets**. The crossover is essentially where terrestrial cost-per-passing exceeds what subsidy will cover, single-digit-percent of US households by count, but **millions of absolute locations**, plus the much larger global rural population outside dense markets. Served-market overbuild is a losing game for any new entrant, space included; the remote tail is the structurally defensible zone. (Whether the space *supply* economics close is a separate question handled by the space-side workstreams, not this doc.)

---

## 7. Europe and Other Major Markets (Brief), plus China Aside

Per-home-passed economics rhyme with the US: dense-urban cheap, suburban/rural expensive, with overbuild risk where incumbents and altnets both build.

| Market | Cost per home passed | Tag | Notes |
|---|---|---|---|
| Spain, urban | **€200–€250** | [FACT] | Among the cheapest in Europe (mature, dense, aerial-friendly) |
| UK (Openreach commercial) | **< £300/premises** | [FACT] | Openreach investing up to £15bn to reach 25M premises by end-2026 |
| Germany, suburban | **€1,000–€1,500+** | [FACT] | Higher labor/permitting; Deutsche Telekom + altnets targeting ~30M passed (~70%) |
| Europe general | overbuild risk where coverage plans sum to **>100%** | [FACT] | Germany and UK flagged as highest overbuild risk |

European take-up and overbuild dynamics mirror the US: ARPU pressure where two fiber networks (plus upgraded cable) chase the same homes. Spain's low per-home cost reflects density and a permissive build environment; Germany's high cost reflects the opposite. [FACT, directional, fewer independent cross-checks than the US figures, so treat as indicative.]

> **China aside (excluded from the main analysis):** China is not part of this base. For completeness only: China built FTTH at very low per-home cost at massive state-directed scale, which is not representative of the US/European commercial economics this doc models, and its market is effectively closed to a Western space operator. It is noted here and excluded from all comparisons above.

---

## Sources

*Fiber deployment cost (US)*
- [Fiber Broadband Association / Cartesian, 2025 Fiber Deployment Cost Annual Report (PDF)](https://fiberbroadband.org/wp-content/uploads/2026/01/FBA_Cartesian_Fiber-Deployment-Cost-Annual-Report_2025.pdf)
- [Cartesian, Fiber Deployment Cost Annual Report 2025](https://www.cartesian.com/fiber-deployment-cost-annual-report-2025/)
- [Broadband Communities, US fiber coverage hits 60% as deployment costs creep higher](https://bbcmag.com/us-fiber-coverage-hits-60-as-deployment-costs-creep-higher/)
- [Fierce Network, Cartesian/FBA: underground fiber costs 2x more than aerial](https://www.fierce-network.com/broadband/underground-fiber-drives-deployment-costs)
- [Arcadian Fiber, Fiber Broadband Expansion Costs 2025](https://arcadianfiber.com/articles/fiber-broadband-expansion-costs-2025-2)
- [DGTL Infra, Fiber Optic Network Construction: Process and Build Costs](https://dgtlinfra.com/fiber-optic-network-construction-process-costs/)
- [EY, How US FTTH providers can navigate an evolving market](https://www.ey.com/en_us/insights/telecommunications/how-us-ftth-providers-can-navigate-an-evolving-market)
- [CSI Magazine, US fibre deployment hits record pace as market nears 100M homes](https://csimagazine.com/csi/US-fibre-deployment.php)

*Cable / HFC / DOCSIS upgrade cost*
- [Light Reading, DOCSIS 4.0 upgrades could reach $300 per home passed](https://www.lightreading.com/cable-technology/docsis-4-0-network-upgrades-could-reach-300-per-home-passed)
- [Light Reading, Analysts peg DOCSIS 4.0 upgrade costs at $180 per home passed](https://www.lightreading.com/cable-tech/analysts-peg-docsis-40-network-upgrade-costs-at-$180-per-home-passed/d/d-id/780980)
- [Light Reading, Cable One pins DOCSIS 4.0 upgrades at $200 per household](https://www.lightreading.com/cable-technology/cable-one-pins-docsis-4-0-network-upgrades-at-200-per-household)
- [Fierce Network, Comcast cites $200 cost per passing for mid-split, DOCSIS 4.0](https://www.fierce-network.com/telecom/comcast-cites-200-cost-passing-mid-split-docsis-40-upgrades)
- [Fierce Network, The Economics of Cable Broadband Upgrades: DOCSIS 4.0 vs FTTH](https://www.fierce-network.com/sponsored/economics-cable-broadband-upgrades-choosing-between-docsis-40-and-ftth)

*Fixed wireless access (FWA)*
- [GSMA, Fixed Wireless Access: Economic Potential and Best Practices](https://www.gsma.com/solutions-and-impact/technologies/networks/5g/fixed-wireless-access-economic-potential-and-best-practices/)
- [Inside Towers, The Great FWA vs FTTH Debate](https://insidetowers.com/the-great-fwa-vs-ftth-debate/)
- [TecknExus, 5G FWA vs Fiber: T-Mobile, Verizon, AT&T](https://tecknexus.com/5g-fwa-vs-fiber-t-mobile-verizon-att/)
- [Dell'Oro Group, FWA equipment spend to exceed $48B over five years](https://www.delloro.com/news/fixed-wireless-access-equipment-spend-to-exceed-48-b-over-the-next-five-years/)
- [Light Reading, 2025 in review: FWA's fangs stay sharp](https://www.lightreading.com/fixed-wireless-access/2025-in-review-fwa-s-fangs-stay-sharp)

*Unit economics, take-rate, ARPU, overbuild*
- [Phoenix Strategy Group, Unit Economics of Fiber Optic Investments](https://www.phoenixstrategy.group/blog/unit-economics-of-fiber-optic-investments)
- [PwC, US consumer fiber: shakeout or step change? 2026 outlook](https://www.pwc.com/us/en/industries/tmt/library/consumer-fiber-shakeout-or-step-change.html)
- [RCR Wireless, Bleeding subs, flat ARPU: the MDU answer US broadband keeps circling](https://www.rcrwireless.com/20260611/analyst-angle/mdu-us-broadband-maravedis)
- [Telecompetitor, Analyst: Fiber Overexuberance? A New Bubble May Be Forming](https://www.telecompetitor.com/analyst-fiber-overexuberance-a-new-bubble-may-be-forming/)
- [TheWriter.id, FTTH Overbuild Strategy and the Five Moves That Win](https://thewriter.id/ftth-overbuild-strategy/)

*Rural / uneconomic tail and unserved counts*
- [Fierce Network, The cost of running fiber in rural America: $230,000 per passing](https://www.fierce-network.com/broadband/cost-running-fiber-rural-america-200000-passing)
- [Fierce Network, Each state must set an extreme high-cost threshold for BEAD money](https://www.fierce-network.com/broadband/each-state-must-set-extreme-high-cost-threshold-bead-money)
- [Benton Institute, Setting the Extremely High Cost Per Location Threshold for BEAD](https://www.benton.org/blog/setting-extremely-high-cost-location-threshold-bead)
- [Broadband Expanded, BEAD eligible locations drop 65% since Dec 2022](https://broadbandexpanded.com/posts/botblocations)
- [StateScoop, The number of eligible BEAD locations dropped again](https://statescoop.com/states-resubmission-bead-proposals-eligible-locations-drops-2025/)
- [Telecompetitor, Eligibility of 1.4M locations for BEAD funding at stake](https://www.telecompetitor.com/eligibility-of-1-4m-locations-for-bead-funding-at-stake-as-ntia-weighs-a-critical-decision/)

*Space alternative (incremental-value context only)*
- [CRS / Congress.gov, Low Earth Orbit Satellites: Potential to Address the Broadband Digital Divide](https://www.congress.gov/crs-product/R46896)
- [Via Satellite, Examining the Size of the US Residential Broadband Opportunity for LEO Satcom (Mar 2026)](https://interactive.satellitetoday.com/via/march-2026/examining-the-size-of-the-us-residential-broadband-opportunity-for-leo-satcom)
- [FTI Consulting, LEO Satellite Has Landed in the Broadband Market](https://www.fticonsulting.com/insights/articles/leo-satellite-landed-broadband-market)

*Europe*
- [ING Think, Fibre rollout: the hardest part is yet to come](https://think.ing.com/articles/fibre-rollout-the-hardest-part-is-yet-to-come/)
- [Point Topic, FTTP adoption rates and market value in Europe, 2024 update](https://www.point-topic.com/post/fttp-adoption-europe-2024)
- [ISPreview, Openreach FTTP build rate and investment](https://www.ispreview.co.uk/index.php/2024/01/openreach-to-hit-quarterly-uk-fttp-broadband-build-rate-of-1m-premises.html)

---

## Confidence

**Overall: medium-high.**

- **High confidence (multi-source, converging):** fiber per-foot build cost (~$18 underground / ~$8 aerial, 2025) and 64–72% labor share; cable D4.0 upgrade at ~$100–$300/home passed (four independent operator/analyst figures); FWA at ~$300–$800/subscriber vs fiber's $800–$6,000; US fiber take-rate ~46–47%; BEAD-eligible location counts and the ~65% decline; ~6% broadband-desert share.
- **Medium confidence (range solid, point values vary):** fiber cost per home passed (the $700–$1,500 urban / $3,000–$6,000 rural *ranges* are well supported; any single point value is operator- and density-specific); per-home-connected $500–$700; ARPU $50–$150.
- **Lower confidence / single primary source (flagged for the lead):** the **~$200,000–$230,000 extreme-rural per-passing** figure (single report); the **~4% ROI for a third overbuilder** (single primary analyst); the GSMA **~74% cost-per-bit** FWA advantage (single primary source); the **~2–3M never-fiber** estimate. Europe figures are directional with fewer independent cross-checks. IRR (~10–15%) and payback (10+ years) are industry working ranges, not audited constants.

---

## Open Questions

1. **Per-home-connected vs per-home-passed precision.** The connect/drop cost ($500–$700) is less consistently reported than passing cost. A cleaner split of "passing capex" vs "success-based connect capex" would tighten any payback model that the COMMS track builds.
2. **Lifetime cost, not just build cost, for FWA.** FWA wins on capex but its opex (tower rental, power, spectrum) can exceed fiber's. A full TCO-per-subscriber comparison across fiber/cable/FWA over a 10-year life would sharpen the technology ladder in Section 3.
3. **Exact crossover density where terrestrial fails.** Sections 5–6 establish that the cliff exists; the precise homes-per-mile (or $/passing) threshold where no subsidy closes the case is the number that sizes the space-addressable tail. Worth pinning with a density-cost model.
4. **Global remote tail beyond the US.** This doc is US-primary with a European sketch. The far larger addressable population is rural/remote outside dense markets (Latin America, Africa, maritime, aviation). Sizing that is a separate research task for the COMMS track and is where a space service's TAM would actually live.
5. **Subsidy dependence.** BEAD/RDOF materially change which rural homes are "economic." If subsidy programs shrink or shift, the terrestrial-uneconomic tail grows and the space-addressable set grows with it. The base case here should be stress-tested against a low-subsidy scenario.
6. **ARPU durability under competition.** The $50–$150 ARPU assumes today's pricing; overbuild and FWA price pressure could compress it, which would lengthen every payback and push more marginal terrestrial builds into the uneconomic zone.

---

## Claims Table

| COMM- ID | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-001 | Fiber cost per home passed, urban/suburban (US) | $700–$1,500 | [FACT] | Arcadian Fiber; DGTL Infra; multi-source |
| COMM-002 | Fiber cost per home passed, rural (US) | $3,000–$6,000+ | [FACT] | Arcadian Fiber; Inside Towers; multi-source |
| COMM-003 | Fiber "typical" cost per home passed | ~$1,000–$1,250 (≈$60–80k/route mile) | [FACT] | DGTL Infra; Arcadian Fiber |
| COMM-004 | Fiber cost per home connected (drop + install) | ~$500–$700 | [FACT] | Light Reading (D4.0-vs-FTTP context); cross-ref |
| COMM-005 | Fiber underground build cost, 2025 median | ~$18.00/ft (+3% YoY) | [FACT] | Cartesian/FBA 2025; BBC Mag |
| COMM-006 | Fiber aerial build cost, 2025 median | ~$8.00/ft (+14% YoY) | [FACT] | Cartesian/FBA 2025; BBC Mag |
| COMM-007 | Labor share of fiber deployment cost | 72% underground / 64% aerial | [FACT] | Cartesian/FBA 2025; BBC Mag |
| COMM-008 | Cable DOCSIS 4.0 / mid-split upgrade cost per home passed | ~$100–$300 | [FACT] | Charter; Comcast; Cable One; Credit Suisse |
| COMM-009 | Cable full-transition cost incl. new modem | ~$250–$400/home passed | [ESTIMATE] | Light Reading |
| COMM-010 | FWA capex per subscriber (radio share + CPE) | ~$300–$800 | [FACT] | GSMA; Inside Towers |
| COMM-011 | FWA cost-per-bit advantage vs wireline | up to ~74% lower | [FACT] | GSMA (single source, verify) |
| COMM-012 | US fiber take-rate (single provider in market) | ~46–47% | [FACT] | EY; PwC; RCR Wireless |
| COMM-013 | Residential broadband monthly ARPU | ~$50–$150 | [FACT] | Phoenix Strategy Group; Starlink/fiber price comps |
| COMM-014 | Fiber target IRR / payback | ~10–15% IRR / 10+ yr payback | [ESTIMATE] | Phoenix Strategy Group |
| COMM-015 | Third overbuilder into 2-incumbent market ROI | ~4% unlevered pre-tax | [FACT] | EY (single primary source, verify) |
| COMM-016 | Share of US locations in overbuild zones | ~16% | [FACT] | RCR Wireless / Maravedis |
| COMM-017 | Extreme-rural fiber cost per passing | up to ~$200,000–$230,000 | [FACT] | Fierce Network (single primary source, verify) |
| COMM-018 | US BEAD-eligible locations remaining | ~4.2 million (mid-2025) | [FACT] | Broadband Expanded; StateScoop |
| COMM-019 | US unserved + underserved (initial 2023 estimate) | ~13.8M (~7.8M + ~6M) | [FACT] | Vantage Point via search; FCC map context |
| COMM-020 | Decline in BEAD-eligible locations since Dec 2022 | ~65% (~7.7M fewer) | [FACT] | Broadband Expanded; StateScoop |
| COMM-021 | US "broadband desert" household share | ~6% (half no terrestrial, half DSL-only) | [FACT] | Via Satellite; CRS |
| COMM-022 | Locations likely never to receive fiber | ~2–3 million households | [ESTIMATE] | Search synthesis (analyst estimate) |
| COMM-023 | US fiber homes passed / coverage | ~88M (2024) → ~60% / ~100M homes (2025) | [FACT] | EY; CSI Magazine; Cartesian/FBA |
| COMM-024 | Fiber per-home passed, Spain urban | €200–€250 | [FACT] | ING Think; Point Topic |
| COMM-025 | Fiber per-home passed, UK Openreach commercial | < £300/premises | [FACT] | ING Think; ISPreview |
| COMM-026 | Fiber per-home passed, Germany suburban | €1,000–€1,500+ | [FACT] | ING Think |
| COMM-027 | Underground vs aerial fiber cost multiple | underground ~2x aerial | [FACT] | Cartesian/FBA 2025; Fierce Network |
