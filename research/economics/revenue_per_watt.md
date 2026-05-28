# AI Data Center Revenue Economics — Revenue per Watt / per GW

*Research date: May 2026. Prepared for the Rocket Lab orbital AI-inference data center feasibility project.*

> **Purpose:** Establish a credible **revenue-per-watt / per-GW** figure for frontier AI compute, grounded in what real GPU-cloud and inference companies earn today. This feeds the project's final framing: "IF you put ~1 GW of frontier-model inference compute in orbit, you generate roughly $X/year."

> **Reading guide:** Each claim is tagged **[FACT]** (company-disclosed / reported 2025–26 data), **[ESTIMATE]** (third-party estimate for a private company), or **[DERIVED]** (our own arithmetic for order-of-magnitude framing). Hard numbers are cross-checked against ≥2 independent sources where possible. Private-company revenue figures are inherently softer than public-company disclosures.

> **Source status (2026-05-25):** See [SOURCE_INDEX.md](../SOURCE_INDEX.md) claim IDs REV-001 through REV-012. Public-company disclosures are source-certified as disclosures. The **$15–20B/GW-year** figure is derived gross IaaS planning math, not profit. The **$25–50B/GW-year** range is a conditional inference-service scenario. GPU-hour prices must keep provider, date, hardware class, and billing model attached.

---

## Summary

- **The headline derived metric:** A GW of modern AI compute, sold as GPU capacity at realistic 2026 contract pricing and ~85–90% utilization, generates roughly **$12–25 billion/year of gross IaaS revenue** — call it an order-of-magnitude **~$15–20B per GW-year** central case. Independent terrestrial data points cluster around **~$12.5M per MW-year** ($12.5B/GW) at the low/infrastructure end, rising toward **~$25–30M/MW-year** when premium managed GPU-cloud pricing and high utilization are layered on. [DERIVED, cross-checked]
- **Anchored in real companies:** CoreWeave did **$5.13B revenue in FY2025** against **~850 MW active power** and **~250k+ GPUs** — an implied **~$6B per GW-year** on *average-during-ramp* capacity, or higher on mature/fully-utilized capacity. CoreWeave's **revenue backlog is ~$66.8B** (some sources cite ~$88B including newer deals). Oracle's OCI RPO backlog hit **~$553B**; Nebius guides to **$3–3.4B 2026 revenue** and a **$7–9B ARR exit**. [FACT]
- **GPU rental pricing (2026):** H100 on-demand has fallen to **~$2–3.70/GPU-hr** (neoclouds) vs **~$7–12/hr** at hyperscalers. GB200/Blackwell rents for **~$3.50–7/GPU-hr** on-demand; a full **GB200 NVL72 rack (72 GPUs) runs ~$750–1,950/hr** ≈ **$6–17M/year per rack** at high utilization. [FACT]
- **Inference vs. raw rental:** Selling GPU-hours is a capacity-rental business (~70–85% reported gross margin, but that often *excludes* GPU depreciation — true economic margin is much thinner). Selling **inference per-token** is a higher-value layer: frontier-model API pricing in 2026 is **~$5–15 per 1M output tokens** (GPT-5.5 $5/$30, Claude Opus 4.7 $5/$25), and a token-serving business can earn **multiples of the underlying GPU rental cost** if the model is differentiated. [FACT]
- **Key risk to revenue-per-watt:** GPUs depreciate fast. CoreWeave depreciates over **6 years**, Nebius over **4 years**; many analysts argue real economic life is **~3–4 years**. Depreciation is the single biggest swing factor between "high gross margin" and "thin true margin."

**Confidence:** Moderate-high on public-company disclosures (CoreWeave, Oracle, Nebius are SEC/listed reporters). Moderate on GPU rental pricing (well-tracked but volatile, wide provider spread). Moderate on the derived revenue-per-GW range (the arithmetic is sound but utilization, pricing tier, and GPU generation each move it ±50%). Lower on private-company figures (Crusoe, Lambda, Together — third-party estimates). The illustrative model is a framing device, not a forecast.

---

## 1. Neocloud / GPU-Cloud Company Economics

The "neocloud" sector — companies that buy NVIDIA GPUs at scale and rent them out — is the cleanest real-world proxy for revenue-per-watt, because they monetize raw compute capacity directly.

