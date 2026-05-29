# Agent Guide

This guide is for future coding or analysis agents working in Rocket Lab
Research. The repository-level umbrella is broader than the current
data-center workstream; the first public investigation is the
Neutron-centered orbital AI-inference data-center case. It keeps procedural
detail out of the human-facing READMEs.

If you entered through root `AGENTS.md`, this is the canonical guide. Keep
`AGENTS.md` short and route detailed agent instructions here.

## Read First

Start with this path before editing or interpreting claims:

- `CONTEXT.md` for vocabulary.
- `README.md` for repository orientation.
- `data_center/README.md` for the workstream map.
- `data_center/conclusion.md` for the current reviewed conclusion.
- `data_center/assumptions.md` and `research/SOURCE_INDEX.md` for source
  status and claim IDs.
- `research/README.md` for the research wiki front door.
- `code/README.md` for run, promote, test, and query commands.
- `docs/architecture-intent.md` for system invariants.
- Relevant ADRs under `docs/adr/` before changing public artifact policy.

The root repository is Rocket Lab Research. The current public artifact set is
data-center first. Communications is reserved for a future researched workstream
until it has its own research, model, source ledger, tests, and public artifact
boundary.

## Research Wiki Map

The `research/` directory is the evidence and source-status layer. It does not
contain the canonical generated model output or the reviewed static conclusion.
Those live under `data_center/`.

Use these files as the wiki map:

- `research/README.md` is the research front door.
- `research/LIBRARY.md` is the topic-discovery catalog.
- `research/RESEARCH_TRACKER.md` records coverage, source-audit status, stale
  material, and open questions.
- `research/SOURCE_INDEX.md` is the claim-level hard-number ledger for `RLDC-*`
  IDs and source status.
- Topic folders hold synthesis, evidence notes, peer review, and historical
  reasoning. Treat them as support for the source ledger, not as promoted model
  outputs.

Use `research/SOURCE_INDEX.md` when deciding whether a number is safe to quote.
Public docs should not cite `placeholder` or `stale` items as settled evidence.

## Research Wiki Skill

If you modify research or run a research agent, use the Research Wiki skill.
This is not optional process decoration; it is how the repository keeps source
work from becoming stranded sidecar notes.

The operating rules are:

- Canonical research findings go under `research/`, not only under `.agent/`.
- `research/LIBRARY.md` must describe new or materially changed research files.
- `research/RESEARCH_TRACKER.md` must record status, audit notes, stale
  material, and open questions.
- `research/SOURCE_INDEX.md` must carry release-critical hard-number claims,
  source status, and `RLDC-*` claim IDs when public docs or model inputs depend
  on those numbers.
- `.agent/` may hold lifecycle notes, diagnostics, reviews, and temporary
  working memory, but it cannot be the only home for research that supports a
  public claim.
- Do not put generated model outputs, current static conclusions, code reports,
  or agent-process essays into `research/`. Research stays research.

When a historical research document is promoted into a current public claim,
trace it through `SOURCE_INDEX.md` and cite the original external sources
where possible. Do not quote an old synthesis, debate, or peer-review note as a
settled current claim just because it is in the research folder.

## Parse Promoted JSON

The promoted space model is `data_center/models/space/default.json`. The
promoted ground reference is `data_center/models/ground/default.json`.

Prefer the embedded query examples before inventing a query:

```sh
jq -r '.meta.query_examples[] | .name + " :: " + .jq' data_center/models/space/default.json
```

For direct inspection:

```sh
jq '.metadata' data_center/models/space/default.json
jq '.inputs.assumption_index | keys | length' data_center/models/space/default.json
jq '.business.years."2036".kw_deployed_this_year.value' data_center/models/space/default.json
jq '.comparison.conclusion_label' data_center/models/ground/default.json
```

Remember that year keys are strings in JSON maps. Use `"2036"`, not `2036`,
when querying `physical.years` or `business.years`.

The space JSON is the canonical agent interrogation surface. Every public
numeric leaf under `physical.years` and `business.years` is a provenance cell
with `value`, `unit`, `formula`, `uses`, `sources`, `source_status`, and
`description`.

The ground JSON is source-linked through per-input `RLDC-GROUND-*` claims. Its
`comparison.conclusion_label` is `same_order_of_magnitude`; do not describe the
ground comparison as parity or proof.

## Trace Inputs To Sources

Use the space artifact's `inputs.assumption_index` for model dials:

```sh
jq '.inputs.assumption_index["inputs.config.cadence.launches_at_year_10"]' data_center/models/space/default.json
```

Each assumption cell carries source status, source references, rationale, and
notes. Public-facing prose should prefer human labels and `RLDC-*` claim IDs
for hard numbers. Exact JSON paths belong in technical tables, query examples,
code documentation, and diagnostics where the reader is actively auditing the
model.

Source rules:

- Model outputs cite the promoted JSON path and, when public-facing, the
  matching `RLDC-*` claim ID.
