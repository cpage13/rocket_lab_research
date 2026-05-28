# Optimized Build Strategy — Orbital AI-Inference Data Center on Neutron

*A cooperative Engineer ↔ CFO refinement document. See [README.md](README.md) for the rules.*
*Round 1 — Chief Engineer — 2026-05-17.*

> **Historical boundary note (2026-05-25).** This strategy document is retained
> as a research/history artifact. References to `CONCLUSION.md` below refer to
> the former model-run summary artifact that no longer lives in `research/`.
> Current reviewed conclusions live outside the research corpus under
> `data_center/`; this document keeps its historical citations as plain text so
> the research folder does not depend on a removed conclusion file.

---

## Round 1 — Chief Engineer

### Engineer's summary

If we engineer this for greatness, the venture is **a fleet of self-contained,
laser-meshed, single-rack inference satellites in dawn-dusk sun-synchronous
orbit, built as a deliberate two-generation program.** The core engineering
choices:

1. **The node is one intact NVL72-class rack** flown as a complete spacecraft —
   never two racks, because a 2-rack node exceeds even an expendable Neutron's
   mass budget ([node_mass_model.md §6](../node_design/node_mass_model.md)).
   Models too big for one rack are split across *separate* laser-linked
   single-rack satellites by pipeline/expert parallelism
   ([multi_rack_inference.md §5–6](../llm_compute/multi_rack_inference.md)).
2. **The single highest-leverage design move is the hot-loop thermal
   architecture** — riding the warm-water cooling trajectory the GPU industry
   is already on to push the radiator surface to ~70–80 °C, cutting the
   heaviest subsystem's mass ~40–55 % via the Stefan-Boltzmann T⁴ term
   ([hot_chip_thermal_trajectory.md](../node_design/hot_chip_thermal_trajectory.md)).
3. **The build-to-learn arc is the program, not a phase.** V1 (GB300-class,
   baseline reusable Neutron) is engineered to *prove* the hard subsystems and
   is financed as a learning + strategic-position asset; V2 (Vera Rubin-class,
   block-upgraded Neutron + hot-loop) is the standalone-profitable product
   ([wave5_synthesis.md §3–4](../synthesis/wave5_synthesis.md)).
4. **Every node is designed to degrade gracefully** — a partitioned pool of
   compute with N+1 cooling and many small NVLink fault domains, planned to
   glide from 100 % to ~78 % capacity over a 3-year life rather than fail on a
   cliff ([reliability_failure_handling.md §5–7](../node_design/reliability_failure_handling.md)).

This Round-1 document designs the strongest *real* build — ambitious, but it
proposes nothing the project research rules out. The CFO will pressure-test the
economics next; where this document carries cost numbers they are flagged as
the weakest inputs and explicitly handed to the CFO.

**Engineer's confidence: medium-high on the architecture, medium on the
schedule and the block-upgrade dependency.** No physics wall stands in the way
([wave5_synthesis.md §7](../synthesis/wave5_synthesis.md)); the residual risk
is engineering execution on the radiator, the block-upgrade being pursued, and
two unpublished Rocket Lab numbers (SSO payload, fairing volume).

---

## 1. The node — the best 1-rack design

The unit of the architecture is **one complete inference satellite carrying one
intact NVL72-class server rack.** This is fixed: a 1-rack node is ~5.6–8.6 t
and flies on a reusable Neutron; a 2-rack node is ~10.7–16.6 t and exceeds even
the ~11 t expendable SSO budget
([node_mass_model.md §6](../node_design/node_mass_model.md);
[wave5_synthesis.md §2.4](../synthesis/wave5_synthesis.md)). One rack already
holds and serves a whole 1–2 T-parameter frontier model
([LIBRARY.md](../LIBRARY.md), inference_scaling.md takeaway).

### 1.1 GPU generation — design V1 to GB300, architect for Vera Rubin

- **V1 flies a space-modified NVIDIA GB300 NVL72** (~135 kW TDP, ~155 kW peak,
  ~1.36 t as the integrated compute cabinet —
  [node_mass_model.md §1](../node_design/node_mass_model.md)). It is the
  buildable-now part, and the data-science model shows the baseline-vehicle
  window is GB200/GB300-class racks in roughly 2025–2026
  ([wave5_synthesis.md §4.1](../synthesis/wave5_synthesis.md)) — so V1 must be
  timed now, not deferred.
- **The node structure, bus, thermal loop and deployables are architected for a
  ~300 kW Vera Rubin NVL72/144** from day one, so V2 is a payload swap onto a
  proven platform, not a clean-sheet redesign. Rubin is the first generation
  whose payback (~2 yr inference-service) clears the ~2–3 yr GPU obsolescence
  window ([wave5_synthesis.md §3](../synthesis/wave5_synthesis.md)).
- **Rubin Ultra (~600 kW) is explicitly out of scope as an intact node** — it
  exceeds even a block-upgraded Neutron + hot-loop (~430–470 kW ceiling). If
  Rubin-Ultra-class compute is ever needed, it is reached by laser-meshing
  multiple sub-600 kW nodes, not by flying one
  ([wave5_synthesis.md §2.4, §3](../synthesis/wave5_synthesis.md)).

### 1.2 The hot-loop thermal architecture — the decisive subsystem

The radiator is the single heaviest power-scaling subsystem and the *only* one
with a 4th-power improvement lever
([hot_chip_thermal_trajectory.md §5](../node_design/hot_chip_thermal_trajectory.md)).
The design:

- **Single-phase warm-water loop, radiator surface targeted at ~70–80 °C.**
  This rides the industry's own warm-water trajectory — Vera Rubin is spec'd
  for 45 °C supply / ~65 °C return water with "no chillers," and ASHRAE has
  added W40/W+ liquid classes for exactly this
  ([hot_chip_thermal_trajectory.md §2](../node_design/hot_chip_thermal_trajectory.md)).
  Moving the radiator surface from a conservative ~40 °C to ~80 °C roughly
  doubles heat rejection per m² (275 → 561 W/m²) and **cuts radiator mass
  ~51 %** ([hot_chip_thermal_trajectory.md headline table](../node_design/hot_chip_thermal_trajectory.md)).
- **Resolve the hot-loop ↔ HBM-thermal tension by decoupling, not by cooking
  silicon.** Chip junction temperature and radiator surface temperature are
  separated by the loop+cold-plate ΔT. GPU Tjmax has barely moved (~83–85 °C
  across H100 → Blackwell → Rubin), and running the *junction* hot carries an
  Arrhenius penalty (~2× wear-out failure rate per +10 °C) plus HBM
  thermal-fatigue exposure
  ([hot_chip_thermal_trajectory.md §4](../node_design/hot_chip_thermal_trajectory.md)).
  The design rule is therefore firm: **bank the radiator-mass win by running
  the loop and radiator hot, and defend the junction near today's ~70 °C with
  ΔT budget** — colder cold-plates, higher coolant flow, full cold-plate
  coverage of the ~10 % of components currently air-cooled (DIMMs, VRMs, NICs,
  switch optics — [node_mass_model.md §2](../node_design/node_mass_model.md)).
- **Reserve a pumped-two-phase loop as a V2 upgrade path.** A two-phase loop can
  hold a hotter, near-isothermal radiator while keeping the evaporator at the
  chip cooler — the gateway to the 100 °C+ radiator columns — but it is not
  required for the ~300 kW V2 node and carries its own mass/reliability cost
  ([hot_chip_thermal_trajectory.md §3.4, open Q3](../node_design/hot_chip_thermal_trajectory.md)).
  V1 ships single-phase; two-phase is a deliberate later option.
- **Honest open item:** the hot-loop verdict assumes the junction can be
  defended with ΔT budget at a ~70–80 °C radiator surface — plausible but not
  yet closed by a real chip→coolant→panel thermal-resistance model. That model
  is the #1 engineering action item (§7)
  ([hot_chip_thermal_trajectory.md open Q1–Q3](../node_design/hot_chip_thermal_trajectory.md);
  [wave5_synthesis.md §7](../synthesis/wave5_synthesis.md)).

### 1.3 Solar and deployable radiator

- **Solar array: advanced GaAs roll-out, ~545 m²/rack for a ~150 kW node**,
  ~370–460 m² for a power-capped Rubin node. Use Rocket Lab's in-house
  IMM-β/quad-junction cells (~33 % efficient, radiation-hard, >40 % lighter
  than typical space cells — [space_hardware_capabilities.md §1.2](../rocket_lab/space_hardware_capabilities.md)).
  GaAs over silicon for V1: silicon needs ~1.5× the area for the same power,
  and the larger blanket/boom/deployment structure offsets the per-cell mass
  saving ([node_mass_model.md §3](../node_design/node_mass_model.md)). Reserve
  Rocket Lab's silicon data-center array as a cost-down option for V2 at
  fleet scale, where supply-chain resilience and $/W matter more than areal
  mass ([space_hardware_capabilities.md §1.4](../rocket_lab/space_hardware_capabilities.md)).
- **Deployable radiator: this is Rocket Lab's one capability gap and the
  program's biggest single engineering risk.** Rocket Lab owns essentially the
  whole node stack — solar, bus, mechanisms (post-Motiv), laser comms, launch —
  but does *not* build large deployable radiators
  ([space_hardware_capabilities.md §6](../rocket_lab/space_hardware_capabilities.md)).
  The strategy: **develop the hot-loop deployable radiator as an in-house
  product, treating it as the program's flagship technology investment**, drawn
  from Rocket Lab's composite-structures heritage and (post-Motiv)
  deployment-mechanism capability — with a parallel make-vs-buy vendor
  competition de-risking schedule. A V1 node needs ~300 m² (working planning
  figure; project range 200–430 m²/rack —
  [node_mass_model.md §4](../node_design/node_mass_model.md)) of
  hot-loop radiator at a target areal density of ~3–5 kg/m².
- **Co-mount the radiator on the back of the solar array where geometry
  allows.** The array front faces the sun, its back faces deep space — a
  documented, NASA-flown technique. For dawn-dusk SSO the geometry is stable;
  co-mounting is best modeled as *sharing deployment structure* (booms,
  gimbals, HDRMs), trimming deployment-structure mass rather than radiator
  panel mass ([node_mass_model.md §4(a)](../node_design/node_mass_model.md)).

### 1.4 Bus, comms terminals and propulsion

- **Bus: a high-power derivative of Flatellite**, Rocket Lab's flat,
  stackable, mass-manufacturable, Neutron-matched platform, integrating
  in-house propulsion, avionics, Sinclair reaction wheels and star trackers,
  Motiv solar-array drives and gimbals, and PMAD
  ([space_hardware_capabilities.md §4](../rocket_lab/space_hardware_capabilities.md)).
  Flatellite's published mass/power are estimates; **data-center-scale power
  management (PMAD/PCDU) at hundreds of kW is a partial capability gap** that
  must be developed alongside the radiator
  ([space_hardware_capabilities.md §6](../rocket_lab/space_hardware_capabilities.md)).
  Bus dry mass budget ~0.7–1.0 t for a 1-rack node
  ([node_mass_model.md §6](../node_design/node_mass_model.md)).
