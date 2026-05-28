# Neutron — Payload Performance by Launch Mode & Orbit, and Block-Upgrade Potential

**Research date:** 2026-05-17
**Purpose:** Pin down Neutron's payload capacity across launch modes (RTLS / downrange / expendable) and orbits (LEO / SSO), and assess a plausible future "block-upgraded" Neutron. These numbers feed the orbital data-center node-flyability and economic models.
**Vehicle status:** In development; **has not flown** as of May 2026. First flight targeted Q4 2026; early flights expendable.

---

> **Source status (2026-05-25):** See [SOURCE_INDEX.md](../../SOURCE_INDEX.md) claim IDs NTR-001 through NTR-011. Rocket Lab/PUG LEO and 500 km polar values are official. The SSO values in this document remain estimates, not Rocket Lab-published figures, and the block-upgrade case is an upside scenario.

## Summary payload table (mode × orbit)

| Launch mode | Payload to LEO (~28.5° / due-east, low alt) | Payload to **SSO** (~97–98°, ~500–600 km) | Basis |
|---|---|---|---|
| **RTLS** (return to launch site) | **8,500 kg** *(PUG official; see source note)* | **~5,500–7,000 kg** *(estimate)* | LEO official; SSO derived |
| **Downrange landing** (DRL, ocean platform) — *baseline reusable* | **13,000 kg** *(official)* | **~8,500–10,500 kg** *(estimate; working figure ~9,500 kg)* | LEO official; SSO derived from polar proxy + SSO penalty |
| **Expendable** (no booster recovery) | **15,000 kg** *(official)* | **~10,000–12,000 kg** *(estimate; working figure ~11,000 kg)* | LEO official; SSO derived from polar proxy + SSO penalty |

**Official** = stated by Rocket Lab or the Neutron PUG. Secondary sources that repeat Rocket Lab are useful cross-checks, but they are not independent validation. **SSO figures are analyst estimates by inference** — Rocket Lab has published **no** Neutron SSO number. SSO is the load-bearing unknown for this project; see §2.

> **Headline for the project:** Use **~9,500 kg (range 8,500–10,500 kg) reusable-to-SSO** as the baseline node mass budget, **~11,000 kg expendable-to-SSO**, and **~12,000–13,000 kg** for a plausible block-upgraded reusable-to-SSO Neutron later in the program (see §6).

---

## 1. Neutron payload by launch mode, to LEO (confirmed / official)

Rocket Lab states **three** LEO payload numbers, differing only by booster-recovery mode. They appear consistently on Rocket Lab's own Neutron page, in the Neutron Payload User's Guide (PUG) v1.0, on Wikipedia (citing Rocket Lab), and have been repeated by Peter Beck in 2025–2026 interviews. Treat them as **official Rocket Lab, high-confidence** values, not as independently derived third-party measurements:

- **Expendable:** up to **15,000 kg (33,100 lb)** to LEO — booster not recovered.
- **Downrange landing (DRL):** **13,000 kg (28,700 lb)** to LEO — booster lands at sea on the *Return On Investment* recovery platform. **This is the headline / baseline number** Rocket Lab uses to describe Neutron, and the baseline reusable mode.
- **Return to launch site (RTLS):** up to **8,500 kg (18,700 lb)** to LEO — booster flies back to Launch Complex 3, Wallops.

