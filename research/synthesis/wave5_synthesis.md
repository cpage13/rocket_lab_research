# Wave-5 Synthesis — Orbital AI-Inference Data Center on Neutron

*Synthesis of research waves 1–5 plus the two models (fairing-packing simulation,
trajectory data-science). Date: 2026-05-17. Status: draft for review.*
*Builds on `preliminary_findings.md` (wave 1), `wave4_synthesis.md` (waves 2–4),
and `lint_report.md`. Folds in the wave-5 research (`payload_and_block_upgrade.md`,
`hot_chip_thermal_trajectory.md`, `rack_cost_trajectory.md`, `rack_internals.md`,
`solar_radiator_trajectory.md`, `reliability_failure_handling.md`,
`energy_operating_costs.md`) and the two models (`simulations/REPORT.md`,
`data_science/REPORT.md`). Every claim is tagged with its source doc.*

> **Superseded launch-cost basis (wave-9, 2026-05-17):** this synthesis (notably
> §4.1) costs the V1 node using a **~$50–55M reusable Neutron launch** described
> as the *internal cost*, giving a "~$65–95M internal / ~$90–130M customer-price"
> V1 node. That ~$50–55M figure is the **external customer price**, not the
> internal cost. Wave 9 re-based the launch to Rocket Lab's **internal marginal
> cost of ~$10–20M**, dropping the V1 node to **~$35–65M (~$45M mid)** — see
> `CONCLUSION.md` Rev 4 and `RESEARCH_TRACKER.md` wave-9. The wave-5 physics and
> flyability findings (the ~9.5 t SSO re-baseline, the reconciled ceilings, the
> three levers, the premium tiers) are unaffected; only the §4.1 launch-cost and
> node-cost dollar figures are superseded.

---

## 1. Bottom line

**No physics wall; the architecture is buildable; and — newly — the wave-5 levers
move it from "explicitly will not close" to "closes, marginally, at the
Vera-Rubin generation, on the right Neutron configuration."** The decisive tension
of waves 1–4 was a *crossover*: GPU economics improve generation-over-generation
while node flyability degrades, and wave 4 found the economics turning favorable
(~Vera Rubin, ~300 kW, ~2 yr payback) only *after* the node had already become
un-flyable on a baseline reusable Neutron (`data_science/REPORT.md`;
`wave4_synthesis.md` §2). Wave 5 supplies three levers that together close most of
that gap: (1) a **corrected, higher Neutron SSO payload** (~9.5 t reusable working,
vs. the prior conservative ~8.5 t — `payload_and_block_upgrade.md` §2); (2) a
**hot-loop radiator** that cuts the heaviest subsystem ~40–55% via the
Stefan-Boltzmann T⁴ term (`hot_chip_thermal_trajectory.md`); and (3) a credible
**block-upgraded Neutron** at ~12–13 t SSO (`payload_and_block_upgrade.md` §5).
With levers (1)+(2) a baseline Neutron flies a ~270–320 kW node — enough to lift a
**power-capped Vera Rubin-class rack**, the first generation whose economics pay
back inside the GPU obsolescence window. With (3) added, the architecture reaches
a full ~430–470 kW node, comfortably flying Rubin and approaching (but not
reaching) Rubin Ultra. The honest verdict: **physically feasible; economically
marginal-but-positive at Vera Rubin; genuinely favorable only with the
block-upgrade; and never a cheaper-than-terrestrial product — it is a premium
product whose buyers pay for capacity they cannot get on the ground.** The
remaining risk is no longer "does it close" but "does it close *cleanly enough*,
fast enough, before a faster/cheaper competitor (Starcloud-on-Starship) does."

---

## 2. Re-baseline the numbers

### 2.1 Adopt the corrected Neutron SSO payload

The wave-5 deep-verification doc (`payload_and_block_upgrade.md`) supersedes every
prior SSO figure. The project now uses:

| Neutron configuration | SSO payload | Confidence | Source |
|---|---|---|---|
| **Reusable (downrange/barge landing) — baseline** | **~9.5 t** (range **8.5–10.5 t**) | Low–Medium (estimate) | `payload_and_block_upgrade.md` §2, §6 |
| **Expendable** | **~11 t** (range 9.8–12 t) | Low–Medium (estimate) | `payload_and_block_upgrade.md` §6 |
| **Block-upgraded reusable** | **~12–13 t** | Speculative (projected +15–30%) | `payload_and_block_upgrade.md` §5 |
| RTLS reusable | ~6 t — under-sized, avoid | Low | `payload_and_block_upgrade.md` §3 |

All three LEO mode figures (8.5 t RTLS / 13 t downrange / 15 t expendable) are
**official and high-confidence**; all SSO figures remain **analyst estimates** —
Rocket Lab publishes no SSO number, and this is still the single largest physical
unknown (`payload_and_block_upgrade.md` open Q1). The correction matters: the prior
~8.5 t working figure sat at the conservative *low end* of a defensible band; the
new ~9.5 t working figure (a ~70% LEO→SSO retention factor) is ~1 t higher and
that ~1 t is decision-relevant against a ~7–10 t node. **The block-upgrade is
credible, not fantasy:** Archimedes runs deliberately de-stressed and has already
demonstrated 102% power; Electron grew +33% on the same airframe; Neutron itself
grew 8→13 t LEO in design (`payload_and_block_upgrade.md` §4, §5). But it is
unannounced and years post-debut — **upside, not baseline.**

