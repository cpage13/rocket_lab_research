# Atlas map: Rocket Lab Research

The pieces of this repository as built, how they connect, what must stay
true, and where to start for each task. The charter (`AGENTS.md`) holds the
mission, rules and goals; each piece has its own page in `atlas/pieces/`.

## Rules of this atlas

- A page may be a sketch, but it states nothing untrue; what cannot be
  verified is marked open.
- A change to a piece updates its page in the same change (in a planned
  cycle, the part that changes it carries the page); the map and the
  charter are updated at acceptance.
- Pages hold what changes slowly; values, counts and schema versions live in
  the code, the scenarios and the promoted JSON. No history: changelogs and
  dated progress belong in git, `code/CHANGELOG.md` and `.agent/` (local).
- Every `.agent/` path (local) exists only in the investor's checkout; its
  mark sits on the path's own line.
- One home per fact. The charter owns the rules and goals; this map the
  edges, flows, invariants with their guards, and the open concerns no
  single piece owns; each piece page its piece's state, rules, procedures,
  open items and test gaps; the glossary words only (an ambiguity is a word
  conflict, never the state of work). A fact stated twice becomes a pointer.

## The pieces

| Piece | Holds | Page |
|---|---|---|
| Research wiki | `research/`: evidence, theses, catalogs, the source ledger | [research-wiki](pieces/research-wiki.md) |
| Assumptions | the scenario files, the two assumptions ledgers, the stated assumptions | [assumptions](pieces/assumptions.md) |
| Data-center model | `code/src/data_center/` | [data-center-model](pieces/data-center-model.md) |
| Communications model | `code/src/communications/`: the Iridium model, its saturation curve, the on-hold cellular family | [communications-model](pieces/communications-model.md) |
| Shared core | `code/src/common/` | [shared-core](pieces/shared-core.md) |
| Promotion | the publishing commands, the gate, the writer, the promoted JSON | [promotion](pieces/promotion.md) |
| Conclusions | each application's verdict and its public documents | [conclusions](pieces/conclusions.md) |

## Reading trails by task

Before any task on a piece with active work in `.agent/INDEX.md` (local),
read the resume point it names: it holds what is decided but not built.

- **Get oriented:** `AGENTS.md`, this map, `CONTEXT.md`; then where the
  models stand: the promotion page's headline reads and, for communications,
  its page's State and Open.
- **Resume active work:** `.agent/INDEX.md` (local), then the resume point
  it names, through forge-recover, then that file's read list.
- **Answer a question about results, or draft a public piece:** the
  charter's Presentation, Public documents and Facts lines; for
  communications, the communications page's State and Open first; the
  conclusions page's public-document rules and guardrails; the value from
  the promoted JSON (query recipes on the promotion page); the claim's
  status in `research/SOURCE_INDEX.md`. A haircut of an engineering case is
  a linear division in the conclusion (the charter), never a model change;
  the market view is the product case (ADR 012), not yet built.
- **Start new research, a new feasibility study or a new document:** the
  research-wiki page and its rules, then a search of `research/LIBRARY.md`
  and `research/SOURCE_INDEX.md`; only gaps get new research.
- **Change a dial:** the application's checklist on the assumptions page,
  then the model's page.
- **Work on the data center:** the data-center page, then
  `data_center/CURRENT_STATE.md`, `data_center/README.md`,
  `data_center/assumptions.md`, `data_center/conclusion.md`.
- **Work on communications or saturation:** the communications page (State
  and Open first) and ADRs 005 to 012; for active work, the resume point
  named in `.agent/INDEX.md` (local), through forge-recover. The folder's
  documents (`communications/CURRENT_STATE.md`, `communications/README.md`,
  `communications/assumptions.md`, `communications/conclusion.md`,
  `communications/design.md`) still describe the model before the
  saturation work until their rewrite (the conclusions page, Open): read
  them for history and sources, never for the built model.
