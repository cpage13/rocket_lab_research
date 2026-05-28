# Rocket Lab Neutron — Launch Vehicle Research

**Research date:** 2026-05-17
**Purpose:** Feasibility input for launching AI-inference data-center hardware (dense compute racks) to orbit, with emphasis on **sun-synchronous orbit (SSO)** delivery.
**Status of vehicle:** In development; **has not flown** as of May 2026. First flight targeted Q4 2026.

---

## Summary table — key specs

| Parameter | Value | Configuration / notes | Confidence |
|---|---|---|---|
| Payload to LEO — expendable | **~15,000 kg (33,100 lb)** | No booster recovery | High (official RL, confirmed by Wikipedia) |
| Payload to LEO — downrange landing (DRL) | **13,000 kg (28,700 lb)** | Booster lands at sea; **the headline/baseline figure** | High (official RL) |
| Payload to LEO — return to launch site (RTLS) | **~8,500 kg (18,700 lb)** | Booster flies back to Wallops/LC-3 | High (official RL) |
| Payload to **SSO** | **Not officially published as a single number** | See "Payload capacity" section — estimate only | **Low** |
| Fairing — height | **~14 m** ("Hungry Hippo" fairing) | Official RL (X post, Jan 2026) | High |
| Fairing — payload diameter accommodation | **up to 5.5 m** | Per Neutron Payload User's Guide v1.0 (Jan 2025) | Medium–High |
| Fairing — usable payload **volume** | **Not officially published** | See "Fairing" section; rough estimate ~150–230 m³ | **Low (estimate)** |
| Rocket height | **~43 m** (some early sources said 40 m) | Wikipedia / RL | Medium–High |
| Rocket base diameter | **7 m** | Tapers toward fairing | High |
| Liftoff mass | **~480,000 kg** | RL spec page | Medium |
| Stages | **2** (partially reusable) | Stage 1 reusable; Stage 2 expendable | High |
| First-stage engines | **9 × Archimedes** (sea-level) | "Octal-plus-one" layout | High |
| Second-stage engine | **1 × Archimedes** (vacuum-optimized) | 890 kN / ~200,000 lbf | High |
| Liftoff thrust | **~6,610 kN (1,485,000 lbf)** | Sum of 9 engines | High |
| Propellant | **LOX / liquid methane (methalox)** | Oxidizer-rich staged combustion | High |
| Target launch price | **~$50–55 M per launch** | Company target (2023); not a published list price | Medium (company guidance) |
| First flight | **Q4 2026 (targeted)** | FAA permit window Jul–Dec 2026 | Medium (schedule has slipped repeatedly) |

> **Bottom line for the data-center thesis:** Neutron is a **Falcon-9-class medium-lift** vehicle. Baseline (reusable) capacity is **13 t to LEO**. SSO capacity is **not published** and should be treated as materially lower than LEO (high-inclination retrograde launches lose performance). The two most decision-critical numbers for rack-dense cargo — **SSO payload mass** and **usable fairing volume** — are **both undisclosed by Rocket Lab** and are the largest uncertainties in this research.

> **Source status (2026-05-25):** See [SOURCE_INDEX.md](../../SOURCE_INDEX.md) claim IDs NTR-001 through NTR-011. The LEO/polar payload values are Rocket Lab/PUG values; the SSO payload is still a working estimate. Secondary sources that repeat Rocket Lab do not make the Rocket Lab figures independently validated. The RTLS LEO value has a minor source split (8.5 t in the PUG vs. 8.0 t on another Rocket Lab page), so cite the PUG when using 8.5 t.

> **Cross-reference (wave-5, 2026-05-17):** the dedicated deep-verification doc
> `rocket_lab/neutron/payload_and_block_upgrade.md` (research item 23)
> **supersedes this doc on SSO performance.** It adopts a working
> **~9.5 t reusable-to-SSO** (range 8.5–10.5 t), ~11 t expendable-to-SSO, and a
> credible block upgrade reaching ~12–13 t reusable-to-SSO — refining the
> "~8–10 t estimate" used below. It also **resolves this doc's Open Question #5**:
> the "8,000 kg to LEO" snippet was the *original 2021 Neutron design figure*,
> not an error and not a garbled SSO number. Treat item 23 as the authoritative
> SSO source; the SSO discussion below is retained as the original derivation.

