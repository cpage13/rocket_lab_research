# Initial Thesis — First-Pass Thinking

> Captured 2026-05-17. This is the founder's raw, unfiltered first take. It is
> deliberately *crude* and will be revised as research lands. Nothing here is
> validated yet. The point is to write down the mental model so we can test
> each piece against physics and economics.

## The core idea

Rocket Lab's **Neutron** launches with AI compute racks bolted in. The racks
have **laser comms**. Once in orbit they operate as nodes in a network. This
is almost certainly an **inference-only** play (not training).

## How it might work — the picture in my head

- Neutron goes up with racks already mounted to it / deployed from it.
- Racks carry **laser comm** terminals.
- The nodes sit in **sun-synchronous orbit** and form a network with each
  other.
- On the ground, there is some special location (a hub) that traffic routes
  to. That hub **laser-links up** to the satellites.
  - Open question: do all customers run their own laser ground terminal, or
    does everyone direct traffic into one (or a few) hub locations that own
    the laser uplink?
- Because the compute lives on racks in space, you will need *many* racks and
  they will need to talk to each other — so inter-node networking matters a
  lot.

## Who buys it

- **Not** consumers / normal people.
- **Businesses and corporations.** Possibly the **frontier AI labs**
  themselves, buying dedicated inference capacity.
- Likely sold at a **premium** — you pay more, you get more dedicated /
  isolated space-based capacity.

## What we are actually evaluating

- Is this **bounded by physics** or only by economics?
- If it is "only" economics, that is fine — it can still be **practical in
  the future**. We are not claiming it is the cheapest option today.
- We want to find the **hard barriers** first.

## What we explicitly defer

- Full economics / revenue modeling. We will get there, but not first.
- Whether a **block-upgraded** (uprated) Neutron is required. Possible — but
  we must nail down baseline Neutron payload capacity *before* speculating.

## Things this implies we must research

(These also live in [RESEARCH_TRACKER.md](../RESEARCH_TRACKER.md).)

1. **Neutron** — payload mass, fairing/usable volume. Mass-bound or volume-
   bound for dense racks?
2. **AI data center hardware** — NVIDIA racks, the full chain from the rack
   to the wider data center: power, cooling, networking, wiring.
3. **How LLMs run** — for a model of a given size, how many racks does it
   use? How many racks need to talk to each other? (e.g. what does it take
   to serve "a terabyte" of model.)
4. **Orbital mechanics & space environment** — sun-sync orbit, thermal,
   radiation, power generation. 2026 state of the art.
5. **Laser comms** — inter-satellite and ground-to-space optical links,
   achievable bandwidth.
6. **Competitors** — Starcloud and others pursuing the same idea.

## Comparable: Starcloud

There is at least one company already chasing this — **Starcloud**. Same
basic idea: NVIDIA GPUs in orbit, laser comms, data centers in space. We
should understand what they have actually done and where they think the
barriers are.

---

## Revision 1 — 2026-05-17 (after first research wave)

The first three foundational research docs (Neutron, AI hardware, Rocket Lab)
landed. Three things change the picture:

### 1. This is a Rocket Lab *prime contractor* play, not "racks on a rocket"

Rocket Lab has quietly assembled the whole stack. They acquired **Mynaric**
(laser comms), **Geost** (payloads), and **Motiv** (robotics), and in
February 2026 announced **silicon solar arrays explicitly aimed at
gigawatt-scale space data centers**. So Rocket Lab can plausibly do: launch
(Neutron) + satellite bus + power (solar) + inter-satellite comms (Mynaric
laser) + on-orbit assembly (robotics). The thesis is no longer "bolt racks to
a Neutron" — it is **"Rocket Lab builds, launches, powers, links, and
operates an orbital inference data center, and rents the compute."**

### 2. The binding constraint is thermal, not rack mass

A modern NVL72-class rack is only ~1.36 t but draws ~130–155 kW, ~all of
which becomes heat. In vacuum the only way out is radiation — an estimated
~370–540 m² of radiator *per rack*. Radiator mass/area, not GPU mass, will
dominate the payload budget. **Thermal is the thing to quantify.** It is most
likely a *sizing* problem (how many racks per launch, how much radiator/solar)
rather than a hard "no" — but that must be proven, not assumed.

### 3. Neutron is mass-bound, which forces a launch-strategy question

~13 t to LEO reusable; SSO is undisclosed (~8–10 t estimated). Reusable
(downrange landing) is cheaper per flight but carries less; fully expendable
carries more but throws away the vehicle. So there is a real tradeoff:
**fewer expendable launches vs. more reusable launches** — driven by how much
the racks + radiators + solar + bus actually weigh per node.

## Sharpened thesis statement

> **You *can* use Neutron to build an orbital inference data center.** It is
> not necessarily the most economical way to do compute today — but it works,
> and it does something real: running large, frontier-scale models reliably,
> with dedicated isolated capacity that some customers (corporations, frontier
> labs) will pay a premium for. We believe that premium market is small today
> and significant within ~10 years. Building and deploying now is itself
> valuable: it informs the next rocket design and the next-gen ("block
> upgraded") Neutron, and de-risks the architecture early.

The project's job: produce either **a concrete, physically-grounded path for
how Rocket Lab could do this**, or a hard "no — here is the physics wall."
We lean toward finding the path — but honestly, gated on physics.

## Sequencing note

Evaluate baseline Neutron first ("can you even fit/power/cool a rack or two?").
Only *then* consider a block-upgraded Neutron with more mass/volume — and what
that unlocks (more racks per node, bigger radiators).

---

## Revision 2 — 2026-05-17 (after wave-1 synthesis)

Wave 1 (9 foundational research docs + competitor analysis) is complete and
synthesized in
[../synthesis/preliminary_findings.md](../synthesis/preliminary_findings.md).
The thesis now firms up.

### Headline: no physics wall

**Wave-1 research found no physics wall.** Every candidate hard barrier — heat
rejection in vacuum, power, radiation, comms bandwidth, inference
communication topology — resolves to an *engineering and economics* problem,
not a law-of-physics "no." We can stop hedging on thermal: at the scale we
target it is a sizing problem, not a wall. The honest framing is
**practical-in-the-future, gated on economics and on a handful of
unconfirmed numbers** — not blocked by physics.

The one genuine wall — thermal at multi-MW/GW scale, where radiator area
becomes enormous — sits *above* our target scale. We deliberately stay below
it. That is also where Starship-class economics live, so it is not our fight.

### The differentiator: whole racks

This is now an architectural identity, not a footnote. **We launch standard,
intact NVL72-class server racks in Neutron's large fairing (up to 5.5 m
diameter) and mesh them by laser.** Starcloud constrains its hardware to fit
SpaceX Starship's "PEZ dispenser" form factor; a Neutron play does not.
Hardware can stay near-COTS rack geometry — modified for space, not
redesigned for a dispenser.