- **Comms: 3–4 Mynaric CONDOR-class optical terminals per node** — 2 for the
  in-string laser daisy-chain, 1 for ring closure, 1 spare/cross-link or
  ground-downlink gateway role
  ([constellation_mesh.md §5–6](../laser_comms/constellation_mesh.md)).
  Target the CONDOR Mk3.1 ~100 Gbps roadmap part; shipping Mk3 is ~2.5 Gbps,
  so the 100 Gbps terminal timeline is a named roadmap dependency
  ([optical_comms.md](../laser_comms/optical_comms.md), via
  [wave5_synthesis.md §7](../synthesis/wave5_synthesis.md)).
- **Retain a modest RF payload** (~100–250 MHz Ka-band, Rocket Lab Frontier
  software-defined radio) serving triple duty: all-weather backup for the
  cloud-vulnerable optical ground link, a low-rate direct B2B channel, and
  TT&C / out-of-band control plane
  ([rf_limited_service.md](../laser_comms/rf_limited_service.md), via
  [wave5_synthesis.md §5](../synthesis/wave5_synthesis.md)).
- **Propulsion: electric (Hall/gridded) for SSO drag make-up and end-of-life
  disposal.** A multi-hundred-m² array at 500–600 km generates real drag;
  budget ~0.25–0.5 t of EP + propellant for a 1-rack node and size formation
  station-keeping into it ([node_mass_model.md §6](../node_design/node_mass_model.md);
  [constellation_mesh.md open Q2](../laser_comms/constellation_mesh.md)).

### 1.5 Radiation-hardening for the 5-year service life

Dawn-dusk SSO at 500–600 km is a **relatively benign radiation environment**
([orbits_environment.md](../orbital/orbits_environment.md), via
[LIBRARY.md](../LIBRARY.md)). The design does *not* full-rad-harden the rack —
that would be mass-prohibitive and unnecessary. Instead:

- **Spot-shield only the most SEE-sensitive parts** — targeted tantalum/aluminum
  shields on switch and control electronics (~15–60 kg/rack —
  [node_mass_model.md §2](../node_design/node_mass_model.md)).
- **SEU (soft, recoverable) is handled by ECC on HBM, parity, watchdogs and
  memory scrubbing** — a manageable nuisance, not a node-killer
  ([reliability_failure_handling.md §4](../node_design/reliability_failure_handling.md)).
- **SEL (latch-up, destructive) is the real radiation tail risk** — commercial
  GPUs are not SEL-hardened, so add **per-domain fast current-limiting /
  power-cycle latch-up protection circuits**
  ([reliability_failure_handling.md §4, §6](../node_design/reliability_failure_handling.md)).

> **Service-life note.** The reliability research characterizes a *3-year* GPU
> economic/competitive life, not 5. The strategy distinguishes the two: the
> **GPU payload** is underwritten against a ~3-year revenue-generating life
> (after which the silicon is obsolete regardless of whether it still
> functions); the **bus, power, comms and structure** are qualified for ~5+
> years so the platform can, in principle, host a refreshed payload generation
> if an on-orbit-serviceable or replaceable-payload architecture is later
> proven. V1 assumes no on-orbit upgrade; designing the bus to outlive the
> payload is cheap insurance and a V2+ option, not a V1 commitment
> ([reliability_failure_handling.md §7](../node_design/reliability_failure_handling.md);
> [initial_thesis.md Rev 3 §1](../vision/initial_thesis.md)).

### 1.6 Redundancy and graceful degradation — design the node to survive itself

The reliability research is unambiguous: the node *will* lose GPUs in orbit
(~7–9 % annual failure rate, ~15–25 % cumulative GPU loss over 3 years), and
the thing that makes that survivable is **architecture, not burn-in**
([reliability_failure_handling.md Summary, §7](../node_design/reliability_failure_handling.md)).

- **Partition the rack into many small NVLink fault domains.** A stock NVL72
  lashes all 72 GPUs into one tightly-coupled domain where one failed GPU
  costs ~15–20 % throughput or destabilizes the rack. Re-architect into
  multiple independent inference partitions (the natural fault domain is the
  smallest GPU group holding one model replica, ~4–8 GPUs) so a dead GPU kills
  *one partition* and the scheduler stops routing to it — capacity drops
  ~1.4 %, not 15–100 %
  ([reliability_failure_handling.md §5](../node_design/reliability_failure_handling.md)).
- **N+1 cooling is mandatory.** The coolant loop / CDU is the leading
  whole-node-kill mode — a pump or CDU failure thermally shuts the rack within
  seconds, and a representative pump MTBF (~30,000 h) is inadequate for a
  3-year un-serviceable node. Fly **N+1 pumps, dual-loop / isolatable CDU,
  redundant power shelves and DC distribution with per-partition isolation**
  ([reliability_failure_handling.md §4, §6](../node_design/reliability_failure_handling.md)).
  Hot-loop operation slightly worsens the Arrhenius wear-out component of pump
  life — size the redundancy with that in mind.
- **Derate aggressively.** A space node is not chasing peak terrestrial clock;
  running GPUs/HBM cooler and at lower voltage trades a few percent of FLOPS
  for materially lower failure rate — an excellent trade when repair is
  impossible ([reliability_failure_handling.md §6](../node_design/reliability_failure_handling.md)).
- **Burn in for 1–3 weeks, not 1–2 days.** Proper space-acceptance burn-in is
  ~200–500 h, plus vibration and thermal-vacuum cycling, with a *post-vibration*
  functional re-test to catch launch-induced latent damage
  ([reliability_failure_handling.md §3](../node_design/reliability_failure_handling.md)).
- **Underwrite the business against end-of-life capacity (~75–85 % of
  beginning-of-life), not BOL** — a partitioned node glides smoothly, and that
  glide must be in the revenue model the CFO builds
  ([reliability_failure_handling.md §5, §7](../node_design/reliability_failure_handling.md)).

---

## 2. The launch & scaling plan

### 2.1 Baseline reusable Neutron for V1; the block-upgrade is the V2 critical path

> **Superseded later in this document (Round 2).** This Round-1 framing — the
> block-upgrade "on the critical path to V2 profitability" — was **overturned by
> the convergence later in this same file**: the CFO's Round 1 ("keep the
> block-upgrade as an *optimization*, never a gating dependency") and the
> Engineer's Round 2 (explicitly: "I wrote 'on the critical path to V2
> profitability' in Round 1; the CFO is right — demote it to margin upside").
> `CONCLUSION.md` Rev 6 adopts the demotion: **V2 closes on a baseline Neutron +
> hot-loop and does not depend on the block-upgrade.** Round 1 below is kept
> unedited as the debate record; read §2.1 and §7 with this correction in mind.

- **V1 flies on a baseline reusable Neutron, downrange/barge recovery** —
  ~9.5 t reusable to SSO (working figure; range 8.5–10.5 t —
  [payload_and_block_upgrade.md §2](../rocket_lab/neutron/payload_and_block_upgrade.md)).
  A V1 GB300 node masses ~6.8 t (sim mid), flying with **~2.7 t of margin** —
  comfortable, not mass-tight ([wave5_synthesis.md §4.1](../synthesis/wave5_synthesis.md)).
- **Reusable over expendable as the baseline.** Reusable downrange recovery is
  the cheaper-per-flight mode and carries enough payload (~9.5 t) for both V1
  and a power-capped Rubin V2 node. Expendable (~11 t SSO) is held as a
  contingency for an over-mass node or a schedule-driven one-off, not the
  plan. RTLS full-reuse (~6 t SSO) is under-sized — avoid it
  ([payload_and_block_upgrade.md §2–3](../rocket_lab/neutron/payload_and_block_upgrade.md)).
- **The block-upgraded Neutron (~12–13 t SSO) is on the critical path to V2
  profitability and must be actively pursued with Rocket Lab.** It is credible
  by analogy — Archimedes runs deliberately de-stressed and has shown 102 %
  power, Electron grew +33 % on the same airframe, Neutron itself grew 8→13 t
  LEO in design — but it is unannounced and realistically arrives years after
  Neutron's first operational flights
  ([payload_and_block_upgrade.md §4–5](../rocket_lab/neutron/payload_and_block_upgrade.md);
  [wave5_synthesis.md §2.1, §4.2](../synthesis/wave5_synthesis.md)). The
  block-upgrade buys *one more power generation per single-rack node* (a full
  ~300 kW Rubin node flown intact), **not a second rack**
  ([wave5_synthesis.md §4.2](../synthesis/wave5_synthesis.md)).

**Reconciled flyability ceilings** (1-rack reusable node), the design space the
launch plan operates in ([wave5_synthesis.md §2.4](../synthesis/wave5_synthesis.md)):

| Neutron configuration | 1-rack flyability ceiling | Enables |
|---|---|---|
| Baseline reusable (~9.5 t SSO) | ~200–250 kW (working ~225 kW) | GB300 node, comfortable |
| Baseline reusable + hot-loop radiator | ~270–320 kW (working ~300 kW) | Full GB300; power-capped Rubin (~190–250 kW) |
| Block-upgraded reusable (~12.5 t SSO) + hot-loop | ~430–470 kW (working ~450 kW) | Full ~300 kW Rubin, generous margin |

### 2.2 Cadence and fleet ramp — one rack per node, one node per launch

The architecture is **one rack per node, one node per launch**
([node_mass_model.md §6](../node_design/node_mass_model.md)). The ramp:

- **Phase 0 — single-node demonstrator (1 launch).** One V1 GB300 node. Proves
  the radiator deployment, hot-loop thermal ops, the partitioned-rack
  architecture, on-orbit operations, and the optical downlink. A valid
  MVP/learning asset but not a commercial service
  ([wave5_synthesis.md §5](../synthesis/wave5_synthesis.md)).
- **Phase 1 — first useful service (~4–8 nodes).** Enough for throughput,
  replica load-balancing, redundancy against a node lost to a coolant-loop
  failure, and overlapping ground-station passes
  ([wave5_synthesis.md §5](../synthesis/wave5_synthesis.md);
  [constellation_mesh.md §6](../laser_comms/constellation_mesh.md)).
- **Phase 2 — robust always-reachable network (~12–24 nodes).** Sized for both
  compute throughput and laser-mesh continuity, growing near-linearly by adding
  independent rack-replica satellites
  ([wave5_synthesis.md §5](../synthesis/wave5_synthesis.md)).
- **Phase 3 — V2 generation.** Block-upgraded Neutron + hot-loop, full ~300 kW
  Vera Rubin nodes, mass-manufactured on the Flatellite production line — the
  standalone-profitable product ([wave5_synthesis.md §4.2](../synthesis/wave5_synthesis.md)).

Cadence is set by burn-in throughput as much as by launch rate: a 1–3 week
per-rack burn-in + TVAC + vibration campaign is a real constraint on how fast
the fleet can ramp, and the number of burn-in stations must be sized to the
target deployment rate ([reliability_failure_handling.md open Q6](../node_design/reliability_failure_handling.md)).
**Compete on cadence, time-to-orbit and turnkey node-level service — not on
$/kg** ([initial_thesis.md Rev 2](../vision/initial_thesis.md)).

---

## 3. The constellation & comms

### 3.1 Formation — a tight along-track string of compute nodes

- **Orbit: ~500–600 km dawn-dusk sun-synchronous** (~97.4–97.8° inclination) —
  ~95–100 % sunlit (eclipse <5 %, so battery cycling is small), steady thermal
  state, benign radiation, and largely natural deorbit compliance with the FCC
  5-year rule ([wave5_synthesis.md §5](../synthesis/wave5_synthesis.md);
  [orbits_environment.md](../orbital/orbits_environment.md)).
