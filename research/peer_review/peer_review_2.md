# Peer Review 2 — AI-Hardware / Compute / Node-Design Slice

**Reviewer:** Peer Reviewer 2
**Date:** 2026-05-17
**Scope audited (9 docs):**
- `data_centers/ai_hardware.md`
- `llm_compute/inference_scaling.md`, `llm_compute/multi_rack_inference.md`, `llm_compute/minimum_viable_scale.md`
- `node_design/node_mass_model.md`, `node_design/rack_internals.md`, `node_design/solar_radiator_trajectory.md`, `node_design/reliability_failure_handling.md`, `node_design/hot_chip_thermal_trajectory.md`

Method: full read of all 9; cross-check against `RESEARCH_TRACKER.md` and `LIBRARY.md`;
spot web-checks of GB300 power, ISS radiator figures, Neutron SSO performance.
**Report only — no documents were edited.**

---

## Overall assessment

The slice is in good shape: claims are generally well-sourced, hard numbers are
attributed, and the physics arithmetic (Stefan-Boltzmann, T⁴ scaling, mass
build-ups) is internally consistent and reproduces correctly on spot-check. The
docs are unusually disciplined about flagging estimates. **No invalidating
errors found.** The significant issues are all *staleness* — superseded SSO
budgets and a superseded headline node-mass figure that were never reconciled
back into the body of two documents — plus one unflagged internal
contradiction (the hot-loop ↔ HBM-thermal tension) and one source figure that
is plausibly misread. Details below.

**Clean (no material issues):** `inference_scaling.md`, `rack_internals.md`,
`reliability_failure_handling.md` — these three are clean (minor notes only).

---

## SIGNIFICANT findings

### S1 — `node_mass_model.md`: the headline Summary table is stale and internally contradicted by the doc's own body

Top-of-doc Summary (lines 12–19):

> | **1-rack node** | **~5.4 t** | 4.3 – 7.0 t |
> **Verdict — mass vs. volume bound:** The node is **volume-bound, not
> mass-bound** …

But §6 (line 231) computes the 1-rack node at **~5.6 / 8.6 / 14.1 t** and §6/§7
explicitly conclude the node is **mass-bound** ("the design is **mass-bound at
the margin**", line 286; "fairing-volume-comfortable but mass-budget-tight",
line 294). The doc reconciles this in a note (line 233) by saying the headline
"~5.4 t" reflects only the "advanced-technology, mass-optimized path" — but the
**Summary as written states a flat headline figure and a flat "volume-bound"
verdict that the rest of the doc, the tracker, and every downstream doc
contradict.** RESEARCH_TRACKER item 14 and LIBRARY both quote "~5.4–8.6 t" and
"mass-tight / mass-bound." The Summary's "~5.4 t" point figure and
"volume-bound, not mass-bound" verdict are **stale dead notes** — superseded by
the doc's own §6–§7 and by every synthesis since. *Severity: significant —
it is the headline of the canonical mass-model doc and it says the opposite
of the project's settled position.*

### S2 — `node_mass_model.md`: Summary still cites the pre-wave-5 radiator/solar areas and the ~8.5 t SSO budget without the correction

Summary line 19 cites "**~140–210 m² of radiator**" per rack. This is the
old wave-1 thermal figure. The doc's *own* §4 (line 141) derives **~430 m²
(375–500 m²)**, and §5 carries a "Superseded (wave-5)" note re-baselining SSO
to ~9.5 t. But the Summary paragraph was never updated: it still says
"~140–210 m²" radiator and "~8.5 t reusable mass budget." The lint reports and
tracker put the project radiator figure at **~200–430 m²/rack (working
~300 m²)** and SSO at **~9.5 t**. So the Summary contradicts (a) the doc's own
§4, and (b) the tracker/LIBRARY. *Severity: significant — stale figures in the
most-cited node doc's abstract.* (Note: §5–§7 carry the supersession notes
correctly; only the Summary block was missed.)

### S3 — Unflagged contradiction: hot-loop radiator strategy vs. HBM thermal limits (the "hot-loop ↔ HBM-thermal tension")

The debate explicitly "surfaced the hot-loop↔HBM-thermal tension"
(tracker D1, line 63), and it remains under-addressed in this slice:

- `hot_chip_thermal_trajectory.md` is careful: it repeatedly insists the win
  comes from a hot **radiator/loop** while the **junction is defended** near
  ~70 °C via ΔT budget / two-phase loop (§4.4, line 191), and concedes the
  100–120 °C columns are "mostly theoretical" with today's silicon (§3.4).
- But `ai_hardware.md` §5.3 (line 155) states flatly: "Running the coolant
  loop hotter (warm-water DLC, which Rubin already favors) **dramatically
  shrinks radiator area via the T⁴ term** — a key design lever," with **no
  mention of the junction-temperature ceiling or the reliability cost.**
