# US Wireless / Cellular Market: Size, Carrier Financials, and the Wholesale Market

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:** [`research/laser_comms/rf_limited_service.md`](../laser_comms/rf_limited_service.md) (the AST SpaceMobile direct-to-device precedent and the Grain Management spectrum-leasing model). That doc treats spectrum access for a Rocket Lab RF sliver; this doc sizes the ground-side US cellular market those direct-to-cell deals plug into. The space-adjacent direct-to-cell players are covered here only as market context, not re-derived.

---

## Summary / Verdict

The US wireless service market is large, mature, and concentrated. Total industry service revenue is roughly **$326 billion in 2025** [ESTIMATE, single major source: IBISWorld], growing low single digits (about 1.8% in 2025). Three carriers (Verizon, AT&T, T-Mobile) hold the overwhelming majority of subscribers and revenue. They are cash-rich, slow-growth, capital-intensive businesses: combined they carry roughly **$575 billion of market cap** and post tens of billions in annual profit, but top-line growth is in the 2 to 4 percent range, not double digits.

The wholesale / MVNO layer sits underneath the three networks. Reputable estimates of the **US MVNO market cluster around $13 to $15 billion in 2025** [ESTIMATE, methodology-dependent], with much larger outlier estimates (~$44 billion) that appear to use a broader scope. The single most important wholesale story is the **cable MVNOs**: Comcast (Xfinity Mobile) and Charter (Spectrum Mobile) buy capacity off Verizon's network and together run well over **20 million mobile lines** [FACT], making them the largest and fastest-growing wholesale buyers in the country.

The space-adjacent angle is **direct-to-cell**. Starlink Direct to Cell (with T-Mobile in the US) reports **16 million unique users** as of March 2026 [FACT], and AST SpaceMobile (with AT&T and Verizon in the US) has agreements covering 45+ operators and **~2.8 billion subscribers** globally [FACT] while still pre-scale on revenue (~$71 million in 2025). This confirms the pattern flagged in `rf_limited_service.md`: the US carriers are not building their own satellites, they are **renting** orbital capacity from space operators to fill coverage gaps. That is the structural opening for a space-based entrant.

**Confidence: medium-high** on carrier financials (drawn from 2025 SEC filings and earnings releases, cross-checked across two or more sources), **medium** on total-market and MVNO sizing (private research-firm estimates that vary by methodology), **medium** on exact stock-price levels (timestamps in secondary coverage are mixed; market-cap figures dated June 2026 are the firmer anchor).

---

## 1. Total US Wireless Market Size

| Metric | Value | Year | Status | Note |
|---|---|---|---|---|
| US wireless carrier service revenue | ~$326.4 billion | 2025 | [ESTIMATE] | IBISWorld; "single major source" |
| Projected US wireless service revenue | ~$336.1 billion | 2026 | [PROJECTION] | IBISWorld, +1.7% |
| US total telecom services (wireless + wireline) | ~$451.7 billion | 2025 | [ESTIMATE] | Mordor Intelligence |
| Total US wireless connections | 579 million | 2024 survey | [FACT] | CTIA; ~1.7 connections per person |
| 5G connections | 259+ million | 2024 survey | [FACT] | CTIA; nearly half of all connections |
| Annual US mobile data used | 132 trillion MB | 2024 | [FACT] | CTIA; ~35% YoY growth, third straight year |
| Top 4 carriers' share of wireless revenue | ~65% | 2025 | [ESTIMATE] | reported in market coverage |

**Reading the numbers.** The market is enormous but barely growing: roughly 2 percent a year on the top line. Connections (579 million) far exceed people because the count includes phones, tablets, connected cars, IoT modules, and fixed-wireless home units, not just human phone subscribers. Growth in the industry now comes from price increases, fixed wireless access (5G home broadband), and converged bundles, not from signing up new phone users in an already-saturated market.

