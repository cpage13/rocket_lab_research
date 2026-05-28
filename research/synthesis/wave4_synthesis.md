# Wave 4 Synthesis — Orbital AI-Inference Data Center on Neutron

*Synthesis of research waves 2–4. Date: 2026-05-17. Status: draft for review.*
*Builds on the wave-1 synthesis (`preliminary_findings.md`) and the numerical
reconciliations in `lint_report.md`. Folds in: orbit types primer, RF satcom +
limited-RF service, optical ground stations, node mass model, AI DC TAM,
revenue-per-watt, premium value case, and Rocket Lab space-hardware
capabilities. Every claim is tagged with its source doc. All corrected numbers
are from `lint_report.md`.*

> **Superseded numbers (wave-5, 2026-05-17):** this synthesis uses a "~8.5–9 t
> reusable Neutron SSO budget" — the conservative low end. Wave 5 re-baselined
> it to a working **~9.5 t (range 8.5–10.5 t)**, which lets a feasibility-mid
> node fly reusable *comfortably* rather than marginally. The wave-4 payback
> *ratios* are SSO-independent and still hold; the *flyability/margin* framing
> ("node sits near the budget") is superseded — draw payback tables from here
> but flyability framing from `synthesis/wave5_synthesis.md`.
>
> **Superseded launch-cost / node-cost basis (wave-9, 2026-05-17):** this
> synthesis costs the launch at the **~$50–55M external customer price**
> ($52M/$63M/$80M reusable/expendable scenarios) and the node at **~$63–120M
> (~$85M mid)**. Wave 9 re-based the launch to Rocket Lab's **internal marginal
> cost of ~$10–20M**, dropping the V1 node to **~$35–65M (~$45M mid)** and
> launch's share of node cost from ~85% to ~45% — see `CONCLUSION.md` Rev 4 and
> `RESEARCH_TRACKER.md` wave-9. This synthesis also runs the **"~2–3-year GPU
> obsolescence window"** as the live payback test; the project later
> (`CONCLUSION.md` Rev 3 / founder wave 8) made a **5-year service life the base
> case** and demoted 2–3 years to a downside addendum. The wave-4 *direction*
> (payback is the crux; a baseline-Neutron node is build-to-learn) stands; the
> launch/node-cost figures and the 2–3-yr window framing are superseded.

---

## 1. Bottom line

**The wave-1 verdict still stands: no physics wall has been found.** Nothing in
waves 2–4 overturns it. Orbit types, RF/optical comms, ground stations, the
per-node mass model, and Rocket Lab's hardware stack all resolve to engineering
and economics, not laws of physics (`orbit_types_primer.md`, `optical_comms.md`,
`rf_satcom.md`, `optical_ground_stations.md`, `node_mass_model.md`,
`space_hardware_capabilities.md`).

**But the centre of gravity of the project has now shifted from physics to
economics — and the economics are genuinely tight.** Waves 2–4 surfaced one
crux that the wave-1 synthesis deferred: a node cannot be upgraded in orbit,
GPUs have a ~2–3 year economic life, so **a node must earn back its entire cost
(hardware + launch) within ~2–3 years** (`premium_value_case.md` §8). Section 2
works that calculation explicitly. The honest current read:

> **Physically feasible; economically unproven and tight.** At raw-GPU-rental
> rates the node payback is marginal-to-failing in the obsolescence window for
> most cost cases. It only closes cleanly under the inference-service revenue
> model (selling tokens, not GPU-hours) *and/or* with launch and spacecraft
> costs at the low end of their ranges *and/or* with the premium the value case
> argues for. The project's verdict moves from "practical-in-the-future, gated
> on a few unconfirmed numbers" to **"practical-in-the-future only if the node
> pays back inside the GPU obsolescence window — and that is now the single
> make-or-break question."**

This is not a "no." It is a sharply narrowed "yes, if." The remainder of this
document shows the arithmetic and identifies exactly what has to be true.

---

## 2. The decisive economic test — node payback vs. GPU obsolescence

This is the most important section. The premium value case
(`premium_value_case.md` §8) identified the crux precisely: terrestrial
operators rack-and-replace GPUs every 2–3 years inside a long-lived shell, so
the building is amortised across many GPU generations. **An orbital node cannot
do this.** When the silicon is obsolete, the *entire node* — rack, bus, solar,
radiator, comms, and the launch cost — is stranded. Therefore the node must
**earn back its full launched cost, plus a return, within the GPU's ~2–3 year
competitive life** (`premium_value_case.md` §8; GPU economic life ~2–3 yr,
~18-month refresh cadence — same doc, cross-checked in `revenue_per_watt.md`
§5).

