# Communications Default Assumptions (The Iridium Model And The Product Case)

This is the human-readable ledger for the communications application's default
assumptions: the engineering case (the Iridium model) and the product case.
The machine-readable scenarios are `code/scenarios/iridium.yaml` and
`code/scenarios/product_case.yaml`. The promoted artifacts are
`communications/models/iridium/default.json` (schema `iridium-v7`), the
saturation curve it reads, `communications/models/iridium/saturation_curve.json`
(schema `saturation-v1`), and `communications/models/product_case/default.json`
(schema `product-case-v1`). The claim ledger is `research/SOURCE_INDEX.md`.

The project is not a DCF. It asks whether a Neutron-launched next-generation
fleet on Iridium's owned L-band could serve people and IoT devices at visible
cost under stated assumptions. The defaults are investor-set where the
investor set them, reviewable, and expected to improve.

The canonical outputs are the promoted JSON. The conclusion is static
editorial prose tied to them. If a default changes, update this ledger and the
promoted JSON, then review `communications/conclusion.md` before treating it
as current.

## Source-Status Taxonomy

| Source status | Meaning |
|---|---|
| `certified` | Directly supported by a primary or official source, or a standard's or a textbook's value, or an operator's published system fact, confirmed by two credible secondary sources that cite it. |
| `sourced_estimate` | Estimated from credible external sources, but not an official exact value. |
| `derived_estimate` | Computed from sourced or scenario inputs using a stated formula. |
| `projection` | A forward-looking market or technical projection from an external source. |
| `extrapolation` | A project extrapolation from known or sourced behavior. |
| `scenario` | A chosen modeling assumption for feasibility analysis. |
| `placeholder` | A known open slot that should not support settled public claims. |
| `stale` | Known old material retained only for historical context. |

Public documentation must not present `placeholder` or `stale` items as settled
evidence.

## The Engineering Case: Key Sourced And Derived Dials

Each class's usage and spectral efficiency, the curve's shell and its demand
grid are named constants in `code/src/communications/constants.py`, each with
its basis in the docstring. The scenario sets the held spectrum, the panel,
satellites per launch, the downlink share, the three class prices, the
cadence share and the two investor-flat cost dials (satellite build cost,
launch cost). The cost dials are scenario overrides: the shared-spine config
defaults they diverge from stay untouched, so the cellular family and the
equality tripwire still see the defaults.

