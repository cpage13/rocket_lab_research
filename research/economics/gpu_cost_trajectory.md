# GPU Cost Trajectory — What It Costs to BUY the Silicon, 2024–2036

*Research date: 2026-05-19. Prepared for the Rocket Lab orbital AI-inference data center feasibility project, to ground the valuation calculator in per-GPU economics. Companion to `economics/rack_cost_trajectory.md` (now partly superseded — see below), `../valuation/ai_compute_trajectory.md`, `economics/hyperscaler_margins.md`.*

> **Scope.** This document is about **acquisition cost** — the price to *buy* AI compute silicon, at the GPU level and the rack-scale-system level, by NVIDIA generation. It is *not* about rental rates, revenue, or operating cost (those live in `revenue_per_watt.md`, `energy_operating_costs.md`). It re-mines and **corrects** the prior `rack_cost_trajectory.md`, whose Vera Rubin rack price was mislabelled and whose "rack price doubles per generation" claim does not survive the latest 2026 data.

> **Reading guide.** Claims are tagged **[FACT]** (company-disclosed or firm reported figure), **[ESTIMATE]** (analyst / leak / press estimate for an unconfirmed number — the dominant category here, because NVIDIA publishes *no* list prices for data-center GPUs or NVL racks), **[DERIVED]** (our arithmetic) or **[PROJECTION]** (directional forecast, explicitly speculative). Every hard number is cited inline. Rows at or before 2026 are historical/near-term; rows after 2026 are **[PROJECTION]** unless noted.

> **Source status (2026-05-25):** See [SOURCE_INDEX.md](../SOURCE_INDEX.md) claim IDs GPU-011 and GPU-012. Rack prices are estimates, not NVIDIA list prices. The GB300 ~$6-6.5M figure is supported by March 2026 reporting but conflicts with later reporting closer to ~$4M for some volume/training configurations. Treat it as a source-date-specific scenario, not a certified universal price.

---

## Summary

**Buying frontier AI silicon gets more expensive every generation — but the per-generation multiplier is ~1.3–2×, not the "doubling" the prior wiki claimed, and it is uneven.** A flagship data-center GPU "as sold" went from ~$10K (A100, 2020) → ~$25–40K (H100, 2022) → ~$30–50K (B200, 2024) → ~$35–55K (B300, 2025–26). The **GB200/GB300 superchip** (1 Grace CPU + 2 Blackwell GPUs) sits at ~$60–70K. At the **rack** level: ~$3M for a GB200 NVL72 → ~$6–6.5M for a GB300 NVL72 → ~$5–7M for the Vera Rubin NVL72 (VR200, shipping H2 2026, *including ~$1M of bundled storage*).

**Two corrections to the existing wiki, both load-bearing:**