Architecture fixed by `node_mass_model.md`: **1 rack per node, 1 node per
Neutron launch.** So the unit of analysis is one NVL72-class rack in orbit.

### 2a. Node cost — build it up

| Cost line | Low | Mid | High | Source / assumption |
|---|---|---|---|---|
| Rack hardware (NVL72-class, space-modified) | $3.0M | $4.0M | $5.5M | NVL72 rack ~$3M to buy (`revenue_per_watt.md` §2). Space modification (cold plates, launch reinforcement, vacuum-rating, rad spot-shielding per `node_mass_model.md` §2) adds cost; estimate +0–80%. **Estimate.** |
| Spacecraft hardware (bus, solar array, deployable radiator, comms terminals, propulsion, deployment structures) | $8M | $18M | $35M | **No direct quote exists in any doc — this is the weakest cost input.** Built up from: a ~150–300 kW-class bus with large deployable arrays + a large bespoke deployable radiator (the capability Rocket Lab does *not* yet have — `space_hardware_capabilities.md` §6) + 3–4 Mynaric optical terminals. Anchored loosely to smallsat/ESPA-class bus costs scaled for a ~5–8 t spacecraft with a first-of-kind radiator. **Estimate — flagged P1.** |
| Neutron launch (1 node/launch) | $52M | $63M | $80M | Reusable target ~$50–55M; expendable ~$70–80M (`neutron_specs.md` §6, `orbits_environment.md` §3). A feasibility-mid 1-rack node (~7–9 t) sits near the reusable SSO budget (~8.5–9 t) — so reusable is the planning case but expendable is a real possibility if the node lands heavy. |
| **Total node cost** | **~$63M** | **~$85M** | **~$120M** | |

Take the planning band as **~$65–120M per node, ~$85M mid.** The launch is the
single largest line — ~60–75% of node cost — which is itself a key finding: the
economics are dominated by launch, not by the GPUs.

### 2b. Node revenue/year — one NVL72-class rack of inference capacity

From `revenue_per_watt.md`, for a GB200/GB300 NVL72-class rack:

**Raw-GPU-rental case (IaaS — sell GPU-hours):**
- §2: a GB200 NVL72 rack rents at ~$756–1,944/hr; at 85% utilisation that is
  **~$5.6M–14.5M per rack-year gross.**
- §3/§6: blended realised contract pricing pulls the central case to
  **~$6–10M/rack-year**; conservative ~$5–6M; aggressive (premium Blackwell,
  near-on-demand) toward the $14M end.
- **Use: low ~$5M, mid ~$8M, high ~$13M per rack-year (gross IaaS).**

**Inference-service case (sell tokens via an API):**
- §4/§6: serving competitive frontier-model tokens earns a **~1.5–2.5× markup**
  over the underlying GPU-rental cost (the model-value premium; OpenAI runs
  ~70% compute gross margin on inference).
- Applying that to the IaaS case: **~$9M low, ~$16M mid, ~$25M high per
  rack-year** — *conditional on owning a competitive model.*

Both figures are **gross top-line**, not profit. They exclude the node's own
operating cost (ground-station network, ops staff, station-keeping). For a
payback test against a sunk node cost this is the right number to use — but the
payback must be read as "gross revenue to recover capital," and a true business
case would haircut it for opex.

### 2c. The payback arithmetic — does it close inside ~2–3 years?

Payback period = node cost ÷ node revenue/year. The obsolescence window is
**~2–3 years** (`premium_value_case.md` §8). To clear it with *any* return, the
node should pay back in well under that — call **≤2 years** the target for a
viable business (the remaining ~0.5–1 yr of competitive life is the margin).

**Raw-GPU-rental case (gross IaaS revenue):**

| | Low cost $65M | Mid cost $85M | High cost $120M |
|---|---|---|---|
| Low rev $5M/yr | 13.0 yr | 17.0 yr | 24.0 yr |
| Mid rev $8M/yr | 8.1 yr | 10.6 yr | 15.0 yr |
| High rev $13M/yr | 5.0 yr | 6.5 yr | 9.2 yr |

**At raw-GPU-rental rates the node does NOT pay back inside the 2–3 year
obsolescence window in any case** — the best case (low cost, high revenue) is
~5 years, roughly 2× too slow; the central case is ~10 years. This is the
honest, uncomfortable headline. **Selling raw GPU-hours from a single
Neutron-launched node does not work** against a 2–3 year GPU life.

