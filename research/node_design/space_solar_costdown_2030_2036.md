# Space Solar Cost-Down, 2030-2036

**Status:** draft research  
**Date:** 2026-05-27  
**Topic owner:** Research Agent Solar  
**Scope:** non-code research for the RKLB orbital data-center research wiki  
**Source-status summary:** Rocket Lab's silicon-array program and vertical-integration claims are `certified` from Rocket Lab public materials. The current model's `$40k/kW` solar default is a `scenario`. A `$20k/kW` solar case is a `scenario` / `sourced-directional sensitivity`, not a certified Rocket Lab cost. Public sources support the direction of lower-cost space solar, but no public source certifies Rocket Lab integrated data-center array cost, W/kg, W/m2, degradation, or delivered five-year EOL power.

---

## Central Question

Can the model plausibly add a 2030-2036 solar cost-down sensitivity where space solar falls from the current default of `$40k/kW` (`$40/W`) to about `$20k/kW` (`$20/W`) for Rocket Lab / SolAero-style silicon arrays, five-year orbital data-center infrastructure, and high-volume internal production?

This matters because the current promoted 2036 space model deploys `90` nodes, each at `421.9776 kW`, for a same-year cohort of `37.978 MW` (`90 * 421.9776 kW`) and a solar cost line of about `$1.519B` (`90 * 421.9776 kW * $0.04M/kW`) in [data_center/models/space/default.json](../../data_center/models/space/default.json). The ground comparison uses a five-year ground reference cost of about `$3.677B`, while the orbital build-plus-launch reference is about `$7.048B`, or `1.9168x` ground, in [data_center/models/ground/default.json](../../data_center/models/ground/default.json).

If solar alone were halved to `$20k/kW`, the 2036 solar line would fall by about `$0.760B`, from `$1.519B` to `$0.760B`. Holding every other default constant, orbital cost would fall from about `$7.048B` to about `$6.288B`, and the all-in orbital / ground ratio would move from about `1.92x` to about `1.71x`. That is meaningful, but it does not by itself reach parity. The larger `~1.50x` cost-down case requires both solar and radiator cost to be halved; radiator is covered by a separate research item.

---

## Current State

### What Public Sources Say About Space Solar Costs

Rocket Lab's February 26, 2026 announcement is directly relevant because it is not a generic solar announcement: Rocket Lab says the arrays are designed for "gigawatt-scale space-based data centers" and says they deliver "low cost per watt at industrial scale" through "mass-manufacturable, lightweight, and modular systems" ([Rocket Lab silicon-array announcement](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/); same announcement on [Rocket Lab investor relations](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-introduces-advanced-silicon-solar-arrays-power-space)). This supports the direction of a lower-cost solar sensitivity, but Rocket Lab does not publish dollars per watt.