- **Touch shared code:** the shared-core page; both models' frozen
  baselines must hold.
- **Review or test:** the invariants and their guards below, the suite view
  under Open, each page's Tests heading, and the charter's Quality bar.
- **Local research wikis**, each a folder directly in `.agent/other/` (local)
  that holds a catalog file named LIBRARY.md, at its top or in a wiki folder:
  - `.agent/other/flatellite_dimensions_09_29/` (local): how large a Flatellite (Rocket Lab's flat, stackable satellite, the body the Iridium model's panel stands for) can be, and how many stack per Neutron launch. Answer (validated; the counts derive from estimates, low confidence): a panel of at most 15.4 m^2 (about 4.1 by 4.0 m), which the investor approved as the panel; 15 per launch today (11 to 20); on a block-upgraded Neutron (11 to 26), 16 with the stack kept in the fairing's cylinder (the investor's approved default), 17 to 19 only if it rises into the nose. The published Iridium model flies the approved panel and 16 per launch (the communications page). Start at its LIBRARY.md.
  - `.agent/other/ground_infrastructure_2036/` (local): what a 2036 ground AI data center costs, line by line. Open and dormant; its front page's Status line is stale (it says wave 1 is ingesting, though the wave-1 synthesis exists). Start at its LIBRARY.md.
  - `.agent/other/starlink_ai1/` (local): do SpaceX's AI-1 specs match the model's mass and thermal ratios? Answer, on SpaceX's revealed specs: AI-1 matched on silicon and solar and beat the model on the radiator, whose deployed double-sided design the default now flies; published as `data_center/ai1_comparison.md`. Start at its LIBRARY.md.
  - `.agent/other/wiki_terminal_uplink/` (local): what upload speed the small and mounted terminals get on the modeled network, and whether the upload side carries every seat the download sizes. Answer: see its front page's Status (open). Start at its LIBRARY.md.

## How the pieces connect

```text
sources (filings, papers, the web)
      |
      v
research wiki (research/): topic documents, theses, source ledger
      |  claim IDs, source statuses, research paths
      v
assumptions: the scenario dials (code/scenarios/; defaults in code/src/)
  and the ledgers (data_center/assumptions.md, communications/assumptions.md),
  whose stated rows set no dial
      |  typed configs
      v
data-center model | communications model  (on the shared core)
      |  promotion: three commands, one rollback writer
      v
promoted JSON (data_center/models/, communications/models/)
      |  deliberate review, never generated
      v
conclusions and public documents (README.md summarizes both)

inside communications, the curve first, then the artifact that reads it:
  the held spectrum, the named constants and the shipped population grid
      --saturation command-->  communications/models/iridium/saturation_curve.json
  the Iridium scenario and that curve, identity-checked
      --Iridium command-->     communications/models/iridium/default.json

.agent/other/ research (local) --validated, investor's go--> research/
```

