# Peer Review 4 — End Documents, Consistency & Hygiene Audit

*Reviewer: Peer Reviewer 4. Date: 2026-05-17. Scope: the end / framing /
synthesis documents — `CONCLUSION.md` (Rev 7), `vision/initial_thesis.md`,
the five synthesis docs, `README.md`, `LIBRARY.md`, `RESEARCH_TRACKER.md`,
`debate/bull_case.md`, `debate/bear_case.md`, `strategy/optimized_strategy.md`.
Report-only — no document was edited. Underlying research docs were opened
where needed to verify a claim's traceability.*

---

## 0. Overall assessment

The project's **conclusions are sound and the CONCLUSION.md (Rev 7) is itself
internally consistent, well-sourced, and carries a proper revision history.**
The thesis-narrative ("no physics wall; build-to-learn V1 → profitable V2;
premium product; fund to a go/no-go gate") is traceable end-to-end.

**But the end-document *layer* is not internally consistent as a set.** The
project ran eleven waves of founder input and revised the CONCLUSION through
v7, but **several upstream framing/index documents were frozen at an earlier
wave and never caught up.** The single biggest finding: `vision/initial_thesis.md`
stops at **Revision 4** (wave-5 vintage), while `CONCLUSION.md` is at Revision 7
and the project has absorbed waves 6–11. The thesis is therefore three to four
revisions stale on every number that moved after wave 5 — the launch-cost
re-base, the 5-year service life, the venture J-curve, the ambition case.
`README.md` is stale by even more. The two lint reports and the debate all
pre-date the conclusion and pre-date the launch-cost re-base, so they sit in
the corpus carrying numbers the project has since superseded.

Confidence in this audit: **high** for the staleness/consistency findings
(they are mechanical and cross-checkable); **medium-high** for the
traceability findings.

---

## SIGNIFICANT FINDINGS

### S1. The thesis was never revised past Rev 4 — it is the project's biggest "dead document"

`vision/initial_thesis.md` ends at **"Revision 4 — 2026-05-17 (after wave-5
synthesis)."** There is no Rev 5, 6, or 7. Yet `CONCLUSION.md` is at v7 and the
`RESEARCH_TRACKER.md` records founder input for waves 6, 7, 8, 9, 10, and 11,
plus three new research docs (items 28–30) and a third model (M3, the investor
projection).

The skill rules (and `README.md` line 15, `LIBRARY.md` line 11) state the
thesis is the versioned record of "what we believe and why it changed." It is
now four revisions and roughly six waves behind the actual project belief.
Concretely, the thesis **never records**:

- the **launch-cost re-base** from ~$50–55M to a ~$10–20M internal marginal
  cost (CONCLUSION Rev 4) — the single largest economic change in the project;
- the **5-year GPU service-life base case** (CONCLUSION Rev 3 / founder wave 8);
  the thesis still frames economics on the harsh "~2–3 year GPU obsolescence
  window" throughout Rev 3–4;
- the **venture-level investor J-curve** (~$1.15B peak, ~year-19–20 crossover —
  CONCLUSION Rev 5);
- the **converged build strategy** and **minimum-viable ~3–5-node deployment**
  (CONCLUSION Rev 6);
- the **conservative-vs-ambition dual case** and the **in-house-radiator
  decision** (CONCLUSION Rev 7).

`vision/initial_thesis.md` Rev 4 sharpened thesis statement still says the V1
node is **"~5–10× terrestrial cost per token"** and the V2 node ~$75–95M — both
costed at the ~$55M external launch price that Rev 4 of the conclusion
explicitly retired. A reader who follows `README.md`'s and `LIBRARY.md`'s
instruction to read the thesis gets a picture the project abandoned waves ago.

This is the most serious rule-compliance gap in the end-document set: the
thesis is supposed to be the living, append-only belief record, and it silently
stopped tracking.

### S2. README.md is badly stale — wrong revision numbers, wrong doc counts

`README.md` "## Status" (lines 64–70) reads:

> "Investigation complete (2026-05-17): 27 research docs, 2 simulations, 5
> syntheses, 2 lint passes, a 2-round adversarial debate; thesis at Revision 4;
> conclusion at v2."

Every count in this sentence is wrong as of the current state:

- **"27 research docs"** — the tracker lists **30** (items 1–30).
- **"2 simulations"** — there are now **3 models** (M1 fairing-packing, M2
  trajectory data-science, **M3 the investor projection** — `RESEARCH_TRACKER.md`
  rows M1/M2/M3).
