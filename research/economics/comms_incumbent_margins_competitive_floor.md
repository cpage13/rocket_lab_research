# Ground Incumbents' Margins and the Competitive Price Floor: What a Space Entrant Must Beat to Take Served-Market Share

*Research date: June 2026. Communications research-wiki effort, wave 3 (shared library).*

**Builds on / does not duplicate:** this doc computes the incumbents' margins and their defend-cost price floor from the wave-1 and wave-2 base. It does not re-fetch the carrier financials (subscriber counts, revenue, net income, ARPU); those are carried from the two market docs and cited by path. Its own new web sourcing is confined to the two numbers the base did not pin: each carrier's **EBITDA margin** and the **marginal / incremental cost to serve**. Load-bearing inputs:

- [research/economics/comms_us_broadband_market.md](./comms_us_broadband_market.md) (broadband provider financials, ARPU, the diminishing-returns curve).
- [research/economics/comms_us_cellular_market.md](./comms_us_cellular_market.md) (the Big Three carrier financials, wireless ARPU, the wholesale/MVNO layer).
- [research/economics/comms_cellular_5g_deployment_economics.md](./comms_cellular_5g_deployment_economics.md) (cellular capex intensity, the RAN-and-energy cost stack, the upgrade-vs-newbuild asymmetry).
- [research/economics/comms_broadband_deployment_economics.md](./comms_broadband_deployment_economics.md) (the cable-defend asymmetry: ~$100-300/home to hold a passed home; take-rate; the density cliff).
- [research/economics/comms_addressable_sizing.md](./comms_addressable_sizing.md) (the served-vs-fringe split; the consolidated new-entrant-addressable pool ~$45-150B/yr ex-China).

> **Reading guide.** Each hard number is tagged **[FACT]** (reported / filed 2025-26 data), **[ESTIMATE]** (third-party sizing or our own arithmetic on sourced inputs), **[PROJECTION]** (forward forecast), or **[ILLUSTRATIVE]** (a figure built to show the shape, not to forecast a captured number). Hard numbers are cross-checked against 2+ independent sources where possible; single-source figures are flagged inline. China is **excluded** and noted only as a labelled aside.

> **Scope.** This is a NEUTRAL supply-side base doc for the shared library. It renders NO verdict on the Rocket Lab comms business. Its single job is to establish, for served US markets, how low an incumbent can cut price before it stops making money, because that floor (not today's retail price, and not the incumbent's all-in cost) is the number a space entrant must beat to win a served-market customer.

---

## Summary / Verdict