**Inference-service case (gross token revenue, 1.5–2.5× markup):**

| | Low cost $65M | Mid cost $85M | High cost $120M |
|---|---|---|---|
| Low rev $9M/yr | 7.2 yr | 9.4 yr | 13.3 yr |
| Mid rev $16M/yr | 4.1 yr | 5.3 yr | 7.5 yr |
| High rev $25M/yr | 2.6 yr | 3.4 yr | 4.8 yr |

**Even the inference-service model only reaches the obsolescence window in its
most optimistic corner** (low cost + high revenue ≈ 2.6 yr). The central
inference case is ~5 years — still ~2× too slow.

### 2d. What it would take to close the gap

The gap between the central case (~5–10 yr payback) and the target (~2 yr) is a
**factor of ~2.5–5×.** That gap must be closed by some combination of:

1. **Sell inference, not raw GPU capacity.** The single biggest lever already in
   the docs: ~1.5–2.5× revenue uplift (`revenue_per_watt.md` §4). This is
   necessary but not sufficient.
2. **Drive launch cost down.** Launch is ~60–75% of node cost. A reusable
   Neutron at the low end (~$50M) vs. expendable (~$80M) is already a ~25% node-
   cost swing. A *block-upgraded* Neutron carrying 2 racks per launch would
   roughly halve launch-$/rack — but `node_mass_model.md` rejects the 2-rack
   node on the *baseline* vehicle (~9.6–16.6 t vs. ~8.5–9 t budget), so this is
   explicitly a block-upgrade question, not a baseline one.
3. **Drive spacecraft hardware cost down.** Mass-manufacture (Rocket Lab's
   Flatellite philosophy — `space_hardware_capabilities.md` §4) and a
   productised radiator could pull the $8–35M spacecraft line toward its low
   end. The deployable radiator is both the cost risk and the capability gap.
4. **Charge the premium.** `premium_value_case.md` argues a sovereign / defense
   / frontier-lab / ESG-constrained buyer who is *capacity-blocked on the
   ground* will pay materially above terrestrial rates. If the premium is, say,
   ~2× terrestrial inference pricing, that stacks on top of lever 1. A ~2×
   premium on the inference-service mid case takes payback from ~5.3 yr to
   ~2.7 yr — into the window.
5. **Extend the revenue-generating life.** If a node can stay economically
   useful 3–4 years (trailing-generation inference still has value for
   latency-tolerant, lower-tier workloads), the bar drops. But
   `revenue_per_watt.md` §3 warns revenue-per-watt falls ~2–3× per GPU
   generation, so a trailing node earns much less — this lever is weak.

**Honest conclusion:** the economics close *only* with **inference-service
revenue AND a genuine premium AND low-end launch/hardware costs** acting
together. No single lever is enough. The "build to learn" framing
(`preliminary_findings.md`; founder input) is important here: early nodes will
*not* pay back as compute assets — their return is the learning and the
strategic position, and they should be financed and justified as such, not as
standalone profit centres. The standalone-profitable node is plausibly a
**block-upgraded-Neutron, multi-rack, mass-manufactured-node** proposition, not
a baseline-Neutron one. **This is the sharpest finding of wave 4 and the
biggest single change to the thesis.**

---

## 3. Reconcile the revenue conflict

`revenue_per_watt.md` and `ai_datacenter_tam.md` disagree by ~5–10× on revenue
per GW. The conflict is real and `revenue_per_watt.md` §6 explicitly flags it
for synthesis. Resolution:

**The two documents measure different things.**

- **`ai_datacenter_tam.md` ~$3.3B/GW-yr** is a *crude proxy*: it divides the
  forecast ~$250B 2030 AI-inference **services market** by ~90 GW of inference
  capacity (its assumption A3). Its own A3 caveat admits this "conflates a
  services revenue figure with a power capacity figure as a crude bridge…
  use for magnitude, not for a business case." It is not measuring what a
  capacity owner bills — it is a top-down market-sizing artefact.
- **`revenue_per_watt.md` ~$15–20B/GW-yr** is built **bottom-up** from real
  rack rental rates and real company disclosures (CoreWeave FY2025, GPU pricing,
  NVL72 rack economics). It measures the **gross compute/IaaS top-line a 1 GW
  capacity owner could bill.** Its ~$25–50B/GW-yr inference figure adds the
  model-value markup.

