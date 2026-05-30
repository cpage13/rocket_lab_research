# Best US Launch Site for a High-Cadence Neutron SSO Campaign: Stay at Wallops, or Relocate (and Where)?

**Research date:** 2026-05-30
**Purpose:** For a sustained, high-cadence Rocket Lab Neutron sun-synchronous-orbit (SSO, ~97 to 98 degree inclination) campaign optimizing BOTH (a) SSO payload performance and (b) reusable first-stage recovery, identify the best US launch site. Wallops/MARS, Virginia (LC-3) is the starting assumption (Neutron can launch SSO from there today via a southerly Atlantic dogleg). The real question this doc answers: to maximize SSO performance, would Rocket Lab eventually relocate, and if so, to where?

**Relationship to existing project research (build on, do NOT redo):**
- `sso_from_virginia_feasibility.md` already established that LC-3/Virginia is Neutron's confirmed pad and that SSO from Wallops is a probable-yes via a southerly Atlantic dogleg, with an estimated extra ~5 to 15% dogleg payload penalty on top of the ~25 to 30% LEO-to-SSO penalty. This doc takes that as given and asks the comparative site-selection question.
- `sso_recovery_cadence_falcon_analogue.md` already covered the Falcon-9 recovery/cadence analogue. This doc references recovery only as it bears on site choice.
- `neutron_payload_vs_orbit.md` / `payload_and_block_upgrade.md` hold the working ~11 t SSO-from-Wallops figure (12.5 t block-upgrade SSO minus dogleg) with ~9.5 t a conservative floor. This doc does NOT redo payload math; it reasons in single-digit-percent terms only.

**Tagging convention (matching the sibling docs):**
- **[FACT]** = flown, documented event, or directly company/agency/operator-stated.
- **[RL-STATED]** = stated by Rocket Lab or the Neutron Payload User's Guide for an un-flown vehicle (design value).
- **[ANALOGY]** = another vehicle/site used by inference to inform the Neutron conclusion.
- **[ESTIMATE/DERIVED]** = arithmetic or reasoning performed here; not an official figure.

---

## BLUF (bottom line up front)

