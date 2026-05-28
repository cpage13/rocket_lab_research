# Preliminary Findings — Orbital AI-Inference Data Center on Neutron

*Synthesis of research wave 1. Date: 2026-05-17. Status: draft for review.*
*Sources: the 9 foundational research docs + competitor analysis. Every claim
below is tagged with the doc it comes from.*

> **Superseded numbers (wave-5, 2026-05-17):** this wave-1 synthesis quotes a
> "~8.5–9 t reusable Neutron SSO budget" throughout. That figure has been
> re-baselined to a working **~9.5 t (range 8.5–10.5 t)** — see
> `rocket_lab/neutron/payload_and_block_upgrade.md` and `synthesis/wave5_synthesis.md`.
> The wave-1 verdict (no physics wall; 1 rack/node, 1 node/launch) still
> stands; only the SSO figure is stale.

---

## 1. Bottom line

**No physics wall has been found.** Every candidate hard barrier examined in
wave 1 — heat rejection, power, radiation, comms bandwidth, inference
communication topology — resolves to an *engineering and economics* problem, not
a law-of-physics "no." The binding constraint is **launch mass to
sun-synchronous orbit per Neutron flight**, which is a budget, not a wall
(`neutron_specs.md`, `thermal_analysis.md`, `orbits_environment.md`).

The most credible concrete architecture given wave-1 numbers: a constellation of
**self-contained, single-node satellites flown to a ~500–600 km dawn-dusk
sun-synchronous orbit**, each node carrying **one intact NVL72-class server rack
(~130–155 kW)**, hot-loop liquid cooling to **edge-on deployable radiators
(~200–430 m²/rack, working ~300 m²/rack)**, a **~150–185 kW/rack roll-out solar
array**, and **3–4 Mynaric-class optical terminals** meshing the nodes. A 1-rack
node masses **~5.4–8.6 t** (design to ~7–9 t) against an estimated **~8.5–9 t
reusable Neutron SSO budget** — so one Neutron flight delivers one complete,
independently useful inference node (`node_mass_model.md`, `thermal_analysis.md`,
`inference_scaling.md`, `optical_comms.md`). A 2-rack node (~9.6–16.6 t) exceeds
the reusable budget and is not a baseline. A single NVL72 rack already holds and
serves a whole 1–2T frontier model, so even the minimum node is a real product
(`inference_scaling.md`).

> **Note (lint correction, 2026-05-17):** This wave-1 synthesis has been
> numerically reconciled with the wave-3 node mass model per
> [lint_report.md](./lint_report.md). Radiator area, node mass,
> racks-per-launch and the Neutron SSO figure below reflect the corrected
> project position; the radiator-area range remains open pending a
> chip→coolant→panel thermal model.

The honest framing: this is **practical-in-the-future, gated on economics and
on a handful of unconfirmed numbers** — not blocked by physics.

---

## 2. Confirmed enablers

Things wave-1 research validated as workable:

- **One rack = one frontier model.** An NVL72-class rack carries 13.5–20 TB HBM;
  a 1–2T-parameter model in FP8 is only 1–2 TB of weights plus KV cache, fitting
  comfortably in a single rack. The minimum viable orbital node is therefore one
  self-contained rack — you scale by adding independent rack-replica satellites,
  not by splitting a model across satellites (`inference_scaling.md`,
  `ai_hardware.md`).
- **Inference fits orbit; training does not.** Inference's heavy traffic
  (tensor-parallel reductions, MoE all-to-all) stays *inside* the rack's
  ~130 TB/s NVLink fabric. Cross-rack traffic is light (~400 Gbps-class) and
  tolerates tens of ms of latency. Training's continuous cluster-wide gradient
  all-reduce does not — confirming the inference-only thesis (`inference_scaling.md`,
  `ai_hardware.md`).
- **Thermal is a sizing problem, not a wall.** Running the coolant loop hot
  (~60–90 °C, which AI silicon tolerates) exploits the Stefan-Boltzmann T⁴ term
  and shrinks radiator area well below the 370–540 m² first crude estimate.
  Heat rejection scales linearly with area; no physical effect forbids it.
  *(Lint correction: the radiator area for a 130–155 kW rack is a **~200–430 m²**
  range, working ~300 m²/rack — the wave-1 "~120–210 m²" figure is a superseded
  optimistic bound; see `node_mass_model.md` and `lint_report.md` §1.1.)*