| Edge | What crosses |
|---|---|
| sources to research wiki | topic documents; a `research/SOURCE_INDEX.md` row (claim ID, source status, sources) for every hard number a public document or model input uses |
| research wiki to assumptions | claim IDs, statuses and research paths, cited by the ledgers; in the data center the input spec tables (`code/src/data_center/input_manifest.py`; the ground's in `code/src/data_center/ground.py`) give every input its claim, status and rationale; a docstring may cite a claim too |
| within assumptions | the scenario dials and the two ledgers (what each ledger covers is on the assumptions page), plus stated rows that set no dial; investor-set values enter here, labeled investor-set |
| assumptions to models | YAML read by `common.file_io.load_yaml_mapping` into frozen Pydantic configs (`data_center.config.load_config`, `data_center.ground.load_ground_config`, `communications.config.load_comms_config`) |
| shipped data to the saturation command | the population grid `communications/data/ghs_pop_e2030_0p25deg.npz` (ADR 009), read by `communications.saturation.load_population_grid` and refused unless its digest is `POPULATION_GRID_SHA256` |
| shared core to models | the cadence spine, the cohort cliff, cell and source-status types, the file boundary, the command conventions |
| models to promoted JSON | promotion, from `code/`, three commands through the rollback writer: `uv run rklb-value --promote` (space and ground), the saturation command `uv run python -m communications.saturation` (the curve; a heavy run) and the Iridium command `uv run python -m communications.json_output` (the Iridium artifact); their arguments, stamps and order on the promotion page |
| promoted curve to the Iridium model | the Iridium command reads the curve its scenario names through `communications.saturation_curve.load_saturation_curve`, and the identity check, `communications.saturation_curve.check_curve_matches`, refuses a curve computed for other inputs: the one promoted file a model reads back |
| promoted JSON to conclusions | a person reviews the JSON and edits the prose; nothing is generated (ADR 001) |
| research wiki to conclusions | public prose cites claim IDs and human labels (the Source rules on the conclusions page) |
| local research to research wiki | validated findings (a separate seat re-checked the sources and recomputed the numbers), read by the investor, moved on their go (the research page's rule 8) |

## The flows

**The feasibility arc.** Each application is a feasibility study. The
investor's hypothesis is an append-only thesis, revised after each research
wave (`research/vision/initial_thesis.md` for the data center,
`research/vision/comms_thesis.md` for communications); the waves hunt the
hard barriers first; the model answers the all-in question; the conclusion
is the feasibility verdict, reviewed against the promoted JSON.

**From research to a published number.** A source lands in a topic
document, the catalog (`research/LIBRARY.md`) and the tracker
(`research/RESEARCH_TRACKER.md`); the hard number gets a source-ledger row
(claim ID, status); the input that carries it cites the claim (where each
model keeps that citation: the assumptions page, Source classes); the model
computes with it; the promoted JSON carries the value (data center: a provenance
cell and an `inputs.assumption_index` entry with its claim; Iridium: the
value, its claim trail staying in `code/src/communications/constants.py`
and the ledger, and the saturation curve's inputs in its `parameters`,
which the Iridium artifact names by `saturation.input_hash`); the
conclusion quotes it with its claim ID or human label.

**Changing a dial**, in the ledgers' own order (their maintenance rule):
the dial's ledger row where it has one (and the source ledger if the claim
trail changes); every home of the default, changed together with its
mirrors; the default guards; the frozen records and the tests that pin the
old value; re-promotion (for communications, the saturation curve first
when the change moves one of its inputs); then a review of every document
that quotes a moved number. Each application's checklist is on the
assumptions page.

**A new application or model family.** Thesis first: a new study runs
locally under the research page's rule 8, and on the investor's go its
thesis moves into `research/vision/` as an append-only belief record;
research waves with claim IDs and labeled estimates (for a communications
family, its lane named); the investor sets every assumption value; then a
ledger, a config block, named constants, a family module whose deployment
rule runs on the shared fleet loop and whose record sits beside the shared
one, a scenario file and a frozen suite, promotion, and a conclusion
written deliberately. A market view of an engineering model is a separate
model on its promoted artifact (ADR 012). `communications/design.md` gives
a communications family's steps, as they stood before the saturation work.

## Final objects

- `data_center/models/space/default.json`: the space artifact (`metadata`,
  `inputs`, `physical`, `business`, `meta`); every numeric leaf under
  `physical.years` and `business.years` is a provenance cell, except each
  year's `year` index.
- `data_center/models/ground/default.json`: the ground reference
  (`metadata`, `anchor`, `inputs`, `ground`, `orbital_reference`,
  `comparison`, `meta`), built from the space output in the same promotion.
- `communications/models/iridium/saturation_curve.json`: the saturation
  curve (`schema_version`, `version_stamp`, `parameters`, `input_hash`,
  `provenance`, `classes`, `bands`, `limits`), each people class's rows and
  markers and the phone class's band points, computed by the saturation
  command and read back by the Iridium command.
- `communications/models/iridium/default.json`: the Iridium artifact
  (`provenance`, `trajectory_summary`, `orbit_scenario`, `iridium_physics`,
  `classes`, `years`, `fixed_books`, `saturation`, `assumptions`);
  `fixed_books` holds ADR 007's two IoT lines, which ADR 011 replaces with
  IoT's capacity when its code lands.
- The conclusions and public documents, reviewed against these.

Each artifact states its schema version (`metadata.schema_version`; the
Iridium artifact's `provenance.schema_version`; the curve's top-level
`schema_version`); `code/CHANGELOG.md` records them, though not yet the
curve's or the current Iridium schema (the promotion page, Open).

## Invariants, binding ADRs, and the guards that enforce them

- Promotion writes JSON only; the conclusions are static reviewed prose
  (`docs/adr/001-static-conclusion-dynamic-models.md`). Guard:
  `test_promote_does_not_overwrite_static_conclusion`
  (`code/tests/data_center/test_cli_promote.py`).
- The promoted JSON is the canonical machine-readable surface: inputs,
  provenance, source statuses, validation, data dictionary, formulas, query
  examples (`docs/adr/002-agent-first-json-contract.md`). Guards, for the
  data center: `test_output.py` (the schema), `test_query_examples.py`
  (every worked query runs), `test_validation_results.py`. The Iridium
  artifact and the saturation curve do not carry it all (Open, below).
- The ground reference anchors to the anchor year's deployed-year cohort
  over its service life, never to the living fleet or a market share, and
  is an order-of-magnitude screen, never parity
  (`docs/adr/003-ground-reference-anchored-to-deployed-year-cohort.md` and
  its amendment). Guards: `test_ground_reference.py`, `test_run_window.py`.
- Git is the archive; the old flat model alias is not restored
  (`docs/adr/004-remove-archive-and-old-model-alias.md`). No test guards
  it; git tracks only the two default files under `data_center/models/`
  (the `.gitignore` rules).
- Inputs and outputs are typed (frozen Pydantic models, `extra="forbid"`
  configs), never loose dictionaries for known shapes. Guard: `mypy --strict`
  over `code/src/`.
- Every release-critical input has a source status and a rationale; in the
  data-center artifacts a value a scenario changes is a scenario override
  (status `scenario`), never under the default's claim. Guards:
  `test_input_manifest.py` (cited `RLDC-*` statuses match the ledger; the
  default publishes no override; an override drops the default's claim) and
  `test_provenance_uses.py` (every `uses` path resolves). The ground
  defaults lack the space default's two guards (the data-center page, Open).
- The data-center code defaults equal `code/scenarios/default.yaml`
  (`test_code_defaults_equal_the_default_scenario_file`); the two rebased
  sensitivity scenarios carry every default dial but their stated changes
  (`test_scenario_drift.py`).
- Launch and node counts are whole numbers, and deployed-year capacity and
  the living fleet stay separate: rules V14 and V16 and the model invariants
  in `code/src/data_center/validation.py`, tested in `test_validation.py`
  and `test_validation_results.py`.
- Data-center revenue is coupled to cost through the revenue multiple: no
  independent revenue dial exists
  (`test_compute_year_revenue_band_is_cost_times_r` in `test_engine.py`;
  `test_naming.py` keeps the revenue and profit fields apart).
- Data-center promotion writes nothing when any check fails
  (`test_cli_promote.py`). The two communications commands have no gate of
  results, and their refusals are listed once, on the promotion page: the
  saturation command writes only a curve that passes its completeness
  check (`check_curve_complete`), and the Iridium command runs only on a
  curve computed for its own inputs (the identity check, below). The
  regeneration test guards the Iridium artifact
  (`test_regenerated_default_artifact_matches_committed`) and the drift
  tests the curve (the frozen baselines, below).
- A people class's saturation number, where its rows reach one, is a
  spectrum bound reported beside the launch cadence, never a build target
  or a cap on the build, and a fleet past a class's last computed row is
  refused, never extrapolated or clamped. A class whose rows never reach
  one has no saturation number: the curve names the last midpoint at which
  its rows measure the elasticity as the fleet it is not reached by, and a
  run whose final year's living fleet passes that fleet is refused, since
  the curve does not measure the elasticity there and which limit binds is
  not known (`docs/adr/005-iridium-spectrum-bound-from-saturation.md`).
  Guards: `test_a_saturation_number_is_reported_beside_the_cadence_never_a_cap`,
  `test_a_fleet_past_a_class_last_row_fails_naming_the_year_the_class_and_the_last_row`,
  `test_a_final_fleet_past_the_not_reached_by_fleet_is_refused` and, at the
  command, `test_a_final_fleet_past_a_no_number_classs_label_is_one_error_line`.
- A run reads only a curve computed for its own inputs: the identity check
  refuses any other, naming the first field that differs
  (`test_the_iridium_entry_runs_only_on_a_curve_computed_for_its_inputs`,
  `test_the_identity_check_names_the_first_field_that_differs`).
- The people of the small terminal, the mounted terminal and the phone
  class come from the curve in one run, times the downlink share and the
  panel factor; every seat is sold at each class's flat price on the fleet
  the cadence builds, with no target and no cap; nothing is sold below the
  coverage floor. Each class's column is the whole fleet sold to that class
  alone, so the columns are never summed: a business view weights them by
  shares of the fleet's beams the investor names, in the conclusions. Each
  class's own margin is its own revenue against the year's whole-fleet
  annualized cost, re-derived after a haircut or a mix, never divided or
  averaged (`docs/adr/006-people-from-the-curve-every-seat-sold.md`,
  `docs/adr/008-downlink-time-share-scales-people.md`). Guards:
  `test_the_headline_every_class_alone_side_by_side`,
  `test_every_class_revenue_rises_every_year_from_the_floor_year`,
  `test_below_the_floor_nothing_is_sold_and_the_cost_accrues`,
  `test_halving_the_downlink_share_halves_people_capacity_and_the_pool_only`,
  `test_the_panel_setting_scales_people_beams_capacity_and_maximum_use_linearly`;
  no test reads the conclusions, so the columns' never-summed rule is held
  by review.
- Every list of the Iridium model's classes runs small terminal, mounted
  terminal, phone class, the order of `DeviceClass`
  (`test_every_class_in_one_run_in_class_order`); the charter's
  Presentation line gives each case's order.
- Demand is every resident of an inhabited cell of the shipped grid, which
  is refused unless its digest matches
  (`docs/adr/009-demand-every-resident-on-a-shipped-grid.md`;
  `test_load_population_grid_refuses_a_file_it_cannot_trust`).
- IoT: ADR 011 (`docs/adr/011-iot-is-capacity-in-the-engineering-model.md`)
  supersedes ADR 007 and is not yet built, so the Iridium artifact still
  carries ADR 007's two IoT lines, each outside every people class's margin
  (`test_the_two_iot_lines_are_fixed_books_frozen_exactly`,
  `test_each_class_revenue_is_its_people_times_its_price_and_the_books_stay_out`);
  government stays out of revenue under both. The product case
  (`docs/adr/012-product-case-is-its-own-model.md`) has no code or guard
  yet.
- `common` imports neither model, and `communications` never imports
  `data_center` or carries Starship, market-share, market-size, adoption,
  take-rate or uptake machinery (`test_no_venture_imports.py`,
  `test_no_venture_cross_import.py`); the shared fleet loop,
  `communications.engine`, imports neither the Iridium family nor the
  curve's contract (`test_engine_imports_no_family_module`); numpy stays
  inside `communications.saturation`
  (`docs/adr/010-numpy-runtime-dependency.md`;
  `test_numpy_stays_inside_the_saturation_module`).
- Both models run on one cadence spine (`test_cadence_move.py`); how their
  all-in cases relate is the charter's Objective 1.
- Frozen baselines lock the published numbers: the data-center golden
  trajectory (`test_parity.py`), the ground invariant, the Iridium suite and
  the committed saturation curve (the drift tests
  `test_committed_curve_has_not_drifted`,
  `test_committed_curve_has_not_drifted_in_its_band_rows` and
  `test_committed_curve_has_not_drifted_in_its_derived_fields`). Beside
  them, `test_a_second_promotion_at_the_coarse_setting_is_byte_identical`
  guards the saturation command's determinism (two coarse promotions write
  the same bytes but for the run's own measurement), not the committed
  curve. The equality tripwire
  (`test_iridium_and_cellular_runs_share_the_fleet_and_cost_records`; HB
  is the on-hold High-Bandwidth Cellular family) locks the shared fleet
  loop: on config defaults, with the cellular subscriber target raised so
  that fleet never reaches it, an Iridium run and a cellular run produce one
  fleet-and-cost record.
- No em-dashes in the files `code/tests/test_no_em_dashes.py` covers: the
  code, tests and scenarios, the promoted JSON, the root documents
  (`CLAUDE.md` among them), every document under `atlas/`, `docs/`,
  `data_center/` and `communications/`, and the research front door and
  ledgers; not the research write-ups.
- Every link, path, module, entry point, `jq` field, test, claim ID and
  code name the charter, the glossary, the atlas and the ADRs spell
  resolves on the tree (a code name is a word of the code, never of a
  comment or docstring alone; a superseded ADR is history, so its code
  names are not checked, its links and paths are), and every line that
  names a `.agent/` path, in any form, is marked (local)
  (`code/tests/test_agent_docs_resolve.py`, which also lists the spans an
  accepted ADR names before its code exists).

## Open, cross-cutting

- **The documents guard's reach.** It resolves names in backticks, not
  numbers, counts, claims or a command's flags, and a name it finds may
  still sit in the wrong place (its docstring says what it misses). The
  human documents (the root `README.md`, `code/README.md` and the folders'
  documents) are outside it: no test resolves their links, paths or
  numbers.
- **The suite as a whole** should keep covering config parsing, the
  generation and physical math, integer cadence, deployed-year versus
  living capacity, the source-status and input-manifest contract, the JSON
  schemas and query examples, promotion and conclusion stability, the
  ground anchor and parity warnings, the saturation curve and its drift,
  the Iridium run on it, and the test command's four gates (charter,
  Project rules). The guards check their own file lists, so they cannot
  pass vacuously (the em-dash guard and the documents guard fail on a
  missing path; `test_comms_src_files_discovered`). Tests anchor every path
  to their own file and write only to temporary folders, so the suite runs
  from `code/` and from the root. No test checks that every module has a
  test file; each page's Tests heading names its own gaps. Fixtures sit in
  `conftest.py` at the test root and in the two model test packages; pytest
  runs in importlib mode, set in `code/pyproject.toml`, because the model
  test packages share module names.
- **Artifact contracts.** The data-center artifacts meet ADR 002; the
  Iridium artifact and the saturation curve carry no per-value provenance
  cells, data dictionary, query examples or validation results, so they
  fall short of it (the curve has its own Pydantic contract and
  completeness check instead).
- **Decided, not built.** ADRs 011 and 012 are accepted with no code yet:
  the Iridium artifact still carries ADR 007's two IoT lines, and the
  product case has no package, page, artifact or guard. Each lands with its
  pages (the atlas's rule): the product case gains its piece page, its row
  above, its final object and its invariants then.
- **Unrecorded decisions.** Modeling the maximum in the engineering models
  (haircuts as a division) and the revenue-cost coupling have no ADR,
  though ADR 006 records the communications haircut rule; the market view's
  separation is ADR 012. Recording the rest waits for the investor.
