# Lint Report 2 — Post-Wave-5 Knowledge-Base Health Check

*Date: 2026-05-17. Prepared by the "lint" agent (second Karpathy-style wiki health pass,
following `synthesis/lint_report.md`).*
*Scope: all ~30 project documents — framing/index, vision, 5 syntheses, ~24 research docs,
and the 2 model REPORTs. This report does NOT edit any document; it only diagnoses, with
file paths and quoted text.*

> **Superseded by the conclusion and the peer review (2026-05-17).** This is
> **lint pass 2**, written *before* `CONCLUSION.md` was drafted — §0/§6 frame it
> as "the checklist that prevents" a conclusion built on stale numbers. The
> conclusion has since been written and revised through Rev 7, and a four-agent
> peer review (`peer_review/`) re-audited the whole corpus. Its P1–P8 fix list
> was largely applied (SSO re-baseline propagated, LIBRARY catalog completed,
> README counts corrected); any residual items were carried into and resolved by
> the peer-review pass — see `peer_review/triage_and_fix_plan.md`. Read this as a
> dated health snapshot; the **current project state is `CONCLUSION.md` Rev 7**.

---

## 0. Summary — how healthy is the wiki?

**Overall: structurally sound, navigationally clean, but numerically out of date in a
specific, systematic way — and the staleness is worse than after lint pass 1 because it
now spans the two simulation REPORTs as well as the older research docs.**

Lint pass 1 fixed the wave-1/wave-3 reconciliation (radiator area, node mass, the ~10→8.5 t
SSO correction). Since then **wave 5 re-baselined two load-bearing numbers a second time**,
and the propagation is incomplete:

1. **The Neutron reusable SSO payload moved again — ~8.5 t → a working ~9.5 t (band
   8.5–10.5 t)** in `rocket_lab/neutron/payload_and_block_upgrade.md`. The two top-level
   syntheses (wave 5) and the thesis Rev 4 adopt ~9.5 t, but **at least eight other
   documents — including both simulation REPORTs, every earlier research doc that quotes an
   SSO figure, `RESEARCH_TRACKER.md`'s key-findings block, and `LIBRARY.md` — still carry
   the stale ~8.5–9 t (or older ~10 t) figure.**
2. **The flyability ceiling is quoted at three different un-reconciled values across the
   models and docs** — simulation ~214 kW, data-science ~163 kW, hot-chip doc ~260–320 kW —
   while only the wave-5 synthesis and thesis Rev 4 carry the reconciled
   ~200–250 / ~270–320 / ~430–470 kW set. Both REPORTs explicitly flag the discrepancy as
   "reconcile in synthesis" — the synthesis did so, but the REPORTs were never annotated.

**Biggest single issue: the ~8.5 t → ~9.5 t SSO re-baseline has not propagated.** It is not
cosmetic — it is the single most decision-relevant number in the project. The simulations'
headline result ("a 1-rack node stops flying at ~214 kW") is computed against the *stale*
8.5 t budget; the wave-5 synthesis itself re-derives ~250 kW at 9.5 t. A reader who opens
`simulations/REPORT.md` or `data_science/REPORT.md` — both `draft`/done and prominently
linked from the tracker — gets a flyability verdict the project's own latest research has
superseded by ~40–90 kW.

**A second, structural issue:** the conclusion document (`RESEARCH_TRACKER.md` row S2,
status `planned`) is about to be written. If it is written off the tracker's stale
key-findings block rather than off wave-5 synthesis, it will inherit ~8.5 t, the
un-reconciled ceiling, and the retired $3.3B/GW proxy. **This report exists to be the
checklist that prevents that.**

**Health scorecard:**

| Category | State |
|---|---|
| Navigation / structure | Good — no orphans, no broken links found |
| Internal consistency of detailed research docs | Fair — wave-5 numbers not back-propagated to waves 1–4 docs |
| Models (`simulations/`, `data_science/`) vs. wave-5 synthesis | **Poor — both REPORTs carry pre-wave-5 SSO budget and un-reconciled ceiling** |
| Top-level docs (thesis Rev 4, wave-5 synthesis, README, LIBRARY) | **Mixed — thesis & wave-5 synthesis current; README & LIBRARY stale** |
| Backlog / gap tracking | Fair — wave-5 open questions only partially folded in |

---

## 1. Contradictions & numerical staleness

### 1.1 ⚠ PRIMARY ISSUE — the Neutron reusable SSO payload: ~9.5 t vs. ~8.5 t vs. ~10 t

Wave 5's deep-verification doc re-baselined the figure. The **current project position** is:

- `rocket_lab/neutron/payload_and_block_upgrade.md` §2, §6: **"Use ~9,500 kg (range
  8,500–10,500 kg) reusable-to-SSO as the baseline node mass budget"**; expendable ~11 t;
  block-upgraded ~12–13 t.