- **Compute nodes fly in a tight along-track string at ~5 km rack-to-rack
  spacing** (range 1–10 km; collision-safety and station-keeping set the floor,
  not optics). At 5 km a laser link adds only ~17 µs one-way — negligible
  against a pipeline-stage compute time of hundreds of µs — so a tight cluster
  is "free" from a latency standpoint
  ([constellation_mesh.md §2–3, §6](../laser_comms/constellation_mesh.md)). The
  ~5 km figure is the softest number in the constellation design and needs a
  dedicated GNC/collision-probability analysis (§7).

### 3.2 The laser mesh

- **Each node carries 3–4 CONDOR-class optical terminals; the cluster topology
  is a daisy-chained ring** — node *k* links to node *k±1*, with a closure link
  for a second fault-tolerant path. This exactly matches pipeline parallelism
  (sequential stages → activations flow node→node down the string) and matches
  how Starlink's 9,000-laser mesh is actually built: a sparse, locally-connected
  lattice, not an all-to-all clique
  ([constellation_mesh.md §5–6](../laser_comms/constellation_mesh.md)).
- **Laser range never binds** — CONDOR Mk3 is rated to ~6,500 km, Starlink
  links routinely hold ~1,500–5,400 km; cooperating racks sit far inside that
  ([constellation_mesh.md §1](../laser_comms/constellation_mesh.md)).
- **Inference is bandwidth-light** — prompts up, tokens down, kB to a few MB
  per query — so the mesh and ground links are sized by *availability*, not
  raw throughput ([wave5_synthesis.md §5](../synthesis/wave5_synthesis.md)).

### 3.3 The relay layer — a deliberate V2 scope decision

A LEO/SSO node sees a given ground station only ~5–15 min per ~96-min orbit. A
single compute cluster is therefore **not globally always-reachable**.

- **V1/Phase 1 accepts contact gaps** — the service is batch / asynchronous
  inference (jobs queued, results returned next contact) or near-real-time
  during passes. With 3–4 diverse ground hubs there is a downlink opportunity
  on most orbits. **Do not pay for a relay constellation in V1**
  ([constellation_mesh.md §4, §6](../laser_comms/constellation_mesh.md)).
- **For always-on coverage, the V2 layer is a ring of small,
  Electron-launched, comms-only relay satellites** — cheap, light, no compute
  payload, no radiator, no large solar array — that hand the compute cluster's
  traffic down to whichever hub is currently cloud-free and sunlit. Electron is
  operational with a high success rate and is correctly sized for small relay
  satellites (it is too small for compute nodes — that is what Neutron is for)
  ([electron_specs.md](../rocket_lab/electron/electron_specs.md), via
  [LIBRARY.md](../LIBRARY.md)). A GEO relay layer is the alternative — it lifts
  contact from ~5–15 % to ~85–100 % but adds ~600 ms round-trip
  ([orbit_types_primer.md](../orbital/orbit_types_primer.md), via
  [LIBRARY.md](../LIBRARY.md)); for a latency-tolerant batch-inference service
  the Electron-launched LEO relay ring is preferred, with the connectivity
  architecture decision (LEO mesh vs. GEO relay vs. ground-diversity-only)
  flagged as an open trade (§7).

### 3.4 Ground hubs — diversity, not aperture

- **≥4 geographically diverse optical ground hubs >1,000 km apart** for ~99 %
  availability; ~10–12 for carrier-grade 99.9 %
  ([optical_ground_stations.md §3](../laser_comms/optical_ground_stations.md)).
- **Each hub is modest-aperture (0.6–1.0 m), multi-terminal (4–8 terminals)**
  with adaptive optics and a high-power multi-sub-aperture uplink. Aperture
  gain is logarithmic and no dish beats cloud — **diversity wins; do not build
  one monster telescope** ([optical_ground_stations.md](../laser_comms/optical_ground_stations.md)).
- **Customers wire into the hubs over terrestrial fiber** — hubs, not homes.
  Customers do not each run a laser terminal
  ([initial_thesis.md Rev 2](../vision/initial_thesis.md)).

---

## 4. The architecture for multi-rack models — laser-meshed single-rack satellites

The project never needs a 2-rack Neutron node, and that is an architectural
strength, not a workaround.

- **A model too big for one rack is split across separate, laser-linked,
  single-rack satellites by pipeline and/or expert parallelism**
  ([multi_rack_inference.md §5–6](../llm_compute/multi_rack_inference.md)).
- **Tensor parallelism must stay in-rack** — it needs ~NVLink-class bandwidth
  (~1.8 TB/s per GPU) with an all-reduce every layer; a 100–200 Gbps laser ISL
  is ~100–150× too slow. But this is *not* a space-specific limitation —
  tensor parallelism cannot cross a *terrestrial* rack boundary either, so any
  multi-rack model is already partitioned to confine TP within each rack
  ([multi_rack_inference.md §2.1, §5](../llm_compute/multi_rack_inference.md)).
- **Pipeline parallelism (activations at stage boundaries) and replica
  parallelism (independent model copies) survive a laser hop comfortably** —
  PP's 100–400 Gbps comfort band is exactly the CONDOR Mk3.1 envelope, and
  replica parallelism needs almost no inter-node bandwidth. Expert parallelism
  works across a short ISL with a modest throughput cost
  ([multi_rack_inference.md §2, §5](../llm_compute/multi_rack_inference.md)).
- **The vacuum speed-of-light bonus works in the project's favor** — light is
  ~47 % faster in vacuum than in fiber, so a laser ISL between close-formation
  satellites *matches or beats* a terrestrial cross-campus fiber link. The
  orbital mesh is the space-borne analogue of NVIDIA's Spectrum-XGS
  "scale-across" product, which already links data centers hundreds of km apart
  over fiber ([multi_rack_inference.md §3, §4.2](../llm_compute/multi_rack_inference.md)).
- **Capacity scales on the embarrassingly-parallel axis** — add independent
  single-rack replica satellites — so the fleet grows near-linearly with no
  special interconnect ([multi_rack_inference.md §5–6](../llm_compute/multi_rack_inference.md)).

> The one caveat the Engineer flags honestly: a PP-split model spread across N
> satellites means one satellite down takes the whole pipelined model down,
> unlike independent replicas. Mitigation: keep PP groups small (2–4
> satellites), prefer replica parallelism as the primary scaling axis, and use
> the ring topology's second path for resilience
> ([multi_rack_inference.md open Q5](../llm_compute/multi_rack_inference.md);
> [constellation_mesh.md §5](../laser_comms/constellation_mesh.md)).

---

## 5. The build-to-learn → V2 path

### 5.1 What V1 must prove

V1 (GB300-class, baseline reusable Neutron, ~4–8 nodes for first service) is
**financed and justified as build-to-learn + strategic position, not as a
standalone profit centre** — it does not pay back inside the GPU obsolescence
window (~3.1 yr inference-service payback, at the upper edge)
([wave5_synthesis.md §4.1](../synthesis/wave5_synthesis.md)). Its job is to
retire the program's hard engineering unknowns:

1. **The hot-loop deployable radiator deploys and performs** — the largest mass
   line, the biggest deployment risk, and Rocket Lab's one capability gap.
2. **Hot-loop thermal operations** — that a ~70–80 °C radiator surface is
   reachable in dawn-dusk SSO with the junction defended.
3. **The partitioned-rack architecture degrades gracefully** — that the node
   glides 100 % → ~78 % over 3 years rather than failing on a cliff.
4. **The space-modified rack survives launch and operation** — vibration,
   thermal cycling (~16,000 eclipse cycles over 3 yr), vacuum, radiation.
5. **On-orbit operations** — formation-keeping a tight string, laser-mesh link
   acquisition and hold, optical downlink through weather-diverse hubs.
6. **The customer-discovery answer** — whether sovereign/defense/frontier-lab
   buyers pay a premium for orbital inference (no observed willingness-to-pay
   data exists — [wave5_synthesis.md §6, §7](../synthesis/wave5_synthesis.md)).

### 5.2 What V2 unlocks

V2 (block-upgraded Neutron + hot-loop, full ~300 kW Vera Rubin node,
mass-manufactured) is the **standalone-profitable product** — ~2.0 yr
inference-service payback, inside the ~2–3 yr obsolescence window
([wave5_synthesis.md §4.2](../synthesis/wave5_synthesis.md)). V2 is reachable
*because* V1 proved the radiator, the hot-loop, the architecture and the
operations — the learnings compound, and rising rack price makes the fixed
launch a structurally smaller share of node cost each generation
([rack_cost_trajectory.md](../economics/rack_cost_trajectory.md), via
[wave5_synthesis.md §3](../synthesis/wave5_synthesis.md)).

**The economic verdict is conditional, and the Engineer states it plainly so
the CFO can pressure-test it:** the favorable verdict holds only under the
**inference-service revenue model** (selling competitive frontier-model tokens
with a model-value markup), not raw GPU-hour rental; and it rests on two
unpublished Rocket Lab numbers (SSO payload, fairing volume) plus an un-quoted
spacecraft-hardware cost line (~$8–35M, ~$18M mid — the weakest input in the
whole project) ([wave5_synthesis.md §3, §4](../synthesis/wave5_synthesis.md)).
The product is **never cheaper than terrestrial compute** — it is a premium
product whose buyers pay for dedicated, physically isolated, 24/7, sovereign
capacity they cannot get on the ground (5-yr grid-interconnection queues, 5-yr
transformer lead times, water-permitting moratoria); a ~50 % premium is
plausible, a 1,000× premium is not, and the thesis never needs it
([wave5_synthesis.md §6](../synthesis/wave5_synthesis.md)).

---

## 6. Key engineering risks and how to design them down

