# Modern AI Data Center Hardware: What an "AI Rack" Physically Is

**Research date:** 2026-05-17
**Purpose:** Feasibility input for orbital AI-inference data center project. Focus on the physical reality of AI compute hardware — mass, power, and (critically) heat — so we can identify which terrestrial "free" support systems become hard problems in space.

---

> **Source status (2026-05-25):** See [SOURCE_INDEX.md](../SOURCE_INDEX.md) claim IDs GPU-001 through GPU-012. GB200/GB300 configurations are well supported by NVIDIA and OEM materials. GB300 mass/power should be vendor-specific, Vera Rubin rack power is still an estimate, Rubin Ultra/Feynman are roadmap projections, and Rubin CPX 370 kW is not source-certified.

## 1. Summary Spec Tables

### 1.1 NVIDIA rack-scale systems (per full rack)

| Spec | GB200 NVL72 | GB300 NVL72 | Vera Rubin NVL72 |
|---|---|---|---|
| Status (as of May 2026) | Shipping since ~2024 H2 | Shipping / ramping (Microsoft, others deployed late 2025) | Announced; production H2 2026 |
| GPUs per rack | 72 Blackwell (B200) | 72 Blackwell Ultra (B300) | 72 Rubin GPUs/packages; die-count wording is not the model unit |
| CPUs per rack | 36 Grace (ARM) | 36 Grace (ARM) | 36 Vera (ARM) |
| Compute trays | 18 | 18 | 18 |
| NVSwitch trays | 9 | 9 | 9 |
| Rack weight | ~1,360 kg (1.36 t / ~3,000 lb) | OEM-specific; roughly ~1,500–1,580 kg in current public materials | Not officially published (est. ~1,400–2,000 kg) |
| Rack form factor | ~48U, OCP/Oberon (600 mm W × 1,068 mm D class) | ~48U, Oberon-class 19"/OCP | Oberon-class (same footprint family) |
| Rack power draw | ~120 kW nominal; 130–132 kW observed under load | OEM-specific; ~132 kW nominal and up to ~155 kW peak in current public materials | ~190 kW (estimate; not a public NVIDIA rack spec) |
| Power per GPU | ~1.0–1.2 kW (B200 TGP ~1.0–1.2 kW) | ~1.4 kW (B300 TDP) | estimate only |
| Cooling | Direct liquid cooling (DLC) mandatory; ~85–90% liquid, rest air | Hybrid: ~90% liquid / ~10% air | Direct liquid; warm-water DLC |
| Heat to reject | ≈ rack power (~120–132 kW thermal) | ≈ rack power (~132–155 kW thermal) | ≈ rack power (~190 kW thermal) |
| FP4 compute (rack) | 1,440 PFLOPS (1.44 EF) with sparsity | 1,400 PFLOPS dense / ~1.1 EF "exaFLOPS" cited | 3,600 PFLOPS (3.6 EF) NVFP4 inference |
| FP8 compute (rack) | ~720 PFLOPS | ~720 PFLOPS FP8/FP6 | ~1,200 PFLOPS (1.2 EF) FP8 training |
| HBM capacity (rack) | 13.4–13.5 TB HBM3e | ~20.7 TB HBM3e | ~20.7 TB HBM4 (~20,736 GB) |
| HBM per GPU | 192 GB HBM3e | 288 GB HBM3e | 288 GB HBM4 |
| HBM bandwidth per GPU | ~8 TB/s | ~8 TB/s | ~13 TB/s (GTC '25 spec) → target ~20–22 TB/s |
| HBM bandwidth (rack) | ~576 TB/s | ~576 TB/s | >1 PB/s |
| NVLink bandwidth (rack, aggregate) | 130 TB/s | 130 TB/s | ~260 TB/s (NVLink 6, ~2×) |
| NVLink per GPU | 1.8 TB/s (NVLink 5) | 1.8 TB/s (NVLink 5) | 3.6 TB/s (NVLink 6) |

**Notes on disagreements / flags:**
- GB300 rack power is reported inconsistently: NVIDIA marketing says "~120 kW" on the GB300 page; OEM datasheets (Supermicro, Lenovo, HPE) and DCIM analyses cite **132–140 kW typical, 135 kW TDP, ~155 kW peak**. Treat **~135 kW** as the planning number and ~155 kW as worst case.
- GB200 "120 kW" is NVIDIA's nominal figure; HPE QuickSpecs and field reports show **130–132 kW** actual (HPE breakdown: 115 kW liquid + 17 kW air = 132 kW). Use **~132 kW** for engineering margin.
- Vera Rubin NVL72 power is **not yet an official published rack spec**. "~190 kW" comes from secondary analysis and trade press; some early guidance said "120–130 kW similar to current." Do not use "NVL144" as the standard rack name unless the text is explicitly discussing package/die-count ambiguity. Flag as **estimate, version-dependent, will change before H2 2026 launch.**
- "1.44 EF" (GB200) and "3.6 EF" (Rubin) FP4 figures include sparsity / are NVIDIA "Jensen math." Dense numbers are roughly half. Flag all FLOPS as vendor-quoted peak, not sustained.

### 1.2 Per-GPU summary

| GPU | Node | FP4 (peak) | HBM | HBM BW | TDP |
|---|---|---|---|---|---|
| B200 (Blackwell) | GB200 NVL72 | ~20 PFLOPS | 192 GB HBM3e | ~8 TB/s | ~1.0–1.2 kW |
| B300 (Blackwell Ultra) | GB300 NVL72 | ~15 PFLOPS dense / ~30 w/ sparsity | 288 GB HBM3e | ~8 TB/s | ~1.4 kW |
| R200 (Rubin) | VR NVL72 | ~50 PFLOPS NVFP4 (per package) | 288 GB HBM4 | ~13→22 TB/s | estimate only |
| Rubin CPX | VR CPX variant | ~30 PFLOPS NVFP4 | 128 GB **GDDR7** | (GDDR7, lower) | not source-certified here |

---

## 2. NVIDIA Rack-Scale Systems in Detail

### 2.1 GB200 NVL72 (Blackwell — the current workhorse)

The GB200 NVL72 is a single liquid-cooled rack that NVIDIA treats as one logical unit ("rack is the new server"). It contains:
- **18 compute trays**, each with 2 GB200 "superchips" (2 B200 GPUs + 1 Grace CPU per superchip) → 72 B200 GPUs + 36 Grace CPUs.
- **9 NVLink switch trays** carrying 18 NVLink-5 switch ASICs that form a non-blocking all-to-all fabric across all 72 GPUs.
- Form factor: ~48U in an OCP Open Rack V3 / "Oberon" cabinet, ~600 mm wide × ~1,068 mm deep (L-rail/equipment depth; the full **cabinet external depth is ~1,200 mm** including doors/clearances — `node_design/node_mass_model.md` §1 uses the 1,200 mm cabinet figure for packaging) — wider/deeper than a legacy 19" rack.

**Mass:** ~1,360 kg (1.36 t, ~3,000 lb) fully populated. Two independent sources agree (Sunbird DCIM; multiple OEM/press citations).

**Power:** NVIDIA nominal 120 kW; real deployments and HPE QuickSpecs show **130–132 kW** under full load (115 kW liquid-captured + 17 kW air-captured). Power per GPU ≈ 1.0–1.2 kW; the rest is CPUs, NVSwitches, NICs, PSU losses, fans.

**Cooling:** Direct-to-chip liquid cooling is **mandatory** — air cooling is not viable at 120+ kW in a single rack. Cold plates sit on GPUs, CPUs, and NVSwitch ASICs. ~85–90% of heat goes to liquid; the ~10–15% remainder (optics, PSUs, drives) is air-cooled.

**Compute & memory:** 1,440 PFLOPS FP4 (with sparsity), ~720 PFLOPS FP8; 13.4–13.5 TB unified HBM3e (192 GB/GPU); ~576 TB/s aggregate HBM bandwidth; 130 TB/s aggregate NVLink bandwidth.

### 2.2 GB300 NVL72 (Blackwell Ultra — inference/reasoning optimized)

Same rack architecture and footprint as GB200, upgraded to B300 "Blackwell Ultra" GPUs. NVIDIA explicitly markets it for **test-time-scaling inference and AI reasoning**.

**Key deltas vs GB200:**
- HBM grows from 192 → **288 GB per GPU** (12-high HBM3e stacks) → ~20.7 TB per rack. This matters: inference is memory-capacity- and bandwidth-bound, so the bigger memory pool is the headline inference feature.
- ~1.5× denser FP4 tensor throughput and ~2× attention performance vs Blackwell.
- Power rises: **~135 kW TDP, ~132–140 kW typical, up to ~155 kW peak.** Per-GPU TDP ~1.4 kW.
- Cooling is hybrid (~90% liquid / ~10% air); CPUs, GPUs, NVSwitch liquid-cooled, OSFP optics / drives / power-distribution-board air-cooled.
- Floor loading is OEM-specific; current public GB300 integrations put the fully populated rack closer to roughly **1.5 t** than the older 1.36 t GB200 planning number.

**Deployment reality (as of late 2025/2026):** Microsoft Azure brought up the first "supercomputer-scale" GB300 NVL72 cluster — 4,608 GB300 GPUs (64 racks) — for OpenAI workloads. This confirms GB300 is in volume production.

### 2.3 Vera Rubin NVL72 (next gen — H2 2026)

Announced at GTC 2025, detailed further at CES 2026. **Production targeted H2 2026** — not yet shipping, specs still moving.

- 72 Rubin (R200) GPUs/packages. Some early notes used die-count language; this doc now uses the public rack-scale product unit, **Vera Rubin NVL72**, for model consistency. 36 Vera CPUs. Same Oberon-class rack family as GB200/GB300 — deliberately infrastructure-compatible.
- ~3.6 EF NVFP4 inference / ~1.2 EF FP8 training per rack.
- ~20.7 TB HBM4 (288 GB/GPU package), HBM bandwidth per GPU jumps to ~13 TB/s (GTC spec) with NVIDIA targeting ~20–22 TB/s in production.
- NVLink 6: ~3.6 TB/s per GPU, roughly double Blackwell; aggregate ~260 TB/s.
- **Power: ~190 kW per rack** (reported/estimated, not official). Roadmap variants may go much higher; the previously cited **Rubin CPX ~370 kW** value is **not certified** by this source audit, while future "Rubin Ultra" rack power near **~600 kW** should be treated as a roadmap target rather than a shipping specification.

### 2.4 Rubin CPX — inference-specialized accelerator (directly relevant to this project)

NVIDIA's most inference-specific 2026 product. Rubin CPX ("Context Phase") is a **monolithic GPU with 128 GB of GDDR7** (not HBM) — deliberately "fat on compute, skinny on memory bandwidth." ~30 PFLOPS NVFP4.

It implements **disaggregated inference**: the **prefill/context phase** (compute-bound, processing the prompt / long context) runs on cheap-memory Rubin CPX; the **decode/generation phase** (memory-bandwidth-bound, token-by-token output) runs on standard HBM Rubin GPUs. The larger Vera Rubin CPX rack combines Rubin CPX accelerators, Rubin GPUs, and Vera CPUs for a much larger inference system. The earlier **~370 kW** rack-power value remains **not source-certified** in this corpus and should not be quoted as a public NVIDIA spec.

**Why this matters for us:** it shows the industry is already physically separating inference into compute-heavy and memory-heavy hardware. An orbital inference design could potentially pick the phase/hardware mix that best matches its power and thermal envelope.

---

## 3. Networking — Scale-Up vs Scale-Out

AI clusters have **two distinct network tiers**:

### 3.1 Scale-up (inside the rack / NVLink domain)
- **NVLink + NVLink Switch** forms a non-blocking, all-to-all fabric so every GPU talks to every other GPU as if it were one giant GPU.
- NVLink 5 (Blackwell): **1.8 TB/s per GPU** (18 links × 100 GB/s bidirectional), ~130 TB/s aggregate per NVL72 rack — ~14× PCIe Gen5, ~18× the scale-out bandwidth.
- NVLink 6 (Rubin): ~3.6 TB/s per GPU.
- The NVLink Switch System can extend the scale-up domain to **576 fully connected GPUs** (8 NVL72 racks) — a "superpod" supernode with >1 PB/s total bandwidth, any-GPU-to-any-GPU at full NVLink speed without touching the slower network.

### 3.2 Scale-out (between racks / pods)
- **InfiniBand (NVIDIA Quantum-X800)** or **Spectrum-X Ethernet** connects racks/pods. Current generation: ConnectX-8 NICs at **800 Gb/s**; Quantum-X800 Q3400 switches with 144 × 800 Gb/s ports.
- Topology example (GB200/GB300 SuperPod): 8 NVL72 racks (576 GPUs) + 8 leaf switches = one "Scalable Unit" (SU); up to 16 SUs → 9,216 GPUs with 128 leaf switches in a fat-tree.
- Spectrum-X Ethernet brings InfiniBand-style congestion control to Ethernet, achieving ~95% throughput vs ~60% for vanilla Ethernet.

### 3.3 Relevance to inference / space
- **Inference needs far less scale-out bandwidth than training.** A single NVL72 rack (or even one node) can serve many models entirely within its own NVLink domain. This is favorable for a space deployment: a self-contained rack-scale unit can do useful inference work without a massive inter-rack fabric.
- Between orbital "racks" or satellites, free-space optical / laser links would replace InfiniBand/Ethernet — much lower bandwidth than 800 Gb/s wired, reinforcing that **inference (low inter-node traffic) fits orbit better than training.**

---

## 4. The Chain From Rack to Data Center — What's "Free" on the Ground

A terrestrial AI rack is the visible tip of a large support iceberg. The chain, and what happens to each link in space:

| Terrestrial subsystem | What it does | Status in orbit |
|---|---|---|
| Grid power → substation → transformers | Delivers MW of utility power | **Replaced by solar arrays + batteries.** No grid. Power becomes the hard, mass-driving constraint. |
| UPS / battery / generator backup | Ride-through and backup | Batteries needed for eclipse; no diesel. |
| Power distribution (busways, PDUs, PSUs) | Steps voltage down to the rack | Similar, but every kg counts. |
| **Heat rejection: cold plates → CDU → facility water loop → chillers → cooling towers / dry coolers** | Moves ~100% of rack power as heat to outside air/water | **THE hard problem.** See §5. |
| Raised floor / structural slab | Carries 1.36 t/rack, ~440 psf | Structural load becomes launch load + microgravity; no "floor." |
| Building shell, fire suppression, security | Environmental envelope | Replaced by spacecraft bus / radiation shielding / MMOD protection. |
| Network fabric (InfiniBand/Ethernet, fiber) | Inter-rack + WAN connectivity | Replaced by laser comms; far lower bandwidth. |

**Key insight:** On the ground, a data center rejects heat almost for free — pump water, blow air, evaporate water in a cooling tower. Convection and evaporation do the heavy lifting and scale cheaply. **None of that exists in vacuum.**

---

## 5. Heat Rejection — The Defining Constraint for Orbital Deployment

### 5.1 The physics problem
Essentially **100% of the electrical power into a rack becomes heat** (compute does no mechanical work). So a GB200 rack must shed **~120–132 kW thermal**, a GB300 rack **~135–155 kW**, a Rubin rack **~190 kW**.

On Earth: convection + evaporation. **In vacuum there is no convection and no evaporation to space** — the *only* steady-state heat-rejection path is **thermal radiation** (plus minor conduction within the structure). Radiated power follows the Stefan–Boltzmann law (∝ area × emissivity × T⁴).

### 5.2 What that means for radiator size (order-of-magnitude)
- A practical spacecraft radiator rejects roughly **~350 W/m² at ~300 K** surface temperature (NSS / spacecraft thermal references). Higher radiator temperature helps a lot (T⁴), but coolant/chip limits cap how hot the loop can run.
- At ~350 W/m²: **1 kW needs ~3 m² of radiator.**
- **One GB200 rack (~130 kW) → ~370 m² of radiator.** One GB300 rack (~150 kW) → ~430 m². One Rubin rack (~190 kW) → ~540 m².
- **Reference check — the ISS** rejects ~70 kW of heat through ~840 m² of radiator panels weighing ~1,000 kg. That is roughly **half of one AI rack's heat load**, using nearly a tonne of radiator and a large deployed area. *(Note: the ~840 m² is the **two-sided** figure — both faces of the ISS's double-sided panels, ~6 assemblies × 8 panels. The one-sided **planform** area is ~420 m². The AI-rack figures above are planform/one-sided, so for a like-for-like comparison the ISS is ~420 m² planform — quote consistently in detailed design.)*

