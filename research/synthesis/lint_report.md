# Lint Report — Knowledge-Base Health Check

*Date: 2026-05-17. Prepared by the "lint" agent (Karpathy-style wiki health pass).*
*Scope: all ~21 project documents. This report does NOT edit any document — it only
diagnoses. Every finding cites file paths and quotes the conflicting text.*

> **Superseded by later passes (2026-05-17).** This is **lint pass 1**, run
> before `CONCLUSION.md` existed. Its three priority fixes (radiator area, node
> mass re-baseline, SSO figure) were subsequently applied and folded into thesis
> Rev 2.1 and the wave-5 work. A second pass (`synthesis/lint_report_2.md`) and
> a four-agent peer review (`peer_review/`) supersede it. Read it as a dated
> health snapshot — the **current project state is `CONCLUSION.md` (Rev 7)** and
> the live fix-status is tracked in `peer_review/triage_and_fix_plan.md`.

---

## 0. Summary — how healthy is the wiki?

**Overall: structurally healthy, but numerically out of date.** Navigation is good
(README → LIBRARY → RESEARCH_TRACKER → docs is consistent), no documents are orphaned,
and no markdown links are broken. The research is thorough and honestly hedged.

**But the wave-3 node mass model (`node_design/node_mass_model.md`) silently
invalidates the headline numbers in every wave-1 and wave-2 summary document** —
radiator area, solar area, per-node mass, racks-per-launch, and the Neutron SSO budget.
The tracker even flags this ("⚠ contradicts thermal doc on radiator area") but the
contradiction was never reconciled and the summary docs (`preliminary_findings.md`,
`initial_thesis.md` Rev 2, `LIBRARY.md`) were never updated. A reader starting at the
thesis or LIBRARY today gets numbers the project's own latest research has superseded.

**Biggest single issue: the radiator-area contradiction (≈120–210 m² vs ≈430 m² per
rack).** It is not cosmetic — it cascades into node mass, racks-per-launch, and the
feasibility margin. It is reconciled in detail in §1 below.

**Health scorecard:**

| Category | State |
|---|---|
| Navigation / structure | Good — no orphans, no broken links |
| Internal consistency of detailed docs | Fair — one major (radiator) + several numeric conflicts |
| Top-level docs vs. detailed docs | **Poor — thesis Rev 2 & preliminary_findings are stale** |
| Backlog / gap tracking | Fair — several raised questions untracked |

---

## 1. Contradictions

### 1.1 ⚠ PRIMARY ISSUE — Radiator area per rack: ~120–210 m² vs ~430 m²

Two documents give incompatible radiator sizing for the same ~130–155 kW rack.

- `orbital/thermal_analysis.md` (wave 1), Summary and §1:
  > "a one-rack node realistically needs **~120-210 m²** of radiator (double-sided),
  > not 370-540 m²."
  Its §1 table gives 143 m²/rack at 130 kW and 170 m²/rack at 155 kW for a ~67 °C
  radiator.

- `node_design/node_mass_model.md` (wave 3), §4(b):
  > "**Radiator area needed** = 150,000 W ÷ ~350 W/m² ≈ **~430 m²** of radiator per
  > rack (range ~375–500 m²)."
  And §4 explicitly: "prior radiator ~120–210 m²/rack looks low."

This is a **~2.5–3× disagreement** on the single biggest mass/area driver in the
project.

**Why they differ — the reconciliation:**

The gap is almost entirely the **assumed radiator surface temperature and how the
"double-sided" factor is applied**, not a math error:

1. **Hot-loop temperature assumption.** `thermal_analysis.md` assumes the *radiator
   surface itself* runs at ~330–355 K (60–80 °C) — i.e. it assumes the chip-to-panel
   thermal gradient is small. `node_mass_model.md` assumes a 60–90 °C *liquid loop*
   but a radiator *surface* of only ~323 K (50 °C), explicitly modeling a "drop from
   loop to surface." Stefan-Boltzmann is a T⁴ law, so 340 K vs 323 K alone changes
   flux by ~30–40%.

