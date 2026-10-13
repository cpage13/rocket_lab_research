# Promotion

**Maturity.** Stable. Checked against `main` at 1570350, 2026-10-12; its
Iridium artifact's IoT blocks against part A's code (`iridium-v7`),
2026-10-13.

**Role.** The publishing boundary: three commands run a scenario and write
the promoted JSON (the final objects, listed on the map) through one
rollback writer. The data-center command gates its pair of artifacts; the
saturation command computes the saturation curve; the Iridium command runs
the Iridium model on that curve. This page also holds the query recipes.

**Serves.** Objective 2 (the promoted JSON carries the provenance) and the
agent-first contract of ADR 002.

**Edges.**
- In: a scenario (the assumptions page), run through its model; for the
  Iridium command, also the promoted curve its scenario names.
- Out: the four promoted files (the map, Final objects), read by the people
  who review the conclusions and by agents; the Iridium command also reads
  the curve back. Scratch runs go to `code/outputs/data_center/runs/`, which
  git ignores.

**Commands** (from `code/`; `code/README.md` lists the data-center commands
and the Iridium command, and the saturation command's module docstring
gives its own):
- `uv run rklb-value --promote 2>&1 | tee /tmp/rklb_promote.txt` writes the
  default space and ground artifacts.
- `uv run rklb-value scenarios/conservative.yaml --promote --output-name conservative`
  writes a named space artifact (local only, no ground artifact).
