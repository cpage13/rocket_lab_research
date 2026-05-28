# AI Compute Trajectory — How Hardware & Economics Evolve Over the Valuation Horizon

*Research date: 2026-05-17. Prepared for the Rocket Lab orbital AI-inference data center feasibility project. Briefed by [trajectory_notes.md](trajectory_notes.md); companion to [rack_cost_trajectory.md](../economics/rack_cost_trajectory.md), [revenue_per_watt.md](../economics/revenue_per_watt.md), [energy_operating_costs.md](../economics/energy_operating_costs.md), [hyperscaler_margins.md](../economics/hyperscaler_margins.md), and [ai_hardware.md](../ai_hardware/ai_hardware.md).*

> **Purpose.** The valuation calculator is **static on per-rack economics** — it models a fleet of frozen 2026-class racks. For a 10–15-year valuation that is a real gap. This document supplies the missing piece: sourced, directional **trajectories** for how AI compute hardware and economics move over time, so a trajectory layer can be built into the calculator. It does **not** modify the calculator, `LIBRARY.md`, or `RESEARCH_TRACKER.md`.

> **Method (the founder's explicit ask).** Each trajectory **first maps the actual last ~3–5 years with real data**, *then* projects ~10 years out. The historical block is hard data. The projected block is **directional and explicitly labelled subjective** — nobody can forecast a decade of semiconductor economics precisely; the value is the *direction*, the *reasoning*, and an honest tailwind/headwind read, not false precision.

> **Reading guide.** Claims are tagged **[FACT]** (company-disclosed / reported 2021–2026 data), **[ESTIMATE]** (third-party estimate, leak, or analyst figure for an unconfirmed number), **[DERIVED]** (our arithmetic), or **[PROJECTION]** (our directional forecast — speculative, the explicitly subjective part). Hard numbers are cited inline. In every table, rows at or before 2026 are historical/near-term; rows after 2026 are **[PROJECTION]** unless noted.

---

## Summary

**Nine trajectories, one through-line: AI compute hardware is moving fast, and it moves the *unit cost down* far faster than it moves the *unit revenue up*.**

- **Rack cost is rising ~2× per ~12–18-month generation** — $149K DGX-1 (2017) → ~$3M GB200 NVL72 (2024) → ~$6–6.5M GB300 (2025–26) → ~$5–8.8M Rubin VR200 NVL72 (H2 2026) → a projected ~$15–25M Rubin Ultra NVL576 (2027). The prior project finding (~2×/generation) is **verified**. [FACT / PROJECTION]
- **Rack power is the steepest curve and the one that hurts orbit:** ~3.5 kW DGX-1 → ~120–132 kW GB200 → ~135–155 kW GB300 → ~190–230 kW Rubin VR200 → **~600 kW Rubin Ultra NVL576** (confirmed NVIDIA roadmap, H2 2027). That is ~5× over three generations. [FACT]
- **Rack performance rises even faster than price** — ~2.5× FP-throughput per generation, compounding to ~10×/3 generations. The buyer gets more compute per dollar of rack every cycle; price-per-FLOP **falls** even as the sticker climbs. [FACT / DERIVED]
- **Rack mass grows slowly** — ~60 kg DGX-1 → ~1,360 kg GB200/GB300 → ~1,400–2,000 kg Rubin. The terrestrial rack itself is *not* the orbital mass problem. **Power is** — radiator + solar mass scale linearly with kW, and kW is exploding. The project's hypothesis (mass grows slow, power grows fast) is **confirmed**.
- **The cost of intelligence is collapsing ~10×/year** — GPT-3-level output fell from ~$60/M tokens (2021) to ~$0.06/M (2024), a **1,000× drop in 3 years** (a16z, Epoch AI). Frontier-tier pricing fell ~50× in 3 years but **reversed upward in 2026** as reasoning models got genuinely costlier to run.
- **GPU rental rates fell then partly recovered** — H100 ~$8/GPU-hr (early 2024) → ~$1.65–2.40 (late 2025) → back to ~$2.35 (2026) as demand outran supply. A ~70% peak-to-trough collapse, then a bounce. [FACT]
- **The decisive finding for the venture — per-rack gross revenue does NOT track FLOPS.** A frontier rack's compute rose ~10×/3 generations; its gross rental revenue rose only ~2–3× over the same span and is *competition-set*, not capability-set. Revenue tracks roughly the *sticker price* of the rack, not its FLOPS. The exploding FLOPS are **consumer surplus** — they make compute cheaper for the buyer, not the rack owner richer.
- **Value-capture is bifurcated and stable:** NVIDIA holds ~75% gross margin generation after generation (scarcity + CUDA moat); integrated hyperscalers hold 35–49% operating margin (software + scale moat); the **bare GPU-rental / neocloud layer was competed down to ~0% operating margin**. The orbital venture, as an *infrastructure owner*, escapes the renter's markup — but owning an asset does not by itself confer pricing power. It earns a durable premium **only** if the orbital niche is genuinely scarce.
- **Terrestrial energy cost is on a clear rising trajectory** — industrial/PPA rates roughly flat-to-modestly-up for contracted hyperscale buyers today, but wholesale +75% YoY in PJM and analysts projecting industrial rates +up-to-40% by 2030. This **widens orbit's free-solar edge over time** — though it remains a second-order effect against launch cost.

**The net read for the orbital venture.** The trajectory hands the venture **two genuine tailwinds** — (1) a fixed launch cost shrinking as a share of an ever-pricier rack, and (2) a rising terrestrial energy bill widening orbit's structural advantage — and **two genuine headwinds** — (1) rack power exploding ~5× over the horizon, which drives node mass up and tightens the flyability ceiling (likely forcing racks/launch 2→1 at Rubin-Ultra-class power), and (2) the hard fact that **per-rack revenue does not scale with FLOPS** — so "the rack got 10× more powerful" does *not* mean "the node earns 10× more." The venture's economics improve over time on the *cost* side and are flat-to-eroding on the *commodity-revenue* side; the entire upside lives in the **premium**, which the trajectory neither creates nor destroys.

**Confidence: Moderate.** High on the historical blocks (2017–2026 hardware specs, token prices, rental rates, NVIDIA margins are all well-sourced and cross-checked). Moderate on the near-term projections (Rubin/Rubin Ultra). Low-to-moderate on the 10-year projections — they are deliberately directional. The single softest input is the **per-rack revenue trajectory**: NVIDIA has never confirmed rack list prices, full-rack rental quotes are thin, and the "$/rack-year" figure swings ±2–3× on pricing tier and utilization.

---

## 1. Rack Cost — Flagship AI Rack/System Price per Generation

The decision-relevant unit is the **rack-scale system**, which NVIDIA made the unit of sale around 2024 ("the rack is the new server"). Per-GPU price is shown alongside for continuity with the older single-GPU era.

### 1.1 Historical → projected (the flagship NVIDIA rack/system)

| Year | Architecture | Flagship system | Per-GPU price (est.) | System / rack price | Tag | Gen-over-gen |
|---|---|---|---|---|---|---|
| 2017 | Volta | DGX-1 (8× V100) | ~$10,000 | **$149,000** | [FACT] confirmed list | — |
| 2020 | Ampere | DGX A100 (8× A100) | ~$10,000–17,000 | **~$199,000** | [FACT] confirmed suggested | ~1.3× |
| 2022–23 | Hopper | DGX H100 (8× H100) | ~$27,000–40,000 | **~$400,000–480,000** | [FACT] reported list | ~2.2× |
| 2024–25 | Blackwell | GB200 NVL72 (72 GPU) | ~$60,000–70,000 (superchip) | **~$3.0–3.4M** | [ESTIMATE] leak/analyst | (unit redefined) |
| 2025–26 | Blackwell Ultra | GB300 NVL72 (72 GPU) | ~$70,000+ | **~$6.0–6.5M** | [ESTIMATE] | ~2.0× vs GB200 |
| H2 2026 | Rubin | VR200 NVL72 (72 Rubin GPU) | not separately priced | **~$5.0–8.8M** (mid ~$7M) | [ESTIMATE] reported | ~1.2–2.3× vs GB200 |
| H2 2027 | Rubin Ultra | NVL576 / Kyber (576 GPU dies) | — | **~$15–25M+** | [PROJECTION] | ~2× vs VR200 |
| ~2028 | Feynman | Feynman NVL-class | — | **~$25–45M** | [PROJECTION] | ~1.5–2× |
| ~2030 | post-Feynman | (unnamed) | — | **~$40–70M** | [PROJECTION] | ~1.5×/gen |
| ~2033 | — | (unnamed) | — | **~$70–120M** | [PROJECTION] | trend extrapolation |
| ~2036 | — | (unnamed) | — | **~$100–180M** | [PROJECTION] | trend extrapolation |

**Reading the table.** Per-rack flagship price has risen from $149K (2017) to ~$3M (2024) to a reported ~$5–8.8M (Rubin, 2026) — confirming the project's prior **~2×-per-generation** finding (`rack_cost_trajectory.md`). The GB200→GB300 step is a clean ~2×; the GB200→Rubin VR200 step is softer (~1.2–2.3×) because Rubin's huge die-level gain is partly delivered by *more dies per package* rather than a proportionally higher NVL72 sticker. Two structural caveats on the projection:

- **NVIDIA has never confirmed a single NVL72/NVL144 rack list price.** Every figure from GB200 onward is a leak or analyst estimate. The GB200 (~$3M) and GB300 (~$6M) numbers are well-corroborated; the Rubin range ($5M Investing.com / Kuo vs. $8.8M Tom's Hardware) is genuinely wide and includes ~$1M of bundled 3D-NAND storage in the lower quote.
- **The 10-year extrapolation assumes the AI-capex supercycle and NVIDIA's pricing power both persist.** A pricing plateau (from AMD, custom ASICs, hyperscaler silicon, or a capex slowdown) would flatten the curve. The *direction* — up — is robust; the **magnitude is the subjective part**. We bracket the projection at ~1.5×/generation (conservative) to ~2×/generation (trend), giving a 2036 flagship rack of **~$100–180M** — squarely in the founder's "extreme thought experiment" territory, reached not by assumption but by extending the observed cadence.

### 1.2 Why this matters for orbit

A fixed launch cost (~$10–20M Rocket Lab internal marginal, per retired root `CONCLUSION.md` Rev 4 and now source-ledgered through `RLDC-LAUNCH-COST-2036` / `NTR-009`) becomes a **shrinking share of node CapEx** as the rack gets pricier. At a $7M Rubin rack, launch is ~50–65% of a rack+launch node; at a projected $30M+ rack it is ~30–40%; at a $100M+ rack it is ~15–20%. **This is the venture's single clearest cost-side tailwind** (see §10). The countervailing force is power (§2).

---

## 2. Rack Power — kW per Rack per Generation

This is the steepest trajectory in the document and the one that most directly threatens the orbital architecture: solar-array and radiator mass scale **linearly with rack power**, so this curve *is* the node-mass curve.

### 2.1 Historical → projected

| Year | Flagship system | Rack/system power | Power per GPU | Tag | Source basis |
|---|---|---|---|---|---|
| 2017 | DGX-1 (8× V100) | **~3.5 kW** | ~0.3 kW (V100 300W SXM) | [FACT] | NVIDIA DGX-1 datasheet (3,500 W) |
| 2020 | DGX A100 (8× A100) | **~6.5 kW** | ~0.4 kW (A100 400W SXM) | [FACT] | NVIDIA DGX A100 datasheet (6,500 W) |
| 2022–23 | DGX H100 (8× H100) | **~10.2 kW** | ~0.7 kW (H100 700W SXM) | [FACT] | NVIDIA DGX H100 datasheet (~10.2 kW) |
| 2024–25 | GB200 NVL72 | **~120–132 kW** | ~1.0–1.2 kW (B200) | [FACT] | HPE QuickSpecs ~132 kW; `ai_hardware.md` |
| 2025–26 | GB300 NVL72 | **~135–155 kW** | ~1.4 kW (B300) | [FACT] | Supermicro/HPE/Lenovo; ~135 kW TDP |
| H2 2026 | Rubin VR200 NVL72 | **~190–230 kW** | ~1.8–2.3 kW (R200) | [ESTIMATE] | Kuo: Max-Q ~190 kW, Max-P ~230 kW |
| H2 2027 | Rubin Ultra NVL576 (Kyber) | **~600 kW** | ~1.0 kW × 576 dies | [FACT] | NVIDIA roadmap; DCD/Introl confirm 600 kW |
| ~2028 | Feynman NVL-class | **~700–900 kW** | rising | [PROJECTION] | trend; NVIDIA "Kyber" successor rack |
| ~2030 | post-Feynman | **~1.0–1.5 MW** | rising | [PROJECTION] | rack-as-megawatt extrapolation |
| ~2033 | — | **~1.5–2.5 MW** | — | [PROJECTION] | trend extrapolation |
| ~2036 | — | **~2–4 MW** | — | [PROJECTION] | trend extrapolation |

**Reading the table.** Rack power rose ~3× per generation through the DGX era (3.5→6.5→10.2 kW), then **jumped an order of magnitude** with the NVL72 rack redefinition (10→130 kW), and continues climbing ~1.3–1.5×/generation in absolute kW. The **600 kW Rubin Ultra figure is a confirmed NVIDIA roadmap number** (not a projection) — DCD and Introl both report the NVL576 Kyber rack at 600 kW for H2 2027. Beyond Rubin Ultra the figures are projected; NVIDIA has publicly discussed "rack as a megawatt" as the trajectory, so a ~1 MW+ rack by ~2030 is a directional extrapolation, not a wild one.

### 2.2 Why this is the headwind

Per the retired `data_science/REPORT.md` historical model summary and [wave5_synthesis.md](../synthesis/wave5_synthesis.md), the reconciled flyability ceiling is **~200–250 kW on a baseline Neutron, ~270–320 kW baseline + hot-loop, ~430–470 kW block-upgraded + hot-loop**. The implications, in trajectory terms:

- GB200/GB300 (~130–155 kW) and Rubin VR200 (~190–230 kW) **fly** — VR200 only with a hot-loop and/or block upgrade.
- **Rubin Ultra (~600 kW) exceeds even the block-upgraded + hot-loop ceiling.** A node carrying a full Rubin Ultra rack is not flyable on Neutron without power-capping (down-clocking / partial population) or multi-launch on-orbit assembly.
- The founder's "racks/launch 2→1" reversal is the direct consequence: as rack power climbs from ~130 kW to ~600 kW, the node mass per rack roughly quadruples, and a block-upgraded Neutron that lifts 2 GB300-class nodes can lift only 1 Rubin-Ultra-class node. **The trajectory forces the reversal — model it.**

The orbital venture is therefore caught between two of its own trajectories: rack cost (§1) makes later, pricier racks *more* attractive per launch dollar, while rack power (§2) makes later racks *un-flyable*. This is the central coupled tension the retired `data_science/REPORT.md` identified; the trajectory data sharpens it but does not resolve it.

---

## 3. Rack FLOPS / Performance per Generation

### 3.1 Historical → projected (per-rack low-precision compute, vendor peak)

| Year | Flagship system | Per-rack compute (lowest-precision, peak) | Per-GPU (peak) | Tag |
|---|---|---|---|---|
| 2017 | DGX-1 (8× V100) | ~1 PFLOPS FP16 | ~125 TFLOPS FP16 (V100) | [FACT] |
| 2020 | DGX A100 (8× A100) | ~2.5 PFLOPS FP16 (5 PF w/ sparsity) | ~312 TFLOPS FP16 (A100) | [FACT] |
| 2022–23 | DGX H100 (8× H100) | ~16 PFLOPS FP8 (32 w/ sparsity) | ~3,958 TFLOPS FP8 (H100) | [FACT] |
| 2024–25 | GB200 NVL72 | **~1,440 PFLOPS (1.44 EF) FP4** | ~20 PFLOPS FP4 (B200) | [FACT] vendor |
| 2025–26 | GB300 NVL72 | **~1,400–1,500 PFLOPS FP4** (~2× attention vs B) | ~15 PF dense / ~30 sparse (B300) | [FACT] vendor |
| H2 2026 | Rubin VR200 NVL72 | **~1,800 PFLOPS (1.8 EF) NVFP4** inference | ~50 PFLOPS NVFP4 (R200 package) | [ESTIMATE] |
| H2 2027 | Rubin Ultra NVL576 | **~15,000 PFLOPS (15 EF) FP4** inference | ~100 PFLOPS FP4 (Rubin Ultra pkg) | [FACT] roadmap |
| ~2028 | Feynman NVL-class | **~25–35 EF FP4-class** | rising | [PROJECTION] |
| ~2030 | post-Feynman | **~60–100 EF** | — | [PROJECTION] |
| ~2036 | — | **~500–1,500 EF** | — | [PROJECTION] |

**Reading the table.** Per-rack peak compute has risen roughly **~2.5× per generation** measured rack-for-rack, compounding to ~10×/3 generations / ~3–4 years. The 1.44 EF → 15 EF jump from GB200 to Rubin Ultra is a confirmed ~10× over ~2.5 years (with most of it from the NVL576 quadrupling the die count, not pure per-die gain). The founder's "~100× over the window" is consistent with the ~2.5×/generation cadence sustained over ~10 years (~6–7 generations → ~100–300×).

**Three caveats that matter for the calculator:**
1. **These are vendor peak FP4/NVFP4 with sparsity ("Jensen math").** Sustained inference throughput is materially lower and workload-dependent — typically ~30–50% of peak. Do not use peak for capacity planning.
2. **The precision floor keeps dropping** (FP16 → FP8 → FP4 → NVFP4 → likely FP4-with-microscaling and below). Much of the headline FLOPS gain is *lower-precision arithmetic*, not raw transistor throughput — real for inference, but it inflates the gen-over-gen multiplier relative to a fixed-precision comparison.
3. **FLOPS is the variable that rises fastest and matters least to revenue** — see §7. This is the crux of the founder↔assistant disagreement: the FLOPS explosion is real, but it accrues to the *buyer* as cheaper intelligence, not to the rack owner as revenue.

---

## 4. Rack Mass — kg per Rack per Generation

### 4.1 Historical → projected (terrestrial fully-populated rack/system mass)

| Year | Flagship system | Rack/system mass | Power | kg per kW | Tag |
|---|---|---|---|---|---|
| 2017 | DGX-1 (8× V100) | **~60 kg** (134 lb, 2U server) | ~3.5 kW | ~17 kg/kW | [FACT] DGX-1 datasheet |
| 2020 | DGX A100 (8× A100) | **~123 kg** (271 lb) | ~6.5 kW | ~19 kg/kW | [FACT] DGX A100 datasheet |
| 2022–23 | DGX H100 (8× H100) | **~130 kg** (287 lb) | ~10.2 kW | ~13 kg/kW | [FACT] DGX H100 datasheet |
| 2024–25 | GB200 NVL72 | **~1,360 kg** (3,000 lb) | ~130 kW | ~10 kg/kW | [FACT] Sunbird/OEM |
| 2025–26 | GB300 NVL72 | **~1,360 kg** (3,000 lb) | ~145 kW | ~9 kg/kW | [FACT] same chassis |
| H2 2026 | Rubin VR200 NVL72 | **~1,400–2,000 kg** (est.) | ~190–230 kW | ~7–10 kg/kW | [ESTIMATE] no official figure |
| H2 2027 | Rubin Ultra NVL576 | **~2,500–4,000 kg** (est.) | ~600 kW | ~5–7 kg/kW | [PROJECTION] |
| ~2030 | post-Feynman | **~4,000–7,000 kg** (est.) | ~1.0–1.5 MW | ~4–5 kg/kW | [PROJECTION] |
| ~2036 | — | **~8,000–15,000 kg** (est.) | ~2–4 MW | ~3–4 kg/kW | [PROJECTION] |

**Reading the table — the project's hypothesis is confirmed.** Rack mass grows **slowly relative to power**. The two are not decoupled (a 600 kW rack genuinely needs more copper, cold-plate, and busbar than a 130 kW one), but the **kg-per-kW ratio is *falling*** — from ~17 kg/kW (DGX-1) to ~9–10 kg/kW (GB200/GB300) and trending lower as racks get power-denser. The terrestrial rack is becoming *more* mass-efficient per watt even as its absolute mass rises.

**The critical orbital implication.** For an orbital node, the terrestrial rack mass (~1.4 t for GB200/GB300) is a *small* part of node mass. The mass that matters is the **solar array + radiator**, both of which scale ~linearly with **power**, not with rack mass. Per `simulations/REPORT.md`, a 150 kW GB300 node masses ~6.8 t total — i.e. the ~1.4 t rack is only ~20% of the node; the balance is power/thermal hardware and bus. So:

> **Rack mass is not the orbital constraint. Rack power is.** A trajectory layer should drive node mass off the **kW curve (§2)**, treating terrestrial rack mass as a slowly-growing minor term. This is exactly the founder's framing in `trajectory_notes.md` — confirmed by the data.

---

## 5. $/Token — The Price of AI Inference ("Cost of Intelligence")

This is the trajectory that most directly tests the founder↔assistant principle: capability and price fall together; the gains are consumer surplus.

### 5.1 Historical — frontier-tier API price (flagship model at launch, $/1M tokens)

| Date | Frontier model | Input $/1M | Output $/1M | Tag |
|---|---|---|---|---|
| Nov 2021 | GPT-3 (davinci) | ~$60 | ~$60–120 | [FACT] |
| Mar 2023 | GPT-4 (8K, at launch) | **$30** | **$60** | [FACT] |
| Nov 2023 | GPT-4 Turbo | $10 | $30 | [FACT] |
| May 2024 | GPT-4o | $5 | $15 | [FACT] |
| 2025 | GPT-5 / GPT-5.x class | ~$1.25–2.50 | ~$10–15 | [FACT] |
| 2026 | GPT-5.5 / Claude Opus 4.7 | **$5** | **$25–30** | [FACT] `revenue_per_watt.md` |

### 5.2 Historical — fixed-capability price (cost to buy a *constant* level of intelligence)

| Capability level | Date first available | Price then ($/1M out) | Cheapest price now | Decline | Tag |
|---|---|---|---|---|---|
| MMLU ≥ 42 (GPT-3 level) | Nov 2021 | ~$60 | ~$0.06 (Llama 3.2 3B, late 2024) | **~1,000× in 3 yr** | [FACT] a16z / Epoch AI |
| MMLU ≥ 83 (GPT-4 level) | Mar 2023 | ~$60 | ~$1 (≈62× cheaper) | **~62× in ~2 yr** | [FACT] a16z |
| GPQA-Diamond ≥ GPT-4 | 2024 | — | — | **~40×/yr** | [FACT] Epoch AI |

**Reading the trajectory.** Two *different* things are happening, and conflating them is the most common error:

- **For a fixed capability**, price collapses at a staggering rate. Epoch AI's regression across six benchmarks finds a **median ~50×/year** decline, accelerating to **~200×/year** for trends measured after January 2024. a16z's headline "**~10×/year**" is the conservative cross-capability read. Either way: **the cost of a fixed unit of intelligence falls roughly an order of magnitude per year.** The "~10×/yr" claim in the brief is **verified — and is, if anything, conservative.**
- **For the frontier**, the story reversed in 2026. After three years of falling (GPT-3 $60 → GPT-4o $5/$15), frontier output pricing **rose** in 2026 — GPT-5.5 at $5/$30, Claude Opus 4.7 at $5/$25 — because reasoning/test-time-compute models are genuinely more expensive to run (more tokens generated per query). OpenAI's o1 was priced at the *same* $60/M output as GPT-3 at launch. Frontier providers are conceding the cheap-commodity tier and holding a premium tier.

### 5.3 Projected $/token

| Year | Fixed-capability (GPT-4 level), $/1M out | Frontier-tier flagship, $/1M out | Tag |
|---|---|---|---|
| 2026 | ~$0.5–1 | ~$25–30 | [FACT] |
| 2028 | ~$0.05–0.2 | ~$20–40 (flat-to-up; reasoning-cost-driven) | [PROJECTION] |
| 2030 | ~$0.01–0.05 | ~$20–50 | [PROJECTION] |
| 2033 | ~$0.002–0.02 | ~$25–60 | [PROJECTION] |
| 2036 | near-zero for commoditised capability | ~$30–80 | [PROJECTION] |

**Projection logic (subjective).** Fixed-capability price keeps falling, but the *rate* decelerates — multiple sources expect ~3–5×/year through ~2028, then ~1.5–2×/year, as the easy gains (quantization, better kernels, MoE sparsity, hardware) are exhausted. Frontier-tier pricing is *not* a smooth curve: it is set by how expensive the newest reasoning paradigm is to run, and 2026 shows it can rise. The directional read: **commodity intelligence trends toward free; frontier intelligence stays expensive-to-priced-for-value.** For the orbital venture this is the key fork from `revenue_per_watt.md` §4 — selling commodity tokens is a race to zero; the venture must sit in the *frontier / differentiated* tier or sell capacity, not tokens.

---

## 6. $/GPU-hr — GPU Rental Rates Over Time

### 6.1 Historical — H100 on-demand rental (the best-tracked series)

| Date | H100 on-demand, neocloud ($/GPU-hr) | Note | Tag |
|---|---|---|---|
| 2023 (shortage peak) | **~$8–12+** | Extreme scarcity; hyperscaler list to ~$12 | [FACT] |
| Early 2024 | ~$2.85–8 | Supply catching up; wide spread | [FACT] Silicon Data |
| Sep 2024 | ~$3.06 (index) | Local high | [FACT] Silicon Data index |
| Jun 2025 | ~$2.36 (index) | −23% YoY | [FACT] Silicon Data index |
| Oct 2025 | **~$1.65–1.70** (1-yr contract low) | Trough | [FACT] |
| Mar 2026 | **~$2.35** (1-yr contract) | +40% off the trough — demand outran supply | [FACT] |
| May 2026 | ~$1.38–11.01 (full provider spread); ~$2–3.70 typical | Neocloud low to hyperscaler high | [FACT] `revenue_per_watt.md` |

### 6.2 Per-generation rental at launch (frontier rack/GPU)

| Generation | On-demand $/GPU-hr at/near launch | Note | Tag |
|---|---|---|---|
| V100 (2017–18) | ~$2–3/GPU-hr | Pre-AI-boom cloud pricing | [ESTIMATE] |
| A100 (2020–21) | ~$1–4/GPU-hr | Rose into the 2023 shortage | [FACT] |
| H100 (2023) | ~$8–12/GPU-hr | Shortage-era peak | [FACT] |
| B200 / GB200 (2024–25) | ~$3.50–7/GPU-hr; spot to ~$2.12 | NVL72 rack ~$756–1,944/hr | [FACT] |
| GB300 (2025–26) | ~$4–8/GPU-hr (inference-optimised) | Premium for HBM capacity | [ESTIMATE] |
| Rubin VR200 (H2 2026) | ~$5–9/GPU-hr (projected at launch) | Frontier premium | [PROJECTION] |

**Reading the trajectory.** Two patterns, both decision-relevant:

1. **Within a generation, rental rates fall hard then can rebound.** H100 fell ~70% peak-to-trough (2023 ~$8–12 → late-2025 ~$1.65), then rebounded ~40% as 2026 demand surprised. The collapse is the commoditization of *aging* silicon; the rebound shows the market is supply-constrained, not demand-saturated. Net: model frontier-rack revenue as **front-loaded — high in years 1–3, decaying as the silicon ages and the next generation ships.**
2. **Across generations, the *frontier* rate at launch is roughly flat-to-modestly-up in $/GPU-hr** (~$3–8/GPU-hr band has held from H100 through Rubin), even though each generation's GPU is several times more capable. This is the single most important observation in the document and the bridge to §7: **the buyer pays a similar hourly rate for a far more capable chip — i.e. they get more compute per rental dollar each generation. The rate is competition-set, not capability-set.**

The brief's "H100 ~$8 → ~$2–3" is **verified** (with the 2026 rebound to ~$2.35 as a real and important wrinkle).

---

## 7. $/Rack-Year (Gross Revenue) — Does Per-Rack Revenue Track FLOPS?

This is the trajectory the founder flagged as the key question. **The answer is no — and the data is fairly clear about it.**

### 7.1 Frontier-rack gross rental revenue per generation

A frontier rack's gross revenue ≈ (GPUs per rack) × ($/GPU-hr) × 8,760 hr × utilization. Using ~85% utilization and blended on-demand-leaning pricing:

| Generation | GPUs/rack | $/GPU-hr (blended) | FP4-class compute/rack | **Gross $/rack-year** | Tag |
|---|---|---|---|---|---|
| DGX H100 (2022–23) | 8 | ~$3–6 | ~16 PFLOPS FP8 | **~$0.2–0.4M** (8-GPU node) | [DERIVED] |
| H100 72-GPU-equiv | 72 | ~$3–6 | ~145 PFLOPS FP8 | **~$1.6–3.2M** | [DERIVED] |
| GB200 NVL72 (2024–25) | 72 | ~$3.50–7 | ~1,440 PFLOPS FP4 | **~$5.6–11.9M** (mid ~$8M) | [FACT/DERIVED] `revenue_per_watt.md` |
| GB300 NVL72 (2025–26) | 72 | ~$4–8 | ~1,400 PFLOPS FP4 | **~$6–13M** (mid ~$9M) | [DERIVED] |
| Rubin VR200 NVL72 (H2 2026) | 72 | ~$5–9 | ~1,800 PFLOPS NVFP4 | **~$7–15M** (mid ~$10M) | [PROJECTION] |
| Rubin Ultra NVL576 (2027) | 576 dies | — | ~15,000 PFLOPS FP4 | **~$20–45M** (scales w/ die count) | [PROJECTION] |

### 7.2 The decisive comparison — revenue vs. FLOPS vs. price

Indexed to GB200 NVL72 = 1.0:

| Generation | Compute index (FP4/rack) | Gross revenue index ($/rack-yr) | Rack price index | Revenue tracks…? |
|---|---|---|---|---|
| H100 72-GPU-equiv | ~0.10 | ~0.30 | ~0.13 | revenue ≈ price, not compute |
| GB200 NVL72 | 1.0 | 1.0 | 1.0 | — |
| GB300 NVL72 | ~1.0 | ~1.1 | ~2.0 | revenue flat; compute flat; price up |
| Rubin VR200 NVL72 | ~1.25 | ~1.25 | ~1.6–2.3 | revenue ≈ compute (NVL72-for-NVL72) ≈ price |
| Rubin Ultra NVL576 | ~10 | ~3–5 | ~5–7 | **revenue badly lags compute** |

**The finding.** Across the GB200→GB300→Rubin span, **per-rack gross revenue rose ~2–3×; per-rack compute rose ~10×.** Revenue tracks **roughly the rack's sticker price** (which also rose ~2–3×) — *not* its FLOPS. The Rubin Ultra row makes it starkest: a ~10× compute jump buys only a ~3–5× revenue jump, because the extra FLOPS are sold at a *falling* $/effective-FLOP.

This confirms the assistant's economic principle in `trajectory_notes.md` and resolves the founder's question:

> **A rack's FLOPS exploding does not make the rack owner richer — it makes compute cheaper for the buyer.** Per-rack revenue is **competition-set, not capability-set**. It rises modestly (roughly with the rack's price, ~2× per generation), while compute rises ~10×/3 generations. The ~8×-and-growing gap between the compute curve and the revenue curve **is the consumer surplus** — it flows to whoever buys the compute, not whoever owns the rack.

### 7.3 Why this is a headwind for the venture — and where the founder's pushback holds

For a valuation calculator, the temptation is to let per-rack revenue ride the FLOPS curve ("Rubin Ultra is 10× GB200, so the node earns 10×"). **The data says don't.** Model per-rack gross revenue as growing ~1.5–2×/generation (tracking price), *not* ~10×/3 generations (tracking FLOPS) — and decaying within each generation as the silicon ages (§6).

**But the founder's pushback is valid and changes the *baseline*, not the *slope*:** the ~$8–11M/rack-year IaaS figure is a *neocloud rental rate* — the most competed-down layer (§8). An **infrastructure owner-operator** that does not pay a renter's markup, and that sells a *differentiated* product, can sit above that rate. So the calculator's anchor may legitimately be the higher end of the band (toward $11–16M/rack-year for owner-operator or inference-service economics), and a **premium** is applied on top. What the trajectory does *not* support is the *growth slope* tracking FLOPS. Baseline: defensible to lift. Slope: must stay modest. This is the cleanest synthesis of the founder↔assistant exchange — the layer matters for the *level*; the FLOPS-vs-revenue gap governs the *trend*.

---

## 8. $/FLOP and $/kW — Derived Efficiency Trends

### 8.1 $/FLOP — capital and rental cost per unit compute

| Metric | H100 (2023) | GB200 (2024–25) | Rubin VR200 (2026) | Rubin Ultra (2027) | Direction |
|---|---|---|---|---|---|
| Rack price per peak PFLOP (capital) | ~$3,000/PF (FP8-equiv) | ~$2,100/PF FP4 | ~$3,000–4,900/PF | ~$1,000–1,700/PF | **falling** |
| Per-GPU $/PFLOP (capital) | ~$5,053/PFLOP | ~$3,000–3,500 (B200) | — | — | **falling** |
| Rental $/effective-FLOP-hour | baseline | ~7× cheaper inference vs H100 | cheaper still | cheaper still | **falling fast** |

**Reading.** $/FLOP falls relentlessly on every basis — capital and rental. NVIDIA itself markets each generation on "$/token down." B200 delivers ~7× cheaper inference per token than H100 despite a higher hourly rate (Silicon Data). **$/FLOP is the buyer's tailwind** — it is the cost of intelligence (§5) viewed from the hardware side. The orbital venture cannot capture this; it is the thing being competed away.

### 8.2 $/kW — capital cost per unit power (the orbital-relevant ratio)

| Generation | Rack price | Rack power | **Rack $/kW (capital)** | Tag |
|---|---|---|---|---|
| DGX H100 (2022–23) | ~$440K | ~10.2 kW | **~$43,000/kW** | [DERIVED] |
| GB200 NVL72 (2024–25) | ~$3.2M | ~130 kW | **~$24,600/kW** | [DERIVED] |
| GB300 NVL72 (2025–26) | ~$6.25M | ~145 kW | **~$43,100/kW** | [DERIVED] |
| Rubin VR200 NVL72 (2026) | ~$7M | ~210 kW | **~$33,300/kW** | [DERIVED] |
| Rubin Ultra NVL576 (2027) | ~$20M | ~600 kW | **~$33,300/kW** | [DERIVED/PROJECTION] |

**Reading — and why $/kW matters more to orbit than $/FLOP.** Rack capital cost per kW is **roughly flat-to-noisy in the ~$25–43K/kW band** — there is no strong trend. This is the orbitally-relevant efficiency metric because **orbital node mass scales with kW** (§2, §4). A flat $/kW means: every extra kW of rack the venture flies costs roughly the same in *rack dollars* — but a *rising* amount in *solar + radiator mass and launch*. So as racks get more powerful, the **non-rack** (power/thermal/launch) cost per kW does not fall the way $/FLOP does. The buyer's $/FLOP tailwind does not become the orbital operator's tailwind, because the operator's binding cost is indexed to **watts**, and watts are not getting cheaper to fly.

---

## 9. Energy Cost — Terrestrial AI-Data-Center Power Cost Trajectory

### 9.1 Historical → projected

| Year | U.S. industrial rate ($/kWh) | Contracted hyperscale / PPA ($/kWh) | Wholesale signal | Tag |
|---|---|---|---|---|
| 2021 | ~$0.067 | ~$0.04–0.06 | pre-AI-boom | [FACT] EIA |
| 2023 | ~$0.081 | ~$0.04–0.07 | rising | [FACT] EIA |
| 2025 | ~$0.086 | ~$0.04–0.07 (PPA-insulated) | PJM Q1 ~$77.78/MWh | [FACT] EIA / `energy_operating_costs.md` |
| 2026 | ~$0.088–0.095 | ~$0.05–0.08 | **PJM Q1 ~$136.53/MWh, +75% YoY** | [FACT] |
| 2028 | ~$0.10–0.12 (proj.) | ~$0.06–0.10 | data-center demand +nearly 2× | [PROJECTION] |
| 2030 | ~$0.11–0.14 (proj.) | ~$0.07–0.12 | "industrial rates +up to 40% vs 2025" | [PROJECTION] |
| 2033 | ~$0.13–0.17 (proj.) | ~$0.08–0.14 | — | [PROJECTION] |
| 2036 | ~$0.15–0.20 (proj.) | ~$0.09–0.16 | — | [PROJECTION] |

**Reading.** The headline trajectory is **clearly up**. Wholesale prices in AI-heavy regions are spiking (PJM +75% YoY 2025→2026; some capacity-auction prices up ~267% over five years). The IEA expects U.S. data-center power demand +~130% by 2030; analysts project industrial rates up to +40% by 2030. **However** — and this is the honest qualifier `energy_operating_costs.md` already established — large *contracted* hyperscale buyers are substantially **insulated by long-term PPAs and special tariffs**; the worst spikes hit residential and uncontracted wholesale. So the contracted-buyer line rises, but more slowly than the headline.

### 9.2 Why this is a (modest) tailwind for orbit

Orbit converts a *recurring, rising* power bill into a *one-time* solar-array capex — no utility bill, ever. As terrestrial power gets more expensive, the value of that avoided bill grows. Per `energy_operating_costs.md`, 5-year per-rack electricity is ~$0.56M today (~16% of a ~$3.5M rack). If industrial rates rise ~40% by 2030 and racks also draw far more power (130 kW → 600 kW), the *absolute* avoided energy bill per node grows several-fold — a 600 kW Rubin-Ultra-class node terrestrially could spend **~$3–6M+ over 5 years on electricity** at 2030 rates. That is still **second-order against launch**, but it is a real and *growing* line, and — importantly — it is one of the few trajectory items moving *in the venture's favor*. The genuinely large terrestrial-power story remains non-financial: orbit sidesteps the multi-year **grid-interconnect queue** (median ~5 yr, up to ~12 yr for data centers) and water permitting entirely.

---

## 10. Synthesis I — Value-Capture by Layer

As compute prices fall (§5, §8), the money does not vanish — it redistributes. The question for the orbital venture: **which layer is it, and does that layer keep margin?**

### 10.1 The four layers, with data

| Layer | What it sells | Gross margin | Operating margin | Held or competed down? | Moat |
|---|---|---|---|---|---|
| **Chipmaker (NVIDIA)** | Scarce frontier silicon | **~75%** (FY2025; ~71% FY2026) | very high | **HELD** — ~75% GM across V100→Blackwell; H100 ~8–10× markup over BOM | Scarcity + CUDA lock-in |
| **Integrated hyperscaler** (AWS/Azure) | Compute + software + SLA + customer | n/d | **35–49%** segment operating | **HELD** — Azure ~49%, AWS ~35%, Google ~21% | Software + scale + customer ownership |
| **Neocloud / GPU renter** (CoreWeave, Lambda) | Bare GPU-hours | ~68–72% *reported* (overstated) | **~0% / slightly negative** | **COMPETED DOWN** — H100 rental fell ~70% peak-to-trough; honest depreciation eats the margin | None — commodity |
| **Inference-service seller** (token API) | Model output per token | ~50–80% *compute* margin | thin-to-negative (R&D, free tier) | **MIXED** — frontier tier holds price (raised in 2026); commodity tier raced to ~$0.06/M | Model quality — only if genuinely differentiated |

Sources: NVIDIA FY2025/FY2026 (Macrotrends; SEC); `hyperscaler_margins.md`; CoreWeave FY2025 ($5.13B revenue, ~−1% operating margin); a16z/Epoch token-price data.

### 10.2 The pattern — and the historical proof

**Margin pools at the two ends that have a moat; the undifferentiated middle gets competed to zero.**

- **NVIDIA held ~75% gross margin generation after generation** — the cleanest proof that a real moat (scarcity + CUDA) defends margin even as the *product* (FLOPS) deflates ferociously. The chip layer is the trajectory's biggest winner.
- **The neocloud / bare-rental layer is the trajectory's clearest loser.** H100 rental collapsing from ~$8–12 to ~$1.65/GPU-hr (2023→late-2025) is the value-capture story in one number: a layer with no moat, reselling someone else's scarce chip, gets exactly the margin competition allows — which trended to ~0% operating margin once GPU depreciation is counted honestly. CoreWeave runs ~$5B revenue at ~−1% operating margin.
- **Integrated hyperscalers held 35–49%** — not from better silicon (it is the *same* NVIDIA chip) but from the *attribute wrapper*: SLA, security, integration, global footprint. Buyers pay AWS/Azure a **3–6× markup over neocloud for identical hardware** — proof that the premium is paid for *attributes*, not FLOPS.

### 10.3 What this implies for the orbital venture — the founder's question, answered

The founder's framing in `trajectory_notes.md`: *the orbital venture **owns its racks** — it is an infrastructure owner, not the squeezed renter — so it should not be modelled as the collapsing commodity-rental layer.* **This is correct, with one critical boundary:**

- **What owning the asset gets you (real, favorable).** The orbital venture is not a neocloud reselling capacity at a competed-down markup over its own rental cost — it *is* the infrastructure owner. It avoids the renter's margin compression and captures the owner's economics directly. This justifies anchoring revenue toward the **upper end** of the §7 band (owner-operator, not rental rate) — the $11M IaaS figure in the calculator is plausibly too low a *base*. This is a genuine, defensible upgrade to the revenue anchor.
- **What owning the asset does NOT get you (the boundary).** Owning an asset does not by itself confer pricing power. An infrastructure owner still **competes with other infrastructure owners** — terrestrial hyperscalers, who own *their* racks too, at lower cost. The layers that *held* margin (NVIDIA, integrated hyperscalers) held it because of a **moat**, not because they owned hardware. Colocation/data-center owners — the closest pure "infrastructure owner" analog — earn only ordinary low-double-digit margins precisely because owning a building confers no moat.
- **Therefore:** the orbital venture captures a durable premium **only if the orbital niche is genuinely scarce and differentiated** — i.e. only if the *premium is real* (schedule certainty, physical isolation/sovereignty, zero-grid-queue, unshaded solar). The layer distinction is a cleaner *justification* for why a premium can be economically real (the venture behaves like the attribute-differentiated sovereign-cloud layer, which documentably earns +10–30%), and a flag to **re-examine the revenue anchor upward**. But it does not, by itself, manufacture the premium. The premium remains the load-bearing variable — exactly the project's standing conclusion.
- **And the chip tax is inescapable.** Whoever owns the rack, NVIDIA still takes its ~75% cut at the silicon layer. The orbital venture's entire margin must come from the *attribute wrapper* on top of NVIDIA-priced hardware — it does not escape the chip tax, and the trajectory shows that tax is not shrinking.

---

## 11. Synthesis II — Tailwinds vs. Headwinds for the Orbital Venture

Pulling the nine trajectories together into an explicit ledger for the venture.

### 11.1 Tailwinds — what the trajectory puts in the venture's favor

| # | Tailwind | Mechanism | Strength |
|---|---|---|---|
| T1 | **Launch cost shrinks as a share of an ever-pricier rack** | Rack price rises ~2×/generation (§1); launch cost is fixed (~$10–20M). Launch falls from ~50–65% of a rack+launch node today toward ~15–30% by the early-2030s. The launch-cost drag — historically the thing that broke the model — structurally fades. | **Strong, robust.** The single clearest tailwind. Direction is not in doubt. |
| T2 | **Rising terrestrial energy cost widens orbit's free-solar edge** | Terrestrial industrial/PPA rates trend up (§9); orbit has no recurring power bill. As racks also draw far more power, the *absolute* avoided energy bill per node grows several-fold over the horizon. | **Moderate.** Real and growing, but second-order vs. launch. Contracted buyers are PPA-insulated, blunting it. |
| T3 | **Rack mass grows slowly; the rack is not the orbital problem** | kg-per-kW is *falling* (§4). The terrestrial rack stays a minor (~20%) share of node mass. | **Modest, supportive.** Confirms the rack itself is not the constraint. |
| T4 | **The terrestrial bottleneck (grid queue, water permits) is worsening** | Interconnect queues ~5–12 yr; water moratoria spreading. Orbit sidesteps both. Worsens over the horizon → orbit's schedule/optionality value rises. | **Moderate.** Non-financial but a real and growing differentiator — feeds the premium. |
| T5 | **Inference is the fastest-growing, most orbit-suitable workload** | Inference 55–67% of AI compute today → dominant by 2030 (`ai_datacenter_tam.md`); low inter-node bandwidth, steady power, graceful degradation — all favor orbit. | **Moderate, contextual.** Grows the addressable market the venture targets. |

### 11.2 Headwinds — what the trajectory puts against it

| # | Headwind | Mechanism | Severity |
|---|---|---|---|
| H1 | **Rack power explodes ~5× → heavier node → flyability ceiling tightens** | Rack power ~130 kW → ~600 kW (Rubin Ultra, confirmed) → ~1 MW+ projected (§2). Node mass scales linearly with kW. Rubin Ultra-class racks exceed even the block-upgraded + hot-loop ceiling — **forcing racks/launch 2→1**, then power-capping or on-orbit assembly. | **Severe.** The hardest constraint — physical, not budgetary. A better payback cannot buy back a kilogram of payload. |
| H2 | **Per-rack revenue does NOT track FLOPS** | Compute rises ~10×/3 generations; per-rack gross revenue rises only ~2–3× (§7). Revenue is competition-set, tracking the rack's *price*, not its capability. The FLOPS gain is consumer surplus — it accrues to the buyer. | **Severe (for valuation).** Kills any model that lets node revenue ride the FLOPS curve. Revenue slope must stay modest (~1.5–2×/gen). |
| H3 | **In-generation revenue decay** | Rental rates fall hard as silicon ages — H100 fell ~70% peak-to-trough (§6). An orbital node holds one fixed rack it cannot refresh; its revenue is front-loaded and decays over its 5-yr life. | **Moderate-high.** Already partly in the calculator (declining-revenue curve); the trajectory confirms the decay is real and steep. |
| H4 | **The commodity layer is being competed to zero margin** | The bare-rental layer the venture most resembles (if it sells raw capacity) earns ~0% operating margin (§10). Selling commodity tokens is a race to ~$0.06/M (§5). | **Moderate.** Avoidable — but only by being genuinely differentiated. Sets the floor the premium must clear. |
| H5 | **Trailing-generation risk** | A multi-year launch/integration lag means an orbital node may field a *trailing* GPU generation vs. terrestrial state-of-the-art, depressing its revenue-per-watt and competitiveness from day one. | **Moderate.** Structural to the architecture; widens as the generation cadence stays ~12–18 months. |
| H6 | **$/kW is flat — orbit's binding cost does not deflate** | $/FLOP falls fast (buyer's tailwind) but $/kW is flat (§8). Orbital node cost is indexed to *watts*, and watts are not getting cheaper to fly. The deflation that helps compute buyers does not reach the orbital operator. | **Moderate.** Explains why the buyer's cost-of-intelligence collapse is not the venture's tailwind. |

