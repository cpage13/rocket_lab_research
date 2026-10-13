# Rocket Lab Research

The charter: purpose, rules and pieces. Read it first, then `atlas/map.md`.
**Precedence.** Memory and old session states are hints, and lose to the
repository and the resume point: for what is built, the code and the promoted
JSON are the truth (a page that disagrees is fixed); for what is decided but
not built, the resume point named in `.agent/INDEX.md` (local).

## What

An independent, source-linked research and modeling repository, built for an
investor analyzing Rocket Lab (RKLB) and published for anyone who wants to
check the reasoning: what new orbital business could Rocket Lab build with
the rockets and spacecraft it already makes? Two applications are modeled,
both on Neutron: an orbital AI-inference data center, and, because Rocket Lab
has agreed to acquire Iridium (`COMM-601`, `COMM-606`), communications: the
most Iridium's owned L-band can carry on a next-generation fleet and, beside
it, the product case: what that network would sell at the investor's prices.
Each is a feasibility study: the investor's hypothesis is an append-only
thesis in `research/vision/`, research waves hunt the hard barriers first,
the model answers the all-in question, and the conclusion gives the verdict.

## Why

Rocket Lab's upside rests on businesses no one prices in public: what a
Neutron fleet could earn and cost in each application at the full launch
cadence (for the data center, also against the ground alternative). The
models are small enough to read and built on sourced research and stated
assumptions, so a reader can dispute an assumption without distrusting the
arithmetic: "You can disagree with the assumptions, but if you make
everything a knob, it's just absolutely overwhelming."

## Objectives

