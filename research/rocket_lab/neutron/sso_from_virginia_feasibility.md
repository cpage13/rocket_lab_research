# Can Neutron Reach Sun-Synchronous Orbit (SSO) from Virginia? Site, Corridor, and Dogleg Payload Penalty

**Research date:** 2026-05-29
**Purpose:** Confirm whether Rocket Lab Neutron can reach a sun-synchronous orbit (SSO, ~97 to 98 degree inclination) from its **Virginia** launch site (Launch Complex 3, Wallops Island), and quantify any payload penalty from the launch-azimuth geometry. This matters because, for US military and US-payload applications, the launch **must be from US soil (Virginia)**; the New Zealand site is not acceptable. The question is whether Virginia is an SSO-capable site, and at what cost.

**Vehicle status:** Neutron is in development and **has not flown** as of May 2026. First flight targeted Q4 2026 (FAA permit window Jul to Dec 2026), slipped repeatedly from 2024 to 2025 to 2026; a Stage 1 propellant tank ruptured in hydrostatic testing on 21 Jan 2026. Everything about Neutron from Wallops is therefore **design/plan, not demonstrated**.

**Tagging convention:**
- **[FACT]** = flown, documented event, or directly company/agency/operator-stated.
- **[RL-STATED]** = stated by Rocket Lab or the Neutron Payload User's Guide (PUG) for an un-flown vehicle (design value).
- **[ANALOGY]** = another vehicle/site used by inference to inform the Neutron conclusion.
- **[ESTIMATE/DERIVED]** = arithmetic or reasoning performed here; not an official figure.

---

## Summary / key-spec table

| Question | Finding | Confidence |
|---|---|---|
| **Is LC-3 (Pad 0D, MARS, Wallops, Virginia) Neutron's pad?** | **Yes. [FACT]** Rocket Lab opened Launch Complex 3 at Pad 0D, Mid-Atlantic Regional Spaceport (MARS), NASA Wallops Flight Facility, Wallops Island, Virginia; ribbon-cutting **28 Aug 2025**. It is Rocket Lab's dedicated Neutron pad, adjacent to the Electron pad (LC-2 / Pad 0C). | **High** |
| Standard licensed launch corridor at MARS | **~38 to 60 degrees inclination [FACT]** (easterly/northeasterly over the Atlantic). This is the *published, standard* corridor; it does **not** by itself include SSO (~98 deg). | **High** |
| Can SSO (~98 deg) be reached from Virginia *at all*? | **Probable yes, via a southerly Atlantic corridor and/or a dogleg [RL-STATED + ANALOGY].** The Neutron PUG and the spaceport operator both state SSO is *reachable/possible*; the physical mechanism (southerly track + dogleg, enabled by autonomous flight safety) is the same one that reopened polar launches from Cape Canaveral. **But no orbital vehicle has ever actually flown an SSO mission from Wallops** (see precedent below). | **Medium** |
| Flown precedent for SSO from Wallops specifically | **None found. [FACT]** Wallops orbital launches (Scout, Minotaur, Electron, NRO) have flown LEO/mid-inclination (~38 to ~50 deg) or, for LADEE, a high-energy lunar trajectory, **not** a ~98 deg SSO. Minotaur's published SSO numbers are **Vandenberg-only**. | **High (absence of precedent)** |
| Strong off-site analogue | **Falcon 9 SAOCOM 1B [FACT]:** first polar launch from Cape Canaveral in ~50 years (30 Aug 2020), **~98 deg / ~610 km SSO**, 3,050 kg, flown SE down the Florida coast then a **second-stage dogleg south**, booster recovered RTLS to LZ-1. Enabled by **autonomous flight safety + booster flyback**. Directly analogous to a Wallops SSO profile. | **High (for Falcon; analogue for Neutron)** |
| Extra payload penalty of the dogleg/southerly azimuth (vs due-east) | **A real but second-order penalty, ESTIMATE ~5 to 15%** for a moderate-altitude SSO on a modern vehicle with cross-range, **on top of** the inclination/no-Earth-assist effect. Anchors: Saturn-era Cape dogleg "at least 20%" to higher orbits (NASA history, old/vehicle-specific); a ~17% Florida-to-400 km-polar figure for an old Falcon 9 (soft source). | **Low (estimate; bracketed by analogues)** |
| Is the dogleg penalty already inside the project's ~25 to 30% LEO-to-SSO penalty? | **Partially, and it must not be double-counted.** The project's ~25 to 30% SSO penalty was derived from **Vandenberg-style** SSO numbers (clean southerly range, no dogleg). A Wallops dogleg adds an **incremental** azimuth-steering loss **on top of** that. Net working SSO retention from Virginia is therefore at the **low end** of, or slightly below, the established band. | **Medium** |
| Has Rocket Lab stated Neutron SSO capability **from LC-3 / Virginia** specifically? | **Only generically. [RL-STATED]** The Neutron PUG says Neutron from LC-3 "can reach inclination orbits and sun-synchronous orbits (SSO)." Rocket Lab's LC-3 opening release frames LC-3 around LEO, ISS, Moon, Mars, and NSSL national-security missions but does **not** headline an SSO-from-Wallops capability or number. The "sun-synchronous through 30 degrees" marketing line is the **New Zealand (Mahia)** site, **not** Wallops. | **Medium** |
| **BOTTOM LINE: is Virginia an SSO guarantee?** | **Probable-yes-with-a-dogleg, NOT a demonstrated guarantee.** Virginia (LC-3) is very likely SSO-capable via a southerly Atlantic dogleg, on Rocket Lab's own statement and a strong Falcon-9-from-Cape precedent, but it carries (a) **no flown SSO precedent from Wallops**, (b) an **extra ~5 to 15% (est.) dogleg payload penalty on top of** the ~25 to 30% LEO-to-SSO penalty, and (c) **unflown-vehicle risk**. It is an **open risk to confirm with Rocket Lab**, not a settled fact. | **Medium** |

