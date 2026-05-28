# Radiator Cost-Down And Hot-Loop Trajectory, 2030-2036

**Status:** draft research  
**Date:** 2026-05-27  
**Scope:** non-code research for the RKLB space data center research wiki  
**Source-status summary:** radiator physics is `certified`; current model radiator
mass is a `derived_estimate`; radiator cost remains a `scenario`; 2036 cost-down
and mass-down ranges are `scenario` or `derived_estimate` depending on whether
they come from physics arithmetic or from cost analogies. Public radiator cost
data is weak.

## Central Question And Premium Relevance

Can radiator cost and/or mass plausibly fall enough by 2030-2036 to narrow the
orbital cost premium versus a comparable ground data center?

The premium question is directly tied to the 2036 deployed-year cohort:

| Anchor | Current value | Source status |
|---|---:|---|
| Nodes deployed in 2036 | `90` | `derived_estimate`, from `data_center/models/space/default.json` and `data_center/models/ground/default.json` |
| GPU packages | `3,330` | `derived_estimate`, same model anchor |
| IT load deployed in 2036 | `37.978 MW` | `derived_estimate`, `90 * 421.98 kW` |
| Ground reference cost | `$3.677B` | `derived_estimate`, source-linked ground model |
| Orbital build plus launch reference | `$7.048B` | `derived_estimate`, current promoted space model |
| Orbital/ground ratio | `1.917x`, or `+91.7%` | `derived_estimate`, current ground comparison |

In the current model, radiator cost is one of the largest orbital-only cost
lines. A 50% radiator cost reduction saves about `$0.760B` on the 2036 cohort.
If solar and radiator are both halved, the all-in orbital/ground ratio falls
from about `1.92x` to about `1.50x`. Radiator cost-down therefore matters, but
it does not close the gap by itself.

The more subtle issue is radiator mass. Cost-down lowers the dollar premium.
Mass-down changes what a Neutron launch can carry. A lower radiator mass can
increase packages per node, provide margin, reduce risk, or lower bus/deployment
complexity. It does not automatically reduce radiator dollars unless the cost
model is linked to area, mass, or manufacturing complexity rather than to kW.

## Current Radiator Model Anchor

The current promoted model uses:

| Quantity | Value | Formula or interpretation |
|---|---:|---|
| Radiator cost dial | `$40k/kW` | `0.04 MUSD/kW` scenario |
| Radiator mass dial | `0.012 t/kW` | `12 kg/kW` derived model input |
| 2036 power per node | `421.9776 kW` | `37 packages * kW/package` |
| Radiator mass per node | `5.064 t` | `421.9776 * 0.012` |
| Radiator cost per node | `$16.879M` | `421.9776 * $40k/kW` |
| 2036 radiator cohort cost | `$1.519B` | `$16.879M * 90 nodes` |

Those values align with the public source ledger entry
`RLDC-SOLAR-RADIATOR-COST`, which records solar and radiator cost dials of
`$0.04M/kW` each as scenario values, and with `THR-003`, which records the
hot-loop radiator mass lever as a derived estimate. They should not be described
as vendor-quoted radiator costs.

## Current State Of Deployable Space Radiators

The current state is technically plausible but not cost-closed.

