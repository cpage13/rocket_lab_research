# The Space-Addressable Communications Market, Sized: Fringe + Premium/Sovereign Against the $1.6T and $129B Anchors (ex-China)

*Research date: June 2026. Communications research-wiki effort, wave 2 (shared library).*

**Builds on / does not duplicate:** this is the wave-2 CONSOLIDATION doc. It does not run new market research. It takes the two now-sized dollar numbers the wave-1 base named as missing, sets them against the cited TAM and the realistic served estimate that wave 1 established, and produces one clean "what a NEW entrant could realistically address" figure. Every underlying derivation lives in the docs cited by path; this doc reconciles them, it does not re-derive them. The load-bearing inputs are:

- [research/economics/comms_rural_fringe_sizing.md](./comms_rural_fringe_sizing.md), which sized the satellite-addressable rural and remote fringe bottoms-up (conservative ~$40-55B/yr, optimistic ~$95-130B/yr, rural-and-remote-proper optimistic ceiling ~$75-100B/yr; all ILLUSTRATIVE).
- [research/economics/comms_premium_sovereign_sizing.md](./comms_premium_sovereign_sizing.md), which sized the premium/sovereign niche (total spend pool ~$75-95B/yr; served-addressable for a new commercial entrant ~$8-30B/yr; all ILLUSTRATIVE on the served range).
- [research/synthesis/comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md), the wave-1 base that set the ~$1.6T cited TAM, the ~$129B realistic served estimate, the ~90% haircut prior, the three structural discounts (density, ARPU-reality, shared-market), and the coverage-gap-vs-usage-gap distinction. Section 5 of that doc listed both missing numbers (items 4 and 6) that this consolidation now fills.
- [research/vision/comms_thesis.md](../vision/comms_thesis.md), the belief record, for the open questions this consolidation answers. (Its Revision 2, appended separately, records the same fill.)

> **Reading guide.** Every hard number is tagged **[FACT]** (reported / filed 2025-26 data), **[ESTIMATE]** (market-research sizing or arithmetic on sourced inputs), **[PROJECTION]** (forward forecast), or **[ILLUSTRATIVE]** (a sizing scenario built to show the shape, not to forecast a captured number). The consolidated "new-entrant-addressable" cases in Sections 3 and 4 are explicitly **[ILLUSTRATIVE]**: they are reconciliations of two sourced bottoms-up builds, not a forecast that any one operator captures them. China is **excluded** from every total and noted only as a labelled aside.

> **Scope.** This doc is ISOLATED TO COMMUNICATIONS and renders **NO verdict** on the Rocket Lab comms business. Its single job is to replace the wave-1 placeholders ("the dollar size of the rural fringe" and "the premium/sovereign niche size") with the two now-sized numbers, reconcile the overlap between them honestly, and place the result against the two reference anchors. The working hypotheses live in [comms_thesis.md](../vision/comms_thesis.md); this is a neutral sizing.

> **Claim-ID note for the lead.** The two wave-2 sizing docs each restarted their COMM- claim numbering at COMM-057, so their IDs collide with each other. To avoid adding a third collision, this consolidation uses a fresh range starting at **COMM-082** (above the highest ID used in either wave-2 doc). The lead reconciles all three wave-2 docs into the shared SOURCE_INDEX.

---

## Summary / Verdict

**Confidence: medium-high on the structural placement (where the dollars sit relative to the $1.6T and $129B anchors, and that the realistic new-entrant pool is a low-tens-of-billions niche); medium on the consolidated dollar band itself (it inherits the ILLUSTRATIVE status of both inputs and adds an overlap reconciliation that is reasoned, not modeled); high on the one finding that governs everything (the headline trillion is not the addressable market, and the two honestly-sized pools land two orders of magnitude below it).**

The two central missing dollar numbers the wave-1 thesis named are now sized. Stated as headlines:

- **The satellite-addressable rural and remote fringe (ex-China): ~$40-55B/yr conservative, ~$95-130B/yr optimistic** [ILLUSTRATIVE]. Bottoms-up on sourced household counts and region-specific ARPU. Source: [comms_rural_fringe_sizing.md](./comms_rural_fringe_sizing.md).
- **The premium/sovereign niche (ex-China): a ~$75-95B/yr total spend pool, of which ~$8-30B/yr is realistically OPEN to a new commercial entrant** after closed national programs (IRIS2, SDA/SDN primes, GOVSATCOM) are removed [ILLUSTRATIVE on the served range]. Source: [comms_premium_sovereign_sizing.md](./comms_premium_sovereign_sizing.md).