- `synthesis/wave5_synthesis.md` §2.1 adopts it: *"Reusable (downrange/barge landing) —
  baseline ~9.5 t (range 8.5–10.5 t)."*
- `vision/initial_thesis.md` Rev 4 adopts it: *"a corrected ~9.5 t SSO payload."*

**Documents that still carry a STALE SSO figure** (every one of these should be updated, or
explicitly annotated as superseded, before the conclusion doc is written):

| Document | Stale text | Correct figure |
|---|---|---|
| `simulations/REPORT.md` §2 inputs table, §4, §5 | "Neutron SSO mass budget – reusable (downrange) **8.5 t**"; headline "stops flying at **~214 kW**" computed at 8.5 t | ~9.5 t → ceiling re-derives to ~250 kW (wave-5 §2.2) |
| `data_science/REPORT.md` §2, §3, throughout | "1-rack node mass crosses Neutron's **~8.75 t** reusable SSO ceiling at a rack power of only ~163 kW" | ~9.5 t → ~163 kW was "the pessimistic corner" per wave-5 §2.2 |
| `orbital/orbits_environment.md` Summary, §2, §3, Open Qs | "**~10 t reusable** … carries ~10 t as the working SSO number"; table "~9.0–11.0 t (carry ~10 t)" | Superseded twice — now ~9.5 t (8.5–10.5 t band) |
| `orbital/thermal_analysis.md` §5, Open Qs | "Neutron SSO budget ≈ **10 t**"; per-launch budget sketch and "1–2 racks/launch" both computed at 10 t | ~9.5 t; and racks-per-launch already corrected to 1 by lint pass 1 |
| `node_design/node_mass_model.md` §5, §6, Open Q1 | "Use **~8.5 t** as the reusable SSO mass budget"; §6 comparison table header "~8.5–9.5 t" | ~9.5 t working (8.5–10.5 t) — note this doc *predates* item 23 |
| `node_design/solar_radiator_trajectory.md` §4.5 | "a reusable SSO budget is **~8.5 t** (downrange recovery; `node_mass_model.md` §5)" | ~9.5 t |
| `node_design/rack_internals.md` §5 | "mass-constrained against Neutron's **~8.5–9 t** reusable SSO budget" | ~9.5 t (8.5–10.5 t) |
| `RESEARCH_TRACKER.md` row 6, "Key findings so far" (2 bullets), row M2 note | "Est. **~8.5-9 t** reusable to SSO (lint-corrected from ~10 t)"; "~8.5–9 t reusable to SSO (project working figure)" | ~9.5 t — the tracker's key-findings block is now itself stale despite being lint-corrected once |
| `LIBRARY.md` `orbits_environment.md` row | "est. **~8.5–9 t** reusable to SSO (project working figure — see `synthesis/lint_report.md`)" | ~9.5 t — and the cross-ref should point to `payload_and_block_upgrade.md`, not lint pass 1 |
| `synthesis/preliminary_findings.md` §1, §3, §4, §5 | "**~8.5–9 t reusable Neutron SSO budget**" throughout | ~9.5 t (or annotate the whole doc as wave-1, superseded) |
| `synthesis/wave4_synthesis.md` §2a, §5, §6 | "~8.5–9 t budget"; the §2a launch-cost table assumes a node "near the reusable SSO budget (~8.5–9 t)" | ~9.5 t — the wave-4 payback math used the conservative low budget |
| `synthesis/lint_report.md` §1.2, §6 P3 | recommends standardizing on "**~8.5–9 t reusable**" — itself now superseded by wave 5 | Note as superseded by `payload_and_block_upgrade.md` |

This is **not a factual error in any single doc** — every SSO figure is correctly flagged
as an estimate — but it is a genuine project-wide inconsistency on the single
highest-leverage number. A reader navigating README → LIBRARY → tracker → simulations gets
~8.5 t (or ~10 t); a reader navigating thesis → wave-5 synthesis gets ~9.5 t. The two paths
disagree by ~1 t, which `payload_and_block_upgrade.md` §2 itself calls "decision-relevant
against a ~7–10 t node."

**Internal wobble inside the verification doc itself:** `payload_and_block_upgrade.md` §1
and §6 say expendable LEO is 15 t and DRL-to-SSO works to ~9.5 t, all consistent — but note
its own §2 derivation table lists the DRL SSO *range* as "~8,500–10,400 kg" while the
headline and §6 say "8,500–10,500 kg." A trivial ±100 kg rounding mismatch; flag only for
tidiness.

### 1.2 ⚠ The flyability ceiling — three un-reconciled numbers still live

The project has **four** distinct ceiling statements in circulation:

