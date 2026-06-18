# Falcon 9 Cadence Ramp Over Time, and What It Implies for the Starship Orbital-Data-Center Timeline

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:**
- [`research/competitors/starship_addendum.md`](starship_addendum.md) (Starship status, reuse state, cadence-gap analysis, and the AI-1 reveal). This doc supplies the Falcon-9 *historical* evidence that the addendum references but does not tabulate.
- [`research/rocket_lab/neutron/launch_cost_economics.md`](../rocket_lab/neutron/launch_cost_economics.md) (Falcon 9 used as the cost analog for Neutron; cadence-dependent $/flight).
- [`research/peer_review/review_engineer.md`](../peer_review/review_engineer.md) (Falcon-9 cadence ceilings: the all-time record of 165/yr, the ~209/yr three-pad theoretical ceiling, and per-pad turnaround as the limiting factor).

This is a side investigation that several tracks (communications, data center) will share. It is written neutrally so any track can pull from it. It carries no go/no-go verdict on the Rocket Lab venture itself.

---

## Summary / Verdict

**Confidence: medium-high** on the historical cadence record (it is a counted, public fact, cross-checked across multiple trackers); **medium** on the forward Starship inference (it is a reasoned projection over an unproven vehicle, so it inherits real uncertainty).

Falcon 9 took **about 14 years to go from 2 launches in its first year (2010) to a record 165 in 2025** [FACT]. The curve is not smooth. It sat in the single digits and low teens for its first six years, and only bent sharply upward **after two things were both true at once: (1) booster reuse was routine and trusted, and (2) SpaceX had its own high-volume internal payload (Starlink) to fill the manifest.** The visible inflection is roughly **2021 to 2022**, when annual cadence roughly doubled from 31 to 61, then climbed to 96, then 134, then 165 [FACT].

Two facts matter most for the Starship question:

1. **The first orbital-class booster landing (Dec 2015) and the first reuse of a booster (Mar 2017) were separated by about 15 months, and getting reuse to a *routine, manifest-dominating* state took until roughly 2020 to 2021** [FACT]. Landing a stage once is not the same as reflying stages at high tempo. There was a multi-year maturation gap between "we recovered one" and "reuse drives our rate."

2. **Falcon 9 reuse is on the BOOSTER (first stage) plus the fairing, NOT the whole stack.** The Falcon 9 second stage has always been expendable [FACT]. Starship's promise is different in kind: it requires reusing the *upper stage* (the "Ship"), which on Falcon 9 was never even attempted. As of the May to June 2026 record, no Starship upper stage has been recovered or reflown ([`starship_addendum.md`](starship_addendum.md)). So Starship does not get to inherit Falcon 9's cadence curve. It has to build a *new* reuse-maturation curve for a harder problem, starting from a vehicle that in 2025 flew 5 times against a 25-flight target ([`starship_addendum.md`](starship_addendum.md)).

**On the founder's thesis (3 years vs at least about 5 years to anything significant for orbital data centers on Starship):** the Falcon-9 analogy supports the founder's "at least about 5 years" framing over the "about 3 years" claim, and supports it strongly. Even granting an aggressive schedule, the chain Starship must complete (upper-stage recovery, then repeated upper-stage reflight, then a cadence ramp, then a deployed and operating data-center constellation at scale) is longer and harder than the chain Falcon 9 ran, and Falcon 9's own equivalent chain took the better part of a decade to reach manifest-dominating tempo. A "significant orbital data center within about 3 years" (i.e. by roughly 2029) would require Starship to compress, on its hardest unsolved problem, a maturation that Falcon 9 needed many years for on an easier one. That is not impossible, but it is well outside the demonstrated track record, and the near-term Starship payload that actually fits the vehicle's likely 2027 to 2029 capability is communications (Starlink-class deploys), not data centers.

---

## 1. Falcon 9 launches per year, 2010 to 2026

The table below is Falcon 9 family launches by calendar year. Where a source reports Falcon 9 separately from Falcon Heavy, the Falcon-9-only figure is given first and the family total (including Falcon Heavy) in parentheses. The early-year figures (2010 to 2015) are SpaceX-total launches in that window, which were all Falcon 9 (Falcon 1 had retired in 2009), so they are effectively Falcon-9 counts.

