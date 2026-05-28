# Solar Arrays & Deployable Radiators — Cost, Mass & Technology Trajectory

*Project: RKLB Space Data Center — feasibility phase. Document date: May 2026.*
*Author: research agent. Scope: the two subsystems that scale with rack power — space solar arrays and deployable radiators. All hard numbers cross-checked against ≥2 sources where possible; estimates explicitly flagged.*

---

> **Source status (2026-05-25):** See [SOURCE_INDEX.md](../SOURCE_INDEX.md) claim IDs THR-002, THR-006, and THR-007. The solar constant and general deployed-array technology context are source-certified. Solar/radiator areas and masses are model-derived. Rocket Lab has announced silicon arrays for space data centers, but public materials do not yet publish the W/kg, W/m2, or $/W values needed to certify this model's silicon-array assumptions.

## Summary

This document characterizes the **cost, mass, and technology trajectory** of the two power-scaling subsystems for an orbital AI-inference node: the **solar array** and the **deployable radiator**. It then models how each scales as rack power rises from today's ~130 kW to a projected ~600 kW.

**Headline scaling result (per rack, mid technology assumptions):**

| Rack power | Solar area | Solar mass | Radiator area | Radiator mass | **Solar+radiator mass (mid)** |
|---|---|---|---|---|---|
| **130 kW** | ~470 m² | ~1.3 t | ~370 m² | ~1.9 t | **~3.2 t** |
| **300 kW** | ~1,090 m² | ~3.0 t | ~860 m² | ~4.3 t | **~7.3 t** |
| **600 kW** | ~2,180 m² | ~6.0 t | ~1,710 m² | ~8.6 t | **~14.6 t** |

(GaAs-ROSA-class array at ~155 W/kg, deployable radiator at ~5 kg/m². Arithmetic in §4. A conservative/silicon technology path roughly **doubles** these masses; an advanced path cuts them ~30–40%.)

> **Radiator-area bracket (project reconciliation, 2026-05-17).** The radiator
> areas in this table are **single-point** estimates (350 W/m², ~40–50 °C
> surface): ~370 m² at 130 kW. The project has since adopted a wider
> **~200–430 m²/rack range with ~300 m²/rack as the working planning number**
> (`synthesis/lint_report.md` §1.1) — the spread reflects unsettled radiator
> surface-temperature and second-face assumptions, pending a
> chip→coolant→panel thermal model. A hot-loop design (~70–80 °C surface) sizes
> nearer the low end; this table's ~370 m² sits mid-band. The *scaling
> conclusion* (mass wall at 300–600 kW) is robust to where in the bracket the
> real number lands; the specific per-row areas are point estimates, not the
> project's settled figure.

**Cost vs. mass verdict.** The founder's two gut calls are **both essentially correct, and the picture sharpens with power density:**

- **At 130 kW, solar+radiator is a manageable mass item (~3 t) and a real-but-secondary cost item.** Cost is not the binding constraint at any power level for a company that builds its own arrays.
- **At 300–600 kW, solar+radiator becomes overwhelmingly a MASS problem.** At 600 kW the two subsystems alone are **~14–15 t mid / up to ~25 t conservative** — they *blow the entire Neutron payload budget* (8.5 t reusable, 13 t downrange, 15 t expendable) by themselves, before the rack, bus, or propellant. Mass — specifically **areal density of the radiator and specific power of the array** — is the constraint that decides whether high-power-density racks can fly at all.
- **Cost scales linearly and benignly; mass scales linearly and catastrophically against a hard launch ceiling.** As rack power density rises, this shifts from "mostly fine" toward "mass-wall." See §7.

**Rocket Lab "N" acquisition.** The founder's recollection of a recent Rocket Lab acquisition starting with "N", relevant to collapsing/expanding structures, **does not check out as stated.** Rocket Lab's only "N"-initial acquisition is **Mynaric** (laser comms, April 2026) — explicitly excluded by the founder and not a structures company. No Rocket Lab acquisition of a deployable-structures / collapsing-expanding-structures company beginning with "N" exists as of May 2026. The relevant *real* capabilities are **SolAero** (2022 — space solar cells, panels, *and composite/precision aerospace structures*) and **Motiv Space Systems** (announced May 2026 — robotics, actuators, precision deployment mechanisms). See §6.

**Confidence: medium.** Areal-mass and specific-power figures for arrays and radiators are well-sourced (medium-high). The forward trajectory and the cost figures are estimate-heavy (manufacturers do not publish $/W for integrated arrays). The 300/600 kW scaling is arithmetic on stated assumptions — robust as a *model*, but the input technology assumptions carry the uncertainty.

---

## 1. Space solar arrays — current best (2026)

Solar flux in Earth orbit is **~1,361 W/m²** (the solar constant) and is **constant** — Earth's orbit is near-circular, so distance from the Sun is **not a design variable**. The only levers on solar mass and area are **cell efficiency** and **areal density** (kg/m² of blanket + structure). ([NASA Small Spacecraft SoA — Power, 2024](https://www.nasa.gov/wp-content/uploads/2025/02/3-soa-power-2024.pdf))

