# Assumptions

**Maturity.** Stable. Checked against `main` at 3381e25, 2026-10-12.

**Role.** Where every assumption lives, in three forms. The machine form:
the scenario files in `code/scenarios/` and the defaults behind them in
code (each model's `constants.py` and `config.py`,
`code/src/common/cadence.py`, and the data-center `generations.py` and
`ground.py`). The human form:
the assumptions ledgers, `data_center/assumptions.md` and
`communications/assumptions.md` (their shapes under The ledgers), with the
stated rows that set no dial. And, for communications, the
stated-assumption lines its artifact publishes, written by `_assumptions`
in `code/src/communications/iridium.py`: part dial values, part text
written for the shipped settings.
This is where the investor's "state assumptions instead of knobs" lives.

**Serves.** Objective 3 (simple models with stated assumptions) and
objective 2 (each input traces to a claim ID or says investor-set).

**Edges.**
- In: claim IDs, statuses and research paths from the source ledger; values
  the investor sets.
- Out: the dials, read by the model loaders (the map's edge table); the
  ledger rows the conclusions cite. In the data center, the input spec
  tables (`CADENCE_SPECS`, `PHYSICAL_SPECS` and the rest in
  `code/src/data_center/input_manifest.py`; for the ground,
  `GROUND_INPUT_SPECS` in `code/src/data_center/ground.py`) carry every
  input's claim, status and rationale into the promoted JSON.

**The scenarios.**

| File | Role |
|---|---|
| `default.yaml` | the data-center default, promoted as `default` |
| `ground_default.yaml` | the ground reference's inputs, promoted with the default; its defaults also live in `ground.py` |
| `generations.yaml` | the committed copy of the code's bundled GPU roadmap (`KNOWN_GENS`); a scenario that omits `generations:` uses the bundled list |
| `with_premium.yaml`, `upside_7yr.yaml` | rebased sensitivities: the default plus their stated changes |
| `ambitious.yaml`, `conservative.yaml` | older sensitivities, not rebased: they still fly the co-mounted radiator and the pre-rebase cost dials |
| `ai1_equivalent.yaml` | AI-1's specs on the model's dials; it fails the `pf_per_kw_in_band` rule by design, so it cannot be promoted |
| `volume_stress.yaml` | a fixture on the co-mounted radiator that trips validation rule V15; quote nothing from it |
| `iridium.yaml` | the Iridium default, promoted as `communications/models/iridium/default.json`; the saturation command reads its held spectrum |

**The ledgers.**
- `data_center/assumptions.md`: a table of claim ID, assumption, source
  status, role, source or path, and notes, with one row per release-critical
  default or public claim (model inputs, outputs, sensitivities, brackets, a
  sanity check); a row may cover several dials, and many dials have no row,
  since the input spec tables and the artifact's `inputs.assumption_index`
  hold every input's claim, status and rationale. Stated rows carry the role
  "Contextual assumption, not a model input" (the launch site,
  `RLDC-LAUNCH-SITE`). Then the public output anchors, the ground and the
  premium and sensitivity boundaries, and the maintenance rule.
- `communications/assumptions.md`: a row per dial (the sourced and derived
  dials), then the assumptions register (investor-set values, the published
  ARPU sheet, why the cadence share is all-in, and the conventions and
  modeling posture, whose rows state what the model leaves out), the output
  anchors, and the maintenance rule, which does not name the artifact's
  stated lines. Its rows still describe the model before the saturation work
  (the four-bucket price sheet, a 25 m^2 panel, uniform-demand geography)
  until its rewrite (the conclusions page, Open).

**Source classes.** Each default in a `constants.py` opens its docstring
with a source class that says how its value was set: in the data center
`SOURCED_FACT`, `SOURCED`, `ESTIMATE`, `EXTRAPOLATION`, `SOURCED_DECISION`
or `INVESTOR_SET`; in communications `SOURCED_FACT`, `SOURCED_ESTIMATE`,
`ESTIMATE`, `SCENARIO`, `INVESTOR_SET` or `DERIVED`, and some carry none.
The cadence defaults (the `*_DEFAULT` constants in
`code/src/common/cadence.py`) carry `ESTIMATE`; the ground defaults in
`ground.py` carry none. A claim's home is
not the docstring: in the data center every input's claim is set in
`input_manifest.py` (its `*_SPECS` tables, and for the GPU roadmap and the R
band its builders and claim constants; for the ground, `GROUND_INPUT_SPECS`
and the `GROUND_*_CLAIM_ID` constants in `ground.py`),
and in communications in the dial's ledger row. A docstring may cite the
claim too; a decision-sourced default cites its decision (such as D7) or a
design rule; unit conversions cite nothing. These classes are not the
public source-status taxonomy (`CONTEXT.md`, Ambiguities).

**Changing a dial**, in the ledgers' own order (their maintenance rule).

*Data center.*
1. Update the dial's row in `data_center/assumptions.md` if it has one (a
   dial that becomes a public claim gets one), and `research/SOURCE_INDEX.md`
   if the claim trail changes.