- **Dawn-dusk SSO is the enabling orbit.** It cuts year-averaged eclipse from
  ~35–38% to ~3–6%, roughly halving the solar array and collapsing battery mass,
  and gives a steady thermal state with radiators held permanently edge-on to a
  near-fixed Sun (`orbits_environment.md`, `thermal_analysis.md`).
- **Radiation is benign at 500–600 km SSO.** ~1–3 krad(Si)/yr behind a few mm of
  aluminium — a reliability-engineering item (ECC, scrubbing, redundancy, spot
  shielding), not a feasibility blocker. Inference is relatively SEU-tolerant; a
  flipped weight bit is usually a small numeric error. Google's Project
  Suncatcher proton-tested TPUs found them "surprisingly radiation-hard" to
  ~15 krad (`orbits_environment.md`, `starcloud.md`).
- **Optical comms works at scale and needs no spectrum license.** Starlink runs
  9,000+ laser terminals at up to ~200 Gbps each; NASA TBIRD hit 200 Gbps
  space-to-ground. Inter-satellite laser is the proven backbone; RF spectrum is
  effectively closed to a new entrant via ITU coordination, so sidestepping it
  with optical is a genuine advantage (`optical_comms.md`, `rf_satcom.md`).
- **A real commercial node fits on Neutron today.** Starcloud's commercial
  product (Starcloud-3) is ~3 t / 200 kW — well inside Neutron's ~8–13 t class.
  Raw lift is not the wall for a single node (`starcloud.md`, `neutron_specs.md`).
- **Rocket Lab is vertically integrated for exactly this.** Launch (Neutron) +
  bus (Flatellite/Photon) + power (Feb-2026 silicon solar arrays announced
  explicitly for space data centers) + laser comms (Mynaric) + robotics (Motiv).
  It can plausibly be the end-to-end prime, not just a launch vendor
  (`overview.md`).

---

## 3. Candidate physics walls + status

| Candidate barrier | Status | Evidence |
|---|---|---|
| **Heat rejection in vacuum** (no convection) | **NOT A WALL** | Radiation scales linearly with area; hot-loop operation (~60–90 °C) shrinks required area to **~200–430 m²/rack (working ~300 m²)** — *corrected; "~120–210 m²" was a superseded optimistic bound, see `lint_report.md` §1.1*. Beats ISS per-m² rejection. A sizing/mass problem. (`node_mass_model.md`, `thermal_analysis.md`) |
| **Power generation** | **NOT A WALL** | Dawn-dusk SSO gives ~95–100% sunlit duty; ~150–185 kW/rack needs ~375–460 m² of array (~1.0–1.2 t at ROSA-class density). Scales linearly. (`thermal_analysis.md`, `orbits_environment.md`) |
| **Radiation / single-event effects** | **NOT A WALL** | ~1–3 krad/yr at 500–600 km behind a few mm Al; SEU handled architecturally (ECC, scrubbing). Inference is SEU-tolerant. (`orbits_environment.md`) |
| **Comms bandwidth (inter-satellite)** | **NOT A WALL** | Inference cross-rack traffic is light (~400 Gbps-class, latency-tolerant); optical ISLs already deliver 100–200 Gbps/terminal at Starlink scale. (`inference_scaling.md`, `optical_comms.md`) |
| **"Many satellites must talk to serve one model"** | **NOT A WALL** (dissolved) | One rack serves a whole frontier model; heavy traffic stays on internal NVLink. Scale by independent replicas. (`inference_scaling.md`) |
| **RF spectrum access** | **NOT A WALL for this design** (it is a wall for an *RF-primary* design) | ITU first-come-first-served effectively closes useful spectrum to a 2026 entrant — but optical needs no license, so the architecture routes around it. (`rf_satcom.md`) |
| **Weather-limited optical ground link** | **NOT A WALL, but the leading open RISK** | A single optical ground station gets only ~50–70% availability; lasers do not penetrate cloud. Mitigated — not eliminated — by 4+ diverse stations >1,000 km apart for ~99.9%. Real cost/latency/ops complexity. (`optical_comms.md`) |
| **Thermal at GW scale** | **WALL — but out of this project's scope** | At multi-MW/GW, radiator area becomes enormous (~800,000+ m² for 600 MW waste heat). This is why the thesis targets the 100 kW–~1 MW node class, where cooling is tractable. (`thermal_analysis.md`, `starcloud.md`) |
| **Neutron SSO payload mass** | **UNRESOLVED** | No official RL figure; the working figure is **~8.5–9 t reusable** (downrange recovery, 25–30% LEO→SSO penalty) — *corrected from the earlier ~10 t; see `lint_report.md` §1.2*. Could be off ±2 t. Not a *physics* wall, but it sets racks-per-launch and the entire economic envelope. (`neutron_specs.md`, `orbits_environment.md`, `node_mass_model.md`) |
| **Deployment mechanics** (unfolding 150–300 m² radiator + 400–900 m² array per node from one fairing) | **UNRESOLVED** | A serious mechanical and fairing-volume packaging challenge, unmodeled in wave 1. Likely an engineering problem, not physics — but unproven. (`thermal_analysis.md`) |
| **GPU lifetime / hot-loop vs. silicon longevity** | **UNRESOLVED** | Running silicon hot to shrink radiators trades against device life; replacement/servicing cadence in orbit is unmodeled. (`thermal_analysis.md`, `starcloud.md`) |

