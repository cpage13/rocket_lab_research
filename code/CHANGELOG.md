# Changelog

All notable changes to the `code/` model package: the `rklb-value` orbital
data-center valuation calculator and, from July 2026, the communications model
families. Versions track each output JSON **schema version** (the data center:
space v9 and ground reference ground-v2; the Iridium model: iridium-v5).

## Data center, space schema v9 and ground schema ground-v2 (2026-09-23), the review fix set

The mechanical fixes from the 2026-09-23 cold code reviews, adversarial
reviews, and `/code-review` pass: phases 1 to 4 (commits 19c76c9, e203397,
6250cd7, 262422f) and phase 6 (the scenario rebases, the input-cell and
cost-line citations with their new ledger rows, `RLDC-BUS-COST` among them,
the em-dash sweep and its guard test, and the re-promotion); the command-line
and file changes shared with the Iridium model have their own entry below. No
headline number moves: the re-promoted default reproduces the 2036 cohort (90
launches, 66 GPU packages and about 753 kW per node, about 67.7 MW deployed),
the 268-node living fleet, $7,418.9M central revenue and $2,473.0M profit, and
the 1.2802x orbit-to-ground ratio exactly. The one intended change to a
default output value is the stowed volume; the two rebased scenarios move by
design (see Fixed). Both default artifacts were re-promoted on 2026-09-24
(their `metadata.generated_at`).

### Fixed

- **One anchor year.** Every hardcoded 2036 (the validation checks, the
  ground anchor, the query examples) reads one config-derived anchor year,
  `anchor_year(base_year, horizon_years)`: the base year + 10 (the year-10
  cadence anchor) when inside the window, else the last window year. The
  default still resolves to FY2036; a five-year window or a 2040 base year
  now runs end to end instead of crashing.
- **Service life everywhere.** V16's lookback and the published formula text
  follow the configured service life
  (`sum(cohorts[Y-(service_life_years-1)..Y].nodes_deployed)`,
  `/ service_life_years`); `FLEET_CLIFF_LOOKBACK_YEARS` is removed, and the
  3-year and 7-year scenarios pass V16.
- **Rules re-pointed.** V9 bands the life-independent node total
  (`node_total_in_band`, $50M to $200M, replacing
  `cost_annual_per_node_in_band`); V6 reads the anchor year, not the last
  window year; V17 checks both radiator dials when co-mounted; V15 checks
  `volume_utilization_pct <= 100` directly.
- **The binding constraint** is computed where N is packed: mass binds when
  less than one package of budget remains, `both` when the fairing is also
  full. The 99 percent threshold is gone; the default reads `mass` every year.
- **Stowed volume physics.** Stowed array volume is the deployed area times
  the stowed panel pitch (a fold changes the footprint, not the stacked
  volume), and the configured `node_volume_fixed_m3` is honored instead of a
  shadowing constant. The default FY2036 node volume moves from about 5.3 m3
  to about 26.6 m3 and fairing utilization from about 6.6 percent to about
  33.2 percent (previously understated about 5x); N and every headline number
  are unchanged.
- **Generations.** Extrapolated generations are dated latest listed plus k x
  cadence (no accumulated float error), the frontier comparison uses the
  named `FRONTIER_YEAR_TOLERANCE`, a generations list must be ordered (it
  fails loudly otherwise), `GenerationSlopes`, `GenerationSpec`, and `Source`
  forbid unknown keys, `year_available` is bounded by `MAX_FY`, and the slope
  defaults have one source.
- **Load-time validators.** Fixed node mass below the mass envelope; cadence
  anchors ordered inside the ceiling (`0 < launches_at_year_5 <
  launches_at_year_10 < cadence_ceiling`); launch-cost anchors ordered;
  revenue bands ordered (`low <= central <= high` at shared anchor years) with
  unique anchor years; `bus_growth_pre > -1`; ground `pue >= 1` and
  `utilization <= 1`. Each invalid case fails at load with a clear message.
- **Exact fits.** Package counts use `PACKAGE_FIT_TOLERANCE`, so an exact fit
  keeps its last package despite float rounding (the V1 slack derives from
  it); cadence is computed once per year.
- **Stale scenarios rebased.** `with_premium.yaml` and `upside_7yr.yaml`
  describe themselves as the default dial set plus stated changes, but still
  carried the dials the 2026-07-14 rebase replaced (the co-mounted radiator at
  0.013 and 0.012 t/kW, solar and radiator cost at 0.04 $M/kW). Both now carry
  the current default dials (radiator architecture `deployed_double_sided`,
  radiator dials 0.00165 t/kW, solar and radiator cost dials 0.02 $M/kW) and
  keep only their stated changes: the premium-uplifted central R band
  (`with_premium`), and the 7-year service life with its flat 1.47 central R
  (`upside_7yr`). FY2036 central living-fleet revenue moves from $6,391.2M to
  $7,518.3M (`with_premium`) and from $4,789.8M to $5,613.5M (`upside_7yr`);
  peak fairing volume utilization (reached in FY2035 and FY2036) moves from
  21.4 to 33.2 percent in both. `ambitious.yaml` still carries the co-mounted
  radiator dials, pending an investor decision.

### Changed

- **One verdict list.** `meta.validation_results` is built in one place: the
  16 V-rules, three checks that hold for any scenario
  (`anchor_year_launches_match_year_10_dial`, which replaces the
  default-pinned `target_cadence_is_90_launches`;
  `living_fleet_distinct_from_deployed_year_cohort`;
  `release_critical_inputs_have_no_placeholder_or_stale_status`), and three
  default guards emitted only for the canonical default scenario (22 checks
  in the default artifact). The text report, its banner counts, and the
  embedded `validation_warnings` query read the same list, so no scenario
  fails for differing from the default.
- **Assumption index.** `inputs.assumption_index` includes the 18
  revenue-band anchors (the default goes from 104 to 119 entries); the
  source-status summary follows.
- **Data-dictionary units** come from the cell each entry describes (66 space
  units corrected; for example, `mounting_overhead_pct` is a fraction).
- **Provenance closes.** Every dial that moves a cell is reachable through
  that cell's `uses` chain, across the space and ground artifacts:
  `gpus_per_node` cites the per-package mass inputs, the radiator dial active
  that year, and the Tjmax lift year; fleet rollups cite the per-vintage cells
  they sum and the service life; cumulative revenue cites the prior
  cumulative; extrapolated generations cite the slopes and cadence they
  derive from (role `derived_input`). A sweep test perturbs all 86 dials.
