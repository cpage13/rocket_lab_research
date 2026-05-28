# Multi-Rack LLM Inference — Can a Model Be Split Across Separate Laser-Linked Satellites?

*Research compiled May 2026. Part of the Rocket Lab orbital AI-inference data center feasibility study.
Companion to `inference_scaling.md` (one rack per model) and `laser_comms/optical_comms.md` (ISL hardware).*

---

## Summary / Verdict (read this first)

**The question:** If a future frontier model is too big for one NVL72-class rack, must the 2+ racks be
*physically co-located* (forcing a block-upgraded Neutron to carry 2 racks per node), or can the model
be split across **two separate single-rack satellites linked by an optical inter-satellite link (ISL)**?

**The verdict — a qualified yes, and the qualification matters:**

- **Tensor parallelism (TP) cannot survive a satellite hop.** TP needs ~NVLink-class bandwidth
  (~1.8 TB/s per GPU, ~18× a scale-out link) with an AllReduce **every layer** — microsecond-latency-
  critical, ~80–100 synchronization barriers per token. A 100-Gbps-class laser ISL is **~150× too slow**
  in bandwidth. TP must stay inside one rack's NVLink fabric. **This is firm.**
- **Pipeline parallelism (PP), expert parallelism (EP), and data/replica parallelism *can* survive a
  laser hop** — with caveats. PP passes only activations at stage boundaries and tolerates 100–400 Gbps
  links. Replica parallelism needs almost no inter-node bandwidth. EP all-to-all is the borderline case:
  it tolerates a hop for *modern hybrid-attention MoE* models but is latency-sensitive.
- **The standard industry pattern is exactly this split:** TP *within* a rack/node, PP and EP *across*
  racks/nodes. NVIDIA's own multi-rack guidance is "NVLink in the rack, InfiniBand across racks";
  DeepSeek-V3 runs 16-way PP + 64-way EP spanning 8 nodes in production.
- **A laser ISL can match or beat a terrestrial cross-campus link.** Light travels ~47% faster in
  vacuum than in glass fiber. For satellites in a close formation (tens to a few hundred km apart),
  one-way propagation is **sub-millisecond** (~0.33 ms at 100 km) — comparable to or *better than*
  NVIDIA's own "scale-across" Spectrum-XGS product, which links data centers "hundreds of km" apart
  over fiber. Per-terminal ISL bandwidth (100–200 Gbps, Starlink-class) is in the same band as a
  single scale-out NIC.
- **Implication for the thesis:** A laser-meshed cluster of **single-rack satellites** is a viable way
  to run a model too big for one rack — *provided the model is partitioned by PP/EP/replica, not TP*.
  This means the project can keep flying **always-feasible single-rack nodes** and never needs a
  2-rack Neutron node. The conclusion is **strong for pipeline/replica parallelism, moderate for
  expert parallelism**, and rests on the (well-supported) fact that today's giant models are MoE and
  are *designed* to be split this way.

**Confidence:** High that TP cannot cross a satellite link and that PP/replica can. High on the
fiber-vs-vacuum speed and ISL latency physics. Medium on EP-across-ISL (latency-sensitive; depends on
model architecture and on the Mk3.1 100-Gbps terminal shipping — see open questions). Frontier-model
internals remain non-public — flagged throughout.

---

## 1. When does a model need more than one rack?

`inference_scaling.md` established that **one NVL72-class rack holds a whole current 1–2 T-parameter
frontier model** (13.5–20 TB HBM vs 1–2 TB of FP8 weights, with room for KV cache). So why would
anyone ever need a second rack? Three distinct reasons — only one of them forces multi-rack:

1. **The model outgrows one rack's HBM (a *capacity* reason).** This is the only reason that *forces*
   multi-rack and is the focus of this document. A 2 T model in FP8 is ~2 TB; a 10 T model would be
   ~10 TB (FP8) or ~5 TB (FP4) — still inside one GB300 rack's 20 TB, but with shrinking KV-cache
   headroom. The Vera Rubin NVL72 (shipping 2H 2026) carries **20.7 TB of HBM4**
   ([NVIDIA Vera Rubin](https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/),
   [NVIDIA newsroom](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform)). A genuinely
   *>~15 T-parameter* frontier model served at FP8 with realistic KV-cache and batch headroom is the
   regime that overflows a single rack. NVIDIA evidently anticipates this: its **Rubin Ultra NVL576**
   fuses *eight* 72-GPU racks into one 576-GPU NVLink domain
   ([NVIDIA Vera Rubin POD](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/),
   [Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date)) —
   a hardware admission that the largest models are projected to need multiple racks acting as one.