**Net:** every barrier that is genuinely about physics resolves to NOT-A-WALL at
the targeted node scale. The remaining items are UNRESOLVED *numbers and
engineering*, plus one GW-scale wall the project deliberately stays below.

---

## 4. The biggest unresolved numbers

The figures that are most load-bearing and least certain:

1. **Neutron SSO payload mass.** *Why it matters:* it sets racks-per-launch,
   node design, constellation launch count, and therefore the whole cost model.
   Currently a ~10 t reusable estimate inferred from a generic 25–30% LEO→SSO
   penalty (`neutron_specs.md`, `orbits_environment.md`). *What resolves it:* the
   Neutron SSO performance curve direct from Rocket Lab (launch@rocketlabusa.com)
   or the full Payload User's Guide.

2. **Usable fairing volume (and usable payload length).** *Why it matters:* a
   node carries large deployable radiators and arrays in stowed form; if the
   design is volume-bound rather than mass-bound, packaging — not kg — becomes
   the constraint. Estimate is a crude ~150–230 m³ with an uncertain
   usable-length input (the "16.5 m" snippet is judged unreliable)
   (`neutron_specs.md`). *What resolves it:* RL fairing internal envelope
   drawings / PUG.

3. **Radiator area and areal mass density.** *Why it matters:* the radiator
   area itself is unsettled — the thermal doc and node mass model bracket
   **~200–430 m²/rack** (working ~300 m²) depending on the assumed radiator
   surface temperature and second-face credit; at 3–8 kg/m² that is ~1–4 t,
   directly costing racks per launch. *What resolves it:* a real
   chip→coolant→panel thermal-resistance model to fix the radiator operating
   temperature (the **P1 open research item**), plus a vendor quote for a
   2026-era deployable composite/heat-pipe radiator at this scale
   (`thermal_analysis.md`, `node_mass_model.md`, `lint_report.md` §1.1).

4. **Mynaric CONDOR Mk3.1 timeline and the 100 Gbps capability.** *Why it
   matters:* shipping Mynaric hardware runs at ~2.5 Gbps; the mesh wants
   ~100 Gbps-class links. *What resolves it:* Mk3.1 delivery schedule and a
   confirmed data rate, mass, and power figure from the (now in-house) Mynaric
   datasheet (`optical_comms.md`).

5. **Rocket Lab silicon solar array specifics (W/kg, W/m², $/W, degradation).**
   *Why it matters:* silicon is lower efficiency than GaAs, so array area/mass
   could be 25–40% worse than the ROSA-class numbers used. *What resolves it:* an
   RL array datasheet; the Feb-2026 announcement was positioning, not specs
   (`thermal_analysis.md`, `overview.md`).

6. **Per-node mass budget validation.** *Now largely answered* by the wave-3
   `node_mass_model.md`: a 1-rack node is **~5.4–8.6 t** (design to ~7–9 t); a
   2-rack node is ~9.6–16.6 t and is dropped as a baseline. Residual
   uncertainty is concentrated in the pumped-loop/heat-pipe mass and the
   radiator areal mass (item 3 above) (`node_mass_model.md`).

---

## 5. A concrete strawman architecture

*Baseline for discussion. Ranges given; assumptions labelled.*

