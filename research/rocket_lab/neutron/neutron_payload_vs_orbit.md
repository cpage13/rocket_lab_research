# Neutron, Payload Mass vs. Target Orbit (LEO / SSO-low / SSO-high)

**Research date:** 2026-05-29
**Purpose:** Quantify Rocket Lab Neutron's payload mass as a function of target orbit (LEO reference vs. sun-synchronous orbit at low and high altitude), validate the project's working assumption of a roughly 10 to 20 percent (about 2.5 tonne) payload penalty going to SSO, and quantify how much ADDITIONAL payload is lost going from a baseline SSO (about 500 to 600 km) to a higher SSO (700 to 800 km and above).
**Vehicle status:** In development; **has not flown** as of May 2026. First flight targeted Q4 2026; early flights expendable; reusable downrange (DRL) operations realistically NET 2027.

**Tagging convention used throughout:**
- **[RL-STATED]**, figure published by Rocket Lab or the Neutron Payload User's Guide (PUG). Secondary sources that merely repeat Rocket Lab are cross-checks, not independent validation.
- **[ANALOGY]**, figure or ratio borrowed from a comparable launch vehicle (mainly Falcon 9, plus Electron as an in-family Rocket Lab reference) and applied to Neutron by inference.
- **[DERIVED]**, arithmetic performed in this document from the inputs above it.

> **One-line answer:** The project's "about 2.5 tonne / 10 to 20 percent SSO penalty" is **directionally right but slightly understated** at the headline. The realistic LEO-to-SSO penalty for Neutron's reusable (DRL) mode is closer to **20 to 30 percent (about 3 to 4 tonnes)**, landing the working SSO budget near the project's **~9.5 t**. Going from a baseline SSO (500 to 600 km) up to a high SSO (700 to 800 km) costs only an **additional ~5 to 10 percent (a few hundred kg)**; even out to 1,000 to 1,200 km the extra penalty is only ~10 to 15 percent. **"Halve the payload" for a higher orbit is firmly refuted** by the closest analogue (Falcon 9): the altitude penalty within the SSO band is small.

---

## Summary / key-spec table

### A. Neutron payload by mode and orbit (the numbers the project should use)

| Mode | Payload to **LEO** (low inclination) | Payload to **SSO-low** (~500 to 600 km, ~97 to 98 deg) | Payload to **SSO-high** (~700 to 800 km) | Basis |
|---|---|---|---|---|
| **Expendable** | **15,000 kg** [RL-STATED] | **~10,500 to 11,500 kg** (working ~11,000 kg) [DERIVED/ANALOGY] | **~9,800 to 10,800 kg** [DERIVED/ANALOGY] | LEO stated; SSO derived |
| **Downrange landing (DRL)**, *baseline reusable* | **13,000 kg** [RL-STATED] | **~9,000 to 10,000 kg** (working ~9,500 kg) [DERIVED/ANALOGY] | **~8,400 to 9,400 kg** [DERIVED/ANALOGY] | LEO stated; SSO derived |
| **RTLS (return to launch site)** | **8,500 kg** [RL-STATED] | **~5,500 to 6,800 kg** (working ~6,000 kg) [DERIVED/ANALOGY] | **~5,100 to 6,400 kg** [DERIVED/ANALOGY] | LEO stated; SSO derived |

**Official Rocket Lab anchor that is NOT LEO-only inference:** the Neutron PUG (v1.0, Jan 2025) publishes **500 km polar** values of **6.2 t RTLS / 10.1 t DRL / 11.8 t expendable** [RL-STATED, single-source; see Sources]. Polar (~90 deg) is not identical to SSO (~97 to 98 deg) but is the closest official high-inclination anchor and is the reason the DRL SSO working figure sits near 9.5 t (slightly below the 10.1 t polar value, because true SSO is slightly retrograde and slightly higher-altitude than 500 km polar).

### B. The two headline questions answered