They are not both "revenue per GW" — one is *gross compute revenue billed by
the infrastructure owner*, the other is a *services-market ÷ capacity ratio*.
The ~$3.3B figure is also closer to (though not equal to) an **operating-profit
or thin-margin** read, while the ~$15–20B is **gross top-line**.

**The right figure to use.** For this project — which asks what a node *earns*
to test payback — the bottom-up `revenue_per_watt.md` figure is correct, because
it is grounded in observed rack rental economics, not a market-ratio proxy. The
`ai_datacenter_tam.md` $3.3B/GW should be **retired as a revenue figure** and
kept only for what it is good for: order-of-magnitude *market sizing* (the
0.1%/1%/10%-of-inference TAM framing).

**One defensible reconciled number:**

| Basis | Per GW-year | Per node (1 NVL72 rack ≈ 1/6,000 GW)\* |
|---|---|---|
| Gross IaaS (sell GPU-hours) | **~$15–20B central** (range ~$5–40B) | **~$5–8M central** (range ~$5–13M) |
| Gross inference-service (sell tokens) | **~$25–50B** (conditional on a competitive model) | **~$9–16M central** (range ~$9–25M) |
| Net operating profit (after depreciation, opex) | ~40–60% of gross is *durable economic value* (`revenue_per_watt.md` §5) | materially lower — node-by-node opex not yet modelled |

\* `revenue_per_watt.md` §6 establishes ~5,500–6,000 NVL72 racks per GW of
facility power. Per-node figures in §2 use ~$5–13M (IaaS) and ~$9–25M
(inference), consistent with this row.

**Project position going forward:** use **~$15–20B/GW-yr gross IaaS** (central)
and **~$25–50B/GW-yr gross inference-service** as the two headline revenue
figures, each with its assumption set attached; treat **~$8M/rack-yr (IaaS) and
~$16M/rack-yr (inference)** as the per-node planning numbers. Stop quoting
$3.3B/GW as a revenue figure.

---

## 4. Confirmed enablers (waves 2–4)

New validated positives since the wave-1 synthesis, each with source:

- **SSO is confirmed a LEO subtype, and Neutron is optimised for exactly this
  orbit.** The orbit choice and the launch-vehicle choice are mutually
  consistent; no MEO/GEO penalty applies to the compute nodes
  (`orbit_types_primer.md` §1a, §6).
- **A relay layer can fix the LEO contact-time weakness if needed.** GEO relays
  lift LEO contact from ~5–15% to ~85–100% (TDRS/EDRS heritage); a LEO mesh is
  the lower-latency alternative. This is a known, solved-in-principle
  architecture — it is a design fork, not a risk (`orbit_types_primer.md` §4).
- **A limited RF service is attainable and is a genuine product, not just a
  backup.** `rf_satcom.md` said RF spectrum is closed; `rf_limited_service.md`
  refines this: a *narrow sliver* (~100–250 MHz Ka) is realistically obtainable
  (proven precedent: Open Cosmos inheriting Liechtenstein filings, satellites
  launched by Rocket Lab itself). It supports ~0.2–3 Gbps for 1k–10k B2B users
  — a "limited Starlink for business" — and doubles as the all-weather backup
  for the optical ground link (`rf_limited_service.md` §2, §5, §6).
- **The optical ground problem is well-characterised and the architecture is
  settled.** Going *big* at one site does not help; *diversity* does. ≥4
  modest-aperture (0.5–1.0 m), multi-terminal hubs >1,000 km apart give ~99%;
  ~10–12 for 99.9%. Inference is bandwidth-light, so throughput is not the risk
  — availability is (`optical_ground_stations.md` §1–3, §5). Per-hub capex
  ~$20–60M; network ~$100–500M (flagged estimates, §6).
- **The per-node mass model is built and confirms 1 rack/node, 1 node/launch.**
  A 1-rack node is ~5.4–8.6 t (design to ~7–9 t); volume-comfortable inside
  Neutron's fairing, mass-tight against the ~8.5–9 t reusable SSO budget. A
  2-rack node (~9.6–16.6 t) is dropped as a baseline (`node_mass_model.md` §6,
  §7).
- **The radiator-on-array-backside idea is validated as geometrically
  feasible.** The founder's "+30%" rule was wrong; the correct relation is
  radiator area ≈ 0.5–0.9× solar area, so the array backside has enough room to
  host the radiator (`node_mass_model.md` §4).
