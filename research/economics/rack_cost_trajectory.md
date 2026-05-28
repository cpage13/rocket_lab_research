# Rack Cost Trajectory: AI Compute Hardware Pricing, 2014–2027

*Research date: May 2026. Prepared for the orbital AI-inference data-center feasibility study (Neutron-launched node).*

> **Superseded launch-cost basis (wave-9, 2026-05-17).** This document was
> written before the wave-9 launch-cost re-base. Its Summary, the §6
> launch-share ladder (94.6%→72.4%), and every payback figure are computed on a
> **fixed ~$50–55M Neutron launch ($52.5M midpoint)** — the *external customer
> price*. The project has since adopted Rocket Lab's **internal marginal launch
> cost of ~$10–20M** (`CONCLUSION.md` Rev 4; `RESEARCH_TRACKER.md` wave-9
> founder input). On the current basis, launch is roughly **~45% of a ~$45M-mid
> node**, not ~85–95%. **The direction of this doc's conclusion is unaffected**
> — a fixed launch cost still becomes a smaller share of node cost as rack
> price rises, so payback still improves generation-over-generation on the same
> rocket. Only the absolute launch-share percentages and the worked payback
> *years* below are stale; treat them as illustrative of the *mechanism*, not as
> live figures. Use `CONCLUSION.md` Rev 4–7 and `data_science/INVESTOR_PROJECTION.md`
> for current node economics.
>
> **Vera Rubin rack-price correction (2026-05-17).** Earlier text in this doc
> attributed the reported **~$7.0–8.8M** rack price to the "Vera Rubin
> **NVL144**." The cited Tom's Hardware article is in fact headlined for the
> **VR200 NVL72** rack ("Vera Rubin NVL72 racks ... up to $8.8 million"). The
> ~$7.0–8.8M figure has been **relabelled to the VR200 NVL72** throughout. This
> is a labelling fix only — the §3 price-per-FLOP conclusion (price-per-FLOP
> flat-to-falling as the sticker price climbs) does **not** shift, because the
> compute figures cited alongside (3.6 NVFP4 EFLOPS) are NVL144-class and the
> comparison is re-stated below on a like-for-like NVL72 basis.

## Summary

**The price of flagship AI compute is rising sharply, generation over generation — at both the per-GPU and the per-rack level — and the rise is accelerating.** A flagship data-center GPU cost roughly $5,700 (Pascal P100, 2016) and now costs $60,000–70,000 (GB200 superchip, 2024) — an ~11× rise in 8 years. At the rack/system level the climb is even steeper and more decision-relevant: the flagship rack-scale system has gone from a $149K DGX-1 (2017) to a ~$3M GB200 NVL72 (2024–25), to ~$6–6.5M for the GB300 NVL72 (2025–26), to a reported **$7M–$8.8M for the Vera Rubin VR200 NVL72 (shipping H2 2026)**. That is roughly a 2× jump per ~12–18-month cadence at the rack level.

Crucially, **compute per rack is rising even faster than price.** FP-class throughput per rack has gone up ~100–1,000× over the same span while rack price rose ~2–3×. The buyer pays more per rack but gets disproportionately more compute — the price-per-FLOP keeps falling even as the sticker price climbs.

**Orbital-economics implication:** The hypothesis holds. If an orbital node = 1 rack + a fixed ~$50–55M Neutron launch, then as rack price climbs the launch becomes a smaller share of node cost. At a $3M rack, launch is ~94% of node CapEx; at a $10M rack, ~84%; at a $20M rack, ~73%. Because revenue scales with the rack's compute (which is rising faster than price), and the launch cost is fixed, **payback economics structurally improve over time even with the identical rocket.** A node launched in 2028–2030 with a Rubin-Ultra-class or later rack should pay back materially faster than one launched today.

**Confidence: Medium-high.** The trend direction (rising rack price, rising compute, improving orbital math) is robust and corroborated across multiple sources. The absolute numbers — especially historical list prices and future rack prices — are estimates: NVIDIA has *never* officially confirmed list prices for NVL72/NVL144 rack systems, and pre-2020 data-center GPUs were sold through OEMs without public MSRPs. Treat individual figures as ±20–40%.

---

## Price by generation (flagship data-center accelerator)