[Wikipedia — Rocket Lab Neutron](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron): *"Neutron is designed to lift up to 15,000 kg (33,100 lb) to LEO while expended, 13,000 kg (28,700 lb) while landing the booster downrange and up to 8,500 kg (18,700 lb) with the first stage returning to the launch site."* Confirmed by [Rocket Lab — Neutron](https://rocketlabcorp.com/launch/neutron/) and by Beck in [NASASpaceFlight (Oct 2025)](https://www.nasaspaceflight.com/2025/10/beck-neutron-update/).

### Usable payload vs. reserved landing propellant — important framing

The three figures above are **usable payload mass delivered to orbit** — i.e., the mass of the customer's spacecraft. They are **not** reduced by the landing propellant; rather, **the landing propellant reservation is the reason the three numbers differ**:

- In **expendable** mode no propellant is held back for a landing burn, so the stage burns to depletion and the full **15,000 kg** is available as usable payload.
- In **DRL** mode the booster reserves enough propellant for a single re-entry/landing burn on a downrange ocean platform — a *modest* reserve because the booster does not reverse its downrange velocity. The performance cost is the gap **15,000 → 13,000 kg ≈ 2,000 kg (≈13%)**.
- In **RTLS** mode the booster must additionally perform a **boostback burn** to null out downrange velocity and fly back to the launch site — a *large* propellant reservation. The performance cost is the gap **15,000 → 8,500 kg ≈ 6,500 kg (≈43%)**, or **13,000 → 8,500 kg ≈ 4,500 kg (≈35%)** relative to DRL.

So "13,000 kg to LEO (DRL)" already **accounts for** the landing propellant — you do not subtract anything further. The quoted number is what the customer gets.

---

## 2. Payload to SSO — the load-bearing unknown (ESTIMATE)

**Rocket Lab has published no Neutron SSO payload figure.** The Neutron PUG v1.0 (Jan 2025) states that Neutron's performance modelling *"accounts for low- through to high-inclination orbits and sun-synchronous orbits (SSO),"* and that Stage 2 supports direct-injection / multi-plane delivery — but it gives **no headline SSO capacity**; customers are directed to request a mission-specific performance estimate. Repeated, targeted searches in May 2026 returned **no official Neutron SSO number** from any source.

The PUG does publish a close official proxy: **500 km polar** payload values of **6.2 t RTLS**, **10.1 t DRL**, and **11.8 t expendable**. Polar is not identical to SSO, but it is the best public Rocket Lab anchor for this project because it is high-inclination performance at a relevant altitude. The SSO estimates below should be read as "polar-proxy plus SSO penalty" rather than LEO-only arithmetic.

### Why SSO costs performance

SSO is a near-polar, slightly **retrograde** orbit (inclination ~97–98°). A launch vehicle loses payload performance to SSO versus a low-inclination LEO insertion for two compounding reasons:

1. **No Earth-rotation assist — actually a penalty.** A due-east launch from Wallops (~37.8°N, LC-3) gains roughly **+0.3–0.4 km/s** "free" from Earth's eastward rotation. An SSO launch is slightly retrograde, so instead of gaining that velocity it must partly *cancel* it. The net swing between a due-east insertion and a sun-synchronous insertion is on the order of **~0.5–0.8 km/s of additional Δv** the vehicle must supply.
2. **Azimuth / dogleg and altitude.** SSO missions from Wallops fly a southerly (and partly dogleg-constrained) azimuth and typically target **500–700 km** rather than a minimal ~200 km LEO, adding orbit-raising Δv.

For comparable two-stage medium-lift vehicles, the SSO figure typically lands at **~65–80% of the same vehicle's quoted low-inclination LEO figure**, depending on target altitude. (SpaceX's Falcon 9 PUG shows the same qualitative LEO > polar > SSO ordering; exact ratios are altitude-dependent.) Note Rocket Lab quotes Neutron's LEO numbers at a relatively low reference altitude/inclination, so the SSO ratio is toward the **middle** of that band, not the top.

### Derived SSO estimate (analyst inference — NOT a Rocket Lab number)

Applying a **~70% (range ~65–80%) LEO→SSO retention factor** to each official LEO figure:

| Mode | LEO (official) | LEO→SSO factor | **SSO estimate (range)** | **SSO working figure** |
|---|---|---|---|---|
| RTLS | 8,500 kg | 0.65–0.80 | **~5,500–6,800 kg** | ~6,000 kg |
| **DRL (baseline reusable)** | 13,000 kg | 0.65–0.80 | **~8,500–10,400 kg** | **~9,500 kg** |
| Expendable | 15,000 kg | 0.65–0.80 | **~9,800–12,000 kg** | **~11,000 kg** |

This **brackets and slightly tightens** the project's prior estimate (~8.5–9 t reusable-to-SSO, a 25–30% penalty). A 25–30% penalty corresponds to a 0.70–0.75 retention factor, which sits inside this range; the prior estimate was on the conservative (low) side. The recommended **working baseline is ~9,500 kg reusable-to-SSO**, with explicit acknowledgement that the true value could plausibly be anywhere from **~8,500 to ~10,500 kg**.

> **This remains the single most important unverified number in the entire feasibility analysis.** It must be confirmed directly with Rocket Lab (launch@rocketlabusa.com) or via the full Neutron PUG performance curves before any economic conclusion is treated as firm. Confidence: **Low–Medium** (the *method* is sound and the range is defensible; the *point value* is not official).

---

## 3. Does landing mode trade against payload as expected?

**Yes — the ordering and gaps are exactly as physics predicts:** RTLS < DRL < Expendable, monotonically.

