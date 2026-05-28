# Orbital Data-Center Venture — Fleet Projection, 2026–2036

> **Stale generated-output note (2026-05-28).** This file is retained only as
> historical research context for an older calculator cycle. It is not the
> current generated model output, not the reviewed static conclusion, and not a
> public claim source. Current promoted model outputs live under
> `data_center/models/`, and current reviewed prose lives under
> `data_center/conclusion.md`.

> **Path note (2026-05-25).** This projection was first drafted against an
> earlier calculator location. The current Python generator lives under `code/`,
> and promoted default space-model output lives at
> `data_center/models/space/default.json`.

*A calculator output, not a forecast. Generated from the `code/` Python
generator (GPU-first, schema v8, cycle 2),
default / central-case scenario. Date: 2026-05-20.*

This is the year-by-year **fleet economic projection** for the Rocket Lab
orbital AI-inference data-center venture, valued **standalone**. Every
number historically traced to a documented dial in the retired
`calculator/scenarios/default.yaml` path and, in that cycle's JSON artifact, to
a typed provenance cell carrying its formula, inputs, and sources. Do not use
the retired path as current navigation.

> **Historical path warning.** The paragraph above describes the original
> generator contract for this artifact. For current work, read
> `docs/agent-guide.md`, `code/README.md`, and the promoted JSON query examples
> before quoting or regenerating values.

## What this projects (read this first)

Cycle 1's calculator answered a deliberately narrow question — the
unit economics of **one node**, year by year. It did not model fleet size,
launch cadence, or cohorts.

Cycle 2 rebuilds the fleet layer on the GPU-first chassis. The calculator
now answers:

> *What is the year-by-year economic trajectory of the orbital inference
> fleet — per-node physical sizing, and per-year fleet revenue, profit, and
> margin — over a 10-year horizon?*

It does this by vintaging each calendar year's launches into a **cohort**
with a fixed launch-year gen-mix, rolling the **living fleet** up under a
5-year service-life cliff (D1), and pricing revenue as an **R band** — three
trajectories (low / central / high) rather than a single ratio (D18).

What it still does **not** compute (D23): DCF, enterprise value, present
value, terminal value, free cash flow, depreciation, R&D ramp, or peak
capital draw. Those higher-order valuation layers sit above this one. The
calculator produces the fleet's *operating economics* — revenue, cost,
profit, margin — as a deterministic, typed, self-validating artifact. It is
not a venture valuation.

---

## THE NUMBERS — central case (default scenario)

The default scenario locks the gospel constants at the cycle-2 strategy's
central values: 12.5 t SSO mass envelope, 2.5 t fixed node mass, 5-year
service life, the v7-archaeology launch-cadence ramp, bus base $8M
flattening at year 5, and the Tjmax lift (radiator t/kW: 0.013 → **0.012**
at year 5 — cycle-2 D17 lifted the post-lift dial from 0.007). The R band's
central trajectory runs **1.50 (2026) → 1.30 (2036)** over six anchors; the
low band runs 1.20 → 1.15 and the high band 1.80 → 1.65.

### Per-year — frontier generation and per-node physical sizing

| FY | Frontier generation | N | Node kW | Mass util | PFLOPS/node | Vol util |
|---:|---|---:|---:|---:|---:|---:|
| 2026 | B300/GB300     | 146 | 299 | 99.5 % |  2,190 | 6.3 % |
| 2027 | Rubin VR200    | 117 | 304 | 99.9 % |  3,978 | 6.3 % |
| 2028 | Rubin Ultra    |  81 | 337 | 99.1 % |  4,212 | 6.4 % |
| 2029 | Feynman        |  70 | 385 | 99.5 % |  7,000 | 6.4 % |
| 2030 | Feynman        |  70 | 385 | 99.5 % |  7,000 | 6.4 % |
| 2031 | Gen+1 (extrap) |  57 | 407 | 99.0 % |  9,262 | 6.4 % |
| 2032 | Gen+2 (extrap) |  45 | 418 | 99.8 % | 11,882 | 6.4 % |
| 2033 | Gen+2 (extrap) |  45 | 418 | 99.8 % | 11,882 | 6.4 % |
| 2034 | Gen+3 (extrap) |  35 | 422 | 99.8 % | 15,018 | 6.4 % |
| 2035 | Gen+4 (extrap) |  27 | 424 | 99.4 % | 18,826 | 6.4 % |
| 2036 | Gen+4 (extrap) |  27 | 424 | 99.4 % | 18,826 | 6.4 % |

**Reading.** N falls (146 → 27) as the frontier package gets heavier; node
power climbs to ~424 kW because per-package compute outruns per-package
power. Mass utilization sits at ~99% every year — N is mass-bound by
construction (D6). Volume utilization stays near 6% — the stowed solar +
radiator volume never approaches the Neutron fairing, so volume never binds.
PFLOPS per node grows ~8.6× across the horizon.