- **"a 2-round adversarial debate"** — the debate ran **3 rounds** each side
  (the CONCLUSION itself, line 32, says "complete at three rounds"; both
  `debate/` files carry Round 3).
- **"thesis at Revision 4"** — true, but only because the thesis itself is
  stale (see S1); it *should* be further along.
- **"conclusion at v2"** — the conclusion is at **v7**.

Both lint reports flagged the README "## Status" line as stale (lint_report.md
§3, lint_report_2.md §3); it was never fixed and has since drifted much
further. `README.md` line 67 also still says "thesis at Revision 4 … conclusion
at v2," which would mislead any reader navigating from the project entry point.

### S3. LIBRARY.md catalog is incomplete and stale — confirmed still unfixed

`LIBRARY.md` bills itself as "the catalog — every document with a one-line
description." Lint report 2 §4.1 listed **nine research/model documents plus
lint_report_1** as missing from the catalog. Cross-checking the current
LIBRARY against the tracker, the catalog **still omits**:

- `economics/hyperscaler_margins.md` (tracker item 28)
- `llm_compute/minimum_viable_scale.md` (item 29)
- `economics/ambition_case.md` (item 30)
- `data_science/INVESTOR_PROJECTION.md` (model M3)
- `synthesis/lint_report.md` (row L1)
- `strategy/optimized_strategy.md` (row D2)
- `peer_review/` (row P1)

LIBRARY does now carry wave-5 research docs (`payload_and_block_upgrade.md`,
`hot_chip_thermal_trajectory.md`, `rack_cost_trajectory.md`, `rack_internals.md`,
`energy_operating_costs.md`, `solar_radiator_trajectory.md`,
`reliability_failure_handling.md`, both REPORTs) — so lint pass 2's P3 was
*partially* applied. But the **waves 6+ documents — the hyperscaler-margins
doc, the minimum-viable-scale doc, the ambition case, the investor projection,
and the strategy doc — are all load-bearing for CONCLUSION Revisions 5–7 and
none of them is catalogued.** LIBRARY also still says (line 11, line 27) the
thesis is "versioned: Rev 1 … Rev 4" — accurate only because of S1.

This is a rule-compliance failure: the research-wiki convention requires the
catalog to be current and complete; roughly a quarter of the corpus that the
conclusion cites is uncatalogued.

### S4. The two lint reports are themselves dead notes — they pre-date the conclusion

`synthesis/lint_report.md` and `synthesis/lint_report_2.md` were written
*before* the CONCLUSION existed. Both are explicit about this:

- `lint_report_2.md` §0: *"the conclusion document (`RESEARCH_TRACKER.md` row
  S2, status `planned`) is about to be written. … **This report exists to be
  the checklist that prevents that.**"*
- `lint_report_2.md` §6 P1–P8 are framed as "what must be true before … the
  final conclusion document is written."

The conclusion has since been written and revised seven times. Neither lint
report carries any note that it pre-dates the deliverable, and `RESEARCH_TRACKER.md`
row L2 still says "Fix agents running." The lint reports remain useful as a
record, but a reader landing on them is told the conclusion is unwritten and is
handed a fix-list whose status is now indeterminate (some items fixed — e.g.
LIBRARY's wave-5 rows; some not — e.g. README status line, the inference_scaling
"~120 kW" figure). They should be marked as superseded-by-conclusion, or the
project should note which P-items were applied.

### S5. The debate pre-dates the launch-cost re-base — its economic verdict is stale

The three-round debate (`debate/bull_case.md`, `debate/bear_case.md`) ran
entirely on the **~$55M external launch price** and a **~$85M node**. The
Bull's Round 3 surviving verdict (`bull_case.md` R3.4, lines 1125–1144)
explicitly states:

> "its central **~5.3-yr payback** sits *within* a ~5-year service life … a
> *comfortable* crossover needs a **~70%+ premium** … The verdict the corrected
> basis supports is the one **`CONCLUSION.md` v2** reached."

This is the pre-Rev-4 world. CONCLUSION Rev 4 re-based launch to ~$20M, which
moved V2 central gross payback from ~5.3 yr to **~2.8 yr** and the break-even
premium from ~70%+ to **~25–40%**. The debate's central numbers (~5.3 yr,
~70%+ premium, ~$85M node, "CONCLUSION v2") are therefore **dead notes** — the
debate was never re-run after the launch re-base.

