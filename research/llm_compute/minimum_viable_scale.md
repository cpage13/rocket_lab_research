# Minimum Viable Service Scale — How Many Nodes to Be a Worthwhile Inference Service

*Research compiled May 2026. Part of the Rocket Lab orbital AI-inference data center feasibility study.
Companion to `inference_scaling.md` (one rack per model), `multi_rack_inference.md` (laser-meshed
multi-rack), and `economics/revenue_per_watt.md` (the ~$8–16M/rack-year revenue basis).*

---

## Summary / Verdict (read this first)

**The question:** "It can run a frontier model" is not "it is a worthwhile service." How much
*throughput / how many users* does a node count actually serve, and what is the smallest deployment
that is commercially meaningful?

**The verdict:**

- **Throughput per node.** A single NVL72-class rack serving a 1–2 T-parameter frontier MoE model
  delivers, as a planning band, **~0.3–1.0 million output tokens/second aggregate** — toward the
  **high end (~0.8–1.0 M tok/s) in a batch/throughput regime** (low per-user speed, KV cache full),
  and toward the **low end (~0.2–0.4 M tok/s) in an interactive regime** that holds ~50–250 tok/s per
  user. This is workload-dependent; every number below carries its assumption set. Public benchmarks
  are for DeepSeek-R1-class (671 B) models — a 1–2 T model runs **somewhat slower per token**, so we
  treat the lower half of the band as the frontier-model planning case.
- **Users per node.** Translating throughput into population: a single rack supports very roughly
  **~10,000–50,000 concurrent active chat users**, or a *registered* base perhaps **20–50× larger**
  (~0.5–2 M registered users) given duty-cycle and concurrency ratios. For **agentic enterprise
  workloads** — which burn **5–30× more tokens per task** — the same rack serves only **~1,000–5,000
  concurrent agentic users** or a few hundred to a few thousand always-on enterprise agents. A node is
  a **mid-five-figure-to-low-six-figure-user** service, not a hyperscale one.
- **1 node vs 2 nodes.** One single-rack node already *runs* a current frontier model and is a
  complete, commercially meaningful service on its own. **Meshing two laser-linked nodes via pipeline
  parallelism primarily adds model-*size* headroom (the >~10–15 T-parameter future model), not
  throughput** — and a PP-split pair actually yields *less* than 2× the throughput of two independent
  replicas because of pipeline bubbles and the ISL hop. For throughput, **two independent replicas
  beat one meshed pair.** Meshing is a capability unlock, not a scaling lever.
- **Minimum viable commercial deployment.** The smallest deployment that (a) runs a frontier model,
  (b) serves a commercially meaningful user base, and (c) earns enough to justify a launch campaign is
  **a single node** on the pure arithmetic — one rack at ~$8–16M/rack-year revenue basis, plus an
  orbital/latency premium, can in principle gross **~$10–25M/year**. **But one node is not viable as a
  *service* because it is a single point of failure with zero redundancy.** The realistic minimum
  viable commercial deployment is **~3–5 nodes**: enough for one frontier-model replica with N+1
  redundancy, a few hundred thousand to ~1 M served users, and **~$30–80M/year of gross revenue** —
  a figure that clears the bar for a dedicated Neutron launch campaign. **The V1 target should be a
  handful of nodes (~3–6), not one, and not dozens.**

**Confidence:** Moderate. Hardware throughput benchmarks are well-sourced but are (i) for
DeepSeek-R1-class models, not 1–2 T frontier models, and (ii) reported with a recurring
per-GPU-vs-per-instance ambiguity that the industry itself is loose about — flagged throughout.
Users-per-node rests on token-consumption estimates that vary 10×+ by workload. The revenue and
node-count conclusions are order-of-magnitude planning figures, not forecasts.

---

## 1. Throughput per node — tokens/second for one NVL72-class rack

### 1.1 The benchmark data

The cleanest public numbers come from the **DeepSeek-V3/R1 (671 B-parameter MoE)** deployment on a
GB200 NVL72, optimized by SGLang/NVIDIA in 2025:

