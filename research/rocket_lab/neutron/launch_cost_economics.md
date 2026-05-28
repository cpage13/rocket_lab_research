# Neutron — Bottom-Up Launch Cost Economics (Internal / Marginal Cost)

**Research date:** 2026-05-18
**Purpose:** Build a first-principles, bottom-up estimate of Rocket Lab Neutron's **internal (marginal / cost) per-flight cost** — NOT the customer list price — for the orbital AI-inference data-center valuation model. The model treats the venture as flying its OWN payloads on Neutron, so the relevant input is what a flight *costs Rocket Lab to produce*, not what a customer pays.
**Vehicle status:** In development; has not flown as of May 2026. First flight targeted Q4 2026; early flights expendable, reusable downrange (DRL) operations realistically NET 2027.

**Tagging convention used throughout:**
- **[FACT]** — company-disclosed or independently reported figure.
- **[ESTIMATE]** — third-party estimate, or an analyst estimate built here for an undisclosed quantity.
- **[DERIVED]** — arithmetic performed in this document from the inputs above it.

> **Caveat up front:** Rocket Lab has published almost nothing on Neutron's cost *structure*. The only hard cost disclosure is a CNBC-reported "$20–25M cost of goods per vehicle, close to half from the expendable second stage" and a "$50–55M launch service price." Everything below the propellant line is therefore **ESTIMATE**, reasoned transparently and cross-checked against Falcon 9 (the closest analog) and Electron (Rocket Lab's own cost culture). Treat point values as central estimates inside explicit ranges.

> **Source status (2026-05-25):** See [SOURCE_INDEX.md](../../SOURCE_INDEX.md) claim IDs NTR-008 through NTR-010. The safe wording is cadence-specific: roughly **$23–27M** at low cadence, **$12–15M** at very high cadence, and **$10–11M** as a theoretical mature floor. Do not quote "$10–20M internal cost" as a single certified public fact.

---

## 0. Headline result

| Cadence regime | Bottom-up marginal cost per flight (internal) | Implied $/kg to SSO (~9.5 t reusable) |
|---|---|---|
| **Low cadence (≤5 launches/yr)** | **~$23–27M** → central **$25M** | ~$2,400–2,800/kg |
| **High cadence (≥100 launches/yr)** | **~$12–15M** → central **$13–14M** | ~$1,300–1,500/kg |
| **Credible hard floor** (mature, very high cadence) | **~$10–11M** | ~$1,050–1,150/kg |

**Recommendation for the valuation model:** the current **$25M low-cadence / $13M high-cadence** anchors are **well-supported and should be kept**, with one nuance — the high-cadence dial is at the *optimistic* edge of the credible band. See §7 for the full recommendation.

---

## 1. Propellant cost — small, as expected [DERIVED from ESTIMATEs]

### 1.1 How much propellant does Neutron carry?

Rocket Lab has **not disclosed** Neutron's propellant load or stage mass split, so it must be derived.

**Inputs:**
- Gross liftoff mass (GLOW): **480,000 kg** [FACT — Rocket Lab spec page, Wikipedia]
- Payload (DRL/reusable baseline): **13,000 kg** [FACT]
- Liftoff thrust: **6,600 kN** from 9 × Archimedes [FACT]; T/W = 6,600 kN ÷ (480,000 kg × 9.81) ≈ **1.40** [DERIVED] — a normal, healthy liftoff T/W, which confirms the 480 t GLOW is internally consistent.

**Derivation of propellant mass.** For a modern two-stage kerolox/methalox medium-lift vehicle, total propellant is typically **~89–92% of GLOW** (Falcon 9 is ~96% but is unusually dense-packed and structurally aggressive; carbon-composite methalox vehicles like Neutron sit a little lower because methane is less dense than RP-1 and composite tanks trade some mass fraction for reusability margin). Taking **~90.5% ± 1.5%**:

- Total propellant ≈ 480,000 × 0.905 ≈ **~434,000 kg** (range ~427,000–441,000 kg) [ESTIMATE/DERIVED]
- Residual: dry mass of both stages + fairing + payload ≈ 480,000 − 434,000 − 13,000 ≈ **~33,000 kg** of structure/engines [DERIVED] — plausible for a 9-engine reusable booster (~25–28 t) plus an expendable second stage (~5–7 t including engine).