2. Change the default in every home it has, together:
   - a model dial: its constant in `code/src/data_center/constants.py` (for
     cadence and launch cost, `code/src/common/cadence.py`; for the base
     year, horizon and radiator architecture, `MetadataConfig` and
     `_default_metadata` in `code/src/data_center/config.py`) and
     `code/scenarios/default.yaml`,
     mirrored into `code/scenarios/with_premium.yaml` and
     `code/scenarios/upside_7yr.yaml`;
   - the GPU roadmap: `KNOWN_GENS` in `code/src/data_center/generations.py`
     and `code/scenarios/generations.yaml`
     (`test_bundled_generations_yaml_matches_known_gens` ties them);
   - a ground input: its `DEFAULT_*` constant in
     `code/src/data_center/ground.py` and `code/scenarios/ground_default.yaml`.
     Its claim and rationale sit in `GROUND_INPUT_SPECS` in the same file, and
     most ground claim IDs spell their value (such as `RLDC-GROUND-PUE-1_25`),
     so a moved value changes its source-ledger row too (step 1). No test ties
     the two homes as a set (the data-center page, Open), so after promotion
     check from the root that no ground input is a scenario override:
     `jq '[.inputs.assumption_index[] | select(.assumption_role == "scenario_override")] | length' data_center/models/ground/default.json`
     must print 0.

   Update the claim and rationale in the input spec tables when the basis
   changes. A cadence default also moves the Iridium run, whose scenario
   inherits the cadence, and any shared default moves the communications
   tests on config defaults: follow the Iridium steps 4 and 5 too.
3. Check the default guards (the data-center page, `validation.py`):
   promotion refuses while one fails; move a guard only on purpose, and
   rename a check ID that names the old value.
4. Re-record the golden trajectory (`code/tests/data_center/test_parity.py`)
   and the ground invariant (`code/tests/data_center/test_ground_reference.py`)
   deliberately, with the reason; update every test that pins the moved
   default (`test_default_config_matches_plan_section_zero_anchors`, the
   defaults in `test_config.py`, the rationale text `test_input_manifest.py`
   checks); run the test command (charter, Project rules).
5. Re-promote: `uv run rklb-value --promote` from `code/` (the promotion page).
6. Review every document that quotes a moved number (the list on the
   conclusions page); a `git grep` for the old values is the quick check.

*Iridium.*
1. Update the dial's row in `communications/assumptions.md` (its rewrite
   pending, the conclusions page, Open), and the source ledger if the claim
   trail changes.
