# Bull Case — Rocket Lab Should Build an Orbital AI-Inference Data Center on Neutron

*Round 1 — opening statement. Author: Bull. Date: 2026-05-17.*
*Every claim below cites a project research doc (path + section) or an
independent source (URL). This is the opening round; the Bear will respond and
later rounds will sharpen what survives cross-examination.*

> **Superseded economics (wave-9, 2026-05-17).** This three-round debate ran
> entirely on the **~$55M external Neutron launch price** and a **~$85M node**.
> Wave 9 re-based the launch to Rocket Lab's **internal marginal cost of
> ~$10–20M**, dropping the node to **~$35–65M (~$45M mid)** and moving central
> V2 gross payback from ~5.3 yr to **~2.8 yr** and the break-even premium from
> ~70%+ to **~25–40%** (`CONCLUSION.md` Rev 4). The debate's *numbers* (payback
> years, premium thresholds, "CONCLUSION v2") are therefore superseded; its
> **qualitative convergence — "fund the bounded build-to-learn programme toward
> a go/no-go gate" — stands**, and `CONCLUSION.md` cites the debate only for
> that. This file is preserved unedited as a dated, append-only debate record;
> for current economics see `CONCLUSION.md` Rev 4–7.

---

## Summary thesis

**Rocket Lab should build this — not because it is the cheapest compute, but
because it is a real, buildable product that no competitor is positioned to
deliver sooner, and because the venture is structurally a multi-generation play
whose economics improve with every launch.**

Five years of project research, across five waves and two quantitative models,
have hunted for a reason to say no. They did not find one. The headline finding
is consistent and load-bearing: **there is no physics wall.** Every candidate
hard barrier — heat rejection in vacuum, power, radiation, comms bandwidth,
inference topology — resolves to engineering and economics, not a law of nature
(`synthesis/wave5_synthesis.md` §7; `synthesis/preliminary_findings.md` §3).
The one genuine wall, radiator area at multi-GW scale, sits *above* the scale
this venture targets and is deliberately avoided (`synthesis/wave5_synthesis.md`
§7; `orbital/thermal_analysis.md`).

What remains is an engineering-and-economics problem — and on that ground the
case is affirmatively strong:

1. **The architecture is buildable today and the economics close at the next
   GPU generation.** A GB300-class node flies on a baseline reusable Neutron
   with ~2.7 t of mass margin; a Vera Rubin-class node — the first generation
   whose payback (~2 yr) clears the GPU obsolescence window — flies on Neutron
   plus a hot-loop radiator (`synthesis/wave5_synthesis.md` §2.4, §3, §4).
2. **The market is real, large, and supply-constrained.** Inference is the
   majority of AI compute and is projected to dominate by 2030; terrestrial
   buildout is choked by ~5-year grid queues, ~5-year transformer lead times,
   and a spreading moratorium movement (`economics/ai_datacenter_tam.md` §1, §8;
   `economics/premium_value_case.md` §1).
3. **Rocket Lab is the single best-positioned company on Earth to do this.**
   It already owns launch, the satellite bus, solar, laser comms, and
   mechanisms — the whole node stack bar one subsystem
   (`rocket_lab/space_hardware_capabilities.md` §6).

The honest framing — carried directly from the project's own thesis — is that
this is a **premium product**, never cheaper than terrestrial compute, sold to
buyers who pay for capacity, isolation, and schedule certainty they cannot get
on the ground (`vision/initial_thesis.md` Rev 4 §3). The bull case does not need
the product to be cheap. It needs it to be *buildable*, *differentiated*, and
*on a path to profit*. The evidence says it is all three.

---

## 1. No physics wall — every barrier is engineering or economics

This is the foundation, and it is the most thoroughly tested claim in the whole
project. Wave 1 examined every candidate hard barrier; waves 2–5 re-tested them
against deeper research. The verdict never moved (`synthesis/wave5_synthesis.md`
§7 — "No physics wall — confirmed across all five waves").

- **Heat rejection in vacuum.** Radiative cooling scales linearly with area; it
  is a sizing and mass problem, not a wall. A 130–155 kW rack needs roughly
  ~200–430 m² of radiator (working ~300 m²), achievable with deployable panels
  (`orbital/thermal_analysis.md`; `node_design/node_mass_model.md`).
- **Power.** A dawn-dusk sun-synchronous orbit delivers ~95–100% sunlight, so
  the solar array scales linearly with rack power and battery mass nearly
  collapses (`orbital/orbits_environment.md`; `synthesis/preliminary_findings.md`
  §3).
- **Radiation.** ~1–3 krad(Si)/yr at 500–600 km behind a few mm of aluminium —
  a reliability-engineering item. Google's Project Suncatcher proton-tested its
  TPUs and found them "surprisingly radiation-hard" to ~15 krad
  (`orbital/orbits_environment.md`; `competitors/starcloud.md` §5).
- **Comms.** Inference cross-rack traffic is light (~400 Gbps-class,
  latency-tolerant) and optical inter-satellite links already run at Starlink
  scale; optical needs no spectrum license, routing around the closed RF
  problem (`llm_compute/inference_scaling.md` §3; `laser_comms/optical_comms.md`).
- **Inference topology.** The old worry — "many satellites must talk to serve
  one model" — is dissolved: one NVL72-class rack holds and serves a whole
  1–2-trillion-parameter frontier model in its own NVLink domain
  (`llm_compute/inference_scaling.md` §2, §5).

The point is decisive for an investment decision. A physics wall would be
permanent — no amount of capital or cleverness moves it. An engineering-and-
economics problem is exactly the kind of problem Rocket Lab is built to solve,
and exactly the kind that gets cheaper with iteration. The project spent five
waves looking for the permanent "no" and did not find it. That absence is the
single most important fact in the bull case.

## 2. The configuration ladder — the architecture flies, and keeps flying as racks scale

The deepest engineering worry was a *crossover*: GPU economics improve
generation over generation, while node flyability degrades as racks draw more
power — and wave 4 found flyability failing *first*, one generation before the
economics turned favorable (`synthesis/wave4_synthesis.md` §2;
`data_science/REPORT.md`). Wave 5 resolved that crossover. The resolution is the
core of the engineering case, and it is best understood as a **ladder of
levers**, each one independently sourced, that keep the single-rack node flying
as rack power climbs.

**Rung 0 — the 1-rack node is always feasible.** One NVL72-class rack is the
minimum viable node and a complete product on its own: it independently serves a
frontier model (`llm_compute/inference_scaling.md` §5). A GB300-class node
masses ~6.8 t (mid) against a ~9.5 t reusable SSO budget — **~2.7 t of margin,
comfortable, not mass-tight** (`synthesis/wave5_synthesis.md` §4.1). The
buildable-now product exists with room to spare.

**Rung 1 — the corrected SSO payload.** Deep verification re-baselined Neutron's
reusable SSO payload from a conservative ~8.5 t to a working **~9.5 t** (a ~70%
LEO→SSO retention factor on the official 13 t downrange LEO figure)
(`rocket_lab/neutron/payload_and_block_upgrade.md` §2). That ~1 t is
decision-relevant against a ~7–10 t node and lifts the baseline 1-rack
flyability ceiling to **~200–250 kW** of rack power
(`synthesis/wave5_synthesis.md` §2.2, §2.4).

**Rung 2 — the hot-loop radiator.** The radiator is the heaviest power-scaling
subsystem and the *only* one with a 4th-power lever. Riding the warm-water
cooling trajectory the industry is already on for its own terrestrial reasons —
NVIDIA's Vera Rubin is specified for 45 °C supply water with "no chillers
needed" — the radiator surface moves from ~40–50 °C to ~70–80 °C *without
cooking the silicon*, because the chip junction is decoupled from the radiator
by the loop ΔT. Via the Stefan-Boltzmann T⁴ term this cuts radiator mass
**~40–55%** (`node_design/hot_chip_thermal_trajectory.md` summary, headline
table). That lifts the ceiling to **~270–320 kW, working ~300 kW**
(`synthesis/wave5_synthesis.md` §2.3, §2.4).

**Rung 3 — the block-upgraded Neutron.** A ~+15–30% uprate to ~12–13 t SSO is
credible by direct analogy: Electron grew +33% payload on the same airframe,
and Neutron's Archimedes engine runs deliberately de-stressed and has already
demonstrated 102% power (`rocket_lab/neutron/payload_and_block_upgrade.md` §4,
§5). With the hot-loop, that lifts the ceiling to **~430–470 kW**
(`synthesis/wave5_synthesis.md` §2.4).

**The single most important number-change of the whole project:** the working
flyability ceiling for a buildable design (baseline Neutron + hot-loop) lands at
**~300 kW** — and ~300 kW is exactly the Vera Rubin rack power
(`synthesis/wave5_synthesis.md` §2.4). The architecture *reaches* the favorable
generation. The crossover is resolved, not stranded.

