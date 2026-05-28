# Hyperscaler & AI-Infrastructure Margins — and Whether an Orbital Data Center Moves the Needle for Rocket Lab

*Research date: May 2026. Prepared for the Rocket Lab orbital AI-inference data center feasibility project.*

> **Purpose:** The project thesis assumes orbital inference compute can be sold at a **50–100% premium**. This document supplies the reference point: what cloud / AI-infrastructure businesses actually earn, who in the value chain captures the margin, how much price dispersion already exists, and — separately — whether the proposed venture is material to Rocket Lab as a company.

> **Reading guide:** Hard numbers are cross-checked against ≥2 independent sources and cited inline. Claims are tagged **[FACT]** (reported 2025–26 data), **[PROJECTION]** (forecast — speculative), or **[ARGUMENT]** (our reasoning). Companion docs: [`premium_value_case.md`](./premium_value_case.md), [`revenue_per_watt.md`](./revenue_per_watt.md), [`ai_datacenter_tam.md`](./ai_datacenter_tam.md).

---

## Summary

**Cloud/AI-infrastructure is a high-gross-margin, capital-hungry business — and the margin is unevenly captured.** [FACT] The chipmaker takes the largest slice: NVIDIA runs a **~75–76% gross margin** with H100-class parts marked up roughly **8–10×** over bill-of-materials. The hyperscalers — at scale and with their own software stack — run **34–49% segment operating margins** (Azure highest, AWS ~35%, Google Cloud ~21%). The pure-play "neoclouds" that resell GPU compute show a **reported** gross margin near 70% but a roughly **break-even-to-negative operating margin** once debt and the brutal depreciation of GPUs is counted. The colocation/power layer earns ordinary infrastructure returns (low-double-digit margins). Net: **margin pools up at the chip and at the integrated-software hyperscaler; the "rent a GPU" middle is thin.**

**Is a 50–100% premium normal or extreme? It is at the high end of observed dispersion, but not unprecedented.** [FACT] Hyperscaler on-demand H100 pricing (~$7/GPU-hr, with Azure list ~$12) already sits at a **3–6× premium over neocloud on-demand (~$2.4/GPU-hr)** — that is a **+200–500% spread for the same silicon**. Reserved/committed pricing runs 20–40% below on-demand. Sovereign / government cloud variants command a **documented 10–30% premium** for nothing more than data-residency and isolation attributes. So a 50–100% premium is *larger* than the sovereign-cloud precedent but *well within* the on-demand-vs-neocloud spread that the market already pays every day. The premium is plausible **if** the orbital product genuinely supplies a scarce attribute (schedule certainty, isolation, zero-grid green) — it is not plausible as a premium on commodity FLOPs alone.

**Does it move the needle for Rocket Lab? On revenue, yes — meaningfully. On the equity story, only as optionality.** [FACT] Rocket Lab is a **~$602M-revenue (FY2025), ~$72B-market-cap** company with a **$2.2B backlog** and **~$1.48B cash**, still operating at a loss (FY2025 GAAP operating loss ~$229M). The project's own projection — **~$500M annual revenue and ~$86M annual profit by year ~10** — would, if realized, roughly **double** today's revenue and would be Rocket Lab's first large profit pool. That is unambiguously material to the **P&L**. But against a **~$72B market cap**, a ~$500M/yr revenue line a decade out is **<1% of enterprise value** on a discounted basis — it does not move the *valuation* by itself. Its real value to the equity story is **strategic optionality**: it converts Rocket Lab from "launch + satellite components vendor" into "owner of an orbital compute platform," which is the kind of narrative re-rating that justifies the ~$1.15B peak funding ask — *if* the technical and obsolescence risks (see `premium_value_case.md` §8) can be retired.

**Confidence:** High on hyperscaler and Rocket Lab financials (multiple converging primary sources). High on the existence and rough size of cloud price dispersion. Moderate on neocloud profitability (accounting is genuinely contested — see Open Questions). The project's $500M/$86M figures are **[PROJECTION]** inputs supplied to us, not validated here.

---

## 1. Hyperscaler & AI-Infrastructure Margins

### 1.1 The big three cloud providers [FACT]