| Year | Falcon 9 launches (family total) | Notes |
|---|---|---|
| 2010 | 2 | Maiden flight June 2010 [FACT] |
| 2011 | 0 | No launches that calendar year [FACT] |
| 2012 | 2 | First Dragon cargo flights [FACT] |
| 2013 | 3 | v1.1 introduced [FACT] |
| 2014 | 6 | [FACT] |
| 2015 | 7 | First orbital-class booster landing, Dec 2015 [FACT] |
| 2016 | 8 | First droneship landing (Apr 2016) [FACT] |
| 2017 | 18 | First reuse of a flown booster (Mar 2017); cadence jumps [FACT] |
| 2018 | 21 (incl. Falcon Heavy debut) | Block 5 introduced May 2018 [FACT] |
| 2019 | 13 | A down year (manifest gap before Starlink scaled) [FACT] |
| 2020 | 25 | Starlink ramp begins; fairing reuse becomes routine [FACT] |
| 2021 | 31 | [FACT] |
| 2022 | 61 | The inflection: cadence roughly doubles year over year [FACT] |
| 2023 | 91 (96) | 91 Falcon 9 + 5 Falcon Heavy [FACT] |
| 2024 | 132 (134) | 132 Falcon 9 + 2 Falcon Heavy [FACT] |
| 2025 | 165 (165) | All-time annual record by any operator [FACT] |
| 2026 (to mid-June) | ~69 (~70) | About 69 Falcon 9 + 1 Falcon Heavy through mid-June; SpaceX guiding to ~140 to 145 for the full year [FACT / PROJECTION] |

