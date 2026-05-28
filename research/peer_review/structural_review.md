# Structural Review — Repository Cleanliness & Organization QA

> **Historical layout note (2026-05-25).** This review describes an older
> repository shape, including former conclusion/current-state locations and the
> plural `direct_communications/` spelling. It is retained as peer-review
> history, not as current navigation guidance.

*Reviewer: Structural QA pass. Date: 2026-05-18. Scope: the whole repository
at `/Users/chris/Documents/projects/rklb_space_data_center` — folder layout,
workstream separation, catalog/tracker completeness, the root README, legacy
content, build cruft, and naming. **Report-only — no file was edited, moved,
renamed, or deleted.** All keep / archive / delete calls are left to the owner.*

This pass is a sibling to the wave-10 `peer_review/` content audit, but with a
different lens: that pass asked "are the numbers right?"; this one asks "is the
repository structurally sound — clean, walkable, and conformant to the
research-wiki / feasibility-forge spec?"

---

## 0. Executive summary

**The repository is structurally sound.** The recent multi-workstream
reorganization landed cleanly. The shared-wiki / `data_center/` /
`direct_communications/` split is real and correctly applied — no analysis is
sitting in the wiki, and (with one borderline exception, `comms_business_case.md`,
which is correctly placed by the project's own stated convention) no research is
sitting in an analysis folder. Both index files exist, the root README is
accurate and genuinely useful, and every research doc and model on disk is
catalogued in both `LIBRARY.md` and `RESEARCH_TRACKER.md`. There are **no
orphaned docs** and **no catalog entries pointing at missing files**.

The issues found are all **hygiene, not structure**, and none of them blocks
navigation or misleads on a load-bearing fact. In priority order, the headline
issues are:

1. **Build cruft is committed into the tree.** Three `.venv/` directories
   (~hundreds of MB), two `__pycache__/` directories, and a `.pytest_cache/`
   are sitting in the Python projects. The `data_science/` and `simulations/`
   projects have a `.gitignore` that *would* exclude them; the `calculator/`
   project has **no `.gitignore` at all**. There is no git repo at the root, so
   nothing is enforcing the ignores. This is the single biggest cleanliness
   problem. (Category 6.)
2. **The thesis revision count is stale in two index references.**
   `LIBRARY.md` calls the thesis "Rev 1 … Rev 5"; `RESEARCH_TRACKER.md` row C1
   says "Thesis at Rev 6"; the file itself now contains Revisions 1, 2, 2.1, 3,
   4, 5, 6. `LIBRARY.md` is one revision behind. (Category 3/4.)
3. **The `direct_communications/` workstream is nearly invisible to the
   catalog.** Its `README.md` is a real workstream entry-point but appears in
   neither `LIBRARY.md` nor `RESEARCH_TRACKER.md`. A reader walking the catalog
   would never discover the second workstream's front door. (Category 2.)
4. **`../CURRENT_STATE.md` is itself an orphan.** The root README
   points at it prominently as the "read this first" doc, but it is catalogued
   in neither `LIBRARY.md` nor `RESEARCH_TRACKER.md`. (Category 2/3.)

On the owner's specific question — **is `data_center/debate/` now legacy?** —
the answer is **no, keep it**; it is correctly preserved versioned history with
supersession banners already in place. Details in Category 5.

Nothing here changes a conclusion or a number. The repository can be navigated
end-to-end today. This is a clean-up list, not a correction list.

---

## 1. Workstream separation

**Verdict: clean.** The three-part structure described in the root README is
faithfully implemented on disk.

**The shared research wiki (repo root)** holds exactly what it should — eight
topic folders (`rocket_lab/`, `ai_hardware/`, `llm_compute/`, `node_design/`,
`orbital/`, `laser_comms/`, `economics/`, `competitors/`), all containing
sourced, topic-by-topic research and nothing else. No analysis doc, no model,
no synthesis has leaked into the wiki. The `data_centers/` → `ai_hardware/`
rename described in `CURRENT_STATE.md` is done — there is no `data_centers/`
folder and therefore no name collision with `data_center/`.

**`data_center/`** holds exactly the orbital-DC *analysis*: `CONCLUSION.md`,
`CURRENT_STATE.md`, `valuation/` (incl. the `calculator/`), the Python models
(`data_science/`, `simulations/`), `debate/`, `synthesis/`, `strategy/`,
`peer_review/`, `vision/`. All of this is analysis or model work specific to
the orbital-data-center business line — correctly placed.

**`direct_communications/`** holds only its `README.md` — correct; the
workstream's research deliberately lives in the shared wiki's `laser_comms/`.

**One borderline item, judged correctly placed.** `laser_comms/comms_business_case.md`
is a *business-case analysis* document, not neutral topic research — it reads
as the `direct_communications/` workstream's first analysis deliverable. Under
a strict "analysis lives in the workstream folder" rule it would sit in
`direct_communications/`. **However**, the project has made an explicit,
documented decision that research stays in the shared wiki even when one
workstream drove it, and both the root README and the `direct_communications/`
README state plainly that this doc lives at `laser_comms/comms_business_case.md`.
The placement is therefore *intentional and internally consistent* — not a
misfiling. Flagging only so the owner is aware of the one doc that blurs the
research/analysis line; **no action needed** unless the convention changes.

No misplaced files were found. This category passes.

---

## 2. Walkability & traceability

**Verdict: sound, with three reachability gaps — all additive fixes.**

Every one of the **71 markdown files** on disk (excluding the stray
`.pytest_cache/README.md`, which is a tool artifact, not project content) was
checked for catalog reachability. Findings:

### 2.1 — No orphaned research docs, no broken catalog links

Every research doc, synthesis, model report, debate doc, strategy doc, and
peer-review doc is reachable by following README → `LIBRARY.md` /
`RESEARCH_TRACKER.md`. Every catalog and tracker link was cross-checked against
the filesystem — **every linked file exists**. No catalog entry points at a
missing file. The folder-level links (`debate/`, `peer_review/`,
`calculator/`) resolve to real directories. This is a genuinely well-maintained
catalog.

### 2.2 — `direct_communications/README.md` is uncatalogued (reachability gap)

The second workstream's entry-point document is catalogued **nowhere**.
`LIBRARY.md`, `RESEARCH_TRACKER.md`, and the root README mention the *string*
`direct_communications` only in passing prose; none links to
`direct_communications/README.md` as a navigable document. A reader walking the
catalog to "find everything" would miss the entire second workstream's front
door. The root README does link it (in the "How to navigate" section), so it is
not *fully* unreachable — but the two index files, which are supposed to be the
complete map, omit it.
**Recommendation:** add `direct_communications/README.md` to `LIBRARY.md`'s
"Framing & navigation" table and to `RESEARCH_TRACKER.md`.

### 2.3 — `../CURRENT_STATE.md` is uncatalogued (reachability gap)

`CURRENT_STATE.md` is the designated "read this first to re-orient" handoff doc
— the root README leads with it twice. Yet it appears in neither `LIBRARY.md`
nor `RESEARCH_TRACKER.md`. It is reachable via the README, so not a true
orphan, but for a doc the project treats as the primary on-ramp, its absence
from both indexes is an inconsistency.
**Recommendation:** add `CURRENT_STATE.md` to `LIBRARY.md`'s "Framing &
navigation" table (and optionally to the tracker).

### 2.4 — The `peer_review/` sub-documents are catalogued only as a folder

`LIBRARY.md` and `RESEARCH_TRACKER.md` (row P1) both catalogue `peer_review/`
as a single folder-level link. The folder contains six files —
`peer_review_1.md` through `_4.md`, `triage_and_fix_plan.md`, and `README.md`.
Cataloguing the folder as a unit is a defensible choice (the `debate/` and
`calculator/` folders are handled the same way, so it is at least *consistent*),
and the folder has its own `README.md` explaining its contents — so it is
walkable once you enter it. This is **not a defect**, just noted: the deepest
peer-review docs are one hop below the catalog's resolution. The same is true of
`debate/` (its own README) and `synthesis/` (no folder README, but every file
is individually catalogued). Consistency-wise the **`synthesis/` folder is the
odd one out** — its files are individually catalogued while `debate/`,
`peer_review/`, and `calculator/` are catalogued at folder level. Minor; no
action required.

### 2.5 — This document

`structural_review.md` (this file) is new and will itself be uncatalogued on
creation. If the owner wants the `peer_review/` folder to remain a complete
unit, no action is needed (it is covered by the folder-level entry). Noted for
completeness.

---

## 3. Catalog completeness

**Verdict: complete and accurate, with two staleness nicks.**

The actual research docs and models on disk were enumerated and cross-checked
against both index files.

### 3.1 — Research docs: fully catalogued in both indexes

All 28 wiki research docs (tracker items 1–32, 38–39) appear in both
`LIBRARY.md` and `RESEARCH_TRACKER.md`. Spot-checks of `rack_splitting.md` and
`comms_business_case.md` (the two newest, dated 2026-05-18) confirm they are in
both. No research doc is missing from either index.

### 3.2 — Models: all six catalogued, but the M5 location is described
imprecisely

Models M1–M6 all appear in `RESEARCH_TRACKER.md`'s "Models & simulations"
table and in `LIBRARY.md`. One imprecision worth a note:

- **M5's location.** The tracker's M5 row gives the location as
  `data_center/data_science/` with the doc link
  `valuation/VALUATION_MODEL.md`. The *code* for M5 is indeed in
  `data_science/src/rklb_analysis/` (`valuation.py`, `valuation_main.py`,
  `valuation_plots.py`), but the *write-up* `VALUATION_MODEL.md` lives in
  `valuation/`. So M5 is physically split — code in one folder, doc in another
  — which the catalog half-acknowledges and half-obscures. This is a legacy of
  the reorganization (the doc was moved into `valuation/` with its siblings;
  the code stayed with the other `data_science/` models). It is not *wrong*,
  but a reader following the M5 row could be confused about where M5 "is."
  **Recommendation:** in the M5 tracker/library entries, state explicitly that
  the model code lives in `data_science/` and the write-up in
  `valuation/VALUATION_MODEL.md`. (Or, longer-term, the owner may want to
  consolidate — see Category 5.)

### 3.3 — Thesis revision count is stale (the headline catalog nick)

The thesis file `../vision/initial_thesis.md` contains Revisions 1, 2,
2.1, 3, 4, 5, and 6. But:

- `LIBRARY.md` describes it twice (lines 11 and 27) as "versioned: Rev 1 …
  Rev 5" / "Rev 1 … Rev 5" — **one revision stale.**
- `RESEARCH_TRACKER.md` row C1 says "Thesis at Rev 6" — **correct.**

So the two indexes disagree with each other, and `LIBRARY.md` is behind the
file. (Note also that the `peer_review/` material, dated 2026-05-17, repeatedly
refers to the thesis as "Rev 5" and `CONCLUSION.md` as "Rev 7" — those
references were correct *at the time of that pass* and are frozen historical
documents, so they should be left alone; only the live `LIBRARY.md` needs to
catch up.)
**Recommendation:** update `LIBRARY.md` to "Rev 1 … Rev 6".

### 3.4 — `CONCLUSION.md` version vs. thesis revision — consistent

`CONCLUSION.md` is at v8; the thesis is at Rev 6; `RESEARCH_TRACKER.md` row C1
and `LIBRARY.md` both reflect v8 for the conclusion. The conclusion-version /
thesis-revision numbers legitimately differ (the project chose to let them
diverge, documented in the thesis's "Revision 5" and "Revision 6" headers).
Consistent — no action.

---

## 4. The root `README.md`

**Verdict: accurate, clear, and a genuinely useful front door.**

The root `README.md` (~5.8 KB) is well-written and correctly describes the
implemented structure. Checks performed:

- The three-part split it describes (shared wiki + two workstream folders) **matches
  the filesystem exactly.**
- All eight wiki topic folders it lists in the table **exist** with the
  contents described.
- Every relative link in the README was resolved: `LIBRARY.md`,
  `RESEARCH_TRACKER.md`, `../CONCLUSION.md`,
  `../CURRENT_STATE.md`, `../vision/initial_thesis.md`
  (referenced indirectly), `direct_communications/README.md`,
  `laser_comms/comms_business_case.md` — **all resolve to real files.**
- The method description (Feasibility Forge on a research-wiki substrate)
  matches the two skill specs at `~/.claude/skills/`.

One minor inaccuracy:

- **README §"How the repo is organized" → `direct_communications/` bullet** says
  "The first analysis doc … lives in the shared wiki at
  `laser_comms/comms_business_case.md`." Accurate. But the README does not
  mention that `direct_communications/README.md` is itself the workstream's
  primary doc until the later "How to navigate" section. Minor; the navigation
  section covers it. No fix strictly required.

The README is in good shape and needs no structural change — only the
downstream `LIBRARY.md` thesis-revision fix (3.3) would keep the whole
front-door layer self-consistent.

---

## 5. Legacy / stale content — keep / archive / delete recommendations

Each item below is **flagged for the owner to decide**. Nothing was moved or
deleted.

### 5.1 — `data_center/debate/` — **RECOMMENDATION: KEEP**

The owner specifically asked whether this folder is now legacy. **It is not —
keep it as-is.** Reasoning:

- The `research-wiki` / `feasibility-forge` method explicitly values history as
  the audit trail of *why* beliefs changed. The debate is part of that trail.
- The folder is **not silently stale**. Both `bull_case.md` and `bear_case.md`
  carry a prominent, dated "Superseded economics (wave-9)" banner at the top
  that tells the reader exactly which numbers are outdated and where the current
  ones live (`CONCLUSION.md` Rev 4–7). `RESEARCH_TRACKER.md` row D1 and
  `LIBRARY.md` both repeat the supersession note. This is the *correct* way to
  retire content — banner it, don't delete it.
- `CONCLUSION.md` still cites the debate for its qualitative convergence ("fund
  the bounded build-to-learn programme"), so the folder is still load-bearing
  for traceability, not dead weight.
- It is small (3 files, ~tens of KB).

The debate is doing exactly what versioned history should do. No archive, no
delete. If anything, it is a model for how the *other* superseded content
(below) is handled.

### 5.2 — `../../code/docs/VALUATION_MODEL.md` (the M5 model) — **RECOMMENDATION: KEEP**

- Superseded by the calculator (M6), and **clearly marked**: a large
  "⚠️ SUPERSEDED — do not cite the headline numbers" banner heads the file,
  enumerating every reason it was retired and pointing to the calculator.
  `LIBRARY.md` and `RESEARCH_TRACKER.md` both carry the same banner.
- This is correct versioned-history handling, identical in spirit to the
  debate. The economist/engineer reviews (`review_economist.md`,
  `review_engineer.md`) are *reviews of M5* — they only make sense if M5 itself
  is still present. Deleting M5 would orphan two reviewed documents.
- **One loose end** (not a delete argument, a tidiness note): M5's *code* still
  lives in `data_center/data_science/src/rklb_analysis/` (`valuation.py` et al.)
  and M5 still emits CSVs/PNGs into `data_science/output/`. The doc was moved to
  `valuation/` in the reorg; the code was not. If the owner ever wants the M5
  artifacts fully consolidated, the code + outputs could move under
  `valuation/` alongside the write-up — but this is optional polish, and the
  catalog imprecision in 3.2 is the cheaper fix. **Keep; consider noting the
  code/doc split in the catalog.**

### 5.3 — Older synthesis lint reports (`synthesis/lint_report.md`,
`synthesis/lint_report_2.md`) — **RECOMMENDATION: KEEP**

- These are point-in-time health-check reports (lint pass 1 and pass 2). The
  `research-wiki` method treats lint reports as part of the synthesis trail,
  same as the wave syntheses. They are individually catalogued in both indexes
  (S-rows L1, L2) and their findings are referenced by later docs.
- They are *inherently* historical — a lint report is a snapshot — and that is
  fine. They are not masquerading as current; `RESEARCH_TRACKER.md` row L2
  explicitly notes its residual items were "folded into the wave-10
  peer-review pass … and resolved there."
- Small. No reason to remove. **Keep.** (If the owner wants the `synthesis/`
  folder to read more cleanly, the lint reports could be grouped under a
  `synthesis/lint/` subfolder — purely cosmetic, low value, optional.)

### 5.4 — The older syntheses (`preliminary_findings.md`, `wave4_synthesis.md`,
`wave5_synthesis.md`) — **RECOMMENDATION: KEEP**

Superseded by later waves and by `CONCLUSION.md`, but they are the wave-by-wave
audit trail the method requires, all catalogued, all dated. `wave5_synthesis.md`
in particular is still actively cross-referenced by many docs for the
flyability-ceiling reconciliation. **Keep.** (See 7.2 for a naming nit:
`preliminary_findings.md` is the wave-1 synthesis but is not named
`wave1_synthesis.md`.)

### 5.5 — `data_center/peer_review/` — **RECOMMENDATION: KEEP**

A completed QA pass (wave 10), all six files dated and coherent, catalogued as a
folder. This `structural_review.md` is being added into it. **Keep.**

### 5.6 — Python model `output/` artifacts (`data_science/output/`, the PNGs
in `simulations/`) — **RECOMMENDATION: KEEP (with a caveat)**

