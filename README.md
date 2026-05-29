# Rocket Lab Research

Rocket Lab Research asks one practical question: what new orbital business could
Rocket Lab build with the rockets and spacecraft it already makes? Each
candidate application gets its own honest, source-linked feasibility study.

## Bottom line

The first application studied is a **Neutron-launched orbital AI-inference data
center**. By **2036**, under deliberately conservative assumptions, the model
lands here:

| Metric (by 2036) | Modeled value |
|---|---|
| Annual revenue | about **$5.94B** |
| Annual gross profit | about **$1.74B** (about **29.3%** margin) |
| Cost vs. an equivalent ground build | about **1.92x** |

Not parity with the ground, but close enough to take seriously. The full story,
with every number traced to a source, is in the
[data-center conclusion](data_center/conclusion.md).

## Applications

| Application | Vehicle | Status |
|---|---|---|
| Orbital AI-inference data center | Neutron | Modeled (current) |
| Communications | (TBD) | Planned |

## Where to read it

The data center is the only modeled application today. Read it in three depths:

- [conclusion.md](data_center/conclusion.md): the verdict and the headline numbers.
- [data_center/README.md](data_center/README.md): how the application works and how to run the model.
- [`models/space/default.json`](data_center/models/space/default.json): every number with its formula, units, and source.

Communications is a reserved workstream; it makes no model claims in this
release.

## Repository map

```text
rklb_space_data_center/
├── README.md            # this file: the program and its applications
├── data_center/         # the data-center application (conclusion, guide, models)
├── communications/      # reserved, not yet modeled
├── research/            # shared evidence wiki and source ledger
├── code/                # the model engine (rklb-value)
└── docs/                # architecture intent, ADRs, agent guide
```

## Running the model

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