This is defensible *as versioned history* (the debate is a dated artifact and
the CONCLUSION supersedes it), and the CONCLUSION correctly cites the debate
only for its *qualitative* convergence ("fund the work to a go/no-go gate"),
not its numbers. **But nothing in the debate files flags that their economics
are superseded**, and `RESEARCH_TRACKER.md` row D1 repeats the stale "fails the
all-in test by a thin margin; closes only at a ~70%+ unobserved premium" line
as if current. The CONCLUSION Verdict (line 78) does say "Round 3 ran the
economics … still at the ~$55M external launch price; Revision 4 re-runs them
at ~$20M" — so the conclusion handles it honestly. The dead note is in the
tracker's D1 row and in the un-annotated debate files.

### S6. Strategy doc Round 1 (Engineer) carries the superseded "block-upgrade on the critical path" framing un-annotated

`strategy/optimized_strategy.md` §2.1 header still reads **"Baseline reusable
Neutron for V1; the block-upgrade is the V2 critical path"** and the body says
"The block-upgraded Neutron (~12–13 t SSO) **is on the critical path to V2
profitability**." The §7 handoff repeats "the block-upgrade as the V2 critical
path."

This was **explicitly overturned later in the same document**: the CFO Round 1
("Keep the block-upgrade as an *optimization*, never a gating dependency") and
the Engineer Round 2 ("Demote the block-upgrade from 'critical path' to margin
upside … I wrote 'on the critical path to V2 profitability' in Round 1; the CFO
is right"). CONCLUSION Rev 6 adopts the demotion as a headline de-risking.

The strategy doc is append-only by design, so Round 1 keeping its original
wording is *correct as a debate record* — but Round 1 §2.1 and §7 are
dead notes the moment Round 2 converges, and they are not cross-referenced
forward. A reader skimming §2.1/§7 gets the abandoned framing. Minor in effect
(the convergence is later in the same file) but it is a genuine stale-claim
instance in an assigned document.

### S7. Thesis Rev 4 ↔ CONCLUSION ladder: "V1+/V2 power-capped Rubin" vs. thesis "block-upgrade for V2"

Because the thesis stopped at Rev 4, its V2 definition disagrees with the
conclusion's. Thesis Rev 4 (sharpened statement, line 575) says V2 is "a
**block-upgraded Neutron**, hot-loop, Rubin-class node." CONCLUSION Rev 6/7 and
the configuration ladder say the opposite: **"V2 closes on baseline Neutron +
hot-loop — it does not depend on the block-upgrade"** (CONCLUSION line 364,
386–402). This is not merely a numbers-staleness issue — it is a **substantive
architectural disagreement between two end documents** on what V2 *is*. The
conclusion is the later, correct position; the thesis is wrong, and because it
was never revised the disagreement is live and unflagged.

---

## DEAD NOTES — stale figures/claims left lying around

A consolidated list of superseded numbers still presented as live. (The lint
reports already catalogued the wave-5 SSO staleness across the *research* docs;
this list focuses on the **end documents** in my slice.)