| Dial | Default | Source status | Source |
|---|---|---|---|
| Exclusive spectrum | 8.0 MHz | `scenario` on a sourced basis | `COMM-611`: 1616 to 1626.5 MHz is a 10.5 MHz span, 7.775 MHz exclusive plus 0.95 MHz shared with Globalstar; 7.775 rounded up to 8.0, stated in code. The Big LEO split is confirmed at `COMM-656`. The curve is computed at 8 MHz: another width is refused at run until the saturation command computes a curve for it. |
| Coordinated spectrum | 10.5 MHz, a conclusions note | `sourced_estimate`, contingent | Same `COMM-611` span. Authorized today is 7.775 plus 0.95 shared; the full 10.5 depends on the live FCC petition over the Globalstar sliver. Not a setting the curve runs: its linear note is about 31 percent more people and class revenue (10.5 / 8 = 1.3125), the fleet and its cost unmoved. |
| Panel | 15.4 m^2 | `derived_estimate` | `COMM-711`: the Flatellite body Rocket Lab drew, at most 15.4 m^2, a chamfered near-square about 4.1 by 4.0 m, sized to Neutron's 4.79 m usable lower band; 14.0 to 15.4 m^2 with clearance. The investor's approved default (2026-10-03). |
| The curve's reference panel | 25 m^2 | `scenario` (the computation basis) | The curve is computed at a 25 m^2 reference panel and scaled linearly by the panel factor, 15.4 / 25 = 0.616, on people, useful beams, capacity and maximum use, never on the saturation numbers, the ocean factor or satellites per launch (ADR 005). Not a satellite that flies. |
| Satellites per launch | 16 | `derived_estimate` | `COMM-713`: 16 Flatellites a launch with the Neutron block upgrade assumed from the first launch (an assumed +15 to +30 percent lift, the envelope unchanged). `COMM-712`: 15 without it, the mass-bound count today. |
| Reuse calibration | 0.15 Gbps per MHz per unit SE, at the reference panel | `derived_estimate` (calibration) | `COMM-410`: a flat 20 to 24 m^2 array on about 25 MHz produces about 5 to 15 Gbps (central 8 to 10); 25 x 2.5 x 0.15 = 9.375 sits inside the central band. The implied 150 beams a satellite sit inside `COMM-411`'s 130 to 200x; at the 15.4 m^2 panel a satellite carries 92.4. |
| Phone-class spectral efficiency | 0.65 bps/Hz (band 0.5 to 0.8) | `sourced_estimate`, measured | `COMM-428/429`: Starlink direct-to-cell measured mean 0.79 and median 0.64 bps/Hz at about 0 dB median SINR (arXiv 2506.00283, fetched and verified verbatim). Central is the band midpoint. IoT's room reads it too. |
| Small-terminal spectral efficiency | 2.0 bps/Hz (band 1.5 to 2.5) | `derived_estimate` | Shannon chain on the phone-class anchor plus the investor's device spec (about 10 dBi patch on a self-orienting mount: a fixed tilt or switched elements, no user pointing; investor decision 2026-07-10, physics loop C-122/C-213: a bare flat face-up patch gets the full gain only at high elevations, so the mount is part of the spec): plus 10 dB gives 1.6 to 2.2 bps/Hz at 60 to 80 percent of Shannon. |
| Mounted-terminal spectral efficiency | 2.5 bps/Hz (band 2.0 to 3.0) | `sourced_estimate` | `COMM-650` and the capacity doc's modern-ACM band (about 2 to 3 bps/Hz to a gain terminal); `COMM-428` carries the AST claim to about 3. |
| Each class's usage | the investor's (2026-10-04) | `scenario`, investor-set | The small terminal 2 Mbps while active, 2.5 percent of users at the busy hour and 0.5 percent off-peak (5.4 GB a month at 4 busy hours and 30 days: "about five gigabytes a month", the investor 2026-10-12); the mounted terminal 5 Mbps, 10 and 2 percent (54 GB); the phone class 0.75 Mbps, 2.5 and 0.5 percent (about 2 GB). Named constants, not settings. The corpus's busy-hour concurrency, about 1 to 5 percent (`COMM-543`), is context. |
| Downlink share d | 0.67 | `scenario` | The time-division duplex band's downlink time share (ADR 008): Certus 700's 2 : 1 down-to-up rate split (`COMM-620`); 0.5 is the symmetric frame, 0.75 an estimated alternative. Each people figure and each class's downlink pool scale with d; IoT's uplink, payload and single-tone rooms with 1 - d. |
| Class prices | $10, $50 and $15 a month, held flat | `scenario`, investor-set | The small terminal $10 and the mounted terminal $50 (2026-10-07: "Yes, let's use the $10 and $50. Let's do that"; they were $15 and $100); the phone class's $15 is its floor (2026-10-03). One price list with the product case's terminals. |
| Satellite build cost | 1.0 million dollars | `scenario`, investor-flat | Investor simplification 2026-07-09, a deliberately flat cost model. Scenario override in `iridium.yaml`, deliberately diverging from the shared config default of 1.05 (untouched); in-band, just below that prior dial and the Starlink V3 hardware anchor of about 1.2 million dollars (`COMM-080`, the consolidated unit-cost trajectory row; a projection, hardware-cost analogy only). |
| Launch cost (flat) | 13.0 million dollars per launch | `scenario`, investor-flat | Investor simplification 2026-07-09: both cadence anchors of the shared log-linear curve set equal in `iridium.yaml`, so the launch cost is flat at every cadence (no stepped pricing as launches scale). In-band, just below the shared curve's grounded 13.5 high-cadence floor; the shared-spine default curve (25.0 to 13.5) is untouched. |
| Satellite lifetime | 5 years | `scenario` | The corpus Starlink operating-life lineage (`COMM-088`, the ~5-year depreciation and replacement treadmill). |
| Coverage floor | 340 satellites | `scenario` on a computed basis | The project coverage simulation's 95 percent column reads 341 at 450 km and a 25 degree mask, investor-rounded to 340; inside `COMM-216`'s 290 to 960 floor band. Honest bounds (2026-07-14 audit): a fuller integer-phasing search finds 320 passing the same stored geographic metric, while the saved 341 case is the robust one under equal-area weighting; the metric is geographic, not population-weighted, so 340 is a supported conservative scenario and the exact floor is an engineering decision. It gates every sale: nothing is sold in a year whose living fleet is below it, and IoT's capacity is null there. |
| Orbit (altitude, inclination) | about 450 km, 53 degrees | `derived_estimate` (Part 7 physics loop) | The coverage-of-people choice: 53 degrees covers the latitudes holding about 99.6 percent of population and needs about 10 percent fewer satellites than polar (341 vs 375); the four couplings (path loss, coverage economy, spectrum saturation, the sun-angle power floor) favor about 450 km, robustly on the link budget and latency. Supports the 340-satellite floor as a conservative scenario (not a solved optimum; see the coverage-floor row); the promoted artifact carries the orbit as a labeled scenario block with the bounds attached (since schema iridium-v4). |
| Saturation numbers | per class, from the curve | `derived_estimate` | The fleet at which a class's elasticity of capacity first falls under 0.10 on the curve: the small terminal 19,995 satellites; the mounted terminal not reached by 55,407 (the last fleet the curve's rows measure it at); the phone class 20,652 (its band points 10,223 to 21,613, the 48-beam point not reached). Each is a spectrum bound reported beside the launch cadence, never a build target or a cap (ADR 005); `COMM-413` to `COMM-416` own the mechanism (overlapping co-channel beams interfere rather than add). |
| Operations cost | 0.0 dollars per year | `scenario`, investor-instructed | A line to research and add later, stated in every model output rather than silently omitted. |
| Government | left out of revenue | `scenario`, investor-set | No government count, price or line (ADR 007, ADR 011; the investor, 2026-10-04). The conclusion names the EMSS contract (`COMM-619`). |
| Cost-plus revenue multiple | 1.5x | `scenario` | The High-Bandwidth Cellular Pure Play family's cost-recovery convention only (revenue equals annualized cost times the multiple, mirroring the data-center central band, `RLDC-REVENUE-MULTIPLE-1_5X`). The Iridium model publishes no cost-plus revenue. |