| Provider (segment) | FY2025 revenue | Segment operating margin | Notes |
|---|---|---|---|
| **AWS** (Amazon) | **$128.7B** (+20% YoY) | **~35.4%** FY2025 avg (down from ~37% in 2024) | ~$45.6B operating income; $142B Q4 run-rate. Margin compressed slightly by AI capex. |
| **Microsoft Intelligent Cloud** (incl. Azure) | n/a (segment) | **~48.6%** | Highest-margin hyperscaler; benefits from bundled enterprise software. Capex/$ of AI revenue declining. |
| **Google Cloud** | n/a (segment) | **~20.7%** | Lowest of the three but rising; analysts expect ~20%+ sustained as TPU adoption scales. |
| **Oracle OCI / cloud** | OCI IaaS ~$3B/qtr (Q4 FY25, +52% YoY) | **~43%** non-GAAP (Q3 FY26) | RPO/backlog **$553B** (Q3 FY26) — extreme forward-booking, mostly AI-infrastructure contracts. |

Sources: [CNBC AWS Q4](https://www.cnbc.com/2026/02/05/aws-q4-earnings-report-2025.html), [Futurum — Amazon Q4 FY25](https://futurumgroup.com/insights/amazon-q4-fy-2025-revenue-beat-aws-24-amid-200b-capex-plan/), [Yahoo Finance — AWS margin](https://finance.yahoo.com/news/amazons-aws-margin-expansion-accelerates-152100148.html), [Microsoft FY25 Q4 Intelligent Cloud](https://www.microsoft.com/en-us/investor/earnings/fy-2025-q4/intelligent-cloud-performance), [Windows News — MSFT vs Google Cloud](https://windowsnews.ai/article/microsoft-vs-google-cloud-2026-ai-flywheel-profit-gap-and-the-enterprise-edge.417378), [Futurum — Oracle Q3 FY26](https://futurumgroup.com/insights/oracle-q3-fy-2026-earnings-driven-by-oci-ai-infrastructure-demand/), [Investing.com — Oracle backlog](https://www.investing.com/analysis/oracle-backlog-of-553b-raises-questions-around-future-revenue-scale-200679538).

**Read-through:** Mature hyperscaler cloud is a **35–49% operating-margin** business — far above ordinary IT services — because the operator owns the software, the customer relationships, and buys hardware at the largest possible scale. Google Cloud's lower ~21% shows that *without* the bundled-software advantage, even a hyperscaler earns a more ordinary infrastructure margin.

### 1.2 The neoclouds (AI-specialist GPU resellers) [FACT]

| Provider | FY2025 revenue | Gross margin | Operating margin | Notes |
|---|---|---|---|---|
| **CoreWeave** | **$5.1B** (+168% YoY) | **~68–72% reported** | **~ −1%** (slightly negative) | EBITDA ~$2.4B; net margin ~ −23%. Reported GM widely flagged as **overstated** — much infrastructure depreciation sits outside cost-of-revenue. |
| **Nebius** | ~$900M–$1.1B run-rate exiting 2025 | n/a (disclosure thin) | Negative | Q3 2025 revenue $146M, +355% YoY. Still investment-phase. |
| **Lambda** | >$250M H1 2025 (private) | n/a | n/a | Private; among revenue leaders with CoreWeave/Crusoe. |
| **Crusoe** | private | n/a | n/a | Among neocloud revenue leaders; vertically integrated into power. |
| **Sector total** | **~$23–25B FY2025** (+~200% YoY) | — | — | Fastest-growing corner of the AI economy; profitability lags growth. |

Sources: [CoreWeave FY2025 results](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Fourth-Quarter-and-Fiscal-Year-2025-Results/), [Macrotrends — CRWV operating margin](https://www.macrotrends.net/stocks/charts/CRWV/coreweave/operating-margin), [Motley Fool — CoreWeave gross margin](https://www.fool.com/investing/2025/10/29/the-hidden-truth-behind-coreweaves-weirdly-high-gr/), [DCD — neocloud revenue >$25bn](https://www.datacenterdynamics.com/en/news/neocloud-revenue-exceeds-25bn-in-2025/), [Fierce Network — neocloud growth](https://www.fierce-network.com/cloud/neoclouds-ride-runaway-revenue-growth-train-2030).

**Read-through [ARGUMENT]:** The neocloud model exposes the real economics of "renting out GPUs." The **headline ~70% gross margin is misleading** — it excludes much of the depreciation of the GPUs themselves. Once full depreciation, debt service, and a ~2–3-year hardware life are counted, the operating margin collapses to **roughly break-even**. This is the single most important reference point for the orbital project: **the GPU-reselling layer is structurally thin once depreciation is honest** — and the orbital project's hardware obsoletes *faster than it can be serviced* (see `premium_value_case.md` §8). The orbital business must earn its return on a *scarce attribute*, not on FLOPs arbitrage.

### 1.3 The chipmaker — NVIDIA [FACT]

- **Gross margin ~75–76%** in FY2025; guides ~75% forward.
- **Data Center is ~78% of revenue** — NVIDIA *is* an AI-infrastructure company now.
- H100-class parts sell for **~$25,000–$40,000** against an estimated BOM near **~$3,300** — an **~8–10× markup** (popular "1,000% margin" framing).
- Pricing power persists even into the Blackwell generation: H100 *rental* prices rose ~40% from late-2025 into 2026 despite newer silicon shipping.

Sources: [NVIDIA FY2025 annual review (SEC)](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000098/finalforfiling-2025xannual.pdf), [IntuitionLabs — NVIDIA GPU pricing](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide), [Medium — H100 margin analysis](https://medium.com/@don-lim/nvidia-cuda-dominance-unpacking-the-1-000-profit-margin-of-the-h100-gpu-with-numbers-106f78aaf796), [Kavout — H100 rental surge](https://www.kavout.com/market-lens/why-are-nvidia-h100-gpu-rental-prices-surging-by-40).

### 1.4 Who captures the margin?

| Value-chain layer | Typical economics | Margin capture |
|---|---|---|
| **Chip (NVIDIA)** | ~75% gross margin, ~8–10× markup on H100-class | **Largest pool.** Scarcity + CUDA lock-in. |
| **Integrated hyperscaler (AWS/Azure)** | 35–49% segment operating margin | **Large.** Owns software, SLAs, customer; buys silicon at max scale. |
| **Neocloud (GPU reseller)** | ~70% *reported* GM, ~0% operating margin | **Thin.** No software moat; full GPU depreciation eats the margin. |
| **Colocation / data-center owner** | Low-double-digit operating margin; REIT-like | **Modest, stable.** Real-estate + power-delivery returns. |
| **Power provider / utility** | Regulated returns (high single digits) | **Small but rising** — power is now the binding scarcity. |

**[ARGUMENT]** Margin concentrates at the two ends with a *moat*: the **chip** (scarcity + software lock-in) and the **integrated hyperscaler** (software + scale + customer ownership). The middle — bare GPU rental and colocation — is a commodity. An orbital data center that simply rents FLOPs would sit in the *thin* part of the chain. To earn a premium it must behave like the *attribute-differentiated* layers (sovereign cloud, dedicated capacity) — see §3.

---

## 2. What Customers Actually Pay, and to Whom

When a frontier AI lab buys inference/training compute, the dollar splits roughly as follows [ARGUMENT, built on §1 FACTs]:

1. **NVIDIA** takes the first and largest cut — embedded in every GPU-hour, whoever the operator is. On a 4–5-year-amortized H100 at ~$30k, the silicon alone is on the order of **$0.7–1.0/GPU-hr** of pure-cost pass-through carrying NVIDIA's ~75% margin.
2. **The cloud operator** (hyperscaler or neocloud) sets the *retail* GPU-hour price and captures the spread between that and its all-in cost (silicon depreciation + power + cooling + networking + staff + SLA).
   - **Neocloud retail:** ~$2.0–2.6/GPU-hr on-demand → spread is thin after honest depreciation.
   - **Hyperscaler retail:** ~$7/GPU-hr (AWS) to ~$12/GPU-hr list (Azure) → a **3–6× markup over neocloud** for the same chip, monetizing SLAs, integration, security, and global footprint.
3. **The data-center / colocation owner** earns a rent-like slice of the operator's cost base (or is the operator itself, vertically integrated, as with Crusoe).
4. **The power provider** earns a small but structurally rising slice — power is now the gating input.

**[ARGUMENT] Framing for the project:** "Who is the premium paid to" — the premium in cloud is overwhelmingly paid to whoever supplies the **scarce, moated thing**: the chip, or the *trusted, integrated, attribute-rich service wrapper*. A customer paying Azure 5× the neocloud rate is not paying for better silicon — it is paying for **availability, SLA, security, and integration**. The orbital project's premium must be the same *kind* of premium: paid for an attribute (schedule certainty / isolation / zero-grid green), not for compute.

---

## 3. Is a 50–100% Premium Normal or Extreme?

**Observed price dispersion in the cloud market today [FACT]:**

| Comparison | Price spread | Premium |
|---|---|---|
| Hyperscaler on-demand H100 (~$7/GPU-hr; Azure list ~$12) vs **neocloud on-demand** (~$2.4/GPU-hr) | 3–6× | **+200% to +500%** |
| On-demand vs **reserved / committed-use** (1-yr) | reserved is 20–40% cheaper | on-demand carries a **+25–65%** premium over reserved |
| **Sovereign / government cloud** vs standard public cloud | AWS GovCloud +20–30%; Azure Gov +15–25%; Google Sovereign +10–20%; Oracle EU Sovereign +15–30% | **+10% to +30%** for isolation/residency attributes alone |

Sources: [IntuitionLabs — H100 rental comparison](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison), [Spheron — GPU cloud pricing 2026](https://www.spheron.network/blog/gpu-cloud-pricing-comparison-2026/), [SemiAnalysis — H100 rental index](https://newsletter.semianalysis.com/p/the-great-gpu-shortage-rental-capacity), [BCG — Cloud Cover: sovereignty & price](https://www.bcg.com/publications/2025/cloud-cover-price-sovereignty-demands-waste), [Data Center Frontier — Microsoft sovereign cloud](https://www.datacenterfrontier.com/hyperscale/article/55371352/microsoft-builds-for-two-worlds-sovereign-cloud-and-ai-factories).

**Verdict [ARGUMENT]:**
- A **50–100% premium is *larger* than the sovereign-cloud precedent** (+10–30%), which is the closest analog (a premium paid purely for an *attribute*, not better compute).
- But it is **comfortably *inside* the on-demand-vs-neocloud spread** (+200–500%) that the market pays every single day for the *same silicon* — purely for SLA, availability, and integration.
- So the project's premium is **plausible but not conservative**. It is *not* an outlier the market has never seen — buyers routinely pay multiples for an attribute wrapper. It *is* at the aggressive end for a premium paid on *attributes alone*, and it depends entirely on the orbital attributes (schedule certainty, physical isolation, zero-grid green) being **genuinely scarce and genuinely valued** — exactly the case `premium_value_case.md` builds and stress-tests.
- **Honest caveat:** the cloud premiums above are paid on top of a *cheap, scalable* base. The orbital base cost is *higher* than terrestrial, so the orbital "premium" is a premium on an already-elevated cost — the customer's all-in price is higher still. The 50–100% figure should be read as *price over the terrestrial alternative*, and the value case must clear that full gap, not just a marginal markup.

---

## 4. Rocket Lab as a "Hyperscaler" — the Comparison

### 4.1 Rocket Lab financials, mid-2026 [FACT]

| Metric | Value | Source |
|---|---|---|
| Market capitalization | **~$72B** (May 2026; stock ~$122, +~72% in 30 days post-Q1) | [companiesmarketcap](https://companiesmarketcap.com/rocket-lab-usa/marketcap/), [stockanalysis](https://stockanalysis.com/stocks/rklb/market-cap/) |
| FY2025 revenue | **$602M** (+38% YoY) | [Rocket Lab FY2025 release](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-announces-fourth-quarter-and-full-year-2025-financial), [GlobeNewswire](https://www.globenewswire.com/news-release/2026/02/26/3246099/0/en/Rocket-Lab-Announces-Fourth-Quarter-and-Full-Year-2025-Financial-Results.html) |
| FY2025 gross margin | **34.4% GAAP / 39.7% non-GAAP** | Rocket Lab FY2025 release (above) |
| FY2025 operating result | **GAAP operating loss ~$229M**; net loss ~$198M; adj. EBITDA loss ~$101M | Rocket Lab FY2025 release (above) |
| Q1 2026 revenue | **$200.3M** (+63.5% YoY); record quarter | [CNBC — RKLB Q1 2026](https://www.cnbc.com/2026/05/08/rocket-lab-rklb-q1-earnings-2026.html), [Simply Wall St](https://simplywall.st/stocks/us/capital-goods/nasdaq-rklb/rocket-lab/news/rocket-lab-rklb-is-up-461-after-record-q1-revenue-and-backlo) |
| Q1 2026 net loss | **~$45M** | CNBC (above) |
| Backlog | **$2.2B** (mid-2026; up from $1.85B at YE2025) | [Alpha Spread](https://www.alphaspread.com/market-news/earnings/rocket-lab-tops-first-quarter-guidance-with-record-revenue-and-22-billion-backlog), CNBC (above) |
| Cash + marketable securities | **~$1.48B** (end Q1 2026) | CNBC (above), [InsiderFinance](https://www.insiderfinance.io/news/rocket-lab-q1-2026-earnings-lift-backlog) |
| Q2 2026 revenue guidance | **$225M–$240M** | CNBC (above) |

### 4.2 Scale comparison [FACT]

| Company | Annual revenue (most recent FY) | Operating margin | Market cap |
|---|---|---|---|
| **Rocket Lab** | ~$0.6B | negative (~ −38% GAAP) | ~$72B |
| CoreWeave (neocloud) | ~$5.1B | ~ −1% | (public, multi-$10B) |
| Oracle (total) | OCI alone growing to ~$18B FY26 | ~43% non-GAAP cloud | very large |
| Google Cloud | tens of $B segment | ~21% | (Alphabet) |
| **AWS** | **$128.7B** | ~35% | (Amazon) |

**[ARGUMENT]** Rocket Lab is **two orders of magnitude smaller by revenue** than AWS, and ~8× smaller than even CoreWeave — yet it trades at a **~120× trailing revenue multiple**, versus AWS/Azure-class businesses at low-single-digit to ~10× revenue. Rocket Lab is **not priced as a launch company; it is priced as a future space-infrastructure platform.** That is the crucial context for §5: the market has *already* paid, in the ~$72B cap, for optionality and narrative that current revenue cannot remotely justify. An orbital data center is one of the bets that valuation is implicitly underwriting.

---

## 5. Does the Venture Move the Needle?

The project's investor projection (supplied to us — **[PROJECTION]**, not validated here): an orbital venture reaching **~$500M annual revenue** and **~$86M annual profit** by **year ~10**, requiring **~$1.15B peak funding**.

### 5.1 As a P&L question — **yes, material**

- ~$500M of new annual revenue would **roughly double Rocket Lab's FY2025 revenue ($602M)**. Even allowing ~10 years of organic growth in the core business, an orbital line of this size would be a **major, distinct revenue pillar**, not a rounding error.
- ~$86M of annual profit would be **Rocket Lab's first large structural profit pool** — the core company posted a ~$229M GAAP operating loss in FY2025. An ~17% net margin on the orbital line (86/500) is **healthier than the neocloud comparables** (~break-even) and in the range of a *differentiated* cloud service — consistent with the §3 premium thesis, *if* it holds.
- **Caveat:** $86M profit is a *standalone-venture* figure; it does not net the dilution/interest cost of raising $1.15B, nor the obsolescence-driven recapex (GPU refresh) that `premium_value_case.md` §8 flags as the central threat. The "profit" is fragile until the hardware-life problem is solved.

### 5.2 As an equity-story question — **only as optionality**

- Against a **~$72B market cap**, a ~$500M/yr revenue line *arriving in year 10* contributes **<1% of present enterprise value** on any reasonable discount. By itself it **does not re-rate the stock**.
- The **$1.15B peak funding ask** is ~1.6% of market cap but **~80% of current cash** ($1.48B) — it is *not* self-fundable from the balance sheet and would require dedicated capital raising or partnership. That is a real strategic commitment, not a side project.
- **Where it matters:** the value is **strategic optionality and narrative**. Rocket Lab's ~120× revenue multiple is sustained by the belief that it becomes a *vertically integrated space company* (launch → satellites → constellations → **space applications**). An owned orbital compute platform:
  - extends the vertical-integration story into the **largest end-market in technology (AI infrastructure)**;
  - gives Neutron a flagship **anchor payload / internal demand sink**, de-risking the rocket's business case;
  - creates a recurring, **services-style revenue** stream (vs. lumpy launch revenue) — the kind of mix shift that supports a higher multiple.
- **[ARGUMENT] Honest framing:** The venture moves the needle on **what Rocket Lab *is*** far more than on **what Rocket Lab *earns* in year 10**. It is a credible call option on a new platform business; it is not, on the supplied projections, a near-term valuation driver. Whether the option is worth ~$1.15B depends on (a) the premium holding (§3), and (b) the obsolescence problem being solved (`premium_value_case.md` §8) — neither is settled.

---

## Margin Comparison Table (consolidated)

| Layer / company | Gross margin | Operating margin | Premium / pricing power |
|---|---|---|---|
| NVIDIA (chip) | ~75–76% | very high | H100 ~8–10× markup over BOM |
| AWS | n/d (segment) | ~35% | On-demand H100 ~$7/hr |
| Microsoft Intelligent Cloud / Azure | n/d | ~49% | On-demand H100 list ~$12/hr |
| Google Cloud | n/d | ~21% | Lower-margin; TPU-driven |
| Oracle OCI / cloud | n/d | ~43% non-GAAP | $553B RPO backlog |
| CoreWeave (neocloud) | ~68–72% *reported* (overstated) | ~ −1% | On-demand H100 ~$2.4/hr |
| Colocation / DC owner | — | low double digits | rent-like, stable |
| Sovereign / gov cloud | — | — | **+10–30% attribute premium** |
| **Rocket Lab (whole company)** | **34% GAAP** | **~ −38% GAAP** | n/a (launch + components) |
| **Orbital venture (projected)** | — | **~17% net (86/500)** [PROJECTION] | proposed **+50–100%** |

---

## Sources

**Hyperscaler / cloud margins**
- [CNBC — AWS Q4 2025 earnings](https://www.cnbc.com/2026/02/05/aws-q4-earnings-report-2025.html)
- [Futurum — Amazon Q4 FY2025](https://futurumgroup.com/insights/amazon-q4-fy-2025-revenue-beat-aws-24-amid-200b-capex-plan/)
- [Yahoo Finance — AWS margin expansion](https://finance.yahoo.com/news/amazons-aws-margin-expansion-accelerates-152100148.html)
- [Microsoft FY25 Q4 Intelligent Cloud Performance](https://www.microsoft.com/en-us/investor/earnings/fy-2025-q4/intelligent-cloud-performance)
- [Windows News — Microsoft vs Google Cloud 2026](https://windowsnews.ai/article/microsoft-vs-google-cloud-2026-ai-flywheel-profit-gap-and-the-enterprise-edge.417378)
- [Futurum — Oracle Q3 FY2026](https://futurumgroup.com/insights/oracle-q3-fy-2026-earnings-driven-by-oci-ai-infrastructure-demand/)
- [Futurum — Oracle Q4 FY2025, RPO $138B](https://futurumgroup.com/insights/oracle-delivers-q4-fy-2025-results-with-27-cloud-growth-rpo-hits-138-billion/)
- [Investing.com — Oracle $553B backlog](https://www.investing.com/analysis/oracle-backlog-of-553b-raises-questions-around-future-revenue-scale-200679538)

**Neoclouds / NVIDIA**
- [CoreWeave — FY2025 results](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Fourth-Quarter-and-Fiscal-Year-2025-Results/)
- [Macrotrends — CoreWeave operating margin](https://www.macrotrends.net/stocks/charts/CRWV/coreweave/operating-margin)
- [Motley Fool — CoreWeave's "weirdly high" gross margin](https://www.fool.com/investing/2025/10/29/the-hidden-truth-behind-coreweaves-weirdly-high-gr/)
- [DCD — neocloud revenue exceeds $25bn in 2025](https://www.datacenterdynamics.com/en/news/neocloud-revenue-exceeds-25bn-in-2025/)
- [Fierce Network — neocloud revenue growth](https://www.fierce-network.com/cloud/neoclouds-ride-runaway-revenue-growth-train-2030)
- [NVIDIA FY2025 annual review (SEC filing)](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000098/finalforfiling-2025xannual.pdf)
- [IntuitionLabs — NVIDIA GPU pricing guide](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide)
- [Medium — H100 1,000% margin analysis](https://medium.com/@don-lim/nvidia-cuda-dominance-unpacking-the-1-000-profit-margin-of-the-h100-gpu-with-numbers-106f78aaf796)

**Price dispersion / premiums**
- [IntuitionLabs — H100 rental prices across 15+ providers](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison)
- [Spheron — GPU cloud pricing comparison 2026](https://www.spheron.network/blog/gpu-cloud-pricing-comparison-2026/)
- [SemiAnalysis — H100 rental capacity index](https://newsletter.semianalysis.com/p/the-great-gpu-shortage-rental-capacity)
- [BCG — Cloud Cover: price swings & sovereignty](https://www.bcg.com/publications/2025/cloud-cover-price-sovereignty-demands-waste)
- [Data Center Frontier — Microsoft sovereign cloud](https://www.datacenterfrontier.com/hyperscale/article/55371352/microsoft-builds-for-two-worlds-sovereign-cloud-and-ai-factories)

**Rocket Lab**
- [Rocket Lab — FY2025 financial results](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-announces-fourth-quarter-and-full-year-2025-financial)
- [GlobeNewswire — Rocket Lab FY2025 ($602M revenue)](https://www.globenewswire.com/news-release/2026/02/26/3246099/0/en/Rocket-Lab-Announces-Fourth-Quarter-and-Full-Year-2025-Financial-Results.html)
- [CNBC — Rocket Lab Q1 2026 earnings](https://www.cnbc.com/2026/05/08/rocket-lab-rklb-q1-earnings-2026.html)
- [Alpha Spread — Rocket Lab Q1 2026, $2.2B backlog](https://www.alphaspread.com/market-news/earnings/rocket-lab-tops-first-quarter-guidance-with-record-revenue-and-22-billion-backlog)
- [companiesmarketcap — Rocket Lab market cap](https://companiesmarketcap.com/rocket-lab-usa/marketcap/)
- [stockanalysis — RKLB market cap](https://stockanalysis.com/stocks/rklb/market-cap/)

---

## Open Questions

1. **Neocloud true profitability.** CoreWeave's ~70% reported gross margin is contested — depreciation classification materially flatters it. The honest figure (full GPU depreciation in COGS) is closer to break-even, but no clean public restatement exists. This directly governs how thin the "rent GPUs" layer really is.
2. **Hyperscaler GPU-specific economics.** None of AWS/Azure/Google break out *AI/GPU* margin separately from blended cloud. The 35–49% figures are whole-segment; GPU-specific operating margin could be higher (scarcity pricing) or lower (capex drag) — unresolved.
3. **Premium on an elevated base.** The 50–100% premium is measured against the *terrestrial* alternative, but orbital base cost is itself higher. The customer's all-in price is premium-on-premium. The value case must clear the *full* gap — quantified in `revenue_per_watt.md` / `premium_value_case.md`.
4. **Project projection not validated.** The ~$500M revenue / ~$86M profit / ~$1.15B funding figures are inputs supplied to this research, not independently verified. The $86M "profit" appears to be a venture-level figure that may not net financing cost or GPU-refresh recapex.
5. **Multiple sustainability.** Rocket Lab's ~120× revenue multiple already prices in heavy optionality. If the orbital venture *fails*, does the multiple compress? The downside case for the equity story is unmodeled here.
6. **Who is the orbital premium actually paid to?** If Rocket Lab buys NVIDIA silicon, NVIDIA still takes its ~75% cut at the chip layer regardless of orbit. The orbital venture's margin must come *entirely* from the attribute wrapper — it does not escape the chip tax.