1. Answer the all-in question for every application: what a Neutron fleet
   delivers, earns and costs at the full modeled cadence, judged by revenue
   and margin in years 5 to 10 (from each config's `metadata.base_year`).
   The applications share one launch ramp; each case runs as if it had the
   ramp to itself, so their headlines never add; a combined case is its own run.
2. Trace every published number to the promoted JSON, a claim ID or an investor-set dial.
3. Keep each model simple: it optimizes one thing and states assumptions, not knobs.
4. Keep the evidence base a research wiki any agent can extend.
5. Publish each application's case as a story a reader can follow and audit.

## Goals

- **Communications, saturation.** Built: the Iridium model derives in code how
  many satellites the owned spectrum can serve for each of its people classes
  (the small terminal, the mounted terminal and the phone class: the class's
  saturation number where its rows reach one, a knee on the promoted
  saturation curve), in place of the inherited cap, and sells every seat of
  the three side by side on the fleet the all-in launch cadence builds (ADRs
  005 to 010). Open until the public documents tell the built model and the
  work is accepted.
- **Communications, IoT and the product case.** IoT as capacity in the
  engineering model, which carries no IoT count, price or revenue (ADR 011),
  and the product case as its own model on the engineering artifact, selling
  the terminals and the two IoT classes at the investor's prices held flat
  (ADR 012); approved 2026-10-07, not yet built.
- **Agent documentation.** The charter, atlas and glossary are true to the
  code; the older agent guides are folded in and retired.
- **Data center.** Rename the space artifact's `gross_profit_*` fields, which
  hold a full-cost profit (approved; it starts on the investor's go).

## Quality bar

- **Ballpark, minimal knobs.** Models are "never to be on the dollar and penny
  ... just kind of really ballpark"; close means the right order of magnitude.
  Unmodeled factors (GPU failures, the launch site, facility accounting, future
  ground stations, a new pad) go in the assumptions ledgers as stated
  assumptions, never as new dials, since their costs amortize over the fleet:
  "That's why we have the assumptions document." An assumed upgrade sets an
  existing value and is stated with it: the Neutron block upgrade is the data
  center's 12.5 t envelope (`RLDC-PAYLOAD-SSO-UPGRADE`) and the approved Iridium
  count of 16 per launch.
- **One model, one maximum.** Each engineering model optimizes one thing (the
  data center, the most GPU packages each launch carries; communications, the
  most the owned spectrum carries) at the full cadence (the ramp, never a flat
  rate: "pedal to the metal") with every seat sold, so revenue rises with the
  fleet. A haircut of an engineering case is a linear division in the
  conclusion ("You just take the final numbers and divide them in two"). The
  market view is the product case, a separate model on the engineering artifact
  that optimizes one thing too (the most median revenue at the investor's
  prices in at least three quarters of the markets, or, when none is, the most
  usable, warned), read beside the engineering case and never added to it
  (ADR 012).
- **Only what exists.** Neutron is the only vehicle modeled (no Starship, heavy vehicle or Electron).
- **The investor's values.** Never invent an assumption: name the grounded
  range and ask the investor to set it. Only the investor moves a settled
  value; its linear alternative gets one line at the end of the conclusion
  and the ledger, or one scenario value, never caveats spread through.
- **Facts apart from estimates.** Every number carries its basis (the
  taxonomy in `research/SOURCE_INDEX.md`), from the model or the research,
  never memory. A cap or ceiling is a window-scoped assumption, never a
  system property or a "full stop"; an untraceable number is not published.
- **Presentation.** Lead with operations (revenue, margin, GPUs, nodes and
  launches, per GPU; for communications, satellites and each class's people
  or devices), from the owner-operator's view, in cohorts at representative
  years; never EV, DCF or net-of-capital. The percentage is the margin (a
  full-cost margin); a dollar figure is the profit, never gross profit. Show
  the device classes side by side, never phone-first: in the engineering case
  the small terminal, the mounted terminal and the phone class, with IoT's
  capacity; in the product case the small terminal, the mounted terminal,
  minimal-packet IoT and data IoT.
- **Public documents.** Story first, upside explicit, one hedge at the end;
  the conservative floor stays visible but never leads, and the tone is
  never promotional (more rules and guardrails on the conclusions page).

## Ideal outcome

A reader, human or agent, follows an application's conclusion to its 10-year
revenue and margin and traces any number to the promoted JSON or a sourced
claim. Changing an assumption is a scenario edit with its ledger row (for a
default, its code home too), a promotion and a review of the prose; arguments
are about assumptions, not arithmetic. Each new application gets the same
treatment on the same spine, and no agent needs the repository explained twice.

## Core pieces

- [Research wiki](atlas/pieces/research-wiki.md): `research/`, the evidence, the theses and the source ledger.
- [Assumptions](atlas/pieces/assumptions.md): the scenario files, the two ledgers, the stated assumptions.
- [Data-center model](atlas/pieces/data-center-model.md): `code/src/data_center/`, the space model and ground reference.
- [Communications model](atlas/pieces/communications-model.md): `code/src/communications/`, the Iridium model on its saturation curve.
- [Shared core](atlas/pieces/shared-core.md): `code/src/common/`, the cadence spine, cells, file boundary, commands.
- [Promotion](atlas/pieces/promotion.md): the commands, gate and writer that publish the promoted JSON.
- [Conclusions](atlas/pieces/conclusions.md): each application's verdict and public documents, reviewed by hand.

Core flow: a research claim sets an assumption (a dial, or a stated ledger
row); a model run makes promoted JSON; a person reviews it into the conclusion.

## Project rules

- **Writing.** No em-dashes anywhere (commas, colons or parentheses; the map
  says what the guard covers). The person is the investor, never "founder".
- **No author identity anywhere.** Commits are `anonymous <>` with no
  trailer; documents carry no "Author:" line, the copyright no name. Never
  raise pushing until the investor does.
- **Changes.** Every tracked file (code, tests, scenarios, promoted JSON,
  ledgers, conclusions, public documents, research) needs the investor's go.
- **Keep the full trace.** Never `rm` or `rmdir`, no mid-work cleanup of drafts,
  round reports or run outputs; removal is the investor's end-of-work call (to the Trash).
- **Research** follows `atlas/pieces/research-wiki.md`. **Seats**: judgment
  seats run on Opus; set every seat's model explicitly.
- **Python** 3.14 under `uv`, from `code/`. Test command:
  `uv run ruff check . && uv run ruff format --check . && uv run mypy --strict src && uv run pytest -q`;
  from the root, `uv run --project code pytest code/tests -q`.
- **Heavy runs.** The saturation command
  (`python -m communications.saturation`) runs one at a time, detached, from
  an isolated worktree: about 30 minutes and a 14 GB memory bound on its last
  measured run (the curve's `provenance.run_measurement`).

## Where next

`atlas/map.md`, `CONTEXT.md` (the glossary), `docs/adr/` (never reverse one
without the investor), `README.md`, and `.agent/INDEX.md` (local), which
holds the goals' status and active work's resume point.