| # | File | Quote / location | Why it is dead |
|---|---|---|---|
| D-1 | `README.md` §Status (l.64–70) | "27 research docs, 2 simulations, 5 syntheses … 2-round adversarial debate; thesis at Revision 4; conclusion at v2" | 30 docs, 3 models, 3-round debate, conclusion at v7 (see S2). |
| D-2 | `vision/initial_thesis.md` Rev 4 (l.575) | V2 = "a block-upgraded Neutron, hot-loop, Rubin-class node" | Superseded by CONCLUSION Rev 6 — V2 closes on **baseline** Neutron + hot-loop (see S7). |
| D-3 | `vision/initial_thesis.md` Rev 4 §3 (l.498) | "V1/GB300 today is ~5–10× terrestrial cost per token" | Re-based to **~3–6×** at the ~$20M internal launch cost — CONCLUSION ladder, l.362, l.673. |
| D-4 | `vision/initial_thesis.md` — whole doc | Economics framed on the "~2–3 year GPU obsolescence window" (Rev 3 headline, Rev 4 carries it) | Superseded by the **5-year service-life base case** (CONCLUSION Rev 3 / founder wave 8); 2–3 yr is now only the downside addendum. |
| D-5 | `vision/initial_thesis.md` Rev 3/4 | node cost "~$65–120M" / V2 "~$75–95M" | Superseded by **~$35–65M (~$45M mid)** after the launch re-base (CONCLUSION Rev 4). |
| D-6 | `RESEARCH_TRACKER.md` row D1 (l.63) | "5-year basis moved V2 from 'fails by ~2×' to 'fails the all-in test by a thin margin; closes only at a ~70%+ unobserved premium'" | The ~70%+-premium / thin-margin-fail read is the pre-Rev-4 world; Rev 4 re-base gives a ~25–40% break-even premium and a central case that *closes*. The D1 row is a dead note. |
| D-7 | `debate/bull_case.md` R3.4 (l.1125–1144) | "central ~5.3-yr payback … needs a ~70%+ premium … the verdict CONCLUSION.md v2 reached" | Whole economic verdict pre-dates the Rev-4 launch re-base; "CONCLUSION v2" no longer exists as the current state (see S5). Un-annotated. |
| D-8 | `strategy/optimized_strategy.md` §2.1, §7 | "the block-upgrade is the V2 critical path" / "on the critical path to V2 profitability" | Overturned by the CFO R1 + Engineer R2 convergence in the same file and by CONCLUSION Rev 6; Round 1 wording not cross-referenced forward (see S6). |
| D-9 | `synthesis/wave4_synthesis.md` §2a (l.74) and throughout | launch "$52M / $63M / $80M", node "~$63–120M (~$85M mid)" | Superseded by CONCLUSION Rev 4's ~$10–20M internal launch and ~$35–65M node. wave4_synthesis has a superseded-banner for the SSO figure but **none for the launch-cost/node-cost figures**, which Rev 4 retired. |
| D-10 | `synthesis/wave4_synthesis.md` / `wave5_synthesis.md` | node payback framed against "~2–3 year GPU obsolescence window" as the live test | Both syntheses run the 2–3 yr window as the operative test; CONCLUSION Rev 3 demoted it to a downside addendum and made 5 years the base case. The syntheses are not annotated for this. |
| D-11 | `synthesis/wave5_synthesis.md` §4.1 (l.234–237) | V1 node "Total node cost ≈ ~$65–95M internal … ~$90–130M at a customer price"; launch "~$50–55M reusable internal cost" | Superseded by Rev 4: the ~$50–55M figure is the *external* price, not internal cost; internal is ~$10–20M. |
| D-12 | `synthesis/lint_report.md` §1.2, §6 P3 | recommends standardizing on "~8.5–9 t reusable" SSO | Self-superseded — lint_report.md §1.2 has a wave-5 banner, but P3 in §6 still says "~8.5–9 t" with no banner. |
| D-13 | `synthesis/preliminary_findings.md` | "~8.5–9 t reusable Neutron SSO budget" throughout; "~6 t / ~11 t" node masses; 2-rack-node framing in §1/§5 | Wave-1 doc; carries a top banner for the SSO figure only. The ~6 t node mass and the surviving 2-rack-node sentences in §1 ("A 2-rack node … is not a baseline") are pre-node-mass-model framing — flagged by lint pass 1 §2.3, never reconciled in-body. |
| D-14 | `RESEARCH_TRACKER.md` "Founder input — wave 9" (l.376) | "this pulls node cost from ~$65–120M down toward ~$35–90M" | The "~$35–90M" range is itself superseded by the final Rev 4/5 figure of ~$24–63M / ~$45M mid; the tracker note was never closed out to the final number. |
| D-15 | `RESEARCH_TRACKER.md` row C1 (l.66) | "Conclusion document … **At v6.** … v7 pending" | The conclusion is at v7 (its own header and revision history confirm). The tracker's C1 row is one revision stale. |
| D-16 | `RESEARCH_TRACKER.md` row L2 (l.62) | lint pass 2 "Fix agents running." | Lint pass 2 is `draft`/done; the "fix agents running" status is stale and the fix outcomes are not recorded. |

Note on what is **not** a dead note: the GPU-life "2–3 year" language *inside
CONCLUSION.md* is correctly handled — it is explicitly demoted to a labelled
downside addendum (CONCLUSION §2, l.623–640). The CONCLUSION does not leave it
lying around as live. The dead-note problem is in the *upstream* docs (thesis,
syntheses, debate, tracker) that the conclusion superseded but that were never
annotated.

---

## TRACEABILITY