**FLAGGED ESTIMATE / reconciliation note.** Trackers differ by a launch or two on individual years depending on whether they count Falcon-9-only or Falcon-family, and on exactly where a launch near a year boundary falls. The shape of the curve is not in dispute. Cross-checked values: 2016 = 8, 2017 = 18, 2018 = 21, 2019 = 13, 2020 = 25, 2021 = 31, 2022 = 61, 2023 = 96 (family), 2024 = 134 (family), 2025 = 165 ([ElonX SpaceX statistics](https://www.elonx.net/spacex-statistics/), [Wikipedia: List of Falcon 9 and Falcon Heavy launches](https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches), [Data Explained: SpaceX launches by year](https://dataexplained.com/trends/spacex-launches-by-year/)). All-time Falcon 9 family launches stand at **664, with a 99.55% success rate (661 full successes, 2 in-flight failures, 1 pre-flight, 1 partial)** as of mid-June 2026 [FACT] ([Wikipedia](https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches)).

### The shape, in words

- **2010 to 2016 (about 7 years): single digits, flat.** Falcon 9 averaged roughly 5 launches a year. The vehicle was being proven; landings were being attempted and mostly failing.
- **2017 to 2019: low double digits, bumpy.** Reuse began (2017), but cadence actually *dipped* in 2019 to 13. Reuse alone did not produce high cadence. There was no large internal manifest yet to fly.
- **2020 to 2021: the ramp begins (25, then 31).** Two enablers arrive together: Starlink becomes a high-volume internal customer, and both booster and fairing reuse become routine rather than experimental.
- **2022 onward: the steep climb (61, 96, 134, 165).** Annual cadence roughly doubled in 2022 and then kept climbing. This is the regime the cheap-$/kg and high-throughput economics actually live in, and it arrived **about 12 years after the first flight and about 6 to 7 years after the first booster landing.**

---

## 2. The reuse inflection: landing once is not the same as flying often

This is the crux for the Starship inference, so it is worth separating the milestones carefully.

| Milestone | Date | What it proved [FACT] |
|---|---|---|
| First orbital-class booster landing | 21/22 Dec 2015 (Orbcomm OG-2, Landing Zone 1) | A first stage can be recovered intact. One stage, once. ([Wikipedia: Falcon 9 flight 20](https://en.wikipedia.org/wiki/Falcon_9_flight_20), [SpaceNews](https://spacenews.com/falcon-9-launches-orbcomm-satellites-first-stage-lands/)) |
| First droneship landing | Apr 2016 (CRS-8) | Recovery works at sea, expanding the envelope of recoverable missions. |
| First reuse of a flown booster | Mar 2017 (SES-10, on the recovered CRS-8 booster) | A recovered stage can fly a second time and still succeed. ([Wikipedia: SpaceX reusable launch system development](https://en.wikipedia.org/wiki/SpaceX_reusable_launch_system_development_program)) |
| Block 5 (reuse-optimized) introduced | May 2018 | The variant designed for rapid, repeated reflight with minimal refurbishment. ([Wikipedia: Falcon 9](https://en.wikipedia.org/wiki/Falcon_9)) |
| Fairing reuse becomes routine | 2020 | 35 of 42 fairing halves launched in 2020 were recovered reflyable; reuse moves from booster-only toward most of the vehicle (minus the second stage). ([Wikipedia: SpaceX fairing recovery program](https://en.wikipedia.org/wiki/SpaceX_fairing_recovery_program)) |
| Reuse dominates the manifest | ~2020 to 2021 onward | The overwhelming majority of launches now fly a flight-proven booster (about 95% of 2025 launches used a reused booster). ([ElonX](https://www.elonx.net/spacex-statistics/)) |

**The key gaps, stated plainly:**

- **First landing (Dec 2015) to first reuse (Mar 2017): about 15 months** [FACT]. Recovering a stage and trusting it enough to refly it are different problems separated by more than a year of work.
- **First reuse (2017) to reuse-driven high cadence (2022): about 5 years** [FACT]. Even after the first reflight, it took roughly half a decade, the purpose-built Block 5, fairing recovery, and a large internal manifest before reuse actually produced the steep cadence climb.
- **First landing (2015) to record cadence (2025): about 10 years** [FACT].

### How far booster reuse eventually matured

Reuse did not just become routine, it became deep. The reuse maturation, by the numbers [FACT]:

- Falcon 9 first-stage boosters have landed and been recovered **623 of 636 attempts** (about 98%) ([orbital trackers, June 2026](https://en.wikipedia.org/wiki/List_of_Falcon_9_first-stage_boosters)).
- The fleet-leader booster **B1067 has flown 35 times** (as of June 2026); the prior fleet leader B1058 was the first to reach 14, then 19 flights ([Wikipedia: List of Falcon 9 first-stage boosters](https://en.wikipedia.org/wiki/List_of_Falcon_9_first-stage_boosters)).
- Fairing halves have been reflown **more than 300 times**, with the most-reflown half flying about 36 times ([Wikipedia: SpaceX fairing recovery program](https://en.wikipedia.org/wiki/SpaceX_fairing_recovery_program)).
- The shortest booster turnaround reached about **9 days** between flights of the same stage [FACT, single source: this specific record is reported by one tracker and should be double-checked] ([Wikipedia: List of Falcon 9 first-stage boosters](https://en.wikipedia.org/wiki/List_of_Falcon_9_first-stage_boosters)).

That depth of reuse (35 flights on one booster, 9-day turnaround) took roughly a decade of iteration to reach. It is the end state, not the starting point. The peer-review engineering doc ([`review_engineer.md`](../peer_review/review_engineer.md)) uses exactly these reference points: the 165/yr record, the approximately 209/yr three-pad theoretical ceiling, and the finding that per-pad turnaround is the fundamental limiting factor on cadence.

---

## 3. The honest framing: Falcon 9 reuse is partial, and Starship's problem is harder

This is the single most important correction to any "Starship will inherit the Falcon 9 ramp" intuition.

**Falcon 9 reuses the booster and the fairing. It has never reused the second stage.** The Falcon 9 upper stage is expended on every flight [FACT]. This is exactly why [`launch_cost_economics.md`](../rocket_lab/neutron/launch_cost_economics.md) notes that Falcon 9's expendable second stage is "close to half" the cost of goods per vehicle, and why Neutron's own expendable upper stage is modeled the same way. Falcon 9 got cheap on the *first stage*, not the whole stack.

**Starship's entire economic case depends on reusing the upper stage** ([`starship_addendum.md`](starship_addendum.md) Section 2). Musk has called the reusable upper-stage heat shield "by far the biggest remaining challenge." As of the May to June 2026 record:

- The Super Heavy *booster* has been reused and tower-caught (Falcon-9-like progress on the easier half).
- The *upper stage* (Ship) has **never been recovered or reflown**. Ships have reached controlled ocean splashdowns and shown heat-shield erosion and flap damage, but none has been caught or flown a second time ([`starship_addendum.md`](starship_addendum.md)).
- Starship flew **5 times in 2025 against a 25-flight target, a 5x miss** ([`starship_addendum.md`](starship_addendum.md)).

So Starship is, in mid-2026, roughly where Falcon 9 was in the **2015 to 2017** window on the part that matters most: it can recover the booster, but it has not demonstrated repeated reuse of the stage whose reuse defines the business case. And the stage it still has to solve (a hypersonic-reentry upper stage) is materially harder than the booster Falcon 9 solved.

**Therefore Starship reuse will not be at an immediate high pace.** Even on an aggressive schedule, Starship has to run its own maturation curve: recover an upper stage at least once, then refly an upper stage, then make that routine, then ramp cadence, then build out a constellation. Falcon 9's equivalent curve, on an easier problem, ran from roughly 2015 to 2022 before reuse drove high tempo. There is no physical or historical basis for assuming Starship compresses the harder version of that curve into a fraction of the time.

China note (excluded from the main analysis, recorded here only as an aside): China has flown reusable-booster test articles and has multiple commercial reusable-launch programs in development, but none has reached Falcon-9-class operational reuse or cadence; this does not change the Starship-specific timeline analysis above.

---

## 4. The 3-year vs about-5-year question for orbital data centers

**The claim to assess:** some hold that Starship will run orbital data centers within about 3 years (i.e. by roughly 2029). **The founder's view:** communications, not data centers, is the near-term Starship payload, and even on an aggressive schedule it will be **at least about 5 years** before Starship delivers anything significant for orbital data centers.

### What "significant orbital data centers on Starship" actually requires

Lay out the dependency chain. Each link is a precondition for the next [PROJECTION, reasoned from the addendum and the Falcon-9 record]:

1. **A reusable, operational Starship upper stage.** Not yet demonstrated even once. This is the gating item. ([`starship_addendum.md`](starship_addendum.md))
2. **Repeated upper-stage reflight at low refurbishment.** The Falcon-9 analog: first landing to first reuse was about 15 months; first reuse to *routine* reuse was about 5 more years. Starship's upper-stage problem is harder.
3. **A sustained high flight cadence.** [`starship_addendum.md`](starship_addendum.md) Section 2 puts meaningful sub-$100/kg lift at usable cadence at roughly 2028 to 2031, and notes Starbase is FAA-capped at 25 launches/yr (SpaceX is seeking overseas sites specifically to break that ceiling). The peer-review doc ([`review_engineer.md`](../peer_review/review_engineer.md)) independently caps even a mature single-site, single-vehicle operation well below the volumes a GW-scale data-center constellation would need.
4. **Deployed, commissioned, operating data-center satellites at scale.** Even SpaceX's own AI-1 design is, as of June 2026, a render with nothing built or flown, and press projections (explicitly not SpaceX commitments) place first deployments at about 2028 ([`starship_addendum.md`](starship_addendum.md), 2026-06-09 update).

A 3-year timeline (by ~2029) requires all four links to complete in sequence, starting from a vehicle that has not yet finished link 1. A roughly-5-year timeline (by ~2031) lines up with the addendum's own independently-derived "2028 to 2031" window for cheap, usable-cadence lift, plus the time to actually deploy and operate a constellation on top of that lift.

### Why communications is the more credible near-term Starship payload

This supports the founder's framing directly:

- **Communications payloads (Starlink-class) fit the vehicle's actual near-term capability.** They tolerate the current expendable-upper-stage, lower-cadence regime, because Starlink deploys are SpaceX's own internal manifest and do not require the full cheap-$/kg end state to be worth flying. Block 3 Starship is explicitly built to carry Starlink-simulator deploys ([`starship_addendum.md`](starship_addendum.md) Section 1). The same internal-manifest logic that drove the Falcon 9 inflection (Starlink filling the manifest) applies first to Starship.
- **Data centers need the cheap, high-cadence end state that does not exist yet.** Orbital data centers are the payload that *requires* the bottom of the $/kg curve and a constellation-scale cadence, the part [`starship_addendum.md`](starship_addendum.md) shows is gated to roughly 2028 to 2031 and dependent on the unsolved upper-stage reuse.

### Verdict on the founder's thesis

**The Falcon-9 cadence evidence supports the founder's "at least about 5 years" position over the "about 3 years" claim, with medium-high confidence on the historical reasoning and medium confidence on the forward projection.**

- The "about 3 years" claim implicitly assumes Starship compresses, on its hardest unsolved problem (upper-stage reuse), a maturation that Falcon 9 needed the better part of a decade to complete on an easier problem (booster-only reuse). The historical record gives no precedent for that compression.
- The "at least about 5 years" position is consistent with (a) the addendum's independently-derived 2028 to 2031 window for cheap usable-cadence lift, (b) the additional time to deploy and operate a constellation on top of that lift, and (c) the Falcon-9 lesson that reuse maturity and high cadence arrive years after the first recovery, not with it.
- The communications-first framing is well-supported: communications is the payload class that fits Starship's likely 2027 to 2029 capability, while data centers are the payload class that needs the not-yet-existing cheap, high-cadence regime.

The honest caveat in the other direction, carried from [`starship_addendum.md`](starship_addendum.md) Section 4: booster reuse is already done, Block 3 is flying, and the upper-stage heat shield is "the last big problem," not an unknown one. If SpaceX solves upper-stage reuse quickly in 2026 to 2027, the back half of the chain could compress faster than a linear read of history suggests. That risk is why the founder's bound is sensibly phrased as "at least about 5 years" (a floor) rather than a fixed point estimate, and why the about-3-year claim is better read as a best-case ceiling than a base case.

---

## Sources

- [Wikipedia: List of Falcon 9 and Falcon Heavy launches](https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches)
- [Wikipedia: List of Falcon 9 first-stage boosters](https://en.wikipedia.org/wiki/List_of_Falcon_9_first-stage_boosters)
- [Wikipedia: SpaceX reusable launch system development program](https://en.wikipedia.org/wiki/SpaceX_reusable_launch_system_development_program)
- [Wikipedia: SpaceX fairing recovery program](https://en.wikipedia.org/wiki/SpaceX_fairing_recovery_program)
- [Wikipedia: Falcon 9](https://en.wikipedia.org/wiki/Falcon_9)
- [Wikipedia: Falcon 9 flight 20 (first booster landing, Orbcomm OG-2)](https://en.wikipedia.org/wiki/Falcon_9_flight_20)
- [SpaceNews: Falcon 9 launches Orbcomm satellites, first stage lands](https://spacenews.com/falcon-9-launches-orbcomm-satellites-first-stage-lands/)
- [Space.com: SpaceX lands orbital rocket successfully in historic first](https://www.space.com/31420-spacex-rocket-landing-success.html)
- [ElonX: SpaceX statistics](https://www.elonx.net/spacex-statistics/)
- [Data Explained: SpaceX launches by year](https://dataexplained.com/trends/spacex-launches-by-year/)
- [Wikipedia: List of spaceflight launches in April to June 2026](https://en.wikipedia.org/wiki/List_of_spaceflight_launches_in_April%E2%80%93June_2026)
- Internal: [`research/competitors/starship_addendum.md`](starship_addendum.md), [`research/rocket_lab/neutron/launch_cost_economics.md`](../rocket_lab/neutron/launch_cost_economics.md), [`research/peer_review/review_engineer.md`](../peer_review/review_engineer.md)

---

## Confidence

**Medium-high on the historical cadence record.** Falcon 9 launches per year, the reuse milestone dates, and the all-time totals are counted public facts, cross-checked across Wikipedia's launch list, ElonX, and Data Explained, which agree on the shape and on every load-bearing figure (the single-digit start, the 2021 to 2022 inflection, the 165 record, the 2015 first landing, the 2017 first reuse). Minor year-to-year discrepancies of a launch or two exist between Falcon-9-only and Falcon-family counts and do not affect any conclusion.

**Medium on the forward Starship inference.** The 3-year-vs-5-year assessment is a reasoned projection over an unproven vehicle. It rests on the demonstrated Falcon-9 maturation timeline (strong), the [`starship_addendum.md`](starship_addendum.md) cadence-gating analysis (strong), and an explicit dependency chain (reasonable but not certain). The main downside risk to the "at least about 5 years" floor is a fast SpaceX solution to upper-stage reuse in 2026 to 2027, which is flagged.

---

## Open Questions

- **When does a Starship upper stage fly a second time?** This is the single gating data point, the direct analog of the Falcon 9 Dec-2015-to-Mar-2017 step. Until it happens, every Starship data-center timeline is unanchored. (Also flagged as the top open question in [`starship_addendum.md`](starship_addendum.md).)
- **Does the Falcon 9 first-landing-to-first-reuse gap (about 15 months) predict the Starship equivalent, or is it shorter/longer?** Starship's upper stage is a harder reentry problem, which argues for longer; SpaceX's accumulated reuse experience argues for shorter. Unresolved.
- **Booster turnaround record (about 9 days): single-source.** The specific fastest-turnaround figure comes from one tracker and should be double-checked against a second before it is quoted as a hard fact.
- **2026 full-year Falcon 9 count vs the ~140 to 145 guidance.** Tracking actual 2026 cadence against SpaceX's own stated target is a useful calibration on how reliable forward cadence guidance is (the same skepticism the Starship 5x-miss warrants).
- **Does Starship's communications-first phase actually arrive on the expected 2027 to 2029 schedule?** If Starlink-class deploys slip, the data-center timeline slips behind them, pushing the "significant data centers" date past the about-5-year floor.

---

## Claims table

| COMM- id | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-001 | Falcon 9 first-year launches (2010) | 2 | FACT | [Data Explained](https://dataexplained.com/trends/spacex-launches-by-year/), [Wikipedia](https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches) |
| COMM-002 | Falcon 9 record annual launches (2025) | 165 | FACT | [ElonX](https://www.elonx.net/spacex-statistics/), [Wikipedia](https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches) |
| COMM-003 | Falcon 9 cadence inflection: 2022 roughly doubled prior year | 31 (2021) to 61 (2022) | FACT | [ElonX](https://www.elonx.net/spacex-statistics/), [Wikipedia](https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches) |
| COMM-004 | Falcon 9 climb after inflection | 61 (2022), 96 (2023), 134 (2024), 165 (2025) family totals | FACT | [Wikipedia](https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches), [ElonX](https://www.elonx.net/spacex-statistics/) |
| COMM-005 | Falcon 9 family all-time launches and success rate | 664 launches, 99.55% success | FACT | [Wikipedia](https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches) |
| COMM-006 | First orbital-class booster landing | 21/22 Dec 2015 (Orbcomm OG-2) | FACT | [Wikipedia: Falcon 9 flight 20](https://en.wikipedia.org/wiki/Falcon_9_flight_20), [SpaceNews](https://spacenews.com/falcon-9-launches-orbcomm-satellites-first-stage-lands/) |
| COMM-007 | First reuse of a flown booster | Mar 2017 (SES-10) | FACT | [Wikipedia: reusable launch system development](https://en.wikipedia.org/wiki/SpaceX_reusable_launch_system_development_program) |
| COMM-008 | Gap from first landing to first reuse | ~15 months | DERIVED (from COMM-006, COMM-007) | [Wikipedia](https://en.wikipedia.org/wiki/Falcon_9_flight_20) |
| COMM-009 | Fairing reuse becomes routine | 2020 (35 of 42 halves reflyable) | FACT | [Wikipedia: SpaceX fairing recovery program](https://en.wikipedia.org/wiki/SpaceX_fairing_recovery_program) |
| COMM-010 | Falcon 9 second stage is expendable (reuse is booster + fairing only) | Always expended | FACT | [Wikipedia: Falcon 9](https://en.wikipedia.org/wiki/Falcon_9), [`launch_cost_economics.md`](../rocket_lab/neutron/launch_cost_economics.md) |
| COMM-011 | Booster reuse depth: fleet-leader flight count | B1067 = 35 flights (June 2026) | FACT | [Wikipedia: list of Falcon 9 first-stage boosters](https://en.wikipedia.org/wiki/List_of_Falcon_9_first-stage_boosters) |
| COMM-012 | Booster landing success rate (cumulative) | 623 of 636 attempts (~98%) | FACT | [Wikipedia: list of Falcon 9 first-stage boosters](https://en.wikipedia.org/wiki/List_of_Falcon_9_first-stage_boosters) |
| COMM-013 | Fastest booster turnaround | ~9 days | FACT (single source, double-check) | [Wikipedia: list of Falcon 9 first-stage boosters](https://en.wikipedia.org/wiki/List_of_Falcon_9_first-stage_boosters) |
| COMM-014 | Share of 2025 Falcon 9 launches on a reused booster | ~95% | FACT (single source) | [ElonX](https://www.elonx.net/spacex-statistics/) |
| COMM-015 | 2026 Falcon 9 launches year-to-date (mid-June) | ~69 (~70 family) | FACT | [SpaceXNow / search aggregate](https://en.wikipedia.org/wiki/List_of_spaceflight_launches_in_April%E2%80%93June_2026) |
| COMM-016 | SpaceX 2026 full-year Falcon 9 guidance (Shotwell) | ~140 to 145 | PROJECTION | [search aggregate, Time magazine quote, single source] |
| COMM-017 | Years from first flight to record cadence | ~14 years (2010 to 2025) | DERIVED | [Wikipedia](https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches) |
| COMM-018 | Starship 2025 flights vs target | 5 vs 25 (5x miss) | FACT | [`starship_addendum.md`](starship_addendum.md) |