Rocket Lab also says it is the "only fully vertically integrated space power supplier," with solar cells, assemblies, modules, substrates, panels, and array wings under one roof, and says its automation supports higher production volumes at lower cost ([Rocket Lab Solar Solutions](https://rocketlabcorp.com/space-systems/solar/); [Rocket Lab investor-relations announcement](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-introduces-advanced-silicon-solar-arrays-power-space)). This is important because an external purchase-price analog may overstate Rocket Lab's internal economic cost if supplier margin is internalized.

Older space-solar cost references are much higher. A National Academies / NASA space solar power assessment reports space arrays at roughly `$300-$1,000/W` and state-of-the-art arrays at roughly `$500-$1,000/W` in the early-2000s source base, with specific powers around `30-60 W/kg` for state-of-practice arrays and `70-100 W/kg` for state-of-the-art arrays ([National Academies assessment](https://www.nationalacademies.org/read/10202/chapter/5)). Those numbers are stale for modern commercial high-volume smallsat supply, but they explain why the project should not treat any low-cost claim as automatically validated.

Current low-cost vendor claims are much lower, but they are not yet proof for a `38 MW/year` orbital data-center wing. Starpath advertises Starlight Classic at `$11.2/W`, `19%` efficiency, `900 g/m2`, silicon technology, and Starlight Air at `$15/W`, `16%` efficiency, and as low as `73 g/m2` ([Starpath / Starlight product page](https://terawatt.space/)). Dealroom's SpaceTech summary reports the same `$15/W` Starlight Air and `$11.20/W` Classic values and flags the scaling risk because Starpath has not yet built large-scale production capacity ([Dealroom SpaceTech summary](https://spacetech.dealroom.co/news/note/starpath-pivots-to-space-solar-with-ultra-thin-15-w-panels)). Treat these as market signals, not mature procurement anchors for Rocket Lab.

Source Energy's public pages also support the direction of lower-cost commercial space solar: it describes "financially sustainable" space energy solutions and deployable high-power arrays with aluminum-boom cost-optimized and carbon-fiber high-performance variants ([Source large deployable arrays](https://www.source.space/products/large-solar-deployable-arrays); [Source about page](https://www.source.space/pages/about)). I did not find a current live Source page that explicitly certifies the previously discussed `$29/W` number, so this memo does not use `$29/W` as a hard input.

### Silicon vs. GaAs / Germanium

Rocket Lab's silicon announcement explicitly frames the issue as a supply-chain and scalability trade. It states that conventional space cells have typically used gallium arsenide and germanium for radiation tolerance, that both are constrained critical-mineral supply chains, and that silicon is the answer for constellation-scale and orbital data-center scale ([Rocket Lab silicon-array announcement](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/); [Rocket Lab investor-relations announcement](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-introduces-advanced-silicon-solar-arrays-power-space)).

Rocket Lab's current solar product page also says its latest cells and CICs achieve efficiencies up to `34%` and that it offers triple-junction, quad-junction, and five-junction space-qualified technologies ([Rocket Lab Solar Solutions](https://rocketlabcorp.com/space-systems/solar/)). That is not a silicon-specific efficiency statement; it is the high-performance SolAero / Rocket Lab cell portfolio. The silicon array is a separate cost-down / scale product, and Rocket Lab has not disclosed its efficiency, W/kg, W/m2, degradation, or array-level dollars per watt.

NASA's 2026 Small Spacecraft State of the Art report describes the continuing progression of small spacecraft power systems and cautions that technology maturity depends on payload, mission requirements, reliability, and environment ([NASA Small Spacecraft SOA 2026](https://www.nasa.gov/smallsat-institute/sst-soa/); [NASA SOA 2026 PDF](https://www.nasa.gov/wp-content/uploads/2026/05/soa-2026.pdf)). NASA's planetary solar-power technology assessment emphasizes that high-power solar arrays need low mass, low volume, high reliability deployment, and high specific power; it also notes that solar array mass is inversely proportional to specific power ([NASA/JPL Solar Power Technologies report](https://science.nasa.gov/wp-content/uploads/2023/09/Solar_Power_Tech_Report_FINAL.pdf)).

Recent review literature keeps the same basic tradeoff: III-V / GaAs multijunction cells remain the high-performance benchmark for efficiency and radiation durability, while silicon and other emerging materials trade performance against cost, mass, scalability, and environment-specific durability ([Space Photovoltaics review](https://www.mdpi.com/2079-9292/15/10/1978)).

### Specific Power, Degradation, Integrated Array vs. Cell Cost, and Qualification

The model cannot treat cell cost as array cost. The data-center node needs an integrated wing: cells or modules, substrate, deployment structure, harnessing, PMAD interface, qualification, margins, and EOL power sizing. Redwire's public ROSA table shows current high-power deployable products ranging from `3.3 kW` at `36 kg` to `37 kW` at `521 kg`, or roughly `71-92 W/kg` across the listed configurations (`3,300 W / 36 kg` and `37,000 W / 521 kg`) ([Redwire ROSA product page](https://rdw.com/product-archive/power/rosa/)). Redwire also says ROSA has LEO, GEO, and deep-space heritage and is intended for demanding power, volume, and mass requirements ([Redwire ROSA product page](https://rdw.com/product-archive/power/rosa/)).

Redwire's March 2026 ELSA announcement is a useful directional comparator: it says ELSA uses ROSA heritage and parallel production, is intended for mass-manufactured satellites, provides up to `50%` more power by volume than traditional solar arrays, and is designed to remain competitive with conventional solar array performance and pricing ([Redwire ELSA announcement PDF](https://d1io3yog0oux5.cloudfront.net/_f54cc955dc237a2d13ec3d03fb7ff03b/redwirespace/news/2026-03-03_Redwire_Announces_New_High_Performance_Low_Mass_218.pdf)). This supports the broader market direction: stowed volume, modularity, and production approach are improving. It does not certify Rocket Lab's cost.

Radiation degradation remains mission-specific. The NASA/JPL solar-power report states that radiation degradation depends on radiation environment, shielding design, cover-glass thickness, contamination environment, and mission duration ([NASA/JPL Solar Power Technologies report](https://science.nasa.gov/wp-content/uploads/2023/09/Solar_Power_Tech_Report_FINAL.pdf)). The same report includes degradation data for space cells at `1E15 1 MeV e/cm2`, with normalized maximum power degradation values around `0.85-0.90` depending on source/test method in its summary table ([NASA/JPL Solar Power Technologies report](https://science.nasa.gov/wp-content/uploads/2023/09/Solar_Power_Tech_Report_FINAL.pdf)). Those values should not be applied directly to this LEO / SSO data-center architecture without an orbit-specific radiation model, but they show why EOL sizing cannot be ignored.

---

## 2030-2036 Trajectory

### What Could Plausibly Improve

The strongest cost-down mechanisms are production and architecture, not a magic cell-efficiency jump.

Rocket Lab's own cost-down path is vertical integration plus silicon. It already operates SolAero-derived space solar manufacturing, says it has the world's largest installed production capacity for GaAs/germanium-based solar arrays, and says adding silicon reduces reliance on critical-mineral supply chains while enabling constellation-scale production ([Rocket Lab investor-relations announcement](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-introduces-advanced-silicon-solar-arrays-power-space); [Rocket Lab Solar Solutions](https://rocketlabcorp.com/space-systems/solar/)).

The broader market is also moving toward modular, high-volume, lower-cost space solar. Redwire's ELSA is explicitly designed for standardized modular power and higher-volume production ([Redwire ELSA announcement PDF](https://d1io3yog0oux5.cloudfront.net/_f54cc955dc237a2d13ec3d03fb7ff03b/redwirespace/news/2026-03-03_Redwire_Announces_New_High_Performance_Low_Mass_218.pdf)). Starpath is publicly advertising space solar products at `$11.2/W` to `$15/W`, albeit with scaling and heritage caveats ([Starpath / Starlight product page](https://terawatt.space/); [Dealroom SpaceTech summary](https://spacetech.dealroom.co/news/note/starpath-pivots-to-space-solar-with-ultra-thin-15-w-panels)). These sources make `$20/W` (`$20k/kW`) by 2036 plausible as a scenario, especially for a five-year, high-volume LEO fleet.

The five-year life matters because it may relax some design margins relative to `15-20+` year GEO spacecraft. NASA's planetary solar-power assessment lists `15 years` as a high-reliability need for future high-power planetary mission contexts, which is longer than the project's five-year service-life assumption ([NASA/JPL Solar Power Technologies report](https://science.nasa.gov/wp-content/uploads/2023/09/Solar_Power_Tech_Report_FINAL.pdf)). A shorter LEO service life can plausibly reduce EOL margin, cover-glass burden, and qualification conservatism. That is a sensitivity argument, not a license to ignore radiation, thermal cycling, micrometeoroid risk, deployment reliability, or array contamination.

### What Cannot Be Assumed

Do not assume Rocket Lab's silicon arrays are cheaper and lighter at the same time. Silicon is lower cost and more scalable, but public sources still indicate III-V / GaAs architectures are the high-efficiency, high-radiation-durability benchmark for space ([Space Photovoltaics review](https://www.mdpi.com/2079-9292/15/10/1978); [Rocket Lab Solar Solutions](https://rocketlabcorp.com/space-systems/solar/)). If silicon efficiency is materially lower than III-V, the same kW requires more area, more structure, more deployment volume, more drag, and potentially more EOL margin.

Do not assume low advertised panel prices translate to a full orbital data-center solar wing. Starpath's public prices are valuable market signals, but the product scale, heritage, radiation qualification, integrated deployment hardware, and large-array power management differ from a `421.98 kW` node and `37.98 MW/year` deployment cohort ([Starpath / Starlight product page](https://terawatt.space/); [Dealroom SpaceTech summary](https://spacetech.dealroom.co/news/note/starpath-pivots-to-space-solar-with-ultra-thin-15-w-panels)).

Do not assume a public `$20/W` Rocket Lab cost. Rocket Lab says low cost per watt; it does not publish the number ([Rocket Lab silicon-array announcement](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/); [Rocket Lab investor-relations announcement](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-introduces-advanced-silicon-solar-arrays-power-space)).

---

## Rocket Lab Vertical Integration / SolAero Implications

Rocket Lab's vertical integration is a real thesis advantage. The company says it provides cells, CICs, modules, substrates, panels, and complete array wings under one roof ([Rocket Lab Solar Solutions](https://rocketlabcorp.com/space-systems/solar/); [Rocket Lab investor-relations announcement](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-introduces-advanced-silicon-solar-arrays-power-space)). It also says automated manufacturing and assembly support higher volumes at lower cost, which is directly aligned with the orbital data-center problem ([Rocket Lab Solar Solutions](https://rocketlabcorp.com/space-systems/solar/)).

For this model, internal production creates a conservative-bias argument: if the cost dial is based on what an outside customer might pay for solar arrays, Rocket Lab's internal economic cost may be lower because some supplier margin is internalized. That does not justify lowering the default by itself because Rocket Lab does not disclose internal cost, margin, yield, or array-level $/W. It does justify adding a clearly labelled cost-down sensitivity.

The vertical-integration point should be framed as:

> Rocket Lab's in-house solar stack may make external purchase-price analogs conservative, but the model keeps `$40k/kW` as the default until Rocket Lab publishes cost/performance data or the project builds a bottom-up internal-cost estimate. `$20k/kW` is a plausible 2036 sensitivity, not a certified cost.

---

## Five-Year-Life Argument

The five-year orbital data-center service life is a plausible reason to model a cheaper solar array than a long-lived GEO or deep-space spacecraft, but it is not a complete answer.

Why it helps:

- Five years is shorter than the `15 years` cited in NASA/JPL future high-power mission needs, so less EOL degradation reserve may be needed than for long-life missions ([NASA/JPL Solar Power Technologies report](https://science.nasa.gov/wp-content/uploads/2023/09/Solar_Power_Tech_Report_FINAL.pdf)).
- A LEO / SSO data-center fleet can be refreshed, so the project may accept lower per-array longevity than a one-off flagship spacecraft.
- High-volume internal production can make replacement and learning curves part of the system design, instead of treating every array as a bespoke one-off.

What risks remain:

- Radiation degradation, cover-glass thickness, contamination, thermal cycling, and mission duration still control EOL power, and NASA/JPL explicitly lists these as degradation drivers ([NASA/JPL Solar Power Technologies report](https://science.nasa.gov/wp-content/uploads/2023/09/Solar_Power_Tech_Report_FINAL.pdf)).
- A shorter life does not remove deployment reliability requirements. A failed deployment can lose the node on day one.
- Silicon may be cheaper but less efficient and potentially more area-intensive than high-efficiency III-V arrays. More area can increase deployment structure and drag.
- Qualification cost does not scale down to zero just because design life is five years.

---

## 2036 Solar Cost Range

All dollar values below are array-level cost scenarios for the project model, expressed as `$/kW` and `$/W`. They are not Rocket Lab published costs.

| 2036 case | Cost | Source status | Rationale |
|---|---:|---|---|
| Aggressive cost-down | `$20k/kW` (`$20/W`) | `scenario` with sourced directional support | Plausible if Rocket Lab's silicon arrays scale, internal production avoids supplier margin, five-year LEO life reduces longevity margin, and low-cost space-solar vendor claims survive qualification. Starpath advertises `$11.2/W` and `$15/W` products, while Rocket Lab says silicon arrays target low cost per watt at industrial scale ([Starpath](https://terawatt.space/); [Dealroom SpaceTech](https://spacetech.dealroom.co/news/note/starpath-pivots-to-space-solar-with-ultra-thin-15-w-panels); [Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/)). |
| Central researched sensitivity | `$30k/kW` (`$30/W`) | `scenario` / `sourced_estimate` | Splits the difference between current cautious default and aggressive vendor-claim direction. Better public support than `$20/W`, but still not certified because integrated Rocket Lab wing cost is unpublished. |
| Current cautious default | `$40k/kW` (`$40/W`) | `scenario` | Conservative enough for public default while source quality remains incomplete. It is below old space-array cost references but above emerging low-cost vendor claims; it protects the model from overclaiming ([National Academies](https://www.nationalacademies.org/read/10202/chapter/5); [Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/)). |
| Stress case | `$50-70k/kW` (`$50-70/W`) | `scenario` | Use if integrated deployment hardware, EOL margin, qualification, low yield, or silicon area penalty dominates. This remains far below old `$300-$1,000/W` references but may be appropriate if the low-cost market claims fail to mature ([National Academies](https://www.nationalacademies.org/read/10202/chapter/5)). |

Interpretation: `$20k/kW` is not a wild sensitivity by 2036, but it is not strong enough to replace `$40k/kW` as the default. `$30k/kW` could be a useful mid sensitivity if the project wants a smoother cost-down ladder.

---

## Public-Safe Claims

- Rocket Lab has publicly announced silicon solar arrays for gigawatt-scale space-based data centers ([Rocket Lab silicon-array announcement](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/)).
- Rocket Lab says those arrays target low cost per watt at industrial scale using mass-manufacturable, lightweight, modular systems ([Rocket Lab silicon-array announcement](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/)).
- Rocket Lab is vertically integrated in space power, offering cells, modules, panels, substrates, and complete array wings ([Rocket Lab Solar Solutions](https://rocketlabcorp.com/space-systems/solar/)).
- Rocket Lab says silicon reduces reliance on gallium arsenide / germanium supply chains, while hybrid arrays can trade cost, schedule, size, weight, power, and performance ([Rocket Lab investor-relations announcement](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-introduces-advanced-silicon-solar-arrays-power-space)).
- The current model's `$40k/kW` solar default is a conservative scenario, not a certified Rocket Lab cost.
- A `$20k/kW` solar value is plausible as a 2036 sensitivity under high-volume, vertically integrated, five-year LEO infrastructure assumptions.

## Unsafe Claims

- "Rocket Lab solar costs `$20k/kW`."
- "Rocket Lab solar costs `$40k/kW`."
- "The project has validated a `$20k/kW` solar default."
- "Silicon arrays are both cheaper and lighter than GaAs arrays for this data-center node."
- "A five-year service life removes the need for radiation or degradation margin."
- "Starpath or Source pricing proves Rocket Lab can deliver a `38 MW/year` integrated orbital data-center solar deployment at the same price."

---

## Implications For Model Defaults

Keep `$40k/kW` as the public default for solar until one of three things happens:

- Rocket Lab publishes integrated silicon-array $/W, W/kg, W/m2, EOL degradation, or large-wing architecture.
- The project builds a bottom-up internal-cost estimate for Rocket Lab / SolAero silicon array production.
- Multiple high-volume space-solar suppliers demonstrate qualified, delivered, integrated arrays near `$20/W` at relevant scale.

Add a named sensitivity:

```text
solar_costdown_2036
solar_cost_musd_per_kw = 0.02
source_status = scenario
rationale = 2036 cost-down sensitivity supported by Rocket Lab silicon-array direction, vertical integration, five-year LEO fleet life, and emerging low-cost space-solar vendor claims; not a certified Rocket Lab cost.
```

Optional second sensitivity:

```text
solar_costdown_mid_2036
solar_cost_musd_per_kw = 0.03
source_status = scenario / sourced_estimate
rationale = middle case between current default and aggressive cost-down; use when avoiding a binary $40/W vs $20/W framing.
```

For public documentation, the safest wording is:

> The default model keeps solar at `$40k/kW` as a conservative scenario. Rocket Lab's silicon-array program, vertical integration, and emerging low-cost space-solar market signals make `$20k/kW` plausible as a 2036 sensitivity, especially for a five-year, high-volume LEO infrastructure fleet. The project does not treat `$20k/kW` as a certified Rocket Lab cost.

---

## Unresolved Questions

- What is Rocket Lab's integrated silicon-array cost per watt at wing level, not just cell or module level?
- What are Rocket Lab silicon arrays' specific power, deployed W/m2, stowed volume, EOL degradation, and qualification envelope?
- How much array oversizing is required for a five-year dawn-dusk SSO service life after radiation, thermal cycling, contamination, and pointing losses?
- Does lower-cost silicon increase deployed area enough to create drag, deployment, or structure penalties that erase part of the cost benefit?
- Can emerging low-cost vendors such as Starpath deliver their advertised cost and durability at meaningful production scale, or are those prices early-market claims?
- Should the model represent Rocket Lab internal cost separately from external purchase-price analogs for solar?

---

## Sources

Local project sources:

- [solar_radiator_trajectory.md](solar_radiator_trajectory.md)
- [SOURCE_INDEX.md](../SOURCE_INDEX.md) claim `THR-013`
- `code/scenarios/default.yaml` solar cost and mass dials

External sources:

- [Rocket Lab advanced silicon solar arrays announcement](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/), official company announcement, 2026-02-26.
- [Rocket Lab Solar Solutions](https://rocketlabcorp.com/space-systems/solar/), official space-solar products and capability page.
- [NASA Small Spacecraft Technology State of the Art](https://www.nasa.gov/smallsat-institute/sst-soa/) and [NASA 2026 SoA PDF](https://www.nasa.gov/wp-content/uploads/2026/05/soa-2026.pdf), power and spacecraft technology context.
- [NASA/JPL Solar Power Technologies for Future Planetary Science Missions](https://science.nasa.gov/wp-content/uploads/2023/09/Solar_Power_Tech_Report_FINAL.pdf), space solar technology and degradation context.
- [National Academies space solar power assessment](https://www.nationalacademies.org/read/10202/chapter/5), historical cost and space-solar investment context.
- [Redwire ROSA](https://rdw.com/product-archive/power/rosa/), deployable solar-array mass/power heritage.
- [TeraWatt](https://terawatt.space/), [Starpath coverage](https://spacetech.dealroom.co/news/note/starpath-pivots-to-space-solar-with-ultra-thin-15-w-panels), and [Source.Space large deployable arrays](https://www.source.space/products/large-solar-deployable-arrays), early-market signals for lower-cost deployable space power. Treat vendor/press claims as directional, not certified defaults.

## Proposed Tracker / Library Entry Text

Suggested `LIBRARY.md` entry:

| File | What it is | Key takeaway |
|---|---|---|
| [space_solar_costdown_2030_2036.md](space_solar_costdown_2030_2036.md) | Fresh solar cost-down research for 2030-2036. | `$20k/kW` solar is plausible as a 2036 sensitivity, but `$40k/kW` should remain the public default until Rocket Lab publishes integrated array cost/performance or the project builds a bottom-up internal-cost model. |

Suggested `RESEARCH_TRACKER.md` entry:

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [space_solar_costdown_2030_2036.md](space_solar_costdown_2030_2036.md) | draft | Tests whether solar can fall from `$40k/kW` to `$20k/kW` by 2030-2036 for Rocket Lab silicon orbital data-center arrays. | Public sources support `$20k/kW` as a scenario sensitivity, not a certified default; Rocket Lab has not published integrated array $/W, W/kg, W/m2, or EOL degradation. |

Suggested `SOURCE_INDEX.md` update:

| Claim ID | Claim text | Source status | Role | Links or internal references | Uncertainty notes |
|---|---|---|---|---|---|
| `THR-013` | A 2036 solar cost-down sensitivity of `$20k/kW` is plausible for high-volume Rocket Lab silicon orbital infrastructure, but not certified. | `scenario` | Model sensitivity support | [space_solar_costdown_2030_2036.md](space_solar_costdown_2030_2036.md); Rocket Lab silicon-array announcement; Rocket Lab Solar Solutions; Starpath market signal | Do not quote as Rocket Lab cost. Keep `$40k/kW` default until integrated cost/performance is sourced. |