- **Source metadata is current.** The radiator dials describe the
  investor-set deployed double-sided bet (2026-07-14) and cite
  `RLDC-SOLAR-RADIATOR-MASS` (status `scenario`), as does the solar-mass
  dial, which keeps `THR-006` as a supporting claim; the fairing-volume dial
  cites `RLDC-FAIRING-VOLUME-80M3` (status `scenario`) instead of the
  payload-mass claim `NTR-004`, so the source-status summary moves those two
  cells from `sourced_estimate` to `scenario`. An input cell can cite
  supporting SOURCE_INDEX claims after its primary claim
  (`CellSpec.supporting_claims`). The cadence ceiling is the horizon-scoped
  infrastructure parameter citing `RLDC-CADENCE-CEILING-150`; labels derive
  from config ("Launches at the year-10 anchor").
- **Cost cells cite cost claims.** The solar and radiator cost lines cited
  `THR-006` (solar-array mass) and `THR-003` (hot-loop radiator area and
  mass), and the bus line and its three dials cited `THR-011` (node power).
  Each cost line now cites first the claim of the cost dial that sets it:
  solar and radiator `RLDC-SOLAR-RADIATOR-COST` (supporting `THR-013` and
  `THR-016`), launch `RLDC-LAUNCH-COST-2036` (supporting `NTR-009`, on the
  business launch-cost cell too), and bus the new ledger row `RLDC-BUS-COST`
  (status `scenario`), which the bus dials cite as well, so the base bus
  cost dial moves from `derived_estimate` to `scenario`. The ground
  reference's orbital components re-cite them; the compute line cites no
  claim, since no ledger row describes the node compute cost.
- **Scenario overrides.** A scenario value that differs from the default has
  the `assumption_role` `scenario_override` and status `scenario`, cites only
  the scenario YAML, and no longer carries the default's claim or rationale.
- **One generations vocabulary.** `meta.generations_dictionary` uses the
  input cells' source statuses (`certified`, `sourced_estimate`, and so on),
  not the internal `fact` and `estimate` tiers.
- **Ground reference.** The comparison window follows the anchor cohort's
  service life; the ground metadata reflects the scenario file actually
  loaded, and `space_model_path` comes from the caller; the anchor check
  compares nodes, GPU packages, kW, and service life with the space output's
  anchor-year cohort; `ArtifactRole` is one StrEnum for space, ground, and
  the CLI (`draft`, `promoted_default`, `promoted_named`,
  `promoted_ground_default`, `promoted_ground_named`); ground inputs use the
  common cell builders (one `ref_type` vocabulary); `uses` entries are
  resolvable paths, prefixed `space:` for cells in the space artifact; the
  ground data dictionary is generated by the shared builder (5 to 122
  entries).
- **Space schema v8 to v9.** The duplicate `business.years.*.kw_on_orbit` and
  `pf_on_orbit` are removed (read `kw_living_fleet` and `pf_living_fleet`);
  the data-dictionary `source_class` is typed by `FieldKind` and emitted
  lowercase (`input`, `constant`, `derived`); formula definitions go from 51
  to 48 and the data dictionary from 162 to 157 entries.
- **Ground schema ground-v1 to ground-v2.** The seven fields named
  `five_year` hold service-life values and now say so:
  `ground.total_service_life_cost`, `ground.cost_per_gpu_package_service_life`,
  `ground.cost_per_mw_service_life`,
  `orbital_reference.cost_per_gpu_package_service_life`,
  `orbital_reference.cost_per_mw_service_life`,
  `comparison.ground_total_service_life_cost`, and
  `comparison.orbital_total_service_life_cost`. The duplicate
  `orbital_reference.five_year_cost_view` gives way to
  `orbital_reference.total_build_and_launch_cost`, and the duplicate
  `ground.source_status_summary` dict to `meta.source_status_summary`. An
  empty anchor-year cohort is refused with one clear error instead of a
  traceback.
- **One implementation each.** A strict `as_float` / `as_int` cell unwrap
  (an integer read never truncates); the cadence and launch-cost dial classes
  and the eight cadence defaults live once in `common/cadence.py` (the
  communications config now validates its cadence anchors too); one R-band
  interpolation (`interpolate_r`); one artifact serializer and writer
  (`render_artifact_json`, `artifact_write`); one half-up rounding helper
  (`round_half_up`).
- **Typed keys and final constants.** `YearString`, `FiscalYear`,
  `FormulaName`, and `ConfigFieldName` key the year and formula maps; module
  constants are `Final`.
- **V14 alone judges whole launch counts** (`cadence_monotonicity`); the
  other rules read launch counts as numbers.
- **The revenue-trace query** (`trace_revenue_multiple_assumption`) reads the
  first central anchor, `.inputs.config.revenue.central[0]`, so a re-anchored
  band still resolves.