**These two pools cannot be naively summed: they overlap.** The high-value mobility and enterprise verticals (maritime, aviation, energy, remote-government) sit in BOTH the rural-fringe build (its Tier B) and the premium-niche build (its premium-enterprise block). Section 3 removes that double-count. After reconciliation, the honest consolidated figure for **what a new entrant could realistically address across the whole space-communications opportunity, ex-China**, is:

| Consolidated new-entrant-addressable space-comms pool (ex-China) | Value | Status |
|---|---|---|
| **Conservative** | **~$45 to $60B/yr** | [ILLUSTRATIVE] |
| **Optimistic** | **~$110 to $150B/yr** | [ILLUSTRATIVE] |

**How that compares to the two anchors the thesis named:**

| Anchor | Value | Consolidated addressable as a share |
|---|---|---|
| **SpaceX cited connectivity TAM** | **~$1.6T** | **~3% (conservative) to ~9% (optimistic)** |
| **Morningstar realistic served estimate** | **~$129B** | **~35-45% (conservative) to roughly at-or-modestly-above it (optimistic)** |

The result is internally consistent in the way that matters: a bottoms-up consolidation of the two honestly-sized pools lands in the **same low-tens-to-low-hundreds-of-billions band** as Morningstar's independent top-down rebuild (~$129B), and roughly **two orders of magnitude below** the cited $1.6T. The optimistic case converging on (and at its top edge slightly exceeding) ~$129B is expected, because the consolidated pool adds the premium/sovereign government layer that Morningstar's broad-LEO consumer/enterprise rebuild only partly counts; the conservative case sitting at ~35-45% of $129B is the rural-and-mobility core plus the open government slice, without the full carrier add-on and without deep emerging-market penetration.

**The three structural points that survive the consolidation (and dominate it):**

1. **The dollars are in the developed-world rural fringe, the mobility/enterprise verticals, and the open government layer, NOT in the billions of unconnected people.** The ~3.1B usage-gap population is an income problem satellite supply does not fix; it adds headcount, not revenue. This is the single asymmetry both sizing docs were built to respect, and it is what keeps the honest number two orders of magnitude under the headline. [FACT on the gap split; ILLUSTRATIVE on the dollar consequence.]
2. **A large majority of the most-cited sovereign spend is CLOSED to a new commercial entrant.** The programs that prove the sovereignty demand (IRIS2 at EUR 10.6B, the SDA tranches, the $2.29B SpaceX SDN award, GOVSATCOM) are captured prime/consortium builds. Only the commercial-augmentation layer (~$3-8B/yr open) is contestable. The open premium/sovereign slice is therefore a fraction of the ~$75-95B gross pool. [FACT on the closed programs; ESTIMATE on the open slice.]
3. **The whole consolidated pool is split across many operators, and the early ramp is capacity-gated, not demand-gated.** The ~$45-150B is the contestable pie across Starlink/Starshield, Eutelsat/OneWeb, SES, Viasat, Amazon Leo, Kepler, and any new entrant combined. No single operator captures it. And a sliver-constrained entrant's first-years capture is bounded by how much capacity it can physically field (the supply side), far below even the conservative figure. [ESTIMATE.]

**The honest one-line read (no verdict):** sized honestly and de-duplicated, the realistically space-addressable communications opportunity a new entrant could compete for is roughly **$45-60B/yr (conservative) to $110-150B/yr (optimistic), ex-China**: about **3-9% of the cited $1.6T**, and **in the same band as the independent ~$129B served estimate**. It is a real, durable, high-margin-at-the-premium-end market, and it is a niche of a niche of the trillion-dollar headline. Whether the space *supply* economics close in that pool, and what share a specific entrant wins, are separate questions this doc does not answer.

---

## 1. The Two Now-Sized Pools, Side by Side

The wave-1 base ([comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md) Section 5, items 4 and 6) named two missing dollar numbers. Both are now sized. This table is the consolidation's starting point; the figures are carried from the two source docs, not re-derived.

