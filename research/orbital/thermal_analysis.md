# Thermal & Power Analysis — Orbital AI Data Center

*Doc 7 of foundational research (companion to Doc 6, `orbits_environment.md`). Status: stale / historical. Date: 2026-05-17.*

> **Source status (2026-05-25):** See [SOURCE_INDEX.md](../SOURCE_INDEX.md) claim IDs THR-001, THR-003 through THR-005, and THR-011 through THR-012. The vacuum/radiation physics is source-certified. The radiator areas, radiator masses, and rack-per-launch conclusions are model-derived and should be read with the later node mass model and source ledger.

## Summary / Verdict

**Thermal is not a hard physics wall — it is a sizing-and-mass problem, and a
solvable one — provided the design commits to two things: (1) running the coolant
loop hot (~60-90 °C, which AI silicon tolerates) and (2) holding radiators edge-on
to the Sun.**

The earlier research pass estimated ~370-540 m² of radiator per ~130-155 kW rack.
That estimate **assumed near-room-temperature radiators**. Running the radiator hot
exploits the T⁴ term in Stefan-Boltzmann and **cuts the area roughly in half**:

| Radiator temp | 2-sided net flux | Area for 130 kW | Area for 155 kW |
|---|---|---|---|
| ~27 °C (300 K) | ~400 W/m² | ~325 m² | ~390 m² |
| ~47 °C (320 K) | ~630 W/m² | ~205 m² | ~245 m² |
| ~67 °C (340 K) | ~910 W/m² | ~145 m² | ~170 m² |
| ~87 °C (360 K) | ~1240 W/m² | ~105 m² | ~125 m² |

So a one-rack node realistically needs **~120-210 m²** of radiator (double-sided),
not 370-540 m². At a modern deployable areal density of ~3-5 kg/m², that is
**~0.5-1.5 t of radiator per rack** — meaningful but not catastrophic.

> **Cross-reference (2026-05-17):** the wave-3 `node_design/node_mass_model.md`
> derives a higher figure (~375-500 m²/rack) under more conservative
> radiator-temperature and second-face assumptions. The two are reconciled in
> `synthesis/lint_report.md` §1.1, which adopts a **~200-430 m²/rack project
> range (working ~300 m²)** pending a chip→coolant→panel thermal model. This
> doc's analysis is unchanged; the "~120-210 m²" here is the optimistic bound.

**Racks per Neutron launch to SSO — SUPERSEDED.** This doc's wave-1 estimate of
"~2 racks/launch (a well-found 2-rack node)" is **no longer the project
position.** The wave-3 node mass model (`node_design/node_mass_model.md`) and
the re-run fairing-packing simulation (`simulations/REPORT.md`) settle a 1-rack
node at ~5.4–8.6 t and a 2-rack node at ~9.6–16.6 t — which exceeds even the
expendable budget. **The settled architecture is 1 rack per node, 1 node per
Neutron launch.** Read the "~2 racks" / "1–2 racks" / "3 racks aggressive"
figures throughout §5 below as a superseded wave-1 estimate; see
`synthesis/lint_report.md` §1.3–§1.4.

> Bottom line: heat rejection is the **dominant mass and deployment-complexity
> driver**, but it scales, and hot-loop operation plus edge-on geometry keep it
> inside Neutron's SSO budget. Thermal does **not** veto the concept; it sets the
> rack-per-launch count and therefore the economics.

---

## 1. Heat Rejection in Vacuum — the Physics

On Earth, data centers dump heat by **convection** (air, then water, then a chiller
and a cooling tower) — moving thousands to tens of thousands of W/m². In orbit there
is **no air and no working fluid to convect into**: the *only* exit for heat is
**thermal radiation** to deep space. This is the entire thermal problem in one
sentence.

### Stefan-Boltzmann
A radiator emits:

> **P = ε · σ · A · (T_rad⁴ − T_sink⁴)**

- σ = 5.67×10⁻⁸ W/m²K⁴ (Stefan-Boltzmann constant)
- ε = surface emissivity (~0.85 for good radiator coatings)
- A = radiating area; T_rad = radiator temperature; T_sink = effective environment temperature
- A panel exposed to space on **both faces radiates from both** → multiply by ~2.

The **T⁴** term is the key lever: pushing the radiator hotter raises rejection per
m² steeply, so the choice of coolant/radiator temperature dominates required area.

### The temperature opportunity
Terrestrial servers are kept cool for longevity, but **AI accelerators tolerate hot
operation** — GPU junctions routinely run 90-110 °C and direct-liquid-cooling loops
commonly run **~45-70 °C coolant**, with hotter loops feasible. A hotter loop means
a hotter radiator, which **radiates far more per m²**. This is the single biggest
design knob.