| Question | Project's current assumption | This research | Verdict |
|---|---|---|---|
| **LEO-to-SSO penalty (DRL/reusable)** | "~10 to 20 percent / ~2.5 t" (headline phrasing), with a working ~9.5 t SSO budget already in the deep docs | **~20 to 30 percent / ~3 to 4 t**; working ~9.5 t SSO from a 13 t LEO base | The **9.5 t working figure is sound**; the "10 to 20 percent / 2.5 t" *headline* is on the low side. The deep doc's own ~25 to 35 percent framing is the better one. |
| **Additional penalty SSO-low to SSO-high (600 to 800 km)** | (implicitly small; "12.5 t SSO" block-upgrade case is altitude-agnostic) | **~5 to 10 percent extra (a few hundred kg)** for 600 to 800 km; **~10 to 15 percent** out to 1,000 to 1,200 km | A higher SSO costs **little extra**. **"Halve the payload" is not realistic**; 10 to 30 percent from the SSO baseline is the right envelope, and the true number is at the low end of that. |

---

## 1. Neutron's stated payload (status and as-of dates)

Rocket Lab states **three** LEO numbers, differing only by booster-recovery mode. They appear on Rocket Lab's own Neutron page, in the Neutron PUG v1.0 (Jan 2025), on Wikipedia citing Rocket Lab, and on third-party trackers, and have been repeated by CEO Peter Beck in 2025 to 2026 interviews. Treat them as **[RL-STATED]**, high-confidence, not independently measured:

- **Expendable:** up to **15,000 kg (33,100 lb)** to LEO (booster not recovered).
- **Downrange landing (DRL):** **13,000 kg (28,700 lb)** to LEO (booster lands at sea on the *Return On Investment* platform). **This is the headline/baseline reusable number.**
- **RTLS:** up to **8,500 kg (18,700 lb)** to LEO (booster flies back to Launch Complex 3, Wallops).

