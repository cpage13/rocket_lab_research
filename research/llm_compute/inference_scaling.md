# LLM Inference Scaling — Sizing an Orbital AI-Inference Node

*Research compiled May 2026. Purpose: determine how much NVIDIA hardware an orbital node must carry to usefully serve large language models, and confirm whether inference (vs training) is the right workload for space.*

---

## Summary (read this first)

- **Model size in "terabytes":** A frontier model today is roughly **1–2 trillion total parameters** (DeepSeek V4 ~1.6T, Llama 4 Behemoth ~2T, Gemini 3 estimated 1T+). At **FP8 = 1 byte/parameter**, a 1T model is **~1 TB of weights**; at **FP4 = 0.5 byte/parameter**, **~0.5 TB**. A 2T model at FP8 is **~2 TB**. So "a terabyte of model" ≈ a 1T-parameter model in FP8. This is the user's intuition translated correctly.
- **Racks to serve one frontier model:** One **NVL72-class rack = 72 Blackwell GPUs**. GB200 NVL72 has **~13.5 TB HBM**; GB300 NVL72 has **~20 TB HBM**. A 1–2T model in FP8 (1–2 TB of weights) plus KV cache fits **comfortably inside a single rack** — the rack is sized for it. The minimum viable orbital inference node is therefore **one NVL72-class rack**. Two-to-four racks raise throughput and redundancy; you do not *need* multiple racks to hold one model.
- **Inference vs training communication:** This is the crux of the space thesis and it **holds up**. Training requires constant, bandwidth-hungry all-reduce of gradients across the *entire* cluster every step (gigabytes per step, thousands of GPUs in lockstep). Inference moves far less data between nodes — mostly small activation tensors and KV-cache hand-offs. Inference's heavy communication (MoE all-to-all, tensor-parallel reductions) is concentrated **inside the rack's NVLink domain**, not across racks. Cross-rack ("scale-out") inference traffic runs over **~400 Gbps/GPU InfiniBand/Ethernet** and is modest. Inference also tolerates **tens of milliseconds of added latency**; training does not.
- **Confidence:** High on hardware specs and the inference-vs-training distinction (multiple official + independent sources). Medium on exact frontier-model parameter counts (closed-model internals are not public — flagged throughout).

---

## 1. Model sizes — what is "a terabyte of model"?

### Parameter counts of 2026 frontier models

Modern frontier models are almost all **Mixture-of-Experts (MoE)**: they have a large *total* parameter count but only activate a fraction per token.

| Model | Total params | Active params/token | Notes |
|---|---|---|---|
| DeepSeek V4 | ~1–1.6 T | ~32 B active | Open weights; figures published |
| Llama 4 Behemoth | ~2 T | ~288 B active (16 experts) | Meta-published |
| Gemini 3 | ≥1 T (estimated, some guess ~7 T) | non-public | Google does not publish |
| GPT-5.x / Claude Opus 4.7 | **non-public** | non-public | No official parameter count |

