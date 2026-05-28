# Rocket Lab Research

Rocket Lab Research asks whether Rocket Lab could turn Neutron into an
infrastructure machine: build AI-inference nodes on the ground, integrate them
with Rocket Lab buses, solar, radiators, thermal systems, and communications,
launch them repeatedly, and compound the learning into an orbital compute
business.

The first investigation is not a Rocket Lab plan, guidance document, precision
revenue forecast, or DCF. It is a transparent, source-linked feasibility case.
The current baseline is conservative: it translates public terrestrial
AI-hardware trajectories into a Neutron-centered orbital stack before any
fully space-optimized engineering pass. That is the point. The repository
shows what already looks interesting, what the numbers say, and where Rocket
Lab-style vertical integration could make the next version better.

One important upside is not fully credited in the baseline numbers: many cost
lines are treated like external buy prices or customer-facing prices. In the
actual Rocket Lab version, Rocket Lab would be its own infrastructure customer
for much of the stack: spacecraft bus, solar, radiators, thermal systems,
integration, launch, operations, and potentially communications. GPUs and some
networking hardware remain the obvious outside purchases. That means the same
program that generates compute revenue can also create internal demand for
Rocket Lab hardware, reliably book Neutron launches, and turn supplier margin
into manufacturing learning and controlled cost.

## What This Repository Contains

Rocket Lab Research is organized around feasibility investigations. The current
public investigation is **Data Center**. The research wiki supports that case
with source notes, claim IDs, and open questions. Communications is present as a
future work area, but it is not modeled yet.

## Data Center

The first focus area is a Neutron-launched orbital AI-inference data center.
The practical vision is simple: buy GPUs and networking hardware, package them
into rack-like compute nodes, test them on the ground, attach them to a
Rocket Lab-built spacecraft bus with power, thermal, and communications, launch
on Neutron, and operate laser-linked orbital capacity for customers that value
scarce, secure, solar-powered infrastructure.

This is not just a payload story. It is also a customer story inside Rocket
Lab: the data-center program would buy the company's own buses, solar,
radiators, integration flow, launch service, and operations capacity. The model
is already interesting before giving Rocket Lab credit for capturing that
internal demand.

The model takes off in **2036**. The ramp starts earlier: by the middle years,
cadence is leaving prototype scale and the central case is already producing
positive gross margin. But **2036** is where the S-curve begins to look like
infrastructure: **90 Neutron launches** in one year, **90 new orbital nodes**,
and about **38 MW** of new orbital node power added in that year alone.

That is the cadence story. The revenue run-rate is separate. By the same year,
the active on-orbit base reaches **268 nodes** and about **112 MW**, producing
roughly **$5.94B** in annual revenue and **$1.74B** in annual gross profit at a
**29.3%** gross margin. Keep those lanes separate: **2036 cadence** is what
Rocket Lab launches and deploys that year; **2036 active base** is the
installed base producing annual revenue.

[Click here to get to the conclusion.](data_center/conclusion.md)

The modeled product is orbital AI inference. Frontier-model training is outside
the current default. Neutron is the focus because it is the relevant Rocket Lab
vehicle for this scale today. The model does not claim raw ground parity: the
current 2036 orbital build-plus-launch reference is about 1.92x the comparable
five-year ground reference. That is close enough to be strategically
interesting, especially because the largest visible orbital burdens are
identifiable: solar, radiator, mass, launch, and the engineering choices around
them.

The model's current scale guardrail is modest: the **2036** cadence year adds
about **38 MW** of new orbital node power, rounded elsewhere to about
**40 MW/year**. That new annual deployment is compared with a rough **100 GW**
market reference only as a scale sanity check, not as a market-share claim.

## Repository Map

```text
rklb_space_data_center/
├── README.md
├── AGENTS.md
├── data_center/
│   ├── README.md
│   ├── assumptions.md
│   ├── conclusion.md
│   └── models/
├── communications/
│   ├── README.md
│   └── models/.gitkeep
├── code/
│   ├── pyproject.toml
│   ├── README.md
│   ├── scenarios/
│   ├── src/
│   └── tests/
├── docs/
│   ├── architecture-intent.md
│   ├── agent-guide.md
│   └── adr/
└── research/
    ├── README.md
    ├── SOURCE_INDEX.md
    └── topic folders
```

The main areas are:

- **Data Center** lives in [data_center/](data_center/). Start with
  [data_center/README.md](data_center/README.md), then read the
  [data-center conclusion](data_center/conclusion.md) and
  [assumptions ledger](data_center/assumptions.md).
- **Research** lives in [research/](research/). Start with
  [research/README.md](research/README.md), then use
  [research/SOURCE_INDEX.md](research/SOURCE_INDEX.md) to check source status
  for quoted numbers.
- **Model code** lives in [code/](code/). Use [code/README.md](code/README.md)
  to run the model, refresh generated artifacts, and inspect outputs.
- **Communications** lives in [communications/](communications/) and is reserved
  for a future researched workstream. It makes no model claims in this release.
- **Agent and maintainer docs** live in [AGENTS.md](AGENTS.md),
  [docs/agent-guide.md](docs/agent-guide.md), and
  [docs/architecture-intent.md](docs/architecture-intent.md).

## Key Files

For a quick human read, the most important files are the
[data-center conclusion](data_center/conclusion.md),
[data-center guide](data_center/README.md),
[assumptions ledger](data_center/assumptions.md), and
[source index](research/SOURCE_INDEX.md).

## Running The Model

Use `uv`; this repository does not require a separate `uvx` or `uvnx` path.

```sh
cd code
uv sync 2>&1 | tee /tmp/rklb_uv_sync.txt
uv run rklb-value scenarios/default.yaml --json 2>&1 | tee /tmp/rklb_model_output.json
uv run rklb-value --promote 2>&1 | tee /tmp/rklb_promote.txt
```

The `--promote` command refreshes the JSON artifacts under
`data_center/models/`. It does not rewrite `data_center/conclusion.md`; after a
model change, review the generated artifacts and update the conclusion
deliberately.

The top-level [communications](communications/README.md) folder is a future
researched workstream. It makes no communications model claims in this release.

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