**CONCLUSION.md is traceable.** Every load-bearing claim I spot-checked cites a
source, and the chain resolves: the ~9.5 t SSO → `payload_and_block_upgrade.md`;
the ~300 kW ceiling → `wave5_synthesis.md` §2.4; the ~$20M launch →
`RESEARCH_TRACKER.md` "Founder input — wave 9"; the venture J-curve →
`data_science/INVESTOR_PROJECTION.md`; the ambition case → `economics/ambition_case.md`;
the radiator decision → `RESEARCH_TRACKER.md` "Founder input — wave 11". The
revision history (v1–v7) is complete and each entry explains what changed and
why. This is good practice and rule-compliant.

Two traceability soft-spots worth flagging:

- **T-1. The ~$20M internal launch cost is "traceable" only to a founder note,
  not to research.** CONCLUSION cites it to `RESEARCH_TRACKER.md` "Founder input
  — wave 9". The conclusion is *honest* about this — it lists the ~$20M figure
  as open unknown #4 and "not a published Rocket Lab figure." But it is the
  single largest driver of the Rev-4 sign-change in the economics, and it rests
  on a founder's back-of-envelope build-up, not a sourced research doc. The
  conclusion handles it correctly by flagging it; I note only that a load-bearing
  number traces to founder intuition, not to the research corpus, and a reader
  should understand that.

- **T-2. The ~85% Neutron first-stage cost-share** (CONCLUSION addendum, l.1254,
  l.1266–1268) is explicitly flagged in-text as "the project owner's — flagged
  for source-check … not an independently sourced number." Correctly disclosed;
  it is a traceability gap that the document itself owns. No fix needed beyond
  what is already there.

- **T-3. Thesis-as-source.** Several end docs cite `vision/initial_thesis.md`
  Rev 2/3/4 as a *source* (e.g. `strategy/optimized_strategy.md` Sources cites
  "initial_thesis.md — Rev 2, 3, 4"; CONCLUSION cites thesis revisions). Because
  the thesis is itself stale (S1), citing it as a current source is mildly
  circular and risks propagating the dead D-2…D-5 figures. The CONCLUSION mostly
  cites the *syntheses* and research docs directly, which is better; the thesis
  citations are low-stakes but worth noting.

No conclusion in CONCLUSION.md was found that "doesn't make sense / can't be
followed." The verdict, the configuration ladder, the five-part profitability
section, and the dual-case section all hang together logically.

---

## RULE COMPLIANCE (research-wiki / feasibility-forge conventions)

| Convention | Status |
|---|---|
| Thesis versioned by appended revisions, never overwritten | **Partial fail.** Revisions are correctly append-only (Rev 1 → 2 → 2.1 → 3 → 4 are all preserved). **But the thesis stopped at Rev 4** and was never updated for waves 6–11 — it is no longer a living record (S1). The append-only *mechanism* is honored; the *keep-it-current* obligation is not. |
| Every hard claim sourced | **Pass** for CONCLUSION.md and the syntheses — sourcing discipline is strong throughout. The ~$20M launch (T-1) and ~85% cost-share (T-2) trace to founder input, which is disclosed. |
| LIBRARY catalog current and complete | **Fail.** ~7 documents load-bearing for CONCLUSION Rev 5–7 are uncatalogued (S3). |
| RESEARCH_TRACKER current and complete | **Mostly pass, with stale spots.** The tracker's *index rows* (1–30, M1–M3, S1–S4, L1–L2, D1–D2, P1, C1) are complete and point at real files — good. But the C1 row says "v6" (D-15), the L2 row says "fix agents running" (D-16), the D1 row carries stale debate economics (D-6), and the wave-9 founder note carries a stale cost range (D-14). The narrative blocks are partly stale. |
| CONCLUSION carries a revision history | **Pass.** v1–v7 history present, ordered oddly (v7, v6, v5, v1, v2, v4, v3) but complete and each entry substantive. The ordering (l.1617 puts v1 between v5 and v2) is a cosmetic defect — the list is not in monotonic order. |
| CONCLUSION is a living, re-versioned state | **Pass.** Explicitly versioned, dated, with a "What would change this conclusion" section. |

One additional cosmetic compliance note: the **CONCLUSION revision-history
ordering is scrambled** (l.1521 v7, l.1552 v6, l.1589 v5, l.1617 v1, l.1624 v2,
l.1640 v4, l.1666 v3). All seven entries exist, but v1–v4 are out of sequence,
which makes the history hard to read.

---

## MINOR FINDINGS

