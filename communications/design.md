# Communications Workstream Design

This document is the architecture of the communications workstream: how model
families are organized, where everything lives, how the Iridium model is
built, and how a scenario becomes a published number. It describes structure,
not results; the results live in the [conclusion](conclusion.md).

## Model Families By Paradigm

The unit of organization is the model family: one communication paradigm, one
device population, one spectrum position, modeled end to end on the shared
engine. The paradigms are the three lanes, kept strictly separate:

- **Cellular**: phones on cellular spectrum (leased or bought). Modeled as
  the High-Bandwidth Cellular Pure Play model.
- **Broadband**: a dish on Ku/Ka spectrum. Deliberately unmodeled, the easier
  case.
- **MSS**: Iridium's owned L-band to purpose-built or in-chipset devices.
  Modeled as the Iridium model, the current focus.

A family is not a fork of the codebase. All families run on one engine (the
cadence ramp, the cohort treadmill, fleet costing, cost-plus revenue), and a
family contributes only what makes it different: a config block of dials, a
derivation from those dials to subscribers per satellite, a scenario file, and
a frozen test suite. The cellular family sets subscriber density directly as a
dial (75,000 per satellite on its 25 MHz basis) and carries the ground
cost comparison; the Iridium family derives density from spectrum physics.

How a new family gets added, in order:

1. Ground it in the research wiki first: claims with `COMM-*` ids, estimate
   tiers labeled, the lane named.
2. Brainstorm and design with the investor; the investor sets every assumption
   value (the model never invents one).
3. Plan, adversarial review, investor approval, then build: a dials block in
   `config.py`, named constants with derivation docstrings in `constants.py`,
   the derivation functions and one guarded branch in `engine.py`.
4. A scenario YAML named for the family, and a frozen test suite locking the
   baseline numbers.
5. Promote to `communications/models/<family>/default.json` and write the
   conclusion prose deliberately.

## The Folder Map

```
communications/                  the workstream documents (this folder)
  README.md                      operating picture and reading path
  conclusion.md                  the static, reviewed verdict
  assumptions.md                 the default-assumption ledger
  design.md                      this document
  CURRENT_STATE.md               short handoff
  models/<family>/default.json   the promoted model output per family
code/
  src/communications/            the shared engine and per-family blocks
    constants.py                 named constants, one section per family
    config.py                    frozen Pydantic config tree, per-family dials
    engine.py                    cadence, cohorts, cost, revenue, derivations
    ground.py                    the cellular family's ground comparison
  scenarios/<family>.yaml        the input dials per family (iridium.yaml)
  tests/communications/          per-family frozen suites plus shared guards
research/                        the evidence wiki (COMM-* claim ledger)
```

The data-center model is the sibling workstream under `data_center/` and
`code/src/data_center/`; a parity test suite keeps the shared conventions
identical, and a cross-import guard keeps the packages separate.

## The Iridium Model's Structure

**The dials.** Nine physics dials, all defaulted from named constants:
spectrum (8.0 MHz exclusive; 10.5 coordinated variant), aperture (25.0 square
meters), device class (phone, small terminal, or terminal), an optional
spectral-efficiency override, active user rate (1.0 Mbps; 2.5 rich variant),
the concurrency pair (2.5 percent peak, 0.5 percent off peak), the IoT device
passthrough (10 million, superseded on the artifact when the ARPU case is
on), and the scenario label. Plus the optional ARPU block (investor-set
2026-07-09, Sheet A): four mix percentages validated to sum to 100 and four
prices per month; None keeps the revenue case off. The fleet dials (12
satellites per launch, 5-year life, the 340 coverage floor, the 2,000
saturation cap, the 0.18 cadence share) are carried from the shared engine;
the default scenario overrides three of them (the cadence share all-in at 1.0,
pedal to the metal, investor-set 2026-07-14; satellite build cost 1.0 million
dollars investor-flat; and a flat 13.0 million dollar launch cost at every
cadence, set by equal curve anchors), leaving the shared config defaults
untouched.