### Worked area calculations
Assumptions: ε = 0.85, **double-sided** panels, effective sink T_sink ≈ 250 K
(a realistic LEO average once Earth IR + albedo + residual solar are folded in for an
edge-on radiator — see §2; deep space alone is ~3 K but Earth is warm and close).
Net 2-sided flux q = 2 · ε · σ · (T_rad⁴ − 250⁴).

| T_rad | (loop temp) | q, net 2-sided | Area, 130 kW | Area, 155 kW |
|---|---|---|---|---|
| 300 K | ~27 °C | ~404 W/m² | **322 m²** | **384 m²** |
| 320 K | ~47 °C | ~634 W/m² | **205 m²** | **245 m²** |
| 340 K | ~67 °C | ~912 W/m² | **143 m²** | **170 m²** |
| 360 K | ~87 °C | ~1242 W/m² | **105 m²** | **125 m²** |

**Sensitivity:** going from a 27 °C radiator to an 87 °C radiator **triples** the
flux and **cuts area to ~1/3**. Going from 27 °C to a moderate 67 °C roughly
**halves** it. The radiator temperature is set by the hottest the chips' coolant
loop can run minus thermal gradients through the loop/heat-pipe/panel; a realistic
**design target is a ~60-80 °C radiator (~330-355 K)**, giving **~120-210 m² per
130-155 kW rack**.

This reconciles with the prior 370-540 m² estimate: that figure implicitly assumed
a cool (~room-temperature, possibly single-sided) radiator. **The physics rewards
running hot**, and AI silicon permits it.