| Source | Ceiling quoted | Basis |
|---|---|---|
| `simulations/REPORT.md` §5, §6, §8 | **~214 kW** (1-rack reusable) | 8.5 t SSO budget; 5 kg/m² radiator @ 500 W/m² |
| `data_science/REPORT.md` §1, §2, §4 | **~163 kW** (crossover point) | 8.75 t SSO budget; heavier `solar_radiator_trajectory.md` mass curve |
| `node_design/hot_chip_thermal_trajectory.md` Summary, §5 | **"~214 kW … plausibly raises that ceiling into the ~260–320 kW range"** | hot-loop radiator, but still anchored to the old 214 kW base |
| `synthesis/wave5_synthesis.md` §2.4, `vision/initial_thesis.md` Rev 4 | **~200–250 kW baseline / ~270–320 kW +hot-loop / ~430–470 kW block-upgrade** | reconciled: 9.5 t SSO + hot-loop |

Both REPORTs **explicitly flag the discrepancy and defer it**: `data_science/REPORT.md` §2
note "⚠ crossover figure ~163 kW vs sim's ~214 kW — reconcile in synthesis";
`RESEARCH_TRACKER.md` row M2 repeats it. **The wave-5 synthesis §2.2 did the
reconciliation** (the difference is the solar+radiator mass curve, not arithmetic — and the
+1 t SSO correction lifts both). But **neither REPORT nor the tracker's M1/M2 rows were
annotated** to point at that resolution. Result: three of the four ceiling figures a reader
can land on are superseded, and only the synthesis/thesis carry the reconciled set.

`hot_chip_thermal_trajectory.md` is a subtler case: its arithmetic is sound but it builds
*on top of* the stale 214 kW base ("~214 → ~260–320 kW"). Wave 5 instead builds the
hot-loop lever on top of the corrected ~225 kW base, giving ~270–320 kW. The two happen to
land in a similar place, but the hot-chip doc should carry a cross-reference noting its
214 kW anchor was superseded.

**Recommended single project position** (already stated in wave-5 synthesis §2.4 — it just
needs propagating): 1-rack reusable node ceiling **~200–250 kW baseline Neutron (working
~225 kW); ~270–320 kW baseline + hot-loop (working ~300 kW); ~430–470 kW block-upgraded +
hot-loop.** The wave-4-era ~163–214 kW figures are superseded.

### 1.3 Radiator area — re-checked, and it is the one number that held up

Lint pass 1 reconciled the radiator-area conflict (`thermal_analysis.md` ~120–210 m² vs.
`node_mass_model.md` ~375–500 m²) to a **~200–430 m²/rack project range, working ~300 m²**.
Re-checking across all docs after wave 5:

- `node_design/hot_chip_thermal_trajectory.md` is internally consistent with this — its
  headline table gives 232 m²/rack at 130 kW for an 80 °C surface, 472 m² at a 40 °C
  surface, which brackets the ~300 m² working figure correctly.
- `node_design/solar_radiator_trajectory.md` §4.3 uses **~371 m²/rack at 130 kW**
  (350 W/m²) — at the upper end of the reconciled band, internally consistent with its own
  conservative assumptions.
- `simulations/REPORT.md` uses **500 W/m²** radiator flux (→ ~300 m² at 150 kW), citing
  "`lint_report.md` 1.1" — consistent with the working figure.
- `LIBRARY.md`, `RESEARCH_TRACKER.md` both carry "~200–430 m²/rack, working ~300 m²" — good.

**Verdict: the radiator-area figure is the cleanest of the load-bearing numbers** — lint
pass 1's reconciliation propagated well and wave 5 did not disturb it. No staleness here,
beyond noting the underlying chip→coolant→panel thermal model is still an open item (§5.3).
One minor wrinkle: `data_centers/ai_hardware.md` §5.2 still gives the *original* crude
"~370–540 m²" first estimate ("One GB200 rack ~370 m²… GB300 ~430 m²") without a
cross-reference to the reconciled range; harmless in context (it is explicitly an
order-of-magnitude passage) but a one-line "superseded — see node_mass_model / lint" pointer
would help.

### 1.4 Node-mass figures — wave-5 V1 case vs. the older envelopes

`synthesis/wave5_synthesis.md` §4.1 introduces a **~6.8 t V1 GB300 node** (sim mid) with
"~2.7 t of margin" against the 9.5 t budget — a deliberately reassuring re-frame. This is
consistent with `simulations/REPORT.md` §4 (6.79 t at 150 kW). But the older docs still
present the node mass differently:

- `node_design/node_mass_model.md` headline still leads with **"1-rack node ~5.4 t"** (the
  mass-optimized path) and a §6 feasibility-mid of **~8.6 t** — the same internal
  double-voicing lint pass 1 flagged (§1.3 of pass 1), still unreconciled.
- `synthesis/preliminary_findings.md` and `thermal_analysis.md` still carry the wave-1
  **"~6 t"** 1-rack node.
- `data_science/REPORT.md` §1 table uses **~8.4 t for the GB300 node** — heavier than the
  sim's 6.8 t, because it uses the heavier `solar_radiator_trajectory.md` mass curve.