> **Cycle-2 vs cycle-1 note.** Cycle-1's default 2036 node was N = 34 at
> 534 kW. The cycle-2 radiator-dial correction (0.007 → 0.012 t/kW
> post-Tjmax, D17) makes radiators heavier from year 5 on, so fewer
> packages fit: 2036 N drops to 27 and node kW to ~424. This is an
> intentional, founder-accepted correction grounded in R1 radiator
> research — not a regression.

### Per-year — per-node economics ($M, central R band)

| FY | Annual cost/node | Annual revenue/node | Annual profit/node |
|---:|---:|---:|---:|
| 2026 | 13.43 | 20.14 | 6.71 |
| 2027 | 13.05 | 19.25 | 6.20 |
| 2028 | 14.82 | 21.49 | 6.67 |
| 2029 | 15.77 | 22.47 | 6.70 |
| 2030 | 15.32 | 21.45 | 6.13 |
| 2031 | 15.43 | 21.22 | 5.78 |
| 2032 | 15.32 | 20.69 | 5.36 |
| 2033 | 14.98 | 20.00 | 5.02 |
| 2034 | 14.79 | 19.53 | 4.73 |
| 2035 | 14.57 | 19.09 | 4.51 |
| 2036 | 14.38 | 18.70 | 4.31 |

Annual cost per node is `node_total / service_life` and stays in a tight
$13–16M band — the GPU-first model predicts roughly *constant* node
capital because the mass envelope is fixed. Per-node revenue rides cost at
the central R band; per-node profit *compresses* over the horizon because
the central R band itself decays 1.50 → 1.30.

### Per-year — living-fleet rollup (central R band)

| FY | Launches | Living fleet | Fleet revenue $M | Fleet profit $M | Margin % |
|---:|---:|---:|---:|---:|---:|
| 2026 |  0.98 |   1 |     20 |      6 | 33.3 |
| 2027 |  1.61 |   3 |     58 |     19 | 32.5 |
| 2028 |  2.94 |   6 |    123 |     39 | 31.7 |
| 2029 |  4.91 |  11 |    235 |     72 | 30.8 |
| 2030 |  8.41 |  19 |    407 |    121 | 29.8 |
| 2031 | 13.93 |  32 |    684 |    196 | 28.6 |
| 2032 | 22.74 |  53 |  1,121 |    307 | 27.3 |
| 2033 | 35.41 |  85 |  1,757 |    462 | 26.3 |
| 2034 | 52.34 | 132 |  2,660 |    675 | 25.3 |
| 2035 | 72.21 | 196 |  3,864 |    951 | 24.6 |
| 2036 | 92.53 | 275 |  5,306 |  1,272 | 23.9 |

**Reading.** Launches per year ramp on the v7-archaeology logistic curve;
the living fleet is the sum of cohorts in the trailing 5-year window. By
2036 the fleet is **275 living nodes** carrying ~116,200 kW on orbit and
~4.58M PFLOPS, generating **~$5.3B fleet revenue** (central band) at a
23.9% gross margin. The central margin compresses over the horizon because
the central R band decays 1.50 → 1.30; the fleet's profit still grows in
absolute terms (6 → 1,272 $M) as the living fleet expands.

### The R band — 2036 fleet revenue spread

Revenue is `R × cost`, and R is a band. At 2036 the fleet's annual revenue
spans:

| Band | 2036 fleet revenue $M | Implied 2036 R |
|---|---:|---:|
| low     | 4,640 | 1.15 |
| central | 5,306 | 1.30 |
| high    | 6,688 | 1.65 |

Cumulative fleet revenue 2026→2036 (central band) is **~$16.2B**. The band
brackets the genuine uncertainty in the revenue-to-cost ratio; the central
case is the planning number, the low and high are the judged downside and
upside.

---

## The five scenarios — headline trajectories

Each row is the 2036 fleet headline for one shipped scenario (see
`calculator/scenarios/`). All five share the same physics, the same
generation trajectory, and the same mass-bound N — the dials that move the
fleet headline are the **mass envelope**, the **R band**, and the **service
life**.

| Scenario | Dials | 2036 fleet revenue $M (central) | 2036 margin % | Cumulative revenue to 2036 $M |
|---|---|---:|---:|---:|
| `default` | 12.5 t SSO, central R band, 5-yr life | 5,306 | 23.9 | 16,239 |
| `conservative` | 11 t SSO, low R band (central 1.40 → 1.15), 5-yr life | 7,706 | 15.5 | 24,049 |
| `ambitious` | 13 t SSO, high R band, 5-yr life | 4,732 | 23.9 | 14,526 |
| `with_premium` | 12.5 t SSO, premium R band, 5-yr life | 6,135 | 34.2 | 18,705 |
| `upside_7yr` | 12.5 t SSO, central R band, 7-yr service life | 3,790 | 23.9 | 11,599 |

**Reading.** `conservative` has the *highest* fleet revenue despite the
lowest margin — its 11 t envelope and lower-R band cut per-node profit, but
the same cadence still vintages a 275-node living fleet, and a thinner
margin on a similar cost base produces a larger gross revenue figure. The
margin column is the truer read of how each scenario's R band differs:
`with_premium`'s premium R lands a 34.2% margin; `conservative`'s low band
compresses to 15.5%. `upside_7yr` lengthens the amortisation window, which
lowers the per-year fleet revenue rate. None of these scenarios claims an
enterprise value — by design.

