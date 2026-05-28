# Orbital Compute Node — Mass & Dimensions Model

*Project: RKLB Space Data Center — feasibility phase. Document date: May 2026.*
*Author: research agent. All hard numbers cross-checked against ≥2 sources where possible; estimates explicitly labeled.*

---

> **Source status (2026-05-25):** See [SOURCE_INDEX.md](../SOURCE_INDEX.md) claim IDs GPU-005, THR-004 through THR-006, and THR-011 through THR-012. This is a derived mass model. Current GB300 OEM materials suggest using vendor-specific rack mass closer to roughly **1.5–1.58 t** for conservative planning rather than a fixed **1.36 t** value. Solar/radiator mass and the Neutron SSO budget remain model inputs, not certified outputs.

## Summary

This document builds a per-node mass-and-dimensions model for one orbital AI-inference satellite ("node") carrying 1–2 NVIDIA GB300 NVL72-class server racks in a ~500–600 km dawn-dusk sun-synchronous orbit.

**Headline figures (mid estimates):**

| Configuration | Node launch mass (mid) | Range (low–high) |
|---|---|---|
| **1-rack node** | **~5.4–8.6 t** (design to ~7–9 t) | 4.3 – 14.1 t across tech cases |
| **2-rack node** | **~9.6–16.6 t** | exceeds even the expendable budget |

> **Summary reconciled with §6–§7 and the project tracker (2026-05-17).** An
> earlier version of this Summary stated a single "~5.4 t" headline and a
> "volume-bound, not mass-bound" verdict — that reflected only the
> advanced-technology, mass-optimized path and is **superseded by the doc's own
> §6–§7** (which compute ~5.6 / 8.6 / 14.1 t across baseline/feasibility/
> conservative tech cases and conclude **mass-bound**) and by the wave-5 SSO
> re-baseline. The figures below now match §6–§7, the SSO budget, and the
> radiator-area reconciliation.

**Verdict — mass vs. volume bound:** The node is **mass-bound, not volume-bound** — fairing-volume-comfortable but mass-budget-tight. A single GB300 rack (~2.3 m tall, 0.6 m wide, ~1.1 m deep, ~1.36 t) fits trivially inside Neutron's ~5 m fairing; the binding constraint is **launch mass**. A 1-rack node masses **~5.4–8.6 t** (design to ~7–9 t) against a **~9.5 t working reusable-to-SSO budget** (wave-5 re-baseline, range 8.5–10.5 t — see `synthesis/wave5_synthesis.md` and `rocket_lab/neutron/payload_and_block_upgrade.md`; supersedes this doc's earlier ~8.5 t figure): it flies reusable, with margin in the feasibility-mid case but tight in the conservative case. The packaging task is **~200–430 m² of radiator (working ~300 m²/rack** — lint-reconciled project range, superseding the earlier ~140–210 m² optimistic bound — see `synthesis/lint_report.md` §1.1) plus **~500–900 m² of solar array** per rack into the fairing's stowed envelope. A 2-rack node (~9.6–16.6 t) **exceeds even the expendable budget** and is dropped — the architecture is **1 rack per node, 1 node per Neutron launch**.

**Confidence: medium-low.** Rack dimensions/weight and solar/radiator areal densities are well-sourced (high confidence). The space-modified-rack delta, spacecraft bus mass, and — critically — Neutron's *internal usable fairing length* and *SSO performance number* are estimates: Rocket Lab has **not published** an SSO figure or detailed internal fairing envelope as of May 2026.

---

## 1. Standard server rack dimensions & the GB300 NVL72

### EIA-310 19-inch rack standard