So the project has 1-rack-node masses of ~5.4 t / ~6 t / ~6.8 t / ~8.4 t / ~8.6 t in
circulation depending on the doc and the mass curve. They are all defensible *bracketing*,
but the conclusion doc must pick one framing. Wave-5 synthesis §4.1's ~6.8 t-with-2.7 t-margin
is the current best statement and should be the standard; the others should be annotated as
mass-optimized or conservative-curve corners of the same envelope.

### 1.5 Minor numeric inconsistencies still live (carried from lint pass 1, not yet fixed)

Lint pass 1 §1.6, §1.7, §2.1 flagged these; they remain unfixed and are worth re-listing
because the conclusion doc should not inherit them:

- **GB300 rack power "~120 kW"** in `llm_compute/inference_scaling.md` §2 table — still the
  NVIDIA marketing figure that `ai_hardware.md` and `node_mass_model.md` explicitly warn
  against (use ~135 kW TDP / ~155 kW peak).
- **Fairing payload diameter** — `neutron_specs.md` treats 5.5 m as current;
  `node_mass_model.md` §5 and `simulations/REPORT.md` use 5.0 m. `payload_and_block_upgrade.md`
  does not restate it. Still not standardized.
- **RTLS-to-LEO** — `orbits_environment.md` §2 says "~8,000 kg RTLS";
  `neutron_specs.md` and `payload_and_block_upgrade.md` say 8,500 kg. The orbital doc is
  stale.
- `RESEARCH_TRACKER.md` "Key findings so far" — lint pass 1 §2.1 asked for the obsolete
  "leading physics-wall candidate / 370–540 m²" framing to be purged. The current tracker
  block no longer contains that exact bullet (it leads with "Heat rejection is a sizing/mass
  problem"), so **this one appears fixed** — good.

---

## 2. Stale claims (statements superseded by later research)

### 2.1 The retired $3.3B/GW revenue proxy still appears as if live

`wave4_synthesis.md` §3 explicitly **retired `ai_datacenter_tam.md`'s ~$3.3B/GW-yr as a
revenue figure** ("kept only for order-of-magnitude market sizing"); thesis Rev 3/Rev 4 and
the tracker key-findings repeat the retirement. But:

- `economics/ai_datacenter_tam.md` itself (§5, assumption A3, the arithmetic tables) still
  presents **"~$3B/GW/yr"** and the "~$0.3 / 3 / 30B/yr" orbital TAM with only its original
  internal "use for magnitude, not a business case" caveat — there is **no cross-reference
  to the wave-4 retirement**. A reader who opens the TAM doc directly is not told the figure
  was superseded as a revenue number.
- `LIBRARY.md`'s `ai_datacenter_tam.md` row ("illustrative orbital TAM ~$0.3–30B/yr") and
  `RESEARCH_TRACKER.md` row 10 carry the figure without the retirement note.

**Recommend:** add a one-line header note to `ai_datacenter_tam.md` §5 pointing to
`wave4_synthesis.md` §3 — "$3.3B/GW retired as a revenue figure; use ~$15–20B/GW-yr gross
IaaS / ~$25–50B/GW-yr inference-service." Lint pass 1 §2.6 already flagged this doc as
"under-integrated"; wave 4 integrated it but the doc itself was never annotated.

### 2.2 "Thermal is the leading physics-wall candidate" — mostly purged, one residue

Lint pass 1 §2.1 flagged this. It is now largely gone — the tracker and LIBRARY lead with
"thermal is a sizing/mass problem, not a wall." Residue check:

- `vision/initial_thesis.md` **Rev 1 §2 still reads "The binding constraint is thermal, not
  rack mass"** and "Thermal is the thing to quantify." This is *correct as a historical
  record* — Rev 1 is explicitly the pre-wave-1 view and Rev 2 onward corrects it — so it is
  not a true error. But a reader skimming the thesis top-to-bottom hits the stale framing
  before the correction. Acceptable as versioned history; no fix strictly needed, but the
  conclusion doc must not quote Rev 1.
- `data_centers/ai_hardware.md` §5.3 still says heat rejection "is likely the **dominant
  mass and deployment-complexity driver**" — this is *not* stale (it is true, and consistent
  with every later doc); it never claimed "physics wall." Fine.

**Verdict: substantially resolved since lint pass 1.** No action needed beyond not quoting
thesis Rev 1 in the conclusion.

### 2.3 The founder "+30%" radiator rule — corrected, but the tracker still shows it open-ish

`node_mass_model.md` §4 corrected the founder's "+30%" radiator-vs-solar rule to **radiator
area ≈ 0.5–0.9 × solar area**. Lint pass 1 §2.2 / P6 asked for the tracker's founder-input
block to be closed out with the result. Re-checking `RESEARCH_TRACKER.md`: the "Founder
input — wave 3" block **now does** carry a "→ Resolved (item 14…)" annotation with the
corrected ratio. **This one is fixed** — good. No residue found in other docs.

