# Data-center model

**Maturity.** Stable: a frozen golden trajectory locks the default run.
Checked against `main` at 3381e25, 2026-10-12.

**Role.** Models a Neutron-launched orbital AI-inference data center, year
by year. Each fiscal year it picks the frontier GPU package generation, fits
as many packages as the Neutron mass envelope allows, prices the node
(compute, bus, solar, radiator, launch at the year's cadence), spreads the
node's full cost over its service life, prices revenue as that annual cost
times the revenue multiple R, and rolls the year's cohort into the living
fleet. The ground reference model prices an equivalent ground cohort for the
anchor year's deployed cohort over its service life and reports the
orbit-to-ground ratio.

**Serves.** Objective 1 (the all-in question for the data center, at the
full modeled cadence) and objective 2 (provenance cells on the outputs, an
assumption-index entry for every input).

**Edges.**
- In: `code/scenarios/default.yaml` (blocks `metadata`, `cadence`, `fleet`,
  `volume`, `r_band`, `launch_cost`, `gospel`, `slopes`, optional
  `generations`) and `code/scenarios/ground_default.yaml` (the assumptions
  page); the defaults in `constants.py`, each with a source class; the
  cadence spine, cohort cliff and cell types from `code/src/common/`.
- Out: the space artifact (`SpaceModelOutput`, defined in `output.py`) and
  the ground artifact (`GroundReferenceOutput`, in `ground.py`), published
  by promotion; a text report and a one-line `--brief` headline.

**Modules** (`code/src/data_center/`; the per-node formulas are in the
`engine.py` module docstring). The deep modules are the config boundary,
the engine, the input manifest, the output contract and the ground
reference: callers never recreate their internal logic.

| Module | Owns |
|---|---|
| `config.py` | the typed scenario boundary (`ValuationConfig`, `load_config`, `anchor_year`) |
| `engine.py` | the run: `run_valuation`, the per-node math, the cadence year |
| `generations.py` | the GPU roadmap: `KNOWN_GENS`, extrapolation, `frontier_at` |
| `fleet.py` | cohorts, R interpolation, the living-fleet rollup |
| `volume.py` | stowed volume against the fairing (reported; mass alone sets the package count) |
| `input_manifest.py` | the input tree, the `*_SPECS` claim tables, the flat `inputs.assumption_index` |
| `output.py` | the artifact schema and its `SCHEMA_VERSION` |
| `json_output.py` | artifact assembly and the generated data dictionary |
| `validation.py` | `meta.validation_results`: the V-rules, the model invariants and, for the default only, three default guards: the anchor-year capacity band (a fixed range, so a moved default can fail it), and the central R and the service life (each compared with its code default, so it moves with the default, though its check ID spells the value) |
| `query_examples.py` | the worked `jq` examples, addressed to the anchor year |
| `ground.py` | the ground reference: anchor, inputs and their claim table `GROUND_INPUT_SPECS`, costs, comparison |
| `text_report.py`, `cli.py`, `constants.py` | the human report, the `rklb-value` command, the defaults (to change one, the assumptions page's checklist) |

**Terms.** space model, ground reference model, node, deployed-year cohort
versus living fleet, revenue multiple (R), margin (see `CONTEXT.md`).

**State.**
- Revenue is coupled to cost: R sets the margin in every year (read
  `margin_central_pct` in the artifact); the low, central and high R bands
  are trajectories with year anchors, linear between them.
- The default flies the deployed double-sided radiator
  (`metadata.radiator_architecture: deployed_double_sided`). The co-mounted
  posture (0.012 to 0.013 t/kW) survives as the labeled conservative
  exception in the public documents and as live dials in the older
  sensitivities and the volume fixture (the assumptions page).
- The mass envelope is a block-upgrade scenario value
  (`gospel.mass_envelope_t`, claim `RLDC-PAYLOAD-SSO-UPGRADE`, supported by
  `NTR-007`).
- The headline values live in the artifact; the promotion page's headline
  reads name the queries.

**Invariants.** On the map: the ground anchor (ADR 003), whole counts,
deployed-year versus living capacity, code defaults equal to the default
scenario, and revenue coupled to cost, each with its guard.

**Open.**
- The `gross_profit_*` rename is a charter goal (approved, not executed);
  the word conflict is in `CONTEXT.md`.
- No test ties the ground's `DEFAULT_*` constants in `ground.py` to
  `code/scenarios/ground_default.yaml`, and none checks that the default
  ground artifact publishes no scenario override; the space side has both
  (`test_code_defaults_equal_the_default_scenario_file`,
  `test_default_scenario_publishes_no_override_and_no_calendar_labels`). A
  ground value changed in one home only publishes as an override, its claim
  dropped. For the facility fit-out and the energy price, the status counts
  `test_ground_reference_contract_is_complete` asserts then fail; for the
  other six inputs nothing catches it (the ground invariant is re-recorded
  with each deliberate change, and a change to the code constant alone does
  not move it). The guard is a test change for the investor.
- Undecided: a radiator floor for the deployed architecture in rule V17
  (decision D7 in `.agent/lifecycle/review_fixes_session_state_09_24.md` (local)).
- The mass envelope sits above Neutron's published SSO curve by more than
  the block-upgrade band the research assumes, per the Flatellite
  experiment's research B, confirmed by its validation D
  (`.agent/other/flatellite_dimensions_09_29/RESEARCH_TRACKER.md` (local));
  the investor has not yet taken it up as a data-center item.
- The load-bearing uncertainties: launch cost, the payload upgrade, solar and
  radiator cost, the GPU generation extrapolation. Ground refinements
  (facility, energy, cooling, operations, utilization, package cost) may
  still move the ground reference.
- The ground-to-orbit link architecture is undecided
  (`data_center/CURRENT_STATE.md`).
- Low-priority follow-ups from the 09-24 review: per-field citations for the
  GPU generation inputs; the emitted "Since v8" schema note
  (`code/src/data_center/json_output.py`); an absurd release-cadence input.

**Tests.** `code/tests/data_center/`. The end-to-end specification is
`test_parity.py`: `run_valuation` on `default.yaml` against a recorded
golden trajectory, re-recorded only on purpose by editing its reference
values, with the reason; the ground's is
`test_default_ground_reproduces_the_recorded_invariant`
(`test_ground_reference.py`). Around them: the engine, fleet, generations,
volume, config, constants, cadence, naming, validation, output,
query-example, text-report, run-window, command and promotion suites, and
`test_input_manifest.py` and `test_provenance_uses.py`. Missed: the ground
defaults' guard (Open), the committed artifacts (the promotion page) and
the conclusion's numbers (the conclusions page).

**If this changes, update here.** A module added or split; a dial block;
the artifact's top-level shape; the anchor rule.

**Drill down.** `data_center/README.md`, `data_center/CURRENT_STATE.md`,
the `code/src/data_center/__init__.py` and `engine.py` docstrings,
`code/README.md` (the space and ground JSON contracts),
`docs/adr/003-ground-reference-anchored-to-deployed-year-cohort.md`.
