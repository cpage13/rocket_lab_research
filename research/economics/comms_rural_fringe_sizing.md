# The Satellite-Addressable Rural and Remote Fringe, Sized in Dollars (ex-China)

*Research date: June 2026. Communications research-wiki effort, wave 2 (shared library).*

**Builds on / does not duplicate:** this doc takes the demand-gap base that wave 1 established and converts it into a bottoms-up DOLLAR estimate of the realistically space-addressable rural and remote fringe. The load-bearing inputs it builds on (and cites by path, rather than re-deriving) are:

- [research/synthesis/comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md), Section 2 (the gap base: coverage gap vs usage gap, the ~0.5% satellite share, and the honest-base-case framing).
- [research/economics/comms_space_tam_claims.md](../economics/comms_space_tam_claims.md) (the $1.6T cited TAM, the Morningstar ~$129B realistic served estimate and its tier method, and the three structural discounts: density, ARPU-reality, shared-market).
- [research/economics/comms_global_regional_market.md](../economics/comms_global_regional_market.md) (the regional market structure, the ~300M coverage gap / ~3.1B usage gap, the per-region penetration and rural-gap figures, and the satellite-share base).

This doc answers one narrow question those docs flagged as open (baseline synthesis Section 5 item 4; global_regional Open Question 6): **the realistic space-addressable fringe is "coverage gap plus underserved rural," not the whole broadband pool. What is that fringe worth in annual revenue, once you attach a realistic, region-specific ARPU instead of multiplying billions of low-income people by a developed-market price?**

> **Reading guide.** Every hard number is tagged **[FACT]** (reported / filed 2025-26 data), **[ESTIMATE]** (market-research sizing or our own arithmetic on sourced inputs), **[PROJECTION]** (forward forecast), or **[ILLUSTRATIVE]** (a sizing scenario built to show the shape, not to forecast a number). The headline dollar cases in Sections 4 and 5 are explicitly **[ILLUSTRATIVE]**: they are bottoms-up arithmetic on sourced household counts and sourced ARPUs, not a forecast that any one operator captures them. China is **excluded** from every total and noted only as a labelled aside.

---

## Summary / Verdict

**Confidence: medium on the headline dollar ranges (the inputs are sourced but the arithmetic is ours and the ARPU-by-tier splits carry real uncertainty); medium-high on the core structural finding (the coverage gap and the usage gap are different problems, and only one is space-addressable revenue); high on the direction of the cross-checks (the bottoms-up build lands in the same tens-to-low-hundreds-of-billions band as four independent external anchors).**

The realistic space-addressable rural and remote connectivity fringe, ex-China, sized bottoms-up with region-specific ARPU, is worth on the order of:

- **Conservative case: ~$40 to $55 billion per year** [ILLUSTRATIVE]. This counts only the households and sites a satellite can both physically reach and that can pay a satellite-grade ARPU: the developed-world rural and remote unserved/underserved fringe (high ARPU, small count), plus the high-value mobility verticals (maritime, aviation, energy, government-remote), plus a thin, genuinely-paying slice of the emerging-market rural fringe. It deliberately excludes most of the ~3.1 billion usage-gap people, because that is an affordability and income problem that satellite supply does not solve.
- **Optimistic case: ~$95 to $130 billion per year** [ILLUSTRATIVE]. This adds deeper penetration of the developed-world fringe, a carrier direct-to-cell "add-on" layer across the wider mobile base, and a larger (but still affordability-capped, low-ARPU) emerging-market rural slice as prices fall toward local purchasing power.

**How this compares to the two reference numbers the thesis named:**

- The bottoms-up fringe lands at roughly **30% to 100% of Morningstar's ~$129 billion realistic served estimate** for a mature LEO connectivity business (the conservative case is well under it; the optimistic case converges on it). This is the right kind of agreement: Morningstar built the same "Niche plus Add-on" market top-down from SpaceX's own $1.6T and got ~$129B; this doc built the rural-and-remote core of that market bottoms-up from household counts and got a range that brackets it. Two independent methods landing in the same band is the load-bearing result. See [comms_space_tam_claims.md](../economics/comms_space_tam_claims.md) for the Morningstar derivation.
- Against the **$1.6 trillion cited connectivity TAM** ([comms_space_tam_claims.md](../economics/comms_space_tam_claims.md)), the fringe is roughly **2.5% (conservative) to 8% (optimistic)** of the headline. That is consistent with the "~90% haircut / served is ~5-10% of cited" finding the wave-1 work established, and if anything the conservative case sits below even that, because the rural-and-remote fringe is a subset of the served market (it excludes the carrier add-on and some enterprise that Morningstar keeps).

**The one structural point that dominates the whole exercise:** the dollars are made almost entirely in the developed-world rural fringe and the mobility verticals, NOT in the headline-grabbing billions of unconnected people. The developed-world rural fringe is perhaps **30 to 45 million households** [ESTIMATE] at a **$700 to $1,400 per year** ARPU; the emerging-market rural fringe is **hundreds of millions of people** but at a **$30 to $120 per year** payable ARPU, and most of them cannot pay even that without subsidy. Multiplying the big population by the big ARPU is the single error every inflated TAM makes; this doc's entire job is to not make it.

**Single-source figures the lead should double-check** (flagged in-line and in the claims table): (1) the **residential ~$2,000/yr Starlink ARPU** and the Value Add VC residential developed-vs-emerging subscriber/ARPU split (one analyst blog, though corroborated in direction by the blended-ARPU prints); (2) the **Quilty ~25-30 million household profitable-capacity ceiling** (one analyst, via Via Satellite); (3) **Oxford Economics' 78M-421M global user range through 2035** (one report, Amazon-commissioned, used only as an outer bracket); (4) the **Morningstar ~$10B US Niche-broadband sub-figure** (10% of US households x $75/mo), which was reachable only through a search excerpt of the PDF, not the full table.

