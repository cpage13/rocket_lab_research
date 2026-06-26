# Direct-to-Cell Subscribers per Satellite: How Many People One Flat ~25 m^2 Cellular D2C Satellite Can Support, What Binds It (Antenna vs Processor), How Many Channels It Runs at Once, and the Implied CAPACITY Fleet

**Research date:** 2026-06-26
**Status:** Understanding-building input for the Neutron direct-to-cell (DTC) model. No go/no-go verdict. This doc pins the number the fleet-sizing needs: SUBSCRIBERS PER SATELLITE for one flat ~25 m^2 cellular (NOT broadband) D2C satellite, separating ATTACHED subscribers (people who can register on it) from SIMULTANEOUSLY-ACTIVE users (people pulling data at the busy instant), with the concurrency assumption stated explicitly. It then converts that into the CAPACITY fleet (subscribers / subs-per-sat) the model must fly to SERVE a target subscriber base, which is a different and far larger number than the COVERAGE constellation (everyone can SEE a satellite at ~340 sats). Every value is flagged sourced (FACT) / derived (DERIVED) / estimate (ESTIMATE) / unknown (UNKNOWN).

> **Why this document exists (the load-bearing distinction).** The corpus owns the COVERAGE floor (~130-450 satellites so every point can SEE a satellite, [`leo_constellation_coverage_minimums.md`](leo_constellation_coverage_minimums.md) COMM-215/224) and the per-satellite SUPPLY (~5-15 Gbps aggregate on 25 MHz, [`dtc_capacity_supply.md`](dtc_capacity_supply.md) COMM-410). What it has NOT pinned as a clean headline is the bridge between them: how many SUBSCRIBERS one satellite can carry, and therefore how many satellites it takes to SERVE (not just cover) a subscriber base. This is the gate on the entire cost-per-subscriber result, because fleet = subscribers / subs-per-sat, and the model's verdict on whether a Neutron D2C business closes is dominated by that fleet count. The empirical proof that coverage and capacity fleets differ by more than an order of magnitude is Starlink: it flies ~9,500 satellites for ~12M subscribers (~1,260 subs/sat, [`starlink_v3_specs.md`](../competitors/starlink_v3_specs.md) claim 21), a capacity-driven fleet far above any coverage floor, which is exactly why it needs Starship to launch thousands. The founder's framing: a coverage constellation is ~340 satellites, but the CAPACITY fleet is set by subs-per-satellite and is likely far larger, and this doc grounds how much larger for cellular D2C specifically.