### 5.3 Implications
- Radiator **area and mass rival or exceed the compute payload itself.** A single rack's heat rejection could need hundreds of m² of deployable panels and possibly ~1 t+ of radiator hardware.
- Running the coolant loop hotter (warm-water DLC, which Rubin already favors) shrinks radiator area via the T⁴ term — a key design lever. **But it is not a cost-free lever:** how hot the loop can run is capped by the GPU/HBM **junction temperature (Tjmax ≈ 83–85 °C, barely moving across generations)**, and pushing junctions hotter raises failure rates sharply — roughly an Arrhenius ~2× failure penalty per +10 °C. The radiator-shrink benefit therefore trades against hardware reliability and service life; this is the project's "hot-loop ↔ HBM-thermal tension." See `node_design/hot_chip_thermal_trajectory.md` for the honest treatment of how far the loop can actually be run hot while defending the junction.
- Heat rejection, not raw compute, is likely the **dominant mass and deployment-complexity driver** for an orbital AI data center. This deserves its own detailed thermal study.
- Inference's lower, steadier power draw (vs training's bursty all-GPU peaks) gives a more predictable thermal load — modestly favorable for radiator sizing.

---

## 6. Inference vs Training — Why This Project Should Be Inference-Focused

| Dimension | Training | Inference |
|---|---|---|
| Compute pattern | Forward + backward passes, gradient sync across thousands of GPUs | Forward pass only; prefill (compute-bound) + decode (memory-BW-bound) |
| Interconnect need | Very high — constant all-reduce across the whole cluster; needs huge scale-out fabric | Low — often fits within one rack/node's NVLink domain; little inter-rack traffic |
| Memory | Large (weights + activations + optimizer states + gradients) | Smaller working set; bound by model weights + KV cache; **capacity & bandwidth** matter most |
| Power profile | Bursty, near-peak across all GPUs simultaneously | Lower average, steadier; decode phase draws less power for longer |
| Hardware | Maxed-out GPUs/TPUs, top interconnect | Flexible — GPUs, and increasingly specialized parts (Rubin CPX, GDDR7) |
| Fault tolerance | A failed node can stall a whole job | Requests are independent; a failed node drops some requests, not the job |