For a high-cadence Neutron SSO data-center campaign, **Wallops/MARS, Virginia (LC-3) is genuinely "good enough" to START**, and is in fact the only option Rocket Lab has in the near term (it is the only built Neutron pad, and Neutron has not yet flown). But Wallops is **not** the performance-optimal SSO site: reaching ~98 degree retrograde inclination from the East Coast requires a southerly Atlantic dogleg that costs an estimated extra ~5 to 15% payload **[ESTIMATE/DERIVED]** on top of the SSO penalty, and the cross-range of that dogleg pushes recovery toward a downrange droneship rather than return-to-launch-site (RTLS). The single best US site for **both** SSO payload **and** clean reusable recovery is a **West Coast site at Vandenberg SFB, California (~34.7 N)**: it launches SSO/polar **directly south over open Pacific with no dogleg** (azimuth corridor ~158 to 201 degrees) **[FACT]**, which both recovers the dogleg payload penalty and re-enables RTLS (SpaceX already lands Falcon boosters at Vandenberg's Landing Zone 4) **[FACT]**. The catch: **Rocket Lab has made no public statement of a West Coast / Vandenberg Neutron pad as of May 2026 [FACT]**, and the two open Vandenberg/Cape Space Force pad solicitations (SLC-14, SLC-46) are explicitly for heavy/super-heavy vehicles and **exclude medium-lift Neutron [FACT]**, so a West Coast Neutron pad is a plausible future move, not an announced one.

**A geography correction that matters:** the founder's instinct to "go further south toward the equator" is correct for low-inclination eastward launches but **backwards for SSO**. SSO needs ~98 degrees regardless of launch latitude, so a more equatorial site does **not** help SSO; what matters is an **unobstructed retrograde/polar launch azimuth over open ocean**, which favors a West-Coast Vandenberg-style site, **not** a more southerly East Coast or equatorial one **[FACT, see Section 3]**.

**Site ranking for a high-cadence Neutron SSO campaign (best to worst):**
1. **Vandenberg SFB, California (West Coast)** - best SSO performance (direct south, no dogleg) AND best recovery (RTLS feasible, proven by SpaceX LZ-4). The performance-optimal relocation target. **[ESTIMATE/DERIVED, on FACT-based geometry]**
2. **Wallops/MARS, Virginia (LC-3)** - good enough to start, only built option, but SSO needs a dogleg (extra ~5 to 15% est. payload hit) and the cross-range pushes toward droneship recovery. **[FACT it is the pad; ESTIMATE the penalty]**
3. **Cape Canaveral / Kennedy, Florida** - SSO is possible via a dogleg over Cuba (SAOCOM 1B precedent, with RTLS to LZ-1), but more southerly latitude does NOT help SSO, and it is not a Rocket Lab site. No advantage over Wallops for SSO. **[FACT precedent; ESTIMATE ranking]**
4. **Kodiak / Pacific Spaceport Complex - Alaska (PSCA), 57.4 N** - geometrically excellent for SSO (widest US azimuth range, clean polar corridor, no dogleg), but far north, weather-limited, historically low cadence, and not a Rocket Lab medium-lift site. Wrong fit for a *high-cadence* campaign. **[FACT geometry; ESTIMATE ranking]**

---

## 1. Is Wallops adequate to START a sustained SSO campaign, and what would relocating buy?

### 1.1 Wallops is adequate to start - and is effectively the only choice in the near term [FACT]
LC-3 at MARS/Wallops is Rocket Lab's **only built Neutron pad**, ribbon-cut 28 Aug 2025, and Neutron has **not yet flown** (first flight targeted Q4 2026) ([Rocket Lab LC-3 opening, BusinessWire, 27 Aug 2025](https://www.businesswire.com/news/home/20250827593085/en/Rocket-Lab-Opens-Launch-Complex-3-A-Critical-Milestone-On-The-Path-To-Neutrons-First-Launch); [NASASpaceFlight, Aug 2025](https://www.nasaspaceflight.com/2025/08/rocket-lab-inaugurates-lc-3-wallops/)). There is no second Neutron pad. So for the first years of any SSO campaign, Wallops is not just adequate, it is the only option, and the prior project research already concluded SSO from Wallops is a probable-yes via a southerly Atlantic dogleg (see `sso_from_virginia_feasibility.md`).

The standard MARS corridor is mid-inclination (~38 to 60 degrees), built for ISS-class easterly/northeasterly launches over the Atlantic, **not** SSO ([Mid-Atlantic Regional Spaceport, Wikipedia](https://en.wikipedia.org/wiki/Mid-Atlantic_Regional_Spaceport); [Virginia Spaceport Authority, Facilities](https://www.vaspace.org/our-facilities)). SSO from Wallops therefore requires going outside the standard corridor: a southerly track plus a dogleg, the same mechanism by which Cape Canaveral reopened polar launches (Section 2.3 of the sibling doc; Section 3.2 here). It is feasible, but it is the long way around to ~98 degrees.

### 1.2 What relocating to a West Coast site would specifically buy
Two distinct gains, both flowing from the same fact (a West Coast site launches SSO directly south over open ocean with no dogleg):

**(a) SSO payload: recover the dogleg penalty (estimated ~5 to 15%).**
The dogleg required to reach ~98 degrees from the East Coast costs an estimated extra ~5 to 15% payload **[ESTIMATE/DERIVED, established in `sso_from_virginia_feasibility.md`]** on top of the ~25 to 30% LEO-to-SSO penalty. A direct-south Vandenberg launch needs no dogleg, so that incremental azimuth-steering loss largely disappears. In the project's single-digit-percent framing, that is a meaningful (not marginal) recovery of usable SSO mass - roughly the difference between the project's ~9.5 t conservative floor and its ~11 t working SSO figure. **[ESTIMATE/DERIVED]**

**(b) Recovery: re-enable RTLS instead of droneship.**
This is the under-appreciated gain. Neutron's published recovery tiers to LEO are **13,000 kg with a downrange droneship landing** ("Return On Investment" platform) versus **8,500 kg with RTLS** ([Rocket Lab / Wikipedia Neutron](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron); [Rocket Lab "Return On Investment" platform reveal, BusinessWire, Feb 2025](https://www.businesswire.com/news/home/20250227129978/en/Rocket-Lab-Reveals-Ocean-Platform-for-Neutron-Rocket-Landings-at-Sea)). The East Coast SSO dogleg adds cross-range, which biases recovery toward the downrange droneship (more ships, more marine ops, slower turnaround). A West Coast direct-south launch keeps the trajectory in-plane and downrange-clean, which is exactly the geometry under which SpaceX recovers Falcon boosters at Vandenberg, either downrange or RTLS to Landing Zone 4 (Section 4). For a **high-cadence** campaign, RTLS-capable geometry is the bigger structural advantage: pad-adjacent recovery avoids the droneship logistics bottleneck. **[ESTIMATE/DERIVED, on FACT-based geometry]**

### 1.3 Net judgment
Wallops is good enough to start and unavoidable in the near term. Relocating to the West Coast would buy (a) recovery of the ~5 to 15% dogleg payload penalty and (b) RTLS-capable recovery geometry that suits high cadence. Neither is a step-change in vehicle capability; both are real, structural improvements to an SSO-specialized, high-cadence operation. **[ESTIMATE/DERIVED]**

---

## 2. Candidate US site comparison for SSO + booster recovery

| Site | Latitude | SSO (~98 deg) reachability | Dogleg needed for SSO? | Recovery for SSO | Rocket Lab status |
|---|---|---|---|---|---|
| **Wallops / MARS, VA (LC-3)** | ~37.8 N | Probable-yes (sibling doc) | **Yes** - southerly Atlantic dogleg | Droneship-biased by cross-range; RTLS harder | **Neutron's only built pad [FACT]** |
| **Vandenberg SFB, CA** | ~34.7 N | **Yes, directly [FACT]** | **No** - launches due south over Pacific | **RTLS feasible (LZ-4 proven) or droneship [FACT]** | **No public Neutron plan [FACT]** |
| **Cape Canaveral / KSC, FL** | ~28.5 N | Yes via dogleg (SAOCOM 1B precedent) | **Yes** - dogleg south over Cuba | RTLS demonstrated (LZ-1, SAOCOM 1B) | Not a Rocket Lab site; medium-lift excluded from open RFI |
| **Kodiak / PSCA, AK** | ~57.4 N | **Yes, directly [FACT]** | **No** - widest US azimuth range | Open Pacific downrange; RTLS unproven there | Not a Rocket Lab site |

### 2.1 Wallops / MARS, Virginia (~37.8 N) - dogleg for SSO; recovery biased to droneship
Covered in detail in `sso_from_virginia_feasibility.md`. Summary for this comparison: SSO requires leaving the standard 38 to 60 degree corridor and flying a southerly Atlantic dogleg **[FACT corridor; RL-STATED SSO; ANALOGY mechanism]**. The dogleg's cross-range biases recovery toward the downrange droneship rather than RTLS. **[ESTIMATE/DERIVED]**

### 2.2 Vandenberg SFB, California (~34.7 N) - direct south, no dogleg, RTLS proven
Vandenberg is "located at 34.7 degrees North latitude with a clear southward flight path over open ocean, making it the premier U.S. site for sun-synchronous orbit (SSO) and polar orbit missions" ([Orbital Radar, Vandenberg profile](https://orbitalradar.com/spaceports/vandenberg)). Its allowable launch azimuths are **southward, ~158 to 201 degrees** (the corridor cleared when it was being prepared as the polar Space Shuttle site), which "only allows for southward launches, making the spaceport suitable for supporting direct launches to polar and near-polar orbits" ([Orbital Radar](https://orbitalradar.com/spaceports/vandenberg); [The Planetary Society, "Of inclinations and azimuths"](https://www.planetary.org/articles/3450)). SSO (~98 deg) is reached **directly, with no dogleg** - the defining advantage over every East Coast option for SSO payload.

**Recovery at Vandenberg [FACT]:** SLC-4 has two pads; SpaceX uses one for Falcon 9 launches and the other as **Landing Zone 4 (LZ-4)**, with RTLS landing operations there since 2018 ([Vandenberg Space Launch Complex 4, Wikipedia](https://en.wikipedia.org/wiki/Vandenberg_Space_Launch_Complex_4)). This is direct proof that a West Coast direct-south SSO/polar launch is compatible with RTLS recovery - the exact combination a high-cadence Neutron SSO campaign wants.

**Rocket Lab West Coast / Vandenberg plans for Neutron:** **None publicly stated as of May 2026 [FACT].** Searches of Rocket Lab releases, Peter Beck interviews, and trade press surface only: LC-3/Wallops as the Neutron launch site; the Archimedes engine **test** complex at NASA Stennis (Mississippi); and the engine **development** complex in Long Beach, California ([Rocket Lab, Neutron](https://rocketlabcorp.com/launch/neutron/); [Space.com, LC-3 opening](https://www.space.com/space-exploration/private-spaceflight/virginia-is-for-space-lovers-rocket-lab-opens-new-seaside-launch-pad-for-reusable-neutron-rocket)). Long Beach and Stennis are California/Mississippi facilities but they are **manufacturing/test**, not launch. So a West Coast Neutron **launch** site is, at this date, an inference about the performance-optimal future, not an announced plan.

**Important pad-availability nuance [FACT]:** The two currently open Space Force pad solicitations are **not** a Neutron path. In late Dec 2025 the Space Force issued RFIs for **SLC-46 at Cape Canaveral** (super-heavy, >50,000 kg to LEO) and **SLC-14 at Vandenberg** (heavy 20,000 to 50,000 kg and super-heavy), and these explicitly target heavy/super-heavy vehicles; the Spaceflight Now coverage states plainly that Rocket Lab's Neutron and Firefly's Eclipse are "classified as medium lift rockets" and are "not in contention for SLC-14" ([Spaceflight Now, SLC-14 RFI, 6 Jan 2026](https://spaceflightnow.com/2026/01/06/dept-of-the-air-force-opens-bidding-for-space-launch-complex-14-at-vandenberg-sfb/); [NASASpaceFlight, Cape/Vandenberg RFI, Jan 2026](https://www.nasaspaceflight.com/2026/01/space-force-launch-interest-cape-vandenberg-pads/)). SpaceX already holds **SLC-6** at Vandenberg (redevelopment finalized Oct 2025, two landing zones, Falcon launches/landings) ([Spaceflight Now, SLC-6, May 2025](https://spaceflightnow.com/2025/05/19/department-of-the-air-force-issues-draft-documents-for-new-spacex-launch-site-at-vandenberg-space-force-base/); [Vandenberg Space Launch Complex 6, Wikipedia](https://en.wikipedia.org/wiki/Vandenberg_Space_Launch_Complex_6)). A future Neutron West Coast pad would therefore most plausibly be a **different existing or refurbished Vandenberg complex**, secured via a Rocket-Lab-specific arrangement, not via these heavy-lift RFIs. **[FACT on the RFIs; ESTIMATE on the implication]**

### 2.3 Cape Canaveral / Kennedy, Florida (~28.5 N) - SSO via dogleg over Cuba; not a clear win
Cape Canaveral's allowable azimuths run ~35 to 120 degrees (land-overflight limited), normally yielding inclinations ~28.5 to 59 degrees ([The Planetary Society](https://www.planetary.org/articles/3450)). SSO is nonetheless achievable via a southerly dogleg: **SAOCOM 1B (30 Aug 2020)** was the first polar launch from the Cape in ~50 years, flying south-southeast then turning to skirt Florida and overfly Cuba to reach its polar/SSO orbit, with the **booster recovered RTLS to Landing Zone 1** ([Spaceflight Now, SAOCOM 1B, Aug 2020](https://spaceflightnow.com/2020/08/31/spacex-launches-first-polar-orbit-mission-from-florida-in-decades/); [SAOCOM, Wikipedia](https://en.wikipedia.org/wiki/SAOCOM)). So Florida proves a dogleg-SSO + RTLS profile is possible from the East Coast.

But for **SSO specifically, Florida offers no advantage over Wallops**, and the more-southerly latitude does **not** help (Section 3). It still needs a dogleg, it overflies Cuba/Caribbean (a harder corridor than Wallops' open-Atlantic southerly track), and it is not a Rocket Lab site. It is a useful precedent, not a relocation candidate for Neutron. **[FACT precedent; ESTIMATE conclusion]**

### 2.4 Kodiak / Pacific Spaceport Complex - Alaska (PSCA), 57.4 N - geometrically ideal, wrong operational fit
PSCA at Narrow Cape, Kodiak Island (57.44 N) is the US's northernmost orbital spaceport and "enjoys the largest launch azimuth range of any spaceport in the US," with **unrestricted downrange azimuths ~110 to 220 degrees** reaching polar and sun-synchronous orbits between ~59 and 110 degrees inclination - purpose-built for polar/SSO with no land overflight and no dogleg ([Alaska Aerospace, Spaceports](https://akaerospace.com/spaceports); [Pacific Spaceport Complex - Alaska, Wikipedia](https://en.wikipedia.org/wiki/Pacific_Spaceport_Complex_%E2%80%93_Alaska)). Geometrically it is excellent for SSO.

But it is the wrong fit for a **high-cadence reusable** campaign: far-north latitude with severe weather constraints, historically very low launch cadence, no demonstrated booster-recovery infrastructure, and it is not a Rocket Lab medium-lift site. A high-cadence data-center campaign needs throughput and recovery turnaround, which Kodiak does not offer. **[FACT geometry; ESTIMATE operational judgment]**

---

## 3. Geography clarification: does going "south toward the equator" help SSO? (No - it is backwards for SSO)

This is the key correction to the founder's musing, and the sources are unambiguous.

**SSO requires ~98 degrees regardless of launch latitude. [FACT]** A sun-synchronous orbit is retrograde and near-polar: for typical 600 to 800 km altitudes it sits at roughly 97.8 to 98.7 degrees inclination, set by the orbit's nodal-precession-matches-the-Sun requirement, **not** by where you launch from ([Sun-synchronous orbit, Wikipedia](https://en.wikipedia.org/wiki/Sun-synchronous_orbit); [Spire, SSO](https://spire.com/spirepedia/sun-synchronous-orbit-sso/)). Every SSO mission, from any site, must end up at ~98 degrees.

**Latitude helps low-inclination eastward launches, NOT SSO. [FACT]** A due-east launch achieves an inclination equal to the launch site's latitude, and the closer to the equator, the more free velocity Earth's eastward rotation contributes - which is why equatorial sites are prized for low-inclination, prograde (eastward) orbits like GEO transfer ([The Planetary Society, "Of inclinations and azimuths"](https://www.planetary.org/articles/3450)). SSO is the opposite case: it is **retrograde** (flown against Earth's rotation), so "launches cannot benefit from Earth's rotation the way an equatorial launch can, so payload capacity shrinks" ([Sun-synchronous orbit, Grokipedia](https://grokipedia.com/page/Sun-synchronous_orbit), summarizing the standard retrograde-SSO penalty). Going more equatorial does not reduce the ~98-degree requirement and does not add usable energy for a retrograde orbit; if anything the larger eastward rotation you would have to cancel is a (small) liability, not an asset, for retrograde SSO.

**What actually matters for SSO is an unobstructed retrograde/polar azimuth over open ocean. [FACT]** Because the inclination is fixed near 98 degrees, the only thing the site can optimize is whether the rocket can fly that near-polar/retrograde heading **directly** over open water without a dogleg and without overflying land. That is exactly why US polar/SSO launches go from **Vandenberg** (clear southward Pacific corridor) and **Kodiak** (widest azimuth range), and why the East Coast (Wallops, the Cape) must dogleg ([The Planetary Society](https://www.planetary.org/articles/3450); [Orbital Radar, Vandenberg](https://orbitalradar.com/spaceports/vandenberg); [Alaska Aerospace](https://akaerospace.com/spaceports)).

**Conclusion (confirms the project's framing):** For SSO, a more southerly/equatorial US site does **not** help; latitude is largely irrelevant because SSO needs ~98 degrees regardless. What matters is an **unobstructed polar/retrograde launch azimuth over open ocean**, which favors a **West-Coast Vandenberg-style site**. Equatorial/southerly sites favor **eastward, low-inclination** launches, the opposite of SSO. The founder's "go south toward the equator" instinct is right for a low-inclination LEO/GEO constellation but **inverted for an SSO campaign**. **[FACT-grounded conclusion]**

---

## 4. Recovery: which site best supports high-cadence reusable recovery for SSO?

The recovery question turns on cross-range, and cross-range turns on whether the SSO trajectory is in-plane (direct south) or doglegged.

**Neutron's recovery-mode payload tiers [FACT/RL-STATED]:** to LEO, **13,000 kg with downrange droneship landing** versus **8,500 kg with RTLS**, and **15,000 kg fully expendable** ([Rocket Lab Neutron, Wikipedia](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron); [Rocket Lab platform reveal, BusinessWire, Feb 2025](https://www.businesswire.com/news/home/20250227129978/en/Rocket-Lab-Reveals-Ocean-Platform-for-Neutron-Rocket-Landings-at-Sea)). Rocket Lab's stated sequence is RTLS first (landing at LC-3), then downrange landing on the "Return On Investment" platform for extended-performance missions ([Rocket Lab platform reveal](https://www.businesswire.com/news/home/20250227129978/en/Rocket-Lab-Reveals-Ocean-Platform-for-Neutron-Rocket-Landings-at-Sea)). The RTLS-vs-droneship gap is large (8.5 t vs 13 t to LEO), so recovery mode is a first-order driver of usable payload.

**East Coast SSO (Wallops, the Cape): dogleg cross-range biases toward droneship. [ESTIMATE/DERIVED]** The southerly dogleg needed to reach ~98 degrees adds lateral displacement and downrange distance, which generally pushes recovery toward a downrange droneship rather than RTLS. SAOCOM 1B shows RTLS is **not impossible** with a dogleg (it landed at LZ-1) ([Spaceflight Now, SAOCOM 1B](https://spaceflightnow.com/2020/08/31/spacex-launches-first-polar-orbit-mission-from-florida-in-decades/)), but that was a relatively light payload (3,050 kg) on a vehicle with large RTLS margin; for a heavier Neutron SSO payload the dogleg makes RTLS harder and droneship the more likely high-performance mode. For high cadence, droneship dependence is a logistics tax: marine recovery, tow-back, and refurbishment cycles gate turnaround.

**West Coast direct-south SSO (Vandenberg): RTLS feasible. [FACT geometry]** A direct-south Vandenberg launch keeps the SSO trajectory in-plane with minimal cross-range, which is precisely the regime in which SpaceX lands Falcon 9 boosters at **Vandenberg LZ-4** (RTLS since 2018) as well as on West Coast droneships ([Vandenberg SLC-4 / LZ-4, Wikipedia](https://en.wikipedia.org/wiki/Vandenberg_Space_Launch_Complex_4)). For a high-cadence campaign, pad-adjacent RTLS is the structurally faster recovery mode (no ship cycle), and West Coast geometry makes it attainable for SSO in a way the East Coast dogleg does not.

**Answer:** A **West Coast direct-south site supports high-cadence reusable SSO recovery best**, because it both reduces cross-range and re-enables RTLS. The Wallops dogleg, by adding cross-range, pushes toward downrange droneship recovery (slower turnaround), whereas a West Coast direct-south launch allows RTLS - confirming the framing in the question. **[ESTIMATE/DERIVED, on FACT-based geometry]**

---

## 5. BOTTOM LINE: ranking, "good enough to start," and what relocation buys

**Is Wallops good enough to start? Yes - and it is effectively mandatory in the near term.** LC-3 is Rocket Lab's only built Neutron pad, Neutron has not yet flown, and the prior project research already concluded SSO from Wallops is a probable-yes via a southerly Atlantic dogleg. A high-cadence SSO campaign can and must begin at Wallops. **[FACT]**

**Is Wallops performance-optimal for SSO? No.** The East Coast dogleg to ~98 degrees costs an estimated extra ~5 to 15% payload **[ESTIMATE/DERIVED]** and biases recovery toward droneship rather than RTLS.

**Ranking for a high-cadence Neutron SSO data-center campaign (best to worst):**
1. **Vandenberg SFB, California (West Coast)** - direct-south SSO with no dogleg (recovers the dogleg payload penalty) AND RTLS-feasible recovery (proven by SpaceX LZ-4). The performance-optimal relocation target for an SSO-specialized, high-cadence operation. Caveat: no announced Rocket Lab Neutron pad there, and the open heavy/super-heavy RFIs (SLC-14) exclude Neutron, so this is the most likely future move, not a current plan. **[ESTIMATE/DERIVED ranking; FACT geometry and recovery; FACT no announced plan]**
2. **Wallops / MARS, Virginia (LC-3)** - good enough to start, only built option, but SSO needs a dogleg and recovery is droneship-biased. **[FACT pad; ESTIMATE penalty]**
3. **Cape Canaveral / KSC, Florida** - SSO possible via dogleg over Cuba (SAOCOM 1B, RTLS to LZ-1), but a more southerly latitude does NOT help SSO; no advantage over Wallops and not a Rocket Lab site. **[FACT precedent; ESTIMATE ranking]**
4. **Kodiak / PSCA, Alaska** - geometrically ideal for SSO (no dogleg) but far north, weather-limited, low historical cadence, no recovery infrastructure; wrong fit for high cadence. **[FACT geometry; ESTIMATE ranking]**

**What relocation (most likely West Coast / Vandenberg) would buy:**
- **SSO payload:** recovery of the estimated ~5 to 15% dogleg penalty by eliminating the dogleg (direct south). **[ESTIMATE/DERIVED]**
- **Recovery:** RTLS-feasible geometry (proven analogue: Vandenberg LZ-4) instead of droneship-biased recovery, which materially helps **high-cadence** turnaround. **[FACT analogue; ESTIMATE benefit]**
- **Specialization:** co-locating an SSO campaign at the premier US SSO/polar site, where the range, corridor, and recovery infrastructure are all already oriented to southward polar flight. **[FACT]**

**The geography correction to carry forward:** for SSO, do NOT go south toward the equator. SSO is ~98 degrees regardless of latitude; the lever is an unobstructed retrograde/polar azimuth over open ocean, which means **West Coast (Vandenberg), not a more southerly East Coast or equatorial site**. **[FACT-grounded]**

---

## Sources

**Neutron vehicle, pad, and recovery (Rocket Lab / encyclopedic):**
- Rocket Lab Neutron, Wikipedia (payload tiers 15 t expendable / 13 t droneship / 8.5 t RTLS; "Return On Investment" downrange platform; LC-3 pad): https://en.wikipedia.org/wiki/Rocket_Lab_Neutron
- Rocket Lab, "Rocket Lab Opens Launch Complex 3..." (LC-3 ribbon-cutting 28 Aug 2025), BusinessWire: https://www.businesswire.com/news/home/20250827593085/en/Rocket-Lab-Opens-Launch-Complex-3-A-Critical-Milestone-On-The-Path-To-Neutrons-First-Launch
- Rocket Lab, "Rocket Lab Reveals Ocean Platform for Neutron Rocket Landings at Sea" (RTLS-first then downrange "Return On Investment"; 13 t reusable / 15 t expendable framing), BusinessWire, Feb 2025: https://www.businesswire.com/news/home/20250227129978/en/Rocket-Lab-Reveals-Ocean-Platform-for-Neutron-Rocket-Landings-at-Sea
- Rocket Lab, Neutron product page (Long Beach engine development; Stennis engine test; LC-3 launch): https://rocketlabcorp.com/launch/neutron/
- NASASpaceFlight, "Rocket Lab inaugurates LC-3 at Wallops," Aug 2025: https://www.nasaspaceflight.com/2025/08/rocket-lab-inaugurates-lc-3-wallops/
- Space.com, "Virginia is for (space) lovers... Rocket Lab opens new seaside launch pad for Neutron": https://www.space.com/space-exploration/private-spaceflight/virginia-is-for-space-lovers-rocket-lab-opens-new-seaside-launch-pad-for-reusable-neutron-rocket

**Launch-site geometry, azimuth corridors, and SSO (geometry sources):**
- The Planetary Society, "Of inclinations and azimuths" (due-east inclination = latitude; Cape azimuths ~35 to 120 deg; why polar/SSO goes from Vandenberg): https://www.planetary.org/articles/3450
- Sun-synchronous orbit, Wikipedia (~97.8 to 98.7 deg; retrograde; nodal-precession definition): https://en.wikipedia.org/wiki/Sun-synchronous_orbit
- Spire, "Sun-Synchronous Orbit (SSO)" (retrograde, near-polar, ~98 deg): https://spire.com/spirepedia/sun-synchronous-orbit-sso/
- Sun-synchronous orbit, Grokipedia (retrograde SSO cannot benefit from Earth's rotation; payload shrinks): https://grokipedia.com/page/Sun-synchronous_orbit
- Dogleg maneuver, Wikipedia (STS-36 ~5 deg KSC dogleg; GRAB/Cuba dogleg to 70 deg; small-rocket polar penalty): https://en.wikipedia.org/wiki/Dogleg_maneuver

**Wallops / MARS, Virginia:**
- Mid-Atlantic Regional Spaceport, Wikipedia (38 to 60 deg corridor; LP-0D = LC-3 mapping): https://en.wikipedia.org/wiki/Mid-Atlantic_Regional_Spaceport
- Virginia Spaceport Authority, Facilities (38 to 60 deg; "potential to support sun-synchronous orbit missions"): https://www.vaspace.org/our-facilities

**Vandenberg SFB, California:**
- Orbital Radar, Vandenberg profile (34.7 N; premier US SSO/polar site; southward azimuth ~158 to 201 deg): https://orbitalradar.com/spaceports/vandenberg
- Vandenberg Space Launch Complex 4, Wikipedia (SLC-4 + Landing Zone 4 / LZ-4; RTLS landings since 2018): https://en.wikipedia.org/wiki/Vandenberg_Space_Launch_Complex_4
- Vandenberg Space Launch Complex 6, Wikipedia (SLC-6 to SpaceX; two landing zones): https://en.wikipedia.org/wiki/Vandenberg_Space_Launch_Complex_6
- Spaceflight Now, "Department of the Air Force issues draft documents for new SpaceX launch site at Vandenberg" (SLC-6 redevelopment), May 2025: https://spaceflightnow.com/2025/05/19/department-of-the-air-force-issues-draft-documents-for-new-spacex-launch-site-at-vandenberg-space-force-base/

**Space Force pad RFIs (Neutron exclusion):**
- Spaceflight Now, "Dept. of the Air Force opens bidding for Space Launch Complex 14 at Vandenberg SFB" (heavy 20 to 50 t / super-heavy >50 t; Neutron and Firefly Eclipse "not in contention for SLC-14"), 6 Jan 2026: https://spaceflightnow.com/2026/01/06/dept-of-the-air-force-opens-bidding-for-space-launch-complex-14-at-vandenberg-sfb/
- NASASpaceFlight, "Space Force requests launch provider interest in Cape and Vandenberg pads" (SLC-46 Cape super-heavy; SLC-14 Vandenberg heavy/super-heavy), Jan 2026: https://www.nasaspaceflight.com/2026/01/space-force-launch-interest-cape-vandenberg-pads/

**Cape Canaveral SSO precedent (SAOCOM 1B):**
- Spaceflight Now, "SpaceX launches first polar orbit mission from Florida in decades" (dogleg south over Cuba; booster RTLS to Landing Zone 1; FAA enablers: booster flyback + autonomous flight safety), 31 Aug 2020: https://spaceflightnow.com/2020/08/31/spacex-launches-first-polar-orbit-mission-from-florida-in-decades/
- SAOCOM, Wikipedia (SAOCOM 1B ~98 deg SSO from Cape Canaveral): https://en.wikipedia.org/wiki/SAOCOM

**Kodiak / Pacific Spaceport Complex - Alaska:**
- Alaska Aerospace, Spaceports (largest US azimuth range; polar/SSO 59 to 110 deg inclination): https://akaerospace.com/spaceports
- Pacific Spaceport Complex - Alaska, Wikipedia (57.44 N; unrestricted downrange azimuths ~110 to 220 deg): https://en.wikipedia.org/wiki/Pacific_Spaceport_Complex_%E2%80%93_Alaska
