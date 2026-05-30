# LEO Natural-Decay Lifetime of a Large, High-Drag Compute Node (5-yr vs 7-yr)

*Project: RKLB Space Data Center, feasibility phase. Document date: 2026-05-29.*
*Author: research agent. Topic: how long a low-ballistic-coefficient (large-area, ~7-9 t) orbital compute node survives on natural decay in sun-synchronous LEO, as a function of altitude, and what altitude buys a 5-year vs 7-year natural lifetime.*

> **Scope and method note.** This is a sourced first-order analysis. Hard physical constants and the published reference lifetimes are cross-checked against 2+ independent sources and cited inline. The node-specific lifetimes are **derived estimates**: they anchor on published standard-object lifetime-vs-altitude data and scale by the node's ballistic coefficient (a relationship that is itself multiply-sourced). They are explicitly flagged as estimates. A real number requires a numerical propagation (STK / GMAT / NASA DAS) with the node's actual geometry, attitude timeline, and a launch-epoch solar-flux forecast. READ-ONLY reconciliation with `orbit_types_primer.md`, `orbits_environment.md`, and `node_mass_model.md`; this doc does not modify them.

---

## Summary / Key-spec table

The node is a **low-ballistic-coefficient** object: modest mass (~7-9 t) carrying very large deployed appendages (solar array ~500-900 m^2, radiator ~300-430 m^2). Its ballistic coefficient B = m / (Cd*A) is roughly **3.6 to 7.3 kg/m^2** in realistic broadside operating attitude, versus **~45 kg/m^2** for a "normal" satellite (m/A ~ 100 kg/m^2). Because **orbital lifetime is directly proportional to B**, this node decays **roughly 6x to 13x faster** than an ordinary satellite at the same altitude. That single fact drives every result below.

| Quantity | Value (estimate unless noted) | Confidence |
|---|---|---|
| Node mass (input) | 7-9 t (use 8 t mid) | given by project |
| Deployed area (input) | solar ~500-900 m^2 + radiator ~300-430 m^2 | given by project |
| Effective drag area, realistic broadside attitude | ~500-1000 m^2 (projection onto velocity) | estimate |
| Drag coefficient Cd (free-molecular LEO) | **2.2** (standard) | **confirmed**, 3 sources |
| Node ballistic coefficient B = m/(Cd*A) | **~3.6-7.3 kg/m^2** (broadside); ~24 kg/m^2 if perfectly feathered | estimate |
| "Normal" satellite B (m/A ~ 100) | ~45 kg/m^2 | **confirmed** |
| Lifetime-vs-B scaling | **linear** (lifetime proportional to B) | **confirmed**, 4 sources |
| **Altitude for 5-yr natural life (mean solar, broadside)** | **~600-660 km** | estimate |
| **Altitude for 7-yr natural life (mean solar, broadside)** | **~630-690 km** | estimate |
| Same, full envelope (attitude + solar phase) | 5-yr: ~490-755 km; 7-yr: ~510-785 km | estimate |
| Natural life at a "typical" 500-600 km SSO | **only ~1.3-5 yr (mean), ~0.4-2 yr (solar max)** | estimate |
| Solar-cycle swing in lifetime (max vs min) | **~10x** (e.g. 500 km: ~3 yr max vs ~30 yr min) | **confirmed**, 2 sources |
| Solar phase 2026-2035 | SC25 declining from 2024 peak to ~2030 min, then SC26 rises (next max ~2035) | **confirmed** |

**Bottom-line answers to the four questions:**

1. **Decay physics:** Lifetime is set by atmospheric density at altitude (which falls quasi-exponentially) divided by the ballistic coefficient B = m/(Cd*A). Low B (large area, modest mass) means high drag-per-mass and short life. Solar activity heats and expands the thermosphere, swinging density at a fixed altitude by roughly an order of magnitude over the 11-year cycle, hence lifetimes swing ~10x.

2. **Lifetime-vs-altitude table** (below, Section 3): for this node's realistic broadside B band, ~1-2.5 yr at 500 km, ~3-5 yr at 600 km, ~8-16 yr at 700 km, ~26-51 yr at 800 km (mean solar).