- **Scenario names carry no em-dash.** The labels of `ambitious.yaml`,
  `conservative.yaml`, `with_premium.yaml`, and `upside_7yr.yaml`, which a run
  emits as `metadata.scenario_name` and `inputs.scenario.name`, use a colon
  instead (for example "Conservative: 11t SSO, 3yr life, low R band, slow
  cadence").
- **Tests.** The em-dash guard (`tests/test_no_em_dashes.py`) holds the
  writing convention after the phase 6 sweep over every file under
  `code/src/`, `code/tests/`, and `code/scenarios/`; `code/README.md`,
  `code/CHANGELOG.md`, and `code/pyproject.toml`; the three promoted
  artifacts; the root documents and `.gitignore`; every document under
  `docs/`, `data_center/`, and `communications/`; and the research front door
  and ledgers (the legacy research write-ups stay excluded pending an investor
  decision). A failure names each offending line. The scenario drift guard
  (`tests/data_center/test_scenario_drift.py`) loads `with_premium.yaml` and
  `upside_7yr.yaml` beside `default.yaml` and fails, naming each dial by path,
  when either differs from the default outside its stated changes or stops
  making them. The citation tests (`tests/data_center/test_provenance_uses.py`
  and `tests/data_center/test_input_manifest.py`) read
  `research/SOURCE_INDEX.md` through a shared ledger fixture: every claim the
  artifacts cite must exist in the ledger, a cost line must cite a claim about
  cost (never a mass claim) and a mass cell never a cost claim, ground copies
  of space cost lines must re-cite them exactly, and every default input cell
  whose primary claim is an `RLDC-*` row must carry that row's source status.

### Removed

- V11 (`no_legacy_r_scalar`), its constants, wiring, and hand-injected test:
  16 V-rules remain.
- The inert dials `volume.fold_ratio`, `volume.si_areal_density_kg_m2`, and
  `volume.radiator_solar_area_ratio`, which no computation used, everywhere
  (config, input manifest, scenarios, tests).
- `data_center/conclusion.py` and `render_conclusion_markdown`: no callers,
  and it published contradictory hardcoded prose.
- The 52 unreferenced `comms_*` formulas and the prefix filter that hid them;
  the uncited formula definitions `launch_cost_musd_linear_ramp`,
  `mass_per_pkg_from_gen_and_dials`, and `r_at_year_from_band_anchors`; the
  test-only `dump_generations_yaml`; unused constants and enum members.
- The compatibility aliases and re-export shims: `ValuationOutput` (use
  `SpaceModelOutput`), `data_center.provenance` and `data_center.cadence`
  (import from `common`), and `QueryExample.jq` (read `jq_expression`).
- The stale `.gitignore` rule `data_center/conclusion_*.md` and its mention in
  the promoted-model comment: nothing writes a conclusion file (promotion
  writes JSON only, and the uncalled conclusion renderer is gone).

## The Iridium model, schema iridium-v5 (2026-09-23), the review fix set

The communications fixes from the same review set (phase 5, commit 5b1de2b,
with the phase 4 cleanup in 262422f). The published default reproduces
exactly: 340 satellites at 31,200 people per satellite, $1,450M
build-and-hold, about $145M a year steady-state cost, $250M final-year
replacement, and $8,250.8M a year of ARPU revenue at a 98.24 percent margin.
`communications/models/iridium/default.json` was re-promoted on 2026-09-23.

### Added

- `trajectory_summary.build_completes_in_horizon` (whether the fleet target
  is built inside the horizon; true at the baseline) and
  `trajectory_summary.built_fleet_annual_cost_musd` (the built fleet's build,
  launch, and replacement cost annualized over the satellite life; equal to
  the steady-state annual cost at the baseline).

### Changed

- **Schema iridium-v4 to iridium-v5**: the two keys above;
  `final_year_replacement_cost_musd`, `final_year_cash_cost_per_subscriber_usd`,
  and `cost_per_subscriber_annualized_usd` are nullable (`null` marks an
  undefined figure instead of a 0.0 that reads as a real cost); the
  "Built-fleet convention" and "Margin definition" stated assumptions are
  reworded to the built-fleet cost basis (each is published in both
  `revenue_arpu_buckets.stated_assumptions` and `assumptions`).
- **The ARPU margin's cost basis** is the built fleet's annualized cost
  (`built_fleet_annual_cost_musd`), the same fleet the revenue is computed on,
  so a build that does not complete inside the horizon no longer reads a
  margin against a different fleet. The baseline margin is unchanged.
- **The served base is capped at capacity**: the smaller of the subscriber
  target (or the served override) times the build-out and the fleet target's
  people capacity, so a saturated fleet never reports serving more people
  than it carries; the binding-regime labels agree. A served override above
  the capacity is capped, with a warning.
- **The replacement line** counts only retiring cohorts, never a build
  tranche; the final-year figures are `null`, not 0.0, when nothing retired;
  a zero space cost yields `null` ground ratios, as documented; the
  final-year cash cost per subscriber divides by the served base.
- **Engine names.** On `CommsTrajectory`,
  `steady_state_annual_replacement_cost_musd` becomes
  `final_year_replacement_cost_musd`, `cost_per_subscriber_annual_usd`
  becomes `final_year_cash_cost_per_subscriber_usd`, and
  `built_fleet_annual_cost_musd` is added; `CommsYear` gains
  `satellites_replaced_this_year`.
- **Validators and guards.** The coverage floor may not exceed the
  saturation cap; off-peak concurrency may not exceed peak; a derived density
  below one person per satellite is a clear error; launch shares round half
  up under `LAUNCH_SHARE_ROUNDING_TOLERANCE`, so an exact half is not lost to
  binary rounding.
- **Stale text corrected**: the cost-plus sentence and the dial-count
  contradiction in `scenarios/iridium.yaml`, the engine docstrings on the
  annualized versus final-year cash lines, and the code citations
  (`RLDC-REVENUE-MULTIPLE-1_5X` for the 1.5x, `COMM-530` for the ground
  cost; no agent-folder paths in code).
- **Tests.** The saturation scenario's published column is frozen end to end
  (2,000 satellites complete in 2035, 62,400,000 people, about $48.5B a year
  of revenue, about $835M a year of fleet cost); the variant densities and a
  strengthened equality tripwire are pinned; and regenerating the promoted
  artifact must reproduce the committed file (held by a strict xfail until
  this re-promotion; the marker is removed).

### Removed

- The unused variant constants `SPECTRUM_MHZ_COORDINATED` and
  `ACTIVE_USER_RATE_MBPS_RICH`, the never-built `PLACEHOLDER_DIAL_FLAGS` map
  and its `DialPath` alias, the module's own JSON renderer (the shared
  `render_artifact_json` serializes the artifact), and the duplicate margin
  helpers (the engine's `margin_pct` and `usd_per_person` serve both).

## Both applications (2026-09-23), promotion, command line, and file I/O

The command-line and file fixes from the same review set (phase 3, commit
6250cd7, hardened in phase 4, 262422f). Every scenario output and promoted
artifact is byte-identical apart from timestamps.

### Changed

- **Promotion rules.** The output name `default` belongs to
  `scenarios/default.yaml` alone (`is_default_scenario`): any other scenario
  needs `--output-name`, and output names are lowercase letters, digits,
  underscores, and hyphens only, so no case variant can land on
  `default.json` on a case-insensitive file system. The artifact role
  follows the scenario, never the name. Promotion refuses, and writes
  nothing, when any validation check fails in the space artifact or the
  ground reference, or when the anchor-year cohort is empty.
- **The backup-and-rollback pair writer.** Space and ground are built in
  memory, then written by `common.file_io.write_files_with_rollback`: each
  file is staged in full beside its destination, each existing destination
  is kept as a hidden backup, and the staged files are renamed into place one
  at a time. If a rename fails, the destinations already replaced are
  restored, and the error says which files were restored and which, if any,
  still hold new content. Staged and backup files are created exclusively
  under fresh random names (a name collision retries), the writer removes
  only files it created, and a destination that is a symbolic link or not a
  regular file is refused before anything is written. The Iridium promotion
  writes through the same function.
- **Exit codes** (`common.cli`): `EXIT_OK` (0); `EXIT_ERROR` (1), one
  `ERROR:` line and no traceback; `EXIT_USAGE` (2) for conflicting flags
  (`--default` with a config path, `--brief` with `--json`, `--output-name`
  without `--promote`, `--brief` or `--json` with `--promote`,
  `--input-schema` with anything else), a malformed `--output-name`, and a
  name that misstates the scenario.
- **Error wording.** A scenario that cannot be read or validated is
  `ERROR: could not load <scenario>: <reason>`; one the model cannot run is
  `ERROR: could not run <scenario>: <reason>`. A base year before the
  earliest listed generation and a generation-extension overflow are clean
  errors, not tracebacks.
- **One YAML loader**, `common.file_io.load_yaml_mapping` (libyaml's
  `CSafeLoader` with a `SafeLoader` fallback, utf-8), for all four loaders,
  raising one `ModelFileError` for YAML, OS, and encoding failures. A
  scenario's `generations:` path resolves beside the scenario file.
- **Logging.** A module logger in every source module; status and errors are
  log lines on stderr (`INFO: promoted <path>`, `ERROR: ...`); stdout carries
  only the product (the report, the headline, the JSON, the schema).
- **Source checkout only.** Repository paths resolve through
  `locate_source_checkout`, so an installed wheel fails clearly instead of
  reading or writing inside its virtual environment. `rklb-value`'s `main`
  takes a `models_dir` so tests promote into a temporary directory.
- **Tests.** Repository-anchored shared fixtures and a session-scoped
  default run; the suite passes from `code/` and from the repository root;
  `ValuationConfig()` is pinned to `default.yaml`; jq runs once per
  expression; the ground module loads lazily.
- **`.gitignore`**: named local promotions and the writer's recovery files
  stay out of git, while the two data-center `default.json` artifacts stay
  tracked, as the file's comment intended.

## Data center, schema v8 (2026-07-15), the deployed-capacity validation band rebased

The `default_2036_deployed_capacity_around_40mw` public validation check had
been failing against the promoted default since the 2026-07-14 light-radiator
rebase moved 2036 deployed capacity from about 38 MW/year to about 68 MW/year.
The band now guards the rebased anchor.

### Changed

- **The deployed-capacity band** (`json_output.py`): `DEPLOYED_KW_LOWER_BOUND`
  and `DEPLOYED_KW_UPPER_BOUND` move from 35,000-45,000 kW to 60,000-75,000 kW,
  and the rule id and text move from
  `default_2036_deployed_capacity_around_40mw` to
  `default_2036_deployed_capacity_around_70mw` ("around 70 MW/year"). The
  ledger claim id `RLDC-DEPLOYED-CAPACITY-2036-40MW` keeps its name for
  reference stability. The AI-1-equivalent scenario (about 81 MW deployed in
  2036) still trips the band by design.

## Data center, schema v8 (2026-07-14), the AI-1-class light-radiator rebase

Per investor decision (commit e0c4494), the default scenario semi-copies the
AI-1 architecture. The schema is unchanged (still v8).

### Changed

- **Radiator architecture.** `RadiatorArchitecture` gains
  `DEPLOYED_DOUBLE_SIDED` (a dedicated deployed wing, edge-on to the sun,
  radiating from both faces, run hot) and the default moves to it,
  superseding the D16 co-mounted lock. Co-mounted stays available as the
  labeled conservative posture, with V17's 0.010 t/kW floor enforced whenever
  it is selected.
- **Radiator mass** goes to 0.00165 t/kW before and after the Tjmax lift
  (within 10 percent of AI-1's implied 0.0015; the Tjmax step is inert in the
  default and kept for the exception scenario).
- **Solar and radiator cost dials** go from the uncited cycle-1 0.04 to 0.02
  $M/kW each (THR-013 / THR-016; investor-set, judged conservative at
  assembly-line manufacturing scale with in-house vertical integration and a
  five-year life). The two moves are booked through two distinct channels,
  never double-counted: the mass dial carries the temperature and
  architecture win, the cost dials carry the manufacturing-scale win.
- **New frozen baseline**: FY2026 223 packages and about 457 kW per node;
  FY2036 66 packages and about 753 kW; the 2036 cohort 90 nodes, about 67.7
  MW, and 5,940 packages; a 268-node living fleet; $7,418.9M fleet revenue
  and $2,473.0M profit at the pinned 33 percent margin. The orbit-to-ground
  ratio moves from 1.9168x to 1.2802x. Tests re-pinned across the parity,
  engine, output, config, constants, and validation suites (554 passed); the
  space and ground artifacts re-promoted. The default deployed-capacity guard
  (then 35,000 to 45,000 kW) failed against the rebased default until the
  2026-07-15 band rebase above.
- The data-center terminology sweep to investor wording rides along (18
  tokens across scenarios, config, output, validation, provenance, and
  tests).

## The Iridium model, schema iridium-v4 (2026-07-14), the promoted contract cleaned

Per investor direction (commit df37011): the trajectory summary's cost bases
now say what they are, and the published orbit posture rides in the
artifact. No old JSON kept.

### Changed

- **Renamed cost keys**, the final-year cash pair:
  `steady_state_annual_replacement_cost_musd` becomes
  `final_year_replacement_cost_musd` (250.0) and
  `cost_per_subscriber_annual_usd` becomes
  `final_year_cash_cost_per_subscriber_usd` (25.0).
- Citation and docstring fixes: the config lifetime citation moves from
  COMM-091 to COMM-088 (091 stays the per-subscriber cost split it actually
  is), and the engine launch-coupling docstring states the inverse-area
  convention (5 at 60 m^2) beside the estimate-bound mass quotient (6).

### Added

- **The annualized basis** beside the cash pair:
  `cost_per_subscriber_annualized_usd` (about 14.50).
- **The denominators the prose quotes**, as first-class fields:
  `living_fleet_final_year` (348), `cumulative_launches_to_completion` (29),
  `cumulative_launches_final_year` (58), `people_capacity_target_fleet`
  (10,608,000), and `people_capacity_living_fleet_final_year` (10,857,600).
- **The `orbit_scenario` block**: the published posture (450 km, 53 degrees,
  source status `scenario`) with a basis paragraph carrying the simulation
  support and its honest bounds, documented in code by
  `ORBIT_ALTITUDE_KM_SCENARIO`, `ORBIT_INCLINATION_DEG_SCENARIO`,
  `ORBIT_SCENARIO_SOURCE_STATUS`, and `ORBIT_SCENARIO_BASIS`.
- The export test freezes the v4 schema: the renamed keys, the annualized
  line, all five denominators, and the orbit block.

## The Iridium model, schema iridium-v3 (2026-07-14), the all-in deployment baseline

Per investor decision (commit b236a13): the Iridium baseline answers the same
all-in deployment question the data-center model answers. A scenario-level
change: no config-schema or artifact-schema change.

### Changed

- **The all-in share.** `scenarios/iridium.yaml` overrides the shared-spine
  `comms_cadence.share_of_fleet` to 1.0 (the config default 0.18 is
  untouched, so the High-Bandwidth Cellular Pure Play family and the equality
  tripwire still ride the defaults; 0.18 is retired to a sensitivity). The
  340-satellite fleet completes in 2031 (29 launches, the ramp-bound floor).
- **The re-promoted default**: full coverage in 2031; FY2036 build-and-hold
  1,450.0 $M (696 satellites and 58 launches: the 2031 build plus one full
  five-year fleet replacement); final-year replacement cash 250.0 $M (25.00
  USD per subscriber over the configured 10M); the steady-state annual cost
  unchanged at about 145 $M; the Sheet A bucket block untouched (8,250.80256
  $M at 98.24 percent). Tests re-frozen to the new baseline plus a
  completion-year pin (554 passed).
- **Terminology**: the communications code, scenarios, and the promoted
  artifact's assumption strings adopt investor wording (commit 02665be, a
  wording change only).

