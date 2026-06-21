# Communications Thesis: Revision 1 (Belief Record Only)

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:** the neutral base is in [comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md), which sizes the markets and the current state of the technologies. This thesis records only the founder's working hypotheses and the open questions on top of that base; it does not repeat the market or technology numbers.

> **Status: no judgments have been made yet.** This is **Revision 1**, the starting belief record for the communications track. It captures the founder's initial hypotheses so each one can be tested against evidence in later waves. **There is no verdict here, for or against a Rocket Lab space-communications business.** Nothing below is validated. The base research is deliberately separated from these beliefs precisely so the beliefs can be revised (or discarded) as waves land. Read every line as "the current working hypothesis, to be tested," not as a finding.

> **Why a belief record exists at all.** The wider project keeps a versioned thesis so the mental model is written down and each piece can be pressure-tested against physics and economics (the data-center track's equivalent is [initial_thesis.md](./initial_thesis.md)). This is that artifact for communications, at its first revision. It will gain confidence ratings, supporting/contradicting evidence, and eventually a verdict only as later waves justify them.

---

## How to read this document

- Each hypothesis is stated plainly, then annotated with **what the base currently suggests** (a pointer to the baseline synthesis, not a re-derivation) and **what would confirm or break it**.
- Confidence is deliberately withheld at the thesis level for now. The base sections each carry their own confidence; the *beliefs* built on them are unrated until tested.
- The open questions at the end are the ones that decide whether each hypothesis survives.

---

## The working hypotheses

### Hypothesis 1: Diminishing returns past baseline broadband

**The belief:** once a user has baseline broadband (enough for everyday streaming, calls, gaming), additional speed and capacity command rapidly diminishing willingness-to-pay. Communications is therefore a market where "more bandwidth" is not, by itself, a premium product the way "more compute" is.

**What the base currently suggests:** this is the strongest-supported of all the hypotheses. The baseline synthesis (Section 4.1) records a sharply concave willingness-to-pay curve (about $2.34/Mbps at the low end collapsing to about $0.02/Mbps from 100 to 1,000 Mbps), gigabit available to over 91% of US homes but bought by only about 30%, a modal tier of 200-500 Mbps, and flat-to-declining operator ARPU. The value curve rewards **reach and reliability, not raw bandwidth** past a low-hundreds-of-Mbps threshold.

**What would confirm it:** the same plateau showing up outside the US (Europe, the gap regions), and a clean unserved/underserved WTP curve confirming high WTP only at the *connect-at-all* end.

**What would break it:** a new high-bandwidth use case (immersive/AI-native applications, something not yet mainstream) that re-steepens the WTP curve and makes raw bandwidth premium again. This is the main downside risk to the hypothesis and is called out as an open question below.

### Hypothesis 2: Space as a possible step change, whose value depends on economics and new use cases

**The belief:** space-delivered communications could be a genuine step change, but its value is *not* in beating ground broadband on raw speed or price in served markets. It depends on (a) the economics closing for the places ground cannot reach, and (b) new use cases that value what space uniquely offers (ubiquity, a path independent of terrestrial fiber, sovereignty, security, latency on long links).

**What the base currently suggests:** the base supports the *direction* and cautions on the *scale*. Space holds about 0.5% of global fixed broadband today; the realistically served slice of the cited trillion-dollar TAMs is roughly 5-10% of the headline (Morningstar's ~$129B for a mature Starlink versus SpaceX's $1.6T claim). The economically meaningful version of "space replaces ground" is the rural and unserved fringe (coverage gap ~300M people plus underserved rural), not the whole market. Where fiber or upgraded cable already exists, the incumbent defends a passed home for ~$100-300, so space adds little incremental value in served territory (baseline synthesis Sections 2 and 4).

**What would confirm it:** a dollar-sized rural/remote fringe (and premium/sovereign niche) where the space *supply* economics close, plus evidence of a real new use case (orbital-DC backhaul, sovereign networks, resilience-as-a-service) paying a premium.

**What would break it:** the supply-side space economics not closing even in the fringe (the space cost stack is a separate workstream and is not assumed here), or terrestrial reach (FWA, subsidized fiber) closing the gap faster than expected.

### Hypothesis 3: Laser, high bandwidth but weather-limited and possibly assuming fiber is already present

**The belief:** laser/optical is the high-bandwidth, no-spectrum-fight winner, but it is weather-limited (cloud/fog break the link, not degrade it), and much of its terrestrial value proposition may quietly assume fiber is already present (as a backup path, a redundant overlay, or a gap-filler between fiber points), rather than replacing fiber.

**What the base currently suggests:** strongly consistent. The base records optical proven at scale for inter-satellite links (Starlink) and downlink (TBIRD 200 Gbps), but a single optical ground site reaches only ~50-70% availability, needing 4+ diverse ground stations for 99-99.9%. Terrestrial laser (Taara) hits the same fog wall and uses a hybrid FSO/RF link for five-nines; its strong case is *where fiber does not exist*, and alongside existing fiber it adds only conditional value (security, latency, fast deploy). The "possibly assuming fiber is already present" instinct is borne out: the terrestrial-laser doc frames the product as "dark fiber in the sky" and a redundant path, i.e. it lives next to fiber as much as beyond it (baseline synthesis Section 3.2).

**What would confirm it:** a clean availability/cost model showing the weather-diversity overhead, and a use-case map showing where laser is a *primary* link versus a *complement* to fiber.

**What would break it:** a weather-mitigation advance (or a dry-climate-only deployment model) that lets optical stand alone at carrier-grade availability without an RF or fiber backup. The base treats the portfolio (optical + RF complement) as the settled architecture, so a pure-optical standalone would be the surprise.

### Hypothesis 4: Security as a differentiator

**The belief:** security and sovereignty (a controlled, hard-to-intercept, independent path) are a genuine differentiator for space communications, and may be a stronger basis to compete on than bandwidth or price.

**What the base currently suggests:** supported as a real but bounded differentiator. The base records that narrow optical beams are very hard to intercept covertly (a tap requires being inside the beam path), with no RF side-lobe leakage, which defense and intelligence users list as a primary reason for free-space optical. The existing scoped business case ([comms_business_case.md](../laser_comms/comms_business_case.md)) already centers sovereignty/security demand (GOVSATCOM operational, the EUR 10.6B IRIS2 program, "sharply increased" sovereign demand). The caveat the base preserves: it is physical-layer obscurity plus tamper-evidence, not cryptographic security; sensitive traffic should still be encrypted, and how much a buyer pays for the edge over encrypted fiber is judgment, not yet data (baseline synthesis Section 3.2, 3.4).

**What would confirm it:** a sized premium/sovereign/defense niche (the central missing dollar number) and evidence that buyers actually pay for the security/sovereignty edge at a margin.

**What would break it:** the security edge proving to be a feature buyers expect for free rather than pay a premium for, or the sovereign demand being captured by closed national programs (IRIS2-style) a new commercial entrant cannot win.

---

## The thread that ties the hypotheses together (working framing, not a verdict)

The four hypotheses point, *as a current working framing only*, toward a single tension the later waves must resolve:

> **Communications is a diminishing-returns market on the axis ground broadband competes on (raw bandwidth into served homes). The open question is whether space communications escapes that by competing on the axes the value curve actually rewards (reach, reliability, sovereignty, security, latency on long links) and on new use cases (orbital-DC backhaul, resilient/independent paths) rather than on bandwidth or price.**

This is explicitly the founder's comparison to the data-center track, where the economics run the other way (demand outrunning supply, continual hardware upgrades, capacity expansion rewarded; baseline synthesis Section 4.2). **Whether the comms case is strong, weak, or conditional is not decided here.** It is the question Revision 2+ exists to answer.

---

## Open questions (these decide whether the hypotheses survive)

1. **Does a new high-bandwidth use case re-steepen the broadband WTP curve?** Hypothesis 1 rests on demand plateauing; an AI-native or immersive application that makes raw bandwidth premium again would weaken it. (The single biggest risk to Hypothesis 1.)
2. **What is the dollar size of the satellite-addressable rural/remote fringe, and of the premium/sovereign niche?** These are the two missing numbers that turn Hypotheses 2 and 4 from direction into an addressable market (baseline synthesis Section 5).
3. **Do the space *supply* economics close in the fringe?** This thesis is isolated to communications demand and the market base; the space-side cost stack (constellation capex, optical ground-station network, launch cadence) is a separate workstream and is *not assumed* here. Hypothesis 2 depends on it.
4. **Is laser a primary link or a fiber complement, and at what weather-diversity cost?** Hypothesis 3 needs a clean availability/cost model and a primary-vs-complement use-case map.
5. **Will buyers pay a premium for the security/sovereignty edge, or expect it for free?** Hypothesis 4 needs evidence of paid margin, not just stated demand, and needs the closed-program risk (IRIS2-style capture) assessed.
6. **Where does a space comms business sit relative to direct-to-device versus fixed broadband versus premium/sovereign?** The base shows these are different (and partly overlapping) markets; the thesis has not chosen which one(s) the comms track targets. That choice is a later-wave decision, not a current belief.
7. **What is the realistic competitive timing?** The base notes a space entrant would be behind operational players (Kepler optical relay) and beside Starlink; whether the differentiation is enough to win share is unresolved and bears on every hypothesis.

---

## What this revision deliberately does not do

- It does not pick a product (direct-to-device, enterprise/B2B backhaul, wholesale capacity, premium/sovereign network). The base shows these are distinct markets; choosing is a later-wave decision.
- It does not size the Rocket Lab opportunity in dollars. The reference points exist (EUR 10.6B IRIS2, $1.3B SDA optical-mesh contracts, $14.8B LEO-satcom forecast) but the served premium/sovereign niche is unsized; that is the central open number.
- It does not assume the space supply economics. This thesis covers communications demand and the market/technology base only.
- It does not render a verdict. **No judgments have been made yet.** This is the starting belief record, to be revised in later waves.

---

## Revision 2 (the two missing dollar numbers are now sized)

*June 2026. Still a belief record. No verdict.*

Revision 1 named two missing dollar numbers as the gate on Hypotheses 2 and 4 (open question 2: "What is the dollar size of the satellite-addressable rural/remote fringe, and of the premium/sovereign niche?"). Wave 2 sized both. This revision records what landed and updates the confirm/break notes for the two hypotheses those numbers gate. It does NOT change Hypotheses 1 or 3, and it does NOT render a verdict: the sizes are demand-side and ILLUSTRATIVE, and the supply economics and the competitive-share question remain open.

### What landed (the now-sized numbers)

- **The satellite-addressable rural/remote fringe (ex-China): ~$40-55B/yr conservative, ~$95-130B/yr optimistic** [ILLUSTRATIVE]. Sized bottoms-up from sourced household counts and region-specific ARPU. The structural finding underneath it is sharper than the number: the dollars are made in the developed-world rural fringe and the high-value mobility/enterprise verticals, NOT in the billions of unconnected people (the ~3.1B usage gap is an income problem satellite supply does not fix; it adds headcount, not revenue). Source: [comms_rural_fringe_sizing.md](../economics/comms_rural_fringe_sizing.md).
- **The premium/sovereign niche (ex-China): a ~$60-95B/yr total spend pool, of which ~$8-30B/yr is OPEN to a new commercial entrant** [ILLUSTRATIVE on the served range]. The biggest single line items (IRIS2 EUR 10.6B, the SDA tranches, the $2.29B SpaceX SDN award, GOVSATCOM) are closed prime/consortium builds and are demand proof, not addressable revenue; only the commercial-augmentation layer is contestable. The niche trades addressable size (far smaller than the mass market) for margin and durability (far better). Source: [comms_premium_sovereign_sizing.md](../economics/comms_premium_sovereign_sizing.md).
- **The consolidated, de-duplicated new-entrant-addressable pool: ~$45-60B/yr conservative, ~$110-150B/yr optimistic** [ILLUSTRATIVE] (the two pools share the mobility/enterprise verticals, so they are reconciled, not summed). That is **~3-9% of the cited $1.6T** and **in the same band as the ~$129B realistic served estimate** the base established. Two independent methods (this bottoms-up consolidation and Morningstar's top-down rebuild) landing in the same band is the load-bearing cross-check. Source: [comms_addressable_sizing.md](../economics/comms_addressable_sizing.md).

### Hypothesis 2 (space as a possible step change): confirm/break notes updated

Revision 1 said Hypothesis 2 "depends on (a) the economics closing for the places ground cannot reach, and (b) new use cases that value what space uniquely offers," and that what would confirm it was "a dollar-sized rural/remote fringe (and premium/sovereign niche) where the space supply economics close."

**Updated read:** the *demand-side* half of the confirmation has now partly landed. There IS a dollar-sized rural/remote fringe (~$40-55B to ~$95-130B/yr) and a dollar-sized premium/sovereign niche (~$8-30B/yr open), and together they are a real, low-tens-to-low-hundreds-of-billions market, not a rounding error. So the "is there a there there" part of Hypothesis 2 is now supported in dollars, not just in direction. **But the confirmation is only half-complete, and the unfinished half is the load-bearing one:**

- **What would now confirm it (revised):** the space *supply* economics closing against these specific revenue pools (the demand size is no longer the open question; the cost stack is), plus evidence that a specific entrant can win a real share of the shared pie rather than the whole pool.
- **What would now break it (revised and sharpened):** (i) the supply-side space economics not closing even against a ~$45-150B addressable pool (still a separate workstream, still not assumed); (ii) the realistic figure being mostly the *developed-world fringe and mobility verticals* that incumbents (Starlink especially) already serve, so a new entrant competes head-on rather than into open space; or (iii) the optimistic end being an artifact of the carrier direct-to-cell add-on and a price-driven emerging-market expansion that compresses ARPU as fast as it adds users (the exact dynamic that pulled Starlink's blended ARPU down 33% in two years). The honest center of gravity is the conservative-to-mid band, and even that is a *shared* pie with a capacity-gated ramp.

Net: Hypothesis 2 moves from "direction supported, scale unknown" to "direction and demand-scale supported; the open question narrows to supply economics and competitive share." It is NOT confirmed; the gate has simply moved one step downstream.

### Hypothesis 4 (security/sovereignty as a differentiator): confirm/break notes updated

Revision 1 said what would confirm Hypothesis 4 was "a sized premium/sovereign/defense niche (the central missing dollar number) and evidence that buyers actually pay for the security/sovereignty edge at a margin," and what would break it was "the sovereign demand being captured by closed national programs (IRIS2-style) a new commercial entrant cannot win."

**Updated read:** the niche is now sized, and the sizing cuts both ways, landing close to the break condition Revision 1 anticipated.

- **The confirming half:** the premium/sovereign niche is real money (~$60-95B/yr gross), it is structurally higher-margin than mass-market connectivity (it sells on sovereignty, security posture, dedicated capacity, resilience, and latency, the attributes the value curve rewards), and government/defense contracts are long, sticky, and price-insensitive. The demand the hypothesis rests on is quantified and durable.
- **The breaking half (and it largely materialized):** the sizing confirms Revision 1's specific fear. A large majority of the niche is CLOSED to a new commercial-services entrant: the EUR 10.6B IRIS2 is an EU-industry consortium build, GOVSATCOM pools member-state assets, and the SDA/SDN programs (>$300 sats; $2.29B SDN to SpaceX) are defense-prime awards. Only the ~$3-8B/yr commercial-augmentation layer is open. So the sovereign demand IS substantially "captured by closed national programs," exactly the break condition Revision 1 named, leaving a much smaller open slice than the gross pool suggests.
- **What would now confirm it (revised):** evidence that the *open* commercial-augmentation layer (the pLEO IDIQ, allied managed-service buys, augmentation demos) is both growing and pays a genuine security/sovereignty premium at a margin, AND that a new entrant can win a share of it beside the incumbents (Starshield is already the dominant buyer of the open layer to date).
- **What would now break it (revised):** the open layer staying small and incumbent-captured (Starshield-dominated), or the security/sovereignty edge proving to be a feature buyers expect inside a managed-service contract rather than a separately-priced premium. The closed-program risk is no longer a hypothetical; it is a measured fact that shrinks the addressable slice.

A neutral note recorded for context, not scored: Rocket Lab uniquely sits on the *closed-prime* side already (>$1.3B in SDA awards), which is a different business from the commercial-managed-service niche sized here. That is relevant to any later verdict but does not change this belief record.

### What Revision 2 deliberately does not do

- It does not render a verdict. The two numbers are demand-side and ILLUSTRATIVE; the supply economics, the single-operator capture rate, and the per-segment margin remain open (now the top open questions, replacing "what is the dollar size").
- It does not change Hypothesis 1 (diminishing returns) or Hypothesis 3 (laser weather-limited / fiber-adjacent); no wave-2 evidence bore on them.
- It does not pick a product. The sizing shows the rural fringe, the mobility/enterprise verticals, the open government layer, and direct-to-cell are different (and partly overlapping) pools; choosing which the comms track targets is still a later-wave decision.
- It does not assume the space supply economics. That remains a separate workstream and is the gate that Hypothesis 2's confirmation now waits on.

---

## Revision 3 (the cost side now has a test: the ground-vs-space ratio and the marginal-cost floor)

*June 2026. Still a belief record. No verdict.*

Revision 2 narrowed Hypothesis 2's open gate to one thing: "the space *supply* economics closing against these specific revenue pools (the demand size is no longer the open question; the cost stack is)." Wave 3 built that cost side. Three docs landed it: the space supply-cost stack ([comms_space_supply_cost.md](../economics/comms_space_supply_cost.md)), the ground incumbents' margins and marginal-cost floor ([comms_incumbent_margins_competitive_floor.md](../economics/comms_incumbent_margins_competitive_floor.md)), and the consolidation that turns them into the headline ratio ([comms_ground_vs_space_cost_ratio.md](../economics/comms_ground_vs_space_cost_ratio.md)). This revision records what the cost side now says and updates the confirm/break notes for Hypothesis 2, which is the hypothesis the cost test bears on. It does NOT change Hypotheses 1, 3, or 4, and it does NOT render a verdict: the ratio is a cost-and-competitive base, the entrant-specific cost stack (a Rocket Lab-scale constellation rather than Starlink) is still unmodeled, and competitive share remains open.

### What landed (the cost-side findings)

- **The ground-vs-space delivery-cost ratio is not one number; it is two that point in opposite directions, split by whether the ground plant already exists.** This is the comms mirror of the data-center track's orbit-to-ground 1.92x, and the honest mirror is a fork, not a constant.
  - **Flavor (a), space vs a FRESH GROUND BUILD (the unserved-area comparison, the true mirror of 1.92x):** annualized per subscriber, space is **BELOW** ground build cost, by roughly **1.3x to 3.2x in ordinary rural areas** and by tens-fold (~65-90x) in the extreme remote tail; the crossover sits around the dense-suburban fringe. Space wins on cost where there is no incumbent. This runs the *opposite* direction to the data-center 1.92x (where the orbital build is the costlier side), because terrestrial comms-to-a-home gets more expensive per unit as density drops, while space carries a flat per-location cost.
  - **Flavor (b), space vs the INCUMBENT'S MARGINAL COST (the served-area comparison the data-center track never faces):** space is **ABOVE** the incumbent's cash cost to defend an already-connected subscriber, by roughly **3x to 8x** (the incumbent defends at ~10-20% of ARPU on sunk fixed plant, ~$84-180/sub/yr, versus space ~$480-680/sub/yr), and per-GB on fixed broadband space is ~5-30x+ above the incumbent's sub-penny marginal cost. A new (non-Starlink) space entrant, whose per-subscriber cost is multiples higher than the mature incumbent's, sits far further above the floor still.
  - Source: [comms_ground_vs_space_cost_ratio.md](../economics/comms_ground_vs_space_cost_ratio.md). The flavor-(a) finding is independently corroborated by 2025-26 BEAD procurement choosing satellite over fiber in the high-cost tail (fiber ~$100k/location rejected for satellite; Maine subsidizing Starlink for ~9,000 remote locations).

- **The marginal-cost floor is the decisive new finding, and it is the cost-side reason the served market is closed to space.** In a served market the competitor is not a fresh build paying full freight (the data-center shape); it is an entrenched incumbent whose plant is sunk and who defends at a cash floor far below both its all-in cost and its sticker price, with ~30-40 points of EBITDA headroom to absorb a defensive cut. A space entrant that is merely cheaper than the incumbent's *list* or *all-in* price has won nothing; it must beat the *marginal* floor, which it is 3-8x above. Source: [comms_incumbent_margins_competitive_floor.md](../economics/comms_incumbent_margins_competitive_floor.md).

- **The cost level a space operator needs to earn the addressable pool at a reasonable margin (~$480-680/sub/yr all-in, ~38% operating / ~63% EBITDA at a ~$790 ARPU) is not aspirational; it is Starlink's disclosed 2025 actual** at ~10.3M-subscriber scale. So the required cost structure is "already achieved at SpaceX scale", stronger than "aggressive but achievable." The binding qualifier is *scale*: the space cost stack is fixed-cost-dominated, so per-subscriber cost is denominator-driven, and the same cost level is unreachable for a small constellation. The winning space economics are a scale phenomenon, and the entity with the scale is the incumbent.

### Hypothesis 2 (space as a possible step change): confirm/break notes updated

Revision 2 left Hypothesis 2 at "direction and demand-scale supported; the open question narrows to supply economics and competitive share," and named as the break condition "the supply-side space economics not closing even against a ~$45-150B addressable pool." Wave 3 gives that condition its first cost-side test, and the result is conditional, not a clean pass or fail.

- **What the cost test now shows:** the space supply economics *do* close, decisively, in the unserved/remote fringe and the premium/sovereign layer, the exact territory the addressable-sizing track (Revision 2) already found the dollars in. There, space is 1.3-3.2x cheaper than a fresh ground build (tens-fold in the tail), and there is no incumbent marginal-cost floor to undercut it. **The cost ratio favors space in precisely the places the demand sits, and two independent lines of reasoning (revenue and cost) landing on the same map is the load-bearing convergence of wave 3.** This is the strongest cost-side support Hypothesis 2 has received.
- **But the cost test also sharpens the break condition into a concrete wall:** the space supply economics do NOT close in dense served markets, where the incumbent defends at a cash cost 3-8x below the space cost. So Hypothesis 2's framing is vindicated almost exactly as written ("its value is *not* in beating ground broadband on raw speed or price in served markets... it depends on the economics closing for the places ground cannot reach"). The cost side confirms both halves: space cannot win served-market cost competition, and it can win unserved-fringe cost competition.
- **What would now confirm it (revised):** evidence that a *specific entrant at a realistic (non-Starlink) constellation scale* can reach the ~$480-680/sub/yr cost level (or close enough at the premium end where ARPU is far higher), because the cost level that closes is currently demonstrated only at Starlink's tens-of-millions-of-subscribers scale; plus a real share of the fringe/premium pool against the incumbents who already operate there.
- **What would now break it (revised and sharpened):** (i) the entrant-specific cost stack at small scale staying multiples above the ~$480-680/sub/yr level even in the fringe (the denominator problem: a Rocket Lab-scale constellation may not reach the cost that closes), so the favorable *unserved* ratio is an incumbent-scale result the entrant cannot replicate; (ii) the fringe being mostly captured by the scaled incumbent (Starlink) already operating at the winning cost, so the open space is smaller than the cost ratio alone implies; or (iii) terrestrial reach (FWA, subsidized fiber) shrinking the unserved fringe where the favorable ratio lives. Note (i) is the new, load-bearing one: the cost ratio favors *space*, but it favors *scaled* space, and whether a new entrant gets there is the question the ratio cannot answer.

Net: Hypothesis 2 moves from "the open question narrows to supply economics and competitive share" to "the supply economics close for scaled space in the fringe (cost-confirmed) and do not close in served markets (cost-confirmed); the open question narrows again to whether a specific entrant at realistic scale can reach the cost level that closes, and to competitive share against the scaled incumbent." It is NOT confirmed; the gate has moved one more step downstream, from "do the economics close at all" to "do they close for *this* entrant at *its* scale."

### What Revision 3 deliberately does not do

- It does not render a verdict. The ratio is a cost-and-competitive base; the entrant-specific (non-Starlink) cost stack, the single-operator capture rate, and the per-segment margin remain open (now the top open questions).
- It does not change Hypothesis 1 (diminishing returns), Hypothesis 3 (laser weather-limited / fiber-adjacent), or Hypothesis 4 (security/sovereignty differentiator). Wave 3 is a cost-and-competitive analysis that bears on Hypothesis 2; the premium/sovereign cost-base note reinforces Hypothesis 4's "different axis" framing but adds no new demand evidence, so Hypothesis 4's Revision 2 notes stand.
- It does not pick a product. The cost ratio shows *where* space wins on cost (the fringe and premium/sovereign) and where it does not (dense served), which informs but does not make the product choice.
- It does not assume the entrant can reach incumbent-scale cost. The ~$480-680/sub/yr level that closes is Starlink's actual; that a Rocket Lab-scale constellation reaches it is exactly what is NOT assumed and is now the gate.

---

## Revision 4 (the model framework, the direct-to-cell reframe, the forward-comparison framing, and spectrum-as-moat)

*June 2026. Still a belief record. No verdict.*

Revisions 1 to 3 built the demand base, sized the addressable pools, and tested Hypothesis 2 on cost. Wave 4 assembles those pieces into a MODEL FRAMEWORK (the comms analogue of the data-center conclusion's method) and adds four new wave-4 source docs: the cellular generations / spectrum-availability doc ([spectrum_generations_and_availability.md](../direct_communication/spectrum_generations_and_availability.md)), the direct-to-cell market/physics/cannibalization doc ([comms_direct_to_cell.md](../economics/comms_direct_to_cell.md)), the 4G-to-5G transition-cost ("X") doc ([comms_4g_5g_transition_cost.md](../economics/comms_4g_5g_transition_cost.md)), the 6G demand-value doc ([comms_6g_demand_value.md](../economics/comms_6g_demand_value.md)), the Starlink V3 benchmark ([starlink_v3_specs.md](../competitors/starlink_v3_specs.md)), the Neutron comms-payload-fit doc ([neutron_comms_payload_fit.md](../rocket_lab/neutron/neutron_comms_payload_fit.md)), and the laser DC-interconnect side track ([laser_dc_interconnect_viability.md](../laser_comms/laser_dc_interconnect_viability.md)). The full framework is written up in [comms_framework_synthesis.md](../synthesis/comms_framework_synthesis.md). This revision records the four working hypotheses the framework crystallizes, and updates the confirm/break notes where wave-4 evidence bears. It does NOT render a verdict: the framework is a structure, not a populated model, and its load-bearing input (the entrant-specific cost per subscriber) is still open.

### The framework, as a working model shape (Hypothesis 5, new)

**The belief:** the communications model has the same spine as the data-center model: start from the **space cost per subscriber** (and per GB), apply a **1.5x revenue multiple** for an approximately **30% regular margin** (revenue minus the full per-subscriber cost, not gross profit), then compare **forward** against what ground must spend, with one structural twist the data-center track never faces. The output is not a single ratio but a **map**.

**What the base now suggests (the framework, [comms_framework_synthesis.md](../synthesis/comms_framework_synthesis.md)):**

- **The unit is cost per subscriber per year and per GB, and it is density-aware.** The defining structural fact, which bends the whole model: a satellite beam is Shannon-times-footprint gated and cannot densify, so **space cost-per-subscriber RISES with user density, the inverse of terrestrial** (which falls with density via cell-splitting). The model must carry the unit per-subscriber for low-consumption direct-to-cell and per-GB for high-consumption broadband, because the per-GB density penalty bites hardest there.
- **The chain forks on the forward comparison.** The data-center model compares forward against a fresh ground build (1.92x). Communications has two ground numbers: a **fresh build** (unserved, where space is cheaper by ~1.3-3.2x rural) and an **incumbent's marginal defense** (served, where space is ~3-8x costlier). So the founder's requested single mirror of 1.92x genuinely does not exist; the output is a map of where space wins the forward comparison (the unserved/remote fringe and premium/sovereign, no sunk-plant floor) and where it loses (dense served).
- **The 1.5x multiple is conservative against reality.** Starlink's disclosed 38.6% operating margin implies revenue at ~1.6x all-in delivery cost, so the 1.5x dial (a ~30% regular margin) is below the incumbent's actual, not above it.

**What would confirm it:** a populated model that places the entrant-specific cost per subscriber (Hypothesis 2's open gate) into the chain and reproduces the win/lose map against real per-segment ground next-upgrade costs.

**What would break it:** the framework shape proving wrong, e.g. a space architecture that escapes the density penalty (it cannot, per Shannon-times-footprint), or a revenue multiple that cannot hold a 30% regular margin at the entrant's cost (the denominator problem, Hypothesis 2).

### The forward-comparison framing (sharpens Hypothesis 2's cost test)

**The belief, stated sharply:** the right benchmark is not the incumbent's already-paid-for plant, nor its list price, but **what ground must spend on its NEXT upgrade cycle** (the 6G radio refresh), the cost the incumbent has not yet sunk. This is the only fair mirror of the data-center 1.92x (both sides not-yet-built), and it catches the incumbent at the moment of its forced spend.

**What the base now suggests:** the 4G-to-5G transition-cost doc establishes the *shape* of that next-cycle cost, "X": it was a new RADIO refresh on (mostly) existing sites (~$20-50k/site, ~55-65% of deployment capex), not new sites, not the core, not (in cash terms) spectrum ([comms_4g_5g_transition_cost.md](../economics/comms_4g_5g_transition_cost.md)). The 6G cycle (~2030-2035) will repeat this shape. So X-on-the-next-cycle is the per-POP/per-subscriber cost of the next radio refresh, plus any new 6G spectrum, possibly plus densification. The forward comparison's headline should be **space all-in per subscriber vs the incumbent's per-subscriber next-upgrade (6G) cost**, bounded by fresh-build (space wins, fringe) and marginal-defense (space loses, dense). This vindicates Revision 1's framing ("its value is not in beating ground on raw speed or price in served markets") and Revision 3's two-flavor fork, now expressed as a forward, not-yet-sunk comparison.

### The direct-to-cell reframe (sharpens the product question, OQ6)

**The belief:** direct-to-cell, not fixed broadband, is the LEAD market, and it is likely larger than home broadband (which it may cannibalize). Fixed broadband is the possibly-shrinking secondary; laser DC-interconnect is a separate side track.

**What the base now suggests ([comms_direct_to_cell.md](../economics/comms_direct_to_cell.md)):**

- **Direct-to-cell is the lead for three structural reasons:** it is the segment where space has a genuine non-substitutable product (reach an unmodified phone in a dead zone), it is where the capital is flowing (SpaceX's ~$17B EchoStar spectrum buy and a 15,000-satellite dedicated D2C fleet; AST's ~45 MHz Ligado deal), and it carries the optionality to grow into the home-broadband wallet. It is a high-volume, low-ARPU (~$10/month, often free-bundled, 50/50 MNO split), capacity-gated line, with delivery at ~$5-9/GB versus terrestrial ~$0.20-0.30/GB (~17-30x).
- **The cannibalization dynamic is real but EDGE-bounded.** D2C cannibalizes the home connection at the edge (rural/remote, single-occupant, light-usage, already-satellite-served), not the core (urban/suburban/indoor/heavy), and the boundary is set by beam-saturation physics, not consumer preference: D2C "will likely never work" indoors or in dense urban areas. A second-order cannibalization comes first: D2C may eat satellite fixed broadband (Starlink dishes) and standalone messaging before it touches terrestrial home broadband. So the "D2C is larger than home broadband" belief is a bet on capacity physics improving (the 6G-era per-GB gap narrowing), not a current fact: near-term D2C served revenue is ~$12-14B ex-China by 2030-31 (~10x below the ~$129B fixed-broadband-class slice), but the addressable base is ~5.5B devices.
- **Fixed broadband is the possibly-shrinking secondary:** diminishing-returns demand (Hypothesis 1), defended-and-shrinking-at-the-edge by D2C, with the Starlink V3 benchmark (~1 Tbps/sat, gigabit-to-a-user, Starship-bound) as its frontier yardstick. Laser DC-interconnect is modeled separately (per-link, not per-subscriber; terrestrial supplement, orbital primary), out of the RF consumer spine.

**What would confirm it:** a sustained (not peak) per-beam throughput that lets the phone credibly substitute for the home line beyond the edge, plus the D2C served-revenue forecasts being met. **What would break it:** sustained per-user throughput staying ~4G-class under realistic loading (so cannibalization stays edge-bound and the lead-market sizing stays ~10x below fixed), or the indoor/density wall proving permanent (it is physics, so likely).

### Spectrum-as-moat (sharpens Hypothesis 2's capacity input and the entry path)

**The belief (new, wave-4):** the binding entry constraint and the durable moat is SPECTRUM, and the realistic entrant accesses it by **partnering with a carrier (an FCC SCS lease)**, not by buying a cellular band. The capacity a beam delivers (and thus cost-per-subscriber) is set by how much spectrum the entrant can ride, and the players who matter are spending billions to control dedicated D2D spectrum precisely because the borrowed slice is too thin.

**What the base now suggests ([spectrum_generations_and_availability.md](../direct_communication/spectrum_generations_and_availability.md)):**

- **The generation and the band are orthogonal:** a satellite speaks whichever standard (4G/5G/6G) the partner's handsets expect over whatever band it leases. "5G" is a capability tier, never a frequency.
- **The realistic door is partner/lease (SCS), not buy:** AST rides AT&T/Verizon 850 MHz; Starlink D2C leases T-Mobile's PCS G-block. This gives instant handset compatibility and near-zero spectrum capex. Buying outright (SpaceX ~$17B EchoStar) is the hyperscale exception, not the entry path. So the model's spectrum input is "the commercial terms of an SCS partnership and the fraction of a carrier's band you ride," not "the cost of a cellular band."
- **More MHz is the capacity lever** (Starlink per-beam throughput scales near-linearly with bandwidth), which is why ~$17B and ~45 MHz changed hands. The moat is that a deep-pocketed incumbent can OWN dedicated spectrum to break the borrowed-slice ceiling, which a small entrant cannot.
- **The forward opening is FR3 / 7-15 GHz at WRC-27** (>400 MHz/operator), the one greenfield not yet filed, but it is upper mid-band (narrower beams, more path loss) and its reachability from orbit for direct-to-cell is unresolved.

**What would confirm it:** an entrant securing an SCS partnership on terms that deliver real capacity at a viable per-subscriber cost. **What would break it:** the SCS-leased slice being too thin to lift throughput past a coverage/messaging layer (so the entrant has no capacity moat), or dedicated D2D spectrum being affordable only at hyperscale (so the moat belongs to the incumbent, reinforcing Hypothesis 2's denominator problem).

### The catalyst recorded (reinforces the forward comparison)

The framework names a catalyst that makes the forward comparison favorable on the model's axis: **the forced 6G upgrade users will not pay a premium for.** Demand plateaus (~two-thirds of users balk above 5 euros/month even for a 10x speed jump; 5G delivered no ARPU premium; ARPU falling ~1.3-2%/yr), yet 6G capex is forced by traffic/parity physics ("you cannot avoid building it"), so the incumbent's per-subscriber economics deteriorate on the next cycle ([comms_6g_demand_value.md](../economics/comms_6g_demand_value.md)). The space alternative races a target whose own unit economics are worsening, and 6G unlocks no consumer premium a space entrant would have to match. This is a working hypothesis consistent with the founder's framing, not a verdict.

### What Revision 4 deliberately does not do

- It does not render a verdict. The framework is a structure; the entrant-specific cost per subscriber (Hypothesis 2's gate), the SCS commercial terms, the sustained per-beam rate, and the competitive share remain the top open questions.
- It does not change Hypothesis 3 (laser weather-limited / fiber-adjacent) on the consumer side; wave 4 adds the laser DC-interconnect side track as a separate, non-consumer line (per-link, orbital-primary), which is recorded in the framework but does not bear on the RF spine.
- It does not assume the entrant reaches incumbent-scale cost. The ~$480-680/sub/yr that closes is Starlink's actual; that a Rocket-Lab-scale constellation reaches it is exactly what is NOT assumed and remains the gate (Hypothesis 2, Revision 3).
- It does not pick a product. The reframe makes direct-to-cell the LEAD market and fixed broadband the secondary, but choosing what the comms track builds is still a later decision; the framework sizes and structures, it does not commit.

---

## Revision history

| Revision | Date | What it records | Verdict? |
|---|---|---|---|
| **Revision 1** | June 2026 | Initial working hypotheses (diminishing returns past baseline broadband; space as a possible step change whose value depends on economics and new use cases; laser high-bandwidth but weather-limited and possibly fiber-dependent; security as a differentiator) and the open questions that test them. Built on [comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md). | **No.** Belief record only. |
| **Revision 2** | June 2026 | Records that the two central missing dollar numbers are now sized (rural/remote fringe ~$40-55B to ~$95-130B/yr; premium/sovereign niche ~$60-95B/yr gross pool, ~$8-30B/yr open to a new entrant; consolidated de-duplicated new-entrant-addressable ~$45-60B to ~$110-150B/yr, ~3-9% of the cited $1.6T and in the same band as the ~$129B served estimate). Updates the confirm/break notes for Hypothesis 2 (space as a step change) and Hypothesis 4 (security/sovereignty differentiator). Built on [comms_rural_fringe_sizing.md](../economics/comms_rural_fringe_sizing.md), [comms_premium_sovereign_sizing.md](../economics/comms_premium_sovereign_sizing.md), [comms_addressable_sizing.md](../economics/comms_addressable_sizing.md). | **No.** Belief record only; the dollar sizes are demand-side and ILLUSTRATIVE, and the supply economics and competitive share remain unresolved. |
| **Revision 3** | June 2026 | Records the cost-side test of Hypothesis 2: the ground-vs-space delivery-cost ratio is two opposed numbers split by whether ground plant already exists. Flavor (a), space vs a fresh ground build (unserved): space is BELOW ground by ~1.3-3.2x rural (~65-90x in the extreme tail), the opposite direction to the data-center 1.92x. Flavor (b), space vs the incumbent's marginal cost (served): space is ABOVE the cash floor by ~3-8x. The marginal-cost floor is the new finding that closes the served market to space on cost. The cost level that earns the addressable pool at a reasonable margin (~$480-680/sub/yr all-in, ~38% op / ~63% EBITDA) is Starlink's disclosed actual, already achieved at SpaceX scale but unreachable for a small constellation (denominator-driven). Updates Hypothesis 2's confirm/break notes: supply economics close for *scaled* space in the fringe and do not close in served markets; the gate narrows to whether a specific entrant at realistic scale reaches the cost level that closes. Built on [comms_space_supply_cost.md](../economics/comms_space_supply_cost.md), [comms_incumbent_margins_competitive_floor.md](../economics/comms_incumbent_margins_competitive_floor.md), [comms_ground_vs_space_cost_ratio.md](../economics/comms_ground_vs_space_cost_ratio.md). | **No.** Belief record only; the ratio is a cost-and-competitive base, the entrant-specific (non-Starlink) cost stack and competitive share remain unresolved. |
| **Revision 4** | June 2026 | Assembles the pieces into a MODEL FRAMEWORK (the comms analogue of the data-center conclusion's method) and records four working hypotheses. (i) Framework (Hypothesis 5, new): space cost per subscriber x 1.5 revenue multiple for ~30% regular margin, compared FORWARD; the unit is density-aware (space cost-per-subscriber RISES with density, the inverse of terrestrial); the output is a MAP, not a single ratio (the forward comparison forks on whether ground plant exists, so the 1.92x mirror does not exist for comms). (ii) Forward-comparison framing: compare against ground's NEXT-upgrade cost (the 6G radio refresh, ~$20-50k/site, the X shape), not paid-off plant. (iii) Direct-to-cell reframe: D2C is the LEAD market (likely larger than home broadband, which it cannibalizes at the EDGE only, beam-physics-bounded); fixed broadband is the possibly-shrinking secondary; laser DC-interconnect is a separate side track. (iv) Spectrum-as-moat: the entry path is a carrier SCS lease, not buying a band; more MHz is the capacity lever; the moat (owned dedicated D2D spectrum) belongs to the deep-pocketed incumbent. Catalyst recorded: the forced 6G upgrade users will not pay a premium for. Built on [comms_framework_synthesis.md](../synthesis/comms_framework_synthesis.md), [spectrum_generations_and_availability.md](../direct_communication/spectrum_generations_and_availability.md), [comms_direct_to_cell.md](../economics/comms_direct_to_cell.md), [comms_4g_5g_transition_cost.md](../economics/comms_4g_5g_transition_cost.md), [comms_6g_demand_value.md](../economics/comms_6g_demand_value.md), [starlink_v3_specs.md](../competitors/starlink_v3_specs.md), [neutron_comms_payload_fit.md](../rocket_lab/neutron/neutron_comms_payload_fit.md), [laser_dc_interconnect_viability.md](../laser_comms/laser_dc_interconnect_viability.md). | **No.** Belief record only; the framework is a structure, not a populated model; the entrant-specific cost per subscriber, the SCS terms, the sustained per-beam rate, and competitive share remain open. |