**Confidence: medium-high on the structure (incumbents defend down to a cash cost far below today's price, and that floor is much lower than the all-in cost a fresh ground build pays); medium on the exact marginal-cost percentages (the ~90% broadband gross margin is journalistic/operator-quoted and triangulated across several outlets, not drawn from one audited analyst breakdown).**

Three numbers carry this doc.

1. **The incumbents are high-margin and have deep room to cut.** US carrier and cable EBITDA margins cluster at **~36-41%** at the consolidated/segment level, and **broadband specifically runs at a ~80-90% gross (cash) margin** because the plant is sunk and the marginal cost of carrying a household's traffic is tiny. [FACT on the EBITDA margins; FACT-but-triangulated on the ~90% broadband gross margin.]

2. **The defend floor is the marginal cost to serve one more existing subscriber, and it is a small fraction of ARPU.** For an already-passed broadband home the incremental cash cost is roughly **10-20% of ARPU**, on the order of **~$7-15 per subscriber per month** against a ~$74 cable ARPU; the marginal cost of the data itself is **under 1 cent per GB** on a fixed network. For wireless the incremental cost is higher (mobile data costs **~$0.50-$1.50 per GB** delivered) but still far below the **~$50-57** postpaid ARPU. [ESTIMATE, from sourced margins and ARPUs.]

3. **The asymmetry versus the data-center comparison is the whole point.** In the data-center track the space alternative races a *fresh* ground build paying full freight (the orbit-to-ground ratio of 1.92x is measured against new construction). In comms the relevant competitor in a served market is an *entrenched incumbent who has already paid* and can drop price all the way to that ~10-20%-of-ARPU cash floor to defend the customer, soaking the cut out of its ~30-40 points of EBITDA room without ever going cash-negative. A space entrant that is lower than the incumbent's *all-in* cost is not automatically lower than the incumbent's *defend* cost, and the defend cost is the one that sets the winning price in served territory. [ESTIMATE, interpretation.]

**The bottom line a space entrant faces, by territory:**

| Territory | The relevant incumbent floor | What a space entrant must beat |
|---|---|---|
| **Served (fiber or upgraded cable already passes the home)** | Marginal cash cost to serve an existing sub: **~10-20% of ARPU (~$7-15/mo broadband)**; plant is sunk | A price below the incumbent's **marginal** cost, not its retail price, because the incumbent will cut to defend. This is a brutal floor. |
| **Served (wireless / mobile coverage exists)** | Incremental cost per GB **~$0.50-$1.50** plus a thin per-line cash cost, well under the **~$50-57** ARPU | Same: the carrier prices the marginal subscriber down to its incremental cost (and already wholesales spare capacity to MVNOs at exactly that logic). |
| **Unserved / underserved fringe (no incumbent plant)** | **No sunk-cost floor.** The incumbent would have to pay the full **$3,000-$200,000+ per passing** to compete | Only the space entrant's own cost. This is the one place the incumbent has no defend advantage, and it is where the addressable dollars sit (per [comms_addressable_sizing.md](./comms_addressable_sizing.md)). |

The conclusion the library should carry forward: **in served markets the price to beat is the incumbent's marginal cost (~10-20% of ARPU for fixed, ~$0.50-$1.50/GB for mobile), not today's bill; in the unserved fringe there is no such floor, which is exactly why the space-addressable opportunity is concentrated there.**

---

## 1. Incumbent Margins: How Much Room Is There to Cut?

Two margin layers matter. **EBITDA margin** (company- or segment-level) measures the cushion an incumbent can sacrifice in a price war before operating cash flow turns negative. **Broadband gross / cash margin** measures the specific service line a space entrant attacks. The first says "how much room to bleed"; the second says "where the floor actually is."

### 1.1 EBITDA margins (FY2025), all five majors

EBITDA margins are computed as adjusted EBITDA / revenue using each company's own FY2025 release. Revenue and net income are carried from the two market docs; only the EBITDA figure is newly sourced here.

| Operator | FY2025 revenue | Net income | Net margin | Adjusted EBITDA | EBITDA margin | Tag |
|---|---|---|---|---|---|---|
| **Comcast** (whole co.) | ~$123.7B | ~$20.0B | ~16% | n/a (segment basis below) | Connectivity & Platforms segment **~37-41%** | [FACT] |
| **Charter** | ~$54.8B | ~$5.0B | ~9% | ~$22.7B | **~41.4%** | [FACT] |
| **Verizon** (whole co.) | ~$138.2B | ~$17.2-17.6B | ~12% | ~$50.0B | **~36%** | [FACT] |
| **AT&T** (whole co.) | ~$125.6-125.7B | ~$21.9-22.0B | ~17-18% | ~$46.4B | **~38.6%** | [FACT] |
| **T-Mobile** (whole co.) | ~$88.3B | ~$11.0B | ~12% | ~$33.9B core adj. EBITDA | **~38% of total revenue (~47.5% of service revenue)** | [FACT] |

Sources for the newly-added EBITDA line: [Comcast 4Q2025 results](https://www.cmcsa.com/news-releases/news-release-details/comcast-reports-4th-quarter-2025-results) (Connectivity & Platforms segment Adjusted EBITDA margin ran 41.4% in Q1 easing to 37.1% in Q4 2025); [Charter FY2025 results](https://corporate.charter.com/newsroom/charter-announces-fourth-quarter-and-full-year-2025-results) and [MacroTrends CHTR EBITDA margin](https://www.macrotrends.net/stocks/charts/CHTR/charter-communications/ebitda-margin); [Verizon FY2025 results](https://www.verizon.com/about/news/verizon-delivers-2025-financial-guidance-highest-quarterly-net-adds) (~$50.0B consolidated adjusted EBITDA) with the ~36% margin corroborated by [Morningstar](https://www.morningstar.com/stocks/this-stock-offers-6-dividend-yield-looks-14-undervalued); [AT&T 4Q/FY2025 results](https://about.att.com/story/2026/4q-earnings-2025.html) (38.6% full-year adjusted EBITDA margin, ~$46.4B); [T-Mobile Q4/FY2025 results](https://www.t-mobile.com/news/business/t-mobile-q3-2025-earnings) (core adjusted EBITDA ~$33.9B on ~$71.3B service revenue). Revenue/net income carried from [comms_us_broadband_market.md](./comms_us_broadband_market.md) and [comms_us_cellular_market.md](./comms_us_cellular_market.md). **[FACT]**

**Read-off.** Every major sits at a **~36-41% EBITDA margin** at the consolidated or relevant-segment level. That is the headroom available to a defending incumbent: it can give up a large slice of price and still be operating-cash-flow positive. The net margins are lower (cable ~9-16%, telco ~12-18%) because depreciation on the sunk plant and interest on the debt that built it sit below EBITDA, but those are **sunk and fixed**, not avoidable costs of serving the next customer, so they do not set the price floor. The EBITDA line is the better read on "room to cut," and it is deep.

> **Capex-intensity note (carried, not re-derived).** These are not capex-light businesses overall: mobile-network capex runs ~14-19% of service revenue and fixed-broadband builds run thousands of dollars per home passed ([comms_cellular_5g_deployment_economics.md](./comms_cellular_5g_deployment_economics.md), [comms_broadband_deployment_economics.md](./comms_broadband_deployment_economics.md)). But that capital is spent to *build and pass*. Once a home is passed or a tower is lit, the capex is sunk; defending the customer who is already on that plant costs almost nothing more. The high capex intensity is what makes the served-market floor so low, not high: the incumbent has already paid the hard part.

### 1.2 Broadband gross / cash margin: ~80-90%

The service line a space entrant actually attacks is connectivity, and connectivity, sold over plant that already exists, is one of the highest-margin products in the economy.

| Source | Cable broadband gross / cash margin | Tag |
|---|---|---|
| [Cablefax, "How Long Will Those Broadband Margins Last?"](https://www.cablefax.com/sponsored-content/how-long-will-those-broadband-margins-last) | "trending in the **80%-90% range**" (vs ~20% video) | [FACT] industry-quoted |
| [Next TV, "MVPDs Find Margin of Victory in Broadband"](https://www.nexttv.com/features/mvpds-find-margin-of-victory-in-broadband) | margins "**hover near 90%**" (vs ~30% video) | [FACT] industry-quoted |
| [Stop the Cap / Wall Street Journal](https://stopthecap.com/2012/11/16/wall-street-journal-90-of-your-broadband-bill-is-pure-profit/) | "as much as **90 percent** of monthly broadband bills" is pure gross profit | [FACT] press |
| [HuffPost, Time Warner Cable HSI](https://www.huffpost.com/entry/time-warner-cables-97-pro_b_6591916) | Time Warner Cable high-speed internet **~97% profit margin** (illustrative single-operator) | [FACT] single example |

[FACT, triangulated across four independent outlets; the figures are operator-/journalist-quoted rather than drawn from one audited analyst-firm breakdown, so the precise number is soft, see Confidence.]

The structural reason the number is so high is in the next section: the *incremental* cost of carrying one more existing household's traffic is sub-penny per GB, so once the fixed plant and the access port exist, nearly the whole bill drops to gross profit. **This ~80-90% gross margin is the single most important number for a space entrant: it means the incumbent's cash cost to keep an existing broadband customer is only ~10-20% of what that customer pays today.** **[FACT, triangulated.]**

---

## 2. The Price Floor to Defend: Marginal Cost as a Fraction of ARPU

The competitive question the assignment poses is precise: an incumbent with sunk towers and fiber does not defend an existing customer at its *all-in* cost (which loads in the build it already paid for) and does not defend at *today's price* (which is loaded with margin). It defends at its **marginal / cash cost to serve one more existing subscriber**, the only cost it actually avoids by losing that customer. That is the floor. Below it the incumbent loses money on the customer and would rationally let them go; above it the incumbent keeps the customer and merely earns less. The space entrant's winning price must sit below that floor.

### 2.1 Fixed broadband: ~10-20% of ARPU, ~$7-15/sub/month

For an already-passed broadband home, the avoidable cost of serving one existing subscriber is the inverse of the ~80-90% gross margin from Section 1.2, plus a thin slice of usage-driven cost.

| Component of marginal cost to serve an existing fixed-broadband sub | Magnitude | Tag |
|---|---|---|
| Implied by ~80-90% gross margin (cash cost = 10-20% of revenue) | **~10-20% of ARPU** | [ESTIMATE] from Section 1.2 |
| Marginal cost of the data itself (fixed network) | **< 1 cent / GB** ("less than one cent, and falling") | [FACT] |
| Internet transit / backbone cost per GB | **fractions of a penny / GB** | [FACT] |
| Applied to cable broadband ARPU **~$73.65** ([comms_us_broadband_market.md](./comms_us_broadband_market.md)) | **~$7-15 / sub / month** cash floor | [ESTIMATE] |

The sub-penny figures: [BroadbandNow, "How Much Does Data Really Cost an ISP?"](https://broadbandnow.com/report/much-data-really-cost-isps) (Netflix's general counsel: "the marginal cost of providing an extra gigabyte of data is less than one cent, and falling"; backbone cost well below a penny per GB) and [International Center for Law & Economics, economics of data caps](https://laweconcenter.org/resources/the-economics-of-broadband-data-caps-and-usage-based-pricing/). The ARPU is carried from the broadband market doc. **[FACT for the per-GB cost; ESTIMATE for the per-sub dollar floor.]**

**So the fixed-broadband defend floor is roughly $7-15 per subscriber per month against a ~$74 bill.** A cable operator could cut a defended customer's price by half or more and still clear its cash cost. (For fiber the picture is even starker: the passing capex is already sunk, and the only success-based cost was the ~$500-700 one-time connect drop, per [comms_broadband_deployment_economics.md](./comms_broadband_deployment_economics.md); ongoing marginal cost is similarly a small fraction of ARPU.) This is the wall a space entrant hits in served territory: not the $74 list price, but a price the incumbent can take down toward ~$10-15 before it would rather walk away. **[ESTIMATE, interpretation.]**

### 2.2 Wireless / mobile: a higher per-GB cost, but still far below ARPU

Mobile is the one place the marginal cost is materially higher than fixed, because radio spectrum and RAN capacity are genuinely shared and congestible, so an extra heavy user can force real incremental capacity spend.

| Component of marginal cost to serve a mobile subscriber | Magnitude | Tag |
|---|---|---|
| Cost to deliver a GB to a device (mobile) | **~$0.50-$1.50 / GB** | [FACT] industry estimate, single-source |
| For contrast, average US retail price of cellular data | **~$4.64 / GB** (2018) | [FACT] |
| Postpaid phone ARPU (the bill being defended) | AT&T **$56.57**, T-Mobile **$50.37**, Verizon core **~$50** ([comms_us_cellular_market.md](./comms_us_cellular_market.md)) | [FACT] |

The mobile per-GB cost: [LinkedIn / Tom Allen, "How much should a gigabyte of mobile data really cost"](https://www.linkedin.com/pulse/how-much-should-gigabyte-mobile-data-really-cost-tom-allen) (~$0.50-$1.50/GB to deliver) and the retail-price contrast from [Statista cellular data price per GB](https://www.statista.com/statistics/994913/average-cellular-data-price-per-gigabyte-in-the-us/). ARPUs carried from the cellular market doc. **[FACT for the per-GB figures; the ~$0.50-1.50 delivery cost is single-source and flagged.]**

Even at the top of that range, a typical postpaid user's monthly data does not consume more than a fraction of the ~$50-57 ARPU in marginal cost. The clinching evidence that the wireless marginal cost sits far below the bill is **revealed in the market the incumbents already run**: the cable MVNOs (Comcast, Charter) buy wholesale capacity off Verizon and resell it profitably, and Verizon profits on the wholesale sale, precisely because the wholesale rate sits above Verizon's marginal cost and below retail. The carriers "monetize otherwise-spare network capacity at high incremental margin" ([comms_us_cellular_market.md](./comms_us_cellular_market.md) Section 3.2). A carrier defending a retail subscriber can price down to the same incremental floor it already accepts from an MVNO. **[FACT on the wholesale logic; ESTIMATE on the defend floor.]**

### 2.3 The floor, stated as a multiple of price

Putting the two together: the incumbents defend at a cash cost that is a **small fraction of the price they currently charge**.

| Service | Today's price (ARPU) | Marginal / cash cost to serve an existing sub | Defend floor as % of price |
|---|---|---|---|
| Fixed broadband (cable) | ~$73.65 | ~$7-15/mo | **~10-20%** |
| Mobile postpaid | ~$50-57 | data ~$0.50-1.50/GB plus thin per-line cash cost | **well under half; likely ~20-40% at typical usage** |

[ESTIMATE, derived from the sourced margins, per-GB costs, and ARPUs above. The fixed-broadband floor is the firmer of the two; the mobile floor is wider because per-subscriber usage and the incremental-capacity trigger vary.]

---

## 3. Can the Incumbent Cut to Defend, and Down to What Point?

Yes, and the magnitude is the point. The assignment asks to distinguish "lose margin" from "lose money." They are very far apart.

### 3.1 "Lose margin" vs "lose money"

| Pricing zone for the defended customer | What happens to the incumbent | Will it defend here? |
|---|---|---|
| At today's ARPU (~$74 broadband / ~$53 mobile) | Full ~80-90% broadband gross margin / ~36-41% EBITDA | Yes, obviously |
| Cut to ~50% of ARPU | Gives up half the revenue; still **deep cash-positive** (cost is only ~10-20% of original price) | Yes, willingly, to hold the customer |
| Cut toward the marginal floor (~10-20% of ARPU broadband; per-GB-plus-thin-line mobile) | Approaching break-even on **avoidable** cost; the sunk plant still does not get paid back, but no incremental cash is lost | Yes, rationally, rather than lose the customer entirely |
| Below the marginal floor | **Loses cash on every month of service** | No, would let the customer go |

The incumbent has, roughly, **30-40 percentage points of EBITDA room and ~70-80 points of broadband gross-margin room** to give up before it reaches the point where defending costs it cash. It will spend that room to defend a customer against a new entrant, because keeping a customer at a reduced margin beats losing the customer and the contribution entirely. This is standard incumbent behavior and it is why broadband and wireless price wars (promotions, retention pricing, free-line bundles) bottom out well below list but rarely go cash-negative. **[ESTIMATE, interpretation grounded in the sourced margins.]**

### 3.2 The non-price defenses stack on top

Price is not the incumbent's only weapon, and the others reinforce the floor. The wave-1 broadband doc establishes that **value plateaus on reach and reliability, not raw speed** (willingness-to-pay for a megabit collapses ~100x past 100 Mbps; ~70% of homes refuse gigabit even when offered), and that **fiber/cable beat satellite on latency and price-per-quality in head-to-head served settings** ([comms_us_broadband_market.md](./comms_us_broadband_market.md) Section 3; [comms_broadband_deployment_economics.md](./comms_broadband_deployment_economics.md) Section 6A). So in served territory the incumbent can often hold the customer **without even reaching its price floor**, on switching costs, bundle lock-in, and a latency/quality edge. The marginal-cost floor is the *worst case* for the incumbent, the price it could go to if forced; the realistic defense rarely needs to go that far. **[ESTIMATE, interpretation.]**

---

## 4. The Asymmetry Versus the Data-Center Comparison

This is the conceptual core of the wave-3 supply-side question, and it is where comms diverges sharply from the data-center track.

### 4.1 What the data-center ratio measures

The data-center track's headline is an **orbit-to-ground cost ratio of ~1.92x**: delivering compute from orbit costs roughly 1.92x what it costs to deliver the same compute from a *new* terrestrial data center. Critically, the ground side of that ratio is a **fresh build paying full freight**, land, power, cooling, GPUs, construction, all incurred at par with the orbital alternative. Both sides of the ratio are greenfield. The competitor is a hyperscaler who must still build the thing.

### 4.2 Why comms is different: the competitor has already paid

In communications, in any **served** market, the competitor is not a fresh build. It is an **entrenched incumbent whose plant is already in the ground and already depreciating**. That changes the comparison in one decisive way:

| | Data-center comparison | Comms served-market comparison |
|---|---|---|
| Who is the ground competitor? | A **new** hyperscaler build | An **existing** incumbent (Comcast, Charter, Verizon, AT&T, T-Mobile) |
| What cost does the ground side bear to compete for the marginal customer? | **Full all-in** build cost (land, power, GPUs, construction) | **Only marginal cost** to serve one more existing sub (~10-20% of ARPU fixed; ~$0.50-1.50/GB mobile) |
| What must the space entrant beat? | The ground build's **all-in** delivered cost | The incumbent's **marginal** cost, far below the incumbent's own all-in or list price |
| Is the ground competitor's sunk cost relevant to the price war? | Yes, it is being incurred now | **No.** It is sunk; it does not set the defend price |

[ESTIMATE, structural interpretation; the 1.92x data-center ratio is carried from the data-center track and not re-derived here.]

The asymmetry: **a space entrant that is cheaper than the incumbent's all-in cost is not necessarily cheaper than the incumbent's defend cost.** In the data-center case, being cheaper all-in than a new build is enough to win, because the new build has no sunk-cost advantage to fall back on. In the comms served-market case, the incumbent has already paid the expensive part and can drop to a cash floor of ~10-20% of ARPU, a floor the space entrant's *own* all-in cost (constellation capex amortized across a sliver of capacity, plus an optical/RF ground segment) is very unlikely to undercut. The incumbent's sunk investment, which is irrelevant to the data-center price war, becomes a near-impregnable moat in the comms served-market price war.

### 4.3 Where the asymmetry disappears: the unserved fringe

The incumbent's advantage is entirely a function of **already having plant in that location**. Where it does not, the advantage vanishes and the comparison flips back toward the data-center shape:

- In the **unserved / underserved fringe**, the incumbent has **no sunk infrastructure**. To compete for that customer it would have to pay the **full per-passing cost**, which runs **$3,000-$6,000 rural and up to ~$200,000-$230,000 in the extreme remote tail**, against an ARPU of only ~$50-150/month ([comms_broadband_deployment_economics.md](./comms_broadband_deployment_economics.md) Sections 5-6). That build case never closes without subsidy.
- There, the incumbent has **no marginal-cost floor to undercut the entrant with**, because it has no marginal customer on existing plant; it has only the same all-in greenfield cost the space entrant faces, and on a per-passing basis the terrestrial number is often **orders of magnitude worse**.
- This is precisely the territory the addressable-sizing doc identifies as the space-addressable pool: the developed-world rural fringe, the mobility/enterprise verticals (maritime, aviation, energy, remote-government), and the open sovereign layer, **~$45-60B/yr conservative to ~$110-150B/yr optimistic, ex-China** ([comms_addressable_sizing.md](./comms_addressable_sizing.md)). The reason the dollars sit there and not in served markets is exactly the floor asymmetry this doc quantifies.

So the two findings lock together: **the incumbent's marginal-cost floor is a wall in served markets and is absent in the fringe, which is why the honestly-sized space-addressable opportunity is concentrated in the fringe.** [ESTIMATE, interpretation; the addressable band and the per-passing costs are carried from the cited docs.]

---

## 5. The Price a Space Entrant Must Beat (Conclusion, no verdict)

Synthesizing Sections 1-4 into the single number the assignment asks for, by territory:

| Territory | Price a space entrant must beat to win share | Basis |
|---|---|---|
| **Served fixed broadband** | The incumbent's **marginal cost, ~10-20% of ARPU (~$7-15/sub/mo)**, not the ~$74 list price | ~80-90% broadband gross margin (Section 1.2); sub-penny/GB data cost (Section 2.1) |
| **Served mobile** | The incumbent's **incremental cost, ~$0.50-$1.50/GB plus a thin per-line cash cost**, well under the ~$50-57 ARPU | mobile per-GB delivery cost; the MVNO wholesale floor the carriers already accept (Section 2.2) |
| **Unserved / underserved fringe** | **No incumbent floor at all**; only the space entrant's own delivered cost competes, because the incumbent would have to pay $3,000-$200,000+ per passing to enter | the density cliff; absence of sunk plant (Section 4.3) |

**The neutral one-line read for the library (no verdict):** to take share in a **served** US communications market, a space entrant must price below the incumbent's **marginal cost to defend** (roughly **10-20% of ARPU for fixed broadband**, an incremental **~$0.50-$1.50/GB for mobile**), because the incumbent has already sunk its plant and can cut to that cash floor while soaking the loss out of ~30-40 points of EBITDA room; in the **unserved fringe** there is **no such floor**, because the incumbent has no sunk infrastructure there, which is why the space-addressable dollars concentrate in the fringe rather than in served markets. Whether a Rocket Lab comms cost stack can clear either bar is a separate, space-side supply question this doc does not answer.

---

## Sources

*EBITDA margins (newly sourced for this doc)*
- [Comcast, 4th Quarter and Full-Year 2025 Results](https://www.cmcsa.com/news-releases/news-release-details/comcast-reports-4th-quarter-2025-results) (Connectivity & Platforms segment Adjusted EBITDA margin ~37-41% across 2025)
- [Comcast, 3rd Quarter 2025 Results](https://www.cmcsa.com/news-releases/news-release-details/comcast-reports-3rd-quarter-2025-results)
- [Charter, Fourth Quarter and Full Year 2025 Results](https://corporate.charter.com/newsroom/charter-announces-fourth-quarter-and-full-year-2025-results) (Adjusted EBITDA ~$22.7B on ~$54.8B revenue → ~41.4%)
- [MacroTrends, Charter Communications EBITDA Margin](https://www.macrotrends.net/stocks/charts/CHTR/charter-communications/ebitda-margin)
- [Verizon, Delivers on 2025 Financial Guidance](https://www.verizon.com/about/news/verizon-delivers-2025-financial-guidance-highest-quarterly-net-adds) (consolidated adjusted EBITDA ~$50.0B)
- [Morningstar, Verizon 6% dividend / valuation (consolidated EBITDA margin ~36%)](https://www.morningstar.com/stocks/this-stock-offers-6-dividend-yield-looks-14-undervalued)
- [AT&T, Strong Fourth-Quarter and Full-Year 2025 Financial Performance](https://about.att.com/story/2026/4q-earnings-2025.html) (full-year adjusted EBITDA margin 38.6%, ~$46.4B)
- [T-Mobile, Q3 2025 / full-year 2025 results](https://www.t-mobile.com/news/business/t-mobile-q3-2025-earnings) (core adjusted EBITDA ~$33.9B on ~$71.3B service revenue → ~47.5% of service revenue, ~38% of total)

*Broadband gross / cash margin and marginal cost to serve*
- [Cablefax, How Long Will Those Broadband Margins Last?](https://www.cablefax.com/sponsored-content/how-long-will-those-broadband-margins-last) (broadband margins 80-90% vs ~20% video)
- [Next TV, MVPDs Find Margin of Victory in Broadband](https://www.nexttv.com/features/mvpds-find-margin-of-victory-in-broadband) (broadband margins near 90% vs ~30% video)
- [Stop the Cap / Wall Street Journal, 90% of Your Broadband Bill is Pure Profit](https://stopthecap.com/2012/11/16/wall-street-journal-90-of-your-broadband-bill-is-pure-profit/)
- [HuffPost, Time Warner Cable's 97% Broadband Profit Margin](https://www.huffpost.com/entry/time-warner-cables-97-pro_b_6591916)
- [BroadbandNow, How Much Does Data Really Cost an ISP?](https://broadbandnow.com/report/much-data-really-cost-isps) (fixed marginal cost < 1 cent/GB; mobile ~$0.50-$1.50/GB)
- [International Center for Law & Economics, The Economics of Broadband Data Caps and Usage-Based Pricing](https://laweconcenter.org/resources/the-economics-of-broadband-data-caps-and-usage-based-pricing/)
- [LinkedIn / Tom Allen, How much should a gigabyte of mobile data really cost](https://www.linkedin.com/pulse/how-much-should-gigabyte-mobile-data-really-cost-tom-allen)
- [Statista, Cellular data average price per GB in the US](https://www.statista.com/statistics/994913/average-cellular-data-price-per-gigabyte-in-the-us/)

*Library docs this doc builds on (each carries its own underlying citations)*
- [research/economics/comms_us_broadband_market.md](./comms_us_broadband_market.md)
- [research/economics/comms_us_cellular_market.md](./comms_us_cellular_market.md)
- [research/economics/comms_cellular_5g_deployment_economics.md](./comms_cellular_5g_deployment_economics.md)
- [research/economics/comms_broadband_deployment_economics.md](./comms_broadband_deployment_economics.md)
- [research/economics/comms_addressable_sizing.md](./comms_addressable_sizing.md)

---

## Confidence

- **EBITDA margins (Section 1.1): high.** Each is computed from the company's own FY2025 release and cross-checked (Charter against MacroTrends; Verizon's margin against Morningstar). The ~36-41% clustering is firm. Note Comcast is given on a segment basis (Connectivity & Platforms) rather than whole-company, and T-Mobile's ~47.5% is on service revenue (~38% on total revenue including equipment), both stated explicitly so they are not misread.
- **Broadband ~80-90% gross margin (Section 1.2): medium-high but triangulated, not audited.** Four independent outlets converge on 80-90%, and the structural logic (sub-penny/GB marginal data cost over sunk plant) independently supports it. But these are operator-/journalist-quoted figures, not a single audited analyst-firm decomposition, and several of the press sources are older (the Time Warner 97% example and the WSJ 90% piece predate 2015). The *direction and magnitude* are robust; the exact percentage is soft. The lead should treat ~90% as "high gross margin, order-of-magnitude correct," not a precise constant. **Flagged.**
- **Marginal-cost-as-%-of-ARPU and the per-sub dollar floors (Section 2): medium.** The fixed-broadband ~10-20%/~$7-15 floor is a clean inverse of the gross margin applied to a filed ARPU and is the firmer figure. The mobile ~$0.50-$1.50/GB delivery cost is **single-source** (one industry commentator) and should be corroborated; it is consistent in magnitude with the carriers' willingness to wholesale to MVNOs, which is the cross-check used here.
- **The asymmetry argument (Section 4): medium-high on the logic, inherited on the inputs.** The structural claim (sunk incumbent floor in served markets, no floor in the fringe) follows directly from the sourced margins and the deployment-cost docs. The 1.92x data-center ratio and the per-passing costs are carried from other tracks/docs and not independently re-verified here.

---

## Open Questions

1. **An audited broadband-margin decomposition.** The ~80-90% gross margin is triangulated from press and operator quotes. A current analyst-firm (MoffettNathanson, LightShed) or operator segment-level cost build that isolates broadband cost-of-service per subscriber would replace the soft ~90% with a hard number and tighten the ~$7-15/mo floor.
2. **The mobile per-GB delivery cost.** The ~$0.50-$1.50/GB figure is single-source. A second independent estimate (or a carrier-disclosed cost-per-GB / incremental-cost figure) would firm the wireless floor, which is currently the wider of the two.
3. **The actual MVNO wholesale rate.** The carriers' wholesale rate to the cable MVNOs is the cleanest real-world proxy for the wireless marginal-cost floor, but the precise per-GB / per-line rate is not public ([comms_us_cellular_market.md](./comms_us_cellular_market.md) flags the same gap). A sourced wholesale rate would let the library state the mobile defend floor as a hard number rather than a range.
4. **How aggressively incumbents actually price to defend against satellite specifically.** This doc establishes the floor the incumbent *could* go to. Whether they discount that far in practice against a LEO/space competitor (versus relying on the latency/quality and bundle defenses in Section 3.2) is a behavioral question worth a market-conduct scan as direct-to-cell and LEO broadband scale.
5. **Where exactly the served/unserved boundary sits for pricing.** Section 4.3 treats it as binary (plant exists or it does not), but FWA and the BEAD-driven fiber build are actively moving the line. The precise count of locations that flip from "no incumbent floor" to "incumbent floor" as terrestrial build-out continues directly sizes the fringe a space entrant can win without facing a marginal-cost wall, and ties to the open questions in [comms_broadband_deployment_economics.md](./comms_broadband_deployment_economics.md) and [comms_addressable_sizing.md](./comms_addressable_sizing.md).

---

## Claims

| COMM- id | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-080 | Comcast Connectivity & Platforms segment Adjusted EBITDA margin, 2025 | ~37-41% (41.4% Q1 → 37.1% Q4) | [FACT] | Comcast 4Q2025 results |
| COMM-081 | Charter Adjusted EBITDA margin, FY2025 | ~41.4% (~$22.7B / ~$54.8B) | [FACT] | Charter FY2025; MacroTrends |
| COMM-091 | Verizon consolidated adjusted EBITDA / margin, FY2025 | ~$50.0B / ~36% | [FACT] | Verizon FY2025; Morningstar |
| COMM-092 | AT&T adjusted EBITDA / margin, FY2025 | ~$46.4B / ~38.6% | [FACT] | AT&T 4Q/FY2025 results |
| COMM-093 | T-Mobile core adjusted EBITDA / margin, FY2025 | ~$33.9B; ~47.5% of service rev (~38% of total rev) | [FACT] | T-Mobile FY2025 results |
| COMM-094 | Cable broadband gross / cash margin | ~80-90% (single example up to ~97%) | [FACT] triangulated, not audited; some sources pre-2015 | Cablefax; Next TV; Stop the Cap/WSJ; HuffPost |
| COMM-095 | Marginal cost of data, fixed broadband network | < 1 cent / GB (transit fractions of a penny) | [FACT] | BroadbandNow; ICLE |
| COMM-096 | Marginal cost of data, mobile network (delivered to device) | ~$0.50-$1.50 / GB | [FACT] single-source, flagged | LinkedIn/Tom Allen; cross-checked vs MVNO wholesale logic |
| COMM-097 | Average US retail cellular data price (contrast to marginal cost) | ~$4.64 / GB (2018) | [FACT] | Statista |
| COMM-098 | Fixed-broadband marginal cost to serve an existing sub, as % of ARPU | ~10-20% of ARPU (~$7-15/sub/mo vs ~$73.65 ARPU) | [ESTIMATE] | derived from COMM-094/095 + broadband-market ARPU |
| COMM-099 | Incumbent EBITDA headroom available to absorb a defensive price cut | ~30-40 pts EBITDA / ~70-80 pts broadband gross margin | [ESTIMATE] | derived from COMM-080/081/091/092/093/094 |
| COMM-100 | Served-market price a space entrant must beat (fixed) | incumbent marginal cost ~10-20% of ARPU, not the ~$74 list price | [ESTIMATE] interpretation | this doc, Sections 2-5 |
| COMM-101 | Served-market price a space entrant must beat (mobile) | incumbent incremental cost ~$0.50-$1.50/GB + thin per-line cost, well under ~$50-57 ARPU | [ESTIMATE] interpretation | this doc, Sections 2-5 |
| COMM-102 | Unserved-fringe incumbent floor | none; incumbent would pay full $3,000-$200,000+ per passing to compete | [ESTIMATE] interpretation | this doc S4.3; comms_broadband_deployment_economics.md |
| COMM-103 | Comms-vs-data-center asymmetry | served-market competitor is an entrenched incumbent pricing to marginal cost, not a fresh build paying full freight (data-center 1.92x ground side is greenfield) | [ESTIMATE] interpretation | this doc, Section 4 |