### Added

- **The saturation companion scenario** `scenarios/iridium_saturation.yaml`:
  the subscriber target raised to the cap-binding 62,400,000; the
  2,000-satellite build completes in 2035 (2,004 living on whole launches,
  200 cumulative launches through FY2036, 5,000.0 $M build-and-hold, about
  835 $M a year steady state, Sheet A about 48,534 $M a year at about 98.3
  percent).

## The Iridium model, schema iridium-v3 (2026-07-10), the cost-plus revenue case removed from the artifact

Per investor direction: the synthetic cost-plus revenue convention (price at
1.5x annualized cost, the automatic 33.3 percent margin) is the data center's
no-prices-available discipline. The Iridium model now has a real published
revenue case (the four-bucket ARPU case, schema iridium-v2) with real cost and
margin, so cost-plus is ruled out of every Iridium-facing surface. The
shared-engine machinery is untouched: the cellular family still earns cost-plus
revenue and the equality tripwire still rides the shared trajectory, exactly
like the earlier placeholder-ARPU removal.

### Removed

- **The two cost-plus fields dropped from the promoted Iridium artifact**
  (`json_output.py`): `steady_state_revenue_cost_plus_musd` and
  `steady_state_gross_margin_cost_plus_pct` are removed from
  `TrajectorySummaryBlock`, which now carries the cost and fleet story only (no
  revenue case; the published Iridium revenue lives in `revenue_arpu_buckets`).
  The ENGINE still computes both on the shared `CommsTrajectory` (the cellular
  family reads them, the equality tripwire rides that shared trajectory), fenced
  with a comment extended from the placeholder-ARPU removal so a future cleanup
  pass keeps the engine seam. `IRIDIUM_SCHEMA_VERSION` bumped to `iridium-v3`.