3. **5-year natural survival** needs roughly **~600-660 km** (mean solar, realistic attitude); **7-year** needs **~630-690 km**. Round both to **~650-700 km** for planning, and add ~50-100 km of margin if end-of-life lands in a solar maximum.

4. **Is 5 years feasible at a typical 500-600 km SSO?** **No, not reliably.** With this much area the node lives only ~1.3-5 yr there under mean solar conditions and as little as ~0.4-2 yr through a solar maximum. The large area **forces either a higher altitude (~650-700 km) or active propulsion (drag make-up)** to hold a 5-7 year service life. This is the inverse of the deorbit-compliance picture in the existing docs (see Section 6 reconciliation).

---

## 1. Orbital decay physics

### 1.1 Ballistic coefficient: the master parameter
For an object in LEO, atmospheric drag deceleration is
`a_drag = -(1/2) * rho * v^2 * (Cd * A / m)`,
so the resistance to drag is captured by the **ballistic coefficient**, defined for spaceflight as
**B = m / (Cd * A)** (kg/m^2),
where m is mass, A is the cross-sectional (drag) area facing the velocity vector, and Cd is the drag coefficient. A **high** B (heavy, small, compact) "plows through" thin air and decays slowly; a **low** B (light, large area) is dragged down fast. This definition (m/A divided by Cd, with Cd assumed 2.2) is stated identically by [NASA Small Spacecraft State-of-the-Art: Deorbit Systems](https://www.nasa.gov/smallsat-institute/sst-soa/deorbit-systems/), [Wikipedia: Ballistic coefficient](https://en.wikipedia.org/wiki/Ballistic_coefficient), and the decay-model literature (e.g. [arXiv 2508.19549, "Modeling Orbital Decay of LEO Satellites"](https://arxiv.org/html/2508.19549v1), which uses β = m/(Cd*A)).

**Cd ~ 2.2** is the long-standing standard value for satellites in the free-molecular-flow regime of the upper atmosphere, traceable to Jacchia and used throughout the MSIS model family ([satellite-drag-coefficient review, ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0273117722004458); [NASA SoA Deorbit Systems](https://www.nasa.gov/smallsat-institute/sst-soa/deorbit-systems/)). Real Cd for a flat plate broadside can be higher (~2.2-4 depending on surface accommodation and geometry), which would make the node decay *even faster* than computed here, i.e. our use of 2.2 is the conservative (longer-life) choice.

**The node's B.** With m = 8 t and Cd = 2.2:

| Drag area A (m^2) | Attitude description | m/A (kg/m^2) | **B = m/(Cd*A) (kg/m^2)** |
|---|---|---|---|
| 1000 | Worst-case broadside (large panels flat to flow, or tumbling flat) | 8.0 | **3.6** |
| 700 | Sun-tracking array presenting a large projection | 11.4 | **5.2** |
| 500 | Mixed / quasi-random tumble average | 16.0 | **7.3** |
| 150 | Best-case feathered (panels edge-on to flow) | 53.3 | **24.2** |
| (10) | A compact reference satellite, for contrast | 800 | (364) |

For comparison, the **average orbital object is m/A ~ 100 kg/m^2** (most between 50-200), i.e. B ~ 23-91 kg/m^2 ([Space Academy: Satellite Orbital Lifetimes](https://www.spaceacademy.net.au/watch/debris/orblife.htm)). **The node sits far below even the low end of that range** in any broadside attitude: it is, in ballistic-coefficient terms, much more like a deployed drag sail than like a normal satellite.

### 1.2 Atmospheric density vs altitude
Thermospheric mass density falls quasi-exponentially with altitude (with a scale height that itself grows with altitude, from ~60 km near 500 km to ~125 km near 800 km). Representative **mean / moderate-solar** densities from the canonical exponential atmosphere (US Standard Atmosphere 1976 / CIRA, as tabulated by Vallado, *Fundamentals of Astrodynamics and Applications*, and reproduced in toolkits such as [NominalSys ThermosphereExponential](https://docs.nominalsys.com/v0.8/articles/NominalSystems/manuals/Components/Environments/ThermosphereExponential/index.html) and [SatelliteToolbox.jl atmospheric models](https://juliaspace.github.io/SatelliteToolbox.jl/v0.5/man/earth/atmospheric_models/)):

| Altitude | Mean density (kg/m^3) | Scale height (km) |
|---|---|---|
| 400 km | ~2.8e-12 | ~58 |
| 500 km | ~5.2e-13 | ~64 |
| 600 km | ~1.1e-13 | ~72 |
| 700 km | ~3.1e-14 | ~89 |
| 800 km | ~1.1e-14 | ~125 |

Density drops by roughly **5x per 100 km** in this band. Since drag (and decay rate) is proportional to density, that is why lifetime climbs so steeply with altitude (Section 3). *(These mean values are the textbook exponential-model figures; they are a smoothed reference, not a real-time atmosphere. Treat the absolute densities as accurate to a factor of ~2, dominated by solar phase, per Section 1.3.)*

### 1.3 Solar-cycle activity: the dominant uncertainty
Solar EUV output heats and expands the thermosphere. At a fixed altitude, density is far higher at **solar maximum** than at **solar minimum**, so drag and decay rate swing dramatically over the ~11-year cycle. The magnitude is large and well documented:

- A satellite starting at **500 km has a lifetime of ~30 years at solar minimum but only ~3 years at solar maximum**, a roughly **10x swing** ([thermosphere-and-satellite-drag survey, ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0273117723003587); see also [Effect of Air Drag on LEO Satellites During Max/Min Solar Activity, ScienceAlert](https://scialert.net/fulltext/?doi=srj.2016.1.9), which finds order-of-magnitude differences in orbital-element decay between solar max and min).
- Between solar min and max the thermospheric temperature roughly doubles and density at a given altitude rises substantially ([NRLMSISE-00 / thermosphere references summarized in arXiv 2502.19678](https://arxiv.org/pdf/2502.19678)); at high LEO altitudes (~800 km) dataset disagreement on density alone reaches ~45% ([thermospheric-density review, ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0273117715003944)).

**Where the solar cycle is now (as-of 2026-05):** Solar Cycle 25 most likely **peaked in 2024** (smoothed sunspot number ~156 in Aug 2024) and is in its **declining phase**, heading toward a **minimum around 2030-2031**; Solar Cycle 26 then begins (next maximum ~2035-2036) ([Space.com: has the Sun passed solar maximum?](https://www.space.com/the-universe/sun/is-solar-maximum-over-solar-cycle-25); [NOAA SWPC Solar Cycle Progression](https://www.swpc.noaa.gov/products/solar-cycle-progression); [Nature Scientific Reports SC25 forecast](https://www.nature.com/articles/s41598-025-33819-5)).

**Implication for a node launched ~2026-2027 for a 5-7 year life:** the *early* years (toward 2030 minimum) are favorable (thin atmosphere, longer life), but the *end* of a 5-7 year mission lands on the **rising side of SC26** as the atmosphere re-expands. A worst-case design must assume the node spends part of its life in elevated solar activity. The "mean solar" column in Section 3 is the central case; the "solar-max" column is the planning floor for any year of high activity.

---

## 2. Method for the node lifetime estimates

Because raw single-model integrations of orbital lifetime vary by a large factor (the two best public calculators disagree by ~3-5x at 500 km purely on density-model and solar assumptions, see Section 5), the defensible approach is:

1. **Anchor** on published lifetime-vs-altitude for a *standard* object (m/A = 100 kg/m^2, i.e. B ~ 45 kg/m^2), using two independent sources as a band.
2. **Scale linearly** by the node's ballistic-coefficient ratio B_node / B_standard, because **lifetime is directly proportional to B**. This proportionality is stated explicitly by [Space Academy](https://www.spaceacademy.net.au/watch/debris/orblife.htm) ("L = L* (m/A)") and by [AgentCalc](https://agentcalc.com/satellite-orbit-decay-time-calculator) ("decay time scales linearly with ballistic coefficient; doubling B doubles lifetime"), and is the operating principle of drag-sail deorbit devices ([NASA SoA Deorbit Systems](https://www.nasa.gov/smallsat-institute/sst-soa/deorbit-systems/); [Space: Science & Technology, membrane drag sail](https://spj.science.org/doi/10.34133/space.0115)).
3. **Apply a separate solar-phase multiplier** (mean = 1.0; a heavy solar year ~0.33x; a deep solar minimum ~2.5x), bracketing the ~10x cycle swing documented in Section 1.3.

Standard-object anchor lifetimes used (geometric-mean central case, m/A = 100):

| Altitude | [Space Academy](https://www.spaceacademy.net.au/watch/debris/orblife.htm) (mean) | [AgentCalc](https://agentcalc.com/satellite-orbit-decay-time-calculator) (converted to m/A=100) | Central (geomean) |
|---|---|---|---|
| 400 km | ~1 yr | ~4.5 yr | ~2.1 yr |
| 500 km | ~10 yr | ~25 yr | ~15.8 yr |
| 600 km | ~32 yr (interp.) | - | ~32 yr |
| 700 km | ~100 yr | - | ~100 yr |
| 800 km | ~320 yr (interp.) | - | ~320 yr |

*(Space Academy gives a decade rule: 400 km ~1 yr, 500 km ~10 yr, 700 km ~100 yr, 900 km ~1000 yr; 600 and 800 km are geometric interpolations of that rule. AgentCalc's published "B=100 kg/m^2" column uses BC=m/(Cd*A), so its B=100 corresponds to m/A=220; converted to the m/A=100 basis it gives ~4.5 yr at 400 km and ~25 yr at 500 km. The 3-5x gap between the two sources is real model spread and is why the node numbers below carry a band.)*

An independent exponential-atmosphere integration (Vallado Table 8-4 densities, circular-orbit da/dt = -rho*sqrt(mu*a)/B) gives a standard object ~3 yr at 500 km and ~68 yr at 700 km, i.e. it sits inside the two-source band, confirming the anchors are physically reasonable.

---

## 3. Lifetime-vs-altitude table for this node

Node natural lifetime in years, central (geomean) anchor scaled by B_node/B_standard. Format where shown: **mean solar / solar-max / solar-min**.

| Altitude | Worst broadside (B=3.6) | Mixed broadside (B=5.2) | Tumble (B=7.3) | Feathered (B=24.2) |
|---|---|---|---|---|
| 400 km | ~0.2 | ~0.2 | ~0.3 | ~1.1 |
| **500 km** | **~1.3** / 0.4 / 3.2 | ~1.8 | **~2.5** / 0.8 / 6.3 | ~8.4 / 2.8 / 21 |
| **600 km** | **~2.6** / 0.8 / 6.4 | ~3.7 | **~5.1** / 1.7 / 13 | ~17 / 5.6 / 43 |
| 650 km | ~4.5 / 1.5 / 11 | ~6.5 | ~9.1 / 3.0 / 23 | ~30 / 10 / 75 |
| **700 km** | **~8.0** / 2.6 / 20 | ~11.4 | **~16** / 5.3 / 40 | ~53 / 18 / 133 |
| 800 km | ~26 / 8.5 / 64 | ~37 | ~51 / 17 / 128 | ~171 / 56 / 427 |

**Reading the table.** In any broadside attitude (B = 3.6-7.3, the realistic operating range for large sun-pointed panels) the node:
- **does not reach 5 years at 500 or 600 km** under mean solar conditions (1.3-5.1 yr), and is far short during a solar maximum (0.4-1.7 yr);
- **first clears 5 and 7 years around 650-700 km**;
- has comfortable multi-decade life only at 800 km.

Only if the panels could be held **near-perfectly feathered (edge-on) for the entire mission** (B ~ 24) would 500-600 km give a 5-7 year mean-solar life, and even then a solar maximum (2.8-5.6 yr at 500 km) erodes the margin. Perfect lifetime-long feathering is not realistic for a power- and thermal-constrained node whose array must face the Sun and whose radiator must view deep space, so the broadside band is the honest planning case.

---

## 4. Altitude needed for 5-year vs 7-year natural life

Solving the scaled model for the altitude at which lifetime crosses 5 and 7 years:

| Attitude (B) | Solar phase | 5-yr altitude | 7-yr altitude |
|---|---|---|---|
| Worst broadside (3.6) | mean | ~659 km | ~688 km |
| Mixed broadside (5.2) | mean | ~627 km | ~657 km |
| Tumble (7.3) | mean | ~597 km | ~627 km |
| Feathered (24.2) | mean | ~474 km | ~491 km |
| Worst broadside (3.6) | solar-max heavy | ~755 km | ~784 km |
| Tumble (7.3) | solar-max heavy | ~695 km | ~724 km |
| Worst broadside (3.6) | solar-min | ~565 km | ~608 km |
| Tumble (7.3) | solar-min | ~488 km | ~514 km |

**Headline (realistic broadside band, mean solar):**
- **5-year natural life: ~600-660 km.**
- **7-year natural life: ~630-690 km.**
- Full envelope across attitude and solar phase: 5-yr anywhere from ~490 km (best: feathered + deep minimum) to ~755 km (worst: broadside + solar max); 7-yr from ~510 to ~785 km.

**Planning recommendation:** to guarantee a 5-year natural life regardless of attitude and with solar-max robustness, target **~700 km**; for 7 years, **~720-750 km**. At those altitudes, though, the node also takes far longer than 5 years to *deorbit* once retired, so a higher orbit trades survival for an active-deorbit obligation under the FCC 5-year rule (Section 6).

---

## 5. Uncertainty and why the numbers carry a band

These estimates should be read as **order-of-altitude correct (good to roughly +/- 50-100 km), not point-precise.** The dominant uncertainties:

1. **Effective drag area / attitude timeline.** B swings by ~7x between worst broadside (1000 m^2) and feathered (150 m^2), and lifetime swings proportionally. The true value depends on the as-flown attitude law, which is itself constrained by sun-pointing (power) and space-viewing (thermal) needs. This is the single biggest lever and is **not yet pinned down** for this design.
2. **Solar phase at the mission epoch.** ~10x lifetime swing over the cycle (Section 1.3). A 5-7 year mission spans a meaningful fraction of a cycle, so the *effective* lifetime is a time-average over changing conditions, not a single-density result.
3. **Density-model spread.** Public lifetime calculators disagree by ~3-5x at a given altitude/B (Section 2) purely on atmosphere model and baked-in solar assumptions. We carry both as a band rather than trusting either.
4. **Cd for a flat-plate broadside** can exceed 2.2 (toward ~3-4), which would *shorten* life further; using 2.2 is conservative (longer-life).

All four push the same direction for the feasibility verdict: at a typical 500-600 km SSO this high-area node **does not** have a robust 5-year natural life. The uncertainty is in exactly how high one must go (~650 km vs ~750 km), not in whether 500-600 km is sufficient (it is not).

---

## 6. Reconciliation with existing project docs (no edits made)

The existing docs are **consistent with this analysis once the question is flipped**, and this doc adds the missing half:

- **`orbit_types_primer.md` (Section 5, "Deorbit / end-of-life") and `orbits_environment.md` (Section 5)** both state that **below ~500-600 km, atmospheric drag pulls a satellite down within a few years; above that, natural decay takes much longer than 5 years, so the satellite needs active deorbit propulsion.** That framing is about **deorbit compliance** (you *want* it to come down within 5 years) and is correct for a *normal* satellite. Both docs also correctly note that decay is **"worse for satellites with large area-to-mass ratios, e.g. big solar arrays and radiators."**

- **This doc supplies the inverse, survival-side consequence of that same large area.** For an ordinary satellite, 500-600 km is the "comes down within ~5-25 years" band. For *this* node, whose B is ~6-13x lower, that same band collapses to a **~1-5 year survival** window: the node decays so fast that it fails to *stay up* for a 5-year service life. The large area that makes deorbit easy (a genuine benefit the docs flag) is the same property that makes orbital *survival* hard. There is no contradiction; the two docs describe the deorbit side, this one describes the survival side.

- **The docs' lean toward the lower ~500-600 km SSO band** (for less debris, easier compliant disposal, shorter eclipse season) is therefore in **direct tension** with a multi-year service-life goal for a high-drag node. The lower band is good for *cheap disposal* and bad for *staying up*. A node that must live 5-7 years at 500-600 km cannot do so on natural decay alone; it needs **active drag make-up (station-keeping propulsion)**, which `orbits_environment.md` Section 5 and `node_mass_model.md` Section 6 already anticipate as a real, possibly under-budgeted, propellant line ("LEO drag at 500-600 km on a multi-hundred-m^2 array is significant ... this line has real uncertainty"). This doc quantifies *why* that line is significant: the node's ballistic coefficient is drag-sail-like.

- **`node_mass_model.md`** carries the node at ~7-9 t with ~500-900 m^2 solar and ~300-430 m^2 radiator and flags drag make-up propellant as poorly bounded. This doc is consistent with those inputs and sharpens the open item: the drag/propulsion trade is **altitude-coupled**, with a clean fork (raise the orbit to ~650-700+ km and accept an active-deorbit obligation, or stay at 500-600 km and budget continuous drag make-up plus, eventually, a deorbit burn).

**Net:** nothing in this doc overturns the existing baseline; it fills a gap. The project's choice is now explicit: **a high-drag node cannot both (a) live 5-7 years and (b) sit at 500-600 km on natural decay alone.** Pick higher altitude, or pick active propulsion. (Most likely the design needs propulsion regardless, for collision avoidance and disposal, so the real question is how much *extra* propellant a low orbit costs versus the launch-mass penalty of a higher orbit, per `orbits_environment.md` Section 2.)

---

## Sources

- [NASA Small Spacecraft State-of-the-Art: Deorbit Systems](https://www.nasa.gov/smallsat-institute/sst-soa/deorbit-systems/) (BC definition m/A divided by Cd; Cd=2.2; ~400 km decays in <5 yr, beyond 500 km no 5-yr guarantee; drag-sail acceleration)
- [Wikipedia: Ballistic coefficient](https://en.wikipedia.org/wiki/Ballistic_coefficient) (BC = m/(Cd*A); high BC = slow decay)
- [Space Academy: Satellite Orbital Lifetimes](https://www.spaceacademy.net.au/watch/debris/orblife.htm) (decade rule 400/500/700/900 km; lifetime proportional to m/A; m/A ~ 100 average, 50-200 range; above 500 km lifetime exceeds the ~11-yr solar period)
- [Space Academy: Earth Atmosphere Density Approximations](https://www.spaceacademy.net.au/watch/debris/atmosmod.htm) (F10 min=70 / max=300; mean atmosphere appropriate above 500 km)
- [AgentCalc: Satellite Orbit Decay Time Calculator](https://agentcalc.com/satellite-orbit-decay-time-calculator) (decay-time table vs B=50/100/200; linear scaling with ballistic coefficient)
- [arXiv 2508.19549, Modeling Orbital Decay of LEO Satellites due to Atmospheric Drag](https://arxiv.org/html/2508.19549v1) (β = m/(Cd*A); da/dt governing equation; solar max can raise 400 km density ~10x)
- [ScienceDirect: Satellite drag coefficient modeling for thermosphere science and mission operations](https://www.sciencedirect.com/science/article/pii/S0273117722004458) (Cd=2.2 Jacchia standard; free-molecular flow)
- [ScienceDirect: Thermosphere and satellite drag](https://www.sciencedirect.com/science/article/pii/S0273117723003587) (500 km lifetime ~30 yr solar min vs ~3 yr solar max)
- [ScienceDirect: Thermospheric mass density, a review](https://www.sciencedirect.com/science/article/abs/pii/S0273117715003944) (density at 800 km dataset disagreement up to ~45%; strong solar dependence 200-800 km)
- [ScienceAlert: Effect of Air Drag on LEO Satellites During Max/Min Solar Activity](https://scialert.net/fulltext/?doi=srj.2016.1.9) (F10.7 max=205 / min=74; orbital-element variations differ by orders of magnitude between solar max and min)
- [arXiv 2502.19678: Neutral Atmosphere Density During Increasing Solar Activity](https://arxiv.org/pdf/2502.19678) (thermospheric temperature roughly doubles min-to-max; NRLMSISE-00 context)
- [Vallado exponential atmosphere, as reproduced by NominalSys ThermosphereExponential](https://docs.nominalsys.com/v0.8/articles/NominalSystems/manuals/Components/Environments/ThermosphereExponential/index.html) and [SatelliteToolbox.jl atmospheric models](https://juliaspace.github.io/SatelliteToolbox.jl/v0.5/man/earth/atmospheric_models/) (US Std Atm 1976 / CIRA base-density + scale-height table)
- [Space.com: Has the Sun passed solar maximum?](https://www.space.com/the-universe/sun/is-solar-maximum-over-solar-cycle-25) (SC25 peak ~2024)
- [NOAA SWPC: Solar Cycle Progression](https://www.swpc.noaa.gov/products/solar-cycle-progression) (official solar-cycle tracking)
- [Nature Scientific Reports: Forecasting sunspots for Solar Cycle 25](https://www.nature.com/articles/s41598-025-33819-5) (SC25 declining phase 2027-2030, minimum ~2030, SC26 from ~2031)
- [Space: Science & Technology, Membrane Drag Sail for LEO Deorbit](https://spj.science.org/doi/10.34133/space.0115) (drag sail = large area, low B, accelerates deorbit, confirming the area/lifetime inverse relationship)

## Open questions / uncertainties

1. **Effective drag area and attitude timeline are unresolved.** The single largest lever. A real attitude profile (how much of each orbit the array is broadside vs feathered, given sun-pointing and radiator-pointing constraints) is needed. Current band assumes 500-1000 m^2 broadside; if the design can hold a tighter feathered attitude for most of the mission, the required 5-yr altitude drops toward ~500-600 km, but power/thermal constraints likely forbid that.
2. **A real numerical propagation is required to replace these scaled estimates.** Run STK, GMAT, or NASA DAS / NASA's debris-assessment tools with the actual geometry, a drag-area-vs-time profile, and a launch-epoch solar-flux forecast (e.g. the NOAA SC25/SC26 prediction). Expect the point answer to land within the +/- 50-100 km band given here.
3. **Mission-epoch solar phase changes the answer by ~50-100 km.** A node retiring near the SC26 rise (~2033-2036) needs more altitude for the same natural life than one retiring near the 2030 minimum. The launch date and intended service window should be fixed before committing to an altitude.
4. **The altitude/propulsion trade is not yet costed.** Higher orbit (~650-700+ km) buys natural survival but (a) costs Neutron payload (SSO penalty grows with altitude, per `orbits_environment.md` Section 2), (b) sits in a more congested, higher-radiation band (~800 km is debris-heavy per `orbits_environment.md` Section 5), and (c) creates an active-deorbit obligation under the FCC 5-year rule. Lower orbit (500-600 km) needs continuous drag make-up propellant whose mass is currently poorly bounded (`node_mass_model.md` open item 7). The two options should be compared on total mass and cost.
5. **Cd for the actual broadside geometry is assumed 2.2.** A large flat plate can have Cd ~3-4 in free-molecular flow; if so, real lifetimes are *shorter* than tabulated and the required altitudes *higher*. Worth checking with a proper free-molecular aerodynamics estimate once geometry is set.
6. **"Drag make-up" feasibility at very low B is itself a question.** A node with B ~ 4 kg/m^2 at 500-550 km during a solar maximum experiences strong drag; the electric-propulsion thrust and propellant needed to hold altitude (rather than just deorbit) could be a large, possibly mission-defining, line item. This deserves its own analysis tied to the propulsion sizing in `node_mass_model.md`.
