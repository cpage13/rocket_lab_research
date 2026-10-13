# Communications Design

This document is the architecture of the communications application: how
model families are organized, where everything lives, how the Iridium model
and the product case are built, and how a scenario becomes a published
number. It describes structure, not results; the results live in the
[conclusion](conclusion.md).

## Model Families By Paradigm

The unit of organization is the model family: one communication paradigm, one
device population, one spectrum position, modeled end to end. The paradigms
are the three lanes, kept strictly separate:

- **Cellular**: phones on cellular spectrum (leased or bought). Modeled as
  the High-Bandwidth Cellular Pure Play model, kept and on hold.
- **Broadband**: a dish on Ku/Ka spectrum. Deliberately unmodeled, the easier
  case.
- **MSS**: Iridium's owned L-band to purpose-built or in-chipset devices.
  Modeled as the Iridium model, the current focus, with the product case
  beside it.

A family is not a fork of the codebase. Every family shares one fleet-and-cost
loop (the cadence ramp, the cohort treadmill, the build, launch and
replacement cost lines), which carries no revenue. A family contributes only
what makes it different: a config block of dials, its own module with its
deployment rule and its people and revenue, a scenario file, and a test suite.
The cellular family sets subscriber density directly as a dial (75,000 per
satellite on its 25 MHz basis) and carries the ground cost comparison; the
Iridium family reads its people from a promoted saturation curve.

How a new family gets added, in order:

1. Ground it in the research wiki first: claims with `COMM-*` ids, estimate
   tiers labeled, the lane named.
2. Brainstorm and design with the investor; the investor sets every assumption
   value (the model never invents one).
3. Plan, adversarial review, investor approval, then build: a dials block in
   `config.py`, named constants with their bases in `constants.py`, and one
   module for the family with its deployment rule (as `iridium.py` has
   `full_cadence_rule`).
4. A scenario YAML named for the family, and a test suite that pins its
   numbers.
5. Promote to `communications/models/<family>/default.json` and write the
   conclusion prose deliberately.

## The Folder Map

```
communications/                           the application's documents (this folder)
  README.md                               operating picture and reading path
  conclusion.md                           the static, reviewed verdict
  assumptions.md                          the default-assumption ledger
  design.md                               this document
  CURRENT_STATE.md                        short handoff
  data/                                   the shipped population grid and its attribution
  models/iridium/saturation_curve.json    the promoted saturation curve
  models/iridium/default.json             the promoted Iridium model (the engineering case)
  models/product_case/default.json        the promoted product case
code/
  src/communications/                     the Iridium model, the curve, the shared engine
    constants.py                          named constants, one section per family
    config.py                             frozen Pydantic config tree, per-family dials
    engine.py                             the shared fleet-and-cost loop, the cellular family
    iridium.py                            the Iridium family: its entry, full-cadence rule, record
    saturation.py                         the curve's computation and its command (numpy)
    saturation_curve.py                   the curve's contract, loader, identity check, readings
    ground.py                             the cellular family's ground comparison
    json_output.py                        the Iridium artifact's writer and command
  src/product_case/                       the product case, its own package (ADR 012)
  scenarios/iridium.yaml                  the Iridium model's settings
  scenarios/product_case.yaml             the product case's settings
  tests/communications/                   the Iridium and cellular suites plus shared guards
  tests/product_case/                     the product case's suite
research/                                 the evidence wiki (COMM-* claim ledger)
```

The data-center model is the sibling application under `data_center/` and
`code/src/data_center/`. The shared cadence spine has its own guard
(`code/tests/common/test_cadence_move.py`), and a cross-import guard keeps the
packages separate.

## The Iridium Model's Structure

**The dials.** The scenario's `iridium:` block holds the held spectrum (8.0 MHz
exclusive), the panel (15.4 m^2), the label, the saturation block (the
downlink share, 0.67, and the promoted curve's path) and the three class
prices (the small terminal $10, the mounted terminal $50 and the phone class
$15 a month, held flat). Each class's usage and spectral efficiency are named
constants, not settings. The scenario also sets 16 satellites per launch, the
all-in cadence share (1.0, investor-set 2026-07-14) and the flat costs
(satellite build 1.0 million dollars, launch 13.0 million at every cadence),
leaving the shared config defaults untouched. There is no fleet target and no
cap.

**The saturation curve.** Computed once by its command and promoted to
`models/iridium/saturation_curve.json`. For each people class and each of 24
requested fleets from 340 to 40,000 satellites (the mounted terminal also at
48,000 and 64,000), on a shell at 450 km and 53 degrees, it counts the
useful beams: the co-channel beams a fleet keeps lit over inhabited cells of
a shipped world population grid (2030, a quarter degree), filled smallest
footprint first; the directional terminals stack layers under sky sectors.
It is computed at the 25 m^2 reference panel with the band in full-time use
(d = 1). It carries each class's markers (maximum use, the saturation
number), the phone class's band points and interference trim, and its stated
limits. Its full method is in its `provenance.method`.

**The run, in four steps.**

