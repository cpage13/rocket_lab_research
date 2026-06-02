# Rocket Lab — Space Hardware / Components Capabilities

**Prepared:** May 2026 · **For:** RKLB space-data-center feasibility study
**Scope:** Deep dive on Rocket Lab's in-house SPACE HARDWARE — solar, deployable structures, actuators/mechanisms, satellite buses, components/electronics — and an assessment of how complete its in-house coverage is for building an orbital AI-inference compute node. Company-level profile lives in `rocket_lab/overview.md`.

---

## Summary

Rocket Lab has assembled, largely through acquisition, an unusually deep in-house space-hardware stack. For a compute-satellite node it **already owns**: space-grade solar cells and arrays (SolAero, the only fully vertically integrated solar supplier in the industry), a new silicon solar-array product line explicitly aimed at gigawatt-scale orbital data centers, satellite buses (Photon, Flatellite), reaction wheels and star trackers (Sinclair Interplanetary), separation systems (Planetary Systems Corp), software-defined radios (Frontier), EO/IR and laser-comms payloads (Geost), laser inter-satellite terminals (Mynaric/CONDOR), composite structures, and (acquisition completed 26 May 2026) solar array drive assemblies, gimbals, actuators and robotic arms (Motiv → "Rocket Lab Robotics").

The **hardest single piece** for a compute node is **deployable thermal radiators**: heat rejection is the single hardest problem for orbital compute (the critical path), and there is no public large-scale deployable-radiator product from Rocket Lab today. This is best read as **pending in-house development (expected; in their wheelhouse)** rather than a capability gap: Rocket Lab already flies its own thermal control on its satellites and owns the composite, mechanism, and solar know-how a node-scale radiator draws on, so it is a question of timing and scale, not a missing competency, and Rocket Lab would develop it in-house (or acquire it). Power management electronics (PCDU/PMAD at data-center scale) is similarly **pending scale-up**, not a capability gap. The "end-to-end prime" claim is strong for launch + bus + power + comms + mechanisms; the thermal subsystem, the critical-path technology for a compute satellite, is the one piece **still pending in-house development**.

**Overall confidence: Medium-High.** Solar, mechanisms, comms, bus and components capabilities are well-documented. The data-center silicon array is real but early-stage (announced Feb 2026, no datasheet, no named customer order). That Rocket Lab has no large-scale deployable-radiator product on the shelf today is an inference from absence of a public product, not a confirmed exclusion, and the underlying thermal-control competency is in-house.

---

## 1. Solar — SolAero and the Solar Array Portfolio

### 1.1 SolAero acquisition and what it makes

