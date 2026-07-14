# Solar And Radiator Cost Refresh, July 2026

**Status:** draft research
**Date:** 2026-07-14
**Topic owner:** Research Agent Cost-Refresh
**Scope:** non-code, web-sourced cost research for the RKLB orbital data-center research wiki. Extends `space_solar_costdown_2030_2036.md` and `radiator_costdown_2030_2036.md`; does not replace them.
**Source-status summary:** the terrestrial silicon module floor, the current advertised space-silicon panel prices, the SpaceX AI-1 reference design, and the terrestrial cost analogies used in the radiator BOM are `certified` or `sourced_estimate` from the linked public materials. The 2036 `$/kW` bands, the radiator bill-of-materials sketch, and the translations from those anchors to a delivered Rocket Lab integrated node are `derived_estimate` or `scenario`. No public source certifies a Rocket Lab integrated array or radiator `$/W`, `$/kW`, `$/m^2`, `W/kg`, or delivered five-year power. The dials remain estimate-class, not vendor-quoted.

---

## Central Question

On 2026-07-14 the model moved its solar and radiator cost defaults to `$20,000/kW` each (`$0.02M/kW`), down from the prior `$40,000/kW` cautious defaults, which were uncited cycle-1 estimates. The move was paired with an AI-1-class light radiator at `1.65 kg/kW` deployed double-sided and run hot (the mass dial), and it assumes a five-year LEO service life plus in-house, vertically integrated, assembly-line production. The investor believes `20/20` is conservative at that scale.

This memo asks one thing, on fresh 2025-2026 web evidence: is investor-set `$20k/kW` solar and `$20k/kW` radiator **conservative, central, or aggressive**? It treats cost on its own feet. It does not re-derive the mass dial.

---

## What Changed Since The May 2026 Corpus

The prior two cost-down memos (both dated 2026-05-27) concluded that `$40k/kW` should stay the public default for both dials and that `$20k/kW` was a plausible-but-uncertified 2036 sensitivity, better supported for solar than radiator. Three things have changed since:

1. The defaults were moved to `20/20` by investor decision (`scenario`), so the question is no longer "is `$20k` a plausible sensitivity" but "is `$20k` a defensible default."
2. SpaceX revealed the **AI-1 orbital data-center satellite** on 2026-06-10 (`certified` that the reveal happened; specs `sourced_estimate` from press coverage). AI-1 is the exact architecture the RKLB node semi-copies, and it converts the radiator question from "does anyone build a large productized deployable pumped-loop radiator" into "here is one, in-house, at datacenter-satellite scale."
3. The radiator mass dial dropped from `12 kg/kW` (May corpus) to `1.65 kg/kW` (AI-1 class). That is the mass dial and is out of scope here, but it sets the physical hardware the cost BOM must price.

The May corpus flagged the radiator as the single least-sourced dial in the model, and as the dial "most likely wrong LOW" because Rocket Lab had no in-house radiator capability ([cost_validation_research_05_21.md](../../.agent/other/cost_validation_research_05_21.md) Section 1.2). Both of those cautions still matter and are carried forward below.

---

## The Decomposition Discipline (Load-Bearing)

`gpu_temperature_cooling_limits.md` implication 4 is explicit: a radiator cost-down must say whether `$20k/kW` "comes from production learning, area reduction, internal build margin, simpler co-mounted architecture, or all of the above," and the area/temperature win is already booked in the mass dial. The same logic applies to solar.

This memo therefore holds cost to three legitimate cost-down mechanisms, and excludes one:

- **Legitimate:** production learning at fleet volume; internalized supplier margin (Rocket Lab is the only fully vertically integrated space-power supplier, `certified` from Rocket Lab materials); productized repetition of one design instead of bespoke one-offs.
- **Excluded:** the "it is small and light because we run it hot double-sided, therefore it is cheap" argument. That area and mass win is already priced in the `1.65 kg/kW` mass dial. Letting it also lower the cost dial would double-count it.

The radiator BOM below is priced on the physical hardware the booked design specifies, and is then **re-checked with the area win stripped out** so the cost verdict does not secretly ride on the temperature/area lever.

---

## Solar

### Fresh 2025-2026 Evidence

