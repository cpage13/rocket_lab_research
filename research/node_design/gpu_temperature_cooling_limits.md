# GPU Temperature And Cooling Limits For Orbital Data-Center Nodes

**Status:** draft research  
**Date:** 2026-05-27  
**Scope:** project-specific non-code research for the RKLB space data center feasibility workstream.  
**Source-status summary:** public evidence is strong for the physics of radiative heat rejection, strong for the industry move toward warmer liquid-cooling loops, medium for current AI rack coolant temperatures, weak-to-medium for exact GPU junction limits because NVIDIA treats detailed thermal thresholds as partner/OEM information, and unresolved for mapping future chip/coolant temperatures into certified space-radiator mass or cost.

This document follows the research-wiki convention: hard numbers are labelled as sourced, derived, scenario, or unresolved. It does not update the shared tracker or library directly; proposed entries are included at the end for integration by the main agent.

## Central Question

What do GPU temperature limits mean, and how do they translate into radiator requirements for an orbital data-center node?

The short answer is that **chip junction temperature is not the same thing as radiator temperature**. A GPU can have a junction limit near the upper end of modern electronics operation while the radiator surface is cooler, because heat must pass through a chain:

`GPU/HBM junction -> package/case -> thermal interface material -> cold plate -> coolant -> heat exchanger / heat pipe / loop -> radiator panel -> space`

Every link consumes temperature difference. The orbital model should therefore avoid saying "chips run at 85 C, so the radiator runs at 85 C." The fair statement is:

> Higher allowable chip and coolant temperatures can allow a hotter radiator, and a hotter radiator rejects more heat per square meter. The size of that benefit depends on the thermal-resistance chain, coolant architecture, radiator areal density, view factors, and reliability margin.

The user's premium question depends on this because radiator mass and radiator cost are major orbital cost drivers. If space solar and radiator costs fall by roughly half, validation currently shows the all-in orbital premium falling from about 92% over the ground reference to about 50%. A hotter loop could support that case only if it reduces radiator area/mass/cost without pushing GPU/HBM junctions into unacceptable reliability or throttling regimes.

## Definitions

**Junction temperature.** The temperature at the active silicon junctions inside the GPU, HBM, or switch ASIC. This is the temperature most directly tied to throttling, leakage, electromigration, time-dependent dielectric breakdown, and other wear mechanisms.

**Case temperature.** The temperature at the package exterior or lid where heat leaves the package into a thermal interface material and cold plate. Case temperature is lower than junction temperature by the internal package thermal resistance times power.