The published margins are each people class's `own_margin_pct` in
`years[].classes[]` and in `saturation.readings[].classes[]` (`iridium-v7`),
and the product case's `headline.years[].totals.margin_pct`
(`product-case-v1`): each a full-cost margin, revenue against the living
fleet's whole annualized build, launch and replacement cost.

## The Engineering Case's IoT: Room And Capacity

The engineering model carries no IoT count, price or revenue (ADR 011). For
every year and reading it publishes IoT's room and each IoT class's device
capacity alone at its reference usage: a capacity, not a forecast.

| Dial | Default | Source status | Source |
|---|---|---|---|
| The room's basis | the phone class's useful beams, in the uplink's share of the frame (1 - d) | `scenario` (the approved basis) | IoT devices are low gain, so their reuse follows the phone rule. Those are the beams lit over inhabited cells: IoT over oceans and empty land is not counted, a conservative basis. No people class's own upload is subtracted from the room. |
| Message size | 340 bytes | `certified` | `COMM-620`: Iridium's SBD IoT messages, about 340 bytes, the volume engine. |
| Minimal-packet IoT's reference usage | 48 messages a day | `scenario`, investor-set | The investor's usage table (2026-10-04): about 1.5 bits a second, the top of `COMM-659`'s 0.03 to 1.5 bits a second for a low-duty narrowband device. |
| Data IoT's reference usage | 4 bursts of 100 KB a day, beside the 48 messages | `scenario`, investor-set | The investor's usage (2026-10-04, an assumption). |
| MAC efficiency | 20 percent | `derived_estimate` | `COMM-659`: the share of a beam's uplink bits that carry payload; the payload view. |
| Random-access window | 57 to 1,650 devices; the capacity reads 57 | `sourced_estimate` | `COMM-654`: the devices one NB-IoT NTN random-access window serves, by mode, a per-opportunity contention figure, not a population cap. |
| Random-access windows a second | 1 | `scenario` | An assumption: no source gives a window rate. |
| Uplink tone | 3.75 kHz | `certified` | `COMM-714`: NB-IoT's narrowest uplink subcarrier, single-tone; the 8 MHz band holds about 2,133. |
| Message airtime | 4 to 7 s on one tone; the capacity reads 7 | `scenario` | `COMM-719`: the design reviewer's figure, 1.5 to 5 times the 1.4 to 2.7 s the corpus's NB-IoT NTN envelope gives before repetition and overhead. |

