# Consistency Review — Cross-File Audit of the `data_center/` Analysis

> **Historical layout note (2026-05-25).** This review audits an older
> data-center analysis shape where `CONCLUSION.md`, `CURRENT_STATE.md`, and the
> calculator lived in different locations. It is retained as a historical
> consistency review, not as current repository navigation.

*Reviewer: independent cross-file consistency peer reviewer. Date: 2026-05-18.
Scope: the `data_center/` analysis layer — `CONCLUSION.md` (v8),
`CURRENT_STATE.md`, the valuation set (`valuation/VALUATION_MODEL.md`, the
calculator, the two M5 reviews, `ai_compute_trajectory.md`,
`trajectory_notes.md`, the supporting `rklb_*` docs), the Python models
(`data_science/`, `simulations/`), `synthesis/`, `strategy/`, `debate/`,
`vision/` — cross-checked against the shared research wiki (`rocket_lab/`,
`node_design/`, `economics/`, `orbital/`, `laser_comms/`, `llm_compute/`).
Report-only — no audited file was edited. This document was the only file
created.*

> **What this audit is.** It hunts for *inconsistencies across files* —
> numbers given materially different values in two current documents,
> conclusions one doc overturned that another still asserts, calculator/model
> dials that disagree with the docs they cite. It deliberately distinguishes a
> **reconciled supersede** (an older doc that flags its own figure as
> superseded — *not* a defect) from an **unreconciled contradiction** (two
> current, both-live documents that simply disagree — a real defect). Only the
> latter is counted as a finding. The project's house discipline on superseded
> banners is genuinely good; most stale figures *are* banner-flagged. The
> findings below are the cases where that discipline broke.

---

## 0. Executive summary

**Overall consistency health: moderate, with one systemic, serious defect.**

The research wiki is internally tight. Physics numbers — Neutron SSO payload
(~9.5 t reusable working, 8.5–10.5 t band), node mass (1-rack ~6.8 t, 2-rack
~9.6–16.6 t over budget), the flyability ceilings (~200–250 / ~270–320 /
~430–470 kW), rack power/cost trajectories — reproduce consistently across
`payload_and_block_upgrade.md`, `node_mass_model.md`, `simulations/REPORT.md`,
`wave5_synthesis.md`, `ai_compute_trajectory.md` and the calculator. The
superseded-banner discipline is real and works: `VALUATION_MODEL.md`,
`data_science/REPORT.md`, and `wave5_synthesis.md §4.1` all carry honest,
specific superseded notes that a reader cannot miss.

**But the project has two parallel "answers" that were never reconciled, and
this is the dominant finding of the audit.** The orbital-DC venture is now
valued by *two* live models that give *opposite-signed* verdicts:

- **`CONCLUSION.md` (v8) and `INVESTOR_PROJECTION.md`** — the venture's central
  case is a **~$500M-revenue, ~$86M-profit business by year 10**, per-node
  payback ~2.5–2.8 yr, venture cumulative crossover ~year 19–20, ~$1.15B peak
  funding. A "mild loss to modestly positive" verdict.
- **The valuation calculator (M6, v3.1)** — the same venture, on its default
  central scenario, is a **capital sink**: DCF −$6.5B, net-of-capital −$0.7B,
  steady-state free cash flow −$0.82B/yr, per-rack margin −38%, peak capital
  draw $8.25B (`calculator/README.md` "Current default-run output";
  `CURRENT_STATE.md`).

`CURRENT_STATE.md` is explicit that the calculator (v3.1, finished 2026-05-18)
is the *current* tool and that `VALUATION_MODEL.md` (M5) is superseded — but
**`CONCLUSION.md`, the project's stated deliverable, never once mentions the
calculator, the flyability wall as a costed economic result, the DCF, or the
−$6.5B / −$0.82B-FCF numbers.** `CONCLUSION.md` v8 is dated 2026-05-17; the
whole valuation workstream (calculator v1→v3.1, the two M5 reviews,
`ai_compute_trajectory.md`) is dated 2026-05-17/18 and post-dates it. The
deliverable is one full workstream behind its own repo. This is **Finding 1**,
and it is the most serious item in this review: a reader who opens
`CONCLUSION.md` (as `README.md` and `CURRENT_STATE.md` both instruct) gets a
verdict the project's own newest model materially contradicts, with no pointer
to the disagreement.

**The most serious findings, in order:**

1. **`CONCLUSION.md` (the deliverable) is stale against the entire valuation
   workstream.** It carries the `INVESTOR_PROJECTION.md` J-curve as the
   venture's economics and never folds in — or even references — the
   flyability-enforced calculator that supersedes that model and reaches an
   opposite-signed (capital-sink) verdict. No superseded note, no pointer.
   *Unreconciled — and structural.*
2. **The `CONCLUSION.md` 5-year-life downside band (~3.5–7 yr) and the GPU
   service-life status disagree across the deliverable, the strategy doc, and
   the debate.** `CONCLUSION.md` runs a 3.5–7 yr band; `bear_case.md` R3.5
   concludes ~3.5–5 yr; `optimized_strategy.md §1.5` underwrites the GPU
   payload against a **3-year** life; the calculator's conservative scenario
   uses 3 yr. The reliability research models 3 yr throughout. The "5-year base
   case" is a defensible *choice*, but the band around it and its status
   (proven fact vs. unproven requirement) are stated inconsistently.
3. **The calculator's headline numbers and `CONCLUSION.md`'s headline numbers
   are not on the same basis and are never reconciled.** `CONCLUSION.md`'s
   ~$500M / ~$86M / ~year-19-20 figures are the *conservative gated*
   `INVESTOR_PROJECTION.md` case; the calculator's default scenario is an
   *ambition-scale* cadence (90 launches/yr at year 10). They are different
   scenarios, but nothing in either document maps one onto the other, so the
   numbers read as contradictory.
4. **The calculator's flyability finding contradicts `CONCLUSION.md`'s central
   reassurance** that V2 "closes on baseline Neutron + hot-loop." The
   calculator, with flyability enforced, makes the venture a sink *because* of
   the power-cap wall — and `CONCLUSION.md` does not carry that result at all.
