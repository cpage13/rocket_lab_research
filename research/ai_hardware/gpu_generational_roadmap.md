# NVIDIA Datacenter GPU Generational Roadmap & Physical Specs, 2022–2036

**Research date:** 2026-05-19
**Purpose:** Ground the project's valuation calculator in per-GPU economics. The calculator currently treats "a rack" as a frozen **72 GPUs**, with a fixed kW-per-GPU. This document supplies the real generation-by-generation trajectory of (1) GPUs per rack, (2) how a "GPU" is defined, (3) kW per GPU, and (4) per-GPU performance — from Hopper (2022–23) through the announced and credibly-projected NVIDIA roadmap to ~2036.

**Companion docs:** `ai_hardware/ai_hardware.md` (what an AI rack physically is), `node_design/rack_splitting.md` (why "a rack" is a rack), `../valuation/ai_compute_trajectory.md` (prior trajectory research), `llm_compute/inference_scaling.md` (inference workload characteristics).

**Reading guide — claim tags.** Every load-bearing number is tagged:
**[FACT]** = NVIDIA-disclosed or multiply-reported confirmed figure; **[ESTIMATE]** = third-party analyst/press estimate for an unconfirmed number; **[DERIVED]** = our arithmetic from tagged inputs; **[PROJECTION]** = our directional forecast, explicitly speculative. As-of dates noted where specs are still moving. Where sources disagree, both numbers are shown.

> **Source status (2026-05-25):** See [SOURCE_INDEX.md](../SOURCE_INDEX.md) claim IDs GPU-001 through GPU-012. GB200/GB300 configurations are source-certified. Vera Rubin rack power remains an estimate. Rubin Ultra 600 kW and Feynman 1 MW are roadmap/keynote targets, not shipping product specifications.

---

## 1. Summary — the two answers the calculator needs

**Is "72 GPUs per rack" fixed? — No, but it held flat for three generations and then steps up.**

In **"as a customer buys it" (package / SXM module) terms**, the rack-scale GPU count was a **flat 72** across Blackwell (GB200, 2024), Blackwell Ultra (GB300, 2025), and Vera Rubin (VR200 NVL72, H2 2026) — three generations, same Oberon rack, same 72 modules. It then **doubles to 144 packages** with Rubin Ultra (Kyber NVL576, H2 2027) and stays at **~144–576 packages** for Feynman (2028, Oberon-576 or Kyber-1,152). So the calculator's "72" is correct for *2024–2026* and then **wrong from 2027** — it must step to 144 (Rubin Ultra) and beyond.

In **GPU-die terms** the count diverges earlier: NVIDIA's marketing counts dies, and a Rubin package has 2 dies, a Rubin Ultra package 4. So Rubin = 144 dies (marketed once as "NVL144"), Rubin Ultra = 576 dies ("NVL576"). **Crucially, NVIDIA reverted the naming**: just before CES 2026 it dropped "NVL144" and went back to **"VR NVL72"** — counting the 72 *packages* as 72 GPUs, because the die-count nomenclature was "too confusing." So the *official customer-facing* unit is the package. This document uses **package = "a GPU as sold"** throughout, and tracks dies as a secondary column. (`node_design/rack_splitting.md`'s "the 72-count is a commercial convention" is correct — and the convention is now confirmed to be *packages*, not dies.)

**Is kW-per-GPU fixed? — No. The bare-package TDP roughly doubles every ~2 generations; the rack-apportioned all-in figure rises from ~1.8 kW (2024) toward ~4–5 kW (2028) and keeps climbing.** Total rack power is the steepest curve in the whole hardware story: ~10 kW (Hopper 8-GPU node) → ~132 kW (GB200) → ~140 kW (GB300) → ~150–220 kW (Rubin, contested) → ~600 kW (Rubin Ultra, roadmap target) → ~1 MW (Feynman roadmap target).

### 1.1 Key-spec table