### Company-by-company (2025 actuals / 2026 guidance)

| Company | Revenue (FY2025) | Backlog / RPO | Capacity operated | GPU count | Tag |
|---|---|---|---|---|---|
| **CoreWeave** | **$5.13B** (FY2025, +168% YoY) | **~$66.8B** revenue backlog (some sources ~$88B incl. newer deals) | **~850 MW active**; **3.1+ GW contracted** (to come online by end-2027) | **~250k+ GPUs** | [FACT] |
| **Oracle (OCI)** | OCI ~$18B (FY2026 guide); cloud infra $4.9B in Q3 FY26 (+84% YoY) | **~$553B RPO** (Q3 FY26, +325% YoY) | n/a (multi-tenant) | n/a | [FACT] |
| **Nebius** | ~$1.2B ARR exiting 2025; **$3–3.4B revenue guided 2026** | n/a; targets $7–9B ARR exit-2026 | targeting **800 MW–1 GW available** by end-2026; **2+ GW contracted** | n/a | [FACT] |
| **Crusoe** | **~$998M projected 2025** (+262% YoY from $276M) | n/a | flagship 1.2 GW Abilene campus; 3.4+ GW total; 45 GW pipeline | up to 400k GB200 (Abilene) | [ESTIMATE] |
| **Lambda** | **~$760M annualized** exiting 2025 (+79% YoY) | n/a | n/a | n/a | [ESTIMATE] |
| **Together AI** | **~$300M annualized** (Sept 2025), from ~$30M Feb 2024 | n/a | n/a (inference + training cloud) | n/a | [ESTIMATE] |

Sources: CoreWeave Q4 FY2025 results and earnings call; Oracle Q3 FY2026 results; Nebius Q4 2025 shareholder letter; Crusoe Series E announcement; Lambda Series E; Together AI funding coverage (see Sources).

### What the disclosures imply about revenue per GW

**CoreWeave is the best public anchor.** FY2025 revenue $5.13B against ~850 MW of *active* power:
- **Naive average:** $5.13B / 0.85 GW ≈ **$6.0B per GW-year**. [DERIVED]
- **But this understates mature-capacity economics:** 2025 was a steep ramp — much of that 850 MW came online *during* the year, so average revenue-generating capacity was well below 850 MW. Revenue per GW on *fully-deployed, fully-contracted* capacity is materially higher.
- **Backlog cross-check:** ~$66.8B backlog against 3.1 GW contracted ≈ **~$21.5B per GW** of *total contract value*. CoreWeave contracts run ~4–6 years, so annualized that is **~$3.5–5B per GW-year** of *contracted* (take-or-pay, often discounted) revenue. [DERIVED]
- The gap between the ~$6B/GW naive figure and the ~$4B/GW backlog figure reflects (a) on-demand/spot pricing being higher than long-term contract pricing, and (b) ramp timing. A reasonable read: **mature CoreWeave-style capacity earns ~$6–10B per GW-year at the IaaS layer.**

**Implied revenue per GPU:** $5.13B / ~250k GPUs ≈ **~$20,500 per GPU-year** (FY2025 average, ramp-depressed). At full utilization and on-demand pricing the theoretical ceiling is far higher — see §3. NextPlatform notes CoreWeave's ~250k GPUs represent ~2.19B sellable GPU-hours/year; at full sell-through the theoretical max approaches ~$13B (i.e. ~$50k+/GPU-year), so 2025 actuals reflect ramp + contract discounting, not a steady state.

> **FACT vs. DERIVED boundary:** The revenue, backlog, capacity and GPU-count numbers are company-disclosed [FACT]. Every "per GW" and "per GPU" figure in this section is our division [DERIVED] and should be treated as order-of-magnitude.

---

## 2. GPU Rental Pricing (2026)

GPU rental pricing is the raw input to revenue-per-watt. The market splits sharply by provider tier.

### Per-GPU-hour rates, 2026