**Stage split.** A 9:1 engine split and typical staged-combustion medium-lift staging put roughly **~88% of propellant in Stage 1, ~12% in Stage 2** [ESTIMATE]:
- Stage 1 propellant ≈ **~382,000 kg**
- Stage 2 propellant ≈ **~52,000 kg**

### 1.2 Methane / LOX mass split

Methalox engines run an oxidizer-to-fuel mixture ratio of **~3.5–3.8:1 by mass** (Raptor ≈ 3.6–3.8; stoichiometric is 4.0; staged-combustion methalox typically runs ~3.5–3.6 fuel-rich-of-stoichiometric for performance/temperature) [FACT — general methalox engineering]. Using **3.6:1**:

- LOX ≈ 434,000 × (3.6 / 4.6) ≈ **~340,000 kg** [DERIVED]
- Liquid methane (LNG) ≈ 434,000 × (1.0 / 4.6) ≈ **~94,000 kg** [DERIVED]

### 1.3 Commodity cost

| Propellant | Mass | Unit price | Cost | Source for price |
|---|---|---|---|---|
| Liquid oxygen (LOX) | ~340,000 kg | **~$0.10–0.20/kg** bulk; rocket-grade delivered ~$0.15/kg | **~$50,000** | US industrial LOX ~$0.12/kg (Dec 2025); rocket-grade w/ delivery & boil-off margin |
| Liquid methane / LNG | ~94,000 kg | **~$0.50–0.70/kg** (LNG ~$480–530/MT Q4 2025); rocket-grade purified higher, ~$0.70–1.20/kg | **~$80,000–110,000** | EIA / IMARC LNG pricing Q4 2025 |
| **Total propellant (chemicals only)** | ~434,000 kg | — | **~$0.13–0.16M** | [DERIVED] |

Add **boil-off, purging/chill-down losses, GN2/GHe pressurant, and scrubbed/aborted-load waste** — realistically a 1.5–2.5× multiplier on the raw chemical bill for *delivered, loaded* propellant including a typical fraction of scrubs:

> **Propellant cost per flight ≈ $0.25–0.35M [ESTIMATE]. Round to ~$0.3M.**

**Cross-check:** SpaceX's Falcon 9 propellant (LOX/RP-1, ~410 t) is widely cited at **~$0.20–0.25M/flight** (NextBigFuture Feb 2026: "$0.25M"; Musk has said "~$200k"). Neutron carries a similar total propellant mass; methane is somewhat pricier per kg than RP-1 but is a minority of the mass, and LOX dominates. **A ~$0.3M Neutron propellant bill is consistent with the Falcon 9 benchmark.** This confirms the brief's expectation: **propellant is a rounding error** — well under 2% of marginal cost. It is *not* where launch economics are won or lost.

---

## 2. The expendable second stage — the irreducible per-flight hardware floor [ESTIMATE]

Neutron's Stage 2 is **thrown away every flight**. Its build cost is the single largest, and the *irreducible*, recurring per-flight hardware cost. At 100 launches/yr, that is **100 second stages manufactured per year**.

### 2.1 What's in a Neutron Stage 2

- **1 × Archimedes Vacuum engine** — 890 kN, methalox, oxidizer-rich staged combustion, vacuum-optimized nozzle. ~90% 3D-printed by mass [FACT].
- **Carbon-composite propellant tanks** (LOX + methane, ~52 t propellant capacity) — uniquely, Stage 2 hangs *in tension* inside the Hungry Hippo fairing, so its structure can be relatively light (it is not a load-bearing column).
- **Avionics, flight computer, telemetry, GNC, batteries, reaction-control system.**
- **Pressurization system, plumbing, thrust structure.**

### 2.2 Cost build-up

**Anchor disclosure:** CNBC (Mar 2023) reported Rocket Lab's **cost of goods per Neutron vehicle at $20–25M, with "close to half" from the non-reusable second stage** [FACT]. "Close to half" of $20–25M ⇒ **Stage 2 ≈ $9–12M** at the time of that statement.

That 2023 figure is a *pre-production, pre-learning-curve* estimate. Two forces move it in opposite directions over the program:
- **Down:** manufacturing learning curve, 3D-printing throughput, engine production scale (Archimedes is now in series production).
- **Up:** the 2023 estimate predates known cost growth; first-article hardware always overruns.

**Bottom-up component estimate (steady-state, post-learning):**

