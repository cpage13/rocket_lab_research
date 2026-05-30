# Higher Orbit vs Station-Keeping Low: Lifetime, Delta-v, and Side Effects

*Orbital trade study. Status: draft. Date: 2026-05-29.*
*All hard numbers cross-checked against 2+ independent sources where possible; estimates explicitly labeled. No em-dashes used.*

## Summary / Verdict

The project baseline is a large-area compute node (~7 to 9 t, with ~430 m² of radiator plus ~545 to 820 m² of solar array) in a low dawn-dusk SSO (~500 to 600 km), where it either decays or must burn propellant to hold altitude. This doc evaluates the alternative: **raise the node once to an altitude where atmospheric drag is negligible for 5 to 7-plus years, so no continuous station-keeping is needed.**

**Finding: raising the orbit is energetically cheap but does not buy a free 7-year life. It trades a continuous, cheap drag-makeup task for two new, harder problems: a rising radiation dose and a regulatory disposal obligation that gets heavier with altitude.**

- **Altitude for a 7-year natural life (this node):** roughly **800 to 900 km**, NOT the ~700 km that a normal satellite would need. The node's huge deployed area gives it an unusually **low ballistic coefficient** (estimated m/A ~20 to 40 kg/m², versus ~50 to 130 for a typical satellite), so it decays faster at any altitude and must fly **~150 to 250 km higher** than a compact satellite to reach the same lifetime (ESTIMATE; see Section 1).
- **Delta-v to raise** from 500 to 600 km up to ~800 to 1000 km is only **~160 to 300 m/s** (confirmed by Hohmann calculation and an independent source). With electric propulsion (Isp ~1500 to 2500 s) the **propellant is ~80 to 200 kg on an 8 t node (1 to 3% of mass)**, plus a months-long spiral. Delta-v is NOT the binding constraint.
- **The binding side effect is RADIATION.** Going from ~500 to 600 km up to ~800 to 1400 km moves the node up into the lower edge of the inner proton belt and increases time-averaged trapped-proton exposure. Total ionizing dose (TID) behind a few mm of aluminium rises from roughly **~0.3 to 3 krad(Si)/yr at 500 to 600 km** toward the **high single digits or low tens of krad(Si)/yr by ~1200 to 1400 km** (ESTIMATE for the upper band; the 500 km polar anchor of 333 rad/yr behind 5 mm Al is sourced). More importantly for GPU-class silicon, the **single-event-upset (SEU) rate scales with the trapped-proton flux**, which is exactly what climbs with altitude, and is **not removable by shielding**.
- **The second binding constraint is end-of-life disposal.** Above ~600 to 650 km the node can no longer satisfy the US **5-year deorbit rule** by natural decay, so it MUST carry a deorbit capability regardless. A controlled deorbit burn costs **~190 m/s from 800 km up to ~330 m/s from 1400 km** (~150 to 320 kg propellant): cheap in delta-v, but it converts "let drag do it for free" into "carry and reserve a disposal system," and it gets monotonically heavier with altitude.

> **Bottom line:** Going higher is a viable engineering path to a 7-year life and the delta-v cost is small, but it is **not free**: it spends the savings on extra shielding mass, harder SEU mitigation, and a mandatory deorbit system. The **binding side effect is radiation** (TID is manageable with shielding mass; the SEU rate is the real concern for GPUs). Net lean: a **modest raise to ~700 to 800 km** is the most defensible compromise (multi-year life with only a small radiation penalty), but the project's existing preference for the **low ~500 to 600 km band with light station-keeping** remains competitive because it keeps both radiation and disposal easy. The choice is a station-keeping-propellant vs radiation-plus-disposal trade, not a clear win for "go higher."

---

## Key-spec table

