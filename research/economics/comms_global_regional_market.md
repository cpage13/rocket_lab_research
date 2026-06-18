# Global and Regional Communications Market (Broadband plus Cellular), by Region, ex-China

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:** the two US anchor docs, [research/economics/comms_us_broadband_market.md](comms_us_broadband_market.md) and [research/economics/comms_us_cellular_market.md](comms_us_cellular_market.md), which size the US market in detail. This doc sizes the rest of the world and the global total around them, and pulls the global broadband-substitution framings the founder asked for. It is a neutral base sizing for the shared library; any track (communications, data center) can reference it. No verdict on the space business is offered here.

---

## Summary / Verdict

**Confidence: medium-high on the global and large-region totals; medium on the per-region splits; low on the two illustrative substitution framings (they are arithmetic, not forecasts).**

The global communications service market (the money end users and enterprises pay operators for connectivity and related services) is on the order of **$2.0 to $2.1 trillion in 2025** [ESTIMATE, reconciled from multiple market-research firms]. That total splits into two very unequal halves by product:

- **Mobile / cellular service revenue: about $1.19 trillion in 2025** [FACT, GSMA], the larger half by far.
- **Fixed broadband service revenue: about $360 to $390 billion in 2025** [ESTIMATE, multiple firms], roughly a sixth to a fifth of the total.

The rest of the ~$2T (enterprise/wholesale/voice/managed services and the wider "telecom services" bucket) sits above those two consumer-connectivity lines, which is why the all-in "telecom services market" prints higher than mobile-plus-fixed-broadband alone.

By region the rank order is stable across sources: **Asia Pacific is the largest (~34% of telecom service revenue), North America second (~29%), Europe third (~26%)**, with Latin America and the Middle East and Africa smaller but faster-growing. The United States alone is roughly a quarter of the global telecom service market (see the US anchor docs).

Two things matter most for a space-delivery lens:

1. **The connection base is enormous but the dollars per connection are thin in exactly the places with the most unconnected people.** There are about **9.2 billion mobile-cellular subscriptions** and about **1.53 billion fixed broadband subscriptions** worldwide in 2025 [FACT, ITU and Point Topic]. About **3.1 billion people remain offline despite living under mobile coverage** (the "usage gap") and about **300 million** live with no coverage at all (the "coverage gap") [FACT, GSMA].
2. **Satellite is today a rounding error of the fixed base.** Satellite is about **0.5% of global fixed broadband subscribers** [FACT, Point Topic]; Starlink, the dominant provider, reached about **9 million subscribers by December 2025** and more than **12 million by mid-2026** [FACT], versus 1.53 billion terrestrial. The two founder framings below quantify the ceiling if that share grew.

China is **excluded** from every total above and below. It is the single largest national market on both axes (China Mobile alone reports about 320 million fixed broadband subscribers), and folding it in would inflate Asia and the global total substantially. It is treated only as a noted aside in Section 8.

---

## 1. Global totals: three different "market sizes," and why they differ

A reader will see wildly different headline numbers for "the telecom market." They are not contradictory; they measure different things. The table separates them.