2. **Throughput / scale-out (a *performance* reason).** Even if one rack *holds* the model, serving
   millions of users needs many copies. This is **replica/data parallelism** — independent racks, each
   a full copy, almost no inter-rack traffic. This never forces co-location (see §2, §5).
3. **Disaggregated prefill/decode (an *architecture* reason).** Splitting the compute-bound prefill
   stage from the memory-bound decode stage onto separate nodes (NVIDIA Dynamo pattern). This creates
   real inter-node KV-cache traffic but is latency-tolerant and bounded (see §3, §5).

**How many racks do real models need today?** For *inference*, today's 1–2 T frontier models need
**one rack** (capacity) plus however many replicas throughput demands. The *projected* regime where a
single model's weights+KV genuinely need 2+ racks is the **multi-trillion (>~10–15 T total) MoE**
generation NVIDIA is building Rubin Ultra NVL576 for. **Estimate, not confirmed** — closed-model
parameter counts are non-public; treat the "one rack today, possibly 2+ for the next generation" band
as the planning assumption, consistent with `inference_scaling.md` open question #1.

---

## 2. The parallelism types and their interconnect demands

A model split across many GPUs uses a *mix* of four strategies. The whole question of "can racks be on
separate satellites" reduces to: **which of these can tolerate a laser-ISL hop instead of in-rack
NVLink?** This is the core of the analysis.

### 2.1 Tensor parallelism (TP) — heaviest; **must stay in-rack**

Each layer's weight matrices are sliced across GPUs; every GPU works on every token simultaneously,
then an **AllReduce/AllGather synchronizes after essentially every layer**.

