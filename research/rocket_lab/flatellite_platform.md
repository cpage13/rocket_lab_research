# Rocket Lab Flatellite: the BROADBAND/D2C Satellite Platform and How Many Fit a Neutron

**Research date:** 2026-06-22
**Purpose:** Ground the BROADBAND (and direct-to-cell) case for a Neutron-launched space communications business in Rocket Lab's OWN flat satellite platform, "Flatellite." Establish what Flatellite is, its (mostly unpublished) specs, whether it is designed for comms/broadband, how many ride a Neutron, and its status. This is the Rocket-Lab-native counterpart to the competitor-benchmark fit doc (Starlink V3 / BlueBird Block 2 on Neutron).
**Vehicle modeled:** Neutron ONLY. Rocket Lab has no Starship-class vehicle; none is assumed.
**Status:** Understanding-building input. No verdict. Most hard Flatellite specs are NOT published by Rocket Lab; every estimate is flagged as such, and the unknowns are named.

> **Grounds in and does not duplicate (references their claim IDs, does not rewrite them):**
> - [`research/rocket_lab/neutron/neutron_comms_payload_fit.md`](neutron/neutron_comms_payload_fit.md) (COMM-225..246): owns the per-Neutron fit arithmetic for the *competitor* benchmarks (Starlink V3 ~5/launch mass-bound; BlueBird Block 2 ~1/launch antenna-size-bound) and the two fit gates (mass gate, volume/shape gate). This doc adds the Rocket-Lab-native satellite (Flatellite) and its per-Neutron count, and reuses that doc's gate framework.
> - [`research/rocket_lab/neutron/neutron_specs.md`](neutron/neutron_specs.md) and [`payload_and_block_upgrade.md`](neutron/payload_and_block_upgrade.md) (SOURCE_INDEX claim IDs **NTR-001..NTR-011**): the authority on Neutron's own numbers (13,000 kg to LEO DRL = NTR-class headline; 5.5 m fairing; ~14 m fairing height with Stage 2 inside; ~9,500 kg to SSO = estimate; usable fairing volume ~150-230 m^3 = estimate). This doc takes those as GIVEN and cites them; it does NOT re-derive them and does NOT mint new NTR- IDs.
> - [`research/competitors/large_array_folding_and_stow.md`](../competitors/large_array_folding_and_stow.md) (COMM-197..208) and [`starlink_v3_v4_spectrum_incorporation.md`](../competitors/starlink_v3_v4_spectrum_incorporation.md) (COMM-178..190): the flat-pack / fold-vs-stow context. Flatellite is a flat, NON-deployed-aperture design (the body IS the aperture), so it inherits the V3-side "flat panel stacks dense, mass-bound not size-bound" logic, NOT the BlueBird-side many-fold accordion logic.
> - Existing scattered Flatellite mentions live in [`rocket_lab/overview.md`](overview.md), [`space_hardware_capabilities.md`](space_hardware_capabilities.md), [`manufacturing_capability_2026.md`](manufacturing_capability_2026.md), and [`vertical_integration_stack_2026.md`](vertical_integration_stack_2026.md). This doc CONSOLIDATES and EXTENDS them (adds the D2C/5G-NTN framing, the volume-bound compute, and a bus-naming correction); it does not restate their vertical-integration argument.

---

## 0. Answer first (the four things the BROADBAND case needs)

1. **What it is:** Flatellite is Rocket Lab's OWN flat, stackable, mass-manufactured, high-power satellite platform, unveiled **27 February 2025**, "designed for mass manufacture and tailored for large constellations." Rocket Lab's official one-line: a **"scalable, long-life, high-power, stackable satellite that enables secure, low-latency, high-speed connectivity and remote sensing capability for national security, defense, and commercial markets."** It is the deliberate "build" half of a launch-plus-build (Neutron + Flatellite) constellation system and the vehicle for Rocket Lab's stated ambition to operate **its own constellation**. [FACT, multi-source] (COMM-249, COMM-250)

2. **Is it broadband / comms?** YES, comms-first, and specifically pointed at the **broadband / direct-to-cell (5G NTN)** market. Rocket Lab VP Richard French framed Flatellite as **"an elegant solution for large-aperture systems, without the need for deployable [antennas]"** and named **"5G NTN (non-terrestrial network)"** as "a great example of a commercial application," with **"minimum viable constellations in the 150 to 200-satellite range."** The flat body itself is the large RF aperture (no unfurled antenna), which is the opposite stow problem to AST BlueBird's many-fold accordion. [FACT, multi-source] (COMM-251, COMM-262)

3. **The specs the broadband math needs are mostly UNPUBLISHED.** Rocket Lab has disclosed NO mass, NO power figure (only the word "high-power"), and NO dimensions for Flatellite. The widely repeated **~800 kg mass** and **~16 per Neutron** are a **single third-party analyst's estimates read off a Rocket Lab render**, explicitly hedged by that author ("just throwing ideas at the wall," could be "~200 kg less," the analysis "may be more fiction than fact"). Treat both as ESTIMATE, not FACT. [Mass/dims: UNKNOWN officially; ~800 kg and ~16: single-source ESTIMATE] (COMM-253, COMM-254, COMM-256, COMM-257)