| Risk | Severity | Design-down strategy |
|---|---|---|
| **Deployable radiator — capability gap, mass driver, deployment risk** | High | Develop in-house as the flagship technology investment (composite + Motiv deployment heritage); run a parallel make-vs-buy vendor competition; hot-loop cuts the mass ~40–55 %; prove deployment on the Phase-0 demonstrator before committing the fleet ([space_hardware_capabilities.md §6](../rocket_lab/space_hardware_capabilities.md); [hot_chip_thermal_trajectory.md](../node_design/hot_chip_thermal_trajectory.md)). |
| **Hot-loop ↔ HBM-thermal tension** | Medium-high | Decouple junction from radiator via loop ΔT; defend the junction near ~70 °C; close the chip→coolant→panel thermal-resistance model before detailed design; reserve two-phase loop as a V2 option ([hot_chip_thermal_trajectory.md §4–5](../node_design/hot_chip_thermal_trajectory.md)). |
| **Coolant loop — leading whole-node-kill mode** | High | N+1 pumps, dual-loop/isolatable CDU, per-partition isolation; size redundancy for hot-loop-worsened Arrhenius wear ([reliability_failure_handling.md §4, §6](../node_design/reliability_failure_handling.md)). |
| **GPU attrition / un-serviceability** | Medium (plannable) | Partitioned NVLink fault domains, derating, 1–3 week burn-in + TVAC + post-vibration re-test; underwrite the business at ~75–85 % EOL capacity ([reliability_failure_handling.md §5, §7](../node_design/reliability_failure_handling.md)). |
| **Block-upgraded Neutron — V2 profitability depends on it** | Risk (uncommitted) | Engage Rocket Lab on the uprate roadmap now; credible by analogy (Electron +33 %, de-stressed Archimedes) but unannounced; V1 is designed to need only baseline Neutron so the program is not stranded if the upgrade slips ([payload_and_block_upgrade.md §5](../rocket_lab/neutron/payload_and_block_upgrade.md)). |
| **Neutron SSO payload + fairing volume unpublished** | Unresolved (largest physical unknown) | Pursue Rocket Lab directly; ±1 t of SSO payload swings the flyability ceiling ±~40 kW; design V1 with ~2.7 t of mass margin so the uncertainty does not bite ([payload_and_block_upgrade.md §2](../rocket_lab/neutron/payload_and_block_upgrade.md)). |
| **Launch-vibration latent damage** | Medium | Vibration-test the flight rack to launch levels; pot/stake heavy components and the NVLink copper spine; *post-vibration* functional re-test ([reliability_failure_handling.md §4](../node_design/reliability_failure_handling.md)). |
| **Weather-limited optical ground link** | Risk (well-characterized) | ≥4 diverse hubs >1,000 km apart; modest RF sliver as all-weather backup; batch-inference service model tolerates handoff jitter ([optical_ground_stations.md](../laser_comms/optical_ground_stations.md)). |
| **CONDOR Mk3.1 100 Gbps timeline** | Roadmap dependency | Mesh sized for availability not throughput; PP/replica parallelism is tolerant; shipping Mk3 (~2.5 Gbps) supports replica-parallel scaling even if Mk3.1 slips ([wave5_synthesis.md §7](../synthesis/wave5_synthesis.md)). |
| **"1.36 t rack scope" definition** | Foundational, cheap to resolve | Confirm whether the intact rack includes separate switch/CDU/PDU sub-racks before detailed design — if so every mass figure rises and the ceiling drops ([node_mass_model.md open Q8](../node_design/node_mass_model.md)). |
| **Competitive timing** | Strategic | Time V1 now — the baseline-vehicle window is GB200/GB300-class racks in 2025–2026, and being the operational Neutron-class orbital-compute prime before Starcloud's Starship-gated product (~2028–2029) is the strategic prize ([wave5_synthesis.md §7](../synthesis/wave5_synthesis.md); [starcloud.md](../competitors/starcloud.md)). |

No item above is a physics wall — every one is an engineering or schedule
problem ([wave5_synthesis.md §7](../synthesis/wave5_synthesis.md)).

---

## 7. Engineer's priority action list (handing the baton to the CFO)

> **Note on item 5 (forward cross-reference).** Item 5 below — "V2 profitability
> is gated on" the block-upgrade — carries the Round-1 framing that was
> **overturned by the Round-2 convergence in this same document** and by
> `CONCLUSION.md` Rev 6: V2 closes on a baseline Neutron + hot-loop, and the
> block-upgrade is **margin upside, not a gating dependency**. Engaging Rocket
> Lab on the block-upgrade roadmap remains worthwhile — but as upside, not as
> the V2 critical path. Round 1 is preserved unedited as the debate record.

The engineering items most decision-relevant to the CFO's economic
pressure-test:

1. **Close the chip→coolant→panel thermal-resistance model** — validates the
   hot-loop ~70–80 °C radiator surface with the junction defended, and pins the
   200–430 m² radiator-area range ([wave5_synthesis.md §8](../synthesis/wave5_synthesis.md)).
2. **Deployable-radiator make-vs-buy + a real cost number** — Rocket Lab's one
   capability gap; the biggest un-quoted mass and cost line.
3. **Replace the ~$8–35M spacecraft-hardware cost estimate with a bottom-up
   build-up** — the weakest input in the project; it decides whether V2 pays
   back at ~2 yr ([wave5_synthesis.md §4.2, §8](../synthesis/wave5_synthesis.md)).
4. **Confirm Neutron SSO payload and usable fairing volume with Rocket Lab.**
5. **Engage Rocket Lab on the block-upgrade roadmap** — V2 profitability is
   gated on it.
6. **Customer willingness-to-pay discovery** — test the ~50 % premium with
   sovereign/defense/frontier-lab buyers; the highest-value commercial unknown.
7. **GNC/collision-probability analysis** to firm up the ~5 km formation
   spacing and station-keeping propellant budget.
8. **Connectivity architecture decision** — Electron-launched LEO relay ring
   vs. GEO relay vs. ground-diversity-only.

**Handoff to the CFO.** This Round-1 strategy commits to: one intact rack per
node, one node per launch; the hot-loop thermal architecture as the decisive
mass lever; an in-house deployable radiator as the flagship technology
investment; a partitioned, N+1-cooled, gracefully-degrading node; baseline
reusable Neutron for V1 with the block-upgrade as the V2 critical path; a tight
along-track laser-meshed string scaling 1 → 4–8 → 12–24 nodes; an
Electron-launched relay ring deferred to V2; and the build-to-learn → V2 arc as
the program's spine. The Engineer's open question for the CFO: **given the
~$65–95M internal V1 node cost and the conditional (~2 yr, inference-service)
V2 payback, how should the program sequence capital across the Phase 0 → 3
ramp, and where should we economize versus where the engineering says do not
cut?** The radiator, the N+1 cooling, the burn-in campaign and the 3–4 optical
terminals per node are, in the Engineer's view, the lines *not* to cut.

---

## Sources

Project documents:
- [strategy/README.md](README.md) — the rules of this Engineer↔CFO loop.
- [vision/initial_thesis.md](../vision/initial_thesis.md) — Rev 2, 3, 4.
- [synthesis/wave5_synthesis.md](../synthesis/wave5_synthesis.md) — §2 re-baseline, §3 crossover, §4 V1/V2 cases, §5 strawman, §6 premium tiers, §7 risks, §8 next steps.
- [node_design/node_mass_model.md](../node_design/node_mass_model.md) — §1 GB300, §2 space-modified rack, §3 solar, §4 radiator + co-mounting, §6 per-node mass, open Q8.
- [node_design/hot_chip_thermal_trajectory.md](../node_design/hot_chip_thermal_trajectory.md) — headline table, §2 warm-water trajectory, §3 orbital payoff, §4 reliability tradeoff, §5 verdict.
- [node_design/reliability_failure_handling.md](../node_design/reliability_failure_handling.md) — §3 burn-in, §4 space failure modes, §5 graceful degradation, §6 redundancy, §7 verdict.
- [node_design/solar_radiator_trajectory.md](../node_design/solar_radiator_trajectory.md) — solar/radiator mass scaling (via LIBRARY).
- [llm_compute/multi_rack_inference.md](../llm_compute/multi_rack_inference.md) — §2 parallelism types, §3 terrestrial inter-rack, §4 optical ISL, §5–6 verdict and thesis implication.
- [laser_comms/constellation_mesh.md](../laser_comms/constellation_mesh.md) — §1 ISL range, §2–3 spacing/latency, §4 node count, §5 topology, §6 strawman spec.
- [laser_comms/optical_ground_stations.md](../laser_comms/optical_ground_stations.md) — diversity over aperture, ≥4 hubs.
- [laser_comms/optical_comms.md](../laser_comms/optical_comms.md), [laser_comms/rf_limited_service.md](../laser_comms/rf_limited_service.md) — CONDOR Mk3/Mk3.1, RF sliver.
- [rocket_lab/space_hardware_capabilities.md](../rocket_lab/space_hardware_capabilities.md) — §1 solar, §4 Flatellite bus, §6 capability coverage and the radiator gap.
- [rocket_lab/neutron/payload_and_block_upgrade.md](../rocket_lab/neutron/payload_and_block_upgrade.md) — §2 SSO payload, §3 recovery modes, §4–5 block-upgrade.
- [rocket_lab/electron/electron_specs.md](../rocket_lab/electron/electron_specs.md) — Electron sizing for relay satellites.
- [orbital/orbits_environment.md](../orbital/orbits_environment.md), [orbital/orbit_types_primer.md](../orbital/orbit_types_primer.md) — dawn-dusk SSO, relay geometry.
- [economics/rack_cost_trajectory.md](../economics/rack_cost_trajectory.md) — rising rack price shrinks the launch share.
- [competitors/starcloud.md](../competitors/starcloud.md) — competitive timing.
- [LIBRARY.md](../LIBRARY.md) — document catalog and cross-references.

*End of Round 1 — Chief Engineer. The CFO responds next.*

---

## Round 1 — CFO

*Round 1 — CFO — 2026-05-17. This section is appended, not a rewrite. Where the
Engineer is right, it says so and builds on it; where the ambition outruns the
economics, it re-scopes with the financial reasoning.*

### CFO's summary

The Engineer's architecture is sound and I am keeping its spine intact: one
intact rack per node, the hot-loop radiator as the decisive mass lever, the
partitioned/N+1-cooled node, the build-to-learn → V2 arc, and the laser-meshed
single-rack constellation. None of that is where the money goes wrong.

**The single biggest financial change I am making is to the *node-ramp pace*,
not to any subsystem.** The strategy as written deploys ahead of earnings hard
enough to drive a **~$1.15B peak funding requirement** and a **~year-19–20
cumulative crossover** (retired `INVESTOR_PROJECTION.md`,
central-case pro-forma). That is financeable only as patient strategic capital,
and it is *fragile*: at a +25% premium or a 2–3-year GPU life the venture never
crosses inside 25 years (retired `INVESTOR_PROJECTION.md`,
"Why you might not"). The fix is not to abandon scale — it is to **gate each
phase on a financial milestone**, slow the steady-state cadence, and re-scope
the program so the premium is *earned by design* rather than assumed.

The three things I am changing:

1. **Re-scope the deployable radiator from "flagship in-house product" to
   "buy/partner first, internalize only if V2 economics demand it."** It is the
   Engineer's #1 *engineering* risk; it is also the largest *un-quoted* cost
   line ([wave5_synthesis.md §7](../synthesis/wave5_synthesis.md)), and a
   first-of-kind in-house radiator program is exactly the kind of fixed R&D that
   pushes the ~$485M R&D burn higher and the crossover later.
2. **Slow the ramp and gate it.** The pro-forma's `0,0,1,2,4,6,7,8,7,7,7`
   deployment schedule (retired `INVESTOR_PROJECTION.md`,
   "node-count ramp") is the proximate cause of the ~$1.15B peak. Gate Phase 1 →
   Phase 2 on observed willingness-to-pay, not on a calendar.
3. **Economize hard on the ground segment and the relay layer; spend heavily
   only on the moat.** The ground segment is the *binding all-in cost variable*
   (retired `CONCLUSION.md` §1) — keep it at the lean ~$150M end. The
   relay ring stays deferred. The moat — the attributes a sovereign buyer pays a
   premium for — is where capital should concentrate.

**CFO confidence: medium-high on the unit economics (a single node is a sound
asset — ~2.5–2.8 yr per-node payback at +50%, retired `CONCLUSION.md`
Profitability section);
medium on the venture-level crossover, which rests on four labelled,
non-cited assumptions; low on the unobserved premium, which is the entire
business case.**

---

### What to keep — engineering choices that are also financially sound

These are correct and I am building on them, not cutting them.

- **One intact rack per node, one node per launch.** This is financially as well
  as physically right. It makes the fleet a portfolio of identical, independently
  financeable units that scale near-linearly
  ([multi_rack_inference.md §5–6](../llm_compute/multi_rack_inference.md)), and
  it lets each node be underwritten on its own ~2.5–2.8-yr payback
  (retired `CONCLUSION.md` Profitability §1). A 2-rack node would
  concentrate risk and break the clean unit economics. Keep it.

