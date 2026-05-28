# Ground Infrastructure And Electricity Cost Basis, 2036 Cohort

**Status:** draft research
**Date:** 2026-05-28
**Scope:** source-backed ground infrastructure and electricity basis for the
2036 deployed-year cohort in the Rocket Lab Research data-center investigation.
**Research-wiki process note:** this document is the canonical research output
for this focused pass. It is cataloged in `LIBRARY.md` and `RESEARCH_TRACKER.md`;
`SOURCE_INDEX.md` carries per-input ground source-status entries, and the
promoted ground JSON points to those entries.

## Central Finding

The current ground reference is not a mystery number. It is a mechanically
simple five-year reference for the same 2036 deployed-year cohort used by the
promoted space model: `90` nodes, `3,330` GPU packages, `37.978 MW` of IT load,
and a `5` year comparison period. Those values come from
`data_center/models/ground/default.json` paths `.anchor.nodes`,
`.anchor.gpu_packages`, `.anchor.kw`, and `.anchor.service_life_years`, which in
turn point back to `data_center/models/space/default.json` paths
`.business.years."2036".nodes_deployed_this_year`,
`.physical.years."2036".gpus_per_node`,
`.physical.years."2036".kw_per_node`, and
`.inputs.config.fleet.service_life_years`.

The promoted ground JSON computes a five-year ground total of about `$3.68B`
and an orbital build-plus-launch reference of about `$7.05B`, so the current
orbital/ground ratio is about `1.92x`. All three values are derived directly
from `data_center/models/ground/default.json` paths
`.ground.total_five_year_cost.value`,
`.orbital_reference.five_year_cost_view.value`, and
`.comparison.orbit_to_ground_ratio.value`.

The delicate public interpretation is:

- The current model supports "same broad order of magnitude" under the current
  scenario.
- It does not support "orbital is cheaper than ground."
- If both sides target comparable margins and throughput, the current default
  implies an orbital token-price requirement about `92%` above the ground
  reference (the `1.92x` ratio minus one).
- The five-year electricity bill is only about `$150M`, or `4.1%` of the
  full ground reference. Electricity is not the main offset.
- The sensitive orbital cost lines are solar and radiator: about `$1.52B` each,
  `$3.04B` combined, from `.orbital_reference.component_costs[]` in the ground
  JSON.

The current repaired baseline is source status plus arithmetic. All nine ground
input cells now carry per-input source IDs in the promoted JSON instead of one
generic `RLDC-GROUND-COST-BASIS` claim. The model distinguishes
`sourced_estimate` inputs from explicit `scenario` dials and keeps uncertainty
visible without treating the ground case as an empty slot.

## How To Read The Promoted JSON

Use the ground JSON for the comparison result and the space JSON for the 2036
cohort source path.

| Question | JSON path | Current value | Status to use in public prose |
|---|---|---:|---|
| Anchor year | `data_center/models/ground/default.json` `.anchor.year` | `2036` | `derived_estimate` model anchor |
| Anchor basis | `.anchor.basis` | `deployed_this_year` | comparison design choice |
| Nodes deployed | `.anchor.nodes` | `90` | `derived_estimate` from space model |
| GPU packages | `.anchor.gpu_packages` | `3330` | `derived_estimate` from `90 * 37` |
| IT load | `.anchor.kw` | `~37,978 kW` (≈37.98 MW) | `derived_estimate` from `90 * 421.98 kW` |
| Comparison period | `.anchor.service_life_years` and `.inputs.assumption_index["inputs.config.comparison_period_years"].value` | `5 years` | `scenario`, aligned to service life |
| Ground five-year total | `.ground.total_five_year_cost.value` | `~3,677 MUSD` (≈$3.68B) | `derived_estimate` from source-linked and scenario inputs |
| Orbital five-year reference | `.orbital_reference.five_year_cost_view.value` | `~7,048 MUSD` (≈$7.05B) | `derived_estimate` from space model cost lines |
| Ground/orbit ratio | `.comparison.ground_to_orbit_ratio.value` | `~0.52` | `derived_estimate` |
| Orbit/ground ratio | `.comparison.orbit_to_ground_ratio.value` | `~1.92` | `derived_estimate` |
| Conclusion label | `.comparison.conclusion_label` | `same_order_of_magnitude` | interpretation label, not a parity claim |
| Ground components | `.ground.component_costs[]` | listed below | mixed status |
| Orbital components | `.orbital_reference.component_costs[]` | listed below | `derived_estimate` |