4. **Per-Neutron count (the candidate BROADBAND satellites-per-launch):** **~16 Flatellites per Neutron** is the working number, and it is **mass-and-render-convergent at LEO**: 13,000 kg LEO (NTR headline) / ~800 kg = ~16, which coincides with the ~16 visible in Rocket Lab's own fairing render. So at the ~800 kg estimate the mass gate and the render agree at ~16 to LEO; to SSO (~9,500 kg estimate) the mass gate alone caps it at **~12**. The volume-bound count cannot be computed independently (Flatellite stowed dimensions unpublished), but the render's ~16 IS Rocket Lab's own implicit volume-and-mass-packed answer. **Binding gate: mass (at SSO) / mass-and-render-together (at LEO); ~16 to LEO, ~12 to SSO, both estimate-bound.** [DERIVED on a single-source mass estimate] (COMM-258, COMM-259, COMM-260)

The rest of this doc sources and derives each, and flags one bus-naming correction the catalogs should pick up.

---

## 1. What Flatellite is (the official record)

### 1.1 Announcement and official description

On **27 February 2025**, at its Spacecraft Production Complex in Long Beach, California, Rocket Lab unveiled **Flatellite** (the name is a portmanteau of "flat" + "satellite"; press coverage also calls it a "pizza box"-shaped satellite). The press release title: *"Rocket Lab Announces Flatellite: A New Satellite Designed for Mass Manufacture and Tailored for Large Constellations."* [FACT, multi-source: Rocket Lab PR via Business Wire; SpaceQ; Space Voyaging; SpaceDaily] (COMM-249)

Rocket Lab's stated description, repeated near-verbatim across outlets:

> A **"scalable, long-life, high-power, stackable satellite that enables secure, low-latency, high-speed connectivity and remote sensing capability for national security, defense, and commercial markets."**

Peter Beck's framing positions it as the capstone of the company's strategy:

> *"The industry is hungry for versatile satellites that are affordable and built fast in high volumes. This is why we created Flatellite."* and Flatellite represents *"the final step in Rocket Lab's ultimate vision of being a truly end-to-end space company, operating its own constellation and delivering services from space."*

[FACT, multi-source: Business Wire / Rocket Lab PR; SpaceQ; Advanced Television; SpaceDaily] (COMM-249, COMM-250)

### 1.2 Design intent (flat, stackable, mass-manufactured, Neutron-matched)

Four design intentions are stated by Rocket Lab and consistent across sources:

- **Flat / low-profile / stackable** so many satellites stack densely in one fairing ("low-profile, stackable structure to maximize the number of satellites that can be deployed per launch"). [FACT]
- **Mass-manufactured / high-volume** ("designed for mass manufacture," "built fast in high volumes"), produced on a dedicated high-volume line at the Long Beach Spacecraft Production Complex. [FACT]
- **Tight Neutron integration** ("seamless integration with Rocket Lab's own Neutron rocket"). [FACT]
- **Heritage-subsystem build** integrating Rocket Lab's in-house propulsion, flight software, avionics, reaction wheels, star trackers, separation system, solar arrays, radios, composite structures, and fuel tanks. [FACT] (this is the subsystem list already cataloged in `space_hardware_capabilities.md`; cross-ref, not re-argued)

(COMM-250) Sources: Rocket Lab PR (Business Wire); SpaceQ; Space Voyaging; SpaceDaily; Orbital Today.

### 1.3 Rocket Lab's OWN constellation ambition

Flatellite is explicitly tied to Rocket Lab operating its own constellation, not just selling buses. Beck's "operating our own constellation and delivering services from space" is the recurring phrase; multiple analyses read Flatellite as the platform that could let Rocket Lab field a Starlink/Kuiper-style commercial constellation. This is the strategic reason a Rocket-Lab comms thesis cares about Flatellite specifically: it is the company's declared path from launch-and-build vendor to constellation operator. [FACT for the stated ambition; the constellation itself is a stated intent, not a funded program] (COMM-250, COMM-261)

---

## 2. Is Flatellite a broadband / comms platform? (YES, and specifically D2C / 5G-NTN)

This is the load-bearing question for the broadband case, and the evidence is stronger than the generic "connectivity" press line.

### 2.1 The official applications: comms-first, plus remote sensing

Every official description leads with **"secure, low-latency, high-speed connectivity"** and pairs it with **"remote sensing."** Rocket Lab's own spacecraft page later describes Flatellite as delivering **"secure, low-latency, and high-speed communications connectivity in LEO,"** a "constellation-class" satellite for national-security and commercial customers. So it is **not** a generic do-anything bus framed neutrally: comms/connectivity is the first-named application, with remote sensing second. [FACT, multi-source: Rocket Lab spacecraft page; Rocket Lab PR; Space Voyaging] (COMM-251)

### 2.2 The direct-to-cell / 5G-NTN framing (the specific broadband signal)

Two months after the unveiling, Rocket Lab VP **Richard French** made the comms intent specific (reported 23 April 2025, SatNews and Advanced Television, both citing the same remarks):

- Flatellite is **"an elegant solution for large-aperture systems, without the need for deployable [antennas]."**
- **"5G NTN (non-terrestrial network) is a great example of a commercial application."**
- **"Minimum viable constellations are in the 150 to 200-satellite range."**

This is the direct-to-cell / direct-to-device case (the "lead market" the comms thesis tracks): closing a link to handsets needs a **large aperture**, and Flatellite's pitch is that the **flat satellite body itself is that aperture**, so it does NOT need a folding antenna. The 150-200-satellite figure is a D2C/5G-NTN constellation-sizing statement, in the same band as AST's ~90-for-global and FCC-authorized-248 numbers carried in `neutron_comms_payload_fit.md`. [FACT, multi-source for the French quotes] (COMM-262)