**Sizing caveat.** The headline ~$326 billion is an IBISWorld figure and is flagged **single source** at that precise value. It is broadly consistent with a bottom-up cross-check: the three majors alone book on the order of $200 billion in wireless **service** revenue (Verizon's wireless service revenue runs ~$80 billion annualized, AT&T's Mobility service revenue is $65.4 billion, T-Mobile's total service revenue is $71.3 billion), and adding the rest of the market (US Cellular legacy, regional carriers, the MVNO layer, IoT/connected devices) lands in the same neighborhood. The lead should treat $326 billion as a reasonable central estimate, not a hard fact.

---

## 2. The Big Three Carriers: Financial Benchmarks

All three are publicly traded US carriers (Verizon: NYSE VZ; AT&T: NYSE T; T-Mobile US: NASDAQ TMUS). Figures below are full-year 2025 unless noted. Market caps are as of mid-June 2026.

### 2.1 Side-by-side benchmark

| Metric | Verizon | AT&T | T-Mobile US | Status |
|---|---|---|---|---|
| Market cap (Jun 2026) | ~$191-201 billion | ~$156-160 billion | ~$216 billion | [FACT] |
| Total revenue (FY2025) | $138.2 billion | $125.6 billion | $88.3 billion | [FACT] |
| Net income (FY2025) | $17.2-17.6 billion | ~$22 billion | $11.0 billion | [FACT] |
| Net margin (FY2025) | ~13% | ~18% | ~12% | [ESTIMATE] derived |
| Total service revenue (FY2025) | ~$80 billion wireless service | $65.4 billion Mobility service | $71.3 billion total service | [FACT] |
| Stock 1-yr direction (to ~mid-2026) | up (~+15%) | roughly flat to modest | down (~-20%) | [FACT] direction; level approx. |
| Postpaid phone ARPU | ~$50 (core); ARPA $147.36 (Q4) | $56.57 | $50.37 | [FACT] |
| Wireless subscribers (scale) | ~146 million retail connections | 74.2 million postpaid phone | 142.4 million total customers | [FACT] |

Notes on the subscriber row: the three carriers report on different bases, so the numbers are not apples-to-apples. Verizon's ~146 million is total wireless retail connections (consumer + business, including some fixed wireless); AT&T's 74.2 million is postpaid **phone** subscribers specifically (its total connection count including connected devices and prepaid is larger); T-Mobile's 142.4 million is total customers across all categories (postpaid phone customers are 85.6 million). ARPU vs ARPA also differ: ARPU is per phone line, ARPA is per account (an account holds multiple lines), which is why the ARPA figures (~$147) are roughly three times the ARPU figures (~$50).

### 2.2 Verizon (VZ)

| Metric | Value | Status | Source basis |
|---|---|---|---|
| Market cap (Jun 2026) | ~$191-201 billion | [FACT] | companiesmarketcap / stockanalysis |
| Total operating revenue FY2025 | $138.191 billion | [FACT] | 2025 results / 10-K |
| Net income FY2025 (consolidated) | $17.2-17.6 billion | [FACT] | 2025 results |
| Free cash flow FY2025 | $20.1 billion | [FACT] | 2025 results |
| Wireless retail connections (YE2025) | ~146 million (Consumer ~116M + Business ~31M) | [FACT] | 2025 results |
| Postpaid phone net adds Q4 2025 | 616,000 (best quarter since 2019) | [FACT] | 2025 results |
| Retail postpaid ARPA Q4 2025 | $147.36 | [FACT] | 2025 results |
| Core prepaid ARPU Q4 2025 | $32.90 | [FACT] | 2025 results |
| Stock (approx, mid-2026) | ~$50 area; up ~15% over prior year | [FACT] direction | secondary coverage |

Verizon is the revenue leader and runs the network the major cable MVNOs ride. It closed the Frontier acquisition in 2025, pushing fixed broadband (fiber + fixed wireless) past 16.3 million connections.

### 2.3 AT&T (T)

| Metric | Value | Status | Source basis |
|---|---|---|---|
| Market cap (Jun 2026) | ~$156-160 billion (down ~20% YoY) | [FACT] | macrotrends / stockanalysis |
| Total operating revenue FY2025 | $125.6 billion (+2.7% YoY) | [FACT] | 4Q/FY2025 release |
| Net income FY2025 | ~$21.9 to $22.0 billion (nearly doubled YoY) | [FACT] | FY2025 release; stocktitan |
| Diluted EPS FY2025 | ~$3.04 to $3.05 | [FACT] | FY2025 release |
| Mobility service revenue FY2025 | $65.4 billion (+3.5% YoY) | [FACT] | FY2025 release |
| Postpaid phone subscribers (YE2025) | 74.2 million (+1.5M net adds in 2025) | [FACT] | FY2025 release |
| Postpaid phone ARPU FY2025 | $56.57 (vs $56.72 in 2024) | [FACT] | FY2025 release / Statista |
| Stock (approx, mid-2026) | high-$20s area; ~+5% over prior 52 weeks per late-2025 coverage | [FACT] direction | secondary coverage |

**Net-income caveat.** AT&T's FY2025 net income (~$22 billion) is reported as nearly double FY2024 (~$10.9 billion). That jump is a year-over-year base effect (the prior year carried large non-cash impairment/charges), not a doubling of the underlying wireless business. Quarterly 2025 net income ran roughly $3.9 to $4.9 billion. The ~18% net margin in the side-by-side is therefore flattered by base effects and should be read as a 2025 point figure, not a structural margin.

### 2.4 T-Mobile US (TMUS)

| Metric | Value | Status | Source basis |
|---|---|---|---|
| Market cap (Jun 2026) | ~$216 billion | [FACT] | macrotrends / companiesmarketcap |
| Total revenue FY2025 | $88.309 billion | [FACT] | Q4/FY2025 8-K |
| Total service revenue FY2025 | $71.306 billion (+8% YoY) | [FACT] | Q4/FY2025 8-K |
| Postpaid service revenue FY2025 | $57.932 billion | [FACT] | Q4/FY2025 8-K |
| Net income FY2025 | $10.992 billion | [FACT] | Q4/FY2025 8-K |
| Diluted EPS FY2025 | $9.72 | [FACT] | FY2025 coverage |
| Total customers (YE2025) | 142.388 million | [FACT] | Q4/FY2025 8-K |
| Postpaid phone customers (YE2025) | 85.594 million | [FACT] | Q4/FY2025 8-K |
| Total net adds FY2025 | 8.0 million | [FACT] | Q4/FY2025 8-K |
| Postpaid phone ARPU FY2025 | $50.37 | [FACT] | Q4/FY2025 8-K |
| Postpaid ARPA FY2025 | $148.97 | [FACT] | Q4/FY2025 8-K |
| Stock (approx, mid-2026) | down ~20% over prior year ("valuation compression") | [FACT] direction | secondary coverage |

T-Mobile is the highest market cap of the three despite the smallest revenue, reflecting its strongest subscriber growth and margin trajectory. Its FY2025 results were boosted by the UScellular, Metronet, and Lumos acquisitions. The stock fell over the trailing year on valuation compression as wireless growth normalized, not on a deterioration in operations.

---

## 3. The Wholesale Cellular / MVNO Market

An MVNO (Mobile Virtual Network Operator) sells mobile service to end users but does not own a radio network; it buys wholesale capacity from one of the three facilities-based carriers and resells it under its own brand. This is the layer most relevant to a space entrant, because **a satellite operator that wants to reach phones does so through a carrier wholesale / hosting arrangement, not by becoming a retail carrier** (the AST/Verizon and Starlink/T-Mobile deals are structurally wholesale, see `rf_limited_service.md` Path C).

### 3.1 Market size

| Source | US MVNO market size 2025 | Forecast | Status |
|---|---|---|---|
| Mordor Intelligence | ~$14.83 billion | ~$20.84 billion by 2030 (7.04% CAGR) | [ESTIMATE] |
| Ken Research / SphericalInsights (USA) | ~$13 billion | growth to 2030 | [ESTIMATE] |
| Verified Market Research (US) | ~$43.82 billion | ~$64.69 billion by 2031 (6.71% CAGR) | [ESTIMATE] outlier |

**The estimates diverge by roughly 3x.** Two firms land near $13 to $15 billion; one lands near $44 billion. The gap is a scope/methodology artifact (the high figure appears to fold in broader connectivity revenue streams such as IoT/M2M wholesale and possibly the full retail value of cable mobile). For planning, the **$13 to $15 billion** cluster is the more defensible "MVNO service revenue" figure; the ~$44 billion number should be flagged and not used without understanding its inclusions. Growth across all estimates is mid-single-digit (~6 to 7% CAGR), faster than the ~2% facilities-based market.

### 3.2 Who buys wholesale, and the economics

The buyers of wholesale mobile capacity fall into a few groups:

- **Cable operators** (the dominant buyers): Comcast Xfinity Mobile, Charter Spectrum Mobile. Covered in Section 4.
- **Value / discount brands**: a long tail of MVNOs targeting cost-sensitive consumers (the carriers also run their own flanker prepaid brands, e.g. AT&T's Cricket, T-Mobile's Metro).
- **IoT / M2M and enterprise connectivity resellers**: businesses embedding cellular into devices and fleets, buying connectivity wholesale rather than retail.
- **Niche / affinity MVNOs**: brand-led plays (retail, media, ethnic-market, etc.).

**Economics.** The MVNO buys capacity at a wholesale rate per gigabyte or per line, sets its own retail price, and keeps the spread. The carrier monetizes otherwise-spare network capacity at high incremental margin and offloads retail acquisition cost to the MVNO. The strategic tension is that a successful MVNO (like the cable operators) eventually drives enough traffic to threaten the host carrier's own retail base, which is exactly why wholesale contracts get renegotiated (see Section 4) and why hosts cap or price-tier heavy users. For a space entrant, the relevant lesson is that the carriers are **comfortable wholesaling network access to a third party** when it monetizes idle capacity, the same logic that makes them willing to host a satellite direct-to-cell layer.

---

## 4. Cable MVNOs: Comcast and Charter on Verizon

The cable MVNOs are the standout wholesale story in the US and the clearest proof that a non-carrier can build a large mobile base on rented capacity.

| Operator | Brand | Host network | Mobile lines (2025) | Status |
|---|---|---|---|---|
| Charter Communications | Spectrum Mobile | Verizon (consumer) | ~11.01 million residential lines (YE Q3 2025) | [FACT] |
| Comcast | Xfinity Mobile | Verizon (consumer) | several million lines (added 323,000 in a recent quarter) | [FACT] adds; total approximate |
| Combined cable mobile | | Verizon | well over 20 million lines | [FACT] |

Key dynamics:

- **Both ride Verizon's network** for consumer service under long-standing MVNO agreements. In late January 2026 they signed an updated, "modernized" MVNO agreement with Verizon at improved wholesale rates [FACT].
- **They are diversifying their host base.** Comcast and Charter struck a **new MVNO deal with T-Mobile for their business customers**, with wholesale connectivity starting in 2026 [FACT]. Consumer service stays on Verizon; the T-Mobile deal is "solely for wholesale mobile connectivity to business customers."
- **They are building offload to cut wholesale cost.** The cable operators are deploying their own CBRS/licensed spectrum and Wi-Fi to carry traffic on-net and reduce what they pay Verizon, the classic MVNO maturation path of "build your way out of dependency."
- **Growth is strong.** Charter added a record 414,000 wireless lines in Q3 2025 and 514,000 in a subsequent quarter; Comcast added 323,000 in a recent quarter [FACT]. Cable mobile is one of the fastest-growing segments of US wireless even as the overall market is flat.

**Why this matters for the communications thesis.** The cable MVNOs demonstrate that (a) Verizon and T-Mobile will wholesale large volumes of capacity to a determined third party, and (b) that third party can accumulate tens of millions of lines. A space operator offering a complementary coverage layer (rural, maritime, dead zones) is a less threatening wholesale partner than a cable company poaching core urban subscribers, which is precisely why the carriers have been willing to sign direct-to-cell deals (Section 5).

---

## 5. Direct-to-Cell: The Space-Adjacent Layer

Direct-to-cell (also "direct-to-device," D2D) lets an ordinary, unmodified smartphone connect to a satellite when no terrestrial tower is in range. In the US this has resolved into a carrier-aligned duopoly of space partners. This section is context for the shared library; the spectrum-access mechanics are in `rf_limited_service.md`.

| Player | US carrier partner(s) | Model | 2025/26 scale | Status |
|---|---|---|---|---|
| Starlink Direct to Cell (SpaceX) | T-Mobile (US) | Carrier hosts; satellite fills gaps | 16M unique users, 10M monthly active (Mar 2026) | [FACT] |
| AST SpaceMobile | AT&T, Verizon (US) | Carrier wholesale/hosting; uses carrier spectrum | 45+ MNO agreements, ~2.8B subscribers covered; rev ~$70.9M (2025) | [FACT] |

Details:

- **US split.** AT&T and Verizon subscribers reach space connectivity through **AST SpaceMobile**; T-Mobile subscribers reach it through **Starlink** [FACT]. The carriers did not build satellites; they partnered.
- **Starlink Direct to Cell** is the scale leader by users (16 million unique, 10 million monthly active as of March 2026) and rides SpaceX's broader Starlink business (~$10.4 billion of SpaceX's ~$15 billion 2025 revenue) [FACT, revenue split is single-source/estimated for SpaceX which is private].
- **AST SpaceMobile** is the pure-play public comparable (NASDAQ ASTS), with a market cap around **$46 billion in mid-2026** [FACT], ~$3 billion cash, and 2025 revenue of only **~$70.9 million** (up from ~$4.4 million) [FACT], guiding to $150 to $200 million in 2026. It is a high-valuation, pre-scale-revenue company: the market is pricing the option, not current earnings.
- **Spectrum precedent (cross-ref).** As established in `rf_limited_service.md`, AST got FCC approval to use AT&T/Verizon spectrum, and Grain Management is positioned to lease D2D spectrum to satellite operators. This is the structural template a Rocket Lab RF sliver would follow.