- **Bandwidth:** enormous. A single Llama-3.1-70B query (8 K in / 256 out) moves up to ~20 GB of TP
  synchronization data *per GPU*; batching multiplies this. Rule of thumb: TP needs **~NVLink-class**
  bandwidth — NVLink 5 delivers **1.8 TB/s per GPU**, roughly **18× a scale-out link**
  ([Introl — NVLink](https://introl.com/blog/nvlink-scale-up-networking-gpu-interconnect-infrastructure-2025),
  [NVIDIA NVLink](https://www.nvidia.com/en-us/data-center/nvlink/)).
- **Latency:** microsecond-critical. With ~80–100 layers, there are ~80–100 synchronization barriers
  *per token*; every barrier waits for the slowest GPU. Any added latency multiplies by the layer
  count.
- **Verdict:** TP **cannot cross a rack**, let alone a satellite link. NVIDIA's explicit design rule:
  "a single TP group is always contained in a single GB200 NVL72 rack"; NVLink handles TP, InfiniBand/
  Ethernet handle everything *between* racks
  ([NVIDIA — NVLink/NVSwitch for LLM inference](https://developer.nvidia.com/blog/nvidia-nvlink-and-nvidia-nvswitch-supercharge-large-language-model-inference/),
  [Nebius — GB200 NVL72](https://nebius.com/blog/posts/leveraging-nvidia-gb200-nvl72-gpu-interconnect)).
  A 100–200 Gbps laser ISL is **~100–150× short** of TP's bandwidth need. **This rules out the one
  thing that would force co-located racks — and it rules it out for terrestrial racks too.**

### 2.2 Pipeline parallelism (PP) — light; **tolerates a cross-rack / cross-satellite link**

Consecutive *layers* are assigned to different GPUs/racks like an assembly line. Only the **activation
tensor at each stage boundary** crosses the link — one modest tensor per microbatch, not a per-layer
all-reduce.

- **Bandwidth:** low. Industry guidance: PP "can tolerate lower bandwidth since only activations
  transfer at stage boundaries, making slower cross-node links (100–400 Gb/s InfiniBand) acceptable,"
  whereas TP needs "NVLink (600+ GB/s)"
  ([premai — TP vs PP vs EP 2026](https://blog.premai.io/multi-gpu-llm-inference-tp-vs-pp-vs-ep-parallelism-guide-2026/),
  [BentoML parallelism](https://bentoml.com/llm/inference-optimization/data-tensor-pipeline-expert-hybrid-parallelism)).
- **Latency:** tolerant. A stage boundary is crossed a handful of times per token, not ~100×. Added
  link latency adds to time-to-first-token but does not stall a global barrier. SGLang's 2026 chunked-
  PP work explicitly targets cross-node PP for million-token contexts, scaling to PP4×TP8 with 82.8%
  strong-scaling efficiency ([LMSYS chunked PP](https://www.lmsys.org/blog/2026-01-15-chunked-pipeline/)).
- **Verdict:** PP is the **canonical cross-rack strategy** — "tensor parallelism within nodes,
  pipeline parallelism between nodes" is the standard multi-node recipe
  ([vLLM parallelism](https://docs.vllm.ai/en/stable/serving/parallelism_scaling/)). A 100–200 Gbps
  laser ISL sits squarely inside PP's stated 100–400 Gbps comfort band. **PP across separate
  satellites is feasible.**

### 2.3 Expert parallelism (EP) — the borderline case; **tolerates a hop, but latency-sensitive**

For MoE models, the *experts* are distributed across GPUs; each token is routed via **all-to-all**
communication to the few experts it activates, and the results are gathered back.

- **Bandwidth:** moderate, and *designed to be cross-node*. DeepSeek's production system spans
  **64-way EP across 8 nodes** over 400 Gb/s InfiniBand (~50 GB/s/NIC); measured cross-node dispatch
  bandwidth >50 GB/s, combine ~40 GB/s
  ([DeepEP](https://github.com/deepseek-ai/DeepEP),
  [DeepSeek-V3 report](https://arxiv.org/pdf/2412.19437)). DeepSeek explicitly built kernels to "fully
  utilize InfiniBand and NVLink bandwidths" so EP works *across* nodes.
- **Latency:** this is the catch. Decode-phase all-to-all is **latency-sensitive** — it "can
  contribute 10–30% to end-to-end latency"; "MoE routing is particularly sensitive to interconnect
  latency"; decode targets time-to-incremental-token <25 ms
  ([Meta Engineering — scaling LLM inference](https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/)).
  An all-to-all happens twice per MoE layer per token, so added link latency multiplies by layer
  count — less brutal than TP but not free.
- **Verdict:** EP **can** cross a cross-rack link (DeepSeek does it daily over InfiniBand) and can
  *probably* cross a close-formation laser ISL — but it is the strategy most exposed to the latency
  penalty. Best confined within a node where possible; **tolerable across a short ISL, with a
  throughput cost.** NVIDIA's "Wide-EP" deliberately keeps the heaviest all-to-all on the NVL72's
  ~130 TB/s in-rack NVLink for exactly this reason
  ([NVIDIA Wide-EP](https://developer.nvidia.com/blog/scaling-large-moe-models-with-wide-expert-parallelism-on-nvl72-rack-scale-systems/)).

### 2.4 Data / replica parallelism — trivial; **the easiest to mesh**

Each rack runs a *complete independent copy* of the model and serves its own requests. Inter-node
traffic is just request routing / load-balancing metadata — kilobytes.

- **Bandwidth/latency:** negligible. Replicas have no synchronization barrier; a slow or
  out-of-contact rack does not stall the others ("embarrassingly parallel" — see `inference_scaling.md`).
- **Verdict:** Trivially survives any link, including a laser ISL. **This is the primary scaling axis
  for the orbital constellation** and needs no special interconnect.

### Summary table — interconnect demand vs. survives a laser ISL?

| Parallelism | What crosses the link | Bandwidth need | Latency sensitivity | Survives a 100–200 Gbps laser ISL? |
|---|---|---|---|---|
| **Tensor (TP)** | AllReduce every layer | ~NVLink-class, **TB/s** | Microsecond-critical (~100 barriers/token) | **No** — must stay in-rack NVLink |
| **Pipeline (PP)** | Activation tensor at stage boundary | Low, **100–400 Gbps** | Tolerant (few crossings/token) | **Yes** — comfortably |
| **Expert (EP)** | All-to-all token routing | Moderate, **~40–50 GB/s** in-rack ideal | Sensitive (10–30% of decode latency) | **Borderline yes** — works, with a throughput cost |
| **Data / replica** | Request routing metadata | Negligible | None | **Yes** — trivially |

---

## 3. Terrestrial inter-rack interconnect — what links racks today

Understanding the terrestrial baseline matters because **a laser ISL only has to match the
*terrestrial cross-rack* link, not the in-rack NVLink fabric.** The industry uses a deliberate
two-tier hierarchy:

- **Tier 1 — scale-up (intra-rack):** NVLink / NVSwitch. NVL72 = ~130 TB/s aggregate, 1.8 TB/s per
  GPU. Carries TP and the heaviest EP all-to-all. Copper inside the rack; Rubin Ultra NVL576 extends
  it across 8 racks with copper + *direct optical* spine.
- **Tier 2 — scale-out (inter-rack):** **InfiniBand** (Quantum-2/X800, 400–800 Gbps NDR/XDR) or
  **Spectrum-X Ethernet** with RoCE. Typically ~400 Gbps per NIC per GPU. Carries PP, EP across nodes,
  and replica routing
  ([NVIDIA — NVLink/NVSwitch](https://developer.nvidia.com/blog/nvidia-nvlink-and-nvidia-nvswitch-supercharge-large-language-model-inference/)).
- **The move to optics between racks.** Cross-rack links are going optical: NVIDIA's **Spectrum-X
  Photonics** switch runs 1.6 Tbps/port with co-packaged silicon photonics, and 800G/1.6T pluggable
  optics are the AI-factory backbone
  ([Network World — NVIDIA networking roadmap](https://www.networkworld.com/article/4050881/nvidia-networking-roadmap-ethernet-infiniband-co-packaged-optics-will-shape-data-center-of-the-future.html),
  [ServeTheHome — CPO](https://www.servethehome.com/nvidia-co-packaged-optics-with-silcion-photonics-for-switching-and-spectrum-xgs-scale-across/)).
  **Inter-rack links are *already* light-based** — a free-space laser ISL is the same physics minus
  the glass.
- **Tier 3 — scale-across (inter-data-center):** NVIDIA shipped **Spectrum-XGS Ethernet** in 2025
  *specifically* to link data centers "in different buildings or separated by **hundreds of
  kilometers**" into one logical AI factory, with congestion control "optimized around the distance
  between communicating devices"
  ([NVIDIA — scale-across blog](https://developer.nvidia.com/blog/how-to-connect-distributed-data-centers-into-large-ai-factories-with-scale-across-networking/),
  [NVIDIA newsroom — Spectrum-XGS](https://nvidianews.nvidia.com/news/nvidia-introduces-spectrum-xgs-ethernet-to-connect-distributed-data-centers-into-giga-scale-ai-super-factories)).
  **This is the key terrestrial precedent:** the industry already accepts splitting a single training/
  inference job across racks that are *hundreds of km apart over fiber*. An orbital mesh of single-rack
  satellites is the space-borne analogue of Spectrum-XGS scale-across.

### KV-cache transfer (disaggregated prefill/decode) — a real but bounded inter-rack flow

The largest *inference* inter-rack flow is the KV-cache hand-off when prefill and decode run on
separate nodes. Sizing:

- KV cache per request ~1.3 GB for a 4 K-token prompt on an 80-layer model in FP16; for a responsive
  TTFT <500 ms with ~300 ms left for transfer, you need ~4.5 GB/s of bandwidth — and optimized
  frameworks cut KV transfer latency from ~0.94 s to ~0.05 s
  ([Jarvis Labs — disaggregated PD](https://jarvislabs.ai/blog/llm-optimization-disaggregated-prefill-decode)).
- Critically, a May 2026 arXiv study, **"Prefill-as-a-Service: KVCache could go cross-datacenter,"**
  finds that for modern *hybrid-attention* MoE models the KV-transfer burden collapses: Ring-2.5-1T
  needs only ~170 Gbps of line capacity, and a real two-cluster deployment ran on ~100 Gbps of
  commodity Ethernet (avg egress 13 Gbps) — *no RDMA fabric required*. Dense-attention models, by
  contrast, would need ~3.8 Tbps and remain infeasible cross-DC
  ([arXiv 2604.15039](https://arxiv.org/html/2604.15039v1)).

So: disaggregated KV-cache hand-off **fits inside a 100–200 Gbps laser ISL for hybrid-MoE models** —
the same architecture class as today's frontier models.

---

## 4. Optical inter-satellite links for rack-to-rack

### 4.1 Achievable ISL bandwidth

From `optical_comms.md` and cross-checked here:

- **Starlink:** ~3 optical terminals per satellite, each rated **up to ~100–200 Gbps**, >99% link
  uptime, 9,000+ lasers moving >42 PB/day
  ([Clemson — LISL in Starlink](https://people.computing.clemson.edu/~jmarty/projects/lowLatencyNetworking/papers/LEO-Sat-Broadband-Access/LaserInterSatLinksInAStarLinkConstellation.pdf),
  cross-checked with project `optical_comms.md`).
- **Mynaric CONDOR (Rocket Lab's in-house terminal):** Mk3 ships at ~2.5 Gbps today; **Mk3.1 targets
  up to 100 Gbps** (roadmap, not shipping as of May 2026 — see `optical_comms.md`).
- **Planning figure: ~100–200 Gbps per ISL terminal**, with 3–4 terminals giving ~0.3–0.8 Tbps of
  aggregate inter-node capacity. This is **the same band as one or two terrestrial scale-out NICs**
  (400 Gbps InfiniBand) — i.e. squarely in PP's comfort zone and adequate for EP and hybrid-MoE
  KV-cache transfer.

### 4.2 Latency — the vacuum advantage, quantified

This is where space *helps*. Light in single-mode fiber travels at ~204,000 km/s (refractive index
~1.4675); in vacuum it travels at 299,792 km/s. **Vacuum is ~1.47× faster — propagation in free space
is ~47% quicker than in glass, equivalently fiber adds ~31% to vacuum's travel time**
([m2optics — fiber latency](https://www.m2optics.com/blog/bid/70587/calculating-optical-fiber-latency),
[Hacker News discussion of the 31% figure](https://news.ycombinator.com/item?id=22294504),
cross-checked [Frank Rayal — LEO vs fiber latency](https://frankrayal.com/2021/07/07/latency-in-leo-satellites-vs-terrestrial-fiber/)).

One-way propagation for a close satellite formation:

| Separation | Vacuum (laser ISL) one-way | Fiber equiv. one-way | Notes |
|---|---|---|---|
| **10 km** | **~0.033 ms** (33 µs) | ~0.049 ms | Tight formation |
| **50 km** | **~0.17 ms** | ~0.24 ms | Loose formation |
| **100 km** | **~0.33 ms** | ~0.49 ms | Confirmed ~0.33 µs/km in vacuum ([arXiv ISL latency](https://arxiv.org/html/2604.15528)) |
| **300 km** | **~1.0 ms** | ~1.47 ms | Upper end of "close formation" |

Add per-hop switching/processing — cut-through switching keeps this to **microsecond scale per hop**
([arXiv — ISL config for fast delivery](https://arxiv.org/html/2511.15861v2)). Acquisition/re-acquisition
of an optical link takes ~seconds, but for a *fixed close formation* the link stays locked — this is a
one-time setup cost, not a per-packet cost (see `optical_comms.md` §3).

**The decisive comparison:** NVIDIA's Spectrum-XGS scale-across product knowingly accepts linking
racks "hundreds of km apart" *over fiber*. A laser ISL between two satellites **100 km apart has
~0.33 ms one-way latency — lower than the ~0.49 ms a 100 km fiber run would add, and far lower than
the multi-hundred-km fiber paths Spectrum-XGS already tolerates.** A rack-on-satellite-A ↔
rack-on-satellite-B laser link, for satellites in a close formation, **matches or beats a terrestrial
cross-campus / cross-metro link** on both bandwidth (100–200 Gbps, comparable to a scale-out NIC) and
latency (sub-ms, faster than equivalent fiber). The vacuum speed-of-light bonus is real and works in
the project's favor.

### 4.3 Formation-flying feasibility

Maintaining laser links between separate free-flying satellites is **proven at scale**: Starlink runs
9,000+ satellites holding laser links continuously, including demonstrated links between satellites
**5,400 km apart**; links over 1,500–1,700 km are routine
([Clemson — LISL](https://people.computing.clemson.edu/~jmarty/projects/lowLatencyNetworking/papers/LEO-Sat-Broadband-Access/LaserInterSatLinksInAStarLinkConstellation.pdf),
[connectivity.technology — LISL](https://www.connectivity.technology/2022/02/laser-inter-satellite-links-lisls-in.html)).
A *deliberately tight* formation of compute satellites (tens to a few hundred km, co-orbiting in the
same plane) is a **far easier** pointing/tracking problem than Starlink's cross-plane links, since
intra-plane geometry is stable (see `optical_comms.md`). Station-keeping a close formation costs
delta-v but is well within standard satellite-bus capability. **Formation flying is not the risk; the
ISL terminal data rate (Mk3.1 roadmap) is.**

---

## 5. The verdict — can you split a model across separate satellites?

**Yes — for the right parallelism strategies. The split survives a laser hop for PP, EP, and replica
parallelism; it does not survive for TP.**

Mapping each strategy onto a laser-meshed cluster of single-rack satellites:

- **Replica/data parallelism — fully viable, the primary axis.** Each satellite carries a complete
  rack running a complete model copy. Inter-satellite traffic is just routing metadata. This is how
  the constellation scales throughput and is *exactly* the embarrassingly-parallel pattern
  `inference_scaling.md` identified. **No performance cost.**
- **Pipeline parallelism — viable for a model too big for one rack.** Split the model's *layers*
  across 2 (or more) single-rack satellites; satellite A runs layers 1–N, satellite B runs layers
  N+1–M; only the activation tensor crosses the ISL at the stage boundary. The 100–200 Gbps ISL is
  inside PP's 100–400 Gbps comfort band. **Cost:** added time-to-first-token from the ISL hop (~0.3–1
  ms propagation for a close formation — negligible against inference SLAs measured in tens of ms),
  and pipeline-bubble inefficiency that exists on terrestrial multi-node PP too. **This is the key
  result: a 2-rack model can run as two laser-linked single-rack satellites.**
- **Expert parallelism — viable but the weakest link.** A hybrid-MoE model's experts can be spread
  across separate satellites; DeepSeek already runs 64-way EP across 8 *nodes* over 400 Gbps
  InfiniBand. Across a laser ISL it would work, but EP all-to-all is latency-sensitive (10–30% of
  decode latency) — the sub-ms ISL propagation is acceptable, but EP across a satellite link will cost
  more throughput than EP within a rack. **Prefer to keep EP within a rack; tolerate it across an ISL
  only if a model's expert count forces it.**
- **Tensor parallelism — cannot cross a satellite link. Full stop.** TB/s bandwidth, ~100
  microsecond-critical barriers per token. A 100–200 Gbps ISL is ~100–150× too slow. TP must stay on
  one rack's NVLink fabric. **But this is not a problem for the mesh thesis** — TP also cannot cross a
  *terrestrial* rack boundary, so any multi-rack model (in space or on the ground) is *already* built
  to confine TP within each rack and split *between* racks using PP/EP. The orbital mesh inherits the
  terrestrial partitioning unchanged.
- **Disaggregated prefill/decode — viable for hybrid-MoE models.** KV-cache hand-off between a
  prefill satellite and a decode satellite fits in ~100–200 Gbps for hybrid-attention models (arXiv
  2604.15039: ~170 Gbps for Ring-2.5-1T; ~100 Gbps commodity link sufficed). Latency-tolerant
  (hundreds of ms budget). Dense-attention models would not fit — a model-architecture dependency to
  flag.

**What it costs in performance:** Splitting a model across satellites instead of co-locating racks
costs (a) the ISL propagation hop — sub-millisecond for a close formation, negligible vs. tens-of-ms
inference SLAs; (b) pipeline-bubble / all-to-all overhead that *also* exists in any terrestrial
multi-rack deployment; (c) a hard constraint that the model's TP groups each fit inside one rack —
which they must anyway. There is **no unique-to-space penalty** beyond the ISL hop, and that hop is
*smaller* than the equivalent terrestrial fiber run. The performance cost is the same modest
multi-node-inference tax data centers already pay — and NVIDIA productized that tax as Spectrum-XGS.

**Formation-flying feasibility:** proven (Starlink). A tight, co-planar compute formation is an easier
case than Starlink's operational cross-plane links.

---

## 6. Implication for the thesis

**The "2 racks per launch" mass problem dissolves — with strong confidence for the common cases.**

`node_mass_model.md` and the fairing-packing simulation found a Neutron node carries **one rack**, and
that a 2-rack node would need a block-upgraded Neutron and remains mass-tight. This document shows that
**constraint is not binding**, because:

1. **You never need to put 2 racks on one satellite.** A model too big for one rack is split by
   *pipeline* (and/or expert) parallelism across **two separate single-rack satellites** linked by a
   laser ISL. Each satellite remains the always-feasible single-rack node the mass model already
   validated.
2. **The orbital mesh is the space-borne version of a pattern NVIDIA already ships.** Spectrum-XGS
   "scale-across" links racks hundreds of km apart over fiber as one logical AI factory. A laser-meshed
   constellation does the same thing — and the vacuum speed-of-light bonus makes the inter-node link
   *faster* than the terrestrial fiber equivalent.
3. **Scaling stays on the embarrassingly-parallel axis.** Most capacity growth is replica parallelism
   — independent single-rack satellites — which needs almost no inter-node bandwidth and is the
   constellation's natural growth mode anyway.

**How strong is this conclusion?**

- **Strong** for pipeline parallelism and replica parallelism: these are well-understood, run across
  100–400 Gbps links terrestrially every day, and the laser ISL comfortably meets their needs. A model
  needing 2 racks can be flown as two laser-linked single-rack satellites with high confidence.
- **Moderate** for expert parallelism and disaggregated prefill/decode: they work, but EP all-to-all
  is latency-sensitive and the KV-cache result depends on the model being hybrid-attention MoE (which
  current frontier models are). If a future model reverted to dense attention or had pathologically
  high expert-routing traffic, EP-across-ISL would degrade.
- **The one firm "cannot":** tensor parallelism never crosses the ISL. This is not a weakness of the
  space approach — it is a universal constraint that terrestrial multi-rack inference obeys too. As
  long as each model's TP group fits within one NVL72-class rack (it does today, and Rubin Ultra
  NVL576 shows NVIDIA scaling the *in-rack-equivalent* NVLink domain to absorb bigger TP groups), the
  mesh works.

**Bottom line:** The project can commit to **always flying single-rack nodes** and **never needs a
2-rack Neutron node.** If and when a frontier model outgrows one rack, mesh two (or more) single-rack
satellites with laser ISLs and partition the model by pipeline/expert parallelism. The thesis is not
just preserved — it is *strengthened*: the mesh architecture turns the "one rack per launch" mass
limit from a ceiling into a non-issue.

---

## Sources

Parallelism types & interconnect demands:
- [premai — Multi-GPU LLM Inference: TP vs PP vs EP (2026)](https://blog.premai.io/multi-gpu-llm-inference-tp-vs-pp-vs-ep-parallelism-guide-2026/)
- [BentoML — data/tensor/pipeline/expert parallelism](https://bentoml.com/llm/inference-optimization/data-tensor-pipeline-expert-hybrid-parallelism)
- [vLLM — Parallelism and Scaling](https://docs.vllm.ai/en/stable/serving/parallelism_scaling/)
- [NVIDIA — NVLink and NVSwitch Supercharge LLM Inference](https://developer.nvidia.com/blog/nvidia-nvlink-and-nvidia-nvswitch-supercharge-large-language-model-inference/)
- [Nebius — rack-scale GPU interconnect with GB200 NVL72](https://nebius.com/blog/posts/leveraging-nvidia-gb200-nvl72-gpu-interconnect)
- [Introl — NVLink and scale-up networking](https://introl.com/blog/nvlink-scale-up-networking-gpu-interconnect-infrastructure-2025)
- [NVIDIA — NVLink (official)](https://www.nvidia.com/en-us/data-center/nvlink/)
- [LMSYS — Chunked Pipeline Parallelism in SGLang](https://www.lmsys.org/blog/2026-01-15-chunked-pipeline/)
- [NVIDIA — Wide Expert Parallelism on NVL72](https://developer.nvidia.com/blog/scaling-large-moe-models-with-wide-expert-parallelism-on-nvl72-rack-scale-systems/)
- [Meta Engineering — Scaling LLM Inference (TP/CP/EP)](https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/)
- [DeepSeek — DeepEP expert-parallel communication library](https://github.com/deepseek-ai/DeepEP)
- [DeepSeek-V3 Technical Report](https://arxiv.org/pdf/2412.19437)

Terrestrial inter-rack & scale-across networking:
- [NVIDIA — How to Connect Distributed Data Centers with Scale-Across Networking](https://developer.nvidia.com/blog/how-to-connect-distributed-data-centers-into-large-ai-factories-with-scale-across-networking/)
- [NVIDIA newsroom — Spectrum-XGS Ethernet](https://nvidianews.nvidia.com/news/nvidia-introduces-spectrum-xgs-ethernet-to-connect-distributed-data-centers-into-giga-scale-ai-super-factories)
- [Network World — NVIDIA networking roadmap (co-packaged optics)](https://www.networkworld.com/article/4050881/nvidia-networking-roadmap-ethernet-infiniband-co-packaged-optics-will-shape-data-center-of-the-future.html)
- [ServeTheHome — NVIDIA Co-Packaged Optics & Spectrum-XGS scale-across](https://www.servethehome.com/nvidia-co-packaged-optics-with-silcion-photonics-for-switching-and-spectrum-xgs-scale-across/)

Hardware — Vera Rubin / NVL576:
- [NVIDIA — Vera Rubin NVL72 (official)](https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/)
- [NVIDIA newsroom — Vera Rubin platform](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform)
- [NVIDIA — Vera Rubin POD (NVL576)](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/)
- [Tom's Hardware — Vera Rubin platform in depth](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date)

Disaggregated prefill/decode & KV-cache transfer:
- [Jarvis Labs — Disaggregated Prefill-Decode](https://jarvislabs.ai/blog/llm-optimization-disaggregated-prefill-decode)
- [arXiv 2604.15039 — Prefill-as-a-Service: KVCache could go cross-datacenter](https://arxiv.org/html/2604.15039v1)

Fiber-vs-vacuum latency & inter-satellite links:
- [m2optics — Calculating Optical Fiber Latency](https://www.m2optics.com/blog/bid/70587/calculating-optical-fiber-latency)
- [Hacker News — light 31% slower in fiber discussion](https://news.ycombinator.com/item?id=22294504)
- [Frank Rayal — Latency in LEO Satellites vs Terrestrial Fiber](https://frankrayal.com/2021/07/07/latency-in-leo-satellites-vs-terrestrial-fiber/)
- [arXiv 2604.15528 — Inter-Satellite Link Optimization for Low-Latency Global Networking](https://arxiv.org/html/2604.15528)
- [arXiv 2511.15861 — Inter-Satellite Link Configuration for Fast Delivery in LEO](https://arxiv.org/html/2511.15861v2)
- [Clemson — Laser Inter-Satellite Links in a Starlink Constellation](https://people.computing.clemson.edu/~jmarty/projects/lowLatencyNetworking/papers/LEO-Sat-Broadband-Access/LaserInterSatLinksInAStarLinkConstellation.pdf)
- [connectivity.technology — LISLs in a Starlink Constellation](https://www.connectivity.technology/2022/02/laser-inter-satellite-links-lisls-in.html)

(See also project docs: `llm_compute/inference_scaling.md`, `laser_comms/optical_comms.md`,
`node_design/node_mass_model.md`.)

---

## Open questions / uncertainties

1. **EP all-to-all across a laser ISL is the weakest verdict.** EP works cross-node terrestrially, but
   decode-phase all-to-all is latency-sensitive (10–30% of decode latency). A close-formation ISL adds
   sub-ms propagation, which *should* be tolerable — but a model-specific simulation of EP throughput
   degradation across a 100–200 Gbps / sub-ms ISL is not yet done. Needed before committing to
   EP-split models.
2. **The 100 Gbps ISL terminal is roadmap, not shipping.** The whole "split a model across satellites"
   case assumes ~100–200 Gbps per terminal. Mynaric's shipping CONDOR Mk3 is ~2.5 Gbps; Mk3.1 (100
   Gbps) is unproven as of May 2026 (see `optical_comms.md`). At 2.5 Gbps, cross-satellite PP would be
   marginal and EP infeasible. **This is the gating dependency.**
3. **Hybrid-attention assumption for KV-cache transfer.** The cross-DC KV-cache result holds for
   hybrid-attention MoE models (~170 Gbps) but *not* dense-attention models (~3.8 Tbps). If a future
   frontier model used dense attention, disaggregated prefill/decode across satellites would break.
   Current frontier models are MoE/hybrid, so this is a low but non-zero risk.
4. **How many racks does the next frontier model actually need?** This document assumes the 2+-rack
   regime arrives with multi-trillion (>~10–15 T) MoE models. Closed-model parameter counts are
   non-public (per `inference_scaling.md` open question #1). If frontier models plateau at 1–2 T, the
   whole multi-rack question is moot and single-rack nodes suffice with no meshing at all — which only
   *strengthens* the thesis.
5. **Formation-flying delta-v and collision risk.** A tight compute formation is an easier pointing
   problem than Starlink cross-plane links, but station-keeping delta-v budget, collision-avoidance,
   and the consequences of a formation-member failure for a PP-split model (one satellite down = the
   whole pipelined model down, unlike independent replicas) need a dedicated reliability/orbital pass.
   Cross-reference `node_design/reliability_failure_handling.md`.
6. **Pipeline-bubble efficiency at constellation scale.** PP across 2 satellites is well-understood;
   PP across many satellites introduces pipeline bubbles and scheduling complexity. The practical
   ceiling on how many single-rack satellites can usefully pipeline one model is not pinned down.
