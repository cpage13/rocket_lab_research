# The Ground-vs-Space Cost to Deliver Communications: The Ratio, the Realistic SpaceX Cost, and the Competitive Verdict

*Research date: June 2026. Communications research-wiki effort, wave 3 (shared library).*

**Builds on / does not duplicate:** this is the wave-3 CONSOLIDATION doc. It does not run a new cost build; it takes the space-side stack and the ground-side stacks that the wave-1 and wave-3 base docs already established, puts them on a common basis, and produces the headline ground-vs-space delivery-cost ratio the founder asked for (the comms mirror of the data-center track's orbit-to-ground 1.92x). The load-bearing inputs, each cited by path:

- [research/economics/comms_space_supply_cost.md](./comms_space_supply_cost.md) (the SPACE numerator: mature-incumbent all-in delivery ~$480-680/subscriber/yr, space-specific replacement ~$200-260/sub/yr, network-average ~$0.05-0.30/GB rising at density, the 5-year replacement treadmill, scale-is-the-whole-game).
- [research/economics/comms_incumbent_margins_competitive_floor.md](./comms_incumbent_margins_competitive_floor.md) (the GROUND MARGINAL floor: incumbent defend-cost ~10-20% of ARPU for fixed broadband, ~$0.50-1.50/GB for mobile, ~30-40 points of EBITDA headroom, the sunk-plant asymmetry).
- [research/economics/comms_broadband_deployment_economics.md](./comms_broadband_deployment_economics.md) (the GROUND BUILD: fiber ~$700-1,500 urban / $3,000-6,000 rural / up to ~$200,000+ extreme tail per passing, +$500-700 connect, cable upgrade ~$100-300, FWA ~$300-800/sub, ~46% take-rate).
- [research/economics/comms_cellular_5g_deployment_economics.md](./comms_cellular_5g_deployment_economics.md) (the GROUND BUILD, mobile: capex intensity ~14-19% of service revenue, ~$20-50k upgrade / ~$100-300k new macro site, GSMA ~EUR35/connection/yr).
- [research/economics/comms_addressable_sizing.md](./comms_addressable_sizing.md) (the revenue target: ~$45-60B/yr conservative to ~$110-150B/yr optimistic new-entrant-addressable pool, ex-China).

> **Reading guide.** Each hard number is tagged **[FACT]** (reported / filed 2025-26 data), **[ESTIMATE]** (third-party sizing or our own arithmetic on sourced inputs), **[DERIVED]** (computed in this doc from cited inputs), **[PROJECTION]** (forward forecast), or **[ILLUSTRATIVE]** (a figure built to show the shape, not to forecast a captured number). Hard numbers are cross-checked against 2+ independent sources where possible; single-source figures are flagged inline. China is **excluded** and noted only as a labelled aside.

> **Scope.** This is a NEUTRAL supply-side base doc for the shared library. It renders **NO verdict** on the Rocket Lab comms business. It establishes the cost-and-competitive base: the ground-vs-space ratio, what cost level a space operator needs to earn the addressable revenue, and where on the map space can and cannot win on cost. Whether Rocket Lab specifically can field that cost stack is the thesis's job, not this doc's.

---

## Summary / Verdict

**Confidence: medium-high on the asymmetry that is the headline insight (space beats a fresh ground build in the unserved fringe and loses badly to an incumbent's marginal cost in served markets); medium on the point ratios (they are arithmetic on sourced ranges, and the ground-build side is annualized with an assumed asset life and capital charge that are stated and defensible but not the only reasonable choices).**

The founder asked for one headline ratio, mirroring the data-center track's orbit-to-ground 1.92x. The honest answer is that **communications has not one ratio but two, and they point in opposite directions**, because the ground "cost to deliver" is two completely different numbers depending on whether the ground side has already been built. That split is the entire story.

**The headline, both flavors (per subscriber per year, mature SpaceX-scale space cost):**

| Flavor | What it compares | Conservative | Aggressive | Which side is cheaper |
|---|---|---|---|---|
| **(a) Space vs a FRESH GROUND BUILD** (the unserved-area comparison, the true mirror of the data-center 1.92x) | Space all-in vs annualized cost of a new rural fiber build | ground ~$875/yr vs space ~$680 = **ground 1.3x space** | ground ~$1,540/yr vs space ~$480 = **ground 3.2x space** | **SPACE is BELOW ground** (space wins by ~1.3x to ~3.2x; in the extreme tail, where ground runs ~$44,000/sub/yr, space wins by ~50-90x) |
| **(b) Space vs the INCUMBENT'S MARGINAL COST** (the served-area comparison, the comms-specific case the data-center track never faces) | Space all-in vs the incumbent's cash cost to defend an already-connected sub | space ~$480 vs ground-marginal ~$180/yr = **space 2.7x ground** | space ~$680 vs ground-marginal ~$84/yr = **space 8.1x ground** | **SPACE is ABOVE ground** (space loses by ~3x to ~8x; a new space entrant, multiples costlier than the mature incumbent, loses by far more) |

[DERIVED, from the cited docs. Flavor (a) annualizes the rural-fiber passing-plus-connect cost over a ~25-year asset life at a ~9% capital charge and adds ground opex; flavor (b) uses the incumbent's sourced marginal-cost floor directly. Both stated as ranges, not point estimates.]

**Per GB, the same split holds and is even starker:**

| Flavor | Space cost per GB | Ground cost per GB | Read |
|---|---|---|---|
| **(a) vs fresh build** | ~$0.05-0.30/GB network-average | <$0.01/GB once plant exists (but the build cost is per-PASSING, not per-GB) | per-GB is the wrong axis for a greenfield build; the build cost lives in the per-passing capex, which is where space wins |
| **(b) vs incumbent marginal** | ~$0.05-0.30/GB network-average, **rising sharply at user density** | fixed <$0.01/GB; mobile ~$0.50-1.50/GB | vs fixed, space is **5-30x+ above**; vs mobile, space network-average is in-range, but space cost rises with density exactly where served markets are dense |

[DERIVED/ESTIMATE.] The per-GB axis exposes the structural ceiling the space doc named: **a space beam's cost-per-user rises with density, the opposite of terrestrial fiber, so the per-GB comparison gets worse for space precisely in the dense markets where served competition happens.**

**The realistic-for-SpaceX answer (Question 2):** the cost level a space operator needs to earn the ~$45-150B addressable pool at a reasonable margin is **~$480-680/subscriber/yr all-in** (space-specific replacement portion ~$200-260/sub/yr), which clears a ~38% operating / ~63% EBITDA margin at a ~$790 ARPU. That is **not an aggressive target that SpaceX might reach: it is Starlink's disclosed 2025 actual** ($11.4B revenue, 38.6% segment operating margin, ~63% segment EBITDA margin, ~10.3M subscribers) [FACT, SpaceX S-1]. So the cost structure is not "aggressive but achievable at SpaceX scale", it is **already achieved at SpaceX scale**. The binding word is *scale*: the same cost level is unreachable for a small constellation, because the space cost stack is fixed-cost-dominated and per-subscriber cost is driven by the denominator. It is achievable for SpaceX specifically, and not for a generic small new entrant.

**The competitive verdict (Question 3, cost-base level, NO business verdict):** the headline insight is an **asymmetry**, not a single number.

> **Space wins on cost where there is no incumbent marginal-cost floor (the unserved/remote fringe and the premium/sovereign layer), and loses on cost where there is one (dense served markets, where the incumbent defends at a cash cost far below its sticker price).** The ground-vs-space ratio flips from "space cheaper by 1.3-3.2x" against a fresh rural build to "space costlier by 3-8x" against an incumbent's marginal defense, and which ratio applies is decided entirely by whether the ground plant already exists at that location.

This is the same conclusion the addressable-sizing track reached from the demand side (the dollars sit in the fringe, the verticals, and the open government layer), now confirmed independently from the cost side: **the space-addressable dollars sit exactly where the cost ratio favors space, and the cost ratio favors space exactly where the incumbent has no sunk plant.** The two halves lock together.

**Single-source / soft figures the lead should note** (flagged in the claims table): the space numerator carries forward the supply-cost doc's flagged figures (the ~$6-8B/yr replacement capex and ~$200-260/sub/yr space-specific split are single-lineage); the ground-build annualization uses an assumed ~25-year fiber asset life (corroborated: IRS class life 24 yr, industry 20-25 yr) and a ~9% capital charge (the midpoint of the sourced ~10-15% IRR hurdle), both stated so they can be re-run; the mobile marginal cost (~$0.50-1.50/GB) is single-source in the floor doc.

---

## 1. Putting the Two Sides on a Common Basis

The data-center track produces a clean single ratio (1.92x) because both sides are greenfield: a new orbital data center against a new terrestrial one, both paying full freight. Communications cannot be reduced to one number, because the ground side appears in two forms that differ by an order of magnitude:

| Ground form | What it is | When it is the right comparison | Cost basis |
|---|---|---|---|
| **Fresh ground build** | A new fiber/cable/FWA/cell build to a location that has none | **Unserved / underserved fringe** (no incumbent plant) | Full per-passing capex (`comms_broadband_deployment_economics.md`, `comms_cellular_5g_deployment_economics.md`) |
| **Incumbent marginal cost** | The cash cost to serve one more already-connected subscriber on sunk plant | **Served markets** (incumbent already passes the home / covers the area) | ~10-20% of ARPU fixed; ~$0.50-1.50/GB mobile (`comms_incumbent_margins_competitive_floor.md`) |

The space side, by contrast, is a single number regardless of geography: the mature incumbent's all-in delivery cost (`comms_space_supply_cost.md`), because a satellite constellation has no "already built there" advantage at any specific location, it carries the same fixed fleet-plus-launch-plus-ground cost everywhere it points.

**The method.** To make a ratio, everything is put on **annualized cost to deliver, per subscriber per year**, the same unit the space doc's headline uses. The space side is already in that unit (~$480-680/sub/yr all-in). The fresh-ground-build side is a one-time capex, so it is annualized:

- Take the rural-fiber passing cost ($3,000-6,000) plus the connect cost ($500-700).
- Divide the passing cost by the ~46% take-rate, because only ~46% of passings become paying subscribers, so the per-*subscriber* capex is higher than the per-*passing* capex (`comms_broadband_deployment_economics.md` Section 4). Connect cost is already per-subscriber.
- Annualize the resulting per-subscriber capex over a **~25-year fiber asset life** at a **~9% capital charge** (capital-recovery-factor / annuity method).
- Add ground opex (~$150/sub/yr, the fixed-network sustaining and serve cost).

The asset-life and capital-charge assumptions are sourced and conservative: fiber's IRS class life is **24 years** and industry depreciation recommendations are **20-25 years** ([POTs and PANs / TFI](https://potsandpansbyccg.com/2016/11/18/economic-lives-of-fiber-assets/), [Beyond Telecom Law Blog](https://www.beyondtelecomlawblog.com/bonus-depreciation-and-fiber-optic-networks/)), and the ~9% capital charge sits at the low end of the sourced ~10-15% fiber IRR hurdle (`comms_broadband_deployment_economics.md`), both of which make the annualized ground number *lower* (more favorable to ground), so the ratio is if anything conservative against space.

The incumbent-marginal side needs no annualization: it is already a recurring cash cost, carried directly from the floor doc as ~10-20% of ARPU (~$7-15/mo = ~$84-180/sub/yr) for fixed broadband.

---

## 2. Flavor (a): Space vs a Fresh Ground Build (the Unserved-Area Ratio)

This is the true mirror of the data-center 1.92x: both sides are greenfield, neither has a sunk-cost advantage, and the question is purely "which costs less to deliver from scratch to a place that has nothing."

### 2.1 The annualized ground-build cost per subscriber

| Ground build (per subscriber per year, annualized) | Passing capex | Capex per sub (÷46% take + connect) | Annualized capital | + opex | **Total** |
|---|---|---|---|---|---|
| Suburban fiber | ~$1,250 | ~$3,300 | ~$340/yr | ~$150 | **~$490/yr** |
| **Rural fiber (low)** | ~$3,000 | ~$7,100 | ~$725/yr | ~$150 | **~$875/yr** |
| **Rural fiber (high)** | ~$6,000 | ~$13,600 | ~$1,390/yr | ~$150 | **~$1,540/yr** |
| Extreme remote tail | ~$200,000 | ~$435,000 | ~$44,300/yr | ~$150 | **~$44,500/yr** |

[DERIVED, from `comms_broadband_deployment_economics.md` passing/connect/take-rate, annualized as in Section 1.] Mobile is shown for context, not as the primary unserved comparison: a new rural macro site is ~$100-300k all-in (`comms_cellular_5g_deployment_economics.md`), and capex intensity runs ~14-19% of a ~$636/yr mobile ARPU (~$90-120/yr capex), but a fresh cell build to truly unserved territory carries the same density penalty fiber does.

### 2.2 The ratio

| Comparison (per sub/yr) | Ground build | Space (mature) | Ratio ground/space | Read |
|---|---|---|---|---|
| Suburban fiber | ~$490 | ~$480-680 | ~0.7-1.0x | roughly a **tie** in the suburban fringe (the crossover zone) |
| **Rural fiber (low)** | ~$875 | ~$480-680 | **~1.3-1.8x** | **space cheaper** by ~1.3-1.8x |
| **Rural fiber (high)** | ~$1,540 | ~$480-680 | **~2.3-3.2x** | **space cheaper** by ~2.3-3.2x |
| Extreme remote tail | ~$44,500 | ~$480-680 | **~65-90x** | **space cheaper** by ~2 orders of magnitude |

[DERIVED.] **The plain statement: in unserved territory, space is BELOW ground build cost, by roughly 1.3x to 3.2x in ordinary rural areas and by tens-fold in the remote tail.** The crossover sits around the dense-suburban fringe (~$490/yr ground vs ~$480-680 space), which is exactly where one would expect the line to fall: denser than that and ground build wins; sparser than that and space wins, by a margin that grows without bound as density drops.

### 2.3 This is not a model artifact: it is happening in procurement now

The flavor-(a) finding is corroborated by real 2025-26 broadband-subsidy decisions, an independent cross-check on the arithmetic. After the BEAD program's 2025 technology-neutral rule change, states are choosing satellite over fiber in the high-cost tail precisely because fiber per-location cost is prohibitive: BEAD fiber plans hitting **~$100,000 per location** are being rejected as unjustifiable versus satellite ([Colorado Sun](https://coloradosun.com/2025/07/25/cheaper-wireless-satellite-internet-trumps-fiber-colorado-broadband-bead/)), Maine is subsidizing Starlink for **~9,000 remote locations**, and Starlink plus Amazon requested **~$363M of Colorado's BEAD allocation** against fiber's ~$464M ([Colorado Sun](https://coloradosun.com/2025/07/25/cheaper-wireless-satellite-internet-trumps-fiber-colorado-broadband-bead/), [Broadband Breakfast](https://broadbandbreakfast.com/starlink-slashes-u-s-prices-in-new-offer-across-several-rural-states/)). The regulators are buying exactly the trade the ratio predicts: where the ground build runs into the thousands-to-hundreds-of-thousands per location, space is the cheaper delivery, full stop. [FACT, 2+ sources.]

---

## 3. Flavor (b): Space vs the Incumbent's Marginal Cost (the Served-Area Ratio)

This is the comparison the data-center track never has to make, and it inverts the result. In a served market the ground competitor is not a fresh build, it is an entrenched incumbent whose plant is sunk and who defends an existing customer at its **cash cost to serve**, far below both its own all-in cost and its sticker price (`comms_incumbent_margins_competitive_floor.md`).

### 3.1 The ratio, per subscriber per year

| Comparison (per sub/yr) | Incumbent marginal cost | Space (mature) | Ratio space/ground-marginal | Read |
|---|---|---|---|---|
| Fixed broadband, 20% of ARPU floor | ~$180/yr | ~$480-680 | **~2.7-3.8x** | **space costlier** |
| Fixed broadband, 10% of ARPU floor | ~$84/yr | ~$480-680 | **~5.7-8.1x** | **space costlier** |

[DERIVED, from `comms_incumbent_margins_competitive_floor.md` (~10-20% of ARPU = ~$84-180/sub/yr) and `comms_space_supply_cost.md` (~$480-680/sub/yr).] **The plain statement: in served territory, space is ABOVE the incumbent's defend cost, by roughly 3x to 8x.** And this uses the *mature incumbent* space cost; a small new space entrant, whose per-subscriber cost is "multiples higher" than Starlink's because it lacks the tens-of-millions-of-subscribers denominator (`comms_space_supply_cost.md` Section 5.4), sits far further above the floor still.

### 3.2 Per GB, served

| Service | Incumbent marginal | Space | Ratio | Read |
|---|---|---|---|---|
| Fixed broadband | <$0.01/GB | ~$0.05-0.30/GB | **~5-30x+** | space far costlier per GB |
| Mobile | ~$0.50-1.50/GB | ~$0.05-0.30/GB network-avg | space in-range to below network-average | but space cost **rises with density**, and served mobile demand concentrates in density |

[DERIVED/ESTIMATE.] The fixed-broadband per-GB gap is the cleanest expression of the asymmetry: an incumbent carries the marginal gigabyte for under a penny on sunk fiber, where space carries it for 5-30x+ more, and worse as users concentrate. The mobile line is the one place the gap narrows (space network-average can sit at or below the ~$0.50-1.50/GB mobile delivery cost), but the comparison is illusory in dense served markets because the space per-GB cost rises with density exactly there, while the mobile incumbent already monetizes spare capacity at that incremental floor (the MVNO-wholesale logic in `comms_incumbent_margins_competitive_floor.md`).

### 3.3 Why the incumbent can hold this floor

The incumbent does not merely have a low marginal cost; it has **~30-40 points of EBITDA headroom and ~70-80 points of broadband gross-margin headroom** to absorb a defensive price cut (`comms_incumbent_margins_competitive_floor.md` Sections 1, 3). It can drop a defended customer's price toward that ~10-20%-of-ARPU cash floor and still be operating-cash-flow positive, soaking the cut out of margin rather than going cash-negative. So a space entrant that is merely cheaper than the incumbent's *all-in* or *list* price has won nothing: the incumbent will price down to its marginal cost to defend, and the space entrant must beat *that* floor, which (per Section 3.1) it is 3-8x above. The non-price defenses (latency, bundle lock-in, switching costs; `comms_incumbent_margins_competitive_floor.md` Section 3.2 and `comms_broadband_deployment_economics.md` Section 6A) stack on top, so in practice the incumbent often holds the customer without even reaching its price floor.

---

## 4. The Two Ratios Side by Side, and the Mirror to the Data-Center 1.92x

| | Data-center track | Comms flavor (a): unserved | Comms flavor (b): served |
|---|---|---|---|
| Ground competitor | A **new** hyperscaler build | A **new** fiber/cell build | An **entrenched incumbent** on sunk plant |
| Ground cost basis | full all-in greenfield | full all-in greenfield (per-passing) | marginal cash cost to defend |
| Ratio | space/ground = **1.92x** (space costlier) | ground/space = **~1.3-3.2x** rural (space **cheaper**) | space/ground-marginal = **~3-8x** (space costlier) |
| Which side wins on cost | ground (space is 1.92x) | **space** (space is below ground by 1.3-3.2x) | ground (space is 3-8x above the floor) |

[DERIVED; the 1.92x is carried from the data-center track, not re-derived here.]

Two things are worth stating plainly about the mirror:

1. **Flavor (a) runs the OPPOSITE direction to the data-center ratio.** In compute, the orbital build is ~1.92x *more* expensive than a fresh ground build. In communications-to-the-unserved, the orbital build is ~1.3-3.2x *less* expensive than a fresh ground build. The sign flips because the ground cost structures are inverted: a data center gets *cheaper* per unit with scale and concentration (you build one big terrestrial facility), whereas terrestrial comms-to-a-home gets *more* expensive per unit as you push into low density (every remote home needs its own civil-works trench). Space has a flat per-location cost; ground does not. Where ground's per-location cost is high (sparse), space wins; where it is low (dense), ground wins.

2. **Flavor (b) is a comparison the data-center track does not have, and it is the one that bites.** A data center has no "incumbent who already built a data center on this exact rack and will defend it at marginal cost." Communications does: the served market is full of sunk plant defended at a cash floor 3-8x below the space cost. This is why the comms competitive picture is harsher than the data-center picture in served markets and more favorable in unserved ones. The single ratio the founder asked for genuinely does not exist for comms; the two-ratio split is the honest answer.

---

## 5. Question 2: What Cost Level a Space Operator Needs, and Whether It Is Realistic for SpaceX

The addressable-sizing doc puts the new-entrant-addressable revenue pool at **~$45-60B/yr conservative to ~$110-150B/yr optimistic, ex-China** (`comms_addressable_sizing.md`). The question is what delivery-cost level lets a space operator earn a meaningful slice of that at a reasonable margin, and whether that level is realistic.

### 5.1 The required cost level

To earn revenue at a healthy margin, the all-in delivery cost must sit well below ARPU. At Starlink's ~$790/yr ARPU, a ~38% operating margin requires all-in delivery of **~$480-490/sub/yr**, and the ~63% EBITDA margin implies an even lower cash-cost line. Expressed at the revenue-pool level:

| Revenue captured | All-in delivery cost at 38.6% op margin | Operating income |
|---|---|---|
| $11.4B (Starlink 2025 actual) | ~$7.0B | ~$4.4B |
| $30B | ~$18.4B | ~$11.6B |
| $50B | ~$30.7B | ~$19.3B |

[DERIVED, from the disclosed Starlink margin applied to higher revenue.] The required **per-subscriber** cost level is the same at any of these revenue points: **~$480-680/sub/yr all-in, of which the space-specific (satellite + launch replacement) portion is ~$200-260/sub/yr** (`comms_space_supply_cost.md`).

### 5.2 Is that aggressive but achievable at SpaceX scale?

**The framing in the question understates the case.** That ~$480-680/sub/yr cost level, at a ~38% operating and ~63% EBITDA margin, is not a target SpaceX would need to stretch for. It is **Starlink's disclosed 2025 actual**: $11.4B segment revenue, **38.6% segment operating margin, ~63% segment adjusted EBITDA margin, ~10.3M subscribers** ([SpaceX S-1, May 2026](https://www.satellitetoday.com/finance/2026/05/20/spacexs-ipo-filing-gives-first-look-into-companys-financials/); [SpaceXChart](https://spacexchart.com/starlink); [New Space Economy](https://newspaceeconomy.ca/2026/05/30/what-is-starlinks-financial-performance/)) [FACT]. So at SpaceX scale the cost structure is not aspirational, it is **already achieved and audited**. The cost-downs the S-1 cites (constellation amortization rolling off, terminal subsidy shrinking, launch $/kg falling as V3-on-Starship lands) point to the cost level continuing *down* from here, not needing to be reached.

**The decisive qualifier is scale, not feasibility.** The space cost stack is overwhelmingly fixed: build and continuously replace a fleet on a 5-year treadmill (~$6-8B/yr at incumbent scale), launch it, run a ground network. Per-subscriber cost is therefore driven by the denominator, the number of subscribers spreading that fixed cost (`comms_space_supply_cost.md` Sections 4-5). At tens of millions of subscribers the per-subscriber cost is ~$480-680/yr; at thousands-to-low-millions it is multiples higher. So the honest answer to "is the cost structure realistic for SpaceX" is:

> **Yes, and stronger than 'achievable': the required cost level is SpaceX's measured reality today. But it is realistic for SpaceX *specifically*, because it is bought with scale (tens of millions of subscribers and a self-supplied launch cadence), and it is NOT available to a small constellation, whose fixed-cost-dominated stack spreads over too few subscribers to reach it.**

This is the cost-side echo of the addressable doc's "scale is the whole game" and the supply-cost doc's conservative-new-entrant case: the space economics that win are a scale phenomenon, and the entity that has the scale is the incumbent.

---

## 6. Question 3: The Competitive Verdict (Cost-Base Level, No Business Verdict)

Where can space actually win on cost, and where can it not? The two ratios answer it directly, and the answer is an asymmetry.

| Territory | Relevant ground cost | Space vs ground | Can space win on cost? |
|---|---|---|---|
| **Dense urban / suburban, served** | incumbent marginal ~10-20% of ARPU (~$84-180/sub/yr fixed); <$0.01/GB | space ~3-8x above the floor; per-GB 5-30x+ above (and rising with density) | **No.** The incumbent defends at a cash floor far below space cost, with EBITDA headroom and non-price moats on top. |
| **Suburban fringe (the crossover)** | fresh build ~$490/sub/yr annualized | roughly a tie (~0.7-1.0x) | **Contested.** This is the boundary; small shifts in density or build cost tip it either way. |
| **Rural / remote, unserved** | fresh build ~$875-1,540/sub/yr annualized | space ~1.3-3.2x cheaper | **Yes.** No incumbent plant, so no marginal-cost floor; space beats a fresh build outright. |
| **Extreme remote tail** | fresh build ~$44,500/sub/yr annualized | space ~65-90x cheaper | **Yes, decisively.** No terrestrial business case closes at any price; space is the only economic delivery. |
| **Premium / sovereign** | no incumbent marginal floor (bespoke or no terrestrial alternative); buyer pays for attributes, not lowest $/GB | space competes on sovereignty / security / resilience / latency, not on raw cost | **Yes on a different axis.** The comparison is not lowest-cost-delivery but a capability the ground cannot offer; there is no sunk-plant floor to undercut. |

[DERIVED/ESTIMATE, synthesizing Sections 2-3 with `comms_addressable_sizing.md` and `comms_incumbent_margins_competitive_floor.md`.]

**The headline insight, stated as the asymmetry it is:**

> **The ground-vs-space cost ratio is not a constant; it flips on whether the ground plant already exists. Space is cheaper than a fresh ground build (by ~1.3-3.2x rural, tens-fold in the remote tail) wherever there is no incumbent, and costlier than an incumbent's marginal defense (by ~3-8x) wherever there is one. Space therefore wins on cost in the unserved/remote fringe and the premium/sovereign layer, where no sunk-plant floor exists, and loses on cost in dense served markets, where the incumbent defends at a cash cost far below its sticker price. The places space wins on cost are exactly the places the addressable-sizing track already found the dollars.**

The convergence is the point worth carrying forward: the demand-side track (`comms_addressable_sizing.md`) found the addressable dollars concentrated in the fringe, the verticals, and the open government layer; the cost-side analysis here finds the cost ratio favors space in exactly those same places and nowhere else. Two independent lines of reasoning, one from revenue and one from cost, land on the same map. That is the cost-and-competitive base. Whether a Rocket Lab comms cost stack can actually be built to the ~$480-680/sub/yr level (a scale question it does not obviously clear) is the thesis's call, not this doc's.

---

## 7. A Note for the Lead (reconciliation, not an edit)

While consolidating, one inconsistency surfaced in the wave-2 premium/sovereign sizing that the lead should reconcile (this doc does not edit the wave-2 doc):

- The premium/sovereign **gross spend pool** is recorded as **~$60-95B/yr** (global COMM-070), of which ~$60-70B is sourced bottom-up from the components and the top of the span (up to ~$95B) is an estimated ceiling, not a sourced figure. The earlier wave-2 headline of ~$75-95B sat above the component sum: the component build (Section 2 buckets) and the underlying `comms_premium_sovereign_sizing.md` roll up nearer **~$60-70B/yr** once summed rather than taken at the headline, a ~$15-25B disagreement. This does not change any conclusion in *this* doc (the addressable-revenue target enters here only as the ~$45-150B *new-entrant-addressable* band, which is downstream of the open slice, not the gross pool). APPLIED (lead, 2026-06-11): the gross pool was restated to ~$60-95B (a span that includes the bottom-up component sum) across the wave-2 docs and the ledger (global COMM-070).

---

## Sources

*Space numerator and ground stacks (carried from the cited base docs, each of which holds its own underlying 2+ source citations inline)*
- [research/economics/comms_space_supply_cost.md](./comms_space_supply_cost.md) (space all-in ~$480-680/sub/yr, ~$200-260 space-specific, ~$0.05-0.30/GB rising at density, 5-yr treadmill, scale-driven new-entrant case)
- [research/economics/comms_incumbent_margins_competitive_floor.md](./comms_incumbent_margins_competitive_floor.md) (incumbent marginal floor ~10-20% of ARPU fixed, ~$0.50-1.50/GB mobile, ~30-40 pts EBITDA headroom, sunk-plant asymmetry)
- [research/economics/comms_broadband_deployment_economics.md](./comms_broadband_deployment_economics.md) (fiber passing/connect, cable upgrade, FWA, take-rate, density cliff, ~$200,000+ tail)
- [research/economics/comms_cellular_5g_deployment_economics.md](./comms_cellular_5g_deployment_economics.md) (mobile capex intensity, per-site, GSMA per-connection)
- [research/economics/comms_addressable_sizing.md](./comms_addressable_sizing.md) (~$45-150B/yr addressable pool, ex-China)

*Independent corroboration verified for this doc*
- [SpaceX IPO filing readout, Via Satellite (May 2026)](https://www.satellitetoday.com/finance/2026/05/20/spacexs-ipo-filing-gives-first-look-into-companys-financials/) ($11.4B Starlink, segment margins, subscribers)
- [SpaceXChart, Starlink unit economics](https://spacexchart.com/starlink) (38.6% operating margin, 5-yr depreciation)
- [New Space Economy, Starlink financial performance](https://newspaceeconomy.ca/2026/05/30/what-is-starlinks-financial-performance/) (~63% segment EBITDA margin)
- [POTs and PANs / TFI, economic lives of fiber assets](https://potsandpansbyccg.com/2016/11/18/economic-lives-of-fiber-assets/) (fiber depreciation 20-25 yr)
- [Beyond Telecom Law Blog, depreciation and fiber optic networks](https://www.beyondtelecomlawblog.com/bonus-depreciation-and-fiber-optic-networks/) (IRS class life 24 yr)
- [Colorado Sun, satellite vs fiber in Colorado BEAD](https://coloradosun.com/2025/07/25/cheaper-wireless-satellite-internet-trumps-fiber-colorado-broadband-bead/) (fiber ~$100k/location rejected for satellite; $363M vs $464M requests)
- [Broadband Breakfast, Starlink rural-state pricing / BEAD](https://broadbandbreakfast.com/starlink-slashes-u-s-prices-in-new-offer-across-several-rural-states/) (state satellite-subsidy programs, Maine ~9,000 locations)
- [Fierce Network, satellite isn't a better replacement for fiber](https://www.fierce-network.com/broadband/satellite-isnt-better-replacement-fiber-heres-why) (the served-market other side: fiber wins on quality/price where it exists)

---

## Confidence

- **The asymmetry (the headline): medium-high.** That space beats a fresh ground build in the unserved fringe and loses to an incumbent's marginal cost in served markets follows directly from the sourced ground and space cost stacks, and is independently corroborated by 2025-26 BEAD procurement choosing satellite in the high-cost tail and by the incumbent gross-margin / marginal-cost data. The *direction* of both ratios is robust.
- **The point ratios: medium.** Flavor (a)'s ~1.3-3.2x rural and flavor (b)'s ~3-8x are arithmetic on sourced ranges. The flavor-(a) number carries an annualization assumption (fiber ~25-yr life, ~9% capital charge) that is sourced and stated; reasonable alternative assumptions (shorter life, higher WACC) would *raise* the ground number and widen space's advantage, so the chosen values are conservative against space. The flavor-(b) number is a clean read of the sourced marginal-cost floor against the sourced space cost.
- **The space numerator: inherited (medium-high on disclosed financials, medium on the derived split).** The ~$480-680/sub/yr all-in is anchored to the audited S-1 segment operating income; the ~$200-260 space-specific split leans on the single-lineage ~$6-8B/yr replacement capex flagged in the source doc. Carried forward with its original confidence, not strengthened.
- **The realistic-for-SpaceX answer: high on the fact, medium on the scale caveat.** That ~$480-680/sub/yr at ~38%/~63% margins is Starlink's disclosed actual is a FACT, cross-checked across three readers. The claim that the same level is unreachable for a small constellation is the supply-cost doc's structural (not modeled) new-entrant argument, carried forward.
- **The crossover density: low-medium.** The suburban-fringe tie (~$490/yr ground vs ~$480-680 space) marks roughly where the line falls, but the exact density at which fresh-build cost crosses space cost is sensitive to the take-rate, asset life, and local build cost, and is given as a zone, not a point. It ties to the same open density-crossover question both base docs flag.

---

## Open Questions

1. **The exact crossover density.** Section 2 places the fresh-build-vs-space crossover around the dense-suburban fringe (~$490/yr annualized ground). The precise homes-per-mile (or $/passing) at which a fresh ground build crosses above the ~$480-680/sub/yr space cost is the single number that sizes the cost-advantaged fringe, and it needs the density-cost model both base docs already flag (`comms_broadband_deployment_economics.md` OQ3, `comms_space_supply_cost.md` OQ4).
2. **A hard space cost-per-GB.** Flavor (b)'s per-GB ratio rests on the ~$0.05-0.30/GB space figure, which is utilization-dependent and the softest number in the space stack. A disclosed Starlink throughput (petabytes/day) would tighten both the per-GB ratio and the density-crossover point.
3. **The new-entrant (non-SpaceX) cost level.** This doc's space numerator is the *mature incumbent*. A concrete small-constellation cost model (N satellites, M subscribers, fixed-cost spread) would convert "multiples higher per subscriber" into a number and let the ratios be re-run for a Rocket Lab-scale entrant rather than for Starlink, which is the comparison the thesis ultimately needs.
4. **How aggressively incumbents actually price to defend against satellite.** Flavor (b) establishes the floor the incumbent *could* cut to; whether it does so against a LEO competitor (versus relying on latency/bundle defenses) is a market-conduct question that bears on how much of the served market is truly closed to space on price (`comms_incumbent_margins_competitive_floor.md` OQ4).
5. **Mobile as the narrowest gap.** Section 3.2 notes the space network-average per-GB can sit at or below the mobile ~$0.50-1.50/GB delivery cost, the one served comparison where the gap nearly closes. Whether direct-to-cell / mobile-augmentation is therefore the served sub-market where space is least disadvantaged on cost (distinct from fixed broadband, where it is 5-30x+ above) is worth a dedicated pass, and ties to the direct-to-cell bucket in the addressable doc.

---

## Claims table

| COMM- id | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-109 | Annualized fresh-ground-build cost to deliver, rural fiber, per subscriber per year | ~$875/yr (low) to ~$1,540/yr (high); suburban ~$490; extreme tail ~$44,500 | DERIVED | this doc S2, from [comms_broadband_deployment_economics.md](./comms_broadband_deployment_economics.md) (passing/connect/take-rate) + 25-yr/9% annualization |
| COMM-110 | Ground-vs-space cost ratio, FLAVOR (a) space vs fresh ground build (unserved) | ground/space ~1.3-3.2x rural (space BELOW ground); ~65-90x in the extreme tail; ~tie at the suburban fringe | DERIVED | this doc S2, from [comms_space_supply_cost.md](./comms_space_supply_cost.md) + COMM-109 |
| COMM-111 | Ground-vs-space cost ratio, FLAVOR (b) space vs incumbent marginal cost (served) | space/ground-marginal ~3-8x (space ABOVE the floor) per sub/yr; per-GB ~5-30x+ above fixed | DERIVED | this doc S3, from [comms_incumbent_margins_competitive_floor.md](./comms_incumbent_margins_competitive_floor.md) (~$84-180/sub/yr) + [comms_space_supply_cost.md](./comms_space_supply_cost.md) (~$480-680) |
| COMM-112 | Fiber asset life used to annualize the ground build | ~25 yr (IRS class life 24 yr; industry 20-25 yr); ~9% capital charge | FACT (asset life) / ASSUMPTION (capital charge) | [POTs and PANs/TFI](https://potsandpansbyccg.com/2016/11/18/economic-lives-of-fiber-assets/), [Beyond Telecom Law Blog](https://www.beyondtelecomlawblog.com/bonus-depreciation-and-fiber-optic-networks/) |
| COMM-113 | BEAD procurement choosing satellite over fiber in the high-cost tail (real-world corroboration of flavor a) | fiber ~$100k/location rejected for satellite; Maine ~9,000 locations on Starlink; CO satellite ~$363M vs fiber ~$464M requests | FACT | [Colorado Sun](https://coloradosun.com/2025/07/25/cheaper-wireless-satellite-internet-trumps-fiber-colorado-broadband-bead/), [Broadband Breakfast](https://broadbandbreakfast.com/starlink-slashes-u-s-prices-in-new-offer-across-several-rural-states/) |
| COMM-114 | Cost level a space operator needs to earn the addressable pool at reasonable margin | ~$480-680/sub/yr all-in (space-specific ~$200-260/sub/yr); clears ~38% op / ~63% EBITDA at ~$790 ARPU | DERIVED/ESTIMATE | this doc S5, from [comms_space_supply_cost.md](./comms_space_supply_cost.md) + [comms_addressable_sizing.md](./comms_addressable_sizing.md) |
| COMM-115 | Whether that cost level is realistic for SpaceX | Already achieved at SpaceX scale (it is Starlink's disclosed 2025 actual: 38.6% op / ~63% EBITDA, ~10.3M subs); unreachable for a small constellation (denominator-driven) | FACT (the actual) / ESTIMATE (the scale caveat) | [SpaceX S-1](https://www.satellitetoday.com/finance/2026/05/20/spacexs-ipo-filing-gives-first-look-into-companys-financials/), [SpaceXChart](https://spacexchart.com/starlink), [New Space Economy](https://newspaceeconomy.ca/2026/05/30/what-is-starlinks-financial-performance/) |
| COMM-116 | The competitive verdict (cost-base level): the asymmetry | Space wins on cost in the unserved/remote fringe and premium/sovereign (no incumbent floor); loses in dense served markets (incumbent defends at marginal cost 3-8x below space). The ratio flips on whether ground plant already exists. | ESTIMATE (interpretation) | this doc S6, synthesizing all cited docs |
| COMM-117 | Crossover zone between flavor (a) space-wins and flavor (b) space-loses | ~dense-suburban fringe (~$490/sub/yr annualized fresh build ~= ~$480-680 space); a zone, not a point | DERIVED/ESTIMATE | this doc S2, S6 |