`data_science/output/` holds ~31 generated CSVs and PNGs; `simulations/` holds
3 generated PNGs at the project root. These are *generated* artifacts (the
`data_science/.gitignore` does **not** ignore `output/`, so they are
deliberately retained). They are referenced by the model REPORT.md files as the
figures behind the analysis, so they have real documentary value. **Keep** —
but note this is a *choice*: they are reproducible by re-running the models. If
the owner prefers a lean tree, `output/` could be regenerated on demand. The
`.venv/` directories (5.7 / Category 6) are a different matter — those are pure
cruft.

### 5.7 — Build cruft — **RECOMMENDATION: DELETE** (see Category 6 for detail)

`.venv/` ×3, `__pycache__/` ×2, `.pytest_cache/` ×1. These are pure
machine-regenerated artifacts with zero documentary value. Safe to delete;
should be git-ignored. Detailed in Category 6.

---

## 6. Cruft

**Verdict: present and committed into the tree — the worst cleanliness issue
in the repo, though all of it is safely removable.**

There is **no git repository** at the project root (`.git` does not exist), so
nothing is actually enforcing any `.gitignore`. The artifacts below are simply
sitting in the working tree.

### 6.1 — Virtual environments (`.venv/`) — three of them

| Path | Notes |
|---|---|
| `data_center/data_science/.venv/` | Python 3.13 env; site-packages incl. matplotlib, PIL, fontTools, etc. — easily 100s of MB. |
| `data_center/simulations/.venv/` | Python 3.13 env. |
| `data_center/valuation/calculator/.venv/` | Python 3.14 env. |