- **The hot-loop radiator as the decisive mass lever.** This is the highest-ROI
  engineering choice in the document. Cutting radiator mass ~40–55% via the T⁴
  term ([hot_chip_thermal_trajectory.md](../node_design/hot_chip_thermal_trajectory.md))
  is what lifts the flyability ceiling to ~300 kW and lets the architecture
  *reach the Vera Rubin generation* — the first generation whose ~2-yr payback
  clears the obsolescence window ([wave5_synthesis.md §3](../synthesis/wave5_synthesis.md)).
  Without it there is no V2 and no profitable product. This deserves heavy R&D
  spend (see *Where to spend*). Keep it, and fund it as a priority.

- **The build-to-learn → V2 arc as the program's spine.** Financing V1 as a
  learning + strategic-position asset rather than a profit centre is exactly
  right and matches the investor framing — V1's ~3.1-yr inference payback sits at
  the upper edge of the GPU window and does not stand alone
  ([wave5_synthesis.md §4.1](../synthesis/wave5_synthesis.md)). The honest
  framing protects the venture from being mis-sold as fast-payback. Keep it.

- **Graceful degradation, N+1 cooling, the 1–3-week burn-in.** The Engineer is
  right that these are not the lines to cut. The coolant loop is the leading
  whole-node-kill mode ([reliability_failure_handling.md §4](../node_design/reliability_failure_handling.md)),
  and a node lost on-orbit is a ~$35–65M write-off with zero salvage. N+1 (the
  conclusion argues realistically N+2) cooling and a proper burn-in are cheap
  insurance against a catastrophic, uninsurable loss — and the 5-year service
  life they protect is itself a make-or-break economic variable: a 2–3-yr
  effective life makes the venture never cross
  (retired `CONCLUSION.md` §2 downside addendum). Keep all of it; this
  is risk-reduction spend, not gold-plating.

- **The 3–4 optical terminals per node and the modest RF sliver.** Comms
  availability is what makes the service *sellable* — a node that cannot be
  reliably reached cannot earn. The terminals are a small fraction of a ~$35–65M
  node and the RF backup is cheap insurance against the cloud-vulnerable optical
  ground link ([rf_limited_service.md](../laser_comms/rf_limited_service.md)).
  Keep them.

- **Dawn-dusk SSO, spot-shielding only, time V1 now.** The orbit choice avoids
  battery-cycling cost and gives benign radiation
  ([orbits_environment.md](../orbital/orbits_environment.md)); not full-rad-
  hardening the rack avoids mass-prohibitive cost; and timing V1 to the
  GB300 window is a real strategic-option value — being the operational
  Neutron-class prime before Starcloud's Starship-gated product
  ([starcloud.md](../competitors/starcloud.md)). All financially sound.

---

### What to cut, defer, or re-scope — where the ambition outruns the economics

