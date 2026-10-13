# Communications

This folder holds the communications application of Rocket Lab Research: what
a Neutron-launched fleet could deliver on Iridium's owned L-band, and what that
network would sell. For the verdict and the numbers, read the
[conclusion](conclusion.md). This page is the guide to what is here and how to
use it.

## Operating Picture

Communications is not one market. The application keeps three paradigms
strictly separate, because the device, the spectrum, and the competition are
different in each:

- **Cellular**: phones on cellular spectrum. The phone already has the radio;
  the spectrum must be leased or bought.
- **Broadband**: a dish on Ku/Ka spectrum. Abundant spectrum and terminal-gain
  physics; Starlink's home market.
- **MSS**: Iridium's owned L-band to purpose-built or in-chipset devices.
  Owned, global, thin spectrum.

The Iridium model has its own scenario, its own module and two promoted
artifacts under [models/iridium/](models/iridium/): the saturation curve and
the model's own artifact. The product case is its own model on that artifact,
with its own scenario and artifact. People and IoT devices are counted
separately and never added.

## The Models

The current focus is **the Iridium model** (formerly Model B), the engineering
case: the most Iridium's owned 8 MHz of L-band can carry on a Neutron-launched
next-generation fleet at the full launch cadence. It sells every seat each
people class's fleet carries: the small terminal, the mounted terminal, and a
phone class that waits on a phone chip for the band. It publishes IoT's room and
each IoT class's capacity beside them, never a count sold. The coordinated
10.5 MHz (COMM-611) is a linear note in the conclusion, not a run. Rocket Lab's
acquisition of Iridium makes this the incumbent-modernization question.

Beside it is **the product case**: what that network would sell at the
investor's prices, held flat, to four classes (the small terminal, the
mounted terminal, minimal-packet IoT and data IoT), over 2,000 drawn markets.
Its headline is the typical market. It reads the Iridium model's artifact and
never feeds it. The two cases stand side by side and never add.

**The High-Bandwidth Cellular Pure Play model** (formerly Model A) is kept and
documented, and on hold: phones on cellular spectrum, compared per subscriber
against ground cellular. It is the greenfield direct-to-cell question, and it
shares the fleet, cost, and cadence machinery with the Iridium model. It has
no scenario file or artifact of its own.

More paradigms may follow. The broadband dish lane is deliberately out of
scope: it has abundant spectrum and established terminal physics, so it is a
different, well-trodden problem, and this work focuses the modeling effort on
the thin-spectrum MSS constraint. That is a research scope choice, not a
verdict from this model.

## Reading Path

| Path | What it is |
|---|---|
| [conclusion.md](conclusion.md) | The verdict and headline numbers, both cases side by side. Start here. |
| [assumptions.md](assumptions.md) | The default-assumption ledger and source-status taxonomy. |
| [design.md](design.md) | The application's architecture: the models, folders, the curve and its readings, promotion. |
| [models/iridium/default.json](models/iridium/default.json) | The Iridium model's artifact (the engineering case), schema `iridium-v7`, with its stated assumptions. |
| [models/iridium/saturation_curve.json](models/iridium/saturation_curve.json) | The saturation curve the Iridium model reads, schema `saturation-v1`. |
| [models/product_case/default.json](models/product_case/default.json) | The product case's artifact, schema `product-case-v1`. |
| [CURRENT_STATE.md](CURRENT_STATE.md) | Short handoff. |
| [../code/scenarios/iridium.yaml](../code/scenarios/iridium.yaml) | The Iridium scenario. |
| [../code/scenarios/product_case.yaml](../code/scenarios/product_case.yaml) | The product case's scenario. |
| [../code/src/communications/](../code/src/communications/) | The Iridium model, the saturation module and the shared engine. |
| [../code/src/product_case/](../code/src/product_case/) | The product case. |
| [../research/README.md](../research/README.md) | The evidence wiki and the `COMM-*` source ledger. |

## Running The Models

From `code/`, run the Iridium model in Python:

```sh
uv run python -c "
from pathlib import Path
from communications.config import load_comms_config
from communications.iridium import run_iridium_model
from communications.saturation_curve import load_saturation_curve
config = load_comms_config('scenarios/iridium.yaml')
curve = load_saturation_curve(Path('..') / config.iridium.saturation.curve_path)
print(run_iridium_model(config, curve).iridium.years[-1])
"
```

Promote the artifacts, in order, from `code/` (a relative output path anchors
to the repository root):

```sh
uv run python -m communications.json_output scenarios/iridium.yaml \
    communications/models/iridium/default.json
uv run python -m product_case.json_output scenarios/product_case.yaml \
    communications/models/product_case/default.json
```

The product case reads the Iridium artifact, so it is promoted again whenever
that artifact changes. The saturation curve has its own command,
`uv run python -m communications.saturation scenarios/iridium.yaml
communications/models/iridium/saturation_curve.json`, needed only when one of
the curve's inputs changes: its last measured run took about 30 minutes and a
14 GB memory bound, so it is never run casually. Promotion does not rewrite
[conclusion.md](conclusion.md); after a scenario change, review the JSON and
update the conclusion deliberately.

## Worth Knowing

The service is device-diverse, and the phone is a later path rather than the
focus: the small terminal and the mounted terminal are purpose-built, and IoT
modules need no chipmaker's permission. Every class runs side by side in one
run, each class's column the whole fleet sold to that class alone, never
summed. The phone class carries a stated ecosystem assumption: Iridium's band
is in no standard phone chipset today, and the model states that in every
output rather than assuming it silently. IoT is the network's focus: the
engineering case publishes its room and capacity, the product case its devices
and revenue. Each number carries its basis (investor-set, certified, a sourced
or derived estimate, a scenario value), traceable through the
[assumptions ledger](assumptions.md) to the research wiki.

The data-center application is the sibling; see
[../data_center/README.md](../data_center/README.md).