These are machine-local environments. They should never be in the tree.
`data_science/` and `simulations/` each have a `.gitignore` that lists
`.venv` — so *if* this were a git repo they would be ignored — but
**`calculator/` has no `.gitignore` at all.** **Recommendation: delete all
three `.venv/` directories** (they regenerate via `uv sync` / `uv run`), and
**add a `.gitignore` to `calculator/`** (copy the one from `data_science/`).

### 6.2 — `__pycache__/` — two directories

- `data_center/valuation/calculator/src/rklb_value/__pycache__/` — 5 `.pyc`
  files (`cli`, `config`, `engine`, `report`, `__init__`), Python 3.14.
- `data_center/valuation/calculator/tests/__pycache__/` — 1 `.pyc`
  (`test_engine`).

Both are in the `calculator/` project, which has no `.gitignore`.
`data_science/` and `simulations/` have no committed `__pycache__/` (their
`.gitignore` covers it and/or they were cleaned). **Recommendation: delete both
`__pycache__/` directories**; the `calculator/` `.gitignore` added per 6.1
will keep them out.

### 6.3 — `.pytest_cache/` — one directory

`data_center/valuation/calculator/.pytest_cache/` — pytest's run cache (it even
contains a `.pytest_cache/README.md`, which is *pytest's own* file, not project
content — and which slightly inflates any naive markdown-file count). Pure
cruft. **Recommendation: delete**; covered by the `.gitignore` fix.