| Pool (ex-China) | Conservative | Optimistic | What it is | Status | Source |
|---|---|---|---|---|---|
| **A. Rural / remote fringe** | **~$40-55B/yr** | **~$95-130B/yr** | The coverage gap plus underserved-but-payable rural, at region-specific ARPU: developed-world rural fringe (high ARPU, small count) + mobility/enterprise verticals + a thin paying slice of emerging-market rural | [ILLUSTRATIVE] | [comms_rural_fringe_sizing.md](./comms_rural_fringe_sizing.md) S4-5 |
| **B. Premium / sovereign niche (total pool)** | **~$75-95B/yr** | (same; this is the gross ceiling) | Government + military satcom envelope + premium enterprise verticals + finance/low-latency + orbital-DC backhaul, OPEN and CLOSED combined | [ESTIMATE] | [comms_premium_sovereign_sizing.md](./comms_premium_sovereign_sizing.md) S4.1 |
| **B-open. Premium / sovereign, contestable** | **~$8B/yr** | **~$30B/yr** | Pool B after removing closed national programs (IRIS2, SDA/SDN primes, GOVSATCOM) and applying a served haircut: the slice OPEN to a new commercial entrant | [ILLUSTRATIVE] | [comms_premium_sovereign_sizing.md](./comms_premium_sovereign_sizing.md) S4.2 |

Two things to read off this table before consolidating:

- **For pool B, the right number to carry forward is B-open (~$8-30B/yr), not the gross ~$75-95B.** A new commercial-services entrant cannot win the closed flagship programs; counting them as addressable would repeat exactly the error the base warns against. The gross pool is the demand proof; the open slice is the addressable revenue. (The closed-prime channel is a different business; Rocket Lab's own >$1.3B in SDA prime awards sits there, recorded for context in the source doc, not scored here.)
- **Pool A already contains the mobility/enterprise verticals.** The rural-fringe build's Tier B (maritime ~$34k/yr/vessel, aviation ~$300k/yr/aircraft, energy/mining/remote-government) is ~$20-28B (conservative) to ~$30-40B (optimistic) of pool A. Those same verticals are a large part of pool B-open's premium-enterprise component. This is the overlap Section 3 must remove.

---

## 2. The Overlap: Why You Cannot Add A and B-open Directly

The two sizing docs were scoped to answer two different questions ("how big is the rural/remote fringe" and "how big is the premium/sovereign niche"), and the high-value mobility and enterprise verticals legitimately belong to both framings. So they appear in both builds. Summing the two pools without removing the shared verticals would double-count them.

The market data confirms the overlap is real and material. The largest LEO operator's own segment mix shows enterprise, maritime, and aviation as distinct high-margin lines sitting alongside the consumer residential base ([Value Add VC segment build](https://valueaddvc.com/blog/starlink-revenue-2025-2026-subscriber-count-arpu-and-the-path-to-profitability); maritime ~$1.94B and enterprise ~$1.68B run-rate into 2026, per the same source as carried in the rural-fringe doc; [Skift on the enterprise/travel grip](https://skift.com/2026/05/26/11-4-billion-and-zero-churn-what-spacex-said-about-starlinks-travel-industry-grip/)). These are exactly the verticals that show up as "Tier B" in the rural-fringe build and as "premium enterprise" in the premium-niche build.

| Vertical | Where it appears in pool A | Where it appears in pool B-open | Consolidation rule |
|---|---|---|---|
| Maritime | Tier B (~$34k/yr/vessel) | Premium enterprise (maritime ~$4.5-7B segment) | Count ONCE |
| Aviation / IFC | Tier B (~$300k/yr/aircraft) | Premium enterprise (aero IFC ~$6B segment) | Count ONCE |
| Energy / mining / oil & gas remote sites | Tier B (Niche non-broadband) | Premium enterprise (critical-infrastructure) | Count ONCE |
| Remote government / defense field sites | Tier B (Niche non-broadband) | Government commercial-augmentation layer | Count ONCE (assign to the government layer) |
| Developed-world rural residential | Tier A | not in pool B | A only |
| Emerging-market rural residential | Tier C | not in pool B | A only |
| Carrier direct-to-cell add-on | Tier D (optimistic only) | not in pool B | A only |
| Closed sovereign constellations (IRIS2, SDA/SDN, GOVSATCOM) | not in pool A | EXCLUDED from B-open | neither (closed) |
| Finance / low-latency, orbital-DC backhaul | not in pool A | premium add-ons in B-open | B only |

**The clean decomposition.** To avoid double-counting, the consolidation treats the space-addressable opportunity as four NON-overlapping buckets:

1. **Developed-world rural/remote residential** (pool A Tier A only). Conservative ~$13-20B; optimistic ~$25-35B.
2. **Emerging-market rural residential, genuinely paying** (pool A Tier C only). Conservative ~$5-8B; optimistic ~$15-25B.
3. **Mobility + enterprise + remote-government verticals** (the SHARED block, counted once). This is pool A Tier B, which already captures the same maritime/aero/energy/remote-gov demand that pool B-open's premium-enterprise component describes. Conservative ~$20-28B; optimistic ~$30-40B.
4. **Premium/sovereign-specific additions NOT in pool A** (the open government commercial-augmentation layer beyond remote-gov field sites, finance/low-latency, orbital-DC backhaul, and the security/sovereignty premium uplift on managed service). Conservative ~$5-10B; optimistic ~$15-30B.
5. **(Optimistic only) Carrier direct-to-cell add-on layer** (pool A Tier D). Optimistic ~$20-30B. Held out of the conservative case and flagged: it is a bolt-on across the general mobile base, not rural-fringe broadband.

Bucket 3 is the reconciliation: it is counted once, using the rural-fringe doc's Tier B sizing, because that build already values the same physical demand (the vessels, aircraft, and remote sites) that the premium-niche doc's enterprise block values. Bucket 4 is what the premium/sovereign doc adds beyond pool A: principally the open *government* commercial-augmentation layer (which the rural-fringe build does not size) plus the small finance and orbital-DC-backhaul add-ons.

---

## 3. The Consolidated New-Entrant-Addressable Figure [ILLUSTRATIVE]

Summing the five non-overlapping buckets from Section 2.

| Bucket (ex-China) | Conservative | Optimistic | Status |
|---|---|---|---|
| 1. Developed-world rural/remote residential | ~$13-20B | ~$25-35B | [ILLUSTRATIVE] |
| 2. Emerging-market rural residential (paying) | ~$5-8B | ~$15-25B | [ILLUSTRATIVE] |
| 3. Mobility + enterprise + remote-gov verticals (shared, counted once) | ~$20-28B | ~$30-40B | [ILLUSTRATIVE] |
| 4. Premium/sovereign-specific additions (open gov layer, finance, orbital-DC backhaul) | ~$5-10B | ~$15-30B | [ILLUSTRATIVE] |
| 5. Carrier direct-to-cell add-on (optimistic only) | not counted | ~$20-30B | [ILLUSTRATIVE] |
| **Consolidated new-entrant-addressable pool** | **~$45-60B/yr** | **~$110-150B/yr** | **[ILLUSTRATIVE]** |

**How to read the consolidated number.**

- **Conservative ~$45-60B/yr** is what a satellite business could address if it wins much of the developed-world rural fringe, owns the high-value mobility/enterprise verticals, gets a thin but real foothold in emerging-market rural, and captures the open (non-closed) government commercial-augmentation layer. It deliberately excludes the carrier direct-to-cell add-on and the closed sovereign programs.
- **Optimistic ~$110-150B/yr** loosens every assumption in the plausible direction: deeper developed-fringe penetration, fuller mobility/enterprise capture, a price-driven expansion of emerging-market rural, a meaningful slice of the carrier direct-to-cell add-on, and a larger open government layer as allied sovereignty programs increasingly buy managed commercial service rather than build.
- The consolidated band is slightly above the simple sum of pool A and pool B-open's headline endpoints, because bucket 4 adds the open *government* layer that pool A never counted, while bucket 3 prevents the mobility double-count that a naive A + B-open sum would have introduced. The two adjustments partly offset; the net is a band that is honest about both the addition (government) and the subtraction (overlap).

**Three reasons the captured number is smaller than this addressable pool** (all carried from the source docs, none of which this consolidation relaxes):

1. **Shared market.** The ~$45-150B is contestable across all operators combined. A specific entrant wins a share, per the base's shared-market discount.
2. **Capacity gate.** A sliver-constrained entrant carries only ~0.2-3 Gbps/beam from a ~100-250 MHz RF slice (optical backbone lifts this 10-100x per link, but the ground segment gates the ramp; industry-wide only ~10% of needed optical ground infrastructure exists). Early-years capture is supply-limited, far below even the conservative figure. Source: [comms_premium_sovereign_sizing.md](./comms_premium_sovereign_sizing.md) S4.2, [comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md) S3.
3. **Supply economics not assumed.** This is a demand-side addressable pool. Whether the space cost stack (constellation capex, optical ground network, launch cadence) closes against these revenues is a separate workstream, explicitly not assumed here.

---

## 4. Placement Against the Two Anchors (the question the thesis asked)

The wave-1 thesis asked for the two missing numbers set against the cited TAM and the realistic served estimate. This is that placement.

| Reference (ex-China) | Value | Status | Source |
|---|---|---|---|
| **SpaceX cited connectivity TAM** | **~$1.6T** ($870B broadband + $740B mobile) | [FACT as claimed] | [comms_space_tam_claims.md / Morningstar](https://www.morningstar.com/business/insights/blog/starlink-market-opportunity), via base |
| **Morningstar realistic served estimate** (mature broad LEO) | **~$129B** (~$84B Niche + ~$45B Add-on; ~$43B US x3 global) | [PROJECTION] | [Morningstar PDF](https://d1e00ek4ebabms.cloudfront.net/production/uploaded-files/Our_Realistic_Starlink_Market_Sizing-915d25bb-5968-4e1f-ae0b-ad5999a9aa87.pdf), via base |
| **Rural / remote fringe (this consolidation's pool A)** | ~$40-55B to ~$95-130B/yr | [ILLUSTRATIVE] | [comms_rural_fringe_sizing.md](./comms_rural_fringe_sizing.md) |
| **Premium / sovereign open slice (pool B-open)** | ~$8-30B/yr | [ILLUSTRATIVE] | [comms_premium_sovereign_sizing.md](./comms_premium_sovereign_sizing.md) |
| **Consolidated new-entrant-addressable (de-duplicated)** | **~$45-60B to ~$110-150B/yr** | **[ILLUSTRATIVE]** | this doc, Section 3 |

| Consolidated case | vs ~$1.6T cited TAM | vs ~$129B realistic served |
|---|---|---|
| **Conservative (~$45-60B)** | **~3%** | **~35-45%** |
| **Optimistic (~$110-150B)** | **~7-9%** | **roughly at it to ~15% above it** |

**What the placement says.**

- **Against the $1.6T headline: ~3-9%.** The consolidated addressable pool is two orders of magnitude below the cited TAM, exactly consistent with the base's ~90% haircut prior (served ~5-10% of cited). The conservative case sits a touch below even that band, because the rural-and-government core excludes the full carrier add-on and most of the dense-urban wallet the headline includes. This is the density discount and the shared-market discount made concrete.
- **Against the ~$129B realistic served: in the same band.** This is the load-bearing convergence. A bottoms-up consolidation of two independently-built pools (rural fringe + premium/sovereign), de-duplicated, lands in the same low-hundreds-of-billions band that Morningstar reached top-down from SpaceX's own $1.6T. The optimistic case converging on (and at its top edge slightly exceeding) ~$129B is expected: the consolidated pool adds the premium/sovereign *government* layer that Morningstar's broad-LEO consumer/enterprise rebuild only partially captures, so a modest overshoot at the optimistic end is the government layer showing up, not an inconsistency. Two methods that do not share an approach landing in the same band is the reason to believe the band.
- **The premium/sovereign open slice alone (~$8-30B) is ~6-23% of ~$129B and ~0.5-2% of $1.6T.** It is the smallest, highest-margin, hardest-to-win piece. Its case rests on margin and durability, not size (Section 5 of the premium-niche doc).

**One caution on the optimistic ceiling.** The optimistic ~$110-150B leans on three things that are plausible but not assured: a price-driven expansion of emerging-market rural (which compresses ARPU as it adds subscribers, the exact dynamic that pulled Starlink's blended ARPU down 33% in two years), a meaningful carrier direct-to-cell add-on (a bolt-on across the general mobile base, definitionally not rural-fringe broadband), and allied governments buying managed commercial service rather than building sovereign systems. Strip the direct-to-cell add-on (bucket 5) out, and the rural-plus-premium-proper optimistic ceiling is ~$90-120B. The honest center of gravity is the conservative-to-mid band; the top end requires several favorable trends at once.

---

## 5. What This Consolidation Settles, and What It Explicitly Does Not

**Settled (the two missing numbers are now filled):**

- The satellite-addressable rural/remote fringe is sized: ~$40-55B/yr conservative, ~$95-130B/yr optimistic [ILLUSTRATIVE].
- The premium/sovereign niche is sized: ~$75-95B/yr gross pool, ~$8-30B/yr open to a new entrant [ILLUSTRATIVE].
- The consolidated, de-duplicated new-entrant-addressable pool is ~$45-60B/yr (conservative) to ~$110-150B/yr (optimistic) [ILLUSTRATIVE], which is ~3-9% of the cited $1.6T and in the same band as the ~$129B realistic served estimate.
- The structural shape is settled and robust: the dollars are in the developed-world fringe, the mobility/enterprise verticals, and the open government layer; the billions of unconnected people are headcount, not revenue; the closed sovereign programs are demand proof, not addressable revenue; the pool is shared across operators and the early ramp is capacity-gated.

**Explicitly NOT settled (and out of scope for this doc):**

- **No verdict on the Rocket Lab comms business.** This is a neutral sizing of the market, not a judgment on whether to build into it.
- **No single-operator capture rate.** The consolidated figure is the all-operators contestable pie. What share a specific new entrant wins (against Starlink/Starshield, Eutelsat/OneWeb, SES, Viasat, Amazon Leo, Kepler) is a competitive-share question neither sizing doc answers.
- **No supply-side economics.** Whether the constellation capex, optical ground network, and launch cadence close against these revenues is a separate workstream, not assumed here.
- **No margin-to-a-number.** The premium niche's structurally better margin profile is established directionally in the source doc; converting it to a modeled gross/operating margin per segment net of capex is a later step.

---

## Sources

*Anchors and segment mix (verified for this consolidation)*
- [Morningstar, Our Realistic Starlink Market Sizing (~$129B; ~$84B Niche + ~$45B Add-on; ~$43B US x3 global)](https://d1e00ek4ebabms.cloudfront.net/production/uploaded-files/Our_Realistic_Starlink_Market_Sizing-915d25bb-5968-4e1f-ae0b-ad5999a9aa87.pdf)
- [Morningstar, Starlink market opportunity blog](https://www.morningstar.com/business/insights/blog/starlink-market-opportunity)
- [Value Add VC, Starlink revenue/subscriber/ARPU and segment mix (maritime ~$1.94B, enterprise ~$1.68B run-rate into 2026)](https://valueaddvc.com/blog/starlink-revenue-2025-2026-subscriber-count-arpu-and-the-path-to-profitability)
- [Skift, $11.4B and zero churn: Starlink's enterprise and travel grip](https://skift.com/2026/05/26/11-4-billion-and-zero-churn-what-spacex-said-about-starlinks-travel-industry-grip/)

*Library docs this consolidation reconciles (each carries the underlying 2+ source citations inline)*
- [comms_rural_fringe_sizing.md](./comms_rural_fringe_sizing.md) (pool A: rural/remote fringe)
- [comms_premium_sovereign_sizing.md](./comms_premium_sovereign_sizing.md) (pool B: premium/sovereign niche)
- [comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md) (the $1.6T and $129B anchors, the 90% haircut, the three discounts, the gap split)
- [comms_thesis.md](../vision/comms_thesis.md) (the belief record and open questions this fills)

---

## Confidence

- **The two input pools (Section 1): inherited.** Pool A is medium and ILLUSTRATIVE (bottoms-up arithmetic on sourced household counts and ARPUs); pool B-open is low-by-design and ILLUSTRATIVE (a reasoned haircut on sourced total-spend pools). This consolidation does not strengthen or weaken them; it carries their status forward.
- **The overlap reconciliation (Section 2): medium-high.** That maritime, aviation, energy, and remote-government appear in both builds is verifiable from the segment data and from reading the two docs; the rule to count them once is sound. The exact dollar attribution of the shared block (assigned to pool A's Tier B sizing) is reasoned, not modeled, so the band rather than any point is the result.
- **The consolidated band (Section 3): medium.** It is a reconciliation of two ILLUSTRATIVE pools with an explicit de-duplication. The structure (five non-overlapping buckets) is honest; the endpoints inherit the uncertainty of both inputs.
- **The placement against the anchors (Section 4): high on the structural finding, medium on the exact percentages.** That the consolidated pool is two orders of magnitude below $1.6T and in the same band as ~$129B is robust and is the load-bearing result. The precise share percentages move with the band endpoints.

---

## Open Questions

These are the consolidation-level open questions; the input-level ones live in the two source docs, and the thesis-level ones in [comms_thesis.md](../vision/comms_thesis.md).

1. **The exact dollar attribution of the shared mobility/enterprise block.** Section 2 counts it once using pool A's Tier B sizing. A reconciled bottoms-up build of maritime + aviation + energy + remote-gov from the segment market data (rather than from two separately-scoped docs) would tighten bucket 3, which is the largest single bucket in the conservative case.
2. **How much of the open government layer (bucket 4) is incremental to pool A's remote-gov sites.** Some remote-government field demand is in pool A's Tier B already; the open commercial-augmentation layer (the pLEO IDIQ, allied managed-service buys) is partly additional and partly the same sites bought through a different channel. The split is reasoned here, not sourced.
3. **Single-operator capture rate.** The consolidated figure is the all-operators pie. The gap between this addressable pool and a specific entrant's revenue is the competitive-share question neither input doc answers.
4. **The capacity-vs-demand binding constraint over time.** Both inputs note the early ramp is supply-gated. At what constellation scale demand becomes the binding constraint (and the addressable pool, not the capacity, sets revenue) is unresolved and interacts directly with the space-side cost workstream.
5. **Whether direct-to-cell belongs in a "space-comms addressable" number at all.** Bucket 5 (~$20-30B optimistic) is a carrier add-on across the general mobile base, not rural-fringe or premium/sovereign service. Whether to count it is a definitional call; stripping it gives a rural-plus-premium-proper optimistic ceiling of ~$90-120B.

---

## Claims (COMM- namespace; starts at COMM-082 to avoid colliding with both wave-2 sizing docs)

Each consolidated figure traces to the two wave-2 sizing docs (which carry the underlying 2+ source citations inline) plus the anchors verified directly for this doc. The lead reconciles all three wave-2 docs into SOURCE_INDEX.

| COMM- id | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-082 | Satellite-addressable rural/remote fringe (pool A), consolidated headline | ~$40-55B/yr conservative; ~$95-130B/yr optimistic | [ILLUSTRATIVE] | [comms_rural_fringe_sizing.md](./comms_rural_fringe_sizing.md) |
| COMM-083 | Premium/sovereign niche total spend pool (pool B, open + closed) | ~$75-95B/yr | [ESTIMATE] | [comms_premium_sovereign_sizing.md](./comms_premium_sovereign_sizing.md) |
| COMM-084 | Premium/sovereign slice OPEN to a new commercial entrant (pool B-open) | ~$8-30B/yr | [ILLUSTRATIVE] | [comms_premium_sovereign_sizing.md](./comms_premium_sovereign_sizing.md) |
| COMM-085 | Consolidated new-entrant-addressable space-comms pool (de-duplicated, ex-China) | ~$45-60B/yr conservative; ~$110-150B/yr optimistic | [ILLUSTRATIVE] | this doc, Section 3 |
| COMM-086 | Consolidated addressable as a share of cited ~$1.6T connectivity TAM | ~3% (conservative) to ~9% (optimistic) | [ESTIMATE] | this doc vs [comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md) |
| COMM-087 | Consolidated addressable as a share of ~$129B realistic served estimate | ~35-45% (conservative) to roughly at-or-slightly-above it (optimistic) | [ESTIMATE] | this doc vs [comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md) |
| COMM-088 | Mobility/enterprise verticals overlap between pools A and B (counted once) | maritime + aviation + energy + remote-gov appear in both builds | [FACT] (overlap) | [comms_rural_fringe_sizing.md](./comms_rural_fringe_sizing.md), [comms_premium_sovereign_sizing.md](./comms_premium_sovereign_sizing.md), [Value Add VC](https://valueaddvc.com/blog/starlink-revenue-2025-2026-subscriber-count-arpu-and-the-path-to-profitability) |
| COMM-089 | Rural-plus-premium-proper optimistic ceiling (excl. carrier direct-to-cell add-on, bucket 5) | ~$90-120B/yr | [ILLUSTRATIVE] | this doc, Sections 3-4 |
| COMM-090 | Closed sovereign programs excluded from the addressable figure (demand proof only) | IRIS2 EUR 10.6B; SDA tranches; SpaceX SDN $2.29B; GOVSATCOM | [FACT] | [comms_premium_sovereign_sizing.md](./comms_premium_sovereign_sizing.md) S1.2 |