### 2.3 Why "no deployable, the body is the aperture" matters (the fold asymmetry, applied)

`large_array_folding_and_stow.md` (COMM-197..208) established the core stow asymmetry: a Starlink V3 broadband aperture barely folds (it is the flat body) and is mass-bound; a BlueBird Block 2 D2C array is a many-fold accordion (~220-265 tiles, "phone booth to studio apartment") and is size-bound. Flatellite's stated design **chooses the V3 side of that asymmetry for a D2C mission**: a large flat aperture with **no deployable**, sized to the satellite footprint, stacked flat. That is the engineering reason Flatellite is plausibly mass-bound (like V3) rather than antenna-stow-bound (like BlueBird), and it is the lever the prior fit doc named as "the path to Neutron relevance" for D2C (a tighter-stowing / no-deployable aperture). The trade is that a flat, non-deployed aperture is limited to the satellite's own flat area, so per-satellite aperture (and thus per-satellite D2C capacity) is capped by how big a flat satellite you can stack, which is the open performance question in Section 6. [DERIVED, anchored to COMM-197..208 and Section 2.2] (COMM-263)

---

## 3. Specs: what is published, what is estimated, what is unknown

**Headline: Rocket Lab has published essentially NO hard Flatellite numbers.** No mass, no power figure (only the adjective "high-power"), no dimensions, no per-satellite capacity, no aperture area. The numbers in circulation are third-party render-reads. This section tags every value.

| Parameter | Value | Tag | Source / basis |
|---|---|---|---|
| Dry mass | **NOT published** | UNKNOWN (official) | Rocket Lab has released no mass figure |
| Wet mass | **NOT published** | UNKNOWN (official) | as above |
| Mass (third-party estimate) | **"slightly over ~800 kg"** (author also floats **~600 kg**, "200 kg less") | ESTIMATE, single-source | illdefined.space, read off the count of Flatellites in Rocket Lab's Neutron-fairing render; author hedges heavily |
| Power | **"high-power"** (no number) | UNKNOWN (official) | only the qualitative descriptor is published |
| Stowed thickness / footprint (L x W) | **NOT published** | UNKNOWN (official) | no dimensions released; "flat / low-profile / pizza-box" is qualitative only |
| Deployed span | **NOT published** | UNKNOWN (official) | design intent is "no deployable [antenna]"; solar-array span not given |
| Stowed volume per satellite | **NOT published** | UNKNOWN (official) | needed for an independent volume-bound count; not available |
| Payload accommodation | **NOT published** as a number; "high-value applications," comms + remote sensing | UNKNOWN (official) | qualitative only |
| Per-Neutron stack count | **~16** (render) | ESTIMATE, single-source / render | Rocket Lab render shows a stack; illdefined.space counts ~16 |
| Design life | **"long-life"** (no number) | UNKNOWN (official) | qualitative descriptor |

(COMM-252, COMM-253, COMM-256, COMM-257)

**The mass estimate, handled honestly.** The ~800 kg figure is NOT a Rocket Lab number and NOT multi-sourced; it is one analyst's inference from a render, and that analyst explicitly says it could be ~200 kg lighter and that the whole exercise "may be more fiction than fact." It is repeated by SpaceDaily/Orbital Today/Space Voyaging, but they are repeating the SAME single render-read, not independently measuring, so this is **single-source despite the apparent spread**. Use **~600-800 kg as an ESTIMATE band**, never as a fact, and flag that the true mass depends on the payload Flatellite carries. [ESTIMATE, single-source] (COMM-256)