---

## What the validation block says

The engine runs **17 V-rules** on every artifact (see
`calculator/src/rklb_value/validation.py`). On the default scenario all 17
pass:

```sh
$ jq '.meta.validation.rules | length' output/default.json
17

$ jq '[.meta.validation.rules[] | .pass_check] | unique' output/default.json
[true]

$ jq '.meta.validation.rules[] | select(.pass_check == false)' output/default.json
# (nothing — every rule passes)
```

V1–V10 are the cycle-1 checks re-pointed at the v8 structure (two were
re-targeted to v8-meaningful invariants when the v8 schema dropped their
cycle-1 subject). V11–V17 are cycle-2 additions: `no_legacy_r_scalar`
(R is a band, not a scalar), `operator_r_consistency` (B2B operator floors
the central base-year R at 1.40), `provenance_formula_keys` (every cell's
`formula_name` exists in the `FORMULAS` table), `cadence_monotonicity`,
`volume_fits_horizon` (no year is *volume-only* bound — D6), `fleet_cliff_
consistency` (the living fleet equals the cohort-cliff sum), and
`radiator_dial_matches_architecture`.

All five normal scenarios pass all 17 rules. The `volume_stress.yaml`
fixture is engineered to fail `volume_fits_horizon` on purpose — it shrinks
the Neutron fairing to 5.0 m³ and the mass envelope to 11.0 t so a few
years become volume-only bound. It is an artificial V15-trigger fixture,
never a real projection.

---

## Estimates vs sourced facts

The load-bearing inputs are genuinely uncertain — sweep them:

* **Per-generation package values (`$/pkg`, `kW/pkg`, `kg/pkg`, `PF/pkg`,
  `die_count`)** — B200/B300/Rubin/Rubin Ultra are *sourced* from public
  NVIDIA datasheets and `ai_hardware/` research; Feynman is an *estimate*;
  Gen+1..Gen+5 are *extrapolations* on the `GenerationSlopes`. Each
  generation's `source` field tags its sourcing class.
* **The R band** — the central trajectory (1.50 → 1.30) is the planning
  case; the low (1.20 → 1.15) and high (1.80 → 1.65) bands are the judged
  downside / upside. The "what is the right R?" question is genuinely open
  and the highest-sensitivity dial. R > 1 is non-negotiable; the
  `operator_r_consistency` rule additionally floors the B2B central
  base-year R at 1.40.
* **5-year service life** — a founder directive (D1), a hard cliff.
  `upside_7yr.yaml` sweeps it to 7.
* **Mass envelope (12.5 t SSO)** — Neutron block-upgrade payload, *sourced*
  from `rocket_lab/`. The 11 t (`conservative`) and 13 t (`ambitious`)
  variants bracket it.
* **Launch cadence and launch cost** — the logistic ramp and the
  cadence-indexed log-linear cost curve are *v7 archaeology* (commit
  `8fdc210`), an *estimate*, not Rocket Lab-published. Predicting cadence
  five-plus years out is the cadence-equivalent of the rack-prediction
  problem; the cadence dials sweep it.
* **Radiator dial — 0.012 t/kW post-Tjmax** (D17) — *sourced estimate*,
  the central of R1's 0.010–0.014 band. Cycle 2 lifted it from cycle-1's
  0.007. The Tjmax-lift step at year 5 (D11) is an *assumed engineering
  milestone*; if it slips, every year past 5 carries the heavier radiator.
* **Post-Feynman growth slopes** — *extrapolation*. Each slope is defended
  individually in the research wiki; the *compound* extrapolation past
  Gen+3 is the most uncertain part of the model.

---

## How to regenerate

```sh
cd code

# the projection above (default scenario)
uv run rklb-value scenarios/default.yaml --json > output/default.json

# promote the default public JSON artifacts
uv run rklb-value --promote

# the other four scenarios + the V15 stress fixture
uv run rklb-value scenarios/conservative.yaml  --json > output/conservative.json
uv run rklb-value scenarios/ambitious.yaml     --json > output/ambitious.json
uv run rklb-value scenarios/with_premium.yaml  --json > output/with_premium.json
uv run rklb-value scenarios/upside_7yr.yaml    --json > output/upside_7yr.json
uv run rklb-value scenarios/volume_stress.yaml --json > output/volume_stress.json
uv run rklb-value scenarios/generations.yaml   --json > output/generations.json

# the input schema
uv run rklb-value --input-schema > output/input_schema.json

# the test suite
uv run pytest
```

All six scenarios regenerate at exit 0; mypy --strict src/ and ruff are
clean. The artifact carries a `meta.data_dictionary` block built by Pydantic
introspection (no parallel glossary), a `meta.validation` block with the
17 V-rule results, and a `meta.query_examples` block of 12 worked `jq`
queries — the cold-reader contract that lets an agent answer the common
questions straight off the artifact.
