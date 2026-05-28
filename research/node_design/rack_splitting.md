# Why Is "A Rack" A Rack — And Can It Be Split For Inference?

*Project: RKLB Space Data Center — feasibility phase. Document date: May 2026.*
*Author: research agent. Hard numbers cross-checked against ≥2 sources where possible; estimates explicitly labeled and reasoned transparently.*

---

## Purpose & relationship to existing project docs

Every prior project document treats the orbital compute node as carrying **one or two intact NVL72-class racks** — `node_mass_model.md` sizes the satellite around a ~1.36 t (terrestrial) / ~1.5–1.74 t (space-modified) rack; `rack_internals.md` opens that rack up component-by-component; `inference_scaling.md` concludes "one NVL72-class rack = the minimum viable orbital inference node"; `multi_rack_inference.md` shows a model too big for one rack can be split *across separate laser-linked single-rack satellites*.

This doc challenges the **node = one intact NVIDIA rack** assumption itself. It asks: *why is a rack a rack* — what physically and architecturally makes 72 GPUs into one indivisible unit — and whether an orbital operator should instead **buy GPUs and integrate its own inference-optimized node** at a GPU count of its own choosing. It does **not** re-derive rack mass (see `rack_internals.md` / `node_mass_model.md`), the optical-interconnect mass lever (`rack_internals.md` §4), or cross-satellite model splitting (`multi_rack_inference.md`) — it builds on all three.

The distinction from `multi_rack_inference.md` matters and is worth stating up front. That doc asked: *given* intact racks, can a model span two of them on separate satellites? This doc asks the prior question: *must the node be an intact rack at all, or can it be a smaller, self-integrated N-GPU unit?* The two are complementary — one splits *across* racks, this one asks whether to split *within* one.

---

## Summary

**The question:** An NVL72 rack is sold and deployed as one indivisible 72-GPU unit. Is that a law of physics, or a packaging convention optimized for ground data centers? Could Rocket Lab buy GPUs and build a smaller, lighter, inference-tuned node — and would a lighter node ease the project's "flyability wall"?

**Headline findings:**

