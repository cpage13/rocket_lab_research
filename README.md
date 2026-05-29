# Rocket Lab Research

Rocket Lab Research is an independent feasibility program. The method is the
same every time: take an orbital application Rocket Lab could plausibly build,
model it honestly against public evidence, and find out whether it pencils out.
Each investigation is a **case**.

The first case pencils out. Under deliberately conservative, source-linked
assumptions, a Neutron-launched orbital AI-inference data center models to
roughly **$5.94B in annual revenue** at about **29.3% gross margin** by
**2036**, for about **1.92x** the cost of an equivalent ground build. Not
parity, but close enough to take seriously.

What makes it worth modeling is who would build it. Rocket Lab already makes and
launches spacecraft, so for an orbital business it would supply most of the
stack to itself: the Neutron launch, the bus, solar, radiators, thermal,
integration, and operations. Only the GPUs and some networking are outside
purchases. Any other entrant has to buy launch, spacecraft, and integration at
market price; Rocket Lab turns those into internal cost, manufacturing learning,
and a steady book of Neutron launches. Each case pressure-tests that advantage
against one real application.

## Cases

| # | Application | Vehicle | Status |
|---|---|---|---|
| **1** | Orbital AI-inference data center | Neutron | **Modeled, current** |
| 2 | Communications | (TBD) | Planned |

**Case 1, the orbital data center,** is the only modeled case today. Read it in
three depths: the [conclusion](data_center/conclusion.md) for the verdict, the
[data-center guide](data_center/README.md) for how it works, and
[`models/space/default.json`](data_center/models/space/default.json) for every
number with its provenance.

**Case 2, communications,** is a reserved workstream. It makes no model claims
in this release.

## Repository Map

```text
rklb_space_data_center/
├── README.md            # this file: the program and its cases
├── data_center/         # Case 1: conclusion, assumptions, model artifacts
├── communications/      # Case 2: reserved, not yet modeled
├── research/            # shared evidence wiki and source ledger
├── code/                # the model engine (rklb-value)
└── docs/                # architecture intent, ADRs, agent guide
```

- **Case 1, Data Center,** lives in [data_center/](data_center/): start with the
  [conclusion](data_center/conclusion.md), then the
  [guide](data_center/README.md) and
  [assumptions ledger](data_center/assumptions.md).
- **Research** lives in [research/](research/): the evidence behind every claim.
  Use [SOURCE_INDEX.md](research/SOURCE_INDEX.md) to check the status of any
  quoted number.
- **Model code** lives in [code/](code/): see [code/README.md](code/README.md)
  to run the model and regenerate artifacts.
- **Maintainer docs** live in [AGENTS.md](AGENTS.md),
  [docs/agent-guide.md](docs/agent-guide.md), and
  [docs/architecture-intent.md](docs/architecture-intent.md).

## Running The Model

Use `uv`:

```sh
cd code
uv sync 2>&1 | tee /tmp/rklb_uv_sync.txt
uv run rklb-value scenarios/default.yaml --json 2>&1 | tee /tmp/rklb_model_output.json
uv run rklb-value --promote 2>&1 | tee /tmp/rklb_promote.txt
```

`--promote` refreshes the JSON artifacts under `data_center/models/`. It does
not rewrite [data_center/conclusion.md](data_center/conclusion.md); after a
model change, review the artifacts and update the conclusion deliberately.

## Disclaimer

This is an independent research project with **no affiliation with, sponsorship
by, or endorsement from Rocket Lab**. "Rocket Lab" and "Neutron" are used only
to name the real-world vehicle and company the analysis reasons about; all
trademarks belong to their respective owners.

Nothing here is a Rocket Lab plan, guidance, or official figure. The numbers are
source-linked feasibility estimates and chosen scenario assumptions, not
predictions, forecasts, or financial projections. **Do not use this repository
as investment advice or as a basis for any investment decision.** It is provided
"as is" under the [MIT License](LICENSE), for research and discussion only.

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 Chris Page.