- **The terrestrial "push" is real, quantified, and worsening — the strongest
  leg of the premium case.** ~2,300–2,600 GW interconnection backlog, ~5-yr
  median grid waits (up to ~12 yr for data centres), ~5-yr transformer lead
  times, moratorium bills in 11–12 states, water now the #2 siting constraint
  (`ai_datacenter_tam.md` §6, `premium_value_case.md` §1, §6).
- **Zero water is a clean, unqualified differentiator.** Radiative cooling uses
  no water; unlike the carbon claim there is no offsetting orbital cost
  (`premium_value_case.md` §3).
- **A documented, fast-growing premium-buyer market exists.** Sovereign-AI
  infrastructure ~$19B (2026) → ~$177B (2035), ~28% CAGR; government/defense is
  the largest segment; major clouds are racing to ship air-gapped single-tenant
  product (`premium_value_case.md` §4, §5).
- **Rocket Lab's in-house stack is strong and nearly complete for a compute
  node.** Owns or is closing on: launch (Neutron), bus (Flatellite/Photon),
  solar (SolAero — only fully vertically integrated supplier; silicon arrays
  announced explicitly for space data centers), mechanisms/SADAs/robotics
  (Motiv), reaction wheels/star trackers (Sinclair), separation systems, RF
  radios (Frontier), laser comms (Mynaric CONDOR), optical payloads (Geost)
  (`space_hardware_capabilities.md` §1–5).

---

## 5. Risks & open issues

Each marked **WALL** / **NOT A WALL** / **RISK** / **UNRESOLVED**.

- **GPU obsolescence vs. node payback — RISK (the dominant one).** Not a physics
  wall, but the make-or-break economic risk. A node must pay back inside a ~2–3
  yr GPU life; §2 shows it does not at raw-GPU rates and only marginally under
  the inference-service model with favourable costs. This is now *the* central
  open question (`premium_value_case.md` §8; §2 above).
- **Deployable-radiator capability gap — RISK (capability + cost + schedule).**
  Rocket Lab does **not** build large deployable radiators — the single clear
  gap in an otherwise complete in-house stack; composites + robotics are
  adjacent but not equivalent (`space_hardware_capabilities.md` §6). The
  radiator is also the largest single mass line and the biggest deployment risk
  (`node_mass_model.md` §7), and a major, un-quoted cost input (§2a). Must be
  developed in-house or bought.
- **Radiator area / mass — UNRESOLVED.** The thermal doc and node mass model
  bracket ~200–430 m²/rack (working ~300 m²); 3–8 kg/m²; node mass swings
  several tonnes on this line. Needs a chip→coolant→panel thermal-resistance
  model (the standing P1 research item) (`lint_report.md` §1.1,
  `thermal_analysis.md`, `node_mass_model.md`).
- **Weather-limited optical ground link — NOT A WALL, but a standing RISK.**
  Mitigated by ≥4 diverse hubs, not eliminated; introduces latency/handoff
  jitter and a real ground-segment capex line (`optical_comms.md`,
  `optical_ground_stations.md`).
- **Neutron SSO payload — UNRESOLVED (largest single unknown).** Rocket Lab
  publishes no SSO figure; project standardises on ~8.5–9 t reusable, could be
  ±2 t. Sets racks-per-launch, node design, and the whole launch-cost-per-rack
  term in §2 (`neutron_specs.md`, `node_mass_model.md` §5).
