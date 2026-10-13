# Conclusions

**Maturity.** Stable discipline; the prose is reviewed by hand whenever a
default changes. Checked against `main` at 1570350, 2026-10-12.

**Role.** Each application's feasibility verdict and the public documents
around it: static prose a person writes against the promoted JSON, never
generated (ADR 001). A conclusion answers its application's thesis (the
research-wiki page) with the model's all-in numbers.

**Serves.** Objective 5 (the public story) and objective 2 (every number
cites the promoted JSON, a claim ID or an investor-set dial).

**Edges.**
- In: the promoted JSON (the promotion page), the source ledger, the
  assumptions ledgers, and the investor's editorial direction.
- Out: the public story; the root `README.md` summarizes both applications
  for humans and must agree with these documents.

**The documents.** Marked * where they quote model numbers; the dial-change
checklists (the assumptions page) review each marked one, along with the
output-anchor sections of both assumptions ledgers.

| File | What it is |
|---|---|
| `data_center/conclusion.md` * | the data-center verdict and headline numbers |
| `data_center/structural_case.md` * | the pitch: the engine, what the numbers refuse to count, the runway |
| `data_center/ai1_comparison.md` * | SpaceX's AI-1 design run through the same model |
| `communications/conclusion.md` * | the Iridium verdict and numbers |
| `communications/design.md` * | the family structure, the derivation spine, the promotion flow, naming |
| `README.md` * | the public front page for both applications |
| `data_center/README.md` *, `communications/README.md` | front pages and reading paths |
| `data_center/CURRENT_STATE.md` *, `communications/CURRENT_STATE.md` * | short handoffs |
| `rocket_lab_primer.md` | a one-page catch-up on Rocket Lab and its rockets, linked from the README; it quotes Neutron's published figures (the research page, Open) |

**Rules.**
- **Source Snapshot.** Each conclusion carries a Source Snapshot section
  naming the scenario and promoted JSON it was reviewed against.
- **Stale check.** A conclusion is stale until reviewed when its scenario,
  its promoted JSON, a claim ID or status it cites, or code that changes
  default semantics has changed; update it deliberately, or label it stale
  before publication. Data center:
  `git diff -- data_center/models/space/default.json data_center/models/ground/default.json data_center/conclusion.md`;
  Iridium: the same over `communications/models/iridium/default.json` and
  `communications/conclusion.md`.
- **Source rules.** A model output cites its promoted JSON path and, in
  public prose, its claim ID. A scenario or source assumption cites its
  claim ID and the source ledger or research path. A derived
  interpretation (the same-margin token premium, say) cites the JSON
  comparison path and its claim ID. Soft strategic rationale (cadence
  learning, infrastructure bootstrapping) stays qualitative unless a model
  value or a sourced claim supports a hard number. Public prose uses human
  labels and claim IDs; raw JSON paths belong in technical tables, query
  examples, code documentation and diagnostics.

**Public-document rules.** These add to the charter's Public documents
line (pending the investor's OK, as the charter's lines are):
- Structure: the answer, the plan by date, the engine, the unpriced upside
  named, the runway, then the one hedge.
- Never count again what a dial already prices: launch-cost gains are in
  the launch price, and scale is in the solar and radiator cost dials.
- Before bolder language ships, a fresh agent checks it adversarially.

**Guardrails for public claims.** Presentation follows the charter's
Quality bar; these add the claim boundaries:
- The data-center product is orbital AI inference, not frontier training.
- The default translates ground hardware into orbit; it is not an
  engineered space-optimized design. Engineering upside (thermal path,
  derating, packaging, cadence learning) is a future design argument, never
  a hidden input to the default.
- The ground comparison is never parity: the default reads above parity,
  and only a labeled AI-1-equivalent bracket reads below.
- The same-margin token premium, the solar and radiator cost sensitivity
  and the superseded thermal package-density sensitivity are separate
  claims.
- Launch cost and cadence are scenario assumptions, not Rocket Lab guidance.
- Lead the data-center headline with cadence and scale (that year's
  launches, new nodes and newly deployed megawatts); the living fleet's
  revenue run-rate goes in a separate sentence.
- Tell the vertical-integration story in its strong form: Rocket Lab is its
  own customer for the bus, solar, radiator and thermal, integration,
  launch, operations and possibly communications; GPUs and some networking
  are the main outside purchases.
- Define any unit (a per-node power, say) against the current promoted JSON;
  never present the old large-capacity language as current. Write "SSO" or
  "sun-synchronous", never "synchronous orbit".
- Communications: keep the three lanes exact; subscribers are people and
  IoT are devices, never summed; frequency and bandwidth stay distinct;
  each people class's column is the whole fleet sold to that class alone,
  so the columns are never summed, and a business view weights them by
  shares of the fleet's beams the investor names, each margin re-derived,
  never averaged (ADR 006); the engineering and product cases stand side by
  side, never added (ADR 012), and IoT and government are never added (ADR
  011).

**Terms.** feasibility study, margin, device class, the three lanes,
investor-set (see `CONTEXT.md`).

**State.** Both applications have a conclusion; the data center's is
reviewed against its promoted JSON and has the structural case and the
AI-1 comparison beside it; the communications one was reviewed against the
model before the saturation work and is stale until its rewrite (Open).

**Open.**
- The README frames the Iridium highlights "under the same all-in
  deployment scenario the data-center model uses", and no public document
  states the charter's rule that the all-in headlines never add (Objective
  1; the 09-23 review's COMMS-AG-23 sentence was never added). The Iridium
  verdict also says the whole modeled Neutron manifest flies communications
  satellites (under its headline table and in How It Deploys), though its
  ledger says the mature fleet frees most of the manifest. A public-document
  edit for the investor.
- The communications documents (`communications/conclusion.md`,
  `communications/assumptions.md`, `communications/CURRENT_STATE.md`,
  `communications/README.md`, `communications/design.md`) and the root
  README's Iridium section still describe the model before the saturation
  work, and wait for a deliberate rewrite to the built one: they publish a
  25 m^2 panel (the investor's panel is 15.4 m^2, the validated Flatellite
  body), the retired four-bucket price sheet with a government bucket, one
  device class a run, a 340 or 2,000 satellite fleet, 2,000 satellites
  called the point where the spectrum saturates (in code 2,000 is only a
  reading, the retired cap, and each class's saturation number is derived:
  the communications page), and a table row linking the retired companion
  scenario. Until the rewrite lands, quote nothing about the Iridium model
  from them.

**Tests.** The em-dash guard covers every `*.md` in `data_center/`,
`communications/` and `docs/`, and the root documents;
`code/tests/data_center/test_cli_promote.py` checks that promotion leaves
`data_center/conclusion.md` untouched. Missed: no test checks the numbers,
links or claim IDs the prose cites.

**If this changes, update here.** A document added or retired; a rule; a
guardrail.

**Drill down.** The documents above;
`docs/adr/001-static-conclusion-dynamic-models.md`;
`research/SOURCE_INDEX.md` for a claim's status.
