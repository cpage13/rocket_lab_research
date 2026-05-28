# Electron — Rocket Specifications

**Prepared:** May 2026 · **For:** RKLB space-data-center feasibility study
**Scope:** Focused specs sheet for Rocket Lab's Electron small-lift launch vehicle. Company-wide context in `../overview.md`.

---

## Summary Table

| Parameter | Value | Confidence |
|---|---|---|
| Class | Small-lift, two-stage orbital launch vehicle | High |
| Operator / manufacturer | Rocket Lab Corporation | High |
| First orbital flight | 2017 (maiden test "It's a Test", May 2017; first success Jan 2018) | High |
| Height | ~18 m (~59 ft) | High |
| Diameter | 1.2 m (~3.9 ft) | High |
| Liftoff mass | ~13,000 kg | High |
| Structure | Carbon-composite (fully composite tanks and structures) | High |
| Stages | 2, plus optional Curie-powered kick stage / Photon | High |
| Payload to LEO | ~300 kg max | High |
| Payload to 500 km SSO | ~200 kg (typical) | High |
| Stage 1 engines | 9 × Rutherford (sea-level) | High |
| Stage 2 engine | 1 × Rutherford (vacuum-optimized) | High |
| Stage 1 thrust (liftoff) | ~162 kN sea level / ~224 kN as quoted vacuum-equivalent | Med (source variance) |
| Stage 2 thrust | ~22–25.8 kN | Med (source variance) |
| Propellant | LOX / RP-1 kerosene | High |
| Engine cycle | Electric-pump-fed (battery-driven pumps) — industry first | High |
| Kick stage engine | Curie (3D-printed) | High |
| Launch sites | LC-1 Māhia, New Zealand (pads 1A/1B); LC-2 Wallops Island, Virginia | High |
| Price per dedicated launch | ~$8.4M list (historically ~$6.5–7.5M; HASTE ~$9.5M/flight) | Med |
| Total launches | ~80+ since 2017 (80th launch Jan 2026) | High |
| 2025 launches | 21, 100% mission success | High |
| Lifetime failures | 4 | High |
| Reusability | Partial — first-stage ocean recovery; first reflight in progress | High |

---

## 1. Overview

Electron is Rocket Lab's operational **small-lift, two-stage orbital rocket**, purpose-built for **dedicated small-satellite launches** to low Earth orbit. It entered service with its first orbital test in May 2017 and first successful orbital flight in January 2018. Electron is the most-flown US small launch vehicle and, by 2025 launch count, second only to SpaceX among Western launch providers.

The vehicle is notable for two engineering choices: an **all-carbon-composite airframe and tanks**, and **electric-pump-fed engines** — the first electric-pump-fed engine to power an orbital-class rocket, replacing gas turbopumps with battery-driven electric pumps.

A suborbital variant, **HASTE** (Hypersonic Accelerator Suborbital Test Electron), uses Electron hardware for hypersonic test missions for US defense customers.

---

## 2. Physical Dimensions & Structure

- **Height:** ~18 m (~59 ft)
- **Diameter:** 1.2 m (~3.9 ft)
- **Liftoff mass:** ~13,000 kg
- **Structure:** Lightweight carbon-composite throughout, including propellant tanks
- **Stages:** Two main stages; an optional kick stage (Curie-powered) — also marketed as the basis of the **Photon** satellite bus — enables precise orbit insertion and multi-manifest deployment.

---

## 3. Payload Capacity

- **Maximum payload to LEO:** ~300 kg
- **Typical payload to 500 km Sun-synchronous orbit (SSO):** ~200 kg
- Quoted ranges of 200–300 kg reflect orbit/altitude/inclination dependence.
- Designed for CubeSats and small satellites; the kick stage allows multiple satellites to be dropped into different orbits on one flight.

**Relevance to data-center thesis:** Electron's ~300 kg LEO capacity is far too small to deploy a meaningful AI-inference data-center payload. Electron is relevant mainly as Rocket Lab's proven, high-cadence operational track record and as a technology/process feeder to Neutron — it is **not** the vehicle for orbital data-center deployment. Neutron (~13,000 kg to LEO) is the relevant launcher.

---

## 4. Propulsion — Rutherford Engines

- **Stage 1:** 9 × **Rutherford** sea-level engines.
- **Stage 2:** 1 × **Rutherford** vacuum-optimized engine.
- **Cycle:** Electric-pump-fed — lithium-polymer batteries drive electric turbopumps. This was an industry first for an orbital rocket and simplifies the engine versus a gas-generator/turbopump design.
- **Propellant:** Liquid oxygen (LOX) and RP-1 kerosene.
- **Manufacturing:** Rutherford is **largely 3D-printed** — combustion chamber, injectors, pumps, and main propellant valves are produced additively, enabling fast, low-cost engine production. Rocket Lab has cited approaching its ~1,000th Rutherford engine flown.
- **Thrust figures vary by source:** Stage 1 commonly cited at ~162 kN (sea level), with vacuum-equivalent / total figures up to ~224 kN; Stage 2 cited at ~22 kN to ~25.8 kN. Treat exact thrust as source-dependent.
- **Kick stage:** powered by the **Curie** engine (also 3D-printed), used for precise orbital maneuvers and multi-orbit deployment.

---

## 5. Launch Sites

- **Launch Complex 1 (LC-1), Māhia Peninsula, New Zealand** — Rocket Lab's primary site; **two pads (LC-1A and LC-1B)** and two integration hangars, enabling simultaneous payload processing and high cadence.
- **Launch Complex 2 (LC-2), Wallops Island, Virginia, USA** — on NASA Wallops land; supports US-based launches, including US government missions.

