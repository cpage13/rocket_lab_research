# Promotion

**Maturity.** Stable. Checked against `main` at 1570350, 2026-10-12; its
Iridium artifact's IoT blocks against part A's code (`iridium-v7`),
2026-10-13; the product case's command against part B's code, 2026-10-13.

**Role.** The publishing boundary: four commands run a scenario and write
the promoted JSON (the final objects, listed on the map) through one
rollback writer. The data-center command gates its pair of artifacts; the
saturation command computes the saturation curve; the Iridium command runs
the Iridium model on that curve; the product case's command runs the
product case on the Iridium artifact. This page also holds the query
recipes.

**Serves.** Objective 2 (the promoted JSON carries the provenance) and the
agent-first contract of ADR 002.

**Edges.**
- In: a scenario (the assumptions page), run through its model; for the
  Iridium command, also the promoted curve its scenario names; for the
  product case's command, the promoted Iridium artifact its scenario names,
  its bytes read once and hashed.
- Out: the four promoted files (the map, Final objects), read by the people
  who review the conclusions and by agents; the Iridium command also reads
  the curve back, and the product case's command reads the Iridium artifact.
  The product case's first promotion writes a fifth file. Scratch runs go to
  `code/outputs/data_center/runs/`, which git ignores.

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
- `uv run python -m product_case.json_output scenarios/product_case.yaml <output.json> --version-stamp <stamp>`
  writes the product case's artifact from the scenario and the Iridium
  artifact its `engineering_artifact_path` names. Its default output,
  communications/models/product_case/default.json, is written only from the
  shipped scenario; a side run writes to a path of its own, outside the
  tracked folders. It runs after the Iridium command, every time: the
  artifact records the SHA-256 of the Iridium bytes it read.
- For the communications commands and the product case's, a relative output
  path anchors to the repository root, and the stamp defaults to today's
  date, so a re-promotion with no model change still diffs: after a change,
  stamp today's date or a `git describe`. To reproduce the Iridium artifact
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

**The product case's command.** No gate of results either; it refuses, in
this order: a scenario it cannot read or that is invalid (a key that sets an
IoT count among the keys it refuses); the default output's path written from
any scenario but `code/scenarios/product_case.yaml` (naming both paths),
before the Iridium artifact is read; an Iridium artifact missing,
unreadable, not JSON or of another schema than `iridium-v7`, and the
engineering view's other refusals (a null coverage floor year, a reported
year absent or before the floor, a zero room); a usage the offers refuse; a
run in which no candidate is usable in any draw (`no_usable_choice`, naming
the test their draws fail most); a run that breaks an invariant or holds a
number that is not finite (naming it and the settings it scales with); and
the writer's refusals (a symbolic link or not a regular file, a failed
write). Each is one `ERROR:` line and exit status 1; a usage error exits 2.
A run that falls back to the most usable candidate, or whose central market
is unusable for the pick, is written and warned in `meta.validation_results`.

**The writer.** The two data-center artifacts are written as a pair with
backup and rollback (`common.file_io.write_files_with_rollback`); each
communications command, and the product case's, writes its one file through
the same writer. In `data_center/models/`, git tracks only the two default
files.

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
The product case's artifact carries its worked queries in
`meta.query_examples`, each tagged `product_case` in its `applies_to`; list
them as the space artifact's, once it is promoted.

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
- Product case, once promoted: its worked queries
  `headline_last_year_revenue_and_margin`, `classes_side_by_side_last_year`,
  `pick_and_basis`, `pick_usable_share`, `spreads_last_year` and
  `engineering_artifact_read`. Its four classes run side by side and are
  never added (people and devices never add), and the whole is read beside
  the Iridium artifact, never added to it (ADR 012).

**Terms.** promoted JSON, provenance cell, default scenario, saturation
curve, product case (see `CONTEXT.md`).

**State.** Each promoted file states its schema version (the map, Final
objects).

**Open.**
- Four commands: the communications and product-case promotions are module
  commands, not `rklb-value` flags, run in order (the curve, the Iridium
  artifact, then the product case), and no project-level runner covers them
  (`data_center/CURRENT_STATE.md` names the runner as future work).
- `code/CHANGELOG.md` has no entry yet for the curve's schema, the current
  Iridium schema or the product case's, and `code/README.md` lists neither
  the saturation command nor the product case's: both wait for the
  documents' rewrite (the conclusions page, Open).
- The product case is not yet promoted: its first promotion writes its
  artifact and adds its regeneration test (the committed artifact against a
  fresh promotion at its own stamp, naming both SHA-256s when the Iridium
  artifact moved).
- The communications artifacts' shortfall against ADR 002: the map, Open.

**Tests.** `code/tests/data_center/test_cli_promote.py` (roles, names,
refusals, the pair write, the conclusion left alone), `test_cli.py`,
`test_run_window.py`, `code/tests/communications/test_promotion_cli.py`,
`test_regenerated_default_artifact_matches_committed`, the saturation
command's tests in `code/tests/communications/test_saturation.py`
(`test_the_command_refuses_a_scenario_without_an_iridium_block`,
`test_a_destination_the_writer_would_refuse_is_refused_before_the_computation`,
`test_a_second_promotion_at_the_coarse_setting_is_byte_identical` and the
drift tests), the product case's command tests in
`code/tests/product_case/test_json_output.py`
(`test_each_refusal_is_one_error_line_exit_1_and_no_file`,
`test_the_file_refusals`,
`test_the_synthetic_case_promotes_and_a_second_promotion_is_byte_identical`),
`code/tests/data_center/test_committed_meta.py` (the committed data-center
data dictionaries and the space artifact's formula definitions against a
fresh build's), and `code/tests/common/test_file_io.py` (the loader and the
writer). Missed: no test compares the committed data-center artifacts whole
with a fresh promotion (`test_committed_meta.py` compares their data
dictionaries and the space artifact's formula definitions); the Iridium
suite compares its own, and the drift tests rebuild the committed curve's
check rows rather than run the saturation command in full; the product case
has no committed artifact to compare until its first promotion.

**If this changes, update here.** A command, flag, gate rule, writer
behavior, query recipe or headline query.

**Drill down.** `code/README.md` (commands, the space and ground JSON
contracts, validation warnings), `code/src/data_center/cli.py`,
`code/src/communications/saturation.py` (its docstring: the command and its
measured run), `code/src/communications/json_output.py`,
`code/src/product_case/json_output.py` (its docstring: the command and its
refusals), `code/src/common/file_io.py`, `code/src/common/cli.py`,
`docs/adr/001-static-conclusion-dynamic-models.md`,
`docs/adr/002-agent-first-json-contract.md`,
`docs/adr/004-remove-archive-and-old-model-alias.md`, `code/CHANGELOG.md`.