### 2.2 Reconcile the flyability-ceiling discrepancy

Two models gave different ceilings for the rack power at which a 1-rack reusable
node stops flying:

- **Simulation (`simulations/REPORT.md`): ~214 kW**, at an **8.5 t** SSO budget.
- **Data-science model (`data_science/REPORT.md`): ~163 kW**, at an **8.75 t**
  SSO budget.

They disagree because they used *different node-mass models*, not different
arithmetic:

1. **Different SSO budget** — 8.5 vs 8.75 t. Minor; the data-science figure was
   actually the *higher* budget yet gave the *lower* ceiling, so this is not the
   driver.
2. **Different solar+radiator mass curve — this is the real cause.** The
   simulation used the reconciled radiator flux of 500 W/m² and 5 kg/m², giving
   ~10 kg/kW radiator + ~9.9 kg/kW solar ≈ **~20 kg/kW** of power-scaling mass
   (`simulations/REPORT.md` §2–4). The data-science model used the heavier
   `solar_radiator_trajectory.md` §4 curve — 3.2 t combined solar+radiator at
   130 kW ≈ **~24.6 kg/kW** (`data_science/REPORT.md` §3). The steeper curve hits
   the ceiling sooner.

**Re-derivation at the corrected ~9.5 t SSO budget.** Take the simulation's
explicit node model: `node_mass = 1.20 × [1,600 kg rack + 700 kg bus-base +
(k_solar + k_rad + 2.5) kg/kW × P]`, with k_solar ≈ 9.93, k_rad ≈ 10.0
(`simulations/REPORT.md` §3–4). Solving `node_mass = 9,500`:
- `9,500 / 1.20 = 7,916.7 kg` available after margin.
- Less fixed mass `(1,600 + 700) = 2,300 kg` → `5,616.7 kg` for power-scaling
  hardware.
- Coefficient `9.93 + 10.0 + 2.5 = 22.43 kg/kW`.
- **Ceiling P = 5,616.7 / 22.43 ≈ 250 kW.**

Running the same solve with the heavier data-science solar+radiator curve
(~24.6 kg/kW combined, +2.5 kg/kW bus → ~27 kg/kW) gives `5,616.7 / 27 ≈ 208 kW`,
and at the conservative 8.5 t end ~165 kW. **Reconciled baseline ceiling: a
1-rack reusable Neutron node stops flying at roughly ~200–250 kW of rack power,
working figure ~225 kW** — the simulation's curve, lifted by the +1 t SSO
correction; the data-science ~163 kW was the pessimistic corner (low budget +
heavy curve).

### 2.3 Apply the hot-loop radiator lever

The radiator is the single heaviest power-scaling subsystem and the *only* one
with a 4th-power improvement lever (`hot_chip_thermal_trajectory.md`). Riding the
warm-water cooling trajectory the industry is already on (Rubin spec'd for 45 °C
supply, ~65 °C return; ASHRAE W40/W+ classes), the radiator *surface* can move
from a conservative ~40–50 °C to a hot-loop ~70–80 °C **without cooking the
silicon** — the chip junction is decoupled from the radiator by the loop ΔT. That
move cuts radiator mass **~40–55%** (`hot_chip_thermal_trajectory.md` summary,
headline table).

Re-derive with radiator k_rad cut ~50% (10.0 → ~5.0 kg/kW). New combined
coefficient `9.93 + 5.0 + 2.5 = 17.43 kg/kW`:
- At 9.5 t SSO: `5,616.7 / 17.43 ≈ 322 kW`.
- At the heavier-solar sensitivity: ~270 kW.

### 2.4 One reconciled flyability ceiling — three configurations

| Neutron configuration | 1-rack node flyability ceiling (rack power) | Basis |
|---|---|---|
| **Baseline Neutron (reusable, ~9.5 t SSO)** | **~200–250 kW** (working ~225 kW) | §2.2 re-derivation |
| **Baseline Neutron + hot-loop radiator** | **~270–320 kW** (working ~300 kW) | §2.3; `hot_chip_thermal_trajectory.md` |
| **Block-upgraded Neutron (~12.5 t SSO) + hot-loop** | **~430–470 kW** (working ~450 kW) | §2.3 solve at 12.5 t: `(12,500/1.2 − 2,300)/17.43 ≈ 466 kW` |

For reference: expendable baseline (~11 t) + hot-loop ≈ `(11,000/1.2 − 2,300)/17.43
≈ 395 kW`. The 2-rack node remains rejected on every configuration — it exceeds
even the expendable budget at 130 kW (`simulations/REPORT.md` §5;
`node_mass_model.md` §6). **Architecture stays: 1 rack per node, 1 node per
launch.**

> **The single most important number-change of wave 5:** the working flyability
> ceiling for a buildable design (baseline Neutron + hot-loop) moves from the
> wave-4 effective ~163–214 kW to **~300 kW** — and ~300 kW is exactly the Vera
> Rubin rack power. That coincidence is what resolves the crossover.

---

## 3. The crossover, resolved