| GPU class | Neocloud on-demand | Hyperscaler on-demand | Reserved / contracted | Tag |
|---|---|---|---|---|
| **H100** (700W) | ~$2.00–3.70/hr (avg ~$3.72 across 41 providers; low ~$1.25) | AWS ~$6.88/hr; Azure ~$12.29/hr | up to ~60% off on-demand (multi-year) | [FACT] |
| **GB200 / Blackwell** (~1,200W/chip) | ~$3.50–4.00/hr per Superchip | Oracle ~$5.85, AWS ~$6.20, Azure ~$6.50, GCP ~$6.95/hr | ~$2.63/hr (≈30% off) | [FACT] |
| **GB200 NVL72 rack (72 GPUs)** | ~$10.50–27 per GPU-equiv-hr → **~$756–1,944/hr per rack** | — | — | [FACT] |

Key trend: H100 on-demand pricing **fell from >$7/GPU-hr (early 2024) to <$3/GPU-hr (2026)** as supply caught up — a major headwind to revenue-per-watt for older GPUs. Frontier Blackwell-class capacity holds higher pricing.

### Translating to annual revenue per rack / per GPU

A **GB200 NVL72 rack = 72 GPUs**, draws **~120–140 kW**:
- At **$756–1,944/hr** and **85% utilization**: 8,760 hr × 0.85 × ($756–1,944) = **~$5.6M–14.5M per rack-year**. [DERIVED]
- An NVL72 rack costs **~$3M** to buy — so gross rental revenue can pay back hardware in well under a year at high utilization (Morgan Stanley pegged GB200 NVL72 "AI factory" rack-level profit margin at ~77.6%, before financing/depreciation timing).

A single **H100** at **$2.50/GPU-hr contract** and **85% utilization**: 8,760 × 0.85 × $2.50 ≈ **~$18,600/GPU-year**; at on-demand $4.25/hr ≈ **~$31,600/GPU-year**. CoreWeave's own example assumes ~$29,500/GPU-year at $4.25/hr and 80% utilization. [DERIVED / FACT]

---

## 3. Revenue per Watt / per GW — The Derived Metric

This is the core deliverable. We build it bottom-up from rack power and pricing.

### Method A — bottom-up from GB200 NVL72 racks

Assumptions (all labeled, all swingable):
- **Rack:** GB200 NVL72 = 72 GPUs, **~130 kW IT power**.
- **Facility overhead (PUE ~1.2–1.4):** total power per rack ≈ **~160–180 kW**. So **~1 GW of total facility power ≈ ~5,500–6,200 NVL72 racks** (≈ 400k–450k GPUs). Use **~6,000 racks/GW** as a round figure.
- **Revenue per rack-year:** $5.6M–14.5M (from §2), central **~$8–10M/rack-year** at blended contract pricing + 85% utilization.

**Result:** 6,000 racks × $8–10M = **~$48–60B per GW-year at on-demand-leaning pricing**, or with conservative blended-contract pricing (~$5–6M/rack) **~$30–36B per GW-year**.

> Method A produces the *high* end. It assumes premium, current-generation Blackwell capacity sold near on-demand rates. Real portfolios include older/discounted GPUs and contracted (take-or-pay, discounted) revenue.

### Method B — top-down from real company economics

- **CoreWeave FY2025:** ~$6B/GW-year naive (ramp-depressed); ~$3.5–5B/GW-year on contracted backlog basis.
- **Terrestrial industry rule-of-thumb (NextBigFuture / industry analyses):** AI data centers generate **~$12.50 per watt-year ≈ $12.5M/MW-year ≈ $12.5B/GW-year** at the infrastructure/IaaS layer, vs ~$4.20/W for traditional data centers. A higher-value managed/cloud layer can add **another ~$15M/MW-year**, taking the total toward **~$25–30M/MW-year (~$25–30B/GW-year)**.

### Reconciled range

| Scenario | Revenue per GW-year | Basis |
|---|---|---|
| **Conservative** (contracted/discounted, mixed-age fleet, ramp) | **~$5–12B** | CoreWeave backlog math; infra-layer rule-of-thumb low end |
| **Central** (blended contract pricing, ~85% utilization, modern fleet) | **~$15–20B** | Midpoint of Methods A & B |
| **Aggressive** (premium Blackwell, near on-demand, ~90% utilization) | **~$30–50B** | Method A high end |

**Working figure for the project: ~$15–20B per GW-year of gross IaaS revenue**, with a plausible range of **~$5B (conservative) to ~$40B (aggressive)**. This is the *gross top-line* a 1 GW capacity owner could bill — not profit, and not net of GPU depreciation.