- **The cost-plus prose dropped from the Iridium assumptions output**
  (`engine.py`, `iridium_assumptions`): the revenue-case lines no longer assert
  cost-plus is published (the ARPU path) or load-bearing (the no-ARPU path) for
  Iridium, so the regenerated artifact carries no cost-plus claim. The cost-plus
  computation, the `CommsTrajectory` fields, and the cellular family's path are
  untouched.

### Changed

- The published ARPU margin (`arpu_margin_vs_steady_state_cost_pct`) is
  unchanged: it is measured against steady-state COST, not cost-plus, so it
  stays exactly as is (98.242595 percent at the baseline).
- **Tests**: `test_promoted_json_export_writes_frozen_baseline` asserts the two
  cost-plus fields ABSENT and freezes schema `iridium-v3`; the 217.5 cost-plus
  freeze (and its now-dead constant) is removed while the cost freezes 900.0 /
  75.0 / 145.0 / 7.5 and the full ARPU block including the 98.242595 margin stay.
  The equality tripwire and the cellular family's cost-plus engine tests are
  untouched (554 passed, DC parity 8).
- Docs refreshed in tandem: `communications/conclusion.md` (the cost-plus floor
  paragraph removed from the money section), `communications/assumptions.md`
  (the cost-plus dial row and register row 14 reframed as shared-engine
  machinery not published for Iridium, the cost-plus output-anchor row dropped,
  the machine-name note refreshed), the root `README.md` (the comms revenue
  sentence reworked to the published case only), `communications/CURRENT_STATE.md`,
  and `communications/design.md`. The promoted `default.json` re-promoted at
  stamp 2026-07-10.

## The Iridium model, schema iridium-v2 (2026-07-09), the flat cost model and the published ARPU margin

A same-day follow-on to the four-bucket ARPU case, per investor direction:
the cost model is simplified to investor-flat dials, the promoted ARPU block
now carries its margin metric, and the margin naming is corrected across the
communications docs (it is not a gross margin).

### Changed

- **The flat cost model (scenario-level only, no config-schema change).**
  `scenarios/iridium.yaml` now sets `launch_cost.low_cadence_cost_musd` and
  `launch_cost.high_cadence_cost_musd` both to 13.0 (equal anchors make the
  shared log-linear curve flat: 13.0 $M per launch at every cadence, just
  below the grounded 13.5 high-cadence floor; the two launches anchors stay
  default) and `satellite.satellite_build_cost_musd` to 1.0 (just below the
  prior 1.05 dial and the ~1.2 $M Starlink V3 hardware anchor, COMM-080).
  The shared-spine config defaults (the 25.0-to-13.5 curve, the 1.05 build
  cost) are untouched, so the cellular family and the equality tripwire are
  unaffected. New frozen baseline costs, all exact: build-and-hold 900.0 $M
  (432 satellites x 1.0 + 36 launches x 13.0), steady-state replacement
  75.0 $M/yr, steady-state annual cost 145.0 $M/yr, cost-plus revenue
  217.5 $M/yr, cost per subscriber 7.50 USD/yr. The ARPU bucket block is
  unchanged (total 8,250.80256 $M/yr).