| Comparison | LEO mass gap | % of expendable | Why |
|---|---|---|---|
| Expendable → DRL | −2,000 kg | −13% | Booster reserves propellant for a single downrange landing burn |
| Expendable → RTLS | −6,500 kg | −43% | Booster additionally reserves propellant for a boostback burn back to LC-3 |
| DRL → RTLS | −4,500 kg | −35% (of DRL) | Incremental cost of the boostback burn alone |

The **RTLS penalty (~43% off expendable, ~35% off DRL)** is steep — consistent with Falcon 9, where RTLS likewise costs far more performance than a downrange droneship landing. **Implication for the project:** RTLS-mode Neutron (~8.5 t LEO, ~6 t SSO est.) is materially under-sized for a meaningful data-center node. The project should baseline **DRL (downrange/ocean-platform) reusable mode** — the booster still returns and is reused, just landed at sea — which is the mode Rocket Lab itself treats as the performance baseline. Reserve RTLS only for cases where launch-site turnaround speed outweighs payload.

---

## 4. Electron payload growth — the block-upgrade reference case

Rocket Lab has a documented track record of growing a vehicle's payload **after** entering service, which is the empirical basis for projecting Neutron block upgrades.

**Electron payload history:**

| Period | Payload to 500 km SSO | Max payload to lower LEO | Source |
|---|---|---|---|
| Maiden flight era (2017–2020 design spec) | **150 kg** | **225 kg** | [Wikipedia — Electron](https://en.wikipedia.org/wiki/Rocket_Lab_Electron); [Rocket Lab on X, Aug 2020](https://x.com/RocketLab/status/1290680251916288000) |
| August 2020 upgrade → current | **200 kg** | **300 kg** (some 2025 spec sheets cite up to ~320 kg) | [Rocket Lab — Increases Electron Payload Capacity](https://rocketlabcorp.com/updates/rocket-lab-increases-electron-payload-capacity-enabling-interplanetary-missions-and-reusability/); [SpaceNews](https://spacenews.com/rocket-lab-increases-electron-payload-capacity/) |

**Percent growth:**
- SSO: 150 → 200 kg = **+33%**
- Max LEO: 225 → 300 kg = **+33%**

**The founder's recollection of "~30%" is confirmed — the actual figure is ~33%.** Rocket Lab achieved this **on the same airframe** ("Same rocket, more payload" — Rocket Lab's own phrasing), primarily through **battery energy-density advances** for the Rutherford electric-pump engines, plus incremental optimization. Rocket Lab explicitly framed the upgrade as partly intended to **offset the mass penalty of adding booster-recovery hardware** — directly analogous to the reuse-vs-payload trade Neutron faces. If 2025 spec sheets citing ~320 kg LEO are taken as current, total growth from the 225 kg baseline is ~**+42%**.

**Neutron has *already* shown one round of pre-flight payload growth:** the **March 2021 design** was announced at **8,000 kg to LEO**; the **September 2022 redesign** (first stage went from 7 to 9 Archimedes engines, larger structure) raised the baseline to the current **13,000 kg DRL**. That ~8 t → 13 t is a paper/design-phase change rather than in-service growth, but it confirms Rocket Lab's willingness to uprate Neutron substantially. (Note: this resolves the prior `neutron_specs.md` "open question" #5 — the "8,000 kg to LEO" snippet was **not erroneous**; it was the *original 2021 Neutron design figure*, since superseded.)

---

## 5. Neutron block-upgrade potential (PROJECTED / SPECULATIVE)

**Status of evidence:** As of May 2026 Rocket Lab has **not announced** a specific uprated or "block 2" Neutron variant, and there is **no published Neutron growth roadmap**. Everything in this section is **projection by analogy** and must be labelled speculative.

**What Rocket Lab *has* said that bears on growth potential:**
- The **Archimedes engine is deliberately run conservatively.** At full power each engine produces **~165,000 lbf (733 kN)**; Rocket Lab states Archimedes *"operates at lower stress levels than other rocket engines to enable rapid and reliable reusability"* and has already demonstrated **102% power** in qualification testing ([Archimedes — Wikipedia](https://en.wikipedia.org/wiki/Archimedes_(rocket_engine)); [Friends of NASA, 2025](https://www.friendsofnasa.org/2025/08/rocket-lab-tests-archimedes-engine-for.html)). A deliberately de-stressed engine is the **textbook precondition for a later thrust-uprating block upgrade** — exactly how SpaceX grew the Merlin/Falcon 9 and how Rocket Lab grew Rutherford/Electron.
- Beck describes Neutron as designed to *"scale quickly"* and has said the architecture is about *"right-sizing the vehicle for the majority of the market"* — language consistent with an intent to evolve the vehicle, though not a committed uprate plan ([NASASpaceFlight, Oct 2025](https://www.nasaspaceflight.com/2025/10/beck-neutron-update/)).
- Rocket Lab acquired the former Virgin Orbit / Long Beach factory explicitly as a **"scaling enabler"** for Neutron production ([SpaceNews](https://spacenews.com/rocket-lab-sees-virgin-orbit-facility-as-scaling-enabler-for-neutron/)) — this is about *rate*, not per-vehicle performance, but signals long-horizon investment.

**Plausible block-upgrade levers (speculative):**
1. **Archimedes thrust uprating** — lifting from the current ~165k lbf toward the demonstrated ≥102% and beyond as qualification margin is retired. A ~5–10% thrust increase across 9 first-stage engines plus the vacuum engine is the most likely first lever.
2. **Propellant tank stretch** — modest tank lengthening to raise propellant load; feasible given carbon-composite tooling, though it interacts with the captive-fairing geometry.
3. **Stage 2 / fairing mass reduction** — manufacturing maturation (e.g., the automated fiber-placement process Rocket Lab adopted after the Jan 2026 tank failure) typically trims dry mass over a program's life.
4. **Recovery-hardware optimization** — lighter landing legs / grid fins recover payload in reusable modes specifically, exactly as Electron's battery upgrade offset recovery mass.

**Projected magnitude.** Electron grew **~33%** on the same airframe through incremental upgrades; Falcon 9 grew **>2×** across v1.0 → Block 5 through engine uprating + stretch. A **single Neutron "block upgrade"** combining engine uprating and modest mass reduction would plausibly land in the **+15–30%** range — well within the Electron precedent and conservative versus Falcon 9. Applied to the DRL baseline:

| Metric | Baseline Neutron | Block-upgraded (projected, +~20%) |
|---|---|---|
| DRL to LEO | 13,000 kg | **~15,000–17,000 kg** |
| DRL to SSO (est.) | ~9,500 kg | **~11,500–13,000 kg** |
| Expendable to SSO (est.) | ~11,000 kg | **~13,000–14,500 kg** |

**Caveats:** No such upgrade is announced; any gain would arrive **years after** first flight (Electron's upgrade came ~3 years after debut); and the SSO figures inherit the §2 estimation uncertainty *on top of* the block-upgrade uncertainty. **Do not baseline the core thesis on a block-upgraded Neutron** — treat it as upside.

---

## 6. Bottom line — payload numbers the project should now use

| Scenario | Payload to SSO | Confidence | Use in model |
|---|---|---|---|
| **Baseline — Neutron reusable (DRL) to SSO** | **~9,500 kg** (range **8,500–10,500 kg**) | Low–Medium (estimate) | **Primary node mass budget.** Run sensitivity across the full range. |
| **Neutron expendable to SSO** | **~11,000 kg** (range 9,800–12,000 kg) | Low–Medium (estimate) | Upside / surge case; higher $/kg, no booster reuse |
| **Block-upgraded Neutron, reusable (DRL) to SSO** | **~12,000–13,000 kg** | Speculative (projected) | **Upside scenario only** — do not baseline; arrives years post-debut |
| RTLS to SSO | ~6,000 kg (range 5,500–7,000 kg) | Low (estimate) | Under-sized for a node; avoid as a baseline mode |

**Key changes vs. prior project assumptions:**
- Prior docs used an estimated **~8.5–9 t reusable-to-SSO** (a 25–30% LEO penalty). This research **widens and slightly raises** that to **~8.5–10.5 t, working figure ~9.5 t** — the prior estimate sat at the conservative low end of a defensible band.
- The **LEO vs. SSO distinction is now unambiguous:** 13,000 kg is a **LEO, low-inclination** figure; the SSO node budget is **~25–35% lower** (~9–10 t), driven by the retrograde-inclination Δv penalty.
- All three **LEO** mode figures (8.5 / 13 / 15 t) are **official and high-confidence**; all **SSO** figures remain **estimates** pending Rocket Lab confirmation.

---

## Sources

- [Rocket Lab Neutron — Wikipedia](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron)
- [Neutron — Rocket Lab official page](https://rocketlabcorp.com/launch/neutron/)
- [Neutron Payload User's Guide v1.0, Jan 2025 — Rocket Lab (PDF)](https://rocketlabcorp.com/assets/Uploads/Rocket-Lab-Neutron-PUG-reduced-final.pdf)
- [Peter Beck discusses Neutron development as maiden flight nears — NASASpaceFlight (Oct 2025)](https://www.nasaspaceflight.com/2025/10/beck-neutron-update/)
- [Rocket Lab announces five-launch Neutron deal — Spaceflight Now (May 7, 2026)](https://spaceflightnow.com/2026/05/07/rocket-lab-announces-five-launch-neutron-deal-as-it-continues-aiming-for-late-2026-debut/)
- [Rocket Lab Reveals Ocean Platform "Return On Investment" — Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-reveals-ocean-platform-for-neutron-rocket-landings-at-sea/)
- [Rocket Lab Increases Electron Payload Capacity — Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-increases-electron-payload-capacity-enabling-interplanetary-missions-and-reusability/)
- [Rocket Lab Increases Electron Payload Capacity — SpaceNews](https://spacenews.com/rocket-lab-increases-electron-payload-capacity/)
- [Rocket Lab on X — Electron 150→200 kg SSO, 225→300 kg LEO (Aug 2020)](https://x.com/RocketLab/status/1290680251916288000)
- [Rocket Lab boosts Electron lift capacity — TechCrunch (Aug 2020)](https://techcrunch.com/2020/08/04/rocket-lab-boosts-electron-rockets-lift-capacity-by-660-lbs/)
- [Rocket Lab Electron — Wikipedia](https://en.wikipedia.org/wiki/Rocket_Lab_Electron)
- [Archimedes (rocket engine) — Wikipedia](https://en.wikipedia.org/wiki/Archimedes_(rocket_engine))
- [Rocket Lab Tests Archimedes Engine — full duration / 102% power — Friends of NASA (2025)](https://www.friendsofnasa.org/2025/08/rocket-lab-tests-archimedes-engine-for.html)
- [Rocket Lab gives first look at bigger, reusable Neutron rocket (original 2021 design) — CNBC (Dec 2021)](https://www.cnbc.com/2021/12/02/rocket-lab-reusable-neutron-rocket-update-competing-with-spacex.html)
- [Rocket Lab sees Virgin Orbit facility as "scaling enabler" for Neutron — SpaceNews](https://spacenews.com/rocket-lab-sees-virgin-orbit-facility-as-scaling-enabler-for-neutron/)
- [US military taps Rocket Lab's Neutron for point-to-point cargo test flight — Space.com](https://www.space.com/space-exploration/launches-spacecraft/us-military-taps-rocket-labs-new-neutron-launcher-for-point-to-point-cargo-test-flight-in-2026)
- [Falcon Payload User's Guide — SpaceX (PDF)](https://www.spacex.com/assets/media/falcon-users-guide-2025-05-09.pdf)
- [Electron — Gunter's Space Page](https://space.skyrocket.de/doc_lau/electron.htm)

---

## Open questions / uncertainties

1. **Neutron SSO payload mass — UNRESOLVED (highest priority).** No official figure exists. The ~9,500 kg DRL working figure (range 8,500–10,500 kg) is inference from a ~65–80% LEO→SSO retention factor. Must be confirmed via Rocket Lab's mission-specific performance estimate or the full PUG performance curves. **The entire node-flyability verdict depends on this.**
2. **LEO→SSO retention factor.** The ~70% mid-point is borrowed from comparable medium-lift vehicles; Neutron's actual factor depends on LC-3 launch azimuth constraints, dogleg requirements, and target SSO altitude — none published. Run the model across the full 0.65–0.80 band.
3. **Reference altitude/inclination for the "LEO" numbers.** Rocket Lab does not state the exact altitude/inclination behind 13,000 kg DRL. If it is quoted at a very low altitude / minimum-energy LEO, the real-world SSO penalty is larger than modeled here.
4. **Block upgrade is unannounced.** The +15–30% projected uprate is analogy-based (Electron +33%, Falcon 9 >2×). No Neutron growth roadmap is public; timing would be years post-debut. Treat strictly as upside.
5. **Archimedes flight thrust may differ from quoted full-power.** Engine demonstrated 102% in test; the flight-derate (if any) for first flights is not public — relevant to how much "free" uprate margin exists for a block upgrade.
6. **Schedule risk.** Neutron has not flown; first flight Q4 2026 is a target (slipped 2024→2025→2026), early flights expendable, reusable DRL operations realistically NET 2027. Any SSO/block-upgrade capability is further out still.