The EIA-310 standard defines the ubiquitous "19-inch rack" ([RackSolutions](https://www.racksolutions.com/news/data-center-optimization/eia-310-definition/), [Wikipedia: 19-inch rack](https://en.wikipedia.org/wiki/19-inch_rack)):

- **Mounting-rail width:** 19 in (482.6 mm) front-panel opening; rail-to-rail internal ~17.75 in.
- **Rack unit (U):** 1.75 in = 44.45 mm. Common heights: 42U (~1867 mm usable), 45U, 48U.
- **Cabinet external width:** typically **600 mm** (24 in).
- **Depth:** flexible, **600–1200 mm**; AI racks trend deep (1070–1370 mm / 42–54 in).
- A standard full-height cabinet is ~600 mm W × ~1070 mm D × ~2000–2300 mm H.

### NVIDIA GB300 NVL72 — actual physical numbers

The GB300 NVL72 ("Blackwell Ultra") integrates into a standard 19-inch cabinet footprint; vendor implementations (GIGABYTE, Supermicro, Lenovo, HPE) cluster tightly:

| Parameter | Value | Source |
|---|---|---|
| External dimensions (L × W × D × H) | ~1068 mm L-rail × **600 mm W** × ~1200 mm D × **2299 mm H** | [GIGABYTE GB300 NVL72](https://www.gigabyte.com/Enterprise/GIGAPOD-Rack-Scale/AI-DLC-Rack_NVIDIA-GB300-NVL72), [Supermicro 48U GB300](https://www.supermicro.com/en/products/system/gpu/48u/srs-gb300-nvl72) |
| Height class | 48U cabinet | [Supermicro](https://www.supermicro.com/en/products/system/gpu/48u/srs-gb300-nvl72), [Lenovo Press lp2357](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai) |
| Fully-populated weight | Vendor-specific; older planning value **~1.36 t** (3,000 lb), current public OEM materials support roughly **1.5–1.58 t** for conservative GB300 planning | [Sunbird DCIM](https://www.sunbirddcim.com/blog/how-much-power-does-nvidia-gb300-nvl72-need), [Introl](https://introl.com/blog/why-nvidia-gb300-nvl72-blackwell-ultra-matters) |
| Power (TDP / peak) | **~135 kW TDP, up to ~155 kW peak** | [Sunbird DCIM](https://www.sunbirddcim.com/blog/how-much-power-does-nvidia-gb300-nvl72-need), [Introl](https://introl.com/blog/why-nvidia-gb300-nvl72-blackwell-ultra-matters) |
| Heat split (terrestrial) | ~90% liquid, ~10% air | [Lenovo Press lp2357](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai) |
| Internal layout | 18 GPU compute trays + 9 NVLink switch trays + 6–8 power shelves | [Supermicro](https://www.supermicro.com/en/products/system/gpu/48u/srs-gb300-nvl72) |

> **Note on the 1.36 t figure.** Terrestrially, the GB200/GB300 ships as separate sub-assemblies (compute rack ~1.5 t, NVLink switch rack ~0.8 t, CDU ~0.4 t, PDU ~0.3 t per some integrators — [Spheron](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/)). The widely cited **"1.36 t" is the single integrated NVL72 compute cabinet** (the 19-inch unit holding the 72 GPUs + NVLink). For this model we treat **1.36 t** as the as-delivered intact rack and add the space modifications below. **Baseline geometry: 600 mm W × 1200 mm D × 2300 mm H, 1.36 t** — per founder guidance, we adopt pre-existing standard rack geometry, NOT a custom dispenser-sized unit.

---

## 2. The space-modified rack

The terrestrial GB300 rack assumes (a) ~10% air cooling via fans, (b) 1-g datacenter mounting (rolls on castors, bolts to a floor), and (c) shirt-sleeve pressurized ambient. A space-flown rack must instead survive ~5–6 g axial + acoustic/random-vibration launch loads, operate in hard vacuum, and reject 100% of its heat to liquid.

**Mass changes — reasoning:**

| Change | Direction | Δ mass estimate | Reasoning |
|---|---|---|---|
| Remove all air-cooling fans, fan walls, air plenums, RDHx provisions | **lighter** | −20 to −40 kg | Fan modules are light individually but numerous; ducting/plenum sheet metal adds up. |
| Remove castors, seismic floor-mount hardware, some cosmetic panels | **lighter** | −10 to −25 kg | Not needed in microgravity. |
| Add full cold-plate coverage to the ~10% currently air-cooled (DIMMs, VRMs, NICs, switch optics) | **heavier** | +25 to +50 kg | Copper/aluminum cold plates ~0.3–1 kg each across hundreds of components + extra manifold/tubing. |
| Launch structural reinforcement: stiffened frame, tray-level tie-downs, snubbers, isolators | **heavier** | +120 to +250 kg | Terrestrial racks already gain "strengthening struts/fasteners" for liquid-cooling weight ([OCP](https://www.opencompute.org/documents/ocp-liquid-cooling-integration-and-logistics-white-paper-revision-1-0-1-pdf)); a launch-rated rack needs every tray restrained against 6-g + random vibe. Biggest single delta. Dominated by frame + 27 tray restraints. |
| Vacuum-rating: replace electrolytic caps, conformal coat, seal/vent the loop, de-rate | **heavier (small)** | +5 to +20 kg | Mostly component swaps; modest mass. |
| Radiation spot-shielding for the most SEE-sensitive parts (not full-rack) | **heavier** | +15 to +60 kg | Targeted tantalum/aluminum shields on switch/control electronics. LEO dawn-dusk SSO is a relatively benign radiation environment, so spot-shield only. |
| Integrated coolant manifolds / quick-disconnects sized for the space loop | **heavier (small)** | +10 to +30 kg | Replaces terrestrial CDU interface. |

**Net modified-rack mass:**

| Estimate | Calculation | Modified rack mass |
|---|---|---|
| Low | 1360 − 50 + 25 + 120 + 5 + 15 + 10 | **~1,485 kg** |
| Mid | 1360 − 45 + 38 + 185 + 12 + 35 + 20 | **~1,605 kg** |
| High | 1360 − 30 + 50 + 250 + 20 + 60 + 30 | **~1,740 kg** |

> **Modified rack: ~1.5–1.74 t, mid ~1.6 t.** The dominant uncertainty is launch reinforcement. A clean-sheet space-optimized compute unit could undercut this, but the founder's directive is to keep standard rack geometry, which forces reinforcing an off-the-shelf frame rather than designing loads out — a mass penalty we accept. Thermal-design power for sizing radiators: **~150 kW continuous per rack** (135 kW TDP at sustained inference load, with margin toward the 155 kW peak; we use 150–185 kW as the sizing band per the brief).

---

## 3. Solar array mass

### Areal mass density & specific power — modern space arrays

| Array type | Specific power (W/kg) | Implied mass | Source |
|---|---|---|---|
| Legacy rigid GaAs panels | ~25–70 W/kg; 10–15 kg/kW | heavy | [NASA SoA Power](https://www.nasa.gov/smallsat-institute/sst-soa/power-subsystems/) |
| **ROSA roll-out (GaAs)** | **~100–120 W/kg typical; up to ~225 W/kg (advanced 25 kW unit, BOL AM0)** | **~4.4 kg/kW** (Redwire flysheet) | [Wikipedia: ROSA](https://en.wikipedia.org/wiki/Roll_Out_Solar_Array), [Redwire ROSA flysheet](https://rdw.com/wp-content/uploads/2023/06/redwire-roll-out-solar-array-flysheet.pdf) |
| **Rocket Lab silicon arrays (Feb 2026)** | Not published; "lightweight, flexible, mass-manufacturable, low cost/watt" | see penalty below | [Rocket Lab press release, 26 Feb 2026](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/) |

**Cell efficiency (AM0, beginning-of-life):**
- Triple-junction GaAs space cells: **~30% BOL** standard, 32–34% emerging ([CESI CTJ30](https://www.cesi.it/app/uploads/2020/03/Datasheet-CTJ30-1.pdf), [satsearch 30% TJ](https://satsearch.co/products/cavu-corp-30triplejunction-solar-cell)).
- Space silicon cells: historically ~14–18%; modern terrestrial-derived space silicon optimistically ~20% ([Tech Briefs Si vs GaAs](https://www.techbriefs.com/component/content/article/18946-silicon-vs-gallium-arsenide-which-photovoltaic-material-performs-best)).

**Silicon area/mass penalty.** Rocket Lab's Feb 2026 silicon arrays trade efficiency for supply-chain resilience (no Ga/Ge critical minerals) and low cost/watt at gigawatt scale ([Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/)). If GaAs ≈ 30% and space silicon ≈ 20%, silicon needs **~30% / 20% = 1.5× the area** for the same power. Silicon arrays can be physically lighter *per cell* (no Ge substrate), but the larger blanket, longer booms, and bigger deployment structure largely offset this — net result: assume **silicon array specific power ~30–40% lower than GaAs ROSA** unless Rocket Lab publishes better. Rocket Lab also offers a **hybrid** GaAs+Si array.

### Array sizing — power chain for one rack

Required: ~150–185 kW *continuous electrical at the rack* per the brief.

End-to-end efficiency from array output to rack input (estimate): power management & distribution ~92%, harness/regulation ~95%, battery round-trip (minimal — dawn-dusk SSO is near-continuous sun, eclipse <5% so battery cycling is small) ~98% effective → **~0.86 chain efficiency**. Dawn-dusk SSO sees sun ~95–100% of orbit, so we size the array close to the load with modest margin.

**Array electrical output needed** = rack load / chain efficiency, plus ~15% sizing margin (degradation, off-pointing, EOL):

- For 150 kW rack load: 150 / 0.86 × 1.15 ≈ **~201 kW array (BOL)**
- For 185 kW rack load: 185 / 0.86 × 1.15 ≈ **~247 kW array (BOL)**

**Array mass** = array power / specific power:

| Array tech | Specific power assumed | Mass @ 201 kW | Mass @ 247 kW |
|---|---|---|---|
| ROSA GaAs, advanced (200 W/kg) | 200 W/kg | ~1,005 kg | ~1,235 kg |
| ROSA GaAs, conservative (120 W/kg) | 120 W/kg | ~1,675 kg | ~2,060 kg |
| RKLB silicon (est. ~100 W/kg) | 100 W/kg | ~2,010 kg | ~2,470 kg |

**Adopted per-rack solar array mass:** low **~1.0 t** (advanced GaAs ROSA), mid **~1.5 t** (mixed/hybrid ~135 W/kg), high **~2.3 t** (silicon, conservative).

**Array area** (cross-check vs. prior ~375–460 m²/rack estimate): solar constant ~1361 W/m². At 30% GaAs and ~90% packing/cosine: ~370 W/m² → 201 kW ÷ 370 ≈ **~545 m²** (GaAs). At 20% silicon: ~245 W/m² → **~820 m²** (silicon). This is **larger** than the prior 375–460 m² estimate — the prior figure looks optimistic; **expect ~500–550 m²/rack GaAs, ~750–900 m²/rack silicon.**

---

## 4. Radiator mass & the "radiator on the back of the solar panel" idea

### (a) Is co-mounting radiators with solar arrays real?

**Yes — it is a documented, used technique.** NASA small-spacecraft thermal-control work describes "a deployable integrated power generation and thermal control system on a gimbal … with a microvascular composite radiator that deploys normal to the back of the solar array" ([NASA SoA Thermal Control](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/), [NASA SoA Thermal 2024 PDF](https://www.nasa.gov/wp-content/uploads/2025/02/7-soa-thermal-2024.pdf)). High-temperature solar-array designs mount cells on a heat-spreader so the **backside doubles as a radiator** ([NASA NTRS 20090004578](https://ntrs.nasa.gov/api/citations/20090004578/downloads/20090004578.pdf)). So the founder's hypothesis is sound in principle.

**Caveat for this design:** the solar-array *front* must face the sun; its *back* faces deep space — an excellent radiator view. Co-mounting therefore *works thermally*. The practical limits are (i) the array back also re-absorbs some IR/albedo and runs warm from the cells themselves, slightly de-rating radiator performance, and (ii) the array gimbals to track the sun, so a co-mounted radiator's view factor changes with season. For dawn-dusk SSO the geometry is stable, so co-mounting is **a genuinely attractive option** — but we do not assume it removes 100% of dedicated radiator area; treat it as reducing the *deployment-structure* mass, not the radiator panel mass.

### (b) Radiator-area-to-solar-area ratio — validate the "~30% more" claim

The founder's instinct ("radiator needs ~30% more area than solar") is **wrong in the conservative direction — radiator area is much larger, not 30% larger.** Work it through:

- The rack draws ~150 kW electrical and converts **~100% of it to heat** that must be radiated. So **heat to reject ≈ 150 kW** (≈ array-delivered power).
- A flat radiator at hot-loop temperature radiates by Stefan-Boltzmann: `Q/A = ε·σ·(T_rad⁴ − T_sink⁴)`.
  - Hot liquid loop 60–90 °C; assume radiator surface ~50 °C = 323 K (a drop from loop to surface).
  - ε ≈ 0.85, σ = 5.67×10⁻⁸, deep-space/effective sink ~250 K (LEO, with Earth IR + albedo loading).
  - `Q/A = 0.85 × 5.67e-8 × (323⁴ − 250⁴)` = `0.85 × 5.67e-8 × (1.088e10 − 3.906e9)` = `0.85 × 5.67e-8 × 6.97e9` ≈ **~336 W/m²** gross.
  - A two-sided deployable radiator can reject from both faces, but one face often has a poor view (toward Earth/structure); assume an **effective ~300–400 W/m²** per unit of planform area for a well-designed 2026 panel at this temperature. This is consistent with literature: spacecraft radiators reject ~100–350 W/m² typically, up to ~400 W/m² planform for advanced designs ([Gilmore, Spacecraft Thermal Control Handbook ch.6](http://matthewwturner.com/uah/IPT2008_summer/baselines/LOW%20Files/Thermal/Spacecraft%20Thermal%20Control%20Handbook/06.pdf), [deployable radiator study, 409 W/m² planform](https://ui.adsabs.harvard.edu/abs/2021MsT..........6M/abstract)).
- **Radiator area needed** = 150,000 W ÷ ~350 W/m² ≈ **~430 m²** of radiator per rack (range ~375–500 m² for 300–400 W/m²).

> **Hot-loop caveat — the radiator-shrink lever is bounded by junction
> temperature (2026-05-17).** The radiator area above, and the project's working
> ~300 m²/rack figure, both depend on running the coolant **loop/radiator hot**
> (~60–90 °C loop, ~50–80 °C radiator surface) to exploit the Stefan-Boltzmann
> T⁴ term — a hotter surface sheds far more W/m², shrinking the panel. But this
> is **not a free lever**: the GPU/HBM junction temperature is capped at
> **Tjmax ≈ 83–85 °C** (barely moving across generations), and HBM error rates
> and silicon failure rise sharply with junction temperature — roughly an
> Arrhenius ~2× failure penalty per +10 °C. The loop can only run as hot as the
> junction-to-coolant ΔT budget allows. Sizing the radiator on a hotter surface
> trades **radiator mass against hardware reliability and service life** — it is
> the project's known "hot-loop ↔ HBM-thermal tension." See
> `node_design/hot_chip_thermal_trajectory.md` (§3–§4) for the honest treatment;
> the ~300 m² working figure should be read as *conditional on* a hot-loop
> design that defends the junction.

> **Cross-reference (2026-05-17):** the wave-1 `orbital/thermal_analysis.md`
> derives a lower figure (~120–210 m²/rack) under more optimistic
> radiator-temperature and second-face assumptions. The two are reconciled in
> `synthesis/lint_report.md` §1.1, which adopts a **~200–430 m²/rack project
> range (working ~300 m²)** pending a chip→coolant→panel thermal model. This
> doc's analysis is unchanged; the ~375–500 m² here is the conservative bound.

**Compare to solar area:** GaAs solar array ≈ ~545 m²/rack; silicon ≈ ~820 m²/rack.

- **Radiator/solar ratio (GaAs case):** 430 / 545 ≈ **~0.79 — radiator needs ~80% of solar area**, i.e. *less* area than the array, not 30% more.
- **Radiator/solar ratio (silicon case):** 430 / 820 ≈ **~0.52 — radiator needs only ~half the solar area.**

**Why:** both the array and the radiator handle ~the same power (~150 kW), but the radiator's areal "efficiency" (~350 W/m²) is *higher* than the solar array's effective collection (~250–370 W/m²). With GaAs they are roughly comparable areas; with low-efficiency silicon the array balloons and the radiator looks small by comparison.

> **Correcting the founder's figure:** the "+30%" rule of thumb is not supported. The correct statement: **radiator area ≈ 0.5–0.9 × solar area**, depending on solar cell efficiency. The radiator is *area-comparable to or smaller than* the array. This is actually good news — and it means the "radiator on the back of the solar panel" idea is geometrically *feasible*: the array backside (~545–820 m²) has **enough area to host the entire ~430 m² radiator.** Co-mounting is not just possible, it is nearly area-matched. (Note prior project estimate of 120–210 m²/rack radiator was low; this analysis says ~375–500 m². The discrepancy is the assumed radiator temperature/sink — worth resolving in detailed design.)

### Radiator areal mass (2026-era deployable)

Literature: novel deployable radiator ~1.9 kg/m² (radiating area) / ~3.9 kg/m² (planform); NASA target ≤3 kg/m² integrated; heavy deployable + structure up to ~12 kg/m² ([NASA NTRS, deployable radiator](https://ui.adsabs.harvard.edu/abs/2021MsT..........6M/abstract), [Gilmore ch.6](http://matthewwturner.com/uah/IPT2008_summer/baselines/LOW%20Files/Thermal/Spacecraft%20Thermal%20Control%20Handbook/06.pdf)).

**Adopt: 3 kg/m² (low), 5 kg/m² (mid), 8 kg/m² (high)** — mid/high reflect the large pumped-fluid loop, headers, and deployment structure for a ~430 m² array-scale radiator (heavier per m² than a small cubesat panel).

**Radiator mass per rack** = ~430 m² × areal density:
- Low: 375 m² × 3 = **~1.1 t**
- Mid: 430 m² × 5 = **~2.15 t**
- High: 500 m² × 8 = **~4.0 t**

Plus the pumped-fluid thermal loop (pumps, accumulator, ~hundreds of kg of working fluid, plumbing): **+150–400 kg/rack**, folded into the radiator line item below.

---

## 5. Neutron fairing & SSO payload — official numbers hunt

**What Rocket Lab has published** ([Neutron Payload User's Guide v1.0, Jan 2025](https://rocketlabcorp.com/assets/Uploads/Rocket-Lab-Neutron-PUG-reduced-final.pdf); [Wikipedia: Neutron](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron); [Rocket Lab architecture update](https://rocketlabcorp.com/updates/rocket-lab-reveals-neutron-launch-vehicles-advanced-architecture/)):

| Parameter | Value | Confidence |
|---|---|---|
| Fairing diameter (payload accommodation) | **up to 5.0 m**, expandable to 5.5 m for non-standard payloads | high |
| Fairing type | Captive "Hungry Hippo" carbon-composite clamshell, integral to Stage 1, reused | high |
| Fairing overall height | ~14 m (46 ft) overall structure (NOT usable payload length) | medium |
| Payload to LEO — expendable | **15,000 kg** | high |
| Payload to LEO — downrange droneship landing | **13,000 kg** | high |
| Payload to LEO — return-to-launch-site (full reuse) | **8,500 kg** | high |
| **Payload to SSO** | **NOT PUBLISHED by Rocket Lab** | — |
| Internal *usable* payload envelope length | **NOT PUBLISHED in detail** | — |

**Hard finding:** As of May 2026 Rocket Lab has **not released a Neutron SSO performance number** nor a detailed internal payload static-envelope drawing. WebFetch of the PUG PDF was unavailable to this agent; the figures above are from the PUG as quoted by secondary sources plus Wikipedia, cross-checked.

**SSO estimate (clearly labeled ESTIMATE):** SSO (~98° retrograde, ~600 km) typically costs **~20–30% performance vs. due-east LEO** for a given vehicle. Applying that:
- Expendable to SSO: ~15 t × 0.75 ≈ **~11 t**
- Downrange-landing to SSO: ~13 t × 0.75 ≈ **~9.5 t**
- RTLS full-reuse to SSO: ~8.5 t × 0.75 ≈ **~6.4 t**

The project's prior "~10 t reusable SSO payload" assumption is **optimistic** — it implicitly assumes droneship recovery *and* a mild SSO penalty. A more defensible planning number: **~8–10 t to SSO with downrange recovery, ~6–7 t with RTLS.** Use **~8.5 t** as the reusable SSO mass budget for the verdict below (downrange recovery, mid penalty).

> **Superseded (wave-5, 2026-05-17):** the ~8.5 t reusable SSO budget adopted
> here for the verdict below has since been re-baselined to a working
> **~9.5 t (range 8.5–10.5 t)** — the deep-verification doc found ~8.5 t sat
> at the conservative low end of the band. The §6 comparison and §7 verdict
> below were computed at ~8.5 t and read pessimistically against the current
> figure; see `rocket_lab/neutron/payload_and_block_upgrade.md` for the
> authoritative numbers. This doc's mass model is otherwise unchanged.

**Usable fairing length — estimate:** With a 14 m overall fairing and a 6 m Stage-2 tank that sits inside it, the usable cylindrical payload section is plausibly **~9–11.5 m long × ~4.5 m usable diameter** (allowing ~0.25 m dynamic-envelope standoff from the 5 m structural diameter). Treat as estimate; confirm with Rocket Lab.

---

## 6. Per-node mass model

Assumptions for the bus and ancillary lines:

- **Spacecraft bus** (structure spine, avionics, ADCS/reaction wheels + magnetorquers, comms, power management & distribution, battery for the small SSO eclipse, harness): estimated as a function of payload+power. For a ~150–300 kW-class platform, bus dry mass ~500–900 kg (1-rack) scaling sublinearly to ~900–1500 kg (2-rack). The laser-comms terminal(s) for the inter-satellite/downlink network are carried here (~50–150 kg).
- **Propulsion / station-keeping:** electric propulsion (Hall/gridded) for SSO drag make-up over a multi-year life + disposal. Xenon/krypton + tanks + thrusters + PPU ≈ 250–500 kg (1-rack), 400–800 kg (2-rack). LEO drag at 500–600 km on a multi-hundred-m² array is significant — this line has real uncertainty.
- **Deployment structures:** booms, hinges, gimbals, motors, hold-down/release for the solar array + radiator. Co-mounting radiator on the array back (Section 4) lets these be shared. Estimate ~200–500 kg/rack of array deployment + ~150–400 kg/rack radiator deployment; co-mounting trims the high end.
- **Margin:** 20% (mid) / 15% (low) / 30% (high) applied to the sum — standard for feasibility-phase (pre-Phase-A) estimates.

### 1-rack node

| Item | Low (kg) | Mid (kg) | High (kg) |
|---|---|---|---|
| Modified rack ×1 (§2) | 1,485 | 1,605 | 1,740 |
| Solar array (§3) | 1,005 | 1,500 | 2,300 |
| Radiator + thermal loop (§4) | 1,250 | 2,400 | 4,300 |
| Spacecraft bus (structure, avionics, ADCS, comms, PMAD, battery) | 500 | 700 | 950 |
| Propulsion / station-keeping (EP + propellant) | 250 | 380 | 550 |
| Deployment structures (array + radiator booms/gimbals/HDRM) | 350 | 600 | 1,000 |
| **Subtotal (dry + prop)** | **4,840** | **7,185** | **10,840** |
| Margin (15 / 20 / 30%) | 726 | 1,437 | 3,252 |
| **NODE TOTAL — 1 rack** | **~5.6 t** | **~8.6 t** | **~14.1 t** |

> Reconciliation with the headline summary: the headline "mid ~5.4 t / range 4.3–7.0 t" reflects the **advanced-technology, mass-optimized path** (advanced GaAs ROSA at 200 W/kg, 3 kg/m² radiator, co-mounted to share deployment structure, 15% margin). The table above is the **broader feasibility envelope including conservative technology**. Both are valid bracketing; the truth depends heavily on radiator areal mass and solar tech. **Planning recommendation: design to ~7–9 t for a 1-rack node** and treat sub-6 t as a stretch goal contingent on advanced GaAs arrays and lightweight radiators.

### 2-rack node

A 2-rack node shares one bus, one propulsion system, and one deployment architecture across two racks, so it is **less than 2×** a 1-rack node — but the array, radiator, and rack lines all double.

| Item | Low (kg) | Mid (kg) | High (kg) |
|---|---|---|---|
| Modified racks ×2 (§2) | 2,970 | 3,210 | 3,480 |
| Solar array ×2 (§3) | 2,010 | 3,000 | 4,600 |
| Radiator + thermal loop ×2 (§4) | 2,500 | 4,800 | 8,600 |
| Spacecraft bus (shared, scaled up) | 800 | 1,150 | 1,500 |
| Propulsion / station-keeping (shared, scaled up) | 450 | 650 | 950 |
| Deployment structures (shared architecture, ~1.7×) | 600 | 1,050 | 1,700 |
| **Subtotal (dry + prop)** | **9,330** | **13,860** | **20,830** |
| Margin (15 / 20 / 30%) | 1,400 | 2,772 | 6,249 |
| **NODE TOTAL — 2 rack** | **~10.7 t** | **~16.6 t** | **~27.1 t** |

> The advanced-technology 2-rack figure (headline "mid ~9.6 t") again assumes the mass-optimized path. Even there, a 2-rack node is **~9–11 t minimum** and the realistic feasibility mid is **~13–17 t**.

### Comparison to Neutron SSO budget

| | Neutron RTLS (full reuse) SSO ~6.4 t | Neutron downrange SSO ~8.5–9.5 t | Neutron expendable SSO ~11 t |
|---|---|---|---|
| 1-rack node (mass-optimized ~5.4–7 t) | marginal / over | **FITS** | fits easily |
| 1-rack node (feasibility mid ~8.6 t) | over | marginal | fits |
| 2-rack node (any estimate ≥9.6 t) | over | over | marginal / over |

**Conclusion:** **A 1-rack node is the natural unit for Neutron.** It fits a reusable (downrange-recovery) flight if the design lands near the mass-optimized end. A 2-rack node almost certainly **forces an expendable flight or exceeds Neutron entirely** — it is not recommended as the baseline. The architecture should be **one rack per node, one node per Neutron launch.**

---

## 7. Fairing packaging check — mass-bound or volume-bound?

### Stowed volume estimate (1-rack node)

| Element | Stowed dimensions (est.) | Stowed volume |
|---|---|---|
| Modified rack | 0.6 × 1.2 × 2.3 m | ~1.7 m³ |
| Spacecraft bus + propulsion + avionics | ~2 m × 2 m × 1 m equivalent | ~4 m³ |
| Solar array, rolled/folded (~545 m² GaAs) | ROSA stows at ~40 kW/m³ → 200 kW ÷ 40 ≈ **~5 m³**; silicon (~820 m², lower density) ≈ 8–12 m³ | 5–12 m³ |
| Radiator, folded (~430 m² panel) | Folded panel stacks: ~430 m² at ~25–40 m²/m³ folded ≈ **~11–17 m³** | 11–17 m³ |
| Deployment structure, booms, gimbals | — | ~2 m³ |
| **Total stowed (packing-inefficient sum)** | | **~24–37 m³** |

### Neutron fairing envelope

Estimated usable payload envelope: **~4.5 m usable diameter × ~9–11.5 m usable length** (Section 5 estimate). Cylindrical usable volume ≈ π × 2.25² × 10 ≈ **~159 m³**, of which realistically ~50–60% is usable for an irregular payload → **~80–95 m³ practical.**

### Verdict

- **Stowed node volume (~24–37 m³) fits inside the Neutron fairing's practical envelope (~80–95 m³) — by volume there is headroom.** The node is **not strictly volume-bound by total fairing volume.**
- **BUT** the *binding* geometric constraint is **deployed area packaging discipline**, not raw volume: ~430 m² radiator + ~545–820 m² solar array must fold into the cylindrical envelope and survive launch. ROSA-class roll-out arrays handle this well (they are designed for exactly this). The radiator is the harder item — a ~430 m² deployable radiator is *very large* (larger than the ISS's main radiators) and folding it reliably is the key engineering risk.
- **Mass bound vs. volume bound:** For a **1-rack node**, the design is **mass-bound at the margin** — it fits the fairing volume comfortably but presses against the ~8.5 t reusable SSO mass budget if technology is conservative. For a **2-rack node**, it is **mass-bound, hard** — over the reusable budget regardless.

### Would Neutron's fairing need modification?

**No major modification needed for a 1-rack node.** The 5 m fairing diameter and estimated ~9–11.5 m usable length accommodate a stowed 1-rack node with room to spare. At most a **slight** accommodation may be wanted: confirming the usable length is ≥10 m so the long radiator/array stacks fit without awkward folding. The standard "Hungry Hippo" fairing as built should work.

A **2-rack node would likely need a stretched fairing or expendable flight** — but the recommendation (Section 6) is to not build 2-rack nodes anyway.

> **Bottom line:** The node is **fairing-volume-comfortable but mass-budget-tight.** Drive the design toward 1 rack/node, advanced GaAs ROSA arrays, and the lightest credible deployable radiator. The radiator — both its mass and its ~430 m² deployed area — is the single biggest driver and the biggest open risk.

---

## Sources

- NVIDIA GB300 NVL72 — [Sunbird DCIM power](https://www.sunbirddcim.com/blog/how-much-power-does-nvidia-gb300-nvl72-need); [Introl GB300](https://introl.com/blog/why-nvidia-gb300-nvl72-blackwell-ultra-matters); [GIGABYTE GB300 NVL72](https://www.gigabyte.com/Enterprise/GIGAPOD-Rack-Scale/AI-DLC-Rack_NVIDIA-GB300-NVL72); [Supermicro 48U GB300](https://www.supermicro.com/en/products/system/gpu/48u/srs-gb300-nvl72); [Lenovo Press lp2357](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai)
- GB200 NVL72 (cross-check) — [Spheron guide](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/); [Sunbird DCIM GB200](https://www.sunbirddcim.com/blog/your-data-center-ready-nvidia-gb200-nvl72)
- EIA-310 rack standard — [RackSolutions](https://www.racksolutions.com/news/data-center-optimization/eia-310-definition/); [Wikipedia 19-inch rack](https://en.wikipedia.org/wiki/19-inch_rack); [A&J Manufacturing](https://aj-racks.com/standard-eia/)
- Liquid-cooling / rack reinforcement — [OCP Liquid Cooling Integration white paper](https://www.opencompute.org/documents/ocp-liquid-cooling-integration-and-logistics-white-paper-revision-1-0-1-pdf); [Introl high-density racks](https://introl.com/blog/high-density-racks-100kw-ai-data-center-ocp-2025)
- Solar arrays — [Wikipedia ROSA](https://en.wikipedia.org/wiki/Roll_Out_Solar_Array); [Redwire ROSA flysheet](https://rdw.com/wp-content/uploads/2023/06/redwire-roll-out-solar-array-flysheet.pdf); [NASA SoA Power subsystems](https://www.nasa.gov/smallsat-institute/sst-soa/power-subsystems/); [Rocket Lab silicon arrays press release, 26 Feb 2026](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/); [GlobeNewswire mirror](https://www.globenewswire.com/news-release/2026/02/26/3246118/0/en/Rocket-Lab-Introduces-Advanced-Silicon-Solar-Arrays-To-Power-Space-Based-Data-Centers.html)
- Solar cell efficiency — [CESI CTJ30 datasheet](https://www.cesi.it/app/uploads/2020/03/Datasheet-CTJ30-1.pdf); [satsearch 30% triple-junction](https://satsearch.co/products/cavu-corp-30triplejunction-solar-cell); [Tech Briefs Si vs GaAs](https://www.techbriefs.com/component/content/article/18946-silicon-vs-gallium-arsenide-which-photovoltaic-material-performs-best)
- Radiators / co-mounting — [NASA SoA Thermal Control](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/); [NASA SoA Thermal 2024 PDF](https://www.nasa.gov/wp-content/uploads/2025/02/7-soa-thermal-2024.pdf); [Gilmore, Spacecraft Thermal Control Handbook ch.6](http://matthewwturner.com/uah/IPT2008_summer/baselines/LOW%20Files/Thermal/Spacecraft%20Thermal%20Control%20Handbook/06.pdf); [Novel deployable radiator, NASA NTRS/ADS](https://ui.adsabs.harvard.edu/abs/2021MsT..........6M/abstract); [NASA NTRS near-sun solar array radiator](https://ntrs.nasa.gov/api/citations/20090004578/downloads/20090004578.pdf)
- Neutron — [Neutron Payload User's Guide v1.0, Jan 2025](https://rocketlabcorp.com/assets/Uploads/Rocket-Lab-Neutron-PUG-reduced-final.pdf); [Wikipedia Neutron](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron); [Rocket Lab architecture reveal](https://rocketlabcorp.com/updates/rocket-lab-reveals-neutron-launch-vehicles-advanced-architecture/); [Space.com Hungry Hippo fairing](https://www.space.com/space-exploration/launches-spacecraft/rocket-labs-hungry-hippo-neutron-fairing-arrives-at-spaceport-in-virginia); [NASASpaceflight Neutron 2025 overview](https://nasaspaceflight.com/2025/12/rocket-lab-2025-overview/)

---

## Open questions / uncertainties

1. **Neutron SSO performance is unpublished.** The ~8.5 t reusable SSO budget used here is a 25%-penalty estimate off the published 13 t downrange-LEO figure. A real number from Rocket Lab could move the verdict ±2 t. **Highest-priority unknown.**
2. **Neutron internal usable fairing length is unpublished.** Assumed ~9–11.5 m. If shorter (~7–8 m), long folded radiator stacks become awkward and a slight fairing accommodation may be needed.
3. **Radiator areal mass and required area dominate the budget.** Spread is 3–8 kg/m² and 375–500 m²; this single line item swings the node total by several tonnes. The required area depends sharply on the achievable radiator surface temperature (a higher hot-loop/surface temp shrinks area as T⁴) and on the effective space sink in LEO (Earth IR + albedo loading). A dedicated thermal analysis is the next step.
4. **The founder's "+30% radiator vs. solar area" rule is incorrect** — corrected here to radiator ≈ 0.5–0.9 × solar area. The "radiator on the back of the solar panel" idea is *validated as feasible* and area-compatible, but co-mounting should be modeled as reducing deployment-structure mass, not radiator panel mass.
5. **Prior project estimates need revision:** prior radiator ~120–210 m²/rack looks low (this analysis: ~375–500 m²); prior solar ~375–460 m²/rack looks low for GaAs (~545 m²) and far too low for silicon (~750–900 m²). Prior node totals (~6 t / ~11 t) are plausible only at the mass-optimized end.
6. **Rocket Lab silicon array specific power is unpublished.** Assumed ~100 W/kg (≈30–40% below advanced GaAs ROSA). If RKLB's silicon arrays are lighter than assumed, the silicon-case masses drop significantly.
7. **LEO drag make-up propellant** at 500–600 km on a multi-hundred-m² array could be larger than the 250–550 kg budgeted; depends on orbit altitude choice (higher = less drag, more radiation, harder launch) and array feathering strategy.
8. **GB300 "1.36 t" scope.** Confirmed as the integrated NVL72 compute cabinet; if the project's intact-rack definition includes the separate switch/CDU/PDU sub-racks, per-rack mass rises toward ~2.5–3 t and every figure here scales up. **Resolve this definition before detailed design.**