| Year | Architecture | Flagship part | Per-GPU price (est.) | Flagship rack/system | System price (est.) | Notes |
|------|-------------|---------------|----------------------|----------------------|---------------------|-------|
| 2014 | Kepler | Tesla K80 (dual-GK210) | ~$7,000 MSRP | (no rack-scale product) | — | K80 = 2 GPUs on one board; **confirmed** $6,999 MSRP |
| 2015 | Maxwell | Tesla M40 | ~$5,000 (est.) | — | — | NVIDIA didn't publish MSRP; OEM-set; **estimate** |
| 2016 | Pascal | Tesla P100 16GB | ~$5,700 (PCIe) | — | — | **Confirmed** $5,699 PCIe MSRP; SXM2 higher |
| 2017 | Volta | Tesla V100 | ~$10,000+ | DGX-1 (8× V100) | $149,000 | **Confirmed** DGX-1 Volta list price |
| 2020 | Ampere | A100 40/80GB | ~$10,000–17,000 | DGX A100 (8× A100) | ~$199,000 | A100 40GB ~$10K (CNBC); 80GB ~$15–17K |
| 2022–23 | Hopper | H100 SXM | ~$27,000–40,000 | DGX H100 (8× H100) | ~$400,000–480,000 | Street price; OEM HGX boards similar |
| 2024–25 | Blackwell | B200 / GB200 superchip | B200 ~$30–40K; GB200 ~$60–70K | GB200 NVL72 (72 GPU) | ~$3.0–3.4M | NVL72 = 36 GB200 superchips |
| 2025–26 | Blackwell Ultra | GB300 / B300 | ~$70K+ (est.) | GB300 NVL72 (72 GPU) | ~$6.0–6.5M | ~2× the GB200 NVL72 rack price |
| H2 2026 | Rubin | Rubin R200 / VR200 | not separately priced | Vera Rubin VR200 NVL72 (72 Rubin GPUs) | ~$7.0–8.8M (reported) | NVIDIA increasingly sells full racks only; the $7–8.8M figure is the NVL72 rack (Tom's Hardware), **not** the larger NVL144 |
| 2027 | Rubin Ultra | — | — | Rubin Ultra NVL576-class | ~$15–25M+ (projection) | 4-chiplet packages; ~600kW racks |

**Reading the table:** Per-GPU flagship price rose ~5–11× over a decade (P100 → GB200). Per-rack flagship system price rose from $149K (DGX-1) → ~$3M (GB200 NVL72) → ~$6M (GB300 NVL72) → ~$8M (Rubin VR200 NVL72) — i.e. **roughly doubling every generation since rack-scale systems became the unit of sale, compared like-for-like at the 72-GPU NVL72 rack.**

---

## 1. Historical flagship GPU/system pricing

- **Kepler era (2014):** The Tesla K80 launched 17 Nov 2014 at a *confirmed* $6,999 MSRP — one of the few publicly listed data-center GPU prices of the era. The K80 packed two GK210 GPUs on a board.
- **Maxwell (2015):** Tesla M40. NVIDIA explicitly declined to publish MSRPs for Maxwell Teslas, leaving pricing to OEMs/resellers. Street pricing was roughly $4,000–6,000. **This is an estimate** — no official list price exists.
- **Pascal P100 (2016):** *Confirmed* $5,699 MSRP for the PCIe 16GB card (launched 20 Jun 2016). The SXM2 module sold higher (typically $8,000–9,000 through OEMs).
- **Volta V100 (2017):** Per-GPU pricing climbed past $10,000. The flagship *system*, the DGX-1 with 8× V100, launched at a *confirmed* $149,000. A cut-down DGX Station (4× V100) launched at $69,000.
- **Ampere A100 (2020):** A100 40GB widely cited at ~$10,000 (CNBC, Feb 2023); the 80GB SXM variant ran ~$15,000–17,000. The DGX A100 (8× A100) carried a suggested price near $199,000.
- **Hopper H100 (2022–23):** Per-GPU street pricing of $27,000–40,000 (it spiked higher during the 2023–24 shortage). The DGX H100 (8× H100) listed at roughly $400,000–480,000.
- **Blackwell GB200 (2024–25):** Jensen Huang publicly floated a $30,000–40,000 figure for a "Blackwell GPU" (B200), later clarifying NVIDIA sells systems not bare chips. The **GB200 superchip** (1 Grace CPU + 2 B200 GPUs) is widely reported at $60,000–70,000. The **GB200 NVL72 rack** (36 superchips = 72 GPUs) is reported at **~$3.0–3.4M**.
- **GB300 NVL72 (2025–26):** Reported at **~$6.0–6.5M per rack** — roughly double the GB200 NVL72. Liquid-cooling hardware alone is ~$50,000 per rack.

**Caveat — historical list prices are murky.** Only K80, P100 PCIe, and the DGX systems have firm public MSRPs. Everything at the GPU level for Maxwell, and all NVL72/NVL144 rack prices, are *industry estimates / leaks*; NVIDIA has never confirmed rack-system list prices.

---

## 2. Is per-unit price rising? — Yes, unambiguously

**Per-GPU:** ~$5,700 (P100, 2016) → ~$10K (V100, 2017) → ~$10–17K (A100, 2020) → ~$27–40K (H100, 2022) → ~$60–70K (GB200 superchip, 2024). That is a **~5–11× rise over 8 years**, and the rate is accelerating in the Hopper→Blackwell step.

**Per-rack/system (the decision-relevant unit):**
- DGX-1 (2017): $149K
- DGX A100 (2020): ~$199K
- DGX H100 (2022): ~$400–480K
- GB200 NVL72 (2024–25): ~$3.0–3.4M
- GB300 NVL72 (2025–26): ~$6.0–6.5M
- Vera Rubin VR200 NVL72 (H2 2026): ~$7.0–8.8M (reported — this is the NVL72 rack, not the NVL144)

The jump from the DGX 8-GPU box (~$0.4M) to the NVL72 rack (~$3M) partly reflects a *redefinition of the product* — NVIDIA shifted the unit of sale from an 8-GPU server to a 72-GPU NVLink-coupled rack. But even holding the rack as the unit, **GB200 → GB300 → Rubin shows ~2× per generation, on a ~12–18-month cadence.** The price of flagship NVIDIA compute moves in one direction: up.

---

## 3. Compute & value per dollar

Price is rising — but compute is rising faster. Approximate dense tensor throughput per flagship GPU:

| Generation | Tensor throughput (peak, approx.) | Lowest-precision mode |
|-----------|-----------------------------------|-----------------------|
| V100 (2017) | ~125 TFLOPS | FP16 |
| A100 (2020) | ~312 TFLOPS FP16 (624 w/ sparsity) | FP16/BF16 |
| H100 (2022) | ~1,979 TFLOPS FP16; ~3,958 TFLOPS FP8 | FP8 |
| B200 (2024) | ~2.2–2.5× H100 across FP8/FP16; adds FP4/FP6 | FP4 |
| Rubin R200 (2026) | ~50 PFLOPS FP4-class per package | NVFP4 |

At the **rack** level the contrast is starkest. Comparing **like-for-like at
the 72-GPU NVL72 rack** (the $7–8.8M price is the VR200 NVL72, not the NVL144):
- **GB200 NVL72:** ~1,440 PFLOPS (1.44 EFLOPS) FP4 per rack, for ~$3M.
- **Vera Rubin VR200 NVL72:** the NVL144 (144 Rubin GPU dies) is rated up to
  **3.6 NVFP4 ExaFLOPS inference** / 1.2 FP8 ExaFLOPS training; the **VR200
  NVL72** is the 72-GPU half of that platform, so **~1.8 NVFP4 ExaFLOPS-class
  inference per rack**, for ~$7–8.8M.

So VR200 NVL72 vs. GB200 NVL72: rack price up ~2.3–2.9×, FP4 inference compute
up ~1.25× per 72-GPU rack — but the Rubin GPU itself is a far larger step at
the *die* level (~50 PFLOPS FP4-class per package), and the NVL144 doubles the
GPU count again. **Measured strictly rack-for-rack at NVL72, price-per-FLOP is
roughly flat across the GB200→VR200 step; measured per-GPU-die or against the
NVL144 it is clearly falling.** Either way the buyer gets *more compute per
dollar of rack* as the generations advance — the dynamic the hypothesis assumed
holds; only the magnitude depends on whether you compare NVL72-to-NVL72 or
GPU-to-GPU. (Note: the "10× per generation" framing is loose — measured
rack-to-rack at NVL72 it is closer to ~2.5× FP-throughput per ~12–18 months,
which compounds to ~10× over 3 generations / ~3–4 years.)

---

## 4. Projected pricing

- **GB200 NVL72 (today):** ~$3.0–3.4M. **Verified** against multiple sources (Tom's Hardware, TechSpot, tae kim/Bloomberg). The "$3–4M today" assumption in the prior synthesis is confirmed, sitting at the low end.
- **GB300 NVL72 (2025–26):** ~$6.0–6.5M — about 2× GB200.
- **Vera Rubin VR200 NVL72 (H2 2026):** Reported $7.0M–$8.8M per rack (the NVL72 rack — the larger NVL144 is a separate, costlier product). NVIDIA has not confirmed; server-maker margins on these are reportedly thin, implying the price is genuinely NVIDIA-driven, not channel markup.
- **Rubin Ultra (2027):** Targets a doubling of performance by moving from 2-chiplet to 4-chiplet GPU packages, with ~600kW racks (NVL576-class). No price leaks yet; **projection: ~$15–25M+ per rack** if the ~2× per-generation cadence holds.
- **Trend over the next 1–3 generations:** Rack price heads from ~$3M (GB200) toward **$10M+ within ~2 generations and plausibly $15–25M by Rubin Ultra (2027).** The direction is not in doubt; the magnitude is a projection.

---

## 5. Revenue per rack trajectory

Rental/inference revenue per rack is rising too, broadly tracking the compute increase:

- **GB200 NVL72 cloud rental:** roughly $10.50–27 per GPU-hour across providers → ~$756–1,944/hr for a full 72-GPU rack. At ~70% utilization that is **~$4.6M–11.9M/year of gross rental revenue per rack** (wide range; on-demand high, reserved low).
- **H100 (prior generation):** 8-GPU HGX nodes rent for far less per rack-equivalent; H100 GPU-hour pricing has fallen toward $2–3/hr in 2025–26 as supply caught up. A 72-GPU-equivalent of H100 would gross materially less than a GB200 NVL72.
- **Pattern:** Each generation's flagship rack commands a higher rental rate at launch because it offers more compute (and lower precision modes that boost effective inference throughput). Revenue-per-rack rises generation-over-generation, then *decays within a generation* as the part ages and newer silicon arrives. Because the orbital node holds one fixed rack, model its revenue as front-loaded: high in years 1–3, declining thereafter.

**Implication for orbital:** Newer racks generate more revenue per node, while the launch cost stays fixed — so revenue/CapEx ratio improves with each generation launched.

---

## 6. The orbital-economics implication (with arithmetic)

Define an orbital node as **1 flagship rack + 1 fixed Neutron launch (~$50–55M)**. Use $52.5M as the launch midpoint. Ignore (for this slice) integration, bus, and ground costs — they don't change the *direction* of the result.

| Scenario | Rack price | Node CapEx (rack + $52.5M launch) | Launch share of node CapEx | Rack share |
|----------|-----------|-----------------------------------|----------------------------|------------|
| Today (GB200 NVL72) | $3M | $55.5M | **94.6%** | 5.4% |
| GB300-class | $6.5M | $59.0M | **89.0%** | 11.0% |
| Near-future ("$10M rack") | $10M | $62.5M | **84.0%** | 16.0% |
| Rubin Ultra-class ("$20M rack") | $20M | $72.5M | **72.4%** | 27.6% |
| Aggressive ("$30M rack") | $30M | $82.5M | **63.6%** | 36.4% |

**What this does to payback.** Two compounding effects both favor later launches:

1. **The fixed launch is amortized over a more valuable payload.** The same $52.5M rocket lifts a node whose revenue-generating asset is 3–7× more capable. Revenue per node rises with the rack's compute; launch cost does not. So revenue / launch-cost ratio improves every generation.

2. **The launch stops being the thing that breaks the model.** Today, ~95% of node CapEx is a rocket — payback is essentially "can the rack out-earn a $52.5M launch?" By the $20M-rack era, the rack is ~28% of CapEx and launch ~72%; the node looks more like a normal capital asset where the *productive* hardware is a meaningful fraction of spend.

**Worked payback sketch.** Suppose an orbital rack captures a premium-priced inference revenue stream and nets, conservatively, ~$8M/year (after operating losses, derating for space constraints, and a discount to terrestrial rates):
- *Today, GB200 node ($55.5M CapEx):* payback ≈ 6.9 years.
- *$10M-rack node ($62.5M CapEx)* — but the newer rack has ~2.5× the compute, so even at a discounted ~$16M/yr net: payback ≈ 3.9 years.
- *$20M-rack node ($72.5M CapEx)* with ~$30M/yr net (compute up ~6×): payback ≈ 2.4 years.

The mechanism: **node CapEx grows sub-linearly with rack capability (because the launch is fixed), while node revenue grows roughly linearly with rack compute. The ratio of revenue to CapEx therefore improves with every generation launched.** The orbital model gets *more* attractive over time on the identical Neutron rocket — the hypothesis is supported.

**Caveat:** This ignores that bigger racks draw more power (GB200 ~120kW; Rubin Ultra racks targeting ~600kW). For an orbital node, power and thermal rejection scale with the rack and may become the true binding constraint — see Open Questions. The CapEx arithmetic favors later launches; the *power/thermal envelope* may not, and could cap how much rack the node can actually carry.

---

## Sources

- [Microway — Tesla K80 / Kepler pricing](https://www.microway.com/knowledge-center-articles/in-depth-comparison-of-nvidia-tesla-kepler-gpu-accelerators/)
- [VideoCardz — NVIDIA Tesla K80 ($6,999 MSRP, Nov 2014)](https://videocardz.net/nvidia-tesla-k80)
- [The Next Platform — Nvidia Brings Maxwell GPUs to Tesla Coprocessors (M40, no public MSRP)](https://www.nextplatform.com/2015/11/10/nvidia-brings-maxwell-gpus-to-tesla-coprocessors/)
- [WCCFtech — Tesla P100 PCIe announced ($5,699 16GB MSRP)](https://wccftech.com/nvidia-tesla-p100-pci-express/)
- [Microway — Tesla P100 Price Analysis](https://www.microway.com/hpc-tech-tips/nvidia-tesla-p100-price-analysis/)
- [TweakTown — Volta DGX-1 at $149,000](https://www.tweaktown.com/news/57487/nvidias-new-volta-powered-dgx-1-costs-149-000/index.html)
- [WCCFtech — Volta V100 / DGX-1 pricing up to $149K](https://wccftech.com/nvidia-volta-tesla-v100-dgx-1-hgx-1-supercomputers/)
- [Microway — Tesla V100 Price Analysis](https://www.microway.com/hpc-tech-tips/nvidia-tesla-v100-price-analysis/)
- [NVIDIA Newsroom — DGX A100 launch (5 PFLOPS, ~$199K)](https://nvidianews.nvidia.com/news/nvidia-ships-worlds-most-advanced-ai-system-nvidia-dgx-a100-to-fight-covid-19-third-generation-dgx-packs-record-5-petaflops-of-ai-performance)
- [CNBC — Nvidia's A100 is the $10,000 chip powering the AI race](https://www.cnbc.com/2023/02/23/nvidias-a100-is-the-10000-chip-powering-the-race-for-ai-.html)
- [IntuitionLabs — NVIDIA AI GPU Pricing Guide (H100 $27K–40K)](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide)
- [Wikipedia — Nvidia DGX (DGX H100 list price)](https://en.wikipedia.org/wiki/Nvidia_DGX)
- [Tom's Hardware — Jensen Huang says Blackwell GPU to cost $30K–40K](https://www.tomshardware.com/pc-components/gpus/nvidias-jensen-huang-says-blackwell-gpu-to-cost-dollar30000-dollar40000-later-clarifies-that-pricing-will-vary-as-they-wont-sell-just-the-chip)
- [Tom's Hardware — Blackwell superchips up to $70K, racks up to $3M+](https://www.tomshardware.com/pc-components/gpus/nvidias-next-gen-blackwell-ai-gpus-to-cost-up-to-dollar70000-fully-equipped-servers-range-up-to-dollar3000000-report)
- [TweakTown — GB200 superchip up to $70K; B200 NVL72 server ~$3M](https://www.tweaktown.com/news/98292/nvidias-new-gb200-superchip-costs-up-to-70-000-full-b200-nvl72-ai-server-3-million/index.html)
- [TechSpot — Blackwell server cabinets ~$2–3M each](https://www.techspot.com/news/103994-nvidia-blackwell-server-cabinets-could-cost-somewhere-around.html)
- [Spheron — GB200 NVL72 guide (specs, ~$2.8–3.4M pricing)](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/)
- [tae kim (X) — GB200 NVL72 ~$3M/rack; "price moves in one direction"](https://x.com/firstadopter/status/1940792115124228482)
- [Tom's Hardware — Vera Rubin NVL72 racks up to $8.8M apiece](https://www.tomshardware.com/tech-industry/artificial-intelligence/price-of-nvidias-vera-rubin-nvl72-racks-skyrockets-to-as-much-as-usd8-8-million-apiece-but-server-makers-margins-will-be-tight-nvidia-is-moving-closer-to-shipping-entire-full-scale-systems)
- [Tom's Hardware — Vera Rubin platform in depth](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date)
- [Awesome Agents — Vera Rubin NVL144 specs (3.6 NVFP4 EFLOPS)](https://awesomeagents.ai/hardware/nvidia-vera-rubin-nvl144/)
- [Introl — NVIDIA Vera Rubin: 600kW racks by 2027](https://introl.com/blog/nvidia-vera-rubin-gpu-600kw-racks-2027)
- [Spheron — NVIDIA B300 (Blackwell Ultra) guide (GB300 NVL72 ~$6–6.5M)](https://www.spheron.network/blog/nvidia-b300-blackwell-ultra-guide/)
- [Exxact — Blackwell vs Hopper tensor throughput comparison](https://www.exxactcorp.com/blog/hpc/comparing-nvidia-tensor-core-gpus)
- [E2E Networks — A100 vs H100 vs H200 FLOPS comparison](https://www.e2enetworks.com/blog/nvidia-a100-vs-h100-vs-h200-gpu-comparison)
- [Hyperstack — GB200 NVL72 on-demand rental pricing](https://www.hyperstack.cloud/nvidia-blackwell-gb200)
- [getdeploying — GB200 cloud pricing across providers](https://getdeploying.com/gpus/nvidia-gb200)

---

## Open questions

1. **NVL72/NVL144 rack list prices are unconfirmed.** NVIDIA has never published them; all rack figures are leaks/analyst estimates. The GB200 (~$3M) and GB300 (~$6M) numbers are well-corroborated; the Rubin $7–8.8M range comes mostly from a single Tom's Hardware report and should be re-verified post-launch.
2. **Power/thermal scaling may cap the orbital node.** Rack power is climbing fast (GB200 ~120kW → Rubin Ultra racks targeting ~600kW). An orbital node must reject all that heat radiatively. The CapEx math favors carrying a bigger, pricier rack — but the power/thermal envelope of the spacecraft bus may make that physically infeasible, regardless of cost. This is the most important unresolved tension.
3. **Will NVIDIA keep the ~2×-per-generation rack-price cadence?** Pricing power depends on competition (AMD MI-series, custom ASICs, hyperscaler silicon) and on whether the AI capex cycle persists. A pricing plateau would weaken — but not reverse — the orbital thesis.
4. **Revenue-per-rack decay rate within a generation.** Rental rates fall as silicon ages (H100 GPU-hour pricing roughly halved in ~2 years). The orbital payback model needs a realistic in-generation revenue decay curve, not a flat rate.
5. **Does the orbital node get refreshed?** This analysis assumes one fixed rack per launched node. If racks can't be serviced on orbit, each node is locked to its launch-era hardware and is eventually outclassed — which argues for *later* launches with better racks, reinforcing the conclusion but also implying nodes have a finite competitive life.
6. **Launch cost is treated as fixed at $50–55M.** If Neutron reuse drives launch cost down over time, the rack share of node CapEx rises even faster and the thesis strengthens further — worth modeling as a sensitivity.