> **Why the range is so wide (±3x):** (1) GPU generation — Blackwell rents for ~2–3x older Hopper per watt of useful work; (2) pricing tier — on-demand is ~2–3x contracted; (3) utilization — 60% vs 90% is a 1.5x swing; (4) IaaS-only vs IaaS+managed services. These compound. Any single revenue-per-GW number is only meaningful with its assumption set attached.

---

## 4. Inference-Specific Economics

The project is about **inference serving**, not GPU rental — and the monetization model is genuinely different.

### Two distinct revenue models

1. **Selling GPU-hours (IaaS):** You rent the hardware; the customer runs whatever they want. Revenue = $/GPU-hr × hours × utilization. This is the CoreWeave/Lambda model and the basis of §3. Revenue per watt is *capped by the rental rate*.

2. **Selling inference per-token (API):** You run the model and bill per million tokens. Revenue is decoupled from hardware cost and instead set by the *value of the model output*. A differentiated frontier model can earn **several times** the underlying GPU cost of producing the tokens.

### Frontier-model token pricing, 2026 [FACT]

| Model | Input ($/1M tok) | Output ($/1M tok) |
|---|---|---|
| GPT-5.5 (OpenAI) | $5 | $30 |
| GPT-5.5 Pro | $30 | $180 |
| Claude Opus 4.7 (Anthropic) | $5 | $25 |
| Budget/small models | ~$0.10–1 | ~$0.40–4 |

Notable 2026 reversal: after two years of falling prices, frontier providers (OpenAI, Anthropic, Google) **raised** API prices in 2026, citing real cost pressure from larger reasoning models.

### Inference margin structure

- **Per-token cost** for *commodity* models collapsed ~1,000x in 3 years — GPT-4-equivalent output costs ~$0.40/1M tokens to serve in 2026 vs ~$20 in 2022.
- **But frontier models are getting more expensive to run** (compute per frontier query rising ~exponentially), which is why frontier API prices are *up*, not down.
- **Gross margin spread:** If serving cost is ~$0.40/1M tokens and you bill $2/1M, margin ≈ 80%. OpenAI is reported to run a ~70% *compute* gross margin on inference — yet still posts large net losses (projected ~$14B loss in 2026) because of training, R&D, and free-tier costs. ICONIQ's 2026 survey puts average AI-product-builder gross margin at ~52%.
- **Implication for revenue-per-watt:** A token-serving operation on the *same* 1 GW of hardware can in principle generate **more revenue per watt than raw GPU rental** — because you capture the model-value markup, not just the hardware-rental rate. But this only holds if you own a competitive model; otherwise you are just a reseller earning the IaaS rate.

> For an orbital-inference thesis, this is the key strategic fork: an orbital data center selling **raw GPU-hours** is bounded by the §3 numbers (~$15–20B/GW central). An orbital data center serving a **competitive frontier model's tokens** could in principle earn a multiple of that — but takes on model-quality risk and competes with terrestrial inference that has far lower latency and cost.

---

## 5. Utilization, Margins & Depreciation

These three factors determine how much of the §3 top-line actually survives to profit — and they bound the *realistic* revenue-per-watt.

### Utilization

- Neoclouds target **~80–90%** utilization on contracted GPUs; CoreWeave's own modeling uses **80%**.
- Contracted (take-or-pay) capacity bills regardless of customer use, so *revenue* utilization can exceed *technical* utilization.
- Spot/on-demand fleets see lower and lumpier utilization. **Use 80–90% for contracted modern capacity, lower for merchant/spot.**

### Gross margins

- CoreWeave reports **~69–85% gross margin** — but the high figure **excludes GPU/server depreciation** from cost of revenue. On a fully-loaded basis the true margin is much thinner.
- CoreWeave FY2025: **$3.09B adjusted EBITDA on $5.13B revenue ≈ 60% EBITDA margin**; but **operating margin was roughly breakeven/slightly negative** (~-1%) after depreciation and pre-IPO opex (consistent with `economics/hyperscaler_margins.md`).
- The honest read: GPU-cloud is **high gross margin, thin-to-negative operating margin during buildout**, because depreciation and interest on debt-financed GPUs are enormous.

### Depreciation — the dominant swing factor