- **M-1. "~5 km along-track string" vs. "≈8 satellites".** CONCLUSION's deployed-
  system strawman (l.1014) says "≈8 single-rack compute satellites in a single
  along-track string," consistent with `constellation_mesh.md`. But the
  *deployment path* in the same section (l.1052–1066) and the strategy doc
  describe a Phase-1 of "~3–4 nodes" and Phase-2 of "~12–24 nodes." The "≈8"
  strawman cluster is never explicitly reconciled with the "3–4 → 12–24" phase
  ladder — a reader must infer that "≈8" is illustrative. Not wrong, but the two
  node-count framings (8-sat strawman vs. 3–4/12–24 phases) sit side by side
  without a bridging sentence. Lint pass 2 §3 flagged the analogous "~4–8 vs.
  ~12–24" tension; it persists into the conclusion.

- **M-2. "first useful service ~4–8 nodes" survives in the syntheses and the
  strategy doc** (`wave5_synthesis.md` §5; `wave4_synthesis.md` §6;
  `optimized_strategy.md` §2.2 Phase 1). CONCLUSION Rev 6 re-scoped Phase 1 to
  **~3–4 nodes** and the minimum-viable deployment to ~3–5. The "~4–8 nodes"
  figure in the upstream docs is now superseded by the minimum-viable-scale
  finding but is not annotated there. Minor — the conclusion carries the
  corrected number.

- **M-3. `inference_scaling.md` "~120 kW" GB300 figure** — flagged by *both*
  lint passes (lint_report.md §1.6, lint_report_2.md §1.5 / P8) as the NVIDIA
  marketing figure the project agreed not to use. Still unfixed. Not in my
  assigned slice's end docs, but it is a lint item the conclusion-era project
  never closed; noting for completeness since the end docs depend on the
  ~135 kW figure.

- **M-4. Strategy doc Engineer §1.5 service-life note.** `optimized_strategy.md`
  §1.5 (l.205–215) says "the reliability research characterizes a *3-year* GPU
  economic/competitive life, not 5" and underwrites the GPU payload on a 3-year
  life. CONCLUSION Rev 3 makes 5 years the base case. The strategy doc's 3-year
  framing is consistent with `reliability_failure_handling.md` (which does say
  1–3 years) but **inconsistent with the conclusion's 5-year base case**. The
  CONCLUSION resolves this by treating 5 years as a *design requirement* the
  build-to-learn program must verify (and 3 years as the downside) — but the
  strategy doc and the conclusion describe the *same* node on *different*
  service-life bases without cross-referencing the reconciliation. Borderline
  significant; placed here because the conclusion's framing (5-yr requirement,
  3-yr downside) does technically encompass the strategy doc's stance.

- **M-5. README "Working thesis" box** (l.15–24) still describes the *original*
  pre-research thesis ("racks bolted in") with no pointer to how far the thesis
  has moved. It does say "to be refined" and links the thesis — acceptable, but
  combined with S1/S2 the entire README front-door is stale.

---

## SUMMARY

The project's actual conclusion — `CONCLUSION.md` Rev 7 — is in good shape:
internally consistent, fully sourced, carrying a complete revision history, and
traceable end-to-end. The verdict and its reasoning hold up.

The problem is the **end-document layer around it**. The most significant
finding: `vision/initial_thesis.md` was frozen at **Revision 4** and never
updated for waves 6–11, so it is three revisions and ~$ multiple stale — it
still costs nodes at the retired ~$55M launch price, still frames economics on
the abandoned 2–3-year GPU window, and still defines V2 as block-upgrade-
dependent, directly contradicting the conclusion. `README.md` is worse:
"27 docs / 2 sims / 2-round debate / conclusion at v2" — every count wrong.
`LIBRARY.md` omits ~7 documents that CONCLUSION Rev 5–7 depend on. The two lint
reports and the three-round debate all pre-date the launch-cost re-base and the
conclusion itself, and carry dead economic numbers (~5.3-yr payback, ~70%+
break-even premium, ~$85M node) with no superseded-banner. The
`RESEARCH_TRACKER.md` index rows are complete, but its D1/C1/L2 narrative rows
and the wave-9 founder note carry stale figures.

Traceability and rule compliance: the conclusion is traceable and rule-
compliant; the **thesis-versioning rule is half-honored** (append-only, but no
longer kept current) and the **LIBRARY-catalog-complete rule fails**. The dead
notes are concentrated upstream of the conclusion, not in it.

Confidence: **high**. The findings are mechanical cross-checks against the
project's own tracker and revision histories.
