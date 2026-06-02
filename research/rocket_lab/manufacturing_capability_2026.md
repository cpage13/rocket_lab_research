# Rocket Lab: Demonstrated Manufacturing-Process Competency (2026)

**Prepared:** June 2026 · **For:** RKLB space-data-center feasibility study
**Scope:** Evidence that Rocket Lab is, today, a high-volume, vertically integrated MANUFACTURER of complex aerospace hardware, and a qualitative argument for why that manufacturing-PROCESS competency transfers to building orbital data-center "nodes" on a production line. This doc is about the *process* track record (additive manufacturing, automated composites, serial production rates, factories, design-for-manufacture), not about *which* subsystems Rocket Lab owns (that is `rocket_lab/space_hardware_capabilities.md`) and not about the general production-line-versus-bespoke economics or Wright's-law learning curves (those live in the node-design and economics docs).

---

## Source-Status Banner

This doc uses the project source taxonomy (see [research/SOURCE_INDEX.md](../SOURCE_INDEX.md)). Inline tags:

- **[FACT]**, directly supported by a primary or reputable secondary source, cited inline. Most production rates, print times, and machine specs here are [FACT].
- **[INFERENCE]**, reasoned from sourced facts; the reasoning is stated.
- **[ESTIMATE]**, a number this doc supplies or rounds; flagged as such.

A specific caution for this topic: **demonstrated/current capability is distinguished from announced/planned capability throughout.** Electron-class manufacturing (Rutherford engines, Rosie composites) is flight-proven and running at volume today. Neutron-class manufacturing (the automated fiber placement machine, the Archimedes production line) is *installed and standing up* but has not yet supported a flown vehicle as of June 2026. The transfer argument leans on the demonstrated Electron/Space-Systems record, with Neutron as strong corroborating evidence of intent and tooling, not as proof.

---

## BLUF (Bottom Line Up Front)

The structural case argues an orbital node should be built like a manufactured **product** on a production line, not as a bespoke one-off. That thesis only holds if the operator can actually run high-volume, repeatable manufacturing of complex aerospace hardware. **Rocket Lab already does exactly this as its core business, and has for years.** Three independent pieces of demonstrated evidence:

1. **Serial additive manufacturing of rocket engines.** The Rutherford engine is "one of the most-manufactured rocket engines on Earth": the **1,000th** unit rolled off the line in **May 2026** [FACT], with primary components (combustion chamber, injectors, pumps, propellant valves) **3D-printed in ~24 hours** [FACT] and production scaled from roughly **one engine per month (2017) to a ~200-units-per-year target** [FACT]. This is mass production of a complex, flight-critical part via additive manufacturing, demonstrated at scale.

2. **Automated composite production.** Rocket Lab's "Rosie the Robot" cell builds the carbon-composite structures of an **entire Electron in ~12 hours**, work that previously took **400+ hours** of hand labor [FACT]. The company sustains a rocket rolling off the Electron line roughly **every 18-20 days** [FACT] and flew **21 Electron missions in 2025 at 100% success** [FACT, per `electron/electron_specs.md`].

3. **Design-for-manufacture, applied deliberately, twice over.** For the Neutron-class Archimedes engine, Peter Beck describes skipping the usual one-off-prototype path: **"We didn't do that. We built a production line"** [FACT]. In Space Systems, Rocket Lab unveiled **Flatellite**, a satellite "designed for mass manufacture" and "built fast in high volumes," produced at a Long Beach **Spacecraft Production Complex** with a dedicated high-volume spacecraft line [FACT].

**Transfer takeaway [INFERENCE]:** A data-center node is, physically, a composite-structured spacecraft bus carrying a power system, a thermal system, comms, and a payload. Every *process* competency a production-line node program needs (additive manufacture of metal parts, automated carbon-composite layup with inline inspection, serial assembly-and-test cadence, factories co-located with the launch path, and a culture that designs for the production line from day one) is something Rocket Lab demonstrably already runs for rockets and satellites. The production-line thesis therefore carries **low manufacturing-process execution risk** relative to its other risks (thermal/radiator subsystem, node power scale, orbital economics). The hard, unproven parts of an orbital data center are not "can it be built repeatably"; they are elsewhere.

---

## 1. Launch-Vehicle Manufacturing

### 1.1 Rutherford engine: mass production by additive manufacturing (DEMONSTRATED)