| Quantity | Low band (baseline) ~500 to 600 km | Mid raise ~700 to 800 km | High raise ~1000 to 1400 km | Confidence |
|---|---|---|---|---|
| Natural lifetime, **typical** satellite (m/A ~50 to 130) | ~10 to 25-plus yr | ~25 to 100-plus yr | centuries | sourced (table spread is large) |
| Natural lifetime, **this node** (m/A ~20 to 40, large area) | ~3 to 10 yr | ~7 to 30 yr | many decades-plus | ESTIMATE (scaled by ballistic coefficient) |
| Station-keeping needed for 7-yr life? | **Yes** (drag makeup) | Marginal / no | **No** | derived |
| Delta-v to raise from ~500 km | n/a (baseline) | **~160 m/s** (to 800) | **~260 to 450 m/s** (1000 to 1400) | confirmed (Hohmann) |
| EP propellant to raise (8 t node, Isp 1500 to 2500 s) | n/a | **~50 to 110 kg** | **~80 to 240 kg** | confirmed (rocket eqn) |
| TID behind ~5 mm Al | **~0.3 to 3 krad(Si)/yr** | ~1 to 5 krad(Si)/yr | **~hi-single-digit to low-tens krad/yr** | mixed (low band sourced; high band ESTIMATE) |
| SEU rate trend (trapped protons) | baseline (SAA passes) | higher | **highest in LEO band** | sourced (qualitative) |
| Controlled-deorbit burn delta-v (to 120 km perigee) | ~110 to 135 m/s | ~190 m/s | **~240 to 330 m/s** | confirmed (calc) |
| Disposal compliance under 5-yr rule | natural decay can help | needs active deorbit | **needs active deorbit, harder** | sourced |
| Collision / congestion | moderate | **800 km is a congested band** | lower density but no drag cleansing | sourced (qualitative) |

---

## 1. Altitude for a 7-year natural life

### The textbook altitude-lifetime curve (typical satellite)

