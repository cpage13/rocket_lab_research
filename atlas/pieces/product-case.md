# Product case

**Maturity.** Built, not yet promoted: the package, its shipped scenario and
its tests stand; its promoted artifact and the regeneration test that guards
it come with its first promotion. Checked against `part-b-product-case` at
9cd2b0d, 2026-10-13.

**Role.** The communications market view, its own model on the engineering
artifact (ADR 012): what the network the Iridium model builds would sell at
the investor's prices held flat, to four classes side by side: the small
terminal, the mounted terminal, minimal-packet IoT and data IoT. It sells no
phone class. It reads only the promoted Iridium artifact, as JSON, its schema
pinned and its SHA-256 recorded; nothing it computes feeds the engineering
model. Each class's customers come from a demand curve anchored on Iridium's
customers and ARPU today, in every drawn market and at the central market
(each market response at the middle of its range). A terminal sells up to its
seats; an IoT class is uncapped, its sales held to IoT's room by the usable
test, and no IoT count is ever set. The candidates hold every price at its
start price, so the pick chooses only each IoT class's usage: the highest
median revenue over the reported years among the candidates usable in at
least the robust floor's share of the drawn markets, or, when none is, the
most usable candidate, warned. The headline is the pick at the central
market; the spreads place it among the drawn markets.

**Serves.** Objective 1 (what the network would sell in years 5 to 10, read
beside the engineering case and never added to it), objective 2 (every input
an input cell with its claim and status, every number under the headline's
years a provenance cell, every published number named by a formula of the
product case's own catalog), objective 3 (the market machinery lives only
here and optimizes one thing) and objective 5 (the four classes side by
side).

**Edges.**
- In: `code/scenarios/product_case.yaml` (the prices, each class's usage path
  and IoT usage scales, the market's draws, seed and three ranges, the
  floors; data IoT's price is twice minimal-packet IoT's, never a setting, and
  a key that sets an IoT count is refused at load); the named constants in
  `constants.py` (the demand curve's anchors, the conventions, the defaults);
  and the Iridium artifact the scenario names (`engineering_artifact_path`),
  read once as bytes, hashed and parsed by `engineering_view_from_bytes`: per
  reported year the living fleet and its annual cost, each terminal's
  whole-fleet people, the phone class's useful beams and IoT's three rooms;
  once, each terminal's beam pool, rate and busy-hour share, the message and
  burst sizes, the airtime and the coverage floor year.
- Out: the product case's artifact (schema `product-case-v1`), written by
  `python -m product_case.json_output` (the promotion page). Its default
  path, communications/models/product_case/default.json, is reserved for the
  shipped scenario; its first promotion writes it. In code,
  `run_product_case(config, engineering)` returns a `ProductCaseRun`.
- It imports `common` alone (the shared-core page), never `communications` or
  `data_center`, and none of those three imports it (ADR 012).

**Modules** (`code/src/product_case/`):

| Module | Owns |
|---|---|
| `constants.py` | the enums (`ProductClass`, `ClassKind`, `UsableTest`, `PickBasis`, `RunState`, `SpreadField`), the demand curve's anchors (`DEMAND_ANCHORS`), the conventions, every `*_DEFAULT`, the two schema versions and the formula catalog (`FORMULA_CATALOG`) |
| `config.py` | the frozen `ProductCaseConfig`, `load_product_case_config`, and each input's cell spec (`SCENARIO_SPECS`, `CONSTANT_INPUTS`) |
| `engineering.py` | the one reader of the Iridium artifact (`engineering_view_from_bytes`) and the network it gives each reported year (`EngineeringView`, `build_engineering_view`) |
| `offers.py` | the choice grid (`choice_grid`) and each choice's prices, usage, service and per-device loads before any market (`choice_offers`) |
| `monte_carlo.py` | the markets (`draw_markets`, `central_market`), each choice over the draws and at the central market (`summarize_grid`, `outcome_in_market`), the fronts, the pick and its spreads (`fronts_of`, `pick_of`, `spreads_of`); the one product-case module that imports numpy |
| `checks.py` | believability, the run's warnings and the invariants |
| `engine.py` | the entry, `run_product_case` |
| `json_output.py` | the artifact (`ProductCaseArtifact`, `build_product_case_artifact`) and its command |

**Terms.** product case, engineering case, device class, minimal-packet IoT,
data IoT, margin, provenance cell (see `CONTEXT.md`). The method's own words
(the central market, a candidate, the usable test, a usage scale, the fronts,
the pick) are defined in the package docstring; they are not yet glossary
terms.

**State.**
- Not yet promoted: no default artifact exists until the first promotion.
- The method runs in nine steps, listed in the package docstring; steps 3 to 9
  carry their formulas in symbols and units in `monte_carlo.py`'s module
  docstring, and each formula is a catalog entry the artifact publishes
  (`meta.formulas`).
- What stops the usage: the robust floor, the median's peak, or the top of an
  IoT class's usage list, where the pick then sits on an upper usage edge,
  warned. The stated line on it names this run's pick (`assumptions`).
- IoT's room, which the usable test holds IoT's sales to, rides the phone
  class's useful beams, the beams lit over inhabited cells, so it counts no
  beam over oceans or empty land: a conservative basis, as in the Iridium
  artifact. The beams there are upside the case does not count; its stated
  line on the room says so.
- The artifact's blocks: `metadata` (the Iridium artifact read: its path,
  schema, stamp and SHA-256), `inputs` (every input an input cell: the
  scenario's, the constants' and the values read from the Iridium artifact),
  `network`, `choices` (every choice's summary), `fronts`, `pick`, `headline`
  (the pick at the central market: the market's three responses, then each
  reported year's four classes side by side and its totals, every number
  under `headline.years` a provenance cell but the year), `spreads` (each
  field over the pick's usable draws and over all draws, with the
  headline's rank; the all-draw basis's label,
  `spreads.all_draws_basis.label`), `meta` (the formulas, the validation
  results, the data dictionary, the worked queries and the source statuses)
  and `assumptions` (the stated lines, each built from the run). No total of
  customers is published: people and devices never add.
- The checks: believability per class and year, a warning that never
  refuses; the run's three warnings (an upper usage edge, the fallback, a
  central market unusable for the pick); and the invariants, which refuse
  the run (whole customers, terminals within their seats, revenue, the pick
  at the start prices and on the candidates' front, the headline's usable
  flag, every number finite).