### 11.3 The net read

The trajectory is **genuinely two-sided, and the two sides are coupled to the same variable — the GPU generation.** Advancing generations make the venture's *cost structure* better (T1: launch shrinks as a share; pricier racks make the launch trivial) and its *operating environment* better (T2, T4: terrestrial energy and permitting worsen). But the *same* advancing generations make the node *physically harder to fly* (H1: power explodes) and do *not* lift per-rack revenue proportionally (H2: revenue tracks price, not FLOPS).

So the honest synthesis for the calculator's trajectory layer:
- **Model rack cost rising ~2×/generation** — and let launch shrink as a share. (Tailwind, robust.)
- **Model rack power rising per §2** — and let node mass rise with it, forcing racks/launch 2→1 at Rubin-Ultra-class power. (Headwind, severe, physical.)
- **Model per-rack gross revenue rising only ~1.5–2×/generation** — tracking price, NOT the ~10×/3-gen FLOPS curve — and decaying within each generation. (Headwind H2/H3 — the most important modelling correction.)
- **The premium remains the load-bearing variable.** Nothing in the trajectory creates or destroys it. The trajectory's contribution is to show *why* a premium is economically necessary (commodity layers deflate to zero margin) and *why* it is plausible (attribute-differentiated layers documentably hold one). The venture's value is not in riding the FLOPS curve — it is in being a *scarce, differentiated infrastructure owner* whose fixed launch cost shrinks against a rising rack price, in a world where terrestrial capacity is increasingly bottlenecked.