**Estimate vs official:** Open models (DeepSeek, Llama) publish real numbers. Closed models (GPT-5.x, Gemini 3, Claude Opus 4.7) do **not** — vendors deliberately omit parameter counts from model cards. The "~1–2 T total" band is the defensible planning range; treat anything above as speculation ([MIT Technology Review](https://www.technologyreview.com/2026/01/07/1130795/what-even-is-a-parameter/), [codingscape](https://codingscape.com/blog/most-powerful-llms-large-language-models), [explainx.ai](https://explainx.ai/blog/llm-model-parameters-billions-explained)).

### Translating parameters to bytes (weight memory footprint)

Memory for weights = (parameter count) × (bytes per parameter). Bytes per parameter is set by the numeric precision used for inference:

| Precision | Bytes/param | 1 T model | 2 T model |
|---|---|---|---|
| FP16 / BF16 | 2 | ~2 TB | ~4 TB |
| **FP8** (E4M3, standard for 2026 inference) | **1** | **~1 TB** | **~2 TB** |
| **FP4 / NVFP4** | **0.5** | **~0.5 TB** | **~1 TB** |

Reference point: a 7 B model is ~14 GB at FP16, ~7 GB at FP8, ~3.5 GB at FP4 ([VRLA Tech](https://vrlatech.com/llm-quantization-explained-int4-int8-fp8-awq-and-gptq-in-2026/), [NVIDIA quantization blog](https://developer.nvidia.com/blog/model-quantization-concepts-methods-and-why-it-matters/)). This scales linearly.

**So: "a terabyte of model" ≈ a 1-trillion-parameter model served in FP8.** A 2 T model in FP8 is ~2 TB; in FP4 a 2 T model drops to ~1 TB. FP8 is the production default on NVIDIA Blackwell/Hopper (native tensor-core support); FP4 is increasingly used for inference to cut memory further, with careful calibration.

### KV cache — the *second* memory consumer

Holding the weights is not enough. Each in-flight request needs a **KV cache** that grows linearly with context length and number of concurrent users:

- Llama 3.1 70B uses **~0.31 MB per token** of KV cache at BF16 — i.e. ~310 MB per 1,000 tokens of context.
- A single 70B request at **128 K context ≈ 40–42 GB** of KV cache — *larger than the model's INT4 weights*.
- 32 concurrent 8 K-token requests on a 70B model exceed **80 GB** of KV cache ([Spheron](https://www.spheron.network/blog/kv-cache-optimization-guide/), [Lyceum Technology](https://lyceum.technology/magazine/kv-cache-memory-calculation-llm/), [Introl](https://introl.com/blog/kv-cache-optimization-memory-efficiency-production-llms-guide)).

For a frontier MoE model the per-token KV cost is smaller relative to its weights, but **at scale the KV cache can rival or exceed the weights**. Practical sizing rule: budget **weights + a comparable allowance for KV cache** when sizing HBM. A rack holding a ~1–2 TB model should reserve several more TB of HBM for KV cache and runtime buffers — which is exactly why NVL72-class racks ship with 13.5–20 TB.

---

## 2. How many GPUs / racks to *serve* one frontier model

### The rack as the unit

| System | GPUs | HBM/GPU | Total HBM/rack | FP4 compute | Power |
|---|---|---|---|---|---|
| **GB200 NVL72** | 72 Blackwell | 192 GB | **~13.5 TB** | ~1.4 EFLOPS | ~120–132 kW |
| **GB300 NVL72** | 72 Blackwell Ultra | 288 GB | **~20 TB** | ~1.1+ EFLOPS FP4 | **~135 kW TDP / ~155 kW peak** |

*(GB300 power updated 2026-05-17 to the web-confirmed ~135 kW TDP / ~155 kW peak — see `data_centers/ai_hardware.md` §1.1; the earlier "~120 kW" was the NVIDIA marketing figure the project agreed not to use. Not load-bearing for this doc's memory/communication argument.)*

Sources: [NVIDIA GB200 NVL72](https://www.nvidia.com/en-us/data-center/gb200-nvl72/), [NVIDIA GB300 NVL72](https://www.nvidia.com/en-us/data-center/gb300-nvl72/), [Spheron GB200 guide](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/), [Introl GB300](https://introl.com/blog/why-nvidia-gb300-nvl72-blackwell-ultra-matters).

### Does a frontier model fit in one rack?

**Yes — with room to spare.** A 1–2 T model in FP8 is 1–2 TB of weights. A single NVL72 rack offers 13.5–20 TB of HBM. Even after reserving HBM for KV cache and buffers, **one rack holds and serves a current frontier model**. NVIDIA explicitly markets the NVL72 for "production inference on 671B-scale reasoning models like DeepSeek R1 that must fit entirely in GPU memory across a single rack" ([Spheron](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/)).

Contrast — older hardware needed multiple nodes for the *same* model: DeepSeek-R1 671B in FP8 (~700–750 GB of weights) does **not** fit in one 8×H100 node (640 GB total), so on Hopper it requires **at least 2 nodes (16 GPUs)** just to hold weights ([Baseten](https://www.baseten.co/blog/how-multi-node-inference-works-llms-deepseek-r1/), [RiseUnion](https://www.theriseunion.com/en/blog/DeepSeek-V3-R1-671B-GPU-Requirements.html)). The NVL72 rack-scale design is precisely what collapses that into one rack.

### The three parallelism strategies (how a model is split across GPUs)

A model too big for one GPU is split using a mix of:

- **Tensor parallelism (TP):** each layer's matrices are sliced across GPUs; all GPUs work on every token in parallel. **Communication-heavy** (AllReduce/AllGather every layer) → must stay on the fast NVLink fabric inside a rack.
- **Pipeline parallelism (PP):** consecutive layers are assigned to different GPUs/nodes, like an assembly line. **Communication-light** (only activations pass between stages) → tolerates slower links, works across racks.
- **Expert parallelism (EP):** for MoE models, the experts are spread across GPUs; each token is routed to its few active experts. Needs **all-to-all** communication to route tokens. NVIDIA's "Wide-EP" on NVL72 leans on the rack's **~130 TB/s coherent NVLink domain** to absorb that all-to-all cost ([NVIDIA Wide-EP blog](https://developer.nvidia.com/blog/scaling-large-moe-models-with-wide-expert-parallelism-on-nvl72-rack-scale-systems/), [BentoML parallelism guide](https://bentoml.com/llm/inference-optimization/data-tensor-pipeline-expert-hybrid-parallelism)).

**Key point for space:** The communication-intensive strategies (TP, EP all-to-all) are deliberately confined **inside a rack's NVLink domain**. The NVL72 exists so that all 72 GPUs behave as one big GPU for these chatty operations. Cross-rack splitting uses the *communication-light* methods (PP, data-parallel replicas).

---

## 3. Inter-rack communication during inference

### Two communication tiers

1. **Scale-up (intra-rack):** NVLink. Inside an NVL72, all 72 GPUs share a non-blocking NVLink fabric (~130 TB/s aggregate; per-GPU NVLink bandwidth on the order of ~0.9–1.8 TB/s). This is where TP reductions and MoE all-to-all live.
2. **Scale-out (inter-rack):** InfiniBand or RoCE Ethernet, typically **~400 Gbps (one NIC) per GPU** for compute traffic, sometimes a second 400 Gbps NIC for storage/KV traffic ([Baseten](https://www.baseten.co/blog/how-multi-node-inference-works-llms-deepseek-r1/), [arXiv 2511.09557](https://arxiv.org/pdf/2511.09557)). NVLink is roughly **an order of magnitude or more** faster than per-GPU InfiniBand.

### How much do racks actually need to talk during inference?

**Not much, if the model fits in one rack.** When a single rack serves the whole model, the only inter-rack traffic is:

- **Load balancing / request routing** between rack-replicas — tiny (request metadata).
- **KV-cache hand-off** in *disaggregated prefill/decode* setups — see below. This is the largest inter-rack inference flow, and it is bursty, not continuous.

NVIDIA's **Dynamo** framework splits inference into a **prefill** stage (compute-bound, processes the prompt) and a **decode** stage (memory-bound, generates tokens). When these run on separate nodes, the KV cache must transfer prefill→decode. This is real inter-node traffic, but it is a **one-time per-request transfer** of a bounded tensor, not a per-step all-reduce. NVIDIA's NIXL library moves KV caches "at wire speed" precisely so this hand-off does not stall decode ([NVIDIA Dynamo blog](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/), [BentoML prefill/decode](https://bentoml.com/llm/inference-optimization/prefill-decode-disaggregation), [Spheron NIXL](https://www.spheron.network/blog/nvidia-nixl-disaggregated-inference-guide/)).

### Inference vs training communication — the hard contrast

| | **Training** | **Inference** |
|---|---|---|
| Passes computed | Forward + backward | Forward only |
| Inter-node traffic | **Gradient all-reduce every step** — gigabytes per step, whole cluster in lockstep | Small activations, occasional KV-cache hand-off |
| Synchronization | Tight, global, every step | Loose; replicas independent |
| Dominant bottleneck | Network bandwidth + sync | **GPU HBM bandwidth** (the network is *not* the bottleneck) |
| Latency tolerance | Low — stragglers stall everyone | High — tens of ms tolerable |

Industry consensus is explicit: "Inference demands fewer computational resources than training... Much less data passes along GPU-to-GPU and node-to-node interconnects... VRAM remains the bottleneck" ([apxml interconnects](https://apxml.com/courses/how-to-build-a-large-language-model/chapter-18-hardware-considerations-llm-training/interconnect-technologies-nvlink-infiniband), [runpod](https://www.runpod.io/articles/guides/infiniband-for-distributed-ai-training)). Training, by contrast, requires "high-performance RDMA networking to... perform all-to-all model weight data reduction operations" continuously ([650 Group](https://650group.com/blog/interconnect-needs-for-llm-inference-to-drive-networking-bandwidth/)).

**Caveat:** Inference is *not* communication-free. MoE all-to-all and TP reductions are genuinely demanding — but they are designed to live **inside the rack** on NVLink. The point is not "inference has no chatter" but "inference's chatter is contained within a rack; only training forces continuous high-bandwidth traffic *across* the whole cluster."

---

## 4. Why inference suits space — confirm or challenge

**The thesis holds, with one honest caveat.**

Confirmed:
- **Less inter-node bandwidth needed.** Inference moves far less data between racks than training (no gradient all-reduce). A space node serving a self-contained model needs only modest inter-rack links.
- **More parallelizable / "embarrassingly parallel."** Inference scales by adding independent replicas; each replica serves requests on its own. There is no global synchronization barrier, so a straggler rack (or a rack temporarily out of ground contact) does not stall the others. Multiple analyses call orbital data centers "better suited for embarrassingly parallel inference" ([Space Investments](https://www.spaceinvestments.io/information-communications/orbital-data-centers-technical-validation-and-strategic-positioning-in-the-2025-2030-transition-period), [Frank Rayal](https://frankrayal.com/2026/04/27/orbital-data-centers-latency/)).
- **Latency-tolerant.** Inference workloads (chat, recommendations, batch processing) tolerate the **tens of ms** added by a LEO round-trip; cited tolerances are ~45–80 ms. Training cannot absorb orbital bandwidth constraints without congestion and tail-latency blowups ([IEEE Spectrum](https://spectrum.ieee.org/orbital-inference-data-center), [Frank Rayal](https://frankrayal.com/2026/04/27/orbital-data-centers-latency/)).
- **Architectural consensus already favors this split:** "terrestrial training in hyperscale data centers... orbital inference at edge nodes" ([Space Investments](https://www.spaceinvestments.io/information-communications/orbital-data-centers-technical-validation-and-strategic-positioning-in-the-2025-2030-transition-period)). NVIDIA itself has announced space-computing initiatives.

Challenge / caveat:
- Within a node, inference is still **HBM-bandwidth-bound and intra-rack-communication-heavy** (MoE all-to-all). That is fine — it is *self-contained* on NVLink inside the rack, which is exactly what makes a single rack a viable independent orbital unit. But it means the orbital node still needs a full rack-scale NVLink fabric; you cannot scatter a model across loosely-connected small satellites.
- The real risk for space is **not** communication — it is **power, cooling (~120 kW/rack, liquid-cooled), and radiation tolerance** of commercial GPUs. Those, not interconnect, are the gating constraints (out of scope here; flagged for the thermal/power workstreams).

**Verdict:** Inference is the correct workload for an orbital data center. The communication argument is sound *provided each orbital node carries a complete rack* so its intensive traffic stays on internal NVLink.

---

## 5. Sizing a serving cluster — throughput scaling and minimum viable node

### How throughput scales

For a fixed model, **system throughput (tokens/sec, concurrent users) scales roughly linearly with added GPUs/racks** — until a saturation point. Adding replicas (more racks each running a copy of the model) raises aggregate tokens/sec and requests/sec and sustains per-user token rate under load ([Anyscale](https://docs.anyscale.com/llm/serving/benchmarking/metrics), [BentoML metrics](https://bentoml.com/llm/inference-optimization/llm-inference-metrics)).

Two scaling levers:
- **More racks = more replicas** → more concurrent users, near-linear, no extra inter-rack chatter (replicas are independent). **This is the space-friendly axis.**
- **Within a rack:** batch more requests → higher total throughput but higher per-token latency (throughput/latency trade-off). Disaggregated prefill/decode (Dynamo) reported up to **~30× more requests served** vs naive single-node serving of DeepSeek-R1 on Blackwell ([NVIDIA Dynamo blog](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/)).

### Minimum viable unit of inference capacity

**One NVL72-class rack (72 GPUs).** Justification:
- It holds a full 1–2 T frontier model in FP8/FP4 with HBM left for KV cache.
- Its NVLink domain contains all the communication-intensive parallelism (TP, EP), so it is **self-sufficient** — it does not depend on a fast link to any other rack.
- It can serve real concurrent traffic on its own.

A sub-rack node (a handful of GPUs) is **not** viable for a frontier model — it cannot hold the weights, and splitting one model across many small loosely-linked satellites reintroduces exactly the cross-node communication problem we are trying to avoid.

Sensible orbital build-out: start with **1 rack = 1 minimum viable node**; grow capacity by adding **independent rack-replicas** (2, 4, ...), each a self-contained unit. This scales throughput near-linearly and adds fault tolerance, with only light inter-rack routing traffic.

---

## Implications for an orbital node

1. **Minimum viable orbital node = one NVL72-class rack (72 Blackwell/Blackwell-Ultra GPUs, 13.5–20 TB HBM, ~120 kW).** This is the smallest unit that can independently serve a frontier model.
2. **One rack holds a current frontier model.** A 1–2 T-parameter model in FP8 is 1–2 TB of weights; the rack's 13.5–20 TB HBM covers weights plus KV cache. No multi-rack requirement to *hold* the model.
3. **Design the node around the rack's internal NVLink fabric.** All bandwidth-intensive inference communication (tensor-parallel reductions, MoE all-to-all) must stay on-rack. Inter-satellite/inter-rack links only carry request routing and occasional KV-cache hand-offs — modest (~400 Gbps-class), latency-tolerant.
4. **Scale by adding independent rack-replicas, not by splitting a model across satellites.** Throughput grows near-linearly with racks; replicas need almost no inter-rack bandwidth. This is the embarrassingly-parallel property that makes space viable.
5. **The space thesis (inference not training) is confirmed.** Training's continuous cluster-wide gradient all-reduce and zero latency tolerance make it a poor fit for orbit; inference's contained communication and tens-of-ms latency tolerance make it a good fit.
6. **Real gating constraints are power, cooling, and radiation — not networking.** ~120 kW/rack liquid-cooled. Hand off to the thermal/power and radiation workstreams.
7. **Plan in FP8 as baseline, FP4 as upside.** FP4 halves the weight footprint, leaving even more HBM for KV cache / larger batches — directly increasing users-served per rack.

---

## Sources

Hardware specs:
- [NVIDIA GB200 NVL72 (official)](https://www.nvidia.com/en-us/data-center/gb200-nvl72/)
- [NVIDIA GB300 NVL72 (official)](https://www.nvidia.com/en-us/data-center/gb300-nvl72/)
- [Spheron — GB200 NVL72 guide](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/)
- [Introl — GB300 NVL72 / Blackwell Ultra](https://introl.com/blog/why-nvidia-gb300-nvl72-blackwell-ultra-matters)
- [server-parts.eu — Blackwell Ultra B300 specs](https://www.server-parts.eu/post/nvidia-b300-gpu-blackwell-ultra-architecture)

Model sizes & quantization:
- [MIT Technology Review — what is a parameter](https://www.technologyreview.com/2026/01/07/1130795/what-even-is-a-parameter/)
- [codingscape — most powerful LLMs 2026](https://codingscape.com/blog/most-powerful-llms-large-language-models)
- [explainx.ai — LLM parameters, MoE, 2026 model cards](https://explainx.ai/blog/llm-model-parameters-billions-explained)
- [VRLA Tech — INT4/INT8/FP8/FP4 quantization 2026](https://vrlatech.com/llm-quantization-explained-int4-int8-fp8-awq-and-gptq-in-2026/)
- [NVIDIA — model quantization concepts](https://developer.nvidia.com/blog/model-quantization-concepts-methods-and-why-it-matters/)

KV cache:
- [Spheron — KV cache optimization guide](https://www.spheron.network/blog/kv-cache-optimization-guide/)
- [Lyceum Technology — KV cache memory calculation](https://lyceum.technology/magazine/kv-cache-memory-calculation-llm/)
- [Introl — KV cache optimization](https://introl.com/blog/kv-cache-optimization-memory-efficiency-production-llms-guide)

Parallelism & multi-node inference:
- [BentoML — data/tensor/pipeline/expert parallelism](https://bentoml.com/llm/inference-optimization/data-tensor-pipeline-expert-hybrid-parallelism)
- [NVIDIA — Wide Expert Parallelism on NVL72](https://developer.nvidia.com/blog/scaling-large-moe-models-with-wide-expert-parallelism-on-nvl72-rack-scale-systems/)
- [Baseten — multi-node inference for DeepSeek-R1](https://www.baseten.co/blog/how-multi-node-inference-works-llms-deepseek-r1/)
- [RiseUnion — DeepSeek-V3/R1 671B GPU requirements](https://www.theriseunion.com/en/blog/DeepSeek-V3-R1-671B-GPU-Requirements.html)
- [arXiv 2511.09557 — LLM inference beyond a single node](https://arxiv.org/pdf/2511.09557)

Communication, training vs inference:
- [apxml — interconnect technologies (NVLink/InfiniBand)](https://apxml.com/courses/how-to-build-a-large-language-model/chapter-18-hardware-considerations-llm-training/interconnect-technologies-nvlink-infiniband)
- [runpod — do I need InfiniBand for distributed training](https://www.runpod.io/articles/guides/infiniband-for-distributed-ai-training)
- [650 Group — interconnect needs for LLM inference](https://650group.com/blog/interconnect-needs-for-llm-inference-to-drive-networking-bandwidth/)

Disaggregated serving & throughput:
- [NVIDIA Dynamo — low-latency distributed inference](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/)
- [BentoML — prefill/decode disaggregation](https://bentoml.com/llm/inference-optimization/prefill-decode-disaggregation)
- [Spheron — NVIDIA NIXL disaggregated inference](https://www.spheron.network/blog/nvidia-nixl-disaggregated-inference-guide/)
- [Anyscale — LLM latency and throughput metrics](https://docs.anyscale.com/llm/serving/benchmarking/metrics)
- [BentoML — key metrics for LLM inference](https://bentoml.com/llm/inference-optimization/llm-inference-metrics)

Space / orbital data centers:
- [IEEE Spectrum — orbital inference data center](https://spectrum.ieee.org/orbital-inference-data-center)
- [Frank Rayal — orbital data centers & latency](https://frankrayal.com/2026/04/27/orbital-data-centers-latency/)
- [Space Investments — orbital data centers technical analysis](https://www.spaceinvestments.io/information-communications/orbital-data-centers-technical-validation-and-strategic-positioning-in-the-2025-2030-transition-period)

---

## Open questions / uncertainties

1. **Exact frontier-model parameter counts are non-public.** GPT-5.x, Gemini 3, Claude Opus 4.7 do not publish parameter counts. The "1–2 T total" planning band is based on open models + estimates. If a future frontier model is genuinely 5–10 T params, FP8 weights would be 5–10 TB — still inside one GB300 rack's 20 TB, but with much less KV-cache headroom. Worth re-checking before final sizing.
2. **KV-cache sizing for MoE frontier models is approximate.** Public per-token KV figures are mostly for dense Llama models. MoE models and architectures with grouped-query / multi-head-latent attention change the per-token cost substantially. A model-specific calculation is needed once a target model is chosen.
3. **Realistic tokens/sec per rack** for a frontier model in orbit is not pinned down here — depends on batch size, context length, and the latency SLA. Needs a dedicated throughput-modeling pass (e.g. using InferenceMAX-style benchmark data).
4. **Disaggregated prefill/decode across racks** would create real inter-rack KV-cache traffic. If an orbital node uses disaggregation across *separate satellites*, the KV-transfer bandwidth and latency budget must be modeled explicitly — this is the one inference pattern that meaningfully stresses inter-rack links.
5. **Power and cooling (~120 kW/rack, liquid)** and **radiation tolerance** of commercial Blackwell GPUs are the true feasibility gates and are out of scope here — flagged for the thermal/power and radiation workstreams.
6. **Per-GPU NVLink and InfiniBand bandwidth figures** vary by source and generation; values here are order-of-magnitude. Confirm against final chosen hardware (GB200 vs GB300 vs successor).
