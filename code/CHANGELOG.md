# Changelog

All notable changes to the `rklb-value` orbital data-center valuation
calculator. Versions track the output JSON **schema version**.

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