- `node_mass_model.md` §4 sizes the radiator at a 50 °C surface; the headline
  "working ~300 m²" project figure depends on hot-loop operation that
  `hot_chip_thermal_trajectory.md` shows is bounded by Tjmax ~83–85 °C and an
  Arrhenius ~2× failure penalty per +10 °C junction.

The tension is real: the radiator-area figures that make the node fly assume
hot-loop operation, while HBM/junction limits (~85 °C, barely moving across
generations) cap how hot the loop can run, and `reliability_failure_handling.md`
independently flags thermal-cycling/HBM fatigue as a primary failure driver.
`hot_chip_thermal_trajectory.md` handles this honestly; **`ai_hardware.md` and
`node_mass_model.md` present the hot-loop lever as cost-free without the
cross-reference.** *Severity: significant — a known project-level tension is
under-flagged in 2 of the 3 docs that depend on it.*

### S4 — `solar_radiator_trajectory.md`: headline scaling table uses a 130 kW radiator area (~370 m²) that the project has since re-bracketed

The §Summary table (line 17) and §4.3 (line 139) size the 130 kW radiator at
**~371 m²** (350 W/m², 40–50 °C surface). `hot_chip_thermal_trajectory.md`'s
own table gives 472 m² at a 40 °C surface and 232 m² at 80 °C for the same
130 kW — i.e. the "~370 m²" sits mid-band and is fine *as a single assumption*,
but the doc never reconciles against the project's adopted **~200–430 m²/rack
(working ~300 m²)** range from `lint_report.md`. The 300/600 kW rows inherit
the same single-point assumption. This is not wrong arithmetic, but the doc
presents a precise-looking scaling table without the bracket the rest of the
project now uses. *Severity: significant-minor — the scaling conclusion (mass
wall at 300–600 kW) is robust; the specific 130 kW area is a stale single-point
estimate not flagged as superseded.* Note §4.5 *does* carry the SSO
supersession note correctly.

---

## MINOR findings

### M1 — `ai_hardware.md`: ISS radiator "~840 m²" is plausibly the two-sided figure, not flagged

§5.2 (line 151): "the **ISS** rejects ~70 kW of heat through ~840 m² of
radiator panels weighing ~1,000 kg." Web cross-check: the ISS EATCS is 6
radiator assemblies × 8 panels × ~8.79 m² ≈ **~422 m² of one-sided panel
area** (NASA ATCS overview; AIAA J. Spacecraft). The "~840 m²" figure is
~2× that — i.e. it counts **both faces** of the double-sided panels. That is a
defensible convention (ISS radiators do radiate from both sides), but the doc
elsewhere sizes AI-rack radiators on **planform** (one-sided) area, so quoting
ISS as "840 m²" against a planform-based "370 m²/rack" is an apples-to-oranges
comparison that overstates the ISS's apparent area efficiency. The ~1,000 kg
mass and ~70 kW are consistent with sources. *Recommend: flag whether 840 m²
is one-face or two-face, for a like-for-like comparison.*

### M2 — `ai_hardware.md` §1.1 vs. `inference_scaling.md` §2: GB300 power figures disagree across the two docs

`ai_hardware.md` correctly carries the **~135 kW TDP / 155 kW peak** GB300
figure (confirmed by web spot-check — Sunbird/Lenovo). But
`inference_scaling.md` §2 (line 64) table still lists **GB300 NVL72 … ~120 kW**.
`inference_scaling.md` is the older doc and its "~120 kW" for *both* GB200 and
GB300 is superseded by `ai_hardware.md`'s more careful split. Not load-bearing
for `inference_scaling.md`'s conclusions (which are about memory/communication,
not power), but it is an internal inconsistency between two docs in this slice.
*Severity: minor — stale figure in a doc whose argument does not depend on it.*

### M3 — `node_mass_model.md` §1 vs. `ai_hardware.md`: rack dimensions disagree slightly

`node_mass_model.md` adopts "**600 mm W × 1200 mm D × 2300 mm H**" while
`ai_hardware.md` §1.1 gives "~600 mm W × 1,068 mm D" (and §2.1 "~1,068 mm").
The 1,068 mm vs. 1,200 mm depth difference (~12%) is the L-rail dimension vs.
the cabinet depth — `node_mass_model.md` line 43 actually shows both
("~1068 mm L-rail … ~1200 mm D"). Harmless for the mass model (volume is not
binding) but the two docs quote different single depth numbers in their
summaries. *Severity: minor.*

### M4 — `multi_rack_inference.md`: two arXiv IDs use a future-dated "26xx" scheme — verify they resolve