**On 2-rack-class models — the architecture never needs a 2-rack Neutron node,
and that is a strength, not a limitation.** A physical 2-rack node masses
~9.6–16.6 t and blows even the expendable budget; it is correctly rejected
(`node_design/node_mass_model.md` §6 — *Verdict*; `synthesis/wave5_synthesis.md`
§2.4). But this matters far less than it first appears, because **inference
scales by adding independent rack-replica satellites, laser-meshed together —
not by splitting a model across a multi-rack node**
(`llm_compute/inference_scaling.md` §2, §5). A model larger than one rack, or
throughput larger than one rack, is served by *two single-rack satellites
meshed by optical inter-satellite links* — and inference's cross-rack traffic
(request routing, occasional KV-cache hand-off) is light and latency-tolerant,
exactly the traffic an optical mesh handles well (`llm_compute/inference_scaling.md`
§3). So the "1 rack per node, 1 node per launch" architecture is not a ceiling
on model size or capacity; it is a clean, near-linearly-scalable unit. Each
launch delivers one complete, independently useful node, and the constellation
grows by addition. **No 2-rack Neutron node is ever needed.**

The honest read: the architecture flies today (Rung 0–1), flies the favorable
generation with a single well-motivated thermal change (Rung 2), and has
headroom for one generation beyond that (Rung 3). Every rung is sourced; none
requires an invention that does not exist.

## 3. The market — inference is the majority of AI compute, and the ground is full

The product needs a large, growing, and *accessible* market. It has one.

**Inference is the majority of AI compute and growing toward dominance.**
Inference is ~55–67% of AI compute today and is projected to dominate by 2030 —
roughly ~93 GW of AI inference versus ~62 GW of training in one 2030 scenario
(`economics/ai_datacenter_tam.md` §summary, §1). Inference is also the *right*
workload for orbit: it is latency-tolerant (tens of ms tolerable), embarrassingly
parallel across replicas, and its heavy communication stays inside the rack —
the precise opposite of training's continuous cluster-wide gradient all-reduce
(`llm_compute/inference_scaling.md` §3, §4). The venture targets the largest and
fastest-growing slice of AI compute, with the workload that actually fits.

**The market is supply-constrained, not demand-constrained — the ground is
physically full.** This is the structural fact that makes orbit interesting
rather than merely exotic:

