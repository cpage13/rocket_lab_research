# The Ground-Side Cost of Cellular Service, Per Subscriber: The Comparison Unit, the Two-Regime Cost, and the Niche

*Research date: June 2026. Communications research-wiki effort (shared library). Direct-to-cell (satellite-cellular) track.*

**Builds on / does not duplicate:** this doc answers ONE founder question the corpus left implicit: when we weigh a satellite-cellular constellation against the ground, *what is the unit*, and *what is the ground number in that unit*. The two-flavor ground-vs-space cost ratio already exists; this doc does not re-derive it. It (1) settles the comparison UNIT (per subscriber per year vs per Mbps vs per GB), (2) pins the ground CELLULAR cost per subscriber per year with a clean capex/opex build (spectrum EXCLUDED, held out to match the space side), and (3) translates that into the per-Mbps and per-GB axes so the space-vs-ground comparison is honest in each. The load-bearing inputs, each cited by path and by its GLOBAL SOURCE_INDEX id where one exists:

- [research/economics/comms_cellular_5g_deployment_economics.md](./comms_cellular_5g_deployment_economics.md) (the GROUND CELLULAR build/opex: capex intensity ~14-19% of service revenue, ~$20-50k upgrade / ~$100-300k new macro site, RAN ~55-65% of capex, energy ~20-40% of opex, US ~$29-30B/yr network capex + ~$53B/yr network opex, ~248,050 macro sites, ~579M connections, GSMA ~EUR35/connection capex).
- [research/economics/comms_incumbent_margins_competitive_floor.md](./comms_incumbent_margins_competitive_floor.md) (the GROUND MARGINAL floor: fixed ~10-20% of ARPU = ~$84-180/sub/yr, mobile data ~$0.50-1.50/GB, fixed data <$0.01/GB, ~30-40 pts EBITDA headroom; global SOURCE_INDEX COMM-096, COMM-098).
- [research/economics/comms_broadband_deployment_economics.md](./comms_broadband_deployment_economics.md) (the GROUND BUILD, fixed: fiber ~$700-1,500 urban / $3,000-6,000 rural / up to ~$200-230k tail per passing; FWA ~$300-800/sub; take-rate ~46%).
- [research/economics/comms_space_supply_cost.md](./comms_space_supply_cost.md) (the SPACE numerator: all-in ~$480-680/sub/yr, space-specific ~$200-260/sub/yr, network-average ~$0.05-0.30/GB RISING with density; global SOURCE_INDEX COMM-091).
- [research/economics/comms_direct_to_cell.md](./comms_direct_to_cell.md) (the DIRECT-TO-CELL delivery cost: ~$5-9/GB beam-saturated vs ~$0.30/GB terrestrial 5G, ~20x; global SOURCE_INDEX COMM-145, COMM-147).
- [research/economics/comms_ground_vs_space_cost_ratio.md](./comms_ground_vs_space_cost_ratio.md) (the two-flavor ratio: space ~1.3-3.2x cheaper than a fresh rural build, ~3-8x costlier than incumbent marginal; global SOURCE_INDEX COMM-100, COMM-101, COMM-103).
- [research/economics/comms_rural_fringe_sizing.md](./comms_rural_fringe_sizing.md) and [research/economics/comms_global_regional_market.md](./comms_global_regional_market.md) (the NICHE: US ~8-13M HH, developed-world ~30-45M HH, coverage gap ~300M people).
- [synthesis/comms_framework_synthesis.md](../synthesis/comms_framework_synthesis.md) (the density-aware unit: the comms model UNIT is cost per subscriber per year and per GB, and space cost-per-subscriber RISES with density; global SOURCE_INDEX COMM-172).

> **Reading guide.** Every hard number is tagged **[FACT]** (sourced 2+ independent), **[FACT, single-source]** (one source), **[DERIVED]** (my arithmetic on cited inputs), **[ESTIMATE]** (third-party model/sizing), or **[UNKNOWN]** (a named gap). China is **excluded** and appears only as a labelled aside. Inline math uses ^2, x, ->, log2.

> **Scope.** This is a NEUTRAL base doc. It renders NO go/no-go verdict on a Rocket Lab satellite-cellular business. It establishes the unit and the ground number in that unit, and identifies where the ground per-subscriber cost gets high enough that a ~$0.5B, few-hundred-satellite constellation could undercut it. Whether Rocket Lab specifically clears that bar is the thesis's call, not this doc's.

> **A note on claim IDs.** The cited base docs each ran an internal COMM- namespace; many collide across files. Where a number was promoted to the single global ledger, this doc cites the GLOBAL [SOURCE_INDEX.md](../SOURCE_INDEX.md) id (e.g. `global COMM-091`), which is unambiguous. This doc's own new claims are COMM-521..534 (the next free contiguous block above the global max; COMM-493..520 are reserved by [dtc_data_rate_vs_spectrum.md](../direct_communication/dtc_data_rate_vs_spectrum.md), of which 493..512 are used).

---

## 0. Answer First