**Terrestrial silicon module floor (the physical floor beneath any space array).** US utility-scale module prices stabilized near `$0.28/W` median in Q1 2026, with imports near `$0.265/W` and US-cell modules near `$0.46/W` ([pv magazine USA, Q1 2026](https://pv-magazine-usa.com/2026/04/03/u-s-solar-module-prices-face-upward-pressure-as-trade-risks-and-feoc-rules-dominate-q1-2026/); [now.solar, 2026](https://now.solar/2026/04/08/u-s-solar-module-prices-2026-stabilization-at-0-28-w-under-new-feoc-rules-news-and-statistics-indexbox-io/)) (`sourced_estimate`). Factory-gate FOB module cost runs `$0.10-0.15/W`, with polysilicon at `$8-12/kg` ([SurgePV supply-chain, 2026](https://www.surgepv.com/blog/solar-supply-chain-trends-2026); [NREL solar manufacturing cost](https://www.nrel.gov/solar/market-research-analysis/solar-manufacturing-cost)) (`sourced_estimate`). Net physical silicon-module floor: roughly `$0.10-0.30/W` (`derived_estimate`). This is the terrestrial process the space-silicon thesis is trying to inherit.

**Advertised space-silicon panel prices (2026, live market).** Starpath sells the Starlight line today: flight model (Classic) at `~$11.20/W`, ultra-thin Air at `$15/W`, engineering model at `$9.81/W`, at `73 g/m^2`, with a money-back guarantee, and says it is "locked in to deliver the first models to customers this year" with a `50 MW` production facility breaking ground in 2026 ([Payload exclusive, 2026](https://payloadspace.com/exclusive-starpath-unveils-new-ultra-thin-space-solar-panels/); [Starpath Starlight page](https://www.starpath.space/starlight); [TechCrunch, 2025-09-25](https://techcrunch.com/2025/09/25/starpath-bets-on-mass-produced-space-rated-solar/)) (`sourced_estimate`; scaling unproven, panel-level not wing-level). Starpath frames these as roughly `10x` cheaper than a stated conventional space-solar band of `$75-250/W` (`sourced_estimate`, vendor comparator).

**Second in-house space-silicon supplier corroborates the direction.** Solestial produces silicon heterojunction space cells reaching `20%` efficiency in production in 2026, claims manufacturing "costs 90% lower than traditional III-V multijunction," is scaling to `60 modules/month` in Q2 2026, and is delivering primary power for EnduroSat's FRAME satellite in H1 2026 ([Solestial](https://solestial.com/); [Solestial-EnduroSat deal](https://solestial.com/solestial-endurosat-deal/); [SatNow, 2026](https://www.satnow.com/news/details/3616-solestial-delivers-silicon-based-solar-solutions-for-the-future-of-space-energy)) (`sourced_estimate`). If legacy III-V space arrays sit at `$150-800/W` (May corpus), "90% lower" lands near `$15-80/W` at the cell/module level (`derived_estimate`).

**Rocket Lab.** The Feb 2026 silicon-array announcement (for gigawatt-scale space-based data centers, "low cost per watt at industrial scale") stands, backed by a reported `$23.9M` CHIPS award to expand semiconductor production in Albuquerque ([Rocket Lab announcement](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/); [Rocket Lab investor relations](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-introduces-advanced-silicon-solar-arrays-power-space)) (`certified` that the claims and award were made; no `$/W` disclosed).

**AI-1 existence proof.** SpaceX's AI-1 carries `150 kW` of solar at `250 W/m^2`, built in-house at Bastrop, Texas ([Data Center Dynamics, 2026-06-10](https://www.datacenterdynamics.com/en/news/spacex-details-ai1-satellite-data-center-claims-150kw-peak-compute/); [Tom's Hardware](https://www.tomshardware.com/tech-industry/spacex-details-its-ai1-compute-satellite)) (`sourced_estimate`). A datacenter-satellite builder makes its own arrays at this scale.

**In-house whole-satellite cost benchmark.** Starlink is the closest analog to "silicon-ish arrays built in-house at fleet volume": V2 mini at `~$800k` for `730 kg` (`~$1,100/kg`), and a projected V3 at `~$1.2M` for `1,500 kg` (`~$800/kg`), per Quilty Space, achieved through vertical integration and high volume ([New Space Economy, 2026-04-13](https://newspaceeconomy.ca/2026/04/13/the-satellite-manufacturing-market-after-starlink-how-mass-production-changed-the-economics-of-building-spacecraft/)) (`sourced_estimate`). This is a blended whole-satellite figure, not an array price, but it bounds what in-house volume production of space hardware costs.

### The Translation From Panel Price To The Dial

The dial multiplies **node** power, but the array must deliver about `1.34x` node power after power-chain losses and degradation margin ([cost_validation_research_05_21.md](../../.agent/other/cost_validation_research_05_21.md) Section 1.2) (`derived_estimate`). So the dial expressed per array watt is lower than the dial per node watt:

```text
$20,000/kW of node power  =  $20/W of node power
$20/W node ÷ 1.34 W array per W node  ≈  $14.9/W of actual array
```

That is the crux. The `$20k/kW` solar default implies an **array price of about `$15/W`**, which equals Starpath's advertised Air price and sits above Starpath's advertised flight model (`$11.20/W`), in the middle of the current advertised space-silicon market, before any 2036 learning and before Rocket Lab's in-house margin is internalized (`derived_estimate`).

Two honest counterweights keep this from being a slam dunk:

- Advertised **panel** price is not a delivered **integrated wing** price at fleet scale. The wing adds deployment structure, PMAD interface, EOL oversizing, and qualification at scale, and Starpath's large-scale capacity is still being built ([TechCrunch](https://techcrunch.com/2025/09/25/starpath-bets-on-mass-produced-space-rated-solar/)). The wing costs more than the panel.
- The array-level `$15/W` is still `~50-100x` the bare terrestrial silicon floor (`$0.15-0.30/W`). That entire gap is space integration, radiation tolerance, and qualification, which is exactly the part that a five-year LEO life and in-house production are assumed to compress. If those compressions underdeliver, solar drifts up.

On the supporting side: a five-year LEO life is shorter than the `15-year` high-reliability need NASA cites for long-life missions, which plausibly relaxes EOL oversizing, cover-glass burden, and qualification conservatism (`scenario`, per `space_solar_costdown_2030_2036.md`). And vertical integration means Rocket Lab's internal economic cost is below any external purchase-price analog (`certified` that Rocket Lab is fully vertically integrated; `derived_estimate` that this lowers internal cost).

### 2036 Solar Band (`$/kW` of node power)

| Case | `$/kW` node | Approx `$/W` array | Status | Rationale |
|---|---:|---:|---|---|
| Floor | `$8-12k/kW` | `~$6-9/W` | `scenario` | In-house silicon at high volume near advertised panel floor, five-year life, learning fully realized. |
| Central | `$15-25k/kW` | `~$11-19/W` | `sourced_estimate` | Brackets current advertised space-silicon panel prices (`$11-15/W`) plus integration. `$20k` sits at mid. |
| Conservative (old default) | `$30-40k/kW` | `~$22-30/W` | `scenario` | If integration, qualification, EOL margin, or slow in-house scale dominate. |
| Stress | `$50k+/kW` | `~$37+/W` | `scenario` | Silicon area penalty, low yield, or first-of-kind wing premium. |

### Where `$20k/kW` Sits For Solar

`$20k/kW` lands in the middle of the Central band. Its implied `~$15/W` array price is already bracketed by today's advertised space-silicon market, before a decade of learning and before in-house margin capture. Verdict for solar: **central, leaning conservative**, and better supported than radiator.

---

## Radiator

### The Cost Evidence Is Still Absent (Confirmed)

The May corpus said radiator `$/kW` and `$/m^2` cost data does not exist publicly. A fresh 2026 hunt across NASA SBIR, ESA procurement, vendor pages, and AI-1 commentary confirms it: there is still no public delivered `$/kW` or `$/m^2` for a hundreds-of-kW deployable pumped-loop radiator. ESA's lightweight-deployable-radiator tender still describes such radiators as "typically heavy, complex, and often expensive" without quantifying ([ESA ARTES tender](https://connectivity.esa.int/archives/open_tender/lightweight-deployable-radiators-artes-4d062-0)) (`certified` qualitative, no number). NASA SBIR thermal awards cap at `$0.75M` Phase II, which is R&D funding, not a product price ([NASA SBIR spacecraft thermal management](https://sbir.gsfc.nasa.gov/content/spacecraft-thermal-management-1)) (`certified`). The stated evidence gate from the corpus, a vendor quote or a bottom-up BOM, is unmet on the quote side, so this memo builds the BOM.

What did change: **AI-1 is a working reference design.** It carries up to `110 m^2` of deployable liquid radiators at about `1,400 W/m^2` radiating both sides knife-edge to the sun, with redundant pumping loops and integrated micrometeoroid shielding, for a `150 kW` peak ([Data Center Dynamics](https://www.datacenterdynamics.com/en/news/spacex-details-ai1-satellite-data-center-claims-150kw-peak-compute/); [Tom's Hardware](https://www.tomshardware.com/tech-industry/spacex-details-its-ai1-compute-satellite)) (`sourced_estimate`). That is `110 m^2 / 150 kW = 0.73 m^2/kW`, exactly inside the task's `0.7-0.9 m^2/kW` hot design point. The architecture is real and buildable in-house at datacenter-satellite scale.

### Bottom-Up BOM Sketch: 750 kW-Class Node

Design point (from the booked mass dial and the AI-1 reference): a `750 kW`-class node, `~0.73 m^2/kW`, so `~550 m^2` of physical panel radiating double-sided; `1.65 kg/kW`, so `~1,238 kg`, or `~2.25 kg/m^2`. That areal density is consistent with NASA/TFAWS's `2-3 kg/m^2` high-temperature radiator target ([NASA TFAWS 2024](https://ntrs.nasa.gov/api/citations/20240009793/downloads/TFAWS%202024%20Paper.pdf?attachment=true)) and with the "carefully designed solid aluminum radiator near `5 kg/m^2`" and "ISS exposed panels near `2.75 kg/m^2`" references ([ToughSF radiators](http://toughsf.blogspot.com/2017/07/all-radiators.html)) (all `sourced_estimate` for the reference points).

Each cost line is priced on the physical hardware, at productized volume and in-house, with a status tag. Terrestrial and aerospace analogies are used only to price the hardware, not to import the area win.

| BOM line | Basis / analogy | Per-node cost | Status |
|---|---|---:|---|
| Panel: Al honeycomb + embedded OHP/heat pipes + high-emissivity coating + integral MMOD | Raw aerospace honeycomb `$50-200/m^2` ([honeycomb price](https://www.dingchengzun.com/application/aluminium-honeycomb-panel-price); [ACP Composites](https://acpcomposites.com/shop/sandwich-panels/aluminum-core-panels/aluminum-sandwich-panel)); embedded-pipe + coating + qual raises it to `~$500-1,500/m^2` productized; `550 m^2` | `$0.3-0.8M` | `derived_estimate` |
| Pumped loop: redundant pumps, accumulators, manifolds, CDU-equivalent | Terrestrial CDU `$24-350/kW` ([LiquidStack](https://liquidstack.com/blog/how-to-choose-the-right-coolant-distribution-unit-cdu-for-your-data-center)), multiplied for space qualification and redundancy | `$0.5-2.0M` | `scenario` |
| Working fluid + headers + plumbing | Modest fluid inventory + distribution | `$0.1-0.3M` | `scenario` |
| Deployment mechanism: booms, hinges, actuators for `~550 m^2` | Large deployable structure, scaled from ROSA/ELSA-class heritage | `$0.5-1.5M` | `scenario` |
| MMOD / whipple beyond integral shielding | Added shielding for a five-year unserviceable loop | `$0.2-0.5M` | `scenario` |
| Integration, test, qualification (amortized over the production run) | Non-recurring spread across a fleet, not a one-off | `$0.5-1.5M` | `scenario` |
| **Total** | | **`$2.1-6.6M`** | `derived_estimate` |

Central BOM: about `$4.0M/node`, which is `$4.0M / 750 kW = ~$5,400/kW` (`derived_estimate`). Even the high end is `$6.6M / 750 kW = ~$8,800/kW`. Both are well under the `$20k/kW` dial (`$20k/kW x 750 kW = $15.0M/node`).

### Decomposition Check: Strip The Area Win

The BOM above uses the small hot-loop area (`550 m^2`), which is the mass dial's booked win. To keep the cost verdict honest, re-price with the area win removed: a colder or single-face radiator needs roughly `2-4x` the area. At `4x` area (`2,200 m^2`), the panel, deployment, and MMOD lines scale up with area while the pump, fluid, and integration lines scale with kW:

```text
panel ~$2.2M + deploy ~$2.5M + MMOD ~$0.8M + loop ~$1.0M + fluid ~$0.3M + integ ~$1.2M
≈ $8.0M/node  =  ~$10,700/kW
```

So even with the temperature/area win fully stripped out, a productized in-house BOM lands near `$8-16k/kW` (`derived_estimate`), still below `$20k/kW`. The `$20k/kW` default does not depend on the hot-loop area lever. That is the point the decomposition discipline requires, and it holds.

### Cross-Checks

- **Space-thermal `$/kg` bound.** `$20k/kW ÷ 1.65 kg/kW = ~$12,100/kg` of radiator hardware. That is at the top of, and slightly above, the `$1,000-10,000/kg` band for space thermal hardware that the May audit used ([cost_validation_research_05_21.md](../../.agent/other/cost_validation_research_05_21.md) Section 1.2) (`derived_estimate`). The dial is generous, not thin, on a mass-cost basis. Radiator hardware (panels, pipes, pumps, fluid) should be cheaper per kg than a blended whole satellite, and Starlink's in-house whole-satellite figure is only `~$800-1,100/kg`. Note: this `$/kg` view imports the mass win, so it is used only as an upper sanity bound, not as the primary argument.
- **Legacy one-off ceiling.** An independent AI-1 analyst puts ISS radiators "on the order of `$500M`" ([Wallington, Medium, 2026](https://medium.com/@graham.wallington/why-spacexs-ai1-orbital-data-centre-doesn-t-add-up-a49d26eb0a48)) (`scenario`, single secondary source). Spread over ISS's `~1,680 m^2` and `~70 kW` of rejection, that is roughly `$300k/m^2` or `~$7M/kW`, a `~350x` multiple over the `$20k/kW` target. This is the cost-plus government one-off regime the entire thesis must escape, not a forecast. It shows how far a productized build has to fall, and that the fall is what "production learning plus internalized margin plus repetition" is claimed to deliver.
- **Independent AI-1 mass tension (flag, not a cost input).** The same analyst pegs AI-1's radiator assembly at `~660 kg` and its heat-pump system at `~780 kg`, a `~1,440 kg` thermal system for `150 kW`, or `~9.6 kg/kW` with the pump ([Wallington, Medium](https://medium.com/@graham.wallington/why-spacexs-ai1-orbital-data-centre-doesn-t-add-up-a49d26eb0a48)) (`scenario`). That is far above the booked `1.65 kg/kW`. Mass is out of scope here, but if the real productized radiator is heavier or more pump-heavy than the aggressive mass design assumes, the panel-area and pump lines of the BOM rise. Even so, the BOM stays at or under `$20k/kW` in the sketch above.

### 2036 Radiator Band (`$/kW` of node heat)

| Case | `$/kW` | Status | Rationale |
|---|---:|---|---|
| Productized BOM, booked hot-loop area | `$3-9k/kW` | `derived_estimate` | Volume, in-house, AI-1-class architecture; area from the booked double-sided hot design. |
| Productized BOM, area win stripped out | `$8-16k/kW` | `derived_estimate` | Cost holds even under a colder or single-face area penalty. Satisfies the decomposition discipline. |
| Investor default | `$20k/kW` | `scenario` | Sits above the disciplined BOM with comfortable margin. Not a vendor quote. |
| Legacy one-off (ISS-class) | `~$100k/kW` and up | `scenario` | Cost-plus government one-off. The regime the thesis escapes, not a forecast. |

### Where `$20k/kW` Sits For Radiator

On a bottom-up productized BOM, `$20k/kW` is **conservative**: the disciplined sketch lands at `$3-9k/kW` on the booked design and `$8-16k/kW` even with the area win removed, comfortably under `$20k`. But the evidence class is a BOM sketch, not a vendor quote, so confidence is lower than solar. And the residual risk is not the cost level, it is **who builds it**: no evidence surfaced of a Rocket Lab in-house large deployable pumped-loop radiator or an acquisition to get one (the June 2026 Iridium acquisition is a communications play, not thermal). The AI-1 reveal proves the architecture is productizable in-house industry-wide, but Rocket Lab's specific radiator capability remains unconfirmed, and an early build-or-buy premium could apply.

---

## Verdict On `20/20`

| Dial | Verdict | Confidence | One-line reason |
|---|---|---|---|
| Solar `$20k/kW` | **Central, leaning conservative** | Higher | Implied `~$15/W` array price is already bracketed by today's advertised space-silicon market, before 2036 learning or in-house margin capture. |
| Radiator `$20k/kW` | **Conservative** on the BOM, but lower confidence | Lower | Disciplined bottom-up BOM lands `$3-16k/kW`; the dial has headroom, but rests on a sketch not a quote, and on unconfirmed RKLB radiator capability. |
| The pair `20/20` | **Defensible, on the conservative side of the fresh 2026 evidence** | Mixed | Not aggressive. The honest caveat is evidence class (estimate and BOM, not certified quote), not the price level. |

The blunt answer to the investor: **`20/20` is not aggressive.** On fresh 2025-2026 evidence it is central-to-conservative. Solar is well anchored by a live market that already prices space silicon at the implied array level. Radiator has more headroom on the numbers but weaker evidence, because the cost-down there rides on a productization Rocket Lab has not yet demonstrated. The right posture is to hold `20/20` as a defensible default while labeling it estimate-class, and to keep hunting a radiator vendor quote or a firmer internal BOM as the evidence that would upgrade the radiator dial from `derived_estimate` to `sourced_estimate`.

---

## What Argues Against `20/20`

Facts over comfort. These are the honest counts against the default:

1. **No vendor quote, no published integrated `$/W` for either dial.** Both remain estimate-class. Solar at least has advertised panel prices; radiator has only a BOM sketch.
2. **Panel price is not wing price.** Starpath's `$11-15/W` is a panel-level advertised number with unproven large-scale capacity (`50 MW` facility only breaking ground in 2026). A delivered integrated wing at fleet scale adds deployment, PMAD, EOL margin, and qualification, and costs more.
3. **Rocket Lab radiator capability gap.** Rocket Lab builds solar and bus in-house, but no evidence of a productized large deployable pumped-loop radiator or an acquisition to obtain one. The radiator BOM assumes an in-house productization not yet demonstrated at Rocket Lab.
4. **Independent AI-1 mass check runs heavier.** An outside analyst estimates AI-1's thermal system near `9.6 kg/kW` including the heat pump, far above the booked `1.65 kg/kW`. If the productized radiator is heavier and more pump-heavy than assumed, the BOM's panel and pump lines rise.
5. **Same number, different confidence.** Both dials moved to the identical `$20k`. The symmetry is convenient, but solar is market-anchored while radiator is BOM-only. They should not be treated as equally certain.
6. **The terrestrial-to-space gap is the least-certain part.** The array-level `~$15/W` is `~50-100x` the bare silicon floor. That gap is all space integration and qualification, and it is precisely what five-year life plus in-house scale is assumed to compress. If those assumptions underdeliver, solar drifts toward `$30-40k/kW`.

---

## Public-Safe Claims

- The terrestrial silicon module floor is about `$0.10-0.30/W` in 2026 ([pv magazine USA](https://pv-magazine-usa.com/2026/04/03/u-s-solar-module-prices-face-upward-pressure-as-trade-risks-and-feoc-rules-dominate-q1-2026/); [SurgePV](https://www.surgepv.com/blog/solar-supply-chain-trends-2026)).
- Starpath advertises space-rated silicon panels at `$11.20/W` (flight) to `$15/W` (Air) in 2026, and is building production capacity ([Payload](https://payloadspace.com/exclusive-starpath-unveils-new-ultra-thin-space-solar-panels/)).
- Solestial claims space-silicon manufacturing costs `90%` below III-V multijunction and is delivering modules in 2026 ([Solestial](https://solestial.com/)).
- SpaceX's AI-1 uses `~110 m^2` of deployable liquid radiators (`~1,400 W/m^2` double-sided) and `150 kW` of in-house solar, proving the large productized architecture exists at datacenter-satellite scale ([Data Center Dynamics](https://www.datacenterdynamics.com/en/news/spacex-details-ai1-satellite-data-center-claims-150kw-peak-compute/)).
- The model's `$20k/kW` solar default implies an array price of about `$15/W`, which is inside the current advertised space-silicon market.
- A bottom-up productized radiator BOM at `750 kW`-class lands well under `$20k/kW`, but this is a sketch, not a vendor quote.
- `$20k/kW` solar and radiator are defensible, estimate-class defaults on 2026 evidence, and are not aggressive.

## Unsafe Claims

- "Rocket Lab solar or radiator costs `$20k/kW`." (No published Rocket Lab cost exists.)
- "The `$20k/kW` radiator default is validated." (It rests on a BOM sketch, not a quote.)
- "Starpath or Solestial pricing proves Rocket Lab can deliver an integrated node solar wing at that price." (Panel price is not wing price at fleet scale.)
- "Rocket Lab builds its own large deployable radiators." (No evidence; capability unconfirmed.)
- "The radiator is cheap because it is light." (That imports the mass/area win, which is already booked in the mass dial.)
- "AI-1's published specs certify Rocket Lab's node cost." (AI-1 is a SpaceX reference design, not a Rocket Lab cost source.)

---

## Proposed SOURCE_INDEX Row Updates

These extend, they do not overwrite, the existing rows `THR-013`, `THR-014`, `THR-016`, `RLDC-SOLAR-RADIATOR-COST`, and `RLDC-SOLAR-RADIATOR-COSTDOWN-SENSITIVITY`. Suggested new or amended rows:

| Claim ID | Claim text | Source status | Role | Links or internal references | Uncertainty notes |
|---|---|---|---|---|---|
| `THR-013` (amend) | A 2036 solar cost of `$20k/kW` (implied array `~$15/W`) is central-to-conservative on 2026 evidence: it sits inside the advertised space-silicon market (Starpath `$11-15/W`, Solestial `90%` below III-V) before 2036 learning or in-house margin capture. | `sourced_estimate` | Model default support | [solar_radiator_cost_refresh_2026_07.md](node_design/solar_radiator_cost_refresh_2026_07.md); [Payload Starpath](https://payloadspace.com/exclusive-starpath-unveils-new-ultra-thin-space-solar-panels/); [Solestial](https://solestial.com/); [pv magazine USA floor](https://pv-magazine-usa.com/2026/04/03/u-s-solar-module-prices-face-upward-pressure-as-trade-risks-and-feoc-rules-dominate-q1-2026/) | Panel price is not delivered wing price at fleet scale; still no Rocket Lab `$/W`. |
| `THR-016` (amend) | A 2036 radiator cost of `$20k/kW` is conservative on a bottom-up productized BOM (`$3-9k/kW` on the booked hot design, `$8-16k/kW` with the area win stripped out), but the evidence is a BOM sketch, not a vendor quote, and Rocket Lab radiator capability is unconfirmed. | `derived_estimate` | Model default support | [solar_radiator_cost_refresh_2026_07.md](node_design/solar_radiator_cost_refresh_2026_07.md); [AI-1 reference, DCD](https://www.datacenterdynamics.com/en/news/spacex-details-ai1-satellite-data-center-claims-150kw-peak-compute/); [ESA ARTES tender](https://connectivity.esa.int/archives/open_tender/lightweight-deployable-radiators-artes-4d062-0); [honeycomb price](https://www.dingchengzun.com/application/aluminium-honeycomb-panel-price) | Cost-down must stand on production learning, internalized margin, and repetition, not the area win (already booked in the mass dial). Vendor quote is the missing evidence. |
| `THR-021` (new) | The SpaceX AI-1 reveal (2026-06-10) is an existence proof of the semi-copied architecture: `~110 m^2` deployable liquid radiators at `~1,400 W/m^2` double-sided with redundant pumps and MMOD shielding (`0.73 m^2/kW`), plus `150 kW` in-house solar at `250 W/m^2`. | `sourced_estimate` | Architecture and dial support | [solar_radiator_cost_refresh_2026_07.md](node_design/solar_radiator_cost_refresh_2026_07.md); [DCD AI-1](https://www.datacenterdynamics.com/en/news/spacex-details-ai1-satellite-data-center-claims-150kw-peak-compute/); [Tom's Hardware AI-1](https://www.tomshardware.com/tech-industry/spacex-details-its-ai1-compute-satellite) | Specs are press-sourced from an unflown design; it is a SpaceX reference, not a Rocket Lab cost. |
| `RLDC-SOLAR-RADIATOR-COST` (amend) | The current model uses solar and radiator cost dials of `$0.02M/kW` each (moved from `$0.04M/kW` on 2026-07-14). | `scenario` | Model input; open research question | Add [node_design/solar_radiator_cost_refresh_2026_07.md](node_design/solar_radiator_cost_refresh_2026_07.md) to the existing reference list | `$20k/kW` is central-to-conservative for solar and conservative-but-weakly-sourced for radiator on 2026 evidence. Not a certified Rocket Lab cost. |

---

## Unresolved Questions

- What is Rocket Lab's integrated silicon-array delivered cost per watt at wing level, at node scale, not panel level?
- Does Rocket Lab build, partner, or acquire a large deployable pumped-loop radiator, and what supplier margin is internalized?
- What is a real vendor quote or firmed internal BOM for a `500-750 kW`-class deployable double-sided pumped-loop radiator?
- How much does the space-integration gap (`~50-100x` the terrestrial silicon floor) actually compress under a five-year LEO life and in-house volume?
- If AI-1's real thermal-system mass runs near `9.6 kg/kW`, does the productized RKLB radiator mass dial of `1.65 kg/kW` hold, and if not, how much does the BOM cost rise?

---

## Sources

Local project sources:

- [space_solar_costdown_2030_2036.md](space_solar_costdown_2030_2036.md)
- [radiator_costdown_2030_2036.md](radiator_costdown_2030_2036.md)
- [gpu_temperature_cooling_limits.md](gpu_temperature_cooling_limits.md) implication 4 (decomposition discipline)
- [cost_validation_research_05_21.md](../../.agent/other/cost_validation_research_05_21.md) Section 1.2 (prior dial audit)
- [SOURCE_INDEX.md](../SOURCE_INDEX.md) rows `THR-013`, `THR-014`, `THR-016`, `RLDC-SOLAR-RADIATOR-COST`

External sources (solar):

- [pv magazine USA, US module prices Q1 2026](https://pv-magazine-usa.com/2026/04/03/u-s-solar-module-prices-face-upward-pressure-as-trade-risks-and-feoc-rules-dominate-q1-2026/) and [now.solar `$0.28/W`](https://now.solar/2026/04/08/u-s-solar-module-prices-2026-stabilization-at-0-28-w-under-new-feoc-rules-news-and-statistics-indexbox-io/), terrestrial silicon module floor.
- [SurgePV solar supply chain 2026](https://www.surgepv.com/blog/solar-supply-chain-trends-2026) and [NREL solar manufacturing cost](https://www.nrel.gov/solar/market-research-analysis/solar-manufacturing-cost), FOB module and polysilicon cost.
- [Payload, Starpath Starlight exclusive](https://payloadspace.com/exclusive-starpath-unveils-new-ultra-thin-space-solar-panels/), [Starpath Starlight page](https://www.starpath.space/starlight), [TechCrunch, Starpath](https://techcrunch.com/2025/09/25/starpath-bets-on-mass-produced-space-rated-solar/), advertised space-silicon prices and production.
- [Solestial](https://solestial.com/), [Solestial-EnduroSat deal](https://solestial.com/solestial-endurosat-deal/), [SatNow Solestial](https://www.satnow.com/news/details/3616-solestial-delivers-silicon-based-solar-solutions-for-the-future-of-space-energy), second in-house space-silicon supplier and the `90%`-below-III-V claim.
- [Rocket Lab silicon-array announcement](https://rocketlabcorp.com/updates/rocket-lab-introduces-advanced-silicon-solar-arrays-to-power-space-based-data-centers/) and [Rocket Lab investor relations](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-introduces-advanced-silicon-solar-arrays-power-space), Rocket Lab program and CHIPS award.
- [New Space Economy, satellite manufacturing after Starlink](https://newspaceeconomy.ca/2026/04/13/the-satellite-manufacturing-market-after-starlink-how-mass-production-changed-the-economics-of-building-spacecraft/), in-house whole-satellite cost benchmark (Quilty V2 mini / V3).
- [arXiv 2604.07760, integrated solar/compute/radiator panels](https://arxiv.org/abs/2604.07760), specific power `~500 W/kg` context (no cost data).

External sources (radiator):

- [Data Center Dynamics, AI-1](https://www.datacenterdynamics.com/en/news/spacex-details-ai1-satellite-data-center-claims-150kw-peak-compute/) and [Tom's Hardware, AI-1](https://www.tomshardware.com/tech-industry/spacex-details-its-ai1-compute-satellite), AI-1 radiator and solar reference specs.
- [Wallington, "Why SpaceX's AI-1 Doesn't Add Up," Medium](https://medium.com/@graham.wallington/why-spacexs-ai1-orbital-data-centre-doesn-t-add-up-a49d26eb0a48), independent AI-1 mass breakdown and the ISS `$500M` radiator aside (single secondary source).
- [ESA ARTES lightweight deployable radiators tender](https://connectivity.esa.int/archives/open_tender/lightweight-deployable-radiators-artes-4d062-0), procurement signal, "heavy, complex, often expensive."
- [NASA SBIR spacecraft thermal management](https://sbir.gsfc.nasa.gov/content/spacecraft-thermal-management-1), SBIR funding structure (not product price).
- [NASA TFAWS 2024 additively manufactured radiator paper](https://ntrs.nasa.gov/api/citations/20240009793/downloads/TFAWS%202024%20Paper.pdf?attachment=true) and [ToughSF radiators](http://toughsf.blogspot.com/2017/07/all-radiators.html), areal-density references.
- [Aluminum honeycomb panel price](https://www.dingchengzun.com/application/aluminium-honeycomb-panel-price) and [ACP Composites honeycomb panels](https://acpcomposites.com/shop/sandwich-panels/aluminum-core-panels/aluminum-sandwich-panel), panel material cost analogy.
- [ThermAvant OHP radiators](https://www.thermavant.com/thermavant-products/oscillating-heat-pipe-radiators) and [Advanced Cooling Technologies, next-gen radiators](https://www.1-act.com/resources/blog/the-next-generation-of-spacecraft-radiators/), embedded-heat-pipe panel performance.
- [LiquidStack CDU guide](https://liquidstack.com/blog/how-to-choose-the-right-coolant-distribution-unit-cdu-for-your-data-center) and [Energy Solutions liquid-cooling cost](https://energy-solutions.co/articles/sub/data-center-cooling-liquid-immersion-vs-air), terrestrial pump/CDU cost analogy.
- [ARQUIMEA deployable radiators](https://www.arquimea.com/products/deployable-radiators-satellite-space/) and [Redwire ODC power/thermal white paper](https://rdw.com/wp-content/uploads/2026/05/RDW26-053-ODC-Power-Thermal-Study-White-Paper-R11-Digital.pdf), deployable-radiator maturity and ODC architecture context.

## Proposed Library / Tracker Entry Text

Suggested `LIBRARY.md` row:

| File | What it is | Key takeaway |
|---|---|---|
| [solar_radiator_cost_refresh_2026_07.md](node_design/solar_radiator_cost_refresh_2026_07.md) | July 2026 web-sourced cost refresh for the `$20k/kW` solar and radiator defaults. | `20/20` is central-to-conservative on 2026 evidence, not aggressive. Solar is market-anchored (`~$15/W` array implied, inside the Starpath/Solestial band). Radiator is conservative on a bottom-up BOM (`$3-16k/kW`) but weakly sourced and rests on unconfirmed Rocket Lab radiator capability. |

Suggested `RESEARCH_TRACKER.md` row:

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [solar_radiator_cost_refresh_2026_07.md](node_design/solar_radiator_cost_refresh_2026_07.md) | draft | Tests whether investor-set `$20k/kW` solar and radiator defaults are conservative, central, or aggressive on fresh 2026 evidence. | Solar `sourced_estimate` and central-to-conservative; radiator `derived_estimate` and conservative-but-BOM-only. Neither is a certified Rocket Lab cost; radiator vendor quote is the missing evidence. |