- **Deployment mechanics — UNRESOLVED.** Unfolding a ~300 m²-class radiator
  (larger than the ISS's main radiators) plus a ~500–900 m² array from one
  fairing is a serious, unmodelled mechanical-reliability challenge — likely
  engineering, not physics (`node_mass_model.md` §7, `thermal_analysis.md`).
- **Neutron schedule & maturity — RISK.** Not flown; first flight Q4 2026
  target, slipped repeatedly; Jan 2026 tank rupture. A thesis depending on
  Neutron should assume operational reusable flights NET 2027
  (`neutron_specs.md` §5, §8).
- **Mynaric 100 Gbps timeline — RISK.** Shipping CONDOR Mk3 runs at ~2.5 Gbps;
  the mesh wants ~100 Gbps-class (Mk3.1 roadmap) (`optical_comms.md` §1).
- **"GB300 1.36 t rack scope" — UNRESOLVED, foundational.** If the intact rack
  includes the separate NVLink-switch/CDU/PDU sub-racks, per-rack mass rises to
  ~2.5–3 t and every mass figure scales up (`node_mass_model.md` open Q8).
- **Latency/bandwidth confines the market — RISK (bounds the TAM).** Orbital
  links rule out real-time interactive serving; the addressable market is
  latency-tolerant batch/async inference only (`premium_value_case.md` §8).
- **GW-scale thermal — WALL, but deliberately out of scope.** Radiator area
  becomes enormous at multi-MW/GW; the project stays at the 100 kW–~1 MW node
  class below it (`thermal_analysis.md`, `starcloud.md`).
- **Lifecycle carbon / launch emissions — RISK (to the "green" claim, not
  feasibility).** Operation is zero-carbon; launch soot/CO₂/ozone is not. Needs
  honest cradle-to-grave accounting (`premium_value_case.md` §7).

**Net:** every genuine *physics* item is NOT-A-WALL (or an out-of-scope
GW-scale wall). The live list is now dominated by **economic and capability
RISKs** — obsolescence/payback first, the radiator gap second.

---

## 6. Updated strawman architecture

Refreshes the wave-1 strawman with corrected numbers (`lint_report.md`) and the
waves 2–4 comms picture.

- **Orbit:** ~500–600 km **dawn-dusk sun-synchronous** (~97.4–97.8°
  inclination). ~95–100% sunlit, steady thermal state, benign radiation
  (~1–3 krad(Si)/yr behind a few mm Al), largely natural deorbit at the lower
  band (`orbits_environment.md`, `orbit_types_primer.md`).

- **The node = a self-contained satellite, one per Neutron launch.**
  - **Compute:** one intact NVL72-class rack (GB300-class, ~135 kW TDP / ~155 kW
    peak; ~150–185 kW with housekeeping; ~1.36 t bare, ~1.5–1.74 t space-
    modified). Networking/routing folds into the single rack (no second rack)
    (`node_mass_model.md` §2, `ai_hardware.md`).
  - **Thermal:** hot-loop liquid cooling (~60–90 °C) to deployable radiators
    held edge-on to the Sun, **~200–430 m²/rack (working ~300 m²)**, ~1–4 t,
    plausibly co-mounted on the solar-array backside (`lint_report.md` §1.1,
    `node_mass_model.md` §4). **Radiator subsystem must be developed or bought
    — Rocket Lab does not build it** (`space_hardware_capabilities.md` §6).
  - **Power:** ~150–185 kW continuous → **~500–550 m²/rack GaAs or
    ~750–900 m²/rack silicon** roll-out array; ~1.0–2.3 t. Rocket Lab's
    announced arrays are silicon, so the larger silicon figure is the realistic
    baseline (`lint_report.md` §1.5, `node_mass_model.md` §3). Minimal
    batteries (dawn-dusk eclipse-season ride-through, or graceful throttling).
  - **Comms (refreshed):** **optical primary + a modest RF sliver.** 3–4
    Mynaric CONDOR-class optical terminals (target ~100 Gbps Mk3.1) for the
    inter-satellite mesh and space-to-ground; **plus a modest LEO Ka-band RF
    payload** (~100–250 MHz sliver) serving triple duty — all-weather backup
    for the optical ground link, a low-rate direct B2B channel / out-of-band
    control plane, and TT&C (`optical_comms.md`, `rf_satcom.md`,
    `rf_limited_service.md`).
  - **Mass budget:** 1-rack node **~5.4–8.6 t** (design to ~7–9 t; sub-6 t a
    stretch goal) against an estimated **~8.5–9 t reusable Neutron SSO budget**.
    Volume-comfortable, mass-tight. One rack per node, one node per launch
    (`node_mass_model.md` §6).

- **Ground segment — diverse hubs, not homes, not monsters.** **≥4
  geographically diverse optical hubs >1,000 km apart**, each with several
  **modest-aperture (0.6–1.0 m) terminals** + adaptive optics + high-power
  multi-sub-aperture uplink; ~10–12 sites for 99.9%. Customers wire into hubs
  over terrestrial fiber. An RF backup path at each hub. Spend on site count and
  terminal count, **not** aperture (`optical_ground_stations.md`).

- **Constellation for a first service:** start with a single 1-rack node (MVP —
  independently serves a frontier model); first commercial service plausibly
  ~4–8 nodes for throughput, redundancy, and replica load-balancing; grow by
  adding independent rack-replica satellites (`preliminary_findings.md`).
  *(Superseded — re-scoped by the wave-10 minimum-viable-scale study to a
  ~3–4-node Phase-1 / ~3–5-node minimum viable deployment — see
  `CONCLUSION.md` Rev 6.)*

- **Economics overlay (new):** each node costs ~$65–120M (~$85M mid; launch is
  ~60–75% of it) and grosses ~$8M/rack-yr (IaaS) or ~$16M/rack-yr
  (inference-service) — see §2. Baseline-Neutron nodes do **not** pay back as
  standalone compute assets inside the GPU obsolescence window; they are
  justified as build-to-learn and strategic positioning. A standalone-profitable
  node likely needs a block-upgraded, multi-rack, mass-manufactured design.

---

## 7. Recommended next research wave

Prioritised, crisp questions. The §2 obsolescence math exposes the sharpest
ones — they are first.

1. **Node unit economics — the full model.** Build the proper bottom-up cost +
   revenue + opex + payback model for one node, then for a 4–8-node service.
   Replace the §2a spacecraft-hardware estimate ($8–35M) with a real build-up.
   *This is now the highest-priority workstream — it decides the project.*
2. **What revenue/cost combination closes the payback inside ~2–3 years?**
   Solve §2 backwards: required launch $/rack, spacecraft $, premium multiple,
   and revenue model. Identify whether a *baseline*-Neutron node can ever close,
   or whether it is inherently a block-upgrade proposition.
3. **What does a block-upgraded Neutron unlock?** Now justified to explore (it
   was gated on baseline SSO capacity, which §2 shows may be the only path to a
   standalone-profitable node). Multi-rack nodes → launch-$/rack roughly halved.
4. **Spacecraft hardware cost build-up**, especially the **deployable radiator**
   — make-vs-buy, vendor quotes, areal mass, and a productised-radiator cost at
   ~300 m²/rack. (Resolves the §2a weak input and the §5 capability gap.)
5. **Neutron's true SSO payload mass and usable fairing volume** — pursue Rocket
   Lab directly. Still the largest single physical unknown (`neutron_specs.md`).
6. **Resolve the "1.36 t rack scope" definition** — does the intact rack include
   switch/CDU/PDU sub-racks? Rescales every mass figure (`node_mass_model.md`
   Q8). Cheap to resolve; do it first.
7. **The chip→coolant→panel thermal-resistance model** — closes the ~200–430 m²
   radiator-area range and therefore the node mass (`lint_report.md` §1.1).
8. **Customer willingness-to-pay for orbital inference** — customer-discovery
   interviews with sovereign / defense / frontier-lab buyers. The premium case
   is documented only in aggregate $; there is no observed WTP for *orbital*
   compute (`premium_value_case.md` open Q4).
9. **How large is the orbit-addressable inference slice?** Size the
   latency-tolerant batch/async subset of the ~90 GW 2030 inference figure
   (`ai_datacenter_tam.md`, `premium_value_case.md` open Q3).
10. **GPU/HBM lifetime under a hot loop in this orbit** — the hot-radiator vs.
    silicon-longevity trade and the resulting economic life (which directly sets
    the §2 payback window) (`thermal_analysis.md`, `premium_value_case.md`).

---

## 8. Proposed thesis revision (Rev 3)

*Proposed only — the thesis file is not edited here.*

- **Promote the economic crux to the headline.** The thesis should now lead with
  the decisive test: a node cannot be upgraded in orbit, GPUs have a ~2–3 year
  economic life, so **a node must earn back its entire cost — hardware + launch
  — within that window.** "No physics wall" remains true but is no longer the
  most important sentence; the most important sentence is now about payback.
- **State the payback finding honestly.** At raw-GPU-rental rates a
  baseline-Neutron 1-rack node does **not** pay back inside the obsolescence
  window (central ~10 yr). It approaches viability only under the
  inference-service revenue model **and** a genuine premium **and** low-end
  launch/hardware costs acting together. The thesis must not claim the economics
  close — it must claim a *path* exists and name the conditions.
- **Reframe "build to learn" with teeth.** Early baseline-Neutron nodes are
  explicitly *not* standalone-profitable compute assets — their return is
  learning and strategic position, and they should be financed as such. This is
  a sharpening, not a retreat, from the wave-2 framing.
- **Name the standalone-profitable architecture as a block-upgrade
  proposition.** The node that pays back cleanly is plausibly a block-upgraded-
  Neutron, multi-rack, mass-manufactured node — so the block-upgrade question is
  no longer merely "deferred," it is on the critical path to profitability.
- **Adopt the corrected revenue figure.** Use ~$15–20B/GW-yr gross IaaS (~$8M/
  rack-yr) and ~$25–50B/GW-yr gross inference-service (~$16M/rack-yr) as the two
  headline numbers; retire `ai_datacenter_tam.md`'s $3.3B/GW as a revenue
  figure (it is a market-sizing proxy, not revenue).
- **State the premium case's foundation precisely.** The premium rests on
  *terrestrial supply constraints + zero water* — the two strongest, most
  defensible legs — not on generic "space is cool." The sovereign/dedicated/
  green attributes are real demand signals but secondary.
- **Name Rocket Lab's one capability gap: deployable radiators.** The in-house
  stack is otherwise strong-to-complete; the radiator subsystem must be
  developed or bought, and it is simultaneously the cost risk, the mass driver,
  and the deployment risk.
- **Refresh the comms picture:** optical primary + a *modest, deliberately
  limited* RF sliver (backup + B2B channel + TT&C); ground = ≥4 diverse
  modest-aperture hubs, not one monster.
- **Carry forward unchanged:** no physics wall; whole intact racks as the
  Starcloud differentiator; 1 rack/node, 1 node/launch; dawn-dusk SSO;
  hubs-not-homes; compete on cadence and node-level service, not $/kg.

---

## 9. Backlog refresh

Open research questions raised across waves 2–4 that should be **added to
`RESEARCH_TRACKER.md`'s open-questions backlog** (currently a stale pre-wave-1
list — `lint_report.md` §5).