### 2.4 "1–2 racks per launch" — fully resolved

Lint pass 1 §1.4 flagged the "~1–2 racks" vs. "1 rack/node" contradiction. Re-checking:
`LIBRARY.md`'s `thermal_analysis.md` row now reads "1 rack/node, 1 node/launch" (lint pass 1
P2 applied); the tracker, syntheses, and thesis are all consistent on 1 rack/node. The
**only residue** is inside `orbital/thermal_analysis.md` itself — §5 still carries its
original "~2 racks/launch working number" and the 2-rack mass column — but the doc now has a
lint cross-reference box at the top of §1 pointing to the reconciliation. Acceptable as
versioned history; the doc's own body is stale but flagged. The conclusion doc must use
`node_mass_model.md` / wave-5 synthesis, not `thermal_analysis.md` §5.

### 2.5 Wave-4 payback numbers computed against the stale SSO budget

`wave4_synthesis.md` §2 — the decisive payback arithmetic — assumes a node "near the
reusable SSO budget (~8.5–9 t)" and a launch-mode split that hinges on it. Wave 5's ~9.5 t
correction means a GB300 node now flies reusable **comfortably** (~2.7 t margin per wave-5
§4.1), not marginally. The wave-4 *payback ratios* (cost ÷ revenue) do not change — they are
not SSO-dependent — but the wave-4 narrative "feasibility-mid node sits near the budget, so
reusable is the planning case but expendable is a real possibility" is now too pessimistic.
Wave-5 synthesis already supersedes this; flag only so the conclusion doc draws the payback
*tables* from wave 4 but the *flyability/margin* framing from wave 5.

### 2.6 The "N-company" founder recollection — correctly closed, no residue

`solar_radiator_trajectory.md` §6.1 cleanly investigated and dismissed the founder's
"Rocket Lab acquired an N-company for collapsing structures" recollection (only Mynaric
starts with N; likely a conflation). No other doc repeats the erroneous recollection. Clean.

---

## 3. Consistency of the top-level docs

**`vision/initial_thesis.md` (Rev 4)** — **current and consistent with the underlying
research.** Rev 4 correctly carries ~9.5 t SSO, the reconciled ~200–250 / ~270–320 /
~430–470 kW ceilings, the three-tier premium framing, the inference-service-conditional
verdict, and 1 rack/node. It correctly states the founder's wave-5 "2 racks on a
block-upgraded Neutron" hypothesis is *not* supported by the mass model. **No staleness in
Rev 4.** The only caveat (noted in §2.2 above): Revs 1–3 contain superseded numbers, which
is correct as versioned history but means the conclusion doc must quote only Rev 4.

**`synthesis/wave5_synthesis.md`** — **current and the best single source** for the
re-baselined numbers. Internally consistent with `payload_and_block_upgrade.md`,
`hot_chip_thermal_trajectory.md`, and the two REPORTs (it explicitly reconciles the REPORTs'
ceiling discrepancy in §2.2). One observation: §5 introduces a constellation sizing of
**"~12–24 nodes"** for a robust laser-meshed service — a larger figure than the "~4–8 nodes"
that `preliminary_findings.md` §5 and `wave4_synthesis.md` §6 use for a "first commercial
service." Wave 5 distinguishes them (4–8 = first service, 12–24 = robust always-on mesh) so
it is not a contradiction — but the conclusion doc should carry both with that distinction
explicit, or the numbers will look inconsistent side by side.

**`README.md`** — **mildly stale.** It is deliberately high-level and defers to the thesis
and tracker, so it carries no hard numbers to go stale — good. But its "## Status" line
still reads *"Project kicked off 2026-05-17. Scaffolding in place; foundational research
agents running."* The project has since completed 5 research waves, 2 simulations, and 5
syntheses. Lint pass 1 §3 flagged this same line; still not updated.

**`LIBRARY.md`** — **stale on the SSO figure and on cross-references.** Specific defects:
- The `orbits_environment.md` row gives "est. ~8.5–9 t reusable to SSO" — stale (§1.1).
- It points readers to `synthesis/lint_report.md` for the SSO figure, but the authoritative
  source is now `rocket_lab/neutron/payload_and_block_upgrade.md`.
- **`rocket_lab/neutron/payload_and_block_upgrade.md` (research item 23) is not in the
  LIBRARY catalog at all** — see §4.1. The wave-5 doc that *re-baselined the project's most
  important number* is missing from the catalog.
- Likewise the other wave-5 research docs (`hot_chip_thermal_trajectory.md`,
  `rack_cost_trajectory.md`, `rack_internals.md`, `solar_radiator_trajectory.md`,
  `reliability_failure_handling.md`, `energy_operating_costs.md`) and the two model REPORTs
  are **not catalogued in LIBRARY** — see §4.1. LIBRARY's catalog effectively stopped at
  wave 3/4.
