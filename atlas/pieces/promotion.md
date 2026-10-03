# Promotion

**Maturity.** Stable. Checked against `main` at 7ff8bc3, 2026-10-03.

**Role.** The publishing boundary: two commands run a scenario, gate it and
write the promoted JSON (the final objects, listed on the map) through one
rollback writer. This page also holds the query recipes.

**Serves.** Objective 2 (the promoted JSON carries the provenance) and the
agent-first contract of ADR 002.

**Edges.**
- In: a scenario (the assumptions page), run through its model.
- Out: the three promoted files (the map, Final objects), read by the
  people who review the conclusions and by agents. Scratch runs go to
  `code/outputs/data_center/runs/`, which git ignores.

**Commands** (from `code/`; `code/README.md` has the full list):
- `uv run rklb-value --promote 2>&1 | tee /tmp/rklb_promote.txt` writes the
  default space and ground artifacts.
- `uv run rklb-value scenarios/conservative.yaml --promote --output-name conservative`
  writes a named space artifact (local only, no ground artifact).
- `uv run python -m communications.json_output scenarios/iridium.yaml communications/models/iridium/default.json --version-stamp <stamp>`
  writes the Iridium artifact; a relative output path anchors to the
  repository root. The stamp defaults to today's date, so a re-promotion
  with no model change still diffs: after a change, stamp today's date or a
  `git describe`; to reproduce the committed file unchanged, pass its own
  `provenance.version_stamp`, as the regeneration test does.
- `uv run rklb-value scenarios/default.yaml --json | tee outputs/data_center/runs/default.json`
  is a scratch run; pipe stdout alone, since status goes to stderr.

**The data-center gate.** `rklb-value --promote` refuses, and writes
nothing, on any `fail` in either artifact's `meta.validation_results`: the
V-rules, the model invariants and, for the default scenario only, the
default guards (the data-center page, `validation.py`). It also refuses a
destination that is a symbolic link or not a regular file and, in the
default promotion, an empty anchor-year cohort. The name `default` belongs
to `scenarios/default.yaml`; any other scenario needs a lowercase
`--output-name`; the artifact role (`promoted_default` or
`promoted_named`) follows the scenario, never the name.

**The Iridium command.** No reserved name and no gate beyond the config's
own validators. It refuses a scenario that does not select the Iridium
model, a symbolic-link or non-regular destination, and a failed write;
otherwise it writes the scenario to the path it is given. No ignore rule
keeps a named Iridium artifact local, so a companion run must never target
`communications/models/iridium/default.json`.

**The writer.** The two data-center artifacts are written as a pair with
backup and rollback (`common.file_io.write_files_with_rollback`); the
Iridium command writes its one file through the same writer. In
`data_center/models/`, git tracks only the two default files.

**Querying** (from the root). List the worked examples:
`jq -r '.meta.query_examples[] | .name + " :: " + .jq_expression' data_center/models/space/default.json`;
the ground artifact carries its own (`ground_anchor`, `ground_assumptions`,
`ground_cost_summary`, `ground_space_ratio`). Year keys are strings
(`.business.years."2036"`). Trace a dial through the space artifact's flat
input map: `jq '.inputs.assumption_index["inputs.config.cadence.launches_at_year_10"]' data_center/models/space/default.json`.
A ground `uses` path prefixed `space:` points into the space artifact.

**The headline reads.**
- Data center: the space artifact's worked queries
  `headline_2036_revenue_central`, `headline_2036_profit_central` and
  `margin_band_2036`; their questions and the profit field still say gross
  until the rename goal lands, so say profit and margin.
- The ground verdict, `comparison.conclusion_label`, and the orbit-to-ground
  cost ratio, `comparison.orbit_to_ground_ratio`, in
  `data_center/models/ground/default.json`; its worked query
  `ground_space_ratio` reads the inverse, ground over orbit.
- Communications: `communications/models/iridium/default.json`, small
  enough to read whole.

**Terms.** promoted JSON, provenance cell, default scenario (see
`CONTEXT.md`).

**State.** Each promoted file states its schema version, and
`code/CHANGELOG.md` records each version.

**Open.**
- Two commands: the Iridium promotion is a module command, not an
  `rklb-value` flag, and no project-level runner covers both models
  (`data_center/CURRENT_STATE.md` names the runner as future work).
- The Iridium artifact's shortfall against ADR 002: the map, Open.

**Tests.** `code/tests/data_center/test_cli_promote.py` (roles, names,
refusals, the pair write, the conclusion left alone), `test_cli.py`,
`test_run_window.py`, `code/tests/communications/test_promotion_cli.py`,
`test_regenerated_default_artifact_matches_committed`, and
`code/tests/common/test_file_io.py` (the loader and the writer). Missed: no
test compares the committed data-center artifacts with a fresh promotion;
the Iridium suite does compare its own.

**If this changes, update here.** A command, flag, gate rule, writer
behavior, query recipe or headline query.

**Drill down.** `code/README.md` (commands, the space and ground JSON
contracts, validation warnings), `code/src/data_center/cli.py`,
`code/src/communications/json_output.py`, `code/src/common/file_io.py`,
`code/src/common/cli.py`, `docs/adr/001-static-conclusion-dynamic-models.md`,
`docs/adr/002-agent-first-json-contract.md`,
`docs/adr/004-remove-archive-and-old-model-alias.md`, `code/CHANGELOG.md`.