- **Node payback vs. obsolescence** — can a node earn back hardware + launch
  within the ~2–3 yr GPU life? The decisive economic test (this doc §2;
  `premium_value_case.md` §8).
- **Spacecraft hardware cost build-up** — bus + solar + radiator + comms +
  propulsion; no quote exists in any doc (this doc §2a).
- **Deployable radiator make-vs-buy** — Rocket Lab's one capability gap; cost,
  areal mass, vendor options (`space_hardware_capabilities.md` §6).
- **Compute-rack vs. networking-rack split** — raised since wave 1, never
  tracked (`lint_report.md` §5.1, `preliminary_findings.md` §6).
- **GPU/HBM lifetime under a hot loop** — hot-radiator vs. silicon-longevity
  trade; sets the payback window (`lint_report.md` §5.2).
- **Radiator deployment mechanics** — reliability of unfolding an ISS-larger
  radiator from one fairing (`lint_report.md` §5.3).
- **GEO-relay vs. LEO-mesh vs. ground-diversity decision** — the connectivity
  design fork (`orbit_types_primer.md` §6, `lint_report.md` §5.4).
- **Pumped fluid-loop / heat-pipe mass** — folded in crudely, needs its own
  estimate (`lint_report.md` §5.5).
- **"GB300 1.36 t rack scope" definition** — does intact rack include
  switch/CDU/PDU sub-racks? Rescales all mass (`node_mass_model.md` Q8,
  `lint_report.md` §5.6).