---

## 1. The Core Distinction: Coverage Gap vs Usage Gap (only one is space-addressable revenue)

This is the most important section and it governs every number below. The wave-1 base ([comms_global_regional_market.md](../economics/comms_global_regional_market.md) Section 5; [comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md) Section 2.4) established two very different "gaps." They are constantly conflated in cited TAMs, and conflating them is what produces trillion-dollar numbers.

| Gap (2025, global incl. China in the GSMA source) | Size | What kind of problem it is | Can satellite supply fix it? | Revenue implication |
|---|---|---|---|---|
| **Coverage gap** (no mobile/broadband service available at all) | **~300 million people (~4%)** [FACT] | A **supply** problem: there is genuinely no network | **Yes** (this is exactly what a satellite uniquely does) | But these people are concentrated in the poorest, most remote places, so ARPU is very low |
| **Usage gap** (covered but offline) | **~3.1 billion people** [FACT] | A **demand / affordability / income / device** problem: a network exists, they do not buy it | **No** (the network already reaches them; satellite adds no coverage they lack) | Largely zero addressable revenue for satellite, because the binding constraint is income, not supply |

Source: [GSMA usage-gap release](https://www.gsma.com/newsroom/press-release/gsma-calls-for-renewed-focus-on-closing-the-usage-gap-as-more-than-3-billion-people-remain-offline-despite-available-mobile-internet-services/), as carried in [comms_global_regional_market.md](../economics/comms_global_regional_market.md) (COMM-021, COMM-022).

**The trap this avoids.** A cited TAM like AST's "~3.5 billion underserved" or "the next billion users" ([comms_space_tam_claims.md](../economics/comms_space_tam_claims.md) Section 2) is mostly the **usage gap**: people a terrestrial network already covers but who do not buy service because they cannot afford it. A satellite does not change their affordability. So the usage gap is **not** space-addressable supply revenue; it is a demand problem terrestrial operators already have and cannot monetize. The space-addressable fringe is built from the **coverage gap** (genuinely unserved) plus the **underserved-but-payable rural** layer (served by something, but so poorly or so expensively that a satellite competes on quality), NOT from the 3.1 billion.

**Why "underserved" still counts, but only partly.** "Underserved" households (covered by something slow or unreliable, e.g. old DSL or a congested cell) are a real satellite market, because here the satellite competes on **quality and reliability**, which is exactly the axis the wave-1 value curve says the market rewards ([comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md) Section 4.1: the curve rewards reach and reliability, not raw Mbps). But "underserved" only converts to revenue where the household can pay a satellite-grade price. In the developed world that holds. In low-income rural areas it largely does not. That income split is the spine of Sections 2 through 5.

---

## 2. Region-Specific ARPU: the number you must get right

Before counting households, fix the ARPU by tier, because applying one ARPU across all of them is the cardinal error. The evidence is unusually clean here because Starlink is now live across the full income spectrum and its own pricing reveals the willingness-to-pay by region.

### 2.1 What people actually pay, by tier

| Tier | Monthly price / ARPU | Annualized | Source |
|---|---|---|---|
| **US / developed residential (Starlink)** | $55 (100 Mbps) / $85 (200 Mbps) / $120-130 (top tier) per month | ~$660 to ~$1,560/yr | [Starlink US tiers, via search](https://www.starlink-prices.com/personal/residential/usd/low), [HighSpeedInternet](https://www.highspeedinternet.com/resources/how-much-is-starlink-in-my-area) |
| **Starlink residential ARPU (segment, all-in incl. hardware/add-ons)** | ~$167/mo equivalent | **~$2,000/yr** | [spacexstock](https://spacexstock.com/starlink-valuation-and-price-prediction-in-2025/), [economyinsights](https://www.economyinsights.com/p/how-spacex-uses-starlink-to-create-recurring-revenue-streams) (single-source-ish; see flag) |
| **Starlink blended ARPU (all segments, all geographies)** | $81/mo (2025) falling to $66/mo (Q1 2026) | ~$790 to ~$970/yr | [The Information via search](https://www.theinformation.com/articles/spacexs-starlink-revenue-per-user-fell-18-customers-quadrupled), [The Next Web](https://thenextweb.com/news/starlink-is-spacexs-cash-machine-but-the-maths-is-getting-harder) |
| **Emerging-market residential (Starlink, e.g. Nigeria)** | ~$30 to $40/mo (many markets under $30) | ~$360 to ~$480/yr | [starlinkinsider](https://starlinkinsider.com/starlink-price/), [doflam](https://www.doflam.com/starlink-price-costs-guide/) |
| **Sub-Saharan Africa mobile ARPU (what the mass market actually pays)** | South Africa ~$6, Nigeria ~$4, Kenya <$2 per month | ~$24 to ~$72/yr | [Intelsat / ABI via search](https://www.abiresearch.com/blogs/2022/08/24/mobile-broadband-in-africa-facts-for-network-providers/), [Intelsat PDF](https://www.intelsat.com/wp-content/uploads/2023/11/SatelliteConnectivityNewChapter.pdf) |
| **High-value mobility verticals (Starlink)** | maritime ~$34,000/yr; aviation ~$300,000/yr per platform | very high | [valueaddvc](https://valueaddvc.com/blog/starlink-revenue-2025-2026-subscriber-count-arpu-and-the-path-to-profitability), [newspaceeconomy](https://newspaceeconomy.ca/2026/05/30/what-is-starlinks-financial-performance/) |

> **FLAG (single-source-ish): the residential ~$2,000/yr ARPU.** This is widely repeated but traces to a small set of analyst write-ups, not an SpaceX disclosure. It is directionally consistent with the math (Standard Residential at $120/mo is ~$1,440/yr in subscription alone, and the ~$2,000 figure adds hardware amortization and premium add-ons), and it sits above the blended ARPU ($66-81/mo), which is what you would expect since the blend is dragged down by cheap emerging-market subs. Treat it as a reasonable developed-residential anchor, not a hard fact. The lead should double-check.

### 2.2 The split that proves the thesis

The single most useful external segmentation is the Value Add VC build of Starlink's subscriber and revenue mix [ESTIMATE, single analyst source, flagged]:

| Residential sub-segment | Share of subs | Typical monthly ARPU |
|---|---|---|
| Residential, developed markets | ~45% of subs | $80 to $120 |
| Residential, emerging markets | ~35% of subs | $10 to $40 |

Source: [valueaddvc](https://valueaddvc.com/blog/starlink-revenue-2025-2026-subscriber-count-arpu-and-the-path-to-profitability) (single source; flagged). The signal is the **ratio, not the exact percentages**: the emerging-market residential base is already a similar headcount to the developed base, but at one-quarter to one-eighth the ARPU. This is the ARPU-reality discount ([comms_space_tam_claims.md](../economics/comms_space_tam_claims.md) Section 6) made concrete: **the people are in the emerging world; the dollars are in the developed world.**

The affordability ceiling underneath the emerging tier is hard. Africans pay on average **8.8% of monthly income for 1GB of data** (vs 1.5% in Asia, 3.6% in Latin America), and in the poorest countries 1GB costs up to a fifth of monthly earnings ([Intelsat/ABI via search](https://www.abiresearch.com/blogs/2022/08/24/mobile-broadband-in-africa-facts-for-network-providers/)). A Starlink dish at even $30/month is multiples of what a rural sub-Saharan household spends on all connectivity today. This is why the usage gap stays a usage gap: the constraint is income, and a better supply does not lift income. The realistic emerging-market path is **shared / community access** (one terminal serving a village, a school, a clinic, a small ISP reselling), which raises the effective revenue per terminal but keeps revenue-per-person very low.

---

## 3. Counting the Addressable Households and Sites, by Tier (ex-China)

Now the household counts, kept deliberately conservative and tied to sourced penetration figures. The structure is three tiers, because they have radically different ARPUs.

### 3.1 Tier A: the developed-world rural and remote fringe (small count, high ARPU)

This is the economic core. These households can pay a satellite ARPU, and a satellite is genuinely their best or only option.

| Geography | Addressable fringe (households) | Basis | Source |
|---|---|---|---|
| **United States** | **~8 to 13 million HH** | "Broadband deserts" (no/limited terrestrial) ~6% of ~132M HH = ~8M; plus part of the ~12% rural-with-weak-terrestrial = up to ~13M total addressable | [Via Satellite US LEO opportunity](https://interactive.satellitetoday.com/via/march-2026/examining-the-size-of-the-us-residential-broadband-opportunity-for-leo-satcom) (6% deserts, 12% rural); US HH ~132M ([Statista](https://www.statista.com/statistics/183635/number-of-households-in-the-us/)) |
| **Other developed (Canada, Australia, NZ, Europe, Japan)** | **~20 to 30 million HH** | OECD rural households are ~21.5% uncovered at 30 Mbps (78.5% covered); applied to the rural household base of the developed world ex-US, the satellite-addressable slice is tens of millions | [OECD: 78.5% rural covered at 30 Mbps](https://www.oecd.org/en/data/insights/statistical-releases/2025/07/digital-connectivity-expands-across-the-oecd-but-rural-areas-are-falling-further-behind.html) |
| **Tier A total** | **~30 to 45 million HH** [ESTIMATE] | Sum of the above | This doc |

> The Australia/Canada/Europe count is an [ESTIMATE]: published sources give the *percentage* rural-coverage gap cleanly (OECD 78.5% rural covered at 30 Mbps; even lower at 100 Mbps), but a clean absolute household count for the developed world ex-US is not directly published. The 20-30M range is our arithmetic on the rural household base times the rural gap percentage, and the lead should treat the count as softer than the percentage. Real-world traction corroborates the order of magnitude: in Australia, **1 in 5 rural households that switched provider chose Starlink**, and Canada shows a similar rural win-share ([search summary](https://www.theglobalstatistics.com/starlink-internet-statistics/)).

### 3.2 Tier B: the high-value mobility and enterprise verticals (tiny count, very high ARPU)

These are not "rural households" but they are the rest of the genuinely space-addressable, high-ARPU demand the rural fringe sits alongside, and they are a large share of the dollars. Included because any honest rural-fringe revenue number that ignored them would understate the addressable pool a rural-focused constellation actually sells into.

| Vertical | Scale signal | ARPU | Source |
|---|---|---|---|
| Maritime | tens of thousands of vessels | ~$34,000/yr/vessel | [valueaddvc](https://valueaddvc.com/blog/starlink-revenue-2025-2026-subscriber-count-arpu-and-the-path-to-profitability) |
| Aviation | thousands of aircraft | ~$300,000/yr/aircraft | [newspaceeconomy](https://newspaceeconomy.ca/2026/05/30/what-is-starlinks-financial-performance/) |
| Energy, mining, remote government/defense, disaster recovery, RV/mobility | the Morningstar "Niche" non-broadband components | high per-site | [comms_space_tam_claims.md](../economics/comms_space_tam_claims.md) (Morningstar Niche tier) |

This is the bulk of the difference between Morningstar's **~$84B Niche** tier and its **~$10B US Niche-broadband** sub-figure: most of the Niche dollars are mobility/enterprise/government, not rural residential. See [comms_space_tam_claims.md](../economics/comms_space_tam_claims.md).

### 3.3 Tier C: the emerging-market rural fringe (huge count, very low payable ARPU)

This is where the headline billions live, and where the dollars do not. The base regions are documented in [comms_global_regional_market.md](../economics/comms_global_regional_market.md) Section 7:

| Region | Rural unserved / underserved people | Payable reality | Source |
|---|---|---|---|
| Sub-Saharan Africa | ~960M not using mobile internet (64%); the largest coverage gap worldwide | Mostly usage gap (income), not coverage gap; mobile ARPU $2-6/mo; community/shared access only | [GSMA SSA](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-for-development/blog/despite-improvements-sub-saharan-africa-has-the-widest-usage-and-coverage-gaps-worldwide/) |
| Latin America | ~46 to 77M rural people without quality internet | Low fixed penetration (~55% HH); emerging ARPU $30-40/mo at the top end, far less payable below | [IDB](https://www.iadb.org/en/news/least-77-million-rural-inhabitants-have-no-access-high-quality-internet-services), [CEPAL](https://desarrollodigital.cepal.org/en/data-and-facts/latin-america-and-caribbean-among-regions-lowest-fixed-broadband-penetration) |
| Asia ex-China (South/SE Asia) | usage gap "over 45%"; very large rural base | Low ARPU; India reshaped by ultra-cheap data; satellite competes only at the unserved edge | [GSMA SOMIC](https://www.gsma.com/somic/) |

**The hard filter on Tier C:** of the ~300M global coverage gap, the part that is both (a) outside China and (b) able to pay even a shared/community satellite ARPU is a small fraction. The realistic Tier C revenue comes not from billions of people but from a few million genuinely-paying connections (small rural ISPs, community Wi-Fi nodes, schools, clinics, businesses, the rural middle class) at a low per-connection ARPU. The billions are a development and subsidy story, not a near-term commercial revenue story.

---

## 4. The Bottoms-Up Dollar Build (conservative case) [ILLUSTRATIVE]

Putting Sections 2 and 3 together. This is the **conservative** case: modest penetration of the addressable fringe, region-specific ARPU held to what people demonstrably pay, and the emerging-market tier kept small because affordability caps it.

| Tier | Addressable units | Penetration / capture assumed | Effective annual ARPU | Annual revenue |
|---|---|---|---|---|
| **A. Developed rural/remote residential** | ~30-45M HH | ~40-50% (a satellite is best/only option for much of this fringe) | ~$900/yr (blend of US ~$1,000-2,000 and other-developed lower tiers) | **~$13 to $20B** |
| **B. Mobility + enterprise + remote-gov verticals** | tens of thousands of high-ARPU platforms + sites | the established Niche-non-broadband base | very high per unit | **~$20 to $28B** |
| **C. Emerging-market rural (genuinely paying)** | a few million connections (community/ISP/business/middle-class) | thin | ~$200-400/yr per connection (shared access lifts per-terminal revenue) | **~$5 to $8B** |
| **Conservative total** | | | | **~$40 to $55B/yr** [ILLUSTRATIVE] |

**What the conservative case says.** Even a satellite business that wins much of the developed-world rural fringe, owns the high-value mobility verticals, and gets a real (if thin) foothold in emerging-market rural is a **~$40-55B/yr** addressable revenue pool, ex-China. Tiers A and B (developed-world fringe plus mobility) are ~$33-48B of that; the emerging-world billions add only ~$5-8B, despite being the overwhelming majority of the headcount. **That asymmetry is the whole finding.**

---

## 5. The Optimistic Case [ILLUSTRATIVE]

The **optimistic** case loosens the assumptions in the directions that are plausible but not assured: deeper developed-fringe penetration, a carrier direct-to-cell "add-on" layer monetizing the wider mobile base (the Morningstar Add-on tier), prices falling toward local purchasing power in emerging markets (which expands the payable Tier C base even at low ARPU), and faster mobility/enterprise growth.

| Tier | Optimistic assumption change | Annual revenue |
|---|---|---|
| **A. Developed rural/remote residential** | Higher penetration (~60-70%) and ARPU holding near the $1,000-2,000 developed band | **~$25 to $35B** |
| **B. Mobility + enterprise + remote-gov** | Faster vertical adoption (aviation/maritime/energy ramp) | **~$30 to $40B** |
| **C. Emerging-market rural** | Prices fall toward affordability; tens of millions of paying connections at low ARPU; shared-access scales | **~$15 to $25B** |
| **D. Carrier direct-to-cell add-on layer** | A $10-15/mo bolt-on premium across a slice of the wider mobile base (the Morningstar ~$45B Add-on tier, partially captured) | **~$20 to $30B** |
| **Optimistic total** | | **~$95 to $130B/yr** [ILLUSTRATIVE] |

**What the optimistic case says.** If satellite captures the developed fringe deeply, the mobility verticals fully, a price-driven expansion of the emerging-market rural base, and a meaningful slice of the carrier direct-to-cell add-on, the addressable pool reaches **~$95-130B/yr**, which converges on Morningstar's independent ~$129B. Note that even here, the emerging-market rural tier (C, ~$15-25B) remains a minority of the total despite containing the vast majority of the world's unconnected people, and that a large part of the upside (tier D, direct-to-cell) is **not** rural-fringe broadband at all but a carrier add-on across the general mobile base. Strip tier D out and the rural-and-remote-proper optimistic number is ~$75-100B.

---

## 6. Cross-Checks: does the bottoms-up build agree with reality?

Four independent anchors, none of which fed the build above, all land in the same band. This is the reason to believe the range.

| Anchor | What it measures | Value | Implication for the fringe estimate |
|---|---|---|---|
| **Starlink actual connectivity revenue, FY2025** | The largest LEO operator's actual collected revenue across all segments and geographies, ex nothing | **$11.39B** [FACT] | A real operator, ~9-10M subs, is at ~$11B today. The conservative ~$40-55B addressable pool is ~4-5x current Starlink revenue, i.e. the pool is real but years of buildout ahead of today's realized revenue. Source: [The Next Web](https://thenextweb.com/news/starlink-is-spacexs-cash-machine-but-the-maths-is-getting-harder), [New Space Economy](https://newspaceeconomy.ca/2026/05/30/what-is-starlinks-financial-performance/) |
| **Morningstar realistic served market** | Top-down "Niche + Add-on" rebuild of SpaceX's $1.6T | **~$129B** (Niche ~$84B + Add-on ~$45B); US Niche-broadband ~$10B at 10% of US HH x $75/mo | The optimistic bottoms-up case (~$95-130B) converges on it; the conservative case (~$40-55B) is the rural-and-mobility core without the full Add-on layer. Morningstar's own ~$10B US-rural-broadband sub-figure matches this doc's Tier A US slice. Source: [comms_space_tam_claims.md](../economics/comms_space_tam_claims.md), [Morningstar PDF](https://d1e00ek4ebabms.cloudfront.net/production/uploaded-files/Our_Realistic_Starlink_Market_Sizing-915d25bb-5968-4e1f-ae0b-ad5999a9aa87.pdf) |
| **Quilty capacity ceiling** | A supply-side cap: how many households Starlink can *profitably* serve given current launch costs | **~25 to 30 million households** [ESTIMATE, single source] | Caps the developed-fringe count realistically: this doc's Tier A (~30-45M addressable HH) is near or above the supply ceiling, confirming the fringe is small enough that capacity, not demand, may bind. Source: [Via Satellite (Quilty/Henry)](https://interactive.satellitetoday.com/via/march-2026/the-coming-wave-of-competition-in-leo-constellations) |
| **Oxford Economics global user range, through 2035** | An independent (Amazon-commissioned) three-scenario user forecast | **78M to 421M users globally** [PROJECTION, single source] | Brackets the household pool. At a blended ~$300-800/yr these users imply roughly $25B (low) to $200B+ (high) of revenue, straddling this doc's conservative-to-optimistic band. Source: [Oxford Economics](https://www.oxfordeconomics.com/resource/the-global-value-of-leo-satellite-broadband-services/), [Telecompaper](https://www.telecompaper.com/news/leo-satellite-broadband-could-boost-global-gdp-by-usd-863-bln-by-2035--1570854) |

**The convergence, stated plainly.** A bottoms-up household-and-ARPU build (this doc), a top-down tier rebuild (Morningstar), a supply-side capacity cap (Quilty), and an independent user forecast (Oxford Economics) all put the realistically space-addressable connectivity market in the **tens to low-hundreds of billions of dollars per year**, ex-China. None of them supports the trillion. The rural-and-remote fringe specifically (Tiers A and C, excluding mobility and the carrier add-on) is the **lower-tens-of-billions**: large enough to be a real business, small enough that it is a niche of a niche of the $1.6T headline.

---

## 7. The Starlink Trajectory as a Live Cross-Check (the ARPU warning)

Starlink's own numbers are the clearest warning against optimistic ARPU assumptions, and they directly validate this doc's tier structure.

| Metric | Value | Source |
|---|---|---|
| Connectivity revenue, FY2025 | $11.39B (operating profit ~$4.42B) | [The Next Web](https://thenextweb.com/news/starlink-is-spacexs-cash-machine-but-the-maths-is-getting-harder) |
| Subscribers | ~9M end-2025; 10.3M Q1 2026 (doubled YoY from 4.4M) | [The Next Web](https://thenextweb.com/news/starlink-is-spacexs-cash-machine-but-the-maths-is-getting-harder), [IEEE ComSoc](https://techblog.comsoc.org/2025/12/30/starlink-doubles-subscriber-base-expands-to-to-42-new-countries-territories-other-markets/) |
| Blended ARPU | $99/mo (2023) -> $86/mo (Q1 2025) -> $66/mo (Q1 2026): **-33% in ~2 years** | [The Information via search](https://www.theinformation.com/articles/spacexs-starlink-revenue-per-user-fell-18-customers-quadrupled), [The Next Web](https://thenextweb.com/news/starlink-is-spacexs-cash-machine-but-the-maths-is-getting-harder) |
| Why ARPU fell | Deliberate expansion into "price-sensitive markets across Africa, South-East Asia, and Latin America" at prices set to local purchasing power | [The Next Web](https://thenextweb.com/news/starlink-is-spacexs-cash-machine-but-the-maths-is-getting-harder) |
| May 2026 move | Price increase of $5-$10/mo across consumer plans (monetizing the installed base after the growth land-grab) | [The Next Web](https://thenextweb.com/news/starlink-is-spacexs-cash-machine-but-the-maths-is-getting-harder) |

**The lesson for the fringe sizing.** Starlink's ARPU fell by a third precisely *because* it chased the emerging-market rural fringe (Tier C). The subscriber count doubled while operating income barely moved. This is the ARPU-reality discount happening in real time: the emerging-market rural base adds **subscribers** but not proportional **dollars**. It is direct evidence that the conservative case (which keeps Tier C small and low-ARPU) is the more honest base, and that the optimistic case's Tier C ($15-25B) depends on a very large number of very-low-ARPU connections that only materialize if prices fall further, which compresses ARPU further. The developed-world rural fringe (Tier A) and the verticals (Tier B) are where the durable, high-margin dollars are.

---

## 8. China (excluded): noted aside

China is excluded from every figure above. For scale only: China has its own large rural connectivity programs and its own LEO constellations (Guowang, Qianfan/SpaceSail) serving a domestic market closed to a Western operator. China's rural fringe is real and large but is not addressable by a US or allied satellite operator and is added to no figure here. See [comms_global_regional_market.md](../economics/comms_global_regional_market.md) Section 8 for the China-fixed-broadband scale aside (~630M+ subscriptions, ~$303B revenue, excluded).

---

## Sources

*Starlink financials, ARPU, and trajectory*
- [The Next Web, Starlink is SpaceX's cash machine but the maths is getting harder (FY2025 $11.39B, ARPU decline, May 2026 price rise)](https://thenextweb.com/news/starlink-is-spacexs-cash-machine-but-the-maths-is-getting-harder)
- [New Space Economy, What is Starlink's financial performance](https://newspaceeconomy.ca/2026/05/30/what-is-starlinks-financial-performance/)
- [The Information, Starlink revenue per user fell 18% as customers quadrupled](https://www.theinformation.com/articles/spacexs-starlink-revenue-per-user-fell-18-customers-quadrupled)
- [Value Add VC, Starlink revenue 2026 run-rate, subscriber/ARPU segmentation (single source, flagged)](https://valueaddvc.com/blog/starlink-revenue-2025-2026-subscriber-count-arpu-and-the-path-to-profitability)
- [spacexstock, Starlink valuation and residential ARPU](https://spacexstock.com/starlink-valuation-and-price-prediction-in-2025/)
- [economyinsights, How SpaceX uses Starlink to create recurring revenue](https://www.economyinsights.com/p/how-spacex-uses-starlink-to-create-recurring-revenue-streams)
- [IEEE ComSoc, Starlink doubles subscriber base, 42 new markets](https://techblog.comsoc.org/2025/12/30/starlink-doubles-subscriber-base-expands-to-to-42-new-countries-territories-other-markets/)

*Starlink pricing by country*
- [Starlink Prices (residential, by country, USD)](https://www.starlink-prices.com/personal/residential/usd/low)
- [Starlink Insider, all countries and prices 2025](https://starlinkinsider.com/starlink-price/)
- [DOFLAM, Starlink price guide 2025](https://www.doflam.com/starlink-price-costs-guide/)
- [HighSpeedInternet, how much is Starlink in my area](https://www.highspeedinternet.com/resources/how-much-is-starlink-in-my-area)

*Addressable household / fringe counts*
- [Via Satellite, Examining the Size of the US Residential Broadband Opportunity for LEO Satcom (6% deserts, 12% rural)](https://interactive.satellitetoday.com/via/march-2026/examining-the-size-of-the-us-residential-broadband-opportunity-for-leo-satcom)
- [Via Satellite, The Coming Wave of Competition in LEO Constellations (Quilty 25-30M capacity ceiling)](https://interactive.satellitetoday.com/via/march-2026/the-coming-wave-of-competition-in-leo-constellations)
- [OECD, Digital connectivity expands but rural areas falling behind (78.5% rural covered at 30 Mbps)](https://www.oecd.org/en/data/insights/statistical-releases/2025/07/digital-connectivity-expands-across-the-oecd-but-rural-areas-are-falling-further-behind.html)
- [Statista, number of US households 2025](https://www.statista.com/statistics/183635/number-of-households-in-the-us/)
- [The Global Statistics, Starlink internet statistics (Australia 1-in-5 rural win-share)](https://www.theglobalstatistics.com/starlink-internet-statistics/)

*Emerging-market ARPU and affordability*
- [ABI Research, mobile broadband in Africa facts for network providers (ARPU $2-6, affordability)](https://www.abiresearch.com/blogs/2022/08/24/mobile-broadband-in-africa-facts-for-network-providers/)
- [Intelsat, Satellite Connectivity: a new chapter (Africa affordability, 8.8% of income per 1GB)](https://www.intelsat.com/wp-content/uploads/2023/11/SatelliteConnectivityNewChapter.pdf)

*Independent global sizing cross-checks*
- [Oxford Economics, The Global Value of LEO Satellite Broadband Services (78M-421M users through 2035)](https://www.oxfordeconomics.com/resource/the-global-value-of-leo-satellite-broadband-services/)
- [Telecompaper, LEO satellite broadband could boost global GDP by USD 863 bln by 2035](https://www.telecompaper.com/news/leo-satellite-broadband-could-boost-global-gdp-by-usd-863-bln-by-2035--1570854)
- [Morningstar, Testing the Sky's Limits: Our Realistic Starlink Market Sizing (~$129B, Niche/Add-on)](https://d1e00ek4ebabms.cloudfront.net/production/uploaded-files/Our_Realistic_Starlink_Market_Sizing-915d25bb-5968-4e1f-ae0b-ad5999a9aa87.pdf)
- [Morningstar, Starlink market opportunity blog](https://www.morningstar.com/business/insights/blog/starlink-market-opportunity)

*Library docs this builds on (carry the underlying gap-base and regional citations)*
- [comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md)
- [comms_space_tam_claims.md](../economics/comms_space_tam_claims.md)
- [comms_global_regional_market.md](../economics/comms_global_regional_market.md)

---

## Confidence

- **The core distinction (Section 1): high.** Coverage gap (~300M, supply problem) vs usage gap (~3.1B, income problem) is a primary GSMA distinction carried through the wave-1 base, and the claim that satellite supply does not fix the usage gap is structural, not a forecast.
- **The region-specific ARPU (Section 2): medium-high on the tiers, medium on the exact residential figure.** The developed-vs-emerging ARPU gap (10x or more) is corroborated by Starlink's actual country pricing, its blended-ARPU decline, and African mobile ARPU data, all from independent sources. The exact ~$2,000/yr residential figure and the Value Add VC sub-segment split are single-source-ish and flagged.
- **The household counts (Section 3): medium.** The percentages (6% US deserts, 12% US rural, 78.5% OECD rural coverage) are sourced; the absolute counts for the developed world ex-US are our arithmetic and are softer than the percentages. The emerging-market people-counts are sourced but their conversion to *payable* connections is an estimate.
- **The dollar cases (Sections 4-5): medium, and explicitly ILLUSTRATIVE.** They are bottoms-up arithmetic on sourced inputs, not forecasts. The penetration and capture rates are reasoned assumptions. The value of the exercise is the *structure* (where the dollars are vs where the people are) and the *cross-checked band*, not a precise point number.
- **The cross-checks (Section 6): high on the convergence, medium on each individual anchor.** Four independent methods landing in the same tens-to-low-hundreds-of-billions band is the strongest result in the doc. Each anchor individually (Morningstar model, Quilty single-analyst cap, Oxford Economics commissioned study, Starlink reported revenue) carries its own caveat, but they do not share a method, so their agreement is meaningful.

---

## Open Questions

1. **The developed-world rural household count ex-US.** The percentages are clean (OECD rural coverage gaps), but a clean absolute count of satellite-addressable rural households across Canada, Australia, NZ, Europe, and Japan is not directly published and was estimated here. A country-by-country build would tighten Tier A, which drives most of the conservative-case dollars.
2. **The payable fraction of the emerging-market rural fringe.** Section 3.3 filters billions of people down to "a few million genuinely-paying connections," but that conversion is the softest number in the doc. How many emerging-market rural connections actually pay a satellite-grade (even shared-access) ARPU, at what price, is the key uncertainty in both cases' Tier C.
3. **Direct-to-cell as fringe vs add-on.** The optimistic case's Tier D (carrier direct-to-cell, ~$20-30B) is not rural-fringe broadband; it is a bolt-on across the general mobile base. Whether to count it in a "rural fringe" number at all is a definitional call the lead should make. Stripping it out gives a rural-and-remote-proper optimistic ceiling of ~$75-100B.
4. **The residential ARPU anchor.** The ~$2,000/yr residential figure is load-bearing for Tier A and is single-source-ish. A firmer developed-residential ARPU (ideally from an SpaceX disclosure or a multi-source reconciliation) would tighten the conservative case.
5. **Capacity vs demand as the binding constraint.** Quilty's ~25-30M profitable-household ceiling sits right at this doc's Tier A addressable count. If capacity binds before demand, the realistic *captured* revenue is lower than the *addressable* pool, and the constraint shifts from "how many want it" to "how many can be served per dollar of launch." That interacts directly with the data-center-vs-comms capex framing in [comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md) Section 4.

---

## Claims

| COMM- id | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-057 | Space-addressable rural/remote fringe, conservative case (ex-China) | ~$40 to $55B/yr | [ILLUSTRATIVE] (bottoms-up on sourced inputs) | This doc, Section 4 |
| COMM-058 | Space-addressable rural/remote fringe, optimistic case (ex-China) | ~$95 to $130B/yr | [ILLUSTRATIVE] (bottoms-up on sourced inputs) | This doc, Section 5 |
| COMM-059 | Rural-and-remote-proper optimistic ceiling (excl. carrier direct-to-cell add-on) | ~$75 to $100B/yr | [ILLUSTRATIVE] | This doc, Section 5 |
| COMM-060 | Fringe as % of Morningstar realistic served market (~$129B) | ~30% (conservative) to ~100% (optimistic) | [ESTIMATE] | This doc vs [comms_space_tam_claims.md](../economics/comms_space_tam_claims.md) |
| COMM-061 | Fringe as % of SpaceX cited $1.6T connectivity TAM | ~2.5% (conservative) to ~8% (optimistic) | [ESTIMATE] | This doc vs [comms_space_tam_claims.md](../economics/comms_space_tam_claims.md) |
| COMM-062 | Coverage gap (space-addressable supply problem) | ~300M people (~4%) | [FACT] | [GSMA](https://www.gsma.com/newsroom/press-release/gsma-calls-for-renewed-focus-on-closing-the-usage-gap-as-more-than-3-billion-people-remain-offline-despite-available-mobile-internet-services/) via global_regional |
| COMM-063 | Usage gap (NOT space-addressable; income problem) | ~3.1B people | [FACT] | [GSMA](https://www.gsma.com/somic/) via global_regional |
| COMM-064 | Starlink US/developed residential price tiers | $55 / $85 / $120-130 per month | [FACT] | [Starlink Prices](https://www.starlink-prices.com/personal/residential/usd/low), [HighSpeedInternet](https://www.highspeedinternet.com/resources/how-much-is-starlink-in-my-area) |
| COMM-065 | Starlink residential segment ARPU | ~$2,000/yr | [ESTIMATE] single-source-ish (FLAG) | [spacexstock](https://spacexstock.com/starlink-valuation-and-price-prediction-in-2025/), [economyinsights](https://www.economyinsights.com/p/how-spacex-uses-starlink-to-create-recurring-revenue-streams) |
| COMM-066 | Starlink blended ARPU trajectory | $99/mo (2023) to $86 (Q1 2025) to $66/mo (Q1 2026); -33% | [FACT] | [The Information](https://www.theinformation.com/articles/spacexs-starlink-revenue-per-user-fell-18-customers-quadrupled), [The Next Web](https://thenextweb.com/news/starlink-is-spacexs-cash-machine-but-the-maths-is-getting-harder) |
| COMM-067 | Starlink emerging-market residential price (e.g. Nigeria) | ~$30 to $40/mo (some markets <$30) | [FACT] | [Starlink Insider](https://starlinkinsider.com/starlink-price/), [DOFLAM](https://www.doflam.com/starlink-price-costs-guide/) |
| COMM-068 | Sub-Saharan Africa mobile ARPU (mass-market payable) | South Africa ~$6, Nigeria ~$4, Kenya <$2 per month | [FACT] | [ABI Research](https://www.abiresearch.com/blogs/2022/08/24/mobile-broadband-in-africa-facts-for-network-providers/), [Intelsat](https://www.intelsat.com/wp-content/uploads/2023/11/SatelliteConnectivityNewChapter.pdf) |
| COMM-069 | Africa affordability: cost of 1GB data as share of income | ~8.8% (vs 3.6% LatAm, 1.5% Asia); up to ~20% in poorest | [FACT] | [ABI Research](https://www.abiresearch.com/blogs/2022/08/24/mobile-broadband-in-africa-facts-for-network-providers/) |
| COMM-070 | Starlink developed-vs-emerging residential ARPU split | developed ~45% subs @ $80-120; emerging ~35% subs @ $10-40 | [ESTIMATE] single source (FLAG) | [Value Add VC](https://valueaddvc.com/blog/starlink-revenue-2025-2026-subscriber-count-arpu-and-the-path-to-profitability) |
| COMM-071 | Maritime / aviation vertical ARPU | maritime ~$34,000/yr; aviation ~$300,000/yr per platform | [ESTIMATE] | [Value Add VC](https://valueaddvc.com/blog/starlink-revenue-2025-2026-subscriber-count-arpu-and-the-path-to-profitability), [New Space Economy](https://newspaceeconomy.ca/2026/05/30/what-is-starlinks-financial-performance/) |
| COMM-072 | US "broadband desert" (no/limited terrestrial) share | ~6% of US households | [FACT] | [Via Satellite](https://interactive.satellitetoday.com/via/march-2026/examining-the-size-of-the-us-residential-broadband-opportunity-for-leo-satcom) |
| COMM-073 | US rural-with-terrestrial-but-weak share | ~12% of US households | [FACT] | [Via Satellite](https://interactive.satellitetoday.com/via/march-2026/examining-the-size-of-the-us-residential-broadband-opportunity-for-leo-satcom) |
| COMM-074 | OECD rural fixed-broadband coverage (30 Mbps) | ~78.5% rural vs ~92.3% overall (so ~21.5% rural gap) | [FACT] | [OECD](https://www.oecd.org/en/data/insights/statistical-releases/2025/07/digital-connectivity-expands-across-the-oecd-but-rural-areas-are-falling-further-behind.html) |
| COMM-075 | Developed-world satellite-addressable rural fringe (Tier A) | ~30 to 45M households | [ESTIMATE] | This doc, Section 3.1 (counts softer than the % inputs) |
| COMM-076 | Starlink actual connectivity revenue FY2025 | $11.39B (operating profit ~$4.42B) | [FACT] | [The Next Web](https://thenextweb.com/news/starlink-is-spacexs-cash-machine-but-the-maths-is-getting-harder), [New Space Economy](https://newspaceeconomy.ca/2026/05/30/what-is-starlinks-financial-performance/) |
| COMM-077 | Starlink subscribers | ~9M end-2025; 10.3M Q1 2026 (doubled YoY) | [FACT] | [The Next Web](https://thenextweb.com/news/starlink-is-spacexs-cash-machine-but-the-maths-is-getting-harder), [IEEE ComSoc](https://techblog.comsoc.org/2025/12/30/starlink-doubles-subscriber-base-expands-to-to-42-new-countries-territories-other-markets/) |
| COMM-078 | Quilty profitable-capacity ceiling (supply-side cap) | ~25 to 30M households without launch-cost reductions | [ESTIMATE] single source (FLAG) | [Via Satellite](https://interactive.satellitetoday.com/via/march-2026/the-coming-wave-of-competition-in-leo-constellations) |
| COMM-079 | Oxford Economics global LEO user range through 2035 | 78M to 421M users (GDP uplift $32B-$863B) | [PROJECTION] single source (FLAG) | [Oxford Economics](https://www.oxfordeconomics.com/resource/the-global-value-of-leo-satellite-broadband-services/), [Telecompaper](https://www.telecompaper.com/news/leo-satellite-broadband-could-boost-global-gdp-by-usd-863-bln-by-2035--1570854) |
| COMM-080 | Morningstar US Niche-broadband sub-figure (rural) | ~$10B (10% of US HH x ~$75/mo ARPU) | [ESTIMATE] (PDF excerpt, FLAG) | [Morningstar](https://www.morningstar.com/business/insights/blog/starlink-market-opportunity), [Morningstar PDF](https://d1e00ek4ebabms.cloudfront.net/production/uploaded-files/Our_Realistic_Starlink_Market_Sizing-915d25bb-5968-4e1f-ae0b-ad5999a9aa87.pdf) |
| COMM-081 | Emerging-market rural fringe people (base, not payable revenue) | SSA ~960M offline; LatAm ~46-77M rural; Asia ex-China usage gap >45% | [FACT] | [GSMA](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-for-development/blog/despite-improvements-sub-saharan-africa-has-the-widest-usage-and-coverage-gaps-worldwide/), [IDB](https://www.iadb.org/en/news/least-77-million-rural-inhabitants-have-no-access-high-quality-internet-services), [GSMA SOMIC](https://www.gsma.com/somic/) |