**Corroboration (2+ independent secondary sources, all tracing to Rocket Lab):** [Wikipedia, Rocket Lab Neutron](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron) (last updated 20 May 2026): *"up to 15,000 kg (33,100 lb) to LEO while expended, 13,000 kg (28,700 lb) while landing the booster downrange and up to 8,500 kg (18,700 lb) with the first stage returning to the launch site"*; [Rocket Lab, Neutron official page](https://rocketlabcorp.com/launch/neutron/); [NextSpaceflight, Neutron](https://nextspaceflight.com/rockets/284/). **Caveat:** Wikipedia backs these to a single citation, and all secondaries trace to Rocket Lab, so this is best described as a well-repeated **company figure**, not an independently validated one.

**Reference altitude/inclination for "LEO":** Rocket Lab does **not** state the exact altitude/inclination behind the 13/15/8.5 t figures. The PUG language refers to a "typical 500 km circular orbit" for injection accuracy, but the headline LEO mass numbers are not pinned to a stated altitude. This matters: if the LEO figure is quoted at a low/minimum-energy altitude, the real SSO penalty is at the larger end of the band modeled here (see Open questions).

**Status / as-of dates:** Neutron **has not flown** as of May 2026. First flight is **targeted Q4 2026** (FAA permit window Jul to Dec 2026), a date that has slipped from 2024 to 2025 to 2026. A Stage 1 tank **ruptured in hydrostatic testing on 21 Jan 2026**, after which Rocket Lab switched to an automated fiber-placement tank process. All payload numbers are **design/spec values for an un-flown vehicle**. ([Spaceflight Now, Nov 2025 delay](https://spaceflightnow.com/2025/11/11/rocket-lab-delays-debut-of-neutron-rocket-to-2026/); [Space.com, tank rupture](https://www.space.com/space-exploration/rocket-labs-new-neutron-rocket-suffers-fuel-tank-rupture-during-test); [NASASpaceFlight Q1 2026](https://www.nasaspaceflight.com/2026/05/rocket-lab-q1-2026/).)

**The 8,000 kg snippet:** an "8,000 kg to LEO" figure still appears on some trackers (e.g. [Gunter's Space Page](https://space.skyrocket.de/doc_lau/neutron.htm)). This is the **original March 2021 Neutron design figure**, superseded by the Sept 2022 redesign (first stage 7 to 9 Archimedes engines) that raised the baseline to today's 13 t DRL. It is **not** a current LEO or SSO number and must not be used as one.

---

## 2. The SSO penalty, validating the "~2.5 t / 10 to 20 percent" assumption

### 2.1 Rocket Lab has published no Neutron SSO number

The Neutron PUG v1.0 (Jan 2025) states its performance modelling *"accounts for low- through to high-inclination orbits and sun-synchronous orbits (SSO),"* and that Stage 2 supports direct-injection / multi-plane delivery, but it gives **no headline SSO capacity**; customers are directed to request a mission-specific estimate. Repeated targeted searches in May 2026 returned **no official Neutron SSO figure** from any source. ([Neutron PUG v1.0 landing reference](https://rocketlabcorp.com/assets/Uploads/Rocket-Lab-Neutron-PUG-reduced-final.pdf); search corroboration via [SatNow, Neutron](https://www.satnow.com/launch-vehicle-details/neutron).)

The best **[RL-STATED]** anchor is the PUG's **500 km polar** trio: **6.2 t RTLS / 10.1 t DRL / 11.8 t expendable**. (These were extracted from the PUG in prior project research; the PUG PDF currently returns HTTP 403 to automated fetch, so this is **single-source [RL-STATED]** and should be re-pulled directly from the PUG before being treated as firm.)

### 2.2 Why SSO costs payload (physics)

SSO is a near-polar, slightly **retrograde** orbit (inclination ~97 to 98 deg). Two compounding effects reduce payload versus a low-inclination LEO insertion:

1. **Loss of Earth-rotation assist (and then some).** A due-east launch from Wallops (~37.8 deg N) gains roughly **+0.3 to 0.4 km/s** free from Earth's eastward rotation. An SSO launch is slightly retrograde, so it must partly *cancel* that velocity instead of gaining it. The net swing is on the order of **~0.5 to 0.8 km/s of extra delta-v**.
2. **Azimuth/dogleg + altitude.** SSO from Wallops flies a southerly, partly dogleg-constrained azimuth and typically targets **500 to 700 km** rather than a minimal ~200 km LEO, adding orbit-raising delta-v.

### 2.3 The Falcon 9 analogue pins the LEO-to-SSO ratio (the load-bearing cross-check)

Because Neutron publishes no SSO number, the **SpaceX Falcon Payload User's Guide performance table** is the cleanest analogue, and it is **internally self-consistent** (same vehicle, same guide, LEO and SSO both stated), which is exactly what a retention-ratio needs. From that guide's Table 4-3 (Sun-Synchronous Orbit, ~96.3 deg at 200 km) and its LEO table:

| Falcon 9 guide figure | Value | Note |
|---|---|---|
| Max LEO, 200 km, 28.5 deg (Cape Canaveral) | **10,454 kg** | Reference LEO |
| SSO, 200 km, 96.3 deg | **8,351 kg** | Same vehicle/guide |
| **Implied LEO-to-SSO retention at the same 200 km** | **0.80 (20 percent penalty)** | [DERIVED] |

So even at identical low altitude, going from due-east LEO to an SSO inclination costs **~20 percent** of payload for Falcon 9. SSO missions also fly higher (500 to 600 km, not 200 km), which from the same curve removes another ~8 to 10 percent (see §3). **Combined LEO-to-(500 to 600 km SSO) penalty is therefore ~25 to 30 percent**, i.e. a **retention factor of ~0.70 to 0.75**, exactly the band the project's deep docs use.

Two independent extractions of that Falcon 9 SSO table agree on the values (600 km = 7,541 kg, 800 km = 7,162 kg, 1,000 km = 6,807 kg), and the LEO reference (10,454 kg at 200 km) and 200 km SSO (8,351 kg) come from the same guide. Sources: [Falcon 9 User's Guide performance section (Yumpu rendering, pp. 18 and 21)](https://www.yumpu.com/en/document/view/3855656/falcon-9-launch-vehicle-payload-users-guide-spacex/18); [Falcon 9 User's Guide (Spaceflight Now PDF copy)](https://www.spaceflightnow.com/falcon9/001/f9guide.pdf). **[ANALOGY]**, these are *Falcon 9* numbers, used only for their LEO-to-SSO and altitude *ratios*, not their absolute kg.

> **Important caveat on absolute Falcon 9 numbers:** the guide above is an **early (2009-era) Falcon 9** document. Current Falcon 9 Block 5 lifts **>= 22,800 kg expendable / >= 17,400 kg reusable to LEO** at 28.5 deg ([Wikipedia, Falcon 9 Block 5](https://en.wikipedia.org/wiki/Falcon_9_Block_5)). The absolute payloads in the old guide are far below today's vehicle; **only the shape/ratios transfer**, and shape (retention vs. inclination and vs. altitude) is governed by orbital mechanics, not the specific vehicle, so the ratios remain a sound analogy.

### 2.4 Applying the retention band to Neutron

Applying a **~0.70 retention factor (range 0.65 to 0.80)** to each [RL-STATED] LEO figure, cross-checked against the [RL-STATED] 500 km polar trio:

| Mode | LEO [RL-STATED] | 500 km polar [RL-STATED] | LEO-to-SSO factor | **SSO-low estimate** | **Working figure** |
|---|---|---|---|---|---|
| RTLS | 8,500 kg | 6.2 t | 0.65 to 0.80 | ~5,500 to 6,800 kg | ~6,000 kg |
| **DRL (baseline reusable)** | 13,000 kg | 10.1 t | 0.65 to 0.80 | **~8,500 to 10,400 kg** | **~9,500 kg** |
| Expendable | 15,000 kg | 11.8 t | 0.65 to 0.80 | ~9,800 to 12,000 kg | ~11,000 kg |

### 2.5 Verdict on the "~2.5 t / 10 to 20 percent" assumption

- A **10 to 20 percent** penalty corresponds to a retention factor of **0.80 to 0.90**. The Falcon 9 analogue shows that **just the inclination change to SSO already costs ~20 percent at equal altitude**, before adding the 500 to 600 km altitude raise. So **10 to 20 percent is the floor, not the central case**, it understates the true SSO penalty for a Wallops-launched, 500-to-600 km SSO mission.
- In absolute terms, **2.5 t off 13 t is a 19 percent penalty** (yielding 10.5 t). The more defensible central penalty is **~25 to 30 percent (~3.5 t)**, yielding **~9.5 t**, which is precisely the project's deep-doc working figure.
- **Reconciliation:** the project is internally inconsistent only at the *headline* level. The headline "~10 to 20 percent / ~2.5 t" is optimistic; the deep docs (`payload_and_block_upgrade.md`) already use the better ~25 to 35 percent / ~9.5 t framing. **Recommendation: retire the "10 to 20 percent / 2.5 t" headline phrasing and standardize on ~9.5 t reusable-to-SSO (range 8.5 to 10.5 t), a ~25 to 30 percent penalty.** The 12.5 t "SSO" figure that appears in the cost doc corresponds to **expendable mode or a block-upgraded Neutron**, not baseline reusable DRL-to-SSO, and should be labeled as such wherever it is used.

---

## 3. Additional payload lost going to a HIGHER SSO (the altitude-only penalty)

This is the cleanest result in the whole analysis, because the Falcon 9 guide gives a continuous SSO payload-vs-altitude table for **one vehicle on one chart**, so the altitude penalty is isolated from everything else.

### 3.1 Falcon 9 SSO payload vs. circular altitude (Table 4-3, ~96 to 98 deg) [ANALOGY]

| Altitude (km) | Payload (kg) | Retention vs. 600 km | Retention vs. 200 km |
|---|---|---|---|
| 200 | 8,351 | 1.11 | 1.00 |
| 400 | 7,949 | 1.05 | 0.95 |
| **600** (SSO-low ref) | **7,541** | **1.00** | 0.90 |
| 700 | 7,348 | 0.97 | 0.88 |
| **800** (SSO-high) | **7,162** | **0.95** | 0.86 |
| 1,000 | 6,807 | 0.90 | 0.82 |
| 1,200 | 6,476 | 0.86 | 0.78 |

Source (two independent extractions agreeing): [Falcon 9 User's Guide, Table 4-3 (Yumpu p. 21)](https://www.yumpu.com/en/document/view/3855656/falcon-9-launch-vehicle-payload-users-guide-spacex/18) and the same table referenced via [Falcon 9 User's Guide PDF (Spaceflight Now)](https://www.spaceflightnow.com/falcon9/001/f9guide.pdf).

### 3.2 The additional penalty is small [DERIVED]

Taking **600 km as the SSO-low baseline**:
- **600 -> 700 km:** lose ~3 percent.
- **600 -> 800 km (the "higher SSO" the question asks about):** lose **~5 percent** (7,541 to 7,162 kg).
- **600 -> 1,000 km:** lose **~10 percent**.
- **600 -> 1,200 km:** lose **~14 percent**.

Even taking a **500 km** baseline (slightly higher payload than 600 km, by interpolation ~7,750 kg), the 500 -> 800 km step is on the order of **~7 to 8 percent**.

### 3.3 Translating to Neutron [DERIVED/ANALOGY]

Applying the same altitude-retention multipliers to Neutron's DRL SSO-low working figure of **~9,500 kg**:

| Neutron DRL to SSO | Altitude | Payload (working) | vs. SSO-low |
|---|---|---|---|
| SSO-low | ~500 to 600 km | **~9,500 kg** | baseline |
| SSO-mid | ~700 km | ~9,200 kg | -3 percent |
| **SSO-high** | **~800 km** | **~9,000 kg** | **-5 percent** |
| SSO-very-high | ~1,000 km | ~8,500 kg | -10 percent |
| SSO-extreme | ~1,200 km | ~8,150 kg | -14 percent |

> **Net:** moving the data-center node from a 500 to 600 km SSO up to a 700 to 800 km SSO costs Neutron only a **few hundred kg (~5 percent)** of payload, not a tonne. This is small relative to the ~1 to 2 t uncertainty already in the SSO baseline itself, so **altitude within the operational SSO band is a second-order effect** for the node-mass budget.

### 3.4 In-family sanity check (Electron) [ANALOGY]

Rocket Lab's own Electron is quoted at **200 kg to 500 km SSO** and **up to 300 kg to "lower orbits" (LEO)**. That is a **~33 percent** LEO-to-500km-SSO gap on a small launcher (combining inclination + altitude), consistent with the ~25 to 35 percent band used for Neutron above, and confirms Rocket Lab vehicles follow the same LEO > SSO ordering. ([Rocket Lab on X, Aug 2020](https://x.com/RocketLab/status/1290680251916288000); [Rocket Lab, Increases Electron Payload Capacity](https://rocketlabcorp.com/updates/rocket-lab-increases-electron-payload-capacity-enabling-interplanetary-missions-and-reusability/).) Electron does not publish a fine-grained altitude curve, so it supports the LEO-to-SSO ratio but not the SSO-altitude slope; the Falcon 9 table carries the altitude-slope conclusion.

---

## 4. Is a "halve the payload" outcome plausible for a much higher orbit?

**No.** A 50 percent payload loss is not consistent with any analogue for a *circular SSO* altitude raise:

- The Falcon 9 guide shows only a **~22 percent** loss going from a 200 km SSO all the way to a **1,200 km** SSO, and only **~5 percent** for the realistic 600 -> 800 km step. To lose 50 percent you would have to go far beyond SSO altitudes (toward MEO/GTO-class energies), which is a different mission class entirely.
- A **halving** is the right mental model for a *mode* change (e.g. Neutron expendable 15 t -> RTLS 8.5 t is a 43 percent drop) or for a **GTO/escape** trajectory (GTO typically costs 40 to 60 percent vs. LEO), **not** for nudging a circular SSO from 600 to 800 km.
- **Realistic envelope for "higher SSO":** **~5 to 15 percent** below the SSO-low baseline across 700 to 1,200 km. The "10 to 30 percent from the SSO baseline" envelope in the question is a safe upper bound; the true number sits at its **low end (~5 to 10 percent)** for the 700 to 800 km orbits most relevant to a data-center node.

The binding constraint on the node-mass budget is therefore the **LEO-to-SSO inclination penalty (~25 to 30 percent, still un-confirmed by Rocket Lab)**, *not* the choice of SSO altitude within a sensible operating band.

---

## Sources

**Rocket Lab / Neutron (primary and primary-tracing):**
- [Rocket Lab, Neutron official page](https://rocketlabcorp.com/launch/neutron/), 13 / 15 / 8.5 t LEO by mode [RL-STATED]
- [Neutron Payload User's Guide v1.0, Jan 2025 (PDF; returns 403 to automated fetch as of 2026-05-29)](https://rocketlabcorp.com/assets/Uploads/Rocket-Lab-Neutron-PUG-reduced-final.pdf), SSO modelled but no headline SSO number; 500 km polar 6.2 / 10.1 / 11.8 t [RL-STATED, single-source]
- [Rocket Lab Neutron, Wikipedia (updated 20 May 2026)](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron), repeats 13 / 15 / 8.5 t (single citation, traces to Rocket Lab)
- [Neutron, NextSpaceflight](https://nextspaceflight.com/rockets/284/), repeats LEO figures, Q4 2026 first flight
- [Neutron Rocket / Launch Vehicle Details, SatNow](https://www.satnow.com/launch-vehicle-details/neutron), secondary spec summary
- [Neutron, Gunter's Space Page](https://space.skyrocket.de/doc_lau/neutron.htm), shows the **superseded 2021 design 8,000 kg LEO**; do not use as current
- [Rocket Lab delays debut of Neutron rocket to 2026, Spaceflight Now (Nov 2025)](https://spaceflightnow.com/2025/11/11/rocket-lab-delays-debut-of-neutron-rocket-to-2026/), schedule/status
- [Rocket Lab's new Neutron rocket suffers fuel tank rupture during test, Space.com](https://www.space.com/space-exploration/rocket-labs-new-neutron-rocket-suffers-fuel-tank-rupture-during-test), Jan 2026 tank rupture
- [Rocket Lab Q1 2026 update, NASASpaceFlight (May 2026)](https://www.nasaspaceflight.com/2026/05/rocket-lab-q1-2026/), status as of May 2026

**Falcon 9 analogue (LEO-to-SSO ratio + SSO-vs-altitude curve):**
- [Falcon 9 Launch Vehicle Payload User's Guide (Spaceflight Now copy, PDF)](https://www.spaceflightnow.com/falcon9/001/f9guide.pdf), Table 4-3 SSO performance; LEO reference [ANALOGY]
- [Falcon 9 User's Guide performance section, pp. 18 and 21 (Yumpu rendering)](https://www.yumpu.com/en/document/view/3855656/falcon-9-launch-vehicle-payload-users-guide-spacex/18), SSO 200 km 8,351 kg; 600 km 7,541; 700 km 7,348; 800 km 7,162; 1,000 km 6,807; 1,200 km 6,476; LEO 10,454 kg at 200 km/28.5 deg
- [Falcon 9 Block 5, Wikipedia](https://en.wikipedia.org/wiki/Falcon_9_Block_5), current Block 5: >=22,800 kg expendable / >=17,400 kg reusable to LEO (shows the 2009-guide absolutes are low; ratios still valid)
- [Falcon 9, Wikipedia](https://en.wikipedia.org/wiki/Falcon_9), general Falcon 9 reference
- [SpaceX Falcon Payload User's Guide (2021, MIT-hosted PDF)](https://web.mit.edu/2.70/Reading%20Materials/SpaceX%20Falcon-users-guide-2021-09.pdf), current guide (SSO shown as a graph; not text-extractable)

**Electron in-family analogue:**
- [Rocket Lab on X, Electron 150->200 kg SSO, 225->300 kg LEO (Aug 2020)](https://x.com/RocketLab/status/1290680251916288000)
- [Rocket Lab Increases Electron Payload Capacity, Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-increases-electron-payload-capacity-enabling-interplanetary-missions-and-reusability/)

**Project docs reconciled (read-only, not modified):**
- `research/rocket_lab/neutron/neutron_specs.md`
- `research/rocket_lab/neutron/payload_and_block_upgrade.md`
- `research/rocket_lab/neutron/launch_cost_economics.md`

---

## Open questions / uncertainties

1. **Neutron SSO payload mass, still UNRESOLVED (highest priority).** No official Rocket Lab SSO figure exists. The ~9,500 kg DRL working figure (range 8,500 to 10,500 kg) is inference from a ~0.65 to 0.80 LEO-to-SSO retention factor, cross-checked against the [RL-STATED] 500 km polar 10.1 t DRL proxy. Must be confirmed via Rocket Lab's mission-specific performance estimate or the full PUG performance curves.
2. **PUG 500 km polar trio is single-source and was not re-verifiable this session.** The 6.2 / 10.1 / 11.8 t figures come from prior project extraction of the PUG; the PUG PDF returned HTTP 403 to automated fetch on 2026-05-29. Re-pull directly from the PUG (or request from Rocket Lab) before treating as firm.
3. **Reference altitude/inclination for Neutron's "LEO" numbers is unstated.** If 13 t DRL is quoted at a very low/minimum-energy altitude, the real LEO-to-SSO penalty is at the larger (≈30 percent) end of the band, pushing the SSO budget toward 9 t rather than 10 t.
4. **The SSO-altitude slope is an [ANALOGY] from Falcon 9, not Neutron.** The ~5 percent (600 to 800 km) and ~10 to 14 percent (to 1,000 to 1,200 km) additional penalties are governed mainly by orbital mechanics and should transfer well, but Neutron's exact Stage 2 sizing could shift the slope modestly. Rocket Lab has published no Neutron payload-vs-altitude curve.
5. **Falcon 9 guide vintage.** The SSO-vs-altitude table is from an early (2009-era) Falcon 9 guide; current Block 5 absolutes are far higher. Only the *ratios* are used here; the SpaceX current guide (2021/2025) presents SSO as a graph that did not text-extract, so the early guide's tabulated values are the usable quantitative source.
6. **Headline-vs-deep-doc inconsistency in the project.** The "~10 to 20 percent / 2.5 t" SSO phrasing (headline) is optimistic versus this research's ~25 to 30 percent central; the deep doc's ~9.5 t / 25 to 35 percent framing is the one to standardize on. The 12.5 t "SSO" figure in the cost doc is an expendable / block-upgrade value, not baseline reusable DRL-to-SSO.
7. **All figures are pre-first-flight.** Neutron has not flown (first flight targeted Q4 2026, slipped repeatedly; Jan 2026 tank rupture). Real payload-vs-orbit data will not exist until reusable DRL operations mature, realistically 2027 to 2028.