---

## Sources

**Rack cost / pricing history**
- [Tom's Hardware — Vera Rubin NVL72 racks up to $8.8M apiece](https://www.tomshardware.com/tech-industry/artificial-intelligence/price-of-nvidias-vera-rubin-nvl72-racks-skyrockets-to-as-much-as-usd8-8-million-apiece-but-server-makers-margins-will-be-tight-nvidia-is-moving-closer-to-shipping-entire-full-scale-systems)
- [Investing.com / Kuo — VR200 NVL72 brings major power upgrades; ~$5–7M quotes](https://www.investing.com/news/stock-market-news/nvidias-vr200-nvl72-ai-server-brings-major-power-upgrades--kuo-93CH-4432521)
- [Tom's Hardware — Blackwell superchips up to $70K, racks up to $3M+](https://www.tomshardware.com/pc-components/gpus/nvidias-next-gen-blackwell-ai-gpus-to-cost-up-to-dollar70000-fully-equipped-servers-range-up-to-dollar3000000-report)
- [Spheron — NVIDIA B300 / GB300 NVL72 ~$6–6.5M guide](https://www.spheron.network/blog/nvidia-b300-blackwell-ultra-guide/)
- [IntuitionLabs — NVIDIA AI GPU pricing guide (H100 $27K–40K)](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide)
- [TweakTown — Volta DGX-1 at $149,000](https://www.tweaktown.com/news/57487/nvidias-new-volta-powered-dgx-1-costs-149-000/index.html)
- [NVIDIA Newsroom — DGX A100 launch (~$199K)](https://nvidianews.nvidia.com/news/nvidia-ships-worlds-most-advanced-ai-system-nvidia-dgx-a100-to-fight-covid-19-third-generation-dgx-packs-record-5-petaflops-of-ai-performance)
- [Wikipedia — Nvidia DGX (DGX H100 list price)](https://en.wikipedia.org/wiki/Nvidia_DGX)
- [tech-insider — NVIDIA Blackwell GPU pricing B200/B300](https://tech-insider.org/nvidia-blackwell-gpu-pricing/)

**Rack power / specs / roadmap**
- [DCD — Rubin Ultra NVL576 rack expected to be 600kW, H2 2027](https://www.datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027/)
- [Introl — NVIDIA Vera Rubin: 600kW racks by 2027](https://introl.com/blog/nvidia-vera-rubin-gpu-600kw-racks-2027)
- [Tom's Hardware — NVIDIA enterprise roadmap: Rubin, Rubin Ultra, Feynman](https://www.tomshardware.com/tech-industry/semiconductors/nvidia-enterprise-roadmap-rubin-rubin-ultra-feynman-and-silicon-photonics)
- [TweakTown — NVIDIA roadmap, Feynman in 2028](https://www.tweaktown.com/news/110521/nvidia-updates-roadmap-with-new-details-on-its-next-gen-gpu-feynman-coming-in-2028/index.html)
- [NextPlatform — NVIDIA GPU system roadmap to 2028](https://www.nextplatform.com/2025/03/19/nvidia-draws-gpu-system-roadmap-out-to-2028/)
- [NVIDIA DGX-1 datasheet (Volta, ~3.5 kW, 134 lb)](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/dgx-1/NVIDIA-DGX-1-Volta-AI-Supercomputer-Datasheet.pdf)
- [NVIDIA DGX A100 datasheet (~6.5 kW, 271 lb)](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/nvidia-dgx-a100-datasheet.pdf)
- [The Register — A closer look at NVIDIA's 120kW DGX GB200 NVL72](https://www.theregister.com/on-prem/2024/03/21/a-closer-look-at-nvidias-120kw-dgx-gb200-nvl72-rack-system/912087)
- [Sunbird DCIM — GB300 NVL72 power](https://www.sunbirddcim.com/blog/how-much-power-does-nvidia-gb300-nvl72-need)

**FLOPS / GPU specs**
- [Exxact — Blackwell vs Hopper tensor throughput comparison](https://www.exxactcorp.com/blog/hpc/comparing-nvidia-tensor-core-gpus)
- [E2E Networks — A100 vs H100 vs H200 comparison](https://www.e2enetworks.com/blog/nvidia-a100-vs-h100-vs-h200-gpu-comparison)
- [Awesome Agents — NVIDIA Rubin R200 specs](https://awesomeagents.ai/hardware/nvidia-rubin-r200/)
- [Glenn Lockwood — NVIDIA Rubin R200 notes](https://www.glennklockwood.com/garden/processors/R200)

**Token prices / cost of intelligence**
- [a16z — Welcome to LLMflation (10×/yr; 1,000× in 3 yr)](https://a16z.com/llmflation-llm-inference-cost/)
- [Epoch AI — LLM inference prices have fallen rapidly but unequally](https://epoch.ai/data-insights/llm-inference-price-trends)
- [DeployBase — Cost per token over time](https://deploybase.ai/articles/cost-per-token-over-time-how-llm-api-pricing-has-dropped)
- [TokenMix — AI API pricing history (GPT-4 $30/$60 at launch)](https://tokenmix.ai/blog/ai-pricing-trends-history)
- [deeplearning.ai — Falling LLM token prices](https://www.deeplearning.ai/the-batch/falling-llm-token-prices-and-what-they-mean-for-ai-companies/)

**GPU rental rates**
- [Silicon Data — H100 rental price over time (2023–2025)](https://www.silicondata.com/blog/h100-rental-price-over-time)
- [SemiAnalysis — The Great GPU Shortage, H100 rental index](https://newsletter.semianalysis.com/p/the-great-gpu-shortage-rental-capacity)
- [IntuitionLabs — H100 rental prices across 15+ providers (2026)](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison)
- [Spheron — GPU cloud pricing 2026](https://www.spheron.network/blog/gpu-cloud-pricing-comparison-2026/)
- [Latent Space — $2 H100s: how the GPU rental bubble burst](https://www.latent.space/p/gpu-bubble)
- [getdeploying — GB200 cloud pricing](https://getdeploying.com/gpus/nvidia-gb200)

**Margins / value capture**
- [Macrotrends — NVIDIA gross margin 2012–2026](https://www.macrotrends.net/stocks/charts/NVDA/nvidia/gross-margin)
- [Sacra — CoreWeave revenue, valuation & funding](https://sacra.com/c/coreweave/)
- [Motley Fool — CoreWeave's "weirdly high" gross margin](https://www.fool.com/investing/2025/10/29/the-hidden-truth-behind-coreweaves-weirdly-high-gr/)
- [Silicon Data — B200 inference cost vs H100 (~7× cheaper per token)](https://www.silicondata.com/blog/b200-rental-price-march-2026-update)

**Energy cost trajectory**
- [Bloomberg — How AI data centers are sending power bills soaring](https://www.bloomberg.com/graphics/2025-ai-data-centers-electricity-prices/)
- [IEA — Energy demand from AI](https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai)
- [CNBC — AI data center frenzy is pushing up electricity bills](https://www.cnbc.com/2025/11/26/ai-data-center-frenzy-is-pushing-up-your-electric-bill-heres-why.html)
- [Yale Climate Connections — data centers pay less, residential bills soar](https://yaleclimateconnections.org/2026/01/home-electricity-bills-are-skyrocketing-for-data-centers-not-so-much/)
- [Tom's Hardware — PJM 76% wholesale price spike](https://www.tomshardware.com/tech-industry/ai-data-centers-trigger-massive-irreversible-76-percent-electricity-price-spike-in-largest-us-region-federal-watchdog-demands-tech-giants-pay-for-their-own-power-infrastructure)

*Project-internal companions: [rack_cost_trajectory.md](../economics/rack_cost_trajectory.md), [revenue_per_watt.md](../economics/revenue_per_watt.md), [energy_operating_costs.md](../economics/energy_operating_costs.md), [hyperscaler_margins.md](../economics/hyperscaler_margins.md), [ai_datacenter_tam.md](../economics/ai_datacenter_tam.md), and [ai_hardware.md](../ai_hardware/ai_hardware.md). Historical companions referenced above include retired `data_science/REPORT.md` and retired root `CONCLUSION.md` Rev 4–8; those are no longer current navigation targets.*

---

## Confidence

**Overall: Moderate.**

- **High** on the historical blocks (2017–2026): NVIDIA hardware specs (power, mass, FLOPS), token-price history, GPU rental history, and NVIDIA gross margins are all well-documented and cross-checked against ≥2 sources. The DGX-era power/mass figures come straight from NVIDIA datasheets.
- **Moderate** on the near-term (2026–2027) projections: Rubin VR200 and Rubin Ultra figures are partly confirmed (the 600 kW NVL576 is a firm NVIDIA roadmap number) and partly leak/estimate (rack prices, VR200 power band, Rubin masses — NVIDIA confirms no rack list prices).
- **Low-to-moderate** on the 2028–2036 projections: these are explicitly directional. The *direction* of every trajectory (rack cost up, power up, FLOPS up, $/FLOP down, $/token down, energy cost up, per-rack revenue up-but-lagging-FLOPS) is robust and multiply-corroborated. The *magnitudes* a decade out are subjective extrapolations of observed cadences and should be treated as ±50–100%.
- **Softest single input:** the **$/rack-year revenue trajectory (§7)**. NVIDIA confirms no rack prices; full-rack rental quotes are thin; the figure swings ±2–3× on pricing tier (on-demand vs. contract) and utilization. The *qualitative* finding — revenue tracks price, not FLOPS — is robust; the absolute dollars are not.

---

## Open Questions

1. **Per-rack revenue level vs. slope.** §7 establishes the *slope* (revenue tracks price ~2×/gen, not FLOPS ~10×/3-gen). The *level* — whether an owner-operator anchor is ~$8M, ~$11M, or ~$16M/rack-year — is unresolved and depends on the IaaS-vs-inference-service and rental-vs-owner-economics question flagged in `revenue_per_watt.md`. The calculator's trajectory layer needs a defensible *base*, not just a slope.
2. **Will NVIDIA hold the ~2×-per-generation rack-price cadence?** The 10-year rack-cost projection rests on it. AMD MI-series, hyperscaler custom silicon (TPU, Trainium, Maia), and a possible AI-capex slowdown could flatten it. A pricing plateau weakens tailwind T1 but does not reverse it.
3. **Where exactly does the racks/launch 2→1 reversal land?** §2 says "Rubin-Ultra-class (~600 kW)" — but the precise rack power at which a block-upgraded Neutron node drops from 2 racks to 1 depends on the node mass model (`simulations/REPORT.md`) and the hot-loop assumption. Needs a dedicated crossover calculation, not a directional estimate.
4. **Trailing-generation discount.** H5 (the orbital node fields a trailing GPU generation due to launch/integration lag) is identified but not quantified. How many months/generations behind, and what revenue-per-watt haircut does that imply? Belongs in the calculator as an explicit derate.
5. **Does the precision floor keep dropping below NVFP4?** Much of the FLOPS trajectory (§3) is lower-precision arithmetic. If the industry hits a precision floor (~FP4 may be near the practical limit for quality), the per-generation FLOPS multiplier shrinks toward the raw-transistor rate — flattening §3 and, indirectly, the compute-vs-revenue gap in §7.
6. **Power-capping economics.** §2/§11 note that Rubin-Ultra-class racks must be power-capped (down-clocked/partially populated) to fly. A power-capped rack delivers less compute *and* less revenue — but how does revenue-per-flown-kW compare to a flagship rack at an earlier generation? This trade is unmodelled and could matter more than the generation choice itself.
7. **Energy-cost projection for contracted buyers.** §9 shows headline rates rising fast but contracted hyperscale buyers PPA-insulated. The *contracted* trajectory — the one that actually sets terrestrial competitors' cost — is genuinely uncertain; the ~$0.07–0.16/kWh 2036 range is wide.