### 6.4 — No `*.egg-info`, no editor/OS junk

Checked explicitly: **no** `*.egg-info` directories, **no** `.DS_Store`,
**no** `Thumbs.db`, **no** `*.swp`, **no** editor backup (`*~`) files anywhere
in the tree. That part is clean.

### 6.5 — Summary of the cruft fix

The whole cruft problem is fixed by three cheap actions (owner to perform):
1. Delete the three `.venv/`, two `__pycache__/`, and one `.pytest_cache/`.
2. Add a `.gitignore` to `data_center/valuation/calculator/` (the
   `data_science/` one is a good template — it already covers `__pycache__/`,
   `*.py[oc]`, `*.egg-info`, `.venv`).
3. If this project is meant to be version-controlled, `git init` at the root
   (or confirm it intentionally is not) — without a repo, no `.gitignore` is
   doing anything.

---

## 7. Naming & consistency

**Verdict: good overall; a handful of minor inconsistencies, none confusing in
practice.**

### 7.1 — Folder names — consistent and clear

The wiki topic folders (`rocket_lab/`, `ai_hardware/`, `llm_compute/`,
`node_design/`, `orbital/`, `laser_comms/`, `economics/`, `competitors/`) and
the `data_center/` sub-folders (`valuation/`, `data_science/`, `simulations/`,
`debate/`, `synthesis/`, `strategy/`, `peer_review/`, `vision/`) are all
lower-snake-case, descriptive, and unambiguous. The `data_centers/` →
`ai_hardware/` rename successfully removed the one real name hazard.

