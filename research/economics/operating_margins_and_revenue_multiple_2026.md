# Operating Margins, Gross Margins, and the Revenue-to-Cost Multiple (R): Is R = 1.5 Fair? (2026)

*Research date: 2026-06-01. Prepared for the Rocket Lab orbital AI-inference data center feasibility project. Companion to and partial update of `economics/hyperscaler_margins.md`, `economics/revenue_economics_2026.md`, `economics/gpu_hour_rental_rates.md`, `economics/revenue_per_watt.md`, and `economics/premium_value_case.md`. Supersedes the stale Oracle "30-40% margin" figure carried in `revenue_economics_2026.md`.*

> **Purpose.** The orbital model prices compute revenue as **R times the node's annualized build-and-launch cost** (amortized CAPEX, divided by service life; the orbital model has near-zero opex because solar is free and there is no grid bill). R is a configurable band: **low 1.2, central 1.5, high 1.8**. R = 1.5 means revenue is 150% of amortized cost, which is a **33.3% gross margin** over that cost base. This document answers four founder questions: (a) what an operating margin is and how it differs from a gross margin and from a cost-plus markup; (b) whether rapid scaling by ground operators is compressing their operating margins; (c) what revenue-to-cost (price-to-cost) multiples ground / GPU-cloud operators actually run; and (d) whether R = 1.5 is a fair, defensible central assumption.

> **Reading guide.** Claims are tagged **[FACT]** (company-disclosed or reported 2025-26 data), **[DERIVED]** (our arithmetic), or **[INFERENCE]** (our reasoning, explicitly not an external fact). Hard numbers are cross-checked against 2+ independent sources and cited inline with URLs. Where a number is an estimate for a private or opaque figure it is marked **[ESTIMATE]**.

---

## BLUF: Is R = 1.5 fair?

**Yes. R = 1.5 (a 33.3% gross markup over amortized build-and-launch cost) is a fair, defensible central assumption, and is arguably mildly conservative for a high-demand, scarcity-priced compute service that is sold as a differentiated owner-operator product.** The single most important framing point: **R is a markup over the node's amortized CAPEX, which makes it a gross-margin-shaped number (close to a cost-of-revenue gross margin), NOT a bottom-line operating or net margin.** Real GPU-cloud operators run *reported* gross margins of roughly 30% (Oracle OCI AI capacity, ~32% in Q3 FY2026, guided 30-40%) up to ~70% (CoreWeave, 71.7% FY2025) once they decide how much depreciation to push below the cost-of-revenue line; their *operating* margins are far thinner and currently compressed by rapid scaling (CoreWeave ~ -0.9% FY2025; Oracle's AI-server-rental deals averaged ~16% deal-level profit and lost money on the newest Blackwell chips). A 33.3% gross margin sits squarely inside the disclosed gross-margin band of the comparable layer and below the mature hyperscaler-cloud operating margins (AWS ~35-38%, Azure/Intelligent Cloud ~45%, Google Cloud 32.9% in Q1 2026). The band edges map cleanly to reality: **R = 1.2 (16.7% gross margin) is the thin-operator / Oracle-deal-level / commodity-rental floor; R = 1.8 (44.4% gross margin) is the strong-pricing-power / mature-hyperscaler-cloud ceiling.** R = 1.5 is the well-centered midpoint. **Confidence: high** on the markup-vs-margin distinction and the disclosed operator gross/operating margins (multiple primary sources); **moderate** on the precise mapping of R to a lifetime price-to-cost multiple, because R is defined over *amortized CAPEX* whereas operator gross margins are defined over *cost of revenue*, and the two cost bases are not identical (see Open Question 1).

---

## 1. Gross margin vs operating margin vs net margin: precise definitions

The founder's first question. These three margins differ only in *which costs* are subtracted from revenue before dividing by revenue. Each is a percentage of **revenue** (the denominator is always revenue).

| Margin | Formula | What is subtracted | What it tells you |
|---|---|---|---|
| **Gross margin** | (Revenue − COGS) / Revenue | Only **cost of goods/revenue (COGS)**: the direct cost of producing/delivering the service | How profitable each unit of service is *before* running the business |
| **Operating margin** | Operating income / Revenue | COGS **plus** all **operating expenses (opex)**: SG&A, sales & marketing, R&D, admin, rent | How profitable the *core business operation* is, before financing and tax |
| **Net margin** | Net income / Revenue | COGS + opex **plus** interest, taxes, and all non-operating items | What the company actually keeps for shareholders |