**Coolant supply temperature.** The temperature of liquid entering the cold plate or technology cooling loop. In data-center standards, be careful: facility water supply temperature is not always the same as the liquid temperature seen by the IT equipment. ASHRAE-facing materials distinguish facility water system classes from technology cooling system temperatures, and CDU approach temperatures can add several degrees between loops ([ASHRAE reference card](https://www.ashrae.org/file%20library/technical%20resources/bookstore/supplemental%20files/therm-gdlns-5th-r-e-refcard.pdf), [ASHRAE Dallas 2025 presentation](https://dallas-ashrae.org/images/meeting/041625/the_ashrae_thermal_guidelines_for_data_centers_____past__present_and_future.pdf)).

**Coolant return temperature.** The temperature of liquid leaving the rack/cold plate after absorbing heat. This is closer to the hot-side temperature available to a radiator, but it is still not identical to radiator surface temperature.

**Cold plate.** A liquid-cooled heat exchanger clamped to the GPU, CPU, HBM-adjacent package surfaces, or switch ASICs. The cold plate spreads heat and transfers it into coolant. Direct-to-chip liquid cooling is now the normal architecture for high-power AI accelerators.

**Single-phase liquid cooling.** The coolant remains liquid through the loop. It is simpler and mature, but the coolant temperature rises along the flow path and the loop needs enough mass flow and pressure margin.

**Two-phase liquid cooling.** The working fluid changes phase, usually by boiling near the heat source and condensing elsewhere. It can move large heat loads at nearly constant temperature, but it adds fluid-selection, microgravity, pump, separator, condenser, and reliability complexity. Public data-center sources describe two-phase as promising but not yet the dominant AI rack architecture; space thermal sources treat heat pipes and loop heat pipes as established, while large active two-phase orbital data-center loops remain a design risk ([Fierce Network](https://www.fierce-network.com/cloud/nvidia-has-no-chill), [NASA thermal control](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/)).

**Radiator surface temperature.** The temperature of the emitting radiator surface. This is the temperature used in Stefan-Boltzmann heat-rejection math. It is usually lower than the hottest coolant temperature because the radiator has internal thermal resistance and non-uniformity.

**Heat-rejection temperature.** A broader phrase for the effective temperature at which the system can reject heat to space. In simple calculations, this is approximated as radiator surface temperature.

**Thermal resistance chain.** The total temperature rise per watt across each link from silicon to radiator. In simplified form:

`T_junction = T_radiator + heat_load * R_total + loop_temperature_offsets`

Low thermal resistance lets the radiator run closer to the chip/coolant temperature. High thermal resistance forces a cooler radiator for the same safe junction temperature.

## Current State

### What public sources say about AI accelerator heat

NVIDIA public product pages and OEM guides are clear on power and cooling architecture, but less clear on exact junction thresholds:

- H100 SXM is publicly specified at up to 700 W configurable TDP, while H100 PCIe/H100 NVL classes sit lower depending on form factor ([NVIDIA H100](https://www.nvidia.com/en-eu/data-center/h100/), [H100 datasheet mirror](https://www.pny.com/File%20Library/Company/Support/Product%20Brochures/NVIDIA%20Data%20Center%20GPUs/english/nvidia-h100-datasheet.pdf)).
- B200-class hardware is now in the 1000 W class per module in Lenovo's public HGX B200 product guide, with liquid-cooled and air-cooled system variants depending on server design ([Lenovo B200 1000 W product guide](https://lenovopress.lenovo.com/lp2226.pdf)).
- GB200 NVL72 is a 72-GPU, 36-Grace-CPU, rack-scale liquid-cooled system in NVIDIA's official product description ([NVIDIA GB200 NVL72](https://www.nvidia.com/en-gb/data-center/gb200-nvl72/)).
- A public NVIDIA developer-forum answer to an H100 thermal-threshold question says the exact maximum stable temperature, recommended range, throttling threshold, and shutdown threshold are available to NVIDIA partners and OEMs, not generally published in that forum thread ([NVIDIA developer forum](https://forums.developer.nvidia.com/t/nvidia-h100-recommended-operating-temperature/342125)).

The practical implication is important: **the project should not claim a certified NVIDIA Tjmax for future GPUs unless it has a vendor/OEM source**. Existing local research uses roughly 83-85 C as a planning band for current NVIDIA-class accelerators, but that should be labelled as a sourced estimate / practical operating band, not a public NVIDIA product guarantee.

### Liquid-cooling temperatures today

The public data-center cooling direction is much better sourced than the exact junction limit.

ASHRAE's liquid-cooling temperature classes include W40, W45, and W+, with W40 at 40 C facility water supply, W45 at 45 C, and W+ above 45 C. The ASHRAE reference card describes W45/W+ as classes typically operated without chillers to improve energy efficiency, while noting that dry-cooler suitability is location-dependent ([ASHRAE reference card](https://www.ashrae.org/file%20library/technical%20resources/bookstore/supplemental%20files/therm-gdlns-5th-r-e-refcard.pdf)). A 2025 ASHRAE presentation further distinguishes facility water supply from technology cooling system temperature and shows technology-cooling-system classes up to S50, or 50 C ([ASHRAE Dallas 2025 presentation](https://dallas-ashrae.org/images/meeting/041625/the_ashrae_thermal_guidelines_for_data_centers_____past__present_and_future.pdf)).

For NVIDIA's next-generation direction, public reporting says Vera Rubin was presented as able to operate with 45 C water and reduced chiller dependence. The safest reading is not "cooling goes away"; it is "warm-water direct liquid cooling shifts the facility from mechanical chilling toward dry coolers / heat rejection." CoolIT explicitly cautions that 45 C water does not eliminate heat rejection and that hot/humid regions may still need chillers ([CoolIT](https://www.coolitsystems.com/resources/news/warm-water-cooling-and-ai-the-future-is-here-but-its-not-chiller-free/)). Fierce Network reports an NVIDIA cooling statement that chips run around 85-90 C and therefore can use 45 C water, while also quoting Vertiv's caveat that heat rejection remains necessary ([Fierce Network](https://www.fierce-network.com/cloud/nvidia-has-no-chill)).

Data Center Dynamics captures the tension well: high liquid coolant temperatures such as 40-45 C are useful, but as chips become more power hungry, internal heat dissipation and reliable cooling can require colder water or better cold plates, so simply pushing to 50-60 C supply is not guaranteed ([DCD hot-water/cold-water analysis](https://www.datacenterdynamics.com/en/analysis/hot-water-cold-water/)).

### Reliability and derating implications

Higher **junction** temperature is not free. Electronics Cooling explains that the common "10 C increase halves life" rule is a rough Arrhenius-based heuristic that applies to specific thermally activated failure mechanisms, often in the 75-125 C range for activation energies around 0.8 eV, but it does not cover every failure mode and can be misleading if applied universally ([Electronics Cooling](https://www.electronics-cooling.com/2017/08/10c-increase-temperature-really-reduce-life-electronics-half/)).

For this project, the correct reliability framing is:

- Hotter radiator surface is good if junction temperature is held constant.
- Hotter coolant is acceptable if the cold plate and package still preserve junction margin.
- Hotter junction temperature increases leakage, can reduce boost/throttle margin, and can accelerate some wear mechanisms.
- Thermal cycling and launch-induced mechanical stress may be as important as absolute temperature for HBM/package/interconnect reliability; local research already flags graceful degradation and coolant-loop redundancy as first-order concerns in [reliability_failure_handling.md](reliability_failure_handling.md).

## Space Translation

### Why radiator temperature matters

In vacuum, waste heat must be radiated. NASA describes deployable radiators as dedicated surfaces for dissipating excess heat by radiative transfer, and notes that deployable radiators become valuable when body surface area is insufficient ([NASA thermal control](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/), [NASA Thermal Systems SOA PDF](https://www.nasa.gov/wp-content/uploads/2025/02/7-soa-thermal-2024.pdf)).

Redwire's 2026 orbital-data-center white paper makes the system-level point directly: nearly all electrical energy consumed by compute becomes heat, and orbital data-center power generation, distribution, and thermal rejection must be designed as a coupled energy system ([Redwire ODC white paper](https://rdw.com/wp-content/uploads/2026/05/RDW26-053-ODC-Power-Thermal-Study-White-Paper-R11-Digital.pdf)). Redwire also emphasizes that radiator performance depends on operating temperature, coatings, view factors, orientation, thermal interfaces, and heat-transport losses, not area alone.

The simplified heat-rejection equation is:

`Q/A = epsilon * sigma * (T_rad^4 - T_sink^4)`

For the sensitivity below, this document uses the same working assumptions as the local thermal work:

- emissivity `epsilon = 0.85` as a good radiator-coating assumption;
- effective sink `T_sink = 250 K` as a LEO/SSO planning value that includes Earth IR and albedo backload;
- one effective radiating face;
- radiator areal density `5 kg/m2` as a midpoint system-level value including panel, transport, fluid, and deployment allowance.

Those are project assumptions, not certified vendor values. They match the local assumptions in [hot_chip_thermal_trajectory.md](hot_chip_thermal_trajectory.md), [solar_radiator_trajectory.md](solar_radiator_trajectory.md), and [thermal_analysis.md](../orbital/thermal_analysis.md).

### Quantitative sensitivity

The table below shows the project-level derived math. It is not a vendor radiator datasheet. It answers: if the radiator surface can be run at a given temperature, what heat flux and mass-per-kW follow under the stated assumptions?

| Radiator surface temperature | Net flux, one effective face | Area per kW | Radiator mass per kW at 5 kg/m2 | Source status |
|---:|---:|---:|---:|---|
| 40 C | 275 W/m2 | 3.63 m2/kW | 18.17 kg/kW | derived estimate |
| 50 C | 337 W/m2 | 2.97 m2/kW | 14.82 kg/kW | derived estimate |
| 60 C | 405 W/m2 | 2.47 m2/kW | 12.33 kg/kW | derived estimate |
| 70 C | 480 W/m2 | 2.08 m2/kW | 10.42 kg/kW | derived estimate |
| 75 C | 520 W/m2 | 1.92 m2/kW | 9.62 kg/kW | derived estimate |
| 80 C | 561 W/m2 | 1.78 m2/kW | 8.91 kg/kW | derived estimate |
| 90 C | 650 W/m2 | 1.54 m2/kW | 7.69 kg/kW | derived estimate |
| 100 C | 746 W/m2 | 1.34 m2/kW | 6.70 kg/kW | derived estimate |

For the current 2036 default node power of roughly 421.98 kW, those same assumptions imply:

| Radiator surface temperature | Radiator mass per 421.98 kW node | 90-node cohort radiator mass | Source status |
|---:|---:|---:|---|
| 40 C | 7.67 t/node | 690 t | derived estimate |
| 50 C | 6.25 t/node | 563 t | derived estimate |
| 60 C | 5.20 t/node | 468 t | derived estimate |
| 70 C | 4.40 t/node | 396 t | derived estimate |
| 75 C | 4.06 t/node | 365 t | derived estimate |
| 80 C | 3.76 t/node | 338 t | derived estimate |

This explains the power of hotter radiator operation:

- 40 C to 80 C roughly halves mass under the stated assumptions.
- 60 C to 80 C saves about 28% of radiator mass.
- 70 C to 80 C saves about 15% of radiator mass.

This also clarifies the current model dial. The default post-hot-loop radiator mass is `0.012 t/kW`, or 12 kg/kW. Under this simplified one-face, 250 K sink, 5 kg/m2 calculation, 12 kg/kW corresponds to a radiator surface a little above 60 C. If the architecture truly reaches an 80 C radiator surface and keeps the effective areal density near 5 kg/m2, the physics-only value would be closer to 0.009 t/kW. If the real co-mounted system has higher effective areal density, nonuniform panels, headers, deployment mass, imperfect view factors, or single-face penalties, then 0.012 t/kW can still be consistent with an 80 C hot-loop architecture.

So the current `0.012 t/kW` default is best described as:

> Conservative relative to an idealized 80 C / 5 kg/m2 radiator, plausible for a single-face co-mounted architecture with system penalties, and still unresolved until a chip-to-coolant-to-panel thermal model exists.

The current model step from `0.013 t/kW` to `0.012 t/kW` is only about a 7.7% reduction. That is much smaller than the theoretical 40 C to 80 C radiator-temperature benefit, which means the current model is not aggressively banking the full hot-loop physics. It is mostly using a guarded single-face co-mounted radiator dial.

## 2030 Trajectory

The likely 2030 direction is **warmer coolant and better heat transport**, not dramatically higher safe junction temperatures.

What appears plausible by 2030:

- 40-45 C facility water is likely to be normal for high-density AI liquid cooling where climate and facility design allow it, because ASHRAE already defines W40/W45/W+ classes and public AI-cooling discussion is moving in that direction ([ASHRAE reference card](https://www.ashrae.org/file%20library/technical%20resources/bookstore/supplemental%20files/therm-gdlns-5th-r-e-refcard.pdf), [CoolIT](https://www.coolitsystems.com/resources/news/warm-water-cooling-and-ai-the-future-is-here-but-its-not-chiller-free/)).
- Technology-cooling-system classes and design conversations are reaching S50, or 50 C, but ASHRAE-facing material also warns that facility water temperature is not identical to IT inlet temperature and that liquid-cooling resiliency is a major concern ([ASHRAE Dallas 2025 presentation](https://dallas-ashrae.org/images/meeting/041625/the_ashrae_thermal_guidelines_for_data_centers_____past__present_and_future.pdf)).
- NVIDIA/Vera Rubin public discussion supports 45 C warm-water cooling as a credible near-term product direction, but this should be treated as public roadmap/cooling-architecture evidence, not a full thermal-resistance guarantee for an orbital radiator ([Fierce Network](https://www.fierce-network.com/cloud/nvidia-has-no-chill), [CoolIT](https://www.coolitsystems.com/resources/news/warm-water-cooling-and-ai-the-future-is-here-but-its-not-chiller-free/)).
- Higher heat flux and rack power will force better cold plates, CDUs, pumps, manifolds, and possibly two-phase technologies. Redwire's orbital data-center paper says heat transport distance, interfaces, radiator temperature, view factors, and thermal losses become increasingly important as scale rises ([Redwire ODC white paper](https://rdw.com/wp-content/uploads/2026/05/RDW26-053-ODC-Power-Thermal-Study-White-Paper-R11-Digital.pdf)).

What is not yet safe to assume:

- A public, certified NVIDIA/Rubin/Feynman junction limit meaningfully above today's practical 83-90 C band.
- A 70-80 C **radiator surface** on a single-phase loop without enough thermal-resistance margin to protect junction temperature.
- A 100 C or higher radiator surface with commodity GPU/HBM packages unless the architecture uses two-phase transport, lower package thermal resistance, derating, or future silicon/package materials that are not currently public.
- A direct cost reduction from higher temperature unless the radiator cost model is changed from "$/kW scenario dial" to an area/mass/BOM-linked cost model.

## What Would Have To Be True For 70-80 C Radiator Assumptions

A 70-80 C radiator surface is plausible but not proven. To make it credible, the project needs one of these pathways:

1. **Single-phase hot-loop path.** The coolant return temperature must be high enough that the radiator surface can sit around 70-80 C after panel gradients, while junction temperatures stay below throttling and reliability limits. This likely requires excellent cold plates, high flow, careful manifold design, and derating.

2. **Two-phase / heat-pipe path.** The chip-side evaporator and radiator-side condenser can move heat with smaller effective temperature differences, or can maintain a near-isothermal transport path. This may support hotter radiator panels without equally hot junctions, but it adds microgravity fluid-management and failure-mode risk.

3. **Thermal-resistance reduction path.** Packaging, cold plates, thermal interface materials, and loop design improve enough by 2030 that the same junction limit can support a hotter radiator surface.

4. **Reliability trade path.** The system accepts a modest increase in junction temperature but derates voltage/frequency and sizes the business model for lower throughput or higher failure rate. This is less attractive but may be usable for inference if graceful degradation is strong.

The key point for the user question is that **hotter allowable chip operation could close part of the premium gap only indirectly**. It closes mass and perhaps cost if it allows a smaller radiator. It does not reduce solar cost, launch cost, or GPU package cost. And if the current model already charges radiator cost by kW rather than area, then higher temperature will not automatically lower modeled cost until the radiator cost dial or cost model is changed.

## Public-Safe Claims

Safe:

- Modern AI accelerators produce rack-scale heat loads that require liquid cooling; GB200 NVL72 is officially a liquid-cooled 72-GPU rack-scale system ([NVIDIA GB200 NVL72](https://www.nvidia.com/en-gb/data-center/gb200-nvl72/)).
- H100 and B200-class public materials show accelerator module powers in the hundreds of watts to 1000 W class, which explains why direct liquid cooling and thermal design dominate ([NVIDIA H100](https://www.nvidia.com/en-eu/data-center/h100/), [Lenovo B200 product guide](https://lenovopress.lenovo.com/lp2226.pdf)).
- ASHRAE liquid-cooling classes already include 40 C, 45 C, and above-45 C facility-water classes, and 2025 ASHRAE-facing materials discuss technology-cooling-system classes up to 50 C ([ASHRAE reference card](https://www.ashrae.org/file%20library/technical%20resources/bookstore/supplemental%20files/therm-gdlns-5th-r-e-refcard.pdf), [ASHRAE Dallas 2025 presentation](https://dallas-ashrae.org/images/meeting/041625/the_ashrae_thermal_guidelines_for_data_centers_____past__present_and_future.pdf)).
- In orbit, radiator area/mass improves strongly with higher radiator surface temperature because heat rejection follows the Stefan-Boltzmann T^4 relationship; local project calculations show roughly a 40-50% mass reduction when moving from conservative cool-surface assumptions toward a 70-80 C hot-loop band.
- The current `0.012 t/kW` post-hot-loop default is plausible for a conservative single-face co-mounted radiator, but it is not source-certified.

Unsafe:

- "NVIDIA publicly guarantees future GPUs can run at 100 C junction temperature."
- "A 45 C facility-water class means the radiator surface can be 80 C."
- "An 80 C radiator proves the orbital premium falls to 50%."
- "The current model fully captures the cost-down from higher radiator temperature."
- "Hotter chips solve the thermal problem." The correct claim is that hotter coolant/radiator operation is one lever, constrained by reliability and thermal resistance.
- "Two-phase cooling is a solved default for this spacecraft." It is promising, but large high-power orbital data-center implementation remains unresolved.

## Implications For Model Defaults

1. **Keep `0.012 t/kW` as a cautious default for now.** It is not absurd; it is roughly equivalent to a 60 C radiator surface with 5 kg/m2 effective areal density, or to a hotter surface with heavier/nonideal system penalties.

2. **Rename or clarify `tjmax_lift_year`.** The model currently uses a "Tjmax lift" phrase, but the real mechanism should be "hot-loop / radiator-temperature / thermal-resistance improvement." Public evidence supports warmer coolant loops more strongly than it supports a certified increase in GPU junction limits.

3. **Separate radiator temperature from chip junction temperature in JSON.** A future model should expose at least:
   - assumed junction design target;
   - coolant supply temperature;
   - coolant return temperature;
   - radiator surface temperature;
   - effective sink temperature;
   - emissivity;
   - effective areal density;
   - one-face/two-face or co-mounted architecture;
   - derived kg/kW.

4. **Do not link radiator cost-down only to temperature yet.** Higher temperature can reduce area/mass. It may reduce cost if cost scales with panel area/BOM. But the current model's radiator cost is a direct `$M/kW` dial, not an area-based cost model. A cost-down sensitivity should say explicitly whether `$20k/kW` comes from production learning, area reduction, internal build margin, simpler co-mounted architecture, or all of the above.

5. **Validation should track this as an unresolved but high-leverage research item.** The key unresolved question is not "Can chips get hotter?" It is "Can the system run a 70-80 C radiator surface while preserving junction reliability and a five-year service-life assumption?"

## Unresolved Questions

- What are the vendor-certified junction, slowdown, and shutdown thresholds for B200, B300, Rubin, and Feynman-class data-center accelerators?
- What junction temperature does NVIDIA/OEM guidance recommend for sustained 24/7 high-utilization operation, not just absolute throttling survival?
- What are realistic chip-to-coolant and coolant-to-radiator thermal resistances for a space-qualified direct-liquid or two-phase architecture?
- Can a single-face co-mounted solar/radiator architecture reach a 70-80 C effective radiator surface while maintaining favorable deep-space view factors?
- What is the mass and reliability penalty for two-phase transport in this power class under microgravity, launch vibration, and five-year unserviceable operation?
- How much of the radiator cost is area/material/deployment mass versus engineering, qualification, and supplier margin?
- If Rocket Lab builds solar internally and partners/builds radiator hardware, how much external supplier margin is being conservatively included in current `$40k/kW` assumptions?

## Sources

Local project sources:

- [hot_chip_thermal_trajectory.md](hot_chip_thermal_trajectory.md)
- [thermal_analysis.md](../orbital/thermal_analysis.md)
- [radiator_costdown_2030_2036.md](radiator_costdown_2030_2036.md)
- [SOURCE_INDEX.md](../SOURCE_INDEX.md) claims `THR-014`, `THR-015`, and `THR-018`

External sources:

- [NVIDIA H100](https://www.nvidia.com/en-eu/data-center/h100/) and [NVIDIA H100 PCIe product brief](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf), public H100 product and thermal-limit references.
- [Lenovo ThinkSystem NVIDIA B200 180GB 1000W GPU](https://lenovopress.lenovo.com/lp2226.pdf) and [NVIDIA GB200 NVL72](https://www.nvidia.com/en-gb/data-center/gb200-nvl72/), current high-power AI accelerator context.
- [ASHRAE thermal-guidelines reference card](https://www.ashrae.org/file%20library/technical%20resources/bookstore/supplemental%20files/therm-gdlns-5th-r-e-refcard.pdf) and [Dallas ASHRAE 2025 presentation](https://dallas-ashrae.org/images/meeting/041625/the_ashrae_thermal_guidelines_for_data_centers_____past__present_and_future.pdf), liquid-cooling temperature-class context.
- [NASA SmallSat thermal control](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/) and [NASA 2024 thermal chapter PDF](https://www.nasa.gov/wp-content/uploads/2025/02/7-soa-thermal-2024.pdf), orbital radiator and thermal-interface context.
- [Redwire orbital data-center power and thermal white paper](https://rdw.com/wp-content/uploads/2026/05/RDW26-053-ODC-Power-Thermal-Study-White-Paper-R11-Digital.pdf), ODC-scale thermal architecture context.
- [Electronics Cooling 10 C reliability-rule discussion](https://www.electronics-cooling.com/2017/08/10c-increase-temperature-really-reduce-life-electronics-half/), reliability heuristic and cautionary framing.

## Proposed Tracker / Library Entry Text

Proposed `LIBRARY.md` entry under Node Design:

| File | What it is | Key takeaway |
|---|---|---|
| [gpu_temperature_cooling_limits.md](gpu_temperature_cooling_limits.md) | GPU/package temperature, liquid-cooling, and orbital radiator-temperature research. | Warmer coolant and hotter radiator operation are plausible high-leverage levers, but junction temperature, coolant temperature, and radiator surface temperature must be kept separate. |

Proposed `RESEARCH_TRACKER.md` entry under Node Design:

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [gpu_temperature_cooling_limits.md](gpu_temperature_cooling_limits.md) | draft | Clarifies GPU junction/coolant/radiator temperature definitions and tests whether hotter operation can reduce orbital radiator mass/cost by 2030. | Public evidence supports warmer liquid-cooling loops and T^4 radiator leverage; exact future GPU junction limits and chip-to-radiator thermal resistance remain unresolved. |

Suggested `SOURCE_INDEX.md` claim additions for later integration:

| Claim ID | Claim text | Source status | Role | Links or internal references | Uncertainty notes |
|---|---|---|---|---|---|
| `THR-013` | ASHRAE liquid-cooling classes include W40, W45, and W+ facility-water supply classes, with 45 C and above-45 C operation part of the public data-center cooling envelope. | certified | Supporting source claim | ASHRAE reference card; ASHRAE Dallas 2025 presentation | Facility water supply is not automatically equal to IT inlet or radiator surface temperature. |
| `THR-014` | A 70-80 C radiator surface materially reduces radiator area/mass versus a 40-50 C surface under the project thermal assumptions. | derived_estimate | Model input support / sensitivity | This document; hot_chip_thermal_trajectory.md; thermal_analysis.md | Depends on sink temperature, emissivity, effective face count, areal density, view factors, and thermal-resistance chain. |
| `THR-015` | Current public evidence supports warmer coolant-loop trajectories more strongly than it supports a certified increase in future GPU junction limits. | sourced_estimate | Public wording guard | NVIDIA forum, ASHRAE materials, CoolIT, DCD, Fierce Network | Vendor/OEM thermal threshold data may exist under partner access but is not public in this research pass. |