- The `neutron_specs.md` row's key takeaway ("~13 t to LEO reusable; no official SSO
  figure; mass-bound for dense racks") is fine but should cross-reference item 23, which
  supersedes it on SSO.

**Bottom line for §3:** the *thesis Rev 4* and *wave-5 synthesis* are current and mutually
consistent — the project's actual conclusions are sound and up to date. The failure is in
the **navigation layer**: `README.md` and especially `LIBRARY.md` were not refreshed after
wave 5, so a reader who starts where the project tells them to start (LIBRARY) is routed to
stale figures and an incomplete catalog. This is the same failure mode lint pass 1
identified — the newest research not folded back into the index — recurring one wave later.

---

## 4. Orphans & broken references

### 4.1 Orphans — wave-5 research docs and both model REPORTs are NOT catalogued in LIBRARY

This is the most concrete structural defect. `LIBRARY.md`'s catalog covers the wave-1–3 docs
plus the four economics docs, but **the following project documents are tracked in
`RESEARCH_TRACKER.md` yet absent from `LIBRARY.md`'s catalog tables:**

| Document | Tracker row | In LIBRARY? |
|---|---|---|
| `rocket_lab/neutron/payload_and_block_upgrade.md` | item 23 | **No** |
| `node_design/hot_chip_thermal_trajectory.md` | item 24 | **No** |
| `economics/rack_cost_trajectory.md` | item 18 | **No** |
| `node_design/rack_internals.md` | item 19 | **No** |
| `economics/energy_operating_costs.md` | item 20 | **No** |
| `node_design/solar_radiator_trajectory.md` | item 21 | **No** |
| `node_design/reliability_failure_handling.md` | item 22 | **No** |
| `simulations/REPORT.md` (+ `simulations/README.md`) | row M1 | **No** |
| `data_science/REPORT.md` (+ `data_science/README.md`) | row M2 | **No** |
| `synthesis/wave4_synthesis.md` | row S3 | **Yes** (added) |
| `synthesis/wave5_synthesis.md` | row S4 | **Yes** (added) |
| `synthesis/lint_report.md` | row L1 | **No** — the first lint report is not catalogued |

So **nine research/model documents and the first lint report are orphaned from the
LIBRARY catalog.** They are not orphaned from the tracker (the tracker is complete and
current — rows 1–24, M1–M2, S1–S4, L1–L2 all present and pointing at real files), so this
is a one-sided orphan: tracked but not catalogued. LIBRARY explicitly bills itself as "the
catalog — every document with a one-line description"; it is currently missing roughly a
third of the corpus.

### 4.2 Broken references / links — none found, with minor notes

- All relative markdown links checked resolve to existing files (README↔LIBRARY↔tracker,
  the thesis's `../synthesis/…` links, the inline `(./rf_satcom.md)`-style links).
- `RESEARCH_TRACKER.md` row L2 points to `synthesis/lint_report_2.md` with status "in
  progress / Agent running" — that is **this file**; once written the row is satisfied (the
  status should move to `draft`).
- `RESEARCH_TRACKER.md` row S2 points to "synthesis/" (a directory) with status `planned` —
  not broken, an expected placeholder for the unwritten conclusion doc.
