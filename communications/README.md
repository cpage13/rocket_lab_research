# Communications Workstream

This folder holds the communications application of Rocket Lab Research: model
families organized by communication paradigm, each asking what a
Neutron-launched fleet could deliver on a specific kind of spectrum to a
specific kind of device. For the current verdict and the numbers, read the
[conclusion](conclusion.md). This page is the guide to what is here and how to
use it.

## Operating Picture

Communications is not one market. The workstream keeps three paradigms strictly
separate, because the device, the spectrum, and the competition are different
in each:

- **Cellular**: phones on cellular spectrum. The phone already has the radio;
  the spectrum must be leased or bought.
- **Broadband**: a dish on Ku/Ka spectrum. Abundant spectrum and terminal-gain
  physics; Starlink's home market.
- **MSS**: Iridium's owned L-band to purpose-built or in-chipset devices.
  Owned, global, thin spectrum.

Each modeled family gets its own scenario, its own config block on the shared
engine, and its own promoted JSON under [models/](models/). Subscribers are
people; IoT are devices, counted separately.

## The Model Families

The first and current focus is **the Iridium model** (formerly Model B): the
maximum practical performance of Iridium's owned 8 to 10.5 MHz of L-band,
delivered to a ladder of devices (purpose-built terminals, IoT modules, and
conditionally phone-class chipsets), on a Neutron-launched next-generation
fleet over the next 10 to 15 years, with a larger, heavier rocket as a
possible later step. Rocket Lab's acquisition of
Iridium makes this the incumbent-modernization question, and the
[conclusion](conclusion.md) carries its verdict.

The second family is **the High-Bandwidth Cellular Pure Play model** (formerly
Model A), kept and documented: phones on cellular spectrum, compared per
subscriber against ground cellular. It is the greenfield direct-to-cell
question, and it shares the fleet, cost, and cadence machinery with the Iridium
model.

More paradigms may follow. The broadband dish lane is deliberately unmodeled:
it is the easier case, with abundant spectrum and proven terminal physics, and
modeling effort goes where the constraint is.

## Reading Path

| Path | What it is |
|---|---|
| [conclusion.md](conclusion.md) | The Iridium model verdict and headline numbers. Start here. |
| [assumptions.md](assumptions.md) | The default-assumption ledger and source-status taxonomy. |
| [design.md](design.md) | The workstream architecture: families, folders, the derivation spine, promotion. |
| [models/iridium/default.json](models/iridium/default.json) | The promoted Iridium model: the frozen baseline with sources. |
| [CURRENT_STATE.md](CURRENT_STATE.md) | Short workstream handoff. |
| [../code/scenarios/iridium.yaml](../code/scenarios/iridium.yaml) | The input dials that produce the promoted model. |
| [../code/src/communications/](../code/src/communications/) | The shared engine and the per-family config blocks. |
| [../research/README.md](../research/README.md) | The evidence wiki and the `COMM-*` source ledger. |

## Running The Model

From the repository root:

```sh
cd code
uv run python -c "
from communications.config import load_comms_config
from communications.engine import run_comms_model
print(run_comms_model(load_comms_config('scenarios/iridium.yaml')).iridium)
" 2>&1 | tee /tmp/comms_iridium_output.txt
```

Promotion refreshes [models/iridium/default.json](models/iridium/default.json).
It does not rewrite [conclusion.md](conclusion.md); after a scenario change,
review the JSON and update the conclusion deliberately.

## Worth Knowing

The service is device-diverse, and the phone is one path rather than the
focus: purpose-built terminals (a puck, a USB device with a small antenna on a
laptop, mounted units) and IoT modules need no chipmaker's permission, and the
baseline is computed at the weakest device class, so every other device does
better on the same fleet. The phone-class numbers carry a stated ecosystem
assumption: Iridium's band is in no standard phone chipset today, and the
model states that in every output rather than assuming it silently. Every
load-bearing number is estimate-tier and traceable through the
[assumptions ledger](assumptions.md) to the research wiki.

The data-center workstream is the sibling application; see
[../data_center/README.md](../data_center/README.md).
