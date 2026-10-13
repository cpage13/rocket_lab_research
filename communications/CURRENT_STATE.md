# Current State: Communications

This application asks what a Neutron-launched fleet could deliver on Iridium's
owned L-band, and what that network would sell. Its public surface is two
models side by side, the engineering case (the Iridium model) and the product
case, with their promoted artifacts and a static reviewed conclusion.

## What Is Current

- The static conclusion is `communications/conclusion.md`.
- The Iridium model's artifact is `communications/models/iridium/default.json`
  (schema `iridium-v7`, stamp 2026-10-13). It reads the saturation curve,
  `communications/models/iridium/saturation_curve.json` (schema
  `saturation-v1`, stamp 2026-10-12).
- The product case's artifact is `communications/models/product_case/default.json`
  (schema `product-case-v1`, stamp 2026-10-13). It reads the Iridium artifact.
- The scenarios are `code/scenarios/iridium.yaml` and
  `code/scenarios/product_case.yaml`.
- The code: `code/src/communications/`, eight modules (config, constants,
  engine, iridium, saturation, saturation_curve, ground, json_output) carrying
  the Iridium model, the saturation curve's computation, the shared engine and
  the cellular family; and `code/src/product_case/`, the product case.
- The test suite is green: 1,305 passed and 1 skipped from the repository root
  (2026-10-13), with mypy strict and ruff clean.
- The evidence library lives in `research/` under the `COMM-*` claim ledger.

## Current Read

Every Neutron launch on the shared ramp flies communications satellites, 16 to
a launch. The fleet passes the 340-satellite coverage floor in FY2031, with
528 satellites flying, and reaches 4,288 in FY2036. The fleet costs $191.4M a
year in FY2031 and $1,554.4M in FY2036. The cost model is investor-flat
(2026-07-09): satellites $1.0M each and launches $13.0M at any cadence.

The engineering case sells every seat of each people class, each class alone.
In FY2036 the small terminal alone serves 24,607,046 people for $2,952.8M a
year, at a 47.4 percent own margin. The mounted terminal alone serves
3,527,090 for $2,116.3M, at 26.5 percent. IoT is a capacity there: in FY2036
the room fits 11,497,881,052 minimal-packet IoT devices or 997,732,709 data
IoT devices, each class alone.

The product case sells four classes at the investor's prices, held flat. In
FY2036, in the typical market, it earns $13,156.2M a year at an 88.2 percent
margin, 79.1 percent of it from IoT. It is usable in 1,744 of 2,000 drawn
markets. The two cases are never added.

Treat these as traceable model outputs from the artifacts, not a final
recommendation.

## What Is Not Current

- Operations cost is explicitly zero, a stated assumption and a line to
  research and add later.
- The phone class is sized in the engineering case, but a phone needs a chip
  for the band: the phone is a later, separate model.
- The terminals' upload speeds and their share of IoT's room are not stated
  until the uplink research is validated.
- The product case reports four years (FY2031, FY2033, FY2035, FY2036), not
  every year.
- The High-Bandwidth Cellular Pure Play model is kept as the second family and
  is on hold, with its own pending items: its ground-versus-space conclusions
  material, its revenue cases, and the 50-million and 100-million subscriber
  projections.

## How To Read This Application

Start with `conclusion.md`. Use the three artifacts under `models/` for actual
values. Use `assumptions.md` for where every dial comes from and `design.md`
for how the models, folders, and derivations fit together.

Use `research/LIBRARY.md` and `research/RESEARCH_TRACKER.md` to understand
where assumptions came from and what research is still open. Research
documents may contain older vocabulary or superseded numbers; the promoted
JSON and the static conclusion are the current communications output.

## Open Work

- Keep `conclusion.md` tied to the promoted JSON through deliberate review,
  not automatic promotion output. Promote the product case again whenever the
  Iridium artifact changes.
- The phone as its own model, once a phone chip speaks the band.
- The terminals' upload, once the uplink research is validated.
- The product case's other years (FY2032 and FY2034), which need usage values.
- Operations cost: research the line and replace the explicit zero.
- Keep the three lanes exact in all prose: cellular phones, broadband dish,
  MSS on Iridium L-band. Subscribers are people; IoT are devices.
- Track the external clocks: the Rocket Lab-Iridium close (mid-2027), the
  Amazon-Globalstar close (2027), the live FCC 1.6 GHz sliver dispute, and
  the Iridium replacement window (about 2035).