- Scenario or source assumptions cite the `RLDC-*` claim ID and the source
  ledger or research path.
- Derived interpretations, such as the roughly 90 percent same-margin token
  premium, cite the JSON comparison path and the matching `RLDC-*` claim ID.
- Soft strategic rationale, such as cadence learning or infrastructure
  bootstrapping, should stay qualitative unless a model value or sourced claim
  supports a hard number.

## Code Orientation

Start with `code/README.md`. The code package is data-center first and turns
YAML scenarios into typed JSON artifacts and text reports.

The important code path is `code/src/data_center/`:

- `config.py` owns typed scenario parsing.
- `engine.py` runs the core model.
- `input_manifest.py` builds the source-traceable assumption index.
- `provenance.py`, `output.py`, and `json_output.py` define public output
  structure, provenance cells, validation metadata, and rendering.
- `ground.py` owns the deployed-year ground reference.
- `query_examples.py` embeds `jq` examples in promoted JSON.
- `cli.py` owns command-line execution and promotion.

Do not infer public defaults from code-level convenience defaults. The public
default scenario is `code/scenarios/default.yaml`, and the promoted public JSON
lives under `data_center/models/`.

## Regenerate Models

Run from `code/`:

```sh
uv run rklb-value scenarios/default.yaml --json 2>&1 | tee outputs/data_center/runs/default.json
uv run rklb-value --promote 2>&1 | tee /tmp/rklb_promote.txt
```

Promotion updates the promoted JSON artifacts only. It does not update
`data_center/conclusion.md`.

## Detect A Stale Static Conclusion

Treat `data_center/conclusion.md` as stale until reviewed if any of these
change:

- `code/scenarios/default.yaml`
- `code/scenarios/ground_default.yaml`
- `data_center/models/space/default.json`
- `data_center/models/ground/default.json`
- source IDs or source statuses in `research/SOURCE_INDEX.md`
- code paths that alter default model semantics

A quick check:

```sh
git diff -- data_center/models/space/default.json data_center/models/ground/default.json data_center/conclusion.md
```

If model values changed but the conclusion did not, update the conclusion
deliberately or label it stale before publication.

Use this same stale-conclusion check when source IDs or source statuses change.
The conclusion is reviewed prose, not generated output.

## Public Claim Guardrails

Keep these boundaries visible in public docs:

- The current product is orbital AI inference, not frontier-model training.
- Neutron is the current data-center focus because it is the relevant Rocket
  Lab vehicle for this scale today. Do not add Electron as a modeled
  data-center launch path.
- The default is a conservative translation of public terrestrial hardware
  assumptions into orbit. It is not a final engineered space-optimized design.
- Engineering-phase upside, such as thermal-path improvement, derating,
  packaging changes, or cadence learning, is a future design-space argument,
  not a hidden input to the promoted default.
- The roughly 90 percent same-margin token premium, the solar/radiator
  cost-down sensitivity toward roughly 50 percent, and the thermal
  package-density sensitivity are separate claims.
- Launch cost and cadence values are scenario assumptions, not Rocket Lab
  guidance.
- Do not describe "4 kW units" in public copy unless the unit is defined
  against the current promoted model. The public 2036 node is about 421.98 kW.
- Do not write "synchronous orbit" when the model means SSO or sun-synchronous
  orbit. Use the orbit language supported by the current model and research.

## Do Not Change Casually

- Do not turn root `AGENTS.md` into a second long guide.
- Do not restore the old flat public model alias.
- Do not make promotion rewrite `data_center/conclusion.md`.
- Do not describe the ground comparison as settled parity. The current default
  is about 1.92x ground, with cost-down sensitivities that can lower the ratio.
- Do not blur the default 90 percent token premium, the solar/radiator cost-down
  sensitivity toward 50 percent, and the separate thermal package-density
  sensitivity.
- Do not turn communications into a real model without its own research,
  source ledger, and tests.
- Do not add Electron as a data-center path.
- Do not present training as the modeled product.
- Do not collapse deployed-year capacity into living-fleet capacity.
- When writing the public 2036 headline, lead with cadence and scale: 90
  launches, 90 new nodes, and about 38 MW newly deployed that year. Then, in a
  separate sentence or section, describe the active on-orbit revenue run-rate:
  about $6.31B revenue and $2.10B gross profit. Do not weave back and forth
  between launch cadence and active-base revenue.
- When writing the vertical-integration story, say the strong version: the
  default uses many external buy-price/customer-facing cost lines, while a
  Rocket Lab-operated program would make Rocket Lab its own customer for bus,
  solar, radiator/thermal, integration, launch, operations, and possibly
  communications. GPUs and some networking hardware are the main outside
  purchases. Do not reduce this to generic "integration advantages."
- Public-facing prose should use human labels and `RLDC-*` claim IDs. Raw JSON
  paths belong in code documentation, query examples, and agent diagnostics.
- Do not use old large-capacity language as the current default.
- Do not use em-dashes anywhere in the public documentation; use commas,
  colons, or parentheses instead.