5. **`VALUATION_MODEL.md` (M5) is correctly banner-flagged superseded, but the
   superseded banner and `CURRENT_STATE.md` describe a different "current"
   calculator version** (banner says "v3.1"; the calculator README's build
   narrative and "current default-run output" are also v3 — consistent — but
   `CURRENT_STATE.md` and `LIBRARY.md`/`RESEARCH_TRACKER.md` cataloguing should
   be checked to all say v3.1). Minor, but it is the kind of version drift that
   the rest of this audit shows the project is prone to.

The good news: none of these is a *physics* error or a broken citation into
the wiki. Every finding is a **reconciliation failure inside the
`data_center/` analysis layer** — the deliverable and the framing/strategy
docs were frozen at the `CONCLUSION.md`-v8 / thesis-Rev-6 vintage, and the
valuation workstream (calculator + reviews + trajectory) ran *after* them and
was never folded back. This is the *exact same failure pattern* the prior
`peer_review_4.md` and `triage_and_fix_plan.md` identified at the
Rev-7-vintage ("upstream framing documents frozen at an earlier wave") — it
has simply recurred one layer up, with `CONCLUSION.md` itself now the frozen
document.

---

## 1. Theme A — The deliverable vs. the valuation calculator (the central defect)

### A1 — `CONCLUSION.md` never folds in, or references, the valuation calculator

**Files:** `CONCLUSION.md` (v8, dated 2026-05-17); `CURRENT_STATE.md`;
`valuation/calculator/README.md`; `valuation/VALUATION_MODEL.md`.

`CURRENT_STATE.md` — the re-orientation doc, dated 2026-05-18 — describes the
calculator as the live, current valuation tool and gives its headline output:

> "**v3.1 — DONE (2026-05-18).** ... **Corrected default numbers (FY2036 /
> year 10): DCF −$6.5B** (was −$35B) · **net-of-capital −$0.7B · steady-state
> FCF −$0.82B/yr · per-rack margin −$16M / −38%.** ... at the conservative
> +50% premium the venture is a *mild* loss — roughly break-even on
> net-of-capital — premium-dependent ... with the flyability wall a real
> residual headwind."  — `CURRENT_STATE.md`

`VALUATION_MODEL.md`'s own superseded banner says the same:

> "**This model (the "M5" company model) is superseded by the valuation
> calculator at `calculator/` (model M6, currently v3.1).**"

But `CONCLUSION.md` — the document `README.md` calls "**the deliverable**" and
"**Start here for this workstream**" — contains **zero** references to the
calculator. A full-text search of `CONCLUSION.md` for "calculator", "M6",
"rklb-value", "DCF", "net of capital", "$6.5B", "$8.25B" returns nothing. Its
economics section (`Profitability` §1–6) is built entirely on
`INVESTOR_PROJECTION.md` and `synthesis/wave5_synthesis.md`, and its headline
venture verdict is:

> "the venture reaches a **~$500M-revenue, ~$86M-annual-profit business by
> year 10** ... its **cumulative cash-flow crossover ... falls at roughly year
> 19–20**, behind a **peak funding requirement of ~$1.15B**."
> — `CONCLUSION.md` Revision 5 / Profitability §5

