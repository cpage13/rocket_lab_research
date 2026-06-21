# Direct-to-Cell (Satellite-to-Phone): Market, Spectrum, Capacity Limits, and the Cannibalization Question

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:**
- [`research/economics/comms_us_cellular_market.md`](./comms_us_cellular_market.md) (the US carrier financials, the cable-MVNO precedent for renting a non-owner onto a carrier network, and the first pass at the D2C duopoly: Starlink 16M users / AST 2.8B reach). This doc takes those carrier and market anchors as given and goes deep on the D2C product, spectrum, physics, and unit economics, which that doc explicitly deferred.
- [`research/economics/comms_space_tam_claims.md`](./comms_space_tam_claims.md) (the AST ~$1.1T cited TAM vs the ~$3-97B BofA bottoms-up, the Morningstar ~$129B served slice, and the ~$2.6-13.8B near-term D2D segment forecasts). This doc does not re-derive those TAMs; it adds the two newer independent forecast houses (Omdia, Juniper), sizes D2C ex-China against fixed broadband, and resolves the "is D2C the larger market" question the lead asked.
- [`research/economics/comms_ground_vs_space_cost_ratio.md`](./comms_ground_vs_space_cost_ratio.md) (the two-flavor ground-vs-space cost ratio, and specifically OQ5: "mobile is the narrowest gap; is direct-to-cell the served sub-market where space is least disadvantaged on cost?"). This doc answers that open question directly with the D2C per-GB cost data.

> **Reading guide.** Every hard number is tagged **[FACT]** (sourced, 2+ independent sources), **[FACT, single-source]** (one source only), **[ESTIMATE]** (third-party model or sizing), or **[DERIVED]** (my own arithmetic on cited inputs). China is **excluded** from all market totals and appears only as a labelled aside. No verdict on the Rocket Lab business is rendered; this is a neutral market-and-physics base doc for the lead market of the comms model.

---

## Summary

**Direct-to-cell (D2C, also "direct-to-device"/D2D, or in 3GPP terms "supplemental coverage from space"/SCS) lets an ordinary unmodified smartphone connect to a satellite when no tower is in range.** It is the lead market of the communications model, and this doc treats it thoroughly. Five findings:

1. **The two pure-play benchmarks have diverged into opposite architectures.** AST SpaceMobile builds a few enormous satellites (Block 2 arrays ~223 m², up to ~2,500-2,800 cells, ~120 Mbps/cell, ~20.3 km narrowest beam footprint, ~56 Gbps theoretical per satellite) [FACT]. Starlink Direct to Cell adds modest D2C payloads to its large LEO fleet (650+ D2C satellites by early 2026, ~3.1 Mbps/beam on current spectrum rising to ~15-18 Mbps/beam with full holdings, targeting 150 Mbps/user peak next-gen) [FACT]. Big-dish-few-birds versus small-payload-many-birds, with the same physics ceiling.

