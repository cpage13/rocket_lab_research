# Communications model

**Maturity.** Stable for the Iridium model (a frozen suite, and a
regenerated artifact that matches the committed one). The High-Bandwidth
Cellular Pure Play family is on hold. The saturation module is planned, not
built. Checked against `main` at 7ff8bc3, 2026-10-03.

**Role.** Models a Neutron-launched communications constellation as model
families on one engine: the cadence ramp and the treadmill (build to the
fleet target, then replace each cohort that retires). The Iridium model, the
published family in the MSS lane, derives subscribers per satellite from
L-band physics (spectrum times the device class's spectral efficiency times
a calibration times an aperture factor, over each person's busy-hour load),
sizes the fleet between the coverage floor and the cap, and publishes the
four-bucket ARPU case at full sell-through, with its margin against the
built fleet's annualized cost.

**Serves.** Objective 1 (the all-in question for communications) and
objective 2 (`COMM-*` claims behind the defaults; the artifact states its
assumptions).

**Edges.**
- In: `code/scenarios/iridium.yaml` (the `iridium` block and its `arpu`
  sheet, plus overrides of shared dials: the all-in
  `comms_cadence.share_of_fleet`, a flat launch cost, a flat satellite cost)
  and its companion (the assumptions page); the defaults in `constants.py`;
  the cadence spine and cohort cliff from `code/src/common/`, never
  `data_center`.
- Out: `communications/models/iridium/default.json`, written by
  `python -m communications.json_output` (the promotion page);
  `run_comms_model` returns a `CommsTrajectory` of plain numbers, no
  provenance cells.

**Modules** (`code/src/communications/`):

| Module | Owns |
|---|---|
| `config.py` | the frozen `CommsConfig`, one block per family, cross-field validators, `load_comms_config` |
| `constants.py` | every default as a named constant, one section per family (to change one, the assumptions page's checklist) |
| `engine.py` | `run_comms_model`, the Iridium derivations, the ARPU buckets, the stated-assumption lines |
| `ground.py` | the cellular family's two-regime ground comparison (no production caller yet) |
| `json_output.py` | the Iridium artifact and its promotion command |

**Adding a family.** The steps are in `communications/design.md`; the map's
flow for a new application or family adds the thesis first.

**Terms.** the Iridium model, High-Bandwidth Cellular Pure Play model, the
three lanes, device class, frequency versus bandwidth, coverage floor,
saturation, treadmill, ARPU buckets (Sheet A), full sell-through,
all-in deployment, equality tripwire (see `CONTEXT.md`).

**State.**
- **Today:** the published baseline is the phone class at the coverage
  floor, sized to a subscriber target (the artifact's `binding_regime`
  reads coverage), so it is not yet the charter's maximum. The largest
  fleet the code runs is the unpromoted saturation companion, which raises
  the subscriber target until the inherited cap binds: an investor setting,
  not the spectrum's limit, which the saturation module will derive.
  Side-by-side device figures (rates, people per satellite) come from the
  conclusion's device section; per-class revenue waits for the saturation
  module (a checked table on the new defaults exists locally, unbuilt:
  quote none of it).
- One device class per run (`iridium.device_class`); the code's radio tiers
  are `small_terminal_class`, `terminal_class` (the mounted terminal) and
  `phone_class`. IoT is a device count and a revenue bucket, not a tier,
  and carries no load in sizing.
- One beam's data pool caps one person's rate; beam reuse multiplies the
  people served, not that rate.
- Operations cost is an explicit zero; the ARPU mix is held constant as the
  fleet grows.
- The cellular family is the config default (no `iridium` block), with no
  scenario file or artifact; the equality tripwire rides its defaults.

**Open.**
- **Approved, not yet built.** The saturation module (planned for
  `code/src/communications/`, not written) will derive how many satellites
  the owned spectrum can serve per device class, replacing the inherited
  cap, under the rules in the charter's saturation goal and the investor's
  new defaults: a 15.4 m^2 panel, 16 per launch with the block upgrade
  assumed, and per-class prices held flat. Until it lands, the old values,
  or numbers built on them, stay in `code/scenarios/iridium.yaml` and its
  companion `iridium_saturation.yaml`, the defaults they inherit from
  `code/src/communications/constants.py` (with their descriptions in
  `config.py`), the frozen Iridium suite, the artifact, the README's Iridium
  section, `communications/conclusion.md`,
  `communications/design.md`, `communications/CURRENT_STATE.md` and
  `communications/assumptions.md`. The work's status and the approved values
  are at the resume point named in `.agent/INDEX.md` (local).
- The cap, `coverage.max_fleet_satellites`, is an investor setting inherited
  from the cellular family; the public wording that calls it the spectrum's
  saturation is on the conclusions page.
- Every satellite counts as serving demand: ocean and empty-land time are
  not modeled (assumption 33 in `communications/assumptions.md`); the
  saturation design corrects this.
- Documented extensions: a per-year ARPU mix and revenue trajectory, and a
  researched operations line in place of the zero
  (`communications/CURRENT_STATE.md`).
- The phone class needs the band in standard phone chipsets (the stated
  ecosystem assumption, published in the artifact).
- The High-Bandwidth Cellular family is on hold, not concluded: keep it and
  its tripwire.
- The engine's field names and some docstrings say "gross margin" for a
  full-cost margin (for example `arpu_gross_margin_pct`), outside the
  data-center rename.
- The artifact's shortfall against ADR 002: the map, Open.

**Tests.** `code/tests/communications/`. The end-to-end specification is
`test_iridium_model.py`: the frozen baseline, the variants and edge cases,
the saturation companion,
`test_regenerated_default_artifact_matches_committed`, and the equality
tripwire `test_iridium_baseline_shares_hb_cellular_trajectory`. Around it:
`test_engine.py` (the treadmill), `test_subscribers.py` (fleet sizing and
the served base), `test_config.py`, `test_ground.py`,
`test_promotion_cli.py`, and `test_no_venture_cross_import.py`. Missed: no
test checks the `COMM-*` citations in `constants.py` against the source
ledger; the conclusion's numbers (the conclusions page).

**If this changes, update here.** A family added or retired; a derivation
step; the artifact's blocks; the saturation module landing (rewrite State
and Open).

**Drill down.** `communications/CURRENT_STATE.md`,
`communications/README.md`, `communications/conclusion.md`,
`communications/design.md`, `communications/assumptions.md`, the
`code/src/communications/__init__.py` and `engine.py` docstrings, and the
accepted saturation design, `.agent/lifecycle/design_09_28.md` (local).