### 1.1 The three array classes

| Array class | Specific power (W/kg) | Areal mass (kg/m²) | Cell efficiency (BOL, AM0) | Notes |
|---|---|---|---|---|
| **Legacy rigid panel (GaAs on honeycomb)** | ~25–70 W/kg | ~2.5–7 kg/m² (panel) | ~28–30% | ISS-era silicon rigid arrays ~28 W/kg; modern rigid GaAs panels ~50–70 W/kg. The state-of-*practice*: flown missions cluster near **~30 W/kg**. ([NASA SoA Power](https://www.nasa.gov/wp-content/uploads/2025/02/3-soa-power-2024.pdf), [NASA SoA Power subsystems page](https://www.nasa.gov/smallsat-institute/sst-soa/power-subsystems/)) |
| **ROSA-class roll-out (flexible blanket, GaAs)** | **~100–120 W/kg typical; up to ~200–225 W/kg** advanced | ~1.5–3 kg/m² (blanket+structure) | ~30–32% | Redwire ROSA: stated **100–120 W/kg**, ~4.4 kg/kW; **3× the specific power, 6× the stowed power density, and ~25% lower cost** vs. rigid arrays. 60 kW ROSA wings tested in 2025 for the lunar Gateway. ([Wikipedia: ROSA](https://en.wikipedia.org/wiki/Roll_Out_Solar_Array), [Redwire ROSA flysheet](https://rdw.com/wp-content/uploads/2023/06/redwire-roll-out-solar-array-flysheet.pdf), [pv-magazine: 60 kW ROSA, Jul 2025](https://pv-magazine-usa.com/2025/07/03/redwire-deploys-60-kw-roll-out-solar-array-for-the-first-lunar-orbit-space-station/)) |
| **Newer silicon space arrays** | est. ~70–110 W/kg (unpublished) | est. ~1.5–3 kg/m² | ~18–22% | Terrestrial-derived, mass-manufacturable silicon. Lower efficiency → ~1.4–1.6× the area of GaAs for equal power. No Ga/Ge → supply-chain-resilient and cheaper per watt. ([Tech Briefs: Si vs GaAs](https://www.techbriefs.com/component/content/article/18946-silicon-vs-gallium-arsenide-which-photovoltaic-material-performs-best)) |

> **Empirical envelope (independent cross-check):** A 2025 survey of flown missions finds space solar arrays "strongly clustered around ~30 W/kg," with the **maximum empirical specific power in the dataset at 200 W/kg** — i.e. ROSA-class advanced arrays define the current ceiling of *flight-proven* hardware. ([ScienceDirect, flexible/high-specific-power PV survey, 2025](https://www.sciencedirect.com/science/article/abs/pii/S2542435125003757))

### 1.2 Rocket Lab's February 2026 silicon arrays for space data centers

On **26 Feb 2026** Rocket Lab announced **advanced silicon solar arrays explicitly aimed at gigawatt-scale space-based data centers** ([Rocket Lab press release](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/); [GlobeNewswire mirror](https://www.globenewswire.com/news-release/2026/02/26/3246118/0/en/Rocket-Lab-Introduces-Advanced-Silicon-Solar-Arrays-To-Power-Space-Based-Data-Centers.html)):

- Described as **modular, lightweight, radiation-hardened silicon modules**, "mass-manufacturable" and delivering **low cost per watt at industrial scale**.
- The explicit pitch is **scaling economically to gigawatt-class orbital power** — i.e. supply-chain resilience and $/W, *not* peak specific power. Silicon avoids the gallium/germanium critical-minerals bottleneck.
- A **hybrid option** mixes silicon with high-efficiency (GaAs) cells.
- Backed by a **$23.9M CHIPS award** to expand semiconductor production in Albuquerque (the former SolAero site).
- **Specific power and efficiency are NOT published.** (FLAG — estimate.) Given ~18–22% silicon efficiency vs. ~30% GaAs, the silicon array needs **~1.4–1.6× the area** for equal power. Per-cell the silicon blanket can be lighter (no germanium substrate), but the larger blanket + longer booms + bigger deployment structure largely offset that. Working assumption: **silicon-array specific power ~70–110 W/kg**, i.e. **~25–40% below advanced GaAs ROSA** — until Rocket Lab publishes otherwise.

**Strategic read:** Rocket Lab is *deliberately* trading array efficiency for cost and manufacturability. This is a tell: it confirms that for a fleet of these nodes, **cost/manufacturability is the lever Rocket Lab is optimizing — but it does so by accepting more area and more mass.** That trade is only safe if mass is *not* the binding constraint. As §4 shows, at high rack power it **is** the binding constraint — so the silicon array is the right call for 130 kW nodes and a risky one for 600 kW nodes unless paired with the hybrid/GaAs option.

---

## 2. Solar trajectory — past ~15 years and forward

| Era | Representative tech | Specific power | Cell efficiency |
|---|---|---|---|
| ~2000–2010 | ISS rigid silicon blanket arrays | **~28 W/kg** | ~14% |
| ~2010–2015 | Rigid GaAs honeycomb panels | ~40–70 W/kg | ~28–30% |
| ~2017–2025 | ROSA roll-out (ISS ROSA flew 2017; iROSA on ISS 2021–2023) | **~100–120 W/kg**, advanced units to ~200 W/kg | ~30–32% |
| ~2026 | Rocket Lab silicon / hybrid arrays; Redwire ELSA | est. ~70–110 W/kg silicon; ELSA targets **+50% stowed power density** vs. ROSA | ~18–22% Si / ~32% GaAs |
| ~2030+ (projected) | Advanced multi-junction (32–34%+), thin-film, perovskite-on-flexible | plausibly ~250–350 W/kg flight; lab IMM/perovskite higher | ~34%+ MJ; perovskite-tandem experimental |

**What improved:** Specific power rose **~4–7×** in 15 years (28 → ~120–200 W/kg), driven *almost entirely by structure*, not cells. Cell efficiency rose only ~14% → ~32% (~2.3×) and is **approaching diminishing returns** — even at the ~68% triple-junction theoretical limit, the area/mass/volume savings are bounded ([NASA SoA Power](https://www.nasa.gov/wp-content/uploads/2025/02/3-soa-power-2024.pdf)). The dominant gain came from **eliminating the rigid honeycomb substrate** (roll-out flexible blankets + composite booms). Stowed power density improved ~6× with ROSA and a further ~50% with Redwire's 2025 **ELSA** ([Redwire ELSA announcement](https://rdw.com/newsroom/redwire-announces-new-high-performance-low-mass-solar-array-building-upon-the-success-of-its-roll-out-solar-array-product-line/)).

**Cost trajectory:** ROSA claims **~25–50% lower cost than rigid arrays** depending on blanket/PV tech ([ROSA on Wikipedia](https://en.wikipedia.org/wiki/Roll_Out_Solar_Array); [NTRS ROSA cost discussion](https://ntrs.nasa.gov/citations/20130008777)). Rocket Lab's silicon array is explicitly a **cost-down** play. Direction of travel: **cost per watt is falling**; specific power is rising but with cells near a ceiling, future gains are mostly structural.

**Projection:** Expect flight-class specific power to reach **~200–300 W/kg by ~2030** and cost/W to keep falling as silicon and mass manufacturing scale. **The trajectory helps — but linearly, while rack power is projected to rise ~4.6× (130→600 kW). Technology improvement does not outrun the power-density growth.** (FLAG — projection, medium-low confidence.)

---

## 3. Deployable radiators — current best (2026)

A node must reject **~100% of rack electrical power as heat** (compute converts essentially all input power to heat). Radiator performance is governed by Stefan-Boltzmann: `Q/A = ε·σ·(T⁴ − T_sink⁴)`. Unlike solar, the radiator has **no flux constant** — performance is a steep function of surface temperature.

### 3.1 State of the art

| Parameter | Current value | Source / notes |
|---|---|---|
| **Heat rejection (planform)** | **~350 W/m² at ~300 K surface**; ~300–400 W/m² for well-designed panels; advanced/high-temp designs higher | [Aerospace Corp Small-Sat Deployable Radiator Study, 2024](http://www.mstl.atl.calpoly.edu/~workshop/archive/2024/presentations/2024_Day1_Session3_Madison.pdf); [NASA SoA Thermal 2024](https://www.nasa.gov/wp-content/uploads/2025/02/7-soa-thermal-2024.pdf) |
| **Areal mass — advanced lightweight panel** | **~3.0–3.1 kg/m²** (NASA target ≤3.0 kg/m²; "Ver. 6" panel achieved 3.08 kg/m²) | [ISNPS Advanced Lightweight Heat Rejection Radiators](https://isnps.unm.edu/reports/ISNPS_Tech_Report_103.pdf) |
| **Areal mass — fission-power radiators (state of practice)** | **~5.2–11.0 kg/m²** | [ISNPS report](https://isnps.unm.edu/reports/ISNPS_Tech_Report_103.pdf) |
| **Areal mass — deployable + structure + fluid loop (realistic system)** | **~3 kg/m² (low) – 5 (mid) – 8–12 (high)** including headers, pumped loop, deployment hardware | [Gilmore, Spacecraft Thermal Control Handbook ch.6](http://matthewwturner.com/uah/IPT2008_summer/baselines/LOW%20Files/Thermal/Spacecraft%20Thermal%20Control%20Handbook/06.pdf); [deployable radiator study, 409 W/m² planform / ~3.9 kg/m²](https://ui.adsabs.harvard.edu/abs/2021MsT..........6M/abstract) |
| **Deployable mechanism** | Loop heat pipes (LHP) standard for deployable panels; oscillating heat pipes (OHP) emerging | [NASA SoA Thermal 2024](https://www.nasa.gov/wp-content/uploads/2025/02/7-soa-thermal-2024.pdf); [ThermAvant OHP radiators](https://www.thermavant.com/thermavant-products/oscillating-heat-pipe-radiators) |
| **Cost** | **Not published** ($/m²); radiators are typically a small fraction of spacecraft cost vs. arrays and avionics | — (FLAG — no public $ figure) |

### 3.2 Radiator trajectory

Radiators have improved **far more slowly than solar arrays.** Heat-rejection-per-m² is near-fundamentally bounded by the T⁴ law and achievable loop temperature; the gains over 15 years are in **areal mass** (fission-class ~11 kg/m² → advanced ~3 kg/m²) and in **deployability** (LHP/OHP-based deployable panels, additive-manufactured integrated heat-pipe panels). The big future lever is **higher loop/surface temperature** — running the radiator hotter shrinks area as T⁴ — but that fights the chip-junction temperature limit. **Net: radiators are a slowly-improving, physics-bounded technology. They do not have solar's improvement runway.** This is why, as §4 shows, the radiator becomes the *heavier* of the two subsystems at every power level.

> **Key working assumptions for §4** (consistent with `node_mass_model.md` §4): effective radiator rejection **~350 W/m² planform** at a ~50 °C surface in LEO (sink ~250 K with Earth IR/albedo loading); areal mass **3 / 5 / 8 kg/m²** (low/mid/high) for a large pumped-loop deployable radiator.

---

## 4. Scaling with rack power — the core model

**Method.** For each rack power level, size the **solar array** to deliver rack load through the power chain, and the **radiator** to reject the rack heat. Then convert area → mass with the areal figures from §1–3. All arithmetic shown.

### 4.1 Fixed assumptions

| Quantity | Value | Basis |
|---|---|---|
| Power-chain efficiency (array output → rack input) | **0.86** | PMAD ×0.92, harness/regulation ×0.95, near-continuous-sun SSO battery ×0.98 (`node_mass_model.md` §3) |
| Sizing margin (degradation, off-point, EOL) | **×1.15** | feasibility-standard |
| Effective solar collection (GaAs, 30%, packing/cosine) | **~370 W/m²** | 1361 × 0.30 × ~0.90 |
| Effective solar collection (silicon, 20%) | **~245 W/m²** | 1361 × 0.20 × ~0.90 |
| GaAs ROSA specific power (mid) | **155 W/kg** | midpoint of 120 (conservative) and ~200 (advanced) |
| Silicon array specific power (mid) | **90 W/kg** | est., §1.2 |
| Heat to reject | **= rack power** (≈100% to heat) | compute thermodynamics |
| Radiator rejection | **~350 W/m² planform** | §3 |
| Radiator areal mass (low/mid/high) | **3 / 5 / 8 kg/m²** | §3 |

### 4.2 Solar array — area and mass

**Array electrical output needed** = rack power ÷ 0.86 × 1.15 = rack power **× 1.337**.

| Rack power | Array output (BOL) | **GaAs area** (÷370) | **GaAs mass** @155 W/kg | Silicon area (÷245) | Silicon mass @90 W/kg |
|---|---|---|---|---|---|
| 130 kW | 130 × 1.337 = **174 kW** | 174,000 ÷ 370 = **~470 m²** | 174,000 ÷ 155 = **~1.12 t** | ~710 m² | ~1.93 t |
| 300 kW | 300 × 1.337 = **401 kW** | **~1,084 m²** | **~2.59 t** | ~1,637 m² | ~4.46 t |
| 600 kW | 600 × 1.337 = **802 kW** | **~2,168 m²** | **~5.17 t** | ~3,273 m² | ~8.91 t |

> Adopted mid solar mass uses GaAs-ROSA-class (155 W/kg) with a small allowance toward the silicon case → **~1.3 / 3.0 / 6.0 t** at 130 / 300 / 600 kW. Conservative (silicon, 90 W/kg) ≈ **1.9 / 4.5 / 8.9 t**. Advanced (200 W/kg GaAs) ≈ **0.87 / 2.0 / 4.0 t**.

### 4.3 Radiator — area and mass

**Radiator area** = rack power ÷ 350 W/m². *(Single-point assumption. The
project-adopted radiator-area figure is a **~200–430 m²/rack range, working
~300 m²/rack** at the ~130–150 kW node scale — see the Summary bracket note and
`synthesis/lint_report.md` §1.1. The ~371 m² below sits mid-bracket; the mass
*scaling* result holds across the bracket.)*

| Rack power | **Radiator area** | Mass @3 kg/m² (low) | **Mass @5 kg/m² (mid)** | Mass @8 kg/m² (high) |
|---|---|---|---|---|
| 130 kW | 130,000 ÷ 350 = **~371 m²** | ~1.11 t | **~1.86 t** | ~2.97 t |
| 300 kW | 300,000 ÷ 350 = **~857 m²** | ~2.57 t | **~4.29 t** | ~6.86 t |
| 600 kW | 600,000 ÷ 350 = **~1,714 m²** | ~5.14 t | **~8.57 t** | ~13.7 t |

Add a pumped-fluid thermal loop (pumps, accumulator, working fluid, plumbing) of **~+150–400 kg at 130 kW**, scaling roughly with power to **~+0.7–1.8 t at 600 kW** — folded into the "high" column / verdict below.

### 4.4 Combined solar + radiator mass — the scaling table

| Rack power | Solar mass (low–mid–high) | Radiator mass (low–mid–high) | **Combined low** | **Combined MID** | **Combined high** |
|---|---|---|---|---|---|
| **130 kW** | 0.87 / 1.3 / 1.9 t | 1.11 / 1.86 / 2.97 t | **~2.0 t** | **~3.2 t** | **~4.9 t** |
| **300 kW** | 2.0 / 3.0 / 4.5 t | 2.57 / 4.29 / 6.86 t | **~4.6 t** | **~7.3 t** | **~11.4 t** |
| **600 kW** | 4.0 / 6.0 / 8.9 t | 5.14 / 8.57 / 13.7 t | **~9.1 t** | **~14.6 t** | **~22.6 t** |

### 4.5 Does this blow the Neutron budget?

Neutron payload capacity ([Neutron Payload User's Guide](https://rocketlabcorp.com/assets/Uploads/Rocket-Lab-Neutron-PUG-reduced-final.pdf), [Wikipedia: Neutron](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron)): **15 t expendable / 13 t downrange-landing / 8.5 t return-to-launch-site (full reuse) — all to LEO**. SSO costs ~20–30%, so a reusable SSO budget is **~8.5 t** (downrange recovery; `node_mass_model.md` §5).

> **Superseded (wave-5, 2026-05-17):** the ~8.5 t reusable SSO budget used in
> the comparison below has been re-baselined to a working **~9.5 t (range
> 8.5–10.5 t)** — see `rocket_lab/neutron/payload_and_block_upgrade.md`. The
> "remaining-budget" column below reads ~1 t pessimistically against the
> current figure; this doc's solar/radiator scaling analysis is unchanged.

| Rack power | Solar+radiator mid | Remaining for rack+bus+propellant+margin, vs ~8.5 t reusable SSO | Vs 15 t expendable LEO |
|---|---|---|---|
| **130 kW** | **~3.2 t** | ~5.3 t left — **rack (~1.6 t) + bus + prop + margin fit. Node closes on a reusable flight.** | comfortable |
| **300 kW** | **~7.3 t** | ~1.2 t left — **does NOT close on a reusable flight**; the rack alone (~3+ t at 300 kW) overruns. Needs expendable or 1-rack/launch with a stripped bus. |
| **600 kW** | **~14.6 t** | **negative — solar+radiator ALONE (~14.6 t) nearly equals the entire 15 t expendable LEO capacity** before the rack, bus, structure, or a gram of propellant. **The node cannot fly on a single Neutron at 600 kW.** |

**Verdict: yes — at high rack power density, solar+radiator mass blows the Neutron budget.** At 130 kW it is a comfortable ~3 t. At 300 kW it consumes most of a reusable flight. **At 600 kW the two power-scaling subsystems alone (~9–23 t, mid ~14.6 t) exceed Neutron's reusable capacity and rival its expendable capacity** — the node would have to be split across multiple launches and assembled, or the rack power-per-node capped. The mass scales **linearly with rack power** (both area terms are linear in watts), so there is no relief from scale — only from better areal density.

---

## 5. Deployable / compact-stow technology

The node must fold **~470–2,200 m² of solar array + ~370–1,700 m² of radiator** into Neutron's ~5 m fairing. Relevant techniques:

| Technique | Principle | Stowed-to-deployed ratio | Maturity |
|---|---|---|---|
| **Roll-out (ROSA-class)** | Flexible PV blanket rolled on a composite slit-tube boom that strain-energy-deploys | ROSA stows at **~40 kW/m³**; ~¼ the volume of rigid arrays for equal power; ELSA adds +50% stowed density | **Flight-proven** (ISS iROSA, lunar Gateway 60 kW wings 2025) ([pv-magazine](https://pv-magazine-usa.com/2025/07/03/redwire-deploys-60-kw-roll-out-solar-array-for-the-first-lunar-orbit-space-station/)) |
| **Z-fold (accordion blanket)** | Blanket folds accordion-style, deployed by a boom/mast | Linear stack; deployed-to-stowed length ratio ~10–50× | Flight-proven (ISS original wings, many GEO sats) |
| **Origami (Miura-ori, flasher)** | 2-D folding pattern collapses a large membrane to a compact prism/disc | Flasher prototype: **deployed-to-stowed diameter ~9×**; CubeSat origami panels ~7:1 | Demonstrated; flew on Japan's Space Flyer Unit (1995, Miura-ori) ([ScienceDirect origami review](https://www.sciencedirect.com/science/article/pii/S1000936125004376), [NASA: high-stowed-volume arrays](https://www.nasa.gov/directorates/stmd/space-tech-research-grants/deployable-solar-array-structures-with-high-stowed-volume-efficiencies/)) |
| **Telescoping / coilable booms** | Composite booms that coil or telescope to extend blankets/radiators far from the bus | Boom coils to a small drum; deployed length 10s of m | Flight-proven (NASA Deployable Composite Booms, solar-sail booms) ([NASA DCB](https://www.nasa.gov/centers-and-facilities/langley/deployable-composite-booms-dcb/)) |
| **Deployable radiator panels** | Hinged/folded radiator panels with loop-heat-pipe thermal joints; or roll-out radiator membranes | Folded panel stacks; ~25–40 m²/m³ folded (est.) | LHP-based deployable radiators flight-proven; large (>1,000 m²) roll-out radiators are **not yet demonstrated** — key risk |

**Packaging takeaway.** Solar-array stowage is a **solved problem** — ROSA-class roll-out arrays are purpose-built for exactly this and stow at ~40 kW/m³ (a 600 kW node's ~800 kW array ≈ ~20 m³ stowed, fits the fairing). The **radiator is the hard packaging problem**: a 600 kW node needs **~1,700 m² of deployable radiator** — larger than the entire ISS radiator system — and a roll-out/foldable radiator at that scale is **not flight-demonstrated**. The radiator drives both the mass budget (§4) *and* the packaging/deployment risk.

---

## 6. Rocket Lab's deployable-structures capability

### 6.1 The "N" acquisition — investigated, and the recollection does not hold

The founder recalled a recent Rocket Lab acquisition of a company **beginning with "N"** (explicitly *not* Mynaric) relevant to **collapsing/expanding structures**. **Cross-checking Rocket Lab's complete acquisition history against multiple sources, no such acquisition exists.**

**Rocket Lab's full acquisition list** ([Wikipedia: Rocket Lab](https://en.wikipedia.org/wiki/Rocket_Lab); [NASASpaceflight Q1 2026](https://www.nasaspaceflight.com/2026/05/rocket-lab-q1-2026/); [SpaceNews: Motiv](https://spacenews.com/rocket-lab-announces-large-launch-contract-and-plans-to-acquire-space-robotics-company/)):

| Company | Date | Domain |
|---|---|---|
| Sinclair Interplanetary | Apr 2020 | Satellite components (reaction wheels, star trackers) |
| Advanced Solutions, Inc. (ASI) | Oct 2021 | Flight software, GN&C |
| Planetary Systems Corporation (PSC) | Dec 2021 | **Satellite separation systems** (mechanisms) |
| **SolAero Holdings** | Jan 2022 | **Space solar cells, solar panels, AND composite/precision aerospace structures** |
| Geost, LLC | Aug 2025 | Electro-optical / IR payload sensors |
| **Mynaric AG** | Apr 2026 | Laser optical comms terminals — *the only "N"-initial acquisition* |
| **Motiv Space Systems** | announced May 2026 (closing Q2 2026) | **Space robotics, actuators, drive electronics, precision deployment mechanisms** |

**Finding (report plainly):** The only Rocket Lab acquisition starting with "N" is **Mynaric** — laser comms, not structures, and explicitly excluded by the founder. **There is no Rocket Lab acquisition of a deployable / collapsing-expanding-structures company whose name begins with "N."** The recollection is most likely a conflation of (a) **Mynaric** (the "N"/"M" confusion is easy), and/or (b) one of the genuine mechanism/structures acquisitions below. It may also conflate Rocket Lab with **Redwire**, which *did* acquire **Deployable Space Systems (DSS)** — the ROSA inventor — a leading deployable-solar-array and structures company (begins with "D", not "N") ([Redwire acquires DSS](https://rdw.com/newsroom/redwire-acquires-deployable-space-systems-dss-a-leading-supplier-of-space-mission-enabling-deployable-solar-arrays-structures-and-mechanisms/)). **Recommend the founder treat the "N-company" memory as unverified.**

### 6.2 Rocket Lab's *actual* relevant capabilities

Rocket Lab nonetheless has **real, directly relevant in-house capability** for this node — just not via an "N" company:

- **SolAero (2022)** — the cornerstone. Provides space solar **cells, panels, AND composite structural products**; >1,000 missions of heritage. This is the foundation of Rocket Lab's solar-array business and the Feb-2026 silicon arrays (§1.2). SolAero's composite-structures line is directly relevant to deployable booms/panels.
- **Motiv Space Systems (May 2026)** — robotics, **actuators, multi-DOF arms, drive electronics, precision mechanisms**. NASASpaceflight characterizes Motiv as adding "the robotic mechanisms that deploy" satellites. This is Rocket Lab's most relevant *deployment-mechanism* acquisition — exactly the actuator/hinge/boom-drive technology a large deployable array+radiator needs.
- **Planetary Systems Corporation (2021)** — separation systems and mechanisms; mechanism/release-device heritage.
- **Sinclair Interplanetary (2020)** — satellite mechanisms and components (reaction wheels, etc.).

**Bottom line:** Rocket Lab can credibly build the solar array (SolAero + the new silicon line) and the deployment mechanisms (Motiv, PSC). What it has **not** demonstrated publicly is a **large deployable radiator** — neither SolAero nor Motiv is a radiator house. The radiator is the capability gap (build, partner, or acquire).

---

## 7. Cost vs. mass verdict

**State it plainly.** For this node, **solar+radiator is primarily a MASS problem, not a cost problem — and the problem gets monotonically worse as rack power density rises.**

**Why mass, not cost:**

- **Cost scales linearly and lands on a soft constraint.** Space solar cells run ~$500–1,000/W at the *cell* level for low volume ([openPR multi-junction market](https://www.openpr.com/news/4389146/multi-junction-space-solar-cells-market-to-reach-us-419-million)), but Rocket Lab *builds its own arrays in-house* (SolAero) and is explicitly driving silicon arrays to **low $/W at industrial scale** ([Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/)). Radiators are not a major cost line. A 4.6× rise in rack power means ~4.6× the array+radiator cost — a budget number, painful but bounded, and falling per-watt over time. Cost never *prevents* the mission.
- **Mass scales linearly and lands on a HARD constraint — the Neutron payload ceiling.** §4.5: solar+radiator alone is ~3.2 t at 130 kW (fine), ~7.3 t at 300 kW (consumes a reusable flight), and **~14.6 t at 600 kW — exceeding Neutron's reusable capacity and rivaling its expendable capacity, before the rack/bus/propellant.** There is no scale relief; both terms are linear in watts. The launch vehicle cannot be "budgeted up."
- **The radiator dominates the mass and barely improves.** At every power level the radiator is heavier than the array (§4.4) and, unlike solar, its W/m² is physics-bounded — it has little improvement runway (§3.2). The radiator is the single worst mass actor.

**How the verdict shifts with power density:**

| Rack power | Character | Binding constraint |
|---|---|---|
| **~130 kW** (today) | Solar+radiator ~3 t — a routine subsystem. Cost real but secondary. | Neither — node closes comfortably. |
| **~300 kW** | Solar+radiator ~7 t — consumes most of a reusable Neutron flight. | **Mass** — forces expendable launch or architecture change. |
| **~600 kW** | Solar+radiator ~15 t — exceeds Neutron alone. | **Mass — hard wall.** Node cannot fly intact on one Neutron. |

**The founder's two gut calls are confirmed:** (a) cost is real but secondary — **correct**; (b) mass is the real constraint as power density rises — **correct, and it is the decisive constraint above ~300 kW.** The actionable levers are the *areal* ones: push array specific power toward the ~200–300 W/kg advanced/GaAs end (not the cheaper, heavier silicon end) for high-power nodes, and attack the radiator's kg/m² aggressively — every kg/m² shaved off a ~1,700 m² radiator is ~1.7 t. If 600 kW racks are the target, the realistic answers are **cap node power (multiple lower-power nodes), or multi-launch on-orbit assembly** — both driven entirely by the mass wall, not by cost.

---

## Sources

- **Solar arrays:** [Wikipedia: Roll Out Solar Array](https://en.wikipedia.org/wiki/Roll_Out_Solar_Array); [Redwire ROSA flysheet](https://rdw.com/wp-content/uploads/2023/06/redwire-roll-out-solar-array-flysheet.pdf); [Redwire ELSA announcement](https://rdw.com/newsroom/redwire-announces-new-high-performance-low-mass-solar-array-building-upon-the-success-of-its-roll-out-solar-array-product-line/); [pv-magazine: 60 kW ROSA, Jul 2025](https://pv-magazine-usa.com/2025/07/03/redwire-deploys-60-kw-roll-out-solar-array-for-the-first-lunar-orbit-space-station/); [NASA Small Spacecraft SoA — Power 2024](https://www.nasa.gov/wp-content/uploads/2025/02/3-soa-power-2024.pdf); [NASA SoA Power subsystems](https://www.nasa.gov/smallsat-institute/sst-soa/power-subsystems/); [ScienceDirect: flexible/high-specific-power PV survey 2025](https://www.sciencedirect.com/science/article/abs/pii/S2542435125003757)
- **Rocket Lab silicon arrays:** [Rocket Lab press release, 26 Feb 2026](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/); [GlobeNewswire mirror](https://www.globenewswire.com/news-release/2026/02/26/3246118/0/en/Rocket-Lab-Introduces-Advanced-Silicon-Solar-Arrays-To-Power-Space-Based-Data-Centers.html)
- **Solar cells / cost:** [Tech Briefs: Si vs GaAs](https://www.techbriefs.com/component/content/article/18946-silicon-vs-gallium-arsenide-which-photovoltaic-material-performs-best); [openPR: multi-junction space solar cell market](https://www.openpr.com/news/4389146/multi-junction-space-solar-cells-market-to-reach-us-419-million); [NTRS: ROSA cost/tech (FACT, Mega-ROSA)](https://ntrs.nasa.gov/citations/20130008777)
- **Radiators:** [ISNPS: Advanced Lightweight Heat Rejection Radiators](https://isnps.unm.edu/reports/ISNPS_Tech_Report_103.pdf); [Aerospace Corp: Small-Sat Deployable Radiator Study 2024](http://www.mstl.atl.calpoly.edu/~workshop/archive/2024/presentations/2024_Day1_Session3_Madison.pdf); [NASA Small Spacecraft SoA — Thermal 2024](https://www.nasa.gov/wp-content/uploads/2025/02/7-soa-thermal-2024.pdf); [Gilmore Spacecraft Thermal Control Handbook ch.6](http://matthewwturner.com/uah/IPT2008_summer/baselines/LOW%20Files/Thermal/Spacecraft%20Thermal%20Control%20Handbook/06.pdf); [Deployable radiator study, 409 W/m² planform](https://ui.adsabs.harvard.edu/abs/2021MsT..........6M/abstract); [ThermAvant OHP radiators](https://www.thermavant.com/thermavant-products/oscillating-heat-pipe-radiators)
- **Deployable/stow technology:** [ScienceDirect: origami in space deployable membranes](https://www.sciencedirect.com/science/article/pii/S1000936125004376); [NASA: deployable solar arrays with high stowed-volume efficiency](https://www.nasa.gov/directorates/stmd/space-tech-research-grants/deployable-solar-array-structures-with-high-stowed-volume-efficiencies/); [NASA Deployable Composite Booms](https://www.nasa.gov/centers-and-facilities/langley/deployable-composite-booms-dcb/)
- **Rocket Lab acquisitions / capability:** [Wikipedia: Rocket Lab](https://en.wikipedia.org/wiki/Rocket_Lab); [NASASpaceflight: Rocket Lab Q1 2026](https://www.nasaspaceflight.com/2026/05/rocket-lab-q1-2026/); [SpaceNews: Rocket Lab to acquire Motiv Space Systems](https://spacenews.com/rocket-lab-announces-large-launch-contract-and-plans-to-acquire-space-robotics-company/); [GlobeNewswire: Motiv acquisition](https://www.globenewswire.com/news-release/2026/05/07/3290619/0/en/rocket-lab-to-acquire-robotics-leader-motiv-space-systems.html); [TechCrunch: Rocket Lab acquires SolAero](https://techcrunch.com/2022/01/18/rocket-lab-acquires-solaero-holdings-for-80m-to-boost-space-solar-cell-production/); [Redwire acquires Deployable Space Systems](https://rdw.com/newsroom/redwire-acquires-deployable-space-systems-dss-a-leading-supplier-of-space-mission-enabling-deployable-solar-arrays-structures-and-mechanisms/)
- **Neutron:** [Neutron Payload User's Guide v1.0](https://rocketlabcorp.com/assets/Uploads/Rocket-Lab-Neutron-PUG-reduced-final.pdf); [Wikipedia: Neutron](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron)
- **Internal:** `node_design/node_mass_model.md` (§3 power chain, §4 radiator, §5 Neutron budget)

---

## Open questions / uncertainties

1. **Rocket Lab silicon-array specific power is unpublished.** Assumed ~70–110 W/kg (~25–40% below advanced GaAs ROSA). If the silicon arrays are lighter than assumed, the silicon-case masses in §4 drop. Highest-value unknown for the array side. (FLAG — estimate.)
2. **No public $/W for integrated arrays.** Cell-level $500–1,000/W figures are low-volume; integrated-array and at-scale silicon costs are proprietary. The cost-vs-mass verdict does not hinge on this (mass is binding) but a real number would firm up §7.
3. **Radiator areal mass dominates the mass budget.** The 3–8 kg/m² spread swings the 600 kW radiator from ~5 t to ~14 t. Required area also depends sharply on achievable radiator surface temperature (area falls as T⁴). A chip→coolant→panel thermal model is the next step (noted also in `node_mass_model.md`).
4. **Large deployable radiators (>1,000 m²) are not flight-demonstrated.** The 300/600 kW radiator areas exceed anything flown. Both a mass risk and a deployment/packaging risk; the §4 numbers assume the technology matures.
5. **The "N-company" recollection is unverified and most likely incorrect.** No Rocket Lab acquisition beginning with "N" relates to deployable/collapsing structures (only Mynaric, laser comms). If the founder has a specific source, it should be produced; otherwise treat as a memory error (possible conflation with Mynaric, with Motiv/PSC mechanisms, or with Redwire's DSS acquisition).
6. **600 kW node is not single-launch-feasible on Neutron.** §4.5 shows solar+radiator alone rivals Neutron's expendable capacity at 600 kW. The architectural response (cap node power, or on-orbit assembly across multiple launches) is outside this doc's scope but is forced by the mass result.
7. **Rocket Lab has no in-house large-radiator capability.** SolAero (solar) and Motiv (mechanisms) are relevant; neither is a radiator house. Build/partner/acquire decision flagged.