- **CoreWeave depreciates GPUs over 6 years; Nebius over 4 years.** Hyperscalers extended server life to 6 years (Amazon's 5→6yr change added ~$3.2B to 2024 operating income — illustrating how much accounting choice moves reported profit).
- Many analysts (and short-sellers, e.g. Michael Burry's 2025 critique) argue real economic life is **~3–4 years**, because each NVIDIA generation (Hopper → Blackwell → Rubin) sharply devalues the prior one.
- **A ~$3M NVL72 rack depreciated over 4 years = ~$750k/year of depreciation per rack** — against ~$8–10M/year of revenue, that is manageable; but if utilization or pricing falls, depreciation can swamp the margin.
- **Net effect on revenue-per-watt:** depreciation does not change the *top-line* revenue-per-GW (~$15–20B) but means the *durable economic value* is perhaps **40–60% of headline gross**, and the model is fragile to pricing erosion.

---

## 6. Illustrative Revenue Model — "1 GW of Frontier Inference Compute"

> **[ILLUSTRATIVE / DERIVED — order-of-magnitude only.]** Fully-labeled arithmetic. Not a forecast.

### Shared assumptions

| Parameter | Value | Note |
|---|---|---|
| Total facility power | **1 GW** | The project's reference scale |
| PUE / overhead | ~1.25–1.35 | Orbital thermal may differ — flagged as open question |
| IT power available | ~0.75–0.80 GW | After overhead |
| Rack type | GB200 NVL72-class, ~130 kW IT | Current frontier generation |
| Racks per GW (facility) | **~5,500–6,000** | ≈ 400k–430k GPUs |
| Utilization | **85%** | Mid-range for contracted modern capacity |

### Scenario A — sell raw GPU capacity (IaaS model)

- Revenue per rack-year (blended contract pricing, 85% util): **~$6–9M**
- 6,000 racks × $6–9M = **~$36–54B/GW-year gross**… but this assumes near-premium pricing.
- Hauling it down to *realized* blended pricing (mix of contract discounts, older GPUs, ramp): central estimate **~$15–20B/GW-year**, conservative **~$8–12B**, aggressive **~$30B+**.

**Scenario A result: ~$15–20B/GW-year gross IaaS revenue (range ~$8–35B).**

### Scenario B — serve frontier-model tokens (inference API model)

- Treat the 1 GW as a token factory. Token throughput depends heavily on model size, context length, and batching — too uncertain to pin precisely.
- Anchor instead to *value capture*: an inference operator selling competitive frontier tokens historically earns a **~1.5–3x markup over the underlying GPU rental cost** of producing them (the model-value premium, per OpenAI's reported ~70% compute margin).
- Applying a ~1.5–2.5x multiple to Scenario A's central case: **~$25–50B/GW-year gross** — *if* the model is competitive and fully sold.

**Scenario B result: ~$25–50B/GW-year gross — higher than IaaS, but conditional on owning a competitive model.**

### Bottom line for the project

> **A 1 GW frontier AI compute facility plausibly generates on the order of $15–20B/year of gross revenue selling raw GPU capacity, or potentially $25–50B/year if it serves competitive frontier-model inference directly. Treat ~$10–30B/GW-year as the defensible order-of-magnitude band; the central planning figure is ~$15–20B/GW-year.**

This is **gross top-line revenue**, not profit. Net economics depend on capex (~$35–60B to build 1 GW all-in, per the project's TAM doc), GPU depreciation (3–6 yr), financing cost, and — for an orbital facility — launch, thermal, and replacement-cycle penalties not captured here.

### Cross-check against the TAM document

The companion `ai_datacenter_tam.md` illustratively values ~0.9 GW of orbital inference at "~$3B/year" of inference-*service* revenue (~$3.3B/GW). That figure is far below this document's ~$15–20B/GW. The discrepancy is real and worth resolving: the TAM doc appears to use a much lower effective $/GW (possibly a thin-margin or service-fee-only basis), whereas this document measures **gross IaaS/compute top-line**. **Flag for synthesis:** the two documents must agree on whether the orbital revenue figure is gross compute revenue, inference-service revenue, or net margin. See Open Questions.

---

## Sources

**CoreWeave:**
- [CoreWeave Q4 FY2025 earnings call transcript](https://s205.q4cdn.com/133937190/files/doc_financials/2025/q4/CORRECTED-TRANSCRIPT-CoreWeave-Inc-CRWV-US-Q4-2025-Earnings-Call-26-February-2026-5-00-PM-ET.pdf)
- [CoreWeave Reports Q4 and FY2025 Results (investor relations)](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Fourth-Quarter-and-Fiscal-Year-2025-Results/)
- [CoreWeave $66.8B backlog — Nasdaq](https://www.nasdaq.com/articles/coreweaves-668b-backlog-boosts-long-term-growth-outlook)
- [CoreWeave $88B backlog — Motley Fool](https://www.fool.com/investing/2026/04/15/coreweave-has-a-massive-88-billion-revenue-backlog/)
- [CoreWeave Q4 FY2025 results — Futurum](https://futurumgroup.com/insights/coreweave-q4-fy-2025-results-highlight-backlog-growth-and-capacity-expansion/)
- [The Hidden Truth Behind CoreWeave's Gross Margin — Motley Fool](https://www.fool.com/investing/2025/10/29/the-hidden-truth-behind-coreweaves-weirdly-high-gr/)
- [CoreWeave gross margin — Macrotrends](https://www.macrotrends.net/stocks/charts/CRWV/coreweave/gross-margin)
- [CoreWeave 250k GPU fleet — NextPlatform](https://www.nextplatform.com/2025/03/05/coreweaves-250000-strong-gpu-fleet-undercuts-the-big-clouds/)
- [CoreWeave financial engineering — NextPlatform](https://www.nextplatform.com/cloud/2026/04/09/coreweave-takes-as-much-financial-engineering-as-it-does-datacenter-design/5215794)

**Oracle / OCI:**
- [Oracle Q3 FY2026 earnings — Futurum](https://futurumgroup.com/insights/oracle-q3-fy-2026-earnings-driven-by-oci-ai-infrastructure-demand/)
- [Oracle $553B RPO backlog — WindowsForum](https://windowsforum.com/threads/oracle-ai-infrastructure-push-q3-fy2026-results-and-massive-553b-rpo.405178/)
- [Oracle Q2 FY2026 — Futurum](https://futurumgroup.com/insights/oracle-q2-fy-2026-cloud-grows-capex-rises-for-ai-buildout/)

**Nebius:**
- [Nebius Q4 2025 shareholder letter (PDF)](https://assets.nebius.com/assets/e59fb92e-9027-473a-8cac-04f9d2e9ea9a/Shareholder%20Letter%20Q4%202025.pdf)
- [Nebius Q4 earnings call highlights — Yahoo Finance](https://finance.yahoo.com/news/nebius-group-q4-earnings-call-180246496.html)
- [Can Nebius reach $7-9B ARR in 2026 — Nasdaq](https://www.nasdaq.com/articles/can-nebius-reach-7-9b-annualized-run-rate-revenue-2026)

**Crusoe / Lambda / Together:**
- [Crusoe Series E announcement](https://www.crusoe.ai/resources/newsroom/crusoe-announces-series-e-funding)
- [Crusoe raises $1.37B at $10B valuation — Tech Startups](https://techstartups.com/2025/10/24/crusoe-raises-1-37b-in-funding-at-10-b-valuation-to-build-gigawatt-scale-ai-data-centers-powered-by-clean-energy/)
- [Crusoe revenue & funding — Sacra](https://sacra.com/c/crusoe/)
- [Lambda raises $1.5B Series E — Lambda blog](https://lambda.ai/blog/lambda-raises-over-1.5b-from-twg-global-usit-to-build-superintelligence-cloud-infrastructure)
- [Lambda revenue & valuation — Sacra](https://sacra.com/c/lambda-labs/)
- [Together AI $3.3B valuation — Crunchbase News](https://news.crunchbase.com/cloud/together-ai-valuation-jump-general-catalyst-nvda/)
- [Together AI revenue — Sacra](https://sacra.com/c/together-ai/)

**GPU pricing:**
- [GPU Cloud Pricing 2026 — Spheron](https://www.spheron.network/blog/gpu-cloud-pricing-comparison-2026/)
- [H100 rental prices across 15+ providers — IntuitionLabs](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison)
- [H100 cloud pricing, 41+ providers — GetDeploying](https://getdeploying.com/gpus/nvidia-h100)
- [H100 rental price over time — Silicon Data](https://www.silicondata.com/blog/h100-rental-price-over-time)
- [GB200 cloud pricing — GetDeploying](https://getdeploying.com/gpus/nvidia-gb200)
- [GB200 NVL72 guide & pricing — Spheron](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/)
- [CoreWeave GPU pricing review — ThunderCompute](https://www.thundercompute.com/blog/coreweave-gpu-pricing-review)

**Rack power / density:**
- [GPU rack density timeline — Syaala](https://syaala.com/blog/gpu-rack-density-timeline-2026)
- [Building 100kW+ GPU racks — Introl](https://introl.com/blog/building-100kw-gpu-racks-power-cooling-architecture)
- [GB200 NVL72 — NVIDIA](https://www.nvidia.com/en-us/data-center/gb200-nvl72/)
- [Morgan Stanley GB200 NVL72 margin analysis — Wccftech](https://wccftech.com/morgan-stanley-nvidia-gb200-nvl72-racks-deliver-a-profit-margin-of-77-6-vs-64-for-amd-mi355x-while-entailing-nearly-the-same-tco/)

**Revenue per watt / inference economics:**
- [Economics of a Megawatt of AI Data Center — NextBigFuture](https://www.nextbigfuture.com/2026/05/economics-of-a-megawatt-of-ai-data-center.html)
- [AI inference cost economics 2026 — Spheron](https://www.spheron.network/blog/ai-inference-cost-economics-2026/)
- [Inference unit economics — Introl](https://introl.com/blog/inference-unit-economics-true-cost-per-million-tokens-guide)
- [OpenAI's 70% compute margin — SaaStr](https://www.saastr.com/have-ai-gross-margins-really-turned-the-corner-the-real-math-behind-openais-70-compute-margin-and-why-b2b-startups-are-still-running-on-a-treadmill/)
- [AI API pricing comparison May 2026 — DevTk](https://devtk.ai/en/blog/ai-api-pricing-comparison-2026/)
- [GPT-5.5 review & pricing — BuildFastWithAI](https://www.buildfastwithai.com/blogs/gpt-5-5-review-2026)

**Depreciation:**
- [GPU depreciation question — CNBC](https://www.cnbc.com/2025/11/14/ai-gpu-depreciation-coreweave-nvidia-michael-burry.html)
- [Resetting GPU depreciation — theCUBE Research](https://thecuberesearch.com/298-breaking-analysis-resetting-gpu-depreciation-why-ai-factories-bend-but-dont-break-useful-life-assumptions/)
- [The depreciation clock — Electron Economics](https://electroneconomics.substack.com/p/the-depreciation-clock-coreweaves)

---

## Open Questions

1. **Reconcile with the TAM document.** `ai_datacenter_tam.md` implies ~$3.3B/GW of orbital inference-service revenue; this document derives ~$15–20B/GW gross compute revenue. The synthesis must explicitly define whether the project's headline "$X/year" is (a) gross compute/IaaS top-line, (b) inference-service revenue net of model costs, or (c) operating profit. These differ by ~5–10x.
2. **Steady-state vs. ramp.** CoreWeave's ~$6B/GW naive figure is depressed by 2025 buildout timing. We need a clean "mature, fully-utilized 1 GW" figure — likely toward the upper end of the range. Worth modeling explicitly.
3. **GPU generation drift.** Revenue-per-watt is a moving target: Blackwell → Rubin → Feynman each reset pricing. An orbital facility with a multi-year launch/deployment lag may field a *trailing* GPU generation, depressing its revenue-per-watt vs terrestrial state-of-the-art. Quantify the generational discount.
4. **Orbital-specific revenue haircut.** Latency (orbital round-trip + ground-station hops), duty-cycle limits (eclipse/thermal), and downlink bandwidth caps on token throughput may all reduce realizable revenue-per-watt below terrestrial. None of that is modeled here — it belongs in the synthesis.
5. **Contracted vs. merchant mix.** Take-or-pay backlog smooths revenue but at discounted rates; merchant/spot earns more per hour but with utilization risk. The optimal mix for an orbital operator (which cannot easily re-task idle capacity) is an open design question.
6. **Depreciation in orbit.** Terrestrial GPUs depreciate over 3–6 years partly due to obsolescence. In orbit, hardware also cannot be physically upgraded without re-launch — so the *economic* life and the *revenue-generating* life may diverge further. Needs its own analysis.