Wave 4's crossover finding (`data_science/REPORT.md`): economics improve down the
GPU ladder while flyability degrades, and flyability failed *first* — the node
became un-flyable (~163 kW ceiling) one generation *before* the economics turned
clearly favorable (Vera Rubin, ~2 yr payback). Wave 5's three levers change the
verdict. Mapping each generation:

| GPU generation | Rack power | Rack price | Flyable? | On which Neutron config | Payback at that generation |
|---|---|---|---|---|---|
| **GB200 NVL72** | ~130 kW | ~$3.2M | **Yes** | Baseline reusable (large margin) | ~4.7 yr inference / ~10 yr IaaS — **outside the ~2–3 yr window** |
| **GB300 NVL72** | ~135–155 kW | ~$6.0–6.5M | **Yes** | Baseline reusable (comfortable now, ~2–3 t margin at 9.5 t SSO) | ~3.1 yr inference — **at the upper edge of the window** |
| **Vera Rubin NVL72/144** | ~190–300 kW | ~$7–8.8M | **Yes — newly** | Baseline reusable **+ hot-loop** (≤~300 kW), or block-upgrade for full headroom | ~2.0 yr inference — **inside the window** |
| **Rubin Ultra (Kyber-class)** | ~600 kW | ~$15–25M+ | **No** | Exceeds even block-upgrade + hot-loop (~450 kW ceiling) and the ~15 t expendable budget | ~1.2 yr inference — best economics, **but un-flyable intact** |

Sources: rack power/price `ai_hardware.md` §1.1, `rack_cost_trajectory.md`;
payback `data_science/REPORT.md` §1, `wave4_synthesis.md` §2c; flyability §2.4
above.

**Does the architecture now reach the favorable generation? Yes — marginally, and
this is the headline result of wave 5.** The favorable generation is Vera Rubin
(~2 yr inference payback, inside the obsolescence window). Wave 4 said Rubin could
not fly. Wave 5 says:

- **A Vera Rubin rack run at its lower power band (~190–250 kW NVL72-class)** flies
  on a **baseline reusable Neutron + hot-loop** within the ~300 kW ceiling.
- **A full ~300 kW Rubin node** is right at the baseline+hot-loop ceiling — flyable
  but with thin margin; comfortably flyable on a **block-upgraded Neutron +
  hot-loop** (~450 kW ceiling).
- **Rubin Ultra (~600 kW) remains un-flyable intact** on any Neutron — it needs
  power-capping (run a partial/down-clocked rack ≤~450 kW), multi-launch on-orbit
  assembly, or a larger vehicle (`data_science/REPORT.md` §4;
  `solar_radiator_trajectory.md` §4.5).

So the crossover is **resolved at Vera Rubin, not stranded.** The cruel-irony
framing of wave 4 ("the generations worth flying are the ones you can't fly")
softens to: the *first* favorable generation is now flyable; the *most* favorable
generation (Rubin Ultra) still is not. The architecture catches the economics —
just barely, and exactly one generation later than it would in a frictionless
world.

**Important honesty check on payback.** The payback figures above
(`data_science/REPORT.md`) use the *inference-service* revenue model with the
$18M-mid spacecraft-hardware estimate — the weakest cost input in the whole
project (`wave4_synthesis.md` §2a). At raw-GPU-rental (IaaS) rates the same nodes
pay back ~2–3× slower and do **not** clear the window at any generation
(`wave4_synthesis.md` §2c). The favorable-generation verdict is therefore
conditional on: (a) selling tokens, not GPU-hours; (b) the spacecraft-hardware
cost landing at/below the ~$18M mid; and (c) the rack-cost-trajectory tailwind
holding — rising rack price makes the fixed launch a smaller share of node cost
each generation, which is real and confirmed (`rack_cost_trajectory.md` §6).

---

## 4. Two concrete cases

### 4.1 V1 — today (1 GB300-class rack, baseline Neutron, barge landing)

The buildable-now product. One intact GB300 NVL72-class rack, ~150 kW sizing
power, downrange/barge-recovered reusable Neutron.

**Node mass** (`node_mass_model.md` §6 feasibility envelope; `simulations/REPORT.md`
§4):

| Line | Mass |
|---|---|
| Space-modified GB300 rack ×1 | ~1.6 t |
| Solar array (~150 kW, ~370 m² GaAs / ~750 m² Si) | ~1.5 t |
| Radiator + thermal loop (~300 m² working, conventional ~50 °C surface) | ~1.5 t (hot-loop ~1.0 t) |
| Spacecraft bus (structure, avionics, ADCS, comms terminals, PMAD, battery) | ~1.0 t |
| Propulsion / station-keeping | ~0.4 t |
| Deployment structures (array + radiator booms/gimbals/HDRM) | ~0.6 t |
| Margin (20%) | ~1.1 t |
| **Node total** | **~6.8 t** (sim mid); feasibility envelope ~5.6–8.6 t |

Against the corrected ~9.5 t reusable SSO budget, a ~6.8 t node flies with
**~2.7 t of margin** — comfortably, no longer "mass-tight." This is the single
most reassuring number in the re-baseline: at the corrected SSO figure, a GB300
node is not marginal, it is *comfortable*.

**Node cost** (`wave4_synthesis.md` §2a; `rack_cost_trajectory.md`):