**Net for the thesis.** The US carriers treat space as a **complementary coverage layer they rent**, not a business they own. The direct-to-cell market is real but early: large user counts (Starlink) but tiny revenue (AST) so far. That is both the opportunity (carriers are paying for orbital capacity) and the caution (the revenue per user from filling dead zones is currently very thin).

---

## China note (excluded from main analysis)

Per scope, China is excluded from the main analysis. For completeness only: China Mobile, China Telecom, and China Unicom dwarf the US carriers in subscriber count (China Mobile alone exceeds ~1 billion connections) and operate under a separate regulatory and spectrum regime. China's direct-to-cell efforts (e.g., via its own LEO constellations) are a parallel, state-aligned track not addressed here. No China figures are used in this doc's market sizing.

---

## Sources

- [IBISWorld, Wireless Telecommunications Carriers in the US (Market Size)](https://www.ibisworld.com/united-states/market-size/wireless-telecommunications-carriers/1267/)
- [Mordor Intelligence, United States Telecom Services Market](https://www.mordorintelligence.com/industry-reports/united-states-telecom-services-market)
- [Digitalsegment, The State of U.S. Wireless Telecom in 2026](https://www.digitalsegment.com/2026/02/10/the-state-of-u-s-wireless-telecom-in-2026/)
- [Statista, Largest US network operators market share 2025](https://www.statista.com/statistics/199359/market-share-of-wireless-carriers-in-the-us-by-subscriptions/)
- [Statista, US mobile operators wireless revenue](https://www.statista.com/statistics/199796/wireless-operating-revenues-of-us-telecommunication-providers/)
- [CTIA, 2025 Annual Survey Highlights](https://www.ctia.org/news/2025-annual-survey-highlights)
- [RCR Wireless, CTIA 2025 survey: cellular demand](https://www.rcrwireless.com/20250919/5g/cellular-demand-in-2025-ctia)
- [Verizon, Delivers on 2025 Financial Guidance (Q4/FY2025)](https://www.verizon.com/about/news/verizon-delivers-2025-financial-guidance-highest-quarterly-net-adds)
- [Verizon, 2025 Annual Report on Form 10-K](https://www.verizon.com/about/sites/default/files/2025-Annual-Report-on-Form-10k.pdf)
- [companiesmarketcap, Verizon market cap](https://companiesmarketcap.com/verizon/marketcap/)
- [stockanalysis, Verizon (VZ) market cap](https://stockanalysis.com/stocks/vz/market-cap/)
- [AT&T, Strong Fourth-Quarter and Full-Year 2025 Financial Performance](https://about.att.com/story/2026/4q-earnings-2025.html)
- [AT&T, 4Q 2025 Earnings Release (PDF)](https://investors.att.com/~/media/Files/A/ATT-IR-V2/financial-reports/quarterly-earnings/2025/4Q-2025/ATT_4Q25_Earnings_Release.pdf)
- [stocktitan, AT&T (T) financials](https://www.stocktitan.net/financials/T/)
- [macrotrends, AT&T market cap](https://www.macrotrends.net/stocks/charts/T/at-t/market-cap)
- [Statista, AT&T wireless ARPU 2018-2025](https://www.statista.com/statistics/489944/atandt-wireless-arpu/)
- [T-Mobile US, Q4/FY2025 8-K (SEC)](https://www.sec.gov/Archives/edgar/data/0001283699/000128369925000008/tmus12312024ex992.htm)
- [stocktitan, T-Mobile US FY2025 results 8-K](https://www.stocktitan.net/sec-filings/TMUS/8-k-t-mobile-us-inc-reports-material-event-e88bc51882d5.html)
- [macrotrends, T-Mobile US market cap](https://www.macrotrends.net/stocks/charts/TMUS/t-mobile-us/market-cap)
- [companiesmarketcap, T-Mobile US market cap](https://companiesmarketcap.com/t-mobile-us/marketcap/)
- [Motley Fool, VZ vs T long-term play (Dec 2025)](https://www.fool.com/investing/2025/12/21/verizon-vs-att-stock-whats-better-long-term-play/)
- [Inside Towers, Telco stocks moving at a different pace](https://insidetowers.com/telco-stocks-moving-at-a-different-pace/)
- [Mordor Intelligence, US MVNO Market](https://www.mordorintelligence.com/industry-reports/united-states-mobile-virtual-network-operator-mvno-market)
- [Verified Market Research, US MVNO Market](https://www.verifiedmarketresearch.com/product/us-mobile-virtual-network-operators-mvno-market/)
- [Ken Research, USA MVNO Market](https://www.kenresearch.com/industry-reports/usa-mobile-virtual-network-operator-market)
- [Light Reading, Modernized MVNO pacts with Verizon (Comcast/Charter)](https://www.lightreading.com/5g/-modernized-mvno-pacts-with-verizon-mean-better-rates-for-comcast-and-charter-entner)
- [Light Reading, How Charter and Comcast build out of Verizon dependency](https://www.lightreading.com/network-platforms/how-charter-and-comcast-are-building-their-way-out-of-verizon-dependency)
- [Fierce Network, T-Mobile, Charter and Comcast MVNO alliance](https://www.fierce-network.com/broadband/t-mobile-charter-comcast-join-forces-new-mvno-alliance)
- [Broadband Breakfast, Comcast, Charter ink business MVNO deal with T-Mobile](https://broadbandbreakfast.com/comcast-charter-ink-business-mvno-deal-with-t-mobile/)
- [AST SpaceMobile, FY2025 8-K (SEC)](https://www.sec.gov/Archives/edgar/data/0001780312/000149315225020005/ex99-1.htm)
- [stockanalysis, AST SpaceMobile (ASTS)](https://stockanalysis.com/stocks/asts/)
- [Trefis, AST SpaceMobile Starlink rival](https://www.trefis.com/stock/asts/articles/586130/ast-spacemobile-is-this-starlink-rival-stock-poised-to-soar-higher/2025-12-26)
- [NewSpaceTracker, Direct-to-Smartphone Satellites](https://newspacetracker.com/articles/direct-to-smartphone-satellites/)
- [Tesorb, AST SpaceMobile vs Starlink direct-to-cell](https://tesorb.com/ast-spacemobile-vs-starlink-direct-to-cell/)

---

## Confidence

- **Carrier financials (Section 2): medium-high.** Revenue, net income, ARPU, and subscriber figures come from FY2025 SEC 8-Ks and earnings releases, cross-checked against secondary aggregators. T-Mobile and Verizon numbers are firm. AT&T's net income is double-sourced (~$21.9 to $22.0 billion) but the year-over-year doubling is a base effect, flagged in-text.
- **Market caps: medium-high** for the values (dated June 2026, two aggregators), but they move daily.
- **Stock-price levels: medium.** Direction over the trailing year is well-attested (VZ up, AT&T modest, TMUS down ~20%), but exact price points in secondary coverage carried mixed timestamps; market cap is the firmer anchor.
- **Total market size (Section 1): medium.** The ~$326 billion headline is a single research firm (IBISWorld); cross-checked for plausibility against the bottom-up carrier sum but not independently confirmed at that exact value.
- **MVNO sizing (Section 3): medium.** Reputable estimates diverge ~3x by scope; the $13 to $15 billion cluster is used as central with the outlier flagged.
- **Direct-to-cell (Section 5): medium-high** on the deal structure and user/revenue figures; the SpaceX revenue split is single-source (SpaceX is private).

---

## Open Questions / Uncertainties

- **Exact total US wireless service revenue.** A second independent source at the ~$326 billion level (or a clean bottom-up build from carrier service-revenue lines plus the MVNO and IoT layers) would firm this up. The lead may already hold a competing figure in the shared SOURCE_INDEX.
- **MVNO scope reconciliation.** What does the ~$44 billion Verified Market Research figure include that the ~$14 billion Mordor figure does not? Resolving the scope difference would let the library cite one defensible MVNO number.
- **Comcast Xfinity Mobile exact line count.** Charter's residential mobile lines (~11 million) are well sourced; a precise Comcast total line count (vs just quarterly adds) should be pinned from Comcast's own filings.
- **Carrier wholesale pricing.** The actual per-GB / per-line wholesale rate the cable MVNOs pay Verizon is not public at a precise level; only "improved rates" after the 2026 renegotiation is reported. A range would help any cost model.
- **Direct-to-cell revenue per user.** Starlink reports 16 million users but no clean per-user revenue for the direct-to-cell layer specifically; AST is still pre-scale. The unit economics of "fill the dead zones" remain unproven, which bears directly on any space-comms revenue model.
- **Where a Rocket Lab offering would sit.** This doc sizes the ground market; it does not decide whether a Rocket Lab comms play targets D2D (crowded, carrier-aligned), enterprise/B2B backhaul (the `rf_limited_service.md` boutique concept), or pure wholesale capacity. That is a thesis decision, not a market fact.

---

## Claims Table

| COMM- ID | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-001 | US wireless carrier service revenue, 2025 | ~$326.4 billion | [ESTIMATE] single major source | IBISWorld |
| COMM-002 | US wireless service revenue projected, 2026 | ~$336.1 billion | [PROJECTION] | IBISWorld |
| COMM-003 | US total telecom services (wireless + wireline), 2025 | ~$451.7 billion | [ESTIMATE] | Mordor Intelligence |
| COMM-004 | Total US wireless connections | 579 million | [FACT] | CTIA 2025 survey, RCR Wireless |
| COMM-005 | US 5G connections | 259+ million | [FACT] | CTIA 2025 survey |
| COMM-006 | Annual US mobile data used, 2024 | 132 trillion MB | [FACT] | CTIA, PR Newswire |
| COMM-007 | Verizon market cap, Jun 2026 | ~$191-201 billion | [FACT] | companiesmarketcap, stockanalysis |
| COMM-008 | Verizon total revenue, FY2025 | $138.191 billion | [FACT] | Verizon FY2025 results / 10-K |
| COMM-009 | Verizon net income, FY2025 | $17.2-17.6 billion | [FACT] | Verizon FY2025 results |
| COMM-010 | Verizon free cash flow, FY2025 | $20.1 billion | [FACT] | Verizon FY2025 results |
| COMM-011 | Verizon wireless retail connections, YE2025 | ~146 million | [FACT] | Verizon FY2025 results |
| COMM-012 | Verizon retail postpaid ARPA, Q4 2025 | $147.36 | [FACT] | Verizon FY2025 results |
| COMM-013 | AT&T market cap, Jun 2026 | ~$156-160 billion (down ~20% YoY) | [FACT] | macrotrends, stockanalysis |
| COMM-014 | AT&T total revenue, FY2025 | $125.6 billion (+2.7%) | [FACT] | AT&T 4Q/FY2025 release |
| COMM-015 | AT&T net income, FY2025 | ~$21.9 to $22.0 billion (base-effect jump) | [FACT] | AT&T FY2025 release, stocktitan |
| COMM-016 | AT&T Mobility service revenue, FY2025 | $65.4 billion (+3.5%) | [FACT] | AT&T FY2025 release |
| COMM-017 | AT&T postpaid phone subscribers, YE2025 | 74.2 million | [FACT] | AT&T FY2025 release |
| COMM-018 | AT&T postpaid phone ARPU, FY2025 | $56.57 | [FACT] | AT&T FY2025 release, Statista |
| COMM-019 | T-Mobile market cap, Jun 2026 | ~$216 billion | [FACT] | macrotrends, companiesmarketcap |
| COMM-020 | T-Mobile total revenue, FY2025 | $88.309 billion | [FACT] | T-Mobile Q4/FY2025 8-K |
| COMM-021 | T-Mobile total service revenue, FY2025 | $71.306 billion (+8%) | [FACT] | T-Mobile Q4/FY2025 8-K |
| COMM-022 | T-Mobile net income, FY2025 | $10.992 billion | [FACT] | T-Mobile Q4/FY2025 8-K |
| COMM-023 | T-Mobile total customers, YE2025 | 142.388 million | [FACT] | T-Mobile Q4/FY2025 8-K |
| COMM-024 | T-Mobile postpaid phone customers, YE2025 | 85.594 million | [FACT] | T-Mobile Q4/FY2025 8-K |
| COMM-025 | T-Mobile postpaid phone ARPU, FY2025 | $50.37 | [FACT] | T-Mobile Q4/FY2025 8-K |
| COMM-026 | US MVNO market size, 2025 (central) | ~$13 to $15 billion | [ESTIMATE] methodology-dependent | Mordor, Ken Research |
| COMM-027 | US MVNO market size, 2025 (outlier) | ~$43.82 billion | [ESTIMATE] broader scope, flagged | Verified Market Research |
| COMM-028 | Charter Spectrum Mobile residential lines, Q3 2025 | ~11.01 million | [FACT] | Light Reading / Charter results |
| COMM-029 | Combined cable (Comcast + Charter) mobile lines | well over 20 million | [FACT] | Light Reading, Mobile World Live |
| COMM-030 | Comcast/Charter modernized MVNO with Verizon | announced late Jan 2026 | [FACT] | Light Reading, TipRanks |
| COMM-031 | Comcast/Charter new business MVNO with T-Mobile | wholesale from 2026 | [FACT] | Fierce Network, Broadband Breakfast |
| COMM-032 | Starlink Direct to Cell users | 16M unique / 10M MAU (Mar 2026) | [FACT] | NewSpaceTracker, Tesorb |
| COMM-033 | AST SpaceMobile MNO agreements / reach | 45+ operators, ~2.8B subscribers | [FACT] | AST FY2025 8-K |
| COMM-034 | AST SpaceMobile revenue, 2025 | ~$70.9 million (from ~$4.4M) | [FACT] | stockanalysis, AST 8-K |
| COMM-035 | AST SpaceMobile market cap, mid-2026 | ~$46 billion | [FACT] | stockanalysis, Motley Fool |
| COMM-036 | US D2D split: AT&T/Verizon via AST; T-Mobile via Starlink | structural | [FACT] | NewSpaceTracker, AST 8-K |
| COMM-037 | SpaceX 2025 revenue / Starlink share | ~$15B total, ~$10.4B Starlink | [ESTIMATE] single-source (SpaceX private) | press coverage |