Each view is read at its conservative end, the least of the three is the
capacity, and each class is given the whole room, so the two capacities never
add. The anchors (`iridium-v7`): in FY2031, 1,965,864,139 minimal-packet IoT
devices (random access binds) or 170,588,558 data IoT devices (payload binds);
in FY2036, 11,497,881,052 or 997,732,709. IoT's customers, usage and revenue
are the product case's, whose usage and time basis differ, so a capacity is
never divided by the product case's devices.

## The Product Case: Dials

The product case reads the engineering artifact (its schema pinned, its
SHA-256 recorded) and never feeds it (ADR 012). Its settings are in
`code/scenarios/product_case.yaml`, and each value's full basis, the
investor's words quoted, is in its constant's docstring in
`code/src/product_case/constants.py` and in the artifact's inputs.

| Dial | Default | Source status | Source |
|---|---|---|---|
| Reported years | FY2031, FY2033, FY2035, FY2036 | `scenario` | `COMM-723`: the product-case design's years, the first year of service to the horizon's end. |
| Small terminal's price | $10 a month, held flat | `scenario`, investor-set | `COMM-722`: the investor, 2026-10-07; one price list with the engineering model. The lower end prices a choice may reach ($9 to $6) are context only. |
| Mounted terminal's price | $50 a month, held flat | `scenario`, investor-set | `COMM-722`: the investor, 2026-10-07. The lower end prices ($45, $40) are context only. |
| Minimal-packet IoT's price | $3 a month, held flat | `scenario`, investor-set | `COMM-722`: the investor, 2026-10-06 ("Let's go with the three and six for now"). |
| Data IoT's price | twice minimal-packet IoT's: $6 | `scenario`, investor-set | `COMM-722`, `COMM-726`: the investor's proportion (2026-10-04), never a setting. |
| Terminals' data a month | the small terminal 5.4, 6.7, 8.1 and 9 GB; the mounted terminal 54, 67, 81 and 90 GB | `scenario`, investor-set | `COMM-724`: FY2031's is the engineering usage; FY2035's the investor's bigger allotment (2026-10-05); FY2036's the investor's (2026-10-12: "go with 9 GB, 90 GB and 13 bursts"); FY2033's about half-way (a scenario value). |
| Minimal-packet IoT's usage path | 48, 72, 96 and 96 messages a day | `scenario` | `COMM-724`: the engineering usage's 48, doubling to 96 by FY2035 and held. Each choice multiplies it by a factor that rises on a straight line from x1 in FY2031 to its usage scale in FY2036, x1 to x16 (`COMM-723`): at the pick's x8, 48, 274, 634 and 768 messages a day. |
| Data IoT's usage | 8, 10, 12 and 13 bursts a day, beside 48 messages; outside the busy hours from FY2033 | `scenario`, investor-set | `COMM-724`: the investor's 8 (2026-10-05) and 13 (2026-10-12) and the bursts' timing (2026-10-05); 10 and 12 are scenario values. Each choice multiplies the bursts by a factor on the same line, from x1 in FY2031 to its usage scale in FY2036, x1 to x8 (`COMM-723`); the pick's is x1. |
| The demand anchors | 402,000 at $47; 16,100 at $259; 1,998,000 IoT devices at $7.78 | `certified` | `COMM-617`, `COMM-618`: Iridium's voice-and-data, broadband and commercial IoT customers and ARPU today. Minimal-packet IoT takes the IoT segment whole. |
| Data IoT's anchor | 999,000 at $15.56 | `scenario`, investor-set | `COMM-726`: half the IoT segment's count at double its ARPU, the investor's proportion (2026-10-04). |
| Busy hours, month, units | 4 busy hours a day; 30-day months; decimal GB and MB | `scenario`, investor-set (the 4 hours) | `COMM-724`: the investor, 2026-10-04, for the 4 hours; the rest are conventions. |
| The market's draws | 2,000 draws, seed 20261006 | `scenario` | `COMM-723`: the same markets every run; another seed or count moves the drawn markets, never the central one. |
| The network response gamma | 0.5 to 1.0 | `scenario` | `COMM-723`: at 0.5 four times the network doubles the customers; at 1.0 the investor's "eight times the network ... about eight times the revenue". No market research grounds the range. |
| The price response epsilon | 0.5 to 1.5 | `scenario` | `COMM-723`: centered on 1, so at the central market, for a given usage, an uncapped class's price change shows as customers, not revenue. No market research grounds the range. |
| The service response eta | 0 to 0.5 | `scenario` | `COMM-723`: at 0 more service brings no customers; at 0.5 twice the service brings 41 percent more. No market research grounds the range. |
| The fill floor | 0.75 of the terminals' busy-hour beams | `scenario` | `COMM-725`: a reading of the investor's "We do not want half our network used". |
| The robust floor | 0.75 of the draws | `scenario` | `COMM-725`: a reading of the investor's "Take the clearly usable ones and then pick where you are". |
| The margin floor | 50 percent, on the whole business | `scenario`, investor-set | `COMM-725`: the investor, 2026-10-06 and 2026-10-07 ("I think about a 50% floor for margin"). |