- **Orbit:** ~500–600 km **dawn-dusk sun-synchronous** (~97.5–97.8° inclination).
  Chosen for ~95–100% sunlit duty, steady thermal state, benign radiation, and
  largely natural deorbit compliance with the FCC 5-year rule
  (`orbits_environment.md`). *Assumption: lower band over 800 km, accepting a
  short eclipse season for less debris and easier disposal.*

- **The node = a self-contained satellite, one per Neutron launch.**
  - **Compute:** **one intact NVL72-class rack** (GB300-class, ~135–155 kW,
    ~1.36–1.4 t). *Corrected (lint):* the wave-3 node mass model rejects a
    2-rack node as a baseline — see the mass budget below. *Differentiator vs.
    Starcloud:* Neutron's large fairing (up to 5 m payload diameter standard,
    5.5 m for non-standard payloads, ~14 m fairing) can take **standard,
    intact server racks**, meshed by laser — it does **not** force Starcloud's
    Starship "PEZ dispenser" form factor. Hardware can be near-COTS rack
    geometry, modified for space rather than redesigned for a dispenser
    (`neutron_specs.md`, `node_mass_model.md`, `ai_hardware.md`; founder input).
  - **Two rack roles.** A deployed node likely carries both **compute**
    (the GPUs/HBM serving the model) and **networking/routing/packet-handling**
    functions (managing the optical mesh, request routing, KV-cache hand-offs,
    ground-link aggregation). *Corrected (lint):* since the node mass model
    rules out a 2-rack node, the networking function must fold into the single
    rack rather than occupy a second rack — sizing this remains a research item
    (founder input; `inference_scaling.md`, `node_mass_model.md`).
  - **Power:** ~150–185 kW continuous per compute rack (IT load + ~15–20%
    housekeeping/thermal/comms overhead) → **~375–460 m²** roll-out solar array
    per rack, ~1.0–1.2 t. Minimal batteries — eclipse-season ride-through only,
    or accept graceful compute throttling (`thermal_analysis.md`).
  - **Thermal:** hot-loop direct liquid cooling (~60–90 °C) to **deployable
    radiator wings held edge-on to the Sun**, **~200–430 m² per rack (working
    ~300 m²)**, ~1–4 t — *corrected (lint): "~120–210 m²" was a superseded
    optimistic bound; the area is unsettled pending a chip→coolant→panel
    thermal model, see `lint_report.md` §1.1*. The ~10–15% air-cooled fraction
    of a terrestrial rack must be re-engineered to all-liquid for vacuum
    (`ai_hardware.md`, `thermal_analysis.md`, `node_mass_model.md`).
  - **Comms:** **3–4 optical terminals** (Mynaric CONDOR Mk3.1-class, target
    ~100 Gbps) for the inter-satellite mesh and space-to-ground, carrying
    ~0.3–0.8 Tbps of inter-node traffic. **RF reserved for TT&C and a low-rate
    weather-backup downlink** only (`optical_comms.md`, `rf_satcom.md`).
  - **Mass budget:** a **1-rack node is ~5.4–8.6 t** (design target ~7–9 t;
    sub-6 t is a stretch goal), against an estimated **~8.5–9 t reusable
    Neutron SSO budget**. A 1-rack node flies reusable if it lands near the
    mass-optimized end. *Corrected (lint):* a 2-rack node (~9.6–16.6 t) blows
    the reusable budget and is **dropped as a baseline** — the architecture is
    **one rack per node, one node per launch** (`node_mass_model.md`).

- **Ground segment — hubs, not homes.** A small number of large, high-power,
  large-aperture **"monster" optical ground stations** at dedicated/corporate
  sites; **customers wire into those hubs**, they do not each operate a laser
  terminal. For ~99.9% availability the network needs **4+ geographically
  diverse stations >1,000 km apart** (uncorrelated cloud cover), with predictive
  weather scheduling and an RF backup path (`optical_comms.md`; founder input).

- **Constellation for a first useful service:** start with a **single 1-rack
  node** as the minimum viable product (it independently serves a frontier
  model). A first commercial service is plausibly **~4–8 nodes** — enough for
  throughput, redundancy, replica load-balancing, and overlapping ground-station
  passes — grown by adding independent rack-replica satellites near-linearly
  (`inference_scaling.md`). *Assumption: B2B / government / sovereign-compute
  customers, premium pricing, not consumer-facing.*