Per-GPU performance index is **NVFP4 dense per package**, indexed to **B200 = 1.0** (the GB200's GPU). "GPUs/rack as-sold" = packages/SXM modules. "kW/GPU all-in" = total rack power ÷ packages.

| Generation (rack SKU) | Year | GPUs/rack **as-sold** (packages) | GPUs/rack **dies** | Rack power (kW) | kW/GPU **package TDP** | kW/GPU **all-in** | Per-GPU perf index (NVFP4 dense, B200=1) | Tag (power / perf) |
|---|---|---|---|---|---|---|---|---|
| HGX/DGX H100 (8-GPU node) | 2022–23 | 8 | 8 | ~10.2 | ~0.7 | ~1.28 | ~0.05 (FP8-era; no native FP4) | [FACT] / [FACT] |
| GB200 NVL72 (Blackwell) | 2024 | 72 | 72 | ~120 nom / **~132** load | ~1.0–1.2 | **~1.6–1.8** | **1.0** (9 PF dense FP4) | [FACT] / [FACT] |
| GB300 NVL72 (Blackwell Ultra) | 2025 | 72 | 72 | ~135 TDP / **~140** typ / ~155 peak | ~1.4 | **~1.9–2.2** | ~1.7 (15 PF dense FP4) | [FACT] / [FACT] |
| VR200 NVL72 (Vera Rubin) | H2 2026 | **72** | 144 | **~150–220** (contested; see §4) | ~1.8 (Max-Q) / ~2.3 (Max-P) | **~2.1–3.1** | ~3.7–5.5 (~33–35 PF dense / 50 PF sparse per pkg) | [ESTIMATE] / [FACT-ish] |
| Rubin Ultra NVL576 ("Kyber") | H2 2027 | **144** | 576 | **~600** | **~3.6** | **~4.2** | ~11 (~100 PF FP4 per pkg, 4-die) | [ROADMAP TARGET] / [FACT] |
| Feynman (NVL-class) | 2028 | **~144–576** (Oberon-576 / Kyber-1,152 die-config dependent) | up to 1,152 | **~1,000** (1 MW target) | **~2** per die-class GPU | **~3–7** (config-dependent) | ~18–28 | [ROADMAP TARGET] / [PROJECTION] |
| Feynman Ultra / post-Feynman | ~2029–30 | ~144–288+ | larger | **~1.0–1.5 MW** | rising | ~5–9 | ~35–60 | [PROJECTION] |
| (unnamed) | ~2033 | — | — | **~1.5–2.5 MW** | rising | ~8–14 | ~120–250 | [PROJECTION] |
| (unnamed) | ~2036 | — | — | **~2–4 MW** | rising | ~12–22 | ~400–1,000 | [PROJECTION] |

**How to read the "kW/GPU all-in" column** — this is the number the calculator should use for power-driven node mass. It is **total rack power ÷ GPU packages**. It is meaningfully *higher* than the bare package TDP because it apportions to each GPU its share of the NVLink switches, the Grace/Vera CPUs, the NICs/DPUs, PSU losses, and in-rack cooling/fans. For GB200 it is ~1.6–1.8 kW vs a ~1.0–1.2 kW package; for Rubin Ultra it is ~4.2 kW vs a ~3.6 kW package. The all-in figure is what actually has to be powered and have its heat rejected.

**The trajectory in one line:** the calculator's frozen "72 GPUs at a fixed kW" is a fair snapshot of **2024–2026** only. From **2027** the package count steps to 144, and the all-in kW/GPU has been climbing the whole time (~1.7 → ~4.2 kW, 2024→2027) and continues up. A trajectory-aware calculator should drive node power off **rack kW** (the cleanest, best-sourced curve), and treat "GPUs per rack" as a step function: 72 through 2026, 144 from 2027, with Feynman+ uncertain.

**Confidence: High** for 2022–2026 configurations where NVIDIA/OEM sources publish rack product details. **Medium** for the single contested item — **Vera Rubin VR200 rack power**, where sources split between ~120–130 kW and ~180–220 kW (§4). **Roadmap-level** for Rubin Ultra 600 kW and Feynman 1 MW: they are useful planning targets, not shipping rack specifications. **Speculative** for everything past ~2029.

---

## 2. Generation-by-generation: SKU, release year, rack-scale product

| Gen | Architecture | Rack-scale SKU | GPU (package) | Release | Status (as of May 2026) |
|---|---|---|---|---|---|
| Hopper | Hopper | **HGX H100 / DGX H100** (8-GPU baseboard; no NVL72-class rack) | H100 SXM5 | 2022–23 | Mature; superseded |
| Blackwell | Blackwell | **GB200 NVL72** | B200 (dual-die) | 2024 H2 | Shipping in volume; the 2024–25 workhorse |
| Blackwell Ultra | Blackwell | **GB300 NVL72** | B300 (dual-die) | 2025 | Shipping/ramping — Microsoft Azure brought up a 4,608-GPU GB300 cluster late 2025 |
| Rubin | Vera Rubin | **VR200 NVL72** (briefly "NVL144") | R200 / VR200 (dual-die) | H2 2026 | Announced GTC 2025, detailed CES 2026; production hardware to partners H2 2026 — **not yet shipping** |
| Rubin Ultra | Vera Rubin | **NVL576 "Kyber"** (a.k.a. Kyber NVL144 by package count) | VR300 / Rubin Ultra (quad-die) | H2 2027 | Announced; ~2 years out — specs partly firm |
| Feynman | Feynman | NVL-class on Oberon or Kyber chassis | Feynman (3D-stacked) | 2028 | Roadmap only — paired with "Rosa" CPU |
| post-Feynman | — | — | — | ~2029–2036 | Pure projection |

**Key naming facts:**

- **The Hopper generation never had an NVL72-class rack.** Its rack-scale unit was the **8-GPU HGX H100 baseboard** (the DGX H100 is that baseboard in a chassis). There was a later **GH200 NVL32** (32 Grace-Hopper superchips, NVLink-switched) but the *mainstream* Hopper deployment unit was the 8-GPU node. This is the origin of the "8 GPUs" row — the rack-as-the-unit era starts with Blackwell. [FACT — [HPCwire Hopper launch](https://www.hpcwire.com/2022/03/22/nvidia-launches-hopper-h100-gpu-new-dgxs-and-grace-megachips/)]
- **NVIDIA changed, then un-changed, how it counts a GPU.** At GTC 2025 NVIDIA announced the Rubin rack as **"NVL144"**, counting **GPU dies** (72 packages × 2 dies). In **late December 2025, just before CES 2026, it reverted to "VR NVL72"** — counting the **72 packages** as 72 GPUs — because, per Jensen Huang, the die-count naming "was too confusing" ([The Register, CES 2026](https://www.theregister.com/2026/01/05/ces_rubin_nvidia/); [SemiAnalysis Vera Rubin](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution)). **Net: the official customer-facing GPU = the package/SXM module.** Some older sources (and the project's own `ai_hardware.md`, written May 17 before this was fully settled) still show "NVL144 = 144 GPUs"; that 144 is the *die* count, not the package count. Rubin Ultra is still styled "NVL576" (576 dies) but is also describable as **Kyber NVL144** (144 packages). The die/package divergence is now permanent — the calculator should pick **package** as its unit and be explicit about it.

---

## 3. GPUs per rack — and the definition of "a GPU"

This is the central question for the calculator. The answer has two layers.

### 3.1 What counts as "a GPU"?

A modern NVIDIA datacenter GPU is a **multi-die package** (a.k.a. SXM module / "superchip" component). The number of compute dies per package has been rising:

| Generation | Dies per package | What NVIDIA calls "1 GPU" | Notes |
|---|---|---|---|
| H100 | 1 (monolithic) | the die = the package | Simple — one die, one GPU. [FACT] |
| B200 / B300 (Blackwell) | 2 | the **2-die package** = 1 GPU | Blackwell's twin dies act as one logical GPU; counted as 1. [FACT — [Spheron B200](https://www.spheron.network/blog/nvidia-b200-complete-guide/)] |
| R200 (Rubin) | 2 | the **2-die package** = 1 GPU (after the NVL144→NVL72 reversion) | NVIDIA briefly counted the 2 dies as 2 GPUs ("NVL144"), then reverted. [FACT — [The Register](https://www.theregister.com/2026/01/05/ces_rubin_nvidia/)] |
| VR300 (Rubin Ultra) | **4** | "NVL576" counts the **dies**; by package it is 144 | Each Rubin Ultra package = 4 reticle-sized dies. [FACT — [Tom's Hardware Vera Rubin in-depth](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date)] |
| Feynman | 3D-stacked (die count not locked) | TBD | Feynman introduces 3D die-stacking; per-package die count unconfirmed. [PROJECTION] |

**The definitional resolution for the calculator:** use the **package** ("a GPU as a customer buys and racks it") as the unit, because (a) that is what NVIDIA officially reverted to, (b) it is what gets a socket, an NVLink port, and a price, and (c) it avoids the die-count whiplash. Track dies only as a performance-scaling note. A "Rubin GPU" = one 2-die package; a "Rubin Ultra GPU" = one 4-die package.

### 3.2 GPUs per rack — the trajectory

| Generation | Year | GPUs/rack **as-sold (packages)** | GPUs/rack **(dies)** | Rack family | Source |
|---|---|---|---|---|---|
| HGX H100 | 2022–23 | **8** (per baseboard/node — not a 72-class rack) | 8 | HGX 8-GPU baseboard | [FACT] [HPCwire](https://www.hpcwire.com/2022/03/22/nvidia-launches-hopper-h100-gpu-new-dgxs-and-grace-megachips/) |
| GB200 NVL72 | 2024 | **72** | 72 | Oberon | [FACT] [NVIDIA GB200 NVL72](https://www.nvidia.com/en-us/data-center/gb200-nvl72/) |
| GB300 NVL72 | 2025 | **72** | 72 | Oberon | [FACT] [NVIDIA GB300 NVL72](https://www.nvidia.com/en-us/data-center/gb300-nvl72/) |
| VR200 NVL72 | H2 2026 | **72** | 144 | Oberon (same family) | [FACT] [The Register CES 2026](https://www.theregister.com/2026/01/05/ces_rubin_nvidia/); [ServeTheHome](https://www.servethehome.com/nvidia-launches-next-generation-rubin-ai-compute-platform-at-ces-2026/) |
| Rubin Ultra NVL576 ("Kyber") | H2 2027 | **144** | 576 | Kyber (new, vertical blades) | [FACT] [Tom's Hardware in-depth](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date); [Tom's Hardware Kyber](https://www.tomshardware.com/pc-components/gpus/nvidia-shows-off-rubin-ultra-with-600-000-watt-kyber-racks-and-infrastructure-coming-in-2027) |
| Feynman | 2028 | **up to 576** on Oberon, **up to 1,152** on Kyber (package counts) | up to 1,152+ (×die-per-pkg) | Oberon or Kyber | [FACT — roadmap] [Tom's Hardware roadmap](https://www.tomshardware.com/pc-components/gpus/nvidia-updates-data-center-roadmap-with-rosa-cpu-and-stacked-feynman-gpus-optical-nvlink-groq-lpus-with-nvfp4-and-nvlink-also-on-deck) |
| post-Feynman | ~2030+ | rising | rising | — | [PROJECTION] |

**The headline finding for the calculator:**

> **Packages per rack was a flat 72 for three generations (GB200 2024, GB300 2025, VR200 2026), then doubles to 144 with Rubin Ultra (2027).** The calculator's frozen "72" is correct through 2026 and **wrong from 2027 onward.**

Two important nuances:

1. **The flat 72 (2024–2026) is real and deliberate.** NVIDIA kept Vera Rubin on the **same Oberon rack** as GB200/GB300 specifically for infrastructure compatibility — same 72 sockets, same physical cabinet family. So for the three generations the calculator most plausibly models *today*, 72 packages per rack is genuinely fixed. The *die* count doubled (72→144) at Rubin because dies-per-package went 1→2, but a customer still racks 72 modules.
2. **Rubin Ultra's jump is a chassis change, not just a count change.** The Kyber rack is a clean-sheet design — compute blades rotated 90° to vertical, four pods of 18 blades, 144 packages. So "144 per rack" at 2027 comes with a *new rack*, new cooling, and 4 dies/package. Feynman then scales further: NVIDIA's roadmap explicitly lists Feynman as **"up to 576 GPU packages on Oberon chassis or up to 1,152 GPU packages on Kyber chassis"** ([Tom's Hardware roadmap](https://www.tomshardware.com/pc-components/gpus/nvidia-updates-data-center-roadmap-with-rosa-cpu-and-stacked-feynman-gpus-optical-nvlink-groq-lpus-with-nvfp4-and-nvlink-also-on-deck)).

**Implication for the orbital project specifically:** `rack_splitting.md` argues an orbital inference node need not be a full intact rack — the binding floor is ~16–36 GPUs of HBM to hold a frontier model. That argument is *strengthened* by this finding: once "a rack" stops being a fixed 72 and becomes a 144-package, 600 kW, clean-sheet Kyber object (2027) or a 1 MW Feynman object (2028), the gap between "what NVIDIA sells as a rack" and "what a mass-constrained satellite can fly" widens fast. The calculator's "rack" abstraction degrades exactly as the project's own roadmap predicts.

---

## 4. kW per GPU — bare package TDP vs rack-apportioned all-in

Two distinct numbers, both needed, clearly separated below.

- **(a) Bare package TDP** — the chip/package power rating in isolation.
- **(b) Rack-apportioned all-in** — **total rack power ÷ GPU packages**. Includes each GPU's share of NVLink switches, Grace/Vera CPUs, NICs/DPUs, PSU conversion losses, and in-rack fans/cooling. This is the number that actually drives "how much power must be generated and how much heat rejected per GPU."

### 4.1 The table

| Generation | Year | GPUs/rack (pkg) | **Rack power (kW)** | **(a) Package TDP (kW)** | **(b) All-in kW/GPU = rack ÷ pkg** | Tag |
|---|---|---|---|---|---|---|
| HGX/DGX H100 | 2022–23 | 8 | **~10.2** | ~0.7 (700 W SXM5) | **~1.28** | [FACT] |
| GB200 NVL72 | 2024 | 72 | **~120 nominal / ~132 under load** | ~1.0–1.2 | **~1.67–1.83** (132÷72) | [FACT] |
| GB300 NVL72 | 2025 | 72 | **~135 TDP / ~140 typical / ~155 peak** | ~1.4 | **~1.94–2.15** (140–155÷72) | [FACT] |
| VR200 NVL72 (Rubin) | H2 2026 | 72 | **~150–220 — CONTESTED** | ~1.8 (Max-Q) / ~2.3 (Max-P) | **~2.1–3.1** (150–220÷72) | [ESTIMATE] |
| Rubin Ultra NVL576 ("Kyber") | H2 2027 | 144 | **~600** | **~3.6** (3,600 W/package) | **~4.17** (600÷144) | [ROADMAP TARGET] |
| Feynman | 2028 | ~576 (Oberon) / ~1,152 (Kyber) | **~1,000 (1 MW target)** | **~2** per die-class GPU | **~3.5–7** (config-dependent) | [FACT target] / [PROJECTION] |
| Feynman Ultra / post-Feynman | ~2029–30 | rising | **~1.0–1.5 MW** | rising | ~5–9 | [PROJECTION] |
| (unnamed) | ~2033 | — | **~1.5–2.5 MW** | rising | ~8–14 | [PROJECTION] |
| (unnamed) | ~2036 | — | **~2–4 MW** | rising | ~12–22 | [PROJECTION] |

### 4.2 The contested item — Vera Rubin VR200 rack power

This is the **single biggest uncertainty** in the near-term roadmap, and sources genuinely split:

- **Low camp (~120–130 kW):** [ServeTheHome's CES 2026 coverage](https://www.servethehome.com/nvidia-launches-next-generation-rubin-ai-compute-platform-at-ces-2026/) and several trade outlets say the standard VR200 NVL72 is "approximately 120–130 kW per rack, similar to current deployments" — emphasizing the Oberon-compatibility story (same rack, same power envelope as GB300).
- **High camp (~180–220 kW):** [SemiAnalysis's Vera Rubin deep-dive](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution) computes from the per-GPU power profiles: 72 packages × up to 2,300 W (Max-P) ≈ 165 kW just for GPUs, and with CPUs/switches/NICs a total rack TDP of **~180–220 kW**. [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-reportedly-boosts-vera-rubin-performance-to-ward-hyperscalers-off-amd-instinct-ai-accelerators-increased-boost-clocks-and-memory-bandwidth-pushes-power-demand-by-500-watts-to-2300-watts) reports NVIDIA *raised* the per-GPU rating to 2.3 kW (from an originally announced 1.8 kW) to boost performance — which pushes the rack figure up.
- **Reconciliation.** The two camps are partly talking past each other: **Max-Q** (1,800 W/GPU, efficiency-optimized) and **Max-P** (2,300 W/GPU, performance-optimized) are *software-managed power profiles of the same hardware*, per SemiAnalysis. At Max-Q the rack is ~150–170 kW; at Max-P it is ~190–220 kW. NVIDIA has **not officially published the VR200 rack power** (both [The Register](https://www.theregister.com/2026/01/05/ces_rubin_nvidia/) and [Tom's Hardware in-depth](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date) explicitly note NVIDIA declined to give a wattage at CES 2026).
- **Recommended planning numbers:** treat VR200 as **~150–170 kW (Max-Q) to ~190–220 kW (Max-P)**, i.e. an all-in kW/GPU of **~2.1–3.1**. The project's `ai_hardware.md` uses "~190 kW"; that sits in the Max-P band and is a defensible engineering-margin figure. **Flag: revisit when NVIDIA or an OEM (Supermicro/HPE/Lenovo) publishes a VR200 datasheet — likely mid-2026.** This is a version-dependent number.

### 4.3 Reading the kW/GPU trajectory

- **Bare package TDP roughly doubles every ~2 generations:** H100 0.7 kW → B200 ~1.0–1.2 kW → B300 ~1.4 kW → R200 ~1.8–2.3 kW → Rubin Ultra **3.6 kW** → Feynman ~2 kW *per die-class GPU* (Feynman's per-GPU number drops because it splits across more, smaller stacked dies — but there are far more of them per rack).
- **All-in kW/GPU rose ~2.5× from 2024 to 2027:** ~1.7 kW (GB200) → ~2.0 kW (GB300) → ~2.1–3.1 kW (Rubin) → **~4.2 kW (Rubin Ultra)**.
- **Total rack power is the steepest curve and the one that hurts orbit most.** It is also the clearest roadmap signal — the **600 kW Rubin Ultra** figure and the **1 MW Feynman** target are reported NVIDIA roadmap/keynote targets, not shipping product specifications ([DCD](https://www.datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027/); [Computer Weekly](https://www.computerweekly.com/news/366639658/Huge-grid-and-heat-challenges-ahead-as-Nvidia-set-for-1MW-rack)). Rack power: ~10 kW (2023 Hopper node) → ~132 kW (2024) → ~140 kW (2025) → ~150–220 kW (2026) → **~600 kW target (2027)** → **~1,000 kW target (2028)**. That is roughly a **100× rise in rack power over 5 years** if the roadmap lands, of which ~5× is in the 2026→2028 window alone.
- **Why all-in > package TDP, and by how much.** The ratio (all-in ÷ package TDP) is ~1.5–1.7× for GB200, ~1.4–1.5× for GB300, ~1.2–1.4× for Rubin, and ~1.16× for Rubin Ultra. It is *shrinking* — as the GPU package itself gets more power-hungry, the fixed overhead (CPUs, switches, PSU losses) becomes a smaller fraction. For a trajectory model, an **all-in ≈ 1.2–1.5× package TDP** rule of thumb is reasonable, trending toward the low end over time.

**Recommendation for the calculator:** do not model per-GPU power as a fixed constant. The cleanest, best-sourced driver is **total rack power** (the §4.1 column), which the project's own `ai_compute_trajectory.md` §2 already tracks and which directly drives orbital solar + radiator mass. If the calculator needs a per-GPU figure, use the **all-in kW/GPU** column (rack ÷ packages), not the bare TDP — and let it rise on the trajectory shown, not sit frozen.

---

## 5. Per-GPU performance

Inference-relevant per-GPU throughput. **All FLOPS are vendor-quoted peak.** Two precision caveats run through this whole section: (1) NVIDIA quotes **sparse** (a.k.a. "with sparsity" / NVFP4 marketed) numbers that are roughly **2× the dense** number — both are given where known; (2) the precision floor keeps dropping (FP16 → FP8 → FP4 → NVFP4 with microscaling), so a chunk of the headline gain is *lower-precision arithmetic*, not raw transistor throughput. Sustained inference throughput is materially lower than peak — typically ~30–50% — so **do not use peak FLOPS for capacity planning** (see `ai_compute_trajectory.md` §3).

### 5.1 Per-GPU (package) spec table

| Generation | GPU (package) | **FP4 dense (PF)** | **FP4 sparse/NVFP4 (PF)** | **FP8 dense (PF)** | HBM capacity | HBM bandwidth | NVLink/GPU | Perf index (dense FP4, B200=1) |
|---|---|---|---|---|---|---|---|---|
| Hopper | H100 SXM5 | — (no native FP4) | — | ~2.0 (3.96 PF sparse) | 80 GB HBM3 | ~3.35 TB/s | 0.9 TB/s (NVLink 4) | ~0.05 (FP8-basis proxy) |
| Blackwell | B200 | **9** | 18 | ~4.5 (9 sparse) | 192 GB HBM3e | ~8 TB/s | 1.8 TB/s (NVLink 5) | **1.0** |
| Blackwell Ultra | B300 | **15** | 30 | ~7.5 (15 sparse) | 288 GB HBM3e | ~8 TB/s | 1.8 TB/s (NVLink 5) | ~1.67 |
| Rubin | R200 (2-die pkg) | **~33–35** | **~50** (NVFP4 marketed) | ~16 | 288 GB HBM4 | **~20–22 TB/s** (initial ~20, target 22) | 3.6 TB/s (NVLink 6) | **~3.7–3.9** |
| Rubin Ultra | VR300 (4-die pkg) | ~50–55 | **~100** (NVFP4 marketed) | ~25 | **1,024 GB (1 TB) HBM4E** | **~32 TB/s** | NVLink 7 | **~5.5–11** (see note) |
| Rubin CPX | Rubin CPX (monolithic) | ~15 | **~30** (NVFP4) | — | 128 GB **GDDR7** | (GDDR7 — much lower) | (limited) | ~1.7 (prefill-specialized) |
| Feynman | Feynman (3D-stacked) | rising | rising | rising | "custom HBM" (HBM4E+) | rising | NVLink 8 (optical) | ~18–28 [PROJECTION] |

**Sourcing the key numbers:**
- **B200:** 9 PF dense FP4 / 18 PF sparse, 192 GB HBM3e, 8 TB/s, ~1,000 W. [FACT — [Spheron B200 guide](https://www.spheron.network/blog/nvidia-b200-complete-guide/), [primeline B200 datasheet](https://www.primeline-solutions.com/media/categories/server/nach-gpu/nvidia-hgx-h200/nvidia-blackwell-b200-datasheet.pdf)]
- **B300:** 15 PF dense FP4 (67% more than B200's 9), 288 GB HBM3e (12-high stacks), 8 TB/s, 1,400 W. [FACT — [Tom's Hardware B300](https://www.tomshardware.com/pc-components/gpus/nvidia-announces-blackwell-ultra-b300-1-5x-faster-than-b200-with-288gb-hbm3e-and-15-pflops-dense-fp4), [server-parts.eu B300](https://www.server-parts.eu/post/nvidia-b300-gpu-blackwell-ultra-architecture)]
- **R200 (Rubin):** here the dense/sparse and die/package distinction matters most. NVIDIA markets **"50 PFLOPS NVFP4 inference per package"**; this is the **sparse** figure. SemiAnalysis computes the **dense FP4 at ~33.3 PF per dual-die package** ([SemiAnalysis](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution), [Glenn Lockwood R200](https://www.glennklockwood.com/garden/processors/R200)). 288 GB HBM4, ~20–22 TB/s (NVIDIA target 22; initial shipments ~20 due to HBM4 supplier ramp). [FACT-ish — vendor + analyst]
- **Rubin Ultra (VR300):** **~100 PF FP4 per package** (4 dies), **1 TB HBM4E**, ~32 TB/s. [FACT — [Tom's Hardware in-depth](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date)]
- **Rubin CPX:** the inference-specialized part — monolithic, 128 GB **GDDR7** (not HBM), ~30 PF NVFP4, built only for the compute-bound *prefill* phase. Directly relevant to the project; covered in `ai_hardware.md` §2.4. [FACT — [NVIDIA Rubin CPX newsroom](https://nvidianews.nvidia.com/news/nvidia-unveils-rubin-cpx-a-new-class-of-gpu-designed-for-massive-context-inference)]

### 5.2 The per-generation per-GPU performance multiplier

Indexed to **B200 = 1.0**, dense FP4 per package:

| Step | Per-package dense FP4 | Multiplier vs prior | Notes |
|---|---|---|---|
| H100 → B200 | (FP8→FP4 transition) | — | Not directly comparable — H100 has no native FP4. On an FP8 basis B200 is ~2× a dense H100; the FP4 jump adds another ~2× from precision. |
| B200 → B300 | 9 → 15 PF | **~1.67×** | Pure architectural + clock gain, same package, same precision. |
| B300 → R200 | 15 → ~33–35 PF | **~2.2–2.3×** | SM count 160→224, Tensor Core width doubled, clock +25% (1.90→2.38 GHz). |
| R200 → Rubin Ultra | ~33–35 → ~50–55 PF (per package) | **~1.5–1.6×** per package | But the package now has **4 dies vs 2** — *per die* the gain is smaller; the per-package gain comes substantially from doubling die count. |
| Rubin Ultra → Feynman | projection | **~1.6–2.5×** | 3D die-stacking + custom HBM. [PROJECTION] |

**Reading the per-GPU performance trajectory:**

- **Per-package dense FP4 performance is rising ~1.5–2.3× per generation** — call it **~1.8–2× per generation** as a planning rate. Compounded, that is **~6–10× over three generations** (~3–4 years).
- **A large share of the gain after Rubin Ultra is "more dies per package," not faster dies.** Rubin Ultra's ~100 PF/package is ~2× Rubin's ~50 PF — but Rubin Ultra has 4 dies vs Rubin's 2. *Per die*, the generational gain is more modest. This matters: if the calculator counts performance per *package*, the multiplier looks bigger than the underlying silicon improvement, because the package is absorbing more dies.
- **Memory capacity and bandwidth — the inference-relevant axes — rise faster than they used to.** HBM/GPU: 80 GB (H100) → 192 GB (B200) → 288 GB (B300, R200) → **1,024 GB (Rubin Ultra)**. HBM bandwidth/GPU: ~3.35 TB/s → ~8 TB/s → ~20–22 TB/s → ~32 TB/s. Since inference (especially decode) is **memory-bandwidth-bound** (`inference_scaling.md` §3), the bandwidth curve is arguably the most decision-relevant per-GPU performance axis for an *inference* venture — and it is climbing ~2–2.7× per generation.
- **The honest caveat for revenue modeling.** Per `ai_compute_trajectory.md` §7, per-GPU/per-rack *performance* exploding ~10×/3-generations does **not** translate into ~10× revenue — revenue tracks the rack's *price* (~2×/generation), and the surplus FLOPS accrue to the *buyer* as cheaper intelligence. So this performance trajectory should drive **capacity / tokens-served modeling**, not be wired directly into a revenue multiplier. The performance index is an input to "how much inference can a node do," not "how much does a node earn."

---

## 6. Synthesis — projected 2026→2036 per-generation trajectory

Pulling §3 (GPUs/rack), §4 (kW), and §5 (performance) into one forward trajectory. **The line between announced fact and projection is explicit below.**

### 6.1 Announced / credibly-firm (2026–2028)

| Year | Generation | GPUs/rack (pkg) | GPUs/rack (dies) | Rack kW | All-in kW/GPU | Per-GPU dense FP4 (PF) | Confidence |
|---|---|---|---|---|---|---|---|
| H2 2026 | VR200 NVL72 (Rubin) | 72 | 144 | ~150–220 (contested) | ~2.1–3.1 | ~33–35 | **High** on counts/perf; **Medium** on rack kW |
| H2 2027 | NVL576 "Kyber" (Rubin Ultra) | 144 | 576 | **~600** | ~4.2 | ~50–55/pkg | **High** — 600 kW & 144-pkg confirmed; perf firm |
| 2028 | Feynman (NVL-class) | ~576 (Oberon) / ~1,152 (Kyber) | up to 1,152+ | **~1,000** (1 MW target) | ~3.5–7 | rising (~60–90 est.) | **Medium** — 1 MW target & ~2 kW/GPU confirmed; die config & counts not locked |

**What is genuinely confirmed here:** Rubin's 72-package / 144-die config and ~33–35 PF dense FP4; Rubin Ultra's 144-package / 576-die config, 600 kW rack, 3,600 W/package, ~100 PF/package, 1 TB HBM4E; Feynman's 2028 timing, 1 MW rack target, ~2 kW/GPU, 3D stacking, NVLink-8 with co-packaged optics, and the Oberon-576 / Kyber-1,152 package-count ceilings. **What is not:** the exact VR200 rack power (±~40%), and Feynman's per-package die count and per-rack FLOPS.

### 6.2 Projected (2029–2036) — explicitly speculative

| Year | "Generation" | GPUs/rack (pkg) | Rack kW | All-in kW/GPU | Per-GPU perf index (dense FP4, B200=1) | Basis |
|---|---|---|---|---|---|---|
| ~2029–30 | Feynman Ultra / post-Feynman | ~144–288+ | **~1.0–1.5 MW** | ~5–9 | ~35–60 | Cadence extrapolation; NVIDIA has hinted at a ~2030 Feynman successor |
| ~2033 | (unnamed) | — | **~1.5–2.5 MW** | ~8–14 | ~120–250 | Trend extrapolation of ~2×/gen perf, ~1.3–1.5×/gen power |
| ~2036 | (unnamed) | — | **~2–4 MW** | ~12–22 | ~400–1,000 | Trend extrapolation — treat as ±50–100% |

**Projection logic and honesty about confidence:**

- **Past ~2028 this is genuinely speculative.** NVIDIA's public roadmap currently extends only to Feynman (2028). A "Feynman Ultra" around 2030 is hinted but unspecified. Everything in the 2029–2036 block is **cadence extrapolation** — applying the observed ~2-year tick-tock, ~1.8–2× per-generation performance, and ~1.3–1.5× per-generation rack-power growth. The *direction* (counts up, power up, performance up) is robust; the *magnitudes* a decade out should be treated as **±50–100%**.
- **The package-count trajectory is the least predictable variable.** It was flat at 72 for three generations, then NVIDIA doubled it (Kyber, 144) and signaled a path to 576–1,152 (Feynman). Whether it keeps climbing or re-stabilizes depends on chassis economics, cooling limits, and how NVIDIA chooses to package — not a smooth curve. The calculator should model GPUs-per-rack as a **step function with named breakpoints** (72 → 144 → uncertain), *not* a continuous growth rate.
- **Rack power is the most reliable forward variable** because NVIDIA itself publishes it as a roadmap target and the physics (more dies, more HBM, higher clocks) only points up. "Rack as a megawatt" by 2028 is NVIDIA's own framing; ~1.5–2.5 MW by the early 2030s is a directional extrapolation, not a wild one. This is consistent with `ai_compute_trajectory.md` §2.
- **The crossover the project cares about:** `ai_compute_trajectory.md` §2.2 reconciles a Neutron flyability ceiling of ~200–470 kW depending on hot-loop and block-upgrade assumptions. Against this trajectory: GB200/GB300 (~132–155 kW) fly comfortably; VR200 (~150–220 kW) flies, at the upper end needing a hot-loop; **Rubin Ultra (~600 kW) and Feynman (~1 MW) exceed even the block-upgraded + hot-loop ceiling** — a full intact rack of those generations is not flyable on Neutron without power-capping or on-orbit assembly. This is the "flyability wall," and the trajectory says it lands at the **Rubin-Ultra generation (2027)**.

### 6.3 What the calculator should change

1. **GPUs per rack: replace the frozen 72 with a step function.** 72 for 2024–2026 (GB200/GB300/VR200), **144 from 2027** (Rubin Ultra Kyber), uncertain (144–576) for Feynman+. Be explicit that the unit is the **package**, not the die.
2. **Per-GPU power: replace the fixed kW with the all-in kW/GPU trajectory** (§4.1) — or, better, drive node power off **total rack kW** directly, since that is the best-sourced curve and what orbital solar/radiator mass actually scales with.
3. **Per-GPU performance: track it for capacity (tokens served), not revenue.** Use the ~1.8–2×/generation dense-FP4 multiplier and the HBM-bandwidth curve to model inference throughput — but keep revenue on the ~2×/generation price-tracking slope per `ai_compute_trajectory.md` §7. Performance and revenue diverge; do not couple them.
4. **Carry the contested VR200 power as a flagged range** (~150–220 kW) and revisit when an OEM datasheet lands.

---

## Sources

**NVIDIA official / OEM:**
- [NVIDIA GB200 NVL72 product page](https://www.nvidia.com/en-us/data-center/gb200-nvl72/)
- [NVIDIA GB300 NVL72 product page](https://www.nvidia.com/en-us/data-center/gb300-nvl72/)
- [NVIDIA H100 product page](https://www.nvidia.com/en-us/data-center/h100/)
- [NVIDIA Newsroom — Rubin CPX announcement](https://nvidianews.nvidia.com/news/nvidia-unveils-rubin-cpx-a-new-class-of-gpu-designed-for-massive-context-inference)
- [NVIDIA Technical Blog — Inside the Vera Rubin Platform: six chips, one supercomputer](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/)
- [NVIDIA Blackwell B200 datasheet (PDF)](https://www.primeline-solutions.com/media/categories/server/nach-gpu/nvidia-hgx-h200/nvidia-blackwell-b200-datasheet.pdf)
- [NVIDIA H100 Tensor Core GPU datasheet (PDF)](https://www.aspsys.com/wp-content/uploads/2023/09/nvidia-h100-datasheet.pdf)

**Rubin (VR200) — CES 2026 / specs:**
- [The Register — NVIDIA unpacks Vera Rubin rack at CES 2026](https://www.theregister.com/2026/01/05/ces_rubin_nvidia/)
- [ServeTheHome — NVIDIA launches Rubin AI compute platform at CES 2026](https://www.servethehome.com/nvidia-launches-next-generation-rubin-ai-compute-platform-at-ces-2026/)
- [Tom's Hardware — Vera Rubin platform in depth](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date)
- [Tom's Hardware — NVIDIA boosts Vera Rubin to ~2,300 W/GPU](https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-reportedly-boosts-vera-rubin-performance-to-ward-hyperscalers-off-amd-instinct-ai-accelerators-increased-boost-clocks-and-memory-bandwidth-pushes-power-demand-by-500-watts-to-2300-watts)
- [SemiAnalysis — Vera Rubin: Extreme Co-Design](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution)
- [SemiAnalysis — GTC 2025: Built For Reasoning, Vera Rubin, Kyber, Jensen Math, Feynman](https://newsletter.semianalysis.com/p/nvidia-gtc-2025-built-for-reasoning-vera-rubin-kyber-cpo-dynamo-inference-jensen-math-feynman)
- [Glenn Lockwood — NVIDIA Rubin R200 notes](https://www.glennklockwood.com/garden/processors/R200)
- [The Register — NVIDIA's new GPU definition (die vs package)](https://www.theregister.com/2025/04/01/nvidia_ai_enterprise_cost/)
- [DCD — NVIDIA announces Vera Rubin Superchip for late 2026](https://www.datacenterdynamics.com/en/news/nvidia-announces-vera-rubin-superchip-for-late-2026/)
- [NextPlatform — NVIDIA's Vera-Rubin platform obsoletes current AI iron](https://www.nextplatform.com/ai/2026/01/06/nvidias-vera-rubin-platform-obsoletes-current-ai-iron-six-months-ahead-of-launch/4092179)

**Rubin Ultra / Kyber:**
- [DCD — Rubin Ultra NVL576 rack expected to be 600kW, H2 2027](https://www.datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027/)
- [Tom's Hardware — Rubin Ultra with 600,000-Watt Kyber racks](https://www.tomshardware.com/pc-components/gpus/nvidia-shows-off-rubin-ultra-with-600-000-watt-kyber-racks-and-infrastructure-coming-in-2027)
- [Introl — NVIDIA Vera Rubin: 600kW racks by 2027](https://introl.com/blog/nvidia-vera-rubin-gpu-600kw-racks-2027)
- [TweakTown — Kyber rack-scale, up to 576 Rubin Ultra GPUs in 2027](https://www.tweaktown.com/news/108238/nvidia-teases-next-gen-kyber-rack-scale-tech-up-to-576-nvidia-rubin-ultra-gpus-in-2027/index.html)

**Feynman / roadmap to 2028+:**
- [Tom's Hardware — NVIDIA enterprise roadmap: Rubin, Rubin Ultra, Feynman, silicon photonics](https://www.tomshardware.com/tech-industry/semiconductors/nvidia-enterprise-roadmap-rubin-rubin-ultra-feynman-and-silicon-photonics)
- [Tom's Hardware — NVIDIA roadmap with Rosa CPU and stacked Feynman GPUs, optical NVLink](https://www.tomshardware.com/pc-components/gpus/nvidia-updates-data-center-roadmap-with-rosa-cpu-and-stacked-feynman-gpus-optical-nvlink-groq-lpus-with-nvfp4-and-nvlink-also-on-deck)
- [Computer Weekly — grid and heat challenges as NVIDIA set for 1MW rack](https://www.computerweekly.com/news/366639658/Huge-grid-and-heat-challenges-ahead-as-Nvidia-set-for-1MW-rack)
- [TweakTown — NVIDIA roadmap, Feynman in 2028](https://www.tweaktown.com/news/110521/nvidia-updates-roadmap-with-new-details-on-its-next-gen-gpu-feynman-coming-in-2028/index.html)
- [NextPlatform — NVIDIA draws GPU system roadmap out to 2028](https://www.nextplatform.com/2025/03/19/nvidia-draws-gpu-system-roadmap-out-to-2028/)
- [Wikipedia — Feynman (microarchitecture)](https://en.wikipedia.org/wiki/Feynman_(microarchitecture))

**Hopper (H100) generation:**
- [HPCwire — NVIDIA launches Hopper H100 GPU, DGXs, Grace superchips](https://www.hpcwire.com/2022/03/22/nvidia-launches-hopper-h100-gpu-new-dgxs-and-grace-megachips/)
- [Continuum Labs — NVIDIA DGX H100 system](https://training.continuumlabs.ai/infrastructure/servers-and-chips/nvidia-dgx-h-100-system)
- [Jarvis Labs — FLOPS performance of the NVIDIA H100](https://jarvislabs.ai/ai-faqs/what-is-the-flops-performance-of-the-nvidia-h100-gpu)

**Blackwell / Blackwell Ultra (B200 / B300):**
- [Spheron — NVIDIA B200 complete guide](https://www.spheron.network/blog/nvidia-b200-complete-guide/)
- [Tom's Hardware — NVIDIA announces Blackwell Ultra B300, 15 PFLOPS dense FP4](https://www.tomshardware.com/pc-components/gpus/nvidia-announces-blackwell-ultra-b300-1-5x-faster-than-b200-with-288gb-hbm3e-and-15-pflops-dense-fp4)
- [server-parts.eu — NVIDIA B300 Blackwell Ultra architecture](https://www.server-parts.eu/post/nvidia-b300-gpu-blackwell-ultra-architecture)
- [Spheron — NVIDIA B300 (Blackwell Ultra) guide](https://www.spheron.network/blog/nvidia-b300-blackwell-ultra-guide/)

**Power / rack-level validation:**
- [TweakTown — GB200 NVL72, 132 kW TDP](https://www.tweaktown.com/news/100839/nvidias-new-gb200-nvl72-ai-server-highest-power-consuming-in-history-with-132kw-tdp/index.html)
- [Sunbird DCIM — Is your data center ready for the GB200 NVL72](https://www.sunbirddcim.com/blog/your-data-center-ready-nvidia-gb200-nvl72)
- [Sunbird DCIM — How much power does the GB300 NVL72 need](https://www.sunbirddcim.com/blog/how-much-power-does-nvidia-gb300-nvl72-need)
- [Introl — NVIDIA Blackwell Ultra B300 infrastructure requirements](https://introl.com/blog/nvidia-blackwell-ultra-b300-infrastructure-requirements-2025)

*Project-internal companions: `ai_hardware/ai_hardware.md`, `node_design/rack_splitting.md`, `../valuation/ai_compute_trajectory.md`, `llm_compute/inference_scaling.md`.*

---

## Open questions / uncertainties

1. **Vera Rubin VR200 rack power is unresolved (~120–130 kW vs ~180–220 kW).** NVIDIA declined to publish it at CES 2026. The split is partly a Max-Q (~150–170 kW) vs Max-P (~190–220 kW) artifact, but the spread is real and ±~40%. **This is the single biggest near-term uncertainty.** Revisit when an OEM (Supermicro/HPE/Lenovo) datasheet lands — likely mid-2026.

2. **Feynman (2028) per-package die count and per-rack FLOPS are not locked.** Confirmed: 1 MW rack target, ~2 kW/GPU, 3D die-stacking, NVLink-8 with co-packaged optics, Oberon-576 / Kyber-1,152 package ceilings. Not confirmed: how many stacked dies per package, the resulting per-rack FLOPS, or which chassis becomes the volume product. The §6.1 Feynman FLOPS figure is an estimate.

3. **The die-vs-package counting could shift again.** NVIDIA flip-flopped once (NVL144 → NVL72). Rubin Ultra is styled "NVL576" (dies) but is "Kyber NVL144" by package. If NVIDIA's marketing convention changes again, the "GPUs per rack" number changes without any hardware change. The calculator should pin the unit explicitly (recommendation: **package**) and not inherit NVIDIA's marketing count uncritically.

4. **FLOPS are vendor peak, with sparsity.** NVIDIA's NVFP4 marketed numbers are ~2× the dense figure. Sustained inference throughput is ~30–50% of peak and workload-dependent. The performance index here is a *relative* generational tracker, not an absolute capacity number — a sustained-throughput model (InferenceMAX-style) is needed for real tokens-served sizing. Flagged the same way in `ai_compute_trajectory.md` §3 and `inference_scaling.md` OQ #3.

5. **Per-die vs per-package performance gain.** From Rubin Ultra onward, much of the per-package FLOPS growth is "more dies per package" (2→4), not faster dies. A calculator that scales performance per *package* will overstate the underlying silicon improvement. If per-GPU economics matter, decide whether the unit is the package or the die and be consistent.

6. **Post-2028 is cadence extrapolation, not roadmap.** NVIDIA's public roadmap ends at Feynman (2028). The 2029–2036 rows are ±50–100%. The *direction* is robust (counts, power, performance all up); the magnitudes are not. A "Feynman Ultra" ~2030 is hinted but unspecified.

7. **All-in kW/GPU ratio drift.** The (all-in ÷ package TDP) ratio is shrinking (~1.6× for GB200 → ~1.16× for Rubin Ultra) as the GPU package itself dominates rack power. The ~1.2–1.5× rule of thumb in §4.3 is a current-era approximation; for far-future generations the overhead fraction is genuinely unknown.

8. **Rubin CPX and GDDR7-class inference silicon are a wildcard for an inference venture.** This document tracks the *mainstream HBM GPU* roadmap. NVIDIA's inference-specialized, GDDR7-based Rubin CPX has a different power/performance/cost profile. If the orbital project deploys CPX-style silicon (per `ai_hardware.md` §2.4), a separate per-chip trajectory is needed — the HBM-GPU numbers here do not apply to it.
