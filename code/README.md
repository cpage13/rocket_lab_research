# rklb-value Code Guide

`code/` contains the runnable Python models for two workstreams. It turns YAML
scenarios into typed JSON artifacts and text reports. The data-center model is
the first application; `communications` holds the communications model families
(the Iridium model first, with the High-Bandwidth Cellular Pure Play model as
the second family). The Iridium promotion command, run from `code/` (a relative
output path anchors to the repository root):
`uv run python -m communications.json_output scenarios/iridium.yaml
communications/models/iridium/default.json`.

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
uv run rklb-value scenarios/default.yaml --json | tee outputs/data_center/runs/default.json
uv run rklb-value --default --json | tee outputs/data_center/runs/default_from_flag.json
uv run rklb-value --input-schema | tee /tmp/rklb_input_schema.json
```

Scratch run outputs belong under `outputs/data_center/runs/`, which is ignored
by Git. The promoted public JSON lives outside the Python package under
`../data_center/models/`.

Output streams: stdout carries only the command's product (the report, the
headline, the JSON artifact, the schema). Status and errors are log lines on
stderr (`INFO: ...`, `ERROR: ...`), so pipe stdout alone when saving JSON, as
above. A successful run writes nothing to stderr. A scenario that cannot be
loaded (missing, malformed, or invalid, including a broken generations file it
names) is one `ERROR: could not load <scenario>: <reason>` line and exit
status 1, never a traceback; one the model cannot run is `ERROR: could not run
<scenario>: <reason>`. Usage errors exit with status 2: conflicting flags (a
config path with `--default`, `--brief` with `--json`, `--output-name`
without `--promote`, `--brief` or `--json` with `--promote`, `--input-schema`
with anything else), a malformed `--output-name`, and an output name that
misstates the scenario (see the promotion rules below).

The commands run from this source checkout only: the scenarios and the
promoted artifacts are repository files the installed wheel does not ship, so
a copy of the package installed elsewhere fails with a clear error instead of
reading or writing inside its virtual environment.

## Promote Public Artifacts

```sh
uv run rklb-value --promote 2>&1 | tee /tmp/rklb_promote.txt
```

Default promotion writes:

```text
../data_center/models/space/default.json
../data_center/models/ground/default.json
```

Promotion rules:

- The scenario is loaded first, so a mistyped path is reported as a missing
  file (exit status 1).
- The output name `default` belongs to `scenarios/default.yaml` alone. Any
  other scenario needs `--output-name <stem>`, and the default scenario is
  promoted only as `default`; a name that breaks either rule is a usage error
  (exit status 2). Stems are lowercase letters, digits, underscores, and
  hyphens only, because macOS file systems are usually case-insensitive and
  `DEFAULT.json` would be `default.json`. The artifact role
  (`promoted_default` or `promoted_named`) follows the scenario, never the
  name.
- Promotion refuses, and writes nothing, when any validation check fails: a
  `fail` in the space artifact's `meta.validation_results` (a critical or
  major rule, a model invariant, or a default guard) or in the ground
  reference's. The `ERROR:` line names the failing checks.
- Promotion also refuses, and writes nothing, when a destination is a
  symbolic link or exists as anything but a regular file, and, for the
  default promotion, when the anchor-year cohort is empty (no GPU package
  deployed in the anchor year, so the ground reference has no cohort to
  price): one `ERROR: could not promote ...` line naming the empty cohort.
- Both artifacts are built in memory first, then written as a pair with
  backup and rollback. Each is staged in full to a hidden temporary file
  beside its destination, the current files are kept as hidden backups, and
  the staged files are renamed into place one at a time. Each rename is
  atomic, but the pair is not: if the second rename fails (a locked file, for
  example), the first artifact is restored from its backup, and the `ERROR:`
  line says which files were restored and which, if any, still hold new
  content (with the backup path that keeps their previous content). A
  failure before any rename (a read-only directory, a full disk) changes
  neither file. Staged and backup files are created under fresh random
  names, and the writer never overwrites or removes a file it did not
  create. They are removed once the write completes or is rolled back,
  except a backup still needed to recover a destination; if the process is
  killed between the two renames, the hidden `.bak` files beside the
  artifacts hold the previous content.
- Status lines (`INFO: promoted <path>`) go to stderr; stdout stays empty.

Promotion does not rewrite `../data_center/conclusion.md`. That file is static
reviewed prose tied to the promoted defaults. If the default scenario changes,
promote the JSON, inspect the diffs, and update the static conclusion
deliberately.

Named space artifacts are supported for local comparison:

```sh
uv run rklb-value scenarios/conservative.yaml --promote --output-name conservative 2>&1 | tee /tmp/rklb_promote_conservative.txt
```

That writes `../data_center/models/space/conservative.json` with role
`promoted_named`. The ground reference is written only by the default
promotion. Named artifacts stay local: `.gitignore` tracks only the two
`default.json` files under `../data_center/models/`.

The Iridium promotion command (`python -m communications.json_output`) follows
the same conventions: one `ERROR:` line and exit status 1 on a bad scenario or
a failed write, exit status 2 on a usage error, and its status line on stderr.
It writes one artifact through the same writer, so its single atomic rename
leaves the existing artifact untouched when the write fails, and it refuses a
symbolic-link or non-regular destination the same way.

## Edit Scenarios

The public default scenario is `scenarios/default.yaml`. To experiment, copy it
to a new YAML file, edit the dials, and run the copy into the scratch directory:

```sh
cp scenarios/default.yaml scenarios/local_experiment.yaml
uv run rklb-value scenarios/local_experiment.yaml --json | tee outputs/data_center/runs/local_experiment.json
```

A scenario may name its own hardware roadmap with `generations: <path>`. A
relative path resolves beside the scenario file (its own directory), never
against the working directory, so a scenario runs the same from any
directory; an absolute path is used as-is. Omit `generations:` to use the
bundled generations.

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
uv run mypy --strict src 2>&1 | tee /tmp/rklb_mypy.txt
uv run pytest -q 2>&1 | tee /tmp/rklb_pytest.txt
```