Sources: [Britannica Money: Profit Margin Types](https://www.britannica.com/money/profit-margin-types), [CloudZero: SaaS Gross Margin](https://www.cloudzero.com/blog/saas-gross-margin/), [The Rich Guy Math: Operating Margin](https://therichguymath.com/operating-margin-guide/), [Wikipedia: Gross margin](https://en.wikipedia.org/wiki/Gross_margin).

**What COGS includes for a compute / cloud business [FACT].** COGS (cost of revenue) is the cost incurred in *delivering* the service. For a cloud / GPU-rental operator the cost of revenue typically includes: **the depreciation of the servers/GPUs, data-center lease or power, cooling, networking, and the direct labor and direct costs of operating the facility.** A widely-used practical test: *"Can my customers still use the service if I don't pay that expense?"* If no, it belongs in COGS / gross margin ([CloudZero](https://www.cloudzero.com/blog/saas-gross-margin/), [Chargebee: SaaS Gross Margin](https://www.chargebee.com/resources/glossaries/saas-gross-margin/)). The single most contested line is **GPU/server depreciation**: it is a real cost of delivering the service and belongs in COGS, but operators frequently report a "gross margin" that pushes much of it below the line, which is why neocloud reported gross margins look high while true economics are thin (see §2).

**What opex (the gross-to-operating gap) includes [FACT].** Operating expenses are the costs of *running the company* that are not tied to delivering a single unit: **sales & marketing, R&D, general & administrative, executive, and corporate overhead** ([The Rich Guy Math](https://therichguymath.com/operating-margin-guide/), [CloudZero: Margin Analysis](https://www.cloudzero.com/blog/margin-analysis/)). Operating margin = gross margin minus these.

**Why this matters for the orbital model [INFERENCE].** The orbital node has an unusual cost structure: **its cost of revenue is dominated by the amortized CAPEX (the depreciation of the build-and-launch cost over the service life), and it has near-zero opex** (solar power is free, there is no grid bill, no water, no data-center lease, and minimal on-orbit labor). So for the orbital node, **gross margin and operating margin are much closer together than for a terrestrial operator**, because the big terrestrial gross-to-operating wedge (power, lease, large facility staff) is largely absent. This is a genuine structural feature, not a modeling shortcut: in orbit the depreciation IS most of the cost, so R-over-amortized-CAPEX captures the bulk of the real cost base. (The model still must, separately, net financing cost, tax, and the cash CAPEX timing below the line to reach an investor return, exactly the gap `review_economist.md` Findings 1-2 flag for the company-level valuation model. R itself is a gross-margin-shaped operating input, not a bottom-line return.)

---

## 2. Cost-plus markup vs gross margin: the exact relationship (and why R = 1.5 = 33.3% margin)

The founder's model uses R as a **multiplier on cost** (revenue = R × amortized cost). That is a **cost-plus markup**, and it converts to a gross *margin* by a fixed formula. Confusing the two is a classic and costly error.

- **Markup** is profit as a percentage of **cost**. R = 1.5 means a **50% markup** (revenue is 1.5× cost, i.e. cost + 50% of cost).
- **Margin** is profit as a percentage of **revenue (price)**.
- Conversion: **Margin = Markup / (1 + Markup)**. So a 50% markup = 0.50 / 1.50 = **33.3% margin**. ([inFlow: Margin vs Markup](https://www.inflowinventory.com/blog/calculate-margin-vs-markup/), [Patriot Software: Margin vs Markup chart](https://www.patriotsoftware.com/blog/accounting/margin-vs-markup-chart-infographic/), [Calculator Academy: Markup to Margin](https://calculator.academy/markup-to-margin-calculator/)).

This is exactly the relationship the founder already understands and is the arithmetic backbone of R. The full band converts as follows [DERIVED]:

| R (revenue / cost) | Markup over cost | Gross margin (profit / revenue) |
|---|---|---|
| **1.2** (low) | +20% | **16.7%** |
| **1.5** (central) | +50% | **33.3%** |
| **1.8** (high) | +80% | **44.4%** |
| *(reference)* 1.1 | +10% | 9.1% |
| *(reference)* 1.9 | +90% | 47.4% |

**The crucial distinction the founder asked for, in one line:** R is a **cost-plus markup that equals a gross margin** (33.3% at R = 1.5): it is a top-of-the-P&L number measured against the cost of delivering the service. It is **not** an operating margin (which would further subtract SG&A/R&D/corporate overhead) and **not** a net margin (which would further subtract interest and tax). Because the orbital node has minimal opex, its operating margin would be *close to* its gross margin, but at the *company* level the venture still pays financing and tax below the line, so R = 1.5 must not be read as a 33% bottom-line return. R = 1.5 is the cost-plus *gross* markup; the bottom-line return is lower and is the subject of the separate valuation model.

---

## 3. What ground / GPU-cloud operators actually earn: sourced margins (2024-2026)

This is the founder's questions (b) and (c). The table separates **gross margin** (cost-of-revenue basis, comparable to R) from **operating margin** (after opex) and adds the implied **revenue-to-cost multiple** where it can be derived. All figures are 2024-2026.

| Operator (layer) | Gross margin | Operating margin | Implied revenue/cost multiple | Source(s) |
|---|---|---|---|---|
| **NVIDIA** (chip) | **71.1% TTM** (≈71-76% range) | **60.4% TTM** | chip sells ~8-10× over BOM | [Yahoo Finance: Oracle/Nvidia margin compare](https://finance.yahoo.com/news/oracle-stock-falls-report-reveals-155035349.html); [hyperscaler_margins.md](./hyperscaler_margins.md) |
| **AWS** (cloud segment) | n/d (segment) | **~35-38%** (Q1 2026 op income $14.16B, +23% YoY) | n/a (blended cloud) | [CNBC: AWS Q1 2026](https://www.cnbc.com/2026/04/29/aws-earnings-q1-2026.html); [HeyGoTrade: hyperscaler race 2026](https://www.heygotrade.com/en/blog/aws-vs-google-cloud-vs-azure-hyperscaler-race/) |
| **Microsoft Intelligent Cloud / Azure** | n/d | **~45%+** (watched for compression below 45%) | n/a | [HeyGoTrade: cloud growth signal Q1 2026](https://www.heygotrade.com/en/blog/reading-cloud-growth-signal-azure-gcp-aws-q1-2026/) |
| **Google Cloud** | n/d | **32.9%** (Q1 2026, up from 17.8% Q1 2025; op income $6.6B on $20.0B rev, +63% YoY) | n/a | [Investing.com: Alphabet Q1 2026](https://www.investing.com/news/company-news/alphabet-q1-2026-slides-cloud-surges-63-ai-investments-accelerate-93CH-4654872); [LevelHeaded Investing: Alphabet Q1 2026](https://www.levelheadedinvesting.com/p/alphabet-inc-google-q1-2026-results-cloud-breaks-escape-velocity-multiple-catches-up) |
| **Oracle OCI (AI capacity / GPU rental)** | **~32% (Q3 FY2026); 14-16% realized on actuals**; guided 30-40% | **~16% deal-level**; **negative on newest Blackwell** | **~1.16-1.19× (gross); ~1.0× or below after depreciation** | [Computer Weekly: Oracle 30-40% OCI](https://www.computerweekly.com/news/366636165/Oracle-expects-to-increase-OCI-margins-by-30-40); [Futurum: Oracle Q3 FY2026](https://futurumgroup.com/insights/oracle-q3-fy-2026-earnings-driven-by-oci-ai-infrastructure-demand/); [Yahoo Finance: thin margins report](https://finance.yahoo.com/news/oracle-stock-falls-report-reveals-155035349.html); [Digitimes: Oracle 14% gross margin](https://www.digitimes.com/news/a20251008PD224/oracle-cloud-computing-business-gross-margin-revenue.html); [Seeking Alpha: Oracle GPU-rental documents](https://seekingalpha.com/news/4502414-oracles-documents-show-financial-challenges-of-renting-out-nvidias-chips) |
| **CoreWeave** (neocloud) | **71.7%** (FY2025) | **-0.9%** (FY2025); **1.0%** adj. op margin Q1 FY2026 (trough), down from 17.0% Q1 FY2025 | **~3.5×** lifetime on list pricing [ESTIMATE]; **~1.0× operating** today | [StockTitan: CRWV financials](https://www.stocktitan.net/financials/CRWV/); [Futurum: CoreWeave Q1 FY2026](https://futurumgroup.com/insights/coreweave-q1-fy-2026-capacity-constraints-amid-accelerating-ai-demand/); [Motley Fool: CoreWeave's "weirdly high" gross margin](https://www.fool.com/investing/2025/10/29/the-hidden-truth-behind-coreweaves-weirdly-high-gr/) |
| **CoreWeave (long-term target)** | n/d | **25-30%** (management long-term adj. op income target) | **~1.33-1.43×** at target [DERIVED] | [Futurum: CoreWeave Q1 FY2026](https://futurumgroup.com/insights/coreweave-q1-fy-2026-capacity-constraints-amid-accelerating-ai-demand/); [LongYield: CoreWeave economics](https://longyield.substack.com/p/coreweave-after-results-hypergrowth) |
| **Nebius** (neocloud) | **~74%** (cost of revenue fell to 26% of revenue in Q1 2026, from 49% Q1 2025) | **negative** (loss from operations widened to $361.7M Q1 2026); ~40% adj. EBITDA target 2026 | rising toward profitability | [Nebius 6-K FY2026 (SEC)](https://www.sec.gov/Archives/edgar/data/0001513845/000110465926059872/tm2614392d1_ex99-2.htm) |
| **Rocket Lab** (whole company, reference) | **34.4% GAAP** (FY2025) | **~ -38% GAAP** (FY2025 op loss ~$229M) | n/a | [hyperscaler_margins.md](./hyperscaler_margins.md) |

**The GPU-rental revenue-to-cost multiple, sized directly [FACT/DERIVED].** The cleanest published bottom-up multiple for renting GPUs is NextPlatform's analysis: a 16,000-GPU cluster costs ~$1.5B all-in ($800M GPUs + $700M data center/networking) and bills ~$5.27B over 4 years at blended AWS pricing (~$9.40/GPU-hr), a **~3.5× revenue-to-cost multiple over the asset life** ([NextPlatform: How to make more money renting a GPU than Nvidia makes selling it](https://www.nextplatform.com/2024/05/02/how-to-make-more-money-renting-a-gpu-than-nvidia-makes-selling-it/)). But that uses *list* AWS pricing; at *realized* neocloud pricing the multiple is far lower. A cleaner per-unit anchor [FACT]: an H100 (~$25-40k) must rent **above ~$2.85/hr to beat a stock-market IRR** and **below ~$1.65/hr it no longer recoups its investment** at all; at ~$2.50/hr it breaks even on the bare GPU in ~14-16 months of full utilization ([IntuitionLabs: NVIDIA GPU pricing](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide), [GMICloud: H100 rent vs buy 2026](https://www.gmicloud.ai/en/blog/nvidia-h100-gpu-pricing-2026-rent-vs-buy-cost-analysis), [Silicon Data: H100 rental price over time](https://www.silicondata.com/blog/h100-rental-price-over-time)). The break-even-to-IRR-clearing band (~$1.65 to ~$2.85/hr) is itself roughly a **1.0× to 1.7× revenue-to-bare-GPU-cost** spread, which brackets R = 1.5 almost exactly.

**Read-through for R [INFERENCE].** Three reference multiples bound the question:
1. **Thin/commodity rental layer (Oracle OCI realized, CoreWeave operating today):** revenue-to-cost ~**1.0-1.2×** (breakeven to ~16% margin). This is the floor, and it maps to **R = 1.2 (16.7% margin)**.
2. **Durable owner-operator target (CoreWeave 25-30% long-term op margin):** ~**1.33-1.43×**. R = 1.5 sits just above this, appropriate, because R is a *gross* markup (pre-opex) while CoreWeave's 25-30% is an *operating* target (post-opex), and a gross markup should sit above the operating margin of the same business.
3. **Mature, scarcity-priced cloud (hyperscaler cloud operating margins 33-49%; reported neocloud gross margins ~70%):** ~**1.5-2.0×**. R = 1.8 (44.4% margin) sits at the operating-margin ceiling of mature hyperscaler cloud and well below reported neocloud gross margins.

R = 1.5 (33.3% gross margin, 1.5× revenue-to-cost) lands between the durable-operator-target and the mature-cloud ceiling: a defensible center.

---

## 4. The scaling effect: is rapid growth compressing operators' margins? (founder question b)

**Yes, but the compression is in OPERATING margin, not gross margin, and it is a timing artifact of rapid CAPEX, not a structural collapse of unit economics. The split is exactly the gross-vs-operating distinction.** [FACT]

**The mechanism [FACT].** When a GPU-cloud operator scales fast, depreciation, lease, and power costs begin *the moment capacity is energized*, but customer workloads take time to fill the new capacity. CoreWeave described this as a timing mismatch that pressures margin during rapid expansion, "especially when new capacity added is large relative to the installed base" ([Futurum: CoreWeave Q1 FY2026](https://futurumgroup.com/insights/coreweave-q1-fy-2026-capacity-constraints-amid-accelerating-ai-demand/)). The result is a dramatic operating-margin compression even as gross margin holds:

- **CoreWeave:** adjusted operating income margin fell from **17.0% (Q1 FY2025) to 1.0% (Q1 FY2026)**, with management explicitly flagging Q1 2026 as the *trough*, while *gross* margin stayed high (~71% FY2025). 2026 capex guidance is **$30-35B against $12-13B revenue** (capex ~2.5× revenue). Management's long-term adjusted operating-income target is **25-30%** ([Futurum](https://futurumgroup.com/insights/coreweave-q1-fy-2026-capacity-constraints-amid-accelerating-ai-demand/), [StockTitan](https://www.stocktitan.net/financials/CRWV/), [tech-insider: CoreWeave $30B capex](https://tech-insider.org/coreweave-30-billion-capex-ai-cloud-2026/)).
- **Nebius:** loss from operations *widened* (to $361.7M in Q1 2026) as it scaled, even as *cost of revenue fell from 49% to 26% of revenue* (gross margin improving from ~51% to ~74%): gross economics improving, operating line still negative on buildout. D&A rose 332% YoY ([Nebius 6-K FY2026, SEC](https://www.sec.gov/Archives/edgar/data/0001513845/000110465926059872/tm2614392d1_ex99-2.htm)).
- **Oracle OCI:** AI-server-rental revenue tripled YoY to ~$900M (T3M ending Aug 2025) but realized gross margin was only ~14-16%, and Oracle *lost ~$100M on the newest Blackwell rentals* specifically (discounting, high power/refresh costs, and variable utilization compressing the new-capacity margin) ([Seeking Alpha](https://seekingalpha.com/news/4502414-oracles-documents-show-financial-challenges-of-renting-out-nvidias-chips), [Digitimes](https://www.digitimes.com/news/a20251008PD224/oracle-cloud-computing-business-gross-margin-revenue.html)).

**The counter-case: hyperscalers' cloud operating margins are EXPANDING, not compressing [FACT].** The integrated hyperscalers, scaling just as fast, show the opposite: **Google Cloud operating margin nearly doubled from 17.8% (Q1 2025) to 32.9% (Q1 2026)** ([Investing.com: Alphabet Q1 2026](https://www.investing.com/news/company-news/alphabet-q1-2026-slides-cloud-surges-63-ai-investments-accelerate-93CH-4654872)); AWS operating income rose ~23% YoY with margin ~35-38% ([CNBC](https://www.cnbc.com/2026/04/29/aws-earnings-q1-2026.html)); Azure/Intelligent Cloud held ~45%+. The difference: hyperscalers spread huge fixed software and customer-relationship value over the new capacity and buy silicon at maximum scale, so operating leverage *improves* with growth. The pure GPU-rental neoclouds have no such software moat, so their operating margin is exposed to the raw depreciation-timing wedge.

**Implication for R [INFERENCE].** The scaling effect is a caution about the *operating/net* line, not about R itself. R is a *gross* markup; the disclosures confirm gross economics are robust (Oracle 30-40% guided, CoreWeave/Nebius ~70%+ reported) even while operating margins are temporarily compressed by buildout. **The orbital model is partly insulated from this specific compression** because it has near-zero opex and no ground-power bill, so the terrestrial gross-to-operating wedge (power/lease/large staff) is mostly absent. **But the orbital model is fully exposed to the underlying driver, depreciation timing**, because its CAPEX (build + launch) is enormous and front-loaded and it cannot refresh silicon. This is precisely why `review_economist.md` Finding 1 insists depreciation be charged on *deployed capital* (full straight-line), not on the attrition-weighted live fleet: the same depreciation-timing reality that compresses CoreWeave's operating margin must be honestly charged against the orbital node, or the orbital operating margin is overstated. R = 1.5 is the *gross* markup that sits *above* that depreciation line; it is the right place to set the revenue-vs-cost-of-service relationship, and it does not by itself promise a 33% bottom-line return.

---

## 5. Verdict: is R = 1.5 fair, conservative, or aggressive?

**R = 1.5 (33.3% gross margin, 1.5× revenue-to-amortized-cost) is FAIR as a central assumption, and leans mildly conservative for a scarcity-priced, differentiated owner-operator compute product.** [INFERENCE, built on §3-4 FACTs]

**Why fair-to-conservative:**
- It sits **inside the disclosed gross-margin band of the comparable layer.** Oracle OCI's AI capacity is guided to a **30-40% gross margin** and ran ~32% in Q3 FY2026 ([Computer Weekly](https://www.computerweekly.com/news/366636165/Oracle-expects-to-increase-OCI-margins-by-30-40), [Futurum](https://futurumgroup.com/insights/oracle-q3-fy-2026-earnings-driven-by-oci-ai-infrastructure-demand/)). A 33.3% gross margin is right in the middle of that range, and *below* the ~70% reported gross margins of CoreWeave and Nebius (which, granted, understate true cost by deferring depreciation).
- It sits **below the mature hyperscaler-cloud operating margins** (AWS ~35-38%, Google Cloud 32.9%, Azure ~45%), and those are *operating* margins (post-opex), so a *gross* markup of the same magnitude is structurally modest.
- It is **above the durable owner-operator operating-margin target** (CoreWeave's long-term 25-30%, ≈ 1.33-1.43× revenue-to-cost), which is appropriate because R is a pre-opex gross markup that should exceed a post-opex operating margin of the same business.
- The orbital product is explicitly a **differentiated, scarce-attribute** offering (schedule certainty, isolation, zero-grid green; `premium_value_case.md`), not a commodity FLOPs reseller. Differentiated compute earns *above* the thin-rental floor, so anchoring the central case at a 33% gross markup rather than the ~16% commodity floor is justified by the product positioning the rest of the project builds.

**Where the band edges sit [DERIVED + FACT]:**
- **R = 1.2 (16.7% gross margin)** is the **thin-operator / commodity floor**. It is almost exactly Oracle's realized ~16% deal-level profit on AI-server rentals and CoreWeave's roughly-breakeven-to-low operating reality during buildout. This is the right low edge: it represents the orbital product competing as undifferentiated capacity.
- **R = 1.8 (44.4% gross margin)** is the **strong-pricing-power ceiling**. It sits at the top of the mature-hyperscaler-cloud *operating*-margin range (Azure ~45%) and below reported neocloud gross margins. It represents the orbital product successfully charging a scarcity/attribute premium. This is the right high edge: aggressive but not unprecedented.
- **R = 1.5 (33.3%)** is the well-centered midpoint: neither the commodity floor nor the premium ceiling.

**The one caveat that must travel with R [INFERENCE]:** R is a **gross markup over amortized CAPEX**, which is close to a gross margin, **not an operating or net margin and not an investor return.** Because the orbital node has minimal opex, its *operating* margin would be close to R's implied gross margin, but the *venture* still pays financing cost on a large front-loaded CAPEX raise and pays tax, both below the operating line. So R = 1.5 should be presented as *"revenue is set at a 33% gross markup over the node's amortized build-and-launch cost, consistent with the disclosed gross margins of GPU-cloud operators"*, and never as *"the venture earns a 33% profit."* The bottom-line return is lower and is the job of the company valuation model (`valuation/VALUATION_MODEL.md`), where `review_economist.md` Findings 1-2 (charge full straight-line depreciation; net financing and tax) directly govern how much of the 33% gross markup survives to the investor. R is sound; what it is a margin *of* must stay precise.

---

## What we already had vs what is new

**What the existing docs already established (and this doc builds on, does not duplicate):**
- `hyperscaler_margins.md` already had the value-chain margin map: NVIDIA ~75% gross / very high operating; hyperscaler cloud **34-49% segment operating** (AWS ~35%, Azure ~49%, Google Cloud ~21%); neocloud **~68-72% reported gross but ~ -1% operating**; and the key insight that **reported neocloud gross margin overstates true economics because depreciation sits outside cost-of-revenue.** It also had the sovereign-cloud +10-30% premium and the on-demand-vs-neocloud +200-500% spread.
- `revenue_economics_2026.md` had the three-layer model (reseller ~$1-2M, owner-operator ~$10-12M, inference-service ~$15-25M per rack-year) and the Oracle "30-40% gross margin" figure, **which this doc now updates** with the fresher, more textured Oracle picture (~32% Q3 FY2026 guided, but 14-16% realized on actuals and negative on Blackwell).
- `gpu_hour_rental_rates.md` had the cost-plus structure of the GPU-hour rate, the ~$2.85 IRR threshold and ~$1.65 recoup floor, CoreWeave's ~56% adjusted EBITDA / 6% adjusted operating margin, and the OCI 30-40% gross-margin benchmark as "the honest owner-operator IaaS gross margin."
- `revenue_per_watt.md` had CoreWeave 69-85% reported gross / ~breakeven operating, the depreciation swing factor, and the OpenAI ~70% inference compute margin.
- `premium_value_case.md` established the differentiated-attribute positioning that justifies pricing the orbital product above the commodity-rental floor.
- `review_economist.md` Findings 1-2 and 5 establish that the *company* model must charge full straight-line depreciation and net financing/tax below the operating line, and warned against premium-on-a-premium, all directly relevant to keeping R framed as a gross markup, not a return.
- `SOURCE_INDEX.md` carries `RLDC-REVENUE-MULTIPLE-1_5X` (central R = 1.5, 33.3% gross margin), `RLDC-SPACE-2036-MARGIN-CENTRAL` (~33.3% gross margin output), `REV-007` ($13M/rack), and `REV-008` (the +50-100% premium, supported by analogy not observed pricing).

**What is genuinely new in this doc:**
1. **Precise gross/operating/net definitions and the COGS/opex breakdown for a compute business**, with the explicit point that the orbital node's near-zero opex makes its gross and operating margins unusually close (a structural feature not previously stated).
2. **The exact markup-to-margin conversion table for the full R band** (1.2 to 16.7%, 1.5 to 33.3%, 1.8 to 44.4%) with the formula Margin = Markup/(1+Markup), and the sourced confirmation that 50% markup = 33.3% margin.
3. **A fresh, multi-sourced replacement for the stale Oracle 30-40% figure**: ~32% Q3 FY2026 gross (guided 30-40%), but **14-16% realized on actuals** ($125M gross profit on $900M AI-server rental revenue, T3M Aug 2025) and **a ~$100M loss on Blackwell rentals**.
4. **The 2026 hyperscaler-cloud operating-margin update**: Google Cloud **17.8% to 32.9%** (Q1 2025 to Q1 2026), AWS ~35-38%, Azure ~45%+, showing hyperscaler operating margins *expanding* while neocloud operating margins compress.
5. **The explicit scaling-effect analysis** (founder question b): operating-margin compression is a depreciation-timing artifact of rapid CAPEX, hits gross margin far less, and splits neocloud (compressing) from hyperscaler (expanding), with the orbital implication that the model is insulated from the opex wedge but fully exposed to depreciation timing.
6. **The mapping of R's band edges to specific real operators** as revenue-to-cost multiples: R = 1.2 ≈ Oracle/commodity floor; R = 1.5 ≈ above CoreWeave's 25-30% durable target; R = 1.8 ≈ mature-hyperscaler-cloud ceiling.
7. **CoreWeave's disclosed long-term 25-30% operating-margin target** as a durable owner-operator anchor (≈ 1.33-1.43× revenue-to-cost), newer than the prior docs' "~breakeven" snapshot.

---

## Sources

**Margin definitions (gross / operating / net; COGS for cloud)**
- [Britannica Money: Profit Margin Types: Gross, Operating & Net](https://www.britannica.com/money/profit-margin-types)
- [Wikipedia: Gross margin](https://en.wikipedia.org/wiki/Gross_margin)
- [The Rich Guy Math: Operating Margin: Definition, Formula & Benchmarks](https://therichguymath.com/operating-margin-guide/)
- [CloudZero: How To Calculate (and Improve) Your SaaS Gross Margin](https://www.cloudzero.com/blog/saas-gross-margin/)
- [CloudZero: Margin Analysis for SaaS](https://www.cloudzero.com/blog/margin-analysis/)
- [Chargebee: What Is SaaS Gross Margin](https://www.chargebee.com/resources/glossaries/saas-gross-margin/)

**Markup vs margin (the R = 1.5 = 33.3% conversion)**
- [inFlow: Margin vs Markup: How to Calculate](https://www.inflowinventory.com/blog/calculate-margin-vs-markup/)
- [Patriot Software: Margin vs Markup Chart & Infographic](https://www.patriotsoftware.com/blog/accounting/margin-vs-markup-chart-infographic/)
- [Calculator Academy: Markup to Margin Calculator](https://calculator.academy/markup-to-margin-calculator/)

**Hyperscaler cloud margins (2026)**
- [CNBC: AWS earnings Q1 2026](https://www.cnbc.com/2026/04/29/aws-earnings-q1-2026.html)
- [HeyGoTrade: AWS vs Google Cloud vs Azure: Hyperscaler Stocks 2026](https://www.heygotrade.com/en/blog/aws-vs-google-cloud-vs-azure-hyperscaler-race/)
- [HeyGoTrade: Reading the Cloud Growth Signal: Azure, GCP, AWS Q1 2026](https://www.heygotrade.com/en/blog/reading-cloud-growth-signal-azure-gcp-aws-q1-2026/)
- [Investing.com: Alphabet Q1 2026 slides: Cloud surges 63%](https://www.investing.com/news/company-news/alphabet-q1-2026-slides-cloud-surges-63-ai-investments-accelerate-93CH-4654872)
- [LevelHeaded Investing: Alphabet Q1 2026: Cloud Breaks Escape Velocity](https://www.levelheadedinvesting.com/p/alphabet-inc-google-q1-2026-results-cloud-breaks-escape-velocity-multiple-catches-up)

**Oracle OCI / AI-cloud margins (the fresh replacement for the stale 30-40% figure)**
- [Computer Weekly: Oracle expects to increase OCI margins by 30-40%](https://www.computerweekly.com/news/366636165/Oracle-expects-to-increase-OCI-margins-by-30-40)
- [Futurum: Oracle Q3 FY2026 Earnings: OCI AI Infrastructure Demand](https://futurumgroup.com/insights/oracle-q3-fy-2026-earnings-driven-by-oci-ai-infrastructure-demand/)
- [Yahoo Finance: Oracle stock falls after report reveals thin margins in AI cloud business](https://finance.yahoo.com/news/oracle-stock-falls-report-reveals-155035349.html)
- [Digitimes: Oracle's cloud business reportedly posts just 14% gross margin](https://www.digitimes.com/news/a20251008PD224/oracle-cloud-computing-business-gross-margin-revenue.html)
- [Seeking Alpha: Oracle's documents show financial challenges of renting out Nvidia's chips](https://seekingalpha.com/news/4502414-oracles-documents-show-financial-challenges-of-renting-out-nvidias-chips)

**Neocloud margins, scaling, depreciation (CoreWeave, Nebius)**
- [StockTitan: CRWV Financials (FY2025 op margin -0.9%, gross 71.7%)](https://www.stocktitan.net/financials/CRWV/)
- [Futurum: CoreWeave Q1 FY2026: Capacity Constraints Amid Accelerating AI Demand](https://futurumgroup.com/insights/coreweave-q1-fy-2026-capacity-constraints-amid-accelerating-ai-demand/)
- [LongYield: CoreWeave After Results: Hypergrowth, Hyper-Capex, and the Real Economics of the AI Cloud Trade](https://longyield.substack.com/p/coreweave-after-results-hypergrowth)
- [tech-insider: CoreWeave's $30B Capex Gamble](https://tech-insider.org/coreweave-30-billion-capex-ai-cloud-2026/)
- [Motley Fool: The Hidden Truth Behind CoreWeave's Weirdly High Gross Margin](https://www.fool.com/investing/2025/10/29/the-hidden-truth-behind-coreweaves-weirdly-high-gr/)
- [Nebius Group N.V.: Form 6-K FY2026 (Q1 2026 results, SEC)](https://www.sec.gov/Archives/edgar/data/0001513845/000110465926059872/tm2614392d1_ex99-2.htm)

**GPU rental revenue-to-cost multiple / owner-operator economics**
- [NextPlatform: How To Make More Money Renting A GPU Than Nvidia Makes Selling It (~3.5× over 4 yr)](https://www.nextplatform.com/2024/05/02/how-to-make-more-money-renting-a-gpu-than-nvidia-makes-selling-it/)
- [IntuitionLabs: NVIDIA AI GPU Prices & Cost Guide ($2.85 IRR threshold, $1.65 recoup floor)](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide)
- [GMICloud: NVIDIA H100 GPU Pricing: 2026 Rent vs. Buy Cost Analysis](https://www.gmicloud.ai/en/blog/nvidia-h100-gpu-pricing-2026-rent-vs-buy-cost-analysis)
- [Silicon Data: H100 Rental Price Over Time (2023-2025)](https://www.silicondata.com/blog/h100-rental-price-over-time)

**Companion project docs (internal)**
- [hyperscaler_margins.md](./hyperscaler_margins.md)
- [revenue_economics_2026.md](./revenue_economics_2026.md)
- [gpu_hour_rental_rates.md](./gpu_hour_rental_rates.md)
- [revenue_per_watt.md](./revenue_per_watt.md)
- [premium_value_case.md](./premium_value_case.md)
- [../peer_review/review_economist.md](../peer_review/review_economist.md)
- [../SOURCE_INDEX.md](../SOURCE_INDEX.md)

---

## Open Questions

1. **CAPEX-basis vs cost-of-revenue-basis mismatch.** R is defined over *amortized CAPEX* (build + launch ÷ service life). Operator gross margins are defined over *cost of revenue* (which for a terrestrial operator includes power, lease, and labor on top of depreciation). For the orbital node these two cost bases nearly coincide (opex ≈ 0), but the mapping of R to operator gross margins is therefore approximate, not exact. A cleaner reconciliation would express both on an identical cost base.
2. **Does the orbital near-zero-opex assumption hold?** The claim that R-over-amortized-CAPEX ≈ operating margin depends on orbital opex being negligible. Ground-station operating cost, mission operations staff, downlink/bandwidth cost, and insurance are real opex lines that the model treats as minimal. If they are material, the gap between R's gross markup and the orbital operating margin widens. Worth a dedicated orbital-opex line item.
3. **Depreciation honesty (cross-ref `review_economist.md` Finding 1).** R = 1.5 is a credible *gross* markup only if the amortized-CAPEX denominator charges the *full* deployed-capital depreciation (straight-line over service life), not an attrition-weighted fraction. If the model under-charges depreciation, the realized gross margin is below 33.3% even at R = 1.5. The R verdict here assumes the depreciation base is correct.
4. **Is 33.3% gross enough to clear the obsolescence hurdle?** `premium_value_case.md` §8 flags that an un-upgradeable orbital node must earn back its full cost inside the silicon's ~2-3 year competitive life. A 33% gross markup over amortized cost may or may not clear that bar once financing and the no-refresh penalty are netted: this is a bottom-line return question the company valuation model must answer, not a gross-margin question.
5. **Will the 2026 hyperscaler operating-margin expansion persist?** Google Cloud's jump to 32.9% and AWS's ~35-38% are recent; if AI capex re-accelerates or pricing competes down, hyperscaler cloud operating margins could compress, pulling the R = 1.8 ceiling reference down. The mapping of the high band edge is the most time-sensitive figure here.
6. **Reserved-vs-on-demand mix in the revenue-to-cost multiple.** The NextPlatform ~3.5× multiple uses a 50/30/20 on-demand/1yr/3yr blend at AWS *list* pricing. Realized neocloud pricing (and take-or-pay contract discounts) would lower the multiple materially. The 3.5× should be read as a list-price ceiling, not a realized owner-operator multiple.