**The comparison unit (Question 1).** Use **cost per subscriber per year as the primary unit**, and carry **cost per GB as the honest secondary**, and treat **cost per Mbps as a trap to be shown but not led with**. The reasons, in one paragraph each below, are: (a) per-subscriber-per-year is the only axis on which both sides report real, audited numbers (Starlink's S-1 gives ~$480-680/sub/yr; the carriers give ARPU, capex, opex, and subscriber counts), and it is the axis the whole comms corpus already uses [global COMM-172]; (b) per-GB is the structurally honest axis because it exposes the one fact that decides the whole question, that satellite cost-per-bit RISES with user density while terrestrial falls; (c) per-Mbps-of-typical-speed flatters the ground so heavily (ground delivers ~170-180 Mbps, space ~20-30 Mbps to a phone) that it makes space look ~16-24x worse than it is on the metric that actually matters, because the satellite product is not selling peak speed, it is selling coverage where there is no speed at all. The honest framing is therefore: **price the satellite per subscriber per year against the ground per subscriber per year in the SAME regime (unserved fringe), cross-check per GB, and never let the per-Mbps ratio stand in for the comparison.**

**The ground cellular cost per subscriber, both regimes (Questions 2 and 3).** Ground cost per subscriber is NOT one number; it splits by whether the plant already exists:

| Regime | Ground cellular cost per subscriber per year (capex + opex, spectrum excluded) | Per GB | Per Mbps of typical speed | Basis |
|---|---|---|---|---|
| **Dense, served (incumbent marginal)** | **~$84-180/sub/yr** (fixed-broadband floor, the cleanest sourced floor); mobile network all-in ~$140-235/sub/yr | mobile ~$0.50-1.50/GB; fixed <$0.01/GB | ~$0.8-1.3 per sub/yr per Mbps | [global COMM-096; this doc S2] |
| **Sparse, fresh build (greenfield)** | **~$875-1,540/sub/yr** rural (annualized); ~$44,500/sub/yr extreme tail | per-GB is the wrong axis (cost is per-passing) | n/a (build cost, not throughput cost) | [global COMM-100; this doc S3] |

[DERIVED/FACT.] The space side carries the SAME ~$480-680/sub/yr everywhere it points [global COMM-091], because a satellite has no "already built here" advantage at any specific location. So the verdict is the asymmetry the cost-ratio doc already found: **space sits BELOW the sparse fresh-build cost (it wins the unserved fringe by ~1.3-3.2x rural, tens-fold in the tail) and ABOVE the dense served marginal cost (it loses to the incumbent's defend-floor by ~3-8x).** This doc's contribution is to put the GROUND CELLULAR number on that axis with its own capex/opex build, and to settle which unit makes the comparison fair.

**The niche where space could undercut (Question 4).** The ground per-subscriber cost crosses above the ~$480-680/sub/yr space cost wherever a fresh build is required and density is low: the **sparse, remote, unserved fringe**. Concretely that is **~8-13M US households** in broadband deserts and weak-terrestrial rural [global COMM-072/073, rural file], **~30-45M developed-world households** [global COMM-075], and the **~300M-person global coverage gap** with no mobile signal at all [global COMM-021]. For satellite-CELLULAR specifically, the niche narrows further to where the demand is a phone, not a home pipe: maritime, aviation, off-grid/rural mobility, emergency/continuity, and the thin-edge rural home that a good-enough phone collapses. The constellation economics the founder posited (~$2-3M/satellite x a few hundred satellites ~= ~$0.5B, a coverage-driven subscriber base) live or die on whether that coverage base is large enough to spread the fixed cost to the ~$480-680/sub/yr level, which is a denominator question, not a per-site question, and is exactly where the corpus says "scale is the whole game" [global COMM-091, COMM-103].

**Confidence: medium-high** on the unit recommendation (it falls out of which numbers are auditable and the density inversion, both well-established in the corpus) and on the served-regime ground floor (sourced, two-regime, carried from the margins doc). **Medium** on this doc's own ground-cellular per-subscriber build (US aggregate capex/opex divided by connection and phone-subscriber counts, my arithmetic, denominator-sensitive, flagged throughout). **Medium** on the niche sizing (carried from the rural-fringe doc, where the household counts are softer than the percentage inputs).

---

## 1. Question 1: The Comparison Unit

The founder framed it exactly right: we are choosing the unit on which space competes with ground, and the choice is load-bearing because the two sides are not symmetric on every axis. The contrast that makes the choice matter:

- The **space side** delivers **~20-30 Mbps to a phone** (the corpus's single-phone operating point: ~25 Mbps single-phone target for a ~25 m^2 aperture on owned spectrum, cross-checked against AST BlueWalker 3's ~21 Mbps single-device demonstration) [FACT/DERIVED, [dtc_per_phone_rate_and_latency.md](../direct_communication/dtc_per_phone_rate_and_latency.md), global COMM-278/362] at a low price (~$10/month D2C add-on, often bundled free) [FACT, global COMM-146 area, [comms_direct_to_cell.md](./comms_direct_to_cell.md)].
- The **ground side** delivers **~170-180 Mbps** typical (US median fixed/mobile broadband) at **~$80/month**.

Three candidate units, judged on whether they make the comparison honest:

### 1.1 Per subscriber per year: the primary unit (recommended)

This is the only axis on which BOTH sides report real numbers:

- Space: Starlink's S-1 gives a DISCLOSED all-in delivery cost of **~$480-680/sub/yr** (revenue minus operating income), space-specific portion ~$200-260/sub/yr [DERIVED from S-1, global COMM-091].
- Ground: the carriers disclose ARPU (~$50-57/mo postpaid phone), capex (~$29-30B/yr US network), opex (~$53B/yr US network), and subscriber counts, from which a per-subscriber cost builds directly (Section 2).

It is also the unit the entire comms corpus already standardizes on: the framework synthesis names "cost per subscriber per year and per GB, density-aware" as THE model unit [global COMM-172], and the two-flavor ratio is computed in it [global COMM-100/101]. Adopting it keeps this doc commensurable with everything upstream and downstream. It is the right PRIMARY unit.

The one caveat to state honestly: a "subscriber" is not the same thing on both sides. A ground postpaid phone subscriber consumes ~25-30 GB/month and treats the phone as a primary connection; a satellite-cellular subscriber today consumes kilobytes-to-megabytes (messaging, occasional data) and treats it as a safety-net supplement [FACT, [comms_direct_to_cell.md](./comms_direct_to_cell.md)]. So "$/subscriber/yr" compares a heavy ground user against a light space user. This is why per-subscriber-per-year must be paired with per-GB (which normalizes for how much is actually delivered), not used alone.

### 1.2 Per GB: the honest secondary (carry it)

Per-GB is the axis that exposes the single fact that decides the whole question:

> **Satellite cost-per-GB RISES with user density; terrestrial cost-per-GB FALLS with density.** [FACT, corroborated across Morningstar, WIA, Madden; global COMM-108, COMM-172]

A terrestrial network adds capacity by adding towers (cells shrink, bits/s per km^2 rises, cost/GB falls). A satellite beam cannot shrink below its aperture-and-altitude limit, so more users under one beam divide the same pie thinner and cost/GB rises [FACT, [comms_direct_to_cell.md](./comms_direct_to_cell.md) Section 3]. The numbers:

| Delivery | Cost per GB | Tag | Source |
|---|---|---|---|
| Fixed broadband, marginal on sunk plant | **<$0.01/GB** | [FACT] | global COMM-095, margins file |
| Terrestrial mobile, marginal data | **~$0.50-1.50/GB** | [FACT, single-source] | global COMM-096, margins file |
| Terrestrial 5G, all-in delivery (analyst) | **~$0.30/GB** | [FACT, single analyst] | global COMM-147, D2C file |
| Satellite, network-average (incumbent, utilization-dependent) | **~$0.05-0.30/GB rising at density** | [ESTIMATE] | global COMM-091, space file |
| Satellite direct-to-cell, beam-saturated delivery | **~$5-9/GB (~20x terrestrial 5G)** | [FACT, single named analyst: Madden] | global COMM-147, D2C file |

[Carried, not re-derived.] The split between the ~$0.05-0.30/GB network-average satellite figure and the ~$5-9/GB beam-saturated D2C figure is itself instructive: it is the SAME density inversion. Spread thin over a sparse footprint, satellite is ~$0.05-0.30/GB; saturate a beam with phones (the D2C case in any populated area), it is ~$5-9/GB. Per-GB is therefore the unit that makes the density story visible, which per-subscriber-per-year hides. Carry it as the honest secondary.

### 1.3 Per Mbps of typical speed: the trap (show, do not lead)

The founder named the alternative explicitly: cost per amount of download speed (per Mbps-per-user). On this axis the comparison is brutally unfair to space, and the unfairness is the point:

| Side | Cost per sub/yr | Typical speed delivered | Cost per sub/yr per Mbps | Tag |
|---|---|---|---|---|
| Ground (mobile network all-in) | ~$140-235/sub/yr (S2) | ~170-180 Mbps | **~$0.8-1.3 per sub/yr per Mbps** | [DERIVED] |
| Space (satellite-cellular) | ~$480-680/sub/yr | ~20-30 Mbps to a phone | **~$16-34 per sub/yr per Mbps** | [DERIVED] |

[DERIVED, this doc. Ground per-Mbps = ~$200/yr / ~175 Mbps; space per-Mbps = ~$580/yr / ~25 Mbps.] On per-Mbps-of-typical-speed, space looks **~16x to ~34x worse** than ground. That ratio is real arithmetic but it is a misleading unit for this comparison, for one reason: **the satellite-cellular product is not competing on peak download speed. It is competing on coverage where the ground speed is zero.** A unit that divides by "typical Mbps delivered" rewards the ground product for being fast in the places it already serves, and penalizes the space product for being slow in the places nothing else reaches at all. In the unserved fringe the ground "typical speed" is not 175 Mbps, it is 0 (no tower), so the ground per-Mbps figure is undefined (division by zero), and the honest comparison is "25 Mbps from space vs nothing from the ground," which the per-Mbps unit cannot express.

> **The recommendation, stated plainly:** lead with **$/subscriber/yr**, in the **same regime** on both sides (compare space to a fresh rural build, not to a dense incumbent, when the target is the unserved fringe). Cross-check on **$/GB**, which is where the density inversion becomes visible and where the satellite product's true cost penalty in populated areas (~$5-9/GB) shows up. Show **$/Mbps** only to make the point that it is the wrong unit: it flatters the ground by ~16-34x because it prices peak speed in served areas, not coverage in unserved ones, which is the only thing the satellite is selling. The corpus already chose this unit (per subscriber per year and per GB, density-aware) [global COMM-172]; this doc confirms it is the right choice and names why the speed-based alternative misleads.

---

## 2. Question 2 and the Served Regime: The Ground Cellular Cost Per Subscriber

This is the doc's own build. The founder asked for the cellular TOWER / INFRASTRUCTURE / MAINTENANCE cost, split into capex (sites, radios, backhaul; spectrum EXCLUDED) and opex (lease, power, backhaul, maintenance, ops), translated to an annual cost per subscriber. The corpus has every input; this section assembles them and divides.

### 2.1 The capex stack (spectrum excluded)

| Capex line | Figure | Tag | Source |
|---|---|---|---|
| US annual wireless NETWORK capex (radios, equipment, integration) | **~$29-30B/yr** | [FACT] | global COMM-018 (CTIA) |
| US annual total wireless INFRASTRUCTURE investment (incl. towers, indirect) | **~$63B/yr** | [FACT] | global COMM-019 (WIA) |
| 5G upgrade of an existing macro site | ~$20-50k/site | [FACT] | global COMM-004 |
| New macro cell site, all-in (radios + tower + civil + backhaul tie-in) | ~$100-300k/site (avg ~$250k); up to >$1M complex | [FACT] | global COMM-005 |
| Cost split: RAN (radios + baseband) | **~55-65% of network capex** (the dominant line) | [FACT direction] | global COMM-009 |
| Cost split: backhaul / transport | ~15-30%; fiber ~$25-150k/km | [FACT direction] | global COMM-010 |
| Capex INTENSITY (capex as % of service revenue) | **~14-19%**, peaking ~19% in 2022, easing to ~15% | [FACT] | global COMM-001/002/003 |
| Sourced capex per CONNECTION (the cleanest anchor) | **GSMA ~EUR35/connection** (~EUR70 for "connectivity leaders") | [FACT] | global COMM-027 |

[Carried.] Spectrum is EXCLUDED from this stack on purpose, to match the space side (the founder's instruction). For scale, US C-band spectrum alone was ~$81B one-time [FACT, global COMM-012], a layer larger than a full year of network capex, but it is a license cost, not infrastructure, and the satellite side holds spectrum out symmetrically (it leases carrier spectrum via SCS at near-zero capex, or the ~$17B EchoStar buy is the hyperscale exception) [global COMM-175]. Holding spectrum out of BOTH sides is the honest matched comparison.

### 2.2 The opex stack

| Opex line | Figure | Tag | Source |
|---|---|---|---|
| US annual wireless NETWORK opex (lease, power, backhaul, maintenance, ops) | **~$53B/yr** | [FACT] | global COMM-020 (WIA) |
| Energy as a share of network opex | ~20-40% | [FACT range] | global COMM-021 |
| 5G site power draw | ~11.5 kW typical, +70% to +140% vs legacy site | [FACT] | global COMM-022 |
| RAN share of network energy | ~73% | [FACT] | global COMM-023 |

[Carried.] The opex line is dominated by site lease, power, and backhaul, with energy (the RAN especially) the fastest-rising component. Maintenance and field ops are folded into the ~$53B WIA network-opex figure.

### 2.3 The denominator: connections vs human phone subscribers

The translation to per-subscriber is denominator-sensitive, and the corpus flags this explicitly [global COMM-032]. Two defensible denominators:

- **All connections: ~579M** [FACT, global COMM-029]. This includes phones, tablets, connected cars, IoT modules, and fixed-wireless home units, not just human phone subscribers (~1.7 connections per person).
- **Human phone subscribers: ~350-400M** [DERIVED from carrier postpaid+prepaid phone counts]. AT&T ~74.2M postpaid phone, T-Mobile ~85.6M postpaid phone, Verizon ~core phone base, plus prepaid and the rest; the big-three postpaid phone bases alone are ~200M+, and adding prepaid and regional lands the human-phone-subscriber count near ~350-400M. The exact split is not cleanly disclosed; this is an estimate [ESTIMATE].

The honest move is to give the per-subscriber number on BOTH bases and flag the range.

### 2.4 The build: ground cellular cost per subscriber per year (DERIVED)

> **FLAGGED DERIVED.** No clean operator-disclosed per-subscriber TOTAL cost benchmark surfaced (the corpus's standing gap, global COMM-032 and the cellular doc's OQ4). The figures below are this doc's arithmetic on the sourced aggregate capex/opex and connection counts. Treat as order-of-magnitude, cross-checked against the GSMA per-connection capex anchor and the margins-doc marginal floor, not as an audited fact.

| Metric | Arithmetic | Result | Tag |
|---|---|---|---|
| Network capex per connection | ~$29B / ~579M | **~$50/connection/yr** | [DERIVED] |
| Network (capex + opex) per connection | (~$29B + ~$53B) / ~579M = ~$82B / 579M | **~$142/connection/yr** | [DERIVED] |
| Total infra (capex + opex, incl. towers) per connection | (~$63B + ~$53B) / ~579M = ~$116B / 579M | **~$200/connection/yr** | [DERIVED] |
| Network (capex + opex) per HUMAN PHONE subscriber | ~$82B / ~375M | **~$219/sub/yr** | [DERIVED] |
| Total infra (capex + opex) per HUMAN PHONE subscriber | ~$116B / ~375M | **~$309/sub/yr** | [DERIVED] |
| Cross-check vs GSMA sourced capex/connection | EUR35 ~= ~$38/connection/yr capex | consistent with the ~$50 derived capex line | [FACT anchor] |

[DERIVED, this doc S2, from global COMM-018/019/020/029.] So the ground CELLULAR cost to build, run, and maintain the network, spectrum excluded, is:

> **~$140-200 per connection per year (all-in network-plus-infrastructure), or ~$220-310 per human phone subscriber per year.** The capex-only slice is ~$50/connection/yr, corroborated by the GSMA's sourced ~EUR35/connection.

Two important framings of this number:

1. **This is the AVERAGE-network cost, which in a mature dense network IS close to the marginal/served cost**, because the plant is built and the incremental subscriber rides sunk towers. It sits alongside the margins doc's fixed-broadband defend-floor of ~$84-180/sub/yr [global COMM-096] and the mobile marginal of ~$0.50-1.50/GB [global COMM-098] as the DENSE-SERVED regime cost. The two are consistent: ~$140-235/sub/yr network-average mobile vs ~$84-180/sub/yr fixed marginal are the same order of magnitude, both far below ARPU (~$600-680/yr mobile, ~$880/yr fixed), which is why the incumbent has ~30-40 points of EBITDA headroom to defend [global COMM-099].

2. **It is NOT the cost in the sparse regime.** This ~$140-310/sub/yr is the cost where ~248,050 macro sites already cover dense and suburban America at high subscribers-per-site. Push into truly sparse territory (few subscribers per site, a fresh build required) and the per-subscriber number explodes, which is Section 3.

### 2.5 The per-GB and per-Mbps translation (served regime)

Completing the unit set for the served regime:

| Axis | Ground cellular (served) | Arithmetic | Tag |
|---|---|---|---|
| Per subscriber per year | **~$140-310/sub/yr** | S2.4 | [DERIVED] |
| Data per connection per year | **~228 GB/connection/yr** (~19 GB/mo) | 132 trillion MB / 579M connections | [DERIVED] |
| Per GB (network all-in) | **~$0.62/GB** | ~$82B / 132 trillion MB | [DERIVED] |
| Per GB (marginal, carried) | mobile ~$0.50-1.50/GB; fixed <$0.01/GB | margins doc | [FACT] |
| Per Mbps of typical speed | **~$0.8-1.3 per sub/yr per Mbps** | ~$200/yr / ~175 Mbps | [DERIVED] |

[DERIVED, this doc, from global COMM-006 (132 trillion MB), COMM-020, COMM-029.] The ~$0.62/GB all-in network cost-per-GB is a clean independent cross-check: it lands right in the middle of the margins doc's mobile marginal ~$0.50-1.50/GB [global COMM-096], confirming the build. It is ~2x the analyst's ~$0.30/GB terrestrial-5G figure [global COMM-147], the difference being all-in (capex+opex, average) vs marginal-incremental, which is the expected gap.

---

## 3. Question 3: The Sparse Regime (The Matched Baseline)

The served regime above is the WRONG comparison for a satellite-cellular play, because the satellite competes where the ground is unbuilt. The matched baseline is the FRESH BUILD cost per subscriber in sparse territory, which the cost-ratio doc already pinned and which this doc carries (it does not re-derive the annualization):

| Sparse regime, ground cost per subscriber per year (annualized fresh build) | Value | Tag | Source |
|---|---|---|---|
| Suburban fiber (the crossover zone) | **~$490/sub/yr** | [DERIVED] | global COMM-100, cost-ratio file |
| Rural fiber (low) | **~$875/sub/yr** | [DERIVED] | global COMM-100 |
| Rural fiber (high) | **~$1,540/sub/yr** | [DERIVED] | global COMM-100 |
| Extreme remote tail | **~$44,500/sub/yr** | [DERIVED] | global COMM-100 |

[Carried.] These annualize the fiber per-passing capex ($3,000-6,000 rural, up to ~$200-230k tail) over a ~25-year asset life at a ~9% capital charge, divided by the ~46% take-rate, plus ~$150/sub/yr opex [global COMM-100/102]. The cellular fresh-build analogue is the same shape: a new rural macro site is ~$100-300k all-in [global COMM-005], and a fresh cell build to truly unserved territory carries the same density penalty (longer backhaul, power provisioning, ~1-3 subscribers worth of demand under a site that costs the same as an urban one). The per-passing/per-site capex is the cost driver in BOTH fixed and cellular fresh builds, which is why the cost-ratio doc uses fiber as the primary fresh-build proxy and notes cellular tracks it.

**Why the two regimes differ by ~5-10x per subscriber.** It is entirely the subscribers-per-site (or subscribers-per-passing) denominator:

- Dense served: one macro site covers thousands of subscribers; the ~$250k site amortizes over a huge base, landing at the ~$140-310/sub/yr of Section 2.
- Sparse fresh build: one new site (or one fiber passing) covers a handful of subscribers (or one home); the same ~$250k site amortizes over ~1-10 subscribers, landing at the ~$875-44,500/sub/yr of this section.

[DERIVED, the structural reason, consistent across global COMM-100 and the cellular per-site figures.] This is the regime split the founder named precisely: **dense urban is cheap per subscriber (many subscribers per site, incumbent marginal cost ~$84-310/sub/yr); sparse rural is expensive per subscriber (few subscribers per site, fresh build ~$875-44,500/sub/yr).** The space cost (~$480-680/sub/yr, flat everywhere) sits BETWEEN them: above the dense-served floor, below the sparse fresh-build cost. That is the entire competitive map.

---

## 4. Question 4: The Niche Where Space Could Undercut

The ground per-subscriber cost crosses above the ~$480-680/sub/yr space cost wherever (a) a fresh build is required (no incumbent marginal floor) and (b) density is low enough that the fresh-build per-subscriber cost exceeds ~$480-680/yr. From Section 3, that crossover sits around the **dense-suburban fringe** (~$490/sub/yr fresh build ~= the bottom of the space range) and everything sparser than it [global COMM-103, COMM-117]. The niche, sized from the corpus:

### 4.1 The geographic / market niche

| Niche | Size | Tag | Source |
|---|---|---|---|
| US broadband deserts (no/limited terrestrial) | ~6% of US households ~= **~8M HH** | [FACT %] | global COMM-072, rural file |
| US rural-with-weak-terrestrial | ~12% of US households | [FACT %] | global COMM-073 |
| US satellite-addressable rural fringe (combined) | **~8-13M households** | [ESTIMATE] | rural file S3.1 |
| Developed-world (incl. US) addressable rural fringe | **~30-45M households** | [ESTIMATE, count softer than % inputs] | global COMM-075 |
| OECD rural fixed-broadband (30 Mbps) coverage gap | ~21.5% (78.5% rural vs 92.3% overall) | [FACT] | global COMM-074 |
| Global mobile COVERAGE gap (no signal at all) | **~300M people (~4%)** | [FACT] | global COMM-021/062 |
| Global mobile USAGE gap (covered but offline, income-limited, NOT space-addressable) | ~3.1B people | [FACT] | global COMM-022/063 |

[Carried.] The crucial distinction the rural docs draw: the **coverage gap (~300M people)** is the space-addressable supply problem (no infrastructure reaches them); the **usage gap (~3.1B people)** is an income problem (covered but cannot pay), which a satellite does NOT solve. The niche is the coverage gap plus the high-cost fringe of served markets where the fresh-build cost exceeds the space cost, NOT the 3.1B usage gap.

### 4.2 Narrowing to satellite-CELLULAR specifically

The niche above is the broad "space beats fresh ground build" fringe (fixed + mobile). For satellite-CELLULAR (direct-to-cell to an unmodified phone) specifically, it narrows to where the demand is a PHONE, not a home pipe, because D2C cannot serve home-broadband data volumes (~360-850 GB/mo) from a shared beam at ~$5-9/GB [FACT, global COMM-147, D2C file]:

- **Maritime, aviation, off-grid mobility** (the phone moves; no fixed alternative exists by definition).
- **Emergency / continuity** (the tower is down or out of range; the safety-net is the product).
- **Rural / remote everyday coverage** where a phone is the only device (single-occupant, light-usage rural homes that a good-enough D2C phone collapses, plus the ~8-13M US / ~30-45M developed-world fringe households whose home connection is thin enough to substitute).
- **The thin-edge home** that the cannibalization analysis identifies: where a home is rural/remote, single-occupant, light-usage, or already satellite-served, a good-enough D2C phone can collapse the dedicated home line [global COMM-159 area, D2C file]. This is self-limiting to the same fringe where space already wins on cost.

[Carried/synthesized.] The near-term served revenue for this D2C niche is ~$12-14B ex-China by ~2030-31 (Omdia/Juniper/ABI/Mordor convergence) [global COMM-152 area, D2C file], an order of magnitude below the ~$129B fixed-broadband-class served slice, but the ADDRESSABLE base (~5.5B out-of-coverage-capable phones) is far larger and the niche grows as spectrum-and-satellite gains push the per-GB cost gap down.

### 4.3 The constellation-economics gate (no verdict)

The founder's posited constellation: **~$2-3M per satellite x a few hundred satellites ~= ~$0.5B**, serving a coverage-driven subscriber base. The question is whether the ground per-subscriber cost in the niche is high enough that this constellation undercuts it. Two facts bound the answer, both carried from the corpus, neither a verdict:

1. **In the niche (sparse fresh build), the ground cost is ~$875-44,500/sub/yr** (Section 3). A space cost ANYWHERE below that wins on cost. So the niche is genuinely cost-advantaged for space, by the same ~1.3-3.2x rural to ~65-90x tail the cost-ratio doc found [global COMM-100].

2. **But the space cost is not fixed at ~$480-680/sub/yr for a small constellation.** That figure is Starlink's DISCLOSED actual at ~10M subscribers spreading a ~$6-8B/yr fixed fleet cost [global COMM-091]. The space cost stack is fixed-cost-dominated, so per-subscriber cost is driven by the DENOMINATOR (subscribers), not the per-satellite price [global COMM-091, COMM-103]. A few-hundred-satellite, ~$0.5B constellation has a far smaller fixed cost than Starlink's fleet, but it also has a far smaller subscriber base, and whether its per-subscriber cost lands below the ~$875-44,500/sub/yr niche-ground cost depends entirely on how many coverage-driven subscribers it captures. The corpus's standing finding: "space delivery is cheap per subscriber only at SpaceX scale, and expensive per subscriber at any smaller scale" [global COMM-091, conservative new-entrant case].

> **The honest statement of the niche, no verdict:** the ground per-subscriber cost is high enough for space to undercut it precisely in the sparse, remote, unserved fringe (~8-13M US households, ~30-45M developed-world, the ~300M-person coverage gap), and for satellite-CELLULAR specifically in the phone-shaped slice of that fringe (maritime, aviation, off-grid mobility, emergency, thin-edge rural). Whether a ~$0.5B / few-hundred-satellite constellation actually undercuts the niche-ground cost is a denominator (scale) question this doc does not answer: it wins if its coverage base is large enough to spread the fixed cost below the ~$875-44,500/sub/yr ground fresh-build cost, and that subscriber-base sizing against the entrant-specific fixed cost is the unmodeled gap the thesis must close [global COMM-091, OQ on new-entrant unit economics].

---

## 5. Open Questions

1. **A clean operator-disclosed per-subscriber TOTAL cost.** Section 2.4's ~$140-310/sub/yr is this doc's arithmetic on aggregate capex/opex divided by connection counts (the corpus's standing gap, global COMM-032, cellular OQ4). A sourced operator benchmark (total cost / subscriber, or a clean capex+opex per net-add) would replace the derivation. The GSMA EUR35/connection is only the CAPEX slice.
2. **The human-phone-subscriber denominator.** The ~350-400M human-phone-subscriber count is estimated from carrier postpaid+prepaid phone bases; the exact split of the 579M connections into phones vs IoT/tablets/cars/FWA is not cleanly disclosed and swings the per-subscriber figure by ~50% (579M vs 375M denominator).
3. **The entrant-specific (non-Starlink) space cost per subscriber.** The ~$480-680/sub/yr is the MATURE incumbent at ~10M subscribers. The constellation the founder posits (~$0.5B, few-hundred satellites) has a different fixed cost and a different (smaller, coverage-driven) subscriber base; converting "multiples higher per subscriber at small scale" into a number for THIS constellation, against THIS niche-ground cost, is the single unmodeled gap that decides Question 4 (the cost-ratio doc's OQ3, carried).
4. **The crossover density.** Section 3 places the fresh-build-vs-space crossover around the dense-suburban fringe (~$490/sub/yr). The exact homes-per-mile (or subscribers-per-site) at which the fresh CELLULAR build crosses above ~$480-680/sub/yr is the number that sizes the cost-advantaged niche, and it needs the density-cost model the corpus already flags (global COMM-100 OQ1, broadband-deployment OQ3).
5. **The D2C per-GB at next-gen spectrum.** The ~$5-9/GB D2C figure predates the EchoStar ~65 MHz and Gen2 ~100 Gbps satellites; a re-derived $/GB at full spectrum tells how far the niche widens (whether D2C ever serves more than the thin edge), bearing on Section 4.2 (carried from the D2C doc's OQ1).

---

## 6. Sources

*Ground cellular cost (this doc's own build), carried from the base docs (each holds its own 2+ source citations inline)*
- [research/economics/comms_cellular_5g_deployment_economics.md](./comms_cellular_5g_deployment_economics.md) (capex intensity, per-site, RAN/backhaul split, US ~$29-30B capex + ~$53B opex, ~248,050 sites, ~579M connections, GSMA EUR35/connection)
- [research/economics/comms_incumbent_margins_competitive_floor.md](./comms_incumbent_margins_competitive_floor.md) (fixed defend-floor ~$84-180/sub/yr, mobile ~$0.50-1.50/GB, fixed <$0.01/GB, EBITDA headroom)
- [research/economics/comms_us_cellular_market.md](./comms_us_cellular_market.md) (carrier ARPUs ~$50-57/mo postpaid phone, postpaid phone subscriber counts, 132 trillion MB US mobile data)
- [research/economics/comms_broadband_deployment_economics.md](./comms_broadband_deployment_economics.md) (fixed fresh-build passing/connect/take-rate, the per-passing cost driver)

*Space numerator and ratio, carried*
- [research/economics/comms_space_supply_cost.md](./comms_space_supply_cost.md) (space all-in ~$480-680/sub/yr, ~$200-260 space-specific, ~$0.05-0.30/GB rising at density, scale-is-the-game)
- [research/economics/comms_direct_to_cell.md](./comms_direct_to_cell.md) (D2C ~$5-9/GB vs ~$0.30/GB terrestrial, ~20x; the density inversion; ~$12-14B near-term served revenue; ~5.5B addressable devices)
- [research/economics/comms_ground_vs_space_cost_ratio.md](./comms_ground_vs_space_cost_ratio.md) (the two-flavor ratio; ~$875-1,540/sub/yr rural fresh build; crossover ~suburban fringe)
- [research/direct_communication/dtc_per_phone_rate_and_latency.md](../direct_communication/dtc_per_phone_rate_and_latency.md) (the ~20-30 Mbps single-phone operating point; ~25 Mbps single-phone clears; AST BW3 ~21 Mbps demo)

*Niche sizing, carried*
- [research/economics/comms_rural_fringe_sizing.md](./comms_rural_fringe_sizing.md) (US ~8-13M HH, developed-world ~30-45M HH, coverage vs usage gap)
- [research/economics/comms_global_regional_market.md](./comms_global_regional_market.md) (global ~9.2B mobile subscriptions, ~300M coverage gap, ~3.1B usage gap)

*Unit framing, carried*
- [research/synthesis/comms_framework_synthesis.md](../synthesis/comms_framework_synthesis.md) (the density-aware unit: cost per subscriber per year and per GB; space cost-per-subscriber rises with density)
- [research/SOURCE_INDEX.md](../SOURCE_INDEX.md) (the global claim ledger this doc cites by `global COMM-NNN`)

---

## 7. Confidence

- **The unit recommendation (Q1): medium-high.** That per-subscriber-per-year is the right primary unit (both sides report it, the corpus standardizes on it) and that per-Mbps misleads (it prices peak speed in served areas, not coverage in unserved ones) both follow directly from which numbers are auditable and from the density inversion, which is well-established [global COMM-172, COMM-108]. The per-Mbps ~16-34x penalty is clean arithmetic; calling it a "trap" is an interpretation, but a well-grounded one.
- **The served-regime ground floor (Q2): medium-high carried, medium on this doc's build.** The ~$84-180/sub/yr fixed defend-floor and ~$0.50-1.50/GB mobile marginal are carried from the margins doc at its original confidence [global COMM-096/098]. This doc's own ~$140-310/sub/yr network-average build is DERIVED arithmetic on sourced aggregates, denominator-sensitive, but it cross-checks cleanly against the GSMA EUR35/connection capex anchor and the ~$0.62/GB all-in figure lands inside the sourced mobile marginal range, which raises confidence in the build.
- **The sparse-regime cost (Q3): medium carried.** The ~$875-1,540/sub/yr rural and ~$44,500/sub/yr tail are carried from the cost-ratio doc, which annualizes with a stated ~25-yr life / ~9% capital charge; reasonable alternative assumptions would RAISE the ground number and WIDEN space's niche advantage, so the carried figures are conservative against space [global COMM-100/102].
- **The niche (Q4): medium.** The ~8-13M US / ~30-45M developed-world household counts are carried from the rural-fringe doc, where the counts are softer than the percentage inputs [global COMM-075]. The ~300M coverage gap is FACT [global COMM-021]. The constellation-economics gate is explicitly left unmodeled (the entrant-specific cost-per-subscriber is the standing gap), so Q4 identifies the niche and the crossover but renders no verdict on whether the posited ~$0.5B constellation clears it.

---

## 8. Claims Ledger

*New hard claims for the catalog/reconciliation step to ingest. Each lists value, status, and source. IDs COMM-521..534 (next free contiguous block above the global max; COMM-493..520 reserved by [dtc_data_rate_vs_spectrum.md](../direct_communication/dtc_data_rate_vs_spectrum.md), 493..512 used). Catalog rows for LIBRARY.md / RESEARCH_TRACKER.md / SOURCE_INDEX.md are returned to the lead, not edited here. This doc is not committed by this pass.*

| COMM- id | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-521 | The recommended comparison UNIT for space-vs-ground cellular: cost per subscriber per year (primary), cross-checked per GB (the density-honest secondary); per Mbps of typical speed misleads and is shown only to be rejected | $/sub/yr primary; $/GB secondary; reject $/Mbps | DERIVED (interpretation) | this doc S1; from [comms_space_supply_cost.md](./comms_space_supply_cost.md) (auditable $/sub/yr), [synthesis/comms_framework_synthesis.md](../synthesis/comms_framework_synthesis.md) (global COMM-172) |
| COMM-522 | Why per-Mbps-of-typical-speed misleads: it flatters ground by ~16-34x because it prices PEAK SPEED in served areas, not COVERAGE in unserved ones (ground typical speed is 0 where the satellite competes, so the ground per-Mbps is undefined there) | ground ~$0.8-1.3 vs space ~$16-34 per sub/yr per Mbps (~16-34x); but undefined in the unserved fringe | DERIVED | this doc S1.3; ground ~$200/yr / ~175 Mbps, space ~$580/yr / ~25 Mbps |
| COMM-523 | Space-side single-phone operating point (the unit's space input): ~20-30 Mbps to a phone | ~20-30 Mbps (~25 Mbps single-phone clears a ~25 m^2 aperture on owned spectrum; AST BW3 ~21 Mbps single-device demo) | FACT/DERIVED (carried) | [dtc_per_phone_rate_and_latency.md](../direct_communication/dtc_per_phone_rate_and_latency.md) (global COMM-278/362) |
| COMM-524 | US wireless ground cellular CAPEX stack, spectrum excluded: ~$29-30B/yr network capex; ~$63B/yr total infra (incl. towers); RAN ~55-65% of capex; capex intensity ~14-19% of service revenue | ~$29-30B network / ~$63B infra per year | FACT (carried) | [comms_cellular_5g_deployment_economics.md](./comms_cellular_5g_deployment_economics.md) (global COMM-018/019/009/001) |
| COMM-525 | US wireless ground cellular OPEX: ~$53B/yr network opex (site lease, power, backhaul, maintenance, ops); energy ~20-40% of opex; RAN ~73% of network energy | ~$53B/yr network opex | FACT (carried) | [comms_cellular_5g_deployment_economics.md](./comms_cellular_5g_deployment_economics.md) (global COMM-020/021/023) |
| COMM-526 | Ground cellular cost per CONNECTION per year, network all-in (capex + opex), spectrum excluded | ~$142/connection/yr ((~$29B + ~$53B) / ~579M); ~$200/connection/yr including towers/infra | DERIVED | this doc S2.4; from global COMM-018/019/020/029 |
| COMM-527 | Ground cellular cost per HUMAN PHONE subscriber per year, network all-in (capex + opex), spectrum excluded | ~$220-310/sub/yr (~$82-116B / ~350-400M phone subs) | DERIVED (denominator-sensitive, flagged) | this doc S2.4; from carrier postpaid+prepaid phone counts in [comms_us_cellular_market.md](./comms_us_cellular_market.md) |
| COMM-528 | Capex-only cross-check: derived ground capex per connection ~$50/yr corroborates the sourced GSMA ~EUR35/connection capex anchor | ~$50/connection/yr capex (~= GSMA ~EUR35) | DERIVED + FACT anchor | this doc S2.4; global COMM-027 (GSMA), COMM-032 (derived) |
| COMM-529 | Ground cellular data per connection ~228 GB/yr (~19 GB/mo); ground all-in network cost-per-GB ~$0.62/GB (cross-checks inside the sourced mobile marginal ~$0.50-1.50/GB) | ~228 GB/connection/yr; ~$0.62/GB all-in | DERIVED | this doc S2.5; from 132 trillion MB (global COMM-006) / 579M; vs global COMM-096 |
| COMM-530 | The DENSE-SERVED regime ground cost per subscriber (the cheap regime, many subs per site): fixed defend-floor ~$84-180/sub/yr; mobile network all-in ~$140-310/sub/yr; both far below ARPU (~30-40 pts EBITDA headroom) | ~$84-310/sub/yr served | DERIVED + FACT (carried) | this doc S2-S3; global COMM-096 (fixed floor), this doc COMM-527 (mobile) |
| COMM-531 | The SPARSE fresh-build regime ground cost per subscriber (the expensive regime, few subs per site): ~$875-1,540/sub/yr rural, ~$44,500/sub/yr extreme tail (annualized; cellular new macro ~$100-300k/site tracks fiber's per-passing driver) | ~$875-44,500/sub/yr sparse | DERIVED (carried) | this doc S3; global COMM-100 (cost-ratio), COMM-005 (per-site) |
| COMM-532 | The two-regime split is denominator-driven (subscribers-per-site), not a difference in site cost: the same ~$250k macro amortizes over thousands of subs dense vs ~1-10 sparse, a ~5-10x per-subscriber swing; space cost (~$480-680/sub/yr, flat) sits BETWEEN the two regimes | dense ~$84-310 < space ~$480-680 < sparse ~$875-44,500 (all per sub/yr) | DERIVED (interpretation) | this doc S3; global COMM-091 (space), COMM-100 |
| COMM-533 | The niche where ground per-subscriber cost exceeds the ~$480-680/sub/yr space cost: the sparse/remote/unserved fringe (~8-13M US HH, ~30-45M developed-world HH, ~300M-person global coverage gap); the ~3.1B usage gap is an income problem NOT space-addressable | US ~8-13M HH; developed ~30-45M HH; ~300M coverage gap | ESTIMATE/FACT (carried) | this doc S4; global COMM-072/073/075/021 (rural + global files) |
| COMM-534 | The satellite-CELLULAR sub-niche (phone-shaped demand only, since D2C cannot serve home data volumes at ~$5-9/GB): maritime, aviation, off-grid mobility, emergency/continuity, thin-edge rural home; ~$12-14B near-term D2C served revenue ex-China; whether a ~$0.5B / few-hundred-sat constellation undercuts the niche-ground cost is an UNMODELED denominator (scale) question, NO verdict | phone-shaped fringe; ~$12-14B near-term; scale-gated, no verdict | DERIVED/ESTIMATE (carried) + UNKNOWN (the gate) | this doc S4.2-S4.3; global COMM-147 ($5-9/GB), D2C served-revenue, COMM-091 (scale gate) |

---

*This doc EXTENDS the existing ground-cost corpus (it does not duplicate the two-flavor ratio or re-derive the space numerator); it adds the unit recommendation, the ground-cellular per-subscriber build with the per-Mbps/per-GB translation, and the niche. New claims COMM-521..534. No verdict. Not committed by this pass; never rm (mv to ~/.Trash only); no Claude/Co-Authored-By attribution in any commit; no em-dashes.*
