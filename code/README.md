# rklb-value Code Guide

`code/` contains the runnable Python model for the data-center workstream. It
turns YAML scenarios into typed JSON artifacts and text reports. The package is
data-center first; `communications` is reserved for a future researched
workstream in this release.

The project configuration in `pyproject.toml` requires Python `>=3.14` and uses
`uv` for environment and command execution. No `uvx` or `uvnx` command is
required for this repository.

## Setup

Run commands from `code/` unless noted.

```sh
cd code
uv sync 2>&1 | tee /tmp/rklb_uv_sync.txt
```

`uv` manages the local `.venv/` and installs the package plus development
dependencies from `pyproject.toml` and `uv.lock`.

## Run The Space Model

```sh
uv run rklb-value scenarios/default.yaml 2>&1 | tee /tmp/rklb_text_report.txt
uv run rklb-value scenarios/default.yaml --brief 2>&1 | tee /tmp/rklb_brief.txt
uv run rklb-value scenarios/default.yaml --json 2>&1 | tee outputs/data_center/runs/default.json
uv run rklb-value --default --json 2>&1 | tee outputs/data_center/runs/default_packaged.json
uv run rklb-value --input-schema 2>&1 | tee /tmp/rklb_input_schema.json
```

Scratch run outputs belong under `outputs/data_center/runs/`, which is ignored
by Git. The promoted public JSON lives outside the Python package under
`../data_center/models/`.

## Promote Public Artifacts

```sh
uv run rklb-value --promote 2>&1 | tee /tmp/rklb_promote.txt
```

Default promotion writes:

```text
../data_center/models/space/default.json
../data_center/models/ground/default.json
```

Promotion does not rewrite `../data_center/conclusion.md`. That file is static
reviewed prose tied to the promoted defaults. If the default scenario changes,
promote the JSON, inspect the diffs, and update the static conclusion
deliberately.

Named space artifacts are supported for local comparison:

```sh
uv run rklb-value scenarios/conservative.yaml --promote --output-name conservative 2>&1 | tee /tmp/rklb_promote_conservative.txt
```

That writes `../data_center/models/space/conservative.json`. The default ground
reference is written only for the default promoted output.

## Edit Scenarios

The public default scenario is `scenarios/default.yaml`. To experiment, copy it
to a new YAML file, edit the dials, and run the copy into the scratch directory:

```sh
cp scenarios/default.yaml scenarios/local_experiment.yaml
uv run rklb-value scenarios/local_experiment.yaml --json 2>&1 | tee outputs/data_center/runs/local_experiment.json
```

Do not treat code-level defaults as a second public contract. If a default
assumption changes, review `../data_center/assumptions.md`,
`../research/SOURCE_INDEX.md`, the promoted JSON, and
`../data_center/conclusion.md` together.

## Keep Code, JSON, Research, And Prose In Sync

Code changes can silently change public claims. If you edit model semantics,
scenario defaults, ground-reference assumptions, source IDs, or source-status
logic, do the full synchronization loop:

```sh
uv run rklb-value --promote 2>&1 | tee /tmp/rklb_promote.txt
git diff -- ../data_center/models/space/default.json ../data_center/models/ground/default.json
```

Then inspect the affected `RLDC-*` claims in `../research/SOURCE_INDEX.md`,
update `../data_center/assumptions.md` if the assumption ledger changed, and
review `../data_center/conclusion.md` before treating the repository as
publication-ready. The promoted JSON, source ledger, assumptions ledger, and
static conclusion must tell the same story.

## Test And Check

```sh
uv run ruff check . 2>&1 | tee /tmp/rklb_ruff.txt
uv run ruff format --check . 2>&1 | tee /tmp/rklb_format.txt
uv run mypy --strict . 2>&1 | tee /tmp/rklb_mypy.txt
uv run pytest 2>&1 | tee /tmp/rklb_pytest.txt
```

The project is strict-typed for source packages. Tests use pytest fixtures and
assert the public JSON contract, promotion behavior, validation metadata, query
examples, and the ground reference.

## Space JSON Contract