2. **The spectrum model is shifting, and this is the most important update to the prior library framing.** The earlier docs said the players "use MNO partner licensed spectrum, not their own." That was true in 2024-25 and is still partly true (both roam onto carriers' terrestrial cellular bands via SCS authority). But in 2025-26 both have moved aggressively to secure their OWN dedicated D2D spectrum: SpaceX bought EchoStar's AWS-4 + H-Block (~65 MHz incl. AWS-3) for ~$17B (May 2026) [FACT], and AST secured long-term (80+ year) access to up to ~45 MHz of lower mid-band via Ligado [FACT]. The model is moving from "rent the carrier's spectrum" toward "own dedicated satellite spectrum + roam on the carrier's as a supplement."

3. **The capacity ceiling is the whole story, and it is set by Shannon and beam geometry, not by the satellite count.** A D2C beam covers a ~20-1,000+ km² patch and shares one finite block of MHz across every phone under it. The result: satellite NTN delivery costs ~$5-9/GB versus ~$0.30/GB for terrestrial 5G, roughly **20x more expensive per GB** [FACT, single analyst, Joe Madden/Mobile Experts]. This is exactly the "mobile is the narrowest but still real gap" that the cost-ratio doc's OQ5 flagged: D2C is the served sub-market where space is *least* disadvantaged, but it is still well above the terrestrial marginal floor on a per-GB basis. Capacity-per-user is the binding constraint, and it gets worse with user density, the opposite of terrestrial.

4. **Cannibalization of fixed/home broadband is real at the messaging/coverage layer and structurally blocked at the broadband layer, for now.** Today D2C is a thin coverage supplement (T-Satellite data is "hundreds of kbps at best" in late 2025) priced at ~$10/month [FACT]. It does not work indoors or in dense urban areas and "will likely never" do so [FACT], which is where ~80%+ of mobile data is consumed. So D2C cannot replace a home connection on capacity grounds today. The forward question (5G/6G speeds making the phone "good enough" to drop the home line) is a capacity-physics question, not a demand question: it requires closing a ~20x per-GB cost gap and a beam-saturation ceiling, which next-gen spectrum narrows but does not eliminate. The honest read: D2C cannibalizes the *thin rural/edge* home connection and the standalone satellite-messaging market, not the dense-market home broadband line, on any near-to-medium horizon.

5. **Is D2C larger than fixed broadband ex-China? On served-revenue, not yet; on addressable reach and strategic optionality, plausibly yes over a 10-year horizon.** Near-term D2C service revenue forecasts cluster at **~$12B by 2030** (Omdia, 411M monthly active users) and **133M monthly active users by 2031** (Juniper, with usage "lower than anticipated") [FACT, two independent houses]. That is small versus the ~$129B Morningstar served-connectivity slice that is mostly fixed-broadband-class. BUT the D2C *addressable base* (every one of ~5.5B out-of-coverage-capable phones, ~$1.1T cited ceiling) is far larger than the fixed-broadband household base, and the strategic case for "larger" rests on D2C eventually absorbing part of the home-broadband wallet as speeds rise. The defensible statement: **D2C is the larger market by addressable devices and by 10-year optionality, but the smaller market by near-term served revenue; whether it overtakes fixed broadband depends entirely on whether the per-GB capacity gap closes.**

**Confidence: medium-high** on the two benchmarks' specs and the spectrum deals (primary filings + 2+ trade sources each); **medium-high** on the ~20x per-GB gap as the binding constraint (single named analyst on the exact figure, but corroborated in direction by every capacity source); **medium** on the forecasts (independent research houses, stated-assumption models that diverge); **medium** on the cannibalization read (a physics-bounded judgment, not a measured outcome).

---

## 1. The Two Pure-Play Benchmarks

The D2C field has resolved into two pure-play architectures that bracket the design space. A third tier (Apple/Globalstar, Lynk, Skylo, Amazon Leo's planned D2D) exists but the two below are the benchmarks the model needs.

### 1.1 Architecture: opposite bets, same physics

| Dimension | AST SpaceMobile | Starlink Direct to Cell (SpaceX) |
|---|---|---|
| Core bet | Few **enormous** satellites, huge phased-array aperture | Many **modest** D2C payloads on the existing LEO fleet |
| Satellite array size | Block 1 ~64 m²; Block 2 ~223 m² (~2,400 sq ft) [FACT] | Small payload added to ~Gen2 bus; "smaller antenna approach" [FACT] |
| Satellites (status, 2026) | 6 BlueBird Block 1 up; Block 2 launching; targeting 45-60 by end-2026 [FACT] | 650+ D2C satellites by early 2026; toward thousands [FACT] |
| US carrier partner(s) | AT&T, Verizon, FirstNet [FACT] | T-Mobile (T-Satellite brand) [FACT] |
| Listing | Public, NASDAQ ASTS (~$46B mid-2026 mkt cap, prior doc) | Inside SpaceX (private; IPO filed 2026) |

Sources: [AST Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/); [AST BlueBird 6 launch (BusinessWire)](https://www.businesswire.com/news/home/20251222922862/en/AST-SpaceMobile-Announces-Successful-Orbital-Launch-of-BlueBird-6-the-Largest-Commercial-Communications-Array-Ever-Deployed-in-Low-Earth-Orbit); [NewSpaceTracker, Direct-to-Smartphone Satellites](https://newspacetracker.com/articles/direct-to-smartphone-satellites/); [IEEE/Nokia 6G NTN context](https://www.nokia.com/blog/6g-will-put-satellite-connectivity-in-every-smartphone-and-device/).

The reason the architectures differ is a single physics trade. A bigger aperture makes a **narrower** beam, which concentrates power and spectrum on a smaller patch of ground, raising capacity per user. AST chases that with one giant array per satellite; SpaceX chases it with sheer satellite count (more satellites means each can use tighter beams over fewer users). **Both are buying the same thing, beam tightness, by different means**, because beam tightness is what sets capacity per user (Section 3).

### 1.2 AST SpaceMobile: capacity and reach

| Metric | Value | Status | Source basis |
|---|---|---|---|
| Processing bandwidth per satellite | 10 GHz (Block 2; ~10x Block 1) | [FACT] | AST; Wikipedia; Gunter's Space Page |
| Peak speed per coverage cell | ~120 Mbps (Block 1); ~200 Mbps (Block 2 peak to phone) | [FACT] | AST Next-Gen BlueBird; SatNews |
| Cells (beams) per satellite | 2,000+ active; Block 2 designed for ~2,500 adjustable beams (one analyst cites 2,800) | [FACT] / [FACT, single-source 2,800] | AST; arxiv 2506.18672; Fierce |
| Bandwidth per downlink beam | over 40 MHz (UHF and L bands) | [FACT] | spacelaunchnow; arxiv 2506.18672 |
| Narrowest beam footprint (Block 2, 725 km) | ~20.3 km diameter, ~324 km² | [FACT, single-source] | arxiv 2506.18672 (spectrum-opportunities paper) |
| Theoretical capacity per satellite | ~56 Gbps (2,800 cells x 20 Mbps floor case) | [DERIVED] | Fierce (Madden); my arithmetic |
| US coverage cells (planned) | 5,600+ for ~nationwide US | [FACT, single-source] | SpaceNews / SEC 8-K |
| MNO agreements / reach | ~45-60 operators, ~3 billion (prior doc: 2.8B) subscribers | [FACT] | AST Q1 2026; prior library doc |
| 2025 revenue / 2026 guide | ~$70.9M actual; $150-200M guide | [FACT] | prior library doc; AST 8-K |

AST's pitch is that one Block 2 satellite, with ~2,500 beams each carrying 40 MHz at up to 120 Mbps, can light up a continent's worth of dead zones. The catch is in Section 3: 120 Mbps *per cell* is shared across everyone in a ~324 km² (best case) to far larger (typical) footprint, so per-user throughput collapses as soon as more than a handful of users share a cell.

### 1.3 Starlink Direct to Cell: capacity and reach

| Metric | Value | Status | Source basis |
|---|---|---|---|
| D2C satellites in orbit | 650+ (early 2026); "largest 4G network by coverage area" | [FACT] | SatelliteInternet.com; Via Satellite; basenor |
| Per-beam throughput, current spectrum | ~3.1 Mbps (PCS G Block, outdoor) | [FACT, single-source technical] | arxiv 2506.00283 (crowdsourced measurement) |
| Per-beam throughput, with H-Block added | ~6.2 Mbps; ~18.6 Mbps aggregate at full holdings | [FACT, single-source technical] | arxiv 2506.00283 |
| Per-user throughput, current | ~4 Mbps top (T-Satellite); data "hundreds of kbps at best" late 2025 | [FACT] | 5gstore; SatelliteInternet.com; basenor |
| Per-user peak target, next-gen | 150 Mbps download | [FACT] | 5gstore (SpaceX policy lead); SDxCentral |
| Concurrent-user illustration | ~100 beams x ~100 users x 1 Mbps = ~10,000 users/satellite | [ESTIMATE] | Mike Puchol model; SDxCentral |
| Next-gen satellite throughput | exceeding 100 Gbps down / 50 Gbps up; ~16x beams; ~100x data density vs Gen1 | [FACT] | SDxCentral; SatelliteInternet.com |
| Subscribers (US, via T-Mobile) | 16M unique / 10M monthly active (Mar 2026); targeting 25M end-2026 | [FACT] | prior library doc; Nokia/IEEE |
| Pricing (T-Satellite) | $10/month; free on top T-Mobile plans; $10 for AT&T/Verizon users | [FACT] | Via Satellite; rvmobileinternet; broadbandbreakfast |

Sources: [arxiv 2506.00283 Direct-to-Cell measurement](https://arxiv.org/html/2506.00283v7); [SDxCentral, Gen2 100x data density](https://www.sdxcentral.com/news/starlink-targets-25m-users-by-year-end-as-gen2-satellite-plan-promises-100x-data-density/); [5gstore, 150 Mbps target](https://5gstore.com/blog/2026/03/26/starlink-direct-to-cell-150mbps/); [Via Satellite, T-Mobile pricing](https://www.satellitetoday.com/connectivity/2025/04/25/t-mobile-cuts-price-on-starlink-satellite-messaging-service-to-start-in-july/); [basenor, FCC 4G/5G power](https://www.basenor.com/blogs/news/fcc-approves-spacex-starlink-direct-to-phone-5g-spectrum-deal).

The contrast is stark and instructive. Starlink's *current* D2C is far below AST's headline per-cell speed (single-digit Mbps per beam vs 120 Mbps per cell), because Starlink started with a tiny 2x5 MHz channel of PCS spectrum, while AST built around 40 MHz per beam and a giant aperture. Starlink's answer is not a bigger dish but **more spectrum and more satellites**: the EchoStar deal (Section 2) and Gen2's ~100 Gbps satellites are designed to close that gap by ~20x. The benchmarks are converging on the same throughput target (~150-200 Mbps peak to a phone) from opposite directions.

---

## 2. The Spectrum Model (the key update to the library)

Spectrum is the capacity ceiling. Per Shannon, capacity scales with bandwidth (MHz) and log of SNR; per the model's spine, capacity divided by customers is cost per subscriber. So **how much spectrum each player controls, and whether it owns or rents it, is the single biggest lever on D2C unit economics.** The prior library framing ("they use MNO partner licensed spectrum, not their own") needs an update.

### 2.1 The original model: roam on the carrier's terrestrial cellular bands (SCS)

The foundational mechanism is **Supplemental Coverage from Space (SCS)**: the FCC's framework (finalized 2024-25) lets a satellite reuse a terrestrial carrier's *already-licensed* low-band cellular spectrum to talk to phones, in the gaps where towers do not reach. The phone thinks it is on its normal network.

- **AST** got FCC commercial D2D authorization (April 2026) to use partner low-band: 700 MHz and 800 MHz via Verizon, AT&T, and FirstNet, plus Band 14 (FirstNet public-safety) [FACT]. It "combines our MNO partners' licensed frequencies with our own global spectrum management strategy" (AST's own words) [FACT].
- **Starlink** got SCS authority to use T-Mobile's PCS spectrum, plus an FCC power waiver (EPFD) enabling 4G/5G-class speeds; Viasat and EchoStar objected to the waiver [FACT].

Sources: [Via Satellite, FCC grants AST D2D authorization](https://www.satellitetoday.com/connectivity/2026/04/22/fcc-grants-ast-spacemobile-commercial-authorization-for-direct-to-device-service/); [SatNews, FCC grants AST 248-satellite + D2C](https://satnews.com/2026/04/21/fcc-grants-ast-spacemobile-authority-for-248-satellite-constellation-and-direct-to-cell-service/); [AST How It Works](https://ast-science.com/how-it-works/); [basenor, FCC 4G/5G power](https://www.basenor.com/blogs/news/fcc-approves-spacex-starlink-direct-to-phone-5g-spectrum-deal).

In this model the satellite operator owns no spectrum; it borrows the carrier's, and the carrier monetizes coverage it could never build to. This is the same wholesale logic as the cable MVNOs in [`comms_us_cellular_market.md`](./comms_us_cellular_market.md): a non-owner rides licensed capacity. Revenue is shared (AST has publicly described a 50/50 MNO revenue split in the prior TAM doc).

### 2.2 The 2025-26 shift: both players bought/leased their OWN dedicated D2D spectrum

This is the update. Roaming on a carrier's ~5-10 MHz of low-band caps capacity hard (Starlink's 2x5 MHz gave ~3.1 Mbps/beam). To break that ceiling, both moved to control dedicated mid-band:

| Deal | Spectrum | Price / terms | What it enables | Status |
|---|---|---|---|---|
| **SpaceX <- EchoStar** | ~65 MHz nationwide: 40 MHz AWS-4 + 10 MHz H-Block (+ 15 MHz AWS-3) | ~$17B (~$8.5B cash + ~$8.5B SpaceX stock) | Exclusive contiguous nationwide 5G-to-phone; FCC filing projects up to ~20x throughput vs current-gen (some coverage says "100x" vs first-gen *system*) | Approved May 12, 2026; license transfer ~Nov 30, 2027 [FACT] |
| **AST <- Ligado** | up to ~45 MHz lower mid-band; incl. ~40 MHz L-band MSS (80+ yr rights) + 5 MHz at 1670-1675 MHz | settlement/usage agreement; payments began Sep 30, 2025 | Premium mid-band for D2D in US + Canada, additive to partner low-band | Term sheet June 2025; subject to approvals [FACT] |

Sources: [DCD, SpaceX acquires EchoStar AWS-4/H-Block $17B](https://www.datacenterdynamics.com/en/news/spacex-acquires-echostars-aws-4-and-h-block-spectrum-for-17bn/); [Space.com, SpaceX $17B spectrum](https://www.space.com/space-exploration/satellites/spacex-buys-usd17-billion-worth-of-satellite-spectrum-to-beef-up-starlink-broadband-service); [EchoStar IR release](https://ir.echostar.com/news-releases/news-release-details/echostar-announces-spectrum-sale-and-commercial-agreement-spacex); [SatNews, AST 45 MHz Ligado](https://news.satnews.com/2025/06/15/ast-spacemobile-announces-settlement-term-sheet-facilitating-long-term-access-to-up-to-45-mhz-of-premium-lower-mid-band-spectrum-in-north-america-for-d2d-apps/); [BusinessWire, AST 45 MHz](https://www.businesswire.com/news/home/20250613700432/en/AST-SpaceMobile-Announces-Settlement-Term-Sheet-Facilitating-Long-Term-Access-to-up-to-45-MHz-of-Premium-Lower-Mid-Band-Spectrum-in-North-America-for-Direct-to-Device-Satellite-Applications).

> **The corrected framing for the model:** D2C spectrum is now a **hybrid**. The operators still roam on MNO-licensed terrestrial bands via SCS (the "borrow" model), but they have each spent billions to acquire dedicated satellite D2D spectrum (the "own" model) precisely because the borrowed slice is too thin to lift throughput past messaging. **For the capacity ceiling that drives cost-per-subscriber, the relevant number is the owned + leased dedicated spectrum (tens of MHz), not just the partner's low-band.** This matters for the Rocket Lab thesis: a new entrant cannot assume free carrier spectrum buys real capacity; the players who matter are buying spectrum outright, and that is a multi-billion-dollar entry cost. (This is consistent with the `rf_limited_service.md` Grain Management spectrum-leasing precedent the prior docs cite.)

### 2.3 Why spectrum is the binding ceiling (the Shannon link)

The measurement data makes the spectrum-to-capacity link concrete. Starlink's per-beam throughput scales almost linearly with bandwidth added: ~3.1 Mbps on 2x5 MHz (PCS G), ~6.2 Mbps with H-Block added, ~18.6 Mbps aggregate at full holdings [FACT, single-source technical: arxiv 2506.00283]. AST's ~120 Mbps/cell comes from ~40 MHz/beam, roughly 8x the bandwidth of Starlink's starting channel. **More MHz is the lever**, which is why ~$17B and ~$45 MHz changed hands. But spectrum is finite and shared with terrestrial users (the WIA notes suitable satellite frequencies are "scarce and costly," and sharing "has proved challenging") [FACT], so the ceiling is real even after the deals.

---

## 3. The Technical Limits: Capacity per Beam, Concurrency, and the Cost Floor

This is the section the cost-ratio doc's OQ5 asked for, and it is the most load-bearing for the model, because **capacity-per-user, not coverage, is what decides whether D2C can be more than a coverage supplement.**

### 3.1 The beam-saturation problem

A D2C beam is a single block of MHz shared by every phone in its footprint. The footprint is large: AST's *narrowest* Block 2 beam is ~20.3 km diameter (~324 km²) [FACT, single-source: arxiv 2506.18672], and typical/edge beams are larger; Starlink's beams cover comparable or larger patches. Compare that to a terrestrial cell, which covers a fraction of a km² in a city. So:

- **Per-cell capacity is fixed** (AST ~120 Mbps; Starlink single-digit-to-~18 Mbps per beam today). [FACT]
- **It divides across all concurrent users in a ~300-1,000+ km² patch.** One AST cell at 120 Mbps serving, say, 120 simultaneous users yields ~1 Mbps each; serving 1,200 yields ~100 kbps each. [DERIVED]
- **Density makes it worse, not better.** Terrestrial networks add capacity by adding towers (cells shrink, capacity per km² rises). A satellite cannot shrink its beam below its aperture-and-altitude limit, so packing more users under one beam only divides the same pie thinner. This is the structural inversion the TAM and cost docs both flagged: **satellite cost-per-user rises with density; terrestrial falls.** [FACT, corroborated across Morningstar, WIA, Madden]

### 3.2 The cost floor: ~$5-9/GB vs ~$0.30/GB (the answer to OQ5)

The cleanest single expression of the limit, from telecom analyst Joe Madden (Mobile Experts):

> Satellite NTN delivery costs **~$5 to $9 per GB**, versus **~$0.30 per GB** for terrestrial 5G, **roughly 20x higher**. With only ~60 satellites, "true broadband (video streaming) would be impossibly expensive because one user would be taking the entire capacity." [FACT, single named analyst]

Sources: [Fierce, AST and the problem of delivering broadband from space](https://www.fierce-network.com/wireless/ast-spacemobile-and-problem-delivering-broadband-space); [Fierce, setting realistic expectations on satellite phones (Madden)](https://www.fierce-network.com/wireless/setting-realistic-expectations-satellite-phones-madden).

**This directly answers the cost-ratio doc's OQ5.** That doc found mobile is the served sub-market where the space-vs-ground per-GB gap is narrowest (space network-average ~$0.05-0.30/GB can sit near the mobile ~$0.50-1.50/GB incumbent floor). The D2C-specific data refines it: at the *beam-saturated D2C delivery* level the cost is ~$5-9/GB, well above both the terrestrial 5G cost (~$0.30/GB) and the incumbent mobile marginal floor. So the precise finding is:

> **D2C is the served sub-market where space is least disadvantaged on *coverage value* (it reaches phones nothing else can), but on raw *cost per GB* it is still ~20x above terrestrial. Space wins D2C on the dollars only where there is no terrestrial alternative at all (the dead-zone/edge), not in served territory where a tower already carries the GB for a fraction of a cent.** This is the mobile-specific confirmation of the cost doc's central asymmetry.

The cost gap narrows as spectrum and satellite count rise (the EchoStar ~20x throughput uplift cuts $/GB materially), but it does not invert: the beam-sharing physics keeps satellite $/GB structurally above terrestrial in any area a tower can serve.

### 3.3 Capacity per satellite, in aggregate

To size the ceiling at the constellation level: AST ~56 Gbps theoretical per satellite (2,800 cells x ~20 Mbps) [DERIVED from Fierce]; Starlink next-gen >100 Gbps down / 50 Gbps up per satellite [FACT, SDxCentral]. For scale comparison, US mobile networks carried ~132 exabytes (132 trillion MB) in 2024, growing ~35%/yr [FACT, CTIA via prior doc and WIA]. A few hundred D2C satellites at ~50-100 Gbps each is a rounding error against that terrestrial volume, which is precisely why every capacity source concludes D2C **supplements** rather than **supplants** terrestrial: it cannot physically carry the mass-market data load. [FACT, corroborated: WIA, Opensignal, Nokia, IEEE]

---

## 4. The Cannibalization Question: Can Good-Enough D2C Eat Home/Fixed Broadband?

The lead asked the strategic question directly: if D2C reaches high 5G or 6G speeds, why keep a dedicated home connection when the phone suffices? This is the most important forward question in the model, because the data-center-style thesis is forward-looking (~10 years), and the answer is a capacity-physics answer, not a demand answer.

### 4.1 The case FOR cannibalization (the bull thesis)

- **The home-broadband job is increasingly mobile-shaped.** Most household internet is streaming and browsing on phones/tablets; a phone that delivers 100+ Mbps anywhere is functionally a home connection for a single-person or rural household.
- **Convergence is already the industry's stated direction.** The "super-bundle" thesis integrates fiber, cellular, FWA, and satellite into one auto-failover service [FACT, thefastmode/Deloitte], and bundled telco-satellite plans "boost ARPU for telcos and expand satellite operator access to mass-market consumers" [FACT]. Once satellite is in the bundle, the marginal home line becomes optional for edge users.
- **The addressable base is enormous.** Every out-of-coverage-capable phone (~5.5B devices, ~$1.1T cited ceiling, prior TAM doc) dwarfs the fixed-broadband household base. If even a thin slice drops the home line, the absolute number is large.
- **6G makes satellite a native layer.** 3GPP/6G integrates NTN as a standard tier; Nokia and IEEE describe satellite connectivity becoming default in every device by the 6G era [FACT]. A phone that is "always connected" by design erodes the rationale for a second, fixed pipe.
- **It is already happening at the thin edge.** BEAD procurement is buying satellite over fiber for the high-cost rural tail (cost-ratio doc, COMM-113): for those homes, the satellite link IS the home broadband, and a D2C phone is one step from collapsing even the dish.

### 4.2 The case AGAINST cannibalization (the bounded reality)

- **It does not work indoors, and "will likely never work" indoors or in dense urban areas** [FACT, WIA]. Home broadband is consumed indoors. A service that needs clear line-of-sight to the sky cannot be the primary home connection for the ~80% of usage that is indoor/urban.
- **The per-GB cost gap is ~20x and the beam-saturation ceiling is structural** (Section 3). Home broadband runs ~360-850 GB/month per household [FACT, Viasat usage tiers]; at ~$5-9/GB that is economically impossible to serve from a shared beam at home-broadband volumes. FWA already does 134-415 Mbps and fiber does gigabits at <$0.01/GB marginal [FACT]; D2C cannot match either on capacity or cost where they exist.
- **Performance is ~4G-class, not 5G, even next-gen** [FACT, WIA]: "roughly equivalent to 4G LTE, not 5G." The 150 Mbps *peak* is a single-user, full-beam, line-of-sight best case, not a sustained shared rate.
- **Demand is trip-shaped, not everyday.** Juniper: D2C demand is "concentrated to specific trips and travel, such as to national parks and nature reserves, rather than during everyday usage," which is why it forecasts usage "lower than anticipated" [FACT]. People want the safety-net, not a home-replacement.
- **The consensus of every independent analyst is supplement-not-supplant** [FACT: WIA, Opensignal, Nokia, IEEE, Deloitte]: "there is no scenario where SpaceX could compete directly with major carriers in urban areas."

### 4.3 The synthesized read

> **D2C cannibalizes the home connection at the *edge*, not at the *core*, and the boundary is set by beam-saturation physics, not by consumer preference.** Where a home is rural/remote, single-occupant, light-usage, or already satellite-served, a good-enough D2C phone can and will collapse the dedicated home line (and even the satellite dish) into the device. Where a home is urban/suburban, multi-occupant, indoor, heavy-usage, the ~20x per-GB gap and the indoor/density limits keep the fixed line in place. **The cannibalization of fixed broadband by D2C is therefore self-limiting to the same fringe where the cost-ratio doc found space already wins**, and it expands only as far as future spectrum-and-satellite gains push the saturation ceiling outward, which narrows but does not close the gap. The thesis-relevant point: do not model D2C as eating the ~$129B fixed-broadband-class wallet; model it as eating the *thin-edge* slice of it plus the standalone messaging/coverage market, with optionality on more if 6G-era capacity closes the gap.

A second-order cannibalization is worth naming: **D2C may cannibalize satellite fixed broadband (Starlink dishes) and standalone satellite-messaging before it touches terrestrial home broadband.** If a phone gets 50-150 Mbps from space, a rural user may drop both the dish and the separate messenger. That is intra-space cannibalization, relevant to how the space-comms wallet splits, but it does not enlarge the total against terrestrial.

---

## 5. Sizing D2C ex-China, and Is It Larger Than Fixed Broadband?

The lead asked to size the D2C opportunity ex-China and argue whether it is larger than fixed broadband. Two newer independent forecast houses sharpen the prior TAM doc's ~$2.6-13.8B near-term D2D band.

### 5.1 The near-term served-revenue forecasts (ex-China where stated)

| Source | D2C/D2D metric | 2030/2031 value | Status |
|---|---|---|---|
| **Omdia** (Mar 2026) | Smartphone D2D service revenue | **~$11.99B by 2030** | [FACT] |
| **Omdia** | Monthly active D2D users | **411M by 2030** (~80%/yr user CAGR, ~49%/yr revenue CAGR from 2026) | [FACT] |
| **Juniper** (2026) | Monthly active D2C users | **17.4M (2026) -> 133M (2031)**; usage "lower than anticipated" | [FACT] |
| Mordor (prior doc) | D2D satellite connectivity | $5.03B (2026) -> $13.80B (2031) | [ESTIMATE] |
| MarketsandMarkets (prior doc) | D2D | $0.57B (2025) -> $2.64B (2030) | [ESTIMATE] |
| ABI (prior doc) | Direct-to-cellular | $11.6B (2030) | [ESTIMATE] |

Sources: [Omdia press release, $12B by 2030](https://omdia.tech.informa.com/pr/2026/mar/smartphone-satellite-direct-to-device-service-revenue-to-approach12-billion-dollars-by-2030); [Telecompaper, Omdia $12B](https://www.telecompaper.com/news/satellite-direct-to-device-market-to-be-worth-usd-12-billion-in-2030-omdia--1564013); [ComputerWeekly, Juniper 17.4M->133M](https://www.computerweekly.com/news/366643796/Direct-to-cell-growth-hits-headwinds-while-6G-set-for-rapid-uptake); [Yahoo/Juniper, MAU 130M+ by 2031, usage lower than anticipated](https://finance.yahoo.com/sectors/technology/articles/direct-cell-monthly-active-users-060000635.html).

**Reading the forecasts.** Omdia (~$12B revenue, 411M MAU by 2030) and Juniper (133M MAU by 2031, low usage) converge on the shape: hundreds of millions of users, but a low ARPU because the service is a thin safety-net add-on (~$10/month, often bundled free). ABI's $11.6B and Mordor's $13.8B sit in the same neighborhood. So the **near-term (to ~2030-31) D2C served revenue is ~$12-14B ex-China** [DERIVED, convergence of 4 houses], an order of magnitude below the ~$129B Morningstar served-connectivity slice that is mostly fixed-broadband-class.

### 5.2 The "is it larger than fixed broadband?" question, resolved on three axes

The answer depends on which "size" you mean, and the honest version distinguishes them:

| Axis of "size" | Direct-to-cell | Fixed broadband (ex-China) | Which is larger |
|---|---|---|---|
| **Near-term served revenue (to ~2030)** | ~$12-14B (Omdia/Juniper/ABI/Mordor) | ~$129B served-connectivity slice is mostly fixed-class (Morningstar, prior doc); US fixed-broadband retail alone is tens of $B | **Fixed broadband**, by ~10x |
| **Addressable base (devices/reach)** | ~5.5B out-of-coverage-capable phones; ~$1.1T cited ceiling (AST/GSMA) | ~400-500M unconnected households (Kuiper framing); ~1B+ broadband households total | **Direct-to-cell**, by reach |
| **10-year optionality (the forward thesis)** | Can absorb part of the home-broadband wallet IF capacity gap closes; native 6G layer in every device | Mature, slow-growth (~2% terrestrial), defended by sunk plant | **Direct-to-cell**, on optionality (capacity-gated) |

> **The defensible answer to the lead's question:** **D2C is the larger market by addressable devices and by 10-year optionality, but the smaller market by near-term served revenue.** It is "likely larger than home broadband" (the model's working hypothesis) only in the forward, optionality sense, and only if the per-GB capacity gap narrows enough for the phone to credibly substitute for the home line beyond the thin edge. On today's served-revenue, fixed broadband is ~10x larger. **The hypothesis that D2C is the larger market is a bet on capacity physics improving, not a current fact**, which is exactly the right framing for a 10-year-out, trajectory-over-base model. The number to carry: near-term D2C ~$12-14B ex-China served revenue, with a ~$1.1T addressable ceiling whose realization is gated by the ~20x cost gap.

### 5.3 Why D2C is nonetheless the right *lead* for the model

Even though fixed broadband is larger today, D2C is the correct lead market for three structural reasons the prior docs support:

1. **It is the segment where space has a genuine, non-substitutable product** (reach an unmodified phone in a dead zone), versus fixed broadband where it is one option among FWA/fiber/cable.
2. **It is where the ~$17B and ~$45 MHz capital is actually flowing** (the players reveal the lead market by where they spend).
3. **It carries the optionality** to grow into the home-broadband wallet if 6G-era capacity closes the gap, which fixed broadband (mature, defended) does not offer a new entrant.

---

## China note (excluded from totals)

Per scope, China is excluded from all sizing above. For completeness only: China runs parallel state-aligned D2C efforts (e.g. via its own LEO constellations and its three carriers, China Mobile alone >1B connections), under a separate spectrum and regulatory regime. None of the Omdia, Juniper, AST, or Starlink figures used here include China, and the ex-China caveat is why the served-revenue numbers are conservative relative to global-including-China headlines.

---

## Sources

*Benchmarks and specs*
- [AST SpaceMobile, Next-Generation BlueBird](https://ast-science.com/next-gen-bluebird/)
- [AST SpaceMobile, How It Works](https://ast-science.com/how-it-works/)
- [AST SpaceMobile, BlueBird 6 launch (BusinessWire)](https://www.businesswire.com/news/home/20251222922862/en/AST-SpaceMobile-Announces-Successful-Orbital-Launch-of-BlueBird-6-the-Largest-Commercial-Communications-Array-Ever-Deployed-in-Low-Earth-Orbit)
- [SatNews, AST Block 2 launch + 5,600 cells](https://satnews.com/2026/06/17/direct-to-device-momentum-ast-spacemobile-successfully-launches-giant-next-gen-bluebird-satellites-atop-spacex-falcon-9/)
- [SpaceNews, AST 17 larger satellites](https://spacenews.com/ast-spacemobile-starts-work-on-17-larger-direct-to-smartphone-satellites/)
- [arxiv 2506.18672, Spectrum Opportunities (AST beam footprint 20.3 km, 40 MHz/beam)](https://arxiv.org/pdf/2506.18672)
- [arxiv 2506.00283, Starlink Direct-to-Cell crowdsourced measurement (per-beam Mbps, spectrum)](https://arxiv.org/html/2506.00283v7)
- [SDxCentral, Starlink 25M target / Gen2 100x data density](https://www.sdxcentral.com/news/starlink-targets-25m-users-by-year-end-as-gen2-satellite-plan-promises-100x-data-density/)
- [5gstore, Starlink D2C 150 Mbps target](https://5gstore.com/blog/2026/03/26/starlink-direct-to-cell-150mbps/)
- [SatelliteInternet.com, Starlink D2C / T-Satellite guide](https://www.satelliteinternet.com/providers/starlink/starlink-direct-to-cell/)
- [NewSpaceTracker, Direct-to-Smartphone Satellites](https://newspacetracker.com/articles/direct-to-smartphone-satellites/)
- [Fierce, AST and the problem of delivering broadband from space (Madden $5-9/GB, 56 Gbps)](https://www.fierce-network.com/wireless/ast-spacemobile-and-problem-delivering-broadband-space)

*Spectrum*
- [Via Satellite, FCC grants AST D2D commercial authorization](https://www.satellitetoday.com/connectivity/2026/04/22/fcc-grants-ast-spacemobile-commercial-authorization-for-direct-to-device-service/)
- [SatNews, FCC grants AST 248-satellite constellation + D2C](https://satnews.com/2026/04/21/fcc-grants-ast-spacemobile-authority-for-248-satellite-constellation-and-direct-to-cell-service/)
- [DCD, SpaceX acquires EchoStar AWS-4/H-Block for $17B](https://www.datacenterdynamics.com/en/news/spacex-acquires-echostars-aws-4-and-h-block-spectrum-for-17bn/)
- [Space.com, SpaceX $17B spectrum for Starlink](https://www.space.com/space-exploration/satellites/spacex-buys-usd17-billion-worth-of-satellite-spectrum-to-beef-up-starlink-broadband-service)
- [EchoStar IR, spectrum sale + commercial agreement with SpaceX](https://ir.echostar.com/news-releases/news-release-details/echostar-announces-spectrum-sale-and-commercial-agreement-spacex)
- [SatNews, AST 45 MHz lower mid-band via Ligado](https://news.satnews.com/2025/06/15/ast-spacemobile-announces-settlement-term-sheet-facilitating-long-term-access-to-up-to-45-mhz-of-premium-lower-mid-band-spectrum-in-north-america-for-d2d-apps/)
- [BusinessWire, AST 45 MHz settlement term sheet](https://www.businesswire.com/news/home/20250613700432/en/AST-SpaceMobile-Announces-Settlement-Term-Sheet-Facilitating-Long-Term-Access-to-up-to-45-MHz-of-Premium-Lower-Mid-Band-Spectrum-in-North-America-for-Direct-to-Device-Satellite-Applications)
- [basenor, FCC approves SpaceX D2C 5G spectrum / 4G-5G power](https://www.basenor.com/blogs/news/fcc-approves-spacex-starlink-direct-to-phone-5g-spectrum-deal)

*Pricing, economics, cannibalization, sizing*
- [Via Satellite, T-Mobile cuts Starlink messaging price ($10/$15/$20)](https://www.satellitetoday.com/connectivity/2025/04/25/t-mobile-cuts-price-on-starlink-satellite-messaging-service-to-start-in-july/)
- [rvmobileinternet, T-Mobile Starlink D2C pricing / beta to all carriers](https://www.rvmobileinternet.com/t-mobiles-starlink-direct-to-cellular-satellite-pricing-announced-expands-beta-to-other-carriers/)
- [Fierce, setting realistic expectations on satellite phones (Madden)](https://www.fierce-network.com/wireless/setting-realistic-expectations-satellite-phones-madden)
- [WIA, Satellite D2D Are Not Replacements for Terrestrial Networks](https://wia.org/satellite-direct-to-device-services-are-not-replacements-for-terrestrial-networks/)
- [Opensignal, D2D at MWC26: sky-high ambitions, ground-level constraints](https://insights.opensignal.com/2026/03/d2d-at-mwc26-sky-high-ambitions-ground-level-constraints/)
- [Omdia, D2D service revenue ~$12B by 2030, 411M MAU](https://omdia.tech.informa.com/pr/2026/mar/smartphone-satellite-direct-to-device-service-revenue-to-approach12-billion-dollars-by-2030)
- [Telecompaper, Omdia D2D $12B by 2030](https://www.telecompaper.com/news/satellite-direct-to-device-market-to-be-worth-usd-12-billion-in-2030-omdia--1564013)
- [ComputerWeekly, Juniper D2C 17.4M->133M, headwinds; 6G](https://www.computerweekly.com/news/366643796/Direct-to-cell-growth-hits-headwinds-while-6G-set-for-rapid-uptake)
- [Yahoo/Juniper, D2C MAU 130M+ by 2031, usage lower than anticipated](https://finance.yahoo.com/sectors/technology/articles/direct-cell-monthly-active-users-060000635.html)
- [The Register, satellite phone dreams orbit reality (D2C to underwhelm)](https://www.theregister.com/networks/2026/06/02/satellite-phone-dreams-orbit-reality-as-direct-to-cell-usage-set-to-underwhelm/5249696)
- [thefastmode, 2026 predictions: always-on, super-bundle](https://www.thefastmode.com/expert-opinion/47484-2026-predictions-connectivity-moving-from-best-effort-to-always-on)
- [Deloitte, next-gen satellite internet predictions 2026](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/next-gen-satellite-internet.html)
- [Nokia, 6G will put satellite connectivity in every device](https://www.nokia.com/blog/6g-will-put-satellite-connectivity-in-every-smartphone-and-device/)
- [WhistleOut, 5G home internet vs satellite (speeds, caps)](https://www.whistleout.com/Internet/Guides/5g-internet-vs-satellite-internet)

---

## Confidence

- **Benchmark specs (Section 1): medium-high.** AST per-cell speed, processing bandwidth, array size, and Starlink per-beam/per-user throughput are each in 2+ sources (company + trade press + the two arxiv technical papers). The AST 20.3 km beam footprint and the 2,800-cell figure are each single-source (one arxiv paper; one analyst) and flagged.
- **Spectrum deals (Section 2): medium-high.** EchoStar $17B/65 MHz and AST/Ligado 45 MHz are each in primary IR/press releases plus 2+ trade outlets. The ~20x vs "100x" throughput-uplift discrepancy is noted (20x is the spectrum-driven, like-for-like figure; 100x compares to the first-gen *system*).
- **The ~20x per-GB cost gap (Section 3): medium-high in direction, medium on the exact number.** The $5-9/GB vs $0.30/GB is one named analyst (Joe Madden), but the *direction* (satellite $/GB structurally far above terrestrial, rising with density) is corroborated by every capacity source (Morningstar, WIA, Opensignal). It is the load-bearing finding and it answers OQ5 of the cost-ratio doc.
- **Cannibalization read (Section 4): medium.** A physics-bounded judgment, not a measured outcome. The indoor/urban limits and supplement-not-supplant consensus are well-attested [FACT]; the forward "if 6G closes the gap" branch is inherently uncertain.
- **Sizing (Section 5): medium.** Omdia and Juniper are independent and recent; the ~$12-14B near-term band is the convergence of four houses. The "larger than fixed broadband" answer is decomposed by axis to avoid a false single answer; the optionality axis is a judgment, not a forecast.

---

## Open Questions / Uncertainties

1. **The exact D2C cost-per-GB at next-gen spectrum.** The $5-9/GB figure predates the EchoStar ~65 MHz and Gen2 ~100 Gbps satellites. A re-derived $/GB at full spectrum and tighter beams would tell the model how far the ~20x gap actually narrows, and whether D2C ever crosses below the terrestrial mobile marginal floor in any served setting.
2. **Sustained (not peak) per-user throughput under realistic loading.** The 150 Mbps (Starlink) and 200 Mbps (AST) figures are single-user, full-beam, line-of-sight peaks. The number that decides home-broadband substitution is the *sustained shared* rate when a beam carries hundreds of users; no operator has disclosed it.
3. **The D2C revenue split and true ARPU.** AST cites 50/50 with MNOs (prior doc); the realized per-user revenue to the satellite operator (after the carrier's half and after free-bundling) is not cleanly public. T-Satellite at $10/month often free-bundled implies a very thin satellite-operator ARPU. This bears directly on whether the ~$12-14B served-revenue forecast is even reachable.
4. **Where the AST vs Starlink architectures actually land on cost.** Big-aperture-few-birds (AST) vs small-payload-many-birds (Starlink) should produce different $/GB and different capacity-vs-coverage trade-offs; a head-to-head cost-per-delivered-GB comparison at scale is not in the public data and would sharpen which architecture a Rocket Lab-scale entrant should emulate (if any).
5. **The 6G NTN substitution timeline.** Section 4's forward branch hinges on when 6G-era NTN makes the phone a credible home-broadband substitute beyond the edge. 3GPP/6G integrates NTN natively (Nokia/IEEE), but the date at which capacity-per-user rises enough to matter for cannibalization is the single most important unknown for the "D2C larger than fixed broadband" hypothesis.
6. **Intra-space cannibalization split.** Section 4.3 flags that D2C may eat satellite fixed broadband (Starlink dishes) and standalone messaging before terrestrial home broadband. How the space-comms wallet splits between D2C and satellite-FWA is unresolved and matters for sizing any single space-comms revenue line.

---

## Claims ledger

*Numbered hard claims for the catalog step to ingest. Each lists value, status, and 2+ sources (or is flagged single-source). No COMM- IDs assigned per instruction.*

1. **AST Block 2 processing bandwidth ~10 GHz per satellite (~10x Block 1).** [FACT], AST Next-Gen BlueBird; Wikipedia (AST SpaceMobile); Gunter's Space Page (BlueBird 2).
2. **AST peak speed ~120 Mbps per coverage cell (Block 1); up to ~200 Mbps to a phone (Block 2 peak).** [FACT], AST Next-Gen BlueBird; SatNews (Block 2 launch).
3. **AST cells per satellite: 2,000+ active; Block 2 designed for ~2,500 adjustable beams (one analyst cites 2,800); ~40 MHz per downlink beam (UHF/L band).** [FACT]; the 2,800 figure is [FACT, single-source], AST; arxiv 2506.18672; Fierce (Madden, 2,800).
4. **AST narrowest Block 2 beam footprint ~20.3 km diameter / ~324 km² at 725 km altitude.** [FACT, single-source], arxiv 2506.18672 (spectrum-opportunities paper).
5. **AST theoretical capacity ~56 Gbps per satellite (2,800 cells x ~20 Mbps).** [DERIVED], Fierce (Madden per-cell 20 Mbps); my arithmetic.
6. **AST ~5,600 coverage cells planned for ~nationwide US coverage.** [FACT, single-source], SatNews; SEC 8-K (via SpaceNews).
7. **AST array size: Block 1 ~64 m² (693 sq ft); Block 2 ~223 m² (~2,400 sq ft, ~3x larger, ~10x data capacity).** [FACT], AST Next-Gen BlueBird; NewSpaceTracker; BusinessWire (BlueBird 6).
8. **Starlink 650+ Direct-to-Cell satellites in orbit by early 2026; "largest 4G network by coverage area."** [FACT], SatelliteInternet.com; Via Satellite; basenor.
9. **Starlink D2C per-beam throughput ~3.1 Mbps on current PCS spectrum; ~6.2 Mbps with H-Block; ~18.6 Mbps aggregate at full holdings.** [FACT, single-source technical], arxiv 2506.00283 (crowdsourced measurement).
10. **Starlink D2C current per-user throughput ~4 Mbps top; data service "hundreds of kbps at best" (late 2025).** [FACT], 5gstore; SatelliteInternet.com; basenor.
11. **Starlink D2C next-gen per-user peak target 150 Mbps download.** [FACT], 5gstore (SpaceX policy lead); SDxCentral.
12. **Starlink next-gen satellite throughput >100 Gbps down / 50 Gbps up; ~16x beams; ~100x data density vs Gen1.** [FACT], SDxCentral; SatelliteInternet.com.
13. **Starlink D2C US subscribers 16M unique / 10M monthly active (Mar 2026), targeting 25M end-2026.** [FACT], prior library doc (`comms_us_cellular_market.md`); Nokia/IEEE.
14. **T-Satellite (Starlink via T-Mobile) pricing $10/month; free on top T-Mobile plans; $10 for AT&T/Verizon users (originally $15 add-on / $20 other-carrier).** [FACT], Via Satellite; rvmobileinternet; broadbandbreakfast.
15. **AST FCC commercial D2D authorization uses partner low-band (700/800 MHz via Verizon/AT&T/FirstNet, Band 14); "combines MNO partners' licensed frequencies with our own."** [FACT], Via Satellite (FCC grant); SatNews; AST How It Works.
16. **SpaceX acquired EchoStar spectrum (~65 MHz: 40 MHz AWS-4 + 10 MHz H-Block + 15 MHz AWS-3) for ~$17B (~$8.5B cash + ~$8.5B stock); approved May 12, 2026; ~20x throughput uplift projected.** [FACT], DCD; Space.com; EchoStar IR; basenor.
17. **AST secured long-term (80+ year) access to up to ~45 MHz lower mid-band via Ligado (~40 MHz L-band MSS + 5 MHz at 1670-1675 MHz); payments began Sep 30, 2025.** [FACT], SatNews; BusinessWire; SpaceDaily.
18. **Satellite NTN delivery cost ~$5-9/GB vs terrestrial 5G ~$0.30/GB (~20x higher).** [FACT, single named analyst: Joe Madden/Mobile Experts], Fierce (two articles, AST broadband problem; realistic expectations).
19. **D2C "will likely never work" indoors or in dense urban areas; next-gen performance ~4G LTE not 5G; requires line-of-sight to sky.** [FACT], WIA; Opensignal.
20. **US mobile data carried ~132 exabytes (132 trillion MB) in 2024, ~35%/yr growth; D2C aggregate capacity is a rounding error against it.** [FACT], CTIA (via prior doc); WIA.
21. **Omdia: smartphone D2D service revenue ~$11.99B and 411M monthly active users by 2030 (~80%/yr user, ~49%/yr revenue CAGR from 2026).** [FACT], Omdia press release; Telecompaper.
22. **Juniper: D2C monthly active users 17.4M (2026) -> 133M (2031); usage "lower than anticipated"; demand concentrated in trips/travel.** [FACT], ComputerWeekly; Yahoo/Juniper.
23. **Near-term (to ~2030-31) D2C served revenue ex-China ~$12-14B (convergence of Omdia ~$12B, ABI $11.6B, Mordor $13.8B).** [DERIVED], Omdia; ABI (prior doc); Mordor (prior doc).
24. **Home broadband household usage ~360-850 GB/month; FWA ~134-415 Mbps; FCC broadband standard 100/20 Mbps; D2C cannot match on capacity/cost where terrestrial exists.** [FACT], Viasat usage tiers; WhistleOut/highspeedinternet.
25. **D2C addressable base ~5.5B out-of-coverage-capable phones / ~$1.1T cited ceiling, far larger than the ~400-500M unconnected-household fixed base; but near-term served revenue ~10x smaller than the ~$129B fixed-broadband-class served slice.** [FACT] (reach figures) / [DERIVED] (the comparison), prior TAM doc (AST/GSMA $1.1T, 5.5B devices; Morningstar $129B; Kuiper 400-500M households).