The posture the product case states with its numbers: the headline is the
central market, each response at the middle of its range, the typical market
(ADR 012), which sits a little below the median of the markets where the pick
is usable; the prices are held flat in nominal dollars and inflation is not
modeled; IoT is uncapped, bounded only by its uplink room, its random access
and its tone time, which the usable test checks, and no IoT count is ever set;
the pick holds the investor's prices and chooses only each IoT class's usage;
people and devices are never added; government is left out of revenue.

## The Assumptions Register

The assumption-class values in the models, with provenance. Investor-set
means the investor chose or confirmed the value; convention means a stated
modeling or engineering convention.

### Investor-Set Values

| # | Assumption | Value |
|---|---|---|
| 1 | Exclusive-spectrum baseline (7.775 rounded up) | 8.0 MHz |
| 2 | The panel, the validated Flatellite body (2026-10-03) | 15.4 m^2 |
| 3 | Satellites per launch, with the Neutron block upgrade assumed from the first launch | 16 |
| 4 | Each class's usage (2026-10-04): rate while active; share of users active at the busy hour; off-peak | 2, 5 and 0.75 Mbps; 2.5, 10 and 2.5 percent; 0.5, 2 and 0.5 percent |
| 5 | The terminal prices, held flat (2026-10-07) | $10 and $50 a month |
| 6 | The phone class's price floor (2026-10-03) | $15 a month |
| 7 | The product case's IoT prices, held flat (2026-10-06) | $3 and $6 a month |
| 8 | The product case's FY2036 usage (2026-10-12) | 9 GB, 90 GB, 13 bursts a day |
| 9 | Operations cost, a line to research later, stated in output | 0.0 dollars per year |
| 10 | Coverage floor (simulation-informed conservative scenario; see the dial's honest bounds): it gates every sale | 340 satellites |
| 11 | Communications share of Neutron cadence (all-in, pedal to the metal; investor-set 2026-07-14) | 1.0 |
| 12 | Satellite build cost (investor-flat 2026-07-09, below the prior 1.05 dial and the V3 anchor; the shared config default 1.05 untouched) | 1.0 million dollars |
| 13 | The margin floor on the whole business (2026-10-07); each class alone at or above break-even; the engineering model's own margins published, never tested against 50 percent | 50 percent |
| 14 | Government left out of revenue (2026-10-04) | out |
| 15 | IoT: the engineering model's capacity and the product case's demand; no IoT count is ever set (2026-10-06) | no count |
| 16 | Data IoT's anchor beside the IoT segment: half its count at double its ARPU (2026-10-04) | 0.5 and 2.0 |

### Why The Cadence Share Is 1.0 (Pedal To The Metal)

The communications share of Neutron cadence (row 11) is an investor-set
scenario dial, not a derived number. As of 2026-07-14 the baseline goes
all-in: share 1.0, the whole modeled Neutron manifest flying communications
satellites. The reasoning is framework consistency: every application in this
repository answers the same all-in question the data-center model answers,
what happens if you go pedal to the metal? Each application runs as if it had
all of Neutron's launches to itself, so their headlines never add.

Under it the fleet flies every launch the ramp allows, 16 satellites to a
launch: 2, 3, 5, 9 and 14 launches from FY2027 to FY2031 (33 in all, 528
satellites flying), then 22, 35, 51, 70 and 90 to FY2036 (301 in all, 4,288
flying). The coverage floor is first passed in FY2031. There is no fleet
target, no hold and no cap: every launch on the ramp flies communications
satellites in every year to the horizon, and the fleet never stops growing
inside it (in FY2036 it replaces 224 satellites and still grows). The share
applies from year one with no phase-in, an aggressive stated assumption chosen
deliberately: the goal is a realistic, clearly-stated trajectory, not manifest
precision. A lower share is a sensitivity: it flies fewer launches each year
and passes the floor later.

### Conventions And Modeling Posture

| # | Assumption | Value |
|---|---|---|
| 17 | Spectral-efficiency centrals are band midpoints | 0.65; 2.5 bps/Hz |
| 18 | Small-terminal band edges (ladder convention) | 1.5 / 2.5 bps/Hz |
| 19 | Small-terminal device spec (about 10 dBi on a self-orienting mount, investor decision 2026-07-10) drives its computed SE | 2.0 bps/Hz |
| 20 | Every seat sold: each year each people class serves every person its living fleet carries; each class's column is the whole fleet sold to that class alone, never summed (ADR 006) | every seat |
| 21 | People per class: the curve's capacity at the year's living fleet, times d and the panel factor, over the class's busy-hour load, rounded half up | from the curve |
| 22 | Off-peak per-user rate capped by the single-beam pool (the beam is the per-person ceiling) | min(pool, ratio) |
| 23 | Capacity linear in the panel's area (the panel rule): below the 25 m^2 reference every class carries at least what the rule gives; computed at 15.4 m^2 directly, the small terminal up to about 1.8 percent more, the phone class up to about 1.1 percent more and the mounted terminal exactly what the rule gives; each beam's rate held at its reference value, the link effect of another panel not modeled (the curve's stated limits) | factor = area / 25 |
| 24 | The curve is computed with the band in full-time use (d = 1); the engine scales people by d and ignores how d relaxes each cell's people cap inside the curve. Measured at the design's one usage, not the promoted settings, a run at d = 0.67 carries 0.50 to 2.75 percent more people for the small terminal and 0.74 to 3.66 percent more for the mounted terminal than the curve times d, the phone class 0.012 percent or less (an estimate; `research/direct_communication/iridium_saturation_module.md`, Section 2.1) | one-sided, small |
| 25 | The curve's demand: every resident of an inhabited cell on a shipped 2030 population grid, take-up 1, the maximal-demand bound; beams over oceans and empty land carry no one (ADR 009) | every resident |
| 26 | The curve's other stated limits: fluid beams, idealized 3 dB footprints and one circular shell; residential population, every place at its busy hour at once; no terrain or building blockage and no interference from other systems; the directional terminals' -20 dB pattern floor an estimate, optimistic for the small terminal; no interference trim for the directional classes; the phone class's trim a sampled mean, read where it levels off (about 16.5 percent at the -0.4 dBi floor from 20,022 satellites up, the steps between rows within about 0.1 point, the draws' noise), never row to row | carried in the artifact |
| 27 | The full cadence: no fleet target, no hold and no cap; no saturation number sizes, caps, stops or slows the build (ADR 005) | full cadence |
| 28 | A fleet past a class's last computed row is refused, never extrapolated or clamped | refused |
| 29 | Scenario label lives in one place on the Iridium block | single home |
| 30 | Base year 2026, horizon 10 years (data-center mirror timeline) | FY2036 end |
| 31 | Cadence ramp anchors: 14 at year 5, 90 at year 10, ceiling 150, first launch index 1 (scenario, not Rocket Lab guidance) | shared spine |
| 32 | Launch-cost curve: 25.0 to 13.5 million dollars, log-linear over 5 to 100 launches per year; the iridium scenario overrides it FLAT at 13.0 (both cost anchors set equal, investor simplification 2026-07-09; the shared-spine default curve untouched) | shared spine, scenario-flattened |
| 33 | Satellite lifetime, the five-year cohort cliff | 5 years |
| 34 | The purpose-built L-band satellite is priced investor-flat at 1.0 million dollars, 16 to a launch on the 15.4 m^2 panel; its cost-equivalence to the cellular family's satellite is asserted, not argued | carried |
| 35 | The 10.5 MHz depends on winning the live FCC coordination (authorized today: 7.775 plus 0.95 shared) | contingent |
| 36 | Deployment is the full cadence from 2026, not deal-timed (close mid-2027) | a shape, not a dated plan |
| 37 | No spares, no launch failures, no satellite failures inside the five-year life | perfect fleet |
| 38 | The equality tripwire in its new form: an Iridium run and a cellular run whose fleet target the horizon never reaches share the fleet-and-cost record whole, and that record's values are frozen | tripwire |
| 39 | IoT carries no people load: the people classes are sized on the downlink, IoT on the uplink's room, beside them | beside |
| 40 | The flat cost model (investor-set simplification, 2026-07-09): launch cost 13.0 million dollars at every cadence and satellite build cost 1.0 million dollars, no stepped pricing as launches scale; both in-band of the research anchors; scenario overrides only, the shared-spine defaults untouched (the cellular family and the equality tripwire still see the defaults) | flat 13.0 / 1.0 |
| 41 | The product case's headline is the central market; its terminals sell the engineering case's seats in today's mix of beams (75.7 and 24.3 percent, the anchors' busy-hour load as beams) | central market |