- **A rack is a rack because of the NVLink scale-up fabric, not because of physics that forbids splitting.** The NVL72's defining feature is a non-blocking, all-to-all **NVLink 5 fabric** — **1.8 TB/s per GPU, ~130 TB/s aggregate**, ~14× PCIe — wired through 9 central NVLink-switch trays and a passive copper spine, making 72 GPUs behave as "one big GPU" ([NVIDIA NVLink](https://www.nvidia.com/en-us/data-center/nvlink/), [NVIDIA GB200 NVL72 blog](https://developer.nvidia.com/blog/nvidia-gb200-nvl72-delivers-trillion-parameter-llm-training-and-real-time-inference/)). NVIDIA explicitly elevated **the rack to "the unit of compute"** — but that is a *commercial and integration* decision ("Nvidia is defining what gets bought and deployed as a single system"), layered on a real *physical* fact: copper NVLink reaches only **~1–2 m**, so the fabric *must* be physically compact ([HPCwire/NVIDIA](https://www.hpcwire.com/off-the-wire/nvidia-running-ai-workloads-on-rack-scale-supercomputers/), and `rack_internals.md` §4).
- **The tight in-rack fabric is justified primarily by TRAINING and by long-context PREFILL — not by steady-state decode inference.** NVIDIA's own headline figures: going from an 8-GPU system to the 72-GPU NVLink domain yields **~4× faster training** but a much larger **~30× faster inference** for GPT-MoE-1.8T ([NVIDIA blog](https://developer.nvidia.com/blog/nvidia-gb200-nvl72-delivers-trillion-parameter-llm-training-and-real-time-inference/), [Arc Compute](https://www.arccompute.io/arc-blog/the-difference-between-nvidia-hgx-b200-hgx-b300-and-gb300-nvl72-which-nvidia-platform-is-right-for-ai-at-scale)). That 30× is real but is **not** evidence that decode needs a 72-wide fabric — it conflates (a) the larger HBM pool letting a huge MoE model fit at all, (b) FP4 tensor cores, and (c) the fabric. Where the fabric *itself* dominates is **tensor-parallel prefill of long contexts**: a 405B model at 122 K-token context generates **~114 TB of aggregate NVLink traffic** and gets **3× faster time-to-first-token** scaling 8→32 GPUs ([NVIDIA GH200 NVL32 blog](https://developer.nvidia.com/blog/low-latency-inference-chapter-2-blackwell-is-coming-nvidia-gh200-nvl32-with-nvlink-switch-gives-signs-of-big-leap-in-time-to-first-token-performance/)). **Decode is memory-bandwidth-bound and far less fabric-hungry** — and NVIDIA itself is now physically separating it.
- **The industry is already un-bundling the rack for inference.** NVIDIA Dynamo runs **disaggregated prefill/decode** — prefill and decode on *separate GPU pools with independently chosen GPU counts and parallelism* ([NVIDIA Dynamo blog](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/)). Rubin CPX is a *separate, GDDR7, lower-bandwidth* prefill chip (`ai_hardware.md` §2.4). And the rack is already sold as **NVL36×2** (two 36-GPU half-racks) — a "half rack" is a shipping SKU, not a hypothetical ([SemiAnalysis](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)). The 72-GPU count is a strong default, not a hard floor.
- **Every other cluster uses the same tightly-coupled strategy — and for the same reason.** Google **TPU v7 "Ironwood"** wires up to 9,216 chips in a 3D-torus ICI fabric; AWS **Trainium2 UltraServer** wires 64 chips in a 4×4×4 3D torus over NeuronLink at 1 TB/s ([Google Cloud](https://docs.cloud.google.com/tpu/docs/tpu7x), [AWS](https://aws.amazon.com/ec2/ultraservers/)). The tightly-coupled scale-up "pod/superpod" is a **universal convergent design** — strong evidence the coupling solves a real problem. But all three vendors size the *coupled domain* far larger than one inference job needs, because the domain is sized for **training and for the largest models**; inference routinely runs on a *slice* of a TPU pod, and Ironwood is explicitly marketed for "the age of inference" while still being divisible into sub-pod slices.
- **The founder's hypothesis is directionally correct and viable — with real costs.** A self-integrated, inference-optimized orbital node (buy GPU+NVLink-switch silicon, design your own enclosure, pick the GPU count) is technically possible — NVIDIA now *sells* the building blocks via **NVLink Fusion** (NVLink SerDes, chiplets, switches, the MGX rack architecture licensed to AWS, Fujitsu, Qualcomm, Marvell et al. for semi-custom systems) ([NVIDIA NVLink Fusion](https://www.nvidia.com/en-us/data-center/nvlink-fusion/), [NVIDIA newsroom](https://nvidianews.nvidia.com/news/nvidia-nvlink-fusion-semi-custom-ai-infrastructure-partner-ecosystem)). And orbital peers already do it: **Starcloud-2** flies individual Blackwell GPUs and an AWS server *blade*, not an intact NVL72 ([NVIDIA blog on Starcloud](https://blogs.nvidia.com/blog/starcloud/)). The costs are loss of NVIDIA's validated rack integration, the warranty/support umbrella, and — if the GPU count is cut too far — the ability to hold a frontier model and to do fast long-context prefill.
- **A splittable / smaller / self-designed node would be LIGHTER — and that directly eases the flyability wall.** A space-modified intact rack is ~1.5–1.74 t (`node_mass_model.md` §2), and the *whole node* is ~5.6–14.1 t, **mass-bound** against Neutron's ~9.5 t reusable-SSO budget. A self-integrated node sheds the ~150–230 kg cabinet/reinforcement penalty and lets the GPU count — hence rack mass, power, radiator and solar — be **chosen** rather than inherited. A 36-GPU inference node is roughly *half* the compute mass and *half* the ~135 kW heat load. **A lighter node flies reusably for more silicon generations before outgrowing Neutron** — see §7.
- **When does splitting make sense? Probably ~6–7 years out, conditionally.** Today the costs (losing NVIDIA's integration, prefill penalty, engineering burden) outweigh the mass saving. The case strengthens as (a) inference disaggregation matures, (b) optical NVLink (Feynman, ~2028) removes the ~1–2 m copper reach limit and makes a "rack" a logical rather than physical object, and (c) per-GPU power keeps climbing, making the *full* rack heavier and hotter each generation. A self-designed inference node is best treated as a **Phase-2 upgrade path (~2031–2033)**, not a baseline.

**Confidence: medium.** High on the NVLink architecture facts, the training-vs-inference communication contrast, and the existence of half-rack SKUs / disaggregation / NVLink Fusion (all multiply sourced). Medium on the quantitative "how much fabric does decode actually need" — NVIDIA publishes *speedup* claims but not decode-phase fabric-utilization percentages. Medium-low on the cost/risk of a self-integrated node — no public teardown of a non-NVIDIA-integrated GPU node exists, and pricing/warranty terms for component-level GPU purchase are not public.

---

## 1. What physically makes an NVL72-class rack a single unit

### 1.1 The rack is the NVLink scale-up domain

An NVL72 rack is not "72 servers in a cabinet." It is one **NVLink scale-up domain**: 72 GPUs wired into a single non-blocking, all-to-all fabric so that — from software's point of view — they are *one* accelerator with one shared, coherent memory space. The physical ingredients (confirmed in `rack_internals.md` §1 and cross-checked here):

- **18 compute trays** (72 Blackwell GPUs + 36 Grace CPUs) + **9 NVLink-switch trays** (18 NVLink-switch ASICs).
- A passive **copper NVLink spine / backplane** — ~2 miles (3.2 km) of copper across ~5,184 cables in 4 cartridges — blind-mating every compute tray to every switch tray.
- **NVLink 5** delivers **1.8 TB/s per GPU** (18 links × 100 GB/s bidirectional), **~130 TB/s aggregate** across the rack — "orders of magnitude higher than PCIe-based architectures" and ~14× a PCIe Gen5 link ([NVIDIA NVLink](https://www.nvidia.com/en-us/data-center/nvlink/), [Introl](https://introl.com/blog/nvlink-scale-up-networking-gpu-interconnect-infrastructure-2025)).
- The 9 switch trays sit **centrally** between the two banks of compute trays — deliberately — because copper NVLink at 200 Gb/s-class lane rates reaches only **~1–2 m**. The fabric *must* be physically compact (`rack_internals.md` §4; [Tom's Hardware Vera Rubin](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date)).

So the rack-as-a-unit rests on **two distinct layers**, and separating them is the crux of this whole document:

1. **A physical layer (real, hard):** the copper NVLink fabric has a ~1–2 m reach. Any all-to-all NVLink domain *must* be a compact, densely-cabled assembly. You cannot spread one NVLink domain across a warehouse — or across satellites (`multi_rack_inference.md` §2.1 reaches the same verdict for tensor parallelism).
2. **A commercial / integration layer (a convention, soft):** NVIDIA *chooses* to sell, warranty, and support the whole 72-GPU cabinet — power shelves, busbar, liquid cooling, switches, GPUs — as one validated SKU. As multiple analysts put it, "Nvidia is defining what gets bought and deployed as a single system" and "the rack becomes the purchase unit, the operating unit, and the optimization target" ([HPCwire/NVIDIA](https://www.hpcwire.com/off-the-wire/nvidia-running-ai-workloads-on-rack-scale-supercomputers/), [Tom's Hardware on Rubin pricing](https://www.tomshardware.com/tech-industry/artificial-intelligence/price-of-nvidias-vera-rubin-nvl72-racks-skyrockets-to-as-much-as-usd8-8-million-apiece-but-server-makers-margins-will-be-tight-nvidia-is-moving-closer-to-shipping-entire-full-scale-systems)).

**The 72-GPU number itself is layer 2, not layer 1.** Nothing physical forces *72*. It is the count NVIDIA picked to (a) maximize the NVLink domain reachable with copper inside one cabinet's mechanical/power/thermal envelope and (b) be large enough to hold and accelerate trillion-parameter training jobs. A different operator with different constraints could, in principle, pick a different number — *if* it is willing to leave layer 2.

### 1.2 Latest 2026 architecture — GB300, Rubin, Rubin Ultra

The rack-scale strategy is *intensifying*, not loosening, across the 2026 roadmap (specs from `ai_hardware.md` §1–2, cross-checked):

| Generation | Status May 2026 | Scale-up domain | Per-GPU NVLink | Aggregate scale-up BW | Rack power |
|---|---|---|---|---|---|
| **GB300 NVL72** (Blackwell Ultra) | Shipping/ramping | 72 GPUs, in-rack copper | 1.8 TB/s (NVLink 5) | ~130 TB/s | ~135 kW TDP (~155 kW peak) |
| **Vera Rubin NVL72/NVL144** | Production H2 2026 | 72 packages / 144 dies, in-rack copper | 3.6 TB/s (NVLink 6) | **~260 TB/s** | ~190 kW (est.) |
| **Rubin Ultra NVL576** ("Kyber") | 2H 2027 | **576 GPUs** across 8 Oberon racks | NVLink 7 | **~1.5 PB/s** | **~600 kW** per Kyber rack |

Two things stand out for this analysis:

- **The coupled domain keeps growing** — from 72 to a 576-GPU NVLink domain (Rubin Ultra NVL576). NVIDIA is betting the *largest* future models need ever-bigger single domains ([DCD](https://www.datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027/), [Tom's Hardware Kyber](https://www.tomshardware.com/pc-components/gpus/nvidia-shows-off-rubin-ultra-with-600-000-watt-kyber-racks-and-infrastructure-coming-in-2027)).
- **NVL576 finally goes optical *between* racks.** Rubin Ultra uses **co-packaged optics (CPO) for the scale-up links connecting the 8 racks**, while keeping copper *inside* each rack ([SemiAnalysis GTC 2026](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands)). This is the important structural shift: once the scale-up fabric is optical, "the rack" stops being a hard physical boundary and becomes a *logical* one — directly relevant to §6 and to `rack_internals.md`'s Feynman-2028 optical-NVLink note.

The takeaway: NVIDIA's 2026 direction makes the *coupled domain* larger and (at the NVL576 tier) *optical*. That cuts both ways for this project — it shows the coupling is genuinely valuable, but it also shows the physical "rack" boundary is starting to dissolve into a logical one.

---

## 2. Is the tight in-rack fabric for training or for inference?

This is the central question. The honest answer: **the fabric is sized for training and for the worst-case inference phase (long-context prefill), and is over-provisioned for steady-state decode.**

### 2.1 Training is genuinely fabric-bound

Training runs forward **and** backward passes and synchronizes **gradients across the entire cluster every single step** — gigabytes per step, thousands of GPUs in lockstep, latency-critical (`inference_scaling.md` §3, `ai_hardware.md` §6). Tensor parallelism does an AllReduce after essentially every layer. This is the canonical justification for NVLink: "NVLink's low latency and high bandwidth support tensor parallelism, where model weights distribute across GPUs and must synchronize at every layer" ([Medium/Daya Shankar](https://medium.com/@daya-shankar/how-nvlink-enhances-multi-gpu-performance-6c797f72f6d0)). Training without a fast scale-up fabric is simply not viable. **For training, the rack-as-unit is fully justified.** (The project already concluded training is the wrong orbital workload — `inference_scaling.md` §4 — so this is mostly context.)

### 2.2 Inference splits into two phases with very different fabric appetites

Inference is forward-pass-only, and it has **two phases** that stress the fabric completely differently:

**Prefill (context phase) — fabric-hungry.** The model ingests the whole prompt at once. With tensor parallelism, "all GPUs involved must exchange data... in an AllReduce synchronization that happens twice per model layer." NVIDIA's measured example: a Llama-3.1-405B query at **122,880-token context** generates **~114 TB of aggregate interconnect traffic** across 32 GPUs, and scaling the NVLink domain from **8 GPUs → 32 GPUs cuts time-to-first-token by 3×** (2.6× for the 70B model) ([NVIDIA GH200 NVL32 blog](https://developer.nvidia.com/blog/low-latency-inference-chapter-2-blackwell-is-coming-nvidia-gh200-nvl32-with-nvlink-switch-gives-signs-of-big-leap-in-time-to-first-token-performance/)). So **long-context prefill genuinely uses the big fabric.** This is the strongest inference-side argument for a wide NVLink domain.

**Decode (generation phase) — memory-bandwidth-bound, far less fabric-hungry.** Decode generates tokens one at a time, autoregressively. It is "inherently sequential" and "fundamentally memory-bound rather than compute-bound" — the bottleneck is HBM bandwidth reading the weights and KV cache, *not* the interconnect ([Jarvis Labs](https://docs.jarvislabs.ai/blog/scaling-llm-inference-dp-pp-tp), [SemiAnalysis GTC 2026](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands)). Strikingly, NVIDIA's own inference characterization work finds that **for decode-dominant workloads "communication and synchronization costs outweigh computational parallelism benefits, making single-GPU execution optimal for both latency and throughput"** for dense models (a Frontier-simulator / arXiv characterization result, [arXiv 2512.01644](https://arxiv.org/pdf/2512.01644)). Decode does *not* want a 72-wide tensor-parallel group.

The one decode caveat is **MoE expert parallelism**: frontier MoE models route each token to a few experts via all-to-all, and "in MoE models the decode phase performs best with a wide Expert Parallelism setup." That all-to-all *does* use the fabric — but it is **moderate** bandwidth (DeepSeek runs 64-way EP across 8 *nodes* over 400 Gb/s InfiniBand — `multi_rack_inference.md` §2.3), not the TB/s firehose tensor parallelism needs. EP wants a *capable* fabric; it does not require the full 130 TB/s NVLink domain.

### 2.3 So how much does inference actually use the rack fabric? — honest quantification

NVIDIA does not publish a clean "decode uses X% of NVLink bandwidth" figure (flagged as an Open Question). What can be assembled from the sourced evidence:

| Workload phase | Fabric demand | Evidence | Could a smaller/looser domain serve it? |
|---|---|---|---|
| **Training** | Very high — continuous cluster-wide all-reduce | `inference_scaling.md` §3; universal industry consensus | No — needs the full fabric |
| **Inference prefill, long context** | High — ~114 TB aggregate for one 405B/122 K query; 3× TTFT from 8→32 GPUs | [NVIDIA GH200 NVL32 blog] | Partly — 32-GPU domain captures most of the 8→72 benefit; benefit saturates |
| **Inference prefill, short context** | Low–moderate | Traffic scales with context length²-ish; short prompts move little | Yes — small domain fine |
| **Inference decode, dense model** | Low — memory-BW-bound; single-GPU often optimal | [arXiv 2512.01644]; [Jarvis Labs] | Yes — decode does not want wide TP |
| **Inference decode, MoE all-to-all** | Moderate — expert-routing all-to-all | NVIDIA Wide-EP; DeepSeek 64-way EP over IB | Mostly — wants a capable fabric, not 130 TB/s |

**The honest synthesis:** the NVL72's 130 TB/s fabric is *sized for training and for long-context tensor-parallel prefill*. Steady-state decode — the bulk of a production inference token budget — is **memory-bandwidth-bound and uses a fraction of that fabric**. The "30× faster inference" NVIDIA headline is real but is **substantially a memory-capacity and FP4-compute story, not purely a fabric story**: an 8-GPU H100 system cannot even *hold* GPT-MoE-1.8T comfortably, so the 30× partly measures "the model fits and runs" vs "it doesn't," not "the fabric is 30× better for decode." NVIDIA's own blog declines to attribute the 30× to the fabric specifically ([NVIDIA GB200 NVL72 blog](https://developer.nvidia.com/blog/nvidia-gb200-nvl72-delivers-trillion-parameter-llm-training-and-real-time-inference/)) — it credits FP4, NVLink, *and* unified memory together.

**Could an inference node use fewer GPUs / a looser interconnect?** Yes, conditionally:
- It still needs **enough aggregate HBM to hold the model + KV cache** — `inference_scaling.md` §1–2: a 1–2 T model in FP8 is 1–2 TB; a GB300's 288 GB/GPU means **~8–16 GPUs hold a current frontier model's weights**, with more needed for KV-cache headroom. So the floor is *memory-driven*, ~16–36 GPUs for a frontier model, not 72.
- It needs a **capable** fabric for prefill and MoE-EP — but NVLink-class within a ~16–36-GPU module suffices; the jump to 72 mostly buys long-context-prefill latency, not decode throughput.
- It can offload long-context prefill to a **separate** stage (Dynamo / Rubin CPX — §3).

This is the technical core of the founder's hypothesis: **for inference, the 72-GPU rack is over-provisioned on fabric; a ~16–36-GPU module is a defensible inference node** provided it carries enough HBM and accepts a longer-context-prefill penalty (or disaggregates prefill).

---

## 3. The industry is already un-bundling the rack — for inference

The founder's hypothesis is not contrarian; NVIDIA and the field are *already moving this way for inference*:

- **Disaggregated prefill/decode (NVIDIA Dynamo).** Dynamo "disaggregates the prefill (compute-bound) and decode (memory-bound) phases across separate GPUs, enabling independent scaling and **phase-specific parallelism strategies**" with "custom GPU counts and model parallelism configurations" per phase ([NVIDIA Dynamo blog](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/), [AKS Engineering blog](https://blog.aks.azure.com/2025/10/24/dynamo-on-aks)). This is NVIDIA itself saying: *inference does not want one monolithic GPU pool — it wants separately-sized prefill and decode pools.* The 30× Dynamo-on-NVL72 figure is a *disaggregation* result, not a "you need 72 coupled GPUs" result.
- **Rubin CPX — a physically separate inference chip.** NVIDIA's most inference-specific 2026 product is a *monolithic GDDR7 GPU* (not HBM, not NVLink-rich) built **only for the prefill/context phase**, deployed alongside standard HBM Rubin GPUs that do decode (`ai_hardware.md` §2.4). NVIDIA is *physically un-bundling* inference into compute-heavy and memory-heavy silicon. An orbital designer could pick the phase/silicon mix that fits its mass-thermal envelope.
- **The "half rack" already ships.** GB200 is sold as **NVL72×1** (72 GPUs, one rack) *and* **NVL36×2** (two racks of 36 GPUs each, NVLink-bridged). Within an NVL36 it is 1 NVLink hop to any of 36 GPUs; crossing to the partner rack costs 2 NVSwitch hops and needs **162 extra 1.6T ACC cables + 324 DensiLink flyover cables (>$10,000/system just in flyover cables)** ([SemiAnalysis GB200 BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)). So a **36-GPU half-rack is a real, shipping, NVLink-coherent unit** — not a hypothetical. The penalty for splitting 72→36+36 is *cabling cost and a 2-hop latency increment*, which is modest and quantifiable.
- **8-GPU baseboards are a mainstream SKU.** The **HGX B200/B300** 8-GPU baseboard is sold as "a cost-efficient starting point... for AI training and inference" with its own NVLink/NVSwitch ([Supermicro](https://www.supermicro.com/en/accelerators/nvidia), [Arc Compute](https://www.arccompute.io/arc-blog/the-difference-between-nvidia-hgx-b200-hgx-b300-and-gb300-nvl72-which-nvidia-platform-is-right-for-ai-at-scale)). NVIDIA *itself* sells GPUs in 8-GPU NVLink islands; the NVL72 is the *large* option, not the *only* option.

**Conclusion of §3:** "Split the rack for inference" is not a fringe idea — it is the direction of NVIDIA's own 2026 inference stack (Dynamo disaggregation, Rubin CPX, NVL36×2, HGX-8). The orbital question is not *whether* sub-72-GPU inference units are valid — they are — but whether Rocket Lab should *self-integrate* one rather than buy an NVIDIA SKU (§5).

---

## 4. TPU and other-cluster comparison — does everyone couple tightly?

**Yes — tight scale-up coupling is a universal, convergent design across every serious AI accelerator. But every vendor sizes the *coupled domain* far larger than one inference job, and every vendor lets it be *sliced*.**

| Cluster | Scale-up fabric | Coupled domain size | Topology | Per-link / aggregate BW | Training vs inference |
|---|---|---|---|---|---|
| **NVIDIA NVL72** | NVLink 5 + NVLink Switch | 72 GPUs (576 at NVL576) | Non-blocking all-to-all (switched) | 1.8 TB/s/GPU; ~130 TB/s | Same fabric both; sized for training + prefill |
| **Google TPU v7 "Ironwood"** | Inter-Chip Interconnect (ICI) | up to **9,216 chips** per pod | **3D torus** (each chip → 6 neighbors), + Optical Circuit Switching | **200 GB/s per axis**, 3 axes | "First TPU for the age of inference" — but pod is *sliced* for jobs |
| **AWS Trainium2 UltraServer** | NeuronLink | **64 chips** (4×4×4) | 2D torus per instance → 3D torus across | **1 TB/s** chip-to-chip | "AI training and inference" |
| **AWS Trainium3 UltraServer** | NeuronLink | larger (GA Dec 2025) | torus | higher | training + inference |

Sources: [Google Cloud TPU7x docs](https://docs.cloud.google.com/tpu/docs/tpu7x), [Google "age of inference" blog](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/ironwood-tpu-age-of-inference/), [Fibermall TPU architecture](https://www.fibermall.com/blog/unveiling-google-tpu-architecture.htm), [AWS UltraServers](https://aws.amazon.com/ec2/ultraservers/), [SemiAnalysis Trainium3](https://newsletter.semianalysis.com/p/aws-trainium3-deep-dive-a-potential), [Next Platform Trainium4](https://www.nextplatform.com/2025/12/03/with-trainium4-aws-will-crank-up-everything-but-the-clocks/).

**Architectural rationale — and the key nuance for this project:**

- **Why everyone couples:** a model too big for one chip *must* be split, and the communication-intensive splits (tensor parallelism, MoE all-to-all) need a fast, low-latency fabric or the chips starve waiting on each other. Every vendor independently converged on a tightly-coupled "pod/superpod/UltraServer" because the alternative — splitting a model over slow links — does not work for training. **The coupling solves a real problem; that NVIDIA, Google, and AWS all do it is strong evidence it is not arbitrary.**
- **Why it differs by topology — and why that matters here.** NVIDIA uses a *switched, non-blocking all-to-all* fabric: any GPU to any GPU at full bandwidth, but it needs central switch trays and is reach-limited to a compact cabinet. Google and AWS use a **torus**: each chip wired only to its **6 (TPU) or near-neighbors (Trainium)** — *no central switch*, cheaper, more scalable to thousands of chips, but any-to-any traffic must *hop* through intermediate chips. **The torus is inherently more "splittable":** a TPU pod is routinely carved into smaller *slices* (a sub-cube of the torus) for individual jobs, and inference very commonly runs on a slice far smaller than the 9,216-chip pod. NVIDIA's all-to-all fabric is *less* naturally divisible — which is part of *why* the NVL72 feels like one indivisible "rack" while a TPU pod feels like a divisible fabric.
- **Training vs inference, across all three:** every vendor sizes the *maximum* coupled domain for training the largest models. **None of them require inference to use the whole domain.** Google explicitly markets Ironwood for "the age of inference" yet a typical inference deployment uses a small torus slice; TPU inference of a model that fits in, say, 8–64 chips runs on 8–64 chips, not 9,216. **This is the cross-cluster confirmation of the founder's hypothesis:** the giant coupled domain is a *training-and-largest-model* artifact; inference universally runs on a right-sized subset.

So the comparison cuts both ways. It *confirms* tight coupling is real and necessary for the communication-heavy parallelism. It *also* confirms that the full pod/rack is over-sized for an inference job, and that the field already runs inference on sliced-down subsets. The NVL72 *feels* more monolithic than a TPU pod mainly because NVIDIA sells it as one SKU and its all-to-all topology is less gracefully divisible than a torus — both *commercial/architectural* facts, not a law forbidding a smaller inference node.

---

## 5. The founder's hypothesis — buy GPUs, self-design an inference-optimized node

> **Founder's hypothesis:** the rack is a packaging convention optimized for *ground* data centers (rolls on a floor, hooks to facility water and grid power, serviced by a technician). An orbital operator could instead **buy GPUs** and integrate its **own inference-optimized node** — choosing the GPU count, designing the "rack" around the orbital constraint (mass, power, the flyability ceiling) rather than around a data-center aisle.

### 5.1 Is it viable? — Yes, technically, and the building blocks are now sold

The hypothesis is **directionally correct and technically viable.** Three independent lines of evidence:

1. **The ground-optimized parts of a rack are dead weight in orbit — and a self-design removes them.** `node_mass_model.md` §2 already strips fans/plenums (−20–40 kg) and castors/floor-mount hardware (−10–25 kg) for the space-modified rack, but it *keeps* the EIA-310 cabinet and then *adds* +120–250 kg of launch reinforcement to an off-the-shelf frame that "forces reinforcing an off-the-shelf frame rather than designing loads out — a mass penalty we accept" (its words). A clean-sheet node designed for launch loads from scratch — load paths, tray restraints and the structure co-designed — avoids paying that penalty twice. `node_mass_model.md` §2 explicitly says "a clean-sheet space-optimized compute unit could undercut this." **The intact-rack baseline is, by the project's own model, carrying ground-DC packaging mass it does not need.**
2. **NVIDIA now *sells the building blocks* — NVLink Fusion.** The historical objection ("you can only buy the whole rack") is weakening fast. **NVLink Fusion** (2025–26) licenses "NVLink SerDes, NVLink chiplets, NVLink Switches, and all aspects of the rack-scale architecture" plus the **OCP MGX rack architecture** to third parties building **semi-custom** systems — adopted by **AWS (Trainium4), Fujitsu, Qualcomm, Marvell, MediaTek, Alchip, Astera Labs** ([NVIDIA NVLink Fusion](https://www.nvidia.com/en-us/data-center/nvlink-fusion/), [NVIDIA newsroom](https://nvidianews.nvidia.com/news/nvidia-nvlink-fusion-semi-custom-ai-infrastructure-partner-ecosystem), [NVIDIA blog](https://developer.nvidia.com/blog/scaling-ai-inference-performance-and-flexibility-with-nvidia-nvlink-and-nvlink-fusion/)). The whole *point* of NVLink Fusion is that a partner can build its **own rack-scale system, with its own chosen components and GPU count, still using NVLink** — exactly the founder's idea, productized by NVIDIA for hyperscalers.
3. **Orbital peers already self-integrate.** **Starcloud-2** (launching 2026) flies "multiple GPUs, including an NVIDIA Blackwell chip and an **AWS server blade**, as well as a bitcoin-mining computer" — a custom satellite payload, **not an intact NVL72** ([NVIDIA blog on Starcloud](https://blogs.nvidia.com/blog/starcloud/), [DCD](https://www.datacenterdynamics.com/en/news/crusoe-to-deploy-in-starcloud-satellite-data-center-in-late-2026-offer-limited-gpu-capacity-in-space-from-2027/)). Starcloud-3 is a clean-sheet "200 kW, 3-ton spacecraft." The orbital-DC field is *already* buying GPUs/blades and self-integrating; no one is bolting a literal NVL72 cabinet to a satellite. (`ai_hardware.md` already notes Rocket Lab itself markets silicon solar arrays for space-based data centers.)

### 5.2 What would it cost / enable / risk

| Dimension | Buy intact NVL72-class rack (baseline) | Self-designed inference node (founder's hypothesis) |
|---|---|---|
| **Mass** | ~1.5–1.74 t space-modified rack, incl. ~150–230 kg cabinet + reinforcement penalty on an off-the-shelf frame | **Lower** — clean-sheet structure designed for launch loads; GPU count chosen, not inherited. A 36-GPU node ≈ half the compute mass. **The core win — see §7.** |
| **Power / heat** | ~135–190 kW inherited (fixed by 72-GPU count) | **Chosen** — a 36-GPU node ≈ ~70–95 kW → roughly half the radiator (`node_mass_model.md` §4) and half the solar (§3). Cascades into multi-tonne node-mass savings. |
| **Integration risk** | **Low** — NVIDIA validates the whole rack; thermal, power, signal integrity, NVLink topology all pre-engineered | **High** — Rocket Lab owns signal integrity of the NVLink fabric, power delivery, the liquid loop, NVSwitch topology. This is hard, specialist engineering. |
| **NVLink fabric** | Full validated 130 TB/s (Rubin: 260 TB/s) all-to-all | Must be re-implemented via **NVLink Fusion** (licensable) — or accept a smaller/looser fabric. Re-implementing a non-blocking NVLink fabric is non-trivial; copper reach (~1–2 m) still constrains physical layout. |
| **Warranty / support** | NVIDIA + integrator (Supermicro/HPE/Lenovo) warranty and support umbrella | **Lost / renegotiated** — NVIDIA's standard manufacturer warranty does not cover self-integrated systems; "system builders, installers and integrators" fall under separate NVIDIA *sales* T&Cs ([NVIDIA warranty](https://www.nvidia.com/en-us/support/warranty/)). For a satellite that cannot be serviced anyway, in-orbit warranty is *already* near-worthless — this risk is smaller for a space operator than for a ground DC. |
| **Frontier-model capability** | 72 GPUs / ~20 TB HBM holds any current frontier model + generous KV headroom | A too-small node (e.g. 8–16 GPUs) **cannot hold a frontier model** + KV cache. Must size ≥~16–36 GPUs (`inference_scaling.md` §2). Long-context prefill degrades below ~32 GPUs unless disaggregated. |
| **Supply chain / cost** | Buy a finished product; ~$3–8.8M/rack (Rubin) | Buy GPUs + switch silicon + license NVLink Fusion; **uncertain** whether component-level GPU allocation is even *available* to a non-hyperscaler at useful volume — NVIDIA prioritizes rack SKUs. **Major commercial unknown.** |
| **Schedule** | Fast — integrate a known product | Slow — a clean-sheet compute node is a multi-year development on top of the satellite bus. |

**Net assessment.** The founder's hypothesis is **viable and the mass logic is sound** — a self-designed inference node *would* be lighter and cooler, and NVIDIA's NVLink Fusion plus the Starcloud precedent show the building blocks exist. But it trades a **low-risk, fast, validated** path for a **high-risk, slow, specialist-engineering** path, and it carries a real commercial unknown: whether Rocket Lab can even *procure* GPUs at component level (versus rack SKUs) at useful volume and price. The warranty loss, often cited as a blocker, is **largely moot for an un-serviceable satellite** — that is a point in the hypothesis's favor.

---

## 6. Can a rack be split — and should it?

### 6.1 What splitting costs, concretely

Splitting an NVL72 into smaller modules (36-GPU half-racks, or ~16-GPU modules) for inference has **quantifiable, modest costs** — not prohibitive ones:

- **Latency / hop penalty.** Within an NVL36 half-rack, any-to-any is **1 NVSwitch hop**; bridging two half-racks is **2 hops** ([SemiAnalysis](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)). Each hop adds sub-microsecond switch latency — negligible against inference SLAs measured in *tens of ms* (`inference_scaling.md` §3). For a node that is a *single* ~36-GPU module with no bridging, there is **no hop penalty at all** — it is just a smaller all-to-all domain.
- **Long-context prefill penalty.** This is the real cost. Dropping the tensor-parallel domain from 72→36→16 GPUs lengthens time-to-first-token for long contexts — the 8→32-GPU data showed a 3× TTFT swing for a 122 K-token 405B query ([NVIDIA GH200 NVL32 blog](https://developer.nvidia.com/blog/low-latency-inference-chapter-2-blackwell-is-coming-nvidia-gh200-nvl32-with-nvlink-switch-gives-signs-of-big-leap-in-time-to-first-token-performance/)). Mitigations: (a) disaggregate prefill onto a separate stage (Dynamo / Rubin CPX), (b) accept slower TTFT for long prompts, (c) keep the module at ~32–36 GPUs, which captures most of the 8→72 benefit (the curve saturates).
- **Inter-module comms.** If a model is split *across* modules, traffic must use a slower link than in-rack NVLink. Tensor parallelism **cannot** cross that boundary (`multi_rack_inference.md` §2.1 — firm). Pipeline and expert parallelism **can**, with a throughput cost. So a split-rack architecture must keep each model's tensor-parallel group inside one module — exactly the constraint `multi_rack_inference.md` already established for cross-satellite splitting.
- **Lost NVIDIA integration.** Splitting into self-designed modules forfeits the validated rack (§5.2) — the dominant *non-technical* cost.

### 6.2 When does splitting make sense?

**Not yet. Probably ~6–7 years out, and conditionally.** The case for a split / self-designed inference node strengthens along three converging trends:

1. **Inference disaggregation matures (happening now → ~2028).** As Dynamo-style prefill/decode disaggregation and Rubin-CPX-style phase-specialized silicon become the norm, the "one monolithic 72-GPU pool" loses its rationale for inference. A node built as a right-sized decode module + a prefill stage becomes the *natural* design, not a compromise.
2. **Optical NVLink removes the reach limit (Feynman, ~2028).** Today copper NVLink's ~1–2 m reach is what forces the fabric into one compact cabinet (§1.1). NVIDIA already uses **CPO for scale-up between racks in Rubin Ultra NVL576** (2027) and offers **optical NVLink from the Feynman generation, ~2028** (`rack_internals.md` §4, [SemiAnalysis GTC 2026](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands)). Once the scale-up fabric is optical, "a rack" becomes a *logical* grouping, not a physical box — and a self-designed node can place GPUs and switches where mass/thermal layout wants them, not where copper reach dictates.
3. **Per-GPU power keeps climbing.** Blackwell ~1.0–1.4 kW/GPU → Rubin ~1.8–2.3 kW/die → Kyber racks at ~600 kW (`ai_hardware.md` §1). Every generation, the *full* 72-GPU rack gets heavier and hotter, pushing the intact-rack node *harder* into Neutron's mass wall. A right-sized inference node — fewer GPUs, chosen power envelope — is a way to *stay under* the wall as the silicon trend works against the intact rack.

**Timeline:** these mature around **2031–2033** — roughly the "~6–7 years out" the brief anticipates. Before then, the intact (or space-modified) rack remains the right baseline: lower risk, faster, and the disaggregation/optical enablers are not yet in hand. The project should treat the self-designed split inference node as a **Phase-2 architecture option**, explicitly revisited when (a) optical NVLink ships and (b) inference disaggregation is mature — not as a Phase-1 baseline.

---

## 7. Why it matters for the project — the flyability-wall linkage

This is the payoff and the reason the founder wants the assumption challenged.

**The flyability wall.** `node_mass_model.md` is unambiguous: the 1-rack node is **mass-bound**, at ~5.6–14.1 t against Neutron's **~9.5 t** working reusable-SSO budget (range 8.5–10.5 t). It fits reusably *only* near the mass-optimized end. Each new silicon generation raises per-GPU power → bigger radiator + bigger solar (the multi-tonne line items) → the node mass climbs. There is a generation at which an intact-rack node **outgrows Neutron's reusable budget** and forces an expendable launch or a Neutron block-upgrade. That is the flyability wall.

**A self-designed / split / smaller inference node directly lowers the wall.** The mechanism is straightforward and compounds through `node_mass_model.md`'s own chain:

- **Fewer GPUs → less rack mass.** A 36-GPU inference module is roughly *half* the compute-tray mass of a 72-GPU rack (compute trays are ~half the rack — `rack_internals.md` §2), and a clean-sheet structure sheds the ~150–230 kg ground-DC cabinet/reinforcement penalty (`node_mass_model.md` §2) on top.
- **Fewer GPUs → less power → much less radiator and solar.** This is the big lever. `node_mass_model.md` shows radiator (~1.1–4.0 t/rack) and solar (~1.0–2.3 t/rack) are the dominant node-mass lines, and **both scale ~linearly with rack power.** A 36-GPU node at ~70–95 kW instead of ~135–190 kW roughly *halves* both — plausibly **2–4 t off the node**. That is the difference between comfortably-reusable and over-budget.
- **A lighter node flies reusably for more silicon generations.** Because the node sits *below* the ~9.5 t reusable ceiling with margin, it can absorb several generations of rising per-GPU power before hitting the wall. **A lighter node flies longer before outgrowing Neutron** — precisely the brief's framing. It also preserves *reusable* (not expendable) launch, the cheaper mode.
- **It composes with the `multi_rack_inference.md` result.** That doc showed capacity grows by adding *independent laser-linked single-rack satellites*. Replace "single-rack" with "single right-sized-inference-module" satellites and the constellation gets the same near-linear scaling with *lighter, cheaper-to-launch* nodes. The two ideas reinforce: split *within* the node (this doc) and mesh *across* nodes (`multi_rack_inference.md`).

**The honest counter-weight.** A smaller node also carries *less compute per launch* — capacity per satellite drops, so more satellites (more launches) are needed for the same total throughput. The trade is **mass-per-node and reusability vs. compute-per-node.** For a *mass-bound, flyability-limited* project, easing the mass wall is plausibly worth more launches of lighter nodes — but this is a constellation-economics question (launch cost per delivered token) that deserves its own quantified study, not a foregone conclusion. The split-node idea is a *lever on the flyability wall*; whether to pull it depends on launch economics.

**Bottom line for the project:** the "node = one intact NVL72-class rack" assumption is a **defensible Phase-1 baseline but not a law.** It is a ground-data-center packaging convention. For *inference*, the 72-GPU rack is over-provisioned on interconnect fabric; the binding floor is ~16–36 GPUs of HBM to hold a frontier model. A self-designed, inference-optimized, ~36-GPU node is **technically viable** (NVLink Fusion sells the parts; Starcloud already self-integrates), would be **materially lighter and cooler**, and would **directly push back the flyability wall** — at the cost of integration risk, a long-context-prefill penalty, lost NVIDIA validation, and a real procurement unknown. It is best carried as a **Phase-2 upgrade path (~2031–2033)**, gated on optical NVLink and mature inference disaggregation, and paired with a launch-economics study of lighter-node-more-launches vs. intact-rack-fewer-launches.

---

## Consolidated answer to the brief's questions

| Question | Answer |
|---|---|
| **Why is a rack a rack?** | It is one NVLink scale-up domain — 72 GPUs in a non-blocking all-to-all 130 TB/s fabric, physically compact because copper NVLink reaches only ~1–2 m. The *72-GPU count* and *sold-as-one-unit* are commercial/integration conventions on top of that physical fact. |
| **Is the tight fabric for training or inference?** | Primarily training, and secondarily long-context inference *prefill*. Steady-state *decode* is memory-bandwidth-bound and uses a fraction of the fabric. The "30× inference" headline is substantially a memory-capacity + FP4 story, not purely a fabric story. |
| **Could an inference node use fewer GPUs / a looser interconnect?** | Yes — floor is ~16–36 GPUs (set by HBM needed to hold a frontier model + KV cache), not 72. A capable NVLink-class fabric within that module suffices; the jump to 72 mainly buys long-context-prefill latency. |
| **Do TPU / Trainium couple the same way?** | Yes — universal convergent design (TPU 3D-torus pods, Trainium NeuronLink torus). But all size the coupled domain for training/largest models and routinely run inference on *sliced-down subsets*. The torus is more naturally divisible than NVIDIA's all-to-all. |
| **Is a self-designed orbital node viable?** | Technically yes — NVLink Fusion licenses the building blocks; Starcloud already self-integrates GPUs/blades. Costs: integration risk, lost NVIDIA validation, a long-context-prefill penalty if undersized, and an unresolved component-procurement unknown. Warranty loss is largely moot for an un-serviceable satellite. |
| **Can/should a rack be split?** | Can: yes — half-racks (NVL36) already ship; splitting costs a 2-hop latency increment (negligible) and a long-context-prefill penalty (real, mitigable). Should: not yet — best as a Phase-2 option ~2031–2033, gated on optical NVLink and mature disaggregation. |
| **Why it matters:** | A lighter, self-designed, ~36-GPU inference node roughly halves rack mass, power, radiator and solar — pushing back the flyability wall so the node flies *reusably* for more silicon generations. Trade-off: less compute per launch → more launches; needs a launch-economics study. |

---

## Sources

NVLink architecture & the rack as a unit:
- [NVIDIA — NVLink & NVLink Switch (official)](https://www.nvidia.com/en-us/data-center/nvlink/)
- [NVIDIA — GB200 NVL72 delivers trillion-parameter LLM training and real-time inference](https://developer.nvidia.com/blog/nvidia-gb200-nvl72-delivers-trillion-parameter-llm-training-and-real-time-inference/)
- [NVIDIA — Running AI Workloads on Rack-Scale Supercomputers](https://developer.nvidia.com/blog/running-ai-workloads-on-rack-scale-supercomputers-from-hardware-to-topology-aware-scheduling/) / [HPCwire mirror](https://www.hpcwire.com/off-the-wire/nvidia-running-ai-workloads-on-rack-scale-supercomputers/)
- [Introl — NVLink and scale-up networking](https://introl.com/blog/nvlink-scale-up-networking-gpu-interconnect-infrastructure-2025)
- [Nebius — rack-scale GPU interconnect with GB200 NVL72](https://nebius.com/blog/posts/leveraging-nvidia-gb200-nvl72-gpu-interconnect)
- [Tom's Hardware — Vera Rubin NVL72 pricing / NVIDIA shipping full systems](https://www.tomshardware.com/tech-industry/artificial-intelligence/price-of-nvidias-vera-rubin-nvl72-racks-skyrockets-to-as-much-as-usd8-8-million-apiece-but-server-makers-margins-will-be-tight-nvidia-is-moving-closer-to-shipping-entire-full-scale-systems)

Latest 2026 architecture — GB300, Rubin, Rubin Ultra NVL576:
- [VideoCardz — Vera Rubin NVL72: 260 TB/s scale-up](https://videocardz.com/newz/nvidia-vera-rubin-nvl72-detailed-72-gpus-36-cpus-260-tb-s-scale-up-bandwidth)
- [DCD — Rubin Ultra NVL576 expected 600 kW, 2H 2027](https://www.datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027/)
- [Tom's Hardware — Rubin Ultra Kyber 600 kW racks](https://www.tomshardware.com/pc-components/gpus/nvidia-shows-off-rubin-ultra-with-600-000-watt-kyber-racks-and-infrastructure-coming-in-2027)
- [SemiAnalysis — GTC 2026: The Inference Kingdom Expands (NVL576 CPO scale-up)](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands)
- [Tom's Hardware — Vera Rubin platform in depth](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date)

Inference vs training fabric demand; prefill vs decode:
- [NVIDIA — Low-Latency Inference Ch.2: GH200 NVL32, time-to-first-token (114 TB, 3× TTFT)](https://developer.nvidia.com/blog/low-latency-inference-chapter-2-blackwell-is-coming-nvidia-gh200-nvl32-with-nvlink-switch-gives-signs-of-big-leap-in-time-to-first-token-performance/)
- [NVIDIA — Scaling AI Inference with NVLink and NVLink Fusion](https://developer.nvidia.com/blog/scaling-ai-inference-performance-and-flexibility-with-nvidia-nvlink-and-nvlink-fusion/)
- [arXiv 2512.01644 — A Systematic Characterization of LLM Inference on GPUs](https://arxiv.org/pdf/2512.01644)
- [Jarvis Labs — Scaling LLM Inference: DP, PP & TP](https://docs.jarvislabs.ai/blog/scaling-llm-inference-dp-pp-tp)
- [Will It Run AI — Multi-GPU LLM Inference Guide: NVLink vs PCIe, Tensor Parallelism (2026)](https://willitrunai.com/blog/multi-gpu-llm-inference-guide)
- [Medium/Daya Shankar — How NVLink Enhances Multi-GPU Performance](https://medium.com/@daya-shankar/how-nvlink-enhances-multi-gpu-performance-6c797f72f6d0)

Un-bundling: disaggregation, half-racks, HGX-8:
- [NVIDIA — Introducing NVIDIA Dynamo (disaggregated prefill/decode)](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/)
- [AKS Engineering — Scaling multi-node LLM inference with Dynamo on GB200 NVL72](https://blog.aks.azure.com/2025/10/24/dynamo-on-aks)
- [SemiAnalysis — GB200 Hardware Architecture & Component Supply Chain (NVL36×2, cabling)](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)
- [Arc Compute — HGX B200 vs HGX B300 vs GB300 NVL72](https://www.arccompute.io/arc-blog/the-difference-between-nvidia-hgx-b200-hgx-b300-and-gb300-nvl72-which-nvidia-platform-is-right-for-ai-at-scale)
- [Supermicro — NVIDIA Blackwell HGX B300/B200 and GB200 NVL72 solutions](https://www.supermicro.com/en/accelerators/nvidia)

TPU & Trainium comparison:
- [Google Cloud — TPU7x (Ironwood) documentation](https://docs.cloud.google.com/tpu/docs/tpu7x)
- [Google — Ironwood: the first TPU for the age of inference](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/ironwood-tpu-age-of-inference/)
- [Fibermall — Unveiling Google's TPU architecture: OCS, 3D torus](https://www.fibermall.com/blog/unveiling-google-tpu-architecture.htm)
- [AWS — EC2 UltraServers (Trainium2/3)](https://aws.amazon.com/ec2/ultraservers/)
- [AWS Neuron docs — Trn2 architecture (NeuronLink, 2D/3D torus)](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn2-arch.html)
- [SemiAnalysis — AWS Trainium3 Deep Dive](https://newsletter.semianalysis.com/p/aws-trainium3-deep-dive-a-potential)
- [Next Platform — With Trainium4, AWS will crank up everything but the clocks](https://www.nextplatform.com/2025/12/03/with-trainium4-aws-will-crank-up-everything-but-the-clocks/)

Self-designed / semi-custom node — NVLink Fusion, warranty, orbital peers:
- [NVIDIA — NVLink Fusion (official)](https://www.nvidia.com/en-us/data-center/nvlink-fusion/)
- [NVIDIA newsroom — NVLink Fusion for semi-custom AI infrastructure](https://nvidianews.nvidia.com/news/nvidia-nvlink-fusion-semi-custom-ai-infrastructure-partner-ecosystem)
- [NVIDIA — Integrating Semi-Custom Compute into Rack-Scale Architecture with NVLink Fusion](https://developer.nvidia.com/blog/integrating-custom-compute-into-rack-scale-architecture-with-nvidia-nvlink-fusion/)
- [NVIDIA — Manufacturer's Warranty](https://www.nvidia.com/en-us/support/warranty/)
- [NVIDIA blog — How Starcloud is bringing data centers to outer space](https://blogs.nvidia.com/blog/starcloud/)
- [DCD — Crusoe to deploy in Starcloud satellite data center](https://www.datacenterdynamics.com/en/news/crusoe-to-deploy-in-starcloud-satellite-data-center-in-late-2026-offer-limited-gpu-capacity-in-space-from-2027/)

(See also project docs: [rack_internals.md](rack_internals.md), [ai_hardware.md](../ai_hardware/ai_hardware.md), [inference_scaling.md](../llm_compute/inference_scaling.md), [multi_rack_inference.md](../llm_compute/multi_rack_inference.md), [node_mass_model.md](node_mass_model.md).)

---

## Open questions / uncertainties

1. **NVIDIA publishes no decode-phase fabric-utilization figure.** The conclusion that decode uses "a fraction" of the 130 TB/s fabric is assembled from speedup claims, the memory-bound nature of decode, and the arXiv characterization that single-GPU decode is often optimal — but no source gives a clean "decode consumes X% of NVLink bandwidth" number. A profiling study (or InferenceMAX-style trace) on a real frontier MoE model would pin this down. **Highest-value unknown for sizing a smaller node.**
2. **Can a non-hyperscaler procure GPUs at component level?** The self-designed-node case assumes Rocket Lab can *buy* GPU + NVSwitch silicon (or license NVLink Fusion) at useful volume and price. NVIDIA prioritizes rack SKUs and reserves NVLink Fusion engagements for large partners (AWS, Fujitsu, Qualcomm, Marvell). Whether a mid-size space operator gets component-level allocation — and at what price vs. a rack SKU — is **not public** and is a gating commercial risk.
3. **No public teardown / mass figure for a self-integrated (non-NVIDIA-rack) GPU node.** The claim that a clean-sheet node sheds the ~150–230 kg cabinet/reinforcement penalty is sound directionally (`node_mass_model.md` §2 says so) but is not backed by a built example. Starcloud's payload masses are not published at component level.
4. **The long-context-prefill penalty below 32 GPUs is bracketed, not measured for the target regime.** The 8→32-GPU 3× TTFT figure is for a 405B/122 K-token query on GH200; the exact TTFT cost of a 36- or 16-GPU module for a *2026 frontier MoE* model at the project's target context length needs a model-specific simulation. If the orbital service targets short-to-moderate contexts, the penalty is small; for 100 K+ contexts it is significant unless prefill is disaggregated.
5. **Optical-NVLink timing (Feynman ~2028) drives the Phase-2 window.** The "split makes sense ~2031–2033" verdict assumes optical NVLink ships ~2028 and matures over a few years. If optical NVLink slips, the physical ~1–2 m copper reach keeps the rack monolithic longer and the self-designed-node window moves right. Conversely, NVL576's 2027 CPO scale-up could pull useful optical building blocks forward. Revisit when Feynman specs firm up.
6. **Launch-economics trade is unquantified.** §7 establishes that a lighter split node eases the flyability wall but carries less compute per launch. Whether lighter-node-more-launches beats intact-rack-fewer-launches on *launch cost per delivered token* is a constellation-economics question this doc flags but does not solve. Needs a dedicated study, cross-referencing `node_mass_model.md` and any launch-cadence/cost doc.
7. **Re-implementing a non-blocking NVLink fabric is hard, specialist engineering.** NVLink Fusion licenses the IP, but signal integrity at 200 Gb/s-class lane rates, NVSwitch topology, and the liquid-cooled power delivery for a self-designed node are genuine engineering risk. The doc treats this as "high risk" qualitatively; an engineering-effort and schedule estimate is not attempted here.
8. **MoE expert-parallelism fabric demand for a *small* module.** Decode-phase EP all-to-all is "moderate" bandwidth, but how a ~16–36-GPU module's narrower fabric affects EP throughput for a wide-expert frontier model is not quantified — borderline, same caveat `multi_rack_inference.md` §2.3 raises for cross-satellite EP.