### 7.2 — `synthesis/preliminary_findings.md` breaks the wave-N naming pattern

The synthesis folder contains `wave4_synthesis.md` and `wave5_synthesis.md` —
but the **wave-1** synthesis is named `preliminary_findings.md`, not
`wave1_synthesis.md`. The catalog correctly identifies it ("Wave-1 synthesis"),
so it is not *lost* — but the naming is inconsistent with its siblings. Also
note there is no `wave2_synthesis.md` or `wave3_synthesis.md` — `wave4_synthesis.md`
is described as covering "waves 2–4", which is fine but means the file numbering
is not a clean 1-per-wave sequence. **Minor; rename to `wave1_synthesis.md` for
consistency if desired, or leave it — the catalog disambiguates.** (Flag only.)

### 7.3 — File-name casing: `CONCLUSION.md` / `CURRENT_STATE.md` / `LIBRARY.md`
/ `RESEARCH_TRACKER.md` / `README.md` vs. `VALUATION_MODEL.md` / `REPORT.md` /
`INVESTOR_PROJECTION.md`

The project uses ALL-CAPS filenames for "important top-level documents." This is
applied consistently — top-level deliverables and index files are caps;
ordinary research docs are lower-snake-case. The model write-ups
(`REPORT.md`, `INVESTOR_PROJECTION.md`, `VALUATION_MODEL.md`,
`cadence_revenue_model.md`) are *mixed*: three are caps, one
(`cadence_revenue_model.md`) is lower-case, despite all four being model
write-ups of the same kind. **Minor inconsistency** — `cadence_revenue_model.md`
is the odd one out among model docs. No practical impact; flag only.