### The node, named precisely

- The **minimum viable node is one self-contained NVL72-class rack** — it
  already holds and serves a whole 1–2T-parameter frontier model. You scale
  capacity by adding **independent rack-replica satellites**, not by splitting
  a model across satellites. The old "how many racks must talk to each other"
  worry is dissolved: for inference, essentially one.
- A deployed node likely carries **two rack roles**: compute racks (GPUs/HBM
  serving the model) and networking/routing/packet-handling racks (optical
  mesh, request routing, ground-link aggregation). Sizing this split is a
  research item.
- One Neutron launch delivers **one complete, independently useful node**.
  The node is **1 rack** (the 2-rack node is dropped as a baseline — *corrected,
  see Rev 2.1*): a 1-rack node masses **~5.4–8.6 t** (design to ~7–9 t) against
  an estimated **~8.5–9 t reusable SSO budget** (*corrected — see Rev 2.1*).

### The orbit and ground segment

- **~500–600 km dawn-dusk sun-synchronous orbit** — ~95–100% sunlight, steady
  thermal state, benign radiation, natural deorbit compliance.
- **Ground = hubs, not homes.** Optical ground stations at dedicated/corporate
  sites; **customers wire into those hubs over fiber** — they do not each run
  a laser terminal. Note (corrected after ground-station research): the lever
  is **diversity, not aperture** — no telescope size beats cloud, so the hubs
  are **modest-aperture (~0.5–1 m), multi-terminal**, and you need **≥4
  geographically diverse sites >1,000 km apart** (~99% availability; ~10–12
  for 99.9%). The weather-limited ground link is the leading open *risk*
  (not a wall).

### "Build to learn" is a product line

Early, small-scale deployment is itself saleable. It lets Rocket Lab and
customers learn radiation-hardening, silicon modifications, hot-loop thermal
ops, and on-orbit operations — knowledge that compounds toward larger-scale
buildout. Frontier labs and government/sovereign-compute customers will pay
for that learning as much as for the compute. This is revenue, not just R&D.

### Scale chosen deliberately

Target the **100 kW–~1 MW node class** (1 rack per node, 1 node per launch —
*corrected, see Rev 2.1*) — explicitly *not* GW-scale hyperscale training.
Compete on **cadence, time-to-orbit, and turnkey node-level service**, not on
$/kg.

### What is honestly still open

- **Binding constraint:** kg-to-SSO per Neutron launch (working figure
  ~8.5–9 t reusable — *see Rev 2.1*).
- **Largest unknown:** Neutron's unpublished SSO payload mass (and usable
  fairing volume) — the whole envelope hinges on it. Pursue Rocket Lab
  directly.
- **Leading risk:** the weather-limited optical ground link.
- **Block-upgraded Neutron:** still deferred — gated on confirming baseline
  Neutron SSO capacity first.

## Sharpened thesis statement (Rev 2)

> **Rocket Lab can build an orbital inference data center on Neutron, and no
> law of physics prevents it.** The architecture: self-contained satellite
> nodes — intact, laser-meshed NVL72-class racks — in dawn-dusk SSO, each one
> a complete frontier-model inference unit, served to B2B / government /
> frontier-lab customers through a few large optical ground hubs. It is not
> the cheapest compute today; it does not need to be. It does something real
> and reliable, some customers will pay a premium for it now, and that premium
> market becomes significant within ~10 years. Building now is itself
> valuable — it generates the radiation, silicon, and operations learning that
> guides the next rocket and the block-upgraded Neutron. The remaining
> questions are economics and a handful of unconfirmed numbers — not physics.

---

## Revision 2.1 — lint corrections (2026-05-17)

A wiki health-check ([../synthesis/lint_report.md](../synthesis/lint_report.md))
found that Rev 2's numbers were superseded by the wave-3 node mass model
([../../node_design/node_mass_model.md](../node_design/node_mass_model.md)). This
revision does **not** change the thesis narrative — "no physics wall," whole
racks, hubs-not-homes, dawn-dusk SSO and the build-to-learn framing all stand.
It corrects three numeric/architectural points; inline figures in Rev 2 above
are marked `(corrected — see Rev 2.1)`.

1. **Radiator area is not settled at ~120–210 m²/rack.** The wave-1 thermal doc
   and the wave-3 node mass model bracket the same physics under optimistic vs.
   conservative modeling of radiator surface temperature and second-face
   crediting. The project position is now a **~200–430 m²/rack range with
   ~300 m²/rack as the working planning number**; "120–210 m²" is a superseded
   optimistic low bound. Open item: a real chip→coolant→panel
   thermal-resistance model is still needed to close this.

2. **Node mass / racks-per-launch re-baselined.** A **1-rack node is ~5.4–8.6 t**
   (design target ~7–9 t; sub-6 t is a stretch goal). A **2-rack node is
   ~9.6–16.6 t**, which blows the reusable launch budget — it is **dropped as a
   baseline**. The architecture is **one rack per node, one node per Neutron
   launch**. The earlier "~6 t / ~11 t, ~1–2 racks" framing is superseded.

3. **Neutron SSO figure standardized.** Earlier docs used ~10 t reusable; the
   later, more conservative node mass model uses ~8.5 t. The project now
   standardizes on **~8.5–9 t reusable to SSO**. It remains an estimate —
   Rocket Lab has not published a Neutron SSO performance number.

---

## Revision 3 — 2026-05-17 (after wave-4 economics synthesis)