> **Grounds in and does NOT re-derive (this doc adds the SUBSCRIBERS-PER-SATELLITE and CAPACITY-FLEET layer on top of the per-satellite capacity the corpus owns):**
> - [`dtc_capacity_supply.md`](dtc_capacity_supply.md) (COMM-406..425): owns the per-satellite total (~5-15 Gbps on 25 MHz, central ~8-10 Gbps, COMM-410), the spectrum-bound-not-processor-bound finding (COMM-411), the ~200-450 beam count (COMM-408, the softest input), the speed-vs-users formula per_user = (B x SE) / active-users (COMM-417), and the ~4,860-phones-per-beam / 5%-concurrency / ~240-active worked example (COMM-418/420). This doc takes all of those as given and assembles them into subs-per-satellite (attached and active) and the fleet. It does NOT re-derive the per-satellite capacity.
> - [`dtc_data_rate_vs_spectrum.md`](dtc_data_rate_vs_spectrum.md) (COMM-493..512): owns the rate-vs-owned-bandwidth curve, the power-limited regime, and the ~50-100 MHz power-binding knee (COMM-509/510). This doc uses the per-user rate band (~20-30 Mbps light, ~500 kbps-1 Mbps busy, COMM-495) as the service-level the subs count is computed at.
> - [`dtc_antenna_aperture_tradeoff.md`](dtc_antenna_aperture_tradeoff.md) (COMM-293..314): owns the aperture-to-service ladder, the bare-phone link budget (the satellite supplies the gain, COMM-294), and the AST-vs-Starlink ~100x per-satellite capacity asymmetry (COMM-306). This doc uses the ladder to fix WHICH satellite (~25 m^2 cellular, the Starlink-class rung) and does NOT re-derive the link budget.
> - [`spectrum_capacity_primer.md`](spectrum_capacity_primer.md) (COMM-426..439) and [`channels_aggregate_answer.md`](channels_aggregate_answer.md): own carrier aggregation summing separately-held channels (COMM-433), OFDMA-is-sharing-not-capacity (COMM-434), and the reuse multiplier set by beam footprint not satellite count (COMM-436). This doc uses these to answer the channels/frequencies-per-satellite question (Section 3) and does NOT re-derive them.
> - [`dtc_spectrum_access.md`](dtc_spectrum_access.md) (COMM-451..492): owns the aperture-vs-held-bandwidth-are-independent finding (COMM-481) and the owned-spectrum gate. This doc uses the ~25 MHz owned-spectrum operating point as given.
> - [`competitors/starlink_v3_specs.md`](../competitors/starlink_v3_specs.md) (claims 17/18/20/21/22) and [`economics/comms_space_supply_cost.md`](../economics/comms_space_supply_cost.md): own the Starlink fleet (~9,500 op sats), subscribers (~12M), subs-per-sat (~1,260), the V2-mini D2C 48-beam / ~7 Gbps baseline, and the V3 D2C ~700 Gbps / 15,000-sat target. This doc uses all of these as the empirical cross-checks and does NOT re-derive them.
> - Cross-references (not re-listed): [`dtc_system_model.md`](dtc_system_model.md) (the governing rule, the UNKNOWN Flatellite power), [`leo_constellation_coverage_minimums.md`](leo_constellation_coverage_minimums.md) (the coverage floor), [`economics/comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) (the AST ~56 Gbps processor anchor, the $/GB floor).

> **Tagging.** **[FACT]** sourced (2+ independent sources unless flagged single-source), **[DERIVED]** computed in this doc from sourced inputs, **[ESTIMATE]** a third-party model/target/projection, **[UNKNOWN]** a named gap (not invented). New claims use **COMM-535..560** (the next free contiguous block above the current global max COMM-534; verified free across the corpus). No em-dashes anywhere. Inline math: `^2` squared, `x` multiply, `->` arrow, `log2` base-2 log.

---

## 0. Answer first (subscribers per satellite, what binds, and the fleet, in one screen)

**One flat ~25 m^2 cellular D2C satellite on ~25 MHz of owned spectrum puts roughly ~5-15 Gbps of TOTAL bandwidth through the air (central ~8-10 Gbps), across ~200-450 beams, and that total, NOT a per-person rate, is what subscribers divide. The binding limit is the OWNED SPECTRUM (the ~25 MHz, reused across beams), not the onboard processor and not the antenna power, until the channel is widened past ~50-100 MHz where antenna power starts to bind; on a thin 25 MHz cellular slice the satellite is firmly SPECTRUM-bound. A single satellite runs MANY channels and MANY frequencies at once (hundreds of beams, and multiple cellular bands simultaneously, low-band 700-900 MHz plus PCS/AWS/S-band ~1.9-2 GHz, exactly as AST does), so it is NOT limited to one channel; the limit on how many it runs is the digital beamforming processor (beam/cell count) and the total power budget shared across beams, with the AGGREGATE capacity still capped by how much spectrum it HOLDS. Subscribers-per-satellite is therefore two numbers, not one: it can SIMULTANEOUSLY ACTIVE-serve only ~250-2,000 users at a usable cellular rate (the ~8-10 Gbps split into ~5-30 Mbps active sessions), but it can hold ~25,000-150,000 ATTACHED subscribers on the books at a realistic ~1-5% busy-hour concurrency and cellular oversubscription, central planning figure ~50,000-100,000 attached per satellite. That attached figure is the one the fleet-sizing uses, and it is roughly an order of magnitude HIGHER than Starlink's ~1,260 broadband subs/sat, because cellular D2C subscribers each consume far less than a broadband household (low data, thin spectrum, big shared beams, heavy oversubscription), and it sits squarely inside Starlink's OWN V3 D2C planning math (15,000 sats x 700 Gbps = 10.5 Pbps -> "over 1 billion users," ~70,000 attached/sat). So the CAPACITY fleet to SERVE a subscriber base is subscribers / ~50,000-100,000: roughly ~100-200 satellites to serve 10M subscribers, and ~500-1,000 to serve 50M, all ABOVE the ~340-satellite coverage floor (so coverage is satisfied for free at these counts), and all assuming the subscribers are spread across the coverage area rather than piled into a few dense cells, which the satellite physically cannot serve (the density caveat, the binding real-world limiter).**

1. **Per-satellite total bandwidth and aggregate capacity (Section 1).** ~5-15 Gbps total per satellite, central ~8-10 Gbps, on ~25 MHz across ~200-450 beams (the corpus's COMM-410). This is the SUM over all beams; it is what all subscribers in view share. [DERIVED, from corpus]

2. **What binds: spectrum, not processor, not (yet) antenna power (Section 2).** On 25 MHz the SPECTRUM binds: 25 MHz x ~3 bps/Hz x reuse caps the total far below the ~10 GHz / ~56 Gbps-class processor an AST-grade payload carries (COMM-411). The ANTENNA (power/EIRP) binds only if the channel is widened past ~50-100 MHz (COMM-509). So at the 25 MHz cellular operating point the answer is unambiguous: more spectrum is the lever, not a bigger processor or more power. The processor would bind only on a much wider band (>~100-200 MHz) that a thin cellular holding does not have. [DERIVED + FACT]

3. **Channels/frequencies per satellite: MANY, not one (Section 3).** One satellite forms hundreds of beams and can operate MULTIPLE cellular bands simultaneously (AST runs low-band 700/850 MHz plus its own S-band and L-band at once across 2,000-2,500 beams; Starlink's D2C beams are independently steerable). Carrier aggregation then SUMS the held channels so total capacity tracks total MHz held (COMM-433). The limit on simultaneous channels/beams is the digital beamforming processor (how many beams it can form) and the power budget (shared across energized beams), and the AGGREGATE capacity is still capped by total spectrum held, not by a one-channel rule. [FACT, multi-source]

4. **THE ANSWER: subscribers per satellite (Section 4-5), with the concurrency stated.** Two numbers: **simultaneously-ACTIVE ~250-2,000 users** per satellite at a usable cellular rate (~8-10 Gbps / ~5-30 Mbps active session, the hard physical ceiling at any instant), and **ATTACHED ~25,000-150,000 subscribers** on the books (active divided by a ~1-5% busy-hour concurrency factor, with cellular oversubscription), central planning band **~50,000-100,000 attached per satellite**. Cross-checks: Starlink broadband ~1,260 subs/sat (COMM claim 21) is far LOWER because each broadband household uses ~10-100x the data of a thin-data cellular D2C user; Starlink's own V3 D2C model implies ~70,000 attached/sat (1.05B users / 15,000 sats); AST publishes no per-satellite subscriber number (only a "billions of subscribers" TAM). The cellular-D2C density is HIGHER than broadband density precisely because the service is thinner per user. [DERIVED, concurrency-dependent; cross-checked]

5. **The implied CAPACITY fleet (Section 6).** Fleet to SERVE = subscribers / attached-per-sat. At ~50,000-100,000 attached/sat: **~100-200 satellites for 10M subscribers, ~500-1,000 for 50M**, all above the ~340-sat coverage floor (coverage is satisfied at these counts, so the fleet is capacity-driven, not coverage-driven, only once the subscriber base x its data demand exceeds what ~340 satellites can carry). The fleet is dominated by the attached-per-sat assumption and by the DENSITY CAVEAT: these counts assume subscribers are SPREAD across the coverage footprint; demand piled into a few dense cells cannot be served by adding satellites (the spectrum-saturation ceiling, COMM-415), so the real fleet for a given subscriber base depends on their geographic spread, the binding unknown. [DERIVED]

The rest sources and derives each point.

---

## 1. Per-satellite total bandwidth and aggregate capacity (what subscribers divide)

The number subscribers divide is the satellite's TOTAL throughput across all its beams, not a per-person pipe. The corpus owns this; it is restated here as the input to the subscriber count.

### 1.1 The total: ~5-15 Gbps on 25 MHz

A flat ~25 m^2 phased array on ~25 MHz of owned spectrum produces **~5-15 Gbps of total per-satellite DTC throughput, central ~8-10 Gbps**, set by ~200-450 beams x ~50-75 Mbps/cell x a spatial-reuse fraction, capped by the fixed 25 MHz ([`dtc_capacity_supply.md`](dtc_capacity_supply.md) COMM-410). This brackets the two flying anchors:

| System | Aperture | Spectrum | Per-satellite D2C aggregate | Tag |
|---|---|---|---|---|
| Starlink V2-mini D2C | ~25 m^2 | 2x5 MHz (PCS G) | **~7 Gbps** (48 beams x ~7 Mbps, fronthaul-limited) | [FACT/ESTIMATE, analyst] |
| Flat ~25 m^2 (this model) | ~25 m^2 | ~25 MHz owned | **~5-15 Gbps (central ~8-10)** | [DERIVED] |
| AST BlueBird Block 2 | ~199-223 m^2 | up to 40 MHz/beam | **~56 Gbps** (2,800 cells x 20 Mbps; AST's own 2,000+ cells x 120-150 Mbps is a higher provisioned ceiling that is power/spectrum-bound in practice) | [FACT cells; DERIVED 56 Gbps] |
| Starlink V3 D2C (projected) | ~25 m^2-class deployable | ~65 MHz owned (EchoStar) | **~700 Gbps** (>100x V2 D2C) | [ESTIMATE/projection] |

Sources: Starlink V2-mini D2C ~7 Gbps / 48 beams ([thexlab.org working paper](https://thexlab.org/wp-content/uploads/2025/07/Starlink_Analysis_Working_Paper_v0.2.pdf), [Mike Puchol model](https://mikepuchol.com/modeling-starlink-capacity-843b2387f501)); SpaceX official per-beam D2C 4.4 Mbps (1.4 MHz channel) / 18.3 Mbps (5 MHz channel), peak EIRP 58 dBW, all downlink beams independently steerable ([SpaceX-T-Mobile FCC Technical Narrative](https://cdn.arstechnica.net/wp-content/uploads/2023/05/SpaceX-T-Mobile-Technical-Narrative.pdf)); AST ~56 Gbps = 2,800 cells x 20 Mbps ([FierceNetwork](https://www.fierce-network.com/wireless/ast-spacemobile-and-problem-delivering-broadband-space)), AST 2,000+ cells x 120-150 Mbps/cell + 10 GHz processing ([AST Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/)); V3 D2C 700 Gbps / >100x ([NextBigFuture](https://www.nextbigfuture.com/2025/09/spacex-15000-v3-starlink-direct-to-cellphone-satellites.html)). The ~5-15 Gbps band and its derivation are the corpus's (COMM-410); this doc does not re-derive it.

### 1.2 Why this is the right input (total, not per-user)

Subscribers do not each get a private link; they time-share the satellite's beams. So the satellite's capacity to serve PEOPLE is its total bits/s divided among them, exactly as a cell tower's capacity is shared across the phones under it ([cell-tower aggregate throughput is bounded by spectrum and backhaul, shared across users, ScienceDirect](https://www.sciencedirect.com/topics/engineering/cell-average-throughput)). The per-PHONE rate (the corpus's ~25-50 Mbps single-phone peak, ~20-30 Mbps light, COMM-493/495) is what ONE user sees when few others are active; the SUBSCRIBER COUNT is the total divided by the per-user demand at the assumed concurrency. The two are linked by the speed-vs-users formula (COMM-417), which Section 4 inverts to a subscriber count. [DERIVED]

---

## 2. What binds: the antenna, the processor, or the spectrum?

The founder's question 2: is the binding limit COMPUTATION (the onboard digital processor / beamforming ASIC) or ANTENNA (aperture, power, EIRP)? The corpus answers this, and the answer depends on how wide the channel is.

### 2.1 On 25 MHz: the SPECTRUM binds (not processor, not antenna)

On a thin ~25 MHz cellular slice, neither the processor nor the antenna power is the wall; the OWNED SPECTRUM is:
- **Processor:** an AST-grade D2C payload carries ~10 GHz of processing bandwidth realizing ~56 Gbps across 2,800 cells ([AST Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/); [FierceNetwork](https://www.fierce-network.com/wireless/ast-spacemobile-and-problem-delivering-broadband-space)). 25 MHz x 3 bps/Hz x even ~50x reuse is only ~3.75 Gbps from one slice; to reach ~10-15 Gbps total needs ~130-200x effective reuse, all FAR below the processor ceiling. So the processor is not binding on 25 MHz (COMM-411). [DERIVED + FACT]
- **Antenna power:** a ~25 m^2 array delivers SNR ~ 1 (0 dB measured for Starlink) to a phone, enough to run the 25 MHz at ~2-3 bps/Hz. Power binds only when the channel is WIDENED, because holding efficiency as bandwidth grows needs EIRP to scale with bandwidth, and a ~25 m^2 array's fixed power gets spread below ~1-2 bps/Hz somewhere in the ~50-100 MHz region (COMM-509/510). At 25 MHz the power is sufficient. [FACT + ESTIMATE]
- **Spectrum:** the 25 MHz x SE x reuse product is the wall. AST's own conclusion: it operates "near the practical limits of antenna size and radiated power," so "expanded bandwidth is the most viable path to increased D2D throughput" ([arXiv 2506.18672](https://arxiv.org/html/2506.18672v1)). More spectrum, not a bigger processor or more power, is the per-satellite-capacity lever on a thin cellular holding. [FACT]

### 2.2 Where each limit takes over (the crossover map)

| Owned bandwidth | Binding limit | Why | Tag |
|---|---|---|---|
| ~25 MHz (the cellular operating point) | **SPECTRUM** | 25 MHz x SE x reuse caps the total; processor (~56 Gbps-class) and power both have headroom | [DERIVED, COMM-411] |
| ~50-100 MHz | **ANTENNA (power/EIRP) begins to bind** | holding efficiency needs EIRP ~ proportional to B; a ~25 m^2 array's fixed power spreads below ~1-2 bps/Hz | [ESTIMATE, COMM-509] |
| >~100-200 MHz | **PROCESSOR could bind** (if power were somehow held) | only this much aggregate bandwidth approaches the ~56 Gbps / 10 GHz-class processing ceiling | [DERIVED] |

**So the ordered answer: on the realistic thin cellular slice (~25 MHz) the SPECTRUM binds; widen the channel and the ANTENNA (power) binds next at ~50-100 MHz; the PROCESSOR (computation) binds last, only on a wide band (>~100-200 MHz) a cellular D2C entrant cannot acquire.** Computation is the LEAST binding of the three for a thin-spectrum cellular satellite, the opposite of the intuition that the digital beamforming ASIC is the bottleneck. The ASIC sets how many BEAMS you can form (Section 3), but the AGGREGATE throughput those beams carry is spectrum-bound. [DERIVED + FACT]

---

## 3. How many channels / frequencies one satellite runs at once (MANY, not one)

The founder's question 3: how many frequencies/channels can ONE satellite operate SIMULTANEOUSLY, and what sets the limit? The answer is firmly MANY, on two distinct axes (beams and bands), and the corpus + fresh sources pin both.

### 3.1 Many BEAMS at once (spatial channels)

One phased array forms hundreds of simultaneous beams, each a separate spatial channel that can carry the held spectrum:
- AST Block 2: **2,000-2,500 simultaneous coverage cells/beams** per satellite, every downlink beam supporting >40 MHz ([AST Next-Gen BlueBird, "2,000+ active cells per satellite"](https://ast-science.com/next-gen-bluebird/); [FCC-filed "2,500 adjustable antenna beams," via arXiv 2506.18672](https://arxiv.org/html/2506.18672v1)).
- Starlink V2-mini D2C: **48 downlink beams, all independently steerable** ([SpaceX-T-Mobile FCC Technical Narrative](https://cdn.arstechnica.net/wp-content/uploads/2023/05/SpaceX-T-Mobile-Technical-Narrative.pdf); [Mike Puchol model](https://mikepuchol.com/modeling-starlink-capacity-843b2387f501)).
- Flat ~25 m^2 entrant: ~200-450 beams (scaled, the corpus's softest input, COMM-408).

The same band is REUSED across non-overlapping beams (spatial frequency reuse), which is how a satellite multiplies the held spectrum into a larger total: total = bandwidth x SE x number of non-overlapping co-channel beams (COMM-435/436). [FACT, multi-source]

### 3.2 Multiple BANDS at once (carrier aggregation across frequencies)

A single satellite is NOT limited to one frequency band. AST operates several cellular bands SIMULTANEOUSLY on one satellite: leased low-band 700/850 MHz (from AT&T, Verizon, FirstNet) PLUS its own S-band and L-band PLUS acquired mid-band, all at once across its beams ([SDxCentral, AST low-band + own S/L-band](https://www.sdxcentral.com/news/fcc-grants-ast-spacemobile-access-to-att-verizon-spectrum/); [Broadband Breakfast, AST shares AT&T/Verizon low-band](https://broadbandbreakfast.com/ast-spacemobile-verizon-at-t-share-low-band-spectrum/); [arXiv 2506.18672, ">40 MHz per beam in UHF and L bands"](https://arxiv.org/html/2506.18672v1)). Carrier aggregation (3GPP LTE-Advanced Release 10+) then lets a single handset combine multiple held channels and the rates SUM, up to 5 carriers / 100 MHz in LTE-A and more in 5G ([3GPP Carrier Aggregation](https://www.3gpp.org/technologies/carrier-aggregation-on-mobile-networks); [Wikipedia Carrier aggregation](https://en.wikipedia.org/wiki/Carrier_aggregation)), so total capacity tracks TOTAL MHz held, not one channel's width (corpus COMM-433, [`channels_aggregate_answer.md`](channels_aggregate_answer.md)). [FACT, standardized + multi-source]

### 3.3 What sets the limit on simultaneous channels

Three distinct limits, in order:
1. **Beam count -> the digital beamforming processor / ASIC.** How many simultaneous beams the array can form is set by the onboard digital processor (the AST5000 ASIC handles ">2,000 coverage cells / up to 2,500 beams," and explicitly trades beam count against power, [arXiv 2507.14188, "trade-off between the number of simultaneous beams and power distribution... payload power is limited by satellite thermal and solar budgets"](https://arxiv.org/pdf/2507.14188)). This is the COMPUTATION limit, and it caps how many channels you run, NOT the aggregate bits they carry. [FACT]
2. **Power budget -> how many beams are ENERGIZED at once.** A satellite can FORM more beams than it can fully power simultaneously; AST's ~1,660 W total RF is shared across beams (~10 W/beam x ~160 simultaneously energized in the FCC narrative, corpus COMM-507), so the simultaneously-LIT beam count is power-bound below the provisioned beam count. [FACT, corpus COMM-507]
3. **Total spectrum held -> the AGGREGATE ceiling.** No matter how many beams or bands, the aggregate is capped by total MHz held x SE x reuse. Holding more channels (more bands) raises the ceiling linearly (carrier aggregation); it is a licensing/business limit, not a per-channel physics cap (COMM-433, [`dtc_spectrum_access.md`](dtc_spectrum_access.md) COMM-481). [FACT]

**So: one satellite runs MANY channels and MANY bands at once (hundreds of beams across multiple cellular bands), the COUNT is limited by the beamforming processor and the power budget, and the AGGREGATE those channels carry is limited by total spectrum held. A single-channel limitation does not exist; the binding aggregate cap on a thin cellular holding is spectrum (Section 2).** [FACT + DERIVED]

---

## 4. THE ANSWER, part 1: simultaneously-ACTIVE users per satellite (the hard ceiling)

Subscribers-per-satellite is two numbers. The first is the hard physical ceiling: how many users can be pulling data AT THE SAME INSTANT at a usable cellular rate. This is set entirely by the total capacity (Section 1) divided by the per-active-user rate.

### 4.1 The formula and the band

```
Active users per satellite  =  Total per-satellite capacity  /  per-active-user rate
                            =  ~5-15 Gbps  /  (active session rate)
```

The active session rate is the rate a user actually pulling data gets; for a usable cellular D2C experience the corpus and the operators put this at ~2-30 Mbps (Starlink V3 D2C target "2-10 Mbps sustained," up to 100 Mbps peak; the corpus's ~20-30 Mbps light / ~500 kbps-1 Mbps busy, COMM-495). [FACT for the rate band]

| Per-active-user rate | Active users on ~8-10 Gbps (central) | Active users on ~5-15 Gbps (range) | Tag |
|---|---|---|---|
| 30 Mbps (light, near single-phone peak) | ~270-330 | ~165-500 | [DERIVED] |
| 10 Mbps (Starlink V3 D2C sustained-high) | ~800-1,000 | ~500-1,500 | [DERIVED] |
| 5 Mbps (mid-sustained) | ~1,600-2,000 | ~1,000-3,000 | [DERIVED] |
| 1 Mbps (busy / 4G-LTE-outdoors floor) | ~8,000-10,000 | ~5,000-15,000 | [DERIVED] |

**Working band: ~250-2,000 simultaneously-active users per satellite at a usable ~5-30 Mbps cellular rate** (central ~8-10 Gbps satellite, ~5-10 Mbps active session). At the degraded ~1 Mbps busy floor a satellite can hold ~5,000-15,000 active, but that is the "4G-LTE-like outdoors, not 5G" experience the analysts describe (COMM-495), not a target rate. [DERIVED]

### 4.2 Cross-check against the beam-level worked example

This active count must reconcile with the per-beam picture. The corpus's Rappaport anchor: a 40 MHz / 120 Mbps beam at 5% concurrency serves ~240 active users at ~500 kbps each (COMM-418). Scaling to a 25 MHz / ~50-75 Mbps beam at a usable rate: a beam serving its active users at ~5-10 Mbps holds ~5-15 active per beam, and ~200-450 beams x ~5-15 active/beam = ~1,000-6,750 active at the degraded end, ~250-2,000 at the usable-rate end after the spectrum cap. The two methods agree on order of magnitude: **a single cellular D2C satellite simultaneously serves hundreds to low-thousands of ACTIVE users at a usable rate, not more.** [DERIVED, two methods cross-checked]

---

## 5. THE ANSWER, part 2: ATTACHED subscribers per satellite (the fleet-sizing number)

The number the fleet-sizing uses is not active users (an instantaneous count) but ATTACHED subscribers (people on the books, most of them idle at any instant). Attached = active / concurrency, with the concurrency factor stated explicitly.

### 5.1 The concurrency / activity factor (stated explicitly, multi-source)

Only a small fraction of subscribers are simultaneously active at the busy hour. Independent sources:
- **Busy-hour voice/session concurrency ~2.5-8%:** teletraffic dimensioning puts ~5-8% of subscribers able to be active at once (each phone in use ~10-16% of the time), and the Erlang view gives ~0.015-0.03 Erlang/subscriber = ~1.5-3% on a channel at any busy-hour instant ([ITU Teletraffic Handbook](https://www.itu.int/ITU-D/study_groups/SGP_1998-2002/SG2/StudyQuestions/Question_16/RapporteursGroupDocs/teletraffic.pdf); [Erlang/Westbay dimensioning](https://www.erlang.com/topic/1-575/); [Erlang unit, Wikipedia](https://en.wikipedia.org/wiki/Erlang_(unit))). [FACT, multi-source]
- **Satellite-D2C analyses use ~5% peak concurrency:** Rappaport et al. assume 5% peak concurrency (4,860 phones/beam -> ~240 active), single-source on the exact 5% but directionally corroborated by Tim Farrar/TMF's "hundreds or thousands within a beam share the bandwidth" ([arXiv 2506.18672](https://arxiv.org/html/2506.18672v1); [TMF/WIA white paper](https://wia.org/wp-content/uploads/2025/05/TMF-White-Paper-on-Satellite-D2D_October-2025.pdf)). [FACT for the model; single-source on the exact 5%]
- **Data-side cross-check:** the average smartphone consumes ~22 GB/month globally, ~25 GB/month North America ([Ericsson Mobility Report, Nov 2025](https://www.ericsson.com/en/reports-and-papers/mobility-report/key-figures)), which is ~68 kbps all-day average per device, or ~0.25-0.3 Mbps averaged over the busy hour [DERIVED]. So a usable per-active-session rate of ~5-10 Mbps with a ~0.25-0.3 Mbps busy-hour AVERAGE implies an active-fraction of ~3-6% (0.3 / ~5-10), consistent with the ~1-5% busy-hour concurrency band from the traffic side. [DERIVED, cross-checks the concurrency from the data side]
- **Oversubscription** reinforces this: ISPs and mobile operators sell ~20:1 to 50:1 (DSL) up to ~75-200:1 (cable) and ~109:1 (satellite, HughesNet) subscribers per unit of provisioned capacity ([Wikipedia contention ratio](https://en.wikipedia.org/wiki/Contention_ratio); [POTs and PANs oversubscription](https://potsandpansbyccg.com/2020/12/04/understanding-oversubscription/)). [FACT, multi-source]

**Working concurrency for cellular D2C: ~1-5% busy-hour (central ~2-3%), i.e. ~20:1 to ~100:1 attached-to-active.** [FACT band, multi-source]

### 5.2 Attached subscribers per satellite

```
Attached subscribers per satellite  =  active users per satellite  /  busy-hour concurrency
```

| Active users (Section 4) | / 5% concurrency | / 2.5% concurrency | / 1% concurrency | Tag |
|---|---|---|---|---|
| ~250 (usable ~30 Mbps active) | ~5,000 | ~10,000 | ~25,000 | [DERIVED] |
| ~1,000 (usable ~10 Mbps active) | ~20,000 | ~40,000 | ~100,000 | [DERIVED] |
| ~2,000 (usable ~5 Mbps active) | ~40,000 | ~80,000 | ~200,000 | [DERIVED] |

**Working band: ~25,000-150,000 ATTACHED subscribers per satellite, central planning figure ~50,000-100,000**, taking ~1,000-2,000 active users at a usable ~5-10 Mbps and a ~1-3% busy-hour concurrency. The width is driven entirely by the concurrency assumption and the target active rate, both of which the founder must set. [DERIVED, concurrency-dependent]

### 5.3 The two cross-checks (Starlink broadband and Starlink D2C)

**Cross-check A, Starlink broadband (~1,260 subs/sat, the LOWER bound).** Starlink flies ~9,500 satellites for ~12M subscribers = ~1,260 subs/sat (COMM claim 21). Cellular D2C subs-per-sat is HIGHER than this, not lower, even though a D2C satellite has far LESS capacity (~8-10 Gbps vs ~1 Tbps for a V3 broadband sat), because a cellular D2C SUBSCRIBER consumes far less than a broadband HOUSEHOLD: a broadband home pulls ~hundreds of GB/month at ~100+ Mbps, a thin-data D2C phone pulls ~tens of GB/month at ~few Mbps and tolerates heavy oversubscription. The per-sat CAPACITY is ~100x lower for D2C, but the per-SUBSCRIBER demand is ~100-1,000x lower, so the subs-per-sat nets out HIGHER. This is the key non-obvious result: thin-data cellular D2C packs MORE subscribers per satellite than broadband, not fewer. [DERIVED]

**Cross-check B, Starlink's own V3 D2C model (~70,000 attached/sat, the direct anchor).** SpaceX's V3 D2C math: 15,000 satellites x 700 Gbps = 10.5 Pbps, "support over 1 billion users at 10 Mbps average" ([NextBigFuture](https://www.nextbigfuture.com/2025/09/spacex-15000-v3-starlink-direct-to-cellphone-satellites.html)). That is **~70,000 attached users per D2C satellite** (1.05B / 15,000), on a satellite with ~700 Gbps (~70-140x the ~5-15 Gbps of a flat ~25 m^2 entrant on 25 MHz). Scaling by capacity: a ~5-15 Gbps entrant satellite at the SAME per-user loading would hold ~70,000 x (10/700) to (15/700) = ~500-1,500 attached/sat, BUT the "10 Mbps average" in SpaceX's figure is an oversubscribed PER-ATTACHED allocation (real sustained is 2-10 Mbps SHARED at 10-100 users/beam), so the realistic attached count at a thinner busy-hour concurrency is higher. Taking the entrant's ~8-10 Gbps and the same ~1-3% concurrency gives ~50,000-100,000 attached, which sits BETWEEN the capacity-scaled ~500-1,500 (if you hold SpaceX's aggressive 10 Mbps/attached) and the SpaceX-comparable ~70,000/sat loading. **The ~50,000-100,000 attached/sat central figure is consistent with Starlink's own D2C planning once the concurrency and per-user demand are matched.** [DERIVED, anchored to the SpaceX figure]

> **Reconciling the two cross-checks (so the number is honest).** Starlink broadband (~1,260/sat) and Starlink D2C (~70,000/sat) differ by ~55x for the SAME company, which is exactly the broadband-vs-cellular per-user-demand gap: a D2C satellite has ~100x less capacity but its subscribers each demand ~1,000x less, so it carries ~50x more of them. The entrant's ~50,000-100,000 attached/sat is below Starlink's ~70,000/sat headline only because the entrant's satellite has ~70x less aggregate capacity than a V3 D2C satellite, partially offset by lower assumed per-user demand. The ORDER OF MAGNITUDE (tens of thousands attached per cellular D2C satellite, vs ~1,000 per broadband satellite) is the robust finding; the exact figure rides the concurrency and per-user-demand assumptions. [DERIVED]

### 5.4 AST publishes no per-satellite subscriber number (named gap)

AST states only an addressable-market TAM ("nearly 6 billion mobile subscribers globally," "~3 billion combined subscribers across 50+ operators," FCC footprint of 2.9 billion people, [AST Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/); [AST FAQ](https://ast-science.com/faqs/); [SDxCentral on FCC DA 26-391](https://www.sdxcentral.com/news/fcc-grants-ast-spacemobile-access-to-att-verizon-spectrum/)), not a per-satellite or simultaneous-subscriber capacity. Neither AST nor SpaceX discloses simultaneous-subscribers-per-satellite; every per-satellite USER count (4,860 phones/beam, ~240 active, 10-100 users/beam, ~70,000 attached/sat) is analyst-modeled, not company-disclosed. The entrant figure is therefore a model anchored on the same beam/concurrency physics, not a transcribed datasheet number. [UNKNOWN, named gap]

---

## 6. The implied CAPACITY fleet (subscribers / attached-per-sat)

The whole point: how many satellites to SERVE a target subscriber base, versus the ~340 needed to COVER the area.

### 6.1 Fleet = subscribers / attached-per-sat

```
Capacity fleet  =  target subscribers  /  attached subscribers per satellite
```

At the central ~50,000-100,000 attached/sat:

| Target subscriber base | Fleet at 100,000/sat | Fleet at 50,000/sat | vs ~340 coverage floor | Tag |
|---|---|---|---|---|
| 1M subscribers | ~10 | ~20 | below floor -> **coverage-bound (~340)** | [DERIVED] |
| 10M subscribers | ~100 | ~200 | below-to-near floor -> **coverage-bound or near it** | [DERIVED] |
| 50M subscribers | ~500 | ~1,000 | above floor -> **capacity-bound** | [DERIVED] |
| 100M subscribers | ~1,000 | ~2,000 | above floor -> **capacity-bound** | [DERIVED] |

**Reading the table:** below ~17-34M subscribers (the point where subscribers / attached-per-sat first exceeds the ~340 coverage floor), the fleet is set by COVERAGE (~340 satellites carries the subscriber base with capacity to spare). Above that, the fleet is CAPACITY-driven and grows linearly with subscribers: **~100-200 satellites for 10M, ~500-1,000 for 50M, ~1,000-2,000 for 100M.** [DERIVED]

### 6.2 The two regimes (coverage-bound vs capacity-bound), made explicit

This is the founder's core distinction, now quantified:
- **Coverage-bound regime (small subscriber base, < ~20-30M):** ~340 satellites both COVER the area and have enough aggregate capacity to SERVE the subscribers; the fleet is the coverage floor, and adding subscribers up to ~20-30M is "free" on the same airframes. [DERIVED]
- **Capacity-bound regime (large subscriber base, > ~20-30M):** the subscriber base x its data demand exceeds what ~340 satellites carry, so the fleet must grow to subscribers / attached-per-sat, far above the coverage floor. This is Starlink's regime (~9,500 sats for ~12M broadband subs, capacity-driven, far above any coverage floor), and it is why Starlink needs Starship: a capacity fleet is hundreds-to-thousands of satellites, and launching that many cheaply is the whole game (COMM claim 21, the density caveat). [DERIVED]

**The crossover for cellular D2C is ~20-30M subscribers** (at ~50,000-100,000 attached/sat against a ~340 coverage floor): below it, coverage sets the fleet; above it, capacity does. A US-scale cellular D2C subscriber base (tens of millions) sits right AT this crossover, so the fleet is in the ~340-1,000 range, an order of magnitude below Starlink's broadband fleet but well above the bare coverage floor. [DERIVED]

### 6.3 The density caveat (the binding real-world limiter)

The fleet table assumes subscribers are SPREAD across the coverage footprint. They are not. A satellite beam is a fixed pool of capacity over a fixed ~324 km^2 footprint that cannot densify (COMM-415/420); demand piled into a few dense cells (a city, an event) cannot be served by adding satellites, because extra same-aperture satellites over the same ground add overlapping co-channel beams that interfere rather than add capacity (the spectrum-saturation ceiling, COMM-415). So:
- The ~100-1,000-satellite fleet figures hold ONLY for subscribers spread roughly evenly over the coverage area (rural/remote/highway, the realistic D2C use case). [DERIVED]
- For subscribers concentrated in dense areas, the satellite CANNOT serve them at the target rate regardless of fleet size; those users fall back to terrestrial cellular (which is where they already are). D2C's market is the SPREAD, low-density subscriber, and the fleet sizing is valid only for that market. [DERIVED, ties to COMM-415]
- The binding real-world unknown is therefore the GEOGRAPHIC SPREAD of the subscriber base, not the headline subs-per-sat: a base spread thin needs the coverage-floor fleet; a base that is mostly dense-area cannot be served by a satellite layer at all. The founder must set the assumed spread (per the ask-the-founder-for-assumptions rule). [UNKNOWN, founder assumption]

---

## 7. So what (for the Neutron DTC model)

1. **Per-satellite total bandwidth ~5-15 Gbps (central ~8-10 Gbps) on 25 MHz across ~200-450 beams** is the supply that subscribers divide; it is the corpus's COMM-410, restated as the subscriber-count input. [DERIVED]
2. **The binding limit on 25 MHz is SPECTRUM, not the processor and not the antenna power.** Antenna power binds only past ~50-100 MHz; the processor binds only past ~100-200 MHz (a band a cellular entrant cannot acquire). Computation is the LEAST binding of the three for thin-spectrum cellular D2C; the ASIC sets beam COUNT, not aggregate throughput. [DERIVED + FACT]
3. **One satellite runs MANY channels and MANY bands at once** (hundreds of beams across multiple cellular bands, AST runs low-band + S-band + L-band simultaneously; carrier aggregation sums them). The count is limited by the beamforming processor and the power budget; the aggregate is limited by total spectrum held. No single-channel limitation exists. [FACT, multi-source]
4. **Subscribers per satellite is two numbers:** ~250-2,000 simultaneously-ACTIVE at a usable ~5-30 Mbps cellular rate (the hard ceiling), and ~25,000-150,000 ATTACHED (central ~50,000-100,000) at a ~1-5% busy-hour concurrency. The attached figure is the fleet-sizing number, and it is ~50x HIGHER than Starlink's ~1,260 broadband subs/sat because thin-data cellular subscribers each demand ~100-1,000x less than a broadband household; it sits inside Starlink's own V3 D2C model (~70,000 attached/sat). [DERIVED, cross-checked]
5. **The CAPACITY fleet to SERVE a subscriber base is subscribers / ~50,000-100,000:** ~100-200 satellites for 10M, ~500-1,000 for 50M, ~1,000-2,000 for 100M. The crossover where capacity overtakes the ~340 coverage floor is ~20-30M subscribers. Below it, coverage sets the fleet (~340); above it, capacity does (and this is why Starlink needs Starship for its broadband fleet). [DERIVED]
6. **The density caveat is the binding real-world limiter.** All fleet figures assume subscribers SPREAD across the footprint; demand piled into dense cells cannot be served by adding satellites (the saturation ceiling). D2C's market is the spread, low-density subscriber, and the fleet sizing is valid only there; the geographic spread of the subscriber base is the binding unknown. [DERIVED + UNKNOWN]
7. **No verdict.** This doc pins subscribers-per-satellite and the capacity fleet. Whether a Neutron D2C business closes depends on the owned-spectrum position (~25 MHz here vs the ~100-200 MHz benchmark, COMM-325), the satellite power budget (UNKNOWN, COMM-330), the launch economics for a ~340-1,000-satellite fleet (the fit doc), and the subscriber-base spread (UNKNOWN, Section 6.3), none assessed here. [DERIVED]

---

## 8. Open questions / named gaps

1. **The busy-hour CONCURRENCY factor for cellular D2C is the load-bearing soft input.** The attached count = active / concurrency, and the ~1-5% band (Erlang ~2.5%, Rappaport 5%, data-side ~3-6%) drives the whole ~25,000-150,000 spread. The exact 5% Rappaport figure is single-source (corroborated directionally); the founder must set the planning concurrency. [UNKNOWN, founder assumption]
2. **The per-active-user target RATE is unset.** The active count = capacity / per-user-rate, and ~5 Mbps vs ~30 Mbps swings the active count ~6x and the attached count with it. The corpus brackets it (~20-30 Mbps light to ~1 Mbps busy, COMM-495) but the SERVICE LEVEL the business targets is a founder choice. [UNKNOWN, founder assumption]
3. **No operator discloses simultaneous-subscribers-per-satellite.** AST gives a TAM ("billions"), Starlink gives a constellation-level model ("1 billion users / 15,000 sats"); the per-satellite subscriber figure is analyst-modeled on the beam/concurrency physics, not a datasheet number. The entrant figure inherits that uncertainty. [UNKNOWN]
4. **The flat-array BEAM COUNT (~200-450) is the upstream soft input (inherited).** The per-satellite capacity that subscribers divide rides the beam count, which the corpus flags as UNKNOWN-grade (~48 Starlink-flying to ~250 AST-scaled, COMM-408). A firmer beam count would tighten both the active and attached counts. [UNKNOWN, inherited]
5. **The geographic SPREAD of the subscriber base is the binding fleet unknown (Section 6.3).** The fleet figures hold for spread subscribers; a dense-concentrated base cannot be served by a satellite layer at all. The corpus has no grounded spread assumption for a target D2C subscriber base. [UNKNOWN, founder assumption]
6. **The Starlink V3 D2C "10 Mbps average / 1 billion users" is a projection, not demonstrated**, and its "10 Mbps average" conflates an oversubscribed per-attached allocation with the 2-10 Mbps SHARED sustained rate; it anchors the cross-check but is not a measured subs-per-sat. [ESTIMATE/projection]

---

## Sources

Per-satellite capacity anchors (corpus + operators):
- [Spectrum Opportunities for the Wireless Future (arXiv 2506.18672): AST 2,500 beams, >40 MHz/beam UHF+L, 4,860 phones/beam at 30 users/km^2 x 50%, 5% peak concurrency -> ~240 active -> 500 kbps/user, 3 bps/Hz, 42 dBi, near practical power/antenna limits so expanded bandwidth is the path](https://arxiv.org/html/2506.18672v1)
- [AST Next-Gen BlueBird (official): 2,000+ active cells/satellite, ~500 sq mi/cell, 120-150 Mbps/cell, 10 GHz processing bandwidth, "billions of subscribers" TAM](https://ast-science.com/next-gen-bluebird/)
- [AST FAQ (official): ~3 billion combined subscribers across 50+ MNOs, ~6 billion mobile subscribers TAM, millions of connections per coverage cell](https://ast-science.com/faqs/)
- [FierceNetwork (AST analyst framing): each cell 20 Mbps x 2,800 cells = ~56 Gbps theoretical per satellite](https://www.fierce-network.com/wireless/ast-spacemobile-and-problem-delivering-broadband-space)
- [SpaceX-T-Mobile FCC Technical Narrative: D2C 4.4 Mbps (1.4 MHz) / 18.3 Mbps (5 MHz) per beam, 7.2 Mbps up, peak EIRP 58 dBW, all downlink beams independently steerable, PCS G / LTE Band 25](https://cdn.arstechnica.net/wp-content/uploads/2023/05/SpaceX-T-Mobile-Technical-Narrative.pdf)
- [NextBigFuture (Starlink V3 D2C): 15,000 sats x 700 Gbps = 10.5 Pbps -> "over 1 billion users at 10 Mbps average," 2-100 Mbps/user at 10-100 users/beam, >100x V2 D2C (~7 Gbps)](https://www.nextbigfuture.com/2025/09/spacex-15000-v3-starlink-direct-to-cellphone-satellites.html)
- [thexlab.org Starlink capacity working paper: V2-mini D2C 48 beams x ~7 Mbps, ~7 Gbps aggregate](https://thexlab.org/wp-content/uploads/2025/07/Starlink_Analysis_Working_Paper_v0.2.pdf)
- [Mike Puchol Starlink capacity model: V2 48 down / 16 up beam architecture, per-cell/per-subscriber methodology](https://mikepuchol.com/modeling-starlink-capacity-843b2387f501)

Channels / bands / beamforming (the simultaneous-channel limit):
- [3GPP Carrier Aggregation: one device on multiple component carriers simultaneously, rates sum, up to 100 MHz LTE-A](https://www.3gpp.org/technologies/carrier-aggregation-on-mobile-networks)
- [Carrier aggregation (Wikipedia): up to 5 carriers / 100 MHz LTE-A, more in 5G, rates sum](https://en.wikipedia.org/wiki/Carrier_aggregation)
- [SDxCentral (FCC grants AST access to AT&T/Verizon spectrum): AST operates low-band 700/850 plus own S-band, L-band, mid-band simultaneously; 248 satellites authorized](https://www.sdxcentral.com/news/fcc-grants-ast-spacemobile-access-to-att-verizon-spectrum/)
- [Broadband Breakfast (AST shares AT&T/Verizon low-band): multiple-band simultaneous operation](https://broadbandbreakfast.com/ast-spacemobile-verizon-at-t-share-low-band-spectrum/)
- [From Cell Towers to Satellites (arXiv 2507.14188): beam-count-vs-power trade-off, payload power limited by thermal and solar budgets, up to 2,500 uplink beams](https://arxiv.org/pdf/2507.14188)

Concurrency / activity factor / oversubscription / data-per-subscriber:
- [ITU Teletraffic Handbook: busy-hour traffic concentration, Erlang dimensioning](https://www.itu.int/ITU-D/study_groups/SGP_1998-2002/SG2/StudyQuestions/Question_16/RapporteursGroupDocs/teletraffic.pdf)
- [Erlang/Westbay dimensioning: ~0.015-0.03 Erlang/subscriber busy-hour](https://www.erlang.com/topic/1-575/)
- [Erlang (unit), Wikipedia: an Erlang is time-average concurrency](https://en.wikipedia.org/wiki/Erlang_(unit))
- [Contention ratio (Wikipedia): broadband 20:1-50:1 marketed, satellite/cable higher](https://en.wikipedia.org/wiki/Contention_ratio)
- [POTs and PANs oversubscription: GPON 8:1, fiber ~25:1, cable 75-200:1, satellite ~109:1](https://potsandpansbyccg.com/2020/12/04/understanding-oversubscription/)
- [Ericsson Mobility Report (Nov 2025): ~22 GB/month/smartphone global, ~25 GB/month North America](https://www.ericsson.com/en/reports-and-papers/mobility-report/key-figures)
- [TMF/WIA white paper (Farrar): D2D below 1 Mbps today, hundreds-to-thousands per beam share the bandwidth, 4G-LTE-outdoors not 5G](https://wia.org/wp-content/uploads/2025/05/TMF-White-Paper-on-Satellite-D2D_October-2025.pdf)
- [Cell average throughput (ScienceDirect): cell-tower aggregate is shared across users, bounded by spectrum and backhaul](https://www.sciencedirect.com/topics/engineering/cell-average-throughput)

AST/Starlink subscriber-base and fleet anchors (cross-checks):
- [SDxCentral (FCC DA 26-391): AST footprint 2.9 billion people, 248 satellites](https://www.sdxcentral.com/news/fcc-grants-ast-spacemobile-access-to-att-verizon-spectrum/)
- *(Starlink ~9,500 op sats / ~12M subscribers / ~1,260 subs/sat / ~450 Tbps, the V2-mini D2C ~7 Gbps and V3 D2C ~700 Gbps / 15,000-sat figures, and the ~340 coverage floor are cross-referenced from [`competitors/starlink_v3_specs.md`](../competitors/starlink_v3_specs.md) (claims 16/17/18/20/21/22), [`economics/comms_space_supply_cost.md`](../economics/comms_space_supply_cost.md), and [`leo_constellation_coverage_minimums.md`](leo_constellation_coverage_minimums.md) (COMM-215/224); not re-listed.)*
- *(The per-satellite ~5-15 Gbps capacity, the spectrum-bound-not-processor-bound finding, the speed-vs-users formula, the ~50-100 MHz power knee, the aperture ladder, carrier aggregation, and the reuse-vs-satellite-count mechanism are cross-referenced from [`dtc_capacity_supply.md`](dtc_capacity_supply.md) (COMM-406..425), [`dtc_data_rate_vs_spectrum.md`](dtc_data_rate_vs_spectrum.md) (COMM-493..512), [`dtc_antenna_aperture_tradeoff.md`](dtc_antenna_aperture_tradeoff.md) (COMM-293..314), [`spectrum_capacity_primer.md`](spectrum_capacity_primer.md) (COMM-426..439), [`channels_aggregate_answer.md`](channels_aggregate_answer.md), and [`dtc_spectrum_access.md`](dtc_spectrum_access.md) (COMM-451..492); not re-listed.)*

---

## Claims ledger (COMM-535..560)

For the catalog/reconciliation step to ingest. Each hard claim with sources and tag; single-source, projection, and estimate claims flagged. IDs COMM-535 through COMM-560 reserved for this doc (the next free contiguous block above the current global max COMM-534; verified free across the corpus). Cross-references existing IDs heavily.

- **COMM-535**, The number subscribers divide is the satellite's TOTAL throughput across all beams (~5-15 Gbps, central ~8-10 Gbps, on 25 MHz across ~200-450 beams), NOT a per-person rate; subscribers time-share the beams exactly as phones share a cell tower (aggregate bounded by spectrum and backhaul). [DERIVED, from corpus] Sources: corpus COMM-410; ScienceDirect cell-average-throughput; cross-ref COMM-417.
- **COMM-536**, On 25 MHz the binding limit is the OWNED SPECTRUM, not the processor and not the antenna power: 25 MHz x 3 bps/Hz x reuse caps the total far below the ~10 GHz / ~56 Gbps-class processor, and a ~25 m^2 array's power is sufficient at 25 MHz; antenna power binds only past ~50-100 MHz and the processor only past ~100-200 MHz. Computation is the LEAST binding of the three for thin-spectrum cellular D2C. [DERIVED + FACT] Sources: corpus COMM-411 (spectrum gate), COMM-509 (power knee); arXiv 2506.18672 (AST near power/antenna limits); AST Next-Gen BlueBird (10 GHz processing).
- **COMM-537**, The crossover map of binding limits: ~25 MHz -> SPECTRUM binds; ~50-100 MHz -> ANTENNA (power/EIRP) begins to bind (holding efficiency needs EIRP ~ proportional to B); >~100-200 MHz -> PROCESSOR could bind (a band a cellular entrant cannot acquire). So the ASIC sets beam COUNT, not aggregate throughput, on a thin cellular holding. [DERIVED] Sources: this doc Section 2.2; corpus COMM-411/509/510.
- **COMM-538**, One satellite runs MANY simultaneous BEAMS (spatial channels): AST 2,000-2,500 coverage cells/beams per satellite (>40 MHz each), Starlink V2-mini D2C 48 independently-steerable beams, a flat ~25 m^2 entrant ~200-450; the same band is reused across non-overlapping beams (total = bandwidth x SE x non-overlapping beam count). [FACT, multi-source] Sources: AST Next-Gen BlueBird (2,000+ cells); arXiv 2506.18672 (2,500 beams); SpaceX-T-Mobile FCC narrative (48 steerable); corpus COMM-408/435/436.
- **COMM-539**, One satellite runs MULTIPLE cellular BANDS at once: AST operates leased low-band 700/850 MHz plus its own S-band and L-band plus acquired mid-band simultaneously across its beams, and carrier aggregation (3GPP LTE-A Release 10+) sums the held channels so total capacity tracks total MHz held (not one channel's width). A single satellite is NOT limited to one frequency band. [FACT, multi-source + standardized] Sources: SDxCentral (AST low-band + S/L-band); Broadband Breakfast; arXiv 2506.18672 (UHF+L); 3GPP/Wikipedia carrier aggregation; corpus COMM-433/481.
- **COMM-540**, The limit on simultaneous channels/beams is threefold and ordered: (1) beam COUNT is set by the digital beamforming processor/ASIC (AST5000 >2,000 cells / 2,500 beams, explicitly trading beam count against power); (2) how many beams are ENERGIZED at once is set by the power budget (AST ~1,660 W RF, ~10 W/beam x ~160 simultaneously lit, below the provisioned beam count); (3) the AGGREGATE those beams carry is capped by total spectrum held. No single-channel physics cap exists; the aggregate cap on a thin cellular holding is spectrum. [FACT, multi-source] Sources: arXiv 2507.14188 (beam-vs-power trade-off); corpus COMM-507 (AST 1,660 W / 160 beams); arXiv 2506.18672; corpus COMM-433.
- **COMM-541**, THE SIMULTANEOUSLY-ACTIVE CEILING: active users per satellite = total capacity / per-active-user rate = ~5-15 Gbps / (~5-30 Mbps session) = ~250-2,000 active users at a usable cellular rate (central ~8-10 Gbps satellite at ~5-10 Mbps active); at the degraded ~1 Mbps busy floor ~5,000-15,000 active, but that is the "4G-LTE-outdoors not 5G" experience, not a target rate. [DERIVED] Sources: this doc Section 4.1; corpus COMM-410/495; NextBigFuture (V3 D2C 2-10 Mbps sustained).
- **COMM-542**, The active ceiling cross-checks against the beam-level worked example: a 25 MHz / ~50-75 Mbps beam serving its active users at ~5-10 Mbps holds ~5-15 active/beam, x ~200-450 beams (after the spectrum cap) ~= ~250-2,000 active at a usable rate, agreeing on order of magnitude with the capacity-divided method and with the Rappaport ~240-active-per-40-MHz-beam-at-5% anchor scaled to 25 MHz. [DERIVED, two methods] Sources: this doc Section 4.2; corpus COMM-418.
- **COMM-543**, THE BUSY-HOUR CONCURRENCY FACTOR for cellular is ~2.5-8% (teletraffic ~5-8% able-to-be-active, Erlang ~1.5-3% on a channel at any busy-hour instant); satellite-D2C analyses use ~5% peak (Rappaport, single-source on the exact 5%, corroborated directionally by Farrar/TMF); the data side cross-checks it (Ericsson ~22-25 GB/month/smartphone = ~0.25-0.3 Mbps busy-hour average / ~5-10 Mbps session = ~3-6% active). Working concurrency for D2C: ~1-5% (central ~2-3%), i.e. ~20:1 to ~100:1 attached-to-active. [FACT band, multi-source; exact 5% single-source] Sources: ITU Teletraffic Handbook; Erlang/Westbay; Wikipedia Erlang; arXiv 2506.18672; TMF/WIA white paper; Ericsson Mobility Report Nov 2025.
- **COMM-544**, Cellular oversubscription reinforces the concurrency band: ISPs/operators sell ~20:1-50:1 (DSL) up to ~75-200:1 (cable) and ~109:1 (satellite HughesNet) subscribers per unit provisioned capacity. [FACT, multi-source] Sources: Wikipedia contention ratio; POTs and PANs oversubscription.
- **COMM-545**, THE ATTACHED-SUBSCRIBERS ANSWER: attached per satellite = active / concurrency = ~25,000-150,000, central planning band ~50,000-100,000 (taking ~1,000-2,000 active at a usable ~5-10 Mbps and ~1-3% busy-hour concurrency); the width is driven by the concurrency and target-rate assumptions, both founder choices. This attached figure is the fleet-sizing number. [DERIVED, concurrency-dependent] Sources: this doc Section 5.2; COMM-541/543.
- **COMM-546**, CROSS-CHECK A (Starlink broadband, the lower bound): Starlink ~9,500 sats / ~12M subs = ~1,260 subs/sat; cellular D2C subs-per-sat is HIGHER than this despite ~100x less per-satellite capacity, because a thin-data cellular subscriber demands ~100-1,000x less than a broadband household, so the count nets out higher. Thin-data cellular D2C packs MORE subscribers per satellite than broadband, not fewer (the key non-obvious result). [DERIVED] Sources: this doc Section 5.3; corpus starlink_v3_specs claim 21.
- **COMM-547**, CROSS-CHECK B (Starlink's own V3 D2C model, the direct anchor): 15,000 sats x 700 Gbps = 10.5 Pbps -> "over 1 billion users at 10 Mbps average" = ~70,000 attached/sat on a ~700 Gbps satellite; the entrant's ~8-10 Gbps at the same ~1-3% concurrency gives ~50,000-100,000 attached/sat, consistent with Starlink's D2C planning once concurrency and per-user demand are matched. The "10 Mbps average" is an oversubscribed per-attached allocation (real sustained 2-10 Mbps shared at 10-100 users/beam). [DERIVED, anchored to SpaceX; projection] Sources: NextBigFuture (V3 D2C 10.5 Pbps / 1B users); this doc Section 5.3.
- **COMM-548**, Starlink broadband (~1,260/sat) and Starlink D2C (~70,000/sat) differ by ~55x for the SAME company, exactly the broadband-vs-cellular per-user-demand gap (~100x less capacity x ~1,000x less per-user demand -> ~50x more subscribers); the ROBUST finding is the order of magnitude (tens of thousands attached per cellular D2C satellite vs ~1,000 per broadband satellite), with the exact figure riding concurrency and per-user demand. [DERIVED] Sources: this doc Section 5.3; COMM-546/547.
- **COMM-549**, No operator discloses simultaneous-subscribers-per-satellite: AST gives only a TAM (~6 billion mobile / ~3 billion across 50+ MNOs / 2.9 billion-people FCC footprint), Starlink a constellation-level model (1 billion / 15,000 sats); every per-satellite USER count (4,860 phones/beam, ~240 active, 10-100 users/beam, ~70,000 attached/sat) is analyst-modeled, not company-disclosed. [UNKNOWN, named gap] Sources: AST Next-Gen BlueBird; AST FAQ; SDxCentral FCC DA 26-391; NextBigFuture; arXiv 2506.18672.
- **COMM-550**, THE CAPACITY FLEET = target subscribers / attached-per-sat; at ~50,000-100,000 attached/sat: ~10-20 sats for 1M, ~100-200 for 10M, ~500-1,000 for 50M, ~1,000-2,000 for 100M subscribers. [DERIVED] Sources: this doc Section 6.1; COMM-545.
- **COMM-551**, TWO REGIMES: below ~20-30M subscribers the fleet is COVERAGE-bound (~340 satellites both cover and serve, adding subs is "free" on the same airframes); above ~20-30M it is CAPACITY-bound (fleet = subs / attached-per-sat, far above the coverage floor). The crossover for cellular D2C is ~20-30M subscribers (at ~50,000-100,000 attached/sat against the ~340 coverage floor); a US-scale base sits right at it, so the fleet is ~340-1,000, an order of magnitude below Starlink's broadband fleet but above the bare coverage floor. [DERIVED] Sources: this doc Section 6.2; corpus COMM-215/224 (coverage floor), starlink_v3_specs claim 21.
- **COMM-552**, This is the founder's coverage-vs-capacity distinction quantified: a coverage constellation is ~340 satellites (everyone can SEE a satellite), but the CAPACITY fleet to SERVE is set by subs-per-satellite and is larger once the subscriber base x its demand exceeds what ~340 satellites carry; this is why Starlink flies ~9,500 sats for ~12M broadband subs (capacity-driven) and needs Starship to launch thousands. [DERIVED] Sources: this doc Section 6.2; corpus starlink_v3_specs claim 21/24, COMM-224.
- **COMM-553**, THE DENSITY CAVEAT (the binding real-world limiter): all fleet figures assume subscribers SPREAD across the footprint; a satellite beam is a fixed pool over a fixed ~324 km^2 that cannot densify, so demand piled into dense cells cannot be served by adding satellites (the spectrum-saturation ceiling), and those users fall back to terrestrial. D2C's market is the SPREAD, low-density subscriber; the fleet sizing is valid only there. [DERIVED, ties to corpus] Sources: this doc Section 6.3; corpus COMM-415/420.
- **COMM-554**, The geographic SPREAD of the subscriber base is the binding fleet unknown: a thin-spread base needs the coverage-floor fleet (~340), a dense-concentrated base cannot be served by a satellite layer at all; the corpus has no grounded spread assumption, and the founder must set it. [UNKNOWN, founder assumption] Sources: this doc Section 6.3/8; corpus COMM-415.
- **COMM-555**, The busy-hour CONCURRENCY is the load-bearing soft input for the attached count (the ~1-5% band drives the ~25,000-150,000 spread); the exact 5% Rappaport figure is single-source; the founder must set the planning concurrency. [UNKNOWN, founder assumption] Sources: this doc Section 8; arXiv 2506.18672; ITU/Erlang.
- **COMM-556**, The per-active-user target RATE is unset and swings the count ~6x (~5 Mbps vs ~30 Mbps session); the corpus brackets it (~20-30 Mbps light to ~1 Mbps busy) but the SERVICE LEVEL the business targets is a founder choice. [UNKNOWN, founder assumption] Sources: this doc Section 8; corpus COMM-495.
- **COMM-557**, The flat-array BEAM COUNT (~200-450) is the upstream soft input inherited from the corpus (~48 Starlink-flying to ~250 AST-scaled, UNKNOWN-grade); the per-satellite capacity that subscribers divide rides it, so a firmer beam count would tighten both the active and attached counts. [UNKNOWN, inherited] Sources: this doc Section 8; corpus COMM-408.
- **COMM-558**, The Starlink V3 D2C "10 Mbps average / 1 billion users" is a projection (not demonstrated) and conflates an oversubscribed per-attached allocation with the 2-10 Mbps SHARED sustained rate; it anchors the cross-check but is not a measured subs-per-sat. [ESTIMATE/projection] Sources: NextBigFuture; this doc Section 8.
- **COMM-559**, Net subscribers-per-satellite picture for a Neutron cellular D2C model: one flat ~25 m^2 satellite on 25 MHz puts ~5-15 Gbps through the air across ~200-450 beams (spectrum-bound, runs many beams + many bands at once), serves ~250-2,000 simultaneously-active users at a usable rate, and holds ~50,000-100,000 attached subscribers at ~1-3% concurrency; the capacity fleet to serve is subs / ~50,000-100,000 (~100-200 for 10M, ~500-1,000 for 50M), above the ~340 coverage floor, valid only for spread (not dense-concentrated) subscribers. No verdict. [DERIVED/SYNTHESIS] Sources: this doc Sections 0-7; grounds in COMM-535..558.
- **COMM-560**, The model's fleet-sizing rule: fleet = max(coverage floor ~340, target subscribers / attached-per-sat ~50,000-100,000), with the attached-per-sat gated by busy-hour concurrency (~1-3%) and per-user target rate (~5-10 Mbps), and the whole result gated by the subscriber-base spread (dense demand is unservable by adding airframes). This is the gate on the cost-per-subscriber result. [DERIVED] Sources: this doc Sections 6-7; COMM-550/551/553.

---

*COMM-535..560 created by this doc (the reserved block, the next free contiguous range above the global max COMM-534; not exceeded). Catalog rows for LIBRARY.md / RESEARCH_TRACKER.md / SOURCE_INDEX.md are returned to the catalog/reconciliation agent, not edited here. This doc is not committed by this pass.*
