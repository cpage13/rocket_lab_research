# Orbital Environment — Sun-Synchronous Orbit for a Space Data Center

*Doc 6 of foundational research. Status: draft. Date: 2026-05-17.*

## Summary / Verdict

A **dawn-dusk sun-synchronous orbit (SSO)** at ~500-800 km is the natural home for
an orbital AI data center: it gives **near-continuous sunlight** (eclipse fraction
falling from ~35-38% in a generic SSO to roughly **0-5% averaged over the year** on
the dawn-dusk terminator), which roughly **halves the required solar array** and
collapses the battery mass needed to ride out shadow.

The cost is payload. SSO is the most expensive common LEO destination because of
its high (~98°) inclination and the energy lost launching out-of-plane. Rocket Lab
publishes no Neutron SSO figure; scaling from the ~13 t reusable / ~15 t expendable
LEO baseline, a defensible **estimate is ~9-11 t reusable and ~11-12.5 t expendable
to a 500-700 km dawn-dusk SSO** (≈25-30% below the equatorial-LEO baseline). This
doc carries **~10 t reusable** as the working SSO number.

> **Superseded (wave-5, 2026-05-17):** the SSO working figure has been
> re-baselined to **~9.5 t reusable (range 8.5–10.5 t)**. The ~10 t figure
> below is superseded — see `rocket_lab/neutron/payload_and_block_upgrade.md`
> for the current numbers. This doc's analysis is otherwise unchanged.

Radiation at this altitude is **benign and well-characterized** — ~1-3 krad(Si)/yr
behind a few mm of aluminium — so radiation is a *reliability-engineering* problem
(ECC, redundancy, modest spot shielding), **not** a physics wall. Debris and the new
5-year deorbit rule are real but manageable constraints on constellation design.

> Bottom line: the orbit is favorable. Dawn-dusk SSO is the enabling choice. The
> binding constraint is **launch mass to SSO**, not the environment — see
> `thermal_analysis.md` for what eats that mass budget.

---

## 1. Sun-Synchronous Orbit and the Dawn-Dusk Variant

### What an SSO is
A sun-synchronous orbit is a near-polar LEO whose orbital plane precesses eastward
~0.986°/day — exactly tracking Earth's motion around the Sun — so the satellite
crosses any given latitude at the **same local solar time** every pass. The
precession is "free": it is produced by the torque of Earth's equatorial bulge (the
J2 perturbation) on a slightly retrograde orbit. This locks **altitude and
inclination together**:

| Altitude | Inclination | Orbital period |
|---|---|---|
| 500 km | ~97.4° | ~94.6 min |
| 600 km | ~97.8° | ~96.7 min |
| 800 km | ~98.6° | ~100.9 min |