`uv run rklb-value <scenario> --json` emits a typed `SpaceModelOutput` with
five top-level keys:

| Key | Purpose |
|---|---|
| `metadata` | Scenario identity, schema version, horizon, artifact role, and generated timestamp. |
| `inputs` | Walkable config inputs plus `inputs.assumption_index` for source-traceable dials. |
| `physical` | Per-year node sizing, power, mass, volume, and per-node economics. |
| `business` | Per-year launches, deployed-year cohort, living fleet, revenue, gross profit, margin, and cumulative revenue. |
| `meta` | Data dictionary, formula definitions, validation results, source-status summary, and query examples. |

Every public numeric leaf under `physical.years` and `business.years` is a
provenance cell with `value`, `unit`, `formula`, `formula_name`, `uses`,
`sources`, `source_status`, and `description`. Use `inputs.assumption_index`
when tracing a public claim back to a scenario dial or `RLDC-*` source ID.

## Ground JSON Contract

Default promotion also builds `../data_center/models/ground/default.json`. It
anchors to the promoted space model's 2036 deployed-year cohort, not the living
fleet. Key fields:

| Field | Purpose |
|---|---|
| `anchor` | Space-model year, deployed nodes, GPU packages, kW, service life, and source paths. |
| `inputs` | Ground assumption cells and their source status. |
| `ground` | Five-year ground cost components and totals. |
| `orbital_reference` | Orbital build-and-launch reference for the same cohort. |
| `comparison` | Ground/orbit ratio, deltas, component deltas, warnings, and conclusion label. |
| `meta` | Query examples, validation results, data dictionary, and source-status summary. |

The current ground comparison links each ground input to a per-input
`RLDC-GROUND-*` source claim and reports
`comparison.conclusion_label = "same_order_of_magnitude"`. Treat it as an
order-of-magnitude screen, not a parity proof.

## Query Promoted JSON

This section is intentionally technical. Public-facing docs should use human
labels and `RLDC-*` claim IDs; code docs and agent diagnostics may use raw JSON
paths because their readers are auditing the model directly.

List the embedded query examples:

```sh
jq -r '.meta.query_examples[] | .name + " :: " + .jq' ../data_center/models/space/default.json
```

Run direct checks against the promoted space model:

```sh
jq '.business.years."2036".kw_deployed_this_year.value' ../data_center/models/space/default.json
jq '.business.years."2036".kw_living_fleet.value' ../data_center/models/space/default.json
jq '.inputs.assumption_index["inputs.config.cadence.launches_at_year_10"]' ../data_center/models/space/default.json
jq '.meta.validation.rules[] | select(.pass_check == false)' ../data_center/models/space/default.json
```

Run direct checks against the promoted ground reference:

```sh
jq '.anchor' ../data_center/models/ground/default.json
jq '.comparison.conclusion_label' ../data_center/models/ground/default.json
jq '.meta.validation_results[]? | select(.severity=="fail")' ../data_center/models/ground/default.json
```

## Validation Warnings

Space validation failures live at `meta.validation.rules[]` with
`pass_check == false`. Promoted defaults should not have failures.

Ground validation should preserve the deployed-year anchor and the parity
boundary. Warnings are acceptable when they describe scope limits, such as the
orbital reference mirroring build-and-launch cost only. Failures should block
promotion until fixed.

## Package Layout

```text
code/
├── pyproject.toml
├── uv.lock
├── scenarios/
│   ├── default.yaml
│   ├── ground_default.yaml
│   └── scenario variants
├── src/
│   ├── common/
│   ├── communications/
│   └── data_center/
│       ├── cli.py
│       ├── config.py
│       ├── engine.py
│       ├── fleet.py
│       ├── ground.py
│       ├── input_manifest.py
│       ├── json_output.py
│       ├── output.py
│       ├── provenance.py
│       ├── query_examples.py
│       └── validation.py
├── tests/
│   ├── communications/
│   └── data_center/
└── outputs/data_center/runs/
```

Public artifacts live outside `code/` so scratch runs and reviewed defaults do
not blur together.