- GB300 rack hardware, space-modified: ~$6–8M (rack ~$6–6.5M buy +
  space-modification).
- Spacecraft hardware (bus + solar + deployable radiator + 3–4 optical terminals +
  propulsion + deployment structures): **~$8–35M, ~$18M mid** — the weakest cost
  input, no direct quote exists.
- Launch: ~$50–55M reusable internal cost; Rocket Lab's customer price would
  carry its targeted ~50% gross margin.
- **Total node cost ≈ ~$65–95M internal** (rack + spacecraft + internal launch),
  or **~$90–130M at a customer price** (~$55M+ launch price + rack + spacecraft +
  ground-segment allocation).

**The honest economic read for V1.** A GB300 node does **not** pay back inside the
~2–3 yr GPU obsolescence window. Inference-service payback is ~3.1 yr — at the
*upper edge* of the window, meaning by the time it pays back the silicon is
already uncompetitive; IaaS payback is ~10 yr (`data_science/REPORT.md` §1;
`wave4_synthesis.md` §2c). **V1 is explicitly a build-to-learn / strategic-position
product, not a standalone profit centre** — unchanged from the Rev-3 thesis. Its
return is the learning (radiation-hardened silicon, hot-loop thermal ops,
deployable-radiator engineering, on-orbit operations — `reliability_failure_handling.md`,
`hot_chip_thermal_trajectory.md`) and the strategic position, plus modest premium
revenue. The reliability work (`reliability_failure_handling.md`) shows a GB300
node will glide from 100% → ~75–85% compute over a 3-year life with a partitioned,
redundantly-cooled architecture — an acceptable, *plannable* degradation, and the
business case must be underwritten against end-of-life capacity. **V1 should be
financed and justified as build-to-learn — and timed now, because the data-science
model shows the baseline-vehicle window is GB200/GB300-class racks in roughly
2025–2026 (`data_science/REPORT.md` §4).**

### 4.2 V2 — the block-upgrade case (block-upgraded Neutron + hot-loop)

The scaled, genuinely-profitable product. A block-upgraded Neutron (~12–13 t SSO)
plus a hot-loop thermal design.

**What it unlocks.** §2.4 gives a ~430–470 kW 1-rack flyability ceiling. That
unlocks **a full ~300 kW Vera Rubin-class rack node with generous margin** — the
favorable generation, flown intact and un-power-capped. It does **not** unlock a
2-rack node (still ~16+ t, over even the block-upgraded budget —
`node_mass_model.md` §6) nor a Rubin Ultra ~600 kW node. So V2 is best understood
as **"a full-power Rubin node flown comfortably,"** not "two racks." (The founder's
wave-5 hypothesis of ~2 racks on a block-upgraded Neutron is *not* supported by the
mass model — the block-upgrade buys ~one more *power* generation per node, not a
second rack.)

**What the block-upgrade must deliver.** A ~+25–30% SSO payload gain (9.5 → 12–13 t)
via Archimedes thrust uprating (the engine runs de-stressed, has shown 102% power)
plus modest tank stretch and recovery-hardware mass reduction — the Electron
precedent (+33% on the same airframe) is the basis (`payload_and_block_upgrade.md`
§4, §5). It is unannounced and realistically arrives years after Neutron's first
operational flights. **V2 is a multi-year-out proposition, gated on Rocket Lab
actually pursuing the uprate.**

**Node mass (V2, ~300 kW Rubin rack, hot-loop):** rack ~1.7–2.0 t (Rubin rack mass
is unpublished, estimated heavier than GB300 — `ai_hardware.md`); solar ~3.0 t;
hot-loop radiator ~2.7 t (vs ~5.5 t conventional — `hot_chip_thermal_trajectory.md`
headline table, 300 kW row); bus ~1.5 t; propulsion ~0.6 t; deployment ~1.0 t;
20% margin ~2.1 t → **node total ≈ ~12.5–13 t**, fitting a block-upgraded Neutron.

**Node cost (V2).** Rubin rack ~$7–9M and rising (`rack_cost_trajectory.md`);
spacecraft hardware, mass-manufactured (Rocket Lab's Flatellite philosophy —
`space_hardware_capabilities.md` §4) and with a productised radiator, pulled toward
the low end ~$10–18M; block-upgraded launch likely similar-to-modestly-higher than
baseline ~$55–70M. **Total node cost ≈ ~$75–95M** — but carrying a rack with ~2×
the compute of GB300.

**The economic read for V2.** This is where it closes. A ~300 kW Rubin node has
~2.0 yr inference-service payback (`data_science/REPORT.md` §1) — **inside the
~2–3 yr obsolescence window**, with the remaining ~0.5–1 yr of competitive life as
margin. Rising rack price makes the fixed launch a smaller share of node cost each
generation (launch share ~70% → ~54% across the GB200→Rubin-Ultra ladder —
`rack_cost_trajectory.md` §6), so revenue/CapEx structurally improves. **V2 is the
standalone-profitable product the thesis has been pointing at since Rev 3** — and
wave 5 confirms it is reachable, conditional on the block-upgrade being pursued and
on the inference-service (token-selling) revenue model. At raw IaaS rates even V2
is marginal (~4 yr); the profit case needs token revenue.

---

## 5. The deployed system — a strawman