For a satellite of ordinary shape, natural orbital lifetime rises extremely steeply with altitude, because thermospheric density falls roughly exponentially. A widely used rough guide for a circular orbit ([Space Academy: Satellite Orbital Lifetimes](https://www.spaceacademy.net.au/watch/debris/orblife.htm)):

| Altitude | Lifetime (typical object) |
|---|---|
| 200 km | ~1 day |
| 300 km | ~1 month |
| 400 km | ~1 year |
| 500 km | ~10 years |
| 700 km | ~100 years |
| 900 km | ~1000 years |

Independent sources give the same shape but with a wide numeric spread driven by the solar cycle and the ballistic coefficient: an arXiv 2025 decay study states "at 200 km, satellites typically decay within weeks, while at 800 to 1000 km, lifetimes extend to several decades" and "above 800 km may survive for centuries" ([arXiv 2508.19549, 2025](https://arxiv.org/html/2508.19549v2)). ESA's debris-mitigation guidance puts the practical break near 600 km: "for a broad range of typical spacecraft having initial circular orbital altitudes below about 600 km, no specific end of life manoeuvre is required, because their remaining lifetime is below 15 years" and "the remaining lifetime will be limited to 25 years ... at about 600 km" ([ESA SP-1301 Space Debris Mitigation](https://www.esa.int/esapub/sp/sp1301/sp1301.pdf)). A simple calculator puts a typical satellite (B = 50 kg/m²) at ">25 years" already at 500 km ([AgentCalc orbit-decay calculator](https://agentcalc.com/satellite-orbit-decay-time-calculator)).

**Read across sources:** for a *typical* satellite, a 7-year-plus natural life (drag negligible) is reached somewhere around **600 to 700 km**, and decades-to-centuries by 800 km. The factor-of-several disagreement between sources is real and is dominated by solar activity (atmospheric density at a given altitude can change by an order of magnitude over a solar cycle) and by the satellite's ballistic coefficient ([Space Academy](https://www.spaceacademy.net.au/watch/debris/orblife.htm), [arXiv 2508.19549](https://arxiv.org/html/2508.19549v2)).

### The wrinkle this project must apply: a LOW ballistic coefficient

Orbital lifetime scales **linearly with the ballistic coefficient** B = m / (C_d · A), i.e. with the mass-to-area ratio m/A. Space Academy states the normalization directly: "L = L* (m/A)", so "a spacecraft with m/A = 200 would have double the lifetime of one with m/A = 100" ([Space Academy](https://www.spaceacademy.net.au/watch/debris/orblife.htm)). Lower B (large area, low mass) means **faster decay** ([arXiv 2508.19549](https://arxiv.org/html/2508.19549v2), [Hou USRA drag-sail paper](https://www.hou.usra.edu/meetings/orbitaldebris2019/orbital2019paper/pdf/6020.pdf)).

The compute node is at the **low-B extreme**. From `node_mass_model.md` and `orbits_environment.md`: mass ~7 to 9 t, with ~430 m² radiator plus ~545 to 820 m² solar array (~1000 to 1250 m² of physical surface). The drag-relevant figure is the time-averaged projected ram area, which depends on attitude; even with arrays feathered edge-on, a realistic time-averaged drag area is on the order of ~100 to 400 m². That gives:

| Mass | Avg drag area | m/A (kg/m²) |
|---|---|---|
| 8,000 kg | 100 m² (well-feathered) | ~80 |
| 8,000 kg | 200 m² | ~40 |
| 8,000 kg | 400 m² (poorly feathered) | ~20 |

A "typical" satellite, the implicit basis of the lifetime tables, sits around **m/A ~50 to 130 kg/m²** (e.g. a 100 kg, 0.5 m² satellite has B ~90; ESA debris with A/m = 0.01 m²/kg is m/A = 100) ([NASA Deorbit Systems SOA](https://www.nasa.gov/smallsat-institute/sst-soa/deorbit-systems/), [ESA SP-1301](https://www.esa.int/esapub/sp/sp1301/sp1301.pdf)). So the node's m/A is roughly **0.3 to 0.8x** that of a typical satellite, and since lifetime scales linearly with m/A, **its natural lifetime at any altitude is roughly one-third to four-fifths of the table value.**

To recover a given lifetime, a low-B object must fly higher. Compressing the steep curve by a factor of ~1.5 to 3x in lifetime corresponds to climbing roughly **~150 to 250 km** higher (ESTIMATE; derived from the linear m/A scaling applied to the King-Hele-type curves above, not from a node-specific propagation):

> **Altitude band for a 7-year natural life for THIS node: ~800 to 900 km (ESTIMATE).** A compact satellite gets 7-plus years at ~600 to 700 km, but the large-area node must climb to roughly 800 to 900 km to clear 7 years robustly across the solar cycle (target the upper end to survive a solar maximum, which thins out lifetimes). Below ~700 km the node will likely still need at least light drag makeup to guarantee 7 years; above ~900 km the node is effectively permanent.

This is the single most important reconciliation with the existing docs: `orbits_environment.md` notes that "above ~800 km, natural decay takes far longer than 5 years" for a generic satellite, but it does **not** carry the low-ballistic-coefficient correction. For this node specifically, the "drag negligible" altitude is pushed up, deeper into the radiation and disposal problem zones below.

---

## 2. Delta-v, EP time, and propellant to raise the orbit

### Delta-v (confirmed)

Raising a circular orbit is a small two-burn (Hohmann) maneuver. Computed values (mu = 398,600 km³/s², R_e = 6378 km), cross-checked against an independent source that gives 500 to 1000 km = ~257 m/s ([Brainly worked Hohmann example](https://brainly.com/question/38269135); [Wikipedia: Hohmann transfer orbit](https://en.wikipedia.org/wiki/Hohmann_transfer_orbit)):

| Raise | Delta-v (this calc) |
|---|---|
| 500 to 800 km | ~161 m/s |
| 500 to 1000 km | ~262 m/s |
| 500 to 1200 km | ~360 m/s |
| 500 to 1400 km | ~454 m/s |
| 600 to 800 km | ~106 m/s |
| 600 to 1000 km | ~208 m/s |

These are tiny compared with the ~9.4 km/s already spent reaching orbit ([Wikipedia: Delta-v budget](https://en.wikipedia.org/wiki/Delta-v_budget)).

### Propellant mass (confirmed, small)

With electric propulsion (Hall thrusters at Isp ~1500 to 2500 s) ([Busek Hall thrusters](https://www.busek.com/hall-thrusters), [Wikipedia: Hall-effect thruster](https://en.wikipedia.org/wiki/Hall-effect_thruster)), the rocket equation (delta-v = Isp · g0 · ln(m0/mf), g0 = 9.807 m/s²) gives a propellant fraction of only **~1 to 3%** for these delta-v values:

| Raise (delta-v) | Propellant fraction | Propellant on an 8 t node |
|---|---|---|
| to 800 km (~160 m/s) | ~0.6 to 1.1% | ~50 to 90 kg |
| to 1000 km (~260 m/s) | ~1.1 to 1.8% | ~85 to 145 kg |
| to 1400 km (~450 m/s) | ~1.8 to 3.0% | ~145 to 240 kg |

For comparison, the node already budgets ~250 to 500 kg of EP plus propellant for *multi-year* drag makeup and collision avoidance (`node_mass_model.md` Section 6). **The one-time raise is smaller than the station-keeping budget it would replace.** The mass implication of raising is therefore favorable on its own; the cost is elsewhere (Section 3).

### Transfer time (the real EP cost of raising)

EP gives high Isp but low thrust, so orbit raising is a slow, many-revolution spiral. The literature example most comparable in scale is a Hall-thruster **LEO-to-MEO transfer of ~192 days** ([AIAA orbit-transfer analysis via search summary](https://pepl.engin.umich.edu/pdf/AIAA-96-2973.pdf); [Busek](https://www.busek.com/hall-thrusters)). A 500-to-1000 km raise is a far smaller energy step than LEO-to-MEO, so the spiral is shorter, but for a ~8 t platform with limited array-to-thrust it is still plausibly **weeks to a few months** (ESTIMATE; depends on installed EP power and thrust). During the spiral the node climbs through progressively higher trapped-proton flux, accumulating extra dose en route, and is not yet on-station earning revenue.

---

## 3. Side effects over a 5 to 7-year life

### 3.1 Radiation: TID and SEU both rise with altitude (the binding side effect)

**Why it rises.** In LEO the dose is "caused almost entirely by electrons and energetic protons trapped in the inner radiation belt" ([ASU TID notes, via search](http://holbert.faculty.asu.edu/eee560/tiondose.html); [ScienceDirect: Inner Radiation Belt](https://www.sciencedirect.com/topics/physics-and-astronomy/inner-radiation-belt)). The **inner Van Allen belt** is dominated by protons of 10 to 50-plus MeV and extends from roughly **600 to 1000 km up to ~6,000 to 12,000 km**, dipping lowest at the **South Atlantic Anomaly (SAA)** ([Wikipedia: Van Allen radiation belt](https://en.wikipedia.org/wiki/Van_Allen_radiation_belt), [ScienceDirect: Inner Radiation Belt](https://www.sciencedirect.com/topics/physics-and-astronomy/inner-radiation-belt)). For a high-inclination orbit "the radiation dose is mainly due to inner belt protons, which increases with altitude because of the pitch angle distribution of the trapped protons" ([Wikipedia: Van Allen radiation belt](https://en.wikipedia.org/wiki/Van_Allen_radiation_belt) and search syntheses). A low SSO at 500 to 600 km only clips the SAA on some passes; raising to 800 to 1400 km spends progressively more time inside the belt's lower edge.

**Anchored TID numbers (behind 5 mm Al, SHIELDOSE-2).** A NASA Ames radiation trade study gives directly comparable, model-verified figures ([NASA/TM-20220011775, Mission Radiation Environment Modeling, Aug 2022](https://ntrs.nasa.gov/api/citations/20220011775/downloads/Mission_Radiation_Modeling_STI.pdf)):

| Orbit (5 mm Al) | Total TID/yr | Note |
|---|---|---|
| LEO Zero (500 km, 0 deg) | ~136 rad | magnetosphere shields almost everything |
| LEO ISS (500 km, 51 deg) | ~430 rad | crosses SAA ~9 of 15 orbits |
| **LEO Polar (500 km, 89 deg)** | **~333 rad (~0.33 krad)** | closest analog to our high-inclination SSO |
| GEO (35,786 km) | ~5,930 rad (~5.9 krad) | outside belts, solar + outer electrons |
| GTO (crosses belts) | ~59,630 rad (~60 krad) | "by far the worst" (double belt dip/day) |

This NASA polar-500 km figure (~0.33 krad/yr behind 5 mm Al) is consistent with, and a useful lower anchor for, the project's existing **~1 to 3 krad(Si)/yr behind a few mm at 500 to 800 km SSO** (`orbits_environment.md`, which cites ~1.87 krad/yr at 800 km), and with an independent rule of thumb of **~4 krad(Si)/yr for low (200 to 1000 km), high-inclination (>28 deg) orbits** (search synthesis of LEO radiation literature). Device-level polar measurements of **~1 to 1.5 rad/day (~365 to 550 rad/yr)** corroborate the same band (search synthesis; [ResearchGate: TID/DDD for various orbits](https://www.researchgate.net/publication/235692893_Studying_the_Total_Ionizing_Dose_and_Displacement_Damage_Dose_effects_for_various_orbital_trajectories)).

**Trend with altitude.** Combining the belt physics with the NASA "annual dose vs altitude/orbit" curve for a polar orbit (Koontz/ESA, reproduced in the NASA TM) ([NASA/TM-20220011775](https://ntrs.nasa.gov/api/citations/20220011775/downloads/Mission_Radiation_Modeling_STI.pdf)): TID for a polar/SSO orbit climbs steeply from the ~0.3 to 3 krad(Si)/yr band at 500 to 800 km as altitude increases through the inner belt, reaching roughly the **high-single-digits to low-tens of krad(Si)/yr by ~1200 to 1400 km** (ESTIMATE; the project should run SPENVIS/SHIELDOSE-2 at the specific candidate altitude to replace this band). The jump from ~600 km to ~1400 km is therefore on the order of a **~3 to 30x increase in dose rate**, depending on exactly how high one goes and the solar-cycle phase (ESTIMATE).

**Implication for GPU-class electronics.**
- **TID is manageable with shielding mass.** Commercial silicon survives tens of krad TID, and a few mm of aluminium already holds a low SSO under ~1 to 3 krad/yr. At ~800 km a 7-year mission is ~7 to 20 krad: survivable with modest spot-shielding. At ~1200 to 1400 km a 7-year mission could be ~50 to 100-plus krad, which begins to require either rad-tolerant parts or meaningfully more shielding mass. Critically, **SHIELDOSE-2 physics shows shielding effectiveness "bottoms out" beyond ~5 mm Al** (the beam hardens and the proton contribution stops falling), so you cannot simply pile on aluminium to defeat a belt-edge proton environment ([NASA/TM-20220011775](https://ntrs.nasa.gov/api/citations/20220011775/downloads/Mission_Radiation_Modeling_STI.pdf)). Past ~5 mm you get only ~2x more reduction for 20 mm, so shielding mass grows fast for diminishing returns.
- **SEU rate is the real concern and it tracks the proton flux that climbs with altitude.** The NASA TM is explicit that for LEO, "trapped particles dominate," and that the inner-belt protons (10 to 50 MeV) are precisely in "the range that produces effects in semiconductors" ([NASA/TM-20220011775](https://ntrs.nasa.gov/api/citations/20220011775/downloads/Mission_Radiation_Modeling_STI.pdf)). Because the SEU rate is driven by the *instantaneous proton flux* (not accumulated dose), and that flux rises with altitude into the belt, **going higher directly increases the bit-flip / single-event-functional-interrupt rate on dense GPU/HBM memory.** This is consistent with the project's existing treatment in `orbits_environment.md`: SEU "is not solved by shielding" and must be handled architecturally (ECC on all memory, scrubbing, checkpoint/restart, redundancy). Going higher makes that architectural budget harder: more scrubbing, more frequent recompute, more redundancy overhead, and a higher floor on uncorrectable-error rate. The NASA TM notes ECC typically buys ~10^5 reduction in effective upset rate and shielding ~10 to 20x, but also warns that thicker shielding generates **secondary particles** that can *raise* upset rates ([NASA/TM-20220011775](https://ntrs.nasa.gov/api/citations/20220011775/downloads/Mission_Radiation_Modeling_STI.pdf)).

> **Radiation verdict:** TID is a manageable shielding-mass line that grows uncomfortable only toward the top of the band (~1200 to 1400 km). The harder, less-defeatable problem is the **rising SEU rate from inner-belt protons**, which shielding cannot fix and which directly degrades GPU compute reliability. **Radiation is the binding side effect of going higher**, and it argues for staying at the LOW end of any "drag-negligible" altitude (i.e. ~700 to 800 km, not ~1200 to 1400 km).

### 3.2 Communications: modest path-loss and latency increase

Raising from ~550 km to ~1000 to 1400 km roughly doubles to triples the slant range. Free-space path loss scales as distance squared, so the link budget worsens by **~6 to 10 dB** (ESTIMATE; 20·log10 of a ~2 to 3x range increase), recoverable with more antenna gain or power. One-way light delay rises from a few ms to ~5 to 10 ms, still negligible versus a GEO relay's ~120 ms ([orbit_types_primer.md], [Light Reading: Starlink vs GEO](https://www.lightreading.com/satellite/starlink-smokes-geo-satellite-operators-in-speed-latency-report)). A higher orbit does see each ground station for slightly longer per pass and covers more ground, marginally helping the LEO pass-duration problem. **Communications is a second-order effect, not a decision driver.**

### 3.3 Debris, collision risk, and congestion

- **800 km is one of the most congested LEO bands**, historically heavy with Earth-observation/weather satellites and the debris from past collisions and ASAT events (`orbits_environment.md`; [ESA SP-1301](https://www.esa.int/esapub/sp/sp1301/sp1301.pdf)). Raising into ~800 km moves the node into worse traffic than ~500 to 600 km.
- **Above ~1000 km, spatial density of operational traffic falls**, but so does the natural "self-cleaning" of debris: at low altitude drag eventually removes debris in years, whereas at ~1000 km-plus fragments persist for centuries. A collision or breakup at the higher altitude is therefore far more consequential and long-lived.
- A large deployed area is itself a **large collision cross-section**, so the node both encounters more flux and presents a bigger target; conjunction screening and occasional avoidance maneuvers are required at any altitude (`orbits_environment.md`).

**Net:** congestion favors the low band or a deliberately chosen altitude away from the ~800 km crowd; debris persistence favors lower (drag-cleansed) altitudes.

### 3.4 End-of-life disposal: harder and mandatory the higher you go

The governing rule is the **US/FCC 5-year deorbit rule**: spacecraft ending life at or below 2,000 km must be disposed of "as soon as practicable and no more than five years after the end of their mission." It took effect **29 September 2024** and replaced the decades-old IADC/NASA/ODMSP **25-year guideline**; it applies to satellites launched two years after the order and to non-US operators seeking US market access ([FCC: 5-Year Rule](https://www.fcc.gov/document/fcc-adopts-new-5-year-rule-deorbiting-satellites-0), [Federal Register, 9 Aug 2024](https://www.federalregister.gov/documents/2024/08/09/2024-17093/space-innovation-mitigation-of-orbital-debris-in-the-new-space-age), [SpaceNews: FCC approves new orbital debris rule](https://spacenews.com/fcc-approves-new-orbital-debris-rule/)).

The consequence is decisive for the "go higher" option:

- **At ~500 to 600 km**, natural decay (helped by the node's large drag area) can plausibly satisfy the 5-year rule with little or no propellant: ESA notes sub-600 km objects generally have lifetimes under 15 years, and the low-B node decays faster still (`orbits_environment.md`, [ESA SP-1301](https://www.esa.int/esapub/sp/sp1301/sp1301.pdf)). This is the disposal advantage of staying low.
- **At ~700 km and above**, natural decay exceeds 5 (and 25) years for the node, so it **must carry an active deorbit capability**. The whole point of raising (drag negligible) directly removes the free-disposal option. You cannot have "no station-keeping" and "free natural disposal" at the same time: the altitude that grants one denies the other.
- **The deorbit burn gets heavier with altitude.** A controlled deorbit (lower perigee to ~120 km for reentry) costs (this calc, cross-checked against a source giving ~600 km deorbit at roughly twice the ~135 m/s of a 350 km case ([CosmoQuest: minimum deorbit delta-v](https://forum.cosmoquest.org/forum/science-and-space/space-astronomy-questions-and-answers/58665-))):

| Deorbit from | Delta-v to 120 km perigee | EP propellant on 8 t node |
|---|---|---|
| 600 km | ~136 m/s | ~70 to 110 kg |
| 800 km | ~188 m/s | ~95 to 155 kg |
| 1000 km | ~237 m/s | ~120 to 195 kg |
| 1200 km | ~284 m/s | ~145 to 235 kg |
| 1400 km | ~328 m/s | ~165 to 270 kg |

So disposal is **cheap in delta-v** (a few hundred m/s, a couple hundred kg of EP propellant) even from 1400 km, but it is now **mandatory, reserved, and growing**: the node must carry a disposal system sized for the chosen altitude, keep that propellant in reserve for the entire mission (not spend it on anything else), and accept the reliability requirement that the deorbit system still works after 7 years in a higher-radiation environment. A failed deorbit at ~1000 km-plus leaves a large-area derelict in a centuries-long orbit, a serious debris liability. (Note: a passive **drag sail** is far less effective at ~1000 km-plus because there is little atmosphere to push against, so high-altitude disposal effectively requires propulsive deorbit, not a sail.)

---

## 4. Net assessment

**Is going higher a viable path to a 7-year life?** Yes, technically. The delta-v to reach a drag-negligible altitude is small (~160 to 450 m/s), the propellant is a 1 to 3% mass hit (smaller than the multi-year station-keeping budget it replaces), and the node can be made permanent above ~900 km. So "raise once, then no drag makeup" is a real option.

**But it is not free, and the savings are spent elsewhere:**

1. **Radiation is the binding side effect.** The node's low ballistic coefficient forces the "drag-negligible" altitude up to ~800 to 900 km (higher than the ~600 to 700 km a normal satellite needs), pushing it into the lower edge of the inner proton belt. TID rises from ~0.3 to 3 krad(Si)/yr (500 to 600 km) toward the low-tens of krad/yr by ~1200 to 1400 km, and shielding effectiveness saturates past ~5 mm Al. More importantly, the **SEU rate on GPU/HBM memory scales with the trapped-proton flux that climbs with altitude and cannot be shielded away**, directly raising the compute-reliability and redundancy burden. This is the dominant penalty.
2. **Mandatory, altitude-growing disposal is the close-second constraint.** Above ~600 to 650 km the 5-year rule can no longer be met by drag, so the node must carry an active deorbit system regardless. It is delta-v-cheap (~190 to 330 m/s) but it is a reserved mass line, a reliability obligation, and a debris liability that all worsen with altitude.
3. **Delta-v / propellant is NOT the binding constraint.** Both raising and deorbiting are cheap; the rocket-equation cost is dwarfed by the radiation and disposal consequences.

**Recommended lean.** The trade is fundamentally **station-keeping propellant (stay low) vs radiation-plus-mandatory-disposal (go high)**. Because the dominant penalty (SEU rate, then disposal burden) both *worsen monotonically with altitude*, if the project goes higher it should go **only as high as needed**, roughly **~700 to 800 km**, where the node gets a multi-year-to-permanent life with only a modest radiation increase over the baseline. The existing project preference for the **low ~500 to 600 km band with light electric station-keeping** remains fully competitive and keeps both radiation and disposal easy; its cost is the continuous drag-makeup propellant, which the node is already designed to carry. A jump to ~1000 to 1400 km buys a permanent orbit but is the worst of both worlds on radiation and on debris persistence, and is not recommended.

---

## Sources

- [Space Academy: Satellite Orbital Lifetimes](https://www.spaceacademy.net.au/watch/debris/orblife.htm)
- [arXiv 2508.19549: Modeling Orbital Decay of LEO Satellites due to Atmospheric Drag (2025)](https://arxiv.org/html/2508.19549v2)
- [ESA SP-1301: Position Paper on Space Debris Mitigation](https://www.esa.int/esapub/sp/sp1301/sp1301.pdf)
- [AgentCalc: Satellite Orbit Decay Time Calculator](https://agentcalc.com/satellite-orbit-decay-time-calculator)
- [NASA Small Spacecraft SOA: Deorbit Systems](https://www.nasa.gov/smallsat-institute/sst-soa/deorbit-systems/)
- [Hou/USRA: DragSail Systems for Satellite Deorbit and Targeted Reentry](https://www.hou.usra.edu/meetings/orbitaldebris2019/orbital2019paper/pdf/6020.pdf)
- [Wikipedia: Hohmann transfer orbit](https://en.wikipedia.org/wiki/Hohmann_transfer_orbit)
- [Brainly: worked 500 to 1000 km Hohmann transfer example (~257 m/s)](https://brainly.com/question/38269135)
- [Wikipedia: Delta-v budget](https://en.wikipedia.org/wiki/Delta-v_budget)
- [Wikipedia: Tsiolkovsky rocket equation](https://en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation)
- [Busek: Hall Thrusters](https://www.busek.com/hall-thrusters)
- [Wikipedia: Hall-effect thruster](https://en.wikipedia.org/wiki/Hall-effect_thruster)
- [PEPL/UMich AIAA-96-2973: Analysis of Hall-Effect Thrusters and Ion Engines for Orbit Transfer (LEO-to-MEO ~192 days)](https://pepl.engin.umich.edu/pdf/AIAA-96-2973.pdf)
- [NASA/TM-20220011775: Mission Radiation Environment Modeling and Analysis (Aug 2022)](https://ntrs.nasa.gov/api/citations/20220011775/downloads/Mission_Radiation_Modeling_STI.pdf)
- [Wikipedia: Van Allen radiation belt](https://en.wikipedia.org/wiki/Van_Allen_radiation_belt)
- [ScienceDirect Topics: Inner Radiation Belt](https://www.sciencedirect.com/topics/physics-and-astronomy/inner-radiation-belt)
- [ASU (Holbert): Total Ionizing Dose notes](http://holbert.faculty.asu.edu/eee560/tiondose.html)
- [ResearchGate: Studying the TID and DDD effects for various orbital trajectories](https://www.researchgate.net/publication/235692893_Studying_the_Total_Ionizing_Dose_and_Displacement_Damage_Dose_effects_for_various_orbital_trajectories)
- [Wikipedia: Sun-synchronous orbit](https://en.wikipedia.org/wiki/Sun-synchronous_orbit)
- [FCC: Adopts New "5-Year Rule" for Deorbiting Satellites](https://www.fcc.gov/document/fcc-adopts-new-5-year-rule-deorbiting-satellites-0)
- [Federal Register: Mitigation of Orbital Debris in the New Space Age (9 Aug 2024)](https://www.federalregister.gov/documents/2024/08/09/2024-17093/space-innovation-mitigation-of-orbital-debris-in-the-new-space-age)
- [SpaceNews: FCC approves new orbital debris rule](https://spacenews.com/fcc-approves-new-orbital-debris-rule/)
- [CosmoQuest forum: minimum delta-v to deorbit (600 km ~2x the 350 km case)](https://forum.cosmoquest.org/forum/science-and-space/space-astronomy-questions-and-answers/58665-)
- [Light Reading: Starlink smokes GEO operators in speed, latency](https://www.lightreading.com/satellite/starlink-smokes-geo-satellite-operators-in-speed-latency-report)

## Open questions / Uncertainties

1. **Node-specific ballistic coefficient is the dominant lifetime unknown.** The ~800 to 900 km "7-year-life" band is derived by applying the linear m/A scaling to generic King-Hele curves, using an assumed time-averaged drag area of ~100 to 400 m². The real number depends on the final geometry and the attitude/feathering strategy of the arrays and radiator. A node-specific orbit propagation (STK/GMAT or ESA OSCAR) with a real drag model and solar-cycle sweep is needed to firm up the altitude band. **Highest-priority unknown.**
2. **TID and SEU rate at the specific higher altitude are not yet modeled for this orbit.** The upper-band TID (~hi-single-digits to low-tens krad/yr at ~1200 to 1400 km) is an estimate extrapolated from belt physics and the NASA polar curves. A SPENVIS/SHIELDOSE-2 (TID) plus CREME96 (SEU) run at the chosen altitude and inclination, with the actual shielding stack, should replace these bands. The per-GPU/HBM SEU rate as a function of altitude is the key reliability driver and is not publicly characterized for modern accelerators.
3. **Solar-cycle phase matters a lot.** Lifetimes at a given altitude can vary by a factor of several between solar minimum and maximum, and trapped-proton flux is anti-correlated with solar activity. The launch date relative to the solar cycle shifts both the required altitude and the dose. Not yet incorporated.
4. **EP transfer time for the raise is unquantified.** "Weeks to a few months" is an order-of-magnitude estimate; it depends on installed EP power/thrust on an ~8 t platform and on how much array power can be diverted to propulsion during the spiral. Affects revenue-start delay and en-route dose.
5. **Deorbit-system reliability after a long high-radiation life.** A mandatory propulsive deorbit from ~800 km-plus must still function after 5 to 7 years in a harsher environment; failure leaves a large-area, long-lived derelict. Reliability and redundancy of the disposal system at higher altitude need a dedicated assessment.
6. **Interaction with the radiator hot-loop / HBM thermal tension.** A higher SEU rate and higher TID compound the existing junction-temperature reliability concern (`node_mass_model.md`, `hot_chip_thermal_trajectory.md`): radiation-induced degradation and thermal derating both attack the same silicon. The combined reliability budget at higher altitude is not yet modeled.
7. **Communications link-budget penalty (~6 to 10 dB) is an estimate** and assumes simple range-squared scaling; the real penalty depends on the chosen relay/ground architecture (`laser_comms/`).