- The same scenario and Iridium artifact give the same bytes on this
  platform (the package docstring says why, and where another platform could
  differ).

**Open.**
- **Not yet promoted.** The first promotion writes the artifact and adds the
  regeneration test (the committed artifact against a fresh promotion at its
  own stamp, naming both SHA-256s when the Iridium artifact moved).
- **Boxes to come**, each in `.agent/LATER.md` (local): the phone as its own
  product model (L3); every year FY2031 to FY2036, where the scenario reports
  four (L4); the terminals' upload in IoT's room, which waits on the
  terminal-uplink research (L5).
- The public documents do not yet tell the product case, and
  `communications/assumptions.md` has no product-case section yet (the
  conclusions page, Open).

**Tests.** `code/tests/product_case/`. The end-to-end specification is
`test_end_to_end.py`: a synthetic Iridium artifact and a small scenario
through the command to the artifact
(`test_every_choice_reads_in_one_market_and_the_headline_is_the_pick_there`,
`test_the_stated_assumptions_are_the_runs_line_by_line`,
`test_every_number_is_linked_to_its_formula`,
`test_a_central_market_unusable_for_the_pick_is_published_and_warned`,
`test_a_believability_flag_never_refuses`), with `test_json_output.py`
(`test_the_synthetic_case_promotes_and_a_second_promotion_is_byte_identical`,
`test_each_refusal_is_one_error_line_exit_1_and_no_file`). Round 3 of the
scratch exploration is reproduced on its own fixtures (`test_reproduction.py`).
The code defaults equal the shipped scenario
(`test_the_code_defaults_equal_the_shipped_scenario_file`); no IoT count is
ever set (`test_an_iot_count_in_the_scenario_is_refused_naming_the_field`,
`test_iot_customers_move_with_the_draw_and_the_year`); the package stays
apart (`test_the_product_case_imports_common_alone`,
`test_only_the_monte_carlo_imports_numpy`,
`test_comms_src_does_not_import_the_product_case`,
`test_common_modules_do_not_import_the_product_case`). Around them:
`test_config.py`, `test_engineering.py`, `test_offers.py`,
`test_monte_carlo.py`, `test_fronts_and_spreads.py`, `test_checks.py`,
`test_run_product_case.py` and `test_claim_citations.py`. Missed: no test
runs the shipped scenario through the Monte Carlo until the regeneration
test comes with the first promotion; no test checks that `data_center`
never imports the product case; no test ties the terminals' prices to the
Iridium scenario's (one price list, the assumptions page).

**If this changes, update here.** A module, a step of the method or the
pick's rule; the artifact's blocks or schema; the command or its refusals;
the Iridium fields it reads or the schema it pins
(`ENGINEERING_SCHEMA_VERSION`); the first promotion (Maturity, State, Open
and Tests).

**Drill down.** The `code/src/product_case/__init__.py` docstring (the nine
steps, what stops the usage, the investor's words, how to run it, where each
number goes, determinism) and each module's; ADRs 010, 011 and 012; the
source-ledger rows `COMM-722` to `COMM-726`; the product-case design,
`.agent/lifecycle/design_product_case_code_10_06.md` (local); round 3 of the
scratch exploration, `.agent/other/run_product_case_scratch_10_06/` (local).