- **`rocket_lab/neutron/neutron_specs.md` predates `payload_and_block_upgrade.md` and is not
  cross-referenced to it.** `neutron_specs.md` §1 / §8 / Open Q1 still present SSO as "~8–10 t
  estimate, the single most important missing number" and Open Q5 puzzles over the
  "8,000 kg to LEO" snippet. `payload_and_block_upgrade.md` §4 **explicitly resolves that
  exact open question** ("this resolves the prior `neutron_specs.md` open question #5 — the
  8,000 kg snippet was the original 2021 Neutron design figure") and supersedes the SSO
  estimate with ~9.5 t. Yet `neutron_specs.md` carries no pointer forward to item 23. A
  reader landing on `neutron_specs.md` (the doc LIBRARY and the tracker list *first*) gets
  the superseded ~8–10 t SSO estimate and an "open" question that is actually closed. **Add
  a cross-reference box to `neutron_specs.md`** pointing to `payload_and_block_upgrade.md`.
- Cosmetic, carried from lint pass 1 §4: `orbital/orbits_environment.md` and
  `orbital/thermal_analysis.md` are both titled "Doc 6 of foundational research"
  (thermal adds "(companion)"). Still duplicated; harmless.

---

## 5. Gaps — open questions raised in a doc but not in the tracker backlog

`RESEARCH_TRACKER.md`'s "Open research questions (backlog)" was refreshed from
`wave4_synthesis.md` §7/§9 and is reasonably current for waves 1–4. But several open
questions raised by the **wave-5 docs and the two models** are not in the backlog:

### 5.1 Re-run the fairing-packing simulation with the corrected inputs
`wave5_synthesis.md` §8 item 5 and `hot_chip_thermal_trajectory.md` Open Q2 both call for
**re-running `simulations/` with the 9.5 t SSO budget and the hot-loop radiator mass curve**
to produce a single defensible ceiling (the ~300 kW figure is currently derived
*analytically* in the synthesis, not confirmed in the model). This is a concrete, cheap,
high-value action item — it is not in the tracker backlog.

### 5.2 Coolant-loop reliability — the leading whole-node-kill mode
`reliability_failure_handling.md` §4 and `wave5_synthesis.md` §7 identify the **coolant
loop / CDU as the single most likely whole-node killer** (pump MTBF ~30,000 h vs. a 3-yr
un-serviceable mission; needs N+1). The tracker backlog has nothing on coolant-loop
reliability or the N+1 cooling-redundancy design requirement. (Lint pass 1 §5.5 flagged the
fluid-loop *mass*; the *reliability* dimension is a distinct, newer gap.)

### 5.3 Hot-loop vs. silicon-longevity / junction-defending ΔT budget
`hot_chip_thermal_trajectory.md` §4 and its Open Qs raise specific unmodeled questions: the
leakage-power feedback at +10–20 °C junction, the Arrhenius-vs-thermal-cycling split of the
~7–9% AFR, whether a two-phase loop is needed to reach the 100 °C+ radiator columns, and
whether Rubin raises Tjmax above ~85 °C. The tracker backlog has the generic "GPU/HBM
lifetime under a hot loop" item (carried from lint pass 1 §5.2) but not the sharper
wave-5 sub-questions.

### 5.4 Burn-in cadence as a launch-cadence constraint
`reliability_failure_handling.md` §3 and Open Q6 establish that proper space-acceptance
burn-in is **1–3 weeks per rack, not 1–2 days** — a real constraint on deployment cadence
and on how many burn-in stations a constellation buildout needs. Not in the backlog.

### 5.5 GPU AFR for Blackwell/GB200 specifically
`reliability_failure_handling.md` Open Q2 notes all hard AFR data is H100-era; GB200/GB300
run hotter and have no published field-reliability data yet. The ~7–9% planning AFR
underwrites the wave-5 "glide to ~75–85% compute" business assumption. Not in the backlog.

### 5.6 Connectivity architecture decision still only partially tracked
`orbit_types_primer.md` §6 raised the GEO-relay vs. LEO-mesh vs. ground-diversity fork;
lint pass 1 §5.4 asked for it in the backlog. `wave5_synthesis.md` §5/§8 item 10 sharpens it
(LEO laser mesh is the practical answer, ~12–24 nodes). The tracker backlog *does* now carry
"GEO-relay vs. LEO-mesh vs. ground-diversity — the connectivity design fork" — **this one is
tracked.** Good. No action.

### 5.7 Items already well-tracked (no action — listed for completeness)
The backlog correctly carries: node unit economics (the decisive workstream), the
spacecraft-hardware cost build-up, deployable-radiator make-vs-buy, Neutron's true SSO
payload, the "1.36 t rack scope" definition, the chip→coolant→panel thermal model, customer
willingness-to-pay, orbit-addressable TAM, and lifecycle carbon. These are current.

---

## 6. Prioritized fix list

Ordered by impact on the integrity of the project's conclusions — i.e. what must be true
before `RESEARCH_TRACKER.md` row S2 (the final conclusion document) is written.

**P1 — Propagate the ~9.5 t SSO re-baseline everywhere, or annotate the stale docs.**
The single most important fix. Update every document in the §1.1 table to **~9.5 t (range
8.5–10.5 t) reusable-to-SSO**, citing `rocket_lab/neutron/payload_and_block_upgrade.md` as
the source. Highest priority within this: the two model REPORTs (`simulations/REPORT.md`,
`data_science/REPORT.md`), because their headline flyability numbers are computed against
the stale budget; the `RESEARCH_TRACKER.md` key-findings block; and `LIBRARY.md`. If full
edits are too costly, at minimum add a one-line "superseded — see item 23, ~9.5 t" banner to
each stale doc so a reader is never silently handed the old number.

**P2 — Reconcile and propagate the single flyability-ceiling figure.** Adopt the wave-5
synthesis §2.4 set as the project position — **~200–250 kW baseline / ~270–320 kW
+hot-loop / ~430–470 kW block-upgrade** — and annotate `simulations/REPORT.md` (~214 kW),
`data_science/REPORT.md` (~163 kW), and `hot_chip_thermal_trajectory.md` (~260–320 kW off a
stale 214 kW base) with a cross-reference to that reconciliation. Ideally also **re-run the
fairing-packing simulation** with the 9.5 t budget + hot-loop radiator curve to confirm the
~300 kW working figure in the model (currently only derived analytically) — see §5.1.

**P3 — Catalog the orphaned documents in `LIBRARY.md`.** Add catalog rows for the nine
wave-5 research/model documents and the first lint report listed in §4.1
(`payload_and_block_upgrade.md`, `hot_chip_thermal_trajectory.md`, `rack_cost_trajectory.md`,
`rack_internals.md`, `energy_operating_costs.md`, `solar_radiator_trajectory.md`,
`reliability_failure_handling.md`, `simulations/REPORT.md`, `data_science/REPORT.md`,
`synthesis/lint_report.md`). LIBRARY currently catalogs only ~⅔ of the corpus.

**P4 — Cross-reference `neutron_specs.md` forward to `payload_and_block_upgrade.md`.** Add a
note to `neutron_specs.md` (§1 / §8 / Open Qs) that item 23 supersedes its ~8–10 t SSO
estimate with ~9.5 t and resolves its Open Question #5. It is the first doc the tracker and
LIBRARY list, and it currently hands readers a superseded estimate and a falsely-open
question.

**P5 — Annotate the retired $3.3B/GW proxy at its source.** Add a header note to
`economics/ai_datacenter_tam.md` §5 (and the LIBRARY/tracker rows) stating the $3.3B/GW
figure was retired as a revenue figure by `wave4_synthesis.md` §3 — use ~$15–20B/GW-yr gross
IaaS / ~$25–50B/GW-yr inference-service. The retirement is recorded everywhere *except* the
doc that contains the figure.

**P6 — Standardize the 1-rack-node mass framing.** Pick the wave-5 synthesis §4.1 statement
(**~6.8 t sim-mid GB300 node, ~2.7 t margin against 9.5 t**) as the headline, and annotate
`node_mass_model.md` (still leads with ~5.4 t), `preliminary_findings.md`/`thermal_analysis.md`
(~6 t), and `data_science/REPORT.md` (~8.4 t) as mass-optimized / conservative-curve corners
of the same envelope. Resolve `node_mass_model.md`'s internal ~5.4 t-headline-vs-~8.6 t-§6
double-voicing (carried unfixed from lint pass 1 §1.3).

**P7 — Refresh the tracker backlog with the wave-5 gaps (§5).** Add: re-run the simulation
with corrected inputs (5.1); coolant-loop reliability / N+1 cooling (5.2); the sharper
hot-loop/junction sub-questions (5.3); burn-in cadence as a deployment constraint (5.4);
Blackwell-specific GPU AFR (5.5).

**P8 — Minor cleanups.** Update `README.md`'s stale "## Status" line (lint pass 1 also asked
for this). Fix GB300 "~120 kW" → ~135 kW in `inference_scaling.md` §2 (carried from lint
pass 1 §1.6). Standardize fairing diameter wording (5.0 vs 5.5 m). Fix "~8,000 kg RTLS" →
8,500 kg in `orbits_environment.md` §2. Add the ~300 m² radiator cross-reference to
`ai_hardware.md` §5.2's "~370–540 m²" passage. De-duplicate the "Doc 6" title shared by the
two orbital docs.