### 7.4 — `data_center` (folder) vs. "data center" / "data-center" (prose)

The folder is `data_center`; prose across the docs uses "data center" and
"data-center" interchangeably. This is normal English-vs-identifier variance
and is not worth changing. Noted only for completeness.

### 7.5 — Model IDs M1–M6 — consistent

The M1–M6 model labelling is used consistently across `RESEARCH_TRACKER.md`,
`LIBRARY.md`, `CONCLUSION.md`, and `CURRENT_STATE.md`. M1 = simulations,
M2/M3/M4 = data_science models, M5 = valuation model, M6 = calculator. Clean.
(The only wrinkle is the M5 code/doc location split — see 3.2 / 5.2.)

---

## 8. Prioritized action list

All actions are for the **owner** to perform. None was performed by this pass.
Ordered high → low priority.

### Priority 1 — cleanliness (do these)

1. **Delete the build cruft.** Remove the three `.venv/`
   (`data_science/`, `simulations/`, `calculator/`), the two `__pycache__/`
   (both under `calculator/`), and the `.pytest_cache/` (under `calculator/`).
   All regenerate automatically. (Category 6.)
2. **Add a `.gitignore` to `data_center/valuation/calculator/`.** It is the
   only Python project without one. Copy `data_science/.gitignore`. (Category 6.)