- **The published ARPU margin** (`json_output.py`, within schema iridium-v2,
  same-day additive field): the `revenue_arpu_buckets` block gains
  `arpu_margin_vs_steady_state_cost_pct`, ARPU revenue less the steady-state
  annual cost over ARPU revenue (98.2426 percent at the baseline), computed by
  a pure helper against the trajectory's `steady_state_annual_cost_musd` with
  the engine's zero-revenue guard convention. `arpu_stated_assumptions`
  (`engine.py`) gains a fourth posture line defining the metric honestly:
  measured against the fleet's full build, launch, and replacement cost;
  operations the explicit zero pending research; corporate overhead never
  included; an operating-style margin, not a gross margin and not a net margin.
- **Tests**: `test_promoted_json_export_writes_frozen_baseline` now freezes the
  five flat-cost values and the margin exactly (new named constants); the
  equality tripwire and every other test untouched (554 passed, DC parity 8).
- Docs refreshed in tandem: `communications/conclusion.md` (the flat-cost
  paragraph, the 217.5 cost-plus floor at about 1.81 dollars per subscriber
  per month, the 98.2 percent margin with its definition, the 88-to-94
  percent investor-range sweep, the premium price-tier reframe),
  `communications/assumptions.md` (the two investor-flat dial rows, register
  rows 13/28/34 plus the new row 42, the output anchors, the premium
  price-tier note), the root `README.md` (about $218M a year at a 33 percent
  margin), and `communications/CURRENT_STATE.md`.

## The Iridium model, schema iridium-v2 (2026-07-09), the published four-bucket ARPU revenue case

The Iridium ARPU revenue case, previously deferred, is now published: four
billable-connection buckets (standard personal, premium terminal, IoT devices,
government), each a percentage mix of one pool anchored to fleet capacity
(`fleet_target x subscribers_per_satellite`), so every bucket scales with the
satellite count. Investor-set Sheet A blessed 2026-07-09. Built per the approved
`design_iridium_arpu_07_09`.

### Added

- **`IridiumArpuDials`** (`config.py`): a frozen, extra-forbid block nested as the
  optional `arpu` field on `IridiumDials` (None by default, so every bare-dials
  construction including the equality tripwire sees no buckets). Eight investor-set
  dials (four percentage mixes, four monthly prices) with Field bounds (the two
  people mixes strictly positive) and a model validator enforcing the four mixes
  sum to 100 within `ARPU_MIX_SUM_EPSILON`.
- **`derive_arpu_buckets`** with `IridiumArpuResult` / `IridiumArpuBucket`
  (`engine.py`): the pure pool algebra (`total_connections = people_capacity /
  people_share`; premium, IoT, and government counts round-half-up; standard the
  residual so the people identity is exact by construction), carried on the
  optional `IridiumResult.arpu` field and computed at the built fleet's people
  capacity. `arpu_stated_assumptions` shares the three posture strings between the
  assumptions output and the artifact block.
- **`revenue_arpu_buckets`** top-level block on the promoted artifact
  (`json_output.py`): per-bucket mix, price, count, and revenue, plus the pool
  total, the summed revenue, and the stated-assumption strings. Omitted (None) on
  the no-ARPU path.
