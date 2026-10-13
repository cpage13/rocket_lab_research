# Conclusions

**Maturity.** Stable discipline; the prose is reviewed by hand whenever a
default changes. Checked against `part-p7-documents` at baa4c04 with p7's
documents, 2026-10-13.

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
| `communications/conclusion.md` * | the communications verdict: the engineering case and the product case side by side, never added |
| `communications/design.md` * | the family structure, the saturation curve and the run, the product case, the promotion flow, naming |
| `README.md` * | the public front page for both applications |
| `data_center/README.md` *, `communications/README.md` | front pages and reading paths |
| `data_center/CURRENT_STATE.md` *, `communications/CURRENT_STATE.md` * | short handoffs |
| `rocket_lab_primer.md` | a one-page catch-up on Rocket Lab and its rockets, linked from the README; it quotes Neutron's published figures (the research page, Open) and names the communications application |

**Rules.**
- **Source Snapshot.** Each conclusion carries a Source Snapshot section
  naming the scenario and promoted JSON it was reviewed against.
- **Stale check.** A conclusion is stale until reviewed when its scenario,
  its promoted JSON, a claim ID or status it cites, or code that changes
  default semantics has changed; update it deliberately, or label it stale
  before publication. Data center:
  `git diff -- data_center/models/space/default.json data_center/models/ground/default.json data_center/conclusion.md`;
  communications: the same over `communications/models/iridium/default.json`,
  the product case's promoted artifact beside it, and
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
AI-1 comparison beside it; the communications one was rewritten against the
Iridium artifact (`iridium-v7`) and the product case's (`product-case-v1`),
the two cases side by side (2026-10-13), and names all three promoted files
in its Source Snapshot.

**Open.**
- The communications documents cite the product case's artifact, which is
  promoted after them: until that promotion lands, their links to it do not
  resolve, and its stamp in the Source Snapshot, the ledger's anchors and
  the handoff is the build run's (2026-10-13).

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