## Model Output Anchors

These values are read from the promoted JSON, not external facts. All are
`derived_estimate`.

### The Engineering Case (`iridium-v7`, stamp 2026-10-13)

| Output | Value |
|---|---|
| Satellite peak (small terminal, mounted terminal, phone class) | 1.4784, 1.848 and 0.48048 Gbps |
| A beam's downlink pool | 10.72, 13.4 and 3.484 Mbps |
| Per-user rate, busy hour / off-peak | 2.0 / 10.0, 5.0 / 13.4 and 0.75 / 3.484 Mbps |
| Beams a satellite | 92.4 (150 at the 25 m^2 reference panel) |
| Living fleet (FY2031, FY2033, FY2035, FY2036) | 528, 1,360, 3,072 and 4,288 satellites |
| Cumulative launches (same years) | 33, 90, 211 and 301 |
| Coverage floor first passed | FY2031 |
| The fleet's cost a year (same years) | 191.4, 493.0, 1,113.6 and 1,554.4 million dollars |
| Cost a satellite-year | 0.3625 million dollars |
| Total cost through FY2036 | 8,729.0 million dollars |
| FY2036 replacement cost | 406.0 million dollars (224 satellites) |
| Small terminal alone, FY2031 / FY2036 | 4,139,229 people, 496.7 million dollars, 61.5 percent / 24,607,046 people, 2,952.8 million dollars, 47.4 percent |
| Mounted terminal alone, FY2031 / FY2036 | 526,557 people, 315.9 million dollars, 39.4 percent / 3,527,090 people, 2,116.3 million dollars, 26.5 percent |
| Phone class alone, FY2031 / FY2036 | 3,560,271 people, 640.8 million dollars, 70.1 percent / 20,823,193 people, 3,748.2 million dollars, 58.5 percent |
| Saturation numbers | 19,995; not reached by 55,407; 20,652 |
| Where the next satellite stops paying, at full price | from about 6,006 (small terminal), 5,402 (mounted terminal) and 8,010 (phone class) satellites: rows of the curve, each crossing within a row's spacing |
| The readings: each a fleet and what it costs a year | the coverage floor, 340 satellites: 123.25 million dollars. The retired 2,000 cap, kept for comparison: 725.0 million. The horizon-end reach, 4,288 satellites: 1,554.4 million. The steady state beyond the horizon, 7,200 satellites: 2,610.0 million. |
| IoT's room, FY2031 / FY2036 | payload 6.6 / 38.5 Gbps; access attempts 1.1 / 6.4 million a second; tones 13.5 / 78.9 million at once |
| IoT capacity, each class alone, FY2031 / FY2036 | minimal-packet 1,965,864,139 / 11,497,881,052; data IoT 170,588,558 / 997,732,709 |

