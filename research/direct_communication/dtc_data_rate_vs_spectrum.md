# Direct-to-Cell Data Rate vs Owned Spectrum: the Rate-vs-Bandwidth Curve for a Flat ~25 m^2 Flatellite, and Whether BANDWIDTH or POWER Is the Binding Limit as the Channel Widens

**Research date:** 2026-06-23
**Status:** Understanding-building input for the Neutron direct-to-cell (DTC) model. No go/no-go verdict. This doc pins the CENTRAL OUTPUT the model needs: the deliverable data rate to a phone, and how it scales as the model's central dial (total OWNED bandwidth) is swept 25 -> 50 -> 100 -> 200 MHz, given that separate channels SUM via carrier aggregation. It confirms the single-phone and per-user rate at 25 MHz against independent sources, delivers the rate-vs-spectrum-held TABLE, and answers the founder's exact question: as the channel widens, does BANDWIDTH (spectrum held) or POWER (the link SNR) bind, and where does power start to bind? Every value is flagged sourced (FACT) / derived (DERIVED) / estimate (ESTIMATE) / unknown (UNKNOWN).

> **Why this document exists.** The corpus owns the per-phone operating point and the per-cell capacity, and it correctly states that rate = bandwidth x spectral efficiency and is "linear in bandwidth AT CONSTANT spectral efficiency." But it explicitly FLAGS, three times and never resolves, that a small flat array spreading FIXED power over a wider channel may NOT hold ~2 to 3 bps/Hz, because SNR-per-Hz falls as the channel widens ([`dtc_per_phone_rate_and_latency.md`](dtc_per_phone_rate_and_latency.md) Section 2.4 point 2, COMM-348, COMM-378; open question 4). The model's CENTRAL DIAL is the total owned bandwidth swept 25 to 200 MHz, so whether that dial is LINEAR (every MHz buys proportional rate) or SATURATING (the rate plateaus and power becomes the wall) is the single most load-bearing un-pinned relationship in the whole DTC supply chain. This doc resolves it, multi-source. The answer changes how the founder should think about the bandwidth dial: it is linear ONLY if power is grown with it; at fixed power it saturates, and POWER becomes the binding limit somewhere in the ~50 to 100 MHz region.

> **Grounds in and does NOT re-derive (this doc adds the RATE-vs-OWNED-BANDWIDTH CURVE and the POWER-vs-BANDWIDTH LIMIT layer on top of the per-phone and per-cell numbers the corpus owns):**
> - [`dtc_per_phone_rate_and_latency.md`](dtc_per_phone_rate_and_latency.md) (COMM-336..378, esp. Section 2.6 and COMM-371..378): owns the single-phone PEAK (~25 to 50 Mbps), the flat ~25 m^2 link-parity-with-BW3 result (COMM-373/375), and the R = B x efficiency method (COMM-374). This doc takes the 25 MHz operating point as given, EXTENDS the curve to 50/100/200 MHz, and resolves the constant-efficiency FLAG the corpus left open (COMM-348/378).
> - [`dtc_capacity_supply.md`](dtc_capacity_supply.md) (COMM-406..425): owns the per-cell formula per_user = (B x SE) / active-users (COMM-417), the ~50 to 75 Mbps/cell on 25 MHz (COMM-409), and the spectrum-saturation ceiling. This doc uses those and adds the per-Hz efficiency behavior under widening bandwidth at fixed power.
> - [`dtc_antenna_aperture_tradeoff.md`](dtc_antenna_aperture_tradeoff.md) (COMM-293..314): owns the handset link budget (the bare phone supplies nothing, the satellite supplies the ~25 dB the path eats, COMM-294) and G = 4 pi eta A / lambda^2 (COMM-296). This doc uses the link budget as the reason the link is POWER-LIMITED and adds the bandwidth dimension to it.
> - [`spectrum_capacity_primer.md`](spectrum_capacity_primer.md) (COMM-426..439): owns Shannon C = B x log2(1+SNR) (COMM-427), the corrected "25 MHz is NOT capped at 75 Mbps" finding (COMM-430..432), carrier aggregation summing channels (COMM-433), and the ~0.5 to 0.8 bps/Hz measured / ~3 bps/Hz claimed efficiency band (COMM-428/429). This doc applies all of those across the 25 to 200 MHz sweep and pins the power-limited wideband behavior the primer only implied.
> - [`dtc_spectrum_access.md`](dtc_spectrum_access.md) (COMM-451..492) and [`channels_aggregate_answer.md`](channels_aggregate_answer.md): own the SPECTRUM-AVAILABILITY side (the phone re-couples you to ~600 MHz to ~2 GHz cellular bands; carrier aggregation sums held channels so total capacity is bounded by how much spectrum you HOLD, a licensing limit). This doc is the complement: it owns the RATE the held spectrum delivers and whether the rate dial saturates before the holding does.
> - Cross-references (not re-listed): [`dtc_system_model.md`](dtc_system_model.md) (the governing rule, the UNKNOWN Flatellite power COMM-330), [`spectrum_purchase_and_6g.md`](spectrum_purchase_and_6g.md) (the 100 to 200 MHz competitive holding benchmark).

> **Tagging.** **[FACT]** sourced (2+ independent sources unless flagged single-source), **[DERIVED]** computed in this doc from sourced inputs, **[ESTIMATE]** a third-party model/target/projection, **[UNKNOWN]** a named gap (not invented). New claims use **COMM-493..520**. The block COMM-451..492 is already held by [`dtc_spectrum_access.md`](dtc_spectrum_access.md) (the prior wave-4 doc), so per the contiguity rule COMM-493 is the next free start above the current global max (COMM-492); the ceiling is not exceeded. No em-dashes anywhere. Inline math: `^2` squared, `x` multiply, `->` arrow, `log2` base-2 log.

---

## 0. Answer first (the rate-vs-spectrum curve and the power wall in one screen)