"If you were to fight for it, what does it look like."

**Constellation / mesh sizing.** Nodes fly in a **~500–600 km dawn-dusk
sun-synchronous orbit** (~97.4–97.8° inclination) — ~95–100% sunlit, steady
thermal state, benign radiation, largely natural deorbit compliance with the FCC
5-year rule (`orbits_environment.md`, `orbit_types_primer.md`). Each node is a
self-contained 1-rack inference unit that independently serves a frontier model
(`inference_scaling.md`). To serve frontier models with always-reachable coverage:

- **First useful service: ~4–8 nodes.** Enough for throughput, redundancy (a node
  lost to a coolant-loop failure does not end the service —
  `reliability_failure_handling.md`), replica load-balancing, and overlapping
  ground-station passes (`preliminary_findings.md` §5, `wave4_synthesis.md` §6).
  *(Superseded — the wave-10 minimum-viable-scale study (`llm_compute/minimum_viable_scale.md`)
  and `CONCLUSION.md` Rev 6 re-scoped this to a **~3–4-node Phase-1 anchor deployment** /
  **~3–5-node minimum viable commercial deployment**. Read "~4–8" as a superseded estimate.)*
  A single node is a valid MVP/demonstrator but not a service.
- **Always-reachable connectivity** is the genuine open design fork. A LEO/SSO
  node sees a given ground station only ~5–15 min per ~96-min orbit
  (`orbit_types_primer.md` §3). Three options: (a) a **LEO mesh** of optical
  inter-satellite links routing traffic node-to-node until one has a ground hub in
  view (Starlink-style, low latency, needs enough nodes for mesh continuity —
  plausibly ~12–24+ nodes for a robust always-on mesh); (b) a small **GEO relay
  layer** (TDRS/EDRS-style, lifts contact 5–15% → 85–100%, adds ~600 ms round-trip);
  (c) **ground-station diversity** alone. For a frontier-inference service the
  practical answer is **(a) a laser mesh among the compute nodes themselves** —
  each node carries 3–4 Mynaric CONDOR-class optical terminals (target ~100 Gbps
  Mk3.1; shipping hardware is ~2.5 Gbps today — `optical_comms.md`) — so a
  meaningful service is ~**12–24 nodes** once you size for both compute throughput
  *and* mesh-continuity, growing near-linearly by adding independent rack-replica
  satellites.
- **Inference is bandwidth-light** (prompts up, tokens down — kB to a few MB per
  query), so the mesh and ground links are sized by *availability*, not throughput
  (`optical_ground_stations.md` §5).

**Ground-hub segment.** **≥4 geographically diverse optical hubs >1,000 km apart**
for ~99% availability; ~10–12 for carrier-grade 99.9% (`optical_ground_stations.md`
§3). Each hub is **modest-aperture (0.6–1.0 m), multi-terminal** (4–8 terminals to
track several nodes at once), with adaptive optics and a high-power
multi-sub-aperture uplink — *diversity beats aperture; do not build one monster
telescope*. Customers wire into hubs over terrestrial fiber. Per-hub capex
~$20–60M; a 4–12-site network ~$100–500M (flagged estimates —
`optical_ground_stations.md` §6). Add a **modest RF sliver** (~100–250 MHz Ka-band,
obtainable via inheriting a distressed priority filing — `rf_limited_service.md`)
serving triple duty: all-weather backup for the cloud-vulnerable optical ground
link, a low-rate direct B2B channel / out-of-band control plane, and TT&C.

**Strawman first-useful-service summary:** ~4–8 GB300/Rubin-class nodes in
dawn-dusk SSO for the initial commercial service; scaling toward ~12–24 nodes for
a robust, always-reachable laser-meshed frontier-inference network; ground segment
of ≥4 (target 6–12) diverse modest-aperture optical hubs plus a modest RF backup
payload on every node.

---

## 6. Economics — honest premium framing

The founder asked for this explicitly: state the orbital product's cost per unit
of compute versus terrestrial, as a premium multiple and where possible per-token
or per-kW, and be honest about what a real customer would pay.

### 6.1 The premium multiple — labeled estimates

Build it from the node cost. A V1 GB300 node costs ~$65–95M internal
(`wave4_synthesis.md` §2a; §4.1 above) and carries one ~150 kW rack. A terrestrial
GB300 rack costs ~$6.5M hardware + a long-lived shell amortized across *multiple*
GPU generations + ~$1.6M of 5-yr opex (`energy_operating_costs.md` §5;
`rack_cost_trajectory.md`). The orbital node's all-in cost per rack is therefore
**~$65–95M vs. a terrestrial fully-loaded ~$5–8M per rack-generation** — a raw
capital ratio of **~10–15×**.

But the *right* comparison is cost per unit of delivered compute over the asset's
revenue-generating life, because the orbital node strands its whole asset at
obsolescence while the terrestrial shell does not. On that basis:

- **V1 (GB300, baseline Neutron):** orbital cost per token / per GPU-hour is an
  **estimated ~5–10× terrestrial.** The node must gross ~$16M/rack-yr
  (inference-service) to reach even a ~3 yr payback; a terrestrial rack reaches
  payback far faster on far less revenue. **Labeled estimate**, derived from the
  payback tables (`wave4_synthesis.md` §2c, `data_science/REPORT.md`).