---

## 1. Payload capacity

### LEO (official Rocket Lab figures, corroborated)
Rocket Lab states three LEO numbers depending on recovery mode:

- **Expendable:** up to **15,000 kg (33,100 lb)** — no booster recovery.
- **Downrange landing (DRL):** **13,000 kg (28,700 lb)** — booster lands at sea on the recovery platform ("Return On Investment"). This is the **headline / baseline** number Rocket Lab uses to describe Neutron.
- **Return to launch site (RTLS):** up to **8,500 kg (18,700 lb)** — booster flies back to the launch site.

These three figures appear consistently in Rocket Lab materials and in secondary sources that cite Rocket Lab, so they are treated as **official Rocket Lab, high-confidence** values. They should not be described as independently validated unless the source trail is explicitly independent of Rocket Lab.

### Sun-synchronous orbit (SSO) — CRITICAL GAP
**Rocket Lab has not published a Neutron SSO payload number.** Multiple searches (including the Neutron Payload User's Guide v1.0, Jan 2025) returned no SSO-specific figure. The PUG reportedly models SSO trajectories but does not state a headline SSO capacity; Rocket Lab directs customers to request mission-specific performance.

**What we can say:**
- The Neutron PUG does publish a useful official proxy: **500 km polar** payload values of **6.2 t RTLS**, **10.1 t DRL**, and **11.8 t expendable**. Polar is not identical to SSO, but it anchors the SSO estimate more tightly than LEO-only inference.
- SSO is a high-inclination (~97–98°), retrograde-launch orbit. It carries a well-understood performance penalty versus a low-inclination LEO insertion — for comparable launch vehicles the SSO figure is typically **roughly 60–80% of the same vehicle's LEO-due-east figure**, depending on altitude and launch azimuth losses.
- Applying that band to Neutron's **13,000 kg DRL** baseline gives a **rough, unofficial estimate of ~8,000–10,000 kg to SSO** in the reusable (DRL) configuration, and proportionally more (~9,000–12,000 kg) expendable. The later payload-focused doc refines the reusable working figure to **~9,500 kg** by also considering the official 10.1 t polar proxy. **This is an analyst estimate by inference only — not a Rocket Lab number — and must be confirmed directly with Rocket Lab before any design decision relies on it.**
- One low-quality search snippet stated "up to 8,000 kg to LEO"; later review traced that to the original 2021 Neutron design target rather than a current payload number. It should not be used as a present-day LEO or SSO performance figure.

> **Action item:** Obtain the SSO performance curve directly from Rocket Lab (launch@rocketlabusa.com) or the full Payload User's Guide. This is the single most important missing number for the thesis.

---

## 2. Fairing ("Hungry Hippo")

Neutron's defining feature is a **captive, reusable carbon-composite fairing** nicknamed "Hungry Hippo." Unlike conventional fairings, **it does not jettison**: it stays attached to Stage 1, opens its two clamshell halves to release the second stage + payload, then closes again so the booster can return and land with the fairing intact. This is described by Rocket Lab as a **commercial first**.

**Dimensions (what is known):**
- **Height:** **~14 m** — stated by Rocket Lab directly (X/Twitter post, Jan 2026: "Neutron's 14 m tall reusable Hungry Hippo fairing"); corroborated by Space.com ("46-foot / 14-meter fairing"). **High confidence.**
- **Payload diameter accommodation:** **up to 5.5 m** — per the Neutron Payload User's Guide v1.0 (Jan 2025) as reported in multiple secondary summaries. Some **earlier** material cited a **5.0 m** fairing. The **5.5 m** figure is the more recent and is treated as current; the discrepancy is noted as a **source disagreement** (older 5.0 m vs. current 5.5 m). **Medium–High confidence.**
- The 14 m is the **external fairing height**; **usable payload length is less** (the second stage is housed entirely inside the fairing, hung from the separation plane, which consumes a large fraction of internal length). One secondary summary cited "16.5 m of usable payload length" — this is **inconsistent** with a 14 m fairing height and is judged **unreliable** (likely a confusion with another vehicle or a misread). **Do not rely on it.**

**Usable payload volume — NOT PUBLISHED.**
Rocket Lab has **not disclosed** a usable internal payload volume in cubic meters. A rough geometric estimate for a ~5 m-diameter usable envelope over an ~8–12 m usable length (cylinder + ogive, after deducting Stage 2 housing) lands in the order of **~150–230 m³**, but this is a **crude estimate, not an official figure**, and the usable length input is itself uncertain.

### Mass-bound vs. volume-bound for rack-dense cargo
- A fully populated server/compute rack is **dense** (high mass per unit volume) relative to typical satellites.
- With ~13 t (DRL LEO) or an estimated ~8–10 t (SSO) payload allowance and a fairing on the order of 150+ m³, **rack-dense data-center cargo is very likely to be MASS-bound, not volume-bound** — i.e., you will hit the payload-mass limit long before you fill the fairing volume.
- Implication: fairing volume is probably **not** the binding constraint; **payload mass to SSO is the binding constraint**, which makes the unpublished SSO number even more important.
- Caveat: if the compute hardware is packaged with extensive radiators, deployable structures, or low-density thermal/structural enclosures, volume could become competitive. This depends entirely on the spacecraft bus design.

---

## 3. Rocket specifications

| Item | Detail |
|---|---|
| Type | Two-stage, partially reusable, medium-lift launch vehicle |
| Height | ~43 m (Wikipedia/RL; some earlier sources said 40 m) |
| Base diameter | 7 m, tapering toward the fairing |
| Liftoff mass | ~480,000 kg (RL spec page) |
| Structure | Carbon-composite tanks and structures (both stages) |
| Propellant | LOX / liquid methane (methalox) |
| Stage 1 engines | 9 × Archimedes (sea-level), "octal-plus-one" layout |
| Stage 1 thrust | ~6,610 kN (1,485,000 lbf) total at liftoff |
| Stage 2 engine | 1 × Archimedes, vacuum-optimized, 890 kN (~200,000 lbf) |
| Stage 2 / fairing integration | Stage 2 housed **entirely inside** the Hungry Hippo fairing, hung in tension from the separation plane |

### Archimedes engine
- In-house, 3D-printed (laser powder-bed fusion; reportedly ~90% of engine mass printed).
- **Oxidizer-rich staged-combustion** cycle, methalox.
- Single design used in both sea-level (Stage 1) and vacuum-optimized (Stage 2) variants — commonality intended to reduce cost and simplify production.
- Originally revealed (Dec 2021) at ~1 MN class; first-stage count raised from 7 to 9 in a Sept 2022 design revision.
- As of Q1 2026, Archimedes is in **qualification testing** at NASA Stennis Space Center (Mississippi) — full-duration burns, thrust-vector-control sweeps, and vacuum-engine hot fires, with both test cells reportedly running continuously.

---

## 4. Reusability

- **What is reused:** Stage 1 (booster) **and** the captive Hungry Hippo fairing (the fairing returns attached to the booster). **Stage 2 is expendable.**
- **Two recovery modes:**
  - **RTLS (return to launch site):** booster flies back to Launch Complex 3, Wallops, Virginia. Lowest payload (~8,500 kg LEO).
  - **DRL (downrange landing):** booster lands at sea on the marine recovery platform. Higher payload (13,000 kg LEO) — this is the baseline mode.
- **Expendable mode:** booster not recovered; highest payload (~15,000 kg LEO).
- Rocket Lab targets **10–20 flights per booster**, comparable to current Falcon 9 booster reuse.
- Reuse cost logic: cost of goods per vehicle estimated at **$20–25 M**, with ~half attributed to the expendable Stage 2 — so the recurring expended hardware cost per flight is dominated by Stage 2.
- Early flights are expected to fly in **expendable mode** to validate performance before transitioning to reusable recovery profiles.

---

## 5. Flight status & cadence (as of May 2026)

- **Has not flown.** First flight **targeted for Q4 2026**. FAA launch permits filed for a window of **July 1 – December 31, 2026**.
- The schedule has **slipped repeatedly** (originally 2024, then 2025, then 2026) — treat the Q4 2026 date as a **target, not a commitment**.
- **January 2026 setback:** a Stage 1 propellant tank **failed hydrostatic pressure testing (Jan 21, 2026)** and ruptured. Rocket Lab attributed it to a hand-lay manufacturing defect class and switched the replacement tank to an **automated fiber-placement** process to eliminate that defect class.
- **Q1 2026 progress:** Archimedes qualification ongoing at Stennis; second stage and reusable fairing systems "cleared additional milestones"; first flight hardware coming together at the Assembly & Integration Complex in Virginia. CEO Peter Beck flagged "items placed on test stands" as the key progress benchmark.
- **Manifest:** Neutron's commercial manifest is filling before first flight. In **May 2026**, Rocket Lab announced its **largest contract ever** — a confidential customer booked **5 dedicated Neutron launches + 3 dedicated Electron launches** (2026–2029). Total company launch manifest reported at **70+ missions**, backlog **$2.2 B+**. A U.S. Air Force **point-to-point cargo demonstration** is also manifested (reusable-profile mission).

---

## 6. Cost

- **No public list price.** Rocket Lab has given a **company target of ~$50 M per launch** (stated 2023, via CNBC), later described as a **"$50–55 M launch service cost."**
- Cost of goods per vehicle: estimated **$20–25 M**, ~half from the expendable Stage 2.
- Rocket Lab targets **~50% gross margin** on Neutron launches.
- Some recent contracts reportedly priced near the company's "average selling price," but **specific contract pricing is undisclosed**.
- **Confidence:** Medium. These are **company guidance / targets**, not validated transaction prices, and predate first flight.

---

## 7. Comparison — Neutron vs. Falcon 9 vs. Electron

| Parameter | **Electron** | **Neutron** | **Falcon 9 (Block 5)** |
|---|---|---|---|
| Class | Small-lift | Medium-lift | Medium-lift |
| Payload to LEO | ~300 kg | 13,000 kg (DRL, reusable) / ~15,000 kg expendable | ~22,800 kg (LEO, low inclination) |
| Payload to SSO | ~200 kg (500 km SSO) | **Not published** (est. ~8–10 t, unofficial) | ~ "cake topper" + rideshare; SSO rideshare from $300k/50 kg |
| Fairing diameter | ~1.2 m | up to 5.5 m payload accommodation | 5.2 m (≈5 m usable) |
| Fairing height | ~2.5 m | ~14 m (external) | ~13.1 m |
| Usable fairing volume | small | **Not published** (est. ~150–230 m³) | ~145 m³ |
| Reusability | Booster recovery attempted | Stage 1 + fairing reusable | Stage 1 + fairings reusable |
| Price | ~$8 M | ~$50–55 M (target) | ~$67 M list (rideshare cheaper) |
| Status | Operational | In development, first flight Q4 2026 target | Operational, high cadence |

**Takeaways:**
- Neutron is **squarely Falcon-9-class** but lands at roughly **55–65% of Falcon 9's LEO payload** (13 t vs. ~22.8 t reusable-class). It is **not** a Falcon Heavy / Starship competitor.
- Neutron's fairing payload diameter (5.5 m) is **slightly larger** than Falcon 9's (~5 m usable); fairing volume is plausibly **similar or modestly larger** than Falcon 9's ~145 m³, though Neutron's number is unconfirmed.
- Electron is **two orders of magnitude smaller** and not relevant for data-center-scale payloads — useful only as a tech-demo / small-sat reference within the Rocket Lab family.

---

## 8. Implications for the orbital data-center thesis

1. **Mass-bound, not volume-bound.** Dense compute racks will almost certainly hit Neutron's **payload-mass** ceiling well before filling the fairing. The binding constraint is mass to SSO.
2. **The SSO number is the critical unknown.** Estimated ~8–10 t to SSO (DRL/reusable) is **inference, not official**. The whole feasibility envelope hinges on confirming this with Rocket Lab.
3. **A single Neutron likely carries one or a few racks, not a full data center** — implying multi-launch campaigns and on-orbit aggregation, or per-launch self-contained "data-center module" spacecraft sized to ~8–13 t.
4. **Schedule risk is real.** Neutron has not flown and has slipped repeatedly; a thesis depending on Neutron availability should assume **first operational reusable flights no earlier than 2027** and build in margin.
5. **Cost.** At a ~$50–55 M target, Neutron's $/kg to SSO (if ~8–10 t) is on the order of **$5,000–7,000/kg** — competitive with Falcon 9 dedicated but well above Falcon 9/Starship rideshare economics. Treat as a target, not a quote.

### Speculative — a hypothetical uprated / "block-upgraded" Neutron
*(Clearly labeled SPECULATION — no Rocket Lab statement supports a specific uprated variant as of May 2026.)*
If baseline SSO capacity proves marginal, historical precedent (Falcon 9 grew ~v1.0 → Block 5 by >2×; Electron received incremental payload bumps) suggests Rocket Lab could pursue **engine uprating, stretched tanks, or expendable-mode optimization** to raise SSO capacity. A plausible *speculative* uprated Neutron might push **SSO capacity toward the low-teens of tonnes** over several years — but **there is no announced Neutron block upgrade**, and any such gain would arrive years after first flight. Do not baseline the thesis on it.

---

## Sources

- [Rocket Lab Neutron — Wikipedia](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron)
- [Neutron — Rocket Lab official page](https://rocketlabcorp.com/launch/neutron/)
- [Neutron Payload User's Guide v1.0, Jan 2025 — Rocket Lab (PDF)](https://rocketlabcorp.com/assets/Uploads/Rocket-Lab-Neutron-PUG-reduced-final.pdf)
- [Archimedes (rocket engine) — Wikipedia](https://en.wikipedia.org/wiki/Archimedes_(rocket_engine))
- [Reusable Rockets — Rocket Lab](https://rocketlabcorp.com/launch/reusable-rockets/)
- [Rocket Lab signs new launch contracts and acquires robotics company during Q1 2026 — NASASpaceFlight (May 2026)](https://www.nasaspaceflight.com/2026/05/rocket-lab-q1-2026/)
- [Rocket Lab announces five-launch Neutron deal as it continues aiming for late 2026 debut — Spaceflight Now (May 7, 2026)](https://spaceflightnow.com/2026/05/07/rocket-lab-announces-five-launch-neutron-deal-as-it-continues-aiming-for-late-2026-debut/)
- [Rocket Lab's Biggest Launch Deal Yet — Rocket Lab Investor Relations (May 7, 2026)](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-labs-biggest-launch-deal-yet-confidential-customer-books)
- [Rocket Lab delays debut of Neutron rocket to 2026 — Spaceflight Now (Nov 11, 2025)](https://spaceflightnow.com/2025/11/11/rocket-lab-delays-debut-of-neutron-rocket-to-2026/)
- [Rocket Lab delays first Neutron launch to 2026 — SpaceNews](https://spacenews.com/rocket-lab-delays-first-neutron-launch-to-2026/)
- [Hungry Hippos and Test Tanks — Rocket Lab building towards Neutron — NASASpaceFlight (Jan 2026)](https://www.nasaspaceflight.com/2026/01/hungry-hippos-test-tanks-neutron/)
- [Rocket Lab's 'Hungry Hippo' Neutron fairing arrives at spaceport in Virginia — Space.com](https://www.space.com/space-exploration/launches-spacecraft/rocket-labs-hungry-hippo-neutron-fairing-arrives-at-spaceport-in-virginia)
- [Rocket Lab on X — "Neutron's 14m tall reusable Hungry Hippo fairing"](https://x.com/RocketLab/status/2015902732142702693)
- [Rocket Lab qualifies Neutron 'Hungry Hippo' fairing — StockTitan](https://www.stocktitan.net/news/RKLB/hungry-hippo-fairing-successfully-qualified-rocket-lab-clears-stsrvu4ym3ag.html)
- [Rocket Lab's new Neutron rocket suffers fuel tank rupture during test — Space.com](https://www.space.com/space-exploration/rocket-labs-new-neutron-rocket-suffers-fuel-tank-rupture-during-test)
- [After record-breaking 2025, Rocket Lab prepares for Neutron's debut in 2026 — NASASpaceFlight (Dec 2025)](https://nasaspaceflight.com/2025/12/rocket-lab-2025-overview/)
- [Neutron switches to methane/oxygen, 1 Meganewton Archimedes engine revealed — NASASpaceFlight (Dec 2021)](https://www.nasaspaceflight.com/2021/12/neutron-update-dec-2021/)
- [US military taps Rocket Lab's Neutron launcher for 'point to point' cargo test flight in 2026 — Space.com](https://www.space.com/space-exploration/launches-spacecraft/us-military-taps-rocket-labs-new-neutron-launcher-for-point-to-point-cargo-test-flight-in-2026)
- [Rocket Lab targets $50 million launch price for Neutron rocket — CNBC (Mar 2023)](https://www.cnbc.com/2023/03/24/rocket-lab-neutron-launch-price-challenges-spacex.html)
- [Rocket Lab Increases Electron Payload Capacity — Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-increases-electron-payload-capacity-enabling-interplanetary-missions-and-reusability/)
- [Falcon 9 — Wikipedia](https://en.wikipedia.org/wiki/Falcon_9)
- [Falcon Payload User's Guide — SpaceX (PDF)](https://www.spacex.com/assets/media/falcon-users-guide-2025-05-09.pdf)
- [Neutron — Gunter's Space Page](https://space.skyrocket.de/doc_lau/neutron.htm)
- [Neutron Rocket / Launch Vehicle Details — SatNow](https://www.satnow.com/launch-vehicle-details/neutron)

---

## Open questions / uncertainties

1. **SSO payload mass — UNRESOLVED (highest priority).** Rocket Lab has not published a Neutron SSO figure. The ~8–10 t (reusable/DRL) estimate here is **inference from comparable vehicles**, not official. Must be confirmed directly with Rocket Lab. The entire feasibility envelope depends on it.
2. **Usable fairing volume — UNRESOLVED.** No official cubic-meter figure. The ~150–230 m³ estimate is crude geometry with an uncertain usable-length input. The "16.5 m usable length" snippet seen in one secondary source is inconsistent with a 14 m fairing and judged unreliable.
3. **Fairing diameter: 5.0 m vs. 5.5 m.** Sources disagree; 5.5 m (PUG v1.0, Jan 2025) is treated as current, older material says 5.0 m.
4. **Rocket height: 40 m vs. 43 m.** Minor source disagreement; 43 m is the more recent figure.
5. **One search snippet claimed "8,000 kg to LEO."** ✅ **RESOLVED** by `rocket_lab/neutron/payload_and_block_upgrade.md` §4: the 8,000 kg figure was the **original 2021 Neutron design payload** (the early-design Neutron, before the vehicle grew to its current ~13 t LEO downrange capacity) — it was neither an error nor a garbled SSO number. The current official LEO figures (13–15 t) stand and reflect the matured design.
6. **Schedule confidence is low.** Q4 2026 is a target; Neutron has slipped from 2024 → 2025 → 2026. The Jan 2026 tank rupture adds risk. Operational reusable flights realistically NET 2027.
7. **Cost figures are company targets**, pre-first-flight, not validated transaction prices.
8. **No announced uprated/block-upgrade Neutron variant** exists; any capacity-growth scenario in this document is explicitly speculative.
9. **Payload-to-fairing geometry:** Stage 2 sits inside the Hungry Hippo fairing, so usable payload length is significantly less than the 14 m external height — exact usable envelope dimensions are not public.