> **One-line answer:** Virginia/LC-3 is Neutron's confirmed pad, and SSO from there is a *probable-yes via a southerly Atlantic dogleg* (Rocket Lab states it; the Falcon-9-from-Cape precedent proves the mechanism), but **there is no flown SSO precedent from Wallops**, and the dogleg adds an **estimated extra ~5 to 15% payload hit on top of** the project's ~25 to 30% LEO-to-SSO penalty. Treat Virginia SSO capability as a **probable-yes-to-confirm**, not a guarantee.

---

## 1. Confirm Neutron's Virginia pad (LC-3, MARS, Wallops)

**Confirmed. [FACT]** Neutron launches from **Launch Complex 3 (LC-3), built at Pad 0D (LP-0D)**, at the **Mid-Atlantic Regional Spaceport (MARS)** on **NASA's Wallops Flight Facility, Wallops Island, Virginia**. It sits next door to Rocket Lab's Electron pad (LC-2 / Pad 0C).

- **Rocket Lab primary source:** Rocket Lab's own announcement, "Rocket Lab Opens Launch Complex 3, A Critical Milestone On The Path To Neutron's First Launch," dates the **ribbon-cutting to 28 Aug 2025** at Wallops Island MARS, Virginia, with CEO Peter Beck calling LC-3 a "symbol of assured access to space" supporting "responsive, high-cadence launches to low Earth orbit, and beyond," and notes Rocket Lab's selection for US Space Force NSSL Phase 3 national-security missions ([Rocket Lab, via Space & Defense mirror, Aug 2025](https://spaceanddefense.io/rocket-lab-opens-launch-complex-3-a-crucial-milestone-on-the-road-to-neutrons-first-launch/); [Rocket Lab press release, BusinessWire, 27 Aug 2025](https://www.businesswire.com/news/home/20250827593085/en/Rocket-Lab-Opens-Launch-Complex-3-A-Critical-Milestone-On-The-Path-To-Neutrons-First-Launch); [Rocket Lab investor release](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-opens-launch-complex-3-critical-milestone-path)). *(The Rocket Lab page itself returned HTTP 403 to automated fetch on 2026-05-29; content here is via the Space & Defense mirror and the BusinessWire/investor copies of the same release.)*
- **Secondary corroboration:** Trade press reported the same LC-3 opening: built at Pad 0D within Wallops, ~700 tons of steel launch mount, Rocket Lab's fourth launch site, engineered for the reusable Neutron, with Virginia Governor Youngkin and Beck at the ceremony ([NASASpaceFlight, Aug 2025](https://www.nasaspaceflight.com/2025/08/rocket-lab-inaugurates-lc-3-wallops/); [CompositesWorld](https://www.compositesworld.com/news/rocket-lab-opens-launch-complex-3-for-neutron-rocket-debut)).
- **Spaceport/encyclopedic confirmation of the pad mapping:** The MARS/Wallops pad list confirms "Launch pad 0D (LP-0D). Rocket Lab will refer to LP-0D as Launch Complex 3 or LC-3," for Neutron ([Mid-Atlantic Regional Spaceport, Wikipedia](https://en.wikipedia.org/wiki/Mid-Atlantic_Regional_Spaceport)).

**Status / date flags:** LC-3 is built and was inaugurated 28 Aug 2025, but **Neutron has not flown**. First flight is targeted Q4 2026 (slipped from 2024 to 2025 to 2026); the Jan 2026 Stage 1 tank rupture added risk. *(Note: the project doc `sso_recovery_cadence_falcon_analogue.md` cites a "Pad 0D ready 2 Sep 2025" date; the public ribbon-cutting was 28 Aug 2025. Both are 2025; treat the late-Aug/early-Sep 2025 window as the pad-ready milestone.)*

---

## 2. Can SSO (~98 degrees) be reached from Wallops, Virginia?

This is the crux. The honest answer has three layers: (a) the **standard** corridor does not include SSO; (b) Rocket Lab and the spaceport operator **state** SSO is reachable; (c) there is **no flown SSO precedent from Wallops**, but there is a strong off-site analogue.

### 2.1 The standard MARS corridor is mid-inclination (38 to 60 degrees) [FACT]
MARS is "approved for launch azimuths from **38 to 60 degrees**," ideal for ISS-class inclinations, and is described as one of the East Coast orbital sites "with launch trajectories to achieve orbital inclinations between approximately **38 degrees and 60 degrees**" ([Mid-Atlantic Regional Spaceport, Wikipedia](https://en.wikipedia.org/wiki/Mid-Atlantic_Regional_Spaceport); [Virginia Spaceport Authority, Facilities](https://www.vaspace.org/our-facilities)). The conventional division of US ranges puts **mid/low inclination at Wallops and the Cape**, and **polar/SSO at Vandenberg and Kodiak/Alaska**: a Virginia-state spaceport overview states plainly that "the Pacific Spaceport Complex in Alaska focuses on launches into polar and high-inclination orbits, while the Mid-Atlantic Regional Spaceport targets launches into equatorial, low-inclination, and mid-inclination orbits" ([VirginiaPlaces, Wallops/space](http://www.virginiaplaces.org/transportation/space.html); [FAA, Spaceports by State](https://www.faa.gov/space/spaceports_by_state)). So **SSO is outside the standard Wallops product.**

### 2.2 The operator and Rocket Lab say SSO is possible from MARS [RL-STATED / operator-stated]
- **Spaceport operator:** The Virginia Spaceport Authority states "MARS **also has the potential to support sun-synchronous orbit missions** to satisfy key requirements for science and imagery missions, such as global coverage of nearly all latitudes" ([Virginia Spaceport Authority, Facilities](https://www.vaspace.org/our-facilities)). This is a "potential," not a flown capability, and is stated by the site operator.
- **Rocket Lab PUG:** The Neutron Payload User's Guide (v1.0, Jan 2025) states Neutron from LC-3 "can reach inclination orbits and sun-synchronous orbits (SSO)" ([Neutron PUG v1.0, PDF](https://rocketlabcorp.com/assets/Uploads/Rocket-Lab-Neutron-PUG-reduced-final.pdf); as extracted in prior project research; the PDF returned 403 to automated fetch on 2026-05-29).

### 2.3 The mechanism: southerly Atlantic corridor + dogleg, enabled by autonomous flight safety [ANALOGY]
SSO from an East Coast site is reached the way Cape Canaveral reopened polar launches: fly **southeast over open ocean, then dogleg south** after staging to reach the retrograde inclination while avoiding land overflight. The key enabler is the **Autonomous Flight Safety System (AFSS)**, which allows safe command-destruct on a southerly heading where ground tracking faces signal attenuation. FAA's Wayne Monteith named the two enablers explicitly for the Cape's first polar mission: "No. 1, booster flyback, and No. 2, even more important, is autonomous flight safety" ([Spaceflight Now, Aug 2020](https://spaceflightnow.com/2020/08/31/spacex-launches-first-polar-orbit-mission-from-florida-in-decades/)). **Wallops itself pioneered autonomous flight termination (NAFTU)**, which is what first enabled Rocket Lab's Electron to fly from Wallops ([NASA, NAFTU](https://www.nasa.gov/centers-and-facilities/wallops/new-nasa-safety-system-enables-rocket-lab-launch-from-wallops/)), so the enabling technology is already resident at the Virginia range.

### 2.4 Precedent: SSO has NOT been flown from Wallops; mid-inclination and lunar have [FACT]
This is the load-bearing caveat. **No orbital vehicle has flown a ~97 to 98 degree SSO mission from Wallops.** What Wallops *has* flown:
- **Minotaur NRO missions** at roughly **mid-inclination**: NROL-111 (Minotaur I, 15 Jun 2021) targeted an orbit "at an inclination of about **50 degrees**," within the standard corridor ([Spaceflight Now, Jun 2021](https://spaceflightnow.com/2021/06/14/minotaur-rocket-set-to-launch-top-secret-satellites-from-virginia/); [AmericaSpace, Jun 2021](https://www.americaspace.com/2021/06/15/minotaur-i-booster-launches-secretive-nrol-111-payload-from-wallops/)). Minotaur's published **SSO** payload (~310 kg to a 740 km SSO) is quoted **only for Vandenberg**, not Wallops ([Minotaur (rocket family), Wikipedia](https://en.wikipedia.org/wiki/Minotaur_(rocket_family))).
- **LADEE** (Minotaur V, 7 Sep 2013) flew a **highly elliptical lunar-phasing trajectory** from MARS Pad 0B, not an SSO, but it demonstrates Wallops can fly **high-energy, non-due-east** trajectories ([Minotaur (rocket family), Wikipedia](https://en.wikipedia.org/wiki/Minotaur_(rocket_family)); [NASA, Minotaur V at Wallops](https://www.nasa.gov/image-article/minotaur-v-nasa-wallops/)).
- **Scout** and **Electron** flights from Wallops have been LEO/mid-inclination science and smallsat missions; no Wallops SSO is documented ([Scout, Astronautix](http://www.astronautix.com/s/scout.html); [Wallops Flight Facility, Wikipedia](https://en.wikipedia.org/wiki/Wallops_Flight_Facility)).

**The strong analogue is off-site:** Falcon 9 **SAOCOM 1B** was the first polar launch from Cape Canaveral in ~50 years (30 Aug 2020), into a **~98 degree / ~610 km SSO**, flying SE down the Florida coast then a **second-stage dogleg south**, with the booster recovered RTLS to LZ-1 ([Spaceflight Now, Aug 2020](https://spaceflightnow.com/2020/08/31/spacex-launches-first-polar-orbit-mission-from-florida-in-decades/); [SAOCOM, Wikipedia](https://en.wikipedia.org/wiki/SAOCOM)). By 2025 SpaceX had flown 11+ polar missions on this corridor. This is the existence proof that a US **East Coast** site can deliver SSO via a southerly dogleg, which is exactly the Wallops mechanism, but it is a **different site and vehicle**.

**Conclusion for Q2:** SSO from Virginia is **physically reachable and stated-reachable**, with a clear mechanism (southerly Atlantic dogleg + AFSS) and a strong East-Coast precedent (SAOCOM 1B), but it is **unproven at Wallops specifically** and **unflown for Neutron**.

---

## 3. Quantify the payload penalty of the dogleg / southerly azimuth (vs due-east)

There are **two distinct penalties**, and the project must not conflate them.

### 3.1 Two separate effects
1. **The inclination / no-Earth-rotation-assist penalty (the "SSO penalty").** A due-east launch from Wallops (~37.8 deg N) gains ~+0.3 to 0.4 km/s from Earth's eastward rotation; a ~98 deg SSO is slightly retrograde, so the vehicle forgoes that assist and partly fights it (~0.5 to 0.8 km/s extra Delta-v), plus typically targets 500 to 700 km rather than minimal LEO. This is the effect already captured in the project's **~25 to 30% LEO-to-SSO penalty** (`neutron_payload_vs_orbit.md`, `payload_and_block_upgrade.md`). It exists **even from a clean polar range like Vandenberg**, where no dogleg is needed.
2. **The dogleg / azimuth-steering penalty (the *extra* Wallops/Cape effect).** To avoid land overflight, an East Coast vehicle cannot fly the straight-line minimum-energy azimuth to SSO; it must steer (dogleg). Steering off the optimal azimuth wastes Delta-v and **costs additional payload beyond** the inclination penalty. Vandenberg's open Pacific range needs **no** dogleg, "does not require rockets to make an in-flight turn," which is precisely why it is preferred for heavy polar/SSO ([Vandenberg Space Launch Complex 6, Wikipedia](https://en.wikipedia.org/wiki/Vandenberg_Space_Launch_Complex_6); search synthesis on Cape-vs-Vandenberg dogleg). This is the penalty unique to going SSO **from Virginia** rather than from Vandenberg.

### 3.2 Magnitude of the dogleg penalty (ESTIMATE, bracketed by analogues)
There is **no cleanly published single percentage** for a modern medium-lift dogleg-to-SSO from the East Coast; primary sources discuss it qualitatively. The available numeric anchors (all flagged):
- **Saturn-era, Cape Canaveral [FACT, but old/vehicle-specific]:** "doglegging a Saturn vehicle into a low-altitude equatorial orbit from Cape Canaveral used enough extra propellant to reduce the payload by as much as **80%**. In higher orbits, the penalty was less severe but still involved at least a **20%** loss of payload" ([NASA History, Moonport SP-4204](https://www.hq.nasa.gov/office/pao/History/SP-4204/ch1-2.html)). This is an extreme, large-plane-change, 1960s case and is an **upper bound**, not representative of a modern optimized SSO dogleg.
- **Falcon 9 to 400 km polar from Florida [SOFT SOURCE]:** "launching into a 400 km polar orbit decreases payload mass of an old version of Falcon 9 by about **17 percent** compared to a 'regular' orbit" (Quora answer; **low source quality, flagged**). Note this ~17% figure appears to **bundle** the inclination penalty *and* the dogleg together (it is measured against a "regular," i.e. easterly, orbit), so it is not a clean isolation of the dogleg alone.
- **Modern medium-lift, optimized SSO dogleg [ESTIMATE/DERIVED]:** Modern vehicles fly an efficient SE-then-dogleg profile and have cross-range margin, so the **incremental** dogleg cost (over and above the inclination penalty) is far below the Saturn extreme. A defensible working estimate is **~5 to 15%** additional payload loss attributable to the dogleg/azimuth steering for a moderate-altitude SSO. **This is an analyst estimate, not an official figure**, bracketed below the Saturn-era "at least 20%" and consistent with the dogleg being the reason Vandenberg is still preferred for the heaviest polar payloads.

**Neutron-specific mitigant [RL-STATED]:** Peter Beck states Neutron has "**more cross range capability**" than other vehicles and that "because Neutron's structure is so light, less dV is needed to return to the launch site" ([Everyday Astronaut, Beck interview](https://everydayastronaut.com/neutron-update-interview-with-peter-beck/)). High cross-range is exactly the property that **reduces** the dogleg penalty (the vehicle can steer more cheaply). This argues for the **low end** of the ~5 to 15% band, but it is a qualitative claim on an unflown vehicle, not a quantified SSO-from-Wallops figure.

### 3.3 Is the dogleg penalty ON TOP of the ~25 to 30% LEO-to-SSO penalty, or already included?
**It is largely ON TOP, and must be added (not double-counted).** The project's ~25 to 30% LEO-to-SSO penalty was derived from a **~65 to 80% LEO-to-SSO retention factor borrowed from comparable medium-lift vehicles** whose SSO numbers are typically quoted for **Vandenberg-style clean southerly ranges with no dogleg** (`payload_and_block_upgrade.md` §2). That band therefore captures the **inclination/no-Earth-assist** effect but **not** a Wallops/Cape dogleg.

So the correct stack for a **Virginia** SSO mission is approximately:

> due-east LEO mass × (LEO-to-SSO retention, ~0.70 to 0.75) × (dogleg retention, ~0.85 to 0.95, ESTIMATE) = Virginia-SSO mass.

**Practical implication [ESTIMATE]:** the project's working **~9,500 kg reusable (DRL) to SSO** is best read, for **Virginia specifically**, as sitting at the **low end** of its 8,500 to 10,500 kg band, or modestly below it (order **~8,000 to 9,500 kg**), once a Wallops dogleg is included, with Neutron's claimed cross-range pulling it back toward the higher side. This does **not** force expendable (the recovery analysis in `sso_recovery_cadence_falcon_analogue.md` stands), it just further trims the SSO mass budget. **Confidence: Low to Medium**, this is an estimate-on-an-estimate and the single biggest reason to obtain a Wallops-specific SSO performance curve from Rocket Lab.

---

## 4. Has Rocket Lab specifically stated Neutron SSO capability from LC-3 / Virginia?

**Only generically, via the PUG; not as a headline LC-3 capability or number. [RL-STATED]**
- **Yes, generically:** The Neutron PUG (v1.0, Jan 2025) states Neutron from LC-3 "can reach inclination orbits and sun-synchronous orbits (SSO)" ([Neutron PUG v1.0, PDF](https://rocketlabcorp.com/assets/Uploads/Rocket-Lab-Neutron-PUG-reduced-final.pdf), via prior project extraction; 403 on direct fetch).
- **Not in the LC-3 opening messaging:** Rocket Lab's LC-3 opening release frames the pad around "low Earth orbit, and beyond," ISS/Moon/Mars, and NSSL national-security missions, and does **not** headline an SSO-from-Wallops capability, azimuth, or payload number ([Rocket Lab via Space & Defense](https://spaceanddefense.io/rocket-lab-opens-launch-complex-3-a-crucial-milestone-on-the-road-to-neutrons-first-launch/)).
- **Do NOT misattribute the "30 degrees" line:** Rocket Lab's "sun-synchronous through to 30 degrees" marketing applies to its **New Zealand (Mahia)** site, not Wallops ([Rocket Lab Launch Sites guide, Saphiric Studios](https://saphiricstudios.com/blog/rocket-lab-launch-sites-a)). The Wallops Electron corridor is the 38 to 60 deg corridor; the New Zealand SSO claim is irrelevant to the Virginia question.

So Rocket Lab asserts SSO reachability from LC-3 in the PUG, but has **not** published a Wallops SSO **payload number** and has not made SSO-from-Virginia a marketed headline. The strongest public US-soil-relevant signal is actually the **NSSL Phase 3 / national-security** selection, which presumes the ability to serve the high-inclination/SSO orbits those missions often require, but that is an inference, not an explicit Wallops SSO statement.

---

## 5. BOTTOM LINE: is Virginia an SSO guarantee for Neutron?

**Verdict: PROBABLE-YES-WITH-A-DOGLEG. Not a demonstrated guarantee; an open risk to confirm.**

- **In favor (why it is probable):** (1) LC-3/Virginia is **confirmed** as Neutron's pad [FACT]. (2) Rocket Lab's PUG and the spaceport operator both **state SSO is reachable** from MARS [RL-STATED / operator-stated]. (3) The **mechanism is proven on the US East Coast**: Falcon 9 SAOCOM 1B flew a ~98 deg SSO from Cape Canaveral via a southerly dogleg, enabled by autonomous flight safety + booster flyback [FACT, analogue], and the enabling AFSS tech already lives at Wallops [FACT]. (4) Neutron's claimed **high cross-range** specifically eases doglegs [RL-STATED].
- **Against (why it is not a guarantee):** (1) **No orbital vehicle has ever flown an SSO from Wallops** [FACT]; Wallops heritage is 38 to ~50 deg plus one lunar trajectory. (2) The standard licensed corridor is **38 to 60 deg**, with SSO described only as a "potential." (3) **Neutron has not flown at all** (first flight Q4 2026 target, repeatedly slipped). (4) A southerly SSO from Virginia carries an **extra dogleg payload penalty (est. ~5 to 15%) on top of** the ~25 to 30% LEO-to-SSO penalty, trimming the SSO mass budget toward the low end (~8,000 to 9,500 kg DRL, estimate).
- **Net:** For US-soil/military payloads, **Virginia is very likely SSO-capable, but the project should carry it as a probable-yes-to-confirm, not a settled guarantee**, and should budget SSO mass at the **conservative (low) end** of the established band to absorb the dogleg. The two confirmations to obtain from Rocket Lab are (a) an explicit **Wallops/LC-3 SSO performance curve/number**, and (b) confirmation of the **southerly corridor / range-safety approval and any dogleg payload cost** for a ~98 deg insertion from Pad 0D.

**Overall confidence: Medium.** The site and the mechanism are well-sourced; the SSO-from-Wallops capability is stated-but-unflown, and the extra payload penalty is an estimate.

---

## Sources

**Neutron's Virginia pad (LC-3 / Pad 0D / MARS / Wallops):**
- [Rocket Lab Opens Launch Complex 3 (Rocket Lab release, via Space & Defense mirror, Aug 2025)](https://spaceanddefense.io/rocket-lab-opens-launch-complex-3-a-crucial-milestone-on-the-road-to-neutrons-first-launch/) - LC-3 at Wallops MARS Virginia; ribbon-cutting 28 Aug 2025; Beck "assured access to space"; NSSL Phase 3
- [Rocket Lab Opens Launch Complex 3 (BusinessWire, 27 Aug 2025)](https://www.businesswire.com/news/home/20250827593085/en/Rocket-Lab-Opens-Launch-Complex-3-A-Critical-Milestone-On-The-Path-To-Neutrons-First-Launch) - Rocket Lab primary release (wire copy)
- [Rocket Lab Opens Launch Complex 3 (Rocket Lab Investor Relations)](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-opens-launch-complex-3-critical-milestone-path) - Rocket Lab primary release (investor copy)
- [Rocket Lab inaugurates LC-3 at Wallops (NASASpaceFlight, Aug 2025)](https://www.nasaspaceflight.com/2025/08/rocket-lab-inaugurates-lc-3-wallops/) - Pad 0D, 700-ton mount, fourth launch site, Youngkin/Beck ceremony
- [Rocket Lab opens Launch Complex 3 for Neutron rocket debut (CompositesWorld)](https://www.compositesworld.com/news/rocket-lab-opens-launch-complex-3-for-neutron-rocket-debut) - secondary corroboration
- [Mid-Atlantic Regional Spaceport (Wikipedia)](https://en.wikipedia.org/wiki/Mid-Atlantic_Regional_Spaceport) - "LP-0D ... Launch Complex 3 or LC-3" for Neutron; "approved for launch azimuths from 38 to 60 degrees"

**MARS / Wallops corridor and SSO potential:**
- [Virginia Spaceport Authority, Facilities (vaspace.org)](https://www.vaspace.org/our-facilities) - 38 to 60 deg corridor; "MARS also has the potential to support sun-synchronous orbit missions"
- [Space: The Final Frontier Starts at Wallops Island (VirginiaPlaces)](http://www.virginiaplaces.org/transportation/space.html) - Wallops targets equatorial/low/mid-inclination; Alaska/Kodiak for polar/high-inclination
- [Spaceports by State (FAA)](https://www.faa.gov/space/spaceports_by_state) - US spaceport/orbital-launch licensing overview
- [Wallops Flight Facility (Wikipedia)](https://en.wikipedia.org/wiki/Wallops_Flight_Facility) - Wallops orbital launch history (Scout, Explorer IX, LADEE)
- [New NASA Safety System Enables Rocket Lab Launch From Wallops (NASA, NAFTU)](https://www.nasa.gov/centers-and-facilities/wallops/new-nasa-safety-system-enables-rocket-lab-launch-from-wallops/) - autonomous flight termination resident at Wallops

**Precedent: SSO/polar from East Coast, and Wallops mid-inclination/lunar:**
- [SpaceX launches first polar orbit mission from Florida in decades (Spaceflight Now, Aug 2020)](https://spaceflightnow.com/2020/08/31/spacex-launches-first-polar-orbit-mission-from-florida-in-decades/) - SAOCOM 1B ~98 deg / ~610 km, dogleg south, RTLS to LZ-1, 3,050 kg; Monteith "booster flyback + autonomous flight safety"
- [SpaceX Conducts First Polar Launch from Cape in over 50 Years (NASASpaceFlight, Aug 2020)](https://www.nasaspaceflight.com/2020/08/spacex-polar-cape-50-years/) - Cape southerly polar corridor reopening
- [SAOCOM (Wikipedia)](https://en.wikipedia.org/wiki/SAOCOM) - SAOCOM 1B 3,050 kg, SSO ~97.9 deg / 620 km
- [Minotaur (rocket family) (Wikipedia)](https://en.wikipedia.org/wiki/Minotaur_(rocket_family)) - Wallops Minotaur launches LEO/lunar; SSO payload quoted for Vandenberg only; LADEE Minotaur V from Pad 0B
- [Minotaur rocket set to launch top secret satellites from Virginia (Spaceflight Now, Jun 2021)](https://spaceflightnow.com/2021/06/14/minotaur-rocket-set-to-launch-top-secret-satellites-from-virginia/) - NROL-111 ~50 deg inclination from Wallops
- [Minotaur I Booster Launches Secretive NROL-111 Payload from Wallops (AmericaSpace, Jun 2021)](https://www.americaspace.com/2021/06/15/minotaur-i-booster-launches-secretive-nrol-111-payload-from-wallops/) - NROL-111 corroboration
- [Minotaur V at NASA Wallops (NASA)](https://www.nasa.gov/image-article/minotaur-v-nasa-wallops/) - LADEE Minotaur V from Wallops
- [Scout (Astronautix)](http://www.astronautix.com/s/scout.html) - Scout program / Wallops history

**Dogleg / azimuth payload penalty (East Coast vs Vandenberg):**
- [Moonport, NASA History SP-4204, Ch.1-2](https://www.hq.nasa.gov/office/pao/History/SP-4204/ch1-2.html) - Saturn-era Cape dogleg penalty: up to 80% to low equatorial, "at least 20%" to higher orbits
- [Vandenberg Space Launch Complex 6 (Wikipedia)](https://en.wikipedia.org/wiki/Vandenberg_Space_Launch_Complex_6) - Vandenberg open Pacific range, no dogleg required; preferred for polar/SSO
- [How hard is it to orbit a satellite on polar orbit (Quora)](https://www.quora.com/How-hard-is-it-to-orbit-a-satellite-on-polar-orbit-compared-to-the-regular-way) - ~17% Florida-to-400 km-polar figure for an old Falcon 9 (LOW source quality, flagged)
- [Neutron Update, Interview with Peter Beck (Everyday Astronaut)](https://everydayastronaut.com/neutron-update-interview-with-peter-beck/) - Neutron "more cross range capability"; lighter structure, less dV to return

**Rocket Lab SSO statements / site attribution:**
- [Neutron Payload User's Guide v1.0, Jan 2025 (Rocket Lab PDF)](https://rocketlabcorp.com/assets/Uploads/Rocket-Lab-Neutron-PUG-reduced-final.pdf) - "can reach inclination orbits and sun-synchronous orbits (SSO)" (403 on direct fetch; via prior project extraction)
- [Rocket Lab Launch Sites: A Comprehensive Guide (Saphiric Studios)](https://saphiricstudios.com/blog/rocket-lab-launch-sites-a) - "sun-synchronous through to 30 degrees" = New Zealand (Mahia), NOT Wallops; Wallops Electron 38 to 60 deg

**Project docs reconciled (read-only, NOT modified):**
- `research/rocket_lab/neutron/neutron_specs.md`
- `research/rocket_lab/neutron/payload_and_block_upgrade.md`
- `research/rocket_lab/neutron/sso_recovery_cadence_falcon_analogue.md`
- `research/rocket_lab/neutron/neutron_payload_vs_orbit.md`

---

## Open questions / uncertainties

1. **Wallops/LC-3 SSO performance number, the top open item.** Rocket Lab states SSO is *reachable* from LC-3 (PUG) but has published **no Wallops-specific SSO payload figure**. Obtain the LC-3 SSO performance curve from Rocket Lab (launch@rocketlabusa.com or full PUG). This is the single most decision-critical confirmation for the US-soil thesis.
2. **No flown SSO precedent from Wallops.** Every Wallops orbital launch on record is LEO/mid-inclination (~38 to ~50 deg) or a lunar trajectory (LADEE). The SSO-from-Wallops case rests on the PUG statement + the off-site SAOCOM 1B analogue, not on a Wallops demonstration. First Neutron SSO from Virginia would be a first-of-its-kind insertion for the site.
3. **Southerly Atlantic corridor / range-safety approval is not publicly documented for SSO.** The standard MARS approval is 38 to 60 deg. Whether a ~98 deg southerly corridor over the Atlantic from Pad 0D is *already approved* (vs. requiring a new range-safety case) is not public. Confirm with Rocket Lab / Virginia Spaceport Authority / FAA.
4. **Dogleg payload penalty is an estimate.** The ~5 to 15% incremental dogleg loss is an analyst estimate bracketed by a Saturn-era upper bound and a soft Falcon-9 figure; no modern medium-lift East-Coast-to-SSO dogleg percentage is cleanly published. Neutron's claimed cross-range should reduce it, but that is unquantified for SSO. Treat the Virginia SSO mass budget at the low end (~8,000 to 9,500 kg DRL, estimate) until confirmed.
5. **Double-counting risk.** The project's ~25 to 30% LEO-to-SSO penalty derives from Vandenberg-style (no-dogleg) analogues and captures the inclination effect only; the dogleg is incremental and additive. Avoid both (a) ignoring the dogleg and (b) re-applying the full SSO penalty twice.
6. **Everything Neutron is pre-flight.** First flight Q4 2026 (target, slipped 2024 to 2025 to 2026; Jan 2026 tank rupture). First flight expendable; reusable SSO operations realistically NET 2027 to 2028. All Wallops SSO statements are design/plan, not demonstrated.
7. **Primary sources behind 403/paywall.** The Rocket Lab Neutron page, the LC-3 opening release on rocketlabcorp.com, the Neutron PUG PDF, and some NASASpaceFlight/SpaceNews articles returned 403/429 to automated fetch on 2026-05-29; their content here is via wire/mirror copies, search synthesis, and prior project extraction. Re-pull directly before treating the PUG SSO line and any payload number as firm.