NASA's Small Spacecraft State of the Art chapter describes deployable radiators
as a way to increase radiative surface area when body-mounted spacecraft area is
insufficient, and flags high power density plus limited external area as core
small-spacecraft thermal problems
([NASA thermal control](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/)).
Redwire's 2026 orbital data-center white paper reaches the same architectural
conclusion for orbital compute: power generation, distribution, and thermal
rejection must be treated as a coupled energy system; nearly all electrical
energy becomes heat that has to be transported and radiated to space
([Redwire ODC white paper](https://rdw.com/wp-content/uploads/2026/05/RDW26-053-ODC-Power-Thermal-Study-White-Paper-R11-Digital.pdf)).

### Radiator Flux And Geometry

Radiator performance is governed by:

```text
Q / A = epsilon * sigma * (T_rad^4 - T_sink^4)
```

where `epsilon` is surface emissivity, `sigma` is the Stefan-Boltzmann constant,
`T_rad` is radiator surface temperature, and `T_sink` is the effective radiative
environment. The project currently uses `epsilon = 0.85`, `T_sink = 250 K`, and
a conservative one-effective-face treatment in the mass model. The local
research corpus treats those as assumptions rather than vendor facts:
[hot_chip_thermal_trajectory.md](hot_chip_thermal_trajectory.md),
[solar_radiator_trajectory.md](solar_radiator_trajectory.md), and
[orbital/thermal_analysis.md](../orbital/thermal_analysis.md).

Redwire gives a useful public sanity check: common radiator panels can radiate
around `250 W/m^2` using ordinary materials and engineering design, while higher
temperature operation can improve rejection but may conflict with compute
hardware temperature limits and architecture
([Redwire ODC white paper](https://rdw.com/wp-content/uploads/2026/05/RDW26-053-ODC-Power-Thermal-Study-White-Paper-R11-Digital.pdf)).
The current model's `12 kg/kW` corresponds to about `83 W/kg` of heat rejection
capacity at the subsystem level. That is conservative relative to optimistic
hot-loop physics, but plausible once large deployable structure, headers,
fluid loop, nonideal view factors, margins, deployment hardware, and one-face
crediting are included.

### Areal Density

The local corpus uses a deployable radiator areal-density range of roughly
`3 / 5 / 8 kg/m^2` for low/mid/high large-system cases. External sources support
that as a reasonable bracket, but not as a closed value:

- NASA/TFAWS 2024 additive-manufactured radiator work says mature spacecraft
  radiators can operate near `400 K` with roughly `12 kg/m^2`, reports a
  graphite/titanium-water heat-pipe concept near `3.5 kg/m^2`, reports a
  tested lower-cost radiator concept near `1.5 kg/m^2`, and notes NASA targets
  for higher-temperature radiators of `500-600 K` and `2-3 kg/m^2`
  ([NASA NTRS TFAWS 2024 paper](https://ntrs.nasa.gov/api/citations/20240009793/downloads/TFAWS%202024%20Paper.pdf?attachment=true)).
- The same paper also warns that high-temperature dissimilar-material bonds,
  polymer adhesives, brazes, CTE mismatch, and heat-pipe integration remain
  real technical challenges.
- NASA's thermal-control chapter says deployable radiators and advanced thermal
  storage are still undergoing testing for small spacecraft, even though larger
  spacecraft thermal technologies are mature
  ([NASA thermal control](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/)).

The implication is that `0.012 t/kW` is not absurd, but it is a conservative
integrated-system value. A future `0.006 t/kW` sensitivity requires both hotter
operation and a lighter deployable radiator architecture; it should not be
presented as a current product specification.

### Deployable Radiator Maturity

Public vendor evidence supports technical maturity at small and moderate scale,
not yet at the 2036 node scale:

- ARQUIMEA sells qualified deployable radiators for satellites, based on
  multi-loop heat pipes, up to `6 m^2` surface, with the complete assembly and
  qualified deployment mechanism
  ([ARQUIMEA deployable radiators](https://www.arquimea.com/products/deployable-radiators-satellite-space/)).
- ThermAvant reports OHP spacecraft radiators with more than `1,000` on-orbit
  or delivered-for-launch units by mid-2025, a temperature range of `-20 deg C`
  to `+100 deg C`, environmental qualification, and examples including a
  `1.7 m^2` high-emissivity radiator capable of rejecting more than `1 kW`
  under worst-case transient conditions
  ([ThermAvant OHP radiators](https://www.thermavant.com/thermavant-products/oscillating-heat-pipe-radiators)).
- Redwire says deployable passive radiator systems have been used in high-power
  space applications, but also calls out additional mass, packaging demands,
  mechanisms, dynamic effects, and mission cost as radiator systems grow
  ([Redwire ODC white paper](https://rdw.com/wp-content/uploads/2026/05/RDW26-053-ODC-Power-Thermal-Study-White-Paper-R11-Digital.pdf)).

The scale mismatch is the key. A `421.98 kW` node at the current `0.012 t/kW`
mass dial implies `5.064 t` of radiator per node. That is far beyond a few
square meters of conventional telecom deployable radiator hardware and belongs
in a new productized large-deployable category.

### Cost Evidence Quality

Radiator cost evidence is weak. Public sources discuss performance, mass,
temperature, deployment, and heritage, but do not provide reliable `$ / kW` or
`$ / m^2` cost curves for a hundreds-of-kW orbital data-center radiator.

ESA's lightweight deployable radiator tender explicitly describes deployable
radiators as typically heavy, complex, and often expensive products
([ESA ARTES lightweight deployable radiators](https://connectivity.esa.int/archives/open_tender/lightweight-deployable-radiators-artes-4d062-0)).
That supports caution, but it does not quantify cost. Vendor pages generally
request contact for quotes. Therefore:

- `$40k/kW` radiator cost is a scenario default, not a sourced fact.
- `$20k/kW` radiator cost is an upside sensitivity, not validated.
- The right next evidence would be a vendor quote or bottom-up bill of
  materials for a productized `300-500 kW` class deployable radiator.

## Hot-Loop Liquid Cooling And GPU Temperature Limits

The physical lever is higher radiator surface temperature. The constraint is
the chip and package thermal path.

### Current GPU And Liquid Cooling Evidence

NVIDIA's public H100 PCIe product brief lists H100 PCIe thermal qualification at
`GPU TAVG = 87 deg C` and `HBM THBM = 95 deg C`, and defines slowdown/shutdown
relative to its thermal limit telemetry rather than publishing a simple public
Tjmax for all H100 products
([NVIDIA H100 PCIe product brief](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf)).
This supports the basic point that modern accelerators are designed for high
internal silicon/HBM temperatures, but it does not mean they can be run
arbitrarily hotter without reliability or throttling costs.

ASHRAE's liquid-cooling guidance is directly relevant. The W classes were
renamed to include upper temperature limits: `W17`, `W27`, `W32`, `W40`, `W45`,
and `W+`, and equipment operating within a class is expected to provide full
performance over that class's environmental range
([ASHRAE liquid cooling white paper](https://www.ashrae.org/file%20library/technical%20resources/bookstore/emergence-and-expansion-of-liquid-cooling-in-mainstream-data-centers_wp.pdf)).
A 2025 ASHRAE presentation clarifies that W classes are facility-water supply
temperatures, not necessarily the technology-cooling-system temperature at the
ITE, and lists `W45` at `45 deg C` and `W+` above `45 deg C`
([Dallas ASHRAE presentation](https://dallas-ashrae.org/images/meeting/041625/the_ashrae_thermal_guidelines_for_data_centers_____past__present_and_future.pdf)).

Data Center Dynamics reports the tension clearly: current high-end processors
and accelerators can be cooled at high liquid coolant temperatures, up to
`40-45 deg C` facility-water supply in some cases, but Schneider Electric's
cooling lead says `50-60 deg C` supply water is highly unlikely for training
loads as chip powers rise
([DCD hot-water analysis](https://www.datacenterdynamics.com/en/analysis/hot-water-cold-water/)).
That is a caution for orbital designs: a hot radiator surface may be feasible,
but the chip inlet temperature cannot simply be set to `70-80 deg C`.

Vendor evidence for GB200-class systems points in the same direction.
ToneCooling's GB200 NVL72 guide says a rack generates `120 kW+`, each GB200
module dissipates up to `1200 W`, and cooling requires direct-to-chip cold
plates with inlet coolant below `45 deg C`
([ToneCooling GB200 cooling](https://tonecooling.com/nvidia-gb200-nvl72-cooling-requirements/)).
NVIDIA's own Q3450-LD liquid-cooled switch documentation lists a maximal
liquid inlet temperature of `45 deg C` and maximal return of `55 deg C` for
that switch platform, which is not a GPU module but supports the broader
point that published liquid-cooled datacenter hardware often centers around
`45 deg C` inlet limits
([NVIDIA Q3450-LD liquid cooling](https://docs.nvidia.com/networking/display/xdrswitcheshwum/q3450-ld-liquid-cooling-system)).

### Applicability To Orbital GPU Packages

For the RKLB model, the safe interpretation is:

- A `70-80 deg C` radiator surface is plausible only if the thermal path can
  keep GPU junction and HBM temperatures inside vendor limits.
- The radiator can be hotter than the coolant entering the cold plate only if
  the heat transport architecture includes enough temperature lift or thermal
  staging. A simple single-phase direct loop does not make this free.
- A hot-side coolant or radiator return temperature around `60-70 deg C` looks
  more supportable from public data than a `70-80 deg C` cold-plate inlet.
- Moving toward `80 deg C` radiator surfaces probably requires careful
  chip-to-coolant-to-panel modeling, high-flow low-resistance cold plates,
  possibly two-phase transport, and explicit reliability derating.

This confirms the local `hot_chip_thermal_trajectory.md` conclusion: the
winning move is to run the loop and radiator hot while defending the silicon,
not to assume the GPU package itself can be run near its limit for five years.

## 2030-2036 Trajectory

The credible improvement path has four parts.

### 1. Higher Radiator Operating Temperature

The highest-leverage mass lever is radiator surface temperature because heat
flux scales with absolute temperature to the fourth power. The local hot-loop
calculation shows a `40 deg C` to `80 deg C` surface-temperature move can cut
radiator area and mass by roughly `51%` under fixed emissivity, sink, face,
and areal-density assumptions. This is a `derived_estimate` from radiative
physics, not a vendor roadmap.

By 2030-2036, a defensible sensitivity is that GPU packages and liquid-cooling
systems continue moving toward warmer coolant operation, but public evidence
does not yet support treating `80 deg C` radiator surface as guaranteed.
The next research step is a chip-to-coolant-to-panel thermal resistance model.

### 2. Lower Areal Density

A mature deployable radiator might move from today's conservative integrated
range toward `2-3 kg/m^2` in selected designs. NASA/TFAWS work identifies
`2-3 kg/m^2` as a target for high-temperature radiator development and reports
prototype concepts near or below that band, while also listing integration
challenges
([NASA NTRS TFAWS 2024 paper](https://ntrs.nasa.gov/api/citations/20240009793/downloads/TFAWS%202024%20Paper.pdf?attachment=true)).

For a large orbital data-center node, the full system value will be worse than
panel-only value because it must include deployment structure, heat acquisition,
headers, fluid inventory, pumps or heat pipes, mechanisms, stiffness, sensors,
and margin. A 2036 integrated range of `0.006-0.012 t/kW` is plausible as a
scenario; the low end needs both high temperature and low areal density.

### 3. Productized Manufacturing

Radiator cost could fall if a vendor or Rocket Lab productizes a repeated
large deployable radiator instead of buying one-off custom spacecraft thermal
hardware. ThermAvant's OHP page emphasizes manufacturability and lower assembly
complexity for embedded OHP radiator structures
([ThermAvant OHP radiators](https://www.thermavant.com/thermavant-products/oscillating-heat-pipe-radiators)).
NASA/TFAWS additive-manufactured radiator work points toward monolithic
embedded heat-pipe radiator panels, which could reduce part count and
interfaces over time
([NASA NTRS TFAWS 2024 paper](https://ntrs.nasa.gov/api/citations/20240009793/downloads/TFAWS%202024%20Paper.pdf?attachment=true)).

This supports cost-down directionally. It does not establish `$20k/kW`.

### 4. Architecture: Modular/Tiled Heat Rejection

Redwire's white paper argues that tiled architectures can integrate compute,
power generation, and thermal transport locally, reducing the penalty of moving
power and heat across long distances
([Redwire ODC white paper](https://rdw.com/wp-content/uploads/2026/05/RDW26-053-ODC-Power-Thermal-Study-White-Paper-R11-Digital.pdf)).
That is relevant to the RKLB model because a co-mounted solar/radiator/bus
architecture could reduce long thermal paths and deployment complexity.

This is probably more important for reliability and mass than for direct
`$/kW` evidence.

## What A 50% Cost Reduction Means

Current 2036 radiator cost:

```text
421.9776 kW/node * $40,000/kW = $16.879M/node
$16.879M/node * 90 nodes = $1.519B
```

At `$20k/kW`:

```text
421.9776 kW/node * $20,000/kW = $8.440M/node
$8.440M/node * 90 nodes = $0.760B
savings = $0.760B
```

That is a financial sensitivity. It does not by itself make the node lighter.
It lowers the all-in orbital cost from about `$7.048B` to about `$6.288B` if
only radiator cost is halved, and lowers the orbital/ground ratio from about
`1.92x` to about `1.71x`. If both solar and radiator are halved, the orbital
cost falls to about `$5.529B`, or about `1.50x` ground.

Public-safe interpretation:

> A `$20k/kW` radiator cost is an upside 2036 sensitivity. It is useful for
> premium analysis, but the current public default should remain `$40k/kW`
> until a vendor quote or bottom-up manufacturing model exists.

## What A 50% Mass Reduction Means

Current 2036 radiator mass:

```text
421.9776 kW/node * 0.012 t/kW = 5.064 t/node
5.064 t/node * 90 nodes = 455.7 t cohort radiator mass
```

At `0.006 t/kW`:

```text
421.9776 kW/node * 0.006 t/kW = 2.532 t/node
savings = 2.532 t/node
cohort radiator mass = 227.9 t
```

That is a physical sensitivity. It creates payload margin or enables more GPU
packages per launch. It does not automatically halve radiator cost unless the
cost model is changed from a simple `$ / kW` dial to an area/mass/manufacturing
model.

In the current 2036 default, node mass is about `12.448 t` against a `12.5 t`
mass envelope, so a `2.532 t/node` radiator mass saving would be extremely
important physically. It would move the design from almost mass-filled to
meaningfully flexible. The model should treat that as a mass/architecture
sensitivity, not just as a cost sensitivity.

## 2036 Ranges

These are recommended research ranges, not proposed default changes.

### Radiator Cost Range

| Case | 2036 radiator cost | Label | Rationale |
|---|---:|---|---|
| Low / upside | `$20k/kW` | `scenario` | Productized large radiator, simple co-mounted architecture, high repetition, internalized integration, no first-of-kind vendor premium. Not publicly validated. |
| Central researched scenario | `$30-40k/kW` | `scenario` | Preserves caution because public vendor `$ / kW` data is absent; current `$40k/kW` default remains acceptable. |
| High / stress | `$60-100k/kW` | `scenario` | One-off deployable thermal system, high qualification burden, complex pumped loop, mechanisms, deployment risk, supplier margin. |

### Radiator Mass Range

| Case | 2036 radiator mass | Label | Rationale |
|---|---:|---|---|
| Low / aggressive | `0.005-0.007 t/kW` | `derived_estimate` plus `scenario` | Requires high radiator surface temperature, low areal density, favorable view factors, and good chip-to-panel thermal resistance. |
| Central | `0.008-0.012 t/kW` | `derived_estimate` | Hot-loop but conservative integrated-system range. Current default `0.012 t/kW` sits at the conservative end. |
| High / stress | `0.014-0.020 t/kW` | `scenario` | Cooler surfaces, poor second-face credit, higher sink temperature, heavier deployment hardware, extra fluid-loop mass. |

The most defensible current public default is still:

```text
radiator_cost_musd_per_kw = 0.04
radiator_t_per_kw_post = 0.012
```

The most useful next sensitivity is:

```text
radiator_cost_musd_per_kw = 0.02
radiator_t_per_kw_post = 0.006 to 0.008
```

But that sensitivity needs a clear title such as
`radiator_hot_loop_costdown_2036`, and it should be labelled as an upside
scenario.

## Public-Safe Claims

Safe:

- Space radiators reject heat by thermal radiation, and heat rejection scales
  with the fourth power of absolute radiator temperature.
- Orbital compute power and thermal rejection must be designed as a coupled
  energy system.
- Deployable radiators exist and have heritage at smaller scales, including
  loop-heat-pipe and oscillating-heat-pipe approaches.
- Public evidence supports the direction of warmer liquid-cooling loops, but
  GPU package temperature limits and reliability constrain how hot the silicon
  can run.
- The current `$40k/kW` radiator default is a cautious scenario, not a quote.
- `$20k/kW` radiator cost is a plausible 2036 sensitivity, not a certified
  value.
- A 50% radiator mass reduction would be physically meaningful because the 2036
  default is mass-bound.

Unsafe:

- "Radiator cost is validated at `$20k/kW`."
- "Radiator cost is validated at `$40k/kW`."
- "GPU packages can run at `80 deg C` coolant inlet for five years."
- "Hotter chips alone close the orbital/ground gap."
- "A 50% radiator cost reduction automatically means a 50% radiator mass
  reduction."
- "Panel-only areal density equals complete deployed radiator system density."

## Implications For Model Defaults And Sensitivities

Do not change the default solely from this research. The evidence supports
adding or keeping a named sensitivity, not replacing the public default.

Recommended model posture:

1. Keep `$40k/kW` radiator default as a cautious scenario until cost evidence
   improves.
2. Add a documented `$20k/kW` radiator cost-down sensitivity if the model gains
   scenario support for it.
3. Separate cost sensitivity from mass sensitivity. They are different levers.
4. Add a hot-loop mass sensitivity around `0.006-0.008 t/kW`, labelled as
   conditional on thermal-resistance modeling.
5. Track whether lower radiator mass increases packages per node, creates
   margin, reduces bus/deployment mass, or changes launch economics. Those are
   physical architecture effects, not just line-item cost effects.
6. Require future public docs to call radiator cost `scenario` and radiator mass
   `derived_estimate/scenario` until vendor quotes, bottom-up design, or test
   data exist.

## Unresolved Questions

- What is the real chip-to-coolant-to-panel thermal resistance for the 2036 GPU
  package and node architecture?
- Can the radiator surface reliably operate near `70-80 deg C` while keeping
  GPU/HBM junction temperatures inside vendor limits over a five-year mission?
- What are the pump, CDU, fluid inventory, heat-pipe, manifold, deployment, and
  sensor masses for a `300-500 kW` class space radiator?
- What is the vendor quote for a repeated large deployable radiator at
  `300-500 kW` class?
- Does Rocket Lab build, partner, or acquire radiator capability, and how much
  supplier margin is internalized?
- Should radiator cost be modeled per kW, per square meter, per kg, or through a
  component bill of materials?
- How much does two-face credit survive after real co-mounted solar, radiator,
  bus, Earth-view, albedo, and self-view geometry is modeled?

## Sources

Local project sources:

- [solar_radiator_trajectory.md](solar_radiator_trajectory.md)
- [hot_chip_thermal_trajectory.md](hot_chip_thermal_trajectory.md)
- [gpu_temperature_cooling_limits.md](gpu_temperature_cooling_limits.md)
- [gpu_hotter_operation_reliability_2030_2036.md](gpu_hotter_operation_reliability_2030_2036.md)
- [SOURCE_INDEX.md](../SOURCE_INDEX.md) claims `THR-014` and `THR-016`
- `data_center/models/ground/default.json` current ground/orbital comparison paths

External sources:

- [NASA SmallSat thermal control](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/), spacecraft thermal-control state-of-the-art and caveats.
- [NASA TFAWS 2024 additively manufactured deployable radiator paper](https://ntrs.nasa.gov/api/citations/20240009793/downloads/TFAWS%202024%20Paper.pdf?attachment=true), deployable radiator mass/architecture context.
- [Redwire orbital data-center power and thermal white paper](https://rdw.com/wp-content/uploads/2026/05/RDW26-053-ODC-Power-Thermal-Study-White-Paper-R11-Digital.pdf), ODC-scale power/thermal architecture framing.
- [ThermAvant OHP radiators](https://www.thermavant.com/thermavant-products/oscillating-heat-pipe-radiators) and [Arquimea deployable radiators](https://www.arquimea.com/products/deployable-radiators-satellite-space/), vendor evidence for radiator maturity and mass-performance direction. Treat vendor numbers as sourced estimates, not certified defaults.
- [ESA ARTES lightweight deployable radiators tender](https://connectivity.esa.int/archives/open_tender/lightweight-deployable-radiators-artes-4d062-0), market/procurement signal.
- [ASHRAE liquid-cooling white paper](https://www.ashrae.org/file%20library/technical%20resources/bookstore/emergence-and-expansion-of-liquid-cooling-in-mainstream-data-centers_wp.pdf) and [ASHRAE thermal-guidelines reference card](https://www.ashrae.org/file%20library/technical%20resources/bookstore/supplemental%20files/therm-gdlns-5th-r-e-refcard.pdf), data-center liquid-cooling temperature context.
- [NVIDIA H100 PCIe product brief](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf), public GPU/HBM thermal qualification context.

## Proposed Tracker/Library Entry Text

Suggested `LIBRARY.md` row:

| [radiator_costdown_2030_2036.md](radiator_costdown_2030_2036.md) | Radiator cost-down and hot-loop trajectory. | `$40k/kW` remains a cautious default; `$20k/kW` and `0.006-0.008 t/kW` are useful 2036 upside sensitivities, but cost evidence remains weak and GPU temperature limits require a chip-to-panel thermal model. |

Suggested `RESEARCH_TRACKER.md` row:

| [radiator_costdown_2030_2036.md](radiator_costdown_2030_2036.md) | draft | Tests whether radiator cost/mass can fall enough by 2030-2036 to narrow the orbital premium. | Physics and mass ranges are source-supported; `$ / kW` remains scenario-only pending vendor quote or bottom-up BOM. |

Suggested backlog item:

- Build a chip-to-coolant-to-panel thermal-resistance model and a radiator
  cost model that separates panel area, areal density, deployment structure,
  pumped-loop hardware, and manufacturing learning. This is required before
  changing the default radiator cost or mass dials.