### Benchmark — the ISS
The ISS External Active Thermal Control System rejects **~70 kW** using **~420 m²**
of deployed ammonia-loop radiator (≈166 W/m² effective), and the full radiator
complement is **~10 t including rotary joints and plumbing**
([NASA — ISS ATCS Overview](https://www.nasa.gov/wp-content/uploads/2021/02/473486main_iss_atcs_overview.pdf);
[Grokipedia — External Active Thermal Control System](https://grokipedia.com/page/External_Active_Thermal_Control_System)).
The ISS runs **cool** radiators (~3-7 °C loop) — which is exactly why it gets only
~166 W/m². An AI node running a hot loop **beats ISS per-m² rejection by 3-7×**, the
single most important reason the orbital-DC thermal numbers are not as dire as the
ISS comparison first suggests.

---

## 2. Orbital Thermal Environment — Sink Temperature & Orientation

"Space is cold" is misleading. The radiator does not see 3 K deep space alone; it
also sees **three heat inputs** that raise its effective sink temperature:

- **Direct solar flux:** ~**1361 W/m²** (the solar constant). A radiator face-on to
  the Sun absorbs a large fraction of this; even a low-absorptivity coating
  (α ≈ 0.15-0.2) still picks up **~200-270 W/m²** of solar load — that is *most of*
  what a room-temperature panel can radiate.
- **Earth albedo:** ~**30%** of sunlight reflected off Earth, ~**400 W/m²** at the
  sub-solar point, falling with the Earth view factor — significant for a radiator
  pointed Earthward.
- **Earth infrared (IR):** Earth radiates ~**240 W/m²** as a ~255 K body; a radiator
  facing Earth absorbs a large share of this and cannot radiate below it.

**Consequence — orientation is everything.** The ISS solution, which an orbital DC
must copy, is to keep radiators **edge-on to the Sun** (projected solar area ≈ 0) and
ideally **facing deep space / away from Earth's limb**. A radiator edge-on to the Sun
and viewing cold sky has an effective sink of only ~**4-30 K** for the radiative term
— but in practice Earth IR + albedo + spacecraft self-view push the *usable* sink to
roughly **220-260 K**; this doc uses **250 K**, which is why the §1 fluxes are
conservative-realistic rather than idealized.

**Why dawn-dusk SSO helps thermally (link to `orbits_environment.md`):**
- The Sun direction is nearly fixed relative to the orbit plane, so radiators can be
  held **permanently edge-on** with a simple, slow rotary joint instead of
  continuous full re-pointing.
- Near-continuous sunlight means a **steady thermal state** — no 100-minute
  hot/cold cycling — which is easier on structures and on loop control.
- Trade-off: in continuous sun there is never an eclipse "cool-down," so the
  radiator must be sized for **steady-state full power**, not an orbit average. The
  §1 areas already assume steady-state, so this is accounted for.

A practical node carries **deployable radiator wings held edge-on to the Sun**, with
the compute box and solar array arranged so the radiators view cold sky, not each
other or the array.

---

## 3. Radiator Mass

### Areal density
Survey of deployable spacecraft radiators
([NASA TP-1998-207427 — Lightweight Space Radiators](https://ntrs.nasa.gov/api/citations/19980236936/downloads/19980236936.pdf);
[Aerospace Corp — Small Satellite Deployable Radiator Study, 2024](http://www.mstl.atl.calpoly.edu/~workshop/archive/2024/presentations/2024_Day1_Session3_Madison.pdf);
[ToughSF — All the Radiators](http://toughsf.blogspot.com/2017/07/all-radiators.html)):

| Class | Areal density |
|---|---|
| Heavy deployable + support structure | ~12 kg/m² |
| ISS-class radiator (panels + structure) | ~8 kg/m² (~2.75 kg/m² panels only) |
| Conventional metal heat-pipe radiators | ~5-10 kg/m² |
| Carbon-carbon / advanced composite | ~2-2.2 kg/m² |
| Best demonstrated deployable | ~1.9 kg/m² (3.9 kg/m² counting planform) |
| NASA stated target | ~2 kg/m² |

This doc uses a **working range of 3-5 kg/m²** (modern deployable composite/heat-pipe
panel including plumbing and deployment structure) — credible for a 2026-era build,
with ~2-3 kg/m² as an optimistic future case and ~8 kg/m² (ISS-like) as pessimistic.

### Radiator mass per node
Using §1 areas at a **~67 °C radiator** (mid-case: 143 m²/rack at 130 kW,
170 m²/rack at 155 kW) and **4 kg/m²**:

| Node | Radiator area | Radiator mass @4 kg/m² | Range (2-8 kg/m²) |
|---|---|---|---|
| 1 rack, 130 kW | ~145 m² | **~0.6 t** | ~0.3-1.2 t |
| 1 rack, 155 kW | ~170 m² | **~0.7 t** | ~0.3-1.4 t |
| 2 rack, ~290 kW | ~290 m² | **~1.2 t** | ~0.6-2.3 t |
| 2 rack, ~310 kW | ~340 m² | **~1.4 t** | ~0.7-2.7 t |

If the design is forced to run **cool** radiators (~27 °C, the §1 worst case), areas
roughly double and radiator mass climbs to **~1.3-1.5 t per rack** at 4 kg/m². That
is the penalty for *not* committing to a hot loop — still not mission-ending, but it
directly costs racks-per-launch. **Conclusion: radiator mass is ~0.5-1.5 t per rack
in the realistic design space — comparable to the compute hardware itself, and the
second-biggest mass line after the bus.**

---

## 4. Solar Power

### Power requirement
Treating each rack's IT load (~130-155 kW) as needing matching electrical input,
plus housekeeping/comms/thermal-pump overhead (~15-20%), continuous generation
needed is roughly:

- 1 rack: **~150-185 kW**
- 2 racks: **~300-370 kW**

Dawn-dusk SSO means this is needed **~95-100% of the orbit** (no large array
oversizing for eclipse recharge — see `orbits_environment.md`).

### Array area
At ~1361 W/m² solar flux, ~30% cell+system efficiency, and normal incidence (dawn-
dusk geometry keeps the array near sun-pointing): net **~400 W/m²** of array.
- ~150-185 kW → **~375-460 m²** of array.
- ~300-370 kW → **~750-925 m²** of array.

### Array mass
Modern flexible roll-out arrays (ROSA-class) achieve **~200-500 W/kg at the wing
level** ([Redwire — Roll Out Solar Array](https://redwirespace.com/products/rosa/);
[Wikipedia — Roll Out Solar Array](https://en.wikipedia.org/wiki/Roll_Out_Solar_Array)).
Using a conservative **~150 W/kg at full system level** (wing + deployment +
harness + drive):
- ~150-185 kW → **~1.0-1.2 t** of array.
- ~300-370 kW → **~2.0-2.5 t** of array.
At an optimistic 300 W/kg these halve (~0.5-0.6 t and ~1.0-1.2 t).

### Rocket Lab's Feb 2026 solar array announcement
On **26 Feb 2026** Rocket Lab announced **advanced silicon solar arrays explicitly
for gigawatt-scale space-based data centers** — "mass-manufacturable, lightweight,
modular," using **radiation-hardened silicon** cells (deliberately avoiding scarce
gallium-arsenide/germanium) to drive **low cost per watt at industrial scale**
([Rocket Lab press release](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/);
[GlobeNewswire](https://www.globenewswire.com/news-release/2026/02/26/3246118/0/en/Rocket-Lab-Introduces-Advanced-Silicon-Solar-Arrays-To-Power-Space-Based-Data-Centers.html)).
**No public W/kg, $/W, or W/m² figures were released** — the announcement is
strategic positioning, not a spec sheet. Two reads for this project: (1) RL is
explicitly building the power subsystem this concept needs, strengthening the
"RL as power + bus + launch prime" thesis; (2) silicon (vs. triple-junction GaAs)
is **lower efficiency (~22-24% vs ~30%)** — likely **more array area and somewhat
more mass per kW** than the ROSA-class figures above, traded for cost and
manufacturability. Treat the §4 mass/area numbers as the *efficient* end; an
all-silicon array could be ~25-40% larger in area.

---

## 5. Verdict & Per-Launch Budget

### Is thermal a hard wall?
**No.** Heat rejection in vacuum is purely radiative and that is genuinely
restrictive *per square meter* — but it **scales linearly with area**, and the T⁴
law means **running the loop hot (which AI silicon allows) buys back most of the
area**. There is no physical effect that forbids the design; there is only a mass
and deployment-complexity bill. The wall is **economic/logistical** (how much
radiator + array mass you can afford to launch and deploy per rack), not physical.

The honest caveats: (a) **deploying 150-300 m² of radiator + 400-900 m² of array per
node** is a serious mechanical-deployment challenge; (b) at **gigawatt** scale the
radiator area becomes enormous (~800,000+ m² for 600 MW of waste heat per third-party
analysis) — but a **single-node, 1-3 rack** scale is firmly tractable.

### Per-launch mass budget sketch (one node, mid-case assumptions)

> **Superseded (wave-5, 2026-05-17):** the ~10 t Neutron SSO budget used in this
> section — and the "1–2 racks/launch" it feeds — is superseded. The current SSO
> working figure is **~9.5 t reusable (range 8.5–10.5 t)** and the architecture
> is settled at **1 rack/node, 1 node/launch** — see
> `rocket_lab/neutron/payload_and_block_upgrade.md` and `node_design/node_mass_model.md`.
> This doc's thermal/area analysis is unchanged.

Working assumptions: 155 kW/rack; ~67 °C radiator (170 m²/rack, 4 kg/m²); efficient
ROSA-class array at ~150 W/kg; dawn-dusk SSO so **batteries are minimal** (eclipse-
season ride-through only, or accept compute throttling); Neutron SSO budget ≈ **10 t**.

| Mass line | 1-rack node | 2-rack node |
|---|---|---|
| Compute rack(s) (NVL-class, ~1.4 t each incl. enclosure) | ~1.4 t | ~2.8 t |
| Radiator (170 m²/rack @4 kg/m²) | ~0.7 t | ~1.4 t |
| Solar array (~185 / ~370 kW @150 W/kg) | ~1.2 t | ~2.5 t |
| Batteries (dawn-dusk: small) | ~0.2 t | ~0.4 t |
| Bus: structure, avionics, ADCS, propulsion+propellant, comms, thermal loop/pumps | ~1.5 t | ~2.3 t |
| Subtotal | ~5.0 t | ~9.4 t |
| Margin (~20%) | ~1.0 t | ~1.9 t |
| **Node total** | **~6.0 t** | **~11.3 t** |

**Read against ~10 t Neutron SSO:**
- A **1-rack node (~6 t)** fits a single Neutron flight comfortably, with spare margin.
- A **2-rack node (~11.3 t)** slightly **exceeds** the ~10 t reusable SSO estimate at
  mid-case assumptions — it fits if (a) the launch is **expendable** (~11-12.5 t SSO),
  (b) radiators run hotter (~80-87 °C → ~125 m²/rack, lighter), (c) lighter
  ~2-3 kg/m² radiators and higher-W/kg arrays are used, or (d) margin is trimmed.

### Racks per Neutron launch to SSO — SUPERSEDED

> **Superseded conclusion (wave-3 / wave-5).** This wave-1 doc originally
> carried "**~2 racks/launch**" as its working number. **That is no longer the
> project position.** The wave-3 node mass model and the re-run fairing-packing
> simulation both find a 2-rack node (~9.6–16.6 t) blows even the expendable
> budget, and the settled architecture is **1 rack per node, 1 node per Neutron
> launch**. The original wave-1 reasoning is left below for the record only —
> read it as superseded, not as a working number.

*Superseded wave-1 estimate (do not use as a planning figure):*
- *Conservative:* 1 rack/launch (cool radiators, heavy panels, generous margin, reusable).
- *Earlier "working" estimate:* ~2 racks/launch — a 2-rack node on an expendable
  flight, or on a reusable flight with hot radiators + lightweight panels.
  **This estimate is superseded — the project carries 1 rack/launch.**
- *Aggressive:* 3 racks/launch — superseded; a multi-rack node is not flown.

So the practical planning figure is **1-2 racks per Neutron launch**, with thermal
and power hardware — not the GPUs — consuming **roughly half the payload mass**.

### Where this leaves the feasibility question
Thermal/power is a **sizing and mass-budget problem, decisively not a physics wall**,
*at the 1-3 rack node scale this project targets*. The design rules that make it
close: **run the coolant loop hot, hold radiators edge-on to the Sun, fly dawn-dusk
SSO to shed battery mass, and use lightweight deployable radiators and arrays.** The
binding constraint remains **kg to SSO per launch** (consistent with the project's
earlier finding), and the leading mass consumers per rack are, in order: **solar
array ≈ bus > radiator > compute hardware**.

---

## Sources

- [NASA — ISS Active Thermal Control System Overview](https://www.nasa.gov/wp-content/uploads/2021/02/473486main_iss_atcs_overview.pdf)
- [Grokipedia — External Active Thermal Control System](https://grokipedia.com/page/External_Active_Thermal_Control_System)
- [NASA TP-1998-207427 — Design Considerations for Lightweight Space Radiators](https://ntrs.nasa.gov/api/citations/19980236936/downloads/19980236936.pdf)
- [Aerospace Corporation — Small Satellite Deployable Radiator Study (2024)](http://www.mstl.atl.calpoly.edu/~workshop/archive/2024/presentations/2024_Day1_Session3_Madison.pdf)
- [ToughSF — All the Radiators](http://toughsf.blogspot.com/2017/07/all-radiators.html)
- [The Thermal Problem of Space Data Centers — Order-of-Magnitude Analysis](https://yage.ai/share/space-datacenter-thermal-en-20260421.html)
- [Per Aspera — Realities of Space-Based Compute](https://www.peraspera.us/realities-of-space-based-compute/)
- [SpaceComputer — Cooling for Orbital Compute: A Landscape Analysis](https://blog.spacecomputer.io/cooling-for-orbital-compute/)
- [Redwire — Roll Out Solar Array (ROSA)](https://redwirespace.com/products/rosa/)
- [Wikipedia — Roll Out Solar Array](https://en.wikipedia.org/wiki/Roll_Out_Solar_Array)
- [Rocket Lab — Advanced Silicon Solar Arrays for Space-Based Data Centers (press release)](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/)
- [GlobeNewswire — Rocket Lab Silicon Solar Arrays announcement (26 Feb 2026)](https://www.globenewswire.com/news-release/2026/02/26/3246118/0/en/Rocket-Lab-Introduces-Advanced-Silicon-Solar-Arrays-To-Power-Space-Based-Data-Centers.html)

## Open Questions / Uncertainties

- **Radiator temperature is the master variable** and depends on the real
  chip→coolant→heat-pipe→panel gradient. The 60-80 °C radiator assumed here needs a
  proper thermal-resistance model; if gradients are large, the radiator runs cooler
  and areas grow toward the §1 worst case.
- **Effective sink temperature (250 K used here)** is an engineering estimate;
  detailed view-factor modeling for the actual node geometry (radiator vs. Earth
  limb vs. array vs. self) could shift fluxes ±20%.
- **Compute-rack mass (~1.4 t)** is an engineering estimate for an NVL-class rack
  with space enclosure; cross-check against
  [ai_hardware.md](../ai_hardware/ai_hardware.md).
- **Rocket Lab silicon array specs are unpublished** — W/kg, W/m², $/W, efficiency,
  radiation-degradation rate all unknown. Array mass/area could be materially worse
  (silicon vs. GaAs) than the ROSA-class figures used.
- **Deployment mechanics** of 150-300 m² of radiator + 400-900 m² of array from one
  Neutron fairing is unmodeled here — likely a real volume/packaging constraint, not
  just a mass one. Ties to the open "usable fairing volume" question.
- **No official Neutron SSO payload** — the ~10 t budget is inherited from
  `orbits_environment.md` and is itself an estimate.
- **Pumped-loop and heat-pipe mass** (moving 130-155 kW from rack to radiator) is
  folded into the bus line crudely; a dedicated fluid-loop mass estimate is needed.
- **Eclipse-season transient:** during the dawn-dusk eclipse season the node loses
  power for up to ~20 min/orbit — battery vs. compute-throttling trade is unresolved
  and affects the battery mass line.