- **V2 (Rubin, block-upgraded Neutron + hot-loop):** the premium compresses to an
  **estimated ~1.5–2.5× terrestrial** cost per token — because rising rack value
  amortizes the fixed launch better, the hot-loop cuts mass/cost, and Rubin's
  compute-per-dollar is higher. **Labeled estimate.** This is the range where a
  real premium buyer plausibly pays.
- **Per-kW / per-rack revenue anchors** (`revenue_per_watt.md`, adopted in
  `wave4_synthesis.md` §3): a rack grosses ~$8M/rack-yr selling raw GPU capacity
  (IaaS) or ~$16M/rack-yr selling frontier-model tokens (inference-service). The
  orbital node must charge a premium *on top of* these terrestrial-anchored rates
  to close — the question is how much, and whether a buyer pays it.

### 6.2 Three tiers, stated honestly

**Tier (a) — pre-favorable.** *V1 / GB200–GB300 generation, baseline Neutron.* The
orbital product is **not cost-competitive** — ~5–10× terrestrial cost per token.
It does **not** pay back inside the GPU obsolescence window. **Required premium to
break even: implausibly large — on the order of several-hundred-percent over
terrestrial inference pricing.** *Would a real customer pay that on a pure-compute
basis? No.* But the tier is still worth doing, and real money flows, for three
reasons that are not "cheap compute": (1) the **learnings** — radiation-hardened
silicon, hot-loop thermal ops, deployable-radiator engineering, on-orbit
operations — which compound into V2 (`hot_chip_thermal_trajectory.md`,
`reliability_failure_handling.md`); (2) **strategic position** — being the
operational Neutron-class orbital-compute prime before Starcloud's Starship-gated
product arrives (`starcloud.md`); (3) a **narrow set of buyers who pay for
non-compute attributes** — a government / defense / sovereign buyer who is
capacity-blocked on the ground, or who values physical isolation, dedicated 24/7
capacity, or jurisdictional separation enough to fund a demonstrator
(`premium_value_case.md` §1, §4, §5). Tier (a) is financed as build-to-learn plus
strategic/sovereign demonstrator revenue — **honestly, not as a profit centre.**

**Tier (b) — premium-but-viable.** *V2 / Vera Rubin generation, block-upgraded
Neutron + hot-loop.* The orbital product costs an **estimated ~1.5–2.5× terrestrial
per token**. Payback reaches ~2 yr — inside the obsolescence window. **Required
premium: customers pay roughly ~50–100% more per token than terrestrial dedicated
inference.** *Would a real customer pay ~50% more? Plausibly yes, for a specific
buyer profile* — a corporation or frontier lab buying **dedicated, physically
isolated, 24/7-reliable, single-tenant, sovereign capacity they genuinely cannot
get on the ground** because of the ~5-year grid-interconnection queue, ~5-year
transformer lead times, water-permitting moratoria, and the sovereign-AI demand
documented at ~$19B (2026) → ~$177B (2035) (`premium_value_case.md` §1, §4, §6).
The premium is paid for **capacity-you-can-actually-get + isolation + zero water +
schedule certainty**, not for cheaper compute. This is the tier where the thesis
is a real business. The honest caveat: there is **no observed willingness-to-pay
data for *orbital* inference specifically** — the ~50% figure is a reasoned
estimate, and customer-discovery is the highest-value open research item
(`premium_value_case.md` open Q4).

**Tier (c) — favorable.** *V2+ at scale, mass-manufactured nodes, and/or the next
launch generation.* Here payback closes cleanly and the product approaches genuine
competitiveness for latency-tolerant inference. Required premium shrinks toward
**~0–25% over terrestrial**, sustained by the zero-water / off-grid /
sovereign attributes rather than by scarcity pricing. This tier depends on the
block-upgrade *plus* mass-manufacturing learning-curve cost reduction *plus*
possibly a cheaper launch generation. It is the multi-generation endpoint, not a
2026–2028 proposition. **Would a customer pay a 1,000× premium? No — and the
thesis never needs them to.** The whole point of the honest framing: the product
lives or dies on whether a real buyer pays the **~50% Tier-(b) premium**, and the
evidence (terrestrial supply crunch, sovereign-AI market growth, dedicated-capacity
demand) says that is plausible — not certain, but plausible.

**One-line honest summary:** *Would a customer pay 50% more per token for
dedicated, isolated, 24/7 orbital compute they cannot get on the ground? Maybe —
and that "maybe" is the entire business case. Would they pay 1,000×? No. The thesis
does not need them to, and never claims they would.*

---

## 7. Risks & open issues

Each marked **WALL** / **RISK** / **UNRESOLVED**, with status.

- **No physics wall — confirmed across all five waves.** Heat rejection, power,
  radiation, comms, inference topology all resolve to engineering/economics
  (`preliminary_findings.md` §3, `wave4_synthesis.md` §5). **Status: settled.**
- **GW-scale thermal — WALL, deliberately out of scope.** Radiator area becomes
  enormous at multi-MW/GW; the project stays at the 100 kW–~1 MW node class below
  it (`thermal_analysis.md`, `solar_radiator_trajectory.md` §4.5). **Status: avoided
  by design.**