Wave 4 (the economics docs — TAM, revenue-per-watt, the premium value case —
plus Rocket Lab's space-hardware capabilities) is complete and synthesized in
[../synthesis/wave4_synthesis.md](../synthesis/wave4_synthesis.md). The centre
of gravity of the thesis now moves: the question is no longer "is there a
physics wall" but "do the economics close."

### 1. Headline: still no physics wall — but the crux is now node payback vs. GPU obsolescence

**Wave 4 found nothing that overturns "no physics wall."** Every physics item
remains NOT-A-WALL (or an out-of-scope GW-scale wall). But the project's
verdict has sharpened from *practical-in-the-future, gated on a few numbers* to
**practical-in-the-future only if the node pays back inside the GPU
obsolescence window — and that is now the single make-or-break question.**

The decisive test: a node **cannot be upgraded in orbit**, GPUs have a ~2–3
year economic life, so the entire node — rack, bus, solar, radiator, comms, and
the launch cost — **must earn back its full launched cost within that ~2–3 year
window.** Terrestrial operators rack-and-replace GPUs inside a long-lived shell;
an orbital node strands the whole asset when the silicon ages out. "No physics
wall" remains true, but it is no longer the most important sentence — payback
is.

### 2. The payback finding, stated honestly

The architecture is fixed at **1 rack per node, 1 node per Neutron launch**.
On that unit:

- A baseline-Neutron node costs **~$65–120M (~$85M mid)** — launch is ~60–75%
  of it, so the economics are launch-dominated, not GPU-dominated.
- At **raw-GPU-rental rates** (selling GPU-hours) the node does **not** pay
  back inside the obsolescence window in *any* cost case — central payback is
  ~10 years, ~3–5× too slow.
- Under the **inference-service model** (selling tokens, with a ~1.5–2.5×
  model-value markup) it only reaches the window in its most optimistic corner
  (~2.6 yr at low cost + high revenue); the central inference case is still
  ~5 years.
- The gap closes **only** with inference-service revenue **and** a genuine
  premium **and** low-end launch/hardware costs acting together. No single
  lever is enough.

So a **baseline-Neutron node is explicitly not a standalone profit centre.**
The thesis does not claim the economics close — it claims a *path* exists and
names the conditions.

### 3. V1 is a premium "build-to-learn" product — a deliberate multi-generation play

This is where the founder's refinement and the wave-4 synthesis **independently
converge on the same conclusion**, and that convergence is itself a signal.

**The founder's framing — "build to learn → next-generation price drop":**
Version 1 (baseline Neutron) is not expected to capture peak economics, and
that is fine *by design*. The analogy is electric cars: not cheap at first,
sold into a premium segment, where the early product both earns revenue **and**
generates the learnings. The learnings here are silicon-level
(radiation-hardening, running chips with less cooling and structural mass),
thermal and packaging technique, and on-orbit operations. Those learnings
compound. The big cost drop and the real profits arrive with the **next
generation** — whether a block-upgraded Neutron, a new vehicle, or simply
accumulated technique. This is a deliberate **multi-generation play**:

- **V1** = premium segment + learning + modest revenue. Financed and justified
  as build-to-learn and strategic position, *not* as a standalone profit
  centre.
- **V2** = the scaled, genuinely profitable product.

**The wave-4 synthesis reached the same place from the numbers.** Working the
payback arithmetic from the bottom up, it found that a baseline-Neutron node
does not pay back inside the GPU obsolescence window and is best understood as
"build-to-learn" — and that the standalone-profitable node is plausibly a
**block-upgraded-Neutron, multi-rack, mass-manufactured-node** proposition. So
the block-upgrade question is no longer merely "deferred": it is on the
**critical path to profitability.** Founder intuition and independent economic
analysis arriving at the identical structure is the strongest form of
corroboration the project has produced so far.

This is a *sharpening* of the Rev 2 "build to learn" framing, not a retreat —
it now has teeth and a numeric basis.

### 4. Revenue figures reconciled — adopt the bottom-up number

Wave 4 resolved a ~5–10× conflict between two revenue figures. They measure
different things: `ai_datacenter_tam.md`'s **~$3.3B/GW-yr** is a crude
top-down market-sizing proxy (services market ÷ capacity); `revenue_per_watt.md`'s
**~$15–20B/GW-yr gross IaaS** is built bottom-up from observed rack rental rates
and company disclosures. For a payback test the bottom-up figure is correct.

- **Headline revenue: ~$15–20B/GW-yr gross IaaS** (~$8M/rack-yr), and
  **~$25–50B/GW-yr gross inference-service** (~$16M/rack-yr, conditional on
  owning a competitive model).
- The **$3.3B/GW proxy is retired as a revenue figure** — kept only for
  order-of-magnitude market sizing.

### 5. What is honestly still open

- **Node unit economics — the full model.** A proper bottom-up cost + revenue
  + opex + payback model for one node, then a 4–8-node service. Highest
  priority — it decides the project.
- **The spacecraft-hardware cost line ($8–35M)** is the weakest input; no
  direct quote exists in any doc. Needs a real build-up.
- **The deployable radiator** — Rocket Lab's one capability gap — is
  simultaneously the cost risk, the mass driver, and the deployment risk.
  Make-vs-buy unresolved.
- **Neutron's true SSO payload mass** remains the largest single physical
  unknown and sets the whole launch-cost-per-rack term.
- **Customer willingness-to-pay for *orbital* inference** is documented only in
  aggregate market $; no observed WTP exists.
- **Whether a baseline-Neutron node can *ever* close**, or whether profitability
  is inherently a block-upgrade proposition.

## Sharpened thesis statement (Rev 3)

> **Rocket Lab can build an orbital inference data center on Neutron, and no
> law of physics prevents it — but the decisive question is now economic: can a
> node earn back its entire launched cost inside the ~2–3 year GPU obsolescence
> window?** A node cannot be upgraded in orbit, so when the silicon ages out
> the whole asset is stranded. Wave-4 arithmetic is honest: a baseline-Neutron
> 1-rack node does **not** pay back at raw-GPU-rental rates (central ~10 yr),
> and reaches the window only in the best corner of the inference-service model
> stacked with a genuine premium and low-end costs. The thesis therefore does
> not claim the economics close — it claims a *path* exists and names the
> conditions. **Version 1 (baseline Neutron) is by design a premium,
> build-to-learn product, not a standalone profit centre.** Like early electric
> cars, it sells into a premium segment, earns modest revenue, and — crucially —
> generates the compounding learnings (radiation-hardened silicon, lighter
> thermal and structural design, on-orbit operations) that make the *next*
> generation cheap and genuinely profitable. This is a deliberate
> multi-generation play: V1 learns and positions; V2 — plausibly a
> block-upgraded-Neutron, multi-rack, mass-manufactured node — is the scaled,
> profitable product. The founder's "build to learn → next-generation price
> drop" intuition and the independent bottom-up wave-4 economics arrived at the
> identical structure. Plan on **~$15–20B/GW-yr gross IaaS (~$8M/rack-yr)** and
> **~$25–50B/GW-yr gross inference-service (~$16M/rack-yr)** as the revenue
> figures; the old $3.3B/GW proxy is retired. The block-upgrade question is no
> longer deferred — it is on the critical path to profitability.

**Carried forward unchanged from Rev 2:** no physics wall; whole intact racks
as the Starcloud differentiator; 1 rack/node, 1 node/launch; dawn-dusk SSO;
hubs-not-homes (≥4 diverse modest-aperture optical ground stations); a modest,
deliberately limited RF sliver alongside optical primary; compete on cadence
and node-level service, not $/kg.

---

## Revision 4 — 2026-05-17 (after wave-5 synthesis)

Wave 5 (the re-baseline docs — corrected Neutron payload + block-upgrade,
hot-chip thermal trajectory, rack cost trajectory, rack internals, solar/radiator
trajectory, reliability, energy/operating costs — plus the two models) is
complete and synthesized in
[../synthesis/wave5_synthesis.md](../synthesis/wave5_synthesis.md). Rev 3 left
the project on a hard question: a baseline-Neutron node does **not** pay back
inside the GPU obsolescence window, and the economically-favorable generation
seemed un-flyable. Wave 5 answers that question — **the crossover resolves.**

### 1. The crossover is resolved — at Vera Rubin

Wave 4 found a *crossover*: GPU economics improve generation-over-generation
while node flyability degrades, and flyability failed **first** — the node
became un-flyable one generation *before* the economics turned clearly
favorable. The favorable generation was **Vera Rubin** (~300 kW rack, ~2-yr
inference-service payback, inside the ~2–3 yr window), and wave 4 said it could
not fly on a baseline reusable Neutron.

Wave 5 supplies **three levers** that together close most of that gap:

1. **A corrected, higher Neutron SSO payload.** Deep verification
   ([../../rocket_lab/neutron/payload_and_block_upgrade.md](../rocket_lab/neutron/payload_and_block_upgrade.md))
   supersedes the prior conservative ~8.5 t with a working **~9.5 t reusable
   to SSO** (a ~70% LEO→SSO retention factor). That ~1 t is decision-relevant
   against a ~7–10 t node.
2. **A hot-loop radiator.** The radiator is the heaviest power-scaling
   subsystem and the only one with a 4th-power lever. Riding the warm-water
   cooling trajectory the industry is already on (Rubin spec'd for 45 °C
   supply), the radiator surface moves from ~40–50 °C to ~70–80 °C *without
   cooking the silicon* — the chip junction is decoupled from the radiator by
   the loop ΔT. Via the Stefan-Boltzmann T⁴ term this cuts radiator mass
   **~40–55%**.
3. **A credible block-upgraded Neutron** at **~12–13 t SSO** — a ~+15–30%
   uprate, credible by analogy (Electron grew +33% on the same airframe; the
   de-stressed Archimedes has shown 102% power) but unannounced and years
   post-debut: upside, not baseline.

**Reconciled flyability ceilings** (1-rack reusable node, the wave-4 effective
~163–214 kW figure is now superseded — it omitted the SSO correction and the
hot-loop lever):

- **~200–250 kW** — baseline Neutron (~9.5 t SSO), working ~225 kW.
- **~270–320 kW** — baseline Neutron + hot-loop radiator, working ~300 kW.
- **~430–470 kW** — block-upgraded Neutron (~12.5 t SSO) + hot-loop, working ~450 kW.

The single most important number-change: the working ceiling for a buildable
design (baseline + hot-loop) moves to **~300 kW** — and ~300 kW is exactly the
Vera Rubin rack power. **A power-capped Rubin node (~190–250 kW NVL72-class)
flies on a baseline Neutron + hot-loop; a full ~300 kW Rubin node flies on a
block-upgraded Neutron + hot-loop.** The architecture *reaches* the favorable
generation — marginally, and exactly one generation later than a frictionless
path would. **Rubin Ultra (~600 kW) stays un-flyable intact** on any Neutron
configuration; it needs power-capping, on-orbit assembly, or a larger vehicle.
The crossover is resolved, not stranded. The architecture stays **1 rack per
node, 1 node per launch** — the block-upgrade buys one more *power* generation
per single-rack node, **not a second rack** (the founder's wave-5 ~2-rack
hypothesis is not supported by the mass model — a 2-rack node exceeds even the
expendable budget).

### 2. The favorable verdict is conditional — name the conditions precisely

The crossover resolves *only* under specific conditions, and the thesis must
say so plainly:

- **Revenue model.** The favorable verdict holds only under the
  **inference-service** revenue model (selling tokens, with a model-value
  markup). At raw-GPU-rental (IaaS) rates the same nodes pay back ~2–3× slower
  and do **not** clear the obsolescence window at any generation. The thesis
  closes on selling competitive frontier-model *inference*, not GPU-hours.
- **Two unpublished Rocket Lab numbers.** The ~9.5 t SSO payload and the usable
  fairing volume are analyst estimates — Rocket Lab publishes neither. ±1 t of
  SSO payload swings the flyability ceiling ±~40 kW.
- **An un-quoted cost.** The spacecraft-hardware cost line ($8–35M, ~$18M mid)
  is the weakest input in the whole project; no direct quote exists. It decides
  whether V2 payback lands at ~2 yr or worse.

### 3. The premium framing, stated honestly — three tiers

The product is **never cheaper than terrestrial compute**; it is a premium
product whose buyers pay for capacity they cannot get on the ground. Stated as
three honest tiers:

- **(a) Pre-favorable — V1 / GB300-class, baseline Neutron.** The orbital
  product is **~5–10× terrestrial cost per token** — *not* cost-competitive,
  and it does not pay back inside the GPU window (~3.1 yr inference, at the
  upper edge). It is sold for the **learnings** (radiation-hardened silicon,
  hot-loop thermal ops, deployable-radiator engineering, on-orbit operations),
  for **strategic position** ahead of Starcloud, and to a narrow set of
  sovereign / defense / dedicated-capacity buyers — **not for competitiveness.**
- **(b) Premium-but-viable — V2 / Vera Rubin, block-upgraded Neutron + hot-loop.**
  The premium compresses to **~1.5–2.5× terrestrial** cost per token; payback
  reaches ~2 yr, inside the obsolescence window. Customers plausibly pay
  **~50–100% more per token** for dedicated, physically isolated, 24/7-reliable,
  single-tenant, sovereign capacity they genuinely cannot get on the ground
  (5-yr grid-interconnection queues, 5-yr transformer lead times, water-permitting
  moratoria, sovereign-AI demand at ~$19B in 2026 → ~$177B by 2035). This is
  the tier where the thesis is a real business — the premium is paid for
  capacity-you-can-actually-get + isolation + zero water + schedule certainty,
  not for cheaper compute.
- **(c) Favorable — V2+ at scale, mass-manufactured nodes and/or a cheaper
  launch generation.** Payback closes cleanly and the premium shrinks toward
  **~0–25%**, sustained by the off-grid / zero-water / sovereign attributes
  rather than scarcity pricing. This is the multi-generation endpoint, not a
  2026–2028 proposition.

**Stated plainly: a ~50% premium is plausible; a 1,000× premium is not — and
the thesis never needs it.** The product lives or dies on whether a real buyer
pays the ~50% Tier-(b) premium; the evidence (terrestrial supply crunch,
sovereign-AI growth, dedicated-capacity demand) says that is plausible — not
certain. There is **no observed willingness-to-pay data for orbital inference
specifically**, so customer discovery is the highest-value commercial unknown.

### 4. V1 → V2, carried forward and sharpened from Rev 3

The Rev-3 "build-to-learn → V2" multi-generation framing stands and now has a
numeric basis:

- **V1** — a GB300-class rack on a baseline Neutron. Against the corrected
  ~9.5 t SSO budget a ~6.8 t node flies with ~2.7 t of margin — *comfortable*,
  no longer mass-tight. But it does not pay back inside the window. Finance and
  justify it as **build-to-learn + strategic position**, and **time it now** —
  the baseline-vehicle window is GB200/GB300-class racks in roughly 2025–2026.
- **V2** — a full ~300 kW Vera Rubin-class node on a block-upgraded Neutron +
  hot-loop. This is the **standalone-profitable product** the thesis has
  pointed at since Rev 3, ~2-yr inference-service payback — reachable, gated on
  the block-upgrade being pursued and on the token-selling revenue model.

### 5. What is honestly still open

- **Neutron's unpublished SSO payload** — the largest single physical unknown.
- **The block-upgrade dependency** — credible but uncommitted; the central V2
  dependency, on the critical path to profitability.
- **The deployable-radiator capability gap** — Rocket Lab's one stack gap; the
  biggest mass line and a major un-quoted cost. Hot-loop makes the radiator
  lighter but does not close the capability gap.
- **Coolant-loop reliability** — the leading whole-node-kill mode; manageable
  with N+1 redundancy, but hot-loop operation slightly worsens the wear-out.
- **Customer willingness-to-pay for orbital inference** — no observed data.

## Sharpened thesis statement (Rev 4)

> **Rocket Lab can build an orbital inference data center on Neutron, no law of
> physics prevents it — and wave 5 shows the economics now close, marginally,
> at the Vera Rubin generation.** Wave 4 left a cruel crossover: GPU economics
> turned favorable (~Vera Rubin, ~300 kW, ~2-yr payback) only *after* the node
> had become un-flyable on a baseline reusable Neutron. Three wave-5 levers
> resolve it — a corrected ~9.5 t SSO payload, a hot-loop radiator that cuts
> radiator mass ~40–55% via the T⁴ term, and a credible block-upgraded Neutron
> at ~12–13 t SSO — lifting the 1-rack flyability ceiling to **~200–250 kW
> baseline, ~270–320 kW baseline + hot-loop, ~430–470 kW block-upgraded +
> hot-loop.** A power-capped Rubin node flies on baseline Neutron + hot-loop; a
> full ~300 kW Rubin node flies on a block-upgraded Neutron — the architecture
> reaches the favorable generation, one generation later than a frictionless
> path, with Rubin Ultra (~600 kW) still un-flyable intact. The verdict is
> **conditional**: it holds only if Rocket Lab sells inference (per-token), not
> raw GPU-hours, and it rests on two numbers Rocket Lab has not published (SSO
> payload, fairing volume) plus an un-quoted spacecraft-hardware cost. The
> product is never cheaper than terrestrial compute — it is a **premium**
> product in three honest tiers: V1/GB300 today is ~5–10× terrestrial cost per
> token, sold for learnings and strategic position, not competitiveness;
> V2/Rubin is ~1.5–2.5× terrestrial with a ~2-yr payback, and customers
> plausibly pay ~50–100% more for dedicated, isolated, 24/7, sovereign capacity
> they cannot get on the ground; at scale the premium shrinks toward ~0–25%. A
> ~50% premium is plausible; a 1,000× premium is not, and the thesis never
> needs it. **V1 remains the build-to-learn product, timed now; V2 — a
> block-upgraded Neutron, hot-loop, Rubin-class node — is where it becomes a
> standalone-profitable business.**

**Carried forward unchanged from Rev 3:** no physics wall; whole intact racks
as the Starcloud differentiator; 1 rack/node, 1 node/launch; dawn-dusk SSO;
hubs-not-homes (≥4 diverse modest-aperture optical ground stations); a modest
RF sliver alongside optical primary; compete on cadence, time-to-orbit and
node-level service, not $/kg; **~$15–20B/GW-yr gross IaaS (~$8M/rack-yr)** and
**~$25–50B/GW-yr gross inference-service (~$16M/rack-yr)** as the revenue
figures.

---

## Revision 5 — 2026-05-17 (consolidated catch-up: waves 6–11)

> **Why this is one consolidated revision.** The thesis was frozen at Rev 4
> (wave-5 vintage) while the conclusion document ran on through six further
> waves of founder input to `CONCLUSION.md` Revision 7. Rather than
> back-fill six separate revisions, this single **Revision 5** brings the
> thesis level with `CONCLUSION.md` Rev 7 — folding in everything from waves
> 6–11. It is **append-only**: Revisions 1–4 above are untouched. Where Rev 4
> figures are now superseded, the supersession is stated here rather than by
> editing Rev 4. The authoritative live state is always `CONCLUSION.md`; this
> revision keeps the belief-record honest about how far the project has moved.

### 1. The launch cost was mis-categorised — re-based to a ~$10–20M internal marginal cost

The single largest economic change since Rev 4. Revisions 1–4 costed every
node at the **~$50–55M price Rocket Lab charges external launch customers** —
a price that carries Rocket Lab's ~50% launch-business gross margin. But the
thesis is **Rocket Lab flying its own payloads**, so the correct figure is the
**internal marginal cost**: a deliberately cheap expended second stage +
propellant + first-stage refurbishment + range/ops, with the reusable first
stage amortized over ~15 flights and Electron already absorbing the
fixed/common overhead. That is a defensible **~$10–20M** (founder judges it may
reach ~$10M with full fast first-stage reuse) — model it as a **$10–20M range**,
not a point, and keep ~$55M only as an external-price sensitivity.

Consequences: a V1 GB300-class node falls from the Rev 3/4 **~$65–120M** to
**~$35–65M (~$45M mid)**, launch drops from ~85% of node cost to **~45%**, and
the un-quoted ~$8–35M spacecraft-hardware line becomes co-equal with launch as
the largest swing factor. This is the change that moves the central V2 case
from "fails the all-in test by a thin margin" to "passes at a ~25–40%
premium." *(`CONCLUSION.md` Rev 4.)*

### 2. The V2 definition is corrected — V2 closes on baseline Neutron + hot-loop

Rev 3/4 put the **block-upgraded Neutron on the critical path to V2
profitability** and defined V2 as "a block-upgraded Neutron, hot-loop,
Rubin-class node." **That is superseded.** The converged build-strategy work
(Engineer ↔ CFO loop) and `CONCLUSION.md` Rev 6 demote the block-upgrade from
critical path to **pure margin upside**: **V2 closes on a baseline Neutron +
hot-loop radiator** — a power-capped Rubin-class node — and does *not* depend
on an uncommitted future rocket. The block-upgrade remains attractive (it buys
one more power generation per single-rack node) but it is no longer a gating
dependency. This removes the most uncomfortable speculative dependency from
the thesis. The architecture stays **1 rack/node, 1 node/launch** — no 2-rack
node is ever needed.

### 3. 5-year GPU service life is the base case — not the 2–3-year window

Revisions 3–4 framed the economics on the harsh **~2–3-year GPU obsolescence
window**. That window is now demoted. A space payload that dies in 2–3 years
is not a serious proposition; LEO satellites last ~5 years anyway, terrestrial
operators now run GPUs ~7 years, and "obsolete ≠ broken." The proposal
**requires ~5 years of radiation-hardened, derated, N+1-cooled GPU service
life as the base case**, models revenue as a *declining curve* over that life
(frontier rates early, batch/async tail later — not flat, not a cliff), keeps
the **2–3-year case only as a clearly-labelled downside addendum**, and a
~7-year life as upside. This materially improves the cumulative-crossover math.
*(`CONCLUSION.md` Rev 2/3.)*

### 4. The venture J-curve — per-node payback is sound; the venture is capital-hungry and long-duration

A venture-level investor pro-forma (`data_science/INVESTOR_PROJECTION.md`) was
built. It draws the crucial **per-node vs. venture-level distinction**:

- **Per-node payback ~2.5–2.8 years** — the *asset* is sound; one node earns
  back its cost well inside its 5-year life.
- **Venture-level cumulative cash-flow crossover ~year 19–20**, behind a
  **~$1.15B peak funding requirement** — because a fast-scaling infrastructure
  venture deploys new nodes ahead of existing-node earnings
  ("deploy-ahead-of-earnings") and carries ~$485M of build-to-learn R&D.

Both are valid measures, not a contradiction. The honest investor read: this
is a **~$1B+, long-duration, asymmetric** bet with sound unit economics — a
patient-capital / strategic-position play, not a fast-payback one. Decisive
sensitivities: at a **+100% premium** the venture crossover pulls in to
**~year 11**; at a **+25% premium** *or* a 2–3-year GPU life it **never crosses
within 25 years**. Venture success hinges on a real premium and the 5-year
life holding. *(`CONCLUSION.md` Rev 5.)*

### 5. The converged build strategy — a gated ramp with a minimum-viable ~3–5-node deployment

The Engineer ↔ CFO refinement (`strategy/optimized_strategy.md`) and
`CONCLUSION.md` Rev 6 settle the build path:

- **Gated ramp:** a 1-node Phase-0 demonstrator → a **~3–4-node Phase-1 anchor
  deployment** → a ~12–24-node Phase-2 network, with **Phase 1→2 gated on a
  signed sovereign / defense / frontier-lab anchor customer** at or above the
  ~+50% premium — so only **~$300M** of capital is at risk before the
  willingness-to-pay question is answered, not ~$1.15B.
- **Minimum viable commercial deployment is ~3–5 replica nodes**
  (`llm_compute/minimum_viable_scale.md`): one node is a *mid-market-scale*
  service (~5–15k concurrent chat users, ~1–3k agentic); a commercially
  worthwhile service needs ~3–5 replica nodes (N+1, ~1–7M users, ~$30–100M/yr).
  Scale by independent replicas; two-node laser-meshing is reserved for
  model-*size* headroom (future >10–15 T models), not throughput.
- Steady-state cadence **capped below ~7 nodes/yr** to hold the funding peak
  down; the **ground segment resolved to the lean ~$150M end** of the
  $100–500M band; the **relay layer deferred** (zero V1 spend).

### 6. In-house radiator ownership — the one capability gap, decided

The deployable radiator is Rocket Lab's single clear stack gap and is
simultaneously the biggest mass line, a major un-quoted cost, and the leading
deployment risk. Rev 4 left make-vs-buy open. The decision (founder wave 11,
`CONCLUSION.md` Rev 7): **Rocket Lab should own the radiator** — develop it
in-house or **acquire a thermal/radiator company** (the SolAero / Mynaric /
Motiv acquisition playbook). Off-the-shelf is a **V1 stopgap only**; a
~$20–25M Phase-0 in-house hot-loop radiator R&D programme is endorsed. The
radiator is too critical to keep buying perpetually.

### 7. Present both cases — the conservative gated case AND the ambition "$5B" case

The conservative gated case alone undersells the opportunity: ~$500M revenue
by year 10 is ~0.003% of the ~156 GW AI-DC market and does not move a
~$70–100B company's equity. The thesis must therefore carry **two cases side
by side** (`economics/ambition_case.md`, `CONCLUSION.md` Rev 7):

- **Conservative gated build-to-learn case** — ~35 nodes / ~$500M revenue /
  ~$86M profit by year 10; ~year-19–20 crossover; ~$1.15B peak funding.
- **Ambition "go for it" case** — ~$5B/yr revenue → a ~420-node fleet,
  ~85–110 Neutron launches/yr (central ~95), launch cost amortizing
  ~$20M→~$10M with cadence, ~$28–34M node cost, ~$1.6B/yr profit at ~32%
  margin, ~$14–22B of staged capital.

The **counter-intuitive key finding: the ambition case crosses over *sooner*
(~year 13–16) than the conservative case (~year 19–20)** — revenue scales ~10×
while capital-at-risk scales only ~13–18×, and launch-cost amortization
expands net margin from ~17% to ~32% in the back half. The conservative case
is slow *because* it stays small. And the venture is **buildout-limited, not
demand-limited**: even $5B is ~0.03% of the market, so the binding constraint
is fleet build-rate, launch cadence, and the premium holding — never customer
demand. The ambition case's two load-bearing, unobserved risks are the **~8×
Neutron cadence ramp** (vs. Rocket Lab's published "monthly" plan) and the
**premium holding** (decaying to ~+50%) across 400+ nodes.

### 8. What is honestly still open

- **Neutron's unpublished SSO payload mass and usable fairing volume** — the
  largest single physical unknown; working figure ~9.5 t reusable to SSO.
- **The ~$10–20M internal launch cost** traces to a founder back-of-envelope
  build-up, not a sourced Rocket Lab figure — and it is the single largest
  driver of the favourable re-base. Disclosed as an open unknown, not removed.
- **Customer willingness-to-pay for orbital inference** — no observed data; the
  highest-value commercial unknown, and what the Phase-1 gate exists to retire.
- **The deployable-radiator capability gap and its cost** — now an in-house
  ownership commitment, but the build/acquire cost is still un-quoted.
- **Coolant-loop reliability** — the leading whole-node-kill mode; hot-loop
  operation slightly worsens the wear-out.

## Sharpened thesis statement (Rev 5)

> **Rocket Lab can build an orbital inference data center on Neutron, no law of
> physics prevents it, and the economics now close at a plausible premium —
> with the decisive risks economic and unobserved, not physical.** Waves 6–11
> sharpened the picture in four ways. First, the **launch cost was
> mis-categorised**: the thesis is Rocket Lab flying its own payloads, so the
> right figure is the **~$10–20M internal marginal cost**, not the ~$50–55M
> external price — this pulls a V1 node from ~$65–120M to **~$35–65M (~$45M
> mid)** and flips the central V2 case to "passes the all-in test at a ~25–40%
> premium." Second, **V2 no longer depends on an uncommitted rocket**: it
> **closes on a baseline Neutron + hot-loop radiator**, with the block-upgrade
> demoted to pure margin upside — the architecture stays 1 rack/node, 1
> node/launch and never needs a 2-rack node. Third, the economics run on a
> **5-year GPU service-life base case** (2–3 years is only a downside
> addendum). Fourth, the **per-node payback is sound (~2.5–2.8 yr)** but the
> **venture-level crossover is long (~year 19–20)** behind a **~$1.15B peak
> funding** requirement — this is a patient-capital, strategic-position bet,
> not a fast-payback one. The build path is a **gated ramp** — a 1-node
> demonstrator → a ~3–4-node Phase-1 anchor deployment → a ~12–24-node Phase-2
> network, with Phase 1→2 gated on a signed sovereign/frontier-lab anchor
> customer so only ~$300M is at risk before willingness-to-pay is tested; the
> **minimum viable commercial deployment is ~3–5 replica nodes**. Rocket Lab
> should **own the deployable radiator** — its one capability gap — in-house or
> by acquisition, not buy it perpetually. And the thesis must be told as **two
> cases**: a conservative gated build-to-learn case (~$500M revenue by year 10)
> and an ambition "$5B go-for-it" case (~420-node fleet, ~$1.6B profit, ~32%
> margin) — where, counter-intuitively, **going bigger crosses over *sooner*
> (~year 13–16 vs. ~19–20)** because revenue scales faster than capital-at-risk
> and launch-cost amortization expands margin at scale. The venture is
> **buildout-limited, not demand-limited**. The verdict is unchanged in kind —
> **fund the bounded build-to-learn programme toward an honest go/no-go gate**
> — but the gate now opens onto a real choice between a modest ~$500M business
> and a ~$5B / ~$1.6B-profit second pillar for Rocket Lab.

**Carried forward unchanged from Rev 4:** no physics wall; whole intact racks
as the Starcloud differentiator; 1 rack/node, 1 node/launch; dawn-dusk SSO;
hubs-not-homes (≥4 diverse modest-aperture optical ground stations); a modest
RF sliver alongside optical primary; compete on cadence, time-to-orbit and
node-level service, not $/kg; the three-tier premium framing (V1 a premium
product sold for learnings and strategic position, V2 premium-but-viable, the
premium shrinking toward ~0–25% at scale); **~$15–20B/GW-yr gross IaaS
(~$8M/rack-yr)** and **~$25–50B/GW-yr gross inference-service (~$16M/rack-yr)**
as the revenue figures.

---

## Revision 6 — 2026-05-17 (the moonshot ceiling and the bigger-rocket reframe)

Two new analyses — `economics/moonshot_50b.md` and `economics/moonshot_150b.md`
— stress-tested the *top* of the scenario ladder, and `CONCLUSION.md` advanced
to Revision 8 to fold them in. This Revision 6 brings the thesis level with
that: it is **append-only** (Revisions 1–5 untouched) and records the one thing
the moonshot work changed about what we believe — **where the ceiling is, and
what lies past it.**

### 1. The moonshot is infeasible on Neutron — and that bounds the thesis

The Rev-5 thesis carried two cases: a conservative ~$500M build-to-learn case
and a ~$5B ambition case. It left open — implicitly — how high the orbital data
center could go. The two moonshot analyses, modelled as target-driven
back-solves over a ~10–12-year horizon, close that question:

- **$50B/yr is infeasible on Neutron.** It back-solves to a **~5,000-node
  fleet**, **~1,000–1,300 Neutron launches/yr** (~6–8× the all-time annual
  launch record — SpaceX's 165 in 2025), and **~$150–250B of cumulative
  capital** (~2.5–3.5× Rocket Lab's market cap)
  (`economics/moonshot_50b.md` §7).
- **$150B/yr is infeasible by a wider ~15–20× margin** — **~15,000 nodes**,
  **~3,000 launches/yr** (~18× the world record), **~$900B–1.2T of capital**
  (`economics/moonshot_150b.md` §7).
- **The binding wall is launch cadence, and it is structural.** Because the
  architecture is rigidly **1 rack per node, 1 node per launch** (Neutron is
  mass-bound at a single ~250 kW node to SSO and cannot carry more —
  `node_design/node_mass_model.md`; `simulations/REPORT.md`), the launch count
  is *chained* to the node count and the node count is *chained* to the revenue
  target. Cadence cannot be engineered down. No amount of capital or will
  closes a ~6–18× gap over the all-time human launch record.

So the thesis now carries an honest ceiling: **on Neutron, this venture tops
out at ~$5–10B/yr of revenue.** The ~$5B ambition case is *not* a rung below
the summit — it **is** approximately the summit, the top of the Neutron ladder
(`economics/moonshot_50b.md` §7; `economics/moonshot_150b.md` §7.3, both
deriving a ~$5–10B realistic ceiling independently).

### 2. The ceiling is a real business — but honestly bounded

This finding is substantial, not disappointing — and the thesis states it in
both directions. A ~$5–10B/yr orbital inference business **more than doubles
all of Rocket Lab** (~$600M FY2025 revenue), at the ambition case's ~32% net
margin it is the company's **first major profit pool** (~$1.6–3B/yr), and it is
a genuine second pillar alongside launch. But it is honestly **not** a
$50–150B, company-redefining line — and at $50B+ the orbital venture would
also have lost its *reason to exist*, since at ~1–3% of global AI compute the
scarcity premium is gone and it becomes a commodity supplier with a structural
cost disadvantage versus terrestrial power (`economics/moonshot_50b.md` §6).
The orbital data center on Neutron is a **single-digit-billions opportunity,
not a fifty-billion one.**

### 3. The reframe — the moonshot is a bigger-rocket bet, a two-act arc

The moonshot infeasibility is a hard wall, but it is not a dead end, and the
thesis presents it constructively. Both moonshot analyses converge on the same
genuine escape hatch: **the launch count only stops exploding if the unit of
deployment changes.** A Starship-class vehicle (~100–150 t to LEO) could carry
**10–60 racks per launch**, collapsing the $150B cadence requirement from
~3,000 launches/yr to ~50–130/yr — back inside demonstrated territory
(`economics/moonshot_50b.md` §3.4; `economics/moonshot_150b.md` §3.3). **The
$50B+ tier and a heavy-lift, many-racks-per-launch vehicle are therefore the
same bet** — you cannot have the company-redefining tier without the bigger
rocket, and the bigger rocket is what unlocks it.

That reframes the venture as a **two-vehicle, two-decade arc**:

- **Act I — Neutron (V1 → ambition case).** The build-to-learn program and, on
  a go decision, the ~$5B ambition case run on Neutron. Act I proves the
  orbital-inference model end-to-end (premium, 5-year hardware life, hot-loop
  thermal, on-orbit operations), builds the sovereign/defense/frontier-lab
  customer base, and earns the ~$1.6–3B/yr of profit that makes Act II
  *fundable*.
- **Act II — a Neutron successor (the bigger rocket).** A heavy-lift vehicle
  carrying tens of racks per launch breaks the one-rack-per-launch chain and
  lifts the ceiling off ~$10B. The company-redefining $50B+ tier lives in Act
  II — reachable only because Act I happened and made the next rocket fundable.

The genuine path past ~$10B is not "work Neutron harder" (that is the wall) but
"build the next rocket" — and the Neutron-era business is the on-ramp that
makes the next rocket fundable.

## Sharpened thesis statement (Rev 6)

> **Rocket Lab can build an orbital inference data center on Neutron, no law of
> physics prevents it, and the economics close at a plausible premium — but the
> upside is honestly bounded: on Neutron this venture tops out at ~$5–10B/yr of
> revenue.** The two moonshot stress tests settle the top of the ladder:
> $50B/yr is infeasible on Neutron (~5,000 nodes, ~1,000–1,300 launches/yr ≈
> ~6–8× the all-time launch record, ~$150–250B of capital) and $150B/yr is
> infeasible by a ~15–20× margin. The wall is **launch cadence**, and it is
> structural — 1 rack per node, 1 node per launch chains the launch count to
> the revenue target, so cadence cannot be engineered down. The ~$5B ambition
> case is therefore *approximately the ceiling*, not a rung below it. That
> ceiling is a real, substantial business — it more than doubles Rocket Lab and
> would be its first major profit pool — but it is honestly **not** a $50–150B
> company-redefining line. The moonshot infeasibility is a hard wall, but **not
> a dead end**: the genuine path past ~$10B is a **bigger rocket** — a
> Neutron-successor heavy-lift vehicle carrying 10–60 racks per launch, which
> breaks the one-rack-per-launch chain. The $50B+ tier and that rocket are the
> *same bet*. So the venture is best understood as a **two-vehicle, two-decade
> arc**: Act I — V1 and the ambition case on Neutron — proves the orbital model,
> builds the customer base, and earns the profit and the right to build the
> bigger rocket; Act II — the Neutron successor — is what unlocks the
> company-redefining tier. The verdict is unchanged in kind — **fund the
> bounded build-to-learn program toward an honest go/no-go gate** — but the
> gate now opens onto a ~$5–10B Neutron-era business that is itself the on-ramp
> to the bigger-rocket moonshot, not a substitute for it.

**Carried forward unchanged from Rev 5:** no physics wall; whole intact racks
as the Starcloud differentiator; 1 rack/node, 1 node/launch; dawn-dusk SSO;
hubs-not-homes (≥4 diverse modest-aperture optical ground stations); a modest
RF sliver alongside optical primary; the ~$10–20M RL-internal launch cost;
V2 closing on baseline Neutron + hot-loop with the block-upgrade demoted to
margin upside; the 5-year GPU service-life base case; the gated build-to-learn
ramp with a ~3–5-node minimum viable deployment; in-house radiator ownership;
the conservative + ambition dual framing; **buildout-limited, not
demand-limited**; **~$15–20B/GW-yr gross IaaS (~$8M/rack-yr)** and
**~$25–50B/GW-yr gross inference-service (~$16M/rack-yr)** as the revenue
figures.

---

## Revision 7 — 2026-05-25 (repository boundary alignment)

This revision changes the repository contract, not the technical thesis.
Earlier revisions refer to `CONCLUSION.md` because, at the time, the generated
conclusion lived beside the research corpus and was treated as the live
deliverable. That is no longer the clean structure.

The research folder is now the evidence base only: source research, synthesis,
lint passes, debate, peer review, strategy, and this append-only thesis. It does
not own model-run summaries, current-state handoffs, model JSON, or code
outputs. Data-center artifacts live under `data_center/`: the default
machine-readable space model is `data_center/models/space/default.json`, the
default ground reference is `data_center/models/ground/default.json`, and the
default human-readable conclusion is `data_center/conclusion.md`.

Historical references to `CONCLUSION.md` in Revisions 1-6 are therefore not
live navigation instructions. They are citations to the retired model-run
summary artifact that carried the state of the project at that point in the
research history. New conclusions should state which model output they are based
on, with the default conclusion based on the default promoted model.

The thesis remains append-only. The live evidence trail for research readers is:
check [SOURCE_INDEX.md](../SOURCE_INDEX.md) for hard-number source status, read
the source documents, then synthesis/lint history, then this versioned thesis.
Read model-run summaries as model-linked outputs, not as research primary
sources.
