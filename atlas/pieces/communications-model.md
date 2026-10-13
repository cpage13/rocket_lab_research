# Communications model

**Maturity.** Built and stable for the Iridium model: a frozen suite, a
regenerated artifact that matches the committed one, and a committed
saturation curve its drift tests rebuild. The High-Bandwidth Cellular Pure
Play family is on hold. IoT as capacity (ADR 011) and the product case (ADR
012) are approved, not built. Checked against `main` at 1570350, 2026-10-12.

**Role.** Models a Neutron-launched communications constellation as model
families on one shared fleet-and-cost loop: each family hands the loop its
deployment rule (how many satellites a year adds, and how many of them
replace retiring cohorts) and builds its own record beside the shared one.
The Iridium model, the published family in the MSS lane, flies every comms
launch the cadence share allows, with no target and no cap; reads the people
of the small terminal, the mounted terminal and the phone class (its three
people classes) from the promoted saturation curve (the useful co-channel
beams a shell keeps lit over the places people live, computed once at the
25 m^2 reference panel with the band in full-time use) times the downlink
share and the panel factor, over each class's busy-hour load per person;
and sells every seat of each of the three at its flat price, side by side in
one run. Each class's column is the whole fleet sold to that class alone,
with its own margin against the year's whole-fleet annualized cost, so the
columns are never summed (ADR 006; the map's invariants). Beside the
cadence it reports each class's saturation number where its rows reach one,
its spectrum bound, never a cap. The saturation module computes the curve;
the cellular family runs the treadmill.

**Serves.** Objective 1 (the all-in question for communications) and
objective 2 (`COMM-*` claims behind the defaults; the artifact states its
assumptions).

**Edges.**
- In: `code/scenarios/iridium.yaml` (overrides of shared dials: the all-in
  `comms_cadence.share_of_fleet`, a flat launch cost,
  `satellite.satellites_per_launch` and a flat satellite build cost; and the
  `iridium` block: the held spectrum, the panel `aperture_m2`, the label,
  the `saturation` block with the downlink share and the curve's path, and
  the `arpu` block with the five monthly prices); the named constants in
  `constants.py` (each class's usage and spectral efficiency, the shell, the
  IoT lines' counts); the promoted curve, read and identity-checked; the
  cadence spine and cohort cliff from `code/src/common/`, never
  `data_center`.
- The curve's own inputs: the held spectrum, the named constants
  `SaturationInputs` reads (the assumptions page's Iridium checklist names
  them) and the shipped population grid
  `communications/data/ghs_pop_e2030_0p25deg.npz` (ADR 009). Its published
  texts (the method and stated limits among them) are code too, so an edit
  to one also re-promotes the curve (the same checklist, step 3).
- Out: `communications/models/iridium/saturation_curve.json`, written by
  `python -m communications.saturation` (a heavy run, the charter's Project
  rules), and `communications/models/iridium/default.json`, written by
  `python -m communications.json_output` (the promotion page). In code,
  `run_iridium_model(config, curve)` returns an `IridiumRun` (the shared
  fleet record and the Iridium record); the cellular entry,
  `run_comms_model(config)`, returns a `CellularRun` and has no command-line
  caller. All plain numbers, no provenance cells.

**Modules** (`code/src/communications/`):

| Module | Owns |
|---|---|
| `config.py` | the frozen `CommsConfig` and its blocks (the Iridium ones: `IridiumDials`, `SaturationDials`, `IridiumArpuDials`), cross-field validators, `load_comms_config` |
| `constants.py` | every default and named constant, one section per family (to change one, the assumptions page's checklist) |
| `engine.py` | the shared fleet-and-cost loop (`run_fleet_loop`, `DeploymentRule`, `FleetTrajectory`), `margin_pct`, and the cellular family (`run_comms_model`, the treadmill) |
| `iridium.py` | the Iridium family: `iridium_dials_of`, `full_cadence_rule`, `run_iridium_model`, its record, the readings, the IoT check, the marginal intervals and the stated assumptions (`_assumptions`) |
| `saturation.py` | the saturation curve's computation and its command; the one module that imports numpy (ADR 010) |
| `saturation_curve.py` | the curve's contract: `SaturationInputs`, `SaturationCurve`, `load_saturation_curve`, the identity check `check_curve_matches`, and the readings at any fleet |
| `ground.py` | the cellular family's two-regime ground comparison (no production caller yet) |
| `json_output.py` | the Iridium artifact and its promotion command |

**Adding a family.** A family module whose deployment rule runs on the
shared loop and whose record sits beside the shared one (the map's flow for
a new application or family adds the thesis first);
`communications/design.md` gives the steps as they stood before the
saturation work, until its rewrite. A market view is a separate model on
the engineering artifact (ADR 012).

**Terms.** the Iridium model, High-Bandwidth Cellular Pure Play model, the
three lanes, device class, frequency versus bandwidth, coverage floor,
saturation, saturation number, saturation curve, useful beams, maximum use,
ocean factor, panel factor, downlink share, readings, marginal interval,
IoT books, treadmill, full sell-through, all-in deployment, equality
tripwire, engineering case, product case (see `CONTEXT.md`).

**State.**
- The published artifact carries the three people classes side by side
  (the small terminal, the mounted terminal, the phone class), each column
  the whole fleet sold to that class alone (Role): each class's price,
  usage and physics, its markers from the curve and the limit that binds at
  the horizon's end, and per year the shared fleet and cost beside each
  class's people, revenue and own margin; then the readings at four fleets
  (the coverage floor, the retired cap kept for comparison, the horizon-end
  reach and the steady state), the IoT check, each class's marginal
  intervals and the stated assumptions. The headline reads are on the
  promotion page.
- The fleet is the cadence's: every comms launch the share allows times the
  satellites per launch, under the cohort cliff. The coverage floor, pinned
  at 340 on the Iridium path, gates every sale: nothing is sold in a year
  whose living fleet is below it.
- People are the curve's capacity at the year's living fleet, times the
  downlink share and the panel factor, over each class's busy-hour load;
  beams over ocean and empty land carry no one. Each class's usage and
  spectral efficiency are named constants, not settings, and the curve is
  computed at them (the assumptions page's Iridium checklist).
- IoT is still ADR 007's two IoT lines (`fixed_books`), each its own revenue
  line outside every people class's margin, until ADR 011's code replaces
  them with IoT's capacity. Government is left out of revenue.
- One beam's data pool caps one person's rate; beam reuse multiplies the
  people served, not that rate.
- Operations cost is an explicit zero, stated in the artifact.
- The cellular family is the config default (no `iridium` block), with no
  scenario file or artifact; the equality tripwire runs it beside the
  Iridium family.

**Open.**
- **Approved, not built.** IoT as capacity in the engineering model, which
  then carries no IoT count, price or revenue (ADR 011), and the product
  case as its own model on this model's artifact (ADR 012). Each lands with
  its code, its pages and its guards; until then the artifact is as State
  says.
- **The public documents.** The root README's Iridium section and the
  folder's documents still describe the model before the saturation work
  (the conclusions page, Open); until their rewrite, the code, the promoted
  JSON and this page are the truth.
- Each class's usage is a named constant the curve is computed at, so a
  seat's service is the same in every year while each added satellite
  reaches fewer people and the fleet's cost a seat rises. The investor ruled
  (2026-10-12) that the conclusions state this plainly beside each class's
  revenue rising every year, and that the product case (ADR 012) carries
  the service that improves; both wait for the documents' rewrite and the
  product case's code.
- Whether the small and mounted terminals' upload carries every seat is an
  open local research wiki, `.agent/other/wiki_terminal_uplink/` (local).
- The phone class needs the band in standard phone chipsets (the stated
  ecosystem assumption, published in the artifact).
- A researched operations line in place of the zero is a documented
  extension.
- The High-Bandwidth Cellular family is on hold, not concluded: keep it and
  its tripwire.
- The cellular record's field names say "gross margin" for a full-cost
  margin (`arpu_gross_margin_pct`, `cost_plus_gross_margin_pct`), outside
  the data-center rename.
- The artifacts' shortfall against ADR 002: the map, Open.

**Tests.** `code/tests/communications/`. The end-to-end specifications are
`test_iridium_model.py` (the frozen run at the shipped scenario: fleets,
costs, every class's people, revenue and margins, the readings, the IoT
lines and the intervals; `test_regenerated_default_artifact_matches_committed`;
and the equality tripwire
`test_iridium_and_cellular_runs_share_the_fleet_and_cost_records`) and
`test_saturation.py` (the curve on synthetic worlds and on the real grid at
a coarse setting, the drift tests on the committed curve, the command's
refusals, numpy's confinement). Around them: `test_engine.py` (the shared
loop and the treadmill), `test_subscribers.py` (the cellular sizing and
served base), `test_config.py`, `test_ground.py`, `test_promotion_cli.py`,
`test_no_venture_cross_import.py` and `test_claim_citations.py` (every
`COMM-*` claim ID the communications code cites has its source-ledger
row). Missed: the suite never runs the
saturation command in full (the drift tests rebuild the committed curve's
check rows); the conclusion's numbers (the conclusions page).

**If this changes, update here.** A family added or retired; the shared
loop or a deployment rule; the curve's inputs, contract or command; the
artifact's blocks; IoT as capacity or the product case landing (rewrite
State and Open).

**Drill down.** The `code/src/communications/__init__.py` docstring and
each module's (`iridium.py`, `saturation.py` and `saturation_curve.py`
above all); ADRs 005 to 012; the artifact's `assumptions` and
`saturation.limits` by `jq`; the research note
`research/direct_communication/iridium_saturation_module.md`; the accepted
saturation design, `.agent/lifecycle/design_09_28.md` (local), and its
strategy, `.agent/lifecycle/strategy_09_29.md` (local), which the code
cites by name; the product-case design,
`.agent/lifecycle/design_product_case_code_10_06.md` (local).