**Verdict — unreconciled, and the most serious finding in this review.** The
project's stated deliverable is one entire workstream out of date. The
calculator is described by `CURRENT_STATE.md` as the *corrected successor* to
the valuation work, it enforces flyability (which `CONCLUSION.md` itself
treats as the central physical constraint), and on its default central case it
reaches an **opposite-signed verdict** to `CONCLUSION.md`'s "mild loss to
modestly positive at +50% premium" — a DCF of −$6.5B and a steady-state FCF of
−$0.82B/yr. A reader directed to `CONCLUSION.md` cannot discover any of this.
At minimum `CONCLUSION.md` needs a new revision (v9) that folds in the
calculator results, or — if a full fold-in is deferred — an explicit banner
pointing to the calculator as the current valuation tool and flagging that the
flyability-enforced economics are materially worse than the
`INVESTOR_PROJECTION.md` J-curve the document currently carries. This is the
same defect class `peer_review_4.md` flagged ("upstream documents frozen at an
earlier wave") — but it has now reached the deliverable itself.

### A2 — The two live models give opposite-signed venture verdicts, on bases that are never mapped onto each other

**Files:** `CONCLUSION.md` / `INVESTOR_PROJECTION.md` vs.
`calculator/README.md` / `calculator/scenarios/default.yaml`.

The two models are not the same scenario, and that is the root of the
confusion — but *nothing in the analysis layer reconciles them*, so they read
as a flat contradiction.

| | `INVESTOR_PROJECTION.md` / `CONCLUSION.md` central case | Calculator `default.yaml` (M6 v3.1) |
|---|---|---|
| Cadence at year 10 | ~7 nodes/yr deployed, ~35 live nodes | ~90 launches/yr; 295 racks deployed over the horizon |
| Verdict | ~$500M rev, ~$86M profit yr 10; crossover ~yr 19–20; +50% premium ≈ "mild loss to modestly positive" | DCF −$6.5B; net-of-capital −$0.7B; steady-state FCF −$0.82B/yr; per-rack margin −38% |
| Premium | +50% central | +50% central (same dial) |
| Service life | 5 yr | 5 yr (same) |
| Flyability | not modelled as a cost — `CONCLUSION.md` asserts V2 "closes on baseline Neutron + hot-loop" | enforced — power-capped to ~23% of flagship at the horizon; this is *why* the venture is a sink |

The calculator's default is essentially the **ambition-scale cadence** (its
`launches_at_year_10: 90` traces to `ambition_case.md`'s ~85–110/yr), whereas
`INVESTOR_PROJECTION.md` is the **conservative gated** ramp (~7 nodes/yr). So
the two are *deliberately* different scenarios. The defect is not that they
differ — it is that **no document states this and maps them**. A reader
holding `CONCLUSION.md` (conservative, "modestly positive") and the calculator
(ambition cadence, −$6.5B DCF) has no way to know they are answering different
questions. The calculator README's "honest reading" section explains the
flyability sink mechanically, and `CONCLUSION.md` explains the J-curve — but
neither says "these are two scenarios; here is how the conservative case looks
in the calculator and the ambition case looks in `INVESTOR_PROJECTION.md`'s
terms." `VALUATION_MODEL.md §7` has a "how this model relates to the others"
table that is exactly the right instrument — and the calculator and
`CONCLUSION.md` both lack it.

**Verdict — unreconciled.** Needs a single reconciliation note (best placed in
`CONCLUSION.md`'s new revision, or in `calculator/README.md`) that states: the
calculator's default is the ambition-cadence scenario; `INVESTOR_PROJECTION.md`
is the conservative-gated scenario; running the calculator at a conservative
cadence (≈ `scenarios/conservative.yaml`, which gives DCF ≈ −$5.0B) is the
apples-to-apples comparison — and even *that* is a sink, which is itself a
finding `CONCLUSION.md` does not currently carry.

### A3 — The flyability wall is a costed *economic* result in the calculator but only a *physical* caveat in `CONCLUSION.md`

**Files:** `calculator/README.md` ("The honest reading of the v3 default
case"); `CONCLUSION.md` ("The configuration ladder"; Profitability §4).

The calculator's central finding is that flyability enforcement *makes the
venture a sink*:

> "The mature **steady-state free cash flow is negative** (~$-0.8B/yr) on the
> central dials: even a right-sized power-capped node does not quite earn back
> its node capital ... The venture, valued honestly against the flyability
> ceiling, is a **mild capital sink at the 12.5 t SSO payload**."
> — `calculator/README.md`

`CONCLUSION.md`, by contrast, treats the flyability wall as a *physical*
constraint that the architecture *clears*:

> "**V2 closes on baseline Neutron + hot-loop — it does not depend on the
> block-upgrade** ... The baseline-Neutron + hot-loop ceiling of ~270–320 kW
> (working ~300 kW) flies a **power-capped Vera Rubin node (~190–250 kW)** with
> margin."  — `CONCLUSION.md`, configuration-ladder section

These are not contradictory *as physics* — a power-capped node does fly. But
they are contradictory *as economics*: `CONCLUSION.md` presents "V2 closes" as
a positive verdict, while the calculator shows that the very power-capping that
keeps the node flyable also strands its launch/bus cost and turns the
steady-state cash flow negative. `CONCLUSION.md`'s `CURRENT_STATE.md` summary
even concedes this ("the flyability wall a real residual headwind") — but
`CONCLUSION.md` itself does not. `CURRENT_STATE.md` knows the answer;
`CONCLUSION.md` was written before it.

**Verdict — unreconciled.** When `CONCLUSION.md` is re-versioned, the
"V2 closes on baseline Neutron + hot-loop" framing must be reconciled with the
calculator's finding that the *economics* past the power-cap wall are a
residual sink. The honest synthesis is `CURRENT_STATE.md`'s own wording: it
flies, but the power-capped node amortizes its fixed launch/bus poorly — a real
headwind, not a clean close.

---

## 2. Theme B — Service life: the 5-year base case, its band, and its status

The "5-year GPU service life" is the project's single most load-bearing
economic dial. The *choice* of 5 years as the base case is consistent across
the corpus and is not a defect. But three things around it are stated
inconsistently across current documents.

### B1 — The downside band: `CONCLUSION.md` says 3.5–7 yr; `bear_case.md` says 3.5–5 yr

**Files:** `CONCLUSION.md` (Profitability §2, "Honest risks") vs.
`debate/bear_case.md` R3.5.

`CONCLUSION.md` repeatedly states the honest service-life band as **3.5–7
years**:

> "The honest outcome band, pending V1 flight data, is **~3.5–7 years** — and
> the economics fail at the bottom of it."  — `CONCLUSION.md` Profitability §2

`bear_case.md` — which `CONCLUSION.md` cites as a converged input and treats as
authoritative — concludes a **narrower, lower** band:

> "The honest outcome band is **~3.5–5 years**, resolved only by [V1 flight
> data]."  — `bear_case.md` R3.5
> "service life must hit ~5 years (not the ~3.5–4 yr the coolant-loop and
> Rubin-HBM [analysis suggests])"  — `bear_case.md`

So the Bear's final position caps the band at ~5 years; `CONCLUSION.md` extends
it to 7 years (and adds a dedicated "~7-year upside case"). The 7-year upside
is sourced in `CONCLUSION.md` to terrestrial hyperscaler depreciation
(`bull_case.md` R3.2: 6-year schedules) — which is a real datapoint — but
`trajectory_notes.md` records the founder's own position that **7 years has
"diminishing returns" and satellites are "unlikely to last past ~7"**, and the
Bear explicitly does *not* grant a 7-year case. The result: the deliverable's
service-life band (3.5–7) is wider on *both* the doc it cites as its adversary
(3.5–5) and the founder's own recorded view.

**Verdict — unreconciled, moderate.** Not a numeric error so much as an
unreconciled range. `CONCLUSION.md` should either (a) state that it is
*extending* the Bear's 3.5–5 band to 3.5–7 on the strength of the hyperscaler
depreciation evidence and say so explicitly, or (b) pull the upside in to match
the Bear. As written, a reader cross-checking `CONCLUSION.md` against
`bear_case.md` finds two different "honest bands."

### B2 — The strategy doc underwrites the GPU payload against a 3-year life

**Files:** `strategy/optimized_strategy.md §1.5` vs. `CONCLUSION.md`
Profitability §2.

`optimized_strategy.md` — a current document, cited by `CONCLUSION.md`
Revision 6 as the converged build strategy — says, in a boxed "Service-life
note":

> "The reliability research characterizes a *3-year* GPU economic/competitive
> life, not 5. The strategy distinguishes the two: the **GPU payload** is
> underwritten against a ~3-year revenue-generating life ... the **bus, power,
> comms and structure** are qualified for ~5+ years."
> — `optimized_strategy.md §1.5`

`CONCLUSION.md` Profitability §2 makes the 5-year life "the explicit base case
the main analysis runs on" and the revenue model runs over a 5-year declining
curve. So the deliverable's revenue model runs the *GPU* over 5 years, while
the converged strategy it cites underwrites the *GPU payload* over 3.

This is partly a genuine analytical distinction (the strategy separates
payload-economic-life from bus-qualification-life) and partly an unreconciled
disagreement: `optimized_strategy.md §1.5` flatly says "a *3-year* GPU
economic/competitive life, not 5," which contradicts `CONCLUSION.md`'s base
case. `optimized_strategy.md §1.6` and §2.1 also repeatedly reference "a 3-year
un-serviceable node" and "~15–25% cumulative GPU loss over 3 years." The
strategy doc was written across the same wave as `CONCLUSION.md` Rev 6 but
carries the *reliability research's* 3-year framing without reconciling it to
the 5-year base case `CONCLUSION.md` adopts.

**Verdict — unreconciled, moderate.** The reliability research
(`node_design/reliability_failure_handling.md`) genuinely models 3 years
throughout — `review_engineer.md` Finding 2 makes exactly this point about the
calculator ("the reliability doc models a 3-year life ... the 5-year figure is
a management/economics choice layered on top"). The project needs *one* stated
position: either the 5-year life is the base case and the strategy doc's
"3-year GPU economic life" language is updated to match, or the 3-year
reliability basis is the planning number and `CONCLUSION.md`'s 5-year base case
is explicitly a *stretch*. Right now the deliverable and the strategy doc it
cites say different things in the same breath.

### B3 — The calculator's "CITED" tag on the 5-year life is exactly the mis-tag `review_engineer.md` flagged — and it was carried forward unfixed

**Files:** `calculator/scenarios/default.yaml` (`node.service_life_years`);
`valuation/review_engineer.md` Finding 2.

`review_engineer.md` Finding 2 (HIGH) — a review the calculator's own README
says it "bakes in" — explicitly flagged that tagging the 5-year life `CITED` is
"materially misleading about the *status* of the number" and recommended:
"re-tag it `ASSUMPTION — proposal minimum requirement, not yet demonstrated;
honest band 3.5–7 yr`."

The calculator's `default.yaml` still tags it, in effect, as the cited base
case:

> "`service_life_years: 5` ... **THE SINGLE HIGHEST-SENSITIVITY DIAL** ...
> Source: this is the BASE CASE = 5 years. Basis: the project owner's standing
> directive ... and `CONCLUSION.md` §2's honest 3.5-7 yr band."
> — `default.yaml`, `node` block

This is better than M5's flat `CITED` (it does name the band and the
"directive" basis), so it is a *partial* fix — but `review_engineer.md`'s
specific recommendation was to label it an unproven *requirement*, and the YAML
still frames it as "the BASE CASE." The calculator README claims it bakes in
the M5 review corrections; on this specific item the fix is incomplete.

**Verdict — partially reconciled / minor.** The calculator did improve the
tag's documentation but did not fully adopt `review_engineer.md` Finding 2's
recommended framing. Low materiality (the dial value is right; the conservative
scenario does run 3 years as the review asked) — flagged because it shows the
"bakes in every review fix" claim in `calculator/README.md` is slightly
overstated.

---

## 3. Theme C — Within the valuation set (M5, its reviews, trajectory docs, the calculator)

This is the cluster the brief specifically asked about. The headline here is
*good*: the calculator genuinely does carry most of the M5 review corrections,
and `VALUATION_MODEL.md` carries an honest superseded banner. The findings are
narrower.

### C1 — `VALUATION_MODEL.md` (M5) is correctly superseded — this is a reconciled supersede, not a defect

**Files:** `valuation/VALUATION_MODEL.md` (banner); `review_economist.md`;
`review_engineer.md`; `calculator/README.md`.

For the record, so it is not mis-counted as a contradiction: `VALUATION_MODEL.md`
carries a prominent, specific superseded banner ("⚠️ SUPERSEDED — do not cite
the headline numbers"), names the M5→M6 succession, lists the five review
defects (depreciation bug, unfinanced cost of capital, 285/yr cadence, 5-year
life treated as fact, 2 racks/launch), and tells the reader to use the
calculator. The calculator README's correction table maps each review finding
to an `engine.py` location. **This is the superseded-discipline working
correctly.** M5's ~$9–13B venture-operating-profit headline and its 285/yr
cadence are *not* a live contradiction with anything — they are explicitly
retired. No finding.

### C2 — The calculator's launch-cost dial ignores `review_economist.md` Finding 7 and `review_engineer.md` Finding 7

**Files:** `calculator/scenarios/default.yaml` (`node.launch_cost_musd` = 20,
`trajectory.launch_cost_growth` = −0.02); `review_economist.md` Finding 7;
`review_engineer.md` Finding 7; `rklb_forward_trajectory.md §2.2`.

Both M5 reviews flagged the flat $20M internal launch cost.
`review_economist.md` Finding 7 (MODERATE) recommended replacing the flat value
with a **cadence-indexed curve** (~$25M at low cadence → ~$10M at high cadence)
and said "if a flat value is retained ... stop calling it 'conservative'."
`review_engineer.md` Finding 7 noted $20M is *below* the only anchored
datapoint (`rklb_forward_trajectory.md §2.2`: the 50%-margin-at-24-launches
target implies **~$25M/launch**).

The calculator did **not** adopt the cadence-indexed curve. It carries a flat
$20M base compounded *down* at −2%/yr — i.e. it makes launch cost *fall* with
calendar time, not with cadence, and never reaches the ~$25M low-cadence figure
the reviews said is the only sourced anchor. The `default.yaml` comment is
honest about the gap ("CAVEAT: no public figure exists; `rklb_forward_trajectory.md`
S2.2 notes the 50%-margin target IMPLIES ~$25M"), so it is *disclosed* — but
the disclosed-and-unfixed status is itself the inconsistency: the calculator
README says it "bakes in the corrections from the two independent reviews,"
and on launch cost it does not. The trajectory layer's −2%/yr launch decline
also traces only to `trajectory_notes.md`'s informal "may trend flat-to-down,"
not to a sourced figure, while the *sourced* direction (low-cadence early
launches cost *more*) is the opposite.

**Verdict — unreconciled, minor-to-moderate.** The calculator's launch-cost
treatment contradicts both M5 reviews' recommendation and the only sourced
datapoint. Either implement the cadence-indexed curve, or — at minimum —
correct the `calculator/README.md` claim that it bakes in *all* the review
corrections (it bakes in the cadence-ceiling, depreciation, premium-on-premium
and capital-draw fixes, but not Finding 7).

### C3 — `ai_compute_trajectory.md`'s rack-cost growth and the calculator's `rack_cost_growth` dial: a reconciled, well-documented divergence

**Files:** `ai_compute_trajectory.md §1`, `trajectory_notes.md` Wave-14;
`calculator/scenarios/default.yaml` (`trajectory.rack_cost_growth` = 0.37).

`trajectory_notes.md` Wave-14 records the founder's framing: "Rack cost rises
~75–100%/yr (≈2×/generation)." `ai_compute_trajectory.md §1` projects ~2×/~12–18-month
generation. The calculator uses `rack_cost_growth: 0.37`/yr. The `default.yaml`
comment handles this explicitly and correctly:

> "the founder's verbal '~75-100%/yr (~2x/gen)' overshoots S1's own table by
> ~3x at 2036; S1 brackets the projection at '~1.5x/gen (conservative) to
> ~2x/gen (trend)', and 0.37/yr is the table-implied ~1.5x per ~1.5-yr
> generation."

This is the project resolving an apparent contradiction *in the open*, in the
dial documentation — a model of how it should be done. **Not a finding** —
flagged here only as the positive counter-example, and because the brief asked
about exactly this cluster. The calculator's 0.37/yr is internally consistent
with `ai_compute_trajectory.md §1`'s table (it lands the 2036 flagship at
~$140M, the table's band-mid). No defect.

### C4 — `data_science/REPORT.md` (model M2) is superseded and correctly banner-flagged — reconciled

**Files:** `data_science/REPORT.md` (banner); `simulations/REPORT.md`;
`wave5_synthesis.md §2.2`.

`data_science/REPORT.md` carries a long, specific superseded banner: it states
its ~163 kW crossover, its node masses (150 kW node at ~8.4 t), and its
"GB300 is the last flyable generation / move now" verdict are all on
pre-wave-5 inputs, and it explicitly defers to `simulations/REPORT.md` (which
puts the same node at ~6.79 t) as "the authoritative node-mass source." This
is a clean reconciled supersede. **Not a finding.** Worth noting only because
`data_science/REPORT.md`'s un-superseded body still reads as alarming ("the
generations worth flying are the ones you can't fly") — the banner is
load-bearing and a reader who skips it would be misled, but the banner *is*
there and is unmissable.

### C5 — The M5 reviews are dated 2026-05-17; they review a model the project had not yet superseded — internally consistent

`review_economist.md` and `review_engineer.md` are both dated 2026-05-17 and
review `VALUATION_MODEL.md` as a live document. The calculator (M6) then
"bakes in" their findings. The sequencing is M5 → reviews → M6, and every
document is self-consistent about its place in that chain. **No finding** —
recorded so the reviews are not mistaken for stale docs (they describe M5
accurately; M5 is correctly retired; the only gap is C2, the launch-cost fix
the calculator skipped).

---

## 4. Theme D — Cadence, fleet size, and the Neutron ceiling

### D1 — The calculator's cadence ceiling (150/yr) and `CONCLUSION.md`'s Neutron-ceiling reasoning are consistent — reconciled

**Files:** `calculator/scenarios/default.yaml` (`cadence.cadence_ceiling` =
150); `CONCLUSION.md` (moonshot section); `review_engineer.md` Finding 1.

`review_engineer.md` Finding 1 (CRITICAL) demolished M5's 285/yr ramp as
"physically incredible" (above the three-pad ~209/yr Falcon 9 theoretical
ceiling). The calculator's `cadence_ceiling: 150` is explicitly the fix —
documented as "below SpaceX's 2025 record of 165" and traced to
`review_engineer.md` Finding 1. `CONCLUSION.md`'s moonshot section
independently uses the same reference points (SpaceX 165 in 2025; ~209/yr
three-pad ceiling). These line up. **Not a finding** — the M5 285/yr cadence is
a reconciled supersede.

### D2 — The calculator's default cadence (~90/yr at year 10) sits above `CONCLUSION.md`'s conservative-case cadence and `rklb_forward_trajectory.md`'s market — disclosed, but it drives D-A2

**Files:** `calculator/scenarios/default.yaml` (`launches_at_year_10: 90`);
`CONCLUSION.md` conservative case (<7 nodes/yr); `rklb_forward_trajectory.md §5`.

The calculator's *default* (not its conservative scenario) anchors year-10
cadence at 90 launches/yr — explicitly the ambition-case rate. `CONCLUSION.md`'s
conservative case caps deployment "below ~7 nodes/yr." `rklb_forward_trajectory.md §5`
states the contestable external launch market is only ~30–50/yr and Rocket
Lab's published plan tops out at ~12/yr. So the calculator's *default scenario*
models the *ambition* cadence — which is a legitimate modelling choice (the
calculator has a `conservative.yaml` for the other case), and the YAML
documents it ("Source: `ambition_case.md` S2"). The inconsistency is not within
the calculator; it is that the *calculator's default* and the *`CONCLUSION.md`
headline* are different scenarios presented as each project's central answer.
This is the mechanism behind Finding A2 and is not a separate defect — flagged
here so the cadence dimension of A2 is explicit: the two "central cases"
differ by roughly 13× in deployment rate.

**Verdict — the disclosure is fine; the cross-document framing is the problem
(see A2).**

### D3 — `VALUATION_MODEL.md`'s "2 racks/launch from year 5" vs. the calculator's derived 2→1 — reconciled supersede, with one residual

**Files:** `VALUATION_MODEL.md §3.2`; `review_engineer.md` Finding 3;
`calculator` (racks-per-launch derived); `node_mass_model.md §6`.

`review_engineer.md` Finding 3 (HIGH) flagged M5's "2 racks/launch from year 5"
as contradicting `node_mass_model.md` (a 2-rack node is ~9.6–16.6 t, over even
the expendable budget). The calculator fixes this properly: racks-per-launch is
*derived* from the flown node mass against the SSO payload, and the README and
`engine.py` are explicit that the 2→1 reversal is "produced by the rising
rack-power curve, not hand-set." M5's "2 racks/launch" is correctly retired by
its superseded banner. **Mostly reconciled.**

One residual worth a line: the calculator's `vehicle.max_racks_per_launch: 2`
still permits 2 racks on a launch for the *lightest early* node, and the README
says "racks-per-launch ... starts at 2 (a light GB300-class node)." But
`node_mass_model.md §6`, `simulations/REPORT.md §4`, and `CONCLUSION.md`
("the architecture stays 1 rack per node, 1 node per launch *at every rung*")
are unanimous that **even a GB300-class 2-rack node (~12.75 t) does not fly on
a reusable Neutron** — `simulations/REPORT.md §4` shows the 2-rack GB300 node
at 12.75 t against the 9.5 t reusable budget, "134% — OVER." So the calculator
*allowing* a derived value of 2 for an early light node is in mild tension with
the rest of the corpus, which says 1 rack/launch holds universally. In
practice the calculator's node-mass physics may never actually return 2 (the
default node at 140 kW masses well over half the 12.5 t payload), so this may
be inert — but `max_racks_per_launch: 2` as a permitted ceiling, and the
README's "starts at 2," read as inconsistent with the unanimous "1 rack/launch
at every rung" finding.

**Verdict — reconciled supersede on the main point; minor unreconciled
residual** on whether 2 racks/launch is ever physical. Recommend either setting
`max_racks_per_launch: 1` (consistent with the corpus) or documenting in the
YAML why a derived 2 is permitted when `node_mass_model.md` rules out a 2-rack
*node* — and confirming the engine never actually returns 2 on the default
dials.

### D4 — The "~$5–10B/yr Neutron ceiling" is consistent across `CONCLUSION.md`, `cadence_revenue_model.md`, and the moonshot docs — reconciled

`CONCLUSION.md` Revision 8 ("on Neutron this venture tops out at ~$5–10B/yr"),
`cadence_revenue_model.md §6` ("~$5–15B/yr ... ~$10B/yr by year 12"),
`moonshot_50b.md §7` ("~$3–8B/yr"), and `moonshot_150b.md §7.3` ("~$7–10B/yr")
all converge on a single-digit-to-low-teens-billions Neutron ceiling. The
ranges overlap and the documents cross-cite consistently. **Not a finding** —
this is the corpus agreeing. (Note one small loose end: `CONCLUSION.md` cites
"`moonshot_50b.md` §7: ~$3–8B" — which is the *low* end of its own ~$5–10B
headline; the documents are consistent but `CONCLUSION.md`'s ~$5–10B is the
union of the two moonshot docs' ranges, slightly rounded. Immaterial.)

---

## 5. Theme E — Mismatched assumptions: calculator/model dials vs. the docs

### E1 — The calculator's revenue anchor ($13M owner-operator) vs. `INVESTOR_PROJECTION.md` / `VALUATION_MODEL.md` ($16M inference-service) — a deliberate, documented divergence, but `CONCLUSION.md` does not carry it

**Files:** `calculator/scenarios/default.yaml` (`revenue.owner_operator_anchor_musd`
= 13); `INVESTOR_PROJECTION.md` ($16M base); `VALUATION_MODEL.md §3.4` ($16M);
`review_economist.md` Finding 5; `ai_compute_trajectory.md §7.3`.

`review_economist.md` Finding 5 (MAJOR) flagged that M5's $16M anchor is the
*inference-service* rate, already elevated above the IaaS rack rate, so adding
a +50% premium on top risks a premium-on-a-premium. The calculator adopts the
fix: it re-anchors to a **$13M owner-operator** rate (mid of `ai_compute_trajectory.md §7.3`'s
~$11–16M owner-operator band) with the premium as a separate dial. This is a
genuine, correct correction, well-documented in the YAML.

But the consequence is that the calculator's revenue base is **~$3M/rack-yr
lower** than the base in `INVESTOR_PROJECTION.md` and `VALUATION_MODEL.md`, and
**`CONCLUSION.md` still carries the $16M inference-service anchor** throughout
its Profitability section ("~$25–50B/GW-yr gross inference-service
(~$16M/rack-yr)"; "the V2 inference-service mid revenue ~$16M/rack-yr"). So the
deliverable's revenue model and the current calculator's revenue model differ
at the anchor — and `CONCLUSION.md` gives no hint that the valuation workstream
re-based the anchor downward and treated the $16M figure as already
premium-inclusive. This is a *component* of Finding A1 (deliverable stale
against the valuation workstream) but is called out separately because it is a
specific, load-bearing number — the revenue anchor — given two different values
($13M vs $16M) in two current documents, with the lower one being the corrected
one and the deliverable carrying the uncorrected one.

**Verdict — unreconciled.** The calculator's $13M re-anchoring is correct and
well-sourced; `CONCLUSION.md`'s $16M is the figure the M5 economist review
flagged as a premium-on-a-premium trap. The deliverable needs to adopt (or
explicitly address) the re-anchored figure.

### E2 — Service life, SSO payload, premium, ground segment: the calculator's dials are consistent with the docs — reconciled

For balance and completeness, the dials that *do* line up:

- **SSO payload.** `default.yaml` `sso_payload_tonnes: 12.5` (block-upgraded)
  with reference figures 9.5 / 11 / 12.5 t — matches
  `payload_and_block_upgrade.md` and `wave5_synthesis.md §2.1` exactly.
- **Orbital premium.** +50% headline / +15% floor — matches
  `INVESTOR_PROJECTION.md`, `hyperscaler_margins.md §3`, and `CONCLUSION.md`'s
  steady-state figure.
- **Ground segment.** $150M, 10-yr amortization — matches `CONCLUSION.md §4`
  Revision 6 ("built lean toward the ~$150M low end") and
  `INVESTOR_PROJECTION.md`.
- **Node opex.** $1.5M/node-yr — matches `INVESTOR_PROJECTION.md` and
  `CONCLUSION.md §5`.
- **R&D ramp.** $90M peak → $40M tail — matches `INVESTOR_PROJECTION.md`'s
  ~$485M-over-11-years front-loaded ramp.
- **Node base costs.** rack $6M, spacecraft $18M, launch $20M — matches
  `CONCLUSION.md §1` Revision-4 build-up.

These are genuine consistency successes and are the reason this audit's verdict
is "moderate health, one systemic defect" rather than "broadly inconsistent."
The calculator's *static base-year inputs* are well-reconciled to the docs; the
problem is entirely that the calculator's *flyability-enforced trajectory
output* (a sink) was never propagated back into `CONCLUSION.md`.

### E3 — One internal-launch-cost figure, three values across the corpus — partially reconciled, worth a note

**Files:** `CONCLUSION.md` (~$20M base, $10–20M range, $55M sensitivity);
`rklb_forward_trajectory.md §2.2` (~$25M implied); `VALUATION_MODEL.md §3.5`
($20M working, ~$25M documented alternative); `calculator` ($20M base);
`ambition_case.md §3` ($20M → ~$10M with cadence).

The internal Neutron launch cost appears as ~$10M, ~$20M, ~$25M, and ~$55M
across the corpus. This is *mostly* reconciled — each document is clear about
which figure it uses and why ($20M = founder wave-9 working value; $55M =
external customer price / sensitivity; ~$25M = the 50%-margin-at-24-launches
implied figure; ~$10M = high-cadence amortized). The peer_review_3.md already
flagged `economics/rack_cost_trajectory.md` for running on the stale $50–55M
basis. The residual inconsistency: `rklb_forward_trajectory.md §7` explicitly
issues a **CORRECTION** — "the project's ~$15–20M figure ... is *not* supported
as a near-term or 24/yr-cadence number ... near-term internal cost ~$25M" — and
both `CONCLUSION.md` and the calculator nonetheless use $20M as the *base*
case, with ~$25M only as a sensitivity or a YAML comment, not the base. So the
project's own sourced forward-trajectory doc says the base should be ~$25M, and
the deliverable + calculator keep it at $20M. `CONCLUSION.md` does list "the
~$20M internal launch cost itself" as open unknown #4 and flags it is not a
published figure — so it is *disclosed* — but the specific `rklb_forward_trajectory.md §7`
correction ("$15–20M not supported as a near-term number") is not reflected in
the choice of base case.

**Verdict — partially reconciled / minor.** Not a flat contradiction (every
doc discloses its figure), but the deliverable's $20M base case sits against an
explicit "correct this upward to ~$25M" in a current sourced doc. Either adopt
~$25M as the near-term base (with $20M as the high-cadence figure), or have
`CONCLUSION.md` acknowledge the `rklb_forward_trajectory.md §7` correction
where it sets the base case.

---

## 6. Theme F — Unsupported / loosely-supported claims in the analysis layer

### F1 — `CONCLUSION.md`'s "$250B inference-services" market — supported, with a caveat on precision

**Files:** `CONCLUSION.md` (Revision 7/8, repeated); `economics/ai_datacenter_tam.md §4`.

`CONCLUSION.md` repeatedly cites "~156 GW / ~$250B 2030 AI-inference market."
`ai_datacenter_tam.md` does support a ~$250B figure — §115: "MarketsandMarkets
~$255B by 2030; Grand View ~$254B; ... converge near ~$250B by 2030." And the
156 GW is `ai_datacenter_tam.md §3` (McKinsey AI-specific demand). **So the
claim is sourced and survives.** The one looseness: `CONCLUSION.md` writes
"~156 GW (~$250B-inference-services)" as if the $250B is the dollar value *of*
the 156 GW — but in the source they are two different metrics (156 GW is
AI-specific *capacity*; $250B is the inference *services/hardware market by
revenue*, and the inference *capacity* slice is ~90–93 GW, not 156 GW).
`ai_datacenter_tam.md §138` itself flags the GW↔$ bridge as "a crude proxy."
The numbers are individually correct; the *phrasing* conflates a capacity
figure and a revenue figure. Low materiality.

**Verdict — supported; minor phrasing imprecision.** Not a defect in substance.

### F2 — `CONCLUSION.md`'s "~85% first-stage cost-share" — correctly flagged as unsourced (good practice, noted for completeness)

`CONCLUSION.md`'s Starship addendum uses "~85% of Neutron vehicle cost in the
reusable first stage" and explicitly flags it: "the ~85% first-stage cost-share
figure is the project owner's — flagged for source-check; it is not an
independently sourced number." This is the project being honest about an
unsourced claim. **Not a finding** — flagged here only as a positive
counter-example of the discipline the rest of this review finds lapsing
elsewhere.

### F3 — The "V2 closes" claim and the "buildout-limited, not demand-limited" claim — sourced to the syntheses, but now in tension with the calculator

`CONCLUSION.md`'s two most quotable verdicts — "V2 closes on baseline Neutron +
hot-loop" and "the venture is buildout-limited, not demand-limited" — both
trace cleanly to `wave5_synthesis.md` and `ambition_case.md` respectively, and
*were* well-supported when written. The calculator does not overturn
"buildout-limited" (it agrees demand is not the constraint). But it *does*
materially qualify "V2 closes": per Finding A3, the calculator shows the
flyability-enforced economics are a residual sink. So "V2 closes" is no longer
*unsupported* so much as **superseded-but-unmarked** — the synthesis that
supports it predates the flyability-enforced calculator. This is the same
defect as A1/A3; recorded here under "unsupported claims" because, read today
against the full corpus, "V2 closes" is a claim the project's newest model does
not support, and `CONCLUSION.md` carries it with no caveat.

**Verdict — see A1/A3; the claim needs a caveat or a re-version.**

---

## 7. Prioritized fix list

Ranked by materiality. Items 1–4 are the substantive ones; 5–9 are hygiene.

| # | Fix | Files | Severity |
|---|---|---|---|
| 1 | **Re-version `CONCLUSION.md` (→ v9) to fold in the valuation calculator.** The deliverable must carry the calculator's flyability-enforced result (DCF −$6.5B, steady-state FCF −$0.82B/yr, net-of-capital −$0.7B at the conservative +50% premium) and reconcile it with the `INVESTOR_PROJECTION.md` J-curve it currently presents. If a full fold-in is deferred, add an interim banner at the top of `CONCLUSION.md` pointing to the calculator as the current valuation tool and stating the flyability-enforced economics are materially worse than the document's current numbers. | `CONCLUSION.md` | **Critical** |
| 2 | **Add a model-reconciliation note** stating that the calculator's `default.yaml` is the *ambition-cadence* scenario and `INVESTOR_PROJECTION.md` is the *conservative-gated* scenario — and give the apples-to-apples cross-read (the calculator's `conservative.yaml`, DCF ≈ −$5.0B). Best placed in the new `CONCLUSION.md` revision; a `VALUATION_MODEL.md §7`-style "how the models relate" table is the right instrument and both the calculator README and `CONCLUSION.md` lack it. | `CONCLUSION.md`, `calculator/README.md` | **Critical** |
| 3 | **Reconcile the GPU service-life position.** Pick one: (a) the 5-year life is the base case and `optimized_strategy.md §1.5`'s "3-year GPU economic life" language is updated to match; or (b) the 3-year reliability basis is the planning number and `CONCLUSION.md`'s 5-year base case is explicitly labelled a stretch. Also reconcile the band: `CONCLUSION.md` says 3.5–7 yr, `bear_case.md` R3.5 says 3.5–5 yr — state which is the project position and why. | `CONCLUSION.md`, `optimized_strategy.md`, `bear_case.md` | **Major** |
| 4 | **Reconcile the revenue anchor.** The calculator uses a $13M owner-operator anchor (the corrected, premium-separated figure per `review_economist.md` Finding 5); `CONCLUSION.md` and `INVESTOR_PROJECTION.md` use $16M inference-service. `CONCLUSION.md` should adopt the re-anchored figure or explicitly explain why it retains $16M (and that $16M is already premium-inclusive). | `CONCLUSION.md`, `INVESTOR_PROJECTION.md` | **Major** |
| 5 | **Fix the calculator's launch-cost treatment, or correct the README claim.** The calculator skips `review_economist.md`/`review_engineer.md` Finding 7 (cadence-indexed launch-cost curve). Either implement the curve, or amend `calculator/README.md`'s claim that it "bakes in the corrections from the two independent reviews" to note Finding 7 is not implemented. | `calculator/`, `calculator/README.md` | Moderate |
| 6 | **Reconcile the internal-launch-cost base case** with `rklb_forward_trajectory.md §7`'s explicit correction (~$25M near-term, not $15–20M). Either move the base case to ~$25M, or have `CONCLUSION.md` acknowledge the correction where it sets $20M as the base. | `CONCLUSION.md`, `calculator/`, `rklb_forward_trajectory.md` | Moderate |
| 7 | **Resolve the `max_racks_per_launch: 2` residual.** The corpus is unanimous that 1 rack/launch holds at every rung (even a GB300 2-rack node is over the reusable budget — `simulations/REPORT.md §4`). Either set `max_racks_per_launch: 1`, or document in the YAML why a derived 2 is permitted, and confirm the engine never returns 2 on the default dials. | `calculator/scenarios/*.yaml`, `calculator/README.md` | Minor |
| 8 | **Fully adopt `review_engineer.md` Finding 2's tag** for the calculator's 5-year service-life dial — label it an unproven *minimum requirement*, not "the BASE CASE," in `default.yaml`. | `calculator/scenarios/default.yaml` | Minor |
| 9 | **Fix the `CONCLUSION.md` "~156 GW (~$250B-inference-services)" phrasing** — 156 GW is AI-specific *capacity*; $250B is the inference *revenue* market; the inference *capacity* slice is ~90 GW. The numbers are sourced; the conflation is not. | `CONCLUSION.md` | Minor |

---

## 8. Closing assessment

The `data_center/` analysis is, at the level of *physics and sourced research*,
in good shape — the wiki numbers are tight, the citations into it hold, and the
superseded-banner discipline is genuinely strong on the documents it was
applied to (`VALUATION_MODEL.md`, `data_science/REPORT.md`,
`wave5_synthesis.md §4.1` are all model reconciled-supersede notes).

The serious problem is singular and structural: **the project ran a full
valuation workstream — the calculator (v1→v3.1), the two M5 reviews, the
trajectory research — entirely *after* `CONCLUSION.md` v8 was written, and
never folded it back into the deliverable.** `CURRENT_STATE.md` knows the
calculator is the current tool and knows its verdict (a capital sink at the
conservative premium); `CONCLUSION.md` does not, and a reader is explicitly
sent to `CONCLUSION.md` first. The deliverable therefore presents a
"modestly positive at a plausible premium" verdict that the project's own
newest, flyability-enforced model contradicts with a −$6.5B DCF — and there is
no banner, pointer, or reconciliation note anywhere in `CONCLUSION.md` to warn
the reader.

This is not a new *kind* of failure for this project: `peer_review_4.md` and
`triage_and_fix_plan.md` already diagnosed the pattern — "upstream framing
documents frozen at an earlier wave while the conclusion moved on." The fix
those reviews prescribed (catch the frozen documents up) was applied to the
*thesis* (now at Rev 6) but the pattern simply recurred one level higher, with
`CONCLUSION.md` itself now the frozen document and the valuation workstream the
work it failed to absorb. Fix items 1–4 close it. Until then, the honest
status of the orbital-DC analysis is: **the research is sound, the calculator
is the current answer, and the document the project calls its deliverable is
one workstream out of date and reads as contradicting it.**

*End of consistency review.*
