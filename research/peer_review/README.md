# Peer Review — Meticulous Validity & Source Audit

A final quality pass. Several independent peer-review agents go meticulously
through the project's documentation to confirm it is **100% correct,
fully sourced, internally consistent, and free of stale "dead notes."**

Peer reviewers **report only — they do not edit.** They flag; a separate fix
pass applies corrections afterward (the same pattern as the lint passes).

## The reviewers

- **Peer reviews 1–3** — each independently audits the **research corpus**
  (the ~28 research docs + the 2 simulation/data-science REPORTs). Each checks:
  - **Validity** — does each claim follow from its stated evidence?
  - **Sources cited** — is every hard number/claim attributed to a source?
  - **Sources confirmed** — spot-check that cited sources actually say what
    the doc claims (flag anything that does not check out).
  - **Internal consistency** — does the doc agree with the others?
  Each writes `peer_review/peer_review_1.md` / `_2.md` / `_3.md` — key findings
  only: "X in doc A doesn't line up with Y in doc B," "source Z does not
  support the claim," etc. No edits.

- **Peer review 4** — audits the **end documents** (`CONCLUSION.md`, the thesis,
  the syntheses) with a consistency-and-hygiene lens:
  - **Inconsistencies** across the end docs and against the research.
  - **"Dead notes"** — stale figures/claims left lying around after the
    project moved past them (e.g. a 2–3-year window still cited after the
    5-year re-base; a superseded SSO figure; an un-updated payback number).
  - **Traceability** — can every conclusion be followed back to its source?
    Flag any conclusion that "doesn't make sense / can't be followed."
  - **Rule compliance** — do the docs follow the `research-wiki` /
    `feasibility-forge` skill conventions (versioned thesis never overwritten,
    every hard claim sourced, catalog/tracker current)?
  Writes `peer_review/peer_review_4.md`.

## When it runs

As the **final QA pass**, after the research, the debate, the strategy loop,
and the conclusion are all settled. Its findings drive one last fix pass, after
which the project is certified meticulously correct.