Ground component values from `.ground.component_costs[]`:

| Component | Path selector | Current value | Current JSON source status |
|---|---|---:|---|
| GPU/package acquisition | `select(.name == "gpu_package_acquisition").cost.value` | `~2,140 MUSD` | `derived_estimate` |
| Facility shell / fit-out | `select(.name == "facility_shell_fitout").cost.value` | `~684 MUSD` | `derived_estimate` |
| Racked power and networking | `select(.name == "racked_power_networking").cost.value` | `266.4 MUSD` | `derived_estimate` |
| Five-year energy | `select(.name == "energy").cost.value` | `~150 MUSD` | `derived_estimate` |
| Cooling infrastructure | `select(.name == "cooling").cost.value` | `~152 MUSD` | `derived_estimate` |
| Operations, maintenance, and labor | `select(.name == "operations_maintenance_labor").cost.value` | `~285 MUSD` | `derived_estimate` |

Orbital reference values from `.orbital_reference.component_costs[]`:

| Component | Current value | Source status |
|---|---:|---|
| Compute hardware | `~2,140 MUSD` | `derived_estimate` |
| Bus/platform | `~618 MUSD` | `derived_estimate` |
| Solar/power | `~1,519 MUSD` | `derived_estimate` |
| Radiator/thermal | `~1,519 MUSD` | `derived_estimate` |
| Launch allocation | `~1,251 MUSD` | `derived_estimate` |

## Reproducing These Numbers

Every value above is read from the promoted JSON, not entered by hand. The
intent here is traceability: each command below regenerates a slice of the
numbers from the repository root, and the raw output simply reproduces the
rounded tables shown earlier.

The comparison summary (anchor, ground and orbital totals, ratios, and the
component breakdowns) comes from one query:

```sh
jq '{anchor: .anchor, ground_total_musd: .ground.total_five_year_cost.value, orbital_total_musd: .orbital_reference.five_year_cost_view.value, ground_to_orbit: .comparison.ground_to_orbit_ratio.value, orbit_to_ground: .comparison.orbit_to_ground_ratio.value, ground_components: [.ground.component_costs[] | {name, value_musd: .cost.value}], orbital_components: [.orbital_reference.component_costs[] | {name, value_musd: .cost.value}]}' data_center/models/ground/default.json
```

