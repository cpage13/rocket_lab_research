# Rocket Lab Research

Rocket Lab Research asks one practical question: what new orbital business could
Rocket Lab build with the rockets and spacecraft it already makes? Each
candidate application gets its own honest, source-linked feasibility study.

## Applications

| Application | Vehicle | Status |
|---|---|---|
| Orbital AI-inference data center | Neutron | Modeled (current) |
| Communications | (TBD) | Planned |

The data center is the only modeled application today. Communications is a
reserved workstream with no model claims in this release.

## Data Center

The first application is a Neutron-launched orbital AI-inference data center.
The operating idea is concrete: integrate GPUs and networking on the ground,
package them into rack-like orbital nodes, attach each node to a Rocket Lab bus
with solar, radiators, thermal, and communications, launch on Neutron, and
operate the result as laser-linked orbital compute.

## Bottom Line

The model ramps for years, but **2036** is the takeoff. That year Rocket Lab
launches **90 Neutron missions**, deploys **90 new orbital nodes**, and adds
about **38 MW** of new orbital compute power. That is the cadence story.

The revenue run-rate is separate. By 2036 the active on-orbit base reaches
**268 nodes** and about **112 MW**, producing roughly **$5.94B** in annual
revenue and **$1.74B** in annual gross profit, about **29.3%** gross margin. The
build-and-launch program runs about **1.92x** the cost of an equivalent ground
data center: not parity, but close enough to take seriously.

## Where To Read It

The full data-center case, with every number traced to a source:

- [conclusion.md](data_center/conclusion.md): the verdict and the headline numbers.
- [data_center/README.md](data_center/README.md): how the application works and how to run the model.
- [`models/space/default.json`](data_center/models/space/default.json): every number with its formula, units, and source.

## Repository Map

```text
rklb_space_data_center/
├── README.md            # this file: the program and its applications
├── data_center/         # the data-center application (conclusion, guide, models)
├── communications/      # reserved, not yet modeled
├── research/            # shared evidence wiki and source ledger
├── code/                # the model engine (rklb-value)
└── docs/                # architecture intent, ADRs, agent guide
```

## Running The Model

```sh
cd code
uv sync 2>&1 | tee /tmp/rklb_uv_sync.txt
uv run rklb-value scenarios/default.yaml --json 2>&1 | tee /tmp/rklb_model_output.json
uv run rklb-value --promote 2>&1 | tee /tmp/rklb_promote.txt
```

`--promote` refreshes the JSON under `data_center/models/`. It does not rewrite
the [conclusion](data_center/conclusion.md); after a model change, review the
artifacts and update the conclusion deliberately.

## Disclaimer

This is an independent research project with **no affiliation with, sponsorship
by, or endorsement from Rocket Lab**. "Rocket Lab" and "Neutron" name the
real-world company and vehicle the analysis reasons about; all trademarks belong
to their respective owners.

Nothing here is a Rocket Lab plan, guidance, or official figure. The numbers are
source-linked feasibility estimates and chosen scenario assumptions, not
predictions, forecasts, or financial projections. **Do not use this repository
as investment advice or as a basis for any investment decision.** It is provided
"as is" under the [MIT License](LICENSE), for research and discussion only.

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 Chris Page.