The doc cites `arXiv 2604.15039` ("Prefill-as-a-Service"), `arXiv 2604.15528`
(ISL latency), and `arXiv 2511.15861`. The `2604.*` identifiers imply an
April-2026 submission — plausible given the May-2026 doc date, but I could not
independently confirm these resolve (arXiv lookups not performed live). The
`2604.15039` paper carries a load-bearing claim (hybrid-MoE KV-cache transfer
fits ~170 Gbps; dense attention needs ~3.8 Tbps) used in the §5 verdict and
Open Question 3. *Severity: minor — recommend a live check that both 2604.*
preprints exist and say what is quoted; if either is unresolvable the
"disaggregated PD survives a laser ISL" sub-conclusion weakens.*

### M5 — `minimum_viable_scale.md`: revenue-basis figure stated two ways

§4.1 says the revenue basis is "**~$8–16M/rack-year**" (calling it "the brief's
stated basis"), then immediately derives "~$5.6–14.5M/rack-year" and "central
~$8–10M" from `revenue_per_watt.md`. The "$8–16M" upper bound is not derived
anywhere in-doc — it is asserted as the brief's number. The companion line in
the doc header also says "~$8–16M/rack-year." Minor, but the doc should either
derive the $16M top or attribute it cleanly; as written it reads as a figure
imported without a source. *Severity: minor — cross-check against
`economics/revenue_per_watt.md` (outside this slice).*

### M6 — `solar_radiator_trajectory.md`: ISS-radiator areal-mass internal-consistency note

The doc adopts "3 / 5 / 8 kg/m²" for deployable radiators. Web cross-check of
the ISS radiators gives **~8 kg/m² (planform incl. structure) / ~2.75 kg/m²
(exposed panel only)** — consistent with the doc's 3–8 band. No error; noting
the spot-check **confirms** the doc's radiator areal-mass assumptions. (This is
a positive confirmation, not a defect.)

### M7 — `node_mass_model.md` §2: terrestrial GB300 "≥21 kN/m² floor loading" wording

`ai_hardware.md` §2.2 line 78 says "Floor loading ≥ ~21 kN/m² (~440 psf)" and
"concentrates 1.36 t into a ~0.64 m² footprint." 1,360 kg over 0.64 m² is
~2,125 kg/m² ≈ 20.8 kN/m² — arithmetic checks out. No defect; noted as a
positive spot-check.

---

## Cross-document consistency summary

| Topic | Status |
|---|---|
| SSO budget (~9.5 t) | `node_mass_model.md` §5 / `solar_radiator_trajectory.md` §4.5 / `rack_internals.md` §5 carry correct supersession notes. **`node_mass_model.md` Summary block does NOT** (S2). |
| Node mass (~5.4–8.6 t, mass-bound) | Tracker, LIBRARY, §6–§7 agree. **`node_mass_model.md` Summary contradicts** (S1). |
| Radiator area (~200–430 m², working ~300 m²) | Tracker/LIBRARY/lint agree. **`node_mass_model.md` Summary (140–210 m²) and `solar_radiator_trajectory.md` (single-point 370 m²) not reconciled** (S2, S4). |
| 1 rack/node, 1 node/launch | Consistent across all 9 docs and tracker. ✓ |
| GB300 power (~135 kW TDP) | `ai_hardware.md` ✓ (web-confirmed); **`inference_scaling.md` stale at 120 kW** (M2). |
| Hot-loop lever | `hot_chip_thermal_trajectory.md` honest; **`ai_hardware.md` / `node_mass_model.md` present it without the Tjmax/reliability caveat** (S3). |
| ~7–9% GPU AFR, glide to ~75–85% | `reliability_failure_handling.md` ↔ tracker ↔ `minimum_viable_scale.md` consistent. ✓ |
| Inference-vs-training, one-rack-per-model | `inference_scaling.md` ↔ `multi_rack_inference.md` ↔ `ai_hardware.md` fully consistent. ✓ |

---

## Bottom line

No claim in this slice is invalid on its evidence, and the engineering
arithmetic reproduces correctly. The defects are concentrated in **stale
abstract/summary blocks of `node_mass_model.md`** (S1, S2) — its Summary still
says "volume-bound," "~5.4 t," "140–210 m²" while its own body and the whole
project say "mass-bound," "~5.4–8.6 t," "~200–430 m²" — and in the
**under-flagged hot-loop↔HBM-thermal tension** (S3). `solar_radiator_trajectory.md`
carries a stale single-point radiator area (S4). Three docs
(`inference_scaling.md`, `rack_internals.md`, `reliability_failure_handling.md`)
are clean. Recommend the fix pass: (1) rewrite the `node_mass_model.md` Summary
to match its §6–§7 and the tracker; (2) add the Tjmax/reliability caveat +
cross-reference to the hot-loop mention in `ai_hardware.md` §5.3; (3) add the
project radiator-range bracket to `solar_radiator_trajectory.md`; (4) refresh
`inference_scaling.md`'s GB300 power cell.