**At 25 MHz of owned spectrum a flat ~25 m^2 array at ~400 km delivers ~25 to 50 Mbps to one lightly-loaded phone (single-phone PEAK) and ~20 to 30 Mbps sustained per user at ~2 to 4 active users per cell, both well-supported by independent demonstrations and analyst data. But the central dial does NOT scale linearly as you widen the channel at FIXED satellite power. A DTC-to-phone link sits at a MEASURED ~0 dB SNR (Starlink's live network), which is deep in the POWER-LIMITED regime, where Shannon capacity is set by total power P/N0 and is nearly INDEPENDENT of bandwidth. Spreading the same power over more hertz lowers the power-spectral-density, lowers SNR-per-Hz, and lowers spectral efficiency, so going 25 -> 200 MHz (8x the bandwidth) at fixed power raises the single-phone rate only ~1.36x (a hard ceiling of ~1.44x = log2(e), the wideband Shannon limit), NOT 8x. The rate scales linearly with owned bandwidth ONLY if the satellite raises EIRP proportionally to the bandwidth (8x bandwidth -> ~8x power) to hold the power-spectral-density and thus the efficiency constant. Whether it can is a POWER question, and anchored to the real DTC analogs (Starlink ~25 m^2 D2C, AST ~199 m^2 BlueBird) a flat ~25 m^2 array's fixed power gets spread below ~1 to 2 bps/Hz somewhere in the ~50 to 100 MHz region. So the binding limit FLIPS as the channel widens: at ~25 to 50 MHz the model is BANDWIDTH-limited (more spectrum is the lever, rate is roughly linear because power can still hold the PSD), and past ~50 to 100 MHz it becomes POWER-limited (more spectrum stops buying rate to one phone; the lever becomes EIRP/power or serving more users instead of one user faster). The regulatory PFD cap does NOT bind the in-band rate first (the FCC declined in-band downlink PFD limits).**

1. **The 25 MHz operating point, confirmed (Section 1).** Single-phone PEAK ~25 to 50 Mbps is corroborated and arguably conservative: AST demonstrated up to ~21 Mbps to one phone on a ~64 m^2 array on a thin channel and ~98.9 Mbps with Block 1, while Starlink's measured single-user-when-alone bound is ~3.1 Mbps on just 2x5 MHz at ~0.6 bps/Hz (which scales to ~15 to 20 Mbps on 25 MHz). The sustained per-USER-under-load number (~20 to 30 Mbps at 2 to 4 active users, falling to ~1 Mbps or less when busy, ~500 kbps at ~5% beam load) is confirmed by two independent primary sources (Tim Farrar/WIA and Rappaport et al.). [FACT, multi-source]

2. **The rate-vs-spectrum-held curve (Section 2), the central output.** Two cases, and the model must state which it is using:
   - **Constant-efficiency (power grows with bandwidth):** rate is LINEAR. R = B x SE at ~2 to 3 bps/Hz gives, single-phone, 25 MHz -> 50 to 75 Mbps, 50 MHz -> 100 to 150 Mbps, 100 MHz -> 200 to 300 Mbps, 200 MHz -> 400 to 600 Mbps. This holds ONLY if the array raises power ~proportionally to B to hold the PSD. [DERIVED]
   - **Fixed-power (the founder's exact concern):** rate SATURATES. Anchoring SNR ~ 1 (0 dB) at 25 MHz, the efficiency falls ~half per doubling of bandwidth, so 25 MHz -> ~25 Mbps, 50 MHz -> ~29 Mbps, 100 MHz -> ~32 Mbps, 200 MHz -> ~34 Mbps, hard-capped at ~1.44x the 25 MHz rate no matter how much spectrum is added. [DERIVED, multi-source physics]
   - The truth sits BETWEEN these, set by how much extra power the array can spend as B grows. The corpus's "linear in bandwidth at constant efficiency" is the OPTIMISTIC case and is only valid while power can hold the PSD. [DERIVED]

3. **Power vs bandwidth, the binding limit (Section 3).** The Shannon physics is unambiguous and triple-sourced (Forney/MIT, Wikipedia, Tse and Viswanath): in the power-limited ~0 dB regime, capacity = (P/N0) x log2(e) is bandwidth-independent. To hold linear scaling, EIRP must scale ~linearly with B. Bounded against AST BlueBird (1,660 W total RF, ~30 m^2 solar, ~199 m^2 array) and Starlink D2C (~25 m^2, peak EIRP density ~+57.7 dBW/MHz), a flat ~25 m^2 entrant is Starlink-class in EIRP density, so its fixed power is spread below ~1 to 2 bps/Hz somewhere in the ~50 to 100 MHz region. **The binding limit is BANDWIDTH at ~25 to 50 MHz and flips to POWER past ~50 to 100 MHz.** The exact knee slides with the entrant's total power budget, which is UNKNOWN for both the entrant and Starlink D2C (the load-bearing gap). The regulatory PFD cap does not bind the in-band carrier first. [DERIVED + FACT; power budget UNKNOWN]

The rest sources and derives each point.

---

## 1. The 25 MHz operating point, confirmed against independent sources

The corpus already pins these two numbers; this section re-validates them against fresh independent datapoints (the prompt's requirement 1) before extending the curve.

### 1.1 The single-phone PEAK rate (~25 to 50 Mbps), and every DTC single-device datapoint found

The single-phone peak is the rate one lightly-loaded phone gets when it is alone in the cell and the scheduler hands it the whole beam (the corpus's converge rule, COMM-339). The independent demonstration datapoints, gathered to triangulate what a ~25 m^2 array at ~400 km on ~25 MHz can do to one phone:

| Operator / system | Array | Spectrum | Single-DEVICE rate | Tag |
|---|---|---|---|---|
| AST BlueWalker 3 (test article) | ~64 m^2 | AT&T LTE low/mid-band, ~one ~5 MHz channel | up to ~21 Mbps to one phone (also ~10.3, ~14 Mbps milestones) | [FACT] |
| AST BlueBird Block 1 | ~64 m^2 | LTE carrier spectrum | peak ~98.9 Mbps to a standard phone (field test) | [FACT] |
| AST BlueBird Block 2 (design) | ~199 to 223 m^2 | up to 40 MHz/beam | ~200 Mbps peak per device (design); 120 Mbps/cell | [FACT for design target] |
| Starlink Direct-to-Cell (MEASURED) | ~25 m^2-class | 2x5 MHz (PCS G-block) | ~3.1 Mbps/beam = single-user-occupies-beam bound, at ~0.6 bps/Hz | [FACT, measured] |
| Starlink DTC (stated target) | ~25 m^2-class | growing | "up to 100 Mbps" peak / 2 to 10 Mbps sustained per phone | [FACT for the stated target] |
| Lynk Global | small | carrier spectrum | voice + 2-way SMS demonstrated; NO published single-phone Mbps | [UNKNOWN Mbps] |
| Globalstar / Apple Emergency SOS | MSS | narrowband | bytes-to-tens-of-bytes/sec class (no Mbps) | [ESTIMATE / single-source] |
| Huawei / China Telecom (Tiantong) | GEO | narrowband | satellite voice/SMS; no handset-link Mbps published | [single-source] |

Sources: AST BW3 ~10/14/21 Mbps ([Fierce](https://www.fierce-network.com/tech/ast-spacemobile-touts-10-mbps-download-speeds-during-tests-hawaii), [RCR Wireless](https://www.rcrwireless.com/20230622/featured/ast-spacemobile-hits-space-based-lte-speeds-of-10-mbps-using-att-spectrum)); AST Block 1 ~98.9 Mbps ([TelecomTalk](https://telecomtalk.info/ast-spacemobile-100mbps-broadband-space-standard-phone/1007598/), [TechTimes](https://www.techtimes.com/articles/318740/20260620/ast-spacemobile-block-2-bluebirds-reach-orbit-satellite-broadband-direct-your-phone-nears.htm)); AST Block 2 ~200 Mbps design ([BusinessWire](https://www.businesswire.com/news/home/20260617420856/en/AST-SpaceMobile-Announces-Successful-Orbital-Launch-of-BlueBirds-8-9-and-10), [AST Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/)); Starlink measured ~3.1 Mbps/beam, ~0.6 bps/Hz ([arXiv 2506.00283](https://arxiv.org/html/2506.00283v7)); Starlink targets ([NextBigFuture FCC 4G/5G power](https://www.nextbigfuture.com/2025/03/fcc-allows-spacex-starlink-direct-to-cellphone-power-for-4g-5g-speeds.html)); Lynk ([Wikipedia/Lynk](https://en.wikipedia.org/wiki/Lynk_Global)); Globalstar/Apple ([Apple support](https://support.apple.com/en-us/122339)).

**Triangulated verdict on the single-phone peak [DERIVED, cross-checked].** The ~25 to 50 Mbps corpus estimate is WELL-SUPPORTED and the band is genuinely efficiency-driven:
- AST's ~98.9 Mbps with a ~64 m^2 array and ~21 Mbps with BW3 set the high anchor; a ~25 m^2 array has ~0.4x AST's aperture area (~4 dB less gain, COMM-372), and at low orbit (~+3.5 to 3.9 dB, COMM-346) sits at near-parity with the BW3 link (COMM-373), so it reaches the tens-of-Mbps band but not ~100 Mbps.
- Starlink's measured ~3.1 Mbps on 2x5 MHz at ~0.6 bps/Hz scales to ~15 to 20 Mbps on 25 MHz (Starlink's own paper projects ~12.4 to 15.5 Mbps per user at 2x25 MHz). This is the FLOOR if the array only achieves Starlink-grade efficiency.
- So the band is: **~15 to 20 Mbps at Starlink-measured efficiency (~0.6 bps/Hz), ~50 to 75 Mbps at AST-claimed efficiency (~3 bps/Hz)**; the corpus's ~25 to 50 Mbps is a sound central estimate, with the explicit caveat that it assumes the array achieves better-than-Starlink efficiency (~2 to 3 bps/Hz), which is the load-bearing assumption (Section 2). [DERIVED]

### 1.2 The sustained per-USER rate under realistic load (~20 to 30 Mbps light, ~1 Mbps or less busy), confirmed

The per-user rate under load is the per-cell pool divided by active users (the corpus formula per_user = (B x SE) / active-users, COMM-417). Independent corroboration, the prompt's requirement 1:

- **Tim Farrar / WIA white paper (analyst) [FACT]:** "Current performance for satellite D2D is below 1 Mbps download, and future systems are expected to reach 4G LTE-like speeds outdoors, not 5G, with any connections indoors being even slower," because "only a few tens of MHz of spectrum is available for D2D and each satellite beam covers huge areas... which forces users to share limited bandwidth" ([WIA/TMF white paper, Oct 2025](https://wia.org/wp-content/uploads/2025/05/TMF-White-Paper-on-Satellite-D2D_October-2025.pdf), [WIA summary](https://wia.org/satellite-d2d-and-terrestrial/)).
- **Rappaport et al. (independent academic, the worked example) [FACT]:** verbatim, "Assuming a spectral efficiency of 3 bps/Hz... a 40-MHz beam could support a total downlink rate of 120 Mbps," and "a single beam would encompass 324x30x0.5 = 4860 smartphones... Assuming 5% peak concurrency usage, about 240 of these phones would be active... for an equal-division allocation of 500 kbps per user, far from broadband rates" ([arXiv 2506.18672](https://arxiv.org/html/2506.18672v1), also [npj Wireless Technology](https://www.nature.com/articles/s44459-025-00008-9)). This is EXACTLY the corpus formula: 120 Mbps / 240 active = 500 kbps.
- **Starlink measured [FACT]:** the ~3.1 Mbps/beam is explicitly "an upper-bound... single user occupying the full bandwidth of the beam," so any multi-user load divides below it; Starlink's FCC framing is 2 to 100 Mbps/user "depending on beam sharing (10 to 100 users/beam)," i.e. ~1 Mbps or less at 100 users ([arXiv 2506.00283](https://arxiv.org/html/2506.00283v7)).

**Verdict [FACT, multi-source].** The corpus picture is confirmed on both ends: at the LIGHT end (2 to 4 active users on 25 MHz at SE 2 to 3), per-user = 50 to 75 Mbps / 2 to 4 = ~15 to 35 Mbps (the corpus ~20 to 30 Mbps); at the BUSY end (hundreds of active phones), per-user falls to ~500 kbps to ~1 Mbps (Farrar, Rappaport, Starlink all agree). The ~20 to 30 Mbps headline is a low-concurrency / lightly-loaded number, not a whole-population number. No independent datapoint contradicts the corpus.

### 1.3 The 25 MHz x efficiency table, and AST 120 Mbps/cell = 40 MHz x 3 bps/Hz, confirmed

Rate = B x SE at B = 25 MHz, the per-cell number a sole-occupant phone sees as its peak [DERIVED]:

| Spectral efficiency (bps/Hz) | Cell rate on 25 MHz | Efficiency anchor |
|---|---|---|
| 0.5 to 0.6 | ~13 to 15 Mbps | Starlink MEASURED (median 0.52, mean 0.61) |
| 0.8 | ~20 Mbps | Starlink upper-measured |
| 1.5 | ~37.5 Mbps | 4G-LTE average grade |
| 2.0 | 50 Mbps | conservative data-grade |
| 2.5 | 62.5 Mbps | mid |
| 3.0 | 75 Mbps | AST-claimed commercial |

AST's "120 Mbps per cell" = 40 MHz x 3 bps/Hz is confirmed from 2+ independent sources: AST official ("peak speeds of 120 Mbps per coverage cell," up to 40 MHz/beam, [AST Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/)) and the independent Rappaport analysis (verbatim "spectral efficiency of 3 bps/Hz... a 40-MHz beam could support 120 Mbps," [arXiv 2506.18672](https://arxiv.org/html/2506.18672v1)). [FACT, multi-source] This anchors the high end of the efficiency band; the Starlink MEASURED ~0.5 to 0.6 bps/Hz anchors the low end ([arXiv 2506.00283](https://arxiv.org/html/2506.00283v7)). The efficiency assumption is the entire swing, exactly as the primer found (COMM-430/431).

**A framing nuance to carry (not a contradiction):** AST Block 2 is quoted two ways: 120 Mbps PER CELL (the shared capacity, 40 MHz x 3) and ~200 Mbps PER DEVICE (the best-case single-device peak, implying more aggregated bandwidth and/or higher efficiency for one lit-up handset). The corpus's use of 120 Mbps/cell as the capacity number is the correct conservative choice; ~200 Mbps is a device peak, not cell capacity. [FACT, reconciled]

---

## 2. The rate-vs-owned-bandwidth curve (25 -> 50 -> 100 -> 200 MHz): linear or saturating?

This is the central output. The corpus says rate is "linear in bandwidth at CONSTANT spectral efficiency" (COMM-374/430) but FLAGS that constant efficiency may not hold as a small flat array spreads fixed power over a wider channel (COMM-348/378). This section resolves the flag, multi-source. The answer is a fork, and the model must state which branch it is on.

### 2.1 The physics: a DTC-to-phone link is POWER-LIMITED, so widening at fixed power does NOT scale linearly

The Shannon law is C = B x log2(1 + SNR), and the crucial term is how SNR depends on bandwidth. For a transmitter with roughly FIXED received signal power P, the noise grows with bandwidth (noise power = N0 x B), so:

```
   SNR = P / (N0 x B)          (SNR is INVERSELY proportional to bandwidth at fixed power)
```

[FACT, multi-source: [arXiv 0812.1553](https://arxiv.org/pdf/0812.1553) ("as the bandwidth increases, the average SNR = P/(N0 B) and the spectral efficiency decreases... as B increases, SNR approaches zero and we operate in the low-SNR regime"); [ScienceDirect, System Spectral Efficiency](https://www.sciencedirect.com/topics/engineering/system-spectral-efficiency) ("the available transmitter power is inversely proportional to the total number of spectrum slices that share the same aggregate transmitter power")].

This splits all radio links into two regimes ([FACT, multi-source: [Forney, MIT OCW 6.451 Ch.4](https://ocw.mit.edu/courses/6-451-principles-of-digital-communication-ii-spring-2005/b286123989945cef13e5a9aa20e56a18_chap4.pdf); [Wikipedia, Shannon-Hartley](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem)]):
- **Bandwidth-limited (high SNR, efficiency >> 1 bps/Hz):** efficiency is roughly FLAT as bandwidth grows, so rate IS ~linear in bandwidth. Forney's boundary is efficiency ~ 2 bps/Hz.
- **Power-limited (low SNR, efficiency << 1 bps/Hz):** capacity is "linear in power" and becomes nearly INDEPENDENT of bandwidth; adding bandwidth spreads the power thinner and buys diminishing rate.

In the power-limited regime the capacity converges, as bandwidth grows at fixed power, to a hard ceiling set ENTIRELY by power [FACT, multi-source]:

```
   C_infinity = (P / N0) x log2(e) = 1.44 x (P / N0)      (the wideband / infinite-bandwidth Shannon limit)
```

[FACT: [Wikipedia, Shannon-Hartley "power-limited case"](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem) ("the capacity is linear in power... capacity is independent of bandwidth if the noise is white," C approx 1.44 x S/N0); [dsplog](https://dsplog.com/2008/06/18/bounds-on-communication-shannon-capacity/) ("increasing bandwidth alone will not lead to increase of the capacity"); Tse and Viswanath, [Fundamentals of Wireless Communication Ch.5](https://web.stanford.edu/~dntse/Chapters_PDF/Fundamentals_Wireless_Communication_chapter5.pdf) (capacity = Theta(P/N0), "virtually independent of bandwidth" in the power-limited regime)]. The textbook states the intuition for exactly this situation (a power-limited link with all the bandwidth you want): Forney's deep-space example concludes "increasing P/N0 by 3 dB will now double the achievable rate R," i.e. rate tracks POWER, not bandwidth, once you are power-limited.

**Which regime is DTC-to-phone in? Power-limited, near-maximally.** The corpus and the fresh sources agree the link sits at a MEASURED ~0 dB SINR (SNR ~ 1):
- Starlink's live-network measurement: "the SINR measurements reveal a median value of 0 dB," giving efficiency 0.64 to 0.79 bps/Hz, explicitly attributed to "the coverage-limited nature of the network" ([arXiv 2506.00283](https://arxiv.org/html/2506.00283v2)).
- The DTC link is "constrained by handset power" with ~7 to 9 dB uplink margin ([arXiv 2605.05843](https://arxiv.org/html/2605.05843v1)); NTN links generally "operate close to the saturation level of their power amplifiers" because of "the very small link budget" ([Ericsson Technology Review](https://www.ericsson.com/en/reports-and-papers/ericsson-technology-review/articles/satellite-direct-to-device-communication); [3GPP TR 38.821](https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf)).
- This is the corpus's own link-budget finding restated: the bare phone supplies nothing and the signal arrives ~25 dB short, closed only by the satellite (COMM-294). A ~0 dB link has NO MCS headroom: at ~0 dB the 3GPP NR MCS table pins the link to low-order QPSK at ~0.5 to 0.8 bps/Hz ([WirelessBrew MCS table](https://www.wirelessbrew.com/tools/mcs-table/), [arXiv 2001.10309](https://arxiv.org/pdf/2001.10309)), so it cannot absorb a drop in SNR-per-Hz by climbing to a higher MCS. It is maximally exposed to the wideband-spreading penalty.

**Conclusion [DERIVED + FACT].** Because DTC-to-phone is power-limited at ~0 dB, widening the owned channel at FIXED power does NOT scale the rate linearly; the efficiency falls as the channel widens, the rate rises sub-linearly, and it saturates at the power-set ceiling C_infinity = 1.44 x P/N0. The corpus's "linear at constant efficiency" is the BANDWIDTH-LIMITED case, which a DTC handset link is NOT in unless power is grown with bandwidth.

### 2.2 The two curves (the model must state which one it is on)

**Case A, constant-efficiency (power grows with bandwidth to hold the PSD): rate is LINEAR.** This is the corpus's stated method (R = B x SE at ~2 to 3 bps/Hz, COMM-374) and it is correct ONLY if the array raises EIRP ~proportionally to B (Section 3). Single-phone rate:

| Owned bandwidth | at 2 bps/Hz | at 2.5 bps/Hz | at 3 bps/Hz | Tag |
|---|---|---|---|---|
| 25 MHz | 50 Mbps | 62.5 Mbps | 75 Mbps | [DERIVED] |
| 50 MHz | 100 Mbps | 125 Mbps | 150 Mbps | [DERIVED] |
| 100 MHz | 200 Mbps | 250 Mbps | 300 Mbps | [DERIVED] |
| 200 MHz | 400 Mbps | 500 Mbps | 600 Mbps | [DERIVED] |

**Case B, fixed-power (the founder's exact concern): rate SATURATES.** Anchor SNR = 1 (0 dB) at 25 MHz (Starlink's measured base), hold total power fixed, widen the channel. SNR-per-Hz falls as 1/B, efficiency = log2(1+SNR) falls ~half per doubling, and the rate asymptotes to 1.44x the 25 MHz rate. Single-phone rate (computed in this doc, verified to 3 decimals by an independent sub-agent and cross-checked against the founder's own arithmetic):

| Owned bandwidth | Bandwidth multiple | SNR-per-Hz (fixed power) | Efficiency = log2(1+SNR) | Rate = B x efficiency | Rate vs 25 MHz | Tag |
|---|---|---|---|---|---|---|
| 25 MHz | 1x | 1.000 | 1.000 bps/Hz | ~25 Mbps | 1.000x | [DERIVED] |
| 50 MHz | 2x | 0.500 | 0.585 bps/Hz | ~29 Mbps | 1.170x | [DERIVED] |
| 100 MHz | 4x | 0.250 | 0.322 bps/Hz | ~32 Mbps | 1.288x | [DERIVED] |
| 200 MHz | 8x | 0.125 | 0.170 bps/Hz | ~34 Mbps | 1.359x | [DERIVED] |
| infinity | infinity | 0 | 0 | ~36 Mbps | **1.443x (hard ceiling)** | [DERIVED] |

The asymptote is exactly log2(e) = 1.4427x the 25 MHz rate ([FACT, the wideband Shannon limit, Section 2.1]). So at fixed power, going 25 -> 200 MHz (8x the spectrum) buys only ~1.36x the rate to one phone, and NOTHING done to bandwidth can exceed ~1.44x. The base efficiency here is taken as 1.0 bps/Hz (SNR = 1) for clean arithmetic; at the realistic Starlink-measured base of ~0.6 bps/Hz the absolute Mbps scale down proportionally but the SHAPE (sub-linear, ~halving per octave, saturating near 1.36 to 1.44x) is unchanged. [DERIVED, multi-source physics: the concavity-of-capacity-in-bandwidth result, [Forney Ch.4](https://ocw.mit.edu/courses/6-451-principles-of-digital-communication-ii-spring-2005/b286123989945cef13e5a9aa20e56a18_chap4.pdf), [Tse and Viswanath Ch.5](https://web.stanford.edu/~dntse/Chapters_PDF/Fundamentals_Wireless_Communication_chapter5.pdf)]

> **The single most important line for the founder.** The bandwidth dial is linear ONLY in Case A (power grown with bandwidth). At fixed power (Case B) it saturates fast: 8x the spectrum buys ~1.36x the rate to one phone, capped at ~1.44x. The truth is between the two, set by how much extra power the array can spend, which is Section 3. The corpus's "25 -> 200 MHz is linear" is the OPTIMISTIC Case A and must carry the power caveat.

### 2.3 What the saturation does NOT prevent (the countervailing factors, so this is balanced)

The fixed-power saturation bites the rate to ONE phone on a wide channel. It does NOT make wide spectrum worthless, for two sourced reasons:
1. **More spectrum serves MORE users, not one user faster.** Carrier aggregation's headline benefit is aggregate capacity: each added channel can carry an ADDITIONAL power-limited user at the same low efficiency, so the per-CELL aggregate throughput can still rise with bandwidth even though a single power-limited link's per-Hz efficiency falls ([Ericsson, 5G carrier aggregation](https://www.ericsson.com/en/blog/2021/6/what-why-how-5g-carrier-aggregation); [Inseego](https://inseego.com/resources/5g-glossary/what-is-carrier-aggregation/)). The beam's total bits/s is power-capped, but spreading that capacity over more users (each at ~500 kbps to a few Mbps) is exactly the DTC use case (Section 1.2). [FACT]
2. **Frequency-selective scheduling (multi-user diversity).** A wider channel lets an OFDMA scheduler hand each user its best sub-bands, raising effective efficiency ([arXiv 1201.6282](https://arxiv.org/abs/1201.6282)). BUT this needs multiple users and a frequency-selective channel; for a SINGLE user on a near-line-of-sight LEO link it largely vanishes ([arXiv 1112.6117](https://arxiv.org/pdf/1112.6117), which also warns too much selectivity can REDUCE throughput). So it does not rescue the single-phone wide-channel rate. [FACT, with limiter]

AST's own analysis states the conclusion directly: Block 2 satellites "operate near the practical limits of antenna size and radiated power," so "expanded bandwidth appears to be the most viable path to increased D2D throughput," with per-Hz efficiency "constrained by link budget limitations in satellite-to-handheld scenarios" ([arXiv 2506.18672](https://arxiv.org/html/2506.18672v1)). In other words: bandwidth raises AGGREGATE (more users) capacity even when per-Hz efficiency is pinned low; it does not raise the single-power-limited-user rate without more power. [FACT]

---

## 3. Power vs bandwidth: which binds, and where does power start to bind?

The founder's exact question. Section 2 established that holding linear scaling requires growing power with bandwidth. This section bounds the satellite power against the real DTC analogs and states where power becomes the wall.

### 3.1 The rule: holding efficiency as bandwidth grows requires EIRP to scale with bandwidth

To keep the power-spectral-density (W/Hz) constant as B goes 25 -> 200 MHz (so SNR-per-Hz and thus efficiency hold), the satellite must raise total transmit power PROPORTIONALLY to B: 8x the bandwidth needs ~8x the EIRP/radiated power, all else equal. [FACT, the direct consequence of SNR = P/(N0 x B): to hold SNR fixed while B grows 8x, P must grow 8x; corroborated by the power-limited-regime physics, Section 2.1]. Equivalently, in the power-limited regime Forney's deep-space example: "increasing P/N0 by 3 dB will double the achievable rate" ([Forney Ch.4](https://ocw.mit.edu/courses/6-451-principles-of-digital-communication-ii-spring-2005/b286123989945cef13e5a9aa20e56a18_chap4.pdf)). Power, not bandwidth, is the rate lever once the link is power-limited.

### 3.2 The satellite-power bounds from the real DTC analogs

The load-bearing empirical part: bound a flat ~25 m^2 entrant's radiated power from the two flying DTC systems, using their FCC engineering filings (the cleanest primary numbers).

**AST SpaceMobile BlueBird (FCC technical narrative, the high-power anchor):**
- Array: Block 1 = ~64.4 m^2 (693 sq ft); Block 2 = ~199 m^2 in the FCC filing (marketing says ~223 m^2) [FACT, [FCC id=376295](https://apps.fcc.gov/els/GetAtt.html?id=376295); discrepancy noted].
- **Total satellite RF power = 1,660 W (32.2 dBW)**, shared across all beams; per-beam total radiated power = 10 dBW (10 W) x 160 simultaneous beams = 1,600 W [FACT, FCC id=376295]. RF power per m^2 of array = 1,660 / 199 = ~8.3 W/m^2 [DERIVED].
- **Solar: ~30 m^2 of silicon cells** [FACT, FCC id=376295], i.e. ~5 to 9 kW total generation (30 m^2 x ~180 to 300 W/m^2) [DERIVED]. (The investor/press "100 to 120 kW" figure is single-tweet-source and contradicts AST's own filed 30 m^2 solar area; it is rejected here.)
- **Downlink EIRP density (per beam, 800 MHz band): roughly +44 to +56 dBW/MHz** depending on array gain (35/41/47 dBi); per-beam total EIRP ~45 to 57 dBW [FACT FCC + DERIVED unit conversion]. AST designs to the FCC OOBE PFD limit, computing -124.5 dBW/m^2/MHz (4.5 dB margin under the -120 limit) [FACT, FCC].
- Bands: low-band cellular 699 to 960 MHz plus PCS/S-band ~1,980 to 1,995 MHz [FACT, FCC].

**Starlink Direct-to-Cell (~25 m^2, the closest analog to the entrant):**
- Array: phased array cited ~25 m^2-class [FACT, multi-source; note a quoted "2.7 x 2.3 m" panel is ~6.2 m^2 geometrically, which does not reconcile with "25 m^2," an unresolved sources looseness, flagged].
- **Peak EIRP = 58 dBW; peak EIRP density = +57.7 dBW/MHz (-2.33 dBW/Hz per 1.4 MHz channel); peak antenna gain = 38 dBi** [FACT, single-source-origin: [SpaceX FCC Gen2 D2C Technical Narrative SAT-MOD-20230207-00021](https://fcc.report/IBFS/SAT-MOD-20230207-00021)].
- **MEASURED median SINR to an unmodified phone = 0 dB (SNR ~ 1)**, median RSRP = -121 dBm (24 dB below terrestrial) [FACT, measured, [arXiv 2506.00283](https://arxiv.org/abs/2506.00283)]. This is the empirical anchor for the whole knee analysis: the real handset link sits AT the 0-dB base over a ~5 MHz channel.
- **Bus/transmit power to the D2C payload: [UNKNOWN]**, not disclosed in the filings. Power-per-m^2: [UNKNOWN].
- Per-beam rate ~3.1 Mbps over one 5 MHz PCS channel -> measured efficiency ~0.52 to 0.61 bps/Hz (3.1/5 = 0.62) [FACT, [arXiv 2506.00283](https://arxiv.org/html/2506.00283v7)].

### 3.3 Where POWER starts to bind for a flat ~25 m^2 entrant (the answer)

Anchor: Starlink delivers SNR ~ 1 (0 dB) to a phone from a ~25 m^2 array over ONE ~5 MHz channel at peak EIRP density ~+57.7 dBW/MHz. AST, at ~199 m^2 (8x the area) and a 1,660 W / 160-beam budget, achieves SNR ~ 1 to a few over 10 MHz beams. The entrant is Starlink-class in aperture (~25 m^2), so it is Starlink-class in achievable EIRP density per beam, NOT AST-class. Because holding efficiency as bandwidth grows requires power to scale ~linearly with B (Section 3.1), and a ~25 m^2 flat array has a roughly fixed EIRP-density ceiling (set by array area x element power), spreading the same total power over more hertz drops the PSD as 1/B [ESTIMATE, anchored to the Starlink measurement]:

| Owned bandwidth | Relative to Starlink's ~5 MHz at SNR ~1 | Power to hold ~1 to 2 bps/Hz across the band | Binding limit | Tag |
|---|---|---|---|---|
| 25 MHz | ~5x the Hz | ~5 to 10x Starlink's per-beam power | BANDWIDTH-limited (power can still hold the PSD if budget is generous); marginal-to-tight at ~2 to 3 bps/Hz | [ESTIMATE] |
| 50 MHz | ~10x the Hz | ~10x Starlink's per-beam power | TRANSITION (power begins to bind) | [ESTIMATE] |
| 100 MHz | ~20x the Hz | ~20x Starlink's per-beam power | POWER-limited (a ~25 m^2 flat array cannot plausibly radiate that PSD; efficiency forced below ~0.3 bps/Hz) | [ESTIMATE] |
| 200 MHz | ~40x the Hz | ~40x Starlink's per-beam power | POWER-limited (deep in saturation; rate ~1.36x the 25 MHz rate regardless of bandwidth) | [ESTIMATE] |

**Verdict [ESTIMATE, the load-bearing finding]: power starts to bind in roughly the ~50 to 100 MHz region** for a fixed-power ~25 m^2 array anchored to the Starlink 0-dB measurement. Below ~50 MHz the array can keep the PSD high enough to stay near ~1 to 2 bps/Hz IF its power budget is generous (so the model is BANDWIDTH-limited and more spectrum is the lever, rate roughly linear). Past ~100 MHz the PSD is forced down so far that efficiency falls below ~0.3 bps/Hz and added bandwidth is nearly wasted on a single phone (so the model is POWER-limited and the lever becomes EIRP/power, or serving more users instead of one user faster, Section 2.3). The exact crossover SLIDES with the assumed total power: an AST-class power budget (1,660 W, 160 beams) pushes the knee toward ~100 MHz; a Starlink-class budget pulls it toward ~25 to 50 MHz. [ESTIMATE]

**The load-bearing UNKNOWN.** The entrant's total satellite power is UNKNOWN (Flatellite power is unpublished, COMM-330), AND Starlink's D2C bus/transmit power is UNKNOWN (not in the filings). So the exact knee bandwidth is bounded (~50 to 100 MHz) but not pinned; it is gated by the entrant's power budget, which the founder must set (per the ask-the-founder-for-assumptions rule). What IS firm: the binding limit FLIPS from bandwidth to power somewhere in that band, and at fixed power the rate to one phone cannot exceed ~1.44x the 25 MHz rate no matter how much spectrum is acquired. [UNKNOWN on the exact knee; FACT on the flip and the ceiling]

### 3.4 Does a regulatory PFD / EIRP-density cap bind first? No (in-band)

A separate question: is the binding PSD limit REGULATORY rather than the satellite's raw power? Checked against the FCC SCS rules:
- **In-band: NO.** The FCC SCS Report and Order (FCC 24-28, March 2024) explicitly DECLINED to impose in-market in-band downlink PFD limits ("we decline to impose in-market downlink PFD limits at this time"); in-band power is left to private contract with the terrestrial spectrum partner ([FCC 24-28](https://docs.fcc.gov/public/attachments/FCC-24-28A1.pdf)). So the in-coverage carrier's PSD is bounded by the satellite's raw power and the lease, not a regulatory in-band ceiling. [FACT]
- **Out-of-band: a cap exists and bites only indirectly.** The R&O adopted an aggregate OOBE PFD limit of -120 dBW/m^2/MHz at 1.5 m above ground (47 CFR 25.202(k)(1)); SpaceX testified that meeting -120 would force it to roughly halve in-band power (~20% throughput hit) and won a waiver to -110.6 dBW/m^2/MHz for the channel adjacent to PCS G-block ([DA-25-197](https://docs.fcc.gov/public/attachments/DA-25-197A1.pdf)). This governs OOBE LEAKAGE and border field strength, not the in-band carrier. [FACT]

**Net [FACT]:** the regulatory PFD cap does NOT bind the in-band downlink PSD before the satellite's own power does. The wall the founder hits as he turns up the bandwidth dial is the array's radiated power (beginning ~50 to 100 MHz), not a PFD rule. The OOBE limit is a second-order tax on achievable in-band power via the emission mask (the mechanism SpaceX litigated), not the first-order limiter.

---

## 4. So what (for the Neutron DTC model)

1. **The 25 MHz operating point is confirmed.** Single-phone PEAK ~25 to 50 Mbps (efficiency-driven, ~15 to 20 Mbps at Starlink-grade ~0.6 bps/Hz, ~50 to 75 Mbps at AST-grade ~3 bps/Hz), sustained per-USER ~20 to 30 Mbps at 2 to 4 active users falling to ~1 Mbps or less busy. No independent datapoint contradicts the corpus. [FACT]
2. **The bandwidth dial is LINEAR only if power grows with it.** At constant efficiency (Case A, power scaled with B) the rate is linear: 25 -> 200 MHz takes a single phone from ~50 to 75 Mbps to ~400 to 600 Mbps. At FIXED power (Case B) the rate SATURATES: 8x the spectrum buys only ~1.36x the rate, hard-capped at ~1.44x = log2(e) the 25 MHz rate, because a DTC-to-phone link is power-limited at the measured ~0 dB SNR. The model MUST state which branch it is on. [DERIVED, multi-source physics]
3. **POWER, not bandwidth, becomes the binding limit as the channel widens.** Holding efficiency as B grows 25 -> 200 MHz needs EIRP to scale ~8x. Bounded against AST (1,660 W RF, ~199 m^2) and Starlink D2C (~25 m^2, +57.7 dBW/MHz peak), a flat ~25 m^2 entrant is Starlink-class in EIRP density, so its fixed power is spread below ~1 to 2 bps/Hz in the ~50 to 100 MHz region. **The model is BANDWIDTH-limited at ~25 to 50 MHz (more spectrum is the lever, rate roughly linear) and flips to POWER-limited past ~50 to 100 MHz (more spectrum stops buying single-phone rate; the lever is power, or serving more users).** [ESTIMATE + FACT]
4. **Wide spectrum still has value, but as AGGREGATE capacity (more users), not single-phone peak.** Carrier aggregation lets each added channel carry another power-limited user at the same low efficiency, so the per-cell pool grows with bandwidth even when the per-Hz efficiency is pinned. AST's own conclusion: bandwidth is "the most viable path to increased D2D throughput" precisely because the satellites are at the power/aperture limit. [FACT]
5. **The regulatory PFD cap does not bind the in-band rate first.** The FCC declined in-band downlink PFD limits; only OOBE leakage (-120 dBW/m^2/MHz) and border field strength are capped, a second-order tax. The binding wall is the array's power. [FACT]
6. **No verdict.** This doc pins the rate-vs-owned-spectrum curve and the power-vs-bandwidth limit. Whether the business closes depends on the owned-spectrum position (~25 MHz here vs the ~100 to 200 MHz competitive benchmark, COMM-325/236), the satellite power budget (the load-bearing UNKNOWN, COMM-330), the per-phone rate and per-cell capacity (the corpus), the active-user density (UNKNOWN), and the launch economics, none assessed here.

---

## 5. Open questions / named gaps

1. **The entrant's total satellite power is the load-bearing UNKNOWN.** The exact bandwidth where power starts to bind (~50 to 100 MHz) is gated by the flat ~25 m^2 array's total radiated/DC power, which is unpublished (COMM-330), AND Starlink's D2C bus/transmit power is also undisclosed, so the anchor itself is partly inferred from EIRP density rather than raw watts. The founder must set the assumed satellite power budget; the knee slides toward ~100 MHz with an AST-class budget and toward ~25 to 50 MHz with a Starlink-class budget. [UNKNOWN, founder assumption]
2. **The base efficiency at 25 MHz (the curve's anchor) has a real spread.** The fixed-power saturation table anchors SNR = 1 (1.0 bps/Hz) for clean arithmetic, but the MEASURED Starlink base is ~0.5 to 0.8 bps/Hz; the SHAPE of the saturation is unchanged, but the absolute Mbps scale with the chosen base efficiency, which is itself a function of the (unknown) array gain and power. [ESTIMATE / spread flagged]
3. **No published SE-vs-bandwidth curve for a satellite-to-phone link exists.** The 25/50/100/200 MHz saturation table is DERIVED from first principles (SNR ~ 1/B in the power-limited regime); the SHAPE (concave, ~halving per octave, saturating near 1.44x) is multi-source-confirmed from the textbook concavity-of-capacity result, but no source publishes the exact per-step DTC numbers, so the specific table is a derivation, not a measurement. [DERIVED, no direct measurement]
4. **The single-phone-peak FLOOR is efficiency-soft.** Under Starlink-measured efficiency (~0.5 to 0.6 bps/Hz) on 25 MHz a single phone might see only ~13 to 18 Mbps, just under the corpus 25 Mbps floor; the ~25 to 50 Mbps band assumes the array achieves better-than-Starlink efficiency (~2 to 3 bps/Hz), which is reasonable for a large dedicated cellular array but is the load-bearing assumption. [ESTIMATE]
5. **The Starlink ~25 m^2 array area is loosely sourced**, and a quoted ~2.7 x 2.3 m panel does not reconcile geometrically with "~25 m^2"; this is the same softness the corpus already flags (COMM-303). It affects the per-m^2 power anchor for the entrant bound. [FACT, but the area is soft]
6. **The AST EIRP-density-to-rate mapping is order-of-magnitude.** AST's ~+44 to +56 dBW/MHz and 1,660 W RF are FCC-filed, but the conversion to "efficiency held across a wide channel" mixes the per-beam (10 MHz) figures with the entrant's wider-channel case; it bounds the entrant but is not an apples-to-apples transfer. [ESTIMATE]

---

## Sources

**Power-limited regime physics, the wideband Shannon limit (textbook):**
- [Forney, MIT OCW 6.451 Principles of Digital Communication II, Chapter 4: power-limited vs bandwidth-limited regimes, the rho ~ 2 bps/Hz boundary, Eb/N0 > ln2 = -1.59 dB ultimate Shannon limit, the deep-space "increase P/N0 by 3 dB to double the rate" example](https://ocw.mit.edu/courses/6-451-principles-of-digital-communication-ii-spring-2005/b286123989945cef13e5a9aa20e56a18_chap4.pdf)
- [Wikipedia: Shannon-Hartley theorem, bandwidth-limited and power-limited cases (C approx 1.44 x S/N0, capacity independent of bandwidth when noise is white)](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem)
- [dsplog: Bounds on communication based on Shannon's capacity (increasing bandwidth alone does not increase capacity; C = 1.44 x Ps/N0)](https://dsplog.com/2008/06/18/bounds-on-communication-shannon-capacity/)
- [Tse and Viswanath, Fundamentals of Wireless Communication, Ch.5: capacity = Theta(P/N0) in the power-limited regime, virtually independent of bandwidth; capacity concave in bandwidth](https://web.stanford.edu/~dntse/Chapters_PDF/Fundamentals_Wireless_Communication_chapter5.pdf)
- [arXiv 0812.1553: Energy Efficiency in Fading Channels under QoS Constraints (SNR = P/(N0 B), spectral efficiency decreases as bandwidth increases, low-SNR regime)](https://arxiv.org/pdf/0812.1553)
- [ScienceDirect, System Spectral Efficiency: power-limited (SE << 1) vs bandwidth-limited (SE >> 1); transmitter power inversely proportional to bandwidth slices](https://www.sciencedirect.com/topics/engineering/system-spectral-efficiency)
- [Eb/N0, Wikipedia (Shannon-limit -1.59 dB value)](https://en.wikipedia.org/wiki/Eb/N0)

**SE-vs-SNR / 3GPP MCS-AMC ladder:**
- [WirelessBrew, 5G NR MCS table reference (MCS0 = 0.2344 bps/Hz QPSK up to 5.55/7.40 bps/Hz)](https://www.wirelessbrew.com/tools/mcs-table/)
- [arXiv 2001.10309: NR Physical Layer Abstraction for System-Level Simulations (MCS SE values, Table 1/Table 2)](https://arxiv.org/pdf/2001.10309)
- [NXG Connect: Link Adaptation in 5G NR (QPSK for low SNR, higher QAM for high SNR)](https://www.nxgconnect.com/post/link-adaptation-in-5g-nr)

**DTC-to-phone is power/coverage-limited at ~0 dB SINR (measurement + NTN):**
- [arXiv 2506.00283: Direct-to-Cell, Starlink crowdsourced measurements (median SINR 0 dB, mean 0.79 / median 0.64 bps/Hz, 3.1 Mbps/beam on 2x5 MHz, single-user-occupies-beam bound, coverage-limited)](https://arxiv.org/html/2506.00283v2)
- [arXiv 2605.05843: Comparative Analysis of Direct-to-Cell (D2C) and 3GPP NTN (D2C constrained by handset power, ~7-9 dB uplink margin, small-link-budget rates)](https://arxiv.org/html/2605.05843v1)
- [Ericsson Technology Review: Satellite direct to device (NTN operates near power-amplifier saturation due to very small link budget)](https://www.ericsson.com/en/reports-and-papers/ericsson-technology-review/articles/satellite-direct-to-device-communication)
- [3GPP TR 38.821 (NTN link budget more limited; MCS/TBS must account for limited link budget)](https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf)

**Countervailing factors (scheduling diversity, aggregate-capacity-vs-one-user):**
- [arXiv 1201.6282: Frequency-Selective Scheduling Gain in SDMA-OFDMA Systems](https://arxiv.org/abs/1201.6282)
- [arXiv 1112.6117: Optimal frequency selectivity for multiuser diversity (an optimum exists; too much selectivity reduces throughput)](https://arxiv.org/pdf/1112.6117)
- [Ericsson: What, why, how 5G carrier aggregation (aggregate capacity, more users)](https://www.ericsson.com/en/blog/2021/6/what-why-how-5g-carrier-aggregation)
- [arXiv 2506.18672: Spectrum Opportunities for the Wireless Future (AST near practical power/antenna limits, expanded bandwidth the most viable path; 120 Mbps = 40 MHz x 3 bps/Hz; 500 kbps/user at 5% load)](https://arxiv.org/html/2506.18672v1)

**Satellite power / EIRP bounds (FCC filings):**
- [FCC ELS id=376295: AST FM1/Block-2 technical narrative (1,660 W total RF = 32.2 dBW, 10 dBW per beam x 160 beams, ~30 m^2 solar, ~199 m^2 array, EIRP density, -124.5 dBW/m^2/MHz OOBE)](https://apps.fcc.gov/els/GetAtt.html?id=376295)
- [FCC IBFS SAT-MOD-20230207-00021: SpaceX Gen2 Direct-to-Cellular Technical Narrative (peak EIRP 58 dBW, peak EIRP density +57.7 dBW/MHz, peak gain 38 dBi)](https://fcc.report/IBFS/SAT-MOD-20230207-00021)
- [arXiv 2506.00283: Starlink D2C measured RSRP/SINR (the 0-dB anchor)](https://arxiv.org/abs/2506.00283)

**Regulatory PFD / SCS rules:**
- [FCC 24-28: SCS Report and Order (declined in-band downlink PFD limits; OOBE PFD -120 dBW/m^2/MHz)](https://docs.fcc.gov/public/attachments/FCC-24-28A1.pdf)
- [FCC DA-25-197: SpaceX OOBE waiver to -110.6 dBW/m^2/MHz](https://docs.fcc.gov/public/attachments/DA-25-197A1.pdf)

**Rate validation (single-phone and per-user):**
- [AST Next-Gen BlueBird (120 Mbps/cell, 40 MHz/beam, 10 GHz processing)](https://ast-science.com/next-gen-bluebird/)
- [TelecomTalk: AST Block 1 98.9 Mbps to a standard phone](https://telecomtalk.info/ast-spacemobile-100mbps-broadband-space-standard-phone/1007598/)
- [TechTimes: AST Block 2 to orbit (device peaks, link-budget framing)](https://www.techtimes.com/articles/318740/20260620/ast-spacemobile-block-2-bluebirds-reach-orbit-satellite-broadband-direct-your-phone-nears.htm)
- [WIA/TMF white paper (Farrar): D2D below 1 Mbps today, 4G-LTE-like outdoors not 5G](https://wia.org/wp-content/uploads/2025/05/TMF-White-Paper-on-Satellite-D2D_October-2025.pdf)
- [npj Wireless Technology / Rappaport et al. (peer-reviewed version of arXiv 2506.18672)](https://www.nature.com/articles/s44459-025-00008-9)
- [NextBigFuture: FCC allows Starlink D2C 4G/5G power (Starlink rate targets)](https://www.nextbigfuture.com/2025/03/fcc-allows-spacex-starlink-direct-to-cellphone-power-for-4g-5g-speeds.html)
- *(The corpus's own per-phone, per-cell, aperture, latency, and spectrum-access claims are cross-referenced from [`dtc_per_phone_rate_and_latency.md`](dtc_per_phone_rate_and_latency.md), [`dtc_capacity_supply.md`](dtc_capacity_supply.md), [`dtc_antenna_aperture_tradeoff.md`](dtc_antenna_aperture_tradeoff.md), [`spectrum_capacity_primer.md`](spectrum_capacity_primer.md), and [`dtc_spectrum_access.md`](dtc_spectrum_access.md); not re-listed.)*

---

## Claims ledger (COMM-493..520)

For the catalog/reconciliation step to ingest. Each hard claim with sources and tag; single-source, projection, and estimate claims flagged. IDs COMM-493 through COMM-520 reserved for this doc. The block COMM-451..492 is already held by [`dtc_spectrum_access.md`](dtc_spectrum_access.md), so COMM-493 is the next free contiguous start above the global max (COMM-492); the ceiling is not exceeded. Cross-references existing IDs heavily.

- **COMM-493**, The single-phone PEAK rate for a flat ~25 m^2 array at ~400 km on ~25 MHz owned spectrum is ~25 to 50 Mbps, well-supported and efficiency-driven: ~15 to 20 Mbps at Starlink-measured ~0.6 bps/Hz, ~50 to 75 Mbps at AST-claimed ~3 bps/Hz; the band assumes the array achieves better-than-Starlink efficiency, the load-bearing assumption. [FACT band; DERIVED central] Sources: AST BW3 ~21 Mbps (Fierce, RCR Wireless), AST Block 1 ~98.9 Mbps (TelecomTalk, TechTimes), Starlink measured ~3.1 Mbps/beam on 2x5 MHz (arXiv 2506.00283); cross-ref COMM-355/375.
- **COMM-494**, DTC single-device demonstration datapoints (triangulation set): AST BW3 ~10/14/21 Mbps (~64 m^2, thin channel), AST Block 1 ~98.9 Mbps, AST Block 2 ~200 Mbps device design, Starlink measured ~3.1 Mbps/beam (~25 m^2-class, 2x5 MHz), Starlink target "up to 100 Mbps" peak; Lynk/Globalstar/Huawei are narrowband with no published single-phone Mbps. [FACT for AST/Starlink; UNKNOWN/single-source for the narrowband systems] Sources: as in COMM-493 plus BusinessWire (Block 2), NextBigFuture (Starlink targets), Wikipedia/Lynk, Apple support (Emergency SOS).
- **COMM-495**, The sustained per-USER rate under load is confirmed multi-source: ~20 to 30 Mbps at 2 to 4 active users per cell (light), falling to ~500 kbps to ~1 Mbps when a cell carries hundreds of active phones; the analyst (Farrar/WIA: "below 1 Mbps... 4G-LTE-like outdoors not 5G"), the academic worked example (Rappaport: 120 Mbps / 240 active = 500 kbps), and Starlink's own beam-sharing math (2 to 100 Mbps/user at 10 to 100 users/beam) all agree. [FACT, multi-source] Sources: WIA/TMF white paper; arXiv 2506.18672 / npj Wireless; arXiv 2506.00283; cross-ref COMM-417/418.
- **COMM-496**, AST's "120 Mbps per cell" = 40 MHz x 3 bps/Hz is confirmed from 2+ independent sources (AST official + Rappaport arXiv); the 25 MHz x efficiency table is ~13 to 15 Mbps at 0.5 to 0.6 (Starlink measured), ~37.5 at 1.5, 50 at 2, 75 at 3 bps/Hz; the efficiency assumption is the entire swing. [FACT + DERIVED] Sources: AST Next-Gen BlueBird; arXiv 2506.18672; arXiv 2506.00283; cross-ref COMM-344/430/431.
- **COMM-497**, FRAMING NUANCE (reconciled, not a contradiction): AST Block 2 is quoted as 120 Mbps PER CELL (shared capacity, 40 MHz x 3) and ~200 Mbps PER DEVICE (best-case single-device peak); the corpus's use of 120 Mbps/cell as the capacity number is the correct conservative choice, and ~200 Mbps is a device peak, not cell capacity. [FACT, reconciled] Sources: AST Next-Gen BlueBird (120/cell); BusinessWire / TechTimes (~200/device); cross-ref COMM-342.
- **COMM-498**, THE CORE PHYSICS: for a fixed received power P, SNR = P / (N0 x B) is INVERSELY proportional to bandwidth, so widening the channel at fixed power lowers the power-spectral-density, lowers SNR-per-Hz, and lowers spectral efficiency. [FACT, multi-source] Sources: arXiv 0812.1553 ("as bandwidth increases, SNR = P/(N0 B) and spectral efficiency decreases"); ScienceDirect System Spectral Efficiency; cross-ref COMM-427.
- **COMM-499**, Radio links split into two regimes (boundary ~2 bps/Hz): BANDWIDTH-limited (high SNR, efficiency >> 1) where efficiency is ~flat with bandwidth so rate is ~linear in bandwidth, and POWER-limited (low SNR, efficiency << 1) where capacity is linear in power and nearly INDEPENDENT of bandwidth. [FACT, textbook] Sources: Forney MIT OCW 6.451 Ch.4; Wikipedia Shannon-Hartley; Tse and Viswanath Ch.5.
- **COMM-500**, In the power-limited regime, as bandwidth grows at fixed power the capacity converges to a hard ceiling set ENTIRELY by power: C_infinity = (P/N0) x log2(e) = 1.44 x (P/N0), the wideband / infinite-bandwidth Shannon limit; the ultimate Eb/N0 floor is ln2 = -1.59 dB. Forney's deep-space example: "increasing P/N0 by 3 dB will double the achievable rate," i.e. rate tracks POWER not bandwidth once power-limited. [FACT, textbook] Sources: Wikipedia Shannon-Hartley (power-limited case); dsplog; Forney Ch.4; Eb/N0 Wikipedia.
- **COMM-501**, A DTC-to-phone link is POWER-LIMITED near-maximally: it sits at a MEASURED median SINR of 0 dB (SNR ~ 1) in Starlink's live network, explicitly "coverage-limited"; NTN links "operate close to power-amplifier saturation" due to the "very small link budget"; at ~0 dB the 3GPP NR MCS table pins the link to low-order QPSK (~0.5 to 0.8 bps/Hz) with no headroom to absorb a drop in SNR-per-Hz. So the wideband-spreading penalty applies near-maximally. [FACT, multi-source] Sources: arXiv 2506.00283 (median SINR 0 dB); arXiv 2605.05843, Ericsson, 3GPP TR 38.821 (power-limited NTN); WirelessBrew MCS table; cross-ref COMM-294/429.
- **COMM-502**, THE RATE-vs-BANDWIDTH FORK: rate is LINEAR in owned bandwidth ONLY in Case A (power grown proportionally to bandwidth to hold the power-spectral-density and thus the efficiency); at FIXED power (Case B) the rate SATURATES, because a DTC-to-phone link is power-limited. The corpus's "linear in bandwidth at constant efficiency" (COMM-374/430) is the OPTIMISTIC Case A and must carry the power caveat. [DERIVED + FACT] Sources: this doc Section 2; COMM-498..501; corpus COMM-348/374/378.
- **COMM-503**, CASE A (constant efficiency, power scaled with bandwidth) single-phone rate, R = B x efficiency at 2 to 3 bps/Hz: 25 MHz -> 50 to 75 Mbps, 50 MHz -> 100 to 150, 100 MHz -> 200 to 300, 200 MHz -> 400 to 600 Mbps; valid ONLY while the array can raise EIRP ~proportionally to B. [DERIVED] Sources: this doc Section 2.2; cross-ref COMM-374.
- **COMM-504**, CASE B (fixed power) single-phone rate, anchoring SNR = 1 (0 dB) at 25 MHz: efficiency falls ~half per doubling (50 MHz 0.585, 100 MHz 0.322, 200 MHz 0.170 bps/Hz), so rate is 25 MHz ~25 Mbps, 50 MHz ~29 (1.17x), 100 MHz ~32 (1.29x), 200 MHz ~34 Mbps (1.36x), asymptoting to exactly 1.443x = log2(e) the 25 MHz rate; 8x the spectrum buys only ~1.36x the rate to one phone, hard-capped at ~1.44x. The shape is unchanged at the realistic ~0.6 bps/Hz base, only the absolute Mbps scale. [DERIVED, arithmetic verified to 3 decimals] Sources: this doc Section 2.2; concavity result Forney Ch.4, Tse and Viswanath Ch.5; COMM-500.
- **COMM-505**, The fixed-power saturation bites the rate to ONE phone on a wide channel; it does NOT make wide spectrum worthless, because (a) carrier aggregation lets each added channel carry ANOTHER power-limited user at the same low efficiency, so the per-CELL aggregate grows with bandwidth (AST: "expanded bandwidth is the most viable path"), and (b) frequency-selective scheduling raises effective efficiency over a wide channel BUT needs multiple users and a frequency-selective channel, so it largely vanishes for a single user on a near-line-of-sight LEO link. [FACT, with limiter] Sources: Ericsson 5G carrier aggregation; Inseego; arXiv 2506.18672 (AST); arXiv 1201.6282, arXiv 1112.6117 (scheduling diversity + its optimum/limiter).
- **COMM-506**, THE POWER RULE: to hold spectral efficiency constant as bandwidth grows 25 -> 200 MHz (so SNR-per-Hz holds), the satellite must raise total transmit power PROPORTIONALLY to B (8x the bandwidth needs ~8x the EIRP, all else equal); power, not bandwidth, is the rate lever once the link is power-limited. [FACT, direct consequence of SNR = P/(N0 x B)] Sources: this doc Section 3.1; Forney Ch.4 (3 dB doubles rate); COMM-498/500.
- **COMM-507**, AST BlueBird power anchor (FCC technical narrative): total satellite RF power = 1,660 W (32.2 dBW), per-beam 10 dBW (10 W) x 160 beams; ~30 m^2 of silicon solar (~5 to 9 kW generation, NOT the single-tweet 100 to 120 kW); ~199 m^2 array (marketing ~223 m^2); RF power ~8.3 W/m^2 of array; downlink EIRP density ~+44 to +56 dBW/MHz per beam; designs to -124.5 dBW/m^2/MHz OOBE. [FACT, FCC; DERIVED for per-m^2 and solar watts] Source: FCC ELS id=376295.
- **COMM-508**, Starlink Direct-to-Cell power anchor (FCC technical narrative): ~25 m^2-class array, peak EIRP 58 dBW, peak EIRP density +57.7 dBW/MHz, peak gain 38 dBi; MEASURED median SINR to a phone = 0 dB over a ~5 MHz channel; bus/transmit power to the D2C payload is UNKNOWN (not in the filings); per-beam ~3.1 Mbps on 5 MHz = ~0.6 bps/Hz measured. [FACT for EIRP/gain (single-source-origin SpaceX FCC); UNKNOWN for bus power; FACT for the 0-dB measurement] Sources: FCC IBFS SAT-MOD-20230207-00021; arXiv 2506.00283.
- **COMM-509**, WHERE POWER BINDS (the answer): anchored to Starlink delivering SNR ~ 1 over ~5 MHz from a ~25 m^2 array at +57.7 dBW/MHz, a flat ~25 m^2 entrant is Starlink-class (not AST-class) in EIRP density, so holding ~1 to 2 bps/Hz needs ~5 to 10x Starlink's per-beam power at 25 MHz, ~20x at 100 MHz, ~40x at 200 MHz; its fixed power is spread below ~1 to 2 bps/Hz in the ~50 to 100 MHz region. The model is BANDWIDTH-limited at ~25 to 50 MHz (more spectrum is the lever, rate roughly linear) and flips to POWER-limited past ~50 to 100 MHz (more spectrum stops buying single-phone rate). [ESTIMATE, load-bearing] Sources: this doc Section 3.3; anchors COMM-507/508; COMM-500/506.
- **COMM-510**, The exact knee bandwidth is bounded (~50 to 100 MHz) but NOT pinned, gated by the entrant's total satellite power (UNKNOWN, Flatellite power unpublished COMM-330) and Starlink's undisclosed D2C bus power; the knee slides toward ~100 MHz with an AST-class budget (1,660 W, 160 beams) and toward ~25 to 50 MHz with a Starlink-class budget. What is firm: the binding limit FLIPS from bandwidth to power in that band, and at fixed power the single-phone rate cannot exceed ~1.44x the 25 MHz rate regardless of spectrum acquired. [UNKNOWN on the knee; FACT on the flip and ceiling] Sources: this doc Section 3.3; cross-ref COMM-330; COMM-500/504/509.
- **COMM-511**, The regulatory PFD cap does NOT bind the in-band downlink rate first: the FCC SCS Report and Order (FCC 24-28) explicitly DECLINED in-market in-band downlink PFD limits (in-band power set by the lease/partner, not a rule), capping only OOBE leakage at -120 dBW/m^2/MHz (SpaceX won a waiver to -110.6) and border field strength; the binding wall on in-band PSD is the array's own radiated power, with OOBE a second-order tax via the emission mask. [FACT] Sources: FCC 24-28; FCC DA-25-197.
- **COMM-512**, Net rate-vs-spectrum picture for the Neutron DTC model: the 25 MHz operating point (~25 to 50 Mbps single-phone, ~20 to 30 Mbps per-user light) is confirmed; the bandwidth dial is linear (Case A, to ~400 to 600 Mbps at 200 MHz) ONLY if power grows with it, and saturates at fixed power (Case B, ~34 Mbps at 200 MHz, capped at ~1.44x the 25 MHz rate); power becomes the binding limit past ~50 to 100 MHz; wide spectrum retains value as AGGREGATE (more-users) capacity not single-phone peak; and the regulatory PFD cap does not bind in-band first. The load-bearing UNKNOWN is the satellite power budget. No verdict. [DERIVED/SYNTHESIS] Sources: this doc Sections 0, 4; grounds in COMM-493..511, corpus COMM-330/348/374/417.

---

*COMM-493..520 reserved for this doc (COMM-493..512 used; COMM-513..520 held in reserve, ceiling not exceeded). The block COMM-451..492 was already held by [`dtc_spectrum_access.md`](dtc_spectrum_access.md), so COMM-493 is the next free contiguous start above the global max. Catalog rows for LIBRARY.md / RESEARCH_TRACKER.md / SOURCE_INDEX.md are returned to the catalog/reconciliation agent, not edited here. This doc is not committed by this pass.*
