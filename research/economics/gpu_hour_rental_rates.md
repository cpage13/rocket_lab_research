# AI GPU-Hour Rental Rates and Their Trend, 2020–2036

*Research date: 2026-05-19. Prepared for the Rocket Lab orbital AI-inference data center feasibility project. Grounds the valuation calculator's revenue side: the venture sells AI compute, and this document supplies a real, sourced GPU-hour rental rate and its trajectory. Companion to `economics/revenue_per_watt.md`, `economics/revenue_economics_2026.md`, `economics/hyperscaler_margins.md`, and `economics/premium_value_case.md`.*

> **Purpose.** Establish, from current market data, (1) what one GPU-hour of frontier datacenter compute rents for in 2026, (2) how the rate has moved across four GPU generations, (3) whether the rate tracks GPU *acquisition cost* or *performance* — and who captures the FLOPS gains, (4) a defensible 2036 rate trajectory, and (5) the utilization and cost-plus markup that link rental revenue to operator cost.

> **Reading guide.** Claims are tagged **[FACT]** (vendor-published, index-tracked, or company-disclosed 2025–26 data), **[ESTIMATE]** (third-party estimate for a private/opaque figure), **[DERIVED]** (our arithmetic), or **[PROJECTION]** (directional forecast — explicitly subjective). Hard numbers are cross-checked against ≥2 independent sources where possible and cited inline. **GPU-hour rates vary by 10–20× depending on commitment term, provider tier, and date** — every figure below is labeled with *what kind* of rate it is and its *as-of* date. List/advertised rates are distinguished from real transacted rates where the data allows.

---

## Summary

**The current frontier GPU-hour rate (May 2026).** A single frontier-class GPU rents for roughly **$2–7/GPU-hour**, and the number you get depends almost entirely on three things — provider tier, commitment term, and which generation:

| GPU class | Neocloud / marketplace on-demand | Hyperscaler on-demand | Reserved / committed (1–3 yr) | Spot | As-of |
|---|---|---|---|---|---|
| **A100** (prior-prior gen, 2020) | ~$1.20–1.50/hr (avg ~$1.29 median) | ~$2–3.50/hr | ~$0.80–1.10/hr | ~$0.27–0.78/hr | May 2026 [FACT] |
| **H100** (700W, 2022) | avg **~$3.43/hr** (43 providers); on-demand avg ~$3.90 | AWS ~$6.88; Azure ~$6.98 | reserved avg ~$3.39; custom ~$1.89 | avg ~$1.75 (low ~$0.34) | May 2026 [FACT] |
| **H200** (2024) | ~$3.50–4.00/hr | AWS ~$4.98; Azure/GCP ~$10.60–10.87 | reserved from ~$2.45 | ~$1.45–2.00/hr | May 2026 [FACT] |
| **B200** (Blackwell, 2025) | avg **~$4.73/hr** (23 providers); on-demand avg ~$6.08 | ~$6–7/hr (AWS p6 spot bid up to ~$14) | reserved avg ~$3.98 (low ~$2.25–2.89, 36-mo) | avg ~$3.11 (low ~$2.45–2.63) | May 2026 [FACT] |
| **B300 / GB300** (Blackwell Ultra, 2025–26) | on-demand ~$4.50–5.80/hr; GB300 ~$4–8/hr | — | reserved ~$3.40/hr | spot from ~$2.45 | May 2026 [FACT] |
| **GB200** (NVL72 superchip) | on-demand avg **~$17.85/hr per GPU** (range $10.50 CoreWeave – $27 Azure) | — | "on request" | — | May 2026 [FACT] |
| **GB200 NVL72 rack** (72 GPUs) | **~$756–1,944/hr per rack** ($10.50–27/GPU-hr) | — | — | — | early 2026 [FACT] |