**Contrast with the competitor benchmarks (for the model's sake).** Where Starlink V3 (~1,900 kg) and BlueBird Block 2 (~5,830-6,100 kg) masses are FACT-grade and multi-sourced (COMM-225-class in the fit doc), Flatellite's mass is an unsourced render-read. So any Flatellite-per-Neutron number is **softer** than the V3 or Block 2 per-Neutron numbers, and must be carried as an estimate-bound range. (COMM-257)

---

## 4. Launch fit: designed for Neutron; the fairing envelope (cross-referenced, not re-minted)

### 4.1 Launch vehicle: Neutron-matched (and Electron-compatible smaller variants implied)

Flatellite is explicitly **designed for Neutron**: "seamless integration with Rocket Lab's own Neutron rocket" is in every release, and Rocket Lab frames Neutron as the vehicle "sized to deploy stacked Flatellite constellations." Rocket Lab also notes it owns both Neutron and Electron, but the stacked-constellation deployment case is Neutron. Rocket Lab has NOT stated Falcon 9 compatibility (it is a competitor vehicle) and there is no public per-fairing count for Flatellite on any non-Neutron vehicle. [FACT for Neutron design intent; Electron/Falcon-9 fit: not stated] (COMM-254)

### 4.2 The Neutron envelope (carried from the NTR ledger, NOT re-derived)

From `neutron_specs.md` / `payload_and_block_upgrade.md` (SOURCE_INDEX **NTR-001..NTR-011**):

| Neutron parameter | Value | Tag | NTR ref |
|---|---|---|---|
| Payload to LEO (DRL, reusable) | **13,000 kg** | [FACT] | NTR headline (NTR-001-class) |
| Payload to LEO (expendable) | **15,000 kg** | [FACT] | NTR ledger |
| Payload to SSO (DRL, reusable) | **~9,500 kg** (range 8,500-10,500) | [ESTIMATE] | NTR ledger; NOT a Rocket Lab number |
| Fairing payload diameter | **up to 5.5 m** | [FACT] | PUG v1.0 (NTR ledger) |
| Fairing external height | **~14 m** ("Hungry Hippo"); usable length much less (Stage 2 inside) | [FACT] | NTR ledger |
| Usable fairing volume | **~150-230 m^3** | [ESTIMATE] | NTR ledger; not published by Rocket Lab |
| Launch price | **~$50-55 M** | [FACT, company target] | NTR ledger |

### 4.3 Has Rocket Lab stated how many Flatellites per Neutron?

**Not in words, but Rocket Lab's own announcement RENDER shows a stack of Flatellites inside the Neutron fairing**, and the only public count read off that render is **~16** (illdefined.space). Rocket Lab itself has not published a numeral; "stacks of up to ~16" traces entirely to the render-read, not to a Rocket Lab statement of "16." So the per-Neutron number is **a render-derived estimate, repeated widely, not an official Rocket Lab figure**. [ESTIMATE, single-source/render] (COMM-255)

---

## 5. Compute: Flatellites per Neutron (mass-bound vs volume-bound)

Clearly labeled, using the grounded Neutron envelope (Section 4.2) and the estimate-bound Flatellite mass (Section 3). **All counts here inherit a single-source mass estimate and the unpublished SSO mass, so they are estimate-bound, softer than the V3/Block 2 counts.**

### 5.1 Mass-bound count

mass-bound count = Neutron payload to orbit / Flatellite mass.

| Neutron mode / orbit | Neutron payload | At ~800 kg/sat | At ~600 kg/sat | Mass-bound count |
|---|---|---|---|---|
| DRL, LEO (FACT) | 13,000 kg | 13,000 / 800 = 16.3 | 13,000 / 600 = 21.7 | **~16 to ~22** |
| DRL, SSO (ESTIMATE) | ~9,500 kg | 9,500 / 800 = 11.9 | 9,500 / 600 = 15.8 | **~12 to ~16** |
| Expendable, LEO (FACT) | 15,000 kg | 15,000 / 800 = 18.8 | 15,000 / 600 = 25.0 | **~19 to ~25** |

[DERIVED on a single-source mass estimate] (COMM-258)

### 5.2 Volume-bound count (cannot be computed independently; the render IS the answer)

A clean volume-bound count needs the Flatellite **stowed volume per satellite**, which Rocket Lab has NOT published (Section 3). So the volume-bound count **cannot be derived from first principles**. What we have instead is Rocket Lab's own render, which packs **~16 Flatellites** into the Neutron fairing: that render is effectively Rocket Lab's OWN combined mass-and-volume-packed answer for the flat-stack. Reading it back: ~16 flat satellites filling the ~5.5 m x ~14 m (Stage-2-reduced) fairing implies each stows as a thin slab whose stack height and 5.5 m-diameter footprint together admit ~16, consistent with the ~150-230 m^3 usable-volume estimate. [DERIVED / render-read; not an independent calculation] (COMM-259)

### 5.3 Which binds, and the per-Neutron number

- **At LEO (13,000 kg), the mass gate and the render CONVERGE at ~16** (13,000 / 800 = 16.3 ~ the ~16 in the render). This convergence is the reason ~16 is the working broadband-satellites-per-Neutron number: Rocket Lab evidently sized the flat-stack so that a full fairing of Flatellites is also near the LEO mass limit. [DERIVED]
- **At SSO (~9,500 kg estimate), the MASS gate binds below the render**, capping the count at **~12** (9,500 / 800), because the lower SSO mass allowance runs out before the fairing is render-full. [DERIVED]
- **Net: ~16 Flatellites per Neutron to LEO, ~12 to SSO**, both estimate-bound (single-source mass, unpublished SSO mass). If the true mass is nearer ~600 kg, both numbers rise (~22 LEO / ~16 SSO); if heavier, they fall. This is the **candidate broadband satellites-per-Neutron** for the model, and it should be carried as **~12-16 (SSO-to-LEO), estimate-bound**, not a point. (COMM-260)

### 5.4 Sanity check against the competitor fit doc

`neutron_comms_payload_fit.md` found **~5 Starlink-V3-class** broadband satellites per Neutron (V3 is ~1,900 kg, mass-bound) and **~1 BlueBird-Block-2-class** D2C satellite per Neutron (antenna-size-bound). Flatellite at ~16/launch (LEO) carries **~3x more satellites per Neutron than a V3-class** simply because a Flatellite (~800 kg estimate) is lighter than a V3 (~1,900 kg), and far more than a Block-2 (~1/launch) because Flatellite has **no folding antenna** to eat fairing volume. So purpose-building the satellite to Neutron's own envelope (lighter, flat, no deployable) is exactly the lever the fit doc said would raise satellites-per-launch, and Flatellite is Rocket Lab's instantiation of that lever. The per-satellite **capacity** trade (a smaller flat aperture than BlueBird's 223 m^2) is the open question (Section 6), so "more satellites per launch" does not automatically mean "more capacity per launch." [DERIVED, cross-ref COMM-225..246] (COMM-264)

---

## 6. Status and timeline

- **Announced:** 27 February 2025 (unveil at Long Beach Spacecraft Production Complex). [FACT] (COMM-249)
- **In production as a real program (not a render):** Rocket Lab states Flatellite is built on its high-volume line; the company reports a **backlog exceeding 40 spacecraft** across commercial/civil/national-security customers. [FACT] (COMM-265)
- **Deployment intent:** Rocket Lab states it aims to **deploy Flatellite constellations starting mid-2026**, with multi-launch Neutron agreements signed (including a confidential multi-launch commercial-constellation deal). [FACT for the stated intent; gated by Neutron's first flight, targeted Q4 2026] (COMM-266)
- **First Flatellite on orbit:** **No public record of a Flatellite having flown** as of June 2026; no first-flight date or on-orbit demonstration has been announced. The deploy-from-mid-2026 intent depends on Neutron, which has not yet flown (maiden flight targeted Q4 2026). [UNKNOWN / not yet flown] (COMM-267)
- **Production rate:** Rocket Lab says "high volumes" / "mass manufacture" but has **NOT published a satellites-per-month or per-unit build-time figure**. [UNKNOWN] (COMM-268)

(Per the project's cadence rule: any Neutron launch cadence used downstream is a ramp that reaches ~90/year only in 2036, never a flat 90; Flatellite deployment is gated by that ramp and by Neutron first flight.)

---

## 7. A bus-naming correction the catalogs should pick up (flagged, not edited elsewhere)

Existing corpus docs (`overview.md`, `space_hardware_capabilities.md`, `manufacturing_capability_2026.md`) state that **Flatellite is being produced for Rocket Lab's $816M SDA prime contract (18 satellites)**. Later 2025-2026 sources indicate this is a **bus-name conflation** and should be corrected:

- The **$816M (reported ~$805M) SDA Tracking Layer Tranche 3** award (18 missile-tracking satellites, next-gen **Phoenix** IR sensor + StarLite) is built on Rocket Lab's **"Lightning"** satellite bus, per Spaceflight Now / SatNews / Rocket Lab's Tranche-3 materials, with launches beginning ~FY2029. It is a **missile-warning/tracking** mission (IR), NOT a comms/Flatellite mission. [FACT, multi-source]
- The **$515M SDA Transport Layer-Beta Tranche 2** award (18 data-transport/comms satellites, optical-mesh, Mynaric CONDOR terminals) was made in **January 2024**, a full year BEFORE Flatellite's Feb-2025 unveiling, so those satellites are **not** Flatellite either (they predate it; built on Rocket Lab's earlier Photon/Pioneer-class bus). [FACT for the Jan-2024 award date and the comms/optical-mesh scope; bus attribution: pre-Flatellite]
- Therefore **Flatellite's validating production program is NOT the $816M SDA tracking contract.** Flatellite is the comms/connectivity (and remote-sensing) commercial+national-security platform; the SDA tracking satellites are Lightning. The "40+ spacecraft backlog" is real, but pinning it to the $816M tracking award as "Flatellite production" is the error. [CORRECTION, multi-source] (COMM-269)

This is flagged here for the reconciliation pass; per instructions this doc does NOT edit `overview.md`, `space_hardware_capabilities.md`, `manufacturing_capability_2026.md`, LIBRARY.md, SOURCE_INDEX.md, or RESEARCH_TRACKER.md.

---

## 8. So what (for the broadband case)

1. **Rocket Lab has a native, comms-first, D2C-pointed flat satellite (Flatellite), and a native medium-lift launcher (Neutron), and designed them as a system.** The broadband case does not require Rocket Lab to fly a competitor's satellite; it has its own flat platform explicitly pitched at 5G-NTN/direct-to-cell with "no deployable antenna." This is the strongest Rocket-Lab-native anchor for the comms thesis. (COMM-249, COMM-262)

2. **The candidate broadband satellites-per-Neutron is ~16 to LEO / ~12 to SSO, but estimate-bound on a single-source mass.** Unlike the V3 (~5) and Block 2 (~1) counts, which sit on FACT-grade competitor masses, the Flatellite count sits on a render-read ~800 kg. It is the most favorable per-launch count in the corpus precisely because Flatellite is light and flat with no folding antenna, but it is also the softest because Rocket Lab has published no mass. Carry **~12-16, estimate-bound.** (COMM-258, COMM-260)

3. **The binding constraint flips with orbit, not with the antenna.** Because Flatellite has no large folding aperture, it is mass-bound (at SSO) or mass-and-volume-co-limited (at LEO, where the render and the mass limit meet at ~16), never antenna-stow-bound the way BlueBird Block 2 is. Neutron's modest 5.5 m fairing, which bit hardest on D2C in the competitor doc, does NOT bind Flatellite the same way, because Flatellite is designed to that fairing. (COMM-259, COMM-263)

4. **The open performance question is capacity per flat satellite, not fit.** "More satellites per launch" (16 vs 1) does not equal "more capacity per launch" until we know each Flatellite's aperture/power/throughput, all unpublished. A flat, non-deployed aperture is inherently smaller than BlueBird's 223 m^2 unfurled array, so per-satellite D2C link budget is the thing to pin before the broadband economics close. (COMM-263, COMM-270)

5. **Status: real production program, not yet flown, deployment gated by Neutron.** Backlog 40+, deploy-from-mid-2026 intent, but no Flatellite on orbit yet and Neutron's maiden flight is the gate. The broadband case is therefore credible on platform existence and intent, and unproven on flight, performance numbers, and unit economics. (COMM-265, COMM-266, COMM-267)

---

## Open questions / uncertainties (named gaps, not invented numbers)

1. **Flatellite mass (dry and wet).** Officially unpublished; the only figure is a single render-read (~600-800 kg). This is the #1 input that sets the per-Neutron count and is the softest number in the whole fit chain. [UNKNOWN officially]
2. **Flatellite power.** Only "high-power" is published; no watts. Decisive for whether a Flatellite can close a D2C link (and, separately, host any compute payload). [UNKNOWN]
3. **Flatellite stowed dimensions and per-satellite stowed volume.** Unpublished; this is what would let the volume-bound count be computed independently instead of read off the render. [UNKNOWN]
4. **Flatellite aperture area and per-satellite capacity (Tbps or D2C cell count).** Unpublished; the "large aperture, no deployable" claim has no m^2 attached, so per-satellite throughput is unknown and the "more sats per launch != more capacity per launch" caveat cannot yet be resolved. [UNKNOWN]
5. **Neutron SSO mass and usable fairing volume.** Both still unpublished (inherited NTR-ledger gaps); they bound the SSO count (~12) and the volume cross-check. [ESTIMATE / UNKNOWN, per NTR ledger]
6. **The "~16 per Neutron" provenance.** It is a render-read, not a Rocket Lab statement; a Rocket Lab numeral would upgrade it from ESTIMATE to FACT. [ESTIMATE]
7. **Bus-naming (Flatellite vs Lightning vs Pioneer/Photon).** Section 7 corrects the "$816M SDA = Flatellite" claim; confirm directly which backlog programs are Flatellite vs Lightning. [CORRECTION pending reconciliation]
8. **Whether Rocket Lab's own constellation is funded or aspirational.** The intent is stated; no funded own-constellation program or FCC filing for a Rocket-Lab-operated broadband/D2C constellation is on public record as of June 2026. [UNKNOWN]

---

## Sources

- [Rocket Lab: Announces Flatellite (official PR; "scalable, long-life, high-power, stackable," mass-manufacture, own-constellation, heritage subsystems)](https://rocketlabcorp.com/updates/rocket-lab-announces-flatellite-a-new-satellite-designed-for-mass-manufacture-and-tailored-for-large-constellations/)
- [Business Wire: Rocket Lab Announces Flatellite (verbatim PR text, Beck quote)](https://www.businesswire.com/news/home/20250227111767/en/Rocket-Lab-Announces-Flatellite-A-new-Satellite-Designed-for-Mass-Manufacture-and-Tailored-for-Large-Constellations)
- [SpaceQ: Rocket Lab unveils Flatellite satellite platform ("pizza box," description, Beck quote, heritage subsystems)](https://spaceq.ca/rocket-lab-unveils-flatellite-satellite-platform/)
- [Space Voyaging: Rocket Lab Unveils Flatellite (description, Long Beach production, own-constellation, no specs)](https://www.spacevoyaging.com/news/2025/03/02/rocket-lab-unveils-flatellite-a-new-spacecraft-for-large-satellite-constellations/)
- [SpaceDaily: Rocket Lab Unveils Flatellite, a High-Volume Satellite (deploy mid-2026, 40+ backlog, 13,000 kg-to-LEO Neutron framing)](https://www.spacedaily.com/reports/Rocket_Lab_Unveils_Flatellite_A_High_Volume_Satellite_for_Large_Constellations_999.html)
- [Advanced Television: Rocket Lab showcases Flatellite (description, own-constellation, announcement)](https://www.advanced-television.com/2025/03/03/rocket-lab-showcases-flatellite/)
- [SatNews: Rocket Lab confirms D2C ambitions (Richard French: "large-aperture systems, without the need for deployable [antennas]"; "5G NTN"; "150 to 200-satellite range")](https://satnews.com/2025/04/23/rocket-lab-confirms-d2c-ambitions/)
- [Advanced Television: Rocket Lab confirms D2C ambitions (corroborates the French large-aperture / no-deployable / 5G-NTN / 150-200 quotes)](https://www.advanced-television.com/2025/04/23/rocket-lab-confirms-d2c-ambitions/)
- [illdefined.space: Stacking the Deck: Rocket Lab's Flatellite (the SINGLE source for ~800 kg and ~16/Neutron, both render-reads; author hedges "200 kg less," "more fiction than fact")](https://www.illdefined.space/stacking-the-deck-rocket-labs-flatellite/)
- [Orbital Today: Flatellite, Is Rocket Lab Secretly Building Its Own Mega Constellation? (~800 kg estimate repeated; own-constellation read; mass depends on payload)](https://orbitaltoday.com/2025/03/03/new-mass-manufacture-satellite-flatellite-announced/)
- [Spaceflight Now: SDA awards ~$3.5B for 72 tracking satellites (Rocket Lab $816M/~$805M Tranche 3 on the "Lightning" bus, Phoenix IR + StarLite, missile-tracking, FY2029; references the earlier $515M Transport Layer-Beta Tranche 2)](https://spaceflightnow.com/2025/12/20/space-development-agency-awards-roughly-3-5-billion-to-4-companies-for-72-missile-tracking-and-warning-satellites/)
- [SpaceNews: SDA confirms Rocket Lab will produce 18 satellites (Transport Layer-Beta Tranche 2, $515M, comms/transport)](https://spacenews.com/space-development-agency-confirms-rocket-lab-will-produce-18-satellites-for-u-s-military-network/)
- [DefenseScoop: Rocket Lab to build 18 satellites for SDA's Tranche 2 Beta (Jan 2024 award, predates Flatellite)](https://defensescoop.com/2024/01/08/rocket-lab-sda-tranche-2-beta-award/)
- *(Neutron envelope: 13,000 kg LEO, 5.5 m fairing, ~14 m fairing, ~9,500 kg SSO estimate, ~150-230 m^3 volume estimate cross-referenced from `rocket_lab/neutron/neutron_specs.md` and `payload_and_block_upgrade.md`, SOURCE_INDEX NTR-001..NTR-011; not re-listed. Competitor V3 / Block 2 masses and per-Neutron counts cross-referenced from `rocket_lab/neutron/neutron_comms_payload_fit.md` COMM-225..246 and `competitors/large_array_folding_and_stow.md` COMM-197..208; not re-listed.)*

---

## Claims ledger (COMM-249..COMM-270)

For the catalog/reconciliation step to ingest. Each hard claim with sources and tag.

> **CATALOG NOTE for reconciliation:** This doc was assigned block **COMM-249..COMM-270**. A pre-existing wave-4 lint-report PLAN (`synthesis/comms_wave4_lint_report.md`) tentatively allocated COMM-247..261 to `laser_dc_interconnect_viability.md` and COMM-262..274 to `comms_framework_synthesis.md`, but those two files do NOT actually define COMM-249..274 in their own ledgers (they use local 1..N numbering and only reference older COMM-/LAS- IDs inline). So COMM-249..270 are not materialized elsewhere; this doc materializes them. **If the reconciliation pass prefers to honor the lint-report plan, renumber this doc's block (e.g., to the next free contiguous range above the current global max) rather than the laser/synthesis docs.** Flagged so the collision is resolved deliberately, not silently.

- **COMM-249**: Rocket Lab unveiled **Flatellite** on **27 February 2025** (Long Beach Spacecraft Production Complex): a flat, stackable, mass-manufactured, high-power satellite "designed for mass manufacture and tailored for large constellations." [FACT, multi-source] Sources: Rocket Lab PR / Business Wire; SpaceQ; Space Voyaging; SpaceDaily.
- **COMM-250**: Official description: a **"scalable, long-life, high-power, stackable satellite that enables secure, low-latency, high-speed connectivity and remote sensing capability for national security, defense, and commercial markets,"** built from Rocket Lab heritage subsystems; Beck frames it as "the final step" toward Rocket Lab "operating its own constellation and delivering services from space." [FACT, multi-source] Sources: Rocket Lab PR / Business Wire; SpaceQ; Advanced Television.
- **COMM-251**: Flatellite is **comms-first**: every official description leads with "secure, low-latency, high-speed connectivity / communications connectivity in LEO," with remote sensing named second; it is a constellation-class connectivity platform, not a neutrally-framed generic bus. [FACT, multi-source] Sources: Rocket Lab spacecraft page; Rocket Lab PR; Space Voyaging.
- **COMM-252**: Rocket Lab has published **NO mass, NO power number (only "high-power"), and NO dimensions** for Flatellite; the hard spec sheet is officially undisclosed. [UNKNOWN, official] Source: absence across all Rocket Lab materials and trade coverage.
- **COMM-253**: The widely repeated **~800 kg mass** is a **single third-party analyst's estimate read off a Rocket Lab render** (not a Rocket Lab figure), and that author also floats ~600 kg ("200 kg less") and warns the analysis "may be more fiction than fact." [ESTIMATE, single-source] Source: illdefined.space (repeated, not independently re-measured, by Orbital Today / SpaceDaily).
- **COMM-254**: Flatellite is **designed for Neutron** ("seamless integration with Rocket Lab's own Neutron rocket"); Neutron is the vehicle "sized to deploy stacked Flatellite constellations." Falcon-9 fit is not claimed; no public non-Neutron per-fairing count exists. [FACT for Neutron design intent] Sources: Rocket Lab PR; SpaceQ; SpaceDaily.
- **COMM-255**: Rocket Lab has **not stated a numeral** for Flatellites-per-Neutron; the announcement **render** shows a stack, and the only public count (**~16**) is read off that render. So "~16 per Neutron" is a render-derived estimate, not a Rocket Lab statement. [ESTIMATE, single-source/render] Source: illdefined.space (render-read); Rocket Lab render.
- **COMM-256**: Use **~600-800 kg as an ESTIMATE band** for Flatellite mass, never as fact; true mass depends on the hosted payload and is unpublished; the apparent multi-outlet spread all traces to ONE render-read, so it is effectively single-source. [ESTIMATE, single-source] Source: illdefined.space; Orbital Today (repeating).
- **COMM-257**: Flatellite's mass is **softer evidence** than the competitor benchmarks: Starlink V3 (~1,900 kg) and BlueBird Block 2 (~5,830-6,100 kg) are FACT-grade multi-sourced (per the fit doc), whereas Flatellite's ~800 kg is an unsourced render-read; therefore any Flatellite-per-Neutron count is estimate-bound, not FACT-bound. [DERIVED] Sources: cross-ref `neutron_comms_payload_fit.md` (COMM-225..246); illdefined.space.
- **COMM-258**: **Mass-bound count:** Neutron 13,000 kg LEO / ~800 kg = **~16** (/ ~600 kg = ~22); ~9,500 kg SSO / ~800 kg = **~12** (/ ~600 kg = ~16); 15,000 kg expendable-LEO = ~19-25. [DERIVED on a single-source mass estimate] Sources: Neutron envelope (NTR ledger via `neutron_specs.md`); Flatellite mass estimate (COMM-256).
- **COMM-259**: **Volume-bound count cannot be computed independently** (Flatellite stowed volume unpublished); Rocket Lab's own render packing **~16** Flatellites into the Neutron fairing IS the company's implicit combined mass-and-volume answer, consistent with the ~150-230 m^3 usable-volume estimate. [DERIVED / render-read] Sources: Rocket Lab render (via illdefined.space); usable-volume estimate (NTR ledger).
- **COMM-260**: **Per-Neutron working number: ~16 Flatellites to LEO, ~12 to SSO**, both estimate-bound. At LEO the mass gate (13,000/800 = 16.3) and the render (~16) CONVERGE; at SSO the lower ~9,500 kg mass allowance binds below the render at ~12. Carry **~12-16 (SSO-to-LEO), estimate-bound**, not a point. [DERIVED] Sources: COMM-258, COMM-259.
- **COMM-261**: Flatellite is explicitly tied to **Rocket Lab operating its OWN constellation** (Beck: "operating our own constellation and delivering services from space"); the own-constellation is a stated strategic intent, not (publicly) a funded program or filed system. [FACT for the stated ambition] Sources: Rocket Lab PR / Business Wire; Advanced Television; SatNews.
- **COMM-262**: Rocket Lab VP **Richard French** framed Flatellite for **direct-to-cell / 5G NTN**: "an elegant solution for **large-aperture systems, without the need for deployable [antennas]**," "5G NTN ... a great example of a commercial application," with **"minimum viable constellations in the 150 to 200-satellite range."** [FACT, multi-source] Sources: SatNews (23 Apr 2025); Advanced Television (23 Apr 2025).
- **COMM-263**: Flatellite chooses the **V3 side of the fold asymmetry for a D2C mission**: a large FLAT aperture (the body) with NO deployable, so it is plausibly mass-bound (like V3) not antenna-stow-bound (like BlueBird Block 2); the trade is a smaller, footprint-capped aperture, making per-satellite capacity the open question. [DERIVED] Sources: cross-ref `large_array_folding_and_stow.md` (COMM-197..208); COMM-262.
- **COMM-264**: Sanity check vs the fit doc: Flatellite ~16/Neutron (LEO) is **~3x the ~5 V3-class/launch** (because lighter) and far above the **~1 Block-2/launch** (because no folding antenna), confirming "purpose-build to Neutron's envelope" as the satellites-per-launch lever; capacity-per-launch is NOT thereby settled. [DERIVED] Sources: cross-ref `neutron_comms_payload_fit.md` (COMM-225..246).
- **COMM-265**: Flatellite is a **real production program** (high-volume line at Long Beach), with Rocket Lab reporting a **backlog exceeding 40 spacecraft** across commercial/civil/national-security customers. [FACT] Sources: SpaceDaily; Rocket Lab; cross-ref `manufacturing_capability_2026.md`.
- **COMM-266**: Rocket Lab states intent to **deploy Flatellite constellations starting mid-2026**, with multi-launch Neutron agreements signed (incl. a confidential commercial-constellation deal); gated by Neutron's first flight (targeted Q4 2026). [FACT for stated intent] Sources: SpaceDaily; Business Wire (multi-launch Neutron contract).
- **COMM-267**: **No public record of a Flatellite on orbit** as of June 2026; no first-flight/demonstration date announced; deployment depends on Neutron, which has not yet flown. [UNKNOWN / not yet flown] Source: absence across trade coverage; Neutron status (NTR ledger).
- **COMM-268**: Rocket Lab has **not published a Flatellite production rate** (no satellites-per-month or per-unit build time), only "high volumes / mass manufacture." [UNKNOWN] Sources: Rocket Lab materials; cross-ref `manufacturing_capability_2026.md`.
- **COMM-269**: **Bus-naming correction:** the **$816M (~$805M) SDA Tracking Layer Tranche 3** (18 missile-tracking sats, Phoenix IR + StarLite, ~FY2029) is built on Rocket Lab's **"Lightning"** bus, NOT Flatellite; the **$515M Transport Layer-Beta Tranche 2** (18 comms/optical-mesh sats) was awarded **Jan 2024**, predating Flatellite (Feb 2025), so it is not Flatellite either. The existing corpus claim "Flatellite is produced for the $816M SDA contract" is a conflation to correct in reconciliation. [CORRECTION, multi-source] Sources: Spaceflight Now; SpaceNews; DefenseScoop; SatNews.
- **COMM-270**: The **open performance question** is **capacity per flat satellite**, not launch fit: a flat non-deployed aperture is smaller than BlueBird's 223 m^2 unfurled array, so "more satellites per launch" (16 vs 1) does NOT equal "more capacity per launch" until Flatellite's aperture/power/throughput are published (all currently UNKNOWN). [DERIVED] Sources: COMM-262, COMM-263; absence of published Flatellite capacity.