- **Node payback vs. GPU obsolescence — RISK (the dominant one), now improved.**
  Wave 5's levers move the favorable generation (Vera Rubin) from un-flyable to
  flyable, so the architecture *reaches* the generation where payback (~2 yr)
  clears the ~2–3 yr window — but only under the inference-service revenue model
  and only marginally for V1. **Status: improved from "fails" to "closes
  marginally at V2"; still the make-or-break variable.**
- **Neutron SSO payload mass — UNRESOLVED (largest single physical unknown).**
  ~9.5 t reusable working figure is an analyst estimate; Rocket Lab publishes
  nothing. ±1 t moves the flyability ceiling ±~40 kW (`payload_and_block_upgrade.md`
  §2, open Q1). **Status: unresolved; pursue Rocket Lab directly.**
- **Block-upgraded Neutron — RISK (on the critical path to V2 profitability).**
  Credible by analogy (Electron +33%, de-stressed Archimedes) but unannounced and
  years post-debut (`payload_and_block_upgrade.md` §5). V2's profitability depends
  on it. **Status: plausible but uncommitted; the central V2 dependency.**
- **Deployable-radiator capability gap — RISK (capability + cost + schedule).**
  Rocket Lab does not build large deployable radiators — the one clear gap in an
  otherwise complete in-house stack (`space_hardware_capabilities.md` §6). It is
  also the biggest mass line, the biggest deployment risk, and a major un-quoted
  cost input. The hot-loop lever makes the radiator ~40–55% lighter but does not
  remove the *capability* gap. **Status: unresolved; make-vs-buy decision needed.**
- **Spacecraft-hardware cost ($8–35M) — UNRESOLVED, weakest economic input.** No
  direct quote exists; it sets whether V2 payback is ~2 yr or worse
  (`wave4_synthesis.md` §2a). **Status: needs a real bottom-up build-up.**
- **Radiator area / chip→coolant→panel thermal model — UNRESOLVED.** The
  ~200–430 m²/rack range (working ~300 m²) is bracketed pending a real
  thermal-resistance model (`lint_report.md` §1.1). The hot-loop analysis assumes
  the junction can be defended with ΔT budget — plausible but unmodeled in detail
  (`hot_chip_thermal_trajectory.md` open Q1–Q3). **Status: unresolved; P1 research
  item.**
- **Coolant-loop reliability — RISK (the leading whole-node-kill mode).** A pump or
  CDU failure thermally shuts the rack within seconds; terrestrial pump MTBF
  (~30,000 h) is inadequate for a 3-yr un-serviceable node without N+1 redundancy
  (`reliability_failure_handling.md` §4). Hot-loop operation slightly worsens the
  Arrhenius wear-out component. **Status: manageable with redundant cooling; must
  be designed in.**
- **GPU attrition / un-serviceability — RISK, characterized and plannable.**
  ~7–9% AFR → glide to ~75–85% compute over 3 yr with a partitioned, redundant
  architecture; burn-in must be 1–3 weeks, not 1–2 days
  (`reliability_failure_handling.md`). **Status: tractable; underwrite the business
  against end-of-life capacity.**
- **Weather-limited optical ground link — RISK, well-characterized.** Mitigated by
  ≥4 diverse hubs, not eliminated; introduces latency/handoff jitter
  (`optical_ground_stations.md`). **Status: engineering, not a wall.**
- **Mynaric 100 Gbps timeline — RISK.** Shipping CONDOR Mk3 is ~2.5 Gbps; the mesh
  wants the Mk3.1 ~100 Gbps roadmap part (`optical_comms.md`). **Status: roadmap
  dependency.**
- **Latency/bandwidth confines the market — RISK (bounds the TAM).** Orbital links
  rule out real-time interactive serving; addressable market is latency-tolerant
  batch/async inference (`premium_value_case.md` §8). **Status: real constraint;
  size the addressable slice.**
- **Customer willingness-to-pay for orbital inference — UNRESOLVED.** No observed
  WTP data; the ~50% Tier-(b) premium is a reasoned estimate
  (`premium_value_case.md` open Q4). **Status: unresolved; highest-value commercial
  research item.**
- **"GB300 1.36 t rack scope" — UNRESOLVED, foundational.** If the intact rack
  includes separate switch/CDU/PDU sub-racks, per-rack mass rises to ~2.5–3 t and
  every mass figure scales up, lowering the flyability ceiling
  (`node_mass_model.md` open Q8). **Status: cheap to resolve; do it first.**
- **Competitive timing — RISK.** Starcloud's Starship-gated commercial product
  (Starcloud-3, ~2028–2029) and Neutron's own slipped schedule (NET 2027 for
  operational reusable flights) mean the build-to-learn window is real but narrow
  (`starcloud.md`, `neutron_specs.md`). **Status: a strategic race, not a physics
  problem.**

---

## 8. Recommended next steps / research

1. **Node unit economics — the full bottom-up model (highest priority).** Cost +
   revenue + opex + payback for one node, then a 4–8-node service. Replace the
   ~$8–35M spacecraft-hardware estimate with a real build-up — it is the weakest
   input and decides whether V2 closes at ~2 yr.
2. **Confirm Neutron SSO payload mass** directly from Rocket Lab — the largest
   single physical unknown; ±1 t swings the flyability ceiling ±~40 kW.