### The Product Case (`product-case-v1`, stamp 2026-10-13)

| Output | Value |
|---|---|
| The pick | minimal-packet IoT at x8 (768 messages a day by FY2036), data IoT at x1 (13 bursts); usable in 1,744 of 2,000 markets |
| The network's scale, FY2031 / FY2036 | 7.8 / 46.6 times today's terminal network |
| FY2031, the central market | 2,194.6 million dollars at a 91.3 percent margin; profit 2,003.2 million dollars |
| FY2036, the central market | 13,156.2 million dollars at an 88.2 percent margin; profit 11,601.8 million dollars |
| FY2036 by class | small terminal 18,636,082 at $10, 2,236.3; mounted terminal 855,857 at $50, 513.5; minimal-packet IoT 184,890,668 at $3, 6,656.1; data IoT 52,087,110 at $6, 3,750.3 (million dollars a year) |
| FY2036 revenue over the usable draws | 10th, 50th and 90th percentiles 8,055.3, 14,159.9 and 26,338.7 million dollars; the headline at the 44.5th |
| All-draw basis | 73 of the 2,000 markets sell IoT past its room in some year |
| The fleet's cost per GB carried (FY2031 to FY2036) | $0.6608, $0.5678, $0.5329 and $0.5218 |
| The IoT anchors' run rate | 373.1 million dollars a year, twice Iridium's IoT revenue today (186.5) |