The nine ground input dials, with units and source status, come from
`.inputs.assumption_index`. They are tabulated under
[Input Audit And Implemented Source Statuses](#input-audit-and-implemented-source-statuses):

```sh
jq -r '.inputs.assumption_index | to_entries[] | [.key, (.value.value|tostring), (.value.unit // ""), .value.source_status] | @tsv' data_center/models/ground/default.json
```

The per-node 2036 orbital cost breakdown that rolls up into the orbital
reference comes from the space model. Rounded, it is:

| Per-node line (2036) | Value |
|---|---:|
| Compute | `~23.78 MUSD` |
| Bus | `~6.87 MUSD` |
| Solar | `~16.88 MUSD` |
| Radiator | `~16.88 MUSD` |
| Launch | `~13.90 MUSD` |
| Node total | `~78.31 MUSD` |

```sh
jq '{nodes: .business.years."2036".nodes_deployed_this_year.value, packages_per_node: .physical.years."2036".gpus_per_node.value, kw_per_node: .physical.years."2036".kw_per_node.value, cost_breakdown_per_node: .physical.years."2036".cost_breakdown}' data_center/models/space/default.json
```

## Current Ground Math

The current model formulas live in `code/src/data_center/ground.py`. The
relevant formulas are:

```text
anchor.gpu_packages = nodes_deployed_this_year * gpus_per_node
anchor.kw = nodes_deployed_this_year * kw_per_node
package_cost_musd = compute_cost_per_node / gpus_per_node
ground GPU acquisition = anchor.gpu_packages * package_cost_musd * gpu_package_cost_multiplier
facility cost = anchor.kw / 1000 * facility_shell_fitout_musd_per_mw
racked power/network cost = anchor.gpu_packages * racked_power_network_musd_per_gpu_package
energy cost = anchor.kw * pue * utilization * 8760 * years / 1000 * USD_per_MWh / 1000000
cooling cost = anchor.kw / 1000 * cooling_cost_musd_per_mw
operations cost = anchor.kw / 1000 * operations_maintenance_musd_per_mw_year * years
```

Using the promoted model:

| Calculation | Result | Source |
|---|---:|---|
| `90 * 37` packages | `3,330` | ground JSON `.anchor` and space JSON 2036 paths |
| `90 * 421.98 kW` | `~37.98 MW` | ground JSON `.anchor.kw` |
| `23.78 MUSD / 37` | `~0.643 MUSD/package` | space JSON 2036 compute and package paths |
| `3,330 * 0.643 MUSD` | `~2,140 MUSD` | ground JSON `.ground.component_costs[]` |
| `37.98 MW * 18 MUSD/MW` | `~684 MUSD` | ground JSON and ground YAML |
| `3,330 * 0.08 MUSD/package` | `266.4 MUSD` | ground JSON and ground YAML |
| `37,978 kW * 1.25 * 0.85 * 8760 * 5 / 1000 * 85 / 1e6` | `~150 MUSD` | ground JSON and ground YAML |
| `37.98 MW * 4 MUSD/MW` | `~152 MUSD` | ground JSON and ground YAML |
| `37.98 MW * 1.5 MUSD/MW-year * 5` | `~285 MUSD` | ground JSON and ground YAML |
| Sum of ground components | `~3,677 MUSD` | ground JSON `.ground.total_five_year_cost.value` |
| Sum of orbital build/launch components | `~7,048 MUSD` | ground JSON `.orbital_reference.five_year_cost_view.value` |
| `~7,048 / ~3,677` | `~1.92x` | ground JSON `.comparison.orbit_to_ground_ratio.value` |

This is the reason the current ground total is close to the May 26 sidecar
research central estimate. The arithmetic and the source-backed central read
both land near `$3.65B-$3.68B`; each ground input is now represented in the
source ledger and promoted JSON.

## External Source Findings

### Epoch AI 1 GW TCO Model

[Epoch AI's 2026 one-gigawatt AI data-center TCO model](https://epoch.ai/data-insights/ai-datacenter-cost-breakdown)
is the cleanest single external sanity check for this ground-cost stack. The
page was published on 2026-05-14 and states that a typical `1 GW` US
hyperscaler AI data center requires about `$38B` of up-front capex, about
`$0.9B/year` of opex, and about `$8.5B/year` of annualized TCO after capex is
annualized by asset life. It also states that servers are about `$5B/year`, or
`60%` of total annualized cost, and energy is about `$0.6B/year`.

Epoch's downloadable annualized CSV
(`https://epoch.ai/data/charts/ai-datacenter-cost-breakdown/one_gw_dc_capex_opex.csv`)
lists these annualized values, in millions of dollars per year: servers
`5021`, facility `1387`, network infrastructure `1167`, energy `594`, taxes
`143`, maintenance `120`, labor `40`, utility works `20`, land `13`, water `6`,
and total `7607` capex plus `907` opex. Epoch's up-front capex CSV
(`https://epoch.ai/data/charts/ai-datacenter-cost-breakdown/one_gw_dc_upfront_capex.csv`)
lists, in millions of dollars: servers `21188`, facility `11433`, network
infrastructure `4925`, land `172`, utility works `164`, and total `37883`.

Epoch's data note says its energy calculation uses `1 GW` of IT capacity,
`8.34 cents/kWh`, `PUE = 1.14`, and a utilization rate of about `71%`, based on
EIA state-level industrial costs, LBNL AI-specialized data-center PUE estimates,
and Tyler Norris's utilization discussion.

How this applies here:

- Epoch supports the broad conclusion that compute hardware dominates total
  cost while energy is the largest opex but a small share of all-in TCO.
- Epoch supports the current model's scale: a `37.978 MW` cohort is about
  `3.8%` of Epoch's `1 GW` reference, and the current non-GPU ground stack is
  of the same order when scaled down.
- Epoch does not certify the project's 2036 values. It is a 2026 stylized
  hyperscaler model using GB200 NVL72 systems, not a Rocket Lab or 2036 forecast.

### EIA Industrial Electricity Price

[EIA Electric Power Monthly Table 5.3](https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_03)
lists the 2025 US industrial average retail electricity price as
`8.62 cents/kWh`, or `$86.20/MWh`; it also lists 2026 year-to-date through March
at `8.94 cents/kWh`, or `$89.40/MWh`. EIA marks 2025 and 2026 values as
preliminary and states that values include power marketer data.

How this applies here:

- The current `energy_price_usd_per_mwh = 85.0` is directly supported as a
  current-real-dollar industrial-price estimate.
- Epoch independently uses `8.34 cents/kWh`, or `$83.40/MWh`, after weighting
  2024 EIA state-level industrial prices by data-center project counts.
- `$85/MWh` is `sourced_estimate` when described as a real-dollar central
  assumption rather than a precise 2036 tariff forecast.

### Google PUE And LBNL PUE Context

[Google's data-center efficiency page](https://datacenters.google/intl/en/efficiency/)
reports a 2024 average annual PUE of `1.09` across its global fleet and a
trailing-twelve-month PUE of `1.09` across large-scale stable-operation data
centers. Google also compares that with an industry average of `1.56`.

The [2024 LBNL United States Data Center Energy Usage Report](https://eta-publications.lbl.gov/sites/default/files/2024-12/lbnl-2024-united-states-data-center-energy-usage-report.pdf?stream=top)
models annual average PUE and WUE by data-center type and cooling system. It
states that liquid IT cooling can use higher water/refrigerant temperatures and
take greater advantage of free cooling; it models hyperscale, AI air-cooled, and
AI liquid-cooled cases with higher UPS/airflow efficiencies than small legacy
categories. It also says average PUE fell from `1.6` in 2014 to `1.4` in 2023
and is expected to fall to `1.15-1.35` by 2028 as hyperscale/colocation and
liquid-cooled AI servers increase. LBNL also reports US data-center electricity
use of `176 TWh` in 2023, or `4.4%` of US electricity consumption, and says
infrastructure energy fell from `40%` of total data-center electricity in 2014
to `30%` in 2023 as average PUE improved.

How this applies here:

- `PUE = 1.14` has external support from Epoch/LBNL as a hyperscale AI central
  value.
- `PUE = 1.25` is conservative but plausible for a source-backed scenario.
- The current `1.25` should not be called a certified fact.

### JLL Construction Cost And AI Fit-Out

[JLL's 2026 Global Data Center Market Outlook](https://www.jll.com/en-us/insights/market-outlook/global-data-centers)
states that average global data-center construction cost rose from
`$7.7M/MW` in 2020 to `$10.7M/MW` in 2025 and forecasts `$11.3M/MW` for 2026.
JLL notes that those figures include shell/core construction only, while tenant
tech fit-out can cost as much as `$25M/MW` for AI infrastructure.

How this applies here:

- JLL supports a low shell/core anchor near `$11.3M/MW`.
- JLL's shell/core plus AI fit-out ceiling supports a stress band near
  `$36.3M/MW`.
- The current `facility_shell_fitout_musd_per_mw = 18.0` sits inside this range
  and is reasonable as a central source-backed estimate only if the model is
  clear about what is and is not included.

### Turner & Townsend Construction Methodology

[Turner & Townsend's 2025 Data Centre Construction Cost Index](https://reports.turnerandtownsend.com/data-centre-construction-cost-index-2025/data-centre-cost-trends)
states that high-density liquid-cooled AI data centers in the US carry a
typical `7-10%` construction premium over similar air-cooled facilities by IT
capacity. It also gives an indicative liquid-cooled cost allocation of `48%`
electrical, `33%` mechanical, `9%` shell/architectural, and `10%`
general-contractor/general-requirements. Its
[methodology page](https://reports.turnerandtownsend.com/data-centre-construction-cost-index-2025/methodology)
states that its index captures shell/core, architectural fit-out and finishes,
mechanical and electrical fit-out, general-contractor preliminaries, margin,
contingency, and mechanical/electrical equipment. It excludes client direct
costs, land purchase, utility works, abnormal groundworks, site works, active
IT equipment, office fit-out fiber cabling, and professional services fees.

How this applies here:

- Turner & Townsend supports keeping electrical, mechanical/cooling, shell, and
  fit-out components explicit.
- It also warns about double counting. If the project's facility line includes
  full mechanical/electrical fit-out, then separate `cooling` and
  `racked_power_networking` lines overlap unless those lines are carefully
  scoped.

### Utilization And Load-Factor Caution

[Tyler Norris's 2025 Power & Policy note](https://www.powerpolicy.net/p/the-puzzle-of-low-data-center-utilization)
argues that load factor, utilization, uptime, and nameplate capacity are often
conflated in data-center power planning. It gives the example that a facility
with `80%` realized peak demand versus rated capacity and `90%` load factor has
only `72%` capacity utilization. It also notes that PUE says nothing about
capacity utilization and cites LBNL's warning that primary utilization data is
scarce.

How this applies here:

- `utilization = 0.85` is plausible as a high-utilization scenario.
- It is not a sourced fact.
- Epoch's `71%` utilization input is better as a sourced central energy
  arithmetic value, but the project may still choose `0.85` to represent a
  high-utilization AI-inference scenario.

## Input Audit And Implemented Source Statuses

| Current input | Current value | Implemented source status | Source basis | Caveat |
|---|---:|---|---|---|
| `gpu_package_cost_multiplier` | `1.0` | `scenario` | Comparison boundary: same 2036 package cohort and same package cost as the space model. | Not a ground-market fact; it is the like-for-like comparison rule. |
| `facility_shell_fitout_musd_per_mw` | `18.0 MUSD/MW` | `sourced_estimate` | JLL 2026 shell/core `$11.3M/MW`; JLL AI tech fit-out up to `$25M/MW`; Turner & Townsend AI liquid-cooled premium and cost allocation. | Must not silently include cooling and power/network lines if those remain separate. |
| `racked_power_network_musd_per_gpu_package` | `0.08 MUSD/package` | `scenario` | Epoch up-front network infrastructure is `$4.925B/GW`, or `$4.925M/MW`; current value maps to about `$7.0M/MW` because the model package is `11.4048 kW`. | Blends networking and racked power distribution; source-supported scenario, not an independently certified rack/network quote. |
| `energy_price_usd_per_mwh` | `85.0 USD/MWh` | `sourced_estimate` | EIA 2025 industrial average is `$86.20/MWh`; Epoch weighted data-center electricity price is `$83.40/MWh`. | Not a certified 2036 tariff or site-specific PPA. |
| `pue` | `1.25` | `scenario` with sourced support | Google fleet PUE `1.09`; Epoch AI model `1.14`; LBNL 2028 aggregate range `1.15-1.35`. | Conservative relative to best-in-class; not the evidence-central value. |
| `utilization` | `0.85` | `scenario` | Tyler Norris warns public utilization data is poor; Epoch uses about `71%` as a sourced modeling input. | High-utilization assumption; affects energy only in current model. |
| `operations_maintenance_musd_per_mw_year` | `1.5 MUSD/MW-year` | `scenario` | Epoch maintenance plus labor is about `$160M/year` for `1 GW`, or `$0.16M/MW-year`. Current value is plausible only if it also includes hardware maintenance/support. | Must not be described as pure labor/facility O&M. |
| `cooling_cost_musd_per_mw` | `4.0 MUSD/MW` | `scenario` | Turner & Townsend liquid-cooled AI construction has `33%` mechanical share and `7-10%` premium; prior local research used `$3-5M/MW` for AI liquid-cooling infrastructure. | Source-supported scenario with double-count risk against facility fit-out. |
| `comparison_period_years` | `5` | `scenario` | Tied to `RLDC-SERVICE-LIFE-5Y` and the space model service-life comparison. | Not a data-center depreciation claim. |

## Electricity Is Small Relative To Ground Infrastructure

The current electricity calculation is:

```text
37,977.984 kW
* 1.25 PUE
* 0.85 utilization
* 8,760 hours/year
* 5 years
/ 1,000 kWh/MWh
* $85/MWh
/ 1,000,000 USD/MUSD
= ~$150M
```

That `~$150M` is only `4.1%` of the `~$3.68B` ground total. Removing the
electricity line still leaves about `$3.53B` of ground cost. The ground side is
not free: non-GPU ground infrastructure and support are about `$1.54B`, or
`41.8%` of the full ground reference. But the utility bill alone is small
because GPU/package acquisition is about `$2.14B` and facility/infrastructure
capex is large.

This agrees with Epoch AI's external model. Epoch says energy is the largest
opex category at about `$594M/year` for a `1 GW` data center, but servers are
about `$5.021B/year` annualized and total annualized cost is about
`$8.514B/year`. The same pattern appears in the project model: energy is
strategically important, but it does not dominate all-in TCO.

## Solar And Radiator Implication

The orbital comparison is sensitive because orbital power and thermal rejection
are capitalized into the spacecraft rather than purchased as utility service.
In the current 2036 cohort:

| Orbital line | Current value | Source |
|---|---:|---|
| Solar/power | `~$1.52B` | ground JSON `.orbital_reference.component_costs[]` |
| Radiator/thermal | `~$1.52B` | ground JSON `.orbital_reference.component_costs[]` |
| Solar plus radiator | `~$3.04B` | sum of the two lines |
| Launch | `~$1.25B` | ground JSON `.orbital_reference.component_costs[]` |
| Solar plus radiator as share of orbital total | `43.1%` | `~$3.04B / ~$7.05B` |
| Solar plus radiator as share of solar/radiator/launch burden | `70.8%` | `~$3.04B / (~$3.04B + ~$1.25B)` |

Ground electricity is therefore not what makes the `~1.92x` ratio delicate.
The delicate part is whether the orbital model can defend the solar and
radiator cost dials. If solar and radiator were both halved from the current
`$40k/kW` dials to `$20k/kW`, the orbital total would fall by about
`$1.52B`, from about `$7.05B` to about `$5.53B`, and the ratio would fall from
`~1.92x` to about `1.50x` against the current ground reference. That is a
sensitivity, not the default.

## Likely Omissions And Double-Count Risks

| Issue | Direction of risk | Research read |
|---|---|---|
| Utility interconnect, substations, and switchgear | Omission or hidden overlap | Turner & Townsend excludes utility works; Epoch lists utility works separately at `$164M` up-front for `1 GW`, which scales to only about `$6.2M` for `37.978 MW`, but real projects can be lumpy and site-specific. |
| Backup generation, UPS, and redundancy | Possible omission or overlap | Turner & Townsend electrical/mechanical benchmarks include equipment categories, but the project model does not explicitly show backup power. AI workloads may tolerate different redundancy than cloud, but this should not be assumed silently. |
| Land, site works, owner costs, professional services | Omission | Epoch land is `$172M` up-front for `1 GW`, about `$6.5M` when scaled to this cohort. Not decisive, but excluded from the promoted ground JSON. |
| Cooling overlap | Double-count risk | JLL shell/core and Turner & Townsend M&E scopes can overlap with the separate `cooling` line. The facility input must be scoped as shell plus partial fit-out if cooling remains separate. |
| Network/fabric | Mixed bucket risk | Epoch network infrastructure is a major line. The current model has one `racked_power_network` package-rate that blends network and rack-side power distribution. |
| Hardware maintenance | Hidden inclusion risk | Current `1.5 MUSD/MW-year` is too high for pure facility O&M/labor if compared with Epoch maintenance plus labor (`0.16 MUSD/MW-year`). It is plausible only as a combined facility O&M plus hardware maintenance/support scenario. |
| Taxes, insurance, security, software, financing/carry | Omission | Epoch includes taxes in annualized cost; the project ground JSON excludes taxes and financing by design. That is acceptable for raw cost screening, not for DCF or provider economics. |
| Water | Omission but small | Epoch water is `$6M/year` for `1 GW`, about `$1.1M` over five years at `37.978 MW` if scaled simply. Not decisive, but should stay visible. |
| Depreciation/accounting | Explicit exclusion | The model is a five-year cash-like cost screen, not GAAP depreciation or DCF. Public prose should say so. |

## Public Claim Boundary

What can be said now:

- "The current 2036 ground reference computes about `$3.68B` over five years
  for the same `90` node, `3,330` package, `37.98 MW` deployed-year cohort."
- "The current orbital build-plus-launch reference computes about `$7.05B`,
  or about `1.92x` the current ground reference."
- "This supports same broad order of magnitude, not orbital cost parity."
- "The current five-year ground electricity line is about `$150M`, a small
  share of full ground TCO; GPU/package acquisition and facility/infrastructure
  capex dominate."
- "The orbital premium is driven mainly by solar, radiator, and launch, with
  solar plus radiator alone about `$3.04B` in the 2036 cohort."

What cannot be claimed publicly yet:

- Do not say the ground total is a certified 2036 fact. It is a
  source-backed scenario/derived estimate.
- Do not say orbital is cheaper than ground. The current default says the
  opposite on raw cost.
- Do not say the project has proven a `1.9x` production token price can clear
  the market. The ratio is a cost requirement under comparable-margin framing,
  not demand evidence.
- Do not say electricity avoidance is the main economic reason for orbit.
  The utility bill is small relative to compute and infrastructure capex.
- Do not present `PUE = 1.25` or `utilization = 0.85` as facts. They are
  conservative/high-utilization scenario choices with external support ranges.
- Do not present `operations_maintenance_musd_per_mw_year = 1.5` as pure
  facility O&M/labor. It needs to be split or documented as including hardware
  maintenance/support.
- Do not treat `facility_shell_fitout_musd_per_mw = 18.0` as fully loaded AI
  fit-out while also adding separate cooling and racked-power/network costs.

## Implemented Source-Status Baseline

| Input or claim | Implemented status | Public wording |
|---|---|---|
| `RLDC-GROUND-COST-BASIS` overall | Repaired in `SOURCE_INDEX.md` and promoted ground JSON | "The ground reference is a derived five-year scenario assembled from source-backed cost bands and explicit scenario choices." |
| Same package cost, `gpu_package_cost_multiplier = 1.0` | `scenario` | "Like-for-like comparison boundary using the same 2036 GPU package cohort and package cost basis." |
| Facility shell / fit-out, `$18M/MW` | `sourced_estimate` | "Central source-backed facility/fit-out allocation within JLL/T&T-supported range; excludes separately modeled cooling and rack/network lines." |
| Racked power/network, `$0.08M/package` | `scenario` | "Conservative rack-side power and networking allowance informed by Epoch network cost scale." |
| Energy price, `$85/MWh` | `sourced_estimate` | "Current-real-dollar industrial/data-center electricity price estimate, bracketed by EIA and Epoch." |
| PUE, `1.25` | `scenario` | "Conservative AI data-center PUE scenario; evidence-central values are closer to Google/Epoch/LBNL best-in-class and hyperscale ranges." |
| Utilization, `0.85` | `scenario` | "High-utilization modeling choice; public utilization data is uncertain." |
| Operations/maintenance/labor, `$1.5M/MW-year` | `scenario` | "Combined facility operations plus hardware maintenance/support allowance; not pure labor/O&M." |
| Cooling, `$4M/MW` | `scenario` | "Liquid-cooling infrastructure allowance; scope must avoid overlap with facility fit-out." |
| Comparison period, `5 years` | `scenario` | "Service-life-aligned comparison period, not a depreciation schedule." |
| Ground five-year total, `~$3.68B` | `derived_estimate` | "Derived from the current source-backed/scenario ground inputs." |
| Orbit/ground ratio, `~1.92x` | `derived_estimate` | "Cost ratio under current default assumptions; not market validation." |

## Sources

Local project sources:

- `data_center/models/ground/default.json`
- `data_center/models/space/default.json`
- `code/scenarios/ground_default.yaml`
- `code/src/data_center/ground.py`
- `research/SOURCE_INDEX.md`

External sources verified on 2026-05-28:

- [Epoch AI, "Servers account for 60% of the total cost of ownership of a one-gigawatt AI data center"](https://epoch.ai/data-insights/ai-datacenter-cost-breakdown), published 2026-05-14.
- [Epoch AI annualized cost CSV](https://epoch.ai/data/charts/ai-datacenter-cost-breakdown/one_gw_dc_capex_opex.csv), updated 2026-05-14.
- [Epoch AI up-front capex CSV](https://epoch.ai/data/charts/ai-datacenter-cost-breakdown/one_gw_dc_upfront_capex.csv), updated 2026-05-19.
- [EIA Electric Power Monthly Table 5.3](https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_03), release page viewed 2026-05-28.
- [Google Data Centers PUE](https://datacenters.google/intl/en/efficiency/), viewed 2026-05-28.
- [LBNL 2024 United States Data Center Energy Usage Report](https://eta-publications.lbl.gov/sites/default/files/2024-12/lbnl-2024-united-states-data-center-energy-usage-report.pdf?stream=top), viewed 2026-05-28.
- [JLL 2026 Global Data Center Market Outlook](https://www.jll.com/en-us/insights/market-outlook/global-data-centers), published 2026-01-05.
- [Turner & Townsend Data Centre Construction Cost Index 2025, cost trends](https://reports.turnerandtownsend.com/data-centre-construction-cost-index-2025/data-centre-cost-trends), viewed 2026-05-28.
- [Turner & Townsend Data Centre Construction Cost Index 2025, methodology](https://reports.turnerandtownsend.com/data-centre-construction-cost-index-2025/methodology), viewed 2026-05-28.
- [Tyler Norris, "The Puzzle of Low Data Center Utilization Rates"](https://www.powerpolicy.net/p/the-puzzle-of-low-data-center-utilization), published 2025-08-07.
