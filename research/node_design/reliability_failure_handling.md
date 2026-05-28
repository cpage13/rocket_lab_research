# Hardware Reliability & Failure Handling for an Un-Serviceable Orbital Compute Node

*Project: RKLB Space Data Center — feasibility phase. Document date: May 2026.*
*Author: research agent. Hard numbers cross-checked against ≥2 independent sources where possible; estimates explicitly flagged.*

---

> **Source status (2026-05-25):** See [SOURCE_INDEX.md](../SOURCE_INDEX.md) claim IDs THR-008 through THR-010. The **7–9% GPU AFR** is a planning estimate inferred from public interruption and failure analyses, not a vendor-certified permanent AFR. The **5-year GPU service life** is a project design target/scenario. The earlier **1–2 day burn-in catches ~90%** idea is not source-certified; credible space-acceptance screening should be planned as roughly **1–3 weeks** or at least **100–200+ hours**, depending on mission risk.

## Summary & Verdict

This document tests the founder's hypothesis: that GPU failure on an un-serviceable orbital node is a *solvable* problem — solved by building a space-qualified rack, running a ~1–2 day ground burn-in / stress test to catch ~90% of infant-mortality failures, and then accepting the residual in-orbit attrition.

**Verdict: the model is directionally sound but the founder's numbers are too optimistic on two points, and the real lever is graceful degradation, not burn-in.**

1. **In-service GPU failure is the dominant risk, not infant mortality.** The best public data — Meta's Llama-3 405B run — implies an **annualized GPU failure rate (AFR) of ~7–9%** ([Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/faulty-nvidia-h100-gpus-and-hbm3-memory-caused-half-of-the-failures-during-llama-3-training-one-failure-every-three-hours-for-metas-16384-gpu-training-cluster), [Jason Hoffman analysis](https://fullhoffman.com/2026/03/21/gpu-failure-rates/)). That failure rate is **mostly *constant-rate* random failure** (the flat bottom of the bathtub), which burn-in *cannot* remove. Burn-in only attacks the early-life hump.