3. **Decide the git question.** There is no `.git` at the root, so no
   `.gitignore` is enforced. Either `git init` (then the ignores work) or
   confirm version control is intentionally external. (Category 6.)

### Priority 2 — catalog accuracy (quick edits to the index files)

4. **Fix the thesis revision count in `LIBRARY.md`** — change "Rev 1 … Rev 5"
   to "Rev 1 … Rev 6" (two places). It currently disagrees with both the file
   and `RESEARCH_TRACKER.md`. (Category 3.3.)
5. **Catalog `direct_communications/README.md`** in `LIBRARY.md` and
   `RESEARCH_TRACKER.md` — the second workstream's front door is currently in
   neither index. (Category 2.2.)
6. **Catalog `../CURRENT_STATE.md`** in `LIBRARY.md` (and optionally
   the tracker) — the project's designated "read first" doc is in neither
   index. (Category 2.3.)
7. **Clarify M5's split location** in the M5 entries of `LIBRARY.md` /
   `RESEARCH_TRACKER.md` — state that the model *code* is in `data_science/`
   and the *write-up* is `valuation/VALUATION_MODEL.md`. (Category 3.2.)

### Priority 3 — optional polish (low value; owner's discretion)

8. Rename `synthesis/preliminary_findings.md` → `wave1_synthesis.md` for
   naming consistency with its siblings. (Category 7.2.)
9. Rename `data_science/cadence_revenue_model.md` →
   `CADENCE_REVENUE_MODEL.md` to match the other ALL-CAPS model write-ups, or
   accept the lower-case form. (Category 7.3.)
10. Consider consolidating M5's code + `output/` artifacts under `valuation/`
    alongside `VALUATION_MODEL.md`, so the model is not physically split across
    two folders. (Category 5.2.)

### Keep / archive / delete — explicit calls for the owner

| Item | Recommendation | Why |
|---|---|---|
| `data_center/debate/` | **KEEP** | Versioned history; correctly banner-superseded; still cited by `CONCLUSION.md`. Not legacy. |
| `../../code/docs/VALUATION_MODEL.md` (M5) | **KEEP** | Superseded but clearly banner-marked; the two economist/engineer reviews depend on it existing. |
| `synthesis/lint_report.md`, `lint_report_2.md` | **KEEP** | Point-in-time health checks; part of the required synthesis trail; catalogued. |
| `synthesis/preliminary_findings.md`, `wave4_synthesis.md`, `wave5_synthesis.md` | **KEEP** | Wave-by-wave audit trail; `wave5` still actively cross-referenced. |
| `data_center/peer_review/` | **KEEP** | Completed QA pass; coherent and dated. |
| `data_science/output/` + `simulations/` PNGs | **KEEP** (caveat) | Generated figures with documentary value; regenerable if a leaner tree is wanted. |
| `.venv/` ×3, `__pycache__/` ×2, `.pytest_cache/` | **DELETE** | Pure machine-regenerated cruft; zero documentary value. |

---

## 9. Bottom line

The reorganization succeeded. The workstream separation is real and clean, the
catalog is complete and link-accurate, the root README is a faithful and useful
front door, and superseded content (the debate, the M5 model, the lint reports)
is handled the right way — bannered and retained, not silently rotting. The
project conforms well to the research-wiki / feasibility-forge spec.

The work remaining is genuine hygiene: **strip the committed build cruft and
give the `calculator/` a `.gitignore`** (Priority 1), and **make three small
catalog additions plus one revision-count fix** so the two index files are
fully self-consistent and the `direct_communications/` workstream is reachable
from the catalog (Priority 2). None of it changes a conclusion or a number.
Confidence: high — the repository is structurally sound.
