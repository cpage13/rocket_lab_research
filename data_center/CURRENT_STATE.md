# Current State - Data Center Workstream

This workstream asks whether Rocket Lab could build and operate orbital
AI-inference data-center nodes launched on Neutron. The current public surface
is a promoted space model, a promoted initial ground reference, and a static
reviewed conclusion.

## What Is Current

- The static conclusion is `data_center/conclusion.md`.
- The promoted space model is `data_center/models/space/default.json`.
- The promoted ground reference is `data_center/models/ground/default.json`.
- The default assumptions live in `code/scenarios/default.yaml`.
- The active model code lives in `code/src/data_center/`.
- The evidence library lives in `research/`.

## Current Read

The workstream has not found a hard physics wall for a small orbital inference
node at the modeled scale. The current issue is whether the economics close
under realistic launch cadence, customer pricing, service life, and hardware
mass assumptions.

The promoted default 2036 block-upgrade central case is mass-bound, with 37 GPU
packages per node, about 422 kW per node, 90 launches in the year, 268 living
nodes, about $5.94B in annual living-fleet revenue, and about 29 percent gross
margin. Treat those as traceable model outputs from
`data_center/models/space/default.json`, not a final recommendation.

The ground reference is an order-of-magnitude check for the same 2036
deployed-year cohort. Its conclusion label is `same_order_of_magnitude` after
the ground inputs were linked to per-input research-wiki source statuses.

## How To Read This Workstream

Start with `conclusion.md`. Use `models/space/default.json` and
`models/ground/default.json` for actual values. The JSON is self-documenting:
model cells carry values, units, formulas, upstream inputs, and source notes;
the space artifact also carries ready `jq` examples in `meta.query_examples`.

Use `research/LIBRARY.md` and `research/RESEARCH_TRACKER.md` to understand
where assumptions came from and what research is still open. Research documents
may contain older vocabulary or superseded numbers; the promoted JSON and
static conclusion are the current data-center output.

## Open Work

- Keep `conclusion.md` tied to the promoted default JSON through deliberate
  review, not automatic promotion output.
- Do not make parity claims; the current default remains about 1.92x ground.
- Keep model JSON under `models/` and conclusions at the workstream level.
- Keep public launch and deployed-node counts as integers. The model may use a
  smooth curve to shape cadence, but raw fractional rates must never appear as
  launched missions.
- Add future scenarios only when they are useful enough to publish; local runs
  should stay out of Git by default.
- If communications or other Rocket Lab workstreams gain runnable scenarios,
  a project-level scenario runner should include them alongside data-center
  scenarios.