Typical SSOs sit at **600-800 km, ~98° inclination, 96-101 min period**
([Wikipedia: Sun-synchronous orbit](https://en.wikipedia.org/wiki/Sun-synchronous_orbit),
[ESA — Polar and Sun-synchronous orbit](https://www.esa.int/ESA_Multimedia/Images/2020/03/Polar_and_Sun-synchronous_orbit)).
SSO is the workhorse orbit for Earth observation because the constant lighting angle
makes images comparable over time.

### Why it matters here: the dawn-dusk variant and eclipse fraction
The relevant quantity for power sizing is the **eclipse fraction** — the share of
each orbit spent in Earth's shadow. This is governed by the **beta angle (β)**, the
angle between the Sun vector and the orbital plane.

- **Generic SSO (e.g. noon/midnight, β near 0°):** the orbit plane lies edge-on to
  the Sun, so the satellite plunges through Earth's shadow every orbit. At β = 0°
  a LEO satellite spends only ~59-65% of the orbit in sunlight — i.e. an
  **eclipse fraction of ~35-41%** ([eclipse-fraction discussion, scaled from beta-angle
  geometry](https://en.wikipedia.org/wiki/Beta_angle)). At 800 km the maximum
  eclipse is ~35 min out of a ~101 min orbit.

- **Dawn-dusk SSO (β ≈ 90°):** the orbit plane is held nearly face-on to the Sun;
  the satellite "rides the terminator" and its solar panels see the Sun
  continuously. For most of the year the **eclipse fraction is 0%**. Earth's axial
  tilt still drags β away from 90° near one solstice, producing a short
  **eclipse season**: real dawn-dusk missions (e.g. PROBA-2) see eclipses only on
  the order of **~80 days/year, peaking at ~18-23 min per orbit** and tapering to
  zero either side ([PROBA-2 launch & orbit, SIDC](https://proba2.sidc.be/about/launch),
  [Wikipedia: Sun-synchronous orbit](https://en.wikipedia.org/wiki/Sun-synchronous_orbit)).

**Year-averaged eclipse fraction:** generic SSO ≈ **35-38%**; dawn-dusk SSO ≈
**3-6%** (zero for ~9 months, then a bounded eclipse season). A higher altitude
(e.g. 700-800 km) further shortens any eclipse and shrinks the eclipse season.

**Design consequence.** Choosing dawn-dusk SSO is the single highest-leverage
orbital decision:
- Solar array sized for ~95-100% sunlit duty instead of ~62% → roughly **half the
  array area** for the same average compute power.
- Battery/energy-storage mass shrinks from "carry the full load through 35 min of
  dark every 100 min" to "carry the load through a worst-case ~20-min eclipse for
  ~80 days/year" — or even accept graceful throttling of compute during the brief
  eclipse season and carry almost no batteries. This is a major mass saving.
- Thermal environment is also steadier (see `thermal_analysis.md`): the radiators
  can be held edge-on to a Sun whose direction barely moves.

---

## 2. Reaching SSO on Neutron — Payload Estimate

### Neutron's published baseline (LEO, not SSO)
Rocket Lab quotes Neutron at **~13,000 kg to LEO reusable** (downrange ocean
landing), **~15,000 kg expendable**, and **~8,500 kg return-to-launch-site (RTLS)**
([Wikipedia: Rocket Lab Neutron](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron),
[Gunter's Space Page — Neutron](https://space.skyrocket.de/doc_lau/neutron.htm)).
*(8,500 kg is the official RTLS figure — consistent with `neutron_specs.md`,
`payload_and_block_upgrade.md` and `orbit_types_primer.md`; an earlier version of
this doc carried 8,000 kg, which is in fact the superseded 2021 original-design
"~8-ton-class to LEO" figure, not the current RTLS number.)* Rocket Lab does not
publish the reference altitude/inclination behind its LEO figures; the **500 km,
40° inclination** sometimes quoted for the 15 t expendable number is a common
assumption, **not an official Rocket Lab specification** — treat it as
illustrative. Rocket Lab publishes **no SSO performance number** as of May 2026.

### Why SSO costs payload
SSO is roughly **97-99° inclination**. Launching to such a high inclination from a
mid-latitude site forfeits most of the "free" eastward velocity from Earth's
rotation (~0.4 km/s at the equator) and, for a near-polar/retrograde plane, can
require a small dogleg. Net effect: SSO needs **a few hundred m/s more delta-v**
than a low-inclination LEO and the rocket must carry it at a worse gravity-loss
geometry. Industry rule of thumb, consistent across Falcon 9 / Electron-class
vehicles: **SSO payload is ~20-35% below the same vehicle's low-inclination LEO
payload**, with the larger penalty when the SSO is also at a higher (700-800 km)
altitude than the reference LEO.

### Estimate (flagged as estimate — no official RL figure)

| Configuration | LEO baseline (official) | SSO estimate (this doc) | Penalty assumed |
|---|---|---|---|
| Reusable, downrange landing | ~13.0 t | **~9.0-11.0 t** (carry **~10 t**) | ~25-30% |
| Expendable | ~15.0 t | **~11.0-12.5 t** | ~20-25% |
| Reusable, RTLS | ~8.5 t | **~6.0-6.5 t** | ~25-30% |

**Reasoning:** SSO at 500-700 km is treated as a ~25-30% haircut on the reusable
LEO baseline (the heavier end because dawn-dusk SSO is typically flown at the upper
altitude band for the lighting geometry, and downrange recovery already spends
margin). Expendable keeps more because there is no recovery reserve to protect.
The project's earlier "~8-10 t SSO" assumption is on the **conservative** side of
this estimate; **~10 t reusable** is used as the working number, with ~8 t as a
pessimistic floor.

> ESTIMATE — not an official Rocket Lab figure. Should be replaced the moment RL
> publishes Neutron SSO performance.

---

## 3. Reusable vs. Expendable Tradeoff

Neutron is **partially reusable**: the first stage and fairing are designed to be
recovered and reflown ("10 to 20 times" per booster, per Rocket Lab, mirroring
Falcon 9 reuse) ([Aerospace America — Rocket Lab's next step](https://aerospaceamerica.aiaa.org/features/rocket-labs-next-step/)).

### The lever
- **Reusable (downrange):** ~10 t to SSO (est.), booster recovered and reflown.
- **Expendable:** ~11-12.5 t to SSO (est.), **+15-25% payload**, but the entire
  first stage (~$20-25M of vehicle) is discarded.
- **RTLS:** ~6.0-6.5 t to SSO (est., from the 8.5 t LEO RTLS baseline) — lowest payload, cheapest/fastest turnaround.

So a constellation buildout can trade **fewer expendable flights at higher unit
cost** against **more reusable flights at lower unit cost**.

### Cost (estimates — Rocket Lab has not published a firm price)
- Rocket Lab's stated **target price is ~$50-55M per reusable Neutron launch**
  ([CNBC, 2023 — $50M target price](https://www.cnbc.com/2023/03/24/rocket-lab-neutron-launch-price-challenges-spacex.html);
  [Grokipedia — Rocket Lab Neutron](https://grokipedia.com/page/Rocket_Lab_Neutron)).
- Vehicle production cost is estimated at **~$20-25M per first stage**; booster
  refurbishment is budgeted around **~$20M per cycle** in third-party analyses.
- Implied **expendable price ≈ $70-80M** (reusable price + the thrown-away stage),
  though Rocket Lab has not quoted an expendable number.

### Worked comparison (illustrative — for ~100 t of hardware to SSO)
| Mode | Payload/flight (SSO est.) | Flights for ~100 t | Est. $/flight | Total launch cost | $/kg |
|---|---|---|---|---|---|
| Reusable | ~10 t | ~10 | ~$50-55M | ~$0.50-0.55B | ~$5.0-5.5k |
| Expendable | ~11.5 t | ~9 | ~$70-80M | ~$0.63-0.72B | ~$5.5-6.3k |

**Read:** reusable is cheaper per kg despite needing one extra flight; expendable
buys **schedule and fewer integration cycles**, not cost. For a multi-launch
constellation, **reusable is the default**; expendable is a tool for an
oversized/indivisible node or a schedule crunch. (Costs are estimates — see Open
Questions.)

---

## 4. Radiation Environment at 500-800 km SSO

### Dose
A 500-800 km SSO sits **below the core proton belt** but clips the **South Atlantic
Anomaly** and sees trapped electrons plus galactic cosmic rays (GCRs) and occasional
solar particle events. Quantitatively:

- **Unshielded** trapped-electron dose at ~800 km is on the order of **~100 krad/yr**,
  but this is dominated by soft electrons and is **easily attenuated**.
- Behind **~4-6 mm of aluminium**, total ionizing dose (TID) at an ~800 km helio-
  synchronous LEO drops to roughly **~1-3 krad(Si)/yr** — one source cites
  **~1.87 krad(Si)/yr** for an 800 km SSO behind typical shielding
  ([Toward COTS in space — true LEO radiation environment, MDPI](https://www.mdpi.com/2079-9292/12/19/4058);
  [TID/DDD for various orbits — ResearchGate](https://www.researchgate.net/publication/235692893_Studying_the_Total_Ionizing_Dose_and_Displacement_Damage_Dose_effects_for_various_orbital_trajectories)).
- General LEO guidance: **1-10 krad(Si)/yr** depending on shielding, altitude and
  solar cycle; ~3 mm Al holds a 3-year mission under ~10 krad(Si).

For context, commercial silicon survives **tens of krad** TID; modern data-center
GPUs are not radiation-hardened but are also not obviously fragile at these dose
rates over a multi-year life. **TID is a manageable lifetime-budget item, not a
wall.**

### Single-event effects (the real concern for GPUs/memory)
The dominant risk for dense compute is **single-event upsets/effects (SEU/SEE)** —
GCRs and SAA protons flipping bits or latching logic. This is **not** solved by
shielding (GCRs are too energetic) and must be handled architecturally:
- **ECC on all memory** (HBM/DRAM/SRAM), end-to-end.
- **Watchdogs, periodic scrubbing, checkpoint/restart**, and node-level redundancy
  so an upset costs a recomputed batch, not a mission.
- AI **inference is relatively SEU-tolerant**: a flipped weight bit is usually a
  small numeric error, often invisible in the output; the risk concentrates in
  control logic and accumulators, which is exactly what ECC + scrubbing protects.
- Independent commentary notes silicon GPUs in orbit "need heavy shielding or
  accept higher error rates," and that wide-bandgap (SiC) parts are far more
  SEU-resistant — relevant if a future hardened accelerator is considered
  ([radiation environment & SEU observations in SSO, IEEE](https://ieeexplore.ieee.org/document/124165)).

### Shielding mass implication
- TID protection is cheap: **~4-6 mm aluminium** (or equivalent in existing
  structure/enclosure walls) is enough. For a rack-scale box this is **a modest,
  sometimes "free," fraction of structural mass** rather than a dedicated mass line.
- **Spot-shielding** the most dose-sensitive parts is cheaper than blanket
  shielding. Blanket-shielding a large compute volume to "rad-hard" levels would be
  mass-prohibitive — but is **not required** at these dose rates.
- GCR/SEU shielding is effectively impossible by mass and is therefore an
  architecture problem, as above.

**Verdict on radiation:** at 500-800 km SSO, radiation is **a known,
design-around-able environment**. It costs some shielding mass (single-digit mm of
Al) and some compute overhead (ECC, scrubbing, redundancy, derated lifetime). It is
**not** a feasibility blocker.

---

## 5. Debris, Station-Keeping, End-of-Life

### Debris environment
**800 km is one of the more congested LEO bands** — historically heavy with Earth-
observation and weather satellites and the debris from past collisions/ASAT events.
Choosing the **lower end (~500-600 km)** materially reduces collision risk and
shortens natural decay. A multi-satellite compute constellation must budget for:
- **Conjunction screening** and occasional collision-avoidance maneuvers (propellant
  + an onboard propulsion system, e.g. electric thrusters).
- **Trackability and coordination** — many co-orbiting compute nodes flying as a
  constellation.

### Station-keeping
At 500-800 km, atmospheric drag is small but non-zero and **rises with the large
area-to-mass ratio** created by big solar arrays and radiator panels — exactly this
design. Drag makeup plus collision-avoidance implies the bus needs **propulsion and
a multi-year propellant budget** (electric propulsion is the mass-efficient choice).
Large deployed surfaces increase drag and make this line item bigger than for a
compact satellite.

### End-of-life — the 5-year rule
The old IADC **25-year** LEO disposal guideline has been superseded for U.S.-licensed
operators by the **FCC 5-year rule**: spacecraft ending life at/below 2,000 km must
deorbit **as soon as practicable and within 5 years** of mission end
([SpaceNews — FCC approves new orbital debris rule](https://spacenews.com/fcc-approves-new-orbital-debris-rule/);
[NASA — Deorbit Systems SOA](https://www.nasa.gov/smallsat-institute/sst-soa/deorbit-systems/)).

Implications for the constellation:
- **At ~500-600 km**, a node with large drag area can comply largely via **natural
  decay** (years), possibly aided by attitude "drag mode" or a small drag device —
  cheap.
- **At ~800 km**, natural decay takes far longer than 5 years; the node would need
  **active deorbit propulsion** to lower perigee at end of life — a real propellant
  mass line.
- This is another argument for the **lower (~500-600 km) dawn-dusk SSO band**: less
  debris, easier compliant disposal, modest cost in eclipse-season length.
- Each node should be **designed for controlled disposal** (deorbit burn or drag
  device), and the constellation operations plan must include replacement cadence
  as nodes age out — itself a driver of launch demand and economics.

---

## Sources

- [Wikipedia — Sun-synchronous orbit](https://en.wikipedia.org/wiki/Sun-synchronous_orbit)
- [ESA — Polar and Sun-synchronous orbit](https://www.esa.int/ESA_Multimedia/Images/2020/03/Polar_and_Sun-synchronous_orbit)
- [Wikipedia — Beta angle](https://en.wikipedia.org/wiki/Beta_angle)
- [PROBA-2 Science Center — Launch and Orbit](https://proba2.sidc.be/about/launch)
- [Wikipedia — Rocket Lab Neutron](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron)
- [Gunter's Space Page — Neutron](https://space.skyrocket.de/doc_lau/neutron.htm)
- [Aerospace America — Rocket Lab's next step](https://aerospaceamerica.aiaa.org/features/rocket-labs-next-step/)
- [CNBC — Rocket Lab targets $50M launch price for Neutron](https://www.cnbc.com/2023/03/24/rocket-lab-neutron-launch-price-challenges-spacex.html)
- [Grokipedia — Rocket Lab Neutron](https://grokipedia.com/page/Rocket_Lab_Neutron)
- [MDPI Electronics — Toward COTS devices in space: true LEO radiation environment](https://www.mdpi.com/2079-9292/12/19/4058)
- [ResearchGate — TID and DDD effects for various orbital trajectories](https://www.researchgate.net/publication/235692893_Studying_the_Total_Ionizing_Dose_and_Displacement_Damage_Dose_effects_for_various_orbital_trajectories)
- [IEEE — Radiation environment & SEU observations in sun-synchronous orbit](https://ieeexplore.ieee.org/document/124165)
- [SpaceNews — FCC approves new orbital debris rule](https://spacenews.com/fcc-approves-new-orbital-debris-rule/)
- [NASA Small Spacecraft SOA — Deorbit Systems](https://www.nasa.gov/smallsat-institute/sst-soa/deorbit-systems/)

## Open Questions / Uncertainties

- **No official Neutron SSO payload.** The ~9-11 t reusable estimate is derived
  from a generic 25-30% LEO→SSO penalty; could be off by ±2 t. Replace with RL data
  when published.
- **Launch price is a target, not a contract price.** $50-55M reusable and the
  ~$70-80M implied expendable are estimates; actual early-flight prices will be
  higher until the booster fleet matures.
- **Drag at large area-to-mass ratio is poorly bounded** for this design — big
  arrays + radiators could make station-keeping/deorbit propellant a larger line
  than assumed. Needs a real drag model once geometry is set.
- **Eclipse-season profile** (exact days/year and per-orbit minutes) depends on
  precise altitude/launch date — needs an STK/GMAT propagation for the chosen orbit.
- **SEU rates for specific modern GPUs/HBM** in this orbit are not publicly
  characterized; flagged for the radiation deep-dive and for hardware selection.
- **Constellation collision risk at 800 km** vs. operational benefit of higher
  altitude (less drag) is an unresolved trade — current lean is toward ~500-600 km.