**Why inference suits orbit:**
1. **Low inter-node bandwidth** — survivable with laser links; no need to replicate 800 Gb/s InfiniBand in space.
2. **Steadier, lower power** → more predictable, smaller thermal/radiator design point.
3. **Independent requests** → graceful degradation, better fit for the higher fault rates of a space environment.
4. **Self-contained rack-scale units** (one NVL72 = a complete inference engine) map naturally onto modular orbital deployment.
5. NVIDIA's own 2026 direction — GB300 and Rubin CPX — is explicitly inference/reasoning-optimized, so inference-grade hardware is exactly what's shipping.

The main inference-specific cost is **memory** (HBM capacity for weights + KV cache), which is why GB300 doubled HBM per GPU. Memory does not change the thermal story much — it's still ~135 kW/rack to reject.

---

## Sources

NVIDIA official / OEM:
- [NVIDIA GB200 NVL72 product page](https://www.nvidia.com/en-us/data-center/gb200-nvl72/)
- [NVIDIA GB300 NVL72 product page](https://www.nvidia.com/en-us/data-center/gb300-nvl72/)
- [Supermicro GB200 NVL72 datasheet (PDF)](https://www.supermicro.com/datasheet/datasheet_SuperCluster_GB200_NVL72.pdf)
- [Supermicro GB300 NVL72 datasheet (PDF)](https://www.supermicro.com/datasheet/datasheet_SuperCluster_GB300_NVL72.pdf)
- [NVIDIA GB200 NVL72 by HPE QuickSpecs](https://www.hpe.com/psnow/doc/a50009224enw)
- [NVIDIA GB300 NVL72 by HPE QuickSpecs](https://www.hpe.com/psnow/doc/a50009244enw)
- [Lenovo NVIDIA GB300 NVL72 Product Guide](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai)
- [Lenovo GB300-NVL72 Mechanical specifications](https://pubs.lenovo.com/gb300-nvl72/server_specifications_mechanical)
- [NVIDIA Newsroom — Rubin CPX announcement](https://nvidianews.nvidia.com/news/nvidia-unveils-rubin-cpx-a-new-class-of-gpu-designed-for-massive-context-inference)
- [NVIDIA Technical Blog — Rubin CPX for 1M+ token context](https://developer.nvidia.com/blog/nvidia-rubin-cpx-accelerates-inference-performance-and-efficiency-for-1m-token-context-workloads/)
- [NVIDIA Technical Blog — Vera Rubin POD](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/)
- [NVIDIA Blog — Blackwell water efficiency / liquid cooling](https://blogs.nvidia.com/blog/blackwell-platform-water-efficiency-liquid-cooling-data-centers-ai-factories/)
- [NVIDIA DGX SuperPOD GB200 reference architecture — network fabrics](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-gb200/latest/network-fabrics.html)

Power / weight / cooling validation:
- [Sunbird DCIM — Is your data center ready for GB200 NVL72](https://www.sunbirddcim.com/blog/your-data-center-ready-nvidia-gb200-nvl72)
- [Sunbird DCIM — How much power does GB300 NVL72 need](https://www.sunbirddcim.com/blog/how-much-power-does-nvidia-gb300-nvl72-need)
- [The Register — A closer look at NVIDIA's 120kW DGX GB200 NVL72](https://www.theregister.com/2024/03/21/nvidia_dgx_gb200_nvk72/)
- [ToneCooling — GB200 NVL72 cooling requirements](https://tonecooling.com/nvidia-gb200-nvl72-cooling-requirements/)
- [ToneCooling — CDU sizing & integration guide](https://tonecooling.com/coolant-distribution-unit-cdu-data-center/)
- [Introl — GB200 NVL72 deployment / liquid cooling](https://introl.com/blog/gb200-nvl72-deployment-72-gpu-liquid-cooled)
- [Introl — NVIDIA Blackwell Ultra / B300 infrastructure](https://introl.com/blog/nvidia-blackwell-ultra-b300-infrastructure-requirements-2025)
- [Build.inc — Data Center Cooling in 2026](https://build.inc/insights/data-center-cooling-technology-2026)
- [Baltimore Aircoil — Data center cooling options](https://baltimoreaircoil.com/articles/data-center-cooling-options)

Rubin / next-gen:
- [ServeTheHome — NVIDIA Rubin platform at CES 2026](https://www.servethehome.com/nvidia-launches-next-generation-rubin-ai-compute-platform-at-ces-2026/)
- [The Register — NVIDIA unpacks Vera Rubin rack at CES](https://www.theregister.com/2026/01/05/ces_rubin_nvidia/)
- [Tom's Hardware — NVIDIA's Vera Rubin platform in depth](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date)
- [Tom's Hardware — NVIDIA boosts Vera Rubin power to ~2,300 W](https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-reportedly-boosts-vera-rubin-performance-to-ward-hyperscalers-off-amd-instinct-ai-accelerators-increased-boost-clocks-and-memory-bandwidth-pushes-power-demand-by-500-watts-to-2300-watts)
- [Tom's Hardware — Microsoft GB300 NVL72 Azure cluster](https://www.tomshardware.com/tech-industry/artificial-intelligence/microsoft-deploys-worlds-first-supercomputer-scale-gb300-nvl72-azure-cluster-4-608-gb300-gpus-linked-together-to-form-a-single-unified-accelerator-capable-of-1-44-pflops-of-inference)
- [SemiAnalysis — Vera Rubin: Extreme Co-Design](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution)
- [SemiAnalysis — Rubin CPX specialized accelerator & rack](https://newsletter.semianalysis.com/p/another-giant-leap-the-rubin-cpx-specialized-accelerator-rack)
- [Introl — Vera Rubin: 600kW Racks by 2027](https://introl.com/blog/nvidia-vera-rubin-gpu-600kw-racks-2027)

Networking:
- [Introl — NVLink and scale-up networking](https://introl.com/blog/nvlink-scale-up-networking-gpu-interconnect-infrastructure-2025)
- [NADDOD — GB200 interconnect architecture analysis](https://www.naddod.com/blog/nvidia-gb200-interconnect-architecture-analysis-nvlink-infiniband-and-future-trends)
- [DEV — B200/B300/GB200/GB300 cluster interconnect analysis](https://dev.to/aicplight/nvidia-b200b300gb200gb300-cluster-interconnect-architecture-analysis-4hka)

Inference vs training:
- [RCR Tech — Training vs inference compute](https://rcrtech.com/semiconductor-news/training-vs-inference-compute/)
- [Glenn Lockwood — Training vs inference](https://www.glennklockwood.com/garden/training-vs-inference)
- [Hedgehog — AI training vs inference networking](https://hedgehog.cloud/blog/ai-training-vs.-inference-designing-networks-for-real-world-ai-machine-learning-workloads)

Spacecraft thermal:
- [Wikipedia — Spacecraft thermal control](https://en.wikipedia.org/wiki/Spacecraft_thermal_control)
- [NSS — Thermal Management in Space](https://www.nss.org/settlement/nasa/spaceresvol2/thermalmanagement.html)
- [NASA — Small Spacecraft Thermal Control SoA](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/)

---

## Open Questions / Uncertainties

1. **GB300 / GB200 power figure spread.** NVIDIA marketing ("~120 kW") vs OEM datasheets / field reports (132–155 kW). Engineering should use the higher OEM numbers. Need a primary OEM datasheet PDF read (HPE QuickSpecs, Supermicro) to lock exact TDP and the liquid/air split.
2. **Vera Rubin rack power and weight are not officially published.** "~190 kW" is third-party (SemiAnalysis / trade press) and has already shifted upward (2,300 W/GPU reports). Rack weight has no public figure at all. Both will firm up closer to H2 2026 launch — revisit.
3. **FLOPS numbers are vendor peak with sparsity ("Jensen math").** Sustained inference throughput is materially lower and workload-dependent. Do not use peak FP4 for capacity planning.
4. **Exact liquid/air heat split per system.** GB200 ~115/17 kW (HPE); GB300 cited ~90/10%. The air-cooled fraction is awkward in vacuum (no air) — needs its own analysis; that ~10–15% may have to be re-engineered to all-liquid for space.
5. **Radiator sizing here is order-of-magnitude.** The 350 W/m² @ 300 K figure is a generic reference; actual sizing depends on coolant loop temperature (warm-water DLC helps via T⁴), radiator orientation vs sun, view factors, and whether deployable vs body-mounted. A dedicated orbital thermal study is needed.
6. **Rack mass vs launch.** ~1.36 t/rack is the terrestrial fully-populated mass; a space version would strip the cabinet/structure but add radiation shielding, structural reinforcement for launch loads, and the radiator system. Net launch mass per "rack-equivalent" is an open number.
7. **Radiation tolerance.** Commercial HBM/GPU silicon is not rad-hardened. SEU/latch-up rates and required shielding mass in the target orbit are unaddressed here and are a major feasibility unknown.
8. **Whether to deploy GPUs at all vs. Rubin CPX-style specialized inference silicon.** GDDR7-based, lower-bandwidth parts may offer a better compute-per-watt and compute-per-kg-of-radiator tradeoff for orbit — worth a dedicated trade study.