- `uv run python -m communications.saturation scenarios/iridium.yaml communications/models/iridium/saturation_curve.json --version-stamp <stamp>`
  writes the saturation curve. It is a heavy run (the charter's Project
  rules), and it reads no curve, so a stale curve never blocks it. It runs first whenever an
  input of the curve moves (the assumptions page's Iridium checklist).
- `uv run python -m communications.json_output scenarios/iridium.yaml communications/models/iridium/default.json --version-stamp <stamp>`
  writes the Iridium artifact from the scenario and the curve its
  `iridium.saturation.curve_path` names.
- For both communications commands a relative output path anchors to the
  repository root, and the stamp defaults to today's date, so a
  re-promotion with no model change still diffs: after a change, stamp
  today's date or a `git describe`. To reproduce the Iridium artifact
  unchanged, pass its own `provenance.version_stamp`, as the regeneration
  test does; a curve re-promoted with its own `version_stamp` differs from
  the committed one only in its `provenance.run_measurement` (the wall time
  and memory of that run).
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

**The communications commands.** No reserved name and no gate of results;
this is the one list of their refusals. Each loads its scenario and refuses
one it cannot read, an invalid one or one without an `iridium:` block
before anything else runs, and each refuses a destination the writer would
refuse (a symbolic link or not a regular file) and a failed write. The
saturation command checks its destination before it computes, refuses a
population grid whose digest is not the expected one, a failed check and a
failed sweep (a worker out of memory, say), and writes only a curve that
passes its completeness check. The Iridium command refuses a curve it
cannot read, one of another schema, an altered or incomplete curve, a curve
computed for other inputs (the identity check), a fleet past a class's last
computed row, a run whose final year's living fleet passes the fleet a
class with no saturation number is not reached by (ADR 005: the curve does
not measure the elasticity there, so which limit binds is not known), a
value the model cannot compute and a run holding a number that is not
finite. Each refusal is one `ERROR:` line and exit status 1. No ignore rule
keeps a communications artifact local, so a trial run never targets a
committed path except with that file's own stamp, to reproduce it.

**The writer.** The two data-center artifacts are written as a pair with
backup and rollback (`common.file_io.write_files_with_rollback`); each
communications command writes its one file through the same writer. In
`data_center/models/`, git tracks only the two default files.

**Querying** (from the root). List the worked examples:
`jq -r '.meta.query_examples[] | .name + " :: " + .jq_expression' data_center/models/space/default.json`;
the ground artifact carries its own (`ground_anchor`, `ground_assumptions`,
`ground_cost_summary`, `ground_space_ratio`). Year keys are strings
(`.business.years."2036"`). Trace a dial through the space artifact's flat
input map: `jq '.inputs.assumption_index["inputs.config.cadence.launches_at_year_10"]' data_center/models/space/default.json`.
A ground `uses` path prefixed `space:` points into the space artifact. The
Iridium artifact carries no worked queries; read it by block, for example
`jq '.classes[] | {device_class, saturation_number, saturation_not_reached_by, binding_limit_at_horizon_end}' communications/models/iridium/default.json`,
or the final year's IoT capacities,
`jq '.years[-1].iot.classes[] | {iot_class, device_capacity, binding_view}' communications/models/iridium/default.json`.

**The headline reads.**
- Data center: the space artifact's worked queries
  `headline_2036_revenue_central`, `headline_2036_profit_central` and
  `margin_band_2036`; their questions and the profit field still say gross
  until the rename goal lands, so say profit and margin.
- The ground verdict, `comparison.conclusion_label`, and the orbit-to-ground
  cost ratio, `comparison.orbit_to_ground_ratio`, in
  `data_center/models/ground/default.json`; its worked query
  `ground_space_ratio` reads the inverse, ground over orbit.
- Communications: `communications/models/iridium/default.json` is long, so
  read it by block: each people class's markers and binding limit
  (`classes`); each IoT class's engineering usage (`iot_classes`); each
  year's fleet and cost, each class's useful beams, people, revenue and own
  margin, and IoT's room with each IoT class's capacity (`years`); the
  readings, each with IoT's room (`saturation.readings`); the stated
  assumptions (`assumptions`). Each class's column is the whole fleet sold
  to that class alone, so the columns are never summed into a fleet revenue
  (ADR 006; the map's invariants); each IoT class's capacity is the whole
  room given to that class alone, never a count sold, and the two are never
  added (ADR 011).

**Terms.** promoted JSON, provenance cell, default scenario, saturation
curve (see `CONTEXT.md`).

**State.** Each promoted file states its schema version (the map, Final
objects).

**Open.**
- Three commands: the communications promotions are module commands, not
  `rklb-value` flags, run in order (the curve, then the Iridium artifact),
  and no project-level runner covers them (`data_center/CURRENT_STATE.md`
  names the runner as future work).
- `code/CHANGELOG.md` has no entry yet for the curve's schema or the
  current Iridium schema, and `code/README.md` does not list the saturation
  command: both wait for the documents' rewrite (the conclusions page,
  Open).
- The communications artifacts' shortfall against ADR 002: the map, Open.

**Tests.** `code/tests/data_center/test_cli_promote.py` (roles, names,
refusals, the pair write, the conclusion left alone), `test_cli.py`,
`test_run_window.py`, `code/tests/communications/test_promotion_cli.py`,
`test_regenerated_default_artifact_matches_committed`, the saturation
command's tests in `code/tests/communications/test_saturation.py`
(`test_the_command_refuses_a_scenario_without_an_iridium_block`,
`test_a_destination_the_writer_would_refuse_is_refused_before_the_computation`,
`test_a_second_promotion_at_the_coarse_setting_is_byte_identical` and the
drift tests), and `code/tests/common/test_file_io.py` (the loader and the
writer). Missed: no test compares the committed data-center artifacts with
a fresh promotion; the Iridium suite compares its own, and the drift tests
rebuild the committed curve's check rows rather than run the saturation
command in full.

**If this changes, update here.** A command, flag, gate rule, writer
behavior, query recipe or headline query.

**Drill down.** `code/README.md` (commands, the space and ground JSON
contracts, validation warnings), `code/src/data_center/cli.py`,
`code/src/communications/saturation.py` (its docstring: the command and its
measured run), `code/src/communications/json_output.py`,
`code/src/common/file_io.py`, `code/src/common/cli.py`,
`docs/adr/001-static-conclusion-dynamic-models.md`,
`docs/adr/002-agent-first-json-contract.md`,
`docs/adr/004-remove-archive-and-old-model-alias.md`, `code/CHANGELOG.md`.