- **"Build to learn" as product.** Early small-scale deployment is itself
  saleable: it lets Rocket Lab and customers learn radiation-hardening, silicon
  modifications, hot-loop thermal ops, and on-orbit operations — knowledge that
  compounds toward larger-scale buildout and that frontier-lab / government
  customers will pay for as much as for the compute itself (founder input).

---

## 6. Recommended next research wave

Prioritized, each as a crisp question:

1. **What is Neutron's true SSO payload mass and usable fairing volume?**
   (Highest priority — the whole envelope hinges on it. Pursue RL directly.)
2. **Is the node mass- or volume-bound?** Model stowed packaging of 150–300 m²
   of radiator + 400–900 m² of array into the actual fairing envelope.
3. **What does a real per-node mass model say?** *Answered* by wave-3
   `node_mass_model.md`: a 1-rack node is ~5.4–8.6 t (design to ~7–9 t), a
   2-rack node ~9.6–16.6 t is dropped as a baseline. Residual work: the
   pumped-loop/heat-pipe mass line still needs a dedicated estimate.
4. **Compute rack vs. networking rack — what is the split?** Size the
   routing/packet-handling/ground-aggregation function and confirm whether a
   node needs a dedicated network rack or can fold that into compute.
5. **What deployable-radiator areal mass and operating temperature are
   achievable in 2026–2028?** Resolve the 3–5 vs. 8 kg/m² spread and build the
   chip→coolant→panel thermal-resistance model.
6. **When does Mynaric Mk3.1 (~100 Gbps) ship, at what mass/power?** Confirm the
   mesh-bandwidth assumption against in-house Mynaric data.
7. **What does a "monster" optical ground station cost and achieve?** Aperture,
   power, per-site throughput, capex/opex, and the 4+-site network sizing for
   target availability.
8. **What is GPU/HBM lifetime under a hot loop in this orbit?** Quantify the
   hot-radiator-vs-silicon-longevity trade and the resulting replacement cadence.
9. **What are Rocket Lab silicon solar array specs?** W/kg, W/m², $/W,
   degradation — to firm the array mass/area line.
10. **Economics first pass.** Revenue per rack, $/launch, payback, and what a
    B2B / frontier-lab / sovereign-compute customer would actually pay a premium
    for. (Deferred until items 1–3 land.)

---

## 7. Proposed thesis revision (Rev 2)

*Proposed only — the thesis file is not edited here.*

- **Reframe the headline finding.** State plainly: *wave-1 research found no
  physics wall.* Every hard barrier checked is engineering/economics. The thesis
  should lead with this and stop hedging on whether thermal is a "wall" — it is
  not, at the targeted scale.
- **Lock the differentiator: whole racks.** Make "we launch standard intact
  server racks in Neutron's large fairing, meshed by laser" the core
  differentiation vs. Starcloud's Starship PEZ-dispenser form-factor constraint.
  This is an architectural identity, not a footnote.
- **Add "build to learn" as an explicit product line.** Early small-scale
  deployment sells learning — radiation-hardening, silicon mods, hot-loop ops —
  that compounds toward scale. Frame it as revenue, not just R&D.
- **Name the node precisely.** The minimum viable node is **one self-contained
  NVL72-class rack** that serves a whole frontier model; scale by independent
  rack-replica satellites. Kill any remaining "split a model across many
  satellites" language — wave 1 dissolved that worry.
- **Adopt two rack roles.** Compute racks vs. networking/routing racks; a
  deployed node likely needs both.
- **Sharpen the ground architecture.** Replace "some special hub location" with:
  a few large "monster" optical ground stations at dedicated/corporate sites;
  **customers wire into hubs, they do not run their own laser terminals**; 4+
  diverse stations for availability.
- **Pick the scale deliberately.** Target the **100 kW–~1 MW node class** (1–2
  racks/launch), explicitly *not* GW-scale hyperscale training — that is where
  the real thermal wall and Starship economics live. Compete on **cadence,
  time-to-orbit, and turnkey node-level service**, not $/kg.
- **State the binding constraint and the open risks honestly.** Binding
  constraint: kg-to-SSO per Neutron launch. Leading open risk: the
  weather-limited optical ground link. Largest unknown: the unpublished Neutron
  SSO payload number.
- **Keep the block-upgrade question deferred** until baseline Neutron SSO
  capacity is confirmed — unchanged from Rev 1, and now explicitly gated on
  research item 1.