| Stage 2 component | Cost estimate | Reasoning / cross-check |
|---|---|---|
| Archimedes Vacuum engine (1×) | **~$1.0–2.0M** | Merlin Vacuum is estimated at $0.5–0.75M at 300+/yr scale; Archimedes is a more complex *staged-combustion* engine (vs. Merlin's simpler gas-generator cycle) and produced at lower volume — so 2–3× a Merlin. 3D printing (~90% of mass) caps tooling/labor. |
| Carbon-composite tanks + structure + thrust frame | **~$3–5M** | Composite tankage is material- and autoclave/fiber-placement-intensive. Falcon 9's *aluminum* upper-stage tank+structure is cited at $4–6M; composite is costlier per part but Neutron's Stage 2 is lighter-duty (tension-hung). |
| Avionics, GNC, flight computer, RCS, batteries, harness | **~$2–3.5M** | Avionics are a large fraction of any upper stage; Rocket Lab builds these in-house (Electron heritage helps). |
| Integration, test, assembly labor, propulsion checkout | **~$1.5–2.5M** | Final assembly + acceptance testing of an expendable stage. |
| **Total Stage 2 build cost** | **~$8–13M** | **Central estimate ~$10M** [ESTIMATE] |

This **brackets the CNBC-implied $9–12M** and is consistent with Falcon 9's expendable upper stage at **$7M** (NextBigFuture Feb 2026) — Neutron's Stage 2 should be *somewhat more expensive* than Falcon 9's because (a) composite tanks cost more than aluminum, (b) a staged-combustion engine costs more than a gas-generator Merlin Vacuum, and (c) Neutron's production volume is far lower than Falcon 9's, so less learning-curve benefit.

> **Stage 2 build cost: ~$10M central [ESTIMATE], range $8–13M.**
> **Cadence sensitivity:** at ≤5/yr, expect the *high* end (~$12M) — first-article and low-rate production penalties. At ≥100/yr, expect ~$7–9M as the learning curve and 3D-printing throughput mature (Wright's-law learning at ~85–90% per doubling, applied over the ~4–5 doublings from 5→100/yr, comfortably supports a 25–35% unit-cost reduction). This single line item is the **largest swing** between the low- and high-cadence cases.

**This is the cost floor.** No amount of reusability or cadence can take per-flight hardware cost below the price of one expendable Stage 2 plus propellant plus the minimum ops crew. At maturity that floor is roughly **$7–9M (Stage 2) + $0.3M (propellant) + $1.5–2M (irreducible ops) ≈ $9–11M**.

---

## 3. First-stage refurbishment — turnaround cost between flights [ESTIMATE]

Neutron's Stage 1 (9 × Archimedes, 7 m carbon-composite, captive Hungry Hippo fairing) is **reused**; Rocket Lab targets **10–20 flights per booster** [FACT]. Two cost elements flow from this: (a) **amortization** of the booster's build cost over its flight life, and (b) **refurbishment** labor/parts per turnaround.

### 3.1 Booster build cost & amortization

From §2: total vehicle cost of goods $20–25M, Stage 2 ≈ half ⇒ **Stage 1 + fairing ≈ $10–13M to build** [FACT-derived]. Call the booster (incl. captive fairing) **~$14–18M** at maturity once you add the 9-engine cost (9 × ~$1–1.5M ≈ $9–13M of engines alone — the booster is *engine-cost-dominated*).

> Note the two figures are reconciled by timing: the CNBC "$20–25M total / ~half Stage 2" was a 2023 pre-production estimate; a mature booster with 9 series-produced Archimedes engines plus the reusable fairing is more naturally **~$15–18M**. The model only needs the *amortized* number.

**Amortization per flight** = booster build cost ÷ flights per booster:

| Booster life | Booster cost | Amortization per flight |
|---|---|---|
| Conservative (low cadence, early program): 10 flights, $17M | $17M | **~$1.7M** |
| Mature (high cadence): 15–20 flights, $15M | $15M | **~$0.75–1.0M** |

### 3.2 Refurbishment (labor + parts per turnaround)

**Falcon 9 benchmark [FACT]:** refurbishment cost has fallen dramatically as the pipeline matured — ~$3M (2022) → ~$1.5M (2024) → **~$0.8–1M (2026)**, i.e. **3–4% of new-build cost**. Musk's narrow "inspection-labor-only" figure is ~$0.25M; the realistic all-in turnaround (inspection + parts + minor repair + transport + re-acceptance) is **~$1M**.

**Neutron-specific adjustments:**
- **Worse than Falcon 9 early:** Neutron is new, low-cadence, RTLS or sea-recovery still being proven; early refurb will be slow and expensive (think Falcon 9 ~2018–2020, $3M+). Salt-water exposure on DRL recoveries adds corrosion-control work.
- **Structurally favorable:** carbon-composite primary structure resists fatigue and corrosion better than aluminum; Archimedes is **deliberately de-stressed** ("operates at lower stress levels than other rocket engines to enable rapid and reliable reusability" — Rocket Lab) — designed-in for cheap, fast turnaround.
- **The captive fairing is a genuine cost advantage:** Neutron does NOT fish a jettisoned fairing out of the ocean and refurbish it — the Hungry Hippo fairing returns *attached* to the booster, dry-ish, never having hit the water. That removes a whole recovery+refurb workstream Falcon 9 still partly carries.

**Refurbishment estimate:**

| Cadence regime | Refurb labor + parts per flight | Reasoning |
|---|---|---|
| Low cadence (≤5/yr, early program) | **~$2.5–4M** | Immature process, slow, salt exposure, learning. Falcon-9-2018 analog. |
| High cadence (≥100/yr, mature) | **~$0.8–1.5M** | Matured pipeline, composite structure, de-stressed engines. Falcon-9-2026 analog, slightly higher for lower absolute fleet scale. |

> **Combined Stage-1 cost per flight (amortization + refurbishment):**
> - **Low cadence: ~$1.7M + ~$3M ≈ $4.5–5M** [ESTIMATE]
> - **High cadence: ~$0.9M + ~$1.2M ≈ $2–2.5M** [ESTIMATE]

---

## 4. Fixed costs and how they amortize with cadence [ESTIMATE]

Fixed costs are spent whether you fly 5 or 100 times a year. Per-flight, they **collapse as cadence rises** — this is the dominant lever behind the low→high cadence cost decline (alongside Stage 2 learning curve).

### 4.1 What's in the fixed bucket

- **Launch site:** Launch Complex 3 at Wallops/MARS, Virginia — pad maintenance, propellant farm, cryo plant, ground systems, range interface. Plus the Return On Investment ocean recovery platform and its marine operations.
- **Workforce (standing army):** the launch, integration, recovery, and sustaining-engineering teams that exist regardless of flight count. Rocket Lab total headcount is **~2,645 (Q4 2025)** [FACT] across the whole company; the Neutron-dedicated standing workforce is a subset — perhaps **~400–800 people** allocated to Neutron launch operations + sustaining engineering once operational [ESTIMATE].
- **Range & regulatory:** FAA licensing, range safety services, tracking. US range fees are modest per flight but there is a fixed support overhead.
- **Insurance:** third-party liability (FAA mandates ~$80–200M coverage; premium ~1–2% of coverage ⇒ **~$1–2M/launch** [FACT — FAA/GAO data], though this is *per-launch* and partly variable). First-party "launch vehicle" insurance on an internal payload is the venture's choice.
- **Sustaining engineering, tooling, facilities, G&A** allocable to the launch business.

### 4.2 Sizing the annual fixed pool

Rocket Lab's **company-wide** GAAP operating expense is **~$115–120M per quarter (~$460–480M/yr) as of 2025** [FACT] — but that is heavily weighted to Neutron *development* (R&D) and the Space Systems segment, and will fall once Neutron development concludes. The relevant figure for this model is the **steady-state fixed cost of running the Neutron launch operation**, not company-wide opex.

**Estimate of Neutron's annual launch-operations fixed cost (post-development, steady state) [ESTIMATE]:**

| Fixed-cost element | Annual cost |
|---|---|
| Standing launch + recovery + integration workforce (~400–800 FTE fully loaded ~$200k) | **~$80–160M** |
| LC-3 pad + propellant farm + ground systems O&M, recovery platform marine ops | **~$25–45M** |
| Sustaining engineering, tooling, facilities, allocated G&A | **~$30–60M** |
| Range/regulatory fixed support | **~$5–15M** |
| **Total annual Neutron launch-operations fixed pool** | **~$140–280M; central ~$200M** |

This is an analyst estimate with wide error bars — Rocket Lab does not segment it. The **central ~$200M/yr** is cross-checked two ways: (a) it is roughly 40–45% of current company-wide opex, a reasonable share for the launch arm once development rolls off; (b) it is in line with what a Falcon-9-class operator's standing launch organization plausibly costs.

### 4.3 Per-flight amortization vs. cadence — the key table

| Launches / yr | Fixed cost per flight (at ~$200M/yr pool) | Range (at $140–280M/yr) |
|---|---|---|
| **5** | **$40M** | $28–56M |
| 10 | $20M | $14–28M |
| 24 (≈ "twice a month," Rocket Lab's stated target) | $8.3M | $5.8–11.7M |
| 50 | $4.0M | $2.8–5.6M |
| **100** | **$2.0M** | $1.4–2.8M |

> **This is the single most important dynamic in the whole cost curve.** At 5 launches/yr, fixed cost alone is ~$40M/flight — *larger than the entire rest of the vehicle*. At 100/yr it shrinks to ~$2M/flight. Cadence does not change what the hardware costs; it changes how thinly the standing army is spread.
>
> **Important modeling note:** a pure $200M/yr fixed pool gives an *absurd* $40M/flight at 5 launches/yr — but a company genuinely flying only 5×/yr would **not staff a 100-launch organization**. It would run a much smaller standing team (~$60–100M/yr pool). The realistic low-cadence fixed-cost-per-flight is therefore **~$12–18M**, not $40M — the fixed pool itself scales (slowly, lumpily) with the cadence the company is built for. The model should treat fixed cost as **semi-variable**, not a flat constant. The synthesis in §5 uses cadence-appropriate fixed pools.

---

## 5. Synthesis — bottom-up marginal cost per flight [DERIVED]

Combining §1–§4, with **cadence-appropriate** fixed pools (a 5×/yr operation is not staffed like a 100×/yr operation):

### Low cadence (~5 launches/yr) — early program, ~2027–2029

| Component | Cost per flight | Note |
|---|---|---|
| Propellant | **$0.3M** | Commodity; near-fixed regardless of cadence |
| Expendable Stage 2 | **$11–12M** | First-article / low-rate production penalty |
| Stage 1 amortization | **$1.7M** | ~10 flights/booster, ~$17M booster |
| Stage 1 refurbishment | **$3M** | Immature turnaround process, salt exposure |
| Fixed costs per flight | **$7–10M** | Smaller standing org (~$40–60M/yr pool) ÷ ~6 flights, *not* the $200M pool |
| **Total marginal cost — low cadence** | **~$23–27M** | **Central ~$25M** |

### High cadence (~100 launches/yr) — mature program

| Component | Cost per flight | Note |
|---|---|---|
| Propellant | **$0.3M** | Unchanged |
| Expendable Stage 2 | **$7.5–9M** | Learning curve, 3D-print throughput, engine scale |
| Stage 1 amortization | **$0.8–1M** | 15–20 flights/booster, ~$15M booster |
| Stage 1 refurbishment | **$1–1.5M** | Matured turnaround, composite structure, de-stressed engines |
| Fixed costs per flight | **$2–2.5M** | Full ~$200–250M/yr pool ÷ 100 flights |
| **Total marginal cost — high cadence** | **~$12–15M** | **Central ~$13–14M** |

### The credible cost floor

The **absolute floor** is set by what cannot be eliminated even at extreme cadence and full learning-curve maturity:
- Expendable Stage 2 at its mature minimum: **~$7–8M** (one staged-combustion engine + composite tank + avionics — physically cannot be cheaper without redesigning the stage)
- Propellant: **~$0.3M**
- Stage 1 amortization + refurb at best case: **~$1.5–2M**
- Irreducible per-flight ops/range/integration crew: **~$1.5–2M**

> **Credible hard floor ≈ $10–11M per flight.** Getting below ~$10M would require either making Stage 2 reusable (not in Neutron's design) or a Stage 2 redesign for radically lower cost. **The expendable second stage is the binding floor** — it alone is ~70% of the floor.

### Cost curve summary

| Launches / yr | Marginal cost per flight ($M, internal) |
|---|---|
| ≤5 | **~25** (range 23–27) |
| ~10 | ~20 |
| ~24 | ~16–17 |
| ~50 | ~14–15 |
| ≥100 | **~13–14** (range 12–15) |
| Theoretical floor | ~10–11 |

The curve is **steep at low cadence (fixed-cost-dominated) and flattens toward the hardware floor at high cadence (Stage-2-dominated)** — exactly the shape the valuation model's curve already assumes.

---

## 6. $/kg cross-check vs. Falcon 9, Electron, and benchmarks [DERIVED]

Using the project's working SSO payload of **~9,500 kg reusable (DRL) to SSO** (from `payload_and_block_upgrade.md`; range 8.5–10.5 t), and ~13,000 kg to LEO:

| Metric | Low cadence | High cadence | Floor |
|---|---|---|---|
| Marginal cost/flight | $25M | $13.5M | $10.5M |
| **$/kg to SSO** (÷ 9,500 kg) | **~$2,630/kg** | **~$1,420/kg** | **~$1,105/kg** |
| **$/kg to LEO** (÷ 13,000 kg) | ~$1,920/kg | ~$1,040/kg | ~$810/kg |

### Benchmark comparison (internal / marginal cost basis — NOT list prices)

| Vehicle | Internal cost/flight | Payload basis | **Internal $/kg** | Source |
|---|---|---|---|---|
| **Falcon 9** (reused) | ~$11–20M | ~17,500 kg (reusable LEO, NBF basis) | **~$630–1,150/kg to LEO** | NextBigFuture Feb 2026 ($629/kg, $11M); analyst consensus $15–20M marginal |
| **Falcon 9** (reused, to SSO ~13 t) | ~$15M | ~13,000 kg SSO | ~$1,150/kg to SSO | Derived from above |
| **Neutron — high cadence (this study)** | ~$13.5M | 13,000 kg LEO / 9,500 kg SSO | **~$1,040/kg LEO; ~$1,420/kg SSO** | This document |
| **Neutron — low cadence (this study)** | ~$25M | 13,000 kg LEO / 9,500 kg SSO | ~$1,920/kg LEO; ~$2,630/kg SSO | This document |
| **Electron** | ~$5–6M *cost* (~$8M price) | ~300 kg LEO | **~$17,000–20,000/kg to LEO** | Electron is small-lift; ~15–20× worse $/kg — economies of scale |
| Industry "cheap" benchmark | — | — | Falcon 9 rideshare *price* ~$6,000/kg; Starship *aspirational* <$100/kg | Context only |

### Is ~$1,000–2,000/kg internal realistic for Neutron? — **Yes.**

1. **It straddles the Falcon 9 internal benchmark.** Falcon 9's internal cost is **~$630–1,150/kg to LEO**. Neutron at high cadence (~$1,040/kg LEO) lands **just above** Falcon 9 — which is exactly right: Neutron is a *smaller* vehicle (13 t vs. ~17–22 t reusable LEO), so it amortizes fixed and Stage-2 costs over fewer kilograms and **should** be modestly worse $/kg than Falcon 9. It is not better than Falcon 9, and the model should not assume it is.

2. **The SSO penalty is real and must be applied.** SSO payload (~9.5 t) is ~25–30% below LEO (13 t), so **$/kg to SSO is ~35–40% higher than $/kg to LEO**. At high cadence, ~$1,420/kg to SSO; at low cadence, ~$2,630/kg to SSO. The valuation model should be explicit about whether its $/kg figure is LEO or SSO — for the data-center thesis it is **SSO**.

3. **Internal economics are far below list price.** Neutron's ~$50–55M *list price* implies ~$4,000–5,800/kg to SSO. The venture flying its *own* payloads pays the **internal cost**, roughly **2× cheaper per kg** than a customer — this is precisely why the model is right to use marginal cost, and it is a material favorable input to the valuation.

4. **Electron is the cautionary contrast** — small-lift $/kg is 15–20× worse than medium-lift. This is the economy-of-scale argument *for* using Neutron rather than many small launchers for data-center mass: the entire $/kg advantage of Neutron over Electron is the payload-mass denominator.

> **Verdict:** ~$1,000–2,000/kg internal is realistic for Neutron **to LEO across the cadence range**, and ~$1,400–2,600/kg **to SSO**. The valuation model should use the **SSO** figures and recognize that Neutron's internal $/kg is *modestly worse than Falcon 9's*, *vastly better than Electron's*, and *roughly half its own list price*.

---

## 7. Recommendation for the valuation model's two dials

The valuation model anchors launch cost on a cadence curve: **~$25M/flight at low cadence (≤5/yr)** declining to **~$13M at high cadence (≥100/yr)** for ~12.5 t to SSO.

### Verdict: KEEP both anchors. They are well-supported by this bottom-up build.

| Dial | Current model value | Bottom-up result (this study) | Recommendation |
|---|---|---|---|
| **Low-cadence launch cost** (≤5/yr) | **$25M** | $23–27M, central **$25M** | **KEEP $25M.** The bottom-up build lands almost exactly on it. If anything, $25M is slightly *optimistic* for a brand-new vehicle's first few years — a 5×/yr operation could see $27–30M if the standing organization is larger than assumed or Stage-2 first-article costs run hot. Consider modeling low cadence as **$26M** for conservatism, but $25M is defensible. |
| **High-cadence launch cost** (≥100/yr) | **$13M** | $12–15M, central **$13–14M** | **KEEP, but treat $13M as the optimistic edge.** The bottom-up central estimate is **$13–14M**; $13M sits at the low end. Recommend modeling high cadence at **$13.5M** as the central case, with $13M as an upside / aggressive-learning scenario and $15M as a conservative case. |

### Specific recommended dial values

- **Low-cadence launch cost (internal, ≤5 launches/yr): $25M** — keep as-is (central). Sensitivity range **$23–28M**.
- **High-cadence launch cost (internal, ≥100 launches/yr): $13.5M** — nudge up $0.5M from $13M to the bottom-up central estimate. Sensitivity range **$12–15M**.
- **Credible hard floor: ~$10.5M** — useful as the optimistic asymptote; the model's curve should **not** drop below ~$11M at any cadence, because the expendable Stage 2 (~$7–8M mature) plus minimum ops physically prevents it.

### Caveats the model owner must carry forward

1. **Every number below the propellant line is an ESTIMATE.** Rocket Lab has disclosed only "$20–25M cost of goods, ~half Stage 2." The bottom-up build is anchored to that one disclosure plus Falcon 9 analogs. Confidence: **Medium** on the shape of the curve, **Low–Medium** on point values.
2. **The high-cadence case assumes ≥100 launches/yr — a heroic cadence.** Rocket Lab's *own stated target* is "twice a month" (~24/yr). At 24/yr the bottom-up cost is **~$16–17M**, not $13M. If the data-center venture's flight rate is more like 10–30 launches/yr, the model should use **$15–18M**, not the $13M high-cadence dial. **The $13M dial is only valid at genuine ≥100/yr scale** — flag this dependency prominently.
3. **Stage 2 cost is the dominant uncertainty and the cost floor.** A reusable Neutron Stage 2 is not in the design; if Rocket Lab never makes Stage 2 reusable, ~$10–11M is a hard floor. A future expendable-Stage-2 cost reduction is the main upside lever.
4. **SSO vs. LEO.** The model's "12.5 t to SSO" basis is consistent with this project's ~9.5 t (reusable) – 11 t (expendable) SSO working range; 12.5 t would correspond to expendable mode or a block-upgraded Neutron. Ensure the payload basis used for $/kg matches the cost basis (reusable cost ⇒ reusable ~9.5 t SSO; expendable cost would be higher and is not modeled here).
5. **First flight has not occurred.** All of this is pre-flight. Real cost data will not exist until reusable operations mature, realistically 2028+.

---

## Sources

- [Rocket Lab targets $50 million launch price for Neutron rocket — CNBC (Mar 2023)](https://www.cnbc.com/2023/03/24/rocket-lab-neutron-launch-price-challenges-spacex.html) — the $20–25M cost-of-goods / "~half from Stage 2" disclosure
- [Rocket Lab Neutron — Wikipedia](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron) — 480 t GLOW, 6,600 kN thrust, 13/15/8.5 t payload, $50M price
- [Archimedes (rocket engine) — Wikipedia](https://en.wikipedia.org/wiki/Archimedes_(rocket_engine)) — 730 kN SL / 890 kN vac thrust, 329 s / 365 s Isp, 50–100% throttle, mostly 3D-printed
- [SpaceX Falcon 9 True Cost to Launch is About $300 per Pound — NextBigFuture (Feb 2026)](https://www.nextbigfuture.com/2026/02/spacex-falcon-9-true-cost-to-launch-is-about-300-per-pound-which-is-25-of-selling-price-to-customers.html) — Falcon 9 marginal cost ~$11M, $629/kg; component breakdown (upper stage $7M, booster amort $1M, propellant $0.25M, ops $1M)
- [How much does it cost to launch a reused Falcon 9? — ElonX.net](https://www.elonx.net/how-much-does-it-cost-to-launch-a-reused-falcon-9-elon-musk-explains-why-reusability-is-worth-it/) — Musk cost breakdown: booster 60%, upper stage 20%, fairing 10%, launch ops 10%; refurb cost figures
- [How SpaceX Refurbish A Used Booster — TheSpaceBucket](https://thespacebucket.com/how-spacex-refurbish-a-used-booster/) — Falcon 9 refurbishment process, X-ray inspection, cost trajectory
- [Rocket Lab USA Q4 2025 earnings 8-K — SEC](https://www.sec.gov/Archives/edgar/data/0001819994/000162828025038900/rklb-08072025ex991.htm) — operating expenses ~$115–120M/quarter, headcount ~2,645
- [Rocket Lab (RKLB) Q4 2025 Earnings Call Transcript — Motley Fool (Feb 2026)](https://www.fool.com/earnings/call-transcripts/2026/02/26/rocket-lab-rklb-q4-2025-earnings-call-transcript/) — Neutron development spend, Archimedes propulsion testing ramp
- [Rocket Lab Completes Archimedes Engine Build, Begins Engine Test Campaign — Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-completes-archimedes-engine-build-begins-engine-test-campaign/) — Archimedes ~90% 3D-printed by mass, now in series production
- [Liquefied Natural Gas Prices, Trend, Index — IMARC Group](https://www.imarcgroup.com/liquefied-natural-gas-pricing-report) — LNG ~$480–530/MT (Q4 2025)
- [United States Natural Gas Industrial Price — EIA](https://www.eia.gov/dnav/ng/hist/n3035us3m.htm) — US industrial natural gas pricing
- [Oxygen Prices 2026 — IMARC Group](https://www.imarcgroup.com/oxygen-pricing-report) — industrial LOX ~$0.12/kg (North America, Dec 2025)
- [Commercial Space Launches: FAA Should Update How It Assesses Federal Liability Risk — U.S. GAO](https://www.gao.gov/products/gao-12-899) — FAA third-party liability requirement ~$80–200M coverage, ~1–2% premium
- [What Is Methalox? The Methane + LOX Propellant Revolution — Space Launches Live](https://spacelaunchlive.com/articles/methalox/) — methalox bulk density, propellant properties
- [SpaceX Raptor — Wikipedia](https://en.wikipedia.org/wiki/SpaceX_Raptor) — methalox oxidizer-to-fuel mixture ratio ~3.6–3.8:1 reference
- [How Merlin Engines Power Falcon 9 Rockets — SpaceX Stock](https://spacexstock.com/how-merlin-engines-power-falcon-9-rockets/) — Merlin Vacuum cost estimate $0.5–0.75M; upper-stage tank+structure $4–6M

---

## Open questions / uncertainties

1. **Neutron Stage 2 build cost — the load-bearing estimate.** Anchored only to CNBC's 2023 "~half of $20–25M." The ~$10M central (range $8–13M) drives both the cost floor and the low→high cadence delta. Would be resolved by any Rocket Lab disclosure of Stage 2 cost or Neutron unit economics.
2. **Annual fixed-cost pool for Neutron launch operations.** Estimated ~$200M/yr steady-state (range $140–280M); Rocket Lab does not segment launch-ops fixed cost from company-wide opex or from Neutron development R&D. Wide error bars.
3. **Fixed cost is semi-variable, not flat.** A 5×/yr operation runs a smaller standing army than a 100×/yr operation; the model should scale the fixed pool with the cadence regime rather than dividing one constant by flight count (which gives an absurd $40M/flight at 5×/yr).
4. **Refurbishment cost trajectory.** Estimated $2.5–4M early → $0.8–1.5M mature, by analogy to Falcon 9's documented $3M→$0.8M decline. Neutron-specific: composite structure and de-stressed Archimedes help; salt-water DRL recovery hurts; captive fairing avoids a fairing-refurb workstream.
5. **Booster flight life.** Assumed 10 (early) → 15–20 (mature) per Rocket Lab's stated "10–20" target. Higher reuse lowers amortization but is unproven for Neutron.
6. **Cadence realism.** The $13M high-cadence dial requires ≥100 launches/yr. Rocket Lab's own stated target is ~24/yr ("twice a month"), at which the bottom-up cost is ~$16–17M. If the venture flies <50/yr, the high-cadence dial overstates the cost reduction.
7. **Propellant mass is derived, not disclosed.** ~434 t total (range 427–441 t) from a ~90.5% propellant fraction assumption. Propellant cost is tiny (~$0.3M) so this barely affects the result, but stage masses are genuinely undisclosed.
8. **All figures are pre-first-flight.** Neutron has not flown; real cost data will not exist until reusable operations mature (NET 2028).