2. **Single- vs double-sided crediting.** `thermal_analysis.md` explicitly computes a
   **net 2-sided flux** (`q = 2·ε·σ·(T⁴−T_sink⁴)`), reaching ~910 W/m² at 340 K.
   `node_mass_model.md` computes a **gross one-face flux** (~336 W/m²) and then
   *discounts* the second face ("one face often has a poor view... assume an effective
   ~300–400 W/m²"). So one doc multiplies by ~2 for the back face; the other nearly
   cancels it. This single modeling choice is most of the 2.5× gap.

3. **Both use the same 250 K sink** — that is consistent and not the cause.

**Which is right / what the project should adopt:** Neither figure is "wrong"; they
bracket the same physics under optimistic vs. conservative assumptions. The honest
status is **the radiator surface temperature and the usable-second-face credit are
unresolved**, and that is exactly what `preliminary_findings.md` §4 item 3 already
flagged as a load-bearing unknown. Recommended interim project number: **adopt a
range of ~200–430 m²/rack and stop quoting "120–210 m²" as settled.** The mid/working
planning figure should be **~300 m²/rack** until a real chip→coolant→panel
thermal-resistance model is built (the action both docs call for). Critically:
`node_mass_model.md` is the **later, more conservative, and more explicitly
reasoned** document — its caution ("prior radiator/solar area estimates were low")
should be treated as the current project position, and the wave-1 thermal doc's
"120–210 m²" should be considered **superseded on the low end**.

**Knock-on effect:** because radiator mass is "the second-biggest mass line," this
also drives the node-mass contradiction in §1.3 and the racks-per-launch
contradiction in §1.4.

### 1.2 Neutron SSO payload: ~10 t vs ~8.5 t reusable

> **Superseded (wave-5, 2026-05-17):** this section's recommendation to
> standardize on "~8.5–9 t reusable" has itself been superseded. Wave 5's
> deep-verification doc re-baselined the SSO working figure to **~9.5 t (range
> 8.5–10.5 t)** — see `rocket_lab/neutron/payload_and_block_upgrade.md` and
> lint pass 2 (`synthesis/lint_report_2.md` §1.1).

Three docs carry three different working numbers off the *same* published 13 t
LEO-DRL baseline:

- `orbital/orbits_environment.md` §2: "**~10 t reusable** is used as the working
  number" (25–30% penalty).
- `synthesis/preliminary_findings.md` §1 and `vision/initial_thesis.md` Rev 2:
  "estimated **~10 t reusable** Neutron SSO budget."
- `node_design/node_mass_model.md` §5: "The project's prior '~10 t reusable SSO
  payload' assumption is **optimistic**... Use **~8.5 t** as the reusable SSO mass
  budget."

`node_mass_model.md` also internally states downrange-landing SSO as "~9.5 t" in one
table and "~8.5–9.5 t" in another, then picks 8.5 t — a mild internal wobble.

All are flagged estimates, so this is not a factual error, but the **summary docs and
the latest detailed doc disagree on the working number**, and a ~1.5 t difference is
material against a ~6 t node. The project should pick one planning number (recommend
**~8.5–9 t reusable**, the more conservative and more recent value) and use it
everywhere, or explicitly state the band "~8.5–10 t."

Note `orbits_environment.md` §2 also says "**~8,000 kg RTLS**" for LEO while
`neutron_specs.md` says "**~8,500 kg RTLS**" — a small stale figure in the orbital doc.

### 1.3 Per-node mass: ~6 t / ~11 t vs ~5.4 t / ~9.6 t vs ~8.6 t feasibility-mid

- `orbital/thermal_analysis.md` §5 and `preliminary_findings.md`: "**~6 t** for a
  1-rack node, **~11 t** for a 2-rack node."
- `node_design/node_mass_model.md` headline: "**1-rack node ~5.4 t**, 2-rack
  **~9.6 t**" (mass-optimized path) — but its own §6 feasibility table gives a
  1-rack **mid of ~8.6 t** (range 5.6–14.1 t) and a 2-rack mid of **~16.6 t**.

So `node_mass_model.md` is internally double-voiced: a ~5.4 t headline and a ~8.6 t
"broader feasibility envelope" mid. The thesis/synthesis "~6 t" sits between them but
is closest to the *optimistic* end. The project should standardize on the
node_mass_model feasibility-mid ("design to ~7–9 t for a 1-rack node," per its own §6
recommendation) and treat sub-6 t as a stretch goal — and propagate that into the
summary docs, which currently imply ~6 t is the expected case.

### 1.4 Racks per Neutron launch: "~1–2 racks" vs "1 rack/node, 1 node/launch"

- `orbital/thermal_analysis.md` §5: "**~2 racks/launch**" working number; LIBRARY and
  RESEARCH_TRACKER repeat "~1–2 racks per Neutron SSO launch."
- `synthesis/preliminary_findings.md` and `initial_thesis.md` Rev 2 carry the 1–2 rack
  / 2-rack-node framing ("~11 t for 2-rack").
- `node_design/node_mass_model.md` §6 verdict: "**A 2-rack node almost certainly
  forces an expendable flight or exceeds Neutron entirely — it is not recommended as
  the baseline. The architecture should be one rack per node, one node per Neutron
  launch.**"

The latest research **rejects the 2-rack node** that the synthesis and thesis still
treat as a live option. This is a genuine architectural contradiction, not just a
number, and it is currently unreconciled in every summary doc.

### 1.5 Solar array area per rack: ~375–460 m² vs ~545 m² (GaAs) / ~750–900 m² (Si)

- `orbital/thermal_analysis.md` §4: "~150-185 kW → **~375–460 m²** of array."
- `node_design/node_mass_model.md` §3: "the prior 375–460 m² estimate looks
  optimistic; **expect ~500–550 m²/rack GaAs, ~750–900 m²/rack silicon**."

`node_mass_model.md` explicitly flags the wave-1 number as low. The summary docs
(`preliminary_findings.md` §5 strawman) still quote "375–460 m²" and "400–900 m²" —
stale on the low end. Note also that Rocket Lab's announced arrays are *silicon*
(per `overview.md` and `thermal_analysis.md` §4), so the **~750–900 m² silicon figure
is the realistic baseline**, yet the strawman implicitly uses the GaAs/ROSA numbers.

### 1.6 GB300 rack power: "~120 kW" vs "~135 kW TDP / ~155 kW peak"

`llm_compute/inference_scaling.md` §2 table lists **GB300 NVL72 at "~120 kW"**, while
`data_centers/ai_hardware.md` (§1.1, §2.2) and `node_mass_model.md` both establish
**~135 kW TDP / 132–140 kW typical / ~155 kW peak** and explicitly say "NVIDIA
marketing '~120 kW'... use the higher OEM numbers." The inference doc's table is using
the marketing figure that `ai_hardware.md` warns against. Minor (the inference doc is
about memory, not thermal) but it is an internal inconsistency on a core spec.

### 1.7 Fairing payload diameter: 5.0 m vs 5.5 m

`neutron_specs.md` treats **5.5 m** as current ("PUG v1.0... 5.5 m... treated as
current"). `node_mass_model.md` §5 table says "**up to 5.0 m, expandable to 5.5 m**"
and then does its packaging math on a "~5 m fairing / ~4.5 m usable diameter."
`preliminary_findings.md` §5 and `initial_thesis.md` Rev 2 say "**up to 5.5 m**."
LIBRARY's glossary doesn't commit. This is a known source disagreement (both docs flag
it), but the project quotes both values as fact in different places. Pick one
(recommend "up to 5 m standard, 5.5 m for non-standard payloads," which reconciles
both) and use it consistently.

---

## 2. Stale claims (superseded by later research, not yet updated)

### 2.1 Thermal is still called "the leading physics-wall candidate" in places

`RESEARCH_TRACKER.md` "Key findings so far" still contains the wave-1-era bullet:
> "**Heat rejection is the leading physics-wall candidate.** ... est. ~370–540 m² of
> radiator per rack."

This bullet was written before `thermal_analysis.md` and is contradicted by the very
next bullet in the same section ("Thermal is NOT a hard physics wall"). The tracker
keeps both the obsolete framing *and* its correction side by side. The 370–540 m²
figure is doubly stale — superseded first by thermal_analysis (120–210 m²) and then
re-expanded by node_mass_model (~430 m²). `LIBRARY.md` also still labels
`orbital/thermal_analysis.md` as "**the leading wall test**" and its key takeaway as
the wave-1 line. Recommend rewording these to the settled "thermal is a sizing/mass
problem, not a wall."

### 2.2 The founder's "+30% radiator-vs-solar area" rule — corrected but the
correction hasn't propagated

`node_mass_model.md` §4 and its open-questions §4 explicitly correct the founder
hypothesis recorded in `RESEARCH_TRACKER.md` ("Founder input — wave 3":
"radiators... need ~30% more area than the solar panels"):
> "the '+30%' rule of thumb is not supported. The correct statement: **radiator area
> ≈ 0.5–0.9 × solar area**."

This correction is **only** in `node_mass_model.md`. `RESEARCH_TRACKER.md` still
records the raw "+30%" founder input with the note "→ Research item 14 to
validate/correct" — but item 14 is now `draft`/done and *did* correct it, so the
tracker note should be closed out with the result. No summary doc records the
corrected ratio.

### 2.3 "~6 t / ~11 t node" in the synthesis and thesis is pre-node-mass-model

`preliminary_findings.md` §1, §5 and `initial_thesis.md` Rev 2 ("~6 t for 1-rack /
~11 t for 2-rack") predate `node_mass_model.md`. The node mass model is the
purpose-built doc that supersedes these stacked estimates (it is literally
synthesis recommendation §6 item 3 — "What does a real per-node mass model say?").
The synthesis still presents the ~6 t/~11 t numbers as current. Stale.

### 2.4 Radiator/solar/node numbers in `preliminary_findings.md` §3 wall table

The candidate-walls table in `preliminary_findings.md` §3 still cites
"~120–210 m²/rack (~0.5–1.5 t)" radiator and "~375–460 m²" array as the resolved
figures. Both are superseded per §1.1 and §1.5 above.

### 2.5 LIBRARY and tracker one-liners for the thermal and node docs

`LIBRARY.md` key takeaway for `thermal_analysis.md`: "~1–2 racks per Neutron SSO
launch" — superseded by node_mass_model's "1 rack/node, 1 node/launch." LIBRARY's
node_mass_model entry is correct ("1 rack/node, 1 node/launch") so LIBRARY is
internally inconsistent between two adjacent rows.

### 2.6 `economics/ai_datacenter_tam.md` — minor: not stale, but the only doc not
referenced by any later synthesis

Not a stale *claim*, but flagged here: the TAM doc's illustrative ~$0.3–30B/yr figure
is carried into LIBRARY and the tracker, yet `preliminary_findings.md` (the wave-1
synthesis) barely uses it — understandable since synthesis is physics-first, but worth
noting the market doc is under-integrated.

---

## 3. Consistency of the top-level docs

**`vision/initial_thesis.md` (Rev 2)** — mostly sound in narrative, stale in numbers:
- ✅ The "no physics wall," "whole racks," "build to learn," "hubs not homes,"
  dawn-dusk SSO framing all still match the detailed docs.
- ❌ "~6 t for 1-rack / ~11 t for 2-rack vs ~10 t reusable SSO budget" — all three
  numbers superseded (§1.2, §1.3).
- ❌ Treats a **2-rack node** as a live option ("one Neutron launch delivers one
  complete node (~1–2 racks)"); `node_mass_model.md` rejects it (§1.4).
- ⚠ "up to 5.5 m" fairing diameter — see §1.7.
- ⚠ Says nodes carry "two rack roles (compute + networking)" as adopted architecture;
  this is still only a founder hypothesis / open research item — no doc has sized it
  (see §5.1). Rev 2 states it more firmly than the evidence supports.

**`synthesis/preliminary_findings.md`** — explicitly a "wave 1" doc, and it shows:
- It is honest that it is wave-1 ("Synthesis of research wave 1"), but it is still
  the doc LIBRARY points readers to for "what the research adds up to," and it has not
  been re-synthesized after waves 2–3 (orbit primer, RF limited service, node mass
  model). Its strawman §5 numbers (radiator, solar, node mass, 2-rack node) are all
  superseded by `node_mass_model.md`.
- Its §6 "recommended next wave" item 3 ("What does a real per-node mass model say?")
  has since been *answered* by `node_mass_model.md` — but nothing closes that loop.
- **No wave-2/wave-3 synthesis exists.** RESEARCH_TRACKER S2 ("full feasibility
  evaluation") is `planned`. So the most current synthesis a reader finds is wave-1,
  pre-dating three of the project's docs.

**`README.md`** — still accurate and high-level enough to be safe; it deliberately
defers to the thesis and tracker. Only nit: "Status: foundational research agents
running" is stale — waves 1–3 are essentially complete. Minor.

**`LIBRARY.md`** — see §2.5; internally inconsistent on racks-per-launch between the
thermal-doc row and the node-doc row. Otherwise the catalog is complete and correct.

**Bottom line for §3:** the *narrative* of the top-level docs survives; the *numbers*
do not. A reader who trusts the thesis/synthesis will quote radiator area, solar area,
node mass, racks-per-launch, and the SSO budget that the project's own latest doc has
revised. This is the single most important thing to fix.

---

## 4. Orphans & broken references

**Good news: no orphaned documents and no broken links found.**

- All 21 files are catalogued in `LIBRARY.md` and (except the framing docs and
  LIBRARY/README/tracker themselves) tracked in `RESEARCH_TRACKER.md` rows 1–14 + S1.
- All relative markdown links checked resolve to existing files: README↔LIBRARY↔
  tracker cross-links, `initial_thesis.md`'s links to `../RESEARCH_TRACKER.md` and
  `../synthesis/preliminary_findings.md`, and the many `(./rf_satcom.md)`-style
  inline links in the laser_comms docs.
- Inline doc-name references (`thermal_analysis.md`, `orbits_environment.md`,
  `inference_scaling.md`, etc.) in the synthesis and thesis all correspond to real
  files.

**Minor issues:**

- **Both `orbital/orbits_environment.md` and `orbital/thermal_analysis.md` are titled
  "Doc 6 of foundational research."** thermal_analysis adds "(companion)," but two
  docs sharing a number is mildly confusing for an index. The RESEARCH_TRACKER lists
  them as items 6 and 7. Cosmetic.
- **`RESEARCH_TRACKER.md` row S2** points to "synthesis/" (a directory, not a file)
  with status `planned`. Not broken, but it is a tracker row without a doc — expected
  for a planned item, just noting it.
- **`orbit_types_primer.md` is item 12** and well-integrated, but neither
  `preliminary_findings.md` nor `initial_thesis.md` references the GEO-relay-vs-LEO-
  mesh trade it raises (see §5.4) — the doc is linked but its main open question is
  orphaned from the synthesis.
- All external URLs are numerous; not validated for liveness (out of scope), but their
  formatting is consistent and correct.

---

## 5. Gaps — raised in a doc but not tracked in the backlog

`RESEARCH_TRACKER.md`'s "Open research questions (backlog)" is largely a pre-wave-1
list and has **not been updated** with questions raised by waves 1–3. Notable gaps:

### 5.1 Compute-rack vs. networking-rack split — raised, promised, never tracked
Founder input (tracker), `preliminary_findings.md` §5/§6 item 4, and
`initial_thesis.md` Rev 2 all call for sizing the "two rack roles." No backlog item,
no assigned doc. The thesis Rev 2 actually *asserts* the two-role architecture as
adopted while the work to size it has not been done — a gap and a slight
overstatement.

### 5.2 GPU/HBM lifetime under a hot loop — flagged repeatedly, not in backlog
`preliminary_findings.md` §3 and §6 item 8, `ai_hardware.md`, `thermal_analysis.md`,
and `starcloud.md` all flag the hot-radiator-vs-silicon-longevity / replacement-cadence
trade as UNRESOLVED. The tracker backlog has a "Radiation" bullet but nothing on
thermal-driven device lifetime / servicing cadence.

### 5.3 Deployment mechanics & stowed packaging of large radiators/arrays
`preliminary_findings.md` §3 lists "Deployment mechanics" as UNRESOLVED;
`thermal_analysis.md` and `node_mass_model.md` §7 both call the ~430 m² deployable
radiator "the biggest open risk." `node_mass_model.md` partly addressed packaging, but
the *mechanical deployment reliability* of an ISS-larger radiator is untracked in the
backlog.

### 5.4 Relay architecture: GEO relay vs. LEO mesh vs. ground-station diversity
`orbit_types_primer.md` §6 and its open questions explicitly call this "a genuine
design fork" / "unresolved." `optical_comms.md` and `optical_ground_stations.md`
resolve the *ground-station* side (diversity) but the **GEO-relay-vs-LEO-mesh decision
for continuous connectivity** is not in the tracker backlog and not in any synthesis.

### 5.5 Pumped fluid-loop / heat-pipe mass
`thermal_analysis.md` open questions and `preliminary_findings.md` §4 item 6 both say
the pumped-loop mass is "folded into the bus line crudely" and needs a dedicated
estimate. `node_mass_model.md` carries "+150–400 kg/rack" but still calls it
uncertain. Not a discrete backlog item.

### 5.6 The "GB300 1.36 t scope" definitional question
`node_mass_model.md` open question 8 raises a real risk: if the project's "intact
rack" includes the separate NVLink-switch / CDU / PDU sub-racks, per-rack mass rises
to ~2.5–3 t and "every figure scales up." This is a foundational definitional gap that
should be resolved before any further mass work — not currently tracked.

### 5.7 Economics
The tracker backlog has an "Economics" bullet and `preliminary_findings.md` §6 item 10
defers it — so this one *is* acknowledged. Noted only for completeness: it remains the
largest unstarted workstream and S2 depends on it.

### 5.8 Eclipse-season battery vs. throttle trade
`thermal_analysis.md`, `orbits_environment.md`, and `starcloud.md` open questions all
raise the dawn-dusk eclipse-season battery-sizing question; no backlog entry.

---

## 6. Prioritized fix list

Ordered by importance (impact on the integrity of the project's conclusions).

**P1 — Reconcile the radiator area (and propagate it).** Resolve §1.1: adopt a single
project radiator-area position. Recommended: state **~200–430 m²/rack, working
~300 m²**, explicitly mark "120–210 m²" as a superseded optimistic bound, and make the
chip→coolant→panel thermal-resistance model an explicit P1 research item. Update
`thermal_analysis.md`, `preliminary_findings.md` §3/§5, `initial_thesis.md` Rev 2,
`LIBRARY.md`, and `RESEARCH_TRACKER.md` key-findings.

**P2 — Re-baseline the node-mass / racks-per-launch story to the node mass model.**
Make `node_design/node_mass_model.md` the authoritative source: **1 rack/node, 1 node/
launch; design to ~7–9 t for a 1-rack node; drop the 2-rack node as a baseline.**
Update `preliminary_findings.md` §1/§5, `initial_thesis.md` Rev 2 ("~1–2 racks"),
`LIBRARY.md` (thermal-doc row), and `RESEARCH_TRACKER.md`. This resolves §1.3 and §1.4.

**P3 — Pick one Neutron SSO working number.** Resolve §1.2: standardize on
**~8.5–9 t reusable** (or an explicit "~8.5–10 t" band) across `orbits_environment.md`,
`neutron_specs.md`-adjacent text, `node_mass_model.md`, `preliminary_findings.md`, and
`initial_thesis.md`. Fix the "~8,000 kg RTLS" vs "~8,500 kg RTLS" mismatch.

**P4 — Write a wave-2/3 synthesis (or revise `preliminary_findings.md`).** The current
synthesis is wave-1 only and predates 3 docs. Either produce the planned S2 or issue a
"preliminary_findings Rev 2" that folds in the node mass model, orbit primer, RF
limited-service, and optical-ground-station findings. This is the structural fix that
prevents the staleness in §2–§3 from recurring.

**P5 — Purge the stale "leading physics-wall candidate" / 370–540 m² language.** Edit
`RESEARCH_TRACKER.md` "Key findings" and `LIBRARY.md`'s `thermal_analysis.md` row so
the obsolete wall framing and the 370–540 m² figure no longer sit next to their own
corrections (§2.1).

**P6 — Close out the corrected founder hypotheses in the tracker.** Mark the "+30%
radiator-vs-solar" founder input as *resolved → radiator ≈ 0.5–0.9 × solar area*
(§2.2), and record the node-mass-model result against tracker item 14.

**P7 — Refresh the backlog.** Add the untracked gaps from §5: rack-role split (5.1),
hot-loop GPU lifetime / servicing cadence (5.2), radiator deployment mechanics (5.3),
GEO-relay-vs-LEO-mesh decision (5.4), fluid-loop mass (5.5), the "1.36 t rack scope"
definition (5.6), and the eclipse battery/throttle trade (5.8). Resolve 5.6 first — it
can rescale every mass figure.

**P8 — Minor consistency cleanups.** Fix GB300 "~120 kW" in `inference_scaling.md` to
~135 kW (§1.6); standardize fairing diameter wording (§1.7); de-duplicate the "Doc 6"
title shared by the two orbital docs; refresh README's "research agents running"
status line.

---

## 7. What is genuinely solid (so fixes don't overcorrect)

For balance — these hold up well across all waves and need no change:
- The inference-not-training thesis and "one rack serves one frontier model" — robust,
  multi-sourced, internally consistent across `inference_scaling.md`, `ai_hardware.md`,
  synthesis, and thesis.
- The dawn-dusk SSO orbit choice and benign-radiation finding — consistent everywhere.
- The optical-primary / RF-backup comms conclusion, including the wave-3 "limited RF
  sliver" refinement, which correctly and explicitly refines (not contradicts)
  `rf_satcom.md`.
- The "diversity beats aperture" ground-station finding and the correction of the
  founder's "monster ground station" idea — cleanly handled.
- Navigation and sourcing discipline — strong throughout.

The project's *direction* is well-supported. The problem is purely that its newest
quantitative research has not been folded back into its older summary documents.