- **Re-scope the in-house deployable radiator: buy/partner first.** The Engineer
  proposes developing the hot-loop deployable radiator "as the program's
  flagship technology investment" in-house, with a make-vs-buy competition as a
  *de-risking* sidecar. **I invert that priority.** The radiator is simultaneously
  (a) Rocket Lab's one genuine capability gap
  ([space_hardware_capabilities.md §6](../rocket_lab/space_hardware_capabilities.md)),
  (b) the biggest single deployment risk, and (c) the largest un-quoted cost line
  in the whole project ([wave5_synthesis.md §7](../synthesis/wave5_synthesis.md)).
  Building a first-of-kind deployable-radiator product in-house is precisely the
  category of fixed, front-loaded R&D that inflates the ~$485M R&D burn and
  pushes the crossover past year 20 (retired `INVESTOR_PROJECTION.md`,
  "Fleet costs"). The financially correct sequence:
  1. **V1 — buy or partner.** Procure the V1 radiator from an established
     deployable-thermal vendor against a fixed-price contract. This converts the
     single weakest cost input into a *quoted* number and de-risks the schedule.
     The Engineer's own action list already asks for "a real cost number"
     ([§7 item 2](#7-engineers-priority-action-list-handing-the-baton-to-the-cfo));
     a vendor quote *is* that number.
  2. **Internalize only if the V2 fleet math demands it.** In-housing makes
     financial sense only at fleet scale, where unit-cost reduction on a
     mass-manufactured radiator outweighs the fixed development cost — i.e. a
     Phase-3/V2 decision, made *after* V1 has proven the thermal architecture and
     *after* the willingness-to-pay gate has confirmed there is a fleet to build.
     Until then, an in-house radiator program is capital spent ahead of demand.
  This is not "cut the radiator" — it is the same radiator, financed so the
  fixed R&D is not committed before the revenue that justifies it is observed.

- **Slow the node-ramp and gate it on willingness-to-pay.** The deploy-ahead-of-
  earnings ramp is the proximate driver of the ~$1.15B peak funding requirement
  (retired `INVESTOR_PROJECTION.md`, "Why the
  venture crossover is so much later"). The strategy should not commit to the
  full `1→4–8→12–24` ramp on a calendar. Instead:
  - **Phase 0 → Phase 1 is gated on V1 demonstrator success** (radiator
    deployment, hot-loop thermal ops, graceful degradation) — an engineering
    gate, as the Engineer has it. Keep.
  - **Phase 1 → Phase 2 must be gated on a financial milestone: a signed
    sovereign/defense/frontier-lab anchor customer at or above the ~+50% premium.**
    Willingness-to-pay for orbital inference is *entirely unobserved*
    ([wave5_synthesis.md §6.2](../synthesis/wave5_synthesis.md);
    [hyperscaler_margins.md Open Q](../economics/hyperscaler_margins.md)). Scaling
    a 12–24-node fleet *before* a customer has confirmed the premium is the single
    most expensive way to discover the premium does not exist. The +25%-premium
    downside — where the venture never crosses
    (retired `INVESTOR_PROJECTION.md`, "Why you
    might not" item 2) — should be discovered with ~$300M of Phase-0/1 capital at
    risk, not ~$1.15B.
  - **Cap the steady-state cadence below ~7 nodes/yr until the cumulative line
    has turned.** A growing fleet is perpetually cash-hungry
    (retired `INVESTOR_PROJECTION.md`, "deploy-
    ahead-of-earnings"). Slowing replacement-plus-growth deployment trades a later
    revenue peak for a materially lower funding peak — the right trade for a
    venture whose binding constraint is patient capital, not demand.

- **Keep the block-upgrade as an *optimization*, never a gating dependency —
  and the strategy should say so in the financing plan.** The Engineer already
  designs V1 to need only baseline Neutron, which is correct. But the document
  still describes the block-upgrade as "on the critical path to V2
  profitability." Financially, the program must be structured so that **V2 is
  viable on a baseline-Neutron + hot-loop power-capped Rubin node (~190–250 kW)**
  ([wave5_synthesis.md §2.4, §3](../synthesis/wave5_synthesis.md)) — because the
  block-upgrade is unannounced, years post-debut, and outside Rocket Lab's
  committed roadmap ([payload_and_block_upgrade.md §5](../rocket_lab/neutron/payload_and_block_upgrade.md)).
  No investor should be asked to fund a venture whose profitable product is
  gated on an uncommitted rocket variant. Treat the block-upgrade as upside that
  improves margin per node, not as a precondition for V2 closing. Engage Rocket
  Lab on the roadmap (cheap), but do not let V2's business case depend on it.

- **Hold the relay layer deferred to V2 — and re-confirm it earns its cost even
  then.** The Engineer correctly defers the Electron-launched relay ring out of
  V1. I keep that. I add: the relay ring is a *discretionary* capex line whose
  justification is always-on coverage, and the service is explicitly
  batch/async, latency-tolerant inference
  ([wave5_synthesis.md §5](../synthesis/wave5_synthesis.md)). Before V2 commits
  to a relay constellation, the connectivity decision (LEO relay vs. GEO relay
  vs. ground-diversity-only) must be made on a **cost-per-availability-point**
  basis — ground-station diversity alone reaches ~99%
  ([optical_ground_stations.md §3](../laser_comms/optical_ground_stations.md)),
  and a relay ring should only be funded if a customer is paying specifically for
  the last availability points. Defer, and gate on a revenue justification.

---

### Where to spend vs. economize — capital allocation

The principle, drawn straight from the margin research: **margin in cloud pools
at the layers with a moat — the chip and the attribute-rich integrated service —
and the commodity middle is thin** ([hyperscaler_margins.md §1.4](../economics/hyperscaler_margins.md)).
The orbital venture's moat is the *scarce attribute* (dedicated, sovereign,
physically isolated, zero-grid 24/7 capacity), not FLOPs. Capital should
concentrate on what creates and defends that attribute.

**Spend heavily (the moat-creating pieces):**

- **The hot-loop thermal architecture and the chip→coolant→panel thermal model.**
  This is the lever that makes V2 exist at all
  ([wave5_synthesis.md §3](../synthesis/wave5_synthesis.md)). Closing the
  thermal-resistance model is the Engineer's #1 action item and it is cheap
  relative to its decision value — fund it first, fully.
- **Reliability and graceful degradation.** Every on-orbit node loss is an
  uninsurable ~$35–65M write-off and a hit to the 5-year-life economics the whole
  case depends on retired `CONCLUSION.md` §2. N+1/N+2 cooling,
  derating, the full burn-in campaign — spend here without flinching.
- **Customer willingness-to-pay discovery.** The cheapest, highest-leverage
  spend in the program. The entire venture pivots on whether a buyer pays the
  ~+50–100% premium (retired `INVESTOR_PROJECTION.md`,
  "Why you might not"; [hyperscaler_margins.md §3](../economics/hyperscaler_margins.md)).
  Fund sovereign/defense/frontier-lab customer discovery *now*, ahead of Phase 1
  — a signed anchor customer is the Phase-1→2 gate.
- **The attribute wrapper itself** — the things a sovereign buyer is actually
  paying the premium *for*: physical isolation, single-tenancy, jurisdictional
  separation, security/SLA, schedule certainty. The sovereign-cloud precedent
  shows buyers pay +10–30% for *isolation/residency attributes alone*
  ([hyperscaler_margins.md §3](../economics/hyperscaler_margins.md)); the orbital
  premium must be *earned* by delivering a genuinely scarce version of that, not
  assumed. This is a product-and-go-to-market spend, not a hardware line, and the
  strategy currently under-weights it.

**Economize hard (the lean lines):**

- **The ground segment — keep it at the lean ~$150M end of the $100–500M band.**
  This is the *binding all-in cost variable* (retired `CONCLUSION.md` §1;
  retired `INVESTOR_PROJECTION.md`, "Fleet
  costs") — the case closes only if the ground segment is "built lean and
  amortized across enough nodes." The Engineer's "diversity, not aperture"
  principle is exactly right and is itself the economizing move: modest-aperture
  (0.6–1.0 m) multi-terminal hubs, not monster telescopes
  ([optical_ground_stations.md](../laser_comms/optical_ground_stations.md)).
  Start with the ≥4-hub ~99% configuration; add hubs toward carrier-grade 99.9%
  *only as customer SLAs require and fund them*. Do not build the 10–12-hub
  network ahead of demand.
- **The relay layer — defer, as above.** Zero V1 spend.
- **The bus — lean-leverage Flatellite, do not clean-sheet.** The Engineer's
  choice of a Flatellite derivative is the economizing choice: it reuses
  Rocket Lab's mass-manufacturable platform and in-house subsystems
  ([space_hardware_capabilities.md §4](../rocket_lab/space_hardware_capabilities.md)).
  The one real spend inside the bus is the data-center-scale PMAD/PCDU
  capability gap — fund that as a focused development, not a whole-bus redesign.
- **R&D discipline overall.** R&D is ~$485M cumulative and is the largest
  *discretionary, controllable* drag on the crossover
  (retired `INVESTOR_PROJECTION.md`, "Why you
  would want in" item 1). Buying the V1 radiator instead of developing it
  in-house is the single biggest R&D economy available. Every in-house
  development should clear the bar: *does this create the moat, or is it
  available off-the-shelf?*

**The capital-sequencing answer to the Engineer's handoff question.** The
Engineer asked how to sequence capital across Phase 0→3. The answer:
*front-load the cheap, decision-critical spend (thermal model, customer
discovery, radiator vendor quote) into Phase 0; gate Phase 1→2 on a signed
anchor customer; keep the ground segment and relay lean and demand-pulled; and
slow the steady-state cadence so the funding peak comes down from ~$1.15B.* The
radiator, N+1 cooling, burn-in and optical terminals stay un-cut, exactly as the
Engineer asked — what changes is *make-vs-buy on the radiator* and *the pace*,
not the bill of materials.

---

### Align with the investor reality — make the premium *earned by design*

The investor pro-forma is unambiguous about what makes this venture financeable
(retired `INVESTOR_PROJECTION.md`): it crosses
early **only at a ~+100% premium** (~year 11), the central +50% case crosses at
~year 19–20, and at +25% it never crosses. The premium is the whole business.
And the margin research is equally clear: a premium on *commodity FLOPs* is not
plausible — a premium on a *scarce attribute* is
([hyperscaler_margins.md §2–3](../economics/hyperscaler_margins.md);
neoclouds reselling raw GPU-hours run ~breakeven operating margin). So the
strategy must be re-scoped so the premium is **designed into the product**, not
hoped for:

1. **Sell the venture as patient strategic capital, not fast-payback.** A
   ~$1.15B, ~20-year-crossover venture with sound unit economics is a
   *strategic-position* play (retired `CONCLUSION.md` Revision 5). The
   strategy document should be explicit that the financing structure is patient
   capital — and the slowed, gated ramp above is what brings the peak down
   toward something a patient investor can underwrite.
2. **Make the product a dedicated/sovereign/isolated *service*, not a FLOPs
   rental.** The favorable verdict holds *only* under the inference-service
   (token-selling) model — at raw IaaS rates even V2 is marginal
   ([wave5_synthesis.md §4.2](../synthesis/wave5_synthesis.md);
   [revenue_per_watt.md §4](../economics/revenue_per_watt.md)). And the premium
   is paid for the *attribute wrapper* — isolation, sovereignty, schedule
   certainty — exactly the layers where margin survives
   ([hyperscaler_margins.md §2](../economics/hyperscaler_margins.md)). The
   strategy should name the target customer (sovereign/defense/frontier-lab,
   capacity-blocked on the ground) and design the node, the SLA, and the
   single-tenancy model *around that buyer* from V1.
3. **Anchor the +100% premium with a real customer before scaling.** The
   difference between a year-11 and a year-20 crossover is the premium landing at
   +100% vs +50% (retired `INVESTOR_PROJECTION.md`).
   A +100% premium is *larger* than the sovereign-cloud precedent (+10–30%) but
   *well inside* the +200–500% on-demand-vs-neocloud spread the market already
   pays for an attribute wrapper ([hyperscaler_margins.md §3](../economics/hyperscaler_margins.md))
   — so it is plausible but must be *proven by a signed contract*, which is why
   it is the Phase-1→2 gate.
4. **Protect the 5-year GPU life as a financeable design requirement.** The
   second variable that decides whether the venture crosses at all is the
   service life (retired `INVESTOR_PROJECTION.md`,
   downside item 3). The Engineer's reliability architecture *is* the answer —
   keep it fully funded; it is the cheapest way to defend the larger of the two
   crossover-determining variables.

The re-scoped strategy is therefore the same architecture, financed honestly: a
gated, demand-pulled ramp with a lower funding peak; a bought-not-built V1
radiator; a lean, demand-pulled ground segment; a deferred relay layer; and a
product deliberately designed as a sovereign/dedicated *service* so the premium
that makes the J-curve turn is earned, not assumed.

---

### CFO's open questions back to the Engineer (Round 2)

1. **Can V2 close on a baseline-Neutron + hot-loop power-capped Rubin node
   (~190–250 kW), with the block-upgrade as pure margin upside?** If yes, the
   investor case no longer carries an uncommitted-rocket dependency. If V2
   genuinely *needs* the block-upgrade, say so plainly so the financing plan can
   price that risk.
2. **What is the engineering cost of a slower ramp?** Does a sub-7-node/yr
   steady-state cadence break the laser-mesh continuity or the burn-in-station
   economics, or is it cleanly throttleable? The burn-in-station sizing
   ([reliability_failure_handling.md open Q6](../node_design/reliability_failure_handling.md))
   may actually *favor* a slower ramp — confirm.
3. **What is the minimum viable Phase-1 fleet for a single anchor customer?**
   The pro-forma assumes ~4–8 nodes for "first useful service." If a sovereign
   anchor customer can be served by fewer, the Phase-1 capital at risk before the
   willingness-to-pay gate drops — quantify the smallest sellable configuration.
4. **Radiator: is there a credible external vendor for a ~300 m²/rack hot-loop
   deployable radiator at ~3–5 kg/m²?** The buy-vs-build re-scope depends on a
   vendor existing. If none does, the in-house program returns to the critical
   path and must be financed as such — and that materially raises the R&D line.

---

### Sources

Project documents:
- [strategy/README.md](README.md) — the rules of this Engineer↔CFO loop.
- Retired `CONCLUSION.md` — Revision 5: node cost ~$35–65M, per-node payback ~2.5–2.8 yr, venture crossover ~year 19–20, ~$1.15B peak funding; Profitability §1 (cost side), §2 (5-year life), §3 (premium tiers). This was a model-run summary artifact and is no longer part of the research folder.
- Retired `data_science/INVESTOR_PROJECTION.md` — central-case pro-forma, node-count ramp, deploy-ahead-of-earnings, the +25%/+50%/+100% premium and GPU-life sensitivities, fleet costs (ground segment, R&D ramp). Historical citation only; the file is no longer present in the current workspace.
- [economics/hyperscaler_margins.md](../economics/hyperscaler_margins.md) — §1.4 where margin pools; §2 who the premium is paid to; §3 the +10–30% sovereign precedent vs. the +200–500% on-demand spread; neocloud ~breakeven operating margin.
- [economics/revenue_per_watt.md](../economics/revenue_per_watt.md) — §4 IaaS vs. inference-service revenue models; ~$8M vs. ~$16M/rack-yr.
- [synthesis/wave5_synthesis.md](../synthesis/wave5_synthesis.md) — §2.4 flyability ceilings, §3 the crossover resolved at Vera Rubin, §4.1–4.2 V1/V2 cases, §5 strawman and ground segment, §6.2 premium tiers, §7 risks.
- [node_design/hot_chip_thermal_trajectory.md](../node_design/hot_chip_thermal_trajectory.md) — the hot-loop mass lever.
- [node_design/reliability_failure_handling.md](../node_design/reliability_failure_handling.md) — §4 coolant loop as leading kill mode, §6 redundancy, open Q6 burn-in stations.
- [rocket_lab/space_hardware_capabilities.md](../rocket_lab/space_hardware_capabilities.md) — §4 Flatellite bus, §6 the deployable-radiator capability gap.
- [rocket_lab/neutron/payload_and_block_upgrade.md](../rocket_lab/neutron/payload_and_block_upgrade.md) — §5 the block-upgrade is unannounced, years post-debut.
- [laser_comms/optical_ground_stations.md](../laser_comms/optical_ground_stations.md) — §3 ≥4 hubs for ~99%, diversity over aperture.
- [laser_comms/rf_limited_service.md](../laser_comms/rf_limited_service.md) — the RF backup sliver.
- [llm_compute/multi_rack_inference.md](../llm_compute/multi_rack_inference.md) — §5–6 near-linear replica scaling.
- [orbital/orbits_environment.md](../orbital/orbits_environment.md) — dawn-dusk SSO, benign radiation.
- [competitors/starcloud.md](../competitors/starcloud.md) — competitive timing window.

*End of Round 1 — CFO. The Engineer responds next.*

---

## Round 2 — Chief Engineer

*Round 2 — Chief Engineer — 2026-05-17. Appended, not a rewrite. The goal of
this round is to converge. The CFO's financial discipline is largely correct
and I adopt it; I push back in exactly one place, with a hybrid that costs
little and protects the moat; and I then state the converged strategy plainly.*

### Engineer's summary

The CFO did not cut the architecture — the spine is intact (one intact rack per
node, hot-loop radiator, N+1/N+2 cooling, partitioned graceful degradation,
build-to-learn → V2, the laser-meshed single-rack constellation). What the CFO
changed is *pace and make-vs-buy*, and on the economics the CFO is right: a
~$1.15B funding peak driven by a deploy-ahead-of-earnings ramp is the venture's
real fragility (retired `INVESTOR_PROJECTION.md`,
"Why the venture crossover is so much later"). **I accept the gated ramp, the
willingness-to-pay gate, the lean ground segment, the deferred relay layer, the
block-upgrade demoted to margin upside, and buy-for-V1 on the radiator.** None
of those harms the engineering.

**I push back in one place only:** "buy V1, internalize *only if* V2 math
demands it" treats the radiator purely as a cost line. It is also the one
subsystem that most differentiates a Rocket Lab orbital-compute prime
([space_hardware_capabilities.md §6](../rocket_lab/space_hardware_capabilities.md)),
and the ~2026–2030 competitive window
([starship_addendum.md](../competitors/starship_addendum.md) via
[LIBRARY.md](../LIBRARY.md)) does not leave room to *start* an in-house program
only after a Phase-3 decision. The fix is not to reject buy-for-V1 — it is a
**hybrid: buy the V1 radiator, and in parallel fund a deliberately small
in-house hot-loop radiator development so V2 can internalize on schedule if the
fleet math says so.** That parallel spend is ~$15–40M, not a flagship program —
small against the ~$485M R&D line and the ~$1.15B peak.

**Engineer's confidence after Round 2: high on the converged architecture and
the gated financing logic; medium on the V1 radiator-vendor availability at the
hot-loop operating point; medium on the schedule against the Starship window.**

---

### 1. What I accept from the CFO — adopted into the converged strategy

These are financially sound and do not harm the engineering. I adopt them
without reservation.

- **Gate Phase 1 → Phase 2 on a signed sovereign/defense/frontier-lab anchor
  customer at or above the ~+50% premium.** This is correct and it is also
  *good engineering discipline*: willingness-to-pay for orbital inference is
  entirely unobserved ([wave5_synthesis.md §6.2](../synthesis/wave5_synthesis.md)),
  and scaling a 12–24-node mesh before the premium is confirmed would commit
  the laser-mesh topology, the burn-in-station count and the ground-hub network
  to a fleet size that may never be justified. A financial gate between "first
  useful service" and "robust network" costs the engineering nothing — the
  Phase-1 fleet is already a complete, operable system
  ([wave5_synthesis.md §5](../synthesis/wave5_synthesis.md)). Adopted.

- **Cap steady-state cadence below ~7 nodes/yr and slow the ramp to lower the
  ~$1.15B peak.** A slower ramp does not break the architecture, and in one
  place it *helps* it: burn-in is a real throughput constraint — a 1–3-week
  per-rack burn-in + TVAC + post-vibration re-test campaign
  ([reliability_failure_handling.md §3, open Q6](../node_design/reliability_failure_handling.md))
  — and a sub-7-node/yr cadence is comfortably served by a small number of
  burn-in stations, avoiding a capital-heavy parallel test farm. A slower ramp
  also means more on-orbit learning per node deployed before the next batch is
  committed — the build-to-learn arc *wants* that feedback latency. Adopted; see
  §4 for the cadence answer the CFO asked for.

- **Hold the ground segment lean (~$150M); defer the relay layer.** The
  "diversity, not aperture" design ([optical_ground_stations.md §3](../laser_comms/optical_ground_stations.md))
  was already the economizing choice — modest 0.6–1.0 m multi-terminal hubs beat
  one monster telescope on physics, not just on cost. A ≥4-hub ~99% network for
  V1/Phase 1, with hubs added toward 99.9% only as a customer SLA funds them, is
  both the lean plan and the technically correct one. The relay ring stays a V2
  discretionary line, justified on a cost-per-availability-point basis against
  ground-diversity-only — the service is latency-tolerant batch/async inference
  ([wave5_synthesis.md §5](../synthesis/wave5_synthesis.md)), so it does not
  *need* the relay layer to function. Adopted.

- **Demote the block-upgrade from "critical path" to margin upside.** I wrote
  "on the critical path to V2 profitability" in Round 1; the CFO is right that
  no investor should fund a venture whose profitable product is gated on an
  unannounced rocket variant ([payload_and_block_upgrade.md §5](../rocket_lab/neutron/payload_and_block_upgrade.md)).
  I correct it: **V2 must close on a baseline-Neutron + hot-loop power-capped
  Rubin node**, and §3 below confirms it engineering-wise. The block-upgrade
  becomes pure margin upside. Adopted.

- **Buy the V1 radiator rather than build it in-house first.** The CFO is right
  that a first-of-kind in-house radiator program committed *before* the
  willingness-to-pay gate is fixed R&D spent ahead of demand. Fresh market
  research confirms credible deployable-radiator vendors exist —
  **ARQUIMEA** ships qualified deployable radiators with multi-loop heat pipes
  and embedded condenser lines up to ~6 m² per assembly *with* the deployment
  mechanism ([ARQUIMEA — Deployable radiators](https://www.arquimea.com/products/deployable-radiators-satellite-space/)),
  **Sierra Space** has TVAC-tested a deployable-radiator prototype at NASA
  Johnson ([Sierra Space](https://www.sierraspace.com/blog/sierra-space-advances-thermal-control-technology-with-successful-tvac-testing-of-deployable-radiator-prototype/)),
  and **ThermAvant** offers deployable oscillating-heat-pipe radiator panels
  ([ThermAvant — OHP Radiators](https://www.thermavant.com/thermavant-products/oscillating-heat-pipe-radiators)),
  with **Paragon** (xRAD extruded radiators — [Paragon](https://www.paragonsdc.com/what-we-do/thermal-control/))
  and **INVENT** (LiDeR passive deployable radiator — [satsearch](https://satsearch.co/products/invent-gmbh-deployable-radiator))
  as further candidates. A V1 node needs ~300 m²/rack
  ([node_mass_model.md §4](../node_design/node_mass_model.md)) — far above any
  single vendor assembly — so V1 buys *multiple* qualified radiator wings and
  integrates them. That converts the project's single weakest cost input into a
  set of fixed-price quotes. **Buy-for-V1 adopted** — but read §2: the buy
  decision and the moat decision are not the same decision.

---

### 2. Where I push back — the radiator is the moat, and a parallel in-house track costs little

This is the one place a clean financial cut risks the long-term engineering and
the competitive moat, so I make the case with sources rather than just adopting.

**2.1 The radiator is the differentiator, not a commodity line.** The CFO's own
margin logic says capital should concentrate on "what creates and defends the
moat" and that the moat is the *scarce attribute*, not FLOPs
([hyperscaler_margins.md §1.4](../economics/hyperscaler_margins.md), cited by
the CFO). For an orbital compute prime the scarce attribute is precisely the
ability to *reject data-center-class heat in vacuum at low mass* — that is the
gating problem for the entire orbital-DC sector
([space_hardware_capabilities.md §6](../rocket_lab/space_hardware_capabilities.md)),
and independent reporting in early 2026 calls cooling "the biggest unsolved
challenge of orbital computing" and "a physics wall," with no vendor's product
yet scaling to multi-MW AI heat loads
([SatNews, Mar 2026](https://satnews.com/2026/03/17/the-physics-wall-orbiting-data-centers-face-a-massive-cooling-challenge/);
[Compute Forecast](https://www.computeforecast.com/blogs/space-data-center-cooling-crisis/)).
A company that *owns* the deployable hot-loop radiator owns the one subsystem
every orbital-compute competitor must also solve. Permanently outsourcing it
means Rocket Lab's orbital-DC prime position rests on a supplier it does not
control — the same strategic exposure the SADA bottleneck represented before
the Motiv acquisition closed it
([space_hardware_capabilities.md §3](../rocket_lab/space_hardware_capabilities.md)).

**2.2 The off-the-shelf vendors do not yet sell the part this node needs.** The
buy-for-V1 plan is sound for *V1* — but it is buying qualified radiators built
for conventional ~30–40 °C coolant loops and satellite-scale heat loads. The
decisive design move in this whole strategy is the **hot-loop ~70–80 °C
radiator surface** that banks the ~40–55% T⁴ mass cut
([hot_chip_thermal_trajectory.md headline table](../node_design/hot_chip_thermal_trajectory.md)).
No surveyed vendor advertises a product qualified at that operating point and
at the ~3–5 kg/m² areal density a Rubin-class V2 node needs — the public
state of the art is satellite-scale assemblies and incremental coating gains,
"not transformative leaps" ([Compute Forecast](https://www.computeforecast.com/blogs/space-data-center-cooling-crisis/)).
So the realistic situation is: **V1 can buy a good-enough radiator; V2's
moat-grade hot-loop radiator does not exist to buy yet and someone has to
develop it.** If Rocket Lab does not, it is either captive to whichever vendor
develops it first, or — worse — that vendor sells the same part to Starcloud.

**2.3 "Internalize only if V2 math demands it" starts the clock too late.** A
deployable-radiator development that is qualified, TVAC-tested and
flight-proven is a multi-year effort — Sierra Space's prototype is only now at
the TVAC-test stage ([Sierra Space](https://www.sierraspace.com/blog/sierra-space-advances-thermal-control-technology-with-successful-tvac-testing-of-deployable-radiator-prototype/)).
If the in-house decision waits for a Phase-3/V2 trigger *after* the
willingness-to-pay gate, the in-house radiator cannot be ready for the V2 nodes
it is meant to fly — V2 would slip, or fly bought radiators at worse mass and
margin. And the slower, gated ramp the CFO (correctly) imposes already pushes
V2 later; the ~2026–2030 window with no operational Starship-economics rival
([starship_addendum.md](../competitors/starship_addendum.md) via
[LIBRARY.md](../LIBRARY.md)) is the period in which being the radiator-owning
prime matters most. Starting the in-house clock only after a Phase-3 gate risks
arriving with the moat subsystem just as the window closes.

**2.4 The hybrid — buy V1, fund a small in-house track in parallel.** This
resolves the disagreement at low cost:

- **V1: buy.** Procure V1 radiators from ARQUIMEA / Sierra Space / ThermAvant /
  Paragon / INVENT against fixed-price contracts, as the CFO specifies.
  Adopted in full.
- **In parallel from Phase 0: fund a deliberately *small* in-house hot-loop
  deployable-radiator development** — not the Round-1 "flagship program," but a
  focused effort to (a) close the chip→coolant→panel thermal-resistance model
  (the Engineer's #1 action item, which has to be done in-house regardless
  because it sets the whole node thermal design — [§7 item 1](#7-engineers-priority-action-list-handing-the-baton-to-the-cfo)),
  and (b) carry one hot-loop radiator design to a TVAC-tested engineering unit.
  Order-of-magnitude ~$15–40M over Phase 0–1 — small against the ~$485M R&D
  line (retired `INVESTOR_PROJECTION.md`, "Fleet
  costs")) and a rounding error against the ~$1.15B peak.
- **Phase-3 decision becomes a real make-vs-buy, not a make-from-scratch.** If
  the V2 fleet math favours in-housing, the in-house design is already at
  engineering-unit maturity and can be productionized on schedule. If a vendor
  has meanwhile productized a hot-loop radiator at the right operating point,
  the in-house unit is the benchmark that disciplines the vendor's price and a
  proven fallback. Either way the moat is protected and V2 is not gated on a
  bet placed too late.

This is a genuine concession to the CFO — Round 1 wanted the flagship in-house
program *now*; Round 2 buys V1 and funds only a small parallel track. It is
also a genuine, sourced push-back: a clean "buy, decide later" defers the one
development whose lead time the schedule cannot absorb.

---

### 3. Closing the CFO's Round-2 questions

**Q1 — Can V2 close on a baseline-Neutron + hot-loop power-capped Rubin node
(~190–250 kW), block-upgrade as upside?** **Yes.** The reconciled ceilings table
([§2.1](#21-baseline-reusable-neutron-for-v1-the-block-upgrade-is-the-v2-critical-path);
[wave5_synthesis.md §2.4](../synthesis/wave5_synthesis.md)) shows baseline
reusable Neutron + hot-loop reaches ~270–320 kW (working ~300 kW), which flies a
power-capped Rubin node (~190–250 kW) with margin. A power-capped Rubin node
still clears the ~2-yr inference-service payback inside the obsolescence window
([wave5_synthesis.md §3, §4.2](../synthesis/wave5_synthesis.md)). So V2's
business case stands on baseline Neutron; the block-upgrade only adds power
headroom (full uncapped ~300 kW Rubin, then ~430–470 kW design space) and thus
margin per node. **V2 does not need the block-upgrade — confirmed.** The
financing plan should carry it as upside only.

**Q2 — Engineering cost of a slower ramp?** Essentially none, and partly a
benefit. Laser-mesh continuity is set by *node count and spacing within an
operating cluster*, not by deployment *rate* ([constellation_mesh.md §5–6](../laser_comms/constellation_mesh.md))
— a cluster is launched and commissioned, then runs; a slower cadence between
clusters does not break a commissioned mesh. Burn-in economics *favour* a slower
ramp: a sub-7-node/yr cadence is served by a small burn-in/TVAC facility rather
than a capital-heavy parallel test farm ([reliability_failure_handling.md open Q6](../node_design/reliability_failure_handling.md)).
The one real constraint is replacement: at ~7–9% GPU AFR and a ~3-yr payload
life, a steady-state fleet needs a replacement cadence roughly equal to
fleet-size ÷ 3 just to hold capacity ([reliability_failure_handling.md Summary](../node_design/reliability_failure_handling.md))
— so the <7-node/yr cap implies a steady-state fleet on the order of ~15–20
nodes before growth competes with replacement. That is consistent with the
Phase-2 "~12–24 nodes" band and is a clean design point, not a conflict.

**Q3 — Minimum viable Phase-1 fleet for a single anchor customer?** Smaller than
the ~4–8-node "first useful service" band. One anchor customer buying dedicated
single-tenant capacity for one or a few frontier models needs: enough nodes to
host the model(s) with replica redundancy against a coolant-loop node loss, plus
mesh closure. That is realistically **~3–4 nodes** — one or two replicas of the
served model plus one spare for graceful-degradation cover
([reliability_failure_handling.md §5](../node_design/reliability_failure_handling.md);
[multi_rack_inference.md §5–6](../llm_compute/multi_rack_inference.md)). A
3-node string still closes a laser ring and still gives multi-pass ground
contact across the ≥4 hubs. So the capital genuinely at risk *before* the
willingness-to-pay gate is the Phase-0 demonstrator (1 node) plus a ~3–4-node
Phase-1 anchor deployment — materially below a 12–24-node commitment, exactly as
the CFO wants. The smallest sellable configuration is ~3–4 nodes.

**Q4 — Is there a credible external vendor for a ~300 m²/rack hot-loop
deployable radiator at ~3–5 kg/m²?** Split answer, and it is the basis of §2's
hybrid. *For V1's operating point* (conventional ~30–40 °C loop, satellite-scale
assemblies integrated in multiples to ~300 m²): **yes** — ARQUIMEA, Sierra
Space, ThermAvant, Paragon and INVENT are credible
([ARQUIMEA](https://www.arquimea.com/products/deployable-radiators-satellite-space/);
[Sierra Space](https://www.sierraspace.com/blog/sierra-space-advances-thermal-control-technology-with-successful-tvac-testing-of-deployable-radiator-prototype/)).
*For the moat-grade V2 hot-loop radiator* (~70–80 °C surface at ~3–5 kg/m²):
**not demonstrably today** — no surveyed vendor advertises that operating point,
and the orbital-DC cooling problem is openly described as unsolved at
data-center scale ([SatNews](https://satnews.com/2026/03/17/the-physics-wall-orbiting-data-centers-face-a-massive-cooling-challenge/)).
That is exactly why the hybrid funds a small in-house track now: V1 buys,
V2's moat part has to be developed by someone, and the schedule cannot wait for
a Phase-3 trigger to start.

---

### 4. The converged strategy

This is the final, agreed build strategy — technically excellent and
financeable. It is the Round-1 architecture, with the CFO's financing
discipline adopted and one hybrid added.

**Architecture (unchanged, agreed by both rounds):** one intact NVL72-class rack
per node, one node per launch ([node_mass_model.md §6](../node_design/node_mass_model.md));
the hot-loop ~70–80 °C single-phase warm-water thermal architecture as the
decisive mass lever ([hot_chip_thermal_trajectory.md](../node_design/hot_chip_thermal_trajectory.md));
a partitioned rack with many small NVLink fault domains, N+1/N+2 cooling, and
graceful degradation to ~75–85% EOL capacity
([reliability_failure_handling.md §5–7](../node_design/reliability_failure_handling.md));
a Flatellite-derived high-power bus with a focused PMAD/PCDU development
([space_hardware_capabilities.md §4, §6](../rocket_lab/space_hardware_capabilities.md));
3–4 CONDOR-class optical terminals plus a modest RF sliver per node
([constellation_mesh.md §5–6](../laser_comms/constellation_mesh.md);
[rf_limited_service.md](../laser_comms/rf_limited_service.md)); a tight
along-track laser-meshed single-rack string in ~500–600 km dawn-dusk SSO; and
multi-rack models split across separate laser-linked single-rack satellites by
pipeline/replica parallelism ([multi_rack_inference.md §5–6](../llm_compute/multi_rack_inference.md)).

**Financing and pace (the CFO's Round-1, adopted):**

- **Phase 0 — 1-node demonstrator.** Engineering gate: radiator deployment,
  hot-loop thermal ops, partitioned graceful degradation, optical downlink.
- **Phase 1 — ~3–4-node anchor deployment** (down from "4–8"; §3 Q3): the
  smallest fleet that serves one sovereign/defense/frontier-lab anchor customer
  with replica redundancy.
- **Phase 1 → Phase 2 financial gate:** a *signed* anchor customer at or above
  the ~+50% premium. No 12–24-node scale-up before the premium is contracted.
- **Phase 2 — ~12–24-node network**, cadence capped below ~7 nodes/yr; this
  implies a steady-state fleet on the order of ~15–20 nodes before growth
  competes with replacement (§3 Q2). The slower ramp is what brings the funding
  peak down from ~$1.15B.
- **Phase 3 — V2:** full Vera Rubin nodes on **baseline Neutron + hot-loop**
  (§3 Q1); the block-upgraded Neutron is margin upside, engaged on the roadmap
  but never a gating dependency.
- **Ground segment lean (~$150M):** ≥4 diverse modest-aperture hubs for ~99%;
  add hubs toward 99.9% only as a customer SLA funds them.
- **Relay layer deferred** to a V2 cost-per-availability-point decision.
- **Capital concentrates on the moat:** the hot-loop thermal model, reliability/
  graceful degradation, customer willingness-to-pay discovery, and the
  sovereign/dedicated *service* wrapper — not commodity FLOPs.

**The radiator — the converged hybrid (the one item Round 2 changed):**

- **V1: buy.** Fixed-price deployable radiators from established vendors,
  integrated in multiples to the ~300 m²/rack requirement.
- **Phase 0 onward, in parallel: a small (~$15–40M) in-house hot-loop
  deployable-radiator development** — close the chip→coolant→panel thermal model
  (needed in-house regardless) and carry one hot-loop radiator design to a
  TVAC-tested engineering unit.
- **Phase 3: a real make-vs-buy** between a mature in-house design and whatever
  the vendor market has by then productized — moat protected, V2 not gated on a
  bet placed too late.

**Build-to-learn → V2 spine (agreed):** V1 is financed as a learning +
strategic-position asset, not a standalone profit centre
([wave5_synthesis.md §4.1](../synthesis/wave5_synthesis.md)); V2 is the
standalone-profitable product, conditional on the inference-service revenue
model and an earned ~+50–100% premium ([wave5_synthesis.md §4.2, §6](../synthesis/wave5_synthesis.md)).

---

### 5. The one open decision for the founder

The Engineer and CFO have converged on everything above. **One item is a
genuine judgment call and is handed explicitly to the founder:**

> **How much in-house radiator development to fund in parallel with the
> bought V1 radiator — and how early.** The CFO's pure position minimizes
> R&D burn and crossover risk: buy V1, and make the in-house decision only at
> Phase 3. The Engineer's position protects the moat and the schedule: fund a
> small (~$15–40M) in-house hot-loop radiator track from Phase 0 so V2 can
> internalize on time if the fleet math says so. Both agree V1 is bought and
> the radiator is *not* cut. The disagreement is narrow and quantified: it is a
> ~$15–40M Phase-0/1 spend, traded against the strategic risk of being captive
> on — or beaten to — the orbital-compute industry's single hardest subsystem
> during the ~2026–2030 competitive window
> ([starship_addendum.md](../competitors/starship_addendum.md);
> [SatNews](https://satnews.com/2026/03/17/the-physics-wall-orbiting-data-centers-face-a-massive-cooling-challenge/)).
> The founder should decide this as a strategic-moat-vs-capital-discipline
> call, informed by the Phase-0 radiator vendor quotes and the customer-
> discovery signal — both of which arrive before the money must be committed.

Everything else is converged.

---

### Sources

Project documents:
- [strategy/README.md](README.md) — the rules of this Engineer↔CFO loop.
- [synthesis/wave5_synthesis.md](../synthesis/wave5_synthesis.md) — §2.4 flyability ceilings, §3 crossover at Rubin, §4.1–4.2 V1/V2 cases, §5 strawman/ground segment, §6 premium tiers.
- [node_design/hot_chip_thermal_trajectory.md](../node_design/hot_chip_thermal_trajectory.md) — the hot-loop ~70–80 °C radiator mass lever; headline T⁴ table.
- [node_design/node_mass_model.md](../node_design/node_mass_model.md) — §4 radiator area (~300 m²/rack), §6 per-node mass.
- [node_design/reliability_failure_handling.md](../node_design/reliability_failure_handling.md) — §3 burn-in, §5 graceful degradation, §6 redundancy, open Q6 burn-in stations, Summary (~7–9% AFR).
- [rocket_lab/space_hardware_capabilities.md](../rocket_lab/space_hardware_capabilities.md) — §3 the SADA/Motiv precedent, §4 Flatellite, §6 the deployable-radiator capability gap.
- [rocket_lab/neutron/payload_and_block_upgrade.md](../rocket_lab/neutron/payload_and_block_upgrade.md) — §5 the block-upgrade is unannounced, years post-debut.
- [laser_comms/constellation_mesh.md](../laser_comms/constellation_mesh.md) — §5–6 mesh topology and node count.
- [laser_comms/optical_ground_stations.md](../laser_comms/optical_ground_stations.md) — §3 ≥4 hubs for ~99%, diversity over aperture.
- [llm_compute/multi_rack_inference.md](../llm_compute/multi_rack_inference.md) — §5–6 replica scaling and fleet sizing.
- [economics/hyperscaler_margins.md](../economics/hyperscaler_margins.md) — §1.4 where margin pools (the moat logic).
- Retired `data_science/INVESTOR_PROJECTION.md` — ~$1.15B peak, ~$485M R&D burn, premium/GPU-life sensitivities. Historical citation only; the file is no longer present in the current workspace.
- [competitors/starship_addendum.md](../competitors/starship_addendum.md) — the ~2026–2030 competitive window.
- [LIBRARY.md](../LIBRARY.md) — document catalog and cross-references.

Independent research (Round 2):
- [ARQUIMEA — Deployable radiators for satellites](https://www.arquimea.com/products/deployable-radiators-satellite-space/) — qualified deployable radiators, multi-loop heat pipes, up to ~6 m²/assembly with deployment mechanism.
- [Sierra Space — TVAC testing of deployable radiator prototype](https://www.sierraspace.com/blog/sierra-space-advances-thermal-control-technology-with-successful-tvac-testing-of-deployable-radiator-prototype/) — deployable-radiator prototype TVAC-tested at NASA Johnson.
- [ThermAvant — Oscillating Heat Pipe Radiators](https://www.thermavant.com/thermavant-products/oscillating-heat-pipe-radiators) — deployable OHP radiator panels, >1 kW rejection.
- [Paragon Space Development — Thermal Control / xRAD](https://www.paragonsdc.com/what-we-do/thermal-control/) — extruded radiator technology.
- [satsearch — INVENT GmbH LiDeR deployable radiator](https://satsearch.co/products/invent-gmbh-deployable-radiator) — passive deployable radiator product.
- [SatNews — "The Physics Wall": orbiting data centers face a massive cooling challenge (Mar 2026)](https://satnews.com/2026/03/17/the-physics-wall-orbiting-data-centers-face-a-massive-cooling-challenge/) — cooling is the gating problem; no product yet scales to multi-MW AI heat.
- [Compute Forecast — The Cooling Crisis Facing Space Data Centers](https://www.computeforecast.com/blogs/space-data-center-cooling-crisis/) — current radiator tech does not scale cleanly to AI data-center heat loads.

*End of Round 2 — Chief Engineer. The strategy is essentially converged; one
open decision is handed to the founder (§5).*