1. **The "$7.0–8.8M Vera Rubin rack" figure in `rack_cost_trajectory.md` is mislabelled.** The [March 2026 Tom's Hardware report](https://www.tomshardware.com/tech-industry/artificial-intelligence/price-of-nvidias-vera-rubin-nvl72-racks-skyrockets-to-as-much-as-usd8-8-million-apiece-but-server-makers-margins-will-be-tight-nvidia-is-moving-closer-to-shipping-entire-full-scale-systems) attaches the **$7–8.8M** range to the **NVL144 VR300** config (a later, larger, Rubin-Ultra-adjacent system, ~late-2028). The **standard Vera Rubin NVL72 (VR200)** — the true GB300 successor — is quoted at **~$5–7M**, and ~$1M of that is bundled 3D-NAND storage. So the real GB300→Rubin step is **~$5–7M vs ~$6–6.5M — roughly flat to modestly up, not a 2× jump.** [ESTIMATE]

2. **"Rack price roughly doubles per generation" is too strong.** The only clean ~2× step in the record is **GB200→GB300** (~$3M→~$6M). DGX-A100→DGX-H100 was ~2.2×; DGX-1→DGX-A100 was only ~1.3×; and **GB300→Rubin VR200 is ~flat-to-up (~1.0–1.2×)**. Futurum's published estimate is **~+25% GB200→Rubin**. The honest figure is **~1.3–2× per generation, averaging ~1.5–1.7×, lumpy** — and it is partly *product redefinition* (8-GPU box → 72-GPU rack), not pure inflation.

**The project's "~$6M GB300 NVL72" assumption is source-supported but not certified as a universal price.** March 2026 reporting corroborated **$6–6.5M** for standard configurations. Later reporting closer to **~$3.7–4M** for some hyperscale volume/training configurations means this should be carried as a scenario value with a source date, not as a single verified market price.

**Is ~$1M per GPU "as sold" by 2036 plausible? — Borderline; defensible only at the *aggressive* end, and only if you count a GPU package the way NVIDIA will (multi-die, ~1TB+ HBM).** A frontier GPU package "as sold" today is ~$30–70K. The historical per-GPU CAGR 2020→2026 is ~25–35%/yr. Extending the *observed* ~1.3–1.7×/generation cadence over ~6–7 generations to 2036 lands a frontier package at **~$250–700K (mid case ~$400K)** — *not* $1M. Reaching ~$1M requires the *high* end of every dial simultaneously: ~2×/generation sustained, more compute dies per package (Feynman is reported at ≥8 dies/socket vs Rubin Ultra's 4), ~1TB→multi-TB HBM per package at sharply higher HBM prices, and NVIDIA holding ~75% gross margin against rising custom-silicon competition. **Verdict: ~$1M/GPU by 2036 is a plausible *upside* scenario, not a base case. Base case ~$300–500K; aggressive ~$700K–1.1M.** Confidence on the 2030+ figures is low — these are extrapolations of an observed cadence, not forecasts.

**NVIDIA pricing power is real and has held — but the decade-out assumption is the weakest link.** NVIDIA ran ~75% gross margin Q4 FY2026 ([SEC 8-K](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000019/q4fy26pr.htm)) and has *raised* ASP every generation. But analysts project NVIDIA's inference-compute share falling from ~90% toward **20–30% by 2028** as hyperscaler custom ASICs (Broadcom-designed TPU/Trainium/Maia-class) take ~35–40% of hyperscaler AI spend. The cost-plus, ~2×-per-generation pricing-power assumption is **safe to ~2028 and genuinely uncertain beyond** — a real reason the 2030+ per-GPU projection is bracketed wide.

**Confidence: Moderate overall.** High on 2020–2026 per-GPU street prices and NVIDIA margins (multiply sourced). Moderate on 2024–2026 rack prices (all estimates — NVIDIA confirms none). Low on 2029–2036 (directional extrapolation; ±50–100%).

---

## Cost Table — Per-GPU "As Sold" and Rack-Scale System Price by Generation

**How to read "per-GPU as sold":** the price of one GPU *package/module* as a customer actually buys it — counted the way NVIDIA sells it. A subtlety that matters for 2026+: **NVIDIA changed its counting in the Rubin generation.** Blackwell called a 2-die module "one GPU"; Rubin calls each die "one GPU," so a Rubin *package* (2 compute dies) = "2 Rubin GPUs" in NVIDIA's nomenclature ([TrendForce](https://www.trendforce.com/news/2026/04/01/news-nvidias-rubin-ultra-seen-sticking-to-dual-die-design-on-packaging-constraints-tsmc-3nm-demand-intact/), [Glenn Lockwood](https://www.glennklockwood.com/garden/processors/R200)). The table below is consistent on the **physical package** (what you buy and socket); the "NVIDIA-nomenclature GPU count" is noted separately so the calculator does not double-count.

| Generation (arch) | Year (volume) | Per-GPU **package** "as sold" | Rack-scale system | GPU **packages**/rack | NVIDIA-nomenclature "GPUs"/rack | Tag | Notes |
|---|---|---|---|---|---|---|---|
| **A100** (Ampere) | 2020 | ~$10–17K (40/80GB) | DGX A100 (8-GPU) | 8 | 8 | [FACT] street | ~$10–12K 40GB PCIe; ~$15–17K 80GB. DGX A100 list ~$199K. |
| **H100** (Hopper) | 2022–23 | ~$25–40K street; **~$23–24K NVIDIA ASP** to hyperscalers | DGX/HGX H100 (8-GPU) | 8 | 8 | [FACT/ESTIMATE] | Street $27–40K; SemiAnalysis puts NVIDIA's *actual ASP* at ~$23–24K/GPU. DGX H100 ~$373–480K. |
| **H200** (Hopper) | 2024 | ~$30–40K | HGX/DGX H200 (8-GPU) | 8 | 8 | [ESTIMATE] | ~15–20% over H100. 8× HGX board ~$308–315K. |
| **B200** (Blackwell) | 2024–25 | ~$30–50K (mfg cost ~$6.4K) | DGX B200 (8-GPU); GB200 NVL72 | 8 / 72 | 8 / 72 | [ESTIMATE] | B200 die is 2-reticle; "one GPU" = 2 dies in Blackwell nomenclature. |
| **GB200 superchip** | 2024–25 | **~$60–70K** (1 Grace + 2 B200) | **GB200 NVL72** | 36 superchips = 72 GPUs | 72 | [ESTIMATE] | NVL72 = 36 superchips. Rack **~$2.8–3.4M** (mid ~$3.0–3.2M). |
| **B300 / GB300** (Blackwell Ultra) | 2025–26 | B300 **~$35–55K** (Spheron ~$53K; others $37–44K); GB300 superchip ~$70K+ | **GB300 NVL72** | 36 superchips = 72 GPUs | 72 | [ESTIMATE] | Rack **~$6–6.5M** standard config; Apple reportedly ~$3.7–4M (volume/training). DGX B300 (8-GPU) ~$300–500K. |
| **Rubin R200 / VR200** (Rubin) | H2 2026 | Not separately priced; **~$50–75K/package implied** (2 dies/package) | **Vera Rubin NVL72 (VR200)** | 72 packages (144 dies) | **144** ("NVL144" by die-count nomenclature) | [ESTIMATE] | Rack **~$5–7M incl. ~$1M storage** → ~$4–6M compute-only. Each package = 2 Rubin dies, 288GB HBM4. |
| **Rubin Ultra** | H2 2027 | Not separately priced; **~$120–180K/package implied** | **Rubin Ultra NVL576 ("Kyber")** | 144 packages (576 dies) | **576** | [ESTIMATE/PROJECTION] | JP Morgan estimate: **~$35M/rack**. Die count contested — 4 dies/package (NVIDIA roadmap) vs 2 dies/package (TrendForce, Apr 2026, packaging-limited). |
| **NVL144 VR300** | ~late 2028 | — | NVL144 VR300 rack | — | 144 | [ESTIMATE] | The config the **$7–8.8M** Tom's Hardware figure actually refers to. |
| **Feynman** | ~2028 | **~$150–300K/package** (proj.) | Feynman NVL-class | ≥8 dies/socket | — | [PROJECTION] | ≥8 GPU dies/socket; 3D-stacked, custom HBM, ~2nm. |
| post-Feynman | ~2030 | **~$200–400K/package** (proj.) | (unnamed) | rising | — | [PROJECTION] | Trend extrapolation. |
| — | ~2033 | **~$250–550K/package** (proj.) | (unnamed) | — | — | [PROJECTION] | ±50–100%. |
| — | ~2036 | **~$300–500K base; ~$700K–1.1M aggressive** | (unnamed) | — | — | [PROJECTION] | See §4. ~$1M is the upside, not the base. |

**Caveat that governs the whole table:** NVIDIA has **never published a list price** for any data-center GPU or any NVL rack ([IntuitionLabs, Apr 2026](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide): "Nvidia does not release suggested retail pricing on its GPU accelerators in the datacenter"). Every GPU figure from H100 on, and *every* NVL-rack figure, is a street price, leak, ODM quote, or analyst estimate. Treat individual numbers as ±20–40%; the GB200 (~$3M) and GB300 (~$6–6.5M) racks are the best-corroborated.

---

## 1. Per-GPU Acquisition Cost ("As Sold") by Generation

**What kind of price is this?** GPU pricing is genuinely murky. There are at least four different "prices" in circulation, and sources rarely say which they mean:

- **NVIDIA's ASP** — what NVIDIA actually receives per GPU. *Lowest.* SemiAnalysis estimated H100 ASP at **~$23–24K/GPU** to hyperscalers in 2024–25 ([per IntuitionLabs synthesis](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide); the NYT quoted SemiAnalysis at ~$20–23K after a 2024 price cut). This is the number that drives NVIDIA's revenue and margin.
- **Street / channel price** — what a mid-volume buyer pays a reseller for a bare GPU or an OEM board. *Higher.* H100 SXM ran **~$27–40K** through 2024–25 ([IntuitionLabs](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide), [Jarvislabs H100 guide](https://jarvislabs.ai/blog/h100-price)).
- **Per-GPU-in-a-system price** — system price ÷ GPU count. Carries the CPU, NVSwitch, networking, chassis, cooling share.
- **Manufacturing / BOM cost** — what the silicon+HBM+substrate costs to build. *Lowest of all.* B200 BOM ≈ **$6,400** (~half is HBM); H100 BOM ≈ **$3,320** ([tech-insider via search synthesis](https://tech-insider.org/nvidia-blackwell-gpu-pricing/)). The gap between BOM and ASP is NVIDIA's ~75% gross margin.

### 1.1 Generation-by-generation (per-GPU package, "as sold")

- **A100 (Ampere, 2020)** — A100 40GB PCIe ~**$10–12K**; 80GB ~**$15–17K** ([IntuitionLabs](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide), [CNBC's "$10,000 chip"](https://www.cnbc.com/2023/02/23/nvidias-a100-is-the-10000-chip-powering-the-race-for-ai-.html)). [FACT — well-corroborated.]
- **H100 (Hopper, 2022–23)** — street **~$25–40K**; SXM5 at the top of that band. NVIDIA's *actual ASP* ~**$23–24K** (SemiAnalysis). The spread *is* the channel markup. [FACT/ESTIMATE.]
- **H200 (Hopper, 2024)** — ~**$30–40K**, roughly **+15–20%** over H100 ([Jarvislabs H200 guide](https://jarvislabs.ai/blog/h200-price), [IntuitionLabs](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide)). Same die as H100, more/faster HBM — the increment is essentially the HBM upgrade. [ESTIMATE.]
- **B200 (Blackwell, 2024–25)** — estimates **~$30–50K** ([IntuitionLabs](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide)). Jensen Huang publicly floated **$30–40K** for "a Blackwell GPU," then clarified NVIDIA sells systems, not bare chips ([Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/nvidias-jensen-huang-says-blackwell-gpu-to-cost-dollar30000-dollar40000-later-clarifies-that-pricing-will-vary-as-they-wont-sell-just-the-chip)). The B200 "GPU" is a 2-reticle-die package; B200 mfg cost ~$6,400. [ESTIMATE.]
- **B300 (Blackwell Ultra, 2025–26)** — sources disagree: Spheron quotes a single B300 at **~$53,000** ([Spheron B300 guide, Apr 2026](https://www.spheron.network/blog/nvidia-b300-blackwell-ultra-guide/)); IntuitionLabs derives **~$37.5–43.75K** from DGX B300 system pricing. Apple reportedly paid **~$51–55K/GPU** for GB300 racks. Call it **~$35–55K**, ~10–25% over B200, with the increment again driven by HBM (192→288GB). [ESTIMATE — genuine source disagreement.]
- **GB200 / GB300 superchip** — the **superchip** (1 Grace CPU + 2 Blackwell GPUs, sold as a unit) is the cleanest "as sold" object for the Blackwell rack generation: **~$60–70K** for GB200 ([Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/nvidias-next-gen-blackwell-ai-gpus-to-cost-up-to-dollar70000-fully-equipped-servers-range-up-to-dollar3000000-report), [TweakTown](https://www.tweaktown.com/news/98292/nvidias-new-gb200-superchip-costs-up-to-70-000-full-b200-nvl72-ai-server-3-million/index.html)); GB300 superchip **~$70K+**. [ESTIMATE.]
- **Rubin R200 (Rubin, H2 2026)** — **not separately priced**; NVIDIA now sells Rubin almost exclusively as rack-scale systems. Backing it out of the ~$5–7M VR200 NVL72 rack (less ~$1M storage, less CPU/switch/networking/chassis) implies very roughly **~$50–75K per Rubin package** (2 dies, 288GB HBM4). In NVIDIA's new die-count nomenclature that package = "2 Rubin GPUs," so **~$25–38K per nomenclature-GPU** — *do not* compare that number directly to an H100 "GPU." [ESTIMATE/DERIVED — low confidence.]

### 1.2 Is per-GPU price rising? — Yes, but ~25–35%/yr, not "doubling"

Per-GPU **package** "as sold," frontier part, street-price basis:

~$10–17K (A100, 2020) → ~$25–40K (H100, 2022) → ~$30–40K (H200, 2024) → ~$30–50K (B200, 2024–25) → ~$35–55K (B300, 2025–26).

That is roughly **3–4× over six years on a like-for-like single-package basis** — a CAGR of **~25–35%/yr**, *not* a per-generation doubling. The doubling story comes from (a) comparing a *superchip* (2 GPUs + CPU, ~$60–70K) to a single earlier GPU, or (b) comparing *racks*, where the unit of sale was redefined (§2). On a consistent single-package basis the per-GPU climb is real but more like **~1.3–1.7× per ~18-month generation**. Memory is now the dominant cost driver: HBM is ~half the B200 BOM, and SK Hynix/Samsung pushed a **~20% HBM3E price hike for 2026** ([IntuitionLabs](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide)), with AMD warning of **≥10% accelerator price increases in 2026** attributable to memory inflation.

---

## 2. Rack-Scale System Price by Generation

NVIDIA made the **rack** the unit of sale around 2024 ("the rack is the new server"). This is the decision-relevant unit for the orbital project — an orbital node is essentially one rack.

| Rack-scale system | Year | System price | Basis / confidence | Source |
|---|---|---|---|---|
| DGX-1 (8× V100) | 2017 | **$149,000** | [FACT] confirmed list | [TweakTown](https://www.tweaktown.com/news/57487/nvidias-new-volta-powered-dgx-1-costs-149-000/index.html) |
| DGX A100 (8× A100) | 2020 | **~$199,000** | [FACT] confirmed suggested | [NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-ships-worlds-most-advanced-ai-system-nvidia-dgx-a100-to-fight-covid-19-third-generation-dgx-packs-record-5-petaflops-of-ai-performance) |
| DGX H100 (8× H100) | 2022–23 | **~$373,000–480,000** | [FACT/ESTIMATE] reported | [Wikipedia DGX](https://en.wikipedia.org/wiki/Nvidia_DGX), [cyfuture](https://cyfuture.cloud/kb/gpu/nvidia-dgx-h100-price-2025-cost-specs-and-market-insights) |
| **GB200 NVL72** (72 GPU) | 2024–25 | **~$2.8–3.4M** (mid ~$3.0–3.2M) | [ESTIMATE] leak/analyst (HSBC) | [Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/nvidias-next-gen-blackwell-ai-gpus-to-cost-up-to-dollar70000-fully-equipped-servers-range-up-to-dollar3000000-report), [Spheron GB200 guide](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/) |
| **GB300 NVL72** (72 GPU) | 2025–26 | **~$6–6.5M** standard; ~$3.7–4M reported volume (Apple) | [ESTIMATE] | [Yahoo/Tom's Hardware Mar 2026](https://finance.yahoo.com/sectors/technology/articles/price-nvidias-vera-rubin-nvl72-100000086.html), [tae kim/Bloomberg](https://x.com/firstadopter/status/1940792115124228482) |
| **Vera Rubin NVL72 (VR200)** (72 packages / 144 dies) | H2 2026 | **~$5–7M incl. ~$1M storage** → ~$4–6M compute-only | [ESTIMATE] reported | [Tom's Hardware Mar 2026](https://www.tomshardware.com/tech-industry/artificial-intelligence/price-of-nvidias-vera-rubin-nvl72-racks-skyrockets-to-as-much-as-usd8-8-million-apiece-but-server-makers-margins-will-be-tight-nvidia-is-moving-closer-to-shipping-entire-full-scale-systems), [Barrack AI](https://blog.barrack.ai/nvidia-rubin-specs-architecture-2026/) |
| **NVL144 VR300** | ~late 2028 | **~$7–8.8M** | [ESTIMATE] | [Tom's Hardware Mar 2026](https://www.tomshardware.com/tech-industry/artificial-intelligence/price-of-nvidias-vera-rubin-nvl72-racks-skyrockets-to-as-much-as-usd8-8-million-apiece-but-server-makers-margins-will-be-tight-nvidia-is-moving-closer-to-shipping-entire-full-scale-systems) |
| **Rubin Ultra NVL576** ("Kyber") | H2 2027 | **~$35M** | [ESTIMATE] JP Morgan | [JP Morgan via Beth Kindig](https://x.com/Beth_Kindig/status/1992293443645952437), [DCD](https://www.datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027/) |

**The two corrections in detail:**

**Correction A — the Vera Rubin rack price was mislabelled in `rack_cost_trajectory.md`.** That doc attached **$7.0–8.8M** to the "VR200 NVL72." The decisive source is the [Yahoo Finance reprint of the Tom's Hardware report (24 Mar 2026)](https://finance.yahoo.com/sectors/technology/articles/price-nvidias-vera-rubin-nvl72-100000086.html), which is explicit: the **VR200 NVL72** is quoted at **$5–7M** (incl. ~$1M of 3D-NAND storage), while the **$7–8.8M** range is the **NVL144 VR300** — a larger, later config not expected in volume until ~late 2028. The prior wiki's relabelling note got the *direction* of the fix wrong. **Correct mapping:** GB300 NVL72 ≈ $6–6.5M → Vera Rubin VR200 NVL72 ≈ $5–7M. The Rubin rack is **not** a 2× step over GB300 — it is roughly flat-to-modestly-up. Futurum independently estimates Rubin at **~+25% over Grace Blackwell**, landing ~$3.5–4M in *their* (lower, training-config) GB200 baseline — consistent with "modest single-generation increase," not doubling.

**Correction B — the GB200→Rubin step is the cleanest evidence against "doubles per generation."** Note also that NVIDIA's *content* is not exploding either: the GB300 NVL72 liquid-cooling BOM is **~$49,860/rack**, rising only to **~$55,710** for the Vera Rubin NVL144 — **+17%**, not +100% ([Tom's Hardware cooling cost](https://www.tomshardware.com/pc-components/cooling/cooling-system-for-a-single-nvidia-blackwell-ultra-nvl72-rack-costs-a-staggering-usd50-000-set-to-increase-to-usd56-000-with-next-generation-nvl144-racks)).

**Why ODM quotes muddy this.** The Tom's Hardware report stresses that many circulating quotes are **ODM prices without a proper warranty**, and that NVIDIA now supplies **fully-assembled "Level-10" compute trays representing ~90% of system cost** — so the "rack price" is increasingly NVIDIA's price, with thin ODM margin on top. The orbital project should treat the rack figure as **NVIDIA-set**, not channel markup — which means it tracks NVIDIA's pricing power directly (§5).

---

## 3. The Cost-Growth Multiplier — "Doubles Per Generation"?

The prior wiki claims rack price "roughly doubles per generation." **The latest data does not support that as a general rule.** Here is the actual record:

| Step | Multiplier | Note |
|---|---|---|
| DGX-1 → DGX A100 (2017→2020) | **~1.3×** | $149K → $199K |
| DGX A100 → DGX H100 (2020→2022) | **~2.0–2.4×** | $199K → ~$400–480K |
| DGX H100 → GB200 NVL72 (2022→2024) | **~7–8×** | **product redefined** — 8-GPU box → 72-GPU rack. Not a like-for-like generation step. |
| GB200 NVL72 → GB300 NVL72 (2024→2025–26) | **~2.0×** | $3M → $6–6.5M. The one clean ~2× step. |
| GB300 NVL72 → Vera Rubin VR200 NVL72 (2025–26→2026) | **~0.9–1.2×** | $6–6.5M → $5–7M. **Flat to modestly up.** |
| Vera Rubin VR200 → Rubin Ultra NVL576 (2026→2027) | **~5–7×** | $5–7M → ~$35M — but **GPU count 72→144 packages (576 dies)**: another product redefinition, not pure price growth. |

**Reading it honestly:**

- **It is per-rack, and it is lumpy.** The clean *generation-to-generation* steps (holding the product roughly constant) are ~1.3× (A100→H100 DGX), ~2× (GB200→GB300), ~1× (GB300→Rubin). Average ≈ **1.3–1.5×**, *not* 2×.
- **The big jumps are product redefinitions.** DGX-H100→GB200 (~7×) and Rubin→Rubin Ultra (~5–7×) are NVIDIA *changing what a "rack" is* — from 8 GPUs to 72, then 72 packages to 144. Per-GPU-package, those steps are far smaller. On a **per-GPU-package** basis the multiplier is the cleaner ~1.3–1.7×/generation of §1.2.
- **So the corrected claim:** *rack acquisition cost rises ~1.3–2× per generation (averaging ~1.5–1.7×, occasionally a clean 2× as in GB200→GB300, occasionally flat as in GB300→Rubin), with periodic ~5–8× discontinuities when NVIDIA enlarges the rack definition.* "Doubles every generation" overstates the steady-state and understates the discontinuities.
- **Per-GPU vs per-rack:** for a fixed rack definition (NVL72), per-rack and per-GPU-package move together (~1.3–1.7×/gen). The divergence is entirely the discontinuities — when the rack grows from NVL72 to NVL576, per-rack jumps ~5–8× while per-GPU-package stays on its ~1.5×/gen path.

**For the calculator:** model rack acquisition cost as **~1.5×/generation** on the smooth segment, with an explicit **step-up event** if/when the modelled node adopts a larger rack class (NVL72 → NVL144 → NVL576). Do not apply a flat 2×.

---

## 4. Projection to 2036 — Is ~$1M Per GPU "As Sold" Plausible?

**Anything past ~2028 is projection.** NVIDIA's public roadmap is firm only through Rubin Ultra (H2 2027) and named-but-thin for Feynman (2028). 2029–2036 is extrapolation. Confidence: **low.** What follows is a *directional* range with explicit drivers.

### 4.1 The per-GPU-package projection

Starting point: a frontier GPU **package** "as sold" is ~$30–70K today (single B300/Rubin-package band; the superchip is ~$70K). Take ~$50K as a round mid-anchor for a frontier package in 2026.

Three scenarios, each compounding from 2026 to 2036 (~6–7 generations at an ~18-month cadence):

| Scenario | Per-generation multiplier | 2036 per-GPU-package "as sold" | What it assumes |
|---|---|---|---|
| **Conservative** | ~1.3×/gen | **~$250–350K** | Competition caps NVIDIA; HBM inflation moderate; modest die-count growth. |
| **Base** | ~1.5×/gen | **~$350–550K** | Observed cadence holds; steady die-count + HBM growth; NVIDIA margin ~70%. |
| **Aggressive** | ~1.9–2×/gen | **~$700K–1.1M** | Pricing power fully intact; ≥8-die packages (Feynman+); multi-TB HBM at high prices; NVIDIA holds ~75%. |

**Verdict on ~$1M/GPU by 2036:** it lands **only in the aggressive scenario**, and only if "GPU" means a *large multi-die package* counted NVIDIA's way. **It is a plausible upside case, not the base case.** The base case is **~$350–550K per frontier GPU package**. The honest one-line answer: *~$1M/GPU by 2036 is reachable but requires the high end of essentially every dial at once — treat it as the optimistic bound of a $300K–1.1M range.*

A second framing confirms this. The historical per-GPU-package CAGR 2020→2026 is **~25–35%/yr**. Sustained to 2036 (10 more years): at 25%/yr, $50K → ~$465K; at 30%/yr → ~$690K; at 35%/yr → ~$1.0M. So **~$1M/GPU by 2036 implies the per-GPU price CAGR holding at its *historical top end* (~35%/yr) for a full decade** — possible, but it requires no deceleration despite mounting competition. Most likely the CAGR decays toward ~15–20%/yr in the 2030s as custom silicon bites, landing the base case at ~$300–500K.

### 4.2 What would DRIVE a higher per-GPU price

1. **More compute dies per package.** This is the single biggest lever and it is *already happening*. Blackwell = 2 dies/"GPU." Rubin = 2 compute dies/package. Rubin Ultra = **4 dies/package** (NVIDIA roadmap; though [TrendForce, Apr 2026](https://www.trendforce.com/news/2026/04/01/news-nvidias-rubin-ultra-seen-sticking-to-dual-die-design-on-packaging-constraints-tsmc-3nm-demand-intact/) reports packaging limits may force it back to 2). Feynman is reported at **≥8 GPU dies per socket** ([Tom's Hardware roadmap](https://www.tomshardware.com/pc-components/gpus/nvidia-updates-data-center-roadmap-with-rosa-cpu-and-stacked-feynman-gpus-optical-nvlink-groq-lpus-with-nvfp4-and-nvlink-also-on-deck)). If a "GPU package" in 2032+ contains 8–16 dies, a ~$1M *package* price is almost arithmetic — it is ~8–16 dies × ~$60–120K/die-equivalent. **The ~$1M question partly dissolves into "how many dies does NVIDIA bundle into the thing it calls one GPU."**
2. **More HBM per package, at higher HBM prices.** HBM is ~half of GPU BOM today and rising. Per-package HBM: 192GB (B200) → 288GB (Rubin R200) → ~1TB (Rubin Ultra) → multi-TB (Feynman "custom HBM"). HBM price is inflating (~20% hike for 2026). More HBM × pricier HBM compounds hard into package cost.
3. **Larger NVLink domains / rack redefinition.** Each time NVIDIA enlarges the rack (NVL72→144→576→...), per-*rack* price jumps ~5–8×; per-package price rides a smaller curve. If the project's "node" tracks the flagship rack class, its acquisition cost steps up at each redefinition.
4. **NVIDIA pricing power (cost-plus + scarcity).** NVIDIA has *raised* ASP every generation and held ~75% gross margin (§5). If that persists, price growth outruns BOM growth.
5. **Process & packaging cost inflation.** TSMC 3nm→2nm wafer prices and advanced-packaging (CoWoS) costs rise each node; NVIDIA passes them through.

### 4.3 What would CAP the per-GPU price

1. **Custom-silicon competition** (the big one — §5). If NVIDIA's inference share falls toward 20–30% by 2028 as analysts project, NVIDIA loses the ability to price purely cost-plus. Hyperscaler ASICs (TPU, Trainium, Maia) cost roughly **half** a comparable Blackwell system ([WCCFtech/Morgan Stanley](https://wccftech.com/nvidia-blackwell-costs-twice-as-much-as-google-and-amazons-custom-ai-chips-yet-morgan-stanley-says-its-worth-it/)) — a standing price ceiling.
2. **AMD.** MI400-series ASP is ~**$31K** ([tech-insider MI400](https://tech-insider.org/amd-mi400-series-ai-gpu-data-center-2026/)) — below NVIDIA's frontier band, competitive on HBM capacity, and now anchored by a ~$60B Meta commitment.
3. **A capex-cycle slowdown.** The 2024–26 AI-infrastructure supercycle is the engine of NVIDIA's pricing power. A demand cooling would flip GPU pricing from "make money while you can" to competitive — exactly the H100 pattern (street price fell from shortage-era highs as supply caught up).
4. **A precision / capability plateau.** If per-die compute gains slow (precision floor near FP4, transistor scaling slowing), buyers have less reason to pay up for each new generation.
5. **Buyer concentration.** A handful of hyperscalers buy most frontier silicon and increasingly dual-source — concentrated buyers with a credible in-house alternative cap a monopolist's price.

### 4.4 Net read for the orbital project

For the calculator's trajectory layer: model the **frontier GPU package "as sold"** rising from ~$30–70K (2026) to a **2036 range of ~$300K (conservative) – ~$500K (base) – ~$1.1M (aggressive)**, i.e. roughly **~1.3–1.5×/generation base case**, with the explicit understanding that a large share of any high-end outcome is *die-count bundling*, not pure price inflation. For **rack-scale** acquisition cost, use ~1.5×/generation on the smooth segment with step-ups at rack-class changes — *not* a flat 2×. And flag, prominently, that the 2030+ figures rest on NVIDIA's pricing power surviving the custom-silicon inflection — the project's softest single assumption past 2028.

---

## 5. NVIDIA Pricing Power — Does Cost-Plus Hold a Decade Out?

### 5.1 The pricing power is real and currently intact [FACT]

- **Gross margin ~75%.** NVIDIA Q4 FY2026 (quarter ended 25 Jan 2026): GAAP gross margin **75.0%**, non-GAAP **75.2%** ([NVIDIA 8-K, FY2026 Q4](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000019/q4fy26pr.htm)). Full-year FY2026 was lower at **71.1%** — pulled down by an early-FY2026 inventory/charge episode — but the *exit run-rate is back at ~75%*, the level NVIDIA held across V100→Hopper→Blackwell.
- **It is a 78%+-data-center company.** FY2026 revenue **$215.9B** (+65% YoY); Q4 data-center revenue **$62.3B** (+75% YoY) ([ServeTheHome](https://www.servethehome.com/nvidia-reports-q4-fy2026-earnings-data-center-and-proviz-drive-revenue-records/), [Fortune](https://fortune.com/2026/02/25/nvidia-nvda-earnings-q4-results-jensen-huang/)).
- **ASP rises every generation.** B200 mfg cost is ~93% above H100's (~$6,400 vs ~$3,320), and NVIDIA pushed a **~43% ASP increase** at the Blackwell generation while *holding ~75%+ margin* — i.e. it passed through cost *and* kept the markup. NVIDIA does **not** publish list prices precisely because opacity supports price discrimination.
- **The moat:** CUDA software lock-in + scarcity + the rack-scale system bundle (NVLink, networking, "Level-10" trays). Buyers pay for the integrated, de-risked, supported system — and NVIDIA increasingly *is* the system integrator.

### 5.2 The competitive threat is genuine and rising [FACT / ESTIMATE]

- **Custom silicon (the main threat).** [Introl's "Custom Silicon Inflection 2026"](https://introl.com/blog/custom-silicon-inflection-2026-hyperscaler-asics-nvidia-gpu) and corroborating analysts project NVIDIA's **inference-compute share falling from ~90% toward 20–30% by 2028**, with custom ASICs taking **~35–40% of hyperscaler AI spend**. Custom silicon is projected to grow from ~21% of the AI-accelerator market (2025) to ~28% (2026), and **ASIC unit shipments may surpass GPU shipments by 2027**.
- **Broadcom** designs the bulk of hyperscaler AI ASICs (Google TPU, Meta, Microsoft Maia) — ~60% share of that design market, custom-AI-processor shipments projected to **triple by 2027** ([BigGo/Broadcom](https://finance.biggo.com/news/8d5mCpwBT1cp21-d45vN)). Morgan Stanley's read: NVIDIA Blackwell costs **~2× a comparable Google/Amazon custom chip** — yet argues it is still "worth it" on performance/TCO. That "~2×" *is* the price ceiling NVIDIA operates under.
- **AMD** — MI400-series ASP ~$31K, competitive HBM, ~$60B Meta deal (~6GW of custom MI450) — a credible #2 that caps the *floor*.
- **The countervailing fact:** even amid all this, H100 *rental* prices *rose* ~40% off their late-2025 trough into 2026, and NVIDIA's order book is multi-quarter. Demand has, so far, outrun every competitive incursion.

### 5.3 The verdict for a 10-year model

- **Through ~2028:** the cost-plus, ~75%-margin, ASP-rises-every-generation assumption is **safe.** NVIDIA's roadmap (Rubin, Rubin Ultra), backlog, and CUDA moat are intact; competition is real but NVIDIA still holds the frontier-training and flexible-inference market.
- **2029–2036:** **genuinely uncertain.** The most likely path is **not** a margin collapse but a **gradual erosion** — NVIDIA keeps the frontier-training and flexible-inference premium, cedes commodity/high-volume inference to custom ASICs, and its *blended* margin drifts from ~75% toward ~60–70%. In that world per-GPU *price* still rises, but ~1.3–1.5×/generation (base case), not ~2×.
- **What this does to the projection:** it is exactly why §4's 2036 range is bracketed so wide. The **aggressive ~$1M/GPU outcome implicitly assumes NVIDIA defeats the custom-silicon inflection** and holds cost-plus pricing for a decade. That is possible — CUDA lock-in has defeated every prior challenger — but it is a bet, not a baseline. The **base case ($350–550K)** assumes the inflection bites and NVIDIA's pricing power *erodes but does not break*.

---

## Sources

**Rack & per-GPU pricing — Blackwell / GB200 / GB300**
- [Tom's Hardware — Blackwell superchips up to $70K, racks up to $3M+](https://www.tomshardware.com/pc-components/gpus/nvidias-next-gen-blackwell-ai-gpus-to-cost-up-to-dollar70000-fully-equipped-servers-range-up-to-dollar3000000-report)
- [Tom's Hardware — Jensen Huang: Blackwell GPU $30K–40K (later clarified)](https://www.tomshardware.com/pc-components/gpus/nvidias-jensen-huang-says-blackwell-gpu-to-cost-dollar30000-dollar40000-later-clarifies-that-pricing-will-vary-as-they-wont-sell-just-the-chip)
- [TweakTown — GB200 superchip up to $70K; B200 NVL72 ~$3M](https://www.tweaktown.com/news/98292/nvidias-new-gb200-superchip-costs-up-to-70-000-full-b200-nvl72-ai-server-3-million/index.html)
- [Spheron — GB200 NVL72 guide (~$2.8–3.4M)](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/)
- [Spheron — NVIDIA B300 / Blackwell Ultra guide (B300 ~$53K; DGX B300 ~$400–500K) — Apr 2026](https://www.spheron.network/blog/nvidia-b300-blackwell-ultra-guide/)
- [tae kim (X) — GB200 NVL72 ~$3M/rack; "price moves in one direction"](https://x.com/firstadopter/status/1940792115124228482)
- [Guru3D — GB300 NVL72 cooling ~$50K/rack](https://www.guru3d.com/story/3f5782f43f98056f6165e6938b8fa0f8e06adaeb/)

**Vera Rubin / Rubin Ultra rack pricing**
- [Tom's Hardware — Vera Rubin NVL72 racks up to $8.8M apiece; ODM vs warranty pricing (Mar 2026)](https://www.tomshardware.com/tech-industry/artificial-intelligence/price-of-nvidias-vera-rubin-nvl72-racks-skyrockets-to-as-much-as-usd8-8-million-apiece-but-server-makers-margins-will-be-tight-nvidia-is-moving-closer-to-shipping-entire-full-scale-systems)
- [Yahoo Finance reprint — Vera Rubin NVL72 pricing: VR200 $5–7M, NVL144 VR300 $7–8.8M (24 Mar 2026)](https://finance.yahoo.com/sectors/technology/articles/price-nvidias-vera-rubin-nvl72-100000086.html)
- [Tom's Hardware — cooling cost $49,860 (GB300) → $55,710 (Vera Rubin NVL144), +17%](https://www.tomshardware.com/pc-components/cooling/cooling-system-for-a-single-nvidia-blackwell-ultra-nvl72-rack-costs-a-staggering-usd50-000-set-to-increase-to-usd56-000-with-next-generation-nvl144-racks)
- [Barrack AI — NVIDIA Rubin specs & architecture: VR200 NVL72 ~$3.5–4M est. (2026)](https://blog.barrack.ai/nvidia-rubin-specs-architecture-2026/)
- [The Next Platform — Vera Rubin obsoletes current AI iron (Jan 2026)](https://www.nextplatform.com/ai/2026/01/06/nvidias-vera-rubin-platform-obsoletes-current-ai-iron-six-months-ahead-of-launch/4092179)
- [Tom's Hardware — Vera Rubin NVL72 launched at CES; 5× inference, 10× lower cost/token](https://www.tomshardware.com/pc-components/gpus/nvidia-launches-vera-rubin-nvl72-ai-supercomputer-at-ces-promises-up-to-5x-greater-inference-performance-and-10x-lower-cost-per-token-than-blackwell-coming-2h-2026)
- [JP Morgan estimate via Beth Kindig (X) — Rubin Ultra NVL576 rack ~$35M](https://x.com/Beth_Kindig/status/1992293443645952437)
- [DCD — Rubin Ultra NVL576 rack 600 kW, H2 2027](https://www.datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027/)
- [NVIDIA Technical Blog — Vera Rubin POD: seven chips, five rack-scale systems](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/)

**Per-GPU street prices & nomenclature — H100/H200/A100/Rubin**
- [IntuitionLabs — NVIDIA AI GPU pricing guide (A100/H100/H200/B200/B300; "no MSRP") — Apr 2026](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide)
- [Jarvislabs — H100 price guide 2026](https://jarvislabs.ai/blog/h100-price)
- [Jarvislabs — H200 price guide 2026](https://jarvislabs.ai/blog/h200-price)
- [CNBC — Nvidia's A100, the "$10,000 chip"](https://www.cnbc.com/2023/02/23/nvidias-a100-is-the-10000-chip-powering-the-race-for-ai-.html)
- [Glenn Lockwood — NVIDIA Rubin R200 notes (die count / nomenclature)](https://www.glennklockwood.com/garden/processors/R200)
- [TrendForce — Rubin Ultra dual-die vs quad-die; packaging constraints (Apr 2026)](https://www.trendforce.com/news/2026/04/01/news-nvidias-rubin-ultra-seen-sticking-to-dual-die-design-on-packaging-constraints-tsmc-3nm-demand-intact/)

**DGX historical pricing**
- [TweakTown — DGX-1 Volta at $149,000](https://www.tweaktown.com/news/57487/nvidias-new-volta-powered-dgx-1-costs-149-000/index.html)
- [NVIDIA Newsroom — DGX A100 launch (~$199K)](https://nvidianews.nvidia.com/news/nvidia-ships-worlds-most-advanced-ai-system-nvidia-dgx-a100-to-fight-covid-19-third-generation-dgx-packs-record-5-petaflops-of-ai-performance)
- [Wikipedia — Nvidia DGX (DGX H100 list price)](https://en.wikipedia.org/wiki/Nvidia_DGX)
- [cyfuture — DGX H100 price 2025 (~$373K)](https://cyfuture.cloud/kb/gpu/nvidia-dgx-h100-price-2025-cost-specs-and-market-insights)

**NVIDIA margins, roadmap & competition**
- [NVIDIA — Q4 FY2026 8-K press release (75.0% GAAP gross margin Q4; 71.1% FY)](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000019/q4fy26pr.htm)
- [ServeTheHome — NVIDIA Q4 FY2026 earnings (data-center revenue $62.3B)](https://www.servethehome.com/nvidia-reports-q4-fy2026-earnings-data-center-and-proviz-drive-revenue-records/)
- [Fortune — NVIDIA Q4 FY2026 ($68B revenue)](https://fortune.com/2026/02/25/nvidia-nvda-earnings-q4-results-jensen-huang/)
- [Introl — Custom Silicon Inflection 2026 (NVIDIA inference share → 20–30% by 2028)](https://introl.com/blog/custom-silicon-inflection-2026-hyperscaler-asics-nvidia-gpu)
- [BigGo — Broadcom to triple ASIC shipments by 2027](https://finance.biggo.com/news/8d5mCpwBT1cp21-d45vN)
- [WCCFtech — Blackwell costs ~2× custom AI chips; Morgan Stanley says worth it](https://wccftech.com/nvidia-blackwell-costs-twice-as-much-as-google-and-amazons-custom-ai-chips-yet-morgan-stanley-says-its-worth-it/)
- [tech-insider — AMD MI400 series (ASP ~$31K)](https://tech-insider.org/amd-mi400-series-ai-gpu-data-center-2026/)
- [Tom's Hardware — NVIDIA roadmap: Feynman stacked GPUs, ≥8 dies/socket](https://www.tomshardware.com/pc-components/gpus/nvidia-updates-data-center-roadmap-with-rosa-cpu-and-stacked-feynman-gpus-optical-nvlink-groq-lpus-with-nvfp4-and-nvlink-also-on-deck)
- [Tom's Hardware — NVIDIA enterprise roadmap: Rubin, Rubin Ultra, Feynman](https://www.tomshardware.com/tech-industry/semiconductors/nvidia-enterprise-roadmap-rubin-rubin-ultra-feynman-and-silicon-photonics)

*Project-internal companions: `economics/rack_cost_trajectory.md` (partly superseded — Vera Rubin rack mislabel corrected here), `../valuation/ai_compute_trajectory.md`, `economics/hyperscaler_margins.md`, `economics/revenue_per_watt.md`.*

---

## Open Questions / Uncertainties

1. **NVIDIA publishes no list prices — every figure here is an estimate.** The GB200 (~$3M) and GB300 (~$6–6.5M) racks are the best-corroborated; the Vera Rubin VR200 ($5–7M) and Rubin Ultra ($35M) figures rest on fewer sources and should be re-verified as those systems ship in volume (H2 2026 / H2 2027).

2. **The GB300 NVL72 price has a 2× internal spread.** Standard-config reporting says $6–6.5M; Apple reportedly paid ~$3.7–4M/rack. This is probably volume discount + config (training vs inference) + ODM-vs-warranty, but it is unresolved — and it materially changes any per-node CapEx built on "the GB300 rack price."

3. **Rubin Ultra die count is contested.** NVIDIA's roadmap says **4 compute dies/package**; [TrendForce (Apr 2026)](https://www.trendforce.com/news/2026/04/01/news-nvidias-rubin-ultra-seen-sticking-to-dual-die-design-on-packaging-constraints-tsmc-3nm-demand-intact/) reports packaging-yield limits may force **2 dies/package**. This swings the per-package "as sold" price and the meaning of "NVL576" (576 dies regardless, but packages = 144 or 288).

4. **"Per-GPU" is becoming an unstable unit.** NVIDIA changed its counting in the Rubin generation (each die = "one GPU"), and packages are absorbing more dies (2 → 4 → ≥8 by Feynman). Any per-GPU price series past 2026 must state explicitly whether it counts *dies*, *NVIDIA-nomenclature GPUs*, or *physical packages* — otherwise the ~$1M-by-2036 question is ill-posed. This document standardises on the **physical package**; the calculator must pick one and hold it.

5. **The 2030+ projection rests on NVIDIA pricing power surviving the custom-silicon inflection.** If NVIDIA's inference share falls to 20–30% by 2028 as analysts project, post-2028 per-GPU price growth likely decelerates to ~1.3×/generation — putting the 2036 figure near $300–400K, not $1M. The aggressive scenario assumes NVIDIA defeats the inflection; that is a bet.

6. **HBM is now the swing cost and HBM pricing is its own forecast.** ~Half of GPU BOM is HBM; HBM prices are inflating (~20% for 2026) and capacity is constrained. A per-GPU cost projection is partly an HBM-supply-and-price projection — a separate uncertainty not modelled here.

7. **Acquisition cost ≠ node cost.** This document covers only the silicon purchase price. For the orbital project, the rack is one input to node CapEx alongside the bus, power/thermal hardware, integration, and launch. The companion `ai_compute_trajectory.md` and `simulations/REPORT.md` carry node-level cost; this doc should feed the *rack acquisition* line only.

8. **A capex-cycle slowdown is the unmodelled tail risk.** Every projection here assumes the AI-infrastructure supercycle persists. A demand cooling would flip GPU pricing from "make money while you can" to competitive within ~1–2 generations — exactly the H100 post-shortage pattern — and would invalidate the upper half of every range above.