Rocket Lab closed the acquisition of **SolAero Holdings** (Albuquerque, New Mexico) in **January 2022 for ~$80 million** ([Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-closes-acquisition-of-space-solar-power-products-company-solaero-holdings-inc/), [TechCrunch](https://techcrunch.com/2022/01/18/rocket-lab-acquires-solaero-holdings-for-80m-to-boost-space-solar-cell-production/)). SolAero is one of only **two US companies** that produce space-grade compound-semiconductor (III-V) solar cells. SolAero hardware has flown on 1,000+ missions including the **James Webb Space Telescope**, Mars **InSight**, and the Mars **Ingenuity** helicopter ([Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-closes-acquisition-of-space-solar-power-products-company-solaero-holdings-inc/)).

Critically, Rocket Lab is **"the world's only fully vertically integrated space power supplier"** — it makes solar cells, Coverglass Interconnected Cells (CICs), panel substrates, complete panels, and integrated array wings all in-house ([Rocket Lab — Solar Solutions](https://rocketlabcorp.com/space-systems/solar/), [Rocket Lab — Customizable Solar Arrays](https://rocketlabcorp.com/updates/rocket-lab-expands-satellite-solutions-with-customizable-solar-arrays/)).

### 1.2 Solar cell efficiency (confirmed)

- **Latest cells and CICs reach up to ~34% efficiency** — among the highest commercially available ([Rocket Lab — Space Solar Cells/CICs](https://rocketlabcorp.com/space-systems/solar/space-solar-cellscics/), [pv magazine](https://www.pv-magazine.com/2022/03/10/rocket-lab-unveils-space-solar-cell-with-33-3-efficiency/)).
- Cell product lines: triple-junction (**ZTJ, ZTJ+, ZTJ-Ω**), quad-junction (**Z4J, Z4J+**), and five-junction **IMM-β** (Inverted MetaMorphic), with cell areas up to **81.5 cm²** ([Rocket Lab — Space Solar Cells/CICs](https://rocketlabcorp.com/space-systems/solar/space-solar-cellscics/)).
- **IMM-β**: ~**33.3% conversion efficiency** in volume production, **>40% lighter** than typical space-grade cells, radiation-hard (87% power-remaining after 1E15 e/cm² 1-MeV electron fluence ≈ ~15 years GEO life). Entered qualification March 2022 ([Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-begins-qualification-of-highest-performing-space-solar-cell-technology/), [Interesting Engineering](https://interestingengineering.com/science/space-solar-panels-33), [Business Wire](https://www.businesswire.com/news/home/20220308006340/en/Rocket-Lab-Begins-Qualification-of-Highest-Performing-Space-Solar-Cell-Technology)).

*Note on numbers:* "Up to 34%" (current marketing) and "33.3%" (IMM-β volume figure) are consistent — IMM-β is the highest-efficiency line; "up to 34%" is the portfolio ceiling. Both are confirmed by 2+ sources.

### 1.3 STARRAY — productized solar arrays (April 2025)

Rocket Lab launched **STARRAY** ("Standardized Array") at the 40th Space Symposium, April 2025 — a family of pre-engineered, customizable solar arrays ([Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-expands-satellite-solutions-with-customizable-solar-arrays/), [Space.com](https://www.space.com/space-exploration/tech/rocket-lab-introduces-line-of-customizable-solar-arrays-for-satellites)):

- **Power range: ~100 W to >2,000 W**, via up to **four panels per wing** (confirmed by [Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-expands-satellite-solutions-with-customizable-solar-arrays/) and [SatNow](https://www.satnow.com/news/details/3135-rocket-lab-introduces-starray-solar-arrays-for-flexible-satellite-power-solutions)).
- **Seven variable array sizes**; uses radiation-hardened **quadruple-junction** cells.
- Available in **both rigid and deployable configurations** — confirmed by multiple sources ([SatNow](https://www.satnow.com/news/details/3135-rocket-lab-introduces-starray-solar-arrays-for-flexible-satellite-power-solutions), [Interesting Engineering](https://interestingengineering.com/innovation/rocket-labs-solar-arrays-satellites)).
- Positioned as "plug-and-play" — pre-engineered to cut non-recurring engineering cost.

### 1.4 Silicon solar arrays for space-based data centers (February 2026)

On **26 February 2026** Rocket Lab announced **advanced silicon solar arrays** designed specifically to power **gigawatt-scale space-based data centers spanning kilometers in orbit** ([Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/), [GlobeNewswire](https://www.globenewswire.com/news-release/2026/02/26/3246118/0/en/Rocket-Lab-Introduces-Advanced-Silicon-Solar-Arrays-To-Power-Space-Based-Data-Centers.html)).

Key points (all from the press release / GlobeNewswire — single primary source, widely syndicated):

- **Why silicon:** Traditional space cells use gallium arsenide and germanium — both **critical minerals with geopolitically constrained supply**. Silicon is abundant and cheap; the move **de-risks the supply chain** and enables industrial-scale volume.
- **Capabilities:** mass-manufacturable, **lightweight, modular, radiation-hardened** silicon cell modules; **low cost per watt at industrial scale**; targets **gigawatt-class** power generation.
- **Flexibility/deployment:** the modules are described as **flexible and lightweight**, explicitly to support "a variety of stowage and deployment methods tailored to any mission" — i.e., compatible with compact-stow / roll-out architectures (relevant for fairing packing).
- **Hybrid option:** Rocket Lab offers a **hybrid array** mixing silicon with high-efficiency III-V cells — III-V where size/weight/power is at a premium, silicon where cost/schedule/scale dominate.
- **Manufacturing backing:** supported by a **$23.9M CHIPS Act award** to expand the Albuquerque compound-semiconductor facility, increasing capacity by **~50% within three years** ([NIST CHIPS](https://www.nist.gov/chips/rocket-lab-new-mexico-albuquerque), [New Electronics](https://www.newelectronics.co.uk/content/news/rocket-lab-signs-239m-chips-incentives-award/)). Note: the CHIPS award targets III-V cell capacity; the silicon line is a separate, newer product thrust.

**Caveats / flags (estimate vs. confirmed):**
- No public **datasheet, cost-per-watt figure, or efficiency number** for the silicon arrays. "Gigawatt-scale" and "kilometers in orbit" are Rocket Lab's framing, not specified deliverables.
- **No named customer order** for the data-center silicon arrays was found as of May 2026. A widely cited April 2026 commentary piece linked Rocket Lab to Meta's space-based solar interest ([24/7 Wall St.](https://247wallst.com/investing/2026/04/27/why-metas-space-based-solar-pact-is-really-a-rocket-lab-story/)), but this is analyst speculation, not a confirmed contract — treat as **unconfirmed**.
- Rocket Lab positions itself in this announcement as a **supplier of power infrastructure** to the orbital-data-center industry, not as a data-center operator.

### 1.5 Roll-out / flexible vs. rigid

Rocket Lab supplies **both rigid PVA panels and flexible PVA panels**, plus panel substrates (CFRP facesheet, aluminum-honeycomb) ([Rocket Lab — Solar Panels & Substrates](https://rocketlabcorp.com/space-systems/solar/substrates-and-panels/)). Flexible/lightweight modules are central to the silicon data-center product. However, Rocket Lab has **not publicly demonstrated a flight-proven large roll-out array** (e.g., ROSA-class). The capability is claimed/adjacent rather than demonstrated — see Open Questions.

---

## 2. Deployable & Expandable Structures

- **Composite structures in-house:** Rocket Lab manufactures CFRP facesheet and aluminum-honeycomb panel substrates and satellite panel structures, plus carbon-composite tanks and structures shared with its launch-vehicle composites heritage ([Rocket Lab — Solar Panels & Substrates](https://rocketlabcorp.com/space-systems/solar/substrates-and-panels/), [Rocket Lab — Spacecraft](https://rocketlabcorp.com/space-systems/spacecraft/)).
- **Deployable solar arrays:** STARRAY ships in deployable configurations; the silicon data-center array is explicitly designed for "a variety of stowage and deployment methods." This is the closest Rocket Lab gets to "pack a large array into a small fairing and unfold it."
- **Robotic deployment / mechanisms (Motiv):** The **Motiv Space Systems** acquisition (signed 6 May 2026, **completed 26 May 2026**, ~$60M total: **$40M cash plus a contingent equity earnout**) adds **multi-degree-of-freedom robotic arms, actuators and drive electronics**, rebranded **Rocket Lab Robotics** ([Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-to-acquire-robotics-leader-motiv-space-systems/), [Aviation Week](https://aviationweek.com/space/space-exploration/rocket-lab-buy-motiv-space-40m-adding-robotics-solar-drives), [GlobeNewswire](https://www.globenewswire.com/news-release/2026/05/07/3290619/0/en/rocket-lab-to-acquire-robotics-leader-motiv-space-systems.html)). Motiv robotics flew on Mars **Perseverance** and the **CADRE** lunar rovers. Robotic arms are relevant to on-orbit assembly / deployment of very large structures.

**Gap flag:** No evidence Rocket Lab builds a *dedicated* large expandable/deployable boom or truss product (analogous to Northrop's ROSA or large deployable-boom systems). Deployment is handled via STARRAY hinges/SADAs and, prospectively, robotics — adequate for satellite-scale arrays, unproven for kilometer-scale structures.

---

## 3. Actuators & Mechanisms

| Capability | Source company | Status | Notes |
|---|---|---|---|
| **Solar Array Drive Assemblies (SADAs)** | Motiv | Closed 26 May 2026 | "Closes one of the final gaps in vertical integration" (Rocket Lab's own words) |
| **Antenna & propulsion gimbals** | Motiv | Closed 26 May 2026 | Precision pointing mechanisms |
| **Precision drive electronics, filter wheels, actuators** | Motiv | Closed 26 May 2026 | Mars-proven motion-control heritage |
| **Robotic arms (multi-DOF)** | Motiv | Closed 26 May 2026 | Perseverance, CADRE rover heritage |
| **Separation systems** | Planetary Systems Corp (acq. Dec 2021, ~$81.4M) | In-house, flying | Maryland; satellite/payload separation, dispensers |
| **Reaction wheels** | Sinclair Interplanetary (acq. April 2020) | In-house, flying | On 200+ satellites incl. BlackSky, Kepler; dedicated high-volume reaction-wheel production facility |
| **Star trackers** | Sinclair Interplanetary | In-house, flying | Best-in-class small-sat attitude sensing |

Sources: [SpaceNews — Sinclair](https://spacenews.com/rocket-lab-to-acquire-smallsat-component-manufacturer/), [Rocket Lab — Sinclair close](https://rocketlabcorp.com/updates/rocket-lab-closes-acquisition-of-satellite-hardware-manufacturer-sinclair-interplanetary/), [Wikipedia — Rocket Lab](https://en.wikipedia.org/wiki/Rocket_Lab), [Aviation Week — Motiv](https://aviationweek.com/space/space-exploration/rocket-lab-buy-motiv-space-40m-adding-robotics-solar-drives), [GovConWire — Motiv](https://www.govconwire.com/articles/rocket-lab-acquisition-motiv-space-systems).

**Assessment:** With Motiv now closed (26 May 2026), Rocket Lab's mechanism portfolio is essentially complete for a satellite: attitude control (wheels/trackers), array articulation (SADAs), pointing (gimbals), separation, and robotic manipulation are all in-house. SADAs in particular were a known supply-constrained bottleneck the company has now eliminated.

---

## 4. Satellite Bus / Platforms

- **Photon** — bus derived from the Electron kick stage; customizable for LEO hosting, lunar, and interplanetary missions. Heritage: NASA **CAPSTONE** (lunar), Varda **Pioneer** spacecraft. Photon is a proven but **modest-power, small/medium-class** bus — not sized for a high-power compute payload on its own ([Rocket Lab — Spacecraft](https://rocketlabcorp.com/space-systems/spacecraft/), [Wikipedia — Photon](https://en.wikipedia.org/wiki/Rocket_Lab_Photon)).
- **Flatellite** — unveiled **27 February 2025**: a flat, **stackable, high-power, mass-manufacturable** satellite for large constellations, designed for tight integration with Neutron (**stacks of up to ~16 per launch**). Integrates Rocket Lab heritage subsystems: propulsion, flight software, avionics, reaction wheels, star trackers, separation system, solar arrays, radios, composite structures, fuel tanks ([Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-announces-flatellite-a-new-satellite-designed-for-mass-manufacture-and-tailored-for-large-constellations/), [SpaceQ](https://spaceq.ca/rocket-lab-unveils-flatellite-satellite-platform/)).
  - **Mass/power: NOT officially published.** A third-party analysis estimates **slightly over ~800 kg**; power is described only as "high-power." Treat mass and power as **estimates** ([Orbital Today](https://orbitaltoday.com/2025/03/03/new-mass-manufacture-satellite-flatellite-announced/), [illdefined.space](https://www.illdefined.space/stacking-the-deck-rocket-labs-flatellite/)).
  - Flatellite is being produced for the **$816M SDA prime contract** (18 satellites) — validating it as a real production platform, not a render.
- **"Flatellite" as a compute host:** Its flat, high-power, mass-manufacturable design is the most plausible Rocket Lab bus for hosting a compute payload, and its design intent (large constellations, tight Neutron integration) aligns with a distributed orbital-compute architecture. But no public spec confirms it can supply data-center-class power or reject data-center-class heat. **Inference, not confirmed.**

---

## 5. Other Components & the Electronics / Payload Companies

**In-house component catalog (confirmed, flying):**

- **Frontier radios** — software-defined space-grade RF, **L/S/C/X/Ka-band**, 13+ years flight heritage (CAPSTONE, Europa Clipper, Parker Solar Probe, Van Allen Probes, Varda Pioneer). Compatible with Deep Space Network, Near Earth Network, AFSCN, KSAT, etc. ([Rocket Lab](https://rocketlabcorp.com/updates/a-new-frontier-in-radios-rocket-lab-announces-expanded-radio-products-for-reliable-command-and-control/), [Business Wire](https://www.businesswire.com/news/home/20250403572210/en/A-New-Frontier-in-Radios-Rocket-Lab-Announces-Expanded-Radio-Products-for-Reliable-Command-and-Control)).
- **Reaction wheels, star trackers, separation systems** — see §3.
- **Solar cells/CICs/panels/arrays** — see §1.
- **Composite structures and tanks, flight & ground software, propulsion** (incl. electric propulsion).

**The EO/IR payload company — Geost:**
Rocket Lab acquired **Geost** (Tucson, Arizona) — announced May 2025, **closed 12 August 2025**, for **$275M** ($125M cash + $150M stock, up to $50M earnout) ([SpaceNews](https://spacenews.com/rocket-lab-to-acquire-satellite-payload-manufacturer-geost-for-275-million/), [Rocket Lab — close](https://rocketlabcorp.com/updates/rocket-lab-closes-acquisition-of-geost-expanding-its-national-security-capabilities-with-launch-spacecraft-and-now-payloads/), [GovConWire](https://www.govconwire.com/articles/rocket-lab-completes-geost-acquisition)). Geost builds **electro-optical/infrared (EO/IR) sensor payloads** for missile warning/tracking, ISR, Earth observation, and space domain awareness — and notably **also makes laser communication terminals and autonomous optical ground stations**. This is Rocket Lab's entry into the **payload** business and adds avionics/electro-optical electronics capability.

**Laser communications — Mynaric:**
Rocket Lab **completed the Mynaric AG acquisition on 14 April 2026** (~$155.3M: nominal cash + 2,277,002 RKLB shares) ([Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-completes-mynaric-acquisition-adding-laser-optical-communications-to-growing-space-systems-portfolio/), [SpaceNews](https://spacenews.com/rocket-lab-to-expand-into-laser-communications-with-mynaric-acquisition/)). Mynaric's **CONDOR** optical inter-satellite terminals:
- **CONDOR Mk2:** 0.1–1.25 Gbps. **CONDOR Mk3:** ships configured at **~2.5 Gbps as-delivered** (SDA Tranche 1; the official Via Satellite description is a "configurable modem up to ~2.5 Gbps") ([Via Satellite](https://www.satellitetoday.com/government-military/2025/06/05/mynaric-reports-condor-mk3-delivery-milestone-progress-on-mk3-1-terminal-for-sda/)).
- **CONDOR Mk3.1** in development targeting **up to 100 Gbps** (SDA Tranche 2) — the 100 Gbps figure is the Mk3.1 roadmap, not a Mk3 ceiling. *(Harmonized 2026-05-17 with `laser_comms/optical_comms.md` and `constellation_mesh.md`: Mk3 as-delivered ~2.5 Gbps, Mk3.1 targets up to 100 Gbps.)*
- Already supplying CONDOR Mk3 terminals into Rocket Lab's SDA constellation work. High-bandwidth inter-satellite links are essential for a distributed orbital-compute network.

---

## 6. Assessment — Capability Coverage for a Compute Node

A compute satellite node needs, at minimum: **(a) large deployable solar power, (b) deployable thermal radiators, (c) actuators/mechanisms, (d) a satellite bus, (e) high-bandwidth comms (laser), (f) power management/distribution, (g) compute payload integration.**

### Coverage table

| Subsystem needed | Rocket Lab in-house? | Strength | Notes |
|---|---|---|---|
| Space-grade solar cells | **Yes — owns** | Very strong | SolAero; only fully vertically integrated supplier; up to ~34% efficiency |
| Deployable / large-area solar arrays | **Yes — owns** | Strong | STARRAY (rigid + deployable); new silicon arrays for GW-scale data centers (early-stage) |
| Compact-stow / roll-out / flexible arrays | **Partial** | Moderate | Flexible PVA panels + silicon modules claimed deployment-flexible; no flight-proven large roll-out array |
| **Deployable thermal radiators** | **Pending in-house build** | **Pending (in their wheelhouse)** | No large-scale radiator product on the shelf today, but Rocket Lab flies its own thermal control and owns the composite + mechanism + solar know-how; expected in-house development. Critical-path item |
| Actuators / SADAs / gimbals | **Yes, owns** | Strong | Motiv (closed 26 May 2026), "Rocket Lab Robotics" |
| Reaction wheels / star trackers | **Yes — owns** | Very strong | Sinclair; on 200+ satellites |
| Separation systems / dispensers | **Yes — owns** | Strong | Planetary Systems Corp |
| Robotic arms / on-orbit manipulation | **Yes, owns** | Strong | Motiv (closed 26 May 2026); Mars/lunar heritage |
| Satellite bus / platform | **Yes — owns** | Moderate–Strong | Photon (small/med); Flatellite (high-power, stackable, Neutron-matched) — power/mass unpublished |
| RF radios | **Yes — owns** | Very strong | Frontier, multi-band, deep flight heritage |
| Laser inter-satellite comms | **Yes — owns** | Strong | Mynaric CONDOR Mk3; ~2.5 Gbps as-delivered, 100 Gbps on the Mk3.1 roadmap |
| EO/IR & optical payload electronics | **Yes — owns** | Strong | Geost |
| Power management / distribution (PCDU/PMAD) at scale | **Pending scale-up** | Moderate | Bus-level power electronics exist; data-center-scale PMAD is a scale-up of an existing competency, not yet a published product |
| Compute payload (servers/silicon) | **No** | Out of scope | Rocket Lab is not a compute-hardware maker; would integrate a third-party payload |
| Launch vehicle (Neutron) | **Yes — owns** | Strong (pre-flight) | Sized to deploy stacked Flatellites; maiden flight Q4 2026 |

### Verdict on the "end-to-end prime" claim

**Strong, with two pieces still pending in-house build-out.** Rocket Lab genuinely owns nearly every *spacecraft-bus and power* subsystem a compute node needs: solar (best-in-class, vertically integrated), mechanisms (post-Motiv, closed 26 May 2026), attitude control, structures, RF and laser comms, and the launch vehicle. The $816M SDA prime contract proves it can deliver as a satellite prime. For the "build the satellite + power it + link it + launch it" scope, the claim holds up well.

**The two pieces still pending in-house development for a compute node specifically:**

1. **Deployable thermal radiators (critical path, in their wheelhouse).** Heat rejection is the gating problem for orbital compute, and Rocket Lab has no large-scale deployable-radiator product on the shelf today. But this is a pending in-house item, not a missing competency: Rocket Lab already flies its own thermal control on its satellites, and its composite-structures and (post-Motiv) deployment-mechanism capabilities feed directly into a node-scale radiator. It is a question of timing and scale, and the company would **develop it in-house (or acquire it)**.
2. **Data-center-scale power management electronics (PMAD/PCDU).** Bus-level power electronics exist; managing hundreds of kW to MW for a compute payload is a scale-up of that existing competency, pending rather than absent.

The **compute payload itself** (server silicon) is outside Rocket Lab's domain by design: it would integrate a partner's hardware, consistent with its stated role as a *power/infrastructure supplier* to the orbital-data-center market rather than an operator.

**Bottom line:** Rocket Lab could credibly be the prime for the *satellite platform, power, comms, mechanisms and launch* of a compute node today. To be a true end-to-end prime for an AI-inference data center, it would still develop in-house (or acquire) the **deployable radiator / thermal-rejection subsystem** and scale up **power management**: both sit squarely within existing competencies (its own satellite thermal control and bus power electronics), pending the timing and scale, rather than being gaps in the catalog.

---

## Sources

- [Rocket Lab — Solar Solutions](https://rocketlabcorp.com/space-systems/solar/)
- [Rocket Lab — Solar Panels & Substrates](https://rocketlabcorp.com/space-systems/solar/substrates-and-panels/)
- [Rocket Lab — Space Solar Cells/CICs](https://rocketlabcorp.com/space-systems/solar/space-solar-cellscics/)
- [Rocket Lab — Closes Acquisition of SolAero](https://rocketlabcorp.com/updates/rocket-lab-closes-acquisition-of-space-solar-power-products-company-solaero-holdings-inc/)
- [TechCrunch — Rocket Lab acquires SolAero for $80M](https://techcrunch.com/2022/01/18/rocket-lab-acquires-solaero-holdings-for-80m-to-boost-space-solar-cell-production/)
- [Rocket Lab — Begins Qualification of Highest-Performing Space Solar Cell (IMM-β)](https://rocketlabcorp.com/updates/rocket-lab-begins-qualification-of-highest-performing-space-solar-cell-technology/)
- [Business Wire — IMM-β qualification](https://www.businesswire.com/news/home/20220308006340/en/Rocket-Lab-Begins-Qualification-of-Highest-Performing-Space-Solar-Cell-Technology)
- [pv magazine — Rocket Lab 33.3% space solar cell](https://www.pv-magazine.com/2022/03/10/rocket-lab-unveils-space-solar-cell-with-33-3-efficiency/)
- [Interesting Engineering — IMM-β 33.3%](https://interestingengineering.com/science/space-solar-panels-33)
- [Rocket Lab — STARRAY customizable solar arrays](https://rocketlabcorp.com/updates/rocket-lab-expands-satellite-solutions-with-customizable-solar-arrays/)
- [Space.com — Rocket Lab customizable solar arrays](https://www.space.com/space-exploration/tech/rocket-lab-introduces-line-of-customizable-solar-arrays-for-satellites)
- [SatNow — STARRAY solar arrays](https://www.satnow.com/news/details/3135-rocket-lab-introduces-starray-solar-arrays-for-flexible-satellite-power-solutions)
- [Interesting Engineering — STARRAY 100W–2,000W](https://interestingengineering.com/innovation/rocket-labs-solar-arrays-satellites)
- [Rocket Lab — Advanced Silicon Solar Arrays for Space-Based Data Centers](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/)
- [GlobeNewswire — Silicon Solar Arrays announcement](https://www.globenewswire.com/news-release/2026/02/26/3246118/0/en/Rocket-Lab-Introduces-Advanced-Silicon-Solar-Arrays-To-Power-Space-Based-Data-Centers.html)
- [NIST CHIPS — Rocket Lab New Mexico](https://www.nist.gov/chips/rocket-lab-new-mexico-albuquerque)
- [New Electronics — Rocket Lab $23.9M CHIPS award](https://www.newelectronics.co.uk/content/news/rocket-lab-signs-239m-chips-incentives-award/)
- [24/7 Wall St. — Meta space-based solar / Rocket Lab commentary](https://247wallst.com/investing/2026/04/27/why-metas-space-based-solar-pact-is-really-a-rocket-lab-story/)
- [Rocket Lab — To Acquire Motiv Space Systems](https://rocketlabcorp.com/updates/rocket-lab-to-acquire-robotics-leader-motiv-space-systems/)
- [Aviation Week — Rocket Lab buys Motiv for $40M, adds robotics/solar drives](https://aviationweek.com/space/space-exploration/rocket-lab-buy-motiv-space-40m-adding-robotics-solar-drives)
- [GovConWire — Rocket Lab acquisition of Motiv](https://www.govconwire.com/articles/rocket-lab-acquisition-motiv-space-systems)
- [GlobeNewswire — Rocket Lab to acquire Motiv](https://www.globenewswire.com/news-release/2026/05/07/3290619/0/en/rocket-lab-to-acquire-robotics-leader-motiv-space-systems.html)
- [SpaceNews — Rocket Lab to acquire Sinclair Interplanetary](https://spacenews.com/rocket-lab-to-acquire-smallsat-component-manufacturer/)
- [Rocket Lab — Closes Sinclair Interplanetary acquisition](https://rocketlabcorp.com/updates/rocket-lab-closes-acquisition-of-satellite-hardware-manufacturer-sinclair-interplanetary/)
- [Rocket Lab — Star Trackers and Reaction Wheels (components)](https://rocketlabcorp.com/space-systems/satellite-components/)
- [Wikipedia — Rocket Lab](https://en.wikipedia.org/wiki/Rocket_Lab)
- [Rocket Lab — Announces Flatellite](https://rocketlabcorp.com/updates/rocket-lab-announces-flatellite-a-new-satellite-designed-for-mass-manufacture-and-tailored-for-large-constellations/)
- [SpaceQ — Rocket Lab unveils Flatellite](https://spaceq.ca/rocket-lab-unveils-flatellite-satellite-platform/)
- [Orbital Today — Flatellite mass estimate](https://orbitaltoday.com/2025/03/03/new-mass-manufacture-satellite-flatellite-announced/)
- [illdefined.space — Stacking the Deck: Rocket Lab's Flatellite](https://www.illdefined.space/stacking-the-deck-rocket-labs-flatellite/)
- [Rocket Lab — Spacecraft (Space Systems)](https://rocketlabcorp.com/space-systems/spacecraft/)
- [Wikipedia — Rocket Lab Photon](https://en.wikipedia.org/wiki/Rocket_Lab_Photon)
- [Rocket Lab — Frontier radios expanded products](https://rocketlabcorp.com/updates/a-new-frontier-in-radios-rocket-lab-announces-expanded-radio-products-for-reliable-command-and-control/)
- [Business Wire — Frontier radio products](https://www.businesswire.com/news/home/20250403572210/en/A-New-Frontier-in-Radios-Rocket-Lab-Announces-Expanded-Radio-Products-for-Reliable-Command-and-Control)
- [SpaceNews — Rocket Lab to acquire Geost for $275M](https://spacenews.com/rocket-lab-to-acquire-satellite-payload-manufacturer-geost-for-275-million/)
- [Rocket Lab — Closes Geost acquisition](https://rocketlabcorp.com/updates/rocket-lab-closes-acquisition-of-geost-expanding-its-national-security-capabilities-with-launch-spacecraft-and-now-payloads/)
- [GovConWire — Rocket Lab completes Geost acquisition](https://www.govconwire.com/articles/rocket-lab-completes-geost-acquisition)
- [Rocket Lab — Completes Mynaric acquisition](https://rocketlabcorp.com/updates/rocket-lab-completes-mynaric-acquisition-adding-laser-optical-communications-to-growing-space-systems-portfolio/)
- [SpaceNews — Rocket Lab to expand into laser communications with Mynaric](https://spacenews.com/rocket-lab-to-expand-into-laser-communications-with-mynaric-acquisition/)
- [Via Satellite — Mynaric CONDOR Mk3 / Mk3.1 progress](https://www.satellitetoday.com/government-military/2025/06/05/mynaric-reports-condor-mk3-delivery-milestone-progress-on-mk3-1-terminal-for-sda/)

---

## Open Questions / Uncertainties

- **Deployable radiators:** No public large-scale deployable-radiator product from Rocket Lab today. Confirm the scope of its existing in-house thermal-control capability and the path to a node-scale radiator; this is the single most important pending in-house item for a compute node (critical path), and it sits in their wheelhouse rather than being a capability gap.
- **Silicon data-center array specs** — No datasheet: efficiency, cost-per-watt, areal mass, deployment mechanism, and TRL are all unpublished. "Gigawatt-scale" is marketing framing, not a delivered capability.
- **Silicon array customer** — No confirmed order. The Meta connection is analyst speculation; verify before relying on it.
- **Flatellite power & mass** — Officially unpublished. ~800 kg is a third-party estimate; "high-power" is undefined. Whether Flatellite can host a high-power compute payload is unconfirmed.
- **Roll-out array maturity** — Rocket Lab makes flexible PVA panels but has not demonstrated a flight-proven large roll-out/compact-stow array; the compact-stow claim for the silicon line is design intent, not demonstrated hardware.
- **Power management at scale:** Whether Rocket Lab has PMAD/PCDU electronics suitable for data-center-class loads (hundreds of kW–MW) is unclear from public sources; bus-level power electronics exist, so this is a pending scale-up of an existing competency.
- **Motiv close:** The Motiv (SADA/robotics) acquisition is closed (signed 6 May 2026, completed 26 May 2026, ~$60M total: $40M cash plus a contingent equity earnout); SADA/gimbal capability is now in-house.
- **On-orbit assembly** — Whether Rocket Lab Robotics (Motiv) capability extends to assembling kilometer-scale structures, vs. satellite-scale manipulation, is unconfirmed.