## Alternatives, One Line Each

- **A cut a reader applies.** A lower price divides the revenue and leaves the
  people; a smaller market divides both. Every margin is re-derived against
  the same fleet cost, never divided. The phone class keeps its $15.
- **Without the block upgrade.** 15 satellites a launch: the fleet is 15 / 16
  of the default, 4,020 satellites in FY2036.
- **Another panel.** People scale with the panel's area: 14.0 m^2, the panel
  with clearance (`COMM-711`), gives about 0.909 times. Below the reference
  panel every class carries at least what this gives.
- **The coordinated 10.5 MHz.** About 31 percent more people and class revenue
  (10.5 / 8 = 1.3125); the fleet and its cost unmoved; the curve is computed at
  8 MHz.
- **IoT at $4 and $8, the investor's earlier prices.** A side run of the
  product case's command: the pick holds, and the central market's revenue is
  the same (13,156.2 million dollars at 88.2 percent in FY2036); the devices
  fall to three quarters (138,668,001 minimal-packet and 39,065,332 data IoT in
  FY2036), and 1,807 of 2,000 markets are usable.

## Catalog Status

The catalog reconciliation is complete: `research/SOURCE_INDEX.md` carries
every claim block these models cite, end to end through `COMM-726` (the
spectrum fundamentals, Iridium acquisition, band designations, Iridium
capacity and modernization, the device gate, and MSS spectrum expansion were
indexed as Waves 8 and 9 on 2026-07-08; the panel, the launch counts and the
saturation module's inputs, `COMM-711` to `COMM-721`, landed 2026-10-05; the
product case's five rows, `COMM-722` to `COMM-726`, on 2026-10-13). The only
gaps in the id space are the documented reserved-unused ranges:
`COMM-191..196`, `COMM-366..370`, `COMM-379..385`, `COMM-440..480`,
`COMM-513..520`, `COMM-575..600`, and `COMM-677..685`.

## Maintenance Rule

When a default assumption changes:

1. Update this ledger, and `research/SOURCE_INDEX.md` if the claim trail
   changes.
2. If the change is to one of the saturation curve's inputs, run the
   saturation command first (`python -m communications.saturation`): about 30
   minutes and a 14 GB memory bound on its last measured run (the curve's
   `provenance.run_measurement`), one at a time. Of the scenario's settings
   only the held spectrum is such an input; the rest are named constants (each
   class's usage and spectral efficiency, the shell, the demand grid). A run on
   a curve computed for other inputs is refused, naming the first that differs.
3. Every other Iridium setting (the panel, satellites per launch, the downlink
   share, the prices, the costs, the cadence share) runs on the promoted curve:
   re-promote the Iridium model with its command alone.
4. After any re-promotion of the Iridium model, re-promote the product case:
   it reads the engineering artifact and records its SHA-256.
5. A terminal price is one price list: change it in both scenarios
   (`iridium.yaml` and `product_case.yaml`) and in both ledger rows.
6. Then review `communications/conclusion.md`. Promotion does not rewrite the
   static conclusion for you.