3. **Deployable-radiator make-vs-buy + cost.** Rocket Lab's one capability gap;
   get a vendor quote for a ~300 m²/rack productised hot-loop deployable radiator,
   areal mass, and a cost number.
4. **Chip→coolant→panel thermal-resistance model.** Closes the ~200–430 m²
   radiator-area range *and* validates that the hot-loop ~70–80 °C radiator
   surface is reachable with the junction defended — the assumption the §2.3
   ceiling rests on.
5. **Re-run the fairing-packing simulation with the hot-loop radiator curve and
   the corrected 9.5 t SSO budget** to produce a defensible single ceiling figure
   (this synthesis derived ~300 kW analytically; confirm in the model).
6. **Customer willingness-to-pay discovery** — interviews with sovereign,
   defense, and frontier-lab buyers to test the ~50% Tier-(b) premium. No observed
   WTP data exists; this is the highest-value commercial unknown.
7. **Resolve the "1.36 t rack scope" definition** — cheap, foundational; rescales
   every mass figure if the intact rack includes switch/CDU/PDU sub-racks.
8. **Quantify the orbit-addressable inference TAM** — the latency-tolerant
   batch/async slice of the ~90 GW 2030 inference figure.
9. **Engage Rocket Lab on the block-upgrade roadmap** — V2 profitability is gated
   on it; understand whether and when an uprated Neutron is realistic.
10. **Connectivity architecture decision** — LEO laser mesh vs. GEO relay vs.
    ground-diversity-only, sized for an always-reachable frontier-inference
    service.

---

## 9. Proposed thesis revision (Rev 4)

*Proposed only — the thesis file is not edited here.*

- **Lead with the resolved crossover.** Rev 3 said the economics did not close
  inside the GPU window and that V1 was build-to-learn. Rev 4 should state the
  wave-5 result: **three levers — a corrected higher Neutron SSO payload
  (~9.5 t reusable), a hot-loop radiator (−40–55% radiator mass via T⁴), and a
  credible block-upgraded Neutron (~12–13 t SSO) — together move the flyability
  ceiling enough that the architecture *reaches* the Vera Rubin generation, the
  first generation whose payback (~2 yr) clears the ~2–3 yr obsolescence window.**
  The crossover is resolved, not stranded.
- **State the reconciled flyability ceiling.** A 1-rack reusable node:
  **~200–250 kW baseline Neutron; ~270–320 kW baseline + hot-loop; ~430–470 kW
  block-upgraded + hot-loop.** The wave-4 effective ~163–214 kW figure is
  superseded — it omitted the SSO correction and the hot-loop lever.
- **Sharpen V1 vs V2.** V1 (GB300, baseline Neutron) is **build-to-learn**, ~3 yr
  payback at the upper edge of the window — finance it as learning + strategic
  position, not profit; and **time it now**, because the baseline-vehicle window is
  GB200/GB300-class racks in 2025–2026. V2 (a full ~300 kW Vera Rubin node on a
  block-upgraded Neutron + hot-loop) is the **standalone-profitable product**, ~2 yr
  inference-service payback — gated on the block-upgrade being pursued.
- **Correct the "2 racks on a block-upgraded Neutron" expectation.** The mass
  model does not support a 2-rack node on any Neutron. The block-upgrade buys
  ~one more *power* generation per single-rack node (a full Rubin node), not a
  second rack. Architecture stays 1 rack / node, 1 node / launch.
- **Adopt the honest three-tier premium framing.** (a) *Pre-favorable* (V1): ~5–10×
  terrestrial cost/token, not cost-competitive — sold for learnings + strategic
  position + a narrow set of sovereign/dedicated-capacity buyers. (b)
  *Premium-but-viable* (V2): ~1.5–2.5× terrestrial, customers plausibly pay ~50–100%
  more per token for dedicated, isolated, 24/7, sovereign orbital capacity they
  cannot get on the ground — this is the real business. (c) *Favorable*: payback
  closes cleanly at scale / next launch generation, premium toward ~0–25%. State
  plainly: a ~50% premium is plausible; a 1,000× premium is not, and the thesis
  never needs it.
- **Name the economic case conditional, precisely.** The favorable verdict holds
  *only* under the inference-service (token-selling) revenue model — at raw IaaS
  rates even V2 is marginal. The thesis closes on selling competitive frontier-model
  inference, not GPU-hours.
- **Keep the dominant risks named:** Neutron's unpublished SSO payload; the
  block-upgrade dependency; the deployable-radiator capability gap and its
  un-quoted cost; coolant-loop reliability as the leading whole-node-kill mode;
  and the absence of observed willingness-to-pay data for orbital inference.
- **Carry forward unchanged from Rev 3:** no physics wall; whole intact racks as
  the Starcloud differentiator; 1 rack/node, 1 node/launch; dawn-dusk SSO;
  hubs-not-homes (≥4 diverse modest-aperture optical ground stations); a modest
  RF sliver alongside optical primary; compete on cadence, time-to-orbit and
  node-level service, not $/kg; ~$15–20B/GW-yr gross IaaS (~$8M/rack-yr) and
  ~$25–50B/GW-yr gross inference-service (~$16M/rack-yr) as the revenue figures.

---

*End of wave-5 synthesis.*