- US grid interconnection queues exceed **~2,600 GW** — more than the entire
  installed US power fleet — with a **median ~5-year wait**, and projects
  needing transmission upgrades sitting in a **5–10 year** range
  ([RMI](https://rmi.org/interconnection-reform-ai-data-centers-generator-queues/);
  `economics/premium_value_case.md` §1).
- Substation transformer lead times have stretched from 24–30 months pre-2020
  to **~5 years in 2026**
  ([Data Center Knowledge](https://www.datacenterknowledge.com/energy-power-supply/why-ai-data-center-projects-face-years-of-delays-after-approval);
  `economics/premium_value_case.md` §1).
- A data-center moratorium movement spread to **at least 12 US state
  legislatures** in early 2026; Maine passed the first statewide moratorium
  ([Built In](https://builtin.com/articles/state-data-center-moratoriums);
  `economics/premium_value_case.md` §1).
- US data centers consumed **~17 billion gallons of water in 2023**, projected
  to **~38–73 billion by 2028**; large sites use up to ~5 million gallons/day
  ([EESI](https://www.eesi.org/articles/view/data-centers-and-water-consumption);
  `economics/premium_value_case.md` §3).

Hyperscalers uniformly report being **supply-constrained, not demand-
constrained** (`economics/premium_value_case.md` §6). The scarce resource in
2026 is not money — it is *time-to-capacity*. That is precisely why Google
(Project Suncatcher) and Starcloud are pursuing orbit, and it is an independent
validation of the thesis: serious, well-capitalized players have reached the
same conclusion (`economics/premium_value_case.md` §6; `competitors/starcloud.md`
§5). An orbital node converts a multi-year, politically contingent permitting
problem into a schedulable manufacture-and-launch problem the customer controls.

**The revenue is large enough to matter.** A GW of modern AI compute grosses
roughly **~$15–20B/GW-yr selling raw GPU capacity (~$8M/rack-yr)** and
**~$25–50B/GW-yr selling frontier-model inference per token (~$16M/rack-yr)**
(`economics/revenue_per_watt.md` §summary; adopted in `synthesis/wave5_synthesis.md`
§6.1). Even a tiny orbital slice of the ~90 GW 2030 inference market is a
multi-billion-dollar annual business (`economics/ai_datacenter_tam.md` §summary).

## 4. The premium value — what customers actually pay for

The product is never cheaper than terrestrial compute, and the bull case states
that plainly (`vision/initial_thesis.md` Rev 4 §3;
`synthesis/wave5_synthesis.md` §6). But "premium" is not a weakness — it is the
business. The premium is paid for attributes that are **structurally
unavailable on the ground at any price**:

- **Zero water.** Radiative cooling in vacuum uses *none* — not "less," zero.
  Unlike the green-power claim, there is no offsetting orbital water cost; the
  project's own premium-value analysis calls this "the single cleanest
  differentiator — unqualified" (`economics/premium_value_case.md` §3, §verdict).
- **Continuous, off-grid, zero-carbon-operation power.** A dawn-dusk SSO gives a
  solar capacity factor >95% versus ~24% for US terrestrial solar, at ~36–40%
  higher irradiance — a given array produces ~5–8× the annual energy of the same
  array on the ground (`economics/premium_value_case.md` §2). No interconnection
  agreement, no transformer queue, no diesel backup.
- **Dedicated, isolated, single-tenant, sovereign capacity.** An orbital node is
  single-tenant *by construction* — there is no multi-tenancy to opt out of —
  and physically isolated from terrestrial grid failures, disasters, and (per
  the project doc) kinetic attack. The sovereign-AI infrastructure market is
  projected to grow from **~$19B in 2026 to ~$177B by 2035** (~28% CAGR), and
  the government/defense segment already holds the largest share
  (`economics/premium_value_case.md` §4, §5).
- **Speed-to-deploy.** Orbit sidesteps the ~5-year grid queue, the ~5-year
  transformer wait, the land vote, and the county moratorium entirely
  (`economics/premium_value_case.md` §1).

**The honest sizing of the premium.** The project's wave-5 framing — which the
bull case adopts without inflation — places the V2/Vera Rubin product at
**~1.5–2.5× terrestrial cost per token**, and finds that customers plausibly pay
**~50–100% more per token** for dedicated, isolated, 24/7, sovereign capacity
they genuinely cannot get on the ground (`synthesis/wave5_synthesis.md` §6.2,
Tier (b); `vision/initial_thesis.md` Rev 4 §3). That premium is paid for
*capacity-you-can-actually-get + isolation + zero water + schedule certainty* —
not for cheaper compute.

The strength of this leg is that **a ~50% premium is plausible, and the thesis
never needs more than that.** It does not depend on a 10× or 1,000× premium; it
depends on one number — will a real buyer pay ~50% more — and the evidence
(genuine, quantified, worsening terrestrial scarcity plus a fast-growing
sovereign-AI market) says that is plausible (`synthesis/wave5_synthesis.md`
§6.2). The project's premium-value doc concludes the premium is "justifiable in
principle" for exactly this buyer profile (`economics/premium_value_case.md`
§verdict).

## 5. Rocket Lab's strategic fit — the right company, with a moat

This is not a generic "someone should do this." Rocket Lab is, by the project's
own capability audit, the **best-positioned company to build an orbital compute
node**, and the fit is specific:

**It owns nearly the entire node stack.** Through a deliberate decade of
acquisition and in-house development, Rocket Lab already owns or is closing on:
launch (Neutron), the satellite bus (Flatellite — flat, high-power,
mass-manufacturable, designed for tight Neutron integration), space-grade solar
(SolAero — "the world's only fully vertically integrated space power supplier,"
plus a Feb-2026 silicon-array line announced *explicitly* for gigawatt-scale
space data centers), laser inter-satellite comms (Mynaric CONDOR, with a
100 Gbps roadmap part), reaction wheels and star trackers (Sinclair),
separation systems (Planetary Systems), and — pending a Q2-2026 close —
solar-array drives, gimbals and robotic arms (Motiv)
(`rocket_lab/space_hardware_capabilities.md` §1–5, §6). The $816M SDA prime
contract proves it can deliver as a satellite prime, not just a launch vendor
(`rocket_lab/space_hardware_capabilities.md` §4).

**There is exactly one capability gap, and it is bridgeable.** The project's
audit identifies a single clear gap: large deployable thermal radiators
(`rocket_lab/space_hardware_capabilities.md` §6). This is honestly the venture's
hardest subsystem. But it is *one* subsystem against a stack of a dozen — and
Rocket Lab's composite-structures heritage and (post-Motiv) deployment-mechanism
capability make in-house development plausible, with buy-from-vendor as the
fallback (`rocket_lab/space_hardware_capabilities.md` §6). A company that owns
the other eleven subsystems and the rocket has a credible path to closing one
gap; a company that owns none of them does not.

**This vertical integration is the moat.** The project's competitive analysis
is direct: Starcloud's serious commercial product (Starcloud-3) is designed
around SpaceX Starship's PEZ-dispenser form factor and gated on unproven
~$500/kg Starship economics and ~2028–2029 timing (`competitors/starcloud.md`
§3, §summary). A Neutron play does not inherit that dependency. Because Rocket
Lab owns its launch vehicle *and* the bus *and* the comms *and* the solar, it
can launch **whole, intact, near-COTS NVL72-class racks in Neutron's large
fairing** — not hardware redesigned to fit a dispenser
(`synthesis/preliminary_findings.md` §5; `vision/initial_thesis.md` Rev 2). It
competes on cadence, time-to-orbit, and turnkey node-level service — exactly the
axes where a vertically integrated prime on an operational-class vehicle beats a
Starship-gated competitor (`competitors/starcloud.md` §"What this means for our
Neutron thesis").

## 6. The build-to-learn → V2 arc — V1 earns and learns, V2 profits

The strongest framing of the venture is as a deliberate **multi-generation
play**, and the most striking corroboration in the whole project is that the
founder's intuition and the independent bottom-up economics arrived at the
*identical* structure (`vision/initial_thesis.md` Rev 3 §3;
`synthesis/wave4_synthesis.md` §3).

**V1 — build to learn, timed now.** A GB300-class node on a baseline Neutron is
the buildable-now product. It is honestly *not* a standalone profit centre — its
inference-service payback is ~3.1 yr, at the upper edge of the GPU obsolescence
window (`synthesis/wave5_synthesis.md` §4.1). But V1 is justified and financed
as **build-to-learn plus strategic position**, and that is a real return, not a
rationalization:

- It generates compounding, bankable learnings — radiation-hardened silicon,
  hot-loop thermal operations, deployable-radiator engineering, on-orbit
  operations — that directly de-risk V2 (`synthesis/wave5_synthesis.md` §4.1;
  `node_design/hot_chip_thermal_trajectory.md`;
  `node_design/reliability_failure_handling.md`).
- It earns modest premium revenue from a narrow set of sovereign/defense/
  dedicated-capacity buyers, and establishes Rocket Lab as the operational
  orbital-compute prime *before* Starcloud's Starship-gated product arrives
  (`synthesis/wave5_synthesis.md` §6.2, Tier (a); `competitors/starcloud.md`).
- It should be **timed now**, because the baseline-vehicle window is
  GB200/GB300-class racks in roughly 2025–2026 (`synthesis/wave5_synthesis.md`
  §4.1). The opportunity has a clock on it.

The electric-car analogy is exact: the early product is not cheap, it sells into
a premium segment, it earns revenue, and — crucially — it generates the
learnings that make the *next* generation genuinely profitable
(`vision/initial_thesis.md` Rev 3 §3).

**V2 — the standalone-profitable product.** A full ~300 kW Vera Rubin-class node
on a block-upgraded Neutron with a hot-loop radiator reaches **~2-year
inference-service payback — inside the ~2–3 year obsolescence window**
(`synthesis/wave5_synthesis.md` §4.2). This is where the venture becomes a real
business.

**And the economics structurally improve with every generation, on the same
rocket.** This is the quiet engine of the whole arc. AI rack prices roughly
double per generation while the Neutron launch cost stays fixed — so the launch
falls from ~95% of node cost (GB200 era) toward ~72% (Rubin-Ultra era)
(`economics/rack_cost_trajectory.md` §6). Meanwhile compute-per-rack rises even
faster than price (`economics/rack_cost_trajectory.md` §3). Node CapEx grows
sub-linearly with rack capability while node revenue grows roughly linearly with
rack compute — so the revenue-to-CapEx ratio, and payback, improve every
generation launched, *on the identical Neutron* (`economics/rack_cost_trajectory.md`
§6). The build-to-learn arc is not a hope; it is a mechanism, and it points one
direction: a node launched in 2028–2030 pays back materially faster than one
launched today.

## 7. Why the honest caveats do not sink the case

A strong case names the real risks and shows why they are survivable, not why
they do not exist. The project has surfaced them; here is why the venture still
clears:

- **Node payback vs. GPU obsolescence — the dominant risk.** Real, and the
  reason V1 is build-to-learn rather than a profit centre. But wave 5 showed the
  economics *do* close at the Vera Rubin generation under the inference-service
  revenue model — the architecture reaches the favorable generation
  (`synthesis/wave5_synthesis.md` §3, §4.2). The risk is "does it close cleanly
  enough, fast enough" — a question of degree, not a binary fail.
- **Two unpublished Rocket Lab numbers (SSO payload, fairing volume).** Genuine
  unknowns. But the working ~9.5 t SSO figure is a *conservative* analyst
  estimate (~70% LEO→SSO retention on an *official* 13 t LEO number), and the
  node is volume-comfortable, never volume-bound, in every model
  (`rocket_lab/neutron/payload_and_block_upgrade.md` §2;
  `node_design/node_mass_model.md` §summary). Rocket Lab itself can resolve both
  numbers — they are not unknowable, just unpublished.
- **The deployable-radiator capability gap.** The one stack gap. But it is one
  subsystem, adjacent to existing Rocket Lab competencies, and the hot-loop
  lever makes whatever radiator is built ~40–55% lighter
  (`rocket_lab/space_hardware_capabilities.md` §6;
  `node_design/hot_chip_thermal_trajectory.md`).
- **The block-upgrade dependency.** V2 profitability is gated on an uprated
  Neutron that is credible-but-uncommitted. But it is credible by direct
  precedent (Electron +33%, de-stressed Archimedes at 102%), and V1 flies and
  earns on the *baseline* vehicle while the upgrade matures
  (`rocket_lab/neutron/payload_and_block_upgrade.md` §4, §5).
- **No observed willingness-to-pay for orbital inference.** True — and it is the
  highest-value commercial unknown. But the *components* of demand are observed
  and quantified: the terrestrial supply crunch, the ~$19B→$177B sovereign-AI
  market, the documented appetite for dedicated air-gapped capacity
  (`economics/premium_value_case.md` §1, §4, §5). The thesis needs a ~50%
  premium, not a heroic one.

None of these is a wall. Every one is a number to pin down or a subsystem to
build — the ordinary work of a hard engineering venture, and exactly the work
Rocket Lab exists to do.

---

## Conclusion — the affirmative case

Rocket Lab should build this because:

1. **There is no physics wall** — proven across five research waves; the venture
   is bounded by engineering and economics, the kind of problem that yields to
   capital and iteration (`synthesis/wave5_synthesis.md` §7).
2. **The architecture flies** — a 1-rack node today with comfortable margin, the
   favorable Vera Rubin generation with one well-motivated thermal change, and
   headroom beyond; capacity scales by laser-meshing single-rack satellites, so
   no 2-rack Neutron node is ever needed (`synthesis/wave5_synthesis.md` §2–4;
   `llm_compute/inference_scaling.md` §5).
3. **The market is real, large, and full** — inference dominates AI compute, the
   ground is supply-constrained on power, water, transformers, and permits, and
   even a tiny orbital slice is a multi-billion-dollar business
   (`economics/ai_datacenter_tam.md`; `economics/premium_value_case.md` §1).
4. **The premium is plausible and modest** — ~50–100%, paid for zero water,
   off-grid power, sovereign isolation, and schedule certainty no ground site
   can offer (`synthesis/wave5_synthesis.md` §6.2).
5. **Rocket Lab owns the stack and the moat** — launch, bus, solar, laser comms,
   mechanisms; one bridgeable gap; and a vertical integration that frees it from
   the Starship dependency that gates its closest competitor
   (`rocket_lab/space_hardware_capabilities.md` §6; `competitors/starcloud.md`).
6. **It is a multi-generation play that compounds** — V1 earns and learns, V2
   profits, and the economics structurally improve every generation on the same
   rocket (`economics/rack_cost_trajectory.md` §6; `vision/initial_thesis.md`
   Rev 3–4).

The verdict the bull case asks the project to carry forward: **this is a
worthwhile venture — a buildable, differentiated, multi-generation business that
no competitor is better placed to win, gated not on physics but on engineering
execution and a handful of numbers Rocket Lab itself can resolve.**

---

## Sources

*Project research documents:*
- `vision/initial_thesis.md` — Rev 2, Rev 3, Rev 4 (thesis evolution; premium
  tiers; build-to-learn → V2 arc)
- `synthesis/preliminary_findings.md` — §3 (candidate walls), §5 (strawman
  architecture)
- `synthesis/wave4_synthesis.md` — §2 (node payback), §3 (build-to-learn
  convergence)
- `synthesis/wave5_synthesis.md` — §2 (re-baselined numbers, flyability
  ceilings), §3 (crossover resolved), §4 (V1/V2 cases), §6 (premium framing),
  §7 (risks)
- `rocket_lab/neutron/payload_and_block_upgrade.md` — §2 (~9.5 t SSO), §4–5
  (block upgrade credibility)
- `rocket_lab/space_hardware_capabilities.md` — §1–5 (capability stack), §6
  (coverage verdict, radiator gap)
- `node_design/node_mass_model.md` — §summary, §6 (1-rack vs 2-rack mass,
  2-rack rejection)
- `node_design/hot_chip_thermal_trajectory.md` — summary, headline table
  (hot-loop −40–55% radiator mass)
- `node_design/reliability_failure_handling.md` — GPU attrition, redundancy
- `orbital/thermal_analysis.md` — radiative cooling as a sizing problem
- `orbital/orbits_environment.md` — dawn-dusk SSO, radiation
- `llm_compute/inference_scaling.md` — §2, §3, §5 (one rack = one model;
  scale by replicas; inference vs training comms)
- `laser_comms/optical_comms.md` — optical ISL, Mynaric CONDOR
- `economics/ai_datacenter_tam.md` — §1, §summary (inference share, market size,
  terrestrial constraints)
- `economics/revenue_per_watt.md` — §summary (~$15–20B/GW-yr IaaS;
  ~$25–50B/GW-yr inference-service)
- `economics/premium_value_case.md` — §1 (permitting), §2 (power), §3 (water),
  §4–5 (sovereign/isolated), §6 (supply constraint), §verdict
- `economics/rack_cost_trajectory.md` — §3 (compute per dollar), §6 (orbital
  economics improve per generation)
- `competitors/starcloud.md` — §3 (Starship dependency), §5, §"What this means
  for our Neutron thesis"
- `data_science/REPORT.md` — the crossover finding

*Independent sources:*
- [RMI — interconnection queue / AI data centers](https://rmi.org/interconnection-reform-ai-data-centers-generator-queues/)
- [Data Center Knowledge — AI data center delays, transformer lead times](https://www.datacenterknowledge.com/energy-power-supply/why-ai-data-center-projects-face-years-of-delays-after-approval)
- [Built In — state data center moratoriums](https://builtin.com/articles/state-data-center-moratoriums)
- [EESI — data centers and water consumption](https://www.eesi.org/articles/view/data-centers-and-water-consumption)
- [NVIDIA Vera Rubin 45 °C warm-water cooling (Tony Grayson)](https://www.tonygrayson.ai/post/nvidia-vera-rubin-cooling-45c-no-chiller)
- [Precedence Research — sovereign AI infrastructure market](https://www.precedenceresearch.com/sovereign-ai-infrastructure-market)
- [Google Research — Project Suncatcher](https://research.google/blog/exploring-a-space-based-scalable-ai-infrastructure-system-design/)

---

## Round 2 — Bull rebuttal

*Round 2. Author: Bull. Date: 2026-05-17. The Bear's Round 1 (its own case +
its 12-point cross-examination) has been read in full and cross-checked against
the project corpus. This section appends; it does not edit Round 1. Where the
Bear caught a genuine error, the Bull concedes it plainly below — a case that
hides its flaws does not survive. Where the Bear overstated, the rebuttal pushes
back with sources.*

### R2.0 — Framing: what this round changes

The Bear's central move is correct in spirit and the Bull accepts it: **"no
physics wall" is necessary but not sufficient, and the Round 1 case leaned on it
too hard as if it were the verdict.** The decision-relevant question is the one
the Bear names — *does a node pay back before its silicon is obsolete* — and on
that question the honest answer is weaker than Round 1's tone implied. The Bull's
Round 2 position is therefore narrowed, not abandoned: **this is not "commit the
capital today"; it is "this is a live, fundable venture whose go/no-go rests on a
short, named list of resolvable unknowns — and the case for funding the work to
resolve them is strong."** That is a real and defensible verdict. It is just not
the verdict Round 1's rhetoric suggested.

### R2.1 — Concessions: what the Bear got right

These are conceded without qualification. A case is more credible for stating
them.

**C-1 — "Five years of project research" is false (Bear CX-10).** The Bull wrote
"Five years of project research, across five waves" (Round 1, Summary). That is
wrong. Every project document is dated 2026-05-17 or within days of it; the
corpus is a multi-*wave* effort compressed into a short span, not a multi-*year*
one. "Five years" appears nowhere in the corpus and was rhetorical inflation. The
correct phrasing is "five research **waves**" — and the Bull should never have
written otherwise. Conceded fully.

**C-2 — Presenting gross payback as profit was an overstatement (Bear CX-12).**
Round 1 §6 said V2 reaches "~2-year inference-service payback… this is where the
venture becomes a real business." The project defines that payback as **gross
top-line revenue ÷ node cost — explicitly excluding the node's operating cost
(ground-station network, ops staff, station-keeping)** (`wave4_synthesis.md`
§2b). A "true business case would haircut it for opex" (same source). The Bull
presented a gross-revenue recovery figure as if it were a profit figure. It is
not. Conceded.

**C-3 — Omitting the ground-segment capex was an overstatement.** Round 1's
node-economics discussion costed the *node* but never carried the **$100–500M
ground segment** — the ≥4–12 optical hubs the architecture requires
(`wave5_synthesis.md` §5; `economics/optical_ground_stations.md` §6). That is a
real, shared, multi-hundred-million-dollar capital line and the Round 1 economics
are incomplete without it. A node "paying back in 2 years gross" sits on top of
infrastructure the Round 1 case did not price. Conceded.

**C-4 — "The economics close" overstated "closes marginally in the optimistic
corner" (Bear CX-1, §1).** Round 1's Summary said "the economics close at the
next GPU generation." The project's own words are: the wave-5 levers move it
"from 'explicitly will not close' to '**closes, marginally**, at the Vera-Rubin
generation, on the right Neutron configuration'" (`wave5_synthesis.md` §1), and
the inference-service model "only reaches the obsolescence window in its **most
optimistic corner**" (`wave4_synthesis.md` §2c). The honest reading of the
payback table (`wave4_synthesis.md` §2c, inference-service case) is that the
**central** inference-service case is **~5.3 years** — roughly 2× the target —
and only the low-cost + high-revenue corner reaches ~2.6 yr. The "~2 yr" V2
figure the Bull headlined is the *best corner of the favorable revenue model*,
not the expected case. "Closes marginally in the best corner" is a materially
weaker verdict than "the economics close," and the Bull presented the stronger
one. Conceded.

**C-5 — "~9.5 t SSO is a *conservative* estimate" was wrong (Bear CX-3).** Round
1 §7 called the ~9.5 t reusable-SSO figure "a *conservative* analyst estimate."
The source says the opposite: ~9.5 t sits at the **~70% mid-point** of a
65–80% LEO→SSO retention band (range 8.5–10.5 t), and it was the **prior 8.5 t**
figure that was "on the conservative (low) side" (`payload_and_block_upgrade.md`
§2; `wave5_synthesis.md` §2.1). ~9.5 t is the *central* estimate. At the
defensible low end (8.5 t) the baseline ceiling re-derives to ~165 kW and the
"~2.7 t margin" the Bull leaned on for V1 shrinks substantially
(`wave5_synthesis.md` §2.2). The Bull quoted the reassuring midpoint as if it
were a floor. Conceded.

**C-6 — V1's economics are genuinely unattractive as a standalone compute
asset.** Round 1 §6 said this ("not a standalone profit centre"), but softened it
with "that is a real return, not a rationalization." The Bear is right that a
buildable-*today* product with a ~3.1-yr inference payback (past the obsolescence
window) and a ~10-yr IaaS payback (`wave5_synthesis.md` §3, §4.1) is, on a
pure-compute basis, a money-loser. The Bull maintains the build-to-learn return
is real (see R2.3) — but concedes V1 must be honestly labelled a research-and-
strategic-position investment, not a profit centre, and the Round 1 framing
flirted with blurring that line.

**C-7 — The orbit-addressable TAM is unquantified (Bear CX-7).** Round 1 §3 sized
the opportunity against the full "~90 GW 2030 inference market." Orbit serves
only the **latency-tolerant batch/async** subset — interactive serving is ruled
out by link latency (`premium_value_case.md` §8) — and the project explicitly
lists "quantify the orbit-addressable inference TAM" as an *unfinished* research
item (`wave5_synthesis.md` §8, item 8). The Bull should have sized against an
unquantified subset, flagged as such, not the headline figure. Conceded.

That is six substantive concessions plus one framing concession. They genuinely
weaken the Round 1 case. The remainder of this section is what the Bull maintains
*survives* them.

### R2.2 — Rebuttals: where the Bear overstated

**R-1 — The "five dependencies in series" framing is the Bear's central
overstatement (Bear §2).** The Bear's most damaging claim is that V2 requires
"five speculative dependencies stacked in series… five independent ways to fail,"
and that the Bull "never multiplies the probabilities." Examined against the
sources, the five are **not all serial, not all speculative, and not all
all-or-nothing.** Take them in turn:

- **(v) The Vera Rubin GPU generation is not speculative — it is shipping.** The
  Bear lists Rubin among "not yet shipping" / "key specs are estimates" items.
  But the project's own rack-cost research states the Vera Rubin NVL144 is
  **"shipping H2 2026"** with a reported $7.0–8.8M rack price
  (`economics/rack_cost_trajectory.md` §summary, price table). V2 is timed to a
  *near-term, announced, priced* NVIDIA product, not a distant one. Its rack
  *mass* is still an estimate (`wave5_synthesis.md` §4.2) — that is fair — but
  "the favorable generation does not exist" is not what the evidence says. This
  is the Bear's weakest sub-claim.

- **(ii) The hot-loop radiator is riding an industry trajectory, not inventing
  one.** The Bear calls the hot-loop "a thermal regime nobody has flown." The
  *flying* is new; the *thermal regime* is not. NVIDIA's Vera Rubin is specified
  by NVIDIA for **45 °C supply water with "no chillers needed"**
  (`node_design/hot_chip_thermal_trajectory.md`; cited NVIDIA/ASHRAE W40/W+
  source in Round 1 Sources). The terrestrial industry is moving to warm-water
  cooling for its *own* reasons. The orbital hot-loop borrows that trajectory.
  The genuinely unmodeled piece is narrower than the Bear implies — it is the
  junction-defense ΔT budget (`wave5_synthesis.md` §7) — and that is a *modeling*
  task on the project's P1 list (`wave5_synthesis.md` §8 item 4), not a physics
  unknown.

- **(iv) The Mynaric 100 Gbps terminal is not on V2's critical path for
  profitability.** The Bear is right that shipping CONDOR is ~2.5 Gbps and
  100 Gbps Mk3.1 is roadmap (conceded — Round 1 §5 should have said this
  plainly). But the Bear overstates its load-bearing role. Inference is
  **bandwidth-light** — "prompts up, tokens down, kB to a few MB per query" — and
  the mesh and ground links are sized by **availability, not throughput**
  (`wave5_synthesis.md` §5; `llm_compute/inference_scaling.md` §3). A first
  service of 4–8 nodes can be built on *today's* ~2.5 Gbps terminals; the
  100 Gbps part is what a *large* always-on mesh wants, not what V2 payback
  needs. This dependency is real but mis-ranked by the Bear as a profit gate.

- **(i) The block-upgraded Neutron gates V2's *full-power comfort*, not the
  venture.** Conceded in Round 1 §7 and again here: the block-upgrade is
  unannounced and the project says explicitly "do not baseline the core thesis on
  a block-upgraded Neutron" (`payload_and_block_upgrade.md` §6). The Bear is right
  to press this (CX-4). **But** the project's own wave-5 verdict is that a
  Vera Rubin rack run at its *lower power band* (~190–250 kW NVL72-class) flies
  on a **baseline reusable Neutron + hot-loop**, within the ~300 kW ceiling
  (`wave5_synthesis.md` §3, generation table, Rubin row; §4.2). The block-upgrade
  buys a *full, un-power-capped* ~300 kW Rubin node "comfortably." So the
  block-upgrade is a margin-and-comfort lever for V2, not an existence condition
  for it. That is a meaningfully different claim from the Bear's "V2… is gated on
  a vehicle the project says must not be baselined."

- **(iii) The radiator capability gap is real — and partly de-risked already.**
  This is the one of the five the Bull most concedes (see C-8 below). But it is
  not "speculative": Rocket Lab has composite-structures heritage and, post-Motiv
  close, deployment-mechanism capability (`rocket_lab/space_hardware_capabilities.md`
  §6), and a buy-from-vendor fallback exists — the project frames it as a
  make-vs-buy decision, not an invention problem. "Adjacent but not equivalent"
  (the Bear's quote) is a real caveat; it is not "cannot be done."

  **The serial-vs-independent point.** Three of the five dependencies are
  *substantially independent of each other and partly already realized*: Rubin is
  shipping (independent of Rocket Lab entirely), the hot-loop rides a separate
  industry trajectory, and the laser terminal is not on the profit path. They do
  not "multiply" the way five coin-flips would, because they are not five
  unconditioned coin-flips — several are conditioned on events already in motion
  or already partly done. The honest count is closer to **two genuine, coupled,
  Rocket-Lab-controlled unknowns** — the block-upgrade decision and the radiator
  development — plus a set of commercial unknowns (WTP, spacecraft cost). That is
  a serious list. It is not "five independent ways to fail."

**R-2 — A not-yet-flown Neutron is a *timing* risk, not a verdict against the
venture concept (Bear §3).** The Bear is right that Neutron has not flown, that
its Stage-1 tank ruptured in a January 2026 qualification test, and that
operational reusable flights are realistically NET 2027
([Space.com](https://www.space.com/space-exploration/rocket-labs-new-neutron-rocket-suffers-fuel-tank-rupture-during-test);
`payload_and_block_upgrade.md` open Q6). The Bull concedes all of that as fact.
But it does not bear on the question this debate asks — *should Rocket Lab build
this* — in the way the Bear implies. The venture is, by construction, a *future*
product: V1 is timed to GB300-class racks (2025–2026 generation) and V2 to Vera
Rubin (shipping H2 2026), with the node program running *in parallel* with
Neutron's own maturation. Rocket Lab is going to fly Neutron regardless of this
venture — Neutron is the company's flagship program. The orbital-DC node rides a
vehicle Rocket Lab is committed to anyway. "The rocket has not flown" is a
schedule input to *when* V1 launches, not evidence that the venture concept is
unsound. A tank rupture in qualification testing is, bluntly, what qualification
testing is *for*; the relevant question is whether Neutron reaches operational
reusable flight, not whether it had a test anomaly.

**R-3 — The Bear's reading of the data-science "cruel timing" finding is
darker than the post-wave-5 evidence supports (Bear §1).** The Bear quotes
`data_science/REPORT.md` §4 — "the generations worth flying are the ones you
can't fly" — as if it were the project's final word. It is not: the LIBRARY
explicitly marks that report's crossover figure **superseded** — "its ~163 kW
crossover is superseded by the wave-5 reconciled ceiling" (`LIBRARY.md`,
`data_science/REPORT.md` row). Wave 5's three levers move the buildable ceiling
to ~300 kW, which is Vera Rubin's rack power (`wave5_synthesis.md` §2.4). The
Bear acknowledges this in passing ("Wave 5 narrowed that gap") but then quotes
the *pre*-wave-5 verdict as the live one. The honest post-wave-5 statement —
which the Bull now adopts in place of Round 1's overconfident "the architecture
flies, and keeps flying" — is the project's own: the crossover is "resolved at
Vera Rubin… just barely, and exactly one generation later than it would in a
frictionless world" (`wave5_synthesis.md` §3). "Just barely" is honest. "Cannot
fly the generations worth flying" is stale.

**R-4 — "No competitor positioned to deliver sooner" — the Bear is right the
Round 1 wording was too strong, but its own counter overreaches (Bear CX-11,
§6).** Conceded: the Bull should not have asserted "sooner" flatly. But the
Bear's framing — "Starcloud has flown hardware… Rocket Lab has flown nothing" —
compares unlike things. Starcloud-1 was a **single H100, ~60 kg, on a Falcon 9
rideshare** (`competitors/starcloud.md` §1, table) — a demonstrator, not a
data-center node. Starcloud's *commercial* product, Starcloud-3, is "**in
development**," 200 kW, ~3 t, and **explicitly gated on SpaceX Starship and
unproven ~$500/kg economics, target 2028–2029** (`competitors/starcloud.md`
§3, summary). So neither company has flown a commercial orbital-compute node, and
both serious products are multi-year-out. The defensible Round 2 claim — narrower
than Round 1's — is: *Rocket Lab's path is not gated on a second company's
not-yet-proven launch vehicle*, which is a genuine structural difference in
dependency risk (`competitors/starcloud.md` §3, "What this means for our Neutron
thesis"). The Bull drops "sooner" and keeps that.

**R-5 — The Bear cites the premium-value verdict selectively too (Bear §5).**
The Bear faults the Bull (fairly — see C-4) for citing `premium_value_case.md`'s
"justifiable in principle" while omitting the following sentence. But the Bear
then does the converse: it quotes "the business case remains unproven" as if it
settled the matter, while omitting that the *same* verdict rests the case on a
**specific, documented, fast-growing buyer segment** — sovereign-AI
infrastructure at ~$19B (2026) → ~$177B (2035), ~28% CAGR, government/defense the
largest share (`premium_value_case.md` §4, §5; Round 1 §4). "Unproven" is the
honest status of the *willingness-to-pay number*. It is not a finding that the
demand is absent — the demand *components* are observed and quantified. Both
sides should quote that verdict whole: the premium is justifiable in principle,
the WTP is unmeasured, and customer discovery is the highest-value open item. The
Bull now states it exactly that way.

### R2.3 — The sharpened surviving case

After the concessions, here is what the Bull maintains — stated at its honest,
reduced strength.

**S-1 — No physics wall still matters — but only as a *gate*, not a verdict.**
The Bear concedes this is "genuine and well-tested" (Bear §7). The Bull concedes
in return (C-4, R2.0) that Round 1 over-weighted it. The correct joint statement:
no physics wall means the venture *cannot be ruled out on first principles* — the
barriers are heat, power, radiation, comms, topology, and every one resolves to
engineering and economics at the target scale (`wave5_synthesis.md` §7;
`synthesis/lint_report_2.md` §7). That clears the venture *to be evaluated on
economics*. It does not win the economic argument. Round 1 treated passing the
gate as winning the race; it is not. But passing the gate is still a real and
non-trivial result — most exotic infrastructure ideas fail it.

**S-2 — The architecture is buildable today, and that is not in dispute.** The
Bear concedes the "1 rack/node, 1 node/launch, scale by replicas" architecture is
"sound" and the 2-rack node "correctly rejected" (Bear §7). A GB300-class V1 node
flies on a baseline reusable Neutron — at the *central* ~9.5 t SSO estimate with
margin, at the *low* 8.5 t end more tightly (C-5). The engineering object exists
and is not speculative. The dispute is entirely about whether it *earns* — which
is the right place for the dispute to be.

**S-3 — The terrestrial supply crunch is real, quantified, worsening, and
conceded by the Bear.** Grid-interconnection queues ~2,600 GW with a median ~5-yr
wait; transformer lead times ~5 years; data-center moratoria in 12+ US states;
water consumption 17 → 38–73 billion gallons (`premium_value_case.md` §1, §3;
`economics/ai_datacenter_tam.md` §1; Round 1 §3). The Bear explicitly concedes
"the *demand pressure* is not manufactured" (Bear §7). This is the load-bearing
floor under the premium case and it survives intact: the *reason* an orbital node
could command a premium — buyers physically cannot get terrestrial capacity on
their timeline — is observed fact, not hypothesis.

**S-4 — Zero water is an unqualified differentiator — conceded by the Bear.**
Radiative cooling uses no water; there is no offsetting orbital water cost; the
project calls it "the single cleanest differentiator — unqualified"
(`premium_value_case.md` §3, §verdict). The Bear concedes this without
qualification (Bear §7). It stands.

**S-5 — Rocket Lab's strategic fit is the strongest leg — and the Bear concedes
it.** "Rocket Lab's in-house stack is genuinely deep… the radiator gap is the
exception, not the rule" (Bear §7). The Bull accepts the Bear's two narrowing
caveats — the "whole intact racks" mass saving is second-order (~50–90 kg,
`LIBRARY.md` `rack_internals.md` row), and "best-positioned to attempt" is not
"should commit." But the surviving claim is still substantial: of roughly a dozen
node subsystems, Rocket Lab owns or is closing on all but one
(`rocket_lab/space_hardware_capabilities.md` §6). No other company — Starcloud
included — owns launch + bus + solar + laser comms + mechanisms under one roof.
That is a genuine structural advantage for *executing* the venture, even if it is
not by itself a reason to commit.

**C-8 — and a final concession folded into S-5: the radiator gap is bigger than
"one of twelve" (Bear CX-6).** Round 1 §5 and §7 minimized it as "one subsystem
against a stack of a dozen." The Bear is right that this understates it: the
deployable radiator is simultaneously the biggest mass line, the biggest
deployment risk, the biggest un-quoted cost, and the one subsystem with "no
public evidence" Rocket Lab can build it (`rocket_lab/space_hardware_capabilities.md`
§6; `node_design/node_mass_model.md` §7). It is the venture's hardest single
engineering item and should be named as *the* critical-path subsystem, not
averaged into a count of twelve. Conceded — and it belongs on the short go/no-go
list below.

**S-6 — The per-generation tailwind is real — conceded by the Bear — with one
honest bound.** The Bear concedes "the rack-cost tailwind is real — a fixed
launch cost amortizes better as rack prices rise" (Bear §7;
`economics/rack_cost_trajectory.md` §6). The Bull accepts the Bear's bound
(CX-9): the tailwind operates only up to the generation that is still flyable —
Rubin Ultra (~600 kW) is un-flyable intact on any Neutron configuration
(`wave5_synthesis.md` §3). So the honest claim is not "improves with every
launch" (Round 1's wording — withdrawn) but "improves across the ~one-to-two
generations the venture can fly, and that improvement is what carries V1's
unattractive economics toward V2's marginal-but-positive ones."

**The surviving verdict.** Stripped of the Round 1 overstatements, the Bull's
Round 2 position is this:

> This is a venture worth **funding to the next decision gate** — not a venture
> to commit full capital to today. The physics gate is passed; the architecture
> is buildable; the demand pressure is real and conceded; Rocket Lab is uniquely
> equipped to execute it. What stands between "interesting" and "commit" is a
> *short, named, resolvable* list: (1) Neutron's true SSO payload — a number
> Rocket Lab itself holds; (2) a real bottom-up spacecraft-hardware cost to
> replace the $8–35M guess (`wave4_synthesis.md` §2a); (3) the deployable-radiator
> make-vs-buy decision and cost (C-8); (4) the block-upgrade roadmap question;
> and (5) customer-discovery on willingness-to-pay (`wave5_synthesis.md` §8). None
> of these is a physics wall; all are resolvable in months, several by Rocket Lab
> unilaterally. The correct decision today is not "build the constellation" — it
> is "fund the work that turns five unknowns into a real go/no-go," and on that
> narrower question the case is genuinely strong.

That is a weaker verdict than Round 1's "Rocket Lab should build this." It is the
verdict the evidence actually supports, and — unlike Round 1's — it survives the
Bear's cross-examination.

### R2.4 — Sources added in Round 2

*Project research documents (already in the Round 1 source list, cited again
here):* `synthesis/wave5_synthesis.md` §1, §2.1–2.4, §3, §4.1–4.2, §5, §7, §8;
`synthesis/wave4_synthesis.md` §2a–2c; `economics/rack_cost_trajectory.md`
§summary, price table, §6; `economics/premium_value_case.md` §1, §3, §4–5, §8,
§verdict; `economics/optical_ground_stations.md` §6; `competitors/starcloud.md`
§1, §3, summary, "What this means for our Neutron thesis";
`rocket_lab/neutron/payload_and_block_upgrade.md` §2, §6, open Q6;
`rocket_lab/space_hardware_capabilities.md` §6; `node_design/node_mass_model.md`
§7; `node_design/hot_chip_thermal_trajectory.md`; `llm_compute/inference_scaling.md`
§3; `LIBRARY.md` (`data_science/REPORT.md` row — crossover superseded;
`rack_internals.md` row).

*Independent sources:*
- [Space.com — Rocket Lab's Neutron fuel tank rupture during test](https://www.space.com/space-exploration/rocket-labs-new-neutron-rocket-suffers-fuel-tank-rupture-during-test)

---

## Round 3 — Bull

*Round 3. Author: Bull. Date: 2026-05-17. Rounds 1–2 ran on a 2–3-year GPU
"obsolescence window." The project has since adopted a corrected basis —
`CONCLUSION.md` v2 — in which the GPU **service life is ~5 years**, not 2–3, and
revenue **declines over that life** rather than running flat then falling off a
cliff. This section re-engages the case on that corrected basis. It appends; it
does not edit Rounds 1–2. The seven Round-2 concessions stand — none is
withdrawn. What changes is the *test the venture is being graded against*, and
that change is decision-relevant.*

### R3.0 — Framing: what the corrected basis actually changes

The whole of Rounds 1–2 was litigated against one number: a **2–3-year GPU
obsolescence window**. Every economic verdict — the Bear's strongest line, "the
central V2 payback is ~5.3 yr, roughly double the window" (`bear_case.md` S-1) —
took that window as the pass/fail line. The Bull conceded it (C-4). On a 2–3-yr
test, a ~5.3-yr payback *fails*, and fails badly.

The corrected basis changes the denominator of that comparison, and it does so
on evidence, not convenience. Three independent facts establish that a 2–3-year
*service life* was the wrong test:

1. **A 2–3-year-life payload is not a serious space proposition.** Nobody
   designs, qualifies, and launches hardware engineered to die in 2–3 years —
   the launch and integration cost cannot be amortized over a life that short.
   A LEO satellite in dawn-dusk SSO has a ~5-year natural mission life anyway
   (`orbital/orbits_environment.md`; `CONCLUSION.md` §Profitability-2), and FCC
   deorbit rules assume ~5 years. The *spacecraft* lasts ~5 years regardless of
   what the chips inside it are doing.

2. **"Obsolete ≠ broken," and the terrestrial market now says so explicitly.**
   The 2–3-yr figure conflated *frontier obsolescence* (the chip is no longer
   the best) with *end of service life* (the chip no longer earns). They are
   not the same. By 2023 all three US hyperscalers had normalized on a
   **six-year** GPU depreciation schedule, and Google, Oracle and others
   underwrite six-year useful lives
   ([SiliconANGLE / theCUBE — Resetting GPU depreciation](https://siliconangle.com/2025/11/22/resetting-gpu-depreciation-ai-factories-bend-dont-break-useful-life-assumptions/);
   [CNBC — how long before a GPU depreciates](https://www.cnbc.com/2025/11/14/ai-gpu-depreciation-coreweave-nvidia-michael-burry.html)).
   The project's own revenue research already carried this: CoreWeave
   depreciates over 6 years, hyperscalers extended server life to 6
   (`economics/revenue_per_watt.md` §5; `CONCLUSION.md` §Profitability-2).

3. **The industry has a *name* for the declining-revenue curve.** Independent
   analysis frames the GPU life as a three-stage "computing cascade": Years 1–2,
   primary life on frontier training/serving; Years 3–4, secondary life on
   high-value real-time inference; Years 5–6, tertiary life on batch/async
   inference and analytics
   ([SiliconANGLE — Resetting GPU depreciation](https://siliconangle.com/2025/11/22/resetting-gpu-depreciation-ai-factories-bend-dont-break-useful-life-assumptions/)).
   That is *exactly* the declining-revenue curve the corrected basis asks for —
   and it is exactly the workload an orbital node is best at, because orbit's
   latency penalty rules out interactive serving and steers the product toward
   batch/async inference anyway (`premium_value_case.md` §8). The orbital node's
   *one structural revenue limitation* — latency-tolerant work only — lines up
   with the *tail* of the GPU cascade. The node spends its frontier years
   earning frontier rates and its later years doing precisely the batch work the
   cascade model says is the natural Year-3-onward use of any GPU.

So the corrected basis is not the Bull moving the goalposts to escape the Bear's
Round-2 win. It is the project recognizing that Rounds 1–2 graded the venture
against the **wrong line**. The honest Round-3 question is not "does V2 pay back
in 2–3 years" — it is "does V2 pay back **within a ~5-year service life**, on a
declining-revenue curve." On that question the Bull's case is materially
stronger, and the rest of this section makes it cleanly — and concedes, just as
plainly, where it still does not close.

### R3.1 — Re-stated case: V2 on the 5-year basis is borderline-viable, not a cliff failure

Hold the project's own central number against the corrected line.

The central V2 inference-service payback is **~5.3 years** (`wave4_synthesis.md`
§2c; conceded by the Bull at C-4 and pressed by the Bear at S-1). That number
has not changed. What changes is what it is measured against:

- **On the old 2–3-yr window:** ~5.3 yr is ~2× the upper bound and ~2.5× the
  ≤2-yr viability target. The node pays back gross capital "roughly two GPU
  generations too late" (`bear_case.md` S-1). **Verdict: fails.**
- **On the corrected ~5-year service life:** ~5.3 yr sits *at the edge of the
  service life* — it crosses gross-capital break-even right around end-of-life.
  **Verdict: borderline-viable, not a cliff failure.** This is precisely the
  reframing `CONCLUSION.md` v2 adopts: V2 moves "from 'fails the test' to
  'borderline-viable'" (`CONCLUSION.md` §Verdict, §Revision history v2).

That is a real and material change in the verdict, and it is honestly come by.
A venture whose central case *fails by 2×* is a research program. A venture
whose central case *lands at the edge of viability* is a fundable venture with
thin margin — a different category of thing. The Bear's Round-2 strongest line —
"V2's expected case is also a money-loser" — was true *against the 2–3-yr line*.
Against the ~5-year line it is no longer true in the same way: at the central
case V2 recovers its node capital within the service life, just without comfort.

**The declining-revenue curve makes this better, not worse — and the Bull states
why carefully.** Round 1–2 implicitly modeled revenue as flat-then-cliff: full
rate until obsolescence, then zero. The corrected basis models it as a declining
curve — frontier rates early, batch/async tail later. Two consequences:

- **Early years are front-loaded.** A declining curve puts *more* revenue in
  years 1–3 than a flat curve that averages the same lifetime total. Payback —
  which is cumulative — therefore arrives *sooner* under a realistic declining
  curve than under a naive flat-line of the lifetime-average rate. The ~5.3-yr
  figure derives from the wave-4 table's flat "$16M/rack-yr mid revenue" row
  (`wave4_synthesis.md` §2c); a front-loaded curve at the same early rate
  reaches cumulative break-even modestly earlier than 5.3 yr. The Bull does not
  claim a precise new number here — the project has not re-run the table on an
  explicit declining curve, and inventing one would violate the sourcing rule —
  but the *direction* is unambiguous and favorable.
- **The tail still earns.** Under the cliff model, a node past obsolescence is
  worth zero. Under the cascade model it keeps earning batch/async revenue
  through years 4–5 (`CONCLUSION.md` §Profitability-4, "obsolete ≠ broken";
  [SiliconANGLE — computing cascade](https://siliconangle.com/2025/11/22/resetting-gpu-depreciation-ai-factories-bend-dont-break-useful-life-assumptions/)).
  That tail revenue is what carries cumulative cash flow past the crossover.

The honest summary of R3.1: **on the corrected basis, V2's central case is
borderline-viable — it crosses gross break-even within service life — and the
declining-revenue curve, properly modeled, pulls the crossover modestly earlier
rather than later.** That is the case Rounds 1–2 could not make because they were
graded against the wrong test. It is not a slam-dunk (see R3.3). It is a pass at
the margin, which is a genuine change of category from a 2× failure.

### R3.2 — The 5-year service life is genuinely achievable — and the build-to-learn program is the mechanism that de-risks it

The corrected basis only helps if the ~5-year service life is *real* — if the
hardware can actually be engineered to operate ~5 years in orbit. This is the
claim the Bull leans into hardest in Round 3, and the evidence supports leaning.

**Point 1 — A ~5-year service life is the *normal* design life for LEO hardware,
not a stretch.** The orbital environment at the target orbit is benign and well
characterized. The project's own reliability and orbits research, plus
independent sources, establish:

- The radiation environment at 500–600 km dawn-dusk SSO is **benign** —
  ~1–3 krad(Si)/yr, totalling roughly 5–15 krad over a 5-year life behind a few
  mm of aluminium (`orbital/orbits_environment.md`;
  `reliability_failure_handling.md` §4 — "SSO radiation at ~500–600 km is fairly
  benign… radiation is **not** the dominant mode"). Independent LEO-electronics
  research puts a 5-year LEO TID at ~5–20 krad and notes satellite payload PCBs
  are routinely designed for 5–15-year missions
  ([PCBSync — satellite PCB requirements](https://pcbsync.com/satellite-pcb/);
  [EE Times — rad-hard power for LEO](https://www.eetimes.com/leo-satellite-proliferation-leads-to-rad-hard-power-modules/)).
- This is **directly validated on the exact hardware class**. Google proton-beam
  tested its Trillium-generation TPUs and found memory errors only after
  ~2 krad — **triple the projected five-year dose behind shielding** — with no
  critical failures until ~15 krad
  ([Data Center Frontier — Google/NVIDIA test space data centers](https://www.datacenterfrontier.com/site-selection/article/55328204/when-the-cloud-leaves-earth-google-and-nvidia-test-space-data-centers-for-the-orbital-ai-era);
  consistent with the project's own `competitors/starcloud.md` §5 — TPUs
  "surprisingly radiation-hard"). And Starcloud-1 ran a commercial 4 nm NVIDIA
  H100 on sustained AI workloads in orbit for **30+ days with no
  radiation-induced crashes** ([Data Center Frontier — Starcloud launches
  orbital AI data center](https://www.datacenterfrontier.com/site-selection/article/55337494/starcloud-launches-orbital-ai-data-center-with-nvidia-h100-gpu)).
  The radiation half of the 5-year-life question is no longer hypothetical —
  it has been measured, on TPUs and on a data-center GPU, and the margin is ~3×.
- Independent industry reporting now states plainly that **orbital compute
  hardware "typically requires replacement every five to six years"**
  ([Data Center Frontier — Google/NVIDIA test space data centers](https://www.datacenterfrontier.com/site-selection/article/55328204/when-the-cloud-leaves-earth-google-and-nvidia-test-space-data-centers-for-the-orbital-ai-era)).
  A ~5-year service life is the *consensus design point* for this exact product
  category, not a Bull-case stretch.

**Point 2 — The reliability work shows ~5 years is an *engineering requirement
the design can be built to meet*, not a hope.** `reliability_failure_handling.md`
is candid and it is the right document to lean on. Its verdict:

- GPUs fail at ~7–9% AFR, dominated by constant-rate random failure. Over a
  3-year life the node glides to ~75–85% of beginning-of-life compute
  (`reliability_failure_handling.md` §5, §7). **This is a graceful glide, not a
  cliff** — and that is the key point for a declining-revenue model: a node that
  is at ~75–85% capacity in year 3 and somewhat lower by year 5 is *still a
  productive batch-inference asset*, exactly the Year-3-onward "tertiary life"
  the cascade model describes. Capacity decline and revenue decline are the same
  curve, and the corrected basis already models revenue as declining.
- The mechanisms that buy the ~5-year life are *standard, mature space
  engineering*: derating (trade a few % of FLOPS for materially lower AFR),
  partition-and-isolate fault domains so a dead GPU costs ~1.4% capacity not the
  rack, N+1-redundant coolant loops, SEL latch-up protection, and a 1–3-week
  burn-in (`reliability_failure_handling.md` §5, §6, §7). The document's own
  bottom line: "the un-serviceable orbital node is a tractable engineering
  problem… **with redundancy, derating and fault containment** — the problem
  satellites have solved for 60 years" (`reliability_failure_handling.md` §7).

**Point 3 — the build-to-learn program is *literally the mechanism* that
de-risks the 5-year life.** This is the strongest structural point of Round 3,
and it inverts a Bear criticism. The Bear's Round-2 S-3 argued the "gate" is not
cheap — it is a multi-quarter engineering program, not a phone call. *That is
correct, and it is the point.* The 5-year service life is not de-risked by a
desk study; it is de-risked by **flying V1 and learning**:

- V1 is explicitly justified as build-to-learn (`wave5_synthesis.md` §4.1;
  Round 1 §6; conceded as research-and-strategic-position at C-6). The
  *learnings it generates* are precisely the inputs to a verified 5-year life:
  radiation-hardened-silicon behavior in the actual SSO environment, hot-loop
  thermal operations, coolant-loop reliability on a real sealed orbital loop
  (the project's #1 reliability open question — `reliability_failure_handling.md`
  open Q5), and the launch-vibration latent-damage rate (open Q3). These are not
  resolvable from the ground. V1 *is* the 5-year-life qualification campaign.
- This means the corrected basis and the build-to-learn arc are not two separate
  arguments — they are the same argument. V1 earns modest premium revenue *and*
  produces the reliability dataset that turns "~5-year life is a design target"
  into "~5-year life is a verified, underwritten number" for V2. The venture's
  structure is self-de-risking on exactly the variable the corrected basis
  depends on.

**Honest bound on Point 3 — where the 5-year life is *not* yet proven.** The
Bull leans in, but does not overstate. Three caveats are real and named:

- **All hard GPU field-reliability data is H100-era.** GB200/GB300/Rubin run
  hotter and have *no published field-reliability data yet*; the ~7–9% AFR
  figure "likely *understates* a space node" (`reliability_failure_handling.md`
  §1, open Q2; `synthesis/lint_report_2.md` §5.5). A 5-year life on
  *Rubin-class* silicon specifically is a design target, not a measured fact.
- **The coolant loop is the genuine threat to the 5-year claim.** A
  representative cooling-pump MTBF is ~30,000 h ≈ 3.4 years
  (`reliability_failure_handling.md` §4) — *below* a 5-year mission life. A
  5-year un-serviceable node therefore demands *more* cooling redundancy margin
  than a 3-year one, and hot-loop operation "slightly worsens the Arrhenius
  wear-out component" (`wave5_synthesis.md` §7). N+1 redundancy makes this
  tractable (`reliability_failure_handling.md` §6), but the Bull concedes
  plainly: **the coolant loop is the subsystem on which the 5-year service life
  most realistically fails, and it must be designed and verified, not assumed.**
- The 5-year life is therefore correctly listed in `CONCLUSION.md` as *itself a
  named go/no-go unknown* (`CONCLUSION.md` §What-it-hinges-on) — "a requirement
  that must be designed in and verified." The Bull adopts that framing without
  softening it.

**Net on R3.2:** the evidence that ~5 years is achievable is *strong* — it is
the normal LEO design life, the radiation environment is benign and the silicon
is now radiation-tested with ~3× margin, the degradation is a graceful glide
handled by 60-year-mature techniques, and the build-to-learn program is the
literal mechanism that verifies it. The honest residual is that *Rubin-class*
silicon and the coolant loop specifically are design targets pending V1's flight
data — which is exactly what V1 is for. The Bull did not find hard evidence that
5 years is *unachievable*; it found a benign environment, a measured radiation
margin, and one subsystem (cooling) that must be engineered with care. That is a
de-riskable program, not a wall.

### R3.3 — Honest concessions: where the corrected basis still does not rescue the case

The 5-year basis moves V2 from "fails" to "borderline-viable." It does not move
it to "proven profitable," and a case that pretended otherwise would not survive
the Bear's Round 3. The Bull concedes the following plainly.

**HC-1 — ~5.3 yr against a ~5-year life leaves *no margin*.** Borderline-viable
is still borderline. A central payback that lands *at or slightly past*
end-of-life means the node recovers its *gross node capital* roughly as it
dies — and that is *before* the haircuts the Bull already conceded in Round 2:
opex, station-keeping, and a per-node share of the **$100–500M ground segment**
(C-2, C-3; `wave5_synthesis.md` §5). Layer those on and the *true business*
crossover for the central case is at or beyond end-of-life, not inside it. The
corrected basis rescues V2 from "fails by 2×"; it does not deliver a comfortable
return at the central case. `CONCLUSION.md` states this exactly — "~5.3 yr is
still at the edge of a ~5-year life, leaving no margin" — and the Bull adopts it
without inflation.

**HC-2 — the crossover only becomes *comfortable* at a ~70%+ premium, and that
premium is unobserved.** Per the `CONCLUSION.md` premium sweep, the cumulative
cash-flow crossover turns clearly positive within the ~5-year life only at a
**~70%-and-above** premium; at ~50% it is borderline; below ~50% it does not
cross (`CONCLUSION.md` §Profitability-4). A ~70%+ premium for orbital inference
is **not observed** — willingness-to-pay for orbital inference specifically
remains the single most load-bearing unmeasured input on the revenue side
(`wave5_synthesis.md` §6.2; `premium_value_case.md` open Q4; conceded by the
Bull at R-5 and by the Bear at S-4). The Bull's Round-2 position held that a
~50% premium is plausible and "the thesis never needs more than that." The
corrected basis sharpens that uncomfortably: at ~50% the crossover is only
*borderline*; a *comfortable* return wants ~70–100%+. The thesis now needs a
*larger* premium than Round 2 claimed to be genuinely comfortable — and that
larger premium is exactly as unobserved as the smaller one. This is a real
weakening, and the Bull concedes it.

**HC-3 — the 5-year life is a *requirement*, not a delivered fact.** Per R3.2's
honest bound: Rubin-class field reliability is unmeasured, and the coolant loop
has MTBF margin *below* the 5-year mission. The corrected basis *assumes* the
5-year life; the venture must still *earn* it through design and V1 flight data.
If V1 reveals the realistic service life is ~3.5–4 years on Rubin-class hardware
with the achievable cooling redundancy, the corrected basis partially unwinds
and V2's ~5.3-yr payback again lands past end-of-life. The downside addendum —
a 2–3-year effective life — is not idle: it is the scenario where the coolant
loop or hot-loop wear-out underdelivers.

**HC-4 — everything conceded in Round 2 still stands.** The corrected basis
changes the *life* and the *revenue shape*. It does not touch: the two
unpublished Rocket Lab numbers (SSO payload, fairing volume); the not-yet-flown
Neutron whose reusable mode is undemonstrated NET 2027; the $8–35M
spacecraft-cost spread that is "the weakest cost input in the whole project";
the deployable-radiator capability gap; or the block-upgrade's unannounced
status (`bear_case.md` S-3, S-5; `wave4_synthesis.md` §2a). None of the seven
Round-2 concessions is withdrawn. The corrected basis improves *one* axis — the
economic test — and leaves the engineering and execution risks exactly where
Round 2 left them.

### R3.4 — The Round 3 surviving verdict

Stated at its honest, corrected strength:

> On the corrected ~5-year service-life basis, V2 is **borderline-viable, not a
> cliff failure** — its central ~5.3-yr payback sits *within* a ~5-year service
> life rather than at ~2× a 2–3-yr window, and a properly modeled
> declining-revenue curve (frontier rates early, batch/async tail later) pulls
> the cumulative crossover modestly earlier. The ~5-year life is genuinely
> achievable: it is the normal LEO design life, the SSO radiation environment is
> benign and the silicon is now radiation-tested with ~3× margin on a five-year
> dose, degradation is a graceful glide handled by mature space-engineering
> techniques, and the build-to-learn V1 program is *literally the mechanism*
> that verifies the 5-year number for V2. **But borderline-viable is not
> proven-profitable:** ~5.3 yr against a ~5-year life leaves no margin once opex
> and the $100–500M ground segment are carried; a *comfortable* crossover needs
> a ~70%+ premium that no customer has confirmed; and the 5-year life is a
> requirement the coolant loop and Rubin-class silicon must still be engineered
> and flight-proven to meet. The verdict the corrected basis supports is the one
> `CONCLUSION.md` v2 reached: this is a **physics-cleared, well-differentiated,
> borderline-viable** venture that deserves **funding to a real go/no-go gate** —
> and the corrected basis is what moves it from "fails the test" to "worth
> funding the work." That is a stronger verdict than Round 2's, honestly come
> by — and it does not overstate.

### R3.5 — Sources added in Round 3

*Project research documents (cited again here):* `CONCLUSION.md` §Verdict,
§Profitability-2, §Profitability-4, §What-it-hinges-on, §Revision-history (v2);
`node_design/reliability_failure_handling.md` §1, §4, §5, §6, §7, open Q2, Q3,
Q5; `synthesis/wave4_synthesis.md` §2a, §2c; `synthesis/wave5_synthesis.md`
§4.1, §5, §6.2, §7; `synthesis/lint_report_2.md` §5.5;
`orbital/orbits_environment.md`; `economics/revenue_per_watt.md` §5;
`economics/premium_value_case.md` §8, open Q4; `competitors/starcloud.md` §5.

*Independent sources:*
- [SiliconANGLE / theCUBE — Resetting GPU depreciation: why AI factories bend but don't break useful-life assumptions](https://siliconangle.com/2025/11/22/resetting-gpu-depreciation-ai-factories-bend-dont-break-useful-life-assumptions/) — six-year hyperscaler depreciation; the three-stage "computing cascade" (primary/secondary/tertiary life)
- [CNBC — The question everyone in AI is asking: how long before a GPU depreciates](https://www.cnbc.com/2025/11/14/ai-gpu-depreciation-coreweave-nvidia-michael-burry.html) — hyperscaler six-year useful-life norm
- [Data Center Frontier — When the cloud leaves Earth: Google and NVIDIA test space data centers](https://www.datacenterfrontier.com/site-selection/article/55328204/when-the-cloud-leaves-earth-google-and-nvidia-test-space-data-centers-for-the-orbital-ai-era) — orbital hardware "typically replaced every five to six years"; Google Trillium TPU proton-tested to ~3× a five-year dose, no critical failures to ~15 krad
- [Data Center Frontier — Starcloud launches orbital AI data center with NVIDIA H100 GPU](https://www.datacenterfrontier.com/site-selection/article/55337494/starcloud-launches-orbital-ai-data-center-with-nvidia-h100-gpu) — a commercial 4 nm data-center GPU ran sustained AI workloads in orbit 30+ days, no radiation-induced crashes
- [PCBSync — Satellite PCB requirements](https://pcbsync.com/satellite-pcb/) — LEO satellite payload electronics routinely designed for 5–15-year missions
- [EE Times — LEO satellite proliferation leads to rad-hard power modules](https://www.eetimes.com/leo-satellite-proliferation-leads-to-rad-hard-power-modules/) — LEO 5-year TID environment and rad-tolerant COTS practice