The Rutherford is the engine that powers Electron: nine on the first stage, one vacuum-optimized on the second stage ([Rocket Lab Electron specs](https://en.wikipedia.org/wiki/Rocket_Lab_Electron), and `electron/electron_specs.md`). What matters for the manufacturing-competency argument is *how* it is made and at *what rate*.

**Additive manufacturing of all primary components [FACT].** Rutherford was the first orbital-class engine to produce all of its primary components (combustion chamber, injectors, pumps, and main propellant valves) by metal additive manufacturing (3D printing), historically via **electron-beam melting (EBM)** ([The Fabricator: Rocket Lab 100th 3D-printed engine](https://www.thefabricator.com/additivereport/news/additive/rocket-lab-celebrates-completion-of-its-100th-3d-printed-engine); [Rocket Lab: 100th Rutherford build](https://rocketlabcorp.com/updates/rocket-lab-celebrates-100th-rutherford-engine-build/)).

**~24-hour print time for primary components [FACT].** Rocket Lab states the primary printed components can be produced in roughly **24 hours**, a fraction of the time required by conventional machining and casting ([The Fabricator](https://www.thefabricator.com/additivereport/news/additive/rocket-lab-celebrates-completion-of-its-100th-3d-printed-engine); [VoxelMatters: 1,000th Rutherford](https://www.voxelmatters.com/rocket-lab-rolls-the-1000th-rutherford-engine-off-its-production-line/)). This compresses the part-fabrication step from weeks to a day, which is the enabling condition for serial volume.

**Production volume and rate [FACT].** Rocket Lab announced the **1,000th Rutherford engine** off its production line in **May 2026**, calling it "one of the most manufactured rocket engines on Earth" ([Rocket Lab on X, 16 May 2026](https://x.com/RocketLab/status/2055097584541442066); [3D Printing Industry: 1,000 units](https://3dprintingindustry.com/news/rocket-labs-3d-printed-engine-hits-1000-units-251599/); [VoxelMatters](https://www.voxelmatters.com/rocket-lab-rolls-the-1000th-rutherford-engine-off-its-production-line/)). Reporting on the milestone describes production scaling from **approximately one engine per month in 2017 to a target of around 200 units annually** ([VoxelMatters](https://www.voxelmatters.com/rocket-lab-rolls-the-1000th-rutherford-engine-off-its-production-line/); [3D ADEPT: additive manufacturing as a moat](https://3dadept.com/rocket-labs-1000th-rutherford-engine-when-additive-manufacturing-becomes-a-competitive-moat/)). By late 2025, **over 800 Rutherford engines had flown** across 70+ Electron launches ([VoxelMatters: AM scales Electron to Neutron](https://www.voxelmatters.com/rocket-lab-targets-1000th-rutherford-engine-launch-as-am-scales-from-electron-to-neutron/)). Since nine engines fly per Electron first stage, 1,000 engines is on the order of ~90 vehicles' worth of additively manufactured propulsion hardware [INFERENCE, arithmetic on the cited 9-engine figure].

**In-house printing fleet and supply chain [FACT].** Engines are produced at Rocket Lab's Long Beach facility on in-house metal 3D-printing systems from **EOS, Nikon SLM Solutions, and Renishaw**, with metal powders supplied by **Carpenter Technology** ([VoxelMatters](https://www.voxelmatters.com/rocket-lab-rolls-the-1000th-rutherford-engine-off-its-production-line/); [3D ADEPT](https://3dadept.com/rocket-labs-1000th-rutherford-engine-when-additive-manufacturing-becomes-a-competitive-moat/)). Rocket Lab has also signed for an ultra-large metal AM platform from Nikon SLM Solutions to support larger parts ([VoxelMatters: AM scales Electron to Neutron](https://www.voxelmatters.com/rocket-lab-targets-1000th-rutherford-engine-launch-as-am-scales-from-electron-to-neutron/)).

*Why this is the relevant kind of evidence:* a rocket engine is among the most demanding mass-produced objects in industry, high pressure, high temperature, flight-critical, zero tolerance for defects. Demonstrating it at four-digit unit volumes is strong proof of repeatable, quality-controlled manufacturing, not a prototype-shop capability.

### 1.2 Electron: automated carbon-composite production ("Rosie the Robot") (DEMONSTRATED)

Electron's airframe and tanks are fully carbon-composite (`electron/electron_specs.md`). Composite layup is normally labor-intensive; Rocket Lab automated it.

**"Rosie the Robot" automated production cell [FACT].** Introduced in late 2019, Rosie is a custom robotic manufacturing system that produces the carbon-composite components of an Electron in **about 12 hours**, a process that previously required **more than 400 hours** of hand labor ([SpaceNews: robotic manufacturing system to increase Electron production](https://spacenews.com/rocket-lab-introduces-robotic-manufacturing-system-to-increase-electron-production/); [Space.com: Rosie builds a booster in 12 hours](https://www.space.com/rocket-lab-rosie-robot-build-rocket-12-hours.html); [TechCrunch: Rosie speeds up production](https://techcrunch.com/2019/11/13/rocket-labs-new-rosie-the-robot-speeds-up-launch-vehicle-production-by-a-lot/)).

**Scope and scale of the cell [FACT].** Rosie occupies roughly **140 square meters** and comprises a **3.5 m × 16 m, 5-axis machining window with a custom sixth rotary axis**, large enough to machine an entire ~12 m Electron first stage as well as the upper stage, kick stage, and fairings. It performs cutting, drilling, sanding, and machining so parts are ready for final assembly ([Space.com](https://www.space.com/rocket-lab-rosie-robot-build-rocket-12-hours.html); [Digital Trends: Rosie the rocket-building robot](https://www.digitaltrends.com/space/rocket-lab-shows-off-rosie-its-rocket-building-robot/); [SpaceNews](https://spacenews.com/rocket-lab-introduces-robotic-manufacturing-system-to-increase-electron-production/)).

**Sustained serial cadence [FACT].** Rosie was explicitly part of a tooling push toward higher Electron production rates ([SpaceNews](https://spacenews.com/rocket-lab-introduces-robotic-manufacturing-system-to-increase-electron-production/)). Reporting describes a finished rocket rolling off the Electron line roughly **every 18-20 days** ([Interesting Engineering: Rosie helps build a launch vehicle every 20 days](https://interestingengineering.com/rocket-labs-rosie-helps-build-a-launch-vehicle-every-20-days)), and the operational outcome is documented in the launch record: **21 Electron launches in 2025 at 100% mission success** and ~80+ launches since 2017 (`electron/electron_specs.md`; [SpaceNews: record launch year](https://spacenews.com/rocket-lab-wraps-up-record-launch-year/)). The flight cadence is the proof that the production cadence is real, not aspirational.

### 1.3 Neutron: large-scale automated composites and a production-line Archimedes (ANNOUNCED / STANDING UP)

Neutron is pre-flight (maiden flight targeted Q4 2026, `rocket_lab/overview.md`), so its manufacturing is **announced and tooled, not yet flight-demonstrated**. But the *tooling itself* is installed and is direct evidence of how Rocket Lab intends to build large hardware.

**A 99-tonne automated fiber placement (AFP) machine [FACT].** Rocket Lab is installing a custom AFP machine built by **Electroimpact** (Mukilteo, Washington) at its **Space Structures Complex in Middle River, Maryland**. Key specs, confirmed across primary and trade sources:

| AFP machine parameter | Value | Source |
|---|---|---|
| Mass | **99 tons (~90 tonnes)** | [CompositesWorld](https://www.compositesworld.com/news/rocket-lab-begins-installation-of-large-afp-machine-for-rocket-production); [SpaceDaily](https://www.spacedaily.com/reports/Rocket_Lab_Installs_Advanced_Carbon_Composite_Manufacturing_System_for_Neutron_Rocket_Production_999.html) |
| Height | **~12 m (39 ft)** | [CompositesWorld](https://www.compositesworld.com/news/rocket-lab-begins-installation-of-large-afp-machine-for-rocket-production); [SpaceDaily](https://www.spacedaily.com/reports/Rocket_Lab_Installs_Advanced_Carbon_Composite_Manufacturing_System_for_Neutron_Rocket_Production_999.html) |
| Carbon-fiber lay-down rate | **up to 100 m/min (328 ft/min)** | [CompositesWorld](https://www.compositesworld.com/news/rocket-lab-begins-installation-of-large-afp-machine-for-rocket-production); [SpaceDaily](https://www.spacedaily.com/reports/Rocket_Lab_Installs_Advanced_Carbon_Composite_Manufacturing_System_for_Neutron_Rocket_Production_999.html) |
| Travel along part | **up to 30 m** | [CompositesWorld](https://www.compositesworld.com/news/rocket-lab-begins-installation-of-large-afp-machine-for-rocket-production) |
| Builds | **28 m interstage + fairing; 7 m-dia first stage; 5 m-dia second-stage tank** | [CompositesWorld](https://www.compositesworld.com/news/rocket-lab-begins-installation-of-large-afp-machine-for-rocket-production); [SpaceDaily](https://www.spacedaily.com/reports/Rocket_Lab_Installs_Advanced_Carbon_Composite_Manufacturing_System_for_Neutron_Rocket_Production_999.html) |
| Projected labor saved | **150,000+ manufacturing hours** at full-scale production | [CompositesWorld](https://www.compositesworld.com/news/rocket-lab-begins-installation-of-large-afp-machine-for-rocket-production); [Interesting Engineering](https://interestingengineering.com/space/3d-printing-beast-builds-worlds-largest-neutron-rocket) |
| Quality control | **fully automated real-time defect inspection** between layup passes | [CompositesWorld](https://www.compositesworld.com/news/rocket-lab-begins-installation-of-large-afp-machine-for-rocket-production); [SpaceDaily](https://www.spacedaily.com/reports/Rocket_Lab_Installs_Advanced_Carbon_Composite_Manufacturing_System_for_Neutron_Rocket_Production_999.html) |

The primary announcement is [Rocket Lab: begins installation of large carbon composite rocket-building machine](https://rocketlabcorp.com/updates/rocket-lab-begins-installation-of-large-carbon-composite-rocket-building-machine/). Beck framed it as combining "proprietary flight-proven carbon composite technology, additive manufacturing and autonomous robotics to design and build large-scale aerospace components at a pace that will support … Neutron's launch cadence" ([CompositesWorld](https://www.compositesworld.com/news/rocket-lab-begins-installation-of-large-afp-machine-for-rocket-production)). The same machine is slated to also produce Electron first stages and composite structures for spacecraft customers ([CompositesWorld](https://www.compositesworld.com/news/rocket-lab-begins-installation-of-large-afp-machine-for-rocket-production)), i.e., it is a shared production asset, not a one-program tool.

**Design-for-manufacture, stated explicitly ("we built a production line") [FACT].** For the Archimedes engine (nine per Neutron first stage), Beck contrasts Rocket Lab's approach with the industry norm of hand-integrating one-off prototypes from "a whole bunch of industrial items and all those Frankenstein bits": **"We didn't do that. We built a production line"** ([NASASpaceFlight: Beck Neutron update](https://www.nasaspaceflight.com/2025/10/beck-neutron-update/); [Everyday Astronaut: Neutron update interview with Peter Beck](https://everydayastronaut.com/neutron-update-interview-with-peter-beck/)). He describes standing up "the experienced team, manufacturing line, and test facilities required to support long-term production of Archimedes" *alongside* the engine's development, rather than after it ([NASASpaceFlight](https://www.nasaspaceflight.com/2025/10/beck-neutron-update/); [SpaceNews: Rocket Lab fires Archimedes for first time](https://spacenews.com/rocket-lab-fires-archimedes-engine-for-the-first-time/)). Archimedes itself reuses the additive playbook: **3D-printed turbopump housings, thrust chamber, valve housings, and structural components** ([VoxelMatters: AM scales Electron to Neutron](https://www.voxelmatters.com/rocket-lab-targets-1000th-rutherford-engine-launch-as-am-scales-from-electron-to-neutron/)).

**A telling detail on manufacturing discipline [FACT/INFERENCE].** A Stage-1 propellant tank failed a hydrostatic test in January 2026; Rocket Lab's response was to **replace the hand-laid tank with an automated-fiber-placement-built unit to eliminate the hand-lay defect class** (`rocket_lab/overview.md`). [INFERENCE] This is the production-engineer's instinct, when a manual process produces a defect, move it onto the automated line, which is precisely the mindset a production-line node program requires.

---

## 2. Spacecraft / Satellite Volume Manufacturing

Rocket Lab is not only a rocket maker; its larger revenue segment is Space Systems, where it manufactures spacecraft and subsystems (`rocket_lab/overview.md`, Q1 2026 segment split: Space Systems $136.7M vs Launch $63.7M). The manufacturing-process point here is that Rocket Lab builds *satellites* on a line too, and has explicitly productized high-volume satellite manufacture.

### 2.1 Flatellite: a satellite "designed for mass manufacture" (ANNOUNCED, in production)

On **27 February 2025** Rocket Lab unveiled **Flatellite**, a flat, stackable spacecraft **"designed for mass manufacture and tailored for large constellations,"** explicitly built to be produced in high volume ([Rocket Lab: Flatellite announcement](https://rocketlabcorp.com/updates/rocket-lab-announces-flatellite-a-new-satellite-designed-for-mass-manufacture-and-tailored-for-large-constellations/); [Business Wire](https://www.businesswire.com/news/home/20250227111767/en/Rocket-Lab-Announces-Flatellite-A-new-Satellite-Designed-for-Mass-Manufacture-and-Tailored-for-Large-Constellations); [SpaceDaily: high-volume satellite](https://www.spacedaily.com/reports/Rocket_Lab_Unveils_Flatellite_A_High_Volume_Satellite_for_Large_Constellations_999.html)).

The design philosophy is the manufacturing point: Flatellite **integrates Rocket Lab's existing in-house heritage subsystems** (propulsion, flight software, avionics, reaction wheels, star trackers, separation system, solar arrays, radios, composite structures, fuel tanks), which is what "enables rapid, high-volume production … without compromising performance or reliability" ([Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-announces-flatellite-a-new-satellite-designed-for-mass-manufacture-and-tailored-for-large-constellations/); [Business Wire](https://www.businesswire.com/news/home/20250227111767/en/Rocket-Lab-Announces-Flatellite-A-new-Satellite-Designed-for-Mass-Manufacture-and-Tailored-for-Large-Constellations)). (The specific subsystem list and its completeness for a *compute* node are analyzed in `rocket_lab/space_hardware_capabilities.md`; here the point is only that a product designed for the line is assembled from standard in-house parts.)

Peter Beck's framing ties manufacturing directly to the launch-plus-build advantage [FACT]:
- *"The industry is hungry for versatile satellites that are affordable and built fast in high volumes. This is why we created Flatellite."*
- *"By having our own rides to space with Neutron and Electron and being able to build our own spacecraft in high volumes, we're at a distinct advantage when it comes to deploying constellations with speed and cost-efficiency."*

([Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-announces-flatellite-a-new-satellite-designed-for-mass-manufacture-and-tailored-for-large-constellations/); [Business Wire](https://www.businesswire.com/news/home/20250227111767/en/Rocket-Lab-Announces-Flatellite-A-new-Satellite-Designed-for-Mass-Manufacture-and-Tailored-for-Large-Constellations).)

**Not just a render [FACT/INFERENCE].** Flatellite is the platform Rocket Lab is producing for its **$816M Space Development Agency prime contract** (18 missile-tracking spacecraft, Dec 2025), with reported backlog exceeding 40 spacecraft ([SpaceNews: SDA confirms Rocket Lab to produce 18 satellites](https://spacenews.com/space-development-agency-confirms-rocket-lab-will-produce-18-satellites-for-u-s-military-network/); `rocket_lab/overview.md`). [INFERENCE] A funded multi-spacecraft prime contract validates the volume-manufacturing intent as a real production program, not a concept.

### 2.2 The Spacecraft Production Complex and a high-volume satellite line (DEMONSTRATED facility)

Rocket Lab's Long Beach **Spacecraft Production Complex** (co-located with HQ) houses spacecraft production and a comprehensive in-house test stack [FACT]: an **~11,000-12,000 sq ft cleanroom** plus on the order of **40,000 sq ft of production and test facilities**, including thermal-vacuum, vibration, and EMI/EMC test ([Rocket Lab: expands footprint with new Long Beach HQ and production complex](https://rocketlabcorp.com/updates/rocket-lab-expands-footprint-with-new-long-beach-headquarters-and-production-complex/); [Rocket Lab: Spacecraft](https://rocketlabcorp.com/space-systems/spacecraft/)). Rocket Lab states it is standing up a **dedicated high-volume spacecraft manufacturing line** to meet demand, and that it manufactures **components, subsystems, and software in-house to accelerate production timelines** ([Rocket Lab: Spacecraft](https://rocketlabcorp.com/space-systems/spacecraft/)).

The in-house, vertically integrated production of high-rate components is independently corroborated by the subsystem businesses (e.g., Sinclair-heritage reaction wheels on 200+ satellites, with a dedicated high-volume reaction-wheel production facility, see `rocket_lab/space_hardware_capabilities.md`). The manufacturing-process takeaway: Rocket Lab runs **build-integrate-test under one roof** for spacecraft, which is the same workflow a node line needs.

### 2.3 Leadership identity: a manufacturer first

Rocket Lab's public self-description and Beck's statements consistently frame the company as a manufacturer applying mass-production methods to space hardware [FACT]:

- Beck on the in-house, build-it-ourselves culture: *"Kiwis aren't afraid to give something a go, even if it means inventing the machine we need or learning how to do it ourselves,"* and the company's approach is *"always very hardware rich,"* enabling fast iteration ([Inc.: Peter Beck explains why his space company thinks different](https://www.inc.com/kit-eaton/rocket-lab-ceo-peter-beck-explains-why-his-space-company-thinks-different/91024435)).
- On vertical integration as a manufacturing necessity: *"Vertical integration strategy for us is not a religion … And you can argue it's not even a strategy. It's just a necessity"* ([HBR: The founder of Rocket Lab on competing with billionaires](https://hbr.org/2026/03/the-founder-of-rocket-lab-on-competing-with-billionaires-to-lead-in-space)).
- The stated north star is *"building an end-to-end space company"* spanning launch, spacecraft manufacture, components, and operations ([Bloomberg: Rocket Lab's CEO on vertical integration and end-to-end space solutions](https://www.bloomberg.com/news/audio/2025-09-23/tech-disruptors-rocket-lab-s-ceo-on-end-to-end-space-solutions); `rocket_lab/overview.md` §6).

[INFERENCE] This is not incidental marketing: the same person and culture that chose to print engines, automate composite layup, and "build a production line" for a new engine is the decision-making layer that would set up a node line. The disposition toward manufacturing-at-scale is itself part of the evidence.

---

## 3. The Transfer-to-Node-Production Argument

**Claim being grounded:** the production-line thesis (assemble a node from in-house parts near the pad, build, test, launch, repeat) is low-risk on the *manufacturing-process* dimension because the required processes are the ones Rocket Lab already runs.

### 3.1 A node is, structurally, a spacecraft Rocket Lab already knows how to build

A data-center node is physically a large spacecraft: a composite primary structure, a deployable power system, a thermal-rejection system, attitude control, comms, and an integrated payload (the GPU rack). [INFERENCE] Strip out the payload and the radiator, and what remains is close to a high-power Flatellite-class bus, exactly the object Rocket Lab has productized for mass manufacture. The node program does not require inventing a manufacturing capability; it requires re-pointing existing ones.

### 3.2 Process-by-process mapping (demonstrated competency → node need)

| Node-line process need | Rocket Lab demonstrated competency | Status | Where shown |
|---|---|---|---|
| Serial production of complex metal parts (brackets, manifolds, propulsion, structural fittings) | Additive manufacture of rocket engines at ~200/yr; 1,000 Rutherfords; ~24 h part prints | **Demonstrated at volume** | §1.1 |
| High-rate carbon-composite primary structure with quality control | Rosie cell (12 h vs 400 h) on Electron; AFP machine (100 m/min, inline defect inspection) for Neutron | **Demonstrated (Electron); installed (Neutron)** | §1.2, §1.3 |
| Repeatable build → integrate → test cadence | Electron every ~18-20 days; Spacecraft Production Complex with in-house thermal-vac/vibe/EMI test | **Demonstrated** | §1.2, §2.2 |
| Design-for-manufacture from program start | "We built a production line" (Archimedes); Flatellite "designed for mass manufacture" | **Demonstrated as method** | §1.3, §2.1 |
| Vertically integrated parts supply (don't wait on vendors) | In-house engines, composites, avionics, power, comms, mechanisms | **Demonstrated** | §2.1, and `space_hardware_capabilities.md` |
| Factories on the launch path | Middle River (MD) structures + Wallops (VA) Neutron pad; Long Beach production | **Demonstrated/installed** | §1.3, `overview.md` |

[INFERENCE] Every row is a process the node thesis depends on, and every row is already populated by a running or installed Rocket Lab capability. The mapping is qualitative, not a cost model (cost-down economics live in the economics/node-design docs), but it establishes the key point: **the manufacturing motions are not novel for this operator.**

### 3.3 Factories adjacent to the launch path

The production-line thesis specifically wants "assemble near the pad, build, test, launch, repeat." Rocket Lab's footprint already approximates this for Neutron: the **Middle River, Maryland** Space Structures Complex (the AFP machine) is on the US East Coast near the **Wallops Island, Virginia** Neutron launch site (LC-3 / MARS) (`rocket_lab/overview.md`; `rocket_lab/neutron/sso_us_launch_site_options.md`). [INFERENCE] A node line could plausibly extend the same build-near-the-pad logistics rather than create a new model. (Note: the project's launch-site assumptions, including a possible West Coast relocation for SSO, are a separate scenario, see `RLDC-LAUNCH-SITE` in `SOURCE_INDEX.md`. This doc only observes that co-located build-and-launch infrastructure is already Rocket Lab's pattern.)

### 3.4 What this argument does NOT claim (honest boundaries)

- **It does not claim Rocket Lab has built a node, or announced one.** As of June 2026 Rocket Lab positions itself as a *supplier of power and components* to the orbital-data-center market, not an operator (`rocket_lab/overview.md` §6, `space_hardware_capabilities.md` §1.4). The transfer is a capability inference, not a stated company plan.
- **It does not close the hard subsystem gaps.** The thermal radiator subsystem in particular is an open gap (`space_hardware_capabilities.md` §2, §6) and data-center-scale power management is partial. Manufacturing competency reduces *execution* risk on building a node repeatably; it does not by itself solve heat rejection.
- **It does not prove cost.** Whether production-line manufacture makes a node *cheap enough* is the economics question handled elsewhere (Wright's-law / production-vs-bespoke docs and the cost model). This doc only grounds the *can-they-manufacture-repeatably* premise.
- **Neutron-class manufacturing is not yet flight-proven.** The strongest demonstrated evidence is Electron-class (engines, Rosie) and Space-Systems-class (Flatellite production, the Spacecraft Production Complex). Neutron's AFP machine and Archimedes line are installed and standing up, corroborating intent and tooling, but Neutron has not flown.

[INFERENCE] With those boundaries stated, the conclusion is narrow and defensible: **of all the risks an orbital-data-center node program faces, "can a complex aerospace product be built repeatably, in-house, at volume, on a production line" is the one Rocket Lab has most clearly already retired.**

---

## Companion Documents (related existing wiki docs: not modified)

- [rocket_lab/space_hardware_capabilities.md](space_hardware_capabilities.md), WHICH subsystems Rocket Lab owns for a compute node (the component list; deliberately not re-enumerated here), and the radiator/thermal and power-management gaps.
- [rocket_lab/overview.md](overview.md), company profile, segment split, vertical-integration strategy, Neutron status, and the Feb 2026 silicon-solar-array-for-data-centers announcement.
- [rocket_lab/electron/electron_specs.md](electron/electron_specs.md), Electron specs, carbon-composite airframe, Rutherford engines, launch cadence and reliability record.
- [rocket_lab/neutron/neutron_specs.md](neutron/neutron_specs.md) and [rocket_lab/neutron/payload_and_block_upgrade.md](neutron/payload_and_block_upgrade.md), Neutron vehicle specs and payload assumptions.
- [rocket_lab/neutron/sso_us_launch_site_options.md](neutron/sso_us_launch_site_options.md), launch-site (Wallops vs West Coast) scenario relevant to "factories near the pad."
- [node_design/node_mass_model.md](../node_design/node_mass_model.md) and [node_design/self_built_rack.md](../node_design/self_built_rack.md), what a node is physically made of (the object the line would build).
- Production-line-versus-bespoke economics and Wright's-law learning curves are covered in the economics / node-design docs (e.g. cost-trajectory and rack docs); this doc intentionally does not re-derive them.

---

## Open Questions / Uncertainties

- **Rutherford production rate precision.** "~200 engines/year" and "~1 engine/month in 2017" come from trade-press coverage of the 1,000th-engine milestone, not a Rocket Lab datasheet. Treat the rate as a sourced order-of-magnitude, not an audited figure. Confirm against an investor presentation if a precise rate becomes load-bearing.
- **EBM vs newer AM processes.** Rutherford has historically been electron-beam-melted; with EOS / Nikon SLM / Renishaw systems and a new ultra-large platform, the current process mix (EBM vs laser powder-bed fusion) per component is not fully specified publicly.
- **Neutron manufacturing is unproven in flight.** The AFP machine specs and Archimedes "production line" are installed/announced; no Neutron has flown (Q4 2026 target). The 150,000-hour labor-saving figure is a Rocket Lab projection "at full-scale production," not a realized result.
- **Electron build cadence figure.** "A rocket every ~18-20 days" is from secondary reporting; sources vary (18 vs 20 days) and the figure predates current tooling. The hard, defensible proxy is the *flight* record (21 launches in 2025).
- **Flatellite production rate.** Rocket Lab says "high volumes" and "mass manufacture" but has not published a satellites-per-month rate or a per-unit build time. The $816M SDA contract (18 spacecraft) and 40+ backlog validate it as a real program, not a stated throughput.
- **Spacecraft Production Complex floor specs.** Cleanroom area is cited at both ~11,000 and ~12,000 sq ft across sources; the "high-volume spacecraft line" is described qualitatively without a stated unit throughput.
- **Node-specific manufacturing.** No public evidence Rocket Lab has prototyped or tooled for a *data-center node* specifically. The entire §3 transfer argument is [INFERENCE] from adjacent demonstrated capability, not a Rocket Lab roadmap. The thermal-radiator manufacturing capability in particular is unestablished (see `space_hardware_capabilities.md`).

---

## Sources

**Rutherford / additive manufacturing**
- [Rocket Lab: Celebrates 100th Rutherford Engine Build](https://rocketlabcorp.com/updates/rocket-lab-celebrates-100th-rutherford-engine-build/)
- [The Fabricator: Rocket Lab completes its 100th 3D-printed engine](https://www.thefabricator.com/additivereport/news/additive/rocket-lab-celebrates-completion-of-its-100th-3d-printed-engine)
- [Rocket Lab on X: 1,000th Rutherford off the production line (16 May 2026)](https://x.com/RocketLab/status/2055097584541442066)
- [3D Printing Industry: Rocket Lab's 3D-printed engine hits 1,000 units](https://3dprintingindustry.com/news/rocket-labs-3d-printed-engine-hits-1000-units-251599/)
- [VoxelMatters: Rocket Lab rolls the 1,000th Rutherford engine off its production line](https://www.voxelmatters.com/rocket-lab-rolls-the-1000th-rutherford-engine-off-its-production-line/)
- [VoxelMatters: Rocket Lab targets 1,000th Rutherford launch as AM scales from Electron to Neutron](https://www.voxelmatters.com/rocket-lab-targets-1000th-rutherford-engine-launch-as-am-scales-from-electron-to-neutron/)
- [3D ADEPT: Rocket Lab's 1,000th Rutherford: additive manufacturing as a competitive moat](https://3dadept.com/rocket-labs-1000th-rutherford-engine-when-additive-manufacturing-becomes-a-competitive-moat/)
- [metal-am.com: Rocket Lab produces its 1,000th Rutherford engine](https://www.metal-am.com/rocket-lab-produces-its-1000th-rutherford-engine/)

**Electron / Rosie automated composites**
- [SpaceNews: Rocket Lab introduces robotic manufacturing system to increase Electron production](https://spacenews.com/rocket-lab-introduces-robotic-manufacturing-system-to-increase-electron-production/)
- [Space.com: Rocket Lab's 'Rosie' can build a booster in just 12 hours](https://www.space.com/rocket-lab-rosie-robot-build-rocket-12-hours.html)
- [TechCrunch: Rocket Lab's new 'Rosie the Robot' speeds up launch-vehicle production](https://techcrunch.com/2019/11/13/rocket-labs-new-rosie-the-robot-speeds-up-launch-vehicle-production-by-a-lot/)
- [Digital Trends: Rocket Lab shows off Rosie, its rocket-building robot](https://www.digitaltrends.com/space/rocket-lab-shows-off-rosie-its-rocket-building-robot/)
- [Interesting Engineering: Rocket Lab's 'Rosie' helps build a launch vehicle every 20 days](https://interestingengineering.com/rocket-labs-rosie-helps-build-a-launch-vehicle-every-20-days)
- [SpaceNews: Rocket Lab wraps up record launch year](https://spacenews.com/rocket-lab-wraps-up-record-launch-year/)

**Neutron / AFP and Archimedes**
- [Rocket Lab: Begins installation of large carbon composite rocket-building machine](https://rocketlabcorp.com/updates/rocket-lab-begins-installation-of-large-carbon-composite-rocket-building-machine/)
- [CompositesWorld: Rocket Lab begins installation of large AFP machine for rocket production](https://www.compositesworld.com/news/rocket-lab-begins-installation-of-large-afp-machine-for-rocket-production)
- [SpaceDaily: Rocket Lab installs advanced carbon composite manufacturing system for Neutron production](https://www.spacedaily.com/reports/Rocket_Lab_Installs_Advanced_Carbon_Composite_Manufacturing_System_for_Neutron_Rocket_Production_999.html)
- [Interesting Engineering: A giant 90-ton 3D printer is building Rocket Lab's Neutron rocket](https://interestingengineering.com/space/3d-printing-beast-builds-worlds-largest-neutron-rocket)
- [NASASpaceFlight: Peter Beck discusses Neutron development as maiden flight nears](https://www.nasaspaceflight.com/2025/10/beck-neutron-update/)
- [Everyday Astronaut: Neutron Update | Interview with Peter Beck](https://everydayastronaut.com/neutron-update-interview-with-peter-beck/)
- [SpaceNews: Rocket Lab fires Archimedes engine for the first time](https://spacenews.com/rocket-lab-fires-archimedes-engine-for-the-first-time/)

**Flatellite / Space Systems manufacturing**
- [Rocket Lab: Announces Flatellite, designed for mass manufacture](https://rocketlabcorp.com/updates/rocket-lab-announces-flatellite-a-new-satellite-designed-for-mass-manufacture-and-tailored-for-large-constellations/)
- [Business Wire: Rocket Lab announces Flatellite](https://www.businesswire.com/news/home/20250227111767/en/Rocket-Lab-Announces-Flatellite-A-new-Satellite-Designed-for-Mass-Manufacture-and-Tailored-for-Large-Constellations)
- [SpaceDaily: Rocket Lab unveils Flatellite, a high-volume satellite](https://www.spacedaily.com/reports/Rocket_Lab_Unveils_Flatellite_A_High_Volume_Satellite_for_Large_Constellations_999.html)
- [SpaceNews: SDA confirms Rocket Lab will produce 18 satellites for U.S. military network](https://spacenews.com/space-development-agency-confirms-rocket-lab-will-produce-18-satellites-for-u-s-military-network/)
- [Rocket Lab: Expands footprint with new Long Beach HQ and production complex](https://rocketlabcorp.com/updates/rocket-lab-expands-footprint-with-new-long-beach-headquarters-and-production-complex/)
- [Rocket Lab: Spacecraft (Space Systems)](https://rocketlabcorp.com/space-systems/spacecraft/)

**Leadership identity / manufacturing philosophy**
- [Inc.: Rocket Lab CEO Peter Beck explains why his space company thinks different](https://www.inc.com/kit-eaton/rocket-lab-ceo-peter-beck-explains-why-his-space-company-thinks-different/91024435)
- [HBR: The founder of Rocket Lab on competing with billionaires to lead in space](https://hbr.org/2026/03/the-founder-of-rocket-lab-on-competing-with-billionaires-to-lead-in-space)
- [Bloomberg: Tech Disruptors: Rocket Lab's CEO on vertical integration and end-to-end space solutions](https://www.bloomberg.com/news/audio/2025-09-23/tech-disruptors-rocket-lab-s-ceo-on-end-to-end-space-solutions)