2. Change the value in its home, together with its mirrors: a scenario
   setting in `code/scenarios/iridium.yaml` (the shared cadence and cost
   dials, `satellite.*`, and the `iridium` block: the held spectrum, the
   panel, the downlink share, the five prices); a named constant in
   `code/src/communications/constants.py` (each class's usage and spectral
   efficiency, the shell, the demand threshold, the IoT lines' counts), with
   its description in `code/src/communications/config.py` where a config
   field defaults to it. A changed config default can also move the
   cellular family and the equality tripwire.
3. If the change moves an input of the saturation curve, re-promote the
   curve first: its inputs are the held spectrum and every named constant
   `SaturationInputs` reads in `code/src/communications/saturation_curve.py`
   (each class's central spectral efficiency, rate while active and
   busy-hour share, its directivity and sky sectors; the link anchor and the
   pattern floor; the shell and the beam; the demand map; the sweep; the
   trim; the band points). Until then the Iridium command refuses the
   committed curve (the identity check). The saturation command is a heavy
   run (the charter's Project rules); re-freeze on purpose the saturation
   suite's values the moved input changes. The panel, the downlink share,
   the prices, the off-peak shares, the IoT lines, satellites per launch,
   the cadence and the costs run on the promoted curve as it stands.
4. Re-promote the Iridium artifact with the Iridium command (the promotion
   page, with today's stamp), re-freeze the Iridium suite's numbers on
   purpose, then run the test command: the regeneration test fails until
   re-promotion.
5. Read the artifact's stated-assumption lines (`_assumptions` in
   `code/src/communications/iridium.py`) for text the moved value leaves
   stale, and review every document that quotes a moved number (the
   conclusions page).

**Rules.**
- Unmodeled factors, assumed upgrades and haircuts follow the charter's
  Quality bar. A stated factor is a ledger row with the contextual role (data
  center) or a row in the register's modeling-posture table (communications).
- The Neutron block upgrade sets a scenario value in both applications:
  the data center's mass envelope (`RLDC-PAYLOAD-SSO-UPGRADE`) and the
  Iridium scenario's 16 satellites per launch (`COMM-713`; 15 without it,
  `COMM-712`), stated in the Iridium artifact.
- A data-center scenario value that differs from the default publishes as a
  scenario override (the map's invariants).

**Terms.** assumptions ledger, investor-set, default scenario, source
status, claim ID (see `CONTEXT.md`).

**State.** A default scenario and its ledger are kept in agreement by
review alone; nothing checks it automatically (Tests, below).

**Open.**
- Three factors the charter names are not yet stated in the data-center
  ledger: GPU failures, facility accounting, future ground stations
  (communications states its no-failure posture). Writing them in is a
  ledger edit for the investor.
- `ambitious.yaml` and `conservative.yaml` were never rebased. On the
  rebased dials (the radiator and the solar and radiator cost)
  `ambitious.yaml` is less favourable than the default, despite its name;
  its nominally favourable cost dials are the investor's open decision D5
  (`.agent/lifecycle/review_fixes_session_state_09_24.md` (local)).
- The Iridium artifact's stated-assumption lines carry text written for the
  shipped settings (dates, claims, the investor's words) beside the values
  they read, so a dial change is followed by a read of them (the Iridium
  checklist, step 5).

**Tests.** `test_code_defaults_equal_the_default_scenario_file`
(`code/tests/data_center/test_parity.py`), `test_scenario_drift.py`,
`test_iridium_yaml_scenario_loads_and_runs` (`test_iridium_model.py`),
`test_the_iridium_entry_runs_only_on_a_curve_computed_for_its_inputs` (the
Iridium dials and constants against the curve's parameters),
`test_committed_curve_has_not_drifted` (the curve against the code),
`test_bundled_generations_yaml_matches_known_gens`,
`test_input_manifest.py` (statuses match the ledger; overrides drop the
default's claim), and `test_validation_results.py` (each shipped scenario's
expected failures). Missed: no test compares a ledger's rows with its
scenario file; none ties the ground constants to their scenario file as a
set (the data-center page, Open); no test reads every stated line at
every setting; and a new data-center scenario
is tested only once it joins the hand-kept lists `_EXPECTED_FAILURES`
(`test_validation_results.py`) and `_SCENARIO_NAMES`
(`test_provenance_uses.py`).

**If this changes, update here.** A scenario added, retired or rebased (a
new data-center scenario also joins those two lists); a ledger section; a
source class; a stated-assumption line; an input of the saturation curve.

**Drill down.** The two ledgers; `code/scenarios/`;
`code/src/data_center/constants.py`, `code/src/data_center/ground.py`,
`code/src/communications/constants.py`, `code/src/common/cadence.py`; the
`*_SPECS` tables in `code/src/data_center/input_manifest.py` and
`GROUND_INPUT_SPECS` in `code/src/data_center/ground.py`; `_assumptions`
in `code/src/communications/iridium.py` and `SaturationInputs` in
`code/src/communications/saturation_curve.py`.