1. The fleet: every comms launch the cadence share allows, times the
   satellites per launch, each cohort living five years (the full-cadence
   rule). No saturation number sizes, caps, stops or slows the build.
2. The years: at each year's living fleet each class reads the curve. Its
   people are the curve's capacity there, times the downlink share and the
   panel factor (15.4 / 25 = 0.616), over the class's busy-hour load, rounded
   half up. From the coverage floor (340) on, every seat is sold at the
   class's flat price, and its own margin is its revenue against the fleet's
   whole annualized cost. Each year also carries IoT's room on the phone
   class's useful beams in the uplink's share of the frame, and each IoT
   class's device capacity alone (ADR 011).
3. The readings: every class at the coverage floor, at 2,000 (the retired
   cap, kept for comparison), at the horizon's end and at the steady state
   beyond it.
4. Each class's block: its price, usage and physics, its markers from the
   curve, the limit that binds at the horizon's end (the launch cadence for
   every class), and where the next satellite stops paying at full price.

A run reads only a curve computed for its own inputs (the identity check):
another held spectrum is refused until the curve is computed for it. A fleet
past a class's last computed row is refused, never extrapolated.

**The test discipline.** The suite (`code/tests/communications/`) pins each
class's physics, IoT's room and capacity, the headline every class alone and
side by side, the no-upgrade bracket, revenue rising with the fleet, the
floor rule, the prices, the downlink share, the panel setting, the readings,
the marginal intervals and the refusals, on the committed curve or on a
synthetic curve stamped for the dials a test sets.

**The equality tripwire.** One test runs both families: an Iridium run and a
cellular run whose fleet target the horizon never reaches share the
fleet-and-cost record whole, and that record's values are frozen. A shared
engine drift that moves both families alike fails on the frozen values;
anything that moves one family's shared record alone breaks the equality. The
premise is registered in the [assumptions ledger](assumptions.md).

## The Product Case's Structure

The product case is its own package, `code/src/product_case/` (ADR 012). It
reads only the Iridium model's promoted artifact, its schema pinned and its
SHA-256 recorded, and nothing it computes feeds that model. Its method, in
brief:

1. The network: the terminals' seats from the engineering case's people in
   today's mix of beams, the network's scale over today's terminal customers,
   and IoT's rooms, as the artifact publishes them.
2. The offers: each choice's prices (the investor's, held flat, with lower
   ones as context) and each IoT class's usage at its scale.
3. The demand curve, anchored on Iridium's customers and ARPU today: it grows
   each class with the network's scale, the price and the service.
4. Sold: a terminal up to its seats; an IoT class uncapped, bounded by its
   room, access and tone time through the usable test.
5. A year's numbers: revenue, the margin against the fleet's annual cost,
   profit, IoT's uses, the GB carried and the cost per GB.
6. The usable test in each of 2,000 drawn markets: the margin floor, the fill
   floor, IoT within its room, revenue rising.
7. Each choice's summary over the markets.
8. The pick: the most median revenue among the usages usable in at least three
   quarters of the markets.
9. The headline at the central market, with the spreads over the usable and
   all draws and the headline's rank in each.

numpy is its runtime dependency in one module, `monte_carlo.py` (ADR 010's
scope widened by ADR 012). Its suite is `code/tests/product_case/`.

## The Promotion Flow

```
code/scenarios/iridium.yaml           edit the settings
        |
        v   only when one of the curve's inputs changes:
python -m communications.saturation   about 30 minutes, a 14 GB memory bound
        |
        v
models/iridium/saturation_curve.json  the promoted curve
        |
        v
python -m communications.json_output
        |
        v
models/iridium/default.json           the promoted Iridium model
        |
        v   every time the Iridium artifact changes:
python -m product_case.json_output    reads code/scenarios/product_case.yaml
        |
        v
models/product_case/default.json      the promoted product case
        |
        v
communications/conclusion.md          reviewed and updated deliberately
```

Promotion refreshes the JSON only. The conclusion is static editorial prose:
after any scenario change, a person reviews the promoted JSON and updates the
conclusion by hand, then the ledger's maintenance rule applies
([assumptions.md](assumptions.md)). Local experiment runs stay out of Git;
only defaults worth publishing are promoted.

## Naming Conventions

- Model families carry descriptive names, never letter codes: the Iridium
  model, the High-Bandwidth Cellular Pure Play model. Files, scenarios, and
  output strings follow the family name (`iridium.yaml`,
  `models/iridium/default.json`).
- The three lanes are quoted exactly: cellular (phones on cellular spectrum),
  broadband (dish on Ku/Ka), MSS (Iridium L-band).
- The classes run the small terminal, the mounted terminal, the phone class
  (and in the product case minimal-packet IoT and data IoT), never
  phone-first, one name per class.
- Subscribers are people. IoT are devices. The two are never summed.
- Frequency (where the dial sits, 1.6 GHz) and spectrum (how much is held,
  8 MHz exclusive of the 10.5 MHz coordinated span, COMM-611) are kept separate
  everywhere.
- Estimates are labeled; every load-bearing number traces to a `COMM-*` claim
  or a registered assumption.