The suite also runs from the repository root, which checks that no test
depends on the working directory:

```sh
uv run --project code pytest code/tests -q 2>&1 | tee /tmp/rklb_pytest_root.txt
```

The source packages under `src/` are strict-typed (`mypy --strict src`).
Tests use pytest fixtures and assert the public JSON contract, promotion
behavior, validation metadata, query examples, and the ground reference.

## Space JSON Contract

`uv run rklb-value <scenario> --json` emits a typed `SpaceModelOutput` with
five top-level keys:

| Key | Purpose |
|---|---|
| `metadata` | Scenario identity, schema version, horizon, artifact role, and generated timestamp. |
| `inputs` | Walkable config inputs plus `inputs.assumption_index` for source-traceable dials. |
| `physical` | Per-year node sizing, power, mass, volume, and per-node economics. |
| `business` | Per-year launches, deployed-year cohort, living fleet, revenue, full-cost profit (published under the `gross_profit_*` field names), margin, and cumulative revenue. |
| `meta` | Data dictionary, formula definitions, validation results (`meta.validation_results`, the complete verdict list), source-status summary, and query examples. |

Every public numeric leaf under `physical.years` and `business.years` is a
provenance cell with `value`, `unit`, `formula`, `formula_name`, `uses`,
`sources`, `source_status`, and `description`. Use `inputs.assumption_index`
when tracing a public claim back to a scenario dial or `RLDC-*` source ID.

## Ground JSON Contract

Default promotion also builds `../data_center/models/ground/default.json`. It
anchors to the promoted space model's anchor-year deployed-year cohort, not the
living fleet: the anchor year is the base year + 10 (the year-10 cadence
anchor), or the last window year for a shorter horizon, so FY2036 for the
default. Costs cover the comparison period, which is the anchor cohort's
service life (five years for the default). Key fields:

| Field | Purpose |
|---|---|
| `anchor` | Space-model year, deployed nodes, GPU packages, kW, service life, and source paths. |
| `inputs` | Ground assumption cells and their source status. |
| `ground` | Ground cost components and totals over the anchor cohort's service life. |
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
jq -r '.meta.query_examples[] | .name + " :: " + .jq_expression' ../data_center/models/space/default.json
```

Run direct checks against the promoted space model:

```sh
jq '.business.years."2036".kw_deployed_this_year.value' ../data_center/models/space/default.json
jq '.business.years."2036".kw_living_fleet.value' ../data_center/models/space/default.json
jq '.inputs.assumption_index["inputs.config.cadence.launches_at_year_10"]' ../data_center/models/space/default.json
jq '.meta.validation_results[] | select(.severity != "pass")' ../data_center/models/space/default.json
```

Run direct checks against the promoted ground reference:

```sh
jq '.anchor' ../data_center/models/ground/default.json
jq '.comparison.conclusion_label' ../data_center/models/ground/default.json
jq '.meta.validation_results[]? | select(.severity=="fail")' ../data_center/models/ground/default.json
```

## Validation Warnings

The complete space verdict list is `meta.validation_results`: the 16 V-rules,
the model invariants that hold for any scenario, and, for the canonical default
scenario only, the default guards (22 checks in the default artifact), each
with a `severity` of `pass`, `warn`, or `fail`. Read it first; the text report
and the embedded `validation_warnings` query read the same list.
`meta.validation.rules[]` mirrors the V-rules alone (`pass_check`). `--promote`
refuses any scenario with a `fail` in `meta.validation_results`.

Ground validation should preserve the deployed-year anchor and the parity
boundary. Warnings are acceptable when they describe scope limits, such as the
orbital reference mirroring build-and-launch cost only. A ground `fail` blocks
promotion until fixed.

## Package Layout

```text
code/
├── pyproject.toml
├── uv.lock
├── scenarios/
│   ├── default.yaml
│   ├── ground_default.yaml
│   ├── iridium.yaml
│   └── scenario variants
├── src/
│   ├── common/                shared by both applications
│   │   ├── cadence.py         the launch ramp, launch cost, and their dials
│   │   ├── cli.py             exit codes, logging, and error lines for both commands
│   │   ├── cohort.py          the service-life cohort cliff
│   │   ├── file_io.py         the YAML loader, artifact writer, and source checkout
│   │   ├── input_manifest.py  input-cell vocabulary and builders
│   │   ├── meta.py            validation and source-status types for meta blocks
│   │   └── provenance.py      provenance cells and the FORMULAS table
│   ├── communications/
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── engine.py
│   │   ├── ground.py
│   │   └── json_output.py     the Iridium artifact and its promotion command
│   └── data_center/
│       ├── cli.py             the rklb-value command
│       ├── config.py
│       ├── constants.py
│       ├── engine.py
│       ├── fleet.py
│       ├── generations.py
│       ├── ground.py
│       ├── input_manifest.py
│       ├── json_output.py
│       ├── output.py
│       ├── query_examples.py
│       ├── text_report.py
│       ├── validation.py
│       └── volume.py
├── tests/
│   ├── common/
│   ├── communications/
│   └── data_center/
└── outputs/data_center/runs/
```

Public artifacts live outside `code/` so scratch runs and reviewed defaults do
not blur together.