---

## 7. What is genuinely solid (so fixes don't overcorrect)

For balance — these hold up across all five waves and need no change:

- **The core verdict — "no physics wall; the architecture is buildable; economics close
  marginally at Vera Rubin under the inference-service model."** Robust, multi-sourced,
  consistent across `preliminary_findings.md`, `wave4_synthesis.md`, `wave5_synthesis.md`,
  and thesis Rev 4.
- **The thesis Rev 4 itself** — fully current, internally consistent, correctly conditional,
  and honest about the three unpublished/un-quoted numbers it rests on.
- **The radiator-area reconciliation** (~200–430 m²/rack, working ~300 m²) — lint pass 1's
  one big fix propagated cleanly and survived wave 5 (§1.3).
- **The 1-rack/node, 1-node/launch architecture** — settled and consistent everywhere; the
  2-rack node is correctly rejected on every Neutron configuration, including in the
  wave-5 docs.
- **The inference-not-training thesis, dawn-dusk SSO choice, optical-primary + RF-sliver
  comms conclusion, and diversity-beats-aperture ground-station finding** — all consistent
  across every doc.
- **`RESEARCH_TRACKER.md` as an index** — complete and current (rows 1–24, M1–M2, S1–S4,
  L1–L2 all present and pointing at real files); only its *key-findings narrative block*
  carries the stale ~8.5 t SSO number.

**The project's direction and its top-line conclusions are sound and up to date.** The
defect is narrow and recurring: the newest wave's re-baselined numbers (here, ~9.5 t SSO and
the reconciled ceiling) have not been folded back into the older research docs, the two
model REPORTs, or the navigation layer (LIBRARY, README) — exactly the failure mode lint
pass 1 named, one wave later. Fixing P1–P3 before the conclusion document is written is what
keeps the final deliverable from inheriting superseded numbers.

---

*End of lint report 2.*