---

## 6. Flight History, Cadence & Reliability

- **Total launches:** ~80+ since 2017 — the 80th Electron launch occurred 22 January 2026 (deploying two satellites for Open Cosmos).
- **2025:** Record year — **21 Electron launches with 100% mission success** (up from 16 in 2024; 3 of the 2025 flights were HASTE suborbital missions).
- **Lifetime failures:** 4 (across the full flight history since 2017).
- **Cadence:** Sustained >20 flights/year; Rocket Lab targets its 100th launch during 2026 and reported 8 successful launches year-to-date by early May 2026.
- Electron has carried customers including NASA, US defense agencies, and numerous commercial smallsat operators.

*(Exact cumulative launch and success totals drift slightly between sources depending on the cutoff date and whether HASTE suborbital flights are counted; the ~80+ orbital figure and 21/21 for 2025 are well-supported.)*

---

## 7. Pricing

- Current list price for a dedicated Electron launch is commonly cited around **~$8.4 million**.
- Historical pricing: ~$6.5M at service entry (2018), later cited around $7.5M; per-kg figures around $25,000/kg are quoted for dedicated missions.
- The Q1 2026 **HASTE block buy** (~$190M for 20 flights) implies ~$9.5M per HASTE flight — roughly 13% above the prior standard Electron price, indicating gradual price escalation.
- Pricing varies with mission requirements; rideshare/multi-manifest customers split the cost across payloads.

---

## 8. Reusability

Rocket Lab is pursuing **partial reusability** of the Electron first stage:

- **Method:** Parachute-softened **ocean splashdown**, followed by rapid boat recovery to limit saltwater exposure to the engines. An earlier plan to catch the stage mid-air with a helicopter was tested and then abandoned in favor of ocean recovery.
- **Status:** A recovered first stage (from the "Four of a Kind" mission, Jan 2024) has been reintroduced into the production line and has passed more acceptance tests than any prior recovered stage — tank pressurization, helium leak check, carbon-fiber structural testing — as Rocket Lab works toward a **first-ever Electron reflight**.
- Reusability know-how on Electron feeds directly into Neutron, which is designed for routine first-stage reuse with downrange droneship landing.

---

## Open Questions / Uncertainties

- **Thrust values** differ across sources (sea-level vs. vacuum, per-engine vs. total). The ~162 kN / ~224 kN spread for Stage 1 and ~22–25.8 kN for Stage 2 should be confirmed against a Rocket Lab datasheet if precise numbers are load-bearing.
- **Cumulative launch count** is a moving target; ~80+ orbital launches is accurate as of early 2026 but increments roughly twice monthly.
- **List price (~$8.4M)** is approximate; Rocket Lab does not always publish current pricing, and contract prices vary (HASTE ~$9.5M/flight).
- **First Electron reflight** had not occurred as of this writing — recovery hardware was in the production line but no reused-stage launch was confirmed.
- Electron is **not relevant as a data-center deployment vehicle** due to its ~300 kg payload ceiling; this doc is included for completeness of the Rocket Lab launch portfolio.

---

## Sources

- [Wikipedia — Rocket Lab Electron](https://en.wikipedia.org/wiki/Rocket_Lab_Electron)
- [Wikipedia — List of Electron launches](https://en.wikipedia.org/wiki/List_of_Electron_launches)
- [Wikipedia — Rocket Lab Launch Complex 1](https://en.wikipedia.org/wiki/Rocket_Lab_Launch_Complex_1)
- [Gunter's Space Page — Electron](https://space.skyrocket.de/doc_lau/electron.htm)
- [Space.com — Rocket Lab's Electron Rocket](https://www.space.com/electron-rocket.html)
- [Rocket Lab — "Meet Rocket Lab's Electron rocket" (education PDF)](https://rocketlabcorp.com/assets/Uploads/RL-EducationGraphics-About-Rocket-Lab-and-Electron.pdf)
- [SatNow — Electron launch vehicle details](https://www.satnow.com/launch-vehicle-details/electron)
- [StockTitan — Rocket Lab ends 2025 with 21 Electron launches, 100% success](https://www.stocktitan.net/news/RKLB/rocket-lab-successfully-launches-for-i-qps-ends-2025-with-21-jvv3dukgezth.html)
- [SpaceNews — Rocket Lab wraps up record launch year](https://spacenews.com/rocket-lab-wraps-up-record-launch-year/)
- [NASASpaceFlight — After record-breaking 2025, Rocket Lab prepares for Neutron's debut](https://nasaspaceflight.com/2025/12/rocket-lab-2025-overview/)
- [VoxelMatters — Rocket Lab targets 1,000th Rutherford engine launch](https://www.voxelmatters.com/rocket-lab-targets-1000th-rutherford-engine-launch-as-am-scales-from-electron-to-neutron/amp/)
- [Space.com — Rocket Lab gearing up to refly Electron booster](https://www.space.com/rocket-lab-recovered-electron-production-line-reflight)
- [Rocket Lab — Announces Reusability Plans for Electron Rocket](https://rocketlabcorp.com/updates/rocket-lab-announces-reusability-plans-for-electron-rocket/)
- [Rocket Lab — $30M HASTE contract for Anduril (pricing reference)](https://rocketlabcorp.com/updates/rocket-lab-awarded-30-million-contract-for-haste-hypersonic-rocket-launches-for-anduril/)
- [BGR — US $190M HASTE block buy of 20 hypersonic test flights](https://www.bgr.com/2154992/us-military-haste-rocket-lab-hypersonic-rockets-contract/)
