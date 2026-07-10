# Changelog

All notable changes to the `code/` model package: the `rklb-value` orbital
data-center valuation calculator and, from July 2026, the communications model
families. Versions track each output JSON **schema version** (data center: v8;
the Iridium model: iridium-v3).

## The Iridium model, schema iridium-v3 (2026-07-10), the cost-plus revenue case removed from the artifact

Per founder direction: the synthetic cost-plus revenue convention (price at
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

A same-day follow-on to the four-bucket ARPU case, per founder direction:
the cost model is simplified to founder-flat dials, the promoted ARPU block
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
  percent founder-range sweep, the premium price-tier reframe),
  `communications/assumptions.md` (the two founder-flat dial rows, register
  rows 13/28/34 plus the new row 42, the output anchors, the premium
  price-tier note), the root `README.md` (about $218M a year at a 33 percent
  margin), and `communications/CURRENT_STATE.md`.

## The Iridium model, schema iridium-v2 (2026-07-09), the published four-bucket ARPU revenue case

The Iridium ARPU revenue case, previously deferred, is now published: four
billable-connection buckets (standard personal, premium terminal, IoT devices,
government), each a percentage mix of one pool anchored to fleet capacity
(`fleet_target x subscribers_per_satellite`), so every bucket scales with the
satellite count. Founder-set Sheet A blessed 2026-07-09. Built per the approved
`design_iridium_arpu_07_09`.

### Added

- **`IridiumArpuDials`** (`config.py`): a frozen, extra-forbid block nested as the
  optional `arpu` field on `IridiumDials` (None by default, so every bare-dials
  construction including the equality tripwire sees no buckets). Eight founder-set
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
- **Founder-locked enums.** `metadata` now carries `workload_type`
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