2. **Ground burn-in is real and worth doing, but a 1–2 day test catches a *minority*, not ~90%, of lifetime infant-mortality defects.** Proper aerospace acceptance burn-in is **~200–500+ hours (≈8–21 days)**, not 1–2 days ([MIL-STD-1540E / Aerospace Corp guidance](https://s3vi.ndc.nasa.gov/ssri-kb/static/resources/TR-2021-00283%20-%20Thermal%20Test%20Tailoring%20Guidelines%20for%20Class%20C%20and%20D%20Space%20Programs.pdf)). A 1–2 day system stress test realistically removes the *worst* infant-mortality defects — gross workmanship errors, dead-on-arrival GPUs, bad solder, weak HBM stacks — but the founder should plan for **a longer burn-in (1–3 weeks) to credibly claim ~80–90% infant-mortality capture.** This is a schedule/cost adjustment, not a showstopper.

3. **The node will lose GPUs in orbit and that is acceptable *if and only if* the architecture degrades gracefully.** Realistic planning numbers for an orbital node over a 3-year life: expect to **lose ~15–25% of GPUs cumulatively** (≈7–9%/yr compounding, possibly lower in benign SSO radiation, possibly higher from launch-vibration latent damage and the impossibility of physical repair). The design must therefore treat the rack as a **pool of compute that shrinks over time**, not an all-or-nothing unit.

4. **The single biggest design risk is NVLink topology coupling.** In a stock NVL72, one failed GPU can destabilize the whole rack, and degraded operation costs ~15–20% throughput per lost GPU ([Introl](https://introl.com/blog/gb200-nvl72-deployment-72-gpu-liquid-cooled)). Terrestrial hyperscalers "solve" this by swapping in a *spare rack* — an option an orbital node does not have. The space-qualified rack **must be re-architected for partition-and-isolate fault domains** so a dead GPU degrades capacity proportionally (~1.4% per GPU) instead of crashing the node.

**Bottom line:** The founder is right that GPU failure is *manageable*. They are wrong that *ground burn-in* is the thing that manages it. Burn-in offsets the early-life hump (a real but modest slice of lifetime failures); **graceful degradation + redundancy + derating** is what makes the residual ~15–25% GPU attrition survivable. Plan the node around "end-of-life at ~75–85% of beginning-of-life compute," and the model holds. **Confidence: medium-high on terrestrial AFR, medium on the space-specific delta, medium-high on the qualitative verdict.**

---

## 1. GPU / accelerator failure rates in large terrestrial AI clusters

The most-cited hard dataset is **Meta's Llama-3 405B training run** (published in the Llama-3 technical report, Table 5; widely reported July 2024):

- Cluster: **16,384 × NVIDIA H100** (80 GB), 54-day pre-training snapshot.
- **419 unexpected interruptions** — averaging **one every ~3 hours** ([Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/faulty-nvidia-h100-gpus-and-hbm3-memory-caused-half-of-the-failures-during-llama-3-training-one-failure-every-three-hours-for-metas-16384-gpu-training-cluster), [Data Center Dynamics](https://www.datacenterdynamics.com/en/news/meta-report-details-hundreds-of-gpu-and-hbm3-related-interruptions-to-llama-3-training-run/)).
- **~78%** of interruptions were confirmed/suspected hardware. GPU issues (incl. NVLink) = **30.1% (148 events)**; HBM3 memory = **17.2% (72 events)**. Combined, **GPU-or-HBM ≈ 58.7%** of all interruptions ([Data Center Dynamics](https://www.datacenterdynamics.com/en/news/meta-report-details-hundreds-of-gpu-and-hbm3-related-interruptions-to-llama-3-training-run/)).
- For contrast: **only 2 CPU failures** in 54 days — GPUs are ~2 orders of magnitude more failure-prone than CPUs in this workload, because of their ~700 W draw and thermal stress.

**Important distinction (confirmed):** an "interruption" is not the same as a *destroyed* GPU. Many interruptions are transient (recoverable with a reboot/checkpoint restore); only a fraction require physically swapping a GPU. So 419 interruptions ≠ 419 dead GPUs.

**Annualized failure rate (AFR).** Multiple independent analyses converge on **~7–9% AFR for *permanent* data-center GPU failure**:
- A widely-circulated industry analysis derives **~9%/yr** from the Llama-3 data, with **cumulative failure risk >25% over 3 years** ([Jason Hoffman, "GPU Failure Rates"](https://fullhoffman.com/2026/03/21/gpu-failure-rates/)).
- A peer-style study of GPU failure modes in AI clusters reports failure rates in a comparable band ([SARC, "GPU Reliability in AI Clusters"](https://sarcouncil.com/download-article/SJECS-97-2025-298-306.pdf)).
- A Google architect (reported by Tom's Hardware / TrendForce) put practical **data-center GPU service life at only 1–3 years** — consistent with single-digit annual attrition compounding into a meaningful fraction over 3 years ([Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/datacenter-gpu-service-life-can-be-surprisingly-short-only-one-to-three-years-is-expected-according-to-unnamed-google-architect), [TrendForce](https://www.trendforce.com/news/2024/10/31/news-datacenter-gpus-may-have-an-astonishingly-short-lifespan-of-only-1-to-3-years/)).

**Planning figure: ~7–9% GPU AFR for permanent failure.** *Confidence: medium-high.* The number is an inference from one large public dataset plus consistent secondary analyses; vendors do not publish official AFRs. It likely *understates* a space node (no repair, launch-induced latent damage) and the harsh duty cycle of 24/7 inference.

**Scale intuition:** in a cluster of thousands, "rare" becomes "constant." Meta's 16K cluster MTTF ≈ 1.8 h; a 131K-GPU cluster MTTF ≈ 14 minutes ([Jason Hoffman](https://fullhoffman.com/2026/03/21/gpu-failure-rates/)). A single orbital node of **72–144 GPUs** is far smaller — at 8% AFR, expect **~6–12 GPU losses per node per year** as a *planning mean*.

---

## 2. The bathtub curve & infant mortality — the crux of the burn-in argument

Electronic-component failure rate over life follows the classic **bathtub curve**: a decreasing-rate **infant-mortality** region, a flat **useful-life** (constant random rate) region, and a rising **wear-out** region ([NIST Engineering Statistics Handbook](https://www.itl.nist.gov/div898/handbook/apr/section1/apr124.htm), [Wikipedia: Bathtub curve](https://en.wikipedia.org/wiki/Bathtub_curve)).

What fraction of failures is infant mortality? **There is no single universal number — it depends entirely on manufacturing quality and screening.** But the literature supports these anchors:

- Infant mortality is caused by **manufacturing defects, assembly errors, weak solder joints, contamination, marginal components** — i.e. *quality escapes*, not random physics ([KES Systems](https://www.kessystemsinc.com/resources/semiconductor-101-the-bathtub-curve/)).
- For *new, complex* systems the early-life slice can be large: one reliability source states **"up to half of all chip-and-wire failures happen within a new system's first few weeks"** ([No MTBF / reliability literature](https://nomtbf.com/2013/06/finding-and-eliminating-early-life-failures-where-the-money-is/)).
- The infant-mortality *period* itself is not a fixed window — "could be the first 30 days or the first 18 months" — it is defined as the time over which failure rate is *decreasing* ([No MTBF](https://nomtbf.com/2013/06/finding-and-eliminating-early-life-failures-where-the-money-is/)).

**The crux for the founder's argument:** burn-in only attacks the *infant-mortality hump*. It does **nothing** for the flat useful-life region — and the ~7–9% GPU AFR observed in mature clusters (Meta's run was *not* on brand-new hardware) is dominated by **constant-rate random failure**: thermal-cycling fatigue, HBM wear, power-cycling stress, electromigration. **Burn-in cannot remove that.** It is the bottom of the tub, by definition.

So: **infant mortality is a real, sizeable slice of *early-life* failures (plausibly 30–50% of failures in the first weeks–months), but it is a *small* slice of the failures accumulated over a 2–3 year life.** Burn-in shifts the curve down at the start; it does not flatten the tub. *Confidence: medium — the concept is rock-solid, the exact split is application-specific and not precisely published for AI GPUs.*

---

## 3. Burn-in / stress-testing effectiveness — does a 1–2 day test catch ~90%?

**What burn-in does (confirmed):** subjects parts/assemblies to elevated temperature, voltage and load to *accelerate* infant-mortality mechanisms so weak units fail on the line, not in the field ([KES Systems](https://www.kessystemsinc.com/resources/an-introduction-to-semiconductor-burn-in/), [Wikipedia: Burn-in](https://en.wikipedia.org/wiki/Burn-in)). It is the standard, effective tool for the job.

**How long, in practice (confirmed, cross-checked):**

| Application class | Typical burn-in | Source |
|---|---|---|
| Consumer electronics | 24–48 h @ 85–105 °C | [PCBSync / industry guides](https://pcbsync.com/burn-in-testing/) |
| Industrial / automotive | 48–168 h @ 125 °C | [PCBSync](https://pcbsync.com/burn-in-testing/) |
| Military / aerospace | **168–500+ h** (≈1–3 weeks) | [PCBSync](https://pcbsync.com/burn-in-testing/) |
| Spacecraft electronic units (MIL-STD-1540E acceptance) | **Total thermal test ≥ 200 h**, made up of ~10 thermal cycles + 4 thermal-vacuum cycles, with **burn-in added to reach the 200 h floor** | [Aerospace Corp / NASA SSRI thermal-test guidance](https://s3vi.ndc.nasa.gov/ssri-kb/static/resources/TR-2021-00283%20-%20Thermal%20Test%20Tailoring%20Guidelines%20for%20Class%20C%20and%20D%20Space%20Programs.pdf), [NASA SSRI Burn-In topic](https://s3vi.ndc.nasa.gov/ssri-kb/topics/47/) |

**This directly contradicts the founder's "1–2 day" figure.** Proper *space acceptance* burn-in is **~200 hours minimum (~8+ days)**, and military/aerospace electronics commonly see **1–3 weeks**. The optimal burn-in duration is set by analyzing failure data — it must be long enough for the failure rate to drop to the flat useful-life floor ([PCBSync](https://pcbsync.com/burn-in-testing/)).

**Does a short test catch "most" infant mortality?** Partially. A 1–2 day system stress test *will* catch the gross, fast-acting defects — dead GPUs, bad HBM stacks, bad solder joints, workmanship errors, marginal power components under load. These are the highest-hazard-rate units and they fail *first* ([electrontest.com](https://www.electrontest.com/burn-in-testing/)). But a documented reliability study found that even a structured burn-in of a sample raised reliability from **0.55 → 0.76 — i.e. roughly halved field failures, not eliminated 90% of them** ([anyPCBA / reliability study summary](https://www.anypcba.com/blogs/practical-engineering/burn-in-testing-weeding-out-infant-mortality-in-electronic-devices.html)). A "~90% capture" claim requires a *full-duration* burn-in (≥1–2 weeks), not 1–2 days.

**Beyond burn-in, space qualification also requires ("shake and bake"):**
- **Vibration / acoustic / shock testing** to launch levels — to surface latent mechanical defects and connector issues *before* flight.
- **Thermal-vacuum (TVAC) cycling** — operating the hardware in vacuum across its temperature extremes; this both screens workmanship and validates the thermal design.
- These are *acceptance* tests on the flight unit itself, distinct from one-time *qualification* tests on a representative unit.

**Practical recommendation:** the founder's "manufacturing-line burn-in" instinct is correct and valuable — but budget **~1–3 weeks** of integrated rack-level stress + TVAC + vibration, not 1–2 days, if the goal is to credibly retire most infant-mortality risk. This is a schedule/throughput cost, not a feasibility blocker. *Confidence: medium-high (durations are from standards and cross-checked); the exact % capture for AI racks specifically is an estimate.*

---

## 4. Space-specific failure modes — which dominate

| Failure mode | Severity for this node | Notes |
|---|---|---|
| **Launch vibration / shock** | **HIGH (one-time, pre-burn-in-able)** | Intense vibration during ascent mechanically stresses every board, connector, solder joint, HBM stack and the heavy NVLink copper spine. This is the *most under-appreciated* risk: it can induce **latent damage** that only manifests weeks into orbit — *after* the ground burn-in. Mitigation: vibration-test the flight rack to launch levels, potting/staking of heavy components, and ideally a *post-vibration* functional re-test. |
| **Thermal cycling** | **HIGH (recurring)** | In LEO the node passes in/out of eclipse ~15×/day → ~16,000 cycles over 3 years. Differential expansion fatigues solder joints and HBM interconnects — a *primary* driver of the constant-rate failures burn-in cannot remove. The orbital node's *internal* thermal design (radiators, coolant) must minimize the swing seen by silicon. |
| **Coolant-loop reliability** | **HIGH (single-point-of-failure risk)** | An NVL72 dumps ~120–135 kW; ~90% via liquid. A pump or CDU failure → thermal shutdown of the whole rack within seconds. Terrestrial best practice is **N+1 pumps / dual-loop CDUs with isolation** ([Data Centre Magazine](https://datacentremagazine.com/news/choosing-the-right-cooling-pumps-for-next-gen-data-centres), [ASME failure analysis of DLC](https://asmedigitalcollection.asme.org/electronicpackaging/article/140/2/020902/367988/Failure-Analysis-of-Direct-Liquid-Cooling-System)). A representative AI-server cooling pump MTBF is ~30,000 h (~3.4 yr) — *not enough margin for an un-serviceable 3-year mission without redundancy*. **The coolant loop, not the GPUs, is the most likely whole-node killer.** |
| **Radiation — SEU (soft, recoverable)** | LOW–MEDIUM | Single-event upsets flip bits; handled by ECC on HBM, parity, watchdogs, scrubbing. Recoverable. Prior project research found **~500–600 km SSO radiation relatively benign** — consistent with SEU being a manageable nuisance, not a node-killer. |
| **Radiation — SEL (latch-up, destructive)** | LOW–MEDIUM | A single ion can trigger a parasitic CMOS thyristor → short from power to ground → thermal runaway and *permanent* destruction ([Wikipedia: SEU](https://en.wikipedia.org/wiki/Single-event_upset), [doEEEt: SEL protection](https://www.doeeet.com/content/eee-components/passives/single-event-latchup-protection-circuits/)). Commercial GPUs are *not* SEL-hardened. Mitigation: per-domain current-limiting / fast power-cycling latch-up protection circuits. In benign SSO this is a tail risk, but a *non-zero permanent-loss* mechanism the design must bound. |
| **No human repair** | STRUCTURAL | Removes the terrestrial escape hatch (swap the rack). Forces every other choice: redundancy, derating, graceful degradation. |

**Which dominates?** For *permanent capacity loss* on this node, the ranking is roughly: **(1) coolant-loop / power single-point failures** (can kill the whole node — must be redundant), **(2) thermal-cycling fatigue + ordinary in-service GPU/HBM attrition** (the steady ~7–9% AFR grind), **(3) launch-induced latent damage**, **(4) radiation SEL** (tail risk in benign SSO). SEU is loud but recoverable. Note prior project research that SSO radiation at ~500–600 km is fairly benign — this is *good news* and means radiation is **not** the dominant mode; terrestrial-style attrition and thermal/cooling are.

---

## 5. Redundancy & graceful degradation — does the node degrade gracefully?

**The problem with a stock NVL72.** All 72 GPUs are lashed into one tightly-coupled NVLink domain. In the as-shipped architecture, **one failed GPU can destabilize the entire rack**, and NVIDIA's automatic NVLink re-routing leaves a **~15–20% throughput penalty *per* failed GPU** ([Introl: GB200 NVL72 deployment](https://introl.com/blog/gb200-nvl72-deployment-72-gpu-liquid-cooled)). Terrestrial operators therefore **do not run degraded NVL72s** — they keep **spare racks** and swap ([Introl](https://introl.com/blog/gb200-nvl72-deployment-72-gpu-liquid-cooled), [NVIDIA DGX GB200 NVL72 release notes](https://docs.nvidia.com/dgx/dgxgb200nvl72-release-notes/known-issues.html)). **An orbital node cannot swap racks.** This is the central architectural finding of this document.

**Can it route around a dead GPU and keep serving?** Yes — *if* the node is designed for it:
- For **inference** (this project's workload), the model is *replicated*, not monolithically trained. The natural fault domain is **the smallest GPU group that holds one model replica** (e.g. 4–8 GPUs for a tensor-parallel shard). If the node is partitioned into many independent inference partitions, a dead GPU kills *one partition*, and the scheduler simply stops routing requests to it. Capacity drops by ~1/72 (~1.4%), not by 15–20% or 100%.
- This requires deliberate design: **multiple smaller NVLink/fault domains** instead of one 72-way domain, partition-level power and (ideally) coolant isolation, and a control plane that health-checks GPUs and reshapes the serving pool.
- Inference is *far* more forgiving than training here — no global synchronization barrier, no checkpoint-restart, replicas are independent.

**Graceful-degradation projection (orbital node, 72–144 GPUs, 3-year life).** Treating GPU loss as ~7–9%/yr compounding random attrition:

| End of year | Surviving GPUs (8% AFR mean) | Surviving compute |
|---|---|---|
| Launch (BOL) | 100% | 100% |
| Year 1 | ~92% | ~92% |
| Year 2 | ~85% | ~85% |
| Year 3 (EOL) | **~78%** | **~78%** |

Range across assumptions: **~70% (pessimistic, ~10%/yr + launch latent damage) to ~85% (optimistic, ~5%/yr in benign SSO with good burn-in).** *These are model outputs on a stated AFR assumption — flagged as estimate, not measured.* The key point: **with a partitioned architecture, this is a smooth glide from 100% → ~75–80% capacity, not a cliff.** That is an *acceptable* degradation profile for an inference node — provided the business model is sized for end-of-life capacity, not beginning-of-life.

**Caveat:** the table assumes GPU losses are *independent* and that no shared subsystem (coolant, power, NVLink spine) takes the node down wholesale. Those shared subsystems are the real cliff risk and must be redundant (see §6).

---

## 6. How satellites handle un-serviceable hardware — and what it implies

Spacecraft have always been un-serviceable; the discipline is mature. Core techniques ([NASA Preferred Reliability Practices](https://extapps.ksc.nasa.gov/reliability/Documents/Preferred_Practices/1319.pdf), [Aerospace Corp fault-management guidelines](https://aerospace.org/sites/default/files/maiw/TOR-2009(8591)-14.pdf), [Siewiorek, Fault-Tolerant Architectures for Space](https://www.cs.unc.edu/~anderson/teach/comp790/papers/Siewiorek_Fault_Tol.pdf)):

- **Block redundancy** — fly two (or more) of critical units; switch to the spare on failure. Standard for un-serviceable, zero-maintenance missions where >1 failure is expected.
- **Cross-strapping** — let either string's units interconnect with either string's downstream units, so a mixed set of survivors still forms a working chain. *Caveat from the literature:* cross-strapping can **propagate** failures — a failed unit can over-stress everything it is strapped to — so fault-isolation barriers are essential ([RAMS 2017: propagating failure modes in cross-strapped systems](https://ieeexplore.ieee.org/document/7889674/)).
- **Derating** — operate components well below rated voltage/current/temperature so stress, and thus failure rate, drops. Cheap reliability with no part-count penalty.
- **Graceful degradation / fault containment** — partition the system so a failure degrades capability rather than ending the mission; isolate fault domains to stop propagation.
- **Design verification for single-point failures and "sneak paths"** — explicitly hunt for places where redundancy is silently defeated.
- A relevant counterpoint: a CubeSat reliability study found **better testing/screening can beat adding redundancy** on a mass budget ([ScienceDirect: CubeSat reliability](https://www.sciencedirect.com/science/article/pii/S0951832021007584)) — i.e. burn-in *and* redundancy both matter; spend where the mass is cheapest.

**Implications for the orbital rack design:**
1. **Make the GPUs the graceful-degradation layer** (many independent inference partitions) and the **shared subsystems the block-redundant layer.**
2. **Coolant loop: N+1 pumps, dual-loop / isolatable CDU.** This is the most likely whole-node killer and *must not* be single-string.
3. **Power: redundant power shelves (NVL72 already ships N+N), redundant DC distribution, per-partition isolation** so a power fault drops one partition, not the rack.
4. **Derate aggressively.** A space node is not chasing peak terrestrial clock; running GPUs/HBM cooler and at lower voltage trades a few % of FLOPS for a materially lower AFR — an excellent trade when repair is impossible.
5. **Add SEL latch-up protection** (per-domain fast current-limit/power-cycle) since commercial GPUs are not SEL-hard.
6. **Avoid cross-strapping the NVLink fabric into one giant domain** — that re-creates the "one GPU kills the rack" problem. Prefer many isolated domains.
7. **Carry cold spares where mass allows** — e.g. a small number of unpowered spare GPUs/trays the control plane can bring online. Mass-budget dependent (see node_mass_model.md).

---

## 7. Verdict — is the founder's model sound?

**The hypothesis, restated:** space-qualified rack + ~1–2 day ground burn-in catching ~90% of infant mortality + accept residual in-orbit attrition.

**Assessment, point by point:**

| Founder's claim | Verdict | Correction |
|---|---|---|
| Don't launch off-the-shelf GPUs; build a space-qualified rack | **Correct** | Space-qualification (vibration, TVAC, SEL protection, derating) is mandatory and standard practice. |
| Ground burn-in catches the bulk of early failures cheaply | **Correct in principle** | Burn-in is the right tool and is far cheaper on the ground. Do it. |
| A ~1–2 day stress test catches ~90% of infant mortality | **Too optimistic** | Aerospace acceptance burn-in is ~200–500 h (~1–3 weeks). 1–2 days catches the *gross* defects (~50%-ish field-failure reduction per the literature), not ~90%. **Budget 1–3 weeks of integrated rack burn-in + TVAC + vibration.** |
| In-orbit failures still happen but are offset by burn-in | **Partially wrong framing** | Burn-in offsets the *infant-mortality hump*. The dominant in-orbit loss is *constant-rate* attrition (~7–9% AFR) that burn-in **cannot** touch. What "offsets" it is **graceful degradation + redundancy**, not burn-in. |
| GPU failure is a solvable problem | **Correct — with the right architecture** | Solvable, but the solution is *architectural* (partitioned fault domains, redundant cooling/power, derating), not just *procedural* (burn-in). |

**What failure rate should the orbital node plan for?**
- **GPU permanent failure: ~7–9% AFR** (terrestrial-derived), → **cumulative ~20–25% GPU loss over 3 years** as a planning mean. Possibly as low as ~15% with benign SSO radiation, good derating and thorough burn-in; possibly higher with launch-induced latent damage.
- **End-of-life compute: plan for ~75–85% of beginning-of-life** capacity, degrading smoothly.
- **Whole-node loss** is driven not by GPUs but by **shared subsystems** (coolant, power, NVLink-domain coupling). With N+1 cooling, redundant power and partitioned fabric, whole-node loss should be a low-single-digit-percent tail risk over 3 years; **without** that redundancy it is the dominant risk and the node could die early from one pump.

**Does graceful degradation make it acceptable? Yes — conditionally.** A partitioned inference node that glides from 100% → ~78% capacity over 3 years is a perfectly viable product, *if* the unit economics are underwritten against ~80% average lifetime capacity and *if* the shared subsystems are redundant enough that the node does not die wholesale. The un-serviceability is real but it is exactly the problem satellites have solved for 60 years — with redundancy, derating and fault containment, not with field repair.

**Final verdict: the founder's model is SOUND in spirit and ~80% right in detail.** Two corrections: (1) burn-in must be ~1–3 weeks, not 1–2 days, to back the "catch most infant mortality" claim; (2) the thing that makes residual attrition *acceptable* is graceful degradation and subsystem redundancy, not burn-in — burn-in only shaves the early-life hump. Design the rack as a *partitioned, redundantly-cooled pool of compute that shrinks gracefully*, size the business for end-of-life capacity, and the un-serviceable orbital node is a tractable engineering problem. **Confidence: medium-high.**

---

## Sources

- [Tom's Hardware — Faulty H100 GPUs and HBM3 caused half of Llama-3 training failures](https://www.tomshardware.com/tech-industry/artificial-intelligence/faulty-nvidia-h100-gpus-and-hbm3-memory-caused-half-of-the-failures-during-llama-3-training-one-failure-every-three-hours-for-metas-16384-gpu-training-cluster)
- [Data Center Dynamics — Meta report: hundreds of GPU/HBM3 interruptions in Llama-3 training](https://www.datacenterdynamics.com/en/news/meta-report-details-hundreds-of-gpu-and-hbm3-related-interruptions-to-llama-3-training-run/)
- [Jason A. Hoffman — GPU Failure Rates and the Vocabulary Problem (2026)](https://fullhoffman.com/2026/03/21/gpu-failure-rates/)
- [SARC — GPU Reliability in AI Clusters: A Study of Failure Modes (2025)](https://sarcouncil.com/download-article/SJECS-97-2025-298-306.pdf)
- [Tom's Hardware — Datacenter GPU service life only 1–3 years (Google architect)](https://www.tomshardware.com/pc-components/gpus/datacenter-gpu-service-life-can-be-surprisingly-short-only-one-to-three-years-is-expected-according-to-unnamed-google-architect)
- [TrendForce — Datacenter GPUs may have a 1–3 year lifespan](https://www.trendforce.com/news/2024/10/31/news-datacenter-gpus-may-have-an-astonishingly-short-lifespan-of-only-1-to-3-years/)
- [NIST Engineering Statistics Handbook — Bathtub curve](https://www.itl.nist.gov/div898/handbook/apr/section1/apr124.htm)
- [Wikipedia — Bathtub curve](https://en.wikipedia.org/wiki/Bathtub_curve)
- [No MTBF — Finding and eliminating early-life failures](https://nomtbf.com/2013/06/finding-and-eliminating-early-life-failures-where-the-money-is/)
- [KES Systems — Semiconductor 101: The Bathtub Curve](https://www.kessystemsinc.com/resources/semiconductor-101-the-bathtub-curve/)
- [KES Systems — An Introduction to Semiconductor Burn-In](https://www.kessystemsinc.com/resources/an-introduction-to-semiconductor-burn-in/)
- [PCBSync — Burn-In Testing: What It Is, How It Works](https://pcbsync.com/burn-in-testing/)
- [electrontest.com — Burn-in Testing](https://www.electrontest.com/burn-in-testing/)
- [anyPCBA — Burn-In Testing: Weeding Out Infant Mortality](https://www.anypcba.com/blogs/practical-engineering/burn-in-testing-weeding-out-infant-mortality-in-electronic-devices.html)
- [Wikipedia — Burn-in](https://en.wikipedia.org/wiki/Burn-in)
- [Aerospace Corp / NASA SSRI — Thermal Test Tailoring Guidelines for Class C and D Space Programs (MIL-STD-1540E)](https://s3vi.ndc.nasa.gov/ssri-kb/static/resources/TR-2021-00283%20-%20Thermal%20Test%20Tailoring%20Guidelines%20for%20Class%20C%20and%20D%20Space%20Programs.pdf)
- [NASA SSRI Knowledge Base — Burn-In](https://s3vi.ndc.nasa.gov/ssri-kb/topics/47/)
- [NASA SSRI Knowledge Base — Thermal Vacuum](https://s3vi.ndc.nasa.gov/ssri-kb/topics/59/)
- [Wikipedia — Single-event upset (SEU/SEL)](https://en.wikipedia.org/wiki/Single-event_upset)
- [doEEEt — Single Event Latchup Protection Circuits](https://www.doeeet.com/content/eee-components/passives/single-event-latchup-protection-circuits/)
- [Introl — GB200 NVL72 Deployment: Managing 72 GPUs in Liquid-Cooled Configurations](https://introl.com/blog/gb200-nvl72-deployment-72-gpu-liquid-cooled)
- [NVIDIA — DGX GB200 NVL72 Release Notes: Known Issues](https://docs.nvidia.com/dgx/dgxgb200nvl72-release-notes/known-issues.html)
- [ASME — Failure Analysis of Direct Liquid Cooling System in Data Centers](https://asmedigitalcollection.asme.org/electronicpackaging/article/140/2/020902/367988/Failure-Analysis-of-Direct-Liquid-Cooling-System)
- [Data Centre Magazine — Choosing the Right Cooling Pumps for Next-Gen Data Centres](https://datacentremagazine.com/news/choosing-the-right-cooling-pumps-for-next-gen-data-centres)
- [NASA — Preferred Reliability Practices (redundancy / cross-strapping)](https://extapps.ksc.nasa.gov/reliability/Documents/Preferred_Practices/1319.pdf)
- [Aerospace Corp — TOR-2009(8591)-14 Effective Fault Management Guidelines](https://aerospace.org/sites/default/files/maiw/TOR-2009(8591)-14.pdf)
- [Siewiorek — Fault-Tolerant Architectures for Space and Avionics Applications](https://www.cs.unc.edu/~anderson/teach/comp790/papers/Siewiorek_Fault_Tol.pdf)
- [IEEE RAMS 2017 — Assessment of propagating failure modes in a cross-strapped redundant system](https://ieeexplore.ieee.org/document/7889674/)
- [ScienceDirect — Improving CubeSat reliability: subsystem redundancy or improved testing?](https://www.sciencedirect.com/science/article/pii/S0951832021007584)

---

## Open Questions

1. **Permanent vs. transient failure split.** The Llama-3 "419 interruptions" mix recoverable hangs with hard GPU deaths. The true *permanent* GPU AFR could be meaningfully below 9% — better public data (e.g. cloud-provider RMA rates for H100/B200) would tighten the ~7–9% planning figure.
2. **Blackwell/GB200 vs. H100.** All hard failure data is H100-era. GB200/GB300 run hotter (~120–135 kW/rack) and are newer — AFR could be worse early in their life. No published GB200 field reliability yet.
3. **Launch-vibration latent-damage rate.** No quantified figure for how many AI-rack components survive ground burn-in but carry vibration-induced latent defects that fail weeks into orbit. This is the gap between "passed burn-in" and "reliable in orbit" — worth a dedicated test campaign.
4. **NVLink spine fault-domain partitioning.** Can the NVL72 copper spine actually be electrically partitioned into independent fault domains, or is re-architecting the scale-up fabric required? This determines whether graceful degradation is a config change or a hardware redesign. (See rack_internals.md on the NVLink spine.)
5. **Coolant-loop reliability in microgravity / vacuum.** Pump MTBF (~30,000 h terrestrial) and two-phase behavior in microgravity are not well characterized for a 3-year sealed, un-serviceable loop. This is the leading whole-node-loss risk and needs its own analysis.
6. **Burn-in cost/throughput.** A 1–3 week per-rack burn-in is a real constraint on launch cadence and capital turns. How many burn-in stations are needed to sustain the deployment rate? (Cross-reference economics/ folder.)
7. **Optimal derating point.** How much AFR reduction is bought per % of FLOPS sacrificed by undervolting/underclocking GPUs? No published curve for Blackwell-class parts — needs vendor data or test.