| Configuration | Prefill (input) tok/s | Decode (output) tok/s | Source |
|---|---|---|---|
| GB200 NVL72, FP8 attn + NVFP4 MoE | **26,156** | **13,386** | [LMSYS Part II](https://www.lmsys.org/blog/2025-09-25-gb200-part-2/) |
| GB200 NVL72, BF16 attn + FP8 MoE | 18,471 | 9,087 | [LMSYS Part II](https://www.lmsys.org/blog/2025-09-25-gb200-part-2/) |
| GB200 NVL72, earlier SGLang build | — | 7,583 | [LMSYS Part I](https://www.lmsys.org/blog/2025-06-16-gb200-part-1/), [InfoQ](https://www.infoq.com/news/2025/06/nvidia-gb200/) |

**A critical caveat — "per GPU" vs "per rack" vs "per instance."** LMSYS reports 26,156 / 13,386 as
**"per GPU"** figures. Taken literally, ×72 GPUs gives **~1.88 M tok/s prefill / ~0.96 M tok/s decode
per rack** ([LMSYS Part II](https://www.lmsys.org/blog/2025-09-25-gb200-part-2/)). However, these are
*disaggregated* prefill/decode runs where prefill and decode use *different* GPU pools, and the
"per GPU" normalization divides instance throughput by the GPUs in that instance — so the naive ×72
double-counts. The industry is loose about this; the honest reading is that a full NVL72 rack serving
a DeepSeek-R1-class model delivers, in a **throughput-optimized regime, on the order of ~0.5–1.0 M
output tok/s aggregate** — with ~1 M being optimistic and ~0.5 M conservative. NVIDIA's own
single-DGX-B200 (8-GPU) figure of **">30,000 tok/s max" on DeepSeek-R1**
([NVIDIA world-record blog](https://developer.nvidia.com/blog/nvidia-blackwell-delivers-world-record-deepseek-r1-inference-performance/))
scales to ~270,000 tok/s for a 72-GPU-equivalent — and an NVL72's coherent NVLink fabric does
*better* than 9× a DGX because of in-rack expert parallelism, supporting the ~0.5–1 M band.

### 1.2 The throughput–interactivity tradeoff (the regime that dominates the answer)

Aggregate throughput is **not a single number** — it trades against per-user speed. SemiAnalysis's
**InferenceMAX / InferenceX** benchmark frames this as a Pareto curve with three zones
([The Register — tokenomics](https://www.theregister.com/2026/03/07/ai_inference_economics/),
[NVIDIA InferenceMAX blog](https://blogs.nvidia.com/blog/blackwell-inferencemax-benchmark-results/)):

| Regime | Per-user speed | Aggregate rack throughput | Use case |
|---|---|---|---|
| **Bulk / batch** | ~10–50 tok/s/user | **Highest** (~0.8–1.0 M tok/s band) | Async, batch, document processing |
| **Goldilocks** | ~50–100 tok/s/user | Mid (~0.4–0.7 M tok/s) | Standard chat, most API traffic |
| **Premium / interactive** | ~200–1,000 tok/s/user | **Lowest** (~0.2–0.4 M tok/s) | Low-latency interactive, reasoning |

NVIDIA's InferenceMAX figures make the slope concrete: gpt-oss-120B (a *small* model) hits
**~60,000 tok/s/GPU at 1,000 tok/s/user**, but drops to **~30,000 tok/s/GPU** when speculative
decoding pushes interactivity — and Llama-3.3-70B does **">10,000 tok/s/GPU at 50 tok/s/user"**
([NVIDIA InferenceMAX blog](https://blogs.nvidia.com/blog/blackwell-inferencemax-benchmark-results/)).
Rack-scale NVL72/GB300 systems "maintain higher interactivity without compromising throughput"
versus 8-GPU boxes, which "run out of steam above ~50 tok/s/user"
([The Register](https://www.theregister.com/2026/03/07/ai_inference_economics/)). SemiAnalysis also
quotes **">3.5 M tok/s per megawatt"** at the bulk end — for a ~130 kW rack that is ~0.45 M tok/s,
consistent with the conservative side of the band once you account for a frontier model being heavier
than the benchmarked ones.

### 1.3 Frontier-model adjustment, context length, and the planning band

Three downward adjustments from the benchmark figures to a **1–2 T frontier model** in orbit:

1. **Model size.** Benchmarks are DeepSeek-R1-class (671 B total). A 1–2 T model has ~1.5–3× the
   total parameters and (depending on active-parameter count) more FLOPs/token. Decode throughput
   scales roughly inversely with active parameters — assume **~0.5–0.8× the benchmark rate**.
2. **Context length.** KV-cache pressure rises with context. The benchmarks use 2 K-token inputs;
   real agentic/long-context traffic (32 K–128 K) cuts the sustainable batch size and therefore
   aggregate throughput, often **2–4×** (`inference_scaling.md` §1: a single 70 B request at 128 K
   context is ~40 GB of KV cache).
3. **Reasoning / "thinking" tokens.** 2026 frontier models emit large hidden reasoning traces;
   effective *useful* output is a fraction of raw tokens generated.

**Planning band for one node (1–2 T frontier model):**

| Regime | Aggregate output tok/s per node | Notes |
|---|---|---|
| **Batch / async** | **~0.4–0.8 M tok/s** | Long-context async work; KV-cache-limited |
| **Standard chat** | **~0.2–0.5 M tok/s** | The realistic central case |
| **Interactive / reasoning** | **~0.1–0.25 M tok/s** | Premium low-latency tier |

**Central planning figure: ~0.3 M output tok/s per node** for a frontier model at a chat-grade SLA,
with a factor-of-2 either way depending on regime. (For context, this is also the regime where the
orbital downlink-bandwidth limit must be checked against token egress — see Open Questions and
`laser_comms/`.)

---

## 2. Users per node — translating throughput into population

Throughput → users requires a **token-consumption-per-user** assumption. These vary enormously by
workload ([iternal.ai token usage guide](https://iternal.ai/token-usage-guide),
[LeanOps — agents burn 50× more tokens](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/),
[Stanford Digital Economy Lab](https://digitaleconomy.stanford.edu/news/how-are-ai-agents-spending-your-tokens/)):

| Workload | Tokens/user/day | Tokens/task | Source |
|---|---|---|---|
| **Conversational / chat** | ~7,500–100,000 | ~500–5,000/session | [iternal.ai](https://iternal.ai/token-usage-guide) |
| **Coding assistant** | ~300,000–2,000,000 | ~10 K–3.5 M/task | [iternal.ai](https://iternal.ai/token-usage-guide) |
| **Agentic enterprise** | ~200,000–100,000,000 | ~10 K–1 M+/task | [iternal.ai](https://iternal.ai/token-usage-guide), [LeanOps](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/) |

Agentic tasks consume **5–30× more tokens than chat** ([LeanOps](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/));
Stanford finds agentic tasks "1000× more tokens than code chat" at the extreme
([Stanford](https://digitaleconomy.stanford.edu/news/how-are-ai-agents-spending-your-tokens/)).

### 2.1 Concurrent users per node

**Concurrent** = users actively generating tokens *right now*. At a chat-grade ~30–50 tok/s/user
target and a central node throughput of ~0.3 M tok/s:

- **Concurrent chat users ≈ 0.3 M ÷ 40 tok/s ≈ ~7,500**, with a plausible **~5,000–15,000** range
  depending on regime (more in batch, fewer in interactive).
- **Concurrent agentic users:** an agentic session sustains a higher effective token draw (tool
  loops, long context). Budgeting ~5–10× the per-user token rate of chat ⇒ **~750–3,000 concurrent
  agentic users** per node, call it **~1,000–3,000**.

### 2.2 Supported (registered) user population per node

Registered users vastly exceed concurrent users — typical consumer-app **peak-concurrency ratios are
~2–10% of daily-active, and DAU is a fraction of registered**. Combining a ~20–50× concurrency-to-
population multiplier:

| Workload | Concurrent users/node | Supported population/node (assumption-dependent) |
|---|---|---|
| **Chat** | ~5,000–15,000 | **~0.2–1.5 M** registered / ~50–300 K DAU |
| **Coding assistant** | ~2,000–6,000 | **~50–300 K** active developers |
| **Agentic enterprise** | ~1,000–3,000 | **~hundreds to a few thousand** always-on enterprise agents, or ~10–50 enterprise customers at moderate agent fleets |

**Assumptions stated explicitly:** 40 tok/s/user chat SLA; ~0.3 M tok/s central node throughput;
~25× concurrency-to-registered multiplier; agentic users draw ~5–10× chat token rate; ~85% node
duty cycle (eclipse/thermal); no downlink-bandwidth cap binding (flagged as open question). Move any
of these and the population shifts by 2–5×.

**Bottom line:** **One node is a mid-five-figure-concurrent-user / low-seven-figure-registered-user
service for chat, or a few-thousand-agent service for enterprise agentic work.** That is a real,
sellable service — comparable to a mid-size SaaS product's user base — but it is *not* hyperscale.

---

## 3. The 1-node and 2-node cases

### 3.1 What one single-rack node serves

A single NVL72-class node:
- **Holds and runs a complete 1–2 T frontier model** in FP8/FP4 with KV-cache headroom
  (`inference_scaling.md` §2 — confirmed).
- Delivers **~0.3 M output tok/s** central / ~0.1–0.8 M across regimes (§1).
- Serves **~5–15 K concurrent chat users** (~0.2–1.5 M registered) or **~1–3 K concurrent agentic
  users** (§2).
- Is **self-contained**: all bandwidth-heavy parallelism (TP, EP all-to-all) stays on in-rack NVLink;
  it needs no laser link to function (`multi_rack_inference.md` §2.4).
- Is a **single point of failure**: one fault (GPU, power, thermal, radiation upset) takes the entire
  service offline. There is no redundancy.

**A single node is a complete, commercially meaningful service technically — but operationally
fragile.** It is a viable *demonstrator / pilot*, not a viable *production service*.

### 3.2 What two laser-meshed nodes serve — and what meshing actually buys

Per `multi_rack_inference.md`, two single-rack satellites can be laser-linked and a model split across
them by **pipeline parallelism (PP)**. The key question: does meshing add **size** headroom,
**throughput**, or both?

**Meshing two nodes via PP primarily adds model-*size* headroom — not throughput.**

- **Size headroom (the real benefit):** PP across two nodes lets a model whose weights+KV genuinely
  overflow one rack — the projected **>~10–15 T-parameter** MoE generation NVIDIA is building Rubin
  Ultra NVL576 for (`multi_rack_inference.md` §1) — run as two laser-linked single-rack satellites.
  This is a *capability unlock*: without it, a too-big model cannot run at all on single-rack nodes.
- **Throughput — meshing actually *underperforms* two independent replicas.** A PP-split model pair
  shares one model instance: its aggregate throughput is bounded by the slower pipeline stage and is
  *reduced* by pipeline bubbles, the ISL-hop latency added to time-to-first-token, and PP's
  strong-scaling inefficiency (SGLang's cross-node chunked-PP reports ~82.8% strong-scaling
  efficiency at PP4×TP8 — i.e. a ~17% loss, and that is for an *optimized terrestrial* case)
  ([LMSYS chunked PP](https://www.lmsys.org/blog/2026-01-15-chunked-pipeline/),
  `multi_rack_inference.md` §2.2). So two PP-meshed nodes serving one frontier model deliver roughly
  **~1.5–1.8× one node's throughput**, whereas **two *independent replica* nodes deliver ~2.0×** with
  *no* inter-node bandwidth requirement (`multi_rack_inference.md` §2.4).

**Conclusion:** For *throughput scaling*, never mesh — add independent replica nodes. Mesh **only**
when a single model genuinely overflows one rack's HBM. For today's 1–2 T frontier models that does
not happen, so **the throughput-scaling axis is replica parallelism and the 2-node mesh is a
forward-looking capability, not a V1 necessity** (consistent with `multi_rack_inference.md` §6 and
`inference_scaling.md` §5: "scale by adding independent rack-replicas, not by splitting a model").

### 3.3 Two independent nodes (the more useful 2-node case)

Two **independent replica** nodes — each a full model copy — serve **~2× one node**: ~0.6 M tok/s
central, ~10–30 K concurrent chat users (~0.5–3 M registered), and — critically — give **N+1
redundancy**: if one node fails, the other still serves (at half capacity). This is the first
configuration that is **operationally viable as a production service**.

---

## 4. Minimum viable commercial deployment

Combine three requirements: (a) runs a frontier model, (b) serves a commercially meaningful user
base, (c) earns enough — at the project's revenue basis plus an orbital premium — to justify a
dedicated Neutron launch campaign.

### 4.1 The revenue basis per node

From `economics/revenue_per_watt.md`:
- A GB200 NVL72 rack grosses **~$5.6–14.5M/rack-year** at $756–1,944/hr and 85% utilization; central
  blended figure **~$8–10M/rack-year** (IaaS basis). The **~$8–16M/rack-year** band used here is the
  project's reconciled headline span: **~$8M/rack-yr** is the central gross IaaS figure
  (~$15–20B/GW-yr) and **~$16M/rack-yr** is the central gross **inference-service** figure
  (~$25–50B/GW-yr) — both from `economics/revenue_per_watt.md` §3 / the wave-4 synthesis revenue
  reconciliation. So the $16M top is the token-selling basis, not an unsourced number.
- Selling **frontier-model tokens** (API basis) rather than raw GPU-hours captures a **~1.5–2.5×
  model-value markup** — so a token-serving node could gross **~$15–30M/year** if it serves a
  competitive model and is well-utilized.
- An **orbital/latency or sovereignty premium** (the project's "premium value case") could add
  further upside — but orbital duty-cycle limits (eclipse, thermal) and a possible trailing GPU
  generation pull the other way. Net: treat **~$10–25M/year gross per node** as the planning band,
  central **~$12–16M/node-year**.

**Cross-check with throughput:** at frontier API pricing of **~$5–25 per 1 M output tokens**
([revenue_per_watt.md §4](../economics/revenue_per_watt.md)), a node doing ~0.3 M tok/s × 85% duty ×
3.15e7 s/yr ≈ **~8 trillion output tokens/year**. At a blended **~$2–3 / 1M tokens realized** (after
free tiers, input/output mix, discounts) that is **~$16–24M/year** — independently consistent with
the revenue-per-watt figure. The two methods agree at **~$10–25M/node-year**. *(This token-volume
arithmetic assumes no downlink-bandwidth cap on egress — flagged §6.)*

### 4.2 Is the minimum 1 node?

**On pure economics, yes — almost.** One node grosses ~$10–25M/year. A single dedicated Neutron
launch is on the order of ~$50–55M (per project Neutron docs), and the rack itself ~$3M. A
single-node service pays back the *rack* in well under a year and the *launch* in ~2–4 years of gross
revenue — not obviously disqualifying, but thin once orbital opex, depreciation, and replacement are
loaded.

**But one node fails requirement (b)/(c) as a *service*:** zero redundancy. A single radiation upset,
thermal excursion, or GPU failure ends the service and the revenue. No enterprise customer will sign
a production SLA against a single un-redundant orbital node. **One node is a pilot/demonstrator, not a
minimum viable commercial service.**

### 4.3 The realistic minimum: ~3–5 nodes

The minimum viable **commercial** deployment is the smallest count that is *both* economically
meaningful *and* operationally credible:

| Deployment | Runs frontier model? | Serves meaningful users? | Redundancy | Gross revenue/yr | Verdict |
|---|---|---|---|---|---|
| **1 node** | Yes | ~0.2–1.5 M users | **None** | ~$10–25M | Pilot only — SPOF |
| **2 nodes (replicas)** | Yes | ~0.5–3 M users | N+1 (degraded) | ~$20–50M | Minimum *technically* viable |
| **3–5 nodes** | Yes | ~1–7 M users | N+1 with margin; rolling maintenance | **~$30–100M** | **Minimum viable commercial deployment** |
| **~10+ nodes** | Yes | ~5–15 M+ users | Full | ~$120M+ | Scaled service |

**The minimum viable commercial deployment is ~3–5 nodes.** Rationale:

1. **Frontier model:** satisfied at 1 node; trivially at 3–5.
2. **Meaningful user base:** 3–5 replica nodes serve **~1–7 M registered chat users** or a few
   thousand enterprise agentic seats — a real, defensible mid-market service.
3. **Revenue justifies a launch campaign:** **~$30–100M/year gross** against a launch campaign of a
   few Neutron flights (~$150–250M) — payback in ~2–4 years on gross, and the campaign amortizes
   fixed costs (ground stations, ops, software) that one node cannot.
4. **Operational credibility:** 3–5 nodes give N+1 redundancy *with margin* — one node can fail or
   go down for any reason and the service continues at >75% capacity, enabling a real SLA. This is
   the gate that 1–2 nodes fail.
5. **It is one coherent launch campaign.** Each node is one single-rack Neutron payload
   (`node_mass_model.md`); 3–5 nodes is 3–5 launches — a single procurement and a single
   build-to-learn batch, not an open-ended program.

Note these are **independent replicas**, not a mesh. Meshing (§3.2) enters only if/when a frontier
model overflows one rack — a V2+ contingency, not part of the minimum viable deployment.

---

## 5. Implication for the strategy

1. **V1 deployment size: a handful of nodes (~3–6), not one.** A single node is the right *first
   flight* (a demonstrator that proves the rack, thermal, power, and radiation case in orbit) — but
   the minimum viable *commercial* V1 is **~3–5 replica nodes**. This is the smallest deployment that
   can carry a production SLA and gross **~$30–100M/year**. Plan the V1 campaign as **one
   demonstrator node followed quickly by a 3–5-node commercial batch**, all single-rack Neutron
   payloads.

2. **Scale by replicas, not by meshing.** Throughput and user growth come from adding independent
   single-rack replica nodes — near-linear, no inter-node bandwidth needed, fault-isolated
   (`inference_scaling.md` §5). Laser-meshing two nodes is reserved for the *capability* case (a
   model too big for one rack), not the *scaling* case. The build-to-learn ramp is therefore a
   **replica-count ramp**: 1 → 3–5 → 10+ identical nodes.

3. **The ramp is naturally incremental and low-risk.** Because every node is an identical,
   self-contained single-rack unit, the constellation can grow one launch at a time, each node
   earning from day one, each launch feeding lessons (radiation, thermal, degradation) into the next
   batch. There is no "big bang" minimum — but there *is* a credibility floor at ~3–5 nodes below
   which the service cannot be sold as production.

4. **Watch the binding constraints, not the model-fit.** "Can it run a frontier model" is settled
   (yes, one rack). The real V1 sizing constraints are: (i) **redundancy** — drives the floor to 3–5
   nodes; (ii) **downlink bandwidth** — token egress for ~0.3 M tok/s/node must fit the laser/RF
   downlink budget (see `laser_comms/`); (iii) **duty cycle** — eclipse/thermal cuts effective
   throughput and revenue ~10–20%; (iv) **GPU-generation drift** — an orbital node may fly a trailing
   generation, discounting revenue-per-node vs terrestrial. These, not model size, determine whether
   the minimum viable deployment clears the bar.

5. **Framing for the business case.** Pitch V1 as "a **~$30–100M/year**, ~1–7 M-user frontier-
   inference service on **3–5 orbital nodes**, expandable replica-by-replica" — a concrete,
   mid-market-scale, redundant service — rather than "one rack that can run a frontier model," which
   is true but not investable.

---

## Sources

Throughput benchmarks (NVL72 / Blackwell inference):
- [LMSYS — Deploying DeepSeek on GB200 NVL72, Part II (3.8× prefill, 4.8× decode)](https://www.lmsys.org/blog/2025-09-25-gb200-part-2/)
- [LMSYS — Deploying DeepSeek on GB200 NVL72, Part I (2.7× decode)](https://www.lmsys.org/blog/2025-06-16-gb200-part-1/)
- [InfoQ — Nvidia GB200 NVL72 2.7× faster inference on DeepSeek V3](https://www.infoq.com/news/2025/06/nvidia-gb200/)
- [NVIDIA — Blackwell Delivers World-Record DeepSeek-R1 Inference Performance](https://developer.nvidia.com/blog/nvidia-blackwell-delivers-world-record-deepseek-r1-inference-performance/)
- [NVIDIA — Blackwell Raises Bar in InferenceMAX Benchmarks](https://blogs.nvidia.com/blog/blackwell-inferencemax-benchmark-results/)
- [NVIDIA — Blackwell Ultra Sets New Inference Records in MLPerf](https://developer.nvidia.com/blog/nvidia-blackwell-ultra-sets-new-inference-records-in-mlperf-debut/)
- [The Register — the deceptively simple science of tokenomics](https://www.theregister.com/2026/03/07/ai_inference_economics/)
- [SemiAnalysis — InferenceX v2: NVIDIA Blackwell vs AMD vs Hopper](https://newsletter.semianalysis.com/p/inferencex-v2-nvidia-blackwell-vs)
- [LMSYS — Chunked Pipeline Parallelism in SGLang](https://www.lmsys.org/blog/2026-01-15-chunked-pipeline/)

Token consumption / users per workload:
- [iternal.ai — AI Token Usage Guide (2026), 10 use-case cost profiles](https://iternal.ai/token-usage-guide)
- [LeanOps — AI Agents Burn 50× More Tokens Than Chats](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/)
- [Stanford Digital Economy Lab — How are AI agents spending your tokens?](https://digitaleconomy.stanford.edu/news/how-are-ai-agents-spending-your-tokens/)
- [TechAhead — The Inference Cost Trap: AI Agent Economics at Scale](https://www.techaheadcorp.com/blog/inference-cost-explosion/)

Revenue / economics:
- [revenue_per_watt.md (project doc)](../economics/revenue_per_watt.md)
- [GB200 NVL72 guide & pricing — Spheron](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/)

(See also project docs: `llm_compute/inference_scaling.md`, `llm_compute/multi_rack_inference.md`,
`economics/revenue_per_watt.md`, `node_design/node_mass_model.md`,
`node_design/reliability_failure_handling.md`.)

---

## Open questions / uncertainties

1. **Per-GPU vs per-instance vs per-rack ambiguity in the benchmarks.** LMSYS's 26,156/13,386 tok/s
   are labeled "per GPU"; naive ×72 over-counts because prefill/decode are disaggregated across
   different GPU pools. The ~0.5–1.0 M tok/s/rack band here is a reasoned reconciliation, not a
   directly published figure. A dedicated benchmark of a *full NVL72 rack serving one model
   end-to-end* would tighten this 2× uncertainty.
2. **No public benchmark for a 1–2 T frontier model on NVL72.** All hard numbers are DeepSeek-R1
   (671 B) or smaller (gpt-oss-120B, Llama-70B). The frontier-model down-adjustment (~0.5–0.8×) is an
   estimate. Closed frontier models publish neither parameter counts nor throughput.
3. **Token-consumption-per-user varies 10×+.** Chat vs coding vs agentic span ~7.5 K to ~100 M
   tokens/user/day. The users-per-node figures are therefore order-of-magnitude and highly
   workload-sensitive. The agentic case in particular could be 3–5× worse than modeled.
4. **Concurrency-to-registered multiplier is assumed (~25×).** Real ratios depend on the customer
   mix (consumer chat vs always-on enterprise agents); a B2B agentic service has a much lower
   multiplier than a consumer chat app.
5. **Downlink-bandwidth cap on token egress is not modeled here.** ~0.3 M tok/s/node of output must
   physically reach the ground. Whether the laser/RF downlink budget supports this for 3–5
   simultaneous nodes is a `laser_comms/` question that could lower realized throughput/revenue.
6. **Duty cycle and GPU-generation discount.** Eclipse/thermal duty-cycle (~10–20% haircut) and a
   possible trailing GPU generation in orbit both reduce revenue-per-node below the terrestrial
   benchmark; neither is fully quantified here.
7. **Where exactly is the redundancy floor — 3, 4, or 5 nodes?** This depends on the per-node failure
   rate and required SLA, which belong to `node_design/reliability_failure_handling.md`. "3–5" is a
   planning band; a reliability model would pin it.
