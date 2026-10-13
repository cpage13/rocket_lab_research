# Research wiki

**Maturity.** Stable rules, growing content. Checked against `research/` on
`main` at 1570350, 2026-10-12.

**Role.** The evidence base for every application. It holds each
application's thesis, the investor's hypothesis as an append-only belief
record revised after each research wave (`research/vision/initial_thesis.md`,
data center; `research/vision/comms_thesis.md`, communications); the topic
documents (sources, reasoning, syntheses, debates, peer reviews); and three
ledgers: the catalog `research/LIBRARY.md`, the tracker
`research/RESEARCH_TRACKER.md`, and the source ledger
`research/SOURCE_INDEX.md`. The catalog ends in its own Glossary of
research words; where it and `CONTEXT.md` share a word, `CONTEXT.md` wins
(the catalog's "source index" is the source ledger). It holds no model
output and no current conclusion. The feasibility arc that runs from thesis
to verdict is on the map.

**Serves.** Objective 2 (the claim IDs every published number can point to)
and objective 4 (an evidence base any agent can extend).

**Edges.**
- In: external sources; research runs, one seat per topic; validated local
  research from `.agent/other/` (local), on the investor's go (rule 8).
- Out: claim IDs and source statuses, cited by the assumptions ledgers, by
  each model's `constants.py`, by the data-center input spec tables and by
  the conclusions; the data-center tests read the ledger's statuses.

**Terms.** claim ID (and the source ledger), source status, feasibility
study (see `CONTEXT.md`).

**State.**
- Topic folders: `ai_hardware`, `competitors`, `debate`,
  `direct_communication`, `economics`, `laser_comms`, `llm_compute`,
  `node_design`, `orbital`, `peer_review`, `rocket_lab` (with subfolders
  `electron` and `neutron`), `strategy`, `synthesis`, `valuation`, `vision`.
- Claim families: `RLDC` (data-center release-critical defaults and public
  claims, with the per-input `RLDC-GROUND-*` rows), `NTR` (Neutron), `GPU`,
  `REV` (revenue and markets), `THR` (thermal, solar, reliability), `COMM`
  (communications). The status taxonomy heads the ledger.

**Rules.** Every research change or research-agent run follows these:
0. Search first: before new research or a new document, read the catalog,
   the tracker and the source ledger and reference what exists; only gaps
   get new research.
1. Canonical findings live in `research/`. `.agent/` (local) may hold
   working notes, never the only home of research behind a public claim.
2. A new or materially changed research file gets a `research/LIBRARY.md`
   entry and a `research/RESEARCH_TRACKER.md` row (status, audit note,
   stale material, open questions).
3. A hard number that a public document or a model input depends on gets a
   `research/SOURCE_INDEX.md` row: claim ID, source status, sources.
4. No generated model output, current conclusion, code report or
   agent-process essay goes into `research/`.
5. A historical document promoted into a current claim is traced through
   the source ledger to its original external sources; an old synthesis,
   debate or peer review is never quoted as a settled current fact.
6. Public documents never cite a `placeholder` or `stale` claim as evidence.
7. Research runs follow the forge-research-wiki skill: one seat per topic,
   two or more independent sources per hard number, estimates flagged, a
   synthesis and a thesis revision per wave, a lint pass between waves.
8. A question too new for the wiki runs locally in `.agent/other/` (local):
   a research wiki under forge-research-wiki, or a hypothesis tested toward
   a verdict (a new feasibility study) under forge-research-feasibility.
   Nothing public cites it until a separate seat validates it (re-checks the
   sources, recomputes the numbers), the investor reads it, and it moves
   here on their go.

**Open.**
- The write-ups (everything but `research/README.md` and the ledgers)
  predate the no-em-dash rule, and the write-ups plus `research/LIBRARY.md` and
  `research/RESEARCH_TRACKER.md` still say "founder"; the em-dash guard
  excludes the write-ups until the investor decides on a sweep.
- The Neutron documents lag the payload user's guide as read by the local
  Flatellite experiment (the 13 t reference orbit, the SSO curves, the
  first-flight claim `NTR-011`, a dead guide link in the ledger); its
  research B lists them for a fix at promotion, on the investor's go
  (`.agent/other/flatellite_dimensions_09_29/RESEARCH_TRACKER.md` (local)).
  The root `rocket_lab_primer.md` quotes the same 13 t and first-flight
  figures. The experiment's panel and per-launch counts are now repo rows
  (COMM-711 to COMM-713, `research/rocket_lab/flatellite_panel_and_stack.md`);
  the Neutron items above stay open.
- A low-priority follow-up from the 09-24 review: record the guide's
  Figure 13 volume read-off under `research/rocket_lab/neutron/`
  (`.agent/lifecycle/review_fixes_session_state_09_24.md` (local)).

**Tests.** The em-dash guard covers `research/README.md` and the three
ledgers (`code/tests/test_no_em_dashes.py`). The data-center suite checks
that each `RLDC`-cited input carries the ledger's status
(`code/tests/data_center/test_input_manifest.py`,
`code/tests/data_center/test_provenance_uses.py`), the communications suite
that every `COMM-*` claim ID its code cites is a ledger row
(`code/tests/communications/test_claim_citations.py`), and the documents
guard that every claim ID the agent pages cite is a ledger row
(`code/tests/test_agent_docs_resolve.py`). Missed: links inside `research/`
and the catalog's coverage of every file (lint passes are agent runs).

**If this changes, update here.** A topic folder, claim family, ledger or
rule added or retired; a change in what may live in `research/`.

**Drill down.** `research/README.md` (the front door), the three ledgers,
the two theses, and the forge-research-wiki and forge-research-feasibility
skills.
