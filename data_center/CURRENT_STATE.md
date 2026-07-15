# Current State - Data Center Workstream

This workstream asks whether Rocket Lab could build and operate orbital
AI-inference data-center nodes launched on Neutron. The current public surface
is a promoted space model, a promoted initial ground reference, and a static
reviewed conclusion.

## What Is Current

- The static conclusion is `data_center/conclusion.md`.
- The companion public documents are `data_center/structural_case.md` (the
  pitch) and `data_center/ai1_comparison.md` (the AI-1 brackets).
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

The promoted default 2036 block-upgrade central case is mass-bound, with 66 GPU
packages per node, about 753 kW per node, 90 launches in the year, 268 living
nodes, about $7.42B in annual living-fleet revenue, and a flat 33.3 percent
margin, at about 1.28x the equivalent ground cohort's five-year cost. The
2026-07-14 investor rebase set this posture: an AI-1-class deployed
double-sided run-hot radiator at 0.00165 t/kW (semi-copying the architecture
SpaceX's June 2026 AI-1 reveal validated) and solar and radiator cost dials of
$0.02M/kW each, reasoned from assembly-line manufacturing scale with in-house
vertical integration; the prior heavy co-mounted posture at $0.04M/kW (1.92x)
is the labeled conservative exception. Treat those as traceable model outputs
from `data_center/models/space/default.json`, not a final recommendation. A
refreshed solar and radiator cost analysis is
`research/node_design/solar_radiator_cost_refresh_2026_07.md`.

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
- Do not make parity claims; the current default is about 1.28x ground, and
  only the AI-1-equivalent bracket at the same cost dials reads below parity
  (about 0.91x), as a labeled scenario.
- Keep model JSON under `models/` and conclusions at the workstream level.
- Keep public launch and deployed-node counts as integers. The model may use a
  smooth curve to shape cadence, but raw fractional rates must never appear as
  launched missions.
- Add future scenarios only when they are useful enough to publish; local runs
  should stay out of Git by default.
- If communications or other Rocket Lab workstreams gain runnable scenarios,
  a project-level scenario runner should include them alongside data-center
  scenarios.
- The orbital communications architecture is only partly defined. Inter-node
  links are optical (laser) and in-house, and that is what "laser-linked orbital
  compute" in these docs refers to: nodes talking to each other. The
  ground-to-orbit link (constellation to Earth) is still TBD, either narrowband
  RF or a ground-to-orbit laser via optical ground stations. Treat it as an open
  research item for the communications workstream, to settle once the
  link architecture is chosen. Do not let "laser-linked" be read as the ground
  link.