- **Eclipse-season battery vs. throttle trade** (`lint_report.md` §5.8).
- **Block-upgraded Neutron** — now on the critical path, not merely deferred
  (this doc §7, §8).
- **Revenue-per-GW reconciliation** — record the §3 resolution (gross IaaS
  ~$15–20B/GW-yr vs. retired $3.3B/GW proxy) so the conflict is closed.
- **Mynaric Mk3.1 ~100 Gbps timeline / mass / power** (`optical_comms.md`).
- **Optical ground network sizing & cost** — exact hub count, terminals/hub,
  capex/opex for target availability (`optical_ground_stations.md` open Q1, Q4).
- **Uplink rate ceiling through turbulence** (`optical_ground_stations.md`
  open Q2).
- **Which specific RF filing/band to acquire**; real RF link budget
  (`rf_limited_service.md` open Qs).
- **Customer willingness-to-pay for orbital inference** — no observed WTP data
  exists (`premium_value_case.md` open Q4).
- **Orbit-addressable inference TAM** — size the latency-tolerant subset
  (`premium_value_case.md` open Q3, `ai_datacenter_tam.md` open Q4).
- **Lifecycle carbon LCA** — launch soot/CO₂/ozone netted against displaced
  grid fossil (`premium_value_case.md` open Q2, §7).
- **Legal reality of "data sovereignty in orbit"** (`premium_value_case.md`
  open Q5).

---

*End of wave-4 synthesis.*