**The derivation spine, in one paragraph.** Resolve the device class to a
spectral efficiency (phone 0.65, small terminal 2.0, terminal 2.5 bits per
hertz, or the override). Per-satellite capacity is spectrum times spectral
efficiency times the 0.15 calibration (Gbps per MHz per unit efficiency,
calibrated to the corpus supply anchor) times the aperture factor
(area over 25): at the baseline, 8.0 x 0.65 x 0.15 = 0.78 Gbps. Subscribers
per satellite is capacity over the per-user load (active rate times peak
concurrency), rounded half up: 780 Mbps / (1.0 x 0.025) = 31,200. The fleet is
the capacity need clamped between the coverage floor and the saturation cap:
min(2,000, max(340, ceil(target / density))), so the 10-million baseline binds
at 340 on coverage. Per-user peak rate is the active rate by construction;
off peak is the smaller of the single-beam pool (spectrum times efficiency,
5.2 Mbps) and the rate scaled by the concurrency ratio, so 5.0 Mbps. Satellites
per launch couples inversely to aperture, floored, never below one:
max(1, floor(12 x 25 / aperture)), which is 12 at the baseline and 5 at the
60-square-meter what-if. The result rides the unchanged fleet machinery for
cost and launches. The engine also computes the cellular family's cost-plus
revenue line on the shared trajectory, but the Iridium artifact does not
publish it as of iridium-v3 (investor direction 2026-07-10). When the ARPU block
is set, the published four-bucket revenue case derives: one pool anchored to
fleet capacity (fleet target times density, 62,400,000 connections at the
baseline), four bucket counts by mix percentage (standard the exact residual,
so the people identity holds by construction), revenue per bucket as count
times price times twelve months, and the margin against the steady-state fleet
cost.

**The frozen-test discipline.** The family's test suite locks every baseline
number (capacity, density, fleet, pool, rates, aggregate, launch identity,
cost per subscriber) as exact assertions, plus the named variants: the rich
tier, the coordinated spectrum, the device ladder, the aperture what-if with
its fold caveat, and the launch coupling. Two honesty features are themselves
tested: the model reports below-target deployment truthfully (the rich tier
reaches 576 of its 802-satellite fleet by FY2036 at the config-default 0.18
share and says so; the promoted all-in scenario completes the same 802 fleet
in 2033), and the fold caveat emits strictly above 25.0 square meters.

**The equality tripwire.** One test runs both families and asserts the Iridium
baseline trajectory equals the cellular default trajectory field by field
(both bind at the 340 floor; the aperture identity holds at 25.0; cost per
subscriber matches to the last digit, 7.951337204338448 dollars). A shared
engine drift moves both models together and the equality holds; anything that
moves one family alone breaks loudly. The premise is registered in the
[assumptions ledger](assumptions.md) so a deliberate dial change that breaks
it surprises nobody.

## The Promotion Flow

```
code/scenarios/iridium.yaml      edit the dials (or copy for a variant)
        |
        v
run the model                    the loader + engine path (see README)
        |
        v
communications/models/iridium/default.json     the promoted output
        |
        v
communications/conclusion.md     reviewed and updated deliberately
```

Promotion refreshes the JSON only. The conclusion is static editorial prose:
after any scenario change, a person reviews the promoted JSON and updates the
conclusion by hand, then this ledger's maintenance rule applies
([assumptions.md](assumptions.md)). Local experiment runs stay out of Git;
only defaults worth publishing are promoted.

## Naming Conventions

- Model families carry descriptive names, never letter codes: the Iridium
  model, the High-Bandwidth Cellular Pure Play model. Files, scenarios, and
  output strings follow the family name (`iridium.yaml`,
  `models/iridium/default.json`).
- The three lanes are quoted exactly: cellular (phones on cellular spectrum),
  broadband (dish on Ku/Ka), MSS (Iridium L-band).
- Subscribers are people. IoT are devices. The two are never summed.
- Frequency (where the dial sits, 1.6 GHz) and spectrum (how much is held,
  8 to 10.5 MHz) are kept separate everywhere.
- Estimates are labeled; every load-bearing number traces to a `COMM-*` claim
  or a registered assumption.
