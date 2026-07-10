# Current State - Communications Workstream

This workstream asks what a Neutron-launched communications fleet could
deliver, organized as model families by communication paradigm. The current
public surface is the Iridium model: a promoted default and a static reviewed
conclusion.

## What Is Current

- The static conclusion is `communications/conclusion.md`.
- The promoted Iridium model is `communications/models/iridium/default.json`.
- The default assumptions live in `code/scenarios/iridium.yaml`.
- The active model code lives in `code/src/communications/`: five modules
  (constants, config, engine, ground, json_output) carrying both model
  families.
- The test suite is green post-cleanup: the frozen Iridium suite, the
  High-Bandwidth Cellular Pure Play suites, the cross-import guard, and the
  data-center parity gate (174 tests at build close; 172 comms plus parity
  and 554 whole-tree as of 2026-07-09, the published four-bucket ARPU case
  and the flat-cost simplification both landed that day; mypy strict and
  ruff clean).
- The evidence library lives in `research/` under the `COMM-*` claim ledger.

## Current Read

The Iridium baseline is coverage-bound, not capacity-bound: 340 satellites by
2035 at an 18 percent cadence share serve about 10 million subscribers at
31,200 per satellite on the owned 8 MHz, at 1.0 Mbps peak and 5.0 off peak to
a phone. The cost model is founder-flat (simplification
2026-07-09): satellites 1.0 million dollars each and launches 13.0 million at
any cadence, scenario overrides only (the shared-spine defaults untouched),
giving a 900.0 million dollar build-and-hold and a 145.0 million dollar
steady-state annual cost. The model publishes the four-bucket ARPU case (Sheet
A, founder-set 2026-07-09): about 8,250.8 million
dollars per year at the baseline under full sell-through on capacity, about a
98.2 percent margin against the steady-state fleet cost (operating-style:
measured against the fleet's full build, launch, and replacement cost, with
operations the explicit zero and corporate overhead excluded; the promoted
artifact carries the metric). Treat those as traceable model outputs from
`communications/models/iridium/default.json`, not a final recommendation. A
two-round traceability audit (converged 2026-07-08) verified 91 numbers with
zero numeric discrepancies and four citation ids corrected in code (one of
them re-corrected 2026-07-09: the build-cost anchor is `COMM-080`, the
consolidated unit-cost trajectory row).

## What Is Not Current

- The ARPU revenue case is now PUBLISHED (the four-bucket Sheet A). What is not
  yet current in that case: a time-varying per-year mix (the founder's "IoT
  grows in volume at a smaller percentage over time") and a per-year revenue
  trajectory are documented v2 extensions; v1 publishes the built-fleet point
  at a constant mix under full sell-through on capacity.
- Operations cost is explicitly zero, a stated assumption and a fixed line to
  research and add later.
- The cash cost per subscriber (7.50 dollars per year) is the final-year
  replacement-cost artifact (one lumpy hold-phase year); aligning to the
  annualized basis (14.50 dollars per subscriber per year at 10 million)
  is a tracked open item.
- The old pre-rewrite communications tree (the former CLI, output, comparison,
  and validation layers and their tests) was retired 2026-07-07. The live tree
  is the five-module engine plus its per-family tests.
- The High-Bandwidth Cellular Pure Play model is kept as the second family,
  with its own pending items: its ground-versus-space conclusions material,
  its revenue cases, and the 50-million and 100-million subscriber
  projections.

## How To Read This Workstream

Start with `conclusion.md`. Use `models/iridium/default.json` for actual
values. Use `assumptions.md` for where every dial comes from and
`design.md` for how the families, folders, and derivations fit together.

Use `research/LIBRARY.md` and `research/RESEARCH_TRACKER.md` to understand
where assumptions came from and what research is still open. Research
documents may contain older vocabulary or superseded numbers; the promoted
JSON and the static conclusion are the current communications output.

## Open Work

- Keep `conclusion.md` tied to the promoted default JSON through deliberate
  review, not automatic promotion output.
- The ARPU case v2: a time-varying per-year mix and a per-year revenue
  trajectory (v1 publishes the built-fleet point at a constant mix).
- Operations cost: research the fixed line and replace the explicit zero.
- Keep the three lanes exact in all prose: cellular phones, broadband dish,
  MSS on Iridium L-band. Subscribers are people; IoT are devices.
- Track the external clocks: the Rocket Lab-Iridium close (mid-2027), the
  Amazon-Globalstar close (2027), the live FCC 1.6 GHz sliver dispute, and
  the Iridium replacement window (about 2035).
