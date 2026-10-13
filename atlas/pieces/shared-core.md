# Shared core

**Maturity.** Stable. Checked against `main` at 1570350, 2026-10-12.

**Role.** The code both models import (`code/src/common/`), one
implementation per helper:

| Module | Owns |
|---|---|
| `cadence.py` | the cadence spine: the logistic whole-fleet launch ramp, the cadence-indexed launch cost, their dial blocks (`CadenceDials`, `LaunchCostDials`) and defaults, `WholeNumber` (a whole-number field that refuses a YAML boolean or a quoted number at load: the cadence's whole-number dials, and the communications metadata's and satellite block's) and `round_half_up` |
| `cohort.py` | the service-life cohort cliff (`LivedCohort`, `cohort_is_alive_at`, `living_cohorts`) |
| `provenance.py` | `ProvenanceCell`, the `FORMULAS` catalog, the `cell` factory, the strict readers `as_float` and `as_int` |
| `input_manifest.py` | the input-cell vocabulary (`InputCell`, `SourceStatus`, `AssumptionRole`) and the default-versus-override rule |
| `meta.py` | the meta-block types: validation checks and results, data dictionary, query examples, formula definitions |
| `file_io.py` | the file boundary: `load_yaml_mapping`, `render_artifact_json`, `artifact_write` and its `PendingWrite`, `write_files_with_rollback`, `locate_source_checkout` and its `SourceCheckout`, whose `anchored` method anchors a relative path at the repository root (the rule both communications commands anchor the curve, the grid and their outputs by; a scenario path resolves against the working directory), `ModelFileError` |
| `cli.py` | the command conventions: product on stdout, status on stderr, exit status 1 for an expected failure and 2 for a usage error, followed by all three promotion commands |

**Serves.** Keeps both applications on one spine (the same launch ramp,
rounding and publishing rules), so they compare like for like; supports
objective 2 through the provenance cells and source statuses.

**Edges.**
- In: dial values from each model's config (the cadence and launch-cost
  blocks are fields of both configs).
- Out: `data_center` uses every module. `communications` uses the cadence
  spine, the cohort cliff, the file boundary and the command conventions
  (its saturation and Iridium commands both write through the one writer),
  `SourceStatus` and the strict readers, not the provenance cells or the
  meta types (its artifacts are plain).
- numpy enters no `common` module: it stays inside
  `communications.saturation` (ADR 010; the communications page).
- `common` imports neither model; callers import by submodule path
  (`from common.provenance import ...`), and the package `__init__`
  re-exports nothing.

**Terms.** cadence spine, deployed-year cohort versus living fleet (the
cohort cliff), provenance cell, source status (see `CONTEXT.md`).

**State.** The launch ramp is fitted through the year-5 and year-10 anchors
under a ceiling. The anchors are scenario values (`NTR-010`), not Rocket Lab
guidance; launch cost is the cadence-indexed internal estimate (`NTR-009`).
The ceiling is a parameter of the ten-year window, not a cap on the system
(the charter's rule on caps): a longer horizon must re-set it.

**Open.** A low-priority follow-up from the 09-24 review: the `FORMULAS`
catalog still names the living-fleet formulas
`kw_on_orbit_from_living_fleet` and `pf_on_orbit_from_living_fleet`, though
schema v8 dropped the `kw_on_orbit` and `pf_on_orbit` fields for
`kw_living_fleet` and `pf_living_fleet`
(`.agent/lifecycle/review_fixes_session_state_09_24.md` (local)).

**Tests.** `code/tests/common/`: `test_cadence_move.py` (both configs hold
these very classes, and the shared blocks refuse a YAML boolean or a quoted
number in both models), `test_cohort.py`, `test_file_io.py` (the loader,
the writer and its rollback, the anchoring), `test_input_manifest_move.py`,
`test_meta_move.py`, `test_provenance_move.py`, and
`test_no_venture_imports.py` (the import guard). End to end, both models'
frozen baselines exercise the spine. Missed: nothing specific to this
piece; the suite-wide gaps are on the map.

**If this changes, update here.** A shared default (a cadence default
moves both applications; a launch-cost default moves every run that does
not override it, and the Iridium scenario overrides it: follow the
assumptions page's checklists); a module added; the command convention.

**Drill down.** The `code/src/common/__init__.py` docstring and each
module's docstring; `code/README.md` (output streams and exit codes).