- The eight ARPU named constants plus `ARPU_PRICE_CEILING_USD_MONTH`,
  `ARPU_MIX_TOTAL_PCT`, and `ARPU_MIX_SUM_EPSILON` (`constants.py`), eight
  `iridium.arpu.*` placeholder-flag entries (all False), and the populated `arpu`
  block on `scenarios/iridium.yaml` (Sheet A the default; Sheet B, the
  today's-device-ratio alternative, documented in the comments).
- Six new tests (frozen Sheet A, the exact people identity including an awkward
  mix, linear scaling at X vs 2X, validator rejection of a bad sheet, the None
  path, the IoT supersession); two updated (the promoted-JSON freeze to
  iridium-v2 and the assumptions accessor to the published case).

### Changed

- **Schema `iridium-v1` to `iridium-v2`**: the two inherited placeholder ARPU
  fields (`steady_state_revenue_arpu_musd`, `steady_state_gross_margin_arpu_pct`,
  computed from the cellular family's $50/month default) are removed from the
  promoted artifact's `TrajectorySummaryBlock`; the published `revenue_arpu_buckets`
  block is added. The engine still computes the inert $50 field on the shared
  trajectory (the cellular family reads it and the equality tripwire rides it), so
  it stays on the engine path, fenced with a comment at the artifact-removal site.
- **IoT supersession (one IoT truth)**: with the ARPU case on, the artifact's
  `iridium_physics.iot_devices` reports the mix-derived IoT bucket count (about
  51.7M at the baseline); the fixed passthrough dial reports only on the no-ARPU
  path. No artifact ever carries two IoT counts.
- Docs refreshed in tandem: `communications/assumptions.md` (eight dial rows, the
  register updates, the Sheet A/B subsection, the output anchors),
  `communications/conclusion.md` (the published four-number table and margin
  framing, the IoT and existing-book reconciliations, the pricing bullet), the root
  `README.md`, and `communications/CURRENT_STATE.md`.

## The Iridium model, schema iridium-v1 (2026-07-07/08), the communications model family

The first communications model family, built per the approved
`plan_iridium_model_07_03` in three phases and audited end to end (91 numbers
traced, zero numeric errors; four docstring citation ids corrected).

### Added

- **The Iridium model** in `src/communications/`: `IridiumDials` (spectrum 8.0
  MHz exclusive with the 10.5 coordinated variant, three device classes with
  spectral-efficiency tiers 0.65/2.0/2.5 bps/Hz, active rate 1.0 Mbps with the
  2.5 rich variant, concurrency 2.5/0.5 percent, aperture 25.0 m^2 with the
  no-fold caveat above the limit, IoT passthrough), the derivation spine
  (per-satellite capacity = spectrum x SE x 0.15 calibration x aperture
  factor; subscribers per satellite derived, not hard-coded), per-user peak and
  off-peak rates, `IridiumResult` on the trajectory, `iridium_assumptions()`,
  the documented `scenarios/iridium.yaml`, the promoted
  `communications/models/iridium/default.json` via the new
  `communications.json_output` (the DC promotion pattern), and 16 frozen tests
  including the equality tripwire (the Iridium baseline shares the
  High-Bandwidth Cellular Pure Play default trajectory, both coverage-bound at
  340).

### Changed

- **Descriptive model naming**: "the High-Bandwidth Cellular Pure Play model"
  (formerly Model A) and "the Iridium model" (formerly Model B) everywhere a
  reader sees them, including four frozen runtime strings with lockstep tests.
- **The cross-import guard** repoints its scenario check to
  `scenarios/iridium.yaml` and parametrizes per live source file (27 tests).

### Removed

- **The pre-rewrite comms tree** (29 files: 10 dead modules, 15 stale test
  files, the failing `comms_default.yaml`, the three old promoted artifacts
  under `communications/models/`, and the dangling `rklb-comms` console
  script), retired per the audit's import census. The whole tree is 548 tests
  green with the communications directory collecting cleanly.

## v8, Cycle 4 (2026-05-30), service-life cliff fix + 7-year flat-R scenario

Schema is unchanged (still v8); this is a bug fix plus a scenario change. The
promoted default (5-year life, flat R 1.50) is byte-identical: the same 268
living nodes and about $6.31B 2036 central revenue.

### Fixed

- **Service-life cliff now tracks the scenario.** The living-fleet cliff in
  `fleet.py` called `is_alive_at(year)` without the configured life, so it
  always used the hardcoded 5-year `SERVICE_LIFE_YEARS` even when a scenario set
  `fleet.service_life_years` to another value. Per-node cost already used the
  scenario value, so a 7-year scenario lowered cost but did not grow the fleet
  (the opposite of the real upside). `compute_fleet_year` now takes a required
  `service_life_years`, threaded from `config.fleet.service_life_years` in
  `engine.py`, and `is_alive_at`'s `service_life` is required (no silent
  default), so this class of bug cannot recur. The 5-year default is unchanged
  (5 equals the old constant).

### Changed

- **7-year upside scenario uses a flat 1.47 central R.** `upside_7yr.yaml`
  carried a leftover central taper (1.50 down to 1.40); it is now flat at 1.47,
  about 2% below the 5-year 1.50, the discount for locking a fixed long-term
  contract. R is kept (not removed) and stays a flat per-cohort multiple with no
  in-life decay curve, because a fixed contract fixes the price. The low / high
  brackets are the flat default 1.20 / 1.80.

### Added

- **Block-upgrade baseline comment.** `default.yaml`'s `mass_envelope_t: 12.5`
  is annotated as the always-on block-upgrade SSO baseline
  (RLDC-PAYLOAD-SSO-UPGRADE, NTR-007).
- **Two 7-year tests.** One asserts the 2036 living fleet grows beyond the
  default's 268 and matches the 7-year cohort window; the other asserts the flat
  1.47 central margin holds at about 31.97% across the trajectory.

## v8, Cycle 3 (2026-05-29), R band flattened (no taper)

Schema is unchanged from cycle 2 (still v8); this is a default-scenario and
constants change only.

### Changed

- **R band flattened, no taper.** The default central / low / high R bands are
  now flat at 1.50 / 1.20 / 1.80, replacing the cycle-2 central taper (1.50
  drifting to 1.40 by 2036). Revenue is locked per cohort at its launch-year R,
  so every cohort holds a constant 33.3% central gross margin across its
  five-year life. The in-code `RBand` defaults (`constants.py`) and the promoted
  default model now agree; previously only the promoted scenario was flat while
  the in-code default still tapered.
- **Golden parity reference re-recorded to the flat band.** The `test_parity.py`
  central per-node and fleet revenue references now reflect flat R. The 2036
  living-fleet central revenue reference moves from 5,942 MUSD (taper) to 6,305
  MUSD (about $6.31B), matching the promoted JSON and the public docs.

## v8, Cycle 2 (2026-05-20), fleet, volume, provenance

The cycle-2 rework. Cycle 1 delivered a GPU-first **per-node** calculator;
cycle 2 rebuilds the **fleet** layer on that chassis, makes the JSON
artifact fully self-describing, and corrects the radiator mass dial. The v8
schema is a **clean break** from v7, no back-compatibility shim (D24).

### Added

- **Fleet rollup.** `fleet.py`, a `Cohort` model (all nodes launched in a
  given calendar year, fixed launch-year gen-mix) and the living-fleet
  rollup under a 5-year service-life hard cliff (D1). The artifact now
  carries per-year launches, nodes deployed, living fleet, kW on orbit,
  PFLOPS on orbit, and fleet revenue / cost / gross profit / margin, cycle 1 reported one node only.
- **Launch cadence.** `cadence.py`, launches per year on a logistic ramp
  fit through the year-5/year-10 scenario anchors, and cadence-indexed
  launch cost on a log-linear curve. The promoted source trail now points
  to `SOURCE_INDEX` claims `NTR-009` and `NTR-010`.
- **Volume model.** `volume.py`, stowed solar + radiator volume vs the
  Neutron fairing. Volume is computed and surfaced as `volume_per_node_m3`,
  `volume_utilization_pct`, and a `binding_constraint` enum, but it does
  **not** gate N, mass is the sole binding constraint (D6).
- **R band (D18).** Revenue is `R × cost`, and R is now three trajectories
  (low / central / high) with year anchors and engine-side linear
  interpolation, replacing cycle-1's single `r_revenue_cost` scalar. Every
  revenue / profit / margin cell is emitted three times, one per band.
- **Inline provenance (D20).** `provenance.py`, a `ProvenanceCell`
  (`{value, unit, formula, formula_name, uses, sources, description}`)
  wraps every leaf numeric value in `physical.years` and `business.years`.
  The `FORMULAS` table is the authoritative `formula_name` lookup; the
  `cell()` factory resolves formula text from it.
- **Agent-first contract (D22).** `query_examples.py`, 12 worked `jq`
  queries embedded at `meta.query_examples`, so a cold agent can answer the
  common questions straight off the artifact.
- **Investor-locked enums.** `metadata` now carries `workload_type`
  (INFERENCE, D14), `operator_model` (B2B_DEDICATED_OPTICAL_RF, D15),
  `radiator_architecture` (SINGLE_FACE_CO_MOUNTED, D16), and
  `deployment_philosophy`.
- **Seven new V-rules (V11–V17).** `no_legacy_r_scalar`,
  `operator_r_consistency` (B2B operator floors the central base-year R at
  1.40), `provenance_formula_keys`, `cadence_monotonicity`,
  `volume_fits_horizon`, `fleet_cliff_consistency`, and
  `radiator_dial_matches_architecture`.
- **`constants.py`**, all fixed numeric dials lifted to documented
  `Final[T]` named constants (no bare numeric literals).
- **New scenario**, `scenarios/volume_stress.yaml`, an artificial fixture
  engineered to trip the `volume_fits_horizon` (V15) rule.
- **`CHANGELOG.md`**, this file.
- **Two-location output workflow.** `code/outputs/data_center/runs/` is
  git-ignored scratch, `data_center/models/space/default.json` holds the
  promoted default space JSON model, and `data_center/conclusion.md` holds the
  current human conclusion. The `rklb-value --promote` flag regenerates the
  selected scenario and writes promoted JSON artifacts. This resolves
  output-JSON timestamp non-determinism: scratch runs no longer churn git, and
  the promoted JSON is a deliberate snapshot. See the README "Run output vs.
  promoted model" section.
- **Draft Markdown rendering.** `conclusion.py` can render a noncanonical
  local Markdown draft from a typed model output, but promotion does not
  rewrite the reviewed static conclusion.

### Changed

- **Output schema v7 → v8.** Five top-level keys (`metadata`, `inputs`,
  `physical`, `business`, `meta`) replace the v7 eight-block shape (D21).
  `physical.years` and `business.years` are year-keyed maps of named
  provenance cells. The v7 `summary`, `decisions`, and `about` blocks are
  gone; their content is folded into `business.years` and `meta`.
- **Naming fix (D25).** The cycle-1 field `annual_rev_per_node_musd` was
  misleadingly named, it carried annual *profit*, not revenue. v8 splits
  it into explicit `revenue_annual_*`, `cost_annual_*`, and
  `gross_profit_annual_*` fields (each in low / central / high band
  variants).
- **Source-clean default.** The default scenario is explicitly named as a
  block-upgrade central case. `first_launch_year` clamps pre-launch years
  to zero without shifting the year-5/year-10 launch anchors, public launch
  and deployed-node counts are integer missions, and the obsolete
  `scurve_steepness` dial was removed.
- **Central R floor tightened.** The default central R band now decays
  1.50 → 1.40 rather than 1.50 → 1.30. Because margin is `(R - 1) / R`,
  that keeps the five-year operating plan above the 25% active-fleet
  gross-margin floor while still allowing modest pricing compression.
- **Radiator dial corrected (D17).** The post-Tjmax radiator dial was
  lifted from 0.007 to **0.012 t/kW** (R1 radiator research, the central
  of a 0.010–0.014 band). Heavier radiators from year 5 on mean fewer
  packages per node: at the cycle-1 kw-growth slope this dropped the
  default 2036 node from N = 34 / 534 kW (cycle 1) to N = 27 / ~424 kW.
  (That N = 27 figure is superseded by the `kw_growth_per_gen` correction
  below, see the next entry.)
- **`kw_growth_per_gen` corrected 0.30 → 0.20 (validation V-A).** The
  per-package electrical-power growth slope was set to 0.30/gen, but that
  was the historical *assembly-level* package-power growth rate, it grew
  that fast only because more packages were added per assembly. Applied as
  a *per-package* slope it double-counts; the research wiki supports
  ~20%/gen per package. Lighter packages from year 5 on let each node hold
  more of them: the default 2036 node rises from N = 27 to **N = 37 / ~422
  kW**, and 2036 fleet revenue/profit (central) move to ~$5.67B / ~$1.36B.
  Diagnosis came from the source-audit pass that reconciled package-level
  power growth against the research wiki.
- **Launch cost.** Now the cadence-indexed log-linear v7-archaeology curve
  (a function of launches per year), replacing cycle-1's simple two-anchor
  year-indexed ramp.
- **V5 and V10 re-targeted.** The v8 schema dropped `cost.compute_share`
  and the `decisions` block, so cycle-1 `V5 monotonic_compute_share` →
  `monotonic_pf_per_kw` and `V10 decisions_populated` →
  `data_dictionary_populated`. V1–V4, V6–V9 are the cycle-1 checks
  re-pointed at the v8 structure.
- **Input YAML schema v8.** Scenarios gain `metadata`, `cadence`, `fleet`,
  `volume`, `r_band`, and `launch_cost` blocks. Pydantic now rejects
  unknown fields (`extra="forbid"`). All five cycle-1 scenarios were
  migrated; `conservative.yaml`'s central base-year R is 1.40 (the B2B
  `operator_r_consistency` floor).