| Metric (2025) | Value | What it counts | Sources |
|---|---|---|---|
| Mobile operator service revenue | **~$1.19 trillion** [FACT] | What mobile operators actually bill for cellular service | [GSMA Mobile Economy](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/), [1Global summary](https://www.1global.com/blog/mobile-operators/takeaways-gsma-mobile-economy-2026) |
| Fixed broadband service revenue | **~$360 to $390 billion** [ESTIMATE] | What end users pay for fixed broadband connections | [Grand View](https://www.grandviewresearch.com/industry-analysis/fixed-broadband-services-market-report), [Precedence](https://www.precedenceresearch.com/broadband-services-market) |
| Total telecom services market | **~$2.0 to $2.1 trillion** [ESTIMATE] | All telecom services: mobile + fixed + enterprise + wholesale + voice + managed | [Precedence](https://www.precedenceresearch.com/telecom-services-market), [Grand View](https://www.grandviewresearch.com/industry-analysis/global-telecom-services-market) |
| (Context only) Mobile economy GDP contribution | ~$7.6 trillion [FACT] | Wider economic value of mobile, NOT service revenue | [GSMA](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/) |

**Important distinction the lead should preserve:** the often-quoted "$7.6 trillion" and "$11.3 trillion by 2030" GSMA figures are the **economic value mobile adds to GDP**, including device makers and downstream productivity. They are NOT operator revenue and must never be summed with the market-size lines. The revenue the industry collects is the ~$1.19T mobile line.

**FLAGGED ESTIMATE (global total):** the "$2.0 to $2.1T total telecom services" band is a reconciliation, not a single sourced number. Estimates range from about **$1.55T** ([Deloitte](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-telecom-outlooks/telecommunications-industry-outlook.html), narrower connectivity scope) and **$1.14T** PwC connectivity revenue (2023, narrowest scope) up to **$2.10T** ([Precedence](https://www.precedenceresearch.com/telecom-services-market)) and **$2.096T** ([Grand View](https://www.grandviewresearch.com/industry-analysis/global-telecom-services-market)) on the broad "services" definition. The spread is scope, not error: connectivity-only is lower, all-services is higher. This doc uses the broad ~$2.0 to $2.1T as the working total and notes the PwC ~$1.14T (2023, growing ~4.3% per year) as the connectivity-only floor.

---

## 2. Global product split: mobile vs fixed broadband

| Product line (2025) | Service revenue | Subscriptions | Sources |
|---|---|---|---|
| Mobile / cellular | ~$1.19 trillion [FACT] | ~9.2 billion subscriptions; ~5.8 billion unique people [FACT] | [GSMA](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/), [ITU 2025 Facts and Figures](https://www.itu.int/itu-d/reports/statistics/2025/10/15/ff25-subscriptions/) |
| Fixed broadband | ~$360 to $390 billion [ESTIMATE] | ~1.53 billion subscriptions [FACT] | [Grand View](https://www.grandviewresearch.com/industry-analysis/fixed-broadband-services-market-report), [Point Topic via IEEE](https://techblog.comsoc.org/2025/10/29/point-topic-global-broadband-subscribers-in-q2-2025-5g-fwa-dsl-satellite-and-fttp/) |

Two structural facts from this table drive everything downstream:

- **Mobile is ~3x the revenue of fixed broadband and ~6x the connection count.** Any "communications market" sizing is dominated by mobile.
- **Mobile broadband is now 89% of all mobile subscriptions** [FACT, ITU], up from under 50% in 2015. The mobile network is increasingly a data network. 5G is about 36% of mobile broadband subscriptions globally [FACT, ITU], having passed 3 billion connections in 2025 [Omdia, single source for the exact 3bn timing].

Fixed broadband by access technology (Q2 2025, share of the 1.53B base) [FACT, [Point Topic](https://techblog.comsoc.org/2025/10/29/point-topic-global-broadband-subscribers-in-q2-2025-5g-fwa-dsl-satellite-and-fttp/)]:

| Technology | Share of global fixed broadband | YoY growth |
|---|---|---|
| Fiber (FTTH/B) | ~72.7% | +7.2% |
| DSL, cable, other legacy | ~24% (declining) | DSL -12.1% |
| Fixed wireless access (FWA) | ~2.8% | 5G FWA +31% |
| **Satellite** | **~0.5%** | **+41.6%** |

The last row is the one that matters for a space thesis: satellite is growing fastest in percentage terms off the smallest base. It is half a percent of fixed broadband today.

---

## 3. Regional revenue split (telecom services, ex-China-adjusted)

Sources report regional shares on the all-in telecom-services definition. The percentages below are the most consistent set across firms; the dollar figures are the matching regional totals. Asia Pacific figures **include China** in most published splits, so the ex-China caveat is noted in the row and quantified in Section 8.

| Region | Approx. 2025 telecom service revenue | Share of global | Notes | Sources |
|---|---|---|---|---|
| Asia Pacific (incl. China) | ~$700 to $717 billion | ~34% | Largest region; ex-China it is far smaller (see Sec. 8) | [Grand View regional](https://www.grandviewresearch.com/horizon/outlook/telecom-services-market/asia-pacific), [Grand View global](https://www.grandviewresearch.com/industry-analysis/global-telecom-services-market) |
| North America | ~$600 to $611 billion | ~29% | US is the bulk (~$520B+); see US anchor docs | [Grand View NA](https://www.grandviewresearch.com/horizon/outlook/telecom-services-market/north-america) |
| Europe | ~$546 billion | ~26% | Mature, low single-digit growth | [Grand View Europe](https://www.grandviewresearch.com/horizon/outlook/telecom-services-market/europe), [Market Data Forecast](https://www.marketdataforecast.com/market-reports/europe-telecom-market) |
| Middle East and Africa | ~$345 billion (MNO market) | high-growth | ~10.8% CAGR to 2030; subscriber base 1.81B (2025) | [Mordor MEA](https://www.mordorintelligence.com/industry-reports/middle-east-and-africa-telecom-market) |
| Latin America | ~$159 billion | smaller | ~6.3% CAGR; expansion-upside (Sec. 7) | [Market Data Forecast LatAm](https://www.marketdataforecast.com/market-reports/latin-america-telecommunication-market) |

**FLAGGED ESTIMATE (regional dollar figures):** the per-region dollar totals come largely from Grand View's auto-generated regional pages and a few peers. They are internally consistent on rank order and roughly add to the global total, but the exact dollar figures differ by firm and by what each bucket includes (the MEA figure is an "MNO market" scope, not strictly comparable to the others). Treat the **shares** as more reliable than the **absolute dollars**. The regional shares also vary by source: one alternate split has North America ~32%, Asia Pacific ~30%, Europe ~26%, Middle East and Africa ~12% ([Grand View global](https://www.grandviewresearch.com/industry-analysis/global-telecom-services-market)). The lead should pick one firm's split for any cross-region arithmetic rather than mixing them.

---

## 4. Per-region detail: size, broadband vs cellular, penetration, top operators

### North America

| Attribute | Value | Source |
|---|---|---|
| Telecom service revenue (2025) | ~$600 to $611 billion (~29% of global) | [Grand View NA](https://www.grandviewresearch.com/horizon/outlook/telecom-services-market/north-america) |
| Dominant product | Mobile data services largest revenue line | [Grand View NA](https://www.grandviewresearch.com/horizon/outlook/telecom-services-market/north-america) |
| Fixed broadband penetration | US ~91% of households, Canada ~96% | [S&P Americas Broadband Roundup](https://www.spglobal.com/market-intelligence/en/news-insights/research/2025/11/americas-broadband-roundup-2025) |
| Mobile-cellular penetration | Americas ~132 per 100 inhabitants | [ITU](https://www.itu.int/itu-d/reports/statistics/2025/10/15/ff25-subscriptions/) |
| Largest operators | Mobile: Verizon, AT&T, T-Mobile. Fixed: Comcast (~31.3M), Charter (~29.7M), Verizon (~16.3M post-Frontier), AT&T (~14.3M), T-Mobile FWA (~8M) | [Broadband Breakfast](https://broadbandbreakfast.com/with-8-million-users-globally-starlink-likely-seventh-largest-fixed-u-s-isp/) |

The US sub-market is detailed in the two US anchor docs ([broadband](comms_us_broadband_market.md), [cellular](comms_us_cellular_market.md)); they are not repeated here. North America is the most saturated, highest-ARPU region: high penetration, low growth (~1% per year in some forecasts), revenue growth coming from convergence (mobile + broadband bundles) and 5G/FWA rather than new connections.

### Europe (ex-Russia/CIS treated separately by most sources)

| Attribute | Value | Source |
|---|---|---|
| Telecom service revenue (2025) | ~$546 billion (~26% of global) | [Grand View Europe](https://www.grandviewresearch.com/horizon/outlook/telecom-services-market/europe) |
| Fixed broadband penetration | ~36.5 subscriptions per 100 inhabitants (highest of any region); ~400M subscriptions across 40+ countries | [OECD](https://www.oecd.org/en/data/insights/statistical-releases/2025/10/fibre-and-5g-drive-oecd-digital-transformation-as-broadband-markets-mature.html) |
| Mobile economic value (context, not revenue) | ~€1.1 trillion EU GDP contribution | [GSMA](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/) |
| Largest operators | Deutsche Telekom, Vodafone, Orange, Telefonica, BT (each multi-country) | [Statista telecom leaders](https://www.statista.com/topics/12811/telecoms-market-leaders/), [Market Data Forecast Europe](https://www.marketdataforecast.com/market-reports/europe-telecom-market) |

Europe is mature and fragmented: the highest fixed-broadband penetration of any region but low growth (~2.5% CAGR) and intense price competition across many national markets and pan-regional groups.

### Latin America

| Attribute | Value | Source |
|---|---|---|
| Telecom service revenue (2025) | ~$159 billion; ~6.3% CAGR to 2033 | [Market Data Forecast LatAm](https://www.marketdataforecast.com/market-reports/latin-america-telecommunication-market) |
| Mobile economic value (context) | ~$600 billion GDP contribution (8.6% of GDP) | [GSMA Mobile Economy LatAm](https://www.gsmaintelligence.com/research/the-mobile-economy-latin-america-2025) |
| Fixed broadband penetration | ~55% of households (2024); ~18% of population; one of the lowest fixed-penetration regions globally | [CEPAL Digital Observatory](https://desarrollodigital.cepal.org/en/data-and-facts/latin-america-and-caribbean-among-regions-lowest-fixed-broadband-penetration), [FTTH Panorama LatAm 2024](https://fiberbroadband.org/wp-content/uploads/2025/01/SmC-FBA-Panorama-Latam-FTTH-2024-202411.pdf) |
| Largest operators | America Movil (Claro; ~$44B regional revenue 2023), Telefonica (Vivo/Movistar; ~$20B), TIM Brasil | [Statista LatAm telecom](https://www.statista.com/topics/7290/telecommunications-in-latin-america/) |

Latin America is mobile-led with a thin and uneven fixed layer. It is an **expansion-upside region** (Section 7).

### Asia (excluding China)

| Attribute | Value | Source |
|---|---|---|
| Asia Pacific telecom revenue (incl. China) | ~$700 to $717 billion (~34% of global) | [Grand View APAC](https://www.grandviewresearch.com/horizon/outlook/telecom-services-market/asia-pacific) |
| Ex-China share | Materially smaller; China is the single largest national market (see Sec. 8) | [RCR Wireless China](https://www.rcrwireless.com/20251209/carriers/china-fixed) |
| Fixed broadband subscriptions | Asia Pacific >600M (largest region, includes China) | [Statista by region](https://www.statista.com/statistics/496846/global-fixed-broadband-subscriptions-by-region/) |
| Largest operators (ex-China) | India: Reliance Jio, Bharti Airtel, Vodafone Idea. Indonesia: Telkom Indonesia, Indosat Ooredoo, XL Axiata | [Grand View APAC](https://www.grandviewresearch.com/horizon/outlook/telecom-services-market/asia-pacific) |

Ex-China, the standout is **India**: forecast to register the highest telecom CAGR in the region (2026 to 2030), with Reliance Jio having reshaped data affordability. Indonesia (~$13.7B market) and the rest of South and Southeast Asia add a large, lower-ARPU, fast-growing base. Parts of Asia ex-China are an **expansion-upside region** (Section 7).

### Middle East and Africa

| Attribute | Value | Source |
|---|---|---|
| Telecom (MNO) market (2025) | ~$345 billion; ~10.8% CAGR to 2030 (fastest region) | [Mordor MEA](https://www.mordorintelligence.com/industry-reports/middle-east-and-africa-telecom-market) |
| Subscriber base | 1.81 billion (2025), growing to 2.64 billion by 2030 | [Mordor MEA](https://www.mordorintelligence.com/industry-reports/middle-east-and-africa-telecom-market) |
| Mobile penetration | Africa ~92 per 100 (lowest region); mobile broadband Africa ~56 per 100 | [ITU](https://www.itu.int/itu-d/reports/statistics/2025/10/15/ff25-subscriptions/) |
| Largest operators | e& (Etisalat), MTN Group, STC, Zain, Vodacom, Ooredoo, Orange | [Mordor MEA companies](https://www.mordorintelligence.com/industry-reports/middle-east-and-africa-telecom-market/companies) |

MEA splits into two very different sub-regions: the Gulf (high ARPU, fast 5G, fiber/FWA upgrades) and Sub-Saharan Africa (the world's largest connectivity gap; see Section 7). It is the fastest-growing region in percentage terms and the single biggest **expansion-upside** zone for any new entrant.

---

## 5. Penetration and the gap base (the demand behind any new supply)

| Metric (2025) | Value | Source |
|---|---|---|
| Mobile-cellular subscriptions, global | ~9.2 billion (112 per 100 inhabitants) | [ITU](https://www.itu.int/itu-d/reports/statistics/2025/10/15/ff25-subscriptions/) |
| Fixed broadband subscriptions, global | ~1.53 billion (~20 per 100 inhabitants) | [Point Topic](https://techblog.comsoc.org/2025/10/29/point-topic-global-broadband-subscribers-in-q2-2025-5g-fwa-dsl-satellite-and-fttp/) |
| Fixed broadband, high-income vs low-income | 39 per 100 vs 0.6 per 100 | [ITU](https://www.itu.int/itu-d/reports/statistics/2025/10/15/ff25-subscriptions/) |
| People using mobile internet | ~4.7 billion (58% of population) | [GSMA SOMIC](https://www.gsma.com/somic/) |
| Coverage gap (no mobile coverage at all) | ~300 million (4% of population) | [GSMA](https://www.gsma.com/newsroom/press-release/gsma-calls-for-renewed-focus-on-closing-the-usage-gap-as-more-than-3-billion-people-remain-offline-despite-available-mobile-internet-services/) |
| Usage gap (covered but not online) | ~3.1 billion | [GSMA](https://www.gsma.com/newsroom/press-release/gsma-calls-for-renewed-focus-on-closing-the-usage-gap-as-more-than-3-billion-people-remain-offline-despite-available-mobile-internet-services/) |

The gap split is the key nuance for a space thesis: the **coverage gap** (people genuinely beyond any terrestrial network) is the part a satellite can uniquely serve, and it is only ~300 million people, concentrated in remote and poor areas. The much larger **usage gap** (~3.1 billion) is an affordability and device problem, not a coverage problem, so satellite supply does not directly address it. This is the realistic boundary on the "expansion-upside" story.

---

## 6. Founder framing (a): all broadband-to-space, aggregated [ILLUSTRATIVE]

**This is an illustrative ceiling, not a forecast.** It answers: if every broadband connection were treated as a candidate for space delivery, how big is that pool today?

| Pool (2025) | Size | Implied revenue at current prices | Source basis |
|---|---|---|---|
| All fixed broadband subscriptions | ~1.53 billion | ~$360 to $390 billion (current fixed broadband service revenue) | [Point Topic](https://techblog.comsoc.org/2025/10/29/point-topic-global-broadband-subscribers-in-q2-2025-5g-fwa-dsl-satellite-and-fttp/), [Grand View](https://www.grandviewresearch.com/industry-analysis/fixed-broadband-services-market-report) |
| of which satellite today | ~0.5% (~7 to 8 million subs) | tiny | [Point Topic](https://techblog.comsoc.org/2025/10/29/point-topic-global-broadband-subscribers-in-q2-2025-5g-fwa-dsl-satellite-and-fttp/) |
| Add: mobile broadband connections (if "broadband" is read widely) | mobile broadband is 89% of ~9.2B mobile subs | mobile service revenue ~$1.19 trillion | [ITU](https://www.itu.int/itu-d/reports/statistics/2025/10/15/ff25-subscriptions/), [GSMA](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/) |

**How to read it:** if "broadband-to-space" means **fixed broadband only**, the aggregate addressable pool is ~1.53 billion connections worth ~$360 to $390 billion per year at today's prices, and satellite holds ~0.5% of it. If "broadband" is read to include **mobile broadband** (direct-to-device and the like), the candidate pool balloons toward the full ~$1.5T+ consumer connectivity market, because almost every mobile subscription is now a broadband subscription. The honest framing is the fixed-broadband one: ~$360 to $390B is the pool that fixed satellite broadband competes inside today.

**FLAGGED as ILLUSTRATIVE:** treating 100% of fixed broadband as "addressable for space" ignores that fiber at ~73% of the base is cheaper, faster, and lower-latency in served areas. The realistic near-term space-addressable slice is the **coverage gap plus the underserved rural fringe**, not the whole pool. This framing is the outer wall, not the room.

---

## 7. Founder framing (b): space replaces ground, full substitution [ILLUSTRATIVE]

**This is a hypothetical full-substitution ceiling, not a forecast and not a plan.** It answers: if space delivery fully replaced terrestrial delivery, what is the size of the market being substituted?

| Scenario | Market being substituted (2025, ex-China) | Source basis |
|---|---|---|
| Replace all fixed broadband | ~$360 to $390 billion/year | Section 2 |
| Replace all fixed broadband + all mobile/cellular | ~$1.5 trillion+/year (combine $360-390B fixed + ~$1.19T mobile) | Sections 1, 2 |
| Replace the entire telecom services market | ~$2.0 to $2.1 trillion/year | Section 1 |

**How to read it:** full ground substitution is a ~$2 trillion-per-year ceiling (everything end users and enterprises pay for connectivity, ex-China). The mobile half (~$1.19T) is the larger prize but the harder one to take from space, because it is dominated by dense urban coverage where terrestrial is overwhelmingly cheaper per bit. The fixed-broadband half (~$360 to $390B) is the more contestable layer, and even there fiber economics dominate in cities.

**FLAGGED as ILLUSTRATIVE, strongly:** this is a "size of the thing being displaced" figure, not an attainable market. No credible path has space replacing urban terrestrial connectivity at current cost structures. The figure is useful only as the absolute upper bound and as the denominator against which any real space share (today ~0.5% of fixed) is measured. The economically meaningful version of "space replaces ground" is **the rural and unserved fringe of this $2T**, sized by the coverage gap (~300M people) and the under-served rural broadband base, not the whole figure.

### Where the real expansion-upside sits (South America and parts of Asia ex-China)

Two regions widen the addressable space-delivery demand because their **ground gaps are structural, not just affordability**:

| Region | Why it is expansion-upside | Key figures | Source |
|---|---|---|---|
| South America / Latin America | Lowest fixed-broadband penetration of the major regions; large rural-urban divide that fiber is not closing fast | ~55% of households on fixed broadband; ~18% of population; only ~4 in 10 rural inhabitants have any connectivity option (vs 71% urban); ~46 to 77 million rural people without quality internet | [CEPAL](https://desarrollodigital.cepal.org/en/data-and-facts/latin-america-and-caribbean-among-regions-lowest-fixed-broadband-penetration), [IDB](https://www.iadb.org/en/news/least-77-million-rural-inhabitants-have-no-access-high-quality-internet-services) |
| Asia ex-China (South/Southeast Asia) | Very large rural populations, wide usage gap, fast-growing but low fixed penetration outside cities | Usage gap "over 45%" in Asia Pacific; India highest regional telecom CAGR | [GSMA SOMIC](https://www.gsma.com/somic/), [Grand View APAC](https://www.grandviewresearch.com/horizon/outlook/telecom-services-market/asia-pacific) |
| (Largest of all) Sub-Saharan Africa | Widest coverage and usage gaps worldwide; terrestrial buildout slowest | ~960 million in Africa not using mobile internet (64% of population); Sub-Saharan Africa has the largest usage gap globally | [GSMA](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-for-development/blog/despite-improvements-sub-saharan-africa-has-the-widest-usage-and-coverage-gaps-worldwide/) |

These regions are where "space replaces ground" is least illustrative and most real, because in the rural fringe there often is no competitive ground to replace. The constraint there is affordability (ARPU is low), which caps the revenue even where the connection need is high.

---

## 8. China (excluded from all totals above): noted aside

China is excluded from every figure in this doc. For scale context only:

| China metric (2025) | Value | Source |
|---|---|---|
| China fixed broadband (China Mobile alone) | ~320 million subscribers | [RCR Wireless](https://www.rcrwireless.com/20251209/carriers/china-fixed) |
| China fixed broadband (China Telecom) | ~200 million subscribers | [RCR Wireless](https://www.rcrwireless.com/20251209/carriers/china-fixed) |
| China fixed broadband (China Unicom) | ~113 million subscribers | [RCR Wireless](https://www.rcrwireless.com/20251209/carriers/china-fixed) |
| China fixed communications service revenue | ~$303 billion (2025), to ~$314B by 2030 | [TelecomLead](https://telecomlead.com/broadband/china-fixed-communications-market-to-reach-314-bn-by-2030-driven-by-fiber-broadband-and-operator-efficiency-123445) |

China's three carriers alone hold roughly **630 million+ fixed broadband subscriptions**, which is more than 40% of the entire global fixed broadband base of 1.53 billion. This is why the Asia Pacific regional totals in Section 3 (which include China) are not a fair proxy for the ex-China Asian opportunity, and why China is carved out: it is a closed market for a Western operator and it dominates Asian totals. It is mentioned here for scale only and is not added to any addressable figure.

---

## Sources

Global market size and revenue:
- [Precedence Research, Telecom Services Market](https://www.precedenceresearch.com/telecom-services-market)
- [Grand View Research, Global Telecom Services Market](https://www.grandviewresearch.com/industry-analysis/global-telecom-services-market)
- [Deloitte, 2026 Global Telecommunications Industry Outlook](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-telecom-outlooks/telecommunications-industry-outlook.html)
- [PwC, Global Telecoms Outlook press release (2023 revenue, 2028 forecast)](https://www.pwc.com/gx/en/news-room/press-releases/2025/pwc-global-telecoms-outlook.html)

Mobile / cellular:
- [GSMA, The Mobile Economy](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/)
- [GSMA Mobile Economy 2025 (PDF)](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/wp-content/uploads/2025/02/030325-The-Mobile-Economy-2025.pdf)
- [1Global, Mobile Economy 2026 takeaways](https://www.1global.com/blog/mobile-operators/takeaways-gsma-mobile-economy-2026)
- [GSMA Mobile Economy Latin America 2025](https://www.gsmaintelligence.com/research/the-mobile-economy-latin-america-2025)
- [GSMA Mobile Economy MENA 2025](https://www.gsmaintelligence.com/research/the-mobile-economy-middle-east-and-north-africa-2025)
- [GSMA State of Mobile Internet Connectivity (SOMIC)](https://www.gsma.com/somic/)
- [GSMA, usage gap / 3 billion offline](https://www.gsma.com/newsroom/press-release/gsma-calls-for-renewed-focus-on-closing-the-usage-gap-as-more-than-3-billion-people-remain-offline-despite-available-mobile-internet-services/)

Fixed broadband and subscriptions:
- [ITU, 2025 Facts and Figures: Subscriptions](https://www.itu.int/itu-d/reports/statistics/2025/10/15/ff25-subscriptions/)
- [Point Topic via IEEE ComSoc, Global Broadband Subscribers Q2 2025](https://techblog.comsoc.org/2025/10/29/point-topic-global-broadband-subscribers-in-q2-2025-5g-fwa-dsl-satellite-and-fttp/)
- [Grand View Research, Fixed Broadband Services Market](https://www.grandviewresearch.com/industry-analysis/fixed-broadband-services-market-report)
- [Precedence Research, Broadband Services Market](https://www.precedenceresearch.com/broadband-services-market)
- [OECD, Fibre and 5G drive OECD digital transformation (2025)](https://www.oecd.org/en/data/insights/statistical-releases/2025/10/fibre-and-5g-drive-oecd-digital-transformation-as-broadband-markets-mature.html)
- [Statista, Fixed broadband subscriptions worldwide by region](https://www.statista.com/statistics/496846/global-fixed-broadband-subscriptions-by-region/)

Regional markets and operators:
- [Grand View, North America Telecom Services](https://www.grandviewresearch.com/horizon/outlook/telecom-services-market/north-america)
- [Grand View, Europe Telecom Services](https://www.grandviewresearch.com/horizon/outlook/telecom-services-market/europe)
- [Grand View, Asia Pacific Telecom Services](https://www.grandviewresearch.com/horizon/outlook/telecom-services-market/asia-pacific)
- [Market Data Forecast, Europe Telecom Market](https://www.marketdataforecast.com/market-reports/europe-telecom-market)
- [Market Data Forecast, Latin America Telecommunication Market](https://www.marketdataforecast.com/market-reports/latin-america-telecommunication-market)
- [Mordor Intelligence, Middle East and Africa Telecom Market](https://www.mordorintelligence.com/industry-reports/middle-east-and-africa-telecom-market)
- [Statista, Telecoms market leaders](https://www.statista.com/topics/12811/telecoms-market-leaders/)
- [S&P Global, Americas Broadband Roundup 2025](https://www.spglobal.com/market-intelligence/en/news-insights/research/2025/11/americas-broadband-roundup-2025)

Expansion-upside (gaps):
- [CEPAL Digital Development Observatory, Latin America fixed broadband](https://desarrollodigital.cepal.org/en/data-and-facts/latin-america-and-caribbean-among-regions-lowest-fixed-broadband-penetration)
- [IDB, 77 million rural inhabitants without quality internet](https://www.iadb.org/en/news/least-77-million-rural-inhabitants-have-no-access-high-quality-internet-services)
- [GSMA, Sub-Saharan Africa widest gaps](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-for-development/blog/despite-improvements-sub-saharan-africa-has-the-widest-usage-and-coverage-gaps-worldwide/)

Satellite (context for framings):
- [Broadband Breakfast, Starlink 8 million users](https://broadbandbreakfast.com/with-8-million-users-globally-starlink-likely-seventh-largest-fixed-u-s-isp/)
- [IEEE ComSoc, Starlink doubles subscriber base](https://techblog.comsoc.org/2025/12/30/starlink-doubles-subscriber-base-expands-to-to-42-new-countries-territories-other-markets/)

China aside:
- [RCR Wireless, China fixed growth stalls](https://www.rcrwireless.com/20251209/carriers/china-fixed)
- [TelecomLead, China fixed communications market](https://telecomlead.com/broadband/china-fixed-communications-market-to-reach-314-bn-by-2030-driven-by-fiber-broadband-and-operator-efficiency-123445)

---

## Confidence

**Overall: medium-high on the headline global and large-region numbers; medium on per-region dollar splits; low on the two illustrative framings (by design).**

- **High confidence:** mobile operator revenue ~$1.19T (GSMA, the industry's own body); fixed broadband ~1.53B subscriptions and the ~0.5% satellite share (Point Topic, the standard broadband subscriber tracker); ~9.2B mobile subscriptions and penetration figures (ITU, the UN telecom authority); the coverage gap (~300M) and usage gap (~3.1B) (GSMA). These are multi-source or primary-body figures.
- **Medium confidence:** the ~$2.0 to $2.1T total telecom services market (market-research firms agree on the broad band but the absolute number depends on scope, ranging $1.55T to $2.1T); the regional revenue shares (rank order is robust; exact percentages vary by firm); fixed broadband revenue ~$360 to $390B (firms cluster but the band is wide).
- **Lower confidence:** the per-region absolute dollar figures (different firms, different bucket definitions, the MEA figure is an MNO-market scope not strictly comparable); the GSMA Latin America/MENA economic-value figures are GDP-contribution, not revenue, and are used only as context.
- **Lowest (by design):** the two founder framings in Sections 6 and 7 are arithmetic ceilings on a base of sourced numbers, explicitly not forecasts.

---

## Open Questions

1. **Ex-China Asia split.** Published Asia Pacific totals include China. A clean ex-China Asia figure (India + Southeast Asia + developed Asia, excluding China) is not directly published and would need to be built bottom-up from country data. The lead may want a dedicated ex-China Asia sizing.
2. **Fixed broadband revenue exact figure.** The $360 to $390B band is wide. A single authoritative fixed-broadband-revenue series (vs the all-services number) would tighten Section 2.
3. **Regional dollar reconciliation.** The per-region dollar figures come from different firms and bucket definitions. The lead should decide whether to standardize on one firm (e.g., Grand View across all regions) for any cross-region arithmetic.
4. **ARPU by region.** This doc has penetration and totals but not a clean ARPU-by-region table. ARPU is what determines whether the "expansion-upside" connection counts translate into revenue, and it is low in exactly the gap regions. A follow-up ARPU table would sharpen both founder framings.
5. **Direct-to-device overlap.** Framing (a) hinges on whether "broadband" includes mobile broadband. The boundary between fixed-satellite broadband and direct-to-device mobile (which overlaps the ~$1.19T mobile pool) needs a definition before the addressable pool is final.
6. **Satellite-addressable rural fringe.** The realistic space-addressable slice is "coverage gap + underserved rural," not the whole pool. Sizing that fringe in dollars (not just people) is the missing number that would make both framings actionable.

---

## Claims

| ID | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-001 | Global mobile operator service revenue, 2025 | ~$1.19 trillion | FACT | [GSMA](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/), [1Global](https://www.1global.com/blog/mobile-operators/takeaways-gsma-mobile-economy-2026) |
| COMM-002 | Global fixed broadband service revenue, 2025 | ~$360 to $390 billion | ESTIMATE | [Grand View](https://www.grandviewresearch.com/industry-analysis/fixed-broadband-services-market-report), [Precedence](https://www.precedenceresearch.com/broadband-services-market) |
| COMM-003 | Total global telecom services market, 2025 (broad definition) | ~$2.0 to $2.1 trillion | ESTIMATE | [Precedence](https://www.precedenceresearch.com/telecom-services-market), [Grand View](https://www.grandviewresearch.com/industry-analysis/global-telecom-services-market) |
| COMM-004 | Total telecom market, connectivity-only floor (PwC, 2023) | ~$1.14 trillion (growing ~4.3%/yr) | FACT (single firm) | [PwC](https://www.pwc.com/gx/en/news-room/press-releases/2025/pwc-global-telecoms-outlook.html) |
| COMM-005 | Mobile economy GDP contribution, 2025 (context, NOT revenue) | ~$7.6 trillion | FACT | [GSMA](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/) |
| COMM-006 | Global mobile-cellular subscriptions, 2025 | ~9.2 billion (112/100) | FACT | [ITU](https://www.itu.int/itu-d/reports/statistics/2025/10/15/ff25-subscriptions/) |
| COMM-007 | Global unique mobile subscribers, 2025 | ~5.8 billion (~70% of population) | FACT | [GSMA](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/) |
| COMM-008 | Global fixed broadband subscriptions, Q2 2025 | ~1.53 billion | FACT | [Point Topic](https://techblog.comsoc.org/2025/10/29/point-topic-global-broadband-subscribers-in-q2-2025-5g-fwa-dsl-satellite-and-fttp/) |
| COMM-009 | Fixed broadband penetration, global | ~20 per 100 inhabitants (39 high-income, 0.6 low-income) | FACT | [ITU](https://www.itu.int/itu-d/reports/statistics/2025/10/15/ff25-subscriptions/) |
| COMM-010 | Satellite share of global fixed broadband subscribers, 2025 | ~0.5% (growing +41.6% YoY) | FACT | [Point Topic](https://techblog.comsoc.org/2025/10/29/point-topic-global-broadband-subscribers-in-q2-2025-5g-fwa-dsl-satellite-and-fttp/) |
| COMM-011 | Fiber (FTTH/B) share of global fixed broadband, 2025 | ~72.7% | FACT | [Point Topic](https://techblog.comsoc.org/2025/10/29/point-topic-global-broadband-subscribers-in-q2-2025-5g-fwa-dsl-satellite-and-fttp/) |
| COMM-012 | Mobile broadband share of all mobile subscriptions, 2025 | ~89% | FACT | [ITU](https://www.itu.int/itu-d/reports/statistics/2025/10/15/ff25-subscriptions/) |
| COMM-013 | 5G share of mobile broadband subscriptions, 2025 | ~36% (passed 3bn connections) | FACT (3bn timing single source: Omdia) | [ITU](https://www.itu.int/itu-d/reports/statistics/2025/10/15/ff25-subscriptions/) |
| COMM-014 | Asia Pacific share of global telecom service revenue (incl. China), 2025 | ~34% (~$700 to $717B) | ESTIMATE | [Grand View](https://www.grandviewresearch.com/horizon/outlook/telecom-services-market/asia-pacific) |
| COMM-015 | North America share of global telecom service revenue, 2025 | ~29% (~$600 to $611B) | ESTIMATE | [Grand View](https://www.grandviewresearch.com/horizon/outlook/telecom-services-market/north-america) |
| COMM-016 | Europe telecom service revenue, 2025 | ~$546 billion (~26%) | ESTIMATE | [Grand View](https://www.grandviewresearch.com/horizon/outlook/telecom-services-market/europe), [Market Data Forecast](https://www.marketdataforecast.com/market-reports/europe-telecom-market) |
| COMM-017 | Latin America telecom service revenue, 2025 | ~$159 billion (~6.3% CAGR) | ESTIMATE (single firm) | [Market Data Forecast](https://www.marketdataforecast.com/market-reports/latin-america-telecommunication-market) |
| COMM-018 | Middle East and Africa telecom (MNO) market, 2025 | ~$345 billion (~10.8% CAGR) | ESTIMATE (single firm, MNO scope) | [Mordor](https://www.mordorintelligence.com/industry-reports/middle-east-and-africa-telecom-market) |
| COMM-019 | Europe fixed broadband penetration, 2024/2025 | ~36.5 per 100 (highest of any region) | FACT | [OECD](https://www.oecd.org/en/data/insights/statistical-releases/2025/10/fibre-and-5g-drive-oecd-digital-transformation-as-broadband-markets-mature.html) |
| COMM-020 | Latin America fixed broadband household penetration, 2024 | ~55% of households (~18% of population) | FACT | [CEPAL](https://desarrollodigital.cepal.org/en/data-and-facts/latin-america-and-caribbean-among-regions-lowest-fixed-broadband-penetration) |
| COMM-021 | Global coverage gap (no mobile coverage), 2025 | ~300 million people (4%) | FACT | [GSMA](https://www.gsma.com/newsroom/press-release/gsma-calls-for-renewed-focus-on-closing-the-usage-gap-as-more-than-3-billion-people-remain-offline-despite-available-mobile-internet-services/) |
| COMM-022 | Global usage gap (covered but offline), 2025 | ~3.1 billion people | FACT | [GSMA](https://www.gsma.com/somic/) |
| COMM-023 | People using mobile internet, 2025 | ~4.7 billion (58%) | FACT | [GSMA SOMIC](https://www.gsma.com/somic/) |
| COMM-024 | Latin America rural inhabitants without quality internet | ~46 to 77 million | ESTIMATE | [IDB](https://www.iadb.org/en/news/least-77-million-rural-inhabitants-have-no-access-high-quality-internet-services), [CEPAL](https://desarrollodigital.cepal.org/en/data-and-facts/latin-america-and-caribbean-among-regions-lowest-fixed-broadband-penetration) |
| COMM-025 | Africa population not using mobile internet | ~960 million (64%) | FACT | [GSMA](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-for-development/blog/despite-improvements-sub-saharan-africa-has-the-widest-usage-and-coverage-gaps-worldwide/) |
| COMM-026 | Framing (a): all-fixed-broadband-to-space aggregated pool | ~1.53B subs / ~$360 to $390B/yr | PROJECTION (illustrative ceiling) | Sections 2, 6 |
| COMM-027 | Framing (b): full ground substitution (fixed+mobile, ex-China) | ~$1.5 trillion+/yr; up to ~$2.0 to $2.1T for all telecom services | PROJECTION (illustrative ceiling) | Sections 1, 2, 7 |
| COMM-028 | Starlink global subscribers, Dec 2025 / mid-2026 | ~9 million / >12 million | FACT | [IEEE ComSoc](https://techblog.comsoc.org/2025/12/30/starlink-doubles-subscriber-base-expands-to-to-42-new-countries-territories-other-markets/), [Broadband Breakfast](https://broadbandbreakfast.com/with-8-million-users-globally-starlink-likely-seventh-largest-fixed-u-s-isp/) |
| COMM-029 | China fixed broadband subscribers (3 carriers, aside, excluded) | ~630 million+ | FACT | [RCR Wireless](https://www.rcrwireless.com/20251209/carriers/china-fixed) |
| COMM-030 | China fixed communications service revenue (aside, excluded) | ~$303 billion (2025) | FACT (single firm) | [TelecomLead](https://telecomlead.com/broadband/china-fixed-communications-market-to-reach-314-bn-by-2030-driven-by-fiber-broadband-and-operator-efficiency-123445) |