> Sources for the table: [GetDeploying H100](https://getdeploying.com/gpus/nvidia-h100) (43 providers, $3.43 avg), [GetDeploying B200](https://getdeploying.com/gpus/nvidia-b200) (23 providers, $4.73 avg), [GetDeploying GB200](https://getdeploying.com/gpus/nvidia-gb200) (9 providers, $20.14 avg, $17.85 on-demand), [GetDeploying A100](https://getdeploying.com/gpus/nvidia-a100), [ThunderCompute market trends](https://www.thundercompute.com/blog/ai-gpu-rental-market-trends), [Silicon Data B200 March update](https://www.silicondata.com/blog/b200-rental-price-march-2026-update), [Spheron B300](https://www.spheron.network/gpu-rental/b300/).

**The four headline findings:**

1. **A frontier GPU-hour, sold by a competitive neocloud, costs ~$4–7 on-demand and ~$3–4 on a multi-year reservation (2026).** The single best central figure for a *current-generation Blackwell* GPU sold by an owner-operator is **~$4.5–5.5/GPU-hour blended**. Hyperscalers charge 1.5–3× that for the *same silicon* — a markup for SLA, integration, and availability, not better compute. [FACT/DERIVED]

2. **The rate is comparatively STICKY in absolute dollars — it does NOT track performance.** This is the most important finding for the project. Across V100 → A100 → H100 → B200, the per-GPU-hour rate has stayed within a roughly **$2–7 band** the whole time, even though per-GPU compute throughput rose **~30–50× over the same span**. The rate loosely tracks **GPU acquisition cost** (a Blackwell chip costs ~$30–50k vs an A100 ~$10–17k — a ~3× span, matching the ~3× rate span from A100 to B200), *not* performance. The performance gains do **not** accrue to the operator as higher hourly revenue; they accrue to the **buyer** as a collapsing **price per unit of work**. [FACT/DERIVED — see §3]

3. **The consumer-surplus answer: the buyer captures the FLOPS gains, not the operator.** Cost to serve a GPT-4-equivalent million tokens fell **~1,000×** in ~3 years ($20 → ~$0.40), while GPU-hour rental rates *stayed flat or rose*. An operator selling a 10×-faster GPU does **not** get 10× the hourly rate — it gets maybe 1.2–1.5× (tracking the chip's higher cost). The exploding FLOPS become cheaper tokens for the customer. [FACT — see §3]

4. **Projected 2036 frontier GPU-hour rate: ~$8–20/GPU-hour, central ~$12.** If GPU acquisition cost rises sharply — Vera Rubin NVL72 racks are already quoted at **$5–8.8M** (vs ~$3M for GB200), and a path toward ~$1M/GPU as-sold is plausible by the 2030s — the hourly rate rises *with cost*, but **far slower than performance**. A defensible trajectory is **~6–9%/yr nominal growth** in the frontier per-GPU-hour rate, reaching roughly **$8–20/GPU-hour by 2036** (central ~$12). The rate stays "rental-shaped" — it does not 10× even though the chip might 30× in throughput. [PROJECTION — see §4]

**Confidence: Moderate-high** on current rates (multiple live price-tracking indices — GetDeploying, Silicon Data, ThunderCompute, Spheron — converge well, though the spread is wide). **High** on the qualitative finding that the rate is sticky/cost-linked rather than performance-linked (multiple independent sources state it explicitly). **Moderate** on the historical V100/A100 rates (less well-documented than H100). **Lower** on the 2036 projection (the direction is robust; the magnitude is ±50%+ over a 10-year horizon, and depends on whether the market stays supply-constrained or tips into oversupply).

---

## 1. Current (2026) GPU-Hour Rental Rates

### 1.1 The structure of the market — why one number cannot answer the question

A GPU-hour rate is meaningless without three qualifiers. The same H100, on the same day (a real 24-hour window observed across 24 marketplaces), traded **from $0.72 to $15.14/hr — a 21× spread** ([Data Center Knowledge](https://www.datacenterknowledge.com/infrastructure/gpu-rental-markets-show-signs-of-pricing-compression)). That spread is not irrational; it reflects four real axes:

- **Provider tier.** Hyperscalers (AWS/Azure/GCP) charge **1.5–3× more than neoclouds** for identical silicon — the premium buys SLA, security, global footprint, integration, and support. `hyperscaler_margins.md` documents this as a structural +200–500% spread on H100 historically.
- **Commitment term.** On-demand > reserved (1–3 yr) > spot/preemptible. Reserved runs **~20–45% below on-demand**; spot runs lower still but is interruptible.
- **GPU generation.** Frontier (Blackwell) commands a premium; aging silicon (A100, early H100) commoditizes downward.
- **Node quality.** Networking (InfiniBand vs Ethernet), storage, single-GPU vs full-cluster, and geography all move the price.

**List vs transacted.** Hyperscaler "list" prices (e.g. Azure H100 ~$6.98/hr) are advertised rack rates; large buyers transact well below list via enterprise discounts and committed-use agreements. Neocloud marketplace prices (GetDeploying, Silicon Data indices) are closer to *real transacted* rates because they aggregate live, competed listings. **Treat hyperscaler figures as list-leaning and neocloud index averages as transaction-leaning.**

### 1.2 H100 — the best-documented anchor (May 2026) [FACT]

The H100 is the most-tracked GPU and the cleanest data point. As of **May 19, 2026** ([GetDeploying, 43 providers, 236 listings](https://getdeploying.com/gpus/nvidia-h100)):

| Billing model | Listings | Average rate | Notes |
|---|---|---|---|
| On-demand | 115 | **$3.90/hr** | competed neocloud + hyperscaler mix |
| Reserved (1–3 yr) | 90 | **$3.39/hr** | committed-use |
| Spot | 29 | **$1.75/hr** | interruptible, low $0.34 |
| Custom contract | 2 | $1.89/hr | negotiated bulk |
| **Blended average** | 236 | **~$3.43/hr** | low $0.34, high $14.90 |

- **Hyperscaler on-demand:** AWS p5 ~**$6.88/hr**, Azure NCadsH100v5 ~**$6.98/hr** ([GetDeploying](https://getdeploying.com/gpus/nvidia-h100)).
- **Neocloud on-demand:** typically **~$2–4/hr**; specialist clouds and marketplaces lower. Silicon Data's late-2025 neocloud median was **~$3.33/hr** ([Silicon Data H100 history](https://www.silicondata.com/blog/h100-rental-price-over-time)).
- **A telling 2026 wrinkle:** H100 on-demand pricing **rose ~25% over the year to May 2026** (GetDeploying notes a move from ~$3.24 to ~$4.06/hr) — even as newer Blackwell silicon shipped. H100 1-year *contract* pricing rose **~40%** from a ~$1.70/hr trough in Oct 2025 to ~$2.35/hr by March 2026 ([Spheron](https://www.spheron.network/blog/gpu-cloud-pricing-comparison-2026/), [IntuitionLabs](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison)). At the same time, smaller-provider H100 rates *fell* ~22% YTD per an FT figure ([Data Center Knowledge](https://www.datacenterknowledge.com/infrastructure/gpu-rental-markets-show-signs-of-pricing-compression)). **The H100 market is genuinely two-sided in 2026 — aging silicon commoditizing at the bottom, supply-constraint pricing power at the contracted top.** Sources legitimately disagree on net direction; the honest read is "roughly flat to modestly up, with a very wide spread."

### 1.3 Blackwell (B200 / B300 / GB200) — the frontier (May 2026) [FACT]

The current frontier generation. B200 as of **May 19, 2026** ([GetDeploying, 23 providers, 86 listings](https://getdeploying.com/gpus/nvidia-b200)):

| Billing model | Average rate | Range |
|---|---|---|
| On-demand | **$6.08/hr** | up to ~$14 (AWS p6 spot bid) |
| Reserved | **$3.98/hr** | low ~$2.25–2.89 (36-mo) |
| Spot | $3.11/hr | low ~$2.45–2.63 |
| **Blended average** | **~$4.73/hr** | $2.25–14.24 |

- **B300 / GB300 (Blackwell Ultra):** on-demand ~$4.50–5.80/hr, reserved ~$3.40/hr, GB300 ~$4–8/hr ([Spheron B300](https://www.spheron.network/gpu-rental/b300/), [GetDeploying B300](https://getdeploying.com/gpus/nvidia-b300)).
- **GB200 (NVL72 superchip):** the on-demand average is much higher — **~$17.85/hr per GPU**, range $10.50 (CoreWeave) to $27 (Azure) ([GetDeploying GB200](https://getdeploying.com/gpus/nvidia-gb200)). *Caveat:* the GB200 figure is partly a units artifact — a "GB200" in NVL72 form is a high-power superchip and sold rack-integrated; the per-GPU number is not directly comparable to a discrete B200. A **GB200 NVL72 rack of 72 GPUs rents for ~$756–1,944/hr** ([Spheron NVL72 guide](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/)).
- **2026 frontier price rebound [FACT].** Blackwell rates *rose* sharply in early 2026: the **B200 rental index jumped ~24% in a single quarter** (Jan–Mar 2026, index 4.40 → 5.48), and GB200 on-demand rose **~35% since July 2025** ($13.25 → $17.85/GPU-hr). Drivers: Samsung/SK Hynix raised **HBM3e contract prices ~20%**, NVIDIA revised MSRPs upward, GTC 2026 triggered enterprise commitments, and a wave of frontier model launches (Claude Opus 4.6, GPT-5.3/5.4, Gemini 3.1) consumed B200 capacity ([Silicon Data B200 March update](https://www.silicondata.com/blog/b200-rental-price-march-2026-update)). **This is the cost-pass-through mechanism in action — when the chip's input costs (HBM) rose, the rental rate rose with it.** Notably, over the same window H100 hyperscaler pricing was flat (−1%) and H100 neocloud rose only 8% — the rebound is frontier-specific supply tightness, not a broad market move.

### 1.4 H200 (the 2024 mid-generation) [FACT]

H200 as of May 2026: neocloud/specialist ~$3.50–4.00/hr on-demand; AWS p5e ~$4.98/hr (after a Jan 2026 ~15% price increase); CoreWeave ~$6.31/hr; Azure/GCP hyperscaler ~$10.60–10.87/hr list; reserved from ~$2.45/hr ([ThunderCompute H200](https://www.thundercompute.com/blog/nvidia-h200-pricing), [JarvisLabs H200](https://jarvislabs.ai/blog/h200-price), [Hyperstack](https://www.hyperstack.cloud/nvidia-h200-sxm)).

### 1.5 The central 2026 figure

> **For a frontier (Blackwell B200/B300-class) GPU sold by an owner-operator at a competitive neocloud rate, the central 2026 GPU-hour rate is ~$4.5–5.5 blended** (on-demand ~$6, reserved ~$4, with the mix landing mid-band). On-demand-leaning is ~$6; contract-heavy is ~$4. Hyperscalers would charge ~$7–11 for the same chip. An aging H100 sits at ~$3–4; a fully-commoditized A100 at ~$1–1.5. [DERIVED — cross-checked against GetDeploying, Silicon Data, ThunderCompute, Spheron]

This is consistent with the project's existing `revenue_economics_2026.md`, which uses 72-GPU NVL72-class racks at a blended **~$1,000–1,400/hr/rack** ⇒ **~$14–19/GPU-hr for GB200-superchip racks** or **~$5–9/GPU-hr for discrete-Blackwell racks** — the rack-level figure folds in the higher-power superchip premium.

---

## 2. The Historical Trend — V100 → A100 → H100 → B200

### 2.1 Per-GPU-hour rates by generation [FACT / ESTIMATE]

| GPU | Launch | Launch-era rate (on-demand) | 2026 rate (commoditized) | Acquisition cost (per chip) |
|---|---|---|---|---|
| **V100** | 2017–18 | ~$2.50–3.00/hr (cloud, 2018–20) | ~$0.50–0.80/hr | ~$8–10k |
| **A100** | 2020 | ~$3–4/hr (cloud on-demand, 2020–21) | ~$1.20–1.50/hr (median ~$1.29) | ~$10–17k ($10–12k 40GB, $15–17k 80GB) |
| **H100** | 2022–23 | **$7–10/hr** (extreme scarcity, "often >$12") | ~$3.43/hr blended | ~$25–40k |
| **B200** | 2025 | ~$6–10/hr (early scarcity) | ~$4.73/hr blended (rising) | ~$30–50k |
| **GB300/B300** | 2025–26 | ~$5–8/hr | current generation | ~$6–6.5M per NVL72 rack |
| **Vera Rubin VR200** | H2 2026 | ~$5–9/hr (projected) | — | **$5–8.8M per NVL72 rack** |

> Sources: [Silicon Data H100 history](https://www.silicondata.com/blog/h100-rental-price-over-time); [IntuitionLabs NVIDIA pricing](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide); [JarvisLabs A100](https://jarvislabs.ai/blog/a100-price); [GetDeploying A100](https://getdeploying.com/gpus/nvidia-a100); [Tom's Hardware Vera Rubin NVL72 $8.8M](https://www.tomshardware.com/tech-industry/artificial-intelligence/price-of-nvidias-vera-rubin-nvl72-racks-skyrockets-to-as-much-as-usd8-8-million-apiece-but-server-makers-margins-will-be-tight-nvidia-is-moving-closer-to-shipping-entire-full-scale-systems). *V100 and early-A100 rates are [ESTIMATE] — less well-documented than H100; treat as order-of-magnitude.*

### 2.2 The H100 price trajectory in detail — the cleanest record [FACT]

The H100, from [Silicon Data's index](https://www.silicondata.com/blog/h100-rental-price-over-time):

| Period | Hyperscaler median | Marketplace / neocloud median |
|---|---|---|
| Aug–Dec 2023 (scarcity) | **$7.76/hr** (on-demand often >$12) | — (market not yet liquid) |
| Jan–May 2024 | $7.92/hr | — |
| Jun–Dec 2024 | $9.34/hr | marketplace $2.58 / neocloud $2.99 |
| Jan–May 2025 | $8.73–9.30/hr | marketplace $2.27–2.46 |
| Jun 2025 (AWS −30% reset) | dropped to $6.94/hr | — |
| Jul–Dec 2025 | $6.26/hr median | marketplace $1.95 / neocloud $3.33 |
| 2026 (rebound) | ~$6.9–7.0/hr | on-demand ~$3.9, contract +40% off Oct-25 trough |

**The H100 story:** launched into extreme scarcity at **$7–10+/hr**, peaked, then **collapsed ~64% peak-to-trough** as (a) NVIDIA ramped shipments in 2024, (b) **300+ new providers** entered the H100 cloud market, (c) GPU marketplaces created price discovery, and (d) inference-optimization software cut the GPU-hours per workload ([Introl GPU cloud price collapse](https://introl.com/blog/gpu-cloud-price-collapse-h100-market-december-2025), [ThunderCompute trends](https://www.thundercompute.com/blog/ai-gpu-rental-market-trends)). Then in 2026 contracted/frontier-adjacent rates rebounded ~25–40% on HBM cost pressure and sustained demand. **An individual GPU's rate is front-loaded and decays as the silicon ages and the next generation arrives** — this is the in-life decay the calculator models.

### 2.3 The pattern: a sticky $2–7 band, not a rising staircase

Stand back from any single generation and the striking fact is **how narrow the band is**:

- V100 launched ~$2.50–3/hr; A100 ~$3–4/hr; H100 spiked to $7–10 then settled ~$3–4; B200 ~$4–7. **The on-demand rate for the current-generation flagship has lived in a ~$3–10/hr band for eight years** — and the *commoditized* rate for any generation lands ~$1–4/hr.
- The H100's $7–10 launch spike was a **scarcity event**, not a structural step-up — it reverted. Strip the spikes and the underlying frontier rate drifts up only **modestly** generation-over-generation.
- Meanwhile **per-GPU compute throughput rose enormously**: V100 → A100 was ~2.5× (FP16), A100 → H100 ~3–6×, H100 → B200 ~2–2.5× for training and more for low-precision inference — compounding to roughly **30–50× more useful throughput per GPU** from V100 to B200.

> **The headline of the history: the rate is comparatively STICKY in absolute dollars. The flagship GPU-hour has roughly held a $3–10/hr band (commoditized: $1–4/hr) across four generations, while per-GPU performance rose ~30–50×.** The rate did **not** track performance. It tracked, loosely, **acquisition cost** — and even that only partially (cost rose ~3–5× V100→B200; the rate rose far less). The next section explains why, and who got the surplus.

---

## 3. What Sets the Rate — Acquisition Cost vs Performance, and Who Captures the FLOPS

This is the analytically most important section for the valuation calculator. The question: when a new GPU is ~10× faster, does its hourly rate rise ~10×?

### 3.1 The answer: the rate tracks COST (loosely), not performance

**The rate is cost-plus, not performance-plus.** The mechanism:

- A GPU-hour rate must, over the hardware's life, **recover the GPU's acquisition cost + power + cooling + networking + financing + operator margin**. The dominant term is acquisition cost. So a pricier chip *must* rent for more to clear an acceptable return.
- This is visible directly. A100 (~$10–17k) rents ~$1.3/hr commoditized; B200 (~$30–50k) rents ~$4.7/hr — the **~3× cost ratio roughly matches the ~3× rate ratio**. The 2026 B200 rebound is the same mechanism on fast-forward: HBM contract prices rose ~20%, NVIDIA lifted MSRPs, and **the rental rate rose ~24% in a quarter in direct response** ([Silicon Data](https://www.silicondata.com/blog/b200-rental-price-march-2026-update)).
- A continuous-operation sanity check: an H100 at ~$3/hr earns ~$26k/year — which "roughly equals the purchase price of the GPU alone" ([Silicon Data](https://www.silicondata.com/blog/h100-rental-price-over-time)). The rate is set so the chip pays itself back in ~1–1.5 years of high-utilization operation, then earns margin. That is a **cost-anchored** rate.

**The rate does NOT track performance.** B200 delivers far more than 1.5× an A100's useful inference work, yet rents for only ~3× — and that 3× is the *cost* ratio, not the *performance* ratio. If rates tracked performance, a 10×-faster GPU would rent for ~10× more. It does not — it rents for roughly its *cost* multiple, which is far smaller. Multiple sources state this explicitly:

> "Falling per-token costs have **not reduced GPU rental pricing**. … GPU marketplace rates for H100s have **remained stable or increased** even as cost-per-token fell." — [GPUnex, AI Inference Economics 2026](https://www.gpunex.com/blog/ai-inference-economics-2026/)

### 3.2 Who captures the FLOPS gains — the consumer-surplus answer

If the operator's hourly rate is roughly flat (cost-linked) while each new GPU does 2–3× more work per hour, then **the value of the extra FLOPS flows past the operator to the buyer.** It shows up as a **collapsing price per unit of work**:

- **Cost to serve a GPT-4-equivalent 1M tokens fell ~1,000× in ~3 years** — from ~$20 (late 2022) to ~$0.40 (early 2026) ([GPUnex](https://www.gpunex.com/blog/ai-inference-economics-2026/), [Introl inference unit economics](https://introl.com/blog/inference-unit-economics-true-cost-per-million-tokens-guide)). API list prices fell similarly — GPT-4 ~$60/1M to GPT-5.4 ~$15/1M, a ~50× drop ([TokenMix pricing history](https://tokenmix.ai/blog/ai-pricing-trends-history)).
- That ~1,000× collapse came from four compounding factors, only one of which is hardware: (1) **hardware efficiency** — each GPU generation ~2–3× more inference throughput per dollar; (2) **software** — vLLM/PagedAttention/continuous batching raised utilization from ~30–40% to ~70–80%; (3) **MoE architectures** — ~3–5× lower compute per token; (4) **quantization** — INT8/INT4, ~2–4× ([GPUnex](https://www.gpunex.com/blog/ai-inference-economics-2026/)).
- **Crucially, the GPU-hour rate did not fall 1,000×. It stayed roughly flat (and in 2026 rose).** The buyer got 1,000× cheaper tokens; the operator kept renting the box for ~$3–7/hr.

**This is a Jevons-paradox dynamic.** Cheaper compute-per-token does not shrink operator revenue, because it *expands total demand* — more workloads become economical, and aggregate GPU-hours sold rise faster than the per-unit price falls ([GPUnex](https://www.gpunex.com/blog/ai-inference-economics-2026/)). The operator's protection is *volume growth*, not *price*.

> **The consumer-surplus verdict — load-bearing for the project.** The exploding FLOPS of each GPU generation are **consumer surplus captured by the compute buyer**, not the operator. An operator (terrestrial or orbital) selling raw GPU-hours **cannot** expect its hourly rate to scale with performance. When it fields a GPU that is 10× faster, it gets perhaps 1.2–1.5× the hourly rate (tracking the chip's higher cost), while the *buyer's* price per token drops by far more. **The orbital venture's revenue per GPU-hour is therefore bounded by a cost-plus rate that grows slowly — it does not inherit the FLOPS curve.** This is exactly the conclusion `revenue_economics_2026.md` §3.2 reached at the rack level ("revenue tracks the rack's price, not its FLOPS"); this document confirms it at the per-GPU-hour level with the inference-cost data.

### 3.3 Where the margin actually pools

A reminder from `hyperscaler_margins.md`, because it explains *why* the operator's rate is cost-anchored and thin: the GPU-hour rate carries **NVIDIA's ~75% gross margin embedded in every hour** regardless of who operates the box. The chipmaker captures the largest pool. The integrated hyperscaler captures a large pool (35–49% segment operating margin) via the SLA/integration markup. The **bare GPU-rental operator earns a thin spread** — competed down to roughly break-even operating margin once honest depreciation is counted. The rate is cost-plus precisely because the rental layer has no moat to push price above cost.

---

## 4. Projection to 2036

### 4.1 The drivers and their directions

| Force | Direction on the rate | Magnitude |
|---|---|---|
| **GPU acquisition cost rising** (HBM, reticle-limit silicon, packaging) | **Up** | Strong — rack cost ~2×/generation; toward ~$1M/GPU as-sold plausible by 2030s |
| **Performance per GPU rising** | **~Neutral on the rate** (flows to buyer as cheaper tokens) | Large on tokens, small on $/GPU-hr |
| **Supply ramp / new entrants / commoditization** | **Down** | Strong for aging silicon; the 300+-provider H100 collapse is the template |
| **Demand growth (agentic, inference > training)** | **Up** | Strong — inference market >$50B in 2026, growing faster than training |
| **In-life decay** (silicon ages within its generation) | **Down over a node's life** | ~10–15%/yr for a given GPU |

The net of these is **NOT** the performance curve and **NOT** flat — it is a **slow upward drift in the frontier per-GPU-hour rate, tracking acquisition cost, punctuated by scarcity spikes and commoditization troughs.**

### 4.2 The acquisition-cost anchor — what "toward $1M/GPU" implies

GPU/rack acquisition cost is rising steeply and visibly:
- GB200 NVL72 rack ~$3M (2024) → GB300 NVL72 ~$6–6.5M (2025–26) → **Vera Rubin VR200 NVL72 quoted at $5–8.8M** (H2 2026) ([Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/price-of-nvidias-vera-rubin-nvl72-racks-skyrockets-to-as-much-as-usd8-8-million-apiece-but-server-makers-margins-will-be-tight-nvidia-is-moving-closer-to-shipping-entire-full-scale-systems)). Per-GPU, an NVL72 of 72 GPUs at $8M ≈ **$110k/GPU as-sold** today at the bleeding edge.
- If the per-generation ~1.3–2× cost step continues over ~5 more generations to 2036, a frontier GPU "as sold" (rack-integrated, allocated) could plausibly reach **~$300k–1M+/GPU**. The project brief's "~$1M/GPU as-sold" is at the high but not implausible end of that path.

**The key question: if the chip's cost 10×'s, does the hourly rate 10×?** Based on §3, **no — but it rises substantially.** The rate is cost-plus, so a 10× cost increase exerts strong upward pressure on the rate. But three things damp it well below 10×: (1) each generation also does far more work, so the rate per *unit of useful work* still collapses — competition forces the operator to pass most of that through; (2) within a rack, much of the cost increase is offset by more GPUs/higher density, so per-GPU-hour cost rises less than rack cost; (3) commoditization and oversupply repeatedly cap the frontier premium. **Historically the rate rose far less than cost** (V100→B200: cost ~3–5×, commoditized rate ~2–3×, flagship on-demand rate roughly flat-to-modest). Extrapolating: **a 10× rise in chip cost over a decade likely produces a ~2–3× rise in the per-GPU-hour rate, not 10×.**

### 4.3 The 2036 trajectory [PROJECTION — directional]

| Year | Frontier generation | Frontier GPU-hour rate, blended owner-operator, central | Tag |
|---|---|---|---|
| **2026** | GB300 / early Rubin | **~$4.5–5.5/GPU-hr** (B200/B300-class, blended) | [FACT/DERIVED] |
| 2028 | Rubin Ultra-class | ~$6–8/GPU-hr | [PROJECTION] |
| 2030 | post-Rubin (Feynman-class) | ~$7–11/GPU-hr | [PROJECTION] |
| 2033 | — | ~$9–15/GPU-hr | [PROJECTION] |
| **2036** | — | **~$8–20/GPU-hr, central ~$12** | [PROJECTION] |

- **Central growth assumption: ~6–9%/yr nominal** in the frontier blended per-GPU-hour rate. This is *below* rack-cost growth (~2×/generation ≈ 15–40%/yr) — the wedge between them is the consumer surplus passed to the buyer — and *below* the project calculator's prior 15%/yr per-rack revenue growth (which `revenue_economics_2026.md` already flagged as too hot and recommended cutting to ~10–12%). Per-rack revenue can grow faster than per-GPU-hour rate because racks pack more GPUs each generation; the per-GPU-hour rate itself grows more slowly, ~6–9%/yr.
- **Wide band (±50%+).** The low case (~$8/GPU-hr by 2036): supply catches up, the market commoditizes like the H100 did, oversupply caps the frontier premium — [Data Center Knowledge](https://www.datacenterknowledge.com/infrastructure/gpu-rental-markets-show-signs-of-pricing-compression) already reports "early signs of pricing compression and infrastructure commoditization." The high case (~$20/GPU-hr): sustained supply constraint, HBM scarcity persists, demand outruns fab/packaging capacity — the 2026 rebound generalizes.
- **The rate stays "rental-shaped."** Even at the high end, $20/GPU-hr in 2036 is only ~4× the 2026 rate — against a chip that may do 10–30× more work. **The hourly rate does not 10×.** The defensible planning statement: *the frontier GPU-hour rate roughly doubles to quadruples by 2036 (central ~2.5×, to ~$12), tracking acquisition cost and demand, while price per unit of work continues to collapse.*

### 4.4 The orbital-specific caveat

An orbital operator cannot refresh silicon without re-launch. Its racks therefore **age toward the commoditized (lower) rate of their generation** while terrestrial operators continuously add frontier capacity. So an orbital node's *realized lifetime* rate drifts from the frontier figure toward the commoditized figure of its launch generation (e.g. a node launched with B200-class silicon trends from ~$5/hr toward the ~$1.5–3/hr H100/A100-style commoditized fate as newer generations arrive). This generational-decay derate is real and belongs in the calculator — `revenue_economics_2026.md` Open Question 1 flags exactly this.

---

## 5. Utilization and Operating Economics

### 5.1 Utilization of rented GPUs [FACT]

- **Contracted/committed capacity:** neoclouds run **above ~90% utilization** on contracted GPUs ([HyperFRAME Research](https://hyperframeresearch.com/2026/05/11/coreweave-reaches-a-new-scale-threshold-but-can-the-ai-neocloud-sustain-long-tail-demand/) — "neocloud providers command premium pricing while maintaining utilization rates above 90%"). CoreWeave's own financial modeling historically used **~80%** as a conservative planning figure (`revenue_per_watt.md`).
- **Take-or-pay contracts bill regardless of customer use** — so *revenue* utilization can exceed *technical* utilization. CoreWeave's revenue backlog is **$99.4B** (Q1 2026), almost all multi-year take-or-pay ([Data Center Knowledge neocloud roundup](https://www.datacenterknowledge.com/cloud/earnings-roundup-neoclouds-shift-from-gpu-race-to-power-wars)).
- **Software raised the *internal* utilization of the silicon** — vLLM and continuous batching pushed GPU compute utilization from ~30–40% to ~70–80% ([GPUnex](https://www.gpunex.com/blog/ai-inference-economics-2026/)) — but this is throughput efficiency, distinct from the fraction of *hours* a rented GPU is paid for.
- **Spot/merchant fleets** see lower, lumpier utilization. **Planning figure: ~85–90% for contracted modern capacity; lower for merchant/on-demand.**

### 5.2 The cost-plus markup and resulting margin [FACT / DERIVED]

The rental rate is set as **operator cost + margin**. The "margin" depends entirely on what counts as cost:

- **Reported gross margin** of the GPU-rental layer looks high — CoreWeave reports **~56% adjusted EBITDA margin** (Q1 2026) and historically ~69–85% "gross margin" — **but the high gross-margin figure excludes GPU/server depreciation**, which is the single largest real cost ([Motley Fool on CoreWeave's gross margin](https://www.fool.com/investing/2025/10/29/the-hidden-truth-behind-coreweaves-weirdly-high-gr/), `hyperscaler_margins.md`).
- **Fully-loaded, the markup is thin.** CoreWeave Q1 2026: revenue $2.08B (+112% YoY), **adjusted EBITDA $1.16B (56% margin)** — but **net loss of $740M** and **Q4 2025 adjusted operating income margin of just 6%** (down from 16%), because depreciation and interest on debt-financed GPUs are enormous ([Data Center Knowledge](https://www.datacenterknowledge.com/cloud/earnings-roundup-neoclouds-shift-from-gpu-race-to-power-wars), [Startup Fortune](https://startupfortune.com/coreweaves-q1-earnings-are-a-live-test-of-whether-gpu-cloud-economics-can-survive-the-debt-they-created/)).
- **Oracle's OCI** — a cleaner disclosure — explicitly guides its AI-infrastructure cloud to a **30–40% gross margin**, versus ~68% for legacy software (`revenue_economics_2026.md`). That ~30–40% is the honest "owner-operator IaaS" gross margin: a **moderate-margin business, not a software-margin business.**
- **The cost-plus structure, summarized.** The GPU-hour rate ≈ (acquisition cost amortized over ~3–6 yr + power + cooling + networking + financing + opex) ÷ (hours × utilization), plus a competed-thin operator margin. At ~$3/hr and high utilization an H100 recovers its ~$26k purchase price in ~1–1.5 years — but the *node* (server, networking, facility, financing) costs far more than the bare GPU, which is why fully-loaded operating margin is only single-digit-to-low-double-digit during buildout. **The rental layer is high-reported-gross-margin, thin-true-operating-margin.**

### 5.3 Implication for the project

The orbital venture, if it sells raw GPU-hours, is an **owner-operator** (`revenue_economics_2026.md` layer 2). It captures the full IaaS rate (no reseller markup paid out) but is bounded by:
- a **cost-plus rate** that grows slowly (~6–9%/yr per GPU-hour, §4);
- a **fully-loaded operating margin** that is moderate at best (~30–40% gross at the OCI benchmark, far thinner net after depreciation);
- and — uniquely for orbit — **no ability to refresh silicon**, so its racks decay toward the commoditized rate of their launch generation.

Any orbital *premium* (the project's 50–100% thesis) must be earned on top of this cost-plus rate as a separate attribute markup — it cannot come from the GPU-hour rate scaling with performance, because it does not.

---

## Sources

**Current GPU-hour rental rates (2026) — live price indices**
- [H100 Cloud Pricing, 43 providers (avg $3.43/hr) — GetDeploying](https://getdeploying.com/gpus/nvidia-h100)
- [B200 Cloud Pricing, 23 providers (avg $4.73/hr) — GetDeploying](https://getdeploying.com/gpus/nvidia-b200)
- [GB200 Cloud Pricing, 9 providers (avg $20.14/hr, $17.85 on-demand) — GetDeploying](https://getdeploying.com/gpus/nvidia-gb200)
- [A100 Cloud Pricing, 38 providers — GetDeploying](https://getdeploying.com/gpus/nvidia-a100)
- [B300 Cloud Pricing — GetDeploying](https://getdeploying.com/gpus/nvidia-b300)
- [H100 Rental Prices Compared, 15+ providers ($1.49–6.98/hr) — IntuitionLabs](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison)
- [GPU Cloud Pricing 2026: H100 from $1.03/hr, B200 from $2.12/hr — Spheron](https://www.spheron.network/blog/gpu-cloud-pricing-comparison-2026/)
- [B300 rental from $2.45/hr — Spheron](https://www.spheron.network/gpu-rental/b300/)
- [GB200 NVL72 guide — rack $756–1,944/hr — Spheron](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/)
- [NVIDIA H100 Pricing May 2026 — ThunderCompute](https://www.thundercompute.com/blog/nvidia-h100-pricing)
- [NVIDIA H200 Pricing May 2026 — ThunderCompute](https://www.thundercompute.com/blog/nvidia-h200-pricing)
- [AI GPU Rental Market Trends, May 2026 — ThunderCompute](https://www.thundercompute.com/blog/ai-gpu-rental-market-trends)
- [NVIDIA H200 Price Guide 2026 — JarvisLabs](https://jarvislabs.ai/blog/h200-price)
- [NVIDIA A100 GPU Price 2026 — JarvisLabs](https://jarvislabs.ai/blog/a100-price)
- [NVIDIA H200 SXM on-demand & reserved — Hyperstack](https://www.hyperstack.cloud/nvidia-h200-sxm)

**Historical price trend**
- [H100 Rental Price Over Time (2023–2025) — Silicon Data](https://www.silicondata.com/blog/h100-rental-price-over-time)
- [B200 Index Price March 2026 Update (+24% in a quarter) — Silicon Data](https://www.silicondata.com/blog/b200-rental-price-march-2026-update)
- [The Great GPU Shortage — H100 1-Year Rental Price Index — SemiAnalysis](https://newsletter.semianalysis.com/p/the-great-gpu-shortage-rental-capacity)
- [GPU Cloud Prices Collapse — Introl (Dec 2025)](https://introl.com/blog/gpu-cloud-price-collapse-h100-market-december-2025)
- [Live GPU Rental Listings Point to Early Price Compression — Data Center Knowledge](https://www.datacenterknowledge.com/infrastructure/gpu-rental-markets-show-signs-of-pricing-compression)
- [Nvidia's H100 rental prices surge ~40% in 6 months — Seeking Alpha](https://seekingalpha.com/news/4572260-nvidias-h100-gpu-rental-prices-surge-nearly-40-in-6-months-semianalysis)

**Acquisition cost / GPU pricing**
- [NVIDIA AI GPU Prices: H100 $27K–40K, H200 $315K/8-GPU — IntuitionLabs](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide)
- [Price of Vera Rubin NVL72 racks up to $8.8M — Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/price-of-nvidias-vera-rubin-nvl72-racks-skyrockets-to-as-much-as-usd8-8-million-apiece-but-server-makers-margins-will-be-tight-nvidia-is-moving-closer-to-shipping-entire-full-scale-systems)
- [GTC 2026: Nvidia Unveils Vera Rubin AI Platform — Data Center Knowledge](https://www.datacenterknowledge.com/data-center-chips/gtc-2026-nvidia-unveils-vera-rubin-ai-platform-eyes-1t-by-2027)

**Cost-per-token / consumer surplus / who captures the gains**
- [AI Inference Economics: The 1,000× Cost Collapse — GPUnex](https://www.gpunex.com/blog/ai-inference-economics-2026/)
- [Inference Unit Economics: True Cost Per Million Tokens — Introl](https://introl.com/blog/inference-unit-economics-true-cost-per-million-tokens-guide)
- [AI API Pricing History: GPT-4 $60 to GPT-5.4 $15 — TokenMix](https://tokenmix.ai/blog/ai-pricing-trends-history)
- [AI Inference Cost Economics in 2026 — Spheron](https://www.spheron.network/blog/ai-inference-cost-economics-2026/)

**Utilization and operating economics**
- [CoreWeave Q1 2026 — earnings roundup, neoclouds shift to power wars — Data Center Knowledge](https://www.datacenterknowledge.com/cloud/earnings-roundup-neoclouds-shift-from-gpu-race-to-power-wars)
- [CoreWeave Reaches a New Scale Threshold (>90% utilization) — HyperFRAME Research](https://hyperframeresearch.com/2026/05/11/coreweave-reaches-a-new-scale-threshold-but-can-the-ai-neocloud-sustain-long-tail-demand/)
- [CoreWeave's Q1 earnings: can GPU cloud economics survive the debt — Startup Fortune](https://startupfortune.com/coreweaves-q1-earnings-are-a-live-test-of-whether-gpu-cloud-economics-can-survive-the-debt-they-created/)
- [The Hidden Truth Behind CoreWeave's Gross Margin — Motley Fool](https://www.fool.com/investing/2025/10/29/the-hidden-truth-behind-coreweaves-weirdly-high-gr/)
- [CoreWeave Q1 2026 8-K (SEC)](https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000220/coreweave1q26earningspress.htm)

**Market size / forecast**
- [GPUaaS revenue to reach $130–134B by 2030 — Analysys Mason](https://www.analysysmason.com/research/content/articles/gpuaas-forecast-overview-rma16/)
- [GPU as a Service Market to $37.10B by 2035 — Precedence Research](https://www.precedenceresearch.com/gpu-as-a-service-market)

---

## Open Questions / Uncertainties

1. **Two-sided 2026 market — which way is the H100 actually moving?** Sources disagree: GetDeploying shows H100 on-demand +25% YoY; an FT figure shows smaller-provider H100 −22% YTD; contract pricing is +40% off its Oct-2025 trough. The honest read is "flat-to-up with a very wide spread," but the *net* direction for a generic mid-life GPU is genuinely uncertain and matters for the in-life-decay assumption.

2. **Does the 2026 frontier rebound persist or fade?** The B200/GB200 price increases (+24%/quarter, +35% since mid-2025) are HBM-supply-driven. If HBM capacity normalizes, frontier rates could resume falling — pulling the 2036 projection toward the low (~$8/GPU-hr) end. The projection's central case assumes the rebound *partly* persists; a scenario where it fully unwinds is not modeled.

3. **Supply-constraint vs commoditization — the decade's biggest fork.** [Data Center Knowledge](https://www.datacenterknowledge.com/infrastructure/gpu-rental-markets-show-signs-of-pricing-compression) reports "early signs of pricing compression and infrastructure commoditization." If the H100's 300+-provider price collapse becomes the template for every generation, the 2036 frontier rate could stay near 2026 levels in real terms. If supply stays constrained (fab/packaging/HBM bottlenecks), it rises. This single fork drives most of the ±50% band.

4. **GB200 per-GPU figure is a units artifact.** The ~$17.85/GPU-hr GB200 on-demand average is partly an artifact of the high-power NVL72 superchip form factor and rack-integrated sale — it is not cleanly comparable to a discrete B200 at ~$4.73/hr. The project should standardize on either a discrete-GPU rate or an explicit NVL72-rack rate and not mix them.

5. **V100 and early-A100 launch rates are weakly sourced.** The pre-2022 historical figures are [ESTIMATE] — current price-tracking indices (Silicon Data, GetDeploying) only have good coverage from the H100 era. The "sticky $2–7 band across four generations" claim is robust for A100→B200 and directionally supported but not precisely documented for V100.

6. **Does "toward $1M/GPU" actually happen?** The projection treats a ~10× rise in per-GPU as-sold cost by the 2030s as the brief's stipulated scenario. Whether NVIDIA's pricing power and the silicon/HBM cost curve actually deliver that — versus competition (AMD, custom ASICs, TPUs) capping it — is an open question. If chip cost rises less than 10×, the cost-plus rate rises less than the projected ~2.5×.

7. **The orbital generational-decay derate is not quantified here.** §4.4 flags that an orbital node's realized rate drifts from the frontier figure toward the commoditized figure of its launch generation, because it cannot refresh silicon. The *speed* of that drift — how many years until an orbital B200-class node is earning H100-commoditized-equivalent rates — needs its own modeling and belongs in the calculator as an explicit input.

8. **List vs transacted for hyperscalers.** Hyperscaler figures (AWS/Azure list) are advertised rates; large enterprise buyers transact below list via committed-use discounts not visible in public data. The true hyperscaler-vs-neocloud premium may be somewhat narrower than the list-price spread suggests.