- **`generations.py` docstring** corrected to the canonical D-decision
  catalog (it had cited a defunct cycle-1 D-numbering scheme).

### Removed

- **`r_revenue_cost` scalar**, superseded by the R band (D18).
- **`revenue_decay_per_yr` dial**, revenue decay dropped entirely (D19).
- **v7 output blocks** `summary`, `decisions`, `about`, folded into the
  v8 structure or dropped (D21/D24).
- **The cycle-1 `annual_rev_per_node_musd` field**, renamed (D25).
- **`tdp_growth_per_gen`**, a dead config slope.
- **`generations.json`**, a stray non-scenario output artifact that no
  scenario or CLI command produced.
- No DCF / EV / PV / FCF, never present, reaffirmed out of scope (D23).

### Project notes

- The cycle-2 rework was executed in 8 phases from pre-cleanup through docs
  and QA.
- Test suite grew from 131 (cycle 1) to **308** tests.
- `mypy --strict src/`, `ruff check`, and `ruff format --check` are clean.

## v7, Cycle 1 (2026-05-20), GPU-first rework

The GPU-first rework. Deleted the NVL72-class **rack** abstraction
entirely and rebuilt the model around the GPU **package** (NVIDIA's "as
sold" unit). Each fiscal year picks a frontier generation off the 18-month
cadence and sizes N packages under Neutron's 12.5 t SSO mass envelope.
Per-node unit economics only, fleet size, launch cadence, FCF, and
valuation were declared out of scope. Schema v7, 10 V-rules, 131 tests.
